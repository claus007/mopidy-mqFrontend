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

import paho.mqtt.client
import pykka


class MosquittoClientBase(pykka.ThreadingActor):
    config = None  # type: dict
    core = None  # type: mopidy.core.Core
    mosquitto_client = None  # type: paho.mqtt.client.Client
    logger = None

    def __init__(self):
        super(MosquittoClientBase, self).__init__()
        self.in_future = self.actor_ref.proxy()

    def on_start(self):
        host = self.config['host']
        port = self.config['port']
        self.mosquitto_client = paho.mqtt.client.Client('Mopidy_Interface')
        self.mosquitto_client.on_connect = self.on_connect
        self.mosquitto_client.on_disconnect = self.on_disconnect
        self.mosquitto_client.on_message = self.on_mq_message

        self.logger.debug('Starting Control Client / Connecting on %s:%d' % (host, port))
        self.mosquitto_client.connect(host, port)
        self.mosquitto_client.loop_start()

    def on_stop(self):
        self.logger.debug('Stopping Client - disabling reconnection')
        self.mosquitto_client.on_disconnect = None
        self.mosquitto_client.disconnect()
        self.mosquitto_client.loop_stop()
        self.logger.info('Client stopped')

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info('Connected')
            self.on_connected()
        else:
            self.logger.error('Connection refused')
            time.sleep(5)
            self.logger.info('Trying to connect again...')
            self.mosquitto_client.reconnect()

    def on_disconnect(self):
        self.logger.error('DISConnected - Reconnecting...')
        self.mosquitto_client.reconnect()

    def on_connected(self):
        pass

    def on_mq_message(self, mqttc, obj, msg):
        pass

    def get_topic(self, sub_topic):
        return "{}/{}".format(self.config['topic'], sub_topic)
