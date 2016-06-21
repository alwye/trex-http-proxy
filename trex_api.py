#!/usr/bin/python

# Copyright (c) 2016 Cisco and/or its affiliates.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script uses T-REX stateless API to drive t-rex instance.

Requirements:
- T-REX: https://github.com/cisco-system-traffic-generator/trex-core
 - compiled and running T-REX process (eg. ./t-rex-64 -i -c 4)
 - trex_stl_lib.api library
- Script must be executed on a node with T-REX instance
- 2 interfaces must be configured in configuretion file /etc/trex_cfg.yaml

##################### Example of /etc/trex_cfg.yaml ##########################
- port_limit      : 2 # numbers of ports to use
  version         : 2
  interfaces      : ["84:00.0","84:00.1"] # PCI address of interfaces
  port_info       :  # set eth mac addr
          - dest_mac        :   [0x90,0xe2,0xba,0x1f,0x97,0xd5]  # port 0
            src_mac         :   [0x90,0xe2,0xba,0x1f,0x97,0xd4]
          - dest_mac        :   [0x90,0xe2,0xba,0x1f,0x97,0xd4]  # port 1
            src_mac         :   [0x90,0xe2,0xba,0x1f,0x97,0xd5]
##############################################################################

Functionality:
1. Configure traffic on running T-REX instance
2. Clear statistics on all ports
3. Ctart traffic with specified duration
4. Print statistics to stdout

"""


import argparse
import json
import socket
import string
import struct
import sys
import pprint

sys.path.insert(0, "trex_client/stl/")
from trex_stl_lib.api import *

# create client
client = STLClient()


def create_stream(mac_dest, src_n, port_n=0):
    # create a base packet and pad it to size
    size = 60  # no FCS

    mac_src = "00:00:dd:dd:ae:11"
    base_pkt = Ether(dst=mac_dest, src=mac_src)/IP(src="10.195.115.232", dst="10.195.115.234")/UDP(dport=12,sport=1025)
    pad = max(0, size - len(base_pkt)) * 'x'

    min_mac_value = (src_n * port_n) + 1
    max_mac_value = min_mac_value + src_n

    print min_mac_value, max_mac_value

    vm = STLScVmRaw(
        [STLVmFlowVar(name="mac_src", min_value=min_mac_value, max_value=max_mac_value, size=2, op="inc"),
         STLVmWrFlowVar(fv_name="mac_src", pkt_offset=10)  # write it to LSB of SRC
         ]
        )

    return STLStream(packet=STLPktBuilder(pkt=base_pkt / pad, vm=vm),
                     mode=STLTXCont(pps=10))


def is_running():
    return client.is_connected()


# Get traffic generation session's details
def get_stats():
    if is_running():
        return client.get_stats()
    else:
        return {}


def start_traffic(pkts_n, duration, pps, mac_dest, src_n):
    """Run the traffic with specific parameters.

    :param pkts_n: Number of packets/ports
    :param duration: Duration of traffic run in seconds (-1=infinite).
    :param pps: Rate of traffic run [percentage, pps, bps].

    :type pkts_n: int
    :type duration: int
    :type pps: string

    :return: nothing
    """

    try:

        port_list = range(0, pkts_n)
        pprint.pprint(port_list)
        rate = str(pps) + "pps"

        # connect to server
        client.connect()

        # prepare our ports (my machine has 0 <--> 1 with static route)
        client.reset(ports=port_list)

        for idx in range(0, pkts_n):
            stream = create_stream(mac_dest=mac_dest,
                                   src_n=src_n,
                                   port_n=idx)
            client.add_streams(stream, ports=[idx])
            print "*** idx = ", idx

        # clear the stats before injecting
        client.clear_stats()
        total_rcvd = 0
        total_sent = 0
        lost_a = 0
        lost_b = 0

        # choose rate and start traffic
        client.start(ports=port_list, mult=rate, duration=duration)

    except STLError as ex_error:
        print_error(str(ex_error))
        sys.exit(1)


def stop_traffic():
    # graceful stop
    if client.is_connected():
        active_ports = client.get_active_ports()
        if len(active_ports) == 0:
            client.stop(client.get_active_ports())
        client.disconnect()


def print_error(msg):
    """Print error message on stderr.

    :param msg: Error message to print.
    :type msg: string
    :return: nothing
    """

    sys.stderr.write(msg+'\n')