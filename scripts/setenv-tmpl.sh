
if [[ $# -eq 0 ]];then
  kcenv="LOCAL"
else
  kcenv=$1
fi

export KAFKA_MAIN_TOPIC=telemetries
case "$kcenv" in
   OCP)
    export KAFKA_BROKERS=eda-dev-kafka-bootstrap-eventstreams.gse-eda-2021-1-0143c5dd31acd8e030a1d6e0ab1380e3-0000.us-east.containers.appdomain.cloud:443
    # Set the SSL certificate location if you are working against an Event Streams instance on OCP
    # Below where appsody will place the certificates you include in the certs folder of this project
    # If you are building the docker image yourself and then running it standalone or through docker compose, you
    # will most likely need to update the cert path
    export KAFKA_CERT="/app/certs/es-cert.pem"
    export SCHEMA_REGISTRY_URL=https://j....
    # Set these if you are using Event Streams on prem or on IBM Cloud
    export KAFKA_USER=app-scram
    export KAFKA_PASSWORD=<>
    ;;
   LOCAL)
    export KAFKA_BROKERS=kafka:9092
    ;;
   CLOUD)
  export KAFKA_PWD=<>
  export KAFKA_USER=token
  export KAFKA_BROKERS=broker-0-...
   ;;
esac

export APP_VERSION=v0.0.2

