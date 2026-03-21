class ParsingException(Exception):
    def __init__(
            self,
            error_code: int,
            message: str,
            expected_key: str,
            csv_header: list[str]
    ):
        super().__init__(error_code, message, expected_key, csv_header)
        self.error_code = error_code
        self.message = message
        self.expected_key = expected_key
        self.csv_header = csv_header