#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *


SITEURL = 'http://blog.yyx.me'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS=['sitemap',]
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "yyxblog"
#CNZZ_ANALYTICS = "1253039383"
# SWIFTYPE_SEARCH = "XwpC765YWzV58fvrdjoQ"
# WEIBOSHOW = "1085956311"
GOOGLE_ANALYTICS = "UA-64342434-1"

