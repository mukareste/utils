#!/usr/bin/env python

"""
get_fb_status_likes.py 0.1 / 2013 by mitchell <dimitar.ivanov@mtr-design.com>.
"""
#
#       Copyright (c) 2013, MTR Design, Ltd. (mtr-design.com)
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

import urllib
import json
import argparse

accessToken = ''


def get_Options():
    """
    Parses the command line arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('post_id', help="The numeric ID of the post", type=str)
    args = parser.parse_args()
    return args.post_id

def get_FB_Likes(postID):
    """
    Get those likes
    """

    likeNames = set()
    requestURL = "https://graph.facebook.com/{}/likes?limit=9999&{}".format(postID, accessToken)

    print("Getting the number of likes for post ID {}...\n").format(postID)

    read = urllib.urlopen(requestURL).read()
    read = json.loads(read)

    try:
        data = read['data']
        for i in data:
            likeNames.add(i.values()[1].encode('utf-8'))
    
    except:
        for i in read.values():
            for k,v in i.items():
                print("{0}: {1}").format(k.title(), v)

    return likeNames

def main():
    """
    The main function
    """

    postID = get_Options()
    likes = get_FB_Likes(postID)

    for like in likes:
        print(like)

    print("\nFound {0} likes for post ID {1}.").format(len(likes), postID)

if __name__ == "__main__":
    main()
