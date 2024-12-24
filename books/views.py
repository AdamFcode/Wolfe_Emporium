from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Book

# Create your views here.

def all_books(request):

    books = Book.objects.all()
    query = None
    sort = None
    direction = None

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                books = books.annotate(lower_name=Lower('name'))

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
    }
    return render(request, 'books/books.html', context)

def book_detail(request, book_id):

    book = get_object_or_404(Book, pk=book_id)

    context = {
        'book': book,
    }

    return render(request, 'books/book_detail.html', context)