#!/usr/bin/env python
import glob
import os
import markdown
import pelican
import requests
import pprint
import sys
import json
import html
import logging
from pelican.utils import SafeDatetime
from peliword_config import pelican_blog_dir, wp_client_secret, wp_username, wp_password, wp_client_id
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

def get_wpcom_access_key():
    headers = {}
    headers['username'] = wp_username
    headers['password'] = wp_password
    headers['client_id'] = wp_client_id
    headers['client_secret'] = wp_client_secret
    headers['grant_type'] = 'password'
    wpcom_access_key_json = requests.post('https://public-api.wordpress.com/oauth2/token', headers=headers)
    pprint.pprint(wpcom_access_key_json)


# You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

wp_api_base = 'https://public-api.wordpress.com/rest/v1.1/sites/feohorg.wordpress.com'

#get_wpcom_access_key()
#sys.exit()

settings = pelican.settings.read_settings()
mdr = pelican.readers.MarkdownReader(settings)

wp_get_posts_response = requests.get(wp_api_base + "/posts" , params={'number':100})
wp_get_posts_json = wp_get_posts_response.text
wp_get_resp = json.loads(wp_get_posts_json)

wp_get_posts = wp_get_resp['posts']

wp_slugs = [ wp_post['slug'] for wp_post in wp_get_posts ]
pprint.pprint(wp_slugs)

if not os.path.exists(pelican_blog_dir):
    print("Not a valid Pelican blog directory: {}".format(pelican_blog_dir))

glob_path = pelican_blog_dir + "/content/*.md"
for post in glob.glob(glob_path):
    mda = mdr.read(post)
    pelican_headers = mda[1]
    # Pelican tags are actually objects. Process them down to a comma separated string of tags
    pelican_tag_objs = pelican_headers['tags']
    pelican_tag_list = [ tag.name for tag in pelican_tag_objs ]
    pelican_tags = ",".join(pelican_tag_list)

    wp_post_headers = pelican_headers
    wp_post_headers['tags'] = pelican_tags

    # Do the same for author.
    author = wp_post_headers['author'].name
    wp_post_headers['author'] = author

    
    pelican_body = mda[0]
    wp_post_headers['content'] = pelican_body

    if pelican_headers.get('slug','') not in wp_slugs:
        print("Posting title: {}".format(pelican_headers['title']))
        print("wp_client_secret={}".format(wp_client_secret))

#        wp_post_response = requests.post(wp_api_base + "/posts/new", headers = headers, data = wp_post_headers)
#        pprint.pprint(wp_post_response)



