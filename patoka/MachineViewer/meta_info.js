export const sections = [
  {
    "title": "Meta data",
    "subsections": ["asof", "name", "description", "backend_version", "provider", "is_simulator"]
  },
  {
    "title": "Availability",
    "subsections": [
      {
        "key": "status",
        "order": [
          "operational",
          "pending_jobs",
          "status_msg"
        ]
      },
      "online_date",
      "max_circuits"
    ]
  },
  {
    "title": "Settings",
    "subsections": [
      {
        "key": "options",
        "order": [
          "shots",
          "memory", "memory_slots", "memory_slot_size",
          "meas_level", "meas_return",
          "rep_time", "rep_delay",
          "init_qubits",
          "use_measure_esp",
          "noise_model",
          "seed_simulator"
        ]
      },
      {
        "key": "properties",
        "order": [
          "last_update_date",
          "general_qlists",
          "general",
          "gates",
          "qubits",
          "faulty_gates",
          "faulty_qubits",
        ]
      }
    ]
  },
  {
    "title": "Qubits",
    "subsections": [
      "num_qubits",
      {
        "key": "coupling_map",
        "order": [
          // "size",
          // "nodes",
          // "edges",
          "circuit_view",
          "distance_matrix",
          "is_symmetric"
        ]
      }
    ]
  },
  {
    "title": "Operations",
    "subsections": ["operation_names", "operations"]
  },
  {
    "title": "Instructions",
    "subsections": ["instructions"]
  },
  {
    "title": "Pulse-related",
    "subsections": [
      {
        "key": "pulse_defaults",
        "order": [
          "qubit_freq_est",
          "meas_freq_est",
        ]
      },
      "meas_map",
      "input_time_resolution",
      "output_time_resolution"
    ]
  },
  {
    "title": "Compiler-related",
    "subsections": ["translation_stage_plugin"]
    // "target",
  },
]

export const titles = {
  // Meta data
  "asof": "Data collected",
  "name": "Name",
  "description": "Description",
  "backend_version": "Version",
  "provider": "Provider",
  "is_simulator": "Is simulator?",

  // Availability
  "status": "Status",
  "operational": "Is operational?",
  "pending_jobs": "Pending jobs",
  "status_msg": "Status",
  "online_date": "Online date",
  "max_circuits": "Maximum circuits",

  // Setups
  "options": "Options",
  "shots": "Default shots per run",
  "memory": "Memory support",
  "memory_slots": "Memory slots",
  "memory_slot_size": "Memory slot size",
  "meas_level": "Supported measurement levels",
  "meas_return": "Level of measurement data for the backend to return",
  "rep_time": "Supported repetition times (program execution time, unit: μs)",
  "rep_delay": "Delay between primitives (unit: sec)",
  "init_qubits": "Reset the qubits to the ground state for each shot",
  "use_measure_esp": "Use excited state promoted (ESP) readout for measurements",
  "noise_model": "Noise model",
  "seed_simulator": "Random seed to control sampling (Simulators only)",

  "properties": "Properties",
  "last_update_date": "Last update date",
  "general": "General system parameters",
  "gates": "Supported gates",
  "qubits": "Qubit data",
  "general_qlists": "General qubit list",
  "faulty_qubits": "Faulty qubits",
  "faulty_gates": "Faulty gates",

  // Qubits
  "coupling_map": "Coupling map",
  "size": "Size",
  "distance_matrix": "Distance matrix",
  "nodes": "Nodes",
  "edges": "Edges",
  "is_symmetric": "Is symmetric?",
  "num_qubits": "Number of qubits",
  "circuit_view": "Circuit",

  // Operations
  "operation_names": "Operation names",
  "operations": "Operations",

  // Instructions
  "instructions": "Instructions",
  "instruction_durations": "Instruciton durationas",
  "instruction_schedule_map": "Instruction schedule map",

  // Pulse-related inforamation
  "pulse_defaults": "Pulse defaults",
  "qubit_freq_est": "Qubit frequencies in Hertz",
  "meas_freq_est": "Measurement frequencies in Hertz",
  "meas_map": "Measurement groupings",
  "input_time_resolution": "Input time resolution",
  "output_time_resolution": "Output time resolutin",

  // Compiler-related information
  "target": "Target",
  "translation_stage_plugin": "Translation stage plugin(s)",
}

export const descriptions = {
  // Meta data
  "asof": "The time when the attributes were collected.",
  "name": "The name of the backend machine.",
  "description": "The overview information about the backend machine.",
  "backend_version": "The version of the backend machine.",
  "provider": "The provider of the backend.",

  // Availability
  "status": "The status of the backend machine",
  "online_date": "This machine has been online since ... (after being offline).",
  "max_circuits": "The maximum number of circuits can be run in a single job.",

  // Setups
  "options": "Options for the backend machine",
  "rep_delay": "This parameter is applicable only if `dynamic=False` is specified or defaulted to.",
  "use_measure_esp": "ESP readout can offer higher fidelity than standard measurement sequences. Backend support for ESP readout is determined by the `flag measure_esp_enabled` in `backend.configuration()`. This parameter is applicable only if `dynamic=False` is specified or defaulted to.",
  "properties": "The properties of the backend machine",
  "qubits": "Anh(armonicity), Freq(uency), M0P1 (= prob_meas0_prep1), M1P0 (= prob_meas1_prep0), RE (=readout error), RL (= readout lenght)",

  // Qubits
  "coupling_map": "The qubit couplings.",
  "num_qubits": "The number of qubits supported",

  // Operations
  "operation_names": "Operation names supported by the machine",
  "operations": "Operations supported by the machine",

  // Instructions
  "instructions": "Instructions supported for each qubit.",

  // Pulse-related inforamation
  "pulse_defaults": "the pulse defaults for the backend. If `None`, the machine is not available for Pulse scheduling.",
  "meas_map": "The grouping of measurements which are multiplexed. If `None`, the machine is not available for Pulse scheduling.",
  "input_time_resolution": "The system time resolution of input signals. If `None`, the machine is not available for Pulse scheduling.",
  "output_time_resolution": "The system time resolution of output signals. If `None`, the machine is not available for Pulse scheduling.",

  // Compiler-related information
  "target": "A description of instructions on a backend and their properties as well as some timing information.",
  "translation_stage_plugin": "The default translation stage plugin name for IBM backends. If `None`, it is not provided.",
}

export const meas_return_desc = {
  "MeasReturnType.SINGLE": "Returns information from every shot",
  "MeasReturnType.AVERAGE": "Returns average measurement output (= averaged over number of shots)"
}


export const markers = {
  // Meta data
  "name": "backend.name",
  "description": "backend.description",
  "backend_version": "backend.backend_version",
  "provider": "backend.provider",
  "is_simulator": "backend.properties().simulator",

  // Availability
  "status": "backend.status",
  "operational": "backend.status.operational",
  "pending_jobs": "backend.status.pending_jobs",
  "status_msg": "backend.status.status_msg",
  "online_date": "backend.online_date",
  "max_circuits": "backend.max_circuits",

  // Setups
  "options": "backend.options",
  "shots": "backend.options.shots",
  "memory": "backend.options.memory",
  "memory_slots": "backend.options.memory_slots",
  "memory_slot_size": "backend.options.memory_slot_size",
  "meas_level": "backend.options.meas_level",
  "meas_return": "backend.options.meas_return",
  "rep_time": "backend.options.rep_time",
  "rep_delay": "backend.options.rep_delay",
  "init_qubits": "backend.options.init_qubits",
  "use_measure_esp": "backend.options.use_measure_esp",
  "noise_model": "backend.options.noise_model",
  "seed_simulator": "backend.options.seed_simulator",

  "properties": "backend.properties()",
  "last_update_date": "backend.properties().last_update_date",
  "general": "backend.properties().general",
  "gates": "backend.properties().gates",
  "qubits": "backend.properties().qubits",
  "general_qlists": "backend.properties().general_qlists",
  "faulty_qubits": "back1.properties().faulty_qubits()",
  "faulty_gates": "back1.properties().faulty_gates()",

  // Qubits
  "coupling_map": "backend.coupling_map",
  "size": "backend.coupling_map.coupling_map.size()",
  "distance_matrix": "backend.coupling_map.distance_matrix",
  "is_symmetric": "backend.coupling_map.is_symmetric",
  "num_qubits": "backend.num_qubits",

  // Operations
  "operation_names": "backend.operation_names",
  "operations": "backend.operations",

  // Instructions
  "instructions": "backend.instructions",
  "instruction_durations": "Instruciton durationas",
  "instruction_schedule_map": "Instruction schedule map",

  // Pulse-related inforamation
  "pulse_defaults": "backend.defaults()",
  "qubit_freq_est": "backend.defaults().qubit_freq_est",
  "meas_freq_est": "backend.defaults().meas_freq_est",
  "meas_map": "backend.meas_map",
  "input_time_resolution": "backend.dt",
  "output_time_resolution": "backend.dtm",

  // Compiler-related information
  "translation_stage_plugin": "translation_stage_plugin = backend.get_translation_stage_plugin() if hasattr(backend, 'get_translation_stage_plugin') else None",
}