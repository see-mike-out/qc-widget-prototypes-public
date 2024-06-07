export const height_unit = 2;

// ptp: point to point; if set, then it starts/ends on a grid

export function getTopPoint(qi, ptp) {
  if (ptp)
    return `${height_unit * qi + 1}rem`;
  else
    return `${height_unit * qi + 0.2}rem`;
}
export function getHeight(qi0, qi1, ptp) {
  if (ptp)
    return `${height_unit * (qi1 - qi0 + 1) - 2}rem`;
  else
    return `${height_unit * (qi1 - qi0 + 1) - 0.4}rem`;
}
export function getBottomPoint(qi, ptp) {
  if (ptp)
    return `${height_unit * (qi + 1) - 1}rem`;
  else
    return `${height_unit * (qi + 1) - 0.2}rem`;
}


export const gate_widths = {
  iswap: 70,
  barrier: 8,
  measure: 32,
  s: 24,
  h: 24,
  cx: 24
}

export function deepcopy(o) {
  JSON.parse(JSON.stringify(o));
}