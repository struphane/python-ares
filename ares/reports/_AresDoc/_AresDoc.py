""" Report Comment


"""

import this
import collections
import os

NAME = 'Reports Documentation'
DOWNLOAD = None
SHORTCUTS = [('Documentation', [
      ('Local Runs', 'AresDocLocalEnv'),
      ('HTML Components', 'AresDocHtml'),
      ('Graph Components', 'AresDocGraph'),
    ]
   )]

def report(aresObj):
  """

  """
  aresObj.title("Report Documentation")
  aresObj.title2("How to create a report")

  aresObj.paragraph('''
    In this section you can get a better explanation of the different features implemented in this framework.
    Basically this will provide you with a web framework to let your users a complete flexibility.

    People will be allowed to create and extend the system in a controlled manner by putting in place shared local
    environments. Those environments will have a limited impact on the production and let you the ability to play with
    data.

    The web framework will come with HTML and graph components that you can directly use from your report to get a better
    a HTML 5 display of your results. This layer can be easily integrated with C++ and C solutions.

    The architecture of your local environments should be as followed:
    {0}

    This is the root path of your environments and it will contain your set of reports.
    The main report will have the same name as your environment
      {1}, please have a look at the template structure here: {2}
      {3}

        The python services that you can call in order to refresh components in your reports.
        Those call will return python dictionaries with some mandatory keys like (status and data)

      {4}

        The .dat files used in your local environment

      {5}

        The folder to load you javascripts callbacks functions. By using this folder you can load javascript functions from
        your python objects instead of writing them as string in the code. This is more dedicated for advanced users that
        could expect to get those functions shared with other environments (and then pushed to the main jasvascript folder)

    If you need more details about the python golden rules please have a look here: {6}.
    If you need more information about all the components and how to build a report please refer to the left side bar
    ''', htmlComp=[aresObj.code('/YouLocalEnv'),
                   aresObj.code('YouLocalEnv.py'),
                   aresObj.main('see templates', {'SCRIPT_NAME': 'AresDocTmpl'}, cssCls=''),
                   aresObj.code('/ajax/'),
                   aresObj.code('/data/'),
                   aresObj.code('/js/'),
                   aresObj.anchor('Golden rules  Good practises', cssCls=''),
                   ])

  aresObj.blockquote([this.s.decode('rot13').split("Peters")[1].strip().replace("\n", "<BR />"), 'Tim Peters'])
