<script>
  export let info;
</script>

{#if info}
  <div>
    <h2>Machine Qubit Information</h2>
    <!-- <h3>Gate: {item.gate}</h3> -->
    <div class="info-section">
      <table>
        <tbody>
          <tr>
            <th>From</th><td>{info.original_qubit_id} </td>
          </tr>
          <tr>
            <th>To</th><td>{info.qubit_id} </td>
          </tr>
          {#if info.readout_error}
            <tr>
              <th>Readout error</th><td>{info.readout_error.value} </td>
            </tr>
          {/if}
        </tbody>
      </table>
    </div>
  </div>
{/if}

<style>
  * {
    box-sizing: border-box;
    line-height: 100%;
  }
  h2 {
    width: calc(100% - 0.5rem);
    margin: 0;
    padding: 0.5rem 1rem 1rem 1rem;
    font-size: 1rem;
    border-bottom: 1px solid #ddd;
    line-height: 0;
  }

  .info-section {
    padding: 0;
    margin-bottom: 0.5rem;
  }
  table {
    width: calc(100% - 0.5rem);
    font-family: Iosevka;
    border-collapse: collapse;
    border-radius: 0.5rem;
  }
  table th,
  table td,
  table thead th,
  table thead td {
    border-bottom: 1px solid #ddd;
    padding: 0.5rem 1rem;
    text-align: left;
  }
  table thead th {
    border-top: 3px solid #ddd;
  }
  table thead tr th,
  table th {
    border-right: 1px solid #ddd;
  }
  table thead tr th:last-of-type {
    border-right: 0;
  }
  /* table tbody tr:last-of-type th,
  table tbody tr:last-of-type td {
    border-bottom: 0;
  } */
</style>
