#!/usr/bin/env python
# -*- coding: Latin-1 -*-
# vim: tabstop=4 shiftwidth=4 expandtab


import yaml
import re


def nml_decode(text):
    """
    """
    output = []
    text = re.sub("\t", " ", text)

    # dummy way to deal with comments. Need to improve it
    text = re.sub("\s*!.*\n", "\n", text)

    for namelists in re.findall("&((?:.*\n)+?)/", text):
        g = re.match("\s*(?P<groupname>\w+)\n((?:.*\n)*)", namelists).groups()
        output.append("%s:\n" % g[0])
        #for p in re.findall("\s+(\w+)\s*=\s*(\.?.*\.?)\s*,?\s*(!.*)\n", g[1]):
        for p in re.findall("\s*(\w+)\s*=\s*(\.?.*\.?)\s*,?\s*\n", g[1]):
            tmp = re.sub(",$|\s*", "", p[1])
            if tmp == ".false.":
                tmp = False
            if tmp == ".true.":
                tmp = True
            output.append("  %s: %s\n" % (p[0], tmp))
    textout = "".join(output)
    return yaml.load(textout)

# Working on
#group_pattern = """
#(&\s*
#(?P<groupname>\w+).*\n
#(.*\n)+
#)
#"""
#re.search(group_pattern, text, re.VERBOSE).groups()


def yaml2nml(cfg):
    """
    """
    output = []
    keys = cfg.keys()
    keys.sort()
    for k in keys:
        output.append(" &%s\n" % k)
        if cfg[k] != None:
            parameters = cfg[k].keys()
            parameters.sort()
            for kk in parameters:
                if cfg[k][kk] is False:
                    v = '.false.'
                elif cfg[k][kk] is True:
                    v = '.true.'
                else:
                    v = cfg[k][kk]
                output.append("    %s = %s,\n" % (kk, v))
        output.append("/\n\n")
    return "".join(output)
