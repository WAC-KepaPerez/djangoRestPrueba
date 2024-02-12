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

# Create your views here.
movies =[
  {
    "id": 1,
    "title": "The Shawshank Redemption",
    "content": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    "url": "https://www.imdb.com/title/tt0111161/"
  },
  {
    "id": 2,
    "title": "The Godfather",
    "content": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
    "url": "https://www.imdb.com/title/tt0068646/"
  },
  {
    "id": 3,
    "title": "The Dark Knight",
    "content": "When the menace known as The Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
    "url": "https://www.imdb.com/title/tt0468569/"
  },
  {
    "id": 4,
    "title": "Pulp Fiction",
    "content": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
    "url": "https://www.imdb.com/title/tt0110912/"
  },
  {
    "id": 5,
    "title": "Inception",
    "content": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
    "url": "https://www.imdb.com/title/tt1375666/"
  }
]

movies2 =[
      {
        "id": 22,
        "title": "Inception",
        "content": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "url": "https://www.imdb.com/title/tt1375666/",
        "uaaa":35
      },
]


@api_view(['GET'])
def pon(request):
         return Response({"pon"})
class MyModelAPIView(APIView):
    def post(self, request):
        pc = Pinecone(api_key=PINECODE_API_KEY)
        index = pc.Index('movies') 
        vectors=[]
        try:
            for movie in movies2:
                movieData=  str(movie)
                response = client.embeddings.create(
                input=movieData,
                model="text-embedding-3-small"
                )
                print(response.data[0].embedding)
                vectors.append(
                    {"id": str(movie['id']), 
                    "values": response.data[0].embedding, 
                    "metadata": movie
                    },
                    )

            response=index.upsert(
                vectors=vectors,
            namespace="ns1"
            )
            print(response)
            return Response({'status': "okey"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("An error occurred:", str(e))
            return Response({'status': "error", "error":e}, status=status.HTTP_400_BAD_REQUEST)   





