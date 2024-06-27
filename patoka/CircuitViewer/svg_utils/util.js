export function get_radian_names(value) {
  let ratio = value / Math.PI
  if (ratio == 0)
    return "0";
  else if (ratio == 1 / 4)
    return "π/4";
  else if (ratio == 1 / 3)
    return "π/3";
  else if (ratio == 1 / 2)
    return "π/2";
  else if (ratio == 2 / 3)
    return "2π/3";
  else if (ratio == 3 / 4)
    return "3π/4";
  else if (ratio == 1)
    return "π";
  else if (ratio == -1 / 4)
    return "-π/4";
  else if (ratio == -1 / 3)
    return "-π/3";
  else if (ratio == -1 / 2)
    return "-π/2";
  else if (ratio == -2 / 3)
    return "-2π/3";
  else if (ratio == -3 / 4)
    return "-3π/4";
  else if (ratio == -1)
    return "-π";
}

export function getGradient(colors) {
  let n = colors.length;
  if (n <= 1) return null;
  let u = 100 / (n - 1);
  let res = colors.map((d, i) => {
    return {
      offset: (u * i) + "%",
      "stop-color": d
    }
  });
  return res;
}

const svgns = 'http://www.w3.org/2000/svg';

export function addGradientDef(pid, def) {
  // Create a <stop> element and set its offset based on the position of the for loop.
  let svgdefs = document.querySelector(`#${pid} defs`);
  let svg = document.querySelector(`#${pid}`);
  if (!svgdefs) {
    svgdefs = document.createElementNS(svgns, "defs");
  }
  let g = document.createElementNS(svgns, "linearGradient");
  g.setAttribute("id", def.id);
  g.setAttribute("x1", 0);
  g.setAttribute("x2", 0);
  g.setAttribute("y1", 0);
  g.setAttribute("y2", 1);
  def.grad_data.forEach((d) => {
    let stop = document.createElementNS(svgns, 'stop');
    stop.setAttribute('offset', d.offset);
    stop.setAttribute('stop-color', d["stop-color"]);
    g.appendChild(stop);
  });
  svgdefs.appendChild(g);
  svg.appendChild(svgdefs);
}
export function removeGradientDef(pid, def_ids) {

}