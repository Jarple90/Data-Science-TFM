import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 29. MINISTERIO DE DERECHOS SOCIALES, CONSUMO Y AGENDA 2030\Estado de Gastos\02_ministerio_sociales.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Reemplazar los NaN
df.fillna('', inplace=True)  # Los NaN se convierten en celdas vacías

# Mostrar las primeras filas
print(df.head())