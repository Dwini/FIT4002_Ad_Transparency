import uuid
from datetime import datetime

import constants

def Log(bot_id, url, actions, search_term=None):
    
    # generate unique id
    id = str(uuid.uuid4())

    # convert dates to string
    date_logged = datetime.now().strftime(constants.datetime_string)

    return {
        'id': { 'S': id },
        'date_logged': { 'S': date_logged },
        'bot_id': { 'S': bot_id },
        'url': { 'S': url },
        'actions': { 'SS': actions },
        'search_term': { 'S': search_term }
    }