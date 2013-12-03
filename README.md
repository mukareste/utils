Pentest Utils
=====

A repository of some custom scripts used for penetration testing and incident response by [MTR Design](http://mtr-design.com) testers.

Contents:
-----

* README.md - This file
* pentest/enumerate_wp_users.py - Enumerates WordPress users using the author tag.
* pentest/findvhosts.py - Enumerates virtual hosts on the same IP address. More information on [Web Security Watch](http://www.websecuritywatch.com/findvhosts-py-update/).
* pentest/bingbong.py - Search Bing via their API.
* pentest/extract_links.py - Extract the links from a given URL.
* pentest/ProgressBar.py - A progress bar class.
* pentest/ipinformation prints network information for the locally assigned IP addresses.
* pentest/extract_links.pl Extract the links from a given URL.
* pentest/dehash.py - Searches http://md5-decrypter.com/ for a password hash.
* pentest/smtp.py - Checks the validity of an e-mail address.
* pentest/recon.py - New version of findvhosts.py. Enter your Bing API key and eWhois login credentials in pentest/csc_utils/recon/enum.py.
* incident_response/malfind_search.py - Searches malc0de and threat expert for hashes of potentially malicious files.
* incident_response/bigsis.sh - monitors the contents of a directory and sends e-mail notifications. Run from cron.
* incident_response/shell_finder.py - Uses clamav and grep to check all accounts on a Cpanel server for malicious files. DB is not included.
* incident_response/shell_finder-2.0/shell_finder.py - New version of shell_finder. Clamav has been removed - too many false positives.
* incident_response/humanize_audit_log.py - Converts epoch times to human-readable dates in an the audit.log files. Pipe the file through the script.
* incident_response/humanize_bash_history_file.py - Converts epoch times to human-readable dates in a .bash_history file. Pipe the file through the script.
* misc/epoch.py - Converts epoch time to date/time.
* misc/get_fb_status_likes.py - Gets the names of the people, who liked a post on a Facebook page.
