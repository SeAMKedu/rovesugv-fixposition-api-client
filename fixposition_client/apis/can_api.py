from typing import Literal

from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class CANInterfaceAPI:
    """CAN interface API."""

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def if_get(self):
        """Get CAN interface saved and active config."""
        return self.client.api_request("/can/if_get", "GET")

    def if_set(
            self, 
            enabled: bool, 
            bitrate: Literal[
                10000, 20000, 50000, 125000, 250000, 500000, 800000, 1000000], 
            dbitrate: Literal[
                10000, 20000, 50000, 125000, 250000, 500000, 800000, 1000000],
        ):
        """Set CAN interface saved config."""
        try:
            data = models.CANIfSet(
                config_enabled=enabled,
                config_bitrate=bitrate,
                config_dbitrate=dbitrate,
            ).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/can/if_set", "POST", data)

    def if_reset(self):
        """Reset CAN interface saved config to default."""
        data = models.ResetDefault().model_dump()
        return self.client.api_request("/can/if_reset", "POST", data)
