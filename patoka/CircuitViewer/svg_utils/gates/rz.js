import { default_fill, defualt_color } from "../constants";
import { getYH } from "../sizing";
import { get_radian_names } from "../util";

let gate_width = 64;
let gate_name = "rz"
export let RZ = {
  name: gate_name,
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
      strokeWidth: 1,
      strokeColor: defualt_color,
      fill: default_fill,
      width: gate_width,
      x: 0,
      y: 0,
      height: pos.height
    }
    plan.elem.push(rect);
    // 4. marker
    let marker = {
      id: `layer-${li}--${gate_name}--marker`,
      type: "text",
      x: gate_width / 2,
      y: pos.height / 2,
      "text-anchor": "middle",
      "alignment-baseline": "middle",
      text: `Rz(${get_radian_names(op.params[0])})`
    }
    plan.elem.push(marker);

    return plan;
  }
};