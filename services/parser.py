from models.seat import Seat
def parse_in(row, col) -> str:
    return str(row) + str(col)

def parse_out(seat_id: str):
    return [seat_id[0], seat_id[1]]


