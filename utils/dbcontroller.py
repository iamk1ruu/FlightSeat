import os
import mysql.connector as mysql
from models.seat import Seat
from dotenv import load_dotenv
from services.parser import parse_in
"""
import mysql.connector as mysql
from tkinter import messagebox
import tkinter as tk

#connect to mysql 9.1
connection = mysql.connect(host="localhost", user="root", passwd="123456", \
                           database="dbstudent")
mydb = connection.cursor()
"""

class DbController:
    def __init__(self, flight_id: str):
        try:
            load_dotenv() # Load the env file
            self._flight_id = flight_id
            self.connection = mysql.connect(
                ... # REPLACE
            )


            self._db = self.connection.cursor()
            self.create_table()
        except Exception as e:
            print("Error connecting to the database:")
            print(e)
            exit(-1)

    def create_table(self):
        self._db.execute(f"CREATE TABLE {self._flight_id} (SEAT_NUMBER VARCHAR(5), NAME_UNDER VARCHAR(100));")

    def store_seat_details(self, name: str, seat: Seat):
        self._db.execute(f"INSERT INTO {self._flight_id} VALUES({parse_in(seat.row, seat.column)}")


if __name__ == "__main__":
    db = DbController("A12345")
    db.store_seat_details("RAVEN NEIL OCAMPO", Seat(5,"A"))