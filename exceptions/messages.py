LBGR001 = 'Service is not working'
LBGR002 = 'Processing'
LBGR003 = 'No Found {}'
DEFAULT = 'Error message missing'


def get_message(key, value_to_format=None):
    try:
        message = globals()[key]
        if value_to_format:
            message = message.format(value_to_format)
        return message
    except KeyError:
        return DEFAULT
