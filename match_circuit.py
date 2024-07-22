import pprint
import math
import copy
import numpy as np

import qiskit.circuit.library as gates
import qiskit.circuit as QCR
from qiskit.circuit import QuantumCircuit

from qiskit_draw_utils import getCircuitLayout

# circuit match
def matchCircuitLayouts(origin, trans, pass_manager):
    # todo: need to come up with some dynamic programming method
    origin_explicated = []
    mapping = trans[1]
    simplified_mapping = {}
    for m in mapping:
        simplified_mapping[m["from"]] = m["to"]
    # match original layer and transpiled layer
    explication = []
    for oli in range(len(origin[0])):
        o_layer = origin[0][oli]
        o_layer_ops = o_layer["operations"]
        for opi in range(len(o_layer_ops)):
            o_op = o_layer_ops[opi]
            op_explicated = explicate_circuit(o_op, pass_manager)
            explication.append(op_explicated)
    
    matches, check = match_circuits(explication, trans[0], simplified_mapping, pass_manager)
    memo = []
    ecnt = 0
    for oli in range(len(origin[0])):
        o_layer = origin[0][oli]
        o_layer_ops = o_layer["operations"]
        for opi in range(len(o_layer_ops)):
            this_match = matches[ecnt]
            item = {
                "from": [oli, opi],
                "to": {
                    "complete": len(this_match) == len(explication[ecnt]),
                    "matches": this_match,
                    "un_matches": abs(len(this_match) - len(explication[ecnt]))
                }
            }
            memo.append(item)
            ecnt = ecnt + 1
    return {
        "layer_match": memo,
        "bit_match": mapping
    }


def match_circuits(explication, transpiled, mapping, pass_manager):
    # outputs
    check = circuit_layout_index_map(transpiled)
    matches = {}
    collocated = {}
    # for the explication of each operation
    ecnt = 0 
    for ex in explication:
        local_matches = []
        # for each layer
        lcnt = 0 
        original_op_counts = 0
        for layer in ex:
            local_matches.append([])
            # for each operation in the current layer (original)
            for _op in layer:
                op = copy.deepcopy(_op)
                op["qubits"] = [ {"register": qubit["register"], "index": mapping[qubit["index"]] } for qubit in op["qubits"]]
                q_index = [q["index"] for q in op["qubits"]]
                original_op_counts = original_op_counts + 1
                # for each transpiled layer
                for tli in range(0, len(transpiled)):
                    # for each operation in the current transpiled layer    
                    tcnt = 0
                    for t_op in transpiled[tli]["operations"]:
                        # pass if it was already matched
                        if check[(tli, tcnt)]["value"]:
                            pass
                        # compare
                        t_q_index = [tq["index"] for tq in t_op["qubits"]]
                        if np.array_equal(q_index, t_q_index) and op["gate"] == t_op["gate"] and np.array_equal(op["params"], t_op["params"]):
                            # add possibilities
                            local_matches[lcnt].append((tli, tcnt, op["gate"]))
                        elif op["gate"] == t_op["gate"] and op["gate"] == "barrier":
                            local_matches[lcnt].append((tli, tcnt, op["gate"]))
                        tcnt = tcnt + 1
            lcnt = lcnt + 1
        # get the best possibility (earlier in the pass)
        matches[ecnt] = find_conseq(local_matches)
        if len(matches[ecnt]) == 0:
            qubits = []
            for layer in ex:
                for op in layer:
                    for qubit in op["qubits"]:
                        qubits.append(qubit["index"])
            qubits = np.unique(qubits).tolist()
            next_in_line = get_next_in_line(qubits, explication, ecnt)
            next_in_line.insert(0, [])
            prev_in_line = get_prev_in_line(qubits, explication, ecnt)
            prev_in_line.insert(0, [])
            compiled_match_collections = []
            score_collections = []
            for ni in range(len(next_in_line)):
                nexts = next_in_line[0:ni + 1]
                for pi in range(len(prev_in_line)):
                    prevs = prev_in_line[0:pi + 1]
                    (merged_data, merged_circit)= merge_gates(ex, prevs[1:], nexts[1:], pass_manager)
                    (merged, temp_mapping, _) = merged_data
                    mlcnt = 0
                    mocnt = 0
                    compiled_matches = []
                    merged_op_count = 0
                    for mlayer in merged:
                        for op in mlayer["operations"]:
                            for qubit in op["qubits"]:
                                qubit["index"] = find_from_qubit_mapping(qubit["index"], temp_mapping, "from")
                            op["qubits"] = [ {"register": qubit["register"], "index": mapping[qubit["index"]] } for qubit in op["qubits"]]
                            merged_op_count = merged_op_count + 1
                    if original_op_counts < merged_op_count:
                        pass
                    for mlayer in merged:
                        ops = copy.deepcopy(mlayer["operations"])
                        for op in ops:
                            compiled_matches.append([])
                            q_index = get_qubit_indices(op["qubits"])
                            # for each transpiled layer
                            for tli in range(0, len(transpiled)):
                                # for each operation in the current transpiled layer    
                                tcnt = 0
                                for t_op in transpiled[tli]["operations"]:
                                    t_q_index = [tq["index"] for tq in t_op["qubits"]]
                                    if np.array_equal(q_index, t_q_index) and op["gate"] == t_op["gate"] and np.allclose(op["params"], t_op["params"]):
                                        # add possibilities
                                        compiled_matches[mocnt].append((tli, tcnt, op["gate"]))
                                    elif op["gate"] == t_op["gate"] and op["gate"] == "barrier":
                                        compiled_matches[mocnt].append((tli, tcnt, op["gate"]))
                                    tcnt = tcnt + 1
                            mocnt = mocnt + 1
                        mlcnt = mlcnt + 1
                        
                        found, score, _, is_single_path = find_conseq_alt(compiled_matches)
                        
                        if len(found) > 0 and not is_single_path:
                            compiled_match_collections.append(found)
                            score_collections.append(score)
                        elif len(found) > 0 and is_single_path:
                            for f in found:
                                compiled_match_collections.append(f)
                                score_collections.append(score)

            if len(compiled_match_collections) > 0:
                max_start_point = np.max([p[0][0] for p in compiled_match_collections]) + 1
                r_scores = [reverse_path_score(p) for p in compiled_match_collections]
                start_points = [p[0][0] for p in compiled_match_collections]
                path_lenghts_diff = [abs(len(p) - original_op_counts) for p in compiled_match_collections]

                score_board = np.array([
                    np.argsort(path_lenghts_diff),
                    np.argsort(start_points),
                    np.argsort(r_scores)
                ]).T
                item_scores = np.zeros(len(compiled_match_collections))
                for i in range(len(score_board)):
                    item_scores[score_board[i][0]] += i
                    item_scores[score_board[i][1]] += i
                    item_scores[score_board[i][1]] += i
                alt_match = compiled_match_collections[np.argmin(item_scores)]
            
            if alt_match is not None:
                matches[ecnt] = alt_match
        for index in matches[ecnt]:
            check[index[0:2]]["value"] = True
            if "from" not in check[index[0:2]]:
                check[index[0:2]]["from"] = []    
            check[index[0:2]]["from"].append(ecnt)
        ecnt = ecnt + 1
    return matches, check

# gate explications
def get_gate(gate_name, n_qubits, params):
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
    
    return gate
    
def get_gate_components(gate_name, n_qubits, params, pass_manager):
    gate = get_gate(gate_name, n_qubits, params)
    
    if gate is not None and gate.definition is not None:
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
        txt = op["gate"] + "_"  + "|".join([str(p) for p in op["params"]]) + "_"  + ("|".join(str(b["index"]) for b in op["qubits"]) if op["gate"] != "barrier" else "")
        l.append(txt)
    return l


ratio_divider = [2, 3, 4, 6, 8, 16, 32]

def get_radian_names(value):
  ratio = value / math.pi
  if ratio == 0:
      return "0"
  elif ratio == 1:
    return "π";
  elif ratio == -1:
    return "-π";
  else:
    sign = "-" if ratio < 0 else ""
    abs_ratio = abs(ratio)
    done = []
    for div in ratio_divider: 
      for nom in range(div):
        if (nom/div) not in done:
          if abs_ratio == nom / div:
            return sign + ("" if nom == 1 else str(nom)) + "π/" + str(div)
          else:
            done.append(nom / div)
    return value

def find_conseq(local_matches):
    length = len(local_matches)
    possibilities = []
    if length > 1:
        for i in range(length):
            cur_row = local_matches[i]
            for item in cur_row:
                cases = find_conseq_recur(item, local_matches[i+1:3])
                for case in cases:
                    if len(case) == length - 1:
                        possibilities.append([item] + case)
    elif length == 1 and len(local_matches[0]) > 0:
        possibilities = [[item] for item in local_matches[0]]
    if len(possibilities) > 0:
        starting_points = [case[0][0] for case in possibilities]
        return possibilities[np.argmin(starting_points)]
    else:
        return []

def find_conseq_recur(seed, sub_matches):
    if sub_matches is None or len(sub_matches) == 0:
        return []
    elif len(sub_matches) == 1:
        possibilities = []
        for sub_item in sub_matches[0]:
            if is_next(seed, sub_item):
                possibilities.append([sub_item])
        return possibilities
    else:
        possibilities = []
        for sub_item in sub_matches[0]:
            if is_next(seed, sub_item):
                next_seq = find_conseq_recur(sub_item, sub_matches[1:len(sub_matches)])
                for next_item in next_seq:
                    possibilities.append([sub_item] + next_item)
        return possibilities 

def is_next(a, b):
    return a[0] + 1 == b[0]

def circuit_layout_index_map(layout, default_value=False):
    index_map = {}
    for li in range(len(layout)):
        ops = layout[li]["operations"]
        for oi in range(len(ops)):
            index_map[(li, oi)] = { 
                "gate": ops[oi]["gate"],
                "qubits": [q["index"] for q in  ops[oi]["qubits"]],
                "value": default_value } 
    return index_map

def get_next_in_line(qubits, explication, from_index):
    output = []
    for ei in range(from_index + 1, len(explication)):
        ex = explication[ei]
        for li in range(len(ex)):
            layer = ex[li]
            for oi in range(len(layer)):
                op = layer[oi]
                op_qubits = [q["index"] for q in op["qubits"]]
                is_matched = 0 < sum([1 if _q in op_qubits else 0 for _q in qubits])
                if len(output) == 0 and not is_matched:
                    pass
                elif len(output) > 0 and not is_matched:
                    return output
                elif is_matched:
                    output.append((ei, li, oi, op))
    return output

# len(qubits) == len(op_qubits) and len(qubits) ==
def get_prev_in_line(qubits, explication, from_index):
    output = []
    for ei in reversed(range(0, from_index)):
        ex = explication[ei]
        for li in range(len(ex)):
            layer = ex[li]
            for oi in range(len(layer)):
                op = layer[oi]
                op_qubits = [q["index"] for q in op["qubits"]]
                is_matched = 0 < sum([1 if _q in op_qubits else 0 for _q in qubits])
                if len(output) == 0 and not is_matched:
                    pass
                elif len(output) > 0 and not is_matched:
                    return output
                elif is_matched:
                    output.append((ei, li, oi, op))
    return output

def get_qubit_indices(qubits):
    return [q["index"] for q in qubits]
    
def build_circuit(instructions, size, pass_manager):
    circ = QuantumCircuit(size, size)
    for inst in instructions:
        if inst[0].name != "measure": 
            
            circ.append(inst[0], inst[1])
        else:
            circ.append(inst[0], inst[1], inst[1])
    circ_trans = pass_manager.run(circ)
    
    return (getCircuitLayout(circ_trans), circ_trans)

def merge_gates(this, prevs, nexts, pass_manager):
    this_flat = []
    used_qubits = []
    for layer in this:
        for op in layer:
            gate_obj = get_gate(op["gate"], op["num_qubits"], op["params"])
            gate_qubits = get_qubit_indices(op["qubits"])
            if gate_obj is None:
                if op["gate"] == "measure":
                    gate_obj = QCR.measure()
                elif op["gate"] == "barrier":
                    gate_obj = QCR.barrier(op["num_qubits"])
            this_flat.append((gate_obj, gate_qubits))
            used_qubits = used_qubits + gate_qubits
    prevs_flat = []
    for item in prevs:
        if len(item) > 0:
            op = item[3]
            gate_obj = get_gate(op["gate"], op["num_qubits"], op["params"])
            gate_qubits = get_qubit_indices(op["qubits"])
            if gate_obj is None:
                if op["gate"] == "measure":
                    gate_obj = QCR.Measure()
                elif op["gate"] == "barrier":
                    gate_obj = QCR.Barrier(op["num_qubits"])
            prevs_flat.append((gate_obj, gate_qubits))
            used_qubits = used_qubits + gate_qubits
    nexts_flat = []
    for item in nexts:
        if len(item) > 0:
            op = item[3]
            gate_obj = get_gate(op["gate"], op["num_qubits"], op["params"])
            gate_qubits = get_qubit_indices(op["qubits"])
            if gate_obj is None:
                if op["gate"] == "measure":
                    gate_obj = QCR.Measure()
                elif op["gate"] == "barrier":
                    gate_obj = QCR.Barrier(op["num_qubits"])
            nexts_flat.append((gate_obj, gate_qubits))
            used_qubits = used_qubits + gate_qubits
    used_qubits = np.unique(used_qubits)
    n_qubits_needed = max(used_qubits) + 1
    (circ, circ_origin) = build_circuit(list(reversed(prevs_flat)) + this_flat + nexts_flat, n_qubits_needed, pass_manager)
    return (circ, circ_origin)

def find_from_qubit_mapping(index, mapping, direct="to"):
    anti_direct = "from" if direct == "to" else "to"
    for item in mapping:
        if item[anti_direct] == index:
            return item[direct]
    return None
def scoring_seq(p, n):
    if p[0] == n[0]:
        return 0
    elif p[0] + 1 == n[0]:
        return 1
    elif p[0] > n[0]:
        return 100000000
    else:
        return abs(n[0] - p[0])

def find_conseq_alt(_local_matches):
    local_matches = []
    for m in _local_matches:
        if len(m) > 0:
            local_matches.append(m)
    if len(local_matches) == 0:
        return [], 0, [], False
    scores = []
    for i in range(len(local_matches)):
        row = local_matches[i]
        scores.append([])
        prev_row = local_matches[i-1] if i > 0 else None
        for j in range(len(row)):
            scores[i].append({})
            item = row[j]
            if i == 0:
                scores[i][j] = { "this": item, "score": 0, "prev": None } 
            else:
                min_score = 100000000
                for pj in range(len(prev_row)):
                    prev_path = prev_row[pj]
                    temp_score = scoring_seq(prev_path, item)
                    if temp_score <= min_score:
                        min_score = temp_score
                        scores[i][j] = { "this": item, "score": min_score + scores[i-1][pj]["score"], "prev": prev_path }
            
    path_restruction = []
    final_score = 0
    for i in reversed(range(len(scores))):
        if i > 0:
            score_row = scores[i]
            if len(score_row) > 0:
                score_values = [score_item["score"] for score_item in score_row]
                min_k = np.argmin(score_values)
                min_score = score_row[min_k]
                path_restruction.append(min_score["this"])
                if i == 1:
                    path_restruction.append(min_score["prev"])
    
    path_restruction = list(reversed(path_restruction))
    final_score = np.min([score_item["score"] for score_item in scores[len(scores)-1]])
    if len(scores) == 1:
        path_restruction = [[score["this"]] for score in scores[0]]
        final_score = 0
    return (path_restruction, final_score, scores, (len(scores) == 1))

def reverse_path_score(paths):
    r_score = 0
    if len(paths) <= 1:
        return 0
    for i in range(1, len(paths)):
        prev = paths[i-1]
        this = paths[i]
        if this[0] < prev[0]:
            r_score = prev[0] - this[0]
    return r_score
