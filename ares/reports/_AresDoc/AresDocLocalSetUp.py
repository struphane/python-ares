"""
"""

NAME = 'Local Run'
DOWNLOAD = None

def report(aresObj):
  """

  """
  aresObj.title("Set up your environment")
  aresObj.title2("Using the installation script")
  content1 = aresObj.paragraph("Using this method you only have to run using your python version the script."
                               "This script will run a query on the server and it will retrieve the full package."
                               "The version of the scripts using this REST service will guarantee a correct synchronisation "
                               "with the server")
  content2 = aresObj.paragraph("Once the installation is completed, the ares folder with all the modules used to produce"
                               " HTML components will be downloaded. You can also find a example of project structure that "
                               "ares will recognise. ")
  aresObj.row([aresObj.col([content1,
                            aresObj.newline(),
                            aresObj.img("install_run.JPG"),
                            aresObj.newline(),
                            content2]),
               aresObj.col([aresObj.img("install_script.JPG"),
                            aresObj.newline(),
                            aresObj.img("install_result.JPG")])])

  aresObj.title2("Manual configuration")
  content1 = aresObj.paragraph("The Framework is very easy to set up and it will allow to perform all the tests fully locally based on your environment "
                              "but it will allow you also to deploy your scripts easily on the server. The only thing required is to click on the Download AReS link "
                              "{0}, to unzip the archive in a folder and then to start writing your first Python codes in a folder.", htmlComp=[aresObj.href("AReS", '', cssCls=[])])
  content2 = aresObj.paragraph("Using this way you will get the same environment except that the NewReport folder will not be generated."
                               "This folder is not very useful, it will just help you on understanding the structure of a project.")
  downloadPicture = aresObj.img('ares_download.JPG')
  aresObj.row([aresObj.col([content1, content2]), downloadPicture])
