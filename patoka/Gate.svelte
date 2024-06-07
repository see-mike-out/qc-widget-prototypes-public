<script>
  import { onMount } from "svelte";
  import Iswap from "./Gates/ISWAP.svelte";
  import Barrier from "./Gates/Barrier.svelte";
  import Measure from "./Gates/Measure.svelte";
  import { gate_widths } from "./Gates/util";
  import H from "./Gates/H.svelte";
  import S from "./Gates/S.svelte";
  import Cx from "./Gates/CX.svelte";

  export let step = {},
    original_step = {},
    n_qubits,
    circuit = {},
    moment = [],
    step_index,
    original_step_index,
    open_tool = () => {},
    is_substep;
  let gate_type, connect;
  let gate_id;
  let subgate_index_test = (q) =>
    typeof q === "string" && q.startsWith("_gate_q");
  onMount(() => {
    gate_type = step.gate_class || step.gate;
    gate_id = "gate-step-" + step.order;
    if (step.qubits.length > 1) {
      connect = [Math.min(...step.qubits), Math.max(...step.qubits)];
    } else {
      connect = false;
    }
    if (is_substep) {
      let bit_dict = {};
      for (let q of step.qubits) {
        if (subgate_index_test(q))
          bit_dict[q] = original_step.qubits[parseInt(q.replace("_gate_q_", ""))];
      }
      step.qubits = step.qubits?.map((d, i) =>
        subgate_index_test(d) ? bit_dict[d] : d,
      );
      step.control = step.control?.map((d, i) =>
        subgate_index_test(d) ? bit_dict[d] : d,
      );
      step.target = step.target?.map((d, i) =>
        subgate_index_test(d) ? bit_dict[d] : d,
      );
      console.log(bit_dict)
    }
  });
</script>

<div class="gate-wrap" style={`width: ${gate_widths[gate_type]}px`}>
  <div class="gate" id={gate_id} style={`width: ${gate_widths[gate_type]}px`}>
    {#if gate_type === "iswap"}
      <Iswap
        {connect}
        {step}
        dblclick={() =>
          open_tool(
            circuit,
            moment,
            step,
            step_index,
            original_step,
            original_step_index,
          )}
      ></Iswap>
    {:else if gate_type === "h"}
      <H
        {connect}
        {step}
        dblclick={() =>
          open_tool(
            circuit,
            moment,
            step,
            step_index,
            original_step,
            original_step_index,
          )}
      ></H>
    {:else if gate_type === "s"}
      <S
        {connect}
        {step}
        dblclick={() =>
          open_tool(
            circuit,
            moment,
            step,
            step_index,
            original_step,
            original_step_index,
          )}
      ></S>
    {:else if gate_type === "cx"}
      <Cx
        {connect}
        {step}
        dblclick={() =>
          open_tool(
            circuit,
            moment,
            step,
            step_index,
            original_step,
            original_step_index,
          )}
      ></Cx>
    {:else if gate_type === "barrier"}
      <Barrier
        {connect}
        {step}
        dblclick={() =>
          open_tool(
            circuit,
            moment,
            step,
            step_index,
            original_step,
            original_step_index,
          )}
      ></Barrier>
    {:else if gate_type === "measure"}
      <Measure
        {step}
        {n_qubits}
        dblclick={() =>
          open_tool(
            circuit,
            moment,
            step,
            step_index,
            original_step,
            original_step_index,
          )}
      ></Measure>
    {:else}
      <div>{step.gate}</div>
    {/if}
  </div>
</div>

<!-- connection -->

<style>
  * {
    box-sizing: border-box;
    line-height: 100%;
  }
  .gate-wrap {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  .gate {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    z-index: 3;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    font-size: 0.85rem;
  }
  :global(.gate *) {
    user-select: none;
  }
  .connect {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2;
  }
</style>
