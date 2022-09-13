import marshmallow as ma

class ExecutionRequest:
    def __init__(self, circuit, provider, qpu, credentials, shots=1000, noise_model=None, only_measurement_errors=False):
        self.circuit = circuit
        self.provider = provider
        self.qpu = qpu
        self.credentials = credentials
        self.shots = shots
        self.noise_model = noise_model
        self.only_measurement_errors = only_measurement_errors



class ExecutionRequestSchema(ma.Schema):
    circuit = ma.fields.Str(required=True)
    provider = ma.fields.Str(required=True)
    qpu = ma.fields.Str(required=True)
    credentials = ma.fields.Dict(keys=ma.fields.Str(), values=ma.fields.Str(),required=True)
    shots = ma.fields.Int(required=False)
    noise_model = ma.fields.Str(required=False)
    only_measurement_errors = ma.fields.Boolean(required=False)

