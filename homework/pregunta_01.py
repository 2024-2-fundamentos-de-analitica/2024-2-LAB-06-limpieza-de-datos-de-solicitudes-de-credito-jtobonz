"""
Escriba el código que ejecute la acción solicitada en la pregunta.
"""
import pandas as pd
import os

def pregunta_01():
    """
    Realiza la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo presenta problemas como duplicados y valores faltantes.
    Se deben aplicar las verificaciones necesarias para garantizar
    la calidad de los datos.

    El archivo limpio debe ser guardado en "files/output/solicitudes_de_credito.csv".
    """
    # Definir rutas de los archivos
    ruta_entrada = 'files/input/solicitudes_de_credito.csv'
    ruta_salida = 'files/output/solicitudes_de_credito.csv'
    directorio_salida = 'files/output'

    # Cargar los datos con el delimitador adecuado
    datos = pd.read_csv(ruta_entrada, sep=';')

    # Eliminar la columna 'Unnamed: 0' si está presente
    if 'Unnamed: 0' in datos.columns:
        datos.drop(columns=['Unnamed: 0'], inplace=True)

    # Eliminar valores nulos y registros duplicados
    datos.dropna(inplace=True)
    datos.drop_duplicates(inplace=True)

    # Procesar la columna 'fecha_de_beneficio' para garantizar el formato YYYY-MM-DD
    datos[['dia', 'mes', 'anio']] = datos['fecha_de_beneficio'].str.split('/', expand=True)
    datos.loc[datos['anio'].str.len() < 4, ['dia', 'anio']] = datos.loc[datos['anio'].str.len() < 4, ['anio', 'dia']].values
    datos['fecha_de_beneficio'] = datos['anio'] + '-' + datos['mes'] + '-' + datos['dia']
    datos.drop(columns=['dia', 'mes', 'anio'], inplace=True)

    # Normalización de texto en las columnas categóricas
    columnas_texto = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito']
    datos[columnas_texto] = datos[columnas_texto].apply(lambda col: col.str.lower().replace(['-', '_'], ' ', regex=True).str.strip())
    datos['barrio'] = datos['barrio'].str.lower().replace(['-', '_'], ' ', regex=True)

    # Formateo de la columna 'monto_del_credito'
    datos['monto_del_credito'] = datos['monto_del_credito'].str.replace(r"[$, ]", "", regex=True).str.strip()
    datos['monto_del_credito'] = pd.to_numeric(datos['monto_del_credito'], errors='coerce').fillna(0).astype(int)
    datos['monto_del_credito'] = datos['monto_del_credito'].astype(str).str.replace('.00', '')

    # Eliminar duplicados nuevamente después de la limpieza
    datos.drop_duplicates(inplace=True)

    # Crear el directorio de salida si no existe
    os.makedirs(directorio_salida, exist_ok=True)

    # Guardar el archivo limpio con el mismo delimitador
    datos.to_csv(ruta_salida, sep=';', index=False)

    return datos.head()

if __name__ == '__main__':
    pregunta_01()
