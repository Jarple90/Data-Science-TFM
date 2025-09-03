import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 24. MINISTERIO DE CULTURA\Estado de Gastos\27_ministerio_cultura.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())