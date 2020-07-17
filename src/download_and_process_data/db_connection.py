# Standard library imports
import time

# Third party imports
import mysql.connector
import pandas as pd

# Local application/library imports
import setup


start = time.time()

cnx = mysql.connector.connect(
    host=setup.RDS_HOST,
    port=setup.RDS_PORT,
    user=setup.RDS_USERNAME,
    password=setup.RDS_PASSWORD,
)

cursor = cnx.cursor()

cursor.execute(f"CREATE DATABASE {setup.DB_NAME}")
cnx.close()

cnx = mysql.connector.connect(
    host=setup.RDS_HOST,
    port=setup.RDS_PORT,
    user=setup.RDS_USERNAME,
    password=setup.RDS_PASSWORD,
)

cursor = cnx.cursor()

cursor.execute(setup.TABLE_QUERY)
cnx.close()

end = time.time()

if end >= 60:
    print(
        "[INFO] Elapsed time on execution: {:.2f} minutes...".format((end - start) / 60)
    )
else:
    print("[INFO] Elapsed time on execution: {:.2f} seconds...".format(end - start))
