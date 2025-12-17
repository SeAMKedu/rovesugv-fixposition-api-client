from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class BackupAPI:

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def get(self):
        """Get a configuration backup."""
        return self.client.api_request("/backup/get", "GET")

    def set(self, config: dict):
        """Restore a configuration backup."""
        try:
            data = models.BackupSet(config=config).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/backup/set", "POST", data)
