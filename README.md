# quantum-midi-py
Quantum Generative MIDI

# Quantum MIDI Sequencer

This is a real-time generative MIDI sequencer powered by quantum circuits using [Qiskit](https://qiskit.org/) and [Mido](https://mido.readthedocs.io/).

## What does it do?

- Generates MIDI note sequences based on the output of a quantum circuit.
- Uses multiple **qubits and random gates** (`h`, `x`, `rz`, `swap`, `cx`) to create unique combinations.
- Runs multiple `shots` per execution to produce **chords or simultaneous layers**.
- Incorporates **quantum LFOs** for:
  - Real-time modulation of `velocity` (note intensity).
  - Smooth variation of note duration via an **accumulative LFO**.

## Quantum Circuit Features

- Each qubit receives a random gate (`h`, `x`, or `rz`) on each cycle.
- Random swaps occur between pairs of qubits.
- Some fixed entanglements are added (`cx(0,1)` and `cx(1,7)`) for deeper interaction.
- Measurement results are converted directly into MIDI notes.

## Quantum Modulation

- `get_quantum_lfo()` produces smoothly distributed random values using multiple qubits.
- `QuantumSmoothLFO` simulates a slow oscillating LFO to vary note duration dynamically.

## Requirements

- Python 3.8+
- loopMIDI (or any virtual MIDI port)
- Dependencies:

```bash
pip install qiskit qiskit-aer mido python-rtmidi
