"""
Purple Air Lib

Functions for interacting with the purple air sensor.

"""

# Base Python #
import logging


# Extended Python #
import requests

# CONSTANTS #
COLOR_CHANNEL_A = "p25aqic"
COLOR_CHANNEL_B = "p25aqic_b"
SENSOR_REQUEST_TEMPLATE = "http://{ip}/json?live={live}"

log_ = logging.getLogger(__name__)


def get_time(raw_time):
    """
    Get treated time value from the raw provided time.

    # 2020/09/05T05:21:48z
    # 2020-09-05T05:21:48z
    # dtr = dt.replace("/","-")[:-1]

    :param raw_time: <string>
    :return treated_time: <datetime>
    """

    treated_time = raw_time.replace("/", "-")

    return treated_time[:-1]


def get_rgb(raw_rgb):
    """
    Get the Red Green Blue values from the raw data.
    'rgb(255,0,0)'
    :param raw_rgb: <string>
    :return rgb: <tuple of ints>
    """

    log_.debug("Getting RGB")
    log_.debug("    from %s", raw_rgb)

    if not raw_rgb.startswith("rgb"):
        raise RuntimeError("Unable to parse raw RGB: {}".format(raw_rgb))

    treated_rgb = raw_rgb[4:-1]
    log_.debug("Treated RGB: %s", treated_rgb)

    split_rgb = treated_rgb.split(",")
    log_.debug("Split RGB: %s", split_rgb)

    rgb = tuple(int(v) for v in split_rgb)
    log_.debug("RGB: %s", rgb)

    return rgb


def get_average_color(first, second):
    """
    Combine two colors into one average
    :param first: <tuple>
    :param second: <tuple>

    :return average_color: <tuple>
    """

    log_.debug("Getting the average color.")
    log_.debug("   from: %s", first)
    log_.debug("   from: %s", second)

    stage = []

    for color_a, color_b in zip(first, second):

        add = color_a + color_b
        avg = add / 2
        final = int(avg)

        log_.debug("%d : %d = %d", color_a, color_b, final)

        stage.append(final)

    log_.debug("Average: %s", stage)

    return tuple(stage)


def get_sensor_data(ip_addr, live=True):
    """
    Get Sensor data from the source.
    :param ip_addr: <string>
    :param live: <bool> Live data or averaged over the past 10m or whatever
    :return raw_data: <dict>
    """

    log_.debug("Getting Sensor Data")
    log_.debug("   from: %s", ip_addr)
    log_.debug("   live: %s", live)

    treated_request = SENSOR_REQUEST_TEMPLATE.format(ip=ip_addr, live=live)

    log_.debug("Sending Request to: %s", treated_request)

    data = requests.get(treated_request)

    log_.debug("Got Data: %s", data)

    return data.json()


def get_sensor_color(ip_addr):
    """
    Get the sensor color from the Purple Air Sensor
    :param ip_addr: <string>
    :return color: <tuple> R, G, B
    """

    log_.info("Getting Sensor Color.")
    raw_data = get_sensor_data(ip_addr)

    channel_a = get_rgb(raw_data[COLOR_CHANNEL_A])
    channel_b = get_rgb(raw_data[COLOR_CHANNEL_B])

    average_color = get_average_color(channel_a, channel_b)

    return average_color
