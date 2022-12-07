import logging

import azure.functions as func


def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.route_params.get('name')

    if name:
        try:
            pageItem = {
                "id": name,
                "visits": 1
                }
            doc.set(func.Document.from_dict(pageItem))

            return func.HttpResponse(
                f"Page {name} updated.",
                status_code = 200)
        except Exception:
            print(Exception)
    else:
        return func.HttpResponse(
             "Pass a valid page name",
             status_code = 400
        )
