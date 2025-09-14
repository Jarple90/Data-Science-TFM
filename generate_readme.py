import os
import pkg_resources

# 📁 Carpeta raíz del proyecto
project_root = "Data Science TFM"

# 🔧 Asegurarse de que la carpeta existe
os.makedirs(project_root, exist_ok=True)

# 📂 Subcarpetas clave
modules_dir = os.path.join(project_root, "modules")
data_dir = os.path.join(project_root, "data")
models_dir = os.path.join(project_root, "models")

# 📦 Extraer dependencias instaladas
dependencies = sorted([
    f"- {pkg.project_name}=={pkg.version}"
    for pkg in pkg_resources.working_set
])

# 📂 Listar archivos .py en carpetas clave
def list_py_files(folder):
    if not os.path.exists(folder):
        return []
    return [f"- `{os.path.relpath(os.path.join(folder, f), project_root)}`"
            for f in os.listdir(folder) if f.endswith(".py")]

modules_list = list_py_files(modules_dir)
models_list = list_py_files(models_dir)

# 📁 Escanear todos los archivos relevantes
def scan_all_files(root):
    file_list = []
    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if file.endswith((".py", ".csv", ".md", ".ipynb", ".docx", ".pdf")):
                rel_path = os.path.relpath(os.path.join(dirpath, file), root)
                file_list.append(f"- `{rel_path}`")
    return file_list

# 📝 Contenido del README
readme = f"""# 📊 Análisis Presupuestario Público con Streamlit

Este proyecto forma parte del Trabajo Fin de Máster y tiene como objetivo ofrecer una herramienta escalable y transparente para el análisis presupuestario en el sector público.

## 🧱 Estructura del Proyecto

- `app.py`: Aplicación principal en Streamlit
- `modules/`: Módulos reutilizables para carga, transformación y visualización de datos
- `data/`: Datos presupuestarios en formato CSV
- `models/`: Módulo de regresión para predicción presupuestaria

## 🔍 Funcionalidades

- Visualización interactiva de presupuestos
- Conversión automática a euros
- Predicción basada en regresión lineal
- Exportación de informes auditables

## 📦 Dependencias

""" + "\n".join(dependencies) + "\n\n"

if modules_list:
    readme += "## 📂 Módulos personalizados\n" + "\n".join(modules_list) + "\n\n"

if models_list:
    readme += "## 📈 Modelos de predicción\n" + "\n".join(models_list) + "\n\n"

readme += "## 📁 Archivos detectados\n" + "\n".join(scan_all_files(project_root)) + "\n\n"

readme += """## 🎨 Presentación

- Paleta institucional adaptada a la universidad
- Diseño modular y escalable
- Cumple con estándares académicos y de auditoría

## 📄 Documentación del TFM

- Documento principal en formato Word/PDF
- Anexos técnicos y visualizaciones
- Código auditado y comentado

## 📜 Licencia

Este proyecto está bajo la licencia MIT / CC-BY-SA.
"""

# 💾 Guardar el README dentro de la carpeta del proyecto
readme_path = os.path.join(project_root, "README.md")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(readme)

print(f"✅ README.md generado correctamente en: {readme_path}")
