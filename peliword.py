#!/usr/bin/env python
import glob
import os
import markdown
import pelican
import requests
import pprint
from peliword_config import pelican_blog_dir, wp_client_secret

settings = pelican.settings.read_settings()
mdr = pelican.readers.MarkdownReader(settings)

if not os.path.exists(pelican_blog_dir):
    print("Not a valid Pelican blog directory: {}".format(pelican_blog_dir))

glob_path = pelican_blog_dir + "/content/*.md"
for post in glob.glob(glob_path):
    mda = mdr.read(post)
    headers = mda[1]
    pprint.pprint(headers)    
    print("title: {}".format(headers['title']))
    slug=headers['slug']
    print("slug: {}".format(slug))


