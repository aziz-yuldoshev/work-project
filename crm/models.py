from django.db import models


# ==========================================
# CUSTOMER
# ==========================================

class Customer(models.Model):

    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('active', 'Faol'),
        ('inactive', 'Faol emas'),
    ]

    name = models.CharField(
        max_length=150,
        verbose_name='Ism'
    )

    phone = models.CharField(
        max_length=20,
        verbose_name='Telefon'
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email'
    )

    address = models.TextField(
        blank=True,
        verbose_name='Manzil'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Status'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Qo‘shilgan sana'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yangilangan sana'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Mijoz'
        verbose_name_plural = 'Mijozlar'
        ordering = ['-created_at']


# ==========================================
# ORDER
# ==========================================

class Order(models.Model):

    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('processing', 'Jarayonda'),
        ('completed', 'Tugallangan'),
        ('cancelled', 'Bekor qilingan'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Buyurtma nomi'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Summa'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# ==========================================
# CUSTOMER ACTIVITY
# ==========================================

class CustomerActivity(models.Model):

    ACTIVITY_TYPES = [
        ('customer_created', 'Mijoz qo‘shildi'),
        ('order_created', 'Buyurtma yaratildi'),
        ('order_completed', 'Buyurtma tugallandi'),
        ('order_cancelled', 'Buyurtma bekor qilindi'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_TYPES
    )

    description = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.description


# ==========================================
# PRODUCT
# ==========================================

class Product(models.Model):

    STATUS_CHOICES = [
        ('active', 'Mavjud'),
        ('inactive', 'Nofaol'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Mahsulot nomi'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Tavsif'
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Narx'
    )

    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Qoldiq'
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Kategoriya'
    )

    # ==========================================
    # PRODUCT IMAGE
    # ==========================================

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Rasm'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Status'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Qo‘shilgan sana'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yangilangan sana'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'
        ordering = ['-created_at']