from bs4 import BeautifulSoup
from flask import url_for
from jinja2 import Template
from markdown import markdown
from logging import getLogger

_logger = getLogger('thusoy.renderers')

class BaseRenderer(object):

    markdown_extensions = [
        'smartypants(entities=named)',
    ]

    prettify = True

    def __init__(self, data):
        self.data = data


    def render_md(self, md):
        return markdown(md, self.markdown_extensions)


    def render(self):
        raw_html = self.render_html()
        if self.prettify:
            pretty_html = BeautifulSoup(raw_html).prettify()
            return pretty_html
        return raw_html


class TextRenderer(BaseRenderer):

    def render_html(self):
        _logger.info("Self data: %s", self.data)
        return self.render_md(self.data['text'])


class QuoteRenderer(BaseRenderer):

    quote_template = """
        <blockquote cite="{{ cite }}">
            {{ quote }}
            <footer>
            &mdash; {{ cite }}
            </footer>
    """

    def render_html(self):
        quote_lines = self.data['text'].split('\n')
        quote_lines = [line.lstrip('> ') for line in quote_lines]
        quotation_md = self.render_md('\n'.join(quote_lines))
        template = Template(self.quote_template)
        quote = template.render(cite=self.data['cite'], quote=quotation_md)
        return quote


class ImageRenderer(BaseRenderer):

    image_template = """
        <a href="{{ img_url }}">
            <img src="{{ img_url }}">
        </a>
    """

    def render_html(self):
        template = Template(self.image_template)
        return template.render(img_url=url_for('images', filename=self.data['imageUrl']))


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

    def render_html(self):
        properties = {name: getattr(self, name) for name in dir(self) if not name.startswith('__')}
        if self.data['source'] == 'vimeo':
            template = Template(self.vimeo_embed_code)
        elif self.data['source'] == 'youtube':
            template = Template(self.youtube_embed_code)
        return template.render(video_id=self.data['remote_id'], **properties)


class GalleryRenderer(BaseRenderer):

    gallery_template = """
        {% for image in gallery %}
            <a href="{{ url_for('images', filename=image['imageUrl']) }}">
                <img src="{{ url_for('images', filename=image['imageUrl']) }}">
            </a>
        {% endfor %}
    """

    def render_html(self):
        template = Template(self.gallery_template)
        images = [image['data'] for image in self.data]
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

    def render_html(self):
        _logger.info(self.data)
        template = Template(self.embed_code)
        return template.render(tweet_id=self.data['id'])


class HeadingRenderer(BaseRenderer):

    heading_class = 'subheading'
    heading_tag = 'h2'

    template = """
        <{{ heading_tag }}
            class="{{ heading_class }}">
            {{ heading }}
        </{{ heading_tag }}>
    """

    def render_html(self):
        template = Template(self.template)
        return template.render(
            heading_class=self.heading_class,
            heading_tag=self.heading_tag,
            heading=self.data['text']
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

    def render_html(self):
        template = Template(self.sourced_quote_template)
        context = {
            'author': self.data['author'],
            'source': self.data['source'],
            'quote': self.data['text'],
        }
        return template.render(**context)
