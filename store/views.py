from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .cart import Cart
from .forms import CheckoutForm, RegisterForm
from .models import Category, Order, OrderItem, Product


def product_list(request):
    products = Product.objects.filter(stock__gt=0)
    category = request.GET.get('category')
    search = request.GET.get('q')

    if category:
        products = products.filter(category__slug=category)
    if search:
        products = products.filter(name__icontains=search)

    return render(request, 'store/product_list.html', {
        'products': products,
        'search_query': search or '',
        'categories': Category.objects.all(),
        'active_category': category or '',
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related,
    })


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if product.stock < 1:
        messages.error(request, f'{product.name} is out of stock.')
        return redirect('store:product_detail', slug=product.slug)

    if quantity > product.stock:
        messages.error(request, f'Only {product.stock} items available.')
        return redirect('store:product_detail', slug=product.slug)

    cart.add(product, quantity=quantity)
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect(request.POST.get('next') or 'store:cart')


def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(product, quantity)
    messages.success(request, 'Cart updated.')
    return redirect('store:cart')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'Removed {product.name} from cart.')
    return redirect('store:cart')


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total=cart.get_total(),
                    shipping_address=form.cleaned_data['shipping_address'],
                    phone=form.cleaned_data['phone'],
                    status='processing',
                )
                for item in cart:
                    product = item['product']
                    if item['quantity'] > product.stock:
                        messages.error(
                            request,
                            f'Not enough stock for {product.name}. Only {product.stock} available.',
                        )
                        order.delete()
                        return redirect('store:cart')

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=item['price'],
                    )
                    product.stock -= item['quantity']
                    product.save()

            cart.clear()
            messages.success(request, f'Order #{order.pk} placed successfully!')
            return redirect('store:order_detail', order_id=order.pk)
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


def register(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome.')
            return redirect('store:product_list')
    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('store:product_list')


class CustomLoginView(LoginView):
    template_name = 'store/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('store:product_list')
