#!/usr/bin/python

import os
import sys
import yum

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

yb = yum.YumBase()
yb.setCacheDir()
plist = yb.rpmdb.returnPackages()
prereqs = ["hadoop-client", "hadoop-lzo", "spark-core", "spark-python", "spark-R", "spark-datanucleus", "hive", "hive-hcatalog", "pig", "tez", "openssl-devel", "emrfs", "emr-*"]
print(plist)
print(type(plist))
for pkg in prereqs:
    if pkg in plist:
        okay = pkg + " is already installed"
        print(bcolors.OKGREEN + okay + bcolors.ENDC)
    else:
        nokay = pkg + " is not installed"
        print(bcolors.FAIL + nokay + bcolors.ENDC)

    #if yb.rpmdb.searchNevra(name=pkg):
     #   okay = pkg + " is already installed"
      #  print(bcolors.OKGREEN + okay + bcolors.ENDC)
    #else:
     #  nokay = pkg + " is not installed"
      #  print(bcolors.FAIL + nokay + bcolors.ENDC)









