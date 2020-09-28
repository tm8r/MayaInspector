# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from maya import cmds


def get_input_targets(blend_shape):
    if not blend_shape:
        return []
    input_targets = cmds.listConnections(blend_shape + ".inputTarget") or []
    return input_targets


def get_relative_blend_shapes(target, all_descendents=False, include_self=False):
    blend_shapes = []
    if not target:
        return blend_shapes
    transforms = cmds.listRelatives(target, type="transform", ad=all_descendents, pa=True) or []
    if include_self:
        transforms.append(target)
    for t in transforms:
        tmp_blend_shapes = cmds.ls(cmds.listHistory(t), type="blendShape")
        if not tmp_blend_shapes:
            continue
        blend_shapes.extend(tmp_blend_shapes)
    return blend_shapes
