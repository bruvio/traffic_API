FROM python:3.8-alpine
LABEL maintainer="bruno.viola@pm.me"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"



RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN apk add g++ postgresql-dev gcc python3-dev libffi-dev musl-dev zlib-dev jpeg-dev

RUN apk del .tmp-build-deps



RUN pip install --upgrade pip && pip install --no-cache-dir numpy pandas

ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}

RUN apk add --no-cache bash
