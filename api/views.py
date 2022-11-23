import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from django.db.models import F, Sum
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    ListAPIView,
)
import stripe
# from .permissions import IsOwnerOrReadOnly, IsOwner
from .serializers import (
    CartSerializer,
    LoginSerializer,
    OrderSerializer,
    PaymentSerializer,
    ProductSerializer,
    BrandSerializer,
    UserSerializer,
    WishlistSerializer,
)
from .models import (
    Brand,
    Product,
    Cart,
    Order,
    Wishlistitems,
    Payment
)

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

User = get_user_model()


class LoginAPI(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        password = request.data["password"]
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=username, password=password)
            print(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


class RegisterAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class BrandViewset(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BrandSerializer


class CartViewset(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,price=serializer.data['product'].price)


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderSerializer


class WishlistViewset(viewsets.ModelViewSet):
    queryset = Wishlistitems.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = WishlistSerializer


class PaymentViewset(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PaymentSerializer


class CreatecheckoutSessionView(APIView):
    def post(self, *args, **kwargs):
        host = self.request.get_host()
        cart = Cart.objects.filter(
            Q(user=1) & Q(is_active=True))
        grand_total = cart.aggregate(grand_total=Sum(
            F('quantity')*F('price') + (F('quantity')*F('price'))))
        user = 1
        order = Order.objects.create(
            user_id=1, status=2, total_order_price=0)
        order.product.add(*cart)
        cart.update(is_active=False)
        print(order.id)
        for item in cart:
            product_name = item.product.title
            product_quantity = item.quantity
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(grand_total['grand_total']),
                        'product_data': {
                            'name': 'mobile',
                        },
                    },
                    'quantity': 1,
                }
            ],
            metadata={
                "order_id": order.id
            },
            mode='payment',
            success_url="http://127.0.0.1:8000/",
            cancel_url="http://127.0.0.1:8000/",
        )
        payment = Payment.objects.create(
            order_id=order.id, transaction_id=checkout_session['id'], payment_status=2)
        payment.save()
        print(checkout_session)
        return redirect(checkout_session.url, code=303)


class StripeWebhookAPIView(APIView):
    def post(self, request, format=None):
        payload = request.body.decode('utf-8')
        event = json.loads(payload)
        print(payload)
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            sessionID = session["id"]
            print(sessionID)
            ID = session["metadata"]["order_id"]
            print(ID)
            Payment.objects.filter(
                transaction_id=sessionID).update(payment_status=1)
            Order.objects.filter(id=ID).update(status=1)
        elif event['type'] == 'charge.failed':
            Payment.objects.filter(
                transaction_id=sessionID).update(payment_status=0)
            Order.objects.filter(transaction_id=sessionID).update(status=0)
        return HttpResponse(True, status=200)
    
