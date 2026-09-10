# -*- coding: utf-8 -*-
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import unicodedata
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def normalize(text):
    if not isinstance(text, str):
        return ""
    nfkd = unicodedata.normalize('NFKD', text)
    no_accent = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return no_accent.lower().strip()

def obtener_conexion():
    return psycopg2.connect(
        host="postgres",
        database="comunidad_db",
        user="admin_comunidad",
        password="TuPasswordSegura2026!"
    )

def generar_reporte_pdf():
    # 1. Cargar URBANA.xlsx para obtener el orden oficial de 1 a 21
    excel_path = "URBANA.xlsx"
    df_excel = pd.read_excel(excel_path)
    df_excel = df_excel.dropna(subset=['id'])
    
    excel_order = {}
    for idx, row in df_excel.iterrows():
        b_name = str(row['barrios por visitar']).strip()
        b_id = int(row['id'])
        excel_order[normalize(b_name)] = (b_id, b_name.upper())

    def get_order_and_name(sector_barrio):
        if not sector_barrio:
            return 999, "ZONA RURAL / OTROS"
        norm = normalize(sector_barrio)
        
        for b_norm, (b_id, b_orig_upper) in excel_order.items():
            if b_norm == norm:
                return b_id, b_orig_upper
                
        for b_norm, (b_id, b_orig_upper) in excel_order.items():
            if b_norm in norm or norm in b_norm:
                return b_id, b_orig_upper
                
        # Coincidencias estrictas basadas en URBANA.xlsx
        if 'las vegas' in norm: return 1, "LAS VEGAS"
        if 'madrigal' in norm: return 2, "MADRIGAL"
        if 'bellavista' in norm: return 3, "BELLAVISTA"
        if 'fray' in norm: return 4, "FRAY PEÑA"
        if 'lleras' in norm: return 5, "LLERAS"
        if 'pizarro' in norm: return 6, "PIZARRO"
        if 'guadalupe' in norm: return 7, "GUADALUPE"
        if 'bolivar' in norm: return 8, "BOLÍVAR"
        if 'uribe' in norm: return 9, "URIBE"
        if 'buenos aires' in norm: return 10, "BUENOS AIRES"
        if 'belalcazar' in norm: return 11, "BELALCÁZAR"
        if 'orizonte' in norm or 'horizonte' in norm: return 12, "NUEVO ORIZONTE"
        if 'pedregal' in norm: return 13, "PEDREGAL"
        if 'trinidad' in norm: return 14, "TRINIDAD"
        if 'campestre' in norm: return 15, "CAMPESTRE REAL"
        if 'dionisio' in norm or 'dionicio' in norm: return 16, "DIONISIO"
        if 'finlandia' in norm or 'finalandia' in norm: return 17, "FINLANDIA"
        if 'estancia' in norm or 'estacia' in norm: return 18, "LA ESTANCIA"
        if 'america' in norm: return 19, "AMÉRICAS"
        if 'guabinas' in norm: return 20, "GUABINAS"
        if 'panorama' in norm: return 21, "PANORAMA"
        
        return 999, sector_barrio.upper()

    # 2. Conectar a PostgreSQL y obtener registros SIN ORDENAR EN SQL
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT sector_barrio, titulo, direccion_referencia, datos_extra, fecha_creacion
        FROM reportes_comunitarios
    """)
    registros = cursor.fetchall()
    cursor.close()
    conn.close()

    # 3. Agrupar en Python asignando su ID oficial numérico
    grupos = {}
    for r in registros:
        b_id, b_name_upper = get_order_and_name(r['sector_barrio'])
        key = (int(b_id), b_name_upper)
        if key not in grupos:
            grupos[key] = []
        grupos[key].append(r)

    # 4. ORDENAR ESTRICTAMENTE EN PYTHON POR ID NUMÉRICO ASCENDENTE (1, 2, ... 21, 999)
    sorted_keys = sorted(grupos.keys(), key=lambda x: x[0])

    print("=== ORDEN DE SECCIONES APLICADO EN EL PDF ===")
    for b_id, b_name in sorted_keys:
        print(f"ID {b_id}: {b_name} ({len(grupos[(b_id, b_name)])} visitas)")

    # 5. Construcción del PDF con ReportLab
    pdf_filename = "ruta_visitas_sgrd.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=30, leftMargin=30,
        topMargin=30, bottomMargin=30
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    titulo_style = ParagraphStyle(
        'TituloRuta', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#B71C1C'), spaceAfter=6, alignment=1
    )
    subtitulo_style = ParagraphStyle(
        'SubTituloRuta', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#555555'), spaceAfter=15, alignment=1
    )
    barrio_header_style = ParagraphStyle(
        'BarrioHeader', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#FFFFFF')
    )
    celda_style = ParagraphStyle(
        'CeldaTexto', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#333333')
    )
    celda_bold = ParagraphStyle(
        'CeldaBold', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Bold', textColor=colors.HexColor('#111111')
    )

    story.append(Paragraph("SGRD YUMBO - PLANILLA DE RUTA DE VISITAS", titulo_style))
    story.append(Paragraph("Ordenado estrictamente por Clasificación Oficial (URBANA.xlsx)", subtitulo_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#B71C1C'), spaceAfter=15))

    for b_id, nombre_barrio in sorted_keys:
        items = grupos[(b_id, nombre_barrio)]
        orden_label = f" [ID: {b_id}]" if b_id != 999 else " [ZONA RURAL / OTROS]"
        titulo_texto = f"<b>BARRIO / SECTOR: {nombre_barrio}{orden_label}</b> ({len(items)} Visitas)"
        
        tabla_barrio_titulo = Table([[Paragraph(titulo_texto, barrio_header_style)]], colWidths=[550])
        tabla_barrio_titulo.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#D32F2F')),
            ('PADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(tabla_barrio_titulo)
        story.append(Spacer(1, 4))

        data_tabla = [[
            Paragraph('<b>Asunto / Novedad</b>', celda_bold),
            Paragraph('<b>Dirección / Referencia</b>', celda_bold),
            Paragraph('<b>Ciudadano Afectado</b>', celda_bold),
            Paragraph('<b>Teléfono</b>', celda_bold),
            Paragraph('<b>Estado</b>', celda_bold)
        ]]

        for item in items:
            extra = item['datos_extra'] or {}
            ciudadano = extra.get('ciudadano', 'Anónimo')
            telefono = extra.get('telefono', 'N/A')
            
            data_tabla.append([
                Paragraph(item['titulo'], celda_style),
                Paragraph(item['direccion_referencia'] or 'S/D', celda_style),
                Paragraph(ciudadano, celda_style),
                Paragraph(telefono, celda_style),
                Paragraph('[   ] Pendiente', celda_style)
            ])

        t = Table(data_tabla, colWidths=[120, 110, 110, 100, 110])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FFCDD2')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

    doc.build(story)
    print("¡PDF generado y ordenado perfectamente por ID de URBANA.xlsx!")

if __name__ == "__main__":
    generar_reporte_pdf()
