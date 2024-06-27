<script>
  export let data = {};
</script>

{#if data}
  <text
    id={data.id}
    class={data._class}
    data-role={data.role}
    x={data.x}
    y={data.y}
    width={data.width}
    height={data.height}
    text-anchor={data["text-anchor"]}
    alignment-baseline={data["alignment-baseline"]}
    font-size={data["font-size"]}
    font-weight={data["font-weight"]}
    fill={data.fill}
  >
    {data.text}
  </text>
{/if}

<style>
  text {
    user-select: none;
  }
</style>
