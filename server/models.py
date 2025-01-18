from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # Prevent 'restaurant_pizzas' from being serialized by excluding it in the fields
    serialize_only = ('id', 'name', 'address')

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # Prevent 'restaurant_pizzas' from being serialized by excluding it in the fields
    serialize_only = ('id', 'name', 'ingredients')

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    pizza = db.relationship('Pizza', backref='restaurant_pizzas')
    restaurant = db.relationship('Restaurant', backref='restaurant_pizzas')

    # Prevent 'pizza' and 'restaurant' from being serialized by excluding them in the fields
    serialize_only = ('id', 'price', 'pizza_id', 'restaurant_id')

    # Add validation for price range
    @validates('price')
    def validate_price(self, key, value):
        if value < 1 or value > 30:
            raise ValueError('Price must be between 1 and 30')
        return value

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
