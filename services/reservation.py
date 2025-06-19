from models.seatmanager import SeatManager
from utils.dbcontroller import DbController
import ui.console_ui as ui
from services.parser import parse_out  # Fixed import


class Reservation:
    def __init__(self, flight_id: str):
        self._seat_mgr = SeatManager()
        self._flight_id = flight_id
        self._db = DbController(flight_id)

    def is_ready(self) -> bool:
        return self._flight_id is not None and self._db is not None

    def reserve(self, name: str, seat_id: str):
        if not self.is_ready():
            ui.error("FLIGHT_NOT_READY")
            return

        try:
            row, col = parse_out(seat_id)

            if self._seat_mgr.is_available(row, col):
                seat = self._seat_mgr.get_seat(row, col)
                seat.reserve()
                self._db.store_seat_details(name, seat)
                ui.success(f"{seat_id} successfully reserved for {name}")
            else:
                ui.error("SEAT_TAKEN")
        except ValueError as e:
            ui.error("INVALID_SEAT_INPUT")
        except Exception as e:
            print(f"Reservation error: {e}")
            ui.error("RESERVATION_ERROR")

    @property
    def seats(self):
        return self._seat_mgr.seats