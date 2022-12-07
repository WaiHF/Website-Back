import logging

import azure.functions as func


def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.route_params.get('name')
    count = req.route_params.get('count')
    countInt = 0

    if count:
        try:
            countInt = int(count) + 1
        except Exception:
            print(Exception)
    else:
        return func.HttpResponse(
             "Invalid count",
             status_code = 400
        )

    if name:
        try:
            pageItem = {
                "id": name,
                "visits": countInt
                }
            doc.set(func.Document.from_dict(pageItem))

            return func.HttpResponse(
                f"Page {name} updated.",
                status_code = 200)
        except Exception:
            print(Exception)
    else:
        return func.HttpResponse(
             "Invalid name",
             status_code = 400
        )
