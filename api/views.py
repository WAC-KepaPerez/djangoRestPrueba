from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from base.models import Item
from .serializer import ItemSerializer
from rest_framework.permissions import IsAuthenticated
import firebase_admin
from firebase_admin import credentials, messaging
import os

# Initialize Firebase
json_file_path = os.path.abspath("gongo-50bb7-firebase-adminsdk-9nbod-d34b4a74d0.json")

firebase_cred = credentials.Certificate(json_file_path)
firebase_admin.initialize_app(firebase_cred)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getItems(request):
    user=request.user
    items=user.item_set.all()
    serializer=ItemSerializer(items,many=True)
    return Response(serializer.data)



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