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
        "num_formulario": "1231", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Angélica Publicidad - Daños en techo, requiere inspección técnica (RDE-1231)[cite: 77].",
        "personas": [{"nombre": "Angélica Publicidad", "doc": "31486660", "fecha": "08/08/1981", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1232", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Sandra Angie Lorena Guacaneme - Venta callejera sin daños reportados (RDE-1232).",
        "personas": [{"nombre": "Sandra Angie Lorena Guacaneme", "doc": "0", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1233", "corregimiento": "Manga Vieja", "prioridad": "BAJA",
        "observaciones_evaluador": "Rolando Castillo Ibarra - Venta de animales sin daños estructurales (RDE-1233).",
        "personas": [{"nombre": "Rolando Castillo Ibarra", "doc": "0", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1234", "corregimiento": "La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Sandra Jimenez Loaiza - Venta de helados, afectación en edificio vecino sin daños propios (RDE-1234).",
        "personas": [{"nombre": "Sandra Jimenez Loaiza", "doc": "0", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1235", "corregimiento": "Nueva Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Tatiana Ceron - Averías en pañete y piso (RDE-1235).",
        "personas": [{"nombre": "Tatiana Ceron", "doc": "0", "fecha": "01/01/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1236", "corregimiento": "Nueva Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Nadira Bravo Urbano - Sistema estructural agrietado con riesgo de colapso, mampostería comprometida (RDE-1236).",
        "personas": [{"nombre": "Nadira Bravo Urbano", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1237", "corregimiento": "Yumbillo", "prioridad": "BAJA",
        "observaciones_evaluador": "Marco Tulio Dino Becerra - Inmueble sin afectaciones estructurales (RDE-1237).",
        "personas": [{"nombre": "Marco Tulio Dino Becerra", "doc": "3224658676", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1238", "corregimiento": "Montañitas", "prioridad": "BAJA",
        "observaciones_evaluador": "Maria Fernanda Gomez - Daños menores en mampostería (RDE-1238).",
        "personas": [{"nombre": "Maria Fernanda Gomez", "doc": "11182937815", "fecha": "01/01/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1239", "corregimiento": "Uribe", "prioridad": "ALTA",
        "observaciones_evaluador": "Maria Concepción Pulido - Viga en triángulo con daño estructural en la parte posterior, parte no habitable (RDE-1239).",
        "personas": [{"nombre": "Maria Concepción Pulido", "doc": "0", "fecha": "01/01/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1240", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Diana Katerine Correa Bolaños (La cuna de las piñatas) - Comercio de piñatería sin afectación estructural (RDE-1240).",
        "personas": [{"nombre": "Diana Katerine Correa Bolaños", "doc": "1112288946", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1241", "corregimiento": "Belalcázar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Magie cosméticos / Maria Fernanda Moreno - Afectación moderada, pérdidas en productos y cerámica (RDE-1241).",
        "personas": [{"nombre": "Maria Fernanda Moreno", "doc": "29973299", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1242", "corregimiento": "Belalcázar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Abastecemos de Occidente / María Fernanda Jaramillo - Supermercado con afectación moderada en mercancía (RDE-1242).",
        "personas": [{"nombre": "María Fernanda Jaramillo", "doc": "38795761", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1243", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Alfty / Juan Carlos - Gimnasio con afectación moderada en infraestructura física (RDE-1243).",
        "personas": [{"nombre": "Juan Carlos", "doc": "0", "fecha": "01/01/1985", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1244", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Bellas Cosmética Imperio S.A.S. - Tienda de cosméticos con afectación leve (RDE-1244).",
        "personas": [{"nombre": "Bellas Cosmética Imperio S.A.S.", "doc": "9016259597", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1245", "corregimiento": "Fray Peña", "prioridad": "BAJA",
        "observaciones_evaluador": "Yenni / Garaazuloas - Litografía, sin afectaciones estructurales (RDE-1245).",
        "personas": [{"nombre": "Yenni", "doc": "0", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1246", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Beauty Cosmetic S.A.S. / Paola Andrea Paz Prado - Tienda de belleza con afectación leve de inventario (RDE-1246).",
        "personas": [{"nombre": "Beauty Cosmetic S.A.S.", "doc": "0", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1247", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Servicentro San Carlos / Lina Maria Pérez Cabrera - Venta de hidrocarburos con afectación leve (RDE-1247).",
        "personas": [{"nombre": "Servicentro San Carlos", "doc": "1118306006", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1248", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Templo de la Moda / Nackeline Perdomo - Comercialización de textiles con afectación leve (RDE-1248).",
        "personas": [{"nombre": "Nackeline Perdomo", "doc": "38641399", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1249", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Hospedaje Romances - Servicios turísticos de hospedaje sin afectaciones (RDE-1249).",
        "personas": [{"nombre": "Hospedaje Romances", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1250", "corregimiento": "Fray Peña", "prioridad": "MEDIA",
        "observaciones_evaluador": "CDA Yumbo / Lina Maria Pérez Cabrera - Revisión tecnomecánica de vehículos con afectación leve en infraestructura (RDE-1250).",
        "personas": [{"nombre": "CDA Yumbo", "doc": "1118306006", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1251", "corregimiento": "Vegas", "prioridad": "ALTA",
        "observaciones_evaluador": "Lorena Gallego - Fábrica de mazamorra, pared agrietada con riesgo para habitantes (RDE-1251).",
        "personas": [{"nombre": "Lorena Gallego", "doc": "0", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1252", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Leidy Alejandra Cardozo - Emprendimiento sin afectaciones en infraestructura (RDE-1252).",
        "personas": [{"nombre": "Leidy Alejandra Cardozo", "doc": "0", "fecha": "01/01/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1253", "corregimiento": "Bellavista", "prioridad": "BAJA",
        "observaciones_evaluador": "Alex Ordoñez - Emprendimiento sin afectaciones en infraestructura (RDE-1253).",
        "personas": [{"nombre": "Alex Ordoñez", "doc": "3206403991", "fecha": "01/01/1985", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1254", "corregimiento": "Fray Peña", "prioridad": "MEDIA",
        "observaciones_evaluador": "Serviteca Lubrilteca 15B / Jose Sander - Local con afectaciones en infraestructura, operando (RDE-1254).",
        "personas": [{"nombre": "Jose Sander", "doc": "6135738", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1255", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Juan Sebastian - Tienda local verificada (RDE-1255).",
        "personas": [{"nombre": "Juan Sebastian", "doc": "0", "fecha": "01/01/2000", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1256", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Restaurante Como En Casa / Nury Sanchez - Infraestructura con afectaciones moderadas (RDE-1256).",
        "personas": [{"nombre": "Nury Sanchez", "doc": "0", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1257", "corregimiento": "Nueva Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Negocio Primos Prince / Alexandra Bermeo - Daños en infraestructura y agrietamiento en paredes (RDE-1257).",
        "personas": [{"nombre": "Alexandra Bermeo", "doc": "3206737697", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1258", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "David Lopez - Unidad productiva sin afectaciones estructurales (RDE-1258).",
        "personas": [{"nombre": "David Lopez", "doc": "0", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1259", "corregimiento": "Buenos Aires", "prioridad": "ALTA",
        "observaciones_evaluador": "Tienda Lunad / Karime Muñoz - Daños estructurales donde está ubicada la unidad productiva (RDE-1259).",
        "personas": [{"nombre": "Karime Muñoz", "doc": "1118301647", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1260", "corregimiento": "Fray Peña", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jonathan Medabel Arnula - Taller de confección, afectación moderada (RDE-1260).",
        "personas": [{"nombre": "Jonathan Medabel Arnula", "doc": "0", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1261", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Maria Helena Ocampo Jaramillo - Grietas en piso (RDE-1261).",
        "personas": [{"nombre": "Maria Helena Ocampo Jaramillo", "doc": "3208439825", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1262", "corregimiento": "Las Américas", "prioridad": "BAJA",
        "observaciones_evaluador": "Luz Encira Aza - Grietas en paredes (RDE-1262).",
        "personas": [{"nombre": "Luz Encira Aza", "doc": "3108110514", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1263", "corregimiento": "Belalcázar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Luzr Bustamante - Daños en mercancía, requiere inspección técnica (RDE-1263).",
        "personas": [{"nombre": "Luzr Bustamante", "doc": "3162474761", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1264", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Rodriguez Cordoba - Sin observaciones críticas registradas (RDE-1264).",
        "personas": [{"nombre": "Rodriguez Cordoba", "doc": "3216151352", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1265", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Leydy Monge - Sin afectaciones estructurales, operando normalmente (RDE-1265).",
        "personas": [{"nombre": "Leydy Monge", "doc": "3128425625", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1266", "corregimiento": "Pueblo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Garcia / Jashny - Averiaciones en paredes de la unidad productiva (RDE-1266).",
        "personas": [{"nombre": "Jashny Garcia", "doc": "3134909767", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1267", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "John Calpa - Sin observaciones registradas (RDE-1267).",
        "personas": [{"nombre": "John Calpa", "doc": "3136015518", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1268", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Calzado JR / Rivera Urbano - Disminución de ventas, operando con normalidad (RDE-1268).",
        "personas": [{"nombre": "Calzado JR", "doc": "642508", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1269", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Ferre Repet Yumbo / Julio Lopez - Sin afectaciones, operando normalmente (RDE-1269).",
        "personas": [{"nombre": "Julio Lopez", "doc": "16448009", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1270", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "VIP Store / Alexis - Venta de ropa y accesorios, sin daños (RDE-1270).",
        "personas": [{"nombre": "Alexis", "doc": "1118300523", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1271", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Abastecemos Del Occidente / Angie Xiamara Velasquez - 100 empleados, sin daños estructurales (RDE-1271).",
        "personas": [{"nombre": "Angie Xiamara Velasquez", "doc": "1118305803", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1272", "corregimiento": "Belalcázar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Pink Boutique / Clavicia Marcela Gomez Duque - Afectación leve en ventas, sin daños físicos (RDE-1272).",
        "personas": [{"nombre": "Clavicia Marcela Gomez Duque", "doc": "25291839", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1273", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Mercado Santa Elena / Cesar Augusto - Daños leves en mercancía, póliza vigente (RDE-1273).",
        "personas": [{"nombre": "Cesar Augusto", "doc": "9850138", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1274", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Taller Auto al Día Yumbo / Richard Mosquera - Sin afectaciones, operando normal (RDE-1274).",
        "personas": [{"nombre": "Richard Mosquera", "doc": "16463422", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1275", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Decoceramicas Yumbo / Johnn Edward - Operando normalmente (RDE-1275).",
        "personas": [{"nombre": "Johnn Edward", "doc": "94505546", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1276", "corregimiento": "Belalcázar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Magik Cosméticos / Maria Fernanda Moreno - Afectación leve por \$800.000 en mercancía (RDE-1276).",
        "personas": [{"nombre": "Maria Fernanda Moreno", "doc": "29973299", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1277", "corregimiento": "Corfalle", "prioridad": "BAJA",
        "observaciones_evaluador": "Pipe Lava Autos - Sin daños estructurales, operando con 10 empleados (RDE-1277).",
        "personas": [{"nombre": "Pipe Lava Autos", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1278", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Sal Sí Puedes - Disminución temporal de ventas, sin daños estructurales (RDE-1278).",
        "personas": [{"nombre": "Yesenia Vandan Llanten", "doc": "1118302384", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1279", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "La Feria del Calzado / Clavicia Marcela Gomez Duque - Operando normalmente, sin daños (RDE-1279).",
        "personas": [{"nombre": "Clavicia Marcela Gomez Duque", "doc": "25291839", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1280", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "VIP Store / Alexis - Venta de ropa y accesorios, sin daños (RDE-1280).",
        "personas": [{"nombre": "Alexis", "doc": "1118300523", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1231-1280...")
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
        print(f"MIGRACIÓN LOTE 1231-1280 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
