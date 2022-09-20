from django.db import models

# Create your models here.
class Book(models.Model):
    
    book_id     = models.CharField(max_length=200, unique=True)
    cover       = models.URLField(null=True)
    isbn        = models.CharField(max_length=100)
    title       = models.CharField(max_length=200)
    subtitle    = models.CharField(max_length=200, null=True)
    author      = models.CharField(max_length=100, null=True)
    published   = models.DateField(null=True)
    publisher   = models.CharField(max_length=100, null=True)
    pages       = models.PositiveSmallIntegerField(default=None, null=True)
    description = models.TextField(null=True)
    website     = models.URLField(null=True)

    def __str__(self):
        return self.title
