from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from base.models import Nota
from .serializer import NotaSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def getNotas(request):
    notas= Nota.objects.all()
    serializer=NotaSerializer(notas,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addNota(request):
    data = request.data
    user = request.user
    nota = Nota.objects.create(
        value=data['value'],
        user= user
    )
    serializer =NotaSerializer(nota,many=False)
    return Response(serializer.data)

@api_view(['DELETE','PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def notaDetails(request,nota_id):
    nota = Nota.objects.get(id=nota_id)
    user = request.user
    if request.method == 'DELETE':
        nota.delete()
        return Response({"message": "Nota eliminada"},status=status.HTTP_204_NO_CONTENT)
    

    elif request.method in ['PUT', 'PATCH']:
        newNota = request.data
        print(type(newNota))
        newNota["user"]= user.pk
        serializer =NotaSerializer(nota,data=newNota)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
