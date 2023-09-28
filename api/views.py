from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base.models import Item
from .serializer import ItemSerializer

@api_view(['GET'])
def getItems(request):
    items=Item.objects.all()
    serializer=ItemSerializer(items,many=True)
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

@api_view(['DELETE'])
def deleteItem(request,item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return Response("Nore was deleted")