<script>
  export let connect = [],
    step = {},
    n_qubits,
    dblclick = () => {};
  import { getTopPoint, getHeight } from "./util";
</script>

<div
  class="measure-gate"
  style={`top: ${getTopPoint(step.qubits[0], true)}; height: ${getHeight(step.qubits[0], n_qubits, true)};`}
  on:dblclick={dblclick}
>
  <div class="measure-qubit-marker">M</div>
  <div class="measure-line"></div>
  <div class="measure-cbit-marker">
    {step.classical_bits[0]}
  </div>
</div>

<style>
  * {
    box-sizing: border-box;
    line-height: 100%;
  }
  .measure-gate {
    position: absolute;
    width: 1.5rem;
    /* background-color: #ddd; */
    left: 0.5rem;
  }
  .measure-qubit-marker {
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
  .measure-line {
    position: absolute;
    top: 0;
    left: calc(50% - 2px);
    width: 4px;
    height: calc(100% - 1px);
    background-color: white;
    border-left: 1px solid black;
    border-right: 1px solid black;
    z-index: 5;
  }
  .measure-cbit-marker {
    position: absolute;
    font-size: 0.7rem;
    bottom: -0.25rem;
    width: 1.5rem;
    transform: translateY(100%);
    text-align: center;
  }
</style>
