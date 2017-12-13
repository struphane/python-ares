""" [SCRIPT COMMENT]


"""

TEAM = '' # Report's team
DSC = '' # Report Short description
NAME = 'Report' # The Report Name in the left menu
# The Shortcuts should be defined as below
# [(Cateogry Name, [List of the script in the root directory])]
# It is only possible to create new links for scripts in the root
SHORTCUTS = [] # All the possible link to other pages
FILE_CONFIGS = [] # All the static and output files configurationa
# The format in the above list should be as: {'filename': 'data.txt', 'folder': 'outputs', 'parser': InFilePricesConfig.InFilePices},

HTTP_PARAMS = [] # If you want to use the param method to set parameter before running hte report


#def params(modalObj):
#  """ Optional param method to be run before the report method to set parameter """


def report(aresObj):
  '''
  Write your function below
  '''
  aresObj.title("My report Title")