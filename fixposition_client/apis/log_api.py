from typing import Literal, Optional

from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class LoggingAPI:

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def disk(
            self, 
            action: Literal["status", "mount", "umount"],
            disk: Optional[Literal["external"]] = None,
        ):
        """Disk actions (mount, umount, info)."""
        try:
            data = models.LogDisk(
                action=action, 
                disk=disk,
            ).model_dump(exclude_none=True)
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/log/disk", "POST", data)

    def ls(self):
        """Get list of available logs on all disks."""
        data = models.LogLs().model_dump()
        return self.client.api_request("/log/ls", "POST", data)

    def dl(
            self,
            disk: Literal["internal", "external"],
            name: str,
        ):
        """Download a log."""
        try:
            params = models.LogDownload(
                disk=disk,
                name=name,
            ).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.download_file("/log/dl", params)

    def rm(
            self,
            disk: Literal["internal", "external"],
            files: list[str],
        ):
        """Delete log(s)."""
        try:
            data = models.LogRm(
                disk=disk,
                files=files,
            ).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/log/rm", "POST", data)
