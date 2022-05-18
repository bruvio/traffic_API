docker build -t python-django-nginx:latest \
  -f docker/nginx/Dockerfile .
docker build -t python-django-python:latest \
  -f docker/python/Dockerfile .

(2) Create ECR repositories:

aws ecr create-repository --repository-name python-django-nginx \
  --query 'repository.repositoryUri' --output text
aws ecr create-repository --repository-name python-django-python \
  --query 'repository.repositoryUri' --output text

(3) Login to Docker registry (ECR):

$(aws ecr get-login --no-include-email)

(4) Tag Docker images:

docker tag python-django-nginx:latest \
111111111111.dkr.ecr.eu-west-1.amazonaws.com/\
python-django-nginx:latest
docker tag python-django-python:latest \
111111111111.dkr.ecr.eu-west-1.amazonaws.com/\
python-django-python:latest

(5) Push Docker images:

docker push \
111111111111.dkr.ecr.eu-west-1.amazonaws.com/\
python-django-nginx:latest
docker push \
111111111111.dkr.ecr.eu-west-1.amazonaws.com/\
python-django-python:latest
