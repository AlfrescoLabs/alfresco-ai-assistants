---
title: Alfresco Office Services
---

Alfresco Office Services (AOS) allows you to access Alfresco directly from your Microsoft Office applications.

Installing Alfresco Office Services allows Microsoft Office Suite applications (for example, Word, PowerPoint, and Excel) to interact with Alfresco similar to SharePoint. This feature allows you to edit Office documents in Alfresco Share and to modify Office files without checking them in and out. Alfresco locks the file while it is being modified and releases the lock when the file is saved and closed.

It is important to note the URL required to access Alfresco from a Microsoft Office application. For more information, see [Using Alfresco from Microsoft Office]({% link microsoft-office/latest/using/index.md %}). The following diagram shows the architecture of AOS in relation to an Alfresco installation:

![Office Services architecture]({% link microsoft-office/images/architecture.png %})

Communication is over HTTP with either the repository (through Alfresco Share) or directly from a Microsoft Office application.

If you are using a proxy server to handle SSL communication, the proxy handles the communication with Share and Microsoft Office through an AJP port (if you are using Tomcat). For more information about setting up a proxy server, see [Configuring SSL]({% link content-services/latest/config/repository.md %}#ssl-repo). The architecture is as follows:

![Office Services proxy architecture]({% link microsoft-office/images/architecture-proxy.png %})

AOS replaces and enhances the Microsoft SharePoint Protocol Support that was available in previous versions of Alfresco.

## Considerations when using Alfresco Office Services

There are some dependencies that you might encounter when using Alfresco Office Services (AOS).

* AOS relies on SSL to allow communication with the repository:
  * You must activate SSL when using Alfresco Office Services. For more information, see [Configuring SSL]({% link content-services/latest/config/repository.md %}).

    If you are using a proxy server to handle SSL, make sure that the proxy is not filtering requests to Alfresco. For more information on proxy SSL configurations, see [Configuring SSL in a production environment]({% link content-services/latest/config/repository.md %}#ssl-prod).

  * There are some limitations when using the Alfresco `external` authentication subsystem. External authentication can work well when using a web browser client, but not when using the MS Office client. This is because no authentication information is sent with the file URL, and MS Office does not store authentication information, so starts a new authentication process. An example of this is when using CAS. CAS authenticates using an HTML form and a web browser that follows an HTTP redirect. The web authentication works correctly, but MS Office authentication will not work because it does not permit completion of the form. This problem is caused by the limited set of authentication protocols that MS Office supports.

    MS Office supports the following authentication mechanisms:

    * HTTP Basic
    * HTTP Digest (NTLM, Kerberos)

    NTLM and Kerberos can be used in an SSO environment.

  * There is limited support for AOS with Microsoft Office for Mac. It is a known problem that there is no property mapping function in Microsoft Office for Mac.
* AOS is installed by default during the standard Alfresco installation:
  * If you are installing the repository manually, you'll need to install the Alfresco Office Services AMP file. See the guidance in [Install an Alfresco Module Package]({% link content-services/latest/install/zip/amp.md %}) for more information.
  * If you have a custom application that is running at the server root directory, it is important that you merge the `_vti_inf.html` and `index.jsp` files into this application to enable AOS. For more information, see [Install into an existing web application]({% link microsoft-office/latest/install/index.md %}#installing-into-an-existing-web-application).
* AOS interacts very closely with Microsoft Office, and there are some implications as a result:
  * Alfresco simulates a SharePoint Site in the `/alfresco/aos` directory and uses the child folder to represent the SharePoint document library. As a result, Office does not check out documents in the repository root; that is, if your document is located in `/alfresco/aos`. Make sure that you add a child folder in the `/alfresco/aos` directory and place documents there. For example:

    ```bash
    http://localhost:8080/alfresco/aos/documents/doc1.docx
    ```

* Alfresco and Office handle property mapping and time values differently:
  * Alfresco and Microsoft use different mechanisms to calculate Daylight Saving Time (DST). In Alfresco, DST is applied to dates; for example, a time in August is displayed in DST, but a time in November is displayed without DST. Microsoft applies DST to all dates depending on the current date. For example, if today is in August, the time values of all dates are displayed in DST, even a time in November. This means that if you are looking at a date six months away, there is a one-hour difference between the time value displayed by Alfresco and the time displayed in Microsoft Office. This mechanism is used across Microsoft products; for example, the same behavior is visible in the last modified timestamp in Windows Explorer.
  * Date values are represented by Microsoft Office and Alfresco as `DateTime` values with the time zeroed out (for example, `03.09.2014 00:00:00`). After applying time zone conversion to this value, the date might change to the previous or next day. For example, if you are storing `03.09.2014 00:00:00` in `UTC+2` and then reading the value in `UTC-1`.
  * If mapped properties are embedded into an `OOXML` file (for example, a `.docx` file), time values are displayed in the user's timezone. Properties embedded into `OLE` files (for example, `.doc` files) are displayed in Coordinated Universal Time (UTC).
  * There are known issues with decimal numeric values (float and double) in non-English versions of certain Office products and if Office runs with a non-English regional setting.

See [Troubleshoot Alfresco Office Services]({% link microsoft-office/latest/admin/index.md %}) to resolve any other issues you might have.
---
title: Troubleshoot Alfresco Office Services
---

Use this information to troubleshoot common Alfresco Office Services issues.

## Issue with protected view (Office 2016 for Windows)

There is a known issue with Office 2016 for Windows, when switching from the protected view into editing mode. Microsoft Office falsely detects file changes on the server and attempts to merge local changes with server changes. After discarding a check out, Office does not reload the file from the server and still displays the version of the file that has just been discarded.

We recommend that you turn off the protected view, by adding your server in the trusted sites or local intranet zone, or alternatively by deactivating the protected view in Office. You can deactivate the protected view by selecting Options, and Word Options, then Trust Center. Select Trust Center Settings and Protected View, and deactivate all settings. Save your changes.

## Issue with immediate editing after checking in a file (Office 2016 for Mac)

There is a known issue in Office 2016 for Mac, if you edit a file immediately after checking the file in. You'll see an error message saying that the file cannot be modified. The workaround is to wait a minute, and try the edit again.

## Issue with Online Editing

There is a known issue where Online Editing is not available using the 64-bit version of Internet Explorer. See [Plan browser support (SharePoint Server 2010)](https://docs.microsoft.com/en-us/previous-versions/office/sharepoint-server-2010/cc263526(v=office.14)?redirectedfrom=MSDN){:target="_blank"} for more information.

## Error message: "The address is not valid" when connecting to `http://server:port/alfresco/aos`

If you have installed Alfresco manually or upgraded from a previous version of Alfresco, you might not have installed the Alfresco Office Services AMP file. If that is the case, you will receive an error message "The address is not valid" when you try to connect and authenticate with the address: `http://server:port/alfresco/aos`. You will also see the following error message in the server log:

```text
Blocked a directory listing request from MS-Office. This indicates a broken MS-Office
deployment. Please check that the ROOT and the _vti_bin webapps are deployed properly and
reachable from the outside!
```

To fix this problem, ensure that you have installed the Alfresco Office Services AMP file, and deployed the `_vti_bin.war` file that is required for AOS to work correctly.

See [Install Alfresco Office Services]({% link microsoft-office/latest/install/index.md %}) for more.

## Missing version history and check in/ check out options in Office

If you cannot see certain fields in the Document Panel in your Microsoft Office applications; for example, version history, check out and check in history, or you cannot see a directory listing for a file, it might be that your ROOT and `_vti_bin` files have not been deployed properly, or you have not applied the Alfresco Office Services AMP file, if you have installed Alfresco manually.

To check whether this is the case, try to open the ROOT and `_vti_bin` files from a browser. In these examples, replace `server:port` with your server and port details.

If you type:`http://server:port/`, you will see a message **Welcome to Alfresco!**.

If you type: `http://server:port/_vti_inf.html`, you will see a blank page. Select Show page source in the browser to see `_vti_bin ScriptUrl` information.

If you type: `http://server:port/_vti_bin/`, you will see a message Welcome to Alfresco! This is the `/_vti_bin` application. This application does not provide a web interface in the browser..

If these files and messages are not available from the browser, then AOS has not been deployed properly.

See [Install Alfresco WARs]({% link content-services/latest/install/zip/tomcat.md %}#install-alfresco-wars) for information on where the deployed `ROOT` and `_vti_bin` WAR files need to be located. If `_vti_bin.war` does not exist, you'll need to reinstall the Alfresco Office Services AMP.

## Extra files created when mounting AOS using WebDAV and Mac Finder

Do not mount the AOS repository root (`alfresco/aos` or any sub folder) as a WebDAV folder with Mac Finder. Otherwise you might see extraneous files in Alfresco Share; for example, files prefixed with the characters `._`.

## Microsoft path length limitation

Microsoft Office has a general path length limitation of 250 characters. This affects any external application interacting with Office, not just AOS. Office can handle more than 250 characters in many cases, but Microsoft does not provide official support in these circumstances. These are problems that you might encounter if you use long paths:

* Office reports that a document cannot be registered and OLE linking is deactivated (due to the path length limitation in OLE)
* The browser plug-in does not open a document

Avoid deep folder structures and path lengths over 250 characters, or if you must use long path lengths, test extensively with Office before deploying to a production environment.

## File dialog in Microsoft Office shows file listing instead of graphical view

For untrusted servers, Microsoft Office blocks the graphical web view of files and instead shows the files as a list.

To solve this problem, either:

* On each client machine, in Internet Options or Internet Accounts, add the server in the list of trusted sites
* On your local intranet, modify the rules used to identify servers to include your server

## Check in failure

There is a known problem if property mapping is activated and, in a single MS Office session, you create a new file with the Save As option, then check it out and check it back in. The check in will fail in this situation.

To avoid this problem, upgrade to Alfresco, or exclude read-only mandatory properties from the property mapping.

The problem is caused when some mandatory fields are not filled out, but are declared as read-only. This is typically caused by system properties (for example, Creator or Modifier) that come with some system aspects. You can avoid this by overwriting the includedAspectsPatterns configuration to include specific custom aspects only.

## Property mapping failure with Office 2013 and Windows

If you are using Office 2013 and are working with an OLE file (for example, `.doc`, `.xls`, or `.ppt` files), and the Protected View is activated for the document, then property mapping can fail even after switching into Editing Mode.

To resolve this problem, you need to prevent the Protected View in Office by adding the repository server to the list of trusted sites.

## Values of date fields in OLE documents not stored

Values of `Date` and `DateTime` fields are not set in OLE documents (for example, `.doc`, `.xls`, or `.ppt` files) if the time zone of the client machine is greater than UTC+1. If these `Date` or `DateTime` fields are declared as mandatory, then you will not be able to save document changes.

To resolve this problem, you need to either set `Date` and `DateTime` as optional fields, or ensure that the time zone is not greater than UTC+1.

## Problems deploying AOS on JBoss

If you use the JBoss application server, you must customize the `web.xml` file in the Alfresco `ROOT.war`, `_vti_bin.war` and `share.war` files to include this code fragment:

```xml
<context-param>
   <param-name>
      org.jboss.jbossfaces.WAR_BUNDLES_JSF_IMPL
   </param-name>
   <param-value>true</param-value>
</context-param>
```

This ensures that the JSF deployer in JBoss uses its own bundled JSF version.

## Fixing 'Edit in Microsoft Office' Issue with AOS when SSO is enabled

### Problem:

After installing AOS module (amp), when user clicks on 'Edit in Microsoft Office Action' (Inline Edit) from 'document-browse' action menu or 'document-details' action menu, following behavior has been noticed:

 - User will see a blank Office application (Word or Excel application without content being displayed)
 - User might be able to open document but will see an error popping-up saying 'Cannot download requested content'

### Cause of the issue:

When user tried to open a document, Microsoft Office Application (AOS) tries to establish a connection from client machine to the alfresco repository server and tries to validates the client certificate that matches with alfresco repository server. This uses Crypto API calls to match certificate using certificate fingerprint.

### Solutions:

Follow the steps outlined below to fix the aforementioned issue:

#### Generating the PKCS12 certificate using JKS certificate:

   - Download certificate from server which is used to configure SSL in tomcat (If certificate has a password then get the password for the root certificate from your certificate provider).
   - Execute command given below to generate the PKCS12 format (.p12) which needs to be imported into client personal certificates:

      ```
      keytool -importkeystore -srckeystore {path_to_JKS_cert} -destkeystore {desired_path_for .p12} -srcstoretype JKS -deststoretype PKCS12 -deststorepass {your_password}
      ```
      1. During the course of the process, you will be prompted to provide the root certificate password (only for the first time). Please provide the root certificate password.
      2. Secondly, you will be prompted to provide a password for `.p12 certificate` (that is being generated). Provide a desired password as per your password policy.
      3. Certificate will be generated and saved to the location of your choice. Keep the newly generated .p12 certificate handy for next steps.


#### Installing the certificate:
   
   1. Use `.p12 certificate` that was generated in previous steps to import into the client machine.
   2. Search for Run Application in your system or press `windows + r` to open run manager.
   3. Enter command `certmgr.msc` and press OK/Enter. You will see certificate manager dialog. See screenshots below.

      
      ![AOS Certificate Fix]({% link microsoft-office/images/run-command-dialog.png %})


      ![AOS Certificate Fix]({% link microsoft-office/images/certificate-manager-dialog.png %})


   4. Click on `Personal` -> `Certificates`
   5. Right click on `Certificates` -> `All Tasks` -> `Import` , To open the certificate import wizard.


      ![AOS Certificate Fix]({% link microsoft-office/images/import-personal-cert-dialog.png %})


   6. Select `.p12 certificate` from your computer and click on `Next`. See screenshots below.

      
      ![AOS Certificate Fix]({% link microsoft-office/images/import-personal-cert-select-dialog.png %})


      ![AOS Certificate Fix]({% link microsoft-office/images/import-personal-cert-selected-dialog.png %})


   7. At this step, you will be see an option to provide a password in certificate import wizard. Provide the password you choose during the PKCS12 certificate generation step (see 2nd point in the generate certificate section) and click `Next`.


      ![AOS Certificate Fix]({% link microsoft-office/images/personal-cert-pass-prompt.png %})


   8. Keep the selection as is to place the certificate in Personal store. 

      ![AOS Certificate Fix]({% link microsoft-office/images/import-personal-cert-saveas-personal.png %})


   9. At this step, the dialog will show the selected `.p12 certificate` path and  `Personal` store as you selected above. Click `Finish` to complete the import process and then Click `OK` to close the prompt. See screenshots below.


      ![AOS Certificate Fix]({% link microsoft-office/images/import-personal-cert-finish.png %})


      ![AOS Certificate Fix]({% link microsoft-office/images/import-personal-cert-finalized.png %})


   10. You should be seeing the "The import was successful" message and newly imported Certificate will be visible in the certificate manager.

   11. Test the 'Edit in Microsoft Office' and it should be working again.




   


   
---
title: Configure Alfresco Office Services
---

You can configure AOS for your environment with a global path to access Alfresco, and you can configure property mapping for injecting custom properties and metadata into Office documents.

## Setting up a global filepath to access Alfresco

In Windows Explorer, you can set up a Group Policy to manage Favorites on client machines, or share a .lnk file in your Links folder. This can be useful if you want to preconfigure the folder that users will need to access the repository from Microsoft Office (`http://servername:port/alfresco/aos`).

On a Windows 7 machine, the contents of Favorites in Windows Explorer is assembled from the .lnk files in `C:\Users\username\Links`. You can create a `.lnk` file in your `Links` folder and distribute this to the `Links` folder of other users, or preferably, you can use a Group Policy to manage Favorites on user machines.

To use a Group Policy:

1. In the Group Policy Management Console, navigate to `User Configuration\Preferences\Window Settings\Shortcuts`.

2. Create a new shortcut (Group Policy Object) to a folder (not a link to a URL) with the following UNC target path:

    ```bash
    \\servername@SSL\DavWWWRoot\alfresco\aos
    ```

    Alternatively, you can specify `@port` instead of `@SSL`, but not both. The default port is `443`.

    For more information, see [Configure a Shortcut Item](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc753580(v=ws.11)?redirectedfrom=MSDN){:target="_blank"}.

## Configuring mapping properties in Alfresco Office Services

Property mapping in AOS allows you to inject custom properties and metadata into Office documents. Property mapping is deactivated by default. Follow these instructions to activate property mapping.

Property mapping is different from the standard metadata extraction mechanism and should be carefully configured to ensure that different properties are set up. Properties stored in the repository are injected into Office documents when these files are read through AOS, and equally properties are extracted from Office files written through AOS and then updated in the repository.

> **Note:** Injected properties form part of the document. If the document is removed from the organization, for example, anyone outside the organization reading the document can view all the properties that have been mapped into the document.

> **Note:** Property mapping in Alfresco Office Services doesn't work for password protected Microsoft Office Open XML files and will generate an exception. To ignore property mapping for password protected Microsoft Office Open XML files, set the property `aos.contentFilter.ignoreOOXMLProtected=false` in the `alfresco-global.properties` file.

Take note of the following:

* Single value properties only can be mapped in Office documents. Multi-value properties are ignored.
* Accepted data type properties are `text`, `mltext`, `int`, `long`, `float`, `double`, `date`, `datetime` and `boolean`. Other data type properties are ignored.
* The following constraints are supported: `MINMAX` for numeric data types, `LENGTH` for text, or `LIST` for text. Properties that have other constraints are ignored; for example, `REGEX` for text.
* Property mapping is only available for OOXML files (`.docx`, `.xlsx`, `.pptx`) and OLE files (`.doc`, `.xls`, `.ppt`). OLE files do not support read-only properties and are ignored. Protected properties are available in OOXML files only.

If any ignored properties are declared as mandatory, then users will not be able to save documents.

It is possible to define a list of types for new documents. Whenever a user creates a new document with the **Save As** dialog, Microsoft Office displays this list to choose from. If the type contains mandatory properties, Office enforces values for these properties before the file can be saved. Files created outside of Office (for example, in Windows Explorer) are created with a type of `cm:content`.

Alfresco provides basic configuration of four patterns, `includedTypesPatterns`, `excludedTypesPatterns`, `includedAspectsPatterns` and `excludedAspectsPatterns` in the `aosBaseDataModelMappingConfiguration` abstract bean.

1. Rename or copy the `<classpathRoot\>/alfresco/extension/custom-aos-metadata-mapping-context.xml.sample` file to `<classpathRoot\>/alfresco/extension/custom-aos-metadata-mapping-context.xml`.

    This sample configuration file activates metadata mapping for the basic `cm:content` type and all its sub-types, except for some system types. All type properties and all applied aspects (except for some system aspects) are mapped into the documents.

2. In `custom-aos-metadata-mapping-context.xml`, check your file type based on the `includedTypesPatterns` and `excludedTypesPatterns` properties.

    Both properties contain a list of regular expressions that are applied to the fully qualified QName. A file is valid for property mapping if its type is accepted by one of the regular expressions in the `includedTypesPatterns` list and does not exist in the `excludedTypesPatterns` list. For more information on regular expressions, see [Class pattern](https://docs.oracle.com/javase/7/docs/api/java/util/regex/Pattern.html){:target="_blank"}.

3. In `custom-aos-metadata-mapping-context.xml`, check the file aspects based on the `includedAspectsPatterns` and `excludedAspectsPatterns` properties.

    If a file is valid for property mapping, aspects applied to this file are filtered further depending on the two properties, `includedAspectsPatterns` and `excludedAspectsPatterns`. Property mapping occurs only if the file type is included in the `includedTypesPatterns` list (even if there are aspects that are included in the `includedAspectsPatterns` property).

4. In `custom-aos-metadata-mapping-context.xml`, check the `includedInstantiableTypesPatterns` and `excludedInstantiableTypesPatterns` properties.

    These properties define the list of types that are available to users for document creation in the **Save As** dialog. If the `includedInstantiableTypesPatterns` is empty or not set, new documents are always created with the default type. If no system type matches the types configured in `includedInstantiableTypesPatterns`, the base type `cm:content` is used by default. If exactly one type matches the configuration, this type is automatically used for all documents created with the **Save As** dialog in Microsoft Office.

## Configuring secure authentication with Identity Service

You can configure AOS to seamlessly integrate with Identity Service, disabling Basic Authentication and relying on Identity Service instead to perform the authentication when leveraging AOS capabilities.

Assuming Identity Service is properly installed and configured, the `authentication.chain` property should already be defined and should include an authentication chain component of type `identity-service`. For example:

```text
authentication.chain=identity-service-1:identity-service,alfrescoNtlm-1:alfrescoNtlm
```

To integrate AOS and Identity Service, it is sufficient that the `authentication.chain` property defines an authentication chain component of type `identity-service` as the first available component.

It is now possible to perform the secure authentication via Identity Service when editing documents in Microsoft Office through Alfresco Content Services.

You can still access the AOS endpoints via a web browser as long as the secure authentication has been performed first by visiting the following URL (assuming the Alfresco Content Services host name is `repo.example.com`):

```text
https://repo.example.com/alfresco/service/aos/authenticate
```

> **Note:** The duration of the authenticated session will be affected by the session timeouts configured within Keycloak.
---
title: Install Alfresco Office Services
---

If you deploy Alfresco using containerized deployment, AOS is already pre-installed in our Docker images. Use this information to install the repository manually, or for installing into an existing Alfresco instance.

Installing Alfresco Office Services allows Microsoft Office Suite applications (for example, Word, PowerPoint, and Excel) to interact with Alfresco similar to SharePoint. This feature allows you to edit Office documents in Alfresco Share and to modify Office files without checking them in and out. Alfresco locks the file while it is being modified and releases the lock when the file is saved and closed.

## Prerequisites for using Alfresco Office Services

There are a number of software requirements for using AOS.

Alfresco Office Services is part of the standard Alfresco installation, and software and hardware requirements are the same as those for Alfresco. See [Supported platforms]({% link microsoft-office/latest/support/index.md %}) for more information.

* Microsoft Office 2016 for Windows (boxed version)
* Microsoft Office 2016 for Mac (boxed version)
* Office 365 Desktop Version for Windows v16 (through subscription)
* Office 365 Desktop Version for Mac v15 (through subscription)
* Microsoft Office 2013 (32 or 64-bit)

> **Note:** You must activate SSL when using Alfresco Office Services 1.2 or above. For more information, see [Configuring SSL]({% link content-services/latest/config/repository.md %}#ssl-repo).

In the latest Microsoft Office versions, such as Microsoft Word for Microsoft 365 and Microsoft Office (Version 2401 Build 16.0.17231.20236) 64-bit, Microsoft has removed the ability to use basic authentication in Exchange Online for Exchange ActiveSync (EAS), POP, IMAP, Remote PowerShell, Exchange Web Services (EWS), Offline Address Book (OAB), Autodiscover, Outlook for Windows, and Outlook for Mac.

> **Note:** To make Alfresco Office Services work with the latest versions of Microsoft Office, you must either:
>
> * Use IdP-initiated Single Sign On (IdP/SSO), since basic authentication is not supported in the latest Microsoft Office versions.
> * Downgrade Microsoft Office to a version where basic authentication is supported.

## Installing manually using the AMP file

To install manually into an existing Alfresco instance, you use the AOS AMP file.

> **Note:** If you deploy Content Services using containerized deployment, AOS is pre-installed in the Docker images.

1. Install the AMP file `alfresco-aos-module-3.0.x.amp`. See [Installing an AMP]({% link content-services/latest/install/zip/amp.md %}) for information about installing an AMP file.

2. Deploy the `_vti_bin.war` file.

    For Tomcat, copy the file to the `tomcat/webapps` folder. When the server starts up, it deploys the WAR file automatically.

    > **Important:** If the `_vti_bin` folder already exists under `tomcat/webapps` (for example, in the case of an upgrade), then remove the folder first, otherwise the new WAR file won't be deployed.

## Install into an existing web application

If you install Alfresco manually, you must deploy the `ROOT.war` application to the server root. If you already have an application running in the server root, you can merge the Alfresco function into your existing web application.

The `ROOT.war` application is required to enable Alfresco Office Services (AOS). If you have a custom application that is running in the server root directory, it is important that you modify this application to enable AOS.

There are two types of requests that are sent to the server root directly by Microsoft Office and Windows:

1. A request for the `_vti_inf.html` file that contains configuration information
2. `OPTIONS` and `PROPFIND` requests

The following diagram shows the information flow between Microsoft Office and Alfresco, including interactions with the `/alfresco`, `_vti_bin` and `ROOT` applications:

![How it works]({% link microsoft-office/images/howitworks.png %})

1. Extract the `_vti_inf.html` file from the `<TOMCAT_HOME>webapps/ROOT.war` archive file and add it to your web application.

2. In your web application, modify the service that responds to requests to the server root, so that it sends `PROPFIND` and `OPTIONS` requests to the /alfresco application.

    If you have a `.jsp` page responding to the server root, you can add this code example to that page:

    ```java
    <%
    if(request.getMethod().equals("PROPFIND") || request.getMethod().equals("OPTIONS"))
    {
      ServletContext alfrescoContext = application.getContext("/alfresco");
      if( (alfrescoContext != null) && !alfrescoContext.equals(getServletContext()) )
      {
         RequestDispatcher rd = alfrescoContext.getRequestDispatcher("/AosResponder_ServerRoot");
         if(rd != null)
         {
                 rd.forward(request, response);
                 return;
         }
      }
    }
    %>
    ```

    and add this import statement to the top of the `.jsp` page:

    ```java
    <%@page session="true" import="javax.servlet.ServletContext, javax.servlet.RequestDispatcher” %>
    ```

    If you have deployed alfresco to a different context path (something other than `/alfresco`), make sure that you edit the `application.getContext` value to represent this.

    If you have a servlet responding to these requests, integrate the Java code from these JSP code examples into your application.

3. Depending on your application server, ensure that requests are dispatched by default between different application servers.

    For Tomcat, add a file called `context.xml` to the META-INF directory of your web application. Here is an example of the `context.xml` file:

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <Context path="/" debug="100" privileged="true" reloadable="true" crossContext="true">
    </Context>
    ```
---
title: Supported platforms
---

The following are the supported platforms for Alfresco Office Services:

| Version | Notes |
| ------- | ----- |
| Content Services 23.2 | |
| Community Edition 23.2 | |
---
title: Upgrade Alfresco Office Services
---

Use this information to upgrade from a previous version of AOS.

1. [Upgrade Alfresco]({% link content-services/latest/upgrade/index.md %}).

    > **Note:** Make sure that you install the `alfresco-aos-module-3.0.x.amp`, and deploy the `_vti_bin.war` file.

    See [Install Alfresco Office Services]({% link microsoft-office/latest/install/index.md %}) for more information.

2. Launch Alfresco Share.

    Test that you can edit your Microsoft Office documents by using the **Edit in Microsoft Office** action on any Office document in Alfresco Share.

3. Alternatively, open a Microsoft Office application (for example, Word) and select the **File** tab and **Open**. Enter the Alfresco server address in the **File name** field in the format: `http://servername:portnumber/alfresco/aos` and browse to a folder to edit an Office document.

    Any version history from the previous version of Alfresco will not be available in Microsoft Office, but is available in Alfresco Share.
---
title: Using Alfresco from Microsoft Office
---

When using Alfresco Office Services (AOS) you can access your files from Content Services directly from your Microsoft Office applications.

This means that you can browse, open, and save Microsoft Office files (Word, PowerPoint, and Excel) in Content Services without the need to go through Chrome, Firefox, or another web browser.

You can also browse Content Services from Windows Explorer, or you can map a network drive.

This is done by entering a web address for Content Services from Microsoft Office applications, with an AOS-specific ending.

To connect to Content Services, the URL needs to end in `/alfresco/aos`, so if your Alfresco address is `https://mycompany.com` then you'd enter `https://mycompany.com/alfresco/aos/`.

Depending on whether you're using Windows or Mac, there are a few differences to how you do this, and you'll need to be online.

> **Note:** Alfresco administrators can find out more about [installing AOS]({% link microsoft-office/latest/install/index.md %}).

There are lots of ways that using Alfresco from Microsoft Office will help you to work more efficiently, so here are a few examples.

![AOS properties]({% link microsoft-office/images/save-dialog.png %})

## Opening Content Services files from Microsoft Office (Windows users)

You can open files stored in Content Services directly from Microsoft Office applications.

1. Open a Microsoft Office application, such as Word, PowerPoint, Visio, or Excel.

2. Click **File** then **Open**.

3. Enter the Content Services address URL where the file is stored. The URL needs to end in `/alfresco/aos`, so if your Alfresco address is `https://mycompany.com` then you'd enter `https://mycompany.com/alfresco/aos/`.

    You can enter URLs that are specific to a site, folder, or file, for example, `https://mycompany.com/alfresco/aos/Sites/sitename/documentLibrary/foldername/filename`.

    * Site or folder-specific URL - browse through the site or folder to find the file you want
    * File-specific URL - open the file directly
4. Browse through the structure to find the file you want to open and click **Open**.

    > **Note:** You might also need to select **Enable Editing**.

    The file opens and you can work with it as you would with any other Microsoft Office file. It's locked to other Alfresco users until you close it, and every time you save it a new version number is created in Alfresco.

    > **Note:** Once you've opened a file you can quickly access it again by selecting **Open** then **Recent Places**.

## Mapping a network drive to Alfresco (Windows users)

You can map a network drive to Alfresco so that you always have easy access to your files.

Make sure that you have an internet connection and the Alfresco URL. These instructions also require HTTPS to be set up by your administrator.

> **Note:** There are various ways to map a network drive, which may vary slightly depending on which version of Windows you're using.

1. In Windows Explorer, select **Map network drive** using your preferred method.

2. Enter the Alfresco address as the folder or target. Make sure that the address ends in `/alfresco/aos`.

3. When prompted enter your Alfresco user name and password and click **Finish**.

You can now browse Alfresco and work with files through Windows Explorer without the need to access Alfresco through Chrome, Firefox, or another web browser. You can also create new files and save them to Alfresco through the mapped network drive.

## Opening Alfresco files from Windows Explorer (Windows users)

You can open files stored in Alfresco directly from Windows Explorer.

You can do this by either mapping a network drive to Alfresco or by entering a modified URL into the Windows Explorer address bar.

1. Open Windows Explorer and in the address bar, enter the Alfresco URL where the file is stored. This needs to be entered in a different way to when you're mapping a network drive or opening a file from Microsoft Office.

    If your Alfresco address is

    ```bash
    https://mycompany.com`
    ```

    then you'd enter

    ```bash
    \\mycompany.com@SSL\DavWWWRoot\alfresco\aos
    ```

2. If prompted enter your Alfresco user name and password.

You can now browse Alfresco and work with files through Windows Explorer without the need to access Alfresco through Chrome, Firefox, or another web browser.

## Connecting to Alfresco from a Mac (Mac users)

Microsoft Office 2016 for Mac connects to OneDrive to access your Alfresco files.

If you have Microsoft Office 365, you can download Office 2016 (Desktop edition). Your subscription is connected to your Microsoft email account.

1. When you open Word, for example, click your initials in File Options to see your account email, and your connected services.
2. Click Open to see where you can open files. For example, you automatically have access to OneDrive to sync your files to your computer.
3. Click + to add a new service. You can map to a SharePoint drive by the SharePoint AOS URL, for example:

    ```bash
    https://mycompany.com/alfresco/aos/
    ```

4. You can then browse your Alfresco files in the same way that Windows users can access them from Windows Explorer.

Alternatively, for earlier versions of Office, Microsoft Document Connection can be used to access Alfresco files. You'll find it with the rest of your Microsoft Office apps in your Applications folder.

> **Note:** Microsoft Office for Mac does not support Kerberos protocol as a method of authentication. Document Connection is not shipped with Microsoft Office 2016, so can only be used with earlier versions of Microsoft Office.

If you are using Microsoft Office 2016, and do not have OneDrive, see [Microsoft OneDrive](https://support.microsoft.com/en-us/office/sync-files-with-onedrive-on-mac-os-x-d11b9f29-00bb-4172-be39-997da46f913f?ui=en-us&rs=en-us&ad=us){:target="_blank"} for information about how to enable this.

If you are using earlier versions of Office, you can set up Microsoft Document Connection.

1. Click **Document Connection** on the Mac toolbar then **Preferences**.

2. Select **Enable Basic authentication** then close the Preferences screen.

3. Click **Add Location** in Document Connection then **Connect to a SharePoint site**.

4. Enter the Alfresco address then click **Connect**.

    To connect with Alfresco the URL needs to end in `/alfresco/aos`, for example `https://mycompany.com/alfresco/aos/`.

    You can enter URLs that are specific to a site, folder, or file, for example, `https://mycompany.com/alfresco/aos/Sites/sitename/documentLibrary/foldername/filename`.

    * Site or folder-specific URL - browse through the site or folder to find the file you want
    * File-specific URL - open the file directly

5. Enter your Alfresco User name and Password and click **Connect**.

    > **Note:** Click **Continue** if you see a further message about encrypted passwords.

    This connection is remembered by Document Connection for future use.

    You'll now see all the folders at the top level of your Alfresco repository, and you can drill-down through sites to all your files.

    You can use the Document Connector to read, add, and check files in and out, and even drag and drop them from your desktop or from Finder.

## Alfresco File Properties in Microsoft Office

Files stored in Alfresco can have lots of properties to help identify and track them. In Microsoft Windows, you can see these when you click the **Info** tab when you have a file open in Microsoft Office.

File properties can include things such as who created a file, the file title, and any categories or tags attributed to the file.

Your Alfresco administrator can choose to set up different content types. If they do then when you save a new file to Alfresco you'll be asked to select a content type to assign it to. The content type you select will give you the option to add additional content type-specific properties to the file.

In Microsoft Windows, you can change file properties when you have a file open in Microsoft Office by clicking on a property in the **Info** tab, or by selecting **File** then **Info**, then clicking **Properties** and selecting **Show Document Panel**. This shows the **Document Panel** above the open file, and you can modify file properties as required.

Some content types may require you to enter specific properties before you can even save a file; in these cases you'll receive a warning and a link to open the **Document Panel**.

When you've saved the file you'll be able to see any changes you've made to the properties if you look at the file in Alfresco.

![AOS Alfresco properties]({% link microsoft-office/images/properties.png %})
