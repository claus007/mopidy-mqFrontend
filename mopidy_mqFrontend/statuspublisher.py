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

from mopidy_mqFrontend.mosquittoclientbase import MosquittoClientBase
from .eventtranslator import EventTranslator
from .keepalive import KeepAlive


class StatusPublisher(MosquittoClientBase, CoreListener):
    event_translator = None  # type: EventTranslator
    keep_alive = None

    def __init__(self):
        super(StatusPublisher, self).__init__()
        self.keep_alive = KeepAlive(self.config['speaker_keep_alive_interval'], self.send_keep_alive)
        self.keep_alive.start()

    def on_connected(self):
        super(StatusPublisher, self).on_connected()
        self.event_translator = EventTranslator(self.core)
        self.mosquitto_client.publish(self.get_topic('status'), 'connected', 0, True)

        messages = self.event_translator.get_playlist_update()
        for message in messages:
            self.mosquitto_client.publish(self.get_topic(message[0]), message[1])

    def on_event(self, event, **kwargs):
        self.logger.debug('Event: {}'.format(event))
        messages = self.event_translator.translate(event, **kwargs)
        self.keep_alive.active = self.event_translator.keepAliveSpeakers
        if not messages:
            return
        for message in messages:
            self.mosquitto_client.publish(self.get_topic(message[0]), message[1])

    def send_keep_alive(self):
        self.mosquitto_client.publish(self.config['speaker_keep_alive_topic'],
                                      self.config['speaker_keep_alive_payload'])

    def on_stop(self):
        super(StatusPublisher, self).on_stop()
        self.keep_alive.stop()
