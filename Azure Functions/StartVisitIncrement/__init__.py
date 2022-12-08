import logging

import azure.functions as func
import azure.durable_functions as df


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)

    page = str(req.route_params.get('page')).lower()
    payload = {"page": page}

    instance_id = await client.start_new(req.route_params["funcName"], None, payload)

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    return client.create_check_status_response(req, instance_id)