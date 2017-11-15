"""
To run this framework you need the below python external modules installed.
  - flask
  - flask_SQLAlchemy
  - flask_login
  - cryptography

The easiest way to configure your enviroment is to use

  pip install packageName

To set the proxy you can use the below command:

  SET HTTPS_PROXY=http://login:password@

This should work with both Python 2.7 and Python 3.x

"""


from app import app, init_db

app.debug = True
init_db()
app.run(host="192.168.0.2", threaded=True)
#app.run(threaded=True)

