# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from logging import getLogger

from maya import cmds

logger = getLogger(__name__)


def has_shape(node):
    children = cmds.listRelatives(node, pa=True, s=True)
    if not children:
        return False
    return bool([x for x in children if cmds.nodeType(x) == "mesh"])
