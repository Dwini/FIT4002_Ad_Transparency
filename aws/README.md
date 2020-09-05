# Instructions for running in AWS

## Instructions for configuring production environment environment - very tedious.
1. Sign up to AWS Educate Account [here](https://www.awseducate.com/student/s/awssite).
2. Allow container logging (for debug help) with a two step process:
  1. Create 'ecsInstanceRole' Role from tutorial [here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_cloudwatch_logs.html).
  2. Create 'ECS-CloudWatchLogs' IAM Policy from tutorial [here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_cloudwatch_logs.html).
3. Install AWS CLI locally.
4. Get updated AWS credentials from [here](https://labs.vocareum.com/main/main.php) (Account Details). These credentials get updated every 3 hours.
5. Update the local AWS credentials file with the credentials found in step 4. On Windows, the local file is saved `C:\Users\<USERNAME>\.aws`.
6. Copy the contents of this 'config' file from this github directory into the local config file.
7. Create your first AWS ECS Task Definition with the following CLI command: `aws ecs register-task-definition --cli-input-json file://task-definition.json`. (Good luck if it throws an error).
8. In the AWS Console, find the Elastic Container Service. Go to Task Definitions and confirm there is now a 'ad-transparency' task.
9. Select the task definition and run task. (Good luck if it throws an error).
10. Create a Docker Hub account and install the Docker Hub CLI. Confirm you can view the current bot (`mattbertoncello/ad_transparency_bot`) and db (`mattbertoncello/ad_transparency_db`) images.

## Updating containers.
1. Get updated AWS credentials from [here](https://labs.vocareum.com/main/main.php) (Account Details) and Update the local AWS credentials file with the credentials found. On Windows, the local file is saved `C:\Users\<USERNAME>\.aws`.
2. Locally build bot and db images separately and push to docker hub.
  * bot image: `mattbertoncello/ad_transparency_bot`.
  * db image: `mattbertoncello/ad_transparency_db`.
3. Any task run from AWS will use the new containers.

## Defining new bot clusters.
4. Update the `task-definition.json` file to include the bot usernames in this batch. The db container must be specified.
5. Run the following command in root directory to define new task `aws ecs register-task-definition --cli-input-json file://task-definition.json`.
6. Login to AWS console and run the newly defined task.
