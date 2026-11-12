import pandas as pd
import hashlib
import os

def calcular_sha256(ruta_fichero):
    """Calcula el hash SHA-256 de un archivo para asegurar su integridad."""
    sha = hashlib.sha256()
    with open(ruta_fichero, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha.update(bloque)
    return sha.hexdigest()

ruta_original = "../datos/telemetria_envios.csv"
ruta_limpia = "../datos/telemetria_limpia.csv"

# 1. Verificación inicial
hash_original = calcular_sha256(ruta_original)
print(f"Hash SHA-256 original: {hash_original}")

# 2. Carga y limpieza de datos (Tratamiento de anomalías)
df = pd.read_csv(ruta_original)

# a) Eliminar registros duplicados
df_limpio = df.drop_duplicates()

# b) Eliminar valores nulos en campos clave
df_limpio = df_limpio.dropna(subset=['temp_celsius', 'peso_kg', 'destino'])

# c) Filtrar inconsistencias lógicas
df_limpio = df_limpio[df_limpio['peso_kg'] > 0]  # Filtrar pesos negativos
df_limpio = df_limpio[df_limpio['temp_celsius'] < 90]  # Filtrar lecturas anómalas (ej. 98.4°C)
df_limpio = df_limpio[df_limpio['estado_envio'] != 'DESCONOCIDO_ERROR']  # Filtrar estados no catalogados

# 3. Guardado del fichero saneado
df_limpio.to_csv(ruta_limpia, index=False)

# 4. Verificación final
hash_limpio = calcular_sha256(ruta_limpia)
print(f"Hash SHA-256 limpio: {hash_limpio}")
print(f"Registros procesados: de {len(df)} a {len(df_limpio)}")