from models.seat import Seat


def parse_in(row, col) -> str:
    return str(row) + str(col)


def parse_out(seat_id: str):
    """
    Parse seat string like "1F" into [row_int, col_str]
    Returns: [int, str] - row as integer, column as string
    """
    if len(seat_id) < 2:
        raise ValueError("Invalid seat format")

    # Extract row number and column letter
    row_str = seat_id[:-1]  # Everything except last character
    col_str = seat_id[-1].upper()  # Last character, uppercase

    try:
        row_int = int(row_str)
    except ValueError:
        raise ValueError("Invalid row number")

    # Validate column
    if col_str not in "ABCDEF":
        raise ValueError("Invalid column letter")

    # Validate row range
    if row_int < 1 or row_int > 30:
        raise ValueError("Row must be between 1 and 30")

    return [row_int, col_str]