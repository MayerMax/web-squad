import re

from bottle import template

src_finder = re.compile(r'src=&quot;([^;]+)&quot;')
img_finder = re.compile(r'&lt;\s?img\s+.+&gt;')


class SafeEscape:
    SAFE_TAGS = {'b', 'i', 'em', 'strong'}

    def __init__(self):
        self.wrappers = {
            'img': 'class="w3-card" style="max-height: 400px; max-width: 400px;"'
        }

    def __call__(self, string):
        for tag in self.SAFE_TAGS:
            string = re.sub('&lt;{}&gt;'.format(tag), '<{}>'.format(tag), string)
            string = re.sub('&lt;/{}&gt;'.format(tag), '</{}>'.format(tag), string)
        print(self.image_wrapper(string.replace('\r\n', '<br>')))

        return self.image_wrapper(string.replace('\r\n', '<br>'))

    def image_wrapper(self, escaped_html):
        copy = escaped_html
        for match in img_finder.findall(escaped_html):

            path = src_finder.findall(match)
            if path:
                path = path[0]
                copy = copy.replace(match, '<img src="{}">'.format(path))
        return copy


s = '&lt;img src=&#039;https://cdn.images.express.co.uk/img/dynamic/67/590x/real-madrid-s-isco-518426.jpg&#039;&gt;'