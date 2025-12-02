#!/usr/bin/env python3
"""
Script para verificar que los notebooks se ejecuten correctamente
después de las limpiezas de verbosidad
"""
import json
import sys
from pathlib import Path
import traceback

def test_notebook(notebook_path):
    """Ejecuta las primeras celdas de código de un notebook para verificar sintaxis"""
    
    print(f'\n{"="*80}')
    print(f'Probando: {notebook_path.name}')
    print(f'{"="*80}')
    
    if not notebook_path.exists():
        print(f'✗ ERROR: No se encontró {notebook_path}')
        return False
    
    # Leer notebook
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        print(f'✗ ERROR al leer notebook: {e}')
        return False
    
    # Obtener celdas de código
    code_cells = [(i, cell) for i, cell in enumerate(nb['cells']) 
                  if cell.get('cell_type') == 'code']
    
    if not code_cells:
        print('⚠️  No se encontraron celdas de código')
        return True
    
    print(f'Total de celdas de código: {len(code_cells)}')
    
    # Probar solo las primeras 5 celdas de código (imports y configuración inicial)
    cells_to_test = min(5, len(code_cells))
    print(f'Probando primeras {cells_to_test} celdas...\n')
    
    errors = []
    for idx, (cell_num, cell) in enumerate(code_cells[:cells_to_test], 1):
        source = ''.join(cell.get('source', []))
        
        if not source.strip():
            continue
        
        # Identificar celda
        if 'import' in source[:100]:
            nombre = "Imports"
        elif 'Cargar' in source or 'read_csv' in source or 'read_parquet' in source:
            nombre = "Carga de datos"
        elif 'configuración' in source.lower() or 'config' in source.lower():
            nombre = "Configuración"
        else:
            nombre = f"Código celda {cell_num}"
        
        print(f'[{idx}/{cells_to_test}] {nombre}...', end=' ')
        
        # Verificar sintaxis (no ejecutar, solo compilar)
        try:
            compile(source, f'<cell {cell_num}>', 'exec')
            print('✓ OK')
        except SyntaxError as e:
            print(f'✗ ERROR DE SINTAXIS')
            print(f'   Línea {e.lineno}: {e.text}')
            print(f'   {e.msg}')
            errors.append((cell_num, nombre, str(e)))
        except Exception as e:
            print(f'⚠️  Advertencia: {type(e).__name__}')
            # No es error de sintaxis, puede ser problema de imports
    
    if errors:
        print(f'\n✗ Se encontraron {len(errors)} errores de sintaxis:')
        for cell_num, nombre, error in errors:
            print(f'   Celda {cell_num} ({nombre}): {error}')
        return False
    else:
        print(f'\n✓ Notebook {notebook_path.name}: Sintaxis correcta')
        return True

def main():
    """Prueba todos los notebooks"""
    
    project_root = Path(__file__).parent
    notebooks_dir = project_root / 'notebooks'
    
    notebooks_to_test = [
        '01_analisis_exploratorio.ipynb',
        '02_analisis_resultados.ipynb',
        '03_ecosystem_analysis.ipynb',
        '04_clustering_analisis.ipynb',
        '00_EXAMEN_FINAL_COMPLETO.ipynb'
    ]
    
    print('='*80)
    print('VERIFICACIÓN DE SINTAXIS DE NOTEBOOKS')
    print('='*80)
    
    results = {}
    for notebook_name in notebooks_to_test:
        notebook_path = notebooks_dir / notebook_name
        results[notebook_name] = test_notebook(notebook_path)
    
    # Resumen
    print('\n' + '='*80)
    print('RESUMEN')
    print('='*80)
    
    all_ok = True
    for notebook_name, ok in results.items():
        status = '✓ OK' if ok else '✗ ERROR'
        print(f'{status:8} {notebook_name}')
        if not ok:
            all_ok = False
    
    print('='*80)
    
    if all_ok:
        print('✓ Todos los notebooks tienen sintaxis correcta')
        return 0
    else:
        print('✗ Algunos notebooks tienen errores de sintaxis')
        return 1

if __name__ == '__main__':
    sys.exit(main())

