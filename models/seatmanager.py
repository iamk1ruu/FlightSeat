from models.seat import Seat
import ui.console_ui as ui
class SeatManager:
    def __init__(self, rows=30, cols="ABCDEF"):
        self._seats = [[Seat(row + 1, col) for col in cols] for row in range(rows)]


    def get_seat(self, row: int, col: str) -> Seat:
        return self._seats[row - 1]["ABCDEF".index(col.upper())]

    @property
    def seats(self):
        return self._seats

    def is_available(self, row: int, col: str):
        return not self.get_seat(row, col).is_taken

