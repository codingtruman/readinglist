import pytest
from rest_framework.test import APIClient


client = APIClient()


@pytest.mark.parametrize(
    "tested, expected",
    [
        ("response.status_code", 200),
        ("len(response.data)", 10),
        ("isinstance(response.data, list)", True),
    ],
)
@pytest.mark.django_db
def test_books(client, tested, expected):
    """test some common characteristics of response for books and ordering APIs"""

    book_urls = [
        "/api/v1/books",
        "/api/v1/books?ordering=published",
        "/api/v1/books?ordering=-published",
        "/api/v1/books?ordering=title",
        "/api/v1/books?ordering=-title",
    ]

    for url in book_urls:
        response = client.get(url)
        assert eval(tested) == expected


@pytest.mark.django_db
def test_book_ordering(client):
    """test some unique attributes of response to check whether they are in correct orders"""

    published_asc_url = "/api/v1/books?ordering=published"
    response = client.get(published_asc_url)

    assert response.data[0]["published"] == "1835-01-01"
    assert response.data[-1]["pages"] == 352

    published_desc_url = "/api/v1/books?ordering=-published"
    response = client.get(published_desc_url)

    assert response.data[1]["publisher"] == "O'Reilly Media"
    assert response.data[-2]["cover"] == "https://picsum.photos/id/1009/640/480"

    title_asc_url = "/api/v1/books?ordering=title"
    response = client.get(title_asc_url)

    assert response.data[0]["isbn"] == "9781449337711"
    assert response.data[-1]["title"] == "You Don't Know JS"

    title_desc_url = "/api/v1/books?ordering=-title"
    response = client.get(title_desc_url)

    assert response.data[1]["book_id"] == "17da4aea-6e54-43a3-aece-11b1362de170"
    assert response.data[-2]["subtitle"] == "A Modern Introduction to Programming"


@pytest.mark.django_db
def test_authors(client):

    authors_url = "/api/v1/authors"
    response = client.get(authors_url)

    assert response.status_code == 200
    assert len(response.data) == 8
    assert isinstance(response.data, dict)
    expected_author_list = [
        "Mr. Jane Doe",
        "Mr. John Doe",
        "Mrs. John Doe",
        "Honoré de Balzac",
        "Prof. John Doe",
        "Prof. Jane Doe",
        "Dr. Jane Doe",
        "Dr. John Doe",
    ]
    # you cannot simply use == to compare two lists with the same length but stored in different memory blocks
    # so, use a list comprehension to find out their difference,
    # if it's an empty list, it means they have the exact same elements
    assert not [
        author for author in response.data.keys() if author not in expected_author_list
    ]
