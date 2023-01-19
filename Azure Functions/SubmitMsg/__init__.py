import json
import azure.functions as func

def main(req: func.HttpRequest, sendGridMessage: func.Out[str]) -> func.HttpResponse:

    # Gets the data from form.
    name = req.form['name']
    email = req.form['email']
    msg = req.form['msg']

    # Creation of email.
    message = {
        "personalizations": [{
          "to": [{
            "email": "waihfun@gmail.com"}],
            "cc": [{
            "email": email}]
            }],
        "subject": "Message from: " + name,
        "content": [{
            "type": "text/plain",
            "value": msg }]
            }

    # Sends email
    sendGridMessage.set(json.dumps(message))

    return func.HttpResponse(f"Sent")