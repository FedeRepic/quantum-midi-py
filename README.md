# quantum-midi-py
Quantum Generative Midi

# Quantum MIDI Sequencer

Este es un secuenciador MIDI generativo en tiempo real impulsado por circuitos cuánticos utilizando [Qiskit](https://qiskit.org/) y [Mido](https://mido.readthedocs.io/).

## ¿Qué hace?

- Genera secuencias de notas MIDI basadas en la salida de un circuito cuántico.
- Utiliza múltiples **qubits y puertas aleatorias** (`h`, `x`, `rz`, `swap`, `cx`) para formar combinaciones únicas.
- Ejecuta múltiples `shots` para crear **acordes o capas simultáneas**.
- Incorpora **LFOs cuánticos** para:
  - Modulación de `velocity` (intensidad) en tiempo real.
  - Variación suave de la duración de cada nota con un **LFO acumulativo**.

## Requisitos

- Python 3.8+
- loopMIDI (u otro puerto MIDI virtual)
- Instalación de dependencias:

```bash
pip install qiskit qiskit-aer mido python-rtmidi

