#!/bin/bash
set -e

ECR_proxy_repo='traffic-django-restapi-proxy'
ECR_app_repo='traffic-django-restapi-app'


AWS_REGION="us-east-1"
accountid=$(aws sts get-caller-identity --query Account --output text)

REPOSITORY_PATH=$accountid".dkr.ecr.us-east-1.amazonaws.com"
FULLY_QUALIFIED_IMAGE_NAME_proxy=$REPOSITORY_PATH"/"$ECR_proxy_repo
FULLY_QUALIFIED_IMAGE_NAME_app=$REPOSITORY_PATH"/"$ECR_app_repo

echo "\n $FULLY_QUALIFIED_IMAGE_NAME_proxy"
echo "\n $FULLY_QUALIFIED_IMAGE_NAME_app"


user_name_proxy='traffic-app-api-ci'
aws_ci_user_name='traffic-app-api-ci-devops'
bucket_name='bruvio-tfstate-traffic-app-api-ci'

table_name='terraform-setup-tf-state-lock-traffic-app-api-ci'
table_primary_key='LockID'


aws ecr create-repository --repository-name $ECR_proxy_repo  \
    --image-scanning-configuration scanOnPush=true || echo "\n repository $ECR_proxy_repo already created"
echo "\n Created ECR repository: $ECR_proxy_repo."


aws ecr create-repository --repository-name $ECR_app_repo  \
    --image-scanning-configuration scanOnPush=true || echo "\n repository $ECR_app_repo already created"
echo "\n  Created ECR repository: $ECR_app_repo."

aws iam create-policy --policy-name TrafficAppApi-ProxyCIPushECR --policy-document file://deploy/aws-policies/TrafficAppApi-ProxyCIPushECR.json
echo" \n  Creted IAM user policy TrafficAppApi-ProxyCIPushECR" || echo "\n policy TrafficAppApi-ProxyCIPushECR already exists"


policy_arn=$(aws iam list-policies --query 'Policies[?PolicyName==`TrafficAppApi-ProxyCIPushECR`].Arn' --output text)



aws iam create-user --user-name ${user_name_proxy}

echo "\n created IAM user ${user_name_proxy}"

aws iam attach-user-policy --user-name ${user_name_proxy} --policy-arn ${policy_arn}

echo "\n attaching IAM policy to user"


aws iam create-access-key --user-name ${user_name_proxy}

# exit
aws ecr describe-repositories --repository-name traffic-django-restapi

repoARN=$(aws ecr describe-repositories --query 'repositories[?repositoryName==`traffic-django-restapi-proxy`].repositoryURI' --output text)


aws s3api create-bucket --bucket $bucket_name || echo "\n bucket $bucket_name already exists"

echo "\n  Creating S3 bucket to store Terraform state"

aws s3api put-bucket-versioning --bucket $bucket_name --versioning-configuration Status=Enabled

aws s3 mb s3://$bucket_name --region us-east-1 && \
aws s3api put-bucket-versioning --bucket $bucket_name --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption \
--bucket $bucket_name \
--server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'

echo "\n bucket created"

echo "\n creating Dynamodb table"

aws dynamodb create-table --table-name $table_name \
    --attribute-definitions AttributeName=$table_primary_key,AttributeType=S \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --key-schema AttributeName=$table_primary_key,KeyType=HASH --region us-east-1 || echo "\n dynamoDB table $table_name already exists"


aws ec2 run-instances --image-id $(aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2 --query 'Parameters[0].[Value]' --output text) --count 1 --instance-type t2.micro




echo " \n  creating IAM user policy TrafficAppApi-CI"
aws iam create-policy --policy-name TrafficAppApi-CI --policy-document file://deploy/aws-policies/TrafficAppApi-CI.json

echo "done \n"


policy_arn_terraform=$(aws iam list-policies --query 'Policies[?PolicyName==`TrafficAppApi-CI`].Arn' --output text)
policy_id_terraform=$(aws iam list-policies --query 'Policies[?PolicyName==`TrafficAppApi-CI`].PolicyId' --output text)



echo "\n creating IAM user ${aws_ci_user_name}"

aws iam create-user --user-name ${aws_ci_user_name}

echo "\n attaching IAM policy to user"
aws iam attach-user-policy --user-name ${aws_ci_user_name} --policy-arn ${policy_arn_terraform}


echo "\n creating access key for ${aws_ci_user_name}"
aws iam create-access-key --user-name ${aws_ci_user_name}

# exit

echo "\n updating $aws_ci_user_name user poicies to allow rds"
aws iam create-policy-version --policy-arn $policy_arn_terraform --policy-document file://deploy/aws-policies/TrafficAppApi-CI-rds-policies.json --set-as-default
echo "\n updating $aws_ci_user_name user poicies to allow bastion host"
aws iam create-policy-version --policy-arn $policy_arn_terraform --policy-document file://deploy/aws-policies/TrafficAppApi-CI-bastion-policies.json --set-as-default


echo "\n copy public gitlab ssh key "
xclip -sel clip < ~/.ssh/id_rsa_gitlab.pub


aws ec2 import-key-pair --key-name traffic-app-api-devops-bastion --public-key-material fileb://~/.ssh/id_rsa_gitlab.pub



echo "\n updating $aws_ci_user_name user poicies to allow ecs use"
aws iam create-policy-version --policy-arn $policy_arn_terraform --policy-document file://deploy/aws-policies/TrafficAppApi-CI-ecs-policies.json --set-as-default

aws iam delete-policy-version --policy-arn  $policy_arn_terraform  --version-id v11

aws iam list-policy-versions --policy-arn $policy_arn_terraform


echo "\n updating $aws_ci_user_name user poicies to allow load balancer use"
aws iam create-policy-version --policy-arn $policy_arn_terraform --policy-document file://deploy/aws-policies/TrafficAppApi-CI-loadbalancer-policies.json --set-as-default

echo "\n updating $aws_ci_user_name user poicies to allow s3 use"
aws iam create-policy-version --policy-arn $policy_arn_terraform --policy-document file://deploy/aws-policies/TrafficAppApi-CI-customdns-policies.json --set-as-default


