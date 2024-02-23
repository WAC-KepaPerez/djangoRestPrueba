from django.urls import path
from . import views


urlpatterns=[
    path('pin/', views.pon, name='pon'),
    path('subir-post', views.SubirPost.as_view(), name='subir-post'),
    path('chat', views.Chat.as_view(), name='chat'),
    path('eliminar-embedding',views.BorrarEmbeddings.as_view(),name='eliminar-embedding'),
    path('subir-post-excel',views.SubirPostExcel.as_view(),name='subir-post-excel')
]


