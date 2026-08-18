#!/bin/bash

# ============================================================
# Emergency Col SGRD - Validación de Teléfonos y Grupos
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Validación de Teléfonos y Grupos${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Función para validar teléfonos duplicados
validate_duplicates() {
    echo -e "${YELLOW}🔍 Buscando teléfonos duplicados...${NC}"
    
    ssh almofa@10.147.17.2 "docker exec db_sgrd psql -U admin_comunidad -d comunidad_db -c \"
    SELECT 
        telefono,
        COUNT(*) as total_reportes,
        STRING_AGG(id::text, ', ') as reportes_ids,
        STRING_AGG(COALESCE(datos_extra->>'ciudadano', 'Anónimo'), ' | ') as ciudadanos
    FROM (
        SELECT 
            id,
            COALESCE(datos_extra->>'telefono', '') as telefono,
            datos_extra
        FROM reportes_comunitarios
    ) t
    WHERE telefono != '' AND telefono IS NOT NULL
    GROUP BY telefono
    HAVING COUNT(*) > 1
    ORDER BY total_reportes DESC;
    \""
}

# Función para crear grupos familiares automáticamente
create_family_groups() {
    echo -e "${YELLOW}👨‍👩‍👧‍👦 Creando grupos familiares...${NC}"
    
    ssh almofa@10.147.17.2 "docker exec db_sgrd psql -U admin_comunidad -d comunidad_db -c \"
    DO \$\$
    DECLARE
        r RECORD;
        grupo_id INTEGER;
        telefono_clean VARCHAR;
    BEGIN
        -- Insertar grupos para cada teléfono único
        FOR r IN (
            SELECT DISTINCT telefono
            FROM (
                SELECT COALESCE(datos_extra->>'telefono', '') as telefono
                FROM reportes_comunitarios
                WHERE datos_extra->>'telefono' != '' 
                  AND datos_extra->>'telefono' IS NOT NULL
            ) t
            WHERE telefono != ''
        ) LOOP
            -- Limpiar teléfono (quitar espacios, guiones, etc.)
            telefono_clean := regexp_replace(r.telefono, '[^0-9]', '', 'g');
            
            -- Verificar si ya existe el grupo
            SELECT id INTO grupo_id 
            FROM grupos_familiares 
            WHERE telefono_principal = telefono_clean;
            
            IF grupo_id IS NULL THEN
                INSERT INTO grupos_familiares (telefono_principal, nombre_grupo)
                VALUES (telefono_clean, 'Familia ' || telefono_clean)
                RETURNING id INTO grupo_id;
                
                -- Asignar reportes a este grupo
                INSERT INTO reportes_grupos_familiares (reporte_id, grupo_familiar_id, telefono_usado)
                SELECT 
                    r.id,
                    grupo_id,
                    r.telefono
                FROM (
                    SELECT 
                        id,
                        COALESCE(datos_extra->>'telefono', '') as telefono
                    FROM reportes_comunitarios
                    WHERE datos_extra->>'telefono' != ''
                ) r
                WHERE regexp_replace(r.telefono, '[^0-9]', '', 'g') = telefono_clean;
            END IF;
        END LOOP;
        
        RAISE NOTICE '✅ Grupos familiares creados exitosamente';
    END \$\$;
    \""
}

# Función para verificar grupos
check_groups() {
    echo -e "${YELLOW}📊 Verificando grupos familiares...${NC}"
    
    ssh almofa@10.147.17.2 "docker exec db_sgrd psql -U admin_comunidad -d comunidad_db -c \"
    SELECT 
        gf.id,
        gf.telefono_principal,
        gf.nombre_grupo,
        COUNT(rgf.reporte_id) as total_reportes,
        STRING_AGG(
            (SELECT datos_extra->>'ciudadano' FROM reportes_comunitarios WHERE id = rgf.reporte_id), 
            ' | '
        ) as ciudadanos
    FROM grupos_familiares gf
    LEFT JOIN reportes_grupos_familiares rgf ON gf.id = rgf.grupo_familiar_id
    GROUP BY gf.id, gf.telefono_principal, gf.nombre_grupo
    HAVING COUNT(rgf.reporte_id) > 0
    ORDER BY total_reportes DESC
    LIMIT 20;
    \""
}

# Menú
echo -e "${YELLOW}Selecciona una opción:${NC}"
echo "  1) Buscar teléfonos duplicados"
echo "  2) Crear grupos familiares automáticamente"
echo "  3) Ver grupos familiares creados"
echo "  4) Todas las opciones"
echo "  5) Salir"
echo ""
read -p "Opción [1-5]: " OPCION

case $OPCION in
  1)
    validate_duplicates
    ;;
  2)
    create_family_groups
    ;;
  3)
    check_groups
    ;;
  4)
    validate_duplicates
    echo ""
    create_family_groups
    echo ""
    check_groups
    ;;
  5)
    echo -e "${GREEN}👋 Saliendo...${NC}"
    exit 0
    ;;
  *)
    echo -e "${RED}❌ Opción inválida${NC}"
    exit 1
    ;;
esac
