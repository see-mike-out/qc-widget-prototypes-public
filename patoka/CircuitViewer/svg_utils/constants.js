export const circuit_line_height = 32;
export const circuit_v_gap = 6;
export const circuit_h_gap = 10;
export const qubit_ref_width = 50;
export const bitHeight = 32;
export const padding = 5;
export const moment_bar_height = 16;

export const qubit_node_wh = 48;
export const qubit_node_gap = 24;

export const defualt_color = "#000000";
export const default_fill = "#ffffff"

export const ord_colors = [
  "#4285f4",
  "#db4437",
  "#f4b400",
  "#0f9d58",
  "#ab47bc",
  "#00acc1",
  "#ff7043",
  "#9e9d24",
  "#5c6bc0",
  "#f06292",
  "#00796b",
  "#c2185b",
  "#7e57c2",
  "#03a9f4",
  "#8bc34a",
  "#fdd835",
  "#fb8c00",
  "#8d6e63",
  "#9e9e9e",
  "#607d8b"
]


export const control_gates_type_0 = [
  // no-target
  "cp"
];

export const control_gates_type_1 = [
  // single-target
  "mcx", "cccx", "c3x", "ccccx", "c4x", "ccx", "c2x",
  "ch", "cs", "csdg", "csx", "cx", "cy", "cz", "ccz",
  "crx", "cry", "crz", "cu", "cu1", "cu3",
  "rccx", "rcccx"
];

export const control_gates_type_2 = [
  // double-target
  "cswap"
];

export const parameter_gates = [
  "crx", "cry", "crz", "cu", "cu1", "cu3",
  "rzz", "cp", "rxx", "ryy", "rzx", "xx_minus_yy", "xx_plus_yy",
  "p", "r", "rx", "ry", "rz", "u", "u1", "u2", "u3"
];

export const swap_gates = [
  "cswap",
  "iswap",
  "swap"
];