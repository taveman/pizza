FROM python:3.7-alpine
MAINTAINER Yuiry

ENV PYTHONUNBUFFERED 1

RUN apk add \
    musl-dev \
    postgresql-libs \
    libc-dev

RUN apk add --update --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    postgresql-dev \
    linux-headers

RUN pip install --no-binary :all: psycopg2

RUN apk del --no-cache .build-deps

RUN mkdir /pizza
WORKDIR /pizza

COPY ["/", "/pizza"]

RUN adduser -D pizza_user
USER pizza_user