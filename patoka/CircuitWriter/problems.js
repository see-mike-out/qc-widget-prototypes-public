export const ProblemMap = {
  superposition: {
    name: "Superposition",
    key: "superposition",
    max_qubits: Infinity,
    params: undefined,
  },
  entanglement: {
    name: "Entanglement",
    key: "entanglement",
    max_qubits: 2,
    params: undefined
  },
  interference: {
    name: "Interference",
    key: "interference",
    max_qubits: Infinity,
    params: [{ key: "theta", name: "Theta", type: "radian" }]
  },
  QFT: {
    name: "Quantum Fourier Transform Circuit",
    key: "QFT",
    max_qubits: Infinity,
    params: undefined
  },
  BTT: {
    name: "Boolean Function Oracle",
    key: "BTT",
    max_qubits: Infinity,
    n_params: 0,
    params: undefined,
    globals: [
      { key: "random_all", name: "Randomize all", type: "boolean" },
      { key: "boolean_expression", name: "Boolean expression", type: "bool_exp" }
    ],
    variables: {
      n_symbols: (self) => unique(self.globals.boolean_expression?.match(/[a-zA-Z]/gi) || []).length,
      n_req_qubits: (self) => unique(self.globals.boolean_expression?.match(/[a-zA-Z]/gi) || []).length + 1,
      n_qubits: (self) => (self.apply_to?.length || 0)
    },
    constraints: [
      {
        key: "match_symbol_req_qubit", match: ["n_req_qubits", "n_qubits"], warning: "Should have enough number of qubits (i.e., #symbols + 1).",
        success: "The right number of qubits are selected."
      }
    ]
  },
  SHOR_period: {
    name: "Shor's Alogrithm for Finding a Period (a^r mod N)",
    key: "SHOR_period",
    max_qubits: Infinity,
    qubit_registers: [
      "counter", "oracle"
    ],
    n_params: 2,
    params: [
      { key: "factor", name: "Base factor (a)", type: "number" },
      { key: "divider", name: "Divider (N)", type: "number" }
    ],
    variables: {
      factor: (self) => self.params?.factor,
      divider: (self) => self.params?.divider,
      oracle_size: (self) => (self.params?.divider || 0)?.toString(2).length,
      n_oracle_qubits: (self) => self.qubit_registers?.oracle?.apply_to?.length || 0,
      oracle_qubits: (self) => self.qubit_registers?.oracle?.apply_to || [],
      counter_qubits: (self) => self.qubit_registers?.counter?.apply_to || []
    },
    constraints: [
      {
        key: "factor_exist", exist: ["factor"], warning: "A factor must be provided.",
        success: "A factor is provided."
      },
      {
        key: "divider_exist", exist: ["divider"], warning: "A divider must be provided.",
        success: "A divider is provided."
      },
      {
        key: "oracle_size_match", geq: ["n_oracle_qubits", "oracle_size"], warning: "The number of qubits for oracle is not sufficient for the oracle.",
        success: "The right number of oracle qubits are selected."
      },
      {
        key: "oracle_counter_separation", array_distinct: ["oracle_qubits", "counter_qubits"],
        warning: "The oracle and counter should have different qubits.",
        success: "The oracle and counter qubits are well-separated."
      }
      //  SHORS_ORACLE_SIZE = len(np.binary_repr(SHORS_MOD))
    ]
  }
};

export const ProblemTypes = Object.keys(ProblemMap).map((k) => ProblemMap[k]);

function unique(arr) {
  return Array(...(new Set(arr)));
}

export function satisfyConstraint(constraint, op, vars) {
  if (constraint.match) {
    let match_values = constraint.match.map((d) => (vars[d].constructor.name === "Function" ? vars[d](op) : vars[d]));
    return match_values.every((a) => a === match_values[0]);
  } else if (constraint.geq) {
    let match_values = constraint.geq.map((d) => (vars[d].constructor.name === "Function" ? vars[d](op) : vars[d]));
    return match_values[0] >= match_values[1];
  } else if (constraint.leq) {
    let match_values = constraint.leq.map((d) => (vars[d].constructor.name === "Function" ? vars[d](op) : vars[d]));
    return match_values[0] <= match_values[1];
  } else if (constraint.gt) {
    let match_values = constraint.qt.map((d) => (vars[d].constructor.name === "Function" ? vars[d](op) : vars[d]));
    return match_values[0] > match_values[1];
  } else if (constraint.lt) {
    let match_values = constraint.lt.map((d) => (vars[d].constructor.name === "Function" ? vars[d](op) : vars[d]));
    return match_values[0] < match_values[1];
  } else if (constraint.array_distinct) {
    let match_values = constraint.array_distinct.map((d) => (vars[d].constructor.name === "Function" ? vars[d](op) : vars[d]));
    return match_values[0].every((a) => !match_values[1].includes(a));
  } else if (constraint.exist) {
    let match_values = constraint.exist.map((d) => (vars[d].constructor.name === "Function" ? vars[d](op) : vars[d]));
    return match_values.every((a) => a != undefined);
  }
}