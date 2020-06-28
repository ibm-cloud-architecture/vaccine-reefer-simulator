# Refrigerated container ML Simulator _(simulator)_

The _simulator_ component is a Python-based application for generating anomalous data events for refrigerated shipping containers (also known as 'reefers').

## Installation

The application is built using [Appsody](https://appsody.dev) as the developer experience tooling using the [python flask appsody stack](https://github.com/appsody/stacks/tree/master/incubator/python-flask).  The Appsody CLI is required locally to build and deploy the application properly, while the Appsody Operator is required on the target cluster to deploy the generated `AppsodyApplication`.

### Run locally

The repository includes a sample `docker-compose.yaml` which you can use to run a single-node Kafka cluster on your local machine. To start Kafka locally, run `docker-compose up`. This will start Kafka, Zookeeper, and also create a Docker network on your machine, which you can find the name of by running `docker network list`.

`appsody run --network network_name --docker-options "--env KAFKA_BROKERS=$KAFKA_BROKERS --env KAFKA_APIKEY=$KAFKA_APIKEY --env KAFKA_CERT=$KAFKA_CER" `

or 

`docker run -e KAFKA_BROKERS=$KAFKA_BROKERS -e KAFKA_APIKEY=$KAFKA_APIKEY -e KAFKA_CERT=$KAFKA_CERT -p 8080:8080 dev.local/reeferiotsimulator`

[http://localhost:8080/](http://localhost:8080/) will go directly to the Open API user interface.

### Docker build

The Docker image can be built from this directory by using the `appsody build` command:

1. Ensure you are logged in to the desired remote Docker registry through your local Docker client.
2. The `appsody build -t ibmcase/vaccine-reefer-simulator:appsody-v1 --push` command will build and push the application's Docker image to the specified remote image registry.

## Running on Kubernetes

To run on Kubernetes, you will first need to deploy Kafka. The easiest way to do that is to use the [Strimzi operator quickstart](https://strimzi.io/quickstarts/). This will deploy a basic Kafka cluster into a `kafka` namespace on your Kubernetes cluster.

You will need to inject the address of your Kafka into your Quarkus application via the `KAFKA_BOOTSTRAP_SERVERS` environment variable. To do this, you can add an `env:` section to your `app-deploy.yaml` that is generated when you run `appsody build`.

```yaml
spec:
  env:
  - name: KAFKA_BOOTSTRAP_SERVERS
    value: my-cluster-kafka-bootstrap.default.svc:9092
```

To get the `value` you need, you can run `kubectl describe kafka -n kafka` and examine the listener address in the status section.

Once you have updated your `app-deploy.yaml` to inject the environment variable, you can run `appsody deploy` to run your Quarkus application on Kubernetes.

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
3. Enter any of the following options for the fields prepopulated in the `control` body:

  - Container: `C01, C02, C03, C04`
  - Product: `P01, P02, P03, P04`
  - Simulation: `poweroff, temperature, co2sensor, o2sensor, normal`
  - Number of records: A positive integer

4. Click **Execute**

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
