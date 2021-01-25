from flask import Flask, redirect, abort
from flasgger import Swagger

import os, time, logging
from datetime import datetime

from api.controller import control_blueprint


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
    "version": "0.1"
  },
  "schemes": [
    "http"
  ],
}

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Application specifics
app = Flask(__name__)

app.register_blueprint(control_blueprint)
swagger = Swagger(app, template=swagger_template)

# It is considered bad form to return an error for '/', so let's redirect to the apidocs
@app.route('/')
def index():
    return redirect('/apidocs')


if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0')