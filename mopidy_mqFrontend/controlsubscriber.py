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

from mopidy_mqFrontend.statuspublisher import StatusPublisher


class ControlSubscriber(StatusPublisher):

    def __init__(self):
        super(ControlSubscriber, self).__init__()

    def on_connected(self):
        super(ControlSubscriber, self).on_connected()
        topic = "{0}/{1}".format(self.config['topic'], 'control')
        self.logger.debug('Subscribing to {}'.format(topic))
        (result, mid) = self.mosquitto_client.subscribe(topic, 2)
        if result == paho.mqtt.client.MQTT_ERR_SUCCESS:
            self.logger.info('Subscribed !')
        else:
            self.logger.error('Not subscribed ErrorCode({})'.format(result))
        self.mosquitto_client.message_callback_add(topic, self.on_mq_control_message)

    def on_mq_control_message(self, mqttc, obj, msg):
        self.logger.info('Received msg: %s' % msg.payload)
        command = str(msg.payload)
        if command == 'stop':
            self.core.playback.stop()
            return
        if command == 'start':
            self.core.playback.start()
            return
        if command == 'pause':
            self.core.playback.pause()
            return
        if command == 'next':
            self.core.playback.next()
            return
        if command.startswith('prev'):
            self.core.playback.previous()
            return
        if command == 'resume':
            self.core.playback.resume()
            return
        if command == 'mute':
            self.core.mixer.set_mute(True)
            return
        if command == 'unmute':
            self.core.mixer.set_mute(False)
            return
        if command.startswith('volume'):
            c = command.split('=')
            if len(c) == 1:
                self.logger.error('Volume format error')
                return
            if c == '+':
                self.core.mixer.set_volume(self.core.mixer.get_volume() + 10)
                return
            if c == '-':
                self.core.mixer.set_volume(self.core.mixer.get_volume() - 10)
                return
            try:
                volume = int(c[1])
            except (ValueError, TypeError):
                self.logger.error('Volume no number')
            self.core.mixer.set_volume(volume)
            return
        if command.startswith('play_now'):
            c = command.split('=')
            if len(c) == 1:
                self.logger.error('uri missing')
                return
            uri = c[1]
            self.core.tracklist.clear()
            self.core.tracklist.add(uri=uri)
            self.core.playback.play()
            return
        if command == 'send_playists_update':
            messages = self.on_event(u'playlists_loaded', None)
            return
