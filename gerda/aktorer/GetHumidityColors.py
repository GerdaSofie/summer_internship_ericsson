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

class GetHumidityColors(Actor):
    """
    Converts humidity to RGB.

    Inputs:
      humidity : a value

    Outputs:
      red : a value
      green : a value
      blue : a value

    """
    def init(self):
        self.setup()

    def setup(self):
        self.use("calvinsys.math.gethumiditycolors", shorthand="gethumiditycolors")
        self.gethumiditycolors = self["gethumiditycolors"]

    def did_migrate(self):
        pass

    @condition(['humidity'], ['red','green', 'blue'])
    def compute(self, humidity):
        return self.gethumiditycolors.compute(humidity)

    action_priority = ( compute, )

    requires = ['calvinsys.math.gethumiditycolors']
