import psycopg2

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'rufe_personas';")
cols = [row[0] for row in cur.fetchall()]
print("Columnas disponibles en rufe_personas:")
for c in cols:
    print(f" - {c}")
cur.close()
conn.close()
