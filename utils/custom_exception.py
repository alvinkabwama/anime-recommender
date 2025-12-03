import sys
from typing import Any

class CustomException(Exception):
    def __init__(self, error_message: Any, error_detail: sys) -> None:
        # Coerce any incoming message/exception to string
        msg_str = str(error_message)

        # Get traceback from the *current* exception context via sys.exc_info()
        _exc_type, _exc_value, exc_tb = error_detail.exc_info()

        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.filename = exc_tb.tb_frame.f_code.co_filename
        else:
            # Fallbacks if raised outside of an except block
            self.lineno = "Unknown Line"
            self.filename = "Unknown File"

        self.error_message = msg_str

        super().__init__(self.__str__())

    def __str__(self) -> str:
        return (
            "Error occurred in python script [{0}] at line [{1}] | message: [{2}]"
            .format(self.filename, self.lineno, self.error_message)
        )