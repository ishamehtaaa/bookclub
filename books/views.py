from django.views.generic import CreateView, TemplateView
from books.forms import BookForm
from books.models import Book

from typing import Any

class IndexView(TemplateView):
    template_name = "books/index.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context

class SuggestBookView(CreateView):
    template_name = "books/suggest_book.html"
    model = Book
    form_class = BookForm
    success_url = "/"
