from django.conf import settings

def cart_contents(request):

    cart_items = []
    total = 0
    book_count = 0
    
    grand_total = total
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'book_count': book_count,
    }

    return context