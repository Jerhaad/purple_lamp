"""
Wrapper Lib for interacting with local OpenHAB
https://python-openhab.readthedocs.io/en/latest/?badge=latest
"""

# Base Python #
import logging

# Extended Python #
from openhab import OpenHAB


# Constants #
SERVER_FORMAT = "http://{ip_addr}:{port}/rest".format
COLOR_NAME_ATTR = "colorName"
POWER_STATE_ATTR = "powerState"

log_ = logging.getLogger(__name__)


class OpenHABServer:
    """Get a handle to the OpenHAB Server"""

    def __init__(self, ip_addr, port, light_base):
        """
        :param ip_addr: <string>
        :param port: <number>
        :param light_base: <string> base code for OpenHAB Thing that all of its items share.  # TODO: Trim out the obv
        """

        self._raw_base = light_base
        self._openhab = None
        self._is_open = None
        self._light_base = _base_transform(light_base)
        self._light_color_name = self._light_base + COLOR_NAME_ATTR
        self._light_power_state = self._light_base + POWER_STATE_ATTR

        self.color_name_item = None
        self.ip_addr = ip_addr
        self.port = port

    def __enter__(self):
        """
        Dunder for context management open
        :return self:
        """

        self.open()

        return self

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        """
        Dunder for context management close
        """

        self.close(exc_type, exc_value, traceback)

    def open(self):
        """
        Open the connection.
        # TODO: Not sure how long it can stay open yet.
        """

        if self._is_open:
            log_.warning("Already Open!")
        else:
            log_.info("Opening connection to the OpenHAB Server.")
            log_.debug("    at %s:%s", self.ip_addr, self.port)

            server_path = SERVER_FORMAT(ip_addr=self.ip_addr, port=self.port)

            self._openhab = OpenHAB(server_path)
            self.color_name_item = self._openhab.get_item(self._light_color_name)
            self.power_state_item = self._openhab.get_item(self._light_power_state)
            self._is_open = True

    def close(self, exc_type=None, exc_value=None, traceback=None):
        """
        Close the connection down.
        """

        if self._is_open:
            log_.debug("Closing connection to the OpenHAB Server")
            self._is_open = False
        else:
            log_.warning("Already Closed!")

        if exc_type:
            log_.error(
                "Passing exception data: %s, %s, %s.", exc_type, exc_value, traceback
            )

    def change_light_color(self, color):
        """
        Post an update to the light.
        :param color: <string>
        """

        # TODO: Hysteresis?  Do we need this?
        log_.info("Posting update to Light")
        log_.debug("   color: %s", color)

        self.color_name_item.command(color)

    def get_lamp_status(self):
        """
        Check the lamp's current ON/OFF status
        :return lamp_is_on: <bool>
        """

        log._debug("Checking Lamp Status")

        lamp_is_on = self.power_state_item.state == "ON"
        return lamp_is_on


def _base_transform(raw):
    """
    OpenHAB's Thing format needs to be transformed for the python API to get Items:
      : -> _
      - -> _
    :param raw: <string>
    :return treated: <string>
    """

    log_.debug("Transforming Raw Thing Base.")
    log_.debug("    raw: %s", raw)

    if not raw.endswith(":"):
        raw = raw + ":"

    treated = raw.replace(":", "_").replace("-", "_")

    log_.debug("Sending back treated: %s", treated)

    return treated
