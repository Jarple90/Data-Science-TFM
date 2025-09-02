import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 21. MINISTERIO DE AGRICULTURA, PESCA Y ALIMENTACIÓN\Estado de Gastos\21_ministerio_agricultura.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())