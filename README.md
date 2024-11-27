# Budget Tracker (Django)

Web site allowing you to conveniently add/save/modify and track your income and expenses. Written with `python3.11`, `Django5.1.3` and uses modern `HTML/CSS/Bootstrap/JS`.

## Main Features:

- Add Expenses / Income functionality (Amount / Description / Category / Income Source / Date)
- Edit / Delete records
- Search by keywords
- Export data to Excel/CSV file
- Sorting records by Amount / Description / Category / Income Source / Date
- Login/Registration/Logout feature (including 'Password reset' feature and 'Email confirmation') with dynamic error handling
- `SMPT` Google-server ('Password reset' by E-mail / Registration confirmation by Email)
- Pagination
- Summary charts (Expenses / Income)
- Change currency type
- Admin panel

### Tech Stack:

- `Python 3.11`
- `Django 5.1.3`
- `PostgreSQL 16`
- `Bootstrap v5.3.3`
- `HTML\CSS\JS`

## Installation:

1) Create a directory and clone the repo in it:
```sh
   git clone https://github.com/ArtemKhov/Budget-Tracker-Django
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
Most configurations are in `budgettracker`->`budgettracker`->`settings.py`.

I set many `settings` configuration with my environment variables (such as: `SECRET_KEY`, `ALLOWED_HOSTS`, `PostgreSQL` and some email configuration parts) and they did **NOT** been submitted to the `GitHub`. You can change these in the code with your own configuration or just add them into your environment variables.

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

Setup `BudgetTracker/budgettracker/budgettracker/settings.py` with PostgreSQL database settings:

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

## Demo
![expenses](https://github.com/user-attachments/assets/9a5626f9-433c-4437-b71a-170b7e0fa968)
![expenses_chart](https://github.com/user-attachments/assets/7759a703-cb3f-4ffc-bb20-91b591f75538)
![login](https://github.com/user-attachments/assets/6304ebcf-b127-41d1-a043-5376c44164b4)
![currency_change](https://github.com/user-attachments/assets/a0ee375f-4a73-4e1f-ba7d-c4875a910593)

## License

Each file included in this repository is licensed under the [MIT License](https://github.com/ArtemKhov/FavouriteBooks/blob/main/LICENSE.txt).
