from dataclasses import fields
from rest_framework import serializers

from .models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields = "__all__"
        fields = [
            "book_id", 
            "cover", 
            "isbn", 
            "title", 
            "subtitle", 
            "author", 
            "published", 
            "publisher", 
            "pages", 
            "description", 
            "website"
            ]
