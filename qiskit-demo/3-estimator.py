import numpy as np
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator

# Initialize Service and Backend
service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

# Step 1: Map - Define the Ansatz and Observable
# We want to measure the correlation between four qubits in the Z-basis 
num_qubits = 4
ansatz = EfficientSU2(num_qubits, entanglement="linear", reps=1)
observable = SparsePauliOp("ZZZZ")

# Step 2: Optimize - Transpile for the Backend
# For Estimator, the observable must also be mapped to the hardware layout [10, 27]
pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
isa_ansatz = pm.run(ansatz)
isa_observable = observable.apply_layout(isa_ansatz.layout)

# Step 3: Execute - Estimator V2 with Error Mitigation
estimator = Estimator(mode=backend)
# Resilience level 1 enables advanced readout error mitigation 
estimator.options.resilience_level = 1

# Generate random parameters for the demo
params = np.random.rand(ansatz.num_parameters)

# Run the job
job = estimator.run([(isa_ansatz, isa_observable, params)])
result = job.result()

# Step 4: Analyze
# The 'evs' (Expectation ValueS) array contains the results [27, 28]
print(f"Computed Expectation Value: {result.data.evs}")
print(f"Variance/Uncertainty: {result.data.stds}")
