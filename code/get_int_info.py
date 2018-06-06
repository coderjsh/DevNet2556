#!/usr/bin/env python
#
from ncclient import manager
import sys
import xml.dom.minidom as DOM

# the variables below assume the user is leveraging a
# Vagrant Image running IOS-XE 16.7 on local device
HOST = '192.168.35.1'
# use the NETCONF port for your IOS-XE
PORT = 830
# use the user credentials for your IOS-XE
USER = 'vagrant'
PASS = 'vagrant'
# YANG filter
NS = """
    <filter>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface></interface>
        </native>
    </filter>
    """


class IntInfo():
    def __init__(self, name, description):
        self.name = name
        self.description = description


def connect(xml_filter):
    """
    Open connection using IOS-XE Native Filter
    """
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:

        return(m.get_config('running', xml_filter))


def get_int_info(int):
    name_obj = int.getElementsByTagName("name")[0]
    name = name_obj.firstChild.nodeValue

    if len(int.getElementsByTagName("description")) != 1:
        description = "empty"
    else:
        description_obj = int.getElementsByTagName("description")[0]
        description = description_obj.firstChild.nodeValue

    return IntInfo(name, description)


def main():
    interfaces = connect(NS)

    doc = DOM.parseString(interfaces.xml)
    node = doc.documentElement

    gigs = doc.getElementsByTagName("GigabitEthernet")
    for GE in gigs:
        ints = get_int_info(GE)
        print("GigabitEthernet%s, description: %s" % (ints.name, ints.description))

    loops = doc.getElementsByTagName("Loopback")
    for LO in loops:
        ints = get_int_info(LO)
        print("Loopback%s,        description: %s" % (ints.name, ints.description))


if __name__ == '__main__':
    sys.exit(main())