"""
Purple Lamp Runner

"""

# Base Python #
import logging
import sys
import time

from argparse import ArgumentParser


# Purple Python #
from color_treatment import get_color_name
from openhab_lib import OpenHABServer

from purple import get_sensor_color

# Constants #
DEFAULT_INTERVAL_S = 120


def get_parser():
    arg_parser = ArgumentParser(description="Purple Lamp Runner.")

    arg_parser.add_argument(
        "--purple", type=str, required=True, help="IP Address of the Purple Air Sensor"
    )

    arg_parser.add_argument(
        "--openhab_ip", type=str, required=True, help="IP Address of the OpenHAB Sever"
    )

    arg_parser.add_argument(
        "--openhab_port", type=str, required=True, help="Port of the OpenHAB Sever"
    )

    arg_parser.add_argument(
        "--lamp_thing_base",
        type=str,
        required=True,
        help="Lamp Thing Base string from OpenHAB",
    )

    arg_parser.add_argument(
        "-t",
        "--time_interval",
        type=int,
        help="Time between updates.",
        default=DEFAULT_INTERVAL_S,
    )

    return arg_parser


def parse_args(*args):

    parser = get_parser()
    if not args:
        args = sys.argv[1:]

    return parser.parse_args(args)


def setup_openhab(ip_addr, port, light_base):
    """
    :param ip_addr: <string>
    :param port: <number>
    :param light_base: <string> base code for OpenHAB Thing that all of its items share.
    :return openhab_server: <?>
    """

    openhab = OpenHABServer(ip_addr, port, light_base)

    return openhab


def run():
    """
    Go!
    """

    # Logger
    # TODO: Move this to INFO
    log = logging.getLogger()
    fmt = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    strm = logging.StreamHandler()
    strm.setLevel(logging.DEBUG)
    strm.setFormatter(fmt)
    log.addHandler(strm)
    log.setLevel(logging.DEBUG)

    # Args
    args = parse_args()

    # Go time
    log.info("Setting up OpenHAB Server.")
    openhab = setup_openhab(args.openhab_ip, args.openhab_port, args.lamp_thing_base)
    openhab.open()

    while True:
        log.info("Getting Sensor Color")
        rgb = get_sensor_color(args.purple)
        log.debug("Got %s.", rgb)

        log.info("Getting Color Name")
        color = get_color_name(rgb)

        log.info("Setting new Color: %s", color)
        openhab.change_light_color(color)

        time.sleep(args.time_interval)


if __name__ == "__main__":
    run()
