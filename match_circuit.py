import pprint
import math
import qiskit.circuit.library as gates
from qiskit_draw_utils import getCircuitLayout
import copy

# gate explications
def get_gate_components(gate_name, n_qubits, params, pass_manager):
    gate = None
    # C3XGate(*args[, _force_mutable])	The X gate controlled on 3 qubits.
    if gate_name == "cccx" or gate_name == "c3x" or (gate_name == "mcx" and n_qubits == 4):
        gate = gates.C3XGate()
    # C4XGate(*args[, _force_mutable])	The 4-qubit controlled X gate.
    elif gate_name == "ccccx" or gate_name == "c4x" or (gate_name == "mcx" and n_qubits == 5):
        gate = gates.C4XGate()
    # CCXGate(*args[, _force_mutable])	CCX gate, also known as Toffoli gate.
    elif gate_name == "ccx" or gate_name == "c2x":
        gate = gates.CCXGate()
    # DCXGate(*args[, _force_mutable])	Double-CNOT gate.
    elif gate_name == "dcx":
        gate = gates.DCXGate()
    # CHGate(*args[, _force_mutable])	Controlled-Hadamard gate.
    elif gate_name == "ch": 
        gate = gates.CHGate()
    # CPhaseGate(theta[, label, ctrl_state, ...])	Controlled-Phase gate.
    elif gate_name == "cp": 
        gate = gates.CPhaseGate(*params)
    # CRXGate(theta[, label, ctrl_state, ...])	Controlled-RX gate.
    elif gate_name == "crx": 
        gate = gates.CRXGate(*params)
    # CRYGate(theta[, label, ctrl_state, ...])	Controlled-RY gate.
    elif gate_name == "cry": 
        gate = gates.CRXGate(*params)
    # CRZGate(theta[, label, ctrl_state, ...])	Controlled-RZ gate.
    elif gate_name == "crz": 
        gate = gates.CRZGate(*params)
    # CSGate(*args[, _force_mutable])	Controlled-S gate.
    elif gate_name == "cs": 
        gate = gates.CSGate()
    # CSdgGate(*args[, _force_mutable])	Controlled-S^dagger gate.
    elif gate_name == "csdg": 
        gate = gates.CSdgGate()
    # CSwapGate(*args[, _force_mutable])	Controlled-SWAP gate, also known as the Fredkin gate.
    elif gate_name == "cswap": 
        gate = gates.CSwapGate()
    # CSXGate(*args[, _force_mutable])	Controlled-√X gate.
    elif gate_name == "csx": 
        gate = gates.CSXGate()
    # CUGate(theta, phi, lam, gamma[, label, ...])	Controlled-U gate (4-parameter two-qubit gate).
    elif gate_name == "cu": 
        gate = gates.CUGate(*params)
    # CU1Gate(theta[, label, ctrl_state, ...])	Controlled-U1 gate.
    elif gate_name == "cu1": 
        gate = gates.CU1Gate(*params)
    # CU3Gate(theta, phi, lam[, label, ...])	Controlled-U3 gate (3-parameter two-qubit gate).
    elif gate_name == "cu3": 
        gate = gates.CU1Gate(*params)
    # CXGate(*args[, _force_mutable])	Controlled-X gate.
    elif gate_name == "cx": 
        gate = gates.CXGate()
    # CYGate(*args[, _force_mutable])	Controlled-Y gate.
    elif gate_name == "cy": 
        gate = gates.CYGate()
    # CZGate(*args[, _force_mutable])	Controlled-Z gate.
    elif gate_name == "cz": 
        gate = gates.CZGate()
    # CCZGate(*args[, _force_mutable])	CCZ gate.
    elif gate_name == "ccz": 
        gate = gates.CCZGate()
    # ECRGate(*args[, _force_mutable])	An echoed cross-resonance gate.
    elif gate_name == "ecr": 
        gate = gates.ECRGate()
    # HGate(*args[, _force_mutable])	Single-qubit Hadamard gate.
    elif gate_name == "h": 
        gate = gates.HGate()
    # IGate(*args[, _force_mutable])	Identity gate.
    elif gate_name == "id": 
        gate = gates.IGate()
    # PhaseGate(theta[, label, duration, unit])	Single-qubit rotation about the Z axis.
    elif gate_name == "p": 
        gate = gates.PhaseGate(*params)
    # RCCXGate(*args[, _force_mutable])	The simplified Toffoli gate, also referred to as Margolus gate.
    elif gate_name == "rccx": 
        gate = gates.RCCXGate()
    # RC3XGate(*args[, _force_mutable])	The simplified 3-controlled Toffoli gate.
    elif gate_name == "rcccx": 
        gate = gates.RCCXGate()
    # RGate(theta, phi[, label, duration, unit])	Rotation θ around the cos(φ)x + sin(φ)y axis.
    elif gate_name == "r": 
        gate = gates.RGate(*params)
    # RXGate(theta[, label, duration, unit])	Single-qubit rotation about the X axis.
    elif gate_name == "rx": 
        gate = gates.RXGate(*params)
    # RXXGate(theta[, label, duration, unit])	Single-qubit rotation about the X axis.
    elif gate_name == "rxx": 
        gate = gates.RXXGate(*params)
    # RYGate(theta[, label, duration, unit])	Single-qubit rotation about the Y axis.
    elif gate_name == "ry": 
        gate = gates.RYGate(*params)
    # RYYGate(theta[, label, duration, unit])	A parametric 2-qubit 
    elif gate_name == "ryy": 
        gate = gates.RYYGate(*params)
    # RZGate(theta[, label, duration, unit])	A parametric 2-qubit 
    elif gate_name == "rz": 
        gate = gates.RZGate(*params)
    # RZZGate(theta[, label, duration, unit])	A parametric 2-qubit 
    elif gate_name == "rzz": 
        gate = gates.RZZGate(*params)
    # RZXGate(theta[, label, duration, unit])	A parametric 2-qubit 
    elif gate_name == "rzx": 
        gate = gates.RZZGate(*params)
    # XXMinusYYGate(theta[, beta, label, ...])	XX-YY interaction gate.
    elif gate_name == "xx_minus_yy": 
        gate = gates.XXMinusYYGate(*params)
    # XXPlusYYGate(theta[, beta, label, duration, ...])	XX+YY interaction gate.
    elif gate_name == "xx_plus_yy": 
        gate = gates.XXMinusYYGate(*params)
    # SGate(*args[, _force_mutable])	Single qubit S gate (Z**0.5).
    elif gate_name == "s": 
        gate = gates.SGate()
    # SdgGate(*args[, _force_mutable])	Single qubit S-adjoint gate (~Z**0.5).
    elif gate_name == "sdg": 
        gate = gates.SdgGate()
    # SwapGate(*args[, _force_mutable])	The SWAP gate.
    elif gate_name == "swap": 
        gate = gates.SwapGate()
    # iSwapGate(*args[, _force_mutable])	iSWAP gate.
    elif gate_name == "iswap": 
        gate = gates.iSwapGate()
    # SXGate(*args[, _force_mutable])	The single-qubit Sqrt(X) gate
    elif gate_name == "sx": 
        gate = gates.SXGate()
    # SXdgGate(*args[, _force_mutable])	The inverse single-qubit Sqrt(X) gate.
    elif gate_name == "sxdg": 
        gate = gates.SXdgGate()
    # TGate(*args[, _force_mutable])	Single qubit T gate (Z**0.25).
    elif gate_name == "t": 
        gate = gates.TGate()
    # TdgGate(*args[, _force_mutable])	Single qubit T-adjoint gate (~Z**0.25).
    elif gate_name == "tdg": 
        gate = gates.TdgGate()
    # UGate(theta, phi, lam[, label, duration, unit])	Generic single-qubit rotation gate with 3 Euler angles.
    elif gate_name == "u": 
        gate = gates.UGate(*params)
    # U1Gate(theta[, label, duration, unit])	Single-qubit rotation about the Z axis.
    elif gate_name == "u1": 
        gate = gates.U1Gate(*params)
    # U2Gate(phi, lam[, label, duration, unit])	Single-qubit rotation about the X+Z axis.
    elif gate_name == "u2": 
        gate = gates.U2Gate(*params)
    # U3Gate(theta, phi, lam[, label, duration, unit])	Generic single-qubit rotation gate with 3 Euler angles.
    elif gate_name == "u3": 
        gate = gates.U3Gate(*params)
    # XGate(*args[, _force_mutable])	The single-qubit Pauli-X gate
    elif gate_name == "x": 
        gate = gates.XGate()
    # YGate(*args[, _force_mutable])	The single-qubit Pauli-Y gate
    elif gate_name == "y": 
        gate = gates.YGate()
    # ZGate(*args[, _force_mutable])	The single-qubit Pauli-Z gate
    elif gate_name == "z": 
        gate = gates.ZGate()
    # GlobalPhaseGate(phase[, label, duration, unit])	The global phase gate 
    elif gate_name == "global_phase": 
        gate = gates.GlobalPhaseGate()
    elif gate_name == "QFT":
        gate = gates.QFT(n_qubits).to_gate()
    if gate is not None:
        gate_transpiled = pass_manager.run(gate.definition)
        return gate_transpiled
    return None

def explicate_circuit(ogate, pass_manager):
    gate_name = ogate["gate"]
    clbits = ogate["clbits"]
    qubits = ogate["qubits"]
    num_clbits = ogate["num_clbits"]
    num_qubits = ogate["num_qubits"]
    qubit_map = makeBitMap(qubits)
    clbit_map = makeBitMap(clbits)
    params = ogate["params"]
    gate_comps = get_gate_components(gate_name, num_qubits, params, pass_manager)
    explication = []
    if gate_comps is not None:
        gate_layout = getCircuitLayout(gate_comps)

        # map converted qubit/clbit indices
        gate_qubit_indices = list()
        gate_clbit_indices = list()
        
        for layer in gate_layout[0]:
            for op in layer["operations"]:
                for qubit in op["qubits"]:
                    if qubit["index"] not in gate_qubit_indices:
                        gate_qubit_indices.append(qubit["index"])
                for clbit in op["clbits"]:
                    if clbit["index"] not in gate_clbit_indices:
                        gate_clbit_indices.append(clbit["index"])

        cnt = 0
        for layer in gate_layout[0]:
            layer_explication = []
            for op in layer["operations"]:
                new_op = {
                    "gate": op["gate"],
                    "params": op["params"],
                    "qubits": matchBitsFromTo(qubit_map, 
                                              gate_qubit_indices, 
                                              op["qubits"]),
                    "clbits": matchBitsFromTo(clbit_map, 
                                              gate_clbit_indices,
                                              op["clbits"]),
                    "num_qubits": op["num_qubits"],
                    "num_clbits": op["num_clbits"],
                    "transpiled": True
                }

                layer_explication.append(new_op)
            cnt += 1
            explication.append(layer_explication)
    else:
        explication.append([{
            "gate": gate_name,
            "params": params,
            "num_qubits": num_qubits,
            "num_clbits": num_clbits,
            "qubits": qubits,
            "clbits": clbits,
            "transpiled": False
        }])
    return explication

def makeBitMap(bits):
    bit_list = [] # ordered
    for bit in bits:
        bit_list.append(bit["index"])
    return tuple(bit_list)

def rearrangeBits(operations):
    qubit_range = set()
    clbit_range = set()
    for op in operations:
        for qubit in op["qubits"]:
            qubit_range.add(qubit["index"])
        for clbit in op["clbits"]:
            clbit_range.add(clbit["index"])
    qubit_range = list(qubit_range)
    qubit_range.sort()
    clbit_range = list(clbit_range)
    clbit_range.sort()
    recon_qubit_map = {}
    recon_clbit_map = {}
    for i in range(len(qubit_range)):
        recon_qubit_map[qubit_range[i]] = i
    for i in range(len(clbit_range)):
        recon_clbit_map[clbit_range[i]] = i
    
    for op in operations:
        for qubit in op["qubits"]:
            qubit["index"] = recon_qubit_map[qubit["index"]]
        for qubit in op["clbits"]:
            clbit["index"] = recon_clbit_map[clbit["index"]]

    return operations

def matchBitsFromTo(f_bit_list, used_bits, t):
    bits = []
    for i in range(len(t)):
        t_bit = copy.deepcopy(t[i])
        t_bit["index"] = f_bit_list[used_bits.index(t_bit["index"])]
        bits.append(t_bit)
    return tuple(bits)



# circuit match
# todo: fix seed

def matchCircuitLayouts(origin, trans, pass_manager):
    # todo: need to come up with some dynamic programming method
    origin_explicated = []
    mapping = trans[1]
    # match original layer and transpiled layer
    memo = []
    for oli in range(len(origin[0])):
        o_layer = origin[0][oli]
        o_layer_ops = o_layer["operations"]
        for opi in range(len(o_layer_ops)):
            o_op = o_layer_ops[opi]
            op_explicated = explicate_circuit(o_op, pass_manager)
            for i in range(10):
                traversed = traverseForMatching(o_op, op_explicated, trans[0], mapping, start=oli)
                if traversed["complete"]:
                    break
            # print(">>>")
            # print(traversed)
            # print("---")
            memo.append({"from": (oli, opi), "to": traversed})
    return {
        "layer_match": memo,
        "bit_match": mapping
    }

def traverseForMatching(origin, origin_exp, trans, mapping, start=0):
    o_count = 0
    bitMap = makeBitMapFromMapping(mapping)
    t_point = 0
    memo = []
    for ei in range(len(origin_exp)):
        e_layer = copy.deepcopy(origin_exp[ei])
        
        for eop in e_layer:
            eop["qubits"] = matchBitsWithMapping(bitMap, eop["qubits"])
            o_count += 1
        for ti in range(t_point, len(trans)):
            t_layer = trans[ti]["operations"]
            parts = isPartOf(e_layer, t_layer, mapping)
            if parts is not False:
                t_point = ti
                for part in parts:
                    memo.append((ti, part))
                break
                
    return {
        "matches": memo,
        "complete": len(memo) == o_count,
        "un_matches":  o_count - len(memo)
    }

def makeBitMapFromMapping(mapping):
    bitMap = {}
    for item in mapping:
        bitMap[item["from"]] = { "new": item["to"] }
    return bitMap
    
def matchBitsWithMapping(bitMap, t):
    bits = []
    for i in range(len(t)):
        t_bit = copy.deepcopy(t[i])
        t_bit["index"] = bitMap[t_bit["index"]]["new"]
        bits.append(t_bit)
    return tuple(bits)

def isPartOf(el, tl, mapping):
    if len(el) > len(tl):
        return False
    else:
        memo = []
        el_simple = instSimplifier(el)
        tl_simple = instSimplifier(tl)
        for i in range(0, len(el_simple)):
            els = el_simple[i]
            if els not in tl_simple:
                return False
            else:
                memo.append(tl_simple.index(els))
        return memo

def instSimplifier(opList):
    l = []
    for op in opList:
        txt = op["gate"] + "_"  + "|".join([str(p) for p in op["params"]]) + "_"  + "|".join(str(b["index"]) for b in op["qubits"]) 
        l.append(txt)
    return l

def get_radian_names(value):
    ratio = value / math.pi
    if ratio == 0:
        return "0"
    elif ratio == 1/4:
        return "π/4"
    elif ratio == 1/3:
        return "π/3"
    elif ratio == 1/2:
        return "π/2"
    elif ratio == 2/3:
        return "2π/3"
    elif ratio == 3/4:
        return "3π/4"
    elif ratio == 1:
        return "π"
    elif ratio == -1/4:
        return "-π/4"
    elif ratio == -1/3:
        return "-π/3"
    elif ratio == -1/2:
        return "-π/2"
    elif ratio == -2/3:
        return "-2π/3"
    elif ratio == -3/4:
        return "-3π/4"
    elif ratio == -1:
        return "-π"


# data sample
# ([{'num_op': 2,
#    'operations': [{'clbits': (),
#                    'gate': 'iswap',
#                    'num_clbits': 0,
#                    'num_qubits': 2,
#                    'params': [],
#                    'qubits': ({'index': 0,
#                                'register': {'name': 'q', 'size': 4}},
#                               {'index': 2,
#                                'register': {'name': 'q', 'size': 4}})},
#                   {'clbits': ({'index': 3,
#                                'register': {'name': 'q', 'size': 4}},),
#                    'gate': 'measure',
#                    'num_clbits': 1,
#                    'num_qubits': 1,
#                    'params': [],
#                    'qubits': ({'index': 3,
#                                'register': {'name': 'q', 'size': 4}},)}]},
#   {'num_op': 1,
#    'operations': [{'clbits': ({'index': 1,
#                                'register': {'name': 'q', 'size': 4}},),
#                    'gate': 'measure',
#                    'num_clbits': 1,
#                    'num_qubits': 1,
#                    'params': [],
#                    'qubits': ({'index': 1,
#                                'register': {'name': 'q', 'size': 4}},)}]},
#   {'num_op': 1,
#    'operations': [{'clbits': ({'index': 0,
#                                'register': {'name': 'q', 'size': 4}},),
#                    'gate': 'measure',
#                    'num_clbits': 1,
#                    'num_qubits': 1,
#                    'params': [],
#                    'qubits': ({'index': 0,
#                                'register': {'name': 'q', 'size': 4}},)}]},
#   {'num_op': 1,
#    'operations': [{'clbits': ({'index': 2,
#                                'register': {'name': 'q', 'size': 4}},),
#                    'gate': 'measure',
#                    'num_clbits': 1,
#                    'num_qubits': 1,
#                    'params': [],
#                    'qubits': ({'index': 2,
#                                'register': {'name': 'q', 'size': 4}},)}]}],
#  [])
# ([{'num_op': 3,
#    'operations': [{'clbits': (),
#                    'gate': 'rz',
#                    'num_clbits': 0,
#                    'num_qubits': 1,
#                    'params': [-3.141592653589793],
#                    'qubits': ({'index': 1,
#                                'register': {'name': 'q', 'size': 5}},)},
#                   {'clbits': (),
#                    'gate': 'rz',
#                    'num_clbits': 0,
#                    'num_qubits': 1,
#                    'params': [1.5707963267948966],
#                    'qubits': ({'index': 2,
#                                'register': {'name': 'q', 'size': 5}},)},
#                   {'clbits': ({'index': 3,
#                                'register': {'name': 'q', 'size': 5}},),
#                    'gate': 'measure',
#                    'num_clbits': 1,
#                    'num_qubits': 1,
#                    'params': [],
#                    'qubits': ({'index': 3,
#                                'register': {'name': 'q', 'size': 5}},)}]},
#   {'num_op': 2,
#    'operations': [{'clbits': ({'index': 4,
#                                'register': {'name': 'q', 'size': 5}},),
#                    'gate': 'measure',
#                    'num_clbits': 1,
#                    'num_qubits': 1,
#                    'params': [],
#                    'qubits': ({'index': 4,
#                                'register': {'name': 'q', 'size': 5}},)},
#                   {'clbits': (),
#                    'gate': 'sx',
#                    'num_clbits': 0,
#                    'num_qubits': 1,
#                    'params': [],
#                    'qubits': ({'index': 1,
#                                'register': {'name': 'q', 'size': 5}},)}]},
#   {'num_op': 1,
#    'operations': [{'clbits': (),
#                    'gate': 'rz',
#                    'num_clbits': 0,
#                    'num_qubits': 1,
#                    'params': [1.5707963267948966],
#                    'qubits': ({'index': 1,
#                                'register': {'name': 'q', 'size': 5}},)}]},
#   {'num_op': 1,
#    'operations': [{'clbits': (),
#                    'gate': 'cx',
#                    'num_clbits': 0,
#                    'num_qubits': 2,
#                    'params': [],
#                    'qubits': ({'index': 1,
#                                'register': {'name': 'q', 'size': 5}},
#                               {'index': 2,
#                                'register': {'name': 'q', 'size': 5}})}]},
#   {'num_op': 1,
#    'operations': [{'clbits': (),
#                    'gate': 'cx',
#                    'num_clbits': 0,
#                    'num_qubits': 2,
#                    'params': [],
#                    'qubits': ({'index': 2,
#                                'register': {'name': 'q', 'size': 5}},
#                               {'index': 1,
#                                'register': {'name': 'q', 'size': 5}})}]},
#   {'num_op': 1,
#    'operations': [{'clbits': (),
#                    'gate': 'rz',
#                    'num_clbits': 0,
#                    'num_qubits': 1,
#                    'params': [1.5707963267948966],
#                    'qubits': ({'index': 2,
#                                'register': {'name': 'q', 'size': 5}},)}]},
#   {'num_op': 1,
#    'operations': [{'clbits': ({'index': 1,
#                                'register': {'name': 'q', 'size': 5}},),
#                    'gate': 'measure',
#                    'num_clbits': 1,
#                    'num_qubits': 1,
#                    'params': [],
#                    'qubits': ({'index': 1,
#                                'register': {'name': 'q', 'size': 5}},)}]},
#   {'num_op': 1,
#    'operations': [{'clbits': (),
#                    'gate': 'sx',
#                    'num_clbits': 0,
#                    'num_qubits': 1,
#                    'params': [],
#                    'qubits': ({'index': 2,
#                                'register': {'name': 'q', 'size': 5}},)}]},
#   {'num_op': 1,
#    'operations': [{'clbits': (),
#                    'gate': 'rz',
#                    'num_clbits': 0,
#                    'num_qubits': 1,
#                    'params': [1.5707963267948966],
#                    'qubits': ({'index': 2,
#                                'register': {'name': 'q', 'size': 5}},)}]},
#   {'num_op': 1,
#    'operations': [{'clbits': ({'index': 2,
#                                'register': {'name': 'q', 'size': 5}},),
#                    'gate': 'measure',
#                    'num_clbits': 1,
#                    'num_qubits': 1,
#                    'params': [],
#                    'qubits': ({'index': 2,
#                                'register': {'name': 'q', 'size': 5}},)}]}],
#  [{'from': 0, 'is_ancilla': False, 'to': 1},
#   {'from': 2, 'is_ancilla': False, 'to': 2},
#   {'from': 1, 'is_ancilla': False, 'to': 3},
#   {'from': 3, 'is_ancilla': False, 'to': 4},
#   {'from': None, 'is_ancilla': True, 'to': 0}])