from confluent_kafka import Producer 
import json, datetime, logging
import userapp.infrastructure.EventBackboneConfiguration as EventBackboneConfiguration

class MetricsEventsProducer:

    def __init__(self):
        self.prepareProducer("ReeferTelemetryProducers")
        
    def prepareProducer(self,groupID):
        options ={
                'bootstrap.servers':  EventBackboneConfiguration.getBrokerEndPoints(),
                'group.id': groupID,
        }
        if (EventBackboneConfiguration.hasAPIKey()):
            options['security.protocol'] = 'SASL_SSL'
            options['sasl.mechanisms'] = 'PLAIN'
            options['sasl.username'] = 'token'
            options['sasl.password'] = EventBackboneConfiguration.getEndPointAPIKey()
        if (EventBackboneConfiguration.isEncrypted()):
            options['ssl.ca.location'] = EventBackboneConfiguration.getKafkaCertificate()
        logging.info("Kafka options are:")
        logging.error(options)
        self.producer = Producer(options)


    def delivery_report(self,err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            logging.error( str(datetime.datetime.today()) + ' - Message delivery failed: {}'.format(err))
        else:
            logging.error(str(datetime.datetime.today()) + ' - Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def publishEvent(self, eventToSend, keyName):
        dataStr = json.dumps(eventToSend)
        logging.error("Send " + dataStr + " with key " + keyName + " to " + EventBackboneConfiguration.getTelemetryTopicName())
        
        self.producer.produce(EventBackboneConfiguration.getTelemetryTopicName(),
                           key=eventToSend[keyName],
                           value=dataStr.encode('utf-8'),
                           callback=self.delivery_report)
        self.producer.flush()
        # self.producer.poll(5)

    def close(self):
        self.producer.close()