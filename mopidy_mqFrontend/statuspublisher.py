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
from mopidy.core.listener import CoreListener
import paho.mqtt.client as mqtt
from .eventtranslator import EventTranslator
import time


class StatusPublisher(pykka.ThreadingActor, CoreListener):
    MOSQUITTO_TIMEOUT = 5.0  # type: float
    MOSQUITTO_MAX_MSGS = 5  # type: int
    SPEAKERS_KEEPALIVE_TIMEOUT = 30  # type: int
    config = None  # type: dict
    core = None  # type: mopidy.core.Core
    mosquitto_client = None  # type: mqtt.Client
    event_translator = None  # type: EventTranslator
    keep_alive_pause = 0  # type: int

    def __init__(self, config, core, logger, *args, **kwargs):
        super(StatusPublisher, self).__init__(*args, **kwargs)
        self.in_future = self.actor_ref.proxy()
        self.config = config
        self.core = core
        self.logger = logger

    def on_start(self):
        host = self.config['host']
        port = self.config['port']
        self.mosquitto_client = paho.mqtt.client.Client()
        self.event_translator = EventTranslator()
        self.mosquitto_client.on_connect = self.on_connect
        self.mosquitto_client.on_disconnect = self.on_disconnect

        self.mosquitto_client.will_set(self.get_topic('status'), 'disconnected', 0, True)

        self.logger.debug('Starting Control Client / Connecting on %s:%d' % (host, port))
        self.mosquitto_client.connect(host, port)
        self.in_future.do_work()
        self.mosquitto_client.publish(self.get_topic('status'), 'connected')

    def on_stop(self):
        self.logger.debug('Stopping Client - disabling reconnection')
        self.mosquitto_client.on_disconnect = None
        self.mosquitto_client.disconnect()
        self.logger.debug('Client stopped')

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info('Connected')
            # needed for keep alive
            self.in_future.do_work()
        else:
            self.logger.error('connection refused')
            time.sleep(5)
            self.logger.info('trying to connect again')
            self.mosquitto_client.reconnect()

    def on_disconnect(self):
        self.logger.error('DISConnected - Reconnecting...')
        self.mosquitto_client.reconnect()

    def on_event(self, event, **kwargs):
        self.logger.debug('Event: {}'.format(event))
        messages =self.event_translator.translate(event, **kwargs)
        if not messages:
            return
        for message in messages:
            self.mosquitto_client.publish(self.get_topic(message[0]), message[1])

    def get_topic(self, sub_topic):
        return "{}/{}".format(self.config['topic'], sub_topic)

    def do_work(self):
        self.mosquitto_client.loop(self.MOSQUITTO_TIMEOUT, self.MOSQUITTO_MAX_MSGS)
        self.keep_alive_pause = self.keep_alive_pause + self.MOSQUITTO_TIMEOUT

        if self.keep_alive_pause > self.SPEAKERS_KEEPALIVE_TIMEOUT:
            self.keep_alive_pause = 0
            if self.event_translator.keepAliveSpeakers:
                self.mosquitto_client.publish(self.get_topic('speakers_needed'), "True")

        self.in_future.do_work()
