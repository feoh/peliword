#!/usr/bin/env python
import glob
import os
import markdown
import pelican
import requests
import pprint
import json
import html

from peliword_config import pelican_blog_dir, wp_client_secret

wp_api_base = 'https://public-api.wordpress.com/rest/v1.1/sites/feohorg.wordpress.com'

settings = pelican.settings.read_settings()
mdr = pelican.readers.MarkdownReader(settings)

wp_posts_response = requests.get(wp_api_base + "/posts" )
wp_posts_json = wp_posts_response.text
wp_resp = json.loads(wp_posts_json)

wp_posts = wp_resp['posts']

wp_titles = [ html.unescape(wp_post['title']) for wp_post in wp_posts ]

print(wp_titles)
# pprint.pprint(wp_posts)


if not os.path.exists(pelican_blog_dir):
    print("Not a valid Pelican blog directory: {}".format(pelican_blog_dir))

glob_path = pelican_blog_dir + "/content/*.md"
for post in glob.glob(glob_path):
    mda = mdr.read(post)
    headers = mda[1]
    title = headers['title']
    if title not in wp_titles:
        print("title: {}".format(title))
