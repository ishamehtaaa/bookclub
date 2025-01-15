from django.forms import ModelForm 
from books.models import Book

class BookForm(ModelForm):
    """
    A form to encapsulate creation of a single book.
    """
    class Meta:
        model = Book
        fields = ['title', 'author']
