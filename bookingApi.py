from flask_restful import Resource
from flask import request
from database import get_db_connection
import logging
from datetime import datetime
import pytz
from dateutil import tz

class Classes(Resource):
    def get(self):
        client_timezone = request.args.get("timezone", "Asia/Kolkata")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute("SELECT * FROM classes")
            classes = cursor.fetchall()

            # Convert class_time from IST to client's timezone
            ist = pytz.timezone("Asia/Kolkata")
            user_tz = pytz.timezone(client_timezone)

            for cls in classes:
                if cls.get("class_time"):
                    ist_time = ist.localize(cls["class_time"])
                    local_time = ist_time.astimezone(user_tz)
                    cls["class_time_local"] = local_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
                    cls["class_time"] = cls["class_time"].strftime("%Y-%m-%d %H:%M:%S")


            logging.info(f"Fetched classes with timezone adjustment to {client_timezone}")
            return classes, 200

        except Exception as e:
            logging.error(f"Error fetching classes: {str(e)}")
            return {"message": "Error fetching classes"}, 500

        finally:
            cursor.close()
            conn.close()


class Book(Resource):
    def post(self):
        data = request.get_json()
        class_id = data.get("class_id")
        client_name = data.get("client_name")
        client_email = data.get("client_email")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        try:
            # Check if class exists and slots are available
            cursor.execute("SELECT * FROM classes WHERE id = %s", (class_id,))
            class_info = cursor.fetchone()

            if not class_info:
                return {"message": "Class not found."}, 404

            if class_info["available_slots"] <= 0:
                return {"message": "No slots available."}, 400
            
            # Check if booking already exists or not to avoid duplicates
            cursor.execute("""
                SELECT * FROM bookings 
                WHERE class_id = %s AND client_name = %s AND client_email = %s
            """, (class_id, client_name, client_email))
            existing_booking = cursor.fetchone()

            if existing_booking:
                return {"message": "Booking already exists for this client."}, 409

            # Insert booking
            cursor.execute("""
                INSERT INTO bookings (class_id, client_name, client_email)
                VALUES (%s, %s, %s)
            """, (class_id, client_name, client_email))

            # Update slots
            cursor.execute("""
                UPDATE classes SET available_slots = available_slots - 1 WHERE id = %s
            """, (class_id,))

            conn.commit()
            logging.info(f"Booking successful for {client_name} in class {class_id}")
            return {"message": "Booking successful"}, 201

        except Exception as e:
            conn.rollback()
            logging.error(f"Error booking class: {str(e)}")
            return {"message": "Internal server error"}, 500

        finally:
            cursor.close()
            conn.close()

class Bookings(Resource):
    def get(self):
        client_email = request.args.get("email")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        try:
            if client_email:
                cursor.execute("""
                    SELECT id, class_id, client_name, client_email
                    FROM bookings
                    WHERE client_email = %s
                """, (client_email,))
                logging.info(f"Fetched bookings for email: {client_email}")
            else:
                cursor.execute("""
                    SELECT id, class_id, client_name, client_email
                    FROM bookings
                """)
                logging.info("Fetched all bookings.")

            bookings = cursor.fetchall()
            return bookings, 200

        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error fetching bookings: {str(e)}")
            return {"message": "Error fetching bookings"}, 500

        finally:
            cursor.close()
            conn.close()