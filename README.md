# Refrigerated container ML Simulator _(simulator)_

The _simulator_ component is a Python-based application for generating anomalous data events for refrigerated shipping containers (also known as 'reefers'). This code is part of the Vaccine Cold Chain monitoring solution, and helps to control the test and the demonstration of the monitoring part of this solution. 

You can read more of the solution in [this site](https://ibm-cloud-architecture.github.io/vaccine-solution-main/). 
The last updated detailed documentation of this component is under [this chapter](https://ibm-cloud-architecture.github.io/vaccine-solution-main/solution/reefer-iot/).

## Installation

The application is built using [Appsody](https://appsody.dev) using the [python flask appsody stack](https://github.com/appsody/stacks/tree/master/incubator/python-flask).  The Appsody CLI is required locally to build and deploy the application properly, while the Appsody Operator is required on the target cluster to deploy the generated `AppsodyApplication`.

## Build

To build the local image:

```shell
appsody build -t ibmcase/vaccine-reefer-simulator:1.0.0
```

If you want to build and push to remote registry:

1. Ensure you are logged in to the desired remote Docker registry through your local Docker client.
2. The `appsody build -t ibmcase/vaccine-reefer-simulator:v1.0.0 --push` command will build and push the application's image to the specified remote image registry.

Once pushed we can deploy it to OpenShift.

## Run locally

The repository includes a sample `docker-compose.yaml` which you can use to run a single-node Kafka cluster on your local machine. To start Kafka locally, run `docker-compose up`. This will start Kafka, Zookeeper, and also create a Docker network on your machine, which you can find the name of by running `docker network list`.

`appsody run --network network_name --docker-options "--env KAFKA_BROKERS=$KAFKA_BROKERS --env KAFKA_APIKEY=$KAFKA_APIKEY --env KAFKA_CERT=$KAFKA_CER" <docker image name>`

or using docker run once the image is built.

`docker run -e KAFKA_BROKERS=$KAFKA_BROKERS -e KAFKA_APIKEY=$KAFKA_APIKEY -e KAFKA_CERT=$KAFKA_CERT -p 8080:8080 ibmcase/vaccine-reefer-simulator:v1.0.0`

[http://localhost:8080/](http://localhost:8080/) will go directly to the Open API user interface.

### Run locally with remote Event Streams on OCP

If you want to remote connect to Event Streams on OpenShift, you need to get the external URL for the bootstrap end point and the TLS certificate in the form of a .pem file. The following commands can help you do so.

```shell
# login to OpenShift
oc login --token=L0.... --server=https://api.eda-solutions.gse-ocp.net:6443
# Access to the project where event streams run
oc project integration
# Access to Event Streams cluster
cloudctl es init
# From the result get the bootstrap address: some thing like:
# ...-kafka-bootstrap-integration.apps.....:443 
# Get the certificate
cloudctl es certificates --format pem
# Get one of the kafka user defined with the scram-sha-512 authentication
oc get kafkausers -n integration
# For example here is an output: 
# NAME      AUTHENTICATION   AUTHORIZATION
# my-user1  scram-sha-512    simple
```

Set the following environment variables:

```shell
export KAFKA_BROKERS=...-kafka-bootstrap-integration.apps.....:443 
export KAFKA_USER=my-user1
export KAFKA_PWD=$(oc -n integration get secret my-user1 -o jsonpath='{.data.password}'  | base64 --decode)
```

```shell
appsody run --docker-options "-e KAFKA_BROKERS=$KAFKA_BROKERS -e KAFKA_USER=$KAFKA_USER -e KAFKA_PWD=$KAFKA_PWD -v $(pwd)/certs/:/certs"
```


## Running on OpenShift

To run on OpenShift, you will first need to deploy Event Streams using the Operator. See [product documentation here](https://ibm.github.io/event-streams/installing/installing/).

* If not done before, define the config map needed to map to environment variables as defined in the `app-deploy.yaml`.
 
 ```shell
 oc apply -f config/configmap.yaml
 # Verify 
 oc describe configmap reefer-simul-cmap
 ```

### Application deployment

The application can be deployed to a remote OpenShift cluster by using the `appsody deploy` command:

1. There are four required configuration elements for connectivity to IBM Event Streams (Kafka) prior to deployment:

  - A `ConfigMap` named `kafka-brokers` **[Reference Link](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/#event-streams-kafka-brokers_1)**
  - A `ConfigMap` named `kafka-topics` **[Reference Link](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/#event-streams-kafka-topics_1)**
  - A `Secret` named `eventstreams-api-key` **[Reference Link](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/#event-streams-api-key_1)**
  - A `Secret` named `eventstreams-cert-pem` _(if connecting to an on-premise version of IBM Event Streams)_ **[Reference Link](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/#event-streams-certificates)**

## Usage

Once deployed, you can access the Swagger-based REST API via the defined route and trigger the simulation controls.

1. To determine the route, use the `oc get route reefer-simulator` command and go to the URL specified in the `HOST/PORT` field in your browser.
2. From there, drill down into the `POST /control` section and click **Try it out!**.
3. Enter any of the following options for the fields pre-populated in the `control` body:

  - Container: `C01, C02, C03, C04`
  - Product: `P01, P02, P03, P04`
  - Simulation: `poweroff, temperature, co2sensor, o2sensor, normal`
  - Number of records: A positive integer

4. Click **Execute**

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

We have improvement requests and bug reports via git issues in this project.
