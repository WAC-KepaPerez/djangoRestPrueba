from django.urls import path
from . import views
from . import notasViews
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns=[
    path('pin/', views.pon, name='pon'),
    path('token/', notasViews.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),

    path('',views.getItems),
    path('<int:item_id>/', views.getItem),
    path('add/',views.addItem),
    path('<int:item_id>/update/',views.updateItem),
    path('<int:item_id>/delete/',views.deleteItem),
    path('sendNotification', views.send_notification),

    path('notas/',notasViews.getNotas ),
    path('notas/add',notasViews.addNota),
    path('notas/<int:nota_id>',notasViews.notaDetails),

    #path('posts/create/', views.MyModelAPIView.as_view(), name='post-create'),
    path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/', views.PostListView, name='post-list'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


