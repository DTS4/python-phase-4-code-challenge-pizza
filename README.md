# Restaurant and Pizza Management API

## Features
* **Restaurant Management**
  - View all restaurants
  - View a specific restaurant by ID
  - Delete a restaurant by ID
* **Pizza Management**
  - View all pizzas
* **Restaurant Pizza Management**
  - Associate pizzas with restaurants
  - Validate price range for restaurant pizzas (between $1 and $30)
  - Handle errors for invalid data inputs

## Technologies Used
* Python (Flask Framework)
* SQLAlchemy for database management
* SQLite for data storage
* Pytest for testing

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Set up a virtual environment and install dependencies:
   ```bash 
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. Set up the database:
   ```bash
   flask db upgrade

4. Run the server:
   ```bash
   flask run

## API Endpoints
### Restaurants
* GET /restaurants: Retrieve all restaurants.
* GET /restaurants/int:id: Retrieve a single restaurant by ID.
* DELETE /restaurants/int:id: Delete a restaurant by ID. 

### Pizzas
* GET /pizzas: Retrieve all pizzas.

### Restaurant Pizzas
* POST /restaurant_pizzas: Create a restaurant-pizza association with price validation.

## Testing
 - Run tests using pytest:
   ```bash 
   pytest

## Error Handling
* Returns 404 for not found resources.
* Returns 400 for validation errors.

## Contribution
Feel free to fork this repository and submit pull requests.

## License 
 - This project is licensed under the MIT License.


