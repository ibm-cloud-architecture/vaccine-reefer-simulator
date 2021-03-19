
if [[ $# -eq 0 ]];then
  kcenv="LOCAL"
else
  kcenv=$1
fi

# vaccine-reefer-simulator_default
if [[ $kcenv == "LOCAL" ]]
then
  docker run -v $(pwd):/app -e KAFKA_BOOTSTRAP_SERVERS=kafka:9092 \
     -e KAFKA_APIKEY="" \
     -e KAFKA_CERT="" \
     -e KAFKA_SASL_MECHANISM="" \
     --network vaccine-monitoring-agent_default  -p 5001:5000  \
      -ti quay.io/ibmcase/vaccine-reefer-simulator bash
else
  source ./scripts/setenv.sh $kcenv
  docker run  -v $(pwd):/app -ti  \
      -e KAFKA_BOOTSTRAP_SERVERS=$KAFKA_BROKERS -e SCHEMA_REGISTRY_URL=$SCHEMA_REGISTRY_URL \
      -e REEFER_TOPIC=$REEFER_TOPIC -e INVENTORY_TOPIC=$INVENTORY_TOPIC \
      -e TRANSPORTATION_TOPIC=$TRANSPORTATION_TOPIC \
      -e KAFKA_USER=$KAFKA_USER -e KAFKA_PASSWORD=$KAFKA_PASSWORD\
      -e KAFKA_CERT=$KAFKA_CERT -e APP_VERSION=$APP_VERSION  \
      -e LOGGER_LEVEL=INFO \
      -p 5000:5000 ibmcase/vaccine-reefer-simulator  bash
fi
