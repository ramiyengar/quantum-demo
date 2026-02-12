from qiskit.circuit.library.phase_oracle import PhaseOracleGate
from qiskit_algorithms import AmplificationProblem, Grover
from qiskit.primitives import StatevectorSampler

# Map - Find inputs that satisfy (a AND NOT b)
expression = "a & ~b"
oracle = PhaseOracleGate(expression)
problem = AmplificationProblem(oracle, is_good_state=["10"])

# Execute
grover = Grover(sampler=StatevectorSampler())
result = grover.amplify(problem)

# Analyze
print(f"Search Successful: {result.oracle_evaluation}")
print(f"Found Solution: {result.top_measurement}")

# To access full counts if needed:
# full_counts = result.circuit_results.data.meas.get_counts()
