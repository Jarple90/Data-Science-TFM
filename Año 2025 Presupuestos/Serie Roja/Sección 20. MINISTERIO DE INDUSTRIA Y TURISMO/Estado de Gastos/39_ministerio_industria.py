import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 20. MINISTERIO DE INDUSTRIA Y TURISMO\Estado de Gastos\39_ministerio_industria.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Reemplazar los NaN
df.fillna('', inplace=True)  # Los NaN se convierten en celdas vacías

# Mostrar las primeras filas
print(df.head())