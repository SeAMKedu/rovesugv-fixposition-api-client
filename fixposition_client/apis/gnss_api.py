from typing import Literal

from pydantic import ValidationError

from fixposition_client import models
from fixposition_client.api_client import APIClient
from fixposition_client.exceptions import handle_validation_error


class GNSS_API:
    """GNSS (Global Navigation Satellite System) API."""

    def __init__(self, host: str) -> None:
        self.client = APIClient(host)

    def rtk_status(self):
        """Get RTK corrections stream status."""
        return self.client.api_request("/gnss/rtk_status", "GET")

    def rtk_get(self):
        """Get RTK correction stream parameters."""
        return self.client.api_request("/gnss/rtk_get", "GET")

    def rtk_set(
            self,
            ntrip_user: str,
            ntrip_pass: str,
            ntrip_host: str,
            ntrip_port: int,
            ntrip_mount: str,
            gga_mode: Literal["auto", "manual"],
            gga_lat: float,
            gga_lon: float,
            gga_height: float,
            source: Literal["ntrip", "serial"],
        ):
        """Set RTK correction stream parameters."""
        try:
            data = models.GNSS_RTKSet(
                ntrip_user=ntrip_user,
                ntrip_pass=ntrip_pass,
                ntrip_host=ntrip_host,
                ntrip_port=ntrip_port,
                ntrip_mount=ntrip_mount,
                gga_mode=gga_mode,
                gga_lat=gga_lat,
                gga_lon=gga_lon,
                gga_height=gga_height,
                source=source,
            ).model_dump()
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/gnss/rtk_set", "POST", data)

    def rtk_reset(self):
        """Reset RTK correction stream parameters to default."""
        data = models.ResetDefault().model_dump()
        return self.client.api_request("/gnss/rtk_reset", "POST", data)

    def rx_reset(self, gnss, type_):
        """Reset GNSS receiver."""
        try:
            data = models.GNSS_RxReset(
                gnss=gnss, 
                type_=type_
            ).model_dump(by_alias=True)
        except ValidationError as error:
            return handle_validation_error(error)
        return self.client.api_request("/gnss/rx_reset", "POST", data)
