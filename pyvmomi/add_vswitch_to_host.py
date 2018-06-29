#!/usr/bin/env python
"""
Written by nickcooper-zhangtonghao
Github: https://github.com/nickcooper-zhangtonghao
Email: nickcooper-zhangtonghao@opencloud.tech
Note: Example code For testing purposes only
This code has been released under the terms of the Apache-2.0 license
http://opensource.org/licenses/Apache-2.0
"""
from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL
from pyVmomi import vim
import atexit
import sys
import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description='Arguments for talking to vCenter')

    parser.add_argument('-s', '--host',
                        required=True,
                        action='store',
                        help='vSpehre service to connect to')

    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='User name to use')

    parser.add_argument('-p', '--password',
                        required=True,
                        action='store',
                        help='Password to use')

    parser.add_argument('-v', '--vswitch',
                        required=True,
                        action='store',
                        help='vSwitch to create')

    parser.add_argument('--uplink1',
                        required=True,
                        action='store',
                        help='Uplink1')

    parser.add_argument('--uplink2',
                        required=True,
                        action='store',
                        help='Uplink2')

    args = parser.parse_args()
    return args


def GetVMHosts(content):
    host_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.HostSystem],
                                                        True)
    obj = [host for host in host_view.view]
    host_view.Destroy()
    return obj


def AddHostsSwitch(hosts, vswitchName, uplink1, uplink2):
    for host in hosts:
        AddHostSwitch(host, vswitchName, uplink1, uplink2)


def AddHostSwitch(host, vswitchName, uplink1, uplink2):
    vswitch_spec = vim.host.VirtualSwitch.Specification()
    vswitch_spec.numPorts = 64
    vswitch_spec.mtu = 1500
    vswitch_spec.bridge = vim.host.VirtualSwitch.BondBridge(nicDevice=[uplink1,uplink2])
    host.configManager.networkSystem.AddVirtualSwitch(vswitchName,
                                                      vswitch_spec)

def checkvSwitchExistence(hosts, vswitch):
    hostSwitchesDict = {}
    for host in hosts:
        switches = host.config.network.vswitch
        hostSwitchesDict[host] = switches

    for host, vswitches in hostSwitchesDict.items():
            for v in vswitches:
                if v.name == vswitch:
                    return True
    return False

def main():
    args = get_args()
    serviceInstance = SmartConnectNoSSL(host=args.host,
                                   user=args.user,
                                   pwd=args.password,
                                   port=443)
    atexit.register(Disconnect, serviceInstance)
    content = serviceInstance.RetrieveContent()

    hosts = GetVMHosts(content)


    if checkvSwitchExistence(hosts, args.vswitch):
        print(args.vswitch + ' already exists. Skipping')
    else:
        print('Creating ' + args.vswitch + '')
        AddHostsSwitch(hosts, args.vswitch, args.uplink1, args.uplink2)


# Main section
if __name__ == "__main__":
    sys.exit(main())
