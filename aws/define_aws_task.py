"""
This module handles the generation of a new `task-definition.json` file that
can be provided to AWS CLI to define a new AWS task.

Last updated: MB 5/09/2020 - created module.
"""
# import external libraries.
import json

# define constants.
OUT_FILE = r'./task-definition.json'

"""
The function will create a new `task-definition.json` file with the usernames
provided in the username_list. When this file is issued to AWS CLI it will create
a new task on AWS ECS. View README.md in the `\aws` directory for deployment
instructions.
"""
def create_task_definition(batch_name, username_list):
    # throw error if username_list is empty.
    if len(username_list) == 0:
        raise Exception("[INPUT ERROR] username_list cannot be empty")

    # object to be written to JSON file.
    obj = {}

    # list of containers to include in this task.
    container_list = []

    # provide the task-wide configuration.
    obj['family'] = batch_name
    obj['networkMode'] = 'awsvpc'
    obj['requiresCompatibilities'] = [ 'FARGATE' ]
    obj['memory'] = '8192'
    obj['cpu'] = '4096'
    obj['executionRoleArn'] = 'ecsTaskExecutionRole'

    # for each profile included in the username_list, configure a bot container
    # and append it to the container_list.
    for username in username_list:
        container_list.append({
            'name': username.replace('.', ''),
            'image': 'mattbertoncello/ad_transparency_bot',
            'essential': False,
            'logConfiguration': {
                'logDriver': 'awslogs',
                'options': {
                  'awslogs-group': '/ecs/ad-transparency',
                  'awslogs-region': 'us-east-1',
                  'awslogs-stream-prefix': 'ecs'
                }
            },
            'environment': [
                { 'name': 'AD_USERNAME', 'value': username },
                { 'name': 'USE_PROXIES', 'value': '0' },
                { 'name': 'CHANGE_LOCATION', 'value': '1' },
                { 'name': 'DB_URL', 'value': 'http://35.173.250.122:8080' },
                { 'name': 'NUM_TERMS', 'value': '10' },
                { 'name': 'UPLOAD_LOGS', 'value': '1' }
            ]
        })

    # add all containers to the json object.
    obj['containerDefinitions'] = container_list

    # open the OUT_FILE to write. override any existing outfile.
    with open(OUT_FILE, 'w') as w_file:
        json.dump(obj, w_file, indent=2)

if __name__ == '__main__':
    # provide google profiles to run in this task.
    username_list = ['piasmith984', 'm3428615', 'lasquishadavis', 'mwest5078', \
        'awhite2627', 'georgjerome934', 'stevensagnes677', 'tj8021671', \
        'eliza.kane.3', 'burgersa68']
    batch_name = 'ad-transparency-batch1'

    # run the tast creation function.
    create_task_definition(batch_name, username_list)
