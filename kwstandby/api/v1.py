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

"""This blueprint defines all URLs and answers."""

import os
import json

import flask

from kwstandby import base

blueprint = flask.Blueprint('v1', __name__)


@blueprint.route('/')
def welcome():
    """Returns detailed information about this specific version of the API."""
    return 'Welcome to Kwstandby!'


@blueprint.route('/status/')
def status():
    """List the nodes status."""
    nodes = {}
    for node in flask.request.nodes:
        nodes[node] = base.status(node)
    return flask.jsonify({'nodes_status': nodes})


@blueprint.route('/status/<node>/')
def detailed_status(node):
    """Get the node status."""
    if node in flask.request.nodes:
        return flask.jsonify({'nodes_status': {node: base.status(node)}})
    else:
        flask.abort(404)


@blueprint.route('/status/<node>/', methods=['PUT'])
def update_status(node):
    """Get or update the node status."""
    data = json.loads(flask.request.data)
    action = data.get('status', None)
    if action == 'wakeup':
        base.wake_up(node)
    elif action == 'standby':
        base.standby(node)
    return detailed_status(node)
