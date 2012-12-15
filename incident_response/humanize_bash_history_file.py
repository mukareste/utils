#!/usr/bin/env python

import sys,re
import datetime

data = sys.stdin.readlines()

for line in data:
    try:
        etime = re.search('^#[0-9]{10}$', line).group(0).replace('#', '').rstrip()
        cur_time = datetime.datetime.fromtimestamp(int(etime)).strftime('%Y-%m-%d %H:%M:%S')
        sys.stdout.write("%s " % (cur_time))
    except(AttributeError):
        sys.stdout.write(line)
