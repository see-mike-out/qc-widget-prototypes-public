from qiskit_draw_utils import getCircuitLayout
from match_circuit import matchCircuitLayouts
from backend_prep import getBackendData
from qiskit.circuit import CircuitInstruction
import json

def prepareData(circuit, pass_manager, backend):
    # deal with backend
    backend_data = getBackendData(backend)
    min_match_score = float('inf')
    # deal with transpiling
    for i in range(10):
        trans = pass_manager.run(circuit)
        layer_original = getCircuitLayout(circuit)
        layer_trans = getCircuitLayout(trans)
        circuit_matches = matchCircuitLayouts(layer_original, layer_trans, pass_manager)
        match_results = [m["to"]["complete"] for m in circuit_matches["layer_match"]]
        match_scores = sum([m["to"]["un_matches"] for m in circuit_matches["layer_match"]])
        if all(match_results):
            return_data = PassData({
                "original_circuit": circuit,
                "original_circuit_layered": layer_original,
                "transpiled_circuit": trans,
                "transpiled_circuit_layered": layer_trans,
                "traspiling_match": circuit_matches,
                "backend_data": backend_data
            })
            break
        elif match_scores < min_match_score:
            min_match_score = match_scores
            return_data = PassData({
                "original_circuit": circuit,
                "original_circuit_layered": layer_original,
                "transpiled_circuit": trans,
                "transpiled_circuit_layered": layer_trans,
                "traspiling_match": circuit_matches,
                "backend_data": backend_data
            })
    return return_data

def bitsToList(bits):
    return [
        {
            "index": bit._index,
            "register": { "name": bit._register._name, "size": bit._register._size }
        }
        for bit in bits
    ]

class PassData:
    def __init__(self, data):
        self.original_circuit = data["original_circuit"]
        self.original_circuit_layered = data["original_circuit_layered"]
        self.transpiled_circuit = data["transpiled_circuit"]
        self.transpiled_circuit_layered = data["transpiled_circuit_layered"]
        self.traspiling_match = data["traspiling_match"]
        self.backend_data = data["backend_data"]
        self.original_global_phase = get_global_pahse(data["original_circuit"][2])
        self.transpiled_global_phase = get_global_pahse(data["transpiled_circuit"][2])

    def toJSON(self):
        return json.dumps({
            "original": {
                "layers": self.original_circuit_layered[0],
                "qubits": bitsToList(self.original_circuit.qubits),
                "clbits": bitsToList(self.original_circuit.clbits),
                "num_qubits": self.original_circuit.num_qubits,
                "num_clbits": self.original_circuit.num_clbits,
                "global_phase": self.original_global_phase
            },
            "transpiled": {
                "layers": self.transpiled_circuit_layered[0],
                "qubits": bitsToList(self.transpiled_circuit.qubits),
                "clbits": bitsToList(self.transpiled_circuit.clbits),
                "num_qubits": self.transpiled_circuit.num_qubits,
                "num_clbits": self.transpiled_circuit.num_clbits,
                "global_phase": self.transpiled_global_phase
            },
            "match": self.traspiling_match,
            "backend": self.backend_data
        })
        
def get_global_pahse(phase):
    if isinstance(phase, int) or isinstance(phase, float):
        return phase
    elif isinstance(phase, CircuitInstruction):
        if phase.operation.name == "measure":
            return 0
        elif phase.operation.name == "rz":
            return phase.operation.params[0]
    else:
        return 0