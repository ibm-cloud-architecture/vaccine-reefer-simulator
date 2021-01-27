from confluent_kafka import Producer 
import json, datetime, logging
import os

KAFKA_BROKERS = os.getenv('KAFKA_BROKERS','')
KAFKA_CERT = os.getenv('KAFKA_CERT','')
KAFKA_USER =  os.getenv('KAFKA_USER','')
KAFKA_PASSWORD =  os.getenv('KAFKA_PASSWORD','')
KAFKA_SASL_MECHANISM=  os.getenv('KAFKA_SASL_MECHANISM','SCRAM-SHA-512')
TOPIC_NAME=os.getenv("KAFKA_MAIN_TOPIC","telemetries")


class MetricsEventsProducer:

    def __init__(self):
        self.prepareProducer("ReeferTelemetryProducer")
        print("MetricsEventsProducer")
        
    def prepareProducer(self,groupID):
        options ={
                'bootstrap.servers':  KAFKA_BROKERS,
                'group.id': groupID,
                'delivery.timeout.ms': 15000,
                'request.timeout.ms' : 15000
        }
        print("kafka-user: " + KAFKA_USER)
        if (KAFKA_USER != ''):
            options['security.protocol'] = 'SASL_SSL'
            options['sasl.mechanisms'] = KAFKA_SASL_MECHANISM
            options['sasl.username'] = KAFKA_USER
            options['sasl.password'] = KAFKA_PASSWORD

        if (KAFKA_CERT != '' ):
            options['ssl.ca.location'] = KAFKA_CERT

        logging.info("--- This is the configuration for the producer: ---")
        logging.info('[KafkaProducer] - {}'.format(options))
        logging.info("---------------------------------------------------")
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
        logging.info("Send " + dataStr + " with key " + keyName + " to " + TOPIC_NAME)
        
        self.producer.produce(TOPIC_NAME,
                           key=eventToSend[keyName],
                           value=dataStr.encode('utf-8'),
                           callback=self.delivery_report)
        self.producer.flush()
        # self.producer.poll(5)

    def close(self):
        self.producer.close()