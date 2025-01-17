import os
from enum import Enum

class QuotedStr(str):
    """This class is used to generate the swagger yaml strings with
    double quote
    """
    pass


class SwaggerMessages(Enum):
    REPLACE_VALUE = "...Replace this value..."


BASE_LINK = os.getenv("JSRL_BASE_PATH", "http://localhost:8080")