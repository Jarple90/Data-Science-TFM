import pandas as pd

ruta = r"R:\Data Science TFM\Año 2024 Presupuestos\Serie Verde\ESTADO\Resumen general por capítulos del presupuesto de gastos\00_resumen_capítulos.CSV"
# Leer el CSV con punto y coma como separador
df = pd.read_csv(ruta, encoding="latin1", sep=";")

# Mostrar las primeras filas
print(df.head())