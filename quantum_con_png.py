from qiskit import QuantumCircuit
from qiskit_aer import Aer
from PIL import Image, ImageDraw, ImageFont

# Crear circuito cuántico con 3 qubits y 3 bits clásicos
qc = QuantumCircuit(3, 3)

# Apply Hadamard gate to qubit 0
qc.h(0)

# Apply CNOT gate between qubit 0 and 1
qc.cx(0, 1)

# Measure qubits into classical bits
qc.measure(0, 0)
qc.measure(1, 1)
qc.measure(2, 2)

# Obtener el diagrama ASCII
ascii_diagram = qc.draw(output='text').__str__()

explicacion = (

"\n"
"\n"
"\n"
"# Crear circuito cuántico\n"
"# con 3 qubits y 3 bits clásicos\n"
"qc = QuantumCircuit(3, 3)\n"
"\n"
"# Apply Hadamard gate to qubit 0\n"
"qc.h(0)\n"
"\n"
"# Apply CNOT gate between qubit 0 and 1\n"
"qc.cx(0, 1)\n"
"\n"
"# Measure qubits into classical bits\n"
"qc.measure(0, 0)\n"
"qc.measure(1, 1)\n"
"qc.measure(2, 2)\n"
)

ascii_diagram = ascii_diagram + explicacion

# Imprimir en consola
print(qc)

# ────────────────────────────────
# Generar imagen tipo consola (opcional)
# ────────────────────────────────

# Configuración de imagen
lines = ascii_diagram.split('\n')
font_size = 18

# Usa una fuente monoespaciada (ajustá la ruta si es necesario)
try:
    font = ImageFont.truetype("CascadiaMono.ttf", font_size)
except:
    font = ImageFont.load_default()

# Tamaño aproximado
max_width = max(len(line) for line in lines)
img_width = max_width * (font_size // 2 + 3)
img_height = len(lines) * (font_size + 4)

# Crear imagen fondo oscuro
img = Image.new("RGB", (img_width, img_height), color=(0, 51, 102))
draw = ImageDraw.Draw(img)

# Dibujar líneas de texto
for i, line in enumerate(lines):
    draw.text((10, i * (font_size + 4)), line, font=font, fill=(173, 216, 230))

# Guardar imagen
img.save("ascii_quantum_circuit.png")

# ────────────────────────────────
# Simulación con Aer
# ────────────────────────────────

# Simulador
simulator = Aer.get_backend('qasm_simulator')

# Ejecutar 1000 veces
job = simulator.run(qc, shots=1000)
result = job.result()
counts = result.get_counts(qc)

# Mostrar resultados
print("Measurement Results:", counts)


