<script>
  import { onMount } from "svelte";
  import { planDrawing } from "./svg_utils/plan_draw";
  import SvgWrap from "./svgs/SVGWrap.svelte";
  export let circuit_data,
    is_original = true,
    match,
    id,
    matched_circuit_id,
    matched_machine_id,
    open_tool = () => {};

  let drawPlan;
  onMount(() => {
    drawPlan = planDrawing(circuit_data, {
      show_moments: true,
      is_original,
      match,
      matched_circuit_id,
      this_circuit_id: id,
      matched_machine_id,
    });
  });

  $: {
    drawPlan = planDrawing(circuit_data, {
      show_moments: true,
      is_original,
      match,
      matched_circuit_id,
      this_circuit_id: id,
      matched_machine_id,
    });
    console.log(drawPlan);
  }
</script>

{#if drawPlan}
  <svg
    {id}
    width={drawPlan.width}
    height={drawPlan.height}
    viewBox={drawPlan.viewBox.join(" ")}
  >
    {#if drawPlan.groups.phase_marker}
      <SvgWrap data={drawPlan.groups.phase_marker}></SvgWrap>
    {/if}
    {#if drawPlan.groups.moment_group}
      <SvgWrap data={drawPlan.groups.moment_group} {open_tool}></SvgWrap>
    {/if}
    {#if drawPlan.groups.qubit_group}
      <SvgWrap data={drawPlan.groups.qubit_group} {open_tool}></SvgWrap>
    {/if}
    {#if drawPlan.groups.circuit_line_group}
      <SvgWrap data={drawPlan.groups.circuit_line_group} {open_tool}></SvgWrap>
    {/if}
    {#if drawPlan.groups.circuit_group}
      <SvgWrap data={drawPlan.groups.circuit_group} {open_tool}></SvgWrap>
    {/if}
  </svg>
{/if}

<style>
  svg {
    font-family: Iosevka;
    font-size: 14px;
  }
</style>
