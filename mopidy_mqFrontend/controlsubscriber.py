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
import paho.mqtt.client


class ControlSubscriber(pykka.ThreadingActor):

    config = None  # type: dict
    core = None  # type: mopidy.core.Core
    mosquitto_client = None  # type: paho.mqtt.client.Client

    def __init__(self, config, core, logger, *args, **kwargs):
        super(ControlSubscriber, self).__init__(*args, **kwargs)
        self.in_future = self.actor_ref.proxy()
        self.config = config
        self.core = core
        self.logger = logger

    def on_start(self):
        host = self.config['host']
        port = self.config['port']
        self.mosquitto_client = paho.mqtt.client.Client()
        self.mosquitto_client.on_connect = self.on_connect
        self.mosquitto_client.on_disconnect = self.on_disconnect
        self.mosquitto_client.on_message = self.on_mq_message

        self.logger.debug('Starting Control Client / Connecting on %s:%d' % (host, port))
        self.mosquitto_client.connect(host, port)

    def on_stop(self):
        self.logger.debug('Stopping Client - disabling reconnection')
        self.mosquitto_client.on_disconnect = None
        self.mosquitto_client.disconnect()
        self.logger.info('Client stopped')

    def on_connect(self):
        self.logger.info('Connected')
        topic = "{0}/{1}".format(self.config['topic'], 'control')
        self.logger.debug('Subscribing to {}'.format(topic))
        self.mosquitto_client.subscribe(topic)
        self.in_future.do_work()

    def on_disconnect(self):
        self.logger.info('DISConnected - Reconnecting...')
        self.mosquitto_client.reconnect()

    def on_mq_message(self, mqttc, obj, msg):
        self.logger.info('Received msg: {}' % msg.payload)
        if msg.payload == 'stop':
            self.core.playlist.stop()
            return
        if msg.payload == 'start':
            self.core.playlist.start()
            return
        if msg.payload == 'stop':
            self.core.playlist.stop()
            return

    def do_work(self):
        self.mosquitto_client.loop()
        self.in_future.do_work()
