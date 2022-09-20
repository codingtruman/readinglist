import os
import json
import pytest


@pytest.fixture
def books_collect():

    # use local json data to test
    data_source = os.path.join(os.getcwd(), "readinglist/tests/test_collect.json")
    # get json content
    print(data_source)
    with open(data_source, "r") as file:
        return json.load(file)
