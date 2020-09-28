# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from inspector.vendor.Qt import QtCore
from inspector.vendor.Qt import QtWidgets

from ..libs import maya
from ..libs import qt
from . import panel_base

from maya import cmds


class ConstraintPanel(panel_base.PanelBase):

    def __init__(self, node_info):
        super(ConstraintPanel, self).__init__(node_info)
        self._constraints = []
        self._rconstraints = []

    # override
    def create_ui(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(root_layout)

        const_widget = qt.widgets.collapse_widget.QCollapseWidget("Constraints")
        root_layout.addWidget(const_widget)
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setIndentation(0)
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setColumnCount(2)
        self.tree_widget.hideColumn(1)
        self.tree_widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tree_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree_widget.itemClicked.connect(self._on_tree_item_clicked)
        const_widget.addWidget(self.tree_widget)
        if self._constraints:
            for const_type, members in self._constraints.items():
                for m in members:
                    item = QtWidgets.QTreeWidgetItem()
                    item.setText(0, "<- {0}({1})".format(cmds.ls(m)[0], const_type))
                    item.setText(1, m)
                    self.tree_widget.insertTopLevelItem(self.tree_widget.topLevelItemCount(), item)
        if self._rconstraints:
            for const_type, members in self._rconstraints.items():
                for m in members:
                    item = QtWidgets.QTreeWidgetItem()
                    item.setText(0, "-> {0}({1})".format(cmds.ls(m)[0], const_type))
                    item.setText(1, m)
                    self.tree_widget.insertTopLevelItem(self.tree_widget.topLevelItemCount(), item)

    # override
    def is_target(self):
        if "transform" not in cmds.nodeType(self._node_info, i=True):
            return False
        self._constraints = maya.constraint.get_constraint_targets_dict(self._node_info)
        self._rconstraints = maya.constraint.get_constraint_mebers_dict(self._node_info)
        if not self._constraints and not self._rconstraints:
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
            targets.append(item.data(1, QtCore.Qt.DisplayRole))

        self.inner_selection_changed.emit(targets)
