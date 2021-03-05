from flask import Flask, redirect, abort
from flasgger import Swagger

import os, time, logging
from datetime import datetime
from api.uispa import ui_blueprint
from api.health import health_blueprint
from api.controller import control_blueprint
from api.prometheus import metrics_blueprint


# The python-flask stack includes the flask extension flasgger, which will build
# and publish your swagger ui and specification at the /apidocs url. Here we set up
# the basic swagger attributes, which you should modify to match you application.
# See: https://github.com/rochacbruno-archive/flasgger
swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "Reefer Simulator for Telemetry generation",
    "description": "API for controlling the simulation, plus health and monitoring",
    "contact": {
      "responsibleOrganization": "IBM",
      "email": "boyerje@us.ibm.com",
      "url": "https://ibm-cloud-architecture.github.io",
    },
    "version": "0.0.3"
  },
  "schemes": [
    "http"
  ],
}
LOGGER_LEVEL=os.getenv("LOGGER_LEVEL","INFO")
numeric_level = getattr(logging, LOGGER_LEVEL.upper(), None)
logging.basicConfig(level=LOGGER_LEVEL.upper())

# Avoid tracing /health calls 
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Application specifics
app = Flask(__name__)

app.register_blueprint(control_blueprint)
app.register_blueprint(health_blueprint)
app.register_blueprint(metrics_blueprint)
app.register_blueprint(ui_blueprint)
swagger = Swagger(app, template=swagger_template)

# It is considered bad form to return an error for '/', so let's redirect to the apidocs
@app.route('/apidocs')
def apidoc():
  return redirect('/apidocs')


if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0',port=5000)