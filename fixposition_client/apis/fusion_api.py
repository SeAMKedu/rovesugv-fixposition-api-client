from typing import Literal, Optional, Union

from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class FusionAPI:

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def control(
            self, 
            action: Literal["status", "enable", "disable", "reset"],
        ):
        """Control Fusion service."""
        try:
            data = models.FusionControl(action=action).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/fusion/ctrl", "POST", data)

    def data(
            self,
            stationary: Literal["", "remove"],
            warmstart: Literal["", "remove"],
        ):
        """Fusion persistent data."""
        try:
            data = models.FusionData(
                stationary=stationary,
                warmstart=warmstart,
            ).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/fusion/data", "POST", data)

    def initialpose(
            self,
            action: Literal["save", "load", "delete", "get", "set"],
            slot: Optional[Union[int, Literal["*"]]] = None,
            label: Optional[str] = None,
            states: Optional[list] = None,
        ):
        """Fusion saved poses management."""
        try:
            if action == "save" and isinstance(slot, int) and label:
                data = models.FusionPoseSave(slot=slot, label=label).model_dump()
            elif action == "load" and isinstance(slot, int):
                data = models.FusionPoseLoad(slot=slot).model_dump()
            elif action == "delete" and slot:
                data = models.FusionPoseDelete(slot=slot).model_dump()
            elif action == "get":
                data = models.FusionPoseGet().model_dump()
            elif action == "set" and states:
                data = models.FusionPoseSet(states=states).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/fusion/initialpose", "POST", data)
