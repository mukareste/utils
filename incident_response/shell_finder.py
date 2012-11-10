#!/usr/bin/env python
"""
Shell Finder for Cpanel v0.9 / 2011 by mitchell <mitchell@csc.bg>.
Developed by Cyber Security Consulting for Solid Hosting (http://solid-hosting.net
"""
#       Copyright (c) 2011, Cyber Security Consulting, Ltd. (csc.bg)
#       All rights reserved.
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#       

import sys
import os
import subprocess
import time
from datetime import datetime

def unique(seq): 
        """Returns a sorted and uniqued list"""
        set = {} 
        map(set.__setitem__, seq, []) 
        return sorted(set.keys())                                                                                                                                                               

def exit(error = ""):
    """Exists with a custom error message"""
    print error
    sys.exit()

def get_accounts(accounts_file):
    """Reads the usernames from the accounts file"""

    if not os.path.exists(accounts_file):
        exit("No accounts file")
    
    accounts = []
    f = open(accounts_file, "r")
    for line in f.readlines():
        accounts.append(line.strip().split(": ")[1])
    f.close()
    return unique(accounts)

def av_scan(accounts):
    """Runs a clamav scan"""

    infected = []
    scanner = "/usr/bin/clamscan"
    nice = "/bin/nice"
    scanner_options = "'-r -i --no-summary'"

    for acct in accounts:
        path = "/home/%s/public_html/" % (acct)
        if not os.path.exists(path):
            continue
        output = subprocess.Popen([nice, '-n', '-20', scanner, '-r', '-i', '--no-summary', "--bytecode-timeout=60", path], stdout = subprocess.PIPE).communicate()[0]
        inf = output.split("\n")
        
        for line in inf:
            res = line.split(": ")
            if not line:
                continue
            infected.append(res[0])
    
    return infected

def grep_for_shells(accounts, grep_str):
    """Grep for shells"""

    shelled = []
    nice = "/bin/nice"
    grepper = "/bin/grep"
    
    for acct in accounts:
        path = "/home/%s/public_html/" % (acct)
        if not os.path.exists(path):
            continue
        output = subprocess.Popen([nice, "-n", "-20", grepper, "-srilFf", grep_str, path], stdout = subprocess.PIPE).communicate()[0]
        inf = output.split("\n")
        for line in inf:
            if not line:
                continue
            shelled.append(line)
    return shelled

def produce_report(timer1,timer2, elapsed, hacked):
    """Prepares and sends a report"""

    # Uncomment the two lines below to make the script exit if there are no findings
    #if len(hacked) == 0:
        #sys.exit()
    sendmail_location = "/usr/sbin/sendmail"
    hostname = os.uname()[1]
    from_mail = "" # Enter the From email
    reply_mail = "" # Enter the Reply-To email
    cc_mail = "" # Enter the CC email
    to_mail = "" # Enter the recipient email
    log_file = '/var/shell_finder/log.txt' # Log file location
    our_header = "X-Produced-By: Shell_Finder"

    times = [datetime.fromtimestamp(timer1), datetime.fromtimestamp(timer2), elapsed / 60]
    users = []

    for i in hacked:
        user = i.split("/")
        users.append(user[2])

    user_count = len(unique(users))
    file_count = len(hacked)

    with open(log_file, 'w') as logfile:
        logfile.write("************************************************************************\n")
        logfile.write("Script started on %s\nScript completed on %s\nScript took %s minutes (%s hours)\n" % (times[0], times[1], times[2], times[2] / 60))
        logfile.write("************************************************************************\n")
        logfile.write("\nAffected users[%s]:\n" % (user_count))

        for i in unique(users):
            logfile.write("%s\n" % (i))

        logfile.write("\nCompromised files[%s]:\n" % (file_count))
        for i in hacked:
            logfile.write("%s\n" % (i))

    p = os.popen("%s -t" % sendmail_location, "w")
    p.write("From: %s\n" % (from_mail))
    p.write("To: %s\n" % (to_mail))
    p.write("CC: %s\n" % (cc_mail))
    p.write("Reply-to: %s\n" % (reply_mail))
    p.write("Subject: Shell Finder identified %s compromised accounts on %s\n" % (user_count, hostname))
    p.write(our_header)
    p.write("\n")

    with open(log_file, 'r') as logfile:
        while True:
            contents = logfile.read()
            if not contents:
                break
            p.write(contents)
    p.close()

def main():
    """The main function"""

    grep_strings_file = "/root/.shell_finder/shell_strings.txt" # The location of the malicious strings database (one string per line)
    grep_v_strings_file = "/root/.shell_finder/grep_legits.txt" # The location of the whitelist
    accounts = get_accounts("/etc/userdomains") # The location of the userdomains file
    infections = av_scan(accounts)
    grepped = grep_for_shells(accounts, grep_strings_file)
    compromised = unique(infections + grepped)

    exclude = []
    f = open(grep_v_strings_file, "r")
    for line in f.readlines():
        exclude.append(line.strip())

    for x in exclude:
        try:
            compromised.remove(x)
        except(ValueError):
            pass

    return compromised

if __name__ == '__main__':

    timer_start = time.time()
    compromised = main()
    timer_end = time.time()
    timer_elapsed = timer_end - timer_start
    produce_report(timer_start, timer_end, timer_elapsed, compromised)
