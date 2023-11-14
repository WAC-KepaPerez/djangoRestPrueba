from django.core.management.commands.inspectdb import Command as InspectDBCommand
from django.core.management.base import CommandError
from django.db import connections

import re

class Command(InspectDBCommand):
    def handle_inspection(self, options):
        connection = connections[self.database]
        introspection = connection.introspection
        table_name_filter = options['table_name_filter']
        tables = introspection.table_names(filter_func=table_name_filter)
        all_models = []
        for table_name in tables:
            try:
                with connection.cursor() as cursor:
                    relations = introspection.get_relations(cursor, table_name)
                    primary_key_column = introspection.get_primary_key_column(cursor, table_name)
                    unique_columns = introspection.get_unique_columns(cursor, table_name)
                    table_description = introspection.get_table_description(cursor, table_name)
            except Exception as e:
                raise CommandError(f"Error: {e}")

            # Modify the generated model fields to match the desired format
            column_to_field_name = lambda column_name: re.sub(r'\W+', '_', column_name)
            model_fields = []
            for row in table_description:
                column_name = row.name
                field_name = column_to_field_name(column_name)
                field_params = f"{field_name} = models.FieldType(db_column='{column_name}')"
                model_fields.append(field_params)

            # Construct the model for this table
            model = f"class {table_name.title().replace('_', '')}(models.Model):\n"
            model += '\n'.join(f"    {field}" for field in model_fields)
            all_models.append(model)

        # Print all generated models
        for model in all_models:
            self.stdout.write(model)
