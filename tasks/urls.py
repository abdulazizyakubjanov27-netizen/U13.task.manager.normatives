from django.urls import path
from .views import test_api, PostListCreateAPIView, PostDetailAPIView

urlpatterns = [
    path('task/', test_api),
    path('posts/', PostListCreateAPIView.as_view()),
    path('posts/<int:pk>/', PostDetailAPIView.as_view()),
]