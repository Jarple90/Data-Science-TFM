import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 37. OTRAS RELACIONES FINANCIERAS CON ENTES TERRITORIALES\Resumen Orgánico\06_otras_relaciones_financieras.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())