# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys

from maya import cmds
from maya import mel

_MODULE_FILE_NAME = "MayaInspector.mod"
_ROOT_PATH_PLACEHOLDER = "$ROOT_PATH"


def onMayaDroppedPythonFile(*args, **kwargs):
    """for Maya2017.3+"""
    distributed = _distribute_mod_file()
    if not distributed:
        return
    _create_shelf()


def onMayaDroppedMelFile():
    "for old Maya"
    distributed = _distribute_mod_file()
    if not distributed:
        return
    _create_shelf()


def _distribute_mod_file():
    root_path = os.path.dirname(__file__)
    module_paths = mel.eval("getenv MAYA_MODULE_PATH;")
    user_app_dir = cmds.internalVar(uad=True)
    version = cmds.about(v=True)[:4]
    module_file_template = os.path.join(root_path, _MODULE_FILE_NAME)
    module_path = user_app_dir + "{0}/{1}".format(version, "modules")
    if module_path not in module_paths:
        cmds.error("MayaInspector install failed. Maya module path is not found.")
        return False

    if not os.path.isdir(module_path):
        os.makedirs(module_path)

    with open(module_file_template, "r") as f:
        module_content = f.read()

    module_content = module_content.replace(_ROOT_PATH_PLACEHOLDER, root_path)

    with open(module_path + "/" + _MODULE_FILE_NAME, "w") as f:
        f.write(module_content)

    script_path = root_path + "/scripts"
    script_path = script_path.replace(os.sep, "/")
    if not os.path.exists(script_path):
        cmds.error("MayaInspector install failed. scripts path is not found.")
        return False
    if script_path not in sys.path:
        sys.path.append(script_path)

    return True


def _create_shelf():
    root_path = os.path.dirname(__file__)
    script_path = root_path + "/scripts"
    icon_path = root_path + "/icons/maya_inspector_icon.png"

    command = """
# -------------------------
# MayaInspector
# Author: @tm8r
# https://github.com/tm8r/MayaInspector
# -------------------------

import inspector.view
win = inspector.view.MayaInspector.open()""".format(script_path)

    shelf = mel.eval("$gShelfTopLevel=$gShelfTopLevel")
    parent = cmds.tabLayout(shelf, query=True, selectTab=True)
    cmds.shelfButton(
        command=command,
        image=icon_path,
        annotation="MayaInspector",
        label="MayaInspector",
        sourceType="Python",
        parent=parent
    )


if __name__ == "_installShelfTm8rMayaInspector":
    onMayaDroppedMelFile()
