import os
import time
import pandas as pd

output_file = 'data/05_model_input/datos_para_modelado.parquet'
check_interval = 10  # seconds

print("="*70)
print("MONITOREANDO PIPELINE DE PROCESAMIENTO")
print("="*70)
print(f"\nEsperando a que se genere: {output_file}")
print(f"Chequeando cada {check_interval} segundos...")

# Get initial modification time if file exists
last_modified = os.path.getmtime(output_file) if os.path.exists(output_file) else 0

while True:
    time.sleep(check_interval)
    
    if os.path.exists(output_file):
        current_modified = os.path.getmtime(output_file)
        
        # Check if file was recently modified
        if current_modified > last_modified:
            print(f"\n✅ ¡Archivo actualizado! Verificando contenido...")
            time.sleep(2)  # Wait a bit for file write to complete
            
            try:
                df = pd.read_parquet(output_file)
                print(f"\n📊 RESULTADO:")
                print(f"   Registros: {len(df):,}")
                print(f"   Columnas: {df.shape[1]}")
                
                # Check for NaN
                nan_counts = df.isna().sum()
                columns_with_nan = nan_counts[nan_counts > 0]
                
                if len(columns_with_nan) > 0:
                    print(f"\n   ⚠️ TODAVÍA HAY NaN:")
                    for col, count in columns_with_nan.head(5).items():
                        print(f"      {col}: {count:,} NaN")
                else:
                    print(f"\n   ✅ NO HAY valores NaN - Dataset listo!")
                
                print(f"\n{'='*70}")
                print(f"Pipeline completado exitosamente")
                print(f"{'='*70}")
                break
                
            except Exception as e:
                print(f"   ⚠️ Error leyendo archivo: {e}")
                print(f"   Esperando...")
    else:
        print(".", end="", flush=True)
