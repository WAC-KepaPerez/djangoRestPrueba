from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from base.models import Item
from .serializer import ItemSerializer,CustomUserSerializer,ChangePasswordSerializer,PostSerializer,MyModelSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
import firebase_admin
from firebase_admin import credentials, messaging
import os
from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework import generics
from base.models import Post
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.db import connection
# Initialize Firebase
json_file_path = os.path.abspath("gongo-50bb7-firebase-adminsdk-9nbod-d34b4a74d0.json")

firebase_cred = credentials.Certificate(json_file_path)
firebase_admin.initialize_app(firebase_cred)

class RegisterView(CreateAPIView):
    serializer_class = CustomUserSerializer
    
    permission_classes = [AllowAny]

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer  # Create this serializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check if the current password matches
            if not user.check_password(serializer.data.get('current_password')):
                return Response({'current_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password and save the user
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getItems(request):
    user=request.user
    items=user.item_set.all()
    serializer=ItemSerializer(items,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def pon(request):
    return Response({"pon"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteItem(request,item_id):
    try:
        item = Item.objects.get(id=item_id)
        
        # Check if the user making the request is the owner of the item
        if item.user == request.user:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You are not authorized to delete this item."}, status=status.HTTP_403_FORBIDDEN)
    except Item.DoesNotExist:
        return Response({"message": "Item not found."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def addItem(request):
   # serializer=ItemSerializer(data=request.data)
   #  if serializer.is_valid():
   #      serializer.create()
    # return Response(serializer.data)
    data = request.data
    item = Item.objects.create(
        name=data['name']
    )
    serializer =ItemSerializer(item,many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def updateItem(request,item_id):
    data = request.data
    item = Item.objects.get(id=item_id)
    serializer =ItemSerializer(item,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



@api_view(['GET'])
def getItem(request,item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item)
    return Response(serializer.data)


@api_view(['POST'])
def send_notification(request):
    data = request.data
    
    titulo = data.get('titulo')
    cuerpo = data.get('cuerpo')
    token = data.get('token')
    type= data.get('type')

    if not token or not titulo:
        return Response({'error': 'some data missing'}, status=status.HTTP_400_BAD_REQUEST)

    # Send Firebase notification
    message = messaging.Message(
        token=token,
        android=messaging.AndroidConfig(
            notification=messaging.AndroidNotification(
                title=titulo,
                body=cuerpo,
                icon="myicon",
            ),
        ),
        data={"notificationType": type},
    )

    try:
        response = messaging.send(message)
        print("Notificación enviada con éxito:", response)
        return Response({'okey': 'sendNotification'}, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error al enviar la notificación:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostListView(APIView):

     def get(self, request):
        data = request.data
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM base_post")
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description] 

        if not result:
            return Response({"detail": "Establecimiento no encontrado"}, status=404)
        data = []
        for row in result:
            data_row = {}
            for i, column_name in enumerate(column_names):
                data_row[column_name] = row[i]
            data.append(data_row)

        for item in data:
            if 'image' in item:
                # Assuming your images are stored in the media folder
                static_path = f'/media/{item["image"]}'
                api_url = request.build_absolute_uri(static_path)
                item['api_url'] = api_url

        return Response(data)
    

   
 

class MyModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MyModelSerializer(data=request.data)
        if serializer.is_valid():
            # Step 2: Save the image to a folder
            instance = serializer.save()

            # Step 3: Generate the static path
            static_path = f'/static/{instance.image.name}'  # Adjust based on your project structure
            
            # Step 4: Call the database procedure with the static path
            # Your logic to call the database procedure goes here

            return Response({'static_path': static_path}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)