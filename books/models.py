from django.core.exceptions import ValidationError
from django.db import models
from users.models import User

# constants
DUPLICATE_BOOK_MESSAGE = "Oops! This book has already been suggested. Please try another one."

class Book(models.Model):
    """
    A single instance of a book.
    """
    STATUS_CHOICES = [
            ('SUGGESTED', 'Suggested'),
            ('VOTING', 'In Voting'),
            ('SHORTLISTED', 'Shortlisted'),
            ('SELECTED', 'Selected'),
            ('ARCHIVED', 'Archived'),
            ('VETOED', 'Vetoed')
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    suggested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    suggested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default='SUGGESTED')
    
    def __str__(self):
        return f'{self.title} - {self.author}'

    class Meta:
        constraints = [models.UniqueConstraint(fields=['title', 'author'], name='unique_book', violation_error_message=DUPLICATE_BOOK_MESSAGE)]
        indexes = [models.Index(fields=['title', 'author'])]

    def clean(self):
        cleaned_title: str = self.title.strip().title()
        cleaned_author: str = self.author.strip().title()

        query = models.Q(title__iexact=cleaned_title) & models.Q(author__iexact=cleaned_author)
        
        # if this is an existing object, exclude itself from query
        if self.pk:
            query = query & ~models.Q(pk=self.pk)

        existing_book = Book.objects.filter(query).first()

        if existing_book:
            raise ValidationError(DUPLICATE_BOOK_MESSAGE)

    def save(self, *args, **kwargs):
        self.clean()
        self.title = self.title.strip()
        self.author = self.author.strip()
        super().save(*args, **kwargs)

class Vote(models.Model):
    """
    A decision made by a user about a given Book. The choice field can be one of (YES/NO/VETO).
    Vetoing a book takes it out of the selection list permanently.
    """

    VOTE_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('VETO', 'Veto')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    choice = models.CharField(
            max_length=5,
            choices=VOTE_CHOICES
            )
    voted_at = models.DateTimeField(auto_now_add=True)

class MonthlyPick(models.Model):
    """
    The book chosen in a given month.
    """
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    month = models.DateField()

    class Meta:
        ordering = ['-month']

    def save(self, *args, **kwargs):
        self.month = self.month.replace(day=1)
        super().save(*args, **kwargs)

