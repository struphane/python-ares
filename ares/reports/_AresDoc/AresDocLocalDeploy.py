"""

"""

NAME = 'Local Deploy'
DOWNLOAD = None

def report(aresObj):
  """ """
  aresObj.title("How to deploy your first script")
  content = aresObj.paragraph("After having produced your reports locally, you can push your results to a shared"
                              " disposable environment. Those environments will be created automatically thanks "
                              "the script {0}. In the same way than the previous one, you can push your list of "
                              "scripts to the server by running this script. Thanks to this all the modules will be"
                              " deployed to the server and your report will automatically and on the fly produce the"
                              " HTML page which will be displayed when you run the url.",
                              htmlComp=[aresObj.code("AresDeploy.py")])
  content2 = aresObj.paragraph("Once the deployment completed, the reports will be available to a dedicated url on the server. "
                               "You can go on the Ares Environment section and your report should appear in the list of folder."
                               "Please be aware that the name will be the variable {0} that you defined in your report",
                               htmlComp=[aresObj.code("NAME")])
  success = aresObj.img('first_script_deploy_success.JPG', cssAttr={"margin-left": '20%'})
  aresObj.row([aresObj.col([content, success, content2]), aresObj.img('first_script_deploy.JPG')])
  aresObj.row([aresObj.img('first_script_deploy_server.JPG')], cssAttr={'margin-top': '20px', 'margin-bottom': '20px'})
  content = aresObj.paragraph("The display should be in line with the one that you got when you run your report locally."
                              "At this stage you can debug your results by using the developer mode of your web browser.")

  div = aresObj.div("Do not worry with the quality of the scripts deployed. If there is any issue in the implementation"
                    " the script will fail and it will display the error. So even if it is recommended to check the report"
                    " localy before pushing it to your disposable environment, any error will only break the run of your"
                    " script and it will not affect the other environments ", cssCls=['alert alert-info'])
  div.addAttr('role', 'alert')
  aresObj.row([aresObj.col([content, div, aresObj.img('first_script_deploy_error.JPG')]),
               aresObj.img('first_script_report_result.JPG')])

