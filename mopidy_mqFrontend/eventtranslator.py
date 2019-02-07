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

import logging
import json

logger = logging.getLogger(__name__)


class EventTranslator:

    keepAliveSpeakers = None  # type: bool

    def __init__(self, core):
        self.core = core
        self.keepAliveSpeakers = False

    def translate(self, event, **kwargs):
        """
        Called on all events.

        *MAY* be implemented by actor. By default, this method forwards the
        event to the specific event methods.

        :param event: the event name
        :type event: string
        :param kwargs: any other arguments to the specific event handlers
        """
        try:
            return getattr(self, event)(**kwargs)
        except Exception:
            # Ensure we don't crash the actor due to "bad" events.
            logger.exception(
                'Triggering event failed: %s(%s)', event, ', '.join(kwargs))

    def track_playback_paused(self, tl_track, time_position):
        """
        Called whenever track playback is paused.

        *MAY* be implemented by actor.

        :param tl_track: the track that was playing when playback paused
        :type tl_track: :class:`mopidy.models.TlTrack`
        :param time_position: the time position in milliseconds
        :type time_position: int
        """
        result = [('state', 'paused')] # , ('time_position', time_position)]

        return result

    def track_playback_resumed(self, tl_track, time_position):
        """
        Called whenever track playback is resumed.

        *MAY* be implemented by actor.

        :param tl_track: the track that was playing when playback resumed
        :type tl_track: :class:`mopidy.models.TlTrack`
        :param time_position: the time position in milliseconds
        :type time_position: int
        """
        result = [('state', 'playing')] # , ('time_position', time_position)]

        return result

    def track_playback_started(self, tl_track):
        """
        Called whenever a new track starts playing.

        *MAY* be implemented by actor.

        :param tl_track: the track that just started playing
        :type tl_track: :class:`mopidy.models.TlTrack`
        """
        result = [('state', 'playing'),
                  ('track_name', tl_track.track.name),
                  ('track_genre', tl_track.track.genre)
                  ]  # , ('time_position', 0)]

        return result

    def track_playback_ended(self, tl_track, time_position):
        """
        Called whenever playback of a track ends.

        *MAY* be implemented by actor.

        :param tl_track: the track that was played before playback stopped
        :type tl_track: :class:`mopidy.models.TlTrack`
        :param time_position: the time position in milliseconds
        :type time_position: int
        """
        result = [('state', 'stopped')] #, ('time_position', time_position)]

        return result

    def playback_state_changed(self, old_state, new_state):
        """
        Called whenever playback state is changed.

        *MAY* be implemented by actor.

        :param old_state: the state before the change
        :type old_state: string from :class:`mopidy.core.PlaybackState` field
        :param new_state: the state after the change
        :type new_state: string from :class:`mopidy.core.PlaybackState` field
        """
        result = [('playback_state', new_state)]

        self.keepAliveSpeakers = new_state == 'playing'

        if new_state != 'playing':
            result.append(('track_name',''))
            result.append(('stream_title',''))

        return result

    def tracklist_changed(self):
        """
        Called whenever the tracklist is changed.

        *MAY* be implemented by actor.
        """
        pass

    def get_playlist_update(self):
        result = {}
        playlists = self.core.playlists.as_list()
        for playlist in playlists.get():
            result[playlist.name]= playlist.uri

        return [("playlists", json.dumps(result))]


    def playlists_loaded(self):
        """
        Called when playlists are loaded or refreshed.

        *MAY* be implemented by actor.
        """
        return self.get_playlist_update()

    def playlist_changed(self, playlist):
        """
        Called whenever a playlist is changed.

        *MAY* be implemented by actor.

        :param playlist: the changed playlist
        :type playlist: :class:`mopidy.models.Playlist`
        """
        return self.get_playlist_update()

    def playlist_deleted(self, uri):
        """
        Called whenever a playlist is deleted.

        *MAY* be implemented by actor.

        :param uri: the URI of the deleted playlist
        :type uri: string
        """
        return self.get_playlist_update()

    def options_changed(self):
        """
        Called whenever an option is changed.

        *MAY* be implemented by actor.
        """
        pass

    def volume_changed(self, volume):
        """
        Called whenever the volume is changed.

        *MAY* be implemented by actor.

        :param volume: the new volume in the range [0..100]
        :type volume: int
        """
        result = [('volume', volume)]

        return result

    def mute_changed(self, mute):
        """
        Called whenever the mute state is changed.

        *MAY* be implemented by actor.

        :param mute: the new mute state
        :type mute: boolean
        """
        result = [('mute', mute)]

        return result

    def seeked(self, time_position):
        """
        Called whenever the time position changes by an unexpected amount, e.g.
        at seek to a new time position.

        *MAY* be implemented by actor.

        :param time_position: the position that was seeked to in milliseconds
        :type time_position: int
        """
        pass

    def stream_title_changed(self, title):
        """
        Called whenever the currently playing stream title changes.

        *MAY* be implemented by actor.

        :param title: the new stream title
        :type title: string
        """
        result = [('stream_title', title)]

        return result
