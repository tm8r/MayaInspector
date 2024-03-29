# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from inspector.vendor.Qt import QtCore
from inspector.vendor.Qt import QtWidgets

from ..libs import maya
from ..libs import qt
from . import panel_base

from maya import cmds


class MaterialPanel(panel_base.PanelBase):

    def __init__(self, node_info):
        super(MaterialPanel, self).__init__(node_info)
        self._materials = []

    # override
    def create_ui(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(root_layout)

        material_widget = qt.widgets.collapse_widget.QCollapseWidget("Materials")
        root_layout.addWidget(material_widget)

        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setFocusPolicy(QtCore.Qt.NoFocus)

        self.tree_widget.itemClicked.connect(self._on_tree_item_clicked)

        material_widget.addWidget(self.tree_widget)
        for i in range(0, len(self._materials)):
            m = self._materials[i]
            mat_item = QtWidgets.QTreeWidgetItem()
            mat_item.setText(0, m)

            self.tree_widget.insertTopLevelItem(i, mat_item)

            file_nodes = maya.material.get_connected_all_files(m)
            if not file_nodes:
                continue
            for f in file_nodes:
                file_item = QtWidgets.QTreeWidgetItem()
                file_item.setText(0, f)
                mat_item.addChild(file_item)
        self.tree_widget.expandAll()

    # override
    def is_target(self):
        if not maya.mesh.has_shape(self._node_info):
            return False
        histories = [x for x in cmds.listHistory(self._node_info, future=True, af=True) if
                     cmds.nodeType(x) == "shadingEngine"]
        if not histories:
            return False
        self._materials = cmds.ls(cmds.listConnections(histories), mat=True)
        if not self._materials:
            return False
        return True

    def _on_tree_item_clicked(self, current, previous):
        selected = self.tree_widget.selectedIndexes()
        if not selected:
            return

        targets = []
        for index in selected:
            item = self.tree_widget.itemFromIndex(index)
            if not item or not item.data:
                return
            targets.append(item.data(0, QtCore.Qt.DisplayRole))

        self.inner_selection_changed.emit(targets)
