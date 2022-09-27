FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1
WORKDIR /src

COPY ./requirements.txt /src

RUN \
  apk update && \
  apk add --virtual .build-deps \
    gcc g++ musl-dev linux-headers libxslt-dev \
    postgresql-libs postgresql-dev \
    python3-dev libffi-dev openssl-dev cargo make &&\
  apk add libpq &&\
  pip install -U setuptools pip &&\
  pip install -r requirements.txt &&\
  apk --purge del .build-deps

COPY ./src /src

COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["sh", "/docker-entrypoint.sh"]
