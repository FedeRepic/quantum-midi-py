from qiskit import QuantumCircuit
from qiskit_aer import Aer
from mido import Message, MidiFile, MidiTrack

# Crear circuito
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.cx(0, 1)
qc.measure(0, 0)
qc.measure(1, 1)
qc.measure(2, 2)

# Simular
simulator = Aer.get_backend('qasm_simulator')
job = simulator.run(qc, shots=100)
result = job.result()
counts = result.get_counts(qc)

# Crear archivo MIDI
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Mapear bitstrings a notas MIDI
note_base = 60  # C4
for bitstring, freq in counts.items():
    note = int(bitstring, 2) % 128  # convertir binario a número, limitar a rango MIDI
    velocity = 64
    duration = 480  # ticks
    
    for _ in range(min(freq, 10)):  # limitar repeticiones
        track.append(Message('note_on', note=note_base + note, velocity=velocity, time=0))
        track.append(Message('note_off', note=note_base + note, velocity=velocity, time=duration))

# Guardar archivo
mid.save('quantum_music.mid')
print("🎶 Archivo 'quantum_music.mid' generado con éxito.")
