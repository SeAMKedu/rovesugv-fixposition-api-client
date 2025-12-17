from fixposition_client.apis.api import API
from fixposition_client.apis.backup_api import BackupAPI
from fixposition_client.apis.camera_api import CameraAPI
from fixposition_client.apis.can_api import CANInterfaceAPI
from fixposition_client.apis.control_api import ControlAPI
from fixposition_client.apis.fusion_api import FusionAPI
from fixposition_client.apis.gnss_api import GNSS_API
from fixposition_client.apis.log_api import LoggingAPI
from fixposition_client.apis.map_api import MapAPI
from fixposition_client.apis.misc_api import MiscAPI
from fixposition_client.apis.netword_api import NetworkAPI
from fixposition_client.apis.params_api import ParamsAPI
from fixposition_client.apis.record_api import RecordAPI
from fixposition_client.apis.system_api import SystemInfoAPI
from fixposition_client.apis.web_api import WebAPI


# TODO: ControlAPI() -> action(): add services
# TODO: LoggingAPI() -> dl(): get filename of downloaded file


class Fixposition:
    """Fixposition API"""

    def __init__(self, host: str, debug: bool = False) -> None:
        self.host = host
        self.debug = debug
        self.api = API(self.host)
        self.backup = BackupAPI(self.host)
        self.camera = CameraAPI(self.host)
        self.can = CANInterfaceAPI(self.host)
        self.ctrl = ControlAPI(self.host)
        self.fusion = FusionAPI(self.host)
        self.gnss = GNSS_API(self.host)
        self.log = LoggingAPI(self.host)
        self.map = MapAPI(self.host)
        self.misc = MiscAPI(self.host)
        self.net = NetworkAPI(self.host)
        self.params = ParamsAPI(self.host)
        self.record = RecordAPI(self.host)
        self.sys = SystemInfoAPI(self.host)
        self.web = WebAPI(self.host)
