from azure.cosmos import CosmosClient, PartitionKey

import config

databaseName = str('waihfun')
# Defines a partition key for container. Can just by "/id".
partitionKey = PartitionKey(path='/pageId')
containerName = str('pagevisists')

# Creates a new client instance with the variables stored in config.py
client = CosmosClient(
    url=config.settings['account'], 
    credential=config.settings['master_key'])

# Creates a new database if it does not already exist and returns the databaseproxy reference.
database = client.create_database_if_not_exists(id=databaseName)

# Creates a new container if it does not already exist abd returns the containerproxy reference.
container = database.create_container_if_not_exists(id=containerName, partition_key=partitionKey)