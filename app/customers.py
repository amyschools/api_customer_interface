import flask
import marshmallow
import typing as _t
from flask import abort, make_response, current_app

from app.models import Customer, customer_schema, customers_schema
from config import db

ACCEPTED_LANGAUGES = ["de", "en"]


def get_list():
    """
    Get a list of all customers
    """
    people = Customer.query.all()
    return customers_schema.dump(people)


def get_single(email: str) -> _t.Dict | flask.Response:
    """
    Get a single customer using their email
    """
    customer = Customer.query.filter(Customer.email == email).one_or_none()

    if customer is not None:
        return customer_schema.dump(customer)
    else:
        current_app.logger.warning("%s not found", email)
        abort(404, f"{email} not found")


def create(customer: _t.Dict) -> _t.Tuple | flask.Response:
    """
    Create a new customer if one with the provided email does not exist
    """
    email = customer.get("email")
    existing_person = Customer.query.filter(Customer.email == email).one_or_none()

    if existing_person is None:
        try:
            new_person = customer_schema.load(customer, session=db.session)
        except marshmallow.exceptions.ValidationError as e:
            current_app.logger.error("%s", e)
            return abort(400, str(e))

        db.session.add(new_person)
        db.session.commit()
        return customer_schema.dump(new_person), 201

    else:
        current_app.logger.warning("%s already exists", email)
        abort(
            400,
            f"Person with email {email} already exists",
        )


def update(email: str, language: _t.Dict) -> _t.Tuple | flask.Response:
    """
    Update a customer's language preference
    """
    existing_person = Customer.query.filter(Customer.email == email).one_or_none()
    updated_language = language["language"].lower()
    if existing_person:
        if updated_language not in ACCEPTED_LANGAUGES:
            return abort(
                400,
                f"Supported languages are {ACCEPTED_LANGAUGES}",
            )
        existing_person.language = language["language"]
        db.session.commit()
        return customer_schema.dump(existing_person), 200
    else:
        current_app.logger.warning("%s not found", email)
        abort(404, f"{email} not found")


def delete(email: str) -> flask.Response:
    """
    Delete a customer's record from the db
    """
    existing_person = Customer.query.filter(Customer.email == email).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{email} successfully deleted", 200)
    else:
        current_app.logger.warning("%s not found", email)
        abort(404, f"Person with email {email} not found")
