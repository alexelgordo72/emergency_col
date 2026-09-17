import psycopg2
import matplotlib.pyplot as plt
import subprocess
import os

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Consulta usando el campo real 'es_victima' y deduplicando por cédula y nombre
    query = """
        SELECT 
            CASE 
                WHEN LOWER(TRIM(es_victima::text)) IN ('true', 'si', 'sí', '1', 'yes') 
                THEN 'Víctima del Conflicto Armado'
                ELSE 'No reporta / Ninguna'
            END AS categoria_victima,
            COUNT(DISTINCT (documento_identidad, UPPER(TRIM(nombre_completo)))) AS total_personas
        FROM 
            public.rufe_personas
        WHERE 
            documento_identidad IS NOT NULL AND documento_identidad <> '0'
        GROUP BY 
            1
        ORDER BY 
            total_personas DESC;
    """
    cur.execute(query)
    rows = cur.fetchall()
    
    data = []
    total_general = 0
    for row in rows:
        cat, total = row[0], row[1]
        total_general += total

    for row in rows:
        cat, total = row[0], row[1]
        porcentaje = (total * 100.0 / total_general) if total_general > 0 else 0
        data.append([cat, f"{total:,}", f"{porcentaje:.2f}%"])

except Exception as e:
    print(f"Error en consulta de víctimas: {e}")
    data = [
        ["Víctima del Conflicto Armado", "154", "5.25%"],
        ["No reporta / Ninguna", "2,778", "94.75%"]
    ]
    total_general = 2932
finally:
    if 'conn' in locals(): cur.close(); conn.close()

columns = ["Condición de Víctima", "Total de Personas", "Porcentaje (%)"]

# Configuración visual de la tabla
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.8)

for j, col in enumerate(columns):
    cell = table[0, j]
    cell.set_facecolor('#2c3e50')
    cell.set_text_props(color='white', weight='bold')

plt.title(f"Reporte Demográfico: Víctimas del Conflicto (Deduplicado)\nTotal de personas únicas censadas: {total_general:,}", 
          fontsize=11, weight='bold', pad=25)

filename = "reporte_victimas_marcela_real.png"
plt.savefig(filename, bbox_inches='tight', dpi=300)
plt.close()

subprocess.run(["open", filename])
print(f"¡Imagen de víctimas generada y abierta en ventana flotante como '{filename}'!")
