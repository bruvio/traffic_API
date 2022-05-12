FROM bruvio/alpine-postgres-pandas-numpy:3.8.12
LABEL maintainer="bruno.viola@pm.me"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# set up the psycopg2
RUN python -c "import pandas as pd; print('\n \n Pandas version is ',pd.__version__)"

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


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
