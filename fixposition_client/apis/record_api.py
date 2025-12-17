from typing import Literal

from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class RecordAPI:

    def __init__(self, host: str) -> None:
        self.host = host
        self.client = APIClient(self.host)

    def info(self):
        """Logging information, such as available logging profiles (levels)."""
        return self.client.api_request("/record/info", "GET")

    def status(self):
        """Logging status."""
        return self.client.api_request("/record/status", "GET")

    def start(
            self,
            target: Literal["internal", "external", "download", "debuglog"],
            profile: Literal["minimal", "medium", "maximal", "calib", "debuglog"],
        ):
        """Start logging."""
        try:
            data = models.LogStart(
                target=target,
                profile=profile,
            ).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        if target == "download":
            self.client.download_log_file("/start", data)
        else:
            return self.client.api_request("/record/start", "POST", data=data)

    def stop(self):
        """Stop logging."""
        return self.client.api_request("/record/stop", "POST", {})
