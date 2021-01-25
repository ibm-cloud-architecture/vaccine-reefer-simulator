
from flask import Blueprint, request, abort
import logging
from flasgger import swag_from
from flask_restful import Resource, Api
from concurrent.futures import ThreadPoolExecutor
from api.prometheus import track_requests
from infrastructure.MetricsEventsProducer import MetricsEventsProducer 
from domain.reefer_simulator import ReeferSimulator
from flask import current_app as app
"""
 created a new instance of the Blueprint class and bound the Controller resource to it.
"""

control_blueprint = Blueprint("control", __name__)
api = Api(control_blueprint)
metricsProducer = MetricsEventsProducer()

def sendEvents(metrics):
    """
    Send Events to Kafka
    """
    app.logger.info(metrics)
    for metric in metrics:
        evt = {"containerID": metric[0],
                "timestamp": str(metric[1]),
                "type":"ReeferTelemetries",
                "payload": str(metric)}
        metricsProducer.publishEvent(evt,"containerID")

# The python-flask stack includes the prometheus metrics engine. You can ensure your endpoints
# are included in these metrics by enclosing them in the @track_requests wrapper.

class SimulationController(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}
    

    # Need to support asynchronous HTTP Request, return 202 accepted while starting 
    # the processing of generating events. The HTTP header needs to return a
    # location to get the status of the simulator task    
    @track_requests
    @swag_from('controlapi.yml')
    def post(self):
        app.logger.info("post control received: ")
        control = request.get_json(force=True)
        app.logger.info(control)
        if not 'containerID' in control:
            abort(400) 
        simulator = ReeferSimulator()
        nb_records = int(control["nb_of_records"])
        if control["simulation"] == ReeferSimulator.SIMUL_POWEROFF:
            metrics=simulator.generatePowerOffTuples(control["containerID"],nb_records,control["product_id"])
        elif  control["simulation"]  == ReeferSimulator.SIMUL_CO2:
            metrics=simulator.generateCo2Tuples(control["containerID"],nb_records,control["product_id"])
        elif  control["simulation"]  == ReeferSimulator.SIMUL_O2:
            metrics=simulator.generateO2Tuples(control["containerID"],nb_records,control["product_id"])
        elif  control["simulation"]  == ReeferSimulator.SIMUL_TEMPERATURE:
            metrics=simulator.generateTemperatureTuples(control["containerID"],nb_records,control["product_id"])
      
        else:
            return {"error":"Wrong simulation controller data"},404
    
        if nb_records < 500:
            sendEvents(metrics)
        else:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(sendEvents,metrics)
            
        return { "reason": "Simulation started"},202
    


api.add_resource(SimulationController, "/control")