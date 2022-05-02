# -*- coding: utf-8 -*-
"""view of Inspector"""
from __future__ import absolute_import, division, print_function

from .vendor.Qt import QtCompat
from .vendor.Qt import QtCore
from .vendor.Qt import QtWidgets

from .libs import maya
from .libs import qt
from . import controller
from . import panel_factory

from maya import cmds
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

try:
    long
except NameError:
    long = int

try:
    MAYA_WINDOW = QtCompat.wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
except:
    MAYA_WINDOW = None

_WINDOW_SUFFIX = "_window"
_WORKSPACE_CONTROL_SUFFIX = "WorkspaceControl"
_UI_SCRIPT_FORMAT = """import {0};{0}.{1}.restore()"""
_ID_FORMAT = "{0}.{1}"


def _create_window_name(object_id):
    return object_id + _WINDOW_SUFFIX


def _create_workspace_control_name(window_id):
    return window_id + _WORKSPACE_CONTROL_SUFFIX


def _convert_identifier(cls):
    return _ID_FORMAT.format(cls.__module__, cls.__name__)


class MayaInspector(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    def __init__(self, parent=MAYA_WINDOW):
        super(MayaInspector, self).__init__(parent)
        self.controller = controller.Controller(self)
        self.factory = panel_factory.PanelFactory(self.controller)

        self.setWindowTitle("Inspector")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName(self.window_name())
        self.setProperty("saveWindowPref", True)
        self.setStyleSheet(qt.stylesheet.StyleSheet().core_css)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.root_widget = QtWidgets.QFrame(self)
        self.root_widget.setObjectName("root")
        self.setMinimumSize(QtCore.QSize(380, 200))
        self.setCentralWidget(self.root_widget)

        root_layout = QtWidgets.QGridLayout(self.root_widget)
        root_layout.setObjectName("root_layout")
        root_layout.setContentsMargins(8, 8, 8, 8)
        root_layout.setSpacing(0)

        main_widget = QtWidgets.QFrame()
        self.inspector_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(self.inspector_layout)

        tool_content_wrapper = QtWidgets.QScrollArea()
        tool_content_wrapper.setWidget(main_widget)
        tool_content_wrapper.setFrameShape(QtWidgets.QFrame.NoFrame)
        tool_content_wrapper.setWidgetResizable(True)
        tool_content_wrapper.setContentsMargins(0, 0, 0, 0)

        root_layout.addWidget(tool_content_wrapper, 0, 0, 1, 1)

        self.controller.update()

    @classmethod
    def window_name(cls):
        return _create_window_name(cls._get_identifier())

    @classmethod
    def workspace_control_name(cls):
        return _create_workspace_control_name(cls.window_name())

    @classmethod
    def ui_script(cls):
        return _UI_SCRIPT_FORMAT.format(cls.__module__, cls.__name__)

    @classmethod
    def _get_identifier(cls):
        return _convert_identifier(cls)

    @classmethod
    def open(cls, *args):
        maya.layout.delete_window(cls.window_name())
        maya.layout.delete_workspace_control(cls.workspace_control_name())

        win = cls()
        ui_script = cls.ui_script()
        win.show(dockable=True, uiScript=ui_script)
        return win

    def refresh_content(self, selected):
        qt.layout.clear_layout(self.inspector_layout)

        if not selected:
            self.inspector_layout.addWidget(QtWidgets.QLabel("No item selected."))
            spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.inspector_layout.addSpacerItem(spacer)
            return

        tab_widget = QtWidgets.QTabWidget()
        self.inspector_layout.addWidget(tab_widget)

        for node in selected:
            frame = QtWidgets.QFrame()
            layout = QtWidgets.QVBoxLayout(frame)

            layout.addWidget(QtWidgets.QLabel("Type: {0}".format(cmds.objectType(node))))
            self.factory.add_panels(node, layout)

            spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
            layout.addSpacerItem(spacer)

            tab_widget.addTab(frame, node)

    @classmethod
    def restore(cls, *args):
        win = cls()
        win.restore_workspace_parent()

    def restore_workspace_parent(self):
        parent = omui.MQtUtil.getCurrentParent()
        mixin_ptr = omui.MQtUtil.findControl(self.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(long(mixin_ptr), long(parent))

    # override
    def dockCloseEventTriggered(self):
        self.controller.destroy()
