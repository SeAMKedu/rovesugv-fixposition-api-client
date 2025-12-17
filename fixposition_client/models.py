from typing import List, Literal, Optional, Union
from typing_extensions import Self

from pydantic import BaseModel
from pydantic import Field, model_validator


#-----------------------------------------------------------------------------
# Exceptions
#-----------------------------------------------------------------------------
class APIException(BaseModel):
    """docstring."""
    ok: bool = Field(serialization_alias="_ok")
    message: str = Field(serialization_alias=("_message"))
    errors: Optional[list] = None


#-----------------------------------------------------------------------------
# Common
#-----------------------------------------------------------------------------
class ResetDefault(BaseModel):
    """Reset configuration to default."""
    reset: str = "default"


#----------------------------------------------------------------------
# Backup
#----------------------------------------------------------------------
class BackupSet(BaseModel):
    config: dict

#-----------------------------------------------------------------------------
# Camera
#-----------------------------------------------------------------------------
class CameraRecRm(BaseModel):
    files: List[str]

class CameraRecord(BaseModel):
    action: Literal["start", "stop", "status"]

class CameraRecDl(BaseModel):
    name: str


#----------------------------------------------------------------------
# Control
#----------------------------------------------------------------------
class ControlService(BaseModel):
    rtk: Optional[Literal["restart"]] = None
    camera: Optional[Literal["restart"]] = None
    fusion: Optional[Literal["start", "stop", "restart"]] = None
    websocket: Optional[Literal["restart"]] = None
    wheels: Optional[Literal["restart"]] = None
    io: Optional[Literal["reload"]] = None

class ControlSystem(BaseModel):
    system: Literal["reboot", "shutdown"]


#-----------------------------------------------------------------------------
# CAN Interface
#-----------------------------------------------------------------------------
class CANIfSet(BaseModel):
    """CAN interface configuration"""
    config_enabled: bool
    config_bitrate: Literal[
        10000, 20000, 50000, 125000, 250000, 500000, 800000, 1000000
    ]
    config_dbitrate: Literal[
        10000, 20000, 50000, 125000, 250000, 500000, 800000, 1000000
    ]

#----------------------------------------------------------------------
# Fusion
#----------------------------------------------------------------------
class FusionControl(BaseModel):
    action: Literal["status", "enable", "disable", "reset"]

class FusionData(BaseModel):
    stationary: Literal["", "remove"]
    warmstart: Literal["", "remove"]

class FusionPoseSave(BaseModel):
    action: str = "save"
    slot: int
    label: str

class FusionPoseLoad(BaseModel):
    action: str = "load"
    slot: int = Field(ge=0)

class FusionPoseDelete(BaseModel):
    action: str = "delete"
    slot: Union[int, Literal["*"]]

class FusionPoseGet(BaseModel):
    action: str = "get"

class FusionPoseSet(BaseModel):
    action: str = "set"
    states: List[dict]

#-----------------------------------------------------------------------------
# GNSS
#-----------------------------------------------------------------------------
class GNSS_RTKSet(BaseModel):
    """RTK correction stream parameters"""
    ntrip_user: str = Field(min_length=1)
    ntrip_pass: str = Field(min_length=1)
    ntrip_host: str = Field(min_length=1)
    ntrip_port: int = Field(ge=1, le=65535)
    ntrip_mount: str = Field(min_length=1)
    gga_mode: Literal["auto", "manual"]
    gga_lat: float = Field(ge=-90, le=90)
    gga_lon: float = Field(ge=-180, le=180)
    gga_height: float = Field(ge=-1000, le=10000)
    source: Literal["ntrip", "serial"]


class GNSS_RxReset(BaseModel):
    gnss: Literal[1, 2]
    type_: Literal["hot", "warm", "cold"] = Field(serialization_alias="type")

#----------------------------------------------------------------------
# Logging
#----------------------------------------------------------------------
class LogDisk(BaseModel):
    action: Literal["status", "mount", "umount"]
    disk: Optional[Literal["external"]] = None

    @model_validator(mode="after")
    def check_disk(self) -> Self:
        # disk is not required for 'status' action
        if self.action == "status" and not self.disk == None:
            self.disk = None
        # disk is required for 'mount' and 'umount' actions
        if self.action in ("mount", "umount") and self.disk == None:
            raise ValueError("disk='external' is required for 'mount' and 'umount'")
        return self

class LogLs(BaseModel):
    disk: str = "internal"

class LogDownload(BaseModel):
    disk: Literal["internal", "external"]
    name: str

class LogRm(BaseModel):
    disk: Literal["internal", "external"]
    files: List[str]

class LogStart(BaseModel):
    target: Literal["internal", "external", "download", "debuglog"]
    profile: Literal["minimal", "medium", "maximal", "calib", "debuglog"]

#-----------------------------------------------------------------------------
# Map
#-----------------------------------------------------------------------------
class MapTokenGet(BaseModel):
    which: str

class MapTokenSet(BaseModel):
    which: str
    token: str

class MapTokenReset(BaseModel):
    reset: str = "default"
    which: str


#-----------------------------------------------------------------------------
# Network
#-----------------------------------------------------------------------------
class NetworkConnection(BaseModel):
    connection: str

class NetworkConnSet(BaseModel):
    connection: str
    auto: Optional[bool] = None
    ip4addr: Optional[str] = None
    ip4gw: Optional[str] = None
    ip4dns: Optional[str] = None
    ip4method: Optional[Literal["auto", "manual", "shared"]] = None
    psk: Optional[str] = None
    keymgmt: Optional[str] = None
    ssid: Optional[str] = None

class WiFiAdd(BaseModel):
    ssid: str
    psk: str
    keymgmt: str
    auto: Optional[bool] = None
    ip4addr: Optional[str] = None
    ip4gw: Optional[str] = None
    ip4dns: Optional[str] = None
    ip4method: Optional[Literal["auto", "manual", "shared"]] = None

class WifiRemove(BaseModel):
    ssid: str

class WifiCfg(BaseModel):
    """Wi-Fi configuration."""
    action: Literal["get", "set", "reset"]
    config_band: Optional[Literal["a", "bg", "off"]] = None
    config_ap: Optional[bool] = None
    reset: Optional[str] = "default"

    @model_validator(mode="after")
    def check_combinations(self) -> Self:
        if self.action == "get":
            self.config_band = None
            self.config_ap = None
            self.reset = None
        elif self.action == "set":
            self.reset = None
            if self.config_ap == None and self.config_band == None:
                raise ValueError("'set' action requires either 'config_band' or 'config_ap'")
        elif self.action == "reset":
            self.config_band = None
            self.config_ap = None
            self.reset = "default"
        return self

#----------------------------------------------------------------------
# Params
#----------------------------------------------------------------------
class ParamsConfigSet(BaseModel):
    params: dict

#----------------------------------------------------------------------
# User data
#----------------------------------------------------------------------
class UserData(BaseModel):
    user_string: Optional[str] = None
    user_json: Optional[dict] = None

#----------------------------------------------------------------------
# Web interface
#----------------------------------------------------------------------
class WebPwSet(BaseModel):
    username: str = Field(min_length=4, max_length=100, serialization_alias="user")
    password: str = Field(min_length=4, max_length=100, serialization_alias="pass")
