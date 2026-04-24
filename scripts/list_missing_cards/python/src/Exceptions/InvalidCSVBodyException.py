class InvalidCSVBodyException(Exception):
    def __init__(
            self,
            line_number,
            key
    ):
        self.message = (
                f"This file is not properly filled at line {line_number}, key '{key}'."
        )
        if line_number == 1:
            self.message += (
                f" Make sure to fill at least one line of content after the header."
            )
