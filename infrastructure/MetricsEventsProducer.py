from confluent_kafka import Producer 
from kafka.errors import KafkaError
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
        logging.info(options)
        self.producer = Producer(options)


    def delivery_report(self,err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            logging.info( str(datetime.datetime.today()) + ' - Message delivery failed: {}'.format(err))
        else:
            logging.info(str(datetime.datetime.today()) + ' - Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def publishEvent(self, eventToSend, keyName):
        dataStr = json.dumps(eventToSend)
        logging.info(dataStr)
        
        future = self.producer.send(EventBackboneConfiguration.getTelemetryTopicName(),
                           key=eventToSend[keyName],
                           value=dataStr.encode('utf-8'))
        try:
            record_metadata = future.get(timeout=10)
            logging.info(str(datetime.datetime.today()) 
                + ' - Message delivered to {} [{}]'.format(record_metadata.topic(), record_metadata.partition()))
        except KafkaError as ex:
            # Decide what to do if produce request failed...
            logging.error(ex)
        finally:
            self.producer.close()

    def close(self):
        self.producer.close()