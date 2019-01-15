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

import pykka
import mopidy
import paho.mqtt.client as mqtt

import logging


class ControlSubscriber(pykka.ThreadingActor):

    def __init__(self, config, core, logger):
        self.config = config
        self.core = core
        self.logger = logger
        self.mqtt_client = mqtt()

    def on_start(self):
        host = self.config["host"]
        port = self.config["port"]
        self.logger.info("Starting Control Client / Connecting on %s:%d" % (host, port))
        self.mqtt_client.connect(host, port)

    def on_stop(self):
        self.logger.info("Stopping Control Client")
