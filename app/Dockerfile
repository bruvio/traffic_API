FROM python:3.8-alpine
LABEL maintainer="bruno.viola@pm.me"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# set up the psycopg2



COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN apk add g++ postgresql-dev cargo gcc python3-dev libffi-dev musl-dev zlib-dev jpeg-dev
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN apk del .tmp-build-deps




RUN mkdir /code
WORKDIR /code

COPY . /code/

RUN chmod +x ./scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# RUN adduser --disabled-password --gecos '' user
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user
VOLUME /vol/web

CMD ["entrypoint.sh"]
