---
title: Alfresco Intelligence Services
---

Alfresco Intelligence Services is an add-on module that adds AI capabilities to Alfresco Content Services and the Digital Workspace. It utilizes a number of Amazon AI Services (i.e. Amazon Transcribe, Amazon Comprehend, Amazon Rekognition, and Amazon Textract) as an additional AI Transform Engine. This documentation describes how to install, set up, and configure Intelligence Services.

The Intelligence Services module enables you to configure and use custom ML models (for Natural Language Processing), created in Amazon Web Services (AWS), to enrich content stored in Content Services and the Digital Workspace. This is done through an integration with the Amazon Comprehend Custom service. With this new release transcripts for audio and video files, including indexing and metadata generation are provided automatically and this content can then be searched easily. Personal Identification Information (PII) in documents can be detected and tagged automatically which provides easier privacy management including automatic detection of PII entities.

Other features introduced in previous versions include:

* Key-value pairs as metadata properties (v1.2)
  * Including the ability to map multiple keys into the same metadata property
  * Check boxes as metadata properties
* All raw lines of text as a metadata property (v1.2)
* [Amazon Comprehend Custom Entity Recognition](https://docs.aws.amazon.com/comprehend/latest/dg/custom-entity-recognition.html){:target="_blank"} support (v1.1)
* [Amazon Comprehend Custom Classification](https://docs.aws.amazon.com/comprehend/latest/dg/how-document-classification.html){:target="_blank"} support (v1.1)
* [Amazon Textract Custom Metadata Extraction](https://docs.aws.amazon.com/textract/latest/dg/how-it-works-analyzing.html){:target="_blank"} support (v1.1)
* Configurable **Request AI renditions** action (v1.1)
* [Amazon Comprehend](https://aws.amazon.com/comprehend/faqs/){:target="_blank"} support (v1.0)
* [Amazon Rekognition](https://aws.amazon.com/rekognition/faqs/){:target="_blank"} support (v1.0)
* [Amazon Textract](https://aws.amazon.com/textract/faqs/){:target="_blank"} support (v1.0)
* Enrichment of content metadata (v1.0)
* Easier access to insights from unstructured content (v1.0)

See [Intelligence Services architecture]({% link intelligence-services/latest/admin/index.md %}) for a general overview.
---
title: Administer Intelligence Services
---

This information provides an overview of Intelligence Services, and helps you to monitor and administer it.

## Intelligence Services architecture

This topic describes the key components of Intelligence Services, and the flow of information between the repository and these components.

### Components of the Intelligence Services module

The main components of the Intelligence Services are:

* **Content Repository (ACS)**: This is the repository where documents and other content resides. The repository produces and consumes events destined for the message broker (such as ActiveMQ or Amazon MQ). It also reads and writes documents to the shared file store. AI overrides for the content repository (via an AMP), Digital Workspace (using a configuration file), and Share (via an AMP) are required to work with the Intelligence Services module.
* **ActiveMQ**: This is the message broker (either a self-managed ActiveMQ instance or Amazon MQ), where the repository and the Transform Router send image transform requests and responses. These JSON-based messages are then passed to the Transform Router.
* **Transform Router**: The Transform Router allows simple (single-step) and pipeline (multi-step) transforms that are passed to the Transform Engines. The Transform Router (and the Transform Engines) run as independently scalable Docker containers. This requires an AI override to work with the Intelligence Services module.
* **Transform Engines**: The Transform Engines transform files referenced by the repository and retrieved from the shared file store. Here are some example transformations for each Transform Engine (this isn't an exhaustive list):
  * LibreOffice (e.g. docx to pdf)
  * ImageMagick (e.g. resize)
  * Alfresco PDF Renderer (e.g. pdf to png)
  * Tika (e.g. docx to plain text)
  * AI Transform Engine (e.g. extracts data from images, such as png, jpeg, gif & tiff, and text from various file types such as pdf, docx, xlsx, pptx, etc.). Note that Comprehend can't process images directly, so the rendition is produced by using multi-step transforms. For example, Textract gets the text from an image, that can then be processed by Comprehend. For a list of supported transformations, see `ai-pipeline-routes.json` (included in the Intelligence Services distribution zip). The data extracted by the AI Engine is saved as AI aspects in the original source file.
* **Shared File Store**: This is used as temporary storage for the original source file (stored by the repository), intermediate files for multi-step transforms, and the final transformed target file. The target file is retrieved by the repository after it's been processed by one or more of the Transform Engines.

The following diagram shows a simple representation of the Intelligence Services components:

![Simple architecture for Intelligence Services]({% link intelligence-services/images/ai-simple-arch.png %})

This shows an example implementation of how you can deploy into AWS, using a number of managed services:

* Amazon EKS - Elastic Container Service for Kubernetes
* Amazon MQ - Managed message broker service for [Apache ActiveMQ](https://activemq.apache.org/){:target="_blank"}
* Amazon EFS - Amazon Elastic File System

You can replace the AWS services (EKS, MQ, and EFS) with a self-managed Kubernetes cluster, ActiveMQ (configured with failover), and a shared file store, such as NFS.

### Integrated AWS Services

The Intelligence Services module integrates four different AWS services:

* [Amazon Comprehend](https://docs.aws.amazon.com/comprehend/latest/dg/comprehend-general.html){:target="_blank"} for text analysis
* [Amazon Rekognition](https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html){:target="_blank"} for image analysis
* [Amazon Textract](https://docs.aws.amazon.com/textract/latest/dg/what-is.html){:target="_blank"} for text detection and form analysis of fields (key-value pairs) including check boxes
* [Amazon Transcribe](https://aws.amazon.com/transcribe/){:target="_blank"} for transcribing text from video and audio files

Alfresco Intelligence Services requests renditions for all four services (Comprehend, Rekognition, Textract, and Transcribe), using the default configuration. However, the API processing calls only take place for the relevant AWS service. From the release of version 1.1, you can configure the requested renditions.

Before you can add these services to your deployment, some configuration is first required in AWS. The details are covered in the [installation guide]({% link intelligence-services/latest/install/index.md %}).

## Analysis using AWS services

The following sections summarize the key features provided by each AWS service. The details are covered in the [installation guide]({% link intelligence-services/latest/install/index.md %})

### Amazon Comprehend

Amazon Comprehend allows you to analyze text by using natural language processing (NLP) to extract insights from your content.

It develops insights by recognizing common elements in your content into a number of content types, such as:

* entities (e.g. people, places, locations)
* language

> **Note:** This release of Alfresco Intelligence Services supports English only.

#### Prerequisites (Comprehend)

The general prerequisites for using Amazon Comprehend are documented in [Getting Started with Amazon Comprehend](https://docs.aws.amazon.com/comprehend/latest/dg/getting-started.html){:target="_blank"}. Since the Transform Engine has to use asynchronous jobs for large text files, some additional setup is required to get the service working correctly. This is covered in the later configuration section.

#### Supported regions (Comprehend)

See the list of supported AWS regions where Amazon Comprehend is [available](https://docs.aws.amazon.com/general/latest/gr/rande.html){:target="_blank"}.

#### Limits (Comprehend)

Synchronous operations have a limit of 5KB (5000 bytes). The encoding of the content must be UTF-8. Note that Amazon Comprehend may store the analyzed content in order to continuously improve the quality of its analysis models.

To bypass the limit for synchronous calls, we use batch operations which analyze a set of up to 25 documents (maximum). Each individual document has the same limit of 5KB, which means that the Transform Engine is able to work synchronously with documents up to 25x5 = 125KB.

To process documents larger than 125KB, we use asynchronous operations that go via an S3 bucket setup for Intelligence Services and Comprehend.

See the AWS site for more details: [Guidelines and Quotas](https://docs.aws.amazon.com/comprehend/latest/dg/guidelines-and-limits.html){:target="_blank"}, [AWS service quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html#limits_amazon_comprehend){:target="_blank"}.

#### Configuration (Comprehend)

You'll need to create an AWS Identity and Access Management (IAM) role with the correct permissions to control access to AWS services and resources.

There's a setting for the level of confidence that Amazon Comprehend has in the accuracy of the extracted content. This is defined as the minimum confidence level and has a default value of 80%.

### Amazon Rekognition

Amazon Rekognition makes it easy to add image analysis to your applications.

This service can identify the following in images:

* objects (e.g. flower, tree, or table)
* events (e.g. a wedding, graduation, or birthday party)
* concepts (e.g. a landscape, evening, and nature)

#### Prerequisites (Rekognition)

The general prerequisites to use Amazon Rekognition are documented in [Getting Started with Amazon Rekognition](https://docs.aws.amazon.com/rekognition/latest/dg/getting-started.html){:target="_blank"}. The configuration is simpler that Amazon Comprehend as you don't need to use asynchronous operations.

#### Supported regions (Rekognition)

See the list of supported AWS regions where Amazon Rekognition is [available](https://docs.aws.amazon.com/general/latest/gr/rande.html){:target="_blank"}.

#### Limits (Rekognition)

There are a number of limits that relate to Amazon Rekognition:

* Amazon Rekognition supports the PNG and JPEG image formats. So the images provided as input to various API operations, such as `DetectLabels`, must be in one of the supported formats.
* Images up to 5 MB are passed directly as raw bytes. Images over 5 MB go via an S3 bucket setup for Intelligence Services and Rekognition. The maximum image size allowed by Rekognition is limited to 15 MB.
* The minimum image size is 80 pixels for both height and width.

See the AWS site for more details: [Limits in Amazon Rekognition](https://docs.aws.amazon.com/rekognition/latest/dg/limits.html){:target="_blank"}, [Amazon Rekognition service quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html#limits_rekognition){:target="_blank"}.

#### Configuration (Rekognition)

You'll need to create an AWS Identity and Access Management (IAM) role with the correct permissions to control access to AWS services and resources.

There's a setting for the level of confidence that Amazon Rekognition has in the accuracy of the extracted content. This is defined as the minimum confidence level and has a default value of 80%.

### Amazon Textract

Amazon Textract makes it easy to add text detection and analysis of your content to your applications.

This service can detect text in a variety of documents (such as financial reports, medical records, and tax forms). For documents with structured data, the following can be detected:

* Forms with their fields and values
* Tables with their cells

#### Prerequisites (Textract)

The general prerequisites to use Amazon Textract are documented in [Getting Started with Amazon Textract](https://docs.aws.amazon.com/textract/latest/dg/getting-started.html){:target="_blank"}.

#### Supported regions (Textract)

See the list of supported AWS regions where Amazon Textract is [available](https://docs.aws.amazon.com/general/latest/gr/rande.html){:target="_blank"}.

#### Limits (Textract)

There are a number of limits that relate to Amazon Textract:

* Amazon Textract synchronous operations (`DetectDocumentText` and `AnalyzeDocument`) support the PNG and JPEG image formats. The maximum document image (JPG/PNG) size is 5 MB.
* Asynchronous operations (`StartDocumentTextDetection`, `StartDocumentAnalysis`) also support the PDF file format. The maximum PDF file size is 500 MB, and a maximum of 3000 pages.
  * To process PDF documents, we use asynchronous operations that go via an S3 bucket setup for Intelligence Services and Textract.
  * The maximum number of concurrent jobs for all asynchronous operations is 1.

See the AWS site for more details on service limits: [Limits in Amazon Textract](https://docs.aws.amazon.com/textract/latest/dg/limits.html){:target="_blank"}.

#### Configuration (Textract)

You'll need to create an AWS Identity and Access Management (IAM) role with the correct permissions to control access to AWS services and resources.

There's a setting for the level of confidence that Amazon Textract has in the accuracy of the extracted content. This is defined as the minimum confidence level and has a default value of 80%.

### Amazon Transcribe

Amazon Transcribe makes it easy for you to generate speech to text from your video and audio files to your applications.

This service can be used to convert video and audio data into text files which can then be searched for key words or used as closed captions on your videos and audio files.

#### Prerequisites (Transcribe)

The general prerequisites to use Amazon Transcribe are documented in [Getting Started with Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/getting-started.html){:target="_blank"}.

#### Supported regions (Transcribe)

See the list of supported AWS regions where Amazon Transcribe is [available](https://docs.aws.amazon.com/general/latest/gr/rande.html){:target="_blank"}.

#### Limits (Transcribe)

See the AWS site for more details on service limits: [Limits in Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/limits-guidelines.html){:target="_blank"}.

#### Configuration (Transcribe)

You'll need to create an AWS Identity and Access Management (IAM) role with the correct permissions to control access to AWS services and resources.

See the AWS site for transcription accuracy information [Improving domain-specific transcription accuracy with custom language models
](https://docs.aws.amazon.com/transcribe/latest/dg/custom-language-models.html){:target="_blank"}.
---
title: Troubleshoot Intelligence Services
---

Use this information to help troubleshoot Intelligence Services.

Make sure that Alfresco Transform Service is working before testing Alfresco Intelligence Services. See [Troubleshoot Transform Service]({% link transform-service/latest/admin/index.md %}#troubleshoot-transform-services) for more.

## Why don't I see any extracted metadata (AI properties)?

Check that your configured rule adds the desired AI aspects to extract and **Requests AI renditions**.

* For Rekognition, you need to add the **AI Labels** aspect.
* For Comprehend, you need to add one or more of the other AI aspects (AI People, AI Organizations, etc.) or all nine of them, if desired.

## I've added AI aspects and requested AI renditions but I'm still not seeing any extracted AI data. Which logs can I refer to see if anything is failing?

First, check the Alfresco Transform Service is running for a document transform (e.g. docx to pdf). See [Troubleshoot Transform Service]({% link transform-service/latest/admin/index.md %}#troubleshoot-transform-services) for more.

Next, check the logs for each microservice (container) including the Transform Router and AI Transform Engine. You can also check ActiveMQ queues to see the Transform Requests / Replies.

## Why don't I see a Rekognition image analysis?

Check the service logs for the Transform Router and AI Transform Engine. You may see the following error:

```bash
Source File size or mime type is not within allowable limits
```

Here's a snippet from the logs:

```bash
aws-ai_1 | 2019-03-26 14:01:43.595 ERROR 1 --- [enerContainer-4] o.a.t.AbstractTransformerController :
 Failed to perform transform (Exception), sending TransformReply{requestId='5575d683-5a7e-476c-9c1c-14e071cbc85b',
 status=500, errorDetails='Failed at processing transformation - AIClientException: [AWS Rekognition Label Detection]
 Source file too large to perform operation on', sourceReference='b75a08b8-17b1-4612-ba65-5ecd582a23e0',
 targetReference='null', clientData='workspace://SpacesStore/67ff9be4-7596-4ddb-bead-929366262e2f aiLabels
 1337801886 mjackson 1553608903465 304 jpg json-ailabels', schema=1, internalContext=InternalContext{multiStep=null,
 attemptedRetries=0, currentSourceMediaType='image/jpeg', currentTargetMediaType='application/vnd.alfresco.ai.labels.v1+json',
 currentSourceSize=21202469, transformRequestOptions={maxLabels=1000, minConfidence=0.8, transform=TikaAuto,
 includeContents=false, notExtractBookmarksText=true, targetMimetype=text/plain, targetEncoding=UTF-8}}}
aws-ai_1 |
aws-ai_1 | org.alfresco.transformer.ai.exception.AIClientException: [AWS Rekognition Label Detection] Source file too large to
 perform operation on
aws-ai_1 | at org.alfresco.transformer.ai.client.AwsRekognitionLabelDetectionRequestFactory.createDetectLabelsRequest(
 AwsRekognitionLabelDetectionRequestFactory.java:88) ~[alfresco-ai-image-analysis-0.4.0.jar!/:na]
```

If the image file size is larger than 15 MB then it'll be skipped. See [Amazon Rekognition limits]({% link intelligence-services/latest/admin/index.md %}#amazon-rekognition) for more.

## Why don't I see a Comprehend text analysis?

Check the service logs for the Transform Router and AI Transform Engine.

If you see the request but not the response, then check if the text file is larger than 125 KB. If so, it may take some time for the asynchronous response. Check again after 5 to 15 minutes.

Verify that you have correctly configured the AWS Comprehend Role to allow the Comprehend service read/write access to the S3 bucket used to temporarily store source files and results.

See [Amazon Comprehend limits]({% link intelligence-services/latest/admin/index.md %}#amazon-comprehend) and [Role-Based Permissions Required for Asynchronous Operations](https://docs.aws.amazon.com/comprehend/latest/dg/access-control-managing-permissions.html#auth-role-permissions){:target="_blank"} for more.

## Why don't I see a Textract image / text analysis?

Check the service logs for the Transform Router and AI Transform Engine. You may see the following error:

```bash
Source File size or mime type is not within allowable limits
```

Here's a snippet from the logs:

```bash
aws-ai_1 | 2019-03-26 13:47:24.848 ERROR 1 --- [enerContainer-5] o.a.t.AbstractTransformerController :
 Failed to perform transform (Exception), sending TransformReply{requestId='5fda6718-27b0-4289-b968-88a6f3bc3fb8',
 status=500, errorDetails='Failed at processing transformation - AIApplicationParameterException: Source File size
 or mime type is not within allowable limits', sourceReference='d36c0d14-06fb-4648-b72a-439af16d7f12',
 targetReference='null', clientData='workspace://SpacesStore/26522de2-6aa5-400c-b670-130dccd010c5 aiTextract
 -1927981676 mjackson 1553607988261 244 png json-aitextract', schema=1, internalContext=InternalContext{multiStep=null,
 attemptedRetries=2, currentSourceMediaType='image/png', currentTargetMediaType='application/vnd.alfresco.ai.textract.v1+json',
 currentSourceSize=12398590, transformRequestOptions={minConfidence=0.8, timeout=910000, transform=TikaAuto,
 includeContents=false, notExtractBookmarksText=true, targetMimetype=text/plain, targetEncoding=UTF-8}}}
aws-ai_1 |
aws-ai_1 | org.alfresco.transformer.ai.exception.AIApplicationParameterException: Source File size or mime type is not
 within allowable limits
aws-ai_1 | at org.alfresco.transformer.ai.service.AwsTextractTransformer.transformInternal(AwsTextractTransformer.java:87)
 ~[alfresco-ai-image-text-analysis-0.4.0.jar!/:na]
```

If the image file size is larger than 5 MB then it'll be skipped. See [Amazon Textract limits]({% link intelligence-services/latest/admin/index.md %}#amazon-textract) for more.

## Why do I see an AWS error when I upload a test folder of test files (e.g. via drag and drop)?

```bash
com.amazonaws.services.textract.model.ProvisionedThroughputExceededException: Provisioned rate exceeded (Service: AmazonTextract;
 Status Code: 400; Error Code: ProvisionedThroughputExceededException; Request ID: fef613f2-2e96-4f03-afd9-936a22dbff36)
```

This is likely to be a limitation of the Textract limits. Check the rate limits in the [Amazon Textract documentation](https://docs.aws.amazon.com/textract/latest/dg/limits.html){:target="_blank"}.

## What file formats/media types can be passed to the AWS services for processing?

The following file types can be passed and processed by AWS services.

**Images** (jpg, png, gif, tiff) are processed by Rekognition and Textract:

* jpg & png are sent directly to Rekognition & Textract.
* gif is converted to jpg (by the Alfresco Transform Engines), and then sent to Rekognition & Textract.
* tiff is converted to gif, then converted to jpg (by the Alfresco Transform Engines), and then sent to Rekognition & Textract.

**Text** (txt) is processed by Comprehend

**Pdf** is processed by Comprehend & Textract:

* pdf is converted to txt (by the Alfresco Transform Engines), and then sent to Comprehend.
* pdf is also sent directly to Textract.

**Office docs** (word, excel, powerpoint & outlook msg) are processed by Comprehend & Textract:

* doc is converted to txt (by the Alfresco Transform Engines), and then sent to Comprehend.
* doc is also converted to pdf and then sent to Textract.

You'll find a summary of the Transform Router configuration properties in `ai-pipeline-routes.json`, which is included in the Intelligence Services distribution zip file.

## I'm getting a lot of inaccurate metadata, what can I do?

The current default on minimum confidence levels is set at 80%.

See [Configuring the minimum confidence level]({% link intelligence-services/latest/install/index.md %}#configure-minimum-confidence-level) for more.

## Which Amazon AI/ML APIs are used for processing?

For Comprehend, we use the Language Detection and Entity Recognition APIs. See the [Amazon Comprehend Features](https://aws.amazon.com/comprehend/features/){:target="_blank"} for more details.

For Rekognition, we use the Object and Scene Detection APIs. See the [Amazon Rekognition Features](https://aws.amazon.com/rekognition/image-features/){:target="_blank"} for more details.

For Textract, we use the Synchronous Operations APIs. See the [Amazon Textract Features](https://docs.aws.amazon.com/textract/latest/dg/how-it-works.html){:target="_blank"} for more details.

## Where can I get more information on the content data model for the AI rendition?

The data model is in a private GitHub project. Alfresco customers can request access to this project by logging a ticket with [Alfresco Support](https://support.alfresco.com/){:target="_blank"}.

## I might be having AWS credential errors, what can I check?

Check your AWS setup and configuration. This also appears in AI Transform Engine service log.

> **Note:** For security reasons, the AWS credentials in the logs are masked (i.e. only a few characters appear - similar to the AWS CLI).

## After starting Intelligence Services, and trying to request AI renditions, what AWS connection errors / exceptions might I see in the AI Transform Engine logs?

You may see one of the following errors:

```bash
* The security token included in the request is invalid
```

```bash
* The request signature we calculated does not match the signature you provided.
Check your AWS Secret Access Key and signing method
```

If you notice AWS connection errors for Rekognition, Comprehend and/or Textract, then check your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` carefully.

For example:

* A mistyped `AWS_ACCESS_KEY_ID` may cause an error such as "`The security token included in the request is invalid`".
* A mistyped `AWS_SECRET_ACCESS_KEY` may cause the error shown in the second example (above).

You may see other connection errors, for example, if neither `AWS_ACCESS_KEY_ID` nor `AWS_SECRET_ACCESS_KEY` has been set.

Also, if you're using Docker Compose, then you may find that setting or exporting environment variables overrides a local `.env` configuration file.

## What do I need to set up to access Amazon AI services: Comprehend, Rekognition & Textract?

See [Set up services in AWS]({% link intelligence-services/latest/install/index.md %}) for more.

## How do the Amazon AI services access the content to be processed?

For very small files, the AWS synchronous APIs are called. However, for many files (see limits above) we may need to call the AWS asynchronous APIs. In this case, you'll need to set up an S3 bucket for asynchronous AWS calls, such that the AWS services can read the files to be processed.

We recommend the following setup:

* Use a different bucket than the one used by Content Services (when using Alfresco Content Connector for AWS S3).
* Create an S3 bucket in the same region as the Amazon AI services.
* For Comprehend, you also need to enable Comprehend to have write access to your S3 bucket for returning the results. This can be done by setting up an IAM role.

See [Set up services in AWS]({% link intelligence-services/latest/install/index.md %}#set-up-services-in-aws) to configure AWS Identity and Access Management and the Amazon AI services.

## When is Amazon Elastic File System (EFS) used?

From the architecture diagram in the [Intelligence Services overview]({% link intelligence-services/latest/admin/index.md %}), the Shared File Store (SFS) provides a mechanism for Content Services to send source files to the Transform Engines and receive target files from the Transform Engines. This includes the new AI Transform Engine that's used to call the Amazon AI services. In order to scale SFS for performance and reliability, it must be able to access a shared volume storage, such as managed EFS or self-managed NFS.

## I'm concerned about data privacy of the content that's processed by AWS. Do I have any control around this?

The AWS data privacy policies state that authorized AWS employees will have access to your content. Review the following AWS pages:

* [Comprehend Data Privacy Policy](https://aws.amazon.com/comprehend/faqs/#Data_privacy){:target="_blank"}
* [Rekognition Data Privacy Policy](https://aws.amazon.com/rekognition/faqs/#Data_Privacy){:target="_blank"}
* [Textract Data Privacy Policy](https://aws.amazon.com/textract/faqs/#Data_Privacy){:target="_blank"}

For Comprehend, Rekognition, and Textract, you can speak directly with your Account Manager at AWS and ask that when your content is passed for processing, it won't be used and stored for the improvement and development of their algorithms.

## What can you tell me about the performance of Intelligence Services?

The performance of this module is mostly dependent on the limitations around processing times and rates for Comprehend, Rekognition, Textract, and less dependent on the Alfresco components. The architecture of the Alfresco components for Intelligence Services are easily scalable to support larger ingestion of content going to Amazon, and also coming back from Amazon. We have internal benchmarking data on the Transform Service which can be referenced, if more information is requested.

## What happens if I leave the 'Request AI renditions' input text field empty?

The default renditions are requested (i.e. `aiFeatures`, `aiLabels`, `aiTextract`, `aiSpeechToText`, `webvtt`, and `aiPiiEntities`).

## What happens if I specify only one default AI rendition?

If you specify only one default AI rendition, such as `aiFeatures`, the other five renditions (`aiLabels`, `aiTextract`, `aiSpeechToText`, `webvtt`, and `aiPiiEntities`) are ignored. This may be really useful for saving costs if other renditions aren't required.

## Do I need to pay for the Amazon Textract service in my AWS account?

In previous versions of Intelligence Services, you could configure a folder rule to request AI renditions. This means that you'd have to pay for any files that are analyzed by Textract, Rekognition and/or Comprehend (depending on the media types and default routes).

Starting from version 1.1, Intelligence Services allows you to explicitly configure the folder rule to request a specific AI rendition (or set of AI renditions). This means that you don't have to use Textract. Note that if you don't specify a rendition, Intelligence Services defaults back to the version 1.0 behavior.

## Do I need to pay for the Amazon S3 service in my AWS account?

The Amazon S3 service is mandatory and required to use the complete functionality of Intelligence Services.

Alfresco Content Connector for AWS S3 is not specifically required for Intelligence Services. However, it can be purchased to use as an alternative content store when deploying Content Services.
---
title: Custom configuration - Comprehend
---

Use this information to configure and deploy a custom AI recognizer and a custom AI classifier using Amazon Comprehend.

This guide takes you through the journey of configuring your Content Services instance to enrich the content with custom metadata detected with powerful state of the art AI algorithms.

Multiple custom entity recognizers and classifiers can be configured and used in Content Services simultaneously, on either the same or different folders, using a flexible configuration.

## Configuration flow

The following diagram shows a high-level representation of the configuration flow:

![Custom AI configuration flow]({% link intelligence-services/images/ai-config-flow.png %})

Follow the remaining sections in this guide to start setting up your custom models.

## Step 1: Train custom models

Use this information to train custom models to use with Intelligence Services.

### Train a Custom Entity Recognition model

In order to have a trained Custom Entity Recognition model, two major steps that must be done:

1. Gathering and preparing training data
2. Training the Amazon Comprehend Custom Entity Recognizer

These steps are described and maintained in the AWS site: [Training Custom Entity Recognizers](https://docs.aws.amazon.com/comprehend/latest/dg/training-recognizers.html){:target="_blank"}.

> **Note:** The **Recognizer ARN** will be available once the model is trained. This is needed later when configuring the repository.

### Train a Custom Classification model

In order to have a trained Custom Classification model, two major steps that must be done:

1. Gathering and preparing training data
2. Training the Amazon Comprehend Custom Classifier

These steps are described and maintained in the AWS site: [Training a Custom Classifier](https://docs.aws.amazon.com/comprehend/latest/dg/how-document-classification-training.html){:target="_blank"}.

> **Note:** The **Classifier ARN** will be available once the model is trained. This is needed later when configuring the repository.

## Step 2: Deploy and configure a custom model

<!-- This section is included in comprehend.md and textract.md -->
Use this information to deploy and configure a custom model for Intelligence Services.

Note that the implementation follows the same process for custom recognition or classification model types, but differs slightly for custom metadata extraction.

Before you can use a custom model with Intelligence Services, you'll need to define a new rendition in configuration files for the repository, Alfresco Share, and Alfresco Digital Workspace.

The process requires the configuration of a number of files that must be mounted in the Docker containers:

|    | Configuration file | Used by custom model / AWS service |
| -- | ------------------ | ---------------------------------- |
| Repository | custom-ai-content-model-context.xml | Comprehend, Textract |
| | customAIContentModel.xml | Comprehend, Textract |
| | custom-ai-renditions-definitions.json | Comprehend
| | customAIPropertyMapping.json | Comprehend, Textract
| | | |
| Share | share-config-custom.xml | Comprehend, Textract
| | bootstrap-custom-labels.properties | Comprehend
| | share-custom-slingshot-application-context.xml | Comprehend, Textract |
| | | |
| Digital Workspace | ai-view.extension.json| Comprehend, Textract, Transcribe |

These files are described in more detail in the remainder of this page.

## Step 3. Configure the repository to use a custom model

Use this information to configure the repository files needed for a custom model. The following files must be mounted in the Alfresco repository Docker container.

### Custom AI content model context

File name: `custom-ai-content-model-context.xml`

Mount location and example:

```bash
./custom-ai-content-model-context.xml:/usr/local/tomcat/shared/classes/alfresco/extension/custom-ai-content-model-context.xml
```

Content:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">

    <!-- Registration of new models -->
    <bean id="org.alfresco.acme.dictionaryBootstrap" parent="dictionaryModelBootstrap" depends-on="org.alfresco.ai.dictionaryBootstrap">
        <property name="models">
            <list>
                <value>alfresco/extension/customAIContentModel.xml</value>
            </list>
        </property>
    </bean>
</beans>
```

### Custom AI content model

File name: `customAIContentModel.xml`

Mount location and example:

```bash
./customAIContentModel.xml:/usr/local/tomcat/shared/classes/alfresco/extension/customAIContentModel.xml
```

Content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<model name="acme:contentModel" xmlns="http://www.alfresco.org/model/dictionary/1.0">

    <description>Custom Content Model for Artificial Intelligence extension</description>
    <version>1.0</version>

    <imports>
        <import uri="http://www.alfresco.org/model/content/1.0" prefix="cm" />
        <import uri="http://www.alfresco.org/model/dictionary/1.0" prefix="d" />
        <import uri="http://www.alfresco.org/model/site/1.0" prefix="st" />
        <import uri="http://www.alfresco.org/model/system/1.0" prefix="sys" />
        <import uri="http://www.alfresco.org/model/ai/1.0" prefix="ai"/>
    </imports>

    <namespaces>
        <namespace uri="http://acme.org" prefix="acme" />
    </namespaces>

    <aspects>
        <aspect name="acme:businesses">
            <title>AI Businesses</title>
            <parent>ai:features</parent>
            <properties>
                <property name="acme:business">
                    <title>Businesses</title>
                    <type>d:text</type>
                    <multiple>true</multiple>
                    <index enabled="true">
                        <tokenised>both</tokenised>
                        <facetable>true</facetable>
                    </index>
                </property>
            </properties>
        </aspect>

        <aspect name="acme:sports">
            <title>AI Sports</title>
            <parent>ai:features</parent>
            <properties>
                <property name="acme:sport">
                    <title>Sports</title>
                    <type>d:text</type>
                    <multiple>true</multiple>
                    <index enabled="true">
                        <tokenised>both</tokenised>
                        <facetable>true</facetable>
                    </index>
                </property>
            </properties>
        </aspect>

        <aspect name="acme:categories">
            <title>AI Categories</title>
            <parent>ai:classifier</parent>
            <properties>
                <property name="acme:category">
                    <title>AI Category</title>
                    <type>d:text</type>
                    <multiple>true</multiple>
                    <index enabled="true">
                        <tokenised>both</tokenised>
                        <facetable>true</facetable>
                    </index>
                </property>
            </properties>
        </aspect>
    </aspects>
</model>
```

### Custom AI rendition definitions

File name: `custom-ai-renditions-definitions.json`

Mount location and example:

```bash
./custom-ai-renditions-definitions.json:/usr/local/tomcat/shared/classes/alfresco/extension/transform/renditions/custom-ai-renditions-definitions.json
```

Content:

The following JSON snippet shows the configuration for three renditions for two custom entity recognizers and one custom classifier.

```json
{
  "renditions": [
    {
      "renditionName": "aiBusinessCustom",
      "targetMediaType": "application/vnd.alfresco.ai.features.v1+json",
      "options": [
        {"name": "endpointAwsComprehendEntityRecognizer", "value": "arn:aws:comprehend:<region-name>:<account-id>:entity-recognizer/<recognizer-name>"},
        {"name": "maxResults", "value": 1000},
        {"name": "minConfidence", "value": 0.8}
      ]
    },
    {
      "renditionName": "aiSportCustom",
      "targetMediaType": "application/vnd.alfresco.ai.features.v1+json",
      "options": [
        {"name": "endpointAwsComprehendEntityRecognizer", "value": "arn:aws:comprehend:<region-name>:<account-id>:entity-recognizer/<recognizer-name>"},
        {"name": "maxResults", "value": 1000},
        {"name": "minConfidence", "value": 0.8}
      ]
    },
    {
      "renditionName": "aiClassification",
      "targetMediaType": "application/vnd.alfresco.ai.classifiers.v1+json",
      "options": [
        {"name": "endpointAwsComprehendClassifier", "value": "arn:aws:comprehend:<region-name>:<account-id>:document-classifier/<classifier-name>"},
        {"name": "maxResults", "value": 1},
        {"name": "minConfidence", "value": 0.2}
      ]
    }
  ]
}
```

The rendition configuration for entity recognition and classification is slightly different:

* `renditionName` - the key/label for the rendition. This must be unique, as it must match the rendition names in the `customAIPropertyMapping.json` file. It's best to choose a name that's indicative of the recognizer/classifier used.
* `targetMediaType` - can be one of two options:
  * `application/vnd.alfresco.ai.features.v1+json` for entity recognizers
  * `application/vnd.alfresco.ai.classifiers.v1+json` for classifiers
* `maxResults` - the maximum number of results (entities/categories) that should be used in Content Services. It makes sense to use a large value when searching for entities in a document, and a very small value when trying to identify a category for an entire document
* `minConfidence` - the minimum confidence for a result (between 0 and 1). A lower value can be used when the maximum number of values is small (i.e. for classification).

### Custom AI property mapping

File name: `customAIPropertyMapping.json`

Mount location and example:

```bash
./customAIPropertyMapping.json:/usr/local/tomcat/customAIPropertyMapping.json
```

Content:

```json
{
  "featureToPropertyMapping": [
    {
      "aiBusinessCustom": [
        {
          "type": "BUSINESS",
          "aspect": "acme:businesses",
          "property": "acme:business"
        }
      ]
    },
    {
      "aiSportCustom": [
        {
          "type": "SPORT",
          "aspect": "acme:sports",
          "property": "acme:sport"
        }
      ]
    }
  ],
  "categoryToPropertyMapping": [
    {
      "aiClassification": {
        "aspect": "acme:categories",
        "property": "acme:category"
      }
    }
  ]
}
```

In the above JSON snippet:

* The rendition name (e.g. `aiBusiness`, `aiSport`, `aiClassification`) is used as a key (for both custom entity recognizers and custom classifiers).
* The aspect/property names must match the Content Services content model.
* For custom entity recognizers, the entity type (e.g. `BUSINESS`, `SPORT`) must match what's returned in the raw results.

### Alfresco Docker service definition (deployment)

```yaml
alfresco:
    image: alfresco/alfresco-content-services-with-amps-applied:x.y
    environment:
      JAVA_OPTS: "
        -Ddb.driver=org.postgresql.Driver
        -Ddb.username=alfresco
        -Ddb.password=alfresco
        -Ddb.url=jdbc:postgresql://postgres:5432/alfresco
        -Dsolr.host=solr6
        -Dsolr.port=8983
        -Dsolr.secureComms=none
        -Dsolr.base.url=/solr
        -Dindex.subsystem.name=solr6
        -Dshare.host=127.0.0.1
        -Dshare.port=8080
        -Dalfresco.host=localhost
        -Dalfresco.port=8080
        -Daos.baseUrlOverwrite=http://localhost:8080/alfresco/aos
        -Dmessaging.broker.url=\"failover:(nio://activemq:61616)?timeout=3000&jms.useCompression=true\"
        -Ddeployment.method=DOCKER_COMPOSE

        -Dtransform.service.enabled=true
        -Dtransform.service.url=http://transform-router:8095
        -Dsfs.url=http://shared-file-store:8099/

        -Dlocal.transform.service.enabled=true
        -DlocalTransform.pdfrenderer.url=http://alfresco-pdf-renderer:8090/
        -DlocalTransform.imagemagick.url=http://imagemagick:8090/
        -DlocalTransform.libreoffice.url=http://libreoffice:8090/
        -DlocalTransform.tika.url=http://tika:8090/
        -DlocalTransform.misc.url=http://misc:8090/

        -Dlegacy.transform.service.enabled=true
        -Dalfresco-pdf-renderer.url=http://alfresco-pdf-renderer:8090/
        -Djodconverter.url=http://libreoffice:8090/
        -Dimg.url=http://imagemagick:8090/
        -Dtika.url=http://tika:8090/
        -Dtransform.misc.url=http://misc:8090/

        -Dcsrf.filter.enabled=false
        -Xms1500m -Xmx1500m

        -Dai.transformation.customAIPropertyMapping.file.location=\"/usr/local/tomcat/customAIPropertyMapping.json\"
        "
    ports:
      - 5006:5006
    volumes:
      - alfresco-volume:/usr/local/tomcat/alf_data
      - ./customAIPropertyMapping.json:/usr/local/tomcat/customAIPropertyMapping.json
      - ./customAIContentModel.xml:/usr/local/tomcat/shared/classes/alfresco/extension/customAIContentModel.xml
      # DOC: file needs to end in -context.xml and to be in this location.
      # Details on (Deployment - App Server) -> https://docs.alfresco.com/content-services/latest/develop/repo-ext-points/content-model/#definedeploy)
      - ./custom-ai-content-model-context.xml:/usr/local/tomcat/shared/classes/alfresco/extension/custom-ai-content-model-context.xml
      - ./custom-ai-renditions-definitions.json:/usr/local/tomcat/shared/classes/alfresco/extension/transform/renditions/custom-ai-renditions-definitions.json
```

In the above `docker-compose` snippet:

* The `transform.service.enabled` property must be set to `true`;
* `ai.transformation.customAIPropertyMapping.file.location` must point to the location where the `customAIPropertyMapping.json` file is mounted;
* The custom AI configuration files must be mounted in the repository container at specific locations.

## Step 4. Configure Share and Digital Workspace to use a custom model

Use this information to configure the files needed by Share and Digital Workspace for a custom model.

### Share

The following files must be mounted in the Share Docker container.

#### 1. Custom AI labels

File name: `share-config-custom.xml`

Mount location and example:

```bash
./share-config-custom.xml:/usr/local/tomcat/shared/classes/alfresco/web-extension/share-config-custom-dev.xml
```

Content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<alfresco-config>
    <config evaluator="string-compare" condition="DocumentLibrary">
        <!-- Aspects that a user can see -->
        <aspects>
            <visible>
                <aspect name="acme:businesses"/>
                <aspect name="acme:sports"/>
                <aspect name="acme:categories"/>
            </visible>
        </aspects>
    </config>
</alfresco-config>
```

#### 2. Custom AI aspect configuration

File name: `bootstrap-custom-labels.properties`

Mount location and example:

```bash
./bootstrap-custom-labels.properties:/usr/local/tomcat/shared/classes/alfresco/web-extension/messages/bootstrap-custom-labels.properties
```

Content:

```bash
aspect.acme_businesses=AI Businesses
aspect.acme_sports=AI Sports
aspect.acme_categories=AI Categories
```

#### 3. Custom AI labels context

File name: `share-custom-slingshot-application-context.xml`

Mount location and example:

```bash
./share-custom-slingshot-application-context.xml:/usr/local/tomcat/shared/classes/alfresco/web-extension/custom-slingshot-application-context.xml
```

Content:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.springframework.org/schema/beans
                http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">

    <bean id="org.alfresco.acme.alfresco-ai-share.resources" class="org.springframework.extensions.surf.util.ResourceBundleBootstrapComponent">
        <property name="resourceBundles">
            <list>
                <value>alfresco/web-extension/messages/bootstrap-custom-labels</value>
            </list>
        </property>
    </bean>
</beans>
```

### Share - Docker service definition

In the `docker-compose` snippet, the custom AI configuration files must be mounted in the Share container at specific locations.

```yaml
share:
    image: quay.io/alfresco/alfresco-share-ai-transformers-module:1.5.x
    environment:
      REPO_HOST: "alfresco"
      REPO_PORT: "8080"
      JAVA_OPTS: "
        -Xms500m
        -Xmx500m
        -Dalfresco.host=localhost
        -Dalfresco.port=8080
        -Dalfresco.context=alfresco
        -Dalfresco.protocol=http
        "
    volumes:
      # DOC: configuring Share -> https://docs.alfresco.com/content-services/latest/develop/share-ext-points/share-config/)
      - ./share-config-custom.xml:/usr/local/tomcat/shared/classes/alfresco/web-extension/share-config-custom-dev.xml
      - ./bootstrap-custom-labels.properties:/usr/local/tomcat/shared/classes/alfresco/web-extension/messages/bootstrap-custom-labels.properties
      - ./share-custom-slingshot-application-context.xml:/usr/local/tomcat/shared/classes/alfresco/web-extension/custom-slingshot-application-context.xml
```

### Digital Workspace

The Digital Workspace configuration for custom AI requires modification of an existing configuration file (`ai-view.extension.json`). The JSON file is included in the Intelligence Services distribution zip. This is unlike the repository and Share configuration, where only new files are created and mounted in the containers.

#### App extension

File name: `ai-view.extension.json`

Mount location and example:

```bash
./ai-view.extension.json:/usr/share/nginx/html/assets/plugins/ai-view.extension.json
```

Content:

```json
[...]
"content-metadata-presets": [
  {
    "id": "app.content.metadata.custom",
    "custom": [
      {
        "id": "ai.metadata.features",
        "title": "AI Data",
        "items": [
          {
            "id": "acme:businesses",
            "aspect": "acme:businesses",
            "properties": "*"
          },
          {
            "id": "acme:sports",
            "aspect": "acme:sports",
            "properties": "*"
          },
          {
            "id": "acme:categories",
            "aspect": "acme:categories",
            "properties": "*"
          },
          [...]
        ]
      }
    ],
    [...]
  }
]
```

The above snippet adds the aspects in the earlier [Custom AI content model configuration]({% link intelligence-services/latest/config/comprehend.md %}#custom-ai-content-model) to the existing `"ai.metadata.features"` list of items in the `ai-view.extension.json` file.

The JSON path for the new items is `$.features.content-metadata-presets[:].custom[:].items`.

For more details on extending the features of Digital Workspace, see the Alfresco Content Application documentation: [Extending](https://alfresco-content-app.netlify.com/#/extending/){:target="_blank"}.

### Digital Workspace - Docker service definition

```yaml
  digital-workspace:
    image: quay.io/alfresco/alfresco-digital-workspace:2.8
    environment:
      BASE_PATH: ./
      APP_CONFIG_PLUGIN_AI_SERVICE: "true"
    volumes:
      - ./ai-view-extension.json:/usr/share/nginx/html/assets/plugins/ai-view-extension.json
```

In the above `docker-compose` snippet, the modified `ai-view-extension.json` configuration file must be mounted in the Digital Workspace container. The environment variable `APP_CONFIG_PLUGIN_AI_SERVICE:` when set to `true` allows the Digital Workspace to index and search by the content of the transcripted files and scanned images.
---
title: Configure Intelligence Services
---

Starting from version 1.1, Intelligence Services allows you to configure custom machine-learning (custom ML) models to enrich the content stored in Content Services. A custom ML model maps each model to metadata in your business documents. This provides a number of benefits:

* Content has metadata automatically applied, and can be categorized or classified based on its business context.
* Unstructured content can be searched and indexed by business context and easily discovered.
* Business rules and processes can automatically be triggered.

Using the Textract OCR solution from Amazon, you can extract plain text from images and PDF files, and then analyze the text. For example, for a given PDF or image, you'll get the raw text from the whole file, tables, forms (using key-value pairs), and check boxes. The extracted data is mapped to properties which are searchable.

## Configuration options

There are several options to configuring Intelligence Services.

* **Default configuration**

    This option allows you to customize the **Request AI renditions** action, so that it only calls the renditions that you wish to use. Use these steps if you don't plan to create a custom ML model.

* **Custom configuration**

Choose one or more of the following options to create custom ML models:

1. Custom entity recognition - configure and deploy a custom AI recognizer. This allows you to identify new entity types that aren't supported by one of the preset entity types.
2. Custom document classification - configure and deploy a custom AI classifier. This allows you to classify documents, for example as either an invoice, purchase order, contract, or whatever fits your business model.
3. Custom metadata extraction - configure and deploy a custom AI model. This allows you to map basic OCR detected text lines into multi-valued text fields, so they can viewed and searched.

You can still customize the **Request AI renditions** action, as in the default configuration.

> **Note:** It's recommended that you start developing one custom model at a time (i.e. either a recognizer or classifier), and test it thoroughly before adding another.

> **Note:** Metadata extraction from tables isn't supported.

## Default configuration

There are four steps to configuring the default (i.e. out-of-the-box) deployment of Intelligence Services: export your environment variables, add the AI Transform Engine to your deployment, override the Transform Router configuration, and override the Digital Workspace configuration.

> **Note:** Ensure that you've completed the [AWS setup]({% link intelligence-services/latest/install/index.md %}#set-up-services-in-aws) before continuing.

A number of environment variables allow you to specify the configuration options and credentials that are required to run the AI Transform Engine.

1. To configure these variables, you need to export your AWS credentials and other settings.

    For example:

    ```bash
    export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXXXXX
    export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
    export AWS_REGION="<region-name>"
    export AWS_S3_BUCKET="<s3-bucket-name>"
    export AWS_COMPREHEND_ROLE_ARN="arn:aws:iam::XXXXXXXXXXXX:role/ComprehendAsyncJobs"
    ```

    **Add the AI Transform Engine to an existing deployment**

2. To include the AI Transform Engine in your existing deployment, add the following configuration.

    Here's an example snippet from a Docker Compose file:

    ```yaml
    aws-ai:
        image: quay.io/alfresco/alfresco-ai-docker-engine:1.5.x
        environment:
            JAVA_OPTS: " -Xms256m -Xmx768m"
            # JAVA_OPTS: " -Xms256m -Xmx512m -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 "
            FILE_STORE_URL: "http://shared-file-store:8099/alfresco/api/-default-/private/sfs/versions/1/file"
            AWS_ACCESS_KEY: "${AWS_ACCESS_KEY_ID}"
            AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
            AWS_REGION: "${AWS_REGION}"
            AWS_S3_BUCKET: "${AWS_S3_BUCKET}"
            AWS_COMPREHEND_ROLE_ARN: "${AWS_COMPREHEND_ROLE_ARN}"
            ACTIVEMQ_URL: "nio://activemq:61616"
        ports:
            - 5005:5005
            - 8094:8090
    ```

    **Override the Transform Router**

3. Add the following configuration to override the Transform Router in your deployment.

    This adds extra environment variables in the router configuration so it's aware of the new AI Transform Engine.

    Here's an example snippet from a Docker Compose file:

    ```yaml
    transform-router:
        image: quay.io/alfresco/alfresco-transform-router:1.5.x
        environment:
            JAVA_OPTS: " -Xms256m -Xmx512m"
            FILE_STORE_URL: "http://shared-file-store:8099/alfresco/api/-default-/private/sfs/versions/1/file"
            ACTIVEMQ_URL: "nio://activemq:61616"
            IMAGEMAGICK_URL: "http://imagemagick:8090"
            PDF_RENDERER_URL: "http://alfresco-pdf-renderer:8090"
            LIBREOFFICE_URL: "http://libreoffice:8090"
            TIKA_URL: "http://tika:8090"
            TRANSFORMER_URL_AWS_AI: "http://aws-ai:8090"
            TRANSFORMER_QUEUE_AWS_AI: "org.alfresco.transform.engine.ai-aws.acs"
            TRANSFORMER_ROUTES_ADDITIONAL_AI: "/ai-pipeline-routes.json"
        links:
            - activemq
        volumes:
        - ./ai-pipeline-routes.json:/ai-pipeline-routes.json
    ```

    > **Note:** The transform routes listed in `ai-pipeline-routes.json` define the supported transformations for all Transform Engines. This file is included in the Intelligence Services distribution zip.

    **Override the Digital Workspace configuration**

4. Add the following configuration to override the settings for Digital Workspace in your deployment.

    ```yaml
    digital-workspace:
        image: quay.io/alfresco/alfresco-digital-workspace:2.8
        environment:
        BASE_PATH: ./
        APP_CONFIG_PLUGIN_AI_SERVICE: "true"
        volumes:
        - ./ai-view-extension.json:/usr/share/nginx/html/assets/plugins/ai-view-extension.json
    ```

    > **Note:** The Digital Workspace configuration file, `ai-view-extension.json`, is also included in the Intelligence Services distribution zip.

    For more details on extending the features of Digital Workspace, see the Alfresco Content Application documentation: [Extending](https://alfresco-content-app.netlify.com/#/extending/){:target="_blank"}.

You're now ready to start Content Services.
---
title: Custom configuration - Textract
---

Use this information to configure and deploy a custom AI model using Amazon Textract.

This guide takes you through the journey of configuring your Content Services instance to enrich the content with custom metadata detected with powerful state of the art AI algorithms.

Multiple custom entity model can be configured and used in Content Services simultaneously, on either the same or different folders, using a flexible configuration.

Follow the remaining sections to start setting up your custom Textract models.

## Step 1: Define custom Textract models

There are two parts to creating a Custom Metadata Extraction model:

* Configuring custom mapping for Textract metadata extraction from forms (as key-value pairs)
* (Optional) Mapping basic OCR detected text lines into a multi-valued text field to enable viewing and searching (using the out-of-box `ai:textLines` aspect)

### Custom mapping

As a developer or administrator, you can define a custom AI content model to enable mapping of extracted text values into Content Services content model properties (or metadata). You can define one or more aspects, each with one or more properties, where each aspect can extend a new "out-of-the-box" parent aspect (`ai:textract`). Note that this is similar to the Comprehend parent aspect, `ai:features`.

* The properties may be single-valued or multi-valued.
* Typically, extracted text values map to properties of data type `d:text`.
* Check boxes typically map to `d:boolean`.

However, in theory, the property may be of any data type to which the extracted value can be mapped without a constraint violation.

You'll need to define the custom Textract metadata configuration in JSON format. This should allow one or more specific key-value pairs to map to the Content Services content model properties. Different aspects may be configured for different document types. The configuration can be statically bootstrapped by the repository on startup.

> **Note:** Textract tables and cells are currently out-of-scope.

### Form extraction (key-value pairs)

Here's an example of the metadata extracted from a form:

![Example of the metadata extracted from a form]({% link intelligence-services/images/textract-form.png %})

#### Key matching

Multiple types of key matching are supported:

* default matching:
  * ignores case
  * ignores non-alphanumeric prefixes and suffixes
  * ignores whitespace

  > **Note:** The default matching would have to process not just the keys received in the Textract JSON response, but also the keys defined in the property mapping configuration files.

* exact matching
* regular expression (regex) matching

The key matching type can be defined for each key in the property mapping configuration file. If omitted, the default matching is used.

#### Multiple keys mapped to one property

Key matching implies a number of different keys may map to the same property. Hence, you may define exact match keys that map to the same property.

When the same key matches multiple times or a number of different matching keys map to the same property then:

* for a *multi-value property* - each *unique* value is stored
* for a *single-value* property - the most confident match of a key-value-set is stored, along with the INFO log messages that some values were skipped/ignored.

#### One key mapped to multiple properties

Due to the supported matching types, keys may match and overlap such that they map to different properties. Similarly, we allow the mapping of one key to multiple properties (by multiple aspects).

When the same matching key maps two different properties, we map to both properties, and log an INFO message with the context.

#### Confidence

The minimum confidence level is checked when mapping each matching element (key-value pair). This uses a new global (system-wide) property:

```bash
ai.transformation.aiTextract.keyValueSet.minConfidence
```

This property has a default: 0.7 (i.e. 70%) unless overridden for a specific key/value mapping.

You can add an optional `confidence` field for each key in the property mapping configuration file to override the global configuration. See example in [Custom AI property mapping]({% link intelligence-services/latest/config/textract.md %}#custom-ai-property-mapping).

#### Custom aspects

An aspect can contain multiple properties (multiple keys). Different aspects can be defined depending on the documents that need to be processed. Their keys might overlap.

#### Log messages

1. If a mapped key value fails to convert the extracted text string to a different target data type (for example, due to constraint violation) it'll be skipped with a one-line INFO log message (including context, for example, nodeId, property name and value).
2. If the same key matches multiple times, or multiple different matching keys map to the same *single-value* property then we store the "most confident match of a key-value-set", and specify in an INFO log message that some values were skipped/ignored.
3. If the same matching key maps two different properties, we map to both properties and state the behavior in an INFO log message.

### Check boxes

Check boxes detected within forms (Textract `selectables` as key-value pairs) are supported. In this case, you can choose to map to `d:boolean` (i.e. whether selected or not) or `d:text`. For `d:text`, the selected status value is stored as returned by Textract, i.e. `SELECTED` or `NOT_SELECTED`.

Here's an example of the metadata extracted from a form that shows both options mixed together in a single aspect:

![Example of the metadata extracted from a form using checkboxes]({% link intelligence-services/images/textract-form-checkbox.png %})

### Raw text extraction

There's an out-of-box `AI Text Lines` aspect (with a `d:text` property type) that an end-user can optionally use when configuring a rule. This enables a non-custom way to extract the Textract "raw text", so that OCR'd text (above the minimum confidence for lines) can be viewed as metadata, as well as being indexed and searchable.

Out-of-the-box, the raw text lines are stored in a multi-valued text property (which appear comma-separated in Alfresco Digital Workspace).

The `ai-content-model.xml` contains an aspect for the raw text. This is included by default in the Intelligence Services AMP:

```xml
<aspect name="ai:textLines">
    <title>AI Text Lines</title>
    <parent>ai:textract</parent>
    <properties>
        <property name="schema:textLines">
            <title>Text</title>
            <type>d:text</type>
            <multiple>true</multiple>
            <index enabled="true">
                <tokenised>both</tokenised>
                <facetable>true</facetable>
            </index>
        </property>
    </properties>
</aspect>
```

## Step 2: Deploy and configure a custom model

<!-- This section is included in comprehend.md and textract.md -->
Use this information to deploy and configure a custom model for Intelligence Services.

Note that the implementation follows the same process for custom recognition or classification model types, but differs slightly for custom metadata extraction.

Before you can use a custom model with Intelligence Services, you'll need to define a new rendition in configuration files for the repository, Alfresco Share, and Alfresco Digital Workspace.

The process requires the configuration of a number of files that must be mounted in the Docker containers:

|    | Configuration file | Used by custom model / AWS service |
| -- | ------------------ | ---------------------------------- |
| Repository | custom-ai-content-model-context.xml | Comprehend, Textract |
| | customAIContentModel.xml | Comprehend, Textract |
| | custom-ai-renditions-definitions.json | Comprehend
| | customAIPropertyMapping.json | Comprehend, Textract
| | | |
| Share | share-config-custom.xml | Comprehend, Textract
| | bootstrap-custom-labels.properties | Comprehend
| | share-custom-slingshot-application-context.xml | Comprehend, Textract |
| | | |
| Digital Workspace | ai-view.extension.json| Comprehend, Textract|

These files are described in more detail in the remainder of this page.

## Step 3: Configure the repository

Use this information to configure the repository files needed for a custom Textract model.

The following files must be mounted in the repository Docker container.

### Custom AI content model context

File name: `custom-ai-content-model-context.xml`

Mount location and example:

```bash
./custom-ai-content-model-context.xml:/usr/local/tomcat/shared/classes/alfresco/extension/custom-ai-content-model-context.xml
```

Content:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">

    <!-- Registration of new models -->
    <bean id="org.alfresco.acme.dictionaryBootstrap" parent="dictionaryModelBootstrap" depends-on="org.alfresco.ai.dictionaryBootstrap">
        <property name="models">
            <list>
                <value>alfresco/extension/customAIContentModel.xml</value>
            </list>
        </property>
    </bean>
</beans>
```

### Custom AI content model

File name: `customAIContentModel.xml`

Mount location and example:

```bash
./customAIContentModel.xml:/usr/local/tomcat/shared/classes/alfresco/extension/customAIContentModel.xml
```

Content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<model name="acme:contentModel" xmlns="http://www.alfresco.org/model/dictionary/1.0">
    <description>Custom Content Model for Artificial Intelligence extension</description>
    <version>1.0</version>

    <imports>
        <import uri="http://www.alfresco.org/model/content/1.0" prefix="cm" />
        <import uri="http://www.alfresco.org/model/dictionary/1.0" prefix="d" />
        <import uri="http://www.alfresco.org/model/site/1.0" prefix="st" />
        <import uri="http://www.alfresco.org/model/system/1.0" prefix="sys" />
        <import uri="http://www.alfresco.org/model/ai/1.0" prefix="ai"/>
    </imports>

    <namespaces>
        <namespace uri="http://acme.org" prefix="acme" />
    </namespaces>

    <aspects>
        <aspect name="acme:applicantInfo">
            <title>Applicant Info</title>
            <parent>ai:textract</parent>
            <properties>
                <property name="acme:addressHome">
                    <title>Address (Home)</title>
                    <type>d:text</type>
                    <index enabled="true" />
                </property>
                <property name="acme:nameFull">
                    <title>Name (Full)</title>
                    <type>d:text</type>
                    <index enabled="true" />
                </property>
                <property name="acme:telephone">
                    <title>Telephone</title>
                    <type>d:text</type>
                    <index enabled="true" />
                </property>
                [...]
            </properties>
        </aspect>
        <aspect name="acme:w9form">
            <title>W-9</title>
            <parent>ai:textract</parent>
            <properties>
                [...]
            </properties>
        </aspect>
    </aspects>
</model>
```

### Custom AI property mapping

File name: `customAIPropertyMapping.json`

Mount location and example:

```bash
./customAIPropertyMapping.json:/usr/local/tomcat/customAIPropertyMapping.json
```

Content:

```json
{
    "keyValueMapping":[
        {
            "aiTextract":[
            {
                "key":"Mailing Address:",
                "aspect":"acme:applicantInfo",
                "property":"acme:addressHome",
                "keyMatch": "EXACT"
            },
            {
                "key":"Full Name",
                "aspect":"acme:applicantInfo",
                "property":"acme:nameFull",
                "confidence": "0.5"
            },
            {
                "key":"telephone number:",
                "aspect":"acme:applicantInfo",
                "property":"acme:telephone"
            },
            [...]
            ]
        }
    ]
}
```

In the above JSON snippet:

* The property mapping configuration is loaded and validated at application startup.
* If there's a mismatch between the aspect and the property, or if one or the other doesn't exist, a `WARN` message is logged, and the pairing is ignored (i.e. that particular pair is ignored, not the entire configuration).
* This example uses an `EXACT` key matching for the `Mailing Address` field. Other options include regular expressions, with a fallback to the default matching if `keyMatch` isn't defined. See [Form extraction (key-value pairs)]({% link intelligence-services/latest/config/textract.md %}#form-extraction-key-value-pairs) for more.

## Step 4: Configure Share and Digital Workspace

Use this information to configure the files needed by Share and Digital Workspace for a custom Textract model.

### Share

The following files must be mounted in the Share Docker container.

#### 1. Custom AI labels

File name: `share-config-custom.xml`

Mount location and example:

```bash
./share-config-custom.xml:/usr/local/tomcat/shared/classes/alfresco/web-extension/share-config-custom-dev.xml
```

Content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<alfresco-config>
    <config evaluator="string-compare" condition="DocumentLibrary">
        <!-- Aspects that a user can see -->
        <aspects>
            <visible>
                <aspect name="acme:applicantInfo"/>
                <aspect name="acme:w9form"/>
            </visible>
        </aspects>
    </config>
</alfresco-config>
```

> **Note:** The `ai:textLines` aspect is pre-configured in the Share AMP, so it doesn't need to be added to the custom configuration.

#### 2. Custom AI aspect configuration

File name: `bootstrap-custom-labels.properties`

Mount location and example:

```bash
./bootstrap-custom-labels.properties:/usr/local/tomcat/shared/classes/alfresco/web-extension/messages/bootstrap-custom-labels.properties
```

Content:

```bash
aspect.acme_applicantInfo=Applicant Info
aspect.acme_w9form=W-9
```

#### 3. Custom AI labels context

File name: `share-custom-slingshot-application-context.xml`

Mount location and example:

```bash
./share-custom-slingshot-application-context.xml:/usr/local/tomcat/shared/classes/alfresco/web-extension/custom-slingshot-application-context.xml
```

Content:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.springframework.org/schema/beans
                http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">

    <bean id="org.alfresco.acme.alfresco-ai-share.resources" class="org.springframework.extensions.surf.util.ResourceBundleBootstrapComponent">
        <property name="resourceBundles">
            <list>
                <value>alfresco/web-extension/messages/bootstrap-custom-labels</value>
            </list>
        </property>
    </bean>
</beans>
```

### Digital Workspace

The Digital Workspace configuration for custom AI requires modification of an existing configuration file (`ai-view.extension.json`). The JSON file is included in the Intelligence Services distribution zip. This is unlike the repository and Share configuration, where only new files are created and mounted in the containers.

#### App extension

File name: `ai-view.extension.json`

Mount location and example:

```bash
./ai-view.extension.json:/usr/share/nginx/html/assets/plugins/ai-view.extension.json
```

Content:

```json
[...]
"content-metadata-presets": [
    {
        "id": "app.content.metadata.custom",
        "custom": [
            {
                "id": "ai.metadata.features",
                "title": "AI Data",
                "items": [
                    {
                        "id": "acme:applicantInfo",
                        "aspect": "acme:applicantInfo",
                        "properties": "*"
                    },
                    {
                        "id": "acme:w9form",
                        "aspect": "acme:w9form",
                        "properties": "*"
                    },
                    [...]
                ]
            }
        ],
        [...]
    }
]
```

The above snippet adds the aspects in the earlier [Custom AI content model configuration]({% link intelligence-services/latest/config/textract.md %}#custom-ai-content-model) (for Textract) to the existing `"ai.metadata.features"` list of items in the `ai-view.extension.json` file.

For more details on extending the features of Digital Workspace, see the Alfresco Content Application documentation: [Extending](https://alfresco-content-app.netlify.com/#/extending/){:target="_blank"}.
---
title: Install Intelligence Services
---

The AI capability in Alfresco Intelligence Services is delivered as a distribution zip and Docker image. The zip contains the AIS extensions as repository and Share AMP files, and a number of configuration files. The Docker image provides an AI T-Engine for connecting with Amazon AI Services.

In this section you'll install and set up everything you need to run Intelligence Services. To get started:

* Review the prerequisites
* Set up services in AWS
* Install with distribution zip

## Prerequisites

* Make sure that you've tested your deployment with non-AI transforms and everything is working
* See [Supported platforms]({% link intelligence-services/latest/support/index.md %}) for more

### Access to Docker images

Some of the Docker images that are used by the Intelligence Services module are uploaded to a private registry, **Quay.io**. Since the Intelligence Services module adds AI capabilities to Alfresco Transform Service (see [Transform Service install overview]({% link transform-service/latest/admin/index.md %}#docker-images-overview)), you'll also need access to the following image:

```bash
alfresco/alfresco-ai-docker-engine
```

See [Install Intelligence Services]({% link intelligence-services/latest/install/index.md %}) and [Configure Intelligence Services]({% link intelligence-services/latest/config/index.md %}) for more.

* A [Quay.io](https://quay.io/){:target="_blank"} account is needed to pull Docker images that are needed for Intelligence Services.

> **Note:** Alfresco customers can request Quay.io credentials by logging a ticket at [Alfresco Support](https://support.alfresco.com/){:target="_blank"}. These credentials are required to pull private (Enterprise-only) Docker images from Quay.io.

> **Note:** Make sure that you request credentials for Alfresco Content Services and Alfresco Intelligence Services, so that you can use the additional `alfresco-ai-docker-engine-1.5.x` Docker image.

### AWS related requirements

To use Alfresco Intelligence Services, you need:

* An AWS account so that you can configure the Amazon AI services
* [Set up services in AWS]({% link intelligence-services/latest/install/index.md %}#set-up-services-in-aws)

### Limitations

* [Amazon Comprehend](https://aws.amazon.com/comprehend/faqs/){:target="_blank"} supports the following [Regions and Endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html){:target="_blank"}. For cost information, see [Amazon Comprehend Pricing](https://aws.amazon.com/comprehend/pricing/){:target="_blank"}.
* [Amazon Rekognition](https://aws.amazon.com/rekognition/faqs/){:target="_blank"} supports the following [Regions and Endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html){:target="_blank"}. For cost information, see [Amazon Rekognition Pricing](https://aws.amazon.com/rekognition/pricing/){:target="_blank"}.
* [Amazon Textract](https://aws.amazon.com/textract/faqs/) supports the following [Regions and Endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html){:target="_blank"}. For cost information, see [Amazon Textract Pricing](https://aws.amazon.com/textract/pricing/){:target="_blank"}.
* [Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/limits-guidelines.html){:target="_blank"} supports the following [Regions and Endpoints](https://docs.aws.amazon.com/general/latest/gr/transcribe.html#transcribe_region){:target="_blank"}. For cost information, see [Amazon Transcribe Pricing](https://aws.amazon.com/transcribe/pricing/){:target="_blank"}.  

You can also check the [AWS Region Table](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/){:target="_blank"} for all AWS global infrastructure.

> **Important:** Choose a common region that supports the Amazon AI Services that you wish to use.

### S3 buckets

You'll need to create a separate S3 bucket to use with the Amazon AI Services. It also needs to be in a common region that's supported by all the Amazon AI Services that you intend to use.

If you have an existing deployment that uses Alfresco Content Connector for AWS S3, it's recommended that you create a separate S3 bucket to use with Intelligence Services.

> **Important:** Create the AI S3 bucket in the same region as you intend to deploy Intelligence Services.

## Set up services in AWS

Use this information to set up the required services in AWS before you install Intelligence Services.

### Configure AWS Identity and Access Management

AWS Identity and Access Management (IAM) enables you to securely control access to AWS services and resources for your users. With IAM, you can create and manage AWS users and groups, and use permissions to allow and deny their access to AWS resources. Intelligence Services uses AWS IAM roles to ensure fine-grained control over access to the AI services and content stored in the S3 bucket.

Access to AWS services, such as Amazon Comprehend, requires that you provide credentials when you access them. The best way to provide those credentials is through IAM.

1. Follow the steps in [Creating your first IAM admin user and group](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html){:target="_blank"} to create and configure an IAM user.

2. Next, [create an S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html){:target="_blank"} to use with the Amazon AI Services.

    > **Note:** If you have an existing deployment that uses Alfresco Content Connector for AWS S3, it's recommended that you create a separate S3 bucket to use with Intelligence Services. Make sure that it's in the same region as you intend to deploy Alfresco Intelligence Services.

    > **Note:** The bucket name must be unique among all AWS users globally. See [S3 bucket restrictions and limitations](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html){:target="_blank"} for more information on bucket naming.

    See [Clean up in S3]({% link intelligence-services/latest/install/index.md %}#clean-up-in-s3) for guidance.

3. Go to the **AWS Console** and open the **IAM** console.

4. Select **Policies** from the menu and click **Create policy**.

5. Switch to the **JSON** tab to create the policy using JSON syntax.

6. Copy the following content, replace the bucket name, `alfrescoai`, with your AI bucket name:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:GetObject",
                "Resource": [
                    "arn:aws:s3:::alfrescoai/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": [
                    "arn:aws:s3:::alfrescoai"
                ]
            },
            {
                "Effect": "Allow",
                "Action": "s3:PutObject",
                "Resource": "arn:aws:s3:::alfrescoai/*"
            }
        ]
    }
    ```

7. Click **Review policy**.

8. Type a name for your policy and click **Create policy**.

    For example, `ComprehendAsyncJobs`.

    > **Note:** The policy name must be unique across your organization.

9. Select **Roles** from the menu and click **Create role**.

    Next, you'll select the type of trusted entity (for example, an AWS service, another AWS account, etc.). Since Amazon Comprehend isn't an available AWS service, you can select EC2 and change the Trust Relationship later.

10. Choose **EC2** and click **Next: Permissions**.

11. Choose one or more policies to attach to your new role (including the one you created in step 8.

12. Click **Next** until you reach the **Review** page.

13. Type a name for the role and click **Create role**.

    For example, `ComprehendAsyncJobs`.

    > **Note:** The role name must be unique across your organization.

14. Select the role you just created, and copy the `Role ARN` field.

    The Amazon Resource Name (ARN) is a unique identifier for this AWS resource. You'll use this later when configuring environment variables.

    Next, change the Trust Relationship to Amazon Comprehend instead of EC2.

15. Switch to the **Trust Relationship** tab, and select **Edit Trust Relationship**.

16. Replace `ec2.amazonaws.com` in the policy document:

    ```json
    "Service": "comprehend.amazonaws.com"
    ```

17. Click **Update Trust Policy** to complete this stage.

    Now that the role has been created, the IAM user needs to be given the ability to assign this role to Amazon Comprehend. You have two options:

    * Give the IAM user full ability to assign any role using [Role-Based Permissions Required for Asynchronous Operations](https://docs.aws.amazon.com/comprehend/latest/dg/access-control-managing-permissions.html#auth-role-permissions){:target="_blank"}.
    * Alternatively, you can give the IAM user only access to the role you created. Here's an example:

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "iam:GetRole",
                        "iam:PassRole"
                    ],
                    "Resource": "arn:aws:iam::XXXXXXXXXXXX:role/ComprehendAsyncJobs"
                }
            ]
        }
        ```

Now you can use asynchronous operations by configuring the `ROLE_ARN` property with the ARN of this configured role. The Transform Engine can now split input documents larger than 125KB, upload the chunks to the configured S3 bucket, start the job, and poll the result until it finishes. The chunks are deleted after the process is completed.

## Set up Amazon AI services

Use this information to set up Amazon AI services (Amazon Comprehend, Amazon Rekognition, and Amazon Textract). Before continuing, make sure that you've already [set up an IAM user](#configure-aws-identity-and-access-management).

### Roles and permissions

Review the permission requirements for each Amazon AI Service that you intend to use.

{% capture comprehend %}

In order to use IAM roles, a new policy must be created that'll be used by the IAM role. Policies are used to grant permissions to groups. If there isn't a policy already in place for Amazon Comprehend access, a new policy must be created. The credentials associated with your IAM user must have permissions to [access Amazon Comprehend actions](https://docs.aws.amazon.com/comprehend/latest/dg/auth-and-access-control.html){:target="_blank"}. These permissions are customized through roles associated with your IAM user.

In order to use Amazon Comprehend, you'll need to create a new IAM role, and [configure a policy](https://docs.aws.amazon.com/comprehend/latest/dg/access-control-managing-permissions.html){:target="_blank"} to access the desired services within Comprehend. You can use one of the predefined policies, `ComprehendFullAccess` or `ComprehendReadOnly`. Both grant you full access to Amazon Comprehend, but the second one doesn't allow you to use asynchronous jobs.

> **Note:** You must grant Amazon Comprehend access to the Amazon S3 bucket (i.e. AI S3 bucket) that contains your document collection. You can do this by creating a data access role in your account to trust the Amazon Comprehend service principal.

{% endcapture %}

{% capture rekognition %}

The credentials associated with your IAM user must have permissions to [access Amazon Rekognition actions](https://docs.aws.amazon.com/rekognition/latest/dg/security-iam.html){:target="_blank"}. These permissions are customized through roles associated with your IAM user.

In order to use Amazon Rekognition, you'll need to create a new IAM role, and [configure a policy](https://docs.aws.amazon.com/rekognition/latest/dg/security_iam_id-based-policy-examples.html){:target="_blank"} to access the desired services within Rekognition. You can use one of the predefined policies, `AmazonRekognitionFullAccess` or `AmazonRekognitionReadOnlyAccess`. Both grant you full access to Amazon Rekognition, but the second one doesn't allow you to create or delete collections.

When analyzing images larger than 5MB (and up to 15MB), they'll first be uploaded to an S3 bucket. Make sure that you setup a bucket in the same region as you intend to deploy Intelligence Services.

> **Note:** You must grant Amazon Rekognition access to the S3 bucket used above.

{% endcapture %}

{% capture textract %}

The credentials associated with your IAM user must have permissions to access Amazon Textract actions. These permissions are customized through roles associated with your IAM user.

In order to use Amazon Textract, you'll need to create a new IAM role and configure a policy to access the desired services within Textract. The easiest way to do this is to attach the AWS managed policy `AmazonTextractFullAccess` to the IAM role.

> **Note:** You must grant Amazon Textract access to the S3 bucket used above.

{% endcapture %}

{% capture transcribe %}

The credentials associated with your IAM user must have permissions to access Amazon Transcribe actions. These permissions are customized through roles associated with your IAM user.

In order to use Amazon Transcribe, you'll need to create a new IAM role and configure a policy to access the desired services within Transcribe. The easiest way to do this is to attach the AWS managed policy `AmazonTranscribeFullAccess` to the IAM role.

> **Note:** You must grant Amazon Transcribe access to the S3 bucket used above.

{% endcapture %}

{% include tabs.html tableid="permissions" opt1="Comprehend" content1=comprehend opt2="Rekognition" content2=rekognition opt3="Textract" content3=textract opt4="Transcribe" content4=transcribe %}

### Configure minimum confidence level

There's a setting for the level of confidence that each AWS AI service has in the accuracy of the extracted content. This is defined as the minimum confidence level and has a default value of 80% (i.e. `0.8`). Here are the settings in `alfresco-global.properties`:

```bash
#################################
# Alfresco-AI Parameters        #
#################################

ai.transformations.aiLabels.minConfidence=0.8
ai.transformations.aiFeatures.minConfidence=0.8
ai.transformations.aiTextract.minConfidence=0.8
ai.transformations.aiPiiEntities.minConfidence=0.8
ai.transformations.aiSpeechToText.minConfidence=0.8
```

### Clean up in S3

Whenever files are written to S3 for processing, they're removed once processing finishes or an exception is encountered. However, if the service is stopped or an uncaught exception is thrown, it's possible that files may be left in S3. It's recommended that you set up a policy on the S3 bucket so that objects that are older than a day are removed from the bucket.

To do this, you can create a lifecycle rule that expires all versions of objects after 1 day, and then permanently deletes them one day after that.

See the AWS site for more details on [Object lifecycle management](https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html){:target="_blank"}.

## Install with zip

Use these instructions to install the Intelligence Services AMP files to an instance of Content Services.

The Intelligence Services distribution zip file, `alfresco-ai-distribution-1.5.x.zip`, includes all the files required to provide Intelligence Services. Ensure that you've installed the required software and completed the AWS set up before installing Intelligence Services.

1. Download the Intelligence Services distribution zip file.

2. Extract the `alfresco-ai-distribution-1.5.x.zip` file into a system directory; for example, `<installLocation>/`.

    In this directory you'll see the following content:

    * `alfresco-ai-repo-1.5.x.amp`: AMP to be applied to the Content Services repository
    * `alfresco-ai-share-1.5.x.amp`: AMP to be applied to Alfresco Share
    * `ai-pipeline-routes.json`: custom Transform Router configuration properties
    * `ai-view.extension.json`: custom extension file for Alfresco Digital Workspace

3. Stop the Content Services server.

4. Copy the provided AMP files to the Alfresco `amps` and `amps_share` directories.

    Copy the repository AMP file to the `amps` directory:

    * `alfresco-ai-repo-1.5.x.amp`

    Copy the Share AMP file to the `amps_share` directory:

    * `alfresco-ai-share-1.5.x.amp`

5. Delete the `tomcat/webapps/alfresco` and `tomcat/webapps/share` folders in the Content Services installation directory.

6. Navigate to the `bin` directory to run the Module Management Tool (MMT) file to install the AMP files into the relevant WAR file:

    1. For the Content Services repository:

        ```java
        java -jar <alfrescoInstallLocation>/bin/alfresco-mmt.jar install <installLocation>/amps-repository/alfresco-ai-repo-1.5.x.amp <installLocation>/tomcat/webapps/alfresco.war
        ```

    2. For Alfresco Share:

        ```java
        java -jar <alfrescoInstallLocation>/bin/alfresco-mmt.jar install <installLocation>/amps-share/alfresco-ai-share-1.5.x.amp <installLocation>/tomcat/webapps/share.war
        ```

    For more information, see [Using the Module Management Tool (MMT)]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt) and [Installing an Alfresco Module Package]({% link content-services/latest/install/zip/amp.md %}).

    Check the output to ensure that the AMP files have installed successfully.

7. Check that the [configuration]({% link intelligence-services/latest/config/index.md %}) is set up correctly for your environment.

8. Restart the Content Services server.
---
title: Supported platforms
---

The following are the supported platforms for Alfresco Intelligence Services 3.1:

| Version | Notes |
| ------- | ----- |
| Content Services 23.x | |
| Content Services 7.4 | |
| Transform Service 4.1 | |
| Transform Service 4.0 | |
| Digital Workspace 4.4 | |
| Digital Workspace 4.3 | |
---
title: Using Intelligence Services
---

You can configure the data to extract using a folder rule in Alfresco Share, and view the data returned by Amazon AI Services (via the AI Transform Engine) in Alfresco Digital Workspace.

To use the default (i.e. out-of-the-box) configuration of Intelligence Services, follow the **default configuration** steps.

If you plan to use custom recognizers and custom classifiers to enrich your content with custom metadata, follow the **default configuration**, and then the **custom configuration** steps.

> **Note:** Before you can use a custom rendition, make sure that you've trained a custom model, deployed and configured one of the custom implementations listed in [Configure Intelligence Services]({% link intelligence-services/latest/config/index.md %}).

## Set up a folder rule

You can use the Intelligence Services components by setting up a folder rule and adding text and images to that folder.

### Default configuration: Requesting default AI renditions

Follow these steps to use the default (i.e. out-of-the-box) configuration of Intelligence Services.

1. In Alfresco Share create a test folder.

2. Select the folder and click **Manage Rules** to create a folder rule.

3. Click **Create Rules**.

4. Enter a name and a description (optional) for the rule.

5. Select when the rule is triggered.

    Choose Items are created or enter this folder, and (optionally) **Items are updated**. Use the + and - icons to add and remove extra criteria.

6. Select when the rule is applied.

    Add **Content of type or sub-type** is **Content**, as shown.

    ![Select criteria for rule]({% link intelligence-services/images/select-criteria.png %})

7. Select a rule action to perform.

    1. Select **Request AI renditions**.

    2. Enter one or more renditions in the text field, separated by commas.

        For example, you can add any of the default renditions:

        ```bash
        aiFeatures, aiLabels, aiTextract, aiSpeechToText, webvtt, aiPiiEntities 
        ```

        > **Note:** If you leave the text field empty all of the default renditions will be requested.

8. (Optional) Select options **Rule applies to subfolders** and also apply when **Items are updated**.

    This will apply the rule to your test folder and all its subfolders.

9. Click **Create** to save the rule.

    At this point, your rule has been applied to request the AI renditions and add the selected AI aspects.

    See the Content Services documentation, [Folder rules]({% link content-services/latest/using/content/rules.md %}) to find out more about applying folder rules.

10. Next, upload content to your test folder.

    For example, choose a text file and a PNG or JPG image.

11. Wait for the renditions to complete.

    As an administrator, you can view the logs for the repository, Transform Router, AI Engine, and ActiveMQ/Amazon MQ to monitor the progress.

    See [Troubleshoot Intelligence Services]({% link intelligence-services/latest/admin/troubleshoot.md %}) for more.

12. Next, [view the AI properties]({% link intelligence-services/latest/using/index.md %}#view-ai-properties) in Alfresco Digital Workspace.

### Custom configuration: Requesting custom AI renditions

If you're planning to use custom recognizers, custom classifiers, or custom metadata extraction, start by following the steps in the default configuration, and then modify step 7.

1. Add a rule on the folder to request custom AI renditions and extract custom metadata.

    Choose Items are created or enter this folder.

2. Select a rule action to perform.

    1. Add custom AI aspects, for example:

        ![Add configured custom AI aspects]({% link intelligence-services/images/cust-aspects.png %})

        See [Custom AI content model]({% link intelligence-services/latest/config/comprehend.md %}#custom-ai-content-model) for configured aspects.

    2. Request custom AI renditions, for example:

        ![Request configured custom AI renditions]({% link intelligence-services/images/cust-renditions.png %})

        See [Custom AI rendition definitions]({% link intelligence-services/latest/config/comprehend.md %}#custom-ai-rendition-definitions) for configured renditions.

    3. For custom metadata extraction (using Textract), request a rendition and add custom AI aspects. For example:

        * Request AI rendition: `aiTextract`
        * Add aspect: `AI Text Lines`
        * Add aspect: `Applicant Info`
        * Add aspect: `w9form`

        See [Custom AI content model (Textract)]({% link intelligence-services/latest/config/textract.md %}#custom-ai-content-model) for configured aspects.

    > **Note:** The new input field for the `Request AI renditions` action adds the ability to request custom renditions as comma separated rendition names. When left blank, the three default renditions are requested - (i.e. `aiFeatures`, `aiLabels`, and `aiTextract`). This allows you to configure a rule using various combinations, such as:
    >
    > ```bash
    > aiFeatures, aiBusinessCustom, aiBusinessSport
    > ```

## View AI properties

You can view the Intelligence Services properties in Alfresco Digital Workspace.

This example shows you how to view these properties in Digital Workspace.

1. Launch Alfresco Digital Workspace.

2. Locate the demo folder or subfolder, if the folder rule also applies to subfolders, as created in [Set up a folder rule]({% link intelligence-services/latest/using/index.md %}#set-up-a-folder-rule).

3. Select a file that you uploaded, and click the information icon.

    The Info Drawer shows the AI properties that were extracted by the AI Engine, and saved as AI Data. These are populated by the aspects defined when you created the folder rule in Share.

4. Click **Less information** to show AI Data under the Properties tab, if you can't see it.

5. Expand the AI Data panel to see all the properties that have been added.

    **Searching for content in ADW**

    You can search for content that matches one of the AI aspects, perform a wildcard search (using an asterisk, wildcar*), or phrase match (using double-quotes, "This Phrase").

6. To search for a place in an AI aspect, type `schema:place:<place-name>` in the search field and press **Enter**.

    The search results are displayed.

    Similarly, if you uploaded test images, you can search for `schema:label:<label>`.

    **Searching for custom properties in ADW**

7. To search by a custom property, type `schema:<category>:<content>` in the search field and press **Enter**.

    For example, enter `schema:sport:runner`

## View Transcription

When configured, transcripts of your audio and video files are generated automatically within the Digital Workspace, including indexing and metadata generation which allows you to search their content easier. Captions of the transcripts can be automatically placed on top of the audio and video content, see the images below. For information on how to configure this in the Digital Workspace see [Set up a folder rule]({% link intelligence-services/latest/using/index.md %}#set-up-a-folder-rule).

**Transcription**
![transcript]({% link intelligence-services/images/text-transcript.png %})

**Caption**
![caption]({% link intelligence-services/images/transcript-caption.png %})

## View PII information

You can detect PII in documents and tag it automatically which enables easier privacy management to comply
with data protection regulations such as General Data Protection Regulation (GDPR). You can also generate metadata automatically to flag PII entities, see the image below. For information on how to configure this in the Digital Workspace see [Set up a folder rule]({% link intelligence-services/latest/using/index.md %}#set-up-a-folder-rule).

**PII**
![pii]({% link intelligence-services/images/pii.png %})