import logging
import json

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    payload = context.get_input()
    
    queryResult = yield context.call_activity('GetPageVisits', payload['page'])

    if queryResult['error'] == '':
        visits = yield context.call_activity('UpdatePageVisits', queryResult)
    else:
        return queryResult

    return visits
main = df.Orchestrator.create(orchestrator_function)