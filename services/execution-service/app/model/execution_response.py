import marshmallow as ma
from marshmallow import fields, ValidationError


class ResultsField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, dict) or isinstance(value, list):
            return value
        else:
            raise ValidationError("Field should be str or list")


class ExecutionResponse:
    def __init__(self, counts, meas_qubits, transpiled_circuit_depth, list_input):
        super().__init__()
        self.counts = counts if list_input else counts[0]
        self.meas_qubits = meas_qubits if list_input else meas_qubits[0]
        self.transpiled_circuit_depth = (
            transpiled_circuit_depth if list_input else transpiled_circuit_depth[0]
        )

    def to_json(self):
        if isinstance(self.transpiled_circuit_depth, list):
            json_execution_response = []
            for i in range(len(self.transpiled_circuit_depth)):
                json_execution_response.append(
                    {
                        "counts": self.counts[i],
                        "meas_qubits": self.meas_qubits[i],
                        "transpiled_circuit_depth": self.transpiled_circuit_depth[i],
                    }
                )
        else:
            json_execution_response = {
                "counts": self.counts,
                "meas_qubits": self.meas_qubits,
                "transpiled_circuit_depth": self.transpiled_circuit_depth,
            }
        return json_execution_response


class ExecutionResponseSchema(ma.Schema):
    counts = ResultsField()
    meas_qubits = ma.fields.List(ma.fields.Int())
    transpiled_circuit_depth = ma.fields.Int()
