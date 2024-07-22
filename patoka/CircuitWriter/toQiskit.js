import { QiskitMachines } from "./machines";
import { ProblemMap } from "./problems";
import { shors_alg, shors_period_operators, shors_var_setup } from "./shors_period";

export function convertToQiskitCode(data, config) {
  let code_lines = [], includes = [], run_codes = [], analysis_codes = [];
  if (!config?.no_includes) {
    includes.push("from qiskit import QuantumCircuit");
    if (data.reporting === "measure") includes.push("from qiskit.visualization import plot_histogram");
  }
  code_lines.push(`circuit = QuantumCircuit(${data?.num_qubits || 0}, ${data?.num_clbits || 0})`);

  let machine = QiskitMachines[data.machine], is_simulator = data.is_simulator;

  if (machine) {
    includes.push("from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager")
    if (machine.name === "Aer") {
      includes.push("from qiskit_aer import AerSimulator");
      includes.push("from qiskit import transpile")
    } else if (is_simulator) {
      includes.push("import qiskit_aer");
      includes.push(`from qiskit_ibm_runtime.fake_provider import ${machine.sim}`);
    } else {
      includes.push("import os");
      includes.push("from qiskit_ibm_runtime import QiskitRuntimeService")
    }
  }

  if (data?.operations) {
    let oi = 0;
    for (const op_def of data.operations) {
      if (!op_def.deactive) {
        let op = ProblemMap[op_def.operation_def];
        if (op?.key === "QFT") {
          code_lines.push("")
          code_lines.push("# Quantum Fourier Transform")
          includes.push("from qiskit.circuit.library import QFT")
          code_lines.push(`qft_${oi} = QFT(${op_def.apply_to.length}).to_gate()`);
          code_lines.push(`circuit.append(qft_${oi}, [${op_def.apply_to.join(", ")}])`);
        } else if (op?.key === "superposition") {
          code_lines.push("")
          code_lines.push("# Superposition")
          op_def.apply_to.forEach((q) => {
            code_lines.push(`circuit.h(${q})`);
          })
        } else if (op?.key === "entanglement") {
          code_lines.push("# Entanglement");
          code_lines.push(`circuit.h(${op_def.apply_to[0]})`);
          code_lines.push(`circuit.cx(${op_def.apply_to.join(", ")})`);
        } else if (op?.key === "interference") {
          code_lines.push("")
          code_lines.push("# Interference")
          op_def.apply_to.forEach((q, i) => {
            code_lines.push(`circuit.rz(${q},${op_def.params?.theta || 0})`);
          })
        } else if (op?.key === "BTT") {
          code_lines.push("")
          // includes
          includes.push("from revkit import netlist, oracle_synth, truth_table");
          includes.push("import revkit.export.qiskit");

          // codes
          code_lines.push("# Boolean Truth Table Function Oracle");
          // todo: parse if possible
          code_lines.push(`tt_bool_${oi} = revkit.truth_table.from_expression("${op_def.globals.boolean_expression}")`);
          code_lines.push(`oracle_${oi} = revkit.oracle_synth(tt_bool_${oi})`);

          if (op.globals.random_all) {
            code_lines.push("# Entangle every qubit");
            op_def.apply_to.forEach((q, i) => {
              code_lines.push(`circuit.h(${q})`);
            });
          }

          code_lines.push(`oracle_gate_${oi} = oracle_${oi}.to_qiskit().to_gate()`);
          code_lines.push(`circuit.append(oracle_gate_${oi}, [${op_def.apply_to.join(", ")}])`);

          // todo: deal with interpreter
        } else if (op?.key === "SHOR_period") {
          if (!includes.includes("import numpy as np")) {
            includes.push("import numpy as np");
          }
          code_lines.push(shors_period_operators)
          let vars = shors_var_setup(op_def.qubit_registers?.counter?.apply_to || [],
            op_def.qubit_registers?.oracle?.apply_to || [],
            op_def.params.divider, op_def.params.factor)
          code_lines.push(vars)
          code_lines.push(shors_alg)
        }
        oi++;
      }
    }
  }

  if (machine) {
    if (machine.name === "Aer") {
      run_codes.push(`aer_sim = AerSimulator()`);
    } else {
      run_codes.push("# backend and optimizer")
      run_codes.push(`optimization_level = ${data.optimization_level || 1}`);
      if (is_simulator) {
        run_codes.push(`backend = qiskit_aer.AerSimulator.from_backend(${machine.sim}())`);
      } else {
        run_codes.push("# the below code retrieves your IBM token that is stored as an environment variable.")
        run_codes.push("# Visit https://docs.quantum.ibm.com/api/runtime/ for details and search 'store an environment variable' for how-to.")
        run_codes.push(`token = os.environ["ibm_token"]`);
        run_codes.push("# Alternatively, you can directly provide your token as a string, which is less recommended.")
        run_codes.push(`# token = YOUR_TOKEN`);
        run_codes.push(`QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)`);
        run_codes.push(`service = QiskitRuntimeService(channel="ibm_quantum")`);
        run_codes.push(`avail_backends = service.backend(name=${machine.machine})`);
      }
      run_codes.push(`pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=optimization_level)`);
    }
    run_codes.push("")
  }

  if (data.reporting === "observe") {
    if (data?.pauli_obs?.length > 0) {
      if (!config?.no_includes) {
        includes.push("from qiskit.quantum_info import SparsePauliOp");
        includes.push("from qiskit_ibm_runtime import EstimatorV2 as Estimator")
      }
      code_lines.push("")
      code_lines.push("# Pauli Observables")
      code_lines.push(`observables_labels = [${data.pauli_obs.map((o) => '"' + o.observable + '"').join(", ")}]`)
      code_lines.push(`observables = [SparsePauliOp(label) for label in observables_labels]`);
      code_lines.push(`mapped_observables = [observable.apply_layout(circuit.layout) for observable in observables]`);
    }

    if (!machine) {
      run_codes.push(`# # Uncomment & run this code with a pass manager`);
      run_codes.push(`# estimator = Estimator(backend)`)
      run_codes.push(`# transpiled = pass_manager.run(circuit)`);
      run_codes.push(`# # Uncomment & Run this code with a backend`)
      run_codes.push(`# job = estimator.run([(transpiled, mapped_observables)])`)
    } else {
      run_codes.push(`# pass manager and run`);
      run_codes.push(`estimator = Estimator(backend)`)
      run_codes.push(`transpiled = pass_manager.run(circuit)`);
      run_codes.push(`job = estimator.run([(transpiled, mapped_observables)])`)
    }
  } else if (data.reporting === "measure") {
    if (data?.measure_all) {
      code_lines.push("")
      code_lines.push("# Measure")
      code_lines.push("circuit.measure_all()");
    } else if (data?.measure && data?.measure.length > 0) {
      code_lines.push("")
      code_lines.push("# Measure")
      let clbits_to_use = data.clbits.slice(0, data.measure.length);
      code_lines.push(`circuit.measure([${data.measure.join(", ")}], [${clbits_to_use.join(", ")}])`)
    }
    if (!machine) {
      run_codes.push(`# # Uncomment & run this code with a pass manager`);
      run_codes.push(`# transpiled = pass_manager.run(circuit)`);
      run_codes.push(`# # Run this code with a backend`);
      run_codes.push(`# job = backend.run(circuit)`);
    } else if (machine.name === "Aer") {
      run_codes.push(`transpiled = transpile(circuit, aer_sim)`);
      run_codes.push(`job = aer_sim.run(transpiled)`);
    } else {
      run_codes.push(`# pass manager and run`);
      run_codes.push(`transpiled = pass_manager.run(circuit)`);
      run_codes.push(`job = backend.run(circuit)`);
    }
    run_codes.push("")
    run_codes.push("counts = job.result().get_counts()")
    run_codes.push("plot_histogram(counts)")
  }


  return includes.join("\n") + "\n\n" + code_lines.join("\n") + "\n\n" + run_codes.join("\n") + "\n\n" + analysis_codes.join("\n")
}