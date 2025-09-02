import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 18. MINISTERIO DE EDUCACIÓN, FORMACIÓN PROFESIONAL Y DEPORTES\Estado de Gastos\37_ministerio_educación.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())