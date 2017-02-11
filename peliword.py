#!/usr/bin/env python
import glob
import os
import markdown
import pelican
import requests
import pprint
import json
import html
import logging
from pelican.utils import SafeDatetime
from peliword_config import pelican_blog_dir, wp_client_secret
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

wp_api_base = 'https://public-api.wordpress.com/rest/v1.1/sites/feohorg.wordpress.com'

settings = pelican.settings.read_settings()
mdr = pelican.readers.MarkdownReader(settings)

wp_get_posts_response = requests.get(wp_api_base + "/posts" )
wp_get_posts_json = wp_get_posts_response.text
wp_get_resp = json.loads(wp_get_posts_json)

wp_get_posts = wp_get_resp['posts']

wp_titles = [ html.unescape(wp_post['title']) for wp_post in wp_get_posts ]

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
    if pelican_headers['title'] not in wp_titles:
        print("Posting title: {}".format(pelican_headers['title']))
        print("wp_client_secret={}".format(wp_client_secret))
        bearer = "Bearer {}".format(wp_client_secret)
        headers = {}
        headers['authorization'] = bearer

        print("headers:")
        pprint.pprint(headers)

        wp_post_response = requests.post(wp_api_base + "/posts/new", headers = headers, data = wp_post_headers)
        pprint.pprint(wp_post_response)
        break;


