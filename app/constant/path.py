
import re
URL_REGEX = {
    "USER_INFO": {
        "regex": r"^/users/([a-zA-Z0-9]+)$",
        "path": "/users/{id}"
    }
}

def check_and_return_path(input_string: str) -> str:
    pattern = re.compile(URL_REGEX["USER_INFO"]["regex"])
    match = pattern.match(input_string)
    if match:
        return URL_REGEX["USER_INFO"]["path"]
    return input_string #return fault path