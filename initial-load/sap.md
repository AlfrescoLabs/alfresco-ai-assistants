---
title: Alfresco Content Connector for SAP Applications
---

The Alfresco Content Connector for SAP applications is an add-on module that offers seamless integration between Alfresco Content Services and SAP (R/3, S/4HANA). It connects the structured data in SAP with the unstructured data (or "living content") in Alfresco.

![sap_certified_integration_saps4hana]({% link sap/images/sap_certified_integration_saps4hana.png %}){:height="60px" width="298px"}![sap_silver_partner_logo]({% link sap/images/sap_silver_partner_logo.png %}){:height="60px" width="100px"}

The following image shows a simple representation of how Content Services (plus other Alfresco products) and the SAP Connector interact with SAP systems.

![sap_alfresco_high_level_architecture]({% link sap/images/sap_alfresco_high_level_architecture.png %})

Here is a summary of the key capabilities:

* **Improved Productivity:** One single source of truth for content via different user interfaces improves productivity.
* **Collaboration Ready:** Make content available in the business process for different teams inside or outside the company.
* **Metadata Synchronization:** Leverage structured data also outside SAP with automated metadata synchronization.
* **Certified by SAP:** All SAP HTTP-Content Server related standard scenarios are covered. For example:
  * SAP Archivelink
    * Incoming documents (e.g. incoming invoices)
      * Early Archiving with SAP Workflow
      * Early Archiving with Barcode
      * Late Archiving
    * Outgoing documents (e.g. order confirmations)
    * Print List Archiving (e.g. quarter end reports)
    * SAP Workflow
* SAP Document Management Service (DMS)
* SAP Attachments
* SAP Data Archiving (ADK)

> **Important:** The SAP Connector module can be applied to Alfresco Content Services. See [Prerequisites]({% link sap/latest/install/index.md %}#prerequisites) and [Supported platforms]({% link sap/latest/support/index.md %}) for more.

> **Note:** This documentation only covers how to use Content Services with the SAP Connector.
---
title: Administer SAP Connector
---

This page shows you how to check the health of the current installation using Alfresco Share, and troubleshooting.

## Administration Console {#sapadminconsole}

The SAP Connector Administration Console provides a smart overview of all important settings for the current state of the SAP Connector. Having all configuration settings and properties, from different parts of the installation,  in one screen makes it easy to identify and review the current state.

The SAP Connector Administration Console is only available for Alfresco Share. If Alfresco Share isn't available, you can use the SAP Connector Administration Health WebScript to check the status of the SAP Connector.
See [SAP Connector Administration Health Web Script](#sapadminhealthwebscript) for more.

### Accessing the Administration Console

The SAP Connector Administration Console is installed as an *Admin Tool*, so you can access it via the **Admin Tools** toolbar in Alfresco Share. A new menu item **SAP Integration** is available. Click it to open the SAP Connector Administration Console.

![sap_inst_002_adminconsole]({% link sap/images/sap_inst_002_adminconsole.png %})

### Using the Administration Console

This is a deep dive into the different sections of the SAP Connector Administration Console.

#### Header Information

The header section provides a brief overview of the installed SAP Connector version and the build. It also displays the current SAP Connector health status based on the three traffic light colors (red, yellow and green). Having this, the overall health can be easily reviewed at a glance.

![sap_inst_002_adminconsole_001_header]({% link sap/images/sap_inst_002_adminconsole_001_header.png %})

| Status Color | Description |
| ------------ | ----------- |
| Green | The SAP Connector is configured properly and is working. No action required. |
| Yellow | Review the current settings. Immediate action may not be required. Examples for this state are:{::nomarkdown}<ul><li>The certificate for a (new) SAP Content Repository is not enabled yet (but exists already).</li><li>The license or the maintenance period expires soon.</li></ul>{:/} |
| Red | This flag requires immediate action. Examples are:{::nomarkdown}<ul><li>The license has expired.</li><li>Properties or values for required parameters are missing.</li><li>A new SAP Content Repository is available but no certificate has been sent yet.</li></ul>{:/} |

#### License Information

All important information regarding the current applied license (including the maintenance period) are displayed for the SAP Connector. In this section you can also apply a new license by using the **Upload License** button. See [Installing the license]({% link sap/latest/install/index.md %}#installing-the-license) for more.

![sap_inst_002_adminconsole_002_license]({% link sap/images/sap_inst_002_adminconsole_002_license.png %})

#### SAP System Configuration Information

This section displays detailed information of all available SAP System Configurations from the `alfresco-global.properties`. Each SAP System Configuration appears in a separate box and contains - besides the configuration settings from the `alfresco-global.properties` - also all SAP Content Repositories which are set up for the SAP System Configuration along with their settings for Jobs, Behaviors. The next screenshot shows how one SAP System Configuration will be displayed. If you have two SAP System Configuration configured, this box displays twice, and so on.

![sap_inst_002_adminconsole_003_sapsystemconfiguration]({% link sap/images/sap_inst_002_adminconsole_003_sapsystemconfiguration.png %})

The following sub-sections explains each area shown in the screenshot above in more detail.

* **Archivelink Settings**

    Display important information used for the basic communication between SAP and Content Services. All settings are related to the settings in the `alfresco-global.properties`.

    > **Note:** The password for the user used to login to Content Services is never transmitted, hence it is not displayed in the Administration Console.

* **SAP Java Connector Settings**

    Display important information used for the connection from Content Services to SAP as well as related information for the [Opening associated Business Object in SAP]({% link sap/latest/config/advanced.md %}#openassocbusinessobjinsap) feature.

    > **Note:** The password for the SAP system user used to connect to SAP is never transmitted, hence it is not displayed in the Administration Console.

* **SAP Content Repositories**

    List all SAP Content Repositories connect via the current SAP System Configuration. Each SAP Content Repository appears in a new line. The background color of each SAP Content Repository indicates its current state in Content Services. The condition is also highlighted with traffic light colors, as the overall health state in the header too. Any other state than Green will affect the overall health state as well, meaning if the state is yellow, then also the overall health state in the header is at least yellow.

    > **Note:** If the state of a SAP Content Repository is highlighted with yellow background, there is a need to activate the certificate (sent from SAP) for that repository. In this case the **Status** column shows a button to activate the certificate.

    | Status Color | Description |
    | ------------ | ----------- |
    | Green | The SAP Content Repository is up and running. |
    | Yellow | The SAP Content Repository exists in Content Services and the certificate was also sent already. However, the certificate still needs to be activated to allow the communication. In this case, a button appears in the **Status** column to enable the certificate. Once enabled, the status color will switch to green. |
    | Red | There are two options which lead to this state:<br><br>1. The SAP Content Repository was not created yet (see [1. Create SAP Content Repository]({% link sap/latest/config/index.md %}#basic-createsapcontentrepo)).<br>2. The SAP Content Repository exists but the certificate was not sent yet (see [2. Secure connection using a certificate]({% link sap/latest/config/index.md %}#basic-secureconnwithcert)).<br><br>However, the message in the `Status` column in such a case will show the exact reason. |

* **Jobs**

    This table lists all available jobs and the current state of each SAP Content Repository for it along with the CRON expression used to invoke the job. See [Configuring jobs]({% link sap/latest/config/index.md %}#configure-jobs) to learn more about how to enable or disable jobs for SAP Content Repositories.

* **Behaviors**

    Like for the jobs above, this table lists all available behaviors and the current state of each SAP Content Repository for it. See [Configuring behaviors]({% link sap/latest/config/index.md %}#configure-behaviors) to learn more about how to enable or disable behaviors for SAP Content Repositories.

* **Feature: Open corresponding SAP Business Object**

    This section only appears if the [Opening associated Business Object in SAP]({% link sap/latest/config/advanced.md %}#openassocbusinessobjinsap) feature is used and the default settings was overridden. See [Advanced configuration]({% link sap/latest/config/advanced.md %}#OpenBusinessObjectSAPAdvancedConfig) for more. It shows the content of related `webClient-config.properties` for the current SAP System Configuration.

    ![sap_inst_002_adminconsole_004_openinsap]({% link sap/images/sap_inst_002_adminconsole_004_openinsap.png %})

#### Additional Settings

This section only appears if there are any of the additional settings which override the standard behavior of the SAP Connector. See [Additional repository settings]({% link sap/latest/admin/reference.md %}#additionalrepoconfig) for more. These common settings affect the SAP Connector as they're not related to a particular SAP System Configuration.

This section lists all additional settings available in the `alfresco-global.properties` which are used to override core behavior. The **Name** column shows the property key, including the default value (in brackets), and the **Value** column shows the current value used to override the default.

![sap_inst_002_adminconsole_005_additionalsettings]({% link sap/images/sap_inst_002_adminconsole_005_additionalsettings.png %})

## Administration Health Web Script {#sapadminhealthwebscript}

This topic shows you how to check the health of the current installation using a Web Script.

The health Web Script can be used as an alternative way to check the state of the SAP Connector without accessing the [SAP Connector Administration Console](#sapadminconsole) in Alfresco Share. It allows to review all settings related to a specific SAP Content Repository name (`archiveId`) defined in `alfresco-global.properties`.

> **Note:** Unlike the SAP Connector Administration Console, this Web Script just provides a configuration overview. It's not intended for any action to be executed.

### Accessing the Web Script

The Web Script is available on the repository tier. To access it, log in to the **Alfresco Web Scripts Home** and browse to **Content Connector for SAP - Admin** web scripts.

![sap_inst_003_healthwebscript_001]({% link sap/images/sap_inst_003_healthwebscript_001.png %})

In this section, scroll to **Health Check of Content Connector for SAP** where the Web Script is available. If you click the link without any modification, the Web Script returns an error. You'll need to change the `archiveId` parameter, as shown in the next section.

![sap_inst_003_healthwebscript_002]({% link sap/images/sap_inst_003_healthwebscript_002.png %})

### List all available SAP System Configurations with SAP Content repository names

You call the Web Script with an **empty value** for the `archiveId` parameter to list all SAP System Configurations with their related SAP Content Repositories. These parameters are defined in `alfresco-global.properties`:

```html
http://localhost:8080/alfresco/s/com/alfresco/sap/admin/healthcheck?archiveId=
```

In this case, the Web Script returns all settings that affect the global behavior of the SAP Connector (if available). See [Additional repository settings]({% link sap/latest/admin/reference.md %}#additionalrepoconfig) for more details. It also lists the `archiveIds` parameter for each available SAP System Configuration, and displays the values (which are the SAP Content Repository names).

Click an SAP Content Repository name to show the details of the related SAP System Configuration.

![sap_inst_003_healthwebscript_004]({% link sap/images/sap_inst_003_healthwebscript_004.png %})

### Check SAP Connector health by SAP Content repository name

You can check the SAP System Configuration for a particular SAP Content Repository by passing the `archiveId` parameter with an existing SAP Content Repository name. For example:

```html
http://localhost:8080/alfresco/s/com/alfresco/sap/admin/healthcheck?archiveId=XX
```

This prints all settings for the given `archiveId`. It includes all settings of the related SAP System Configuration, and also SAP Connector core settings. See [Additional repository settings]({% link sap/latest/admin/reference.md %}#additionalrepoconfig) for more details. In addition, it may show any detected configuration errors for this `archiveId`.

![sap_inst_003_healthwebscript_003]({% link sap/images/sap_inst_003_healthwebscript_003.png %})

## Troubleshoot SAP Connector

Your problem may be related to any one of the following issues:

### License not valid

If you can't apply the SAP Connector license you've received successfully, make sure you've provided the correct details of your landscape (such as *Is Alfresco Content Services running in a virtual machine?*) which are important to issue the license.

### Error during connection test setting up a secure connection (HTTPS) in OAC0

If you receive an error during the connection test in `OAC0` for the SAP Content Repository, make sure you've removed the `Port Number`. Only provide the `SSL Port Number` in this case.

### Payment required (HTTP Response code 402)

If the SAP Connector license becomes invalid or is missing, the SAP user will get a popup which states "Payment required", along with a 402 HTTP response code once they try to store a document in Content Services. In this case, check the SAP Connector license. See [Installing the license]({% link sap/latest/install/index.md %}#installing-the-license) for more.

### Content Services fails to start

Before applying the provided SAP Connector AMP files, the native SAP Java Connector libraries must be merged into the delivered SAP Connector repository AMP file. If you don't do this, then Content Services fails to start.

In this case, the related error message in the log file looks similar to:

```java
**java.lang.UnsatisfiedLinkError: no sapjco3 in java.library.path: \[/usr/local/tomcat/native-jni-lib, /usr/java/packages/lib, /usr/lib64, /lib64, /lib, /usr/lib\]**
        at java.base/java.lang.ClassLoader.loadLibrary(ClassLoader.java:2660)
        at java.base/java.lang.Runtime.loadLibrary0(Runtime.java:829)
        at java.base/java.lang.System.loadLibrary(System.java:1867)
        at com.sap.conn.jco.rt.DefaultJCoRuntime.loadJCoLibrary(DefaultJCoRuntime.java:898)
```

> **Note:** The same message also appears if the wrong native files (related to the Content Services target system) of the SAP Java Connector have been applied.

To solve this issue, follow the steps in [Installing SAP Connector]({% link sap/latest/install/index.md %}).
---
title: SAP Connector reference
---

This page provides useful references for the SAP Connector.

## Abbreviations

Here are all the abbreviations that are used in the SAP Connector documentation.

| Abbreviation | Description |
| ------------ | ----------- |
| ABAP | Advanced Business Application Programming (SAP) |
| AMP | Alfresco Module Package |
| DIR | Document Info Record (SAP) |
| DMS | Document Management Service (SAP) |
| ECC | SAP ERP Central Component |
| ERP | Enterprise Resource Planning |
| HTTP(S) | Hypertext Transfer Protocol (Secure) |
| ICM | Internet Communication Manager (SAP) |
| IMG | Implementation Guide (SAP) |
| JCo | SAP Java Connector |
| PSE | Personal Security Environment (SAP) |
| SAP | Systeme, Anwendungen und Produkte |
| OSS | Online Service System (SAP) |
| t-code | Transaction Code |

The SAP Connector release includes the following third-party software. These are used either at runtime or while packaging the delivery:

| Abbreviation | Description |
| ------------ | ----------- |
| jcabi-manifests | Manager of MANIFEST.MF files |
| jcabi-logs | Wrapper for Simple Logging Facade for Java (SLF4J) and a few supplementary logging classes |
| license4j-runtime-library | License4J runtime library |
| jcommander | Library to handle command line arguments for the password encryption |
| commons-io | Library of utilities to assist with developing IO functionality required for the SAP JCo Packer tool only |
| commons-compress | Library to compress the modified SAP Connector repository AMP with the included SAP JCo libraries. Required for SAP JCo Packer tool only |
| zip4j | Library to extract the ZIP file from the SAP Java Connector, downloaded from SAP. Required for SAP JCo Packer tool only |
| slf4j-api | Logging framework used for the SAP-Packer. Required for SAP JCo Packer tool only |
| slf4j-simple |Java binding for the logging framework. Required for SAP JCo Packer tool only |

## Additional repository settings {#additionalrepoconfig}

The following table lists additional settings that can be provided in the `alfresco-global.properties` file to override the standard behavior of the SAP Connector. These settings are not related to a particular SAP System Configuration, but they will affect the basic functionality and should be used with caution.

> **Important:** The recommendation is to always consult Alfresco Support before overriding SAP Connector standard behavior with any of the settings below.

| Property | Description |
| -------- | ----------- |
| integrations.sap.configuration.attributeService.enabled | Use the SAP Connector internal `AttributeService` to find documents from SAP, across multiple nodes in high availability systems. Only required if the *Alfresco Full Text Search* within the *Transactional Query Options* was set to `**Never use Database**` in the Alfresco Admin Console. Default value: `false` |
| integrations.sap.configuration.defaultDocProtection | Override the default setting for the `SAP DocProtection` (property `connexasArchivelink:docprot`). If no `docProt` parameter is transferred or an [SAP Archivelink Document](#archivelinktype) is created, this value will be used to override the default. Default value: `rcdu` |
| integrations.sap.configuration.chunkSize | Chunk size that is used to read the payload of the HTTP request. Usually there is no need to change this setting. Default value: `65536 (byte)` |
| integrations.sap.configuration.postFilter.enabled | If `true`, the SAP Connector queries the database only for `docId` instead of `docId`, `compId` and `archiveId`.In this case, `compId` and `archiveId` will be filtered in a second step. Recommended if the database execution plan prioritizes `compId` and `archiveId` (both not unique) over the `docId` (unique) and therefore get an huge result set. Default value: `false` |
| integrations.sap.configuration.doubleSearch.enabled | If `true`, the query used for finding documents requested by SAP is first executed against Solr. If we don't find the desired document, we search again, but against the database using transactional metadata queries (TMQ). In some situations, especially large databases, this can improve speed. Default value: `false` |

## Example configurations {#examplesapsysconfigs}

This section gives examples of different types of system configurations.

### Example 1: One SAP system configuration with Archivelink only {#examplesapsysconfig1}

This is an example for one *SAP System Configuration* with one connected SAP Content Repository, using pure Archivelink (metadata replication is off).

Copy and paste the *SAP System Configuration* code snippet below to your `alfresco-global.properties` and replace the **values** indicated according to your specification.

> **Note:** Do not remove unused property keys.

```text
integrations.sap.system.1.al.alfrescoUser=**admin**
integrations.sap.system.1.al.alfrescoPassword=**t0ps3cR3t**
integrations.sap.system.1.al.archiveIds=**M1**
integrations.sap.system.1.al.documentRoot=**/app:company_home/st:sites/cm:sap/cm:documentLibrary/cm:SAP_Documents**
integrations.sap.system.1.al.checkSignature=**true**
integrations.sap.system.1.al.checkExpiration=**true**

integrations.sap.system.1.enabled=**false**
integrations.sap.system.1.name=${sap.system.1.name}
integrations.sap.system.1.host= ${sap.system.1.host}
integrations.sap.system.1.client= ${sap.system.1.client}
integrations.sap.system.1.systemNumber= ${sap.system.1.systemNumber}
integrations.sap.system.1.user= ${sap.system.1.user}
integrations.sap.system.1.password= ${sap.system.1.password}
integrations.sap.system.1.language= ${sap.system.1.language}
integrations.sap.system.1.webClient.enabled=false
integrations.sap.system.1.webClient.url=https://sapserver:port/sap/bc/gui/sap/its/webgui

integrations.sap.system.1.jobs.sapContentConnectorReplicate.enabled = false
integrations.sap.system.1.jobs.sapContentConnectorReplicate.cronExpression = 0 0/1 * 1/1 * ? *
integrations.sap.system.1.jobs.sapContentConnectorPlus.enabled = false
integrations.sap.system.1.jobs.sapContentConnectorPlus.cronExpression = 0 0/1 * 1/1 * ? *
integrations.sap.system.1.jobs.sapContentConnectorBarcode.enabled = false
integrations.sap.system.1.jobs.sapContentConnectorBarcode.cronExpression = 0 0/1 * 1/1 * ? *
integrations.sap.system.1.jobs.sapContentConnectorDirReplicate.enabled = false
integrations.sap.system.1.jobs.sapContentConnectorDirReplicate.cronExpression = 0 0/1 * 1/1 * ? *
```

### Example 2: One SAP system configuration with metadata replication

This is an example for one *SAP System Configuration* with one connected SAP Content Repository, using default and additional metadata replication. It also enables the *Open corresponding business object in SAP* feature in Alfresco Share.

Copy and paste the *SAP System Configuration* code snippet below to your `alfresco-global.properties` and replace the **values** indicated according to your specification.

> **Note:** Do not remove unused property keys.

```text
integrations.sap.system.1.al.alfrescoUser=**admin**
integrations.sap.system.1.al.alfrescoPassword=**t0ps3cR3t**
integrations.sap.system.1.al.archiveIds=**M1**
integrations.sap.system.1.al.documentRoot=**/app:company_home/st:sites/cm:sap/cm:documentLibrary/cm:SAP_Documents**
integrations.sap.system.1.al.checkSignature=**true**
integrations.sap.system.1.al.checkExpiration=**true**

integrations.sap.system.1.enabled=**true**
integrations.sap.system.1.name=**SAP Finance (NSP)**
integrations.sap.system.1.host=**192.168.112.112**
integrations.sap.system.1.client=**800**
integrations.sap.system.1.systemNumber=**01**
integrations.sap.system.1.user=**ALFRESCO**
integrations.sap.system.1.password=**t0ps3cR3tP@Ssw0rD**
integrations.sap.system.1.language=**EN**
integrations.sap.system.1.webClient.enabled=**true**
integrations.sap.system.1.webClient.url=**https://192.168.112.112:8021/sap/bc/gui/sap/its/webgui**

integrations.sap.system.1.jobs.sapContentConnectorReplicate.enabled=**true**
integrations.sap.system.1.jobs.sapContentConnectorReplicate.cronExpression=**0 0/1 \* 1/1 \* ? \***
integrations.sap.system.1.jobs.sapContentConnectorPlus.enabled=**true**
integrations.sap.system.1.jobs.sapContentConnectorPlus.cronExpression=**0 0/1 \* 1/1 \* ? \***
integrations.sap.system.1.jobs.sapContentConnectorBarcode.enabled=false
integrations.sap.system.1.jobs.sapContentConnectorBarcode.cronExpression=0 0/1 * 1/1 * ? *
integrations.sap.system.1.jobs.sapContentConnectorDirReplicate.enabled=false
integrations.sap.system.1.jobs.sapContentConnectorDirReplicate.cronExpression=0 0/1 * 1/1 * ? *
```

### Example 3: Two SAP system configurations with metadata replication

This is a more complex example with two *SAP System Configurations*, different SAP Content Repositories having a mix of properties enabled and disabled.

Copy and paste the *SAP System Configuration* code snippet below to your `alfresco-global.properties` and replace the **values** indicated according to your specification.

> **Note:** Do not remove unused property keys.

In this example, the first *SAP System Configuration* uses plain-text passwords while the second *SAP System Configuration* uses encrypted passwords (see [Encrypting passwords](#encryptpwd) for more). It also has two connected SAP Content Repositories and uses a different site to store the documents. It doesn't have the SAP Web-GUI enabled, and the metadata replication jobs are invoked every 5 minutes instead running each minute like in the first *SAP System Configuration*.

```text
// SAP System Configuration 1
integrations.sap.system.1.al.alfrescoUser=**admin**
integrations.sap.system.1.al.alfrescoPassword=**t0ps3cR3t**
integrations.sap.system.1.al.archiveIds=**M1**
integrations.sap.system.1.al.documentRoot=**/app:company_home/st:sites/cm:sap/cm:documentLibrary/cm:SAP_Documents**
integrations.sap.system.1.al.checkSignature=**true**
integrations.sap.system.1.al.checkExpiration=**true**

integrations.sap.system.1.enabled=**true**
integrations.sap.system.1.name=**SAP Finance (NSP)**
integrations.sap.system.1.host=**192.168.112.112**
integrations.sap.system.1.client=**800**
integrations.sap.system.1.systemNumber=**01**
integrations.sap.system.1.user=**ALFRESCO**
integrations.sap.system.1.password=**t0ps3cR3tP@Ssw0rD**
integrations.sap.system.1.language=**EN**
integrations.sap.system.1.webClient.enabled=**true**
integrations.sap.system.1.webClient.url=**https://192.168.112.112:8021/sap/bc/gui/sap/its/webgui**

integrations.sap.system.1.jobs.sapContentConnectorReplicate.enabled=**true**
integrations.sap.system.1.jobs.sapContentConnectorReplicate.cronExpression=**0 0/1 \* 1/1 \* ? \***
integrations.sap.system.1.jobs.sapContentConnectorPlus.enabled=**true**
integrations.sap.system.1.jobs.sapContentConnectorPlus.cronExpression=**0 0/1 \* 1/1 \* ? \***
integrations.sap.system.1.jobs.sapContentConnectorBarcode.enabled=false
integrations.sap.system.1.jobs.sapContentConnectorBarcode.cronExpression=0 0/1 * 1/1 * ? *
integrations.sap.system.1.jobs.sapContentConnectorDirReplicate.enabled=false
integrations.sap.system.1.jobs.sapContentConnectorDirReplicate.cronExpression=0 0/1 * 1/1 * ? *
  
// SAP System Configuration 2
integrations.sap.system.2.al.alfrescoUser=**sapinteg**
integrations.sap.system.2.al.alfrescoPassword=**ENC(XbfE4Z112==)**
integrations.sap.system.2.al.archiveIds=**K2,Z1**
integrations.sap.system.2.al.documentRoot=**/app:company_home/st:sites/cm:sap_hr/cm:documentLibrary/cm:SAP_Documents**
integrations.sap.system.2.al.checkSignature=**true**
integrations.sap.system.2.al.checkExpiration=**true**

integrations.sap.system.2.enabled=**true**
integrations.sap.system.2.name=**SAP HR (S4H)**
integrations.sap.system.2.host=**192.168.1.110**
integrations.sap.system.2.client=**100**
integrations.sap.system.2.systemNumber=**00**
integrations.sap.system.2.user=**ALF_HR**
integrations.sap.system.2.password=**ENC(RET45324GFDSFfsf43ZEr4rfer45)**
integrations.sap.system.2.language=**EN**
integrations.sap.system.2.webClient.enabled=**false**
integrations.sap.system.2.webClient.url=https://sapserver:port/sap/bc/gui/sap/its/webgui

integrations.sap.system.2.jobs.sapContentConnectorReplicate.enabled=**true**
integrations.sap.system.2.jobs.sapContentConnectorReplicate.cronExpression=**0 0/5 \* 1/1 \* ? \***
integrations.sap.system.2.jobs.sapContentConnectorPlus.enabled=**true**
integrations.sap.system.2.jobs.sapContentConnectorPlus.cronExpression=**0 0/5 \* 1/1 \* ? \***
integrations.sap.system.2.jobs.sapContentConnectorBarcode.enabled=false
integrations.sap.system.2.jobs.sapContentConnectorBarcode.cronExpression=0 0/1 * 1/1 * ? *
integrations.sap.system.2.jobs.sapContentConnectorDirReplicate.enabled=false
integrations.sap.system.2.jobs.sapContentConnectorDirReplicate.cronExpression=0 0/1 * 1/1 * ? *
```

## Reference for SAP Object Type Mapping {#refsapobjecttypemap}

This is the reference for all supported `SAP Object Types` that are available by default in Alfresco Share to open the associated SAP Business Object along with their related transaction within the SAP Web-GUI.

See the [Opening associated Business Object in SAP]({% link sap/latest/config/advanced.md %}#openassocbusinessobjinsap) feature to learn how to enable and how to customize it.

> **Note:** Because the SAP Object Types `BKPF` and `BUS2081` requires a split of the replicated `SAP Object Id` into at least 2 separate parameters, the URL of both SAP Object Types should never be changed (not even the order).

| SAP Object Type | SAP Transaction | Description | URL parameter attached to the SAP Web-GUI |
| --------------- | --------------- | ----------- |----------------------------------------- |
| BKPF | FB03 | Accounting Document Header | ?~transaction=FB03%%20RF05L-BELNR=%s;RF05L-BUKRS=%s;RF05LGJAHR=%s&~okcode=/00 |
| BUS1065 | PA40 | Personnel Actions | ?~transaction=PA40%%20RP50G-PERNR=%s&~okcode=/00 |
| BUS2010 | ME43 | Request For Quotation | ?~transaction=ME43%%20RM06E-ANFNR=%s&~okcode=/00 |
| BUS2012 | ME23 | Purchase Order | ?~transaction=ME23%%20RM06E-BSTNR=%s&~okcode=/00 |
| BUS2017 | MB03 | Material Document | ?~sap-client=%SAP_CLIENT%&~transaction=MB03%20RM07M-MBLNR=%SAP_OBJECT_ID{1:10}%;RM07M-MJAHR=%SAP_OBJECT_ID{11:14}%&~okcode=/00 |
| BUS2032 | VA03 | Sales Order | ?~transaction=VA03%%20VBAK-VBELN=%s&~okcode=/00 |
| BUS2078 | QM03 | Quality Notification | ?~sap-client=%SAP_CLIENT%&~transaction=QM03%20RIWO00-QMNUM=%SAP_OBJECT_ID%&~okcode=/00 |
| BUS2081 | MIR4 | MIRO - Change Status | ?~transaction=MIR4%%20RBKP-BELNR=%s;RBKP-GJAHR=%s&~okcode=/00 |
| BUS2105 | ME53 | Purchase Requisition | ?~transaction=ME53%%20EBAN-BANFN=%s&~okcode=/00 |
| EQUI | IE03 | Equipment | ?~sap-client=%SAP_CLIENT%&~transaction=IE03%20RM63E-EQUNR=%SAP_OBJECT_ID%&~okcode=/00 |
| KNA1 | VD03 | Customer (Sales) | ?~sap-client=%SAP_CLIENT%&~transaction=VD03%20RF02D-KUNNR=%SAP_OBJECT_ID%&RF02D-D0110=true&~okcode=/00 |
| LFA1 | MK03 | Vendor Master | ?~sap-client=%SAP_CLIENT%&~transaction=MK03%20RF02K-LIFNR=%SAP_OBJECT_ID%&RF02K-D0110=true&~okcode=/00 |
| PREL | PA20 | HR Master Data | ?~sap-client=%SAP_CLIENT%&~transaction=PA20%20RP50G-PERNR=%SAP_OBJECT_ID{0:8}%&~okcode=/00 |
| VBRK | VF03 | Billing Documents | ?~sap-client=%SAP_CLIENT%&~transaction=VF03%20VBRK-VBELN=%SAP_OBJECT_ID%&~okcode=/00 |

## Additional SAP JavaConnector properties {#sapjavaconprops}

This reference lists the additional properties (such using Logon Groups) for the SAP JavaConnector that are supported for each available SAP System Configuration.

See [Configure repository properties]({% link sap/latest/install/index.md %}#configrepo) and the [example configurations](#examplesapsysconfigs). The properties in the table below use [SAP system configuration with Archivelink only](#examplesapsysconfig1) as an example.

> **Note:** See the SAP JavaConnector documentation to learn more about the available properties and their behaviors in detail.

| Property | Description |
| --------- | ----------- |
| integrations.sap.system.1.destination.auth_type | The authentication type - configured user or current user. |
| integrations.sap.system.1.destination.auth_type | The authentication type - configured user or current user. |
| integrations.sap.system.1.configured_user | The destination configured for the specified user only. |
| integrations.sap.system.1.current_user | The connection created using this destination belongs to the current user. |
| integrations.sap.system.1.alias_user | Logon user alias, can be used instead of logon user. |
| integrations.sap.system.1.codepage | Initial logon codepage in SAP notation. |
| integrations.sap.system.1.pcs | Initial logon codepage type (`1`: non-Unicode or `2`: Unicode enabled, optional). |
| integrations.sap.system.1.mshost | SAP message server host. |
| integrations.sap.system.1.msserv | SAP message server service or port number (optional). |
| integrations.sap.system.1.r3name | System ID of the SAP system, the so-called SID. |
| integrations.sap.system.1.group | Logon group name of SAP application servers (optional, default is PUBLIC). |
| integrations.sap.system.1.saprouter | SAP router string to use for networks being protected by a firewall. |
| integrations.sap.system.1.mysapsso2 | SAP Cookie Version 2 as logon ticket. |
| integrations.sap.system.1.getsso2 | Get/don't get an SSO ticket after logon (`1` or `0`). |
| integrations.sap.system.1.x509cert | X.509 certificate as logon ticket. |
| integrations.sap.system.1.extid_data | External identification user logon data. |
| integrations.sap.system.1.extid_type | Type of the external identification user logon data. |
| integrations.sap.system.1.lcheck | Enable/disable logon check at open time (`1`: enable [default] or `0`: disable). |
| integrations.sap.system.1.delta|Enable/disable table parameter delta management (`1`: enable [default] or `0`: disable). |
| integrations.sap.system.1.snc_partnername | SNC name of the communication partner server. For example: p:CN=SID, O=ACompany, C=EN. |
| integrations.sap.system.1.snc_qop | SNC quality of protection; valid values: `1`, `2`, `3`, `8` (default), `9`. |
| integrations.sap.system.1.snc_myname | Own SNC name of the caller (optional). Overrides the default SNC name. For example: p:CN=MyUserID, O=ACompany, C=EN. |
| integrations.sap.system.1.snc_mode|Secure Network Communications (SNC) mode; `1`: on, `0`: off (default). |
| integrations.sap.system.1.snc_sso | Turn on/off the SSO mechanism of SNC. If set to `0`, use alternative credentials like user/password instead. Valid values are `1` (yes, default) and `0` (no). |
| integrations.sap.system.1.snc_lib | Full path to the library which provides the SNC service. Default: value from {% include tooltip.html word="SAP_JCo" text="JCo" %} middleware property `jco.middleware.snc_lib`. |
| integrations.sap.system.1.destination.peak_limit | Maximum number of active connections that can be created for a destination simultaneously. |
| integrations.sap.system.1.destination.pool_capacity | Maximum number of idle connections kept open by the destination. A value of `0` provides no connection pooling, i.e. connections will be closed after each request. |
| integrations.sap.system.1.destination.expiration_time | Time in milliseconds (ms) after that the connections held by the internal pool can be closed. |
| integrations.sap.system.1.destination.expiration_check_period | Interval in milliseconds (ms) with which the timeout checker thread checks the connections in the pool for expiration. |
| integrations.sap.system.1.destination.max_get_client_time | Maximum time in milliseconds (ms) to wait for a connection, if the maximum allowed number of connections is allocated by the application. |
| integrations.sap.system.1.destination.repository_destination | Specifies which destination should be used for repository queries. |
| integrations.sap.system.1.destination.repository.user | Optional: If repository destination is not set, and this property is set, it will be used as user for repository queries. This allows using a different user for repository lookups and restrict the permissions accordingly. |
| integrations.sap.system.1.destination.repository.passwd | The password for a repository user. Mandatory, if a repository user should be used. Enter as plain-text or use encrypted password. For latter, the value must be enclosed with string `ENC()`. |
| integrations.sap.system.1.destination.repository_scn_mode | Optional: If SNC is used for this destination, it is possible to turn it off for repository connections, if this property is set to `0`. Defaults to the value of `jco.client.snc_mode`. |
| integrations.sap.system.1.destination.repository_roundtrip_optimization | `1`: forces the usage of RFC_METADATA_GET in {% include tooltip.html word="SAP_ABAP" text="ABAP" %} System, `0`: deactivates it. If the property is not set, the destination will initially do a remote call to check whether RFC_METADATA_GET is available. If it's available, then it'll use it. |
| integrations.sap.system.1.cpic_trace | Enable/disable CPIC trace (`-1`: take over environment value CPIC_TRACE, `0`: no trace, `1,2,3` - different trace levels). |
| integrations.sap.system.1.trace | Enable/disable RFC trace (`0` or `1`). |
| integrations.sap.system.1.gwhost | SAP gateway host. |
| integrations.sap.system.1.gwserv | SAP gateway service or port number. |
| integrations.sap.system.1.tphost | Host on which to start an external RFC server executable program. |
| integrations.sap.system.1.tpname | Registered RFC server program ID / External RFC server executable program name. |
| integrations.sap.system.1.type | Connection type (optional). |
| integrations.sap.system.1.use_sapgui | Start a SAP GUI and associate with the connection (`0`: do not start [default], `1`: start GUI, `2`: start GUI and hide if not used). |
| integrations.sap.system.1.deny_initial_password | Deny usage of initial passwords (`0` [default] or `1`). |

## Communication via HTTPS {#securecomms}

Set up a secure communication between Content Services and SAP.

The SAP Connector works well over HTTPS. In general, there is no need to configure the SAP Connector. The main part is to prepare the SAP system and Content Services with the related certificates to use a secure connection.

> **Important:** This chapter only describes the necessary steps to implement the certificate from the Content Services web server in SAP and prepare SAP Content Repositories to use HTTPS over HTTP for the communication.

> **CAUTION**: The creation and installation of the certificate on the Content Services web server is not part of this section.

### Get current certificate from Alfresco {#getcertfromalfresco}

Get the current certificate from Alfresco.

The current certificate used by the Content Services webserver must be known (and imported) in SAP. Therefore, export the certificate by following the steps below:

> **Important:** The Content Services webserver must be up and running on a secure connection. This documentation does not cover the installation and configuration of the SSL connection on Content Services side. It only covers how to get the existing certificate.

1. Open Content Services (either the Alfresco Share or Alfresco Digital Workspace login page) in a web-browser and view the details of the current certificate.

    ![sap_inst_004_https_002_alf_certificate]({% link sap/images/sap_inst_004_https_002_alf_certificate.png %})

2. Export the certificate to the local machine (depending on the browser manufacturer).

    ![sap_inst_004_https_002_alf_certificate_export]({% link sap/images/sap_inst_004_https_002_alf_certificate_export.png %})

3. Make sure you use `DER encoded binary X.509 (.CER)` as the export format.

    ![sap_inst_004_https_002_alf_certificate_export_format]({% link sap/images/sap_inst_004_https_002_alf_certificate_export_format.png %})

4. Once successfully saved, the file will be required in step [Import Alfresco Certificate in SAP PSE](#importcertinsappse).

Prepare the SAP Content Repository to use a secure connection.

### Prepare SAP Content Repository for HTTPS

Set up SAP Content Repository connection to use a secure connection.

To prepare the SAP Content Repository to use a secure connection, follow these steps:

1. Open transaction `OAC0`.

2. Select the desired SAP Content Repository.

3. Enter `%https` in the transaction code field to show required HTTPS related settings:

    1. Remove the value for `Port Number`.

    2. Add the `SSL Port Number`.

    3. Select `HTTPS required` as a value for **HTTPS on frontend**.

    4. Select `HTTPS required` as a value for **HTTPs on backend**.

4. Save the settings for the SAP Content Repository.

![sap_inst_004_https_001]({% link sap/images/sap_inst_004_https_001.png %})

> **Note:** Make sure you remove the non-SSL Port Number, otherwise the connection will fail.

Import the certificate from Content Services to the Personal Security Environment (PSE) in SAP.

### Import Alfresco Certificate in SAP PSE {#importcertinsappse}

Import the certificate to the SAP Personal Security Environment.

Make sure you have the certificate from Content Services webserver available.

To import the certificate to the SAP {% include tooltip.html word="SAP_PSE" text="PSE" %} follow these steps:

1. Open transaction `STRUST`.

2. Check whether a `SSL Client (Standard)` {% include tooltip.html word="SAP_PSE" text="PSE" %} exists.

    > **Note:** If there is no `SSL Client (Standard)` PSE available yet, select `SSL Client (Standard)` entry and use the context menu to create a new PSE. Use default settings, if applicable.

3. Select the PSE (double-click) for `SSL Client (Standard)` and scroll down on the settings screen. At the bottom there is a button for uploading the certificate.

    ![sap_inst_004_https_003_strust_pse_import_certificate]({% link sap/images/sap_inst_004_https_003_strust_pse_import_certificate.png %})

4. Upload the certificate previously downloaded from the Content Services webserver ([Get current certificate from Alfresco](#getcertfromalfresco)).

5. Once imported, enter the **Edit** mode (menu **Display ↔ Change**) and click on **Add to Certificate List**.

    ![sap_inst_004_https_003_strust_pse_certificate_add]({% link sap/images/sap_inst_004_https_003_strust_pse_certificate_add.png %})

6. The certificate should now appear in the **Certificates List** of the screen.

    ![sap_inst_004_https_003_strust_certificate_save]({% link sap/images/sap_inst_004_https_003_strust_certificate_save.png %})

7. **Save** the changes.

### Restart SAP Internet Communication Manager

You can restart the Internet Communication Server (ICM) to apply the certificate to the SAP system. Make sure the certificate from the Content Services webserver was successfully imported in SAP {% include tooltip.html word="SAP_PSE" text="PSE" %}.

1. Open transaction `SMICM`.

2. Restart the SAP ICM in menu **More > Administration > ICM**.

    ![sap_inst_004_https_004_smicm_restart]({% link sap/images/sap_inst_004_https_004_smicm_restart.png %})

Next, test the communication via a secured connection.

### (Optional) Test secured connection

To test the secure connection from the SAP side:

1. Open transaction `SM59`.

2. Review the current HTTP connections to external servers by expanding the **HTTP Connections to External Server** section. In this section a new entry must be created pointing to Content Services.

3. Create a new RFC Destination via the **Create** icon with connection type `G HTTP connection to external server` and a name, then click **Continue**.

    ![sap_inst_004_https_005_sm59_create]({% link sap/images/sap_inst_004_https_005_sm59_create.png %})

4. Now, in the **Technical Settings** section, enter the Content Services **Host** along with the **SSL Port** and use `/alfresco` as the **Path Prefix**.

    ![sap_inst_004_https_005_sm59_create_2]({% link sap/images/sap_inst_004_https_005_sm59_create_2.png %})

5. Switch to section **Logon & Security** and scroll down to **Security Options > Status of Secure Protocol**. Select `Active` for **SSL** and choose `DEFAULT SSL Client (Standard)` as **SSL Certificate**.

    ![sap_inst_004_https_005_sm59_create_3]({% link sap/images/sap_inst_004_https_005_sm59_create_3.png %})

6. **Save** the settings.

7. Click **Connection Test** in the toolbar.

    ![sap_inst_004_https_005_sm59_test]({% link sap/images/sap_inst_004_https_005_sm59_test.png %})

8. Review the test result. The connection should work and return with HTTP status code `200` .

    ![sap_inst_004_https_005_sm59_testresult]({% link sap/images/sap_inst_004_https_005_sm59_testresult.png %})

9. The newly created RFC Destination is now available in section **HTTP Connections to External Servers** for transaction `SM59` and can be tested at any time.

The communication via HTTPS should work fine between the SAP system and Content Services.

## Using encrypted passwords {#encryptpwd}

Encrypt all passwords used in the `alfresco-global.properties` by the SAP Connector instead of storing it as plain-text. Make sure the SAP Connector is configured properly and working as expected.

1. Go to [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2. Download the related JAR file:

    ```text
    sap-content-connector-encryptor-2.0.jar
    ```

3. Create a public key and private key:

    Navigate to the folder of the downloaded JAR and run the following command to create the key pair in the current path:

    ```bash
    java –jar sap-content-connector-encryptor-2.0.jar init -path .
    ```

    Two files are created:

    * `sapContentConnectorPrivateKey.pri` (private key)
    * `sapContentConnectorPublicKey.pub` (public key)

4. Create an encrypted password:

    ```bash
    java -jar sap-content-connector-encryptor-2.0.jar encrypt -password H3ll0W0rlD112! -publicKey ./sapContentConnectorPublicKey.pub
    ```

    The encrypted password will be printed to the console, for example:

    ```text
    ENC(XbfE4Z112==)
    ```

    Since it's already surrounded by the required `ENC()` function, it can be copied and used as-is.

5. Upload the private key file to Content Services.

    To be able to resolve the password, the previously created private key (`sapContentConnectorPrivateKey.pri`) must be uploaded to the application server root directory (such as `/usr/local/tomcat/sapContentConnectorPrivateKey.pri`).

6. Provide encrypted password.

    To use the encrypted password, paste it as a value for the required properties in the `alfresco-global.properties` file.

    For example:

    ```text
    integrations.sap.system.1.al.alfrescoPassword = **ENC(XbfE4Z112==)**
    ```

7. Restart the application server since `alfresco-global.properties` has changed.

The passwords are now encrypted and not plain-text.
---
title: Advanced configuration
---

This chapter describes all additional configuration options for the SAP Connector to replicate metadata from the SAP Business Object to the document in Content Services.

If a document is stored in SAP via the SAP Content-Server HTTP-Interface on a content server, SAP submits only three additional properties in the HTTP-request (besides the content itself). These are the `SAP Content Repository` (name of the SAP Content Repository), the `SAP Document Id` (unique number created from SAP to identify the object) and the `SAP Component Id` (hidden in the Alfresco Share UI because of non-human readable values). The additional parameters will show up in an aspect with name `SAP Connection Details` at the document.

![sap_conf_aspect_sap-connection-details]({% link sap/images/sap_conf_aspect_sap-connection-details.png %})

However, there may be a lot of additional reasons to have more information from the SAP Business Object in Content Services available than just these few, which are also not very meaningful to a user, by the way.

The SAP Connector offers the capability to make additional metadata available outside SAP already by default. To get additional metadata out of SAP and store it at the document in Content Services, the connection to SAP is done through the SAP Java Connector (JCo). Furthermore, the SAP Connector takes advantage of different ways to trigger an action which results in the metadata replication.

These are mainly Jobs and Behaviors, but also event-based action is possible. The replicated information will be provided in connexas related aspects at the documents in Content Services.

## Enable Alfresco - SAP communication

This chapter basically describes all additional configuration settings for the SAP Connector to replicate metadata from the SAP Business Object to the document in Content Services.

The SAP Connector takes advantage of the SAP JavaConnector to establish the connection from Content Services to the SAP system. The required connection properties must be provided in the `alfresco-global.properties` file. All related properties are already available in this file, but must still be adapted to your SAP system.

The following property keys are required for the connection - see [Configure repository properties]({% link sap/latest/install/index.md %}#configrepo) for details.

* `integrations.sap.system.1.enabled`
* `integrations.sap.system.1.name`
* `integrations.sap.system.1.host`
* `integrations.sap.system.1.client`
* `integrations.sap.system.1.systemNumber`
* `integrations.sap.system.1.user`
* `integrations.sap.system.1.password`
* `integrations.sap.system.1.language`
* `integrations.sap.system.1.webClient.enabled`
* `integrations.sap.system.1.webClient.url`
* `integrations.sap.system.1.jobs.sapContentConnectorReplicate.enabled`
* `integrations.sap.system.1.jobs.sapContentConnectorReplicate.cronExpression`
* `integrations.sap.system.1.jobs.sapContentConnectorPlus.enabled`
* `integrations.sap.system.1.jobs.sapContentConnectorPlus.cronExpression`
* `integrations.sap.system.1.jobs.sapContentConnectorBarcode.enabled`
* `integrations.sap.system.1.jobs.sapContentConnectorBarcode.cronExpression`
* `integrations.sap.system.1.jobs.sapContentConnectorDirReplicate.enabled`
* `integrations.sap.system.1.jobs.sapContentConnectorDirReplicate.cronExpression`

> **Important:** The properties above are only required to connect from Content Services to SAP. There are still other properties required to specify a valid SAP System Configuration. See [Installing SAP Connector]({% link sap/latest/install/index.md %}).

1. SAP Content Repositories

    There is no limitation in the number of SAP Content Repositories that can be created and connected to Content Services (only SAP restrictions apply). For one connected SAP system you can use one SAP System Configuration of the SAP Connector in the `alfresco-global.properties`. All SAP Content Repository names can be entered as comma-separated list for the `archiveIds` parameter. Example:

    `integrations.sap.system.1.al.archiveIds = Archive1[,Archive2, ArchiveN]`

2. Using Wildcard

    The usage of a Wildcard (`*`) for parameter `archiveIds` is not recommended anymore. For setting up metadata replication specify each SAP Content Repository by its name in the `archiveIds` parameter.

### Configure jobs

The SAP Connector offers a couple of predefined jobs which accomplishes different tasks. This section describes all available jobs with their purpose and how each of them can be configured.

The jobs connect from Content Services to the SAP system via the SAP Java Connector. Each job invokes a different function module on the SAP side. Values that are returned (except for the [Job: sapContentConnectorBarcode](#sapContentConnectorBarcodeJob)), are stored in properties and displayed within a separate aspect on the document.

> **Note:** The CRON trigger beans for all available jobs are disabled by default in the `alfresco-global.properties`.

#### Enable / disable jobs (CRON trigger bean)

The SAP Connector offers the capability to disable the related CRON trigger bean of each job during Content Services startup. This must be done in the `alfresco-global.properties`. Once disabled, the class for the job is never executed, which takes load from the system.

> **Note:** The recommendation is to disable the CRON trigger beans for each job that is not needed.

> **Note:** This affects **all** SAP Content Repositories which are defined for the related SAP System Configuration. Once a CRON trigger bean for a job is disabled in the `alfresco-global.properties`, the related setting at the repository file has no effect.

#### SAP Function Modules

The following table lists the SAP function modules or tables, invoked by the different jobs.

| Job Name | SAP Function Module or Table |
| -------- | ---------------------------- |
| sapContentConnectorReplicate | `ARCHIV_GET_CONNECTIONS` |
| sapContentConnectorPlus | Table `TOAAT` |
| sapContentConnectorBarcode | `BAPI_BARCODE_SENDLIST` |
| sapContentConnectorDirReplicate | `BAPI_DOCUMENT_GETDETAIL2` |

#### Job: sapContentConnectorReplicate {#sapContentConnectorReplicateJob}

The job is responsible for replicating common metadata of the SAP Business Object to make it available at the associated document in Content Services. The job can be enabled and used without any further requirement or prerequisites.

The following table lists all the metadata that's accessible to the standard functional module and that will be replicated:

| Property | Description |
| -------- | ----------- |
| SAP Client | The SAP client that was used to store the document on the SAP side. |
| SAP Object Type | The SAP business object type that's linked to the document. |
| SAP Document Type | The SAP ArchiveLink document type which the document has been stored within SAP. |
| SAP Object Id | The SAP Business Object Id (unique identifier in SAP) that's linked to the document. |
| SAP Reserve | The file extension of the document stored from SAP, e. g. PDF. |
| SAP Archive Date | The date when the current document was stored in Content Services or when an existing document was connected to SAP. |
| SAP Deletion Date | The deletion date that's usually used to save the earliest date that the object can be deleted from the connected archive. This information will only be available if the customization on the SAP side has been done accordingly (i.e. maintains the retention period in transaction `OAC3`). |

The metadata will appear in an aspect `SAP Replicate Details` for the document in Content Services.

![sap_conf_aspect_sap-replicate]({% link sap/images/sap_conf_aspect_sap-replicate.png %})

##### Enable / disable job

The job can be enabled or disabled at the repository file for each SAP Content Repository:

1. Navigate to related SAP Content Repository folder **Data Dictionary > SAP Content Connector > SAP Repositories > XX**.
2. Edit properties of the file **XX Repository**.
3. In aspect `SAP Connection Repository Details`, there is text-field `Enabled Jobs` available containing a list of all jobs of the SAP Connector.

    ![sap_conf_aspect_sap-connection_repository_jobs]({% link sap/images/sap_conf_aspect_sap-connection_repository_jobs.png %})

    1. To disable the job, remove the text `sapContentConnectorReplicate` (including the comma) from the field and save the file.
    2. To enable the job, add the text `**sapContentConnectorReplicate**` to the field and save the file. You may need to add a comma before it to correctly format the comma-separated list. Click the question mark besides the field to show the help text, including a list of all possible values.

        > **Note:** The changes reflects immediately. There is no restart of Content Services required.

> **Note:** The job is always enabled (present as list value in this field) by default, once a new SAP Content Repository is created (see [1. Create SAP Content Repository]({% link sap/latest/config/index.md%}#basic-createsapcontentrepo)). In contrast the CRON trigger bean in the `alfresco-global.properties` is always disabled by default.

##### Execution time

The execution time for the job is stored as a value for the following property of the related SAP System Configuration:

```text
integrations.sap.system.1.jobs.sapContentConnectorReplicate.cronExpression = 0 0/1 * 1/1 * ? *
```

This value is a CRON expression that provides the most flexible way of executing the job. By default, the job is triggered every full minute.

##### CRON trigger bean

To disable the CRON trigger bean for the `sapConnectorReplicate` job, set the following property key in the `alfresco-global.properties` to `false` (remember the desired SAP System Configuration):

```text
integrations.sap.system.1.jobs.sapConnectorReplicate.enabled = false
```

Once the job is disabled, the related setting on the repository file (see above) is no longer considered and has no effect.

> **Note:** Changing the execution time or enabling/disabling the job requires a restart of Content Services.

#### Job: sapContentConnectorPlus {#sapContentConnectorPlusJob}

The job is responsible for replicating additional metadata of the SAP Business Object to make it available at the associated document in Content Services. The job can be enabled and used without any further requirement or prerequisites.

The following table lists the additional metadata that will be replicated:

| Property | Description |
| -------- | ----------- |
| SAP Creator | The SAP user name who stored the document. |
| SAP File Name | The original filename of the uploaded file. |
| SAP Description | The short description field where the user can enter some brief information in SAP before storing the document. |

The metadata will appear in an aspect `SAP Replicate Plus Details` for the document in Content Services. For example, this information can be used to rename the document in Content Services with its original name (instead of *data*) and / or to provide the description of the SAP Business Object also as description for the document in Content Services.

![sap_conf_aspect_sap-replicate_plus]({% link sap/images/sap_conf_aspect_sap-replicate_plus.png %})

##### Enable / disable job - sapContentConnectorPlus

The job can be enabled or disabled at the repository file for each SAP Content Repository.

1. Navigate to related SAP Content Repository folder **Data Dictionary > SAP Content Connector > SAP Repositories > XX**
2. Edit the properties of the file **XX Repository**.
3. In aspect `SAP Connection Repository Details`, there is text-field `Enabled Jobs` available containing a list of all jobs of the SAP Connector.

    ![sap_conf_aspect_sap-connection_repository_jobs]({% link sap/images/sap_conf_aspect_sap-connection_repository_jobs.png %})

    1. To disable the job, remove the text `sapContentConnectorPlus` (including the comma) from the field and save the file.
    2. To enable the job, add the text `sapContentConnectorPlus` to the field (there might be a need to add a comma before as this is a comma-separated list) and save the file. Click the question mark besides the field to show a help including all possible values.

        > **Note:** The changes reflects immediately. There is no restart of Content Services required.

> **Note:** The job is always enabled (present as list value in this field) by default, once a new SAP Content Repository is created (see [1. Create SAP Content Repository]({% link sap/latest/config/index.md %}#basic-createsapcontentrepo)). In contrast the CRON trigger bean in the `alfresco-global.properties` is always disabled by default.

##### Execution time - sapContentConnectorPlus

The execution time for the job is stored as a value for the following property of the related SAP System Configuration:

```text
integrations.sap.system.1.jobs.sapContentConnectorPlus.cronExpression = 0 0/1 * 1/1 * ? *
```

This value is a CRON expression that provides the most flexible way of executing the job. By default, the job is triggered every full minute.

##### CRON trigger bean - sapContentConnectorPlus

To disable the CRON trigger bean for the `sapContentConnectorPlus` job, set the following property key in the `alfresco-global.properties` to `false` (remember the desired SAP System Configuration):

```text
integrations.sap.system.1.jobs.sapContentConnectorPlus.enabled = false
```

Once the job is disabled, the related setting on the repository file (see above) is no longer considered and has no effect.

> **Note:** Changing the execution time or enabling/disabling the job requires a restart of Content Services.

#### Job: sapContentConnectorBarcode {#sapContentConnectorBarcodeJob}

The job is responsible for storing related information from the documents having the `SAP Barcode Details` aspect in the external Barcode table of the SAP system. The job requires the related [Behavior: sapContentConnectorBarcode](#sapContentConnectorBarcodeBehavior) as well as SAP customization (see below). The job is implemented for batch processing. This means, all existing Barcode documents in Content Services will be considered and processed as long as they are not already successfully linked.

In Content Services the aspect `SAP Barcode Details` is related to the job. This aspect must be present at the document to be considered as barcode document that should be linked to SAP by the job.

![sap_conf_aspect_sap-barcode]({% link sap/images/sap_conf_aspect_sap-barcode.png %})

If the `SAP Barcode Details` aspect is added to a document, the related [Behavior: sapContentConnectorBarcode](#sapContentConnectorBarcodeBehavior) is invoked automatically and will add the required `SAP Connection Details` aspect to the document. Therefore, also the mandatory `SAP Content Repository` of this aspect must be set.

The following table lists the additional data of the aspect required for the job. Both properties are mandatory:

| Property | Description |
| -------- | ----------- |
| SAP Barcode | The barcode. |
| SAP Document Class | The file extension of the document, e.g. PDF. |

##### Enable / disable job: sapContentConnectorBarcode

The job can be enabled or disabled at the repository file for each SAP Content Repository.

1. Navigate to related SAP Content Repository folder **Data Dictionary > SAP Content Connector > SAP Repositories > XX**
2. Edit the properties of the file **XX Repository**.
3. In aspect `SAP Connection Repository Details`, there is text-field `Enabled Jobs` available containing a list of all jobs of the SAP Connector.

    ![sap_conf_aspect_sap-connection_repository_jobs_barcode]({% link sap/images/sap_conf_aspect_sap-connection_repository_jobs_barcode.png %})

    1. To disable the job, remove the text `sapContentConnectorBarcode` (including the comma before the name) from the field and save the file.
    2. To enable the job, add the text `sapContentConnectorBarcode` to the field (there might be a need to add a comma before as this is a comma-separated list) and save the file. Click the question mark besides the field to show a help including all possible values.

        > **Note:** Make sure the related behavior with same name is also enabled and therefore available in field for **Enabled Behaviors**.

        > **Note:** The changes reflects immediately. There is no restart of Content Services required.

> **Note:** The job is always enabled (present as list value in this field) by default, once a new SAP Content Repository is created (see [1. Create SAP Content Repository]({% link sap/latest/config/index.md %}#basic-createsapcontentrepo)). In contrast the CRON trigger bean in the `alfresco-global.properties` is always disabled by default.

##### Execution time - sapContentConnectorBarcode

The execution time for the job is stored as a value for the following property of the related SAP System Configuration:

```text
integrations.sap.system.1.jobs.sapContentConnectorBarcode.cronExpression = 0 0/1 * 1/1 * ? *
```

This value is a CRON expression that provides the most flexible way of executing the job. By default, the job is triggered every full minute.

##### CRON trigger bean - sapContentConnectorBarcode

To disable the CRON trigger bean for the `sapContentConnectorBarcode` job, set the following property key in the `alfresco-global.properties` to `false` (remember the desired SAP System Configuration):

```text
integrations.sap.system.1.jobs.sapContentConnectorBarcode.enabled = false
```

Once the job is disabled, the related setting on the repository file (see above) is no longer considered and has no effect.

##### SAP customization

To run the `sapContentConnectorBarcode` job, the SAP system requires some customization to set up the barcode scenario.

1. Open transaction `SPRO` then click on **SAP Reference {% include tooltip.html word="SAP_IMG" text="IMG" %}**
2. Navigate though the structure shown below to find all related customization settings for `Bar Code Scenarios` (alternatively, enter the customization section via transaction `OAM1`).

    ![sap_conf_barcode_customization_sap]({% link sap/images/sap_conf_barcode_customization_sap.png %})

3. Proceed with the necessary customization.

> **Note:** Detailed information about the SAP customizing for Barcode scenarios can be found in the SAP ArchiveLink documentation *Storage Scenarios with Integration of Bar Code Technology*.

#### Job: sapContentConnectorDirReplicate

The job is responsible for replicating metadata from a SAP Document Info Record (DIR) and make it available for the associated document in Content Services. It supports metadata replication from the DIR document as well as from the superior document (pre-document), if exists. Furthermore, the `Draft` state of a DIR for documents uploaded through SAP Fiori applications is supported.

The following table lists the metadata that will be replicated from the SAP Document Info Record:

| Property | Description |
| -------- | ----------- |
| Document Type | The document type of the object which is used to identify the document. |
| Document Number | The document number which is used to identify the document. |
| Document Part | Section of a document which is maintained as an independent document. Design departments, for example, can use document parts to divide up large documents such as design drawings into pages. |
| Document Version | The document version. |
| Description | The description from the Document Info Record. |
| SAP User | The user in SAP who has created the document info record. |
| SAP Client | The client in SAP which was used during the document info record creation. |
| Deletion Flag | Shows whether the document is to be deleted during the next reorganization run. |
| CAD Indicator | Shows whether the object (e.g. BOM) was changed in the CAD system (Pro/Engineer, CATIA,..) or not. |
| Document Structure | Shows whether the object is part of a document structure. |
| Document State (internal) | Document status field. |
| Document State (external) | State of the document (language dependent) depending on the underlying status network. |
| Lab/Office | Key for the design office, laboratory, or laboratory worker responsible. |
| Change Number | Number of the change master record which groups together logically linked documents and any other SAP objects (such as bill of material, routing, material). |
| Valid From | Date, from which the change object (for example, document) change is effective with the corresponding change number. |
| Authorization Group | The authorization group which is used to enable protect access. |
| Status Log | The status logs for each status change. |

The following metadata will be replicate from the related superior document, if any:

| Property | Description |
| -------- | ----------- |
| Document Type | The document type of the superior document must not be the same as that of the document you are currently processing. |
| Document Number | The document number of the superior document. |
| Document Part | Section of the document, used as part of the document key identifying the superior document. |
| Document Version | Document version, used as part of the document key identifying the superior document. |

The metadata will appear in aspects `SAP Document Info Record (DIR) Details` and `SAP DIR Superior Document Details` for the document in Content Services.

![sap_conf_aspect_sap-dir]({% link sap/images/sap_conf_aspect_sap-dir.png %})

##### SAP customization prerequisites

To use the SAP Document Info Record replication job, the SAP Content Repository must be set up in a different way than explained earlier in [(1) Create SAP Content Repository](#basic-createsapcontentrepo). The important change must be done in the **Document Area** selection. Instead of `Archivelink` the value `Document Management System` must be selected. Hence, always use a different SAP Content Repository than for Archivelink.

![sap_conf_003_create_repo_values_dms]({% link sap/images/sap_conf_003_create_repo_values_dms.png %})

> **Note:** Always use also a separate SAP System Configuration for SAP Document Management Service (DMS) related scenarios in the `alfresco-global.properties` and disable the CRON trigger bean at least for the [Job: sapContentConnectorReplicate](#sapContentConnectorReplicateJob) and [Job: sapContentConnectorPlus](#sapContentConnectorPlusJob).

##### Enable `Draft` state

The job also supports the `Draft` state for SAP Document Info Records. This state comes into place if documents are uploaded through SAP Fiori applications. To consider the `Draft` state, a flag must be enabled on the repository file to replicate metadata even if the document is still in `Draft` state.

To enable the `Draft` state:

1. Navigate to related SAP Content Repository folder **Data Dictionary > SAP Content Connector > SAP Repositories > M3**
2. Edit the properties of the file **M3 Repository**.
3. In aspect `SAP Connection Repository Details` enable the flag for `Enable Draft for SAP Document Info Records (DIR)`

    ![sap_conf_aspect_sap-connection_repository_dir_draft]({% link sap/images/sap_conf_aspect_sap-connection_repository_dir_draft.png %})

##### Enable / disable job - sapContentConnectorDirReplicate

The job can be enabled or disabled at the repository file for each SAP Content Repository.

1. Navigate to related SAP Content Repository folder **Data Dictionary > SAP Content Connector > SAP Repositories > XX**
2. Edit the properties of the file **XX Repository**.
3. In aspect `SAP Connection Repository Details`, there is text-field `Enabled Jobs` available containing a list of all jobs of the SAP Connector.

    ![sap_conf_aspect_sap-connection_repository_jobs]({% link sap/images/sap_conf_aspect_sap-connection_repository_jobs.png %})

    1. To enable the job, add the text `sapContentConnectorDirReplicate` to the field (there might be a need to add a comma before as this is a comma-separated list) and save the file. Click the question mark besides the field to show a help including all possible values.

        > **Note:** The changes reflects immediately. There is no restart of Content Services required.

    2. To disable the job, remove the text `sapContentConnectorDirReplicate` from the field and save the file.

> **Note:** The job is always **disabled** (different than for the other jobs) by default, once a new SAP Content Repository is created (see [1. Create SAP Content Repository]({% link sap/latest/config/index.md %}#basic-createsapcontentrepo)). Like the other jobs, it the CRON trigger bean in the `alfresco-global.properties` is also disabled by default. This means, you have to enable this job on two places.

##### Execution time - sapContentConnectorDirReplicate

The execution time for the job is stored as a value for the following property of the related SAP System Configuration:

```text
integrations.sap.system.1.jobs.sapContentConnectorDirReplicate.cronExpression = 0 0/1 * 1/1 * ? *
```

This value is a CRON expression that provides the most flexible way of executing the job. By default, the job is triggered every full minute.

##### CRON trigger bean - sapContentConnectorDirReplicate

To disable the CRON trigger bean for the `sapContentConnectorDirReplicate` job, set the following property in the `alfresco-global.properties` to `false` (remember the desired SAP System Configuration):

```text
integrations.sap.system.1.jobs.sapContentConnectorDirReplicate.enabled = false
```

Once the job is disabled, the related setting on the repository file (see above) is no longer considered and has no effect.

> **Note:** Changing the execution time or enabling/disabling the job requires a restart of Content Services.

### Configure behaviors

The SAP Connector offers three behaviors which accomplishes different tasks on updating or creating documents.

The behaviors connect from Content Services to the SAP system via the SAP Java Connector. Each behavior invokes a different function module on the SAP side. In contrast to the Jobs, Behaviors are used to trigger an action on the SAP side rather then replicate metadata. The following behaviors are available:

| Behavior Name | Description |
| ------------- | ----------- |
| sapContentConnectorCreateArchivelink | Connect documents stored in Alfresco to existing SAP Business Objects. |
| sapContentConnectorBarcode | Add the barcode to the SAP external barcode table. |
| sapContentConnectorWorkflow | Start a SAP Workflow for a specified SAP user attaching the current document. |

> **Important:** Check with your SAP sales representative if the behavior triggered remote access to SAP is covered by the existing SAP license of your company.

#### Behavior: sapContentConnectorCreateArchivelink {#createArchivelinkBehavior}

The behavior is responsible to connect the current document based on entered metadata to an existing SAP Business Object. Therefore, the `SAP Create Archivelink Aspect` is used. To connect a document to an SAP Business Object, the `SAP Create Archivelink Aspect` must be added and its values must be filled. Along with the `SAP Create Archivelink Aspect` the `SAP Connection Details` aspect will be added automatically.

Once all mandatory properties of the aspects are set and the document is saved, the behavior fires `onUpdateProperties` and invokes a SAP function module which will create the related entries in the SAP tables based on the aspect data. The current document is then available in the attachment list of the related SAP Business Object.

The following table lists the required data of the aspect which are required to connect the SAP Business Object:

| Property  | Description |
| --------- | ----------- |
| SAP Document Type | The document type associated with the current `SAP Object Type`. |
| SAP Client | The SAP client used to store in the SAP tables. |
| SAP Object Id | The object id of the SAP Business Object where the current document should be connected to. |
| SAP Object Type | The object type (e.g. `BKPF`, `EQUI`, `BUS2012`,...). |
| SAP Document Class | Document class (e.g. PDF). |
| SAP Filename | The file name used to display in the attachment list of the SAP Business Object. |
| SAP Description | The description used as short-description for the attachment in the attachment list |
| SAP Creator | The SAP user that should be used in SAP as creator of the attachment. |
| SAP Archive Date | The archive date to be stored in SAP. |

Because the `SAP Connection Details` aspect was automatically added along with the `SAP Replicate Plus Details`,
there is a need to set the mandatory `SAP Content Repository` as well.

The `SAP Replicate Plus Details` and `SAP Connection Details` aspects with example values:

![sap_conf_aspect_sap-createarchivelink]({% link sap/images/sap_conf_aspect_sap-createarchivelink.png %})

##### Enable / Disable behavior - sapContentConnectorCreateArchivelink

The behavior can be enabled or disabled at the repository file for each SAP Content Repository.

1. Navigate to related SAP Content Repository folder **Data Dictionary > SAP Content Connector > SAP Repositories > XX**
2. Edit the properties of the file **XX Repository**.
3. In aspect `SAP Connection Repository Details`, there is text-field **Enabled Behaviors** available containing a list of all behaviors of the SAP Connector.

    ![sap_conf_aspect_sap-connection_repository_behavior]({% link sap/images/sap_conf_aspect_sap-connection_repository_behavior.png %})

    1. To disable the behavior, remove the text `sapContentConnectorCreateArchivelink` (including the comma) from the field and save the file.
    2. To enable the behavior, add the text `sapContentConnectorCreateArchivelink` to the field (there might be a need to add a comma before as this is a comma-separated list) and save the file. Click the question mark besides the field to show a help including all possible values.

        > **Note:** The changes reflects immediately. There is no restart of Content Services required.

> **Note:** The behavior is always enabled (present as list value in this field) by default, once a new SAP Content Repository is created (see [1. Create SAP Content Repository]({% link sap/latest/config/index.md %}#basic-createsapcontentrepo)).

> **Important:** Check with your SAP sales representative if the behavior triggered remote access to SAP is covered by the existing SAP license of your company.

#### Behavior: sapContentConnectorBarcode {#sapContentConnectorBarcodeBehavior}

This behavior will add the `SAP Connection Details` aspect to each document where the aspect `SAP Barcode Details` was added before. With this, the [Job: sapContentConnectorBarcode](#sapContentConnectorBarcodeJob) is able to process the documents.

> **Note:** Always enable/disable the Barcode behavior together with the Barcode job. Just one of both enabled would result that the Barcode scenario is not working.

##### Enable / Disable the behavior - sapContentConnectorBarcode

The behavior can be enabled or disabled at the repository file for each SAP Content Repository.

1. Navigate to related SAP Content Repository folder **Data Dictionary > SAP Content Connector > SAP Repositories > XX**
2. Edit the properties of the file **XX Repository**.
3. In aspect `SAP Connection Repository Details`, there is text-field **Enabled Behaviors** available containing a list of all behaviors of the SAP Connector.

    ![sap_conf_aspect_sap-connection_repository_behavior]({% link sap/images/sap_conf_aspect_sap-connection_repository_behavior.png %})

    1. To disable the behavior, remove the text `sapContentConnectorBarcode` (including the comma) from the field and save the file.

        > **Note:** If disabled, also the related Job with same name in the **Enabled Jobs** field should be disabled.

    2. To enable the behavior, add the text `sapContentConnectorBarcode` to the field (there might be a need to add a comma before as this is a comma-separated list) and save the file. Click the question mark besides the field to show a help including all possible values.

        > **Note:** The changes reflects immediately. There is no restart of Content Services required.

> **Note:** The behavior is always enabled (present as list value in this field) by default, once a new SAP Content Repository is created (see [1. Create SAP Content Repository]({% link sap/latest/config/index.md %}#basic-createsapcontentrepo)).

#### Behavior: sapContentConnectorWorkflow {#workflowBehavior}

The behavior will create a new inbox task for a SAP user in his SAP Business Workplace (transaction `SBPW`) in the SAP system. The current document will be attached to this task as a reference link. The inbox task can be related to any SAP Workflow then (depends on SAP customizing). To invoke the behavior, the `SAP Workflow Details` aspect must be added to a document in Content Services. Along with this aspect the required `SAP Connection Details` aspect is added automatically. The mandatory aspect values must be filled and if the properties are saved, the behavior is invoked (`onUpdateProperties`).

The following table lists the required data of the aspect that's required to create the inbox task for the SAP user:

| Property  | Description |
| --------- | ----------- |
| Start SAP Workflow | Whether to create the SAP Workflow inbox task for the `Username` below if the properties are saved. |
| SAP Document Type | The document type customized with the Workflow. |
| SAP Document Class | Document class (e.g. PDF). |
| Userclass | The userclass. |
| Username | The user name of the SAP user which should receive the inbox task. |
| Late Archiving | To use late archiving or not. |

Here's the view from Alfresco Share if the aspects are available:

![sap_conf_aspect_sap-workflow]({% link sap/images/sap_conf_aspect_sap-workflow.png %})

##### Enable / Disable the behavior - sapContentConnectorWorkflow

The behavior can be enabled or disabled at the repository file for each SAP Content Repository.

1. Navigate to related SAP Content Repository folder **Data Dictionary > SAP Content Connector > SAP Repositories > XX**
2. Edit the properties of the file **XX Repository**.
3. In aspect `SAP Connection Repository Details`, there is text-field **Enabled Behaviors** available containing a list of all behaviors of the SAP Connector.

    ![sap_conf_aspect_sap-connection_repository_behavior]({% link sap/images/sap_conf_aspect_sap-connection_repository_behavior.png %})

    1. To disable the behavior, remove the text `sapContentConnectorWorkflow` (including the comma) from the field and save the file.
    2. To enable the behavior, add the text `sapContentConnectorWorkflow` to the field (there might be a need to add a comma before as this is a comma-separated list) and save the file. Click the question mark besides the field to show a help including all possible values.

        > **Note:** The changes reflects immediately. There is no restart of Content Services required.

> **Note:** The behavior is always enabled (present as list value in this field) by default, once a new SAP Content Repository is created (see [1. Create SAP Content Repository]({% link sap/latest/config/index.md %}#basic-createsapcontentrepo)).

> **Important:** Check with your SAP sales representative if the behavior triggered remote access to SAP is covered by the existing SAP license of your company.

### SAP Connector content model types

The SAP Connector offers a couple of predefined content model types which accomplishes the different tasks of the available jobs. This section describes all available content model types with their purpose.

The available content model types are closely related to the available SAP Connector jobs ([Configuring jobs](#configure-jobs)) and SAP Connector behaviors ([Configuring behaviors](#configure-behaviors)). The types are already prepared with the necessary aspects.

The SAP Connector offers the following predefined content model types:

* SAP ArchiveLink Document
* SAP Barcode
* SAP Workflow

#### Changing content model types

To change the existing type of the document to a SAP Connector type, follow the Content Services documentation for **Change Type**. The following screenshot shows the available types while executing the **Change Type** action in Alfresco Share:

![sap_conf_types_change_contenttype]({% link sap/images/sap_conf_types_change_contenttype.png %})

> **Note:** A special case for all SAP Connector Content Model types, the `SAP Document Id` in aspect `SAP Connection Details`, is usually created by SAP internally (with a unique number). Because these SAP Connector scenarios all start from Content Services and not from the SAP side, there is a need to create these Ids in Content Services. Therefore, to get a unique number, the SAP Connector uses the UUID of the current document (property `sys:node-uuid`). However, this does not affect the later process.

#### SAP Archivelink Document type {#archivelinktype}

The `SAP Archivelink Document` type allows you to link a document in Alfresco manually to its corresponding business object in SAP. Based on the properties that must be entered during the creation, the connection to the SAP business object will be done automatically.

> **Note:** Make sure you've enabled [Behavior: sapContentConnectorCreateArchivelink](#createArchivelinkBehavior).

To link a document to a corresponding SAP Business Object by the `SAP Archivelink Document` type:

1. Change the type of the document to `SAP Archivelink Document`.
2. Edit the properties of the document and enter all mandatory fields for the `SAP Create Archivelink Details` and `SAP Connection Details` aspects:

    ![sap_conf_types_archivelink_properties]({% link sap/images/sap_conf_types_archivelink_properties.png %})

3. Save the document. Now the [Behavior: sapContentConnectorCreateArchivelink](#createArchivelinkBehavior) will be invoked and call a related SAP function module which will create the necessary table entries.
4. The current document is now available as attachment for the SAP Business Object (matching the aspect values).

> **Note:** To connect a document of any other type, add the `SAP Create Archivelink Details` aspect to that document and provide the related aspect values that match an SAP Business Object.

#### SAP Barcode type

The `SAP Barcode` type allows you to process a document in Alfresco with the barcode scenario (as certified by the SAP HTTP-Content Server). Based on the barcode entered as a value for the related aspect, the SAP Connector invokes an SAP function module which creates the entry in the **External Barcode** table in SAP.

* If the barcode already exists in SAP, the document is available immediately as an attachment for the related SAP Business Object (i.e. Late Archiving).
* If the barcode isn't yet in SAP, the document will be attached to an SAP Business Object when an SAP user enters the barcode (i.e. Early Archiving).

> **Note:** Make sure you've enabled the [Job: sapContentConnectorBarcode](#sapContentConnectorBarcodeJob).

To link a document to an SAP Business Object by the `SAP Barcode` type:

1. Change the type of the document to `SAP Barcode`.
2. Edit the properties of the document and enter the mandatory fields for the `SAP Connection Details` and `SAP Barcode Details` aspects:

    ![sap_conf_types_barcode_properties]({% link sap/images/sap_conf_types_barcode_properties.png %})

3. Save the document.

    Depending on the CRON expression of the [Job: sapContentConnectorBarcode](#sapContentConnectorBarcodeJob), the job will pick up the document and create the necessary entry in the **External Barcode** table (check transaction `OAM1`) of the SAP system.

    * For Late Archiving, the document is immediately available as an attachment on the related SAP Business Object.
    * For Early Archiving, the document is available as soon as the SAP user manually enters the matching barcode on an SAP Business Object.

> **Note:** To use the barcode with any other Content Services content type, add the `SAP Barcode Details` aspect to a document **and** make sure to have the [Behavior: sapContentConnectorBarcode](#sapContentConnectorBarcodeBehavior) **in addition** to the [Job: sapContentConnectorBarcode](#sapContentConnectorBarcodeJob) enabled for the current SAP System Configuration.

#### SAP Workflow type

The `SAP Workflow` type allows you to create a new inbox task (SAP Workflow) for a SAP user with the current document attached. The SAP Workflow to be started must be customized in SAP.

> **Note:** Do not confuse **Alfresco Workflow** with **SAP Workflow**.

> **Note:** Related transaction in SAP to view the inbox tasks of a user: `SBWP`.

To create a new inbox task (SAP Workflow) for a SAP user including the current document by the `SAP Workflow` type, proceed with the following steps:

1. Change the type of the document to `SAP Workflow`.
2. Edit the properties of the document and enter all mandatory fields for the `SAP Connection Details` and `SAP Workflow Details` aspects:

    ![sap_conf_types_sapworkflow_properties]({% link sap/images/sap_conf_types_sapworkflow_properties.png %})

3. If the inbox task should be created immediately, make sure to check **Start SAP Workflow**.
4. Save the document. Now the [Behavior: sapContentConnectorWorkflow](#workflowBehavior) will be invoked and call a related SAP function module (`ARCHIV_PROCESS_RFCINPUT`) which will create the inbox task for the user.

    > **Note:** As long as `Check SAP Workflow` is disabled, the behavior will not consider the current document.

5. The current document is now available as attachment (link to the document in Content Services) of an inbox task assigned to the user in SAP.

## Configure GenericXchange

The GenericXchange module is used for flexible data exchange either via a secure Remote Function Call (RFC/SNC) connection or by invoking an Open Data Protocol (OData) service on the related SAP System (either SAP Cloud Essentials or SAP S/4HANA on-premises).

To configure this module, see the Alfresco Content Connector for SAP Cloud documentation, [Configure GenericXchange]({% link sap-cloud/latest/config/genericxchange.md %}){:target="_blank"}.

## Open associated Business Object in SAP {#openassocbusinessobjinsap}

This feature allows you to open the corresponding SAP Business Object that's linked to a document in Alfresco Share. This action is provided in the **Document Actions** menu, and once clicked it opens the SAP Web-GUI and invokes the SAP Business Object in the related transaction.

The feature is available for documents in Content Services that have the `SAP Replicate Details` aspect applied.

A prerequisite is to have the [Job: sapContentConnectorReplicate](#sapContentConnectorReplicateJob) enabled and running.

> **Note:** To log in to the SAP Web-GUI, an SAP user is required.

### Configuration

Use these steps to configure opening an associated SAP Business Objects in SAP.

1. Before you continue, make sure that the job is enabled: [Job: sapContentConnectorReplicate](#sapContentConnectorReplicateJob).

    The related document action is only available in Alfresco Share, and only for documents with the **SAP Replicate Details** and **SAP Connection Details** aspects applied.

2. The required properties from these aspects are:

    1. `SAP Content Repository` (aspect `SAP Connection Details`)
    2. `SAP Object Type` (aspect `SAP Replicate Details`)
    3. `SAP Object Id` (aspect `SAP Replicate Details`)

3. Set the following properties in the `alfresco-global.properties` for the desired SAP System Configuration:

    | Property | Description |
    | -------- | ----------- |
    | integrations.sap.system.1.webClient.enabled | Enable or disable the feature for all SAP Content Repositories related to the SAP System Configuration. |
    | integrations.sap.system.1.webClient.url | Specify the base URL to the SAP Web application server. |

    > **Note:** Any property changes require a restart of Content Services.

The following table lists all available `SAP Object Types`, which are supported by default, including their associated `Transaction`. These are used to open the corresponding SAP Business Object. The parameter in the `Field Names in URL` column are automatically filled with the related values from the aspects.

| SAP Object Type | SAP Transaction | Field Names in URL |
| --------------- | --------------- | ------------------ |
| BKPF | FB03 | RF05L-BELNR, RF05L-BUKRS, RF05L-GJAHR |
| BUS1065 | PA40 | RP50G-PERNR |
| BUS1001006 | MM03 | RMMG1-MATNR |
| BUS2010 | ME43 | RM06E-ANFNR |
| BUS2012 | ME23 | RM06E-BSTNR |
| BUS2032 | VA03 | VBAK-VBELN |
| BUS2017 | MB03 | RM07M-MBLNR, RM07M-MJAHR |
| BUS2081 | MIR4 | RBKP-BELNR, RBKP-GJAHR |
| BUS2078 | QM03 | RIWO00-QMNUM |
| BUS2081 | MIR4 | RBKP-BELNR, RBKP-GJAHR |
| BUS2105 | ME53 | EBAN-BANFN |
| EQUI | IE03 | RM63E-EQUNR |
| KNA1 | VD03 | RF02D-KUNNR, RF02D-D0110 |
| LFA1 | MK02 | RF02K-LIFNR, RF02K-D0110 |
| PREL | PA20 | RP50G-PERNR |
| VBRK | VF03 | VBRK-VBELN |

If you need to to call anything other than the default SAP Object Types, refer to the following:

* [Advanced configuration](#OpenBusinessObjectSAPAdvancedConfig).
* [Reference for SAP Object Type Mapping]({% link sap/latest/admin/reference.md %}#refsapobjecttypemap).

### Advanced configuration {#OpenBusinessObjectSAPAdvancedConfig}

If there is a need to open SAP Business Objects of `SAP Object Types` which are not covered by default, there is a way to override the default settings globally or even for each SAP System Configuration.

As template file to override these settings use file `webClient-config.properties` in the reference section. Alternatively, this template can be found in the exploded web-application in folder `<app-srv_root>/webapps/alfresco/WEB-INF/classes/alfresco/module/sap-content-connector-repo/webClient-config.properties` as well.

#### Override defaults globally

To override the default settings globally, meaning for each available SAP System Configuration:

1. Extend or change the `webClient-config.properties` template according your needs.
2. Upload the file into folder **Data Dictionary→ SAP Content Connector→ Configuration** (create folder **Configuration** if it does not exists). The changes will reflect immediately.

![sap_feature_openinsap_conf_001]({% link sap/images/sap_feature_openinsap_conf_001.png %})

#### Override defaults for individual SAP System Configuration

It's also possible to override the `SAP Object Types` for an individual SAP System Configuration, hence for a dedicated SAP Content Repository / SAP system. This might be important if there are SAP Content Repositories of different SAP systems (having different versions or patch levels) connected to Content Services which requires different parameters to call the transactions.

The basic approach to override the settings is to extend the the **file name** of `webClient-config.properties` with the number of the SAP System Configuration in the following format:

```text
webClient-config.sap.system.<X>.properties
```

> **Note:** The `.sap.system.` in the name is always fixed, and the `X` must be replaced by the number of the SAP System Configuration.

> **Note:** If there is a need to have at least one individual file available, you must create and upload the files for each other SAP System Configuration as well - even if they just contains the default settings!

To override the settings for an SAP System Configuration:

1. Copy the file `webClient-config.properties` and rename it according the above specification, e.g. to `webClient-config.syp.system.1.properties`.
2. Do the same for each SAP System Configuration in the `alfresco-global.properties`.
3. Extend or change the `webClient-config.sap.system.<X>.properties` according your needs.
4. For all other files leave the default content.
5. Upload all files into folder **Data Dictionary→ SAP Content Connector→ Configuration** (create folder **Configuration** if it does not exists). The changes will reflect immediately.

![sap_feature_openinsap_conf_002]({% link sap/images/sap_feature_openinsap_conf_002.png %})

#### Add a new SAP Object Type

To add a new `SAP Object Type` that allows the user to open the associated SAP Business Object in a transaction that's not covered by default:

1. Provide the `webClient-config.properties` (or individual `webClient-config.sap.system.<X>.properties`) as described above.
2. Enter each new `SAP Object Type` as a new line at the end of the file.
3. Split the `SAP Object Type` and the URL by an equals sign.
4. Provide all necessary parameter for the URL required to invoke the transaction via SAP Web-Gui.

The following macros are supported as values for URL parameter, if applicable :

| Macro Name | Description |
| ---------- | ----------- |
| %SAP_CLIENT% | The SAP Client, specified in the `alfresco-global.properties` for the SAP System Configuration. |
| %SAP_OBJECT% | The `SAP Object Type`, read from aspect value `connexasReplicate:sapobject`. For example `BKPF` (see [Job: sapContentConnectorReplicate](#sapContentConnectorReplicateJob)). |
| %SAP_ARCHIVE_OBJECT% | The `SAP Document Type`, read from aspect value `connexasReplicate:saparchiveobject`. For example `Z_INV_XX`. |
| %SAP_OBJECT_ID% | The `SAP Object Id`, read from aspect value `connexasReplicate:sapobjectid`. |
| %SAP_RESERVE% | The `SAP Reserve`, read from aspect value `connexasReplicate:sapreserve`. For example `PDF`. |

If there is a need to have only a part of the macro value (substring) available for a parameter, the following notation like demonstrated for the `SAP Object Id` below must be used:

```text
%SAP_OBJECT_ID{0:4}%
```

This extracts the substring beginning from 0 to 4. The start index is included while the end index is not included (as usual for Java programming language).

As an example, to override the `SAP Object Type` **BKPF** (opens transaction `FB03`), the following line can be added to the file:

```text
BKPF=?~sap-client=%SAP_CLIENT%**&~transaction=FB03%20RF05LBELNR=%SAP_OBJECT_ID{4:14}%;RF05L-BUKRS=%SAP_OBJECT_ID{0:4}%;RF05LGJAHR=%SAP_OBJECT_ID{14:18}%&~okcode=/00
```
---
title: Configure SAP Connector
nav: false
---

Use this information to configure the SAP Connector. Check the following SAP access privileges in order to continue with the configuration.

To configure the SAP Connector properly on the SAP side, an **SAP dialog user** is required who has access to the following SAP transactions:

| Transaction | Description |
| ----------- | ----------- |
| `OAC0` | Define and maintain SAP Content Repositories which includes the storage system (Alfresco) for the documents. |
| `OAC2` | Define global document types and assign document classes. Required for end-user testing. |
| `OAC3` | Link SAP Content Repositories, document types and SAP object types. Assign retention periods. Required for end-user testing. |
| `SE38` | Run and edit SAP function modules ({% include tooltip.html word="SAP_ABAP" text="ABAP" %} programs). Required for functional testing (RSCMST). |

## Basic configuration

In this section, you'll create and configure a new SAP Content Repository where the "Content Server" is Content Services. In addition, the connection between the SAP Content Repository and Content Services is secured by a certificate and tested.

### 1. Create SAP Content Repository {#basic-createsapcontentrepo}

Create a new SAP Content Repository which points to Content Services.

The maintenance screen for creating new SAP Content Repositories can be accessed with transaction `OAC0`.

1. In the SAP Content Repository overview, click **Display/change** (**CTRL+F4**).

    Another icon appears: **Create** (**F5**). Click on it to create a new SAP Content Repository.

    ![sap_conf_001_0ac0]({% link sap/images/sap_conf_001_0ac0.png %})

2. Enter mandatory values for the new repository.

    See the following table to choose the correct settings.

    * Values in **bold** must match the values given in the table exactly.
    * Values in _italics_ are customer specific and need to be adapted according to your environment.

    ![sap_conf_002_create_repo_initial]({% link sap/images/sap_conf_002_create_repo_initial.png %})

    | Field | Description |
    | ----- | ----------- |
    | Content Rep. | The name of the new repository. Remember the SAP naming conventions (only 2 characters allowed for Archivelink). <br>Value: _XX_ |
    | Description | A brief description for the repository (max 50 characters). <br>Value: _Alfresco Content Services via SAP Connector_ |
    | Document Area | The document area for the documents. <br>Value: **Archivelink** |
    | Storage Type | The storage type of the repository <br>Value: **HTTP content server** |
    | Version no. | Number of the current SAP content server version. For content server version 4.7 enter 0047. <br>Value: _0047_ |
    | HTTP Server | The IP address of the Content Services server - or the Load Balancer. <br>Value: _85.112.116.117_ |
    | Port Number | The port number where the Content Services is listening - usually 8080. <br>Value: _8080_ |
    | SSL Port Number | The port number for secure layer. Only required for [Communication via HTTPS]({% link sap/latest/admin/reference.md %}#securecomms). <br>Value: For now, leave empty. |
    | HTTP Script | The Web Script location in Content Services where all requests from SAP are processed. <br>Value: **alfresco/service/com/alfresco/sap/http** |
    | Transfer drctry | For some ArchiveLink scenarios, files have to be created in a transfer directory (on SAP side) before sending it to the content server. Maintain it, if the default value does not match your company standard. |

3. Click either on icon **Test connection** or on icon **Status information**.

    In both cases, a message appears saying the content repository does not exist.

    > **Note:** Any other message than *Content repository XX does not exist* indicates an issue with the network connection between the SAP server and the Alfresco server. In such a case, double-check the login credentials for Alfresco (`alfresco-global.properties`) and make sure Alfresco is available.

    ![sap_conf_004_create_repo_values_with_check]({% link sap/images/sap_conf_004_create_repo_values_with_check.png %})

4. Save the current repository configuration (click **Save** on the bottom line) before proceeding with the next steps.

5. To create the repository on the content server click on icon **CS Admin** (**C**ontent **S**erver **Admin**istration) in the middle of the screen, besides the **Test connection** icon.

    ![sap_conf_005_cs_admin]({% link sap/images/sap_conf_005_cs_admin.png %})

6. In the administration area, the repository has to be created by the **Create repository** icon on the left. It is available in section **Create**.

    ![sap_conf_006_create_repo_cs_admin]({% link sap/images/sap_conf_006_create_repo_cs_admin.png %})

7. If the repository has been created successfully, you'll be redirected to the **Details** section. At the bottom of this screen, you'll see already some basic repository information coming "live" from Content Services.

    ![sap_conf_007_create_repo_cs_admin_done]({% link sap/images/sap_conf_007_create_repo_cs_admin_done.png %})

8. Click the **Save** (**CTRL + S**) button in the bottom bar to save the changes again.

    After saving, the screen can be closed by clicking on **Exit** button in the top right toolbar.

### 2. Secure connection using a certificate {#basic-secureconnwithcert}

Create a certificate in SAP that will be stored in Content Services to allow only authorized requests from the SAP Content Repository.

By default, all HTTP(S)-requests coming from the SAP Content Repository and arriving via the SAP Connector in Content Services are dropped until a certificate is available and active (you can disable the certificate check in the `alfresco-global.properties` file).

> **Important:** We strongly recommend securing the connection between SAP and Alfresco at all times.

1. Open the newly created SAP Content Repository for editing in transaction `OAC0` again.

2. Navigate to the Content Server Administration by clicking the **CS Admin** button.

3. Switch to section **Certificates** and refer to the **Certificates Properties** table at the bottom (which is still empty).

4. Click the button **Send certificate** (mail icon) to send a certificate to the SAP Content Repository.

    ![sap_conf_008_create_repo_cs_admin_certificate]({% link sap/images/sap_conf_008_create_repo_cs_admin_certificate.png %})

5. The certificate is sent to Content Services. It appears in the table **Certificates Properties** but it's not yet active (since the checkbox in the **Active** column isn't selected).

    ![sap_conf_009_create_repo_cs_admin_certificate_created]({% link sap/images/sap_conf_009_create_repo_cs_admin_certificate_created.png %})

    > **Note:** From the SAP HTTP-Content Server protocol specification, the certificate can only be activated from the content repository side. This is an additional security step. Therefore, no additional action is required in SAP. Switch to Content Services and proceed with the activation in the next step.

### 3. Enable security by activating the certificate

Activate the certificate in Content Services to process authorized requests only.

There are two options for activating the recently sent certificate. Either activate it in the SAP Connector - Administration Console (recommended and preferred way) or manually edit the related property at the certificate document in the Alfresco repository.

1. **Activation via SAP Connector - Administration Console:**

    1. Log in to Alfresco Share and navigate to the SAP Connector - Administration Console (via menu *Admin Tools* > *SAP Integration*).

    2. Scroll down to the related SAP System Configuration where the recently created SAP Content Repository belongs to.

    3. Click the **Enable certificate for content repository XX** button.

        ![sap_conf_010_share_certificate_before]({% link sap/images/sap_conf_010_share_certificate_before.png %})

    4. The connection is now secured by the certificate.

        ![sap_conf_010_share_certificate_after]({% link sap/images/sap_conf_010_share_certificate_after.png %})

2. **Activation by manually editing the certificate properties:**

    1. Log in to Alfresco Share and navigate to the following (new) folder structure in the Alfresco repository to find the recently created certificate document: **Repository > Data Dictionary > SAP Content Connector > SAP Repositories > XX**.

    2. Within the **XX** folder two files are available. The repository file (with name `XX Repository`) and the certificate document (contains the common name of the SAP system in the document name).

        ![sap_conf_011_share_certificate_in_repo]({% link sap/images/sap_conf_011_share_certificate_in_repo.png %})

    3. Edit the properties of the certificate document, and select checkbox **Certificate Active** and **save** the document.

        ![sap_conf_012_share_certificate_properties]({% link sap/images/sap_conf_012_share_certificate_properties.png %})

        The connection is now secured by the certificate.

### 4. Check certificate in SAP

Use this information to confirm that the certificate activation in Content Services reflects in the SAP system for the SAP Content Repository.

To prove that the activation of the certificate from the previous step reflects immediately for the SAP Content Repository, check the certificate section of the SAP Content Repository.

1. In the SAP system, open the created SAP Content Repository in transaction `OAC0` again.

2. Click button **CS Admin**.

3. Switch to **Certificates** section and refer to table **Certificate Properties**.

4. In column **Active** the checkbox is now selected.

    ![sap_conf_013_sap_certificate_active]({% link sap/images/sap_conf_013_sap_certificate_active.png %})

### 5. Functional test

This page describes how the SAP Connector, and therefore the ArchiveLink interface, can be tested. The testing requires some additional SAP fundamentals, and is based on the same procedure used by SAP to certify the SAP Connector content ArchiveLink interface.

> **Note:** In order to successfully complete these tests, all the mandatory steps described in the Basic configuration section should have been completed.

1. In SAP, open the **ABAP** editor with transaction `SE38`.

2. Enter `RSCMST` as report name in the **Program** field and execute it. You can click **Execute** in the toolbar or press **F8** to execute it.

    ![sap_conf_014_sap_rscmst_1]({% link sap/images/sap_conf_014_sap_rscmst_1.png %})

3. In the **Repository** field, enter the name of the recently created SAP Content Repository and click **Execute** in the toolbar (or press **F8**).

    ![sap_conf_014_sap_rscmst_2]({% link sap/images/sap_conf_014_sap_rscmst_2.png %})

4. In the next screen, all sub-reports are listed that could be executed against the repository.

    ![sap_conf_014_sap_rscmst_3]({% link sap/images/sap_conf_014_sap_rscmst_3.png %})

5. The most important report is `RSCMSTH0`. This will test the basic communication like `create`, `info`, `search`, `update` or even `delete` commands via HTTP against the repository. Click the **Execute** icon for the report.

6. The report returns successfully if the SAP Content Repository is properly configured, and hence the SAP Connector is working.

    ![sap_conf_014_sap_rscmst_4]({% link sap/images/sap_conf_014_sap_rscmst_4.png %})

7. (Optional) If you’re interested in more technical details of the test, then click the **Details** icon near the green result.

    In this screen, each function call with its parameter is logged that was sent to Alfresco. Scroll down to the end of the detail page and find a summary of the functions which was tested including times.

    ![sap_conf_014_sap_rscmst_6]({% link sap/images/sap_conf_014_sap_rscmst_6.png %})

8. (Optional) You can execute some further test reports against the repository.

    This will test additional functionality of the HTTP interface. The additional available test reports are: `RSCMSTH1`, `RSCMSTH2` and `RSCMSTH3`.

    ![sap_conf_014_sap_rscmst_5]({% link sap/images/sap_conf_014_sap_rscmst_5.png %})

    > **Note:** For SAP BASIS component 740 up to (at least) 752 there is a known bug in the `RSCMSTH2` report. If the report returns with a lot of issues regarding document protection like `DOC_P[rc]`, refer to the following SAP {% include tooltip.html word="SAP_OSS" text="OSS" %} notes: 2371386, 2198970. Skip this report unless the notes are implemented.
---
title: Install SAP Connector
---

The SAP Connector capability for Content Services is delivered as a distribution zip file containing repository and Share {% include tooltip.html word="AMP" text="AMP" %} files, server files for the SAP Connector, and third-party license information.

In these topics you'll install and set up everything you need to run the SAP Connector. See [Prerequisites]({% link sap/latest/install/index.md %}#prerequisites) and [Supported platforms]({% link sap/latest/support/index.md %}) for information on what you require before you start the installation.

You can download the Alfresco Content Connector for SAP applications software from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

## Prerequisites

Below are the environment/software prerequisites for installing and using the SAP Connector.

### General requirements

* A valid license for SAP Connector.
* Both systems, Content Services and SAP, must be available in the same network, or connected through a VPN.
* Access to the [SAP Support Portal](https://support.sap.com/){:target="_blank"} to download the native libraries of the SAP Java Connector for your current system architecture.

### SAP requirements

* SAP {% include tooltip.html word="SAP_ECC" text="ECC" %} 6.0 (or up to latest) with at least SAP GUI 7.30
* SAP S/4HANA (build 1809 or up to latest) with at least SAP GUI 7.50
* SAP dialog user who is able to:
  * Create new SAP Content Repositories (transaction `OAC0`)
  * Create related ArchiveLink customization as described in the SAP Implementation Guide (available via transaction `SPRO`)
  * Test the ArchiveLink interface in any related module (for example transaction `FB03` for Finance)
* SAP system user who is able to:
  * Invoke BAPIs ({% include tooltip.html word="SAP_ABAP" text="ABAP" %} function modules via RFC connection)
* SAP Java Connector (JCo): JCo 3.1.x must be installed

### Alfresco requirements

* Content Services - see [Supported platforms]({% link sap/latest/support/index.md %}) for compatible versions.
* Alfresco server system architecture must be one of the following (for these architectures, SAP offers native Java Connector versions):
  * Linux 64bit x86
  * Windows 64bit x86
  * Windows 64bit Itanium
  * Linux 64bit Itanium
  * Linux IBM eServer z Series 64bit
  * Linux IBM PowerPC processors 64bit BE and LE
  * HP-UX 64bit PA-RISC
  * HP-UX 64bit Itanium
  * IBM AIX 64bit
  * IBM z/OS 64bit
  * IBM i 64bit
  * Sun OS 64bit SPARC
  * Sun OS 64bit x86
  * Mac OS X (for Intel) 64bit x86
* Firewall does not block HTTP traffic on port 80 / 8080 / 8082.
* Access to the Content Services server with administrator privileges to:
  * Apply the SAP Connector {% include tooltip.html word="AMP" text="AMP" %} files
  * Edit `alfresco-global.properties` file
  * Stop/start the application server
* Alfresco user with administrator permissions.

## Install overview

The SAP Connector is packaged as Alfresco Module Package (AMP) files. There are several stages to installing the SAP Connector: re-package the repository AMP, and then install the AMP files.

> **Note:** The SAP Connector uses the advantages of the SAP Java Connector for the communication between Content Services and the SAP system. According to the SAP terms & conditions, the redistribution of the native Java Connector libraries is no longer allowed. Hence, these libraries aren't included in the SAP Connector delivery package, and must be downloaded manually from the SAP Support Portal (requires an S-ID to log in). Once done, these libraries must be merged with the repository AMP file for the SAP Connector before starting the installation.

## Download files

Use the following steps to download the files required to install the SAP Connector.

1. Go to [Hyland Community](https://community.hyland.com/products/alfresco){:target="_blank"}, click **Product downloads**, and then download the SAP Connector distribution zip, which contains the following files:

    * `sap-content-connector-repo-6.0.x.amp` for Content Services.
    * `sap-content-connector-share-6.0.x.amp` for Alfresco Share.
    * `sap-content-connector-jco-packer-2.x.jar` - the **SAP JCo Packer tool** for merging the native SAP Java Connector libraries into the repository AMP file.
    * `sap-content-connector-encryptor-2.0.jar` to [encrypt plain-text passwords]({% link sap/latest/admin/reference.md %}#encryptpwd) for all SAP Connector related properties in the `alfresco-global.properties` file.
    * `alfresco-global.properties_append` contains all required property keys to be added in the `alfresco-global.properties` for an SAP connection.

2. Log in to the [SAP Support Portal](https://support.sap.com/){:target="_blank"} with your SAP Universal ID:

    1. [Download](https://support.sap.com/en/product/connectors/jco.html){:target="_blank"} the native libraries for the SAP Java Connector based on your current system architecture.

        > **Important:** Ensure you download the correct SAP Java Connector version, which is related to the current system architecture of your Content Services server.

        ![]({% link sap/images/sap_packer_001.png %})

    2. Once all the required files have been downloaded, the next step is to copy the required SAP Java Connector libraries into the SAP Connector repository AMP file before starting the installation.

## Re-package the repository AMP

Use the SAP JCo Packer tool provided in the distribution zip to merge the native SAP Java Connector libraries into the SAP Connector repository AMP.

Before continuing, make sure you've [downloaded all the required files](#download-files).

The re-packaging is done by using the SAP JCo Packer tool (`sap-content-connector-jco-packer-2.x.jar`), which helps to create a merged AMP file that's used as the foundation for the installation.

> **Important**: You must have at least **Java Version 8** installed in order to run the distributed SAP JCo Packer tool.

1. Prepare the files for merge:

    1. Create a new temporary directory and copy the following files into it:

        * `sap-content-connector-jco-packer-2.x.jar`
        * `sap-content-connector-repo-6.0.x.amp`
        * `sapjco31P_3-20009381.zip` (example file name for native Java Connector libraries, downloaded from the SAP Support Portal)

            > **Note:** The ZIP name could be different, depending on your chosen system architecture.

        ![]({% link sap/images/sap_packer_002.png %})

    2. Verify the `sap-content-connector-repo-6.0.x.amp` file size. It should be less than 1 MB.

2. Run the merge tool:

    Starting from your temporary folder, run the SAP JCo Packer tool:

    ```java
    java -jar .\sap-content-connector-jco-packer-2.x.jar
    ```

    ![]({% link sap/images/sap_packer_003.png %})

    You'll see a few log statements to show what's happening, and the tool should finally return: **Processing finished...**

3. Verify the merge:

    Verify that the merge is successful and double-check the file size of the `sap-content-connector-repo-6.0.x.amp` again. This should now be much larger than before.

    > **Note:** Depending on the chosen system architecture of the SAP Java Connector, the repository AMP file may be up to 7 MB. This indicates that the required native SAP libraries are now available inside the AMP file.

    ![]({% link sap/images/sap_packer_004.png %})

4. Copy and save the re-packaged AMP file:

    The re-packaged `sap-content-connector-repo-6.0.x.amp` file should now be saved for the future. This is the final file that's needed to [install](#installsapconnamps) the SAP Connector.

    > **Note:** You only need to merge the native SAP Java Connector libraries once for a specific release of the SAP Connector.

5. Cleanup:

    Once the re-packaged AMP file is saved and stored outside the current temporary folder, you can safely delete the temporary folder.

## Install the SAP Connector {#installsapconnamps}

These steps describe how to install the SAP Connector to an instance of Content Services.

> **Note**: Ensure that you've followed the instructions to [repackage the repository AMP](#re-package-the-repository-amp) before installing the SAP Connector AMPs.

1. You need the following files to apply the SAP Connector:

    * `sap-content-connector-repo-6.0.x.amp` for Content Services

        > **Note**: This must be the re-packed file which includes the native SAP Java Connector libraries. Don't use the original file from the delivery package without the required changes.

    * `sap-content-connector-share-6.0.x.amp` for Alfresco Share

2. Use the Module Management Tool (MMT) to install the {% include tooltip.html word="AMP" text="AMP" %} files into the Repository WAR (`alfresco.war`) and the Share WAR (`share.war`).

    For more information, see [Using the Module Management Tool (MMT)]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt) and [Installing an Alfresco Module Package]({% link content-services/latest/install/zip/amp.md %}).

3. Add the related properties to the `alfresco-global.properties` file.

    See [Configure repository](#configrepo) for more information.

    You'll need to adapt the related property values to your configuration.

4. Check that the [configuration]({% link sap/latest/config/index.md %}) is set up correctly for your environment.

5. Start Content Services.

## Configure repository {#configrepo}

These are the minimum required properties that must be appended to the `alfresco-global.properties` in order to establish the connection between Content Services (the Repository) and SAP.

> **Note:** There are additional properties that can be used to login to the SAP system via the SAP JavaConnector (such as using Logon Groups instead of the Gateway). See [Additional SAP JCo properties]({% link sap/latest/admin/reference.md %}#sapjavaconprops) which lists the additional properties that are supported.

1. Open `alfresco-global.properties` in your Content Services installation.

2. Add all properties from the table below to the end of the file and set their values according to your environment.

3. Save the file.

    > **Note:** There are up to 100 possible SAP System Configurations. The table below shows the basic configuration for the first configuration. Therefore, the property contains the number **1** in the key.

    The letters **al** in some keys are the abbreviation for **A**rchive**l**ink. These settings are mandatory for the basic communication between SAP and Content Services.

| Property Key | Description |
| ------------ | ----------- |
| integrations.sap.system.1.al.alfrescoUser | Username for the connection used to login to Content Services (should have administrator role). <br>Example value: `admin` |
| integrations.sap.system.1.al.alfrescoPassword | Password for the user. Either plain-text or use encrypted password. See [Encrypting passwords]({% link sap/latest/admin/reference.md %}#encryptpwd) for more. <br>Example value: `H3ll0W0rlD112!` or `ENC(XbfE4Z112==)` |
| integrations.sap.system.1.al.archiveIds | Comma separated list of all connected SAP Content Repositories of this configuration. <br>Example value: `M1` or `M2,M3,M4` |
| integrations.sap.system.1.al.documentRoot | The document root folder where all documents from the SAP Content Repositories of the current SAP System Configuration are stored. Must exist and must be entered in XPath syntax. <br>Example value: `/app:company_home/st:sites/cm:sap/cm:documentLibrary/cm:SAP_Documents` |
| integrations.sap.system.1.al.checkSignature | Enables the signature check for the HTTP Content Server interface. If disabled, all requests will be accepted no matter if they are signed or not. <br>Example value: `true` (default) or `false` |
| integrations.sap.system.1.al.checkExpiration | If enabled, a check occurs, whether the signed requests have been sent in the valid time window. <br>Example value: `true` (default) or `false` |
| integrations.sap.system.1.enabled | Whether data replication should be enabled for the current SAP System Configuration or not. If `true`, the following properties must be present with correct values. <br>Example value: `true` or `false` (default) |
| integrations.sap.system.1.name | An arbitrary value for the current SAP System Configuration. Should not contain special characters. Must be unique across all available SAP System Configurations. Recommendation: Should contain the name of the connected SAP system. <br>Example value: `NSP SAP System` or `NSP Repos M1, M2` |
| integrations.sap.system.1.host | The IP address of the SAP server or the SAP Router string. <br>Example value: `192.168.112.112` or `sap.mydomain.com` or `/H/80.112.112.112/H/192.168.112.112/S/3201` |
| integrations.sap.system.1.client | The SAP client used to log in to the SAP system. <br>Example value: `100` or `800` |
| integrations.sap.system.1.systemNumber | The SAP system number. <br>Example value: `00` or `01` |
| integrations.sap.system.1.user | SAP system user used for the login. <br>Example value: `ALFR3SC0` |
| integrations.sap.system.1.password | Password for the SAP user. Either plain-text or use encrypted password. See [Encrypting passwords]({% link sap/latest/admin/reference.md %}#encryptpwd) for more. <br>Example value: `H3ll0W0rlD112!` or `ENC(XbfE4Z112==)` |
| integrations.sap.system.1.language | The SAP system language used to login. <br>Example value: `EN` or `DE` |
| integrations.sap.system.5.webClient.enabled | Enables the document action "Open corresponding business object in SAP" in Alfresco Share to be opened in the SAP Web-GUI. If `true`, the `webclient.url` below must resolve. <br>Example value: `true` or `false` (default) |
| integrations.sap.system.5.webClient.url | The url to the SAP Web-GUI. <br>Example value: `https://sapserver:port/sap/bc/gui/sap/its/webgui` |
| integrations.sap.system.1.jobs. sapContentConnectorReplicate.enabled | Enables the metadata replication job. Adds the aspect **SAP Replicate Details** <br>Example value: `true` or `false` (default) |
| integrations.sap.system.1.jobs. sapContentConnectorReplicate.cronExpression | The CRON expression used for the job. <br>Example value: `0 0/1 * 1/1 * ? *` |
| integrations.sap.system.1.jobs. sapContentConnectorPlus.enabled | Enables the additional metadata replication job. Adds the aspect **SAP Replicate Plus Details** <br>Example value: `true` or `false` (default) |
| integrations.sap.system.1.jobs. sapContentConnectorPlus.cronExpression | The CRON expression used for the job. <br>Example value: `0 0/1 * 1/1 * ? *` |
| integrations.sap.system.1.jobs. sapContentConnectorBarcode.enabled | Enables the barcode job. <br>Example value: `true` or `false` (default) |
| integrations.sap.system.1.jobs. sapContentConnectorBarcode.cronExpression | The CRON expression used for the job. <br>Example value: `0 0/1 * 1/1 * ? *` |
| integrations.sap.system.1.jobs. sapContentConnectorDirReplicate.enabled | Enables the SAP DIR replication job. Adds the aspect **SAP Document Info Record (DIR) Details** <br>Example value: `true` or `false` (default) |
| integrations.sap.system.1.jobs. sapContentConnectorDirReplicate.cronExpression | The CRON expression used for the job. <br>Example value: `0 0/1 * 1/1 * ? *` |

## Install the license

The access and use of the SAP Connector is managed by a license. Any limitations are set when you purchased the license. To increase the limitations, contact Alfresco to obtain a new license. If you don't have a license yet, you can request a trial license.

> **Note:** Make sure you have a valid license file available before continuing. The name of the license file is `content-connector-for-sap.l4j`.

### Apply the license via the Alfresco Share user interface

1. Log in to Alfresco Share as an administrator.
2. Navigate to **Admin Tools** and click menu **SAP Integration**. This displays the SAP Connector Administration Console.

3. In the **License Information** section click **Choose Files**.
4. Select file `content-connector-for-sap.l4j`, and then click **Upload**.

    > **Note:** The new license is applied immediately- no restart of Content Services is required.

    ![sap_inst_001_license]({% link sap/images/sap_inst_001_license.png %})

An existing license file is backed up, renamed with the current time stamp, and remains on the file system (for example: `sapContentConnectorYYYY-mm-dd_hh:mm:ss.l4j`).

### Apply the license via the file system

1. Open the file `alfresco-global.properties` and search for the key `dir.license.external`. Note this value as you'll need it next.
2. Navigate to the folder provided in the property value.
3. Copy the license file `content-connector-for-sap.l4j` into that folder.
4. Restart the Content Services application server.

## Set up in a cluster

To set up the SAP Connector in clustered landscapes for high availability:

1. Install the `sap-content-connector-repo-5.x.amp` for Content Services on each node in the cluster.

    >  **Important:** Make sure you only use the merged SAP Connector repository AMP file, which includes the native SAP libraries, as described in [Installing overview]({% link sap/latest/install/index.md %}).

2. Install the `sap-content-connector-share-5.x.amp` for Alfresco Share on each node in the cluster.
3. Update the `alfresco-global.properties` with the SAP related properties.
4. On the SAP side, for each SAP Content Repository (transaction `OAC0`), the HTTP-Server must point to the load balancer instead of a dedicated application server instance. See the Content Services documentation for [high availability]({% link content-services/latest/admin/cluster.md %}#scenariohighthrucluster).
---
title: Supported platforms
---

The following are the supported platforms for Alfresco Content Connector for SAP Applications:

| Version | Notes |
| ------- | ----- |
| Content Services 23.x | |
---
title: Upgrade SAP Connector
---

Use this information to upgrade the SAP Connector from the previous version Connexas 4.2 to Alfresco Content Connector for SAP applications 5.x.

This guide only covers the upgrade from the previous version Connexas 4.2 to the rebranded SAP Connector version.

> **Important:** If you're running on a Connexas version below 4.2, contact the support. There is a need to follow a sequential upgrade from any previous version to Connexas 4.2 before you can proceed with the upgrade to the SAP Connector.

> **Important:** If you've implemented any custom module or any code relying on the current SAP integration *connexas*, make sure to adapt the code to the new SAP Connector structure before.

> **Important:** If you're planning to upgrade your current Content Services version as well to the next available major version (e.g. from 5.2 to 6.x), we recommend to upgrade the SAP Connector first, then upgrade Content Services in the second step.

## 1. Preparation & prerequisites

These are the necessary preparations and prerequisites to upgrade to the SAP Connector.

Before starting the upgrade, check whether your current installation is working without issues.

To verify this:

1. Login to Alfresco Share.
    * Alternatively, check with the Health Web Script.
2. Access the **connexas Administration Panel**: menu **Admin Tools > connexas**.

**CAUTION:**

If the Overall-Health-Status is not OK, fix the issues before proceeding with the upgrade.

If the installed core is not *connexas 4.2.x*, contact Support.

![sap_upgrade_connexasadminpanel]({% link sap/images/sap_upgrade_connexasadminpanel.png %})

### Prerequisites

Make sure you've fulfilled all prerequisites for the SAP Connector, as described in [Prerequisites]({% link sap/latest/install/index.md %}#prerequisites) and [Supported Platforms]({% link sap/latest/support/index.md %}).

For the technical upgrade, follow the steps below. Due to the product rebranding from *connexas* to the SAP Connector, the most important part of the upgrade needs to be done in the `alfresco-global.properties` and in the Content Services repository.

> **Important:** All customer specific enhancements (such as additional Jobs or Behaviors connecting to SAP via the current *framexas* framework of *connexas*) need to be modified separately to match the SAP Connector in order to continue working. Either change the modules before proceeding with the technical upgrade or skip it for now.

### Technical upgrade

Use the following steps to proceed with the technical upgrade of the software modules:

1. Stop the Content Services server.
2. Back up any custom folders and files that you have created.
3. Back up the current exploded web application folders for the repository and Alfresco Share.
4. Back up the database used for the repository.
5. Remove the former *connexas* modules from the `amps` and `amps_share` folders.
6. Download the new SAP Connector {% include tooltip.html word="AMP" text="AMP" %} files from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

    Follow the instructions in the [Install SAP Connector]({% link sap/latest/install/index.md %}#installsapconnamps) page. After applying the {% include tooltip.html word="AMP" text="AMP" %} files, verify the new SAP Connector version:

    ![sap_upgrade_modules]({% link sap/images/sap_upgrade_modules.png %})

7. Clean up all log files, temp and work folders on the Content Services server.
8. **Do not start** the Content Services server yet.

    > **Important:** You need to update the related property keys in `alfresco-global.properties`.

## 2. Modify Alfresco repository properties

Due to the product rebranding, the names of the property keys used for the SAP connection in the `alfresco-global.properties` have changed. These need to be updated before restarting the Content Services server.

### Rename property keys

Within the *connexas* version, the related property keys started with prefix `pernexas.*`.

For the SAP Connector, the prefix has changed to `integrations.*`. You need to search for all instances of `pernexas` and replace them with `integrations`, for each SAP System Configuration that's available in the `alfresco-global.properties`.

To complete the replacement, in an error-proof way, the recommendation is to search for `pernexas.sap.system` and replace it with `integrations.sap.system` as shown:

![sap_upgrade_globalprops_searchreplace]({% link sap/images/sap_upgrade_globalprops_searchreplace.png %})

### Rename jobs

After renaming the property keys with the new prefix, you also need to rename the jobs in a second step.

The table below lists the mapping of the former names in *connexas* and the new names used from now in the SAP Connector:

| Previous Name (in *connexas*) | New Name |
| ----------------------------- | -------- |
| replicateSap | sapContentConnectorReplicate |
| connexasPlus | sapContentConnectorPlus |
| barcode | sapContentConnectorBarcode |
| dirReplicate | sapContentConnectorDirReplicate |

To rename the jobs, search for the previous name and replace it with the new name. For each job there are two property keys affected - `enabled` and `conExpression`. Again, this must be done for each available each SAP System Configuration.

### Results

Once both steps above has been completed, the content of the `alfresco-global.properties` file for one SAP System Configuration should look similar to the example below.

> **Note:** Note the new prefix and the new names for the jobs.

![alfresco_upgrade_gp_after]({% link sap/images/alfresco_upgrade_gp_after.png %})

Next, restart Content Services and login to Alfresco Share.

## 3. Cross check & install new license {#crosscheckinstallnewlic}

Cross check whether the technical upgrade of the module has been successful and install the new license.

### Cross check via SAP Connector Administration Console

Once the previous steps have been completed and Content Services is up and running again, the first point to review is whether the modification of the property keys in the `alfresco-global.properties` was successful.

Open the SAP Connector Administration Console:

1. Login to Alfresco Share with administrator privileges.
2. Navigate to **Admin Tools > SAP Integration**.
    * Note that this menu item was previously shown as *connexas* before the upgrade.

The structure of the UI is similar to what was available in previous releases, with a few changes. See [SAP Connector Administration Console]({% link sap/latest/admin/index.md %}#sapadminconsole) for more details.

> **Note:** At this point, the Overall-Health-Status should appear red. This is nothing to worry about at this point.

### Check for missing properties in any SAP System Configuration

To check whether the changes to `alfresco-global.properties` was successful, review each available SAP System Configuration.

If there are any SAP System Configuration sections that are highlighted in red with an error message (as shown), it indicates that at least one required property is missing. Review the recently updated settings in `alfresco-global.properties` and make sure the renaming was done for all properties.

> **Important:** Ensure that all configuration are valid (i.e. with no error messages), otherwise you can't proceed to the next step.

![alfresco_adminpanel_sapconnector_missing_props]({% link sap/images/alfresco_adminpanel_sapconnector_missing_props.png %})

If there are no issues, you can now apply the license.

### Install new license

Install the license via the **License Information** section. See [Installing the license]({% link sap/latest/install/index.md %}#installing-the-license) for more.

> **Important:** The SAP Connector requires a new license. You can't use the license file of the previous *connexas* version. Contact Support, if you don't have a new license file available.

## 4. Modify SAP Content Repositories

On the SAP side, the SAP Content Repositories connected to Content Services must be recreated.

> **Important:** To execute this step successfully, the license for the SAP Connector must be installed and valid (see [3. Cross check & install new license](#crosscheckinstallnewlic)).

### Modify HTTP-Script

The product rebranding of *connexas* to the SAP Connector has also caused a new package structure for the Web Script which is called from the SAP side. Therefore, for **each** SAP Content Repository that's connected to Content Services the value for `HTTP Script` must be changed.

1. Login to SAP and open transaction `OAC0`.
2. For each affected SAP Content Repository connected to Content Services:
    1. Edit the SAP Content Repository.
    2. Change the value for `HTTP Script`:

        | Current Value | New Value |
        | ------------- | --------- |
        | alfresco/service/com/pernexas/archivelink | alfresco/service/com/alfresco/sap/http |

        ![sap_upgrade_oac0_httpscript]({% link sap/images/sap_upgrade_oac0_httpscript.png %})

    3. Save the SAP Content Repository.
    4. Go to the next SAP Content Repository.

### Recreate SAP Content Repositories and send the Certificates

Due to the product rebranding, the folder structure has also changed how the SAP Connector handles the SAP Content Repository files and certificates.

Previously, the SAP Content Repository files and certificates were stored in the `connexas` folder of the `Data Dictionary`. Now, the SAP Connector stores the files in the `SAP Content Connector` folder of the `Data Dictionary`.

To recreate the SAP Content Repositories and their certificates, follow the steps in [(1) Create SAP Content Repository]({% link sap/latest/config/index.md %}#basic-createsapcontentrepo) starting from **step 3**. Make sure you follow each required step including the functional test.

Once created, the folder structure in the **Data Dictionary** should look like the following screenshot.

**CAUTION:**

The **Data Dictionary** still contains the former *connexas* folder structure but also the new SAP Connector structure. Both should have the same SAP Repositories. Do not delete the *connexas* folder for now. It will be required to identify customer specific settings for Jobs and Behaviors (if there are any). Continue with the following steps - the deletion of the *connexas* folder is done in the Cleanup section.

![sap_upgrade_datadictionary]({% link sap/images/sap_upgrade_datadictionary.png %})

## 5. Modify Jobs, Behavior and Draft for SAP DIR

The configuration for Jobs and Behaviors must be mapped from existing SAP Content Repositories to newly created SAP Content Repositories.

Since all the files in the SAP Content Repository have been recreated in the previous step, each SAP Content Repository now has the default settings for Jobs, Behaviors and the Draft mode for SAP {% include tooltip.html word="SAP_DIR" text="DIR" %}. However, these settings can be customized. Therefore, the settings have to be mapped from the old SAP Content Repository files to the new ones, in order to achieve the same behavior and functionality as before.

The image below shows the affected properties with the default values of the former *connexas* installation versus the SAP Connector of a SAP Repository file.

![sap_upgrade_repofilesettings]({% link sap/images/sap_upgrade_repofilesettings.png %})

### Modify Job settings

To change the job configuration, the values for the **Enabled Jobs** property of the `SAP Connection Repository Details` aspect in each SAP Content Repository file must be compared with it's counterpart. This comparison should between folders **Data Dictionary > connexas > SAP Repositories** and **Data Dictionary > SAP Content Connector > SAP Repositories**.

> **Important:** Do not Copy & Paste the values as the Job names have changed in the SAP Connector. Use the mapping table below.

| Previous Name (in *connexas*)|New Name |
| -------------------------------|-------- |
| connexasReplicate | sapContentConnectorReplicate |
| connexasPlus | sapContentConnectorPlus |
| connexasBarcode | sapContentConnectorBarcode |
| connexasDirReplicate | sapContentConnectorDirReplicate |

**CAUTION:**

Any additional value besides the default requires special attention, because this indicates a customer specific job based on the former *connexas* installation. Make sure that the underlying module for the custom job works as expected with the new SAP Connector.

### Modify Behavior settings

To change the behavior configuration, the values for the **Enabled Behaviors** property of the `SAP Connection Repository Details` aspect in each SAP Content Repository file must be compared with it's counterpart. This comparison should between folders **Data Dictionary > connexas > SAP Repositories** and **Data Dictionary > SAP Content Connector > SAP Repositories**.

> **Important:** Do not copy & paste the values as the behavior names have changed in the SAP Connector. Use the mapping table below.

| Previous Name (in *connexas*) | New Name |
| ----------------------------- | -------- |
| connexasCreateArchivelink | sapContentConnectorCreateArchivelink |
| connexasWorkflow | sapContentConnectorWorkflow |
| connexasBarcode | sapContentConnectorBarcode |

**CAUTION:**

Any additional value besides the default requires special attention, because this indicates a customer specific behavior based on the former *connexas* installation. Make sure that the underlying code for the custom behavior works as expected with the new SAP Connector.

### Modify Draft for SAP DIR

To change the Draft mode for SAP {% include tooltip.html word="SAP_DIR" text="DIR" %}, the option for `Enable Draft for SAP DIR` in aspect `SAP Connection Repository Details` of each SAP Content Repository file must be compared with it's counterpart. This comparison should be between folders in folder **Data Dictionary > connexas > SAP Repositories** and **Data Dictionary > SAP Content Connector > SAP Repositories**.

## 6. Modify additional configuration

Change any additional configurations, such as for the *Open associated Business Object in SAP* feature.

### Modify Open associated Business Object in SAP feature

If there's an advanced configuration for [Opening associated Business Object in SAP]({% link sap/latest/config/advanced.md %}#openassocbusinessobjinsap), this must also be merged into the new SAP Connector structure in the **Data Dictionary**. In order to do so, follow these step-by-step instructions:

1. In Alfresco Share navigate to folder **Data Dictionary > connexas > Configuration**.

    > **Note:** If the **Configuration** folder does not exist, you don't have any additional configuration. You can skip these steps.

2. Identify all necessary files used to enhance the feature (see [Advanced configuration]({% link sap/latest/config/advanced.md %}#OpenBusinessObjectSAPAdvancedConfig) for more info).
3. Create a new **Configuration** folder under **Data Dictionary > SAP Content Connector** .
4. Copy (or move) all files from **Data Dictionary > connexas > Configuration** to **Data Dictionary > SAP Content Connector > Configuration**.

### Recreate "Perform Action" section for SAP related rules

This section may be of interest if there are rule scripts in place that move the documents from SAP to a final folder structure and/or rename the files according the SAP original file name.

If there are Alfresco rules in place that rely on rule scripts used to react on SAP replicated metadata (such as to move / rename documents), you'll need to redefine the rule action script. In the former *connexas* versions, a special **Patched Execute Script** action was required to execute the related JavaScript. The **Patched Execute Script** selection has been removed since the product rebranding, so the underlying Id has changed. With this change, the selected JavaScript to be executed has also been removed. This means, the rule doesn't execute the selected script anymore.

The **Patched Execute Script** is still available in the new SAP Connector version, but it has a new internal Id.

> **Note:** You'll need to edit each affected rule to re-apply the required action.

1. Identify the affected rules.

    They're usually found in the folder for all incoming SAP documents (which may be defined by the property `sap.system.1.al.documentRoot` in `alfresco-global.properties`), as well as in the folder where the documents finally end up after moving them to the desired structure.

2. Select the folder, click on action **Manage Rules**, then select the affected rule.

    The **Perform Action** section is empty, which means nothing will happen. Also, this is not a valid state:

    ![sap_upgrade_connexas_rule_1]({% link sap/images/sap_upgrade_connexas_rule_1.png %})

3. Click **Edit** to start editing the rule.
4. Scroll down to the **Perform Action** section, and select **Patched Execute Script** in the list. Finally, select the related JavaScript:

    ![sap_upgrade_connexas_rule_2]({% link sap/images/sap_upgrade_connexas_rule_2.png %})

5. **Save** the rule and test it.
6. Repeat these steps for all affected rules.

## 7. Perform extensive testing

To verify the successful upgrade from *connexas* to the SAP Connector, perform extensive testing of all scenarios used with the SAP Connector.

### Functional tests

Perform the functional (technical) testing of each recreated SAP Content Repository, as described in the [Basic configuration]({% link sap/latest/config/index.md %}#basic-configuration).

### Accessibility tests

Make sure that existing documents are still accessible from the attachment list of the SAP Business Objects.

### Scenario tests

Do intensive testing of all scenarios used with the SAP Connector (such as store documents, test barcode, start SAP Workflow, etc.). Make sure the behavior for new as well as existing documents is still as expected, for example for all Jobs and Behaviors.

## 8. Cleanup

This cleanup section removes all former *connexas* files after the successful upgrade to the SAP Connector.

### Delete folder in Data Dictionary

If all SAP Content Repositories are available under **Data Dictionary > SAP Content Connector > SAP Repositories** *and* all related settings of the previous chapters have been merged, you can safely delete the folder: **Data Dictionary > connexas**.

Make sure you delete it from the **Trash** of the administrator user as well.

### Delete old license file

Delete the former *connexas* license, as it's invalid. The license is stored on the Content Services server, in the folder specified by the `dir.license.external` property in the `alfresco-global.properties`. See [Installing the license]({% link sap/latest/install/index.md %}#installing-the-license) for more.

The name of the former license file is `connexas.l4j`. You can safely delete it.

You can also safely delete any backup files for the previous *connexas* version (such as `connexas2019-10-21_13-10-23.l4j`).
