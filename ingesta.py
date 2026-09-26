import csv
import boto3
import pymysql

# Datos de conexion a la base de datos MySQL (contenedor "mysql-db" en la misma red Docker)
host = "mysql-db"
usuario = "admin"
password = "IngestaS3_2025"
baseDatos = "ingesta_db"
tabla = "personas"

ficheroUpload = "data.csv"
nombreBucket = "gcr-output-02-mx"

# 1. Conectarse a MySQL y leer todos los registros de la tabla
conexion = pymysql.connect(host=host, user=usuario, password=password, database=baseDatos)
cursor = conexion.cursor()
cursor.execute(f"SELECT * FROM {tabla}")
filas = cursor.fetchall()
columnas = [col[0] for col in cursor.description]
cursor.close()
conexion.close()

# 2. Guardar los registros leidos en un archivo csv
with open(ficheroUpload, "w", newline="") as f:
    escritor = csv.writer(f)
    escritor.writerow(columnas)
    escritor.writerows(filas)

# 3. Subir el archivo csv al bucket S3
s3 = boto3.client('s3')
response = s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)
print(response)

print("Ingesta completada")
