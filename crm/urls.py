from django.urls import path
from .views import (
    dashboard,
    orders,
    customers,
    customer_detail,
    add_order,
    edit_customer,
    delete_customer,
    add_customer,
    order_detail,
    edit_order,
    delete_order,
    products,
    add_product,
    product_detail,
    edit_product,
    delete_product,
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('customers/', customers, name='customers'),
    path(
        'customers/<int:customer_id>/',
        customer_detail,
        name='customer_detail'
    ),

    path(
        'customers/<int:customer_id>/edit/',
        edit_customer,
        name='edit_customer'
    ),

    path(
        'customers/<int:customer_id>/delete/',
        delete_customer,
        name='delete_customer'
    ),

    path(
        'customers/add/',
        add_customer,
        name='add_customer'
    ),

    path(
        'customers/<int:customer_id>/orders/add/',
        add_order,
        name='add_order'
    ),

    path(
        'orders/',
        orders,
        name='orders'
    ),

    path(
        'orders/<int:order_id>/',
        order_detail,
        name='order_detail'
    ),

    path(
        'orders/<int:order_id>/edit/',
        edit_order,
        name='edit_order'
    ),

    path(
        'orders/<int:order_id>/delete/',
        delete_order,
        name='delete_order'
    ),

    path('products/', products, name='products'),

    path('products/', products, name='products'),

    path(
        'products/add/',
        add_product,
        name='add_product'
    ),

    path(
        'products/<int:product_id>/',
        product_detail,
        name='product_detail'
    ),

    path(
        'products/<int:product_id>/edit/',
        edit_product,
        name='edit_product'
    ),

    path(
        'products/<int:product_id>/delete/',
        delete_product,
        name='delete_product'
    ),
]
