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

from app import circuit_executor
from flask import abort, request
from flask_smorest import Blueprint
from app.model.execution_request import ExecutionRequestSchema, ExecutionRequest
from app.model.execution_response import ExecutionResponseSchema, ExecutionResponse


blp = Blueprint(
    "objective",
    __name__,
    description="compute objective value from counts",
)


@blp.route("/execution-service", methods=["POST"])
@blp.arguments(
    ExecutionRequestSchema,
    example=dict(circuit="OPENQASM 2.0; include \"qelib1.inc\"; qreg q[4]; creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;",
                 provider = "IBM",
                 qpu = "aer_qasm_simulator",
                 credentials = {"token": "YOUR TOKEN"},
                 shots = 1000,
                 )
)
@blp.response(200, ExecutionResponseSchema)
def execute_circuit(json: ExecutionRequest):
    """Execute a given quantum circuit on a specified quantum computer."""
    print("request", json)
    return circuit_executor.execute_circuit(json)
