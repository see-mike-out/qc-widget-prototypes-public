<script>
  import { onMount } from "svelte";
  import { planMachineView } from "./svg_utils/plan_draw_machine";
  import SvgWrap from "./svgs/SVGWrap.svelte";
  import { writable } from "svelte/store";
  import MachineViewProgress from "./MachineViewProgress.svelte";
  import LayerTimeMarker from "./LayerTimeMarker.svelte";
  import { scaleSequential, interpolateRdYlGn } from "d3";
  import {
    addGradientDef,
    getGradient,
    removeGradientDef,
  } from "./svg_utils/util";
  export let data,
    id,
    original_circuit_id,
    transpiled_circuit_id,
    match,
    operation_data,
    machine_moment_at = writable(0),
    open_tool = () => {};
  let browser = true;
  let drawPlan;
  let curr_layer = writable(null),
    anim_curr_layer = writable(0);
  let autoplay = writable(false),
    keep_timescale = writable(false),
    is_playing = false;
  let total_duration = 10;

  let nodeColorScale = scaleSequential(interpolateRdYlGn);

  curr_layer.subscribe((i) => {
    dehighlight_edge_gate();
    if (i >= 0 && i <= drawPlan?.operations?.length - 1) highlight_edge_gate(i);
    change_node_esp(i);
  });

  anim_curr_layer.subscribe((i) => {
    dehighlight_edge_gate();
    if (i >= 0 && i <= drawPlan?.operations?.length - 1) highlight_edge_gate(i);
    change_node_esp(i);
  });

  $: {
    if (drawPlan && drawPlan.operations) {
      curr_layer.set(0);
    }
  }

  $: {
    if (data) {
      drawPlan = planMachineView(data, operation_data, {
        id,
        original_circuit_id,
        transpiled_circuit_id,
        match,
        nodeColorScale,
      });
      total_duration = drawPlan.operations
        ?.map((e) => e.duration)
        .reduce((a, c) => a + c, 0);
      change_node_esp(0);
    }
  }

  let gradientDefs = [];

  onMount(() => {
    if (data) {
      drawPlan = planMachineView(data, operation_data, {
        id,
        original_circuit_id,
        transpiled_circuit_id,
        match,
        nodeColorScale,
      });
      total_duration = drawPlan.operations
        ?.map((e) => e.duration)
        .reduce((a, c) => a + c, 0);
      change_node_esp(0);
    }
  });

  let time_factors = [
    1000 / 50,
    1000 / 100,
    1000 / 150,
    1000 / 200,
    1000 / 250,
    1000 / 300,
    1000 / 350,
    1000 / 400,
  ];
  let time_factor = writable(3);

  function slower_animation() {
    time_factor.update((f) => {
      return Math.max(f - 1, 0);
    });
  }

  function faster_animation() {
    time_factor.update((f) => {
      return Math.min(f + 1, time_factors.length - 1);
    });
  }

  function pause(ms) {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  }

  async function animate() {
    is_playing = true;
    anim_curr_layer.set(0);
    for (const layer of drawPlan.operations) {
      if (!is_playing) {
        autoplay.set(false);
        curr_layer.set($anim_curr_layer);
        return;
      }
      // update
      let time =
        time_factors[$time_factor] * ($keep_timescale ? layer.duration : 100);
      if (time > 0) await pause(time);
      // todo: dehighlight (edges, gates)
      if (!is_playing) {
        autoplay.set(false);
        curr_layer.set($anim_curr_layer);
        return;
      }
      anim_curr_layer.update((i) => i + 1);
    }
    autoplay.set(false);
    curr_layer.set(0);
    return;
  }

  function highlight_edge_gate(i) {
    // (edges, gates)
    removeGradientDef(transpiled_circuit_id, gradientDefs);
    gradientDefs = [];
    let layer = drawPlan?.operations?.[i];
    let match_color = [],
      original_layers = [];
    if (layer?.elem) {
      let op_groups = layer.elem.filter(
        (d) => d.role === "op-layer-operation-group",
      );
      if (op_groups) {
        op_groups.forEach((op_group) => {
          let edge_ids = op_group.data.edge_ids;
          edge_ids.forEach((ei) => {
            let el = document.querySelector(
              `#${id} #${ei}--group .highlight-wrap`,
            );
            if (el) {
              el.classList.add("edge-highlighted");
              el.style.fill = op_group.data.match_color;
              el.style.fillOpacity = `0.4`;
            }
          });
          let oid = op_group.data.operation;
          let top_elem = document.querySelector(
            `#${transpiled_circuit_id} .gate-wrap.layer-${i}.gate-${oid}.transpiled`,
          );
          if (top_elem) {
            top_elem.classList.add("op-highlighted");
            top_elem.style.outline = `2px solid ${op_group.data.match_color}`;
          }
          let olid = op_group.data.original_layer;
          original_layers.push(olid);
          let ooid = op_group.data.original_operation;
          let oop_elem = document.querySelector(
            `#${original_circuit_id} .gate-wrap.layer-${olid}.gate-${ooid}.original`,
          );
          if (oop_elem) {
            oop_elem.classList.add("op-highlighted");
            oop_elem.style.outline = `2px solid ${op_group.data.match_color}`;
          }
          match_color.push(op_group.data.match_color);
        });
      }
      let lwrap = document.querySelector(
        `#${transpiled_circuit_id} #layer-${i}--interaction-wrap`,
      );
      if (lwrap) {
        let grad_data = getGradient(match_color);
        let grad_value = grad_data ? `tg-l-${i}` : null;
        if (grad_value) {
          addGradientDef(transpiled_circuit_id, {
            id: grad_value,
            grad_data,
          });
          gradientDefs.push(grad_value);
        }
        lwrap.classList.add("layer-highlighted");
        lwrap.style.fill = grad_value
          ? `url(#${grad_value})`
          : match_color[0] || "#000000";
        lwrap.style.fillOpacity = `0.2`;
      }
      original_layers.forEach((olid, k) => {
        let olwrap = document.querySelector(
          `#${original_circuit_id} #layer-${olid}--interaction-wrap`,
        );
        if (olwrap) {
          olwrap.classList.add("layer-highlighted");
          olwrap.style.fill = match_color[k];
          olwrap.style.fillOpacity = `0.2`;
        }
      });
    }
  }
  function dehighlight_edge_gate() {
    // (edges, gates)
    let ehls = Array.from(
      browser ? document.querySelectorAll(".edge-highlighted") : [],
    );
    ehls?.forEach((el) => {
      el.classList.remove("edge-highlighted");
      el.style.fill = "#ffffff";
      el.style.fillOpacity = 0;
    });
    let lhls = Array.from(
      browser ? document.querySelectorAll(".layer-highlighted") : [],
    );
    lhls?.forEach((el) => {
      el.classList.remove("layer-highlighted");
      el.style.fillOpacity = 0;
    });
    let ohls = Array.from(
      browser ? document.querySelectorAll(".op-highlighted") : [],
    );
    ohls?.forEach((el) => {
      el.classList.remove("op-highlighted");
      el.style.outline = null;
    });
  }
  function change_node_esp(li) {
    let point = drawPlan?.operations[li].elem?.filter(
      (d) => d.role === "op-layer-operation-group",
    )?.[0];
    if (point) {
      data?.design?.nodes?.forEach((node, ni) => {
        machine_moment_at.set(li);
        let value =
          (point.data?.esp_qubit_wise?.[node.index] - operation_data.esp) /
          (1 - operation_data.esp);
        let el = document.querySelector(`#qubit-node-${node.index}--node`);
        if (el) el.setAttribute("fill", nodeColorScale(value));
      });
    }
  }

  function quit_animate() {
    is_playing = false;
  }

  autoplay.subscribe((a) => {
    if (a) {
      animate();
    } else {
      quit_animate();
    }
  });
</script>

{#if data && drawPlan}
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
    {#if drawPlan.groups.machine}
      <SvgWrap data={drawPlan.groups.machine} {open_tool}></SvgWrap>
    {/if}
    {#if drawPlan.operations && !$autoplay}
      <SvgWrap data={drawPlan.operations[$curr_layer]} {open_tool}></SvgWrap>
    {:else if drawPlan.operations && $autoplay}
      <SvgWrap data={drawPlan.operations[$anim_curr_layer]} {open_tool}
      ></SvgWrap>
    {/if}
  </svg>

  {#if drawPlan.operations}
    {#if $keep_timescale && $autoplay}
      <div class="button-wrap">
        <LayerTimeMarker
          duration={drawPlan.operations?.[
            $autoplay ? $anim_curr_layer : $curr_layer
          ]?.duration}
        ></LayerTimeMarker>
      </div>
    {/if}
    <div class="button-wrap">
      <MachineViewProgress
        total={drawPlan.operations.length}
        curr={$autoplay ? $anim_curr_layer : $curr_layer}
      ></MachineViewProgress>
    </div>
    <div class="button-wrap">
      <button
        disabled={$curr_layer == 0 || $autoplay}
        on:click={() => {
          curr_layer.update((i) => {
            return 0;
          });
        }}>To first</button
      >
      <button
        disabled={$curr_layer == 0 || $autoplay}
        on:click={() => {
          curr_layer.update((i) => {
            return i - 1;
          });
        }}>&leftarrow; Prev</button
      >
      <button
        on:click={() => {
          curr_layer.update((i) => {
            return i + 1;
          });
        }}
        disabled={$curr_layer == drawPlan.operations.length - 1 || $autoplay}
        >Next &rightarrow;</button
      >
      <button
        disabled={$curr_layer == drawPlan.operations.length - 1 || $autoplay}
        on:click={() => {
          curr_layer.update((i) => {
            return drawPlan.operations.length - 1;
          });
        }}>To last</button
      >
    </div>
    <div class="button-wrap">
      <button
        on:click={() => {
          autoplay.set(true);
        }}
        disabled={$autoplay}>Autoplay</button
      >
      <button
        on:click={() => {
          autoplay.set(false);
        }}
        disabled={!$autoplay}>Stop</button
      >
      <button
        on:click={() => {
          slower_animation();
        }}
        disabled={$time_factor == 0}>Slower</button
      >
      <button
        on:click={() => {
          faster_animation();
        }}
        disabled={$time_factor == time_factors.length - 1}>Faster</button
      >
      <br />
      <div style="margin-top: 0.25rem;">
        <input
          type="checkbox"
          name="match-time-scale"
          on:change={(e) => {
            keep_timescale.set(e.target.checked);
          }}
        />
        <label for="match-time-scale" style="font-family: iosevka"
          >Keep times</label
        >
        <span style="font-family: iosevka; padding-left: 1rem;">
          Speed: {5 / time_factors[$time_factor]}x
        </span>
      </div>
    </div>
  {/if}
  <span class="note">
    To support how each qubit contributes to the overall success, each qubit
    node shows its own ESP (estimated success probability) as the product of ESP
    values of the operations that have been applied to the qubit so far (i.e.,
    up to the current moment). Thus, the term may be different then the overall
    ESP value which is the product of the ESP values of all the operations in
    the circut. The overall ESP value change is shown in the transpiled circuit
    view.
  </span>
{/if}

<style>
  .button-wrap {
    margin: 1rem 0;
  }
  .button-wrap button {
    font-family: iosevka;
    padding: 0.5rem 1rem;
    appearance: none;
    line-height: 100%;
    border: 1px solid #aaa;
    background-color: white;
    border-radius: 0.25rem;
  }
  .button-wrap button:hover {
    background-color: #f0f0f0;
  }
  .note {
    color: #787878;
    font-size: 0.9rem;
  }
</style>
