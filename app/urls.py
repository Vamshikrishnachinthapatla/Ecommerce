from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('stores', StoreViewSet)
router.register('categories', CategoryViewSet)
router.register('subcategories', SubcategoryViewSet)
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [

    # AUTH
    path('auth/send-otp/', SendOTPView.as_view()),
    path('auth/verify-otp/', VerifyOTPView.as_view()),

    # CART
    path('cart/', CartView.as_view()),
    path('cart/add/', AddToCartView.as_view()),

    # PAYMENT
    path('payments/create/', CreatePaymentView.as_view()),
    path('payments/verify/', FakePaymentVerifyView.as_view()),

    path('', include(router.urls)),
]