import { circuit_h_gap, circuit_v_gap, control_gates_type_0, control_gates_type_1, control_gates_type_2, defualt_color, ord_colors, padding, qubit_node_gap, qubit_node_wh, swap_gates } from "./constants"
import { get_original_layer } from "./plan_draw";
import { get_radian_names } from "./util";

let meta_data_area_width = 160, title_area_height = 30;

export function planMachineView(data, operation_data, config) {
  // sizing
  let width = 0, height = 0;
  // machine layout
  let machine = {
    type: "g",
    role: "machine-circuit",
    id: "machine-circuit",
    _class: "machine-circuit",
    x: 0,
    y: 0,
    width: 0,
    height: 0,
    elem: []
  };

  machine.elem.push({
    type: "text",
    id: "title",
    role: "title",
    _class: "title",
    text: "Machine: " + data.name + (data.machine_data.simulator ? " (simulator)" : ""),
    "font-size": 16,
    x: 0,
    y: 16,
    "font-weight": 700,
    "text-anchor": "start",
    "alignment-baseline": "bottom",
  })

  let qubit_nodes = {
    type: "g",
    role: "qubit-nodes",
    id: "qubit-nodes",
    _class: "qubit-nodes",
    x: padding,
    y: padding + title_area_height + circuit_v_gap,
    width: 0,
    height: 0,
    elem: []
  };

  let node_bbox = {};
  for (const node of data?.design?.nodes) {
    let readout_error = data.readout_errors[node.index];
    let gate_info = data.gate_info.filter((d) => d?.qubits?.includes(node.index));
    let qubit_match;
    if (config?.match?.bit_match) {
      qubit_match = config?.match?.bit_match.filter(d => d.to === node.index)[0]
    }
    let data_object = {
      readout_error,
      gate_info,
      qubit_id: node.index,
      original_qubit_id: qubit_match.from,
      match_color: ord_colors[qubit_match.from || data?.design?.nodes.length],
      id: config?.id,
      original_circuit_id: config?.original_circuit_id,
      transpiled_circuit_id: config?.transpiled_circuit_id,
    };
    let g = {
      type: "g",
      role: "qubit-node--group",
      id: `qubit-node-${node.index}--group`,
      _class: "qubit-node--group",
      x: 0,
      y: 0,
      width: qubit_node_wh,
      height: qubit_node_wh,
      elem: [],
      data: data_object
    };
    let x = node.x * (qubit_node_gap + qubit_node_wh);
    let y = node.y * (qubit_node_gap + qubit_node_wh);
    let r = qubit_node_wh / 2;
    g.x = x;
    g.y = y;

    // qubit marker
    g.elem.push({
      type: "circle",
      role: "qubit-node--node",
      id: `qubit-node-${node.index}--node`,
      _class: "qubit-node--node",
      cx: r,
      cy: r,
      r,
      stroke: defualt_color,
      "stroke-width": 2,
      fill: "#ff0000",
      "fill-opacity": readout_error.value
    });

    // qubit marker text
    g.elem.push({
      type: "text",
      role: "qubit-node--marker",
      id: `qubit-node-${node.index}--marker`,
      _class: "qubit-node--marker",
      text: node.index,
      x: r,
      y: r + 2,
      "text-anchor": "middle",
      "alignment-baseline": "middle",
      stroke: defualt_color,
      "stroke-width": 2,
      fill: defualt_color
    });

    // click wrap
    g.elem.push({
      type: "click-wrap",
      role: "qubit-node-click-wrap",
      id: `qubit-node-${node.index}--click-wrap`,
      _class: "qubit-node-click-wrap",
      x: 0,
      y: 0,
      width: qubit_node_wh,
      height: qubit_node_wh,
      data: data_object
    });

    node_bbox[node.index] = [
      [x + r, y],
      [x, y + r], [x + 2 * r, y + r],
      [x + r, y + 2 * r]
    ];
    node_bbox[node.index].x = x;
    node_bbox[node.index].y = y;
    node_bbox[node.index].cx = x + r;
    node_bbox[node.index].cy = y + r;

    // size update
    width = Math.max(width, g.x + g.width);
    height = Math.max(width, g.y + g.height);
    qubit_nodes.elem.push(g);
  }
  qubit_nodes.width = width;
  qubit_nodes.height = height;


  let qubit_edges = {
    type: "g",
    role: "qubit-edges",
    id: "qubit-edges",
    _class: "qubit-edges",
    x: padding,
    y: padding,
    width: 0,
    height: 0,
    elem: []
  };

  let edge_draw_prep = {}
  for (const edge of data?.design?.edges) {
    let ei = edge.toSorted().join(">"), eio = edge.join(">");
    if (!edge_draw_prep[ei]) {
      edge_draw_prep[ei] = {
        nodes: edge,
        from_to: get_edge_xy(node_bbox[edge[0]], node_bbox[edge[1]]),
        bi_dir: false
      };
    } else {
      if (ei !== eio) {
        edge_draw_prep[ei].bi_dir = true;
      }
    }
  }

  let ecnt = 0, edge_dict = {};
  for (const ei in edge_draw_prep) {
    let edge = edge_draw_prep[ei]
    let x1 = edge.from_to[0][0],
      x2 = edge.from_to[1][0],
      y1 = edge.from_to[0][1],
      y2 = edge.from_to[1][1];
    let x = Math.min(x1, x2), y = Math.min(y1, y2);
    let w = Math.max(x1, x2) - Math.min(x1, x2), h = Math.max(y1, y2) - Math.min(y1, y2);
    let edge_angle = angle_btw([w, -h], [w, 0]), edge_angle_inv = edge_angle + 180;

    let g = {
      type: "g",
      role: "qubit-edge--group",
      id: `qubit-edge-${ecnt}--group`,
      _class: "qubit-edge--group",
      x,
      y: y + title_area_height + circuit_v_gap,
      width: w,
      height: h,
      elem: []
    };

    g.elem.push({
      type: "line",
      role: "qubit-edge--edge",
      id: `qubit-edge-${ecnt}--edge`,
      _class: "qubit-edge--edge",
      x1: 0, x2: w, y1: 0, y2: h,
      stroke: defualt_color,
      "stroke-width": 1
    });

    if (edge.bi_dir || (!edge.bi_dir && edge_dir(edge.from_to[0], edge.from_to[1])) > 0) {
      g.elem.push({
        type: "arrow-end",
        role: "qubit-edge--edge-arrow-1",
        id: `qubit-edge-${ecnt}--edge-arrow-1`,
        _class: "qubit-edge--edge-arrow",
        x: w,
        y: h,
        fill: defualt_color,
        "stroke-width": 0,
        rotate: edge_angle
      });
    }

    if (edge.bi_dir || (!edge.bi_dir && edge_dir(edge.from_to[0], edge.from_to[1])) < 1) {
      g.elem.push({
        type: "arrow-end",
        role: "qubit-edge--edge-arrow-2",
        id: `qubit-edge-${ecnt}--edge-arrow-2`,
        _class: "qubit-edge--edge-arrow",
        x: 0,
        y: 0,
        fill: defualt_color,
        "stroke-width": 0,
        rotate: edge_angle_inv
      });
    }

    let w2 = w + padding * 4, h2 = h + padding * 4
    g.elem.push({
      type: "rect",
      role: "qubit-edge--highlight-wrap",
      id: `qubit-edge-${ecnt}--highlight-wrap`,
      _class: "qubit-edge--highlight-wrap highlight-wrap",
      x: w / 2 - w2 / 2,
      y: h / 2 - h2 / 2,
      width: w2,
      height: h2,
      "stroke-width": 0,
      "fill-opacity": 0
    });

    edge_dict[ei] = `qubit-edge-${ecnt}`;
    ecnt++;
    // size update
    qubit_edges.elem.push(g);
  }

  machine.width = width;
  machine.height = height;

  machine.elem.push(qubit_nodes)
  machine.elem.push(qubit_edges)

  // operation animation data;
  let operations = [], lcnt = 0;

  let max_error_rate = 0;
  for (const info of data.gate_info) {
    max_error_rate = Math.max(info.gate_error.value, max_error_rate)
  }
  for (const i in data.readout_errors) {
    max_error_rate = Math.max(data.readout_errors[i].value, max_error_rate)
  }

  let error_cap = Math.ceil(max_error_rate * 100) / 100;

  for (const layer_data of operation_data.layers) {
    let ops = {
      type: "g",
      role: "op-layer-group",
      id: `layer-${lcnt}--op-layer-group`,
      class: "op-layer-group",
      x: padding,
      y: padding + title_area_height + circuit_v_gap,
      width,
      height,
      elem: [],
      data: {}
    }
    let ocnt = 0, total_duration = 0;

    // metadata
    let layer_meta_g = {
      type: "g",
      x: width + circuit_h_gap * 2,
      y: padding + 8,
      elem: []
    };
    layer_meta_g.elem.push({
      type: "text",
      x: 0,
      y: 0,
      "text-anchor": "start",
      "alignment-baseline": "bottom",
      "font-weight": 700,
      text: "Layer info"
    });

    layer_meta_g.elem.push({
      type: "text",
      x: 0,
      y: 14,
      "font-size": 12,
      "text-anchor": "start",
      "alignment-baseline": "bottom",
      text: `Layer: ${lcnt}` + (lcnt === operation_data.layers.length - 1 ? " (last)" : "")
    });

    for (const op_data of layer_data.operations) {
      let gate_info = data.gate_info.filter((d) =>
        bit_order_match(op_data.qubits.map(e => e.index), d?.qubits) &&
        d.gate == op_data.gate
      )?.[0];
      let duration = gate_info?.gate_length?.value || 0;
      total_duration = Math.max(duration, total_duration);
      let gate_error = gate_info?.gate_error?.value || 0;
      let gate_qubits = gate_info?.qubits || op_data.qubits.map(e => e.index);
      if (op_data.gate === "measure") {
        gate_error = data.readout_errors[op_data.qubits[0].index]?.value;
      }

      let { edges, edge_ids } = get_edges(gate_info, edge_dict);
      let match_color;
      let layer_match = get_original_layer(config?.match?.layer_match, "t-o", lcnt, ocnt);
      if (layer_match) {
        match_color =
          ord_colors[(layer_match.layer + layer_match.operation * 10) % ord_colors.length];
      }

      let op = {
        type: "g",
        role: "op-layer-operation-group",
        id: `layer-${lcnt}--operation-${ocnt}--op-group`,
        class: "op-layer-group",
        x: 0,
        y: 0,
        is_timed: true,
        duration,
        elem: [],
        data: {
          original_circuit_id: config?.original_circuit_id,
          transpiled_circuit_id: config?.transpiled_circuit_id,
          layer: lcnt,
          operation: ocnt,
          original_layer: layer_match.layer,
          original_operation: layer_match.operation,
          duration,
          unit: gate_info?.gate_length?.unit,
          edges,
          edge_ids,
          match_color,
          gate_error
        }
      };

      ops.data.unit = gate_info?.gate_length?.unit;

      let controls = [], targets = [], params = [], swaps = [];
      if (control_gates_type_0.includes(op_data.gate)) {
        controls = op_data.qubits.map(d => d.index);
      } else if (control_gates_type_1.includes(op_data.gate)) {
        controls = op_data.qubits.slice(0, -1).map(d => d.index);
        targets = op_data.qubits.slice(-1).map(d => d.index);
      } else if (control_gates_type_2.includes(op_data.gate)) {
        controls = op_data.qubits.slice(0, -2).map(d => d.index);
        targets = op_data.qubits.slice(-2).map(d => d.index);
      } else if (swap_gates.includes(op_data.gate)) {
        swaps = op_data.qubits.map(d => d.index);
      } else {
        targets = op_data.qubits.map(d => d.index);
      }
      params = op_data.params.map(d => get_radian_names(d));

      // markings
      for (const qubit of op_data.qubits) {
        let node_pos = [node_bbox[qubit.index].cx, node_bbox[qubit.index].cy];
        if (controls.includes(qubit.index)) {
          op.elem.push({
            type: "rect",
            id: `layer-${lcnt}--operation-${ocnt}--gate-${op_data.gate}--qubit-${qubit.index}`,
            role: 'layer-op-gate-control',
            _class: 'layer-op-gate-control',
            width: 8,
            height: 8,
            x: node_pos[0] - 4,
            y: node_pos[1] + qubit_node_gap / 2 - 2,
            fill: match_color,
            "stroke-width": 1
          });
        } else if (targets.includes(qubit.index)) {
          let text = op_data.gate
          if (params.length > 0) {
            text += `(${params.join(",")})`
          }
          let op_mark_width = (text.length + 2) * 6;
          op.elem.push({
            type: "rect",
            id: `layer-${lcnt}--operation-${ocnt}--gate-${op_data.gate}--qubit-${qubit.index}`,
            role: 'layer-op-gate-target',
            _class: 'layer-op-gate-target',
            width: op_mark_width,
            height: qubit_node_gap * 0.8,
            x: node_pos[0] - (op_mark_width) / 2,
            y: node_pos[1] + qubit_node_gap / 2 - 3,
            "stroke-width": 1,
            fill: match_color
          });
          op.elem.push({
            type: "text",
            id: `layer-${lcnt}--operation-${ocnt}--gate-${op_data.gate}--qubit-${qubit.index}--marker`,
            role: 'layer-op-gate-target-marker',
            _class: 'layer-op-gate-target-marker',
            x: node_pos[0],
            y: node_pos[1] + qubit_node_gap - 4,
            "font-size": 12,
            "text-anchor": "middle",
            "alignment-baseline": "middle",
            fill: "white",
            text
          });
        } else if (swaps.includes(qubit.index)) {
          op.elem.push({
            type: "rect",
            id: `layer-${lcnt}--operation-${ocnt}--gate-${op_data.gate}--qubit-${qubit.index}`,
            role: 'layer-op-gate-swap',
            _class: 'layer-op-gate-swap',
            width: 12,
            height: 12,
            x: node_pos[0] - 6,
            y: node_pos[1] + qubit_node_wh / 3 - 6,
            fill: match_color,
            "stroke-width": 0
          });
          op.elem.push({
            type: "text",
            id: `layer-${lcnt}--operation-${ocnt}--gate-${op_data.gate}--qubit-${qubit.index}`,
            role: 'layer-op-gate-swap-marker',
            _class: 'layer-op-gate-swap-marker',
            "font-size": 12,
            x: node_pos[0] - 5,
            y: node_pos[1] + qubit_node_wh / 3 - 5,
            "text-anchor": "middle",
            "alignment-baseline": "middle",
            fill: "white",
            text: "×"
          });
        }
      }

      // edge information
      if (op_data.qubits.length > 0) {
        for (let i = 0; i < op_data.length; i++) {
          let qubit_a = op_data.qubits[i];
          for (let j = i + 1; j < op_data.length; j++) {
            let qubit_b = op_data.qubits[j];
            let ei = [qubit_a.index, qubit_b.index].toSorted().join(">");
            if (edge_dict[ei]) {
              op.data.edges.push(edge_dict[ei]);
            }
          }
        }
      }
      // gate error information 
      if (gate_error !== undefined) {
        let gate_error_x = width + circuit_h_gap * 2;
        let gate_error_y = ocnt * qubit_node_wh + padding + 16 + 48;
        let gate_error_g = {
          type: "g",
          role: "op-gate-error-group",
          id: `layer-${lcnt}--operation-${ocnt}--gate-error`,
          class: "op-gate-error",
          x: gate_error_x,
          y: gate_error_y,
          elem: []
        };
        if (ocnt == 0) {
          ops.elem.push({
            x: gate_error_x,
            y: gate_error_y - 4,
            "text-anchor": "start",
            "alignment-baseline": "bottom",
            "font-weight": 700,
            type: "text",
            text: "Gate error info"
          });
          gate_error_g.elem.push({
            type: "text",
            x: meta_data_area_width - padding,
            y: 12,
            "font-size": 12,
            "text-anchor": "end",
            "alignment-baseline": "bottom",
            text: `(${error_cap})`,
            fill: "#999999"
          });
        }
        gate_error_g.elem.push({
          type: "text",
          role: "op-gate-error-group-label",
          id: `layer-${lcnt}--operation-${ocnt}--gate-error--label`,
          class: "op-gate-error-label",
          x: 0,
          y: 12,
          "font-size": 12,
          "text-anchor": "start",
          "alignment-baseline": "bottom",
          text: op_data.gate + `(${gate_qubits.join(",")})` + ": " + gate_error.toString().slice(0, 7)
        });
        gate_error_g.elem.push({
          type: "rect",
          role: "op-gate-error-group-bar-wrap",
          id: `layer-${lcnt}--operation-${ocnt}--gate-error--bar-wrap`,
          class: "op-gate-error-bar-wrap",
          x: 0,
          y: 22,
          width: meta_data_area_width - padding,
          height: 16,
        })
        gate_error_g.elem.push({
          type: "rect",
          role: "op-gate-error-group-bar",
          id: `layer-${lcnt}--operation-${ocnt}--gate-error--bar`,
          class: "op-gate-error-bar",
          x: 0,
          y: 22,
          width: (meta_data_area_width - padding) * (gate_error / error_cap),
          height: 16,
          fill: "#ff0000",
          "fill-opacity": gate_error / error_cap
        })
        gate_error_g.elem.push({
          type: "click-wrap",
          role: "op-gate-error-group-click-wrap",
          id: `layer-${lcnt}--operation-${ocnt}--gate-error--click-wrap`,
          class: "op-gate-error-click-wrap",
          x: 0,
          y: 0,
          width: (meta_data_area_width - padding),
          height: qubit_node_wh,
          data: {
            gate_error_info: {
              gate_error,
              layer: lcnt,
              operation: ocnt,
              qubits: gate_qubits,
              gate: op_data.gate,
              gate_duration: duration,
              duration_unit: gate_info?.gate_length?.unit
            }
          }
        })
        op.elem.push(gate_error_g);
      }
      ops.elem.push(op);
      ocnt++;
    }

    layer_meta_g.elem.push({
      type: "text",
      x: 0,
      y: 28,
      "font-size": 12,
      "text-anchor": "start",
      "alignment-baseline": "bottom",
      text: `Duration: ${total_duration.toString().slice(0, 7)} (${ops.data.unit || 'ns'})`
    });

    ops.elem.push(layer_meta_g);

    lcnt++;
    ops.is_timed = true;
    ops.duration = total_duration;
    operations.push(ops);
  }


  return {
    type: "svg",
    width: width + padding * 2 + meta_data_area_width + circuit_h_gap * 2,
    height: height + padding * 2 + title_area_height + circuit_v_gap,
    viewBox: [0, 0, width + padding * 4 + meta_data_area_width, height + padding * 2 + title_area_height + circuit_v_gap],
    groups: {
      machine
    },
    operations
  };
}

function get_edges(gate_info, edge_dict) {
  let edges = [], edge_ids = [];
  if (gate_info) {
    let qubits = gate_info.qubits;
    if (qubits.length > 0) {
      qubits = qubits.toSorted();
      for (let i = 0; i < qubits.length; i++) {
        for (let j = 0; j < qubits.length; j++) {
          let ei = qubits[i] + ">" + qubits[j]
          if (edge_dict[ei]) {
            edges.push([qubits[i], qubits[j]]);
            edge_ids.push(edge_dict[ei]);
          }
        }
      }
    }
  }
  return { edges, edge_ids };
}

function get_edge_xy(b1, b2) {
  let len = 9000000000, rec;
  for (const ba1 of b1) {
    for (const ba2 of b2) {
      let d = dist(ba1, ba2);
      if (d < len) {
        len = d;
        rec = [ba1, ba2];
      }
    }
  }
  return rec;
}

function dist(a, b) {
  return Math.sqrt(
    Math.pow(a[0] - b[0], 2) + Math.pow(a[1] - b[1], 2)
  );
}

function angle_btw(a, b) {
  let ang = Math.acos(
    dot(a, b) / (inner(a) * inner(b))
  );
  if (isNaN(ang)) {
    ang = Math.PI / 2
  }
  return (ang / Math.PI) * 180
}
function dot(a, b) {
  return (a[0] * b[0] + a[1] * b[1])
}
function inner(a) {
  return Math.sqrt(
    Math.pow(a[0], 2) + Math.pow(a[1], 2)
  )
}
function edge_dir(a, b) {
  if (a[0] <= b[0] && a[1] <= b[1]) return 1;
  else return -1
}

function bit_order_match(a, b) {
  return a.join(",") === b.join(",");
}