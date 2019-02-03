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

from threading import Thread
import time

class KeepAlive(Thread):
    running = False
    call_every = 60
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
            self.time = 0

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
        self.join()

