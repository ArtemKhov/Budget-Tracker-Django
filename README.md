# Django Favourite Books site 

A website that allows you to save your favorite books and leave a small review of them. Written with `python3.11`, `Django5.1.1` and uses modern `HTML/CSS/JS`.

## Main Features:

- Add books functionality (Title / Description / Publishing state / Select Genres / Select book Image)
- Edit / Delete books
- Comment feature (including likes on comments / ability to delete comments)
- Filtering books by Genres (tags) (different filtering on the page with user's books and on the page with all books)
- Login/Registration feature (including 'Password reset' feature)
- OAuth Login via `Google / GitHub`
- Profile (including 'Change password' feature)
- `SMPT` Google-server (ability to receive feedback by E-mail / 'Password reset' by E-mail)
- Captcha
- Pagination (Books page / Comments section)
- Access to certain pages and actions only for authorized users or authors of the article.
- Admin panel with additional functionality

### Tech Stack:

**Main:**

- `Python 3.11`
- `Django 5.1.1`
- `PostgreSQL 16`

**Additional:**
- `django-debug-toolbar` - for more thorough debugging.
- `ipython` - provides an improved interactive shell for Python that makes working with code much easier, combined with Django Shell Plus from Django Extensions, IPython provides autocomplete commands and saves command history for more productive work.
- `django-extensions` - provides a set of useful commands and utilities that greatly extend the capabilities of the standard Django command set.
- `django-unique-slugify` - the package automatically generates unique slugs for models.
- `psycopg` and `psycopg-binary` - for correct working and connect PostgreSQL and Django
- `django-simple-captcha` - for captcha

**A few words about `HTML/CSS/JS`:**
- A [free template](https://html5up.net/massively) was used, which was adapted and modified for the specifics of a site about favorite books.
- [License](https://html5up.net/license) - the Creative Commons Attribution 3.0 License




## Installation:

1) Create a directory and clone the repo in it:
```sh
   git clone https://github.com/ArtemKhov/FavouriteBooks
   ```
2) Create your virtual environment:
```
python -m venv venv
```
3) Activate your virtual environment:
```
env\Scripts\activate
```
4) Install the requirements.txt:
```
pip install -r requirements.txt
```

### Configuration
Most configurations are in `favouritebooks`->`favouritebooks`->`settings.py`.

I set many `settings` configuration with my environment variables (such as: `SECRET_KEY`, `ALLOWED_HOSTS`, `DEBUG`, `OAUTH`, `PostgreSQL` and some email configuration parts) and they did **NOT** been submitted to the `GitHub`. You can change these in the code with your own configuration or just add them into your environment variables.

## Run

### Create `PostgreSQL` database:
- Install [PostgreSQL 16](https://www.postgresql.org/) according to your operating system
- Launch **_pgAdmin_**
- In the **_Login/Group Roles_** tab, create a new administrator user:
  - in the General tab, come up with a user name;
  - in the Definition tab, a new password that will relate specifically to this user;
  - in the Privileges tab, set all permissions for the user;
- In the **_Databases_** tab, create a new database
  -  in General tab, type the name of the database and select the user you just created above. 

### Modify `settings.py`:

Setup `favourite_books_site/favouritebooks/favouritebooks/settings.py` with PostgreSQL database settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Your DB NAME using in PostgreSQL',
        'USER': 'Your USER NAME using in PostgreSQL',
        'PASSWORD': 'Your PASSWORD using in PostgreSQL',
        'HOST': os.getenv('HOST_PG') or 'localhost',
        'PORT': os.getenv('PORT_PG') or 5432,
    }
}
```

Run the following commands in Terminal:
```bash
python manage.py makemigrations
python manage.py migrate
```  

### Create super user

Run command in terminal:
```bash
python manage.py createsuperuser
```

### Collect static files
Run command in terminal:
```bash
python manage.py collectstatic --noinput
python manage.py compress --force
```

### Getting start to run server
Execute: `python manage.py runserver`

Open up a browser and visit: http://127.0.0.1:8000/ , the you will see the site.

Further you can fill the site with data at your discretion to understand how everything looks like (admin panel can also help) or you can see the approximate filling of the site in the folder Demo.

## License

Each file included in this repository is licensed under the [MIT License](https://github.com/ArtemKhov/FavouriteBooks/blob/main/LICENSE.txt).
