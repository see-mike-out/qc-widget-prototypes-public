import json 
from backend_design import get_backend_circuit_nodes
import re

aer_sim_name_re = re.compile("aer_simulator_from\\(fake_([a-zA-Z]+)\\)")

def getBackendData(backend):
    # meta data
    props = backend.properties().to_dict()
    backend_name = props["backend_name"]
    if backend_name == "" and hasattr(backend, "name"):
        backend_name = backend.name
        name_parsed = aer_sim_name_re.match(backend_name)
        if name_parsed is not None:
            backend_name = backend_name.replace("aer_simulator_from(fake_", "")
            backend_name = "ibm_" + backend_name[0:-1]
    backend_version = props["backend_version"] if "backend_version" in props else ""
    last_update_date = timeToStr(props["last_update_date"]) if "last_update_date" in props else ""
    machine_data = backend.configuration().to_dict()
    machine_data["online_date"] = timeToStr(machine_data["online_date"])  if "online_date" in props else ""

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


def timeToStr(dt):
    return dt.strftime("%m/%d/%Y, %H:%M:%S") if dt is not None else ""
    