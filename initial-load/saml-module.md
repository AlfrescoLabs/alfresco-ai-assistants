---
title: SAML Module for Alfresco Content Services
---

> **Important:** It is recommended to use the SAML Module in conjunction with the [Identity Service single sign on (SSO) guide]({% link identity-service/1.8/tutorial/sso-v1/saml.md %}) when setting up SAML authentication and SSO capabilities. Check the compatibility of your installed products as the SAML configuration has changed since Alfresco Content Services 7.3:
>
> * [Supported platforms for SAML Module]({% link saml-module/latest/support/index.md %})
> * [Supported platforms for Identity Service]({% link identity-service/1.8/support/index.md %})

You can use Security Assertion Markup Language (SAML) with Alfresco to support SAML authentication for Content Services.

SAML standards define an XML-based framework for describing and exchanging security information between an identity provider (IdP) and service provider (SP).

Security information is expressed in the form of portable SAML assertions that applications working across security boundaries can trust.

Alfresco Share uses Web Browser SSO and Single-Logout (SLO) profiles, using the HTTP Post Binding only.

SAML is based on a trust relationship between an IdP (for example, PingFederate or AD FS) and an SP (for example, Alfresco Share) who agree to share authentication information; for example, metadata and configuration information that is required to access services.

Alfresco uses SAML 2.0. See [OASIS SAML v2.0](https://wiki.oasis-open.org/security/FrontPage){: target="_blank"} for more information on SAML specifications.

> **Note:** The SAML Module for Alfresco Content Services 1.2 can be applied to Alfresco Content Services 6.2 - 7.0 only.

This diagram explains the exchange of information between the service provider (in this case, Alfresco Share), and the identity provider (in this case, PingFederate):

![An overview of SAML information exchange]({% link saml-module/images/overview.png %})
---
title: Troubleshoot the SAML Module
---

Use this information to troubleshoot common issues with the SAML Module.

## General troubleshooting tips

Check the IdP server logs for more information.

Check the Alfresco log files. Watch the following packages:

For repository errors:

* `org.alfresco.repo.security.authentication.saml`
* `org.alfresco.repo.web.scripts.saml`

For service provider errors:

* `org.alfresco.web.auth.saml`
* `org.alfresco.web.scripts.saml`
* `org.alfresco.web.site.servlet.saml`

> **Note:** SAML logging is set to INFO by default. You can increase SAML logging in your SAML `log4j.properties` file.

Check the IdP URLs in Alfresco for SSO and SLO match the information provided by your identity provider.

Check the IdP certificate matches the path you have specified in Alfresco, and is valid.

In the IdP, check that you have created a valid user, with a valid email address.

## Troubleshooting REST API and AOS service providers

1. Open the following URL:

    * For REST API: `/alfresco/service/saml/-default-/rest-api/authenticate`

    * For AOS: `/alfresco/service/saml/-default-/aos/authenticate`

2. Check that you are redirected to your IdP.
3. If not, check the IdP SSO URL in the AOS SP config on the Admin Console.
4. Check that the IdP accepts this authentication request. If not (error message in the IdP), check that the IdP certificate and the entity identifier are valid in the AOS SP configuration on the Admin Console.
5. Check the log of your IdP.
6. Log in to your IdP.
7. Check that you are redirected back to `/alfresco/service/saml/-default-/rest-api/authenticate-response` for REST API and `/alfresco/service/saml/-default-/aos/authenticate-response` for AOS. If not, check the configuration of your IdP. It is possible that you may need to configure a return URL for this connection.

Some IdPs will require to specify the format of the data in the URL used. For example:

* For REST AP SP: `http:/localhost:8080/alfresco/service/saml/-default-/rest-api/authenticate-response?format=json`
* For AOS SP: `http:/localhost:8080/alfresco/service/saml/-default-/aos/authenticate-response?format=html`

## Unable to log in to service provider

Check the IdP certificate expiry date.

Ensure that you are using a valid IdP certificate.

If a user exists in the IdP but can't log on to the service provider, then the administrator should check that the user has an email address configured in the IdP.

> **Note:** If you are an Alfresco Administrator with username, **admin**, and you are using Alfresco Share as your service provider, and you need to perform some emergency Share activities, but you can't log in, you can use this URL to bypass SAML-enabled Share: `http://localhost:8080/share/page/?useIdp=false` where `localhost:8080` is your Alfresco host name and port.

If you are using ADFS with Windows 2000 or earlier, Windows requires that special characters are replaced (commonly with an underscore) in the `sAMAccountName`. As a result, either set up Alfresco users with user names that match the `sAMAccountName` or use a different value in the `saml.sp.user.mapping.id` setting.

## SAML information not appearing in the Alfresco Admin Console

If you can't see the SAML page in the Admin Console, it might be that the updated `alfresco.war` has not been deployed.

1. Stop Alfresco.
2. Delete the `tomcat/webapps/alfresco` and `tomcat/webapps/share` folders in the Alfresco installation directory. This forces the `alfresco.war` and `share.war` files to be exploded when Alfresco restarts.
3. Restart Alfresco.
4. Check the Admin Console for the SAML page.

## SAML enabled error messages

* "SAML is enabled but the IdP SSO request URL is invalid"
* "SAML is enabled but the IdP SLO request URL is invalid"
* "SAML is enabled but the IdP SLO response URL is invalid"

Check that you have specified the correct URLs in the SAML IdP settings section in the Admin Console. For example, that you have not entered `https://your-idp-hostname:your-idp-port/idp/SSO.saml2` instead of `https://your-idp-hostname:your-idp-port/idp/SLO.saml2` in the **IdP Single Logout Request Service URL** field.

## IdP request URLs invalid error messages

* "IdP SSO request URL is invalid"
* "IdP SLO request URL is invalid"
* "IdP SLO response URL is invalid"

Check that you have specified the correct URLs in the SAML IdP settings section in the Admin Console. For example, that you have not entered `https://your-idp-hostname:your-idp-port/idp/SSO.saml2` instead of `https://your-idp-hostname:your-idp-port/idp/SLO.saml2` in the **IdP Single Logout Request Service URL** field.

## Certificate invalid error messages

* "SAML is enabled but the IdP certificate path is invalid"
* "IdP certificate path is invalid"

Check that you have specified the correct path to the IdP certificate, or whether the IdP certificate has moved.

## Service provider error messages

* "SAML is enabled but the SP issuer is invalid"
* "SP issuer is invalid"

Check if the issuer property is empty, or contains one of these characters: `"${}"`

## Unsuccessful login error message

* "Your login to Alfresco was unsuccessful."

Check that the user logging on has been set up with an account in both Alfresco and the IdP. If the user doesn't have an account, they can't log in. If you are using LDAP synchronization, check your settings to ensure that the user is created before attempting to log in.

## Error message when trying to log out from the service provider

If you are using AD FS as an IdP, and you log out locally from the IdP, you will get an error message when you attempt to log out from the service provider.

To avoid the error, do not locally sign out from ADFS. Alternatively, on your ADFS page, click the Sign in to one of the following sites option, and choose the URL that relates to your service provider setup. Then you can log out from the service provider successfully.

## Error after redeploying or updating the SAML AMP

After redeploying the SAML AMP, you may get an error during login or logout initiated with SAML. For example, after a SAML version update, you may need to re-upload the IdP certificate using the Admin Console and also upload a new SAML SP certificate inside of your IdP.

Using the Admin Console, check that all the service provider properties are correct.

## Error message if boolean properties have an invalid value

If you enter an incorrect value for a boolean property from JMX using JConsole, you will get a **Startup of 'Search' subsystem, ID: [Search, managed, noindex] failed** error message in the IdP server log.

To resolve this error, use the `revert` method under `SAML/<service_provider>/Operations`.

## Other tips and information

* Depending on the configuration requirements of your application, you can replace all the REST API service provider IDs in the calls to the SAML authentication dance with the value of any other repository type service provider defined in Alfresco.

* If your organization uses SAML to authenticate with (custom) applications other than Share, make sure that the SAML web scripts in the repository side are accessible by all the clients that need access to them.

* It may help you with the configuration of your IdP if you know that you can download the metadata for any of the service provider configured in Alfresco. Go to `http://localhost:8080/alfresco/s/enterprise/admin/admin-saml`, select the tab that you want (for example, REST API), and select **Download SP Metadata**.

* When using the SAML Module, you cannot have an empty authentication chain, as shown:

    ```bash
    authentication.chain=
    ```
---
title: Configure Active Directory
---

The following steps are example instructions for configuring Active Directory Federation Services (ADFS) as the identity provider to use with the SAML Module in Alfresco.

## Prerequisites

* A working domain on your Windows Server
* Active Directory is set up
* Users exist in Active Directory
* Alfresco Content Services is configured for SSL

## Setup steps

1. Run a full LDAP sync. This can be done by restarting Alfresco Content Services.

    > **Note**: If a user exists in LDAP, but not in Alfresco, they will not be able to log in to Alfresco when SAML is enabled. See [Configuring LDAP (Active Directory)]({% link content-services/latest/admin/auth-sync.md %}#configure-ldap) for more information.

2. Install ADFS. For example purposes we will use a domain name of `example.com` and a Federation Service name of `adfs.example.com`.

    Test your AD FS installation by accessing these URLs:

    * `https://adfs.example.com/adfs/ls/idpinitiatedsignon`
    * `https://adfs.example.com/federationmetadata/2007-06/federationmetadata.xml`

    where `adfs.example.com` is your Federation Service Name.

3. Log in to ADFS as an administrator and go to **Account Settings**.

4. In **Idp AuthenticationRequest Service URL**, enter the location of the **SingleSignOnService** element of the ADFS metadata.

    For example `https://adfs.example.com/federationmetadata/2007-06/federationmetadata.xml`

    Alfresco supports the HTTP-POST binding only, so you only need to copy the location of the HTTP-POST services.

    For example:

    ```xml
    <SingleSignOnService Location="https://adfs.example.com/adfs/ls/" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"/>
    ```

5. In **IdP SingleLogoutRequest Service URL** and **IdP SingleLogoutResponse Service URL**, enter the location of the **SingleLogoutService** element of the ADFS metadata.

    For example:

    ```xml
    <SingleLogoutService Location="https://adfs.example.com/adfs/ls/" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"/>
    ```

6. Export the ADFS certificate:

    1. Click **ADFS Management** (**Server Manager > Tools**), then **Service**, then **Certificates**.

    2. In the Token-signing section, right click the certificate and select **View Certificate**.

    3. On the **Details** tab, click **Copy to file** and **Next**.

    4. Select `DER encoded binary X.509 (.CER)`, and click **Next**.

    5. Select where you want to save the file and enter a name for it. Click **Save**, **Next**, and **Finish**.

7. In a browser window, log in to the Admin Console SAML page as an administrator, to upload your exported certificate to Alfresco: `https://localhost:8443/alfresco/service/enterprise/admin/admin-saml`

8. Click **Upload IdP Certificate** to browse to and upload the ADFS certificate you exported in step 6, and click **Save**.

    IdP Certificate Status shows whether the certificate is valid and the expiry date of the current certificate.

    > **Note**: Alfresco Content Services does not allow you to upload an expired certificate.

9. While you are in the Admin Console, click **Download SP Certificate** to download the certificate required by ADFS and **Download SP Metadata** for later use.

10. Add a Relying Party Trust (RPT).

    1. Click A**DFS Management** (**Server Manager > Tools > ADFS Management**), and expand **Trust Relationships**.

    2. Select the **Relying Party Trusts** folder. Right click **Relying Party Trusts** and select **Add Relying Party Trust**.

    3. Click **Start** in the wizard that appears.

    4. In the **Select Data Source** window, select **Enter data about the relying party manually** and click **Next**.

    5. In the **Specify Display Name** window, enter a display name that you'll remember, and any notes that you require. Click **Next**.

    6. In the **Choose Profile** window, click the ADFS profile radio button and click **Next**.

    7. In the **Configure Certificate** window, accept the default certificate settings by clicking **Next**.

    8. In the **Configure URL** window, check **Enable support for the SAML 2.0 WebSSO protocol** box and enter in the **Relying party SAML 2.0 SSO service URL**.

        In your Alfresco metadata, this is the Location value of the AssertionConsumerService element. For example:

        * For Alfresco Share: `https://localhost:8443/share/page/saml-authnresponse`
        * For REST API: `https://localhost:8443/alfresco/service/saml/-default-/rest-api/authenticate-response`
        * For Alfresco Office Services: `https://localhost:8443/alfresco/service/saml/-default-/aos/authenticate-response`

    9. In the **Configure Identifiers** window, enter a relying party trust identifier.

        This value must match the value in the **Entity Identification (Issuer)** field of the Alfresco Admin Console. For example:

        * For Alfresco Share: `https://localhost:8443/share`
        * For REST API: `https://localhost:8443/alfresco`

    10. In the **Configure Multi-factor Authentication Now?** window, click the radio button **I do not want to configure multi-factor authentication settings for this relying party trust at this time** and click Next.

    11. In the **Choose Issuance Authorization Rules** window, click the radio button **Permit all users to access this relying party** and click **Next**.

    12. In the **Ready to Add Trust** window, leave the default settings and click **Next**.

    13. In the **Finish** window, check the check box and click **Close** to exit. The **Edit Claim Rules** editor will open.

11. Create the claim rules.

    > **Note**: If the Edit Claim Rules editor doesn't open after you have created the trust, right click the relying party name that you created in the previous step and select Edit Claim Rule.

    1. In the **Issuance Transform Rules** tab, click **Add Rule** and click **Next**.

    2. In the **Choose Rule Type** window, select **Send LDAP Attributes as Claims** and click **Next**.

    3. In the **Configure Claim Rule** window:

        1. In **Claim rule name**, enter a name for the rule, for example: `LDAP Attributes`.
        2. In **Attribute store**, select **Active Directory**.
        3. In the **Mapping of LDAP attributes to outgoing claim types** table, select **E-Mail Addresses** in the **LDAP Attribute** column and the **Outgoing Claim Type** column.
        4. In the next row, select **SAM-Account-Name** in the **LDAP Attribute** column.
        5. In the next row, select **Name ID** in the **Outgoing Claim Type** column.

            > **Note:** Adding the **Name ID** instructs ADFS to specifically send the SessionIndex with the response. You need the SessionIndex to use Alfresco Single Logout.

    4. Click **Finish** to save the rule and **OK** to complete.

12. Adjust the **Relying Party Trust** settings.

    1. Click A**DFS Management** (**Server Manager > Tools > ADFS Management**), and expand **Trust Relationships**.

    2. Right click the **Relying Party Trust** that you created in step 10 and select **Properties**.

    3. Click the **Advanced** tab, and make sure you select **SHA-256** as the secure hash algorithm. Click **OK**.

    4. Click the **Endpoints** tab, and click **Add SAML** to add a new endpoint.

        1. For **Endpoint** type, select **SAML Logout**.
        2. For **Binding**, select **POST**.
        3. For **Trusted URL**, enter the Alfresco logout request URL. This is the `Location` value in the Alfresco metadata SingleLogoutService element. For example:

            * For Alfresco Share:

                ```xml
                <md:SingleLogoutService
                ...
                Location="https://localhost:8443/share/page/saml-logoutrequest"/>
                ```

            * For REST API:

                ```xml
                <md:SingleLogoutService
                ...
                Location="https://localhost:8443/alfresco/service/saml/-default-/rest-api/logout-request"/>
                ```

            * For Alfresco Office Services:

                ```xml
                <md:SingleLogoutService
                ...
                Location="https://localhost:8443/alfresco/service/saml/-default-/aos/logout-request"/>
                ```

        4. In **Response URL**, enter the Alfresco logout response URL. This is the `ResponseLocation` value in the Alfresco metadata SingleLogoutService element. For example:

            * For Alfresco Share:

                ```xml
                <md:SingleLogoutService 
                ...
                ResponseLocation="https://localhost:8443/share/page/saml-logoutresponse"/>
                ```

            * For REST API:

                ```xml
                <md:SingleLogoutService 
                ...
                ResponseLocation="https://localhost:8443/alfresco/service/saml/-default-/rest-api/logout-response"/>
                ```

            * For Alfresco Office Services:

                ```xml
                <md:SingleLogoutService 
                ...
                ResponseLocation="https://localhost:8443/alfresco/service/saml/-default-/aos/logout-response"/>
                ```

        5. Click **OK**.

    5. Click the **Signature** tab, and **Add** to upload the Alfresco certificate that you downloaded in step 9.

        > **Note:** You may see a warning about the length of a certificate key. You can ignore this message.

    6. Click **OK** to save your changes.

13. Test your setup.

    1. Create a user in the Windows Server Active Directory.

    2. Add an email address for the created user.

        Right click on the user, select Properties, and add the email address that matches your Alfresco instance and Windows server domain. For example, if you have created a user in Alfresco with the username `user1`, ADFS assigns an email address of `user1@example.com`, where `example.com` is the ADFS domain.

    3. Go to `https://adfs.example.com/adfs/ls/idpinitiatedsignon` where `adfs.example.com` is your Federated Service name.

    4. Select the RPT name that you created in step 10 and sign in. You should see confirmation that you are signed in to ADFS.

To troubleshoot ADFS, use the Event Viewer.
---
title: Configure Alfresco products
---

After configuring an identity provider such as [Active Directory]({% link saml-module/latest/config/adfs.md %}) or [PingFederate]({%link saml-module/latest/config/ping.md %}), service providers need to be configured for the features of Alfresco in which you want to enable SAML: Alfresco Share, the REST API and Alfresco Office Services.

The configuration can be done in any of three ways:

* Using the Alfresco Admin Console
* In configuration files, such as `alfresco-global.properties`
* Dynamically, using JMX if enabled

## Alfresco Share

{% capture share-admin %}

### Configure Alfresco Share using the Admin Console

Administrators can enable and configure SAML authentication for Alfresco Share using the Admin Console.

1. Log on to the SAML page of the Alfresco Admin Console with your user credentials: `http://localhost:8080/alfresco/service/enterprise/admin/admin-saml`

2. Select the **Share** tab.

3. Select **Enable SAML (SSO) Authentication**.

    **SAML Status** shows whether SAML is currently enabled or disabled.

4. (Optional) Deselect **Enforce SAML Login**.

    This option is selected by default and all logins to this service provider must use the Identity Provider (IdP). If you do not enforce the SAML login, the user can decide to use either the Alfresco Share login or login using the IdP link.

5. Specify the **Identity Provider (IdP) Description**.

    This description is shown to users as an alternate login option when **Enforce SAML Login** is deactivated. If no description is provided, the text displayed on the Alfresco login screen would read **your single sign-on provider**. Clicking on this description will redirect you to the IdP.

6. Enter the IdP settings:

    | Setting | Description |
    | ------- | ----------- |
    | IdP Authentication Request Service URL | The address where the authentication request is sent. This redirects you to the identity provider login page. For example: `https://pingfederate.alfresco.me:9031/idp/SSO.saml2` |
    | IdP Single Logout Request Service URL | The address where the logout request is sent when logging out of Alfresco Share. This logs you out of Alfresco Share and any other applications that use your SSO setup. For example: `https://pingfederate.alfresco.me:9031/idp/SLO.saml2` |
    | IdP Single Logout Response Service URL | The address where the logout response is sent when the identity provider gets a logout request. For example: `https://pingfederate.alfresco.me:9031/idp/SLO.saml2` |
    | Entity Identification (Issuer) | Some IdPs use the issuer to determine which service provider connection to use. If you are using ADFS, this is the Base URL, for example: `http://localhost:8080/share`. |
    | User ID Mapping | The SAML attribute that maps to an Alfresco User ID. For PingFederate, this maps to `PersonImmutableID`. For ADFS, the SAML attribute is the `Subject/NameID` specified for the SAML subject `NameID`. |

7. Click **Upload IdP Certificate** to browse to and upload the IdP certificate that you downloaded from your identity provider during configuration.

    **IdP Certificate Status** shows whether the certificate is valid, and the expiry date of the current certificate.

    > **Note**: Alfresco Content Services does not allow you to upload an expired certificate.

    > **Note:** If SAML is enabled, Alfresco always checks for an existing certificate.

8. Click **Download SP Certificate** to download the certificate required by your IdP.

    This is a copy of your self-signed certificate. You should have already downloaded this information when setting up your connections in the IdP.

9. Click **Download SP Metadata** if you need to download the service provider signature verification certificate.

    This is required for ADFS configuration, if you are using ADFS as your IdP.

10. Click **Save**.

You can disable these settings by deselecting **Enable SAML (SSO) Authentication**.

{% endcapture %}

{% capture share-properties %}

### Configure Alfresco Share using the `alfresco-global.properties` file

Administrators can enable and configure SAML authentication for Share using the `alfresco-global.properties` file and a combination of subsystem properties files.

The SAML module uses subsystems to control, configure, and extend the service providers that are supported, therefore it is recommended to use this approach when configuring the subsystems. The SAML subsystems can be configured like any other Alfresco subsystem. For more information, see [Extension classpath]({% link content-services/latest/config/subsystems.md %}#extension-classpath).

> **Note:** Properties set in the `alfresco-global.properties file` apply to the entire SAML module, including all the SAML subsystem instances, such as Alfresco Share, REST API, and Alfresco Office Services.

To configure Alfresco Share, create the properties file in the `<classpathRoot>/alfresco/extension/subsystems/SAML/share/share/my-custom-share-sp.properties` directory:

The default `saml.properties` file for Alfresco Share can be found in the `<TOMCAT_HOME>/webapps/alfresco/WEB-INF/classes/alfresco/subsystems/SAML/share` directory. Use this file to copy the SAML settings into your `<classpathRoot>/alfresco/extension/subsystems/SAML/share/share/my-custom-share-sp.properties` file.

**Note:** Changes to `<classpathRoot>/alfresco-global.properties` are applicable in a single service provider scenario only.

If you use multiple service providers, use subsystem extensions for type and instance. For example, for the Alfresco Share service provider, create a `my-custom-share-sp.properties` file with the classpath: `<TOMCAT_HOME>/shared/classes/alfresco/extension/subsystems/SAML/share/share/my-custom-share-sp.properties`.

1. Locate the `<TOMCAT_HOME>/webapps/alfresco/WEB-INF/classes/alfresco/subsystems/SAML/share/saml.properties` file.

    These are the settings:

    ```bash
    #SAML key store configuration
    saml.keystore.location=classpath:alfresco/keystore/saml.keystore
    saml.keystore.keyMetaData.location=classpath:alfresco/keystore/saml-keystore-passwords.properties
    saml.keystore.provider=
    saml.keystore.type=JCEKS

    # Time, in milliseconds, that message state is valid
    # 300000 = 5 minutes
    saml.message.state.duration.in.millis=300000
    # Clock skew - the number of seconds before a lower time bound, or after an upper time bound, to consider still acceptable.
    saml.issueInstantRule.check.clock.skew.in.seconds=60
    # Number of seconds after a message issue instant after which the message is considered expired  expires
    saml.issueInstantRule.check.expiration.in.seconds=30

    # It is RECOMMENDED that a system entity use a URL containing its own domain name to identify itself
    saml.sp.idp.spIssuer.namePrefix=

    # The SAML attribute (or 'Subject/NameID' for SAML subject NameID) to map to the Alfresco user's ID
    saml.sp.user.mapping.id=Subject/NameID

    # The SAML attribute to map to the Alfresco user's email
    saml.sp.user.mapping.email=Email

    # The SAML attribute to map to the Alfresco user's first name
    saml.sp.user.mapping.firstName=GivenName

    # The SAML attribute to map to the Alfresco user's last name
    saml.sp.user.mapping.lastName=Surname

    # Whether or not SAML is enabled for the service provider
    saml.sp.isEnabled=false

    # Whether or not SAML login is enforced
    saml.sp.isEnforced=true

    # IdP description if you choose to enforce SAML login
    saml.sp.idp.description=

    # IdP URL to which the Authentication Request from Alfresco is posted for the service provider
    saml.sp.idp.sso.request.url=

    # IdP URL to which a logout *request* from Alfresco is posted when logging out from the service provider
    saml.sp.idp.slo.request.url=

    # IdP URL to which a logout *response* from Alfresco is posted when receiving a logout request from your IdP for the service provider
    saml.sp.idp.slo.response.url=

    # Path to the certificate used to validate the requests and responses from the IdP
    saml.sp.idp.certificatePath=

    # Entity identification (issuer) for the service provider.  Some IdPs may use this to determine which SP connection to use.
    saml.sp.idp.spIssuer=

    # Some IdPs, like LemonLDAP, may require a specific format for NameID section of the logout request.
    saml.sp.slo.request.nameid.format=
    ```

2. To enable SAML, use these settings in your `<classpathRoot>/alfresco/extension/subsystems/SAML/share/share/my-custom-share-sp.properties` file:

    ```bash
    saml.sp.isEnabled=true
    saml.sp.isEnforced=false
    saml.sp.idp.description=<Identity Provider>
    ```

    * `saml.sp.isEnabled` specifies whether or not SAML is enabled for the service provider.

    * `saml.sp.isEnforced` accepts a boolean value and specifies whether or not SAML login is enforced. If set to `false`, SAML login is not enforced.

    * `saml.sp.idp.description` accepts a string value and specifies the IdP description at the login screen if you choose to not enforce SAML login.

3. Set the Identity Provider (IdP) settings:

    * `saml.sp.idp.sso.request.url`: The address where the authentication request is sent. This redirects you to the identity provider login page.
    * `saml.sp.idp.slo.request.url`: The address where the logout request is sent when logging out of Alfresco. This logs you out of Alfresco and any other applications that use your SSO setup.
    * `saml.sp.idp.slo.response.url`: The address where the logout response is sent when the identity provider gets a logout request.
    * `saml.sp.idp.spIssuer`: Some IdPs use the issuer to determine which service provider connection to use.
    * `saml.sp.user.mapping.id`: The SAML attribute that maps to an Alfresco User ID. The SAML attribute is the `Subject/NameID` specified for the SAML subject `NameID`.

4. Enter a path to the certificate: `saml.sp.idp.certificatePath`

    > **Note:** If SAML is enabled, Alfresco always checks for an existing certificate.

5. Review the other SAML settings in the `saml.properties` file to understand if they apply to your setup.

6. Save and close all the properties files, and restart Alfresco to apply your changes.

{% endcapture %}

{% capture share-jmx %}

### Configure Alfresco Share using JMX

JMX values (Managed Bean or MBean attributes) are exposed in the Alfresco Admin Console and with internal tools (Alfresco JMX Dump) or external tools like JConsole. The SAML Module beans are described here with their default values.

> **Note**: Example values are given. Always check the values in your own system as these can vary depending on the install method or operating system.

> **Important**: Be aware that any changes you make to attributes in the live system are written to the database. The next time that Alfresco starts, these values will take precedence over any values specified in properties files.

The following are the attributes available for `Alfresco:Type=Configuration, Category=SAML, Object Type=SAML$managed$share`:

|Attribute |Example|
|--------------|-------------|
|$type|`share`|
|idpCertificateExpiryDate| |
|idpCertificateSerialNumber| |
|idpCertificateStatus|`missing`|
|idpCertificateSubject| |
|instancePath|`[managed, share]`|
|saml.issueInstantRule.check.clock.skew.in.seconds|`60`|
|saml.issueInstantRule.check.expiration.in.seconds|`30`|
|saml.keystore.keyMetaData.location|`classpath:alfresco/keystore/saml-keystore-passwords.properties`|
|saml.keystore.location|`classpath:alfresco/keystore/saml.keystore`|
|saml.keystore.provider| |
|saml.keystore.type|`JCEKS`|
|saml.message.state.duration.in.millis|`300000`|
|saml.share.spSloRequestURLSuffix|`/saml-logoutrequest`|
|saml.share.spSloResponseURLSuffix|`/saml-logoutresponse`|
|saml.share.spSsoURLSuffix|`/saml-authnresponse`|
|saml.sp.idp.certificatePath|Set the path to the certificate you require|
|saml.sp.idp.slo.request.url| |
|saml.sp.idp.slo.response.url| |
|saml.sp.idp.spIssuer| |
|saml.sp.idp.spIssuer.namePrefix| |
|saml.sp.idp.sso.request.url| |
|saml.sp.isEnabled|`false`|
|saml.sp.isEnforced|`true`|
|saml.sp.idp.description|`<Identity Provider>`|
|saml.sp.user.mapping.email|`Email`|
|saml.sp.user.mapping.firstName|`GivenName`|
|saml.sp.user.mapping.id|`Subject/NameID`|
|saml.sp.user.mapping.lastName|`Surname`|
|spSigningCredentialStatus|`missing`|
|saml.sp.slo.request.nameid.format| |

The following is the attribute available for `Alfresco:Type=Configuration, Category=SAML, Object Type=SAML$manager`:

|Attribute|Example|
|--------------|-------------|
|chain|`share:share,rest-api:repository,aos:repository`|

A [complete list of of Alfresco MBeans]({% link content-services/latest/admin/jmx-reference.md %}) is also available.

{% endcapture %}

{% include tabs.html tableid="share" opt1="Admin Console" content1= share-admin opt2="Properties" content2=share-properties opt3="JMX" content3=share-jmx %}

### Authenticate users for Alfresco Share

After configuring SAML in Alfresco for Share, you can test that everything is set up correctly by doing the following:

1. Verify that the administrator email address is configured correctly in the identity provider.

2. Login to Alfresco Share as the administrator: `http://localhost:8080/share`

    You should get redirected to the login page for the identtiy provider.

3. Enter the administrator's credentials.

    You should get redirected to Alfresco Share.

4. Log out of Alfresco Share.

    If you navigate to your identity provider page, you should also be logged out.

## Alfresco REST API

> **Note**: When SAML is enforced for the REST API any web script authentication calls to the repository will be rejected. A valid authentication ticket can only be [obtained via SAML](#authenticate-users-for-the-rest-api), or an administrator can log into the Admin Console using basic authentication.

{% capture rest-admin %}

### Configure the REST API using the Admin Console

Administrators can enable and configure SAML authentication for the REST API using the Admin Console.

> **Important:** If you enable and enforce SAML for the REST API, all applications using the REST API (such as Alfresco Share) will use SAML as well. This means that Alfresco Share must also have SAML enabled and enforced if the REST API is. The enforce option is ignored if SAML is disabled for the REST API.

1. Log on to the SAML page of the Alfresco Admin Console with your user credentials: `http://localhost:8080/alfresco/service/enterprise/admin/admin-saml`

2. Select the **REST API** tab.

3. Select **Enable SAML (SSO) Authentication**.

4. (Optional) Select **Enforce SAML Login**.

    If this option is selected by default then all logins to this service provider must use the Identity Provider (IdP). If you do not enforce the SAML login, the user can decide to use either the Alfresco login or login using the IdP link.

5. Specify the **Identity Provider (IdP) Description**.

    This description is shown to users as an alternate login option when **Enforce SAML Login** is deactivated. If no description is provided, the text will read **your single sign-on provider**. Clicking on this description will redirect you to the IdP.

6. Enter the IdP settings:

    | Setting | Description |
    | ------- | ----------- |
    | IdP Authentication Request Service URL | The address where the authentication request is sent. This redirects you to the identity provider login page. For example: `https://pingfederate.alfresco.me:9031/idp/SSO.saml2` |
    | IdP Single Logout Request Service URL | The address where the logout request is sent when logging out of Alfresco. This logs you out of Alfresco and any other applications that use your SSO setup. For example: `https://pingfederate.alfresco.me:9031/idp/SLO.saml2` |
    | IdP Single Logout Response Service URL | The address where the logout response is sent when the identity provider gets a logout request. For example: `https://pingfederate.alfresco.me:9031/idp/SLO.saml2` |
    | Entity Identification (Issuer) | Some IdPs use the issuer to determine which service provider connection to use. If you are using ADFS, this is the Base URL, for example: `http://localhost:8080/share`. |
    | User ID Mapping | The SAML attribute that maps to an Alfresco User ID. For PingFederate, this maps to `PersonImmutableID`. For ADFS, the SAML attribute is the `Subject/NameID` specified for the SAML subject `NameID`. |

7. Click **Upload IdP Certificate** to browse to and upload the IdP certificate that you downloaded from your identity provider during configuration.

    **IdP Certificate Status** shows whether the certificate is valid, and the expiry date of the current certificate.

    > **Note**: Alfresco Content Services does not allow you to upload an expired certificate.

    > **Note:** If SAML is enabled, Alfresco always checks for an existing certificate.

8. Click **Download SP Certificate** to download the certificate required by your IdP.

    This is a copy of your self-signed certificate. You should have already downloaded this information when setting up your connections in the IdP.

9. Click **Download SP Metadata** if you need to download the service provider signature verification certificate.

    This is required for ADFS configuration, if you are using ADFS as your IdP.

10. Click **Save**.

You can disable these settings by deselecting **Enable SAML (SSO) Authentication**.

If you want to check if SAML is enabled (or enforced) in your Alfresco server, make a call to:

```http
http://localhost:8080/alfresco/service/saml/-default-/rest-api/enabled
```

where:`-default-` is the tenant name and `rest-api` is the id of the SAML REST API service provider

This will return a JSON response with the information about the REST API service provider, for example:

```json
{
    "entry":
    { 
      "isSamlEnabled": true,
      "isSamlEnforced": true,
      "idpDescription": ".....",
      "tenantDomain": "...."
    }
}
```
{% endcapture %}

{% capture rest-properties %}

### Configure the REST API using the `alfresco-global.properties` file

Administrators can enable and configure SAML authentication for the REST API using the `<classpathRoot>/alfresco-global.properties` file and a combination of subsystem properties files. Use this as an alternative to configuring SAML using the Admin Console.

To configure the REST API, create the properties file in the` <classpathRoot>/alfresco/extension/subsystems/SAML/repository/rest-api/my-custom-rest-api-sp.properties` directory.

The default `saml.properties` file can be found in the `<TOMCAT_HOME>/webapps/alfresco/WEB-INF/classes/alfresco/subsystems/SAML/repository` directory. Use this file to copy the SAML settings into your `<classpathRoot>/alfresco/extension/subsystems/SAML/repository/rest-api/my-custom-rest-api-sp.properties` file.

**Note:** Changes to `<classpathRoot>/alfresco-global.properties` are applicable in a single service provider scenario only.

If you use multiple service providers, use subsystem extensions for type and instance. For example, for the REST API service provider, create a `my-custom-rest-api-sp.properties` file with the classpath: `<TOMCAT_HOME>/shared/classes/alfresco/extension/subsystems/SAML/repository/rest-api/my-custom-rest-api-sp.properties`.

1. Locate the `<TOMCAT_HOME>/webapps/alfresco/WEB-INF/classes/alfresco/subsystems/SAML/repository/saml.properties` file.

    These are the settings:

    ```bash
    #SAML key store configuration
    saml.keystore.location=classpath:alfresco/keystore/saml.keystore
    saml.keystore.keyMetaData.location=classpath:alfresco/keystore/saml-keystore-passwords.properties
    saml.keystore.provider=
    saml.keystore.type=JCEKS

    # Time, in milliseconds, that message state is valid
    # 300000 = 5 minutes
    saml.message.state.duration.in.millis=300000
    # Clock skew - the number of seconds before a lower time bound, or after an upper time bound, to consider still acceptable.
    saml.issueInstantRule.check.clock.skew.in.seconds=60
    # Number of seconds after a message issue instant after which the message is considered expired  expires
    saml.issueInstantRule.check.expiration.in.seconds=30

    # It is RECOMMENDED that a system entity use a URL containing its own domain name to identify itself
    saml.sp.idp.spIssuer.namePrefix=

    # The SAML attribute (or 'Subject/NameID' for SAML subject NameID) to map to the Alfresco user's ID
    saml.sp.user.mapping.id=Subject/NameID

    # The SAML attribute to map to the Alfresco user's email
    saml.sp.user.mapping.email=Email

    # The SAML attribute to map to the Alfresco user's first name
    saml.sp.user.mapping.firstName=GivenName

    # The SAML attribute to map to the Alfresco user's last name
    saml.sp.user.mapping.lastName=Surname

    # Whether or not SAML is enabled for the service provider
    saml.sp.isEnabled=false

    # Whether or not SAML login is enforced
    saml.sp.isEnforced=false

    # IdP description if you choose to enforce SAML login
    saml.sp.idp.description=

    # IdP URL to which the Authentication Request from Alfresco is posted for the service provider
    saml.sp.idp.sso.request.url=

    # IdP URL to which a logout *request* from Alfresco is posted when logging out from the service provider
    saml.sp.idp.slo.request.url=

    # IdP URL to which a logout *response* from Alfresco is posted when receiving a logout request from your IdP for the service provider
    saml.sp.idp.slo.response.url=

    # Path to the certificate used to validate the requests and responses from the IdP
    saml.sp.idp.certificatePath=

    # Entity identification (issuer) for the service provider.  Some IdPs may use this to determine which SP connection to use.
    saml.sp.idp.spIssuer=

    # Provide a ticket to the user after authentication
    saml.sp.outcome.provideTicket=true

    # Establish a session after authentication
    saml.sp.outcome.establishSession=true

    # Some IdPs, like LemonLDAP, may require a specific format for NameID section of the logout request.
    saml.sp.slo.request.nameid.format=
    ```

2. To enable SAML, use these settings in your `<classpathRoot>/alfresco/extension/subsystems/SAML/repository/rest-api/my-custom-rest-api-sp.properties` file:

    ```bash
    saml.sp.isEnabled=true
    saml.sp.isEnforced=false
    saml.sp.idp.description=<Identity Provider>
    ```

    * `saml.sp.isEnabled` specifies whether or not SAML is enabled for the service provider.

    * `saml.sp.isEnforced` accepts a boolean value and specifies whether or not SAML login is enforced. If set to `false`, SAML login is not enforced.

    * `saml.sp.idp.description` accepts a string value and specifies the IdP description at the login screen if you choose to not enforce SAML login.

3. Set the Identity Provider (IdP) settings:

    * `saml.sp.idp.sso.request.url`: The address where the authentication request is sent. This redirects you to the identity provider login page.
    * `saml.sp.idp.slo.request.url`: The address where the logout request is sent when logging out of Alfresco. This logs you out of Alfresco and any other applications that use your SSO setup.
    * `saml.sp.idp.slo.response.url`: The address where the logout response is sent when the identity provider gets a logout request.
    * `saml.sp.idp.spIssuer`: Some IdPs use the issuer to determine which service provider connection to use.
    * `saml.sp.user.mapping.id`: The SAML attribute that maps to an Alfresco User ID. The SAML attribute is the `Subject/NameID` specified for the SAML subject `NameID`.

4. Enter a path to the certificate: `saml.sp.idp.certificatePath`

    > **Note:** If SAML is enabled, Alfresco always checks for a existing certificate.

5. Review the other SAML settings in the saml.properties file to understand if they apply to your setup.

6. Save and close all the properties files, and restart Alfresco to apply your changes.

{% endcapture %}

{% capture rest-jmx %}

### Configure the REST API using JMX

JMX values (Managed Bean or MBean attributes) are exposed in the Alfresco Admin Console and with internal tools (Alfresco JMX Dump) or external tools like JConsole. The SAML Module beans are described here with their default values.

> **Note**: Example values are given. Always check the values in your own system as these can vary depending on the install method or operating system.

> **Important**: Be aware that any changes you make to attributes in the live system are written to the database. The next time that Alfresco starts, these values will take precedence over any values specified in properties files.

The following are the attributes available for `Alfresco:Type=Configuration, Category=SAML, Object Type=SAML$managed$rest-api`:

|Attribute |Example|
|--------------|-------------|
|$type|`repository`|
|idpCertificateExpiryDate| |
|idpCertificateSerialNumber| |
|idpCertificateStatus|`missing`|
|idpCertificateSubject| |
|instancePath|`[managed, rest-api]`|
|saml.issueInstantRule.check.clock.skew.in.seconds|`60`|
|saml.issueInstantRule.check.expiration.in.seconds|`30`|
|saml.keystore.keyMetaData.location|`classpath:alfresco/keystore/saml-keystore-passwords.properties`|
|saml.keystore.location|`classpath:alfresco/keystore/saml.keystore`|
|saml.keystore.provider| |
|saml.keystore.type|`JCEKS`|
|saml.message.state.duration.in.millis|`300000`|
|saml.share.spSloRequestURLSuffix|`/saml-logoutrequest`|
|saml.share.spSloResponseURLSuffix|`/saml-logoutresponse`|
|saml.share.spSsoURLSuffix|`/saml-authnresponse`|
|saml.sp.idp.certificatePath|Set the path to the certificate you require|
|saml.sp.idp.slo.request.url| |
|saml.sp.idp.slo.response.url| |
|saml.sp.idp.spIssuer| |
|saml.sp.idp.spIssuer.namePrefix| |
|saml.sp.idp.sso.request.url| |
|saml.sp.isEnabled|`false`|
|saml.sp.isEnforced|`true`|
|saml.sp.idp.description|`<Identity Provider>`|
|saml.sp.user.mapping.email|`Email`|
|saml.sp.user.mapping.firstName|`GivenName`|
|saml.sp.user.mapping.id|`Subject/NameID`|
|saml.sp.user.mapping.lastName|`Surname`|
|spSigningCredentialStatus|`missing`|
|saml.sp.slo.request.nameid.format| |

The following is the attribute available for `Alfresco:Type=Configuration, Category=SAML, Object Type=SAML$manager`:

|Attribute|Example|
|--------------|-------------|
|chain|`share:share,rest-api:repository,aos:repository`|

A [complete list of of Alfresco MBeans]({% link content-services/latest/admin/jmx-reference.md %}) is also available.

{% endcapture %}

{% include tabs.html tableid="rest" opt1="Admin Console" content1= rest-admin opt2="Properties" content2=rest-properties opt3="JMX" content3=rest-jmx %}

### Authenticate users for the REST API

After configuring SAML for REST API requests in Alfresco users need to be authenticated via SAML before making any REST API requests.

Without authenticating the user, if you try to access any of the SAML-protected URLs, for example: `https://localhost:8443/alfresco/api/-default-/public/alfresco/versions/1/sites`

An 401 unauthorized response will be returned, for example:

```json
{
    "status" :
  {
    "code" : 401,
    "name" : "Unauthorized",
    "description" : "The request requires HTTP authentication."
  }, 
  
  "message" : "02210007 Authentication failed for Web Script org\/alfresco\/api\/ResourceWebScript.get", 
  "exception" : "org.springframework.extensions.webscripts.WebScriptException - 02210007 Authentication failed for Web Script org\/alfresco\/api\/ResourceWebScript.get",
 
  "callstack" :
  [
          ""      ,"org.springframework.extensions.webscripts.WebScriptException: 02210007 Authentication failed for Web Script org\/alfresco\/api\/ResourceWebScript.get"
      ,"org.alfresco.repo.web.scripts.RepositoryContainer.executeScriptInternal(RepositoryContainer.java:404)"
      ,"org.alfresco.repo.web.scripts.RepositoryContainer.executeScript(RepositoryContainer.java:281)"
      ...
      ,"org.apache.tomcat.util.net.JIoEndpoint$SocketProcessor.run(JIoEndpoint.java:310)"
      ,"java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)"
      ,"java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)"
      ,"java.lang.Thread.run(Thread.java:745)"
  ],
 
  "server" : "Enterprise v5.0.3 (r122151-b84) schema 8 040",
  "time" : "21 mars 2017 11:45:44"
}
```

Use the following to authenticate a user via SAML:

1. Navigate to `https://localhost:8443/alfresco/service/saml/-default-/rest-api/authenticate` in a browser. This can either be a webview component in a mobile or desktop application or within an iframe in a web application.

    You will be redirected to your identity provider's login page.

2. Enter your login credentials.

    If the identity provider has accepted the credentials, the browser will be redirected to `https://localhost:8443/alfresco/service/saml/-default-/rest-api/authenticate-response`.

3. Start making authenticated requests. You have two ways to make requests to the repository:

    * Use the `alf_ticket` contained in the JSON file returned by the `/authenticate-response`. A desktop or mobile application that is running the SAML authentication in a webview can access the content of this webview and grab the `alf_ticket` from the JSON file. This can then be used to make requests, such as `curl https://localhost:8443/alfresco/api/-default-/public/alfresco/versions/1/sites?alf_ticket=TICKET_ed6db2aca17e94864799c9849780f66c0a738e9b`

    * Use the authentication cookie. A web application has typically no access to the content of an iframe. So you are not able to read the `alf_ticket` from the `/authenticate-response`.

To logout from using REST API, use the following `/logout-request`:

```http
https://localhost:8443/alfresco/service/saml/-default-/rest-api/logout-request?alf_ticket=TICKET_17196d7019fc1704ed29a270bf4f54598393abdc
```

with a response of:

```json
{"entry":{}}
```

The SAML ticket is now invalid and the user can no longer access Alfresco.

## Alfresco Office Services (AOS)

{% capture aos-admin %}

### Configure AOS using the Admin Console

Administrators can enable and configure SAML authentication using the Alfresco Admin Console.

1. Log in to the SAML page of the Alfresco Admin Console with your user credentials: `http://localhost:8080/alfresco/service/enterprise/admin/admin-saml`

2. Select the **AOS** tab.

3. Select **Enable SAML (SSO) Authentication**.

    SAML Status shows whether SAML is currently enabled or disabled.

4. Specify the **Identity Provider (IdP) Description**.

5. Enter the IdP settings:

    | Setting | Description |
    | ------- | ----------- |
    | IdP Authentication Request Service URL | The address where the authentication request is sent. This redirects you to the identity provider login page. For example: `https://pingfederate.alfresco.me:9031/idp/SSO.saml2` |
    | IdP Single Logout Request Service URL | The address where the logout request is sent when logging out of Alfresco. This logs you out of Alfresco and any other applications that use your SSO setup. For example: `https://pingfederate.alfresco.me:9031/idp/SLO.saml2` |
    | IdP Single Logout Response Service URL | The address where the logout response is sent when the identity provider gets a logout request. For example: `https://pingfederate.alfresco.me:9031/idp/SLO.saml2` |
    | Entity Identification (Issuer) | Some IdPs use the issuer to determine which service provider connection to use. If you are using ADFS, this is the Base URL, for example: `http://localhost:8080/share`. |
    | User ID Mapping | The SAML attribute that maps to an Alfresco User ID. For PingFederate, this maps to `PersonImmutableID`. For ADFS, the SAML attribute is the `Subject/NameID` specified for the SAML subject `NameID`. |

6. Click **Upload IdP Certificate** to browse to and upload the IdP certificate that you downloaded from your identity provider during configuration.

    **IdP Certificate Status** shows whether the certificate is valid, and the expiry date of the current certificate.

    > **Note**: Alfresco Content Services does not allow you to upload an expired certificate.

    > **Note:** If SAML is enabled, Alfresco always checks for an existing certificate.

7. Click **Download SP Certificate** to download the certificate required by your IdP.

    This is a copy of your self-signed certificate. You should have already downloaded this information when setting up your connections in the IdP.

8. Click **Download SP Metadata** if you need to download the service provider signature verification certificate.

    This is required for AD S configuration, if you are using ADFS as your IdP.

9. Click **Save**.

You can disable these settings by deselecting **Enable SAML (SSO) Authentication**.

{% endcapture %}

{% capture aos-properties %}

### Configure AOS using the `alfresco-global.properties` file

Administrators can enable and configure SAML authentication for AOS using the `<classpathRoot>/alfresco-global.properties` file and a combination of subsystem properties files. Use this as an alternative to configuring SAML using the Admin Console.

To configure AOS, create the properties file in the` <classpathRoot>/alfresco/extension/subsystems/SAML/repository/aos/my-custom-aos-sp.properties` directory.

The default `saml.properties` file can be found in the `<TOMCAT_HOME>/webapps/alfresco/WEB-INF/classes/alfresco/subsystems/SAML/repository` directory. Use this file to copy the SAML settings into your `<classpathRoot>/alfresco/extension/subsystems/SAML/repository/aos/my-custom-aos-sp.properties` file.

**Note:** Changes to `<classpathRoot>/alfresco-global.properties` are applicable in a single service provider scenario only.

If you use multiple service providers, use subsystem extensions for type and instance. For example, for the REST API service provider, create a `my-custom-aos-sp.properties` file with the classpath: `<TOMCAT_HOME>/shared/classes/alfresco/extension/subsystems/SAML/repository/aos/my-custom-aos-sp.properties`.

1. Locate the `<TOMCAT_HOME>/webapps/alfresco/WEB-INF/classes/alfresco/subsystems/SAML/repository/saml.properties` file.

    These are the settings:

    ```bash
    #SAML key store configuration
    saml.keystore.location=classpath:alfresco/keystore/saml.keystore
    saml.keystore.keyMetaData.location=classpath:alfresco/keystore/saml-keystore-passwords.properties
    saml.keystore.provider=
    saml.keystore.type=JCEKS

    # Time, in milliseconds, that message state is valid
    # 300000 = 5 minutes
    saml.message.state.duration.in.millis=300000
    # Clock skew - the number of seconds before a lower time bound, or after an upper time bound, to consider still acceptable.
    saml.issueInstantRule.check.clock.skew.in.seconds=60
    # Number of seconds after a message issue instant after which the message is considered expired  expires
    saml.issueInstantRule.check.expiration.in.seconds=30

    # It is RECOMMENDED that a system entity use a URL containing its own domain name to identify itself
    saml.sp.idp.spIssuer.namePrefix=

    # The SAML attribute (or 'Subject/NameID' for SAML subject NameID) to map to the Alfresco user's ID
    saml.sp.user.mapping.id=Subject/NameID

    # The SAML attribute to map to the Alfresco user's email
    saml.sp.user.mapping.email=Email

    # The SAML attribute to map to the Alfresco user's first name
    saml.sp.user.mapping.firstName=GivenName

    # The SAML attribute to map to the Alfresco user's last name
    saml.sp.user.mapping.lastName=Surname

    # Whether or not SAML is enabled for the service provider
    saml.sp.isEnabled=false

    # Whether or not SAML login is enforced
    saml.sp.isEnforced=false

    # IdP description if you choose to enforce SAML login
    saml.sp.idp.description=

    # IdP URL to which the Authentication Request from Alfresco is posted for the service provider
    saml.sp.idp.sso.request.url=

    # IdP URL to which a logout *request* from Alfresco is posted when logging out from the service provider
    saml.sp.idp.slo.request.url=

    # IdP URL to which a logout *response* from Alfresco is posted when receiving a logout request from your IdP for the service provider
    saml.sp.idp.slo.response.url=

    # Path to the certificate used to validate the requests and responses from the IdP
    saml.sp.idp.certificatePath=

    # Entity identification (issuer) for the service provider.  Some IdPs may use this to determine which SP connection to use.
    saml.sp.idp.spIssuer=

    # Provide a ticket to the user after authentication
    saml.sp.outcome.provideTicket=true

    # Establish a session after authentication
    saml.sp.outcome.establishSession=true

    # Some IdPs, like LemonLDAP, may require a specific format for NameID section of the logout request.
    saml.sp.slo.request.nameid.format=
    ```

2. To enable SAML, use these settings in your `<classpathRoot>/alfresco/extension/subsystems/SAML/repository/aos/my-custom-aos-sp.properties` file:

    ```bash
    saml.sp.isEnabled=true
    saml.sp.isEnforced=false
    saml.sp.idp.description=<Identity Provider>
    ```

    * `saml.sp.isEnabled` specifies whether or not SAML is enabled for the service provider.

    * `saml.sp.isEnforced` accepts a boolean value and specifies whether or not SAML login is enforced. If set to `false`, SAML login is not enforced.

    * `saml.sp.idp.description` accepts a string value and specifies the IdP description at the login screen if you choose to not enforce SAML login.

3. Set the Identity Provider (IdP) settings:

    * `saml.sp.idp.sso.request.url`: The address where the authentication request is sent. This redirects you to the identity provider login page.
    * `saml.sp.idp.slo.request.url`: The address where the logout request is sent when logging out of Alfresco. This logs you out of Alfresco and any other applications that use your SSO setup.
    * `saml.sp.idp.slo.response.url`: The address where the logout response is sent when the identity provider gets a logout request.
    * `saml.sp.idp.spIssuer`: Some IdPs use the issuer to determine which service provider connection to use.
    * `saml.sp.user.mapping.id`: The SAML attribute that maps to an Alfresco User ID. The SAML attribute is the `Subject/NameID` specified for the SAML subject `NameID`.

4. Enter a path to the certificate: `saml.sp.idp.certificatePath`

    > **Note:** If SAML is enabled, Alfresco always checks for a existing certificate.

5. Review the other SAML settings in the `saml.properties` file to understand if they apply to your setup.

6. Save and close all the properties files, and restart Alfresco to apply your changes.

{% endcapture %}

{% capture aos-jmx %}

### Configure AOS using JMX

JMX values (Managed Bean or MBean attributes) are exposed in the Alfresco Admin Console and with internal tools (Alfresco JMX Dump) or external tools like JConsole. The SAML Module beans are described here with their default values.

> **Note**: Example values are given. Always check the values in your own system as these can vary depending on the install method or operating system.

> **Important**: Be aware that any changes you make to attributes in the live system are written to the database. The next time that Alfresco starts, these values will take precedence over any values specified in properties files.

The following are the attributes available for `Alfresco:Type=Configuration, Category=SAML, Object Type=SAML$managed$aos`:

|Attribute |Example|
|--------------|-------------|
|$type|`repository`|
|idpCertificateExpiryDate| |
|idpCertificateSerialNumber| |
|idpCertificateStatus|`missing`|
|idpCertificateSubject| |
|instancePath|`[managed, aos]`|
|saml.issueInstantRule.check.clock.skew.in.seconds|`60`|
|saml.issueInstantRule.check.expiration.in.seconds|`30`|
|saml.keystore.keyMetaData.location|`classpath:alfresco/keystore/saml-keystore-passwords.properties`|
|saml.keystore.location|`classpath:alfresco/keystore/saml.keystore`|
|saml.keystore.provider| |
|saml.keystore.type|`JCEKS`|
|saml.message.state.duration.in.millis|`300000`|
|saml.share.spSloRequestURLSuffix|`/saml-logoutrequest`|
|saml.share.spSloResponseURLSuffix|`/saml-logoutresponse`|
|saml.share.spSsoURLSuffix|`/saml-authnresponse`|
|saml.sp.idp.certificatePath|Set the path to the certificate you require|
|saml.sp.idp.slo.request.url| |
|saml.sp.idp.slo.response.url| |
|saml.sp.idp.spIssuer| |
|saml.sp.idp.spIssuer.namePrefix| |
|saml.sp.idp.sso.request.url| |
|saml.sp.isEnabled|`false`|
|saml.sp.isEnforced|`true`|
|saml.sp.idp.description|`<Identity Provider>`|
|saml.sp.user.mapping.email|`Email`|
|saml.sp.user.mapping.firstName|`GivenName`|
|saml.sp.user.mapping.id|`Subject/NameID`|
|saml.sp.user.mapping.lastName|`Surname`|
|spSigningCredentialStatus|`missing`|
|saml.sp.slo.request.nameid.format| |

The following is the attribute available for `Alfresco:Type=Configuration, Category=SAML, Object Type=SAML$manager`:

|Attribute|Example|
|--------------|-------------|
|chain|`share:share,rest-api:repository,aos:repository`|

A [complete list of of Alfresco MBeans]({% link content-services/latest/admin/jmx-reference.md %}) is also available.

{% endcapture %}

{% include tabs.html tableid="aos" opt1="Admin Console" content1= aos-admin opt2="Properties" content2=aos-properties opt3="JMX" content3=aos-jmx %}

### Authenticate users for AOS

After configuring SAML for AOS, you can test that everything is set up correctly.

1. Verify that the administrator email address is configured correctly in the IdP.

2. Login to Share as the administrator: `http://localhost:8080/share`

    You should get redirected to the identity provider login page.

3. Enter your user credentials.

    You should be redirected to Alfresco Share.

4. For a given site, go to the Document Library.

5. Hover over a file you want to edit and click **More** then **Edit in Microsoft Office**.

6. The MS Office file opens the IdP login page in a separate window.

7. Enter your user credentials again.

8. The file is now open and you can edit it, as needed.

9. Additionally, you can also map the AOS network drive in Windows Explorer or Finder. You will be presented with a repository to browse.

10. Log out of Alfresco Share.

    If you go back to your IdP page, you should also be logged out.

    > **Note**: After logging out of Alfresco Share, you won't be able to access the recent history in Office files or map to the AOS network drive.
---
title: Overview of the SAML Module configuration
---

To use the SAML Module for Alfresco Content Services an identity provider and service providers need to be setup and configured. Three service providers exist on startup of SAML: Alfresco Share, Alfresco Office Services and the REST API.

Irrespective of the service provider you are using, configure your connection in this order:

1. Configure an identity provider.

    >**Note**: Alfresco should work with any identity provider that supports SAML 2.0, however example instructions for configuring PingFederate or ADFS are provided.

2. Download your identity provider certificate from the identity provider.
3. Configure SAML in Alfresco in one of the following ways:
    * Using the Alfresco Admin Console
    * In configuration files, such as `alfresco-global.properties`
    * Dynamically, using JMX if enabled

> **Note:** Ensure that users are created in Alfresco before attempting to log on using SAML. Users that are disabled or de-authorized can't log in.

User authentication is handled differently depending on whether SAML is enforced, enabled or both:

| Enabled | Enforced | Action |
| ------- | -------- | ------ |
|Yes|Yes|SAML is enabled and enforced. User is authenticated through SAML and is redirected to the identity provider login page.|
|No|Yes|SAML is disabled. User is authenticated either using Share login or basic authentication.|
|Yes|No|User can choose either to use Share login or to login using the identity provider.|
|No|No|SAML is disabled. User is authenticated either using Share login or basic authentication.|
---
title: Configure PingFederate
---

The following steps are example instructions for configuring PingFederate as the identity provider to use with the SAML Module in Alfresco. For detailed instructions on configuration use the [PingFederate documentation](https://support.pingidentity.com/s/PingFederate-help){:target="_blank"}.

PingFederate can be configured manually or you can reuse or clone an [existing connection](#reuse-an-existing-connection).

## Configure PingFederate manually

1. Log in to your PingFederate administrative console as the administrator.

    The URL is in the format `https://<DNS_NAME>:9999/pingfederate/app`

2. In **IdP Configuration** > **SP Connections**, click **Create New** to create a service provider connection for Alfresco Content Services.

3. Enter information in each of the following tabs to set the type of connection you want to establish between PingFederate and Alfresco Content Services.

    1. **Connection Type**: Select the **Browser SSO Profiles** check box and click **Next**.

    2. **Connection Options**: Select the **Browser SSO** check box and click **Next**.

    3. **Import Metadata**: Use this tab to import the metadata file describing this new connection.

        1. In a new browser window, log in to the SAML Admin Console page as an administrator: `http://localhost:8080/alfresco/service/enterprise/admin/admin-saml`

        2. Click `Download SP Metadata`.
        3. Save the file.

            > **Note:** The Admin Console settings for SAML will be setup later.

    4. Set these values in the **General Info** tab:

        1. Specify the **Partner's Entity ID (Connection ID**) and the **Connection Name** for your connection.
        2. Ensure that the Base URL is pointing to your service provider. For example:

            * For Alfresco Share: `http://localhost:8080/share`
            * For REST API: `http://localhost:8080/alfresco`
            * For Alfresco Officer Services: `http://localhost:8080/alfresco`

        3. Optionally, you can also provide contact information.
        4. Set the level of transaction logging you need. Ensure that **Standard** is selected as the **Logging Mode**.
        5. Click **Next**.

            > **Note:** You can save the configuration by clicking **Save Draft**. You can then retrieve it by selecting **Manage All SP** from **SP Connections** on the main administrative console page.

        6. The **Browser SSO** tab has a number of sections to complete. Click **Configure Browser SSO** and complete the following steps on each of the Browser SSO tabs.

4. Use the Browser SSO section to setup message transfers between Alfresco and PingFederate.

    1. Select all four available profiles on this tab and click **Next**.

        **SAML Profiles**: Alfresco uses all the SSO and SLO profiles available.

    2. **Assertion Lifetime**: Accept the default and click **Next**.

        This sets the time for which an assertion is valid. A SAML assertion is an XML document that contains authentication, authorization, and attribute information. Each assertion has validity time period.

    3. Click **Configure Assertion Creation** in the **Assertion Creation** tab.

        Configuring assertions involves specifying how PingFederate obtains user-authentication information and uses it to create assertions for Alfresco Content Services. This includes choosing an identity mapping method, defining the attribute contract and configuring adapters.

    4. **Identity Mapping**: Ensure that the **Standard** mapping is selected and click **Next**.

    5. Enter the following information for the **Attribute Contract**:

        1. Choose **urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified** as the subject name format for the SAML_SUBJECT attribute contract.

            > **Note:** The contract includes the default SAML_SUBJECT, which identifies the user in the assertion. This is because you used the standard identity mapping.

        2. Extend the Contract by adding an email part to it. Type **Email** in the **Extend the Contract** text box.
        3. Choose **urn:oasis:names:tc:SAML:2.0:attrname-format:basic** as the attribute name format and click **Add**. The details are added.
        4. Click **Next**.

5. In Authentication Source Mapping, click **Map New Adapter Instance**, and complete the following steps for the **IdP Adapter Mapping** tabs.

    IdP adapters are used for user authentication in the Single Sign-On process. When an Alfresco user enters credentials, the user attributes are returned to PingFederate.

    1. **Adapter Instance**: Select **IdP Adapter** from the **Adapter Instance** menu and click **Next**.

        An adapter instance is a configured and deployed adapter.

    2. **Assertion Mapping**: Ensure **Use only Adapter Contract values in the SAML assertion** is selected. Click **Next**.

        Setting up assertion mappings involves defining data stores that you want to use to look up adapter contract values.

    3. Set these values for **Attribute Contract Fulfilment**:

        1. For the Email attribute contract, select **Adapter** as the **Source**.
        2. For the Email attribute contract, select **email** as the **Value**.
        3. For the SAML_SUBJECT attribute contract, select **Adapter** as the **Source**.
        4. For the SAML_SUBJECT attribute contract, select **subject** as the **Value** .
        5. Click **Next**.

    4. Click through **Next** and **Done**, as the information is optional for the **Issuance Criteria** tab.

    5. Click **Next** and **Done**.

        You are redirected to the **Browser SSO** tab to configure bindings, endpoints, and other settings needed for the SAML profile.

        > **Note:** You can save the configuration at any time by clicking **Save Draft**. You can then retrieve it by selecting **Manage All SP** from **SP Connections** on the main administrative console page.

6. Click **Protocol Settings** in the **Browser SSO** tab and complete the following tasks on each of the **Protocol Settings** tabs.

    1. Specify information for the **Assertion Consumer Service URL**:

        For Alfresco Share:

        1. Select **POST** from the **Binding** menu.
        2. Type **/page/saml-authnresponse (POST)** in the **Endpoint URL** field.
        3. Click **Add**. Click **Next**.

        For REST API:

        1. Select **POST** from the **Binding** menu.
        2. Type **/service/saml/-default-/rest-api/authenticate-response (POST)** in the **Endpoint URL** field.
        3. Click **Add**. Click **Next**.

        For Alfresco Office Services:

        1. Select **POST** from the **Binding** menu.
        2. Type **/service/saml/-default-/aos/authenticate-response (POST)** in the **Endpoint URL** field.
        3. Click **Add**. Click **Next**.

    2. Specify information for the **SLO Service URLs**. These specify where Alfresco receives logout requests when a Single Log-out (SLO) request is initiated by PingFederate, and where PingFederate sends SLO responses.

        For Alfresco Share:

        1. Select **POST** from the **Binding** menu.
        2. Type **/page/saml-logoutrequest** in the **Endpoint URL** field.
        3. Type **https://-your server-/share/page/saml-logoutresponse** in the **Response URL** field.For example: `https://localhost:8443/share/page/saml-logoutresponse`
        4. Click **Add**. Click **Next**.

        For REST API:

        1. Select **POST** from the **Binding** menu.
        2. Type **/service/saml/-default-/rest-api/logout-request (POST)** in the **Endpoint URL** field.
        3. Type **https://-your server-/alfresco/service/saml/-default-/rest-api/logout-response** in the **Response URL** field.

        For Alfresco Office Services:

        1. Select **POST** from the **Binding** menu.
        2. Type **/service/saml/-default-/aos/logout-request (POST)** in the **Endpoint URL** field.
        3. Type **https://-your server-/alfresco/service/saml/-default-/aos/logout-response** in the **Response URL** field.

    3. **Allowable SAML Bindings**: Ensure that only **POST** is selected as the binding type. Click **Next**.

    4. **Signature Policy**: You do not need to select an option; just click **Next**.

    5. Configure the **Encryption Policy**:

        1. Ensure that **None** is selected and click **Next**.
        2. Check the summary and click **Done**.
        3. Click **Next**.
        4. Review the final settings and click **Done**. You are redirected to the **SP Connection > Browser SSO** tab.

7. Click the **Credentials** tab and **Configure Credentials** and complete the following steps on each tab.

    1. **Digital Signature Settings**: Download the PingFederate certificate.

        In the Credentials section, select **Digital Signature Settings** and Manage Certificates.

        1. Click **Export** for the IdP certificate that you require.
        2. Select **Certificate only** and click **Next**.
        3. Click **Export**, and save the file to a folder. Click **Done**.

        > **Note**: You will need this certificate for uploading into the administration console later.

        On the **Digital Signature Settings** screen, select the signing certificate and the signing algorithm.

        1. Select the certificate from the drop-down list.
        2. Select the **Signing Algorithm** from the drop-down list. Make sure that the selected Signing Algorithm is **RSA SHA256**.

    2. **Signature Verification Settings**: Specify the **SP Certificate** used by PingFederate to validate SAML messages sent from Alfresco products.

        1. Select **Manage Signature Verification Settings**.
        2. Select the **Unanchored** option.
        3. Click **Next**.
        4. Click **Manage Certificates**.
        5. Click **Import** and **Browse** to select the SP Certificate that you downloaded from the SAML administration console and then click **Extract**.
        6. In a new browser window, log in to the Admin Console SAML page as an administrator: `http://localhost:8080/alfresco/service/enterprise/admin/admin-saml`
        7. Click **Download SP Certificate**.
        8. Save the file.
        9. Click **Next**. The **Summary** screen is displayed. You can review or edit your credentials configuration here.
        10. When you finish editing the existing settings, click **Done** on the **Summary** screen, and **Save** on the  **Credentials** screen.

8. Ensure that your connection is active.

    You can check your connection from the main administrative console. Select **SP Connections > Manage All SP** and scroll down to see the connection you created. Each connection has a status of Active, Inactive or Draft.

## Reuse an existing connection

1. Log in to your PingFederate administrative console as the administrator: `https://<DNS_NAME>:9999/pingfederate/app`

2. Download or copy an existing connection profile from PingFederate:

    From the PingFederate main administrative console, select **SP Connections > Manage All SP** and scroll down to an existing connection for Alfresco. Click **Export Connection** and **Save** to download and edit offline, or **Copy** to create a new connection in PingFederate.

3. If you are downloading the connection information to edit it offline, the file is saved as a `sp-pingfederate-connection.xml` file, for example (with encoding information removed):

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <md:EntityDescriptor entityID="nameofconnection" urn:name="nameofconnection" urn:baseUrl="http://localhost:8080/share" urn:LogLevel="STANDARD" urn:isActive="true" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:urn="urn:sourceid.org:saml2:metadata-extension:v2">
      <md:Extensions>
        <urn:EntityExtension PFVersion="7.3.0.5" LicenseGroup="">
          <urn:DigitialSignatureAliases SigningAlgorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1" includeX509inXmlSig="true" includeRawKeyInXmlSig="false"/>
          <urn:Encryption>
            <urn:EncryptionPolicy EncryptionAlgorithm="http://www.w3.org/2001/04/xmlenc#aes128-cbc" KeyTransportAlgorithm="http://www.w3.org/2001/04/xmlenc#rsa-oaep-mgf1p" EncryptAssertion="false" EncryptSubjectNameID="false" SLOEncryptSubjectNameID="false"/>
            <urn:DecryptionPolicy AssertionEncrypted="false" SubjectNameIDEncrypted="false" AttributeEncrypted="false" SLOSubjectNameIDEncrypted="false"/>
          </urn:Encryption>
          <urn:Dependencies>
            <urn:SigningKeyPairReference MD5Fingerprint="fingerprint_number"/>
            <urn:DsigVerificationCert>
             <urn:Base64EncodedCert>certificate_info</urn:DsigVerificationCert>
            <urn:SecondaryDsigVerificationCert/>
            <urn:DecryptionKeyPairReference/>
            <urn:EncryptionCert/>
            <urn:SoapAuth>
              <soap:Incoming xmlns:soap="http://www.sourceid.org/2004/04/soapauth"/>
              <soap:Outgoing xmlns:soap="http://www.sourceid.org/2004/04/soapauth"/>
            </urn:SoapAuth>
          </urn:Dependencies>
          <urn:ConnectionTemplateProperties/>
        </urn:EntityExtension>
      </md:Extensions>
      <md:SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol" AuthnRequestsSigned="false" WantAssertionsSigned="false">
        <md:Extensions>
          <urn:RoleExtension ArtifactTimeoutSeconds="60">
            <urn:IncomingBindings Artifact="false" POST="true" Redirect="true" SOAP="false"/>
            <urn:EnabledProfiles IDPInitiatedSSO="true" IDPInitiatedSLO="true" SPInitiatedSSO="true" SPInitiatedSLO="true"/>
            <urn:SP AssertionValidityAfterMinutes="5" AssertionValidityBeforeMinutes="5" ConnectionTargetType="Standard" EnableCDCDuringSSO="false">
              <urn:AdapterToAssertionMapping AbortIfNotFoundInAnyDataSources="false" RestrictVirtualServerIds="false" AdapterInstanceId="idpadapter">
                <urn:DefaultAttributeMapping>
                  <urn:AttributeMap Name="SAML_SUBJECT" Type="Adapter" Value="subject"/>
                  <urn:AttributeMap Name="Email" Type="Adapter" Value="email"/>
                  <urn:AttributeMap Name="PersonImmutableID" Type="Adapter" Value="username"/>
                  <urn:TokenAuthorizationIssuanceCriteria/>
                </urn:DefaultAttributeMapping>
              </urn:AdapterToAssertionMapping>
              <urn:NameIdentifierMappingType IncludeAdditionalAttributes="false" IncludeAdditionalTransientAttributes="false"/>
            </urn:SP>
          </urn:RoleExtension>
        </md:Extensions>
        <md:SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="/page/components/saml/logoutrequest" ResponseLocation="http://localhost:8080/share/page/saml-logoutresponse"/>
        <md:NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified</md:NameIDFormat>
        <md:AssertionConsumerService index="0" Location="/page/saml-authnresponse" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" isDefault="true"/>
        <md:AttributeConsumingService index="0">
          <md:ServiceName xml:lang="en">AttributeContract</md:ServiceName>
          <md:RequestedAttribute Name="Email" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic"/>
          <md:RequestedAttribute Name="PersonImmutableID" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic"/>
        </md:AttributeConsumingService>
      </md:SPSSODescriptor>
      <md:ContactPerson contactType="administrative">
        <md:Company>your-company</md:Company>
        <md:EmailAddress>your_address</md:EmailAddress>
      </md:ContactPerson>
    </md:EntityDescriptor>
    ```

    > **Note**: `entityID` and `urn:name` are the name of your PingFederate connection, and `urn:baseUrl` is the name of your service provider instance. Ensure that you also have the correct `ResponseLocation` defined.

4. From the PingFederate main administrative console page, select **Import from the SP Connections** section. Click **Browse** to find your `sp-pingfederate-connection.xml` file. Click **Import** and **Done**.

5. Review the settings for the connection.

    From the PingFederate main administrative console, select **SP Connections > Manage All SP** and scroll down to the connection you created. Click the connection name and view the summary information.

6. Ensure that your connection is active.

    Each connection has a status of Active, Inactive or Draft.

### Download an identity provider certificate

> **Note:** You can skip this task if you have already downloaded the certificate in the manual setup steps.

1. Log in to the identity provider administrative console as the administrator, for example:`https://<DNS_NAME>:9999/pingfederate/app`

2. For PingFederate, in the Server Configuration section, select **Certificate Management** and **Digital Signing & XML Decryption Keys & Certificates**.

    1. Click **Export** for the IdP certificate that you require.

    2. Select **Certificate only** and click **Next**.

    3. Click **Export**, and save the file to a folder for uploading to Alfresco in the next task. Click **Done**.

## Setup users in PingFederate

The following steps can be used to setup users in PingFederate for development and test environments. 

For production environments, see the guidance in the [PingFederate documentation](https://support.pingidentity.com/s/PingFederate-help){:target="_blank"} on other options, including configuring an LDAP connection.

1. Run a full LDAP sync. This can be done by restarting Alfresco Content Services.

    If a user exists in LDAP and PingFederate, but not in Alfresco, they will not be able to log in to Alfresco when SAML is enabled. See [Configuring LDAP (Active Directory)]({% link content-services/latest/admin/auth-sync.md %}#configure-ldap) for more information.

2. Stop the PingFederate server.

3. Add a section at the end of the file: `root/pingfederate-7.3.0/pingfederate/server/default/deploy/quickstart-app-idp.war/WEB-INF/classes/users.xml`, above the </users> closing tag.

    The format expected is as follows for each Alfresco user:

    ```xml
    <user> 
    <first-name>Administrator</first-name>
    <last-name>Administrator</last-name>
    <email-address>admin@alfresco.com</email-address>
    <user-id>admin</user-id>
    <password>admin</password>
    <attribute name="SSN">123-45-6789</attribute>
    <attribute name="net worth">$38.26</attribute>
    <attribute name="salary">18500</attribute>
    </user>
    ```

    Ensure you choose a non-trivial password for each user, and that the details match the user in Alfresco Content Services.

4. Restart the PingFederate server.

    The new users are loaded and visible in the menu when you next go to your IdP logon page. You can check the PingFederate `server.log` for more information.
---
title: Develop with the SAML Module
---

This information is intended for developers or system administrator to create applications that interact with Alfresco using the SAML Module.

## Prerequisites

* The SAML Module [installed]({% link saml-module/latest/install/index.md %}) and [configured]({% link saml-module/latest/config/index.md %}).

> **Note**: The examples below use Alfresco Content Services running locally on port 8080: `http://localhost:8080/alfresco`.

> **Note**: SAML in Alfresco does not support user provisioning. This means that user IDs have to be created in Alfresco Content Services and in the identity provider before trying to authenticate the users with SAML in Alfresco or in a custom application.

## Service description

Alfresco offers a configurable mode for interacting with the SAML support. As an administrator, you can go to `http://localhost:8080/alfresco/s/enterprise/admin/admin-saml` to see the configured service providers that Alfresco exposes for interacting with various Alfresco functionality and components.

In this example, we will discuss the REST API service provider in detail. This is the recommended service provider to use for interacting with the Alfresco Public REST APIs. For more information, see [REST API]({% link content-services/latest/develop/rest-api-guide/index.md %}).

If configuring SAML using JMX beans, there are two additional properties that you can update in the JMX console. These properties are: `saml.sp.outcome.establishSession` and `saml.sp.outcome.provideTicket`. The use of the ticket based pattern is recommended to ensure authentication for the REST API. It is also recommended to avoid using session (cookie based), so `saml.sp.outcome.establishSession` should be set to `false`.

## General usage information

The initial REST API use cases are targeting clients that leverage CMIS, the Mobile SDK, and the Public REST API. These clients should all be able to manage authenticate with SAML through the identity provider (IdP) HTTP POST binding (requires browser capabilities). Different IdPs support different SAML bindings and may have small differences when working with them.

### Authenticate users in an application using SAML via the REST API

1. [Configure the REST API]({% link saml-module/latest/config/alfresco.md %}#alfresco-rest-api).

2. Check if SAML is enabled (or enforced) in your setup by making a call to `http://localhost:8080/alfresco/service/saml/-default-/rest-api/enabled` where`-default-` is the tenant name and `rest-api` is the ID of your SAML REST API service provider.

    This web script is documented at:

    ```http
    http://localhost:8080/alfresco/s/script/org/alfresco/repository/authentication/saml/service-provider/enabled.get
    ```

    The web script will return a JSON object with the information:

    ```json
    {
        "entry":
        { 
          "isSamlEnabled": true,
          "isSamlEnforced": true,
          "idpDescription": ".....",
          "tenantDomain": "...."
        }
    }
    ```

3. To start the SAML authentication protocol, your application will have to open an embedded browser (such as webkit) and navigate to: `http://localhost:8080/alfresco/service/saml/-default-/rest-api/authenticate`

    This process generates the callback URL which the IdP will use after the user has logged in. The URL gets built using the `alfresco.host`, `alfresco.port`, and `alfresco.protocol` properties. Your application will need to know the values of these properties.

    You can find the description of the callback here:

    ```http
    http://localhost:8080/alfresco/s/script/org/alfresco/repository/authentication/saml/service-provider/authenticate.get
    ```

    This web script returns an HTML page that contains an embedded form which automatically submits and redirects to the configured IdP login page.

4. Enter the credentials of your application and click the **Login** button on the IdP page in the embedded browser. This will submit and redirect back to an Alfresco web script: `http://localhost:8080/alfresco/service/saml/-default-/rest-api/authenticate-response`

    In this POST operation, the Alfresco repository will receive a SAML message from the IdP containing an assertion about the identity of the user. The repository will then verify the message and check if the user is authorized for the repository. If successful, it responds with the following JSON:

    ```json
    {
        "entry":
        {
            "id":"TICKET_81c0bd117a3804f26efc7c8aa645918d05f2598b",
            "userId":"test"
        }
    }
    ```

    Your application should monitor the embedded browser you started to detect when it hits this final URL: `http://localhost:8080/alfresco/service/saml/-default-/rest-api/authenticate-response`

    Pick up the ticket from the JSON response and close the browser. You now have an Alfresco ticket to talk to the REST APIs. For more information, see: `http://localhost:8080/alfresco/s/script/org/alfresco/repository/authentication/saml/service-provider/authenticate-response.post`.

5. Using this Alfresco ticket, you can talk to any Alfresco API. For more information, see [Specifying user identity]({% link content-services/latest/tutorial/platform/web-scripts.md %}#specifying-user-identity).

    You can pass the ticket as the `alf_ticket` query parameter in the URL. For example to get a list of sites use: `http://localhost:8080/alfresco/s/api/sites?alf_ticket=TICKET_97990b0a1c9152282b715a31bf365b41a3e21f01`

    For CMIS, you can also invoke any API and use the special name `ROLE_TICKET` as the username and your ticket as the password.

6. You can initiate a Single-Log-Out from the IdP to invalidate your ticket and sign the user out of all services through the IdP. As with the login, you need to embed a browser again and navigate to: `http://localhost:8080/alfresco/service/saml/-default-/rest-api/logout-request?alf_ticket=<your-ticket>`

    The repository will respond with an HTML page containing a form that gets submitted to the IdP automatically. The IdP will then sign out the user and ultimately respond with an HTML page containing a form that is submitted back to this repository URL: `http://localhost:8080/alfresco/service/saml/-default-/rest-api/logout-response`

    In this POST operation, the repository will receive a SAML message from the IdP containing the logout status. On success, the repository will invalidate the ticket and respond with an empty JSON message:

    ```json
    {"entry":{}}
    ```

    > **Note**: The logout from Alfresco should be done during the first call to `/logout-request`, as the last redirect to `/logout-response` doesn't have an assertion to tell which user was logged out. So, Alfresco relies on the cookie to match the logout response to the correct user.

## General Alfresco REST API information

From Alfresco Content Services 6.2 onwards, there is a comprehensive API Explorer that should help you build applications faster, more securely, and consistently. For more information, see [https://api-explorer.alfresco.com/api-explorer/](https://api-explorer.alfresco.com/api-explorer/){:target="_blank"} and [https://github.com/Alfresco/rest-api-explorer](https://github.com/Alfresco/rest-api-explorer){:target="_blank"}.

## Enforcing SAML

You can configure the REST API service provider in Alfresco to enforce SAML authentication. In this case, the REST API will no longer accept any authentication by username and password. The only way to invoke the APIs is by using an Alfresco ticket (as described above). All endpoints to receive such a ticket by username and password are disabled. This means that the only way to get a valid ticket to use with the REST API is through the SAML login API. This means all applications using the REST API (such as Alfresco Share) will have to use SAML. The enforce option is ignored if SAML is disabled for the REST API.

## Administration Console

Although both the Alfresco Admin Console and REST API use web scripts, the Admin Console is excluded from SAML enforcement. The Administrator is still able to access the Admin Console by using a username and password. This exclusion is performed based on the family of the web script (`<family>AdminConsole</family>`) or based on a whitelist of web script IDs. If you have to add additional web scripts to this whitelist, you can do so by setting the property `saml.authenticator.bypass.script.pattern` to a Java pattern, matching web script IDs in `alfresco-global.properties`.

## Example in Java SE (with Java FX)

See [https://github.com/andrei-rebegea/hello-alfresco-saml-api-client-demo](https://github.com/andrei-rebegea/hello-alfresco-saml-api-client-demo).

## Example in Android

See [https://gitlab.alfresco.com/mobile/android-saml-testing-app](https://gitlab.alfresco.com/mobile/android-saml-testing-app).

## Single page web applications

When calling APIs on the repository directly from the browser, you may run into CSRF and CORS issues.

## Configure CSRF

The Application Development Framework (ADF) documentation contains some information on how to configure CSRF. For more information, see [Flag to disable csrf in the core and in the demo shell](https://github.com/Alfresco/alfresco-ng2-components/issues/819) and [Prerequisites for building and running apps with the Alfresco Application Development Framework](https://github.com/Alfresco/alfresco-ng2-components/blob/f575bc5f61210b1ce233fbdda6ab9cb37814abed/PREREQUISITES.md).

## Enable CORS in Alfresco

The web client for ADF will be loaded from a different web server than the one Alfresco runs on. This means that the Alfresco server needs to know that any request that comes in from this custom web client should be allowed access to the repository. This is done by enabling cross-origin resource sharing (CORS).

To enable CORS in the Alfresco server, do one of the following:

* Download and install the CORS module:

    1. Download the [CORS module](https://artifacts.alfresco.com/nexus/service/local/repositories/releases/content/org/alfresco/enablecors/1.0/enablecors-1.0.jar){:target="_blank"}.
    2. Stop the Alfresco server.
    3. Add the enable CORS platform module JAR to the `<ALFRESCO_HOME>/modules/platform` directory.
    4. Restart the Alfresco server.

        > **Note:** By default the CORS filter that is enabled will allow any origin.

* Manually update the `web.xml` file

    1. Open `<ALFRESCO_HOME>/tomcat/webapps/alfresco/WEB-INF/web.xml`.
    2. Uncomment the following section:

        ```xml
        <filter-mapping>
            <filter-name>CORS</filter-name>
            <url-pattern>/api/*</url-pattern>
            <url-pattern>/service/*</url-pattern>
            <url-pattern>/s/*</url-pattern>
            <url-pattern>/cmisbrowser/*</url-pattern>
        </filter-mapping>
        ```

    3. Update `cors.allowOrigin` URL to `http://localhost:3000`. Make sure to use the URL that will be used by the web client.

## Proxies and clustering

There are a number of recommendations when running SAML for Alfresco behind a proxy.

Make sure that the IdP is accessible to the client applications. At a minimum, configure the `alfresco.host`, `alfresco.port`, and `alfresco.protocol` properties to use the correct values of the proxy server. For more information, see [sysAdmin subsystem properties]({% link content-services/latest/config/repository.md %}#sysadmin-props). For deploying Alfresco with a reverse proxy, see [Deploying Alfresco with a different context path]({% link content-services/latest/config/repository.md %}#deploy-contextpath).

The limitations that apply to using web scripts with ticket authentication also applies to clustering for SAML usage. Make sure you have set up your load balancer correctly.

### Recommendation for proxy

In a production environment, for the REST API and AOS, implement a setup with a reverse proxy in front of Alfresco. This reverse proxy is configured to block all API requests except those that you want to be let through, for example, CMIS. Such a setup needs to allow these requests:

* `/alfresco/service/saml/-default-/aos/authenticate`
* `/alfresco/service/saml/-default-/aos/authenticate-response`
* `/alfresco/service/saml/-default-/rest-api/authenticate`
* `/alfresco/service/saml/-default-/rest-api/authenticate-response`
---
title: Install with zip
---

The SAML Module is installed as a module of Alfresco Content Services. These modules are referred to as Alfresco Module Packages (AMP) and use the `.amp` file format.

AMPs can be installed in the `amps` directory of your Alfresco Content Services installation or by using the [Module Management Tool]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt).

## Prerequisites

There are a number of prerequisites for installing the SAML Module in addition to the [supported platforms]({% link saml-module/latest/support/index.md %}).

### Software

Alfresco should work with any identify provider (IdP) that supports SAML 2.0, however the following IdPs have been tested:

* Microsoft Active Directory Federation Services (ADFS) 3.0 for Microsoft Windows 2012 R2 and above
* PingIdentity PingFederate 7.0 and later

Make sure that you have the public key of the certificate from your chosen IdP. You also need the SSO request, SLO request, and SLO response URLs.

### SAML level

Alfresco uses SAML 2.0. See [OASIS SAML v2.0](https://wiki.oasis-open.org/security/FrontPage){:target="_blank"} for more information on SAML specifications.

### Authentication chain

SAML is not a part of the authentication chain. It is used as a replacement for the authentication chain.

If you have not enforced SAML for a specific service provider, you can use the other authentication methods specified in your authentication chain alongside SAML when accessing that service provider.

### Changes to configuring keystores {#keystores-change}

The way you configure keystores in Content Services and related projects has changed. In previous releases, the configuration was stored in a password file, like `keystore-passwords.properties`.

> **Note:** The old way of configuring should still work for backwards compatibility, but it's discouraged due to security reasons. If the old approach is used, you'll see a warning in the logs.
> In the SAML module, the property `saml.keystore.keyMetaData.location` is deprecated, but it's still available only for backwards compatibility.

The recommended way of specifying the configuration is to use JVM system properties.

See the Alfresco Content Services documentation, [Managing Alfresco keystore]({% link content-services/latest/admin/security.md %}#managealfkeystores), for more details the keystores changes.

In the following steps, you can follow either:

* Step 6.3 to use the updated configuration (recommended).
* Step 6.4 to continue using the old configuration, bearing in mind the security risk (deprecated).

## Installation steps

> **Note:** If you are installing the SAML Module on top of Alfresco Content Connector for AWS S3, use the `-force` option, otherwise Alfresco Content Services will not start correctly.

> **Note:** If you are running Alfresco Content Services behind a proxy, make sure the identity provider references the proxy endpoint instead of directly referencing the Alfresco cluster.

1. Stop the Alfresco Content Services server.

2. Navigate to [Hyland Community](https://community.hyland.com/){:target="_blank"}, download and unzip the SAML Module for Alfresco Content Services zip package:

    * `alfresco-saml-1.2.x.zip`

    This file contains the following content:

    ```text
    ├── README.txt
    ├── alfresco
    │   └── extension
    │       └── subsystems
    │           └── SAML
    │               ├── repository
    │               │   ├── aos
    │               │   │   └── my-custom-aos-sp.properties.sample
    │               │   └── rest-api
    │               │       └── my-custom-rest-api-sp.properties.sample
    │               └── share
    │                   └── my-custom-share-sp.properties.sample
    ├── alfresco-global.properties.sample
    ├── alfresco-saml-repo-1.2.x.amp
    ├── alfresco-saml-share-1.2.x.amp
    └── share-config-custom.xml.sample
    ```

3. Move or copy `alfresco-saml-repo-1.2.x.amp` to the `amps` directory and `alfresco-saml-share-1.2.x.amp` to the `amps_share` directory in your Alfresco Content Services installation.

4. If you are using Tomcat, navigate to the `bin` directory and run the `apply_amps.bat` file to install the AMP files.

    * `/opt/alfresco/bin`
    * (Windows) `c:\Alfresco\bin`

    Check the output from the script to ensure that the AMP files have installed successfully.

5. If you are not using Tomcat, use the [Module Management Tool]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt) to apply the AMP files.

6. The SAML module does not supply a service provider certificate that is used to sign messages sent to the IdP. You must generate your own certificate, as shown in the following example:

    This will generate a self-signed certificate.

    1. Run the following command:

       ```bash
       keytool -genkeypair -keyalg RSA -alias my-saml-key -keypass change-me -storepass change-me -keystore my-saml.keystore -storetype JCEKS
       ```

    2. Place the generated `my-saml.keystore` file into a location of your choice that is accessible to the repository.

        Set the file permissions accordingly to limit who can read it.

    3. (Recommended) To use the latest keystore configuration method, set the following as JVM properties. For example, for a Tomcat installation, set them using `JAVA_TOOL_OPTIONS`:

       ```bash
       set "JAVA_TOOL_OPTIONS=-Dsaml-keystore.aliases=my-saml-key -Dsaml-keystore.password=password_AES -Dsaml-keystore.my-saml-key.password=password_AES -Dsaml-keystore.my-saml-key.algorithm=AES"
       ```

    4. (Deprecated) To continue using the old keystore configuration method:

        1. Generate a SAML keystore metadata file in the same location as the keystore and add the following content:

            ```bash
            aliases=my-saml-key
            keystore.password=change-me
            my-saml-key.password=change-me
            ```

            Set the file permissions accordingly to limit who can read it.

        2. Set the following values in the `alfresco-global.properties` file:

            ```bash
            saml.keystore.location=<full pathname>/my-saml.keystore
            saml.keystore.keyMetaData.location=<full pathname>/my-saml-keystore-passwords.properties
            ```

            > **Note:** This deprecated method is not recommended. You should review and [switch to using the updated method](#keystores-change) described earlier.

    5. Restart the Alfresco Content Services server.

    6. Use the SAML Admin Console **Download SP Certificate** button to download the certificate for your SP, which can then be uploaded to your IdP.

    7. Stop the Alfresco server.

7. Locate your `share-config-custom.xml.sample` file.

    This sample configuration file is shipped with SAML and shows the required rules and properties that need to be added to the CSRFPolicy to allow SAML logouts.

    1. If you are using Alfresco Share as your service provider, and you have custom CSRFPolicy configurations in your installation, copy and paste the *SAML SPECIFIC CONFIG* section of the sample file into your custom CSRFPolicy filter, and save.

    2. If you have a `share-config-custom.xml` file in your Alfresco Share installation, merge the contents of `share-config-custom.xml.sample` into your `share-config-custom.xml` file, and save.

    3. Alternatively, if you do not have a `share-config-custom.xml` in your Alfresco Share installation, rename `share-config-custom.xml.sample` to `share-config-custom.xml`.

    4. Review the details in the CSRFPolicy section for accuracy.

8. Restart the Alfresco Content Services server.

## Uninstall steps

Use the [Module Management Tool]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt) to uninstall the SAML Module from Alfresco Content Services.

1. Stop the Alfresco server.

2. Use the information in [Uninstalling an AMP file]({% link content-services/latest/install/zip/amp.md %}#uninstall-an-amp-file) to uninstall each AMP file.

    For example, from the Alfresco root directory, you need two commands:

    ```bash
    java -jar bin/alfresco-mmt.jar uninstall alfresco-saml-repo tomcat/webapps/alfresco.war
    java -jar alfresco-mmt.jar uninstall alfresco-saml-share tomcat/webapps/share.war
    ```

    Use these commands to check whether the AMP files were removed:

    ```bash
    java -jar bin/alfresco-mmt.jar list tomcat/webapps/alfresco.war
    java -jar bin/alfresco-mmt.jar list tomcat/webapps/share.war
    ```

3. Delete the `tomcat/webapps/alfresco` and `tomcat/webapps/share` folders in the Alfresco installation directory.

    Deleting these directories forces Tomcat to read the edited WAR files when Alfresco is restarted.

4. Remove any `share-config-custom.xml` customizations that you added when you installed the SAML module.

    For example:

    1. If you are using Alfresco Share as your service provider, and you have custom CSRFPolicy configurations in your installation, remove the *SAML SPECIFIC CONFIG* section, and save.

    2. Remove the contents of `share-config-custom.xml.sample` from your `share-config-custom.xml` file, and save. If there is no other content in your `share-config-custom.xml` file, you can simply remove the file.

5. Restart the Alfresco server.
---
title: Supported platforms
---

The following are the supported platforms for SAML Module for Alfresco Content Services 1.2:

| Version | Notes |
| ------- | ----- |
| Content Services 7.0.x | |
| Content Services 6.2.x | |
| **Application servers** | |
| Tomcat 8.5.43 | |
| **Third party integrations** | |
| Microsoft Office 2013 | |
| Microsoft Office 2016 | |
