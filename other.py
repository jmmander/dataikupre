#!/usr/bin/python

import os
import sys
import yum
#imported yum stuff
yb = yum.YumBase()
yb.setCacheDir()
prereqs = ["emr-*", ]

for
if yb.rpmdb.searchNevra(name=prereqs):
    okay = prereqs + " is already installed"
    print(okay)
else:
    nokay = prereqs + " is not installed"
    print(nokay)