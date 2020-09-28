# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from inspector.vendor.Qt import QtCore
from inspector.vendor.Qt import QtWidgets

from ..libs import maya
from ..libs import qt
from . import panel_base


class SkinPanel(panel_base.PanelBase):

    def __init__(self, node_info):
        super(SkinPanel, self).__init__(node_info)
        self._skin_cluster = None
        self._influences = []
        self._materials = []

    # override
    def create_ui(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(root_layout)

        skin_widget = qt.widgets.collapse_widget.QCollapseWidget("Skin")
        root_layout.addWidget(skin_widget)

        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tree_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.tree_widget.itemClicked.connect(self._on_tree_item_clicked)

        skin_widget.addWidget(self.tree_widget)
        if not self._skin_cluster:
            return

        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, self._skin_cluster)

        self.tree_widget.insertTopLevelItem(0, item)
        for influence in self._influences:
            child_item = QtWidgets.QTreeWidgetItem()
            child_item.setText(0, influence)
            item.addChild(child_item)
        self.tree_widget.expandAll()

    # override
    def is_target(self):
        if not maya.mesh.has_shape(self._node_info):
            return False
        skin_cluster = maya.skin.get_skin_cluster(self._node_info)
        if not skin_cluster:
            return False
        self._skin_cluster = skin_cluster
        self._influences = sorted(maya.skin.get_influences(skin_cluster, self._node_info + ".vtx[0]", ignore_below=0))
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
