# Generated by Django 5.1.5 on 2025-01-15 19:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['title', 'author'], name='books_book_title_b7b426_idx'),
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_book', violation_error_message='Oops! This book has already been suggested. Please try another one.'),
        ),
    ]
