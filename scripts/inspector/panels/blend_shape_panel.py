# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from inspector.vendor.Qt import QtCore
from inspector.vendor.Qt import QtWidgets

from ..libs import maya
from ..libs import qt
from . import panel_base


class BlendShapePanel(panel_base.PanelBase):

    def __init__(self, node_info):
        super(BlendShapePanel, self).__init__(node_info)
        self._blend_shapes = []

    # override
    def create_ui(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(root_layout)

        material_widget = qt.widgets.collapse_widget.QCollapseWidget("BlendShape")
        root_layout.addWidget(material_widget)

        tree_widget = QtWidgets.QTreeWidget()
        tree_widget.setHeaderHidden(True)
        tree_widget.setColumnCount(1)
        tree_widget.setFocusPolicy(QtCore.Qt.NoFocus)

        tree_widget.itemClicked.connect(self._on_tree_item_clicked)

        material_widget.addWidget(tree_widget)
        for i in xrange(0, len(self._blend_shapes)):
            target = self._blend_shapes[i]
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, target)

            tree_widget.insertTopLevelItem(i, item)

            input_targets = maya.blend_shape.get_input_targets(target)
            if not input_targets:
                continue
            for f in input_targets:
                file_item = QtWidgets.QTreeWidgetItem()
                file_item.setText(0, f)
                item.addChild(file_item)
        tree_widget.expandAll()

    # override
    def is_target(self):
        self._blend_shapes = maya.blend_shape.get_relative_blend_shapes(self._node_info, include_self=True)
        if not self._blend_shapes:
            return False
        return True

    def _on_tree_item_clicked(self, current, previous):
        self.inner_selection_changed.emit(current.text(0))
