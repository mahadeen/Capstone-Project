Description:

    Amber Bank is a web-based banking system designed to simulate core financial operations, including account creation, deposits, withdrawals, and transaction history tracking. The application provides users with a clean and intuitive interface for managing accounts, functioning as a lightweight online banking platform.

    This project was developed as part of the General Assembly Software Engineering Career Bridging Program capstone project, demonstrating full-stack web development proficiency through the use of Django, Python, HTML, CSS, and JavaScript. The system incorporates relational database design, authentication, and CRUD operations aligned with industry best practices.


Tech Stack:

	Backend: Django 4.2.25 (Python 3.9.6)
	Database: PostgreSQL (via psycopg2-binary adapter)
	Frontend: HTML5, CSS3
	Version Control: Git and GitHub


Installation Guide:

    Follow these steps to set up and run Amber Bank (Capstone-Project) locally.

    1. Clone the repository

    git clone https://github.com/mahadeen/Capstone-Project.git
    cd Capstone-Project

    2. Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate      (Mac/Linux)
    venv\Scripts\activate       (Windows)

    3. Install project dependencies

    pip install -r requirements.txt

    4. Configure the database

    Ensure PostgreSQL is installed and running. You can create the database manually if it does not exist:

    psql -U postgres
    CREATE DATABASE "capstone-project";
    \q

    Database name: capstone-project
    Username: postgres
    Password: 0000 (as set in settings.py)

    Note: These credentials must match your settings.py file:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'capstone-project',
            'USER': 'postgres',
            'PASSWORD': '0000',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

    5. Apply migrations

    python manage.py makemigrations
    python manage.py migrate
    (You can run seeds to fill some dummy data using this command: python manage.py seed)
    6. Create a superuser (admin account)

    Since auth.User is swapped with main_app.Client, create a superuser for admin access:

    python manage.py createsuperuser --username admin --email admin@example.com

    7. Run the development server

    python manage.py runserver

    Open your browser and navigate to:

    http://127.0.0.1:8000/

    You should see the homepage of your web app.

    Django admin panel is accessible at:
    http://127.0.0.1:8000/admin/

    Notes
    Make sure PostgreSQL is running before running migrations or the server.
    Any changes to the database models require makemigrations and migrate commands.
    If you encounter errors with main_app.Client superuser creation, ensure your custom user model is properly configured in settings.py under:

    AUTH_USER_MODEL = 'main_app.Client'


Feature Documentation:

    Sign Up: Users can create a new account with personal details.
    Sign In / Log Out: Secure authentication system to access or leave the account.
    Deposit: Add money to an account.
    Withdraw: Remove money from an account with balance validation.
    Transfer (Self): Move money between the user’s own accounts.
    Transfer (Others): Send money to other clients’ accounts securely.
    Transaction History: Display all deposits, withdrawals, and transfers in a chronological list.

Challenges encountered and solutions applied:

    1- user: 
        I created a user myself, then found out that I had to use Django auth, then I had it inherit class Client(AbstractUser)
        which has an unhashed password and then I used makepassword() to hash it so that Django would accept it.

    2- hiding invalid fields when selecting transaction type:

    3- ERD: thought about having 1:1 for accounts and clients but what if a client has more than one account? Also, transactions were saved in their own table to keep history, so that I could have a validtion method of balances for any account by summing up all the transactions, to have one source of truth.

    4- Using engines/services: Instead of having all of the busniess logic happening in views.py floating around, I can just change them in one place and the changes would take effect whereever they're referenced. Planning on doing that for accounts in the future as I've only done it for transactions for now (using transaction_engine).

    5- utilizing enum-like behaviour: enums are hard to work with Django migration databases, so instead of having the transaction types as plain strings, I created classes that behave like enums would, so that for example I could change "Deposit" to "deposit" in one place and not have to change it anywhere else.

    E.g.
    
    class TransactionTypes:
        DEPOSIT = "Deposit"
        WITHDRAWAL = "Withdrawal"
        TRANSFER = "Transfer"

    6- Save() vs create(): Managed to understand the difference between normal python objects in memory and the data in the database, and that using Django, model.objects."something()", this allows me to deal with the database or create soomething in the database. Also, Model.save() is what actually writes in the database

    7- Atomic transactions: This means that if one of a sequence of steps fails, the rest of the steps will rollback, and can do this using the @atomic decorator.