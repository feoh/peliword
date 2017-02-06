#!/usr/bin/env python
import glob
import os
import markdown
import pelican
import requests
import pprint
import json
import html
from pelican.utils import SafeDatetime

from peliword_config import pelican_blog_dir, wp_client_secret

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
    pprint.pprint(pelican_headers)    
    pelican_tag_list = pelican_headers['tags']
    pelican_tags = [ tag.name for tag in pelican_tag_list ].
    print("tags: {}".format(pelican_tags))

    next
    pelican_body = mda[0]
    if pelican_headers['title'] not in wp_titles:
        print("Posting title: {}".format(pelican_headers['title']))
        headers = { 'authorization', 'Bearer {}'.format(wp_client_secret)}

        test_post = "Date: {}\nTitle: {}\nAuthor: {}\ntags: {}\ncategory: {}\n".format(pelican_headers['date'],
                                                                                       pelican_headers['title'],
                                                                                       pelican_headers['author'],
                                                                                       pelican_headers['tags'],
                                                                                       pelican_headers['category'])
        print(test_post)

        
        # wp_post_response = requests.post(wp_api_base + "/posts/new", data = {'title': pelican_headers['title'],
        #                                                                      'author': pelican_headers['author'],
        #                                                                      'tags': pelican_headers['tags'],
        #                                                                      'date': pelican_headers['date'],
        #                                                                      'category': pelican_headers['category'],
        #                                                                      'content' : pelican_body})
        #pprint.pprint(wp_post_response)
