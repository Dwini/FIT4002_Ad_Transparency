import uuid
from datetime import datetime

import constants

def Bot(name, username, password, sex, DOB):
    
    # generate unique id
    id = str(uuid.uuid4())

    # convert dates to string
    date_created = datetime.now().strftime(constants.datetime_string)
    DOB_string = DOB.strftime(constants.datetime_string)

    return {
        'id': { 'S': id },
        'date_created': { 'S': date_created },
        'name': { 'SS': name },
        'username': { 'S': username },
        'password': { 'S': password },
        'sex': { 'S': sex },
        'DOB': { 'S': DOB_string }
    }