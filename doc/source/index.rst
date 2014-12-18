..
      Copyright 2013 François Rossigneux (Inria)

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

=======================
Kwstandby documentation
=======================

Kwstandby provides a REST API to shutdown and wake up the hosts using their IPMI cards.
This documentation offers information on how Kwstandby works.

==========
Installing
==========

Installing Kwstandby
====================

1. Clone the Kwstandby git repository to the management server::

   $ git clone https://github.com/frossigneux/kwstandby

2. As a user with ``root`` permissions or ``sudo`` privileges, run the
   Kwstandby installer and copy the configuration files::

   $ pip install kwstandby
   $ cp -r kwstandby/etc/kwstandby /etc/

Running Kwstandby service
=========================

   Start the Kwstandby API::

   $ kwstandby-api

=====================
Configuration Options
=====================

The following table lists the Kwstandby options in the configuration file.
Please note that Kwstandby uses openstack-common extensively,
which requires that the other parameters are set appropriately.

=============  =============================================================================================  =========================
Parameter      Default                                                                                        Note
=============  =============================================================================================  =========================
api_port       5002                                                                                           API port
acl_enabled    true                                                                                           Keystone authentication
policy_file    /etc/kwstandby/policy.json                                                                     Access rules
log_file       /var/log/kwstandby.log                                                                         Log file
ipmi_node      ``{'interface':'lanplus', 'host':'192.168.0.2', 'username':'user1', 'password':'secret1'}``    IPMI card information
=============  =============================================================================================  =========================

The config file contains also a section dedicated to Keystone authentication.

===================  ===========  ===============
Parameter            Default      Note
===================  ===========  ===============
auth_node            localhost    Auth node
auth_protocol        http         Auth protocol
admin_user           kwstandby    Admin
admin_password       password     Password
admin_tenant_name    service      Tenant name
===================  ===========  ===============

A sample configuration file can be found in `kwstandby.conf`_.

.. _kwstandby.conf: https://github.com/frossigneux/kwstandby/blob/master/etc/kwstandby/kwstandby.conf

API
===

====    ===========================     ============================================   ================================================
Verb    URL	                            Parameters	                                   Expected result
====    ===========================     ============================================   ================================================
GET     /v1/status/                                                                    Returns all hosts status
GET     /v1/status/<host>/              host                                           Returns the host status
PUT     /v1/status/<host>/              host, ``{"status": "standby" or "wakeup"}``    Update the host status
====    ===========================     ============================================   ================================================

=======================
Project Hosting Details
=======================

:Code Hosting: https://github.com/frossigneux/kwstandby
