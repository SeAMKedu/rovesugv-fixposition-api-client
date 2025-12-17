from fixposition_client.api_client import APIClient


class SystemInfoAPI:
    """System information API."""

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)
    
    def load(self):
        """Get system load."""
        return self.client.api_request("/sys/load", "GET")

    def cpu(self):
        """Get CPU load and temperature."""
        return self.client.api_request("/sys/cpu", "GET")

    def uptime(self):
        """Get system uptime."""
        return self.client.api_request("/sys/uptime", "GET")

    def load_cpu_uptime(self):
        """Get system load and uptime, CPU load and temperature."""
        return self.client.api_request("/sys/load_cpu_uptime", "GET")

    def info(self):
        """Get system information."""
        return self.client.api_request("/sys/info", "GET")

    def timesync(self):
        """Get system time sync status."""
        return self.client.api_request("/sys/timesync", "GET")
