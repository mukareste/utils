#!/usr/bin/env python

"""
malfind_search.py 0.1 / 2012 by mitchell <mitchell@csc.bg>.
"""
#       Copyright (c) 2012, Cyber Security Consulting, Ltd. (csc.bg)
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

import urllib,urllib2,sys,os
from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser

if len(sys.argv) != 2:
	print 'Usage: %s <MD5 hash>' % sys.argv[0]
	sys.exit(1)
elif len(sys.argv[1]) !=32:
	print 'MD5 hash should be 32 characters, and you provided %d.' % len(sys.argv[1])
       	sys.exit(2)


hash = sys.argv[1]

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return '\t'.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def md5_search(site):
	user_agent = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.12) Gecko/20101027 Ubuntu/10.10 (maverick) Firefox/3.6.12'
	headers = { 'User-Agent' : user_agent }

	url = site + hash
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	results_page = response.read()

	soup = BeautifulSoup(results_page)
	results = soup.findAll('tr')
	for result in results:
		text_result = str(result)
		print strip_tags(text_result)

def main():
	print "\nSearching malc0de database...\n\n"
	md5_search('http://malc0de.com/database/index.php?MD5=on&search=')
	print "\nTrying to pull Threat Expert report...\n"
	os.system("./threatex_submit.pl %s" % hash)

if __name__ == '__main__':
    main()
