from qiskit_algorithms import Grover, AmplificationProblem
from qiskit.circuit.library.phase_oracle import PhaseOracleGate
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram

# Define the search problem using a Boolean logic expression
# Find w, x, y, z such that (w!= x) AND (y == z) AND (x, y, z are all True)
expression = "(w ^ x) & ~(y ^ z) & (x & y & z)"

# Step 1: Oracle Engineering
# PhaseOracleGate automatically synthesizes the complex gate logic 
oracle = PhaseOracleGate(expression)

# Step 2: Problem Definition
# AmplificationProblem encapsulates the oracle and the search space [8, 9]
problem = AmplificationProblem(oracle)

# Step 3: Initialization of the Grover Algorithm
# StatevectorSampler is used here for local, exact simulation [8, 9]
grover = Grover(sampler=StatevectorSampler())

# Step 4: Execution
# The amplify method handles the optimal number of iterations [8, 9]
result = grover.amplify(problem)

# Step 5: Interpretation of Results
print(f"Satisfying Assignment: {result.assignment}")
# result.circuit_results contains the final state distribution 
plot_histogram(result.circuit_results)
