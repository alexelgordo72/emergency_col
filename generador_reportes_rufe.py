import psycopg2
import matplotlib.pyplot as plt
import subprocess

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

def generar_reporte_animales_rufe():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Consulta blindada incluyendo aves, perros, gatos y otros animales
        query = """
            SELECT 
                SUM(CASE WHEN CAST(cantidad_perros AS text) ~ '^[0-9]+$' THEN CAST(cantidad_perros AS integer) ELSE 0 END) AS total_perros,
                SUM(CASE WHEN CAST(cantidad_gatos AS text) ~ '^[0-9]+$' THEN CAST(cantidad_gatos AS integer) ELSE 0 END) AS total_gatos,
                SUM(CASE WHEN CAST(cantidad_aves AS text) ~ '^[0-9]+$' THEN CAST(cantidad_aves AS integer) ELSE 0 END) AS total_aves,
                SUM(CASE WHEN CAST(otros_animales AS text) ~ '^[0-9]+$' THEN CAST(otros_animales AS integer) ELSE 0 END) AS total_otros
            FROM 
                public.dashboard_agrupado;
        """
        cur.execute(query)
        res = cur.fetchone()
        cur.close()
        conn.close()
        
        if not res:
            print("No se encontraron datos de animales.")
            return

        total_perros, total_gatos, total_aves, total_otros = res
        total_general = total_perros + total_gatos + total_aves + total_otros
        
        data = [
            ["Perros", f"{total_perros:,}", f"{(total_perros*100.0/total_general):.2f}%" if total_general > 0 else "0%"],
            ["Gatos", f"{total_gatos:,}", f"{(total_gatos*100.0/total_general):.2f}%" if total_general > 0 else "0%"],
            ["Aves (Gallinas/Patos)", f"{total_aves:,}", f"{(total_aves*100.0/total_general):.2f}%" if total_general > 0 else "0%"],
            ["Otros Animales", f"{total_otros:,}", f"{(total_otros*100.0/total_general):.2f}%" if total_general > 0 else "0%"]
        ]

        # Generar Gráfica estilo WhatsApp
        columns = ["Especie", "Total", "Porcentaje (%)"]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis('tight')
        ax.axis('off')
        
        table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 2.2)
        
        # Estilo de cabecera verde corporativo (WhatsApp)
        for j, col in enumerate(columns):
            cell = table[0, j]
            cell.set_facecolor('#075E54')
            cell.set_text_props(color='white', weight='bold', fontsize=12)
            
        plt.title(f"Censo Completo de Animales y Mascotas - RUFE\nTotal General: {total_general:,}", fontsize=13, weight='bold', pad=15)
        
        filename = "reporte_whatsapp_animales.png"
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
        
        subprocess.run(["open", filename])
        print(f"¡Reporte completo de animales generado con éxito: {filename} (Total: {total_general})!")

    except Exception as e:
        print(f"Error generando reporte de animales: {e}")

if __name__ == "__main__":
    generar_reporte_animales_rufe()
