<script>
  import { onDestroy, onMount } from "svelte";
  import { writable } from "svelte/store";
  export let model;
  export let key_circ = "circ_code";
  let circ = model.get(key_circ);
  let event = `change:${key_circ}`;
  let data = writable();

  let callback = () => {
    circ = model.get(key_circ);
    data.set(circ);
  };

  onMount(() => {
    data.set(circ);
    model.on(event, callback);
  });

  onDestroy(() => {
    model.off(event, callback);
  });

  data.subscribe((d) => {
    model.set(key_circ, d);
    model.save_changes();
  });
</script>
<h1>Circuit Writer</h1>

<button on:click={(e) => { data.update((d) => { return d + " >>"}) }}>Change</button>

{$data}