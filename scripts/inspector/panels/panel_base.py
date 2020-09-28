# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from inspector.vendor.Qt import QtCore
from inspector.vendor.Qt import QtWidgets


class PanelBase(QtWidgets.QFrame):
    inner_selection_changed = QtCore.Signal(list)

    def __init__(self, node_info, parent=None):
        super(PanelBase, self).__init__(parent=parent)
        self._node_info = node_info

    def is_target(self):
        return False
