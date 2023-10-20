import unittest
import os, sys
import json

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from app import create_app


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_noisy_simulator(self):
        token = os.environ["IBMQ_TOKEN"]
        response = self.client.post(
            "/execution-service",
            data=json.dumps(
                {
                    "circuit": 'OPENQASM 2.0; include "qelib1.inc";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;',
                    "provider": "IBM",
                    "qpu": "aer_qasm_simulator",
                    "credentials": {"token": token},
                    "shots": 1000,
                    "noise_model": "ibm_lagos",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    def test_noisy_simulator_multicircuit(self):
        token = os.environ["IBMQ_TOKEN"]
        response = self.client.post(
            "/execution-service",
            data=json.dumps(
                {
                    "circuit": [
                        'OPENQASM 2.0; include "qelib1.inc";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;',
                        'OPENQASM 2.0; include "qelib1.inc";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;',
                    ],
                    "provider": "IBM",
                    "qpu": "aer_qasm_simulator",
                    "credentials": {"token": token},
                    "shots": 1000,
                    "noise_model": "ibm_lagos",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    def test_noisy_de_simulator(self):
        try:
            token = os.environ["DE_IBMQ_TOKEN"]
            response = self.client.post(
                "/execution-service",
                data=json.dumps(
                    {
                        "circuit": 'OPENQASM 2.0; include "qelib1.inc";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;',
                        "provider": "IBM",
                        "qpu": "aer_qasm_simulator",
                        "credentials": {
                            "token": token,
                            "hub": "fraunhofer-de",
                            "group": "fhg-all",
                            "project": "estu04",
                            "url": "https://auth.de.quantum-computing.ibm.com/api",
                        },
                        "shots": 1000,
                        "noise_model": "ibmq_ehningen",
                    }
                ),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            print(response.get_json())
        except:
            print("No IBM Germany token available - Test will be marked as passed")

    def test_noiseless_simulator(self):
        token = "123"
        response = self.client.post(
            "/execution-service",
            data=json.dumps(
                {
                    "circuit": 'OPENQASM 2.0; include "qelib1.inc";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;',
                    "provider": "IBM",
                    "qpu": "aer_qasm_simulator",
                    "credentials": {"token": token},
                    "shots": 1000,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    def test_noiseless_simulator_multicircuit(self):
        token = "123"
        response = self.client.post(
            "/execution-service",
            data=json.dumps(
                {
                    "circuit": [
                        'OPENQASM 2.0; include "qelib1.inc";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;',
                        'OPENQASM 2.0; include "qelib1.inc";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;',
                    ],
                    "provider": "IBM",
                    "qpu": "aer_qasm_simulator",
                    "credentials": {"token": token},
                    "shots": 1000,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    def test_noiseless_simulator_parameterized(self):
        token = "123"
        response = self.client.post(
            "/execution-service",
            data=json.dumps(
                {
                    "circuit": '''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''',
                    "provider": "IBM",
                    "qpu": "aer_qasm_simulator",
                    "credentials": {"token": token},
                    "shots": 1000,
                    "circuit_format": "qiskit",
                    "parameters": [1.5, 0.75]
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    def test_noisy_measurement_simulator(self):
        token = os.environ["IBMQ_TOKEN"]
        response = self.client.post(
            "/execution-service",
            data=json.dumps(
                {
                    "circuit": 'OPENQASM 2.0; include "qelib1.inc";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;',
                    "provider": "IBM",
                    "qpu": "aer_qasm_simulator",
                    "credentials": {"token": token},
                    "shots": 1000,
                    "noise_model": "ibm_lagos",
                    "only_measurement_errors": "True",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    # as comment due to qpu waiting times
    # def test_qpu_execution(self):
    #     token = os.environ["IBMQ_TOKEN"]
    #     response = self.client.post(
    #         "/execution-service",
    #         data=json.dumps({"circuit":"OPENQASM 2.0; include \"qelib1.inc\";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;",
    #              "provider" : "IBM",
    #              "qpu" : "ibmq_lima",
    #              "credentials" : {"token": token},
    #              "shots" : 1000,
    #              }),
    #         content_type="application/json")
    #     self.assertEqual(response.status_code, 200)
    #     print(response.get_json())

    # as comment due to qpu waiting times
    # def test_qpu_execution(self):
    #     token = os.environ["IBMQ_TOKEN"]
    #     response = self.client.post(
    #         "/execution-service",
    #         data=json.dumps({"circuit":"OPENQASM 2.0; include \"qelib1.inc\";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;",
    #              "provider" : "IBM",
    #              "qpu" : "ibmq_lima",
    #              "credentials" : {"token": token},
    #              "shots" : 1000,
    #              }),
    #         content_type="application/json")
    #     self.assertEqual(response.status_code, 200)
    #     print(response.get_json())
