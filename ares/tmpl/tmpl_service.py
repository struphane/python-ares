""" Module dedicated to run a function and update only a part of the web page

All the python logic should be defined in the call function.
The aresObj is the usual object, there is no special thing on the ajax call.
Indeed the same functions are defined in this script.

Namely:
  - DIRECTORY is the currently script repository
    All the script should be directly defined in the root path of your special environment

  - REPORT_NAME is te environment variable. It will refer to the name of your folder
    The main script of your environment should have the name of your script

As the module path will be stored in the class path when a script will be run, all the scripts
can be used as import. For example if you want to use a script for another xxx sub folder (with a __init__),
you can use in you report:
  import XXX.MyModule

Please if you are using a useful import liaise with BDI London and it might be something that
we will move to the common Lib folder.

The script can return something according to what is defined in your ajax call.
By default it will return true or falsk to give a status on the result of the script
"""

import json

def call(aresObj):
  """
  [ PLEASE DETAIL YOU SCRIPT HERE ]
  """

  return {'status': '', 'data': []}