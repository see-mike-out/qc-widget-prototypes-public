<script>
  export let connect = [],
    step = {},
    dblclick = () => {},
    n_qubits;
  import { getTopPoint, getHeight } from "./util";
</script>

<div
  class="cx-gate"
  style={`top: ${getTopPoint(Math.min(...step.qubits), true)}; height: ${getHeight(Math.min(...step.qubits), Math.max(...step.qubits), true)};`}
  on:dblclick={dblclick}
>
  <div
    class="cx-target-marker"
    style={`top: ${getTopPoint(step.target[0], false)};`}
  >
    +
  </div>
  <div class="cx-line"></div>
  <div
    class="cx-control-marker"
    style={`top: ${getTopPoint(step.control[0]-1, true)};`}
  >
    -
  </div>
</div>

<style>
  * {
    box-sizing: border-box;
    line-height: 100%;
  }
  .cx-gate {
    position: absolute;
    width: 1.5rem;
    /* background-color: #ddd; */
    left: 0.5rem;
  }
  .cx-target-marker {
    position: absolute;
    /* top: 0; */
    transform: translateY(calc(-50% - 0.2rem));
    width: 1.5rem;
    height: 1.5rem;
    line-height: 50%;
    text-align: center;
    padding: 0rem;
    background-color: white;
    border: 1px solid black;
    font-size: 2rem;
    font-weight: 100;
    z-index: 6;
    border-radius: 0.75rem;
  }
  .cx-line {
    position: absolute;
    top: 0;
    left: calc(50% - 0.5px);
    width: 0;
    height: calc(100% - 1px);
    /* background-color: white; */
    border-left: 1px solid black;
    z-index: 5;
  }
  .cx-control-marker {
    position: absolute;
    left: 50%;
    font-size: 0.7rem;
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 0.15rem;
    background-color: black;
    transform: translate(-50%, 150%);
    text-align: center;
  }
</style>
