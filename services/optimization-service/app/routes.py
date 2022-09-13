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
import threading

from app import app
from flask import jsonify, abort, request
from .optimizer import Optimizer


@app.route('/optimization-service', methods=['POST'])
def execute_circuit():
    print(request.json)
    app.logger.info(request.json)
    """Execute a given quantum circuit on a specified quantum computer."""

    app.logger.info('Received Post request to execute circuit...')
    if not request.json:
        app.logger.error("Service currently only supports JSON")
        abort(400, "Only Json supported")

    if 'topic' not in request.json:
        app.logger.error("topic not defined in request")
        abort(400, "topic not defined in request")
    topic = request.json['topic']
    app.logger.info('topic: ' + topic)

    if 'optimizer' not in request.json:
        app.logger.error("optimizer not defined in request")
        abort(400, "optimizer not defined in request")
    optimizer = request.json['optimizer']
    app.logger.info('optimizer: ' + optimizer)
    if not optimizer.lower() in ['cobyla', 'spsa', 'nelder-mead']:
        app.logger.error("optimizer is not supported.")
        abort(400, "optimizer is not supported.")

    if 'initialParameters' not in request.json:
        app.logger.error("initialParameters not defined in request")
        abort(400, "initialParameters not defined in request")
    initialParameters = request.json['initialParameters']
    app.logger.info('initialParameters: ' + str(initialParameters))


    process = Optimizer(topic, optimizer, initialParameters)
    process.start()

    return jsonify('Optimization process for id {} started'.format(topic))
