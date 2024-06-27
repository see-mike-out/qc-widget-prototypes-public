import { planGateDrawing } from "./plan_gate";

import { circuit_line_height, circuit_v_gap, circuit_h_gap, qubit_ref_width, padding, moment_bar_height, ord_colors } from "./constants"
import { get_radian_names } from "./util";

export function planDrawing(data, config) {
  if (!data) return null;

  // define overall sizing
  let width = 0, height = 0, body_height = 0, qubits = [], circuit_lines = [];

  let is_transpiled_bitmatch = !config?.is_original && config?.match?.bit_match
  let transpiled_bitmatch = config?.match?.bit_match;
  let qubit_area_width = qubit_ref_width + (!config?.is_original && config?.match?.bit_match ? qubit_ref_width : 0);

  // global phase
  let phase_marker;
  if (data.global_phase) {
    phase_marker = {
      type: "g",
      x: padding,
      y: padding,
      role: "global-phase",
      id: `global-phase`,
      elem: []
    }
    phase_marker.elem.push({
      type: "text",
      x: qubit_area_width,
      y: moment_bar_height,
      role: "global-phase--marker",
      id: "global-phase--marker",
      "text-anchor": "end",
      "font-size": 12,
      text: `Global phase: ${get_radian_names(data.global_phase)}`
    })
  }

  // qubit column
  if (data?.num_qubits > 0) {
    width += qubit_area_width;
    body_height = circuit_line_height * data.num_qubits + circuit_v_gap * (data.num_qubits - 1);
    height += body_height;
    for (let qubit of data.qubits) {
      let trans_prefix = "";
      let bit_match;
      if (config?.is_original) {
        bit_match = transpiled_bitmatch.filter((q) => q.from == qubit.index)[0];
      } else {
        bit_match = transpiled_bitmatch.filter((q) => q.to == qubit.index)[0];
      }
      let match_color = ord_colors[bit_match.from || data.qubits.length]
      if (is_transpiled_bitmatch) {
        if (bit_match && !bit_match.is_ancilla) {
          trans_prefix = qubit.register.name + bit_match.from + ' > ';
        } else if (bit_match && bit_match.is_ancilla) {
          trans_prefix = "ancilla/" + bit_match.to + ' > ';
        }
      }

      let qubit_group = {
        type: "g",
        x: 0,
        y: (circuit_line_height + circuit_v_gap) * qubit.index,
        width: qubit_area_width,
        height: circuit_line_height,
        role: "qubit-group",
        id: `qubit-${qubit.index}--group`,
        _class: `qubit-group qubit-${qubit.index}` + (config?.is_original ? " original" : " transpiled"),
        data: {
          qubit,
          bit_match,
          matched_circuit_id: config?.matched_circuit_id,
          this_circuit_id: config?.this_circuit_id,
          matched_machine_id: config?.matched_machine_id,
          match_color
        },
        elem: []
      }

      qubit_group.elem.push({
        type: "rect",
        x: 0,
        y: 0,
        width: qubit_area_width,
        height: circuit_line_height,
        role: "qubit-background",
        "fill-opacity": 0.2,
        "stroke": "transparent",
        _class: `qubit-background qubit-${qubit.index}` + (config?.is_original ? " original" : " transpiled")
      });

      qubit_group.elem.push({
        type: "text",
        text: trans_prefix + qubit.register.name + qubit.index,
        "text-anchor": "end",
        "alignment-baseline": "middle",
        x: qubit_area_width,
        y: circuit_line_height / 2,
        width: qubit_area_width,
        height: circuit_line_height,
        role: "qubit",
        _class: `qubit qubit-${qubit.index}` + (config?.is_original ? " original" : " transpiled"),
      });

      qubit_group.elem.push({
        type: "click-wrap",
        x: 0,
        y: 0,
        width: qubit_area_width,
        height: circuit_line_height,
        role: "qubit-group-click-wrap",
        data: {
          qubit,
          bit_match,
          matched_circuit_id: config?.matched_circuit_id,
          this_circuit_id: config?.this_circuit_id,
          matched_machine_id: config?.matched_machine_id,
          match_color
        },
      });

      qubits.push(qubit_group);

      circuit_lines.push({
        type: "line",
        x1: 0,
        y1: qubit.index * circuit_line_height + circuit_v_gap * qubit.index + circuit_line_height / 2 - 0.5,
        "stroke-width": 1
      });
    }
  }
  // clibt row
  if (data.num_clbits > 0) {
    height += circuit_line_height + circuit_v_gap;
    qubits.push({
      type: "text",
      text: "C/" + data.num_clbits,
      "text-anchor": "end",
      "alignment-baseline": "middle",
      x: qubit_area_width,
      y: body_height + circuit_v_gap + circuit_line_height / 2,
      width: qubit_area_width,
      height: circuit_line_height,
      role: "clbit",
      data: data.clbits
    });

    qubits.push({
      type: "click-wrap",
      x: 0,
      y: body_height + circuit_v_gap,
      width: qubit_area_width,
      height: circuit_line_height,
      role: "qubit-group-click-wrap",
      data: data.clbits
    });
    circuit_lines.push({
      type: "double-line",
      x1: 0,
      y1: body_height + circuit_v_gap + circuit_line_height / 2 - 2,
      "stroke-width": 4
    });
  }

  // circuit body (gates)
  let circuit_width = 0;
  let circuit_body = [];
  let prev_x = circuit_h_gap;
  // per layer
  for (let i = 0; i < data.layers.length; i++) {
    let layer = data.layers[i];
    let layer_group = {
      id: `layer-${i}--group`,
      type: "g",
      role: "layer-group",
      _class: `layer-wrap layer-${i}` + (config?.is_original ? " original" : " transpiled"),
      x: prev_x,
      y: 0,
      width: 0,
      height,
      elem: [],
      data: {
        layer,
      }
    };

    // per gate
    let layer_width = 0;
    for (let j = 0; j < layer.operations.length; j++) {
      let op = layer.operations[j]
      let op_plan = planGateDrawing(op, i);

      // layer match
      let layer_match, match_color;
      if (config?.is_original) {
        layer_match = get_original_layer(config?.match?.layer_match, "o-t", i, j);
        match_color = ord_colors[(i + j * 10) % ord_colors.length];
      } else {
        layer_match = get_original_layer(config?.match?.layer_match, "t-o", i, j);
        if (layer_match)
          match_color =
            ord_colors[(layer_match.layer + layer_match.operation * 10) % ord_colors.length];
      }

      if (op_plan) {
        op_plan._class = `gate-wrap layer-${i} gate-${j}` + (config?.is_original ? " original" : " transpiled");
        op_plan.data.operation_index = j;
        op_plan.data.layer_match = layer_match;
        op_plan.data.match_color = match_color;
        op_plan.data.matched_circuit_id = config?.matched_circuit_id;
        op_plan.data.this_circuit_id = config?.this_circuit_id;
        op_plan.data.matched_machine_id = config?.matched_machine_id;

        op_plan.elem.push({
          id: `layer-${i}--${op.gate}--click-wrap`,
          _class: `gate-group-click-wrap`,
          role: `gate-group-click-wrap`,
          type: "click-wrap",
          x: 0,
          y: 0,
          width: op_plan.width,
          height: op_plan.height,
          data: op_plan.data
        })
      }

      layer_group.elem.push(op_plan);
      layer_width = Math.max(layer_width, op_plan?.width || 32);
    }
    layer_group.width = layer_width;

    layer_group.elem.forEach((el) => {
      if (el && el.width < layer_width) {
        el.x += (layer_width - el.width) / 2
      }
    });

    // add interaction wrap
    layer_group.elem.unshift({
      id: `layer-${i}--interaction-wrap`,
      _class: "interation-wrap",
      type: "rect",
      x: - (circuit_h_gap / 2),
      y: config?.show_moments ? (- moment_bar_height - circuit_v_gap - padding) : 0,
      width: layer_width + circuit_h_gap,
      height: config?.show_moments ? height + moment_bar_height + circuit_v_gap + padding * 2 : height,
      fill: "rgba(0, 0, 0, 0)",
      stroke: "transparent"
    });

    prev_x = prev_x + layer_width + circuit_h_gap;
    circuit_width = circuit_width + layer_width + circuit_h_gap
    circuit_body.push(layer_group);
  }

  // update sizing
  circuit_width = circuit_width + circuit_h_gap;
  width += circuit_width + circuit_h_gap;

  // update circuit line pos
  circuit_lines.forEach((line) => {
    line.x2 = circuit_width;
    line.y2 = line.y1;
  });

  let final_plan = {
    type: "svg",
    width: width + padding * 2,
    height: height + padding * 2,
    viewBox: [0, 0, width + padding * 2, height + padding * 2],
    groups: {
      qubit_group: {
        id: `qubits--group`,
        type: "g",
        x: padding,
        y: padding,
        width: qubit_area_width,
        height,
        elem: qubits,
        role: "qubits",
        data: {
          qubits: data.qubits,
          clbits: data.clbits,
          num_qubits: data.num_qubits,
          num_clbits: data.num_clbits
        }
      },
      circuit_line_group: {
        id: `circuit-line--group`,
        type: "g",
        x: padding + qubit_area_width + circuit_h_gap,
        y: padding,
        width: circuit_width,
        height,
        elem: circuit_lines,
        role: "circuit_lines"
      },
      circuit_group: {
        id: `circuit-body--group`,
        type: "g",
        x: padding + qubit_area_width + circuit_h_gap,
        y: padding,
        width: circuit_width,
        height,
        elem: circuit_body,
        role: "circuit_body",
        data: data.layers
      },
      phase_marker
    }
  }

  //---------- conditionals

  // show moments
  if (config?.show_moments) {
    let moment_group = {
      id: `moment--group`,
      type: "g",
      x: padding + qubit_area_width + circuit_h_gap,
      y: padding,
      width: circuit_width,
      height: moment_bar_height,
      elem: []
    };

    moment_group.elem = circuit_body.map((m, i) => {
      return {
        id: `moment-${i}--marker`,
        type: "text",
        text: i,
        x: m.x + m.width / 2,
        y: moment_bar_height / 2,
        "font-size": 12,
        data: m.data,
        "text-anchor": "middle",
        "alignment-baseline": "middle",
      };
    });

    let y_increment = moment_bar_height + circuit_v_gap;
    final_plan.height += y_increment;
    final_plan.viewBox[3] += y_increment;
    final_plan.groups.qubit_group.y += y_increment;
    final_plan.groups.circuit_line_group.y += y_increment;
    final_plan.groups.circuit_group.y += y_increment;

    final_plan.groups.moment_group = moment_group;
  }


  return final_plan;
}

// fix : include operation ids
export function get_original_layer(match, dir, li, oi) {
  if (dir === "o-t") {
    // origintal to transpiled
    let searched = match.filter(d => d?.from?.[0] == li && d?.from?.[1] == oi)?.[0];
    if (searched) {
      return {
        layer: searched.from[0],
        operation: searched.from[1],
        matches: searched.to.matches,
        complete: searched.to.complete
      };
    } else {
      return null;
    }
  } else if (dir === "t-o") {
    // transpiled to original
    let searched = match.filter(d => {
      return d.to.matches.some((e) => {
        return e?.[0] == li && e?.[1] == oi
      });
    })?.[0];
    if (searched) {
      return { layer: searched.from[0], operation: searched.from[1], colleagues: searched.to.matches, complete: searched.to.complete };
    } else {
      return null;
    }
  }
  return null;
}