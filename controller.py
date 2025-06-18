import ui.console_ui as ui
from models.flight import Flight

class Controller:
    def __init__(self):
        self._flight = None
        self._seats = None
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
