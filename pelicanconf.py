#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import datetime

AUTHOR = u'yyx'
SITENAME = u'YYX\'s WEBlog'
SITEURL = ''

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
          ('weibo', 'https://weibo.com/p/1005051085956311'),
          # ('linkedin', '#'),
          )

CC = 'https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en'

MENUITEMS = (('Photo', 'http://photo.yyx.me'),)

DEFAULT_PAGINATION = 6

USE_FOLDER_AS_CATEGORY = True
PAGE_PATHS = ['_pages']
STATIC_PATHS = ['statics', 'extra/robots.txt', 'extra/CNAME']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/CNAME': {'path': 'CNAME'}
}
# MD_EXTENSIONS = ['extra']

ARTICLE_URL = 'posts/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{slug}.html'
PAGE_URL = 'pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'
PAGE_LANG_URL = 'pages/{slug}-{lang}.html'
PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}.html'
AUTHOR_SAVE_AS = '' #only me
AUTHOR_AVATAR = SITEURL + '/theme/images/cat_avatar.png'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

MINIMALXY_START_YEAR = '2014'
MINIMALXY_START_YEAR = datetime.date.today().strftime('%Y')

THEME = 'theme/MinimalXY'
THEME_STATIC_DIR = 'theme'

