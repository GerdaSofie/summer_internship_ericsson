# -*- coding: utf-8 -*-

# Copyright (c) 2015 Ericsson AB
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

from calvin.actor.actor import Actor, manage, condition
from calvin.utilities.calvinlogger import get_actor_logger

_log = get_actor_logger(__name__)

class RGBtoHSL(Actor):
    """
    Converts inputs of RGB to HSL.

    Inputs:
      red : a value
      green : a value
      blue : a value

    Outputs:
      hue : The hue
      saturation : The saturation
      brightness : The brightness

    """
    def init(self):
        self.setup()

    def setup(self):
        self.use("calvinsys.math.rgbtohsl", shorthand="rgbtohsl")
        self.rgbtohsl = self["rgbtohsl"]

    def did_migrate(self):
        pass

    @condition(['red', 'green', 'blue'], ['hue','saturation', 'brightness'])
    def compute(self, red, green , blue):
        return self.rgbtohsl.compute(red,green,blue)

    action_priority = ( compute, )

    requires = ['calvinsys.math.rgbtohsl']
