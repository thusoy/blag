FROM debian:stretch as build

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  python3-dev \
  python3-virtualenv \
  libpq-dev \
  libjpeg-dev \
  libwebp-dev \
  zlib1g-dev \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*

COPY setup.py requirements.txt prod-requirements.txt /app/

RUN python3 -m virtualenv /app/venv -p $(which python3)

RUN /app/venv/bin/pip install --no-cache-dir -r prod-requirements.txt --no-dependencies --no-binary :all:

COPY setup.py .
RUN /app/venv/bin/pip install wheel
RUN /app/venv/bin/pip wheel --no-cache-dir -r requirements.txt --no-dependencies --no-binary :all:
RUN /app/venv/bin/python setup.py bdist_wheel


# Build the minimal image that should be distributed
FROM debian:stretch-slim as prod

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-virtualenv \
    libpq5 \
    libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /app/*.whl ./
COPY --from=build /app/dist/* .
COPY blag /app/blag
COPY .tmp/static /app/static
COPY setup.py /app/
ENV BLAG_STATIC_FILES=/app/static

RUN python3 -m virtualenv /app/venv -p $(which python3)
RUN /app/venv/bin/pip install *.whl gunicorn .
RUN apt-get purge python3-virtualenv -y && apt-get autoremove -y

RUN useradd --create-home --home-dir /app gunicorn
USER gunicorn

EXPOSE 5000

ENTRYPOINT ["/app/venv/bin/gunicorn"]

CMD ["blag:create_app()","-b", "127.0.0.1:5000"]
