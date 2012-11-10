Pentest Utils
=====

A repository of some custom scripts used for penetration testing and incident response by MTR Design (http://mtr-design.com) testers.

Contents:
-----

* README.md - This file
* pentest/enumerate_wp_users.py - Enumerates WordPress users using the author tag
* pentest/findvhosts.py - Enumerates virtual hosts on the same IP address. More information on http://www.websecuritywatch.com/findvhosts-py-update/
* pentest/extract_links.py - Extract the links from a given URL
* pentest/ProgressBar.py - A progress bar class
* pentest/ipinformation prints network information for the locally assigned IP addresses
* pentest/extract_links.pl Extract the links from a given URL
* pentest/dehash.py - Searches http://md5-decrypter.com/ for a password hash
* pentest/smtp.py - checks the validity of an e-mail address
* incident_response/malfind_search.py - Searches malc0de and threat expert for hashes of potentially malicious files
* incident_response/bigsis.sh - monitors the contents of a directory and sends e-mail notifications. Run from cron.
* misc/epoch.py - Converts epoch time to date/time
* incident_response/shell_finder.py - Uses clamav and grep to check all accounts on a Cpanel server for malicious files. DB is not included.
