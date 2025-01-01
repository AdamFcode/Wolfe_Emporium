from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

# Create your views here.
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart appears to be empty.")
        return redirect(reverse('books'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51QcTDNIdri0maLGSveyWElwhjEXH7aiD9IQpmIhrkrbGpHDGAZAnxAbCB3UOEJUOLnLZf8md8zPizExGn3EoILjn00CbJlMuEd',
        'client_secret': 'test cient secret',
    }

    return render(request, template, context)

