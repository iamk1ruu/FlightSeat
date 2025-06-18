import ui.console_ui as ui
from services.parser import parse_out
from models.flight import Flight
from utils.dbcontroller import DbController


class Controller:
    def __init__(self):
        self._flight = None
        self._seats = None
        self._db = None
        self.main_menu()

    def main_menu(self):
        choice = ui.show_main()
        match choice:
            case 1:
                ui.new_flight()
                self._flight = Flight(input())
                self._seats = self._flight.seats
                self.reservation_menu()
            case 2:
                """Retrieve the Flight object, so we need to make flight parser methods in parser.py"""


    def reservation_menu(self):
        ui.display_seatmap(self._flight.id, self._seats)
        choice = int(input())
        match choice:
            case 1:
                seat_input = input("Which seat?")
                try:
                    seat_pos = parse_out(seat_input)
                    self._flight.reserve_seat(seat_pos[0], seat_pos[1])
                    ui.sucess("Seat reserved successfully.")
                except:
                    ui.error("INVALID_SEAT_INPUT")
            case 2:
                seat_input = input("Which seat?")
                try:
                    seat_pos = parse_out(seat_input)
                    self._db = DbController(self._flight.id)
                    ui.show_details(self._db.fetch_details(seat_pos))
                except Exception as e:
                    ui.error(err_id="ERROR_DB_SEAT", exception=Exception)




