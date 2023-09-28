from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from base.models import Item
from .serializer import ItemSerializer
from rest_framework.permissions import IsAuthenticated

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
    #item = Item.objects.get(id=item_id)
    #item.delete()
    #return Response("Nore was deleted")

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


@api_view(['GET'])
def getItem(request,item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item)
    return Response(serializer.data)


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

