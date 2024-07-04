import { circuit_h_gap, circuit_line_height, circuit_v_gap, default_fill, defualt_color } from "../constants";
import { getYH } from "../sizing";

let gate_width = 12;
let gate_name = "barrier"
export let BARRIER = {
  name: gate_name,
  is_custom: true,
  width: gate_width,
  plan: function (op, li) {
    let plan = {
      id: `layer-${li}--${gate_name}--group`,
      type: "g",
      x: 0,
      y: 0,
      width: gate_width,
      height: 0,
      elem: []
    };
    // 0. get x, y, h 
    let pos = getYH(op);
    plan.y = pos.y;
    plan.height = pos.height;

    // 1. rectangle 
    let rect = {
      id: `layer-${li}--${gate_name}--wrap`,
      type: "rect",
      "stroke-width": 1,
      stroke: "#cccccc",
      fill: "#cccccc",
      width: gate_width,
      x: 0,
      y: 0,
      height: pos.height,
    }
    plan.elem.push(rect);

    return plan;
  }
};