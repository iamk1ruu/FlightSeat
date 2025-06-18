from services.reservation import Reservation
import ui.console_ui as ui
class Flight:
    def __init__(self, flight_id: str):
        self._flight_id = flight_id
        self._reservation = Reservation(self._flight_id)

    def reserve_seat(self, name: str, seat_id: str):
        self._reservation.reserve(name, seat_id)

    @property
    def seats(self):
        return self._reservation.seats

    @property
    def id(self):
        return self._flight_id









