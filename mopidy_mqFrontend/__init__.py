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
import os

from mopidy import config, ext
from mopidy_mqFrontend.configdefinition import get_config_definition

__version__ = '0.99'

# If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)


class Extension(ext.Extension):
    """ this is just the extension class 
    look for MainActor.
    I have to admit this is a little confusing 
    The way is setup.py --> __init__.py --> Extension --> MainActor
    """
    dist_name = 'mopidy-mqFrontend'
    ext_name = 'mqfrontend'
    version = __version__

    def get_default_config(self):
        result = '''
#this file is automatically created once
# please seee configdefintition file
# or https://github.com/claus007/mopidy-mqFrontend/blob/master/mopidy_mqFrontend/configdefinition.py
# for more info

[mqfrontend]
enabled=True
'''
        conf_definition = get_config_definition()
        for item in conf_definition:
            result = result + '\n# '
            result = result + item[3]
            result = result + ("\n%s=%s\n" % (item[0], item[2]))
        return result

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        conf_definition = get_config_definition()
        for item in conf_definition:
            schema[item[0]] = item[1]
        return schema

    def get_command(self):
        pass

    def validate_environment(self):
        # Any manual checks of the environment to fail early.
        # Dependencies described by setup.py are checked by Mopidy, so you
        # should not check their presence here.
        pass

    def setup(self, registry):
        # You will typically only do one of the following things in a
        # single extension.

        # Register a frontend
        from .mainactor import MainActor
        registry.add('frontend', MainActor)

        # Or nothing to register e.g. command extension
        pass
