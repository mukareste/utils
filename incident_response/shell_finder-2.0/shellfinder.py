#!/usr/bin/env python

from sfutils.helpers.GenOps import *
from sfutils.scanner.Scanner import *
import time
from datetime import datetime

config_file = 'shellfinder.ini'

def main():
    """ The main func """

    operations = GenOps()
    finder = SearchShells()
    strings_file, domains_file, report_file, legits, from_address, to_address, cc_address, header = operations.GetOptions(config_file)
    users = operations.GetAccounts(domains_file)
    timer_start = time.time()
    compromised = finder.GrepForShells(users, strings_file, legits)
    timer_end = time.time()
    timer_elapsed = timer_end - timer_start
    report = operations.ProduceReport(timer_start, timer_end, timer_elapsed, compromised, report_file)
    mail_report = operations.MailReport(report_file, from_address, to_address, cc_address, header, compromised)

if __name__ == "__main__":

    main()
