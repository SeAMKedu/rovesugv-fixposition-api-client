from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class MapAPI:

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def token_get(self, which: str):
        """Get map access token."""
        try:
            data = models.MapTokenGet(which=which).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/map/token_get", "POST", data)

    def token_set(self, which: str, token: str):
        """Set map access token."""
        try:
            data = models.MapTokenSet(which=which, token=token).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/map/token_set", "POST", data)

    def token_reset(self, which: str):
        """Reset map access token."""
        try:
            data = models.MapTokenReset(which=which).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/map/token_reset", "POST", data)
