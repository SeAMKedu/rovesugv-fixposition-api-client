from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class WebAPI:

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def pw_get(self):
        """Get password protection state."""
        return self.client.api_request("/web/pw_get", "GET")

    def pw_set(self, username: str, password: str):
        """Enable password protection."""
        try:
            data = models.WebPwSet(
                username=username, 
                password=password,
            ).model_dump(by_alias=True)
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request( "/web/pw_set", "POST", data)

    def pw_reset(self):
        """Reset password protection to default (i.e., remove it)."""
        data = models.ResetDefault().model_dump()
        return self.client.api_request("/web/pw_reset", "POST", data)
