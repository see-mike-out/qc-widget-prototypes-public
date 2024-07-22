import { markers } from "./meta_info";

export function makeCode(basket_data) {
  let code = `def get_data(backend):`;
  code += "\n"
  let dict_keys = [];
  for (const line of basket_data) {
    if (line.includes(" = ")) {
      code += `    ${line}`;
      dict_keys.push(line.split(" = ")[0]);
    } else {
      code += `    ${line} = ${markers[line]}`;
      dict_keys.push(line);
    }
    code += "\n"
  }
  code += "\n    output = {\n"
  for (const key of dict_keys) {
    code += `        "${key}": ${key},`
    code += "\n"
  }
  code += "    }\n"
  code += "    return output"
  return code
}

export function decideBlackWhite(hexCode) {
  let colorCode = hexCode.replace("#", "");
  let rgb = [colorCode.slice(0, 2), colorCode.slice(2, 4), colorCode.slice(4, 6)].map((d) => parseInt(d, 16));
  if ((rgb[0] * 0.299 + rgb[1] * 0.587 + rgb[2] * 0.114) > 186) return "#000000"; else return "#ffffff";
}