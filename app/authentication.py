import flask
import marshmallow
import typing as _t

from flask import abort, current_app
from flask_bcrypt import generate_password_hash

from app.models import Customer, CustomerAuthentication, customer_auth_schema
from config import db


def login(customer_auth: _t.Dict) -> _t.Tuple | flask.Response:
    """
    Log in an existing customer using email and password
    """
    cust_auth = CustomerAuthentication.query.filter(
        CustomerAuthentication.email == customer_auth["email"]
    ).one_or_none()

    if cust_auth:
        authorized = cust_auth.check_password(customer_auth["password"])
        if not authorized:
            current_app.logger.warning("%s failed to log in", customer_auth["email"])
            abort(401, f"{customer_auth['email']} failed to log in")
        else:
            customer = Customer.query.filter(
                Customer.email == customer_auth["email"]
            ).one_or_none()
            if customer:
                return (customer.email, customer.language), 200
            else:
                return (cust_auth.email, f"No Language Added"), 200

    else:
        current_app.logger.warning("%s not found", customer_auth["email"])
        abort(404, f"{customer_auth['email']} not found")


def reset_password(customer_auth: _t.Dict) -> _t.Tuple | flask.Response:
    """
    Reset a customer's password and update the db with the hashed value
    """
    cust_auth = CustomerAuthentication.query.filter(
        CustomerAuthentication.email == customer_auth["email"]
    ).one_or_none()

    if cust_auth:
        hashed_password = generate_password_hash(customer_auth["password"])
        cust_auth.password = hashed_password
        db.session.commit()
        return customer_auth_schema.dump(cust_auth), 200
    else:
        current_app.logger.warning("%s not found", customer_auth["email"])
        abort(404, f"{customer_auth['email']} not found")


def sign_up(customer_auth: _t.Dict) -> _t.Tuple | flask.Response:
    """
    Create a new customer with email and password
    """
    email = customer_auth.get("email")
    cust_auth = CustomerAuthentication.query.filter(
        CustomerAuthentication.email == email
    ).one_or_none()

    if cust_auth is None:
        try:
            new_person = customer_auth_schema.load(customer_auth, session=db.session)
            hashed_password = generate_password_hash(new_person.password)
            new_person.password = hashed_password
        except marshmallow.exceptions.ValidationError as e:
            return abort(400, str(e))

        db.session.add(new_person)
        db.session.commit()
        return customer_auth_schema.dump(new_person), 201

    else:
        current_app.logger.warning("%s already exists", customer_auth["email"])
        abort(
            400,
            f"Customer with email {email} already exists",
        )
