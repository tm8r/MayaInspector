# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from . import panels

_PANELS = [
    panels.BlendShapePanel,
    panels.ConstraintPanel,
    panels.MaterialPanel,
    panels.SkinPanel,
]


class PanelFactory(object):

    def __init__(self, controller):
        self.panels = _PANELS
        self._controller = controller

    def add_panels(self, node, layout):
        for p in self.panels:
            panel = p(node)
            if not panel.is_target():
                continue
            panel.create_ui()

            panel.inner_selection_changed.connect(self._controller.select_node)
            layout.addWidget(panel)
