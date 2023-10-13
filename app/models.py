from datetime import datetime
from config import db, ma
from flask_bcrypt import generate_password_hash, check_password_hash


class Customer(db.Model):
    __tablename__ = "t_customers"
    customer_id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(32), unique=True)
    country = db.Column(db.String(2))
    language = db.Column(db.String(2))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class CustomerAuthentication(db.Model):
    __tablename__ = "t_customer_authentication"
    email = db.Column(
        db.String, db.ForeignKey("t_customers.email"), nullable=False, primary_key=True
    )
    password = db.Column(db.String(50), nullable=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)


class CustomerAuthenticationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerAuthentication
        load_instance = True
        include_fk = True
        sqla_session = db.session


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
customer_auth_schema = CustomerAuthenticationSchema()
