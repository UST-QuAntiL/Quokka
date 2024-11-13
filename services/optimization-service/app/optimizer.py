# ******************************************************************************
#  Copyright (c) 2020 University of Stuttgart
#
#  See the NOTICE file(s) distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************


import time
from multiprocessing import Process
import scipy.optimize as optimize
from app import app
import requests

from .plot import visualizeOptimizationLandscape, figure_to_base64

class Optimizer (Process):
    def __init__(self, topic, optimizer, parameters, endpoint):
        super().__init__()
        self.topic = topic
        self.optimizer = optimizer
        self.parameters = parameters
        self.camundaEndpoint = endpoint
        self.return_address = None
        print('endpoint', self.camundaEndpoint)
        self.pollingEndpoint = self.camundaEndpoint + '/external-task'
        self.optimizationHistory = []


    def run(self):
        print("Starting optimization")
        print(self.parameters)

        def decoyfunction(opt_parameters, *args):
            app.logger.info(opt_parameters[0])
            app.logger.info('publish' + str(opt_parameters))

            opt_parameters = fix_parameters_list(opt_parameters)

            optimization_landscape = "Optimization landscapes are currently only available for optimization processes with 2 optimization parameters"
            if len(self.optimizationHistory) > 1 and len(self.optimizationHistory[0]["params"]) == 2:
                optimization_landscape = visualizeOptimizationLandscape(self.optimizationHistory)

            # send response
            if optimization_landscape == "Optimization landscapes are currently only available for optimization processes with 2 optimization parameters":
                print("sending response without visualization")
                body = {
                    "workerId": "optimization-service",
                    "variables":
                        {"optimizedParameters": {"value": str(opt_parameters), "type": "String"},
                         "optimizationHistory": {"value": str(self.optimizationHistory), "type": "String"}}
                }
            else:
                print("sending response with visualization")
                body = {
                    "workerId": "optimization-service",
                    "variables":
                        {"optimizedParameters": {"value": str(opt_parameters), "type": "String"},
                         "optimizationHistory": {"value": str(self.optimizationHistory), "type": "String"},
                         "optimizationLandscape": {"value": optimization_landscape, "type": "File", "valueInfo": {"filename": "optimizationLandscape.png", "mimetype":"application/png", "encoding":"base64"}}}
                }
            print("returning optimizationhistory")
            if self.return_address:
                app.logger.info(self.pollingEndpoint + '/' + self.return_address + '/complete' + ' body: ' + str(body))
                response = requests.post(self.pollingEndpoint + '/' + self.return_address + '/complete',
                                     json=body)
                app.logger.info(response)
            returned_objective_value = self.poll()
            self.optimizationHistory.append({"obj_value": returned_objective_value, "params": opt_parameters})
            return returned_objective_value

            res = optimize.minimize(decoyfunction, self.parameters, method=self.optimizer)
            final_parameters = fix_parameters_list(res.x)
        print(res)
        # send final result
        body = {
            "workerId": "optimization-service",
            "variables":
                {"converged": {"value": "true", "type": "String"},
                 "optimizedParameters": {"value": str(final_parameters), "type": "String"}
                 }
        }
        app.logger.info(self.pollingEndpoint + '/' + self.return_address + '/complete' + ' body: ' + str(body))
        response = requests.post(self.pollingEndpoint + '/' + self.return_address + '/complete',
                                 json=body)
        app.logger.info(response)
        
    def poll(self):
        polling_timer = 1
        while(True):
            app.logger.info('Polling for new external tasks at the Camunda engine with URL: {}'.format(self.pollingEndpoint))
            print('Polling for new external tasks at the Camunda engine with URL: ', self.pollingEndpoint)

            body = {
                "workerId": "optimization-service",
                "maxTasks": 1,
                "topics":
                    [{"topicName": self.topic,
                      "lockDuration": 100000000,
                      "variables": ["objValue"]
                      }]
            }

            try:
                response = requests.post(self.pollingEndpoint + '/fetchAndLock', json=body)
                if response.status_code == 200:
                    app.logger.info('in 200')
                    app.logger.info(response.json())
                    for externalTask in response.json():
                        app.logger.info('External task with ID for topic ' + str(externalTask.get('topicName')) + ': ' + str(
                            externalTask.get('activityId')))
                        self.return_address = externalTask.get('id')
                        variables = externalTask.get('variables')
                        if externalTask.get('topicName') == self.topic:
                            if ('objValue' in variables):
                               app.logger.info(variables)
                               return float(variables.get("objValue").get("value"))
            except Exception as e:
                print('Exception during polling!')
                print(e)
            time.sleep(polling_timer)
            if polling_timer < 7:
                polling_timer = polling_timer+1

def fix_parameters_list(broken_list):
    fixed_list = []
    for parameter in broken_list:
        fixed_list.append(parameter)

    return fixed_list