# -*- coding: utf-8 -*-
"""manage style sheet"""
from __future__ import absolute_import, division, print_function

import os

_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")

_TEMPLATE_DICT = {
    "MAIN_COLOR": "#48aab5",
    "MAIN_DARK_COLOR": "#398891",
}


class StyleSheet(object):
    """manage style sheet"""

    _CSS_DICT = {}

    def __init__(self):
        """initialize"""
        self._core_css = _replace_template(_read_text(_RESOURCES_DIRECTORY + "/core.css"), _TEMPLATE_DICT)

    @property
    def core_css(self):
        """get core css

        Returns:
            str: core css
        """
        return self._core_css

    def get_css(self, path):
        """get merged css(core css and unique css)

        Args:
            path (str): css path

        Returns:
            unicode: result css
        """
        if path not in self._CSS_DICT:
            self._CSS_DICT[path] = _replace_template(_read_text(path), _TEMPLATE_DICT)
        return self._core_css + self._CSS_DICT[path]

    def reload(self):
        """reload CSS(for develop)"""
        self._core_css = _replace_template(_read_text(_RESOURCES_DIRECTORY + "/core.css"), _TEMPLATE_DICT)
        self._CSS_DICT = {}


def _replace_template(data, replace_dict):
    for key, value in replace_dict.items():
        data = data.replace(key, value)
    return data


def _read_text(path):
    res = ""
    if not os.path.isfile(path):
        return res
    with open(path, "r") as f:
        res = f.read()
    return res
