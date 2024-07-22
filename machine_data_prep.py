import pprint
import datetime 
from machine_viewer_meta import meas_return_desc
from machine_data_prcessing import timeToStr, process_qubit_data, process_gate_data, process_nudv_data, process_operations_data, process_instructions_data
from backend_design import get_backend_circuit_nodes
import json

def getMachineMetaInfo(backend):
    if backend.name == 'aer_simulator':
        return {
            "name": "Aer",
            "is_simulator": True
    }
    else:
        name = backend.properties().backend_name
        is_simulator = backend.configuration().simulator
        return {
            "name": backend.name,
            "is_simulator": is_simulator
        }

def getMachineInformation(backend):
    calltime = timeToStr(datetime.datetime.now())
    # attributes
    # name
    name = backend.name
    machine_nodes = get_backend_circuit_nodes(name)
    is_simulator = backend.configuration().simulator
    # description
    description = backend.description
    # online since...
    online_date = backend.online_date
    # backend version
    backend_version = backend.backend_version
    # Return the CouplingMap object (todo)
    coupling_map = backend.coupling_map
    # the system time resolution of input signals; required to be implemented if the backend supports Pulse scheduling
    input_time_resolution = backend.dt
    # the system time resolution of output signals
    output_time_resolution = backend.dtm
    # Return the InstructionDurations object (todo)
    instruction_durations = backend.instruction_durations
    # Return the InstructionScheduleMap for the instructions defined in this backend’s target (todo)
    instruction_schedule_map = backend.instruction_schedule_map
    # A list of Instruction tuples on the backend of the form (instruction, (qubits) (todo)
    instructions = backend.instructions
    # The maximum number of circuits (or Pulse schedules) that can be run in a single job. If there is no limit this will return None.
    max_circuits = backend.max_circuits
    # Return the grouping of measurements which are multiplexed; This is required to be implemented if the backend supports Pulse scheduling.
    meas_map = backend.meas_map
    # Return the number of qubits the backend has.
    num_qubits = backend.num_qubits
    # A list of instruction names that the backend supports.
    operation_names = backend.operation_names
    # A list of Instruction instances that the backend supports. (todo)
    operations = backend.operations
    # Return the options for the backend
    options = backend.options
    option_dict = dict(options)
    if "meas_level" in option_dict:
        option_dict["meas_level"] = int(option_dict["meas_level"])
    if "meas_return" in option_dict:
        option_dict["meas_return"] = str(option_dict["meas_return"])
        option_dict["meas_return_desc"] = meas_return_desc[option_dict["meas_return"]]
        
    # Return the Provider responsible for the backend
    provider = backend.provider
    # A qiskit.transpiler.Target object for the backend
    target = backend.target

    # methods
    # Return the pulse defaults for the backend; None if the backend does not support pulse
    pulse_defaults = backend.defaults()
    # Return the default translation stage plugin name for IBM backends
    if hasattr(backend, 'get_translation_stage_plugin'):
        translation_stage_plugin = backend.get_translation_stage_plugin()
    else:
        translation_stage_plugin = None
    # Return the backend properties, subject to optional filtering. (todo)
    # This data describes qubits properties (such as T1 and T2), gates properties (such as gate length and error), and other general properties of the backend.
    properties = backend.properties()
    property_dict_0 = properties.to_dict()
    property_dict= {
        "last_update_date": timeToStr(property_dict_0["last_update_date"]),
        "qubits": process_qubit_data(property_dict_0["qubits"]), # done
        "gates": process_gate_data(property_dict_0["gates"]), # done
        "general": process_nudv_data(property_dict_0["general"]), # done
        "general_qlists": property_dict_0["general_qlists"],
        "faulty_qubits": properties.faulty_qubits(), # terminal
        "faulty_gates": process_gate_data(properties.faulty_gates()), # need processing (same as gates)
    }

    status = backend.status()
    
    return MachineData({
        "asof": calltime, # terminal #dumped
        "name": name, # terminal #dumped
        "description": description, # terminal #dumped
        "backend_version": backend_version, #terminal #dumped
        "provider": provider, #terminal #dumped
        "is_simulator": is_simulator,

        "status": status.to_dict(), # done #dumped
        "online_date": timeToStr(online_date), # terminal #dumped
        "max_circuits": max_circuits, # terminal #dumped

        "options": option_dict, # done #dumped
        "properties": property_dict, # done

        "num_qubits": num_qubits, # terminal #dumped
        "circuit_nodes": machine_nodes,
        "coupling_map": {
            "size":  coupling_map.size(),
            "distance_matrix": coupling_map.distance_matrix.tolist(),
            "nodes": list(coupling_map.physical_qubits),
            "edges": list(coupling_map.get_edges()),
            "is_symmetric": coupling_map.is_symmetric
        }, # done
        
        "operation_names": operation_names, # terminal #dumped
        "operations": process_operations_data(operations), # done #dumped

        "instructions": process_instructions_data(instructions, instruction_durations), #done #dumped
        # "instruction_durations": instruction_durations, # with instructions
        # "instruction_schedule_map": instruction_schedule_map, # skip
        
        "pulse_defaults": {
            "qubit_freq_est": pulse_defaults.qubit_freq_est,
            "meas_freq_est": pulse_defaults.meas_freq_est
        }, #done #dumped
        "meas_map": meas_map, # terminal #dumped
        "input_time_resolution": input_time_resolution, # terminal #dumped
        "output_time_resolution": output_time_resolution, # terminal #dumped

        # "target": target, #skip
        "translation_stage_plugin": translation_stage_plugin # terminal #dumped
    })

class MachineData:
    def __init__(self, data):
        self.data = data
        
    def toJSON(self):
        return json.dumps(self.data)