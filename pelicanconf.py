#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals
import datetime

AUTHOR = u'YYX'
SITENAME = u'YYX\'s Website'
SITEURL = '' # used by links
SITEDOMAIN = 'yyx.me'

PATH = 'content'
OUTPUT_PATH = 'docs' # for Github, also need to change path in Makefile and develop_server.sh

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github', 'https://github.com/GreatYYX'),
          ('instagram', 'https://www.instagram.com/debug.dog/'),
          ('500px', 'https://500px.com/yyx'),
          ('weibo', 'https://weibo.com/p/1005051085956311'),
          ('rss', SITEURL + '/feeds/all.atom.xml'),
          # ('linkedin', '#'),
          )

CC = 'https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en'

# only use MENUITEMS to control what to display on menu
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_LIST = False
DISPLAY_ARCHIVES_LIST = False
DISPLAY_PAGES_ON_MENU = False
MENUITEMS = (
	('Posts','/posts/', False),
	('Gallery', '/gallery/', False),
	# ('Gallery', 'http://photo.yyx.me', True),
	('About','/about/', False),
)

DIRECT_TEMPLATES = ['index', 'categories', 'tags', 'archives'] # 'authors' 

# pagination
DEFAULT_PAGINATION = 6
PAGINATED_TEMPLATES = {
	'index': None, 'tag': None, 'category': None, 'author': None, 'archives': DEFAULT_PAGINATION
}
PAGINATION_PATTERNS = (
    (1, '{url}', '{save_as}'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

USE_FOLDER_AS_CATEGORY = True
PAGE_PATHS = ['_pages']
STATIC_PATHS = ['statics', 'extra/robots.txt', 'extra/CNAME', 'extra/photos.json']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/CNAME': {'path': 'CNAME'},
    'extra/photos.json': {'path': 'photos.json'}
}
# MD_EXTENSIONS = ['extra']

# index
INDEX_SAVE_AS = 'index.html'
# articles & archives (use it as article list)
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'
ARCHIVES_URL = 'posts/'
ARCHIVES_SAVE_AS = 'posts/index.html'
# tags
TAG_URL = 'tags/{slug}/'
TAG_SAVE_AS = 'tags/{slug}/index.html'
TAGS_URL = 'tags/'
TAGS_SAVE_AS = 'tags/index.html'
# categories
CATEGORY_URL = 'categories/{slug}/'
CATEGORY_SAVE_AS = 'categories/{slug}/index.html'
CATEGORIES_URL = 'categories/'
CATEGORIES_SAVE_AS = 'categories/index.html'
# pages
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
PAGE_LANG_URL = '{slug}-{lang}/'
PAGE_LANG_SAVE_AS = '{slug}-{lang}/index.html'
# author
AUTHOR_URL = '' #only me
AUTHOR_SAVE_AS = '' #only me
AUTHOR_AVATAR = SITEURL + '/theme/images/cat_avatar.png'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

MINIMALXY_START_YEAR = '2014'
MINIMALXY_CURRENT_YEAR = datetime.date.today().strftime('%Y')
MINIMALXY_FAVICON = SITEURL + '/theme/images/favicon-32x32.png'

THEME = 'theme/MinimalXYZ'
THEME_STATIC_DIR = 'theme'

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS=['jinja2content',]
