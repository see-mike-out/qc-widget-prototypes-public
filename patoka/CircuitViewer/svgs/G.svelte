<script>
  import SvgWrap from "./SVGWrap.svelte";
  export let data = {},
    open_tool = () => {};
  function getQubitMatchEls(data) {
    let el1, el2, el3;
    if (data._class.includes(" original")) {
      el1 = document.querySelector(
        `#${data.data.this_circuit_id} .qubit-background.qubit-${data.data.bit_match.from}`,
      );
      el2 = document.querySelector(
        `#${data.data.matched_circuit_id} .qubit-background.qubit-${data.data.bit_match.to}`,
      );
      el3 = document.querySelector(
        `#${data.data.matched_machine_id} #qubit-node-${data.data.bit_match.to}--group`,
      );
    } else if (data._class.includes(" transpiled")) {
      el1 = document.querySelector(
        `#${data.data.matched_circuit_id} .qubit-background.qubit-${data.data.bit_match.from}`,
      );
      el2 = document.querySelector(
        `#${data.data.this_circuit_id} .qubit-background.qubit-${data.data.bit_match.to}`,
      );
      el3 = document.querySelector(
        `#${data.data.matched_machine_id} #qubit-node-${data.data.bit_match.to}--group`,
      );
    } else if (data._class.includes("qubit-node--group")) {
      el1 = document.querySelector(
        `#${data.data.original_circuit_id} .qubit-background.qubit-${data.data.original_qubit_id}`,
      );
      el2 = document.querySelector(
        `#${data.data.transpiled_circuit_id} .qubit-background.qubit-${data.data.qubit_id}`,
      );
      el3 = document.querySelector(
        `#${data.data.id} #qubit-node-${data.data.qubit_id}--group`,
      );
    }
    return [el1, el2, el3];
  }

  function getOpMatchEls(data) {
    let els = [],
      tel = [];
    if (data._class.includes(" original")) {
      els = data.data.layer_match.matches.map((d) => {
        return document.querySelector(
          `#${data.data.matched_circuit_id} #layer-${d[0]}--interaction-wrap`,
        );
      });
      els.push(
        document.querySelector(
          `#${data.data.this_circuit_id} #layer-${data.data.layer_match.layer}--interaction-wrap`,
        ),
      );
      tel = data.data.layer_match.matches.map((d) => {
        return document.querySelector(
          `#${data.data.matched_circuit_id} .gate-wrap.layer-${d[0]}.gate-${d[1]}`,
        );
      });
      tel.push(
        document.querySelector(
          `#${data.data.this_circuit_id} .gate-wrap.layer-${data.data.layer_index}.gate-${data.data.operation_index}`,
        ),
      );
    } else if (data._class.includes(" transpiled")) {
      els = data.data.layer_match.colleagues.map((d) => {
        return document.querySelector(
          `#${data.data.this_circuit_id} #layer-${d[0]}--interaction-wrap`,
        );
      });
      els.push(
        document.querySelector(
          `#${data.data.matched_circuit_id} #layer-${data.data.layer_match.layer}--interaction-wrap`,
        ),
      );
      tel = data.data.layer_match.colleagues.map((d) => {
        return document.querySelector(
          `#${data.data.this_circuit_id} .gate-wrap.layer-${d[0]}.gate-${d[1]}`,
        );
      });
      tel.push(
        document.querySelector(
          `#${data.data.matched_circuit_id} .gate-wrap.layer-${data.data.layer_match.layer}.gate-${data.data.layer_match.operation}`,
        ),
      );
    }
    return [els, tel];
  }
</script>

{#if data}
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <!-- svelte-ignore a11y-mouse-events-have-key-events -->
  <g
    id={data.id}
    class={data._class}
    data-role={data.role}
    height={data.height}
    width={data.width}
    transform={`translate(${data.x} ${data.y})`}
    on:mouseover={(e) => {
      if (data.role === "qubit-group" || data.role === "qubit-node--group") {
        let [el1, el2, el3] = getQubitMatchEls(data);
        if (el1) {
          el1.style.fill = data.data.match_color;
        }
        if (el2) {
          el2.style.fill = data.data.match_color;
        }
        if (el3) {
          el3.style.outline = `2px solid  ${data.data.match_color}`;
        }
      } else if (data.role === "gate-group") {
        let [els, tel] = getOpMatchEls(data);
        if (els) {
          els.forEach((el) => {
            if (el) {
              el.style.fill = data.data.match_color;
              el.style.fillOpacity = 0.2;
            }
          });
        }
        if (tel) {
          tel.forEach((el) => {
            el.style.outline = `2px solid  ${data.data.match_color}`;
          });
        }
      }
    }}
    on:mouseout={(e) => {
      if (data.role === "qubit-group"|| data.role === "qubit-node--group") {
        let [el1, el2, el3] = getQubitMatchEls(data);
        if (el1) {
          el1.style.fill = "transparent";
        }
        if (el2) {
          el2.style.fill = "transparent";
        }
        if (el3) {
          el3.style.outline = null;
        }
      } else if (data.role === "gate-group") {
        let [els, tel] = getOpMatchEls(data);
        if (els) {
          els.forEach((el) => {
            if (el) el.style.fill = "transparent";
          });
        }
        if (tel) {
          tel.forEach((el) => {
            el.style.outline = null;
          });
        }
      }
    }}
  >
    {#each data.elem as el}
      <SvgWrap data={el} {open_tool}></SvgWrap>
    {/each}
  </g>
{/if}
