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
        "num_formulario": "991", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Comestibles MYH SAS - No puede operar, 11 a 50 trabajadores, situación crítica (RDE-991)[cite: 62].",
        "personas": [{"nombre": "Comestibles MYH SAS", "doc": "900626909", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "992", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Comercial de aluminio vidrios Espinosa - 2 a 5 trabajadores, afectación moderada (RDE-992)[cite: 63].",
        "personas": [{"nombre": "Comercial de Aluminio Vidrios Espinosa", "doc": "6531265", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "993", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Conbutotal y P.H. SAS - 6 a 10 trabajadores, daño grave en infraestructura (RDE-993)[cite: 63].",
        "personas": [{"nombre": "Conbutotal y P.H. SAS", "doc": "9001149041", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "994", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "CIAY S.A. - 51 a 200 trabajadores, daños graves en infraestructura y maquinaria (RDE-994)[cite: 63].",
        "personas": [{"nombre": "CIAY S.A.", "doc": "805016105", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "995", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Conde Murillo Edilmer - 2 a 5 trabajadores, afectación moderada (RDE-995).",
        "personas": [{"nombre": "Edilmer Conde Murillo", "doc": "16637236", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "996", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Centro Medico de Yumbo Limitada - 11 a 50 trabajadores, daños moderados (RDE-996).",
        "personas": [{"nombre": "Centro Medico de Yumbo Limitada", "doc": "800189588", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "997", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Cerdos del Valle - Más de 200 trabajadores, afectación moderada (RDE-997)[cite: 64].",
        "personas": [{"nombre": "Cerdos del Valle", "doc": "805018495", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "998", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Centro Eventos y hostelería Casona Blanca - 5 trabajadores, no puede operar (RDE-998)[cite: 64].",
        "personas": [{"nombre": "Casona Blanca", "doc": "979040900", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "999", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Bituvial SAS - 6 a 10 trabajadores, afectación moderada (RDE-999)[cite: 64].",
        "personas": [{"nombre": "Bituvial SAS", "doc": "900531654", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1000", "corregimiento": "Arroyohondo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Asociación de micro y medianas empresas seccional valle del cauca - 2 a 95 empleados (RDE-1000)[cite: 64].",
        "personas": [{"nombre": "Asociación Valle del Cauca", "doc": "890300228", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1001", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Cafeteria Rincon Viajero - 6 a 10 trabajadores, daños en infraestructura y equipos (RDE-1001).",
        "personas": [{"nombre": "Cafeteria Rincon Viajero", "doc": "87718232", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1002", "corregimiento": "Parques del Pinar", "prioridad": "BAJA",
        "observaciones_evaluador": "Artesanía Iku - inventarios o mercancía afectada (RDE-1002).",
        "personas": [{"nombre": "Artesanía Iku", "doc": "31913378", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1003", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Establecimiento comercial - Más de 200 trabajadores, reducción de clientes (RDE-1003)[cite: 63].",
        "personas": [{"nombre": "Comercial Yumbo", "doc": "800157508", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1004", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Cosas industriales SAS - 51 a 200 trabajadores, daños en infraestructura y maquinaria (RDE-1004)[cite: 63].",
        "personas": [{"nombre": "Cosas industriales SAS", "doc": "901321856", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1005", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "DAMIS S.A.S. - 51 a 200 trabajadores, daños estructurales graves (RDE-1005)[cite: 64].",
        "personas": [{"nombre": "DAMIS S.A.S.", "doc": "900208659", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1006", "corregimiento": "Miravalle Norte", "prioridad": "ALTA",
        "observaciones_evaluador": "Silvia Constanta Castillo Calle - 2 a 5 trabajadores, no puede operar, crítico (RDE-1006).",
        "personas": [{"nombre": "Silvia Constanta Castillo Calle", "doc": "29940982", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1007", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Yuliana Balanta - 11 a 50 trabajadores, afectación locativa grave (RDE-1007).",
        "personas": [{"nombre": "Yuliana Balanta", "doc": "901641980", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1008", "corregimiento": "Alta Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Refugio Corazones Verdes - 1 trabajador, daños entre 5 y 20 millones (RDE-1008).",
        "personas": [{"nombre": "Refugio Corazones Verdes", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1009", "corregimiento": "Mulaló", "prioridad": "MEDIA",
        "observaciones_evaluador": "Rapitienda el lago - Afectación moderada, daños en infraestructura (RDE-1009).",
        "personas": [{"nombre": "Rapitienda el lago", "doc": "29940145", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1010", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Rincon del Sabor Cocina tradicional y ancestral - 1 a 5 personas, operación parcial (RDE-1010).",
        "personas": [{"nombre": "Rincon del Sabor", "doc": "1088589028", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1011", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Protecnica Ingenieria S.A.S. - Pérdidas superiores a 100 millones, afectación grave (RDE-1011)[cite: 64].",
        "personas": [{"nombre": "Protecnica Ingenieria S.A.S.", "doc": "890312630", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1012", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Productos Varios Produvarios S.A. - Operación parcial, afectación moderada (RDE-1012).",
        "personas": [{"nombre": "Productos Varios Produvarios S.A.", "doc": "890305586", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1013", "corregimiento": "El Pedregal", "prioridad": "MEDIA",
        "observaciones_evaluador": "Rancho Dos Años - Pérdidas entre 5 y 20 millones, afectación moderada (RDE-1013).",
        "personas": [{"nombre": "Rancho Dos Años", "doc": "1107845715", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1014", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Restaurante los manzanos - Pérdidas entre 5 y 20 millones, afectación moderada (RDE-1014).",
        "personas": [{"nombre": "Restaurante los manzanos", "doc": "1079684038", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1015", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Servi-Produc - Escombros sobre maquinaria de coser, no puede operar (RDE-1015).",
        "personas": [{"nombre": "Servi-Produc", "doc": "902061000", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1016", "corregimiento": "Santa Ines", "prioridad": "MEDIA",
        "observaciones_evaluador": "Tienda Emma - 1 a 5 empleados, operación parcial, pérdidas menores a 5 millones (RDE-1016).",
        "personas": [{"nombre": "Tienda Emma", "doc": "31487282", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1017", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Soluciones Mahecha S.A.S. - Pérdidas entre 5 y 20 millones, afectación crítica (RDE-1017).",
        "personas": [{"nombre": "Soluciones Mahecha S.A.S.", "doc": "902634935", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1018", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Inversiones Walter S.A.S. - Pérdidas superiores a 100 millones, afectación grave (RDE-1018).",
        "personas": [{"nombre": "Inversiones Walter S.A.S.", "doc": "8000996731", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1019", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Sierra Pelaez - Operación normal, pérdidas menores a 5 millones (RDE-1019).",
        "personas": [{"nombre": "Sierra Pelaez", "doc": "4107034292", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1020", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Espinosa Ramos S.A.S. - Pérdidas entre 5 y 20 millones, afectación moderada (RDE-1020).",
        "personas": [{"nombre": "Espinosa Ramos S.A.S.", "doc": "901523536", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1021", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Distribuidora de Suministros S.A.S. - Pérdidas entre 20 y 100 millones, afectación crítica (RDE-1021)[cite: 65].",
        "personas": [{"nombre": "Distribuidora de Suministros S.A.S.", "doc": "830111877", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1022", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Distribuidora la Costa S.A. - Pérdidas superiores a 100 millones, afectación grave (RDE-1022).",
        "personas": [{"nombre": "Distribuidora la Costa S.A.", "doc": "805010752", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1023", "corregimiento": "Lleras Camargo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Emergency Group - Pérdidas menores a 5 millones, operación parcial (RDE-1023).",
        "personas": [{"nombre": "Emergency Group", "doc": "16463698", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1024", "corregimiento": "Miravalle", "prioridad": "MEDIA",
        "observaciones_evaluador": "Dimensión Física S.A.S. - Pérdidas entre 5 y 20 millones, afectación moderada (RDE-1024).",
        "personas": [{"nombre": "Dimensión Física S.A.S.", "doc": "902634935", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1025", "corregimiento": "Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Granotes Colombia S.A.S. - Pérdidas superiores a 100 millones, afectación grave (RDE-1025).",
        "personas": [{"nombre": "Granotes Colombia S.A.S.", "doc": "901397568", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1026", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Gloriventas A - Pérdidas superiores a 100 millones, afectación grave (RDE-1026)[cite: 65].",
        "personas": [{"nombre": "Gloriventas A", "doc": "890319112", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1027", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "FERPlasticos S.A. - Pérdidas entre 20 y 100 millones, afectación moderada (RDE-1027).",
        "personas": [{"nombre": "FERPlasticos S.A.", "doc": "890318231", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1028", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Leiver / Doode Leiver - Pérdidas entre 5 y 20 millones, afectación moderada (RDE-1028).",
        "personas": [{"nombre": "Doode Leiver", "doc": "3207754751", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1029", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Gomez Paula Leidy Alexandra - Pérdidas menores a 5 millones, afectación moderada (RDE-1029).",
        "personas": [{"nombre": "Gomez Paula Leidy Alexandra", "doc": "34327689", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1030", "corregimiento": "Guadubas", "prioridad": "BAJA",
        "observaciones_evaluador": "Equipos, Proyectos y Mantenimientos - Inmueble verificado con prioridad baja (RDE-1030).",
        "personas": [{"nombre": "Equipos, Proyectos y Mantenimientos", "doc": "901087847", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1031", "corregimiento": "Vegas", "prioridad": "ALTA",
        "observaciones_evaluador": "Angie - Daños a infraestructura y maquinaria, nivel de afectación grave (RDE-1031)[cite: 66].",
        "personas": [{"nombre": "Angie", "doc": "1151947949", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1032", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "El rey de las arepas - Pérdidas entre 5 y 20 millones, operación parcial (RDE-1032)[cite: 66].",
        "personas": [{"nombre": "El rey de las arepas", "doc": "16747848", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1033", "corregimiento": "Vegas", "prioridad": "MEDIA",
        "observaciones_evaluador": "D.M. - Pérdidas menores a 5 millones, operación normal (RDE-1033)[cite: 66].",
        "personas": [{"nombre": "D.M.", "doc": "1111111111", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1034", "corregimiento": "Parque Logistico Empicor", "prioridad": "BAJA",
        "observaciones_evaluador": "Datecsa S.A. - Más de 200 empleados, operación normal (RDE-1034)[cite: 66].",
        "personas": [{"nombre": "Datecsa S.A.", "doc": "800136505", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1035", "corregimiento": "Las Cruces", "prioridad": "MEDIA",
        "observaciones_evaluador": "EDE Comunicaciones - Microempresa, daños en infraestructura (RDE-1035)[cite: 66].",
        "personas": [{"nombre": "EDE Comunicaciones", "doc": "901790097", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1036", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Elit Jack S.A.S. - 2 a 5 trabajadores, pérdidas menores a 5 millones (RDE-1036)[cite: 66].",
        "personas": [{"nombre": "Elit Jack S.A.S.", "doc": "902044175", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1037", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "De Pural Ladreria Parda S.A.S. - Pérdidas entre 20 y 100 millones, afectación crítica (RDE-1037)[cite: 66].",
        "personas": [{"nombre": "De Pural Ladreria Parda S.A.S.", "doc": "901829548", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1038", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Cocina y Tradición - 1 empleado, pérdidas menores a 5 millones (RDE-1038)[cite: 66].",
        "personas": [{"nombre": "Cocina y Tradición", "doc": "31476144", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1039", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Centro Skipe - 6 a 10 empleados, pérdidas entre 20 y 100 millones (RDE-1039)[cite: 66].",
        "personas": [{"nombre": "Centro Skipe", "doc": "7254955", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1040", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Vidrios de Occidente - 11 a 50 trabajadores, pérdidas superiores a 100 millones (RDE-1040)[cite: 66].",
        "personas": [{"nombre": "Vidrios de Occidente", "doc": "890311168", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1047", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Grupo It Global S.A.S. - Pequeña empresa con afectaciones moderadas (RDE-1047)[cite: 67].",
        "personas": [{"nombre": "Grupo It Global S.A.S.", "doc": "890302180", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1051", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Verde Vital - 1 trabajador, pérdidas menores a 5 millones (RDE-1051)[cite: 68].",
        "personas": [{"nombre": "Verde Vital", "doc": "1118305951", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1052", "corregimiento": "Cencar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Cencar S.A.S. - Vidrios y accesorios, 6 a 10 trabajadores, pérdidas entre 5 y 20 millones (RDE-1052)[cite: 68].",
        "personas": [{"nombre": "Cencar S.A.S.", "doc": "901881380", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1053", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Aura Myriam Zuñiga Calvoche - Pérdidas menores a 5 millones (RDE-1053)[cite: 68].",
        "personas": [{"nombre": "Aura Myriam Zuñiga Calvoche", "doc": "34639087", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1054", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Zlomara Villana Maldonado - 2 a 5 trabajadores, pérdidas menores a 5 millones (RDE-1054)[cite: 68].",
        "personas": [{"nombre": "Zlomara Villana Maldonado", "doc": "1144201246", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1055", "corregimiento": "Santa Ines", "prioridad": "MEDIA",
        "observaciones_evaluador": "Tunstions S.A.S. - Microempresa, 2 a 5 trabajadores, pérdidas menores a 5 millones (RDE-1055)[cite: 68].",
        "personas": [{"nombre": "Tunstions S.A.S.", "doc": "901829548", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1056", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Tunstions S.A.S. (Sucursal) - 6 a 10 trabajadores, pérdidas entre 20 y 100 millones (RDE-1056)[cite: 68].",
        "personas": [{"nombre": "Tunstions S.A.S. (Sucursal)", "doc": "901829548", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1057", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Rodolfo Ussa Garcia - Microempresa, 2 a 5 trabajadores, pérdidas menores a 5 millones (RDE-1057)[cite: 68].",
        "personas": [{"nombre": "Rodolfo Ussa Garcia", "doc": "94468438", "fecha": "01/01/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1058", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "WN Impresores S.A. - Mediana empresa, 51 a 200 trabajadores, pérdidas entre 20 y 100 millones (RDE-1058)[cite: 68].",
        "personas": [{"nombre": "WN Impresores S.A.", "doc": "805001509", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1059", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Venetto Ind S.A.S. - Pequeña empresa, 11 a 50 trabajadores, pérdidas superiores a 100 millones (RDE-1059)[cite: 68].",
        "personas": [{"nombre": "Venetto Ind S.A.S.", "doc": "901859532", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1060", "corregimiento": "Cencar", "prioridad": "ALTA",
        "observaciones_evaluador": "Transportes Especializados RTP Ltda - Mediana empresa, 11 a 50 trabajadores, pérdidas superiores a 100 millones (RDE-1060)[cite: 68].",
        "personas": [{"nombre": "Transportes Especializados RTP Ltda", "doc": "8913045980", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 991-1060...")
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
        print(f"MIGRACIÓN LOTE 991-1060 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
