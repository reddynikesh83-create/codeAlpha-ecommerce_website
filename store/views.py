import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Order, OrderItem
from .forms import UserRegisterForm, CheckoutForm


def home(request):
    """Homepage: product listing with search and category filtering."""
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', '').strip()

    products = Product.objects.all()

    if category and category != 'All':
        products = products.filter(category=category)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')

    categories = [cat[0] for cat in Product.CATEGORY_CHOICES]

    context = {
        'products': products,
        'selected_category': category or 'All',
        'query': query,
        'sort': sort,
        'total_products': products.count(),
        'all_categories': categories,
    }
    return render(request, 'store/home.html', context)


def product_detail(request, product_id):
    """Detailed view for an individual product."""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def cart_view(request):
    """Shopping cart view with line items, quantities, and totals."""
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0.00')

    # Reconstruct cart items with live Product instances
    for product_id, item_data in list(cart.items()):
        try:
            product = Product.objects.get(id=int(product_id))
            quantity = int(item_data.get('quantity', 1))
            line_total = product.price * quantity
            subtotal += line_total

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'line_total': line_total,
            })
        except Product.DoesNotExist:
            # Clean orphaned product from cart
            del cart[product_id]
            request.session.modified = True

    # Free shipping on orders over $50, else $5.00 flat shipping
    shipping = Decimal('0.00') if subtotal >= 50 or subtotal == 0 else Decimal('5.00')
    tax = (subtotal * Decimal('0.08')).quantize(Decimal('0.01'))  # 8% estimated tax
    grand_total = subtotal + shipping + tax

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'grand_total': grand_total,
        'is_free_shipping': subtotal >= 50,
        'remaining_for_free_shipping': max(Decimal('0.00'), Decimal('50.00') - subtotal) if subtotal > 0 else Decimal('50.00'),
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    """Add a product to session-based shopping cart."""
    product = get_object_or_404(Product, id=product_id)
    
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect('product_detail', product_id=product.id)

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    cart = request.session.get('cart', {})
    str_id = str(product.id)

    current_qty = cart.get(str_id, {}).get('quantity', 0)
    new_qty = current_qty + quantity

    if new_qty > product.stock:
        new_qty = product.stock
        messages.warning(request, f"Limited to available stock ({product.stock} items).")

    cart[str_id] = {
        'quantity': new_qty,
        'price': str(product.price),
    }

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f"Added {product.name} to your shopping cart!")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'home'
    if 'cart' in request.POST.get('redirect_to', ''):
        return redirect('cart')
    return redirect(next_url)


def update_cart_quantity(request, product_id):
    """Update item quantity directly or via +/- buttons."""
    if request.method == 'POST':
        action = request.POST.get('action')  # 'increase', 'decrease', or 'set'
        cart = request.session.get('cart', {})
        str_id = str(product_id)

        if str_id in cart:
            product = get_object_or_404(Product, id=product_id)
            current_qty = cart[str_id].get('quantity', 1)

            if action == 'increase':
                if current_qty < product.stock:
                    cart[str_id]['quantity'] = current_qty + 1
                    messages.success(request, f"Increased {product.name} quantity.")
                else:
                    messages.warning(request, f"Maximum available stock reached ({product.stock}).")
            elif action == 'decrease':
                if current_qty > 1:
                    cart[str_id]['quantity'] = current_qty - 1
                    messages.info(request, f"Decreased {product.name} quantity.")
                else:
                    del cart[str_id]
                    messages.info(request, f"Removed {product.name} from cart.")
            elif action == 'set':
                new_qty = int(request.POST.get('quantity', 1))
                if new_qty <= 0:
                    del cart[str_id]
                    messages.info(request, f"Removed {product.name} from cart.")
                elif new_qty > product.stock:
                    cart[str_id]['quantity'] = product.stock
                    messages.warning(request, f"Adjusted to maximum available stock ({product.stock}).")
                else:
                    cart[str_id]['quantity'] = new_qty

            request.session['cart'] = cart
            request.session.modified = True

    return redirect('cart')


def remove_from_cart(request, product_id):
    """Remove an item completely from cart."""
    cart = request.session.get('cart', {})
    str_id = str(product_id)

    if str_id in cart:
        del cart[str_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Item removed from cart.")

    return redirect('cart')


def checkout_view(request):
    """Checkout page: handles customer info, validations, and order creation."""
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty. Add products before proceeding to checkout.")
        return redirect('home')

    # Calculate totals
    subtotal = Decimal('0.00')
    cart_items = []
    for product_id, item_data in cart.items():
        try:
            prod = Product.objects.get(id=int(product_id))
            qty = int(item_data['quantity'])
            line_total = prod.price * qty
            subtotal += line_total
            cart_items.append({'product': prod, 'quantity': qty, 'line_total': line_total})
        except Product.DoesNotExist:
            continue

    if not cart_items:
        messages.warning(request, "Cart items are no longer available.")
        return redirect('home')

    shipping = Decimal('0.00') if subtotal >= 50 else Decimal('5.00')
    tax = (subtotal * Decimal('0.08')).quantize(Decimal('0.01'))
    grand_total = subtotal + shipping + tax

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_amount = grand_total
            order.status = 'Pending'
            order.save()

            # Create OrderItems and decrement stock
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    quantity=item['quantity'],
                    price=item['product'].price
                )
                # Deduct stock
                item['product'].stock = max(0, item['product'].stock - item['quantity'])
                item['product'].save()

            # Clear cart session
            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, f"Order #{order.id} placed successfully! Thank you for your purchase.")
            return redirect('order_success', order_id=order.id)
        else:
            messages.error(request, "Please check the form for invalid or missing details.")
    else:
        # Prepopulate for logged-in user if available
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
            }
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)


def order_success(request, order_id):
    """Order confirmation and summary page."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def my_orders(request):
    """View previous orders for the logged-in customer."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration error. Please correct the highlighted errors.")
    else:
        form = UserRegisterForm()

    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next') or 'home'
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('home')
