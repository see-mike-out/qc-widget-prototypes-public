<script>
  export let connect = [],
    step = {},
    dblclick = () => {};
  import { getTopPoint, getHeight } from "./util";
</script>

<div
  class="box-gate"
  style={`top: ${getTopPoint(connect[0])}; height: ${getHeight(connect[0], connect[1])};`}
  on:dblclick={dblclick}
>
  <span class="gate-qubit-marker" style={`top: 0.2rem;`}>
    {connect[0]}
  </span>
  <span class="gate-name">ISWAP</span>
  <span class="gate-qubit-marker" style={`bottom: 0.2rem;`}>
    {connect[1]}
  </span>
</div>

<style>
  * {
    box-sizing: border-box;
    line-height: 100%;
  }
  .box-gate {
    position: absolute;
    width: 70px;
    border: 1px solid black;
    background-color: white;
    padding: 0.25rem;
  }
  .box-gate .gate-qubit-marker {
    position: absolute;
    display: block;
    left: 0.2rem;
  }
  .box-gate .gate-name {
    position: relative;
    top: calc(50% - 0.425rem);
    padding-left: 0.75rem;
    padding-right: 0.25rem;
  }
</style>
