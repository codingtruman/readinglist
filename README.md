# Reading List API

A project of Django REST framework. 


---
## Features

- [x] Index page lists all the URLs redirecting to necessary APIs for checking, or you can check it mannually by Postman.

- [x] `/api/v1/insertion` performs an action to collect data from [the source](https://hokodo-frontend-interview.netlify.app/data.json) and insert into db
- [x] `/api/v1/books` returns a collection of books
- [x] `/api/v1/books?ordering=published` returns data sorted by publication date, ascending
- [x] `/api/v1/books?ordering=-published` returns data sorted by publication date, descending
- [x] `/api/v1/books?ordering=title` returns data sorted alphabetically by title, ascending
- [x] `/api/v1/books?ordering=-title` returns data sorted alphabetically by title, descending
- [x] `/api/v1/books?search={keyword}` returns data that partially or completely match the keyword in book id, isbn, and author columns.
- [x] `/api/v1/authors` returns a collection of authors, each author item contains a collection of their books

---

## Instructions to run this project locally

1. ```shell
   $ git clone https://github.com/codingtruman/DRF_project.git
   $ cd DRF_project
   $ virtualenv venv --python=python3.8
   $ source venv/bin/activate
   $ pip install -r requirements.txt
   ```
   
2. Change DATABASES setting to your local db setting.

3. ```shell
   $ python manage.py migrate
   $ python manage.py runserver
   ```

4. Open the url http://127.0.0.1:8000/ you will have an index page. Check the APIs by clicking the redirecting urls or doing it mannually by Postman.

5. If pytest raises `DJANGO_SETTINGS_MODULE not defined` error , simply `export DJANGO_SETTINGS_MODULE=readinglist.config.settings`

---

## Workflow

> ### Build

1. Make a repo dir, create virtual env under this repo dir, activate the virtualenv and install django and djangorestframework packages. Then, create a project.
```shell
$ mkdir DRF_project && cd DRF_project
$ virtualenv venv --python=python3.8
$ source venv/bin/activate
$ git init
$ pip install django djangorestframework
$ django-admin startproject readinglist
```
2. We need requests package to read from data source, psycopg2 package because Django only supports PostgreSQL for advanced queries like distinct(), which is used to `SELECT DISTINCT authors`.
```shell
$ pip install requests psycopg2
```
3. Change `DATABASES`, and register `"readinglist"`, `"rest_framework"` in INSTALLED_APPS in `settings.py`

4. ```shell
   $ python manage.py createsuperuser
   ```
   But it prompts an error `database connection isn't set to UTC`, because if you are using Django 2.2, you must use psycopg < 2.9. I failed to degrade psycopg2 to 2.8, so the solution is to remove `USE_TZ=TRUE` in settings. After solving this, we finish creating the superuser.

5. ```shell
   $ python manage.py makemigrations readinglist
   $ python manage.py migrate readinglist
   $ python manage.py runserver
   ```
   Migrate data and check the index and admin page.
   
6. Observe [the json data source](https://hokodo-frontend-interview.netlify.app/data.json), and prepare a table to store the data:

  - In `models.py`, create a Book class and write the data constraint.
  - Then, register the Book model in `admin.py`, so we can check it from admin panel.
  - makemigrations and migrate

7. Write scripts to retrieve the data:

- Set the data source url in settings as `DATA_URL`
- Write collection and insertion functions in `views.py`
     (need to clean the raw data to fit the models constraint, and insert them into db with a loop)
- makemigrations and migrate

8. Design the urls for API and set the routing in `config/urls.py` and `app/urls.py`

9. 
- Create an html page to navigate API routing under `templates/` dir. 
- Set the templates `DIRS` in `settings.py`
- Set the url routing for `index.html` in `urls.py`
- Write a function in `views.py` to render the index page

10. For `/books` endpoint:

   - Create a Booklist class in `views.py` inherited from `ListAPIView` of rest_framework to return a collection of books.
   - Set the `filter_backends` and `ordering_fields`, as well as `search_fields`, so the collection can be ordered by publication date and title. The `search_fields` defines a fuzzy keyword (not strict) match and the parameters that can be searched from.
   - Create `serializers.py` to customize the return fields of Booklist class.
   - Set the routing in `urls.py` for `books/` enpoint and ordering child endpoints.

11. For `/authors` endpoint:

   - Write an Authorlist class in `views.py` inherited from `ListAPIView` of rest_framework to return a collection of authors, followed by their books.
   - Construct the data structures in the response.
   - Set the url routing for `authors/` endpoint.

> ### Test

1. ```shell
   $ pip install pytest pytest-django
   ```

2. Under the project dir, create `pytest.ini` and write initial settings for pytest. Then create a dir named `tests/` and create `__init__.py` under the dir to make it a python package.

2. __The methodology of testing is to Arrange, Act and Assert.__ 

   The main parts we are going to test are the URL routing, views, and models. Put the decorator `@pytest.mark.django_db` on top of each test function, since they all need to access django database. Also, we need a dummy client to simulate web requests. Thus, we need to `from rest_framework import APIClient` in each test.
   
3. For urls, put all urls in the decorator `@pytest.mark.parametrize()`, and make a get request to check whether the status code of response is 200.

4. For models, we need fake some data and see if we can insert them into db. I saved the json data from original source in `test_collect.json` and changed some author names and book_id (with unique key, they have to be changed). 

   ___Note here, since the requirement says the data might change in the future. This method is also able to test if it goes well when the data is retrieved from a local file,  instead of from an online source.___ 

   We assert the number of records equals 10, since there are 10 persistent records in db already. After data collection and insertion, we assert the number to be 20.

5. For views, the main idea is to make requests to different endpoints and resources, and assert the response data equals to our expected data. Since there will be many similar actions, we can take them as parameters in `@pytest.mark.parametrize()` decorator, and then use `eval()` function in a loop for different URLs to compare the tested results and expected results. This complies to  __DRY (Don't Repeat Yourself) principle__.

> ### Prepare for production

- [ ] Install dependecies for deployment and update `requirements.txt`
```shell
$ pip install dj-database-url whitenoise boto3 botocore s3transfer
$ pip freeze > requirements.txt
```

- [ ] Append private or useless file or dir names in `.gitignore`

- [ ] Hide `SECRET_KEY` in `.env` file like: `SECRET_KEY=igz(8scgn%y3+ltzfq=mequ_en3nyvo1i$b8b2s(5^goxe4($h`

   Also put AWS setting variables in `.env` file like the above.

- [ ] Hide database info:
```shell
export DATABASE_URL=postgres://username:password@example.com:5432/my_db
```

- [ ] Install SSL certificate on this project

- [ ] In `settings.py`, set: 

```python
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
PRODUCTION = os.environ.get("YESNO_PRODUCTION", "false").lower() in {"true", "yes", "y"}
if PRODUCTION is True:
    DEBUG = False
else:
    DEBUG = True
ALLOWED_HOSTS = ["example.com"]

# DATABASES settings
DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

# HTTPS settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Authentication settings
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

MIDDLEWARE = [
    # append this line in MIDDLEWARE
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# AWS settings
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
S3_BUCKET = os.environ.get("S3_BUCKET")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
# if a user upload a file with the same name as another in s3, rename it automatically
AWS_S3_FILE_OVERWRITE = False
# some issue with the default value, so reset it to None
AWS_DEFAULT_ACL = None
# set the storage backend
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
```

- [ ] Finally, ask Django to check it out for deployment: 

```shell
$ python manage.py check --deploy
```
