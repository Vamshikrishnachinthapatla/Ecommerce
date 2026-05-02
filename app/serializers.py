from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "otp"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "mobile_number", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

#Store serializer
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
        ]

class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Subcategory
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "category_name",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    subcategory_name = serializers.CharField(source="subcategory.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "description",
            "price",
            "inventory_count",
            "category",
            "category_name",
            "subcategory",
            "subcategory_name",
        ]
        

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=Subcategory.objects.all()
    )

    class Meta:
        model = Product
        fields = [
            "sku",
            "name",
            "price",
            "inventory_count",
            "description",
            "category",
            "subcategory",   # 👈 REQUIRED
        ]

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product_name", "quantity", "price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items"]


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderDetail
        fields = ["product_name", "quantity", "unit_price", "line_total"]


class OrderSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "total_amount", "status", "item_count"]

    def get_item_count(self, obj):
        return obj.items.count()


class CreateOrderSerializer(serializers.Serializer):
    shipping_address_id = serializers.UUIDField()
    billing_address_id = serializers.UUIDField()

    def validate(self, attrs):
        try:
            attrs["shipping_address"] = Address.objects.get(id=attrs["shipping_address_id"])
            attrs["billing_address"] = Address.objects.get(id=attrs["billing_address_id"])
        except Address.DoesNotExist:
            raise serializers.ValidationError("invalid_address")
        return attrs



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(source="order.id", read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            "invoice_number",
            "order_id",
            "amount",
            "taxes",
            "total",
            "issued_at",
        ]

    def get_total(self, obj):
        return obj.amount + obj.taxes
    

class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    product_details = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "product", "product_details"]