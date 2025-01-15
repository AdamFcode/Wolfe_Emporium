from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from books.models import Book


def cart_contents(request):

    cart_items = []
    total = 0
    book_count = 0
    cart = request.session.get('cart', {})

    for item_id, item_data in cart.items():
        if isinstance(item_data, int):
            book = get_object_or_404(Book, pk=item_id)
            total += item_data * book.price
            book_count += item_data
            cart_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'book': book,
            })

    context = {
        'cart_items': cart_items,
        'total': total,
        'book_count': book_count,
    }

    return context
