import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 13. MINISTERIO DE LA PRESIDENCIA, JUSTICIA Y RELACIONES CON LA CORTE\Estado de Gastos\16_ministerio_presidencia_justicia.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())