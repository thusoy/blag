FROM debian:stretch

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  python-dev \
  python-pip \
  python-virtualenv \
  python-setuptools \
  libpq-dev \
  libjpeg-dev \
  libwebp-dev \
  zlib1g-dev \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*

COPY setup.py requirements.txt prod-requirements.txt /app/

RUN python -m virtualenv /app/venv

RUN /app/venv/bin/pip install --no-cache-dir -r prod-requirements.txt --no-dependencies --no-binary :all:

RUN apt-get purge gcc -y && apt-get autoremove -y

RUN useradd --home-dir /app gunicorn

COPY blag /app/blag
COPY .tmp/static /app/static

USER gunicorn

EXPOSE 5000

ENTRYPOINT ["/app/venv/bin/gunicorn"]

CMD ["blag:create_app()","-b", "127.0.0.1:5000"]
