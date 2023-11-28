from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Operator
import numpy as np
from scipy.linalg import expm

kicking_strength = 1.0
planck_constant = 2 * np.pi / 10
num_qubits = 5  # Determines the size of the Hilbert space

def create_qkr_circuit(num_qubits, kicking_strength, planck_constant):
    circuit = QuantumCircuit(num_qubits)

    # Kinetic term
    for qubit in range(num_qubits):
        circuit.rx(planck_constant * (qubit - num_qubits // 2)**2, qubit)

    # Change to the position basis (Fourier transform)
    circuit.barrier()
    circuit.append(QFT(num_qubits, inverse=True), range(num_qubits))
    circuit.barrier()

    # Potential term (kicking)
    for qubit in range(num_qubits):
        circuit.rz(kicking_strength, qubit)

    # Change back to the momentum basis
    circuit.barrier()
    circuit.append(QFT(num_qubits), range(num_qubits))
    circuit.barrier()

    return circuit


# Create the QKR circuit
circuit = create_qkr_circuit(num_qubits, kicking_strength, planck_constant)

# Convert the circuit to a unitary matrix
unitary_operator = Operator(circuit)

# To visualize the circuit (optional)
# print(circuit.draw(output='text'))

############### Retrieve Eigenvalues ###############
eigenvalues, _ = np.linalg.eig(unitary_operator.data)

# Normalize the eigenvalues to get phases
phases = np.angle(eigenvalues)

# You can print the eigenvalues / phases
print(phases)

