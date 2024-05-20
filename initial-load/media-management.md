---
title: Alfresco Media Management
---

Alfresco Media Management provides the capability to transform and add metadata and relationships to your digital media.

Digital media in enterprises is becoming a core content type, from sharing video and images internally, for marketing requirements, and publishing externally. The ability to manipulate, find and store digital media is extremely important. Digital assets do not lend themselves to traditional text-based searching, so providing the ability to add informational metadata for file retrieval is key. Digital assets can be large and might also be located in silos across an enterprise and it is crucial to centrally store, re-use and share these assets to provide value and collaboration within the organization.

Media Management provides many user interface enhancements for rich media handling, including video timeline comments and thumbnails, video trimming, and image manipulation.

Media Management enables you to optimize the delivery of media to different devices in a more resource effective way.

> **Note:** Alfresco Media Management 1.4 can be applied to Alfresco Content Services 6.2 only.

With Media Management you have flexibility when transforming your content, either on-premise with content transformation nodes that use FFmpeg and ImageMagick, or remotely through Amazon Web Services (AWS) Elastic Transcoder content transformer.

The AWS CloudFront publishing channel is supported to make content available outside your organization.

International Press Telecommunications Council (IPTC) standards support is provided with Media Management to add metadata and relationships to your content, including:

* Full IPTC data model support
* Full IPTC metadata extraction (both core and extension metadata)
* Mapping of IPTC keywords to standard tags
* IPTC metadata embedding

You can also add and extract your own custom XMP metadata, and set up rules to process your digital assets.

For more information on IPTC, see [http://www.iptc.org/site/Home/](http://www.iptc.org/site/Home/){:target="_blank"}.

For more information about FFmpeg, see [http://ffmpeg.org](http://ffmpeg.org){:target="_blank"}.

For more information about ImageMagick, see [https://imagemagick.org/index.php](http://www.imagemagick.org/){:target="_blank"}.

For more information about installing Media Management, see [Installing Media Management]({% link media-management/latest/install/index.md %}).

## Media Management architecture

Media Management provides a framework for transforming and sharing content, ideally using a remote server to ensure that the Alfresco Content Services server is not overloaded.

A video transformer is provided when you install Media Management to locally transform your content, however using this instance can be resource intensive and slow down your repository. You can create one or more content services nodes to offload work, or you can use remote transformation services, like Amazon Elastic Transcoder to transform your content. The configuration file for the content services node, config.yml, contains the location of ActiveMQ and the shared content workspace. The shared content workspace is a temporary workspace, used by the content services node to read source files and write to target files. See [Content services node architecture](#content-services-node-architecture) for information about the content services nodes and [Configuring transformation services]({% link media-management/latest/config/index.md %}#configuring-transformation-services) for information about transformation services.

> **Note:** Ensure that your remote server and your Content Services server are using Network Time Protocol (NTP). If your servers are not synchronized, work is not sent to the remote content services nodes, and jobs are processed on the local Content Services server.

If you are using a remote content services node, Media Management components should be started in the following order:

1. ActiveMQ
2. Content services node
3. Alfresco repository
4. Alfresco Share

FFmpeg and ImageMagick from the command line are required on any server where a content services node is running to transform content. FFmpeg, ImageMagick and ExifTool are required on the Alfresco server to view media in Share. ExifTool is used for metadata handling in the repository only.

ActiveMQ monitors for events and we recommend that you install it on the Alfresco server if you have other components that use ActiveMQ. If you are using ActiveMQ solely for Media Management, you might prefer to install ActiveMQ on the content services node server, but ensure that it resides on one server only.

Using the `alfresco-global.properties` file you can define properties for the FFmpeg path, ExifTool path, ActiveMQ broker URL, shared content workspace type, Zencoder and AWS Elastic Transcoder credentials, and other properties. See [Configure Media Management]({% link media-management/latest/config/index.md %}) for more information on `alfresco-global.properties` settings.

You can publish your content from the repository to the CloudFront publishing channel. See [Configuring a CloudFront publishing channel]({% link media-management/latest/config/index.md %}#configuring-a-cloudfront-publishing-channel) for more information.

The diagram shows the relationship between the Alfresco server and the content services node server. Alfresco can connect to a transformation service (Amazon Elastic Transcoder), a publishing channel (CloudFront), and a shared content workspace (a file system or Amazon S3). The content services node can connect to the shared content workspace and the transformation service that you defined in the `alfresco-global.properties` file.

> **Note:** Ensure that you review the security of the following connections:

* Alfresco server to server (or servers) where remote content services nodes are installed
* Alfresco server to the shared content workspace
* Remote content services node (or nodes) to the shared content workspace

Ensure that only the repository and the content services nodes have access to the shared content workspace, because temporary copies of the content binary files (for both file and S3 types) are stored in the workspace.

![Architecture]({% link media-management/images/architecture.png %})

The diagram shows the relationship between the Alfresco server and the content services node server. Alfresco can connect to a transformation service (Amazon Elastic Transcoder), a publishing channel (CloudFront), and a shared content workspace (a file system or Amazon S3). The content services node can connect to the shared content workspace and the transformation service that you defined in the Alfresco server `alfresco-global.properties` file.

For information on monitoring the components of the architecture, see [Monitoring Media Management]({% link media-management/latest/admin/index.md %}#monitoring-media-management).

## Content services node architecture

Media Management provides a content services node infrastructure to process your transformations. You can create content services nodes remotely to offload low level transformations.

You can have multiple content services nodes running on the same server, ideally separate from your Alfresco server, however configuring a single content services node on a single server (with servers scaled as required) provides the optimum framework for multiple parallel transformations.

The four main architectural areas are:

* **Client Application (Alfresco repository)**: Task messages are generated and sent from the Alfresco repository, containing a reference to the source content (Source ContentReference) and other options. The options specified depend on the task, for example, a target reference or media type. The content reference needs to be in a format that the task nodes can handle, for example, a file on a shared disk, an S3 path, or a CMIS document ID. The source and target content is stored in a content workspace. Supported formats are shared file or Amazon S3 storage.
* **Message Routing (ActiveMQ)**: A message routing system, for example, ActiveMQ, then directs the request to the appropriate queue for consumption by processing nodes. When you view the ActiveMQ queues in the web console (`http://localhost:8161/admin`), there are separate queues for image transform requests, image transform responses, video transform requests and video transform responses.
* **Transform Component**: A component listens for messages on a queue and calls on ImageMagick or FFmpeg workers to perform the task specified by the source content reference. The component can optionally send a reply that is consumed by the original requestor or another party.
* **Task Node**: Task nodes bootstrap one or more components.

![Content Services Node architecture]({% link media-management/images/gytheio.png %})

1. Task message sent from Alfresco repository to Source content on shared content workspace.
2. Image transformation request sent from Alfresco repository to ActiveMQ (message routing).
3. Transform request sent from ActiveMQ to transform component on Task node.
4. Source content on shared content workspace sends request to SourceContentReferenceHandler in ImageMagick worker (in Transform Component.)
5. TargetContentReferenceHandler in ImageMagick worker (in Transform Component) sends response to Target content on Shared content workspace.
6. Transformation reply sent from Transform Component to MessageProducer and on to ActiveMQ.
7. Image Transformation Response (POJO) sent to Alfresco repository.
8. Target content sent to Alfresco repository.

For more information on launching a content services node, see [Start Media Management]({% link media-management/latest/config/start.md %}).

For more information on advanced ActiveMQ settings, see [Configuring advanced settings in ActiveMQ]({% link content-services/latest/config/activemq.md %}#advanced).
---
title: Feature dependency mapping to component
---

You need a number of components to use all the Media Management capabilities. This information maps each feature with its dependencies.

|Feature|Software to implement|Distributed by Alfresco?|
|-------|---------------------|------------------------|
|IPTC metadata extraction|[FFmpeg](https://www.ffmpeg.org/){:target="_blank"} and MM Java|No|
|PBCore technical video metadata|[FFmpeg](https://www.ffmpeg.org/){:target="_blank"}|No|
|Custom XMP metadata|[ExifTool](http://www.sno.phy.queensu.ca/~phil/exiftool/){:target="_blank"}|No|
|Metadata embedding|[ExifTool](http://www.sno.phy.queensu.ca/~phil/exiftool/){:target="_blank"}|No|
|Video thumbnails|[FFmpeg](https://www.ffmpeg.org/){:target="_blank"}|No|
|Local video transcoding|[FFmpeg](https://www.ffmpeg.org/){:target="_blank"}|No|
|Remote video transcoding|[FFmpeg](https://www.ffmpeg.org/){:target="_blank"},[Zencoder](https://github.com/bitzeche/zencoder-java){:target="_blank"} and AWS (SDK through content services node)|Yes|
|Video trim (transformation)|[FFmpeg](https://www.ffmpeg.org/){:target="_blank"}|No|
|Image crop and rotate (transformation)|[ImageMagick](https://imagemagick.org/index.php){:target="_blank"}|No|
|Back end components|[Content services node](https://github.com/Alfresco/gytheio){:target="_blank"}|Yes|
|HTML5 video player|[video.js](https://github.com/videojs/video.js){:target="_blank"}|Yes|
|Video timeline comments|[videojs-markers](https://github.com/spchuang/videojs-markers){:target="_blank"}|Yes|
|Video storyboard thumbnails|[videojs-thumbnails](https://github.com/brightcove/videojs-thumbnails){:target="_blank"}|Yes|
|Video trim UI|[rangeslider-videojs](https://github.com/danielcebrian/rangeslider-videojs){:target="_blank"}|Yes|
|Image rotate UI|[Icons](http://findicons.com/icon/474073/rotate?id=485645){:target="_blank"}|Yes|
|Image pan and zoom|[imgAreaSelect](http://odyniec.net/projects/imgareaselect/){:target="_blank"}|Yes|
|Dark site theme|[jquery.panzoom](https://github.com/timmywil/jquery.panzoom){:target="_blank"}|-|
|UI utilities|CSS|Yes|
|AWS CloudFront integration|AWS (SDK using content services node)|Yes|
---
title: Administering Media Management
---

This information helps you to monitor and administer Alfresco Media Management.

If you are backing up and restoring Media Management, use the standard Alfresco guidance: [Back up and restore]({% link content-services/latest/admin/backup-restore.md %}).

## Monitoring Media Management

You can monitor the flow of media events from the Alfresco repository through ActiveMQ and system logs.

1. Check the health of ActiveMQ, particularly that the following events are occurring:

    * **Topics > alfresco.health.contentservices** shows that heartbeats are being sent
    * **Queues > alfresco.transform.request.image, alfresco.transform.reply.image, alfresco.transform.request.video, and alfresco.transform.reply.video** are showing messages enqueuing and dequeuing
    ActiveMQ provides a web console:

    ```json
    http://localhost:8161/admin/
    ```

    where `localhost` is the name of the Alfresco server.

    You can also check the ActiveMQ log, which is located in `activemq/data/activemq.log` where `activemq` is the name of directory where you installed ActiveMQ.

    By default, subscribers are set to Active Durable Topic Subscribers to ensure that if ActiveMQ fails, messages are not lost.

    >**Note:** For technical reasons, Topics **> Messages Dequeued** never decrements. Do not monitor this queue.

2. Check the content services node log to monitor what is being transformed:

    * Port 8889 is reserved for the content services node. `http://localhost:8889/healthcheck` shows the last transformation after startup (but before any transformations). You should see:

        ```json
        {"FFmpeg":{"healthy":true},"ImageMagick":{"healthy":true},"deadlocks":{"healthy":true}}
        ```

        and after a transformation request:

        ```json
        {"FFmpeg":{"healthy":true,"message":"lastRequest: \"6075f46f-de9c-4232-aa78-d3ed1280a371\""},"ImageMagick":{"healthy":true},"deadlocks":{"healthy":true}}
        ```

    * Check the log, which is located in `remote-node/logs/content-services-node.log`, where `remote-node` is the name of directory that you unzipped when you installed Media Management.
    * You can change the log level of the content services node in the `remote-node/config.yml` file.
3. Check `alfresco.log`, after setting the log level to `debug`, for any errors.

4. Use the `log4j.properties.sample` file to add loggers to your `tomcat/webapps/alfresco/WEB-INF/classes/alfresco/module/org_alfresco_mm_repo/log4j.properties` file.

    A `log4j.properties.sample` file is provided in the Media Management installation zip. This file contains loggers that you can add to your Alfresco `log4j.properties` file to trace and debug your Media Management workflow.

## Admin Tools for Media Management

Administrators can view information about transformations and add publishing channels in the Admin Tools option of the Share menu bar.

1. Select **Admin Tools** on the Share toolbar, to see a list of tools on the left of the page.
2. The **Tools > Application** section lists the themes available. Media Management provides a black background (a dark theme) for Share. See [Using an Alfresco dark site theme]({% link media-management/latest/using/index.md %}#using-an-alfresco-dark-site-theme) for more information.
3. The **Content Publishing > Channel Manager** section lists the channels that are configured for users to publish media (for example, CloudFront). Use this guidance to add a new publishing channel: [Configuring a CloudFront publishing channel]({% link media-management/latest/config/index.md %}#configuring-a-cloudfront-publishing-channel).
4. The **Transformations** section lists the installed transformers and their status. Select Transformer FFmpeg to see information on whether the transformer is available, and the version of FFmpeg that is installed with the options configured.
---
title: JMX beans
---

JMX values (Managed Bean or MBean attributes) are exposed in the Alfresco Admin Console, and with internal tools (Alfresco JMX Dump) or external tools like JConsole. The Media Management beans are described here with their default values.

The default values given are the defaults for an installer-installed instance of Alfresco on Windows. These values can differ if you are using a different install method or operating system.

>**Note:** Be aware that any changes you make to attributes in the live system are written to the database. The next time that Alfresco starts, these values will take precedence over any values specified in properties files, for example, `alfresco-global.properties`.

## Alfresco:Type=Configuration, Category=Transformers, Object Type=Transformers$default**

|Attribute name|Example value|
|--------------|-------------|
|content.transformer.AwsElasticTranscoder.mimetypes.video/*.video/mp4.priority|`110`|
|content.transformer.Ffmpeg.extensions.*.3g2.supported|`false`|
|content.transformer.Ffmpeg.extensions.*.3gp.supported|`false`|
|content.transformer.Ffmpeg.extensions.*.gif.supported|`false`|
|content.transformer.Ffmpeg.extensions.*.jp2.supported|`false`|
|content.transformer.Ffmpeg.extensions.*.ras.supported|`false`|
|content.transformer.Ffmpeg.extensions.*.xbm.supported|`false`|
|content.transformer.Ffmpeg.extensions.*.xwd.supported|`false`|
|content.transformer.Ffmpeg.extensions.3g2.*.supported|`false`|
|content.transformer.Ffmpeg.extensions.3gp.*.supported|`false`|
|content.transformer.Ffmpeg.mimetypes.application/mxf.image/*.supported|`false`|
|content.transformer.Ffmpeg.mimetypes.application/mxf.video/*.supported|`false`|
|content.transformer.Ffmpeg.mimetypes.audio/*.video/*.supported|`false`|
|content.transformer.Ffmpeg.mimetypes.video/*.image/*.priority|`50`|
|content.transformer.Ffmpeg.mimetypes.video/*.video/*.priority|`150`|
|content.transformer.RemoteImage.mimetypes.application/pdf.image/*.supported|`false`|
|content.transformer.RemoteImage.mimetypes.image/*.image/*.supported|`false`|
|content.transformer.RemoteImage.mimetypes.image/bmp.image/*.priority|`150`|
|content.transformer.RemoteImage.mimetypes.image/gif.image/*.priority|`150`|
|content.transformer.RemoteImage.mimetypes.image/jpeg.image/*.priority|`150`|
|content.transformer.RemoteImage.mimetypes.image/png.image/*.priority|`150`|
|content.transformer.RemoteImage.mimetypes.image/x-raw-*.image/*.priority|`50`|
|content.transformer.RemoteVideo.mimetypes.application/*.*.supported|`false`|
|content.transformer.RemoteVideo.mimetypes.application/mxf.image/*.supported|`false`|
|content.transformer.RemoteVideo.mimetypes.application/mxf.video/*.priority|`100`|
|content.transformer.RemoteVideo.mimetypes.application/mxf.video/*.supported|`false`|
|content.transformer.RemoteVideo.mimetypes.audio/*.video/*.supported|`false`|
|content.transformer.RemoteVideo.mimetypes.image/*.*.supported|`false`|
|content.transformer.RemoteVideo.mimetypes.text/*.*.supported|`false`|
|content.transformer.RemoteVideo.mimetypes.video/*.application/*.supported|`false`|
|content.transformer.RemoteVideo.mimetypes.video/*.audio/*.supported|`false`|
|content.transformer.RemoteVideo.mimetypes.video/*.image/*.priority|`150`|
|content.transformer.RemoteVideo.mimetypes.video/*.image/*.supported|`false`|
|content.transformer.RemoteVideo.mimetypes.video/*.text/*.supported|`false`|
|content.transformer.RemoteVideo.mimetypes.video/*.video/*.priority|`50`|
|content.transformer.RemoteVideo.mimetypes.video/*.video/*.supported|`false`|
|content.transformer.strict.mimetype.check|`true`|
|transformer.strict.mimetype.check.whitelist.mimetypes|`application/eps;application/postscript;application/illustrator;application/pdf;application/x-tar;application/x-gtar;application/acp;application/zip;application/vnd.stardivision.math;application/x-tika-msoffice;image/x-raw-adobe;image/tiff`|
|content.transformer.Zencoder.mimetypes.video/*.video/*.priority|`100`|

For the complete list of Alfresco MBeans, see [JMX bean categories reference]({%link content-services/latest/admin/jmx-reference.md %}).
---
title: Transform options
---

Media Management provides additional transform options for images and video.

The tables give details of registered file types with information about their available transform options.

You can also view more information about file types and the proxies used to transform them by using the browser command:

```html
localhost:8080/alfresco/service/mimetypes?mimetype=*
```

where `localhost:8080` is the host and port number of your active Content Services instance.

Audio and video files are transformable using FFmpeg. Image files are transformable using ImageMagick. The formats listed are in addition to the standard formats as specified in [ACS Transformation options]({% link content-services/latest/admin/transformations.md %}).

```text
application/eps - eps, image/bmp - bmp, image/cgm - cgm, image/gif - gif, image/ief - ief, image/jp2 - jp2, image/jpeg - jpg, image/png - png, image/tiff - tiff, image/vnd.adobe.photoshop - psd, image/vnd.adobe.premiere - ppj, image/x-dwg - dwg, image/x-dwt - dwt, image/x-portable-anymap - pnm, image/x-portable-bitmap - pbm, image/x-portable-graymap - pgm, image/x-portable-pixmap - ppm, image/x-raw-adobe - dng, image/x-raw-canon - cr2, image/x-raw-fuji - raf, image/x-raw-hasselblad - 3fr, image/x-raw-kodak - k25, image/x-raw-leica - rwl, image/x-raw-minolta - mrw, image/x-raw-nikon - nef, image/x-raw-olympus - orf, image/x-raw-panasonic - rw2, image/x-raw-pentax - pef, image/x-raw-red - r3d, image/x-raw-sigma - x3f, image/x-raw-sony - arw, image/x-rgb - rgb, image/x-xpixmap - xpm and image/x-xwindowdump - xwd
```

|Format|Transformable from:|
|------|-------------------|
|video/mp2t|X|
|video/mp4|X|
|video/mpeg|X|
|video/ogg|X|
|video/quicktime|X|
|video/webm|X|
|video/x-flv|X|
|video/x-m4v|X|
|video/x-ms-asf|X|
|video/x-ms-wmv|X|
|video/x-msvideo|X|

```text
audio/basic - au, audio/mp4 - m4a, audio/mpeg - mp3, audio/ogg - oga, audio/vorbis - ogg, audio/x-aiff - aiff, audio/x-flac - flac, audio/x-ms-wma - wma, audio/x-wav - wav
```

All file types are transformable into and from the following formats, excepting themselves (i.e. audio/mp4 is not transformable into audio/mp4, or from audio/mp4).

|Format|Transformable to:|Transformable from:|
|------|-----------------|-------------------|
|application/mxf| |X|
|audio/basic|X|X|
|audio/mp4|X|X|
|audio/mpeg|X|X|
|audio/ogg|X|X|
|audio/vorbis|X|X|
|audio/x-aiff|X|X|
|audio/x-flac|X|X|
|audio/x-ms-wma|X|X|
|audio/x-wav|X|X|
|video/mp2t| |X|
|video/mp4| |X|
|video/mpeg| |X|
|video/ogg| |X|
|video/quicktime| |X|
|video/webm| |X|
|video/x-flv| |X|
|video/x-m4v| |X|
|video/x-ms-asf| |X|
|video/x-ms-wmv| |X|
|video/x-msvideo| |X|

```text
audio/vnd.adobe.soundbooth - asnd, video/3gpp - 3gp, video/3gpp2 - 3g2, video/mpeg2 - mpeg2, video/x-rad-screenplay - avx, video/x-sgi-movie - movie and x-world/x-vrml - wrl
```

> **Note:** These formats cannot be transformed into, or generated from, any other format.

```text
video/mp2t - ts, video/mp4 - mp4, video/mpeg - mpg, video/ogg - ogv, video/quicktime - mov, video/x-msvideo - avi, video/webm - webm, video/x-flv - flv, video/x-m4v - m4v, video/x-ms-asf - asf, video/x-ms-wmv - wmv, and video/x-msvideo - avi
```

All file types are transformable into and from the following formats, excepting themselves (i.e. video/mp4 is not transformable into video/mp4, or from video/mp4).

|Format|Transformable to:|Transformable from:|
|------|-----------------|-------------------|
|application/eps|X| |
|audio/basic|X| |
|audio/mp4|X| |
|audio/mpeg|X| |
|audio/ogg|X| |
|audio/vorbis|X| |
|audio/x-aiff|X| |
|audio/x-flac|X| |
|audio/x-ms-wma|X| |
|audio/x-wav|X| |
|image/bmp|X| |
|image/cgm|X| |
|image/gif|X| |
|image/ief|X| |
|image/jp2|X| |
|image/jpeg|X| |
|image/png|X| |
|image/tiff|X| |
|image/vnd.adobe.photoshop|X| |
|image/vnd.adobe.premiere|X| |
|image/x-cmu-raster|X| |
|image/x-dwt|X| |
|image/x-portable-anymap|X| |
|image/x-portable-bitmap|X| |
|image/x-portable-graymap|X| |
|image/x-portable-pixmap|X| |
|image/x-raw-adobe|X| |
|image/x-raw-canon|X| |
|image/x-raw-fuji|X| |
|image/x-raw-hasselblad|X| |
|image/x-raw-kodak|X| |
|image/x-raw-leica|X| |
|image/x-raw-minolta|X| |
|image/x-raw-nikon|X| |
|image/x-raw-olympus|X| |
|image/x-raw-panasonic|X| |
|image/x-raw-pentax|X| |
|image/x-raw-red|X| |
|image/x-raw-sigma|X| |
|image/x-raw-sony|X| |
|image/x-rgb|X| |
|image/x-xbitmap|X| |
|image/x-xpixmap|X| |
|image/x-xwindowdump|X| |
|video/mp2t|X|X|
|video/mp4|X|X|
|video/mpeg|X|X|
|video/ogg|X|X|
|video/quicktime|X|X|
|video/webm|X|X|
|video/x-flv|X|X|
|video/x-m4v|X|X|
|video/x-ms-asf|X|X|
|video/x-ms-wmv|X|X|
|video/x-msvideo|X|X|
---
title: Troubleshooting
---

Use this information to help diagnose any problems when using Media Management.

## Video proxy generation starts but does not complete

If the timeout value for video transformation is too low, it is likely that videos will not load in Alfresco Share. In some setups, the `content.transformer.default.timeoutMs` setting might be limited. To resolve this problem, set the following option in your `alfresco-global.properties` file and check that this value is not being overridden by JMX:

```bash
content.transformer.default.timeoutMs=64800000
```

## Error in Alfresco log if FFmpeg is not installed, thumbnails not available

If you preview a video or image and you do not have FFmpeg installed, you will see an error in the `alfresco.log` file, for example:

```bash
ERROR [org.springframework.extensions.webscripts.AbstractRuntime] [http-apr-8080-exec-11]  Exception from executeScript - redirecting to status template error:  03220008
The content node was not specified so the content cannot be streamed to the client: classpath*:alfresco/templates/webscripts/org/alfresco/repository/thumbnail/thumbnail.get.js org.springframework.extensions.webscripts.WebScriptException: 03220008  
The content node was not specified so the content cannot be streamed to  the client: classpath*:alfresco/templates/webscripts/org/alfresco/repository/thumbnail/thumbnail.get.js
```

The error message should not affect the ability to preview the video, however thumbnails will not be available. Install FFmpeg to resolve this error.

## Error when running ImageMagick: *RegistryKeyLookupFailed*, *CoderModulesPath*

If you see a `CoderModulesPath` error, it might be because the file type that you are trying to transform has not been added to the DELEGATES list for ImageMagick. To check which delegates are supported, run this command from the ImageMagick installation directory:

```bash
convert -version
```

The delegates supported are listed in the results.

If you are using RAW image formats, you must install an ImageMagick delegate, for example, UFRaw.

## Unable to create proxy when loading video

When you load a video in Alfresco Share, if you receive the message `Could not create proxy, try viewing or downloading the source`, you need to include the correct proxy, for example, H.264. See [FFmpeg](http://ffmpeg.org/ffmpeg.html){:target="_blank"} for more information.

## Failure loading images or video in Alfresco Share

If you do not have FFmpeg or ImageMagick available to Java, then you will not be able to view images and video in Alfresco Share. Ensure that Java has FFmpeg and ImageMagick on its command line path, or define the path location in your `alfresco-global.properties` file. See See [step 7 of Installing Media Management]({% link media-management/latest/install/index.md %}) for information on how to set these in the `alfresco-global.properties` file.
---
title: Configure Media Management
---

You can configure Media Management using the alfresco-global.properties file or by using a JMX client such as JConsole.

1. Open the `alfresco-global.properties` file and add the required properties to the file.

    A sample `alfresco-global.properties` file is shipped in the root folder of the Media Management distribution zip, which defines properties for the FFmpeg path, ExifTool path, ActiveMQ broker URL, shared content workspace type, and AWS Elastic Transcoder credentials, custom metadata extraction properties, video thumbnail settings, and video proxy timeout settings.

2. Save the `alfresco-global.properties` file, and then restart your Alfresco server.

    The following table shows an overview of the available properties:

    |Property|Description|
    |--------|-----------|
    |ffmpeg.exe=|Sets the FFmpeg executable path. Default is ffmpeg. Remember to use the forward slash (/) in your path if you are using Unix, and back slash (\) if you are using Windows.|
    |exiftool.exe=|Sets the ExifTool executable path. Default is exiftool. Remember to use the forward slash (/) in your path if you are using Unix, and back slash (\) if you are using Windows.|
    |messaging.broker.url=failover: (tcp://broker1:61616,tcp://broker2:61616)|Sets the host name and port of the ActiveMQ instance. Default is localhost|
    |content.remote.default.contentRefHandler. source.type=|Sets the shared content workspace for source. Type can be file or s3|
    |content.remote.default.contentRefHandler. source.file.dir=|If you are using a file type for the shared content workspace, specify the file directory.|
    |content.remote.default.contentRefHandler. source.s3.bucketName=|If you are using S3 for the shared content workspace, specify the S3 bucket.|
    |content.remote.default.contentRefHandler. target.s3.bucketRegion=|If you are using S3 for the shared content workspace, specify the S3 bucket region.|
    |content.remote.default.contentRefHandler. target.s3.accessKey=|If you are using S3 for the shared content workspace, specify the S3 access key.|
    |content.remote.default.contentRefHandler. target.s3.secretKey=|If you are using S3 for the shared content workspace, specify the S3 secret key.|
    |content.transformer.AwsElasticTranscoder. s3.accessKey=|If you are using the AWS Elastic Transcoder content transformer, specify the S3 access key.|
    |content.transformer.AwsElasticTranscoder. s3.secretKey=|If you are using the AWS Elastic Transcoder content transformer, specify the S3 secret key.|
    |content.transformer.AwsElasticTranscoder. s3.bucketName=|If you are using the AWS Elastic Transcoder content transformer, specify the S3 bucket.|
    |content.transformer.AwsElasticTranscoder. s3.bucketRegion=|If you are using the AWS Elastic Transcoder content transformer, specify the S3 bucket region. Default is `us-east-1`|
    |content.transformer.AwsElasticTranscoder. transcoder.accessKey=|If you are using the AWS Elastic Transcoder content transformer, specify the transcoder access key.|
    |content.transformer.AwsElasticTranscoder. transcoder.secretKey=|If you are using the AWS Elastic Transcoder content transformer, specify the transcoder secret key.|
    |content.transformer.AwsElasticTranscoder. transcoder.pipelineId=|If you are using the AWS Elastic Transcoder content transformer, specify the transcoder pipeline identifier.|
    |content.transformer.AwsElasticTranscoder. transcoder.region|If you are using the AWS Elastic Transcoder content transformer, specify the transcoder region. Default is `us-east-1`|
    |content.transformer.AwsElasticTranscoder. transcoder.defaultPreset.video/mp4=|If you are using the AWS Elastic Transcoder content transformer, specify the transcoder preset for video and MP4. Default is `1351620000001-000010`|
    |metadata.extracter.TikaExifTool.extract. namespace.prefix.custom=|URL used by external applications to read XMP custom metadata. Example entry is `http://example.com/model/custom/1.0`|
    |metadata.extracter.TikaExifTool.extract. XMP-custom\:Text=|Type of field for extraction of single lines of XMP custom metadata. Example value is `custom:text`|
    |metadata.extracter.TikaExifTool.extract. XMP-custom\:TextML[]=|Type of field for extraction of multiple lines of XMP custom metadata. Example value is `custom:textMultiLine`|
    |content.metadataExtracter.default. timeoutMs=|Maximum time for extracting content metadata to complete. Default is 60000 milliseconds \(60 seconds\).|
    |video.thumbnail.defaultOffset=|The offset time before creating a video thumbnail. Default is `00:00:00.5`.|
    |video.thumbnail.storyboardIntervalSeconds=|Time interval between video thumbnails. Default is 2 seconds.|
    |video.thumbnail.storyboardMaxElements=|Maximum number of video thumbnails. Default is 30 elements.|
    |system.videoProxy.definition.default. timeoutMs=|Maximum time for a video proxy to complete. Parameter is used by the `h264-720` proxy. Default is 64800000 milliseconds (18 hours).|

    You can also set where you want each of your transformations to take place: locally, with the remote content services node, or with a remote transformer like Elastic Transcoder, and in what order the transformations should be attempted. The default settings are appropriate for most configurations.

    The full list of remote properties, with their default values, that you can override in your `alfresco-global.properties` file is as follows:

    ```bash
    # mimetypes ffmpeg can be made to support, but support not present in many environments
    content.transformer.Ffmpeg.extensions.3gp.*.supported=false
    content.transformer.Ffmpeg.extensions.3g2.*.supported=false
    content.transformer.Ffmpeg.extensions.*.3gp.supported=false
    content.transformer.Ffmpeg.extensions.*.3g2.supported=false

    content.transformer.Ffmpeg.extensions.*.gif.supported=false
    content.transformer.Ffmpeg.extensions.*.jp2.supported=false
    content.transformer.Ffmpeg.extensions.*.ras.supported=false
    content.transformer.Ffmpeg.extensions.*.xbm.supported=false
    content.transformer.Ffmpeg.extensions.*.xwd.supported=false

    # conversions ffmpeg can support, but don't make much sense in most cases
    content.transformer.Ffmpeg.mimetypes.audio/*.video/*.supported=false

    # Grabbing thumbnail frames isn't resource intensive so perform locally
    content.transformer.Ffmpeg.mimetypes.video/*.image/*.priority=50
    content.transformer.Ffmpeg.mimetypes.application/mxf.video/*.supported=false
    content.transformer.Ffmpeg.mimetypes.application/mxf.image/*.supported=false

    # Remote transcoding should be preferred if available
    content.transformer.Ffmpeg.mimetypes.video/*.video/*.priority=150

    # Content service node settings
    content.transformer.RemoteVideo.mimetypes.video/*.video/*.supported=true
    content.transformer.RemoteVideo.mimetypes.video/*.image/*.supported=true
    content.transformer.RemoteVideo.mimetypes.video/*.audio/*.supported=true
    content.transformer.RemoteVideo.mimetypes.video/*.application/*.supported=false
    content.transformer.RemoteVideo.mimetypes.video/*.text/*.supported=false
    content.transformer.RemoteVideo.mimetypes.application/*.*.supported=false
    content.transformer.RemoteVideo.mimetypes.application/mxf.video/*.supported=false
    content.transformer.RemoteVideo.mimetypes.application/mxf.image/*.supported=false
    content.transformer.RemoteVideo.mimetypes.image/*.*.supported=false
    content.transformer.RemoteVideo.mimetypes.text/*.*.supported=false
    content.transformer.RemoteImage.mimetypes.image/*.image/*.supported=true
    content.transformer.RemoteImage.mimetypes.application/pdf.image/*.supported=true

    # Conversions ffmpeg can support, but don't make much sense in most cases
    content.transformer.RemoteVideo.mimetypes.audio/*.video/*.supported=false

    # Only send resource intensive transcoding remote
    content.transformer.RemoteVideo.mimetypes.video/*.video/*.priority=50
    content.transformer.RemoteVideo.mimetypes.video/*.image/*.priority=150
    content.transformer.RemoteVideo.mimetypes.application/mxf.video/*.priority=100

    # Only send resource intensive RAW conversion remote
    content.transformer.RemoteImage.mimetypes.image/x-raw-*.image/*.priority=50
    content.transformer.RemoteImage.mimetypes.image/jpeg.image/*.priority=150
    content.transformer.RemoteImage.mimetypes.image/png.image/*.priority=150
    content.transformer.RemoteImage.mimetypes.image/gif.image/*.priority=150
    content.transformer.RemoteImage.mimetypes.image/bmp.image/*.priority=150

    # AWS Elastic Transcoder
    content.transformer.AwsElasticTranscoder.mimetypes.video/*.video/mp4.priority=110
    ```

    The priority settings define which type of transformation will be tried first. The lower the number, the higher the priority. For example, if the default settings are used, video to video transcoding would have these settings:

    ```bash
    content.transformer.RemoteVideo.mimetypes.video/*.video/*.priority=50
    content.transformer.AwsElasticTranscoder.mimetypes.video/*.video/mp4.priority=110
    content.transformer.Ffmpeg.mimetypes.video/*.video/*.priority=150
    ```

    The content services node is tried first, as it has the highest priority with a value of `50`. Elastic Transcoder would be tried next. If any of the transformer types is not configured, or there is a problem, the video to video transcoding would fall back to the local FFmpeg transformer, which is set with the lowest priority as `content.transformer.Ffmpeg.mimetypes.video/*.video/*.priority=150`.

    You can set these variables in your `alfresco-global.properties` file, or dynamically when Alfresco is running, using a JMX client. If you set values in both places, the JMX client overrides the `alfresco-global.properties` value, but not the `alfresco-global.properties` file itself. The values are in the **Alfresco:Type=Configuration, Category=Transformers** MBean.
    See [JMX beans for Media Management]({% link media-management/latest/admin/jmxbeans.md %}) for more information about Media Management JMX beans.

   > **Note:** You can use a wildcard (*) in the settings. However, more specific mimetype or extension configurations take precedence over wildcard configurations, regardless of the order specified.

3. Use the `log4j.properties.sample` file to add loggers to your `tomcat/webapps/alfresco/WEB-INF/classes/alfresco/module/org_alfresco_mm_repo/log4j.properties` file.

    A `log4j.properties.sample` file is provided in the Media Management installation zip.

    See [Runtime administration with a JMX client]({% link content-services/latest/config/index.md %}#using-jmx-client-to-change-settings-dynamically) for instructions on how to connect a JMX client to your Alfresco server.

## Configuring a shared file content workspace

You can configure Alfresco to use Amazon S3 or file directories for sharing content.

Configure a directory as a shared content workspace using `alfresco-global.properties`.

Ensure that you have installed the required external and internal software. See [Prerequisites for using Media Management]({% link media-management/latest/install/index.md %}).

1. Stop the Alfresco server.

2. Edit your `alfresco-global.properties` file to specify your source and target content workspace type, and the location of your source and target directories, for example:

    ```bash
    content.remote.default.contentRefHandler.source.type=file
    content.remote.default.contentRefHandler.source.file.dir=
    content.remote.default.contentRefHandler.target.type=file
    content.remote.default.contentRefHandler.target.file.dir=
    ```

    A sample `alfresco-global.properties` file is shipped in the root folder of the Media Management distribution zip, which defines custom properties.

3. Update your `remote-node/config.yml` file that you extracted from the Media Management distribution zip with your shared content workspace properties:

    ```yaml
    transform:
        contentReferenceHandler:
            source:
                type: file
                file:
                    path: /tmp/AlfrescoContentServices
            target:
                type: file
                file:
                    path: /tmp/AlfrescoContentServices
    ```

    You can use the same mounted network volume directory (for example, NFS) for both the Content Services repository (configured using `content.remote.default.contentRefHandler.* properties`) and the remote node.

    The content services node uses ImageMagick and FFmpeg and requires that the executable directories are available on the system PATH variable or are specified in `alfresco-global.properties`.

    For more information about the content services framework, see [Content services node architecture]({% link media-management/latest/index.md %}).

4. Start your Content Services server to apply the changes.

## Configuring an Amazon S3 shared content workspace

Amazon S3 can be configured as a shared content workspace using `alfresco-global.properties`.

Ensure that you have installed the required external and internal software. See [Prerequisites for using Media Management]({% link media-management/latest/install/index.md %}) for more information. Make sure you have your Amazon S3 account set up.

1. Stop the Alfresco server.

2. Edit your `alfresco-global.properties` file to specify your source and target content workspace type, source and target S3 keys, and S3 bucket information, for example:

    ```bash
    content.remote.default.contentRefHandler.source.type=s3
    content.remote.default.contentRefHandler.source.s3.bucketName=
    content.remote.default.contentRefHandler.source.s3.bucketRegion=
    content.remote.default.contentRefHandler.source.s3.accessKey=
    content.remote.default.contentRefHandler.source.s3.secretKey=
    content.remote.default.contentRefHandler.target.type=s3
    content.remote.default.contentRefHandler.target.s3.bucketName=
    content.remote.default.contentRefHandler.target.s3.bucketRegion=
    content.remote.default.contentRefHandler.target.s3.accessKey=
    content.remote.default.contentRefHandler.target.s3.secretKey=
    ```

    A sample `alfresco-global.properties` file is shipped in the root folder of the Media Management distribution zip, which defines custom properties.

    You can find your S3 details in your AWS S3 settings.

3. Update your `remote-node/config.yml` file that you extracted from the Media Management distribution zip with your shared content workspace properties:

    ```yaml
    source:
      type: s3
      s3:
         accessKey: <key>
         secretKey: <secret>
         bucketName: <bucket>
         bucketRegion: us-east-1
    target:
      type: s3
      s3:
         accessKey: <key>
         secretKey: <secret>
         bucketName: <bucket>
         bucketRegion: us-east-1
    ```

    The content services node uses ImageMagick and FFmpeg and requires that the executable directories are available on the system PATH variable or are specified in `alfresco-global.properties`.

    For more information about the content services framework, see [Content services node architecture]({% link media-management/latest/index.md %}).

4. Start your Content Services server to apply the changes.

## Configuring transformation services

This information helps you to configure Alfresco to communicate with AWS Elastic Transcoder. This transformation service is often configured for cloud deployments or very large resource intensive on-premise deployments.

Edit the `alfresco-global.properties` file to turn off content service node transformations for certain file (MIME) types, for example, video to video, video to audio, and image to image:

```bash
content.transformer.RemoteVideo.mimetypes.video/*.video/*.supported=false
content.transformer.RemoteVideo.mimetypes.video/*.audio/*.supported=false
content.transformer.RemoteImage.mimetypes.image/*.image/*.supported=false

```

> **Note:** Video transformation (transcoding) is very resource intensive and can take a long time to complete. Make sure that any rules that you configure using video transcoding run in the background, to prevent the rule from failing due to a Share timeout. For more information about creating rules, see [Creating a rule]({% link content-services/latest/using/content/rules.md %}).

## Configuring the Elastic Transcoder content transformer

Amazon Web Services (AWS) Elastic Transcoder is supported for remote video transcoding with Amazon S3. If you are using this transformer, configure your connection using `alfresco-global.properties`.

Ensure that you have installed the required external and internal software before configuring the transformer. See [Prerequisites for using Media Management]({% link media-management/latest/install/index.md %}) for more information. Make sure you have your Elastic Transcoder and S3 accounts set up.

1. Stop the Alfresco server.

2. Edit your `alfresco-global.properties` file to specify your Elastic Transcoder S3 access key, S3 keys, S3 bucket, and Elastic Transcoder information, for example:

    ```bash
    content.transformer.AwsElasticTranscoder.s3.accessKey=**MY-S3-ACCESS-KEY**
    content.transformer.AwsElasticTranscoder.s3.secretKey=**MY-S3-SECRET-KEY**
    content.transformer.AwsElasticTranscoder.s3.bucketName=**MY-S3-BUCKET-NAME**
    content.transformer.AwsElasticTranscoder.s3.bucketLocation=EU
    # Access and secret keys below can be the same as above
    content.transformer.AwsElasticTranscoder.transcoder.accessKey=**MY-TRANSCODE-ACCESS-KEY**
    content.transformer.AwsElasticTranscoder.transcoder.secretKey=**MY-TRANSCODE-SECRET-KEY**
    content.transformer.AwsElasticTranscoder.transcoder.pipelineId=**MY-PIPELINE-ID**
    content.transformer.AwsElasticTranscoder.transcoder.region=EU_WEST_1
    content.transformer.AwsElasticTranscoder.transcoder.defaultPreset.video/mp4=1351620000001-000010
    ```

    A sample `alfresco-global.properties` file is shipped in the root folder of the Media Management distribution zip, which defines custom properties.

    > **Note:** Elastic Transcoder provides the following support only:

    * `mp4` container
    * `H.264` video
    * `AAC` audio
    Each job must be submitted to a configured preset, which means that Elastic Transcoder handles `TransformationOptions` of type `AwsElasticTranscoderTransformationOptions with a valid awsTranscodePresetId` only. Additionally, Elastic Transcoder does not report percentage progress on jobs.

    For more information on using Amazon Elastic Transcoder with S3, see [Getting started with Elastic Transcoder](http://docs.aws.amazon.com/elastictranscoder/latest/developerguide/getting-started.html){:target="_blank"}.

3. Start your Alfresco server to apply the changes.

## Configuring a CloudFront publishing channel

You can configure Content Services to use the AWS CloudFront publishing channel to make content available outside your organization.

Configure a publishing channel to allow you upload and manipulate content in the Amazon CloudFront Content Delivery Network (CDN).

Ensure that you have installed the required external and internal software before configuring the transformer. See [Prerequisites for using Media Management]({% link media-management/latest/install/index.md %}) for more information. Make sure you have your Amazon S3 account set up.

1. Start Alfresco Share and click Admin Tools from the toolbar, and Content Publishing > Channel Manager.

    The Channel Manager section lists the channels that are configured for users to publish media.

2. Click New and the CloudFront channel type.

    A Channel Authentication screen is displayed.

3. Enter your AWS credentials in the User Name and Password fields.

    Use your S3 access key in the User Name field, and your S3 secret key in the Password field.

    A new channel is created.

4. You can edit the user groups and permissions (using the Permissions option), or reauthorize with new credentials or delete the channel.

    Additionally, if you click the icon for the channel you created, an Edit Channel window appears. From this window you can perform these actions:

    * Edit the name of the channel
    * S3 Bucket Name: define the Amazon S3 bucket that is used for the channel (mandatory field)
    * S3 Path: define the Amazon S3 path
    * S3 Region: define the Amazon S3 region
    * Distribution Domain Name: define the preferred domain name for distribution
    You can create channels for different S3 buckets, paths or distribution domain names, for example, a campaign-specific channel for Marketing, and a web channel for final website content.

## Configuring custom XMP metadata extraction

You can map custom XMP (Extensible Metadata Platform) metadata fields to custom Alfresco data model properties using `alfresco-global.properties`.

Ensure that you have installed the required external and internal software before configuring the transformer. See [Prerequisites for using Media Management]({% link media-management/latest/install/index.md %}) for more information.

1. Stop the Alfresco server.

2. Edit your `alfresco-global.properties` file to specify your custom metadata properties, for example:

    ```bash
    metadata.extracter.TikaExifTool.extract.namespace.prefix.cm=http://www.alfresco.org/model/content/1.0
    metadata.extracter.TikaExifTool.extract.namespace.prefix.custom=http://example.com/model/custom/1.0
    metadata.extracter.TikaExifTool.extract.XMP-custom\:Text=custom:text
    # Force multi-line parsing with []
    metadata.extracter.TikaExifTool.extract.XMP-custom\:TextML[]=custom:textMultiLine
    metadata.extracter.TikaExifTool.extract.XMP-custom\:Date=custom:date
    metadata.extracter.TikaExifTool.extract.XMP-custom\:Integer=custom:integer
    metadata.extracter.TikaExifTool.extract.XMP-custom\:ClosedChoice=custom:closedChoice
    metadata.extracter.TikaExifTool.extract.XMP-custom\:OpenChoice=custom:openChoice
    metadata.extracter.TikaExifTool.extract.XMP-custom\:Boolean=custom:boolean
    ```

    A sample `alfresco-global.properties` file is shipped in the root folder of the Media Management distribution zip, which defines custom properties.

    The `metadata.extracter.TikaExifTool.extract.XMP-custom\:Text` attribute specifies simple text fields. The `metadata.extracter.TikaExifTool.extract.XMP-custom\:TextML[]` attribute specifies multi-line text fields for metadata extraction.

3. Start your Alfresco server to apply the changes.

## Configuring storyboard thumbnails for Media Management

Use this information to configure storyboard thumbnails for video.

Storyboard thumbnails are images shown at regular intervals along the timeline of a video, that show the progress of the video as you hover over the timeline. These thumbnails are shown on videos rendered using an HTML5 player. If you do not want to use the default settings, you can configure this thumbnail information.

1. Stop the Alfresco server.

2. Edit your `alfresco-global.properties` file to specify when the thumbnails start, the interval and number of thumbnails shown in a timeline, for example:

    ```bash
    video.thumbnail.defaultOffset=00:00:00.5
    video.thumbnail.storyboardIntervalSeconds=2
    video.thumbnail.storyboardMaxElements=30
    ```

    A sample `alfresco-global.properties` file is shipped in the root folder of the Media Management distribution zip, which defines custom properties.

3. Start your Alfresco server to apply the changes.

## Setting up a new proxy for Media Management

Use this information to configure an new proxy rendition.

The standard H.264 proxy is used for video transformations in Media Management. This proxy is called in `tomcat/webapps/alfresco/WEB-INF/classes/alfresco/module/org\_alfresco\_mm\_repo/alfresco-mm-standard-context.xml`.

1. If you need to use a different proxy, you can use the standard proxyDefinition720p bean as a template:

    ```xml
    <bean id="proxyDefinition720p" class="org.alfresco.repo.thumbnail.DeletingThumbnailDefinition">
      <property name="name" value="h264-720"/>
      <property name="mimetype" value="video/mp4"/>
      <property name="transformationOptions">
       <bean class="org.alfresco.repo.content.transform.GytheioPassthroughTransformationOptions">
        <property name="gytheioTransformationOptions">
         <bean class="org.gytheio.content.transform.options.VideoTransformationOptions">
          <property name="resizeOptions">
           <bean class="org.gytheio.content.transform.options.ImageResizeOptions">
            <property name="width" value="1280"/><property name="height" value="720"/>
            <property name="maintainAspectRatio" value="true"/>
           </bean>
          </property>
          <property name="targetVideoCodec" value="h264"/>
          <property name="targetVideoBitrate" value="2400000"/>
          <property name="targetVideoFrameRate" value="29.97"/>
          <property name="targetAudioCodec" value="aac"/>
          <property name="targetAudioBitrate" value="160000"/>
          <property name="targetAudioSamplingRate" value="44100"/>
          <property name="targetAudioChannels" value="2"/>
          <property name="additionalOptions">
           <map>
            <entry key="AWS_TRANSCODE_PRESET_ID" value="1351620000001-000010"/>
           </map>
          </property>
         </bean>
        </property>
        <property name="timeoutMs" value="${system.thumbnail.definition.default.timeoutMs}"/>
        <property name="readLimitTimeMs" value="${system.thumbnail.definition.default.readLimitTimeMs}"/>
        <property name="maxSourceSizeKBytes" value="${system.thumbnail.definition.default.maxSourceSizeKBytes}"/><property name="readLimitKBytes" value="${system.thumbnail.definition.default.readLimitKBytes}"/>
        <property name="pageLimit" value="${system.thumbnail.definition.default.pageLimit}"/>
        <property name="maxPages" value="${system.thumbnail.definition.default.maxPages}"/>
       </bean>
      </property>
      <property name="placeHolderResourcePath" value="alfresco/thumbnail/thumbnail_placeholder_256.png"/>
      <property name="mimeAwarePlaceHolderResourcePath" value="alfresco/thumbnail/thumbnail_placeholder_256{0}.png"/><property name="runAs" value="System"/>
      <property name="failureHandlingOptions" ref="standardFailureOptions"/>
      <property name="deleteOnContentUpdate" value="true"/>
    </bean>
    ```

2. Change the bean id, value and property name, and any H.264 proxy specific attributes to reflect your new proxy.
---
title: Start Media Management
---

You need to start up ActiveMQ, your content services node, the repository and Alfresco Share.

Ensure that you have installed the required external and internal software before installing Alfresco Media Management. See [Prerequisites for using Media Management]({% link media-management/latest/install/index.md %}#prerequisites-for-media-management) for more information.

For information on how to set up ActiveMQ and the content services node to start automatically, see [Running Media Management automatically](#running-media-management-automatically).

For more information on advanced ActiveMQ settings, see [Configuring advanced settings in ActiveMQ]({% link content-services/latest/config/activemq.md %}#advanced).

1. Navigate to the `activemq/bin` directory where `activemq` is the name of the directory where you installed ActiveMQ. Start ActiveMQ using the command:

    ```bash
    ./activemq start
    ```

    ```bash
    activemq start
    ```

    ActiveMQ is used by the repository to queue event notifications as they are generated.

    You can check that ActiveMQ is working correctly through the ActiveMQ web interface here: `http://localhost:8161/admin/index.jsp`, where localhost is the Alfresco server.

2. From the remote-node directory, launch your content services node using the following command:

    ```bash
    java -jar content-services-node-x.x.x.jar server config.yml
    ```

    where `x.x.x` is the version of the JAR file. If there is no command line output or error messages, then the node has started successfully. If ImageMagick or FFmpeg are not correctly installed, the node will not start.

3. Start your Alfresco server, and log in to Share.

## Running Media Management automatically

You can configure the Media Management components (Apache ActiveMQ and content services nodes) to suit your specific requirements.

These topics explain how to configure Media Management to run automatically in a production environment.

> **Note:** These instructions are for a Unix environment only.

These topics use `init.d` scripts. For more information on using these scripts, see [Init scripts](https://www.linux.com/training-tutorials/managing-linux-daemons-init-scripts/){:target="_blank"}.

Make sure you have set the correct permissions before configuring Media Management to run automatically.

## Configuring ActiveMQ to run automatically

ActiveMQ can be configured to start and run automatically.

1. Create a user named `activemq` that you will use to run the ActiveMQ automatic process:

    ```bash
    sudo useradd -m activemq
    ```

2. Create an `init.d` script, for example, in /etc/init.d/activemq to run the ActiveMQ shell script under the `activemq` user:

    ```bash
    #!/bin/bash
    # chkconfig: 2345 80 20
    cd opt/activemq
    /bin/su activemq -c "bin/activemq $@"
    ```

3. Make the file executable and enable the script:

    ```bash
    chmod +x /etc/init.d/activemq
    chkconfig --add activemq
    ```

## Configuring the content services node to run automatically

A content services node in Media Management can be configured to start and run automatically.

Review the recommended [architecture]({% link media-management/latest/index.md %}) for guidance on setup of your Alfresco server and remote server.

These instructions are for a Unix environment only and use an `init.d` script. For more information on using these scripts, see [Init scripts](https://www.linux.com/training-tutorials/managing-linux-daemons-init-scripts/){:target="_blank"}.

1. Create a new directory, `/opt/contentservices`, and move the files from the `remote-node` installation directory to the new directory.

    See [Installing Media Management]({% link media-management/latest/install/index.md %}) for more information on the shipped Media Management installation files.

2. Create a user named `contentservices` that you will use to run the automatic process, with a home set to `/opt/contentservices`:

    ```bash
    sudo useradd -m contentservices
    ```

3. Create an `init.d` script, for example, in `/etc/init.d/contentservices` to run the content services node under the `contentservices` user:

    ```bash
    #!/bin/bash
    # chkconfig: 345 91 9
    # description: Alfresco Content Service
    ### BEGIN INIT INFO # Provides: Alfresco MM Module Content Service
    # Required-Start: $local_fs $network $activemq
    # Required-Stop: $local_fs $network $activemq
    # Default-Start: 3 4 5
    # Default-Stop: 0 1 6
    # Description: Start the program
    ### END INIT INFO

    ### Fill in these bits:
    USER="contentservices"
    JAR_LOCATION=/opt/contentservices
    PID_FILE="/var/run/contentservices/contentservices.pid"
    JAR_VERSION=0.3-SNAPSHOT
    JAR_FILE=content-services-node-$JAR_VERSION.jar
    START_CMD="\"cd $JAR_LOCATION;java -jar $JAR_FILE server config.yml > /dev/null 2>&1 &\""
    NAME="alfresco-contentservices"
    PGREP_STRING="$JAR_FILE"

    ### No Changes required below this point

    CUR_USER=`whoami`

    killproc() {
      pkill -u $USER -f $PGREP_STRING
    }

    start_daemon() {
      eval "$*"
    }

    log_success_msg() {
      echo "$*"
      logger "$_"
    }

    log_failure_msg() {
      echo "$*"
      logger "$_"
    }

    check_proc() {
      pgrep -u $USER -f $PGREP_STRING
          >/dev/null
    }

    start_script() {
      if [ "${CUR_USER}" != "root" ] ; then
        log_failure_msg "$NAME can only
          be started as 'root'."
        exit -1
      fi

      check_proc
      if [ $? -eq 0 ]; then
        log_success_msg "$NAME is
          already running."
        exit 0
      fi

      [ -d /var/run/$NAME ] || (mkdir /var/run/$NAME )

      # For SELinux we need to use 'runuser' not 'su'
      if [ -x "/sbin/runuser" ]; then
         SU="/sbin/runuser -s /bin/sh"
      else
         SU="/bin/su -s /bin/sh"
      fi
      start_daemon $SU $USER -c "$START_CMD"

      # Sleep for a while to see if anything cries
      sleep 5
      check_proc

      if [ $? -eq 0 ]; then
        log_success_msg "Started $NAME."
       else
        log_failure_msg "Error starting $NAME."
        exit -1
      fi
    }

     stop_script() {
      if [ "${CUR_USER}" != "root" ] ; then
        log_failure_msg "You do not have permission to stop $NAME."
        exit -1
      fi

      check_proc
      if [ $? -eq 0 ]; then
        killproc -p $PID_FILE >/dev/null

        # Make sure it's dead before we return
        until [ $? -ne 0 ]; do
          sleep 1
          check_proc
        done

        check_proc
        if [ $? -eq 0 ]; then
          log_failure_msg "Error stopping $NAME."
          exit -1
        else
          log_success_msg "Stopped $NAME."
        fi
      else
        log_failure_msg "$NAME is not running or you don't have permission to stop it"
      fi
    }

    check_status() {
      check_proc
      if [ $? -eq 0 ]; then
        log_success_msg "$NAME is running."
      else
        log_failure_msg "$NAME is stopped."
        exit -1
      fi
    }

    case "$1" in
      start)
        start_script
        ;;
      stop)
        stop_script
        ;;
      restart)
        stop_script
        start_script
        ;;
      status)
        check_status
        ;;
      *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
    esac

    exit 0
    ```

4. Make the file executable and enable the script:

    ```bash
    chmod +x /etc/init.d/contentservices
    chkconfig --add alfresco-contentservices
    ```

5. Modify the `config.yml` file to specify your environment settings, for example, your ActiveMQ host name if it is on a different server:

    ```yaml
    messaging:
    broker:
      url: tcp://localhost:61616
    ```

    The content services node uses ImageMagick and FFmpeg and requires that the executable directories are available on the system PATH variable.

    For more information about the content services framework, see [Content services node architecture]({% link media-management/latest/index.md %}).

6. Ensure that the target server port is open and not blocked by a firewall.
---
title: Install Media Management
---

The Media Management capability in Alfresco is delivered as a zip file containing AMP files, an instance of ActiveMQ, and the content services node infrastructure.

In these topics you will set up ActiveMQ, install the AMP files into an existing Alfresco instance, configure your settings and start Media Management.

## Prerequisites for Media Management

There are a number of prerequisite software requirements for Media Management before you start the installation.

You require one of each of the following components.

|Requirement|Description|
|-----------|-----------|
|Software|{::nomarkdown}<ul><li>FFmpeg 2.5.4 from the command line for video transformations.  Make sure that your FFmpeg installation has support for H.264 and AAC codecs. If FFmpeg is not available locally, Media Management functionality is reduced.</li><li>ExifTool 9.76 from the command line for full IPTC metadata extraction.</li><li>Apache ActiveMQ 5.15 or later.</li><li>ImageMagick 6.8.6-6 for image manipulation.</li></ul>{:/}**Note:** If you are using RAW image formats, you must install an ImageMagick delegate, for example, UFRaw, to manipulate the images. See [UFRaw](http://ufraw.sourceforge.net/){:target="_blank"} for more information. To preview RAW image formats, you need to set additional configuration properties. See [step 8](#install-the-media-management-amp-files).**Note:** [FFmpeg](http://ffmpeg.org){:target="_blank"} and [ExifTool](http://www.sno.phy.queensu.ca/~phil/exiftool/){:target="_blank"} are required to view media in Share. See [step 8](#install-the-media-management-amp-files) for information on how to set these in the `alfresco-global.properties` file. See [Configure ActiveMQ]({% link content-services/latest/config/activemq.md %}) for more information about installing ActiveMQ. See [Install ImageMagick]({% link content-services/latest/install/zip/additions.md %}#install-imagemagick) for more information about installing ImageMagick.|
|Alfresco Content Services|Content Services 6.2. See [Supported Platforms]({% link content-services/latest/support/index.md %}) for more information.|
|Java requirements|OpenJDK 11 or later.|
|Remote transformation services (optional)|AWS Elastic Transcoder. See [AWS](http://aws.amazon.com/elastictranscoder/){:target="_blank"} and [Configuring the Elastic Transcoder content transformer]({% link media-management/latest/config/index.md %}) for more information.|

## Install the Media Management AMP files

Download and install the Media Management AMP files, and add Media Management properties to your `alfresco-global.properties` file. Ensure that you have installed the required external software before installing Alfresco Media Management. See [Prerequisites for Media Management](#prerequisites-for-media-management) for information on what you require before you start the installation.

1. Stop the Content Services server.

2. Unzip the Alfresco Media Management package into a new system directory, for example, `opt/media-management`:

    `alfresco-mm-distribution-1.4.x.zip`

    The ZIP file contains the following folders:

    * `activemq`: contains ActiveMQ software
    * `amps-repository`: contains one AMP file to be applied to the Content Services repository
    * `amps-share`: contains one AMP file to be applied to Alfresco Share
    * `remote-node`: contains content services node software and configuration file
    If you are using the recommended [Media Management architecture]({% link media-management/latest/index.md %}#media-management-architecture), the `activemq`, `amps-repository` and `amps-share` folders reside on the Content Services server, and you must move the `remote-node` folder to your remote server.

3. Install the repository AMP file. Navigate to the `amps-repository` directory and copy the following file to the `amps` folder.

    `alfresco-mm-repo-1.4.x.amp`

4. Install the Share AMP file. Navigate to the amps_share directory and copy the following file to the amps_share directory.

    `alfresco-mm-share-1.4.x.amp`

5. Delete the `tomcat\webapps\alfresco` and `tomcat\webapps\share` folders in the Content Services installation directory.

6. Navigate to the `bin` directory and run the Module Management Tool (MMT) file to install the repository AMP files:

    1. For the Content Services repository:

        ```bash
        java -jar alfresco-mmt.jar install ../amps/alfresco-mm-<version>.amp ../tomcat/webapps/alfresco.war
        ```

        ```bash
        java -jar alfresco-mmt.jar install ..\amps\alfresco-mm-<version>.amp ..\tomcat\webapps\alfresco.war
        ```

        where `alfresco-mm-<version>.amp` is the specific AMP file that you downloaded.

    2. For Alfresco Share:

        ```bash
        java -jar alfresco-mmt.jar install ../amps_share/alfresco-mm-<version>.amp ../tomcat/webapps/share.war
        ```

        ```bash
        java -jar alfresco-mmt.jar install ..\amps_share\alfresco-mm-<version>.amp ..\tomcat\webapps\share.war
        ```

        where `alfresco-mm-<version>.amp` is the specific AMP file that you downloaded.

    Check the output to ensure that the AMP files have installed successfully.

7. Take a copy of the most recent `tomcat/webapps/alfresco.war<numbers>.bak` file in case you need to uninstall Media Management.

8. Define properties relevant to Media Management in your `alfresco-global.properties` file.

    A sample `alfresco-global.properties` file is shipped in the root folder of the Media Management distribution zip, which defines custom properties. See [Configure Media Management]({% link media-management/latest/config/index.md %}) for the full list.

    1. If you have ActiveMQ on a separate server, configure the host and port number for ActiveMQ:

        ```bash
        # Messaging broker, default is localhost
        messaging.broker.url=failover:(tcp://broker1:61616,tcp://broker2:61616)
        ```

        where `broker` is each ActiveMQ instance that you have configured.

        You need to set this property only if your ActiveMQ instance is not on the same server as Content Services.

    2. Configure FFmpeg and ExifTool if they are not already available on the command line executable path:

        ```bash
        # FFmpeg executable path, default is ffmpeg
        ffmpeg.exe=

        # ExifTool executable path, default is exiftool
        exiftool.exe=
        ```

    3. If you want to preview raw images, set the following properties in the `alfresco-global.properties` file.

        ```bash
        transformer.strict.mimetype.check=true
        transformer.strict.mimetype.check.whitelist.mimetypes=image/x-raw-adobe
        ```

        Set the `transformer.strict.mimetype.check` property to `true`, and use the `transformer.strict.mimetype.check.whitelist.mimetypes` property to add the `x-raw-adobe` MIME type to an existing whitelist.

    4. If you are using shared content workspaces, remote transformations or publishing channels, configure these as specified in [Configure Media Management]({% link media-management/latest/config/index.md %}).

9. Update the `remote-node/config.yml` file that you extracted from the Media Management installation zip.

    Specify the ActiveMQ host name and prefetch policy (to ensure that transformations can be processed in parallel):

    ```bash
    messaging:
    broker:
      url: tcp://localhost:61616?jms.prefetchPolicy.queuePrefetch=1
    ```

    The content services node uses ImageMagick and FFmpeg and requires that the executable directories are available on the system PATH variable or are specified using `img.exe` and `ffmpeg.exe` system properties.

    For more information about the recommended architecture for Media Management, see [Media Management architecture]({% link media-management/latest/index.md %}#media-management-architecture). For information about the content services framework, see [Content services node architecture]({% link media-management/latest/index.md %}#content-services-node-architecture).

10. Restart the server.

11. Launch Alfresco Share.

    To check that the Media Management AMPs have installed correctly, add a video or image to Share, open the file and check that you can see that the media loading and a Renditions Panel is available.

## Uninstalling Media Management

To uninstall Media Management, you need to use the Module Management Tool (MMT) and reinstate certain files.

1. Stop the Content Services server.

2. Use the topic, [Uninstall an AMP file]({% link content-services/latest/install/zip/amp.md %}), to uninstall the module.

3. If you have used a Media Management content model like IPTC or PBCore, you must clean out your database before restarting Alfresco. See [Dynamic deployment approach]({% link content-services/latest/develop/repo-ext-points/content-model.md %}#dynamic-deployment-approach) for more information.

4. Restart the Alfresco server.
---
title: Supported platforms
---

The following are the supported platforms for Alfresco Media Management 1.4:

| Version | Notes |
| ------- | ----- |
| Content Services 6.2 | |
---
title: Alfresco Media Management video tutorials
---

Watch these videos to see what you can do with Alfresco Media Management.

## Admin settings

Learn about transformer settings, creating publishing channels and setting site themes in Media Management.

> **Note:** This video contains functionality that's no longer available in Media Management, i.e. the Brightcove publishing channel.

{% include media.html id="CHGBxV7DarE" %}

## Editing images

Learn how to edit and manipulate images with Media Management.

{% include media.html id="PF6OmNwP0jE" %}

## Editing videos

Learn how to edit and manipulate videos with Media Management.

{% include media.html id="-T0o52KJ1LE" %}

## Working with metadata

Learn how to embed and view metadata in Media Management.

{% include media.html id="hR3PpZhDFqs" %}
---
title: Using Media Management
---

Alfresco Media Management allows you to view and manipulate your digital assets in Alfresco Content Services.

Features provided with Media Management include video support and enhanced image manipulation, for example, video thumbnails and proxies, video trim, time-coded comments for video, and image crop and rotate capabilities. A dark site theme is also available.

You can embed metadata into a file using rules, with the Embed properties as metadata in content action, and view metadata in Alfresco and in an image editor. See [Working with metadata]({% link media-management/latest/tutorial/index.md %}#working-with-metadata) for more information about extracting and embedding metadata.

> **Note:** Video transformations are very resource intensive and can take a long time to complete. Make sure that any rules that you create that use video transcoding run in the background, to prevent the rule from failing due to an Alfresco timeout. For more information about creating rules, see [Creating a rule]({% link content-services/latest/using/content/rules.md %}).

Media Management is integrated with AWS CloudFront publishing channel for publishing your content.

## Uploading media

Media Management provides information and features about media files that you upload in Content Services.

1. Select the folder in the Document Library where you want to add your content.

2. You can drag and drop images or videos, or select Upload from the toolbar, as you would normally do in Alfresco.

    You will see the image or video in File Preview. If you upload a video, the duration of the video is shown in the information below the name of the video, for example, this is the icon that you would see if the video is three minutes and seven seconds long.

    A rendition or proxy is a version of the original video or image, for example, a copy of an image that is optimized for web viewing. By default, not all renditions (including video) are created after uploading. It is only when a user first views the image or video that a rendition is created.

   >**CAUTION:** Creating video proxies (when viewing videos for the first time) is very resource intensive. You might experience very slow performance while this is occurring unless your Alfresco administrator has configured additional resources to process this workload.

## Viewing media

Alfresco Media Management provides additional information and features in Alfresco when you view image or video files.

1. Select an image or video in the Document Library, as you would normally in Alfresco, by clicking the thumbnail or name, to view it in the file preview screen.

2. You will see additional preview options relating to the image or video:

    * **Renditions** panel, which shows the different options that are available for this image or video. These might include a low resolution thumbnail, a medium size JPEG file for an image, or H.264 proxy for video.
    * PBCore additions to the **Properties** panel, including the duration of a video, data rate, frame rate, and sampling rate.
    * IPTC additions in the **Properties** panel, including informational metadata like IPTC contact information, IPTC scene codes, headline and description.

        > **Note:** IPTC metadata is mapped to existing tags. For example, the IPTC Caption/Description is also displayed on the Document Library view of an image or video, if this field is present.

3. If you are the first user to open a video file, you will see a progress bar indicating the time estimated for the video to load.

    For example: ![Progress bar]({% link media-management/images/generating_video.png %})

    **Note:** This progress bar is not visible if AWS Elastic Transcoder is set up in your organization to process your video content.

    The progress bar is visible only on the first upload of a video. After it has been loaded once, this video is available to all users to view, without delay.

    >**Note:** Creating video proxies (when viewing videos for the first time) is very resource intensive. You might experience very slow performance while this is occurring unless your Alfresco administrator has configured additional resources to process this workload.

## Manipulating video

Alfresco Media Management provides features to allow you to edit video files in Content Services.

1. Select a video file from the Document Library, as you would normally in Alfresco, by clicking the thumbnail or name, to view it in the file preview screen.

2. Click the arrow to play the video, and then click the ![pencil icon]({% link media-management/images/pencil.png %}) edit icon.

    * ![trim video icon]({% link media-management/images/trim.png %}): Trim the video length. Before clicking this icon you need to move the yellow sliders shown above the video timeline to your preferred start and end times.
    * Create Copy: click the checkbox before selecting the trim icon to save a copy of the image. The trimmed image is created in the same folder with the name Copy of original, where original is the name of your original image. If more than one copy is taken, the name is Copy x of originalimage, where x relates to the number of copies taken.
    Each time that the video is edited, it is stored as a new version of the original video (as long as the video is versionable), unless the Create Copy checkbox is selected.

3. You can add a comment in the usual way by clicking Add Comment, however with Media Management you can add this to the timeline of the video:

    1. Click Add Comment while the video is playing.

    2. Click the From box and click the ![current playback position icon]({% link media-management/images/playback.png %}) current playback position icon, at the point where you want to make a comment.

        You can optionally add an end time, in the format HH:MM:SS:MS.

    3. When you (or another user) next view the video, yellow markers (timecode markers) indicate where the timeline comments have been placed.

        When you hover on the yellow marker, the comment is displayed. A new icon, ![closed caption icon]({% link media-management/images/cc.png %}), is now available on the video control bar, which allows you to toggle the comments as subtitles on the video.

## Manipulating images

Alfresco Media Management provides features to allow you to edit image files in Alfresco.

1. Select an image from the Document Library, as you would normally in Alfresco, by clicking the thumbnail or name, to view it in the file preview screen.

2. Click the ![pencil icon]({% link media-management/images/pencil.png %}) edit icon, and perform these actions to edit the image directly in Alfresco:

    * ![crop icon]({% link media-management/images/crop.png %}): hold down your left mouse button to select an area of the image, and click the icon to crop the image
    * ![Rotate clockwise icon]({% link media-management/images/clock.png %}): click the icon to rotate the image clockwise
    * ![Rotate counterclockwise icon]({% link media-management/images/anticlock.png %}): click the icon to rotate the image counterclockwise
    * Create Copy: click the checkbox before selecting either of the rotate icons to take a copy of the image. The rotated image is saved in the same folder with the name Copy of original, where original is the name of your original image. If more than one copy is taken, the name is Copy x of originalimage, where x relates to the number of copies taken.
    Each time the image is edited, it is stored as a new version of the original image (as long as it is versionable), unless the Create Copy checkbox is selected.

    You can also use the scroll wheel to navigate large images.

## Transforming rich media

Alfresco Media Management allows you to request transformations of media from one format to another.

There are several methods used to request rich media transformations, and the method depends on the type of relationship that exists between the original source and the transformation result.

Renditions, for example, lower resolution JPEG image and video proxy files, are often requested automatically, when required in Alfresco. For example, they are requested when browsing a site's document library or navigating to the document details page.

You can explicitly request a rendition by clicking the **+** icon in the **Renditions** panel of the document details page. See [Viewing media]({% link media-management/latest/using/index.md %}#viewing-media) for more information about the Renditions panel.

You can perform an ad hoc format transformation in a number of ways, for example, create a rule with a Transform and Copy Content action. See [Applying rules to folders]({% link content-services/latest/using/content/rules.md %}) for more information about setting up rules.

## Publishing media

Alfresco Media Management provides publishing options in Alfresco.

1. In the Document Library, click the title of the file you want to view.

2. Select Publish from the Document Actions panel and choose the channel you want to publish to (for example, CloudFront. You can optionally add a message).

    This option allows you to publish content to CloudFront, as long as your Alfresco administrator has set up a publishing channel.

3. The Publishing History panel in the preview screen updates with the version of the media and the channel that you selected to publish the media.

## Using an Alfresco dark site theme

Alfresco Media Management provides a black background (dark theme) for Share, that mutes elements until they are required, and makes it easier to work with rich media content. If you're a site administrator you can enable this theme.

For more information about using themes in general, see [Share themes]({% link content-services/latest/develop/share-ext-points/share-config.md %}#sharethemeconfig). Only an administrator can enable a theme.

1. From the Content Services toolbar, select Admin Tools and click Application in the Tools list.

    The Options page appears.

2. Select Dark Theme from the menu.

    The new theme now displays every time that you use Alfresco unless you choose to change it again.
