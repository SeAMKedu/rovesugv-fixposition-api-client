from fixposition_client.api_client import APIClient


class API:
    """API responsiveness monitoring."""

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def api_up(self):
        """Check if the API is up."""
        return self.client.api_request("/api_up", "GET")
