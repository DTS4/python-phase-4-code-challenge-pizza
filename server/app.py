from models import db, Restaurant, RestaurantPizza, Pizza
from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

api = Api(app)

# Initialize the app with the database
db.init_app(app)

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    with app.app_context():  # Ensures app context is available
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants])


@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant_by_id(id):
    with app.app_context():
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        
        restaurant_pizzas = RestaurantPizza.query.filter_by(restaurant_id=id).all()
        restaurant_data = restaurant.to_dict()
        restaurant_data["restaurant_pizzas"] = [rp.to_dict() for rp in restaurant_pizzas]
        
        return jsonify(restaurant_data)



@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    with app.app_context():
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204   


@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    with app.app_context():
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict() for pizza in pizzas])


@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        # Validation for missing fields
        if not all(k in data for k in ("price", "pizza_id", "restaurant_id")):
            return jsonify({"errors": ["Missing required fields"]}), 400

        # Price validation (1 <= price <= 30)
        if not (1 <= data["price"] <= 30):
            return jsonify({"errors": ["validation errors"]}), 400

        new_restaurant_pizza = RestaurantPizza(
            price=data["price"],
            pizza_id=data["pizza_id"],
            restaurant_id=data["restaurant_id"]
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        response_data = new_restaurant_pizza.to_dict()
        response_data["pizza"] = new_restaurant_pizza.pizza.to_dict()
        response_data["restaurant"] = new_restaurant_pizza.restaurant.to_dict()

        return jsonify(response_data), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["Invalid data or foreign key constraint violation"]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400   



if __name__ == "__main__":
    with app.app_context():   
        app.run(port=5555, debug=True)
