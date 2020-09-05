# Instructions for running in AWS

## Instructions for configuring production environment environment - very tedious.
1. Sign up to AWS Educate Account [here](https://www.awseducate.com/student/s/awssite).
2. Allow container logging (for debug help) with a three step process:
  a. Create 'ecsInstanceRole' Role from tutorial [here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/instance_IAM_role.html). Section 'To create the ecsInstanceRole IAM role for your container instances'. This is to create a user role which can save CloudWatch logs.
  b. Create 'ECS-CloudWatchLogs' IAM Policy from tutorial [here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_cloudwatch_logs.html). Section 'CloudWatch Logs IAM Policy'. This is to define the process of logging to CloudWatch.
  c. Create a log group by going into CloudWatch -> Logs -> Log groups. Create a new group called '/ecs/ad-transparency'. This is where the logs will be saved.
3. Create 'ecsTaskExecutionRole' Role from tutorial [here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html). Section 'Creating the task execution IAM role'. This is to create a user role which can deploy tasks in ECS.
4. Install AWS CLI locally.
5. Get updated AWS credentials from [here](https://labs.vocareum.com/main/main.php) (Account Details). These credentials get updated every 3 hours.
6. Update the local AWS credentials file with the credentials found in step 4. On Windows, the local file is saved `C:\Users\<USERNAME>\.aws`.
7. Copy the contents of this 'config' file from this github directory into the local config file.
8. Create your first AWS ECS Task Definition with the following CLI command: `aws ecs register-task-definition --cli-input-json file://task-definition.json`. (Good luck if it throws an error).
9. In the AWS Console, find the Elastic Container Service. Go to Task Definitions and confirm there is now a 'ad-transparency' task.
10. Select the task definition and run task. (Good luck if it throws an error).
11. Create a Docker Hub account and install the Docker Hub CLI. Confirm you can view the current bot (`mattbertoncello/ad_transparency_bot`) and db (`mattbertoncello/ad_transparency_db`) images.

## Updating containers.
1. Get updated AWS credentials from [here](https://labs.vocareum.com/main/main.php) (Account Details) and Update the local AWS credentials file with the credentials found. On Windows, the local file is saved `C:\Users\<USERNAME>\.aws`.
2. Locally build bot and db images separately and push to docker hub.
  * bot image: `mattbertoncello/ad_transparency_bot`.
  * db image: `mattbertoncello/ad_transparency_db`.
  a. `docker build -t <image_name> .`.
  b. `docker tag <image_id> mattbertoncello/ad_transparency_bot:latest` or ad_transparency_db.
  c `docker push mattbertoncello/ad_transparency_bot:latest` or ad_transparency_db.
3. Any task run from AWS will use the new containers.

## Defining new bot clusters.
1. Run the `define_aws_task.py` file with appropriate username, batch_name and environment variable values.
2. Get updated AWS credentials from [here](https://labs.vocareum.com/main/main.php) (Account Details) and Update the local AWS credentials file with the credentials found. On Windows, the local file is saved `C:\Users\<USERNAME>\.aws`.
3. Run the following command in root directory to define new task `aws ecs register-task-definition --cli-input-json file://task-definition.json`.
4. Login to AWS console and run the newly defined task.
