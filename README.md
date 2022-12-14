## Setting up a static webpage through Azure storage

<br>

## Creating a storage account to host the website

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

## Mapping a custom domain name

To map a custom domain name, we'll need to first own a domain. A domain can be purchased for around £10 a year from most domain name registrars. Alternatively, we can purchase a domain through Azure App Service Domains ([guide](https://learn.microsoft.com/en-us/azure/app-service/manage-custom-dns-buy-domain)). This method will create a DNS zone so it does save us some work.

If we own a domain name outside of Azure then we should be able to either create a CNAME record to point at Azure or host our domain using Azure DNS. In this instance I followed [Microsoft's guide](https://learn.microsoft.com/en-us/azure/dns/dns-delegate-domain-azure-dns) to host my domain. In addition to Azure DNS we'll also need to use Azure CDN to delivery our content under our domain name.

<br>

1. Azure DNS will allow us to host our domain name and manage our DNS records. Search for “DNS zones” on the Azure marketplace and create a new resource.
    1. Subscription: project subscription.
    2. Resource group: project resource group.
    3. Name: enter domain name e.g. waihfun.com
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
    1. CDN endpoint name: name e.g. waihfun (exclud the top level domain)
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

(Optional) We can create another alias so that our apex (root) domain also points to the CDN endpoint. Currently the site can only be reached through w<span>ww.</span>domain.name instead of just domain.name like many other websites. **Enabling HTTPS on root domains will require additional steps.**

1. On the DNS zone create a new record set.
2. Name: @
3. Type: A
4. Alias record set: yes.
5. Alias type: Azure resource
6. Subscription: project subscription.
7. Azure resource: select previously created Azure CDN profile.
8. Create a new custom domain on the CDN endpoint.

<br>

## Enabling HTTPS

HTTPS uses digital certificates for authentication and encryption. While we probably do not need to use HTTPS for this basic site it would still be ideal to enable HTTPS especially when we can easily do this for free on our www subdomain.

1. Within the CDN endpoint click on the custom domain beginning with ww<span>w.</span>
    1. Custom domain HTTPS: On  
    2. Certificate management type: CDN managed.
    3. Minimum TLS version: TLS 1.2.
    4. Save.
    - Microsoft took around 1 hour to provision the certificate, but once completed I was able to access the site and view the certificate.

2. With https enabled we will not be able to access the site through http. We can resolve this by creating a rule to redirect http requests to https. Within the CDN endpoint go the to “Rules engine” blade.
    1. Add rule.
    2. Add condition > Request Protocol.
    3. Operator: Equals.
    4. Value:  HTTP.
    5. Add action > URL Redirect
    6. Type: Move (301).
    7. Protocol: HTTPS.
    8. Save.

### (Optional) Enabling HTTPS for root domain

Azure CDN will not provide certificates for root domains. In order to enable HTTPS for root domains we will need to acquire a certificate and provide it to Azure (Azure Key Vault). Luckily we can do this for free by using [Certbot](https://certbot.eff.org/) to generate certificates using [Let's Encrypt](https://letsencrypt.org/) (a non-profit certificate authority). The only downside to manually generating a certificate through the method below is that they have a 90 day expiry. While I can generate another one, I plan to automate this, as I'll probably forget to renew the certificate.

1. [Install Certbot.](https://certbot.eff.org/instructions) Using Ubuntu 22.04.1 LTS on a VM, I was able to install from terminal with `sudo snap install --classic certbot`
    
2. Onces installed we can run `certbot certonly --manual --preferred-challenges dns -d *.domain.name` in terminal.
    - `certonly --manunal` - Will only obtain a certificate through manual validation.
    - `--preferred-challenges dns` - sets challenge to DNS challenge.
    - `-d` - specifies the domain. The *. in front of our domain allows us to generate a wildcard certificate so we don't have to do this for multiple sub domains.

3. In the Azure DNS zone that hosts the domain create a new record set and set the values as per the instructions provided by Certbot.
    - Name: _acme-challenge.domain.name
    - Type: TXT
    - Value: copy/paste from Certbot

4. In order to upload the certificate to Azure Key Vault we'll need to convert the certificate and private key provided by Certbot to pfx format.
    1. OpenSSL is required for this operation. The version of Ubuntu I used already has OpenSSL. Git for windows also has OpenSSL.
    2. Navigate to the folder that contains the newly generate private key and certificate.
    3. Execute the command `openssl pkcs12 -export -out <certificate_name>.pfx -inkey privkey.pem -in fullchain.pem -passout pass:<certificate_password>`
    - `pkcs12 -export` - creates a PKCS#12 file instead of parsing.
    - `-out` - specifies filename of the PKCS#12 file to be created.
    - `-inkey` - specifies the filename of the private key.
    - `-in` - specifies the filename of the certificate.
    - `-passout` - password for the PKCS#12 file.

5. Azure Key Vault is needed to securely store our pfx certificate and to provide a location for the CDN to check. Search for “Key vaults” on the Azure marketplace and create a new resource.
    1. Subscription: project subscription.
    2. Resource group: project resource group.
    3. Key vault name: name (must be unique).
    4. Region: a region (probably the closest region).
    5. Pricing tier: Standard.
    6. Review + create.

6. To upload the certificate, go to the key vault and click on the "Certificates" blade.
    1. Generate/import.
    2. Method of Certificate Creation: Import
    3. Certificate name: name.
    4. Upload Certificate File: select the newly created .pfx file.
    5. Password: password set in `-passout` option of previous command.
    6. Create.

7. The final step involves granting the CDN endpoint access to the key vault and assigning the certificate to the root domain.
    1. Navigate to the custom root domain in the CDN endpoint.
    2. Custom domain HTTPS: On
    3. Certificate management type: User my own certificate.
    4. Minimum TLS version: 1.2
    5. Follow the instructions provided by MS to create a new service principle and the application access to key vault.
    6. Key vault: key vault name.
    7. Certificate/Secret: certificate name.
    8. Certificate/Secret version: Latest 
    - Similar to the CDN managed certificate it took around 30 - 60 minutes for the certificate to be visible on the webpage.
    - If a wild card certificate was created then the www sub domain could be changed over to our own just to test that it works.

8. (Optional) For consistency in the URL we can create a rule to always redirect the www sub domain to our root domain. In the CDN endpoint go to the "Rules engine" blade.
    1. Add rule.
    2. Add condition > Request URL.
    3. Operator: Begins with.
    4. Request URL: ht<span>tps://w<span>ww.<span>domain.name
    5. Case transform: To lowercase (not sure if this makes a difference).
    6. Add action > URL redirect.
    7. Type: Moved (301).
    8. Protocol: HTTPS.
    9. Hostname: domain.name
    10. Save.
