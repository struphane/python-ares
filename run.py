# Run a test server.
from app import app, init_db

app.debug = True
init_db()
#app.run(host="192.168.0.2", threaded=True)
app.run(threaded=True)