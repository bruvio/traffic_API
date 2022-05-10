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

I created a ngnix proxy that can be used as Django's built-in webserver is not designed for production use.
Nginx is designed to be fast, efficient, and secure, so it's a better choice to handle incoming web requests when your website is on the public Internet and thus subject to large amounts of traffic (if you're lucky and your site takes off) 

## run the code

to run the code first create a virtual enviroment. I used [poetry](https://python-poetry.org/docs/) to manage dependencies.

```
poetry install
poetry shell
pytest
```



`docker-compose build` (takes lots of time to build numpy and pandas wheels!)
then 

`docker-compose up`

and finally open a browser and navigate to `localhost:8000`

if you prefer to run locally simulating the production enviroment with the proxy run
`docker-compose -f docker-compose-proxy.yml up` and then navigate to 

`127.0.0.0:8000`


## Deployment to AWS

to deploy to AWS I chose to use Gitlab CI and terraform in conjuction with docker.
to do so I created a little script with a set of instruction to create policies, users, and some resources that the infrastructure needs. 


just run `./aws_scripts.sh`








