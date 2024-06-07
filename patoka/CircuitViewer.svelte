<script>
  import { onDestroy, onMount } from "svelte";
  import { parseQASM } from "./qasmParser.js";
  import Moment from "./Moment.svelte";
  import { writable } from "svelte/store";
  export let model;
  export let key_circ = "circ";
  let circ = model.get(key_circ);
  let parsed_circ = parseQASM(circ);
  let event = `change:${key_circ}`;
  let callback = () => (count = model.get(key_circ));
  let moments = [];
  onMount(() => {
    moments = parsed_circ.moments.map((m) => writable(m));
    model.on(event, callback);
  });
  onDestroy(() => {
    model.off(event, callback);
  });
  let show_tools, curr_circuit, curr_moment, curr_step;
  function open_tool(circuit, moment, step, step_index) {
    show_tools = true;
    curr_circuit = circuit;
    curr_moment = moment;
    curr_step = step_index;
  }
</script>

<section class="circuit-view-wrap">
  <div class="qubit-markers">
    {#each parsed_circ.qubits as qubit, qi}
      <div class="row qubit-marker"><span> {qubit} </span></div>
    {/each}
    {#if parsed_circ.n_bits}
      <div class="row qubit-marker"><span> C/{parsed_circ.n_bits} </span></div>
    {/if}
  </div>
  {#each moments as n, i}
    <div class="moment">
      <Moment moment={moments[i]} circuit={parsed_circ} {open_tool}></Moment>
    </div>
  {/each}
</section>
{#if show_tools}
  <section class="tools">
    {#if $curr_moment[curr_step]?.gate_class || $curr_moment[curr_step]?.gate}
      <h3>
        {$curr_moment[curr_step].gate_class || $curr_moment[curr_step].gate} Gate
      </h3>
    {/if}
    {#if $curr_moment[curr_step]?.is_custom}
      <div>
        {#if !$curr_moment[curr_step].show_extended}
          <button
            on:click={() => {
              curr_moment.update((m) => {
                m[curr_step].show_extended = true;
                return m;
              });
            }}>Show the underlying gates</button
          >
        {:else}
          <button
            on:click={() => {
              curr_moment.update((m) => {
                m[curr_step].show_extended = false;
                return m;
              });
            }}>Hide the underlying gates</button
          >
        {/if}
      </div>
    {/if}
  </section>
{/if}

<span>
  <pre>
{JSON.stringify(parsed_circ, null, 2)}
</pre>
</span>

<style>
  * {
    box-sizing: border-box;
    font-family: sans-serif;
    line-height: 100%;
  }
  .circuit-view-wrap {
    width: 100%;
    overflow-x: scroll;
    display: flex;
  }
  .qubit-markers {
    position: sticky;
    left: 0;
    width: 2rem;
  }
  .row {
    height: 2rem;
  }
  .qubit-marker {
    position: relative;
    width: 2rem;
    text-align: center;
  }
  .qubit-marker span {
    display: block;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
  .tools {
    min-width: 300px;
    font-size: 0.85rem;
    margin-top: 1rem;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    background-color: white;
    box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.05);
  }
  h3 {
    margin: 0 0 0.5rem 0;
    line-height: 100%;
    font-size: 1rem;
  }
  .tools button {
    appearance: none;
    border: 1px solid #ddd;
    border-radius: 0.25rem;
    background-color: white;
    line-height: 100%;
    padding: 0.5rem;
  }
  .tools button:hover {
    background-color: #f0f0f0;
  }
</style>
