import logging
import json

import azure.functions as func

def main(req: func.HttpRequest, doc:func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    result = {}
    
    for page in doc:
        if page['id'] == req.route_params.get('name'):
            result = {
                "id": page['id'],
                "visits": page['visits']
            }
            break

    return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"    
        )
