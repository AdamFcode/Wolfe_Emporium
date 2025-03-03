from django.db import models
from profiles.models import UserProfile


# Create your models here.
class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Book(models.Model):
    category = models.ForeignKey('Category', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    isbn = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    author = models.CharField(max_length=254, default='Gene Wolfe')
    published = models.CharField(max_length=254)
    description = models.TextField()
    series = models.CharField(max_length=254, null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Partner(models.Model):

    bookstore = models.CharField(max_length=254,)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    county = models.CharField(max_length=80, null=False, blank=False, default='Unknown')

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  
    book = models.ForeignKey('Book', on_delete=models.CASCADE)  
    
    class Meta:
        unique_together = ('user_profile', 'book')  
        
    def __str__(self):
        return f"{self.user_profile.user.username}'s Wishlist: {self.book.name}"

