from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
import uuid



class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class BaseModel(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )

    status_flag = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    comments = models.TextField(blank=True, null=True)

    active_from = models.DateTimeField(null=True, blank=True)
    active_to = models.DateTimeField(null=True, blank=True)

    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)

    cuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='created_%(class)s',
        on_delete=models.SET_NULL
    )

    muser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='modified_%(class)s',
        on_delete=models.SET_NULL
    )

    is_deleted = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    class Meta:
        abstract = True



class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_store_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    otp = models.CharField(max_length=6, default='1234')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email or self.mobile_number or "user"


class Store(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    staff = models.ManyToManyField(
        User,
        blank=True,
        related_name="staff_stores"  
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_stores" 
    )
    address = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name or "store"


class Category(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    store = models.ForeignKey(Store, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name or "category"


class Subcategory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name or "subcategory"



class Product(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=50, unique=True)

    name = models.CharField(max_length=255)
    description = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    inventory_count = models.IntegerField(default=0)
    attributes = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name or self.sku


class ProductImage(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)

    order = models.IntegerField(default=0)


class Address(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name or self.city or "address"



class Cart(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"cart-{self.id}"


class CartItem(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(BaseModel):
    STATUS_CHOICES = (
        ('CREATED', 'Created'),
        ('PAID', 'Paid'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    shipping_address = models.ForeignKey(Address, related_name='shipping_orders', on_delete=models.SET_NULL, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_orders', on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')

    def __str__(self):
        return str(self.id)


class OrderDetail(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku = models.CharField(max_length=50)

    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    line_total = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[
        ('INITIATED', 'Initiated'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ])

    paid_at = models.DateTimeField(null=True, blank=True)



class Invoice(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    invoice_number = models.CharField(max_length=100, unique=True)
    issued_at = models.DateTimeField()

    due_at = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.invoice_number or str(self.id)