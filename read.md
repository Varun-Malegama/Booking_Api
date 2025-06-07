Project Description:

A RESTful API built using Python Flask that allows users to view and book fitness classes. Includes MySQL database integration and logging for monitoring requests.


Features:

- User registration and authentication
- View available fitness classes
- Book or cancel classes
- Admin panel for managing classes
- MySQL integration
- Logging and error handling


Technologies Used:

- Python 3.11
- Flask & Flask-RESTful
- MySQL
- SQLAlchemy / MySQL Connector
- Logging module
- dotenv for environment variables


Project Structure:

app.py               # Flask app and API initialization
bookingApi.py        # Core logic for viewing, booking, and retrieving bookings
database.py          # Database connection using credentials from .env
requirements.txt     # Python dependencies
.env                 # Environment variables for DB and logging
README.md            # Project documentation


app.py — Application Entry Point:

- Initializes Flask and Flask-RESTful API
- Loads environment variables using dotenv
- Configures logging (log_path from .env)
- Registers API resources:
- /classes → List all classes
- /book → Book a fitness class
- /bookings → View existing bookings


bookingApi.py — Booking Logic

Defines three resources for API endpoints:
Classes (GET /classes):
 - Fetches all available classes from the database.
 - Logs success or errors.
Book (POST /book):
 - Validates the requested class and available slots.
 - Prevents duplicate bookings.
 - Inserts a new booking and updates the class's available slots.
 - Returns appropriate status codes and logs actions.
Bookings (GET /bookings):
 - Fetches all bookings or filters by client email.
 - Returns the booking records and logs the request.


database.py:

- Loads DB credentials from .env
- Creates and returns a MySQL connection
- Used by all API endpoints for DB operations


Setup Instructions:

Clone the repository:

using hte below command you can clone into your machine
git clone https://github.com/Varun-Malegama/Booking_Api.git


Install dependencies:

using the below command install dependencies
pip install -r requirements.txt


Setup the .env file:

Replace with your credentials

host=localhost
user_name= Your username
password= Your password
db=fitness_bookings


Run:

Run the file with the below command in your terminal after setup or just click the run button in your vscode
python .\app.py


MySQL Table Sructure:

CREATE TABLE classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    instructor VARCHAR(100),
    available_slots INT
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_id INT,
    client_name VARCHAR(100),
    client_email VARCHAR(100),
    FOREIGN KEY (class_id) REFERENCES classes(id)
);


Postman URL'S:

'Get' call = http://127.0.0.1:5000/classes
'Get call' = http://127.0.0.1:5000/classes?timezone=America/New_York    #sample timezone get call
'Post' call = http://127.0.0.1:5000/book
'Get' call = http://127.0.0.1:5000/bookings
'Get' call = http://127.0.0.1:5000/bookings?email=pavan@gmail.com


Sample json data for post call:

{
  "class_id": 1,
  "client_name": "Pavan",
  "client_email": "pavan@gmail.com"
}


NOTE:

- Ensure your DB has two tables: classes and bookings
- Logs are written to the file specified in log_path
- Use Postman or similar tools for API testing