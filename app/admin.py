from django.contrib import admin
from .models import (
    User, Store, Category, Subcategory,
    Product, ProductImage,
    Cart, CartItem,
    Order, OrderDetail,
    Payment, Invoice, Address
)

admin.site.register(User)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Payment)
admin.site.register(Invoice)
admin.site.register(Address)