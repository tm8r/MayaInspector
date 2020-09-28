# -*- coding: utf-8 -*-
u"""コントローラー"""
from __future__ import absolute_import, division, print_function

from inspector.vendor.Qt import QtCore

from maya import cmds
from maya.api import OpenMaya as om


class Controller(QtCore.QObject):
    block_changed = QtCore.Signal(bool)
    selection_changed = QtCore.Signal(list)

    def __init__(self, view):
        super(Controller, self).__init__()
        self._initialized = False
        self._view = view
        self._selected = []
        self._callback_ids = []
        self._block_refresh = False
        self._add_event_callback()
        self._connect_signals()
        self._update_selection()
        self._initialized = True

    @property
    def selected(self):
        return self._selected

    def select_node(self, node):
        self._block_refresh = True
        cmds.select(node)

        cmds.evalDeferred(self._unblock_refresh)

    def _add_event_callback(self):
        self._callback_ids.append(om.MEventMessage.addEventCallback("SelectionChanged", self._on_selection_changed))

    def _connect_signals(self):
        self.selection_changed.connect(self._view.refresh_content)

    def _unblock_refresh(self):
        self._block_refresh = False

    def _on_selection_changed(self, *args, **kwargs):
        if self._block_refresh:
            return
        self._update_selection()

    def _update_selection(self, force=False):
        tmp_selected = cmds.ls(sl=True, o=True, st=True)
        selected_dict = dict(zip(tmp_selected[::2], tmp_selected[1::2]))
        res = set()
        for node, node_type in selected_dict.items():
            if node_type == "mesh":
                parents = cmds.listRelatives(node, parent=True)
                if not parents:
                    continue
                res.add(parents[0])
                continue
            res.add(node)

        if not force and not set(self._selected).symmetric_difference(res):
            return

        self._selected = list(res)
        if self._initialized:
            self.selection_changed.emit(self._selected)

    def update(self):
        self._update_selection(force=True)

    def destroy(self):
        for callback_id in self._callback_ids:
            om.MEventMessage.removeCallback(callback_id)
