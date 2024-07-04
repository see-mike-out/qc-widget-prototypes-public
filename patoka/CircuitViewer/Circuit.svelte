<script>
  import { onMount } from "svelte";
  import { planDrawing } from "./svg_utils/plan_draw";
  import SvgWrap from "./svgs/SVGWrap.svelte";
  import { writable } from "svelte/store";
  export let circuit_data,
    is_original = true,
    match,
    id,
    matched_circuit_id,
    matched_machine_id,
    machine_moment_at = writable(),
    open_tool = () => {};

  let showTooltip = false,
    tooltip_x,
    tooltip_y,
    tootlip_content,
    curr_scroll_x_pos = 0;

  function openTooltip(e, cont) {
    showTooltip = true;
    tooltip_x = e.clientX + 5;
    tooltip_y = e.clientY + 5;
    tootlip_content = cont;
  }
  function moveTooltip(e) {
    if (showTooltip) {
      tooltip_x = e.clientX + 5;
      tooltip_y = e.clientY + 5;
    }
  }
  function closeTooltip() {
    showTooltip = false;
  }

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
    machine_moment_at.subscribe((li) => {
      let g = document.querySelector(`#${id} #layer-${li}--group`);
      if (g) g.scrollIntoView({ behavior: "smooth" });
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
  }
</script>

{#if drawPlan}
  <div
    id={id + "-wrapper"}
    style="position: relative; width: 100%; overflow-x: scroll; overflow-y:hidden;"
  >
    <!-- todo: sticky -->
    <div
      class="circuit-sticky"
      style={`width: ${drawPlan.groups.qubit_group.x + drawPlan.groups.qubit_group.width}px; height:${drawPlan.height}px;`}
    >
      <svg
        id={id + "-sticky"}
        width={drawPlan.groups.qubit_group.x +
          drawPlan.groups.qubit_group.width}
        height={drawPlan.height}
        viewBox={drawPlan.viewBox
          .map((d, i) =>
            i == 2
              ? drawPlan.groups.qubit_group.x +
                drawPlan.groups.qubit_group.width
              : d,
          )
          .join(" ")}
      >
        <style>
          g {
            font-family: Iosevka;
            font-size: 14px;
          }
        </style>
        {#if drawPlan.groups.phase_marker}
          <SvgWrap
            data={drawPlan.groups.phase_marker}
            {openTooltip}
            {closeTooltip}
            {moveTooltip}
          ></SvgWrap>
        {/if}
        {#if drawPlan.groups.qubit_group}
          <SvgWrap
            data={drawPlan.groups.qubit_group}
            {open_tool}
            {openTooltip}
            {closeTooltip}
            {moveTooltip}
          ></SvgWrap>
        {/if}
        {#if drawPlan.groups.esp_axis_group}
          <SvgWrap
            data={drawPlan.groups.esp_axis_group}
            {open_tool}
            {openTooltip}
            {closeTooltip}
            {moveTooltip}
          ></SvgWrap>
        {/if}
      </svg>
    </div>
    <div class="circuit-main">
      <svg
        {id}
        width={drawPlan.width}
        height={drawPlan.height}
        viewBox={drawPlan.viewBox.join(" ")}
      >
        <style>
          g {
            font-family: Iosevka;
            font-size: 14px;
          }
        </style>
        {#if drawPlan.groups.phase_marker}
          <SvgWrap
            data={drawPlan.groups.phase_marker}
            {openTooltip}
            {closeTooltip}
            {moveTooltip}
          ></SvgWrap>
        {/if}
        {#if drawPlan.groups.moment_group}
          <SvgWrap
            data={drawPlan.groups.moment_group}
            {open_tool}
            {openTooltip}
            {closeTooltip}
            {moveTooltip}
          ></SvgWrap>
        {/if}
        {#if drawPlan.groups.qubit_group}
          <SvgWrap
            data={drawPlan.groups.qubit_group}
            {open_tool}
            {openTooltip}
            {closeTooltip}
            {moveTooltip}
          ></SvgWrap>
        {/if}
        {#if drawPlan.groups.circuit_line_group}
          <SvgWrap
            data={drawPlan.groups.circuit_line_group}
            {open_tool}
            {openTooltip}
            {closeTooltip}
            {moveTooltip}
          ></SvgWrap>
        {/if}
        {#if drawPlan.groups.circuit_group}
          <SvgWrap
            data={drawPlan.groups.circuit_group}
            {open_tool}
            {openTooltip}
            {closeTooltip}
            {moveTooltip}
          ></SvgWrap>
        {/if}
        {#if drawPlan.groups.esp_axis_group}
          <SvgWrap
            data={drawPlan.groups.esp_axis_group}
            {open_tool}
            {openTooltip}
            {closeTooltip}
            {moveTooltip}
          ></SvgWrap>
        {/if}
        {#if drawPlan.groups.esp_group}
          <SvgWrap
            data={drawPlan.groups.esp_group}
            {open_tool}
            {openTooltip}
            {closeTooltip}
            {moveTooltip}
          ></SvgWrap>
        {/if}
      </svg>
    </div>
  </div>
{/if}

{#if showTooltip}
  <div class="g-tooltip" style={`top: ${tooltip_y}px; left: ${tooltip_x}px;`}>
    {@html tootlip_content}
  </div>
{/if}

<style>
  .g-tooltip {
    position: fixed;
    padding: 0.5rem;
    background-color: #ffffff;
    border: 1px solid #000;
    font-family: iosevka;
    line-height: 100%;
    font-size: 0.9rem;
  }
  :global(.g-tooltip .item) {
    display: block;
  }
  .circuit-sticky {
    position: sticky;
    top: 0;
    left: 0;
    z-index: 9;
    background-color: #ffffff;
  }
  .circuit-main {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 0;
  }
</style>
