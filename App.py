from flask import Flask
from Routes import Routes

# init app
app = Flask(__name__)

Routes.register(app)

# Run Server
app.run(debug=True, host='127.0.0.1', port=9999)
