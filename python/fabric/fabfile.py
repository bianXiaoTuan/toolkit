#!/usr/bin/python
# -*- coding: utf-8 -*-

from fabric.api import run

def host_type():
    run('uname -s')
