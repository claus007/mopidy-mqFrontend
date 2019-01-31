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

from mopidy.core.listener import CoreListener
from threading import Thread
import time

from mopidy_mqFrontend.mosquittoclientbase import MosquittoClientBase
from .eventtranslator import EventTranslator


class KeepAlive(Thread):
    running = False
    call_every = 6000
    time = 0
    func = None
    __active = False

    def __init__(self, interval, func):
        super(KeepAlive, self).__init__()
        self.call_every = interval
        self.func = func

    @property
    def active(self):
        """ activated """
        return self.__active

    @active.setter
    def active(self, state):
        self.__active = state
        if state:
            self.func()

    def run(self):
        self.time = 0
        self.running = True
        while self.running:
            time.sleep(1)
            self.time = self.time + 1
            if self.time > self.call_every:
                self.time = self.time - self.call_every
                if self.__active:
                    self.func()

    def stop(self):
        self.running = False


class StatusPublisher(MosquittoClientBase, CoreListener):
    SPEAKERS_KEEPALIVE_TIMEOUT = 30  # type: int
    event_translator = None  # type: EventTranslator
    keep_alive = None

    def __init__(self):
        super(StatusPublisher, self).__init__()
        self.keep_alive = KeepAlive(30, self.send_keep_alive)
        self.keep_alive.start()

    def on_connected(self):
        super(StatusPublisher, self).on_connected()
        self.event_translator = EventTranslator()
        self.mosquitto_client.publish(self.get_topic('status'), 'connected')

    def on_event(self, event, **kwargs):
        self.logger.debug('Event: {}'.format(event))
        messages = self.event_translator.translate(event, **kwargs)
        self.keep_alive.active = self.event_translator.keepAliveSpeakers
        if not messages:
            return
        for message in messages:
            self.mosquitto_client.publish(self.get_topic(message[0]), message[1])

    def send_keep_alive(self):
        self.mosquitto_client.publish(self.get_topic("speakers_needed"), True)

    def on_stop(self):
        super(StatusPublisher, self).on_stop()
        self.keep_alive.stop()
