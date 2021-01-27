import os,sys
from confluent_kafka import Consumer, KafkaError

KAFKA_BROKERS = os.getenv('KAFKA_BROKERS')
KAFKA_CERT = os.getenv('KAFKA_CERT','')
KAFKA_USER =  os.getenv('KAFKA_USER','token')
KAFKA_PWD =  os.getenv('KAFKA_PWD','')
KAFKA_SASL_MECHANISM=  os.getenv('KAFKA_SASL_MECHANISM','SCRAM-SHA-512')
SOURCE_TOPIC= os.getenv('KAFKA_TOPIC','telemetries')
TOPIC_POLL_S=10

def getConsumerConfiguration(groupID, autocommit):
    options ={
            'bootstrap.servers': KAFKA_BROKERS,
            'group.id': groupID,
            'auto.offset.reset': "earliest",
            'enable.auto.commit': autocommit,
    }
    if (KAFKA_PWD != ''):
        # Set security protocol common to ES on prem and on IBM Cloud
        options['security.protocol'] = 'SASL_SSL'
        # Depending on the Kafka User, we will know whether we are talking to ES on prem or on IBM Cloud
        # If we are connecting to ES on IBM Cloud, the SASL mechanism is plain
        if (KAFKA_USER == 'token'):
            options['sasl.mechanisms'] = 'PLAIN'
        # If we are connecting to ES on OCP, the SASL mechanism is scram-sha-512
        else:
            options['sasl.mechanisms'] = KAFKA_SASL_MECHANISM
        # Set the SASL username and password
        options['sasl.username'] = KAFKA_USER
        options['sasl.password'] = KAFKA_PWD
    # If we are talking to ES on prem, it uses an SSL self-signed certificate.
    # Therefore, we need the CA public certificate for the SSL connection to happen.
    if (os.path.isfile(KAFKA_CERT)):
        options['ssl.ca.location'] = KAFKA_CERT

    # Print out the producer configuration
    printConsumerConfiguration(options)
    return options

    
def printConsumerConfiguration(options):
    # Printing out consumer config for debugging purposes        
    print("[KafkaConsumer] - This is the configuration for the consumer:")
    print("[KafkaConsumer] - -------------------------------------------")
    print('[KafkaConsumer] - Bootstrap Server:      {}'.format(options['bootstrap.servers']))
    print('[KafkaConsumer] - Topic:                 {}'.format(SOURCE_TOPIC))
    print('[KafkaConsumer] - Topic timeout:         {}'.format(TOPIC_POLL_S))
    if (KAFKA_PWD != ''):
        # Obfuscate password
        if (len(options['sasl.password']) > 3):
            obfuscated_password = options['sasl.password'][0] + "*****" + options['sasl.password'][len(options['sasl.password'])-1]
        else:
            obfuscated_password = "*******"
        print('[KafkaConsumer] - Security Protocol:     {}'.format(options['security.protocol']))
        print('[KafkaConsumer] - SASL Mechanism:        {}'.format(options['sasl.mechanisms']))
        print('[KafkaConsumer] - SASL Username:         {}'.format(options['sasl.username']))
        print('[KafkaConsumer] - SASL Password:         {}'.format(obfuscated_password))
        print('[KafkaConsumer] - SSL CA Location:       {}'.format(options['ssl.ca.location']))
    print('[KafkaConsumer] - Offset Reset:          {}'.format(options['auto.offset.reset']))
    print('[KafkaConsumer] - Autocommit:            {}'.format(options['enable.auto.commit']))
    print("[KafkaConsumer] - -------------------------------------------")
    
# Prints out and returns the decoded events received by the consumer
def traceResponse(msg):
    print('[KafkaConsumer] - Next Message consumed from {} partition: [{}] at offset: {}\n\tkey: {}\n\tvalue: {}'
                .format(msg.topic(), msg.partition(), msg.offset(), msg.key().decode('utf-8'), msg.value().decode('utf-8')))

# Polls for next event
def pollNextEvent(consumer):
    # Poll for messages
    msg = consumer.poll(timeout=TOPIC_POLL_S)
    # Validate the returned message
    if msg is None:
        print("[KafkaConsumer] - [INFO] - No new messages on the topic")
    elif msg.error():
        if ("PARTITION_EOF" in msg.error()):
            print("[KafkaConsumer] - [INFO] - End of partition")
        else:
            print("[KafkaConsumer] - [ERROR] - Consumer error: {}".format(msg.error()))
    else:
        # Print the message
        traceResponse(msg)




def parseArguments():
    nb_records = 1
    if len(sys.argv) > 1:
        nb_records = int(sys.argv[1])
    return nb_records

if __name__ == "__main__":
    print("--------- Start Consuming message --------------")
    nb_records = parseArguments()
    consumer_conf = getConsumerConfiguration("TelemetryConsumer-jb", False)
    consumer = Consumer(consumer_conf)
    consumer.subscribe([SOURCE_TOPIC])
    try:
        for i in range(0,nb_records):
            pollNextEvent(consumer)
    except KeyboardInterrupt:
        consumer.close()
        sys.exit(0)