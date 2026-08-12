import os

ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    c = f.read()

injected = """IconButton(
                                icon: const Icon(Icons.history_edu, color: Colors.blue),
                                tooltip: 'Trazabilidad y Ciclo de Vida',
                                onPressed: () {
                                  showDialog(
                                    context: context,
                                    barrierDismissible: false,
                                    builder: (context) => TrazabilidadDialog(reporte: reporte),
                                  );
                                },
                              ),
                              """

if injected in c:
    # 1. Detectar dónde se inyectó y removerlo temporalmente
    idx_injected = c.find(injected)
    c = c.replace(injected, "", 1)
    
    # 2. Buscar el IconButton original (el de edición) justo en esa posición
    idx_iconbutton = c.find('IconButton', max(0, idx_injected - 10))
    
    if idx_iconbutton != -1:
        # 3. Contar los paréntesis para encontrar el final exacto del botón de edición
        brackets = 0
        end_idx = -1
        started = False
        for i in range(idx_iconbutton, len(c)):
            if c[i] == '(':
                brackets += 1
                started = True
            elif c[i] == ')':
                brackets -= 1
                if started and brackets == 0:
                    end_idx = i
                    break
        
        if end_idx != -1:
            # 4. Envolver ambos botones dentro de un Row
            edit_btn = c[idx_iconbutton:end_idx+1]
            row_wrapper = f"""Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            {injected.strip()},
                            {edit_btn}
                          ],
                        )"""
            
            c = c[:idx_iconbutton] + row_wrapper + c[end_idx+1:]
            
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(c)
            print("✅ Error solucionado: Los botones se empaquetaron correctamente en un Row.")
        else:
            print("⚠️ No se pudo determinar el final del IconButton.")
    else:
        print("⚠️ No se encontró el IconButton original.")
else:
    print("⚠️ El código inyectado no se encontró. Verifica el archivo.")
