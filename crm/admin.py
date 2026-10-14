from django.contrib import admin
from .models import Customer, Order, CustomerActivity, Product



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'phone',
        'email',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'name',
        'phone',
        'email',
    )

    list_editable = (
        'status',
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'title',
        'amount',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'title',
        'customer__name',
    )

    @admin.register(Product)
    class ProductAdmin(admin.ModelAdmin):
        list_display = (
            'id',
            'name',
            'category',
            'price',
            'quantity',
            'status',
            'created_at',
        )

        list_filter = (
            'status',
            'category',
        )

        search_fields = (
            'name',
            'category',
        )

        list_editable = (
            'price',
            'quantity',
            'status',
        )

        ordering = (
            '-created_at',
        )