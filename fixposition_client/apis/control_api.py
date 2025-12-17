from typing import Literal, Optional

from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class ControlAPI:

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def status(self):
        """Get system and service status."""
        return self.client.api_request("/ctrl/status", "GET")

    def action(
            self, 
            system: Optional[Literal["reboot", "shutdown"]] = None,
            rtk: Optional[Literal["restart"]] = None,
            camera: Optional[Literal["restart"]] = None,
            fusion: Optional[Literal["start", "stop", "restart"]] = None,
            websocket: Optional[Literal["restart"]] = None,
            wheels: Optional[Literal["restart"]] = None,
            io: Optional[Literal["reload"]] = None,
        ):
        """Control system and services."""
        try:
            if system:
                data = models.ControlSystem(system=system).model_dump()
            else:
                data = models.ControlService(
                    rtk=rtk,
                    camera=camera,
                    fusion=fusion,
                    websocket=websocket,
                    wheels=wheels,
                    io=io,
                ).model_dump(exclude_none=True)
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/ctrl/action", "POST", data)
