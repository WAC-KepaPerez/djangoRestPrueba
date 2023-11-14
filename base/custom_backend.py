from django.db.backends.mysql.introspection import DatabaseIntrospection

class CustomMySQLIntrospection(DatabaseIntrospection):
    def get_table_description(self, cursor, table_name):
        # Get the table description from the cursor
        description = super().get_table_description(cursor, table_name)
        
        # Return the description without modifying the column names
        return [
            (info.name, info.type_code, None, None, None, None, None)
            for info in description
        ]