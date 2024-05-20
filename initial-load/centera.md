---
title: Alfresco Content Connector for EMC Centera
---

Use this information to install and configure the Alfresco Content Connector for EMC Centera. It also lists the prerequisites for setting up the EMC Centera environment on Windows and Linux platforms.

The Centera Connector module addresses the Centera store directly through its native API.

The module uses a series of properties to control the way that you access the store. A feature of this module allows you to set retention policies, such as, preventing content from being deleted for a period of time (for example, retaining invoices for seven years).

> **Note:** Alfresco Content Connector for EMC Centera 2.2 can be applied to Alfresco Content Services 6.0 - 6.2 only.
---
title: Configure Centera Connector
---
Use these instructions to configure your Alfresco Content Services environment for the Centera Connector.

You can configure the Centera Connector module to alter the behavior of the connection.

1. Open the `<classpathRoot>/alfresco-global.properties` file.

2. Add the `centera.url` property.

    For example:

    ```xml
    centera.url=168.159.214.24?c:/centera/c2armtesting.pea
    ```

    The `centera.url` property specifies the details of the Centera server. For example, in this case, it specifies the IP address `168.159.214.24`.

    The property also includes the location of the Centera `c2armtesting.pea` file. For example, `C:/centera/c2armtesting.pea` or `/usr/local/Centera_SDK/c2armtesting.pea`.

3. Set any additional properties to alter the way that the Centera Connector behaves.

    There are various additional properties that can be set to control the Centera Connector module. For example, the retention period for storing content is controlled using the `xam.archive.retentionPeriodDays=1` property.

    > **Note:** The sample `alfresco-global.properties` file supplied in the Alfresco EMC Centera Connector AMP provides example settings and values.

4. Save the `alfresco-global.properties` file.

5. Ensure that Java can find the Centera libraries.

    On Windows, set the `Path` environment variable.

    1. Open **Control Panel\All Control Panel Items\System**.

    2. Select **Advanced System Settings > Advanced > Environment Variables**.

    3. In the **System Variables** section, modify the existing `Path` environment variable by adding the path to the Centera libs.

    For example:

    ```bash
    Path=c:\centera\lib64
    ```

    On Linux, set the `PATH` and `LD_LIBRARY_PATH` environment variables.

    For example:

    ```bash
    export PATH=$PATH:/usr/local/Centera_SDK/lib/64
    export LD_LIBRARY_PATH=/usr/local/Centera_SDK/lib/64
    ```

## Centera Connector module properties

The following properties can be set for the Centera Connector module.

Set these properties in the `alfresco-global.properties` file.

| Property | Description |
| -------- | ----------- |
|centera.url | Specifies the full Centera connection string. For example, `centera.url=168.159.214.24?c:/centera/c2armtesting.pea`|
|xam.archive.storeName | Specifies the name of the XAM store that will be used by the `xam:archive` behavior. For example, `xam.archive.storeName=xamArchive`|
|xam.archive.retentionPeriodDays| Specifies the number of days to retain a XAM document. Use `0` to ignore; `>0` days to retain. Alfresco Content Services can be configured to allow deletes in conflict to the Centera enforce retention periods. A retention period is the time that a C-Clip and its underlying blobs must be stored on an EMC Centera before an application is allowed to delete them. According to configuration, `retentionPeriod` is set to 1 day. If you switch the server date to 1-2 days ahead on the Alfresco Content Services side, this will not result in the expiry of retention periods in the Centera cluster. For this reason, delete is not permitted. You should not change the date/time but wait until this period finished. Change the `xam.archive.retentionPeriodDays` to be not be greater then `system.content.orphanProtectDays`. This will prevent the cleaner from deleting non-expired Centera binary content. For example, `xam.archive.retentionPeriodDays=0`|
|xam.archive.addLock=true|Specifies whether to add the `cm:lockable` aspect automatically. Set to true to apply a lock when the aspect is added; set to false to not apply a lock|
|xam.archive.cronExpression| Specifies a cron expression for the XAM archive cleaner job. For example, `xam.archive.cronExpression=0 0 21 * * ?`|
|xam.archive.bindingPropertiesPattern| Specifies the pattern for all binding properties. Any property (full property name at time of writing) that does not match will be written as non-binding. For example, `vnd\\.com\\.alfresco\\..*` will match all properties prefixed with `vnd.com.alfresco`. Refer to [http://download.oracle.com/javase/tutorial/essential/regex/](http://download.oracle.com/javase/tutorial/essential/regex/), also [http://download.oracle.com/javase/6/docs/api/](http://download.oracle.com/javase/6/docs/api/).|
|xam.archive.app.db| The XAM well-known properties, which will be automatically populated. For example, `xam.archive.app.db=${db.url}`|
|xam.archive.globalPropertiesPrefix| The list of global properties to add to the XSet (comma-separated). For example, `${xam.archive.globalPropertiesPrefix}xam.archive.app.vendor`. This can be a list of any value that can be set in the alfresco-global.properties file but you should import any required properties using variable replacement to get consistent naming. For example, `xam.archive.globalPropertiesPrefix=vnd.com.alfresco. xam.archive.globalPropertiesToWrite=xam.archive.app.vendor, xam.archive.app.name, xam.archive.app.version, xam.archive.app.db`|
|xam.archive.contentFieldName| Specifies the name of the property against which to store content. For example, `xam.archive.contentFieldName=${xam.archive.globalPropertiesPrefix}content`|
|xam.archive.nodePropertiesPrefix| The list of node properties to add to the XSet (comma-separated, namespace-prefixes). For example, `${xam.archive.globalPropertiesPrefix}${xam.archive.nodePropertiesPrefix}cm:name`. Properties that are not present on the node are ignored. Implicit properties are generated and can be listed, for example, `sys:ref`, `sys:path`. For example, `xam.archive.nodePropertiesPrefix=xam.archive.node. xam.archive.nodePropertiesToWrite=sys:ref, sys:path, cm:name, cm:created, cm:creator, cm:owners`|
|xam.archive.forceBackgroundStoreMove| Specifies whether to move content to the XAM store immediately or as a background job. The aspect `xam.archivemodel:archivePending` is added to the document, pending the move to the XAM store. Set to false to move the content binaries to XAM as soon as the retention date is set. Set to true to move the content when the scheduled job runs. The default value for this property is false.|
|centera.fp.option.embedded.data| The maximum data size, in bytes, for data to be embedded in the CDF instead of being stored as separate blobs. The default value is 0 bytes, meaning data is never embedded in the CDF. The maximum value is 102400 bytes (100 KB). The value for the embedded data threshold can be set to less than or equal to 102400 bytes. For example, `centera.fp.option.embedded.data=102400`|
|centera.fp.option.maxconnections| The maximum number of sockets that the SDK will allocate for your application. Sockets are used to communicate with the Atmos CAS nodes managed in each pool object. The default value is 100. The maximum value is 999. For example, `centera.fp.option.maxconnections=100`|
|centera.fp.option.buffersize| The size of an internal C-Clip buffer in bytes. The default value is 16*1024. This value must be greater than 0. For example, `centera.fp.option.buffersize=153600`|
|centera.fp.option.prefetch.size| The size of the prefetch buffer. This buffer is used to assist in determining the size of the blob. The default size is 32 KB. The maximum size is 1 MB. For example, `centera.fp.option.prefetch.size=1048576`|

## Testing the EMC Centera connection

The JCASScript tool is provided with the EMC Centera® SDK and Community Tools.

> **Note:** From version 2.2 the Centera Connector only supports the EMC Centera proprietary API. The Alfresco XAM connector is no longer supported.

Use the JCASScript tool to connect to the Centera server using the `centera.url` property that you specified in the alfresco-global.properties file.

1. Start the JCASScript tool using the following command:

    ```bash
    java -jar JCASScript.jar
    ```

2. Enter the following command to connect to the Centera server:

    ```bash
    poolOpen 168.159.214.24?/usr/local/Centera_SDK/c2armtesting.pea
    ```

    An example of the output is as follows:

    ```bash
    CASScript>poolOpen 168.159.214.24?/usr/local/Centera_SDK/c2armtesting.pea

    Attempting to connect to: 168.159.214.24?/usr/local/Centera_SDK/c2armtesting.pea

    Connected to: 168.159.214.24?/usr/local/Centera_SDK/c2armtesting.pea

    CASPool Properties:
       Connection String:                 168.159.214.24?/usr/local/Centera_SDK/c2armtesting.pea
      Cluster Time:                      2014.01.10 06:25:31 GMT
      Buffer Size:                       16384
      Prefetch Buffer Size:              32768
      Connection Timeout:                120000
      Multi-Cluster Failover Enabled:    True
      Collision Avoidance Enabled:       False
    ```
---
title: Install Centera Connector
---
These steps describe how to install the Centera Connector module to an instance of Alfresco Content Services.

## Software prerequisites for the Centera Connector

To use the Centera Connector module, ensure that you have the prerequisite software installed on your machine.

Contact your EMC/Dell representative directly to access any downloads, for example:

* EMC Centera® SDK 3.3
* Server details and `.pea` files

## Setting up the Centera Connector environment

Create the environment for checking the EMC Centera connection.

{% capture windows %}

1. Download and install the Microsoft Visual C++ 2005 Service Pack 1 Redistributable Package.

2. Download and extract EMC Centera® SDK to a suitable directory, for example, `C:\centera`.

    * `Centera_SDK_Windows_2000-5.0-Win32Dev8.zip` for 32-bit systems
    * `Centera_SDK_Windows_2000-5.0-Win64Dev8.zip` for 64-bit systems
    On 32-bit systems, the subdirectory structure of the `C:\centera` directory includes the following directories:

    ```bash
    docs
    include
    lib
    lib32
    sdk_samples
    ```

    On 64-bit systems, the subdirectory structure of the `C:\centera` directory includes the following directories:

    ```bash
    docs
    include
    lib
    lib64
    sdk_samples
    ```

3. Download the Centera `.pea` file.

    For example, `c2armtesting.pea`.

4. Move the `c2armtesting.pea` file to the `C:\centera` directory.

5. Download and extract EMC Centera® SDK and Community Tools to any directory.

The structure of the `C:\centera` directory is similar to the following example (for 32-bit systems):

```bash
10.01.2014  17:55    <DIR>          .
10.01.2014  17:55    <DIR>          ..
11.12.2013  16:25             2 470 c2armtesting.pea
10.01.2014  17:41    <DIR>          docs
10.01.2014  17:41    <DIR>          include
10.01.2014  17:41    <DIR>          lib
10.01.2014  17:41    <DIR>          lib32
10.01.2014  17:41    <DIR>          sdk_samples
               1 File(s)          2 470 bytes
               7 Dir(s)  49 088 593 920 bytes free
```

The structure of the `C:\centera` directory is similar to the following example (for 64-bit systems):

```bash
10.01.2014  17:55    <DIR>          .
10.01.2014  17:55    <DIR>          ..
11.12.2013  16:25             2 470 c2armtesting.pea
10.01.2014  17:37    <DIR>          docs
10.01.2014  17:37    <DIR>          include
10.01.2014  17:37    <DIR>          lib
10.01.2014  17:37    <DIR>          lib64
10.01.2014  17:37    <DIR>          sdk_samples
               1 File(s)          2 470 bytes
               7 Dir(s)  49 088 593 920 bytes free
```

The structure of the `C:\centera\lib32` directory is similar to the following example:

```bash
10.01.2014  17:41    <DIR>          .
10.01.2014  17:41    <DIR>          ..
29.08.2012  17:33           774 144 FPCore.dll
29.08.2012  17:33           610 304 FPLibrary.dll
29.08.2012  17:33           610 948 FPLibrary.lib
29.08.2012  17:33           323 584 fpos32.dll
29.08.2012  17:33         2 011 136 fpparser.dll
29.08.2012  17:33           184 320 FPStreams.dll
29.08.2012  17:33           438 272 FPUtils.dll
29.08.2012  17:33           184 320 FPXML.dll
10.01.2014  17:41    <DIR>          lib
29.08.2012  17:33           262 144 pai_module.dll
               9 File(s)      5 399 172 bytes
               3 Dir(s)  49 088 593 920 bytes free
```

The structure of the `C:\centera\lib64` directory is similar to the following example:

```bash
10.01.2014  17:37    <DIR>          .
10.01.2014  17:37    <DIR>          ..
29.08.2012  17:34           983 552 FPCore.dll
29.08.2012  17:34           690 688 FPLibrary.dll
29.08.2012  17:34           616 178 FPLibrary.lib
29.08.2012  17:34           412 160 fpos64.dll
29.08.2012  17:34         2 919 424 fpparser.dll
29.08.2012  17:34           165 888 FPStreams.dll
29.08.2012  17:34           483 840 FPUtils.dll
29.08.2012  17:34           168 960 FPXML.dll
10.01.2014  17:37    <DIR>          lib
29.08.2012  17:34            63 488 pai_module.dll
               9 File(s)      6 504 178 bytes
               3 Dir(s)  49 088 593 920 bytes free
```

{% endcapture %}

{% capture linux %}

1. Download and extract EMC Centera® SDK (`Centera_SDK_Linux-gcc3.3.tgz`), for example, to `/opt`.

    A subdirectory structure of the `/opt/Centera_SDK` directory includes the following directories:

    ```bash
    total 20
    drwxr-xr-x.  4 root root 4096 Jan 10 21:32 docs
    drwxr-xr-x.  2 root root 4096 Jan 10 21:32 include
    drwxr-xr-x.  2 root root 4096 Aug 30  2012 install
    drwxr-xr-x.  2 root root 4096 Jan 10 21:32 lib
    drwxr-xr-x. 13 root root 4096 Sep 14  2006 sdk_samples
    ```

2. Install the EMC Centera® SDK using the following commands:

    ```bash
    cd /opt/Centera_SDK/install
    ./install
    ```

    The default installation directory is `/usr/local/Centera_SDK`.

3. Download the Centera `.pea` file.

    For example, `c2armtesting.pea`.

4. Move the `c2armtesting.pea` file to the Centera `/usr/local/Centera_SDK` directory.

5. Download and extract EMC Centera® SDK and Community Tools to any directory.

The structure of the `/usr/local/Centera_SDK` directory is similar to the following example:

```bash
total 12
-rw-r--r--. 1 root root 2470 Dec 11 16:25 c2armtesting.pea
drwxr-xr-x. 2 root root 4096 Dec 19 22:51 include
drwxr-xr-x. 4 root root 4096 Dec 19 22:51 lib
```

The structure of the `/usr/local/Centera_SDK/lib/32` directory is similar to the following example:

```bash
total 6316
lrwxrwxrwx. 1 root root      52 Dec 19 22:51 libFPCore32.so -> /usr/local/Centera_SDK/lib/32/libFPCore32.so.3.3.719
-rwxr-xr-x. 1 root root 1063484 Dec 19 22:51 libFPCore32.so.3.3.719
lrwxrwxrwx. 1 root root      44 Dec 19 22:51 libFPCore.so -> /usr/local/Centera_SDK/lib/32/libFPCore32.so
lrwxrwxrwx. 1 root root      55 Dec 19 22:51 libFPLibrary32.so -> /usr/local/Centera_SDK/lib/32/libFPLibrary32.so.3.3.719
-rwxr-xr-x. 1 root root  643603 Dec 19 22:51 libFPLibrary32.so.3.3.719
lrwxrwxrwx. 1 root root      47 Dec 19 22:51 libFPLibrary.so -> /usr/local/Centera_SDK/lib/32/libFPLibrary32.so
lrwxrwxrwx. 1 root root      53 Dec 19 22:51 libFPParser32.so -> /usr/local/Centera_SDK/lib/32/libFPParser32.so.3.3.50
-rwxr-xr-x. 1 root root 3800245 Dec 19 22:51 libFPParser32.so.3.3.50
lrwxrwxrwx. 1 root root      46 Dec 19 22:51 libFPParser.so -> /usr/local/Centera_SDK/lib/32/libFPParser32.so
lrwxrwxrwx. 1 root root      55 Dec 19 22:51 libFPStreams32.so -> /usr/local/Centera_SDK/lib/32/libFPStreams32.so.3.3.719
-rwxr-xr-x. 1 root root  121784 Dec 19 22:51 libFPStreams32.so.3.3.719
lrwxrwxrwx. 1 root root      47 Dec 19 22:51 libFPStreams.so -> /usr/local/Centera_SDK/lib/32/libFPStreams32.so
lrwxrwxrwx. 1 root root      53 Dec 19 22:51 libFPUtils32.so -> /usr/local/Centera_SDK/lib/32/libFPUtils32.so.3.3.719
-rwxr-xr-x. 1 root root  648376 Dec 19 22:51 libFPUtils32.so.3.3.719
lrwxrwxrwx. 1 root root      45 Dec 19 22:51 libFPUtils.so -> /usr/local/Centera_SDK/lib/32/libFPUtils32.so
lrwxrwxrwx. 1 root root      51 Dec 19 22:51 libFPXML32.so -> /usr/local/Centera_SDK/lib/32/libFPXML32.so.3.3.719
-rwxr-xr-x. 1 root root  129647 Dec 19 22:51 libFPXML32.so.3.3.719
lrwxrwxrwx. 1 root root      43 Dec 19 22:51 libFPXML.so -> /usr/local/Centera_SDK/lib/32/libFPXML32.so
lrwxrwxrwx. 1 root root      56 Dec 19 22:51 libPAI_module32.so -> /usr/local/Centera_SDK/lib/32/libPAI_module32.so.3.3.100
-rwxr-xr-x. 1 root root   49036 Dec 19 22:51 libPAI_module32.so.3.3.100
lrwxrwxrwx. 1 root root      48 Dec 19 22:51 libPAI_module.so -> /usr/local/Centera_SDK/lib/32/libPAI_module32.so
```

The structure of the `/usr/local/Centera_SDK/lib/64` directory is similar to the following example:

```bash
total 6736
lrwxrwxrwx. 1 root root      52 Dec 19 22:51 libFPCore64.so -> /usr/local/Centera_SDK/lib/64/libFPCore64.so.3.3.719
-rwxr-xr-x. 1 root root 1098829 Dec 19 22:51 libFPCore64.so.3.3.719
lrwxrwxrwx. 1 root root      44 Dec 19 22:51 libFPCore.so -> /usr/local/Centera_SDK/lib/64/libFPCore64.so
lrwxrwxrwx. 1 root root      55 Dec 19 22:51 libFPLibrary64.so -> /usr/local/Centera_SDK/lib/64/libFPLibrary64.so.3.3.719
-rwxr-xr-x. 1 root root  671881 Dec 19 22:51 libFPLibrary64.so.3.3.719
lrwxrwxrwx. 1 root root      47 Dec 19 22:51 libFPLibrary.so -> /usr/local/Centera_SDK/lib/64/libFPLibrary64.so
lrwxrwxrwx. 1 root root      53 Dec 19 22:51 libFPParser64.so -> /usr/local/Centera_SDK/lib/64/libFPParser64.so.3.3.50
-rwxr-xr-x. 1 root root 4061679 Dec 19 22:51 libFPParser64.so.3.3.50
lrwxrwxrwx. 1 root root      46 Dec 19 22:51 libFPParser.so -> /usr/local/Centera_SDK/lib/64/libFPParser64.so
lrwxrwxrwx. 1 root root      55 Dec 19 22:51 libFPStreams64.so -> /usr/local/Centera_SDK/lib/64/libFPStreams64.so.3.3.719
-rwxr-xr-x. 1 root root  134962 Dec 19 22:51 libFPStreams64.so.3.3.719
lrwxrwxrwx. 1 root root      47 Dec 19 22:51 libFPStreams.so -> /usr/local/Centera_SDK/lib/64/libFPStreams64.so
lrwxrwxrwx. 1 root root      53 Dec 19 22:51 libFPUtils64.so -> /usr/local/Centera_SDK/lib/64/libFPUtils64.so.3.3.719
-rwxr-xr-x. 1 root root  713762 Dec 19 22:51 libFPUtils64.so.3.3.719
lrwxrwxrwx. 1 root root      45 Dec 19 22:51 libFPUtils.so -> /usr/local/Centera_SDK/lib/64/libFPUtils64.so
lrwxrwxrwx. 1 root root      51 Dec 19 22:51 libFPXML64.so -> /usr/local/Centera_SDK/lib/64/libFPXML64.so.3.3.719
-rwxr-xr-x. 1 root root  151395 Dec 19 22:51 libFPXML64.so.3.3.719
lrwxrwxrwx. 1 root root      43 Dec 19 22:51 libFPXML.so -> /usr/local/Centera_SDK/lib/64/libFPXML64.so
lrwxrwxrwx. 1 root root      56 Dec 19 22:51 libPAI_module64.so -> /usr/local/Centera_SDK/lib/64/libPAI_module64.so.3.3.100
-rwxr-xr-x. 1 root root   52961 Dec 19 22:51 libPAI_module64.so.3.3.100
lrwxrwxrwx. 1 root root      48 Dec 19 22:51 libPAI_module.so -> /usr/local/Centera_SDK/lib/64/libPAI_module64.so
```

{% endcapture %}

{% include tabs.html tableid="centera" opt1="Windows" content1=windows opt2="Linux" content2=linux %}

## Install the Centera Connector AMP

The Centera Connector is packaged as an Alfresco Module Package (AMP) file.

1. Browse to [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2. Download the `alfresco-centera-connector-2.2.x.amp` file.

3. Use the Module Management Tool (MMT) to install the AMP.

    `java -jar <installLocation>\bin\alfresco-mmt.jar install <installLocation>\amps\alfresco-centera-connector-2.2.x.amp <installLocation>\tomcat\webapps\alfresco.war`

    If your Alfresco Content Services installation is running within the Tomcat application server, you can use the `<installLocation>\bin\apply_amps` command to apply all AMP files that are located in the `<installLocation>\amps` directory.

4. Restart the Alfresco Content Services server.

## Test the Centera Connector

Test that the Centera Connector module is working correctly with Alfresco Content Services.

1. Enable `DEBUG` logging for the Centera Connector components.

    For example:

    ``` xml
    log4j.logger.org.alfresco.enterprise.repo.content.centera=DEBUG
    log4j.logger.org.alfresco.enterprise.repo.centera=DEBUG
    ```

2. Add the `xam:archived` aspect to the share-config-custom.xml file.

    For example:

    ```xml
    <alfresco-config>

       <config evaluator="node-type" condition="cm:content">

          <forms>
             <form>
                <!-- 2 column template -->

                <edit-form />

                <field-visibility>

                <!-- aspect: cm:storeSelector -->

                <show id="cm:storeName" />

                <!-- aspect: xam:archive -->
                <show id="xam:dateArchived" for-mode="view" />
                <show id="xam:retainUntil" for-mode="view" />
                <show id="cm:content" for-mode="view" />
                </field-visibility>

                <appearance>
                   <!-- Store Selector -->
                   <field id="cm:storeName" label="Store Name" description="Content Store Name" />
                   <set id="xam-archive" appearance="bordered-panel" label="XAM Archived" />
                   <field id="xam:dateArchived" label="XAM Date Archived" set="xam-archive" />
                   <field id="xam:retainUntil" label="XAM Retain Until Date" set="xam-archive" />
                </appearance>
             </form>
          </forms>
       </config>

    <config evaluator="string-compare" condition="DocumentLibrary">
       <aspects>
             <visible>
                <aspect name="xam:archive" label="XAM Archive" />
             </visible>
       </aspects>
    </config>
    </alfresco-config>
    ```

3. View the metadata for the document.

    The new store is shown as **xamArchive** and the **retainedUntil** date is set.

4. Copy the ClipID, and then open the C-Clip using the JCASScript tool.

    For example:

    ```bash
    CASScript>clipopen EQM2GC012MC77e72B24N2MMFU59G418ACSAIE70BAS340TN3E1JJL

    Clip Properties:

      Name:                untitled
      Creation Date:       2013.11.27 01:35:09 GMT
      Size:                13474
      Number of Tags:      1
      Number of Blobs:     1
      Retention Class:
      Retention Seconds:   86396
      Modified:            False
      EBR Enabled :        False
      Retention Hold:      False
    ```

    1. Check that the retention period was set.

        ```bash
        CASScript>clipattribs

        Number of attributes:  17

        Name:   creation.poolid        Value:   861673fa-1dd2-11b2-b535-b66ede9133c1-7
        Name:   retention.period       Value:   86396
        Name:   sdk.version            Value:   3.3.718
        Name:   modification.poolid    Value:   861673fa-1dd2-11b2-b535-b66ede9133c1-7
        Name:   type                   Value:   Standard
        Name:   name                   Value:   untitled
        Name:   creation.date          Value:   2013.11.27 13:35:09 GMT
        Name:   modification.date      Value:   2013.11.27 13:35:12 GMT
        Name:   creation.profile       Value:   armtesting
        Name:   modification.profile   Value:   armtesting
        Name:   numfiles               Value:   1
        Name:   totalsize              Value:   13474
        Name:   refid                  Value:   E5S2HABU8PRRBAS340TN3E1JJL
        Name:   clusterid              Value:   25c57a54-1dd2-11b2-b87c-ce625a7031f2
        Name:   prev.clip              Value:  
        Name:   clip.naming.scheme     Value:   MD5
        Name:   numtags                Value:   1
        ```

    2. Check that the node and application properties have been copied over.

        Select the first tag of the opened C-Clip. For example:

        ```bash
        CASScript>tagfirst

        CASTag Properties:

         Name:                com.alfresco.content
         Has Blob:            True
         Blob Size:           13474
         Number of Attributes:10
         Has Parent:          False
         Has Next Sibling:    False
         Has Child:           False
        ```

        Display all the attributes. For example:

        ```bash
        CASScript>tagattribs

        Number of attributes: 10

         Name: modified-date   Value: 1385553402696
         Name: com.alfresco.xam.archive.node.sys:ref        Value: workspace://SpacesStore/51bba786-184b-4d7b-8b2a-da90875e5b16
         Name: com.alfresco.xam.archive.app.name            Value: Main Repository
         Name: com.alfresco.xam.archive.node.cm:created     Value: 2013-11-27T15:56:27.011+04:00
         Name: com.alfresco.xam.archive.app.version         Value: 4.2.0 (28)
         Name: com.alfresco.xam.archive.app.db              Value: jdbc:mysql://localhost:3306/alfresco?useUnicode=yes&characterEncoding=UTF-8
         Name: com.alfresco.xam.archive.node.sys:path       Value: /app:company_home/st:sites/cm:test/cm:documentLibrary/cm: abc.txt
         Name: com.alfresco.xam.archive.node.cm:creator     Value: admin
         Name: com.alfresco.xam.archive.node.cm:name        Value: abc.txt
         Name: com.alfresco.xam.archive.app.vendor          Value: Alfresco Software
        ```

    3. Type `tagClose` to close the current tag.

    4. Type `clipClose` to close the current C-Clip.

    5. Type `poolClose` to close the current connection to EMC Centera pool.

5. Test the folder hierarchy.

    1. Create a folder containing several files and folders,

    2. Apply the `xam:archived` aspect to the top-level folder.

    3. Check that the aspect has been applied to the entire hierarchy.

    4. Choose one of the files in the hierarchy and check through for a single file from step 1.

## Setting up the CenteraContentStore as the main store

To set up the CenteraContentStore to be the main store, it is recommended that you also configure the primary store as a CachingContentStore.

See [Configuring CachingContentStore]({% link content-services/latest/admin/content-stores.md %}#caching-content-store-ccs) for more information.

This setup relates to new content and cannot be applied retrospectively, unless all content is moved from the file system to Centera.

1. Create `xam-custom-context.xml` file in the `<extension>` directory.

    For example, `<installLocation>/tomcat/shared/classes/alfresco/extension`.

2. Copy the `org_alfresco_module_centera_centeraContentStore` bean from `<installLocation>/tomcat/webapps/alfresco/WEB-INF/classes/alfresco/module/org_alfresco_module_xamconnector/module-context.xml` file.

    For example:

    ```xml
    <?xml version='1.0' encoding='UTF-8'?>

    <!DOCTYPE beans PUBLIC '-//SPRING//DTD BEAN//EN' 'http://www.springframework.org/dtd/spring-beans.dtd'>

    <beans>

        <bean id="org_alfresco_module_centera_centeraContentStore" class="org.alfresco.enterprise.repo.content.centera.CenteraContentStore" init-method="init">

            <property name="readOnly" value="false" />
            <property name="centeraConnection" ref="org_alfresco_module_centera_centeraConnection"/>
            <property name="contentFieldName" value="${xam.archive.contentFieldName}"/>

        </bean>

    </beans>
    ```

3. Paste the bean in to the newly created `xam-custom-context.xml` file.

4. Change the bean id to `fileContentStore`.

    For example:

    ```xml
    <?xml version='1.0' encoding='UTF-8'?>

    <!DOCTYPE beans PUBLIC '-//SPRING//DTD BEAN//EN' 'http://www.springframework.org/dtd/spring-beans.dtd'>

    <beans>

        <bean id="fileContentStore" class="org.alfresco.enterprise.repo.content.centera.CenteraContentStore" init-method="init">

            <property name="readOnly" value="false" />
            <property name="centeraConnection" ref="org_alfresco_module_centera_centeraConnection"/>
            <property name="contentFieldName" value="${xam.archive.contentFieldName}"/>

        </bean>

    </beans>
    ```

5. Add the following property to `alfresco-global.properties` file.

    ```bash
    xam.archive.contentFieldName=com.alfresco.content
    ```

6. Disable the `contentstore.deleted` store by emptying the list of listeners in the `content-services-context.xml` file.

    For example:

    ```xml
    <bean id="deletedContentBackupListeners" class="java.util.ArrayList">
          <constructor-arg>
             <list>
                <!--
                <ref bean="deletedContentBackupListener" />
                -->
             </list>
          </constructor-arg>
       </bean>
    ```

7. Start Alfresco Content Services server.
---
title: Supported platforms
---

The following are the supported platforms for Alfresco Content Connector for EMC Centera 2.2:

| Version | Supported |
| ------- | --------- |
| Alfresco Content Services 6.2.x | |
| Alfresco Content Services 6.1.x | |
| Alfresco Content Services 6.0.x | |
