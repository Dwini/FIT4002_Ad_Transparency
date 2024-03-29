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
def create_task_definition(batch_name, username_list, use_proxies='0', change_location='0'):
    # throw error if username_list is empty.
    if len(username_list) == 0:
        raise Exception("[INPUT ERROR] username_list cannot be empty")

    # throw error if use_proxies is not '0' or '1'.
    if use_proxies != '0' and use_proxies != '1':
        raise Exception("[INPUT ERROR] use_proxies is not '0' or '1': "+str(use_proxies))

    # throw error if change_location is not '0' or '1'.
    if change_location != '0' and change_location != '1':
        raise Exception("[INPUT ERROR] change_location is not '0' or '1': "+str(change_location))

    # object to be written to JSON file.
    obj = {}

    # list of containers to include in this task.
    container_list = []

    # provide the task-wide configuration.
    obj['family'] = batch_name
    obj['networkMode'] = 'awsvpc'
    obj['requiresCompatibilities'] = [ 'FARGATE' ]
    obj['memory'] = '4096'
    obj['cpu'] = '2048'
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
                { 'name': 'USE_PROXIES', 'value': use_proxies },
                { 'name': 'CHANGE_LOCATION', 'value': change_location },
                { 'name': 'DB_URL', 'value': 'http://18.210.23.37:8080' },
                { 'name': 'NUM_TERMS', 'value': '2' },
                { 'name': 'UPLOAD_LOGS', 'value': '0' }
            ]
        })

    # add all containers to the json object.
    obj['containerDefinitions'] = container_list

    # open the OUT_FILE to write. override any existing outfile.
    with open(OUT_FILE, 'w') as w_file:
        json.dump(obj, w_file, indent=2)

if __name__ == '__main__':
    # provide google profiles to run in this task.
    username_list = ['Joel.Trump.3546', 'jw1083888', 'Phillipfranko44', 'goodwill.peter.8.3.4', \
        'jf0895694', 'ewaters213', 'Mel.Phillips.2454']
    batch_name = 'ad-transparency-batch2'

    # run the tast creation function.
    create_task_definition(batch_name, username_list)
