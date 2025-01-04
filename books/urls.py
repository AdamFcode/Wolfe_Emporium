from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_books, name='books'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('partner/', views.partner_contact, name='partner_contact'),
]