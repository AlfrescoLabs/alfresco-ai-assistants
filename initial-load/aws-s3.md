---
title: Alfresco Content Connector for AWS S3
---

The Content Connector for AWS S3 is an add-on module that provides an alternative content store. It uses Amazon's Simple Storage Service (S3) as the storage mechanism for Alfresco Content Services, allowing for virtually unlimited and inexpensive storage.

This release of the S3 Connector is a compatibility release to support Alfresco Content Services 23.1 and Java 17.

Other features introduced in previous versions include:

* Support for AWS Glacier storage type and introduction of [Cloud Storage Properties]({% link aws-s3/latest/config/index.md %}#cloud-storage-properties) (v5.0).
* [Direct Access URLs]({% link aws-s3/latest/config/direct-access.md %}) (v4.1)
* [S3 Content Store Subsystems]({% link aws-s3/latest/config/index.md %}#content-store-subsystems) (v3.1)
* S3MultipleBuckets subsystem configuration (v3.1)
* Changes to the S3 Connector configuration and properties (v3.1)
* Support for AWS S3 for on-premises installation of Alfresco Content Services (v2.1)
* [AWS S3 Standard - Infrequent Access (S3 IA) storage class](https://aws.amazon.com/s3/storage-classes/){:target="_blank"} support (v2.1)
* Refactored to use AWS SDK instead of old JetS3t libraries as it's less error prone (v2.0)
* [AWS Identity and Access Management (IAM)](https://aws.amazon.com/iam/){:target="_blank"} support (v2.0)
* [AWS Key Management Service (KMS)](https://aws.amazon.com/kms/){:target="_blank"} support (v2.0)
* Storage path approach optimized for high-throughput reads and writes (v2.0)
* Handling incomplete multipart uploads abort (v2.0)

The AWS SDK provides better support, stability, and extensibility for developers, and is more actively maintained.

>**Important:** The S3 Connector 6.1 module can be applied to Alfresco Content Services 23.2.

>**Important:** To leverage the full capabilities, it's recommended to run your Alfresco Content Services instance on 
>Amazon's Elastic Compute Cloud (EC2), connected to Amazon's Simple Storage Service (S3). From S3 Connector 2.1 you can 
>also use the S3 Connector with an Alfresco Content Services instance running on-premises, with 
>[some limitations]({% link aws-s3/latest/config/index.md %}#onpremconfig). Other devices or services that advertise as 
>being S3 compatible have not been tested and aren't supported.

The following diagram shows a simple representation of how Alfresco Content Services and the S3 Connector interact with AWS S3.

![]({% link aws-s3/images/s3-simple-architecture.png %})
---
title: Direct Access URLs
---

The main purpose of Direct Access URLs (or DAUs) is to accelerate the local download of content by allowing you to have direct content URLs for your binary content that can help with distributed content repositories in customer environments, and cloud deployments.

AWS S3 provides a way of generating [pre-signed URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html){:target="_blank"} for sharing objects. This feature is a perfect candidate for implementing direct access to your content.

> **Note:** The AWS S3 pre-signed URLs are temporary links with an expiration time.

The Alfresco repository infrastructure now supports direct access URLs. This includes the `ContentService` and the `ContentStore` interface for which default methods have been provided so that `ContentStore` implementations for older versions of this interface throw a `Not Supported` exception. The new methods are auditable using the node reference and time (in seconds) for which the DAU is valid as the parameters.

ReST API endpoints can be used for requesting a new DAU (i.e. a direct download link) for a specific file in the content repository.

Access to direct URLs is strictly controlled. Their expiration date is set/restricted by configurations in the repository using global and content store specific properties.

* Values in the content store properties, **default expiry time** and **maximum expiry time**, are used in preference to the system-wide properties, if valid.
* If invalid, an attempt is made to default to the system-wide properties.
* However, if that still doesn't result in a valid configuration, the DAUs for that specific content store are disabled.

## Default configuration

Direct access URLs are disabled by default. This means the following configuration properties are `false`:

* `system.directAccessUrl.enabled`
* `restApi.directAccessUrl.enabled`
* `connector.s3.directAccessUrl.enabled`

## System-wide configuration

Below are the system-wide configuration settings required in Content Services.

| Property | Description |
| -------- | ----------- |
| system.directAccessUrl.enabled | Controls whether this feature is available, system-wide (for example `false`). <br><br>For DAUs to work, the feature needs to be enabled both system-wide and on the individual Content Store. |
| system.directAccessUrl.defaultExpiryTimeInSec | Sets the default expiry time for the DAU across all Content Stores (for example `30`). <br><br>Its value cannot exceed the system-wide maximum expiry time (`system.directAccessUrl.maxExpiryTimeInSec`) - it can only be equal or lower (otherwise all DAUs are disabled). <br>**Note:** This property is **mandatory** if DAUs are enabled system-wide - (otherwise all DAUs are disabled). |
| system.directAccessUrl.maxExpiryTimeInSec | Sets the upper limit for the DAUs expiry time in seconds (for example `300`, i.e. `5 minutes`). <br><br>This means that a Content Store will be able to override this value but not exceed it, and the same goes for the clients. A service (Java Interface) client will be able to request a DAU for a custom expiry time but that time can't exceed this value. If the requested time exceeds the maximum value, the expiry time reverts to the default configured one. <br>**Note:** This property is **mandatory** if DAUs are enabled system-wide - (otherwise all DAUs are disabled). |

## ReST API configuration

The ReST API configuration only affects the ReST layer in Content Services.

| Property | Description |
| -------- | ----------- |
| restApi.directAccessUrl.enabled | Enables/disables DAU requests via the ReST API (for example `false`). |
| restApi.directAccessUrl.defaultExpiryTimeInSec | Sets the expiry time in seconds for all the DAUs requested via a ReST call (for example `30`). DAU ReST API calls cannot request an explicit expiry time - unlike the service layer calls).<br><br>Its value cannot exceed the system-wide maximum expiry time configuration (`system.directAccessUrl.maxExpiryTimeInSec`) - it can only be equal to or lower (otherwise the ReST API DAUs are disabled).<br><br>If it's not set, the default system-wide property is used (`system.directAccessUrl.defaultExpiryTimeInSec`). |

## Storage connector content store

In the example of the S3 Connector, each content store (i.e. "final" content store, one that provides actual storage, as opposed to a caching content store), should have dedicated configuration options:

| Property | Description |
| -------- | ----------- |
| connector.s3.directAccessUrl.enabled | Controls whether DAUs are enabled on this specific content store (for example `false`). |
| connector.s3.directAccessUrl.defaultExpiryTimeInSec | Sets the expiry time in seconds for the DAU in this store, by overriding the global configuration (for example `30`). <br><br>If this value exceeds the content store limit (described below) or the global limit it should fallback to the global configuration. Its value cannot exceed the system-wide maximum expiry time configuration (`system.directAccessUrl.maxExpiryTimeInSec`) - it can only be equal or lower (otherwise DAUs for the specific content store will be disabled). <br><br>If it's not set, the default system-wide setting is used (`system.directAccessUrl.defaultExpiryTimeInSec`). |
| connector.s3.directAccessUrl.maxExpiryTimeInSec=300 | The maximum expiry time interval that can be requested by clients - content-store specific setting. <br><br>Its value cannot exceed the system-wide configuration (`system.directAccessUrl.maxExpiryTimeInSec`) - it can only be equal or lower (otherwise DAUs for the specific content store will be disabled). <br><br>If it's not set, the default system-wide setting is used (`system.directAccessUrl.maxExpiryTimeInSec`). |

> **Note:** Callers within the platform (i.e. Java interfaces) can either request a specific expiry time or rely on the default value.

> **Note:** When multiple S3 buckets are used for storage in Alfresco, each S3 Content Store can be configured with either the default (common) S3 Connector-specific properties (i.e. `connector.s3.directAccessUrl.enabled` etc.), or new separate properties can be defined for each and every store (i.e. `connector.s3store1.directAccessUrl.enabled`, `connector.s3store2.directAccessUrl.enabled`, etc.).

## Configuration priorities

For DAUs to be usable on the service-layer, the feature must be enabled both system-wide and on the content-store(s). 
For the feature to be usable through ReST (outside the JVM) the *rest-api configuration* must also be enabled.

The `system.directAccessUrl.enabled` property is the main switch for this feature. If this is set to false, then **all** 
DAUs are disabled.

The next configuration that controls specific DAUs is the one for the content store. The `connector.s3.directAccessUrl.enabled` 
property controls whether DAUs are enabled for that specific store.

Whether a client can request a DAU by using a ReST endpoint is controlled by the `restApi.directAccessUrl.enabled` 
property. If the ReST endpoint is disabled, but the feature is enabled system-wide and on the content-store, then the 
DAUs will only be usable by Java clients (i.e. only service-level requests will be possible).

## APIs
The ReST API.

### ReST endpoints

The following endpoints can be used to send requests to obtain DAUs in Content Services:

* `POST /nodes/{nodeId}/request-direct-access-url`
* `POST /nodes/{nodeId}/renditions/{renditionId}/request-direct-access-url`
* `POST /nodes/{nodeId}/versions/{versionId}/request-direct-access-url`
* `POST /nodes/{nodeId}/versions/{versionId}/renditions/{renditionId}/request-direct-access-url`
* `POST /deleted-nodes/{nodeId}/request-direct-access-url`
* `POST /deleted-nodes/{nodeId}/renditions/{renditionId}/request-direct-access-url`

Optionally, the POST body can specify an `attachment` flag. A value of `true` indicates that a download link is required; `false` indicates an embedded link is required. This defaults to `true` if it's not specified.

The endpoints return the following type of response for the S3 connector:

```json
{
  "entry": {
    "contentUrl": "https://<bucket_name>.s3.<region_name>.amazonaws.com/<binary_name>.bin?response-content-disposition=attachment%3B%20filename%20%3D%22graph.JPG%22&response-content-type=image%2Fjpeg&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJGMEQCIDmc%2Fb1e55l4sQjKGG3%2Fr1CU0gtzOOqFnr0Q%2BuXoNa%2BXAiB5oSPGJI1%2FZORobOtV%2BUmiim6GMQJxoKT9I%2Fn6t9ANvir6AwgUEAMaDDE3NTEyNTQyOTQ0MiIMA1qC5mzeuQyHnfd%2BKtcDgAHmPq1MEq5lrb2ggn7Ev%2FSJ%2FQgMVB33Y7NyfsD4BTB3Cn7e1uH17uIH8SkHX6tA9cjBOKx6Sym3gzzP2kTdKSPimQ1UOXMw4uhtaI0f%2FkqnI%2BhMh6GZXT6lOfqDE%2Fkz9nM3QuBxaNI2b8Nb71lP0KPmq7bzBagJOIccf2%2BK3VW3en5gS%2FVAoU2Wx8j1HEQJuk%2FS1whspl970hPFXKIFGIbedO5H8P66wOYdb9LKiHVxvNK7cAJfrVT6jnmqf1L6GyRJa01xgOqgUw1LvsqGsf8kkw%2FkWwJz25StcmJLtpLcWsmZ0x8aHmDNi8SHixteB5XXKJ9Bv8Ex0iIMH3%2Bs8uWmBFssu9il6u8GyV%2FlaIhKYcZLLpIFSTtVudWe60UpQhFPqyHZ6gqqi4e%2BZZfGqqhUNbZucqMvc31V76NbvwdHxI%2F0H0I8fVqCtIatO655qtq6sy%2B29qYymE7RLI9Vnrotkz%2FJafHt4LDIOjX3aDcHS0%2FTxr4QmyJbh%2B%2F0JKsSlqyoosUgzi0mqzw0B8zsTlrkfR9dPkQTNntxZoARaddEIA4Q8QRryQLFe8FITeHSFhUpdPXei3ZEmguSUpkqUQroUdQm8W3C2aoV%2F0A%2BS80IaffqNUY6MPawjpAGOqYBSMI0t5Xt7oW8QqGQrDSMllhX18T0UoxNEvYBii6vFzjuKKasQV5WaGtOMhcg8B5Ee7AxXTCl06FSPhmrQ3f%2FtFTqYtbd8FR8QTK0ZJekBMoM5thzFJ4EztnCYrkAnDo1oDUDOuBQxVho8w5llTEaKLo1SgomysnvpRFshJdBl%2BKXuFVM6Q2tmqSCY%2Bmm%2BVVte%2Bt8Yc4Ulg5eZpkkt3g2HOBaI0cnOw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220209T115428Z&X-Amz-SignedHeaders=host&X-Amz-Expires=30&X-Amz-Credential=ASIASRRSJ7TBNPZVGWOY%2F20220209%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=6b240b52024eca8a07e47dfad6970f84a75de049a1ae7af5855ed8c655f76cda",
    "attachment": true,
    "expiryTime": "2022-02-09T11:54:58.700+0000"
  }
}
```

The length of time for which a direct access URL is valid defaults to `30` seconds if not configured otherwise in `alfresco-global.properties`.

**Method:** `POST`

**Response:**

Link to the resource wrapped in a JSON Object which also contains an attachment flag and the DAU expiration date.

**Error codes:**

If there's no DAU provider installed in Alfresco (such as the S3 Connector), or DAUs aren't enabled, then a `501` HTTP status code is returned.

**Parameters:**

* `attachment` is an optional flag which controls the download method (attachment URL vs. embedded URL). Defaults to `true` when not specified, which means the value of the [Content-Disposition](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition){:target="_blank"} response header will be attachment.
* The `filename` part of the `Content-Disposition` header will be set in the service layer logic, and can't be controlled by the DAU client.

### Discovery API

The Discovery API provides status information about the DAUs feature (enabled/disabled) via a new field:

* `RepositoryInfo > StatusInfo > isDirectAccessUrlEnabled`

For example:

```json
"status": {
        "isReadOnly": false,
        "isAuditEnabled": true,
        "isQuickShareEnabled": true,
        "isThumbnailGenerationEnabled": true,
        "isDirectAccessUrlEnabled": true
      },
```

This field is `true` only when **all** of the following conditions are met:

* DAUs are enabled system-wide.
* DAUs are enabled on the ReST API.
* If there's at least one ContentStore that's configured and has DAUs enabled.

#### **S3 Connector**

The [AWS Java S3 SDK](https://docs.aws.amazon.com/AmazonS3/latest/dev/ShareObjectPreSignedURLJavaSDK.html){:target="_blank"} is used to generate the pre-signed DAUs with the configured duration (see the configuration settings for the repository and Content Store expiry times). The pre-signed request generates a download for the remote content.

**Known limitations:**

DAU generation on AWS S3 depends on the security credentials used - see [Sharing an object with a presigned URL](https://docs.aws.amazon.com/AmazonS3/latest/dev/ShareObjectPreSignedURL.html){:target="_blank"} for more details.

See the [GitHub project documentation](https://github.com/Alfresco/acs-packaging/blob/master/docs/direct-access-urls.md#main-flows){:target="_blank"} for a detailed view of the main flows and other parts of the implementation.
---
title: Configure Content Connector for AWS S3
---

The Content Connector for AWS S3 is configured using properties set in the `alfresco-global.properties` file.

## Default configuration properties
These are the configuration properties that are applied when you install the S3 Connector:

```text
# Location where new buckets should be created if they do not exist. The default Region is US East (N. Virginia).
# For a list of available AWS Regions, see Regions and Endpoints in the AWS General Reference.
connector.s3.bucketRegion=us-east-1

# Encryption to be requested for items stored in S3. Used to set the header x-amz-server-side-encryption when the content is added.
connector.s3.encryption=AES256

# A number of retries in case an error occurs
connector.s3.maxErrorRetries=3

# The minimum days to wait before aborting an incomplete multipart upload. If the value is 0 then the abort is disabled.
connector.s3.abortIncompleteMultipartUploadDays=1

# Cloud Storage Properties configuration
connector.s3.nativeStorageProperties=x-amz-archive-status,x-amz-restore,x-amz-storage-class
connector.s3.restoreExpiryDaysDefault=7
connector.s3.restoreTierDefault=Standard
connector.s3.archiveClassDefault=Glacier

# Default S3 content store subsystem
filecontentstore.subsystem.name=S3OnPrem

# Repository Content cashing
system.content.caching.maxUsageMB=51200
system.content.caching.minFileAgeMillis=0
```

If you need to override them for your environment, check the available settings in the configuration guides or 
[properties reference]({% link aws-s3/latest/config/index.md %}#properties-reference).

## Basic configuration properties
The following properties needs to be set up specifically for your environment and access to AWS S3.

1.  Open the `<classpathRoot>/alfresco-global.properties` file.

    If you plan to use IAM roles instead of AWS access and secret keys, ensure you have 
    [configured AWS Identity and Access Management]({% link aws-s3/latest/config/index.md %}#configiam) correctly 
    before continuing from step [4]({% link aws-s3/latest/config/index.md %}#bucketName).

    If you have existing content in a local contentstore (i.e. where Alfresco Content Services is deployed on-premises) 
    and you'd like to transition to using AWS S3 as the only content store, ensure you include the property described in 
    [Configuring S3 Connector on-premises]({% link aws-s3/latest/config/index.md %}#onpremconfig) before continuing.

2.  Add the `connector.s3.accessKey` property, for example:

    ```text
    connector.s3.accessKey=AKIAIOSFODNN7EXAMPLE
    ```

    The access key is required to identify the AWS account and can be obtained from the AWS Management Console. 
    See [AWS Credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys) 
    for access details.

3.  Add the `connector.s3.secretKey` property, for example:

    ```text
    connector.s3.secretKey=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    ```

    The secret key is required to identify the AWS account and can be obtained from the AWS Management Console. 
    See [AWS Credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys) 
    for access details.

4.  Add the `connector.s3.bucketName` property, for example:

    ```text
    connector.s3.bucketName=myawsbucket
    ```

    The bucket name must be unique among all AWS users globally. If the bucket does not already exist, it will be created, 
    but the name must not have already been taken by another user. If the bucket has an error, it will be reported in 
    the alfresco.log file. See [S3 bucket restrictions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html) 
    for more information on bucket naming.

5.  Add the `connector.s3.bucketRegion` property as specified in the [AWS service endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region) page.

    The value is taken from the *Code* column. For example, for *Region Name* Europe (Frankfurt):

    ```text
    connector.s3.bucketRegion=eu-central-1
    ```

    >**Note:** If you use a region other than the US East (N. Virginia) endpoint (previously named US Standard) to 
    > create a bucket, `connector.s3.bucketRegion` is a mandatory field. Use the [AWS service endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region) 
    > for guidance on the correct value.

6.  Set the type of content store subsystem, for example:

    ```text
    filecontentstore.subsystem.name=S3
    ```

    This sets the active content store subsystem to S3 only, as opposed to the default subsystem, `S3OnPrem`, which sets 
    an aggregating content store: S3 and file system.

    >**Note:** This setup is recommended for a new clean installation of Alfresco Content Services and the S3 Connector.

    **Optional configuration properties**

7.  If you plan to use the AWS KMS service to manage encryption, you'll need to change the default `s3.encryption` setting.

    See [Configuring AWS Key Management Service]({% link aws-s3/latest/config/index.md %}#configkeymgmt) for more encryption options.

8.  Set where the cached content is stored, and how much cache size you need.

    The cached content location (and default value) is `dir.cachedcontent=${dir.root}/cachedcontent`. See 
    [CachingContentStore properties]({% link content-services/latest/admin/content-stores.md %}#caching-content-store-ccs) 
    for more information on the caching content store.

    >**Note:** The size of the local caching content store can be configured as necessary to limit its use to a maximum 
    > overall size or by files with a maximum file size. For example:
    > ```text
    > # Maximum disk usage for the cache in MB 
    > system.content.caching.maxUsageMB=51200
    > # Maximum size of files which can be stored in the cache in MB (zero implies no limit) 
    > system.content.caching.maxFileSizeMB=0
    > ```

    The S3 Connector supports multipart uploads where files larger than 20MB are split. The file upload is attempted and 
    retried, in case there are issues, up to a specific limit.

9.  Set the number of days that Amazon S3 should keep the files which are incomplete or aborted uploads, before marking 
    them for deletion:

    ```text
    connector.s3.abortIncompleteMultipartUploadDays=1
    ```

    >**Note:** If lifecycle configuration on the bucket is not required, then set the value to `0`:
    > ```text
    > connector.s3.abortIncompleteMultipartUploadDays=0
    > ```

    See [Multipart upload overview](#multipart-upload-overview) for more details.

10. If you want to apply a tag to your content when it's written into the S3 bucket, you can add the 
    `connector.s3.tagName` and `connector.s3.tagValue` properties.

    See [Properties reference]({% link aws-s3/latest/config/index.md %}#properties-reference) for more details.

    >**Note:** Use the AWS documentation [Object key and metadata](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html) 
    > for naming guidelines, as the properties must respect the same restrictions as if they were added via the 
    > AWS Management Console.

11. Starting from version 3.1, the S3 Connector has the deleted content store disabled by default, since this feature is 
    already present in Amazon's S3 service. For details on how to re-enable it, see 
    [S3 Connector deleted content store](#enabledeletedcontentstore).

12. Save the `alfresco-global.properties` file.

    You are now ready to start Alfresco Content Services.

## Cloud Storage Properties configuration {#cloud-storage-properties}
Cloud Storage Properties are represented as a key-value pair (String-String) collection. Mentioned pairs are either directly 
retrieved from Cloud Storage Provider APIs object headers or derived from their values.

Storage Properties are reflected at the content level and content may (especially when in Cloud Storage) or 
may not have at least one such property. **Storage Properties are not persisted as part of the metadata** (or any other way), 
so we rely on the `ContentStore` and `ServiceAdapter` implementations to provide the means to retrieve/derive the 
storage properties information.

When cloud connectors do not provide functionality to retrieve storage properties, none will be returned.

Configuration properties applicable to AWS Cloud Storage Properties functionality:

|Property name |Property value|Description|  
|---|---|---|
|`connector.s3.nativeStorageProperties`|`x-amz-archive-status,x-amz-restore,x-amz-storage-class`|Limits the list of S3 specific storage properties to be retrived|
|`connector.s3.archiveStorageClass`|`GLACIER` / `DEEP_ARCHIVE`|Archive storage class set for content archive request.|
|`connector.s3.restoreExpiryDays`|7|Default number of expiration days for archive-restore|
|`connector.s3.restoreTierDefault`|`Standard` / `Expedited`|Default archive-restore tier (restore priority). Used when no respective value passed in archive-restore request.|

The following headers are currently (by default) returned from AWS S3 Storage:

|Name |Possible values|  
|---|---|  
|`x-amz-storage-class`| `REDUCED_REDUNDANCY` / `STANDARD_IA` / `ONEZONE_IA` / `INTELLIGENT_TIERING` / `GLACIER_IR` / `GLACIER` / `DEEP_ARCHIVE` / `OUTPOSTS`|  
|`x-amz-archive-status`| `ARCHIVE_ACCESS` / `DEEP_ARCHIVE_ACCESS`|  
|`x-amz-restore`| Complex, e.g.  `ongoing-request="false", expiry-date="Fri, 21 Dec 2012 00:00:00 GMT"`|

>**Note**: 'STANDARD' AWS S3 storage class is not returned by AWS S3 API (hence, nor by the S3 Connector), however it appears in AWS docs

Derived Storage Properties are Alfresco specific and currently reflecting information whether content is archived 
(offline) and whether it is being restored from offline state (and for how long):

|Name |Possible values|Description|  
|---|---|---|
|`x-alf-archived`|`true`, `false`|Indicates whether content is archived (offline) and not immediately accessible|
|`x-alf-archive-restore-in-progress`|`true`, `false`|Indicates whether a request to restore content from archive is progress.|
|`x-alf-archive-restore-expiry`|YYYYMMDDThhmmssZ (ISO-8601) datetime|Indicates expiry time for content restored from archive, applicable to AWS S3|

## Backwards compatibility configuration properties
You may need to configure a number of optional properties for the S3 Connector to ensure backwards compatibility with 
S3 Connector 1.x and behavior.

* `dir.contentstore`

    The `dir.contentstore` property provides backwards compatibility with S3 Connector 1.x.

    **S3 Connector 1.x**

    S3 Connector 1.x doesn't create S3 object IDs (or paths) that are ideal for high-scale S3 read and write request 
    rates. To help achieve this, `dir.contentstore` should be ignored except for backwards compatibility reads of 
    existing content stored in Alfresco Content Services.

    When using S3 Connector 1.x the format of the S3 path is:

    ```text
    /{contentRoot}/{tenant}/[datepath/]{guid}.bin
    ```

    When `s3.flatRoot=true` the s3 path format is:

    ```text
    /{contentRoot}/{tenant}/{guid}.bin
    ```

    **S3 Connector 2.0**

    Starting from S3 Connector 2.0 `dir.contentstore` is ignored except for backwards compatibility reads.

    When `flatRoot=true` the s3 path format is:

    ```text
    /{tenant}/{guid}.bin
    ```

    When `flatRoot=false` the s3 path format is:

    ```text
    /{tenant}/{datepath}/{guid.bin}
    ```

    >**Note:** The behavior of existing properties `s3.flatRoot` and `dir.contentstore.deleted` is maintained. You can 
    > apply the S3 Connector v2.0 to an existing installation where S3 Connector v1.x was previously used without 
    > affecting the running of the system. This means existing paths remain as they are, and new paths are generated 
    > based on your configuration.

* `s3.useTenantDomainInPath`

    Added in S3 Connector v2.0. When the property value is set to `true` the tenant domain is added to the S3 path. 
    This was the default behavior in S3 Connector v1.x. The change in the default property value is required to achieve 
    an optimal path for high throughput reads and writes where:

    ```text
    s3.useTenantDomainInPath=false
    dir.contentstore=
    s3.flatRoot=true
    ```

    You can apply S3 Connector 2.0 to an existing installation where S3 Connector 1.x was previously used without affect 
    to the running of the system. This means that existing paths remain as they are, and new paths are generated based 
    on your configuration.

    **Example 1:**

    When `s3.useTenantDomainInPath=false` and `s3.flatRoot=true` the s3 path format is:

    ```text
    /{guid}.bin
    ```

    **Example 2:**

    When `s3.useTenantDomainInPath=false` and `s3.flatRoot=false` the s3 path format is:

    ```text
    /{datepath}/{guid.bin}
    ```

## On-premises configuration {#onpremconfig}
Use this information to configure the S3 Connector for an on-premises installation of Alfresco Content Services.

For on-premises customers, AWS S3 is often a more cost effective method to store your content, paying just for what you 
need and does not require you to budget up front for growth capacity.

The S3 Connector is supported as the default content store for Alfresco Content Services. When installed on-premises, 
existing content will remain accessible from your existing content store(s), and all new content is written to the 
S3 content store.

The following diagram shows a simple representation of how an on-premises (on-prem) deployment of Alfresco Content Services 
using the S3 Connector can interact with AWS S3.

![s3-onprem-architecture]({% link aws-s3/images/s3-onprem-architecture.png %})

**Installation and configuration**

You can install and configure Alfresco Content Services and the S3 Connector on-premises using the default configuration. 
Follow the steps in [Installing the S3 Connector]({% link aws-s3/latest/install/index.md %}), and the basic 
configuration steps in [Configuring the S3 Connector]({% link aws-s3/latest/config/index.md %}).

>**Note:** If you have existing content in a local content store, and you'd like to take advantage of the features 
> provided by the S3 Connector, add the following property to `alfresco-global.properties`:
> ```text
> dir.contentstore=${dir.root}/contentstore
> ```

As an existing customer using the default [Encrypted content store]({% link content-services/latest/admin/content-stores.md %}#encrypted-content-store) 
configuration, the environment uses:

* AES256 encryption for new content
* Content decryption on reads from the existing on-premises files

**Best practice**

In order to connect an on-premises instance of Alfresco Content Services to AWS S3, it's recommended that you use the 
default credentials file (`~/.aws/credentials`). This ensures that the `secretKey` and `accessKey` aren't exposed beyond 
what's absolutely necessary. Here's an example credentials file:

```text
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY 
```

**Difference between running in AWS and running outside AWS**

The following table highlights the capabilities that are supported depending on your deployment scenario.

|Deployment|IAM|KMS|
|----------|---|---|
|New deployment (on-prem)|Supported via AWS API keys only|Supported|
|New deployment (in AWS)|Supported via Instance Profile|Supported|
|Existing deployment (on-prem)|Supported via AWS API keys only|Supported|
|Existing deployment (in AWS)|Supported via Instance Profile|Supported|

## Configuring AWS Storage Classes {#configstorageclass}

Use this information to configure S3 Connector for infrequent access to objects stored in AWS S3.

Objects in AWS S3 can be stored under several storage classes during an object's lifetime, such as 
Standard and Standard - Infrequent Access (Standard-IA).

* **Standard**

    This is the default storage class for objects uploaded to AWS S3, and should be used for frequently accessed data.

* **Standard-IA**

    Content should be changed to Standard-IA, or S3 IA, when it's less frequently used. For example, this may be useful 
    for archiving or storing old data that is less likely to be accessed, as this may reduce storage costs. 
    See [Amazon S3 Storage Classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html) and 
    [Amazon S3 Pricing](https://aws.amazon.com/s3/pricing/) for more.

The transition of content from S3 to S3 IA is configured through the AWS console. You can change an object's 
storage class either manually or by adding a lifecycle policy for an S3 bucket. 
See [Creating a Lifecycle Policy](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) for more.

You can use S3 storage class analysis to fine tune the lifecycle rules according to your storage access patterns, 
so that the right data is transitioned to Standard-IA storage class. 
See [Amazon S3 Storage Class Analysis](https://docs.aws.amazon.com/AmazonS3/latest/userguide/analytics-storage-class.html) for more.

**Conditions for changing storage class to Standard-IA**

Before transitioning objects to Standard-IA, consider the following limitations:

* The minimum retention period required before an object can be changed to Standard-IA is 30 days.
* The minimum object size is 128KB.

>**Note:** When using the S3 Connector, new versions of a document are stored using the Standard storage class by default.

Here are some example scenarios to help you consider if using storage classes is right for your environment:

1.  Collaboration: On an S3 bucket with frequently used content as part of any current work.
    * Create a lifecycle rule for content older than **365 days** to be moved to Standard-IA, as part of the aging process.
2.  Document Archiving: On an S3 bucket with content that's known to be archival content.
    * Create a lifecycle rule for content older than **30 days** to be moved to Standard-IA.

The following diagram shows a simple representation of how Alfresco Content Services and the S3 Connector 
interact with AWS S3, when using the default Standard storage class and transitioning content to Standard-IA (S3 IA).

![s3-ia-architecture]({% link aws-s3/images/s3-ia-architecture.png %})

## Configuring AWS Identity and Access Management {#configiam}
AWS Identity and Access Management (IAM) enables you to securely control access to AWS services and resources for 
your users. Using IAM, you can create and manage AWS users and groups, and use permissions to allow and deny their 
access to AWS resources. The S3 Connector uses AWS IAM's roles to ensure fine-grained control over access to 
the content stored in the S3 bucket.

In order to use IAM roles, instead of AWS secret and access keys, a new policy must be created that will be 
used by the IAM role. Policies are used to grant permissions to groups. If there isn't a policy already in 
place for S3 access, a new policy must be created.

1.  Create a new policy.

    You'll need to add the following IAM policy for the S3 Connector to work properly.

    1.  Go to the **AWS Console** and open the **IAM** console.

    2.  Select **Policies** from the menu and click **Create policy**.

    3.  Switch to the **JSON** tab to create the policy using JSON syntax.

    4.  Copy the following content, and replace the bucket name with your bucket name:

        1.  If an S3 bucket already exists, add:

            ```json
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:DeleteObject"
                ],
                "Resource": "arn:aws:s3:::YourBucket/*"
            }
            ```

        2.  If no S3 bucket exists, then add the following action:

            ```text
            "s3:CreateBucket"
            "s3:PutLifecycleConfiguration"
            "s3:GetLifecycleConfiguration"
            ```

        3.  If lifecycle configuration on the bucket is not required, then see step (8) in [Configuring the S3 Connector]({% link aws-s3/latest/config/index.md %}).

    Follow the steps from the AWS site to [Create a New Policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) for additional guidance.

2.  Here are additional configuration options that you can apply to the bucket. These IAM policies grant additional permissions to the IAM user.

    To configure and view the encryption of a bucket:

    ```text
    "s3:PutEncryptionConfiguration",
    "s3:GetInventoryConfiguration"
    ```

    To enable object tagging support (available from S3 Connector version 3.1):

    ```text
    "s3:PutObjectTagging"
    "s3:GetObjectTagging"
    ```

    To access information from various metrics:

    ```text
    "s3:PutMetricsConfiguration"
    "s3:GetMetricsConfiguration"
    ```

    To access to the bucket lifecycle policy:

    ```text
    "s3:PutLifecycleConfiguration"
    ```

    This allows the user to set an Infrequent Access (IA) storage class lifecycle rule on the bucket.

    See the AWS site for more documentation on IAM roles:

    * [What Is IAM?](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
    * [Create a New Policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html).
    * [Getting Started: Security Best Practices](https://aws.amazon.com/blogs/security/getting-started-follow-security-best-practices-as-you-configure-your-aws-resources/)

3.  Use the policy simulator to test the new IAM policy.

    Follow the steps from the AWS site to [Test IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html).

4.  Create a new role. You can attach up to 10 policies to each role.

    Follow the steps from the AWS site to [Create IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html).

    If an Amazon EC2 configuration is already in place, the new policy that you created is attached to the existing role used on the EC2 instance. Follow the steps from the AWS site to [Manage IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage.html).

5.  Attach the role to the EC2 instance where Alfresco Content Services is running.

    Note that one single role can be applied to an EC2 instance.

6.  Edit `alfresco-global.properties` to remove the `connector.s3.accessKey` and `connector.s3.secretKey` properties.

    By removing these properties, the IAM role that's attached to the EC2 instance takes over the responsibility of accessing the S3 bucket.

    You are now ready to start Alfresco Content Services.

## Configuring AWS Key Management Service {#configkeymgmt}
AWS Key Management Service (KMS) is a managed service that makes it easy for you to create and control the encryption 
keys used to encrypt your content.

The primary resources in AWS KMS are customer master keys (CMKs). These are either customer-managed or AWS-managed. 
You can use either type of CMK to protect data encryption keys (or data keys) which are then used to encrypt or 
decrypt content stored by Alfresco Content Services in AWS S3. CMKs never leave AWS KMS unencrypted, but data keys can.

For more details, see [AWS KMS Concepts](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html) 
and [How Envelope Encryption Works with Supported AWS Services](https://docs.aws.amazon.com/kms/latest/developerguide/workflow.html).

To learn more about how AWS KMS uses cryptography and secures master keys, see the 
[AWS Key Management Service Cryptographic Details whitepaper](https://d0.awsstatic.com/whitepapers/KMS-Cryptographic-Details.pdf).

The S3 Connector provides the following encryption options:

|Property setting|Description|
|----------------|-----------|
|connector.s3.encryption|Setting `connector.s3.encryption=none` means content stored in S3 is unencrypted. **Note:** Storing your content unencrypted isn't recommended.|
|connector.s3.encryption=aes256|The content store is encrypted using AWS managed encryption.|
|connector.s3.encryption=kms|The content store is encrypted using AWS KMS managed encryption.|

>**Note:** If the `connector.s3.encryption` property is missing, then the content store is **AES256** encrypted by AWS-managed encryption.

For more information about each of these encryption options, see the [Encryption overview](#encryption-overview).

You can configure AWS KMS by adding the relevant properties to the global properties file.

1.  Edit `alfresco-global.properties` to set the server-encryption algorithm to KMS:

    ```text
    connector.s3.encryption=kms
    ```

    If you plan to use the AWS-managed default master key then continue from step 4.

2.  To use a customer master key, either [create a new KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html) using the AWS steps, or use a CMK by [importing your existing key material](https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html).

3.  Edit `alfresco-global.properties` and set the value of `connector.s3.awsKmsKeyId` property to the key alias (see example) or the Amazon Resource Name (ARN) of the KMS key created.

    ```text
    connector.s3.awsKmsKeyId=alias/kmsKeyAlias
    ```

    You can leave the property empty in order to use the default master key attached to your account.

4.  You are now ready to start Alfresco Content Services.

### Encryption overview
Alfresco supports server-side encryption for content stored in AWS S3. There are several encryption types that you can 
configure to use with S3 Connector. These include AWS Managed Encryption, and AWS Key Management Service (KMS) Encryption.

>**Note:** S3 doesn't work with the [Alfresco Content Encryption]({% link content-services/latest/admin/content-stores.md %}#encrypted-content-store) module. When using the S3 Connector we recommend using AWS KMS.

**AWS Key Management Service (KMS) Encryption**

The AWS name is Server-Side Encryption with AWS KMS Managed Keys (SSE-KMS).

SSE-KMS is similar to SSE-S3, but with some additional benefits plus additional charges for using this service. 
There are separate permissions for the use of an envelope key (that is, a key that protects your data's encryption key) 
that provides added protection against unauthorized access to your content in S3. SSE-KMS also provides an audit 
trail of when your key was used and by whom. You also have the option to create and manage encryption keys yourself, 
or use a default key that is unique to you, the service you're using, and the region you're working in.

For more information, see [Protecting Data Using Server-Side Encryption with AWS KMS-Managed Keys (SSE-KMS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html).

**Customer-Provided Key Encryption**

The AWS name is Server-Side Encryption with Customer-Provided Keys (SSE-C). This type of key allows you to protect your 
data at rest, setting your own encryption keys.

This option isn't supported by the S3 Connector.

For more information, see [Protecting Data Using Server-Side Encryption with Customer-Provided Encryption Keys (SSE-C)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html).

**AWS Managed Encryption**

This is the default encryption mechanism for the S3 Connector. The AWS name is S3-Managed Encryption Keys (SSE-S3).

Amazon S3 encrypts each object with a unique key. As an additional safeguard, it encrypts the key itself with a master 
key that it regularly rotates. Amazon S3 server-side encryption uses one of the strongest block ciphers available, 
256-bit Advanced Encryption Standard (AES-256), to encrypt data.

For more information, see [Protecting Data Using Server-Side Encryption with Amazon S3-Managed Encryption Keys (SSE-S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html).

**Unencrypted**

Storing your content unencrypted isn't recommended.

## Multipart upload overview

The S3 Connector supports multipart uploads where files larger than 20MB are split.

The multipart upload enables you to upload large files in parts, and is triggered when you upload a file larger 
than 20 MB. Amazon S3 stores these parts, but it creates the file from the parts only after you upload all of 
them and send a successful request to complete the multipart upload. Upon receiving the complete multipart 
upload request, AWS S3 constructs the file from the uploaded parts and you can then access the file just as 
you would any other file in your bucket.

**Abort incomplete multipart upload**

If you don't send the complete multipart upload request successfully, AWS S3 will not assemble the parts and will 
not create any file. So the parts remain in S3. As best practice, we recommend you configure a lifecycle rule. 
See [Aborting Incomplete Multipart Uploads Using a Bucket Lifecycle Policy](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html#mpu-abort-incomplete-mpu-lifecycle-config) for more details.

We create the bucket and a global lifecycle rule to enforce the abort and deletion of incomplete uploads automatically 
only if the bucket name configured in the global properties file doesn't exist in S3. In this case, you can configure 
the number of days that S3 should keep the files before marking it for deletion. The default setting is 1 day:

```text
connector.s3.abortIncompleteMultipartUploadDays=1
```

When a file reaches the end of its lifetime, S3 queues it for removal and removes it asynchronously. 
There may be a delay between the expiration date and the date when S3 removes a file.

See [AWS Multipart Upload Overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) for more details.

## Content store subsystems

Starting from version 3.1, the S3 Connector provides out-of-the-box content store repository *subsystems*. Older versions of the S3 Connector hard-wired the Amazon Simple Storage Service (S3) content store directly into Alfresco Content Services.

The repository subsystem approach allows a more flexible use of the S3 content store, even in conjunction with existing content stores. A subsystem can be started, stopped, and configured independently, and it has its own isolated Spring application context and configuration. The S3 subsystems belong to the `ContentStore` category, and have types `S3` or `S3OnPrem`.

See the Alfresco Content Services documentation on [Subsystems]({% link content-services/latest/config/subsystems.md %}) for more.

**S3OnPrem content store subsystem**

This defines an aggregating content store with S3 as the primary content store and the file system as the secondary store.

This configuration is similar to what's used in previous S3 Connector versions (i.e. 2.x - 3.0) and is set as the 
default content store.

**S3 content store subsystem**

This defines a pure S3 content store, which uses S3 as the only storage mechanism for Alfresco Content Services.

This content store is recommended for a clean Alfresco Content Services and S3 Connector installation, 
or an upgrade of an installation that's never used the file system.

**Using an S3 content store subsystem**

The default subsystem that's enabled on installation is **S3OnPrem**. This ensures that the new AMP version is 
compatible with a previous installation. You can change the subsystem used by overwriting the global 
variable `filecontentstore.subsystem.name`, for example:

```text
filecontentstore.subsystem.name=S3
```

>**Important:** We don't recommend switching to a pure S3 content store from S3OnPrem, if binaries have already been saved on the file system.

**Customizing the subsystem properties**

You can manage subsystems by using a JMX client under `MBeans > Alfresco > Configuration > ContentStore > managed`. Here, you can change all the properties defined for the subsystem, and restart the subsystem.

Another way to extend a subsystem is to add a `*-context.xml` and a properties file in the extension path for that subsystem:

```text
alfresco/extension/subsystems/ContentStore/S3/S3/*-context.xml
alfresco/extension/subsystems/ContentStore/S3/S3/*.properties
```

For example, the common bean `s3ClientConfiguration`, used to set AWS SDK client configurations, can be overwritten in a subsystem extension:

```xml
<!-- Client configuration options such as proxy settings, user agent string, max retry attempts, etc. -->
    <bean id="s3ClientConfiguration" class="com.amazonaws.ClientConfiguration">
        <!-- Sets the retry policy upon failed requests -->
        <property name="retryPolicy" ref="s3RetryPolicy"/>
        <!-- Sets whether throttled retries should be used -->
        <property name="useThrottleRetries" value="true"/>
        <property name="requestTimeout" value="${connector.s3.httpRequestTimeout}"/>
    </bean>
```

>**Important:** In Alfresco Content Services 7.1 or  newer and S3 Connector 4.1 or newer, changing the current content store subsystem using the JMX client isn't supported. There's a limitation in Alfresco Content Services which only allows switching between the embedded content stores.

See next section about enabling deleted content store.

## Enable deleted content store {#enabledeletedcontentstore}

The deleted content store support in Alfresco Content Services moves the deleted content (e.g. folders and files) 
to a dedicated location, `contentstore.deleted` (defined by the `dir.s3.contentstore.deleted` property). 
System administrators can schedule a job to delete the binaries from this location.

**Deleted content store support provided by the repository vs. managed by S3 capabilities**

Starting with version 3.1, the S3 Connector has the deleted content store disabled by default, since this feature 
is already present in Amazon's S3 service.

However, you can enable the Alfresco Content Services deleted content store, if required. Just add a context file, 
such as `enable-deleted-content-store-context.xml`, in the `extension` directory:

```text
$CATALINA_HOME/shared/classes/alfresco/extension
```

You can find a sample file in `alfresco-s3-connector-6.1.x.amp':

* `enable-deleted-content-store-context.xml.sample` in `config/alfresco/extension`

This creates a proxy bean to the deleted content store defined in the subsystem. By doing this, the repository knows 
about it when the subsystem is started.

```xml
<bean id="deletedContentStore" class="org.alfresco.repo.management.subsystems.SubsystemProxyFactory">
    <property name="sourceApplicationContextFactory">
        <ref bean="${filecontentstore.subsystem.name}" />
    </property>
    <property name="sourceBeanName">
        <value>deletedContentStore</value>
    </property>
    <property name="interfaces">
        <list>
            <value>org.alfresco.repo.content.ContentStore</value>
        </list>
    </property>
</bean>
```

## Using multiple buckets {#multibucketconfig}

Starting from version 3.1, the S3 Connector contains an S3 multiple buckets sample. If enabled, this adds 
`S3MultipleBuckets` as a third alternative for the S3 content store subsystems.

Review the prerequisites in [S3 Connector content store subsystems](#content-store-subsystems) which introduces 
the S3 content store subsystems. The out-of-the-box S3 subsystems have two possible types: 
`S3` and `S3OnPrem`.

### Overview

The S3 multiple buckets sample is a new content store subsystem that's based on the `StoreSelectorContentStore`. 
The Store selector has two stores (instances of the S3 content store):

* `store1.s3ContentStore` as the default
* `store2.s3ContentStore` as the second one

The sample files are found in `alfresco-s3-connector-6.1.x.amp`:

* `s3-multiple-buckets-context.xml.sample` in `config/alfresco/extension`
* `s3-mb-contentstore-context.xml.sample` and `s3-mb-contentstore.properties.sample` are in `config/alfresco/extension/subsystems/ContentStore/S3MultipleBuckets/S3MultipleBuckets`

### The s3-multiple-buckets-context.xml.sample file 

This file provides a new Spring child Application Context based on the `*.xml` files and `*.properties` files in

```text
alfresco/subsystems/ContentStore/S3MultipleBuckets/S3MultipleBuckets
```

### The s3-mb-contentstore-context.xml.sample file

The subsystem configuration file is split into the following sections to make it easier to extend:

* Deleted content store
* Common configuration
* Stores
* Store selector
* Caching content store

**Deleted content store**

```xml
<bean id="deletedContentStore" class="org.alfresco.integrations.connector.DeletedS3ContentStore"
    depends-on="store1.s3Adapter">
    <property name="contentRoot" value="${dir.s3.contentstore.deleted}" />
    <property name="serviceAdapter" ref="store1.s3Adapter" />
    <property name="nodeService" ref="nodeService" />
    <property name="useContentRootInPath" value="${s3.useContentRootInPath}"/>
    <property name="objNameSuffix" value="${connector.s3.deleted.objectNameSuffix}" />
    <property name="objNamePrefix" value="${connector.s3.deleted.objectNamePrefix}" />
    <property name="storeProtocol" value="${connector.s3.storeProtocol}"/>
    <!-- if true put all files into tenant root folder ! -->
    <property name="flatRoot" value="${s3.flatRoot}" />
</bean>
```

>**Note:** If you re-enable the soft deletion provided by the repository, all deleted files will go to `/dir.s3.contentstore.deleted` from the bucket of the first store (e.g. `connector.s3.bucketName`).

**Common configuration**

This configuration is shared by the two stores.

```xml
<!-- [Start] Common configuration - could be duplicated for each store if needed -->

<bean id="s3RetryPolicy" class="com.amazonaws.retry.RetryPolicy">
    <constructor-arg ref="s3RetryCondition"/>
    <constructor-arg>
        <util:constant static-field="com.amazonaws.retry.PredefinedRetryPolicies.DEFAULT_BACKOFF_STRATEGY"/>
    </constructor-arg>
    <constructor-arg value="${connector.s3.maxErrorRetries}"/>
    <constructor-arg value="false" />
</bean>

<!-- Client configuration options such as proxy settings, user agent string, max retry attempts, etc. -->
<bean id="s3ClientConfiguration" class="com.amazonaws.ClientConfiguration">
    <!-- Sets the retry policy upon failed requests. -->
    <property name="retryPolicy" ref="s3RetryPolicy"/>
    <!-- Sets whether throttled retries should be used -->
    <property name="useThrottleRetries" value="true"/>
    <property name="requestTimeout" value="${connector.s3.httpRequestTimeout}" />
</bean>

<!-- [End] Common configuration -->
```

For more information on how to change this, see [Advanced customization for S3MultipleBuckets subsystem](#advancedconfigmultibucket)

**Stores**

```xml
<!-- [Start] Store 1 -->

<bean id="store1.s3Adapter" class="org.alfresco.integrations.connector.AmazonS3ServiceAdapter" init-method="init">
    <property name="accessKey" value="${connector.s3.accessKey}" />
    <property name="secretKey" value="${connector.s3.secretKey}" />
    <property name="bucketName" value="${connector.s3.bucketName}" />
    <property name="bucketRegion" value="${connector.s3.bucketRegion}" />
    <property name="encryption" value="${connector.s3.encryption}" />
    <property name="abortIncompleteMultipartUploadDays" value="${connector.s3.abortIncompleteMultipartUploadDays}" />
    <property name="autoLowerCaseBucketName" value="${s3.autoLowerCaseBucketName}" />
    <property name="awsKmsKeyId" value="${connector.s3.awsKmsKeyId}" />
    <property name="endpoint" value="${connector.s3.endpoint}" />
    <property name="clientConfiguration" ref="s3ClientConfiguration"/>
    
    <property name="tagName" value="${connector.s3.tagName}" />
    <property name="tagValue" value="${connector.s3.tagValue}" />
</bean>

<bean id="store1.s3ContentStore" class="org.alfresco.integrations.connector.TenantS3ContentStore" depends-on="store1.s3Adapter">
    <property name="useTenantDomainInPath" value="${s3.useTenantDomainInPath}" />
    <property name="contentRoot" value="${dir.s3.contentstore}" />
    <property name="serviceAdapter" ref="store1.s3Adapter"/>
    <property name="nodeService" ref="nodeService" />
    <property name="defaultRootDir" value="${dir.s3.contentstore}" />

    <!-- Force the contentStore to use the prefix, otherwise the files would end up in the root of bucket -->
    <property name="useContentRootInPath" value="${s3.useContentRootInPath}"/>
    <property name="objNameSuffix" value="${connector.s3.objectNameSuffix}" />
    <property name="objNamePrefix" value="${connector.s3.objectNamePrefix}" />
    <property name="storeProtocol" value="${connector.s3.storeProtocol}"/>
    <!-- if true put all files into tenant root folder ! -->
    <property name="flatRoot" value="${s3.flatRoot}" />
</bean>

<!-- [End] Store 1 -->
```

**Store selector**

```xml
<!-- [Start] Store Selector -->

<!-- Override the selector to add in the S3Connector stores -->
<bean id="storeSelectorContentStore" parent="storeSelectorContentStoreBase">
    <property name="defaultStoreName">
        <value>default</value>
    </property>
    <property name="storesByName">
        <map>
            <entry key="default">
                <ref bean="store1.s3ContentStore"/>
            </entry>
            <entry key="s3ContentStore2">
                <ref bean="store2.s3ContentStore"/>
            </entry>
        </map>
    </property>
</bean>

<!-- Overwrite the store constraint with a no op constraint for now-->
<bean id="storeSelectorContentStore.constraint" class="org.alfresco.repo.dictionary.constraint.NoOpConstraint" init-method="initialize" >
    <property name="shortName">
        <value>defaultStoreSelector</value>
    </property>
    <property name="registry">
        <ref bean="cm:constraintRegistry" />
    </property>
</bean>

<!-- [End] Store Selector -->
```

**Caching content store**

The caching content store is defined over the content store selector so that we have one cache for all stores and 
makes the sample easier to extend when adding more stores.

```xml
<bean id="cachingContentStore"
class="org.alfresco.repo.content.caching.CachingContentStore"
init-method="init">
<property name="backingStore" ref="storeSelectorContentStore"/>
<property name="cache" ref="contentCache"/>
<property name="cacheOnInbound" value="true"/>
<property name="quota" ref="standardQuotaManager"/>
</bean>

<bean id="contentStoresToClean" class="java.util.ArrayList" >
    <constructor-arg>
        <list>
            <ref bean="cachingContentStore"/>
        </list>
    </constructor-arg>
</bean>
```

**s3-mb-contentstore.properties.sample**

This provides the subsystem properties where the `S3MultipleBuckets` subsystem declares default values for all the 
properties it requires.

See the Alfresco Content Services documentation on [Subsystem properties]({% link content-services/latest/config/subsystems.md %}#subsystem-properties) for more info.

**Deleted content store support provided by the repository vs. managed by S3 capabilities**

See [S3 Connector deleted content store](#enabledeletedcontentstore) for more info.

### Adding a new S3 store to the S3MultipleBuckets subsystem

These steps describe how to add a new S3 store starting from the `S3MultipleBuckets` subsystem sample.

1.  Locate the file `s3-mb-contentstore-context.xml` in folder:

    ```text
    $CATALINA_HOME/shared/classes/alfresco/extension/subsystems/ContentStore/S3MultipleBuckets/S3MultipleBuckets
    ```

2.  Duplicate the **Store 2** section, and replace `store2.` with `store3.`

    ```xml
    <bean id="store2.s3Adapter" class="org.alfresco.integrations.connector.AmazonS3ServiceAdapter" init-method="init">
        <property name="accessKey" value="${connector.s3.store2.accessKey}" />
        <property name="secretKey" value="${connector.s3.store2.secretKey}" />
        <property name="bucketName" value="${connector.s3.store2.bucketName}" />
        <property name="bucketRegion" value="${connector.s3.store2.bucketRegion}" />
        <property name="encryption" value="${connector.s3.store2.encryption}" />
        <property name="abortIncompleteMultipartUploadDays" value="${connector.s3.store2.abortIncompleteMultipartUploadDays}" />
        <property name="autoLowerCaseBucketName" value="${s3.store2.autoLowerCaseBucketName}" />
        <property name="awsKmsKeyId" value="${connector.s3.store2.awsKmsKeyId}" />
        <property name="endpoint" value="${connector.s3.store2.endpoint}" />
        <property name="clientConfiguration" ref="s3ClientConfiguration"/>
        
        <property name="tagName" value="${connector.s3.store2.tagName}" />
        <property name="tagValue" value="${connector.s3.store2.tagValue}" />
    </bean>
        
    <bean id="store2.s3ContentStore" class="org.alfresco.integrations.connector.TenantS3ContentStore" depends-on="store2.s3Adapter">
        <property name="useTenantDomainInPath" value="${s3.store2.useTenantDomainInPath}" />
        <property name="contentRoot" value="${dir.s3.contentstore}" />
        <property name="serviceAdapter" ref="store2.s3Adapter"/>
        <property name="nodeService" ref="nodeService" />
        <property name="defaultRootDir" value="${dir.s3.contentstore}" />
    
        <!-- Force the contentStore to use the prefix, otherwise the files would end up in the root of bucket -->
        <property name="useContentRootInPath" value="${s3.store2.useContentRootInPath}"/>
        <property name="objNameSuffix" value="${connector.s3.store2.objectNameSuffix}" />
        <property name="objNamePrefix" value="${connector.s3.store2.objectNamePrefix}" />
        <property name="storeProtocol" value="${connector.s3.store2.storeProtocol}"/>
        <!-- if true put all files into tenant root folder ! -->
        <property name="flatRoot" value="${s3.flatRoot}" />
    </bean>
    ```

3.  Add the new store to the Store Selector Content Store.

    For example:

    ```xml
    <entry key="s3ContentStore3">
        <ref bean="store3.s3ContentStore"/>
    </entry>
    ```

4.  Locate the file `s3-mb-contentstore.properties` in folder:

    ```text
    $CATALINA_HOME/shared/classes/alfresco/extension/subsystems/ContentStore/S3MultipleBuckets/S3MultipleBuckets
    ```

5.  Duplicate the **Store 2** section, and replace the content as described in the sub-steps below:

    ```text
    connector.s3.store2.accessKey=${connector.s3.accessKey}
    connector.s3.store2.secretKey=${connector.s3.secretKey}
    connector.s3.store2.bucketName=
    connector.s3.store2.bucketRegion=
    
    connector.s3.store2.encryption=${connector.s3.encryption}
    connector.s3.store2.awsKmsKeyId=
    
    connector.s3.store2.endpoint=
    
    connector.s3.store2.abortIncompleteMultipartUploadDays=${connector.s3.abortIncompleteMultipartUploadDays}
    s3.store2.autoLowerCaseBucketName=${s3.autoLowerCaseBucketName}
    
    s3.store2.useTenantDomainInPath=${s3.useTenantDomainInPath}
    s3.store2.useContentRootInPath=${s3.useContentRootInPath}
    
    connector.s3.store2.objectNamePrefix=
    connector.s3.store2.objectNameSuffix=
    connector.s3.store2.storeProtocol=s3v2
    connector.s3.store2.tagName=
    connector.s3.store2.tagValue=
    ```

    1.  Replace `connector.s3.store2` with `connector.s3.store3`.

    2.  Replace `s3.store2` with `s3.store3`.

### Advanced customization for the S3MultipleBuckets subsystem {#advancedconfigmultibucket}

These steps describe how to enhance the `S3MultipleBuckets` subsystem sample by adding specific configuration for each S3 store.

By default, the `Common configuration` section in `s3-mb-contentstore-context.xml` defines the client configuration and 
retry policy shared by all stores. You can duplicate this section in case you need a specific configuration for one of 
the stores.

1.  Locate the file `s3-mb-contentstore-context.xml`, for example:

    ```bash
    $CATALINA_HOME/shared/classes/alfresco/extension/subsystems/ContentStore/S3MultipleBuckets/S3MultipleBuckets/s3-mb-contentstore-context.xml
    ```

2.  Duplicate the **Common configuration** section:

    ```xml
    <bean id="s3RetryPolicy" class="com.amazonaws.retry.RetryPolicy">
        <constructor-arg ref="s3RetryCondition"/>
        <constructor-arg>
            <util:constant static-field="com.amazonaws.retry.PredefinedRetryPolicies.DEFAULT_BACKOFF_STRATEGY"/>
        </constructor-arg>
        <constructor-arg value="${connector.s3.maxErrorRetries}"/>
        <constructor-arg value="false" />
    </bean>
        
    <!-- Client configuration options such as proxy settings, user agent string, max retry attempts, etc. -->
    <bean id="s3ClientConfiguration" class="com.amazonaws.ClientConfiguration">
        <!-- Sets the retry policy upon failed requests. -->
        <property name="retryPolicy" ref="s3RetryPolicy"/>
        <!-- Sets whether throttled retries should be used -->
        <property name="useThrottleRetries" value="true"/>
        <property name="requestTimeout" value="${connector.s3.store2.httpRequestTimeout}" />
    </bean>
    ```

3.  Add a specific store prefix (e.g. `store2.`) to the bean names and properties.

    For example:

    ```xml
    <bean id="store2.s3RetryPolicy" class="com.amazonaws.retry.RetryPolicy">
        <constructor-arg ref="s3RetryCondition"/>
        <constructor-arg>
            <util:constant static-field="com.amazonaws.retry.PredefinedRetryPolicies.DEFAULT_BACKOFF_STRATEGY"/>
        </constructor-arg>
        <constructor-arg value="${connector.s3.store2.maxErrorRetries}"/>
        <constructor-arg value="false" />
    </bean>
         
    <!-- Client configuration options such as proxy settings, user agent string, max retry attempts, etc. -->
    <bean id="store2.s3ClientConfiguration" class="com.amazonaws.ClientConfiguration">
        <!-- Sets the retry policy upon failed requests. -->
        <property name="retryPolicy" ref="store2.s3RetryPolicy"/>
        <!-- Sets whether throttled retries should be used -->
        <property name="useThrottleRetries" value="true"/>
        <property name="requestTimeout" value="${connector.s3.store2.httpRequestTimeout}" />
    </bean>
    ```

4.  Update the `s3ClientConfiguration` in `store2.s3Adapter`.

    For example:

    ```xml
    <property name="clientConfiguration" ref="store2.s3ClientConfiguration"/>
    ```

## Properties reference

The S3 Connector provides a number of properties on installation and for customizing your configuration.

This section describes what's changed in the properties configuration:

* New properties
* New properties that supersede older properties
* Properties deprecated in S3 Connector 3.1

### New properties

Here is a list of properties that were added in S3 Connector 4.0.

* `connector.s3.deletionTagInsteadOfDelete`

    Default value: `false`.

    When set to `true`, the content won't be deleted but tagged instead. This property also requires the `deletionTagName` and `deletionTagValue` properties to be populated, otherwise an error will appear when an object deletion is performed. This property allows you to tag content that needs to be deleted when there are no delete permissions, so the content can be found and deleted later. It also allows you to define your own custom lifecycle policies based on tags.

* `connector.s3.deletionTagName`

    Blank by default.

    This property defines a tag value to apply to the content that needs to be deleted. When the content is tagged it won't be deleted. This property also requires the `deletionTagValue` property to be populated and the `deletionTagInsteadOfDelete` property to be set to `true`.

    > **Note:** The name of the deletion tag needs to be carefully chosen to ensure it is not used anywhere else. If actual content is tagged with `deletionTagName` there is a risk that content will be removed in error.

    > **Note:** Use the AWS documentation Object key and metadata for your naming guidelines because the properties must respect the same restrictions as if they were added via the AWS Management Console.

* `connector.s3.deletionTagValue`

    Blank by default.

    This property defines a tag value to apply to the content that needs to be deleted. When the content is tagged it won't be deleted. This property also requires the `deletionTagName` property to be populated and the `deletionTagInsteadOfDelete` property to be set to `true`.

### New properties that supersede older properties

To help align the configuration properties across the Alfresco connectors (in particular between the S3 Connector and the Azure Connector), a number of new properties have been introduced, with the final purpose of replacing their older equivalents in time.

|New property|Defaults to old property|
|------------|------------------------|
|connector.s3.maxErrorRetries|${s3.maxErrorRetries}|
|connector.s3.httpRequestTimeout|${s3.httpRequestTimeout}|
|connector.s3.abortIncompleteMultipartUploadDays|${s3.abortIncompleteMultipartUploadDays}|
|connector.s3.bucketName|${s3.bucketName}|
|connector.s3.bucketRegion|${s3.bucketLocation}|
|connector.s3.endpoint|${s3.endpoint}|
|connector.s3.accessKey|${s3.accessKey}|
|connector.s3.secretKey|${s3.secretKey}|
|connector.s3.encryption|${s3.encryption}|
|connector.s3.awsKmsKeyId|${s3.awsKmsKeyId}|

>**Note:** The new configuration properties default to the equivalent older properties (i.e. properties without the "`connector.*`" prefix). This ensures that upgrades of the S3 Connector will not require configuration updates. **However, it is recommended that you use the newer properties.**

Until now, the S3 Connector would override and use `dir.contentstore` and `dir.contentstore.deleted` properties defined in the `repository.properties` file in Alfresco Content Services (for `fileContentStore` and `deletedContentStore`).

Starting from version 3.1, the S3 Connector provides out-of-the-box content store subsystems. The subsystem approach allows a more flexible use of the S3 content store, even in conjunction with existing content stores.

>**Important:** In this case, we should not override the properties mentioned in the deprecated and superseded sections with S3 specific values. Instead, new properties have been introduced to be used only by the S3 Connector:

* `dir.s3.contentstore` - defaults to `contentstore`

* `dir.s3.contentstore.deleted` - defaults to `contentstore.deleted`

* `dir.s3.contentstore`

    Directory name used within the S3 bucket for the contentstore. The default is `contentstore`.

* `dir.s3.contentstore.deleted`

    Directory name used within the S3 bucket for the deleted contentstore. The default is `contentstore.deleted`.

* `connector.s3.bucketName`

    The bucket name must be unique among all AWS users globally. If the bucket does not already exist, it will be created, but the name must not have already been taken by another user. If the bucket has an error, it will be reported in the `alfresco.log` file.

* `connector.s3.bucketRegion`

    The location where the new S3 bucket should be created if it doesn't exist.

    For a list of available AWS Regions, see Regions and Endpoints in the AWS General Reference. The default region is US East (N. Virginia) - i.e. `us-east-1`.

* `connector.s3.endpoint`

    This is blank by default, but it can be used to add a custom endpoint, for example `connector.s3.endpoint=s3.us-gov-west-1.amazonaws.com`.

* `connector.s3.maxErrorRetries`

    The maximum number of attempts to retry reads or writes to the S3 bucket in case of failed transfers. The default is `3`.

    This configuration uses throttling retries. See [Retry Throttling](https://aws.amazon.com/blogs/developer/introducing-retry-throttling/) for more details.

* `connector.s3.abortIncompleteMultipartUploadDays`

    The minimum number of days that AWS S3 should keep the incomplete multipart upload parts before marking them for deletion. If the value is `0` then the abort is disabled. The default is `1`.

    If the bucket (identified by the value of `connector.s3.bucketName`) doesn't already exist, then we create the bucket and a global lifecycle rule to enforce the abort and deletion of incomplete uploads after the specified number of days. When an object reaches the end of its lifetime, Amazon S3 queues it for removal and removes it asynchronously.

    >**Note:** There may be a delay between the expiration date and the date on which AWS S3 removes an object.

* `connector.s3.encryption`

    Encryption to be applied for content stored in AWS S3. Two options are supported for managing encryption keys: AES256 and KMS. The default value on installation is `AES256`.

* `connector.s3.awsKmsKeyId`

    Indicates the key alias or ARN to be used for KMS encryption.

    For more details see [create a key using KMS key material origin](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html) or by [importing key material in AWS Key Management Service](https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html).

    If no value is provided, the default master key attached to your account is used. See [Protecting Data Using Server-Side Encryption with AWS KMS-Managed Keys (SSE-KMS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html).

* `connector.s3.accessKey`

    Required to identify the AWS account and can be obtained from the AWS Management Console. See [AWS Credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys) for access details. This property is not required if you plan to use [IAM roles](#configiam).

* `connector.s3.secretKey`

    Required to identify the AWS account and can be obtained from the AWS Management Console. See [AWS Credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys) for access details. This property is not required if you plan to use [IAM roles](#configiam).

### Properties deprecated in S3 Connector 3.1

The following properties were deprecated in S3 Connector 3.1, and should no longer be used as they'll be removed in a future release.

* `s3.useContentRootInPath`

    The default is `false`. When set to `true`, Alfresco Content Services won't start, and you'll see an error:

    ```text
    The V1 storage protocol s3:// has been deprecated since version 2.0 of this connector 
    and has been removed. This version no longer supports  s3.useContentRootInPath
    parameter being set to true. If you need to partition the objects in your bucket, we 
    recommend either using tags or the new connector.s3.objectNamePrefix option.
    ```

    Check [Replicating `s3.useContentRootInPath` behavior](#S3ContentStore) for details of how to replicate the old behavior of the `s3.useContentRootInPath` option through new configuration properties.

* `s3.useTenantDomainInPath`

    Defines whether the tenant name is used in the S3 path. The default is `false`. When set to either `true` or `false`, you'll see a warning specifying that multi-tenancy is no longer supported:

    ```text
    Multi-tenancy is no longer supported
    ```

    In spite of the warning, the behavior of the S3 Connector hasn't changed in relation to this property. However, only *content store* beans of type `org.alfresco.integrations.connector.TenantS3ContentStore` actually contain logic that can interpret this property. (In the S3 Connector default Spring configuration, there's currently only one such bean: `tenantS3ContentStore`).

* `s3.autoLowerCaseBucketName`

    The default is `false`. When set to either `true` or `false`, you'll see a warning:

    ```text
    The property s3.autoLowerCaseBucketName is no longer supported
    ```

    In spite of the warning, the S3 Connector behavior hasn't changed yet.

* `s3.flatRoot`

    Defines whether all content items should be stored in the same single directory in the bucket, otherwise the standard date-based hierarchy is used. The default is `true`. When set to `false`, you'll see a warning:

    ```text
    The property flatRoot is no longer supported, is highly discouraged, and will be 
    removed with the next release.
    ```

    In spite of the warning, the configuration is still evaluated and followed (i.e. no behavior changes yet).

## Properties behavior changes

The newly added configuration options and code changes in S3 Connector 3.1 are backwards compatible with older 
content created or uploaded by older versions of the S3 Connector. Regardless of the old `contentURL` and S3 object path, 
the existing content should still be readable by the new S3 Connector.

### S3ContentStore

**Deprecated properties and old behavior**

|s3.useContentRootInPath|dir.contentstore|Alfresco ContentURL (DB)|S3 path|
|-----------------------|----------------|--------------------------|-------|
|false|contentstore|s3v2://{uuid}.bin|{uuid}.bin|
|true|contentstore|s3://{uuid}.bin|contentstore/{uuid}.bin|

**New properties and behavior**

|connector.s3.objectNamePrefix|connector.s3.objectNameSuffix|connector.s3.storeProtocol|Alfresco ContentURL (DB)|S3 path|
|-----------------------------|-----------------------------|--------------------------|--------------------------|-------|
|"" (i.e. blank)|"" (i.e. blank)|s3v2|s3v2://{uuid}.bin|{uuid}.bin|
|"" (i.e. blank)|.bar|s3v2|s3v2://{uuid}.bin|{uuid}.bin.bar|
|foo/|.bar|s3v2|s3v2://{uuid}.bin|foo/{uuid}.bin.bar|
|foo/|.bar|s3blue|s3blue://{uuid}.bin|foo/{uuid}.bin.bar|

**Replicating s3.useContentRootInPath behavior**

The default configuration in the new S3 Connector has the `connector.s3.objectNamePrefix` as *blank*. This is compatible 
with old deployments that had `s3.useContentRootInPath` as `false`, resulting in no contentroot/prefix directory in the S3 path.

For compatibility with old deployments (where `s3.useContentRootInPath` was `true`), the `connector.s3.objectNamePrefix` 
property should be configured with the `${dir.s3.contentstore}` value. This inherits the value from the `dir.s3.contentstore` property, and ensures that:

1.  Old content is still readable, as it currently is, without moving/renaming it in S3.
2.  New content is created in the same old `dir.s3.contentstore` directory as before the S3 upgrade.

### DeletedS3ContentStore

**Deprecated properties and old behavior**

|dir.contentstore.deleted|Alfresco ContentURL (DB|S3 path|
|------------------------|------------------------|-------|
|contentstore.deleted|s3://{uuid}.bin|contentstore.deleted/{uuid}.bin|

**New properties and behavior**

|connector.s3.deleted.objectNamePrefix|connector.s3.deleted.objectNameSuffix|connector.s3.storeProtocol|Alfresco ContentURL (DB)|S3 path|
|-------------------------------------|-------------------------------------|--------------------------|--------------------------|-------|
|"" (i.e. blank)|"" (i.e. blank)|s3v2|s3v2://{uuid}.bin|{uuid}.bin|
|foo/|.bar|s3v2|s3v2://{uuid}.bin|foo/{uuid}.bin.bar|
|foo/|.bar|s3red|s3red://{uuid}.bin|foo/{uuid}.bin.bar|
|contentstore.deleted|.bar|s3v2|s3v2://{uuid}.bin|contentstore.deleted/{uuid}.bin.bar|

To ensure backwards compatibility for the `DeletedS3ContentStore`, the default configuration sets the `connector.s3.deleted.objectNamePrefix` property value to inherit the `${dir.s3.contentstore.deleted}` property value. This matches the default Spring Configuration, which assumes that the content root should always be used in the S3 path for the `DeletedS3ContentStore`. It also ensures that content created by older S3 Connector versions is still compatible with the current implementation.

### Other properties that affect the Content URLs

Currently, the two other properties that can still affect the Alfresco Content URLs and the S3 paths are `s3.useTenantDomainInPath` and `s3.flatRoot`.

Assuming:

* `connector.s3.objectNamePrefix=foo/`
* `connector.s3.objectNameSuffix=.bar`
* `connector.s3.storeProtocol=s3v2`

we have the following situations:

|s3.useTenantDomainInPath|s3.flatRoot|Alfresco ContentURL (DB)|S3 path|
|------------------------|-----------|--------------------------|-------|
|false|true|s3v2://{uuid}.bin|foo/{uuid}.bin.bar|
|true|true|s3v2://{tenant}/{uuid}.bin|foo/{tenant}/{uuid}.bin.bar|
|false|false|s3v2://{year}/{month}/{day}/{hour}/{minute}/{uuid}.bin|foo/{year}/{month}/{day}/{hour}/{minute}/{uuid}.bin.bar|
|true|false|s3v2://{tenant}/{year}/{month}/{day}/{hour}/{minute}/{uuid}.bin|foo/{tenant}/{year}/{month}/{day}/{hour}/{minute}/{uuid}.bin.bar|

The `s3.flatRoot` property is currently evaluated by all types of S3 Content Stores (including the `DeletedS3ContentStore`).

The `s3.useTenantDomainInPath` is only evaluated by instances/beans of type `TenantS3ContentStore` (`S3ContentStore` subclass). 
The `S3ContentStore` configured in the default S3 Connector Spring configuration is of type `TenantS3ContentStore`, 
and supports this property (although the property itself is configured as `false` by default).
---
title: Install Content Connector for AWS S3
---

Use this information to install and configure the Content Connector for AWS S3 as an alternative content store.

Using an Alfresco Module Package (AMP), the connector supplies a new content store which replaces the default file 
system-based implementation for the standard and (optionally) the deleted content stores. 
The content store implementation is responsible for reading and writing content streams (i.e. files) using the S3 API, 
however, in order to improve performance a local Caching Content Store is used which uses the local disk to 
cache recently-used content items.

>**Note:** By default the module configures the caching content store to use a maximum of 50 GB of disk, with no limit on individual file sizes.

Starting from version 3.1, the S3 Connector module provides out of the box content store subsystems, which can easily be 
set up based on the most suitable configuration. The subsystem approach allows a more flexible use of the S3 content store, 
even in conjunction with existing content stores.

You have two options for installing the S3 Connector:

* [Installing the S3 Connector](#installing)
* [Installing the S3 Connector with S3MultipleBuckets subsystem](#installingmultibucket)

The steps for both options are very similar, but the second allows you to add `S3MultipleBuckets` as a third alternative 
for the S3 content store subsystem.

## Prerequisites

There are a number of software requirements for installing Content Connector for AWS S3.

### Alfresco requirements

* Alfresco Content Services.

### Java requirements

* OpenJDK 17.

### AWS related requirements

In order to use the S3 Connector, you will need an AWS account so that you can configure the S3 Connector successfully. This includes having an admin account to set up an S3 bucket, or have access to a bucket that's already set up.

>**Note:** The bucket name must be unique among all AWS users globally. See [S3 bucket restrictions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html) for more information on bucket naming.

### Summary of features

If you want to use the functionality introduced in S3 Connector 2.0, you can configure the following:

* For IAM roles integration, see [Configuring AWS Identity and Access Management]({% link aws-s3/latest/config/index.md %}#configiam).
* For KMS integration, see [Configuring AWS Key Management Service]({% link aws-s3/latest/config/index.md %}#configkeymgmt).

If you want to use the functionality introduced in S3 Connector 2.1, you can configure the following:

* For S3 Connector on-premises configuration, see [Configuring S3 Connector on-premises]({% link aws-s3/latest/config/index.md %}#onpremconfig).
* For AWS Storage Classes configuration, see [Configuring AWS Storage Classes]({% link aws-s3/latest/config/index.md %}#configstorageclass).

If you want to use the functionality introduced in S3 Connector 3.1, you can configure the following:

* For S3 Connector content store subsystems configuration, see [S3 Connector content store subsystems]({% link aws-s3/latest/config/index.md %}#content-store-subsystems).
* For S3MultipleBuckets subsystem configuration, see [Configuring multiple buckets using S3 Connector]({% link aws-s3/latest/config/index.md %}#multibucketconfig).
* For changes to the S3 Connector configuration, see [Properties reference]({% link aws-s3/latest/config/index.md %}#properties-reference) and [Properties behaviour changes]({% link aws-s3/latest/config/index.md %}#properties-behavior-changes).

## Installing

These steps describe how to install the Content Connector for AWS S3 to an instance of Alfresco Content Services.

The S3 Connector is packaged as an Alfresco Module Package (AMP) file.

>**Note:** Ensure that you don't start Alfresco Content Services before installing the S3 Connector AMP.

1.  Go to [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2.  Download the `alfresco-s3-connector-6.1.x.amp` file.

3.  Use the Module Management Tool (MMT) to install the AMP into the repository WAR (`alfresco.war`).

    For more information, see [Using the Module Management Tool (MMT)]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt) and [Installing an Alfresco Module Package]({% link content-services/latest/install/zip/amp.md %}).

4.  Check that the [configuration]({% link aws-s3/latest/config/index.md %}) is set up correctly for your environment.

    >**Note:** For a new clean installation, we recommend that you choose a pure S3 content store. See [S3 Connector content store subsystems]({% link aws-s3/latest/config/index.md %}#content-store-subsystems) and [Properties reference]({% link aws-s3/latest/config/index.md %}#properties-reference) for more details.

5.  Starting from version 3.1, the S3 Connector has the deleted content store disabled by default, since this feature is already present in Amazon's S3 service. For details on how to re-enable it, see [S3 Connector deleted content store]({% link aws-s3/latest/config/index.md %}#enabledeletedcontentstore).

6.  Start Alfresco Content Services.

## Installing with S3MultipleBuckets subsystem {#installingmultibucket}

These steps describe how to install the S3 Connector to an instance of Alfresco Content Services, and how to 
enable the `S3MultipleBuckets` subsystem sample.

The S3 Connector is packaged as an Alfresco Module Package (AMP) file.

>**Note:** Ensure that you don't start Alfresco Content Services before installing the S3 Connector AMP.

1.  Go to [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2.  Download the `alfresco-s3-connector-6.1.x.amp` file.

3.  Use the Module Management Tool (MMT) to install the AMP into the repository WAR (`alfresco.war`).

    For more information, see [Using the Module Management Tool (MMT)]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt) and [Installing an Alfresco Module Package]({% link content-services/latest/install/zip/amp.md %}).

4.  Unzip the `alfresco-s3-connector-6.1.x.amp` file.

5.  Copy the three sample files and rename them by removing the `.sample` extension.

    The sample files are located under:

    ```text
    alfresco-s3-connector-6.1.x.amp/config/alfresco/extension/...
    ```

    They need to be copied to the relevant paths under the following folder:

    ```text
    $CATALINA_HOME/shared/classes/alfresco/extension/...
    ```

    1.  Copy and rename `s3-multiple-buckets-context.xml.sample` to:

        ```text
        s3-multiple-buckets-context.xml
        ```

    2.  Copy and rename `subsystems/ContentStore/S3MultipleBuckets/S3MultipleBuckets/s3-mb-contentstore-context.xml.sample` to:

        ```text
        subsystems/ContentStore/S3MultipleBuckets/S3MultipleBuckets/s3-mb-contentstore-context.xml
        ```

    3.  Copy and rename `subsystems/ContentStore/S3MultipleBuckets/S3MultipleBuckets/s3-mb-contentstore.properties.sample` to:

        ```text
        subsystems/ContentStore/S3MultipleBuckets/S3MultipleBuckets/s3-mb-contentstore.properties
        ```

6.  Check that the configuration is set up correctly for your environment.

    1.  Check the S3 Connector properties for store 1 (for example, `connector.s3.*` or `s3.*`)

        See `s3-mb-contentstore.properties` for the complete list.

        The minimum properties required are:

        ```text
        -Dconnector.s3.accessKey=${AWS_ACCESS_KEY_ID}
        -Dconnector.s3.secretKey=${AWS_SECRET_ACCESS_KEY}
        -Dconnector.s3.bucketName=${S3_BUCKET_NAME}
        -Dconnector.s3.bucketRegion=${S3_BUCKET_REGION}
        ```

    2.  Check the S3 Connector properties for store 2 (for example, `connector.s3.store2.*` or `s3.store2.*`)

        See `s3-mb-contentstore.properties` for the complete list..

        The minimum properties required are:

        ```text
        -Dconnector.s3.store2.bucketName=${S3_BUCKET2_NAME}
        -Dconnector.s3.store2.bucketRegion=${S3_BUCKET_REGION}
        ```

    3.  Set S3 multiple buckets as the default file content store subsystem:

        ```text
        filecontentstore.subsystem.name=S3MultipleBuckets
        ```

7.  Check that any other [configuration]({% link aws-s3/latest/config/index.md %}) is set up correctly for your environment and specifically check the [multiple bucket config]({% link aws-s3/latest/config/index.md %}#multibucketconfig).

8.  Start Alfresco Content Services.
---
title: Supported platforms
---

The following are the supported platforms for the Content Connector for AWS S3 6.1:

| Version | Notes |
| ------- | ----- |
| Content Services 23.2.x |  |
---
title: Upgrade Content Connector for AWS S3
---

Use this information to upgrade the S3 Connector from a previous version for Tomcat-based deployments only.

1.  Stop the Alfresco Content Services server.

2.  Navigate to the root directory of your installation.

3.  Use the following command to check for the module you wish to delete:

    ```bash
    java -jar bin/alfresco-mmt.jar list tomcat/webapps/alfresco.war
    ```

    This displays a list of the installed modules. Make a note of the module ID of the module you wish to uninstall, for example, `org_alfresco_integrations_S3Connector`.

4.  Use the Module Management Tool (MMT) to uninstall the AMP from the repository WAR (`alfresco.war`). For example:

    ```bash
    java -jar bin/alfresco-mmt.jar uninstall org_alfresco_integrations_S3Connector 
     tomcat/webapps/alfresco.war
    ```

    For more information, see [Using the Module Management Tool (MMT)]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt) and [Uninstalling an Alfresco Module Package]({% link content-services/latest/install/zip/amp.md %}#uninstall-an-amp-file).

5.  Navigate to the `amps` directory.

6.  Delete any previously installed S3 Connector AMP.

7.  Copy the AMP file you downloaded during [installation]({% link aws-s3/latest/install/index.md %}#installing) to the `amps` directory.

8.  Use the Module Management Tool (MMT) to install the AMP into the repository WAR (`alfresco.war`).

    For more information, see [Using the Module Management Tool (MMT)]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt) and [Installing an Alfresco Module Package]({% link content-services/latest/install/zip/amp.md %}).

9.  Check that the [configuration]({% link aws-s3/latest/config/index.md %}) is set up correctly for your environment.

    >**Note:** To upgrade a system that never used the file system (i.e. on-premises installation without locally saved binaries), we recommend that you choose a pure S3 content store. See [S3 Connector content store subsystems]({% link aws-s3/latest/config/index.md %}#content-store-subsystems) and [Properties reference]({% link aws-s3/latest/config/index.md %}#properties-reference) for more details.

10. Starting from version 3.1, the S3 Connector has custom soft deletion disabled by default, since this feature is already present in Amazon's S3 service. For details on how to re-enable it, see [S3 Connector deleted content store]({% link aws-s3/latest/config/index.md %}#enabledeletedcontentstore).

11. Start the server.
---
title: Content Connector for AWS S3 FAQ
---

Here are the answers to some frequently asked questions about the S3 Connector.

## Does the S3 Connector support multipart upload?

The S3 Connector supports multipart uploads where files larger than 20MB are split. The file upload is attempted and retried up to 3 times, in case there are issues. The number of attempts to read and write to the S3 bucket is configurable (see `s3.maxErrorRetries`).

## Is the S3 Connector compatible with existing data stores where IAM is not used?

The use of IAMs is recommended best practice from AWS. Should you prefer not to leverage the IAM functionality, the S3 Connector remains compatible as long as the access key and secret key are provided in the `alfresco-global.properties` file. The S3 Connector will then use these credentials to connect to the S3 bucket.

## What is the default delete behaviour when using the S3 Connector with S3 versioning enabled?

AWS versioning-enabled buckets are completely transparent to Alfresco, so the standard delete activity should take place as defined in the node lifecycle. In summary this means:

* when a user deletes content, the store changes to the Archive Store - nothing happens to the content
* when a user deletes content from the Trashcan (or archive store), `alf_node.deleted=1` and `alf_content_url.orphantime` is set
* If the S3 deleted content store is enabled, the`ContentStoreCleaner` copies the content to the `.deleted` directory and removes the content (by default after 14 days)
* `NodeServiceCleanup` purges the remaining database information

## As a customer upgrading from a previous version to S3 Connector 3.x, should I remove the useTenantDomainPath property?

The `s3.useTenantDomainInPath` property is `false` by default, so any new content you create won't add the tenant domain to the S3 path. If you want to add the tenant domain back to the path, then set this property to `true`. Note that this doesn't provide the optimal path for high throughput reads and writes.

## Do I need to re-encrypt all content in an S3 bucket if I move to KMS?

No, content is encrypted with the S3 file itself, so content encrypted by a previous key will remain encrypted using that encryption. If you require the content to be re-encrypted, you will need to follow AWS recommended practices.

## Why do I require the S3 Connector when AWS S3 can be mounted as a file system?

You can mount S3 as a file system using a third party library, but is not recommended by AWS or supported by Alfresco due to the very poor performance.

## Does the S3 Connector work with the Alfresco Content Encryption module?

A number of customers have requested that the [Alfresco Content Encryption]({% link content-services/latest/admin/content-stores.md %}#encrypted-content-store) module should be able to be deployed in conjunction with AWS KMS encryption on the S3 Content Store. In this release, we have taken steps to make this possible and it should be supported in the next release of the S3 Connector.

## Is there any guidance to support cross-region replication when using KMS keys in S3?

If you require cross-region replication, then you will need to use the S3 Connector without KMS. AWS S3 does not currently provide support for cross-region replication with KMS enabled.

## Do I need to do anything, such as re-encrypt all content in an S3 bucket, if I want to make use of IAM and KMS?

You don't need to do anything. Any existing content is still encrypted as it was when initially uploaded. For example, if the content was encrypted with AES256 it will remain accessible and encrypted under AES256.

## Does the S3 Connector support Amazon S3 Glacier?

Starting from version 5.0, the S3 Connector includes support for Amazon S3 Glacier via REST APIs.
