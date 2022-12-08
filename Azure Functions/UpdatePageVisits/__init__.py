import logging

import azure.functions as func


def main(page: dict, document) -> dict:

    try:
        if int(page['visits']) >= 0:
            page['visits'] += 1
        else:
            page['visits'] = 0
            page['error'] = 'Reset visitors to 0. Count was negative.'
            logging.warning('Reset visitors to 0. Count was negative.')
    except Exception:
            page['visits'] = 0
            page['error'] = 'Reset visitors to 0. Count was not a number.'
            logging.warning('Reset visitors to 0. Count was not a number.')

    if page['id']:
        try:
            document.set(func.Document.from_dict({
                'id': page['id'],
                'visits': page['visits']
            }))
        except Exception as e:
            logging.warning(e)
            page['error'] = 'Failed to update visit counter.'
    else:
        page['error'] = 'No ID provided.'

    return page
