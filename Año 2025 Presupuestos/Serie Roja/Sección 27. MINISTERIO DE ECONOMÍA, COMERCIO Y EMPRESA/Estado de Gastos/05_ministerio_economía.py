import pandas as pd

ruta = r"R:\Data Science TFM\Año 2025 Presupuestos\Serie Roja\Sección 27. MINISTERIO DE ECONOMÍA, COMERCIO Y EMPRESA\Estado de Gastos\05_ministerio_economía.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Reemplazar los NaN
df.fillna('', inplace=True)  # Los NaN se convierten en celdas vacías

# Mostrar las primeras filas
print(df.head())