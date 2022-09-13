# Optimization Service
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


The circuit enables the use of optimization libraries such as [Scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html) or [Qiskit](https://github.com/Qiskit/qiskit-terra/tree/main/qiskit/algorithms/optimizers).

This service decouples the optimization process from the other components. Thus, objective functions, cost functions and other methods typically directly integrated into the optimizer can be executed in a loosely coupled fashion.

Currently, the Camunda engine is supported as a messaging system for this service, however, other messaging systems, e.g., RabbitMQ, can easily be integrated and used instead.

## Running the Application
The easiest way to get start is using a pre-built Docker image:

``docker run -p 5074:5074 planqk/optimization-service``

Alternatively, the application can be built manually:
1. Clone the repository using ``git clone https://github.com/UST-QuAntiL/Quokka.git``
2. Navigate to the repository  ``cd Quokka/services/optimization-service``
3. Build the Docker container: ``docker build -t optimization-service:0.1 .``
4. Run the Docker container: ``docker run -p 5074:5074 optimization-service:0.1``

Then the application can be accessed via: [http://127.0.0.1:5074](http://127.0.0.1:5074).

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
The Camunda endpoint for requsts has to be set as an environment variable ``CAMUNDA_ENDPOINT`` available to the service .

Once the optimization process is initialized, it is polling for objective values - values describing the quality of the solution for the recommended parameters - at the Camunda endpoint.
The value must be saved in a variable called ``objValue``.

Once new parameters were generated on the basis of the previous objective value they are sent to the Camunda task that sent the objective value.

An example showcasing this process can be found [here](https://github.com/UST-QuAntiL/Quokka)


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