<script>
  import { onDestroy, onMount } from "svelte";
  import { writable } from "svelte/store";
  import { convertToQiskitCode } from "./toQiskit";
  import { QiskitMachines } from "./machines";

  import MachineSection from "./MachineSection.svelte";
  import OperationsSection from "./OperationsSection.svelte";
  import ObservableSection from "./ObservableSection.svelte";
  import MeasureSection from "./MeasureSection.svelte";

  export let model;
  export let key_circ = "circ_code",
    key_machine = "machine";
  let circ = model.get(key_circ),
    machine_info;
  let event = `change:${key_machine}`;
  let callback = () => (count = model.get(key_machine));
  let data = writable({});
  let output_code = writable({});

  onMount(() => {
    if (model.get(key_machine))
      machine_info = JSON.parse(model.get(key_machine));
    circ = model.get(key_circ);

    data.subscribe((d) => {
      // data check
      if (d.operations) {
        d.num_operations =
          d.operations?.filter((e) => !e.deactive)?.length || 0;
      }
      if (d.pauli_obs) {
        d.num_pauli_obs = d.pauli_obs?.filter((e) => !e.deactive)?.length || 0;
        d.pauli_obs.forEach((obs) => {
          if (obs.observable.length < d.machine_qubits) {
            obs.observable =
              obs.observable +
              "I".repeat(d.machine_qubits - obs.observable.length);
          } else if (obs.observable.length > d.machine_qubits) {
            obs.observable = obs.observable.substring(0, d.machine_qubits);
          }
        });
      }

      if (d.machine) {
        d.machine_qubits = QiskitMachines[d.machine]?.n_qubits;
        if (!QiskitMachines[d.machine].sim) {
          d.no_sim = true;
          d.no_machine = false;
          d.is_simulator = false;
        } else if (!QiskitMachines[d.machine].machine) {
          d.no_machine = true;
          d.no_sim = false;
          d.is_simulator = true;
        } else {
          d.no_sim = false;
          d.no_machine = false;
        }
        if (d.no_sim) {
          d.sim_not_choosable = true;
        } else if (d.no_machine) {
          d.sim_not_choosable = true;
        } else {
          d.sim_not_choosable = false;
        }
      }

      if (d.measure && d.measure.length > 0) {
        d.measure.sort();
      }

      output_code.set(convertToQiskitCode(d));

    });

    output_code.subscribe((code) => {
      // output
      model.set(key_circ, code);
      model.save_changes();
    });

    data.set({
      machine: machine_info?.name,
      is_simulator: machine_info?.is_simulator
    });
    model.on(event, callback);
  });

  onDestroy(() => {
    model.off(event, callback);
  });
</script>

<section class="circuit-write-wrap">
  <h3>Writing a quantum circuit</h3>
  <div class="content">
    <MachineSection {data}></MachineSection>

    <OperationsSection {data}></OperationsSection>

    <article class={$data.num_qubits ? "" : "deactive"}>
      <h4>3. Measure? or Observe?</h4>
      <div class="input-row">
        <div class="input-form">
          <label>Choose reporting method</label>
          <div class="checkbox-group">
            <div class="checkbox-item">
              <input
                type="radio"
                id="reporting-measure"
                checked={$data.reporting === "measure"}
                on:change={(e) => {
                  data.update((d) => {
                    if (e.target.checked) {
                      d.reporting = "measure";
                    }
                    return d;
                  });
                }}
              />
              <label for="reporting-measure">Measure</label>
            </div>
            <div class="checkbox-item">
              <input
                type="radio"
                id="reporting-observe"
                checked={$data.reporting === "observe"}
                on:change={(e) => {
                  data.update((d) => {
                    if (e.target.checked) {
                      d.reporting = "observe";
                    }
                    return d;
                  });
                }}
              />
              <label for="reporting-observe">Pauli-Observables</label>
            </div>
          </div>
        </div>
      </div>
    </article>
    {#if $data.reporting === "observe"}
      <ObservableSection {data}></ObservableSection>
    {:else if $data.reporting === "measure"}
      <MeasureSection {data}></MeasureSection>
    {/if}
  </div>
</section>

<style>
  .circuit-write-wrap,
  .circuit-write-view {
    margin-top: 1rem;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    overflow: hidden;
  }
  .content {
    padding: 0;
    overflow-x: scroll;
  }
  article {
    padding: 1rem;
    margin-bottom: 0;
    border-top: 1px solid #ddd;
  }
  article:first-of-type {
    margin-top: 0;
    border-top: 0;
    padding-top: 0;
  }
  h2 {
    font-size: 2.5rem;
    font-weight: 100;
    margin-top: 2rem;
    margin-bottom: 2rem;
  }
  h3 {
    font-size: 1rem;
    padding: 0.5rem 1rem;
    margin: 0 0 0.5rem 0;
    background-color: #f0f0f0;
    border-bottom: 1px solid #ddd;
    border-radius: 0.5rem 0.5rem 0 0;
  }
  h4 {
    margin: 0 0 0.25rem 0;
    padding: 0 0 0.5rem 0;
    font-size: 1rem;
    line-height: 100%;
    font-weight: 600;
  }

  .input-row {
    display: flex;
    column-gap: 1rem;
    row-gap: 1rem;
    font-size: 0.9rem;
    margin-top: 0.25rem;
    margin-bottom: 0.5rem;
    max-width: 80vw;
    flex-wrap: wrap;
  }

  .input-form {
    display: flex;
  }
  .input-form > label {
    display: block;
    padding: 0.5rem 0.5rem;
    border: 1px solid #ddd;
    border-radius: 0.25rem 0 0 0.25rem;
    background-color: #f0f0f0;
    font-family: var(--font-mono);
    line-height: 100%;
  }

  .checkbox-group {
    display: flex;
    /* column-gap: 1rem; */
    padding: 0;
    border: 1px solid #ddd;
    border-left-width: 0;
    border-radius: 0 0.25rem 0.25rem 0;
    font-family: var(--font-mono);
    line-height: 100%;
    flex-wrap: wrap;
    max-width: 80vw;
    /* overflow-x: scroll; */
  }
  .checkbox-item {
    display: flex;
    align-items: center;
    /* border-left: 1px solid #ddd; */
    padding: 0.25rem 0.5rem;
  }
  .checkbox-item:first-of-type {
    border-left: 0;
  }
  .checkbox-group input {
    display: block;
    line-height: 100%;
  }
  .checkbox-group label {
    display: block;
    font-family: var(--font-mono);
    line-height: 100%;
    padding-left: 0.25rem;
    padding-right: 0.25rem;
  }

  .deactive * {
    opacity: 0.5;
  }
</style>
