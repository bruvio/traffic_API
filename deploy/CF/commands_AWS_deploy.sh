#!/bin/bash

IMAGE_NAME="traffic_api"
echo ""
echo "image name" $IMAGE_NAME
REPO_NAME="traffic_api"
echo ""
echo "repository name" $REPO_NAME


SERVICE_NAME="traffic_api"
# IMAGE_VERSION="v_"${BUILD_NUMBER}
IMAGE_VERSION=${1:-latest}
# IMAGE_VERSION="latest"
# TASK_FAMILY="dashboard"
CLUSTER="traffic_api"
REGION="us-east-1"

profile_name='AWS-cli'
accountid=$(aws sts get-caller-identity --query Account --output text)
DNS_name='brunoviola.com'


task_role='traffic_api' #ecsTaskExecutionRole
task_execution_role='ecsTaskExecutionRole'




docker build -t $IMAGE_NAME:$IMAGE_VERSION .

# exit
docker tag $IMAGE_NAME:$IMAGE_VERSION bruvio/$IMAGE_NAME:$IMAGE_VERSION

docker push $IMAGE_NAME:$IMAGE_VERSION bruvio/$IMAGE_NAME:$IMAGE_VERSION

# docker run -p 8080:80 tp_dashboard:latest
# docker-compose -f docker-compose_aws_credential.yml up --build -d
# docker container run -it --name dash tp_dashboard:external bash
# docker run -v ${HOME}/.aws/credentials:/root/.aws/credentials:ro -p 8080:80 tp_dashboard:latest
# exit


aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $accountid.dkr.ecr.$REGION.amazonaws.com

# create repository on AWS ECR

REPO_URI=$(aws ecr describe-repositories --repository-names "${REPO_NAME}" --query "repositories[0].repositoryUri" --output text 2>/dev/null || \
           aws ecr create-repository --repository-name "${REPO_NAME}"  --query "repository.repositoryUri" --output text)

echo ""
echo "repository uri" $REPO_URI

docker tag $IMAGE_NAME $REPO_URI:$IMAGE_VERSION

docker push $REPO_URI:$IMAGE_VERSION
# exit


# aws ecs register-task-definition --generate-cli-skeleton

echo ""
echo "creating task execution role"
aws iam wait role-exists --role-name $task_execution_role 2>/dev/null || \ aws iam --region $REGION create-role --role-name $task_execution_role \
  --assume-role-policy-document file://task-execution-assume-role.json || return 1

echo ""
echo "adding AmazonECSTaskExecutionRole Policy"
aws iam --region $REGION attach-role-policy --role-name $task_execution_role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy || return 1

echo ""
echo "adding AmazonEC2ContainerServiceRole Policy"
aws iam --region $REGION attach-role-policy --role-name $task_execution_role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole || return 1

echo ""
echo "creating task role"
aws iam wait role-exists --role-name $task_role 2>/dev/null || \
aws iam --region $REGION create-role --role-name $task_role \
  --assume-role-policy-document file://task-role.json

echo ""
echo "adding AmazonS3ReadOnlyAccess Policy"
aws iam --region $REGION attach-role-policy --role-name $task_role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess  || return 1




# exit
 #to be used only at the very beginning when configuring ecs-cli
# ecs-cli configure profile --access-key AWS_ACCESS_KEY_ID --secret-key AWS_SECRET_ACCESS_KEY --profile-name $profile_name


echo ""
echo "if service up turn it down first"
ecs-cli down --force --cluster-config $CLUSTER --ecs-profile $profile_name

echo ""
echo "configuring cluster"
# Create a cluster configuration, which defines the AWS region to use, resource creation prefixes, and the cluster name to use with the Amazon ECS CLI:
# create task definition for a docker container
ecs-cli compose --project-name $CLUSTER create

ecs-cli configure --cluster $CLUSTER --default-launch-type FARGATE --config-name $CLUSTER --region $REGION


echo ""
echo "creating a new AWS CloudFormation stack called amazon-ecs-cli-setup-"$CLUSTER
# Create an Amazon ECS cluster with the ecs-cli up command. Because you specified Fargate as your default launch type in the cluster configuration, this command creates an empty cluster and a VPC configured with two public subnets.

ecs-cli up --force --cluster-config $CLUSTER --ecs-profile $profile_name




echo ""
echo "getting resource ids "
VPCid=$(aws ec2 describe-vpcs --vpc-ids --query "Vpcs[0].VpcId" --output text)
echo ""
echo $VPCid
export VPCid=$VPCid

SGid=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPCid" \
  --region $REGION  --query "SecurityGroups[0].GroupId" --output text)
echo ""
echo $SGid
export SGid=$SGid

SUBNET_IDS=$(aws ec2 describe-subnets --filter "Name=vpc-id,Values=$VPCid" --region us-east-1 --query "Subnets[*].SubnetId" --output text )

IFS=$'\t ' read -r -a subnet_ids <<< $SUBNET_IDS
subnet1=${subnet_ids[0]}
subnet2=${subnet_ids[1]}
echo ""
echo $subnet1
echo $subnet2

export subnet1=$subnet1
export subnet2=$subnet2

echo ""
echo "adding ingress rules to security groups"
aws ec2 authorize-security-group-ingress --group-id $SGid --protocol tcp \
--port 80 --cidr 0.0.0.0/0 --region $REGION

echo ""
echo "generating docker compose file to be used"

## creating automatically docker-compose file using image name to use
export image=$REPO_URI
export REGION=$REGION
rm -f docker-compose.yml temp.yml
( echo "cat <<EOF >docker-compose.yml";
  cat docker-template.yml;
#   echo "EOF";
) >temp.yml
. temp.yml
# cat docker-compose.yml
# exit

echo ""
echo "generating ecs params file"
## creating automatically ecs-params with SGid and subnet ids
export task_role
export task_execution_role
export subnet1=$subnet1
export subnet2=$subnet2
export secgroupid=$SGid
rm -f ecs-params.yml temp.yml
( echo "cat <<EOF >ecs-params.yml";
  cat ecs-params-template.yml;
#   echo "EOF";
) >temp.yml
. temp.yml



# echo ""
# echo " ecs service file"
# ## creating automatically ecs service file
# export SERVICE_NAME
# export task_role
# # rm -f ecs-simple-service-elb.json temp.json
# ( echo "cat <<EOF >ecs-simple-service-elb.json";
#   cat ecs-simple-service-elb-template.json;
#   echo "EOF";
# ) >temp.json
# # . temp.json


# cat ecs-params.yml

#####
# ecs-cli configure --region us-east-1 --cluster $CLUSTER_NAME

# create ecs cluster of ec2 instances
# ecs-cli up --keypair $KEY_PAIR --capability-iam --size $CLUSTER_SIZE --security-group $SSH_SECURITY_GROUP --vpc $VPC_ID --subnets $SUBNET_ID --image-id $AMI_ID --instance-type $INSTANCE_TYPE --verbose


# echo "creating task definition"
# # create task definition for a docker container
# ecs-cli compose create --file docker-compose.yml --project-name $SERVICE_NAME --cluster-config $CLUSTER

echo "create elb & add a dns CNAME for the elb dns"
# create elb & add a dns CNAME for the elb dns
# aws elb create-load-balancer --load-balancer-name $SERVICE_NAME --listeners Protocol="HTTP,LoadBalancerPort=8080,InstanceProtocol=TCP,InstancePort=80" --subnets $subnet1 $subnet2 --security-groups $SGid --scheme internal

exit
# aws elb delete-load-balancer --load-balancer-name $SERVICE_NAME
lb=$(aws elbv2 create-load-balancer --name $SERVICE_NAME --type gateway --subnets  $subnet1 $subnet2 --output json)

aws elbv2 describe-load-balancers --load-balancer-name $SERVICE_NAME --region $REGION --query "Subnets[*].SubnetId" --output text


targetgroup-arn=$(aws elbv2 create-target-group --name $SERVICE_NAME'targets' --protocol GENEVE --port 6081 --vpc-id $VPCid --output text)

aws elbv2 register-targets --target-group-arn $targetgroup-arn --targets Id=i-1234567890abcdef0 Id=i-0abcdef1234567890

aws elbv2 create-listener --load-balancer-arn loadbalancer-arn --default-actions Type=forward,TargetGroupArn=targetgroup-arn

aws elbv2 describe-target-health --target-group-arn targetgroup-arn
# aws elbv2 create-target-group \
#     --name my-targets \
#     --protocol HTTP \
#     --port 80 \
#     --target-type ip \
#     --vpc-id $VPCid



echo "create service with above created task definition & elb"
# create service with above created task definition & elb
aws ecs create-service \
    --cluster $CLUSTER \
    --service-name $SERVICE_NAME \
    --cli-input-json file://ecs-simple-service-elb.json




ecs-cli compose --project-name $SERVICE_NAME service up --create-log-groups \
  --cluster-config $CLUSTER --ecs-profile $profile_name --load-balancer-name $SERVICE_NAME

echo ""
echo "here are the containers that are running in the service"
ecs-cli compose --project-name $SERVICE_NAME service ps --cluster-config $CLUSTER --ecs-profile $profile_name



# TASK_DEF=$(aaws ecs describe-task-definition --task-definition $SERVICE_NAME --query "taskDefinition.taskDefinitionArn" --output text)

# echo ""
# echo $TASK_DEF


# aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,InstanceType,PublicIpAddress,Tags[?Key==`Name`]| [0].Value]' --output table




# exit

# aws ecs update-service \
# --cluster $CLUSTER \
# --service $SERVICE_NAME \
# --task-definition feedback-bot-dev \
# --region $REGION
