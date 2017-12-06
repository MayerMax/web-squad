import re

from bottle import template


class SafeEscape:
    SAFE_TAGS = {'b', 'i', 'em', 'strong'}

    def __init__(self):
        pass

    def __call__(self, string):
        for tag in self.SAFE_TAGS:
            string = re.sub('&lt;{}&gt;'.format(tag), '<{}>'.format(tag), string)
            string = re.sub('&lt;/{}&gt;'.format(tag), '</{}>'.format(tag), string)
        return string.replace('\r\n', '<br>')