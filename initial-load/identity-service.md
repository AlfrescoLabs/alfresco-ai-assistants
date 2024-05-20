---
title: Identity Service
---

The Identity Service is responsible for supporting user authentication of other Alfresco software.

The key capabilities of the Identity Service include the ability to:

* Enable Single Sign On (SSO) capabilities for Alfresco Content Services and Alfresco Process Services
* Configure user authentication between Identity Service and an LDAP provider
* Configure a supported SAML provider to enable Single Sign On (SSO) with an existing identity provider

More information is available about the Identity Service covering:

* An overview of the Identity Service architecture is within the [Alfresco/alfresco-identity-service](https://github.com/Alfresco/alfresco-identity-service/tree/2.0.0){:target="_blank"} GitHub project documentation.
* How to [install the Identity Service]({% link identity-service/latest/install/index.md %}).
* How to [configure]({% link identity-service/latest/config/index.md %}) realm and theme customizations.

> **Note:** See the [supported platforms]({% link identity-service/latest/support/index.md %}) page for compatibility between Alfresco Content Services or Alfresco Process Services and Identity Service.
---
title: Configure Identity Service
---

There are two things that can be configured in the Identity Service:

## Configure a custom realm

The Identity Service is installed or deployed with a default realm applied called `Alfresco`. The realm can be customized manually or by using a `JSON` file.

> **Important:** The default realm provided is not production ready and should be used as a reference only.

### Customize a realm manually

Customizing a realm manually uses the administrator console of the Identity Service to configure realm settings.

1. Sign into the master realm administrator console using the credentials created on your first sign in.
2. [Add a new realm](https://www.keycloak.org/docs/21.1.2/server_admin/index.html#proc-creating-a-realm_server_administration_guide){:target="_blank"} or edit the `Alfresco` realm.
3. [Create a new OIDC client](https://www.keycloak.org/docs/21.1.2/server_admin/index.html#_oidc_clients){:target="_blank"} or edit the existing one.
4. Configure any [groups](https://www.keycloak.org/docs/21.1.2/server_admin/index.html#proc-managing-groups_server_administration_guide){:target="_blank"} or users.

### Customize a realm using a JSON file

Customizing a realm using a `JSON` file configures a realm outside of the Identity Service and imports it into the configuration using the administrator console or during deployment if [installing to Kubernetes cluster using Helm charts]({% link identity-service/latest/install/k8s/index.md %}).

To import the configuration in the administrator console:

1. Edit or use the [default realm file](https://github.com/Alfresco/alfresco-identity-service/blob/master/helm/alfresco-identity-service/alfresco-realm.json){:target="_blank"} provided in the Identity Service GitHub project as a reference to create a custom realm file.
2. Sign into the master realm administrator console using the credentials created on your first sign in.
3. Navigate to the **Create Realm** page and use the **Browse...** option to import your custom realm file.

To set the realm file during deployment:

1. Create a Kubernetes secret in the cluster called `realm-secret`:

    ```bash
    kubectl create secret generic realm-secret \
        --from-file=./realm.json \
        --namespace=$DESIREDNAMESPACE
    ```

    > **Important:** The name of the realm file must **not** be set as `alfresco-realm.json`

2. Deploy the Helm chart with the additional argument to use the custom realm file (*remember to replace any `<placeholders>`*):

    ```bash
    cat > realm-values.yaml << EOL
    keycloakx:
      extraEnv: |
        - name: KEYCLOAK_ADMIN
          value: <placeholder>
        - name: KEYCLOAK_ADMIN_PASSWORD
          value: <placeholder>
        - name: KEYCLOAK_IMPORT
          value: /data/import/realm.json
        - name: JAVA_OPTS_APPEND
          value: >-
            {%raw%}-Djgroups.dns.query={{ include "keycloak.fullname" . }}-headless{%endraw%}
    EOL 

    helm install alfresco-stable/alfresco-infrastructure \
        --set alfresco-infrastructure.activemq.enabled=false \
        --set alfresco-infrastructure.nginx-ingress.enabled=true \
        --set alfresco-infrastructure.alfresco-identity-service.enabled=true \
        --values realm-values.yaml \
        --namespace $DESIREDNAMESPACE
    ```

## Run Identity Service with Process Services

You can run the Identity Service with Process Services. You must configure both applications for the logout functionality in Process Services to function correctly.

> **Note:** If you do not configure the Identity Service and Process Services correctly, you will receive an error when you try and logout using Process Services.

To run the Identity Service with Process Services:

1. Deploy your Identity Service installation by adding the following command-line parameter:

    ```xml
    --spi-login-protocol-openid-connect-legacy-logout-redirect-uri=true
    ```

2. Ensure you've set `keycloak.token-store=cookie` in the `activiti-identity-service.properties` file in Process Services.

    See `keycloak.token-store` in the [Process Services properties]({% link process-services/latest/config/authenticate.md %}#properties) table for more details.

3. Restart Process Services.

The Process Services logout functionality will now work with the Identity Service.

## Configure a custom theme

Deploying the Identity Service will deploy an Alfresco login theme.

A custom theme can be applied to the following components of the Identity Service:

* Login screens
* Administrator console
* Email
* Account management

The [Alfresco theme](https://github.com/Alfresco/alfresco-keycloak-theme){:target="_blank"} includes a custom login theme only.

### Developing a theme

Themes are created using a combination of CSS, HTML [Freemarker templates](https://freemarker.apache.org/){:target="_blank"}, theme properties and images.

Use the [Alfresco theme](https://github.com/Alfresco/alfresco-keycloak-theme){:target="_blank"} or the default [Keycloak theme](https://www.keycloak.org/docs/21.1.2/server_development/index.html#creating-a-theme){:target="_blank"} as a base to extend and create custom themes from.

### Importing a theme for a Kubernetes deployment

There are a number of options for importing a theme into a Kubernetes deployment, for example:

* Create a new Docker image that contains a custom theme.
* Use an `emptyDir` that is shared with the Identity Service container and configure an `init container` that runs the new theme image and copies it into the theme directory.

    The following is an example of configuring this in the `values.yaml`:

    ```yaml
    keycloak:
        extraInitContainers: |
            - name: custom-theme
              image: <theme-image-location-and-tag>
              imagePullPolicy: IfNotPresent
              command:
                - sh
              args:
                - -c
                - |
                  echo "copying new theme..."
                  cp -R /<theme-image-name>/* /theme
              volumeMounts:
                - name: theme
                mountPath: /theme
    
        extraVolumeMounts: |
            - name: theme
              mountPath: /opt/keycloak/themes/<theme-folder-name>
    
        extraVolumes: |
            - name: theme
              emptyDir: {}
    ```

However a new theme is imported, the new theme will need to be applied by signing into the administrator console and selecting the new themes for each component in the **Themes** tab under **Realm Settings**.

### Importing a theme for a standalone installation

1. Navigate to the themes directory of the installation.
2. Create a new directory for the custom theme.
3. Copy the custom files into directories for each custom theme component for example /themes/login/
4. Restart the Identity Service service.
5. In the administrator console select the new themes for each component in the **Themes** tab under **Realm Settings**.
---
title: Install options
---

The Identity Service can be deployed into a new or existing Kubernetes cluster or installed manually using a standalone ZIP distribution.

There are two options for installing the Identity Service:

* [Install using Helm charts]({% link identity-service/latest/install/k8s/index.md %})
* [Install using a ZIP distribution]({% link identity-service/latest/install/zip/index.md %})

> **Note:** It is recommended that you familiarize yourself with the [concepts of containerized deployment]({% link content-services/latest/install/containers/index.md %}) before working with Docker, Kubernetes, and Helm.

Instructions are also provided for [upgrading the Identity Service]({% link identity-service/latest/upgrade/index.md %}).
---
title: Install Identity Service into Kubernetes Cluster
---

The Identity Service can be deployed into a new or existing Kubernetes cluster.

## Prerequisites

* A Kubernetes cluster
* Helm configured in the cluster

## Installation steps

1. Create a new namespace or use an existing empty namespace to avoid any conflicts:

    ```bash
    export DESIREDNAMESPACE=new-namespace
    kubectl create namespace $DESIREDNAMESPACE             
    ```

2. Add the Alfresco Kubernetes chart repository and the Keycloak repository to Helm:

    ```bash
    helm repo add alfresco-stable https://kubernetes-charts.alfresco.com/stable
    helm repo add codecentric https://codecentric.github.io/helm-charts
    ```

3. Deploy the Helm chart with a command similar to the following:

    The Identity Service is deployed as part of the Alfresco infrastructure chart. Normally the infrastructure chart will be deployed as part of another product chart, such as Alfresco Content Services or Alfresco Process Services.

    As an example, the following command references the infrastructure chart on its own to deploy the Identity Service and the [ngnix-ingress](https://github.com/helm/charts/tree/master/stable/nginx-ingress){:target="_blank"}.

    ```bash
    helm install alfresco-stable/alfresco-infrastructure \
        --set alfresco-infrastructure.activemq.enabled=false \
        --set alfresco-infrastructure.nginx-ingress.enabled=true \
        --set alfresco-infrastructure.alfresco-identity-service.enabled=true \
        --namespace $DESIREDNAMESPACE
    ```

4. (*Optional*) To set the `redirectUri` property during deployment add the following line to the deployment command setting the `{DNSNAME}`:

    ```bash
    --set alfresco-identity-service.realm.alfresco.client.redirectUris="{$DNSNAME}" \
    ```

    > **Note:** To include multiple `redirectUri` use comma separated values without any whitespace between the DNS names.

5. (*Optional*) To set the `webOrigins` property during deployment add the following line to the deployment command setting the `{DNSNAME}`:

    ```bash
    --set alfresco-identity-service.realm.alfresco.client.webOrigins="{$DNSNAME1,$DNSNAME2,$DNSNAME3}" \
    ```

6. (*Optional*) To set the number of replicas during deployment add the following line to the deployment command using the required number of replicas:

    ```bash
    --set alfresco-identity-service.keycloakx.replicas=3
    ```

7. To successfully deploy Identity Service with the specified realm being automatically imported, whilst preserving the `/auth` root path (*remember to set `MY_KEYCLOAK_HOST` appropriately*):

    ```bash
    --set alfresco-identity-service.keycloakx.command[0]="/opt/keycloak/bin/kc.sh" \
    --set alfresco-identity-service.keycloakx.command[1]="start" \
    --set alfresco-identity-service.keycloakx.command[2]="--import-realm" \
    --set alfresco-identity-service.keycloakx.command[3]="--http-relative-path=/auth" \
    --set alfresco-identity-service.keycloakx.command[4]="--hostname=${MY_KEYCLOAK_HOST}"
    ```

8. (*Optional*) To use an external database for persistence purposes you can refer to [this example](https://github.com/codecentric/helm-charts/blob/keycloakx-2.2.1/charts/keycloakx/examples/postgresql/readme.md){:target="_blank"}. If you choose to use PostgreSQL remember to also set the following, on top of the required configuration based on the example:

    ```bash
    --set alfresco-identity-service.keycloakx.postgresql.enabled=true
    ```

9. Navigate to `http://localhost:8080/auth` once all pods have started.

10. Enter a username and password to create an administrator user for the master realm.

The administrator console for the `Alfresco` realm can be accessed at `http://localhost:8080/auth/admin/alfresco/console/`. The administrator user for this realm has the following credentials:

|Property|Value|
|--------|-----|
|Administrator username|`admin`|
|Administrator password|`admin`|
|Administrator email address|`admin@app.activiti.com`|
|Alfresco client redirect URIs|`http://localhost*`|

> **Important:** Reset the administrator password for the `Alfresco` realm when first signing into its administrator console.

The Identity Service can be [configured]({% link identity-service/latest/config/index.md %}) further.
---
title: Install Identity Service from ZIP file
---

The Identity Service can be installed using a standalone ZIP distribution.
A default realm called `Alfresco` is installed.

## Prerequisites

* Java 11 JDK installed

## Installation steps

1. Download the `alfresco-identity-service-2.0.0.zip` file from [Hyland Community](https://community.hyland.com/en/products/alfresco/release-notes/release-notes/alfresco-identity-service-version-200){:target="_blank"}.

2. Move the downloaded zip file to install location of choice and unzip the contents:

    For a Linux or Unix environment:

    ```bash
    $ unzip alfresco-identity-service-2.0.0.zip
    ```

    For a Windows environment:

    ```bash
    > unzip alfresco-identity-service-2.0.0.zip
    ```

3. Change directory to the `bin` directory of the unzipped folder and run the start script:

    For a Linux or Unix environment:

    ```bash
    $ cd alfresco-identity-service-2.0.0/bin
    $ ./kc.sh start --import-realm --http-relative-path="/auth" --hostname=<HOSTNAME> --https-certificate-file=<PATH_TO_CERT_FILE> --https-certificate-key-file=<PATH_TO_CERT_KEY_FILE>
    $ # alternatively, without HTTPS:
    $ ./kc.sh start --import-realm --http-relative-path="/auth" --hostname=<HOSTNAME> --http-enabled=true --hostname-strict-https=false
    ```

    For a Windows environment using a bat script:

    ```bash
    ...\alfresco-identity-service-2.0.0\bin\kc.bat start --import-realm --http-relative-path="/auth" --hostname=<HOSTNAME> --https-certificate-file=<PATH_TO_CERT_FILE> --https-certificate-key-file=<PATH_TO_CERT_KEY_FILE>
    :: alternatively, without HTTPS:
    ...\alfresco-identity-service-2.0.0\bin\kc.bat start --import-realm --http-relative-path="/auth" --hostname=<HOSTNAME> --http-enabled=true --hostname-strict-https=false
    ```

4. Navigate to `http://localhost:8080/auth` once the service has started.

5. Enter a username and password to create an administrator user for the master realm.

The administrator console for the `Alfresco` realm can be accessed at `http://localhost:8080/auth/admin/alfresco/console/`. The administrator user for this realm has the following credentials:

|Property|Value|
|--------|-----|
|Administrator username|`admin`|
|Administrator password|`admin`|
|Administrator email address|`admin@app.activiti.com`|
|Alfresco client redirect URIs|`*`|

> **Important:** Reset the administrator password for the `Alfresco` realm when first signing into its administrator console.

The Identity Service can be [configured]({% link identity-service/latest/config/index.md %}) further.
---
title: Supported platforms
---

The following are the supported platforms for the Identity Service version 2.0:

| Version | Notes |
| ------- | ----- |
| Alfresco Content Services 23.1.x | Content Services supports the use of CMIS and authentication with the v1 REST APIs using the Identity Service. ADF and other modules are not currently supported for authentication. |
| Content Services 7.4 | Content Services supports the use of CMIS and authentication with the v1 REST APIs using the Identity Service. ADF and other modules are not currently supported for authentication. |
| Content Services 7.3.1 | Content Services supports the use of CMIS and authentication with the v1 REST APIs using the Identity Service. ADF and other modules are not currently supported for authentication. |
| | |
| **Integrations** | Check the individual documentation on prerequisites and supported platforms for each integration. Check the compatibility of each integration in your installed version of [Alfresco Content Services]({% link content-services/latest/support/index.md %}). |
| Digital Workspace | |
| Office Services | |
| Sync Service | Not currently supported with Kerberos |
| Desktop Sync | Not currently supported with Kerberos |
| Process Services | |
| Alfresco iOS APS Mobile App | Not currently supported with Kerberos |
---
title: Tutorials
---

The tutorials for the Identity Service include how to set up Single Sign On (SSO) capabilities for Alfresco products using LDAP, SAML and Kerberos.

> **Note:** If you've installed Content Services 7.2 or older versions, you'll need to use the SSO Guide v1 provided in the previous version of the Identity Service (v1.8):
>
> * [Single Sign On Guide v1 (ACS 7.2 and older)]({% link identity-service/1.8/tutorial/sso-v1/index.md %})
---
title: Single Sign On Guide v2 (ACS 7.3+)
---

This documentation describes the configuration required to setup Single Sign On (SSO) capabilities for Alfresco products. Single Sign On refers to the ability for users to access Alfresco Share, the Alfresco Digital Workspace, and Alfresco Process Services in a single browser session by signing in only once to any of the applications.

**This guide applies to Alfresco Content Services 7.3 and above.**

> **Note:** If you've installed Content Services 7.2 or older versions, you'll need to use the SSO Guide v1 provided in the previous version of the Identity Service (v1.8):
>
> * [Single Sign On Guide v1 (ACS 7.2 and older)]({% link identity-service/1.8/tutorial/sso-v1/index.md %})

## Before you begin

See the [supported platforms]({% link identity-service/latest/support/index.md %}) for the combinations of products and versions that are supported for SSO.

## Authentication types

There are different authentication methods that can be used to configure SSO with. Each of these has additional prerequisites and detailed configuration steps:

* Kerberos
* LDAP
* SAML

## Post-configuration

The following are items to be aware of after configuring SSO:

* The Alfresco Process Services Administrator Application is not covered by SSO and is accessed using basic authentication.

* If not using a Microsoft device and browser, users will be prompted to enter their credentials again when editing documents in Microsoft Office utilizing Alfresco Office Services (AOS).

* User permissions need to be managed in individual products. For example, deactivating a user in Alfresco Content Services will not stop the same user from accessing Alfresco Process Services.
---
title: Kerberos
---

The configuration for Kerberos authentication will allow users to access Alfresco products by entering their credentials only once when logging into their Windows environment.

The following diagram illustrates the components and authentication flow for a Kerberos setup:

![Kerberos authentication diagram]({% link identity-service/images/1-5-kerberos.png %})

## Prerequisites

The following are the prerequisites needed to configure SSO with Kerberos:

* The [correct product versions]({% link identity-service/latest/support/index.md %}) of the Alfresco software you are using.
* A Kerberos Key Distribution Center (KDC).
* An instance of Active Directory.
* Administrator access to all systems.

## Configuration

There are five steps to configuring SSO using Kerberos with Alfresco products. The following are the host names used as examples throughout the configuration:

* Alfresco Content Services: `repo.example.com`
* Alfresco Share: `share.example.com`
* Alfresco Digital Workspace: `adw.example.com`
* Alfresco Process Services: `aps.example.com`
* Active Directory: `ldap.example.com`
* Load Balancer: `alfresco.example.com`

> **Note:** If using a containerized deployment there are [several amendments and additions](#optional-containerized-deployment) required for certain steps.

## Step 1: Configure Kerberos files

A user account and `keytab` file is required for Alfresco Content Services (ACS), Alfresco Share and Alfresco Process Services (APS) and a `krb5.conf` file that details the location of the authentication server needs to be located on each server. The files can be configured against a load balancer.

The following table explains the values used to generate the `keytab` and `krb5.conf` files:

| Variable | Description |
| -------- | ----------- |
| host | A server host or load balancer name without a domain suffix, for example `alfresco` |
| domain| The Domain Name System (DNS) domain, for example `example.com` |
| domainnetbios | The Windows domain NetBIOS name, for example `example` |
| REALM | The DNS domain in uppercase, for example `EXAMPLE.COM` |

1. Create a user account in Active Directory for the SSO authentication filters:
    * Enter a full name such as `HTTP alfresco`.
    * Enter a login name such as `httpalfresco`.
    * Enable the setting **Do not require Kerberos pre-authentication**.
2. Use the `ktpass` command to generate a key table for the user account created in the previous step:

    ```bash
    ktpass -princ HTTP/<host>.<domain>@<REALM> -pass <password> -mapuser
    <domainnetbios>\http<host> -crypto all -ptype KRB5_NT_PRINCIPAL -out
    c:\temp\http<host>.keytab -kvno 0
    ```

    For example:

    ```bash
    ktpass -princ HTTP/alfresco.example.com@EXAMPLE.COM -pass <password> -mapuser
    example\httpalfresco -crypto all -ptype KRB5_NT_PRINCIPAL -out
    c:\temp\httpalfresco.keytab -kvno 0
    ```

3. Use the `setspn` command to create Service Principal Names (SPN) for the user account created in the first step:

    ```bash
    setspn -a HTTP/<host> http<host>
    setspn -a HTTP/<host>.<domain> http<host>
    ```

    For example:

    ```bash
    setspn -a HTTP/alfresco httpalfresco
    setspn -a HTTP/alfresco.example.com httpalfresco
    ```

4. In the **Delegation** tab of the **Properties** of the user account created in the first step, tick the **Trust this user for delegation to any service (Kerberos only)** checkbox.
5. Copy the key table file created to a protected area on each server such as `C:\etc`.

    > **Note:** The servers to copy the key table file to are Alfresco Content Services, Alfresco Share and Alfresco Process Services.

6. Configure a `krb5.conf` file that contains details of the authentication server:

    ```bash
    [libdefaults]
    default_realm = <REALM>
    default_tkt_enctypes = rc4-hmac
    default_tgs_enctypes = rc4-hmac

    [realms]
    <REALM> = {
            kdc = <host>.<domain>
            admin_server = <host>.<domain>
              }

    [domain_realm]
    <host>.<domain> = <REALM>
    .<host>.<domain> = <REALM>
    ```

    The following is an example `krb5.conf` file:

    ```bash
    [libdefaults]
    default_realm = EXAMPLE.COM
    default_tkt_enctypes = rc4-hmac
    default_tgs_enctypes = rc4-hmac

    [realms]
    EXAMPLE.COM = {
                kdc = ldap.example.com
                admin_server = ldap.example.com
                  }

    [domain_realm]
    ldap.example.com = EXAMPLE.COM
    .ldap.example.com = EXAMPLE.COM
    ```

7. Copy the `krb5.conf` file to the servers running Alfresco Content Services, Alfresco Share and Alfresco Process Services. By default it is located in `$WINDIR\krb5.conf` where `$WINDIR` is the location of the Windows directory such as `C:\Windows\krb5.conf`.

## Step 2: Configure Alfresco Content Services (ACS)

The Java login files need to be updated with details of the Kerberos configuration and the `alfresco-global.properties` updated to enable SSO using Kerberos.

1. Configure or create the Java configuration file `java.login.config` located in `/java/conf/security`. The following is an example of a `java.login.config` file. The important properties to set are `keyTab` and `principal`.

    * `keyTab` is the location of the [`keytab` file](#step-1-configure-kerberos-files) copied to the ACS server
    * `principal` is in the format `HTTP/<host>.<domain>`

    ```bash
    Alfresco {
      com.sun.security.auth.module.Krb5LoginModule sufficient;
    };

    AlfrescoHTTP
    {
      com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        useKeyTab=true
        doNotPrompt=true
        keyTab="/etc/kerberos.keytab"
        principal="HTTP/alfresco.example.com";
    };

      com.sun.net.ssl.client {
        com.sun.security.auth.module.Krb5LoginModule sufficient;
    };

    other {
      com.sun.security.auth.module.Krb5LoginModule sufficient;
    };
    ```

2. Edit the following line in the Java security configuration file `java.security` by default located in `java/conf/security/`to point to the `java.login.config` file using the full file path:

    ```bash
    login.config.url.1=file:<installLocation>/java/conf/security/java.login.config
    ```

3. Use the following configuration parameters in an `alfresco-global.properties` file:

    | Property | Description |
    | -------- | ----------- |
    | authentication.chain | The authentication chain needs to be set for Kerberos, for example: `kerberos,alfrescoNtlm1:alfrescoNtlm` |
    | kerberos.authentication.realm | The Kerberos realm to authenticate against. The realm name is the domain name in uppercase, for example: `EXAMPLE.COM` |
    | kerberos.authentication.sso.enabled | Sets whether authentication using Kerberos is enabled or not |
    | kerberos.authentication.sso.fallback.enabled | Sets whether a fallback authentication mechanism such as database credentials is used |
    | kerberos.authentication.user.configEntryName | The name of the entry in the Java Authentication and Authorization Service (JAAS) file used for password-based authentication. The default value of `Alfresco` is recommended |

## Step 3: Configure Alfresco Share

The Java login files need to be updated with details of the Kerberos configuration and the `share-config-custom.xml` file edited to enable SSO using Kerberos.

1. Configure or create the Java configuration file `java.login.config` located in `/java/conf/security`. The following is an example of a `java.login.config` file. The important properties to set are `keyTab` and `principal`.

    * `keyTab` is the location of the [`keytab` file](#step-1-configure-kerberos-files) copied to the ACS server
    * `principal` is in the format `HTTP/<host>.<domain>`

    ```bash
    Alfresco {
      com.sun.security.auth.module.Krb5LoginModule sufficient;
    };

    ShareHTTP
    {
      com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        useKeyTab=true
        doNotPrompt=true
        keyTab="/etc/kerberos.keytab"
        principal="HTTP/alfresco.example.com";
    };

      com.sun.net.ssl.client {
        com.sun.security.auth.module.Krb5LoginModule sufficient;
    };

    other {
      com.sun.security.auth.module.Krb5LoginModule sufficient;
    };
    ```

    > **Note:** If Alfresco Share is hosted on the same server as Alfresco Content Services then the contents of the `java.login.config` can be merged into a single file.

2. Edit the following line in the Java security configuration file `java.security` by default located in `java/conf/security/`to point to the `java.login.config` file using the full file path:

    ```bash
    login.config.url.1=file:<installLocation>/java/conf/security/java.login.config
    ```

3. Open the `share-config-custom.xml` file:

    * Update the `<realm>`property with the [realm name](#step-1-configure-kerberos-files), for example `<realm>EXAMPLE.COM</realm>`.
    * Update the `<endpoint-spn>` property with the [SPN value](#step-1-configure-kerberos-files), for example `<endpoint-spn>HTTP/alfresco@EXAMPLE.COM</endpoint-spn>`
    * Uncomment the **two** sections that begin with: `<config evaluator="string-compare" condition="Remote">`
    * Navigate to the `<!--- Kerberos settings --->` section and replace `condition="KerberosDisabled"` with `condition="Kerberos"`

    > **Note:** For Kerberos to work with user names that contain non-ASCII characters, add the following option to `JAVA_OPTS` for the Share JVM:
    >
    > ```bash
    > -Dsun.security.krb5.msinterop.kstring=true
    > ```

## Step 4: Configure Alfresco Digital Workspace

The Alfresco Digital Workspace requires one property added to enable Kerberos SSO. This can be added in the `app.config.json`, located by default in the `/src`directory.

The following is the property to add to the `app.config.json`:

```json
 "auth": {
      "withCredentials": true
}
```

## Step 5: Configure Alfresco Process Services

The Java login files need to be updated with details of the Kerberos configuration and the `activiti-ldap.properties` updated to enable SSO using Kerberos.

1. Configure or create the Java configuration file `java.login.config` located in `/java/conf/security`. The following is an example of a `java.login.config` file. The important properties to set are `keyTab` and `principal`.

    * `keyTab` is the location of the [`keytab` file](#step-1-configure-kerberos-files) copied to the ACS server
    * `principal` is in the format `HTTP/<host>.<domain>`

    ```bash
    Alfresco {
      com.sun.security.auth.module.Krb5LoginModule sufficient;
    };

    AlfrescoHTTP
    {
      com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        useKeyTab=true
        doNotPrompt=true
        keyTab="/etc/kerberos.keytab"
        principal="HTTP/alfresco.example.com";
    };

      com.sun.net.ssl.client {
        com.sun.security.auth.module.Krb5LoginModule sufficient;
    };

    other {
      com.sun.security.auth.module.Krb5LoginModule sufficient;
    };
    ```

2. Edit the following line in the Java security configuration file `java.security` by default located in `java/conf/security/`to point to the `java.login.config` file using the full file path:

    ```bash
    login.config.url.1=file:<installLocation>/java/conf/security/java.login.config
    ```

3. Use the following configuration parameters in an `activiti-ldap-properties` file:

    | Property | Description |
    | -------- | ----------- |
    | kerberos.authentication.enabled | Sets whether authentication via Kerberos is enabled. This needs to be set to `true` to setup SSO using Kerberos, for example `true` |
    | kerberos.authentication.principal | The Service Principal Name (SPN) to authenticate against, for example `HTTP/alfresco.example.com` |
    | kerberos.authentication.keytab | The location of key table file, for example `C:/alfresco/alfrescohttp.keytab` |
    | kerberos.authentication.krb5.conf | The location of the Kerberos ini file, for example `C:/Windows/krb5.ini` |
    | kerberos.allow.ldap.authentication.fallback |Sets whether to allow sign in from unsupported browsers using LDAP credentials, for example `false` |
    | kerberos.allow.database.authentication.fallback | Sets whether to allow sign in from unsupported browsers using database credentials, for example `true` |
    | kerberos.allow.samAccountName.authentication | Sets whether authentication can use the short form such as `username` rather than `username@domain.com`, for example `true` |
    | security.authentication.use-externalid | A setting that enables authentication through Kerberos, for example `true` |
    | ldap.authentication.enabled | Sets whether LDAP authentication is enabled. This setting needs to be set to `true` for SSO to work for Kerberos, for example `true` |

## (Optional) Containerized deployment

In a containerized deployment it is assumed that a load balancer is used to route traffic to the relevant applications. The Active Directory instance used to authenticate users with in a containerized Kerberos scenario is also more likely to exist outside of the domain of the Alfresco applications.

### Kerberos configuration files

In [Step 1](#step-1-configure-kerberos-files) the `keytab` and `krb5.conf` files need to be edited if the Active Directory instance is in a separate domain.

1. The `keytab` file can be configured to refer to an Active Directory instance in a separate domain if necessary.

    For example:

    ```bash
    ktpass -princ HTTP/alfresco.example.com@AD-SSO.EXAMPLE.COM -pass PASSWORD -mapuser 
    ad-sso\httpsalfresco -crypto all -ptype KRB5_NT_PRINCIPAL -out 
    c:\temp\httpalfresco.keytab -kvno 0
    ```

    Where `alfresco.example.com` is the load balancer address, `AD-SSO.EXAMPLE.COM` is the domain of the Active Directory instance and `ad-sso` is the `domainnetbios` of the Active Directory instance.

2. The `krb5.conf` uses the internal IP address of the Active Directory container.

    For example:

    ```bash
    [libdefaults]
    default_realm = AD-SSO.EXAMPLE.COM
    default_tkt_enctypes = rc4-hmac
    default_tgs_enctypes = rc4-hmac

    [realms]
    AD-SSO.EXAMPLE.COM = {
              kdc = ec2amaz-5gk9lmd.ad-sso.example.com
              }

    [domain_realm]
    ec2amaz-5gk9lmd.ad-sso.example.com = AD-SSO.EXAMPLE.COM
    .ec2amaz-5gk9lmd.ad-sso.example.com = AD-SSO.EXAMPLE.COM
    ```

### Share configuration file

The same edits need to be carried out on the [`share-config-custom.xml`](#step-3-configure-alfresco-share) however the `<realm>` will be the Active Directory domain name and the `<endpoint-spn>` will use the load balancer address and Active Directory domain.

For example:

```bash
<realm>AD-SSO.EXAMPLE.COM</realm>
<endpoint-spn>HTTP/alfresco.example.com@AD-SSO.EXAMPLE.COM</endpoint-spn>
```

### Dockerfiles

In a containerized deployment, the updated files will need to be copied to the relevant application containers to overwrite the existing files with the correct configuration. This can be achieved by using the Dockerfile to update each container.

The following files need to be overwritten:

| Application | File |
| ----------- | ---- |
| Alfresco Content Services | `krb5.conf` |
| | `kerberos.keytab` |
| | `java.login.config` |
| | `java.security` |
| | `alfresco-globabl.properties` |
| | |
| Alfresco Share | `krb5.conf` |
| | `kerberos.keytab` |
| | `java.login.config` |
| | `java.security` |
| | `share-config-custom.xml` |
| | |
| Alfresco Digital Workspace | `app.config.json` |
| | |
| Alfresco Process Services | `krb5.conf` |
| | `kerberos.keytab` |
| | `java.login.config` |
| | `java.security` |
| | `activiti-ldap.properties` |

The following is an example Dockerfile used to overwrite the files in the Alfresco Process Services container assuming the new files are in a directory called `/config/`:

```dockerfile
FROM alfresco/process-services:1.10.0

COPY config/krb5.conf /etc/krb5.conf
COPY config/kerberos.keytab /etc/kerberos.keytab
COPY config/java.login.config /usr/java/default/conf/security/java.login.config
COPY config/java-aps.security /usr/java/default/conf/security/java.security
COPY config/activiti-ldap.properties /usr/local/tomcat/lib/activiti-ldap.properties
```

### Clustered deployments

If using a clustered deployment on Kubernetes set `sessionAffinity: ClientIP` on the Alfresco Content Services service so that client requests are passed to the same pod. The [Kubernetes documentation](https://kubernetes.io/docs/concepts/services-networking/service/#proxy-mode-ipvs){:target="_blank"} provides further information on this setting.

## Verify the configuration

To verify that SSO is working correctly after configuring Kerberos, the following are required:

* A Windows client machine that is part of the domain and has a browser installed that is configured to use Kerberos authentication.

The following is an example sequence to follow to verify that SSO works correctly:

1. Sign in to the Windows client machine as the user configured in [Step 1](#step-1-configure-kerberos-files).
2. Open a new browser session and navigate to the Alfresco Digital Workspace at the URL `http://adw.example.com/workspace` and there should be no additional sign in step required.
3. Create a new tab in the same browser session and navigate to Alfresco Share at the URL `http://share.example.com/share` and there should be no additional sign in step required.
4. Create a new tab in the same browser session and navigate to Alfresco Process Services at the URL `http://aps.example.com/activiti-app` and there should be no additional sign in step required.
---
title: LDAP
---

The configuration for LDAP authentication will allow users to access Alfresco products in a single browser session by entering their credentials only once and authenticating against an LDAP directory.

The following diagram illustrates the components and authentication flow for an LDAP setup:

![LDAP authentication diagram]({% link identity-service/images/1-5-ldap.png %})

As shown in the diagram, the Identity Service is used to authenticate the Alfresco Digital Workspace, Alfresco Share, and Alfresco Process Services.

Alfresco Share is configured to authenticate against the Identity Service using a SAML connection, however this does not require a SAML identity provider to be used.

Alfresco Content Services and Alfresco Process Services are configured directly to the Identity Service instance so that the Identity Service can authenticate a user when it is contacted by the respective web application.

The LDAP directory is used for user and group management and is configured to synchronize users to the Identity Service, Alfresco Content Services and Alfresco Process Services individually.

## Prerequisites

The following are the prerequisites needed to configure SSO with LDAP:

* The [correct product versions]({% link identity-service/latest/support/index.md %}) of the Alfresco software you are using.
* The Identity Service is installed.
* An LDAP directory.
* Administrator access to all systems.

## Configuration

There are ten steps to configuring SSO using an LDAP directory with Alfresco products. The following are the host names used as examples throughout the configuration:

* Alfresco Content Services: `repo.example.com`
* Alfresco Share: `share.example.com`
* Alfresco Digital Workspace: `adw.example.com`
* Alfresco Process Services: `aps.example.com`
* Identity Service: `ids.example.com`
* LDAP Directory: `ldap.example.com`
  * OpenLDAP was used for testing purposes.

It is also assumed that certificates are correctly set up for each host and that each host exposes its service solely via TLS on the default port (443).

## Step 1: Configure a realm and clients

A realm and client need to be configured in the Identity Service for the Alfresco products to sit under. A single realm is required and the client will be used for all services other than Alfresco Share and Alfresco Office Services (AOS).

1. Sign in to the administrator console of the Identity Service as an administrator. The URL of the Identity Service administrator console is `https://ids.example.com/auth/admin`.

2. Select the default realm, `Alfresco` or create a new realm to use that the Alfresco products will be accessed through. Note down the **Name** for later use. The realm `Alfresco` will be used in this example.

3. Select **Tokens** and set a timeout period in the **Realm Settings** for the realm `Alfresco`.

4. Use the default client under the `Alfresco` realm or create a new client and configure it. Make sure that at least the following are set:

    * The client is **Enabled**.
    * A **Client ID** is set.
    * **Implicit Flow Enabled** is switched on.
    * A wildcard `*` is entered for **Valid Redirect URIs**.

5. To configure single logout for Process Services add the following URL into the **Admin URL**: `aps.example.com/activiti-app`.

6. Create a new client for Alfresco Share under the `Alfresco` realm or the realm you created, setting at least the following:

    * **Client ID** is set to a valid value (for example, `share`).
    * **Enabled** is set to true.
    * **Client Protocol** is set to `openid-connect`.
    * **Access Type** is set to `public`.
    * **Standard Flow** is enabled.
    * **Valid Redirect URIs** is set to `*`.

## Step 2: Configure LDAP synchronization

An LDAP directory needs to be synchronized with the Identity Service, Alfresco Content Services (ACS) and Alfresco Process Services (APS). The following steps detail the synchronization with the Identity Service, whilst the configuration to ACS and APS is covered in later steps.

1. Sign in to the administrator console of the Identity Service as an administrator. The URL of the Identity Service administrator console is `https://ids.example.com/auth/admin`.

2. Select **User Federation** and **Add provider...** then choose **ldap**.

3. Choosing a **Vendor** will auto-populate many of the fields.

4. Enter the **Connection URL** for the LDAP instance in the format:
    * `ldap//ldap.example.com:389` or
    * `ldaps//ldap.example.com:636` for SSL-enabled installations

5. Set the **Batch Size** and whether to use **Full Sync** and/or **Period Changed Users Sync** followed by the associated **Sync Periods**.

6. Save the configuration.

## Step 3: Configure Alfresco Content Service properties

The properties listed that need to be set for Alfresco Content Services (ACS) are only those that are required for setting up SSO. They include the synchronization with an LDAP directory and the location of a SAML keystore. The Alfresco Share configuration file also requires updating to enable SSO.

1. Use the following configuration parameters either in an `alfresco-global.properties` file, via the repository config map in Kubernetes or as environment variables in a docker-compose file:

    | Property | Description |
    | -------- | ----------- |
    | authentication.chain | The authentication chain needs to be set for the Identity Service and LDAP synchronization, for example `identity-service-1:identity-service,alfrescoNtlm-1:alfrescoNtlm,ldap-1:ldap`|
    |identity-service.auth-server-url|The base URL of the Identity Service, for example `https://ids.example.com/auth`|
    |identity-service.enable-basic-auth | Sets whether basic authentication is also supported by the Identity Service, for example `true`|
    |identity-service.realm | The realm name configured in the Identity Service for the Alfresco applications, for example `alfresco`|
    |identity-service.resource|The **Client ID** set up in the Identity Service for Alfresco Content Services. The client needs to exist underneath the realm set for `identity-service.realm`, for example `alfresco`|
    |ldap.authentication.active | Sets whether LDAP authentication is enabled or not. This needs to be set to `false` to use SAML authentication via the Identity Service, for example `false`|
    |ldap.synchronization.active|Sets whether LDAP synchronization is enabled or not. This needs to be set to `true` to sync users with the repository, for example `true`|
    |ldap.synchronization.java.naming. security.authentication | The mechanism to use to authenticate with the LDAP server, for example `simple`|
    |ldap.synchronization.java.naming. security.principal|The user principal name (UPN) of the account used to retrieve account details for all users and groups, for example `alfresco@domain.com`|
    |ldap.synchronization.java.naming.security.credentials | The password for the account set in `ldap.synchronization.java.naming.security.principal`, for example `secret`|
    |ldap.*|There are several optional [configuration]({% link content-services/latest/admin/auth-sync.md %}#ldapconfprops) and [synchronization]({% link content-services/latest/admin/auth-sync.md %}#synchronization-configuration-properties) properties|
    |csrf.filter.referer | The referer value of ACS to prevent Cross Site Request Forgery (CSRF), for example `https://repo.example.com`|
    |csrf.filter.origin | The origin value of ACS to prevent Cross Site Request Forgery (CSRF), for example `https://repo.example.com/*`|

2. Update the `share-config-custom.xml` file located by default in `$ALFRESCO_HOME/tomcat/shared/classes/alfresco/web-extension/`:

    * Set the `CSRFPolicy` to true as in the following example:

        ```xml
        <config evaluator="string-compare" condition="CSRFPolicy" replace="true">
        ```

3. Sign in to the administrator console of ACS as an administrator. The URL of the administrator console is `https://repo.example.com:443/alfresco/service/enterprise/admin`.

4. Navigate to **Directories** > **Directory Management** and click **Run Synchronize** to perform a manual LDAP sync.

5. Sign into Share as an administrator. The URL for Share is `https://share.example.com/share`.

6. Navigate to **Admin Tools** > **Users** to verify that all user accounts have been synchronized correctly.

## Step 4: Configure Alfresco Digital Workspace

Alfresco Digital Workspace only requires its properties to be updated to enable SSO. For manual deployments these can be updated in the `app.config.json` file and for Docker and Kubernetes deployments using environment variables.

| Property | Environment variable | Description |
| -------- | -------------------- | ----------- |
| authType | APP_CONFIG_AUTH_TYPE |The authentication type. Must be set to `OAUTH`|
| host | APP_CONFIG_OAUTH2_HOST |The address of the Identity Service including the realm name configured in [step 1](#step-1-configure-a-realm-and-clients). In the example the realm name is *Alfresco*|
| clientId | APP_CONFIG_OAUTH2_CLIENTID |The name of the client configured in [step 1](#step-1-configure-a-realm-and-clients) for Digital Workspace|
| implicitFlow | APP_CONFIG_OAUTH2_IMPLICIT_FLOW | |
| silentLogin | APP_CONFIG_OAUTH2_SILENT_LOGIN |Setting `silentLogin` to true removes a login page from displaying if a user is already authenticated. Setting the value to `false` will display a sign in page even though a user needs to only select the **Sign in** option and not enter any credentials|
| redirectSilentIframeUri | APP_CONFIG_OAUTH2_REDIRECT_SILENT_IFRAME_URI |The address that Digital Workspace uses to refresh authorization tokens|
| redirectUri | APP_CONFIG_OAUTH2_REDIRECT_LOGIN |The URL to redirect to after a user is successfully authenticated|
| redirectUriLogout | APP_CONFIG_OAUTH2_REDIRECT_LOGOUT |The URL to redirect to after a user successfully signs out|

> **Note:** If `implicitFlow` is set to `false` the grant type `password` will be used instead.

The following is an example `app.config.json` file excerpt. By default this file is located in the `/src` directory.

```json
"authType": "OAUTH",
"oauth2": {
        "host": "https://ids.example.com/auth/realms/alfresco",
        "clientId": "alfresco",        
        "scope": "openid",
        "implicitFlow": true,
        "silentLogin": true,
        "redirectSilentIframeUri": "https://adw.example.com/workspace/assets/silent-refresh.html",
        "redirectUri": "/workspace/",
        "redirectUriLogout": "/workspace/logout"
        }
```

## Step 5: Configure Alfresco Share properties

The properties listed that need to be set for Alfresco Share are only those that are required for setting up SSO.

Use the following configuration parameters either in the `share-config.properties` file, using the share config map in Kubernetes, or as environment variables in a Docker Compose file:

|Property|Description|
|--------|-----------|
| aims.enabled | Enables or disables Identity Service, for example `true`. |
| aims.realm | The name of the realm, for example `alfresco`. |
| aims.resource | The Client ID of the application, for example `share`. |
| aims.authServerUrl | The base URL of the Identity Service, for example `https://ids.example.com` |
| aims.publicClient | If set to `true`, the adapter will not send credentials for the client to Identity Service. |

## Step 6: (Optional) Configure Alfresco Sync Service

If Alfresco Sync Service is used and a client has been created for it in [step 2](#step-2-configure-clients-for-alfresco-content-services) then the following properties need to be set in the `sync/service-sync/config.yml`:

| Property | Description |
| -------- | ----------- |
| identity-service.auth-server-url |The base URL of the Identity Service, for example `https://ids.example.com/auth`|
| identity-service.realm |The realm name configured in the Identity Service for the Alfresco application, for example `alfresco`|
| identity-service.resource |The **Client ID** set up in the Desktop Sync for Alfresco Content Services. The client needs to exist underneath the realm set for `identity-service.realm`, for example `desktop-sync`|
| identity-service.public-client |The adapter will not send credentials for the client to the Identity Service if this is set to true, for example `true`|
| identity-service.credentials.secret |The secret key for this client if the access type is not set to public.|

## Step 7: Configure Alfresco Process Services

Alfresco Process Services (APS) has two sets of properties that need to be configured to setup SSO. One set synchronizes APS with an LDAP directory and the other set configure with the Identity Service.

1. Configuration for LDAP synchronization can be achieved manually for WAR file deployments using the `activiti-ldap-properties` file or reference an external file for Docker and Kubernetes deployments:

    | Property | Description |
    | -------- | ----------- |
    | ldap.authentication.enabled |Sets whether LDAP authentication is enabled. This needs to be `false` as LDAP is only being used for user synchronization, for example `false`|
    | ldap.authentication.java.naming.provider.url |The URL of the LDAP instance, for example `ldaps://ldap.example.com:636`|
    | ldap.synchronization.java.naming.security.principal |The user used to access the LDAP directory to perform the synchronization, for example `uid=admin,ou=system`|
    | ldap.synchronization.java.naming.security.credentials |The password for the user set in `ldap.synchronization.java.naming.security.principal`, for example `secret`|
    | ldap.synchronization.full.enabled | Sets whether full LDAP synchronization is enabled or not, for example `true`|
    | ldap.synchronization.full.cronExpression |The cron expression describing how often the full synchronization should run, for example `0 0 0 * * ?`|
    | ldap.synchronization.differential.enabled |Sets whether differential LDAP synchronization is enabled or not, for example `true`|
    | ldap.synchronization.differential.cronExpression |The cron expression describing how often the differential synchronization should run, for example `0 0 */4 * * ?`|
    | ldap.synchronization.userSearchBase |The section of the LDAP directory to restrict user synchronization to, for example `ou=users,dc=alfresco,dc=com`|
    | ldap.synchronization.groupSearchBase |The section of the LDAP directory to restrict group synchronization to, for example `ou=groups,dc=alfresco,dc=com`|

2. Configuration with the Alfresco Process Services can be achieved manually for WAR file deployments using the `activiti-identity-service.properties` or reference an external file for Docker and Kubernetes deployments:

    | Property | Description |
    | -------- | ----------- |
    | keycloak.enabled |Sets whether Process Services will use the Identity Service to authenticate against, for example `true`|
    | keycloak.realm |The realm name configured in the Identity Service for the Alfresco applications, for example `alfresco`|
    | keycloak.auth-server-url |The base URL of the Identity Service, for example `https://ids.example.com/auth`|
    | keycloak.ssl-required |Sets whether SSL is mandatory for access or not, for example `all`|
    | keycloak.resource |The **Client ID** set up in the Identity Service for Process Services. The client needs to exist underneath the realm set for `keycloak.realm` or `IDENTITY_SERVICE_REALM`, for example `alfresco`|
    | keycloak.principal-attribute |The attribute to identify users by for authentication. This needs to be set to `email` for Process Services, for example `email`|
    | keycloak.public-client |The adapter will not send credentials for the client to the Identity Service if this is set to `true`, for example `true`|
    | keycloak.always-refresh-token |Sets whether a token should be refreshed for every request or not, for example `true`|
    | keycloak.autodetect-bearer-only |This should be set to true to serve both a web application and web services, for example `true`|
    | keycloak.token-store |The location of where account information token should be stored, for example `cookie`|
    | keycloak.enable-basic-auth |Sets whether basic authentication is also supported by the Identity Service, for example `true`|

## Step 8: (Optional) Configure a connection between Process Services and Content Services

An SSO connection can be configured between Process Services and Content Services so that communication between the two systems is achieved using tokens instead of stored credentials when executing processes.

1. Set these additional properties in `activiti-identity-service.properties`:

    | Property | Description |
    | -------- | ----------- |
    | alfresco.content.sso.enabled |Sets whether SSO is enabled between Process Services and Content Services, for example `${keycloak.enabled}`|
    | alfresco.content.sso.client_id |The **Client ID** within the realm that points to Process Services, for example `${keycloak.resource}`|
    | alfresco.content.sso.client_secret |The secret key for the Process Services client, for example `${keycloak.credentials.secret}`|
    | alfresco.content.sso.realm |The realm that is configured for the Content Services and Process Services clients, for example `${keycloak.realm}`|
    | alfresco.content.sso.scope |Sets the duration that tokens are valid for. For example using the value `offline_access` a token is valid even after a user logs out as long as the token is used at least once every 30 days. See the [Keycloak documentation](https://www.keycloak.org/docs/21.1.2/server_admin/#_offline-access){:target="_blank"} for further information, for example `offline_access`|
    | alfresco.content.sso.javascript_origins |The base URL for the Javascript origins of the Process Services instance, for example `https://aps.example.com`|
    | alfresco.content.sso.auth_uri |The authorization URL, for example `https://ids.example.com/realms/alfresco/protocol/openid-connect/auth`|
    | alfresco.content.sso.token_uri |The authorization token URL, for example `https://ids.example.com/realms/alfresco/protocol/openid-connect/token`|
    | alfresco.content.sso.redirect_uri |The redirect URI for authorization. The value in the example column needs to be updated with the correct base URL for the Process Services instance, for example`https://aps.example.com/activiti-app/rest/integration/sso/confirm-auth-request`|

2. Sign into Process Services as an administrator.

3. Navigate to **Identity Management** > **Tenants** > **Alfresco Repositories**.

4. Add a new repository or edit an existing connection.

5. Configure the following settings for the repository connection:

    | Setting | Description |
    | ------- | ----------- |
    |Name|A name for the repository connection.|
    |Alfresco tenant|The tenant to create the repository under.|
    |Repository base URL|The base URL of the repository instance to connect to.|
    |Share base URL|The base URL of Share for the repository instance to connect to.|
    |Alfresco version|The version of Content Services to connect to.|
    |Authentication type|Select **Identity Service authentication** to use SSO.|

## Step 9: (Optional) Configure a mobile client for Process Services

If Process Services for mobile is required then a client needs to be created for it in the Identity Service to enable SSO capability. The redirect URI is preconfigured for the mobile application using the operating system it is installed on, which means that the **Valid Redirect URIs** value in the Identity Service must match this value.

1. Sign in to the administrator console of the Identity Service as an administrator. The URL of the Identity Service administrator console is `https://ids.example.com/auth/admin`.

2. Create a new client for the mobile application under the `Alfresco` realm or the realm you created in [step 1](#step-1-configure-a-realm-and-clients) and set at least the following in the **Settings** tab:

    **iOS**

    * A unique and identifiable **Client ID**. The default value is `alfresco-ios-aps-app`.
    * The **Valid Redirect URI** must be set to `iosapsapp://aims/auth`.
    * **Implicit Flow Enabled** is switched off.

    **Android**

    * A unique and identifiable **Client ID**. The default value is `alfresco-android-aps-app`.
    * The **Valid Redirect URI** must be set to `androidapsapp://aims/auth`.
    * **Implicit Flow Enabled** is switched off.

## Step 10: (Optional) Configure a client for Content Services for iOS

If Content Services for iOS is required then a client needs to be created for it in the Identity Service to enable SSO capability. The redirect URI is preconfigured for the mobile application using the operating system it is installed on, which means that the **Valid Redirect URIs** value in the Identity Service must match this value.

1. Sign in to the administrator console of the Identity Service as an administrator. The URL of the Identity Service administrator console is `https://ids.example.com/auth/admin`.

2. Create a new client for the mobile application under the `Alfresco` realm or the realm you created in [step 1](#step-1-configure-a-realm-and-clients) and set at least the following in the **Settings** tab:

    * A unique and identifiable **Client ID**. The default value is `alfresco-ios-acs-app`.
    * The **Valid Redirect URI** must be set to `iosacsapp://aims/auth`.
    * **Implicit Flow Enabled** is switched off.

## Verify the configuration

After configuring SSO with an LDAP directory, the following is an example sequence to follow to verify that SSO works correctly:

1. Open a new browser session and navigate to Alfresco Digital Workspace at the URL `http://adw.example.com/workspace`. Sign in to the SAML provider when redirected.

2. Create a new tab in the same browser session and navigate to Alfresco Share at the URL `http://share.example.com/share` and there should be no additional sign in step required.

3. Create a new tab in the same browser session and navigate to Alfresco Process Services at the URL `http://aps.example.com/activiti-app` and there should be no additional sign in step required.

> **Note:** If timeout is configured in the [Identity Service](#step-1-configure-a-realm-and-clients) accessing any of the applications after the specified time will prompt a user to sign in again.
---
title: SAML
---

The configuration for SAML authentication allows users to access Alfresco products in a single browser session by entering their credentials only once and authenticating against a SAML identity provider. An LDAP directory is used for user and group management.

The following diagram illustrates the components and authentication flow for a SAML setup:

![SAML authentication diagram]({% link identity-service/images/1-5-saml.png %})

As shown in the diagram, a connection to the SAML identity provider is configured within Identity Service in order to authenticate Alfresco Share, Alfresco Digital Workspace, and Alfresco Process Services. This also includes setting up a service provider within the SAML identity provider for Identity Service.

Alfresco Content Services and Alfresco Process Services are configured directly to the Identity Service instance so that the Identity Service can authenticate a user when it is contacted by the respective web application.

The LDAP directory is used for user and group management and is configured to synchronize users to the Identity Service, Alfresco Content Services and Alfresco Process Services individually.

## Prerequisites

The following are the prerequisites needed to configure SSO with SAML:

* The [correct product versions]({% link identity-service/latest/support/index.md %}) of the Alfresco software you are using.
* The Identity Service is installed.
* A SAML identity provider
* An LDAP directory
* Administrator access to all systems

## Configuration

There are thirteen steps to configuring SSO using a SAML identity provider with Alfresco products. The following are the host names used as examples throughout the configuration:

* Alfresco Content Services: `repo.example.com`
* Alfresco Share: `share.example.com`
* Alfresco Digital Workspace: `adw.example.com`
* Alfresco Process Services: `aps.example.com`
* Identity Service: `ids.example.com`
* SAML Identity Provider: `saml.example.com`
  * PingFederate was used for testing purposes.
* LDAP Directory: `ldap.example.com`
  * OpenLDAP was used for testing purposes.

It is also assumed that certificates are correctly set up for each host and that each host exposes its service solely via TLS on the default port (443).

## Step 1: Configure a realm and clients

A realm and client need to be configured in the Identity Service for the Alfresco products to sit under. A single realm is required, however multiple clients may be used instead of the single one used in this example.

A separate client always needs to be created and configured for Desktop Sync if it is used. The configuration steps for this additional client can be ignored if Desktop Sync is not used.

1. Sign in to the administrator console of the Identity Service as an administrator. The URL of the Identity Service administrator console is `https://ids.example.com/auth/admin`.
2. Select the default realm, `Alfresco` or create a new realm to use that the Alfresco products will be accessed through. Note down the **Name** for later use. The realm `Alfresco` will be used in this example.
3. Select **Tokens** and set a timeout period in the **Realm Settings** for the realm `Alfresco`.
4. Use the default client under the `Alfresco` realm or create a new client and configure it. Make sure that at least the following are set:
    * The client is **Enabled**.
    * A **Client ID** is set.
    * **Implicit Flow Enabled** is switched on.
    * A wildcard `*` is entered for **Valid Redirect URIs**.
5. To configure single logout for Process Services add the following URL into the **Admin URL**: `aps.example.com/activiti-app`.

6. Create a new client for Alfresco Share under the `Alfresco` realm or the realm you created, setting at least the following:

    In the **Settings** tab:

    * **Client ID** is set to a valid value, for example `share`.
    * **Enabled** must be set to true.
    * **Client Protocol** is set to `openid-connect`.
    * **Access Type** is set to public.
    * **Standard Flow** is enabled.
    * **Valid Redirect URIs** is set to `*`.

7. Create a new client for Desktop Sync under the `Alfresco` realm or the realm you created setting at least the following :

    In the **Settings** tab:

    * A unique and identifiable **Client ID** .
    * The **Valid Redirect URI** must be set to `http://127.0.0.1*, http://localhost*`.
    * **Implicit Flow Enabled** is switched off.

## Step 2: Configure LDAP synchronization

An LDAP directory needs to be synchronized with the Identity Service, Alfresco Content Services (ACS) and Alfresco Process Services (APS). The following steps detail the synchronization with the Identity Service, whilst the configuration to ACS and APS is covered in later steps.

1. Sign in to the administrator console of the Identity Service as an administrator. The URL of the Identity Service administrator console is `https://ids.example.com/auth/admin`.
2. Select **User Federation** and **Add provider...** then choose **ldap**.
3. Choosing a **Vendor** will auto-populate many of the fields.
4. Enter the **Connection URL** for the LDAP instance in the format:
    * `ldap//ldap.example.com:389` or
    * `ldaps//ldap.example.com:636` for SSL-enabled installations
5. Set the **Batch Size** and whether to use **Full Sync** and/or **Period Changed Users Sync** followed by the associated **Sync Periods**.
6. Save the configuration.

## Step 3: Configure a service provider for the Identity Service

A Service provider needs to be set up in the SAML identity provider for the Identity Service using a certificate generated by the Identity Service API.

1. Use the Identity Service certificate descriptor API. The URL of the API is `https://ids.example.com/auth/realms/alfresco/protocol/saml/descriptor`.
2. Copy the value of `<dsig:X509Certificate>`.
3. Paste the value of `<dsig:X509Certificate>` into a new text file between the `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----` commands. The following is an example of a completed text file:

    ```bash
    -----BEGIN CERTIFICATE-----
    MIICnzCCAYcCBgFkqEAQCDANBgkqhkiG9w0BAQsFADATMREwDwYDVQQDDAhhbGZyZXNjbzA
    -----END CERTIFICATE-----
    ```

4. Save the file with the file extension `.cert`.
5. Sign into the SAML identity provider as an administrator and configure a new service provider:

    * The base URL to use is: `https://ids.example.com/`.
    * Use the certificate created in the previous step.
    * The redirect URI to use will be in the format `https://ids.example.com/auth/realms/alfresco/broker/saml/endpoint`.

    > **Note:** The alfresco part of the URL is the name of the realm configured in [step 1](#step-1-configure-a-realm-and-clients). Make sure this is changed if you used a different realm name.

6. Export or note down the details of the newly created service provider to import into the Identity Service in the following step.

## Step 4: Configure a service provider connection

The Identity Service needs to have a connection to the SAML identity provider configured. This can be setup manually or by importing connection details from an external file.

1. Sign in to the administrator console of the Identity Service as an administrator and select the `Alfresco` realm. The URL of the Identity Service administrator console is `https://ids.example.com/auth/admin`.
2. Select **Identity Providers** and **Add provider...** then choose **SAML v2.0**.
3. Enter an **Alias** for the provider.

    > **Note:** The **Alias** will appear on the sign in page to users when they first sign in to an Alfresco application.

4. Manually configure the connection settings in the Identity Service to match the SAML provider or use the import function to import the settings from a file.
5. Set the **Name ID Policy Format** to `Unspecified`.
6. Save the configuration.

## Step 5: (Optional) Enforcing SAML

Enforcing SAML removes the option for users to sign into Alfresco products with basic authentication and only displays the option for a SAML sign in.

1. Sign in to the administrator console of the Identity Service as an administrator and select the `Alfresco` realm. The URL of the Identity Service administrator console is `https://ids.example.com/auth/admin`.
2. Select **Authentication** and navigate to the **Flows** tab.
3. `Browser` in the dropdown list and select **Action** > **Config** for the **Identity Provider Redirector** row.
4. Fill in the resulting form with the details of the SAML identity provider configured in [step 4](#step-4-configure-a-service-provider-connection).

    > **Important:** The **Alias** and **Default Identity Provider** need to match the values configured in [step 4](#step-4-configure-a-service-provider-connection).

## Step 6: Configure Alfresco Content Services properties

The properties listed that need to be set for Alfresco Content Services (ACS) are only those that are required for setting up SSO. They include the synchronization with an LDAP directory and updating the Alfresco Share configuration file to enable SSO. A timeout period can also be set for Share.

1. Use the following configuration parameters either in an `alfresco-global.properties` file, via the repository config map in Kubernetes or as environment variables in a docker-compose file:

    | Property | Description |
    | -------- | ----------- |
    | authentication.chain | The authentication chain needs to be set for the Identity Service and LDAP synchronization, for example `identity-service-1:identity-service,alfrescoNtlm-1:alfrescoNtlm,ldap-1:ldap`|
    |identity-service.auth-server-url|The base URL of the Identity Service, for example `https://ids.example.com/auth`|
    |identity-service.enable-basic-auth | Sets whether basic authentication is also supported by the Identity Service, for example `true`|
    |identity-service.realm | The realm name configured in the Identity Service for the Alfresco applications, for example `alfresco`|
    |identity-service.resource|The **Client ID** set up in the Identity Service for Alfresco Content Services. The client needs to exist underneath the realm set for `identity-service.realm`, for example `alfresco`|
    |ldap.authentication.active | Sets whether LDAP authentication is enabled or not. This needs to be set to `false` to use SAML authentication via the Identity Service, for example `false`|
    |ldap.synchronization.active|Sets whether LDAP synchronization is enabled or not. This needs to be set to `true` to sync users with the repository, for example `true`|
    |ldap.synchronization.java.naming. security.authentication | The mechanism to use to authenticate with the LDAP server, for example `simple`|
    |ldap.synchronization.java.naming. security.principal|The user principal name (UPN) of the account used to retrieve account details for all users and groups, for example `alfresco@domain.com`|
    |ldap.synchronization.java.naming.security.credentials | The password for the account set in `ldap.synchronization.java.naming.security.principal`, for example `secret`|
    |ldap.*|There are several optional [configuration]({% link content-services/latest/admin/auth-sync.md %}#ldapconfprops) and [synchronization]({% link content-services/latest/admin/auth-sync.md %}#synchronization-configuration-properties) properties|
    |csrf.filter.referer | The referer value of ACS to prevent Cross Site Request Forgery (CSRF), for example `https://repo.example.com`|
    |csrf.filter.origin | The origin value of ACS to prevent Cross Site Request Forgery (CSRF), for example `https://repo.example.com/*`|

2. Update the `share-config-custom.xml` file located by default in `$ALFRESCO_HOME/tomcat/shared/classes/alfresco/web-extension/`:

    * Set the `CSRFPolicy` to true as in the following example:

        ```xml
        <config evaluator="string-compare" condition="CSRFPolicy" replace="true">
        ```

3. Set a session timeout in both `web.xml` files located by default in `$ALFRESCO_HOME/tomcat/webapps/share/WEB-INF` and `$ALFRESCO_HOME/tomcat/webapps/alfresco/WEB-INF`. This should match the value [configured for the realm](#step-1-configure-a-realm-and-clients).

    The following is an example of the property to add:

    ```xml
    <session-config>
        <session-timeout>720</session-timeout>
    </session-config>
    ```

    > **Note:** This example sets a session time of 12 hours.

4. Sign in to the administrator console of ACS as an administrator. The URL of the administrator console is `https://repo.example.com:443/alfresco/service/enterprise/admin`.
5. Navigate to **Directories** > **Directory Management** and click **Run Synchronize** to perform a manual LDAP sync.
6. Sign into Share as an administrator. The URL for Share is `https://share.example.com/share`.
7. Navigate to **Admin Tools** > **Users** to verify that all user accounts have been synchronized correctly.

## Step 7: Configure Alfresco Digital Workspace

Alfresco Digital Workspace only requires its properties to be updated to enable SSO. For manual deployments these can be updated in the `app.config.json` file and for Docker and Kubernetes deployments using environment variables.

| Property                       | Environment variable                         | Description                                                                                                                                                                                                                                                  |
|--------------------------------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| authType                       | APP_CONFIG_AUTH_TYPE                         | The authentication type. Must be set to `OAUTH`                                                                                                                                                                                                              |
| oauth2.host                    | APP_CONFIG_OAUTH2_HOST                       | The address of the Identity Service including the realm name configured in [step 1](#step-1-configure-a-realm-and-clients). In the example the realm name is *Alfresco*                                                                                      |
| oauth2.clientId                | APP_CONFIG_OAUTH2_CLIENTID                   | The name of the client configured in [step 1](#step-1-configure-a-realm-and-clients) for Digital Workspace                                                                                                                                                   |
| oauth2.implicitFlow            | APP_CONFIG_OAUTH2_IMPLICIT_FLOW              |                                                                                                                                                                                                                                                              |
| oauth2.silentLogin             | APP_CONFIG_OAUTH2_SILENT_LOGIN               | Setting `silentLogin` to true removes a login page from displaying if a user is already authenticated. Setting the value to `false` will display a sign in page even though a user needs to only select the **Sign in** option and not enter any credentials |
| oauth2.redirectSilentIframeUri | APP_CONFIG_OAUTH2_REDIRECT_SILENT_IFRAME_URI | The address that Digital Workspace uses to refresh authorization tokens                                                                                                                                                                                      |
| oauth2.redirectUri             | APP_CONFIG_OAUTH2_REDIRECT_LOGIN             | The URL to redirect to after a user is successfully authenticated                                                                                                                                                                                            |
| oauth2.redirectUriLogout       | APP_CONFIG_OAUTH2_REDIRECT_LOGOUT            | The URL to redirect to after a user successfully signs out                                                                                                                                                                                                   |

> **Note:** If `implicitFlow` is set to `false` the grant type `password` will be used instead.

The following is an example `app.config.json` file excerpt. By default this file is located in the `/src` directory.

```json
"authType": "OAUTH",
"oauth2": {
        "host": "https://ids.example.com/auth/realms/alfresco",
        "clientId": "alfresco",        
        "scope": "openid",
        "implicitFlow": true,
        "silentLogin": true,
        "redirectSilentIframeUri": "https://adw.example.com/workspace/assets/silent-refresh.html",
        "redirectUri": "/workspace/",
        "redirectUriLogout": "/workspace/logout"
        }
```

## Step 8: Configure Alfresco Share properties

The properties listed that need to be set for Alfresco Share are only those that are required for setting up SSO.

Use the following configuration parameters either in the `share-config.properties` file, using the share config map in Kubernetes, or as environment variables in a Docker Compose file:

|Property|Description|
|--------|-----------|
| aims.enabled | Enables or disables Identity Service, for example `true`. |
| aims.realm | The name of the realm, for example `alfresco`. |
| aims.resource | The Client ID of the application, for example `share`. |
| aims.authServerUrl | The base URL of the Identity Service, for example `https://ids.example.com` |
| aims.publicClient | If set to `true`, the adapter will not send credentials for the client to Identity Service. |

## Step 9: (Optional) Configure Alfresco Sync Service

If Alfresco Sync Service is used and a client has been created for it in [step 1](#step-1-configure-a-realm-and-clients) then the following properties need to be set in the `sync/service-sync/config.yml`:

| Property | Description |
| -------- | ----------- |
| identity-service.auth-server-url |The base URL of the Identity Service, for example `https://ids.example.com/auth`|
| identity-service.realm |The realm name configured in the Identity Service for the Alfresco application, for example `alfresco`|
| identity-service.resource |The **Client ID** set up in the Desktop Sync for Alfresco Content Services. The client needs to exist underneath the realm set for `identity-service.realm`, for example `desktop-sync`|
| identity-service.public-client |The adapter will not send credentials for the client to the Identity Service if this is set to true, for example `true`|
| identity-service.credentials.secret |The secret key for this client if the access type is not set to public.|

## Step 10: Configure Alfresco Process Services

Alfresco Process Services (APS) has two sets of properties that need to be configured to setup SSO. One set synchronizes APS with an LDAP directory and the other set configure with the Identity Service.

1. Configuration for LDAP synchronization can be achieved manually for WAR file deployments using the `activiti-ldap-properties` file or reference an external file for Docker and Kubernetes deployments:

    | Property | Description |
    | -------- | ----------- |
    | ldap.authentication.enabled |Sets whether LDAP authentication is enabled. This needs to be `false` as LDAP is only being used for user synchronization, for example `false`|
    | ldap.authentication.java.naming.provider.url |The URL of the LDAP instance, for example `ldaps://ldap.example.com:636`|
    | ldap.synchronization.java.naming.security.principal |The user used to access the LDAP directory to perform the synchronization, for example `uid=admin,ou=system`|
    | ldap.synchronization.java.naming.security.credentials |The password for the user set in `ldap.synchronization.java.naming.security.principal`, for example `secret`|
    | ldap.synchronization.full.enabled | Sets whether full LDAP synchronization is enabled or not, for example `true`|
    | ldap.synchronization.full.cronExpression |The cron expression describing how often the full synchronization should run, for example `0 0 0 * * ?`|
    | ldap.synchronization.differential.enabled |Sets whether differential LDAP synchronization is enabled or not, for example `true`|
    | ldap.synchronization.differential.cronExpression |The cron expression describing how often the differential synchronization should run, for example `0 0 */4 * * ?`|
    | ldap.synchronization.userSearchBase |The section of the LDAP directory to restrict user synchronization to, for example `ou=users,dc=alfresco,dc=com`|
    | ldap.synchronization.groupSearchBase |The section of the LDAP directory to restrict group synchronization to, for example `ou=groups,dc=alfresco,dc=com`|

2. Configuration with the Alfresco Process Services can be achieved manually for WAR file deployments using the `activiti-identity-service.properties` or reference an external file for Docker and Kubernetes deployments:

    | Property | Description |
    | -------- | ----------- |
    | keycloak.enabled |Sets whether Process Services will use the Identity Service to authenticate against, for example `true`|
    | keycloak.realm |The realm name configured in the Identity Service for the Alfresco applications, for example `alfresco`|
    | keycloak.auth-server-url |The base URL of the Identity Service, for example `https://ids.example.com/auth`|
    | keycloak.ssl-required |Sets whether SSL is mandatory for access or not, for example `all`|
    | keycloak.resource |The **Client ID** set up in the Identity Service for Process Services. The client needs to exist underneath the realm set for `keycloak.realm` or `IDENTITY_SERVICE_REALM`, for example `alfresco`|
    | keycloak.principal-attribute |The attribute to identify users by for authentication. This needs to be set to `email` for Process Services, for example `email`|
    | keycloak.public-client |The adapter will not send credentials for the client to the Identity Service if this is set to `true`, for example `true`|
    | keycloak.always-refresh-token |Sets whether a token should be refreshed for every request or not, for example `true`|
    | keycloak.autodetect-bearer-only |This should be set to true to serve both a web application and web services, for example `true`|
    | keycloak.token-store |The location of where account information token should be stored, for example `cookie`|
    | keycloak.enable-basic-auth |Sets whether basic authentication is also supported by the Identity Service, for example `true`|

## Step 11: (Optional) Configure a connection between Process Services and Content Services

An SSO connection can be configured between Process Services and Content Services so that communication between the two systems is achieved using tokens instead of stored credentials when executing processes.

1. Set these additional properties in `activiti-identity-service.properties`:

    | Property | Description |
    | -------- | ----------- |
    | alfresco.content.sso.enabled |Sets whether SSO is enabled between Process Services and Content Services, for example `${keycloak.enabled}`|
    | alfresco.content.sso.client_id |The **Client ID** within the realm that points to Process Services, for example `${keycloak.resource}`|
    | alfresco.content.sso.client_secret |The secret key for the Process Services client, for example `${keycloak.credentials.secret}`|
    | alfresco.content.sso.realm |The realm that is configured for the Content Services and Process Services clients, for example `${keycloak.realm}`|
    | alfresco.content.sso.scope |Sets the duration that tokens are valid for. For example using the value `offline_access` a token is valid even after a user logs out as long as the token is used at least once every 30 days. See the [Keycloak documentation](https://www.keycloak.org/docs/21.1.2/server_admin/#_offline-access){:target="_blank"} for further information, for example `offline_access`|
    | alfresco.content.sso.javascript_origins |The base URL for the Javascript origins of the Process Services instance, for example `https://aps.example.com`|
    | alfresco.content.sso.auth_uri |The authorization URL, for example `https://ids.example.com/realms/alfresco/protocol/openid-connect/auth`|
    | alfresco.content.sso.token_uri |The authorization token URL, for example `https://ids.example.com/realms/alfresco/protocol/openid-connect/token`|
    | alfresco.content.sso.redirect_uri |The redirect URI for authorization. The value in the example column needs to be updated with the correct base URL for the Process Services instance, for example`https://aps.example.com/activiti-app/rest/integration/sso/confirm-auth-request`|

2. Sign into Process Services as an administrator.
3. Navigate to **Identity Management** > **Tenants** > **Alfresco Repositories**.
4. Add a new repository or edit an existing connection.
5. Configure the following settings for the repository connection:

    |Setting|Description|
    |-------|-----------|
    |Name|A name for the repository connection.|
    |Alfresco tenant|The tenant to create the repository under.|
    |Repository base URL|The base URL of the repository instance to connect to.|
    |Share base URL|The base URL of Share for the repository instance to connect to.|
    |Alfresco version|The version of Content Services to connect to.|
    |Authentication type|Select **Identity Service authentication** to use SSO.|

## Step 12: (Optional) Configure a mobile client for Process Services

If Process Services for mobile is required then a client needs to be created for it in the Identity Service to enable SSO capability. The redirect URI is preconfigured for the mobile application using the operating system it is installed on, which means that the **Valid Redirect URIs** value in the Identity Service must match this value.

1. Sign in to the administrator console of the Identity Service as an administrator. The URL of the Identity Service administrator console is `https://ids.example.com/auth/admin`.
2. Create a new client for the mobile application under the `Alfresco` realm or the realm you created in [step 1](#step-1-configure-a-realm-and-clients) and set at least the following in the **Settings** tab:

    **iOS**

    * A unique and identifiable **Client ID**. The default value is `alfresco-ios-aps-app`.
    * The **Valid Redirect URI** must be set to `iosapsapp://aims/auth`.
    * **Implicit Flow Enabled** is switched off.

    **Android**

    * A unique and identifiable **Client ID**. The default value is `alfresco-android-aps-app`.
    * The **Valid Redirect URI** must be set to `androidapsapp://aims/auth`.
    * **Implicit Flow Enabled** is switched off.

## Step 13: (Optional) Configure a client for Content Services for iOS

If Content Services for iOS is required then a client needs to be created for it in the Identity Service to enable SSO capability. The redirect URI is preconfigured for the mobile application using the operating system it is installed on, which means that the **Valid Redirect URIs** value in the Identity Service must match this value.

1. Sign in to the administrator console of the Identity Service as an administrator. The URL of the Identity Service administrator console is `https://ids.example.com/auth/admin`.
2. Create a new client for the mobile application under the `Alfresco` realm or the realm you created in [step 1](#step-1-configure-a-realm-and-clients) and set at least the following in the **Settings** tab:

    * A unique and identifiable **Client ID**. The default value is `alfresco-ios-acs-app`.
    * The **Valid Redirect URI** must be set to `iosacsapp://aims/auth`.
    * **Implicit Flow Enabled** is switched off.

## Verify the configuration

After configuring SSO using SAML, the following is an example sequence to follow to verify that SSO works correctly:

1. Open a new browser session and navigate to Alfresco Digital Workspace at the URL `http://adw.example.com/workspace`. Sign in to the SAML provider when redirected.
2. Create a new tab in the same browser session and navigate to Alfresco Share at the URL `http://share.example.com/share` and there should be no additional sign in step required.
3. Create a new tab in the same browser session and navigate to Alfresco Process Services at the URL `http://aps.example.com/activiti-app` and there should be no additional sign in step required.

> **Note:** If timeout is configured using the same value for the Identity Service and ACS, accessing any of the applications after the specified time will prompt a user to sign in again.
---
title: Upgrade Identity Service
---

Use the following information to upgrade the Identity Service to version 2.0.

> **Important:**
>
> * Upgrading the Identity Service requires downtime and should be performed in a test environment before being attempted in a production environment.
> * After the upgrade the database will no longer be compatible with the old server.

Before performing an upgrade, make sure you review the recommended guidelines in the following sections:

* [Upgrade from version 1.2](#upgrade-v12)
* [Remove SmallRye references](#remove-smallrye-references)
* [Upgrade ZIP installation](#upgrade-zip-installation)
* [Upgrade Kubernetes deployment with PostgreSQL database](#upgrade-kubernetes-deployment-with-postgresql-database)  

For Keycloak's upgrade documentation, see the [Upgrading Guide](https://www.keycloak.org/docs/21.1.2/upgrading/){:target="_blank"}.

## Upgrade from version 1.2 {#upgrade-v12}

If you are currently using the Identity Service 1.2 you must first modify the **_First Broker Login_** authentication before upgrading to version 1.8.

1. Log into the Keycloak administration console and select the **Alfresco** realm.

2. Select **Authentication** from the menu on the left to open the authentication configuration page.

3. Select **First Broker Login** from the dropdown menu.

4. Ensure **Create User If Unique (create unique user config)** flow is set to **ALTERNATIVE**.

**Result:** You can now upgrade directly to version 1.8.

## Remove SmallRye references

You must manually remove all the **_SmallRye_** modules in the `standalone.xml` file before upgrading to version 1.8.

> **Important:** From Keycloak 13.0.0 the modules called **_SmallRye_** have been removed from the [WildFly](https://www.wildfly.org/){:target="_blank"} application. The server will not start if your configuration references them.

See the Keycloak documentation [Migrating to 13.0.0](https://www.keycloak.org/docs/18.0/upgrading/#migrating-to-13-0-0){:target="_blank"} for more information.

## Upgrade from version 1.8

Upgrading from Identity Service 1.8.x to >= 2.0.0 implies migrating from a Wildfly to a Quarkus-based Keycloak distribution. The way Keycloak is structured, configured, and started up changed so it is recommended to go through the [official Keycloak documentation](https://www.keycloak.org/docs/21.1.2/upgrading/){:target="_blank"} to upgrade your current installation without losing critical data.

You can find the full list of potentially relevant migration changes in the Keycloak site, [Migration changes](https://www.keycloak.org/docs/21.1.2/upgrading/index.html#migration-changes){:target="_blank"}, starting with the [Migrating to 19.0.0](https://www.keycloak.org/docs/21.1.2/upgrading/index.html#migrating-to-19-0-0){:target="_blank"} section.

Some of the most noticeable changes are:

| Change | Mitigation |
| ------ | ---------- |
| The `/auth` default HTTP context path has been removed. | The server should be started with `--http-relative-path="/auth"` to restore the context path. |
| The `userinfo` endpoint now requires the provided Access Token to have the `openid` scope. | If you were relying on the `userinfo` endpoint you should make sure that your Access Tokens include the `openid` scope. |
| The `userinfo` endpoint error responses have changed according to [Upgrading Guide](https://www.keycloak.org/docs/21.1.2/upgrading/index.html#userinfo-endpoint-changes){:target="_blank"}. | If you were relying on parsing error responses coming from this endpoint, the relevant code should be reviewed and adapted to the new behavior. |
| `RSA_SHA1` and `DSA_SHA1` algorithms [have been deprecated](https://www.keycloak.org/docs/21.1.2/upgrading/index.html#deprecated-rsa_sha1-and-dsa_sha1-algorithms-for-saml){:target="_blank"} and aren't valid algorithms to sign SAML responses anymore. | Adapt the configuration of your SAML identity provider so that it uses a valid algorithm such as SHA256 instead.<br><br>If the mitigation is not applicable, you can override the `$JAVA_HOME/conf/security/java.security` file and remove the relevant disallowed algorithms within `jdk.xml.dsig.secureValidationPolicy` instead. |
| The embedded H2 database has been upgraded from 1.x to 2.x, making it impossible to simply copy a previous H2 database file and use it in the newer version of Keycloak to retain the data. | If you need to retain the data that was present in an H2 1.x database file, you'll need to migrate it first to an H2 2.x compatible version before copying it into the new installation. |

## Upgrade ZIP installation

Use the following information to upgrade your ZIP installation:

1. Download the `alfresco-identity-service-2.0.0.zip` file from [Hyland Community](https://community.hyland.com/en/products/alfresco/release-notes/release-notes/alfresco-identity-service-version-200){:target="_blank"}.

2. Unzip the ZIP file and configure your installation using the Keycloak documentation: [Upgrading Keycloak](https://www.keycloak.org/docs/21.1.2/upgrading/){:target="_blank"}.

## Upgrade Kubernetes deployment with PostgreSQL database

### Upgrade from chart `>=1.1.0` to `2.1.0`

The upgrade should be seamless.

### Upgrade to chart `>=3.0.0`

1. Identify your chart release name and namespace and save them into variables.

    ```bash
    export RELEASENAME=<Your-Release-Name>
    export RELEASENAMESPACE=<Your-Release-Namespace>
    ```

2. Delete the postgresql StatefulSets.

    ```bash
    kubectl delete statefulsets.apps $RELEASENAME-postgresql-id --cascade=false --namespace $RELEASENAMESPACE
    ```

3. Upgrade Identity Service.

    ```bash
    helm upgrade $RELEASENAME alfresco-stable/alfresco-identity-service --version=3.0.0 --namespace $RELEASENAMESPACE
    ```

4. Delete the postgresql pod.

    ```bash
    kubectl delete pod $RELEASENAME-postgresql-id-0 --namespace $RELEASENAMESPACE
    ```

### Upgrade to chart `>=8.0.0`

The Helm charts are now based on the newer [keycloakx](https://github.com/codecentric/helm-charts/tree/keycloakx-2.2.1/charts/keycloakx){:target="_blank"} codecentric charts which are significantly different from the previous version and include several breaking changes. Refer to the [Keycloak-X documentation](https://github.com/codecentric/helm-charts/blob/keycloakx-2.2.1/charts/keycloakx/README.md){:target="_blank"} to get a clearer understanding of the structure of the new charts. It's also recommended to go through some of the examples to get familiar with the new way of [enabling persistence](https://github.com/codecentric/helm-charts/tree/keycloakx-2.2.1/charts/keycloakx/examples/postgresql){:target="_blank"}.

You'll find additional documentation specific to this version of Identity Service by following these links: [README](https://github.com/Alfresco/alfresco-identity-service/blob/2.0.0/README.md){:target="_blank"}, [helm README](https://github.com/Alfresco/alfresco-identity-service/blob/2.0.0/helm/alfresco-identity-service/README.md){:target="_blank"}.
