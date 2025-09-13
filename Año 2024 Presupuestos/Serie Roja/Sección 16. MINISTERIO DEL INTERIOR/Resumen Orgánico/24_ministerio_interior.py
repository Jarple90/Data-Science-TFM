import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Serie Roja\Sección 16. MINISTERIO DEL INTERIOR\Resumen Orgánico\24_ministerio_interior.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())