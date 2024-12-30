from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from books.models import Book

# Create your views here.

def view_cart(request):

    return render(request, 'cart/cart.html')

def add_to_cart(request, item_id):

    book = get_object_or_404(Book, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
        messages.success(request, f'Updated {book.name} quantity to {cart[item_id]}')
    else:
        cart[item_id] = quantity
        messages.success(request, f'Successfully added {book.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)

def adjust_cart(request, item_id):

    book = get_object_or_404(Book, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    
    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f'Updated {book.name} quantity to {cart[item_id]}')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))

def remove_from_cart(request, item_id):
    book = get_object_or_404(Book, pk=item_id)
    cart = request.session.get('cart', {})

    try:
        cart.pop(item_id)
        messages.success(request, f'Removed {book.name} from your bag')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)