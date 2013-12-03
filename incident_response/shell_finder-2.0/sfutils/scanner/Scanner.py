import os
import subprocess

class SearchShells(object):
    """ Shell Scanners """

    def __init__ (self):
        """ Constructor """


    def GrepForShells(self, *args):
        """ Grep for shells """

        self.shelled = set()
        self.notshelled = set()
        self.accounts = args[0]
        self.grep_str = args[1]
        self.whitelist_file = args[2]
        self.nice = subprocess.Popen(['which', 'nice'], stdout = subprocess.PIPE).communicate()[0].strip()
        self.grepper = subprocess.Popen(['which', 'grep'], stdout = subprocess.PIPE).communicate()[0].strip()

        for acct in self.accounts:
            self.scan_path = "/home/%s/public_html/" % (acct)
            if not os.path.exists(self.scan_path):
                continue
            self.output = subprocess.Popen([self.nice, "-n", "19", self.grepper, "-srilFf", self.grep_str, self.scan_path], stdout = subprocess.PIPE).communicate()[0]
            self.inf = self.output.split("\n")
            for line in self.inf:
                if not line: continue
                self.shelled.add(line)

        with open (self.whitelist_file, 'r') as whitelist:
            for line in whitelist.readlines():
                self.notshelled.add(line.rstrip())

        for w in self.notshelled:
            self.shelled.discard(w)

        return sorted(self.shelled)
