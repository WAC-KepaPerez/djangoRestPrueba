from django.urls import path
from . import views

urlpatterns=[
    path('',views.getItems),
    path('<int:item_id>/', views.getItem),
    path('add/',views.addItem),
    path('<int:item_id>/update',views.updateItem),
]