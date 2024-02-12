from django.urls import path
from . import views


urlpatterns=[
    path('pin/', views.pon, name='pon'),

]


