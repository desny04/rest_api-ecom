from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name=models.charField(max_length=100,unique=True)
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.charField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image1=models.FileField(upload_to='products/',blank=True,null=True)
    image2=models.FileField(upload_to='products/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlist')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='wishlisted')
    added_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','product')

    def __str__(self):
        return f"{self.user.username}-{self.product.name}"
