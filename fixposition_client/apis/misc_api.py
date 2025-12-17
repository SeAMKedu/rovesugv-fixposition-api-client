from typing import Optional

from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class MiscAPI:

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def data_get(self):
        """Get user data."""
        return self.client.api_request("/misc/data_get", "GET")

    def data_set(
            self,
            user_string: Optional[str] = None,
            user_json: Optional[dict] = None,
        ):
        """Set user data."""
        try:
            data = models.UserData(
                user_string=user_string,
                user_json=user_json,
            ).model_dump(exclude_none=True)
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/misc/data_set", "POST", data)

    def data_reset(self):
        """Reset user data."""
        data = models.ResetDefault().model_dump()
        return self.client.api_request("/misc/data_reset", "POST", data)
