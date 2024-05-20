---
title: Alfresco Content Connector for Salesforce
---

Alfresco Content Connector for Salesforce allows you to store documents in Alfresco Content Services, but access them directly from Salesforce.

New features introduced in v3.1 include support for multiple Salesforce organizations (or instances). This adds the ability to connect a single Content Services instance to multiple Salesforce organizations.

Other features introduced in previous versions include:

* **Full document management support**

  * You can upload, share, edit, and delete files and folders in Salesforce that are stored securely in Content Services. It also provides version history and tagging capability. You can store personal files as well as those that you want to share.
  * You can link files and folders to Salesforce records.
  * You can choose what metadata and record properties are carried through from Salesforce to Content Services.

* **Access for non-Salesforce users**

  * Non-Salesforce users can access content, as it is stored in Content Services, enabling secure online collaboration with people outside your organization.

* **Automated business processes**

  * You can set up rules in Content Services that automatically manage your Salesforce business processes. For example, you could set up rules so that your documents are sent straight to the right people for approval as soon as they're saved in Content Services. You can then track the progress and completion of the approval process.
---
title: Configure Salesforce Connector
---

This page describes how to configure the Salesforce Connector for use with Single Sign On (SSO).

Here, you'll use the Identity Service with Salesforce and Alfresco Content Services. There are two parts to this configuration - first configure SSO for the Salesforce Connector, and then configure your Salesforce domain to use the Identity Service as SSO.

## SSO prerequisites {#prereqs}

Before you begin ensure you've installed the following - see the [Supported platforms]({% link salesforce/latest/support/index.md %}) page for specific versions:

* [Alfresco Content Services]({% link content-services/latest/install/index.md %})
* [Alfresco Content Connector for Salesforce]({% link salesforce/latest/install/index.md %})
* [Identity Service]({% link identity-service/latest/install/index.md %})

There are two parts to this configuration: [configure SSO between Content Services and the Salesforce Connector](#sso-alfresco) and [configure SSO for Salesforce](#sso-salesforce)

## Configure SSO in Alfresco products {#sso-alfresco}

To configure Single Sign On (SSO) between Content Services and the Salesforce Connector, you must add your Identity Service URL to `JAVA_OPTS`, and also configure your `X-Frame-Options` and `Content Security Policy` in the Identity Service.

Ensure you have the [prerequisites](#prereqs) installed and configured first.

1. Stop Alfresco Content Services.

2. Set `JAVA_OPTS=%JAVA_OPTS% -Dsfdc.config.trustedOrigins=<Identity Service URL>` in:

    For Linux based users: `<TOMCAT_HOME>/bin/catalina.sh`

    For Microsoft Windows users: `<TOMCAT_HOME>/bin/catalina.bat`

3. Navigate to your Identity Service and log in as an Administrator.

4. Log in to the Administration Console.

5. Select the **Alfresco** realm from the drop list on the top left.

6. Go to **Realm Settings > Security Defenses** tab.

7. Add `ALLOW-FROM <Your Salesforce URL>` to the **X-Frame-Options** field.

8. Add `frame-src 'self' <Your Salesforce URL>` to the **Content-Security-Policy** field.

    > **Note:** `<Your Salesforce URL>` can take two different forms:
    >
    > * For the Classic view, the URL will take the form `visual.force.com`.
    > * For the Lightning view, the URL will take the form `lightning.force.com`.

## Configure SSO for Salesforce {#sso-salesforce}

To configure Single Sign On (SSO) for use with Salesforce you must create a new authentication provider in Salesforce, create a Salesforce domain, configure a Custom Logout URL for Salesforce, and update the Apex Code.

Ensure you have the [prerequisites](#prereqs) installed and configured first, and have also [configured SSO in Alfresco products](#sso-alfresco).

1. To create an authentication provider, navigate to Salesforce and log in as an Administrator.

2. Go to **Setup Tab > Identity > Auth. Providers** and click **New**.

3. Select **OpenID Connect** from the **Provider Type** drop down list.

    The table represents the fields on the **Auth. Provider Edit** window.

    |Auth. Provider create fields|Value/Description|
    |----------------------------|-----------------|
    |Provider Type|OpenID Connect|
    |Name|Enter a name for the authentication service.|
    |URL Suffix|Automatically filled in based on the name you enter.|
    |Consumer Key|To find this key go to Identity Service > **Alfresco Realm > Clients** and the client ID you have configured for Alfresco Content Services. The key is usually `alfresco`.|
    |Consumer Secret|1. Go to the Identity Service > **Alfresco Realm > Realm Settings > Keys Tab**.<br>2. Click **Public key** next to the algorithm that has one.<br>3. Copy and paste the key.|
    |Authorize Endpoint URL|1. Go to the Identity Service > **Alfresco Realm > Realm Settings**.<br>2. Click the link in the **Endpoints** field.<br>3. Copy and paste the JSON output into a reader to make it more readable.<br>4. Find the value for `authorization_endpoint`.<br>5. Copy and paste the value.<br><br>**Note:** Keep the JSON file because it will be used to find other URLs for other fields.|
    |Token Endpoint URL|1. Find the value for `token_endpoint` in the JSON file.<br>2. Copy and paste the value.|
    |User Info Endpoint URL|1. Find the value for `userinfo_endpoint` in the JSON file.<br>2. Copy and paste the value.|
    |Token Issuer|1. Find the value for `issuer` in the JSON file.<br>2. Copy and paste the value.|
    |Default Scopes|OpenID email<br><br>**Note:** See [Use the Scope URL Parameter](https://help.salesforce.com/articleView?id=sso_provider_addl_params_scope.htm&type=5){:target="_blank"} for more on the use of OpenID.|
    |Send access token in header|Selected|
    |Send client credentials in header|Not Selected|
    |Include Consumer Secret in API Responses|Selected|
    |Custom Error URL|Leave Empty|
    |Custom Logout URL|Leave Empty<br><br>**Note:** The Custom Logout URL will be configured later on in the configuration steps.|
    |Registration Handler|Select an existing Registration Handler for your provider or click **Automatically create a registration handler template**.<br><br>**Note:** Creating a template will require modification by your Salesforce team for it to  work for your use case and provider.|
    |Execute Registration As|Select an Admin user.|
    |Portal|None|
    |Icon URL|***Optional.*** Enter a URL where an image can be found.|

4. Enter your information in the fields and click **Save**.

5. To create your domain go back to **Setup Tab > Company Settings > My Domain**.

6. Enter the name of the domain you want to use and click **Check Availability**.

7. Click **Register Domain** if it's available.

    You will see a notice that tells you the domain is registering. This process may take 60 minutes.

8. Once the domain is registered you can test it. Use the **Login** button to log in and test the domain.

9. Click **Deploy to Users** to deploy your domain.

10. Click **Edit** under the **Authentication Configuration** heading.

11. Select the Auth. Provider service you have created under the **Authentication Service** heading and click **Save**.

12. To add your **Custom Logout URL** copy your domain name as it appears next to **Your domain name is**.

13. Go back to **Setup Tab > Identity > Auth. Providers** and edit the authentication provider you created earlier.

14. Paste your domain URL into the **Custom Logout URL** field.

15. Navigate to the JSON file you used earlier and find the value of `end_session_endpoint` and also paste it into the **Custom Logout URL** field.

16. Add `?redirect_uri=` between your domain URL and the `end_session_endpoint` value and click **Save**.

    It should take the form of `end_session_endpoint?redirect_uri=<Your domain>`.

### Customize Registration Handler {#configure-handler}

Configuring the registration handler should be completed by someone with an understanding of Apex, Salesforce SSO, and your identity provider. Below is a sample approach for a simplified implementation using the default template. This should not be used for production as it may not meet your specific needs. We encourage testing to validate that your registration handler is configured correctly. This is not a definitive guide on how to customize the registration handler.

1. To update the Apex code, in the newly created Auth. Providers window click the link next to **Registration Handler** to open the **Apex classes** window.

2. Click **Edit** and change the generate Global Class name to something more meaningful to you such as *`IdentityServiceRegistrationHandler`*.

    The generated name will be something like *`AutocreatedRegHandler1624989012775`*.

3. Comment out all references to the method `canCreateUser(Auth.UserData data)`.

    If the method references are not commented out, you will not be able to log in through your provider because a new user will not be created. The method is `false` by default.

4. In the `createUser` method, change the value of the string `@myorg.com` to be the email domain as specified in your identity provider within the section where  a standard user object is instantiated. To do this within the Apex code:

    * Find `u.username = data.username + '@myorg.com'` and add your domain instead.
    * If your providers username is formated as an email address, change the line to be `u.username = data.username`.

> **Note:** In the example above, a new Salesforce user is created at login through your provider. If you are attempting to match an existing Salesforce user, the same `createUser` method is called, but the Registration Handlers Apex code should be updated to use some combination of identifiable values from your provider to query Salesforce to find user values to identify, and return an existing user instead of attempting to create a new user.

> **Note:** You can configure the Apex code in lots of different ways to suit your organization. See the Salesforce documentation for more information:
>
> * [What is Apex?](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_intro_what_is_apex.htm){:target="_blank"}.
> * [Setup SSO for your users](https://developer.salesforce.com/docs/atlas.en-us.externalidentityImplGuide.meta/externalidentityImplGuide/external_identity_accept_identity_from_existing_provider.htm){:target="_blank"}.
> * [RegistrationHandler Interface](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_auth_plugin.htm){:target="_blank"}.

## Configure a Salesforce Community

To configure access to Salesforce Community you must add the internal Salesforce users to the `GROUP_SALESFORCE_MODERATORS` group in Alfresco Content Services.
Internal Salesforce users added to this group will be allowed to share content externally to Community Members. Users not added to this group will not be granted access to share content externally.

> **Note:** Support for Salesforce Community is only available when using Alfresco Cloud (PaaS).

1. Log in to Alfresco Content Services as an administrator and click **Admin Tools**.

2. Click **Groups** under **Users and Groups**.

3. Select **Show System Groups** on the top right.

4. Click **Browse** and select `GROUP_SALESFORCE_MODERATORS`.

5. Click the **Add User** icon.

    You are presented with the **Add User** window.

6. Search for the administrator user you want to add.

7. Click the **Add** button next to the user.

You will see the user you have added will appear in the middle column.

### Add trustedOrigin configuration for Salesforce Communities

Add the `sfdc.config.trustedOrigins` property to allow the connector to be displayed within a Salesforce Community page, for example, `alfresco-content-connector.my.site.com`. This property accepts multiple values, where each value is separated by the pipe character, `|`, for example, `alfresco-content-connector.my.site.com|alfresco-sales.my.site.com`.

1. Stop Alfresco Content Services.

2. Set `JAVA_OPTS=%JAVA_OPTS% -Dsfdc.config.trustedOrigins=<Community domain name>` in:

    For Linux based users: `<TOMCAT_HOME>/bin/catalina.sh`

    For Microsoft Windows users: `<TOMCAT_HOME>/bin/catalina.bat`

    Example: `-Dsfdc.config.trustedOrigins=alfresco-content-connector.my.site.com`
---
title: Install Salesforce Connector
---

You now have a choice of selecting your organization's user interface experience: Salesforce Classic UI or the new Salesforce Lightning UI.

The Lightning Experience offers a more streamlined user experience by providing tools to create components that are reusable across applications and devices.

To begin, [install the AMP files](#installamps) and then [install the app in Salesforce](#installapp). Depending on what's the best layout for your organization, choose one of the following UIs:

* [Install Salesforce Connector - Lightning Experience](#install-lightning)
* [Install Salesforce Connector - Classic](#installclassic)

## Prerequisites

There are a number of software requirements for using the Salesforce Connector.

See [Supported platforms]({% link salesforce/latest/support/index.md %}) for specific versions.

### Alfresco requirements

* Alfresco Content Services
* Identity Service (if you plan to use Single Sign On (SSO))

> **Note:** Support for Salesforce Community is only available when using Alfresco Cloud (PaaS).

### Salesforce requirements

Salesforce Group is the minimum requirement. See [Salesforce Connected Apps](https://help.salesforce.com/apex/HTViewHelpDoc?id=connected_app_overview.htm){:target="_blank"} for guidance on levels of Salesforce required with connected apps.

### Java requirements

* OpenJDK 17.

### Other requirements

Your Salesforce and Alfresco instances must be on a shared network or otherwise accessible in order to share information.

## Support for multiple Salesforce organizations

Starting from version 3.1, the Salesforce Connector provides support for multiple Salesforce organizations (or instances) adds the ability to connect a single Content Services instance to multiple Salesforce organizations. This may be a combination of Production and Sandbox organizations. The detailed steps are included in **Step 4** of the installation steps for the Salesforce Classic and Lightning Experience.

## Step 1: Install AMP files {#installamps}

Download and install the AMP files to connect to Salesforce.

Make sure you are running the correct versions of operating system and software before you install the AMP files. See [Prerequisites for using Salesforce Connector](#prerequisites) for more information.

1. Stop the Alfresco server.

2. Browse to [Hyland Community](https://community.hyland.com/){:target="_blank"}, download and unzip the Salesforce zip package.

3. Copy the provided AMP files to the Alfresco `amps` and `amps_share` directories.

    Copy this file to the `amps` directory:

    * `alfresco-content-connector-for-salesforce-repo-3.1.x.amp`

    Copy this file to the `amps_share` directory:

    * `alfresco-content-connector-for-salesforce-share-3.1.x.amp`

4. To install the AMP files, run the `apply_amps.bat` file from the Alfresco `bin` directory.

    Check the output from the script to ensure that the AMP files have installed successfully.

5. Restart the Alfresco server.

6. If you are running Alfresco One 5.1 or later, check for any `Aikau * Module Config.xml` files, and delete them.

    Use the Node Browser (`http://host:port/alfresco/s/enterprise/admin/admin-nodebrowser` for Alfresco One 5.0 and `http://host:port/alfresco/s/admin/admin-nodebrowser` for Alfresco One 5.1) using this `xpath`:

    ```text
    /app:company_home/st:sites/cm:surf-config/cm:module-deployments
    ```

7. Locate the `share-config-custom.xml.sample` file.

    This sample configuration file is shipped with in Salesforce zip file and shows the required rules (and properties) that need to be added to the `CSRFPolicy` to allow Salesforce logouts.

    1. If you are using Alfresco Share as your service provider, and you have custom `CSRFPolicy` configurations in your installation, copy and paste the `SALESFORCE SPECIFIC CONFIG` section of the sample file into your custom `CSRFPolicy` filter, and save.

    2. If you have a `share-config-custom.xml` file in your Alfresco Share installation, merge the contents of `share-config-custom.xml.sample` into your `share-config-custom.xml` file, and save.

    3. Alternatively, if you do not have a `share-config-custom.xml` in your Alfresco Share installation, rename `share-config-custom.xml.sample` to `share-config-custom.xml`.

    4. Review the details in the `CSRFPolicy` section for accuracy.

8. Test that the AMPs have been applied successfully.

    Using your administrator logon, go to:

    ```html
    http://localhost:8080/alfresco/s/enterprise/admin/admin-salesforce
    ```

    where `localhost` is your Alfresco host name, and `8080` is your port number. You'll see the Salesforce settings that you will need to link Alfresco to Salesforce.

9. Create a new site to hold your Salesforce content.

    Log on to Alfresco:

    ```html
    http://localhost:8080/share
    ```

    where `localhost` is your Alfresco host name, and `8080` is your port number. Follow these instructions: [Creating sites]({% link content-services/latest/using/sites/index.md %}#creating-a-site). You can use this as your default site for Salesforce.

## Step 2: Install the Salesforce connector app {#installapp}

The Alfresco Content Connector app is available on the Salesforce AppExchange.

This task assumes that you are installing the app through the AppExchange.

If you've been provided a URL to install the Salesforce Connector, log in to Salesforce, and paste the URL you've been given into your browser. Select the required security level option, click **Install**, and then click **Done** when the installation is complete.

1. Search for Alfresco Content Connector in the [Salesforce AppExchange](https://appexchange.salesforce.com/){:target="_blank"}, and download the app.

    >**Note:** You'll need to log in the AppExchange first.

2. Click **Get it Now** to download.

3. Confirm whether you want to **Install in production** or **Install in sandbox** environment.

    Selecting **Install in production** will install the Alfresco Content Connector to your live Salesforce environment.

4. Read the terms and conditions then click **Confirm and Install**.

    >**Note:** You might be prompted to re-enter your Salesforce login details.

    The Package Installation Details screen displays the package details, including the package name, version name, version number, the publisher name, description of the application, and the package components.

5. Click **Continue**.

6. Select the required security level option in the **Choose security level** screen.

    You have three options:

    * **Install for Admins Only**
    * **Install for All Users**
    * **Install for Specific Profiles...**
  
    > **Note:** Selecting a security level can have an effect on future usage. When choosing a level you may be required to manually adjust permissions for users, profiles, or permission sets along with adding those users, profiles, and permission sets directly on classes, Visualforce pages, and/or the Connected App Definition.
    >
    > Specifically, you may need to adjust permissions on the `AlfrescoCanvasLifeCycleHandler` and add the API Enabled permission on a profile.
    >
    > **Permission Sets** and **Profiles** can also be used with the Connected App Definition to control who can see/use the Connector within a page layout.
    >
    > Consult with your Salesforce Admin in your organizations best practices when applying permissions.

7. Click **Next**, then on the next screen click **Install**.

8. Click **Done** when the installation is complete.

    After a few seconds the Install Complete screen displays confirming that the Alfresco Content Connector is installed.

    From here you can choose to **View Components**, **View Dependencies**, or **Uninstall**.

Depending on what's the best layout for your organization, you can choose either to [Install the Salesforce Connector - Lightning Experience](#install-lightning) or [Install the Salesforce Connector - Classic](#installclassic).

## Install Salesforce Connector - Lightning Experience {#install-lightning}

Use this information to install the AMP files in Alfresco, and the Alfresco App in Salesforce with the Lightning Experience UI.

### Step 3: Configure app in Salesforce {#configappinsalesforce-lightning}

After you've installed the app, create a new connected app definition using the Salesforce Setup menu.

Make sure that you've downloaded the Alfresco Content Connector app, as described in [Step 2: Install the app in Salesforce](#installapp). In this task, you'll use the Setup menu in Salesforce to customize the install. You need administrator rights to make these changes.

1. In your Salesforce account, find Setup. This is accessible by clicking the gear icon, ![]({% link salesforce/images/gear.png %}){:height="18px" width="18px"}, from the top-right toolbar on the Salesforce page.

    See [Explore the Salesforce Setup Menu](https://help.salesforce.com/articleView?id=basics_nav_setup.htm&type=5){:target="_blank"} for more guidance on where to find this.

    Search for Apps in the Quick Find search bar, and click **App Manager** to see your installed apps.

2. Click **New Connected App** to create a new connected app.

    ![salesforce-connected-app]({% link salesforce/images/salesforce-connected-app.png %})

    This new app extends the standard connector to work for your organization. Use the following settings:

    1. **Connected App Name**: Name your app something memorable and unique; for example, `Alfresco On-Premise`
    2. **API Name**: Choose a meaningful name. This is the name used by the API and managed packages. The name must be less than or equal to 40 characters.

        >**Note:** A suggested name is `Alfresco_for_Salesforce`. You'll need to remember the API Name when you configure the Alfresco Setup tab.

        >**Note:** If this is not set up correctly, you'll see an error message. See [Troubleshooting]({% link salesforce/latest/using/troubleshoot.md %}) for guidance.

    3. **Contact Email**: Enter an administrator email address.
    4. Check **Enable OAuth Settings**.
    5. **Callback URL**: this field is not used, but does need to be completed. You can set this to `https://www.alfresco.com/dummy_callback`.
    6. In **Selected OAuth Scopes** add the following scopes:

        * `Full access (full)`
        * `Perform requests on your behalf at any time (refresh_token, offline_access)`

    7. Check **Force.com Canvas**.
    8. In **Canvas App URL**, enter a secure (https) URL that points to the Alfresco Share environment, that you have configured with the Alfresco Content Connector. You also need a suffix of `share/page/sfdc/canvas/signedrequest`. For example:

        ```html
        https://localhost:8443/share/page/sfdc/canvas/signedrequest
        ```

    9. **Access Method**: Select Signed Request (POST)
    10. Add these **Locations**:

        * `Chatter Tab`
        * `Layouts and Mobile Cards`
        * `Lightning Component`
        * `Visualforce Page`

        These are locations in Salesforce where the canvas app can be displayed.

    11. In **Lifecycle Class**, look up the options and select `AlfrescoCanvasLifeCycleHandler`.
    12. Click **Save** to save your settings.

    Next, you’ll need to manage the connected app that you've just created.

3. For the new connected app, click **Manage** to set permissions and accessibility.

4. In the OAuth policies section, enter these values:

    1. **Permitted Users**: Select `Admin approved users are pre-authorized`.
        Click **OK** to accept the Salesforce message.
    2. **IP Relaxation**: Select `Enforce IP restrictions`.
    3. **Refresh Token Policy**: Select the `Refresh token is valid until revoked` radio button.
    4. **Save** your settings.

5. In the Manage Profiles section, click **Manage Profiles**, check the required profiles, and **Save** your settings.

    For example, select `System Administrator` and `Standard User`. We'll now find the consumer secret ready to paste into Alfresco.

### Step 4: Enable Salesforce in the Admin Console

You'll need to copy the Salesforce consumer key and consumer secret from your connected app into the Alfresco Admin Console. These credentials prove that Alfresco has permission to be displayed in and communicate with Salesforce.

Make sure that you've applied your AMP files, downloaded the Alfresco Content Connector app, and created a connected app, as described in the previous sections. You need administrator rights to make these changes.

1. In your Salesforce account, click the gear icon ![]({% link salesforce/images/gear.png %}){:height="18px" width="18px"} from the top-right toolbar on the Salesforce page, and click **Setup Home**.

2. Under **PLATFORM TOOLS**, click **Apps > App Manager**.

3. On the **Lightning Experience App Manager** screen, click the down-arrow icon for the app that you created in [Step 3: Configure the app in Salesforce](#configappinsalesforce-lightning) and select **View**.

    ![sf-view]({% link salesforce/images/sf-view.png %})

4. In the **API (Enable OAuth Settings)** section, click **Manage Consumer Details** to reveal the Consumer Key and Secret. You'll return to this screen to copy the code for both fields.

   ![sf-manage-consumer-details]({% link salesforce/images/sf-manage-consumer-details.png %})

5. In a separate browser window, log on to the Salesforce page of the Alfresco Admin Console with your administrator credentials:

    ```html
    http://localhost:8080/alfresco/service/enterprise/admin/admin-salesforce
    ```

    where `localhost:8080` is your Alfresco host name and port.

6. In the Admin Console window, click **Add Connection**.

   A new window opens that allows you to enter the Salesforce Organization Id, Salesforce Consumer Token, and Salesforce Consumer Secret.

7. Paste your Salesforce Org Id into **Salesforce Org Id**.

   Here's how to find your Organization Id in your Salesforce account:

   1. Navigate to **Salesforce Settings**.
   2. Click on **Company Settings**.
   3. Select **Company Information**.

      The Salesforce.com Organization Id is shown in this window.

8. From the Salesforce window, copy your **Consumer Key** and paste it into the Admin Console **Salesforce Consumer Token**.

9. From the Salesforce window, copy your **Consumer Secret** and paste it into the Admin Console **Salesforce Consumer Secret**.

    You can optionally hide the password when you have pasted it into the Admin Console.

10. Select the **Salesforce Environment Type** that Alfresco should use.

    There are two options: `Production` (the default value) and `Sandbox`:

    ![sf-adminconsole]({% link salesforce/images/sf-adminconsole.png %})

11. Save the new connection by clicking the **Save** button.

12. (*Optional*) You can change the list size of records that are displayed.

    Enter a number in **Recently Viewed Records List Size** to specify how many recent Salesforce records are displayed when you link an Alfresco file or folder with a record. The default setting is `20` records.

    >**Note:** Alternatively, you can set this in your `alfresco-global.properties` file using `sfdc.canvas.recordMruSize`.
    >
    >For example: `sfdc.canvas.recordMruSize=10`

13. **Save** your settings.

Once a connection is created, you can add additional connections, if needed. You can also remove or update an existing connection. Removing a connection won't remove any content.

> **Important:**
>
> * Upgrading the Salesforce Connector requires you to re-add any previous connections.
> * Re-adding the connection won't affect any content that you've previously added through the Salesforce Connector.

In the Salesforce Record Folder, you'll now see a new metadata field: `Organization Id`. This can help you differentiate Salesforce records added through different Salesforce organizations. A link is also added in the folder description of the Salesforce Record, if no other value is currently present. This link allows you to directly navigate to the Salesforce Record.

### Step 5: Add an Alfresco site and map metadata in Salesforce

Configure the Alfresco site that you want to point to, and map your metadata.

Make sure that you've downloaded the Alfresco Content Connector app, as described in [Step 2:. Install the app in Salesforce](#installapp). You need administrator rights to make these changes.

1. In Salesforce, click **Alfresco Content Connector**. This is available from the **App Launcher**.

2. Click the **Alfresco Setup** tab and in **API Name**, enter the API name of the connected app definition you created in [Step 3: Configure the app in Salesforce](#configappinsalesforce-lightning).

    >**Note:** The API name must be less than or equal to 40 characters.

    If your API name appears as `Alfresco_Content_Connector_for_Salesforce`, then you must to change it to `Alfresco_for_Salesforce`.

    This sets the Alfresco site that you want to use for your content. If this isn't set up correctly, you'll see an error message. See [Troubleshooting]({% link salesforce/latest/using/troubleshoot.md %}) for guidance.

3. You'll see two tabs; **Site to Object Mapping** and **Metadata Mapping**. Select a tab and you'll see the Alfresco login screen. Log in to your connected Alfresco instance.

    This is a sample screen, before logging in:

    ![salesforce_admin_tab]({% link salesforce/images/salesforce_admin_tab.png %})

    The **Site to Object Mapping** and **Metadata Mapping** tabs set where Salesforce puts content in Alfresco.

    >**Note:** Metadata mapping is available with Alfresco One 5.1 and later versions only.

    It can take a little while for Alfresco to load the first time you log in, or after an Alfresco server restart.

4. In **Site to Object Mapping**:

    1. Click **Set Default Site** and choose the site that you want to set as the default entry point for your organization, and **Save**.

    2. Click **Add New Mapping** to specify where content of a specific Salesforce object type should be stored in Alfresco. Pick a site and an object type that maps to that site.

        For example, you can map documents with a Contracts object type to a site that contains only contracts in Alfresco, or you can map sensitive HR data to an HR object type. Your mappings are then displayed in a table.

5. In **Metadata Mapping**:

    1. Choose a Salesforce object and select from the list of associated properties.

        This defines what Salesforce properties or metadata that you want to share with Alfresco.

    2. Click **OK**.

        A new Salesforce object type is created, with a matching Alfresco model with an associated aspect, and the specified properties. This creates a new model in Alfresco.

    You can enable or disable an object model. If a model is:

    * `Enabled`: metadata is synchronized with the Alfresco object model.
    * `Disabled`: metadata can't be synchronized with the Alfresco object model.

    >**Note:** Models are inactive when they are added to Salesforce, and can be deleted while they're inactive. A model can be explicitly activated and deactivated. A model can be deleted only if it's deactivated and has not been used. If the model has been used and a user attempts to delete it, an error message is issued explaining that it can't be removed. See [Content modeling with Model Manager]({% link content-services/latest/config/models.md%}) for more.

    >**Note:** Do not edit the prefix of a Salesforce model, as this can make your model unusable. Also, do not update the model in the Model Manager in Share.

    Here is an example of a completed Alfresco Setup tab:

    ![site_and_metadata]({% link salesforce/images/site_and_metadata.png %})

### Step 6: Add the Alfresco app using a Salesforce Lightning Component {#addappusinglightningcomponent}

To allow the Alfresco Content Connector to appear in the Lightning experience view of Salesforce you need to add a Salesforce lightning component.

Make sure that you've downloaded the Alfresco Content Connector app, as described in [Step 2: Install the app in Salesforce](#installapp). You need administrator rights to make these changes. You also need to have a custom Salesforce domain that has been deployed and activated for your users, for more see [Configure SSO for Salesforce]({% link salesforce/latest/config/index.md %}#prereqs).

To create the Lightning Component follow these steps:

1. Login to Salesforce Lightning view with an administrator account.

2. Click the gear icon ![gear]({% link salesforce/images/gear.png %}){:height="18px" width="18px"} from the top-right toolbar on the Salesforce page and select **Developer Console**.

3. Go to **File > New > Lightning Component**.

    You will see the New Lightning Bundle window.

4. Enter a Name and a Description and click **Submit**.

    >**Note:** You do not need to select any of the check boxes.

5. Select the Component part of the bundle by clicking **COMPONENT** in the right hand pane.

6. Remove any code already in there, and copy and paste the following code snippet into the window.

    ```xml
    <aura:component implements="flexipage:availableForRecordHome,force:hasRecordId,force:hasSObjectName">
        <aura:attribute name="canvasParameters" type="string" />
        <aura:handler name="init" value="{!this}" action="{!c.doInit}"/>
        <force:canvasApp developerName="THE NAME OF YOUR CANVAS APP" height="450px" width="1300px" parameters="{!v.canvasParameters}"/>
    </aura:component>
    ```

7. Edit the code and add the name of your **Canvas App** as the value of the `developerName` property.

8. Select the Controller part of the bundle by clicking **CONTROLLER** in the right hand pane.

9. Remove any code already in there, and copy and paste the following code snippet into the window.

    ```json
    ({
        doInit : function(cmp, evt, helper) {
            var recordId = cmp.get("v.recordId");
            var sObjectName = cmp.get("v.sObjectName");
            cmp.set("v.canvasParameters", JSON.stringify({
                recordId: recordId,
                type: sObjectName
            }));
        }
    })
    ```

10. Click **File** and **Save All**.

11. Edit your Record page by clicking the gear icon ![gear]({% link salesforce/images/gear.png %}){:height="18px" width="18px"} and then clicking **Edit**.

12. Under the Custom heading in the left hand pane drag over and then drop the component into the desired location on the Activity tab of the Record page.

    >**Note:** If your Component is not visible you will see a message that will instruct you to deploy your domain.

13. Click the Activation button on the top right, to activate your change.

    Review the Activation Opportunity Record Page and assign the level you want for this component.

14. Click **Close**.

15. Click the **Save** button on the top right and then the Salesforce **Back** button directly above it.

    The component is now ready to use.

## Install Salesforce Connector - Classic {#installclassic}

Use this information to install the AMP files in Alfresco, and the Alfresco App in Salesforce with the Classic UI.

### Step 3: Configure app in Salesforce {#configappinsalesforce-classic}

After you've installed the app, create a new connected app definition using the Salesforce Setup menu.

Make sure that you've downloaded the Alfresco Content Connector app, as described in [Install the app in Salesforce](#installapp). In this task, you'll use the Setup menu in Salesforce to customize the install. You need administrator rights to make these changes.

1. In your Salesforce account, find **Setup**. This is often on the toolbar or under your name (see [Explore the Salesforce Setup Menu](https://help.salesforce.com/articleView?id=basics_nav_setup.htm&type=5){:target="_blank"} for more guidance on where to find this).

    Search for Apps in the Quick Find search bar, and in **App Setup** click **Create > Apps** to see your installed apps.

2. Scroll down to **Connected Apps** and click **New** to create a new connected app.

    ![salesforce_connected_apps]({% link salesforce/images/salesforce_connected_apps.png %})

    This new app extends the standard connector to work for your organization. Use the following settings:

    1. **Connected App Name**: Name your app something memorable and unique; for example, `Alfresco On-Premise`
    2. **API Name**: Choose a meaningful name. This is the name used by the API and managed packages. The name must be less than or equal to 40 characters.

        >**Note:** A suggested name is `Alfresco_for_Salesforce`. You'll need to remember the API Name when you configure the **Alfresco Setup** tab.

        >**Note:** If this is not set up correctly, you'll see an error message. See [Troubleshooting]({% link salesforce/latest/using/troubleshoot.md %}) for guidance.

    3. **Contact Email**: Enter an administrator email address.
    4. Check **Enable OAuth Settings**.
    5. **Callback URL**: this field is not used, but does need to be completed. You can set this to `https://www.alfresco.com/dummy_callback`.
    6. In **Selected OAuth Scopes** add the following scopes:
        * `Full access (full)`
        * `Perform requests on your behalf at any time (refresh_token, offline_access)`
    7. Check **Force.com Canvas**.
    8. In **Canvas App URL**, enter a secure (https) URL that points to the Alfresco Share environment, that you have configured with the Alfresco Content Connector. You also need a suffix of `share/page/sfdc/canvas/signedrequest`. For example:

        ```html
        https://localhost:8443/share/page/sfdc/canvas/signedrequest
        ```

    9. **Access Method**: Select `Signed Request (POST)`
    10. Add these **Locations**:

        * `Chatter Tab`
        * `Layouts and Mobile Cards`
        * `Visualforce Page`

        These are locations in Salesforce where the canvas app can be displayed.

    11. In **Lifecycle Class**, look up the options and select `AlfrescoCanvasLifeCycleHandler`.
    12. Click **Save** to save your settings.

    Next, you’ll need to manage the connected app that you have just created.

3. For the new connected app, click **Manage** to set permissions and accessibility.

4. In the **OAuth policies** section, enter these values:

    1. **Permitted Users**: Select `Admin approved users are pre-authorized`.
        Click **OK** to accept the Salesforce message.
    2. **IP Relaxation**: Select `Enforce IP restrictions`.
    3. **Refresh Token Policy**: Select the `Refresh token is valid until revoked` radio button.
    4. **Save** your settings.

5. In the **Manage Profiles** section, click **Manage Profiles**, check the required profiles, and **Save** your settings.

    For example, select **System Administrator** and **Standard User**. We will now find the consumer secret ready to paste into Alfresco.

### Step 4: Enable Salesforce in the Admin Console

You'll need to copy the Salesforce consumer key and consumer secret and from your connected app into the Alfresco Admin Console. These credentials prove that Alfresco has permission to be displayed in and communicate with Salesforce.

Make sure that you've applied your AMP files, downloaded the Alfresco Content Connector app, and created a connected app, as described in the previous topics. You need administrator rights to make these changes.

1. In your Salesforce Setup menu, click **Create > Apps**, and then the connected app name that you created in [Step 3: Configure the app in Salesforce](#configappinsalesforce-classic).

2. In the **API (Enable OAuth Settings)** section, click **Manage Consumer Details** to reveal the Consumer Key and Secret. You'll return to this screen to copy the code for both fields.

   ![sf-manage-consumer-details]({% link salesforce/images/sf-manage-consumer-details.png %})

3. In a separate browser window, log on to the Salesforce page of the Alfresco Admin Console with your administrator credentials:

    ```html
    http://localhost:8080/alfresco/service/enterprise/admin/admin-salesforce
    ```

    where `localhost:8080` is your Alfresco host name and port.

4. In the Admin Console window, click **Add Connection**.

   A new window opens that allows you to enter the Salesforce Organization Id, Salesforce Consumer Token, and Salesforce Consumer Secret.

5. Paste your Salesforce Org Id into **Salesforce Org Id**.

   Here's how to find your Organization Id in your Salesforce account:

   1. Navigate to **Salesforce Settings**.
   2. Click on **Company Settings**.
   3. Select **Company Information**.

      The Salesforce.com Organization Id is shown in this window.

6. From the Salesforce window, copy your **Consumer Key** and paste it into the Admin Console **Salesforce Consumer Token**.

7. From the Salesforce window, copy your **Consumer Secret** and paste it into the Admin Console **Salesforce Consumer Secret**.

    You can optionally hide the password when you have pasted it into the Admin Console.

8. Select the **Salesforce Environment Type** that Alfresco should use.

    There are two options: `Production` (the default value) and `Sandbox`:

    ![sf-adminconsole]({% link salesforce/images/sf-adminconsole.png %})

9. Save the new connection by clicking the **Save** button.

10. (*Optional*) You can change the list size of records that are displayed.

    Enter a number in **Recently Viewed Records List Size** to specify how many recent Salesforce records are displayed when you link an Alfresco file or folder with a record. The default setting is 20 records.

    >**Note:** Alternatively, you can set this in your `alfresco-global.properties` file using `sfdc.canvas.recordMruSize`. For example:
    >
    >```text
    >sfdc.canvas.recordMruSize=10
    >```

11. **Save** your settings.

Once a connection is created, you can add additional connections, if needed. You can also remove or update an existing connection. Removing a connection won't remove any content.

> **Important:**
>
> * Upgrading the Salesforce Connector requires you to re-add any previous connections.
> * Re-adding the connection won't affect any content that you've previously added through the Salesforce Connector.

In the Salesforce Record Folder, you'll now see a new metadata field: `Organization Id`. This can help you differentiate Salesforce records added through different Salesforce organizations. A link is also added in the folder description of the Salesforce Record, if no other value is currently present. This link allows you to directly navigate to the Salesforce Record.

### Step 5: Add an Alfresco site and map metadata in Salesforce

Configure the Alfresco site that you want to point to, and map your metadata.

Make sure that you've downloaded the Alfresco Content Connector app, as described in [Step 2: Install the app in Salesforce](#installapp). You need administrator rights to make these changes.

1. In Salesforce, click **Alfresco Content Connector**. This is available from the **Force.com** App Menu.

2. Click the **Alfresco Setup** tab and in **API Name**, enter the API name of the connected app definition you created in [Configure the app in Salesforce](#configappinsalesforce-classic).

    >**Note:** The API name must be less than or equal to 40 characters.

    If your API name appears as `Alfresco_Content_Connector_for_Salesforce` then you must to change it to `Alfresco_for_Salesforce`.

    This sets the Alfresco site that you want to use for Alfresco content. If this is not set up correctly, you'll see an error message. See [Troubleshooting]({% link salesforce/latest/using/troubleshoot.md %}) for guidance.

3. You'll see two tabs; **Site to Object Mapping** and **Metadata Mapping**. Select a tab and you'll see the Alfresco login screen. Log on to your connected Alfresco instance.

    This is a sample screen, before logging on to Alfresco:

    ![salesforce_admin_tab]({% link salesforce/images/salesforce_admin_tab.png %})

    The **Site to Object Mapping** and **Metadata Mapping** tabs set where Salesforce puts content in Alfresco.

    >**Note:** Metadata mapping is available with Alfresco One 5.1 and later versions only.

    It can take a little while for Alfresco to load the first time you first log in, or after an Alfresco server restart.

4. In **Site to Object Mapping**:

    1. Click **Set Default Site** and choose the site that you want to set as the default entry point for your organization, and **Save**.

    2. Click **Add New Mapping** to specify where content of a specific Salesforce object type should be stored in Alfresco. Pick a site and an object type that maps to that site.

        For example, you can map documents with a Contracts object type to a site that contains only contracts in Alfresco, or you can map sensitive HR data to an HR object type. Your mappings are then displayed in a table.

5. In **Metadata Mapping**, choose a Salesforce object and select from the list of associated properties.

    This defines what Salesforce properties or metadata that you want to share with Alfresco. Click OK and a new Salesforce object type is created, with a matching Alfresco model with an associated aspect, and the specified properties. This creates a new model in Alfresco.

    You can enable or disable an object model. If a model is:

    * `Enabled`: metadata is synchronized with the Alfresco object model.
    * `Disabled`: metadata can't be synchronized with the Alfresco object model.

    >**Note:** Models are inactive when they are added to Salesforce, and can be deleted while they are inactive. A model can be explicitly activated and deactivated. A model can be deleted only if it is deactivated and has not been used. If the model has been used and a user attempts to delete it, an error message is issued explaining that it can't removed. See [Content modeling with Model Manager]({% link content-services/latest/config/models.md %}) for more.

    >**Note:** Do not edit the prefix of a Salesforce model, as this can make your model unusable.

    Here is an example of a completed Alfresco Setup tab:

    ![site_and_metadata]({% link salesforce/images/site_and_metadata.png %})

### Step 6: Add the Alfresco app in Salesforce

There are two ways to add the Connector in Salesforce Classic: as a [Canvas Component](#configappinsalesforce-classic-canvas) or as a [Visualforce Page](#configappinsalesforce-classic-visualforce).

#### Add the Alfresco app in Salesforce (Canvas Component) {#configappinsalesforce-classic-canvas}

Lastly, you'll need to load the Alfresco canvas app for page layouts. You can add the app to any record type that supports layouts (for example; Accounts, Cases, and Opportunities). This is done by setting Alfresco for Salesforce example page layouts as the default for selected user profiles.

Make sure that you've downloaded the Alfresco Content Connector app, as described in [Step 2: Install the app in Salesforce](#installapp). You need administrator rights to make these changes.

1. In your Salesforce account, find **Setup**. This is often on the toolbar or under your name (see [Explore the Salesforce Setup Menu](https://help.salesforce.com/articleView?id=basics_nav_setup.htm&type=5){:target="_blank"} for more guidance on where to find this).

    Search for `Page Layouts` in the Quick Find search bar, and in **App Setup > Customize**, choose the page layout for your selected page type (for example, Accounts).

2. Click **Edit** next to the layout you want and add the Alfresco app to the layout:

    1. From the available components in the scrollable window, select **Canvas Apps**.

    2. You might need to add a new section, depending on your page layout.

        If you need to add a new section, set it to **1-Column** with a minimum height of 350 pixels (400 pixels is the recommended height). Click **OK**. Drag and drop the section onto your layout, and save the changes, before adding the new canvas app.

    3. Click the canvas app that matches the Alfresco Content Connector connected app that you created in [Step 3: Configure the app in Salesforce](#configappinsalesforce-classic), and drag it to where you want it on your page.

        You can add a canvas app only once to a page. If you've already added the app, Salesforce shows you where on the page it has been added.

        ![salesforce_canvas_app]({% link salesforce/images/salesforce_canvas_app.png %})

    4. Set the canvas app to display in **1-Column** with a minimum height of 350 pixels (400 pixels is the recommended height), and click **OK**.

        If the Alfresco widget is too small, you can't see all the buttons and elements. For instance, it is not possible to log in as the buttons are not visible.

    5. Save your changes.

        It can take a little while for the Alfresco widget to load for the first time.

    6. Open a record that has the new page layout. You should now be able to see an Alfresco section, with a **Files** tab. You can add files here by dragging and dropping them, or by using the **Upload** button.

        You can also add new folders with the **Create** button. Equally, any files added in Alfresco can be seen in this window. This content is stored directly in Alfresco and can be viewed either in Salesforce, or in your usual Alfresco site.

#### Adding the Alfresco app in Salesforce (Visualforce Page) {#configappinsalesforce-classic-visualforce}

Lastly, you'll need to load the Alfresco canvas app for page layouts. You can add the app to any record type that supports layouts (for example; Accounts, Cases, and Opportunities). This is done by setting Alfresco for Salesforce example page layouts as the default for selected user profiles.

Make sure that you've downloaded the Alfresco Content Connector app, as described in [Step 2: Install the app in Salesforce](#installapp). You need administrator rights to make these changes.

To create the Visualforce Pages for each object where you want the app to appear, follow these steps:

1. In your Salesforce account, find Setup. This is accessible by clicking the gear icon ![gear]({% link salesforce/images/gear.png %}){:height="18px" width="18px"} from the top-right toolbar on the Salesforce page. See [How to find Setup](https://help.salesforce.com/apex/HTViewHelpDoc?id=basics_nav_setup.htm){:target="_blank"} for more guidance.

    From Setup, enter Visualforce Pages in the Quick Find search bar and then select **Visualforce Pages**.

2. Click **New** to open the Visualforce Page editor.

    1. Enter a **Label** for the page. The label is displayed where the page appears in the page layout.

    2. Enter a **Name** for the page.

    3. Check **Available for Salesforce mobile apps and Lightning Pages**.

        ![sf-visualforce-page]({% link salesforce/images/sf-visualforce-page.png %})

    4. Copy and paste the following code in the **Visualforce Markup** editor:

        ```xml
        <apex:page standardController="{Your Object Name}">
            <apex:canvasApp id="AlfCanvas" applicationName="{Your Connected App API Name}" width="100%" height="450px" scrolling="auto"/>
        </apex:page>
        ```

        >**Note:** Replace `{Your Object Name}` with the `sObject` or `custom object API` name where you want the app to appear. For example, `Account`, `Lead`, `Asset`, or `training__c`.
        >**Note:** Replace the {`Your Connected App API Name}` with the API Name you set when creating the Connected App definition. For example, `Alfresco_Content_Connector_for_Salesforce`.

3. **Save** your settings.

    Repeat Step 2 and 3 for every object where you want the app to appear.

4. Now for each Salesforce object where you want the app to appear, you need to add the Visualforce page you just created in the Lightning page layout. To do so, follow these steps:

    1. For example, if the Salesforce object is `Account`, then on the Salesforce page, click **Accounts**.

        The ACCOUNTS screen appears listing all the accounts.

    2. Click the account where you want the Visualforce page to appear.

    3. Click the gear icon ![gear]({% link salesforce/images/gear.png %}){:height="18px" width="18px"} from the top-right toolbar on the Salesforce page.

    4. Click **Edit Page**.

    5. Select **Visualforce** from the **Standard** components list in the scrollable window.

        You can drag and place the component where you want it on the page.

    6. Specify a **Label** for the Visualforce page. If no label is specified, the default label of the Visualforce page is used.

    7. Select the Visualforce page you have created from the **Visualforce Page Name** drop-down list. This field is mandatory.

    8. Specify a minimum **Height** of 450 pixels.

    9. **Save** your settings.

        If you're editing the page for the first, you may need to activate the page if this is the first time you are editing the page.

        It can take a little while for the Alfresco widget to load for the first time.

5. Open a record that has the new page layout. You should now be able to see an Alfresco section, with a Files tab. You can add files here by dragging and dropping them, or by using the Upload button.

    You can also add new folders with the Create button. Equally, any files added in Alfresco can be seen in this window. This content is stored directly in Alfresco and can be viewed either in Salesforce, or in your usual Alfresco site.

## Uninstall the Salesforce app and AMP files

Remove the Alfresco package in Salesforce and then use the Module Management Tool (MMT) and remove the AMP files.

1. In your Salesforce account, find **Setup**. This is often on the toolbar or under your name (see [Explore the Salesforce Setup Menu](https://help.salesforce.com/articleView?id=basics_nav_setup.htm&type=5){:target="_blank"} for more guidance on where to find this).

    Search for `Installed` in the Quick Find search bar, and click **Installed Packages**.

2. Click **Uninstall** next to the Alfresco Content Connector package, and confirm that you want to uninstall the package.

    For more information about removing packages in Salesforce, see [Uninstalling a Package](https://help.salesforce.com/articleView?id=distribution_uninstalling_packages.htm&type=5){:target="_blank"}.

3. Stop the server.

4. Use the information in [Uninstalling an AMP file]({% link content-services/latest/install/zip/amp.md %}#uninstall-an-amp-file) to uninstall the AMP files for Salesforce.

5. Restart the server.
---
title: Supported platforms
---

The following are the supported platforms for the Content Connector for Salesforce 3.1:

| Version | Notes |
| ------- | ----- |
| Content Services 23.x | |
| Identity Service 2.0 | If using Single Sign On (SSO) |

> **Note:** Support for Salesforce Community is only available when using Alfresco Cloud (PaaS).
---
title: Salesforce Community
---

Support for Salesforce Community allows external Salesforce Community Members to store and access documents in Alfresco. To provide access and share documents with external Salesforce Community Members, internal Salesforce users need to perform a series of actions.
Before you begin, ensure your internal Salesforce users have been added to the `GROUP_SALESFORCE_MODERATORS` group in Alfresco Content Services, for more see [Configure Salesforce Community]({% link salesforce/latest/config/index.md %}#configure-a-salesforce-community).
This documentation describes a Salesforce Case object, however any standard or custom object can be shared externally with Community Members.

> **Note:** Support for Salesforce Community is only available when using Alfresco Cloud (PaaS).

## Lightning Experience

1. See [Create an Experience Cloud Site pg. 51](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/communities.pdf){:target="_blank"}

2. See [Add Members to Your Experience Cloud Site pg. 54](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/communities.pdf){:target="_blank"}

3. [Share content externally to Community Members Lightning Experience](#share-content-externally-to-community-members-lightning-experience)

## Share content externally to Community Members Lightning Experience

1. Log in to Salesforce.

2. Log in as an administrator to Alfresco Share in the Canvas app.

      ![lightning-alfresco-tab]({% link salesforce/images/lightning-alfresco-tab.png %})

3. Click the down arrow next to **Cases** and then **New Case**.

      ![lightning-create-case]({% link salesforce/images/lightning-create-case.png %})

4. Select the required **Case Origin** and any other information needed for the case. Click **Save**.

      ![lightning-new-case]({% link salesforce/images/lightning-new-case.png %})

5. Click the drop down arrow next to **Change Owner** and select **Sharing**.

      ![create-new-lightning-page]({% link salesforce/images/lightning-sharing.png %})

6. Click the drop down arrow in the search bar and select **Public Group**.

      ![lightning-public-group]({% link salesforce/images/lightning-public-group.png %})

7. Type *all* into the search field and select **All Customer Portal Users**.

      ![lightning-portal-users]({% link salesforce/images/lightning-portal-users.png %})

8. Click the **Case Access** field and select the type of access required for this case. Click **Save**.

      ![lightning-share-access]({% link salesforce/images/lightning-share-access.png %})

9. Click the **Create** drop down list and select **Folder**.

      ![lightning-create-folder]({% link salesforce/images/lightning-create-folder.png %})

10. Enter the details you require for your new folder and then click **Create**.

      ![lightning-details-folder]({% link salesforce/images/lightning-details-folder.png %})

11. Click the **Actions** drop down list and select **Share Externally**.

    ![lightning-share-externally]({% link salesforce/images/lightning-share-externally.png %})

12. Select the **Salesforce Community Name** you would like to share with and the **Users**. Click **Save**.

      ![lightning-externally-select]({% link salesforce/images/lightning-externally-select.png %})

You will see a **Salesforce Community Member Access** message. The result of the performed actions is that when the Community Member logs into Salesforce they will see the case in their **All Open Cases** list.

## Salesforce Classic

1. See [Create an Experience Cloud Site pg. 51](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/communities.pdf){:target="_blank"}

2. See [Add Members to Your Experience Cloud Site pg. 54](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/communities.pdf){:target="_blank"}

3. [Share content externally to Community Members Salesforce Classic](#share-content-externally-to-community-members-salesforce-classic)

## Share content externally to Community Members Salesforce Classic

1. Log in to Salesforce.

2. Click **Alfresco Repository** and Log in as an administrator to Alfresco Share in the Canvas app.

      ![lightning-alfresco-tab]({% link salesforce/images/lightning-alfresco-tab.png %})

3. Click **Cases** and click the **Create New** drop down list and then select **Case**.

      ![classic-create-case]({% link salesforce/images/classic-create-case.png %})

4. Select the required **Case Origin** and any other information needed for the case. Click **Save**.

      ![classic-new-case]({% link salesforce/images/classic-new-case.png %})

5. Click the **Sharing** button above the case.

      ![classic-sharing]({% link salesforce/images/classic-sharing.png %})

6. Click the **Add** button.

      ![classic-sharing-add]({% link salesforce/images/classic-sharing-add.png %})

7. Search **Public Groups** and add **All Customer Portal Users** to the **Share With** column. Click **Save**.

      ![classic-sharing-groups]({% link salesforce/images/classic-sharing-groups.png %})

8. Click the **Create** drop down list and select **Folder**.

      ![classic-create-folder]({% link salesforce/images/classic-create-folder.png %})

9. Enter a name for the folder and click **Create**.

      ![classic-name-folder]({% link salesforce/images/classic-name-folder.png %})

10. Click the **Actions** button and select **Share Externally**.

      ![classic-share-externally]({% link salesforce/images/classic-share-externally.png %})

11. Select the **Salesforce Community Name** you would like to share with and the **Users**. Click **Save**.

      ![lightning-externally-select]({% link salesforce/images/lightning-externally-select.png %})

You will see a **Salesforce Community Member Access** message. The result of the performed actions is that when the Community Member logs into Salesforce they will see the case in their **All Open Cases** list.

## Community Member accessing shared content

1. Log in to Salesforce Community.

2. Click the **My Open Cases** drop down list and then select **All Open Cases**.

      ![lightning-open-cases]({% link salesforce/images/lightning-open-cases.png %})

3. Click the link of the case number that has been shared with you to open it.

      ![lightning-all-new]({% link salesforce/images/lightning-all-cases.png %})

4. Log in as a Community Member to access the case and documents linked to the case.

      ![lightning-alfresco-tab]({% link salesforce/images/lightning-alfresco-tab.png %})

  Community Members can download and view documents linked to the case. They can also upload documents to the case that will get stored in Alfresco.
  
## Community Visualforce Page Configuration and Setup

To expose the connector in a Salesforce Community (Digital Workspace) we need to add a visualforce page for the connector. 
Visualforce Page must be added to your Salesforce organization using the following template:

```xml
<apex:page docType="html-5.0" standardController="<Object API Name>">
 <apex:canvasApp id="AlfrescoConnector" applicationName="<Connected APP API Name>" width="100%" height="450px" scrolling="auto" parameters="{'community':'simple'}"/>  
</apex:page>
```

The connector is tied to a Standard or Custom Salesforce object. 

Insert your Object API Name as the value of the `standardController` attribute. For Example : Case or Opportunity

The `id` attribute is required and can be set to any non-empty, non-null value.

The `applicationName` attribute must be set to the API Name of the connected app created for the connector during the initial setup.

The `width`, `height`, and `scrolling` attributes can be set to values that meet the use case.

The most important attribute is the `parameters` attribute.  The value must be set to `{'community':'simple'}`.Without this value, the connector will surface the standard connector view. 

The Visualforce page will need to have the appropriate profiles added for it to be visible to the correct community users.

**Example 1:**

```xml
<apex:page docType="html-5.0" standardController="Case">
  <apex:canvasApp id="AlfCanvas3" applicationName="ACS_Salesforce" width="100%" height="450px" scrolling="auto" parameters="{'community':'simple'}"/>
</apex:page>
```

Add the new Visualforce Page to the desired record detail in your Salesforce Community.
---
title: Using Salesforce Connector
---

With the Salesforce Connector you can upload, create, and delete files, and link Alfresco content with Salesforce records. You can also browse and search Alfresco directly from within Salesforce.

There are two methods you can use to work with your Alfresco content in Salesforce. If your Salesforce administrator has added the Alfresco app to your Salesforce settings, you can use Alfresco:

1. Directly in a Salesforce record (if the Alfresco app has been added to the record layout)
2. By using the **Alfresco Repository** tab on the Salesforce toolbar. Use this method if you need to associate or link files with Salesforce records.

Salesforce administrators can use this information to install and configure the Salesforce Connector: [Installing and configuring the Salesforce Connector]({% link salesforce/latest/install/index.md %}).

## Working with Alfresco content in a Salesforce record

You can work with your Alfresco files directly from a Salesforce record.

The Alfresco app can be added to any record type that supports layouts (for example; Accounts, Cases, and Opportunities), if it's been added by your Salesforce administrator. You'll see a section containing Alfresco content if the app has been added to the record type. The name of this section depends on what your Salesforce administrator has called it. In this task, we'll call it the Alfresco section.

1. In Salesforce, click the record that you want to work with. For example, this might be a specific account from the **Accounts** tab in Salesforce.
2. In the **Alfresco** section, enter your Alfresco login details. Contact your system administrator if you don't know what your login details are for Alfresco. See [Logging in to Alfresco]({% link content-services/latest/using/share.md %}) for more information.
3. In the **Alfresco** section you can:

    * **Search** for content using the search box.
    * **Create** a new folder or text document in Alfresco.
        Click the name of a folder and it opens in the current Salesforce view. Click a file and it opens a new Alfresco window showing the full details of that file. As you are already logged in to Alfresco, you don't need to enter your Alfresco login details again.
    * Click **Upload** to navigate to content on your device and upload it.
    * **Add** one or more files by dragging and dropping directly into the window. A new window tells you whether each file or folder has been added successfully.

    There's also a breadcrumb trail of folders to help you navigate.

    File actions include **Download**, **View in Browser**, and **Remove Association** if a file or folder has been linked with the record. See [Linking Alfresco content with a Salesforce record](#linkingrecord) for more information about linking content with records.

    >**Note:** You can also delete content that you have created or have permission to delete.

    >**Note:** While you are editing a file, associated files are not visible. After you have checked the file in, any file associations are then shown.

    ![View of Alfresco in a record]({% link salesforce/images/salesforce-record-files.png %})

## Using the Alfresco Repository tab in Salesforce

You can use the **Alfresco Repository** tab to link a file or folder with a record, to add files or folders to Alfresco, and to find content.

1. In Salesforce, click **Alfresco Content Connector**. This is available from the **Force.com** App Menu.

2. Click the **Alfresco Repository** tab.

    Log in to Alfresco. Contact your system administrator if you don't know what your login details are for Alfresco. See [Logging in to Alfresco]({% link content-services/latest/using/share.md %}) for more information.

    An Alfresco view is displayed, with tabs for **Personal Files**, **Repository**, **Sites**, and **Search**.

    ![salesforce-repo-completed]({% link salesforce/images/salesforce-repo-completed.png %})

3. On each tab you can:

    * **Search** for content using the search box.
    * **Create** a new folder or text document in Alfresco.

        Click the name of a folder and it opens in the current Salesforce view. Click a file and it opens a new Alfresco window showing the full details of that file. As you are already logged in to Alfresco, you don't need to enter your Alfresco login details again.

    * Click **Upload** to navigate to content on your device and upload it.
    * **Add** one or more files by dragging and dropping directly into the window. A new window tells you whether each file or folder has been added successfully.

    There's also a breadcrumb trail of folders to help you navigate.

4. On each file or folder you can use the same actions that are available in Alfresco. For example, folder actions include **Download as Zip** and **Delete Folder**.

    There is an additional action, **Associate with Salesforce Record**. This allows you to link a file with a specific record in Salesforce. You can select from a list of recently viewed records. See [Linking Alfresco content with a Salesforce record](#linkingrecord) for more information.

5. **Personal Files** tab: You can add files here that are stored in Alfresco, but are not shared with other users. Any files and folders that you add here are shown in the **Library > Personal Files** folder.

6. **Repository** tab: This is a view of the full Alfresco repository, and is most useful for system administrators. This is the same structure that you see if you click **Repository** from the toolbar in Alfresco.

7. **Sites** tab: This is a list of your Alfresco sites, and the place that most users look for their content. You need to be a member (or creator) of a site for it to be displayed here. If you click a site, it opens the contents into a new tab that has the same name as your site.

    For example, if I am a member of a site called **Salesforce default**, a new tab called **Salesforce default** is displayed where I can see folders and files:

    ![salesforce-sites]({% link salesforce/images/salesforce-sites.png %})

8. **Search** tab: Search in the repository or sites in Alfresco. The search uses the Alfresco faceted search and filtering. The usual Alfresco actions are available for any files or folders that are returned in the search results.

## Linking Alfresco content with a Salesforce record {#linkingrecord}

Use the **Alfresco Repository** tab and **Associate with Salesforce Record** option to associate or link a file with a record in Salesforce.

When you are working with a Salesforce record, there might be marketing, customer-related or other files that you want to store alongside the record. Use this option to link your Alfresco files with your records. When you link a file, the record ID is stored in the parent folder.

1. In Salesforce, click **Alfresco Content Connector**. This is available from the **Force.com** App Menu.

2. Click the **Alfresco Repository** tab.

3. Enter your Alfresco login details. Contact your system administrator if you don't know what your login details are for Alfresco. See [Logging in to Alfresco]({% link content-services/latest/using/share.md %}) for more information.

    An Alfresco view is displayed, with tabs for **Personal Files**, **Repository**, **Sites**, and **Search**.

4. Find the file or folder you require by searching or navigating. Right-click the file, select the record that you want to link from **Most recently used records** and click **+** and **OK** to link the record with the Alfresco content.

    On every file that you see in the **Alfresco** section, you have the option to **Associate with Salesforce Record**. This allows you to link content with a specific record in Salesforce. When you use this action, you can select from a list of recently viewed records to associate with:

    ![salesforce-associate]({% link salesforce/images/salesforce-associate.png %})

    To better identify the record that you require, you can hover over a recently used record to see the Record ID, Record Type and Site that relate to that record.

    ![salesforce-link]({% link salesforce/images/salesforce-link.png %}){:height="18px" width="18px"} denotes that the file is now linked with a record. Also, in the **Alfresco** section of the Salesforce record itself, you'll see the same file is displayed as a linked file.

5. Go to the Salesforce record that you used to link to your Alfresco content.

    In the Alfresco section of the record, you'll see the file is displayed as a linked file.

    ![salesforce-record-files]({% link salesforce/images/salesforce-record-files.png %})

6. Click the folder to open it in Alfresco.
---
title: Surfacing recommended content
---

You can configure a Visualforce Page for one or more Salesforce objects, for example Opportunity or Account, to display a **Recommended Content** panel. The configuration consists of one or more named sections. Each section executes an Alfresco Search Query which can return many results of content items per query. The queries can also be informed by Salesforce field values that can be matched with Alfresco metadata values (content model properties).

A Salesforce user can view the **Recommended Content** panel when creating, viewing, and editing Salesforce objects. The panel will run each of the pre-configured Alfresco Search Queries and display a list of content item results for each named section. Each content item result will initially show the name of the document or file with a clickable link to open the Share document details page.

Starting from version 2.3.4, the Sales Admin can optionally apply the aspect `Recommended Content Link` (`sfdc:recommendedContentLink`) in the **Document Details** page, and then edit the **Properties** to configure where the link should send the Salesforce user. Only one type of link is allowed per document.

The properties for the type of link are:

| Property | Description |
| -------- | ----------- |
| Details | Opens the **Document Details** page in a new tab/window. This is the default behavior if the aspect isn't applied (i.e. the same behavior as in previous releases of the Salesforce Connector). |
| Parent | Opens the parent folder view of the document/folder in a new tab/window. |
| Download | Downloads the content. |
| External | Opens the link provided in the `External link` field in a new tab/window. |
| Record | Opens the Salesforce record provided in the `Record link` field in a new tab/window. |

You must provide additional settings when you select a link type of either `External` or `Record`:

| Property | Description |
| -------- | ----------- |
| External | *Mandatory.* Enter either a relative link (to the parent window) or an absolute link in the `External link` field. If an absolute link is provided, the link must use the `https` protocol. |
| Record | *Mandatory.* Enter the 15 or 18 character Salesforce record Id (alphanumeric) in the `Record link` field. |

> **Note:** Both fields are validated when you click **Save**. You'll get an error message if you enter invalid characters for the URL in the`External link` field, or not enough characters for the Salesforce record Id in the `Record link` field.

## Configuration and setup (Sales Admin)

You can configure a Visualforce Page to run one or more Alfresco Search Queries.

To use the Recommended Content feature, a Visualforce page must be added to your Salesforce organization using the following pattern:

```xml
<apex:page standardController="<Salesforce Object>">
  <apex:canvasApp id="AlfCanvas" applicationName="<The name of your Connected App>" width="100%" height="450px" scrolling="auto" parameters="<A JSON Object the follows the structure documented below>"/>
</apex:page>
```

The structure of the parameters object is:

```json
{'recommended': [
    {'id': 1, 'name': 'Name 1', 'query': 'Alfresco Search Query (afts syntax)' },
    {'id': 2, 'name': 'Name 2', 'query': 'Alfresco Search Query (afts syntax)', maxResults : 10 }
    {'id': 3, 'name': 'Name 3', 'query': 'Alfresco Search Query (afts syntax)', 'sort': [{'field':'cm:name', 'ascending':true}] }, 
    {'id': 2, 'name': 'Name 2', 'query': 'Alfresco Search Query (afts syntax)', 'sort': [{'field':'cm:modified', 'ascending':false}], 'maxResults': 7 }
    ]}
```

The `id`, `name`, and `query` parameters are mandatory. The `sort` and `maxResults` are optional but have pre-defined values if you don't configure them.

In a simple scenario the sales administrator curates the recommended content into two specific folders within Alfresco Content Services. These folders are visible when you create new opportunities in Salesforce. In this case the sales administrator could configure something similar to the following examples, which display two sections by running two Alfresco search queries to list content within two specific parent folders:

**Example 1:**

```xml
<apex:page standardController="Opportunity">
  <apex:canvasApp id="AlfCanvas" applicationName="Alfresco_Salesforce_Connector" width="100%" height="450px" scrolling="auto"

  parameters="{'recommended':[

    {'id': 1, 'name': 'Data Sheets', 'query': 'PARENT:\'workspace://SpacesStore/38745585-816a-403f-8005-0a55c0aec813\' AND TYPE:content'},
    {'id': 2, 'name': 'Competitive Info', 'query': 'PARENT:\'workspace://SpacesStore/8f2105b4-daaf-4874-9e8a-2152569d109b\' AND TYPE:content'}]}"/>
</apex:page>
```

>**Note:** The parent `nodeRef` can be copied from the Share URL when listing a folder. A `path` query could be used instead of a `parent` query but will stop working if the folder is renamed or moved.

**Example 2:**

```xml
<apex:page standardController="Opportunity">
  <apex:canvasApp id="AlfCanvas" applicationName="Alfresco_One_for_Salesforce" width="100%" height="500px" scrolling="auto"

  parameters="{'recommended':[

    {'id':1,'name':'Customer Presentation','query':'(=TS:Solution:\'Content Management\') AND (=TS:SalesMotion:\'Propose Solution\') AND (=TS:MarketingContentType:\'Customer Presentation\')'},
    {'id':2,'name':'Datasheets','query':'(=TS:Solution:\'Content Management\') AND (=TS:SalesMotion:\'Propose Solution\') AND (=TS:MarketingContentType:\'Datasheet\')'},
    {'id':3,'name':'Demo Video','query':'(=TS:Solution:\'Content Management\') AND (=TS:SalesMotion:\'Propose Solution\') AND (=TS:MarketingContentType:\'Demo Video\')'},
    {'id':4,'name':'Training - Technical','query':'(=TS:Solution:\'Content Management\') AND (=TS:SalesMotion:\'Propose Solution\') AND (=TS:MarketingContentType:\'Training- Technical\')'}

  ]}"/>
  
</apex:page>
```

### Simple examples of Alfresco search queries

List content within a parent folder:

```json
{[
  {"id":1,"name":"My 1","query":"PARENT:'workspace://SpacesStore/38745585-816a-403f-8005-0a55c0aec813' AND TYPE:content"}
]}
```

List content with given tag(s):

```json
{[
  {"id":1,"name":"My 1","query":"TAG:'mytag1' AND TYPE:content"},
  {"id":2,"name":"My 2","query":"TAG:'mytag1' AND TAG:'mytag2' TYPE:content"}
]}
```

List content matching specific metadata custom property / properties (example 1):

```json
{[
  {"id":1,"name":"My 1","query":"=myprefix:myprop1:'value x' AND TYPE:content"},
  {"id":2,"name":"My 2","query":"=myprefix:myprop1:'value x' AND =myprefix:myprop2:'value y' AND TYPE:content"}
]}
```

List content matching specific metadata custom property / properties (example 2):

```json
{[
  {"id":1,"name":"Customer Presentation","query":"(=TS:Solution:'Content Management') AND (=TS:SalesMotion:'Propose Solution') AND (=TS:MarketingContentType:'Customer Presentation')"},
  {"id":2,"name":"Datasheets","query":"(=TS:Solution:'Content Management') AND (=TS:SalesMotion:'Propose Solution') AND (=TS:MarketingContentType:'Datasheet')"}
]}
```

>**Note:** For more details related to the syntax of the Alfresco Search Query Language see [Alfresco Full Text Search Reference]({% link search-services/latest/using/index.md %}).

### Advanced examples of Alfresco search queries (informed by Salesforce field values)

The Alfresco Search Query can reference properties from the Salesforce object using the standard Salesforce notation of `{!<Object>.<property>}`. For example `{!Opportunity.Name}` would display the name of the Opportunity record where the Visualforce page is being displayed.

You can use complicated business logic, or reference object properties that don't have a child relationship to the object, through additional Apex code referenced in the `extensions` attribute of the `apex:page` tag.

If a property could have characters that may break the structure of a JSON file they should be wrapped in a [Salesforce JSENCODE formula function](https://help.salesforce.com/articleView?id=customize_functions.htm&type=5){:target="_blank"} i.e. `{!JSENCODE(Opportunity.Name)}`.

Example with Salesforce object field pickvalue (single-valued and mandatory):

```json
{[
  {"id":1,"name":"My 1","query":"=myprefix:myprop1:{!Opportunity.LeadSource}"}
]}
```

Example with Salesforce object field pickvalue (single-valued and optional):

```json
{[
  {"id":1,"name":"My 1","query":"{!IF(ISBLANK(Opportunity.LeadSource),(''),('AND =my:prop:'+Opportunity.LeadSource))}"}
]}
```

>**Note:** In this example, the extra property match is not applied if the field is not set.

### Assumptions and implications

Exact match for values in Salesforce and/or Alfresco drop-downs (list of values).

* Typical example might use:
  * Alfresco custom metadata (content models) with list constraints.
  * Salesforce pickvalues.

* Example with custom Salesforce object fields

  **Prerequisites**

  * custom Alfresco properties: `TS:ProductName` and `TS:Region`
  * custom Opportunity fields: `AlfProductName` and `AlfRegion` (the labels of custom fields in Salesforce are suffixed by `__c`)

  * Opportunity with the **Recommended Content** panel configured with the following queries:

    ```json
    {[
        {'id':1,'name':'Product Name: {!JSENCODE(Opportunity.AlfProductName__c)}  AND  Region: {!JSENCODE(Opportunity.AlfRegion__c)}','query':'(=TS:ProductName:{!JSENCODE(Opportunity.AlfProductName__c)}) AND (=TS:Region:{!JSENCODE(Opportunity.AlfRegion__c)})'},
        {'id':2,'name':'Product Name: {!JSENCODE(Opportunity.AlfProductName__c)}','query':'=TS:ProductName:{!JSENCODE(Opportunity.AlfProductName__c)}'}
    ]}
    ```

    1. Opportunity is configured with `AlfProductName` = `Alfresco Content Services` and `AlfRegion` = `EMEA`:

        ![edit-demo-opportunity]({% link salesforce/images/edit-demo-opportunity.png %})

        Queries results are displayed in the **Recommended Content** panel:

        ![demo-opportunity]({% link salesforce/images/demo-opportunity.png %})

    2. Opportunity is updated with `AlfProductName` = `Alfresco Governance Services`:

        ![editting-demo-opportunity]({% link salesforce/images/editting-demo-opportunity.png %})

        **Recommended Content** panel is dynamically updated:

        ![demo-opportunity2]({% link salesforce/images/demo-opportunity2.png %})

## Surfacing recommended content (Sales Rep)

A Sales Rep creates, views and/or edits a Salesforce object, such as a new Opportunity.

>**Note:** As with the current Salesforce Connector, the Sales Rep needs to login to Alfresco Content Services before they will be able to see the Recommended Content query results. The Sales Rep can login within the Salesforce Connector panel or by using the Alfresco Content Services URL within another browser tab.

### UI Interfaces

As per the current Salesforce Connector its necessary to login to Alfresco Content Services. This is done either in the Salesforce component or in a separate Share tab.

### Viewing recommended content

Lightning UI:

![]({% link salesforce/images/sf-poc-layout-lightning.png %})

Classic UI:

![]({% link salesforce/images/sf-poc-layout-classic.png %})

Once you click on a file in the **Recommended Content** panel, the existing Salesforce Connector Document Details tab will open (by default):

![]({% link salesforce/images/sf-preview-sfdc-document.png %})

Starting from version 2.3.4, once you click on a file in the **Recommended Content** panel, one of the following actions may occur (if configured by the sales administrator):

* Open the **Document Details** page in a new tab/window (this is the default behavior).
* Open the **Document Details** parent folder.
* Download the content.
* Link to an external resource.
* Link to a Salesforce record.

## Lightning configuration and setup

Create a new lightning page with lightning configuration.

1. Go to **Setup > Visualforce** pages:

    ![visualforce-pages]({% link salesforce/images/visualforce-pages.png %})

2. **Create** a new page:

    ![visualforce-pages4]({% link salesforce/images/visualforce-pages4.png %})

3. Go to **Lightning App Builder**:

    ![lightning-app-builder2]({% link salesforce/images/lightning-app-builder2.png %})

4. Select **Record Page** and then click **Next**:

    ![customize-lightning-experience]({% link salesforce/images/customize-lightning-experience.png %})

5. Select **Opportunity** and enter a name for the new lightning page and then click **Next**:

    ![create-new-lightning-page-label]({% link salesforce/images/create-new-lightning-page-label.png %})

6. Select the **layout** you want and click **Finish**:

    ![create-new-lightning-page]({% link salesforce/images/create-new-lightning-page.png %})

7. Select the **section** where you want to insert the component, and then select the **component** from the Visualforce menu on the left:

    ![desired-name-page]({% link salesforce/images/desired-name-page.png %})

8. Go to an **Opportunity** page to see the new view.

    ![visualforce-opportunity]({% link salesforce/images/visualforce-opportunity.png %})

## Classic configuration and setup

Create a new lightning page with classic configuration.

1. Go to **Setup > Visualforce** pages:

    ![visualforce-pages-classic]({% link salesforce/images/visualforce-pages-classic.png %})"

2. **Create** a new page:

    ![visualforce-pages2]({% link salesforce/images/visualforce-pages2.png %})"

3. Go to **Lightning App Builder**:

    ![lightning-app-builder]({% link salesforce/images/lightning-app-builder.png %})"

4. Select **Record Page** and then click **Next**:

    ![customize-lightning-experience]({% link salesforce/images/customize-lightning-experience.png %})"

5. Select **Opportunity** and enter a name for the new lightning page and then click **Next**:

    ![create-new-lightning-page-label]({% link salesforce/images/create-new-lightning-page-label.png %})"

6. Select the **layout** you want and click **Finish**:

    ![create-new-lightning-page]({% link salesforce/images/create-new-lightning-page.png %})"

7. Select the **section** where you want to insert the component, and then select the **component** from the Visualforce menu on the left:

    ![desired-name-page]({% link salesforce/images/desired-name-page.png %})"

8. Go to an **Opportunity** page to see the new view:

    ![visualforce-opportunity]({% link salesforce/images/visualforce-opportunity.png %})"

## Search considerations in Salesforce and Alfresco

Consider how you want to structure your information based on whether you need to restrict access.

There are a number of ways in Salesforce that you can search for content, and the results returned depend on the method.

You can search:

1. In a Salesforce record.

    If you search for information (for example, an account) in a Salesforce record, only accounts that are linked to that particular Salesforce record are returned.  Content might exist in multiple places, but that content is returned only if it is linked with the record.

2. In the Alfresco Repository tab that is displayed in Salesforce.

    If you search for content in the Alfresco Repository tab, all results that you have permission to see are returned from the Alfresco repository. The user can then link the file to one or more Salesforce records.

    If metadata synchronization is enabled, this synchronization happens when a user views a Salesforce record that contains the Alfresco canvas app. The app checks whether a folder for that record exists in Alfresco, and creates a new folder if it does not exist. The app then adds the mapped property values from the Salesforce record to the parent record folder in Alfresco.  If a user searches for that metadata directly in Alfresco (for example, using the Share application), the results are returned successfully.

There is certain content, and associated metadata, that you might want only certain users to see; for example, Human Resources (HR) personnel data. Use a private site for this record type. See [Creating sites]({% link content-services/latest/using/sites/index.md %}#creating-a-site) for more information about the different site types.

You can map an specific object (and therefore all records associated with that object) to a named site in Share. See part 4 of [Step 6: Add the Alfresco app using a Salesforce Lightning Component]({% link salesforce/latest/install/index.md %}#addappusinglightningcomponent) for instructions on how to do this.
---
title: Troubleshoot Salesforce Connector
---

Use this information to troubleshoot common issues when connecting Alfresco to Salesforce.

## Associated document not available

There is a known issue with associating (linking) a document. If you associate a document in Alfresco, and then download and edit the source document offline, the associated document is not available. If you cancel the **Edit Offline** action, the associated document is available.

## Error when trying to configure Alfresco to Salesforce connection

When you configure Alfresco in Salesforce, in the Salesforce **Alfresco Setup** tab, you configure both **Site to Object Mapping** and **Metadata Mapping**. When you first set this up, you should see the Alfresco login screen.

If you see a grey Salesforce box in either of these sections instead of the Alfresco login screen, this is because you have a browser error, which is caused by a self signed certificate not being approved by the browser.

You should also check that your Salesforce and Alfresco instances are on a shared network or otherwise accessible to one another to share information.

## All Salesforce record folders created with a 15- or 18-character ID

There is a known problem if the Alfresco connected app definition in Salesforce has been configured with the wrong lifecycle class. If the lifecycle class is not set to `AlfrescoCanvasLifeCycleHandler`, all record folders in Salesforce are created with IDs that are 15 or 18 characters in length.

Edit the Alfresco connected app definition, as specified in [Step 3: Configure app in Salesforce]({% link salesforce/latest/install/index.md %}#configappinsalesforce-lightning) and ensure that the lifecycle class is set to `AlfrescoCanvasLifeCycleHandler`.

## Alfresco does not start in Salesforce

If you are having problems starting Alfresco in Salesforce, it might be because you have not configured Chatter. Here is a sample error message if Chatter is not enabled:

```bash
GET request for "https://na30.salesforce.com/services/data/v23.0/chatter/users/me" resulted in 403 (Forbidden); invoking error handler
```

Make sure that you have Chatter enabled. To do this, access the **Chatter Settings** page, enter Chatter in the Quick Find box in Salesforce and select Chatter Settings.

## Problems loading Site to a Mapping in Alfresco Setup

If you are having problems with Site to Object Mapping and Metadata Mapping, check your level of Java. If you are running with Java 7, you might see this message:

```text
org.springframework.social.salesforce.api.SalesforceRequestException: TLS 1.0 has been disabled in this organization.
Please use TLS 1.1 or higher when connecting to Salesforce using https.
```

Salesforce requires access to the API using TLS 1.1 or 1.2. You can enable TLS 1.1 and 1.2 in Java 7 using JVM parameters, but they are enabled by default with Java 8. See [Diagnosing TLS, SSL, and HTTPS](https://blogs.oracle.com/java-platform-group/diagnosing-tls,-ssl,-and-https){:target="_blank"} and [JDK 8 will use TLS 1.2 as default](https://blogs.oracle.com/java-platform-group/jdk-8-will-use-tls-12-as-default){:target="_blank"} for more information.

## "Unable to resolve the server's DNS address"

If you see the following message in Salesforce:

```text
Unable to resolve the server's DNS address
```

Then Alfresco is unavailable. Check whether Alfresco is behind a firewall, or whether your Virtual Private Network (VPN) connection has dropped, as both these situations can cause this error.

## "Error rendering Force.com Canvas application"

If you see either of the following messages in Salesforce:

```text
Oops, there was as error rendering Force.com Canvas application [Alfresco_Salesforce_Connector]
```

```text
[Alfresco_for_Salesforce]. Canvas can not locate an installed canvas app with the namespace [] and API name [Alfresco_for_Salesforce].
```

Check whether a connected app definition exists for Alfresco, and that the **API Name** property in the **Alfresco Setup** page has been defined with the correct value. The values in the Alfresco connected app definition and **API Name** must match. See [Step 3: Configure app in Salesforce]({% link salesforce/latest/install/index.md %}#configappinsalesforce-lightning) for more guidance.

## Alfresco connection error when accessing Salesforce content

If you see the following message in Alfresco when you try to access Salesforce content:

```text
Something's wrong with this page...
We may have hit an error or something might have been removed or deleted, so check that the URL is correct.
Alternatively you might not have permission to view the page (it could be on a private site) or there could
have been an internal error. Try checking with your Alfresco administrator.
```

Check that the correct Share URL is specified in the **Canvas App URL** in Salesforce. See [Step 3: Configure app in Salesforce]({% link salesforce/latest/install/index.md %}#configappinsalesforce-lightning) for more guidance.

## HTTP Status 404 or Service Unavailable messages

If you see an `HTTP Status 404` message, `The server refused the connection`, or a `Service Unavailable message`, check that the correct Share URL is specified in the Canvas App URL in Salesforce, and that Alfresco is running. See [Step 3: Configure app in Salesforce]({% link salesforce/latest/install/index.md %}#configappinsalesforce-lightning) for more guidance.

## Edit Offline problems with Apple Safari

If you are using Apple Safari, you might encounter problems when using the **Edit Offline** action. The following message is displayed:

```text
We couldn't load the data.
Try refreshing your screen, or check with your Alfresco Administrator that the server is running.
```

This is caused by an OS X browser problem. To resolve this problem, use a different browser with the **Edit Offline** action.

## Unable to load the Alfresco Content Connector in Salesforce using Firefox

Firefox introduced a new feature called [Tracking Protection](https://support.mozilla.org/en-US/kb/what-happened-tracking-protection){:target="_blank"}, designed to identify and block website trackers. Tracking Protection is enabled by default for private Firefox browsing sessions.

To resolve this issue, disable the Tracking Protection in the Firefox browser settings. Alternatively, use a different browser, such as Chrome or Internet Explorer.

## Comments made outside a site in Alfresco show @@NULL@@ in My Activities dashlet
<!--THIS IS OLD!-->
This is a known issue with Alfresco One 5.0.4 and Alfresco One 5.1.1.

If comments are added to a document outside of a site (including My Files, Shared Files, and Repository) or through the Salesforce Connector, it results in an activity entry that a comment was added, updated, or deleted in a site with the name of `@@NULL@@@`.

## Using the Canvas App Component directly in the Lightning UI

The Canvas app is not correctly configured if you attempt to either:

* Access the App in Salesforce and it opens it in a new Salesforce tab
* Drag and drop a document into the App, which then automatically downloads the document or opens it directly in the browser.

To resolve this issue, remove the canvas app from the Classic UI page layout and follow the instructions to [Set up the App for use in Lightning]({% link salesforce/latest/install/index.md %}#addappusinglightningcomponent).

## "Oops, there was an error rendering Canvas application..."

```text
Oops, there was an error rendering Canvas application [Alfresco_for_Salesforce].Canvas can not locate an installed canvas app with the namespace [] and API name [Alfresco_for_Salesforce].
```

To resolve this, The Canvas app is not correctly configured if you attempt to:

## How do I enable debug logs on both Share and the Repository?

Go to **Log Settings** in the Alfresco Admin Console (`/alfresco/s/enterprise/admin/admin-log-settings`) and add the `org.alfresco.integrations.sfdc.webscripts` package with `DEBUG` level. These changes will persist until the server is shut down or restarted, at which point any changes will be lost.

## Receiving a blank page in Recommended Content Panel.

This can occur when the syntax of the JSON provided in the `parameters` attribute of the `apex:canvasApp` tag in the Visualforce page is incorrect. Review the JSON you are providing in the `parameters` attribute.
