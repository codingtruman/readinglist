import pytest
from rest_framework.test import APIClient
from readinglist.api.models import *


client = APIClient()


@pytest.mark.django_db
def test_insert(client, books_collect):
    """test when the data source changes, whether they can still be inserted into db"""

    # test whether books_collect from conftest returns a dict
    assert isinstance(books_collect, dict)

    # there are 10 persistent records already in db
    assert Book.objects.count() == 10

    booklist = books_collect["books"]
    for book in booklist:
        Book.objects.create(
            book_id=book.get("id"),
            cover=book.get("cover"),
            isbn=book.get("isbn"),
            title=book.get("title"),
            subtitle=book.get("subtitle"),
            author=book.get("author"),
            published=book.get("published"),
            publisher=book.get("publisher"),
            pages=book.get("pages"),
            description=book.get("description"),
            website=book.get("website"),
        )
    # added 10 new rows, so 20 in total
    assert Book.objects.count() == 20
