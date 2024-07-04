<script>
  import { onDestroy, onMount } from "svelte";
  import { writable } from "svelte/store";
  import Circuit from "./Circuit.svelte";
  import Information from "./Information.svelte";
  import MachineView from "./MachineView.svelte";
  import { getSVGimageLink } from "./svg_utils/util";
  export let model;
  export let key_circ = "circ";
  let circ = model.get(key_circ);
  let parsed_circ = JSON.parse(circ);
  let event = `change:${key_circ}`;
  let callback = () => (circ = model.get(key_circ));
  let data = writable();
  let machine_moment_at = writable(0);

  let selected_info = writable();
  let images = {};
  let images_loader = writable();
  images_loader.subscribe((d) => {
    if (d) {
      images[d.id] = d;
    }
  });

  function open_tool(info) {
    selected_info.set(info);
  }
  onMount(() => {
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
      <h1>
        Original Circuit <button
          class="save-make"
          on:click={(e) => {
            getSVGimageLink("original-circuit", images_loader);
          }}>Save the image</button
        >
        {#if images["original-circuit"]}
          <a
            class="save-download"
            href={images["original-circuit"].png}
            download>Download (png)</a
          >
          <a
            class="save-download"
            href={images["original-circuit"].svg}
            download>Download (svg)</a
          >
        {/if}
      </h1>
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
      <h1>
        Transpiled Circuit <button
          class="save-make"
          on:click={(e) => {
            getSVGimageLink("transpiled-circuit", images_loader);
          }}>Save the image</button
        >
        {#if images["transpiled-circuit"]}
          <a
            class="save-download"
            href={images["transpiled-circuit"].png}
            download>Download (png)</a
          >
          <a
            class="save-download"
            href={images["transpiled-circuit"].svg}
            download>Download (svg)</a
          >
        {/if}
      </h1>
      <div class="circuit">
        <Circuit
          id="transpiled-circuit"
          circuit_data={$data?.transpiled}
          is_original={false}
          match={$data?.match}
          matched_circuit_id="original-circuit"
          matched_machine_id="on-machine"
          {open_tool}
          {machine_moment_at}
        ></Circuit>
      </div>
    </section>

    <section class="circuit-view-wrap">
      <h1>
        On-machine view <button
          class="save-make"
          on:click={(e) => {
            getSVGimageLink("on-machine", images_loader);
          }}>Save the image</button
        >
        {#if images["on-machine"]}
          <a class="save-download" href={images["on-machine"].png} download
            >Download (png)</a
          >
          <a class="save-download" href={images["on-machine"].svg} download
            >Download (svg)</a
          >
        {/if}
      </h1>
      <div class="circuit">
        <MachineView
          data={$data?.backend}
          match={$data?.match}
          id="on-machine"
          transpiled_circuit_id="transpiled-circuit"
          original_circuit_id="original-circuit"
          operation_data={$data?.transpiled}
          {open_tool}
          {machine_moment_at}
        ></MachineView>
      </div>
    </section>
  </div>
  <div class="contexts">
    <section class="circuit-view-wrap info-section-group">
      <h1>Information & Interaction</h1>
      <div class="info-section-wrap">
        {#if $selected_info}
          <Information info={$selected_info.data} {machine_moment_at}
          ></Information>
        {/if}
      </div>
    </section>
  </div>
</div>

<!-- <span>
  <pre>
{JSON.stringify($data, null, 2)}
</pre>
</span> -->

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
  .info-section-group {
    position: sticky;
    top: 0;
  }
  .info-section-wrap {
    max-height: 700px;
    overflow-y: scroll;
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
    width: calc(100vw - 400px - 1rem);
    max-height: 800px;
    overflow-y: scroll;
  }
  .contexts {
    width: 400px;
    padding-left: 0.5rem;
  }
  .save-make,
  .save-download {
    appearance: none;
    display: inline-block;
    font-size: 0.9rem;
    text-decoration: none;
    margin-left: 2rem;
    color: #454545;
    border: 0;
    padding: 0;
    background-color: transparent;
    cursor: pointer;
  }
  .save-make:hover,
  .save-download:hover {
    outline: 2px solid orange;
  }
</style>
