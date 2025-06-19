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
                user="YOUR_USERNAME_HERE",
                passwd="YOUR_PASSWORD_HERE",
                database="dbflight",
                auth_plugin='mysql_native_password',
                autocommit=False
            )
            self._db = self.connection.cursor()
            if not self.flight_entry_exists(flight_id):
                self.create_table()
        except Exception as e:
            print("Error connecting to the database:", e)
            exit(-1)

    def create_table(self):
        try:
            query = f"CREATE TABLE IF NOT EXISTS `{self._flight_id}` (SEAT_NUMBER VARCHAR(5) PRIMARY KEY, NAME_UNDER VARCHAR(100) NOT NULL)"
            self._db.execute(query)
            self.connection.commit()
            print(f"Table for flight {self._flight_id} created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
            self.connection.rollback()

    def store_seat_details(self, name: str, seat: Seat):
        try:
            seat_number = parse_in(seat.row, seat.column)
            print(f"DEBUG: Storing seat {seat_number} for {name}")  # Debug print

            # Check if seat already exists
            check_query = f"SELECT COUNT(*) FROM `{self._flight_id}` WHERE SEAT_NUMBER = %s"
            self._db.execute(check_query, (seat_number,))
            exists = self._db.fetchone()[0] > 0

            if exists:
                print(f"DEBUG: Seat {seat_number} already exists, updating...")
                update_query = f"UPDATE `{self._flight_id}` SET NAME_UNDER = %s WHERE SEAT_NUMBER = %s"
                self._db.execute(update_query, (name, seat_number))
            else:
                print(f"DEBUG: Inserting new seat {seat_number}...")
                insert_query = f"INSERT INTO `{self._flight_id}` (SEAT_NUMBER, NAME_UNDER) VALUES (%s, %s)"
                self._db.execute(insert_query, (seat_number, name))

            # Commit the transaction
            self.connection.commit()
            print(f"DEBUG: Transaction committed for seat {seat_number}")

            # Verify the insert
            verify_query = f"SELECT * FROM `{self._flight_id}` WHERE SEAT_NUMBER = %s"
            self._db.execute(verify_query, (seat_number,))
            result = self._db.fetchone()
            print(f"DEBUG: Verification result: {result}")

        except Exception as e:
            print(f"Error storing seat details: {e}")
            self.connection.rollback()
            raise e

    def flight_entry_exists(self, flight_id: str) -> bool:
        try:
            self._db.execute("""
                        SELECT COUNT(*)
                        FROM information_schema.tables
                        WHERE table_schema = DATABASE()
                        AND table_name = %s
                        """, (flight_id,))
            result = self._db.fetchone()[0] == 1
            print(f"DEBUG: Flight table exists: {result}")
            return result
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

    def fetch_details(self, seat_input: str) -> tuple | None:
        try:
            # Parse the seat input to get the seat number format expected in DB
            from services.parser import parse_out
            row, col = parse_out(seat_input)
            seat_number = parse_in(row, col)

            print(f"DEBUG: Fetching details for seat {seat_number}")
            query = f"SELECT SEAT_NUMBER, NAME_UNDER FROM `{self._flight_id}` WHERE SEAT_NUMBER = %s"
            self._db.execute(query, (seat_number,))
            result = self._db.fetchone()
            print(f"DEBUG: Fetch result: {result}")
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
            query = f"SELECT SEAT_NUMBER, NAME_UNDER FROM `{self._flight_id}`"
            self._db.execute(query)
            result = self._db.fetchall()
            print(f"DEBUG: All seats: {result}")
            return result
        except Exception as e:
            print(f"Error fetching all seats: {e}")
            return []

    def debug_table_contents(self):
        try:
            query = f"SELECT * FROM `{self._flight_id}`"
            self._db.execute(query)
            results = self._db.fetchall()
            print(f"DEBUG: Table contents for {self._flight_id}:")
            for row in results:
                print(f"  {row}")
            return results
        except Exception as e:
            print(f"Error debugging table contents: {e}")
            return []