import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Series Roja\Sección 17. MINISTERIO DE TRANSPORTES Y MOVILIDAD SOSTENIBLE\Estado de Gastos\06_ministerio_transporte.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())