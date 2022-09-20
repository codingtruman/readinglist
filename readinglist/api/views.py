import json
from datetime import datetime
from urllib import response

import requests
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import *
from .serializers import *
from readinglist.config.settings import DATA_URL


def index(request):
    return render(request, "index.html", {})


def collection(DATA_URL):

    """
    To decouple data collection from insertion, in case the data source changes,
    this function will only collect data from the URL provided in settings
    """

    try:
        response = requests.get(DATA_URL)
        json_content = response.json()

    except Exception as e:
        # this exception can later be added to logs like Sentry to analyse
        print(e)
        return HttpResponse("Unable to extract json from this resource.")

    return json_content


def insertion(request, json_content=collection(DATA_URL)):

    """this function is to process the data and insert into the db"""

    # get all the books in a list
    raw_booklist = json_content["books"]
    # create an empty list to store objects
    booklist = []

    for book in raw_booklist:
        # process publishing date
        date_string = book.get("published")[:10]
        date = datetime.strptime(date_string, "%Y-%m-%d")

        # append every Book object
        booklist.append(
            Book(
                book_id=book.get("id"),
                cover=book.get("cover"),
                isbn=book.get("isbn"),
                title=book.get("title"),
                subtitle=book.get("subtitle"),
                author=book.get("author"),
                published=date,
                publisher=book.get("publisher"),
                pages=book.get("pages"),
                description=book.get("description"),
                website=book.get("website"),
            )
        )

    # insert the objects into the db
    try:
        # or you can put the creation in the for loop,
        # to have smaller granularity and prevent every piece of repetitive data
        Book.objects.bulk_create(booklist)

    except IntegrityError:
        return HttpResponse("Please do not insert the same data.")

    return HttpResponse("Successfully inserted json data into the database.")


class Booklist(ListAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ("published", "title")
    search_fields = ("$book_id", "$isbn", "$author")


class Authorlist(ListAPIView):
    def list(self, request):
        # get all the books
        books = Book.objects.all()
        # get all the authors
        authors = books.values_list("author").distinct()
        # serialize the book object
        book_serializer = BookSerializer(books, many=True)
        # try to rebuild the json response
        response = {}

        for person in authors:
            # person is a tuple, so person[0] to get the string
            author_books = books.filter(author=person[0])
            # serialize the books of each author"s
            book_serializer = BookSerializer(author_books, many=True)
            # add the author and his/her books as a key-value pair
            response[person[0]] = [book_serializer.data]

        # return the customized json
        return Response(response)
