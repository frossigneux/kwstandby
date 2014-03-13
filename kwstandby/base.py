# -*- coding: utf-8 -*-
#
# Author: François Rossigneux <francois.rossigneux@inria.fr>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import ast
import subprocess

from oslo.config import cfg

from kwstandby.openstack.common import log

LOG = log.getLogger(__name__)

base_opts = [
    cfg.MultiStrOpt('ipmi_node',
                    required=True),
]

cfg.CONF.register_opts(base_opts)

ipmi_nodes = {}


def load_config():
    """Load the config."""
    for node in cfg.CONF.ipmi_node:
        node = ast.literal_eval(node)
        ipmi_nodes[node['host']] = dict((k, node[k]) for k in
                                        ('interface', 'username', 'password'))


def wake_up(node):
    """Wake up the node."""
    if node not in ipmi_nodes:
        LOG.error('Unknown node %s' % node)
        return False

    print "Wake up " + node
    ipmi_nodes[node]['status'] = "on"
    return True

    command = _get_base_command(node) + 'power on'
    child = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE
                             )
    output, error = child.communicate()
    if child.returncode == 0:
        LOG.info('Wake up %s' % node)
        return True
    else:
        LOG.error('Failed to wake up %s' % node)
        return False


def standby(node):
    """Put the node in standby mode."""
    if node not in ipmi_nodes:
        LOG.error('Unknown node %s' % node)
        return False

    print "Standby " + node
    ipmi_nodes[node]['status'] = "off"
    return True

    command = _get_base_command(node) + 'power soft'
    child = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE
                             )
    output, error = child.communicate()
    if child.returncode == 0:
        LOG.info('Wake up %s' % node)
        return True
    else:
        LOG.error('Failed to shutdown %s' % node)
        return False


def status(node):
    """Get the node status."""
    if node not in ipmi_nodes:
        LOG.error('Unknown node %s' % node)
        return False

    try:
        return ipmi_nodes[node]['status']
    except:
        return "Unknown"

    command = _get_base_command(node) + 'power status'
    child = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE
                             )
    output, error = child.communicate()
    if child.returncode == 0:
        LOG.info('Check %s status' % node)
        if 'is on' in output:
            status = 'on'
        else:
            status = 'off'
        return {'node': node, 'status': status}
    else:
        LOG.error('Failed to check %s status' % node)
        return {'node': node, 'status': 'unknown'}


def _get_base_command(node):
    command = 'ipmitool '
    command += '-I ' + ipmi_nodes[node]['interface'] + ' '
    command += '-H ' + node + ' '
    command += '-U ' + ipmi_nodes[node]['username'] + ' '
    command += '-P ' + ipmi_nodes[node]['password'] + ' '
    return command
