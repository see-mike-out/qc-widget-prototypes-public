<script>
  import { onDestroy, onMount } from "svelte";
  import { writable } from "svelte/store";
  import Circuit from "./Circuit.svelte";
  import Information from "./Information.svelte";
  import MachineView from "./MachineView.svelte";
  export let model;
  export let key_circ = "circ";
  let circ = model.get(key_circ);
  let parsed_circ = JSON.parse(circ);
  let event = `change:${key_circ}`;
  let callback = () => (circ = model.get(key_circ));
  let data = writable();

  let selected_info = writable();

  function open_tool(info) {
    console.log(info);
    selected_info.set(info);
  }

  onMount(() => {
    // console.log(parsed_circ);
    data.set(parsed_circ);
    model.on(event, callback);
  });

  onDestroy(() => {
    model.off(event, callback);
  });
</script>

<div class="frame">
  <div class="circuits">
    <section class="circuit-view-wrap">
      <h1>Original Circuit</h1>
      <div class="circuit">
        <Circuit
          id="original-circuit"
          circuit_data={$data?.original}
          is_original={true}
          match={$data?.match}
          matched_circuit_id="transpiled-circuit"
          matched_machine_id="on-machine"
          {open_tool}
        ></Circuit>
      </div>
    </section>

    <section class="circuit-view-wrap">
      <h1>Transpiled Circuit</h1>
      <div class="circuit">
        <Circuit
          id="transpiled-circuit"
          circuit_data={$data?.transpiled}
          is_original={false}
          match={$data?.match}
          matched_circuit_id="original-circuit"
          matched_machine_id="on-machine"
          {open_tool}
        ></Circuit>
      </div>
    </section>

    <section class="circuit-view-wrap">
      <h1>On-machine view</h1>
      <div class="circuit">
        <MachineView
          data={$data?.backend}
          match={$data?.match}
          id="on-machine"
          transpiled_circuit_id="transpiled-circuit"
          original_circuit_id="original-circuit"
          operation_data={$data?.transpiled}
          {open_tool}
        ></MachineView>
      </div>
    </section>
  </div>
  <div class="contexts">
    <section class="circuit-view-wrap info-wrap">
      <h1>Information & Interaction</h1>
      <div class="info-section">
        {#if $selected_info}
          <Information info={$selected_info.data}></Information>
        {/if}
      </div>
    </section>
  </div>
</div>
<span>
  <!--pre>
{JSON.stringify($data, null, 2)}
</pre-->
</span>

<style>
  * {
    box-sizing: border-box;
    font-family: sans-serif;
    line-height: 100%;
  }
  .circuit-view-wrap {
    padding: 0;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
  }
  .circuit {
    padding: 0.5rem 1rem;
    overflow-x: scroll;
  }
  h1 {
    font-size: 1rem;
    padding: 0.5rem 1rem;
    margin: 0 0 0.5rem 0;
    background-color: #f0f0f0;
    border-bottom: 1px solid #ddd;
  }
  .frame {
    display: flex;
  }
  .circuits {
    width: calc(100% - 400px);
  }
  .contexts,
  .info-section {
    width: 400px;
  }
  .contexts {
    width: 400px;
    padding-left: 0.5rem;
  }
  .info-wrap {
    position: sticky;
    top: 0;
  }
</style>
