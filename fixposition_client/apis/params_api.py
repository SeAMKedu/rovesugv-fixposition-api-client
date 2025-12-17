from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class ParamsAPI:

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def config_get(self):
        """Get current configuration parameters."""
        return self.client.api_request("/params/config/get", "GET")

    def config_def(self):
        """Get default configuration (a.k.a. customer config) parameters."""
        return self.client.api_request("/params/config/def", "GET")

    def config_set(self, params: dict):
        """Set current configuration (a.k.a. customer config) parameters."""
        try:
            data = models.ParamsConfigSet(params=params).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/params/config/set", "POST", data)

    def config_reset(self):
        """Reset current configuration (a.k.a. customer config) parameters to default."""
        data = models.ResetDefault().model_dump()
        return self.client.api_request("/params/config/reset", "POST", data)

    def camera_get(self):
        """Get camera information."""
        return self.client.api_request("/params/camera/get", "GET")

    def hw_get(self):
        """Get hardware information."""
        return self.client.api_request("/params/hw/get", "GET")
