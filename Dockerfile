FROM nickgryg/alpine-pandas:3.8.13
LABEL maintainer="bruno.viola@pm.me"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# set up the psycopg2
RUN python -c "import pandas as pd; print(pd.__version__)"

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN apk add g++ postgresql-dev gcc python3-dev libffi-dev musl-dev zlib-dev jpeg-dev
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN apk del .tmp-build-deps

ENV PATH="/scripts:${PATH}"


RUN mkdir /code
WORKDIR /code

COPY . /code/

COPY ./scripts/ /scripts/
RUN chmod +x /scripts/*


RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# RUN adduser --disabled-password --gecos '' user
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user
VOLUME /vol/web

CMD ["entrypoint.sh"]
