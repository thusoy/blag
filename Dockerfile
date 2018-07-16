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

COPY blag /app/blag
COPY setup.py requirements.txt prod-requirements.txt /app/
COPY .tmp/static /app/static

RUN python -m virtualenv /app/venv

RUN /app/venv/bin/pip install --no-cache-dir -r prod-requirements.txt --no-dependencies --no-binary :all:

RUN apt-get purge gcc -y && apt-get autoremove -y

RUN useradd --create-home --home-dir /app gunicorn

USER gunicorn

EXPOSE 5000

ENTRYPOINT ["/app/venv/bin/gunicorn"]

CMD ["blag:create_app()","-b", "0.0.0.0:5000"]
