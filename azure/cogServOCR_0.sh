#!/bin/bash

az login

export subscription_id=$(echo "3a06912d-cc8f-41d9-88d6-357c4f21c79f")
az account set -s $subscription_id

# ---------------------------------------------

#let "randomIdentifier=$RANDOM*$RANDOM"

# ---------------------------------------------

# Create a Resource Group
export location=$(echo "global")
export resourceGroupname=$(echo "delphi-systems_group")

#az group create --name $resourceGroupname --location $location

# ---------------------------------------------

# Create a Storage Account
export STORAGE_NAME=$(echo "regionofinterest")
#az storage account create --name $STORAGE_NAME \
#                              --resource-group $resourceGroupname \
#                              --location $location \
#                              --kind StorageV2 \
#                              --sku Standard_LRS \
#                              --allow-blob-public-access true

# Get important storage account information to create the blobcontainer 
export ids=$(az storage account show -g $resourceGroupname -n $STORAGE_NAME | jq '.id')
export connectionstring=$(az storage account show-connection-string -g $resourceGroupname -n $STORAGE_NAME | jq '.connectionString')
export STORAGE_ACCOUNT_KEY=$(az storage account keys list -g $resourceGroupname -n $STORAGE_NAME | jq '.[].value' |cut -d $'\n' -f 1)
export destination=$(az storage account show -g $resourceGroupname -n $STORAGE_NAME | jq '.primaryEndpoints.file')

# ---------------------------------------------

# Create a Computer Vision Cognitive Service
export COGSERVname=$(echo "yokohama-balaji")
#az cognitiveservices account create --name $COGSERVname \
#                                        --resource-group $resourceGroupname \
#                                        --kind ComputerVision \
#                                        --sku F0 \
#                                        --location $location 
#                                        --yes
export VISION_KEY=$(az cognitiveservices account keys list --name $COGSERVname -g $resourceGroupname  | jq -r '.key1')
export VISION_ENDPOINT=$(az cognitiveservices account show -n $COGSERVname -g $resourceGroupname | jq -r '.properties.endpoint')
export VISION_LOCATION=$(az cognitiveservices account show --resource-group $resourceGroupname --name $COGSERVname --query location --output tsv)