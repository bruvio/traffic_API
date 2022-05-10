# TRAFFIC API

The links below all give information on traffic count and major road data.

- Data: <https://storage.googleapis.com/dft-statistics/road-traffic/downloads/data-gov-uk/dft_traffic_counts_aadf_by_direction.zip>
- Metadata: <https://storage.googleapis.com/dft-statistics/road-traffic/all-traffic-data-metadata.pdf>
- General info: <https://roadtraffic.dft.gov.uk/about>

I will Create (and deploy) a web service/API that allows a user to navigate this data.

- The data is public so no authentication is required
- We will test it with one or more of python, javascript and curl
- The API structure is up to you
- Use Python or Node.js
- Use postgres for the database if you decide to use one

Requires
- [poetry](https://python-poetry.org/docs/)
- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)



## RUN the code locally

I created a Jupyter-Notebook `data_explore` that allows to visualize a bit the input data contained in `traffic_data.csv`
from here I defined a few models that allow to count and filter the data.



The app can be either run locally or inside a docker container.

A `Dockerfile` and a `docker-compose` files are provided.

I created a nginx proxy that can be used as Django's built-in webserver is not designed for production use.
Nginx is designed to be fast, efficient, and secure, so it's a better choice to handle incoming web requests when your website is on the public Internet and thus subject to large amounts of traffic (if you're lucky and your site takes off)

## run the code

to run the code first create a virtual environment. I used [poetry](https://python-poetry.org/docs/) to manage dependencies.

```
poetry install
poetry shell
```
or if you prefer 

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The first time is necessary to build the Docker image


`docker-compose build` (takes lots of time to build numpy and pandas wheels!)
then

`docker-compose up`

and finally open a browser and navigate to `localhost:8000`

if you prefer to run locally simulating the production environment with the proxy run
`docker-compose -f docker-compose-proxy.yml up` and then navigate to

`127.0.0.0:8000`

to run tests
```
docker-compose run --rm app sh -c "python manage.py wait_for_db && pytest API/tests"
```


## Deployment to AWS

to deploy to AWS I chose to use Gitlab CI and terraform in conjunction with docker.
to do so I created a little script with a set of instruction to create policies, users, and some resources that the infrastructure needs.


just run `./aws_scripts.sh`


if all the commands run successfully.
you are ready to run terraform.

Before doing so it is necessary to store as env variables AWS credentials.
I choose to use [aws-vault](https://github.com/99designs/aws-vault) as provides additional security creating ephemeral credentials that last maximum 12h.

In my case I will run

`aws-vault exec <myuser> --duration=12h`

or you can choose to export
```
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}
```


To make life easy in the `deploy` folder there is a makefile with some alias to run terraform commands.
Without going into the details. 
The users has to create a workspace (dev, staging, prod ...), initialize, plan and apply.

The `apply` command will create resources.


A deployment can also be triggered using the Gitlab CI. Here the user can tag releases and branches.

if everything is successfull you can access the API at 
`api.<workspace>.<yourdns>.net`


