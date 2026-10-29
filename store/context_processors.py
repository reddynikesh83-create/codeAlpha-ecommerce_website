from .models import Product


def cart_context(request):
    """
    Context processor to provide cart item count and active categories to all templates.
    """
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 0) for item in cart.values()) if isinstance(cart, dict) else 0

    categories = [cat[0] for cat in Product.CATEGORY_CHOICES]

    return {
        'cart_count': cart_count,
        'global_categories': categories,
    }
