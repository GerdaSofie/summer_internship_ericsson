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


class PersonCounter(Actor):
    """
    Counts people in differrent rooms
    Inputs:
      room : which room the person walked in or out.
      id : who walked in or out.
    Outputs:
      rooms : dictionary of people in rooms.
      status : operation successful.
    """
    @manage(['rooms'])
    def init(self):
        self.rooms = dict()

    @condition(["room","id"], ["rooms","status"])
    def compute(self, room, id):
        allowed = True
        for key in self.rooms.keys():
            if key is not room:
                if id in self.rooms[key]:
                    allowed = False
                    break

        if allowed and room in self.rooms:
            if id in self.rooms[room]:
                self.rooms[room].remove(id)
            else:
                self.rooms[room].append(id)
        elif allowed:
            self.rooms[room] = list()
            self.rooms[room].append(id)

        return (self.rooms, allowed)

    action_priority = (compute, )
