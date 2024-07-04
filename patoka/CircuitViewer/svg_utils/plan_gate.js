import { CX } from "./gates/cx";
import { CCX } from "./gates/ccx";
import { ISWAP } from "./gates/iswap";
import { MEASURE } from "./gates/measure";
import { RZ } from "./gates/rz";
import { SX } from "./gates/sx";
import { CUSTOM } from "./gates/custom";
import { BARRIER } from "./gates/barrier";


export const gate_data = {
  ISWAP,
  MEASURE,
  RZ,
  SX,
  CX,
  CCX,
  CUSTOM
};


export function planGateDrawing(op, layer_index) {
  let output;

  // ++++++ with 2+ control + target
  // C3XGate(*args[, _force_mutable]) The X gate controlled on 3 qubits.
  // mcx/cccx/c3x + 4 qubits (3 controls + 1 target)


  // C4XGate(*args[, _force_mutable])	The 4-qubit controlled X gate.
  // mcx/ccccx/c4x/ + 5 qubits (4 contorls + 1 target)

  // CCXGate(*args[, _force_mutable])	CCX gate, also known as Toffoli gate.
  // ccx/c2x + 3 qubits (2 controls + 1 target) 

  if (op.gate === CCX.name) {
    output = CCX.plan(op, layer_index);
  }


  else if (op.gate === ISWAP.name) {
    output = ISWAP.plan(op, layer_index);
  } else if (op.gate === MEASURE.name) {
    output = MEASURE.plan(op, layer_index);
  } else if (op.gate === RZ.name) {
    output = RZ.plan(op, layer_index);
  } else if (op.gate === SX.name) {
    output = SX.plan(op, layer_index);
  } else if (op.gate === CX.name) {
    output = CX.plan(op, layer_index);
  } else if (op.gate === BARRIER.name) {
    // some common gate?
    output = BARRIER.plan(op, layer_index);
  } else {
    // some common gate?
    output = CUSTOM.plan(op, op.gate, layer_index);
  }
  if (output) {
    output.role = "gate-group";
    output.data = { operation: op, layer_index };
  }
  return output;
}


// ++++++ with 2+ control + target
// C3XGate(*args[, _force_mutable]) The X gate controlled on 3 qubits.
// mcx/cccx/c3x + 4 qubits (3 controls + 1 target)

// C4XGate(*args[, _force_mutable])	The 4-qubit controlled X gate.
// mcx/ccccx/c4x/ + 5 qubits (4 contorls + 1 target)

// CCXGate(*args[, _force_mutable])	CCX gate, also known as Toffoli gate.
// ccx/c2x + 3 qubits (2 controls + 1 target) 




// ++++++ with 1 control + 2+ target
// CSwapGate(*args[, _force_mutable])	Controlled-SWAP gate, also known as the Fredkin gate.
// cswap + 3 qubits (1 control + 2 targets)---targets: 'X' with no boxes (swap marker)




// ++++++ with 1 control + 1 target (CX-like)
// CHGate(*args[, _force_mutable])	Controlled-Hadamard gate.
// ch + 2 qubits (1 control + 1 target)

// CSGate(*args[, _force_mutable])	Controlled-S gate.
// cs + 2 qubits (1 control + 1 target)

// CSdgGate(*args[, _force_mutable])	Controlled-S^dagger gate.
// csdg + 2 qubits (1 control + 1 target)

// CSXGate(*args[, _force_mutable])	Controlled-√X gate.
// csx + 2 qubits (1 control + 1 target)

// CXGate(*args[, _force_mutable])	Controlled-X gate.
// cx + 2 qubits (1 control + 1 target)

// CYGate(*args[, _force_mutable])	Controlled-Y gate.
// cy + 2 qubits (1 control + 1 target)

// CZGate(*args[, _force_mutable])	Controlled-Z gate.
// cz + 2 qubits (1 control + 1 target)




// +++++++ with 1 control + 1 target + parameters
// CRXGate(theta[, label, ctrl_state, ...])	Controlled-RX gate.
// crx + 2 qbuits (1 control + 1 target) + 1 param

// CRYGate(theta[, label, ctrl_state, ...])	Controlled-RY gate.
// cry + 2 qbuits (1 control + 1 target) + 1 param

// CRZGate(theta[, label, ctrl_state, ...])	Controlled-RZ gate.
// crz + 2 qbuits (1 control + 1 target) + 1 param

// CUGate(theta, phi, lam, gamma[, label, ...])	Controlled-U gate (4-parameter two-qubit gate).
// cu + 2 qubits (1 control + 1 target) + 4 params

// CU1Gate(theta[, label, ctrl_state, ...])	Controlled-U1 gate.
// cu1 + 2 qubits (1 control + 1 target) + 1 param

// CU3Gate(theta, phi, lam[, label, ...])	Controlled-U3 gate (3-parameter two-qubit gate).
// cu3 + 2 qubits (1 control + 1 target) + 3 params




// +++++++ only controls 
// CCZGate(*args[, _force_mutable])	CCZ gate.
// ccz + 3 qubits (3 controls)

// SwapGate(*args[, _force_mutable])	The SWAP gate.
// swap + 2 qubits (2 swap markers)


// +++++++ only controls + parameters
// CPhaseGate(theta[, label, ctrl_state, ...])	Controlled-Phase gate.
// cp + 2 qubits (2 controls) + 1 param (shwon in the middle)

// RZZGate(theta[, label, duration, unit])	A parametric 2-qubit 
// rzz + 2 qubits (2 controls) + 1 param (shwon in the middle)



// +++++++ multi-qubit (ISWAP-like)
// iSwapGate(*args[, _force_mutable])	iSWAP gate.
// iswap + 2 qubits

// DCXGate(*args[, _force_mutable])	Double-CNOT gate.
// dcx (2 CXs when explicated) + 2 qubits

// ECRGate(*args[, _force_mutable])	An echoed cross-resonance gate.
// ecr + 2 qbuits

// RCCXGate(*args[, _force_mutable])	The simplified Toffoli gate, also referred to as Margolus gate.
// rccx + 3 qubits

// RC3XGate(*args[, _force_mutable])	The simplified 3-controlled Toffoli gate.
// rcccx + 4 qubits




// +++++++ multi-qubit (ISWAP-like) + params
// RXXGate(theta[, label, duration, unit])	Single-qubit rotation about the X axis.
// rxx + 2 qubits + 1 param

// RYYGate(theta[, label, duration, unit])	A parametric 2-qubit 
// ryy + 2 qubits + 1 param

// RZXGate(theta[, label, duration, unit])	A parametric 2-qubit 
// rzx + 2 qubits + 1 param

// XXMinusYYGate(theta[, beta, label, ...])	XX-YY interaction gate.
// xx_minus_yy + 2 qubits + 1 param (XX-YY)

// XXPlusYYGate(theta[, beta, label, duration, ...])	XX+YY interaction gate.
// xx_plus_yy + 2 qubits + 1 param (XX+YY)



// +++++++ single-qubit with parameters (RZ-like)
// PhaseGate(theta[, label, duration, unit])	Single-qubit rotation about the Z axis.
// p + 1 qubit + 1 param

// RGate(theta, phi[, label, duration, unit])	Rotation θ around the cos(φ)x + sin(φ)y axis.
// r + 1 qubit + 1 param

// RXGate(theta[, label, duration, unit])	Single-qubit rotation about the X axis.
// rx + 1 qubit + 1 param

// RYGate(theta[, label, duration, unit])	Single-qubit rotation about the Y axis.
// ry + 1 qubit + 1 param

// RZGate(theta[, label, duration, unit])	A parametric 2-qubit 
// rz + 1 qubit + 1 param

// UGate(theta, phi, lam[, label, duration, unit])	Generic single-qubit rotation gate with 3 Euler angles.
// u + 1 qubit + 3 params

// U1Gate(theta[, label, duration, unit])	Single-qubit rotation about the Z axis.
// u1 + 1 qubit + 1 param

// U2Gate(phi, lam[, label, duration, unit])	Single-qubit rotation about the X+Z axis.
// u2 + 1 qubit + 2 params

// U3Gate(theta, phi, lam[, label, duration, unit])	Generic single-qubit rotation gate with 3 Euler angles.
// u3 + 1 qubit + 3 params

// ++++++ single-qubit (boxed)
// HGate(*args[, _force_mutable])	Single-qubit Hadamard gate.
// h + 1 qubit (H)

// IGate(*args[, _force_mutable])	Identity gate.
// id + 1 qubit (I)

// SGate(*args[, _force_mutable])	Single qubit S gate (Z**0.5).
// s + 1 qubit (S)

// SdgGate(*args[, _force_mutable])	Single qubit S-adjoint gate (~Z**0.5).
// sdg + 1 qubit (Sdg)

// SXGate(*args[, _force_mutable])	The single-qubit Sqrt(X) gate
// sx + 1 qubit

// SXdgGate(*args[, _force_mutable])	The inverse single-qubit Sqrt(X) gate.
// sxdg + 1 qubit

// TGate(*args[, _force_mutable])	Single qubit T gate (Z**0.25).
// t + 1 qubit

// TdgGate(*args[, _force_mutable])	Single qubit T-adjoint gate (~Z**0.25).
// tdg + 1qubit

// XGate(*args[, _force_mutable])	The single-qubit Pauli-X gate
// x + 1 qubit

// YGate(*args[, _force_mutable])	The single-qubit Pauli-Y gate
// y + 1 qubit

// ZGate(*args[, _force_mutable])	The single-qubit Pauli-Z gate
// z + 1 qubit
