# Backend of website

## Setting up a static webpage through Azure storage

### Creating a storage account and uploading the website files.

A resource group, storage account, and a basic HTML file is all that is needed to get this project started.

1. A resource group is required by the resources that will be made. It'll also keep the project resources in one place. Search for “Resource groups” on the Azure marketplace and create a new resource.
    1. Subscription: default (unless you have multiple).
    2. Resource group: enter a name e.g. website-rg
    3. Region: default (This only effects where the resource meta data is stored.).
    4. Review + create.

2. A storage account is required to store the website files. Search for “Storage accounts” on the Azure marketplace and create a new resource.
    1. Subscription: default (unless you have multiple).
    2. Resource group: select previously created resource group.
    3. Storage account name: enter a new (must be unique).
    4. Region: select a appropriate region (probably the closest region)
    5. Performance: Standard.
    6. Redundancy: Locally-redundant storage (unless greater redundancy is needed).
    7. Review + create.

3. The static website feature needs to be enabled on the storeage account to enable us to host the content. Within the storage account, click on “Static website” blade.
    1. Static website: Enable.
    2. Note down the “Primary endpoint” address.
    3. Index document name: enter in the index file name e.g. index.html
    4. (Optional) Error document path: enter in the 404 file name e.g. 404.html

4. Within the storage account navigate to “Containers” (left side menu) and click on the “$web” container.

5. Click on “Upload” and select the content e.g. index.html, 404.html, etc.

6. After a minute we should be able to access the website through the Primary endpoint address noted down from earlier.
