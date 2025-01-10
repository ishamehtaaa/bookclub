from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ContentWarning(models.Model):
    """
    Represents a content warning in a book. Used to provide information about if the book is suitable.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Represents a single book. Books can be voted on in multiple rounds.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content_warnings = models.ManyToManyField(ContentWarning, blank=True)
    date_suggested = models.DateTimeField(default=timezone.now)
    suggested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available for Voting'),
        ('VETOED', 'Vetoed'),
        ('SELECTED', 'Selected'),
        ('COMPLETED', 'Completed')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')

    def __str__(self):
        return f"{self.title} by {self.author}"

class VotingRound(models.Model):
    """
    A single voting round. Users will participate in a voting round and can cast a Vote (see below). 
    There will usually be multiple voting rounds in a given month.
    """
    month = models.DateField(unique=True)
    books = models.ManyToManyField(
        Book,
        related_name='voting_rounds',
        limit_choices_to={'status': 'AVAILABLE'}
    )
    selected_book = models.ForeignKey(
        Book, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='selected_for'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Voting for {self.month.strftime('%B %Y')}"

class Vote(models.Model):
    """
    A user's vote. They can vote YES/NO/VETO. If a book is vetoed, then it will never appear again in any voting rounds.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voting_round = models.ForeignKey(VotingRound, on_delete=models.CASCADE)
    
    VOTE_CHOICES = [
        ('YES', 'Want to Read'),
        ('NO', 'Not Interested'),
        ('VETO', 'Veto')
    ]
    vote = models.CharField(max_length=4, choices=VOTE_CHOICES)
    date_voted = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['book', 'user', 'voting_round']

    def save(self, *args, **kwargs):
        if self.vote == 'VETO':
            self.book.status = 'VETOED'
            self.book.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s vote on {self.book.title}"
