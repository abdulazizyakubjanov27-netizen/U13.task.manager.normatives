from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import test_api, PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')

urlpatterns = [
    path('task/', test_api),
    path('', include(router.urls)),
    # path('posts/', PostListCreateAPIView.as_view()),
    # path('posts/<int:pk>/', PostDetailAPIView.as_view()),
]