import mysql.connector
import pandas as pd
import time

start = time.time()

DB_NAME = "Electabuzz"

cnx = mysql.connector.connect(host="1", port=1, user="1", password="1",)

cursor = cnx.cursor()

cursor.execute(f"CREATE DATABASE {DB_NAME}")
cnx.close()

cnx = mysql.connector.connect(
    host="1", port=1, user="1", password="1", database=DB_NAME
)

cursor = cnx.cursor()

cursor.execute(
    """CREATE TABLE mercado_electrico (
                DEPARTAMENTO VARCHAR(255), 
                MUNICIPIO VARCHAR(255), 
                AGENTE_COMERCIALIZADOR VARCHAR(255),
                NIVEL_TENSION INT(255),
                DIA INT(255),
                DEMANDA DECIMAL(64,10),
                PRECIO DECIMAL(64,10),
                FECHA INT(255))
               """
)

db = pd.read_csv("csv_in_one_file/data.csv")

end = time.time()

if end >= 60:
    print(
        "[INFO] Elapsed time on execution: {:.2f} minutes...".format((end - start) / 60)
    )
else:
    print("[INFO] Elapsed time on execution: {:.2f} seconds...".format(end - start))
