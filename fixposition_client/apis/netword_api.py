from typing import Literal, Optional

from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class NetworkAPI:

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def online(self):
        """Check if the sensor is online."""
        return self.client.api_request("/net/online", "GET")

    def status(self):
        """Get network devices (interfaces) connection status."""
        return self.client.api_request("/net/status", "GET")

    def conn_get(self):
        """Get network connections config."""
        return self.client.api_request("/net/conn_get", "GET")

    def conn_set(
            self,
            connection: str,
            auto: Optional[bool] = None,
            ip4addr: Optional[str] = None,
            ip4gw: Optional[str] = None,
            ip4dns: Optional[str] = None,
            ip4method: Optional[Literal["auto", "manual", "shared"]] = None,
            psk: Optional[str] = None,
            keymgmt: Optional[str] = None,
            ssid: Optional[str] = None,
        ):
        """Set network connections config."""
        try:
            data = models.NetworkConnSet(
                connection=connection,
                auto=auto,
                ip4addr=ip4addr,
                ip4gw=ip4gw,
                ip4dns=ip4dns,
                ip4method=ip4method,
                psk=psk,
                keymgmt=keymgmt,
                ssid=ssid,
            ).model_dump(exclude_none=True)
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/net/conn_set", "POST", data)

    def conn_up(self, connection: str):
        """Connect network connection."""
        try:
            data = models.NetworkConnection(connection=connection).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/net/conn_up", "POST", data)

    def conn_down(self, connection: str):
        """Disconnect network connection."""
        try:
            data = models.NetworkConnection(connection=connection).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/net/conn_down", "POST", data)

    def conn_reset(self):
        """Reset all connections to default."""
        data = models.ResetDefault().model_dump()
        return self.client.api_request("/net/conn_reset", "POST", data)

    def wifi_list(self):
        """List available Wi-Fi networks."""
        return self.client.api_request("/net/wifi_list", "GET")

    def wifi_add(
            self,
            ssid: str,
            psk: str,
            keymgmt: str,
            auto: Optional[bool] = None,
            ip4addr: Optional[str] = None,
            ip4gw: Optional[str] = None,
            ip4dns: Optional[str] = None,
            ip4method: Optional[Literal["auto", "manual", "shared"]] = None,
        ):
        """Add a Wi-Fi network connection."""
        try:
            data = models.WiFiAdd(
                ssid=ssid,
                psk=psk,
                keymgmt=keymgmt,
                auto=auto,
                ip4addr=ip4addr,
                ip4gw=ip4gw,
                ip4dns=ip4dns,
                ip4method=ip4method
            ).model_dump(exclude_none=True)
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/net/wifi_add", "POST", data)

    def wifi_remove(self, ssid: str):
        """Remove a Wi-Fi network connection."""
        data = models.WifiRemove(ssid=ssid).model_dump()
        return self.client.api_request("/net/wifi_remove", "POST", data)

    def wifi_cfg(
            self,
            action: Literal["get", "set", "reset"],
            config_band: Optional[Literal["a", "bg", "off"]] = None,
            config_ap: Optional[bool] = None,
            reset: Optional[str] = "default",
        ):
        """Wi-Fi configuration."""
        try:
            data = models.WifiCfg(
                action=action,
                config_band=config_band,
                config_ap=config_ap,
                reset=reset,
            ).model_dump(exclude_none=True)
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/net/wifi_cfg", "POST", data)
