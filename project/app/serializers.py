from rest_framework import serializers
from django.contrib.auth.models import User
from .models import*

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username','email','password']

    def create(self,validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    category_id=serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model=Product
        fields=['id','name','description','price','image1','image2','category','category_id','created_at']

class WishlistSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    product_id=serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model=Wishlist
        fields=['id','product','product_id','added_at']