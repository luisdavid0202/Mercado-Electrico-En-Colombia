import os

import boto3
import botocore
import paramiko

os.system("scp -i colelectrica.pem csv_in_one_file/data.csv ubuntu@ec2-54-92-164-20.compute-1.amazonaws.com:~/")

key = paramiko.RSAKey.from_private_key_file("colelectrica.pem")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(hostname="35.175.129.74", username="ubuntu", pkey=key)

    stdin, stdout, stderr = client.exec_command("python3 insert_sql.py")
    
    print(stdout.read())

    client.close()

except Exception as  e:
    print(e)
