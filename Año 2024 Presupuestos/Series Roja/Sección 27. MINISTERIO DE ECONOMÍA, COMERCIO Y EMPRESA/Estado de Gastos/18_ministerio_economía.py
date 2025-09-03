import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 27. MINISTERIO DE ECONOMÍA, COMERCIO Y EMPRESA\Estado de Gastos\18_ministerio_economía.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())