---
title: Alfresco Collaboration Connector for Microsoft 365
---

Alfresco Collaboration Connector for Microsoft 365 allows you to integrate with Microsoft Office Online applications from the Alfresco Digital Workspace.

Users can edit Microsoft Office documents including Word, Excel and PowerPoint that are stored in Alfresco from the Digital Workspace directly in Office Online.

The following features are available:

* Edit Microsoft Office Word, Excel, and PowerPoint documents stored in Alfresco.
* Share Microsoft Office Word, Excel, and PowerPoint documents with collaborators.
* Co-author Microsoft Office Word, Excel, and PowerPoint documents with collaborators in real-time.
* Create Microsoft Office Word, Excel, and PowerPoint documents.
---
title: Install the Microsoft 365 Connector
---

The Microsoft 365 Connector can be installed using Docker Compose or a distribution zip.

## Prerequisites

There are a number of software requirements for installing the Microsoft 365 Connector:

### Alfresco requirements

* Alfresco Content Services 6.2.2 or later.
* Alfresco Digital Workspace 2.0.0 or later.

See the [Supported Platforms]({% link microsoft-365/latest/support/index.md %}) for more information.

### Microsoft 365 requirements

In order to use the Microsoft 365 Connector, you will need a Microsoft 365 Business, Enterprise or Government subscription plan.

> **Note**: Personal subscription plans are not supported.

It is also required to register a single-page application (SPA) in your organizations Microsoft Azure Active Directory.

## Register a single-page application (SPA)

A single-page application needs to be registered in your Microsoft Azure Active Directory to complete the installation and configuration of the Microsoft 365 Connector.

1. Sign in to the [Microsoft Azure Portal](https://portal.azure.com/){:target="_blank"} as an administrator for your organization.

2. Select the **Azure Active Directory** service, followed by **App registrations** from the side menu and choose to create a **New Registration**.

3. Enter a display name. This will be the user facing display name for the application and will be visible in each user's OneDrive under the **Apps** folder.

    > **Note:** Do not add spaces at the start of the name, otherwise the integration will fail.

4. Select **Accounts in this organizational directory only**.

5. Select **Single-page application SPA** under the **Redirect URI** heading and add a redirect URI using your Content Services HTTPS endpoint, for example `https://<appservername>`.

6. Click **Register**.

    Once you have completed these steps your app registration will have an **Application (client) ID** and a **Directory (tenant) ID** assigned to it.

    > **Note:** These IDs are required when installing and configuring the Digital Workspace.

    ![Azure ID screenshot]({% link microsoft-365/images/azure-ids.png %})

7. Select **API permissions** from the left menu and click **Add a permission** and then select **Microsoft Graph**.

8. Select **Delegated permissions** and search for **Files.ReadWrite.All** in the **Select permissions** search box.

9. Expand **Files** and select **Files.ReadWrite.All** and then click **Add permissions**.
 
10. Select **Grant admin consent for `<your-app-name>`**.

## Install with zip

The Microsoft 365 connector zip file includes all the files required to install the connector.

1. Browse to the [Hyland Community](https://community.hyland.com/customer-portal/5097/downloads/alfresco){:target="_blank"}, download `alfresco-onedrive-integration-2.x.x.zip` and extract the contents:

    * `onedrive-springboot-2.x.x.jar`
    * `alfresco-ooi-content-model.xml`
    * README.md

2. Start the Microsoft 365 connector spring boot app:

    ```java
    java -Dalfresco.base-url=https://<my-alfresco-url> -jar onedrive-springboot-2.x.x.jar
    ```

    Where the `base-url` is the base URL of the Content Services installation in the format `<protocol><domain><port>`. For example, `https://mydomain.com/`

3. Log into Alfresco Share as an administrator and place the `alfresco-ooi-content-model.xml` into the `Data Dictionary/Models` folder. Click **Edit Properties** on the file and check the **Model Active** box.

4. Expose the Microsoft 365 connector service to your proxy, for example using NGINX:

    ```bash
    location /ooi-service/ {
            proxy_pass http://ooi-service:9095;

            # If using an external proxy / load balancer (for initial redirect if no trailing slash)
            absolute_redirect off;  
    ```

5. Configure the Digital Workspace using its `app.config.json` file and set the following properties:

    | Property | Description |
    | -------- | ----------- |
    | microsoftOnline | *Required.* Enable the Microsoft 365 connector plugin by setting the value to `true`. |
    | msonline.msHost | *Required.* The full URL of the Microsoft 365 Connector service, for example `https://<app-server-name>/ooi-service/api/-default-/private/office-integration/versions/1/edit-sessions/`, where `<app-server-name>` is the external web address. |
    | msonline.msClientId | *Required.* The **Application (client) ID** produced when [registering a single-page application](#register-a-single-page-application-spa) in your organization's Microsoft Azure Active Directory. |
    | msonline.msAuthority | *Required.* The **Directory (tenant) ID** produced when [registering a single-page application](#register-a-single-page-application-spa) in your organization's Microsoft Azure Active Directory appended to the Microsoft Online portal address, for example `https://login.microsoftonline.com/ca8490603-2g01-4l8j-8522-fyh4234579f6`. |
    | msonline.msRedirectUri | *Required.* The URL of the Digital Workspace to redirect to. |

    An example of the `app.config.json` is:

    ```json
        "plugins": {
            "microsoftOnline": "true"
        },
        "msOnline": {
            "msHost": "https://<appservername>/ooi-service/api/-default-/private/office-integration/versions/1/edit-sessions/",
            "msClientId": "6548946f3-f7a1-588a-9e68-d595b7b4ul99",
            "msAuthority": "https://login.microsoftonline.com/ca8490603-2g01-4l8j-8522-fyh4234579f6",
            "msRedirectUri": "https://<appservername>"
        },
    ```

6. Save the `app.config.json` and restart all services.

## Install using Docker Compose

Installations using Docker Compose should only be used for development and test environments. To run the Microsoft 365 Connector using Docker Compose, you can either utilize the [Alfresco Content Services download trial]({% link content-services/latest/install/containers/docker-compose.md %}) or use an existing installation of Content Services.

> **Note**: To access the Docker images for the Microsoft 365 Connector, access to [Quay.io](https://quay.io/){:target="_blank"} is required. Alfresco customers can request Quay.io credentials by logging a ticket with [Alfresco Support](https://support.alfresco.com/){:target="_blank"}.

1. Download the Content Services download trial `docker-compose.yml` following the [initial steps]({% link content-services/latest/install/containers/docker-compose.md %}).

2. Edit the `docker-compose.yml` to include the settings for the Microsoft 365 Connector image and update the settings for the Digital Workspace to include the environment variables to run the 365 Connector:

    ```yaml
    ooi-service:
        image: quay.io/alfresco/alfresco-ooi-service:2.0.0
        mem_limit: 768m
        environment:
            JAVA_OPTS: "
              -Xms256m -Xmx512m
              -Dalfresco.base-url=http://alfresco:8080
              "
        ports:
            - 9095:9095

    digital-workspace:
        image: quay.io/alfresco/alfresco-digital-workspace:4.0.0
        mem_limit: 128m
        environment:
            BASE_PATH: ./
            APP_CONFIG_PLUGIN_MICROSOFT_ONLINE: 'true'
            APP_CONFIG_MICROSOFT_ONLINE_OOI_URL: https://<appservername>/ooi-service/api/-default-/private/office-integration/versions/1/edit-sessions/
            APP_CONFIG_MICROSOFT_ONLINE_CLIENTID: <client-id-guid-from-azure-app-registration>
            APP_CONFIG_MICROSOFT_ONLINE_AUTHORITY: https://login.microsoftonline.com/<tenant-id-guid-from-azure-app-registration>
            APP_CONFIG_MICROSOFT_ONLINE_REDIRECT: https://<appservername>
    ```

    | Variable | Description |
    | -------- | ----------- |
    | APP_CONFIG_PLUGIN_MICROSOFT_ONLINE | *Required.* Enable the Microsoft 365 connector plugin by setting the value to `'true'`. |
    | APP_CONFIG_MICROSOFT_ONLINE_OOI_URL | *Required.* The full URL of the Microsoft 365 Connector service, for example `https://<app-server-name>/ooi-service/api/-default-/private/office-integration/versions/1/edit-sessions/`, where `<app-server-name>` is the external web address. |
    | APP_CONFIG_MICROSOFT_ONLINE_CLIENTID | *Required.* The **Application (client) ID** produced when [registering a single-page application](#register-a-single-page-application-spa) in your organization's Microsoft Azure Active Directory. |
    | APP_CONFIG_MICROSOFT_ONLINE_AUTHORITY | *Required.* The **Directory (tenant) ID** produced when [registering a single-page application](#register-a-single-page-application-spa) in your organization's Microsoft Azure Active Directory appended to the Microsoft Online portal address, for example `https://login.microsoftonline.com/ca8490603-2g01-4l8j-8522-fyh4234579f6`. |
    | APP_CONFIG_MICROSOFT_ONLINE_REDIRECT | *Required.* The URL of the Digital Workspace to redirect to. |

3. Expose the Microsoft 365 Connector service to override the default NGINX proxy configuration in the `docker-compose.yml` file:

    Replace:

    ```yaml
    proxy:
        image: alfresco/alfresco-acs-nginx:3.3.0
        mem_limit: 128m
        depends_on:
            - alfresco
            - digital-workspace
            - control-center
        ports:
            - "8080:8080"
        links:
            - digital-workspace
            - alfresco
            - share
            - control-center
    ```

    with:

    ```yaml
    proxy:
        image: nginx:stable-alpine
        mem_limit: 256m
        depends_on:
            - alfresco
            - digital-workspace
            - control-center
        ports:
            - "8080:8080"
        links:
            - digital-workspace
            - alfresco
            - share
            - control-center
            - ooi-service
        volumes:
          - ./nginx.conf:/etc/nginx/nginx.conf
    ```

4. If you want to add an additional location, add the following to your local copy of the `nginx.conf`:

    ```text
    location /ooi-service/ {
                proxy_pass http://ooi-service:9095;

                # If using an external proxy / load balancer (for initial redirect if no trailing slash)
                absolute_redirect off;
            }
    ```

5. Make the folder containing the `docker-compose.yml` your working directory.

6. Sign into Quay.io: `docker login quay.io`.

7. Run the command `docker-compose up` to start the Docker containers.

8. Browse to the [Hyland Community](https://community.hyland.com/customer-portal/5097/downloads/alfresco){:target="_blank"}, download `alfresco-onedrive-integration-2.x.x.zip` and extract the contents.

9. Log into the Digital Workspace as an administrator and place the `alfresco-ooi-content-model.xml` into the `Data Dictionary/Models` folder. View the details of the file, select the **Edit** option and check the **Model Active** box.
---
title: Supported platforms
---

The following are the supported platforms for the Alfresco Collaboration Connector for Microsoft 365 version 2.0.x:

| Version | Notes |
| ------- | ----- |
| Alfresco Content Services 23.x.x | |
| Alfresco Content Services 7.4.x | |
| | |
| **Integrations** | Check the individual documentation on prerequisites and supported platforms for each integration. Check the compatibility of each integration in your installed version of [Alfresco Content Services]({% link content-services/latest/support/index.md %}). |
| Alfresco Digital Workspace | |
---
title: FAQs
---

If you have any problems working with the Microsoft 365 Connector have a look through the list to see if there is a way to resolve your issue.

## What is Microsoft 365?

Microsoft 365 (formerly Office 365) is Microsoft’s subscription-based cloud platform that includes popular Office Online apps like Word, Excel and PowerPoint.

## What are the benefits of integrations into cloud office suites like Microsoft 365?

Office is the de facto productivity suite for most enterprises. Native integration between the Alfresco and Microsoft platforms enhances collaboration, allows users to seamlessly use everyday tools to get work done, and ultimately ensure that important business content is stored in a secure and compliant way in Alfresco.

## Why is it important to follow a ‘single source of truth’ strategy for content storage?

Content sprawl across multiple repositories and business systems is a challenge many organizations face today. Alfresco is an enterprise-class content management system that provides integrations into other business applications so that you avoid creating content silos (such as storing content permanently in Microsoft OneDrive).

## What are the supported Microsoft Office Online xml formats?

The supported Microsoft Office Online xml formats are `docx`, `xlsx`, and `pptx` (Word, Excel, and PowerPoint).

> **Note**: Options to Edit Online will not be available for other file formats, such as `doc`, `xls`, or `ppt`.

## What Microsoft services are being used for the Microsoft 365 connector?

The integration uses Microsoft OneDrive as well as Microsoft Graph API for files.

## What should I expect to see in my Microsoft OneDrive account?

You will see a Microsoft 365 connector folder in your Apps folder, under My files. The folder name may vary depending on the name your Administrator chose when registering the Application.

Documents you edit will appear in date stamped folders. These date stamped folders are used to store a temporary copy of the document you are editing. All edits you make are being made to this temporary copy. You should not open or manage this temporary copy of the document.

Once you finish making edits and save edits back to Alfresco, or discard edits, this temporary copy is deleted in OneDrive and put in the Recycle Bin.

> **Note**: Items deleted to the Recycle Bin are not automatically permanently deleted. We recommend manually deleting files in the Recycle Bin regularly.

## Why am I unable to edit a file in Office Online?

File names that contain special characters such as `# “ %` are unable to open in Office Online. When attempting to edit such files errors will appear in the Console and the file will not open in Office Online.

## Why am I unable to see my edits in the document preview of Digital Workspace?

Document previews in the Digital Workspace are not updating with the latest version of a document through Firefox browsers. Once you re-login into the Digital Workspace, they will see the latest document previews.

## Why do I see a 400 invalid request message from the API?

You may see this error message if there is a leading space in the Application’s display name. Ensure there is no leading space in the Application’s registered display name.

## Why do I see a 400 error message from the API?

You will see this error message if the Office Online content model is not activated. Ensure the `alfresco-ooi-content-model.xml` is deployed and activated.

## Why do I receive a CORS error message from `https://microsoftonline.com`?

You may receive the following error message:

"Access to XMLHttpRequest at `https://login.microsoftonline.com/common/v2.0/oauth2/token` from origin `yourApp.com` has been blocked by CORS policy: No `Access-Control-Allow-Origin` header is present on the requested resource."

This message indicates you have incorrectly selected Web when [registering your single-page application (SPA)]({% link microsoft-365/latest/install/index.md %}#register-a-single-page-application-spa), instead of correctly selecting Single-page application SPA.
---
title: Using the Microsoft 365 Connector
---

The Microsoft 365 Connector can be used to edit, share, co-author, and create documents.

## Edit a document

Files such as Word, Excel and PowerPoint documents that are stored in Alfresco can be edited in Office Online.

1. In the Digital Workspace right click on the file you want to edit.

2. Select **Edit in `<document-type>` Online**, for example `Edit in Excel Online`.

3. You will be prompted to sign into Microsoft Online to open the document in a new browser tab.

    > **Note:** The document will be locked in the Digital Workspace. A padlock icon against the document will indicate this.

4. Once you have finished editing the document, close the browser tab.

    > **Note:** It is recommended to always close the browser tab when you have finished editing a document.

5. Navigate to the Digital Workspace, right click on the document you were editing and select **End Editing**.

6. Set how you would like to handle the changes you made to the document in the **End Editing** window, such as including a comment about the edits that were made. Click **END EDITING** to finish.

7. Your changes will be visible within the Digital Workspace. To preview the changes click on the document name and refresh the Digital Workspace.

## Share a document

Files such as Word, Excel and PowerPoint documents that are stored in Alfresco can be shared with colleagues.

1. In the Digital Workspace right click on the file you want to share.

2. Select **Edit in `<document-type>` Online**, for example `Edit in PowerPoint Online`.

3. You will be prompted to sign into Microsoft Online to open the document in a new browser tab.

    > **Note:** The document will be locked in the Digital Workspace. A padlock icon against the document will indicate this.

4. Click the **Share** button at the top right of the window in the Office document.

5. Click **People in `<your-organization>` with the link can edit** and select the **Allow editing** checkbox followed by **Apply**.

6. Enter the name or email address of who you want to share the document with and click **Send**.

    The collaborator will receive an email that contains a link to the document. Once the collaborator clicks the **Open** button in the email they then login using their Microsoft Online credentials. The collaborator will then have the document opened in Office Online.

## Co-author a document

Files such as Word, Excel and PowerPoint documents that are stored in Alfresco can be edited in real-time with colleagues.

1. Once a document has been [shared](#share-a-document) with another user, the collaborators for the document appear at the top right of the window.

    When you hover over their name you will see a message that says your collaborator has this document open. You will see all edits and changes your collaborators make to your document in real-time.

2. Once a user has finished editing the document, they should close the browser tab.

    > **Note:** It is recommended to always close the browser tab once you have finished making your edits.

3. Navigate to the Digital Workspace, right click on the document that was being edited and select **End Editing**.

4. Set how you would like to handle the changes that were made to the document in the **End Editing** window, such as including a comment about the edits that were made. Click **END EDITING** to finish.

5. The changes will be visible within the Digital Workspace. To preview the changes click on the document name and refresh the Digital Workspace.

## Create a new document

You can create new Word, Excel, and PowerPoint documents that will open online and be stored in Alfresco which can be edited in real-time with colleagues.

1. In the Digital Workspace click **New**.

2. Select the type of document you want to create, either **Word**, **Excel** or **PowerPoint**.

3. Enter a name for the document, and optionally a description and then click **Create and Open Online**.

    > **Note:** If you do not have the 365 Connector installed only the **Create** option will be visible.

4. You will be prompted to sign into Microsoft Online to open the newly created document in a new browser tab.

    > **Note:** The document will be locked in the Digital Workspace. A padlock icon against the document will indicate this.

5. Once you have finished editing the document, close the browser tab.

    > **Note:** It is recommended to always close the browser tab when you have finished editing a document.

6. Navigate to the Digital Workspace, right click on the document you were editing and select **End Editing**.

7. Set how you would like to handle the changes you made to the document in the **End Editing** window, such as including a comment about the edits that were made. Click **END EDITING** to finish.

8. Your changes will be visible within the Digital Workspace. To preview the changes click on the document name and refresh the Digital Workspace.
