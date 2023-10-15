# Carly Customer Interface

### Overview
This API provides an interface for customer data. Customers can be
created, updated, viewed, and deleted. Users can also sign up for the 
first time with their email and a password, log in, and reset their password.

### Documentation
Full API documentation can be found at `http://127.0.0.1:8000/api/ui/`

How to start the app locally (with the required libraries):
```python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Routes:
Home :  `http://127.0.0.1:8000/`

API documentation: `http://127.0.0.1:8000/api/ui/#/`

Customers routes: `http://127.0.0.1:8000/customers`

Single Customer routes: `http://127.0.0.1:8000/customers/{email}`

Authentication routes: `http://127.0.0.1:8000/auth/{login/signup/reset}`


### Choices
#### Framework
I am using Flask for this project because it provides a very lightweight
structure for an API microservice. 

If the API was going to be expanded
or the project was going to contain other resources such as a frontend, Django/Django Rest Framework
would probably be a more robust choice.

#### API
For the API I am using the library Connexion, which allows you create 
documentation with Swagger at the same time as you create the API itself. 

#### Database
I am using SQLite since it is lightweight and comes built in with Python.
On top of this I am using SQLAlchemy as the ORM. SQLAlchemy is frequently used with Flask.

I am also using Marshmallow, a schema library, to provide a layer 
of error handling and data standardization between the API and the SqlAlchemy 
ORM.

The t_customers table is populated with the customer JSON provided, as well as a timestamp.

The t_customer_authentication table holds an email primary and foreign key, and the user's password.


### To-Do List:
- Sign up/New User flow
  - This needs to be improved. Currently, a user can signup, login and then create 
  their Customer object. The Customer object could be created at the same time 
  as signup, and the password could be part of the Customer object. I
  chose to create a separate table for passwords because the customers provided in 
  the export did not have passwords, and this should be a required field, (and not one
  you can use a default for). 
- Add Sentry for improved error logging, and Datadog for metrics.
- Authentication is not production-ready:
  - Add JWT tokens on log in to persist the user session
  - Add authentication login requirement on endpoints 
- Convert SQLite db to Postgres, and use Alembic for migrations so there
is a record of database changes.
- Add tests.

