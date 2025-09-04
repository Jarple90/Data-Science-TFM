import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 28. MINISTERIO DE CIENCIA, INNOVACIÓN Y UNIVERSIDADES\Estado de Gastos\43_ministerio_ciencia.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())