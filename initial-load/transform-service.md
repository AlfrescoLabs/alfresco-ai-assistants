---
title: Alfresco Transform Service
---

The Alfresco Transform Service provides a secure, scalable, reliable, and extensible mechanism for converting files from 
their current format into other formats.

The Transform Service provides a number of Transform Engines (T-Engines) that perform single-step transformations. The
Transform Service also provides a Transform Router that sits in front of the T-Engine(s) to provide move complex
multi-step transformations that combine the single steps into pipelines and a failover mechanism where alternatives are
tried until one of them succeeds.

The Transform Router, and the T-Engine(s), runs as independently scalable Docker containers. The Transform Router is 
connected to the Alfresco Content Services repository and T-Engines via ActiveMQ, a message broker, which is used to
send transformation requests and responses:

![Transform service components Overview Docker Compose]({% link transform-service/images/ats-1.4-components-docker-compose-deploy.png %})

The message broker by its nature is asynchronous, making these request-responses asynchronous. However, there are
currently some situations in the Alfresco Share user interface and for text extraction to Solr where a synchronous
request-response is required. In these cases, the Alfresco Content Services repository will communicate directly with
the T-Engines via HTTP. It also provides the same pipeline or failover transforms as the T-Router. This synchronous
usage of the T-Engine(s) is referred to as *Local Transforms*. You might also come across something called *Legacy 
Transformers*, which were transformers embedded in the Repository code. In Alfresco Content Services 7, the
out-of-the-box Legacy transformers and framework have been removed. The Community Edition only has access
to the *Local Transforms* framework which is used both for synchronous and asynchronous requests.

Files that to be transformed or returned to the Alfresco Content Services repository or Elastic Search are generally
stored in the Shared File Store. If configured, direct access URLs may also be used to avoid some file transfer steps.

Multiple T-Engines may be deployed, but for simplicity there is an all-in-one T-Engine that provides the same
Core transformations as five separate T-Engines for use in all but the largest deployments, where it's still  
advisable to separate out the different types of transforms into their own images. Note that the all-in-one 
Transform Core T-Engine is the default option for the Docker Compose deployment and installation using the distribution zip.
However, Kubernetes deployments with Helm continue to use the five separate T-Engines in order to provide balanced 
throughput and scalability improvements. Additional T-Engines may be added to the mix:

![Transform service components Overview Kubernetes]({% link transform-service/images/ats-1.4-components-helm-deploy.png %})

The extraction of metadata is performed in the T-Engines. Prior to Alfresco Content Services 7, it was performed inside
the content repository.

The key capabilities of the Transform Service include the ability to:

* Scale the transformation capabilities independently of the content repository.
* Exposed the transformation capabilities to other components.
* Provide a greater level of reliability and fault tolerance by using persistent queues.
* Develop custom (i.e. out of process) transformers to enable the migration of any existing transform customizations.
* Scale the metadata extraction independently of the content repository.

There are two main options for deployment: 

* [Containerized deployment]({% link transform-service/latest/install/index.md %}#containerized-deployments)
* [Distribution zip install]({% link transform-service/latest/install/index.md %}#prereq-non-containerized-deploy)

>**Important:** The Transform Service is deployed as part of the Alfresco Content Services deployment for containerized 
>deployments only. See [What's deployed in Content Services]({% link content-services/latest/install/containers/index.md %}#whats-deployed-in-content-services) 
>for the list of components.

>**Important:** If you're installing Content Services using the distribution zip, you can install the Transform Service 
>using an additional distribution zip.
---
title: Administer Transform Service
---

The following section describes the Transform Service components, and also explain the flow of information between the repository and these components during the transformation process.

## Transform Service components

The Transform Service handles the essential transforms, such as Microsoft Office documents, images, and PDFs. These include PNG for thumbnails, PDF and JPEG for downloads and previews.

The main components of the Transform Service are:

* **Content Repository (ACS)**: This is the repository where documents and other content resides. The repository produces and consumes events destined for the message broker (such as ActiveMQ or Amazon MQ). It also reads and writes documents to the shared file store.
* **ActiveMQ**: This is the message broker (either a self-managed ActiveMQ instance or Amazon MQ), where the repository and the Transform Router send image transform requests and responses. These JSON-based messages are then passed to the Transform Router.
* **Transform Router**: The Transform Router allows simple (single-step) and pipeline (multi-step) transforms that are passed to the Transform Engines. The Transform Router (and the Transform Engines) run as independently scalable Docker containers.
* **Transform Engines**: The Transform Engines transform files referenced by the repository and retrieved from the shared file store. Here are some example transformations for each Transform Engine (this is not an exhaustive list):
  * LibreOffice (e.g. docx to pdf)
  * ImageMagick (e.g. resize)
  * Alfresco PDF Renderer (e.g. pdf to png)
  * Tika (e.g. docx to plain text)
  * Misc. (not included in diagram)
* **Shared File Store**: This is used as temporary storage for the original source file (stored by the repository), intermediate files for multi-step transforms, and the final transformed target file. The target file is retrieved by the repository after it's been processed by one or more of the Transform Engines.

The following diagram shows a simple representation of the Transform Service components:

![Transform service components Overview]({% link transform-service/images/ats-1.3.2-components.png %})

Note that from Transform Service version 1.3.2 the metadata extraction that usually takes part in the core repository 
legacy transform engines has now been lifted out into the separate transform engine processes. This enables scaling 
of the metadata extraction.

This shows an example implementation of how you can deploy into AWS, using a number of managed services:

* Amazon EKS - Elastic Container Service for Kubernetes
* Amazon MQ - Managed message broker service for [Apache ActiveMQ](https://activemq.apache.org/){:target="_blank"}
* Amazon EFS - Amazon Elastic File System

You can replace the AWS services (EKS, MQ, and EFS) with a self-managed Kubernetes cluster, ActiveMQ (configured with failover), and a shared file store, such as NFS.

> **Note:** For more detailed representations of the Alfresco Content Services deployment (including the Transform Service), see the GitHub [Docker Compose](https://github.com/Alfresco/acs-deployment/tree/master/docs/docker-compose){:target="_blank"} and [Helm](https://github.com/Alfresco/acs-deployment/tree/master/docs/helm){:target="_blank"} documentation.

The advantage of using Docker containers is that they provide a consistent environment for development and production. They allow applications to run using microservice architecture. This means you can upgrade an individual service with limited impact on other services.

## Docker images overview

A typical containerized deployment of Transform Service looks as follows:

![Docker Compose Deployment Overview]({% link transform-service/images/ats-1.3.2-containerized-deployment.png %})

Note that from Transform Service version 1.3 all the transform engines are contained in one component called 
Transform Core All-In-One (AIO) Engine. Only for large deployments are the Transform Engines deployed separately.

Some of the Docker images that are used by the Transform Service are uploaded to a private registry, **Quay.io**. Enterprise customers can contact [Alfresco Support](https://support.alfresco.com/){:target="_blank"} to request Quay.io account credentials to pull the private (Enterprise-only) Docker images:

* `quay.io/alfresco/alfresco-transform-router`

The other images are available in DockerHub:

* `alfresco/alfresco-transform-core-aio`
* `alfresco/alfresco-pdf-renderer`
* `alfresco/alfresco-imagemagick`
* `alfresco/alfresco-libreoffice`
* `alfresco/alfresco-tika`
* `alfresco/alfresco-shared-file-store`
* `alfresco/alfresco-transform-misc`

For information about deploying and configuring the Transform Service, see [Install Transform Service]({% link transform-service/latest/install/index.md %}).

## Troubleshoot Transform Services

Use this information to help monitor and troubleshoot the Transform Service.

### How do I monitor the Transform Engines (e.g. LibreOffice) and the Transform Router

There are two options for monitoring each component:

* View the logs via the Kubernetes dashboard.
* Access the `/metrics` and the `/prometheus` endpoint, which expose information about the running processes.

### What do I do if LibreOffice hangs

If LibreOffice hangs, the health endpoint will fail to respond, and the container/pod will automatically reboot. This applies to all five Docker transformers. The Content Services Helm deployment uses two replicas for each component of the Transform Service by default (except for the shared file store) in order to provide scalability and fault tolerance.

### What debug logging is available for the Transform Service

All the key operations are logged, as well as the different entry and exit points for all kind of processes and actions.

### What do I do if Tika runs out of memory

Similar to LibreOffice, the Tika container/pod should automatically restart since OOM is an error. If the automatic restart fails, the pods can be restarted from the Kubernetes dashboard.

### How do I monitor ActiveMQ / Amazon MQ

* Access the ActiveMQ Admin Console (Web Console) at `<amazon-mq-host>`.
* The micrometer implementation also monitors the size of the queue.

### Are any metrics sent to/via HeartBeat

No. HeartBeat hasn't been integrated yet.

### Where are the temporary files located for individual and multi-step transforms

The individual transform, or Transform Engine, cleans up its own temporary files within the running container. For multi-step transforms, the intermediate files will eventually be cleaned up by the Shared File Store.

### Is any monitoring/metrics system available

Yes:

* All the Transform Service components use micrometer.
* The Prometheus service that's deployed ingests data from the Transform Router.

### If a transform fails when uploading a complex XLSX document, what happens

The Transform Service will attempt to retry the transform a few times (this is configurable). Otherwise, a failed transform is returned to the repository, so no preview or thumbnail will be available. The repository will no longer retry.

### Can you share the Transform Service with multiple repositories

This release will only support a single Content Services repository instance. For example, if you have two or more separate Content Services deployments (whether clustered or not), then each one will need to its own Transform Service instance.

## Error handling in Transform Router

Use this information to review the possible responses from the Transform Router (T-Router) if a problem occurs.

The Transform Service is designed to be easy to set-up and debug. However, when a problem occurs, the T-Router tries to respond with a failed Transform Reply (T-Reply). Here are a few examples:

|T-Reply|Possible T-Reply response|
|-------|-------------------------|
|400 BAD REQUEST|T-Request with an `invalid JSON` is received|
|400 BAD REQUEST|T-Request with `invalid/missing values` is received|
|400 BAD REQUEST|T-Request with an `unsupported transformation` is received|
|500 INTERNAL SERVER ERROR|Transformation `fails in the T-Engine`|
|500 INTERNAL SERVER ERROR|When any other `unexpected exception in the T-Router` is thrown|
|no reply|When a `Java Error` (*Throwable*, but not *Exception*) occurs in the T-Router, the problem is only logged.|
---
title: Add T-Engines to T-Router 
---

The Transform Router (T-Router) uses Transform Engine (T-Engine) names to register new engines via properties. The names 
must be unique and consistent for each engine, for both of its properties (url and queue). Examples of such name are: 
`IMAGEMAGICK`, `LIBREOFFICE`, `PDF_RENDERER`, `TIKA`, `TRANSFORMER1`, `CUSTOM_ENGINE`, `CUSTOM_RED_ENGINE`, etc. 

The T-Engine names are case-insensitive.

Engine configuration is part of the T-Router SpringBoot `application.yaml` configuration:

```yaml
transformer:
  url:
    imagemagick: http://imagemagick-host:8091
    pdf_renderer: http://pdf-renderer-host:8090
  queue:
    imagemagick: org.alfresco.transform.engine.imagemagick.acs
    pdf_renderer: org.alfresco.transform.engine.alfresco-pdf-renderer.acs
  engine:
    protocol: ${TRANSFORMER_ENGINE_PROTOCOL:jms}  # this value can be one of the following (http, jms)
```

These properties can be overridden by environment variables on the T-Router container:

```bash
export TRANSFORMER_URL_IMAGEMAGICK="http://host1"
export TRANSFORMER_QUEUE_IMAGEMAGICK="queue66"

export TRANSFORMER_URL_PDF_RENDERER="http://host2:8099"
export TRANSFORMER_QUEUE_PDF_RENDERER="queue-red-black"

export TRANSFORMER_ENGINE_PROTOCOL="http"
```

Additional custom engines can be configured through environment variables as well:

```bash
export TRANSFORMER_URL_CUSTOM_RED_ENGINE="http://red-engine-host:8090"
export TRANSFORMER_QUEUE_CUSTOM_RED_ENGINE="red-engine-queue"
```

The HTTP URL is for retrieving the engine config, and for transform requests in HTTP mode. The queue is used for 
transform requests in JMS mode, transform config is not retrieved in this way.

All registered engines are queried via their HTTP URL for transform config on T-Router startup. This allows for 
auto-configuration of engine transformers, and generates a transform config for the T-Router. The T-Router transform 
config consists of aggregated transform configs from all engines plus all available pipeline transformers. It can be 
checked using the `/transform/config` endpoint. During the registration process, the engine names provided in the 
properties are mapped to the corresponding transformers supported by the particular engine and to the corresponding 
JMS queue.

## T-Router pipeline configuration
This section assumes that you're familiar with transformer concepts used in Alfresco Content Services and now in the 
Transform Service. A good place to start is the [Content Services](https://github.com/Alfresco/acs-packaging/blob/master/docs/custom-transforms-and-renditions.md){:target="_blank"} 
GitHub documentation, as the concepts and transformer configuration are identical.

Here's a very brief overview.

Each T-Engine may contain multiple transformers, as exposed via its `/transform/config` endpoint. Each transformer has a 
list of supported transforms, which consist of:

* source and target media types (similar to mimetype)
* maximum supported source file size
* priority

The priority is used in resolving conflicts or to deliberately override existing transforms, where everything else is 
equal. Each transformer can also have a set of options, for example, an image processing transformer might have options 
for the target image parameters (resolution, aspect ratio, etc.). All of this information determines the transformer for 
each incoming request. Pipeline transformers can be defined in terms of other pipeline transformers. Pipelines examples 
are provided later.

## Out of the box pipeline transformer definitions
The T-Router supports pipeline transformers, allowing it to perform transformations in a sequence of requests to various 
engines. This functionality is identical in definition to Content Services pipeline transformers (starting from Alfresco 
Transform Service 1.3.0). For more information on these pipelines, see the Content Services GitHub documentation on 
[Configuring a custom transform pipeline](https://github.com/Alfresco/acs-packaging/blob/master/docs/custom-transforms-and-renditions.md#configure-a-custom-transform-pipeline){:target="_blank"} 
as the T-Router pipeline transformers are defined using the same format. Due to this commonality, pipelines defined in 
Content Services can be moved to Transform Service directly. However, it's worth mentioning that most of the pipeline 
definitions provided out of the box are identical to the pipeline definitions in Content Services.

The pipeline configuration file provided is bundled in the standard T-Router artifact/Docker image (the top resource 
being `transformer-pipelines.json`).

The default file is specified through the SpringBoot property `transformer-routes-path`, which can be overridden by 
the `TRANSFORMER_ROUTES_PATH` environment variable.

>**Note:** It is not recommended to override the default routes file, unless none of the pipelines are applicable for 
>the use case. Instead, you can specify additional transforms defined in the provided `transformer-pipelines.json` file.

Here's one of the pipeline transformers that provides additional transforms defined in the provided 
`transformer-pipelines.json` file:

```json
{
    "transformers": [
        {
            "transformerName": "pdfToImageViaPng",
            "transformerPipeline": [
                {
                    "transformerName": "pdfrenderer",
                    "targetMediaType": "image/png"
                },
                {
                    "transformerName": "imagemagick"
                }
            ],
            "supportedSourceAndTargetList": [],
            "transformOptions": [
                "pdfRendererOptions",
                "imageMagickOptions"
            ]
        }
    ]
}
```

The above definition will introduce a new transformer, specifically a pipeline transformer called `pdfToImageViaPng`. The 
pipeline transformer is made up of two single-step transformers, `pdfrenderer` and `imagemagick`. If the 
`supportedSourceAndTargetList` is left blank, then the T-Router will complete the supported list automatically. The 
supported list can be restricted to specific sources and targets by explicitly defining them, just like a single-step 
transformer in an engine would. Priorities can be used to override conflicting transforms provided by other transformers.

>**Note:** Pipeline transformers become available only if all the involved single-step transformers are available. The 
>application logs will report any missing pipeline transformers on startup and config refresh.

## Add new pipeline transformer definitions
Additional transformers can be defined in new JSON or YAML files and specified through environment variables with the 
`TRANSFORMER_ROUTES_ADDITIONAL_` prefix:

```bash
export TRANSFORMER_ROUTES_ADDITIONAL_<name>="/path/to/the/additional/route/file.json"
```

>**Note:** The `<name>` suffix can be a random string. It doesn't need to match any other labels - it just 
>differentiates multiple additional route files.

Here's example content of an additional pipeline in JSON format (same as the `transformer-pipelines.json`) provided. 
The environment variable `TRANSFORMER_ROUTES_ADDITIONAL_OFFICE_TO_IMAGE="/additional.json"`, and the `additional.json` 
file could be:

```json
{
    "transformers": [
        {
            "transformerName": "pdfToImageViaPng",
            "transformerPipeline": [
                {
                    "transformerName": "pdfrenderer",
                    "targetMediaType": "image/png"
                },
                {
                    "transformerName": "imagemagick"
                }
            ],
            "supportedSourceAndTargetList": [],
            "transformOptions": [
                "pdfRendererOptions",
                "imageMagickOptions"
            ]
        }
    ]
}
```

The custom pipeline definition files must be mounted on the T-Router container file-system.

Multiple additional pipeline files can be specified. Ideally, for each new custom engine a separate custom pipeline file 
should be added.

In case of clashes between transformers and their supported transforms:

* If two transformers support the same source and target media type, the transformer with the higher priority is used 
  (i.e. a lower numeric value is considered higher priority).
* If the same transform is specified in multiple transformers with the same transform options, `priority` and 
  `maxSourceFileSize`, then one of the transformers will be chosen at random.

## Transform option filtering
Each transformer can reference transform option names which it claims to support, but a pipeline transformer might 
reference options for multiple transformers as inherited from its single-step transformers. In order to send the correct 
options to the correct transformer, the options are filtered for each transform request to a T-Engine.

If the applicable transformer is a single-step transformer, the request is sent to the relevant T-Engine, with the 
request transform options filtered based on the transformer's supported transform options list.

If the applicable transformer is a pipeline transformer, then T-Router will filter transform options from the request 
for each intermediate step with respect to the current step's transformer.
---
title: Configure Transform Service
---

The Transform Router (T-Router) configures Transform Engines (T-Engine) transformers automatically by retrieving the 
engine transform configurations from each configured T-Engine. The engine transform configurations provide the
transformer configuration, including the supported transformers, and their transform options.

For more information on the format of the transform configuration and instructions on how to create a transform
configuration files for a custom engine, see [Creating a T-Engine](https://github.com/Alfresco/acs-packaging/blob/23.1.0/docs/creating-a-t-engine.md){:target="_blank"}.

T-Engines are added to the T-Router by adding the engine's URL and JMS queue name used by each and every engine. See
next section for the URL and JMS queue name property format.

The T-Router supports 2 types of transformers:

* **Single-step transformer**: This maps transformation requests to a single T-Engine, which can directly transform the
  `source media type` to the `target media type` with the provided `transform options` and `source file size`.

  For example: `image/png` to `image/png` is handled by the `IMAGEMAGICK` transformer.

* **Pipeline transformer**: This maps transformation requests to a sequence of intermediate transformation requests steps,
  which are handled by multiple T-Engines. These transformers handle situations where there is no single engine that can
  directly transform one media type to another, but that can be achieved through intermediate media types and transformations.

  For example: `application/msword` to `image/png` can't be directly performed by one single engine, but it can be
  handled by `LIBREOFFICE` (which would generate `application/pdf`) and then `PDF_RENDERER`.

Single-step transformers map to a transformer, which in turn maps to a T-Engine. Each T-Engine can have multiple
transformers defined in its configuration. The single-step transformers are configured automatically from T-Engine
transform configuration files.

Pipeline transforms map to a pipeline transformer, which in turn maps to a series of single-step transformers. These are
defined through configuration files in the T-Router. This is described in the later section about pipelines.

A T-Engine is intended to be run as a Docker image, but may also be run as a standalone process.

For an overview of the Transform Service, including the T-Router, T-Engines, Local transforms, Legacy transforms etc see [overview]({% link transform-service/latest/index.md %}).

## Repository specific configuration
This section covers transform configuration on the Alfresco Content Services Repository side. As it is possible to 
configure transformations on both the Repository side, and the T-Router side, we will cover both. Repository configuration
is also used when the Alfresco Content Services Community Edition is used.

### Configure a T-Engine as a Local Transform
For the Repository to talk to a T-Engine directly, it must know the engine's URL. The URL can be added as an Alfresco 
global property (i.e. in `alfresco-global.properties`), or more simply as a Java system property. `JAVA_OPTS` may be 
used to set this if starting the repository with Docker:

```text
localTransform.<engineName>.url=
```

The `<engineName>` is a unique name of the T-Engine. For example, `localTransform.helloworld.url`. Typically, a T-Engine
contains a single transform or an associated group of transforms. Having set the URL to a T-Engine, the Repository will
update its configuration by requesting the [T-Engine configuration](https://github.com/Alfresco/acs-packaging/blob/master/docs/creating-a-t-engine.md#t-engine-configuration){:target="_blank"}
on a periodical basis. It is requested more frequently on start up or if a communication or configuration problem has
occurred, and less frequently otherwise:

```text
local.transform.service.cronExpression=4 30 0/1 * * ?
local.transform.service.initialAndOnError.cronExpression=0/10 * * * * ?
```
### Configure the Repository to use the Transform Service
The Transform service, including the T-Router, is disabled by default, but Docker Compose and Kubernetes Helm Charts
enable it again by setting `transform.service.enabled=true`. The Transform Service handles communication with all its
own T-Engines via the T-Router and builds up its own combined configuration JSON which is requested by the
Repository periodically.

```text
transform.service.enabled=true
transform.service.cronExpression=4 30 0/1 * * ?
transform.service.initialAndOnError.cronExpression=0/10 * * * * ?
```

### Enabling and disabling transforms
Local transforms or Transform Service transforms can be enabled or disabled independently of each other. The Repository 
will try to transform content using the Transform Service via the T-Router if possible and fall back to direct Local 
Transforms. If you are using Share, Local Transforms are required, as they support both synchronous and asynchronous 
requests. Share makes use of both, so functionality such as preview will be unavailable if Local transforms are disabled. 
The Transform service only supports asynchronous requests.

The following sections will show how to create a direct Local transform pipeline, a Local transform failover or a Local
transform override, but remember that they will not be used if the Transform Service (ATS) with the T-Router is able to 
do the transform and is enabled (i.e. in `alfresco-global.properties`):

```text
transform.service.enabled=true
local.transform.service.enabled=true
```

Setting the enabled state to `false` will disable all the transforms performed by that particular service. It is
possible to disable individual Local Transforms by setting the corresponding T-Engine URL property
`localTransform.<engineName>.url` value to an empty string:

```text
localTransform.helloworld.url=
```

### Deploying configurations
This section walks through where to deploy configurations for transform pipelines, renditions, and mimetypes.

#### Transform definition deployments
To deploy a configuration on the Repository side copy the JSON file, for example `custom_pipelines.json` into the 
`tomcat/shared/classes/alfresco/extension/transform/pipelines` directory. Then make sure `alfresco-global.properties` is 
configured with the default location for transform pipelines: 

```text
local.transform.pipeline.config.dir=shared/classes/alfresco/extension/transform/pipelines
```

On startup this location is checked every 10 seconds, but then switches to once an hour if successful. After a problem,
it tries every 10 seconds again. These are the same properties used to decide when to read T-Engine configurations,
because pipelines combine transformers in the T-Engines.

```text
local.transform.service.cronExpression=4 30 0/1 * * ?
local.transform.service.initialAndOnError.cronExpression=0/10 * * * * ?
```

If you are using Docker Compose in development, you will need to copy your pipeline definition into your running
Repository container. One way is to use the following command, and it will be picked up the next time the location is
read, which is dependent on the cron values.

```bash
docker cp custom_pipelines.json <alfresco container>:/usr/local/tomcat/shared/classes/alfresco/extension/transform/pipelines/
```

In a Kubernetes environment, [ConfigMaps](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/){:target="_blank"}
can be used to add pipeline definitions. You will need to create a `ConfigMap` from the JSON file and mount the ConfigMap
through a volume to the Repository pods.

```bash
kubectl create configmap custom-pipeline-config --from-file=custom_pipelines.json
```

The necessary volumes are already provided out of the box and the files in ConfigMap `custom-pipeline-config` will be mounted to
`/usr/local/tomcat/shared/classes/alfresco/extension/transform/pipelines/`. Again, the files will be picked up the next
time the location is read, or when the repository pods are restarted.

>**Note**: From Kubernetes documentation: Caution: If there are some files in the `mountPath` location, they will be deleted.

#### Rendition definition deployments
Just like Pipeline Definitions, custom Rendition Definitions need to be placed in a directory of the Repository. There are
similar properties that control where and when these definitions are read, and the same approach may be taken to get them
into Docker Compose and Kubernetes environments.

```text
rendition.config.dir=shared/classes/alfresco/extension/transform/renditions/
```

```text
rendition.config.cronExpression=2 30 0/1 * * ?
rendition.config.initialAndOnError.cronExpression=0/10 * * * * ?
```

In a Kubernetes environment:

```bash
kubectl create configmap custom-rendition-config --from-file=custom-renditions.json
```

#### Mimetype definition deployments
Just like Pipeline and Rendition Definitions, custom Mimetype Definitions need to be placed in a directory of the 
Repository. There are similar properties that control where and when these definitions are read, and the same approach 
may be taken to get them into Docker Compose and Kubernetes environments.

```text
mimetype.config.dir=shared/classes/alfresco/extension/mimetypes
```
```text
mimetype.config.cronExpression=0 30 0/1 * * ?
mimetype.config.initialAndOnError.cronExpression=0/10 * * * * ?
```

In a Kubernetes environment:

```bash
kubectl create configmap custom-mimetype-config --from-file=custom-mimetypes.json
```

The necessary volumes are already provided out of the box and the files in ConfigMap `custom-mimetype-config` will be
mounted to `/usr/local/tomcat/shared/classes/alfresco/extension/mimetypes`. Again, the files will be picked up the next
time the location is read, or when the repository pods are restarted.

## Deploying configurations to a T-Engine
To deploy configurations on the T-Engine side copy the JSON file, for example `custom_pipelines.json` into the T-Router 
container. This is usually done by creating a custom image via a `Dockerfile`. Then Export an environment variable 
pointing to the file location inside the container. 

The variable name should have this pattern: 

```text
TRANSFORMER_ROUTES_ADDITIONAL_<name>
```

The variable can be defined inside the container: 

```text
export TRANSFORMER_ROUTES_ADDITIONAL_HTML_VIA_TXT="/custom_pipelines.json"
```

Or by changing the Docker Compose file as shown below:

```text
transform-router:
  mem_limit: 512m
  image: quay.io/alfresco/alfresco-transform-router:4.1.0
  environment:
    JAVA_OPTS: " -XX:MinRAMPercentage=50 -XX:MaxRAMPercentage=80"
    ACTIVEMQ_URL: "nio://activemq:61616"
    TRANSFORMER_ROUTES_ADDITIONAL_HTML_VIA_TXT: "/custom_pipelines.json"
    CORE_AIO_URL : "http://transform-core-aio:8090"
    FILE_STORE_URL: "http://shared-file-store:8099/alfresco/api/-default-/private/sfs/versions/1/file"
  ports:
    - 8095:8095
  links:
    - activemq
```

## Transformer selection strategy
The Repository and the Transform Service T-Router uses the [T-Engine configuration](https://github.com/Alfresco/acs-packaging/blob/master/docs/creating-a-t-engine.md#t-engine-configuration){:target="_blank"}
in combination with their own pipeline files to choose which T-Engine will perform a transform. A transformer definition
contains a supported list of source and target Media Types. This is used for the most basic selection. This is further
refined by checking that the definition also supports transform options (parameters) that have been supplied in a
transform request, or a Rendition Definition used in a rendition request. See [Configure a Custom Rendition](#configure-a-custom-rendition).

```text
Transformer 1 defines options: Op1, Op2
Transformer 2 defines options: Op1, Op2, Op3, Op4
```

```text
Rendition provides values for options: Op2, Op3
```

If we assume that both transformers support the required source and target Media Types, Transformer 2 will be selected because
it knows about all the supplied options. The definition may also specify that some options are required or grouped.

The configuration may impose a source file size limit resulting in the selection of a different transformer. Size limits
are normally added to avoid the transforms consuming too many resources. The configuration may also specify a priority
which will be used in Transformer selection if there are a number of options. The highest priority is the one with the
lowest number.

## Configuring T-Engines
This section covers general JSON format for transform, rendition, and mimetype configurations applicable to the Repository 
and the T-Engines.

### Transform pipelines
Transformations may be combined in a pipeline to form a new transform, where the output from one becomes the
input to the next and so on. A pipeline definition (JSON) defines the sequence of transform steps and intermediate Media Types.
Like any other transformer, it specifies a list of supported source and target Media Types. If you don't supply any,
all possible combinations are assumed to be available. The definition may reuse the `transformOptions` of transformers in the
pipeline, but typically will define its own subset of these.

The following example begins with the `helloWorld` Transformer described in [Creating a T-Engine](https://github.com/Alfresco/acs-packaging/blob/23.1.0/docs/creating-a-t-engine.md){:target="_blank"},
which takes a text file containing a name and produces an HTML file with a `*`Hello <name>` message in the body. This is
then transformed back into a text file.

This example contains just one pipeline transformer, but many may be defined in the same file, such as 
`custom_pipelines.json`:

```json
{
  "transformers": [
    {
      "transformerName": "helloWorldText",
      "transformerPipeline" : [
        {"transformerName": "helloWorld", "targetMediaType": "text/html"},
        {"transformerName": "html"}
      ],
      "supportedSourceAndTargetList": [
        {"sourceMediaType": "text/plain", "priority": 45,  "targetMediaType": "text/plain" }
      ],
      "transformOptions": [
        "helloWorldOptions"
      ]
    }
  ]
}
```

* `transformerName` - Unique name for the transform.
* `transformerPipeline` - A list of transformers in the pipeline. The `targetMediaType` specifies the intermediate
  Media Types between transformers. There is no final `targetMediaType` as this comes from the `supportedSourceAndTargetList`.
* `supportedSourceAndTargetList` - The supported source and target Media Types, which refer to the Media Types this
  pipeline transformer can transform from and to, additionally you can set the priority and the
  `maxSourceSizeBytes` see [Supported Source and Target List](https://github.com/Alfresco/alfresco-transform-core/blob/master/docs/engine_config.md#supported-source-and-target-list){:target="_blank"}.
  If blank, this indicates that all possible combinations are supported. This is the cartesian product of all source types to the first
  intermediate type and all target types from the last intermediate type. Any combinations supported by the first transformer are excluded. They
  will also have the priority from the first transform.
* `transformOptions` - A list of references to options required by the pipeline transformer.

### Failover transform pipelines
A failover transform simply provides a list of transforms to be attempted one after another until one succeeds. For
example, you may have a fast transform that is able to handle a limited set of transforms and another that is slower
but handles all cases.

```json
{
  "transformers": [
    {
      "transformerName": "imgExtractOrImgCreate",
      "transformerFailover" : [ "imgExtract", "imgCreate" ],
      "supportedSourceAndTargetList": [
        {"sourceMediaType": "application/vnd.oasis.opendocument.graphics", "priority": 150, "targetMediaType": "image/png" },
        ...
        {"sourceMediaType": "application/vnd.sun.xml.calc.template",       "priority": 150, "targetMediaType": "image/png" }
      ]
    }
  ]
}
```

* `transformerName` - Unique name for the transform.
* `transformerFaillover` - A list of transformers to try.
* `supportedSourceAndTargetList` - The supported source and target Media Types, which refer to the Media Types this 
  failover transformer can transform from and to, additionally you can set the priority and the `maxSourceSizeBytes` 
  see [Supported Source and Target List](https://github.com/Alfresco/alfresco-transform-core/blob/master/docs/engine_config.md#supported-source-and-target-list){:target="_blank"}.
  Unlike pipelines, it must not be blank.
* `transformOptions` - A list of references to options required by the pipeline transformer.

### Adding pipelines and failover transforms to a T-Engine
So far we have talked about defining pipelines and failover transforms in the Repository or the Transfrom Service T-Router 
pipeline files. It is also possible to add them to a T-Engine's configuration, even when they reference a transformer 
provided by another T-Engine. It is only when all transform steps exist that the pipeline or failover transform becomes 
available. Warning messages will be issued if step transforms do not exist.

Generally it is better to add them to T-Engines to avoid having to add an identical entry to both the Repository and 
Transfrom Service T-Router pipeline files.

### Modifying existing pipeline configurations
The Repository and the Transfrom Service T-Router reads the configuration from T-Engines and then their own pipeline
files. The T-Engine order is based on the `<engineName>` and the pipeline file order is based on the filenames. As 
sorting is alphanumeric, you may wish to consider using a fixed length numeric prefix.

For example:

```text
localTransform.imagemagick.url=http://localhost:8091/
localTransform.libreoffice.url=http://localhost:8092/
localTransform.misc.url=http://localhost:8094/
localTransform.pdfrenderer.url=http://localhost:8090/
localTransform.tika.url=http://localhost:8093/

shared/classes/alfresco/extension/transform/pipelines/0100-basePipelines.json
shared/classes/alfresco/extension/transform/pipelines/0200-a-cutdown-libreoffice.json
```

The following sections describe ways to modify the configuration that has already been read. This may be added to
T-Engine or pipeline files.

#### Overriding transform pipelines
It is possible to override a previously defined transform definition. The following example
removes most of the supported source to target media types from the standard `libreoffice`
transform. It also changes the max size and priority of others. This is not something you would normally want to do.

```json
{
  "transformers": [
    {
      "transformerName": "libreoffice",
      "supportedSourceAndTargetList": [
        {"sourceMediaType": "text/csv", "maxSourceSizeBytes": 1000, "targetMediaType": "text/html" },
        {"sourceMediaType": "text/csv", "targetMediaType": "application/vnd.oasis.opendocument.spreadsheet" },
        {"sourceMediaType": "text/csv", "targetMediaType": "application/vnd.oasis.opendocument.spreadsheet-template" },
        {"sourceMediaType": "text/csv", "targetMediaType": "text/tab-separated-values" },
        {"sourceMediaType": "text/csv", "priority": 45, "targetMediaType": "application/vnd.ms-excel" },
        {"sourceMediaType": "text/csv", "priority": 155, "targetMediaType": "application/pdf" }
      ]
    }
  ]
}
```

#### Removing a transformer
To discard a previous transformer definition include its name in the optional `"removeTransformers"` list. You might 
want to do this if you have a replacement and wish to keep the overall configuration simple (so it contains no alternatives), 
or you wish to temporarily remove it. The following example removes two transformers before processing any other 
configuration in the same T-Engine or pipeline file.

```json
{
  "removeTransformers" : [
    "libreoffice",
    "Archive"
   ]
  ...
}
```

#### Overriding the supportedSourceAndTargetList
Rather than totally override an existing transform definition from another T-Engine or pipeline file, it is generally 
simpler to modify the `"supportedSourceAndTargetList"` by adding elements to the optional `"addSupported"`, 
`"removeSupported"` and `"overrideSupported"` lists. You will need to specify the `"transformerName"` but you will not 
need to repeat all the other `"supportedSourceAndTargetList"` values, which means if there are changes in the original, 
the same change is not needed in a second place.

The following example adds one transform, removes two others and changes the `"priority"` and `"maxSourceSizeBytes"` of
another. This is done before processing any other configuration in the same T-Engine or pipeline file:

```json
{
  "addSupported": [
    {
      "transformerName": "Archive",
      "sourceMediaType": "application/zip",
      "targetMediaType": "text/csv",
      "priority": 60,
      "maxSourceSizeBytes": 18874368
    }
  ],
  "removeSupported": [
    {
      "transformerName": "Archive",
      "sourceMediaType": "application/zip",
      "targetMediaType": "text/xml"
    },
    {
      "transformerName": "Archive",
      "sourceMediaType": "application/zip",
      "targetMediaType": "text/plain"
    }
  ],
  "overrideSupported": [
    {
      "transformerName": "Archive",
      "sourceMediaType": "application/zip",
      "targetMediaType": "text/html",
      "priority": 60,
      "maxSourceSizeBytes": 18874368
    }
  ]
  ...
}
```

#### Default maxSourceSizeBytes and priority values
When defining `"supportedSourceAndTargetList"` elements the `"priority"` and `"maxSourceSizeBytes"` are optional
and normally have the default values of `50` and `-1` (no limit). It is possible to change those defaults. In precedence 
order from most specific to most general these are defined by combinations of `"transformerName"` and `"sourceMediaType"`.

* `transformer and source media type default` - both specified
* `transformer default` - only the transformer name is specified
* `source media type default` - only the source media type is specified
* `system wide default` - neither are specified.

Both `"priority"` and `"maxSourceSizeBytes"` may be specified in an element, but if only one is specified it is only that 
value that is being defaulted.

Being able to change the defaults is particularly useful once a T-Engine has been developed as it allows a system 
administrator to handle limitations that are only found later. The `system wide defaults` are generally not used but are 
included for completeness.

The following example says that the `"Office"` transformer by default should only handle zip files up to 18 Mb and by
default the maximum size of a `.doc` file to be transformed is 4 Mb. The third example defaults the priority,
possibly allowing another transformer that has specified a priority of say `50` to be used in
preference.

Defaults values are only applied after T-Engine and pipeline files have been read.

```json
{
  "supportedDefaults": [
    {
      "transformerName": "Office",             // default for a source type within a transformer
      "sourceMediaType": "application/zip",
      "maxSourceSizeBytes": 18874368
    },
    {
      "sourceMediaType": "application/msword", // defaults for a source type
      "maxSourceSizeBytes": 4194304,
      "priority": 45
    },
    {
      "priority": 60                           // system wide default
    },
    {
      "maxSourceSizeBytes": -1                 // system wide default
    }
  ]
  ...
}
```
### Configure a custom rendition {#configure-a-custom-rendition}
Renditions are a representation of source content in another form. A Rendition Definition (JSON) defines the transform 
option (parameter) values that will be passed to a transformer and the target Media Type:

```json
{
  "renditions": [
    {
      "renditionName": "helloWorld",
      "targetMediaType": "text/html",
      "options": [
        {"name": "language", "value": "German"}
      ]
    }
  ]
}
```

* `renditionName` - A unique rendition name.
* `targetMediaType` - The target Media Type for the rendition.
* `options` - The list of transform option names and values corresponding to the transform options defined in
  [T-Engine configuration](https://github.com/Alfresco/acs-packaging/blob/master/docs/creating-a-t-engine.md#t-engine-configuration){:target="_blank"}.
  If you specify `sourceNodeRef` without a value, the system will automatically add the values at run time.
  
#### Disabling an existing rendition
Just like transforms, it is possible to override renditions. The following example effectively disables the `doclib` 
rendition, used to create the thumbnail images in Share's Document Library page and other client applications. A good 
name for this file might be `0200-disableDoclib.json`.

```json
{
  "renditions": [
    {
      "renditionName": "doclib",
      "targetMediaType": "image/png",
      "options": [
        {"name": "unsupported", "value": 123}
      ]
    }
  ]
}
```

Because there is not a transformer with a transform option called `unsupported`, the rendition can never be performed. 
Having turned on `TransformerDebug` logging you normally would see a transform taking place for `-- doclib --` when 
you upload a file in Share. With this override the doclib transform does not appear.

#### Overriding an existing rendition
It is possible to change a rendition by overriding it. The following `0300-biggerThumbnails.json` file changes the size 
of the `doclib` image from `100x100` to be `123x123` and introduces another rendition called `biggerThumbnail` that is 
`200x200`:

```json
{
  "renditions": [
    {
      "renditionName": "doclib",
      "targetMediaType": "image/png",
      "options": [
        {"name": "resizeWidth", "value": 123},
        {"name": "resizeHeight", "value": 123},
        {"name": "allowEnlargement", "value": false},
        {"name": "maintainAspectRatio", "value": true},
        {"name": "autoOrient", "value": true},
        {"name": "thumbnail", "value": true}
      ]
    },
    {
      "renditionName": "biggerThumbnail",
      "targetMediaType": "image/png",
      "options": [
        {"name": "resizeWidth", "value": 200},
        {"name": "resizeHeight", "value": 200},
        {"name": "allowEnlargement", "value": false},
        {"name": "maintainAspectRatio", "value": true},
        {"name": "autoOrient", "value": true},
        {"name": "thumbnail", "value": true}
      ]
    }
  ]
}
```

### Configure a custom MIME type
Quite often the reason a custom transform is created is to convert to or from a MIME type (or Media type) that is not 
known to Alfresco Content Services by default. Another reason is to introduce an application specific MIME type that
indicates a specific use of a more general format such as XML or JSON.

From Alfresco Content Services 6.2, it is possible add custom MIME types in a similar way to custom Pipelines and 
Renditions. The JSON format and properties are as follows:

```json
{
  "mediaTypes": [
    {
      "name": "MPEG4 Audio",
      "mediaType": "audio/mp4",
      "extensions": [
        {"extension": "m4a"}
      ]
    },
    {
      "name": "Plain Text",
      "mediaType": "text/plain",
      "text": true,
      "extensions": [
        {"extension": "txt", "default": true},
        {"extension": "sql", "name": "SQL"},
        {"extension": "properties", "name": "Java Properties"},
        {"extension": "log", "name": "Log File"}
      ]
    }
  ]
}
```

* `name` Display name of the mimetype or file extension. Optional for extensions.
* `mediaType` used to identify the content.
* `text` optional value indicating if the mimetype is text based.
* `extensions` a list of possible extensions.
* `extension` the file extension.
* `default` indicates the extension is the default one if there is more than one.


---
title: Install Transform Service
---

This release provides two main options for deployment: 

* [Distribution zip](#prereq-non-containerized-deploy) - The Transform Service zip can be applied when installing 
  Alfresco Content Services using the distribution zip. For an overview of components, see the first picture on this 
  [page]({% link transform-service/latest/index.md %}). 
* [Containerized deployment(Docker or Kubernetes)](#containerized-deployments). The Transform Service is also deployed 
  as part of the Content Services containerized deployment using Docker images that are referenced from Helm charts. 
  These charts are a deployment template that can be used as the basis for your specific deployment needs.
  For an overview of components, see the second picture on this [page]({% link transform-service/latest/index.md %}).
  
>**Note:** Deployment of Transform Service with Content Services on AWS, such as Amazon EKS (Elastic Kubernetes Service), 
>is recommended only for customers with a good knowledge of Content Services, and strong competencies in AWS and 
>containerized deployment.

## Prerequisites
There are a number of software requirements for installing the Transform Service.

The Transform Service is only deployed by default as part of Content Services for containerized deployments.

However, this is not the case if you're installing Content Services using the distribution zip. 
See [Supported platforms]({% link transform-service/latest/support/index.md %}) for more information.

### Containerized deployments {#containerized-deployments}
The images downloaded directly from [Docker Hub](https://hub.docker.com/u/alfresco/){:target="_blank"}, or 
[Quay.io](https://quay.io/){:target="_blank"} are for a limited trial of the Enterprise version of Content Services that 
goes into read-only mode after 2 days. For a longer (30-day) trial, get the Alfresco Content Services 
[Download Trial](https://www.hyland.com/en/resources/alfresco-ecm-download){:target="_blank"}.

> **Note:** A [Quay.io](https://quay.io/) account is needed to pull the Docker images that are needed for the Transform Service:
>
> * `quay.io/alfresco/alfresco-transform-router`
> * `quay.io/alfresco/alfresco-shared-file-store`

The Transform Core Engine (T-Engine) Docker Image is also used by Alfresco Content Services Community Edition, so it is 
available in Docker Hub:

* `alfresco/alfresco-transform-core-aio`

#### Software requirements (Helm)
To use the Content Services deployment (including the Transform Service), you need to install the following software:

* [AWS CLI](https://github.com/aws/aws-cli#installation){:target="_blank"} - the command line interface for Amazon Web Services.
* [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/){:target="_blank"} - the command line tool for Kubernetes.
* [Helm](https://github.com/helm/helm#install){:target="_blank"} - the tool for installing and managing Kubernetes applications.
  * There are Helm charts that allow you to deploy Content Services with Transform Service in a Kubernetes cluster, for example, on AWS.

See [Install with Helm charts]({% link transform-service/latest/install/index.md %}#install-with-helm-charts) for more details.

#### Software requirements (Docker)
This is recommended for evaluations only (i.e. test and development environments).

* [Docker](https://docs.docker.com/install/){:target="_blank"} (latest stable version)
  * This allows you to run Docker images and `docker-compose` on a single computer.
* [Docker Compose](https://docs.docker.com/compose/install/){:target="_blank"}
  * Docker Compose is included as part of some Docker installers. If it's not part of your installation, then install it 
    separately after you've installed Docker.

>**Note:** Check the prerequisites for your operating system, both for Docker and Docker Compose.

See [Install with Docker Compose]({% link transform-service/latest/install/index.md %}#install-with-docker-compose) for more details.

### Non-containerized deployment {#prereq-non-containerized-deploy}
Before installing Transform Service from the distribution ZIP file, 
[install Alfresco Content Services using distribution ZIP]({% link content-services/latest/install/zip/index.md %}).
This will also install the ActiveMQ message broker, which is used by the Transform Service.

In a non-containerized environment you need to install the following software before installing Transform Service:

* LibreOffice: see [Install LibreOffice](#install-libreoffice)
* ImageMagick: see [Install ImageMagick](#install-imagemagick)
* alfresco-pdf-renderer: see [Install alfresco-pdf renderer](#install-pdf-renderer)
* Exiftool: see [Install Exiftool](#install-exiftool)

You can install the third-party software used by the Transform Service independently.

#### Install LibreOffice {#install-libreoffice}
With the Transform Service, you can transform a document from one format to another, for example, a text file to a PDF 
file. To access these transformation facilities, you must install LibreOffice.

1. Browse to the LibreOffice download site: [LibreOffice download site](https://www.libreoffice.org/download/download/){:target="_blank"}
2. Download the latest (stable) version of LibreOffice for your platform.
3. When prompted, specify a download destination.
4. Browse to the location of your downloaded file, and install the application.
5. Change the installation directory to:
    * (Windows) `c:\Alfresco\LibreOffice`
    * (Linux) `/opt/alfresco/LibreOffice`
   If you're installing LibreOffice on Linux, you also need a number of libraries to be installed. See [Install Linux libraries](#install-linux-libraries) for more.

##### Install Linux libraries {#install-linux-libraries}
Use this information to install Linux libraries manually on supported Linux distributions, such as Ubuntu, SUSE and Red Hat.

LibreOffice requires the following libraries to be installed on your system:

* libfontconfig
* libICE
* libSM
* libXrender
* libXext
* libXinerama
* libcups
* libGLU
* libcairo2
* libgl1-mesa-glx

If the required libraries are missing, you'll get a warning message. You can install them using your preferred package 
manager from the command line. Note that the file names for the Linux libraries may vary by distribution.

For Red Hat Enterprise Linux/CentOS, you can run:

```bash
cd <libre-install-dir>/LibreOffice_*.*.*.*_Linux_x86-64_rpm/RPMS/
```

```bash
sudo yum localinstall *rpm
```

For Ubuntu:

```bash
cd <libre-install-dir>/LibreOffice_*.*.*.*_Linux_x86-64_rpm/RPMS/
```

```bash
sudo dpkg -i *deb
```

If LibreOffice doesn't start up normally with Transform Service, test it manually, for example, by running this startup script:

```bash
start ex. {installdir}/libreoffice/scripts/libreoffice_ctl.sh start
status ex. {installdir}/libreoffice/scripts/libreoffice_ctl.sh status
```

If you receive errors that indicate that a library is missing, work with your system administrator to add the missing 
library or its equivalent from your configured repositories.

#### Install ImageMagick {#install-imagemagick}
To enable image manipulation in Transform Service, you must install and configure ImageMagick. Transform Service uses 
ImageMagick to manipulate images for previewing.

1. Check if ImageMagick is already installed on your system.
   Use the ImageMagick convert command to check that you have the right software installed on your machine. This command is usually located in `/usr/bin`: `install Image`.
2. If the ImageMagick software isn't available on your system, download and install the appropriate package for your platform.
   To download ImageMagick, browse to [ImageMagick download website](https://www.imagemagick.org/script/download.php){:target="_blank"}.

   > **Note:** In next steps, you'll make changes to the Content Services configuration files to enable the manually installed ImageMagick application. These steps can only be performed after Content Services has been installed.

The following table lists example of how to set the paths to different things when starting Transform Core AIO later on:

   |Property|Description|
   |--------|-----------|
   |img.root| Windows: `img.root=C:\\ImageMagick`<br>Linux: `img.root=/ImageMagick`<br><br>**Note:** Don't include a slash (`/`) at the end of the path, i.e. `/ImageMagick/`.|
   |img.dyn|Windows: `img.dyn=${img.root}\\lib` <br>Linux: `img.dyn=${img.root}/lib`|
   |img.exe|Windows: `img.exe=${img.root}\\convert.exe` <br>Linux: `img.exe=${img.root}/bin/convert`|
   |img.coders|Windows: `img.coders=${img.root}\\modules\\coders` <br>Linux: `img.coders=${img.root}/modules/coders`|
   |img.config|Windows: `img.config=${img.root}\\config` <br>Linux: `img.config=${img.root}/config`|
   |img.url|Windows: `img.url=${img.root}\\url` <br>Linux: `img.url=${img.root}/url`|

> **Note:** Test that you're able to convert a PDF using the command: `convert filename.pdf[0] filename.png`

#### Install alfresco-pdf-renderer {#install-pdf-renderer}
Transform Service uses `alfresco-pdf-renderer` for creating document thumbnails and previews. Use this information to 
install `alfresco-pdf-renderer` on your system.

>**Note:** The `alfresco-pdf-renderer` executable file is platform-specific. You can download the binaries from our Nexus repository.

* For Windows:
    * Download [alfresco-pdf-renderer-1.1-win64.tgz](https://artifacts.alfresco.com/nexus/content/groups/public/org/alfresco/alfresco-pdf-renderer/1.1/alfresco-pdf-renderer-1.1-win64.tgz).
    * Browse to the location of your saved file and extract the archive to a location of your choice.
    * Note down the exe path: `<alfresco-pdf-renderer_installation_dir>/alfresco-pdf-renderer`.

* For Linux:
    * Download [alfresco-pdf-renderer-1.1-linux.tgz](https://nexus.alfresco.com/nexus/service/local/repositories/releases/content/org/alfresco/alfresco-pdf-renderer/1.1/alfresco-pdf-renderer-1.1-linux.tgz).
    * Browse to the location of your saved file and extract the archive to a location of your choice.
    * Note down the exe path: `<alfresco-pdf-renderer_installation_dir>/alfresco-pdf-renderer`.

#### Install ExifTool {#install-exiftool}
Transform Service uses the [ExifTool](https://exiftool.org/){:target="_blank"} for metadata extraction. It is used by 
Apache Tika for extracting image metadata if the auto-detect parser is enabled, which automatically figures out what 
kind of content you have, then calls the appropriate parser for you.

Download version 12.25 of the ExifTool from [Alfresco Nexus Server](https://nexus.alfresco.com/nexus/service/local/repositories/thirdparty/content/org/exiftool/image-exiftool/12.25/image-exiftool-12.25.tgz){:target="_blank"}

See this [ExifTool page](https://exiftool.org/install.html){:target="_blank"} for installation instructions.

The steps to install are:

* Download exiftool
* Unzip exiftool
* ExifTool needs to then be installed globally

Example installation based on a downloaded `image-exiftool-12.25.tgz` file:

Create a new directory named `exiftool` under your Alfresco installation, such as `/usr/local/acs74` directory.

```bash
$ sudo mkdir /usr/local/acs74/exiftool
```

Extract `~/Downloads/image-exiftool-12.25.tgz` and copy the contents of `~/Downloads/Image-ExifTool-12.25` into the 
`/usr/local/acs74/exiftool/` directory:

```bash
$ sudo tar -xvf ~/Downloads/image-exiftool-12.25.tgz --directory ~/Downloads/
$ sudo cp -R ~/Downloads/Image-ExifTool-12.25/* /usr/local/acs74/exiftool/
```

Export the `exiftool` directory to the `PATH` variable:

```bash
export PATH=$PATH:/usr/local/acs74/exiftool
```

Update the file permissions for `/usr/local/acs74/exiftool` directory:

```bash
$ sudo chgrp -R Alfresco /usr/local/acs74/exiftool
$ sudo chmod -R 755 /usr/local/acs74/exiftool
```

## Install with Helm charts
Use this information to deploy Content Services (including the Transform Service) using Helm charts by running a 
Kubernetes cluster on Amazon Web Services (AWS). These charts are a deployment template which can be used as the basis 
for your specific deployment needs.

The Helm charts are provided as a reference that can be used to build deployments in AWS. If you're a System administrator, 
ensure that data persistence, backups, log storage, and other system-level functions have been configured to meet your needs.

You'll need your [Quay.io](https://quay.io){:target="_blank"} account credentials to access the Docker images. If you 
don't already have these credentials, contact [Alfresco Support](https://support.alfresco.com/){:target="_blank"}.

Here is a summary of the steps required:

1. Set up your Kubernetes cluster on AWS.
2. Install the Kubernetes Dashboard to manage your Kubernetes cluster.
3. Set up Content Services on the Kubernetes cluster, including creating file storage.
4. To access the images in [Quay.io](https://quay.io/){:target="_blank"}, you'll need to generate a pull secret and apply it to your cluster.
5. Deploy Content Services.

    > **Note:** Remember to pass the name of the secret as an extra `--set` argument in the `helm install` command.

6. Check the status of your deployment.

See the [Alfresco/acs-deployment](https://github.com/Alfresco/acs-deployment/){:target="_blank"} GitHub project 
documentation for the prerequisites and detailed setup:

* [Deploying with Helm charts on AWS using EKS](https://github.com/Alfresco/acs-deployment/blob/master/docs/helm/eks-deployment.md){:target="_blank"}

## Install with Docker Compose
Use this information to quickly start up Content Services (including Transform Service) using Docker Compose. Due to the 
limited capabilities of Docker Compose, this deployment method is only recommended for development and test environments.

To check which branch tag corresponds to a specific Content Services release, review the 
[released versions](https://github.com/Alfresco/acs-deployment#versioning){:target="_blank"} in GitHub. Choose a version 
from the left column that corresponds to the required Content Services version you want to deploy.

   > **Note:** Check the prerequisites for your operating system, both for Docker and Docker Compose, using the links provided.

1. Download [one of the Docker Compose files](https://github.com/Alfresco/acs-deployment/tree/master/docker-compose/){:target="_blank"} from the `acs-deployment` repository, and navigate to the folder where the file is saved.

    Alternatively, if you want to contribute to the open source code, you can use one of the options provided in the **Code** dropdown of the [main repository page](https://github.com/Alfresco/acs-deployment/tree/master){:target="_blank"}. These options are **Clone** the repository, **Open with GitHub Desktop**, or **Download ZIP** to save a copy of the code. For example, if you want to see the latest release code for Content Services 23.x, then select tag `v8.0.0`.

    > **Note:** Make sure that exposed ports are open on your host computer. Check the `docker-compose.yml` file to 
    > determine the exposed ports - refer to the `host:container` port definitions. You'll see they include 5432, 8080, 
    > 8083 and others.

2. Log in to Quay.io using your credentials:

    ```bash
    docker login https://quay.io
    ```

    You'll need your [Quay.io](https://quay.io){:target="_blank"} account credentials to access the Docker images. If 
    you don't already have these credentials, contact [Alfresco Support](https://support.alfresco.com/){:target="_blank"}.

3. (OPTIONAL) Make sure the Docker Compose file uses the following versions of Transform Router, Transform Core AIO T-Engine, and Shared file store:

   ```yaml
   transform-router:
     mem_limit: 512m
     image: quay.io/alfresco/alfresco-transform-router:4.1.0
     environment:
       JAVA_OPTS: " -XX:MinRAMPercentage=50 -XX:MaxRAMPercentage=80"
       ACTIVEMQ_URL: "nio://activemq:61616"
       CORE_AIO_URL: "http://transform-core-aio:8090"
       FILE_STORE_URL: "http://shared-file-store:8099/alfresco/api/-default-/private/sfs/versions/1/file"
     ports:
       - "8095:8095"
     links:
       - activemq

   transform-core-aio:
     image: alfresco/alfresco-transform-core-aio:5.1.0
     mem_limit: 1536m
     environment:
       JAVA_OPTS: " -XX:MinRAMPercentage=50 -XX:MaxRAMPercentage=80"
       ACTIVEMQ_URL: "nio://activemq:61616"
       FILE_STORE_URL: "http://shared-file-store:8099/alfresco/api/-default-/private/sfs/versions/1/file"
     ports:
       - "8090:8090"
     links:
       - activemq
   
   shared-file-store:
     image: quay.io/alfresco/alfresco-shared-file-store:4.1.0
     mem_limit: 512m
     environment:
       JAVA_OPTS: " -XX:MinRAMPercentage=50 -XX:MaxRAMPercentage=80"
       scheduler.content.age.millis: 86400000
       scheduler.cleanup.interval: 86400000
     ports:
       - "8099:8099"
     volumes:
       - shared-file-store-volume:/tmp/Alfresco/sfs
   ```

4. Deploy Content Services, including the repository, Share, Postgres database, Search Services, and Transform Service:

    ```bash
    docker-compose up
    ```

    This downloads the images, fetches all the dependencies, creates each container, and then starts the system:

    ```bash
    Creating network "docker-compose_default" with the default driver
    Creating docker-compose-digital-workspace-1 ... done
    Creating docker-compose-solr6-1             ... done
    Creating docker-compose-shared-file-store-1 ... done
    Creating docker-compose-sync-service-1      ... done
    Creating docker-compose-alfresco-1          ... done
    Creating docker-compose-control-center-1    ... done
    Creating docker-compose-share-1             ... done
    Creating docker-compose-postgres-1          ... done
    Creating docker-compose-activemq-1          ... done
    Creating docker-compose-proxy-1              ... done
    Creating docker-compose-transform-router-1   ... done
    Creating docker-compose-transform-core-aio-1 ... done
    Attaching to docker-compose-digital-workspace-1, docker-compose-shared-file-store-1, docker-compose-alfresco-1, ...
    ```

    As an alternative, you can also start the containers in the background by running `docker-compose up -d`.

5. Wait for the logs to show messages:

    ```bash
    ...
    docker-compose-alfresco-1 | ... INFO  [service.descriptor.DescriptorService] [main] Alfresco license: Creating time limited trial license
    docker-compose-alfresco-1 | ... WARN  [repo.usage.RepoUsageMonitor] [main] The Alfresco Content Services license will expire in 2 days.
    ...
    docker-compose-alfresco-1 | ... INFO ... Starting 'Transformers' subsystem, ID: [Transformers, default]
    docker-compose-alfresco-1 | ... INFO ... Startup of 'Transformers' subsystem, ID: [Transformers, default] complete
    ```

    If you encounter errors whilst the system is starting up:

    * Stop the session (by using `CONTROL+C`).
    * Remove the container using `--rmi all`. This option also removes the images created by docker-compose up, and the images used by any service. You can use this, for example, if any containers fail and you need to remove them.
    * Try allocating more memory resources, as advised in `docker-compose.yml`. For example, in Docker, change the memory setting in **Preferences** (or **Settings**) > **Advanced** > **Memory**, to at least 8GB. Make sure you restart Docker and wait for the process to finish before continuing.
    * Go back to step 5 in the initial Docker Compose instructions to start the deployment again.

    > **Note:** You'll need a machine with at least 13GB of memory to distribute among the Docker containers.

6. Open your browser and check everything starts up correctly:

    | Service | Endpoint |
    | ------- | -------- |
    | Administration and REST APIs | `http://localhost:8080/alfresco` |
    | Share | `http://localhost:8080/share` |
    | Digital Workspace | `http://localhost:8080/workspace` |
    | Search Services administration (see [this page]({% link content-services/latest/install/containers/docker-compose.md %}) for info on how to login)| `http://localhost:8083/solr` |
    | Transform Router configuration | `http://localhost:8095/transform/config` |
    | ActiveMQ Admin Web Console | `http://localhost:8161/admin` |

7. Log in as the `admin` user. Enter the default administrator password `admin`.

You can use a number of commands to check that the system started correctly, see below.

See the [Alfresco/acs-deployment](https://github.com/Alfresco/acs-deployment/tree/master/docs/docker-compose) GitHub project 
documentation for the prerequisites and detailed setup.

### Check system start up
Use this information to verify that the system started correctly, and to clean up the deployment.

1. Open a new terminal window.

2. Change directory to the `docker-compose` folder that you created in the deployment steps.

3. Verify that all the services started correctly.

    1. List the images and additional details:

        ```bash
        docker-compose images
        ```

        You should see a list of the services defined in your `docker-compose.yaml` file:

        ```bash
        Container                             Repository                                     Tag                        Image Id         Size
        --------------------------------------------------------------------------------------------------------------------------------------- 
        docker-compose-activemq-1             alfresco/alfresco-activemq                     5.18-jre17-rockylinux8   8d025606b35f        686MB
        docker-compose-alfresco-1             quay.io/alfresco/alfresco-content-repository   23.2.1                   c50a76324708        1.15GB
        docker-compose-control-center-1       quay.io/alfresco/alfresco-control-center       8.4.1                    9f7f1ce0ba60        43.2MB
        docker-compose-digital-workspace-1    quay.io/alfresco/alfresco-digital-workspace    4.4.1                    bb6bda03b42e        47.5MB
        docker-compose-postgres-1             postgres                                       14.4                     fb7289787ade        355MB
        docker-compose-proxy-1                alfresco/alfresco-acs-nginx                    3.4.2                    f9c4519b7920        23.4MB
        docker-compose-share-1                quay.io/alfresco/alfresco-share                23.2.1                   f4063f4d7a62        715MB
        docker-compose-shared-file-store-1    quay.io/alfresco/alfresco-shared-file-store    4.1.0                    ac8ce4ddeeb7        567MB
        docker-compose-solr6-1                quay.io/alfresco/search-services               2.0.8.2                  be4b827d934a        835MB
        docker-compose-sync-service-1         quay.io/alfresco/service-sync                  4.0.1                    cb8e65443e11        719MB
        docker-compose-transform-core-aio-1   alfresco/alfresco-transform-core-aio           5.1.0                    448b02b47f7d        1.67GB
        docker-compose-transform-router-1     quay.io/alfresco/alfresco-transform-router     4.1.0                    bcdf3867f26c        598MB
        ```

        > **Note:** The Docker images listed above are based on an updated Docker Compose file, using the code snippet from step 3 in the initial Docker Compose instructions.

    2. List the running containers:

        ```bash
        docker-compose ps
        ```

        You should see a list of the services defined in the `docker-compose.yaml` file.

    3. View the log files for each service `<service-name>`, or container `<container-name>`:

        ```bash
        docker-compose logs <service-name>
        docker container logs `<container-name>`
        ```

        For example, to check the logs for Share, run any of the following commands:

        ```bash
        docker-compose logs share
        docker container logs docker-compose-share-1
        ```

        You can add an optional parameter `--tail=25` before `<container-name>` to display the last 25 lines of the 
        logs for the selected container.

        ```bash
        docker container logs --tail=25 docker-compose-share-1
        ```

        Check for a success message:

        ```bash
        Successfully retrieved license information from Alfresco.
        ```

    Once you've tested the services, you can clean up the deployment by stopping the running services.

4. Stop the session by using `CONTROL+C` in the same window as the running services:

    ```bash
    ^CGracefully stopping... (press Ctrl+C again to force)
    Stopping docker-compose-transform-core-aio-1 ... done
    Stopping docker-compose-transform-router-1   ... done
    Stopping docker-compose-proxy-1              ... done
    Stopping docker-compose-sync-service-1       ... done
    Stopping docker-compose-shared-file-store-1  ... done
    Stopping docker-compose-postgres-1           ... done
    Stopping docker-compose-activemq-1           ... done
    Stopping docker-compose-control-center-1     ... done
    Stopping docker-compose-share-1              ... done
    Stopping docker-compose-solr6-1              ... done
    Stopping docker-compose-alfresco-1           ... done
    Stopping docker-compose-digital-workspace-1  ... done
    ```

5. Alternatively, you can open a new terminal window, change directory to the `docker-compose` folder, and run:

    ```bash
    docker-compose down
    ```

    This stops the running services, as shown in the previous example, and removes them from memory:

    ```bash
    Stopping docker-compose-transform-core-aio-1 ... done
    ...
    Stopping docker-compose-digital-workspace-1  ... done
    Removing docker-compose-transform-core-aio-1 ... done
    ...
    Removing docker-compose-digital-workspace-1  ... done
    Removing network docker-compose_default
    ```

6. You can use a few more commands to explore the services when they're running. Change directory to `docker-compose` 
   before running these:

    1. Stop all the running containers:

        ```bash
        docker-compose stop
        ```

    2. Restart the containers (after using the `stop` command):

        ```bash
        docker-compose restart
        ```

    3. Starts the containers that were started with `docker-compose up`:

        ```bash
        docker-compose start
        ```

    4. Stop all running containers, and remove them and the network:

        ```bash
        docker-compose down [--rmi all]
        ```

        The `--rmi all` option also removes the images created by `docker-compose up`, and the images used by any service. 
        You can use this, for example, if any containers fail and you need to remove them.

See the [Docker documentation](https://docs.docker.com/){:target="_blank"} for more on getting started with Docker and using Docker.

## Install with zip
Use these instructions to install the Transform Service using the distribution zip and connect it to an instance of 
Alfresco Content Services.

The Transform Service distribution zip file includes all the files required to provide the transformation and 
metadata extraction capabilities. Ensure that you've installed the [prerequisites](#prereq-non-containerized-deploy) 
before continuing.

1. Browse to [Hyland Community](https://community.hyland.com/){:target="_blank"} and download 
   `alfresco-transform-service-distribution-4.1.x.zip`.

2. Extract the zip file into a system directory; for example, `<installLocation>/`.

    In this directory you'll see the following content including three runnable JAR files:

    * `alfresco-shared-file-store-controller-4.1.x.jar`
    * `alfresco-transform-core-aio-boot-5.1.x.jar`
    * `alfresco-transform-router-4.1.x.jar`
    * `README.md`
    * IPTC Content Model
      * Needs to be bootstrapped into Alfresco Content Services for IPTC Metadata extraction to work, unless you are using Alfresco Content Services version 7.1.0+. See [Supported platforms]({% link transform-service/latest/support/index.md %}) for more information.

3. Start Active MQ.

    For example, run the following command from the ActiveMQ installation directory:

    ```bash
    bin/activemq start
    ```

    For more information on installing and configuring ActiveMQ, see [Configure ActiveMQ]({% link content-services/latest/config/activemq.md %}).

    Check the output to ensure that it starts successfully.

    Make a note of the TCP URL, with example format `tcp://server:port`, where server is the host name of the server 
    where ActiveMQ is installed. This is used in later steps.

    Content Services uses ActiveMQ for message queuing with various products, including the Transform Service.

4. Start the Shared File Store (SFS) controller:

    ```java
    java -DfileStorePath="/path/to/your/AlfrescoFileStore" \
         -Dscheduler.contract.path="/path/to/tempdir/scheduler.json" \
         -jar alfresco-shared-file-store-controller-4.1.x.jar
    ```

    Check the output to ensure that it starts successfully.

    By default, files are stored in `fileStorePath=/tmp/Alfresco`. This can be modified using the `fileStorePath` 
    parameter as shown in the above example.

    The SFS allows components such as the repository, and the Transform Service to share a common place to 
    store and retrieve files, for example, to enable transforms from an input source file to an output target file.
   
    >**Note:** Adding the scheduler contract path property to SFS startup is only required if running Windows.

5. Start the all-in-one Transform Core Engine Spring Boot app:

    ```java
    java -DPDFRENDERER_EXE="<alfresco-pdf-renderer_installation_dir>/alfresco-pdf-renderer" \
         -DLIBREOFFICE_HOME="<libreoffice_installation_dir>" \
         -DIMAGEMAGICK_ROOT="<imagemagick_installation_dir>" \
         -DIMAGEMAGICK_DYN="<imagemagick_installation_dir>/lib" \
         -DIMAGEMAGICK_EXE="<imagemagick_installation_dir>/bin/convert" \
         -DACTIVEMQ_URL="failover:(tcp://<server>:61616)?timeout=3000" \
         -DFILE_STORE_URL="http://<server>:8099/alfresco/api/-default-/private/sfs/versions/1/file" \
         -jar alfresco-transform-core-aio-boot-5.1.x.jar
    ```

    > **Note:** LibreOffice, ImageMagick and Alfresco PDF Renderer binaries needs to be installed on the server where the all-in-one core T-Engine is setup. See the [Prerequisites](#prereq-non-containerized-deploy) for more details. You may need to change the paths depending on your operating system.

    For example:

    ```java
    java -DPDFRENDERER_EXE="/usr/local/acs74/alfresco-pdf-renderer/alfresco-pdf-renderer" \
         -DLIBREOFFICE_HOME="/usr/local/acs74/libreoffice" \
         -DIMAGEMAGICK_ROOT="/usr/local/acs74/imagemagick" \
         -DIMAGEMAGICK_DYN="/usr/local/acs74/imagemagick" \
         -DIMAGEMAGICK_EXE="/usr/local/acs74/imagemagick/convert" \
         -DIMAGEMAGICK_CODERS="/usr/local/acs74/imagemagick/modules-Q16HDRI/coders" \
         -DIMAGEMAGICK_CONFIG="/usr/local/acs74/imagemagick/config-Q16HDRI" \
         -DACTIVEMQ_URL="failover:(tcp://localhost:61616)?timeout=3000" \
         -DFILE_STORE_URL="http://localhost:8099/alfresco/api/-default-/private/sfs/versions/1/file" \
         -jar /usr/local/acs74/bin/alfresco-transform-core-aio-boot-5.1.0.jar
    ```

    Check the output to ensure that it starts successfully.

    The all-in-one core T-Engine combines the five T-Engines (i.e. LibreOffice, ImageMagick, Alfresco PDF Renderer, 
    Tika, and Misc) into one single engine. All functionality that's available in the five T-Engines is available in the 
    all-in-one core T-Engine. The command-line options provide the paths to the installation locations and the URL of the 
    messaging broker.

6. Start the Transform Router Spring Boot app:

    ```java
    java -DCORE_AIO_QUEUE="org.alfresco.transform.engine.aio.acs" \
         -DCORE_AIO_URL="http://localhost:8090" \
         -DACTIVEMQ_URL="failover:(tcp://localhost:61616)?timeout=3000" \
         -DFILE_STORE_URL="http://localhost:8099/alfresco/api/-default-/private/sfs/versions/1/file" \
         -jar alfresco-transform-router-4.1.x.jar
    ```

    Check the output to ensure that it starts successfully.

    The Transform Router allows simple (single-step) and pipeline (multi-step) transforms that are passed to the 
    Transform Engines. The command-line options provide the router with the required data for T-Engines, queuing, 
    and file-store URL.

7. Set the following properties in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file:

    ```bash
    # ActiveMQ properties:
    messaging.broker.url=failover:(tcp://server:61616)?timeout=3000
    messaging.broker.username=$MQUSER
    messaging.broker.password=$MQPASS

    # Shared File Store properties:
    sfs.url=http://localhost:8099
    sfs.endpoint=${sfs.url}/alfresco/api/-default-/private/sfs/versions/1

    # Transform Router properties:
    transform.service.enabled=true
    transform.service.url=http://<Transform Service host>:8095/

    # Transform Core properties:
    localTransform.core-aio.url=http://<Transform Service host>:8090/
    ```

    This overrides the default properties provided by Content Services.

    > **Note:** Any changes to `alfresco-global.properties` require you to restart Alfresco Content Services to apply 
    > the updates. See the Content Services documentation [Using alfresco-global.properties]({% link content-services/latest/config/index.md%}#using-alfresco-globalproperties) 
    > for more information.

8. Check that the [configuration]({% link transform-service/latest/config/index.md %}) is set up correctly for your environment.

9. Restart Alfresco Content Services.

10. Ensure that the environment is up and running:

    1. Check the logs for Content Services startup.

    2. Monitor ActiveMQ by accessing the Web Console, e.g. `http://localhost:8161/admin/`.

    3. Temporarily enable `TransformDebug` in the repository if you want to see detailed debug log entries.

    4. Navigate to Digital Workspace or Share, and upload a file (such as a `.jpg`, `.png`, `.docx` etc.).

    5. Check the logs to see the metadata and work performed for the uploaded file. These should be available in the Spring Boot apps:

        * `alfresco-transform-router`
        * `alfresco-transform-core-aio`

Files should also be available in the specified path for the `alfresco-shared-file-store`. However, these files will 
only temporarily appear in the Shared File Store until explicitly deleted by the repository and/or expired and cleaned up.
---
title: Supported Platforms
---

The following are the supported platforms and software requirements for Alfresco Transform Service 4.1:

|Version|Notes|
|-------|-----|
| Content Services 23.x | |
| Content Services 7.4.x | |
