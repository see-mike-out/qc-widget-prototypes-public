<script>
  import { decideBlackWhite } from "./util";
  export let qubit,
    qubit_node,
    qubit_gap = 35,
    edge_width = 15,
    padding = 20,
    qubit_radius = 25,
    qubit_info_value,
    info_type,
    colorScale = () => {},
    openTooltip = () => {},
    hideTooltip = () => {},
    moveTooltip = () => {},
    qubit_info_selected;
</script>

{#if qubit !== undefined && qubit_node}
  <node
    id={"qubit-" + qubit}
    class="circuit-element"
    style={`top: ${padding * 2 + qubit_node.y * qubit_gap - qubit_radius / 2}px; 
    left: ${padding * 2 + qubit_node.x * qubit_gap - qubit_radius / 2}px;
    width: ${qubit_radius}px;
    height: ${qubit_radius}px;
    border-radius: ${qubit_radius / 2}px;
    font-size: ${qubit_radius * 0.55}px;
    padding-top: ${qubit_radius * 0.225}px;
    background-color: ${colorScale(qubit_info_value.value)};
    color: ${decideBlackWhite(colorScale(qubit_info_value.value))}`}
    on:mouseover={(e) => {
      openTooltip(
        e,
        "Qubit " + qubit,
        qubit_info_selected,
        qubit_info_value,
        "qubit-" + qubit,
        [qubit]
      );
    }}
    on:mousemove={(e) => {
      moveTooltip(e);
    }}
    on:mouseout={(e) => {
      hideTooltip();
    }}>{qubit}</node
  >
{/if}

<style>
  node {
    box-sizing: border-box;
    display: block;
    position: absolute;
    background-color: lightgray;
    font-family: iosevka;
    text-align: center;
    line-height: 100%;
    border: 1px solid white;
    user-select: none;
  }
</style>
