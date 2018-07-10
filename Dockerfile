FROM debian:stretch

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  python-dev \
  python-pip \
  python-setuptools \
  libpq-dev \
  libjpeg-dev \
  libwebp-dev \
  zlib1g-dev \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*

COPY blag /app/blag
COPY requirements.txt /app
COPY .tmp/static /app/static

RUN pip install --no-cache-dir -r requirements.txt --no-dependencies --no-binary :all:

RUN pip install gunicorn

RUN apt-get purge gcc -y && apt-get autoremove -y

RUN useradd --create-home --home-dir /app gunicorn

USER gunicorn

EXPOSE 5000

ENTRYPOINT ["gunicorn"]

CMD ["blag:create_app()","-b", "0.0.0.0:5000"]
