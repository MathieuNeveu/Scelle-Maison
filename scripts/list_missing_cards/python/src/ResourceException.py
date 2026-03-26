class ResourceException(Exception):
    def __init__(
            self,
            error_code: int,
            resource_location: str
    ):
        self.error_code = error_code
        self.resource_location = resource_location
        self.message = (
            f"No such file in directory."
            f" Make sure to fill an absolute csv file path."
            f" Location that caused failure: {resource_location}"
        )
