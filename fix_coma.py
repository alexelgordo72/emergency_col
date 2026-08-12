ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    c = f.read()

# Reemplazamos la doble coma por una sola
c = c.replace('),,', '),')

with open(ruta, 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ Doble coma eliminada correctamente de main.dart")
