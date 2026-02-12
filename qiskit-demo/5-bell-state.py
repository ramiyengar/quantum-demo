from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Map - Create the Bell State circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all() # Required for Sampler

# Execute - Using local StatevectorSampler (No API needed)
sampler = StatevectorSampler()
job = sampler.run([qc])
result = job.result()

# Analyze - Index into the result container  to get the data
pub_result = result 
counts = pub_result[0].data.meas.get_counts()
bitstrings = pub_result[0].data.meas.get_bitstrings()

print(f"Aggregated Counts: {counts}")
print(f"First 5 outcomes: {bitstrings[:5]}")
