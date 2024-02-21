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



@api_view(['GET'])
def pon(request):
         return Response({"pon"})


class SubirPost(APIView):
  def post(self, request):
    
 

    if not request.body:
      return JsonResponse({'error': 'Empty request body'}, status=400)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    openai_wac_chat_api_key = body['openai_wac_chat_api_key']
    openai_wac_chat_model = body['openai_wac_chat_model']
    openai_wac_chat_token_limit = body['openai_wac_chat_token_limit']
    openai_wac_chat_temperature = body['openai_wac_chat_temperature']
    pinecone_wac_chat_api_key = body['pinecode_wac_chat_api_key']
    post = body['post']
    vectors=[]

    pc = Pinecone(api_key=pinecone_wac_chat_api_key)
    client = OpenAI(api_key=openai_wac_chat_api_key)
    index = pc.Index('movies') 
    
    try:
      postData=  str(post)
      response = client.embeddings.create(
      input=postData,
      model="text-embedding-3-small"
      )
      #print(response.data[0].embedding)
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
      return Response({'status': "succes"}, status=status.HTTP_200_OK)
    except Exception as e:
        print("An error occurred:", str(e))
        return Response({'status': "error", "error":e}, status=status.HTTP_400_BAD_REQUEST)   



class Chat(APIView):
  def post(self, request):
    
    if not request.body:
      return JsonResponse({'error': 'Empty request body'}, status=400)
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    print(body['message'])
    messagesCliente = body['message']
    openai_wac_chat_api_key = body['openai_wac_chat_api_key']
    openai_wac_chat_model = body['openai_wac_chat_model']
    openai_wac_chat_token_limit = body['openai_wac_chat_token_limit']
    openai_wac_chat_temperature = body['openai_wac_chat_temperature']
    pinecone_wac_chat_api_key = body['pinecode_wac_chat_api_key']
    
    pc = Pinecone(api_key=pinecone_wac_chat_api_key)
    index = pc.Index('movies') 
    client = OpenAI(api_key=openai_wac_chat_api_key)


    try:
      responseAI = client.embeddings.create(
        input=str(messagesCliente[-1]), 
        model="text-embedding-3-small"
      )
      vector =responseAI.data[0].embedding

      response = index.query(
        namespace='ns1',
        top_k=5,
        include_values=True,
        include_metadata=True,
        vector=vector,
      )
    
      metadata=response['matches'][0]['metadata']
      matches = response['matches']
      # Initialize an empty array to store metadata values
      metadata_values = []

      for match in matches:
          if match['metadata']:
                  metadata_values.append(match['metadata'])

      messagesAPI=[
          {
            "role": "system", 
            "content": "Actúa como un asistente buscador de comercios. Tu labor será la de asistir al usuario en las dudas que tenga sobre los establecimientos registrados. Se te dará un user prompt y los metadatos de una página de wordpress con la ficha de los establecimientos obtenidos mediante embedding. No saques respuestas de más de 250 tokens. Saca siempre el nombre del establecimiento que a su vez será un enlace a la ficha. Este enlace será la url del establecimiento entre etiquetas <a> html como un link."
          },
          {
            "role": "user",
            "content":str(metadata_values),
          },
      ]
      messagesAPI += messagesCliente
      chat_completion = client.chat.completions.create(
      messages=messagesAPI,
      model="gpt-3.5-turbo",
      temperature=openai_wac_chat_temperature,
      max_tokens=openai_wac_chat_token_limit
      )

      print(chat_completion)
      #return Response({"message":chat_completion.choices[0].message.content,"title":metadata['title'],"url":metadata['url']}, status=status.HTTP_200_OK)
      return Response({"message":chat_completion.choices[0].message.content}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print("An error occurred:", str(e))
        return Response({'status': "error", "error":e}, status=status.HTTP_400_BAD_REQUEST)   


