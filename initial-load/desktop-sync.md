---
title: Alfresco Desktop Sync
---

With Desktop Sync, desktop users can securely and automatically sync content between their desktop and Alfresco Content Services.

This release of Desktop Sync is a compatibility release to support Alfresco Sync Service 4.0, and includes minor UI changes.

You can easily connect to Alfresco Content Services and select folders and sites to view and work with on the desktop, even when working offline.

Once the folders and sites are selected, they are automatically downloaded and visible using Microsoft File Explorer (for Windows) or Finder (for Mac).

Changes are automatically synced from Alfresco Content Services to the desktop, so the latest content is always available. This allows you to work in places where you don't have internet access, secure in the knowledge that your changes will show up in Alfresco Content Services once you're back online.

> **Note:** Desktop Sync replicates content on local desktops for users with the appropriate access. If replication outside the repository isn't allowed by your content policy, you shouldn't deploy Desktop Sync. This version of Desktop Sync doesn't support Smart Folders.

For information about installing and configuring the Desktop Sync service server-side AMP, see [Installing Sync Service]({% link sync-service/latest/install/index.md %}).
---
title: Administer Desktop Sync
---

If you’re an IT administrator, you can configure a number of features to centrally manage your Desktop Sync clients.

## Manage automatic configuration updates

If you're an IT administrator, you can upload a new configuration file to the repository so that it's automatically 
provided to all Desktop Sync clients.

This allows you to update the configuration file for all your Desktop Sync users without any manual intervention.

1. Create a **Desktop Sync** folder in the Alfresco Content Services repository path: `/Data Dictionary/`

2. Browse to [Hyland Community](https://community.hyland.com/){:target="_blank"} and download the configuration file: `AlfrescoSync.conf`.

3. Save the file in the new **Desktop Sync** folder.

    >**Note:** Don't rename the file, otherwise the configuration update won't work.

    Once the configuration file is uploaded, users receive a notification telling them that the new configuration 
    file has been downloaded.

    When the Desktop Sync client connects to the repository for file updates, it checks for new versions of the configuration. 
    The client periodically checks for new configuration files - no more than once per 24 hour period. 
    When a new configuration file is found, it's downloaded and retained in the appropriate folder. For example:

    * Windows: `<userHome>\AppData\Local\Alfresco`
    * Mac: `~/Library/Application Support/Alfresco`

    The existing configuration file is kept as a backup (i.e. `AlfrescoSync-backup.conf`).

    Users will have to restart Desktop Sync to apply the changes.

    >**Note:** If you're a Windows user, you'll see a message stating:
    >
    >```text
    >C:\Users\Program Files\AppData\Local\Alfresco\AlfrescoSync.conf
    >This file has been modified by another program. Do you want to reload it?
    >```

4. Select **OK** to apply the changes to your configuration.

## Manage automatic installation updates

If you're an IT administrator, you can upload new installation files into the repository to automatically update 
all users with Desktop Sync clients.

This ensures users with Desktop Sync clients are always up to date with minimal manual intervention.

1. Create a **Desktop Sync** folder in the Alfresco Content Services repository path: `/Data Dictionary/`
2. Upload the latest installer files for Windows and Mac clients to this location.

    >**Note:** Don't rename the files, otherwise the client upgrade won't work.

    Once the installer files are uploaded, users receive a notification telling them that an update is available and a 
    new installation file has been downloaded.

    Users will have to restart Desktop Sync to apply the new installation file.

    See [Updating Desktop Sync]({% link desktop-sync/latest/upgrade/index.md %}) for more information about how an update is applied.

## SAML authentication

Starting from version 1.4, Alfresco Desktop Sync users can authenticate through a SAML identity provider.

The following prerequisites are required - see the [Supported platforms]({% link sync-service/latest/support/index.md %}) page for specific versions:

* Alfresco Content Services
* Alfresco Sync Service
* Identity Service

SAML authentication in Desktop Sync clients (Windows and Mac) is automatically enabled if the 
Alfresco Content Services repository is configured to use the Identity Service.

See the Alfresco Sync Service documentation for [SAML configuration]({% link sync-service/latest/config/index.md %}#saml-configuration) details.

Once users have entered the repository URL (shown in step 2 of [Setting up Desktop Sync]({% link desktop-sync/latest/install/index.md %}#setting-up-desktop-sync-on-windows) for Windows and [Setting up Desktop Sync]({% link desktop-sync/latest/install/index.md %}#faq/mac) for Mac), they will be asked to enter their username and password into the SAML provider login page via their default browser.

> **Note:** In earlier versions of Desktop Sync, the user was logged out every 30 minutes and needed to enter their credentials again to re-authenticate. Starting from Desktop Sync 1.17, the logged in session will not terminate unless the system has unforeseen issues.

## Manage sync configuration

As an IT administrator, you can manage the configuration of your Desktop Sync client apps via the Desktop Sync UI and a configuration file. You can choose to enable or disable the content selection dialog from the UI for all your Desktop Sync clients, while setting enforced paths to sync from the configuration file.

The content selection dialog is displayed by default. The property that controls if this dialog appears is `syncui.enableManageContent` which is `true` by default. If you want to hide the whole dialog, change the value of the property to `false`, so that the user is only prompted to set the sync target location. Next, define enforced sync paths as described in [Manage enforced sync](#manage-enforced-sync).

The property to *enable/disable the content selection dialog* is specified as:

```text
syncui.enableManageContent = <true/false>
```

* The property defaults to `true`, even if it's not specified.

* If there are enforced sync paths in the configuration file and the content selection dialog is enabled, those path are always marked as checked/unchecked in the UI as specified in the configuration file.

* If there are no valid enforced sync paths from the configuration file (i.e. paths that exist and that the user can access), the value for this property is automatically set to `true`. So the value from the configuration file isn't taken into account, and the content selection dialog is enabled.

> **Note:** A special case that's worth highlighting from the last comment is where you can't add a folder as a constraint that's already covered by an enforced sync path. For example, setting the following values results in the content selection dialog being displayed, even though the `syncui.enableManageContent` property is set to `false`, since it would result in there being no valid paths to sync:
>
> ```text
> syncui.enableManageContent = false
>
> # Enforced sync path
> test.path.1 = /User Homes/username/folder1
>
> # Incorrect sync path to exclude - results in no valid paths to sync
> test.excludePath.1 = /User Homes/username
> ```

## Manage enforced sync

If you're an IT administrator, you can configure Desktop Sync client apps to enforce the sync of specific paths or Sites, and optionally enforce the exclusion of sub-folders for those paths or Sites. This allows you to restrict what your Desktop Sync clients sync by pre-selecting the sync folders.

When you add this configuration, users can't select anything to sync as the Desktop Sync client hides the content selection dialog.

The properties to *enforce sync* are specified as:

```text
test.path.<n> = <enforced-sync-path>
test.siteName.<n> = <enforced-sync-siteId>
```

where `<n>` is an ascending index number starting at `1`. These must be consecutive otherwise, if a number is skipped, all paths that follow are ignored.

The properties to *enforce exclusion* are specified as:

```text
test.subfolderFilter.<enforced-sync-path> = <relative path to folder to be excluded>
test.subfolderFilter.<enforced-sync-siteId> = <relative path to folder to be excluded>
```

Here's an example of how these properties are configured:

```bash
test.path.1 = /Shared
test.path.2 = /Sites/siteId/documentLibrary/folder3
test.path.3 = /User Homes/username
test.subFolderFilter./Shared=folder8,folder9
test.subFolderFilter./User Homes/username=folder7
```

> **Note:**
>
> * The exclusion property `test.subfolderFilter` can't be used on its own - it needs to be applied to one of the paths specified by `test.path.<n>`.
> * If all enforced sync paths are specified incorrectly, then the content selection dialog is enabled.
> * If, for example, one of two paths is invalid and one is valid, the content selection dialog is disabled and only the valid path is synced.
> * If an excluded folder is renamed, then that folder will be synced after a restart.

## Manage hidden sync

If you're an IT administrator, you can configure Desktop Sync client apps to hide specific paths or Sites. This allows you to restrict what your Desktop Sync clients can sync by hiding those locations from view in the content selection dialog.

The properties to *hide content from sync* are specified as:

```bash
test.excludePath.<n>=<full-path-to-folder-or-site>
test.excludeSite.<n>=<siteId>
```

where `<n>` is an ascending index number starting at `1`.

Adding this configuration ensures that users aren't able to sync the defined content. In addition:

* The folder/site will not be shown in the content selection dialog.
* If the excluded folder is inside a synced path, the excluded folder will be skipped when syncing.
* The sync folder selection is checked every time the Desktop Sync client restarts. If a sync location is hidden by the administrator, then that content is removed from the client.
---
title: Configure Desktop Sync
---

If you're an IT administrator, you can configure Desktop Sync for central installation purposes using the `AlfrescoSync.conf` file located at:

* (Windows): `<userHome>\AppData\Local\Alfresco`
* (For Mac): `~/Library/Application Support/Alfresco`

Using the configuration file, you can update:

* timer values, such as polling and retry intervals
* sync constraint patterns for files/folders to be ignored by Desktop Sync
* disk space limits
* custom content type mappings for particular file extensions
* user interface defaults and customization (including localization)
* network access configuration
* debug logging
* [timezone](#change-timezone) used in `AlfrescoDesktopSync.log` file

The configuration properties values are case sensitive and use the format `name.subname=value`, 
for example, `syncmanager.deferFileSyncTimer=15`.

## Sharing files

You can configure a file sharing URL, (defined by `syncmanager.quickShareURL`), so that when you share a link to a file, 
a correctly formatted URL is provided. This link should either access Alfresco Digital Workspace or Alfresco Share.

The format for this property is: `<protocol>://<yourserveraddress>/<path>/`, where:

* `<protocol>` is set to either `http` or `https`
* `<yourserveraddress>` is the address of the server
* `<path>` is the path to access a link in either Alfresco Digital Workspace or Alfresco Share

Here are examples of how you can set the URL to access a file:

* For Digital Workspace: `syncmanager.quickShareURL=https://workspace.mycompany.com/#/preview/s/`
* For Share: `syncmanager.quickShareURL=https://alfresco.mycompany.com/share/s/`

>**Note:** You must choose to share links either in Alfresco Digital Workspace or Alfresco Share but not both. 
>The URL must also use an `http` or `https` protocol. If the property is left blank or not set correctly, 
>the file sharing feature won't be available in Desktop Sync.

For more information, see [Sharing files]({% link desktop-sync/latest/using/sharing.md %}).

## User interface

Use the user interface properties to configure the Desktop Sync UI.

|Property|Default value|Description|
|--------|-------------|-----------|
|syncui.defaultServer| |Specifies a default server URL to be entered in the login screen when Desktop Sync is run for the first time (usually at the end of the installation process).The user can change the URL on the login screen, if required.|
|syncui.enableAnalytics|true|Controls whether Alfresco Content Services collects anonymized data. Applies to Mac only.|
|syncui.language| |Add this property to specify the language for the Desktop Sync UI (requires app restart). See [Localization](#localization) for supported values.|
|syncui.showConsistencyCheck|true|Specifies whether the **Consistency Check** option is available in Desktop Sync.As an Administrator, you can disable this option as consistency check scans all the folders that are synced to Desktop Sync, and this may effect your server's performance. Applies to Windows only.|
|syncui.showMyFilesTab|true|Controls whether My Files is shown in the content selection dialog.|
|syncui.showSharedFilesTab|true|Controls whether Shared Files is shown in the content selection dialog.|
|syncui.showSitesTab|true|Controls whether Sites is shown in the content selection dialog.|
|syncui.showRepositoryTab|true|Controls whether Company Home is shown in the content selection dialog.|
|syncmanager.userMemberSitesMaxItems|250|Add this property to change the number of sites shown in the content selection dialog.|
|syncui.enableAspects| |Controls which aspects are shown in the **Property** dialog.Format: `syncui.enableAspects=<aspect1>,<aspect2>, ...`|
|syncui.disableProperties| |Controls which properties are hidden for a given aspect.Format: `syncui.disableProperties.<index>=<aspect>|<property1>,<property2>, ...`|
|syncui.fileCustomTypes| |Controls the file custom types that are visible in the **Property** dialog. Format: `syncui.fileCustomTypes=display_name (type_id),...`. Note that the display name is optional.|
|syncui.folderCustomTypes| |Controls the file custom types that are visible in the **Property** dialog. Format: `syncui.fileCustomTypes=display_name (type_id),...`. Note that the display name is optional.|

## Enable analytics (Mac only)

Alfresco Content Services collects some anonymized information about fatal errors and basic usage which are used to 
help us improve the product in the future. There's no data that could identify a customer, user, or machine. 
If you wish to prevent this anonymized data from being sent, change the value of the `syncui.enableAnalytics` property to `false` 
to turn it off.

Here are some examples of the information that's collected:

* Application crash logs
* Event metrics for specific features:
    * Conflict detected
    * Conflict resolved: Keep my changes, Discard my changes, error
    * Check out: success / error
    * Cancel check out: success / error
    * Check in: success / error, Has comment: yes / no, Major version: yes / no
    * Remove Account: Initial sync finished: yes / no, Has conflict: yes / no
    * Initial sync started

## Desktop Sync UI

As an IT administrator, you can control the parts of the Desktop Sync UI that users can access, 
so that they can't sync content from specific areas in Alfresco Content Services. 

By default, the content selection dialog (see [selecting content to sync]({% link desktop-sync/latest/using/select-to-sync.md %})) 
displays **My Files**, **Shared Files**, **Sites**, and **Company Home**. 
If you want to hide any of these areas, change the value of the relevant `syncui.show*` property to `false`.

## View and edit properties

As an IT administrator, you can control which aspects and properties that your end users can view and edit from their desktops. 
By default, users can view and edit general properties for files or folders, such as the Title, Name, Description, and Author 
(if they have the correct permissions).

You can extend this functionality to allow users to view and edit additional properties. Add the `syncui.enableAspects` and 
(optional) `syncui.disableProperties` settings to your central configuration file.

>**Note:** We recommend adding `syncui.disableProperties` so that your end users aren't overwhelmed by properties they don't need to see, 
> such as system properties or potentially sensitive values.
>
>Here are a few examples:
>
>```bash
>syncui.enableAspects=cm:titled,exif:exif,dp:restrictable
>syncui.disableProperties.1=cm:titled|cm:title
>syncui.disableProperties.2=exif:exif|exif:exposureTime,exif:orientation,exif:flash
>```

As an IT administrator, you can also control the list of available custom types for files and folders that your end users 
can apply to their content from their desktops. If either `syncui.fileCustomTypes` or `syncui.folderCustomTypes` are missing 
from the configuration file, the custom types are fetched from the repository. 
Otherwise, the custom type field is populated with the values read from the configuration file.

In the **Property** dialog > **General properties** tab, there's a drop-down menu with the custom types that can be 
applied to a file or folder. This menu lists only custom types created using the Content Model Manager API.

Example:

```bash
syncui.fileCustomTypes=My custom type (model-1:custom_type_name)
```

>**Note:**
>
>* If a custom type is applied to the file/folder from the **Properties** dialog, all data entered that was not saved will be discarded. We suggest you save your changes first before applying a custom type.
>* If the file or folder already has a custom type applied, then the custom type drop-down will contain only sub-types of that custom type. You can't change between unrelated custom types, as the Content Model Manager API doesn't allow it.

## Sync manager timers

|Property|Default value|Description|
|--------|-------------|-----------|
|alfrescosync.initialPollInterval|15 seconds|Sets the number of seconds before the first server polling after application startup:{::nomarkdown}<ul><li>Minimum value: 0 seconds</li><li>Maximum allowed value: 18000 seconds (5 hours)</li></ul>{:/}|
|alfrescosync.pollingInterval|300 seconds|Sets the number of seconds between polling of the sync server for server-side file change events. This does not affect the processing of desktop file change events; they are always processed immediately:{::nomarkdown}<ul><li>Minimum value: 10 seconds</li><li>Maximum allowed value: 18000 seconds (5 hours)</li></ul>{:/}|
|syncmanager.deferFileSyncTimer|15 seconds|Sets the number of seconds between retries of a deferred update for a file, such as when an application still has the file open:{::nomarkdown}<ul><li>Minimum value: 10 seconds</li><li>Maximum allowed value: 60 seconds</li></ul>{:/}|
|syncmanager.deferDelayRetryTimer|3600 seconds|Sets the number of seconds to retry syncing a deferred update for a file. If you wish to override the default setting, add this property in the configuration file:{::nomarkdown}<ul><li>Minimum value: 10 seconds</li><li>Maximum allowed value: 36000 seconds (10 hours)</li></ul>{:/}|
|syncmanager.deferOnlineCheckTimer|60 seconds|Sets the number of seconds between retries when a server connection is offline. This may be due to server being down, no network connection, or no route to the server:{::nomarkdown}<ul><li>Minimum value: 15 seconds</li><li>Maximum allowed value: 600 seconds</li></ul>{:/}|
|syncmanager.consistencyCheckRetryInterval|120 seconds|Sets the number of seconds between consistency check retry attempts. A consistency check may be aborted when too many file system changes are received during the consistency check scan:{::nomarkdown}<ul><li>Minimum value: 30 seconds</li><li>Maximum allowed value: 3600 seconds</li></ul>{:/}|
|syncmanager.freeSpaceCheckTimer|120 seconds|Sets the number of seconds between free space checks when syncing has been paused due to the local free disk space threshold being reached:{::nomarkdown}<ul><li>Minimum value: 15 seconds</li><li>Maximum allowed value: 1800 seconds</li></ul>{:/}|

## Sync manager constraints

Use the sync constraints configuration section to specify desktop files and folders that should not be 
synced to the server, such as temporary files or work files.

Constraint rules are specified as `syncmanager.constraint.<n>=<rule>`, where:

* `<n>` is an ascending number starting at one
* `<rule>` is specified as `<ruletype>|<parameter>[,<parameter>,...]`

The available constraint rule types are:

|Constraint rule type|Description|
|--------------------|-----------|
|FileExt|Ignores files with a particular file extension. Multiple extensions can be specified per rule.|
|Name|Ignores files with a particular name. Multiple names can be specified per rule.|
|NamePattern|Ignores files that match a regular expression. Multiple regular expressions can be specified per rule.|
|FolderNamePattern|Ignores folders that match a regular expression. Multiple regular expressions can be specified per rule. |

Here is a sample sync constraints configuration section:

```bash
# Sync constraints

syncmanager.constraint.1=FileExt|.tmp,.temp
syncmanager.constraint.2=Name|desktop.ini,thumbs.db,.DS_Store
syncmanager.constraint.3=NamePattern|~\\$.*\\.doc,~\\$.*\\.docx,~\\$.*\\.xlsx,~\\$.*\\.pptx,~\\$.*\\.xls,~\\$.*\\.ppt,~\\$.*\\.xlsm
syncmanager.constraint.4=NamePattern|\\._.*
syncmanager.constraint.5=NamePattern|^[0-9A-F]{8}
syncmanager.constraint.6=FolderNamePattern|^[0-9A-F]{8}
```

## Disk space limits

Desktop Sync is initially configured to only sync content when the available disk space on a computer is above a 
specific limit (defined by `syncmanager.freeSpaceLimit`). By default value, the minimum amount of free space required 
is set to 3GB. Below this value, Desktop Sync will pause syncing, until the available disk space reaches an 
upper limit (`syncmanager.freeSpaceRestart`). When the available disk space reaches this value, syncing will restart. 
The default value for restarting sync is set to 3500MB (or 3.5GB).

If you wish to override the default settings, add these entries to your configuration file with new values:

```bash
# Free space limits
    
syncmanager.freeSpaceLimit=3G
syncmanager.freeSpaceRestart=3500M
```

>**Note:** Since floating point values aren't valid, you can set a property value to `3500M` (that's 3500MB) 
>to represent 3.5GB. Also, `syncmanager.freeSpaceRestart` should have a higher value than `syncmanager.freeSpaceLimit`.

The free space properties are specified as `syncmanager.freeSpace<Property>=<value>[<scale>]` where:

* `<value>` is an integer
* `<scale>` provides optional scaling using `K|M|G|T` for kilobyte, megabyte, gigabyte, and terabyte values
* add `+/-` in front of the `<value>` to specify values relative to the currently available free space: '+' specifies the limit above the currently available disk space; '-' specifies the limit below the currently available disk space.

To specify a simple limit, without using any scaling, use this example:

```bash
syncmanager.freeSpaceLimit=1073741824
```

In this example, the minimum amount of disk space required for content syncing is set to 1GB.

To specify relative values above the current available disk space, use this example:

```bash
syncmanager.freeSpaceLimit=+2G
syncmanager.freeSpaceRestart=+2500M
```

In this example, the `freeSpaceLimit` is set 2GB above the available space and the `freeSpaceRestart` is set 2.5GB above the current available space. So if you have 3GB of free disk space and your `freeSpaceLimit` is set 2GB, when the free space on your hard drive reaches 5GB, sync will pause. Sync only resumes once your hard drive has 5.5GB of free space.

You can also specify relative values below the current available disk space, use this example:

```bash
syncmanager.freeSpaceLimit=-3G
syncmanager.freeSpaceRestart=-3500M
```

In this example, the `freeSpaceLimit` is set 3GB below the available space and the `freeSpaceRestart` is set 3.5GB below the current available space.

## Force maximum size for user sync

You can limit the amount of data that a user can select to sync by setting `syncmanager.maxSyncSize` to `10` bytes or more. This property is only checked in the content selection dialog. When this is set and the data to sync exceeds the limit, you'll be notified in the content selection dialog, and the **Sync** button is disabled.

The `syncmanager.maxSyncSize` property is specified as:

```bash
syncmanager.maxSyncSize=<number of bytes greater than 10>
```

> **Note:**
>
> * If the size is set to `0` or less than `10` bytes, then no limit is set.
> * The value of the property must be an integer followed by one character: `K|M|G|T` for kilobyte, megabyte, gigabyte, and terabyte values (where 1K = 1 kilobyte = 1024 bytes).
> * If the value is not set correctly, then the maximum size limit defaults to bytes. For example, if there's an illegal character in the value, like `12W345K`, then the limit will be set to just `12` bytes.

## CMIS transfers

Use the CMIS transfer properties to control problems with slow or stalled data transfers when Desktop Sync is 
downloading or uploading content to/from the Alfresco Content Services CMIS server.

|Property|Default value|Description|
|--------|-------------|-----------|
|cmis.lowSpeedTime|30 seconds|Specifies the number of seconds of low speed transfer that are required for a data transfer to be aborted.|
|cmis.lowSpeedLimit|1 bytes per second|Specifies the number of bytes per second that is considered to be a slow data transfer.|
|syncmanager.resumeDownloadFileSize|500K|Specifies the size limit above which a download will resume. Default value is 500KB.|

## CMIS content type mappings

When files are uploaded to the Alfresco Content Services CMIS server they should have a mimetype associated with them. 
Desktop Sync contains a list of built-in file extension to mimetype mappings, but in some cases it may be necessary 
to add new mappings or override existing mappings.

The CMIS content type mappings are specified as `cmis.contentType.<n>=<extension>,<mimetype>`, 
where `<n>` is an ascending number starting at one.

Here is a sample CMIS content type mapping configuration section:

```bash
# CMIS content type mappings

cmis.contentType.1=pptx,application/vnd.ms-powerpoint
cmis.contentType.2=test,application/test
```

## Networking

|Property|Default value|Description|
|--------|-------------|-----------|
|net.SSLVerifyPeer|true|Specifies whether an SSL connection to the Alfresco server does full SSL verification. If the Alfresco server is using a self-signed certificate for SSL, the value must be set to `false`.|
|net.syncServer.SSLVerifyPeer|true|Specifies whether an SSL connection to the sync server does full SSL verification. If the sync server is using a self-signed certificate for SSL, the value must be set to `false`.|

## Debug logging

Desktop Sync can generate a lot of debug information or error level logging information.

The log output configuration contains two sections.

Use the first section to setup the log location, default logging level, formatting, rotation, and compression.

Here is a sample logging configuration section:

```bash
# Logging

logging.loggers.root.channel = c1
logging.loggers.root.level = error
logging.channels.c1.class = FileChannel
logging.channels.c1.path = ${alfresco.configDir}/AlfrescoDesktopSync.log
logging.channels.c1.formatter.class = PatternFormatter
logging.channels.c1.formatter.pattern = %Y-%m-%d %H:%M:%S.%c %N[%P]:%s:%q:%t
logging.channels.c1.rotation=daily
logging.channels.c1.compress=true
logging.channels.c1.purgeAge=7 days
logging.channels.c1.archive=timestamp
logging.formatters.f1.class = PatternFormatter
#logging.formatters.f1.formatter.pattern = %Y-%m-%d %H:%M:%S.%c %N[%P]:%s:%q:%t
logging.formatters.f1.times = UTC
```

This logging configuration will create a log file called `AlfrescoDesktopSync.log` in the following folder:

* Windows: `<userHome>\AppData\Local\Alfresco`
* Mac: `~/Library/Application Support/Alfresco`

The log files are rotated daily and the old log files are compressed. Only the last 7 days of log files are kept.

Use the later section of the log output configuration to enable debug output from different components of Desktop Sync. 
This is done by configuring individual logging levels as shows below:

```bash
logging.loggers.l<n>.name = <logging level name>
logging.loggers.l<n>.level = <debug|error>
```

where `<n>` is an ascending index number starting at one. Both the configuration lines must use the same index number.

The available debug logging levels are:

|Debug logging level|Description|
|-------------------|-----------|
|AccountSetup|Account setup, create/remove sync targets|
|AlfrescoAPI|Alfresco API calls|
|AlfrescoFileStoreMonitor|Remote file system event polling|
|CMISAPI|CMIS API calls|
|CMISFileStore|Remote file I/O|
|CMISFilter|Repository node type/aspect filters|
|CMISObjectCache|CMIS objects cache|
|DeferredCheckSyncPattern|Deferred files special handling|
|DeleteAddSyncPattern|Delete/add (drag/drop cut/paste) local event special handling|
|DeleteRenameSyncPattern|Delete/rename local event special handling|
|DeviceRegAPI|Device registration API calls|
|DirectoryWatcher|Low level local file system event handling|
|DirRouter|Routing of local file system events|
|DumpJSON|JSON request responses|
|KeychainAPI|MacOS keychain access|
|LibCURLAPI|LibCurl low level HTTP network I/O processing|
|LocalFileStore|Local file I/O|
|LocalSyncScanner|Sync manager startup local sync area scanner|
|PocoSQLiteDB|Sync database access|
|RenameShuffleSyncPattern|MS Office rename/shuffle local event special handling|
|RESTAPI|Base REST API processing|
|SharedWin32FileStoreMonitorSharedMacOSXFileStoreMonitor|Local file system monitoring|
|SyncChecker|Consistency checker|
|SyncClientAPI|Shell extension to sync client application calls|
|SyncConstraint|File/folder name/extension constraints|
|SyncEventManager|Event queue manager|
|SyncManager|The top level sync component|
|SyncServiceAPI|Sync Service API calls|
|SyncServiceRouter|Shared synchronization service polling/event routing|
|SyncTarget|Handles the connection between a single local/remote folder|
|SyncUI|Desktop Sync UI configuration properties|
|TargetDelete|Sync target delete parent folder special handling|
|TargetMoveToFrom|Move files/folders between sync targets special handling|
|TargetRename|Sync target parent folder rename special handling|
|WaterMark|File watermarking (not currently used)|

Here's a sample Desktop Sync logging configuration:

```bash
# Logging

logging.loggers.root.channel = c1
logging.loggers.root.level = error
logging.channels.c1.class = FileChannel
logging.channels.c1.path = ${alfresco.configDir}/AlfrescoDesktopSync.log
logging.channels.c1.formatter.class = PatternFormatter
logging.channels.c1.formatter.pattern = %Y-%m-%d %H:%M:%S.%c %N[%P]:%s:%q:%t
logging.channels.c1.rotation=daily
logging.channels.c1.compress=true
logging.channels.c1.purgeAge=7 days
logging.channels.c1.archive=timestamp
logging.formatters.f1.class = PatternFormatter
#logging.formatters.f1.formatter.pattern = %Y-%m-%d %H:%M:%S.%c %N[%P]:%s:%q:%t
logging.formatters.f1.times = UTC

logging.loggers.l1.name = SyncManager
logging.loggers.l1.level = debug

logging.loggers.l2.name = SyncTarget
logging.loggers.l2.level = debug

logging.loggers.l3.name = DirectoryWatcher
logging.loggers.l3.level = error

logging.loggers.l4.name = SharedMacOSXFileStoreMonitor
logging.loggers.l4.level = error

logging.loggers.l5.name = CMISAPI
logging.loggers.l5.level = error

logging.loggers.l6.name = PocoSQLiteDB
logging.loggers.l6.level = error
```

For more details on the logging configuration, see the [PocoProject](https://pocoproject.org/){:target="_blank"} documentation.

## Change timezone {#change-timezone}

The default timezone used in the `AlfrescoDesktopSync.log` file is `UTC`. As an IT administrator, if you want to change this so that the log file uses your local timezone, edit the configuration file:

1. Remove the line `logging.formatters.f1.times = UTC`.
2. Add the following lines:

    ```bash
    logging.channels.c1.formatter.times = local
    logging.formatters.f1.times = local
    ```

3. Restart the Desktop Sync client, and open the log file to see the changes.

## Localization

Desktop Sync supports 16 languages across the user interface, notifications and right-click context menu. 
The language is automatically set based on your computer locale settings, but this can be overridden by 
adding one of the following `syncui.language` values:

|Language|Value (Windows)|Value (Mac)|
|--------|-----------------|-------------|
|English (US)|en|en|
|Brazilian Portuguese|pt-BR|pt\_BR|
|Czech|cs-CZ|cs|
|Danish|da-DK|da|
|Dutch|nl-NL|nl|
|Finnish|fi-FI|fi|
|French|fr-FR|fr|
|German|de-DE|de|
|Italian|it-IT|it|
|Japanese|ja-JP|ja|
|Norwegian Bokmål|nb-NO|nb|
|Polish|pl-PL|pl|
|Russian|ru-RU|ru|
|Simplified Chinese|zh-CN|zh\_CN|
|Spanish|es-ES|es|
|Swedish|sv-SE|sv|

>**Note:** If you're using MacOS Mojave, after switching languages (e.g. from Japanese to Spanish), 
>the options in the content context menu in Finder will remain in the first language. 
>To fix this, reset the Desktop Sync Finder Extension and **Relaunch** Finder:
>
>1. Hold the ⌥ (alt/option) key on your keyboard.
>2. Right-click on the **Finder** icon in your Dock.
>3. Click **Relaunch**.

## Automatic installation updates

You can manage the installation of your Desktop Sync client apps by uploading an installation file in a 
central location in Alfresco Content Services. This allows you to update the installed version of all your 
Desktop Sync clients without any manual intervention.

See [Managing automatic installation updates]({% link desktop-sync/latest/admin/index.md %}#manage-automatic-installation-updates) for more.

## Automatic configuration updates

You can manage the configuration of your Desktop Sync client apps by uploading a configuration file in a 
central location in Alfresco Content Services. This allows you to update the configuration settings for all your 
Desktop Sync clients without any manual intervention.

See [Managing automatic configuration updates]({% link desktop-sync/latest/admin/index.md %}#manage-automatic-configuration-updates) for more.

## Manage sync configuration methods

As an IT administrator, you can manage the configuration of your Desktop Sync client apps via the Desktop Sync UI and a configuration file. You can choose to enable or disable the content selection dialog from the UI for all your Desktop Sync clients, while setting enforced paths to sync from the configuration file.

See [Manage sync configuration]({% link desktop-sync/latest/admin/index.md %}#manage-sync-configuration) for more.

## Force users to sync specific paths {#force-user-sync}

You can configure your Desktop Sync client apps to enforce the sync and exclusion of specific paths or Sites that are added to the configuration file. This allows you to restrict what your Desktop Sync clients sync by pre-selecting the sync folders.

See [Manage enforced sync]({% link desktop-sync/latest/admin/index.md %}#manage-enforced-sync) for more.

## Hide specific paths from users {#hide-from-sync}

You can configure your Desktop Sync client apps to hide specific paths or Sites that are added to the configuration file. This allows you to restrict what your Desktop Sync clients sync by hiding those locations from view in the content selection dialog.

See [Manage hidden sync]({% link desktop-sync/latest/admin/index.md %}#manage-hidden-sync) for more.
---
title: Install Desktop Sync
---

Your Alfresco Administrator can give you a link or location to download the Desktop Sync installation files for Windows and Mac.

{% capture windows %}

If you want to use Desktop Sync on Windows, you'll need:

* Windows 10: 64-bit or 32-bit version
* Windows 7: 64-bit or 32-bit version

To install Desktop Sync, follow these steps.

1. Download the setup file:

    * Windows 64-bit: `Alfresco-Desktop-Sync-Setup-v1.17.x_64.exe`

2. Double-click the downloaded file to run it.

    A wizard will install Alfresco Desktop Sync for you at `C:\Program Files\Alfresco\Alfresco Desktop Sync`.

After the installation is over, the Desktop Sync login screen appears.

### Setting up Desktop Sync on Windows

The first time you open Desktop Sync you need to enter your login details to connect to Alfresco.

1. Open Desktop Sync just as you would any other program by double-clicking the icon on your desktop or opening it through Explorer.

    Speak to your IT team if you need any help.

2. Enter the Alfresco address supplied by your IT team.

    This is the address of the server - make sure the URL provided is the repository URL.

    This could be, for example, `https://alfresco.mycompany.com/alfresco`.

3. When prompted, log in using your user name and password.

4. Click **Sign In**.

    That's it. Your Desktop Sync account is now set.

The **Select sites and folders to sync** screen appears.

![Initial sync selection screen]({% link desktop-sync/images/setup-1.17.png %}){:height="555px" width="346px"}

All your favorite Alfresco content, My Files, Shared Files, and your Alfresco sites are displayed.

{% endcapture %}

{% capture mac %}

If you want to use Desktop Sync on Mac, you'll need:

* Mac OS version 10.13 or later

1. Download the Mac installation file: `Alfresco-Desktop-Sync-v1.17.x.dmg`

2. Double click the downloaded file to unpack the content.

3. Double click the PKG file to start the installation: `Alfresco-Desktop-Sync-v1.17.x.pkg`

    A wizard will install Alfresco Desktop Sync at `/Applications/Alfresco Desktop Sync`.

4. Click **Change Install Location** to choose another location.

    You may be asked to enter your Mac OS X password to complete the installation.

5. Click **Install Software** to continue.

6. Click **Close** to close the setup wizard.

    The Alfresco Desktop Sync icon is added automatically to your `/Applications` folder.

Now you're ready to log in to Desktop Sync and set up your account.

>**Note:** The Desktop Sync Finder Extension does not automatically start in Mac OS Mojave (10.14). To enable the Extension in Mojave, **Relaunch** Finder:
>
>1. Hold the ⌥ (alt/option) key on your keyboard.
>2. Right-click on the **Finder** icon in your Dock.
>3. Click **Relaunch**.

### Setting up Desktop Sync on Mac

The first time you open Desktop Sync you need to enter your login details to connect to Alfresco Content Services.

1. Open Desktop Sync from your **Applications**.

    The Alfresco Desktop Sync login dialog appears. Speak to your IT team if you need any help.

2. Enter the address supplied by your IT team.

    This is the address of the server - make sure the URL provided is the repository URL.

    This could be, for example, `https://alfresco.mycompany.com/alfresco`.

3. When prompted, log in using your user name and password.

4. Click **Sign In**.

    That's it. Your Desktop Sync account is now set.

The **Select sites and folders to sync** dialog appears.

![Initial sync selection screen]({% link desktop-sync/images/setup-mac-1.9.png %}){:height="382px" width="640px"}

All your Alfresco Content Services folders will be displayed from My Files, Shared Files, and your Sites.

### Uninstalling Desktop Sync on Mac

Before uninstalling Desktop Sync for Mac you should first remove your account then drag the application to the Trash. You can then perform a number of checks to verify that the content has been removed cleanly.

1. Click ![alfresco]({% link desktop-sync/images/ico-ds-alfresco.png %}){:height="18px" width="18px"} then ![settings]({% link desktop-sync/images/ds-ico-settings.png %}){:height="18px" width="18px"} to access **Settings**, and select **Remove Account**.

    This removes the content subscriptions, device registration, keychain, databases, etc.

2. Click Quit to shutdown Desktop Sync.

3. Drag the Desktop Sync application from the `Applications` folder to the Trash.

    This ensures that the application is removed cleanly.

4. In Finder, click on the **Go** menu and select **Go to Folder...**.

    A text field appears.

5. Paste the path `~/Library/Application Support` into the text field and click **Go**.

6. Delete the `Alfresco` folder.

    This removes the sync logs, database files, and configuration files.

7. Open `/<userHome>` and delete the `Alfresco` folder.

    This removes any remaining synced content, such as orphaned files, i.e. any content that was in conflict when you removed your account.

    > **Note:** You don't need to uninstall the Desktop Sync client before installing a new version. Simply run the new installer to update the application.

{% endcapture %}

{% include tabs.html tableid="install" opt1="Windows" content1=windows opt2="Mac" content2=mac %}
---
title: Supported platforms
---

The following are the supported platforms for Desktop Sync 1.17:

| Version | Notes |
| ------- | ----- |
| Content Services 23.x | Requires Alfresco Sync Service 4.0 |
| Content Services 7.4.x | |
| Content Services 7.3.x | |
| Content Services 7.2.x | |

> **Note:** This version of Desktop Sync doesn't support Smart Folders.
---
title: Upgrade Desktop Sync
---

You'll be notified when a newer version of Desktop Sync is provided by your IT team. 
This is shown as a notification in the system tray (Windows) or in the menu bar (Mac).

When a new version of Desktop Sync is available to install, a warning icon is displayed.

1. Click the notification or select one of the following options:

    * (Windows) Right-click the system tray icon and select **Update client**.
    * (Mac) Click the menu bar icon and select **Update client**.
    
    The new installer is downloaded to your local **Downloads** folder.

2. Once the download completes, then the installer starts automatically.

3. Follow the steps in [Installing Desktop Sync]({% link desktop-sync/latest/install/index.md %}) to complete the installation.

    >**Note:**
    >
    >* If the download fails, then a notification is shown. Re-try the installer download to continue.
    >* If you choose to defer the update, or the install doesn't complete, then the notification is repeated daily, and each time that the app is restarted.
---
title: Compatibility with Alfresco Governance Services
---

Desktop Sync is fully compatible with Alfresco Governance Services. 
This topic explains how Desktop Sync handles records and classified files.

## Initial content sync

Sites and folders available to synchronize may already include files that have been 
declared as records and/or files that are classified. When synchronization starts, the files are treated as follows:

* **Classified Files** are not synchronized to any users desktops
* **Records** are synchronized as read-only files, which can't be edited on the desktop
* The Records Management File Plan is not available to synchronize

## Content synchronization

Once the initial synchronization is completed, Governance actions are treated in specific ways:

* When a file is **Classified** then it's removed from users desktops
* Files that are **Declared as Records** are synchronized as ready only
* If a Classified file is **Declassified** then synchronization will resume
* If a record is **Rejected**, then its editable state will return where user permissions are sufficient

## Desktop record declaration

Files can be declared as records from within Windows Explorer (Windows) or Finder (Mac).

* Windows: Right-click the file and select **Declare as Record** under **Alfresco Sync**
* Mac: Right-click the file and select **Declare as Record**

>**Note:** **Declare as Record** is not available with Alfresco One 5.1.

## Hidden records

Records that are hidden from a collaboration site are removed from users desktops.
---
title: Application icons and menu
---

The following sections describe the Desktop Sync icons and menu actions on Windows and Mac.

{% capture windows %}

### Desktop Sync icons

Desktop Sync always ensures that the files in your `C:\Users\<username>\Alfresco` folder are synced with Alfresco. It adds status icons to your files and folders so you know the application is working.

You'll see icons in two different places: in the system tray and over individual files and folders.

#### System tray icons

Icons that appear over the Desktop Sync icon in your system tray represent the overall status of your `Alfresco` folder. Here's what each of these icons means.

|Icon name|System tray icon|Description|
|---------|----------------|-----------|
|Green tick|![]({% link desktop-sync/images/ds-greentick.png %}){:height="35px" width="35px"}|A green tick shows all your files are synced and accessible from your desktop.|
|Red cross|![]({% link desktop-sync/images/ds-redcross.png %}){:height="35px" width="35px"}|A red cross indicates there are conflicts that need to be resolved by the user. Something isn't working properly and your file(s) are not being synced.|
|Pause|![]({% link desktop-sync/images/ds-pause.png %}){:height="35px" width="35px"}|A pause icon indicates that Desktop Sync is paused due to invalid server credentials or there's nothing configured to sync.|
|Warning|![]({% link desktop-sync/images/ds-hcfail-mac.png %}){:height="35px" width="35px"}|A warning icon indicates that either:{::nomarkdown}<ul><li>Desktop Sync failed to get a successful server health check. Contact your IT team if you see this warning when you're having problems working with your files.</li><li>An update is available for Desktop Sync (i.e. the installed version is older than the one provided by your IT team).</li></ul>{:/}|
|Offline|![]({% link desktop-sync/images/ds-offline-mac.png %}){:height="35px" width="35px"}|An offline icon indicates that Desktop Sync isn't connected to Alfresco and you are working offline. Check your Internet connection to resume syncing your files.|

#### Context menu icons

Icons that appear over individual files and folders represent the status of that file or folder. Here's what each of these icons means.

|Icon name|Context menu icon|Description|
|---------|-----------------|-----------|
|Green tick|![]({% link desktop-sync/images/ds-ico-synced.png %}){:height="35px" width="35px"}|It's synced - A green tick on a file indicates that the file or folder is in sync with the server copy.|
|Refresh arrows|![]({% link desktop-sync/images/ds-ico-pending.png %}){:height="35px" width="35px"}|It's in use - Blue arrows indicate that Desktop Sync is waiting for the application to release the file or for free space to become available, or a server file to be checked in.|
|Red flag|![]({% link desktop-sync/images/ds-ico-conflict.png %}){:height="35px" width="35px"}|It's in conflict - A red cross on a file or folder indicates that update/rename/delete has conflicted with a server-side change and we were not able to automatically resolve it. You need to decide which version to keep.|
|Grey arrow|![]({% link desktop-sync/images/ds-ico-checkedout-other.png %}){:height="35px" width="35px"}|It's checked out by another user. A grey arrow indicates that the file is checked out by another user in Alfresco. The file is locked, so you can't make changes until the file is checked in, or the check out is cancelled.|
|Blue arrow|![]({% link desktop-sync/images/ds-ico-checkedout.png %}){:height="35px" width="35px"}|It's checked out by you. A blue arrow indicates that the file is checked out by you. The file is locked on the server, so others can't make changes until the file is checked in, or the check out is cancelled.|
|Grey pencil|![]({% link desktop-sync/images/ds-ico-readonly.png %}){:height="35px" width="35px"}|It's read-only. A grey pencil indicates that you don't have permission to edit this file. This could be due to insufficient privileges on the server, or the file has been declared as a record.|

### Explorer menu actions

You can access Desktop Sync actions through the Windows File Explorer context menu by right clicking on a file or folder.

|Action|Description|
|------|-----------|
|Sync Now|Use this option when you want to sync content immediately.|
|Check Out|When you check out a file, it's locked in Alfresco, so that other users can't overwrite it while you make changes offline. This also applies when [working with multiple files in Explorer]({% link desktop-sync/latest/using/app-menu.md %}#working-with-multiple-files-in-windows-explorer).|
|Check In|Shown only when you have one or more files checked out. Select this option when you're ready to upload a new version to Alfresco. See [working with multiple files in Explorer]({% link desktop-sync/latest/using/app-menu.md %}#working-with-multiple-files-in-windows-explorer) for more.|
|Cancel Check Out|Shown only when you have one or more files checked out. You can cancel editing to unlock the file(s) without saving changes. See [working with multiple files in Explorer]({% link desktop-sync/latest/using/app-menu.md %}#working-with-multiple-files-in-windows-explorer) for more.|
|Resolve|Shown only when you need to resolve a conflict. Selecting this option opens a screen where you can decide to keep your changes or the changes from the server.|
|Declare as Record|Shown only when Alfresco Governance Services is running. Select this option to declare the file as a record. See [Declaring records]({% link governance-services/latest/using/easy-access-records.md %}#file-as-record) for more. **Note:** Files previously rejected as a record can't be automatically declared again. See [Managing unfiled records]({% link governance-services/latest/using/manage-fileplan.md %}#managing-unfiled-records) for information on resetting the status.|
|Share|Shown only when you right-click a file (i.e. not a folder). Select this option to share a link to a file. See [Sharing files]({% link desktop-sync/latest/using/sharing.md %}#sharing-on-windows) for more.|
|Version History|Select this option to view and manage the version history of a file. See [Version history]({% link desktop-sync/latest/using/versions.md %}) for more.|
|Properties|Select this option to view, edit, and update properties directly in Desktop Sync. See [Properties]({% link desktop-sync/latest/using/metadata.md %}#manage-the-properties-for-content-on-windows) for more.|
|Update Desktop Sync|Shown only when a newer version of Desktop Sync is provided by your IT team. Select this option to update Desktop Sync. See [Updating Desktop Sync]({% link desktop-sync/latest/upgrade/index.md %}) for more.|

{% endcapture %}

{% capture mac %}

### Desktop Sync icons

Desktop Sync always ensures that the files in your `/<userHome>/Alfresco` folder are synced with Alfresco. It adds status icons to your files and folders so you know the application is working.

You'll see icons in two different places: in the menu bar and next to individual files and folders.

#### Menu bar icons

Icons that appear over the Desktop Sync icon in your menu bar represent the overall status of your Alfresco folder.

Here's what each of these icons means.

|Icon name|Icon|Description|
|---------|----|-----------|
|Green tick|![]({% link desktop-sync/images/ds-synced-mac.png %}){:height="35px" width="35px"}|A green tick shows all your files are synced and accessible from your desktop.|
|Red flag|![]({% link desktop-sync/images/ds-conflict-mac.png %}){:height="35px" width="35px"}|A red flag indicates there are conflicts that need to be resolved by the user. Something isn't working properly and your file(s) are not being synced.|
|Blue arrows|![]({% link desktop-sync/images/ds-syncing-mac.png %}){:height="35px" width="35px"}|A syncing icon indicates that file(s) are being synced or waiting to be synced.|
|Pause|![]({% link desktop-sync/images/ds-pause-mac.png %}){:height="35px" width="35px"}|A pause icon indicates that Desktop Sync is paused due to invalid server credentials or there's nothing configured to sync.|
|Warning|![]({% link desktop-sync/images/ds-hcfail-mac.png %}){:height="35px" width="35px"}|A warning icon indicates that either:{::nomarkdown}<ul><li>Desktop Sync failed to get a successful server health check. Contact your IT team if you see this warning when you're having problems working with your files.</li><li>An update is available for Desktop Sync (i.e. the installed version is older than the one provided by your IT team)</li></ul>{:/}.|
|Offline|![]({% link desktop-sync/images/ds-offline-mac.png %}){:height="35px" width="35px"}|An offline icon indicates that Desktop Sync isn't connected to Alfresco and you are working offline. Check your Internet connection to resume syncing your files.|

#### Content icons

Icons that appear next to individual files and folders represent the status of that file or folder.

Here's what each of these icons means.

|Icon name|File / Folder icon|Description|
|---------|------------------|-----------|
|Green tick|![]({% link desktop-sync/images/ds-ico-synced.png %}){:height="35px" width="35px"}|It's synced - A green tick on a file indicates that the file or folder is in sync with the server copy.|
|Refresh arrows|![]({% link desktop-sync/images/ds-ico-pending.png %}){:height="35px" width="35px"}|It's in use. The blue arrows indicate that Desktop Sync is waiting for the application to release the file or for free space to become available.|
|Red flag|![]({% link desktop-sync/images/ds-ico-conflict.png %}){:height="35px" width="35px"}|It's in conflict. A red flag on a file or folder indicates that update/rename/delete has conflicted with a server-side change and we aren't able to automatically resolve it. You need to decide which version to keep.|
|Grey arrow|![]({% link desktop-sync/images/ds-ico-checkedout-other.png %}){:height="35px" width="35px"}|It's checked out by another user. A grey arrow indicates that the file is checked out by another user in Alfresco. The file is locked, so you can't make changes until the file is checked in, or the check out is cancelled.|
|Blue arrow|![]({% link desktop-sync/images/ds-ico-checkedout.png %}){:height="35px" width="35px"}|It's checked out by you. A blue arrow indicates that the file is checked out by you. The file is locked on the server, so others can't make changes until the file is checked in, or the check out is cancelled.|
|Grey pencil|![]({% link desktop-sync/images/ds-ico-readonly.png %}){:height="35px" width="35px"}|It's read-only. A grey pencil indicates that you don't have permission to edit this file. This could be due to insufficient privileges on the server, or the file has been declared as a record.|

> **Note:** You can hide the icons displayed in Finder by changing a setting on your Mac. To hide the Finder extension, open **System Preferences > Extensions**. Locate the **Alfresco Desktop Sync** extension, then remove the tick in the check box next to **Finder**.

#### Desktop Sync user interface

Click ![Settings]({% link desktop-sync/images/ico-ds-alfresco.png %}) to open the Desktop Sync User Interface (UI). By default, this is docked (or locked) to the menu bar. Click and drag it away from the menu bar to move it. Here is a brief description of each tab in the UI.

|Tab name|Description|
|--------|-----------|
|Checked out|Displays files that you have checked out from your synced folder in Desktop Sync. You can click the icon or file name to open it, or double-click to reveal the file in Finder. See [working with multiple checked out files]({% link desktop-sync/latest/using/app-menu.md %}#faq/mac) for more.|
|Pending|Displays any changes that are waiting to be synced to Alfresco. **Note:** Files that are currently in use by another application are listed here.|
|Conflicts|Displays a list of files or folders that are in conflict. **Note:** If a folder is in conflict as well as any of its contents (such as a file or sub-folder), special rules apply for how this content is resolved. See [sync conflict resolution guide]({% link desktop-sync/latest/using/sync-conflict-guide.md %}#faq/mac) for more details.|

#### Finder menu actions

You can access Desktop Sync actions through the Finder context menu by right clicking on a file or folder.

|Action|Description|
|------|-----------|
|Sync Now|Use this option when you want to sync content immediately.|
|Check Out|When you check out a file, it's locked in Alfresco, so that other users can't overwrite it while you make changes offline. This also applies when [working with multiple files in Finder]({% link desktop-sync/latest/using/app-menu.md %}#faq/mac).|
|Check In|Shown only when you have one or more files checked out. Select this option when you're ready to upload a new version to Alfresco. See [working with multiple files in Finder]({% link desktop-sync/latest/using/app-menu.md %}#faq/mac) for more.|
|Cancel Check Out|Shown only when you have one or more files checked out. You can cancel editing to unlock the file(s) without saving changes. See [working with multiple files in Finder]({% link desktop-sync/latest/using/app-menu.md %}#faq/mac) for more.|
|Keep my Changes|Shown only when you need to resolve a conflict. Select this option to keep the changes made on your computer. This will sync your changes to Alfresco as a new version.|
|Discard my Changes|Shown only when you need to resolve a conflict. Select this option to discard the changes made on your computer. This will sync the latest version from Alfresco, overwriting your changes in your `Alfresco` sync folder.|
|Declare as Record|Shown only when Alfresco Governance Services is running. Select this option to declare the file as a record. See [Declaring records]({% link governance-services/latest/using/easy-access-records.md %}#file-as-record) for more. **Note:** Files previously rejected as a record can't be automatically declared again. See [Managing unfiled records]({% link governance-services/latest/using/manage-fileplan.md %}#managing-unfiled-records) for information on resetting the status.|
|Share|Shown only when you right-click a file (i.e. not a folder). Select this option to share a link to a file. See [Sharing files]({% link desktop-sync/latest/using/sharing.md %}#faq/mac) for more.|
|Version History|Select this option to view and manage the version history of a file. See [Version history]({% link desktop-sync/latest/using/versions.md %}) for more.|
|Properties|Select this option to view, edit, and update properties directly in Desktop Sync. See [Properties]({% link desktop-sync/latest/using/metadata.md %}#faq/mac) for more.|
|Update Desktop Sync|Shown only when a newer version of Desktop Sync is provided by your IT team. Select this option to update Desktop Sync. See [Updating Desktop Sync]({% link desktop-sync/latest/upgrade/index.md %}) for more.|

> **Note:** From time to time Finder extensions are disabled by another application. To enable them, go to **System Preferences > Extensions** and select **Alfresco Desktop Sync**.

{% endcapture %}

{% include tabs.html tableid="icons" opt1="Windows" content1=windows opt2="Mac" content2=mac %}
---
title: Application menu in taskbar
---

The following sections describe the Desktop Sync application menu on Windows and Mac.

{% capture windows %}

You can access Desktop Sync from the Windows system tray where the application icon appears:

![]({% link desktop-sync/images/ds-system-tray.png %}){:height="32px" width="192px"}

Hover your cursor over the Desktop Sync icon to display sync status information, such as date and time of last sync, sync issues (conflicts), and any pending updates.

![]({% link desktop-sync/images/ds-system-msg.png %}){:height="76px" width="184px"}

Right-click on the Desktop Sync icon ![]({% link desktop-sync/images/ds-icon.png %}) to see the application popup menu:

![]({% link desktop-sync/images/ds-system-menu-1.14.png %}){:height="178px" width="184px"}

### Application menu items

The following section goes through each one of the Desktop Sync menu items.

#### Open

Displays information about checked out files, any pending syncs, and conflicts.

![]({% link desktop-sync/images/conflict-1.17.png %}){:height="374px" width="756px"}

* Select **Checked out** to view information about any files you've checked out from Desktop Sync, for example, file name, file location, and details when the file was downloaded.
* Select **Pending** to view information about any pending syncs, for example, file name, status of the pending sync, modifier, file location, and details when the file was last accessed.
* Select **Conflicts** to view conflict-related information and resolve the conflict. The information displayed includes file name, the conflict or issue, modifier, location of the conflict, and details when the file was last modified.
* Select the file in conflict and click **Resolve**.

To resolve a conflict, choose which version to keep, Alfresco or your changes and click **Keep**:

![]({% link desktop-sync/images/conflict-resolution-1.17.png %}){:height="246px" width="350px"}

* **Alfresco version**: Replaces the local file with the Alfresco copy.
* **My version**: Copies updates made to content locally to Alfresco.

##### Working with multiple checked out files

If several files are **Checked out**, you have the following options:

* Select files individually using the check boxes to the left hand side, or use the select all files check box at the top.
* When you select more than one check box, you can pick bulk actions at the top of the tab, **Check In** and **Cancel Check Out**. If you choose **Check In**, you can select if the new version is a major or minor change, and optionally input a comment. Select **Check In** again to save your changes. This applies the same version change and comment (if added) to all the selected files.

#### Go to Alfresco Folder

Opens the `Alfresco` sync folder for Desktop Sync.

#### Search

Opens the **Search** dialog so you can search your local synced files and folders.

You can only search the content that's already synced in the `Alfresco` folder. This avoids having to use the search feature in Mac Finder/Windows Explorer which takes longer and sometimes provides irrelevant results.

* Start your search by typing in the search field. You'll see results presented even if you've only provided partial search text. In the search results, you'll see files and folders are easily identifiable by their respective icons.
* You can view the search results listed by *Name*, *Location*, *Modified Date*, and *Size*. You can also search by file name and file extension, for example, by entering `png` or `.png`.
* To locate a file from the **Search** dialog, double-click the file/folder icon to show the content in Windows Explorer.

#### Recent Files

Click **Recent Files** to open the Recent Files dialog and view your recently used files in the `Alfresco` sync folder.

* The recently used files are listed by *Name*, *Location*, *Modified Date*, and *Size*, where the most recently updated file is at the top.
* To locate a file from the **Recent Files** dialog, double-click the required file to show the content in Windows Explorer.

#### Sync Now

By default local content is synced to Alfresco immediately and Alfresco content is synced locally every five minutes. Click this if you want content synced immediately.

#### Pause Sync

Pauses Sync if you don't wish to synchronize files from the server, for example when you have a low bandwidth connection.

#### Manage Your Account

You can manage which folders and sites get synced on your desktop and other account details using **Manage Your Account**. The available options are:

* **Manage Folders**: Opens Choose folders and sites to sync screen. See [Select content to sync]({% link desktop-sync/latest/using/select-to-sync.md %}#sync/windows).

    If you deselect a previously synced folder and click **Sync**, then the synced content from your desktop is removed. In case you have any unsynced or conflicted files, they will be orphaned in `C:\Users\<username>\Alfresco\`orphaned.

* **Consistency Check**: Performs a consistency check on Desktop Sync. This is typically used in collaboration with your IT team when you need support.

* **Account Information**: View the account information for Desktop Sync:

    * **User Name** for the currently logged in user.
    * **Storage Used** by the `Alfresco` sync folder on your hard drive.

* **Enter Your New Password**: If you have recently changed your Alfresco password, use this option to update the same password in Desktop Sync.

    The **Have you recently changed your password in Alfresco?** window appears. Specify the updated password to resume syncing and click **Update**.

* **Remove Local Content**: Removes all the synced content from Desktop Sync without the need to remove the user account. This provides support for a customer policy where content is only kept on a device when users are actively working on that content and using Desktop Sync.

    To start using Desktop Sync again, you'll need to set up your synced files via the **Manage Your Account > Manage Folders** menu option. See [Select content to sync]({% link desktop-sync/latest/using/select-to-sync.md %}#sync/windows).

* **Remove Account**: Removes the synced user from Desktop Sync and deletes all the synced content from the desktop. You can still access your files in Alfresco. On removing your account you are taken back to the Desktop Sync login screen. See [Setting up Desktop Sync]({% link desktop-sync/latest/install/index.md %}#setting-up-desktop-sync-on-windows).

#### About

Tells you which version of Desktop Sync you're using.

#### Help

View online help.

#### Quit

Closes Desktop Sync.

You will no longer be able to sync during this time. Syncing will resume when you restart Desktop Sync. Any content updated while Desktop Sync was closed will be synced when the application is restarted.

It's recommended that you always have Desktop Sync up and running so that your local content and Alfresco are in sync.

### Windows Explorer context menu

The folder and file context menu can be accessed via the Windows Explorer.

#### Accessing and using the context menu

To view the Desktop Sync context menu, follow the steps below:

1. Navigate to your synced content (folder or file) in the File Explorer.
2. Right-click the content to access the Explorer menu actions.
3. Click **Sync Now** to sync your content immediately.
4. Click **Check Out** to lock it in Alfresco, so that other users can't overwrite it while you make changes. Once you check out a file, you'll see two more options:
    * **Check In**: Uploads a new version of your content to Alfresco.
    * **Cancel Check Out**: Cancels editing to unlock the file without saving any changes.
5. In the event of a conflict, you'll see one more option:
    * **Resolve**: Selecting this option opens a screen where you can decide to keep your changes or the changes from the server.
6. Click **Share** to enable file sharing when you right-click a synced file. Once set up in your configuration file, this option allows you to share a direct link to a file, so that anyone that has the link can view the file.
    * See [Configuring Desktop Sync]({% link desktop-sync/latest/config/index.md %}) for configuration details.
    * See [Sharing files]({% link desktop-sync/latest/using/sharing.md %}#sharing-files-on-windows) for more.
7. Click **Version History** to view and manage version history when you right-click synced content.
    * See [Version History]({% link desktop-sync/latest/using/versions.md %}) for more.
8. Click **Properties** to enable viewing, editing, and updating of properties when you right-click synced content.
    * See [Properties]({% link desktop-sync/latest/using/metadata.md %}#manage-the-properties-for-content-on-windows) for more.
9. Click **Update Desktop Sync** to download the new installer file to your local Downloads folder. See [Updating Desktop Sync]({% link desktop-sync/latest/upgrade/index.md %}) for more.

#### Working with multiple files in Windows Explorer

You can also work with multiple files by using the Explorer right click menu actions:

* **Sync Now**, **Check Out**, and **Properties**.
* **Check In** and **Cancel Check Out** are displayed if any file is already checked out.
* When you click **Check In**, select if the new version is a major or minor change, and optionally input a comment. Click **Check In** again to save your changes. This applies the same version change and comment (if added) to all the selected files.
* If you have selected a mixture of items, for example where you have files checked out and not checked out, then all the relevant options are shown. When an action is selected, it's only applied to the files that are in a relevant state.
* If any of the files you selected are in conflict, you'll have to resolve these individually, as the conflict resolution options are not displayed.

{% endcapture %}

{% capture mac %}

You can access Desktop Sync from the Mac OS X menu bar where the application icon appears:

![]({% link desktop-sync/images/ds-icon-tray.png %})

* **Application icon**

    Click the Desktop Sync ![Desktop Sync]({% link desktop-sync/images/ico-ds-alfresco.png %}){:height="23px" width="23px"} icon to see more options.

* **Search**

    Click the Search ![Search]({% link desktop-sync/images/ds-ico-search.png %}){:height="23px" width="23px"} icon to open the **Search** dialog and search your local synced files and folders.

    You can only search the content that's already synced in the `Alfresco` folder. This avoids having to use the search feature in Mac Finder/Windows Explorer which takes longer and sometimes provides irrelevant results.

  * Start your search by typing in the search field. You'll see results presented even if you've only provided partial search text. In the search results, you'll see files and folders are easily identifiable by their respective icons.
  * You can view the search results listed by *Name*, *Modified Date*, and *Size*. You can also search by file name and file extension, for example, by entering `png` or `.png`.
  * To locate a file from the **Search** dialog, click the icon on the right side of the required row to show the content in Mac Finder.

* **Sync folder**

    Click the folder ![Sync Folder]({% link desktop-sync/images/ds-open-sync-folder.png %}){:height="23px" width="23px"} icon to open the `Alfresco` sync folder on your computer.

* **Settings**

    Click the ![Settings]({% link desktop-sync/images/ds-ico-settings.png %}){:height="23px" width="23px"} icon to open the Desktop Sync settings menu. See [Settings](#settings) for more details.

### Settings

You can access Desktop Sync settings by clicking the application icon in the menu bar then selecting **Settings**.

Click ![]({% link desktop-sync/images/ico-ds-alfresco.png %}){:height="23px" width="23px"} then ![Settings]({% link desktop-sync/images/ds-ico-settings.png %}){:height="23px" width="23px"} to access the **Settings** options.

#### Pause / Resume Sync

Select Pause Sync when you prefer to work offline, for example due to slow network speeds, or if you're working on a particularly large file. Once you've selected **Pause Sync**, the menu option changes to **Resume Sync**.

Select Resume Sync to resume syncing with Alfresco Content Services.

#### Consistency Check

Performs a consistency check on Desktop Sync. This is typically used in collaboration with your IT team when you need support.

#### Recent Files {#recent-files-mac}

Click **Recent Files** to open the Recent Files dialog and view your recently used files in the `Alfresco` sync folder.

* The recently used files are listed by *Name*, *Modified Date*, and *Size*, where the most recently updated file is at the top.
* To locate a file from the **Recent Files** dialog, click the<!-- icon on the right side of the--> required row to show the content in Mac Finder.

#### Manage Sync Folder

Selecting **Manage Sync Folder** opens the Select sites and folders to sync dialog. This allows you to select more content to sync, or deselect content to stop syncing. See [Select content to sync]({% link desktop-sync/latest/using/select-to-sync.md %}#sync/mac) for more.

If you deselect a previously synced folder and click **Sync**, then the synced content from your desktop is removed. In case you have any unsynced or conflicted files, they will be orphaned in `/<userHome>/Alfresco/orphaned`.

#### Manage Your Account {#manage-your-account-mac}

* **Account Information**

    View the account information for Desktop Sync:

    * **User Name** for the currently logged in user.
    * **Storage Used** by the `Alfresco` sync folder on your hard drive.

* **Remove Local Content**

    Removes all the synced content from Desktop Sync without the need to remove the user account. This provides support for a customer policy where content is only kept on a device when users are actively working on that content and using Desktop Sync.

    To start using Desktop Sync again, you'll need to set up your synced files via the **Manage Sync Folder** menu option. See [Select content to sync]({% link desktop-sync/latest/using/select-to-sync.md %}#sync/mac).

* **Remove Account**

    Removes the synced user from Desktop Sync and deletes all the synced content from the desktop. Use this option as the first stage of uninstalling Desktop Sync.

    You can still access your files in Alfresco. Any content that can't be removed from your desktop is orphaned. On removing your account you are taken back to the Desktop Sync login dialog. Close the login dialog to quit the application. See [Setting up Desktop Sync]({% link desktop-sync/latest/install/index.md %}#faq/mac).

#### Help

View online help.

#### About

View the version number of Desktop Sync you're using.

#### Quit

Closes Desktop Sync.

You won't be able to sync content during this time. Syncing will resume when you restart Desktop Sync. Any content updated while Desktop Sync was closed will be synced when the application is restarted.

It's recommended that you always have Desktop Sync up and running so that your local content and Alfresco are in sync.

### Check Outs, Conflicts and Pending {#checkouts-conflicts-pendingsyncs}

Displays information about checked out files, any pending syncs, and conflicts.

![]({% link desktop-sync/images/ds-tabbed-ui-1.17.png %}){:height="358px" width="260px"}

* Select **Checked out** to view information about any files you've checked out from Desktop Sync, for example, file name, file location, and details when the file was downloaded.
* Select **Pending** to view information about any pending syncs, for example, file name, status of the pending sync, modifier, file location, and details when the file was last accessed.
* Select **Conflicts** to view conflict-related information and resolve the conflict. The information displayed includes file name, the conflict or issue, modifier, location of the conflict, and details when the file was last modified.

    To resolve a conflict, select the conflict and either click:

    * **Discard my changes**: Replaces the local file with the Alfresco copy.
    * **Keep my changes**: Copies updates made to content locally over to Alfresco.

> **Note:** There may be times when you can't resolve a conflict for a file because the parent folder also has a conflict. In this case, your only choice is to resolve the conflict on the folder by either selecting **Keep my changes** or **Discard my changes**. Your choice is then applied to all files within that folder.

### Working with multiple checked out files {#working-with-multiple-checkedout-files-mac}

If several files are **Checked out**, you have the following options:

* Select files individually using the check boxes to the left hand side, or use the select all files check box at the top.
* When you select more than one check box, you can pick bulk actions at the top of the tab, **Check In** and **Cancel Check Out**. If you choose **Check In**, you can select if the new version is a major or minor change, and optionally input a comment. Select **Check In** again to save your changes. This applies the same version change and comment (if added) to all the selected files.

### Update password

Desktop Sync doesn't allow you to change your password directly. However, if your [password changes]({% link content-services/latest/using/dashboard.md %}#changing-your-password) in Alfresco Share, you will see a notification in Desktop Sync asking you to update your password. Click **Update Password** to continue.

### Mac Finder context menu

The folder and file context menu can be accessed via the Mac Finder.

#### Accessing and using the context menu

To view the Finder menu actions, follow the steps below:

1. Navigate to your synced content in Finder.
2. Right-click on a file or folder to access the Finder menu actions.
3. Click **Sync Now** to sync your content immediately.
4. Click **Check Out** to lock it in Alfresco, so that other users can't overwrite it while you make changes offline. Once you check out a file, you'll see two more options:
    * **Check In**: Uploads a new version of your content to Alfresco.
    * **Cancel Check Out**: Cancels editing to unlock the file without saving any changes.
5. In the event of a conflict, you'll see two more options:
    * **Discard my Changes**: Replaces the local file with the Alfresco copy.
    * **Keep my Changes**: Copies updates made to content locally over to Alfresco.
6. Click **Share** to enable file sharing when you right-click a synced file. Once set up in your configuration file, this option allows you to share a direct link to a file, so that anyone that has the link can view the file.
    * See [Configuring Desktop Sync]({% link desktop-sync/latest/config/index.md %}) for configuration details.
    * See [Sharing files]({% link desktop-sync/latest/using/sharing.md %}#faq/mac) for more.
7. Click **Version History** to view and manage version history when you right-click synced content.
    * See [Version History]({% link desktop-sync/latest/using/versions.md %}) for more.
8. Click **Properties** to enable viewing, editing, and updating of properties when you right-click synced content.
    * See [Properties]({% link desktop-sync/latest/using/metadata.md %}#faq/mac) for more.
9. Click **Update Desktop Sync** to download the new installer file to your local Downloads folder. See [Updating Desktop Sync]({% link desktop-sync/latest/upgrade/index.md %}) for more.

#### Working with multiple files in Finder

You can also work with multiple files by using the Finder right click menu actions:

* **Sync Now**, **Check Out**, and **Properties**.
* **Check In** and **Cancel Check Out** are displayed if any file is already checked out.
* When you click **Check In**, select if the new version is a major or minor change, and optionally input a comment. Click **Check In** again to save your changes. This applies the same version change and comment (if added) to all the selected files.
* If you have selected a mixture of items, for example where you have files checked out and not checked out, then all the relevant options are shown. When an action is selected, it's only applied to the files that are in a relevant state.
* If any of the files you selected are in conflict, you'll have to resolve these individually, as the conflict resolution options are not displayed.

{% endcapture %}

{% include tabs.html tableid="menu" opt1="Windows" content1=windows opt2="Mac" content2=mac %}
---
title: Desktop Sync FAQ
---

Here's a list of common questions about Desktop Sync for Windows and Mac.

{% capture windows %}

### So, what gets synced?

Desktop Sync shows you all your Alfresco sites and folders which you have access to, plus your My Files and Shared Files content. You can select any (or all) of these and click **Sync** to create a local copy of the content on your computer.

Individual files you've favorited aren't displayed and can be synced directly, you need to sync the folder they're in.

Whenever you update any of this local content (which includes adding, moving, and deleting files and folders within the synced area) these changes will automatically be replicated on Alfresco.

Whenever you or anyone else make changes in Alfresco to sites or folders that you've synced with, then these changes will be replicated in your local content.

>**Note:** Some temporary files don't get synced. These include, but aren't limited to \*.tmp, \*.temp, desktop.ini, \*.~, and Thumbs.db files. You can configure the file types you don't want to be synced in AlfrescoSync.config. For more information, see [Client configuration]({% link desktop-sync/latest/config/index.md %}).

### Can I use Desktop Sync during initial sync?

Yes. During initial sync, a content created on your desktop will be synced only after the initial sync is over.

### Will syncing happen while I am offline?

Sync needs a connection to the server. Syncing will resume when the connection is restored.

### Where can I find my synced files?

The content is synced to `C:\Users\<username>\Alfresco`, by default, or whatever location you chose after the initial setup. The `Alfresco` folder can also be found in File Explorer under **Favourites**.

### How many folder levels can I sync?

You can sync as many folder levels but the maximum length for a path should not be more than 260 characters. This is a limitation of the Windows File System.

For more information see [Maximum Path Length Limitation](https://docs.microsoft.com/en-gb/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN#maxpath){:target="_blank"}.

### Can I cancel initial sync?

Yes. As a Desktop Sync user, you can either:

* Take your machine offline: You can simply ignore initial sync and shut down your machine or disconnect the network. Initial sync will resume when connection is restored.
* Keep your machine running but discontinue initial sync: You can quit Desktop Sync and initial sync will resume when restart Desktop Sync.
* Amend your selected content choices by clicking **Return to content selection**.

### I made changes to a local file that aren't showing in Alfresco.

A number of scenarios can cause this:

* The file is held/locked open by an application on your computer.
* Network connection problems, Alfresco connection problems, or synchronization service connection problems; contact your IT team.
* If you've made changes locally that are showing in Alfresco, then make sure that Desktop Sync is running by confirming that the ![Menu bar]({% link desktop-sync/images/ico-ds-alfresco.png %}) icon is showing in the system tray.
* It's also possible that someone was updating the content in Alfresco at the same time as you were updating the local content. The file is in conflict state. See sync conflict resolution guide for [Windows]({% link desktop-sync/latest/using/sync-conflict-guide.md %}#resolve-and-manage-sync-conflicts-on-windows).

### What's the *orphaned* folder in my local synced drive?

If you deselect synced content in Desktop Sync and click **Sync**, then you're effectively breaking the link between local content and Alfresco content.

The content won't be synced any more. Files that were not synced to Alfresco due to conflict or deferred can be found in *orphaned* folder. This folder is automatically created in your synced area and the previously synced content is moved to there.

### If a file is checked out by another user in Alfresco, can I update it?

No, you can't update files that are checked out by other users.

### When will a deferred file be synced?

First you need to find the reason why the file is in a deferred state. The file can be in a deferred state for the following reasons.

* When you don't have free space on your desktop.
* If you have an Office file open and you are saving it to your local.
* You're not connected to the server.

Resolve the issue and your file will be synced automatically.

### I see a red cross on my system tray. What does that mean?

See [App icons and context menu]({% link desktop-sync/latest/using/app-icons.md %}#application-icons-and-menu-on-windows).

See also sync conflict resolution guide on [Windows]({% link desktop-sync/latest/using/sync-conflict-guide.md %}#resolve-and-manage-sync-conflicts-on-windows).

### Do I need to restart Desktop Sync when I restart my machine?

No, Desktop Sync is automatically started when your machine starts.

### Can I use Desktop Sync while I am offline?

You can continue working on your files offline and they'll be synced to Alfresco whenever you have a connection to the server.

### What happens to a file/ folder which is moved out of Alfresco folder on my desktop?

The moved file or folder is deleted in Alfresco.

### Why can't I see status icons on my files and folders?

Windows has a limit of 15 icon overlay handlers, some of which are reserved by the system. 
The number of different icon overlay handlers is limited by the amount of space available for icon overlays 
in the system image list. So, uninstalling other applications that use system overlays could make some slots 
available for Desktop Sync icon overlays.

Additionally, check if you have accidentally quit Desktop Sync. Upon restart, the icons should be restored.

See [application icons]({% link desktop-sync/latest/using/app-icons.md %}#application-icons-and-menu-on-windows) 
for more details.

### What happens if two Alfresco sites have the same name?

If the site name is duplicate, one of the site name will be displayed as SiteName_01, for example, Test Site_01.

### What happens if the site name is invalid or contains unsupported Windows characters?

A file name can't contain the following characters: `\ / : * ? " < >`. Desktop Sync replaces these characters with underscores, for example, Test\>test will be replaced as Test_test on your desktop.

### How do I uninstall Desktop Sync?

1. Open **Programs and Features** by clicking **Start**.
2. Click **Control Panel**.
3. Under **Programs**, click **Uninstall a program**.
4. Select Desktop Sync, and then click **Uninstall**.

### Can Desktop Sync be installed in an unattended mode?

Yes.

### Can I setup Desktop Sync using a central installation process?

Yes, Desktop Sync installer contains an MSI, which can be used with any central installation tool, such as Microsoft System Center Configuration Manager.

### I'm running Windows in a Virtual Machine. Why is the automatic update for the configuration file not working correctly?

This is due to folder paths in some virtual machines being non-standard Windows paths.

### I'm running Windows in a Virtual Machine. Why is the automatic update not installing correctly?

The download folder path in some virtual machines is a non-standard Window path, and the installer isn't able to start.

### Upon unselecting, not all files are getting removed. What's wrong?

When a file of folder is locked by Windows File Explorer, applications, like Desktop Sync, can not remove that file and folder. In that case, when unsubscribing content or removing the application, some files and folders maybe left behind. They should be removed manually.

### Where do I find the Desktop Sync log file?

If you're having any issues with Desktop Sync then your Alfresco Administrator might ask you to provide the log file.

You can find the log file in the following locations, but be aware that it's a hidden file. If you don't know how to view hidden files then your Alfresco Administrator can help you.

* Windows - `C:\Users\Administrator\AppData\Local\AlfrescoSync.log`

Additionally, you can use applications, such as DebugView to monitor debug output on your computer. To use DebugView, follow the steps below:

1. Download and install [DebugView](https://docs.microsoft.com/en-gb/sysinternals/downloads/debugview){:target="_blank"}.

    DebugView will immediately start capturing debug output.

2. On the top menu bar, click **Edit** and then **Filter/Highlight...**.

    The **DebugView Filter** window appears.

3. To filter and display only the output from the shell extension, specify `AlfrescoSyncExtension` in **Include** and click **OK**.

### I no longer need a site. How do I remove the site and its contents from my desktop?

Go to **Manage Folders** and deselect the sites you no longer need. Click **Sync** to remove the selected files and folders from your desktop.

### Can I use Desktop Sync while I am offline?

You can continue working on your files offline but they will get synced to Alfresco whenever you have a connection to the server.

### Will syncing happen while I am offline?

Sync needs a connection to the server. Syncing will resume when your connection is restored.

### Will my files be versioned in Alfresco?

Yes. All file updates in Alfresco using Desktop Sync are versioned.

### Can I recover a deleted file using Desktop Sync?

Yes. Any file deleted in Alfresco using Desktop Sync is moved to the Alfresco trash can.

### I have changed the site name in Alfresco. Can I continue using Desktop Sync?

Yes, you can continue working with Desktop Sync but the site name won't be updated in the File Explorer.

### Which file extensions are supported by Desktop Sync?

Desktop Sync syncs all file extensions except for the temporary file extensions mentioned below:

```bash
part,thumbdata3--1967290299,thumbdata3--1763508120,crdownload,~cr,exo,tmp,cvr,download,thumbdata3--number,mxdl,tt2,etl,egt
,csi,thumbdata5--1763508120_0,csd,fseventsd-uuid,localstorage-journal,thumbdata5--1967290299_0,dwl,laccdb,torchdownload,thumbdata5,cache,lck,ewc2,!ut
,regtrans-ms,blf,mmsyscache,sfk,filepart,imgcache,dtapart,sav,aaa,thumbdata,h64,lock,rra,bc
,npk,download,adadownload,hex,tec,chkn,steamstart,partial,thumbdata5--1967290299_1,pnf,idlk,lrd,thumbdata5-1763508120_1,fb!
,temp,waf,tmt,dlm,bu,swo,rcv,reapeaks,dap,pkf,fsf,thumbdata3-1763508120,dmp,db-wal
,pft,little,_501,glh,db-shm,box,cfa,installstate,tv5,tbn,sqlite-journal,dat,thumbdata3-1967290299,onecache
,msj,exd,isl,objectcache,nov,dca,thumbdata4--1967290299,swn,rld,temporaryitems,aso,thumbdata5--1967290299_3,rsc_tmp,bdm
,ptn2,indexarrays,id3tag,thumbdata3,cos2,dia,download,cah,wfm,as$,meb,clp,thumbdata5-1763508120_2,thumbdata4--1763508120
,save,heu,nb2,tof,thumbdata5-1763508120_3,bc!,snapdoc,hrd,rsx,)2(,cache-2,prmdc,bridgecachet,tmd
,fuse_hidden,db3-journal,phc,rdn,ims,cache-3,bsd,thumbdata4,ytf,4sh,tic,hax,buf,init
,cdc,bmc,sqlite3-journal,indexpositions,bts,db,wov,dinfo,indexcompactdirectory,bmb,crc,citriodownload,pkc,pm$
,shadowindexgroups,dtf,peb,bom,oemigaccount,utpart,lai,m_p,md0,bdi,00a,appdownload,inprogress,mbc
,mex,qbi,help,tombstone,csstore,adm,qbt,xp,hmap,@@2,indexdirectory,yumtx,@@1,thumbdata5--1967290299_4
,bridgecache,thumbdata5--1967290299_5,zoner-rawdata-cache,wcc,tst,000,ci,onetmp,indexpositiontable,stf,identcache,qdat,out,inf
,shadowindextermids,adblock,filetablelock,wpk,thumbdata5-1967290299_8,xcuserstate,tv2,aria2,mx1,002,ilp,bv4,par,alt
,nc2,a$v,ddat,cpd,escopy,ipe_tempfile,mpgindex,bv1,tv4,$db,db$,pat,bphys,wa~
,clean,thumbdata5--1967290299_7,^fsf,xps~,sss~,chk,iniis,moz,---,bt0,fts,tv7,wlx,nmu
,swd,dov,bde,~$~,~nt,vsscc,jnk,abc,tv3,thumbdata5-1763508120_6,wsb,dmsk,fes,shadowindexcompactdirectory
,ird,thumbdata5-1763508120_5,qtindex,bv2,svn-work,pzx,$ed,tv1,rad,thumbdata5-1763508120_4,thumbdata5-1763508120_0,$vm,thumbdata5-1763508120_7,compo
,preview7,asab,$$$,pls,pet,001,wtmp,lockfile,ger,tb0,pfc,(d),zoner-index-cache,qp1
,blk,zsr,mtx,wid,ipl22,tv6,vdjcache,xp~,lex,xps,cachedmsg,bv3,f2l,lst
,4sw,wtmp,mov,iff,\#$\#,vmdk-converttmp,bv7,t44,dw3,zl,nav2,bv5,bsi,ccc
,asx,ipl,sdx,u96,dir00,qp2,qtmp,s2mi,fdpart,t$m,hmap.dir,journal,spc,als
,simpl_int,r1m,scuf,dem,patchcache,ers,csac,sfm,thumbdata5-1763508120_8,cnv,vmc,file,s,m
,met,mpx,tv8,zn~,thumbdata5-1763508120_20,cdt,db$,thumbdata5-1763508120_12,ebktml,bv6,tv9,bv8,vaf,thumbnail
,ref,\#\#\#,pspcache,c1s,muf,onlineresources,memb,w44,§§§,dir,lvl,bcm,$a,bv9
,fchc,rgt,ncch,grbdropfile,wrk,cached_icon,thumbdata5-1763508120_17,aecache,mdccache,thumbdata5-1763508120_19,lref,1,0
```

### If a file has a file extension which is in the exempted list above, can I include that file in the sync set?

Yes. In the `<userHome>\AppData\Local\Alfresco\AlfrescoSync.conf` file, in the Sync constraints section, 
update the `syncmanager.constraint.1=FileExt|.tmp,.temp` property

### What files should be backed up/restored on the client ?

You can find the synced data in the `C:\Users\<username>\Alfresco` folder. 
The sync client settings/database/logs can be found in the `C:\Users\<username>\AppData\Local\Alfresco` folder.

When the sync client starts up, it uses the modification time stamp from the `AlfrescoSync.time` file in the `AppData\Local\Alfresco` folder to check if any files/folders were changed while Desktop Sync was not running. If you delete and recreate the `AlfrescoSync.time` file after restoring the Desktop Sync data and settings, it would do a full scan of the local and remote folders.

### I have a new computer, is it possible to migrate my Alfresco sync folder to the new computer?

To avoid problems with conflicts on device registration, and content going out of sync during the migration process, you should first remove your account from the deprecated computer, and then setup Alfresco Desktop Sync on the new machine.

{% endcapture %}

{% capture mac %}

### So, what gets synced?

Desktop Sync shows you all your Alfresco sites and folders which you have access to, plus your My Files and Shared Files content. You can select any (or all) of these and click **Sync** to create a local copy of the content on your computer.

Individual files you've favorited aren't displayed and can be synced directly, you need to sync the folder they're in.

Whenever you update any of this local content (which includes adding, moving, and deleting files and folders within the synced area) these changes will automatically be replicated on Alfresco.

Whenever you or anyone else make changes in Alfresco to sites or folders that you've synced with, then these changes will be replicated in your local content.

> **Note:** Some temporary files don't get synced. These include, but aren't limited to `*.tmp`, `*.temp`, `desktop.ini`, `*.~`, and `Thumbs.db` files. You can configure the file types you don't want to be synced in `AlfrescoSync.config`. For more information, see [Configuring Desktop Sync]({% link desktop-sync/latest/config/index.md %}).

### Can I use Desktop Sync during initial sync?

Yes. During initial sync, any content created on your desktop will be synced only after the initial sync is over.

### Will syncing happen while I am offline?

Sync needs a connection to the server. Syncing will resume when the connection is restored.

### Where can I find my synced files?

The content is synced to `<userHome>/Alfresco`, by default, or whatever location you chose after the initial setup. The `Alfresco` folder can also be found in File Explorer under **Favourites**.

### How many folder levels can I sync?

You can sync as many folder levels on a Mac. This is only a limitation of the Windows File System, where the maximum length for a path should not be more than 260 characters.

### Can I cancel initial sync?

Yes. As a Desktop Sync user, you can either:

* Take your computer offline: You can simply ignore initial sync and shut down your computer or disconnect the network. Initial sync will resume when connection is restored.
* Keep your computer running but discontinue initial sync: You can quit Desktop Sync and initial sync will resume when you restart Desktop Sync.
* Amend your selected content choices by clicking **Return to content selection**.

### I made changes to a local file that aren't showing in Alfresco.

A number of scenarios can cause this:

* The file is held/locked open by an application on your computer.
* Network connection problems, Alfresco connection problems, or synchronization service connection problems; contact your IT team.
* If you've made changes locally that are showing in Alfresco, then make sure that Desktop Sync is running by confirming that the ![Menu bar]({% link desktop-sync/images/ico-ds-alfresco.png %}) icon is showing in the menu bar.
* It's also possible that someone was updating the content in Alfresco at the same time as you were updating the local content. The file is in conflict state. See sync conflict resolution guide for [Mac]({% link desktop-sync/latest/using/sync-conflict-guide.md %}#faq/mac).

### What's the *orphaned* folder in my local synced drive?

If you deselect synced content in Desktop Sync and click **Sync**, then you're effectively breaking the link between local content and Alfresco content.

The content won't be synced any more. Files that weren't synced to Alfresco due to conflict or deferred can be found in the *orphaned* folder. This folder is automatically created in your synced area and the previously synced content is moved to there.

### If a file is checked out by another user in Alfresco, can I update it?

No, you can't update files that are checked out by other users.

### When will a deferred file be synced?

First you need to find the reason why the file is in a deferred state. The file can be in a deferred state for the following reasons.

* When you don't have free space on your desktop.
* If you have an Office file open and you're saving it to your computer.
* You're not connected to the server.

Resolve the issue and your file will be synced automatically.

### I see a red flag on my menu bar. What does that mean?

See [App icons and context menu]({% link desktop-sync/latest/using/app-icons.md %}#faq/mac)

If a file is in conflict and the parent folder is also in conflict:

* You can only resolve the parent folder.
* You can't resolve the child as the Finder menu actions aren't visible.
* Any children in conflict are shown in an indented list below the parent.
* Once you select a resolution, the child is resolved using the same choice as the parent.

See also sync conflict resolution guide on [Mac]({% link desktop-sync/latest/using/sync-conflict-guide.md %}#faq/mac).

### Do I need to restart Desktop Sync when I restart my computer?

No, Desktop Sync is automatically started when your computer starts.

### Can I use Desktop Sync while I am offline?

You can continue working on your files offline and they'll be synced to Alfresco whenever you have a connection to the server.

### What happens to a file/folder which is moved out of Alfresco folder on my desktop?

The moved file or folder is deleted in Alfresco.

### Why can't I see content icons on my files and folders?

If, for some reason, your content icons are hidden in Finder, you can make them visible by checking your **System Preferences**.

See [application icons]({% link desktop-sync/latest/using/app-icons.md %}#faq/mac) for more details.

Additionally, check if you have accidentally quit Desktop Sync. Upon restart, the icons should be restored.

### What happens if two Alfresco sites have the same name?

If the site name is duplicated, one of the site names will be displayed as `SiteName_01`, for example, `Test Site_01`.

### What happens if the site name is invalid or contains unsupported characters?

A file name can't contain the following characters: `\ / : * ? " < >`. Desktop Sync replaces these characters with underscores, for example, `Test>test` is replaced by `Test_test` on your desktop.

### How do I uninstall Desktop Sync?

See [Uninstalling Desktop Sync]({% link desktop-sync/latest/install/index.md %}#faq/mac).

### Can Desktop Sync be installed in an unattended mode?

Yes.

### I'm running Windows in a Virtual Machine. Why is the automatic update for the configuration file not working correctly?

This is due to folder paths in some virtual machines being non-standard Windows paths.

### I'm running Windows in a Virtual Machine. Why is the automatic update not installing correctly?

The download folder path in some virtual machines is a non-standard Windows path, and the installer isn't able to start.

### Upon unselecting not all files are getting removed. What's wrong?

When a file or folder is locked by Finder, applications, like Desktop Sync, can't remove that file and folder. In that case, when unsubscribing content or removing the application, some files and folders maybe left behind. They should be removed manually.

### What is the Icon? file in the Alfresco Content Services sync folder?

`Icon?` is a hidden file that's used by Mac OS X to put the Alfresco Content Services logo on the `Alfresco`sync folder in Finder.

### Where do I find the Desktop Sync log file?

If you're having any issues with Desktop Sync, then your IT team might ask you to provide the log file.

You can find the log file in the following location, but be aware that it's a hidden file. If you don't know how to view hidden files, then your IT team can help you.

* `~/Library/Application Support/Alfresco/AlfrescoSync.log`

### Where do I find the Desktop Sync crash log file?

If Desktop Sync quits unexpectedly, a log file is generated that can help to 
identify potential issues on your Mac. To help troubleshoot the issue, your IT team may ask you to provide the crash log.

To find your crash logs follow these steps.

1. In Finder, click on the **Go** menu and select **Go to Folder...**. A text field should appear in Finder.
2. Paste the path `~/Library/Logs/DiagnosticReports/` into the text field and click **Go**.
3. In this folder, find all log files with filename `Alfresco*.crash`.
4. Send these files to your IT team.

### I no longer need a site. How do I remove the site and its contents from my desktop?

Go to **Settings > Manage Sync Folder** and deselect the sites you no longer need. Click **Sync** to remove the selected files and folders from your desktop.

### Can I use Desktop Sync while I am offline?

You can continue working on your files offline but they will get synced to Alfresco whenever you have a connection to the server.

### Will syncing happen while I am offline?

Sync needs a connection to the server. Syncing will resume when your connection is restored.

### Will my files be versioned in Alfresco?

Yes. All file updates synced in Alfresco using Desktop Sync are versioned.

### Can I recover a deleted file using Desktop Sync?

Yes. Any file deleted in Alfresco using Desktop Sync is moved to the Alfresco trashcan.

### Which file extensions are supported by Desktop Sync?

Desktop Sync syncs all file extensions except for the temporary file extensions mentioned below:

```bash
part,thumbdata3--1967290299,thumbdata3--1763508120,crdownload,~cr,exo,tmp,cvr,download,thumbdata3--number,mxdl,tt2,etl,egt
,csi,thumbdata5--1763508120_0,csd,fseventsd-uuid,localstorage-journal,thumbdata5--1967290299_0,dwl,laccdb,torchdownload,thumbdata5,cache,lck,ewc2,!ut
,regtrans-ms,blf,mmsyscache,sfk,filepart,imgcache,dtapart,sav,aaa,thumbdata,h64,lock,rra,bc
,npk,download,adadownload,hex,tec,chkn,steamstart,partial,thumbdata5--1967290299_1,pnf,idlk,lrd,thumbdata5-1763508120_1,fb!
,temp,waf,tmt,dlm,bu,swo,rcv,reapeaks,dap,pkf,fsf,thumbdata3-1763508120,dmp,db-wal
,pft,little,_501,glh,db-shm,box,cfa,installstate,tv5,tbn,sqlite-journal,dat,thumbdata3-1967290299,onecache
,msj,exd,isl,objectcache,nov,dca,thumbdata4--1967290299,swn,rld,temporaryitems,aso,thumbdata5--1967290299_3,rsc_tmp,bdm
,ptn2,indexarrays,id3tag,thumbdata3,cos2,dia,download,cah,wfm,as$,meb,clp,thumbdata5-1763508120_2,thumbdata4--1763508120
,save,heu,nb2,tof,thumbdata5-1763508120_3,bc!,snapdoc,hrd,rsx,)2(,cache-2,prmdc,bridgecachet,tmd
,fuse_hidden,db3-journal,phc,rdn,ims,cache-3,bsd,thumbdata4,ytf,4sh,tic,hax,buf,init
,cdc,bmc,sqlite3-journal,indexpositions,bts,db,wov,dinfo,indexcompactdirectory,bmb,crc,citriodownload,pkc,pm$
,shadowindexgroups,dtf,peb,bom,oemigaccount,utpart,lai,m_p,md0,bdi,00a,appdownload,inprogress,mbc
,mex,qbi,help,tombstone,csstore,adm,qbt,xp,hmap,@@2,indexdirectory,yumtx,@@1,thumbdata5--1967290299_4
,bridgecache,thumbdata5--1967290299_5,zoner-rawdata-cache,wcc,tst,000,ci,onetmp,indexpositiontable,stf,identcache,qdat,out,inf
,shadowindextermids,adblock,filetablelock,wpk,thumbdata5-1967290299_8,xcuserstate,tv2,aria2,mx1,002,ilp,bv4,par,alt
,nc2,a$v,ddat,cpd,escopy,ipe_tempfile,mpgindex,bv1,tv4,$db,db$,pat,bphys,wa~
,clean,thumbdata5--1967290299_7,^fsf,xps~,sss~,chk,iniis,moz,---,bt0,fts,tv7,wlx,nmu
,swd,dov,bde,~$~,~nt,vsscc,jnk,abc,tv3,thumbdata5-1763508120_6,wsb,dmsk,fes,shadowindexcompactdirectory
,ird,thumbdata5-1763508120_5,qtindex,bv2,svn-work,pzx,$ed,tv1,rad,thumbdata5-1763508120_4,thumbdata5-1763508120_0,$vm,thumbdata5-1763508120_7,compo
,preview7,asab,$$$,pls,pet,001,wtmp,lockfile,ger,tb0,pfc,(d),zoner-index-cache,qp1
,blk,zsr,mtx,wid,ipl22,tv6,vdjcache,xp~,lex,xps,cachedmsg,bv3,f2l,lst
,4sw,wtmp,mov,iff,\#$\#,vmdk-converttmp,bv7,t44,dw3,zl,nav2,bv5,bsi,ccc
,asx,ipl,sdx,u96,dir00,qp2,qtmp,s2mi,fdpart,t$m,hmap.dir,journal,spc,als
,simpl_int,r1m,scuf,dem,patchcache,ers,csac,sfm,thumbdata5-1763508120_8,cnv,vmc,file,s,m
,met,mpx,tv8,zn~,thumbdata5-1763508120_20,cdt,db$,thumbdata5-1763508120_12,ebktml,bv6,tv9,bv8,vaf,thumbnail
,ref,\#\#\#,pspcache,c1s,muf,onlineresources,memb,w44,§§§,dir,lvl,bcm,$a,bv9
,fchc,rgt,ncch,grbdropfile,wrk,cached_icon,thumbdata5-1763508120_17,aecache,mdccache,thumbdata5-1763508120_19,lref,1,0
```

### If a file has a file extension which is in the exempted list above, can I include that file in the sync set?

Yes. In the `~/Library/Application Support/Alfresco/AlfrescoSync.conf` file, find the Sync constraints section, and update the `syncmanager.constraint.1=FileExt|.tmp,.temp` property.

### How are files with an unknown or no extension handled?

When a file is renamed in Alfresco Content Services to either an unknown extension (such as `.aaa`) or to remove the extension, it may not open on your computer. Since the file extension is used to associate programs with files, rename the file to a known extension to fix the file association so you can open the file.

### What files should be backed up/restored on the client?

You'll find the synced data in the `<userHome>/Alfresco` folder. The sync client settings/database/logs are in the `~/Library/Application Support/Alfresco` folder.

When the sync client starts up, it uses the modification time stamp from the `AlfrescoSync.time` file in the `/Application Support/Alfresco` folder to check if any files/folders were changed while Desktop Sync wasn't running. If you delete and recreate the `AlfrescoSync.time` file after restoring the Desktop Sync data and settings, it'll do a full scan of the local and remote folders.

### I have a new computer, is it possible to migrate my Alfresco sync folder to the new computer?

To avoid problems with conflicts on device registration, and content going out of sync during the migration process, you should first remove your account from the deprecated computer and then setup Alfresco Desktop Sync on the new machine.

{% endcapture %}

{% include tabs.html tableid="faq" opt1="Windows" content1=windows opt2="Mac" content2=mac %}
---
title: Manage the properties for content
---

The following sections describe how to manage properties for your content on Windows and Mac.

{% capture windows %}

You can view, edit, and update file and folder properties (i.e. metadata) from the Windows Explorer menu actions.

By default, you can view and edit general properties, such as Title, Name, Description, and Author (if you have the correct permissions).

1. In your **Alfresco** synced folder, find the file or folder that you want to update.

2. Right-click the item and select **Properties**.

    A window appears displaying a number of properties. For example:

    ![]({% link desktop-sync/images/ds-properties-view-win-1.17.png %}){:height="491px" width="673px"}

    By default, the properties are read-only.

3. Click **Edit** to start editing the content.

    Note that the **Edit** button changes to **Save** (if you have edit permissions on the selected content).

4. In the **General properties** tab, you may see a **Custom Type** field. When custom types have been defined in the Desktop Sync configuration file by your IT team, you'll see them listed in this field.

    * To change the content type, select one from the available options, and then click **Apply**.

        Once you apply the change, a new tab appears with the name of the selected custom type.

    * Click **Edit** to start editing the content.

        > **Note:** If a custom type has already been applied to a synced file that's synced from the repository, and it has no sub-types (i.e. children), then you won't be able to change the type.

5. Click **Save** to update the content.

    New changes are shown in the properties panel for Share or Digital Workspace.

    >**Note:**
    >
    >* The **Edit** button is not available in the following cases:
    >    * If a file is declared as a record. See [Governance Services]({% link desktop-sync/latest/using/ags.md %}) for more.
    >    * If your role is set to Consumer or Collaborator on files. See [Permissions]({% link desktop-sync/latest/using/permissions.md %}) for more.
    >* There are validation checks for all fields.
    >    * For example, if a property is incorrectly left blank when you click **Save**, a red background appears indicating that there's a problem. Correct the content to fix the problem.

### Bulk editing of properties

You can also edit properties (i.e. metadata) in multiple files simultaneously. The steps are similar to what's described earlier.

1. Select multiple files, right-click and select **Properties**.
   * This shows the common properties between all of the selected files.
2. You can now view and edit those common properties.

   For example, if you edit the `Title` field, that title will be updated in all of the selected files.

{% endcapture %}

{% capture mac %}

You can view, edit, and update file and folder properties from the Mac Finder menu actions.

By default, you can view and edit general properties, such as Title, Name, Description, and Author (if you have the correct permissions). If enabled by your IT team, you may be able to view and edit additional properties.

1. In your **Alfresco** synced folder, find the file or folder that you want to update.

2. Right-click the item and select **Properties**.

    A window appears displaying a number of properties. For example:

    ![]({% link desktop-sync/images/ds-properties-view-mac2-1.17.png %}){:height="378px" width="690px"}

    By default, the properties are read-only.

3. Click **Edit** to start editing the content.

    Note that the **Edit** button changes to **Save** (if you have edit permissions on the selected content).

4. In the **General properties** tab, you may see a **Custom Type** field. When custom types have been defined in the Desktop Sync configuration file by your IT team, you'll see them listed in this field.

    1. To change the content type, select one from the available options, and then click **Apply**.

        Once you apply the change, a new tab appears with the name of the selected custom type.

    2. Click **Edit** to start editing the content.

        > **Note:** If a custom type has already been applied to a synced file that's synced from the repository, and it has no sub-types (i.e. children), then you won't be able to change the type.

5. Click **Save** to update the content.

    New changes are shown in the properties panel for Share or Digital Workspace.

    >**Note:**
    >
    >* The **Edit** button is not available in the following cases:
    >    * If a file is declared as a record. See [Governance Services]({% link desktop-sync/latest/using/ags.md %}) for more.
    >    * If your role is set to Consumer or Collaborator on files. See [Permissions]({% link desktop-sync/latest/using/permissions.md %}) for more.
    >* There are validation checks for all fields.
    >    * For example, if a property is incorrectly left blank when you click **Save**, a red background appears indicating that there's a problem. Correct the content to fix the problem.

### Bulk editing of properties

You can also edit properties in multiple files simultaneously. The steps are similar to what's described earlier.

1. Select multiple files, right-click and select **Properties**.
   * This shows the common properties between all of the selected files.
2. You can now view and edit those common properties.

   For example, if you edit the `Title` field, that title will be updated in all of the selected files.

{% endcapture %}

{% include tabs.html tableid="metadata" opt1="Windows" content1=windows opt2="Mac" content2=mac %}
---
title: Manage content permissions
---

Alfresco Content Services permissions are replicated on the desktop for files and folders that have been synchronized, ensuring that users are not able to edit files offline as well as on the server.

A role, as set in Alfresco, will determine what you can do to the files and folders. Each role in Alfresco has a default set of permissions. See [User roles and permissions]({% link content-services/latest/using/permissions.md %}) for more information about roles.

The roles are replicated on the desktop as follows:

|Role|Role Definition|Permissions|
|----|---------------|-----------|
|Manager|Full rights to all content|Managers will be able to create, edit, and delete files and folders that are synchronized where the Manager role is set - (*) **see note below**.|
|Collaborator|Full rights to content that they own; can edit but not delete content created by other users|Collaborators will be able to create new files/folders, edit, move, rename, and delete their own files/folders, edit other users content, but won't be able to rename/move/delete files/folders created by someone else - (*) **see note below**. They will be able to check-out/declare as record any file.|
|Contributor|Full rights to content that they own, but cannot edit or delete content created by other users|Contributors will be able to create new files/folders, edit, move, rename, and delete their own files/folders, but not files/folders created by someone else. Contributors won't be able to check-out/declare as record files created by other users. They will be able to check-out/declare records for their own files.|
|Consumer|View-only rights; cannot create content|Files and folders with the Consumer role will be set to read-only on the desktop.|

>**Important:** (*) Mac OS X and Windows don't have the same permissions granularity that Alfresco Content Services provides, so users will experience limitations on their desktops.
>The most notable differences are:
>
>* Specific permissions applied to a file that override the inherited permission from the folder. For example, a Consumer that's given Manager permissions on a file won't be able to rename, move, or delete the file.
>* Collaborators are only able to edit content that other users have created. Other actions, like rename or move are not permitted.

>**Note:** Role changes on content will synchronize from the server to the desktop.

>**Note:** Attempts to override locally set permissions are immediately reset, even when not connected to the server.
---
title: Select content to sync
---

Once you've set up Desktop Sync, all your Alfresco Content Services folders will be displayed from My Files, Shared Files, and your Sites.

{% capture windows %}

Once you've set up Desktop Sync, all your Alfresco Content Services folders are displayed from My Files, Shared Files, and My Sites.

Use the *Select sites and folders to sync* screen to select the content to sync between Alfresco Content Services and your desktop. The content is synced at `C:\Users\<username>\Alfresco`.

If you work with content that has deep folder structures, you may wish to deselect the **Include all files and sub-folders** checkbox. This allows you to only sync selected folders deep in your hierarchy, without syncing the intermediate folders, and prevent lengthy folder paths being created. By default, this feature is enabled, and if you want to sync only particular folders then the checkbox has to be deselected. In this case, only the files in the selected folders are synced using a folder structure starting from their respective root paths in Content Services (such as My Files, Shared Files, and your Sites).

Here’s an example that shows how the folder paths may be shortened:

* `My Files` > `<selected-sync-folder>`
* `Sites` > `<Site Name>` > `<selected-sync-folder>`
* `Shared Files` > `<selected-sync-folder>`

When the checkbox is selected (since it's enabled by default), the folders are synced using the hierarchy in Content Services. This replicates the behavior from previous releases of Desktop Sync.

> **Note:** The screen provides an estimate of how much disk space will be occupied, so only select the content you need. The more content you select, the more space will be taken on your local machine and the more time it will take to perform the initial sync.

1. Synchronize your content from **My Files** and **Shared Files**.

    ![Initial sync selection screen]({% link desktop-sync/images/setup-1.17.png %}){:height="555px" width="346px"}

    1. Select **My Files** to expand the folder list in your **My Files** area of Alfresco Content Services.

        You can navigate through the folder hierarchy and click the check box to select individual folders, or select ![]({% link desktop-sync/images/ico-ds-sync-fav.png %}) **My Files** to sync everything. See [My Files]({% link content-services/latest/using/content/index.md %}#my-files) for more.

    2. Select **Shared Files** to sync all the files and folders under **Shared Files** in Alfresco.

        You can navigate through the folder hierarchy and click the check box to select individual folders, or select ![]({% link desktop-sync/images/ico-ds-sync-fav.png %}) **Shared Files** to sync everything. See [Shared Files]({% link content-services/latest/using/content/index.md %}#shared-files) for more.

2. Select ![]({% link desktop-sync/images/ico-ds-sync-fav.png %}) next to **Favorite Sites** to sync all your favorite sites.

    To select specific sites, click ![]({% link desktop-sync/images/ds-expand.png %}) to expand the list and select the relevant site.

    To sync a specific folder within a site, double-click the site name and select the folder.

3. Select ![]({% link desktop-sync/images/ico-ds-sync-fav.png %}) next to **Favorite Folders** to sync all your favorite folders.

    To sync specific folders, click ![]({% link desktop-sync/images/ds-expand.png %}) to expand the list, double-click the site name and select the relevant folder.

    When you expand **Favorite Folders**, all the favorite folders for a site are grouped under that site.

4. Under **My Sites**, you'll see all the sites you're a member of.

    To sync specific folders, click ![]({% link desktop-sync/images/ds-expand.png %}) to expand the list, double-click the site name and select the relevant folder.

    > **Note:** Sites display their full name and folders display the hierarchy of the folder, for example, **My Site \| My Folder**.

5. Under **Company Home**, you'll see all the folders created by the Administrator under Company Home of Alfresco repository.

6. Click **Sync** to start initial syncing of the selected Alfresco files and folders to your desktop.

    > **Tip:** You can click **Cancel** to cancel the sync and close the Select sites and folders to sync screen.

    > **Note:** During the initial sync, don't disconnect your computer from the network or put your computer to sleep. Although the sync will resume if interrupted, it will likely need to check the content again and very large initial syncs may take a long time to complete.

7. In the **Alfresco sync folder location** dialog, choose where the sync folder is stored.

    The content is synced to `C:\Users\<username>\Alfresco` by default.

    1. To use the default location and start the sync, click **OK**.

    2. To change the sync location, select **Browse…**, choose a new location, click **Select Folder**, and then click **OK** to start the sync.

    > **Note:** If you wish to move the Alfresco sync folder location later, you'll have to remove your account and set up Desktop Sync again.

    > **Note:** The sync folder location must be set to a local folder as network folders aren't supported.

### About the initial sync {#init-sync-win}

The **Sync** progress screen shows the status of initial sync. The Alfresco icon ![]({% link desktop-sync/images/ds-spin.png %})in the system tray will spin during the sync process. On completion, a notification appears on the system tray.

![]({% link desktop-sync/images/initialsync-1.12.png %}){:height="160px" width="469px"}

In C`:\Users\<username>\Alfresco`, copies of all the content you've selected to sync are created. Desktop Sync automatically keeps both the local copy and the Alfresco versions in sync with each other whenever any changes are made.

![]({% link desktop-sync/images/sync.png %})

During initial sync:

* You can **Return to content selection** to change the content selected for synchronization. Note that after making changes, your sync will restart from the beginning.
* If you create a new file or update a file on your desktop, it will be synced only after the initial sync is over.
* It's recommended that you don't move the parent folders being synced.

### Working with content

To save your work in Alfresco, just work on your files in the `C:\Users\<username>\Alfresco` folder, and everything in the folder will be automatically synced to Alfresco.

{% endcapture %}

{% capture mac %}

Use the *Select sites and folders to sync* dialog to select the content to sync between Alfresco Content Services and your desktop. The content is synced to your `/<userHome>/Alfresco` folder, located in Finder under **Go > Home**.

If you work with content that has deep folder structures, you may wish to deselect the **Include all files and sub-folders** checkbox. This allows you to only sync selected folders deep in your hierarchy, without syncing the intermediate folders, and prevent lengthy folder paths being created. By default, this feature is enabled, and if you want to sync only particular folders then the checkbox has to be deselected. In this case, only the files in the selected folders are synced using a folder structure starting from their respective root paths in Content Services (such as My Files, Shared Files, and your Sites).

Here’s an example that shows how the folder paths may be shortened:

* `My Files` > `<selected-sync-folder>`
* `Sites` > `<Site Name>` > `<selected-sync-folder>`
* `Shared Files` > `<selected-sync-folder>`

When the checkbox is selected (since it's enabled by default), the folders are synced using the hierarchy in Content Services. This replicates the behavior from previous releases of Desktop Sync.

> **Note:** The screen provides an estimate of how much disk space will be occupied, so only select the content you need. The more content you select, the more space will be taken on your computer and the more time it'll take to perform the initial sync.

1. Synchronize your content from **My Files** and **Shared Files**.

    ![Initial sync selection screen]({% link desktop-sync/images/setup-mac-1.9.png %}){:height="382px" width="640px"}

    1. Select **My Files** to expand the folder list in your **My Files** area of Alfresco Content Services.

        You can navigate through the folder hierarchy and click the check box to select individual folders, or select ![]({% link desktop-sync/images/ico-ds-sync-fav.png %})**My Files** to sync everything. See [My Files]({% link content-services/latest/using/content/index.md %}#my-files) for more.

    2. Select **Shared Files** to expand the folder list in your **Shared Files** area of Alfresco Content Services.

        You can navigate through the folder hierarchy and click the check box to select individual folders, or select ![]({% link desktop-sync/images/ico-ds-sync-fav.png %})**Shared Files** to sync everything. See [Shared Files]({% link content-services/latest/using/content/index.md %}#shared-files) for more.

2. Select **Sites** to expand the list of sites you are a member of in Alfresco Content Services, sites you have favorited, and sites with content that you have favorited.

    ![]({% link desktop-sync/images/sites-favorites-mac.png %}){:height="327px" width="640px"}

    * ![]({% link desktop-sync/images/site-fav-mac.png %}) indicates a favorite site or folder
    * ![]({% link desktop-sync/images/folder-fav-mac.png %}) indicates a site or folder that contains favorited content

    These are listed in alphabetical order, grouped by favorites, then sites with favorited content, and then other sites you're a member of.

    * Select **Sites** to expand the folder list in your **Sites** area of Alfresco Content Services.

       You can navigate through the folder hierarchy and click the check box to select individual folders.

    * Select **Company Home** to expand the folder list in your **Company Home** area of Alfresco Content Services (if set up by your IT team).

       You can navigate through the folder hierarchy and click the check box to select individual folders.

       > **Note:** It's not possible to select all your **Sites** or all of **Company Home** as it's likely to involve a large sync and may take a long time.

3. Click **Sync** to start initial syncing of the selected files and folders to your desktop.

    > **Tip:** You can click **Cancel** to cancel selecting content and close the Select sites and folders to sync dialog.

    > **Note:** During the initial sync, don't disconnect your computer from the network or put your computer to sleep. Although the sync will resume if interrupted, it's likely to need to check the content again, and very large initial syncs may take a long time to complete.

4. In the **Alfresco sync folder location** dialog, choose where the sync folder is stored.

    The content is synced to `<userHome>/Alfresco` by default.

    1. To use the default location and start the sync, click **OK**.

    2. To change the sync location, select **Browse…**, choose a new location, click **Select Folder**, and then click **OK** to start the sync.

    > **Note:** If you wish to move the Alfresco sync folder location later, you'll have to remove your account and set up Desktop Sync again.

    > **Note:** The sync folder location must be set to a local folder as network folders aren't supported.

### About the initial sync {#init-sync-mac}

The **Sync** progress dialog shows the status of the initial sync. The Alfresco icon in the menu bar changes to indicate that the sync is in progress ![]({% link desktop-sync/images/ds-syncing-mac.png %}){:height="23px" width="23px"}. Once the sync has completed successfully, the icon changes to ![]({% link desktop-sync/images/ds-synced-mac.png %}){:height="23px" width="23px"}.

![]({% link desktop-sync/images/initialsync-mac-1.17.png %}){:height="221px" width="469px"}

In `/<userHome>/Alfresco`, copies of all the content you've selected to sync are created. Desktop Sync automatically keeps both the local copy and the Alfresco Content Services versions in sync with each other whenever any changes are made.

![]({% link desktop-sync/images/sync-mac.png %}){:height="351px" width="747px"}

During initial sync:

* You can close the sync progress dialog using the red cross, and the initial sync will continue in the background which allows you to continue working elsewhere.
* You can **Return to content selection** to change the content selected for synchronization. Note that after making changes, your sync will restart from the beginning.
* If you create a new file or update a file on your desktop, it'll be synced after the initial sync is over.
* It's recommended that you don't move folders until the initial sync has completed.

### Working with content

To save your work in Alfresco, just work on your files in the `/<userHome>/Alfresco` folder, and everything in the folder will be automatically synced to Alfresco.

{% endcapture %}

{% include tabs.html tableid="sync" opt1="Windows" content1=windows opt2="Mac" content2=mac %}
---
title: Sharing files
---

You can easily share a file from the Explorer or Finder menu actions. Clicking the **Share** action generates a URL that you can send by email. People with access to the URL can view the file.

{% capture windows %}

Make sure that you've [configured file sharing]({% link desktop-sync/latest/config/index.md %}#sharing-files) before continuing.

1. In your **Alfresco** synced folder find the file you want to share.

    You can only share files, not folders.

2. Right-click the file and select **Share**.

    A window appears displaying that link sharing is enabled (**Link sharing on**), the URL for this file, and no expiry date is set.

    ![]({% link desktop-sync/images/ds-share-file-1.17.png %}){:height="190px" width="360px"}

    > **Note:** If a file is record, link sharing is not allowed. If a file is read-only, the file can be shared but you can't set an expiry date. However, if a read-only file was previously shared and had an expiry date, the date is displayed but can't be changed (i.e. the field is read-only).

3. Click the copy ![Copy]({% link desktop-sync/images/ds-ico-copy.png %}){:height="21px" width="21px"} icon to copy the link.

    You can paste it wherever you like, such as an email or document. Here's a preview of the shared file in Alfresco Share:

    ![]({% link desktop-sync/images/ds-share-preview.png %}){:height="255px" width="480px"}

4. (Optional): To set an expiry date for the shared link, first click the **Calendar** icon and then set the required date.

    To remove an expiry date, remove the tick from the **Set expiry date** check box.

5. Click **Close**.

    When you don't want the shared file to be available anymore, you can break the link. Once you make the link invalid, anyone who tries to access it will be unable to reach the page.

6. Right-click the shared file and select **Share**.

7. Click the link sharing switch (i.e. set **Link sharing off**) to break the link.

    A notification appears stating that the shared link will be deleted.

8. Click **Remove** to complete the action.

    > **Note:** When the file is shared again, a new link is generated.

{% endcapture %}

{% capture mac %}

Make sure that you've [configured file sharing]({% link desktop-sync/latest/config/index.md %}#sharing-files) before continuing.

1. In your **Alfresco** synced folder find the file you want to share.

    You can only share files, not folders.

2. Right-click the file and select **Share**.

    A window appears displaying that link sharing is enabled (**Link sharing on**), the URL for this file, and no expiry date is set.

    ![]({% link desktop-sync/images/ds-share-file-mac-1.17.png %}){:height="202px" width="400px"}

    > **Note:** If a file is record, link sharing is not allowed. If a file is read-only, the file can be shared but you can't set an expiry date. However, if a read-only file was previously shared and had an expiry date, the date is displayed but can't be changed (i.e. the field is read-only).

3. Click the copy ![Copy]({% link desktop-sync/images/ds-ico-copy.png %}){:height="21px" width="21px"} icon to copy the link.

    You can paste it wherever you like, such as an email or document. Here's a preview of the shared file in Alfresco Digital Workspace:

    ![]({% link desktop-sync/images/ds-shared-file-adw.png %}){:height="277px" width="562px"}

4. (Optional): To set an expiry date for the shared link, first tick the **Set expiry date** check box, and then adjust the date using the up and down arrows.

    To remove an expiry date, remove the tick from the **Set expiry date** check box.

5. Click **Close**.

    When you don't want the shared file to be available anymore, you can break the link. Once you make the link invalid, anyone who tries to access it will be unable to reach the page.

6. Right-click the shared file and select **Share**.

7. Click the link sharing switch (i.e. set **Link sharing off**) to break the link.

    A notification appears stating that the shared link will be deleted.

8. Click **Remove** to complete the action.

    > **Note:** When the file is shared again, a new link is generated.

{% endcapture %}

{% include tabs.html tableid="sharing" opt1="Windows" content1=windows opt2="Mac" content2=mac %}
---
title: Resolve and manage sync conflicts 
---

Use the following information to resolve and manage Desktop Sync conflicts.

Whilst Desktop Sync ensures that content is kept up to date silently, under normal operation there may be circumstances where Desktop Sync can't resolve differences between a file stored on your desktop and the corresponding file in Alfresco.

When the sync changes can't be updated automatically you are asked to resolve the conflict manually. This happens when a file has changed in both locations since its last sync, making it difficult to determine which changes to save.

For example, a conflict occurs when you update a file in your `Alfresco` sync folder and an update to the same file has happened on the server since the last sync. Desktop Sync will give you a choice of resolving the sync conflict by either choosing to keep your changes, or discarding your changes in favor of the latest copy from Alfresco.

{% capture windows %}

A conflict may either be resolved automatically by Desktop Sync or may require you to do something.

![]({% link desktop-sync/images/conflict-resolution-1.17.png %}){:height="500px" width="351px"}

### User action needed

|Alfresco action|Desktop Sync action|Result|Resolution|
|---------------|-------------------|------|----------|
|Update|Update|![]({% link desktop-sync/images/cross.png %})|Select either the desktop version or the Alfresco version. If you select the desktop version, that version is uploaded in Alfresco. If you select the Alfresco version, that version is applied on the desktop. [Open]({% link desktop-sync/latest/using/app-menu.md %}#open-menu-item) the conflicts and pending syncs dialog for information on resolving the conflict.|
|Rename|Rename|![]({% link desktop-sync/images/cross.png %})|Select either the desktop version rename or the Alfresco version rename.If you select the desktop renamed file, the Alfresco version rename is discarded. If you select the Alfresco renamed file, the desktop version rename is discarded. [Open]({% link desktop-sync/latest/using/app-menu.md %}#open-menu-item) the conflicts and pending syncs dialog for information on resolving the conflict.|
|Move|Move|![]({% link desktop-sync/images/cross.png %})|Select either the desktop action or the Alfresco action.If you select the desktop move, the Alfresco move of the file is cancelled and the desktop move is replicated in Alfresco. If you select the Alfresco move, desktop move of the file is cancelled and the Alfresco move is replicated on your desktop. [Open]({% link desktop-sync/latest/using/app-menu.md %}#open-menu-item) the conflicts and pending syncs dialog for information on resolving the conflict.|
|Delete|Update|![]({% link desktop-sync/images/cross.png %})|Select either the desktop update action or the Alfresco delete action. If you select the desktop action, the updated desktop file is restored in Alfresco. If you select the Alfresco delete action, the file on your desktop is deleted and the update is discarded. [Open]({% link desktop-sync/latest/using/app-menu.md %}#open-menu-item) the conflicts and pending syncs dialog for information on resolving the conflict.|
|Delete|Rename|![]({% link desktop-sync/images/cross.png %})|Select either the desktop rename action or the Alfresco delete action. If you select the desktop action, the desktop renamed file is restored in Alfresco with the new name. If you select the Alfresco delete action, the file on your desktop is deleted and rename is discarded. [Open]({% link desktop-sync/latest/using/app-menu.md %}#open-menu-item) the conflicts and pending syncs dialog for information on resolving the conflict.|
|Delete|Move|![]({% link desktop-sync/images/cross.png %})|Select either the desktop move action or the Alfresco delete action. If you select the desktop action, the file is recreated on your desktop at the new location. If you select the Alfresco delete action, the file is deleted from its new location on your desktop. [Open]({% link desktop-sync/latest/using/app-menu.md %}#open-menu-item)  the conflicts and pending syncs dialog for information on resolving the conflict.|

where ![]({% link desktop-sync/images/cross.png %}) indicates a conflict.

### No user action needed

|Alfresco action|Desktop Sync action|Result|Resolution|
|---------------|-------------------|------|----------|
|Update|Rename|![]({% link desktop-sync/images/tick.png %})|File is renamed and updated|
|Update|Move|![]({% link desktop-sync/images/tick.png %})|File is moved and updated|
|Update|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File not deleted as it was updated in Alfresco.Conflict is resolved by restoring the Alfresco version to your desktop.|
|Update|Delete parent|![]({% link desktop-sync/images/tick.png %})|Parent file not deleted as it was updated in Alfresco.Conflict is resolved by restoring the Alfresco version of the parent file to your desktop.|
|Rename|Update|![]({% link desktop-sync/images/tick.png %})|File is renamed and updated|
|Rename|Move|![]({% link desktop-sync/images/tick.png %})|File is moved and updated|
|Rename|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File not deleted as it was updated in Alfresco.Conflict is resolved by restoring Alfresco version to your desktop.|
|Rename|Delete parent|![]({% link desktop-sync/images/tick.png %})|Parent file not deleted as it was updated in Alfresco.Conflict is resolved by restoring the Alfresco version of the parent file to your desktop.|
|Move|Update|![]({% link desktop-sync/images/tick.png %})|File is moved and updated|
|Move|Rename|![]({% link desktop-sync/images/tick.png %})|File is renamed and moved|
|Move|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File not deleted as it was updated in Alfresco.Conflict is resolved by restoring the file in a new location on your desktop.|
|Move|Delete parent|![]({% link desktop-sync/images/tick.png %})|Parent file not deleted as it was updated in Alfresco.Conflict is resolved by restoring the parent file in a new location on your desktop.|
|Move out of synced site|Update|![]({% link desktop-sync/images/tick.png %})|File moved to a new location in Alfresco. On your desktop, the file is moved to `C:\Users\<username>\Alfresco\orphaned` as it can't be saved in Alfresco.|
|Move out of synced site|Rename|![]({% link desktop-sync/images/tick.png %})|File moved to a new location in Alfresco. On your desktop, the file is moved to `C:\Users\<username>\Alfresco\orphaned` as it can't be saved in Alfresco.|
|Move out of synced site|Move|![]({% link desktop-sync/images/tick.png %})|File moved to a new location in Alfresco. On your desktop, the file is moved to `C:\Users\<username>\Alfresco\orphaned` as it can't be saved in Alfresco.|
|Move out of synced site|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File deleted|
|Move out of synced site|Delete parent|![]({% link desktop-sync/images/tick.png %})|File deleted|
|Delete|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File deleted|
|Delete|Delete parent|![]({% link desktop-sync/images/tick.png %})|File deleted|
|Delete parent|Update|![]({% link desktop-sync/images/tick.png %})|Parent folder is deleted in Alfresco. On your desktop, the file is moved to `C:\Users\<username>\Alfresco\orphaned` as it can't be saved in Alfresco.|
|Delete parent|Rename|![]({% link desktop-sync/images/tick.png %})|Parent folder is deleted in Alfresco. On your desktop, the file is moved to `C:\Users\<username>\Alfresco\orphaned` as it can't be saved in Alfresco.|
|Delete parent|Move|![]({% link desktop-sync/images/tick.png %})|Parent folder is deleted in Alfresco. On your desktop, the file is moved to `C:\Users\<username>\Alfresco\orphaned` as it can't be saved in Alfresco.|
|Delete parent|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File deleted|
|Delete parent|Delete parent|![]({% link desktop-sync/images/tick.png %})|File deleted|

where ![]({% link desktop-sync/images/tick.png %}) indicates no conflict.

{% endcapture %}

{% capture mac %}

A conflict may either be resolved automatically by Desktop Sync or may require you to do something.

![]({% link desktop-sync/images/conflict-resolution-mac-1.17.png %}){:height="414px" width="300px"}

### User action needed

|Alfresco action|Desktop Sync action|Result|Resolution|
|---------------|-------------------|------|----------|
|Update|Update|![]({% link desktop-sync/images/cross.png %})|Select either to keep your update or discard your changes.If you keep your changes, that version is uploaded in Alfresco. If you discard your changes, the Alfresco version is applied on your desktop. See [Check Outs, Conflicts and Pending]({% link desktop-sync/latest/using/app-menu.md %}#faq/mac) for information on resolving the conflict.|
|Rename|Rename|![]({% link desktop-sync/images/cross.png %})|Select either to keep your rename or discard your changes.If you keep your changes, the Alfresco version rename is discarded. If you discard your changes, the Alfresco rename is applied on your desktop. See [Check Outs, Conflicts and Pending]({% link desktop-sync/latest/using/app-menu.md %}#faq/mac) for information on resolving the conflict.|
|Move|Move|![]({% link desktop-sync/images/cross.png %})|Select either to keep your move action or discard your changes. If you keep your changes, the Alfresco move is cancelled, and your desktop move is replicated in Alfresco. If you discard your move, the desktop move is cancelled, and the Alfresco move is replicated on your desktop. See [Check Outs, Conflicts and Pending]({% link desktop-sync/latest/using/app-menu.md %}#faq/mac) for information on resolving the conflict.|
|Delete|Update|![]({% link desktop-sync/images/cross.png %})|Select either to keep your update action or discard your changes. If you keep your changes, the updated file is restored in Alfresco. If you discard your changes, the update is discarded, and the file on your desktop is deleted to reflect the Alfresco delete action. See [Check Outs, Conflicts and Pending]({% link desktop-sync/latest/using/app-menu.md %}#faq/mac) for information on resolving the conflict.|
|Delete|Rename|![]({% link desktop-sync/images/cross.png %})|Select either to keep your rename action or discard your changes. If you keep your changes, the renamed file is restored in Alfresco with the new name. If you discard your changes, the rename is discarded, and the file on your desktop is deleted. See [Check Outs, Conflicts and Pending]({% link desktop-sync/latest/using/app-menu.md %}#faq/mac) for information on resolving the conflict.|
|Delete|Move|![]({% link desktop-sync/images/cross.png %})|Select either to keep your move action or discard your changes. If you keep your changes, the file is recreated on your desktop at the new location. If you discard your changes, the file is deleted from its new location on your desktop. See [Check Outs, Conflicts and Pending]({% link desktop-sync/latest/using/app-menu.md %}#faq/mac) for information on resolving the conflict.|

where ![]({% link desktop-sync/images/cross.png %}) indicates a conflict.

### No user action needed

|Alfresco action|Desktop Sync action|Result|Resolution|
|---------------|-------------------|------|----------|
|Update|Rename|![]({% link desktop-sync/images/tick.png %})|File is renamed and updated|
|Update|Move|![]({% link desktop-sync/images/tick.png %})|File is moved and updated|
|Update|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File not deleted as it was updated in Alfresco.Conflict is resolved by restoring the Alfresco version to your desktop.|
|Update|Delete parent|![]({% link desktop-sync/images/tick.png %})|Parent file not deleted as it was updated in Alfresco.Conflict is resolved by restoring the file from Alfresco to your desktop.|
|Rename|Update|![]({% link desktop-sync/images/tick.png %})|File is renamed and updated|
|Rename|Move|![]({% link desktop-sync/images/tick.png %})|File is moved and updated|
|Rename|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File not deleted as it was updated in Alfresco.Conflict is resolved by restoring the file from Alfresco to your desktop.|
|Rename|Delete parent|![]({% link desktop-sync/images/tick.png %})|Parent file not deleted as it was updated in Alfresco.Conflict is resolved by restoring the file from Alfresco to your desktop.|
|Move|Update|![]({% link desktop-sync/images/tick.png %})|File is moved and updated|
|Move|Rename|![]({% link desktop-sync/images/tick.png %})|File is renamed and moved|
|Move|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File not deleted as it was updated in Alfresco.Conflict is resolved by restoring the file in a new location on your desktop.|
|Move|Delete parent|![]({% link desktop-sync/images/tick.png %})|Parent file not deleted as it was updated in Alfresco.Conflict is resolved by restoring the parent file in a new location on your desktop.|
|Move out of synced site|Update|![]({% link desktop-sync/images/tick.png %})|File moved to a new location in Alfresco. On your desktop, the file is moved to `/<userHome>/Alfresco/orphaned` as it can't be saved in Alfresco.|
|Move out of synced site|Rename|![]({% link desktop-sync/images/tick.png %})|File moved to a new location in Alfresco. On your desktop, the file is moved to `/<userHome>/Alfresco/orphaned` as it can't be saved in Alfresco.|
|Move out of synced site|Move|![]({% link desktop-sync/images/tick.png %})|File moved to a new location in Alfresco. On your desktop, the file is moved to `/<userHome>/Alfresco/orphaned` as it can't be saved in Alfresco.|
|Move out of synced site|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File deleted|
|Move out of synced site|Delete parent|![]({% link desktop-sync/images/tick.png %})|File deleted|
|Delete|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File deleted|
|Delete|Delete parent|![]({% link desktop-sync/images/tick.png %})|File deleted|
|Delete parent|Update|![]({% link desktop-sync/images/tick.png %})|Parent folder is deleted in Alfresco. On your desktop, the file is moved to `/<userHome>/Alfresco/orphaned` as it can't be saved in Alfresco.|
|Delete parent|Rename|![]({% link desktop-sync/images/tick.png %})|Parent folder is deleted in Alfresco. On your desktop, the file is moved to `/<userHome>/Alfresco/orphaned` as it can't be saved in Alfresco.|
|Delete parent|Move|![]({% link desktop-sync/images/tick.png %})|Parent folder is deleted in Alfresco. On your desktop, the file is moved to `/<userHome>/Alfresco/orphaned` as it can't be saved in Alfresco.|
|Delete parent|Delete/Move out of synced site|![]({% link desktop-sync/images/tick.png %})|File deleted|
|Delete parent|Delete parent|![]({% link desktop-sync/images/tick.png %})|File deleted|

where ![]({% link desktop-sync/images/tick.png %}) indicates no conflict.

{% endcapture %}

{% include tabs.html tableid="conflicts" opt1="Windows" content1=windows opt2="Mac" content2=mac %}
---
title: Manage the version history
---

You can view and manage the version history from the Windows Explorer/Mac Finder menu actions.

1. In your **Alfresco** synced folder, find the file that you want to update.

2. Right-click the item and select **Version History**.

    A window appears displaying the version history with a number of available actions. The latest version of the file is shown at the top of the left panel, with older versions listed below it (if available).

    For example on Windows:

    ![]({% link desktop-sync/images/ds-history.png %}){:height="361px" width="498px"}

    For example on Mac:

    ![]({% link desktop-sync/images/ds-history-mac.png %}){:height="371px" width="684px"}

3. Click **Download** to download the selected version to your **Downloads** folder.

    The file name is saved using format `<filename>-<version.number>.<ext>`.

4. Click **Revert** to revert the content to the version selected in the left panel.

    A new minor version is created based on the selected version.

5. Click **Delete** to remove the selected version.

    New changes are shown in the properties panel for Share or Digital Workspace.

    >**Note:**
    >
    > * The default download location isn't changeable.
    > * You'll see a notification when reverting and deleting a version.
