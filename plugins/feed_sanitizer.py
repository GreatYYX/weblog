"""Strip characters that are illegal in XML 1.0 from feed items.

Newer feedgenerator releases raise UnserializableContentError on control
characters (e.g. the raw 0x18/0x19 arrow bytes in IDA listings or the ASCII
column of hex dumps). Older releases wrote them silently. This keeps the
source Markdown untouched and only cleans what goes into the Atom/RSS feeds.
"""
import re

from pelican import signals

_XML_ILLEGAL = re.compile('[\x00-\x08\x0b\x0c\x0e-\x1f]')


def _clean(value):
    return _XML_ILLEGAL.sub('', value) if isinstance(value, str) else value


def sanitize_feed(context, feed):
    for item in feed.items:
        for key, value in item.items():
            item[key] = _clean(value)


def register():
    signals.feed_generated.connect(sanitize_feed)
