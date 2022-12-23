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
                    "noise_model": "ibmq_lima",
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
                    "noise_model": "ibmq_lima",
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
                    "circuit": '''gASVlxUAAAAAAACMHXFpc2tpdC5jaXJjdWl0LnF1YW50dW1jaXJjdWl0lIwOUXVhbnR1bUNpcmN1
                                aXSUk5QpgZR9lCiMCl9iYXNlX25hbWWUjAhRQU9BLTExNZSMBG5hbWWUaAaMBV9kYXRhlF2UKIwh
                                cWlza2l0LmNpcmN1aXQucXVhbnR1bWNpcmN1aXRkYXRhlIwSQ2lyY3VpdEluc3RydWN0aW9ulJOU
                                KYGUTn2UKIwJb3BlcmF0aW9ulIwncWlza2l0LmNpcmN1aXQubGlicmFyeS5zdGFuZGFyZF9nYXRl
                                cy5olIwFSEdhdGWUk5QpgZR9lCiMC19kZWZpbml0aW9ulE6MBV9uYW1llIwBaJSMC19udW1fcXVi
                                aXRzlEsBjAtfbnVtX2NsYml0c5RLAIwHX3BhcmFtc5RdlIwGX2xhYmVslE6MCWNvbmRpdGlvbpRO
                                jAlfZHVyYXRpb26UTowFX3VuaXSUjAJkdJR1YowGcXViaXRzlIwecWlza2l0LmNpcmN1aXQucXVh
                                bnR1bXJlZ2lzdGVylIwFUXViaXSUk5QpgZROfZQojAZfaW5kZXiUSwCMBV9yZXBylIwhUXViaXQo
                                UXVhbnR1bVJlZ2lzdGVyKDQsICdxJyksIDAplIwJX3JlZ2lzdGVylGgijA9RdWFudHVtUmVnaXN0
                                ZXKUk5QpgZQojAFxlEsEigikvdioFNT3LYwXUXVhbnR1bVJlZ2lzdGVyKDQsICdxJymUXZQoaCVo
                                JCmBlE59lChoJ0sBaCiMIVF1Yml0KFF1YW50dW1SZWdpc3Rlcig0LCAncScpLCAxKZRoKmgtjAVf
                                aGFzaJSKCAGVdGV29voVdYaUYmgkKYGUTn2UKGgnSwJoKIwhUXViaXQoUXVhbnR1bVJlZ2lzdGVy
                                KDQsICdxJyksIDIplGgqaC1oNIoI0zHZyI5FE9J1hpRiaCQpgZROfZQoaCdLA2gojCFRdWJpdChR
                                dWFudHVtUmVnaXN0ZXIoNCwgJ3EnKSwgMymUaCpoLWg0iggsmSmyWA5jLHWGlGJldJRiaDSKCKgt
                                JPxoSLX4dYaUYoWUjAZjbGJpdHOUKYwUX2xlZ2FjeV9mb3JtYXRfY2FjaGWUTnWGlGJoDCmBlE59
                                lChoD2gSKYGUfZQoaBVOaBZoF2gYSwFoGUsAaBpdlGgcTmgdTmgeTmgfaCB1YmghaDGFlGhBKWhC
                                TnWGlGJoDCmBlE59lChoD4wpcWlza2l0LmNpcmN1aXQubGlicmFyeS5zdGFuZGFyZF9nYXRlcy5y
                                enqUjAdSWlpHYXRllJOUKYGUfZQoaBVOaBaMA3J6epRoGEsCaBlLAGgaXZSMInFpc2tpdC5jaXJj
                                dWl0LnBhcmFtZXRlcmV4cHJlc3Npb26UjBNQYXJhbWV0ZXJFeHByZXNzaW9ulJOUKYGUTn2UKIwS
                                X3BhcmFtZXRlcl9zeW1ib2xzlH2UjBhxaXNraXQuY2lyY3VpdC5wYXJhbWV0ZXKUjAlQYXJhbWV0
                                ZXKUk5SMBmdhbW1hMJSMBHV1aWSUjARVVUlElJOUKYGUfZSMA2ludJSKECShLw1Ze+66TE2BHdLj
                                WBBzYoaUgZR9lGgHaF5zYowfc3ltZW5naW5lLmxpYi5zeW1lbmdpbmVfd3JhcHBlcpSMCmxvYWRf
                                YmFzaWOUk5RDHAEAAAkAAQAAgA0AAAAABgAAAAAAAABnYW1tYTCUhZRSlHOMC19wYXJhbWV0ZXJz
                                lI+UKGhmkIwMX3N5bWJvbF9leHBylGhqQ28BAAAJAAEAAIAPAAAAAgAAgAAAAAABAAAAAAAAADEC
                                AAAAAAAAAAMAAIANAAAAAAYAAAAAAAAAZ2FtbWEwBAAAgAAAAAABAAAAAAAAADEFAACABgAAAAAA
                                AAAAAPA/BgAAgAAAAAABAAAAAAAAADKUhZRSlIwJX25hbWVfbWFwlE51hpRiYWgcTmgdTmgeTmgf
                                aCB1YmghaCVoMYaUaEEpaEJOdYaUYmgMKYGUTn2UKGgPaBIpgZR9lChoFU5oFmgXaBhLAWgZSwBo
                                Gl2UaBxOaB1OaB5OaB9oIHViaCFoNoWUaEEpaEJOdYaUYmgMKYGUTn2UKGgPaE8pgZR9lChoFU5o
                                FmhSaBhLAmgZSwBoGl2UaFYpgZROfZQoaFl9lGhmaGpDHAEAAAkAAQAAgA0AAAAABgAAAAAAAABn
                                YW1tYTCUhZRSlHNobo+UKGhmkGhwaGpDbwEAAAkAAQAAgA8AAAACAACAAAAAAAEAAAAAAAAAMQIA
                                AAAAAAAAAwAAgA0AAAAABgAAAAAAAABnYW1tYTAEAACAAAAAAAEAAAAAAAAAMQUAAIAGAAAAAAAA
                                AAAA8D8GAACAAAAAAAEAAAAAAAAAMpSFlFKUaHROdYaUYmFoHE5oHU5oHk5oH2ggdWJoIWglaDaG
                                lGhBKWhCTnWGlGJoDCmBlE59lChoD4wocWlza2l0LmNpcmN1aXQubGlicmFyeS5zdGFuZGFyZF9n
                                YXRlcy5yeJSMBlJYR2F0ZZSTlCmBlH2UKGgVTmgWjAJyeJRoGEsBaBlLAGgaXZRoVimBlE59lCho
                                WX2UaF2MBWJldGEwlGhhKYGUfZRoZIoRPktQI0f4WYlMT/ZlJ04B1QBzYoaUgZR9lGgHaJ1zYmhq
                                QxsBAAAJAAEAAIANAAAAAAUAAAAAAAAAYmV0YTCUhZRSlHNobo+UKGihkGhwaGpDjwEAAAkAAQAA
                                gA8AAAACAACAAAAAAAEAAAAAAAAAMQMAAAAAAAAAAwAAgA0AAAAABQAAAAAAAABiZXRhMAQAAIAA
                                AAAAAQAAAAAAAAAxBQAAgAYAAAAAAAAAAADwPwYAAIAAAAAAAQAAAAAAAAAxBwAAgAYAAAAAAAAA
                                AAAAQAgAAIAAAAAAAQAAAAAAAAAxlIWUUpRodE51hpRiYWgcTmgdTmgeTmgfaCB1YmghaCWFlGhB
                                KWhCTnWGlGJoDCmBlE59lChoD2hPKYGUfZQoaBVOaBZoUmgYSwJoGUsAaBpdlGhWKYGUTn2UKGhZ
                                fZRoZmhqQxwBAAAJAAEAAIANAAAAAAYAAAAAAAAAZ2FtbWEwlIWUUpRzaG6PlChoZpBocGhqQ28B
                                AAAJAAEAAIAPAAAAAgAAgAAAAAABAAAAAAAAADECAAAAAAAAAAMAAIANAAAAAAYAAAAAAAAAZ2Ft
                                bWEwBAAAgAAAAAABAAAAAAAAADEFAACABgAAAAAAAAAAAPA/BgAAgAAAAAABAAAAAAAAADKUhZRS
                                lGh0TnWGlGJhaBxOaB1OaB5OaB9oIHViaCFoMWg2hpRoQSloQk51hpRiaAwpgZROfZQoaA9oEimB
                                lH2UKGgVTmgWaBdoGEsBaBlLAGgaXZRoHE5oHU5oHk5oH2ggdWJoIWg6hZRoQSloQk51hpRiaAwp
                                gZROfZQoaA9oTymBlH2UKGgVTmgWaFJoGEsCaBlLAGgaXZRoVimBlE59lChoWX2UaGZoakMcAQAA
                                CQABAACADQAAAAAGAAAAAAAAAGdhbW1hMJSFlFKUc2huj5QoaGaQaHBoakNvAQAACQABAACADwAA
                                AAIAAIAAAAAAAQAAAAAAAAAxAgAAAAAAAAADAACADQAAAAAGAAAAAAAAAGdhbW1hMAQAAIAAAAAA
                                AQAAAAAAAAAxBQAAgAYAAAAAAAAAAADwPwYAAIAAAAAAAQAAAAAAAAAylIWUUpRodE51hpRiYWgc
                                TmgdTmgeTmgfaCB1YmghaDFoOoaUaEEpaEJOdYaUYmgMKYGUTn2UKGgPaJUpgZR9lChoFU5oFmiY
                                aBhLAWgZSwBoGl2UaFYpgZROfZQoaFl9lGihaGpDGwEAAAkAAQAAgA0AAAAABQAAAAAAAABiZXRh
                                MJSFlFKUc2huj5QoaKGQaHBoakOPAQAACQABAACADwAAAAIAAIAAAAAAAQAAAAAAAAAxAwAAAAAA
                                AAADAACADQAAAAAFAAAAAAAAAGJldGEwBAAAgAAAAAABAAAAAAAAADEFAACABgAAAAAAAAAAAPA/
                                BgAAgAAAAAABAAAAAAAAADEHAACABgAAAAAAAAAAAABACAAAgAAAAAABAAAAAAAAADGUhZRSlGh0
                                TnWGlGJhaBxOaB1OaB5OaB9oIHViaCFoMYWUaEEpaEJOdYaUYmgMKYGUTn2UKGgPaE8pgZR9lCho
                                FU5oFmhSaBhLAmgZSwBoGl2UaFYpgZROfZQoaFl9lGhmaGpDHAEAAAkAAQAAgA0AAAAABgAAAAAA
                                AABnYW1tYTCUhZRSlHNobo+UKGhmkGhwaGpDbwEAAAkAAQAAgA8AAAACAACAAAAAAAEAAAAAAAAA
                                MQIAAAAAAAAAAwAAgA0AAAAABgAAAAAAAABnYW1tYTAEAACAAAAAAAEAAAAAAAAAMQUAAIAGAAAA
                                AAAAAAAA8D8GAACAAAAAAAEAAAAAAAAAMpSFlFKUaHROdYaUYmFoHE5oHU5oHk5oH2ggdWJoIWg2
                                aDqGlGhBKWhCTnWGlGJoDCmBlE59lChoD2iVKYGUfZQoaBVOaBZomGgYSwFoGUsAaBpdlGhWKYGU
                                Tn2UKGhZfZRooWhqQxsBAAAJAAEAAIANAAAAAAUAAAAAAAAAYmV0YTCUhZRSlHNobo+UKGihkGhw
                                aGpDjwEAAAkAAQAAgA8AAAACAACAAAAAAAEAAAAAAAAAMQMAAAAAAAAAAwAAgA0AAAAABQAAAAAA
                                AABiZXRhMAQAAIAAAAAAAQAAAAAAAAAxBQAAgAYAAAAAAAAAAADwPwYAAIAAAAAAAQAAAAAAAAAx
                                BwAAgAYAAAAAAAAAAAAAQAgAAIAAAAAAAQAAAAAAAAAxlIWUUpRodE51hpRiYWgcTmgdTmgeTmgf
                                aCB1YmghaDaFlGhBKWhCTnWGlGJoDCmBlE59lChoD2iVKYGUfZQoaBVOaBZomGgYSwFoGUsAaBpd
                                lGhWKYGUTn2UKGhZfZRooWhqQxsBAAAJAAEAAIANAAAAAAUAAAAAAAAAYmV0YTCUhZRSlHNobo+U
                                KGihkGhwaGpDjwEAAAkAAQAAgA8AAAACAACAAAAAAAEAAAAAAAAAMQMAAAAAAAAAAwAAgA0AAAAA
                                BQAAAAAAAABiZXRhMAQAAIAAAAAAAQAAAAAAAAAxBQAAgAYAAAAAAAAAAADwPwYAAIAAAAAAAQAA
                                AAAAAAAxBwAAgAYAAAAAAAAAAAAAQAgAAIAAAAAAAQAAAAAAAAAxlIWUUpRodE51hpRiYWgcTmgd
                                TmgeTmgfaCB1YmghaDqFlGhBKWhCTnWGlGJoDCmBlE59lChoD4wWcWlza2l0LmNpcmN1aXQuYmFy
                                cmllcpSMB0JhcnJpZXKUk5QpgZR9lChoHE5oFowHYmFycmllcpRoGEsEaBlLAGgaXZRoHU5oFU5o
                                Hk5oH2ggdWJoIShoJWgxaDZoOnSUaEEpaEJOdYaUYmgMKYGUTn2UKGgPjBZxaXNraXQuY2lyY3Vp
                                dC5tZWFzdXJllIwHTWVhc3VyZZSTlCmBlH2UKGgWjAdtZWFzdXJllGgYSwFoGUsBaBpdlGgcTmgd
                                TmgVTmgeTmgfaCB1YmghaCWFlGhBjCBxaXNraXQuY2lyY3VpdC5jbGFzc2ljYWxyZWdpc3RlcpSM
                                BUNsYml0lJOUKYGUTn2UKGgnSwBoKIwmQ2xiaXQoQ2xhc3NpY2FsUmVnaXN0ZXIoNCwgJ21lYXMn
                                KSwgMCmUaCpqNQEAAIwRQ2xhc3NpY2FsUmVnaXN0ZXKUk5QpgZQojARtZWFzlEsEiggH18OuJPyp
                                oowcQ2xhc3NpY2FsUmVnaXN0ZXIoNCwgJ21lYXMnKZRdlChqOAEAAGo3AQAAKYGUTn2UKGgnSwFo
                                KIwmQ2xiaXQoQ2xhc3NpY2FsUmVnaXN0ZXIoNCwgJ21lYXMnKSwgMSmUaCpqPQEAAGg0iggLD9Lc
                                o9w/+3WGlGJqNwEAACmBlE59lChoJ0sCaCiMJkNsYml0KENsYXNzaWNhbFJlZ2lzdGVyKDQsICdt
                                ZWFzJyksIDIplGgqaj0BAABoNIoI3as2QLwrWLd1hpRiajcBAAApgZROfZQoaCdLA2gojCZDbGJp
                                dChDbGFzc2ljYWxSZWdpc3Rlcig0LCAnbWVhcycpLCAzKZRoKmo9AQAAaDSKCDYTh6nJ2Z3UdYaU
                                YmV0lGJoNIoIsqeB89kT8KB1hpRihZRoQk51hpRiaAwpgZROfZQoaA9qMAEAAGghaDGFlGhBakEB
                                AACFlGhCTnWGlGJoDCmBlE59lChoD2owAQAAaCFoNoWUaEFqRQEAAIWUaEJOdYaUYmgMKYGUTn2U
                                KGgPajABAABoIWg6hZRoQWpJAQAAhZRoQk51hpRiZYwPX29wX3N0YXJ0X3RpbWVzlE6MFF9jb250
                                cm9sX2Zsb3dfc2NvcGVzlF2UjAVxcmVnc5RdlGgtYYwFY3JlZ3OUXZRqPQEAAGGMB19xdWJpdHOU
                                XZQoaCVoMWg2aDpljAdfY2xiaXRzlF2UKGo4AQAAakEBAABqRQEAAGpJAQAAZYwOX3F1Yml0X2lu
                                ZGljZXOUfZQoaCVoAIwMQml0TG9jYXRpb25zlJOUSwBdlGgtSwCGlGGGlIGUaDFqbgEAAEsBXZRo
                                LUsBhpRhhpSBlGg2am4BAABLAl2UaC1LAoaUYYaUgZRoOmpuAQAASwNdlGgtSwOGlGGGlIGUdYwO
                                X2NsYml0X2luZGljZXOUfZQoajgBAABqbgEAAEsAXZRqPQEAAEsAhpRhhpSBlGpBAQAAam4BAABL
                                AV2Uaj0BAABLAYaUYYaUgZRqRQEAAGpuAQAASwJdlGo9AQAASwKGlGGGlIGUakkBAABqbgEAAEsD
                                XZRqPQEAAEsDhpRhhpSBlHWMCV9hbmNpbGxhc5RdlIwNX2NhbGlicmF0aW9uc5SMC2NvbGxlY3Rp
                                b25zlIwLZGVmYXVsdGRpY3SUk5SMCGJ1aWx0aW5zlIwEZGljdJSTlIWUUpSMEF9wYXJhbWV0ZXJf
                                dGFibGWUjB1xaXNraXQuY2lyY3VpdC5wYXJhbWV0ZXJ0YWJsZZSMDlBhcmFtZXRlclRhYmxllJOU
                                KYGUTn2UKIwGX3RhYmxllH2UKGhmap0BAACME1BhcmFtZXRlclJlZmVyZW5jZXOUk5QpgZRdlCho
                                UEsAhpRogUsAhpRor0sAhpRoyEsAhpRo7EsAhpRlYmihaqUBAAApgZRdlCholksAhpRo2ksAhpRo
                                /ksAhpRqEAEAAEsAhpRlYnWMBV9rZXlzlI+UKGhmaKGQjAZfbmFtZXOUj5QoaF5onZB1hpRiaG5O
                                jAdfbGF5b3V0lE6MDV9nbG9iYWxfcGhhc2WUSwCMCGR1cmF0aW9ulE6MBHVuaXSUaCCMCV9tZXRh
                                ZGF0YZROdWIu''',
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
                    "noise_model": "ibmq_lima",
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
