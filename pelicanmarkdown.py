import markdown
import pelican
import requests
import pprint

settings = pelican.settings.read_settings()
mdr = pelican.readers.MarkdownReader(settings)
mda = mdr.read("/home/feoh/src/personal/blindnotdumb/content/Bacon+Microwave=Jerky.md")
headers = mda[1]
print("title: {}".format(headers['title']))

