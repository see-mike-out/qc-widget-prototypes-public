<script>
  export let connect = [],
    step = {},
    dblclick = () => {},
    n_qubits;
  import { getTopPoint, getHeight } from "./util";
</script>

<div
  class="s-gate"
  style={`top: ${getTopPoint(step.qubits[0], true)};`}
  on:dblclick={dblclick}
>
  <div class="s-qubit-marker">S</div>
</div>

<style>
  * {
    box-sizing: border-box;
    line-height: 100%;
  }
  .s-gate {
    position: absolute;
    width: 1.5rem;
    /* background-color: #ddd; */
    left: 0.5rem;
  }
  .s-qubit-marker {
    position: absolute;
    top: 0;
    transform: translateY(-50%);
    width: 1.5rem;
    height: 1.6rem;
    line-height: 140%;
    text-align: center;
    padding: 0.2rem;
    background-color: white;
    border: 1px solid black;
    font-weight: 600;
    z-index: 6;
  }
</style>
