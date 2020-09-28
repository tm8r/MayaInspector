# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import defaultdict

from maya import cmds


class ConstraintType(object):
    parentConstraint = "parentConstraint"
    pointConstraint = "pointConstraint"
    orientConstraint = "orientConstraint"
    scaleConstraint = "scaleConstraint"
    aimConstraint = "aimConstraint"


def get_constraint_targets(node, constraint_type=None):
    constraints = _get_constraints(node, constraint_type)
    if not constraints:
        return []
    res = []
    for c in constraints:
        members = cmds.listConnections(c + ".target")
        if not members:
            continue
        res.extend(list(set([x for x in members if x != c])))
    return list(set(res))


def get_constraint_members(node, constraint_type=None):
    constraints = _get_constraints_reverse(node, constraint_type)
    if not constraints:
        return []
    res = []
    for c in constraints:
        members = cmds.listConnections(c + ".constraintParentInverseMatrix")
        res.extend(members)
    return list(set(res))


def get_constraint_targets_dict(node):
    constraints = _get_constraints(node)
    res = defaultdict(list)
    if not constraints:
        return res
    for c in constraints:
        members = cmds.listConnections(c + ".target")
        if not members:
            continue
        members = list(set([x for x in members if x != c]))
        res[c].extend(members)
    return res


def get_constraint_mebers_dict(node):
    constraints = _get_constraints_reverse(node)
    res = defaultdict(list)
    if not constraints:
        return res
    for c in constraints:
        members = cmds.listConnections(c + ".constraintParentInverseMatrix")
        if not members:
            continue
        res[c].extend(members)
    return res


def _get_constraints(node, constraint_type=None):
    constraints = cmds.listConnections(node, s=True, d=False, t="constraint")
    if not constraints:
        return []
    constraints = list(set(constraints))
    if constraint_type:
        constraints = [x for x in constraints if constraint_type in x]
    return constraints


def _get_constraints_reverse(node, constraint_type=None):
    constraints = cmds.listConnections(node + ".parentMatrix", d=True, s=False, t="constraint")
    if not constraints:
        constraints = []
    constraints = list(set(constraints))

    if constraint_type:
        constraints = [x for x in constraints if constraint_type in x]
    return constraints
