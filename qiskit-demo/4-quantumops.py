import pytest
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

@pytest.fixture
def ideal_sampler():
    # Use a fixed seed for reproducibility in tests [32, 33]
    sim = AerSimulator(seed_simulator=42)
    return Sampler(mode=sim)

def test_hadamard_superposition(ideal_sampler):
    # Setup a single qubit in superposition
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()
    
    # Execution
    result = ideal_sampler.run([qc]).result()
    counts = result.data.meas.get_counts()
    
    # Probability should be ~50% for '0' and '1'
    total = sum(counts.values())
    p0 = counts.get('0', 0) / total
    p1 = counts.get('1', 0) / total
    
    # Use pytest.approx for statistical tolerance [32, 34]
    assert p0 == pytest.approx(0.5, abs=0.05)
    assert p1 == pytest.approx(0.5, abs=0.05)
