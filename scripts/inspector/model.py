# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class NodeInfo(object):

    def __init__(self, node):
        self._node = node

    @property
    def node(self):
        return self._node
