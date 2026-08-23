from pymongo import MongoClient
from bson.binary import Binary
from datetime import datetime

# Conexión directa a MongoDB en tu servidor (10.147.17.2)
client = MongoClient("mongodb://10.147.17.2:27017/")
db = client["comunidad_db"]
coleccion = db["solicitudes_co_multimedia"]

# Ruta del archivo Co-1.pdf en la carpeta Descargas de tu Mac
ruta_pdf = "/Users/admin/Downloads/Co-1.pdf"

# Leer el archivo PDF en modo binario
try:
    with open(ruta_pdf, "rb") as f:
        contenido_pdf_binario = f.read()
except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta: {ruta_pdf}")
    exit()

# Construir el documento con el PDF completo incrustado
documento_mongo = {
    "mongo_document_id": "MONGO_DOC_ID_CO_001",
    "prefijo": "CO-",
    "tipo_solicitud": "Derecho de Petición",
    "datos_solicitante": {
        "nombre_completo": "Kelly Johana Mosquera Giraldo",
        "cedula": "31486655",
        "correo": "johanamosqueragir@gmail.com",
        "telefono": "3113484150"
    },
    "ubicacion": {
        "municipio": "Yumbo, Valle del Cauca",
        "sector": "Ciudad Guabinas",
        "direccion": "Carrera 18E #7-131, Conjunto Residencial Palomino, Torre 26, Apartamento 503"
    },
    "archivo_pdf_original": {
        "nombre_archivo": "Co-1.pdf",
        "tipo_contenido": "application/pdf",
        "datos_binarios": Binary(contenido_pdf_binario)
    },
    "fecha_creacion": datetime.utcnow()
}

# Insertar en MongoDB
resultado = coleccion.insert_one(documento_mongo)
print(f"¡PDF Co-1.pdf subido con éxito a MongoDB en el servidor! ID del documento: {resultado.inserted_id}")
