import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from dotenv import load_dotenv
import os
load_dotenv()

# Access environment variables
PINECODE_API_KEY = os.getenv("PINECODE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
from pinecone import Pinecone,ServerlessSpec
client = OpenAI(api_key=OPENAI_API_KEY)


@api_view(['GET'])
def pon(request):
         return Response({"pon"})


class SubirPost(APIView):
    def post(self, request):
        pc = Pinecone(api_key=PINECODE_API_KEY)
        index = pc.Index('movies') 
        vectors=[]
        body_unicode = request.body.decode('utf-8')
        post = json.loads(body_unicode)
      
        if not request.body:
          return JsonResponse({'error': 'Empty request body'}, status=400)
        try:
            postData=  str(post)
            response = client.embeddings.create(
            input=postData,
            model="text-embedding-3-small"
            )
            print(response.data[0].embedding)
            vectors.append(
              {
              "id": str(post['id']), 
              "values": response.data[0].embedding, 
              "metadata": post
              },
            )
            response=index.upsert(
                vectors=vectors,
            namespace="ns1"
            )
            print(response)
            return Response({'status': "okey"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("An error occurred:", str(e))
            return Response({'status': "error", "error":e}, status=status.HTTP_400_BAD_REQUEST)   





