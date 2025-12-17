from typing import List, Literal

from pydantic import ValidationError

from fixposition_client import exceptions
from fixposition_client import models
from fixposition_client.api_client import APIClient


class CameraAPI:

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def calib_check(self):
        """Check if camera calibration is present."""
        return self.client.api_request("/camera/calib_check", "GET")

    def calib_upl(self, filepath: str):
        """Upload camera calibration file."""
        try:
            files = {"file": open(filepath, "rb")}
        except FileNotFoundError as error:
            return exceptions.handle_file_not_found_error(error)
        return self.client.api_request("/camera/calib_upl", "POST", files=files)

    def rec_ls(self):
        """List available recordings and disk info."""
        return self.client.api_request("/camera/rec_ls", "POST", data={})

    def rec_dl(self, filename: str):
        """Download a bag file."""
        try:
            params = models.CameraRecDl(name=filename).model_dump()
        except ValidationError as error:
            return exceptions.handle_validation_error(error)
        self.client.download_file("/camera/rec_dl", params)

    def rec_rm(self, files: List[str]):
        """Remove (delete) recording(s)."""
        try:
            data = models.CameraRecRm(files=files).model_dump()
        except ValidationError as error:
            return exceptions.handle_validation_error(error)
        return self.client.api_request("/camera/rec_rm", "POST", data)

    def record(self, action: Literal["start", "stop", "status"]):
        """Record camera calibration sequence."""
        try:
            data = models.CameraRecord(action=action).model_dump()
        except ValidationError as error:
            return exceptions.handle_validation_error(error)
        return self.client.api_request("/camera/record", "POST", data)

    def stream(self):
        """Camera image stream (low rate, low resolution, distorted)."""
        self.client.stream("/camera/stream")
