import marshmallow as ma

class ExecutionResponse:
    def __init__(self, counts, meas_qubits, transpiled_circuit_depth):
        super().__init__()
        self.counts = counts
        self.meas_qubits = meas_qubits
        self.transpiled_circuit_depth = transpiled_circuit_depth

    def to_json(self):
        json_execution_response = {
            "counts": self.counts,
            "meas_qubits": self.meas_qubits,
            "transpiled_circuit_depth": self.transpiled_circuit_depth
        }
        return json_execution_response


class ExecutionResponseSchema(ma.Schema):
    counts = ma.fields.Dict(keys=ma.fields.Str(), values=ma.fields.Float())
    meas_qubits = ma.fields.List(ma.fields.Int())
    transpiled_circuit_depth = ma.fields.Int()