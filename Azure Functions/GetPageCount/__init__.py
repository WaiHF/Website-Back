import logging

import azure.functions as func


def main(req: func.HttpRequest, cosmos: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.route_params.get('name')

    print(req.method)

    if not name or not req.method == "PUT":
        return func.HttpResponse(
             "Pass a name in the query string or in the request body for a personalized response.",
             status_code = 400
        )

    if name:
        try:
            pageItem = {
                "id": name,
                "visits": 0
                }
            cosmos.set(func.Document.from_dict(pageItem))

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
