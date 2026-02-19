from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from .serializers import *
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import *
from rest_framework.permissions import SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class AuthViewSet(viewsets.ViewSet):
    permission_classes=[AllowAny]
    @action(detail=False,methods=['post'])
    def register(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message':'User Created'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False,methods=['post'])
    def login(self,request):
        username=request.data.get('username')
        password=request.data.get('password')

        user=authenticate(username=username,password=password)
        if user:
            refresh=RefreshToken.for_user(user)
            return Response({
                'access':str(refresh.access_token),
                'refresh':str(refresh),
                'username':user.username
            })
        return Response({'error':'invalid credentials'},status=401)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsStaffOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all().order_by('-created_at')
    serializer_class=ProductSerializer
    permission_classes=[IsStaffOrReadOnly]
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['category']
    def get_permissions(self):
        if self.action=='retrieve':
            return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class=WishlistSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
    