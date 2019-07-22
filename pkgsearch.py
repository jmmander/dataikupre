#!/usr/bin/python

import os
import sys
from yummy import yumbase

yb = yum.YumBase()
yb.setCacheDir()
prereqs = ["hadoop-client", "hadoop-lzo", "spark-core", "spark-python", "spark-R", "spark-datanucleus", "hive", "hive-hcatalog", "pig", "tez", "openssl-devel", "emrfs", ''"emr-*"'']
for pkg in prereqs:
    if yb.rpmdb.searchNevra(name=pkg):
        print(pkg + "is already installed")
else:
   print(pkg + "not installed")









