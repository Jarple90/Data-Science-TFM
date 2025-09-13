import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Serie Verde\ESTADO\Estructura económica de los recursos asignados a los centros gestores para cada programa de gasto\17. MINISTERIO DE TRANSPORTES Y MOVILIDAD SOSTENIBLE\00_ministerio_transporte.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Reemplazar los NaN
df.fillna('', inplace=True)  # Los NaN se convierten en celdas vacías

# Mostrar las primeras filas
print(df.head())