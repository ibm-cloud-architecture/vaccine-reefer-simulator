
from flask import Blueprint, request, abort, jsonify
import logging
from flasgger import swag_from
from flask_restful import Resource, Api
from concurrent.futures import ThreadPoolExecutor
from api.prometheus import track_requests
from infrastructure.MetricsEventsProducer import MetricsEventsProducer 
from domain.reefer_simulator import ReeferSimulator
import logging


"""
 created a new instance of the Blueprint class and bound the Controller resource to it.
"""

control_blueprint = Blueprint("control", __name__)
api = Api(control_blueprint)

class SimulationController(Resource):

    def __init__(self):
        print("SimulationController")
        self.simulator = ReeferSimulator()
        self.metricsProducer = MetricsEventsProducer()

    @swag_from('version.yaml')
    def get(self):
        return jsonify({"version": "v0.0.2"})
    

    def sendEvents(self,metrics):
        """
        Send Events to Kafka
        """
        logging.info(metrics)
        for metric in metrics:
            evt = {"containerID": metric[0],
                    "timestamp": str(metric[1]),
                    "type":"ReeferTelemetries",
                    "payload": str(metric)}
            self.metricsProducer.publishEvent(evt,"containerID")
            
    # Need to support asynchronous HTTP Request, return 202 accepted while starting 
    # the processing of generating events. The HTTP header needs to return a
    # location to get the status of the simulator task    
    @track_requests
    @swag_from('controlapi.yml')
    def post(self):
        logging.info("post control received: ")
        control = request.get_json(force=True)
        logging.info(control)
        if not 'containerID' in control:
            abort(400) 
        
        nb_records = int(control["nb_of_records"])
        if control["simulation"] == ReeferSimulator.SIMUL_POWEROFF:
            metrics=self.simulator.generatePowerOffTuples(control["containerID"],nb_records,control["product_id"])
        elif  control["simulation"]  == ReeferSimulator.SIMUL_CO2:
            metrics=self.simulator.generateCo2Tuples(control["containerID"],nb_records,control["product_id"])
        elif  control["simulation"]  == ReeferSimulator.SIMUL_O2:
            metrics=self.simulator.generateO2Tuples(control["containerID"],nb_records,control["product_id"])
        elif  control["simulation"]  == ReeferSimulator.SIMUL_TEMPERATURE:
            metrics=self.simulator.generateTemperatureTuples(control["containerID"],nb_records,control["product_id"])
        elif  control["simulation"]  == ReeferSimulator.NORMAL:
            metrics=self.simulator.generateNormalRecords(control["containerID"],nb_records,control["product_id"])
        else:
            return {"error":"Wrong simulation controller data"},404
    
        self.sendEvents(metrics)
            
        return { "reason": "Simulation started for " + str(nb_records) + " records"},202
    


api.add_resource(SimulationController, "/control")