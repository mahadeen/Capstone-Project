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

	1.	Custom User Model:
        Initially I created a user model manually, then realized Django’s authentication system must be extended properly. I refactored it to inherit from Class Client(AbstractUser), which stored unhashed passwords at first, then used make_password() to hash them correctly.

	2.	Hiding Unnecessary Fields by Transaction Type:
        Implemented conditional logic to dynamically hide or disable irrelevant fields based on the selected transaction type.

    3.	Database Design (ERD):
        Initially considered a 1:1 relation between Client and Account, but changed it to one-to-many to allow multiple accounts per client. Transactions were stored in a separate table to maintain a complete history and serve as a single source of truth for balance validation.

    4.	Engines / Service Layer:
        Moved business logic from views.py into dedicated service modules to keep the code organized. Implemented this for transactions (transaction_engine), with plans to extend it to accounts.

	5.	Enum-like Behavior for Transaction Types:
        Since native enums conflict with Django migrations, created Python classes that mimic enum behavior. This allows centralized control over transaction type strings without breaking database compatibility.

	6.	Understanding save() vs create():
        Learned that Model.save() writes data to the database, while methods like Model.objects.create() both instantiate and save. This clarified the difference between Python objects in memory and database records.

	7.	Atomic Transactions:
        Implemented @transaction.atomic to ensure that a sequence of related operations either all succeed or all rollback, preserving data integrity during complex transactions.