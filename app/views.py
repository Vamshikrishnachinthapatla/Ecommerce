from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from .serializers import *



class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsStoreStaffOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.is_admin or user.is_store_owner or user.is_store_staff



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "user_created",
            "data": UserSerializer(user).data
        })



class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.filter(is_deleted=False)
    serializer_class = StoreSerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.filter(is_deleted=False)
    serializer_class = SubcategorySerializer
    permission_classes = [IsAdminOrReadOnly]



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False)
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]

    permission_classes = [IsStoreStaffOrAdmin]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductCreateUpdateSerializer
        return ProductSerializer



class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.filter(is_deleted=False)
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)


class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            product = get_object_or_404(Product, id=request.data.get("product_id"))
            qty = int(request.data.get("quantity", 1))

            cart, _ = Cart.objects.get_or_create(user=request.user)
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            item.quantity = qty if created else item.quantity + qty
            item.save()

            return Response({
                "message": "added_to_cart",
                "product": product.name,
                "quantity": item.quantity
            })

        except Exception:
            raise ValidationError("invalid_cart_request")


class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        item = get_object_or_404(
            CartItem,
            id=request.data.get("item_id"),
            cart__user=request.user
        )
        item.delete()
        return Response({"message": "removed_from_cart"})



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.all() if user.is_admin else Order.objects.filter(user=user)

    def get_serializer_class(self):
        return CreateOrderSerializer if self.action == "create" else OrderSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data

        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.items.exists():
            raise ValidationError("cart_empty")

        store = cart.items.first().product.store

        order = Order.objects.create(
            user=user,
            store=store,
            shipping_address=data["shipping_address"],
            billing_address=data["billing_address"],
            total_amount=0,
            status="CREATED"
        )

        total = 0

        for item in cart.items.select_related("product"):
            product = item.product

            if product.inventory_count < item.quantity:
                raise ValidationError(f"out_of_stock:{product.name}")

            line_total = product.price * item.quantity
            total += line_total

            OrderDetail.objects.create(
                order=order,
                product=product,
                sku=product.sku,
                quantity=item.quantity,
                unit_price=product.price,
                line_total=line_total
            )

            product.inventory_count -= item.quantity
            product.save(update_fields=["inventory_count"])

        order.total_amount = total
        order.save(update_fields=["total_amount"])

        cart.items.all().delete()

        return Response({
            "message": "order_created",
            "order_id": order.id,
            "total": total
        })



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(is_deleted=False)
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.filter(is_deleted=False)
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


# ---------------- AUTH ----------------

class AdminLoginView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data.get("email")).first()

        if user and user.check_password(request.data.get("password")):
            token = RefreshToken.for_user(user)
            return Response({
                "access": str(token.access_token),
                "refresh": str(token),
                "role": "admin"
            })

        return Response({"error": "invalid_credentials"}, status=401)


class CustomerLoginView(APIView):
    def post(self, request):
        user = User.objects.filter(mobile_number=request.data.get("mobile_number")).first()

        if user and user.otp == request.data.get("otp"):
            token = RefreshToken.for_user(user)
            return Response({
                "access": str(token.access_token),
                "refresh": str(token),
                "role": "customer"
            })

        return Response({"error": "invalid_otp"}, status=400)