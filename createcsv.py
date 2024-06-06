import pandas as pd

# Datos de ejemplo
data = {
    'Nombre': ['Ana', 'Luis', 'Carlos', 'María'],
    'Edad': [23, 34, 29, 25],
    'Ciudad': ['Madrid', 'Barcelona', 'Sevilla', 'Valencia']
}

# Crear un DataFrame con los datos
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
csv_file_path = 'datos.csv'
df.to_csv(csv_file_path, index=False)

print(f"Archivo CSV guardado en: {csv_file_path}")
