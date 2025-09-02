import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 09. APORTACIONES AL MUTUALISMO ADMINISTRATIVO\Resumen Económico\06_aportaciones_mutualismo_administrativo.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())