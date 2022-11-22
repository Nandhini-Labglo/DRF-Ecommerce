from django.urls import path, include
from .views import (
    CartViewset,
    CreatecheckoutSessionView,
    LoginAPI,
    OrderViewset,
    PaymentViewset,
    ProductViewset, 
    BrandViewset,
    RegisterAPI,
    StripeWebhookAPIView,
    WishlistViewset,
    test_payment,
)
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register(r'register', RegisterAPI)
router.register(r'brand', BrandViewset)
router.register(r'product', ProductViewset)
router.register(r'cart', CartViewset)
router.register(r'order', OrderViewset)
router.register(r'wishlist', WishlistViewset)
router.register(r'payment', PaymentViewset)

urlpatterns = [

    #login
    path("login/", LoginAPI.as_view(), name="login"),

    path("session",CreatecheckoutSessionView.as_view(),),
    path("webhook",StripeWebhookAPIView.as_view(),),
    path("pay",test_payment,),
    
    #router
    path('router/', include(router.urls)),
]