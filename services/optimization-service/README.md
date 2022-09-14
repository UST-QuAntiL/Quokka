# Optimization Service
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

The circuit enables the use of optimization libraries such as [Scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html) or [Qiskit Terra](https://github.com/Qiskit/qiskit-terra/tree/main/qiskit/algorithms/optimizers).

This service decouples the optimization process from the other components.
Thus, objective functions, cost functions, and other methods typically directly integrated into the optimizer can be executed in a loosely coupled fashion.

Currently, the service can be configured to subscribe to a topic provided by a [Camunda BPMN engine](https://camunda.com/platform-7/workflow-engine) and to retrieve optimization requests from there.
In the future, it can be extended to support messaging systems, such as [RabbitMQ](https://www.rabbitmq.com/) or [Apache Kafka](https://kafka.apache.org/).

## Running the Service
The easiest way to get start is using a pre-built Docker image:

``docker run -p 5074:5074 planqk/optimization-service``

Alternatively, the service can be built manually:
1. Clone the repository using ``git clone https://github.com/UST-QuAntiL/Quokka.git``
2. Navigate to the corresponding folder within the cloned repository ``cd Quokka/services/optimization-service``
3. Build the Docker container: ``docker build -t optimization-service .``
4. Run the Docker container: ``docker run -p 5074:5074 optimization-service``

Then the service can be accessed via: [http://127.0.0.1:5074](http://127.0.0.1:5074).

## API Documentation

### Initialize an Optimization Process

An optimization process can be started by sending a request to [http://127.0.0.1:5074/optimization-service](http://127.0.0.1:5074/optimization-service).
The format is as follows:
````json
{
  "topic": "exampleTopic",
  "optimizer": "Cobyla",
  "initialParameters": [
    0,
    0
  ]
}
````

### Optimization with Camunda

The Camunda endpoint for requests has to be set as an environment variable ``CAMUNDA_ENDPOINT`` available to the service.

Once the optimization process is initialized, it is polling for objective values - values describing the quality of the solution for the recommended parameters - at the Camunda endpoint.
The value must be saved in a variable called ``objValue``.

Once new parameters were generated based on the previous objective value, they are sent to the Camunda task that sent the objective value.

An example showcasing this process can be found [here](https://github.com/UST-QuAntiL/Quokka).

## Developer Guide

### Setup (exemplary for ubuntu 18.04): 
```shell
git clone https://github.com/UST-QuAntiL/Quokka.git
cd Quokka/services/optimization-service

# if virtualenv is not installed
sudo -H pip install virtualenv

# create new virtualenv called 'venv'
virtualenv venv

# activate virtualenv; in Windows systems activate might be in 'venv/Scripts'
source venv/bin/activate

#install application requirements.
pip install -r requirements.txt
```

### Execution:
Run the application with: ``flask run --port=5074``

## Disclaimer of Warranty
Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.

## Haftungsausschluss
Dies ist ein Forschungsprototyp. Die Haftung für entgangenen Gewinn, Produktionsausfall, Betriebsunterbrechung, entgangene Nutzungen, Verlust von Daten und Informationen, Finanzierungsaufwendungen sowie sonstige Vermögens- und Folgeschäden ist, außer in Fällen von grober Fahrlässigkeit, Vorsatz und Personenschäden, ausgeschlossen.

## Acknowledgements
The initial code contribution has been supported by the project [SEQUOIA](https://www.iaas.uni-stuttgart.de/forschung/projekte/sequoia/) funded by the [Baden-Wuerttemberg Ministry of the Economy, Labour and Housing](https://wm.baden-wuerttemberg.de/).