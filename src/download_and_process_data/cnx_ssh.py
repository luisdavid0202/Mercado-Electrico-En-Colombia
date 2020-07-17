# Standard library imports
import os

# Third party imports
import boto3
import botocore
import paramiko

# Local application/library imports
import setup

os.system(setup.COMMAND_CSV_TO_UBUNTU)

key = paramiko.RSAKey.from_private_key_file(setup.PEM_KEY_PATH)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(hostname=setup.HOST_NAME, username=setup.USERNAME, pkey=key)

    stdin, stdout, stderr = client.exec_command(setup.INSERT_DATA)

    print(stdout.read())

    client.close()

except Exception as e:
    print(e)
