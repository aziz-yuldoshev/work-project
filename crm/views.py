from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum, Avg, Count, F, DecimalField
from django.db.models.functions import Coalesce

from .models import (
    Customer,
    Order,
    CustomerActivity,
    Product
)


# ==========================================
# DASHBOARD
# ==========================================

def dashboard(request):
    # =========================
    # MIJOZLAR STATISTIKASI
    # =========================

    total_customers = Customer.objects.count()

    new_customers = Customer.objects.filter(
        status='new'
    ).count()

    active_customers = Customer.objects.filter(
        status='active'
    ).count()

    inactive_customers = Customer.objects.filter(
        status='inactive'
    ).count()

    # =========================
    # BUYURTMALAR STATISTIKASI
    # =========================

    total_orders = Order.objects.count()

    active_orders = Order.objects.filter(
        status='processing'
    ).count()

    completed_orders = Order.objects.filter(
        status='completed'
    ).count()

    cancelled_orders = Order.objects.filter(
        status='cancelled'
    ).count()

    # =========================
    # JAMI SAVDO
    # =========================

    total_sales = Order.objects.filter(
        status='completed'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # =========================
    # MAHSULOTLAR STATISTIKASI
    # =========================

    total_products = Product.objects.count()

    active_products = Product.objects.filter(
        status='active'
    ).count()

    inactive_products = Product.objects.filter(
        status='inactive'
    ).count()

    low_stock_products = Product.objects.filter(
        status='active',
        quantity__lte=5
    ).count()

    # =========================
    # JAMI MAHSULOT QOLDIG‘I
    # =========================

    total_quantity = Product.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # =========================
    # OMBORDAGI UMUMIY QIYMAT
    # price × quantity
    # =========================

    total_product_value = Product.objects.filter(
        status='active'
    ).aggregate(
        total=Sum(
            F('price') * F('quantity'),
            output_field=DecimalField(
                max_digits=15,
                decimal_places=2
            )
        )
    )['total'] or 0

    # =========================
    # OXIRGI 5 TA BUYURTMA
    # =========================

    recent_orders = Order.objects.select_related(
        'customer'
    ).order_by(
        '-created_at'
    )[:5]

    # =========================
    # CONTEXT
    # =========================

    context = {

        # Mijozlar
        'total_customers': total_customers,
        'new_customers': new_customers,
        'active_customers': active_customers,
        'inactive_customers': inactive_customers,

        # Buyurtmalar
        'total_orders': total_orders,
        'active_orders': active_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,

        # Savdo
        'total_sales': total_sales,

        # Oxirgi buyurtmalar
        'recent_orders': recent_orders,

        # Mahsulotlar
        'total_products': total_products,
        'active_products': active_products,
        'inactive_products': inactive_products,
        'low_stock_products': low_stock_products,
        'total_quantity': total_quantity,
        'total_product_value': total_product_value,
    }

    return render(
        request,
        'crm/dashboard.html',
        context
    )


# ==========================================
# ORDERS
# ==========================================

def orders(request):
    orders = Order.objects.select_related(
        'customer'
    ).order_by(
        '-created_at'
    )

    # =========================
    # SEARCH
    # =========================

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:
        orders = orders.filter(
            title__icontains=search
        ) | orders.filter(
            customer__name__icontains=search
        )

    # =========================
    # STATUS FILTER
    # =========================

    status = request.GET.get(
        'status',
        ''
    )

    if status in [
        'new',
        'processing',
        'completed',
        'cancelled'
    ]:
        orders = orders.filter(
            status=status
        )

    # =========================
    # STATISTICS
    # =========================

    total_orders = Order.objects.count()

    new_orders = Order.objects.filter(
        status='new'
    ).count()

    processing_orders = Order.objects.filter(
        status='processing'
    ).count()

    completed_orders = Order.objects.filter(
        status='completed'
    ).count()

    cancelled_orders = Order.objects.filter(
        status='cancelled'
    ).count()

    # =========================
    # PAGINATION
    # =========================

    paginator = Paginator(
        orders,
        8
    )

    page_number = request.GET.get(
        'page'
    )

    orders_page = paginator.get_page(
        page_number
    )

    context = {

        'orders': orders_page,

        'total_orders': total_orders,

        'new_orders': new_orders,

        'processing_orders': processing_orders,

        'completed_orders': completed_orders,

        'cancelled_orders': cancelled_orders,

        'search': search,

        'selected_status': status,
    }

    return render(
        request,
        'crm/orders.html',
        context
    )


# ==========================================
# CUSTOMERS
# ==========================================

def customers(request):
    customer_list = Customer.objects.all()

    # SEARCH

    search = request.GET.get(
        'search',
        ''
    ).strip()

    # STATUS

    status = request.GET.get(
        'status',
        ''
    )

    if search:
        customer_list = customer_list.filter(
            name__icontains=search
        ) | customer_list.filter(
            phone__icontains=search
        ) | customer_list.filter(
            email__icontains=search
        )

    if status:
        customer_list = customer_list.filter(
            status=status
        )

    context = {

        'customers': customer_list,

        'search': search,

        'selected_status': status,
    }

    return render(
        request,
        'crm/customers.html',
        context
    )


# ==========================================
# CUSTOMER DETAIL
# ==========================================

def customer_detail(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    orders = customer.orders.all().order_by(
        '-created_at'
    )

    # =========================
    # STATISTIKA
    # =========================

    total_orders = orders.count()

    processing_orders = orders.filter(
        status='processing'
    ).count()

    completed_orders = orders.filter(
        status='completed'
    ).count()

    cancelled_orders = orders.filter(
        status='cancelled'
    ).count()

    new_orders = orders.filter(
        status='new'
    ).count()

    # =========================
    # MOLIYAVIY STATISTIKA
    # =========================

    completed_data = orders.filter(
        status='completed'
    )

    total_spent = completed_data.aggregate(
        total=Sum('amount')
    )['total'] or 0

    average_order = completed_data.aggregate(
        average=Avg('amount')
    )['average'] or 0

    # =========================
    # OXIRGI BUYURTMA
    # =========================

    last_order = orders.first()

    # =========================
    # ACTIVITY
    # =========================

    activities = customer.activities.all()[:10]

    context = {

        'customer': customer,

        'orders': orders,

        'activities': activities,

        'total_orders': total_orders,

        'new_orders': new_orders,

        'processing_orders': processing_orders,

        'completed_orders': completed_orders,

        'cancelled_orders': cancelled_orders,

        'total_spent': total_spent,

        'average_order': average_order,

        'last_order': last_order,
    }

    return render(
        request,
        'crm/customer_detail.html',
        context
    )


# ==========================================
# ADD ORDER
# ==========================================

def add_order(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == 'POST':

        title = request.POST.get(
            'title'
        )

        amount = request.POST.get(
            'amount'
        )

        status = request.POST.get(
            'status'
        )

        order = Order.objects.create(

            customer=customer,

            title=title,

            amount=amount,

            status=status,
        )

        CustomerActivity.objects.create(

            customer=customer,

            activity_type='order_created',

            description=(
                f'"{order.title}" nomli '
                f'buyurtma yaratildi'
            )
        )

        if status == 'completed':

            CustomerActivity.objects.create(

                customer=customer,

                activity_type='order_completed',

                description=(
                    f'"{order.title}" '
                    f'buyurtmasi tugallandi'
                )
            )


        elif status == 'cancelled':

            CustomerActivity.objects.create(

                customer=customer,

                activity_type='order_cancelled',

                description=(
                    f'"{order.title}" '
                    f'buyurtmasi bekor qilindi'
                )
            )

        return redirect(
            'customer_detail',
            customer_id=customer.id
        )

    return render(
        request,
        'crm/add_order.html',
        {
            'customer': customer
        }
    )


# ==========================================
# EDIT CUSTOMER
# ==========================================

def edit_customer(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == 'POST':
        customer.name = request.POST.get(
            'name'
        )

        customer.phone = request.POST.get(
            'phone'
        )

        customer.email = request.POST.get(
            'email'
        )

        customer.address = request.POST.get(
            'address'
        )

        customer.status = request.POST.get(
            'status'
        )

        customer.save()

        return redirect(
            'customer_detail',
            customer_id=customer.id
        )

    return render(
        request,
        'crm/edit_customer.html',
        {
            'customer': customer
        }
    )


# ==========================================
# DELETE CUSTOMER
# ==========================================

def delete_customer(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == 'POST':
        customer.delete()

        return redirect(
            'customers'
        )

    return render(
        request,
        'crm/delete_customer.html',
        {
            'customer': customer
        }
    )


# ==========================================
# ADD CUSTOMER
# ==========================================

def add_customer(request):
    if request.method == 'POST':
        name = request.POST.get(
            'name'
        )

        phone = request.POST.get(
            'phone'
        )

        email = request.POST.get(
            'email'
        )

        address = request.POST.get(
            'address'
        )

        status = request.POST.get(
            'status'
        )

        Customer.objects.create(

            name=name,

            phone=phone,

            email=email,

            address=address,

            status=status,
        )

        return redirect(
            'customers'
        )

    return render(
        request,
        'crm/add_customer.html'
    )


# ==========================================
# ORDER DETAIL
# ==========================================

def order_detail(request, order_id):
    order = get_object_or_404(

        Order.objects.select_related(
            'customer'
        ),

        id=order_id
    )

    return render(
        request,
        'crm/order_detail.html',
        {
            'order': order
        }
    )


# ==========================================
# EDIT ORDER
# ==========================================

def edit_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id
    )

    old_status = order.status

    if request.method == 'POST':

        order.title = request.POST.get(
            'title'
        )

        order.amount = request.POST.get(
            'amount'
        )

        order.status = request.POST.get(
            'status'
        )

        order.save()

        # =========================
        # ACTIVITY
        # =========================

        if old_status != order.status:

            if order.status == 'new':

                description = (
                    f'"{order.title}" buyurtmasi '
                    f'"Yangi" statusiga o‘zgartirildi'
                )


            elif order.status == 'processing':

                description = (
                    f'"{order.title}" buyurtmasi '
                    f'"Jarayonda" statusiga o‘zgartirildi'
                )


            elif order.status == 'completed':

                description = (
                    f'"{order.title}" buyurtmasi '
                    f'"Tugallangan" statusiga o‘zgartirildi'
                )


            elif order.status == 'cancelled':

                description = (
                    f'"{order.title}" buyurtmasi '
                    f'"Bekor qilingan" statusiga o‘zgartirildi'
                )


            else:

                description = (
                    f'"{order.title}" buyurtmasi '
                    f'statusi o‘zgartirildi'
                )

            CustomerActivity.objects.create(

                customer=order.customer,

                activity_type='order_created',

                description=description
            )

        return redirect(
            'order_detail',
            order_id=order.id
        )

    return render(
        request,
        'crm/edit_order.html',
        {
            'order': order
        }
    )


# ==========================================
# DELETE ORDER
# ==========================================

def delete_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == 'POST':
        order.delete()

        return redirect(
            'orders'
        )

    return render(
        request,
        'crm/delete_order.html',
        {
            'order': order
        }
    )


# ==========================================
# PRODUCTS
# ==========================================

def products(request):

    products = Product.objects.all().order_by('-created_at')

    # =========================
    # ASOSIY STATISTIKA
    # =========================

    total_products = products.count()

    active_count = products.filter(
        status='active'
    ).count()

    inactive_count = products.filter(
        status='inactive'
    ).count()

    low_stock_count = products.filter(
        quantity__lte=10
    ).count()

    total_quantity = products.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    total_value = products.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0


    # =========================
    # ENG QIMMAT MAHSULOTLAR
    # =========================

    expensive_products = products.order_by(
        '-price'
    )[:5]


    # =========================
    # ENG KO‘P QOLGAN MAHSULOTLAR
    # =========================

    stock_products = products.order_by(
        '-quantity'
    )[:5]


    # =========================
    # KATEGORIYALAR
    # =========================

    categories = (
        products
        .values('category')
        .annotate(
            count=Count('id'),
            quantity=Sum('quantity')
        )
        .order_by('-count')
    )


    context = {

        'products': products,

        'total_products': total_products,

        'active_count': active_count,

        'inactive_count': inactive_count,

        'low_stock_count': low_stock_count,

        'total_quantity': total_quantity,

        'total_value': total_value,

        'expensive_products': expensive_products,

        'stock_products': stock_products,

        'categories': categories,

    }

    return render(
        request,
        'crm/products.html',
        context
    )


# ==========================================
# ADD PRODUCT
# ==========================================

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        status = request.POST.get('status')

        # 📸 Rasm
        image = request.FILES.get('image')

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
            status=status,
            image=image
        )

        return redirect('products')

    return render(request, 'crm/add_product.html')


# ==========================================
# PRODUCT DETAIL
# ==========================================

def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'crm/product_detail.html',
        {
            'product': product
        }
    )


# ==========================================
# EDIT PRODUCT
# ==========================================

def edit_product(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.category = request.POST.get('category')
        product.status = request.POST.get('status')

        # 📸 Agar yangi rasm tanlangan bo‘lsa
        image = request.FILES.get('image')

        if image:
            product.image = image

        product.save()

        return redirect(
            'product_detail',
            product_id=product.id
        )

    return render(
        request,
        'crm/edit_product.html',
        {
            'product': product
        }
    )


# ==========================================
# DELETE PRODUCT
# ==========================================

def delete_product(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':
        product.delete()

        return redirect(
            'products'
        )

    return render(
        request,
        'crm/delete_product.html',
        {
            'product': product
        }
    )
