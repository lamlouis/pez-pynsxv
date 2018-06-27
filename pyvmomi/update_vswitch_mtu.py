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

    parser.add_argument('-m', '--mtu',
                        type=int,
                        required=True,
                        action='store',
                        help='mtu')

    parser.add_argument('-v', '--vswitch',
                        required=True,
                        action='store',
                        help='vSwitch to create')

    args = parser.parse_args()
    return args


def GetVMHosts(content):
    host_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.HostSystem],
                                                        True)
    obj = [host for host in host_view.view]
    host_view.Destroy()
    return obj


def UpdateHostsSwitch(content, hosts, vswitchName, mtu):
    for host in hosts:
        UpdateHostSwitch(content, host, vswitchName, mtu)


def UpdateHostSwitch(content, host, vswitchName, mtu):
    for host in _get_vim_objects(content, vim.HostSystem):
      for vswitch in host.config.network.vswitch:
         if vswitch.name == vswitchName:
            vswitch_spec = vim.host.VirtualSwitch.Specification()
            vswitch_spec = vswitch.spec
            vswitch_spec.mtu = mtu
    host.configManager.networkSystem.UpdateVirtualSwitch(vswitchName, vswitch_spec)


def _get_vim_objects(content, vim_type):
    '''Get vim objects of a given type.'''
    return [item for item in content.viewManager.CreateContainerView(
        content.rootFolder, [vim_type], recursive=True
    ).view]



def main():
    args = get_args()
    serviceInstance = SmartConnectNoSSL(host=args.host,
                                   user=args.user,
                                   pwd=args.password,
                                   port=443)
    atexit.register(Disconnect, serviceInstance)
    content = serviceInstance.RetrieveContent()

    hosts = GetVMHosts(content)
    UpdateHostsSwitch(content, hosts, args.vswitch, args.mtu)


# Main section
if __name__ == "__main__":
    sys.exit(main())
