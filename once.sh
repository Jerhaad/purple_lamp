#!/bin/bash
#

# Constants
PURPLE=192.168.42.47
OPENHAB_IP=10.0.10.138
OPENHAB_PORT=8080
LAMP_THING_BASE=amazonechocontrol_smartHomeDevice_8dfb0191_1c497908_dad4_46b1_a64a_33d603ec5b1e

# Set up venv
script_dir=`dirname $0`
cd $script_dir
. bin/activate

python cli.py --purple $PURPLE --openhab_ip $OPENHAB_IP --openhab_port $OPENHAB_PORT --lamp_thing_base $LAMP_THING_BASE --once
