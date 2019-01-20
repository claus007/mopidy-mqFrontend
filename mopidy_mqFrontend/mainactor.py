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

from .controlsubscriber import ControlSubscriber
from .statuspublisher import StatusPublisher

import logging
import pykka


class MainActor(pykka.ThreadingActor):

    config = None  # type: dict
    status = None  # type: StatusPublisher
    control = None  # type: ControlSubscriber

    def __init__(self, config, core):
        super(MainActor, self).__init__()
        self.config = config
        self.core = core
        # import logger
        self.logger = logging.getLogger(__name__)

    def on_start(self, *args, **kwargs):
        self.logger.info('Starting MqFrontend')
        control = ControlSubscriber(self.config, self.core, self.logger.getChild('ControlSubscriber'))
        self.control = control.start(*args, **kwargs)
        status = StatusPublisher(self.config, self.core, self.logger.getChild('StatusPublisher'))
        self.status=status.start(*args, **kwargs)

    def on_stop(self):
        self.logger.debug('Stopping MqFrontend')
        self.control.stop()
        self.status.stop()
