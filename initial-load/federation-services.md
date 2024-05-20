---
title: Alfresco Federation Services
---

Alfresco Federation Services is an add-on module that provides a powerful and easy way to search and manage content federated from leading business systems and content management applications. Manage in place functionality allows you to access, control, and govern content residing in more than sixty different business and content repository types. This provides a single view of information across different content systems, by synchronizing content into Alfresco Content Services.

By connecting information from different systems, you can provide a single view of information stored across multiple repositories.

Here is a summary of the key capabilities:

* Federated search - content can be searched for across multiple content repositories and made accessible inside Alfresco Content Services. This means it doesn't need to be migrated from different content systems.
* Manage content in place - all content can be controlled, no matter where it's stored.
* Intelligent content migration - enables content migration to be completed in the background, with minimal disruption to your end users.

Alfresco Federation Services ensures that customers are able to:

* Federate and manage content or records in other repositories
* Apply Alfresco Governance Services to content that's stored in other content systems (using the manage in place functionality)
* Support enterprise-wide eDiscovery cases in order to allow legal holds across the enterprise

The following diagram shows a simple representation of how Alfresco Content Services and Alfresco Federation Services interact with different content systems.

![Simple architecture diagram for Federation Services]({% link federation-services/images/simple-architecture-3.0.png %}){:height="300px" width="615px"}

Alfresco Federation Services can integrate any two endpoints in systems such as:

* CMS (Alfresco Content Services, Documentum, SharePoint, etc.)
* Network file systems

See the [Alfresco Federation Services summary and demo](https://www.alfresco.com/information-governance/content-federation-and-manage-place){:target="_blank"} to learn more.

## Terminology

Here's some useful terminology from the Federation Services documentation.

|Term|Description|
|----|-----------|
|Auth Connector|This allows you to authenticate against a repository.|
|Repository Connector|This is a connector to a repository for getting content, metadata, versions, and renditions.|
|Output Connector|This is a connector to the output system you want to migrate or index to. to.|
|Content Service Connector|This connector allows you to attach a system to the Objective 3Sixty Content Services API for Federation.|
|Discovery Connector|This connector is used to get schema information from a system.|
|Job|A job is a basic construct used to specify the repository and output used in a migration or index. This is how you connect two systems together with Federation Services.|
|Mapping|Provides metadata mapping between types/aspects from a source system to an output system. These can be used in a job and in a content services connector.|
|Tasks|Provides a processing pipeline that allows you to process documents, metadata, versions, and renditions as part of a job.|
|TCS|Transparent Content Services (for managing content in-place)|
|TSearch|This component provides federated search capabilities|
---
title: Administer Federation Services
---

The Admin app allows you to setup and manage your Federation Services environment.

The Admin app is a console for managing the administration of your Federation Services environment. It has separate menus that identify a particular activity or feature, and sub-menus that allow you to configure everything you need to perform migrations or federation.

The Dashboard displays a snapshot of the admin information, including sections for Connectors, Discovery, Migration, Federation, Reports, and Admin. In each of these sections, you can view a list of recently accessed settings.

![Screenshot of the Federation Services menu]({% link federation-services/images/menu.png %}){:height="220px" width="140px"}

|Menu option|Description|
|-----------|-----------|
|Connectors|Allows you to configure Authentication, Repository, and Output connectors.|
|Discovery|Allows you to perform schema discovery and create aggregate reports.|
|Migration|Allows you to create and manage jobs.|
|Groups|Allows you to manage Job, Mapping, and Task groups.|
|Federation|Allows you to manage your federation information. Specifically, this is where you manage Federated Search and related views, as well as configure Content Service and Search connectors.|
|Reports|Provides basic audit reports.|
|Admin|Allows you to manage users, logging, import/export, license keys, etc..|

## Managing Licenses

In the Admin app, the **Licenses** page allows you to manage your license keys.

When you first deploy the Federation Services Admin app, you'll need to apply your license key.

You can add a new license key, or reactivate previously entered keys. The details of each key are listed, including the associated **MAC Address**, **Documents Allowed**, **Documents Used**, **End Date**, and which key is in use.

1. Access the Federation Services Admin app.

2. In the left hand menu, click **Admin > License**.

3. Paste your license key into the **License Key** field, and click **Add License Key**.

    The license information displayed in the table.

    > **Note:** You can only have one active license at a time.

If you need to reactivate a license key or add a new license key, simply repeat the steps above. If the key already exists, then it will be activated and the old key will be set to inactive.
---
title: Configure Federation Services
---

The configuration for Federation Services is managed in the Admin app.

<!--FIXME: update all Simflofy text & links to 3Sixty-->

Below is a high-level summary of the configuration process using the menu options in the Admin app. You'll need to follow the links provided in the Simflofy documentation to set up your environment. You can also see the Simflofy [Connectors](https://simflofy.helpdocsonline.com/connectors){:target="_blank"} documentation for a list of supported connectors and configuration details.

Start by accessing the Admin app and then expand the **Connectors** menu option:

1. Open your browser and navigate to: `http://<servername>:<port>/3sixty-admin`, where `<server>` is the IP address or DNS address to your Federation Services server and `<port>` is the port to your Federation Services server.

    For example, if installing on your localhost, your URL may be: `http://localhost:6060/3sixty-admin`

2. Enter your user name and password, and then click **Login**.

    The default administrator user name/password is `admin/admin`.

3. Expand the **Connectors** menu

![Screenshot of the connectors menu]({% link federation-services/images/connectors.png %}){:height="220px" width="140px"}

Next, complete the configuration in each of the following areas.

1. Create an Authentication Connection - one entry for each of the systems that you'd like to federate.

    For example, see the Simflofy [Google Drive OAuth Connector](https://simflofy.helpdocsonline.com/google-drive-oauth-connector){:target="_blank"} documentation for creating a Google Drive connector.

2. Create a **Repository Connection** - one entry for each authentication connection. This configuration uses the authentication connection that you created in the previous step.

    > **Note:** If the option is available, validate your connection by clicking **Test**.

    See the Simflofy [Repository connector](https://simflofy.helpdocsonline.com/repository-connector){:target="_blank"} documentation for more information.

3. Create a **Content Services Connection** so that you can use the manage in place functionality.

    See the Simflofy [Content services](https://simflofy.helpdocsonline.com/content-services){:target="_blank"} documentation for more information.

4. Create an **Output Connection** that sets the target folder for the repository / output.

    See the Simflofy [Output connector](https://simflofy.helpdocsonline.com/output-connector){:target=_blank"} documentation for more information.

5. Create a **Discovery connector** that configures the retrieval of content metadata from your source systems. You can run a report to view the discovery results.

    See the Simflofy [Discovery connector](https://simflofy.helpdocsonline.com/discovery-connector){:target="_blank"} documentation for more information.

6. Create a Job for federated search - one entry to synchronize a single source system to a single target system.

    > **Note:** If you're planning to use manage in place federation, expand **Advanced Options** settings, and uncheck the **Include Binary** checkbox.

    See the Simflofy [Jobs](https://simflofy.helpdocsonline.com/jobs){:target="_blank"} documentation for more information.

7. Run the Job after completing the above configuration. Click **Migration** > **Run and Monitor Jobs** to start, stop, and view the status of your jobs.

See the Simflofy documentation on [Setting Up Federated Search](http://simflofy.helpdocsonline.com/setting-up-federated-search-tutorial){:taget="_blank"} for more information.
---
title: Install Federation Services
---

The Federation Services capability for Alfresco Content Services is delivered in a number of installation files.

## Prerequisites

Check the [supported platforms]({% link federation-services/latest/support/index.md %}) for information on what you require before you start the installation.

> **Note**: A compatible version of Alfresco Governance Services (if you plan to use the Manage in Place capabilities) is required, for example: if using Alfresco Content Services 23.1, make sure that you install Alfresco Governance Services 23.1.

You can download the Federation Services software from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

### Federation Services requirements

* Federation Services Admin server (i.e. 3Sixty Admin)
<!--* TSearch component (provides federated search capabilities)-->
* MongoDB server
* Tomcat server

    > **Note:** We recommend using a separate instance, where possible, instead of using the same one used by Alfresco Content Services.

See the [3Sixty documentation](https://helpdocs.objective.com/3sixty_user/Content/get-started/architecture.htm){:target="_blank"}, for specific hardware and software requirements.

> **Note:** This release of Alfresco Federation Services doesn't support deployment in Docker containers.

## Install steps

These steps describe how to install Federation Services to an instance of Alfresco Content Services.

1. Go to [Hyland Community](https://community.hyland.com/){:target="_blank"} and download the files provided for the Federation Services release.

    This should include the following:

    * `AFS-federation.war`
    * `AFS-admin.war`

    <!--FIXME: Describe each artefact and purpose-->
    <!--* `t-search-3.0.0.6.war`: Federated search application-->
    <!--* `transparent-content-services-platform-3.0.0.6.jar`: Transparent Content Services (TCS) JAR module for Manage-In-Place (to be applied to the Alfresco Content Services repository)-->
    <!--* `transparent-content-services-share-3.0.0.6.jar`: Transparent Content Services (TCS) JAR module for Manage-In-Place (to be applied to Alfresco Share)-->

2. Follow the steps in the 3Sixty documentation, [Install 3Sixty](https://helpdocs.objective.com/3sixty_user/Content/get-started/installation.htm){:target="_blank"}.

3. After completing all the installation steps, you'll need to access the Admin app through your preferred browser to [configure]({% link federation-services/latest/config/index.md %}) your installation.
---
title: Supported platforms
---

The following are the supported platforms for Alfresco Federation Services 3.1:

| Version | Notes |
| ------- | ----- |
| Content Services 23.1 | |
| | |
| **Java** | |
| Java JRE 17 or later | |
| | |
| **Browsers** | |
| Chrome (latest) | |
| Firefox (latest) | |
| Safari (latest) | |
