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
      ('Lib', '__init__.py'),
      ('Lib', 'AresChartsService.py'),
      ('Lib', 'flask_dummy.py')
    ],
  },
  'EXCLUDED': {
    'FOLDERS': [],
    'FILES': ['AresSecurity.py'],
  },

  #
  #
  'REMAP': {
      'FOLDERS': {
        ('ares', 'Lib', 'tools'): ()
       },
      'FILES': {
        ('Lib', 'flask_dummy.py'): ('flask.py', )
      } ,
    }
}

CHART = {
  'INCLUDED': {
    'FILES': [
      ('Lib', 'AresChartsService.py')
    ]
  }
}

DUMMY = {
   'INCLUDED': {
     'FILES': [
       ('Lib', 'mailer.py')
     ]
   },

   'REMAP': {
     'FILES': {
        ('Lib', 'mailer.py'): ('mailer.py', )}
   }
}

