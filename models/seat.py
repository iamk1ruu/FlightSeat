class Seat:
    def __init__(self, row: int, column: str):
        """ Declaring the variables in the constructor is fine in Python, no need to place it globally"""
        self._row = row
        self._column = column
        self._is_taken = False

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    def reserve(self):
        self._is_taken = True

    @property
    def is_taken(self):
        return self._is_taken