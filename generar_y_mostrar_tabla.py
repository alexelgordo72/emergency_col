import matplotlib.pyplot as plt
import subprocess
import os

# Datos limpios y validados para Marcela
data = [
    ["Sin pertenencia étnica / No reporta", "2,887", "99.14%"],
    ["Afrocolombiano(a)", "22", "0.76%"],
    ["Indígena", "2", "0.07%"],
    ["Raizal", "1", "0.03%"]
]
columns = ["Pertenencia Étnica", "Total de Personas", "Porcentaje (%)"]

# Configuración de la figura y diseño estético
fig, ax = plt.subplots(figsize=(9, 3.8))
ax.axis('tight')
ax.axis('off')

# Crear la tabla visual
table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 1.8)

# Estilizar encabezados con color profesional
for j, col in enumerate(columns):
    cell = table[0, j]
    cell.set_facecolor('#2c3e50')
    cell.set_text_props(color='white', weight='bold')

# Título del reporte
plt.title("Reporte Demográfico: Distribución de la Población por Pertenencia Étnica\nTotal de personas únicas censadas (sin duplicados): 2,912", 
          fontsize=12, weight='bold', pad=25)

# Guardar temporalmente en disco
filename = "reporte_etnias_marcela.png"
plt.savefig(filename, bbox_inches='tight', dpi=300)
plt.close()

# Abrir automáticamente en la ventana por defecto de macOS
subprocess.run(["open", filename])
print(f"¡Imagen generada y abierta en una ventana flotante como '{filename}'!")
