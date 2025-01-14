from django.db import models
from django.contrib.auth.models import User

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

