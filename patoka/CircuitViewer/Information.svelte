<script>
  import { writable } from "svelte/store";
  import EspInfo from "./ESPInfo.svelte";
  import GateErrorInfo from "./GateErrorInfo.svelte";
  import GateInfo from "./GateInfo.svelte";
  import QubitGateInfo from "./QubitGateInfo.svelte";
  import QubitInfo from "./QubitInfo.svelte";
  import ReadoutErrorInfo from "./ReadoutErrorInfo.svelte";

  export let info,
    machine_moment_at = writable();
</script>

{#if info}
  {#if info.qubit}
    <QubitInfo {info}></QubitInfo>
  {/if}
  {#if info.operation}
    <GateInfo {info}></GateInfo>
  {/if}
  {#if info.readout_error}
    <ReadoutErrorInfo {info} {machine_moment_at}></ReadoutErrorInfo>
  {/if}
  {#if info.gate_info}
    <QubitGateInfo {info}></QubitGateInfo>
  {/if}
  {#if info.gate_error_info}
    <GateErrorInfo {info}></GateErrorInfo>
  {/if}
  {#if info.esp_this}
    <EspInfo {info}></EspInfo>
  {/if}
{/if}
