---
title: Alfresco Google Docs Integration
---

Google Docs Integration allows you to use Google Docs to edit document content stored in Alfresco Content Services, as an alternative to the online and offline editing capabilities in Alfresco Share.

To install Google Docs Integration, you need to apply the Google Docs AMP files to enable the feature.

With Google Docs Integration, you'll see new actions for creating documents, spreadsheets, and presentations. Also, you'll see an action called **Edit in Google Docs** on all supported document types.

> **Note**: When configuring Google Docs Integration with Alfresco Content Services, you don't need to identify a 'system' Google account.
---
title: Configure Google Docs Integration
---

There are two ways to configure the Google Docs Integration: modify the properties in `alfresco-global.properties` or update the settings in the **Google Docs Console** of the Admin Console (Enterprise-only).

## Configure using properties

The following properties can be configured for Google Docs Integration in the `alfresco-global.properties` file.

| Property | Description |
| -------- | ----------- |
| googledocs.enabled | *Required.* Enables the Google Docs functionality. By default, this property is set to true. If you set this option to false, the **Edit in Google Docs** action will not be available. Documents that are currently being edited will still be available using the **Resume editing in Google Docs** action until they are saved or discarded. |
| googledocs.idleThresholdSeconds | *Optional.* Sets the idle time threshold in seconds. Additional Google users that you invite to collaborate on the document will be considered to be 'idle' after this period. The period is measured from the time when the user last made a change to the document. When saving documents back to Alfresco Content Services, or discarding changes, you must confirm that you want to disconnect any non-idle users before the action completes. |

## Configure using the Admin Console

The **Google Docs Console** provides the settings for enabling and controlling Google Docs Integration (in Enterprise-only releases). Launch the **Admin Console** by following the steps in [Launch Admin Console]({% link content-services/latest/admin/admin-console.md %}#launch-admin-console).

1. Open the Admin Console.

2. In the Consoles section, click **Google Docs Console**.

3. Set the properties:

    | Property | Description |
    | -------- | ----------- |
    | googledocs.enabled | *Required.* Enables the Google Docs functionality. By default, this property is set to true. If you set this option to false, the **Edit in Google Docs** action will not be available. Documents that are currently being edited will still be available using the **Resume editing in Google Docs** action until they are saved or discarded. |
    | googledocs.idleThresholdSeconds | *Optional.* Sets the idle time threshold in seconds. Additional Google users that you invite to collaborate on the document will be considered to be 'idle' after this period. The period is measured from the time when the user last made a change to the document. When saving documents back to Alfresco Content Services, or discarding changes, you must confirm that you want to disconnect any non-idle users before the action completes. |

4. Click **Save** to apply the changes you have made to the properties.

    If you do not want to save the changes, click **Cancel**.

## Authenticate Google accounts with Alfresco Content Services

In Enterprise-only releases, you can register a custom Google configuration for API access.

> **Note:** This functionality is not available in Alfresco Community Edition releases.

When this configuration is added to the Google Docs Integration, you can define the OAuth flow by creating your own web application configuration in the Google API Manager.

1. Place [google-auth-return.html](https://raw.githubusercontent.com/Alfresco/googledrive/master/google-auth-return.html){:target="_blank"} on a web server that's accessible by all users.

    This file lets users authenticate their Google account with Alfresco Content Services.

2. Register the Google Docs Integration from the Google API Manager: [https://console.developers.google.com](https://console.developers.google.com){:target="_blank"}.

    Check that you have enabled the Google Drive API.

3. Click Library in the left-hand navigation, select **Drive API**, and then **Enable**.

    This allows your registered application to access the Drive API.

4. Click Credentials, select **Create Credentials**, and then pick **OAuth client ID** from the list.

5. Click **Configure consent screen**, complete the required fields, and then select **Save**.

6. Select **Web Application** as the application type.

7. Enter a name for your application.

    This is what the application will be known as in your users Google Account.

8. Enter a path in the **Authorized redirect URIs** field.

    This is the path to the `google-auth-return.html` page.

9. Click **Create**.

    You may be see a popup showing your Client ID and Secret. If so, click **OK**.

10. Navigate to your registered application by selecting the name.

11. Click **Download JSON**.

    Next, use the Repository Administration Console to add your custom configuration.

12. Open the Admin Console.

13. In the Consoles section, click **Google Docs Console**.

14. Copy the content of the JSON file into the **Google Docs OAuth Config** field.

15. Click Save.

    > **Note:** Before completing these steps, be aware that if there are files currently being edited in Google Docs when changing this configuration, it will cause users to lose the ability to use the **Check in** action to bring those files back into Alfresco Content Services. We recommend that all files are checked back into Alfresco Content Services before switching the configuration.

    > **Note:** Switching the integration repeatedly between different configurations can corrupt the Google authentication store in Alfresco Content Services for your users. If this happens, users will need to remove access to the integration from their Google Account so that their connection can be set up again.

    > **Note:** If, while using the Google Docs Integration, when a user is logging into their Google Drive account and they see the message `This App isn't verified, you'll need to upgrade to at least version 4.1.0 of the integration.` Users can click the Advanced link in the message to allow them to continue to the login screen.

## Google Docs supported document types

Google Docs restricts the formats of files or documents that can be uploaded or created.

The following table shows the file format restrictions for content that integrates with Google Docs.

|File type|Description|
|---------|-----------|
|DOC|A Microsoft Word 97-2003 document.|
|XLS|A Microsoft Excel 97-2003 Workbook.|
|PPT|A Microsoft PowerPoint 97-2003 Presentation.|
|DOCX|An XML-based Microsoft Word document.|
|XLSX|An XML-based Microsoft Excel Workbook.|
|PPTX|An XML-based Microsoft PowerPoint presentation.|

> **Note:** You can edit the DOC, XLS, and PPT formats in Google Docs but when you save the content back to Alfresco Content Services, you must confirm that these formats will be converted to the equivalent Microsoft Office 2007 (OOXML) formats.

Google places further restrictions on the size and complexity of documents that can be edited in Google Docs. The **Edit in Google Docs** action is not available for documents or spreadsheets larger than 2 MB and presentations larger than 50 MB. Google also prevents editing of other documents that exceed their published limits. See the published [Google size limits](https://support.google.com/drive/answer/37603?hl=en){:target="_blank"}.
---
title: Install Google Docs Integration
---

Use these steps to install the Google Docs Integration.

1. Download the installation files.

    For Alfresco Content Services, browse to [Hyland Community](https://community.hyland.com/Products/alfresco/release-notes/release-notes/Alfresco-Google-Docs-Integration-Releases/){:target="_blank"}:

    | File | Description |
    | ---- | ----------- |
    | alfresco-googledrive-repo-enterprise-4.1.x.amp |This AMP contains the Google Docs functionality that is applied to the core repository. The AMP should be applied to the `tomcat/webapps/alfresco directory`. |
    | alfresco-googledrive-share-4.1.x.amp | This AMP file contains the additional Google Docs functionality that is applied to an existing Alfresco Share user interface. The AMP should be applied to the `tomcat/webapps/share` directory. |

    For Alfresco Community Edition, you'll need:

    | File | Description |
    | ---- | ----------- |
    | alfresco-googledrive-repo-community-4.1.x.amp | This AMP contains the Google Docs functionality that is applied to the core repository. The AMP should be applied to the `tomcat/webapps/alfresco directory`. |
    | alfresco-googledrive-share-4.1.x.amp | This AMP file contains the additional Google Docs functionality that is applied to an existing Alfresco Share user interface. The AMP should be applied to the `tomcat/webapps/share` directory. |

2. Change into the root of the installation directory (`<installLocation>`). Directories specified in the following procedures are relative to this directory.

3. Move the repository AMP file to the amps directory.

4. Move the Share AMP file to the `amps_share` directory.

5. Stop the server.

6. Delete the `tomcat\webapps\alfresco` and `tomcat\webapps\share` folders in the installation directory.

7. Use the Module Management Tool (MMT) to install the AMP files into the relevant WAR file:

    For the repository:

    ```bash
    java -jar <installLocation>\bin\alfresco-mmt.jar install <installLocation>\amps\alfresco-googledrive-repo-**<version>**.amp <installLocation>\tomcat\webapps\alfresco.war
    ```

    > **Note:** Replace `<version>` with your specific file name.

    * Alfresco Content Services: `alfresco-googledrive-repo-enterprise-4.1.x.amp`
    * Alfresco Community Edition: `alfresco-googledrive-repo-community-4.1.x.amp`

    For Alfresco Share:

    ```bash
    java -jar <installLocation>\bin\alfresco-mmt.jar install <installLocation>\amps_share\alfresco-googledrive-share-**<version>**.amp <installLocation>\tomcat\webapps\share.war
    ```

    > **Note:** Replace `<version>` with your specific file name.

    Alternatively, if your installation is running in the Tomcat application server, you can use the `<installLocation>\bin\apply_amps` command to apply all AMP files that are located in both the amps and `amps_share` directories.

    Install both Google Docs AMP files at the same time by using the `apply_amps` command:

    * Linux: `bin/apply_amps.sh`
    * Windows: `bin\apply_amps.bat`

    The `apply_amps` command checks the version of Alfresco Content Services so that you install the relevant AMP package to the correct version.

8. Start the server.
---
title: Supported platforms
---

The following are the supported platforms for Google Docs Integration:

| Version | Notes |
| ------- | ----- |
| Content Services 23.x | |
| Community Edition 23.x | |
