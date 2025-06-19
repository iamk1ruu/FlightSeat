import ui.console_ui as ui
from services.parser import parse_out
from models.flight import Flight
from utils.dbcontroller import DbController


class DEBUGTRACE:
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
                flight_id = input()
                print(f"DEBUG: Creating flight with ID: {flight_id}")
                self._flight = Flight(flight_id)
                self._seats = self._flight.seats
                print(f"DEBUG: Flight created, seats initialized")
                self.reservation_menu()
            case 2:
                """Retrieve the Flight object, so we need to make flight parser methods in parser.py"""

    def reservation_menu(self):
        ui.display_seatmap(self._flight.id, self._seats)
        choice = int(input())
        match choice:
            case 1:
                seat_input = input("Which seat?")
                name_input = input("Under which name? ")
                print(f"DEBUG: Attempting to reserve seat {seat_input} for {name_input}")

                try:
                    # Validate seat input first
                    seat_pos = parse_out(seat_input)
                    print(f"DEBUG: Parsed seat position: {seat_pos}")

                    # Reserve the seat
                    self._flight.reserve_seat(name_input, seat_input)

                    # Debug: Check if seat is marked as taken
                    from services.parser import parse_out
                    row, col = parse_out(seat_input)
                    seat_mgr = self._flight._reservation._seat_mgr
                    seat_obj = seat_mgr.get_seat(row, col)
                    print(f"DEBUG: Seat {seat_input} is_taken: {seat_obj.is_taken}")

                    # Debug: Check database contents
                    db = DbController(self._flight.id)
                    db.debug_table_contents()

                    ui.success("Seat reserved successfully.")
                    self.reservation_menu()

                except Exception as e:
                    print(f"DEBUG: Error during reservation: {e}")
                    import traceback
                    traceback.print_exc()
                    ui.error("INVALID_SEAT_INPUT")
                    self.reservation_menu()

            case 2:
                seat_input = input("Which seat?")
                try:
                    print(f"DEBUG: Fetching details for seat {seat_input}")
                    self._db = DbController(self._flight.id)
                    details = self._db.fetch_details(seat_input)
                    if details:
                        ui.show_details(details)
                    else:
                        print("No details found for this seat.")
                        # Debug: Show all seats in database
                        print("DEBUG: All seats in database:")
                        self._db.debug_table_contents()
                    self.reservation_menu()
                except Exception as e:
                    print(f"DEBUG: Error fetching details: {e}")
                    import traceback
                    traceback.print_exc()
                    ui.error(err_id="ERROR_DB_SEAT", exception=e)
                    self.reservation_menu()