---
title: Alfresco Content Connector for AWS Glacier
---

The Alfresco Content Connector for AWS Glacier (Glacier Connector) works in conjunction with the Alfresco Content Connector for AWS S3 (S3 Connector) and enables access to Amazon S3 Glacier.

Amazon S3 Glacier is a storage service optimized for infrequently used data, and it suits the long term storage of archive and backup data. Amazon S3 Glacier gives you a number of retrieval options, offering different levels of retrieval speed. See [Amazon S3 Glacier retrieval tiers](#retrieval-tiers) for more information on retrieval types.

Amazon S3 Glacier is supported with Alfresco Content Services and Alfresco Governance Services. See [Supported platforms]({% link aws-glacier/latest/support/index.md %}) and [Glacier Connector FAQs]({% link aws-glacier/latest/using/index.md %}) for more information.

> **Note:** The Glacier Connector is not available for the Alfresco Community Edition versions of the products.

> **Note:** Alfresco Content Connector for AWS Glacier 2.2 can be applied to Alfresco Content Services 6.2 - 7.1 only.

> **Important:** For customers who've previously used the **Archive** action in a folder rule to move content into AWS Glacier: this is no longer supported. **Customers wishing to continue using this functionality should not upgrade to Alfresco Content Services 7.2.** The S3 REST API provides support for moving content to AWS Glacier or content can be manually moved to Glacier via the AWS S3 tools.

The following diagram shows a simple representation of how Alfresco Content Services, Alfresco Governance Services, the S3 Connector and the Glacier Connector interact with Amazon S3 (Amazon Simple Storage Service). The S3 Connector connects you with Amazon S3 and the Glacier Connector allows you to connect with Amazon S3 Glacier.

![glacier-architecture]({% link aws-glacier/images/glacier-architecture.png %})

## Amazon S3 Glacier retrieval tiers {#retrieval-tiers}

Amazon S3 Glacier has three different retrieval tiers.

### Expedited retrieval

Expedited retrieval allows you to quickly access your data when you need to have almost immediate access to your information. This retrieval type can be used for archives up to 250MB. Expedited retrieval usually completes within 1 and 5 minutes.

### Standard retrieval

Standard retrieval provides access to any of your archives within several hours. Standard retrieval usually takes between 3 and 5 hours to complete.

### Bulk retrieval

Bulk retrieval is Amazon S3 Glacier's lowest-cost retrieval type. You can retrieve large amounts of data inexpensively. Bulk retrieval usually completes within 5 and 12 hours.

> **Note:** For more information on Amazon S3 Glacier retrieval tiers, see [Retrieving Glacier Archives](https://docs.aws.amazon.com/amazonglacier/latest/dev/downloading-an-archive-two-steps.html){:target="_blank"}.
---
title: Configure Glacier Connector
---

You can configure rules in Alfresco Content Services and Alfresco Governance Services that archive or restore your files when using Amazon S3 Glacier.

## Creating a rule for archiving files

To archive files to Amazon S3 Glacier, you need to create a rule for your archive folder in Alfresco Content Services or Alfresco Governance Services that indicates you want to archive its content.

> **Note:** Once a file has been archived to Amazon S3 Glacier, the only information available to you in Alfresco Content Services or Alfresco Governance Services is the metadata of the file. You will receive a message that informs you that the content is being archived. Only when a file has been restored does it become available again.

1. Login to Alfresco Content Services.

2. Create a folder that you can use as your archive folder.

    Anything moved here will be archived to Amazon S3 Glacier.

    > **Note:** Creating an archive folder for a Records Management site in Alfresco Governance Services has a minor limitation. See [Glacier Connector FAQs]({% link aws-glacier/latest/using/index.md %}) for more details.

3. Select **More** for the new folder and then click **Manage Rules**.

4. Click **Create Rules**.

5. Enter a name for the new rule.

6. Define your rule and select **Archive to AWS Glacier** from the **Perform Action** list.

     For more information see the Alfresco Content Services documentation, [Creating a rule]({% link content-services/7.1/using/content/rules.md %}).

7. Select **Run rule in background**.

8. Click **Create**.

## Creating a rule for restoring files

To restore files from Amazon S3 Glacier, you need to create a rule for your restore folder in Alfresco Content Services or Alfresco Governance Services. When the file is restored you will see the content of the file, otherwise you will see a message stating the file is being archived or pending restoration.

1. Log in to Alfresco Content Services.

2. Create a folder that you can use as your restore folder.

    Anything you request to be restored will be moved here.

    > **Note:** Creating a restore folder for a Records Management site in Alfresco Governance Services has a minor limitation. See [Glacier Connector FAQs]({% link aws-glacier/latest/using/index.md %}) for more details.

3. Select **More** for the new folder and then click **Manage Rules**.

4. Click **Create Rules**.

5. Enter a name for the new rule.

6. Define your rule and select **Restore from AWS Glacier** from the **Perform Action** list.

    For more information see the Alfresco Content Services documentation, [Creating a rule]({% link content-services/7.1/using/content/rules.md %}).

7. Select **More** for the new folder and then click **Manage Rules**.

8. Click **Create Rules**.

9. Enter a name for the new rule.

10. Define your rule and select **Restore from AWS Glacier** from the **Perform Action** list.

11. Select your restoration tier.

    For more information on tiers see [Amazon S3 Glacier retrieval tiers]({% link aws-glacier/latest/index.md %}#retrieval-tiers).

12. Enter a number of days in the **Expiration in days** field.

    Enter how many days you want access to a restored file for, once it has been restored.

13. Select **Run rule in background**.

14. Click **Create**.
---
title: Install Glacier Connector
---

Use this information to install the Glacier Connector. You install the Glacier Connector by using an Alfresco Module Package (AMP).

## Prerequisites

There are a number of software requirements for installing the Glacier Connector. It can only be installed using an Alfresco Module Package (AMP) file.

### Alfresco requirements

* Alfresco Content Services - [installed using the distribution zip]({% link content-services/7.1/install/zip/index.md %})

* Alfresco Content Connector for AWS S3 - [installed and configured]({% link aws-s3/4.1/install/index.md %})

* (Optional) Alfresco Governance Services - [installed using the distribution zip]({% link governance-services/7.1/install/zip.md %})

See [Supported Platforms]({% link aws-glacier/latest/support/index.md %}) for more information.

> **Note:** You don't need to install Alfresco Governance Services to use the Glacier Connector with Alfresco Content Services. You must have an Alfresco Governance Services **license** to use the Glacier Connector, even if you don't intend to use Alfresco Governance Services. If you plan to use Alfresco Governance Services with the Glacier Connector, ensure that you read the [Glacier Connector FAQs]({% link aws-glacier/latest/using/index.md %}) before you proceed.

> **Important:** If you're already using Amazon S3 with WORM storage, you're unable to use the Glacier Connector. Amazon S3 with WORM storage requires that you use multiple buckets, which is not supported by the Glacier Connector. See [Configuring multiple buckets using S3 Connector]({% link aws-s3/4.1/config/index.md %}#multibucketconfig) for more.

### AWS related requirements

To use the S3 Connector and Glacier Connector you need an AWS account. See [AWS](https://aws.amazon.com/){:target="_blank"} for more information.

## Installing using AMP file

These steps describe how to install the Glacier Connector to an instance of Alfresco Content Services when you installed it using a distribution zip. The Glacier Connector is packaged as an Alfresco Module Package (AMP) file and is installed using the Module Management Tool (MMT).

When you purchase the Glacier Connector, a support case is created with the AMP file attached. If you no longer have access to the AMP file, or you didn't receive a case notification, raise a new case through [Hyland Community](https://community.hyland.com/){:target="_blank"}.

1. Stop Alfresco Content Services.

2. Use the Module Management Tool (MMT) to install the `alfresco-glacier-connector-repo-2.2.x.amp` file into the repository WAR (`alfresco.war`).

    See the Alfresco Content Services documentation for [Using the Module Management Tool (MMT)]({% link content-services/7.1/develop/extension-packaging.md %}#using-the-module-management-tool) and [Installing an Alfresco Module Package]({% link content-services/7.1/install/zip/amp.md %}).

3. Restart Alfresco Content Services.

## Creating a lifecycle rule in Amazon S3

These steps describe how to use the AWS Management Console to create a lifecycle rule in Amazon S3. The lifecycle rule allows you to manage the archiving of your files to Amazon S3 Glacier.

> **Note:** Ensure you have the required AWS login credentials before you begin.

1. Log in to your AWS Management Console and then open the **S3 console**.

2. Search for and select the S3 bucket you want to use as your Amazon S3 Glacier content store.

3. Select the **Management** tab.

4. Click **Add lifecycle rule**.

    This creates a lifecycle rule to define how Amazon S3 manages your files stored in an S3 bucket.

5. Enter a name for the rule.

6. Add the following tag and then press **Enter**:

    ```text
    archive | now
    ```

7. Click **Next**.

8. Select **Current version**.

9. From the **Object creation** list select **Transition to Amazon Glacier after**.

10. Enter **0** for **Days after creation** and then Click **Next**.

    Even when a transition of 0 days has been entered there may still be a minor delay.

11. Ensure **Current version** is the only item selected and then click **Next**.

12. Review your lifecycle rule and then click **Save**.

These steps can also be performed using the Amazon S3 API. For more information, see:

* [PUT Bucket lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketLifecycleConfiguration.html){:target="_blank"}
* [Examples of Lifecycle Configuration](https://docs.aws.amazon.com/AmazonS3/latest/dev/lifecycle-configuration-examples.html){:target="_blank"}
---
title: Supported platforms
---

The following are the supported platforms for the Content Connector for AWS Glacier 2.2:

| Version | Notes |
| ------- | ----- |
| Alfresco Content Services 7.1.x | |
| Alfresco Content Services 7.0.x | |
| Alfresco Content Services 6.2.2 | |
| | |
| **Integrations** | Check the individual documentation on prerequisites and supported platforms for each integration. Check the compatibility of each integration in your installed version of [Alfresco Content Services]({% link content-services/7.1/support/index.md %}). |
| Alfresco Governance Services | |
| Alfresco Content Connector for AWS S3 | |
---
title: Glacier Connector FAQ
---

Here are the answers to some frequently asked questions.

## Why can't I create an **Archive** or **Restore** rule in a Records Management site?

The **Archive** or **Restore** rule isn't available on a folder when creating a rule on a Records Management site. To move declared records from S3 to Amazon S3 Glacier, they must first be declared as Easy Access records from a collaboration site. You can then configure the **Archive** or **Restore** rule on the folder in the collaboration site.

> **Note:** The **Archive** and **Restore** action is available using the v1 REST API and is displayed as an action in the rules engine for Alfresco Content Services.

## Why can't I view the content of the Record version of a file?

When a file is 'Declared version as record' the record created has the same internal content url as the file. If the original file has been archived, the declared as version node has not been marked as archived in Alfresco Content Services. For the Record version file you won't receive the message stating the content has been archived.

> **Note:** See additional information in the [S3 Connector FAQs]({% link aws-s3/4.1/using/faq.md %}).
