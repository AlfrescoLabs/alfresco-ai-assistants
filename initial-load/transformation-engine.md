---
title: Alfresco Document Transformation Engine
---

The Document Transformation Engine is a stable, fast, and scalable solution for high-quality transformations of Microsoft Office documents (Word, Excel, and PowerPoint only) to PDF. It is an enterprise alternative to LibreOffice. It is an Alfresco Content Services module that is enabled with a license key.

The engine features an open architecture and offers the following features:

* **High quality**: The Document Transformation Engine uses genuine Microsoft Office software to transform Word, Excel, and PowerPoint documents to PDF. This guarantees the handling of the supported file types and pixel-perfect transformations, and it corrects previous layout issues in the Share preview feature.

    The Document Transformation Engine can also be used to convert emails to PDFs. This is a useful feature in conjunction with the Outlook Plugin.

* **Scalable**: The Document Transformation Engine communicates with Alfresco Content Services using an HTTP REST API, which means that you can scale up by adding multiple instances of the engine and connecting them through a standard HTTP Network Load Balancer.

* **Stable**: If Microsoft Office can open and transform your document, then so can the Document Transformation Engine. Robust error handling will take care of corrupt and encrypted documents. A Web Console shows you a detailed report if there is a problem during transformation, allowing you to correct documents.

* **Fast**: The Document Transformation Engine is two to three times faster when transforming multi-megabyte Office documents when compared with LibreOffice on the same hardware.

* **Extensible format support**: The Document Transformation Engine supports the transformation of MS Office formats.
---
title: Administer the Document Transformation Engine
---

The Document Transformation Engine can be integrated with monitoring tools such as Nagios or Hyperic, by using HTTP REST calls.

The tool should call the Document Transformation Engine URL with a set of parameters and then monitor the response.

Two calls are available:

* Connection tester call

    This call is also used by the Alfresco Transformation client to test availability. It checks the transformation service is up and responding.

    1. URL: `http://<transformation-host>:<port>/transformation-backend/service/transform/v1/version`

    2. HTTP Method: `GET`

    3. Make sure that you include basic authentication credentials to your call.

* Transformation execution call

    This call gets an Office file from the Transformation Service to check whether the transformation engine is still functioning (the Transformation Service makes an internal post, but the HTTP method is still a GET call). This can be used for more in-depth monitoring.

    1. URL: `http://<transformation-host>:<port>/transformation-backend/service/transform/v1/available`

    2. HTTP Method: `GET`

    3. Make sure that you include basic authentication credentials to your call.
---
title: Configure the Document Transformation Engine
---

The standalone Document Transformation Engine can be configured using the Web Console. You only need to change the password of the transformation service.

1. Open your browser and navigate to `http://<transformation-host>:<port>/transformation-server/#/settings` or `https://` if you are using SSL.

2. Enter your login name and a password.

    By default, the login name is set to `alfresco`, and the password is set to `alfresco`. The login name `alfresco` cannot be changed.

3. Enter a new password, and then click **Change** to save the password.

<!-- WILL NEED ADDING BACK IN FOR 3.2.1
4. To set up SSL with the Document Transformation Engine, update or replace the keystore in the default location: `C:\\Program Files (x86)\\TransformationServer\\tomcat\\conf\\.keystore` using the method described in [Configuring SSL for a test environment]({% link content-services/latest/admin/security.md %}#managealfkeystores).

    See [Managing Alfresco keystores]({% link content-services/latest/config/repository.md %}#configure-ssl-for-a-test-environment) for more information about keystores.

## Configure the Alfresco Transformation client

There are three ways to configure the Alfresco Transformation client:

* Using the `alfresco-global.properties` file
* Using a JMX client, if you have installed the Oracle Java SE Development Kit (JDK)
* Using the `default-configuration.properties` file

### Transformation timeout considerations

There are a number of timeout settings in Alfresco Content Services that affect the Document Transformation Engine. These are the defaults:

```bash
content.transformer.default.timeoutMs=120000
transformserver.transformationTimeout=300
transformer.timeout.default=300
```

`content.transformer.default.timeoutMs` is the system transformation timeout (set to 120000 milliseconds by default), but the Document Transformation Engine is controlled by `transformserver.transformationTimeout` and `transformer.timeout.default`. This means that with the default settings, Alfresco Content Services stops processing after 120 seconds, whereas the Document Transformation Engine attempts to transform a document for up to 300 seconds and any results returned after 120 seconds are ignored.

Set the following to configure the Document Transformation Engine to stop processing at the same time as the default system transformation timeout:

```bash
transformserver.transformationTimeout=120
transformer.timeout.default=120
```

### Configuration using the `global-properties.file`

You configure the Alfresco Transformation client by adding the relevant properties to the global properties file.

1. Open the `alfresco-global.properties` file.

2. Add the required properties for configuration settings on the Alfresco Transformation client.

3. Save the `alfresco-global.properties` file, and then restart your server.

The following table shows an overview of the available properties:

| Property | Description |
| -------- | ----------- |
|transformserver.aliveCheckTimeout | Sets the timeout for the connection tester in seconds. If the Document Transformation Engine does not answer in this time interval, it is considered to be off line. The default value is `2`. |
| transformserver.test.cronExpression | Sets the cron expression that defines how often the connection tester will check. The default is every 10 seconds: `0/10 * * * * ?` |
| transformserver.disableSSLCertificateValidation | Set this property to true to allow self-signed certificates (that is, it is not issued by an official Cert Authority). The default is `false`.|
| transformserver.username | The user name used to connect to the Document Transformation Engine. **Note:** **Do not change** from the default `alfresco`. |
| transformserver.password | The password used to connect to the Document Transformation Engine. **Note:** **Always change** the password from the default `alfresco`. |
| transformserver.qualityPreference | There are two values for this property. The default is `QUALITY`. {::nomarkdown}<ul><li>QUALITY: optimizes the preview for quality.</li><li>SIZE: optimizes the preview for size. This is interesting if you have a lot of big Office documents, for example, PPT file over 100 MB.</li></ul>{:/} |
| transformserver.transformationTimeout | Sets the time in seconds to wait for the transformation to complete before assuming that it has hung and therefore stop the transformation. If you are transforming very large or complex files, this time can be increased. The default is `300`. |
| transformserver.url | The URL of your Document Transformation Engine (or the network load balancer if you are using more then one transformation engine). Use `https://` if you want to use encrypted communication between the Alfresco Content Services server and the Document Transformation Engine. |
| transformserver.usePDF_A | Use this setting to transform PDF to PDF/A or to keep PDF/A in PDF/A format. The default is `false`. |

In a normal setup, you will always overwrite the `transformserver.password` and `transformserver.url` properties. If you want to use SSL encryption with the default certificate of the transformation engine, make sure that you set `transformserver.disableSSLCertificateValidation=true`.

### Configuration using JMX

The Alfresco Transformation client configuration parameters are exposed as JMX MBeans, which means that you can view and set the parameters using a JMX client.

See [Using a JMX client to change settings dynamically]({% link content-services/latest/config/index.md %}#using-jmx-client-to-change-settings-dynamically) for instructions on how to connect a JMX client to your server.

### Configuration using the default configuration properties file

You can configure timeout values in the Alfresco Transformation client by adding the relevant properties to the transformation engine configuration file in `C:\\Program Files (x86)\\TransformationServer\\tomcat\\webapps\\transformation-server\\WEB-INF\\classes\\default-configuration.properties`.

Use the code sample to set these timeouts:

```bash
# transformer timeout in seconds
transformer.timeout.default=300
transformer.timeout.word = ${transformer.timeout.default}
transformer.timeout.excel = ${transformer.timeout.default}
transformer.timeout.powerpoint = ${transformer.timeout.default}
```
-->

## Configure DTE with SSL

Below is a very basic example of how to configure Secure Sockets Layer (SSL) for DTE. It forms a good starting point for customers with experience and competencies in DevOps.

1. Edit `C:\Program Files (x86)\TransformationServer\tomcat\conf\server.xml`:

    For example:

    1. Comment out this connector:

        ```xml
        <Connector executor="tomcatThreadPool"
                port="${https.port}" protocol="org.apache.coyote.http11.Http11NioProtocol"
                SSLEnabled="true">
            <SSLHostConfig>
                <Certificate certificateKeystoreFile="conf/.keystore" certificateKeystorePassword="tomcat" type="RSA" />
            </SSLHostConfig>
        </Connector>
        ```

    2. Uncomment this Connector:

        ```xml
        <Connector executor="tomcatThreadPool"
            port="${https.port}" protocol="org.apache.coyote.http11.Http11NioProtocol"
            SSLEnabled="true" scheme="https" secure="true"
            clientAuth="false" sslProtocol="TLS"
            keystoreFile="PATH_TO_KEYSTORE" keystorePass="KEYSTORE_PASSWORD" />
        ```

2. Check the REST configuration URL under: `https://<dte-hostname>:8443/transformation-server/#/settings`:

    This should be set to: `https://<dte-hostname>:8443`.

3. Edit `alfresco-global.properties`:

    Change `localTransform.transform-dte.url=http://<dte-hostname>:8080/transform-dte`

    to `localTransform.transform-dte.url=https://<dte-hostname>:8443/transform-dte`

For more information on configuring SSL on Tomcat, see the Tomcat documentation [SSL/TLS Configuration How-To](https://tomcat.apache.org/tomcat-9.0-doc/ssl-howto.html){:target="_blank"}.

## Configure HTML sanitizer

Starting from DTE 2.4.2, DTE brings new configuration options to control the behavior for HTML sanitizing when converting HTML files.

There are multiple modes you can choose from:

| Mode | Description |
| ---- | ----------- |
| Blacklist | This is the default setting. You can choose which HTML parts and attributes are not allowed. Ths setting is empty by default, but it stops Server-Side Request Forgery (SSRF) attacks. |
| Whitelist | You can choose which HTML parts and attributes are allowed. This setting is empty by default, but it stops SSRF attacks. |
| None | `None` means there is no sanitization provided at all. SSRF attacks are possible when using this mode, as it re-enables features like embedded script execution or iframe preview. <br><br>**Note:** This mode is not recommended. Administrators - use this setting at your own risk. |

### Default configuration

The default configuration provided in `C:\Program Files (x86)\TransformationServer\tomcat\webapps\transformation-backend\WEB-INF\classes\default-configuration.properties` is shown below:

```text
# Configuration for HTML sanitizer
# Sample configuration for HTML sanitizer
# Modes are WHITELIST, BLACKLIST, NONE (Use at own risk, not recommended)
sanitizer.mode=BLACKLIST
# Only works with BLACKLIST mode. Sample: sanitizer.disallowed.elements=a,script,iframe,style
sanitizer.disallowed.elements=
# Only works with BLACKLIST mode. Sample: sanitizer.disallowed.attributes=a.onclick,a.onmouseover,img.onerror,button.onclick (element.attribute)
sanitizer.disallowed.attributes=
# Only works with WHITELIST mode. Sample: sanitizer.allowed.elements=p,div,span,ul,ol,li,h1,h2,h3,a
sanitizer.allowed.elements=
# Only works with WHITELIST mode. Sample: sanitizer.allowed.attributes=a.href,a.target,img.src,img.alt,div.class (element.attribute)
sanitizer.allowed.attributes=
```

You can override the default configuration in `C:\Program Files (x86)\TransformationServer\tomcat\webapps\transformation-backend\WEB-INF\classes\custom-configuration.properties`.

### Examples

Below are some examples of how to configure the new HTML sanitizer which comes with DTE 2.4.2.

Configuration for `BLACKLIST` mode:

```text
# Configuration for HTML sanitizer
# Sample configuration for HTML sanitizer
# Modes are WHITELIST, BLACKLIST, NONE (Use at own risk, not recommended)
sanitizer.mode=BLACKLIST
# Only works with BLACKLIST mode. Sample: sanitizer.disallowed.elements=a,script,iframe,style
sanitizer.disallowed.elements=a,script,iframe,style
# Only works with BLACKLIST mode. Sample: sanitizer.disallowed.attributes=a.onclick,a.onmouseover,img.onerror,button.onclick (element.attribute)
sanitizer.disallowed.attributes=img.onerror
```

* This mode explicitly disables the following HTML elements: `a`, `script`, `iframe`, and `style`.
* It also explicitly disables the `onError` attribute in `img` elements.

> **Note:** Most of these elements are already sanitized by choosing "BLACKLIST" mode, which also prevents potential SSRF attacks.

Configuration for `WHITELIST` mode:

```text
# Configuration for HTML sanitizer
# Sample configuration for HTML sanitizer
# Modes are WHITELIST, BLACKLIST, NONE (Use at own risk, not recommended)
sanitizer.mode=WHITELIST
# Only works with WHITELIST mode. Sample: sanitizer.allowed.elements=p,div,span,ul,ol,li,h1,h2,h3,a
sanitizer.allowed.elements=p,div,span,ul,ol,li,h1,h2,h3,a
# Only works with WHITELIST mode. Sample: sanitizer.allowed.attributes=a.href,a.target,img.src,img.alt,div.class (element.attribute)
sanitizer.allowed.attributes=img.src
```

* This mode explicitly disables the following HTML elements: `p`, `div`, `span`, `ul`, `ol`, `li`, `h1`, `h2`, `h3`, and `a`.
* It also explicitly disables the `src` attribute in `img` elements.

> **Note:** You cannot enable SSRF critical elements with the whitelist.

Configuration for `None` mode:

```text
# Configuration for HTML sanitizer
# Sample configuration for HTML sanitizer
# Modes are WHITELIST, BLACKLIST, NONE (Use at own risk, not recommended)
sanitizer.mode=NONE
```

> **Important:** This mode is not recommended. Use this at your own risk.

* This mode re-enables all HTML features such as embedded script tag execution or preview of iframes. However, this comes with the cost of potential SSRF attacks.
* If you choose to select this mode, the behavior is exactly the same as older DTE versions prior to 2.4.2.
---
title: Installation overview
---

The standalone Document Transformation Engine runs on Microsoft Windows and provides file transformations.

## Prerequisites

There are a number of important notes to consider when installing the Document Transformation Engine in addition to the [Supported platforms]({% link transformation-engine/latest/support/index.md %}).

* The Document Transformation Engine requires an installation of [Alfresco Transform Service]({% link transform-service/latest/install/index.md %}).

* The standalone Document Transformation Engine requires the software components to be installed and available on the same machine.

* Only install the English versions of Microsoft Windows Server, and Microsoft Office because other languages cause encoding issues resulting in unpredictable behavior.

    > **Note:** Although the engine must be configured in English, this has no impact on the transformation language used for documents.

* Microsoft Office (32-bit and 64-bit).

    > **Note:** Please be advised that the Alfresco Document Transformation Engine (DTE) uses Microsoft Office to automate the creation of high-fidelity renderings of Office document formats; as a result, it is your responsibility as a user of DTE to ensure that you have proper licensing arrangements in place with Microsoft to allow for such automation.

* To enable the Document Transformation Engine to work with non-English documents you must install the desired Microsoft Office language pack of the language you want to work with.

* The Document Transformation Engine does not work with Windows non-English regional settings.

* Make sure that the Windows print spooler service is running.

See [Supported platforms]({% link transformation-engine/latest/support/index.md %}) for more information.

### Sizing

There are a number of recommendations for calculating sizing. You will need:

* Four high clocked cores per engine, with between 4 GB and 6 GB RAM. If you find that you need more power, it is better to add another engine instance with a similar specification than to upgrade the hardware. The reason for this is that Microsoft Office is not very scalable.

* Between 10 GB and 15 GB of free space. Storage is not that important, but if you have lots of large files, you should make sure that creating temporary copies of those files will not slow the system down.

* Gigabit Ethernet.

* At least one CPU for each concurrent transformation that is expected to be processed by the engine.

### Disc I/O bandwidth

Microsoft Office transformations are I/O-heavy, and so on some solutions, I/O contention can be a performance bottleneck. When multiple Word conversions occur in parallel, performance can suffer heavily from poor random read and write speeds.

## Installation

The Document Transformation Engine is installed using an `msi` file where you can select to install a T-Engine at the same time. Alternatively you can install the Document Transformation Engine using the `msi` and use Docker Compose to install the T-Engine. See [Install with MSI]({% link transformation-engine/latest/install/msi.md %}) for more details. There is also an [SDK that can be installed]({% link transformation-engine/latest/install/sdk.md %}).

### Set `JAVA_HOME`

If you're using any JDK which does not set a registry key, you need to manually set the `JAVA_HOME` system variable. This mostly happens when using a `zip` package installation of the JDK.

1. Locate your JDK installation (it's most likely in a directory such as `C:\Program Files\jdk-11.x.x`).
2. Search for **Advanced system settings**.
3. Select **View advanced system settings > Environment Variables**.
4. In the **System variables** section, click **New** (or **User variables** for a single user setting).
5. Add the following settings:

    * Variable name = `JAVA_HOME`
    * Variable value = path to the JDK installation (from step 1).

6. Click **OK** (twice) and finally click **Apply** to save the changes.
---
title: Installation
---

The standalone Alfresco Document Transformation Engine is installed by using an `.msi` file where you can either:

* Select to install a T-Engine wrapper from the `.msi`.
* Install a hybrid version by using a Docker Compose file to install the T-Engine.

In previous versions the installation files were contained within a `.zip` file. This file also contained `.amp` files that enabled you to install the Document Transformation client into Alfresco Content Services. In the current version this is not possible.

* [Install with MSI](#install-with-msi)
* [Install T-Engine using Docker Compose](#install-t-engine-using-docker-compose)

## Install with MSI

> **Note:** When upgrading the Document Transformation Engine, the previous installation must be uninstalled first.
>
> * If your old version is earlier than 1.3.1, use the Control Panel **Uninstall a program** option to remove the old version, and then manually remove the Document Transformation Engine directory. By default, the Document Transformation Engine directory is `C:\Program Files (x86)\Transformation Engine\`.
> * If your old version is 1.3.1 or later, the new Document Transformation Engine MSI prompts you to uninstall the previous version. When the uninstall is complete, you can run the MSI package again to install the new version. There is no need to manually remove anything.

1. Download `alfresco-document-transformation-engine-server-2.4.x.msi` from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2. Log into the Microsoft Windows Server as an administrator.

3. Double click the `.msi` installer package, and then click **Next**.

4. Review the supported software requirements, and then click **Next**.

5. (Optional) Select DTE T-Engine.

    > **Important:** If you do not intend to use the DTE T-Engine Docker image, you must select this option for DTE to work correctly.

    > **Note:**
    >
    >* For Alfresco Content Services 7.x, you can only use the T-Engine approach. Installing the Alfresco Module Packages (AMP) files is no longer supported.
    >* You can use Content Services 6.x with the T-Engine approach and with the old approach (i.e. installing the AMP files in Content Services).

6. Click **Next** and the license information screen displays.

7. Click **Next** and select an installation folder or accept the default folder, and then click **Next**.

8. Click **Next** to start the installation.

    You will see a progress bar and a command line window during the installation. The installer will show a confirmation when the installation is finished.

9. Click **Close** to finish the installation.

10. Verify that the installation has completed successfully.

    1. Check the Windows Services in the management console.

    2. Locate the new service called **Document Transformation Engine**, and check that it is **Started**.

    > **Note:** Each time a file is transformed in Alfresco Content Services, the `.NET` program starts and Microsoft Office tries to check for a Certificate Revocation List (CRL). Depending on the access that the Document Transformation Engine has to the Internet when transforming a file, this check can delay the operation for up to two minutes, and will therefore, delay transformation of the file. To prevent this, use the Windows server firewall to block internet access for all office binaries.

11. Add the following property to `alfresco-global.properties`:

    ```bash
    localTransform.transform-dte.url=http://<dte-hostname>:8080/transform-dte
    ```

## Install T-Engine using Docker Compose

To deploy the Document Transformation Engine T-Engine with the Transform Service, you'll need to update your Docker Compose file to include the Document Transformation Engine T-Engine.

> **Important:** You still need to install the Document Transformation Engine using the `.msi`.

> **Note:** While Docker Compose is often used for production deployments, the Docker Compose file provided is recommended for development and test environments only. Customers are expected to adapt this file to their own requirements, if they intend to use Docker Compose to deploy a production environment.

1. Add the Document Transformation Engine T-Engine container to your `docker-compose.yaml` file:

    ```yaml
    transform-dte-engine:
        image: quay.io/alfresco/transform-dte-engine:1.2.0
        mem_limit: 2g
        environment:
            JAVA_OPTS: " -Xms256m -Xmx512m -DdteServerUrl=http://<dte-hostname>:8080/transformation-backend"
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
    -DlocalTransform.transform-dte.url=http://transform-dte-engine:8090/
    ```

See the Content Services documentation - [T-Engine configuration](https://github.com/Alfresco/acs-packaging/blob/master/docs/creating-a-t-engine.md#t-engine-configuration){:target="_blank"} for more details. For further development, see [Content Transformers and Renditions Extension Points]({% link content-services/latest/develop/repo-ext-points/content-transformers-renditions.md %}).
---
title: Install the SDK
---

Use this information to install the Document Transformation Engine SDK.

Download the Document Transformation Engine SDK from [Hyland Community](https://community.hyland.com/){:target="_blank"}. This is an executable JAR file with all dependencies that works as a command line client. The executable class is `com.westernacher.transformationserver.demo.DemoClient`.

To invoke the Document Transformation Engine SDK JAR file, use the following syntax:

```java
java -jar alfresco-document-transformation-engine-sdk-2.4.x-plain.jar -in input.doc -out output.pdf -url http://trafo-url:8080/transformation-server
```

An API usage example is available at `com.westernacher.transformationserver.demo.ApiUsageExample`. You can copy, modify, and use this code in your own product.

A list of the most important file formats is available at `mimetypes.properties`. These file formats have their mime type auto-detected by the file extension. Note that this is not the full list of supported formats.

The most important source and target formats are:

Source formats:

* Most image formats
* Nearly all Microsoft Word, Excel, and PowerPoint formats
* `.eml` and `.msg` Emails

Target formats:

* PDF and PDF/A
* SWF
* Most image formats

Functions that do not work with the SDK:

* OCR
* Resizing an image, which is necessary to produce thumbnails
* PDF/A as a target format
---
title: Supported platforms
---

The following are the supported platforms for Document Transformation Engine 2.4:

| Version | Notes |  
| ------- | ----- |
| Content Services 23.1.x | *Required.* Use with DTE T-Engine v1.2.0 |
| Content Services 7.4.x | *Required.* Use with DTE T-Engine v1.2.0 |
| Content Services 7.3.x | *Required.* Use with DTE T-Engine v1.2.0 |
| Content Services 7.2.x | *Required.* Use with DTE T-Engine v1.2.0 |
| Content Services 7.1.x | *Required.* Use with DTE T-Engine v1.2.0 |
| Content Services 7.0.x | *Required.* Use with DTE T-Engine v1.2.0 |
| | |
| **Java** | |
| Oracle JDK 11 | |
| | |
| **Microsoft Windows Server** | |
| Microsoft Windows Server 2022 | |
| Microsoft Windows Server 2019 | |
| Microsoft Windows Server 2016 | |
| Microsoft Windows Server 2012 | |
| | |
| **Microsoft Office** | |
| Microsoft Office 2021 32/64 bit | |
| Microsoft Office 2019 32/64 bit | |
| Microsoft Office 2016 32/64 bit | |
---
title: Using the Document Transformation Engine Web Console
---

The Document Transformation Engine is used when you upload files to Alfresco Content Services, and you can see results in the Alfresco Share preview.

Administrators can view information about the engine and transformation errors using the Web Console which shows:

* The status of the engine
* A historical view of all the transformations completed
* The number of successful and failed transformations

**Note:** Only Administrators can access and use the Document Transformation Engine Web Console.

1. To view the Document Transformation Engine Web Console, open a browser and navigate to `http://<transformation-host>:</port>/transformation-server/`, or `https://` if you are using SSL.

    The **Server Status** view is the default view when you open the Web Console. This displays an overview of the health and the memory use of the Document Transformation Engine.

2. Click **History** view.

    Alternatively, you can go directly to the **History** view by navigating to `http://transformation-server/#/history`.

    The **History** view shows the details of the document transformations. It provides a number of search functions that allow administrators to find transformation problems for specific documents.

3. You can query the transformation history using the following parameters:

    * Date-time From and To
    * File name
    * Status
    * User name
    * Document type From and To

4. To investigate errors, set the **Outcome** field to **Error**. Hover over the warning sign to view an indication of the problem with the file.
