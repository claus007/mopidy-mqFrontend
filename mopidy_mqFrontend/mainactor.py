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


class MainActor(ControlSubscriber):

    def __init__(self, config, core):
        logger = logging.getLogger(__name__)
        super(MainActor, self).__init__(self,config[u'mqfrontend'],core,logger)
        self.logger.debug("Config: %s" % self.config)

    def on_start(self):
        self.logger.info('Starting MqFrontend')

    def on_stop(self):
        self.logger.debug('Stopping MqFrontend...')

    def on_failure(self, exception_type, exception_value, traceback):
        self.on_stop()