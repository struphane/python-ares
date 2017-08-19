# Run a test server.
from app import app

app.debug = True
#app.run(host="192.168.0.2", threaded=True)
app.run(threaded=True)