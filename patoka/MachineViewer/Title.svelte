<script>
  export let title = "",
    hide,
    level = 1;
  export let toggleSection = () => {};
</script>

{#if level == 1}
  <h1>
    {title}
    <button
      on:click={() => {
        toggleSection();
      }}>{hide ? "Open" : "Close"}</button
    >
  </h1>
{:else if level == 2}
  <h2>
    {title}
    <button
      on:click={() => {
        toggleSection();
      }}>{hide ? "Open" : "Close"}</button
    >
  </h2>
{/if}

<style>
  h1 {
    margin: 0 0 0.5rem 0;
    font-size: 1.4rem;
    font-weight: 500;
    line-height: 100%;
    vertical-align: middle;
  }
  h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    font-weight: 500;
    line-height: 100%;
    vertical-align: middle;
  }
  button {
    display: inline-block;
    appearance: none;
    margin: 0 0 0 1rem;
    border: 0;
    background-color: transparent;
    line-height: 100%;
    font-size: 0.8rem;
    vertical-align: middle;
  }
</style>
