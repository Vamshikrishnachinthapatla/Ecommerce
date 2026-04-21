from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminLoginView, CustomerLoginView
from rest_framework_simplejwt.views import TokenRefreshView


from .views import (
    UserViewSet, RegisterView,
    StoreViewSet,
    CategoryViewSet, SubcategoryViewSet,
    ProductViewSet,
    CartView, AddToCartView, RemoveFromCartView,
    OrderViewSet,
    PaymentViewSet, InvoiceViewSet,
    AddressViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('stores', StoreViewSet)
router.register('categories', CategoryViewSet)
router.register('subcategories', SubcategoryViewSet)
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)
router.register('payments', PaymentViewSet)
router.register('invoices', InvoiceViewSet)
router.register('addresses', AddressViewSet)

urlpatterns = [

    path('auth/register/', RegisterView.as_view()),

    path('cart/', CartView.as_view()),
    path('cart/add/', AddToCartView.as_view()),
    path('cart/remove/', RemoveFromCartView.as_view()),

    path('auth/admin/login/', AdminLoginView.as_view()),
    path('auth/customer/login/', CustomerLoginView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('', include(router.urls)),

]