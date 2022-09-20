import pytest
from rest_framework.test import APIClient


client = APIClient()


@pytest.mark.parametrize("param", [
    "/", 
    "/api/v1/insertion", 
    "/api/v1/books", 
    "/api/v1/authors"
])
@pytest.mark.django_db
def test_render_views(client, param):
    """test url routing to view fucntions"""

    response = client.get(param)
    assert response.status_code == 200
