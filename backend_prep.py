import json 

def getBackendData(backend):
    # meta data
    props = backend.properties().to_dict()
    backend_name = props["backend_name"]
    backend_version = props["backend_version"]
    last_update_date = timeToStr(props["last_update_date"])
    machine_data = backend.configuration().to_dict()
    machine_data["online_date"] = timeToStr(machine_data["online_date"])

    # design
    edges = backend.configuration().to_dict()["coupling_map"]
    nodes = get_backend_circuit_nodes(backend_name)

    # qubit errors
    readout_errors = {}
    for qi in range(len(props["qubits"])):
        qubit = props["qubits"][qi]
        for item in qubit:
            if item["name"] == "readout_error":
                readout_errors[qi] = {
                    "value": item["value"],
                    "asof": timeToStr(item["date"])
                }

    gate_info = []
    for qubit_gate in props["gates"]:
        qubits = qubit_gate["qubits"]
        gate = qubit_gate["gate"]
        gate_error = {}
        gate_length = {}
        for param in qubit_gate["parameters"]:
            if param["name"] == "gate_error":
                gate_error["value"] = param["value"]
                gate_error["asof"] = timeToStr(param["date"])
            elif param["name"] == "gate_length":
                gate_length["value"] = param["value"]
                gate_length["unit"] = param["unit"]
                gate_length["asof"] = timeToStr(param["date"])
        gate_info.append({
            "qubits": qubits,
            "gate": gate,
            "gate_error": gate_error,
            "gate_length": gate_length
        })
        
    return {
        "name": backend_name,
        "version": backend_version,
        "last_update_date": last_update_date,
        "machine_data": machine_data,
        "design": {
            "nodes": nodes,
            "edges": edges
        },
        "readout_errors": readout_errors,
        "gate_info": gate_info
    }


def get_backend_circuit_nodes(name):
    if name == "ibmq_vigo":
        return NODES_IMBQ_VIGO


NODES_IMBQ_VIGO = [
    {"index": 0, "x": 0, "y": 0},
    {"index": 1, "x": 1, "y": 0},
    {"index": 2, "x": 2, "y": 0},
    {"index": 3, "x": 1, "y": 1},
    {"index": 4, "x": 1, "y": 2}
]

def timeToStr(dt):
    return dt.strftime("%m/%d/%Y, %H:%M:%S")
    