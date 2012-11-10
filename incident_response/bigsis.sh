#!/bin/bash

#       bigsis.sh 0.1/2011 - Watches a directory from changes. Could be started from cron on each hour. Sends an e-mail with the diffs between the file listings.
#
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


#
# Configure the variables below
#

WATCH_DIR="$1"
DIFF_DIR=""
DIFF_FILE="$DIFF_DIR/listing.txt"
CHANGES_FILE="$DIFF_DIR/changes.txt"
HOST="$(/bin/hostname)"
SEND_MAIL=`which sendmail`
MAIL_ADDRESS=""

if [ -d "$WATCH_DIR" ] && [ -w "$DIFF_DIR" ];then
    if [ -e "$DIFF_FILE" ];then
        mv $DIFF_FILE $DIFF_FILE.prev
    fi
    ls -dAlR $(find $WATCH_DIR) > $DIFF_FILE
    diff -cN $DIFF_FILE.prev $DIFF_FILE > $CHANGES_FILE
    MESSAGE=$(cat $CHANGES_FILE)
else
    echo "Watch directory not specified or cannot write to $DIFF_FILE."
    exit 1
fi

if [ -s "$CHANGES_FILE" ];then
    echo -e "To: $MAIL_ADDRESS=\nFrom: bigsister@$HOSTNAME\nSubject: Watched directory $WATCH_DIR changed on $HOST\n\n$MESSAGE" | sendmail -t
fi
