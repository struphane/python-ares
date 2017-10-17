"""

"""

def report(aresObj):
  """
  """
  aresObj.title("How to test your first Ajax Service")
  aresObj.paragraph("You can write and test also scripts which are not dedicated to produce a HTML "
                    "report from this environment. You can also design quick services that everybody"
                    " can share. The Lab will allow you to promote to a common server and to share within"
                    " {0} you favorite local scripts. Also if you believe that your script could benefit the "
                    "community of developers please do not hesitate to send us an email and we will add"
                    " it to the common library !",


                    htmlComp=[aresObj.http['CONFIG']['COMPANY']])
  aresObj.title2("How to proceed")
  aresObj.paragraph("First you will have to write your service in your local environment. The services"
                    " should have a call method with the aresObj. In the same way that we use this object "
                    "in your report to define the context, you will use this object to pass GET and POST http"
                    " parameters to your service. Indeed even if you can test your script locally, the design "
                    "is implemented to run in a standardised way on a server, so you will have to use GET and "
                    "POST methods. Please be aware that the keys are always converted in {0} in the service side",
                    htmlComp=[aresObj.text("uppercase", cssAttr={'font-weight': 'bold'})]
                    )
  aresObj.paragraph("In the below example, we are just writing a service to return a path when a Json file is written"
                    " on the server. The Service / Ajax calls must return a valid python object. Those objects have "
                    "to be simple enough to be able to be converted to string object using the json module. Indeed "
                    "on the server the return will always be converted by the javascript layer to a string.")

  aresObj.img("first_service_call.JPG")

  aresObj.paragraph("You can test this locally by running the script {0} from your local AReS tools."
                    "You can set the variable {1} to true if you want to test result of your service from your computer."
                    "Then you can deploy you ajax service - using the keyword ajax during the deployment - to test your"
                    " script on the server. No need for extra configuration, your service will be directly available online"
                    " in your disposable environment !",
                     htmlComp=[aresObj.text("AresServiceRun.py", cssAttr={'font-weight': 'bold'}),
                               aresObj.code("localTest")]
                    )
  aresObj.img("first_service_local.JPG")
