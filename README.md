## Setting up a static webpage through Azure storage

### Creating a storage account and uploading the website files.

A resource group, storage account, and a basic HTML file is all that is needed to get this project started.

1. A resource group is required by the resources that will be made. It'll also keep the project resources in one place. Search for “Resource groups” on the Azure marketplace and create a new resource.
    1. Subscription: default (unless you have multiple).
    2. Resource group: name e.g. website-rg
    3. Region: default (This only effects where the resource meta data is stored).
    4. Review + create.

2. A storage account is required to store the website files. Search for “Storage accounts” on the Azure marketplace and create a new resource.
    1. Subscription: project subscription.
    2. Resource group: project resource group.
    3. Storage account name: name (must be unique).
    4. Region: a region (probably the closest region).
    5. Performance: Standard.
    6. Redundancy: Locally-redundant storage (unless greater redundancy is needed).
    7. Review + create.

3. The static website feature needs to be enabled on the storage account to allow us to host the content. Within the storage account, click on “Static website” blade.
    1. Static website: Enable.
    2. Note down the “Primary endpoint” address.
    3. Index document name:** enter in the index file name e.g. index.html
    4. (Optional) Error document path: enter in the 404 file name e.g. 404.html

4. Within the storage account navigate to “Containers” (left side menu) and click on the “$web” container.

5. Click on “Upload” and select the content e.g. index.html, 404.html, etc.

6. After a minute we should be able to access the website through the Primary endpoint address noted down from earlier.

<br>

### Mapping a custom domain name

To map a custom domain name, we'll need to first own a domain. A domain can be purchased for around £10 a year from most domain name registrars. Alternatively, we can purchase a domain through Azure App Service Domains ([guide](https://learn.microsoft.com/en-us/azure/app-service/manage-custom-dns-buy-domain)). This method will create a DNS zone so it does save us some work.

If we own a domain name outside of Azure then we should be able to either create a CNAME record to point at Azure or host our domain using Azure DNS. In this instance I followed [Microsoft's guide](https://learn.microsoft.com/en-us/azure/dns/dns-delegate-domain-azure-dns) to host my domain. In addition to Azure DNS we'll also need to use Azure CDN to delivery our content under our domain name.

<br>

1. Azure DNS will allow us to host our domain name and manage our DNS records. Search for “DNS zones” on the Azure marketplace and create a new resource.
    1. Subscription: project subscription.
    2. Resource group: project resource group.
    3. Name: enter domain name e.g. waihfun.com (can be anything, but the domain is easier to recognise)
    4. Review + create.

2. Return to the project resource group and click on the new DNS zone. 
    1. Within the "Overview" blade note down the four name servers on the right side.
    2. Most domain name registrars have a management page. From there we can set the domain's name server to the ones from Azure.

3. Azure CDN will help distribute our static website, but it will also allow us to host the site with a custom domain name. Search for “Front Door and CDN profiles” on the Azure marketplace and create a new resource.
    1. Select “Explore other offerings” + “Azure CDN Standard from Microsoft (classic)”
    2. Continue.
    3. Subscription: project subscription.
    4. Resource group: project resource group.
    5. Name: name e.g. cdn-profile.
    6. Region: Global (default).
    7. Pricing tier: Microsoft CDN (classic).
    8. Tick “Create a new CDN endpoint”.
    1. CDN endpoint name: name e.g. waihfun (exluded the top level domain)
    2. Origin type: Storage static website.
    3. Origin hostname: previously noted primary endpoint address from storage account e.g. \*\**.***.web.core.windows.net.
    9. Review + create.

4. To point our domain name at Azure CDN (our content) we'll need to create new DNS records in our DNS zone. Within the "Overview" blade of our DNS zone create a Record set.
    1. Name: www
    2. Type: CNAME.
    3. Alias record set: yes.
    4. Alias type: Azure resource
    5. Subscription: project subscription.
    6. Azure resource: select previously created Azure CDN endpoint.

5. Now that our domain directs us to the CDN endpoint, we can create a custom domain name on the CDN endpoint. Within the "Overview" blade of our CDN endpoint create a Custom domain.
    1. Custom hostname: w<span>ww.</span>domain.name e.g. w<span>ww.</span>.waihfun.com
    2. Try loading the website from the custom domain name after around 20 – 30 minutes.

(Optional) We can create another alias so that our apex (root) domain also points to the CDN endpoint. Currently the site can only be reached through w<span>ww.</span>domain.name instead of just domain.name like many other websites. **Enabling HTTPS on apex domains will require additional steps.**

1. On the DNS zone create a new record set.
2. Name: @
3. Type: A
4. Alias record set: yes.
5. Alias type: Azure resource
6. Subscription: project subscription.
7. Azure resource: select previously created Azure CDN profile.
8. Create a new custom domain on the CDN endpoint.

<br>

### Enabling HTTPS

HTTPS uses digital certificates for authentication and encryption. While we probably do not need to use HTTPS for this basic site it would still be ideal to enable HTTPS especially when we can easily do this for free on our www subdomain.

1. Within the CDN endpoint click on the custom domain beginning with www.
    1. Custom domain HTTPS: On  
    2. Certificate management type: CDN managed.
    3. Minimum TLS version: TLS 1.2.
    4. Save.
    - Microsoft took around 1 hour to provision the certificate, but once complete I was able to access the website via https://w<span>ww.</span>waihfun.com

2. With HTTPS enabled we will not be able to access the site through http://**. We can resolve this by creating a rule to redirect http requests to https. Within the CDN endpoint go the to “Rules engine” blade.
    1. Add rule.
    2. Add condition > Request Protocol.
    3. Operator: Equals.
    4. Value:  HTTP.
    5. Add action > URL Redirect
    6. Type: Move (301).
    7. Protocol: HTTPS.
    8. Save.