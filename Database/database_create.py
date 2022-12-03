import uuid
import json
from azure.cosmos import CosmosClient, PartitionKey

import config

databaseId = str('waihfun')
# Defines a partition key for container. Can just by "/id".
partitionKey = PartitionKey(path='/pageId')
containerId = str('pagevisits')

pages = ['index', 'projects']

# Creates a new client instance with the variables stored in config.py
client = CosmosClient(
    url=config.settings['account'], 
    credential=config.settings['master_key'])

# Creates a new database if it does not already exist and returns the databaseproxy reference.
database = client.create_database_if_not_exists(id=databaseId)

# Creates a new container if it does not already exist abd returns the containerproxy reference.
container = database.create_container_if_not_exists(id=containerId, partition_key=partitionKey)

# creates the items for each page in the pages array.
for p in pages:
    # Query's the container for matching pageId.
    result = container.query_items(
        query="SELECT * FROM " + containerId + " c WHERE c.pageId = @pageId", 
        parameters=[{"name": "@pageId", "value": p}],
        enable_cross_partition_query=False)

    # If there are items returned then display the result else create the item.
    if any(result):
        # PROBLEM: Iterating through a iterator consumes it. This does nothing as it's empty after the If statement.
        for i in result:
            print(json.dumps(i, indent=False))
    else:
        print('Item ' + p + ' not found. Creating item.')
        # Creates the item.
        container.create_item({
            'id': str(uuid.uuid4()),
            'pageId': p,
            'visits': 0
        })