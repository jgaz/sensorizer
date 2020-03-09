#!/usr/bin/env bash
az login
az account set --subscription "$SUBSCRIPTION_NAME"
az container create \
    --location northeurope \
    --name sensorizer-04 \
    --image $DOCKER_IMAGE_NAME \
    --os-type Linux \
    --cpu 1 \
    --memory 1.5 \
    --resource-group $RESOURCE_GROUP \
    --registry-password $REGISTRY_PASSWORD \
    --registry-login-server $REGISTRY_SERVER \
    --registry-username $REGISTRY_USER \
    --secure-environment-variables \
      'EVENT_HUB_SAS_KEY'=$EVENT_HUB_SAS_KEY \
    --environment-variables \
        'EVENT_HUB_ADDRESS'=$EVENT_HUB_ADDRESS \
        'EVENT_HUB_SAS_POLICY'=$EVENT_HUB_SAS_POLICY
