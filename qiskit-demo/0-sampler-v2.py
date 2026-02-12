import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram

# Initialize the Qiskit Runtime Service
# This requires a valid IBM Quantum API token and instance CRN [18, 19]
service = QiskitRuntimeService()

# Selection of the least busy backend ensures efficient execution time
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=2)

# Stage 1: Problem Mapping - Creating the Bell State Circuit
qc = QuantumCircuit(2)
qc.h(0)        # Apply Hadamard to qubit 0
qc.cx(0, 1)    # Entangle qubit 0 and 1
qc.measure_all() # Explicit measurements are required for SamplerV2 

# Stage 2: Optimization - Transpilation to ISA
# The pass manager optimizes the circuit for the specific backend connectivity 
pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
isa_circuit = pm.run(qc)

# Stage 3: Execution - Submitting to Sampler V2
# The 'mode' parameter specifies the execution environment (hardware or simulator) 
sampler = Sampler(mode=backend)
job = sampler.run([isa_circuit]) # Input is a list of Primitive Unified Blocs (PUBs) 
result = job.result()

# Stage 4: Analysis - Retrieving and Visualizing Counts
# Results are retrieved from the 'meas' register by default 
pub_result = result
counts = pub_result.data.meas.get_counts()
print(f"Sampling Results: {counts}")
plot_histogram(counts)
