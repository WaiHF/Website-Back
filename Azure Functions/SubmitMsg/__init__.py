import json
import azure.functions as func

def main(req: func.HttpRequest, sendGridMessage: func.Out[str]) -> func.HttpResponse:

    print(req.form)

    # Gets the data from form.
    try:
      name = req.form['name']
      email = req.form['email']
      msg = req.form['msg']
    except:
      print('Missing form attribute.')
      return func.HttpResponse(f"Missing form attribute")

    # Creation of email.
    try:
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
    except:
      print('Failed to create and send email')
      return func.HttpResponse(f"Failed to create and send email")

    return func.HttpResponse(f"Sent")