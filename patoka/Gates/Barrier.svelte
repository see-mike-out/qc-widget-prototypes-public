<script>
  export let connect = [],
    step = {},
    dblclick = () => {};
  import { getTopPoint, getHeight } from "./util";
</script>

<div
  class="barrier-gate"
  style={`top: ${getTopPoint(connect[0])}; height: ${getHeight(connect[0], connect[1])};`}
  on:dblclick={dblclick}
></div>

<style>
  * {
    box-sizing: border-box;
    line-height: 100%;
  }
  .barrier-gate {
    position: absolute;
    width: 0.5rem;
    background-color: #ddd;
    left: 0.5rem;
  }
</style>
