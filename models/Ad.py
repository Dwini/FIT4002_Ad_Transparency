import uuid
from datetime import datetime

import constants

def Ad(bot_id, url, html_string):

    id = str(uuid.uuid4())
    date_captured = datetime.now().strftime(constants.datetime_string)

    return {
        'id': { 'S': id },
        'date_captured': { 'S': date_captured },
        'bot_id': { 'S': bot_id },
        'url': { 'S': url },
        'html_string': { 'S': html_string }
    }