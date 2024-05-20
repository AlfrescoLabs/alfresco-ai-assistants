---
title: Alfresco Outlook Integration
---

Alfresco Outlook Integration allows you to use email and repository management without having to leave Microsoft Outlook.

New features introduced in v3.0 are:

* Adds support for Alfresco Content Services 23.1 and 23.2.
* Updates T-Engine to Alfresco Transform Core All-In-One T-Engine 5 (`alfresco-transform-core-aio`).
* Removes legacy configuration for Win Forms - `enableWPF` from `<feature>` section in the client configuration.

Features of Outlook Integration include the ability to archive content (i.e. emails, meetings, appointments, and files) into Alfresco, full metadata support, full search, tagging and workflow capabilities, and the ability to attach files and view archived emails in your inbox. In addition, you can create new versions of existing documents, review the version history of a versioned document, and revert back to previous versions.

>**Note:** In this documentation, the term 'email' is used to refer to emails, meetings, and appointments for the sake of readability.

For information about using the Outlook Integration, see [Using Alfresco from Microsoft Outlook]({% link microsoft-outlook/latest/using/index.md %}).

For information about installing and configuring the Outlook Integration, see [Install and configure Outlook Integration]({% link microsoft-outlook/latest/install/index.md %}).
---
title: Administer Outlook Integration
---

This section contains information related to administration of the Outlook Integration.

## Using SAML SSO with Outlook Integration {#usingsaml}

Use this information to set up SAML Single Sign-On (SSO) authentication for Alfresco Content Services with the Outlook Integration.

> **Note:** With the deprecation of the SAML Module for Alfresco Content Services, the configuration to enable SAML has been moved to Identity Service. Outlook Integration uses the OpenId Connect protocol to manage the authentication against the Identity Service, while the Identity Service handles the SAML-related part depending on the configuration of the SAML provider.

See the [Identity Service documentation]({% link identity-service/latest/tutorial/sso/saml.md %}) for details.

### Prerequisites

* Identity Service needs to be installed and configured to be used with an Alfresco Content Services instance.
* A SAML Identity Provider (IdP) like Active Directory Federation Services (AD FS) needs to be configured for Identity Service:
  * See steps 3 - 5 of the [Identity Service SAML guide]({% link identity-service/latest/tutorial/sso/saml.md %}).
* Outlook Integration needs to be able to reach the Identity Service and the SAML IdP to handle authentication.

Once you've installed the Outlook client and completed the configuration, you should see the OIDC authentication radio button in the Outlook plugin
configuration.

To see this option, open Microsoft Outlook, and in the **Alfresco Client** tab select **Configure** to view the client configuration:

![Alfresco client configuration in Outlook]({% link microsoft-outlook/images/2-10-Outlook-connection-saml.png %})

## Configuration in Identity Service

### Valid Redirect URIs

The OpenId Connect authentication in Outlook Integration uses an embedded browser in combination with the `authorization_code` grant type to authenticate the user against the Identity Service. Extracting the authentication tokens is done within the embedded browser while the redirect happens. As the token extraction is happening within the embedded browser, Outlook Integration does not need to open a web server or a listener on a specific port. It requires an arbitrary URL the Outlook client can be redirected to by the Identity Service after a successful login.

As per the default configuration, a specific loopback address `https://127.0.0.1:6543/OutlookCallback` is defined. This address must be added in the Identity Service - **Valid Redirect URIs** section for the OpenId Connect client that is used.

You can change the redirect URI, if needed. It just needs to match the valid redirect URIs.

### Refresh Tokens

Outlook integration relies on refresh tokens from the Identity Service to automatically retrieve new AccessToken/RefreshToken pairs while Outlook is open. This reduces the number of times for a re-authentication against the SAML IdP.

To ensure this works, the configured OpenId Connect client must provide refresh tokens with the authentication response. To do this, set the following configuration parameters in the Identity Service.

### (Optional) Set up an OpenId Connect Client for Outlook Integration

1. Create a new OpenId Connect client for the realm that is used:
   1. Client authentication: `Off`.
   2. Authorization: `Off`.
   3. Authentication flow: enable `Standard flow`.
2. Specify a valid redirect URI.

> **Note:** Although this step is optional, it is possible to use the default Alfresco client. Setting up a specific OpenId Connect client for Outlook is the preferred way.

Make sure the client specific settings match the server-side configuration.

## Configuration in Alfresco Outlook Integration

The Outlook clients initiates the authentication process directly against the Identity Service server. Therefore, you must configure the IDS configuration parameters on the client-side to match the system environment:

* Authentication Server URL
* Realm
* Client ID
* Redirect URL

Details about the configuration parameters are in the [configuration]{% link microsoft-outlook/latest/config/index.md %} page.

> **Note:** To allow the use of the SAML provider without additional user interaction, you must force the use of the SAML provider. See [Identity Service documentation]({% link identity-service/latest/tutorial/sso/saml.md %}#step-5-optional-enforcing-saml) for
details.

## Single Sign-On (SSO)

SSO requires that the SAML IdP and the environment is set up properly. If SSO is not working and a form-based authentication dialog is shown, you may need to extend the list of allowed agents for Windows Integration Authentication on the Active Directory Federation Services side with `Trident/7.0`.
---
title: Configure Outlook Integration
---

Configure Outlook settings in Alfresco Share using the Share Admin Tools menu, in Microsoft Outlook using the Alfresco Client toolbar, or by editing configuration files directly.

In Alfresco Share, as an administrator, click **Admin Tools** on the Alfresco toolbar. In the left **Tools** panel, scroll down and under **Outlook Integration** there are the following options for configuration:

* *Metadata Settings* - custom metadata and list view settings
* *Search Settings* - custom simple and advanced search settings
* *Integration Settings* - server and client setup, upload restrictions and email settings
* *Access Tokens* - view and remove active users
* *Licenses* - view and register server and client licenses
* *System Info* - view version, license, server and installed module information

The URL is:

```html
http://localhost:8080/share/page/console/admin-console/mail-customization-config
```

where `localhost:8080` is your Alfresco server and port number.

On the Microsoft Outlook toolbar, there is an Alfresco Client tab, with the following entries:

![Alfresco Outlook Client ribbon in Outlook]({% link microsoft-outlook/images/2-8-ribbon-top.png %}){:width="600px"}

* *Configure* - client configuration and license
* *Language* - client display language
* *Show Sidebar* - show the Alfresco repository window
* *Send and Archive* - automatically archive email after sending
* *Message Details* - displays details of a selected archived email
* *Help* - link to Alfresco Outlook Client documentation
* *Info* - version and copyright information

>**Note:** Not all settings can be configured using the Alfresco Client toolbar.

## Alfresco Share configuration

This section contains Alfresco Share configuration instructions for the Outlook Integration.

### Configure metadata and list view settings {#configmetadataandlistview}

You can configure metadata and list view settings for the Outlook Integration using Share **Admin Tools**. These settings define global controls across your enterprise and are applied immediately.

1. Open Alfresco Share, and click **Admin Tools** on the toolbar.

2. Click **Metadata Settings** and **Edit**.

    See [Outlook metadata settings](#detailedconfigmetadatasettings) for more detailed guidance on adding metadata.

3. Check the box to **Enable custom metadata support** in the relevant custom metadata section.

    If you select this option, the **Configuration XML content** field becomes active.

4. Paste the XML code that contains the configuration settings for the Alfresco Outlook Client into the **Configuration XML content** field, or load and edit the default configuration template by clicking **Load default configuration template**.

    You can use the default configuration template for testing purposes, and edit this if you prefer.

5. In the list view section, **Allow overwriting** is enabled by default. Uncheck to set global list view settings for Outlook.

    This means that users are able to change their settings locally.

6. Edit the XML settings in the third **Configuration XML content** field or use your own settings. The default configuration template is preloaded.

7. Click **Apply** to save.

    If your XML isn't valid, you won't be allowed to save your settings, and you'll see an error message.

8. You can download the list view settings locally by clicking **Download configuration**.

#### Detailed config of metadata settings {#detailedconfigmetadatasettings}

Use this guidance to configure templates for adding metadata to folders, files, emails and attachments in Outlook.

You can configure the fields and validation rules that are used when a user drags and drops an email into the
Alfresco sidebar in Outlook. This configuration supports content models, including data types, constraints, lists, regular expressions and other attributes. You can also configure the columns shown in the list view depending on the navigation location of a user. This configuration applies to the current view of the folder's documents, emails, and sub-folders as well as the search results.

When a user stores an email, attachment or file, the Outlook Integration finds the best match for the metadata dialog. The `<match>` element uses the first rule that matches the attributes in the tag. If you are using multiple rules, you should always start with the most specific rule first.

In the `<match>` element:

1. Define the match type. This can be a folder, type or aspect.

2. Define the match pattern. This can be the location of the folder (defined in xpath format), or it can be based on a defined model, type, or aspect. When using a folder location for the metadata, you can use the asterisk wildcard (`*`) - an example is shown in step **21**.

See step **11** for the complete example of metadata settings.

1. Open Alfresco Share, and click **Admin Tools** on the toolbar.

2. Click **Metadata Settings**, then **Edit**.

    You can configure XML settings for **Custom content metadata**, **Custom folder metadata** and **List view**.

3. Check **Enable custom metadata support** to activate the required **Configuration XML content** field.

    The **List view** field for **Configuration XML content** is activated and populated with XML content by default.

4. You can load and edit the default configuration template for each section by clicking **Load default configuration template**.

    Here is the full list of metadata settings that you can configure, with examples shown in the next steps:

    |Section name|Key name|Description|Values|
    |------------|--------|-----------|------|
    |`match`|`type`|Mandatory. Defines type of the attribute|`folder`, `type`, `aspect`|
    | |`pattern`|Mandatory. Path to the site or folder where custom metadata is applied|Example:<br><br>Site: `pattern="/app: company_home/st:sites/cm:qaext- standard-metadata"`<br><br>Folder: `pattern="/app: company_home/st:sites/cm:qaext- custom-metadata/cm: documentLibrary/cm:numericmetadata"`|
    | |`showEmailDialog`|Controls metadata dialog behavior|`true`: metadata dialog displayed (default)<br><br>`false`: metadata dialog not displayed|
    | |`showDocumentDialog`|Controls metadata dialog behavior|`true`: metadata dialog displayed (default)<br><br>`false`: metadata dialog not displayed|
    |`target`|`useTags`|Controls use of tags|`true`: tags are permitted<br><br>`false`: tags are not permitted|
    | |`emlType`|Type of .EML files| |
    | |`msgType`|Type of .MSG files| |
    | |`attachmentType`|Type of attachments| |
    | |`docType`|Type of documents| |
    | |`schemaID`|Schema ID|Example: <br><br>`c9379665`: Cryptic ID specified by server<br><br>`TEST-FOLDER-SCHEMA-ID`: Custom schema ID|
    | |`default`|Default metadata scheme to display|`true`|
    |`property`|`name`|Name of the custom property|Text format|
    | |`allowedValues`|List of permitted values|Text format|
    | |`allowedCategoryValues`|Path to the list of permitted values|Text format|
    | |`defaultValue`|Default value to display|Text format|
    |`ui`|`multiline`|Controls use of multiple lines in a box|`true`: multiple lines are permitted<br><br>`false`: multiple lines are not permitted|
    | |`validationMsg`|Defines validation message| |
    | |`editable`|Controls if a field is editable|`true`: field is editable<br><br>`false`: field is read-only|

5. To turn off the metadata dialog completely, use this example:

    ```xml
    <match type="folder" pattern="/app:company_home/st:sites/cm:myexample-1-site-no-metadata">
    </match>
    ```

    This rule turns off the metadata dialog for all folders under the site `my-example-1-site-no-metadata`.

6. To enable a Tags field only in the metadata dialog, use this example:

    ```xml
    <match type="folder" pattern="/app:company_home/st:sites/cm:myexample-2-site-only-tags" >
        <target useTags="true" emlType="wpsmail-qa-ext:custom-eml" msgType="wpsmail-qa-ext:custom-msg" attachmentType="wpsmail-qaext:custom-attachment">
        </target>
    </match>
    ```

    In this example, the only available child element is `<target>`. In `<target>` you can specify `useTags`, `emlType`, `msgType`, and `attachmentType` as attributes. If you set the attributes `emlType`, `msgType`, or `attachmentType`, you can assign your own custom type to the uploaded EML, MSG, or attached object. The server automatically creates the corresponding nodes with the correct type during the upload. In the example shown:

    * The Tags metadata dialog is enabled (`useTags="true"`)
    * Automatic type conversion takes place during upload:
        * For EML files, the node type is set to the `wpsmail-qa-ext:custom-eml`
        * For MSG files, the node type is set to the `wpsmail-qa-ext:custom-msg`
        * For email attachments, the node type is set to the `wpsmail-qa-ext:custom-attachment`

    If no type information is present, the default `cm:content` type is used for all nodes stored in Share. The `<target>` element can contain 0 or more child elements called `<property>`.

    In the `<property>` tag:

    * Use the `name` attribute to set a valid model property like `cm:name`
    * Use the `<ui>` child element to control how the fields are displayed in the metadata dialog

7. To add standard metadata fields to the metadata dialog, use this example:

    ```xml
    <match type="folder" pattern="/app:company_home/st:sites/cm:myexample-3-site-standard-metadata" >
       <target>
          <property name="cm:title" />
          <property name="cm:description">
            <ui multiline="true"/>
          </property>
       </target>
    </match>
    ```

    In this example, the user sees a metadata dialog with two fields; one for `cm:title` and one for `cm:description` when they upload files to the `my-example-3-site-standard-metadata` site.

    The `cm:description` field can contain multiple lines by setting `<ui multiline="true"/>`.

8. To add numeric, date/time and boolean metadata fields to the metadata dialog, use this example:

    ```xml
    <match type="folder" pattern="/app:company_home/st:sites/cm:myexample-4-site/cm:documentLibrary/cm:numeric-metadata-date" >
       <target>
         <property name="wpsmail-qa-ext:number-metadata-float" />
         <property name="wpsmail-qa-ext:number-metadata-double" />
         <property name="wpsmail-qa-ext:number-metadata-int" />
         <property name="wpsmail-qa-ext:number-metadata-long" />
         <hr/>
         <property name="wpsmail-qa-ext:various-metadata-date" />
         <property name="wpsmail-qa-ext:various-metadata-datetime" />
         <property name="wpsmail-qa-ext:various-metadata-boolean" />
       </target>
    </match>
    ```

    In this example, the user sees a metadata dialog for all files uploaded to the `numeric-metadata-date` folder (or its sub folders) on the `myexample-4-site` site. The dialog will contain four fields with custom numeric data in float, double, int and long format.

    The `<hr/>` element adds a horizontal line to the metadata dialog.

    Three additional fields are available; a date field and a date time field (both displayed using a calendar widget), and a boolean field (displayed using a radio button widget).

9. To add list constraint fields to the metadata dialog, use this example:

    ```xml
    <match type="folder" pattern="/app:company_home/st:sites/cm:myexample-5-site/cm:documentLibrary/cm:list-metadata" >
       <target>
         <property name="wpsmail-qa-ext:list-metadata-country-text" allowedCategoryValues="cm:categoryRoot/cm:generalclassifiable/cm:Regions/cm:EUROPE/cm:Northern_x0020_Europe" />
         <property name="wpsmail-qa-ext:list-metadata-languagetext" allowedCategoryValues="cm:categoryRoot/cm:generalclassifiable/cm:Languages" />
         <property name="wpsmail-qa-ext:list-metadata-greekalphabet-text" defaultValue="Iota" allowedValues="/app:company_home/app:dictionary/cm:wps_alfresco_mail_integration_ext_constraints/cm:ext-categorylist-greek-alphabet.txt" />
         <property name="wpsmail-qa-ext:list-metadata-arabicnumerals-int" allowedValues="/app:company_home/app:dictionary/cm:wps_alfresco_mail_integration_ext_constraints/cm:ext-categorylist-arabic-numerals.txt" />
         <property name="wpsmail-qa-ext:list-metadata-romannumerals-text" allowedValues="/app:company_home/app:dictionary/cm:wps_alfresco_mail_integration_ext_constraints/cm:ext-categorylist-roman-numerals.txt" />
         <property name="wpsmail-qa-ext:list-metadata-vegetabletext" />
       </target>
    </match>
    ```

    There are three ways to define list constraints in the metadata dialog. You can reference:

    * A category root
    * A text file with a number of list entries
    * A property that has a LIST constraint in the model

    In this example, when a file is uploaded to the `list-metadata` folder on the `my-example-5-site` site, the metadata dialog shows six different fields. The field with the attribute name `wpsmail-qa-ext:list-metadata-country-text` shows only categories that are located in `cm:categoryRoot/cm:generalclassifiable/cm:Regions/cm:EUROPE/cm:Northern_x0020_Europe`.

    You can also define your own value list and save it as a text file in Share. Reference the location of your list file in the `allowedValues` attribute. Set a default value from your value list in the `defaultValue` attribute.

    >**Note:** You can use `defaultValue` to set the default value of text fields, checkboxes, and other fields. It's not limited to working in combination with lists.

    In the example, the `wpsmail-qa-ext:list-metadata-greek-alphabet-text` attribute references `/app:company_home/app:dictionary/cm:wps_alfresco_mail_integration_ext_constraints/cm:ext-category-list-greek-alphabet.txt` in the `allowedValues` attribute. The metadata dialog fills in the value `Iota` as a default value.

10. To add type mapping fields to the metadata dialog, use this example:

    ```xml
    <match type="type" pattern="wpsmail-qa-ext:invoice-type-folder" >
       <target>
         <property name="wpsmail-qa-ext:invoice-number" />
         <property name="wpsmail-qa-ext:invoice-amount" />
       </target>
    </match>
    ```

    The match type is defined in the model as `wpsmail-qa-ext:invoice-type-folder`. Every time a file is uploaded to a folder with the type `wpsmail-qa-ext:invoice-type-folder`, the metadata dialog displays two fields with custom metadata. In this example, these fields are `wpsmail-qa-ext:invoice-number` and `wpsmail-qa-ext:invoice-amount`.

11. To add aspect mapping fields to the metadata dialog, use this example:

    ```xml
    <match type="aspect" pattern="wpsmail-qa-ext:claims-aspect-folder" >
       <target>
         <property name="wpsmail-qa-ext:claims-value" />
       </target>
    </match>
    ```

    The matching aspect is defined in the model as `wpsmail-qa-ext:claims-aspect-folder`. Every time a file is uploaded to a folder with the type `wpsmail-qa-ext:claims-aspect-folder`, the metadata dialog displays one field with custom metadata. In this example, this field is `wpsmail-qa-ext:claims-value`.

    Here is a complete example of metadata settings:

    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <metadata>
        <!-- For "No metadata" Site -->
        <match type="folder" pattern="/app:company_home/st:sites/cm:qa-ext-no-metadata" >
          <!-- No configuration -->
        </match>
        <!-- For "Standard metadata" Site -->
        <match type="folder" pattern="/app:company_home/st:sites/cm:qa-ext-standard-metadata" >
           <target useTags="true" emlType="wpsmail-qa-ext:custom-eml"msgType="wpsmail-qa-ext:custom-msg" attachmentType="wpsmail-qaext:custom-attachment">
              <property name="cm:title" />
              <hr/>
              <property name="cm:description">
                  <ui multiline="true"/>
              </property>
           </target>
        </match>
        <!-- For "Numeric Metadata" folder of "Custom metadata" Site -->
        <match type="folder" pattern="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:numeric-metadata" >
           <target>
              <property name="wpsmail-qa-ext:number-metadata-float" />
              <property name="wpsmail-qa-ext:number-metadata-double" />
              <property name="wpsmail-qa-ext:number-metadata-int" />
              <property name="wpsmail-qa-ext:number-metadata-long" />
           </target>
        </match>
        <!-- For "List Metadata" folder of "Custom metadata" Site -->
        <match type="folder" pattern="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:list-metadata" >
           <target>
              <property name="wpsmail-qa-ext:list-metadata-countrytext" allowedCategoryValues="cm:categoryRoot/cm:generalclassifiable/cm:Regions/cm:EUROPE/cm:Northern_x0020_Europe" />
              <property name="wpsmail-qa-ext:list-metadata-languagetext" allowedCategoryValues="cm:categoryRoot/cm:generalclassifiable/cm:Languages" />
              <property name="wpsmail-qa-ext:list-metadata-greekalphabet-text" defaultValue="Iota" allowedValues="/app:company_home/app:dictionary/cm:wps_alfresco_mail_integration_ext_constraints/cm:ext-categorylist-greek-alphabet.txt" />
              <property name="wpsmail-qa-ext:list-metadata-arabicnumerals-int" allowedValues="/app:company_home/app:dictionary/cm:wps_alfresco_mail_integration_ext_constraints/cm:ext-categorylist-arabic-numerals.txt" />
              <property name="wpsmail-qa-ext:list-metadata-romannumerals-text" allowedValues="/app:company_home/app:dictionary/cm:wps_alfresco_mail_integration_ext_constraints/cm:ext-categorylist-roman-numerals.txt" />
              <property name="wpsmail-qa-ext:list-metadatavegetable-text" />
          </target>
        </match>
        <!-- For "Text Metadata" folder of "Custom metadata" Site -->
        <match type="folder" pattern="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:text-metadata" >
           <target>
              <property name="wpsmail-qa-ext:text-metadata-numbertext" />
              <property name="wpsmail-qa-ext:text-metadata-notnumber-ml-text" />
           </target>
         </match>
         <!-- For "Various Metadata" folder of "Custom metadata" Site -->
        <match type="folder" pattern="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:various-metadata" >
          <target emlType="wpsmail-qa-ext:custom-eml" msgType="wpsmail-qa-ext:custom-msg" attachmentType="wpsmail-qa-ext:customattachment">
             <property name="wpsmail-qa-ext:various-metadata-date" />
             <property name="wpsmail-qa-ext:various-metadatadatetime" />
             <property name="wpsmail-qa-ext:various-metadataboolean" />
          </target>
        </match>
        <!-- For "Standard Metadata" folder of "Custom metadata" Site-->
        <match type="folder" pattern="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:standard-metadata" >
           <target useTags="true" >
              <property name="cm:title" />
              <property name="cm:description" />
           </target>
        </match>
        <!-- For "No Metadata" folder of "Custom metadata" Site -->
        <match type="folder" pattern="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:no-metadata" >
           <!-- No configuration -->
        </match>
        <!-- For "Invoice Type" folder of "Custom metadata" Site -->
        <match type="type" pattern="wpsmail-qa-ext:invoice-typefolder" >
           <target>
              <property name="wpsmail-qa-ext:invoice-number" />
              <property name="wpsmail-qa-ext:vendor-name" allowedValues="/app:company_home/app:dictionary/cm:alfresco_mail_integration_ext_constraints/cm:ext-categorylist-greek-alphabet.txt" />
              <property name="wpsmail-qa-ext:invoice-amount" />
           </target>
        </match>
        <!-- For "Claims Aspect" folder of "Custom metadata" Site -->
        <match type="aspect" pattern="wpsmail-qa-ext:claims-aspectfolder" >
           <target>
              <property name="wpsmail-qa-ext:claims-value" />
              <property name="wpsmail-qa-ext:claims-type" allowedCategoryValues="cm:categoryRoot/cm:generalclassifiable/cm:Software_x0020_Document_x0020_Classification" />
           </target>
        </match>
    </metadata>
    ```

12. To automatically populate predefined metadata, use this example:

    We are defining two properties for automatic population, called `source` and `source-type`:

    ```xml
    <aspect name="wpsmail-qa-ext:source-aspect">
      <title>WPS Source Aspect</title>
       <properties>
         <property name="wpsmail-qa-ext:source">
            <title>Source</title>
            <type>d:text</type>
         </property>
       </properties>
    </aspect>
    <aspect name="wpsmail-qa-ext:source-type-aspect">
      <title>WPS Source Type Aspect</title>
       <properties>
         <property name="wpsmail-qa-ext:source-type">
           <title>Source Type</title>
           <type>d:int</type>
         </property>
       </properties>
    </aspect>
    ```

    `source` is set to Outlook, and `source-type` is set to 123:

    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <metadata>
       <extended>
         <autofill>
            <property name="wpsmail-qa-ext:source" value="Outlook" />
            <property name="wpsmail-qa-ext:source-type" value="123" />
         </autofill>
       </extended>
    </metadata>
    ```

13. To set the type (`docType`) for all files that are dragged and dropped into Share, use this example:

    We are setting the type of incoming files to `gsliu:uwdoc`:

    ```xml
    <match type="folder" pattern="/app:company_home/st:sites/cm:gsliu-3rd-party" >
      <target useTags="false" attachmentType="gsliu:uwdoc" msgType="gsliu:uwdoc" emlType="gsliu:uwdoc"
    docType="gsliu:uwdoc">
        <property name="gsliu:category_name" allowedValues="app:company_home/app:dictionary/cm:
    WPS_x0020_Alfresco_x0020_Mail_x0020_Integration_x0020_LM_x0020_Constraints/cm:lm-category-list-constraint-1stparty.txt">
          <ui multiline="false" />
        </property>
      </target>
    </match>
    ```

    The `emlType`, `msgType` and `attachmentType` attributes are relevant when a user moves emails to the content repository:

    * `emlType` defines the type of the eml object that represents the email in the document library.
    * `msgType` defines the type of the original MSG file that is stored in a hidden folder and linked to the email (if the option **Store original MSG** is enabled).
    * `attachmentType` defines the type of the attachments that are extracted from the email. The objects are stored in a hidden folder and linked to the email.

    The `docType` attribute is relevant when a user moves documents to the repository. This happens when a user:

    * Drags and drops a document from the desktop to the Alfresco sidebar in Outlook
    * Drags and drops a document that is listed as an email attachment to the Alfresco sidebar in Outlook

    >**Note:** Make sure that you set `docType` to ensure that the custom type is inherited.

14. To provide multiple content metadata options in the metadata dialog, use this example:

    ```xml
    <match pattern="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:various-metadata"
    type="folder">
        <target name="No Metadata" schemaId="99ef8057" />
        <target attachmentType="wpsmail-qa-ext:custom-attachment" default="true"
    docType="wpsmail-qa-ext:custom-document" emlType="wpsmail-qa-ext:custom-eml" msgType="wpsmail-qa-ext:custom-msg"
    name="Various Metadata" schemaId="c9379665">
            <property name="wpsmail-qa-ext:various-metadata-date"/>
            <property name="wpsmail-qa-ext:various-metadata-datetime"/>
            <property name="wpsmail-qa-ext:various-metadata-boolean"/>
        </target>
    </match>
    ```

    This rule allows you to add multiple `target` elements to configure different sets of content metadata fields that are presented to the user when they upload new content. This is useful when users want to upload different types of content in one particular folder, and so you can assign different sets of metedata depending on the type of content.

    For users to be able to distinguish between multiple metadata schemes, assign meaningful names to the `<target>` elements by using the `name` attribute. If there are multiple `<target>` elements defined for one location, you can set a default by defining the attribute `default="true"`. This is shown by default to users in the metadata scheme field.

    The `schemaID` attribute allows multiple `target` elements to be defined in a `<match>` section. In this example, the server adds a cryptic schemaID such as `schemaId="c9379665"`. You can assign a meaningful schemaID, such as `TEST-SCHEMA-ID`, instead of keeping the server generated one.

    >**Note:** Once a user has uploaded content into a location where a `schemaID` is configured, this ID shouldn't be changed, otherwise the Alfresco Outlook Client won’t find the metadata assigned to that content.

15. To define a custom validation message in the metadata dialog, use this example:

    ```xml
    <property name="wpsmail-test:test-aspect-for-metadata-date">
        <ui validationMsg="MM/DD/YYYY"/>
    </property>
    ```

    In this example, the validation message for the date property is shown as `MM/DD/YYYY`. This message is displayed to the user as a guideline of what values a particular field can take.

    This attribute can contain either a direct message, as in the example above, or a reference to message bundle key.

    If the attribute contains a reference to a property key that is available in a properties resource bundle in your system, the scheme name can be localized: `validationMsg="com.company.outlook.validationMsg.1.name"`

16. To define a metadata field as read-only, use this example:

    ```xml
    <property name="wpsmail-test:test-aspect-for-metadata-boolean">
        <ui editable="false"/>
    </property>
    ```

    In this example, the boolean field is presented as a read-only field.

17. To provide multiple folder metadata options when users create and update folders, use this example:

    ```xml
    <match pattern="/app:company_home" type="folder">
        <target name="No Metadata" schemaId="99ef8057" />
        <target folderType="cm:folder" name="Payload Target" schemaId="TEST-FOLDER-SCHEMA-ID" useTags="true">
            <property name="wpsmail-test:test-aspect-for-metadata-date">
                <ui validationMsg="MM/DD/YYYY"/>
            </property>
        </target>
    </match>
    ```

    The custom metadata for folders is enabled by selecting the checkbox in the **Custom folder metadata** configuration field.

    This rule allows you to add multiple `target` elements to configure different sets of folder metadata fields that are presented to the user when they create new folders or edit the metadata. This is useful when users want to upload different types of folders in one particular location, and so you can assign different sets of metedata depending on the type of folder.

    For users to be able to distinguish between multiple metadata schemes, assign meaningful names to the `<target>` elements by using the `name` attribute. If there are multiple `<target>` elements defined for one location, you can set a default by defining the attribute `default="true"`. You can also add a custom validation message to a field, and set a field to read-only, similar to configuring custom content metadata.

18. To customize the behavior of the metadata dialog for all files that are dragged and dropped into Alfresco Outlook Client, use this example:

    ```xml
    <match pattern="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:various-metadata" type="folder" showEmailDialog="false" showDocumentDialog="true">
        ...
    </match>
    ```

    The `showEmailDialog`, and `showDocumentDialog` attributes allow you to control what happens when a user moves emails or other documents into Alfresco:

    * `showEmailDialog` defines if the metadata dialog opens when a user drags and drops an email object, with or without attachments, into the Alfresco Outlook Client.
    * `showDocumentDialog` defines if the metadata dialog opens when a user drags and drops an email attachment document or other document from the desktop into the content repository.

    If both attributes are set to `false`, the metadata dialog is not shown when emails or documents are either dragged and dropped or archived directly.

19. To configure the list view displayed at a specific navigation location, use this example:

    ```xml
    <match pattern="/app:company_home/st:sites/cm:qa-ext-custom-metadata/
    cm:documentLibrary/cm:numeric-metadata" name="numericmetadata">
        <declare>
            <special-column name="type" width="40" />
            <special-column name="name" width="160" />
            <property-column name="wpsmail-qa-ext:number-metadata-float" width="80"/>
            <property-column name="wpsmail-qa-ext:number-metadata-double" width="80"/>
            <property-column name="wpsmail-qa-ext:number-metadata-int" width="80"/>
            <property-column name="wpsmail-qa-ext:number-metadata-long" width="80"/>
        </declare>
        <visible>
            <special-column name="type" />
            <special-column name="name" />
            <property-column name="wpsmail-qa-ext:number-metadata-float"/>
            <property-column name="wpsmail-qa-ext:number-metadata-double"/>
            <property-column name="wpsmail-qa-ext:number-metadata-int"/>
            <property-column name="wpsmail-qa-ext:number-metadata-long"/>
        </visible>
    </match>
    ```

    This rule allows you to deviate from the default column settings when the Alfresco Outlook Client presents content in the specified `numeric-metadata` folder (and its sub folders) on the `qa-ext-custom-metadata` site. The `<match>` rule is added into an `<overrides>` section of the XML configuration. In this example, when a user navigates to this location or starts a search in this location, an alternative list view is presented. The dialog shows four fields with custom numeric data in float, double, int, and long format.

    Instead of using a folder, the `<match>` tag can be used with an aspect, for example:

    ```xml
    <match pattern="cm:aspectName" type="aspect" name="myListSettingsForAnAspect">
    ```

    If no `type` is given, the pattern will be treated as a folder.

    Note how the rule is similar to the custom content metadata configuration. The `<list-view>` and `<match>` elements can be assigned names, which will be displayed in the list view configuration of the Alfresco Outlook Client. The user can still define which columns of a particular server-side list view configuration are enabled/disabled.

20. To provide users with the capability to rename the email subject before uploading it to the repository, use this example:

    ```xml
    <match pattern="/app:company_home" type="folder">
        <target>
            <property name="cm:subjectline" />
        </target>
    </match>
    ```

21. To use wildcards, add the asterisk character in the folder path, for example:

    ```xml
    <match type="folder" pattern="/app:company_home/st:sites/*/cm:standard-metadata-folder" >
        <target>
            <property name="cm:title" />
            <property name="cm:description">
                <ui multiline="true"/>
            </property>
        </target>
    </match>
    ```

    This rule allows you to assign metadata to every `standard-metadata-folder` located under any `st:sites`, and with any number of folders between `st:sites` and `cm:standard-metadata-folder`.

    Here is another example to show how the asterisk can be used in multiple locations:

    ```xml
    <match type="folder" pattern="/app:company_home/st:sites/*/cm:testfolder/*/cm:metadatafolder1">
    ```

    You can also use the asterisk wildcard in this way:

    ```xml
    <match type="folder" pattern="/app:company_home/st:sites/cm:test*/cm:metadatafolder1">
    ```

    > **Note:** An exact match of the folder without a wildcard takes priority over the wildcard pattern.

22. Starting from Outlook Integration 2.9.1, you can configure a dependent picklist that defines a constraint between two lists of values. For example:

    ```xml
    <match pattern="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:list-metadata" type="folder">
        <target default="true" name="List Metadata" schemaId="81143a75">
            <property allowedCategoryValues="cm:categoryRoot/cm:generalclassifiable/cm:Regionen/cm:EUROPA/cm:Nördliches_x0020_Europa" name="wpsmail-qa-ext:list-metadata-country-text">
                <picklist targetProperty="wpsmail-qa-ext:list-metadata-language-text">
                    <controllingField name="United Kingdom">
                        <value name ="English"/>
                        <value name ="Scottish"/>
                        <value name ="Irish"/>
                        <value name ="Welsh"/>
                    </controllingField>
                    <controllingField name="Germany">
                        <value name ="German"/>
                    </controllingField>
                    <controllingField name="Spain">
                        <value name ="Spanish"/>
                    </controllingField>                    
                </picklist>
            </property>
            <property name="wpsmail-qa-ext:list-metadata-languagetext" allowedCategoryValues="cm:categoryRoot/cm:generalclassifiable/cm:Languages" />
         </target>
    </match>
    ```

    If a property controls more than one dependent drop-down list, you can define `<picklist>` multiple times under the `<property>` tag.

    In this example, the first defined property contains a picklist to control the second property. When selecting a value for the first property, the Outlook plugin will try to find a corresponding entry in the configuration by using the `<controllingField>`.

    * If a match is found, the plugin filters the second property to only show the specified values.
    * If no matching `<controllingField>` is found, the second property shows all available values.

    Here is an example of how the dependency works.

    | Drop-down box 1 values | Drop-down box 2 values |
    | ---------------------- | ---------------------- |
    | {::nomarkdown}<ul><li>United Kingdom </li><li>Germany </li><li>Spain </li><li>France </li></ul>{:/} | {::nomarkdown}<ul><li>English </li><li>German </li><li>Spanish </li></ul>{:/} |

    When you select `Spain` in the first drop-down box, the second drop-down only allows you to select the value `Spanish`. However, when you select `France` in the first drop-down, the second drop-down shows all available languages without filtering, because `France` isn't configured as a `<controllingField>`.

23. Save your changes and restart Microsoft Outlook.

    The template changes are applied.

    You can download the custom content metadata, custom folder metadata, and list view settings locally by clicking **Download configuration**.

### Configure search settings

You can configure search settings for the Outlook Integration using Share Admin Tools. These settings define global controls across your enterprise and are applied immediately.

1. Open Alfresco Share, and click **Admin Tools** on the toolbar.

2. Click **Search Settings** then **Edit**.

    See [Outlook search settings](#detailedconfigsearchsettings) for more detailed guidance on adding search settings.

3. Paste the XML code that contains the configuration settings for the Alfresco Outlook Client into the **Configuration XML content** field, or load and edit the default configuration template by clicking **Load default configuration template**.

    You can use the default configuration template for testing purposes, and edit this if you prefer.

4. Click **Apply** to save.

    If your XML isn't valid, you won't be allowed to save your settings, and you'll see an error message.

#### Detailed config of search settings {#detailedconfigsearchsettings}

Use this guidance to configure simple and advanced search criteria in Outlook.

You can configure the search criteria presented when a user starts a search in Outlook. This configuration supports the content models, including data types, constraints, lists, regular expressions and other attributes.

You can configure navigation-sensitive simple and advanced searches based on the search location. Use the **Custom simple search** to configure a simple search, where the Outlook Integration includes the metadata fields in the search dynamically for the search term provided. Use the **Custom advanced search** to configure an advanced search, where the search form adapts dynamically so different fields are shown, depending on the navigation context of the user.

When a user starts a search, the Outlook Integration finds the best match for the metadata dialog. The `<match>` element uses the first rule that matches the attributes in the tag. If you are using multiple rules,
you should always start with the most specific rule first.

In the `<match>` element:

1. Define the match type. This can be a folder, type or aspect.

2. Define the match pattern. This can be the location of the folder (defined in xpath format), or it can be based on a defined model, type, or aspect.

See examples of how to use these search settings below.

1. Open Alfresco Share, and click **Admin Tools** on the toolbar.

2. Click **Search Settings** then **Edit**.

    You can configure XML settings for **Custom simple search**, and **Custom advanced search**.

3. You can load and edit the default configuration template for each section by clicking **Load default configuration template**.

    Here is the full list of metadata settings that you can configure:

    |Section name|Key name|Description|Values|
    |------------|--------|-----------|------|
    |`match`|`type`|Mandatory. Defines type of the attribute|`folder`, `type`, `aspect`|
    | |`pattern`|Mandatory. Path to the site or folder where custom metadata is applied|Example:<br><br>Site: `pattern="/app: company_home/st:sites/cm:qaext- standard-metadata"`<br><br>Folder: `pattern="/app: company_home/st:sites/cm:qaext- custom-metadata/cm: documentLibrary/cm:numeric-metadata"`|
    |`target`|`useTags`|Controls use of tags|`true`: tags are permitted<br><br>`false`: tags are not permitted|
    | |`useText`|Controls use of full-text search|`true`: full text search permitted<br><br>`false`: full text search not permitted|
    |`property`|`name`|Name of the custom property|Text format|
    | |`allowedValues`|List of permitted values.|Text format|
    | |`allowedCategoryValues`|Path to the list of permitted values|Text format|
    |`ui`|`multiline`|Controls use of multiple lines in a box|`true`: multiple lines are permitted<br><br>`false`: multiple lines are not permitted|

4. To apply default search criteria for the whole repository, use this example:

    ```xml
    <match pattern="/app:company_home/st:sites/cm:myexample-1-site-standard-search" >
        <target useTags="true" useText="true">
            <property name="cm:title"/>
            <hr/>
            <property name="cm:description">
              <ui multiline="true"/>
            </property>
        </target>
    </match>
    ```

    In this example, the only available child element is `<target>`. In `<target>` you can specify `useTags` and `useText` as attributes. In the example shown:

    * The Tags search field is enabled (`useTags="true"`)
    * The Text search field is enabled (`useTags="true"`)

    The user sees a search dialog with several fields including `cm:title` and `cm:description`. This allows the user to search for documents and folders by title and description, as well as by tags, and through the full text of documents.

    The `cm:description` field can contain multiple lines by setting `<ui multiline="true"/>`.

    The `<hr/>` element adds a horizontal line to the search dialog.

    If no type information is present, the default `cm:content` type is used for all nodes stored in Share. The `<target>` element can contain 0 or more child elements called `<property>`.

    In the `<property>` tag:

    * Use the `name` attribute to set a valid model property like `cm:title`
    * Use the `<ui>` child element to control how the fields are displayed in the search dialog

5. To add numeric fields to the search dialog, use this example:

    ```xml
    <match type="folder" pattern="/app:company_home/st:sites/cm:myexample-2-site-custom-metadata/cm:documentLibrary/cm:numeric-metadata" >
        <target>
            <property name="wpsmail-qa-ext:number-metadata-float" />
            <property name="wpsmail-qa-ext:number-metadata-double" />
            <property name="wpsmail-qa-ext:number-metadata-int" />
            <property name="wpsmail-qa-ext:number-metadata-long" />
        </target>
    </match>
    ```

    In this example, the user sees a different search dialog in the `numeric-metadata` folder (or its sub folders) on the `myexample-2-site` site. The dialog will contain four fields with custom numeric data in float, double, int and long format.

    If the above example is applied to the **Custom advanced search** configuration, the user sees the default search fields for any site or folder in the repository except in `myexample-2-site/custom-metadata/numeric-metadata`.

    If the above example is applied to the **Custom simple search** configuration, the Outlook Integration uses the search criteria mentioned in the `<target>` element only to find search results.

6. To apply search criteria using an aspect, use this example:

    ```xml
    <match type="aspect" pattern="cm:versionable">
        <target useTags="true" useText="true">
            <property name="cm:title"/>
            <hr/>
            <property name="cm:description">
                <ui multiline="true"/>
            </property>
        </target>
    </match>
    ```

7. To use wildcards, add the asterisk character in the folder path, for example:

    ```xml
    <match pattern="/app:company_home/st:sites/*/cm:myexample-1-site-standard-search" >
        <target useTags="true" useText="true">
            <property name="cm:title"/>
            <hr/>
            <property name="cm:description">
                <ui multiline="true"/>
            </property>
        </target>
    </match>
    ```

    Starting from Outlook Integration 2.8.1, this rule allows you to assign the search configuration to every `myexample-1-site-standard-search` located under any `st:sites`, and with any number of folders between `st:sites` and `myexample-1-site-standard-search`.

    Here is another example to show how the asterisk can be used in multiple locations:

    ```xml
    <match pattern="/app:company_home/st:sites/*/cm:testfolder/*/cm:myexample-1-site-standard-search">
    ```

    You can also use the asterisk wildcard in this way:

    ```xml
    <match pattern="/app:company_home/st:sites/cm:test*/cm:myexample-1-site-standard-search">
    ```

    > **Note:** An exact match of the pattern without a wildcard takes priority over the wildcard pattern.

8. Click **Apply** to save your changes and restart Microsoft Outlook.

    The template changes are applied.

    If your XML isn't valid, you won't be allowed to save your settings, and you'll see an error message.

    You can download the custom simple search and custom advanced search settings locally by clicking **Download configuration**.

### Configure email settings {#configoutlookemailsettings}

You can configure email integration settings for the Outlook Integration using Share **Admin Tools**.
These settings define global controls across your enterprise and are applied immediately.

1. Open Alfresco Share, and click **Admin Tools** on the Alfresco toolbar.

    The URL is:

    ```html
    http://localhost:8080/share/page/console/admin-console/mail-customization-config
    ```

    where `localhost:8080` is your Alfresco server and port number.

2. Select **Integration Settings** from the Tools menu and click **Edit**.

3. In **Browse sites** you can specify which sites are displayed when you select an email and use the **Archive Directly** right click option in the Alfresco Outlook Client.

    Options are **All public sites**, **My sites** or **Favorite sites**.

    >**Note:** Outlook users are able to change this and other settings locally for the Alfresco Outlook Client. See [Configure extended settings in Outlook](#configure-extended-settings) for more information.

4. In **Prevent email duplication in**, choose to check the uniqueness of files and at what level.

    When a new email document is uploaded, the server checks if it has already been archived in the repository. As an administrator, you can configure the server to check for existing email documents in the repository or at the site level. Select one of the following values:

    1. **None**: duplication check is not required.

    2. **Repository**: emails with same messageID are not allowed across the whole repository.

    3. **Site**: emails with same messageID are not allowed across a site.

    >**Note:** If an email is dropped into a folder, where the same email document already exists, the version detection feature will recognize it, and the **Versioning** dialog is displayed. See [Managing file versions in Outlook]({% link microsoft-outlook/latest/using/index.md %}#managing-file-versions-in-outlook) for more details.

5. If you have an Alfresco Application Development Framework (ADF) application installed, such as the Digital Workspace, you can configure your Outlook clients to use links to it instead of Alfresco Share. For example, if you want to view the document details page, this configuration will open the relevant page in Digital Workspace instead of Share.

    In **ADF App Base URL**, set the path to something like:

    ```http
    http://localhost:8081/digital-workspace
    ```

6. Specify a number in **Page size** to limit the number of files and folders visible at a time in the Explore view of the Alfresco sidebar in Outlook.

    >**Note:** Entering a value of 0 removes any limit on the number of files and folders displayed.

7. Specify a number in **Maximum number of search results** to limit the number of results returned in the Alfresco sidebar in Outlook.

    >**Note:** Entering a value of 0 removes any limit.

8. Check **Automatically convert emails (EML, MSG) uploaded using Share, CIFS, WebDAV, FTP, NFS** if you want every email (EML / MSG) which is uploaded from Share, CIFS, WebDAV, FTP or NFS (for example, uploading using an integrated WebDAV folder in the Windows tree structure) to be converted in exactly the same way, as if it were uploaded through Outlook.

    **Module version** displays the version of the Alfresco Outlook Client.

9. Check **Auto configure all clients** if you want every connected client with an installed Alfresco Outlook Client to receive the configuration settings automatically.

    Checking this box activates **Allow overwriting**.

    1. Check **Allow overwriting** to set global general settings for the Outlook Client.

    2. Paste the XML code that contains the configuration settings for the Alfresco Outlook Client into the **Configuration XML content** field, or load and edit the default configuration template by clicking **Load default configuration template**.

10. Check **Enable attachment stripping** to upload attachments to the selected site in the Alfresco repository. In the email they are replaced with a link to the repository file.

    If **Enable attachment stripping** is enabled, the **Target site** field becomes mandatory (in order that the files are stored in the designated repository).

    >**Note:** Automated attachment stripping isn't supported for meetings and appointments.

11. Click **Select** next to the **Target site** field to specify the Alfresco site where you want to store attachments. Click the plus (+) sign next to your chosen site, and **OK** to add it.

    Only one site can be specified in this field.

12. Select one or both of the stripping rules:

    Wildcard characters can't be used in these fields, and if selected, they can't be left blank.

    1. **Strip attachments when all recipients have the following domain**: type the required domain name.

    2. **Strip attachments when recipient list contains the following email address**: type the required email address.

13. Specify a number in **Min size in KB**. This number controls the minimum size of attachment that is stripped; for example, to exclude company logos or very small attachments.

14. Click **Manage** to prevent stripping of media in the email signature.

    Enter a space delimited list of file extensions or files that you don't want stripped from the email, for example;

    ```text
    test.docx *.txt *.xlsx
    ```

15. Click **Enable custom labels for Email as Link action** to define properties that determine what text is shown when you select **Email as link** in Alfresco.

16. Specify the Subject text that you would like to be displayed in the **Email as link in subject prefix** field.

17. Specify the Action text that you would like to identify in the **Email as link action text**; for example, **Click to view file {0}** displays the file name at the end of the label.

18. Click **Enable upload restrictions** and **Manage** to specify content that can't be uploaded from the Outlook Client.

    * Enter a space delimited list of file extensions or files that you don't want to be uploaded to Alfresco, for example;

    ```text
    *.docx *.txt *.xlsx
    ```

    >**Note:** Only content that is uploaded in the Alfresco Outlook Client is restricted. If you upload content directly to Alfresco (through Share), it isn't restricted.

19. Click **Apply** to save your settings.

    * Specify the maximum number of files for the folder upload.

    This limits the number of files that your users can drop at once onto the plugin to reduce server load.

    * Specify the maximum combined file size in MB.

    This sets a limit for the folder size that your users can drop onto the plugin.

20. Click **Apply** to save your settings.

### Configure other settings

You can view and edit other settings for the Outlook Integration using Share **Admin Tools**.
These settings define global controls across your enterprise.

1. Open Alfresco Share, and click **Admin Tools** on the Alfresco toolbar.

2. Select **Access Tokens** from the Tools menu and click **Edit**.

    In the list of access tokens, there is information about logged in users.

3. Select **Remove** or **Remove all** to disconnect individual (or all) users.

4. Select Licenses from the Tools menu and click **Edit** to add new licenses.

    See [Installing server and client licenses in Alfresco Share]({% link microsoft-outlook/latest/install/index.md %}#installserverclientlicenses) for more information about installing licenses.

5. Select **System Info** from the Tools menu to view system information.

6. Select **Download all settings** to download all your email configuration server settings locally as a zip file.

    This may be useful to share with our Support team, if requested.

## Microsoft Outlook configuration

This section contains Microsoft Outlook configuration instructions for the Outlook Integration.

### Configure connection settings

Configure Microsoft Outlook to find and connect to the correct Alfresco server.

1. Select **Configure > Connection** from the Alfresco Client tab in Microsoft Outlook.

2. In **Server URL**, type the address of the Alfresco server that you want to connect to.

    Type only the information before `/share`. For example, `https://IP address` or `server name`:`port number`.

    >**Note:** For the HTTPS connection to work from the Alfresco Outlook Client to Alfresco, we strongly recommend using an SSL configuration for a production environment, as a self-signed certificate will not work.

3. In **Alfresco Repository path**, type the name of the Alfresco repository.

    >**Tip:** This is often `alfresco`.

4. In **Alfresco Share path**, type the name of the Alfresco Share instance.

    >**Tip:** This is often `share`.

    Alternatively, specify an alternative Share URL in the **Alternative Share URL** field, if Alfresco and Share are running on different servers.

5. Select either **Windows authentication** or **Standard** authentication.

    If you select standard authentication, enter your Alfresco user name and password. If you select Windows authentication, the `passthru` authentication is used. For more information about authentication subsystem types, see [Authentication subsystem types]({% link content-services/latest/admin/auth-sync.md %}#Authentication subsystem types).

6. Click **Check connection** to test the connection to the Alfresco server.

### Configure email archive settings

You can configure Microsoft Outlook to archive email in Alfresco, including archiving emails as links.

You can decide what format you want to use to save your emails, and how to archive your emails. In **Email Archiving**, take one or more of the following actions:

* Save the original Outlook MSG file in Alfresco with the original email
* Save attachments as separate files in Alfresco
* Save email as a link to the content in Alfresco
* Use default settings for archiving (where all emails are saved to the Alfresco server, based on the option selected in **Default archive** settings)
* Show settings when archiving (to select how each email will be archived)
* Compress the email message when uploading the content
* Always use the default folder

You can reduce the size of your Outlook inbox by replacing emails with links to the content in Alfresco:

1. Select **Configure > Email Archiving** from the **Alfresco Client** tab in Microsoft Outlook.

2. Click **Replace content with links** and your preferred option in **Email archive** settings.

    **Replace content with links** saves the email (as an EML file) in Alfresco and a link (without text and attachments) in Microsoft Outlook.

    If you click the **Download original email message** link in an archived email, the original email is loaded from Alfresco and can be opened in Outlook.

Outlook emails are archived to the Alfresco server, and can be accessed using links in Microsoft Outlook.

#### Configure alternative naming of emails {#configalternativenamingemails}

You can configure Microsoft Outlook to archive email in Alfresco using an alternative naming convention. By default, the Alfresco Outlook Client shows the subject line for emails instead of the name. This allows to change the name of an email document that's displayed in the Alfresco Outlook Client, in Alfresco Share or in Webdav.

Previously, changes to the `cm:name` attribute in Share or Webdav did not affect the name that was displayed in the Alfresco Outlook Client. In addition, if you used a naming convention for emails saved in your file system (for example, on a networked drive), when you moved these files into Alfresco via the Alfresco Outlook Client, the file name of the document was not saved as the email name in the Alfresco Outlook Client. Instead, the email was named using the email subject, so you needed to manually rename each email after the upload.

#### Alternate naming settings

You can change the default behavior for archiving email to display the `cm:name` attribute in the **Name** column in the Alfresco Outlook Client. Since the `cm:name` might not look like the subject line, special characters need to be replaced. As an administrator, you can change the display attribute for the email name in the [Alfresco Client Settings file](#advanced-configuration) XML file.

As an administrator, you can decide if email names should be derived from the email document's file name or its subject line when uploaded from the desktop. For example, you can add the following attributes to the XML file to enable each setting:

```xml
<feature useFilenameOnUploadMsg="true" useFilenameOnRenderMsg="true" />
```

>**Note:** These attributes are not exposed in the UI for Alfresco Outlook Client settings.

See [Alfresco Client Settings file](#advanced-configuration) for more details.

### Configure Send and Archive

You can decide whether to use a default folder for every email sent with the **Send and Archive** button or always receive a prompt to choose a folder.

1. Select **Configure > Email Archiving** from the **Alfresco Client** tab in Microsoft Outlook.

2. Select **Always use default folder**, choose a folder in the **Folder selection** window, and click **OK** to save your selection.

3. Select **Open default folder** to open the folder in a new browser window, for example, if you wish to change your selection.

4. Click **OK** to save your **Email Archiving** settings.

See the `<storage>` section in [Alfresco Client Settings file](#advanced-configuration) for more details.

### Configure extended settings

You can configure Outlook extended settings; for example, change the display language, Alfresco settings, or drag and drop priorities.

1. Select **Configure > Extended** from the **Alfresco Client** tab in Microsoft Outlook.

2. **Language**: Choose the display language.

    >**Note:** You can also change the display language by selecting **Language** from the **Alfresco Outlook** toolbar tab.

3. **Theme**: Choose the theme for the Outlook plugin.

    >**Note:** Restart Microsoft Outlook to apply the new theme.

4. **Show Alfresco Outlook Client**: Show or hide the **Alfresco Outlook Client** panel (the Alfresco sidebar).

    >**Note:** This box is checked automatically if you have selected **Show Sidebar** from the **Alfresco Client** tab in Outlook.

5. **Show sidebar for new emails**: Show or hide the Alfresco sidebar in emails that are open in a current window.

6. **Repository root**: Select whether the Alfresco sidebar and **Archive Directly** right click option allow you to see certain sites (**Sites only**) or all of Alfresco (**Full repository**).

7. **Browse Sites**: Specify the default selection for the **Sites** list that is displayed in the **Explore** tab of the Alfresco sidebar.

8. **Drag and drop priority**: Defines the priority for drag and drop from Alfresco:

    * **File**: Use drag and drop to attach a file from Alfresco into an email as a binary attachment. Hold down the Control (Ctrl) key to link files from Alfresco to the email as HTTP links.
    * **Link**: Use drag and drop to add files from Alfresco to the email as HTTP links. Hold down the Control (Ctrl) key to add files from Alfresco to the email as binary attachments.
    * **PDF**: Use drag and drop to convert Office files to PDF format and attach them to email.
    * **Link to PDF**: Use drag and drop to convert Office files to PDF format and add to the email as an HTTP link.

9. **Use web URIs for**: Controls the target application for calling a browser directly from Outlook.

    Options are:

    * Alfresco Share (standard)
    * Alfresco ADF (Application Development Framework)

    The location of the ADF client application must be configured in Share Admin Tools by your IT team.

10. **Show tooltip on email hover**: Select to see a tool tip when you hover over an email.

11. **Use default web browser**: Select whether the default browser should be used to open files.

12. **Enable debug logging**: Check to enable logging for debug purposes. Check the log file by clicking **Open Log**.

13. **Folder sort order**: Select the order you want for your Alfresco folders. Choose from **Name and subject (ascending)**, **Name and subject (descending)**, **Date modified (ascending)**, or **Date modified (descending)**.

14. **Date sort display options**: If you select **Date modified (ascending)** or **Date modified (descending)** you can choose the display format from **Subject or name**, **Date and subject**, or **Date/time and subject**.

### Configure views

You can configure the look and feel of the Alfresco sidebar.

You can configure which fields are visible in the list view of the Alfresco sidebar.

1. Select **Configure > Views** from the **Alfresco Client** tab in Microsoft Outlook.

    If your IT team has configured the list view so that you can't edit your settings locally, the buttons on this tab are grayed out.

2. Check all columns that you want to see in the list view in the sidebar.

    You can also move columns up and down (for example, if you want to see the name of a file or folder before the modified date, you can move that column name higher. **Type** is not editable and is always visible. This column is displayed as an icon representing a site, file, or folder.

    If your IT team has assigned an alternative column configuration for a specific site, folder, or content type, you can define different list views for each location.

3. Click **Reset** to restore the default column views.

    See [Configuring Outlook metadata and list view settings in Alfresco Share](#configmetadataandlistview) for more information.

4. Click OK to save.

### Import the configuration template

Set the configuration template to import when the configuration dialog is called for the first time.

1. Select **Configure > Configuration** from the **Alfresco Client** tab in Microsoft Outlook.

2. Click **Apply central settings** to apply settings that have been defined in Alfresco Share **Admin Tools > Outlook Integration > Integration Settings > Auto configure all clients**.

    For more information, see [Configuring Outlook email settings in Alfresco Share](#configoutlookemailsettings).

### Advanced configuration

Use the Alfresco Client Settings XML file for advanced configuration of Alfresco Microsoft Outlook client.

The `AlfrescoClientSettings-3.0.x.xml` file contains advanced configuration properties.
Use this file to set up attributes and metadata settings.

1. Locate and open `AlfrescoClientSettings-3.0.x.xml` in the `C:\Users\<username>` directory, where `<username>` is your Windows user name.

    The `<outlook>` section contains elements that you can configure to customize the Alfresco Outlook Client, and also additional `<storage>`, `<connection>`, `<logging>`, `<restrictions>`, and `<tabs>` sections:

    Here is a sample configuration file:

    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <settings>
      <outlook format="1.0" dragPrio="document" showExplorer="true" showExplorerNew="false" defaultBrowser="true" visibleSites="public" visibleNodes="default" showEmailTooltip="false" hoverPreview="true" isSitesRoot="true" showMySites="false" folderSort="name_asc" dateSortView="subject" sendLinkUrl="details" panelViewMode="tree" searchMode="standard" mailNameDisplayPattern="" culture="en" customAppTitle="" customRibbonTitle="" customMenuTitle="">
        <connection url="http://127.0.0.1:8080/" shareUrl="share" alfrescoUrl="alfresco" login="admin" password="7DkTRpO8sfo=" checkCertificate="true" checkVersion="true" authentication="basic" webApp="2" shareAlterUrl="" settingsCheckInterval="480" />
        <logging minLevel="info" />
        <storage archiveOption="0" storeFiles="true" storeLink="true" storeMsg="false" compress="true" />
        <feature autoPaging="false" tokenAlterMode="false" messageIcon="false" />
        <explorer-search-properties />
        <search-properties />
      </outlook>
    </settings>
    ```

2. Configure the attributes that you need for the base `<outlook>` element:

    |Attribute|Description|Value|
    |---------|-----------|-----|
    |`dragPrio`|Sets behavior for files that are dragged and dropped into a new email from the Explore tab in the Alfresco sidebar|`document`: attaches to a new email as a file. This is the default setting.<br><br>`link`: a link to a file is created in the email body<br><br>`pdf`: file is converted to PDF format and is attached to a new email<br><br>`pdflink`: a link to the converted PDF file is created in the email body|
    |`showExplorer`|Shows or hides the Explore tab in the Alfresco sidebar|`True`: tab is shown. This is the default setting.<br><br>`False`: tab is not shown.|
    |`showExplorerNew`|Controls the appearance of the Alfresco sidebar in emails that are open in a current window.|`True`: sidebar is shown. This is the default setting.<br><br>`False`: sidebar is not shown.|
    |`defaultBrowser`|Sets the external browser to use to open links to Alfresco|`True`: system default browser is used. This is the default setting.<br><br>`False`: Internet Explorer is used.|
    |`visibleSites`|Sets the sites that are shown in the Explore tab in the Alfresco sidebar|`public`: all sites are visible. This is the default setting.<br><br>`private`: only sites that the current user is a member of are visible<br><br>`favorites`: only sites set by the user as a favorite are visible|
    |`visibleNodes`|Controls content visible in the Explore tab tree view in the Alfresco sidebar|`default`: all files and folders are visible. This is the default setting.<br><br>`favdocument`: only files marked by the user as a favorite are visible<br><br>`favfolder`: only folders marked by the user as a favorite are visible<br><br>`favonly`: only files and folders marked by the user as a favorite are visible|
    |`hoverPreview`|Controls the behavior of the Preview window in the Search tab of the Alfresco sidebar|`true`: preview window is shown when hovering over the found item. This is the default setting.<br><br>`false`: preview window is not shown when hovering over the found item.|
    |`isSitesRoot`|Sets a root folder to show in the Explore tab of the Alfresco sidebar|`true`: root is the Sites folder. This is the default setting.<br><br>`false`: root is the Company Home folder.|
    |`mailNameDisplayPattern=" #subject (#from)"`|Modifies the email appearance in the Explore tab tree view of the Alfresco sidebar|Use these variables to modify the email fields displayed: `#subject`, `#from`, `#to`, `#sent`|
    |`culture`|Sets the language used in Alfresco Outlook Client|Possible settings:`en`: English<br><br>`de`: German<br><br>`es`: Spanish<br><br>`it`: Italian<br><br>`fr`: French<br><br>`ja`: Japanese<br><br>`ru`: Russian<br><br>`zh-cn`: Chinese (Simplified)<br><br>`pt-br`: Brazilian Portuguese<br><br>`nl`: Dutch<br><br>`nb-no`: Norwegian (Bokmal)<br><br>`cs`: Czech<br><br>`da`: Danish<br><br>`sv`: Swedish<br><br>`fi`: Finnish<br><br>`pl`: Polish<br><br>|
    |`customAppTitle`|Renames the Alfresco Outlook Client sidebar|Enter your chosen title as a text string.|
    |`customRibbonTitle`|Renames the Alfresco Client tab|Enter your chosen title as a text string.|
    |`customMenuTitle`|Renames the Alfresco Client option when right clicking a file|Enter your chosen title as a text string.**Note:** If you set this option, the same value is applied to `customRibbonTitle` if `customRibbonTitle` is blank.|
    |`sendLinkUrl`|Controls the behavior of links to files in Alfresco|`details`: link to the Document Details page is created. This is the default setting.<br><br>`download`: link to the Document Download page is created (only applies for Share URLs)|
    |`folderSort`|Sets the sorting options for folders in the Explore tab tree view of the Alfresco sidebar|`name_asc`: folders are sorted in alphabetical order. This is the default setting.<br><br>`name_desc`: folders are sorted in reverse alphabetical order<br><br>`modified_asc`: folders are sorted by date modified ascending<br><br>`modified_desc`: folders are sorted by date modified descending|
    |`dateSortView`|Sets the date sort display options in the Explore tab of the Alfresco sidebar|`subject`: files are sorted by subject or name. This is the default setting.<br><br>`date`: files are sorted by date and subject<br><br>`datetime`: files are sorted by date and time, and subject|
    |`showEmailTooltip`|Controls whether a tool tip is shown when hovering over an email|`true`: tool tip is shown when hovering over the email. This is the default setting.<br><br>`false`: tool tip is not shown when hovering over the email.|
    |`panelViewMode`|Controls the appearance of the Outlook sidebar|`list`: sidebar is shown as a list. This is the default setting.<br><br>`tree`: sidebar is shown as a tree structure.|
    |`searchMode`|Controls the search behavior|`standard`: standard search is used. This is the default setting.<br><br>`advanced`: Advanced search is used.|
    |`showMySites`|Controls the appearance of My Sites site selector|`true`: My Sites site selector is shown. This is the default setting.<br><br>`false`: My Sites site selector is not shown.|
    |`theme`|Sets the theme of the Outlook plugin.<br><br>Added in Outlook Integration 2.9.|`classic`: Classic plugin theme is used. This is the default setting.<br><br>`dark`: Dark theme is used.|
    |`showSpecificLanguages`|Sets the available languages of the Outlook plugin.<br><br>Added in Outlook Integration 2.9.2.|`empty`: All supported languages can be selected. This is the default setting.<br><br>`en,de,fr`(example): Only English, German and French can be selected.|

3. Configure the attributes that you need for the `<storage>` element:

    |Attribute|Description|Value|
    |---------|-----------|-----|
    |`archiveOption`|Controls email archive settings|`0` or `1`: default archive settings are used. This is the default setting.<br><br>`2`: archiving options are shown before the email is uploaded.|
    |`storeFiles`|Controls the Extract email attachment archive option|`true`: email attachments are extracted on upload to Alfresco. This is the default setting.<br><br>`false`: email attachments are not extracted on upload to Alfresco.|
    |`storeFilesFromDesktop`|Controls the Extract attachments from files archive option.<br><br>Added in Outlook Integration 2.9.|`true`: email attachments from desktop files are extracted on upload to Alfresco.<br><br>`false`: email attachments are not extracted on upload to Alfresco. This is the default setting.|
    |`storeLink`|Controls the Archive as link email option|`true`: email is replaced with a link to email stored in Alfresco<br><br>`false`: email is not replaced with a link to the email stored in Alfresco. This is the default setting.|
    |`storeMsg`|Controls the Store original Outlook .MSG file archive option|`true`: original Outlook . MSG file is stored on upload to Alfresco<br><br>`false`: original Outlook . MSG file is not stored on upload to Alfresco. This is the default setting.|
    |`compress`|Controls the Compress message while uploading setting|`true`: message is compressed while uploading to Alfresco. This is the default setting.<br><br>`false`: message is not compressed while uploading to Alfresco|
    |`alwaysUseDefaultSendAndArchiveFolder`|Controls the Always use default folder archive option|`true`: uses the specified default folder.<br><br>`false`: select folder with every upload. This is the default setting.|

4. Configure the attributes that you need for the `<connection>` element:

    |Attribute|Description|Value|
    |---------|-----------|-----|
    |`url`|URL to Alfresco server|This is the path to your Alfresco server.|
    |`login`|User name for Alfresco server|This is your Alfresco user name.|
    |`password`|Password for Alfresco server (encrypted)|This is your Alfresco password.|
    |`shareUrl`|Path to Alfresco Share|`share`: this is the default setting. Specify a text string for an alternative path.|
    |`alfrescoUrl`|Path to Alfresco repository|`alfresco`: this is the default setting. Specify a text string for an alternative path.|
    |`authentication`|Authentication type for connection to Alfresco|`basic`: basic authentication is used to connect to Alfresco. This also works out-of-the-box if using the Identity Service.<br><br>`windows`: Kerberos authentication is used to connect to Alfresco.<br><br>`oidc`: OpenId Connect authentication is used to connect to Alfresco.<br><br>**Note:** Contact Alfresco support before using these settings.|
    |`webApp`|Which Alfresco web application is used to display details, links, etc. outside of the Outlook Integration.|`2`: Share. This is the default setting.<br><br>`3`: ADF|
    |`shareAlterUrl=""`|Sets alternative URL for Alfresco Share|Specify your alternative URL.<br><br>|
    |`checkCertificate`|Specifies whether to check for a server certificate|`true`: certificate is checked and if it is not correct then the connection fails. This is the default setting.<br><br>`false`: certificate is not checked|
    |`checkVersion`|Specifies whether to check the Alfresco server version|`true`: version is checked and if it is not correct then the connection fails. This is the default setting.<br><br>`false`: version is not checked|
    |`settingsCheckInterval`|Specifies the interval, in seconds, between checks to determine if the central settings have changed|`480`: 480 seconds is the default setting.|
    |`writeStreamBuffering`|Sets the `AllowWriteStreamBuffering` parameter of the HttpWebRequest.<br><br>**Note:** In a clustered Alfresco environment, you may encounter the error message _“This request requires buffering data to succeed”_ while uploading emails or files. Setting `writeStreamBuffering` to `true` will prevent this error from happening.<br><br>Added in Outlook Integration 2.7.|`true`: `AllowWriteStreamBuffering` is enabled.<br><br>`false`: `AllowWriteStreamBuffering` is disabled. This is the default setting.|

5. Configure the attributes that you need for the `<oidc>` element. The `<oidc>` configuration element is part of the `<connection>` element:

    |Attribute|Description|Value|
    |---------|-----------|-----|
    |`serverUrl`|URL to the Alfresco Identity Service system that is used for authentication via OpenId Connect.<br><br>**Note:** Only relevant if the authentication type is set to `oidc` in `<connection>` element.<br><br>Added in Outlook Integration 2.10.|URL to Identity Service server|
    |`realm`|Realm of the Alfresco Identity Service system that is used for authentication via OpenId Connect.<br><br>**Note:** Only relevant if the authentication type is set to `oidc` in `<connection>` element.<br><br>Added in Outlook Integration 2.10.|`alfresco` is the default setting.<br><br>You can change the value if a different realm is set in Identity Service.|
    |`clientId`|Identity Service OpenId Connect client that is used for the authentication.<br><br>**Note:** Only relevant if the authentication type is set to `oidc` in `<connection>` element.<br><br>Added in Outlook Integration 2.10.|`alfresco` is the default setting.<br><br>You can change the value if a different OpenId Connect client is set in Identity Service.|
    |`redirectUrl`|Redirect URL that is used by Identity Service to redirect the Outlook Integration to do the token exchange for authentication.<br><br>**Note:** Only relevant if the authentication type is set to `oidc` in `<connection>` element.<br><br>Added in Outlook Integration 2.10.|`"https://127.0.0.1:6543/OutlookIntegrationCallback"` is the default setting.<br><br>You can change the value, but it needs to match the Identity Service setting for allowed redirects for the configured client.|

6. Configure the attributes that you need for the `<feature>` element:

    |Attribute|Description|Value|
    |---------|-----------|-----|
    |`autoPaging`|Controls auto paging (for the tree view)|`true`: auto paging is enabled. A refreshed list of files and folders is automatically loaded when scrolling to the bottom of the tree.<br><br>`false`: auto paging is not enabled. This is the default setting. A More button is displayed to allow loading of content.|
    |`messageIcon`|Controls the appearance of the Alfresco icon for archived mail|`true`: Alfresco icon appears on archived emails. This is the default setting.<br><br>`false`: Alfresco icon appears on archived emails.<br><br>**Note:** There is no visual icon to indicate that the email is archived.|
    |`useFilenameOnUploadMsg`|Controls if Alfresco should use the file name of email files uploaded from the desktop or the subject line to name the document in the repository. This option applies to email files uploaded from the desktop only.<br><br>Added in Outlook Integration 2.4.7. Supported in versions 2.4.7 onwards and 2.6.|`true`: Alfresco uses the file name to name the document in the repository.<br><br>`false`: Alfresco uses the subject line of the email to name the document in the repository.|
    |`useFilenameOnRenderMsg`|Controls if Alfresco should use the `cm:name` or `subjectline` attribute to display in the list/tree view. This option applies to email documents only.<br><br>Added in Outlook Integration 2.4.7. Supported in versions 2.4.7 onwards and 2.6.|`true`: Alfresco uses the `cm:name` instead of the `subjectline` attribute to show the email document in the list/tree view.<br><br>`false`: Alfresco uses the `subjectline` attribute to show the email document in the list/tree view.|
    |`enableWFTab`|Controls the visibility of the Workflow tab in high resolution mode.<br><br>Added in Outlook Integration 2.6.|`true`: Workflow tab is visible.<br><br>`false`: Workflow tab is collapsed. This is the default setting.|
    |`tokenAlterMode`|Used for QA and testing. Toggles the way a client is uniquely identified.|**Note:** Keep the default value: `false`.|
    |`copyMoveWarningThreshold`|Sets the threshold for when a warning should be displayed, when a large amount of files is being copied/moved inside the repository with the copy/move & paste feature. Warns the user that copying `x` amount of files can take a long time depending on the server.<br><br>Added in Outlook Integration 2.7.|`100` is the default setting.|

7. Configure the attributes that you need for the `<logging>` element:

    |Attribute|Description|Value|
    |---------|-----------|-----|
    |`minLevel`|Sets logging level|`debug`: activates debug logging<br><br>`info`: activates info logging. This is the default setting.<br><br>`warning`: activates warning logging<br><br>`error`: activates error logging|

8. Configure the attributes that you need for the `<restrictions>` element.

    1. For the high resolution front-end of the Alfresco Outlook Client:

        Restrictions can be set either to apply globally or context-based. The context-based configuration supports a specific location, and the behavior of Microsoft Office and non-Microsoft Office documents.

        Here are some examples:

        |Attribute|Description|
        |---------|-----------|
        |`<action type="browse" enabled="false" enabledForMsOffice="true" />`|Open menu item is hidden for any item in the repository, but is visible for Microsoft Office documents.|
        |`<action type="edit" enabled="false" location="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:_x0031__x0020__x0026__x0020_2_x0026_3" />`|Edit menu item is disabled for any Microsoft Office documents in the specified location.|
        |`<action type="delete" enabled="false" enabledForMsOffice="true" location="/app:company_home/st:sites/cm:qa-ext-custom-metadata/cm:documentLibrary/cm:_x0031__x0020__x0026__x0020_2_x0026_3" />`|Delete is enabled only for Microsoft Office documents in the specified location:|
        |`<action type="delete" enabled="false" />`|Delete is disabled at the repository level for any item. The previous option overrides this one.|
        |`<action type="checkout" enabledForMsOffice="false"/>`|Checkout is disabled at the repository level for any Microsoft Office document.|
        |`<action type="download" enabled="false" />`|Download is disabled at the repository level for any item.|

    2. For all versions of the Alfresco Outlook Client:

        |Attribute|Description|Value|
        |---------|-----------|-----|
        |`<action type="new-folder" enabled="true" />`|Sets action: create a new folder|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="new-document" enabled="true" />`|Sets action: create a new file|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="edit" enabled="true" />`|Sets action: edit online|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="rename-document" enabled="true" />`|Sets action: rename a file|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="rename-folder" enabled="true" />`|Sets action: rename a folder|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="delete" enabled="true" />`|Sets action: delete|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="send-content" enabled="true" />`|Sets action: email as an attachment|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="send-link" enabled="true" />`|Sets action: email as link|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="set-favorite" enabled="true" />`|Sets action: add to favorites|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="workflow" enabled="true" />`|Sets action: start workflow|`true`: action is enabled (only available if `webApp` is set to Share). This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="details-msg" enabled="true" />`|Sets action: Alfresco Details|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="details" enabled="true" />`|Sets action: details|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="download-pdf" enabled="true" />`|Sets action: download as a PDF|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="download" enabled="true" />`|Sets action: download|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="import-msg" enabled="true" />`|Sets action: import message|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="browse" enabled="true" />`|Sets action: open|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="search-full-text" enabled="true" />`|Sets action: Search text and metadata in Search menu|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="search-metadata" enabled="true" />`|Sets action: Search metadata in Search menu|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="search-sites" enabled="true" />`|Sets action: Search sites in Search menu|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="set-metadata" enabled="true" />`|Sets action: edit metadata|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="checkout" enabled="true" />`|Sets action: checkout|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="cancel-checkout" enabled="true" />`|Sets action: cancel checkout|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="version-history" enabled="true" />`|Sets action: version history|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled|
        |`<action type="download-drop" enabled="true"/>`|Sets action: drag & drop<br><br>Drag & drop was formerly linked to the "download" restriction and is now independent.<br><br>Added in Outlook Integration 2.7.|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled.|
        |`<action type="copy-document" enabled="true"/>`|Sets action: copy document<br><br>Added in Outlook Integration 2.7.|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled.|
        |`<action type="move-document" enabled="true"/>`|Sets action: move document<br><br>Added in Outlook Integration 2.7.|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled.|
        |`<action type="copy-folder" enabled="true"/>`|Sets action: copy folder<br><br>Added in Outlook Integration 2.7.|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled.|
        |`<action type="move-folder" enabled="true"/>`|Sets action: move folder<br><br>Added in Outlook Integration 2.7.|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled.|
        |`<action type="upload-drop-folder" enabled="true"/>`|Sets action: upload folder via drag & drop<br><br>Added in Alfresco Outlook Integration 2.8|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled.|
        |`<action type="send-and-archive" enabled="true"/>`|Sets action: send and archive<br><br>Added in Outlook Integration 2.8.|`true`: action is enabled. This is the default setting.<br><br>`false`: action is not enabled.|

9. Configure the attributes that you need for the `<tabs>` element:

    |Attribute|Description|Value|
    |---------|-----------|-----|
    |`<tab type="workflow" enabled="true" />`|Controls visibility of Workflow tab in Alfresco sidebar in low resolution mode|`true`: Workflow tab is visible.<br><br>`false`: Workflow tab is not visible. This is the default setting.|

10. Configure the attributes that you need for the `<metadata>` element:

    |Attribute|Description|Value|
    |---------|-----------|-----|
    |`extended`|Controls automatic completion of metadata|Use the `<extended>` element to specify text that you would like auto-completed for metadata. You can define one or more properties in the `<autofill>` element. Use the format shown in the example:|

    ```xml
    <metadata>
      <extended>
        <autofill>  
         <property name="wpsmail-qaext: source" value="Outlook" />
         <property name="wpsmail-qaext: source-type" value="123" />
        </autofill>
      </extended>
    </metadata>
    ```

11. Save your changes and restart Microsoft Outlook.

    The template changes are applied.
---
title: Install Outlook Integration
---

Outlook Integration is an extension to Content Services and Microsoft Outlook that allows you to save and file your emails to Alfresco from within Microsoft Outlook, in a centralized and structured way.

You can drag and drop emails in and out of the repository, and add metadata automatically when an email is filed. Other features include leveraging Alfresco's in-built workflow processing and filtered search capabilities.

Advanced metadata support includes:

* Full support for custom models
* A configurable and dynamic metadata dialog
* The ability to map metadata configuration to a path, folder type, or aspect
* The ability to assign the same metadata to a set of emails in Microsoft Outlook, or a set of files in your file system

You can apply a sorted view to the Alfresco repository (from within Microsoft Outlook), and page through a folder or site if it contains a large number of files.

You can also create new versions of existing documents, review the version history of a versioned document, and revert back to previous versions.

This information helps system administrators to install, configure, and manage Outlook Integration.

The software you need to install Outlook Integration is as follows:

* AMP files that are applied to Alfresco and provide the administration tooling in Alfresco Share
* A server license that is applied in Alfresco Share
* Client licenses that can be applied in Alfresco Share or in Microsoft Outlook
* A zip file that provides an addition to the Microsoft Outlook toolbar, which you unzip and install before you start up Microsoft Outlook

If you plan to enable the transformation of MSG and EML files into PDF format, you need to install and configure Alfresco Transform Service.

You can download the Outlook Integration software from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

## Prerequisites

There are a number of software requirements for installing Outlook Integration. See [Supported Platforms]({% link microsoft-outlook/latest/support/index.md %}) for more information.

You need one of each of the following components:

### Operating system requirements

You can use one of the following operating systems:

* Microsoft Windows 11 with latest updates
* Microsoft Windows 10 with latest updates

### Software requirements

You can use one of the following Outlook releases:

* Microsoft Outlook for Office 365 (x86/x64) with latest updates
* Microsoft Outlook 2019 (x86/x64)
* Microsoft Outlook 2016 (x86/x64)
* [Visual Studio Tools for Office 4.0 Runtime](https://msdn.microsoft.com/en-us/library/ms178739.aspx){:target="_blank"}
* Microsoft .NET Framework 4.7.2 or above

### Alfresco requirements

* Alfresco Content Services 23.x.

See the [Supported platforms]({% link microsoft-outlook/latest/support/index.md %}) for more.

#### Alfresco Search Services 2.0 and above

If you're using Alfresco Search Services or Alfresco Search and Insight Engine 2.0 and above in combination with Outlook Integration 2.10 and above, you must add the `messageId` property to the `shared.properties` file for SOLR. See the Indexing recommendations (Cross locale section) for the product you're using to locate this file:

* Search Services: [Indexing recommendations - Cross locale]({% link search-services/latest/config/indexing.md %}#cross-locale)
* Search and Insight Engine: [Indexing recommendations - Cross locale]({% link insight-engine/latest/config/indexing.md %}#cross-locale)

Add the following lines to the configuration:

```bash
alfresco.cross.locale.property.#={http://www.alfresco.org/model/imap/1.0}messageId
alfresco.cross.locale.property.#={http://www.westernacher.com/alfresco/models/wpsmail-v2}messageId
```

where `#` is an ascending index number that hasn't been used.

Starting from Outlook Integration 2.10, you must also enable cross-locale data types in Alfresco Search Services or Alfresco Search and Insight Engine 2.0 and above.

Follow the steps in the Indexing recommendations (Cross locale section) for the product you're using to enable this configuration. This applies for both the `messageId` property addition and enabling cross-locale data types:

* Search Services: [Indexing recommendations - Cross locale]({% link search-services/latest/config/indexing.md %}#cross-locale)
* Search and Insight Engine: [Indexing recommendations - Cross locale]({% link insight-engine/latest/config/indexing.md %}#cross-locale)

> **Note:** These changes require a SOLR restart, but no reindex.

#### Alfresco Search Enterprise

If you're using Alfresco Search Enterprise in combination with Outlook Integration, you must add the `messageId` property to the `shared.properties` file for Elasticsearch configuration in Alfresco Content Services. See the recommendations in the Exact Term Search section to locate this file:

* Search Enterprise: [Exact Term Search]({% link search-enterprise/latest/config/index.md %}#exact-term-search)

Add the following lines to the configuration:

```bash
alfresco.cross.locale.property.#={http://www.alfresco.org/model/imap/1.0}messageId
alfresco.cross.locale.property.#={http://www.westernacher.com/alfresco/models/wpsmail-v2}messageId
```

where `#` is an ascending index number that hasn't been used.

You must also enable cross-locale data types in Search Enterprise.

Follow the steps in the Exact Term Search (Cross locale section) to enable this configuration. This applies for both the `messageId` property addition and enabling cross-locale data types:

* Enterprise Search: [Exact Term Search]({% link search-enterprise/latest/config/index.md %}#exact-term-search)

### Java requirements

* Java: OpenJDK 17 is recommended. This needs to be installed on the server only (i.e. not the Outlook clients). See the Content Services [Supported Platforms]({% link content-services/latest/support/index.md %}) for more information.

### Access to Docker image

The Docker image that you can use for the Outlook Integration T-Engine is uploaded to a private registry, **Quay.io**. You'll need access to the following image:

```bash
transform-outlook
```

* A [Quay.io](https://quay.io/){:target="_blank"} account is needed to pull Docker images that are needed for Outlook Integration.

> **Note:** Alfresco customers can request Quay.io credentials by logging a ticket at [Alfresco Support](https://support.alfresco.com/){:target="_blank"}. These credentials are required to pull private (Enterprise-only) Docker images from Quay.io.

> **Note:** Make sure that you request credentials for Alfresco Content Services and Alfresco Outlook Integration, so that you can use the additional `transform-outlook-1.2.x` Docker image.

> **Note:** It is recommended that you familiarize yourself with the concepts of [containerized deployment]({% link content-services/latest/install/containers/index.md %}) before working with Docker.

## Install AMPs

There are three steps to installing Outlook Integration:

* Install the Alfresco AMP files (the Alfresco Outlook Server software)
* Apply the licenses
* Install the Microsoft Outlook zip file (the Alfresco Outlook Client software)

Make sure you are running the correct versions of operating system and software before you install the AMP files.

* If you plan to transform MSG and EML files into PDF format, check the requirements in [Transform Service prerequisites]({% link transform-service/latest/install/index.md %}#prerequisites).

1. Stop the Alfresco server.

2. Browse to [Hyland Community](https://community.hyland.com/){:target="_blank"}, download and unzip the Outlook Integration zip package:

    `alfresco-outlook-integration-3.0.x.zip`

3. Copy the provided AMP files to the Alfresco `amps` and `amps_share` directories.

    Copy this file to the `amps` directory:

    `alfresco-outlook-repository-3.0.x.amp`

    and this file to the `amps_share` directory:

    `alfresco-outlook-share-3.0.x.amp`

4. To install the AMP files, run the `apply_amps.bat` file from the Alfresco `bin` directory.

    Check the output from the script to ensure that the AMP files have installed successfully.

5. Restart the Alfresco server.

6. Open Alfresco Share, and click **Admin Tools** on the Alfresco toolbar to see the Outlook configuration section.

    The URL is: `http://localhost:8080/share/page/console/admin-console/mail-customization-config`

    where `localhost:8080` is your Alfresco server and port number.

If you plan to transform MSG and EML files into PDF format, you need to install and configure the Transform Service, and then select an installation method under [Install Transform Engine](#install-transform-engine) for more information.

### Install server and client licenses in Alfresco Share {#installserverclientlicenses}

Use Alfresco Share Admin Tools to install your Outlook Integration server and client licenses.

Ensure that you have applied the Alfresco Outlook Server AMP files ([see Install Outlook Integration AMPs](#install-amps)).

1. Open Alfresco Share, and click **Admin Tools** on the Alfresco toolbar.

    The URL is: `http://localhost:8080/share/page/console/admin-console/mail-customization-config`

    where `localhost:8080` is your Alfresco server and port number.

2. Select Licenses and click **Edit**.

3. Open the server license file in a text editor, and copy and paste the contents into the Server License field.

4. *(Optional)* Open the client license file in a text editor, and copy and paste the contents into the **Outlook Client License** field.

    Alternatively, specify the client license in Microsoft Outlook in **Alfresco Client > Configure > License**.

    >**Note:** There is no Lotus Notes capability, so you do not need to add information in **Lotus Notes Client License**.

5. Click **Save**.

    The server license status, number of current users, maximum users, product version and other information is displayed. Check that the license status is valid.

    >**Note:** If you added a client license, the license key is displayed, with a message to check the **Alfresco Client > Configure > License** tab in Microsoft Outlook (do this check after you have installed Alfresco Outlook Client).

    >**Note:** The server and client licenses are stored in a system folder in Alfresco, and will persist after a restart in containerized environments. The folder location is:
    > `/sys:system/cm:wps_alfresco_mail_integration/cm:license/cm:mail`.

## Install Transform Engine

The Outlook Integration Transform Engine (or T-Engine) enables transformation of MSG and EML files into PDF format when used with the Transform Service. The Outlook Integration T-Engine is available both as a Docker image and as a Web Archive (WAR) file.

### Install T-Engine on Tomcat {#tengine-war}

If you wish to use a Tomcat application server, you can use the WAR bundle to install the Outlook Integration T-Engine.

> **Note:** Check the supported Tomcat version based on your version of the [Content Services documentation]({% link content-services/latest/support/index.md %}) before continuing.

1. Install the latest required version of Tomcat, for example, [Tomcat 10](https://tomcat.apache.org/download-10.cgi){:target="_blank"} to run as a service.

    See the [Tomcat documentation](https://tomcat.apache.org/tomcat-10.1-doc/index.html){:target="_blank"} for more information about configuring and using a Tomcat server.

    For information about securing Tomcat, see [Tomcat security considerations](https://tomcat.apache.org/tomcat-10.1-doc/security-howto.html){:target="_blank"}.

2. Rename the WAR file from `transform-outlook-webapp-${version}.war` to `transform-outlook.war`.

    You'll find the file, `transform-outlook-webapp-2.0.0.war`, in the distribution zip.

3. Copy the WAR file into your `<TOMCAT_HOME>/webapps` folder.

4. To enable ActiveMQ in the Outlook T-Engine, set the following URL property in `JAVA_OPTS`:

    `-DACTIVEMQ_URL=${activemq.url}`

5. To enable the shared file store in the Outlook T-Engine, set the following URL property in `JAVA_OPTS`:

    `-DFILE_STORE_URL=${shared.file.store.url}`

6. Start the Tomcat service.

7. Test that the T-Engine is running:

    1. Open your browser and access `http(s)://${SERVER}:{PORT}/transform-outlook` to load the T-Engine test page.

    2. Add the following configuration property in `alfresco-global.properties`:

        ```bash
        localTransform.transform-outlook.url=http(s)://${SERVER}:{PORT}/transform-outlook
        ```

### Install T-Engine using Docker Compose {#tengine-docker}

To deploy the Outlook Integration T-Engine with the Transform Service, you'll need to update your Docker Compose file to include the Outlook T-Engine.

> **Note:** While Docker Compose is often used for production deployments, the Docker Compose file provided is recommended for development and test environments only. Customers are expected to adapt this file to their own requirements, if they intend to use Docker Compose to deploy a production environment.

1. Add Outlook Integration T-Engine container to your `docker-compose.yaml` file:

    ```yaml
    transform-outlook:
        image: quay.io/alfresco/transform-outlook:2.0.0
        mem_limit: 2g
        environment:
            JAVA_OPTS: " -Xms256m -Xmx512m"
            ACTIVEMQ_URL: "nio://activemq:61616"
            ACTIVEMQ_USER: "admin"
            ACTIVEMQ_PASSWORD: "admin"
            FILE_STORE_URL: "http://shared-file-store:8099/alfresco/api/-default-/private/sfs/versions/1/file"
        ports:
            - 8091:8090
        links:
            - activemq
    ```

2. Add the following `JAVA_OPTS` property to the `alfresco` container:

    ```yaml
    -DlocalTransform.transform-outlook.url=http://transform-outlook:8090/
    ```

See the Content Services documentation - [T-Engine configuration](https://github.com/Alfresco/acs-packaging/blob/master/docs/creating-a-t-engine.md#t-engine-configuration){:target="_blank"} for more details. For further development, see [Content Transformers and Renditions Extension Points]({% link content-services/latest/develop/repo-ext-points/content-transformers-renditions.md %}).

## Install Alfresco Outlook Client in Microsoft Outlook {#installclient}

Inside the Outlook Integration zip is another zip file that installs the Alfresco Outlook Client into Microsoft Outlook.

You might need local administrator rights to install .NET and Microsoft VS Tools for Office Runtime. Ensure you have already installed the required AMP files in your Alfresco instance ([see Install Outlook Integration AMPs](#install-amps)).

>**Note:** If you are distributing Alfresco Outlook Client across an organization, see [Install the Alfresco Outlook Client in unattended mode](#installunattendedmode) for guidance on installing in unattended mode.

1. Extract the contents of the `alfresco-outlook-client-3.0.x.zip` file using a standard unzip tool.

2. Navigate to the directory containing the unzipped content and double click the `install.bat` file.

    The Alfresco Outlook Client installer checks whether the required components already exist on the system. The required files are installed and the Alfresco Outlook Client installer wizard opens.

3. Read the copyright information and click **Next**.

4. Specify the folder where you would like the Outlook Client to be installed and click **Next**.

    Alternatively, accept the default path specified.

5. Click **Next** to confirm that the installation can start.

6. Select your preferred language, and click **Continue**.

    Microsoft Office Primary Interop Assemblies are also installed, if they do not already exist in your version of Microsoft Office.

7. Click **Close** to complete the installation.

8. Open Microsoft Outlook.

    You will see an **Alfresco Client** tab on the toolbar. Click this tab to view options for configuring the Alfresco Outlook Client.

    If you did not enter a client license key in Alfresco Share, you must enter one when you open Microsoft Outlook. Navigate to **Alfresco Client > Configure > License** to enter your key.

### Install Alfresco Outlook Client in unattended mode {#installunattendedmode}

You can automate the Alfresco Outlook Client installation by using the `msiexec` command.

You might need local administrator rights to install .NET and Microsoft VS Tools for Office Runtime. Ensure you have already installed the required AMP files in your Alfresco instance ([see Install Outlook Integration AMPs](#install-amps)).

1. Extract the contents of the `alfresco-outlook-client-3.0.x.zip` file using a standard unzip tool.

2. Locate `x64/AlfrescoOutlookClient_x64_3.0.x.msi` or `x86/AlfrescoOutlookClient_x86_3.0.x.msi`, depending on whether you are running a 64-bit or 32-bit version of Windows.

3. From a command line, navigate to the `x64` or `x86` directory, and run the `msiexec` command. For example:

    For an interactive installation:

    ```bash
    msiexec /i AlfrescoOutlookClient_x86_3.0.x.msi HOST=127.0.0.1:8080 AUTH=basic
    ```

    For a non-interactive installation:

    ```bash
    msiexec /i AlfrescoOutlookClient_x86_3.0.x.msi HOST=127.0.0.1:8080 AUTH=basic /quiet
    ```

    For a non-interactive installation with OpenId Connect enabled:

    ```bash
    msiexec /i AlfrescoOutlookClient_x86_3.0.x.msi HOST=127.0.0.1:8080 AUTH=oidc /quiet
    ```

    >**Note:** Microsoft Office Primary Interop Assemblies are also installed, if they do not already exist in your version of Microsoft Office.

    Here is a full list of parameters that can be used with the `msiexec` command:

    |Parameter|Values|Description|
    |---------|------|-----------|
    |`HOST`|Format: `<http|https>://<hostname>:<port>`|Sets the Alfresco server URL. Port is optional.|
    |`SHARE`|Default: `share`|Sets context to Alfresco Share.|
    |`ALFRESCO`|Default: `alfresco`|Sets context to the Alfresco repository.|
    |`CULTURE`|`en|de|es|it|fr|ja|ru|zh-cn|pt-br|nl|nb-no|cs|da|fi|pl|sv` Default: `en`|Sets language for Alfresco Outlook Client.|
    |`SHAREALT`|No default|Sets alternative URL for Alfresco Share.|
    |`AUTH`|`basic|windows|oidc`|Sets authentication type.|
    |`APPTITLE`|Default: Alfresco Outlook Plugin|Sets a custom title for Alfresco Outlook Client. Format: `"My Custom Title"`|
    |`LANGS`|No default|Sets the available languages for the Alfresco Outlook Client. Format: `"en,de,fr"`. See `CULTURE` parameter for available language codes.<br><br>Added in Outlook Integration 2.9.2.|
    |`OIDCHOST`|Format: `https://<idsHost>:<port>`|Sets the URL for the Identity Service that is used for OpenId Connect.<br><br>Added in Outlook Integration 2.10.|
    |`OIDCCID`|Default: `alfresco`|Sets the OpenID Connect Client that is used in the Identity Service.<br><br>Added in Outlook Integration 2.10.|
    |`OIDCREALM`|Default: `alfresco`|Sets the realm that is used in the Identity Service.<br><br>Added in Outlook Integration 2.10.|
    |`OIDCURL`|Default: `https://127.0.0.1:6543/OutlookCallback`|Sets local redirect callback URL that is used in the Outlook Client to do the token exchange with the Identity Service.<br><br>Added in Outlook Integration 2.10.|

4. Verify that Alfresco Outlook Client has installed in Microsoft Outlook.

    You will see an **Alfresco Client** tab on the toolbar. Click this tab to view options for configuring the Alfresco Outlook Client.

    If you did not enter a client license key in Alfresco Share, you must enter one when you open Microsoft Outlook. Navigate to **Alfresco Client > Configure > License** to enter your key.

## Uninstall

This section walks through how to uninstall Outlook Integration.

### Uninstall Outlook Integration

To uninstall the Alfresco Outlook files, use the Module Management Tool (MMT). To completely remove Outlook Integration, you must uninstall the Outlook package from Alfresco, as well as from Microsoft Outlook on all Windows clients.

This information provides uninstall directions for Alfresco Content Services.

>**Note:** See [Uninstall Outlook Client](#uninstall-outlook-client) to uninstall the Alfresco Outlook Client.

1. Stop the Alfresco server.

2. Use the information in [Uninstall an Amp file]({% link content-services/latest/install/zip/amp.md %}#uninstall-an-amp-file) to uninstall each AMP file.

    For example, from the Alfresco root directory, you need two commands:

    ```bash
    java -jar bin/alfresco-mmt.jar uninstall com.westernacher.wps.AlfrescoMailIntegrationRepository tomcat/webapps/alfresco.war

    java -jar bin/alfresco-mmt.jar uninstall com.westernacher.wps.AlfrescoMailIntegrationShare tomcat/webapps/share.war
    ```

    Use these commands to check whether the AMP files were removed:

    ```bash
    java -jar bin/alfresco-mmt.jar list tomcat/webapps/alfresco.war
                  java -jar bin/alfresco-mmt.jar list tomcat/webapps/share.war
    ```

3. Delete the `tomcat/webapps/alfresco` and `tomcat/webapps/share` folders in the Alfresco installation directory.

    Deleting these directories forces Tomcat to read the edited WAR files when Alfresco is restarted.

4. Restart the Alfresco server.

### Uninstall Outlook Client

Learn how to uninstall the Alfresco Outlook Client.

>**Note:** You can uninstall the Outlook client from your Microsoft Windows machines. Using the standard **Programs > Uninstall Program** feature in Windows. Look for **Alfresco Outlook Client** and uninstall it.

There are two different ways to uninstall the Alfresco Outlook Client for enterprise installations:

1. Use the original `.msi` file to uninstall the client by running a single command.

    ```bash
    msiexec /x <Path_to_msi_file> /q
    ```

    where `/x = uninstall`, `/q = silent`.

2. Use the identifying number.

    The identifying number is tied to a specific version of your Outlook Integration. If your users have different versions installed, you need to find out the product IDs for each version.

    1. Install the Outlook plugin version that was distributed to the machines of your end users.

    2. Run the PowerShell command:

        ```bash
        get-wmiobject Win32_Product | Format-Table IdentifyingNumber, Name, LocalPackage -AutoSize
        ```

    3. Search for Alfresco Outlook Client and copy the identifying number from the first column of the output (including the brackets).

    4. Run the `msiexec` command with administration permissions on the end user machine using the identifying number. For example:

        ```bash
        msiexec /x  {723B7FFD-3B53-4786-9741-D845BC1796A3} /q
        ```

        where `/x = uninstall`, `/q = silent`.

        >**Note:** For more Microsoft msiexec documentation, see [Command-Line Options](https://docs.microsoft.com/en-us/windows/win32/msi/command-line-options){:target="_blank"}.
---
title: Supported platforms
---

The following are the supported platforms for Outlook Integration 3.0:

| Version | Notes |
| ------- | ----- |
| Alfresco Content Services 23.2.x | *Optional.* Use with Outlook Integration T-Engine v2.0.0 |
| Alfresco Content Services 23.1.x | *Optional.* Use with Outlook Integration T-Engine v2.0.0 |
| | |
| | Check the [Alfresco Content Services Supported platforms]({% link content-services/latest/support/index.md %}) page for specific versions of the individual components. |
| **Application servers** | |
| Apache Tomcat | |
| | |
| **Java** | |
| JDK 17 | Check the supported JDKs based on your Content Services version |
---
title: Upgrade Outlook Integration
---

If you are upgrading to a new release of Outlook Integration, uninstall the previous Alfresco AMPs and Outlook zip file.

These instructions show you how to upgrade your instance of Outlook Integration.

1. Stop the Alfresco server.

2. Back up any custom folders and files that you have created.

3. Uninstall the Outlook Integration AMP files, using MMT (Module Management Tool).

    See [Uninstall Outlook Integration]({% link microsoft-outlook/latest/install/index.md %}#uninstall) for instructions on how to uninstall the AMP files.

    Delete the `tomcat/webapps/alfresco` and `tomcat/webapps/share` folders before restarting Alfresco in step 6 to ensure that the new war files are exploded.

4. Download, extract and install the new Outlook Integration files.

    You do not need to uninstall a previous version of Alfresco Outlook Client. You can install the new client and all settings are transferred to the new version. See [Install Outlook Integration]({% link microsoft-outlook/latest/install/index.md %}) for instructions on how to do this.

5. Restart the Alfresco server and open Microsoft Outlook.

    Test that you can connect successfully to the Alfresco repository from Microsoft Outlook.

6. If you used custom types in a previous version of Alfresco Outlook, you can optionally run an upgrading model script.

    Later versions of Alfresco Outlook use `cm:content` instead of a custom type to store email-related objects. All emails archived from version 2.0 onwards use the `cm:content` model. You need to run the script only if you want to align all emails to the same model.

    1. Enter the URL: `http://localhost:8080/alfresco/service/wps/mail/bulkmailmodelupdate` where `localhost:8080` is your Alfresco host and port number.

    2. Select **Test** to run the script in test mode, to understand how many files might change.

    3. Select **Model Update** to change your archived content to use the `cm:content` model.

7. Starting from Outlook Integration 2.10 and with the deprecation of Alfresco SAML Module, the authentication protocol has changed to OpenId Connect.

    If the previous version of the Outlook Integration is configured to use SAML as the authentication type, you'll need to configure OpenId Connect related parameters in the **Connection** tab of the **Alfresco Client**.

    See [Using SAML SSO with Outlook Integration]({% link microsoft-outlook/latest/admin/index.md %}) for the client-side configuration details:

    ![Alfresco client configuration in Outlook]({% link microsoft-outlook/images/2-10-Outlook-connection-saml.png %})

    If the client configuration is synced via the server, the existing server-side configuration needs to be extended with the `<oidc>` element using the Share Admin Tools page `https://<ALFRESCO_HOST>/share/page/console/admin-console/mail-general-config`.

    The `<oidc>` element must be placed inside the `<connection>` element of the **Integration Client Settings** panel, as seen in the following sample:

    ![Integration Client Settings in Alfresco Share Admin Tools]({% link microsoft-outlook/images/2-10-Integration-Client-Settings.png %})

    ```xml
    <connection shareUrl="share" alfrescoUrl="alfresco" authentication="basic" webApp="2" shareAlterUrl="" checkCertificate="true" checkVersion="true" settingsCheckInterval="480" writeStreamBuffering="false">
        <oidc serverUrl="https://<IdentityServiceUrl>" clientId="alfresco" realm="alfresco" redirectUrl="https://127.0.0.1:6543/OutlookCallback" />
    </connection>
    ```
---
title: Using Outlook Integration
---

The Alfresco Outlook Client is part of the Outlook Integration and allows you to use email and repository management without having to leave Microsoft Outlook.

Features of Outlook Integration include the ability to archive content (i.e. emails, meetings, appointments, and files) into Alfresco, full metadata support, full search, tagging and workflow capabilities, and the ability to attach files and view archived emails in your inbox. In addition, you can create new versions of existing documents, review the version history of a versioned document, and revert back to previous versions.

>**Important:** In this documentation, the term 'email' is used to refer to emails, meetings, and appointments for the sake of readability.

For information about installing and configuring the Outlook Integration, see [Installing and configuring the Outlook Integration]({% link microsoft-outlook/latest/install/index.md %}).

## Archiving content in Outlook

You can archive emails to a site or folder by dragging and dropping the email into a folder in your chosen site in the Alfresco sidebar.

When you drag and drop the email with a subject that already exists in a specific location, you'll be asked to rename it.

>**Note:** If you drag and drop to a folder, you're not prompted for a location for the email.

1. Archive an email manually by dragging and dropping it into a folder in your chosen site.

2. You might see a **Metadata** dialog, if this has been configured by your IT team. Enter the information needed for archiving the email.

    For example, you may be able to select different metadata settings, if configured by your IT team. Select the **Numeric Metadata** content type to see the fields you can apply to the uploaded content. If you're filing a number of emails, you can check **Remember metadata for next object** to retain your settings for the next time you archive an email.

    Here is an example **Metadata** dialog:

    ![This screen capture shows the metadata dialog with a metadata selector and associated fields, plus icons for the actions listed.]({% link microsoft-outlook/images/Outlook-metadata-dialog.png %})

    * The first line indicates the number of emails that you are archiving (in this case, **1 / 1** is 1 of 1 emails), and the title of the current email. If you're archiving more than one email, the **Next** and **Previous** options are enabled so that you can page between the emails.
        >**Note:** By default, Alfresco Outlook Integration displays the subject line of the email document as the title. See [Configuring alternative naming of emails in Outlook]({% link microsoft-outlook/latest/config/index.md %}#configalternativenamingemails) if you want to change this behavior.
    * If you have email attachments, the **Apply to all attachments** option is enabled and you can apply any metadata you enter to all attachments related to that email.  
    * If you're archiving more than one email, the **Apply to all emails** option is enabled and you can apply the same metadata to all emails that are being archived.
        >**Note:** You can only try to archive one type of Outlook item at a time, either emails, meetings or appointments.
    * If your IT team has configured multiple metadata options for a specific upload location, the **Content type** field shows a list of options and you can pick the most appropriate metadata depending on the content you're archiving.
    * Select **Save** to save your changes.
    * If you copy a single file to a folder in Alfresco Share, and then choose the **Cancel** option to stop the transfer, the file will still transfer into Share. The **Cancel** action works best when transferring multiple files. The last transferred file remains in Share, however the other files are not transferred.
    * If you select **Send to background** during the transfer, the window is hidden and you can view the progress in a **Transfer** tab in the Alfresco sidebar.

        During the file transfer, you can cancel the file transfer from this tab, or bring the window back to the foreground.

        After the file transfer is complete, you can open the target folder in the Alfresco sidebar, or click **Close** to close the tab:

        ![]({% link microsoft-outlook/images/outlook-transfer.png %})

        The **Transfer** tab color is green if the transfer progresses successfully, or red if there are issues. For file transfer issues, a link to the log is displayed in the tab content.

        >**Note:** It is not possible to start another upload while the background transfer is in progress. Also, in Alfresco Outlook Integration 2.7, the **Workflow** tab is disabled by default.

    A check is made for duplicates during email archiving. The ID of each email is checked to see if it has already been saved in the repository or on the same site. If the email has already been saved, a message is displayed saying that the message already exists in the repository, giving details of who archived the file, when it was archived, and the path of the archived file. You can open the previously archived email, save a new version of the email with a different subject, or cancel the archive operation.

    Here is a summary of how the combined version detection and email duplication detection works:

    1. The Alfresco Outlook Client checks if the email to be uploaded already exists in the upload location.
    2. If it does exist, the version detection dialog is shown, and offers you an alternative name.
    3. Next, there's a check to see if the email exists in another folder, either at site-level or repository-level (depending what your IT team has configured). See [Configuring Outlook email settings in Alfresco Share]({% link microsoft-outlook/latest/config/index.md %}#configoutlookemailsettings) for guidance on customizing **Integration Settings**.
    4. If a match is found, the Alfresco Outlook Client shows the duplication dialog, presenting a reference to the duplicate email in the other folder.

    When an email is archived, it is usually identified with an Alfresco icon in the Outlook inbox: ![Alfresco archive icon in Outlook]({% link microsoft-outlook/images/Outlook_alf_icon.png %}){:height="18px" width="18px"}

    An email that is archived as an attachment can be opened directly by double-clicking the email in Outlook. The email opens in a new window and can be read normally. An email that is archived as a link can be loaded into Outlook by clicking the link in the email.

    See [Outlook metadata settings]({% link microsoft-outlook/latest/config/index.md %}#configmetadataandlistview) for metadata configuration guidance.

### Archiving emails after sending

When sending a new email, you can choose to automatically archive it after it has been sent by using the **Send and Archive** button located in your **Alfresco Client** tab.

This button is available in the **Alfresco Client** tab when you’re composing an email, and combines the separate actions for sending the email and then manually dragging it onto the Outlook sidebar to archive it:

![This image shows the Send and Archive button in the Alfresco Client tab]({% link microsoft-outlook/images/2-8-ribbon.png %}){:width="600px"}

> **Note:** The standard **Send** button inside your email is not affected.

> **Note:** This functionality is only supported for Microsoft Exchange accounts.

## Archiving folders in Outlook

You can create folders in the Alfresco Outlook Client and assign metadata to these folders, similar to when archiving emails.

You can create different types of folders within a particular location and assign different sets of metadata depending on the type of content the folder contains. You may be able to select different metadata settings, if configured by your IT team. This allows you to select the best metadata fields from a list in the metadata dialog.

1. Click the **Explore** tab from the Alfresco sidebar, or navigate through the list view.

    If there is no **Explore** tab displayed, continue to the next step.

2. Select a site and folder from the directory tree, right-click the context menu then select **Create folder**.

    The system displays a folder metadata dialog. The default folder metadata scheme and associated properties are shown.

3. In the **New Folder** dialog, enter the information needed to create the folder.

    For example, you may be able to select different folder metadata settings, if configured by your IT team. Select **Payload Target** in the **Folder type** list to see the fields you can apply to the new folder.

    Here is an example folder metadata dialog:

    ![This screen capture shows the metadata dialog shown when creating a new folder and (optionally) assigning metadata.]({% link microsoft-outlook/images/Outlook-folder-metadata.png %})

    * In the **Folder name** field, enter a name for the new folder.
    * If your IT team has configured multiple folder metadata options for a specific upload location, the **Folder type** field shows a list of options and you can pick the most appropriate metadata depending on the content you're archiving. Note that some fields may be read-only, such as the **Boolean property** field, and you can't change them.
    * Select **Save** to create the new folder with defined folder type and properties.

    The system updates the navigation panel and shows the new folder.

   See [Outlook metadata settings]({% link microsoft-outlook/latest/config/index.md %}#configmetadataandlistview) for metadata configuration guidance.

## Managing files using the Alfresco sidebar

In Outlook, use the sidebar to browse and work with your connected repository.

1. In the **Alfresco Client** tab on the Outlook toolbar and click **Show Sidebar**.

    This option displays a new window on the right side of the screen, called **Alfresco Outlook Client**.

    >**Note:** If the sidebar is already displayed, clicking **Show Sidebar** hides the sidebar.

2. There are two tabs available: **Explore** and **Workflow**.

    These tabs are shown at the bottom of the sidebar and allow you to switch from one view to another.

    The **Explore** view and allows you to work with your files and folders in Alfresco Share.

    >**Note:** In Alfresco Outlook Integration 2.7, the **Explore** tab is only available if the **Workflow** tab is also enabled to save space for more content. The **Workflow** tab is hidden by default.

3. Use the following tasks to learn about these tabs.

### Explore options in the Alfresco sidebar

Work with your files and folders using the Alfresco sidebar.

1. Click the **Explore** tab from the **Alfresco Outlook Client** sidebar, or navigate through the list view.

    ![Outlook Client sidebar - 2.9.2+]({% link microsoft-outlook/images/2-9-2-outlook-sidebar-annotated.png %})

    >**Note:** In Alfresco Outlook Integration 2.7, the **Explore** tab is only available if the **Workflow** tab is also enabled to save space for more content. The **Workflow** tab is hidden by default.

    >**Note:** In Alfresco Outlook Integration 2.9.2, the **Explore** tab includes a Simple Search Filter that allows you to filter the simple search results via options **Exclude folders** or to show **Folders only**. The default option is to show **All content**.

2. Repo location selector: choose which sites and content you wish to see. You can see the full repository in this view, or limit the view to certain sites only (**All Sites**, **My Sites** or **Favorite Sites**).

3. Content filter: choose to view all content, or only your favourite files or folders.

4. View selector: choose whether to see your content in a tree view or a list view.

5. Search selector: choose between a simple or complex search (if this is configured).

    1. Search mode selector: choose whether to search text and metadata, or just metadata, or search at a site level.

    2. Enter your search criteria.

        Type directly in the search box, where it says **Enter your search**.

        You can choose favorite folders or sites to filter the search.

    3. The content that matches your criteria is displayed below the search box.

        Once you select a folder in the search results, use **Back to search results** to return to the search results in the original search location. You can clear the search results by clicking X next to the search box starting a new search.

    4. Context menu: there are a number of actions to apply for each search result. These include:

        * ![Outlook Client email attachment icon]({% link microsoft-outlook/images/outlook-search-attach-email.png %}){:height="18px" width="18px"} Send an email, with this result attached (applicable to files only)
        * ![Outlook Client email link icon]({% link microsoft-outlook/images/outlook-search-email-link.png %}){:height="18px" width="18px"} Send an email, with this result embedded as a link
        * ![Outlook Client favorite icon]({% link microsoft-outlook/images/outlook-search-favorite.png %}){:height="18px" width="18px"} Mark as a favorite
        * ![Outlook Client metadata icon]({% link microsoft-outlook/images/outlook-metadata.png %}){:height="18px" width="18px"} Add metadata for the file or folder. This opens the metadata dialog that was displayed when the file was filed in Share.
        * View the version history of a document. See [Working with file versions](#working-with-file-versions) for more.
        * Check out a document for editing offline.

6. Drag and drop files into the repository. A number of options are available, depending on your configuration settings.

    The options available to you are shown in the right-click context menu. For example, if you have selected a Microsoft Office file, you can edit this online in addition to other standard options. See [Configuring extended settings in Outlook]({% link microsoft-outlook/latest/config/index.md %}#configure-extended-settings) for more information on configuration settings.

    If your IT team has enabled email duplication prevention, the Alfresco Outlook Client will receive information from the server that a particular email document already exists (either in the repository or the site). The following message is presented:

    ![]({% link microsoft-outlook/images/email-duplication-message.png %})

    Select one of the following options:

    * **Open:** Opens the details page of the email in a browser. This is similar to using the **Details** action on an email from the **Explore** tab context menu.
    * **Continue:** Archives the email.
    * **Cancel:** Keeps the original email.
      * If a single email is selected, this cancels the process and closes the dialog.
      * If multiple emails are selected, this cancels the processing of the current email, and starts to process for the next email.

7. Open folders and view files from the **Explore** tab. Depending on your configuration settings and the number of files in your repository, you have the option to see additional files by clicking ![More icon]({% link microsoft-outlook/images/outlook_more_v2.png %})

8. Use **Configure > Extended** from the **Alfresco Client** toolbar to dynamically change the way that the files and folders are displayed.

    For example, this format is displayed when **Folder sort order** is set to date modified (ascending), with **Date sort display options** set to date/time and subject:

    ![The screen capture shows the date/time and subject fields in a site hierarchy.]({% link microsoft-outlook/images/outlook-sort_v2.png %})

    >**Note:** Right click a folder and select **Sort by** and your chosen option to dynamically sort the contents of a folder.

### Workflow options in the Alfresco sidebar

Start workflows using the Alfresco sidebar.

1. Go to the **Alfresco Client** tab on the Outlook toolbar and click **Show Sidebar**.

    This option displays a new window on the right side of the screen, called **Alfresco Outlook Client**.

2. Click the **Workflow** tab:

    1. Use the option list to filter by **My initiated workflows** or **My tasks**.

        You can start and view workflows from the Alfresco sidebar, following rules that are set in Alfresco Share.

        Upcoming appointments and tasks are shown in the left panel.

        >**Note:** In Alfresco Outlook Integration 2.7, the **Workflow** tab is disabled by default. Contact your IT team for further help.

## Managing file versions in Outlook

You can create new versions of files that already exist in Alfresco Outlook Client. There are two ways to trigger versioning for one or more files: implicit and explicit versioning.

* **Implicit versioning**

    Drag and drop one or more files into a site or folder in the Alfresco sidebar, and it will determine if files of the same name already exist.

* **Explicit versioning**

    Drag a file into the Alfresco sidebar and explicitly drop it on an existing file.

In both cases, the Alfresco Outlook Client lets you decide if you'd like to create a new version, rename it on upload, or ignore it.

>**Note:** Versioning only applies to files, so emails can't be versioned. If you add an email with a subject that already exists, in a specific location, you'll be asked to rename it.

### Working with file versions

Create new versions of files by dragging & dropping them into the Alfresco sidebar. You can also review the version history of a versioned file, and revert to a previous version.

1. Click the **Explore** tab from the **Alfresco Outlook Client** sidebar.

2. For implicit versioning: drag and drop one or more files into a site or folder in the Alfresco sidebar. You will see the **Versioning** dialog.

    If one or more files with the same name as the dropped file(s) already exist in that location, only those with the same name and extension are versioned.

    Here is an example **Versioning** dialog:

    ![Outlook version detection - new version]({% link microsoft-outlook/images/Outlook-version-new-ver.png %})

    * The first line indicates the number of files that are available for versioning (in this case, **1 / 3** is 1 of 3 files), and the name of the current file. If you're versioning more than one file, the **Next** and **Previous** options are enabled so that you can page between the files.
    * If you have more than one file, the **Apply to all items** option is enabled and you can apply the information you enter to all items related to that file.
    * Select **Save** to save your changes and begin the upload.
    * If you copy a single file to a folder in Alfresco Share, and then choose the **Cancel** option to stop the transfer, the file will still transfer into Share. The **Cancel** action works best when transferring multiple files. The last transferred file remains in Share, however the other files are not transferred.

    1. Select **New version** to create a new version of a file.

        Choose to save either a **Major** or **Minor** version.

        Add a **Version comment** (optional).

    2. Select **New document** to create a new file.

        ![Outlook version detection - new document]({% link microsoft-outlook/images/Outlook-version-new-doc.png %})

        The existing file won't be versioned. An index number is automatically added to the file name to avoid naming conflicts, but you can change this before saving.

        For example, if the original file is `1.pptx`, the suggested file name for versioning is given as `1-0001.pptx`.

    3. Select **Skip** to prevent the file from being uploaded to Share.

    Select an action for each file listed in the Versioning dialog.

    >**Note:** You might see a **Metadata** dialog if this has been configured by your IT team. Enter the information needed for archiving. See [Archiving content in Outlook](#archiving-content-in-outlook) for more details.

    See [Outlook metadata settings]({% link microsoft-outlook/latest/config/index.md %}#configmetadataandlistview) for metadata configuration guidance.

3. For explicit versioning: drag and drop a single file onto an existing file in the Alfresco sidebar. You will see the **Versioning** dialog.

    >**Note:** Both files must have the same extension.

    1. Hover your mouse over the file that you'd like to version for a few seconds.

        ![Outlook versioning - explicit]({% link microsoft-outlook/images/Outlook-version-explicit.png %})

        The file is highlighted with a blue bar. In this example, `1.txt` will be versioned.

        >**Note:** You can only version one file at a time using explicit versioning. Use implicit versioning to version multiple files.

    2. In the **Versioning** dialog, follow the same steps as described earlier for implicit versioning.

    You can review the version history of a versioned file by using the context menu.

4. Right click on a versioned file and select **Version history**.

    ![Open version history]({% link microsoft-outlook/images/Outlook-version-history.png %})

    This open the Version History dialog with several options:

    ![Outlook version history dialog]({% link microsoft-outlook/images/Outlook-version-history-dialog.png %})

    * **Download** - allows you to download any version of a file
    * **Revert...** - allows you to revert to a previous version
    * **More** - displays the properties (or metadata) for a file

        ![More option in Outlook version history dialog]({% link microsoft-outlook/images/Outlook-version-history-more.png %})

    To revert a file to a previous version, follow these steps.

    1. Click **Revert...**.

        A Revert Version dialog opens.

        ![Revert version dialog]({% link microsoft-outlook/images/Outlook-version-revert.png %})

    2. Click **Major** or **Minor** to revert your file to a previous major or minor version.

    3. Enter a **Version comment** or keep the pre-filled content.

    4. Click **Revert**.

        This replaces the content and metadata from the current version with the previous version.

    You can also check out a file by using the context menu.

5. Right click on a file and select **Checkout**.

    A working copy of your file is created that you can download and work offline. The original file is locked, so you can work on the content, while other users can't edit it until you check it back in. When you've finished working on the file and saved the changes, check in the file to create a new version. Alternatively, you can cancel the check out to abandon any changes to the file, and restore the original.

    If you add an email with a subject that already exists in a specific location, you'll be asked to rename it.

6. Drag and drop an email into a site or folder in the Alfresco sidebar.

    The **Versioning** dialog is displayed if an email with the same name already exists in the upload location.

    >**Note:** The **New version** tab is greyed out, and a warning message is displayed as you can't version emails.

    ![Email uploaded as new document]({% link microsoft-outlook/images/Outlook-email-upload.png %})

    1. In the **New document** tab, an index number is automatically added to the email subject (or name) to avoid naming conflicts, but you can change this before saving.

    2. Select **Save** to save your changes and begin the upload.

        Select **Skip** or **Cancel** to prevent the email upload.

    The original email remains in the selected location.

## Uploading folders in Outlook

You can drop folders from Windows Explorer onto the Alfresco Outlook Integration.

1. Archive a folder by dragging and dropping it into a folder in your chosen site.

    You might see a **Metadata** dialog for the folder (if this has been configured by your IT team).

2. Enter the information needed for archiving the folder.

    After saving, you may see a second **Metadata** dialog showing all files for all folders (if this has also been configured by your IT team).

The upload starts after saving. This operation runs in the background until it's completed. While the upload is running, you can't upload any other files.

* To indicate that the process is still running, you'll see a progress bar in your Outlook plugin with the option to **Cancel** the upload.
* For every folder created (with associated files), you may see an email duplication dialog if your folder contains emails that have already been uploaded to the system.
* Once the operation is complete, the Outlook plugin will display the files that haven't been uploaded if there was a problem with uploading some of your data.

## Managing archived files in Alfresco Share

View your archived emails in Alfresco Share, just like any other files in Alfresco. Email filters allow you to search for the archived emails in a site or across Alfresco Repository.

In the simple Alfresco view, view the properties of each archived email. In the detailed Alfresco view, HTML and rich text emails, and attachments are displayed as a color preview.

In Document Actions, send a link to the email in Alfresco by selecting the **Email as link** option. Also, if a MSG file is saved, open it using the **MSG file** button in the preview. All other options remain available.

Use the advanced Alfresco search to find archived emails by using the option **Look for: Emails** from the Advanced Search toolbar.

## Troubleshooting the Outlook Integration

Use this information to help troubleshoot Alfresco Outlook.

### Error when using a hybrid workflow in Alfresco Outlook

There's a known issue when using hybrid workflows in Alfresco Outlook (`hybridworkflow.enabled=true`). This function is currently not available in Alfresco Outlook Integration, and you will receive an error message when you attempt to start a new workflow in the Outlook Client:

```text
An error has occurred in this dialog.
Message: 66
Unspecified error.
```

### File transfer is not cancelled when instructed

In the Alfresco Outlook Client, if you copy a single file to a folder in Alfresco Share, and then decide to cancel the transfer, the file will still transfer into Share. This is because unless the client-server connection is very slow or the file is very big, the file transfers too quickly to be cancelled. The Cancel action works best when transferring multiple files - the last transferred file will remain in Share, however the other files will not be transferred.

### Unable to connect to Alfresco Share message

In the Alfresco Outlook Client, you might see a message indicating that you can't connect to Share. This is either because your repository is not running, or you have issues with your setup. From the toolbar, check that your sign in details are correct in **Configure > Connection** and click **Check connection**. You can also enable debugging in **Configure > Extended** to get more information on the issue. You will need to provide this log if you need Alfresco Support to resolve your issue.

### Error on write access from Alfresco Outlook Client to Records Management site

The Alfresco Outlook Client no longer permits direct write access to a Records Management site. All create and edit related actions in the context menu aren't visible for content in this site. However, the Alfresco Outlook Client still supports read access in the following cases:

* Search content in the Records Management site from the Alfresco Outlook Client
* Attach links or binaries from the Records Management site to email
* Download content from the Records Management site

### Error when declaring a record from within Alfresco Outlook Client

In the Alfresco Outlook Client, you might see a message stating that you can't declare a record from within the client. This action is no longer supported. However, you can declare content in a collaboration site as a record (i.e. create an inline record).
