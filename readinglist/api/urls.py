from django.urls import path

from .views import *

APP_NAME = "api"

urlpatterns = [
    path("", index, name="index"),
    path("api/v1/insertion", insertion, name="insertion"),
    path("api/v1/books", Booklist.as_view(), name="books"),
    path("api/v1/authors", Authorlist.as_view(), name="authors"),
]
