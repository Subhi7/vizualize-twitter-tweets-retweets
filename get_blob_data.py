import config
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from io import StringIO
import pandas as pd


def get_data(CONTAINER_NAME, BLOB_NAME, REQUEST_ID):
	# CONTAINER_NAME, BLOB_NAME, REQUEST_ID = "container052021", 'Blob_06_05_2021', 'request_4244'

	blob_service_client = BlobServiceClient.from_connection_string(conn_str=config.AZURE_STORAGE_CONNECTION_STRING)
	container_client = blob_service_client.get_container_client(CONTAINER_NAME)

	blob_list = container_client.list_blobs()
	df_final = pd.DataFrame()

	for blob in blob_list:
		if REQUEST_ID+'/' in blob.name:
			print("Working on blob:", blob.name)
			blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob.name)
			data = blob_client.download_blob().readall()
			s=str(data,'utf-8')
			data = StringIO(s)
			df_curr = pd.read_csv(data)
			df_final = df_final.append(df_curr, ignore_index=True)


	return df_final