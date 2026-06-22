from .cart import Cart
from .shop_config import FREE_DELIVERY_MIN, SHOP_NAME, SHOP_TAGLINE


def cart(request):
    return {
        'cart': Cart(request),
        'shop_name': SHOP_NAME,
        'shop_tagline': SHOP_TAGLINE,
        'free_delivery_min': FREE_DELIVERY_MIN,
    }
