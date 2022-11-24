## Setting up a static webpage through Azure storage

### Creating a storage account and uploading the website files.

A resource group, storage account, and a basic HTML file is all that is needed to get this project started.

<br>

1. A resource group is required by the resources that will be made. It'll also keep the project resources in one place. Search for “Resource groups” on the Azure marketplace and create a new resource.
    1. Subscription: default (unless you have multiple).
    2. Resource group: **name** e.g. website-rg
    3. Region: default (This only effects where the resource meta data is stored).
    4. Review + create.

2. A storage account is required to store the website files. Search for “Storage accounts” on the Azure marketplace and create a new resource.
    1. Subscription: default (unless you have multiple).
    2. Resource group: **project resource group.**
    3. Storage account name: **name (must be unique).**
    4. Region: **a region (probably the closest region).**
    5. Performance: **Standard.**
    6. Redundancy: **Locally-redundant storage (unless greater redundancy is needed).**
    7. Review + create.

3. The static website feature needs to be enabled on the storage account to allow us to host the content. Within the storage account, click on “Static website” blade.
    1. **Static website:** Enable.
    2. Note down the “Primary endpoint” address.
    3. **Index document name:** enter in the index file name e.g. index.html
    4. (Optional) Error document path: enter in the 404 file name e.g. 404.html

4. Within the storage account navigate to “Containers” (left side menu) and click on the “$web” container.

5. Click on “Upload” and select the content e.g. index.html, 404.html, etc.

6. After a minute we should be able to access the website through the Primary endpoint address noted down from earlier.

<br>

### Mapping a custom domain name

<br>

To map a custom domain name, we'll need to first own a domain. A domain can be purchased for around £10 a year from most domain name registrars. Alternatively, we can purchase a domain through Azure App Service Domains ([guide]) (https://learn.microsoft.com/en-us/azure/app-service/manage-custom-dns-buy-domain). This method will create a DNS zone so it does save us some work.

If we own a domain name outside of Azure then we should be able to either create a CNAME record to point at Azure or host our domain using Azure DNS. In this instance I followed [Microsoft's guide] (https://learn.microsoft.com/en-us/azure/dns/dns-delegate-domain-azure-dns) to host my domain. In addition to Azure DNS we'll also need to use Azure CDN to delivery our content under our domain name.

<br>

1. Azure DNS will allow us to host our domain name and manage our DNS records. Search for “DNS zones” on the Azure marketplace and create a new resource.
    1. Subscription: default (unless you have multiple).
    2. **Resource group:** project resource group.
    3. **Name:** enter domain name e.g. waihfun.com (can be anything, but the domain is easier to recognise)
    4. Review + create.

2. Return to the project resource group and click on the new DNS zone. 
    1. Within the "Overview" blade note down the four name servers on the right side.
    2. Most domain name registrars have a management page. From there we can set the domain's name server to the ones from Azure.

3. Azure CDN will help distribute our static website, but it will also allow us to host the site with a custom domain name. Search for “Front Door and CDN profiles” on the Azure marketplace and create a new resource.
1. Select “Explore other offerings” + “Azure CDN Standard from Microsoft (classic)”
2. Continue.
3. Subscription: default (unless you have multiple).
4. Resource group: select previously created resource group.
5. Name: enter a name e.g. cdn-profile.
6. Region: Global.
7. Pricing tier: Microsoft CDN (classic).
8. Tick “Create a new CDN endpoint”.
1. CDN endpoint name: enter domain name excluding top level domain e.g. waihfun
2. Origin type: Storage static website.
3. Origin hostname: previously noted primary endpoint address e.g. ***.***.web.core.windows.net.
9. Review + create.

4. To point our domain name at Azure CDN (our content) we'll need to create new DNS records in our DNS zone. Within the Overview blade of our DNS zone create a “Record set”.
1. Name: www.
2. Type: CNAME.
3. Alias record set: yes.
4. Alias type: Azure resource
5. Subscription: default (unless you have multiple).
6.  Azure resource: select previously created Azure CDN profile.

(Optional) We can create another alias so that our apex (root) domain also points to the CDN endpoint. Currently the site can only be reached through www.domain.name instead of just domain.name like many other websites. However, we will run into additional issues with enabling HTTPS on the Apex domain later on as this is no longer managed by Microsoft.
7. Create a new record set.
8. Name: @
9. Type: A
10. Alias record set: yes.
11. Alias type: Azure resource
12. Subscription: default (unless you have multiple).
13.  Azure resource: select previously created Azure CDN profile.

5. Now that our domain directs us to the CDN endpoint, we can create custom domain names. On the CDN endpoint, create “Custom domain” under the Overview blade.
1. Custom hostname: www.domain.name e.g. www.waihfun.com
2. (Optional) If a apex domain name record was created in the DNS zone then create another custom domain name with the hostname being domain.name.
3. www.domain.name should display the website after around 20 – 30 minutes.