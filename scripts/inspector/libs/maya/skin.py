# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from maya import cmds


def get_influences(skin_cluster, vertex, ignore_below=0.00000000000000000000000000000000000000001):
    return cmds.skinPercent(skin_cluster, vertex, q=True, ib=ignore_below, t=None)


def get_skin_cluster(mesh):
    histories = cmds.listHistory(mesh)
    if not histories:
        return None
    return next((x for x in histories if cmds.objectType(x) == "skinCluster"), None)
