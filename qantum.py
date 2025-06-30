from qiskit import QuantumCircuit
from qiskit_aer import Aer

# Create quantum circuit with 3 qubits and 3 classical bits
qc = QuantumCircuit(3, 3)

# Apply Hadamard gate to qubit 0
qc.h(0)

# Apply CNOT gate between qubit 0 and 1
qc.cx(0, 1)

# Measure qubits into classical bits
qc.measure(0, 0)
qc.measure(1, 1)
qc.measure(2, 2)

# Print ASCII circuit diagram
print(qc)

# Use Aer's simulator to run the circuit
simulator = Aer.get_backend('qasm_simulator')

# Execute the circuit 1000 times to collect statistics
job = simulator.run(qc, shots=1000)

# Get results
result = job.result()
counts = result.get_counts(qc)

# Print the result counts
print("Measurement Results:", counts)




