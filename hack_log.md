# Qiskit Hacks

## Circuit
A circuit is a `QuantumCircuit` instance.
It has the following properties:
- `data`: an iterable of `CircuitInstruction`s (order is meaningful).
- `layout`: a`TranspileLayout` instance about bits **after transpiling**. Note: sometimes, ancillas after transpiling do not appear in the `ancillas` property.
- `qubits`: the list of the `Qubit`s.
- `clbits`: the list of the `Clbit`s.
- 

### `CircuitInstruction`
An `circuitInstruction` of a `QuantumCircuit.data` consists of `operation`, `qubits`, and `clbits` (classical bits).
- `operation`: an `Instruction` instance.
    - `name`: the name of the instruction (gate name or special instruction).
    - `num_qubits`: the number of required qubits.
    - `num_clbits`: the number of classical bits.
    - `params`: paraemeters needed for the operation.
- `qubits`: a tuple of `Qubit` instances each containing the original qubit register (`QuantumRegister` instance) and the index of the target qubit.
- `clbits`: a tuple of `Clbit` instances each containing the original classical bit register (`ClassicalRegister` instance) and the index of the target classical bit.

### `TranspileLayout`
- `initial_layout`: the qubit layout (`Layout` instance); a dict-like object <index: qubit>
- `input_qubit_mapping`: a dict-like object <qubit: index>
- `_input_qubit_count`: the number of qubits used in the circuit before transpiling
- `final_layout`: (no information yet)
- `_output_qubit_list`: the output qubit layout (they are flattened into common qubits)

