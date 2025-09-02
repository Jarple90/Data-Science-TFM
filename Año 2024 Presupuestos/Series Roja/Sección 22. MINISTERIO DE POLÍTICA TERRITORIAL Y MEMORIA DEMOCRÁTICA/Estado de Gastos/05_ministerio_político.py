import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 22. MINISTERIO DE POLÍTICA TERRITORIAL Y MEMORIA DEMOCRÁTICA\Estado de Gastos\05_ministerio_político.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())