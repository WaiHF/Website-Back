import json
# pip3 install --upgrade azure-cosmos. needed for below.
from azure.cosmos import CosmosClient, PartitionKey

import config

databaseId = str('website')
# Defines a partition key for container. Can just by "/id".
partitionKey = PartitionKey(path='/id')
containerId = str('page_visits')

pages = ['index', '404', 'projects', 'contact']

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
        query="SELECT * FROM " + containerId + " c WHERE c.id = @id", 
        parameters=[{"name": "@id", "value": p}],
        enable_cross_partition_query=False)

    # PROBLEM: Iterating through a iterator consumes it.
    # Probably a better fix than just dumping the results into a list.
    resultList = []
    for r in result:
        resultList.append(r)

    # If there are items returned then display the result else create the item.
    if any(resultList):
        print('\nResult found:\n' + json.dumps(resultList, indent=False))
    else:
        print('Item ' + p + ' not found. Creating item.')
        # Creates the item.
        container.create_item({
            'id': p,
            'visits': 0
        })