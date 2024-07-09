from array import array
import os
from PIL import Image
import sys
import time
import numpy as np
import pandas as pd
import os
import sys
import os
from azure.storage.blob import BlobClient
from azure.storage.blob import ContentSettings
import msrest
import re



def extract_text_dimag(url, endpoint, credentials):
    print(url)    
    from azure.cognitiveservices.vision.computervision import ComputerVisionClient
    from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
    computervision_client = ComputerVisionClient(endpoint=endpoint, credentials=credentials)

    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read(url,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]

    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            out = []
            for line in text_result.lines:
                #print(line.text)
                out.append(line.text)
                #print(line.bounding_box)
                
    return out

# Load resource group name, subscription_id, and credentials
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
RESOURCE_GROUP_NAME = f"delphi-systems_group"
subscription_id = "3a06912d-cc8f-41d9-88d6-357c4f21c79f"


# Obtain storage account information
STORAGE_ACCOUNT_NAME = f"regionofinterest"

from azure.mgmt.storage import StorageManagementClient
storage_client = StorageManagementClient(credential, subscription_id)
keys = storage_client.storage_accounts.list_keys(RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME)

print(f"Primary key for storage account: {keys.keys[0].value}")
os.environ['AZURE_STORAGE_CONNECTION_STRING'] = f"DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={keys.keys[0].value}"

print(f"Connection string: {os.getenv('AZURE_STORAGE_CONNECTION_STRING')}")

filenom = sys.argv[1]

CONTAINER_NAME = f"aone"


from azure.storage.blob import BlobServiceClient
conn_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
print(conn_str)

# Create the BlobServiceClient object : 
blob_service_client = BlobServiceClient.from_connection_string(conn_str)
print('blob_service_client: ', blob_service_client)

# Create the blob storage container, public_access means you can obtain the image with a url
from azure.storage.blob import PublicAccess
#container_client = blob_service_client.create_container(CONTAINER_NAME, 
#                                                        public_access='BLOB')
container_client = blob_service_client.get_container_client(CONTAINER_NAME)



blob = BlobClient.from_connection_string(conn_str=conn_str,
                                         container_name=CONTAINER_NAME,
                                         blob_name=filenom)
    
    # Content-type
with open(file=filenom, mode="rb") as data:
    blob.upload_blob(data, 
                     overwrite=True, 
                     content_settings=ContentSettings(content_type='image/jpeg'))

# Call OCR
from msrest.authentication import CognitiveServicesCredentials
VISION_KEY = '854b060e2fbe452e9fed1988f64b909c'
credentials = CognitiveServicesCredentials(VISION_KEY)
#endpoint = "https://global.api.cognitive.microsoft.com/"
endpoint = "https://centralindia.api.cognitive.microsoft.com/"


blobs_list = container_client.list_blobs()
for blob in blobs_list:
    print(blob.name + '\n')
    
    # Obtenir url pour chaque objet
    url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob.name}"
    
    text_result = extract_text_dimag(url, endpoint, credentials)
    
    dateFound = False
    date_extract_pattern = "[0-9]{2}[-|\/]{1}[0-9]{1}[-|\/]{1}[0-9]{2}"
    for line in text_result:
        dateVal = re.search(date_extract_pattern, line)
        if dateVal is not None:
            dateFound = True
            print(dateVal.group())

    if dateFound == False:
        print("Date not found")