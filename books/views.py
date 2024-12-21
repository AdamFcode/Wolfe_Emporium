from django.shortcuts import render, get_object_or_404
from .models import Book

# Create your views here.

def all_books(request):

    books = Book.objects.all()

    context = {
        'books': books,
    }

    return render(request, 'books/books.html', context)

def book_detail(request, book_id):

    book = get_object_or_404(Book, pk=book_id)

    context = {
        'book': book,
    }

    return render(request, 'books/book_detail.html', context)