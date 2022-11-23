from django.urls import path, include
from .views import (
    CartViewset,
    CreatecheckoutSessionView,
    LoginAPI,
    Orderlist,
    PaymentViewset,
    ProductViewset,
    BrandViewset,
    RegisterAPI,
    StripeWebhookAPIView,
    WishlistViewset,
)
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register(r'register', RegisterAPI)
router.register(r'brand', BrandViewset)
router.register(r'product', ProductViewset)
router.register(r'cart', CartViewset)
router.register(r'wishlist', WishlistViewset)
router.register(r'payment', PaymentViewset)

urlpatterns = [

    # login
    path("login/", LoginAPI.as_view(), name="login"),

    # stripe
    path("session", CreatecheckoutSessionView.as_view(),),
    path("webhook", StripeWebhookAPIView.as_view(),),

    path("order",Orderlist.as_view()),
    # router
    path('router/', include(router.urls)),
]
