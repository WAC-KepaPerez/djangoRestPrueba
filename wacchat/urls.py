from django.urls import path
from . import views


urlpatterns=[
    path('pin/', views.pon, name='pon'),
    path('subir-post', views.SubirPost.as_view(), name='subir-post'),
]


