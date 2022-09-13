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
        token = os.getenv('token')
        response = self.client.post(
            "/execution-service",
            data=json.dumps({"circuit":"OPENQASM 2.0; include \"qelib1.inc\";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;",
                 "provider" : "IBM",
                 "qpu" : "aer_qasm_simulator",
                 "credentials" : {"token": token},
                 "shots" : 1000,
                 "noise_model" : "ibmq_lima"}),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    def test_noisy_de_simulator(self):
        token = os.getenv('de_token')
        response = self.client.post(
            "/execution-service",
            data=json.dumps({"circuit":"OPENQASM 2.0; include \"qelib1.inc\";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;",
                 "provider" : "IBM",
                 "qpu" : "aer_qasm_simulator",
                 "credentials" : {"token": token, "hub": "fraunhofer-de", "group": "fhg-all", "project": "estu04", "url":"https://auth.de.quantum-computing.ibm.com/api"},
                 "shots" : 1000,
                 "noise_model" : "ibmq_ehningen"}),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    def test_noiseless_simulator(self):
        token = os.getenv('token')
        response = self.client.post(
            "/execution-service",
            data=json.dumps({"circuit":"OPENQASM 2.0; include \"qelib1.inc\";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;",
                 "provider" : "IBM",
                 "qpu" : "aer_qasm_simulator",
                 "credentials" : {"token": token},
                 "shots" : 1000,
                 }),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    def test_noisy_measurement_simulator(self):
        token = os.getenv('token')
        response = self.client.post(
            "/execution-service",
            data=json.dumps({"circuit":"OPENQASM 2.0; include \"qelib1.inc\";qreg q[4];creg c[4];x q[0]; x q[2];barrier q;h q[0];cu1(pi/2) q[1],q[0];h q[1];cu1(pi/4) q[2],q[0];cu1(pi/2) q[2],q[1];h q[2];cu1(pi/8) q[3],q[0];cu1(pi/4) q[3],q[1];cu1(pi/2) q[3],q[2];h q[3];measure q -> c;",
                 "provider" : "IBM",
                 "qpu" : "aer_qasm_simulator",
                 "credentials" : {"token": token},
                 "shots" : 1000,
                 "noise_model" : "ibmq_lima",
                 "only_measurement_errors": "True"}),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        print(response.get_json())

    # as comment due to qpu waiting times
    # def test_qpu_execution(self):
    #     token = os.getenv('token')
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
    #     token = os.getenv('token')
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
