class ParameterException(Exception):
    def __init__(
            self,
            error_code: int,
            expected_type, #issue_4
            parameter_type, #issue_4
            method_name: str,
            parameter_name: str
    ):
        self.error_code = error_code
        self.expected_type = expected_type
        self.parameter_type = parameter_type
        self.parameter_name = parameter_name
        self.method_name = method_name
        self.message = (
            f"In `{method_name}` method, `{parameter_name}` parameter"
            f" Exception ({error_code}). {parameter_type} type founded"
            f" instead of {expected_type}"
        )
