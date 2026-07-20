from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from django.test.utils import CaptureQueriesContext
from django.db import connection

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            title="Test sarlavhasi",
            content="Test uchun yozilgan content",
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test sarlavhasi")
        self.assertEqual(self.post.author.username, "testuser")

    def test_post_str_method(self):
        self.assertEqual(str(self.post), "Test sarlavhasi")

class PostSerializerTest(TestCase):
    def test_valid_data(self):
        data = {"title": "Yaxshi sarlavha", "content": "Yetarlicha uzun content matnidir"}
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_empty_title(self):
        data = {"title": "", "content": "Yetarlicha uzun content matnidir"}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_short_content(self):
        data = {"title": "Sarlavha", "content": "qisqa"}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class PostPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass12345')
        self.user2 = User.objects.create_user(username='user2', password='pass12345')
        self.post = Post.objects.create(
            title="User1 foydalanuvchi posti",
            content="Bu user1 foydalanuvchi tomonidan yaratilgan post",
            author=self.user1
        )

    def test_owner_can_update(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(f'/task/posts/{self.post.id}/', {
            "title": "Yangilangan sarlavhasi",
            "content": "Yangilangan content matni bu yerda"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_cannot_update(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(f'/task/posts/{self.post.id}/', {
            "title": "Ruxsatsiz yangilash",
            "content": "Bu ishlamasligi lozim edi"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_create(self):
        response = self.client.post('/task/posts/', {
            "title": "Anonim posti",
            "content": "Bu login qilmasdan yaratilmasligi kerak"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class QueryOptimizationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='quser', password='pass12345')
        for i in range(5):
            Post.objects.create(
                title=f"Post {i}",
                content=f"Bu {i}-postning contenti, yetarlicha uzun",
                author=self.user
            )

    def test_query_count_is_optimized(self):
        with CaptureQueriesContext(connection) as ctx:
            posts = Post.objects.select_related('author').all()
            for post in posts:
                _ = post.author.username
        print(f"\nQuery soni (select_related bilan): {len(ctx.captured_queries)}")
        self.assertLessEqual(len(ctx.captured_queries), 2)
