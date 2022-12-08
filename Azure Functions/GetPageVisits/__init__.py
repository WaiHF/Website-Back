import logging


def main(pageId: str, doc) -> dict:
    result = {
        'id': '',
        'visits': 0,
        'error': ''
    }

    try:
        for page in doc:
            if page['id'] == pageId:
                result['id'] = page['id']
                result['visits'] = page['visits']
                break
    except Exception:
            logging.warning(Exception)

    if result['id'] == '':
        logging.warning('No results were found')
        result['error'] = 'No results were found for page ' + "'" + pageId + "'"

    return result    
