#!/usr/bin/env python3

# Copyright (c) 2019, Alchemy Meister
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
"""

import sys
from constants.overlay import OverlayMode, OverlayPosition
from gui.model import OverlayModel
from patterns.factory import OverlayFactory
from patterns.singleton import Singleton

from .overlay import Overlay

class OverlayManager(metaclass=Singleton):
    """
    """
    def __init__(
            self, launcher, default_overlay_enabled=False,
            default_overlay_id=None, default_position=None, default_theme=None
        ):
        self.launcher = launcher
        self.overlay_factory = OverlayFactory()
        self.overlays = dict()

        self.current_theme = None

        self.current_overlay: Overlay
        self.current_overlay = None

        if default_overlay_id is not None:
            self.__add_overlay(default_overlay_id)
        else:
            self.__add_overlay(OverlayMode.FRAMEDATA.value)

        self.overlay_enabled = default_overlay_enabled
        self.enable_overlay(self.overlay_enabled)

        if default_position:
            self.change_overlay_position(default_position)
        else:
            self.change_overlay_position(OverlayPosition.TOP)

        if default_theme:
            self.change_overlay_theme(default_theme)
        else:
            self.change_overlay_theme(OverlayModel().get_theme(1))

    def enable_overlay(self, enable):
        self.overlay_enabled = enable
        if enable:
            self.current_overlay.on()
        else:
            self.current_overlay.off()

    def change_overlay(self, mode: OverlayMode):
        sys.stdout.write('Turning overlay off')
        self.current_overlay.off()
        self.overlays[self.current_overlay.__class__.CLASS_ID] = (
            self.current_overlay
        )
        change_overlay = self.overlays.get(mode.value)
        if change_overlay:
            sys.stdout.write('changing overlay')
            self.current_overlay = change_overlay
        else:
            sys.stdout.write('creating new overlay')
            self.__add_overlay(mode.value)
        sys.stdout.write('Turning overlay on')
        self.current_overlay.on()

    def change_overlay_position(self, position):
        self.current_position = position
        self.current_overlay.set_position(position)

    def change_overlay_theme(self, theme_dict):
        self.current_theme = theme_dict
        self.current_overlay.set_theme(theme_dict)

    def write_to_overlay(self, string):
        if self.current_overlay.enabled and self.current_overlay.visible:
            self.current_overlay.write(string)

    def __add_overlay(self, overlay_id):
        self.current_overlay = self.overlay_factory.create_class(
            overlay_id, self.launcher
        )