from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book, Category, Partner, Wishlist, UserProfile
from .forms import PartnerForm
from django.db.models.functions import Lower

def all_books(request):

    books = Book.objects.all()
    categories = None
    query = None
    sort = None
    direction = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            books = books.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                books = books.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            books = books.order_by(sortkey)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Your search did not return anything!")
                return redirect(reverse('books'))

            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(published__icontains=query)
            books = books.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'books': books,
        'search_term': query,
        'current_sorting': current_sorting,
        'current_categories': categories,
    }
    return render(request, 'books/books.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    in_wishlist = False

    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        in_wishlist = user_profile.wishlist_set.filter(book=book).exists()

    context = {
        'book': book,
        'in_wishlist': in_wishlist,
    }

    return render(request, 'books/book_detail.html', context)


def partner_contact(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        
        if form.is_valid():
            messages.success(request, 'Your form was successfully submitted!')
            return redirect('books:partner_contact')
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
            print(form.errors)
        
    else:
        form = PartnerForm()

    return render(request, 'books/partner_contact.html', {'form': form})


@login_required
def add_to_wishlist(request, book_id):
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        book = Book.objects.get(id=book_id)
        Wishlist.objects.get_or_create(user_profile=user_profile, book=book)
    except Book.DoesNotExist:
        messages.error(request, "The book was not found.")
        return redirect('books:books')
    return redirect('books:book_detail', book_id=book.id)


@login_required
def remove_from_wishlist(request, book_id):
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        book = Book.objects.get(id=book_id)
        Wishlist.objects.filter(user_profile=user_profile, book=book).delete()
    except Book.DoesNotExist:
        messages.error(request, "The book was not found.")
        return redirect('books:books')
    return redirect('books:view_wishlist')



@login_required
def view_wishlist(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    wishlist_books = Wishlist.objects.filter(user_profile=user_profile)
    return render(request, 'books/wishlist.html', {'wishlist_books': wishlist_books})
