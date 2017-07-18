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

from calvin.utilities.calvinlogger import get_actor_logger
from calvin.actor.actor import Actor, condition, manage

_log = get_actor_logger(__name__)


class MultipleImageRenderer(Actor):

    """
    Render images.

    Inputs:
        image: image to add
        id: Id to add image with
        remove: Id to remove from images
    """

    @manage(['width', 'height', 'images'])
    def init(self, width=640, height=480):
        self.width = width
        self.height = height
        self.images = dict()
        self.setup()

    def setup(self):
        self.use("calvinsys.media.image", shorthand="image")
        self.use('calvinsys.native.python-base64', shorthand="base64")
        self.image = self["image"]

    def did_migrate(self):
        self.setup()

    def will_end(self):
        self.image.close()

    def will_migrate(self):
        self.image.close()
    

    def show_images(self):
        imagelist = list()
        for usrid, image in self.images.iteritems():
            imagelist.append(image)
        self.image.show_images(imagelist, self.width, self.height)

    @condition(action_input=('image','id'))
    def add_image(self, image, usrid):
        if "id%d" % usrid in self.images:
            _log.error("Id %d already existed in images list." % usrid)
        else:
            self.images["id%d" % usrid] = self['base64'].b64decode(image)
        self.show_images()

    @condition(action_input=('remove',))
    def del_image(self, remove):
        if "id%d" % remove not in self.images:
            _log.error("Id %d does not exist" % remove)
        else:
            del self.images["id%d" % remove]
        self.show_images()

    action_priority = (add_image, del_image)
    requires =  ['calvinsys.media.image', 'calvinsys.native.python-base64']
