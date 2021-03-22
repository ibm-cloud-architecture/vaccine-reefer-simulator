# Refrigerated container ML Simulator _(simulator)_

The _simulator_ component is a Python-based application for generating anomalous data events for refrigerated shipping containers (also known as 'reefers'). This code is part of the Vaccine Cold Chain monitoring solution, and helps to control the test and the demonstration of the cold chain monitoring scenario or the anomaly detection use case.

This implementation illustrates the following technologies:

* Flask, with blueprint, flasgger.Swagger, prometheus metrics
* Kafka producer code using Confuent-python library
* Integration with Health for kubernetes deployment
* Sensor simulator using numpy, Pandas to generate tuples and simulated data
* Use of gnunicorn for serving the webapp in production
* Vuejs application connect to Server Side End point from another service
* Dynamic end point URL injection to the Vuejs via a REST end point (see `api/freezerURL.py`)
* Vuejs and gauge implemented with
* Docker-compose to run locally
* Use gipops and Kustomize for deployment. This is declared in a separate [gitops repository](https://github.com/ibm-cloud-architecture/vaccine-gitops) under `apps` folder.

You can read more of the solution in [this site](https://ibm-cloud-architecture.github.io/vaccine-solution-main/).

The last updated detailed documentation of this component is under [the Reefer Simulator IoT design chapter](https://ibm-cloud-architecture.github.io/vaccine-solution-main/solution/reefer-iot/).

## Build

To build the local image use `./script/buildAll.sh` which runs:

```shell
docker build -t ibmcase/vaccine-reefer-simulator .
docker push ibmcase/vaccine-reefer-simulator
```

The build includes a user interface in Vuejs and the Flask app.

## Run locally

We have different modes to run the simulator locally depending of the target Kafka cluster.

### Run with local Kafka

The repository includes a sample `docker-compose.yaml` which you can use to run a single-node Kafka cluster on your local machine.

* To start Kafka locally, run `docker-compose up -d`. This will start Kafka, Zookeeper, and the Reefer manager service, all connected via a Docker network on your machine, which you can find the name of by running `docker network list`.

We did not mount any folder to persist Kafka topics data, so each time you start this cluster you must create the `telemetries` topic with the command: `./scripts/createTopics.sh`.

You can always validate the list of topics with the command: `./scripts/listTopics.sh`

* For development purpose, you can start a docker image with a Python environment using the command:

```shell
./scripts/startPythonEnv.sh
# then in the container shell start the app
python app.py
```

Access the OpenAPI doc at [http://localhost:5000/apidocs](http://localhost:5000/apidocs).

* Use the following command to send 20 simulated temperatures

```
curl -X POST http://localhost:5000/control -d "{\"containerID\": \"C01\",\"nb_of_records\": 20,\"product_id\": \"P01\",\"simulation\": \"tempgrowth\"}"
```

The response is a string of tuples like:

```
[('C01', '2021-03-19 02:48:25', 'P01', -50.66101485, -50., 18.6447905, 3.65012681, 0, 1, 4, 21.75044215, 78.3859634, 40.7754046, 7.81047338, True, True, True, '37.8226902168957', '-122.324895', 0), ('C01', '2021-03-19 02:53:25', 'P01', -50.60219959, -50., 18.06471888, 2.27853715, 0, 1, 3, 21.38479556, 78.68539182, 40.37011913, 6.44987377, True, True, True, '37.8226902168957', '-122.324895', 0), ('C01', '2021-03-19 02:58:25', 'P01', -50.63849678, -50., 19.77104538, 2.79465754, 0, 1, 5, 19.55180659, 77.93256727, 41.7870542, 8.3963486, True, True, True, '37.8226902168957', '-122.324895', 0), ('C01', '2021-03-19 03:03:25', 'P01', -52.43289337, -50., 17.86306113, 1.80923096, 0, 1, 4, 18.95530879, 78.34202763, 39.11963127, 6.85136766, True, True, True, '37.8226902168957', '-122.324895', 0),...
```

Where the columns are: 

```
[“container_id”, “measurement_time”, “product_id”,
 “temperature”, “target_temperature”, “ambiant_temperature”,
 “kilowatts”, “time_door_open”,
 “content_type”, “defrost_cycle”,
 “oxygen_level”, “nitrogen_level”, “humidity_level”, “carbon_dioxide_level”,
  “fan_1”, “fan_2", “fan_3”, “latitude”, “longitude”, “maintenance_required”
```

* Verify the telemetries records are in the topic: `./scripts/verifyTelemetrieTopicContent.sh`

### Start the User Interface

The `ui` folder includes a Vuejs app which can be started by doing the following:

```shell
export VUE_APP_SERVER_URL=http://localhost:5000
# under ui folder
yarn serve
```

Then point your web browser to [http://localhost:4200/](http://localhost:4200/#/), you should get a list of existing containers and then once selecting one of them, you should see the simulator controller page:

![](./docs/simulator.png)

See the demonstration script in [this note](https://ibm-cloud-architecture.github.io/vaccine-solution-main/use-cases/cold-chain/#scenario-script).

### Run the simulator as a standalone program

It is possible to use the simulator as a standalone tool to create csv file. Here is an example on how to do that using python:

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

## Deploy and run on OpenShift

We are using a separate gitops repository to manage the deploy of the application on OpenShift. See for example [this lab](https://ibm-cloud-architecture.github.io/vaccine-solution-main/use-cases/cold-chain/#tldr-one-click-deploy) to understand how the simulator is deployed.

### Usage

Once deployed, you can access the Swagger-based REST API via the defined route and trigger the simulation controls.

1. To determine the route, use the `oc get route vaccine-reefer-simulator` command and go to the URL specified in the `HOST/PORT` field in your browser.
2. From there, drill down into the `POST /control` section and click **Try it out!**.
3. Enter any of the following options for the fields pre-populated in the `control` body:

  - Container: `C01, C02, C03, C04`
  - Product: `P01, P02, P03, P04`
  - Simulation: `poweroff, temperature, tempgrowth, co2sensor, o2sensor, normal`
  - Number of records: A positive integer

4. Click **Execute**
5. Verify the telemetries are created in the `telemetries` topic.

### Testing

#### Unit test the Simulator

The test coverage for this project is not great yet. 

```shell
cd ./scripts
./startPythonEnv.sh
root@1de81b16f940:/# python test/unit/TestSimulator.py
```

#### Functional testing

To be able to run locally, you need a Kafka simple cluster. We have defined a docker compose for that, see [previous section](#run).

Use the web browser or a Postman to go to the URL: [http://localhost:8080/control](http://localhost:8080/control) and do a POST. Here is an image of the open API UI:

![](images/simulapp-control-openapi.png)


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

We have improvement requests and bug reports via git issues in this project.
