from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Order, OrderItem
from .forms import OrderForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_list', category_id=product.category.id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'product': product})


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    request.session['cart'] = cart
    return redirect('cart')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart and cart[str(product_id)] > 1:
        cart[str(product_id)] -= 1
    elif str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(request.user.orders, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def order_history(request):
    status_filter = request.GET.get('status', None)
    sort_by = request.GET.get('sort', '-created_at') 

    orders = request.user.orders.all()

    if status_filter:
        orders = orders.filter(status=status_filter)

    orders = orders.order_by(sort_by)
    return render(request, 'order_history.html', {'orders': orders})


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    categories = Category.objects.all()  
    products = Product.objects.all() 
    return render(request, 'home.html', {'categories': categories, 'products': products})


def product_list(request, category_id=None):
    if category_id:
        products = Product.objects.filter(category_id=category_id) 
    else:
        products = Product.objects.all() 
    return render(request, 'product_list.html', {'products': products})


def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = [
        {'product': product, 'quantity': cart[str(product.id)], 'total': product.price * cart[str(product.id)]}
        for product in products
    ]
    total_price = sum(item['total'] for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart')


@login_required(login_url='/login/')
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = [
        {'product': product, 'quantity': cart[str(product.id)], 'total': product.price * cart[str(product.id)]}
        for product in products
    ]
    total_price = sum(item['total'] for item in cart_items)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():

            order = Order.objects.create(user=request.user, total_price=total_price)


            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    
                    quantity=item['quantity'],
                    price=item['product'].price
                )


            request.session['cart'] = {}

            return render(request, 'checkout_success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items, 'total_price': total_price})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



@staff_member_required
def manage_orders(request):
    orders = Order.objects.all()

    if request.method == "POST":
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()

    return render(request, 'manage_orders.html', {'orders': orders})

