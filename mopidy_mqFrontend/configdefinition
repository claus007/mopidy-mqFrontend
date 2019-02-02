# Copyright 2019 Claus Ilginnis <claus@ilginnis.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, unicode_literals

from mopidy import config


def get_config_definition():
    config_definition = [['topic', config.String(True), 'mopidy', 'Mosquitto Main topic'],
                         ['client_id', config.String(True), 'mopidy-mqFrontend', 'Client Id as shown in Mosquitto'],
                         ['host', config.Hostname(True), 'localhost', 'Mosquitto host'],
                         ['port', config.Port(optional=True), 1883, 'Mosquitto port'],
                         ['keepAlive', config.Integer(optional=True), 60, 'Keep alive for Mosquitto protocol'],
                         ['reconnect_after', config.Integer(optional=True), 15,
                          'If connect lost reconnect after X seconds'],
                         ['username', config.String(True), None, 'User name if needed'],
                         ['password', config.Secret(True), None, 'Password if needed'],
                         ['speaker_keep_alive_interval', config.Integer(optional=True), 30, 'Keep alive for interval '
                                                                                            'for speakers - zero to '
                                                                                            'disable'],
                         ['speaker_keep_alive_topic', config.String(True), 'mopidy/speakers_needed', 'Topic to send '
                                                                                                     'keep speakers '
                                                                                                     'alive'],
                         ['speaker_keep_alive_payload', config.String(True), True, 'payload of speakers keep alive '
                                                                                   'message']]

    return config_definition
