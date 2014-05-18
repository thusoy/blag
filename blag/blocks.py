from bs4 import BeautifulSoup
from flask import url_for
from jinja2 import Template
from markdown import markdown
from logging import getLogger

_logger = getLogger('blag.renderers')


class BaseRenderer(object):

    def render_md(self, md):
        return markdown(md, ['smarty'])


    def render(self, data, prettify=True):
        raw_html = self.render_html(data)
        if prettify:
            pretty_html = BeautifulSoup(raw_html).prettify()
            return pretty_html
        return raw_html


class TextRenderer(BaseRenderer):

    def render_html(self, data):
        _logger.info("Self data: %s", data)
        return self.render_md(data['text'])


class QuoteRenderer(BaseRenderer):

    quote_template = """
        <blockquote cite="{{ cite }}">
            {{ quote }}
            <footer>
            &mdash; {{ cite }}
            </footer>
    """

    def render_html(self, data):
        quote_lines = data['text'].split('\n')
        quote_lines = [line.lstrip('> ') for line in quote_lines]
        quotation_md = self.render_md('\n'.join(quote_lines))
        template = Template(self.quote_template)
        quote = template.render(cite=data['cite'], quote=quotation_md)
        return quote


class ImageRenderer(BaseRenderer):

    image_template = """
        <a href="{{ img_url }}">
            <img src="{{ img_url }}">
        </a>
    """

    def render_html(self, data):
        template = Template(self.image_template)
        return template.render(img_url=url_for('images', filename=data['imageUrl']))


class VideoRenderer(BaseRenderer):

    video_height = 390
    video_width = 640

    vimeo_embed_code = """
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
    """

    youtube_embed_code = """
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
    """

    def render_html(self, data):
        properties = {name: getattr(self, name) for name in dir(self) if not name.startswith('__')}
        if data['source'] == 'vimeo':
            template = Template(self.vimeo_embed_code)
        elif data['source'] == 'youtube':
            template = Template(self.youtube_embed_code)
        return template.render(video_id=data['remote_id'], **properties)


class GalleryRenderer(BaseRenderer):

    gallery_template = """
        {% for image in gallery %}
            <a href="{{ url_for('images', filename=image['imageUrl']) }}">
                <img src="{{ url_for('images', filename=image['imageUrl']) }}">
            </a>
        {% endfor %}
    """

    def render_html(self, data):
        template = Template(self.gallery_template)
        images = [image['data'] for image in data]
        return template.render(gallery=images, url_for=url_for)


class TweetRenderer(BaseRenderer):

    embed_code = """
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
    """

    def render_html(self, data):
        _logger.info(data)
        template = Template(self.embed_code)
        return template.render(tweet_id=data['id'])


class HeadingRenderer(BaseRenderer):

    heading_class = 'subheading'
    heading_tag = 'h2'

    template = """
        <{{ heading_tag }}
            class="{{ heading_class }}">
            {{ heading }}
        </{{ heading_tag }}>
    """

    def render_html(self, data):
        template = Template(self.template)
        return template.render(
            heading_class=self.heading_class,
            heading_tag=self.heading_tag,
            heading=data['text']
        )


class SourcedQuoteRenderer(BaseRenderer):

    sourced_quote_template = """
        <blockquote cite="{{ source }}">
            {{ quote }}

            <footer>
                &mdash; <a href="{{ source }}">{{ author }}</a>
            </footer>
        </blockquote>
    """

    def render_html(self, data):
        template = Template(self.sourced_quote_template)
        context = {
            'author': data['author'],
            'source': data['source'],
            'quote': data['text'],
        }
        return template.render(**context)


def render_blocks(blocks):
    html_parts = []
    for block in blocks:
        html_parts.append(render_block(block))
    return '\n'.join(html_parts)


def render_block(block):
    print 'Rendering block: %s' % block
    renderer_map = {
        'text': TextRenderer,
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
