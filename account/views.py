from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    if not username or not password or not confirm_password:
        return Response({"error": "Hammasi to'ldirilishi kerak"}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_password:
        return Response({"error": "Parol topilmadi"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username band"}, status=status.HTTP_400_BAD_REQUEST)

    user = User(username=username)
    user.set_password(password)
    user.save()

    return Response({"message": "Ro'yxatdan muvaffaqiyatli o'tildingiz"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response({"error": "Username yoki parol noto'g'ri"}, status=status.HTTP_400_BAD_REQUEST)

    login(request, user)
    return Response({"message": f"Xush kelibsiz, {user.username}!"})

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"message": "Tizimdan chiqib ketdingiz"})