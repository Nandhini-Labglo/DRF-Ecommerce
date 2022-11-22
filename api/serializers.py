from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import (
    Brand, 
    Product,
    Cart,
    Order,
    Wishlistitems,
    Payment
)

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    password = serializers.CharField(
        min_length=8, max_length=32, write_only=True)
    email = serializers.EmailField(max_length=50, allow_blank=False)
    token = serializers.SerializerMethodField('get_user_token')

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "token"]

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def get_user_token(self, obj):
        return Token.objects.get_or_create(user=obj)[0].key
    

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_name','brand_logo',]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','image','price','in_stock','brand']

class CartSerializer(serializers.ModelSerializer):
     class Meta:
        model = Cart
        fields = ['id','product','user','quantity','is_active','price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','status',]

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlistitems
        fields = ['id','user']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id','order','transaction_id','payment_status',]



    


