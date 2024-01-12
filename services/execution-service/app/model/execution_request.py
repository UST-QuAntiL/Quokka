import marshmallow as ma
from marshmallow import fields, ValidationError


class CircuitField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, list):
            return value
        else:
            raise ValidationError("Field should be str or list")


class ExecutionRequest:
    def __init__(
        self,
        circuit,
        provider,
        qpu,
        credentials,
        shots=1000,
        noise_model=None,
        only_measurement_errors=False,
        circuit_format="openqasm2",
        parameters=None
    ):
        self.circuit = circuit
        self.provider = provider.lower()
        self.qpu = qpu
        self.credentials = credentials
        self.shots = shots
        self.noise_model = noise_model
        self.only_measurement_errors = only_measurement_errors
        self.circuit_format = circuit_format.lower()
        self.parameters = parameters


class ExecutionRequestSchema(ma.Schema):
    circuit = CircuitField(required=True)
    provider = ma.fields.Str(required=True)
    qpu = ma.fields.Str(required=True)
    credentials = ma.fields.Dict(
        keys=ma.fields.Str(), values=ma.fields.Str(), required=True
    )
    shots = ma.fields.Int(required=False)
    noise_model = ma.fields.Str(required=False)
    only_measurement_errors = ma.fields.Boolean(required=False)
    circuit_format = ma.fields.Str(required=False)
    parameters = ma.fields.List(ma.fields.Float(), required=False)
