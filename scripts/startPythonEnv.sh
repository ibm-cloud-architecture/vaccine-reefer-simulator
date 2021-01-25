
if [[ $# -eq 0 ]];then
  kcenv="LOCAL"
else
  kcenv=$1
fi
source ./setenv.sh $kcenv

if [[ -z "$IPADDR" ]]
then
    export IPADDR=$(ifconfig en0 |grep "inet " | awk '{ print $2}')
fi

cd ..

if [[ $kcenv == "LOCAL" ]]
then
  docker run -e DISPLAY=$IPADDR:0 -v $(pwd):/home -e KAFKA_BROKERS=$KAFKA_BROKERS \
     -e KAFKA_APIKEY="" \
     -e KAFKA_CERT="" \
     --network kafkanet \
      -ti ibmcase/python37 bash
else
  docker run  -e DISPLAY=$IPADDR:0 -v $(pwd):/home -ti -v $(pwd):/app \
      -e KAFKA_BROKERS=$KAFKA_BROKERS -e SCHEMA_REGISTRY_URL=$SCHEMA_REGISTRY_URL -e REEFER_TOPIC=$REEFER_TOPIC -e INVENTORY_TOPIC=$INVENTORY_TOPIC -e TRANSPORTATION_TOPIC=$TRANSPORTATION_TOPIC -e KAFKA_USER=$KAFKA_USER -e KAFKA_PASSWORD=$KAFKA_PASSWORD -e KAFKA_CERT=$KAFKA_CERT -e APP_VERSION=$APP_VERSION ibmcase/python37  bash
fi
