import os
import mysql.connector as mysql
from models.seat import Seat
from services.parser import parse_in


class DbController:
    def __init__(self, flight_id: str):
        try:
            # load_dotenv() # Load the env file
            self._flight_id = flight_id
            self.connection = mysql.connect(
                host="localhost",
                user="root",
                passwd="raven",
                database="dbflight",
                auth_plugin='mysql_native_password'
            )
            self._db = self.connection.cursor()
            if not self.flight_entry_exists(flight_id):
                self.create_table()
        except Exception as e:
            print("Error connecting to the database:", e)
            exit(-1)

    def create_table(self):
        try:
            self._db.execute(f"CREATE TABLE `{self._flight_id}` (SEAT_NUMBER VARCHAR(5), NAME_UNDER VARCHAR(100))")
            self.connection.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

    def store_seat_details(self, name: str, seat: Seat):
        try:
            # Fixed the SQL query - was missing closing parenthesis and name parameter
            seat_number = parse_in(seat.row, seat.column)
            self._db.execute(f"INSERT INTO `{self._flight_id}` VALUES (%s, %s)", (seat_number, name))
            self.connection.commit()
        except Exception as e:
            print(f"Error storing seat details: {e}")

    def flight_entry_exists(self, flight_id: str) -> bool:
        try:
            self._db.execute("""
                        SELECT COUNT(*)
                        FROM information_schema.tables
                        WHERE table_schema = DATABASE()
                        AND table_name = %s
                        """, (flight_id,))
            return self._db.fetchone()[0] == 1
        except Exception as e:
            print("Error checking if flight entry exists:", e)
            return False

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def fetch_details(self, seat_pos: str) -> tuple | None:

        try:
            self._db.execute(f"SELECT * FROM `{self._flight_id}` WHERE SEAT_NUMBER = %s", (seat_pos,))

            result = self._db.fetchone()
            return result

        except Exception as e:
            print(f"Error fetching seat details: {e}")
            return None

    def fetch_all_seats(self) -> list:
        """
        Fetch all seat details for the flight
        Returns: list of tuples [(seat_number, name), ...]
        """
        try:
            self._db.execute(f"SELECT * FROM `{self._flight_id}`")
            return self._db.fetchall()
        except Exception as e:
            print(f"Error fetching all seats: {e}")
            return []



