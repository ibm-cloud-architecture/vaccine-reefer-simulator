from flask import Blueprint, jsonify
from flasgger import swag_from
import os

url_blueprint = Blueprint("freezerurl", __name__)

@url_blueprint.route("/freezerurl")
@swag_from('freezerURL.yaml')
def getFreezerURL():
    return jsonify({"freezerMgrURL": os.getenv('FREEZER_MGR_URL','http://localhost:8082')})