from bs4 import BeautifulSoup
from flask import url_for
from jinja2 import Template
from markdown import markdown
from logging import getLogger
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name
import pygments

_logger = getLogger('blag.renderers')


class BaseRenderer(object):
    """ Parent of all renderers. Implements defaults for all methods required.

    Most renderes only need to subclass this class and add an attribute `template` (an instance of
    `jinja2.Template`), and optionally `parse_data`, to clean up or change names on the variables
    sent to the template.

    If full control of the rendering is required, override `render_html` and return the finished
    html.
    """

    template = Template('{{ text }}')

    def render_md(self, md):
        md = md.replace('(tm)', '&trade;')
        return markdown(md, ['smarty'])


    def render(self, data, prettify=False):
        raw_html = self.render_html(data)
        if prettify:
            pretty_html = BeautifulSoup(raw_html).prettify()
            return pretty_html
        return raw_html


    def render_html(self, data):
        """ Renders the template with the data, after first parsing the data using the renderers
        `parse_data` implementation.
        """
        parsed_data = self.parse_data(data)
        return self.template.render(parsed_data)


    def parse_data(self, data):
        return data


class TextRenderer(BaseRenderer):

    def render_html(self, data):
        _logger.info("Self data: %s", data)
        return self.render_md(data['text'])


class QuoteRenderer(BaseRenderer):

    template = Template("""
        <blockquote cite="{{ cite }}">
            {{ quote }}
            <footer>
            &mdash; {{ cite }}
            </footer>
    """)

    def parse_data(self, data):
        quote_lines = data['text'].split('\n')
        quote_lines = [line.lstrip('> ') for line in quote_lines]
        quotation_md = self.render_md('\n'.join(quote_lines))
        return {'cite': data['cite'], 'quote': quotation_md}


class ImageRenderer(BaseRenderer):

    template = Template("""
        <a href="{{ img_url }}">
            <img src="{{ img_url }}">
        </a>
    """)

    def parse_data(self, data):
        return dict(img_url=url_for('images', filename=data['imageUrl']))


class VideoRenderer(BaseRenderer):

    video_height = 390
    video_width = 640

    vimeo_embed_code = Template("""
        <iframe src="//player.vimeo.com/video/{{ video_id }}"
            {% if video_width %}
                width="{{ video_width }}"
            {% endif %}
            {% if video_height %}
                height="{{ video_height }}"
            {% endif %}
            frameborder="0"
            webkitallowfullscreen
            mozallowfullscreen
            allowfullscreen
        />
    """)

    youtube_embed_code = Template("""
        <iframe src="http://www.youtube.com/embed/{{ video_id }}"
            id="ytplayer"
            type="text/html"
            {% if video_width %}
                width="{{ video_width }}"
            {% endif %}
            {% if video_height %}
                height="{{ video_height }}"
            {% endif %}
            frameborder="0"
        />
    """)

    def render_html(self, data):
        properties = {name: getattr(self, name) for name in dir(self) if not name.startswith('__')}
        if data['source'] == 'vimeo':
            template = self.vimeo_embed_code
        elif data['source'] == 'youtube':
            template = self.youtube_embed_code
        return template.render(video_id=data['remote_id'], **properties)


class GalleryRenderer(BaseRenderer):

    template = Template("""
        {% for image in gallery %}
            <a href="{{ url_for('images', filename=image['imageUrl']) }}">
                <img src="{{ url_for('images', filename=image['imageUrl']) }}">
            </a>
        {% endfor %}
    """)

    def parse_data(self, data):
        images = [image['data'] for image in data]
        return {'gallery': images, 'url_for': url_for}


class TweetRenderer(BaseRenderer):

    template = Template("""
        <blockquote
            id="twttr-id-{{ tweet_id }}">
        </blockquote>
        <script>
            window.twttr = (function (d,s,id) {
              var t, js, fjs = d.getElementsByTagName(s)[0];
              if (d.getElementById(id)) return; js=d.createElement(s); js.id=id; js.async=true;
              js.src="//platform.twitter.com/widgets.js"; fjs.parentNode.insertBefore(js, fjs);
              return window.twttr || (t = { _e: [], ready: function(f){ t._e.push(f) } });
            }(document, "script", "twitter-wjs"));

            twttr.ready(function(){
                twttr.widgets.createTweet(
                    {{ tweet_id }},
                    document.getElementById("twttr-id-{{ tweet_id }}")
                );
            });
        </script>
    """)

    def parse_data(self, data):
        return {'tweet_id': data['id']}


class HeadingRenderer(BaseRenderer):

    heading_class = 'subheading'
    heading_tag = 'h2'

    template = Template("""
        <{{ heading_tag }}
            class="{{ heading_class }}">
            {{ heading }}
        </{{ heading_tag }}>
    """)

    def parse_data(self, data):
        return dict(
            heading_class=self.heading_class,
            heading_tag=self.heading_tag,
            heading=data['text']
        )


class SourcedQuoteRenderer(BaseRenderer):

    template = Template("""
        <blockquote cite="{{ source }}">
            {{ text }}

            <footer>
                &mdash; <a href="{{ source }}">{{ author }}</a>
            </footer>
        </blockquote>
    """)


class CodeRenderer(BaseRenderer):

    def parse_data(self, data):
        lexer = get_lexer_by_name(data.get('language', 'bash'))
        formatter = get_formatter_by_name('html')
        return dict(text=pygments.highlight(data['text'], lexer, formatter))


def render_blocks(blocks):
    html_parts = []
    for block in blocks:
        html_parts.append(render_block(block))
    return '\n'.join(html_parts)


def render_block(block):
    renderer_map = {
        'code': CodeRenderer,
        'text': TextRenderer,
        'markdown': TextRenderer,
        'quote': QuoteRenderer,
        'image': ImageRenderer,
        'video': VideoRenderer,
        'gallery': GalleryRenderer,
        'tweet': TweetRenderer,
        'heading': HeadingRenderer,
        'sourced_quote': SourcedQuoteRenderer,
    }
    renderer_class = renderer_map.get(block['type'], TextRenderer)
    renderer = renderer_class()
    return renderer.render(block['data'])
