#!/usr/bin/env python

import sys

data = sys.stdin
for line in data:
    line = line.split('=', 1)
    print("export \"{}\"='{}'".format(line[0], line[1].rstrip()))

