<script>
  import { onDestroy, onMount } from "svelte";
  import { writable } from "svelte/store";
  import { sections, titles, descriptions, markers } from "./meta_info";
  import { makeCode } from "./util";
  import Section from "./Section.svelte";
  export let model;
  export let data_key = "machine_data", output_key = "code";
  let str_data = model.get(data_key);
  let parsed_data = JSON.parse(str_data);
  let event = `change:${data_key}`;
  let callback = () => (circ = model.get(data_key));
  let data = writable();
  let basket = writable([]);
  let basket_code;

  onMount(() => {
    data.set(parsed_data);
    model.on(event, callback);
    basket.subscribe((d) => {
      basket_code = makeCode(d);
      model.set(output_key, basket_code);
      model.save_changes();
    });
  });

  onDestroy(() => {
    model.off(event, callback);
  });

  function addToBasket(a) {
    basket.update((d) => {
      if (d.includes(a)) {
        d.splice(d.indexOf(a), 1);
      } else {
        d.push(a);
      }
      return d;
    });
  }
</script>

<div class="wrap" id="machine-viewer-wrap">
  {#if $data}
    <Section {data} {addToBasket} {basket} section_meta={sections[0]}></Section>
    <Section {data} {addToBasket} {basket} section_meta={sections[1]}></Section>
    <Section {data} {addToBasket} {basket} section_meta={sections[2]}></Section>
    <Section {data} {addToBasket} {basket} section_meta={sections[3]}></Section>
    <Section {data} {addToBasket} {basket} section_meta={sections[4]}></Section>
  {/if}
</div>

<pre>
{@html basket_code}
</pre>

<style>
  * {
    box-sizing: border-box;
    font-family: sans-serif;
    line-height: 100%;
  }
  .wrap {
    max-height: 770px;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    overflow-y: scroll;
  }
  pre {
    font-family: iosevka;
  }
</style>
