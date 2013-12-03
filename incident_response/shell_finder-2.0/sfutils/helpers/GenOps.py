import sys
import os
import subprocess
from datetime import datetime
from ConfigParser import SafeConfigParser

class GenOps(object):
    """ Helper functions """


    def __init__ (self):
        """ Constructor """

        self.hostname = os.uname()[1]

    def GetOptions(self, config_file):
        """ Get the options from the config file """

        self.config_file = config_file
        if not os.path.exists(self.config_file):
            print("Please, create the config file: {0}").format(self.config_file)
            sys.exit()
        self.parser = SafeConfigParser()
        self.parser.read(self.config_file)
        self.strings = self.parser.get('General', 'strings')
        self.domains = self.parser.get('General', 'domains')
        self.report = self.parser.get('General', 'report')
        self.legits = self.parser.get('General', 'legits')
        self.from_address = self.parser.get('Mail', 'from')
        self.to_address = self.parser.get('Mail', 'to')
        self.cc_address = self.parser.get('Mail', 'cc')
        self.header = self.parser.get('Mail', 'header')

        return self.strings, self.domains, self.report, self.legits, self.from_address, self.to_address, self.cc_address, self.header
            

    def GetAccounts(self, *args):
        """Reads the usernames from the accounts file"""

        self.accounts_file = args[0]
        self.accounts = set()

        if not os.path.exists(self.accounts_file):
            exit("No accounts file")

        f = open(self.accounts_file, "r")
        for line in f.readlines():
            self.accounts.add(line.strip().split(": ")[1])
        f.close()
        return sorted(self.accounts)

    def ProduceReport(self, *args):
        """Generate the report file """

        self.timer1 = args[0]
        self.timer2 = args[1]
        self.elapsed = args[2]
        self.hacked = args[3]
        self.reportfile = args[4]
        self.users = set()
        self.times = [datetime.fromtimestamp(self.timer1), datetime.fromtimestamp(self.timer2), self.elapsed / 60]

        for i in self.hacked:
            self.user = i.split("/")
            self.users.add(self.user[2])
           
        self.user_count = len(self.users)
        self.file_count = len(self.hacked)

        with open(self.reportfile, 'w') as logfile:
            logfile.write("************************************************************************\n")
            logfile.write("Script started on %s\nScript completed on %s\nScript took %s minutes (%s hours)\n" % (self.times[0], self.times[1], self.times[2], self.times[2] / 60))
            logfile.write("************************************************************************\n")
            logfile.write("\nAffected users[%s]:\n" % (self.user_count))
        
            for i in sorted(self.users):
                logfile.write("%s\n" % (i))
        
            logfile.write("\nCompromised files[%s]:\n" % (self.file_count))
            for i in self.hacked:
                logfile.write("%s\n" % (i))


    def MailReport(self, *args):
        """ Sends the report to the specified e-mail addresses """

        self.reportfile = args[0]
        self.from_mail = args[1]
        self.reply_mail = self.from_mail
        self.to_mail = args[2]
        self.cc_mail = args[3]
        self.our_header = args[4]
        self.hacked = args[5]
        self.users = set()
        self.sendmail_location = subprocess.Popen(['which', 'sendmail'], stdout = subprocess.PIPE).communicate()[0].strip()

        for i in self.hacked:
            self.user = i.split("/")
            self.users.add(self.user[2])

        self.user_count = len(self.users)

        self.p = os.popen("%s -t" % self.sendmail_location, "w")
        self.p.write("From: %s\n" % (self.from_mail))
        self.p.write("To: %s\n" % (self.to_mail))
        self.p.write("CC: %s\n" % (self.cc_mail))
        self.p.write("Reply-to: %s\n" % (self.reply_mail))
        self.p.write("Subject: Shell Finder identified %s compromised accounts on %s\n" % (self.user_count, self.hostname))
        self.p.write(self.our_header)
        self.p.write("\n")

        with open(self.reportfile, 'r') as logfile:
            while True:
                self.contents = logfile.read()
                if not self.contents:
                    break
                self.p.write(self.contents)
        self.p.close()
