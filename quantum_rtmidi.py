import time
import random
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from mido import Message, open_output, get_output_names

# -------------------------------
# CONFIGURACION PRINCIPAL
# -------------------------------
PORT_NAME = 'loopMIDI Port 3'    # Nombre del puerto MIDI virtual al que se enviarán las notas
BPM = 80                         # Tempo en beats por minuto
BEAT_DURATION = 60 / BPM         # Duración de un beat en segundos
BASE_NOTE = 60                   # Nota base (C4) en notación MIDI
NUM_QUBITS = 9                   # Número de qubits en el circuito cuántico principal
NUM_BITS = 6                     # 
SHOTS = 3                        # Número de ejecuciones por circuito (genera acordes)
USE_LFO = True                   # Si True, se usa LFO cuántico para modulación de velocidad

# -------------------------------
# INICIALIZACION
# -------------------------------
simulator = Aer.get_backend('qasm_simulator')  # Backend cuántico simulado de Qiskit

# Mostrar puertos MIDI disponibles
print("Puertos MIDI disponibles:")
for name in get_output_names():
    print(f" - {name}")

# Abrir puerto MIDI especificado
midi_out = open_output(PORT_NAME)
print(f"\n🎵 Secuenciador cuántico extendido en '{PORT_NAME}'")
print("Presiona Ctrl+C para detener...\n")

# -------------------------------
# FUNCION: LFO CUÁNTICO para VELOCITY
# -------------------------------
def get_quantum_lfo(num_bits=7, mod_range=60, offset=50):
    """
    LFO cuántico: genera valores entre offset y offset + mod_range
    con resolución de num_bits (más bits = más precisión)
    """
    lfo_qc = QuantumCircuit(num_bits, num_bits)
    for i in range(num_bits):
        lfo_qc.h(i)
    lfo_qc.measure(range(num_bits), range(num_bits))
    
    result = simulator.run(lfo_qc, shots=1).result()
    bitstring = list(result.get_counts())[0].replace(" ", "")
    value = int(bitstring, 2)

    max_val = 2 ** num_bits - 1
    scaled = int((value / max_val) * mod_range)

    return offset + scaled

# -------------------------------
# CLASE: LFO acumulativo suave para DURACIÓN
# -------------------------------
class QuantumSmoothLFO:
    def __init__(self, min_val=20, max_val=400, step_size=20):
        """
        LFO cuántico acumulativo: genera una onda suave entre min_val y max_val
        """
        self.min_val = min_val
        self.max_val = max_val
        self.step_size = step_size
        self.state = (min_val + max_val) // 2
        self.simulator = Aer.get_backend('qasm_simulator')

    def step(self):
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        result = self.simulator.run(qc, shots=1).result()
        bit = list(result.get_counts())[0].replace(" ", "")

        if bit == '1':
            self.state = min(self.state + self.step_size, self.max_val)
        else:
            self.state = max(self.state - self.step_size, self.min_val)

        return self.state

# -------------------------------
# FUNCION: Crear circuito cuántico
# -------------------------------
def create_quantum_circuit():
    """
    Construye un circuito cuántico con puertas aleatorias por qubit,
    y aplica conexiones entre qubits para generar variaciones.
    """
    qc = QuantumCircuit(NUM_QUBITS, NUM_BITS)

    for i in range(NUM_QUBITS):
        gate = random.choice(["h", "x", "rz"])
        if gate == "h":
            qc.h(i)
        elif gate == "x":
            qc.x(i)
        elif gate == "rz":
            qc.rz(random.uniform(0.1, 3.14), i)

    # SWAP aleatorio entre pares
    if NUM_QUBITS >= 2 and random.random() < 0.4:
        a, b = random.sample(range(NUM_QUBITS), 2)
        qc.swap(a, b)

    # CNOTs fijos para entrelazamiento
    qc.cx(0, 1)
    qc.cx(1, 7)

    qc.measure_all()
    return qc

# -------------------------------
# LOOP PRINCIPAL DEL SECUENCIADOR
# -------------------------------
try:
    lfo_duration = QuantumSmoothLFO(min_val=50, max_val=250, step_size=random.randint(15, 25))
    print(create_quantum_circuit())  # Imprime el primer circuito como referencia

    while True:
        qc = create_quantum_circuit()
        job = simulator.run(qc, shots=SHOTS)
        result = job.result()
        counts = result.get_counts(qc)

        for bitstring, repetitions in counts.items():
            note_value = int(bitstring.replace(" ", ""), 2) % 36  # valor entre 0–35
            midi_note = BASE_NOTE + note_value                    # nota MIDI final

            for _ in range(repetitions):
                velocity = get_quantum_lfo() if USE_LFO else random.randint(60, 100)
                midi_out.send(Message('note_on', note=midi_note, velocity=velocity))
                
                dur = get_quantum_lfo() / 100  # duración variable
                time.sleep(dur)

                midi_out.send(Message('note_off', note=midi_note, velocity=velocity))

        #time.sleep(BEAT_DURATION)

except KeyboardInterrupt:
    print("\n🛑 Secuenciador detenido.")
    midi_out.close()
