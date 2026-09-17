import psycopg2
import uuid
import re

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

LOTES_NUEVOS_RUFE = [
    {
        "num_formulario": "1331", "corregimiento": "Uribe", "prioridad": "ALTA",
        "observaciones_evaluador": "Lasso Zapata Carolina - Nivel de afectación grave (RDE-1331)[cite: 69].",
        "personas": [
            {"nombre": "Carolina Lasso Zapata", "doc": "31484407", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1332", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Fernandez Garcia Leiver Dario - Nivel de afectación crítica (RDE-1332)[cite: 69].",
        "personas": [
            {"nombre": "Leiver Dario Fernandez Garcia", "doc": "1118296663", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1333", "corregimiento": "Guacandá", "prioridad": "ALTA",
        "observaciones_evaluador": "Food and Drink Boachica - Nivel de afectación grave (RDE-1333)[cite: 69].",
        "personas": [
            {"nombre": "Food and Drink Boachica", "doc": "374433602", "fecha": "01/01/1985", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1334", "corregimiento": "San Vicente", "prioridad": "MEDIA",
        "observaciones_evaluador": "Industria Satecol S.A. - Verificado sin clasificación (RDE-1334)[cite: 69].",
        "personas": [
            {"nombre": "Industria Satecol S.A.", "doc": "890324299", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1335", "corregimiento": "Cali / Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "JAD Arredondo S.A.S. - Nivel de afectación moderada (RDE-1335)[cite: 69].",
        "personas": [
            {"nombre": "JAD Arredondo S.A.S.", "doc": "901216553", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1336", "corregimiento": "Santa Inés", "prioridad": "ALTA",
        "observaciones_evaluador": "Café Mashman Artesanal / Yolanda Muñoz - Unidad productiva afectada (RDE-1336)[cite: 69].",
        "personas": [
            {"nombre": "Yolanda Muñoz", "doc": "1081592974", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1337", "corregimiento": "San Nicolás", "prioridad": "ALTA",
        "observaciones_evaluador": "MedGroup - Nivel de afectación grave (RDE-1337)[cite: 72].",
        "personas": [{"nombre": "MedGroup", "doc": "1118310556", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1338", "corregimiento": "Vía Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Asociación de Usuarios Acueducto El Paraíso - Nivel de afectación moderada (RDE-1338)[cite: 72].",
        "personas": [{"nombre": "Acueducto El Paraíso", "doc": "900795386", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1339", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Otalvaro Rivera Brayan Steevens - Nivel de afectación grave (RDE-1339)[cite: 72].",
        "personas": [{"nombre": "Brayan Steevens Otalvaro Rivera", "doc": "1118303437", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1340", "corregimiento": "Manga Vieja", "prioridad": "ALTA",
        "observaciones_evaluador": "Roncancio Velosa Claudia Patricia / Finca la Alborada - Nivel de afectación crítica (RDE-1340)[cite: 70].",
        "personas": [{"nombre": "Claudia Patricia Roncancio Velosa", "doc": "51959168", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1341", "corregimiento": "Rafael Uribe Uribe", "prioridad": "ALTA",
        "observaciones_evaluador": "Cuaresmeros, Bizcochuelos y Suspiros 'Elsy' - Nivel de afectación crítica (RDE-1341)[cite: 70].",
        "personas": [{"nombre": "Cuaresmeros Elsy", "doc": "6548393", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1342", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "THR Logística S.A.S. - Nivel de afectación moderada (RDE-1342)[cite: 70].",
        "personas": [{"nombre": "THR Logística S.A.S.", "doc": "800025617", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1343", "corregimiento": "Portal de Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "D'Casta Empanadas - Nivel de afectación grave (RDE-1343)[cite: 70].",
        "personas": [{"nombre": "D'Casta Empanadas", "doc": "16797851", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1344", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Innova Quimicas AS - Nivel de afectación crítica (RDE-1344)[cite: 70].",
        "personas": [{"nombre": "Innova Quimicas AS", "doc": "900772179", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1345", "corregimiento": "Miravalle Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Amaya Reyes Alberto - Nivel de afectación grave (RDE-1345)[cite: 70].",
        "personas": [{"nombre": "Alberto Amaya Reyes", "doc": "19468985", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1346", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Mejía Elejalde Silvia Juliana - Nivel de afectación moderada (RDE-1346)[cite: 70].",
        "personas": [{"nombre": "Silvia Juliana Mejía Elejalde", "doc": "38893682", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1347", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Carpas IWF Cali S.A.S. - Nivel de afectación baja (RDE-1347)[cite: 70].",
        "personas": [{"nombre": "Carpas IWF Cali S.A.S.", "doc": "901308345", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1348", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Soluciones Deportivas Masters S.A.S. - Nivel de afectación crítica (RDE-1348)[cite: 70].",
        "personas": [{"nombre": "Soluciones Deportivas Masters S.A.S.", "doc": "902034935", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1349", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "De Pura Madre Taquería Dapa S.A.S. - Nivel de afectación crítica (RDE-1349)[cite: 70].",
        "personas": [{"nombre": "De Pura Madre Taquería Dapa S.A.S.", "doc": "901829548", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1350", "corregimiento": "Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Cardona Rodriguez Monica - Nivel de afectación moderada (RDE-1350)[cite: 70].",
        "personas": [{"nombre": "Monica Cardona Rodriguez", "doc": "1118306067", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1351", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "SI S.A.S. - Nivel de afectación grave (RDE-1351)[cite: 71].",
        "personas": [{"nombre": "SI S.A.S.", "doc": "890301753", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1352", "corregimiento": "Miravalle Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Sierra Pelaez Paola Andrea - Nivel de afectación moderada (RDE-1352)[cite: 71].",
        "personas": [{"nombre": "Paola Andrea Sierra Pelaez", "doc": "107034292", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1353", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Gomez Prado Leidy Alexandra - Sin clasificación (RDE-1353)[cite: 71].",
        "personas": [{"nombre": "Leidy Alexandra Gomez Prado", "doc": "34327689", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1354", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Balanta Mina Elmar - Nivel de afectación grave (RDE-1354)[cite: 71].",
        "personas": [{"nombre": "Elmar Balanta Mina", "doc": "16464842", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1355", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Venetto Ind S.A.S. - Nivel de afectación crítica (RDE-1355)[cite: 71].",
        "personas": [{"nombre": "Venetto Ind S.A.S.", "doc": "901859532", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1356", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Ferplasticos SAS - Nivel de afectación moderada (RDE-1356)[cite: 71].",
        "personas": [{"nombre": "Ferplasticos SAS", "doc": "890318231", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1357", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Coisas Industrias SAS - Cielos acabados PVC - Nivel de afectación crítica (RDE-1357)[cite: 71].",
        "personas": [{"nombre": "Coisas Industrias SAS", "doc": "901321856", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1358", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Teppack S.A.S. - Nivel de afectación moderada (RDE-1358)[cite: 71].",
        "personas": [{"nombre": "Teppack S.A.S.", "doc": "901523536", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1359", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Vargas Murcia Eliana - Sin clasificación (RDE-1359)[cite: 71].",
        "personas": [{"nombre": "Eliana Vargas Murcia", "doc": "31476144", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1360", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Establecimiento verificado - Sin clasificación (RDE-1360)[cite: 71].",
        "personas": [{"nombre": "Establecimiento Comercial", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1361", "corregimiento": "La Laguna", "prioridad": "MEDIA",
        "observaciones_evaluador": "Beltran Baonza David Alexander - Nivel de afectación moderada (RDE-1361)[cite: 72].",
        "personas": [{"nombre": "David Alexander Beltran Baonza", "doc": "1144187942", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1362", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Asados al barril salsabor - Nivel de afectación baja (RDE-1362)[cite: 72].",
        "personas": [{"nombre": "Asados al barril salsabor", "doc": "1193125111", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1363", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Control Total & P.H. S.A.S. - Nivel de afectación grave (RDE-1363)[cite: 72].",
        "personas": [{"nombre": "Control Total & P.H. S.A.S.", "doc": "901149041", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1364", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Brújula Trips S.A.S. - Nivel de afectación grave (RDE-1364)[cite: 72].",
        "personas": [{"nombre": "Brújula Trips S.A.S.", "doc": "901555159", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1365", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Elit Yack S.A.S. - Nivel de afectación moderada (RDE-1365)[cite: 72].",
        "personas": [{"nombre": "Elit Yack S.A.S.", "doc": "902044175", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1366", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Rincon Astaiza Jessica - Nivel de afectación grave (RDE-1366)[cite: 72].",
        "personas": [{"nombre": "Jessica Rincon Astaiza", "doc": "1112101277", "fecha": "01/01/1993", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1367", "corregimiento": "Las Américas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Tiki bar - Nivel de afectación moderada (RDE-1367)[cite: 72].",
        "personas": [{"nombre": "Tiki bar", "doc": "1118290464", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1368", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inversiones Waljor Sociedad por Acciones Simplificada - Nivel de afectación moderada (RDE-1368)[cite: 72].",
        "personas": [{"nombre": "Inversiones Waljor S.A.S.", "doc": "900996731", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1369", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Establecimiento comercial verificado - Nivel de afectación grave (RDE-1369)[cite: 72].",
        "personas": [{"nombre": "Establecimiento Comercial", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1370", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "DAMIS S.A.S. - Nivel de afectación crítica (RDE-1370).",
        "personas": [{"nombre": "DAMIS S.A.S.", "doc": "900208659", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1371", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "P&CO Group S.A.S. - Nivel de afectación crítica (RDE-1371).",
        "personas": [{"nombre": "P&CO Group S.A.S.", "doc": "901956021", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1372", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Proyectar Maderas Sas - Nivel de afectación crítica (RDE-1372).",
        "personas": [{"nombre": "Proyectar Maderas Sas", "doc": "900514450", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1373", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Castillo Calle Silvia Constanza - Nivel de afectación crítica (RDE-1373).",
        "personas": [{"nombre": "Silvia Constanza Castillo Calle", "doc": "29940982", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1374", "corregimiento": "Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Granotec Colombia S.A.S. - Nivel de afectación grave (RDE-1374).",
        "personas": [{"nombre": "Granotec Colombia S.A.S.", "doc": "901397568", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1375", "corregimiento": "Cencar", "prioridad": "ALTA",
        "observaciones_evaluador": "Plexo SAS - Nivel de afectación crítica (RDE-1375).",
        "personas": [{"nombre": "Plexo SAS", "doc": "900184057", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1376", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Colombia Industrial & Automotriz S.A.S. - Nivel de afectación crítica (RDE-1376).",
        "personas": [{"nombre": "Colombia Industrial & Automotriz S.A.S.", "doc": "805011264", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1377", "corregimiento": "Buenos Aires", "prioridad": "MEDIA",
        "observaciones_evaluador": "Grisales Quintero Jose Fabian - Nivel de afectación moderada (RDE-1377).",
        "personas": [{"nombre": "Jose Fabian Grisales Quintero", "doc": "1118292898", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1378", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Comestibles M&M SAS - Nivel de afectación moderada (RDE-1378).",
        "personas": [{"nombre": "Comestibles M&M SAS", "doc": "900626909", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1379", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Asociación de Mujeres Cabeza de Familia Progresar San Marcos - Sin clasificación (RDE-1379).",
        "personas": [{"nombre": "Asociación de Mujeres Progresar", "doc": "805014770", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1380", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Tableros Electricos SAS - Nivel de afectación crítica (RDE-1380).",
        "personas": [{"nombre": "Tableros Electricos SAS", "doc": "800093443", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    }
]

def obtener_grupo_poblacional(edad):
    if edad is None: return "Sin Registro"
    if edad <= 14: return "1. Primera Infancia y Niños (0-14)"
    elif edad <= 28: return "2. Jóvenes (15-28)"
    elif edad <= 59: return "3. Adultos (29-59)"
    else: return "4. Adultos Mayores (60+)"

def calcular_edad_2026(fecha_str):
    match = re.search(r'(19\d{2}|20\d{2})', str(fecha_str))
    if match: return 2026 - int(match.group(1))
    return None

def main():
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1331-1380...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute("ALTER TABLE public.rufe_personas ADD COLUMN IF NOT EXISTS grupo_poblacional VARCHAR(50);")
        
        formularios_creados, formularios_actualizados = 0, 0
        personas_creadas, personas_actualizadas = 0, 0
        
        cur.execute("SELECT id FROM public.reportes_comunitarios LIMIT 1;")
        res_reporte = cur.fetchone()
        
        if not res_reporte:
            reporte_id = str(uuid.uuid4())
            cur.execute("INSERT INTO public.reportes_comunitarios (id, activo) VALUES (%s, true) ON CONFLICT DO NOTHING;", (reporte_id,))
        else:
            reporte_id = res_reporte[0]
            
        for form in LOTES_NUEVOS_RUFE:
            num_limpio = form["num_formulario"].lstrip('0')
            
            cur.execute("SELECT id FROM public.rufe_formularios WHERE numero_formulario = %s", (num_limpio,))
            resultado = cur.fetchone()
            
            if resultado:
                form_id = resultado[0]
                cur.execute("""
                    UPDATE public.rufe_formularios 
                    SET prioridad = %s, observaciones_evaluador = %s WHERE id = %s;
                """, (form["prioridad"], form["observaciones_evaluador"], form_id))
                formularios_actualizados += 1
            else:
                cur.execute("""
                    INSERT INTO public.rufe_formularios 
                    (reporte_id, numero_formulario, corregimiento, prioridad, observaciones_evaluador)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (reporte_id, num_limpio, form["corregimiento"], form["prioridad"], form["observaciones_evaluador"]))
                form_id = cur.fetchone()[0]
                formularios_creados += 1
                
            for p in form["personas"]:
                if p["doc"] == "0": continue
                edad_calc = calcular_edad_2026(p["fecha"])
                grupo_pob = obtener_grupo_poblacional(edad_calc)
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE REPLACE(documento_identidad, '.', '') = %s", (p["doc"],))
                res_persona = cur.fetchone()
                
                if res_persona:
                    persona_id = res_persona[0]
                    cur.execute("""
                        UPDATE public.rufe_personas 
                        SET fecha_nacimiento = %s, edad = %s, es_jefe_hogar = %s, parentesco = %s, sexo = %s, etnia = %s, grupo_poblacional = %s
                        WHERE id = %s;
                    """, (p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"], grupo_pob, persona_id))
                    personas_actualizadas += 1
                else:
                    cur.execute("""
                        INSERT INTO public.rufe_personas 
                        (rufe_formulario_id, nombre_completo, documento_identidad, fecha_nacimiento, edad, es_jefe_hogar, parentesco, sexo, etnia, grupo_poblacional)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (form_id, p["nombre"], p["doc"], p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"], grupo_pob))
                    personas_creadas += 1

        print(f"\n==================================================")
        print(f"MIGRACIÓN LOTE 1331-1380 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
