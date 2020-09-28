# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from maya import cmds


def get_connected_all_files(target):
    result = []
    result.extend(get_connected_files(target))
    result.extend(get_files_via_shading_depend_node(target, "layeredTexture"))
    result.extend(get_files_via_shading_depend_node(target, "bump2d"))
    return result


def get_files_via_shading_depend_node(target, via_type):
    result = []
    shading_depend_nodes = cmds.listConnections(target, type=via_type)
    if not shading_depend_nodes:
        return result
    for n in shading_depend_nodes:
        result.extend(get_connected_files(n))
    return result


def get_connected_files(target):
    result = []
    files = cmds.listConnections(target, type="file")
    if not files:
        return result
    return list(set(files))


def get_material_from_transform(transforms, full_path=False):
    res = []
    materials = cmds.ls(mat=True)
    for material in materials:
        connections = cmds.listConnections(material, d=True, type="shadingEngine")
        for c in connections:
            members = cmds.listConnections(c + ".dagSetMembers", s=True)
            if not members:
                continue
            members = cmds.ls(members, l=full_path)
            for m in members:
                if m not in transforms:
                    continue
                res.append(material)
    return list(set(res))
