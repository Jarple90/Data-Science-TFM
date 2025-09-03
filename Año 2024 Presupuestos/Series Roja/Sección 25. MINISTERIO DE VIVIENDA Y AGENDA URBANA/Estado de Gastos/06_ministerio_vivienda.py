import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 25. MINISTERIO DE VIVIENDA Y AGENDA URBANA\Estado de Gastos\06_ministerio_vivienda.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())