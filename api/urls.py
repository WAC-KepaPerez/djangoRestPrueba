from django.urls import path
from . import views
from . import notasViews

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns=[
    path('token/', notasViews.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('',views.getItems),
    path('<int:item_id>/', views.getItem),
    path('add/',views.addItem),
    path('<int:item_id>/update/',views.updateItem),
    path('<int:item_id>/delete/',views.deleteItem),
    path('sendNotification', views.send_notification),

    path('notas/',notasViews.getNotas ),
    path('notas/add',notasViews.addNota),
    path('notas/<int:nota_id>',notasViews.notaDetails),
]