import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Serie Verde\ORGANISMOS AUTÓNOMOS\Resumen general por artículos y secciones del presupuesto de gastos\00_resumen_artículos.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Reemplazar los NaN
df.fillna('', inplace=True)  # Los NaN se convierten en celdas vacías

# Mostrar las primeras filas
print(df.head())