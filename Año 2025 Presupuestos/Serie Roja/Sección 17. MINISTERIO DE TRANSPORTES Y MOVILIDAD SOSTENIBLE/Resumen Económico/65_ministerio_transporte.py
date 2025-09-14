import pandas as pd

ruta = r"R:\Data Science TFM\Año 2025 Presupuestos\Serie Roja\Sección 17. MINISTERIO DE TRANSPORTES Y MOVILIDAD SOSTENIBLE\Resumen Económico\65_ministerio_transporte.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Reemplazar los NaN
df.fillna('', inplace=True)  # Los NaN se convierten en celdas vacías

# Mostrar las primeras filas
print(df.head())