import copy
import numpy as np
import pprint
from match_circuit import get_gate
from match_circuit import get_radian_names

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

def merge_gates(this, prevs, nexts):
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

def match_circuits(explication, transpiled, mapping):
    # outputs
    check = circuit_layout_index_map(trans_layout)
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
                    (merged_data, merged_circit)= merge_gates(ex, prevs[1:], nexts[1:])
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



# def traverseForMatching(origin, origin_exp, trans, mapping, start=0):
#     o_count = 0
#     bitMap = makeBitMapFromMapping(mapping)
#     t_point = start
#     memo = []
#     # print(",,,")
#     # print(start)
#     for ei in range(len(origin_exp)):
#         e_layer = copy.deepcopy(origin_exp[ei])
        
#         for eop in e_layer:
#             eop["qubits"] = matchBitsWithMapping(bitMap, eop["qubits"])
#             o_count += 1
#         for ti in range(t_point, len(trans)):
#             t_layer = trans[ti]["operations"]
#             parts = isPartOf(e_layer, t_layer, mapping)
#             # print(parts)
#             if parts is not False:
#                 t_point = ti
#                 for part in parts:
#                     memo.append((ti, part))
#                 break
                
#     return {
#         "matches": memo,
#         "complete": len(memo) == o_count,
#         "un_matches":  o_count - len(memo)
#     }
