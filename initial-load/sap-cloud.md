---
title: Alfresco Content Connector for SAP Cloud
---

The Alfresco Content Connector for SAP Cloud is an add-on module that offers seamless integration between Alfresco Content Services and SAP S/4HANA Cloud Essentials as well as on-premises through the SAP Document Management Service (via the CMIS protocol). It allows you to manage SAP related documents within an SAP environment while the documents are actually stored in Alfresco Content Services.

Here is a summary of the key capabilities:

* Support SAP S/4HANA Cloud Essentials
* Support SAP S/4HANA on-premises
* Manage documents using Content Management Interoperability Services (CMIS)
* Provides the necessary folder structure in Alfresco Content Services
* Fully flexible data exchange either via OData or RFC/SNC.

This release includes a [`GenericXchange` framework]({% link sap-cloud/latest/config/genericxchange.md %}) - a Low Code approach that offers an easy and fully flexible data exchange for any kind of metadata between the content in Alfresco and the related SAP Business Object. This is accomplished either by calling any existing OData service in SAP Cloud Essentials (or SAP S/4HANA on-premises) or invoking any remote enabled SAP function module via the SAP JavaConnector (using RFC/SNC connection).

> **Important:** The SAP Cloud Connector module can be applied to several versions of Content Services. See [Prerequisites]({% link sap-cloud/latest/install/index.md %}#prerequisites) and [Supported Platforms]({% link sap-cloud/latest/support/index.md %}) for more.

> **Note:**
>
> * This documentation only covers how to use Content Services with the SAP Cloud Connector.
>
> * The Alfresco Content Connector for SAP Cloud can be applied to Alfresco Content Services 7.0 - 7.3 only.
---
title: Administer SAP Cloud Connector
---

This page shows you how to check the health of the current installation and troubleshooting.

## Test connection use-cases on SAP S/4HANA Cloud Essentials

Follow the guidance to test the newly installed and configured module on SAP S/4HANA Cloud Essentials.

### Product Master Data

In this section we'll show you how to upload an attachment to a Product so it's shown in the **Business Object Types > Product** folder in Content Services.

1. Log in to SAP S/4HANA Cloud Essentials.
2. Open the **Product Master Data** app and select any Material (e.g. `FG111`):

   ![Product Master Data App]({% link sap-cloud/images/sap_cloud_manage_product_master_data.png %})

3. Navigate to section **Attachments - Document Management Service** on the Material.
4. Click **Edit** and upload a document with the **Upload** button.

    Choose **Office Documents** as Document Type for now:

   ![Upload Attachment]({% link sap-cloud/images/sap_cloud_add_attachment_1.png %})

5. Once the document is successfully uploaded, it is set to **Draft** mode.

    > **Note:** **DO NOT CLICK** the **Save** button for now. We just want to verify that **Draft** mode is supported.

   ![Uploaded Attachment]({% link sap-cloud/images/sap_cloud_add_attachment_2_draft.png %})

6. Log in to Content Services and navigate to the **Knowledge Provider > DMS_PCD1**  folder in the repository.

    You'll see the document is available in this folder but it hasn't yet been moved to the final/expected folder (i.e. under **Business Object Types > DocumentInfoRecord**). This is because it's still in **Draft** mode:

    ![Draft Mode Content Services]({% link sap-cloud/images/sap_cloud_add_attachment_2_draft_alfresco.png %})

7. Now, switch back to SAP S/4HANA Cloud Essentials and click **Save** for the recently stored Attachment.

    Note that the Product is not in **Edit** mode anymore, hence the attachment is no longer in **Draft** mode:

    ![Saved Attachment]({% link sap-cloud/images/sap_cloud_add_attachment_2_final.png %})

8. Again, switch back to Content Services and refresh the page.

    The document is removed from the previous location and is no longer in **Knowledge Provider > DMS_PCD1**. It's now been moved to the final folder under **Business Object Types > DocumentInfoRecord**:

    ![Saved Attachment]({% link sap-cloud/images/sap_cloud_add_attachment_2_final_alfresco.png %})

## Test connection use-cases on SAP S/4HANA on-premises

Follow the guidance to test the newly installed and configured module for the selected SAP Business Objects.

### Material Master

In this section we'll show you how to upload an attachment to a Material Master so it's shown in the **Business Object Types > Product** folder in Content Services.

1. Go to transaction `MM03` and choose any material:

   ![SAP transaction MM03]({% link sap-cloud/images/sap_test_mm03_1.png %})

2. In the {% include tooltip.html word="GOS" text="GOS" %} menu click **Create... > Create Attachment** and upload any desired file. This stores it in Content Services via CMIS:

   ![SAP transaction MM03]({% link sap-cloud/images/sap_test_mm03_2.png %})

3. Verify the availability by checking the attachment list. Open the document, so that it's retrieved from Content Services via CMIS:

   ![SAP transaction MM03]({% link sap-cloud/images/sap_test_mm03_3.png %})

#### Verify Material Master in Content Services

In the Content Services repository, navigate to the **Business Object Types > Product** folder to find the recently stored document. There will be some basic CMIS related aspects available:

![View in Content Services]({% link sap-cloud/images/sap_test_mm03_4_acs_view.png %})

### Equipment

To upload attachments to an Equipment:

1. Choose any existing Equipment via transaction `IE03`:

   ![SAP transaction IE03]({% link sap-cloud/images/sap_test_ie03_1.png %})

2. Upload a document via the {% include tooltip.html word="GOS" text="GOS" %} menu **Create... > Create Attachment**.
3. Verify the document has been successfully stored via CMIS in Content Services by opening it again in the Attachment List.

#### Verify Equipment in Content Services

In Content Services, navigate to the **Business Object Types > Equipment** folder to find the recently stored document. There will be some basic CMIS related aspects available:

![View Equipment in Content Services]({% link sap-cloud/images/sap_test_ie03_2_acs_view.png %})

## Supported Business Objects

The following table lists all SAP Business Objects that are currently supported.

| SAP Business Object Name |
| ---------------- |
| Bill Of Material |
| Billing Document |
| Business Partner |
| Condition Contract |
| Customer Return |
| Document Info Record |
| Equipment |
| Inbound Delivery |
| Journal Entry |
| Legal Document |
| Legal Transaction |
| Material Master |
| Outbound Delivery |
| Product |
| Production Order |
| Purchase Order |
| Purchase Requisition |
| Sales Contract |
| Sales Inquiry |
| Sales Order |
| Sales Quotation  |
| Sales Contract  |
| Supplier |
| Supplier Invoice |
| Supplier Quotation |

## Troubleshooting

Sorry you're having trouble with the Content Connector for SAP Cloud. Your problem may be related to any one of the following issues.

### SAP on-premises: RFC destination connection test fails (HTTP response code 400)

The connection test of the created RFC destination (`SM59`) returns with **`400`** response code:

![RFC Connection Test fails]({% link sap-cloud/images/sap_no_license_3_rfc_connection.png %})

This may be due to an incorrect **Path Prefix** specified for the target system. Make sure you use the exact value mentioned in [step 3 of creating the RFC Connection]({% link sap-cloud/latest/config/index.md %}#new-http-connection).

### SAP on-premises: RFC destination connection test fails (HTTP response code 402)

The connection test of the created RFC destination (`SM59`) returns with **`402`** response code:

![RFC Connection Test fails]({% link sap-cloud/images/sap_no_license_2_rfc_connection.png %})

This may be due to a missing (or expired) license file. Make sure you've [applied a valid license file]({% link sap-cloud/latest/install/index.md %}#install-license).

### SAP on-premises: Upload of attachments fails

The upload of an attachment fails in any transaction with the following error:

![SAP Application Error]({% link sap-cloud/images/sap_no_license_1.png %})

In most cases, this is due to an expired license file. Make sure you've [applied a valid license file]({% link sap-cloud/latest/install/index.md %}#install-license) for the SAP Cloud Connector.

If the license exists and is valid, this error may be due to incorrect configuration of the related repository in `OAC0`. In this case, check the repository configuration again.

### SAP Cloud: Upload of attachments fails

The upload of an attachment fails in any Fiori app with the following error:

![SAP Application Error]({% link sap-cloud/images/sap_cloud_troubleshooting_error_upload.png %})

If it's not related to a missing or expired license (see above), make sure you've entered the correct Content Services CMIS endpoint for the [Destination in the SAP Business Technology Platform]({% link sap-cloud/latest/config/cloud.md %}#create-destination).
---
title: Configure SAP S/4HANA Cloud Essentials
---

Use this information to configure the SAP Cloud Connector for SAP S/4HANA Cloud Essentials.

## Connect SAP Cloud with SAP Business Technology Platform (BTP) {#connect-btp}

There are a few steps required to connect an external repository to the SAP S/4HANA Cloud Essentials, such as:

* SAP BTP must be fundamentally configured (i.e. Subaccount, Cloud Foundry, Entitlements).
* SAP BTP must be enabled to work with the Document Management Service.
* The Content Services repository must be set up as a Destination in the SAP BTP (described in the step below).
* In SAP S/4HANA Cloud Essentials, the required Communication Scenarios (including Communication User) must be created and maintained.
* SAP S/4HANA Cloud Essentials must be enabled to connect to the SAP BTP.
  
> **Note:** The steps above are explained roughly because they're not part of the SAP Cloud Connector installation. They might differ slightly from customer to customer.

The final configuration steps required in SAP are to connect an arbitrary external content repository to SAP S/4HANA Cloud Essentials. You'll find a good starting point for the complete list of required steps in the *Document Management Service, Integration Option* link below. Follow the steps in the official SAP documentation:

* [Content Management Interoperability Services (CMIS)](https://help.sap.com/viewer/a630d57fc5004c6383e7a81efee7a8bb/LATEST/en-US/afa76f9f02204717958bbef34a81c386.html){:target="_blank"}
* [Manage Document Management Service, Integration Option](https://help.sap.com/viewer/f6e70dd4bffa4b65965b43feed4c9429/LATEST/en-US/64fa80a1d698429fa8c57a6160e9ba40.html){:target="_blank"}
* *Set-Up Instructions for Customer managed CMIS Repository*
  * This PDF document is provided directly to customers by SAP

### Create Destination on SAP BTP {#create-destination}

As a foundation, Content Services must be created as a Destination on the SAP Business Technology Platform. This is the only touch-point in the whole process where the connection to the Content Services must be specified.

1. Navigate to the Subaccount and click `Destinations`.
2. Select `New Destination` to start configuring a new destination.
3. Specify the required fields, including the mandatory ones marked with an asterisk (*).
    For the `URL:*` field:

    1. Enter the fully qualified URL to the CMIS Browser binding of Content Services.

        The default should look like this:

        ```text
        http://<content-services>/alfresco/api/-default-/public/cmis/versions/1.1/browser
        ```

    2. **Replace** the default Content Services endpoint `cmis` with the value **`sapcmis`**.

        The URL should look like this:

        ```text
        http://<content-services>/alfresco/api/-default-/public/sapcmis/versions/1.1/browser
        ```

Here's an example of the configuration screen:

![Create Destination]({% link sap-cloud/images/sap_btp_destination.png %})
---
title: Configure GenericXchange
---

Use this information to configure the GenericXchange module used for flexible data exchange either via a secure Remote Function Call (RFC/SNC) connection or by invoking an Open Data Protocol (OData) service on the related SAP System (either SAP Cloud Essentials or SAP S/4HANA on-premises).

The `GenericXchange` (`GX` for short) is a powerful module that allows you to exchange any metadata between SAP and Content Services by using a Low Code approach. This means the configuration is done in a JSON file that must be uploaded to Content Services. Once uploaded, the changes are reflected immediately, and no restart of the application server is required. The module can either invoke any OData service in SAP Cloud Essentials as well as in an SAP S/4HANA on-premises system, or it can be used to call any remote enabled function module in an SAP S/4HANA on-premises system using RFC via the SAP JavaConnector.

## Basic configuration {#gx_basic}

Once the module is successfully installed, you'll need to apply some basic settings in the `alfresco-global.properties`. These changes require a restart of the application server afterwards.

### Settings for OData {#gx_basic_odata}

If you're configuring data exchange via **OData** services, the properties in the table below must be added.

> **Note:** In general, any REST service can be invoked by the Content Connector for SAP Cloud. As the primarily connection is intended to connect to an SAP Cloud system, this documentation uses the word **OData** from now onwards.

| Property | Description |
| -------- | ----------- |
| genericXchange.rest.sap.system.1.job.enabled | Set if data exchange should be enabled for the configuration (`1`) or not. Example value: `true` or `false` (default). |
| genericXchange.rest.sap.system.1.job.cronExpression | The CRON expression used for the job. Example value: `0 0/1 * 1/1 * ? *`. |

It is possible to have up to 100 different Jobs, where each can invoke a separate OData service. This can be accomplished by duplicating the both properties and increasing the number within the key names.

### Settings for RFC/SNC {#gx_basic_rfc}

If you're configuring data exchange via RFC/SNC by calling an SAP function module with the SAP JavaConnector, the properties in the table must be added.

> **Note:** To invoke function modules with the SAP JavaConnector, the required native libraries from SAP need to be available. These must be [downloaded from the SAP Support Portal]({% link sap/latest/install/index.md %}#download-files) for the current system architecture.  

| Property | Description |
| -------- | ----------- |
| genericXchange.rfc.sap.system.1.job.enabled | Sets if data exchange for a [Job](#gx_job) should be enabled for the configuration (`1`) or not. In case of [Behaviour](#gx_behaviour) usage, this setting has no effect. Example value: `true` or `false` (default). |
| genericXchange.rfc.sap.system.1.job.cronExpression | The CRON expression used for the job. Example value: `0 0/1 * 1/1 * ? *`. |
| genericXchange.rfc.sap.system.1.name | An arbitrary value for the current configuration. Should not contain special characters. Must be unique across all available configurations. **Recommendation:** This should contain the name of the connected SAP system. Example value: `NSP SAP System` or `SAP Cloud System`. |
| genericXchange.rfc.sap.system.1.host | The IP address of the SAP server or the SAP Router string. Example value: `192.168.112.112`, `sap.mydomain.com`, or `/H/80.112.112.112/H/192.168.112.112/S/3201`. |
| genericXchange.rfc.sap.system.1.systemNumber | The SAP system number. Example value: `00` or `01`. |
| genericXchange.rfc.sap.system.1.client | The SAP client used to log in to the SAP system. Example value: `100` or `800`. |
| genericXchange.rfc.sap.system.1.user | SAP system user used for the login. Example value: `ALFR3SC0`. |
| genericXchange.rfc.sap.system.1.password | Password for the SAP user. Either plain-text or use encrypted password. See [Encrypting passwords]({% link sap/latest/admin/reference.md %}#encryptpwd) for more. Example value: `H3ll0W0rlD112!` or `ENC(XbfE4Z112==)`. |
| genericXchange.rfc.sap.system.1.language | The SAP system language used to login. Example value: `EN` or `DE`. |

> **Note:** For both, OData and RFC/SNC, it is possible to have up to 100 separate configurations, where each can invoke a separate configuration file in Content Services. This can be accomplished by duplicating all properties above and increasing the number within the key names.

### Prepare Content Services {#gx_basic_prepare_acs}

Once the related settings in the `alfresco-global.properties` are applied, check if the following folder exists in Content Services: **Data Dictionary > SAP Content Connector > genericXchange**.

If the folder (structure) doesn't exist then create it. Pay attention to the correct spelling (i.e. uppercase, lowercase, and spaces).

This is the folder to upload all JSON configuration files that are responsible for data exchange.

### Using Jobs or Behaviours {#gx_basic_job_behaviour}

You can schedule the data exchange on a periodic basis (using a `Job`) or based on a particular action on the document/folder (using a `Behaviour`) in Content Services. Each method requires a slightly different JSON notation.

> **Note:** The recommendation is to always use a `Job` whenever possible.

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| Job | *Preferred.* A queue is available. This means that in any error case the document(s) could be picked up again in the next Job execution based on the document state. | Execution does not happen immediately. |
| Behaviour | Execution happens immediately after the related action. | There is no queue. A separate paid SAP (system) user is required (otherwise this approach infringes the SAP Terms & Conditions). Ask your SAP representative for more details. |

## Behaviour approach {#gx_behaviour}

> **Note:** Using this approach requires a separate SAP (system) user.  

## Job approach {#gx_job}

> **Note:** You must set exclusion criterion in the mandatory `query` of the [`filter` property](#gx_prop_filter) of the JSON. To set a flag after the SAP function module has successfully processed the document, use the `success` property. The `success` property can set any property to an arbitrary value at the Alfresco document. Then, use this property value for the exclusion criterion in the `query`. If there is no exclusion criterion set, the document(s) are repeatedly picked up in the next Job execution.

## Mapping {#gx_mapping}

The mapping between the settings part in the `alfresco-global.properties` (see [Basic configuration](#gx_basic)) and the related JSON file uploaded to Content Services is done via filename of the JSON file, and is different for OData and RFC/SNC usage.

### Mapping for OData Services {#gx_mapping_odata}

A JSON file with name `restJob.`**1**`.json` is mapped to keys `genericXchange.rest.sap.system.`**1**`.job.enabled` and `genericXchange.rest.sap.system.`**1**`.job.cronExpression` in the `alfresco-global.properties`.

### Mapping for RFC/SNC invoked by Job {#gx_mapping_rfc_job}

A JSON file with name `rfcJob.`**1**`.json` is mapped to all keys starting with `genericXchange.rfc.sap.system.`**1**`.*` in the `alfresco-global.properties`. See [Settings for RFC/SNC](#gx_basic_rfc).

### Mapping for RFC/SNC invoked by Behaviour {#gx_mapping_rfc_behaviour}

A JSON file with name `rfcBehaviour.`**1**`.json` is mapped to all keys starting with `genericXchange.rfc.sap.system.`**1**`.*` in the `alfresco-global.properties`. See [Settings for RFC/SNC](#gx_basic_rfc).

In addition, the value of `genericXchange.rfc.sap.system.`**1**`.name` must match the value of key `sapName` in the related JSON file.

> **Note:** The value for `genericXchange.rfc.sap.system.`**1**`.name` (and therefore even the value for `sapName` in the JSON) should only consist of characters (a-z, A-Z) and/or numbers (0..9). No whitespace, special characters or any character beyond 128 in the ASCII table.

## Configuration {#gx_job_config}

Below are the configuration options for the Job and Behaviour JSON file(s), with a detailed property specification.

### Job JSON {#gx_job_json}

The following table lists all available settings for the `restJob.1.json` (= OData) respective `rfcJob.1.json`. The column **`Required For`** specifies for which type the setting must be present in the JSON configuration file (i.e. either OData, RFC, or All).

| Property | Type | Required For | Description |
| -------- | ---- | :----------: | ------------ |
| enabled | Boolean | All | Sets if the Job is enabled or not. Also remember that there's a  `genericXchange.rest.sap.system.1.job.enabled` property in `alfresco-global.properties`. If this is `false` then the related setting in the JSON has no effect, regardless of its value. Example value: `true` or `false`. |
| filter | Object | All | Defines the {% include tooltip.html word="AFTS" text="AFTS" %} query to find the desired documents to be processed in Content Services. It also holds a threshold value which is responsible for the termination criterion. The threshold defines the maximum number tries to process a document until it is excluded. See [Property `filter`](#gx_prop_filter) for more details. |
| mandatoryProperties | Array| All | A list of mandatory properties that must be present in the documents which are returned by the `filter` to be considered for processing. Example value: `cm:title`, `cm:description`. |
| createALFolder | Boolean | RFC | **Note:** This property is only required with [Alfresco Content Connector for SAP Applications]({% link sap/latest/index.md %}) and it's not required for Content Connector for SAP Cloud. <br/>If `true`, the parent folder for the current document is created, and the required SAP ArchiveLink related aspects is applied to it. This is to match the SAP ArchiveLink protocol specification. Example value: `true` or `false`. |
| mode | String | RFC | Sets how the module handles the specified function modules.{::nomarkdown}<ul><li>standard: Invokes one function module for the current document.</li><li>chain: Invokes multiple function modules in the given order for the current document.</li><li>batch: Invokes one function module with a bunch of Alfresco documents.</li><ul>{:/} |
| functionModule(s) | Object | RFC | Specifies SAP function module(s) including all required parameter. See [Property `functionModule`](#gx_rfc_prop_functionmodule) for more details. . |
| request | Object | OData | Defines the request to call the OData service with all necessary parameter. See [Property `request`](#gx_odata_prop_request) for more details. |
| response | Object | OData | Defines the mapping between each property of the OData call result and the property in Content Services. See [Property `response`](#gx_odata_prop_request) for more details. |
| error | Object | All | *Optional.* Handles the errors which might be returned by the `request` or `functionModule`. See [Property `error`](#gx_prop_error) for more details. |
| success | Object | All | *Optional*. Handles the success messages which might be returned by the `request` or `functionModule`. See [Property `success`](#gx_prop_success) for more details. |

### Behaviour JSON {#gx_behaviour_json}

> **Note:**
>
> * Make sure you have all the [required RFC related settings](#gx_basic_rfc) present in `alfresco-global.properties`.
> * Make sure you always use a separate paid SAP (system) user for the connection.

> **Important:** Each change in the JSON configuration file for a Behaviour requires a reload of the script on all Content Services nodes (or by restarting each Content Services node). To reload the Behaviour JSON file, a Webscript with name `genericXchange Reload` is provided. This Webscript is part of the `Content Connector for SAP - genericXchange` Webscript family which is accessible in the `Alfresco WebScripts Home`.

The following table lists all available settings for the `rfcBehaviour.1.json`, as it's not possible to use OData calls along with an Alfresco Behaviour. All the settings below must be present in the JSON configuration file.

| Property | Type | Description |
| -------- | ---- | ----------- |
| enabled | Boolean | Sets if the Behaviour is enabled or not. Example value: `true` or `false`. |
| sapName | String | Defines the mapping to the related SAP system configuration in the `alfresco-global.properties`. This must match the value of key `genericXchange.rfc.sap.system.`**1**`.name`. Example value: `GX_Behaviour_S4H`. |
| mode | String | Sets how the module handles the specified function modules.{::nomarkdown}<ul><li>standard: Invokes one function module for the current document.</li><li>chain: Invokes multiple function modules in the given order for the current document.</li></ul>{:/} |
| behaviour | String | Any behaviour from the [NodeServicePolicies interface](https://dev.alfresco.com/resource/docs/java/org/alfresco/repo/node/NodeServicePolicies.html){:target="_blank"} of the Alfresco Public API. Example value: `onUpdateProperties`, `onAddAspect`, or see the NodePolicy list. |
| notificationFrequency | String | Defines where in the transaction event the handler is invoked. See the [Behavior Policies Extension Point]({% link content-services/latest/develop/repo-ext-points/behavior-policies.md %}) documentation for more details. Example value: `TRANSACTION_COMMIT`, `EVERY_EVENT`, or `FIRST_EVENT`. |
| listeningOn | String | The aspect which must be available on the document to invoke the behaviour. Must be entered with a namespace prefix. Example value: `cm:summarizable`. |
| mandatoryProperties | Array | List of all mandatory properties on the document which must be set to invoke the behavior. This can't be empty or null. <br/>**Note:** The behaviour is invoked only if all specified properties have changed their values. It is not enough just to have the property available and filled, it also must be changed. Example value: `cm:summary`. |
| aspects | Array | List of all aspects which must be available on the document to invoke the behaviour. Example value: `cm:titled`. |
| noAspects | Array | List of all aspects which should not be present on the document to invoke the behaviour. If at least one aspect in this list is available, the behaviour does not fire. Example value: `cm:taggable`. |
| values | Object | A list of objects with property names and defined values which must be available to invoke the behaviour. Here it’s possible to trigger the behaviour only for specified values of a property. For a list of defined property/value pairs all must match to invoke the behaviour. <br/>**Note:** The value must exactly match the defined value (i.e. case sensitive, and no wildcards). A list of possible values can also be defined (see example for `noValues`). Based on the following example, the behaviour would only be invoked if `cm:title` exactly matches the word `Alfresco`. Example value: *[<br/>"cm:title": "Alfresco"<br/>]*. |
| noValues | Object | A list of objects with property names having defined values which are not allowed to invoke the behaviour. Here it’s possible to prevent the execution of the behaviour for properties with specified values. <br/>**Note:** The value must exactly match the defined value (i.e. case sensitive, and no wildcards). Looking at the example, the behaviour would only be invoked if `cm:summary` exactly matches either the word `Happy` **OR** the word `Day` **AND** `cm:title` matches the word `Alfresco`. Example value: *[<br/>"cm:title": "Alfresco", <br/>"cm:summary": ["Happy" , "Day"]<br/>]*. |
| detachBehaviour | Boolean | If `true` the RFC call (see parameter `functionModule`/`functionModules` below) is fired after the behaviour has been finished. Example value: `true` or `false`. |
| asyncRfc | Boolean | Sets whether to invoke the behaviour asynchronously or synchronously. Example value: `true` (asynchronous) or `false` (synchronous). |
| createALFolder | Boolean | If `true`, the parent folder for the current document is created and the required SAP ArchiveLink related aspects are applied to it. This is to match the SAP ArchiveLink protocol specification. Example value: `true` or `false`. |
| functionModule or functionModules | Object | Specify SAP function module(s) including all required parameters. See [Property `functionModule`](#gx_rfc_prop_functionmodule). |
| error | Object | *Optional.* Handles the errors which might be returned by the `request` or `functionModule`. See [Property `error`](#gx_prop_error). |
| success | Object | *Optional.* Handles the success messages which might be returned by the `request` or `functionModule`. See [Property `success`](#gx_prop_success). |

### Property specification {#gx_property_specification}

This section contains the detailed Object definitions for the example values in the [tables above](#gx_job_json}).

#### ***Property `success`*** {#gx_prop_success}

> **Note:** This is an optional property.

This property stores the defined text (key `state`) in any available Alfresco document property (key `alfProp`) once the SAP function module returns successfully. To handle errors, refer to the [property `error`](#gx_prop_error) .

| Property | Type | Description |
| -------- | ---- | ----------- |
| alfProp | String | Defines the Alfresco document property which holds the success state, for example `connexasAdministration:sapstatus`. |
| state | String | Defines the value for `alfProp`, for example `Linked to SAP`. |

Example

```json
"success": {
    "alfProp": "connexasAdministration:sapstatus",
    "state": "Linked to SAP"
}
```

#### ***Property `error`*** {#gx_prop_error}

> **Note:** This is an optional property.

If the OData call returns with an error, the returned value of this *error* property can be written to any available property on the current document in Content Services.

| Property | Type | Description |
| -------- | ---- | ----------- |
| alfProp | String | Specifies the Alfresco document property which holds the error state, for example `connexasAdministration:sapstatus`. |
| state | String | Defines the value for `alfProp`, for example `Error`. |
| message | Object | Defines the document property where the error message should be stored. This can also be a list of properties setting different values from the error response (see example below). |

Example

```json
"error": {
    "alfProp": "connexasAdministration:sapstatus",
    "state": "Error",
    "message": {
        "connexasAdministration:saperror": "error.message.value",
        "cm:description": "error.message.statusCode"
    }
}
```

#### ***Property `filter`*** {#gx_prop_filter}

This property queries all documents in the repository for processing based on the given `query`. It also specifies the maximum number of tries where the files are picked up for processing until it is excluded (e.g. in case of errors). For RFC/SNC calls (but not for OData), an additional `archiveIds` parameter is available.

> **Note:** Don't forget to specify exclusion criteria for the documents in the `query`.

| Property | Type | Description |
| -------- | ---- | ----------- |
| query | String | Define the AFTS query to find content for processing. Example value: `TYPE:\"cm:content\" AND NOT ASPECT:\"cm:titled\"`. |
| errorThreshold | Number | Maximum number of tries to process the document until it is excluded, for example `10`. |
| archiveIds | Array | *Optional.* Defines the archiveIds that must be available on the document in property `connexas:archiveId`, for example `D1`. |

Example

```json
  "filter": {
    "query": "TYPE:\"cm:content\" AND NOT ASPECT:\"cm:titled\"",
    "errorThreshold": 10,
    "archiveIds": [ "D1" ]
  },
```

#### ***Property `request`*** {#gx_odata_prop_request}

This property defines all required data to call an OData service.

| Property | Type | Description |
| -------- | ---- | ----------- |
| method | String | Defines the HTTP method for the OData service, for exa,ple `get`.|
| validateCertificate | Boolean | Deactivates or activates the `https` certificate check, for example `true` to activate the validation. |
| baseUrl | Object | The url to the OData endpoints of the SAP system. |
| endpoint | Object | Specifies the OData service endpoint. See [Property `endpoint`](#gx_odata_prop_request_endpoint). |
| headers | Object | Headers for `method`, such as PUT, POST, UPDATE or DELETE. |
| body | Object | The body content for `method`, such as PUT, POST, UPDATE or DELETE. Dependent on the OData service. |
| credentials | Object | Username and Password to login to the SAP Cloud. |

#### ***Property for `endpoint`*** {#gx_odata_prop_request_endpoint}

This property is a child element of [`request`](#gx_odata_prop_request).

> **Note:** Only OData services that return a JSON response are supported.

| Property | Type | Description |
| -------- | ---- | ----------- |
| url | String | The name of the OData service endpoint. To pass values from the current document in Content Services, use placeholders such as `{1}`, `{2}`, etc.. These placeholders are substituted with the values of the defined property specified in `substitutions`. Example value: `\<mysapcloud\>.com/sap/opu/odata/sap/`. |
| substitutions | Object | Substitutions for the placeholder used in the `url` above. Example value: `"alfProp": "sapbo:Product:Product"`. **Note:** Starts with index of `1` and replaced in the given order. |

Example for property `request` [Return Product Master Records](https://api.sap.com/api/API_PRODUCT_SRV/resource){:target="_blank"}

```json
"request": {
    "method": "get",
    "validateCertificate": true,
    "baseUrl": "https://mysapcloud-api.s4hana.ondemand.com/sap/opu/odata/sap/",
    "endpoint": {
        "url": "API_PRODUCT_SRV/A_Product('{1}')?$format=json",
        "substitutions": [
            {
                "alfProp": "sapbo:Product:Product"
        }
        ]
    },
    "headers": {
    },
    "body": {
    },
    "credentials": {
        "user": "USERNAME",
        "password": "PASSWORD"
    }
},
```

#### ***Property `response`*** {#gx_odata_prop_response}

> **Note:** Only OData services that return a JSON response are supported.

This property defines how the values in the response of the OData call are mapped to the data-model properties of Content Services. The content is a list of *key*-*value* pairs. The *key* defines the name of the data-model property in Content Services where the *value* should be stored. The *value* for the *key* in turn specifies the path to the desired element in the JSON map which holds the value. It can be accessed by using the format `$.d.KeyName`.

Example

```json
"response": {
    "cm:name": "$.d.Product",
    "cm:title": "$.d.Language",
    "cm:description": "$.d.ProductDescription"
},
```

#### ***Property `functionModule/functionModules`*** {#gx_rfc_prop_functionmodule}

> **Note:** Only required for RFC/SNC calls. Refer to [Job JSON overview table above](#gx_job_json).

This parameter holds the specification of the function modules which is invoked by the job.

* If the `mode` parameter is set to `chain`, this section requires a list of objects, and therefore the parameter name **must** be set to `functionModules` (plural). This means the *SAP Function Modules* in this list are invoked in the given order.
* If the `mode` parameter is set to `standard` or `custom`, the parameter name must be `functionModule` (singular) only. The table below breaks down the structure required to fill this parameter.

| Property | Type | Description |
| -------- | ---- | ----------- |
| name | String | The name of the RFC enabled function module in SAP, for example `ARCHIV_GET_CONNECTIONS`. |
| importParams | Object | List of import parameter that should be used. See [property `importParams`](#gx_rfc_prop_functionmodule_importparams). |
| exportParams | Object | List of export parameter from the function module that should be used to store its values in Content Services. See [property `exportParams`](#gx_rfc_prop_functionmodule_exportparams). |

#### ***Property `importParams`*** {#gx_rfc_prop_functionmodule_importparams}

This property is a child element of [`functionModule` / `functionModules`](#gx_rfc_prop_functionmodule) and is an array which holds a list of objects with all required import parameter of the *SAP Function Module* that should be used.

| Property | Type | Description |
| -------- | ---- | ----------- |
| paramType | String | The type of the import parameter, for example `struct`, `parameter`, or `table`. |
| name | String | The name of the import parameter of the SAP Function Module, for example `ARCHIV_ID`. |
| content | Object | Depending on the value of `paramType` above, this property defines which property in Content Services should be used for the current import parameter. See [property `content`](#gx_rfc_prop_functionmodule_importparams_content). |

#### ***Property `content`*** {#gx_rfc_prop_functionmodule_importparams_content}

The structure of property `content` depends on the value set in the property `paramType`.

#### ***Property `content` when `paramType = struct`*** {#gx_rfc_prop_functionmodule_importparams_content_struct}

This property is an array of parameters, where each parameter can be of type `struct`, `parameter` or `table`.

Example

```json
{
    "paramType": "struct",
    "name": "DATA_GENERAL_EXP",
    "content": [
        {
            "sapProp": "DESCRIPT",
            "alfProp": "cm:description",
            "type": "string"
        }
    ]
}
```

#### ***Property `content` when `paramType = parameter`*** {#gx_rfc_prop_functionmodule_importparams_content_parameter}

This property is an object containing the following keys which pass the desired values from the document in Content Services to the current SAP import parameter.

| Property | Type | Description |
| -------- | ---- | ----------- |
| alfProp | String | The name of the property in Content Services where its value is used for the import parameter in SAP. Example value: `connexasArchivelink:archiveid`. |
| type | String | The Content Services type for `alfProp`, for example `string`, `date`, `int`, `datetime`, `boolean`, or `const`. |

Example

```json
{
    "paramType": "parameter",
    "name": "QUERY_TABLE",
    "content": {
        "alfProp": "cm:created",
        "type": "date",
        "format": "ddmmYY"
    }
}
 ```

#### ***Property `content` when `paramType = table`*** {#gx_rfc_prop_functionmodule_importparams_content_table}

This property is a list of SAP table rows which contains a list of SAP table columns. Each cell has the following properties:

| Property | Type | Description |
| -------- | ---- | ----------- |
| sapProp | String | The name of the SAP table column, for example `TEXT`.
| alfProp | String | The name of the property in Content Services where its value is used for the import parameter in SAP. Example value: `connexasArchivelink:sapid`. |
| type | String |  The Content Services type for `alfProp`, for example `string`, `datetime`, `int`, `date`, `boolean`, or `const`. |
| format | String | *Optional.* If `type` is `date` this can be used to format the date (using Java date format strings). Example values: `ddmmYY`. |

Example

```json
{
    "paramType": "table",
    "name": "OPTIONS",
    "content": 
    [
        [
            {
                "sapProp": "TEXT",
                "alfProp": "ARC_DOC_ID = '${connexasArchivelink:sapid}'",
                "type": "string"
            }
        ]
    ]
}
```

#### ***Property `exportParams`*** {#gx_rfc_prop_functionmodule_exportparams}

This property is a child element of [`functionModule` / `functionModules`](#gx_rfc_prop_functionmodule) and is an array which holds a list of objects with all export parameters provided by the *SAP Function Module*.

| Property | Type | Description |
| -------- | ---- | ----------- |
| paramType | String | The type of the export parameter, for example `struct`, `parameter`, `dynamicExportTable`, or `exportTable`. |
| name | String | The name of the export parameter in the SAP Function Module, for example `DATA`. |
| content | Object | Depending on the value of `paramType` above, this property defines to which property in Content Services the return value should be stored.<br/>- See [`content` when `paramType=struct`](#gx_rfc_prop_functionmodule_exportparams_content_struct)<br/>- See [`content` when `paramType=parameter`](#gx_rfc_prop_functionmodule_exportparams_content_parameter)<br/>- See [`content` when `paramType=dynamicExportTable`](#gx_rfc_prop_functionmodule_exportparams_content_dynamicexporttable)<br/>- See [`content` when `paramType=exportTable`](#gx_rfc_prop_functionmodule_exportparams_content_exporttable) |

#### ***Property `content` when `paramType = struct`*** {#gx_rfc_prop_functionmodule_exportparams_content_struct}

This property holds an array of parameters. Each parameter can be of type `struct`, `parameter`, `dynamicExportTable` or `exportTable`.

Example

```json
{
    "paramType": "struct",
    "name": "DATA_GENERAL_EXP",
    "content": [
        {
            "sapProp": "DESCRIPT",
            "alfProp": "cm:description",
            "type": "string"
        }
    ]
}
```

#### ***Property `content` when `paramType = parameter`*** {#gx_rfc_prop_functionmodule_exportparams_content_parameter}

This property is an object containing the following keys which are responsible for storing the return value from the SAP export parameter to the Alfresco document.

| Property | Type | Description |
| -------- | ---- | ----------- |
| alfProp | String | The name of the property in Alfresco where its value is used for the export parameter in SAP. Example value: `connexasArchivelink:archiveid`. |
| type | String |  The Alfresco content model type for `alfProp`, for example `string`, `date`, `int`, `datetime`, `boolean` or `const`. |
| format | String | Optional. If `type` is `date` or `datetime` this can be used to convert a string (returned from SAP) to a date (using Java date format strings) that is stored in the Alfresco content model. Example value: `ddmmYY`. |

Example

```json
{
    "paramType": "parameter",
    "name": "QUERY_TABLE",
    "content": {
        "alfProp": "connexasArchivelink:creationdate",
        "type": "datetime",
        "format": "yyyy-MM-dd HH:mm:ss"
    }
}
```

#### ***Property `content` when `paramType = dynamicExportTable`*** {#gx_rfc_prop_functionmodule_exportparams_content_dynamicexporttable}

| Property | Type | Description |
| -------- | ---- | ----------- |
| alfProp | String | The name of the property in Alfresco where its value is used for the export parameter in SAP, for example `cm:name`. |
| type | String | The Alfresco content model type for `alfProp`, for example `string`, `date`, `int`, `datetime`, or `boolean`. |
| sapPropStart | int | Begin index to read the value from the SAP cell, for example `123`. |
| sapPropEnd | int | End index for the value, for example `145`. |
| format | String | *Optional.* If `type` is `date` this can be used to format the date (using Java date format strings). Example value: `ddmmYY`. |

Example

```json
{
    "paramType": "dynamicExportTable",
    "name": "DATA",
    "content": [ {
            "alfProp": "cm:name",
            "type": "string"
            "sapPropStart": 123,
            "sapPropEnd": 145,
        }
    ]
}
```

#### ***Property `content` when `paramType = exportTable`*** {#gx_rfc_prop_functionmodule_exportparams_content_exporttable}

This property is an object containing the following keys which are responsible for storing the defined columns of the first row returned from the SAP export table.

| Property | Type | Description |
| -------- | ---- | ----------- |
| sapProp | String | The name of the SAP table column, for example `OBJECT_ID`. |
| alfProp | String | The name of the property in Alfresco where its value is used for the export parameter in SAP. Example value: `connexasReplicate:sapobjectid`. |
| type | String | The Alfresco content model type for `alfProp`. Example value: `string`, `date`, `int`, `datetime`, `boolean`, or  `const`. |
| format | String | *Optional.* If `type` is `date` or `datetime` this can be used to convert a string (returned from SAP) to a date (using Java date format strings) that is stored in the Alfresco content model. Example value: `yyyy-MM-dd`. |

Example

```json
{
    "paramType": "exportTable",
    "name": "CONNECTIONS",
    "content": [
        {
            "sapProp": "OBJECT_ID",
            "alfProp": "connexasReplicate:sapobjectid",
            "type": "string"
        },
        {
            "sapProp": "AR_OBJECT",
            "alfProp": "connexasReplicate:saparchiveobject",
            "type": "string"
        },
        {
            "sapProp": "AR_DATE",
            "alfProp": "connexasReplicate:archiveDate",
            "type": "date",
            "format": "yyyy-MM-dd"
        }
    ]
}
```
---
title: Configure SAP S/4HANA on-premises
---

Use this information to configure the SAP Cloud Connector for on-premises installations of SAP S4/HANA.

## Customize SAP

This section guides you through the configuration steps in the related SAP system to allow the storage of attachments via the CMIS protocol in Content Services.

### Create new HTTP connection to Content Services {#new-http-connection}

1. Create a new **HTTP Connection to External Server** within the RFC Connection transaction `SM59`.

    ![SM 59]({% link sap-cloud/images/sap_sm59_create_connection.png %})

2. Enter a name and choose **HTTP Connection to External Server** as the Connection type.

    We suggest you use a descriptive destination name, avoiding whitespace and other special characters.

    ![SM 59]({% link sap-cloud/images/sap_sm59_create_connection_create.png %})

3. As a minimum, add the required values for the fields in the **Target System Settings** area:

    * The host must match the Alfresco server (use port `8080`)
    * Enter the following as the **Path Prefix** (this must be an exact match):

        ```text
        /alfresco/api/-default-/public/sapcmis/versions/1.1/browser
        ```

    ![SM 59]({% link sap-cloud/images/sap_sm59_create_connection_create_target_system.png %})

4. Save the changes and switch to the **Logon &amp; Security** tab.

5. Select **Basic Authentication** from the **Logon Procedure** section and provide the username and password to log in to Content Services.

    If Single Sign-On is enabled, configure the  **Logon with Ticket** section.

    ![SM 59]({% link sap-cloud/images/sap_sm59_create_connection_create_target_system_logon.png %})

6. Save the changes again.

7. Click **Connection Test** in the menu to verify the connection.

    * Content Services should respond with an HTTP `200` response.
    * If not, check that the module is installed correctly on Content Services, and ensure the username and password from the previous step match.

    ![Connection Test]({% link sap-cloud/images/sap_sm59_create_connection_create_target_system_test.png %})

### Create new Content Repository for CMIS {#new-repo-cmis}

Based on the HTTP Connection created in the previous section, a new CMIS Content Repository must now be created.

1. Go to transaction `OAC0`.
2. Create a new Content Repository with the following values:

    * **Content Rep.:** `-DEFAULT-`

    > **Important: This must be an exact match - written in UPPERCASE with leading and trailing slash.** *The name can't be changed as it's the default setting in Content Services for the CMIS repository* SAP may not allow you to create it with `-DEFAULT-` and might show an error message similar to `The selected key is reserved for SAP`. If this error shows up, hit the Enter key twice.

    * **Document area:** *Leave empty*
    * **Storage type:** `CMIS Content Server`
    * **RFC destination:** `ALF_CMIS_ACS_7` *Select the previously created HTTP Connection.*

![OAC0 Create Repo]({% link sap-cloud/images/sap_oac0_create_cmis_repo.png %})

#### (Optional) Create Logical Repositories

In addition to the `-DEFAULT-` repository, you can create **Logical Repositories** for **ArchiveLink** and reference the `-DEFAULT-` repository to provide more flexibility.

To do this, create another Content Repository and use the following values:

* **Document Area:** `ArchiveLink`
* **Storage type:** `Logical Repository`
* **Symbolic Rep.:** `-DEFAULT-`

![OAC0 Create Logical Repo]({% link sap-cloud/images/sap_oac0_create_logical_repo.png %})

## Run CMIS setup report

You'll need to run the CMIS report to create the necessary folder structure in Content Services.

1. In transaction `SE38` select the program **CMIS_REPOSITORY_SETUP** and execute it with the following values:

    * **RFC_DEST:** `ALF_CMIS_ACS_7` (the recently created HTTP Connection)
    * **CMIS_REP:** `-DEFAULT-`

    ![SE38]({% link sap-cloud/images/sap_se38_cmis_repo_setup_report.png %})

    > **Note:** The report runtime can take up to 5 minutes.

2. The result should look like the following screenshot.

    The errors can be skipped because the stated types have already been created by applying the `sap-content-connector-cmis-repo-x.x.x.amp` in the very first step:

    ![SE38]({% link sap-cloud/images/sap_se38_cmis_repo_setup_report_result.png %})

    > **Note:** The reason behind the errors is that Content Services doesn't support the type creation via CMIS, but the module takes care of this creation.

### Verify folder creation in Content Services

Log in to Content Services with administrator privileges and navigate to the **Repository** folder. Here you'll find two new folders:
  
 1. Knowledge Provider
 2. Business Object Types

These folders have a structure that's created along with the report.

![View in Content Services]({% link sap-cloud/images/sap_se38_cmis_repo_setup_report_result_acs.png %})

This is also the proof that the errors in the report above can be skipped, because both folders were mentioned in the error log even though they exist.

## Maintain storage category for CMIS

To store documents (attachments) from SAP via CMIS to Content Services, the **SOFFDB** and **SOFFHTTP** categories should point to the `-DEFAULT-` content repository. Change it in transaction `OACT`.

![Change SOFFDB and SOFFHTTP categories]({% link sap-cloud/images/sap_oact_soffdb_soffhttp_category_to_default.png %})

## Map Categories for Physical Documents Class

Go to transaction `SKPR08` and map the new category under `SOFFPHIO`.

![Map SOFFDB under new category]({% link sap-cloud/images/sap_skpr08_map_category_to_soffdb.png %})
---
title: Install SAP Cloud Connector
---

The Content Connector for SAP Cloud capability is delivered in a repository Alfresco Module Package (AMP) file.

In these topics you'll install and set up everything you need to run the SAP Cloud Connector. See [Prerequisites](#prerequisites) and [Supported Platforms]({% link sap-cloud/latest/support/index.md %}) for information on what you require before you start the installation.

## Prerequisites

There are a number of software requirements for installing and using the SAP Cloud Connector.

See [Supported platforms]({% link sap-cloud/latest/support/index.md %}) for more information.

### General requirements

You also need to [install a valid license](#install-license) for the SAP Cloud Connector.

## Install SAP Cloud Connector {#install-connector}

The SAP Cloud Connector is packaged as an {% include tooltip.html word="AMP" text="AMP" %} file. These steps describe how to install the SAP Cloud Connector to an instance of Content Services.

1. Go to [Hyland Community](https://community.hyland.com/){:target="_blank"}, and then download the Alfresco Content Connector for SAP Cloud delivery package. It is provided as a ZIP file and contains at least the following files:

    * Module `sap-content-connector-cmis-repo-2.0.x.amp` for Content Services:
        * This contains the business logic for the SAP Cloud Connector.
    * Module `sap-content-connector-genericXchange-2.x.x.amp` for Content Services:
        * This contains the business logic for additional data exchange.
        * See [Configure GenericXchange]({% link sap-cloud/latest/config/genericxchange.md %}) for more details.
    * `alfresco-global.properties_append` template:
        * This is only required if using GenericXchange, and contains required keys/properties to add to the current `alfresco-global.properties` file.
    * `sap-content-connector-jco-packer-x.x`:
        * This is only required if using GenericXchange with RFC (SAP JavaConnector).
        * See [Re-package the repository AMP]({% link sap/latest/install/index.md %}#re-package-the-repository-amp) for more details.

2. To install the two {% include tooltip.html word="AMP" text="AMP" %} files from the delivery package:

    * Use the Module Management Tool (MMT) to install both repository AMP files into the repository WAR (`alfresco.war`). For more information, see:

        * [Using the Module Management Tool (MMT)]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt)
        * [Installing an Alfresco Module Package]({% link content-services/latest/install/zip/amp.md %})

3. Start Content Services.

## Install the license {#install-license}

The access and use of the SAP Cloud Connector is managed by a license. If you don't have a license yet, you can request a trial license from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

> **Note:** Make sure you have a valid license file before continuing. The name of the license file is `content-connector-for-sap-cloud.l4j`.

### Apply the license via the file system

1. Open the `alfresco-global.properties` file and search for the key **`dir.license.external`**. Note down this value as you'll need it in the following steps.
2. Navigate to the folder provided in the property value.
3. Copy the license file `content-connector-for-sap-cloud.l4j` into that folder.
4. Restart the Content Services application server.
---
title: Supported platforms
---

The following are the supported platforms for Alfresco Content Connector for SAP Cloud:

| Version | Notes |
| ------- | ----- |
| **Alfresco** | |
| Content Services 23.x | |
| | |
| **SAP S/4HANA Cloud Essentials** | |
| CE2105 (and up) | |
| **SAP S/4HANA on-premises** | |
| S4/HANA 1909 (and up) | Version must support CMIS |
