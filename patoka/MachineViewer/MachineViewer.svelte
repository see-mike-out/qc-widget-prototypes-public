<script>
  import { onDestroy, onMount } from "svelte";
  import { writable } from "svelte/store";
  import { sections, titles, descriptions, markers } from "./meta_info";
  import { makeCode } from "./util";
  import Section from "./Section.svelte";
  export let model;
  export let data_key = "machine_data",
    output_key = "code";
  let str_data = model.get(data_key);
  let parsed_data = JSON.parse(str_data);
  let event = `change:${data_key}`;
  let callback = () => (circ = model.get(data_key));
  let data = writable();
  let basket = writable([]);
  let basket_code = writable("");

  onMount(() => {
    data.set(parsed_data);
    model.on(event, callback);
    basket.subscribe((d) => {
      basket_code.set(makeCode(d));
    });
    basket_code.subscribe((code) => {
      model.set(output_key, code);
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

<section class="wrap" id="machine-viewer-wrap">
  <h3>Machine information</h3>
  {#if $data}
    <Section {data} {addToBasket} {basket} section_meta={sections[0]}></Section>
    <Section {data} {addToBasket} {basket} section_meta={sections[1]}></Section>
    <Section
      {data}
      {addToBasket}
      {basket}
      section_meta={sections[2]}
      hide={true}
    ></Section>
    <Section {data} {addToBasket} {basket} section_meta={sections[3]}></Section>
    <Section
      {data}
      {addToBasket}
      {basket}
      section_meta={sections[4]}
      hide={true}
    ></Section>
    <Section
      {data}
      {addToBasket}
      {basket}
      section_meta={sections[5]}
      hide={true}
    ></Section>
    <Section
      {data}
      {addToBasket}
      {basket}
      section_meta={sections[6]}
      hide={true}
    ></Section>
    <Section {data} {addToBasket} {basket} section_meta={sections[7]}></Section>
  {/if}
</section>

<style>
    
    :root {
        --font-body: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Arial,
            Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        --font-mono: Iosevka, 'Fira Mono', monospace;
    }
  h3 {
    font-size: 1rem;
    padding: 0.5rem 1rem;
    margin: 0 0 0.5rem 0;
    background-color: #f0f0f0;
    border-bottom: 1px solid #ddd;
    border-radius: 0.5rem 0.5rem 0 0;
  }
  h3 button {
    appearance: none;
    cursor: pointer;
    display: inline;
    border: 0;
    padding: 0.15rem;
    margin: 0 0 0 1rem;
    background-color: transparent;
    border-radius: 0.25rem;
  }
  h3 button:hover {
    background-color: rgba(255, 255, 255, 0.9);
  }
  .wrap {
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    height: 60vh;
    overflow-y: scroll;
  }
  pre {
    font-family: var(--font-mono);
  }
  :global(article .content-wrap *) {
    font-family: var(--font-mono) !important;
  }
</style>
