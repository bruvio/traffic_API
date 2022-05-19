FROM bruvio/alpine-postgres-pandas-numpy:poetry
LABEL maintainer="bruno.viola@pm.me"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# set up the psycopg2
RUN python -c "import pandas as pd; print('\n \n Pandas version is ',pd.__version__)"
RUN mkdir /code
WORKDIR /code

COPY . /code/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi



ENV PATH="/scripts:${PATH}"




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
