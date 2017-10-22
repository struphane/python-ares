""" Module dedicated to define the packages available for download in the Lab

"""

# Ares package
ARES = {
  'INCLUDED': {
    'FOLDERS': [
      ('ares', 'Lib', 'graph'),
      ('ares', 'Lib', 'html'),
      ('ares', 'Lib', 'tools'),
      ('ares', 'Lib'),
      ('ares', 'tmpl')
    ],
    'FILES': [
      ('Libs', '__init__.py'),
      ('Libs', 'AresChartsService.py'),
      ('Libs', 'flask_dummy.py')
    ],
  },
  'EXCLUDED': {
    'FOLDERS': [],
    'FILES': [],
  },

  #
  #
  'REMAP': {
      'FOLDERS': {
        ('ares', 'Lib', 'tools'): ()
       },
      'FILES': {
        ('Libs', 'flask_dummy.py'): ('flask.py', )
      } ,
    }
}

CHART = {
  'INCLUDED': {
    'FILES': [
      ('Libs', 'AresChartsService.py')
    ]
  }
}

DUMMY = {
   'INCLUDED': {
     'FILES': [
       ('Libs', 'mailer.py')
     ]
   },

   'REMAP': {
     'FILES': {
        ('Libs', 'mailer.py'): ('mailer.py', )}
   }
}

