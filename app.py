from flask import Flask
from flask_restful import Api
from database import get_db_connection
from bookingApi import Classes, Book, Bookings
import logging
from flask.logging import default_handler
from dotenv import load_dotenv
import os

app = Flask(__name__)
api = Api(app)
mysql = get_db_connection()

app.logger.removeHandler(default_handler)

# Logging setup
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
log_filename = os.getenv('log_path')

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    filename=log_filename,
    filemode='w',
format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
)

api.add_resource(Classes, '/classes')
api.add_resource(Book, '/book')
api.add_resource(Bookings, '/bookings')

if __name__ == '__main__':
    app.run(debug=True)
