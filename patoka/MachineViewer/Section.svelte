<script>
  import { writable } from "svelte/store";
  import Title from "./Title.svelte";
  import Panel from "./Panel.svelte";
  import Subsection from "./Subsection.svelte";

  export let data = writable();
  export let addToBasket = () => {};
  export let basket;
  export let section_meta;
  let hide = false;
  function toggleSection() {
    hide = !hide;
  }
</script>

{#if $data && section_meta}
  <section>
    <Title title={section_meta.title} {toggleSection} {hide} level={1}></Title>
    {#if !hide}
      <div class="panel">
        {#each section_meta?.subsections as sub}
          <!-- special cases -->
          {#if sub === "asof"}
            <Panel key={sub} value={$data[sub]} level={1}></Panel>
          {:else if !sub.key}
            <Panel key={sub} value={$data[sub]} level={1} {addToBasket} {basket}
            ></Panel>
          {/if}
        {/each}
      </div>
      {#each section_meta?.subsections as sub}
        {#if sub.key && sub.order}
          <Subsection section_meta={sub} {addToBasket} {basket} {data}
          ></Subsection>
        {/if}
      {/each}
    {/if}
  </section>
{/if}

<style>
  * {
    box-sizing: border-box;
    font-family: sans-serif;
    line-height: 100%;
  }
  section {
    width: 100%;
    padding: 1rem;
    border-bottom: 1px solid #ddd;
  }
  .panel {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    column-gap: 1rem;
    row-gap: 1rem;
  }
</style>
