# Refrigerated container ML Simulator _(simulator)_

The _simulator_ component is a Python-based application for generating anomalous data events for refrigerated shipping containers (also known as 'reefers'). This code is part of the Vaccine Cold Chain monitoring solution, and helps to control the test and the demonstration of the cold chain monitoring scenario or the anomaly detection use case.

You can read more of the solution in [this site](https://ibm-cloud-architecture.github.io/vaccine-solution-main/).
The last updated detailed documentation of this component is under [this chapter](https://ibm-cloud-architecture.github.io/vaccine-solution-main/solution/reefer-iot/).

## Installation


## Build

To build the local image:

```shell
docker build -t ibmcase/vaccine-reefer-simulator .
docker push ibmcase/vaccine-reefer-simulator
```

## Run locally


### Run with remote Kafka cluster deployed on OpenShift

* Get user and pem from event streams instance to be used:

  ```shell
  # login to OpenShift
  oc login --token=L0.... --server=https://api.eda-solutions.gse-ocp.net:6443
  # Access to the project where event streams run
  oc project eventstreams
  # Access to Event Streams cluster
  cloudctl es init
  # From the result get the bootstrap address: some thing like:
  # ...-kafka-bootstrap-integration.apps.....:443
  # Get the certificate
  cloudctl es certificates --format pem > certs/es-cert.pem
  # Get one of the kafka user defined with the scram-sha-512 authentication
  oc get kafkausers -n eventstreams
  # For example here is an output:
  # NAME      AUTHENTICATION   AUTHORIZATION
  # app-scram  scram-sha-512    simple
  ```
* Decode the user's password using its secret: with `oc -n eventstreams get secret app-scram -o jsonpath='{.data.password}'  | base64 --decode`

* Modify the environment variables in the `scripts/setenv-tmpl.sh` to reflect the user and broker URLs under the OCP condition
* Rename `scripts/setenv-tmpl.sh` to `scripts/setenv-.sh`
* If not done at least one time, build the docker image: ibmcase/vaccine-reefer-simulator with `docker build -t ibmcase/vaccine-reefer-simulator .` as this image will include all the dependencies.
* Launch the python environment: `./scripts/startPythonEnv.sh OCP`

* In the shell session start the app with `python app.py`
* Use your web browser to access [http://localhost:5000](http://localhost:5000) to access the swagger.

### Run the simulator as a standalone program

It is possible to use a standalone tool to create csv file. Here is an example on how to do that using python:

```shell
# Create normal records
python reefer_simulator_tool.py --stype norma --cid C01 --product_id covid-19 --records 1000 --file telemetries.csv 
# Append errors on temperature (18% faulty records)
python reefer_simulator_tool.py --stype temperature --cid C01 --product_id covid-19 --records 700 --file telemetries.csv --append
# Append errors on co2sensor 
python reefer_simulator_tool.py --stype co2sensor --cid C01 --product_id covid-19 --records 700 --file telemetries.csv --append
# append errors for o2sensor
python reefer_simulator_tool.py --stype o2sensor --cid C01 --product_id covid-19 --records 700 --file telemetries.csv --append
```

### Run with local Kafka

The repository includes a sample `docker-compose.yaml` which you can use to run a single-node Kafka cluster on your local machine. To start Kafka locally, run `docker-compose up -d`. This will start Kafka, Zookeeper, and also create a Docker network on your machine, which you can find the name of by running `docker network list`.

Use the startPython environment:

```shell
./scripts/startPythonEnv.sh LOCAL
# then in the container shell
python app.py
```

[http://localhost:8080/](http://localhost:5000/) will go directly to the Open API user interface.


## Running on OpenShift

To run on OpenShift, you will first need to deploy Event Streams using the Operator. See [product documentation here](https://ibm.github.io/event-streams/installing/installing/).

### Application deployment

The application can be deployed to a remote OpenShift cluster by using the deployment config: [deployment](https://github.com/ibm-cloud-architecture/vaccine-reefer-simulator/blob/master/config/app-deployment.yaml)

* Connect to the vaccine project using: `oc project vaccine`
* Create a SCRAM-512-based user: **_(the current implementation of this microservice does not support TLS-based user authentication)_**

  ```shell
  oc get kafkausers -n eventstreams
  # NAME                                CLUSTER   AUTHENTICATION   AUTHORIZATION
  # app-scram                           eda-dev   scram-sha-512    simple
  # app-tls                             eda-dev   tls              simple
  ```

* Modify the `config/configmap.yaml` with the Kafka Broker URL and Topic information.

* Create the necessary configuration information in a ConfigMap via the following command:

   ```shell
   oc apply -f config/configmap.yaml
   ```

* Modify the `config/secret.yaml` with the Kafka user credentials created above.

* Create the necessary configuration information in a Secret via the following command:

  ```shell
  oc apply -f config/secret.yaml
  ```

* Get the secret for the cluster certificate from the `eventstreams` project to your project:

  ```shell
  oc get secret {cluster-name}-cluster-ca-cert -n eventstreams -o yaml | oc apply -f -
  ```

* Modify the following elements of the `containers` section of the Deployment object in the `config/app-deployment.yaml` file:
  *  `envFrom.configMapRef.name` should point to the name of the ConfigMap you created above _(if changed in `config/configmap.yaml`)_
  *  `envFrom.secretRef.name` should point to the name of the Secret you created above _(if changed in `config/secret.yaml`)_
  *  `volumes[0].secret.secretName` should point to the Secret you copied from the `eventstreams` namespace

* Deploy the application:

  ```shell
  oc apply -f config/app-deployment.yaml
  ```

### Usage

Once deployed, you can access the Swagger-based REST API via the defined route and trigger the simulation controls.

1. To determine the route, use the `oc get route vaccine-reefer-simulator` command and go to the URL specified in the `HOST/PORT` field in your browser.
2. From there, drill down into the `POST /control` section and click **Try it out!**.
3. Enter any of the following options for the fields pre-populated in the `control` body:

  - Container: `C01, C02, C03, C04`
  - Product: `P01, P02, P03, P04`
  - Simulation: `poweroff, temperature, co2sensor, o2sensor, normal`
  - Number of records: A positive integer

4. Click **Execute**
5. Verify the telemetries are created in the `telemetries` topic.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

We have improvement requests and bug reports via git issues in this project.
