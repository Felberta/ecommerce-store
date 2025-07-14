from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Homepage with categories
def index(request):
    categories = Category.objects.all()
    return render(request, 'store/index.html', {'categories': categories})

# View products in a category
def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category_products.html', {'category': category, 'products': products})

# Product detail page
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

# Register new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Add to cart
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        order_item.quantity += 1
    order_item.save()
    return redirect('cart')

# Remove from cart
@login_required
def remove_from_cart(request, id):
    order = get_object_or_404(Order, user=request.user, complete=False)
    item = get_object_or_404(OrderItem, order=order, product_id=id)
    item.delete()
    return redirect('cart')

# Cart view
@login_required
def cart_view(request):
    try:
        order = Order.objects.get(user=request.user, complete=False)
    except Order.DoesNotExist:
        order = None

    items = []
    total = 0

    if order:
        items = order.orderitem_set.all()
        total = sum([item.product.price * item.quantity for item in items])

    return render(request, 'store/cart.html', {
        'items': items,
        'total': total
    })

# Checkout view
@login_required
def checkout(request):
    try:
        order = Order.objects.get(user=request.user, complete=False)
        items = order.orderitem_set.all()
        total = sum([item.product.price * item.quantity for item in items])

        if request.method == 'POST':
            order.complete = True
            order.save()
            return render(request, 'store/checkout.html', {'placed': True})

        return render(request, 'store/checkout.html', {
            'items': items,
            'total': total,
            'placed': False
        })
    except Order.DoesNotExist:
        return render(request, 'store/checkout.html', {'placed': False})
    
@login_required
def payment(request):
    try:
        order = Order.objects.filter(user=request.user, complete=False).last()
        items = order.orderitem_set.all()
        total = sum([item.product.price * item.quantity for item in items])

        if request.method == 'POST':
            if request.POST.get("confirmed") == "yes":
                # Mark the order complete
                order.complete = True
                order.save()
                return redirect('payment_success')
            else:
                # User clicked "Proceed to OTP", show OTP input
                return render(request, 'store/payment.html', {
                    'order': order,
                    'items': items,
                    'total': total,
                    'show_otp': True
                })

        return render(request, 'store/payment.html', {
            'order': order,
            'items': items,
            'total': total,
            'show_otp': False
        })

    except Order.DoesNotExist:
        return redirect('index')




@login_required
def payment_success(request):
    try:
        order = Order.objects.filter(user=request.user, complete=True).last()
        total = sum([item.product.price * item.quantity for item in order.orderitem_set.all()])
        return render(request, 'store/payment_success.html', {'order': order, 'total': total})
    except Order.DoesNotExist:
        return redirect('index')


@login_required
def update_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__complete=False)
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            item.quantity = quantity
            item.save()
    return redirect('cart')



# About page
def about(request):
    return render(request, 'store/about.html')

# Contact page
def contact(request):
    return render(request, 'store/contact.html')
