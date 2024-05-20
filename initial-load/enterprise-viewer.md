---
title: Alfresco Enterprise Viewer
---

Alfresco Enterprise Viewer (AEV), formerly OpenAnnotate,  provides high-speed and secure viewing of document, video and audio content with team collaborative annotation, redaction and other modern document capabilities for Alfresco Content Services (ACS). It features collaboration and lightweight PDF editing features.

Enterprise Viewer can be used as a standalone viewer or within applications such as the Alfresco Content Accelerator.

Enterprise Viewer is configured out of the box to allow Annotations on documents that have either their native content or a rendition in the following formats:

* PDF
* JPEG
* GIF
* PNG
* MP3
* MP4

If the documents in your repository are already available in one of the above formats, then you are all set to go! If your documents are not available in one of the above formats, it is easy to write a transformer that will render your documents into one of the above formats. The most common example of this is to configure all `.doc` or `.docx` files to be rendered into a `.pdf` when they are checked into the repository.
---
title: Configure AEV actions and modes
---

To modify what actions and modes appear in the Alfresco Enterprise Viewer, certain properties can be edited in the `openannotate-override-placeholders.properties` file. This file would have been deployed to the Tomcat classpath as a part of the install process. Note that in order for changes to this file to take effect, the Tomcat will need to be restarted after the changes are made.  

Some important configuration features to point out when configuring AEV:

1. You can configure what buttons (actions) should appear in each mode individually, as well as the order they appear in the toolbar.
2. You can add Action types to whitelist, rather than listing each button individually.
3. You can configure where actions appear and what they look like.

Below is a list of the properties you can override in the `openannotate-override-placeholders.properties` to change the actions and modes that appear in each AEV mode:

* enabledAnnotationActions
* enabledRedactionActions
* enabledIndexerActions
* enabledEditActions
* enabledPageSelectActions
* enabledSignatureActions
* enabledOpenViewerActions
* enabledOpenViewerWithTextActions

Additional detail about each of these properties and their default values are listed in the next section.

## Redaction types and security

There are three types of redaction that you can configure:

* `redactInPlace` makes the redactions directly on the document being redacted.
* `redactedAsCopy` makes a copy of the document being redacted, and makes the redactions on the copy, so the original document is not be modified.
* `unredactedAsCopy` makes a copy of the document being redacted, and make the redactions on the original document, so the copy doesn't include the redactions.

### Set up security for redacted/unredacted files

To lock a version (redacted or unredacted) to a particular security level, you can create a new Alfresco Behavior to run once the redactions occur. You may implement the `org.alfresco.repo.node.NodeServicePolicies` interface and use the method `OnUpdatePropertiesPolicy` to write custom logic to secure the redacted/unredacted document appropriately.

Below is a sample code snippet showing custom logic written to set stricter permission to the UNREDACTED version of a document. In this example:

* The behavior code is written for the scenario where the `redactionType` is set to `unredactedAsCopy`. This secures the unredacted copy of the document to limit access more strictly.
* The `nodeRef` mentioned in this example is the unredacted copy of the original document.

```java
public void onUpdateProperties(final NodeRef nodeRef, final Map<QName, Serializable> before, final Map<QName, Serializable> after) {
    logger.debug("Starting UnredactedPermissionsBehavior.onUpdateProperties");
    
    // STEP 1: Add "-UNREDACTED" to cm_title of the copy document
    NodeService nodeService = serviceRegistry.getNodeService();
    QName titleProp = QName.createQName(NamespaceService.CONTENT_MODEL_1_0_URI, TITLE_NAME);
    Serializable currentTitle = nodeService.getProperty(nodeRef, titleProp);
    currentTitle = (StringUtils.contains(currentTitle.toString(), "-UNREDACTED") ? currentTitle : currentTitle + "-UNREDACTED");
    nodeService.setProperty(nodeRef, titleProp, currentTitle);
    
    AuthenticationUtil.runAs(new AuthenticationUtil.RunAsWork<Boolean>(){
        public Boolean doWork() {		
            PermissionService permissionService = serviceRegistry.getPermissionService();
            
            // STEP 2: clear out any permissions the copy document may be inheriting from its parent
            boolean inheritTrue = permissionService.getInheritParentPermissions(nodeRef);
            if(inheritTrue) {
                permissionService.setInheritParentPermissions(nodeRef, false);
            }
            
            // STEP 3: loop through the property names that are keys on the propertyMap...
            // the propertyMap in this example is a 2 level map(Map<String, Map<String, String>>), it maps a property name to another map
            // the second Map maps a property value to the list of groups that that property value corresponds to
            // We recommend injecting this map into this new behavior class via spring bean injection 
            for (String prop : propertyMap.keySet()) {
                // the "prop" here is the oc_name for a particular property (ex: hy_documentTypeCode)
                // We use that prop to get the second level map (aka propertyValueMap) based on that "prop"
                Map<String, List<String>> propertyValueMap = propertyMap.get(prop);
                
                // We then get QName of property
                QName propName = getPropertyQName(prop);

                // Make sure our injected map was configured correctly and that we were able to locate the property we are currently looping on
                if (propName != null) {

                    // At this point, we've located the property...
                    // Since this behavior runs on update, check if the property value changed on this doc as a part of this update
                    if (AlfrescoEmbUtil.propertyChanged(propName, before, after)) {
                        if (propertyValueMap.get((String)before.get(propName)) != null) {

                            // STEP 5: If the property value changed, let's clear out the permissions related to the old value of the property 
                            // since the permissions will now be based on the new property value 
                            List<String> prevGroups = propertyValueMap.get((String)before.get(propName));
                            for (String groupName : prevGroups) {
                                permissionService.clearPermission(nodeRef, groupName);
                            }
                        }
                    }

                    // STEP 6: Get the current value of the property we are looping on 
                    // and check if that value is in our propertyValueMap (meaning we have a permissions value in the map we can set for it)
                    if (propertyValueMap.get((String)after.get(propName)) != null) {
                        // STEP 7: If we found that property value in the map, lets set permissions for the new groups
                        // after we get the value of the groups from the map 
                        List<String> newGroups = propertyValueMap.get((String)after.get(propName));

                        // for each group, set the permissions on the doc
                        for (String groupName : newGroups) {
                            permissionService.setPermission(nodeRef, groupName, PermissionService.CONSUMER, true);
                        }
                    }	
                } else {
                    // if the property doesn't exist will log an error and continue
                    logger.error("UnredactedPermissionsBehavior: Unable to set permissions - property does not exist: " + prop);
                }
            } 
            return true;
        }
    }, AuthenticationUtil.getSystemUserName());

    logger.debug("Finishing UnredactedPermissionsBehavior.onUpdateProperties");
}
```

## Default AEV enabled actions

The following dives into each of these properties and documents the default values for the AEV actions enabled in each mode.

### enabledAnnotationActions

The Actions enabled in annotation mode.

Default value:

```text
(t:Navigation),(prevPage,nextPage, zoomIn,zoomOut,--isSmallScreen),
(t:Mode),(t:PageEntry),d(checkinOfflineAnnotatedPdf,annotatedPdf,nativeContentDownload,extractPdfPages,offlineAnnotatedPdf,printAnnotatedPdf,
printSectionsAction,--dropdownLabel-Downloads,--dropdownIcon-save_alt),(t:AnnotationManipulation),
(t:Misc),d(t:Text,--dropdownLabel-Text Annotations,--dropdownIcon-font_download,--dropdownShowSelected),
d(drawLine,drawArrow,drawEllipse,drawRectangle,drawBox,textbox,freeDraw,--dropdownLabel-Drawing Tools,--dropdownIcon-edit,--dropdownShowSelected),
d(approvedStamp,paidStamp,reviewedStamp,acceptStamp,rejectStamp,pageSizedCheckmarkStamp,--dropdownLabel-Stamps,--dropdownIcon-layers,--dropdownShowSelected),
d(t:Color,--dropdownLabel-Color Picker,--dropdownIcon-palette,--dropdownShowSelected),
(save,--isSmallScreen),(printAnnotatedPdf,--isSmallScreen),(stickyNote,--isSmallScreen),(highlight,--isSmallScreen),(t:Help),(toggleChat,t:Summary,--sidebar)
```

### enabledRedactionActions

The Actions enabled in redaction mode.
​

Default value:

```text
(t:Navigation),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),
(t:Mode),(t:PageEntry),(save,--showAtAllSizes),(mouse),(drawRedaction,textRedaction,--showAtAllSizes),(t:Help),(t:Search,--sidebar)
enabledIndexerActions=(t:PageEntry),(t:Navigation),(mouse),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),(drawRectangle,--showAtAllSizes),(selectText),(t:Help)
enabledEditActions=(t:Navigation),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),
(t:Mode),(t:PageEntry),(save,--showAtAllSizes),(t:DocumentManipulation,--showAtAllSizes),(t:Help)
```

### enabledIndexerActions

The Actions enabled in indexing mode.
​

Default value:

```text
(t:PageEntry),(t:Navigation),(mouse),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),(drawRectangle,--showAtAllSizes),(selectText),(t:Help)
```

### enabledEditActions

The Actions enabled in document editing mode.
​

Default value:

```text
(t:Navigation),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),
(t:Mode),(t:PageEntry),(save,--showAtAllSizes),(t:DocumentManipulation,--showAtAllSizes),(t:Help)
```

### enabledPageSelectActions

The Actions enabled in document page selecting mode.  No additional actions are configured by default
​

Default value:

```text
(t:PageEntry),(t:Navigation),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),(t:Help)
```
​

### enabledSignatureActions

The Actions enabled in document signing mode.

> **Note: This action allows users to draw their signature on a document.**
​

Default value:

```text
(t:Navigation),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),
(t:Mode),(t:PageEntry),(save,--showAtAllSizes),(mouse),(signature),(t:Help)
```

### enabledOpenViewerActions

The Actions enabled in the quick document viewing mode.
​

Default value:

```text
(t:Navigation),(prevPage,nextPage, zoomIn,zoomOut,--isSmallScreen),
(t:Mode),(t:PageEntry),(printAnnotatedPdf),(t:DocumentManipulation,--showAtAllSizes),(mouse),(t:Help)
```

### enabledOpenViewerWithTextActions

The Actions enabled in the quick document viewing mode with text search and select capabilities added.
​

Default value:

```text
(t:Navigation),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),(selectText),
(annotationMode,editMode,redactMode,viewerwithtextMode),(t:PageEntry),(printAnnotatedPdf),(mouse),(t:Search,--sidebar)
```

## Overriding enabled actions

Overriding any of the properties listed in the last section in the `openannotate-override-placeholders.properties` with a value different than the default would change the actions displayed in AEV for that mode.

### Overriding enabled actions using ActionIds

To add a particular action to a specific mode in AEV, the actionId for that action can be added to the comma separated list for the mode specific property.

For example, if you want to add the `Print Annotated PDF` Action to `Signature Mode`, add the following to the `openannotate-override-placeholders.properties`:

```text
enabledSignatureActions=(t:Navigation),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),(t:Mode),(save,--showAtAllSizes),(mouse),(signature),(t:Help),(printAnnotatedPdf)
```

 This overrides the default value of `enabledSignatureActions`:

```text
enabledSignatureActions=(t:Navigation),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),(t:Mode),(save,--showAtAllSizes),(mouse),(signature),(t:Help)
```

 And add the `printAnnotatedPdf` action to this mode.

### Overriding enabled actions using ActionTypes

AEV action types are predefined groups of actions made for faster/easier (though less granular) configuration of AEV.

Notice that in the default values listed in the section above, certain values are prefixed with "t:" (example: `(t:Navigation)`) while others are listed without a prefix (example: `(selectText)`).

Those with the prefix signify that we are configuring an entire action type (group of actions) while those without the prefix signify that what we are configuring is a specific actionId for one singular action.

See the full list and description of these Action Types below:

```json
/**
 * Action which change the mode Alfresco Enterprise Viewer is currently in.
 */
MODE: "Mode",
```

Actions that belong to this type: `annotationMode`, `redactMode`, `editMode`, `signatureMode`.
​

```json
/**
 * Actions which require the document being viewed to be a  PDF to function.
 */
PDF: "Pdf",
```

Actions that belong to this type: `drawRedaction`, `signature`, `rotatePageClockwise`, `rotatePageCounterClockwise`, `selectText`, `strikeout`, `insertText`, `replaceText`, `annotatedPdf`, `unannotatedPdf`, `offlineAnnotatedPdf`, `extractPdfPages`, `printAnnotatedPdf`, `checkinOfflineAnnotatedPdf`.

```json
/**
 * Actions which require the document to have multiple pages.
 */
MULTI_PAGE: "MultiPage"
```

Actions that belong to this type: `extractPdfPages`, `extractPdfAndSavePages`, `prunePdf`, `deletePdfPages`, `nextPage`, `prevPage`, `sectionPdfDocument`.

```json
/**
 * Actions related to navigating the document.
 */
NAVIGATION: "Navigation",
```

Actions that belong to this type: `zoomIn`, `zoomOut`, `fitWidth`, `fitHeight`, `nextPage`, `prevPage`.

```json
/**
 * Actions related to changing the zoom level of the document being viewed.
 */
ZOOM: "Zoom",
```

Actions that belong to this type: `zoomIn`, `zoomOut`, `fitWidth`, `fitHeight`.

```json
/**
 * Actions that once selected, remain active until the tool is used.  Currently these are all actions for 
 * creating annotations or annotation-like objects.  
 */
TOOL: "Tool",
```

Actions that belong to this type: `mouse`, `drawRedaction`, `signature`, `stickyNote`, `drawLine`, `drawArrow`, `drawRectangle`, `textbox`, `drawEllipse`, `freeDraw`, `selectText`, `highlight`, `strikeout`, `insertText`, `replaceText`, `acceptStamp`, `approvedStamp`, `pageSizedCheckmarkStamp`, `rejectStamp`, `reviewedStamp`.

```json
/**
 * Actions that once selected, remain active until the they are selected again.  Toggle actions might also
 * have different behaviors between when they are selected and de-selected.
 */
TOGGLE: "Toggle",
```

Actions that belong to this type: `toggleAnnotations`, `keepToolSelected`,  `compareDoc`, `syncScroll`, `sectionPdfDocument`.

```json
/**
 * Actions that in some form download or export the document being viewed.
 */
DOWNLOAD: "Download",
```

Actions that belong to this type: `annotatedPdf`, `unannotatedPdf`, `offlineAnnotatedPdf`, `extractPdfPages`, `printAnnotatedPdf`, `sectionPdfDocument`.

```json
/**
 * Actions that create annotations on the document.
 */
ANNOTATION: "Annotation",
```

Actions that belong to this type: `stickyNote`, `drawLine`, `drawArrow`, `drawRectangle`, `textbox`, `drawEllipse`, `freeDraw`, `highlight`, `strikeout`, `insertText`, `replaceText`, `acceptStamp`, `approvedStamp`, `pageSizedCheckmarkStamp`, `rejectStamp`, `reviewedStamp`, `undo`, `redo`, `checkinOfflineAnnotatedPdf`.

```json
/**
 * Actions that manipulate/related-to annotations but do not create then.
 */
ANNOTATION_MANIPULATION: "AnnotationManipulation",
```

Actions that belong to this type: `save`, `undo`, `redo`, `refresh`, `toggleAnnotations`.

```json
/**
 * Actions that create/draw annotations on the document using Raphael.
 */
DRAWING: "Drawing",
```

Actions that belong to this type: `drawLine`, `drawArrow`, `drawRectangle`, `textbox`, `drawEllipse`, `freeDraw`, `drawRedaction`.

```json
/**
 * Actions that create/draw annotations that are attached to the document's text.
 */
TEXT: "Text",
```

Actions that belong to this type: `selectText`, `highlight`, `strikeout`, `insertText`, `replaceText`.

```json
/**
 * Actions that create annotations which are a static or dynamic image on the document.
 */
STAMP: "Stamp",
```

Actions that belong to this type: `acceptStamp`, `approvedStamp`, `pageSizedCheckmarkStamp`, `rejectStamp`, `reviewedStamp`, `signature`.

```json
/**
 * Miscellaneous. Actions that create annotations and do not fit into any other type.
 */
MISC: "Misc",
```

Actions that belong to this type: `mouse`, `stickyNote`, `keepToolSelected`, `addAttachment`.

```json
/**
 * Actions that can permanently modify the document itself.
 */
DOCUMENT_MANIPULATION: "DocumentManipulation",
```

Actions that belong to this type: `extractPdfAndSavePages`, `prunePdf`, `deletePdfPages`, `sectionPdfDocument`, `rotatePagerClockwise`, `rotatePageCounterClockwise`.

```json
/**
 * Actions that uses page selection.
 */
PAGE_SELECTION: "PageSelection",
```

Actions that belong to this type: `extractPdfPages`, `extractPdfAndSavePages`, `prunePdf`, `deletePdfPages`, `sectionPdfDocument`.

```json
/**
 * Actions relating to the annotation summary.
 */
SUMMARY: "Summary",
```

Actions that belong to this type: `printSummary`, `exportSummary`.

```json
/**
 *  Actions relating to redact all search button in the redaction mode.
 */
SEARCH: "Search",
```

Actions that belong to this type: `redactSearchResults`.

```json
/**
 * Actions that related to comparing the current document with another document within Alfresco Enterprise Viewer. 
 */
COMPARE: "Compare",
```

Actions that belong to this type: `compareDoc`, `syncScroll`.

```json
/**
 * Actions that should be collapsed into the 'Tools' dropdown when the screen is a small size.
 */
SMALL_DROPDOWN: "Smalldropdown",
```

Actions that belong to this type: `extractPdfPages`, `extractPdfAndSavePages`, `prunePdf`, `sectionPdfDocument`.

```json
/**
 * Actions that refer the user to help or tutorials that show them how to use Alfresco Enterprise Viewer.
 */
HELP: "Help"
```

Actions that belong to this type: `help`.

```json
/**
 * Actions that should be used only if the document has sections.
 */
SECTIONED: "Sectioned"
```

Actions that belong to this type: `printSectionsAction`.
​
**Note** : The `printSectionsAction` action and the `SECTIONED` action type was developed alongside a new property, `determineSectionsFromProperty` that can allow you to parse sections automatically for your document based on a document property. `determineSectionsFromProperty` defaults to `false`, but should be equal to the name of the property if you want to turn on the feature.

```json
/**
 * Actions that can be used by non-sectioned documents. 
 */
NONSECTIONED: "NonSectioned"
```

Actions that belong to this type: `printAnnotatedPdf`.
​

## Action groups, toolbar order, and dropdowns

### Action groups

The grouping of actions is controlled by enclosing each group of actions or action types within parenthesis.  These action groups are displayed in the toolbar separated by vertical dividers.

### Toolbar ordering

The order of actions in the toolbar is controlled by the order of the comma separated list of these action groups. The order of the comma separated list determines how the toolbar appears in AEV.  

> **Note:** The AEV logo, load time, and color picker are currently not configurable and will always appear in set positions.  

### Action dropdowns

Dropdowns are configured by adding dropdown specific properties within the group.  For example, the actions in the Action Type `Download` can be set as a dropdown using the following:

`d(t:Download,--dropdownLabel-Downloads,--dropdownIcon-download-alt)`

The `d` surrounding the group configures it to be a dropdown.
​
Properties relating to dropdowns:

| Property | Description |
| -------- | ----------- |
| --dropdownLabel | Sets the `dropdownLabel` to the specified value. Defaults to an empty string. |
| --dropdownIcon  | Sets the `dropdownIcon` to the specified value. Defaults to chevron-down. These refer to glyphicon values provided at [https://getbootstrap.com/docs/3.3/components/](https://getbootstrap.com/docs/3.3/components/){:target="_blank"}. |

## Enabling and disabling modes of AEV

The modes that appear in AEV are controlled by the `enable{MODE}Actions` properties just like the actions are.

Available modes in AEV are displayed on the toolbar in a dropdown. To display all available modes in AEV, you can configure the `(t:Mode)` Action Group on every `enable{MODE}Actions` property and all modes will show in the dropdown no matter what mode you are currently in.

To get more granular with what modes appear you can use a comma separated list of modes to include rather than using the Action Group. For example, `(annotationMode,editMode)`.

Take a look at the following example of disabling modes in AEV:

To disable certain modes in AEV, we would change the (t:Mode) enabledAction to the specific modes we want to be enabled. For instance, if we only wanted to enable Edit mode, then our properties would go from:

`enabledEditActions=(t:Navigation),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),`
`(t:Mode),(t:PageEntry),(save,--showAtAllSizes),(t:DocumentManipulation,--showAtAllSizes),(t:Help)`
`enabledOpenViewerActions=(t:Navigation),(prevPage,nextPage, zoomIn,zoomOut,--isSmallScreen),`
`(t:Mode),(t:PageEntry),(printAnnotatedPdf),(t:DocumentManipulation,--showAtAllSizes),(mouse),(t:Help)`
​
\
\
to:

`enabledEditActions=(t:Navigation),(prevPage,nextPage,zoomIn,zoomOut,--isSmallScreen),`
`(editMode),(t:PageEntry),(save,--showAtAllSizes),(rotatePageCounterClockwise,rotatePageClockwise,--showAtAllSizes),(t:Help)`
`enabledOpenViewerActions=(t:Navigation),(prevPage,nextPage, zoomIn,zoomOut,--isSmallScreen),`
`(editMode),(t:PageEntry),(printAnnotatedPdf),(rotatePageCounterClockwise,rotatePageClockwise,--showAtAllSizes),(mouse),(t:Help)`
---
title: AEV collaboration features
---

Alfresco Enterprise Viewer has support for real-time collaboration features including real-time annotations, chat functionality, and presentation mode. To take advantage of these collaboration features, a web socket server must be installed and configured. Currently, the only web socket implementation of Enterprise Viewer is one that uses [Socket.IO](http://socket.io/){:target="_blank"} built on a Node server. See the [Node website](https://nodejs.org/){:target="_blank"} for more information.

You can see a [screen capture of the collaboration features](https://www.youtube.com/watch?v=yUOtGXHnxXo){:target="_blank"} in YouTube.

## Install NodeJS

In order to use the collaboration features, you must first install Node on the server that will act as the collaboration server.

1. Download the appropriate installer from the [NodeJS website](https://nodejs.org/download/){:target="_blank"}.

    On Windows, use [Nodist](https://github.com/marcelklehr/nodist){:target="_blank"} to easily manage NodeJS installations.

    On Linux, follow the [instructions](https://github.com/nodesource/distributions){:target="_blank"} to install from the command-line.

2. Run the installer to completion.

    Make sure that the path to your installed instance of Node is on the system `PATH`.

To verify that Node is installed successfully and has been added to the system `PATH`, open a command prompt from any directory, type each command, and press the ENTER key after each one:

  ```bash
  node -v
  npm -v
  ```

The version of Node and `npm` are output on the command-line. `npm` is a command-line tool for installing Node packages.

## Collaboration server port

The node server port is configured in the `config/collaborationConfig.js` file. By default, the collaboration server listens for HTTP requests on port `3000` and does not listen on an HTTPS port.

The HTTP port can be configured by modifying the following line:

```text
config.httpPort = 3000;
```

The collaboration server can support listening on an HTTPS port as well. Note that you can configure HTTP _and_ HTTPS, as well as one or the other. To listen on a port with SSL, configure the following properties (example values shown):

  ```text
  config.httpsPort = 3000;
  config.sslKeyPath = "../../../Apache/Apache24/conf/certificates/{my-key}.key";
  config.sslCertPath = "../../../Apache/Apache24/conf/certificates/{my-cert}.crt";
  ```

Note that the file path properties are relative to wherever the `server.js` file is located.

## Configure Enterprise Viewer to connect to the Node server

In order to use the Node server, you must configure Enterprise Viewer to use it. The two properties that must be set are the `collaborationEndpoint` and `collaborationModeEnabled` properties. For more information on these properties and how to set these properties, read [AEV configuration files]({% link enterprise-viewer/latest/config/files.md %}).

## Collaboration modes

With collaboration features enabled, Enterprise Viewer can be run in: normal mode or collaboration mode.

### Normal mode

Normal mode is the default mode for Enterprise Viewer. This mode does not include any collaboration features. It is configured by setting the `collaborationModeEnabled` property to `false`.

### Collaboration mode

Collaboration mode is the mode that enables real-time annotations and well as chat functionality. It is configured by setting the `collaborationModeEnabled` property to `true`.
---
title: Enterprise Viewer FAQ
---

### Is Enterprise Viewer based on OpenAnnotation (`http://www.openannotation.org/`)?

No, Enterprise Viewer is based on the open Adobe XFDF standard for annotating PDFs - [https://www.iso.org/obp/ui/#iso:std:iso:19444:-1:ed-1:v1:en](https://www.iso.org/obp/ui/#iso:std:iso:19444:-1:ed-1:v1:en>){:target="_blank"}.

### Where are annotations stored?

Annotations are stored in the ECM repository as related objects to the document being annotated. The annotations are stored in the XFDF specification to allow other applications to interface with the open specification.

### I use old versions of web browsers. Is it compatible?

The front-end uses jQuery and Dojo.

### Does Enterprise Viewer allow concurrent access to annotate the same document by several users?

Enterprise Viewer allows any number of users to concurrently annotate a document since each users' annotations are stored as separate objects.

### I am seeing stale page images, does Enterprise Viewer Cache?  How can I clear this cache?

Yes. Enterprise Viewer makes heavy use of caching at both the Server and Browser level. To see totally fresh document pages, clear out AEV's server caches, as well as your browser cache to see your changes take effect. To clear a running instance of AEV's server cache, you can simply hit these endpoints:

First:

![Get Ticket Endpoint]({% link enterprise-viewer/images/get-ticket.png %})

Save the ticket from the above call for the next call:

Finally:

![Clear Caches]({% link enterprise-viewer/images/clear-caches.png %})

After those two steps and browser cache clear, you should see fresh images.

### How does Enterprise Viewer scale for large deployments?

Enterprise Viewer easily scales to multiple instances with load balancing to allow scaling to any number of users.
---
title: AEV configuration files
---

When installing and setting up Alfresco Enterprise Viewer it's important to understand how configuration settings work.

## Spring properties files

## AEV web application properties

Spring loads properties files into the system in a specific order to allow overriding. Properties are loaded in the following order (last wins):

1. `defaults.properties` (sensible defaults for every property)
2. `project-placeholders.properties` (project specific properties)
3. `openannotate-override-placeholders.properties` (Optional. Tomcat-specific properties)
4. `override-placeholders.properties` (environment-specific properties)

In general, use the `openannotate-override-placeholders.properties` to override any of the default properties. This file must be placed on the Tomcat classpath (for example, in the `<TOMCAT_HOME>/shared/classes` folder), and overrides all properties located in `OpenAnnotate.war`. Properties defined here can still be overridden by `override-placeholders.properties`, but if for example server URLs are all that need to be defined, these can be left in `openannotate-override-placeholders.properties`, allowing WARs to be promoted through various environments without needing to be re-built / configured.

## OpenContent properties

OpenContent properties related to AEV are located in the `universal-defaults.properties` file. Any of these properties can be overridden if desired in the `opencontent-override-placeholders.properties` file.

## Default properties

The following are the configurable properties for Enterprise Viewer:

### serviceAccountUsername

This is the service account user name to use when logging in using the "stored" endpoint. The stored endpoint allows you to log in using the configured service account and provide a display name (`displayName`) to identify the user you are logging in for.

> **Note:**  This property must be overridden if you're using the "stored" endpoint.

Default value: `""`

### serviceAccountPassword

This is the service account password to use when logging in using the "stored" endpoint. The stored endpoint allows you to log in using the configured service account and provide a display name to identify the user you are logging in for.

> **Note:** This property must be overridden if you're using the "stored" endpoint.

Default value: `""`

### isServiceAccountPasswordEncrypted

Set to `true` if the password for the service account for the stored login endpoint is encrypted, or `false` if otherwise.

Default value: `false`

### serviceAccountDocbase

The docbase the service account should login to.

Default value: `""`

### emailInviteUrl

This URL is used in the invitation to collaborate email. If the `[docId]` placeholder is specified, it is replaced by the `objectId` of the document being viewed when the invitation is sent.

Default value: `http://localhost:8080/OpenAnnotate/viewer.htm?docId=[docId]&presenterMode=true&mode=readOnly`

### ocRestEndpointAddress

This URL is the REST endpoint for the running instance of OpenContent. If Enterprise Viewer is being used in a load balancing setup and the instances of Enterprise Viewer and OpenContent are on the same server, this property should be the **non-load balanced url**, to ensure that the requests to OpenContent are always directed to the same OpenContent instance.

Default value: `http://localhost:8080/OpenContent/rest`

### clientRequestUrl

The URL that client requests from Enterprise Viewer to OpenContent should be made to. Generally, this only changes if OpenContent has a different REST root, `/alfresco/OpenContent` for example used when OC is an Alfresco subsystem.

Default value: `/OpenContent/rest`

### collaborationEndpoint

This URL is the endpoint on which the web socket server is listening for a connection. This should be used when Enterprise Viewer is run in collaboration mode. If collaboration mode is enabled but this property is not specified, collaboration mode will not work properly.

For load balanced setups, there should only be a single collaboration server. So this should point to the **single, non-load balanced URL**.

Default value: `http://localhost:3000`

### collaborationModeEnabled

This property represents whether or not Enterprise Viewer is being run in collaboration mode to take advantage of features like real-time annotations and chat functionality.

Default value: `false`

### forceNonModalNotifications

This property represents whether or not Enterprise Viewer forces non-modal notifications.

Default value: `true`

### singleAnnotationDialog

Set to `true` if only one annotation dialog should ever be open at a time, or `false` otherwise.

Default value: `true`

### allowExternalReviewers

When set to `true` annotations from third party applications for both users that do not have an account in Alfresco and users that have corresponding accounts in Alfresco should be accepted. When set to `false`, only annotations from users with a corresponding Alfresco account will be accepted. 

In order to have `allowExternalReviewers` set to `true`, a special license setting must be set in your AEV license by the Hyland License Team with the property `hasExternalOAUsers: true`.

Default value: `false`

### AllowMultipleOfflineReviewers

When set to `false` offline annotations will be owned by the user that checked the annotations in. No matter which user is set on the offline annotation, the annotation will always be displayed as being added by the user who checked in the document.

Default value: `true`

### excludeEmbeddedAnnotations

Set to `true` if annotations embedded in the PDF should not be fetched, or `false` to allow annotations to be imported from third party systems like Adobe. Any users that do not have a corresponding Alfresco account will not have their annotations displayed in AEV.

Default value: `true`

### serverAnnotationsEditable

Set to `true` if server annotations can be edited. Setting this to `false` prevents users from editing their annotations after their session ends.

Default value: `true`

### sidebarDefaultOpen

This property represents whether or not Enterprise Viewer should start up with its sidebar (which contains other modules like summary, search and collaboration) showing.

Default value: `true`

### helpUrl

This URL points to a "help" website for using Enterprise Viewer. **This is not recommended to be overridden.**

Default value: `https://docs.alfresco.com/`

### printSummaryBaseType

This is the base type to use when fetching the attributes for the print summary window. If the attributes specified are not attributes on this type, Enterprise Viewer fails to initialize properly.

Default value: `Document`

### oaLogoPath

The path for the logo to display at the top left corner on the toolbar in the Enterprise Viewer interface. Useful to override for different logos. This path is relative to the `src/main/webapp` directory.

Default value: `images/logos`

### oaIconPath

The path for the icons to display in the Enterprise Viewer interface. This path is relative to the `src/main/webapp` directory.

Default value: `images/icons`

### targetMimetype

The target MIME type to use when transforming documents. Defaults to PNG, but supports JPG (`image/jpeg`) as well.

Default value: `image/png`

### imageFullResolution

The final resolution to use when transforming image pages to PNG or JPG. Lower resolutions may be loaded first.

Default value: `64`

### imageMinimumResolution

The minimum resolution to load the image when progressively loading the image.

Default value: `16`

### pdfFullResolution

The final resolution to use when transforming PDF pages to PNG or JPG. Lower resolutions may be loaded first.

Default value: `244`

### pdfMinimumResolution

The minimum resolution to load the image when progressively loading the image.

Default value: `64`

### progressiveReloadSteps

The number of reloads to make between the minimum resolution image and the full resolution.

Default value: `1`

### pageZoom

The initial page zoom to use when loading a document. The allowed values are either `fitHeight` or `fitWidth`. Fit height adjusts the document so the entire height is visible. Fit width adjusts the document so the entire width is visible.

Default value: `fitWidth`

### numPreloadPages

The number of pages to preload. Preloading works by making requests to fetch pages close to the current page the user is viewing in order to cache the image, which results in shorter load times when the page is changed. The allowed values are the following:

* `0`: This tells AEV to preload all the pages of the document
* `-1`: This tells AEV to not use preloading at all
* Any other positive integer: This integer specifies the total number of pages to preload - half are pages before the current page and the other half are after the current page.

   > **Note:**
   >
   > * The configured value should be a multiple of 2 because the number of pages to preload is divided by 2.
   > * Specifying `1` and `2` accomplishes the same result.
   >
   > * Once the number of preloaded pages equals the configured value, no more pages are preloaded until the page is changed.

Default value: `10`

### enhancedColorMode

This flag controls the colors that are displayed and allowed to be chosen for annotations.

* If set to `true` there is no limit on the color of created annotations and the downloaded annotations maintain their colors.
* If set to `false` the user may not choose different colors for annotations and instead, all of the user's annotations are either red, yellow for a highlight, and all other annotations are blue (the same is true for the downloaded annotated PDF).

Default value: `true`

### dateFormat

The format to use when displaying dates in annotation dialog boxes. The formatting uses the open source library `Moment.js`, so any formats found in the [Moment.js formatting Documentation](http://momentjs.com/docs/#/displaying/format/){:target="_blank"} may be used.

Default value: `MM/DD/YYYY`

### enabledActions and Modes

Configuring what Buttons and Actions appear in Enterprise Viewer is a little more in-depth than the average configuration option.

See [Configure Enterprise Viewer actions and modes]({% link enterprise-viewer/latest/config/actions.md %}) for more details.

### quillEnabledButtons

A comma separated list of buttons that's visible in the quill toolbar. All currently supported quill buttons are bold, italic, and underline.

Default value: `bold,italic`

### leftSidebarModules

A comma separated list of views to be enabled in the left sidebar.

Default value: `bookmarks,attachedDocs,thumbnails,sections,documentList`

### rightSidebarModules

A comma separated list of views to be enabled in the right sidebar.

Default value: `summary,search,participants,suggestedRedactions`

### redactionType

What type of redaction should be made when entering redaction mode via the dropdown.
Possible values include `redactInPlace`, `redactedAsCopy`, and `unredactedAsCopy`.

Default value: `redactInPlace`

### initialDrawingTool

A comma separated list of drawing buttons that should be selected when Enterprise Viewer loads. The first valid button on the list is selected when Enterprise Viewer first loads.

Default value: `drawRedaction, signature, mouse`

### autosaveInterval

The number of milliseconds Enterprise Viewer waits between each autosave.

* `0`: This tells AEV to NOT autosave.
* Any other positive integer: The number of milliseconds Enterprise Viewer waits for between each autosave. This should not be set to a number below 5000 - 10000 (5 - 10 seconds), as it could cause undefined behavior.

Default value: `60000`

### autosaveBeforeExit

Set to `true` if Enterprise Viewer should automatically save before exiting, or `false` otherwise.

Default value: `true`

### enabledPopupNotifications

The list of the Collaboration mode notifications that are enabled and appear on internal popups when the **Participants** tab is closed. To disable a type of notification, remove it from the list of notification in this property. The default is that all notification are enabled.

Default value:

```text
chat,userJoined,userLeft,serverConnection,checkInAnnotations,checkInAnnotationsFailed,burnInRedactionFailed,checkinAnnotationsFinished,pageSelectMode,welcomeBackPage,save,loadedAnnotations,saveFinished,copyPaste,copyPasteNotReady,tooLargeForThumbnails,closeSave,closeCopyPaste,pageRangeInvalid,logstashFailed,portfolioContainsNonPdf,docHasAnnotations,afterPageLoad,textLocationDataFailed,enterSectioningMode,sectionNameInvalid,displayDocumentListFailed
```

### slideViewerTileDirectoryRoot

The root directory on the server filesystem where the slide viewer "tiles" should be served from. It is commonly a URL that is redirected through Apache to request files from the server.

Default value: `http://localhost:8080/OpenAnnotate/images/seadragon/`

### sessionCookieName

The name of the session cookie which is used to track sticky sessions in load balanced environments. For load balanced environments, sticky sessions are required to ensure Enterprise Viewer always hits the correct correct OpenContent with all its internal requests.

Default value: `JSESSIONID`

### checkServletRequestForSessionId

Set to `true` if a check should be made for the sessionId on the Servlet requests from Enterprise Viewer's front-end and append it to the requests to OC, or `false` otherwise. This sessionId is used to maintain sticky sessions in load-balanced environments. If this property and `checkServletCookieForSessionId` are both set, the sessionId set on the Servlet request overrides any sessionId set on the cookie.

Default value: `true`

### checkServletCookieForSessionId

Set to `true` if a check should be made for the sessionId on a cookie and append it to the requests to OC, or `false` otherwise. This sessionId is used to maintain sticky sessions in load-balanced environments. If this property and `checkServletRequestForSessionId` are both set, the sessionId set on the Servlet request overrides any sessionId set on the cookie.

Default value: `true`

### snapThreshold

The percentage of a highlight that must overlap a word for it to be detected as a word. Highlights snap to the detected words and get the underlying text. If no highlight snapping is desired, set to a value over 100% (i.e. < 1.0).

Default value: `0.15`

The GIFs below show the results of different values of `snapThreshold`:

#### Example snap threshold = 10% (`0.1`)

![Highlight Snap Threshold 10%]({% link enterprise-viewer/images/snap-threshold_10.gif %})

#### Example snap threshold = 40% (`0.4`)

![Highlight Snap Threshold 40%]({% link enterprise-viewer/images/snap-threshold_40.gif %})

#### Example snap threshold 100% or more (greater than `1.0`)

![Highlight Snap Threshold 100% or more (greater than 1.0)]({% link enterprise-viewer/images/snap-threshold_gt_100.gif %})

### rerenderPageOnResize

Set to `true` to send new requests to OC every time you zoom in or out on a page, or `false` otherwise.

Default value: `true`

### quickSearch

Set to `true` to allow the user to immediately search selected text when  Ctrl+F is pressed, or `false` otherwise.

Default value: `false`

### numberOfPagesForLargeDocuments

The number of pages that are considered as a "large" document.

* If the value is `0`, it ignores considering documents with many pages as a large document.
* If a document has more pages than the value here, text search data isn't loaded initially, and thumbnails are disabled.
* Text search data can still be manually loaded by the user later, after answering `yes` to a modal dialog box informing them of the delay.

Default value: `99`

### sizeOfLargeFiles

The size (in bytes) to consider a document as "large". If a document's size is bigger than the value here, a user is prompted with a modal dialog box to confirm calls that require a lot of resources to limit memory usage.

Default value: `104857600`(100 MB)

### maxDocumentSize

The maximum size of a document (in bytes) that is loaded.

* If the value is `0`, there are no bounds for large documents.
* Otherwise, if a document's size is bigger than the defined value, a modal dialog box appears to let the user know that their document is too large to open.

Default value: `2147483648`(2 GB)

### enableCommentBox

Set to `true` if the comment box is enabled in the annotation dialog box, or `false` otherwise.

Default value: `true`

### enablePicklist

Set to `true` if picklist features are enabled for Enterprise Viewer, or `false` otherwise.

If picklists are enabled, `picklistUrl` must have a parameter to work.

> **Note:** Currently, picklists are only used for annotation dialog boxes.

Default value: `false`

### enableStatuses

Set to `true` if annotations can have a status and previous statuses appear.

Default value: `true`

### showSmallActionName

Set to `true` if the actions dropdown shown at small resolutions should reflected the currently selected tool, or `false` otherwise.

Default value: `true`

### asyncPicklist

Set to `true` if picklists used for Enterprise Viewer are asynchronous, or `false` otherwise.

Default value: `false`

### picklistUrl

The picklist information needed to retrieve picklist data. This is either a picklist name to reference a configured picklist in OpenContent or a URL to retrieve picklist data from an external source.

Default value: `""`

### externalPicklist

Set to `true` if the picklist is from an external source, or `false` otherwise.

Default value: `false`

### searchPagesPerRequest

The number of pages to fetch search data for in a single request.

Default value: `200`

### textDataPagesPerRequest

The number of pages to fetch text select data for in a single request.

Default value: `200`

### enableMacroMetadataFetching

> **Note: UNIMPLEMENTED - DO NOT USE -**

Gets all PDF MetaData (wordmaps, text select, bookmarks, etc.) in a single request if set to `true`. Otherwise each one is fetched via its own server request.

Default value: `false`

### macroMetadataFetchingBatchSize

> **Note: UNIMPLEMENTED - DO NOT USE -**

The number of pages to fetch ALL PDF metadata for per request.

Requires `enableMacroMetadataFetching` to be set to `true`, or otherwise does nothing.

Default value: `200`

### maxUserPageCookieSize

The maximum number of user page cookie objects to store.

Default value: `50`

### annotationSummaryDefaultSort

The XFDF fields to sort the annotation summaries on, ordered from most important to least important.

Default value: `page,!p4`

### warnBeforeSaveModifications

Whether or not the user wants a modal dialog box to appear asking them to confirm that they want to save page modifications when in edit mode.

Default value: `false`

### thumbnailResolution

The minimum resolution to load the thumbnail images for the document.

Default value: `32`

### initialThumbnailLoad

Amount of thumbnails to initially load.

Default value: `25`

### newVersionOnModification

Set to `true` if a new version of the document should be created when the document is modified. If `false`, the document in the repository remains the same version when modified.

Default value: `true`

### majorVersionOnModification

Set to `true` if a major version of the document should be created when the document is modified. If `false`, the document in the repository defaults to a minor version when modified.

Default value: `false`

### alertDocumentHasAnnotations

Set to `true` if the user is alerted that the current document in OpenViewer has annotations.

Default value: `true`

### keepToolSelectedDefault

Whether the keep tool selected feature should be on by default.

Default value: `false`

### annotationTypesToShowDialogForWithKeepToolSelected

Which annotation type(s) dialogs to show when the annotation is created.

Different annotation types:

```text
Line,Oval,Rectangle,Highlight,Cross-Out,Inserted Text,Replacement Text,Reply,Sticky Note,Signature,Approved Stamp,Accept Stamp,Reject Stamp,Reviewed Stamp,PageSizedCheckmark Stamp,Status,Freetext,File Attachment,Free Draw,Redaction
```

Default value: `""`

### thumbnailBatchSize

The number of thumbnails to load for every subsequent batch after the first.

Default value: `200`

### thumbnailWidth

The width of the sidebar thumbnail previews.

Default value: `150`

### configuredLocales

Enterprise Viewer takes a list of locales from the browser and returns the first configured locale from this list as the language to display in AEV. If none of the locales from the list are configured in the users' browser, the `defaultLocale` is used regardless.

You'll find a list of all locales AEV supports in [Supported Platforms]({% link enterprise-viewer/latest/config/supported-languages.md %}).

Default value: `en,fr,de`

### defaultLocale

The default locale to use if the user has no configured locales. This value must already be available in the configured locales.

Default value: `en`

### checkRenditioningDelay

The default time between checks for whether a document has a rendition.

Default value: `10000`

### loadAnnotationsWithDocInfo

Load annotations simultaneous with document information. Prevents the user from viewing the document until the annotations are loaded.

Default value: `false`

### displayAnnotationModifyDate

Display an annotation modified date instead of the creation date throughout Enterprise Viewer.

Default value: `false`

### minPagesToDefafultSectionModeOn

The minimum number of pages to default into sectioning mode. Set to `0` to prevent sectioning mode.

Default value: `10`

### determineSectionsFromProperty

Whether to determine sections automatically from a property property name or keep the default value.

Default value: `false`

### saveSectionsAsBookmarks

Whether or not to save sections as bookmarks. Overriding this to `false` only saves the page reordering and rotating when sectioning is done.

Default value: `true`

### enablePageObfuscation

Whether or not OpenContent should obfuscate pages when transforming them. This is to prevent users from viewing a secure document through network calls.

Default value: `false`

### enableSecureViewingOverlay

Whether or not to apply the secure viewing overlay to pages when viewing them. This overlay shows the display name of the user viewing the page. Displays the current username on the document and the date when they viewed it.

Default value: `false`

### enableAEVTOverlays

Whether or not to enable functionality for AEVT (Optimus Transformations) overlays. When `true` (and AEVT is enabled), overlays are applied where configured.

Default value: `false`

### zoomClientID

Client ID property for sending a Zoom authorization call that eventually sends a request that creates a meeting. Blank by default, as you'll need to create a Zoom app to get this value and use this feature.

Default value: ``

### clientKey

The optional OC client key to be used in `OAUtil.oaRestTemplateGet/oaRestTemplatePost` calls. This key, if configured, sets as a request header and eventually used OC side for some SSO implementations.

Default value: ``

### aevChatAuthor

The chat author name that's posting in the chat from OpenContent.

Default value: `AEV Chat Bot`

A fully qualified REST URL for client side use.

Default value: `http://localhost:8080/OpenContent/rest`

## OpenContent - default properties

### license.doSendWarningEmail

Whether or not to send a warning email when the current OpenContent license is approaching an invalid state. For example: expiring, or almost at the maximum user or group user limit.

Default value: `true`

### license.expiringSoonCounter

The number of days before the license expires in which OpenContent sets a warning state for the active license.

Default value: `30`

### license.systemUserLimitCounter

Used with a user-based license: this property configures how close to the maximum allowed users the system can get before setting a warning state on the active license.

Default value: `25`

### license.groupUserLimitCounter

Used with a group-based license: this property configures how close to the maximum allowed users the license group(s) can get before setting a warning state on the active license.

Default value: `5`

### license.warning.email.recipients

When in a warning state and configured to do so, OpenContent sends a license warning email to all of the recipients listed in this property.

Default value: ``

### fail.loud.on.errored.embedded.annotations

Fail loudly on errors that occur with embedded annotations. This defaults to `true` so that the user is notified of errors loading annotations.

This is an experimental feature. If set to `false`, users may be able to load, download, print previously erroring annotated PDFs but some annotations may be missing.

Default value: `true`
---
title: Configuring overlays 
---

## What is an overlay?

An overlay, also known as a watermark, is applied to the surface of the PDF and bonded to it, preventing the user from moving or modifying the overlay. The overlay is applied using OpenOverlay, a Java-based tool embedded within Alfresco Content Services. Out of the box overlays are supplied as part of some base Accelerator configurations. Configuration is required to customize overlay behavior in Alfresco Content Accelerator and Alfresco Enterprise Viewer. Below are the details of how to wire up a new overlay configuration file and how to assemble it.  

## Overlay capabilities

OpenOverlay can apply overlays to document PDF renditions. These overlays include static text, a static image file, a dynamic property value (such as a value set on the document node), and/or one of a few special keywords tokens including `pageNum`, `isFirstPage` and `isLastPage`. For example, you can stamp `cm:createdDate` or `cm:title` on the document, with pixel precision at any location on the page. You can configure different overlays to be applied based on dynamic criteria, including Object Type, node property value, and page layout. You can also configure dynamically generated overlays upon document view time (most common use case), or permanently applied upon initial PDF creation. For instance, many customers use OpenOverlay to dynamically apply the `Viewed On` date to the document to ensure the date extracted is known, should the document be printed or sent outside the system. You can specify the text as any font, color, and size.

## Overlay limitations

* OpenOverlay applies images directly at the pixel location specified, and does not wrap text or images.
* OpenOverlay is limited to working with the fonts that are installed on the operating system running OpenOverlay (either the Alfresco Content Services system or the AEVT system depending on your configuration).

## Set up application to display overlays

There are a few configurations that need to be set up to view overlays on documents.

1. `annotation.shouldUseOverlays=true/false`

    This property tells the application that it should display configured overlays on documents. This should be set to true in order to see any configured overlays on viewing of documents.

    Out of the Box, this is set to `false` by default. If you installed an accelerator (PnP or Claims) which included installing the `opencontent-override-placeholders.properties` file packaged with the release, then the configuration will by default be set to `true`.

    You can override this property in the `opencontent-extension-override-placeholders.properties` file in your [custom AMP]({% link content-accelerator/latest/develop/extension-content-accelerator.md %}).

2. `enableAEVTOverlays=true/false`

    This property enables AEVT (OAT) to handle the overlays. If you have AEVT installed and overlays should be displayed, then this should be set to `true`, or else it should be set to `false`. The default value is `false`.

    You can override this property in the `openannotate-override-placeholders.properties` file in the `/alfresco` classpath, for example, `ALFRESCO_HOME/tomcat/shared/classes`.

## Creating a new overlay

You can configure a new overlay using XML. The following section walks through the different components of an example XML overlay configuration and provides additional sample overlays. These same principles apply when modifying existing overlay configurations by overriding existing XML overlay beans.

### Overlay configuration XML components

Below are the XML components for overlay configuration.

#### Text Templates

The text template allows for the reuse of certain text formatting within overlays.  

`<text-templates />`  

Properties:

* name: unique id used as a reference for the template.

Example:

```xml
<text-template name="default">
    <text font-size="12" font-family="Arial" embed-font="true" font-weight="none">Sample.</text>
</text-template>
```

##### Text Tag {#text}

The tag within a text Template.

`<text />`

Properties:  

* template: template to use for the overlay. If not specified the template named `default` is used. **Note:** Not required for tags within `<text-template>`.
* font-size: the size of the font in points  
* font-family: the font/font-family to use  
* font-weight: bold is the currently the only supported option  
* font-style: italic is currently the only supported option  
* color: color of font as a hex (i.e. `#FFFFFF`) or string (i.e. `"red"`)  
* embed-font: `true` if the font should be embedded (defaults to `false` if not specified)  

Example:  

```xml
<text font-size="12" font-family="Arial" embed-font="true" font-weight="none" font-style="none" color="black">Text string goes here.</text>
```

#### Overlays

Specifies the configuration for an overlay.  

`<overlay />`

Properties:  

* id: unique identifier for this overlay.

Example:  

```xml
<overlay id="mySampleOverlay">...</overlay>
```

##### Block Tag

A Tag within the overlay tag. It is used as a container for a aspects of the overlay. Allows you to set it's position on the page, styling, and rotation.

`<block />`

Properties:  

* id: unique id for the overlay  
* x: x position (0 is right)
* y: y position (0 is bottom)
* alignment: defaults to left (right, left, center)  
* rotation: degrees, defaults to 0 (0, 90, 180, 270)  
* opacity: float between 0-1.0 (defaults to 1.0)  

The following example has a rectangle placed within this parent block:  

```xml
<block id="1" x="30" y="720" alignment="left" rotation="0" opacity="1">
    <rectangle x-offset="550" y-offset="0.5" background-color="black" border-width="0"/>
</block>
```

>**Note:** x="0" y="0" specifies the BOTTOM RIGHT corner of the page.

##### Text Tag

Like the text tag within the Text Template, there can also be a text tag within the overlay tag. When within a block, these text elements can take advantage of a predefined template. Any property added to the text element will override what is set in the referenced template, or the default template if no template is specified.  

`<text />`

Properties:  

* See [here]({% link enterprise-viewer/latest/config/overlay.md %}#text) for properties.  
Example (The following example's output will have formatting following that the default template but it will have red text and print `Updated Text.`):  

```xml
<text template="default" color="red">Updated Text.</text>
```

##### Image Tag

A Tag within the overlay tag. Used for adding images to overlays.

`<image />`

Properties:  

* file: Path to image to use for overlay as either a absolute path or classpath.  
* scale: percentage to scale the image by  

Example:  

```xml
<image file="classpath:@imagesBase@ocforms-header-logo.png" scale="23%"/>
```

##### Rectangle Tag

A Tag within the overlay tag. Used for adding rectangles to overlays.

`<rectangle />`

Properties:  

* background-color: color of rectangle as a hex (i.e. #FFFFFF) or string (i.e. "red")  
* border-width: line width of rectangle (must be defined, if set to 0 will defaulted to 0.1)  
* x-offset: offset to add to the x position of the block coordinate to determine the upper right x position of the rectangle  
* y-offset offset to add to the y position of the block coordinate to determine the upper right y position of the rectangle  

Example:

```xml
<rectangle x-offset="550" y-offset="0.5" background-color="black" border-width="0" />
```

##### Restrictions Tag

A Tag within the overlay tag. These tags set the container for restriction tags.

`<restrictions />`  

##### Restriction Tag

A Tag within the overlay tag. These tags are used to limit which documents/scenarios apply to the specific overlay.  

`<restriction />`  

Properties:  

* key: the OpenContent name-variable key which the restriction will be applied to.
* Hint: OpenContent names are "Alfresco Short Namespace" followed by `_` followed by "Local Property Name. For example, for `cm:name`, it would be `cm_name`.

* value: which specific value that needs to match for the overlay to be applied.  

Example:  

```xml
<overlay id="sample-portrait>
    <restrictions>
        <restriction key="page.orientation" value="portrait"/>
        <restriction key="ocContentRequest" value="true"/>
    </restrictions>
</overlay>
```

##### Actions Tag

 `<actions />`

### Using property values in XML overlay configuration  

Below are examples of properties that you can use throughout the configuration file. These keys are the OpenContent names related to each property. Depending on the environment, and even object type, these keys will change.  

```xml
<block id="0" x="30" y="30" alignment="left" rotation="0">
    <text template="default" font-size="10">Status: ${status}</text>
</block>

```

#### Built-in properties

There are also built in properties that do not need to relate to the specific object. Below are examples of these:  
`${currentDate}` resolves to the datetime that the overlay was created for the user. Ex: May 20th, 2020 11:10AM CST. It can also accept a formatting along with other datetime properties. `${currentDate~dd-MMM-yyyy}`  

```xml
<block id="0" x="30" y="30" alignment="left" rotation="0">
    <text template="default" font-size="10">Created On: ${currentDate}</text>
</block>
```

### Useful XML overlay configuration Examples

```xml
<overlay id="headerOnView">
    <restrictions>
        <restriction key="page.orientation" value="portrait"/>
        <restriction key="page.size" value="letter"/>
        <restriction key="objectType" value="Page Set Instance|simple_cr"/>
        <restriction key="ocContentRequest" value="true"/>
    </restrictions>
    <actions />
    <block id="0" x="580" y="730" alignment="right" rotation="0">
        <text template="default" font-size="10">${aw_status}</text>
    </block>
</overlay>
```

```xml
<overlay id="footerOnEmail">
    <restrictions>
        <restriction key="page.orientation" value="portrait"/>
        <restriction key="page.size" value="letter"/>
        <restriction key="objectType" value="Page Set Instance|simple_cr"/>
        <restriction key="ocEmail" value="true"/>
    </restrictions>
    <actions />
    <block id="0" x="30" y="20" alignment="left" rotation="0">
        <!-- extra space to line up with creation date -->
        <text template="default" font-size="10">Viewed On:  ${currentDate}</text>
    </block>
    <block id="0" x="580" y="30" alignment="right" rotation="0">
        <text template="default" font-size="10">Page ${currentPage} of ${totalPages}</text>
    </block>
</overlay>
```

```xml
<overlay id="engPortraitDraft">
    <restrictions>
        <restriction key="objectType" value="engDemo_document|engDemo_drawing|engDemo_procedure|engDemo_instructional"/>
        <restriction key="engDemo_status" value="Draft" />
    </restrictions>

    <block x="195" y="275" rotation="45" opacity="0.25">
        <text template="draft" />
    </block>
</overlay>
```

```xml
<overlay-config>
    <text-templates>
        <text-template name="default">
            <text font-size="12" font-family="Arial" embed-font="true" font-weight="none" font-style="none" color="black">This is the default text.</text>
        </text-template>
    </text-templates>
    <overlay id="oaSecureViewing">
        <restrictions>
            <restriction key="oaSecureViewing" value="true"/>
        </restrictions>
        <actions/>
        <block id="0" x="50" y="760" alignment="left" rotation="0" opacity="0.25">
            <text template="default" font-size="17" font-family="arial" font-weight="bold" color="red">Viewed by: ${displayName} on ${currentDate~dd-MMM-yyyy}</text>
        </block>
    </overlay>
</overlay-configs>
```

## Override overlay configuration files - AEVT not installed

When AEVT is not installed, you can override the overlay configurations in your [custom AMP].

Follow the steps in [Extension Content Accelerator]({% link content-accelerator/latest/develop/extension-content-accelerator.md %}) in the Content Accelerator documentation.

### How to override overlay configurations in the custom AMP

To override the default overlay configurations, the custom AMP will need to inject a file called `opencontent-override-overlay-spring-config.xml` into the `alfresco/module/com.tsgrp.opencontent` location. This file should contain similar looking beans to this:

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<beans xmlns="http://www.springframework.org/schema/beans" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-2.0.xsd">

  <bean id="overlayConfigBean" class="com.tsgrp.openoverlay.core.XmlConfigFactory" factory-method="createInstance">
    <!-- Spring note - even though these elements are 'constructor-arg' elements, they are really params for the createInstance factory method -->
    <constructor-arg value="path to custom oc overlay configurations.xml" />
    <constructor-arg value="default" />
  </bean>

<!-- iText Overlay Engine-->
  <bean id="openPdfEngine" name="overlayEngine" class="com.tsgrp.openoverlay.openpdf.OpenPdfOverlayEngine" init-method="onInit">
    <property name="overlayConfig">
      <ref bean="overlayConfigBean" />
    </property>
  </bean>
</beans>
```

See the above section [Creating a new Overlay](#creating-a-new-overlay) for instructions on building new overlay beans as well as additional overlay examples. To override an existing overlay configuration and make changes to it, just make a copy of the overlay bean you wish to override and maintain the bean id of the original overlay bean. Then, make any desired changes and this override file will override the existing overlay configurations.

## Override overlay configuration files - AEVT installed

This section only applies to installations that include AEVT (most do not). This section explains how to override the overlay configuration files within our AEVT application (formerly OAT).

AEVT loads these overlay configuration override files via the GET REST endpoint `/configs/assetFile` within the `RESTConfigService`. This returns the `.zip` file that holds all the overlay configuration override files. These files are placed within the temporary directory of whatever Tomcat is running AEVT, and reference (or pointed to) so that OpenOverlay knows to use these files instead of the `oc-overlay-config.xml` file within the Tomcat classpath (ex: `tomcatHome/shared/classes`), if there is one.

There are two ways that the overlay configuration override files are used within AEVT:

1. On startup of AEVT, there is a scheduled job that runs only on startup.

    See [Override overlay configuration files - first time use](#override-overlay-config-files-for-the-first-time)

2. Calling an AEVT REST endpoint called `optimus/refreshOverlayConfigOverrides`.

    See [Update or version existing overlay configuration overrides](#update-or-version-existing-overlay-config-overrides)

### Override overlay configuration files - first time use

#### Turn on override

In order to let AEVT know that you want to override the overlay configuration files, simply switch the property `optimus.enableOverlayConfigOverride` to `true`, within the `application.properties`. To override the `application.properties`, place a file called `application.properties` (that will contain all the properties you want to override) on the Tomcat classpath (for example, in the `tomcatHome/shared/classes` directory).

```xml
optimus.enableOverlayConfigOverride=true
```

In order for AEVT to use your overrides, you also need to set useOverrideOverlayConfigs to `true` in the `application.properties` file.

```xml
optimus.useOverrideOverlayConfigs=true
```

#### Configure overlay overrides

Once you enable the overlay configuration override, you have to add the overlay override ZIP file in the correct place within the repository by following these steps.

1. Create the `oc-overlay-config-override.xml`:

    > **Note:** The naming of this file is crucial as the new enhancements to AEVT specifically look for this specific file name overlay configuration XML.

    * You can create the `oc-overlay-config-override.xml` like any other `oc-overlay-config.xml`.

      See the OpenOverlay XML configuration section above for additional details on configuring your overlay.

    * However, remember anything in the `oc-overlay-config-override.xml` will be used instead of `oc-overlay-config.xml` entirely, since it overrides this file.

2. Change any `classPath` with `tempPath` in the overlay configuration XML file:

    * One important change within the `oc-overlay-config-override.xml` is the for pointing to the location of the image files. Typically, in the `oc-overlay-config.xml` this would be denoted by `classpath:@imagesBase@ocforms-header-logo.png`.
    * Now, use the `tempPath` followed by whatever you named the overlay configuration override ZIP file then the name of the asset/image like normal. Here is an example of what is should look like:

    ```xml
    <image file="tempPath:oc-overlay-override-files/ocforms-header-logo.png" scale="23%"/>
    ```

3. Find or create the assets folder:

    * We have the ability to configure different asset files within the application when they are placed under an `Assets` folder.
    * However, only assets that will override the default assets will be placed within this folder. So, it is possibly to not have this `Assets` folder. 
    * If the folder path does not exist in the repository, create it now. The folder path needed in the repository is `hpi > default > Assets`
        * Note that this path assumes the appId is configured to the default (`optimus.overlayConfigOverrideAppId=default`) if you are overriding this value, you will need to update this path to reflect that.

4. Name the overlay configuration override ZIP file:

    * Naming is important within the `Assets` folder as AEVT will look for a particular ZIP name. This ZIP name is configurable within the `application.properties`. The default ZIP name is `oc-overlay-override-files`.

    ```xml
    optimus.overlayConfigOverrideZipName=oc-overlay-override-files
    ```

5. Upload overlay configuration override ZIP file:

    * Upload the overlay configuration override ZIP file into the Assets folder in the repository.

6. Check other notable configuration properties:

    * There are a couple other notable configuration properties that need to be set.

    * **openContentUrl**: the openContentUrl will be exactly what the name indicates, the URLthat points to OpenContent (for example, `http://localhost:8080/alfresco/OpenContent`). This is important for how AEVT needs to communicate with OpenContent.

    * **tempDirForFilesCachedFromNas**: the name is a little deceiving for how we are using it here, but it is defining what directory should we use as the temporary directory (for example, `C:/apacheHome/temp`). The `temp` directory is where these overridden overlay configuration files are placed.

    ```xml
    optimus.tempDirForFilesCachedFromNas=C:/Apache/apache-tomcat-8.5.45-oat/temp
    optimus.openContentUrl=http://localhost:8080/alfresco/OpenContent/
    optimus.overlayConfigOverrideZipName=oc-overlay-override-files
    ```

7. Restart ACS:

    A job runs on startup to pull in the updated overlay configurations.

### Update or version existing overlay configuration overrides

The overlay configuration override file has been set and at this point you want to make changes to it. Follow the steps below.

1. Update the overlay configuration override ZIP file:

    * To make changes, simply follow ([step 5 in Configure Overlay Overrides](#configure-overlay-overrides)) to re-upload the configurations or re-upload the overlay configuration override file within the repository.

2. Clear the OC cache:

    * The asset files are cached for faster retrieval time. This is an issue when an update needs to be made to the overlay configuration override ZIP file, though.
    * Run this OC endpoint to refresh the caches: `/cache/refreshEagerCaches` by supplying an **administrator's ticket**
    * Example of endpoint call: `http://localhost:8080/alfresco/OpenContent/cache/refreshEagerCaches?ticket=`

3. Run the AEVT refresh endpoint:

    * Once the following update was made to the overlay configuration override ZIP file within the `Assets` folder, you can run the AEVT GET endpoint `/optimus/refreshOverlayConfigOverrides` to refresh the overlay configuration override files. If successful, this deletes any existing overlay configuration override files within the temp directory and put these updated ones in the temp directory.
    * The GET endpoint has no parameters. Here is an example of the endpoint: `http://localhost:7080/oat/optimus/refreshOverlayConfigOverrides`.
---
title: AEV performance tuning
---

Alfresco Enterprise Viewer (AEV) relies heavily on progressive transformations of PDF to PNG content to generate its premium user experience. These transformations incur the vast majority of system load, therefore, performance tuning generally focuses on the load use cases below:

* Loading native or renditioned content from the repository (full binary)
* Transformation of individual page(s) of PDF to PNG at specific resolution

To understand what requires performance tuning, here is a step by step description of what happens when a user loads a document in AEV (simplified for performance tuning purposes):

* The browser makes a request to OpenContent for binary content, properties, associated annotation information.
* If the binary content is cached (keyed on object id and modify date), return cached binary content.
* If the binary content is not cached, fetch using ECM API.
* Once a user has loaded Enterprise Viewer, individual pages are viewed in the browser as PNGs. These PNGs are transformed on demand as the user scrolls through the document pages. The application requests individual page transformations at the following times:
  * Viewing current page
  * Precaching nearby pages (within a preconfigured range)
  * Progressively scaled different resolution images for gracefully degraded view experience
  *Page resize events

As the transformation requests require page-specific transformation events, the current iteration of the Alfresco T-Engine framework does not support the needs of AEV. Thus, transformations are performed by default in the server hosting the OpenContent REST API (typically the ACS server node). See the "AEVT" section below for an alternative for extreme scaling requirements.

Here are the configurable options that may be set in an override properties file, or ACA Extension AMP, that can assist in troubleshooting and tuning performance issues related to the PDF->PNG transformations:

```text
# pdfium transformation default property values.

# The path to the installation of pdfium to use to transform PDFs to PNGs. NOTE: This path is only used for non window systems
# The pdfium windows build is included in OC
pdfium.path=/opt/pdfium

# A commas separated list of options to be passed into the pdfium command. See https://pdfium.googlesource.com/pdfium/ for more info.  For example: use `-A 0` for turning off anti-alias
pdfium.options=

# True if this is being run in debug mode and a temporary file should be created for pdfium's stderr stream & command, false otherwise.
pdfium.debugMode=false

# The most pdfium transformation threads that can be running at a single time.  Setting this property to 0 disables thread limiting.
pdfium.maxThreadCount=5

# The maximum number of pdfium transformations that will back up into the queue.  Unused if maxThreadCount is not defined.
pdfium.maxQueueSize=100

# The maximum idle time (in milliseconds) a thread will be kept alive. Unused if maxThreadCount is not defined.
pdfium.threadKeepAliveTime=5000

#Can be set to kill a Linux thread after a certain amount of time.. ex 10s, 5s, 1s.
pdfium.threadTimeout=5s

# Can be set to send a brute force kill in Linux after a certain amount of time.. ex 10s, 5s, 1s of sending original kill signal.
pdfium.threadKillAfter=5s

# This is a basic regex to allow any character to be passed in, this should be overriden by project
# ^\\/nas\\/vault\\d+\\/alf_data\\/contentstore\\/\\d+\\/\\d+\\/\\d+\\/\\d+\\/\\d+\\/((?!(.*[;<>|]+.*))(?!(.*&&.*))(?!(.*\\$\\(.*))(?!(.*\\|\\|.*))).+
# This is an example that requires the path to start with /nas/vault##/alf_data_contentstore/##/##/##/##/document-name without allowing && $( || | ; as they are command injection threats in linux

pdfium.pathRegexPattern=.+

#The max amount of processes to use when transforming content.
pdfium.maxProcessCount=4
```

## Ehcache

Handles binary caching of pre and post transformed content.

Some General places to look to improve your specific production environment are to properly size the OpenContent heap and caches are in `ehcache.xml`. If your usage patterns are that users don't end up coming back to view the same documents multiple times, you will likely want MORE `oc-content` and `oc-document-overlays` since that is the raw byte[] of the content that the transformation agent keeps going to each time to get the content rather than having to go to the repository each time. `oc-pages` isn't as important in this case since the browser will cache most of the pages anyways.

```xml
 <!-- cache for the content of our objects -->
 <cache name="oc-content" eternal="true" maxBytesLocalHeap="150M"
  maxBytesLocalDisk="5G" memoryStoreEvictionPolicy="LRU">
  <persistence strategy="localTempSwap" />
 </cache>

 <!-- cache for the page transformations from PDFs to PNG for our objects -->
 <cache name="oc-pages" eternal="true" maxBytesLocalHeap="250M"
  maxBytesLocalDisk="5G" memoryStoreEvictionPolicy="LRU">
  <persistence strategy="localTempSwap" />
 </cache>

 <!-- cache for the overlays of our objects -->
 <cache name="oc-document-overlays" eternal="true"
  maxBytesLocalHeap="50M" maxBytesLocalDisk="5G"
  memoryStoreEvictionPolicy="LRU">
  <persistence strategy="localTempSwap" />
 </cache>
```

Optionally, in the case of "single view" usage of document, local storage can be disabled entirely. See below XML for suggested configuration:

```xml
<ehcache xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:noNamespaceSchemaLocation="../config/ehcache.xsd"
    maxBytesLocalHeap="3g">

    <!-- where to store the files written to disk on overflow -->
    <diskStore path="java.io.tmpdir"/>
    
    <!-- cache for the content of our objects -->
    <cache name="oc-content"
        maxBytesLocalHeap="1g"
        eternal="true"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="none" />
    </cache>
    
    <!-- cache for the page transformations from PDFs to PNG for our objects -->
    <cache name="oc-pages"
        maxBytesLocalHeap="1g"
        eternal="true"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="none" />
    </cache>
        
    <!-- cache for the overlays of our objects -->
    <cache name="oc-document-overlays"
        maxBytesLocalHeap="1g"
        eternal="true"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="none" />
    </cache>
            
</ehcache>
```

## PdFium / GhostScript / MuPDF

Every page of a document is transformed using either PdFium, GhostScript, or MuPDF. So anything that can be done to improve the performance of this process will help.

* By default, AEV uses PDFium. A third-party license may be required for using MuPDF or GhostScript.
* Use a solid state drive (SSD) for your temporary directories.
* Even better performance, use a [RAM Disk/tempfs](https://en.wikipedia.org/wiki/Tmpfs){:target="_blank"} like `/dev/shm` as that is faster than even an SSD.

## AEV performance

Enterprise Viewer has a configuration to toggle if a "low-res" and a "high-res" image are requested for a page. Toggle the `progressiveReloadSteps=0` property to reduce the load on the system and only load the high-resolution rather than both. There are times that the high-res call could complete before the other call if the system is really bogged down, so the less load that can be triggered in general has been found to have a positive impact at peak usage.

## AEV transformations

Should the embedded OpenContent transformations not scale to the level necessary for your implementation, the "Alfresco Enterprise Viewer Transformation" application can operate at scale. This application is also known as "Alfresco Enterprise Viewer Transformations", or AEVT for short. See [Installing Alfresco Enterprise Viewer Transformer]({% link enterprise-viewer/latest/install/aevt.md %})

AEVT/OAT is used on Alfresco PaaS.
---
title: Configure suggested redaction
---

The suggested redaction functionality uses regular expression (RegEx) patterns. You can configure these patterns by overriding the bean with id `RedactionRegexAttrMap`, as described below.

1. Create an Extension Content Accelerator AMP.

    Follow the steps in [Extension Content Accelerator]({% link content-accelerator/latest/develop/extension-content-accelerator.md %}) in the Content Accelerator documentation, and then return to this page.

2. Locate or create the `alfresco/module/com.tsgrp.opencontent` path.

3. Locate or create the XML file `opencontent-override-overlay-spring-config.xml` using the following example.

    The out-of-the-box suggested redactions bean default to:

    ```xml
    <bean id="RedactionRegexAttrMap" class="com.tsgrp.opencontent.universal.util.RedactionTextStripper">
      <property name="redactionRegexAttrMap">
        <map>
          <!-- Regex patterns must consist of exactly two capturing groups, with the second group containing the text to be redacted. -->
          <entry key="SSN" value="(SSN: )?(\d{3}-\d{2}-\d{4})"/>
          <entry key="Phone Number" value="(Phone Number: )?((?:\+?1[-.])?(?:\(?\d{3}\)?)?[-. ]?\d{3}[-.]\d{4})"/>
          <entry key="Credit Card" value="(Credit Card Number:[ ]*)?((?:\d{4}[ -]?){4})"/>
          <entry key="Name" value="([Nn]ame:[ ]*)([A-Za-z]+ [-'A-Za-z]+)"/>
        </map>
      </property>
    </bean>
    ```

4. You can override the pattern to include for suggested redactions by modifying the bean in `opencontent-override-overlay-spring-config.xml`.

    Add or remove as many patterns are you need.

5. Provide a key-value pair similar to the above example to set your own custom redaction suggestion based on your RegEx pattern setup.
---
title: Supported languages
---

* DE - German
* EN - English
* ES - Spanish
* FR - French
* IT - Italian
* JA - Japanese
* NL - Dutch
---
title: Embed AEV in ADF
---

You can integrate Enterprise Viewer (AEV) into the Alfresco Application Development Framework (ADF) application by replacing or overriding the default ADF Viewer component behavior.

## Sample ADF AEV application configuration

Include the following block in your application's `app.config.json` file and change as needed for your local environment:

```json
"alfresco-enterprise-viewer": {
    "$version": "1.0.0",
    "enabled" : true,
    "properties": {
      "endpoints": {
        "aev": "/OpenAnnotate",
        "aevVideo": "/OpenAnnotateVideo"
      },
      "supportedMimetypes": {
        "videos": [
          "video/mp4"
        ]
      },
      "aevVideoSeperate" : false,
      "alfrescoDocumentStorePrefix": "workspace://SpacesStore/",
      "extraAEVUrlParams" : {}
    }
  }

```
---
title: Integrations
---

## REST API

* Authentication
  * [Normal login](#normal-login)
  * [External login](#external-login)

### Normal login

Endpoint to perform a log in operation using the provided parameters. Redirects to viewer.htm after successful authentication.

* **URL**  
`/login.htm`  
* **Method**  
`POST`  
* **Required Parameters**
  * `username`: {String} the username to use for logging in
  * `password`: {String} the password to use for logging in (not encrypted)
* **Optional Parameters**
  * `docbase`: {String} the docbase to log in to.
  * `docId`: {String} the document id that should be passed to viewer.htm after a successful log in
  * `docIdList`: {String} a list of document ids (comma separated) to attach to the viewer.htm after a successful login
  * `parentId`: {String} the parent id of the document to view in the viewer.htm after a successful login.
  * `mode`: {String} the mode that AEV should open into. Either **openviewer, pageSelect, readOnly, edit, signature, annotation, redact** or **false** (default) for unspecified (which will launch the viewer in annotation mode).
  * `redactionMode`: {Boolean} set to **true** if we are redacting the document as a copy (defaults to **false**).
  * `useLocalStorageForRedaction`: {Boolean} set to **true** if we should saved the unredacted document id and redacted document id in the local storage. `redactionMode` must be set to **true** for this to be used. (defaults to **false**).
  * `pageSelectMode`: {Boolean} set to **true** if we want to open AEV up in page selected mode (defauled to **false**).
  * `pageSelectButtonLabel`: {String} what the button label will be named in the currently selected pages notification in pageSelectMode. `pageSelectMode` must be set to **true** for this to be used.
  * `pageSelectEventName`: {String} the name of the event that will happen when the currently selected pages notification button is clicked. `pageSelectMode` must be set to **true** for this to be used.
  * `emptyPageSelectionValid`: {Boolean} set to **true** if it is valid to select no pages (defaults to **false**).
  * `startupSearch`: {String} the search term that the user wants to search on when first loading the document.
  * `currentPage`: {Integer} the page that the user should be jumped to when they first open the document.
  * `viewerTitle`: {String} the title that the viewer page will display after successful login.
  * `viewerMessage`: {String} a message that the viewer page will display after successful login.
  * `redirectedToOV`: {Boolean} set to **true** if the user is being redirected to OpenViewer because of permissions (defaults to **false**).
* **Success Response**
  * Code: 200
  * User will be routed to the viewer.htm page within AEV.
* **Sample Call**

    Expected result - the admin will login successfully and be redirected to the AEV viewer with the document supplied as the `docId` parameter open to page 5 and with 3 documents showing in the document list sidebar.

    ```text
    https://{server}/OpenAnnotate/login.htm
    ```

* **Form-data body**
  * `username`: admin
  * `password`: admin
  * `docId`: workspace://SpacesStore/c47ef310-e731-427c-afc0-af8821c40890
  * `docIdList`: workspace://SpacesStore/64e76092-4b32-4291-aa78-7b6ede902bab,workspace://SpacesStore/5d09828e-7efd-4387-8a44-0c83c8fb8a0f,workspace://SpacesStore/97a859af-4b38-479e-bbc5-5f945a8e551
  * `currentPage`: 5

### External login

Endpoint to login from an external source with a username. The endpoint expects a valid ticket to be provided. If a valid ticket is not provided, the user will be redirected to the login screen to generate a new, valid ticket.  This endpoint is most commonly used through an iframe of a parent application that is embedding AEV, like the Alfresco Content Accelerator.

* **URL**  
`/login/external*`  
* **Method**  
`GET`  
* **Required Parameters**
  * `ticket` : {String} Ticket from the current session.
  * `username`: {String} the username to use for logging in
* **Optional Parameters**
  * `docbase`: {String} the docbase to log in to.
  * `docId`: {String} the document id that should be passed to viewer.htm after a successful log in
  * `docIdList`: {String} a list of document ids (comma separated) to attach to the viewer.htm after a successful login
  * `parentId`: {String} the parent id of the document to view in the viewer.htm after a successful login.
  * `mode`: {String} the mode that AEV should open into. Either **openviewer, pageSelect, readOnly, edit, signature, annotation, redact** or **false** (default) for unspecified (which will launch the viewer in annotation mode).
  * `redactionMode`: {Boolean} set to **true** if we are redacting the document as a copy (defaults to **false**).
  * `useLocalStorageForRedaction`: {Boolean} set to **true** if we should saved the unredacted document id and redacted document id in the local storage. `redactionMode` must be set to **true** for this to be used. (defaults to **false**).
  * `pageSelectButtonLabel`: {String} what the button label will be named in the currently selected pages notification in pageSelectMode.
  * `pageSelectEventName`: {String} the name of the event that will happen when the currently selected pages notification button is clicked.
  * `emptyPageSelectionValid`: {Boolean} set to **true** if it is valid to select no pages (defaults to **false**).
  * `startupSearch`: {String} the search term that the user wants to search on when first loading the document.
  * `startupPage`: {Integer} the page that the user should be jumped to when they first open the document.
  * `viewerTitle`: {String} the title that the viewer page will display after successful login.
  * `viewerMessage`: {String} a message that the viewer page will display after successful login.
  * `redirectedToOV`: {Boolean} set to **true** if the user is being redirected to OpenViewer because of permissions (defaults to **false**).
* **Success Response**
  * Code: 200
  * User will be routed to the viewer.htm page within AEV.
* **Sample Call**

    Expected result: the admin will be successfully authenticated and be redirected to the AEV viewer with the document supplied as the `docId` parameter open.

    ```text
    https://{server}/OpenAnnotate/login/external.htm?username=admin&ticket=TICKET_6dd55060d45cc05957b16da3becd9938f9414b9e&docId=workspace://SpacesStore/c47ef310-e731-427c-afc0-af8821c40890
    ```

## Features

* [Document list sidebar view](#document-list-sidebar-view)
* [Startup search](#startup-search)

### Document list sidebar view

The purpose of this feature is to allow a user to easily navigate between documents in AEV by displaying a list of documents in a sidebar tab. In order for this tab to show up, the `viewer.htm` request must contain the `docIdList` parameter with a comma separated list of document ids.

#### Example

Document ID List Parameter (Alfresco):

```text
docIdList=workspace://SpacesStore/d7de806c-9aa6-4b14-8ff2-95b902d33d5d,workspace://SpacesStore/0ed0e588-8c70-42ad-8e77-2211e4bdd9ce,workspace://SpacesStore/0f39c66d-f414-4a06-861e-c91a3ff12335
```

Document ID List Parameter (Documentum):

```text
docIdList=090130da806908e9,090130da806908e2,090130da806908e5
```

Full request:  

```text
https://{server}/OpenAnnotate/viewer.htm?docId=workspace://SpacesStore/fbe65690-62b2-4275-8655-f9f08778c12a&username=admin&docIdList=workspace://SpacesStore/d7de806c-9aa6-4b14-8ff2-95b902d33d5d,workspace://SpacesStore/0ed0e588-8c70-42ad-8e77-2211e4bdd9ce,workspace://SpacesStore/0f39c66d-f414-4a06-861e-c91a3ff12335
```

Expected Result: the admin will be redirected to the AEV viewer with the document supplied as the `docId` parameter and with 3 documents showing in the document list sidebar.

#### Configuration

**Sidebar**

By default, the document list view is enabled in the left sidebar. This can be changed by adding/removing `documentList` from the `leftSidebarModules` or `rightSidebarModules` in the `defaults.properties` file.

**Popup Notification**

When one or more invalid document ids have been passed in (causing the call to `/openContentObjects` to fail), a popup notification will be displayed in the bottom right-hand corner of the viewer by default. This can be changed by adding/removing `displayDocumentListFailed` from the `enabledPopupNotifications` configurable in the `default.properties` file.

### Startup search

The purpose of this feature is search for a term when AEV initially loads. This will allow for results to appear highlighted in the document and in the search results tab on first load.

#### Example: Startup

Startup  Search Parameter:

`startupSearch=termToSearchOn`

Full request:  

```text
https://{server}/OpenAnnotate/viewer.htm?docId=workspace://SpacesStore/fbe65690-62b2-4275-8655-f9f08778c12a&username=admin&startupSearch=termToSearchOn
```

Expected Result: Once the page loads, any matches on the term to search are highlighted in the document and search results tab.
---
title: Integrate AEV with Alfresco Application Development Framework
---

AEV can also be integrated with an existing ADF application.

1. Install Enterprise Viewer as per the [installation guide]({% link enterprise-viewer/latest/install/index.md %}) (either as part of the Alfresco Tomcat or as a separate Tomcat/Java application server).

2. Update or fork the existing document preview action to open a link in an IFrame to the Enterprise Viewer external link using the nodeId as parameter.

3. If on a separate application server, update the proxy rules for your ADF application to ensure the Enterprise Viewer external link may be accessed without CORS errors.
---
title: Install Alfresco Enterprise Viewer Transformer (optional)
---

> **Important:** AEVT (formerly known as "OAT") is not recommended for most installs of AEV. AEVT makes an environment more complex and should only be deployed when needed.

## What is AEVT

AEV requires individualized PDF->PNG page transformations, which is something beyond the capabilities of the current feature set of the Alfresco Transform Service. The OpenContent Alfresco Module Package (AMP) module supports performing these types of transformations, but the downside is that those transformations occur on the ACS container (similar to legacy Alfresco Transformation Services). For the vast majority of deployments, this is sufficient from a performance and infrastructure perspective.

AEVT divorces the page transformation load from the ACS container by installing a completely separate component (or components) based on Spring Boot that is horizontally and vertically scalable. A reverse proxy is required to intercept and redirect requests to the separate components when the AEV application makes a request to the `alfresco/OpenContent/openannotate/transform*` URL. There are significant security, architecture, scalability, and general complexity concerns that all must be answered when deploying AEVT.

## When to deploy AEVT

AEVT is recommended when:

* There is a need to scale AEV page transformation process separately from ACS instance(s)

* There are large amounts of concurrent users viewing documents, which would put CPU pressure on the ACS instance if AEVT is not used

> **Note:** Customers can always skip using AEVT, monitor usage and CPU on the ACS server, and add AEVT into the environment if needed at a later time. This is recommended over installing out without a firm need.

## AEVT architecture

See the below graphic for how AEVT can be added to an AEV installation.

![AEVT Architecture]({% link enterprise-viewer/images/aevt_architecture.png %})

## AEVT install

### Install webapps

This sections walks through how to install the Enterprise Viewer Transformer web application.

1. Install Apache Tomcat.

    See [https://archive.apache.org/dist/tomcat](https://archive.apache.org/dist/tomcat){:target="_blank"}.

2. Copy the `oat.war` file into the `TOMCAT_HOME/webapps` directory.

   You can find this WAR file in the `Web Applications` folder of the `alfresco-enterprise-viewer-package` ZIP file.

3. Configure Tomcat for shared classpath loader as well as encoded slashes:

   * Edit the `TOMCAT_HOME/conf/catalina.properties` file and enable the `shared.loader` by adding the following line (if not already there):

   ```text
   shared.loader=${catalina.base}/shared/classes,${catalina.base}/shared/lib/*.jar
   ```

4. Configure Tomcat ports in the `TOMCAT_HOME/conf/server.xml`:

   Configure the connector, server, and redirect ports to not conflict with the Alfresco Tomcat or any other Tomcats (example below):

   * Set Connector - `port="9090"` (defaults to `8080`)
   * Set Connector - `redirectPort="9443"` (defaults to `8443`)
   * Set Server - `port="9005"` (defaults to `8005`)

5. Start Tomcat.

### Configure OpenContent to Pass the contentPath

AEVT is enabled by setting up a property in OpenContent that tells OC to pass back the `contentPath` of the file on the `getDocumentInfo` call that Enterprise Viewer makes. The property in OpenContent to enable is `annotation.useContentFilepathForTransformations=true`. Once that property is enabled, the AEV frontend has access to the contentPath since it will be returned in the getDocumentInfo call (for example, `/mnt/nas/alf_data/contentstore/2019/05/15/8/3/26/d38b7e22-816e-4bbd-b7ff-f9b164edcfee.bin`).

To enable this property:

1. Stop Alfresco.

2. Set the following property in the `opencontent-override-placeholders.properties` found on the `/alfresco` classpath, for example, in the `ALFRESCO_HOME/tomcat/shared/classes/alfresco/module/com.tsgrp.opencontent/` directory:

    * `annotation.useContentFilepathForTransformations=true`

3. Delete the current Alfresco deployed WAR files:

   Navigate to the `ALFRESCO_HOME/tomcat/webapps` directory and delete the `alfresco` folder.

4. Start Alfresco.

### Proxy calls to go to AEVT

The next step is to configure a proxy so that calls that previously would be going to `/OpenContent/openannotate/transform?`, would now go to AEVT instead.

Below is the example ProxyPass/forwarding rule on Apache Httpd. Note that you can proxy this path in whatever makes the most sense in your setup as long as the same proxy rules apply.

> **Important:** This proxy pass must occur BEFORE any other rules that reference the same host (since a rule with `/alfresco` will match and overrule any rules under it that are more specific).

```text
#Proxy all requests for AEVT
ProxyPass /alfresco/OpenContent/openannotate/transform http://oat-servername:8080/oat/optimus/transform
ProxyPassReverse /alfresco/OpenContent/openannotate/transform http://oat-servername:8080/oat/optimus/transform
ProxyPass /alfresco/OpenContent/openannotate/getThumbnails http://oat-servername:8080/oat/optimus/getThumbnails
ProxyPassReverse /alfresco/OpenContent/openannotate/getThumbnails http://oat-servername:8080/oat/optimus/getThumbnails
```

For example, this request from AEV:

`/OpenContent/openannotate/transform?id=workspace://SpacesStore/82b15c11-b09a-4ab5-8b3a-058029296969&pageNum=3&resolution=64&lastModified=1560972048092&imageWidth=843&docWidth=612&docHeight=792&contentPath=/mnt/nas/alf_data/contentstore/2019/05/15/8/3/26/d38b7e22-816e-4bbd-b7ff-f9b164edcfee.bin`

would now be proxied to:

`/oat/optimus/transform?id=workspace://SpacesStore/82b15c11-b09a-4ab5-8b3a-058029296969&pageNum=3&resolution=64&lastModified=1560972048092&imageWidth=843&docWidth=612&docHeight=792&contentPath=/mnt/nas/alf_data/contentstore/2019/05/15/8/3/26/d38b7e22-816e-4bbd-b7ff-f9b164edcfee.bin`

### (Optional) Map calls between OpenContent and AEVT

Sometimes in may be beneficial to map the calls between OpenContent and AEVT, so the same calls can be made to the OpenContent and AEVT server. This can be accomplished on Tomcat 8+ through extra configuration, without having to install an additional proxy.

On the OAT Tomcat, add the following line to your `conf/server.xml` file:

```xml
...
<Host name="localhost"  appBase="webapps" unpackWARs="true" autoDeploy="true">
...
    <!-- The following will allow native Tomcat url rewriting -->
    <Valve className="org.apache.catalina.valves.rewrite.RewriteValve" />
...
</Host>
```

Then create a new `rewrite.config` file in your `conf/Catalina/localhost` directory. Create this directory if it does not yet exist. The file should contain:

```text
RewriteRule ^/alfresco/OpenContent/openannotate/(.*)$ /oat/optimus/$1 [L]
```

This will cause all incoming to calls from `/alfresco/OpenContent/openannotate` to get mapped to `/oat/optimus`. Thus both the OpenContent and AEVT servers can accept calls to `/alfresco/OpenContent/openannotate`. URL rewriting is no longer necessary at the Proxy/Load Balancer level.

If you are not on Tomcat 8+, setting up the [Tuckey UrlRewriteFilter](https://tuckey.org/urlrewrite){:target="_blank"} may be an option. Or you can setup an additional proxy on the AEVT server.

## AEVT configuration

Your deployment must include an `application.properties`. The `application.properties` can be placed on the `/oat` classpath (for example: `TOMCAT_HOME/shared/classes` or whatever was configured in the shared loader in the webapps install above).

Some of the common properties that will likely need configuration in the `application.properties` as they typically change between environments are:

```java
server.port=8080
# Configs Independent of Transformer
optimus.tempDirForFilesCachedFromNas=/opt/tmp
# if set to true will have the transformer contact OpenContent to determine if the user has permissions for the document
optimus.enableRepositorySecurity=false
# URL the transformer should use to contact OpenContent
optimus.openContentUrl=http://alfresco:8080/alfresco/OpenContent
# Default transformer to user
optimus.defaultTransformer=pdfium
pdfium-configs.executablePath=/opt/pdfium
```

## Limitations

AEVT only supports Content Services installations that have a single content store. If multiple content stores are being used, AEVT will not operate properly.

AEVT reads content directly from a content store or S3. This means that installations where the content is stored elsewhere cannot be implemented for use with AEVT. For example if a document is stored in Content Services as a link, which navigates to another source system, AEVT will not work properly.
---
title: Install Enterprise Viewer
---

Use this information to install the Enterprise Viewer. If you're installing both the Content Accelerator and the Enterprise Viewer, its recommended that you start with the Content Accelerator install guide.

## Prerequisites

> **Important:** If the Enterprise Viewer license you have been issued with is a `GROUP` license you must create a group within Alfresco that contains the people you want to have access to the Enterprise Viewer. This new group must be named: `aev_users`. All the people outside of this group will continue to see the default PDF viewer. If this is done after the installation of the Enterprise Viewer, then you must restart Tomcat for the changes to take effect.

### Distribution zips

You can install the Enterprise Viewer using a distribution ZIP. Download the following ZIP file from [Hyland Community](https://community.hyland.com/products/alfresco){:target="_blank"}:

* `alfresco-enterprise-viewer-package-4.0.x.zip`

### Java

Enterprise Viewer requires Java 11 or above. Consult your repository of choice for more detailed requirements. If you are using Java 17, refer to our [Java 17 support guide]({% link enterprise-viewer/latest/install/java-support.md %}).

### Alfresco repository version

See the [Supported Platforms]({% link enterprise-viewer/latest/support/index.md %}) for more information.

Make sure you have the correct version of the Enterprise Viewer package for your Content Services version. If you are unsure, please contact Hyland Support.

### Operating system requirements

Operating system and libraries for the target server machine:

* Windows: Windows Server 2016 or newer
* Linux: CentOS, Ubuntu, RHL, Amazon Linux
  
## Install proxy

### Do you need a web proxy?

When installing AEV you have 2 options:

| Option 1 | Deploy AEV to the Alfresco Tomcat. <br><br>Skip to the [OpenContent install]({% link enterprise-viewer/latest/install/index.md %}#installoc) section since no proxy will need to be installed. |
| Option 2 | *Preferred.* For production deployment. <br><br>Deploy AEV to a separate Tomcat instance. In this case, you must complete the following steps to setup a proxy. |

### Proxy setup

The following routes must be proxied to their respective ports and applications in order for AEV to work correctly. SSL is recommended at a minimum at the Proxy layer for production installations.

* `{Application Base URL}/alfresco`
* `{Application Base URL}/share`
* `{Application Base URL}/OpenAnnotate`
* `{Application Base URL}/oat` (if installed)

When installing a proxy please note that you are not limited to using Apache or NGINX. These are just two common options which we cover example installs of below. As long as the above routes are proxied appropriately you can move onto the [AEV install]({% link enterprise-viewer/latest/install/index.md %}#install).

> **Important:** If you've already completed the ACA install guide and setup a proxy as part of that installation, you can just add the following routes to that proxy configuration and restart the proxy:
>
> * `{Application Base URL}/OpenAnnotate`
> * `{Application Base URL}/oat` (if installed)
>
> Next, go to the [AEV install]({% link enterprise-viewer/latest/install/index.md %}#install).

### Example proxy install 1 - Apache HTTPD on Windows

1. Install Apache `httpd`.

   Download the binaries from [https://www.apachelounge.com/download/](https://www.apachelounge.com/download/){:target="_blank"}.

   Install Apache to `C:\Apache\Apache24` (change to your desired version as appropriate). This is referred to as `${apache.home}` below.

   * Navigate to `${apache.home}\conf` and open up `httpd.conf`
   * Find the line that has ServerRoot on it  
      * It should default to something like `ServerRoot "c:/Apache24"`
      * Change the ServerRoot to where you extracted Apache
   * If you would like to install as a service, consult the Readme.txt file that comes with the installation.

2. Modify `httpd.conf` (`${apache.home}\conf\httpd.conf`) to load the Virtual Hosts configuration file, and the Proxy, ProxyAJP, and Rewrite modules. **Uncomment** the following lines:

    ```text
    Include conf/extra/httpd-vhosts.conf
    LoadModule proxy_module modules/mod_proxy.so
    LoadModule proxy_ajp_module modules/mod_proxy_ajp.so
    LoadModule proxy_http_module modules/mod_proxy_http.so
    LoadModule rewrite_module modules/mod_rewrite.so
    LoadModule access_compat_module modules/mod_access_compat.so
    LoadModule authz_host_module modules/mod_authz_host.so
    LoadModule filter_module modules/mod_filter.so
    ```

3. Modify the `httpd-vhosts.conf` file (`${apache.home}\conf\extra\httpd-vhosts.conf`).

    * Remove the sample virtual hosts from the file by deleting the `<VirtualHost *:80>` sections.

4. Add a new virtual host to your `vhosts` configuration file that points to the Alfresco Tomcat and Tomcat running AEV by adding the following lines.

    * Make sure to update server names and paths as needed (for example, replace anything surrounded by `${})`).
    * Make sure you also update the `proxyPass` sections at the bottom to proxy the appropriate routes.

        ```xml
        <VirtualHost *:80>
        ServerName ${your-server-name}
        ErrorLog "logs/${your-server-name}-error.log"
            CustomLog "logs/${your-server-name}-access.log" common
            ServerAlias ${your-server-name}

            AllowEncodedSlashes On
            LimitRequestFieldSize 65536
            ProxyIOBufferSize 65536

            #Optional - these two lines redirect the root URL (/) to /ocms.
            RewriteEngine on
            RewriteRule ^/$ /ocms [PT]

            <Directory />
                Options All
                Order Deny,Allow
                Allow from all
            </Directory>

            ProxyRequests off

            <Proxy *>
                Order Deny,Allow
                Allow from all
            </Proxy>

            <Location />
                Order Deny,Allow
                Allow from all
            </Location>

            # Proxy /alfresco requests to Alfresco's Tomcat
            ProxyPass /alfresco ajp://${your-TOMCAT-server-name}:8009/alfresco
            ProxyPass /share ajp://${your-TOMCAT-server-name}:8009/share
            # OR, use HTTP like this (use AJP in a production environment, as HTTP has more overhead and issues):
            # ProxyPass /alfresco http://{server}:8080/alfresco

            #Proxy all requests at the root to the Tomcat that actually has the application in question ex: 
            ProxyPass / ajp://${your-TOMCAT-server-name}:9090/

            </VirtualHost>
        ```

5. (Re)start the proxy.

   Go to `${apache.home}/bin`, open a command prompt, and run `httpd.exe`.

6. Test the proxy is working properly by opening `http://{server}/alfresco`.

### Example proxy install 2 -  NGINX install on Amazon Linux

Here are some sample steps of installing NGINX as a proxy (steps are done on amazon-linux and may need to be adjusted for other distributions)

1. Install NGINX on the server, for example:

    * `sudo amazon-linux-extras list | grep nginx`
    * `sudo amazon-linux-extras enable nginx1`
    * `sudo yum clean metadata`
    * `sudo yum -y install nginx`
    * `nginx -v`

2. Confirm you can startup NGINX:

    * `sudo systemctl start nginx.service` (start the service)
    * `sudo systemctl reload nginx.service` (reload the service)
    * `sudo systemctl status nginx.service` (check that the status is active)
    * `sudo systemctl stop nginx.service` (stop the service)

3. Configure the proxy:

    * `sudo vi /etc/nginx/nginx.conf`
    * Replace contents of the file with the following (replacing ports and servers and adding additional `proxy_pass` configurations as required).

        ```text
        worker_processes  1;

        events {
        worker_connections  1024;
        }

        http {
        server {
            listen *:80;

            client_max_body_size 0;

            set  $allowOriginSite *;
            proxy_pass_request_headers on;
            proxy_pass_header Set-Cookie;

            # External settings, do not remove
            #ENV_ACCESS_LOG

            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
            proxy_redirect off;
            proxy_buffering off;
            proxy_set_header Host            $host:$server_port;
            proxy_set_header X-Real-IP       $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass_header Set-Cookie;

            # Protect access to SOLR APIs
            location ~ ^(/.*/service/api/solr/.*)$ {return 403;}
            location ~ ^(/.*/s/api/solr/.*)$ {return 403;}
            location ~ ^(/.*/wcservice/api/solr/.*)$ {return 403;}
            location ~ ^(/.*/wcs/api/solr/.*)$ {return 403;}

            location ~ ^(/.*/proxy/alfresco/api/solr/.*)$ {return 403 ;}
            location ~ ^(/.*/-default-/proxy/alfresco/api/.*)$ {return 403;}
            
            # Protect access to Prometheus endpoint
            location ~ ^(/.*/s/prometheus)$ {return 403;}
            
            location /alfresco {
                    proxy_pass http://{server}:8080/alfresco;
            }

            location /share {
                    proxy_pass  http://{server}:8080/share;
            }

            location /OpenAnnotate {
                    proxy_pass http://{server}:9090/OpenAnnotate;
            }

        }
        }
        ```

4. Start the NGINX proxy and confirm it started up correctly:

    ```bash
    sudo systemctl start nginx.service
    ```

    ```bash
    sudo systemctl status nginx.service
    ```

5. Make sure whatever port your proxy is listening on is open to the end user.

   For example: open port `80` if you're using the configuration in our example above.

6. Test the proxy is working properly by opening `http://{server}/share`.

## Install OpenContent {#installoc}

You only need to follow these steps if installing AEV without ACA:

1. Stop the Alfresco server

2. Copy the OpenContent AMP to the Alfresco Content Services installation:

   Navigate to the `ALFRESCO_HOME/amps` directory and copy the `tsgrp-opencontent-{version_info}.amp` to this directory.

   You'll find the AMP file in the `alfresco-enterprise-viewer-package` distribution zip under `Alfresco Artifacts` folder.

   > **Note:** Make sure you are using the correct `tsgrp-opencontent.amp` for your version of Alfresco.

   For example:

   * If using Alfresco Content Services 23.x, use the `tsgrp-opencontent-4.0.0-for-acs23.amp`.

3. From the directory where your Alfresco Tomcat server is installed, run the following command to apply the AMP:

    Linux:

    ```java
    java -jar {ALFRESCO_HOME}/bin/alfresco-mmt.jar install {ALFRESCO_HOME}/amps/tsgrp-opencontent.amp tomcat/webapps/alfresco.war -force
    ```

    Windows:

    ```java
    java\{javaVersion}\bin\java -jar {ALFRESCO_HOME}\bin\alfresco-mmt.jar install {ALFRESCO_HOME}\amps\tsgrp-opencontent.amp tomcat\webapps\alfresco.war -force
    ```

4. Delete current Alfresco deployed WAR files:

   Navigate to the `ALFRESCO_HOME/tomcat/webapps` directory and delete the `alfresco` folder (if it exists).

5. Install license file for OpenConnect:

   Create the `module/com.tsgrp.opencontent/license` folder structure on the `/alfresco` classpath, for example, at `ALFRESCO_HOME/tomcat/shared/classes/alfresco`

   Place a `TextLicense.l4j` file in the `license` directory.

6. Deploy the OpenConnect configuration:

    Create a file called `opencontent-override-placeholders.properties` and put it onto the `/alfresco` classpath, for example, in the `ALFRESCO_HOME/tomcat/shared/classes/alfresco/module/com.tsgrp.opencontent/` folder.
  
    Update the necessary environment variables in the `opencontent-override-placeholders.properties`.

    There are many configurations that can be overridden. These are described later. To start, set the follow property:

     * `oc.email.smtp.host={SMTP host}`

7. Update Tomcat server configuration:

   By default, Apache Tomcat doesn't support UTF-8 characters for languages other than English. To enable support, the `web.xml` and `server.xml` files need to be modified in the deployed Tomcat.

   * When running OpenContent on Tomcat 8+, the `relaxedQueryChars` and `relaxedPathChars` parameters are required on the Connector.
   * If you are using Tomcat older than version 8.5, you may need to add this to `catalina.properties` in your `tomcat/conf` folder: `tomcat.util.http.parser.HttpParser.requestTargetAllow=|{}`.

   Update the following files:

   1. In `${tomcat.home}/conf/web.xml`:

        Uncomment the `setCharacterEncodingFilter` and its mapping in `web.xml` (if not already uncommented):

        ```html
        <!-- ================== Built In Filter Definitions ===================== -->

        <!-- A filter that sets character encoding that is used to decode -->
        <!-- parameters in a POST request -->
        <filter>
        <filter-name>setCharacterEncodingFilter</filter-name>
        <filter-class>org.apache.catalina.filters.SetCharacterEncodingFilter</filter-class>
        <init-param>
            <param-name>encoding</param-name>
            <param-value>UTF-8</param-value>
        </init-param>
        <async-supported>true</async-supported>
        </filter>

        <!-- ==================== Built In Filter Mappings ====================== -->

        <!-- The mapping for the Set Character Encoding Filter -->
        <filter-mapping>
            <filter-name>setCharacterEncodingFilter</filter-name>
            <url-pattern>/*</url-pattern>
        </filter-mapping>
        ```

   2. In `${tomcat.home}/conf/server.xml`:

        Add the following to the connector if not already present:

        * `URIEncoding="UTF-8"`
        * `connectionTimeout="20000"`
        * `maxHttpHeaderSize="32768"`
        * `relaxedQueryChars="{}[]|"`
        * `relaxedPathChars="{}[]|"`

            ```xml
            <Connector port="8080" protocol="HTTP/1.1"
            connectionTimeout="20000"
            redirectPort="8443"
            URIEncoding="UTF-8"
            relaxedQueryChars="{}[]|"
            relaxedPathChars="{}[]|" />
            ```

   > **Note:** In a typical Alfresco installation, the `8080` connector can be modified for HTTP communications and the `443` connector can be modified for `HTTPS` connections.

8. (Optional) This step is only required if using Alfresco Search Services 2.0 or greater:

    1. Navigate to the `SOLR_HOME/solrhome/conf` folder.

    2. In the file `shared.properties`, uncomment the following properties (if not already uncommented):

       * `alfresco.cross.locale.datatype.0={http://www.alfresco.org/model/dictionary/1.0}text`
       * `alfresco.cross.locale.datatype.1={http://www.alfresco.org/model/dictionary/1.0}content`
       * `alfresco.cross.locale.datatype.2={http://www.alfresco.org/model/dictionary/1.0}mltext`

    3. Once the above changes have been made, Solr must be reindexed.

       Stop the Solr process if it is running.

       Clear out the following folder paths:

        * `SOLR_HOME/solrhome/alfresco/index`
        * `SOLR_HOME/solrhome/archive/index`
        * `SOLR_HOME/solrhome/alfrescoModels`

       Start Solr process.

9. Start up Alfresco server.

10. Confirm OpenContent has been installed correctly by accessing `http://{server}/alfresco/OpenContent`.

## Install libraries {#install}

### Install PDFium (optional) {#pdfium}

> **Note:** This step is only needed if using Enterprise Viewer on Linux.

1. Locate the`pdfium.tar.gz` in the `Third Party` folder of the `alfresco-enterprise-viewer-package` ZIP.

2. Unpack the `pdfium.tar.gz` source to a location on your server.

3. Note the path where `pdfium` is installed as `PDFIUM_HOME`.

4. Navigate into the newly unpacked `PDFIUM_HOME` directory.

5. Run the following command from the `PDFIUM_HOME` to ensure `pdfium` was unpacked successfully:

    ```bash
    ./pdfium --help
    ```
  
   The `pdfium` help message is displayed.

### Install FFMPEG (optional)  {#ffmpeg}

> **Note:** This step is only needed if using Enterprise Viewer Video.

1. Download and install an official FFMPEG package from [here](https://ffmpeg.org/download.html){:target="_blank"}.

    Use the latest supported release. Note that the latest Windows release is included in the `Third Party` folder of the `alfresco-enterprise-viewer-package` zip

2. Note the path where FFMPEG is being installed as `FFMPEG_HOME`.

3. Navigate into the newly unpacked FFMPEG directory.

4. Run the following command from the `FFMPEG_HOME` to ensure `ffmpeg` was unpacked successfully:

    ```bash
    ./{FFMPEG_HOME}/ffmpeg --help
    ```

   The `ffmpeg` help message is displayed.

## Configure OpenContent for AEV

> **Note:** You only need to complete this section if you've installed FFMPEG and/or PDFium above.

1. Stop Alfresco.

2. Configure OpenConnect.

    Update the environment variables in the provided `opencontent-override-placeholders.properties`. Deploy the updated file to the `/alfresco` classpath, for example, the `ALFRESCO_HOME/tomcat/shared/classes/alfresco/module/com.tsgrp.opencontent/` directory:

    If you installed FFMPEG and PDFium above, update the following properties:

    * `FFMPEG.path=FFMPEG_HOME` (if installed, get the `FFMPEG_HOME` value from [Install FFMPEG](#ffmpeg))
    * `pdfium.path=PDFIUM_HOME` (if installed, get the `PDFIUM_HOME` value from [Install PDFium](#pdfium))

3. Delete current Alfresco deployed WAR files.

   Navigate to the `ALFRESCO_HOME/tomcat/webapps` directory and delete the `alfresco` folder (if it exists).

4. Start Alfresco.

## Install collaboration (optional)  {#collab}

In this section the Enterprise Viewer collaboration features Socket.IO server is installed.

> **Note:** This installation is only needed if the collaboration features are required.

1. Install `Node.js`.

   Both `NodeJS` and `npm` must be installed. Follow the `Node.js` install instructions at [https://nodejs.org/](https://nodejs.org/){:target="_blank"}.

   * `Node.js` - use the latest version your OS supports
   * `npm` - Node package manager, included with `Node.js`

2. Install Socket Server.

   Locate the `socket-server.zip` in the `Collaboration` folder of the `alfresco-enterprise-viewer-package` zip.

   Place the `socket-servers.zip` in the directory where the collaboration server is to be installed, and unzip it. This location will be known as `SOCKET_HOME`.

   This directory will now contain `server.js`, `Dockerfile`, `windows-service.js`, `package.json`, etc.

3. If no `node_modules` directory is included in the `SOCKET_HOME`, then run `npm i` from the `SOCKET_HOME`directory to generate the `node_modules` directory.

4. Test the Socket Server.

   To start the collaboration server, navigate to `SOCKET_HOME` and run the following command: `node server.js`.

   A Node JavaScript server starts listening on port 3000 for connections, and the command prompt displays the message `"listening on *:3000”`.

5. Stop the Socket Server.

   Press Ctrl+C to end the process.

6. Install the forever tool.

   Install forever by running the following command:

   * Linux: `sudo npm install forever -g`
   * Windows: `npm install forever -g`

7. Start the Socket Server.

   Start the collaboration server using forever by running the following command:

    ```text
    forever start server.js
    ```
In previous releases, the Socket Server URL for AEVV (Alfresco Enterprise Viewer Video) was set at build-time. There was no way to update or change the socket server URL without rebuilding the entire application. 

Starting from Enterprise Viewer 3.6, an enhancement has been added so the socket server URL is fetched from the `appConfig.json` at runtime. This provides users with the capability to change the socket server URL by unpacking the `opencontent.war` file, changing the `SOCKET_URL` value in `appConfig.json`, and repacking the WAR file. You can unpack & repack the WAR file in an archive manager such as WinRAR. The URL change takes effect without rebuilding the application.

## Install webapps

This sections walks through how to install the Enterprise Viewer web application.

> **Note:**
>
> * If you installed a proxy then follow the steps in [Install web applications on separate Tomcat](#separate-tomcat-oa).
>
> * If no proxy was installed then follow the steps to [Install web applications on Alfresco Tomcat](#alfresco-tomcat-oa).

### Install web applications on separate Tomcat {#separate-tomcat-oa}

This section walks through how to install the web applications on a separate Tomcat instance (meaning, you must have a proxy setup).

1. Install Apache Tomcat.

    See [https://archive.apache.org/dist/tomcat](https://archive.apache.org/dist/tomcat){:target="_blank"}. Note that if you installed ACA, you can use the same Tomcat you may have installed for ACA. Shut it down now if it's already running.

2. Copy the `OpenAnnotate.war` file into the `TOMCAT_HOME/webapps` directory.

   You'll find the WAR file in the `Web Applications` folder of the `alfresco-enterprise-viewer-package` zip.

3. Configure Tomcat for shared classpath loader as well as encoded slashes (if not already configured in the Content Accelerator installation):

   Edit the `TOMCAT_HOME/conf/catalina.properties` file and enable the `shared.loader` by adding the following line (if not already there):

   `shared.loader=${catalina.base}/shared/classes,${catalina.base}/shared/lib/*.jar`

   ACA has some routes that are formatted like:

    ```text
    /hpi/{aca-module}/{object-id}
    ```

   In the above case, the object ID is URL encoded. This means that forward slashes in the object ID are URL encoded to `%2F`. By default, Tomcat does not serve any URLs with a URL encoded forward (or back) slash.

   To work around the issue, edit the `TOMCAT_HOME/conf/catalina.properties` file and add the following line (if not already there):

    ```java
    org.apache.tomcat.util.buf.UDecoder.ALLOW_ENCODED_SLASH=true
    ```

4. (If not already configured in the ACA install) - Configure Tomcat ports in the `TOMCAT_HOME/conf/server.xml`:

   Configure the connector, server, and redirect ports to not conflict with Alfresco Tomcat’s (example below):

   * Set Connector - `port="9090"` (defaults to `8080`)
   * Set Connector - `redirectPort="9443"` (defaults to `8443`)
   * Set Server - `port="9005"` (defaults to `8005`)

   Note that you will need to ensure that the port chosen (i.e. `9090`) is open to the end user.

5. (If not already configured in the ACA install) - Create a `classes` directory:

   Create the path `TOMCAT_HOME/shared/classes`, if it does not already exist.

6. Locate the `openannotate-override-placeholders.properties` file in the `Web Applications` folder of the `alfresco-enterprise-viewer-package` zip.

7. Update the provided `openannotate-override-placeholders.properties` file:

   Set the `ocRestEndpointAddress` property to point to the root REST endpoint URL for OpenContent within Alfresco:

   `{Application Base URL}/alfresco/OpenContent`

   > **Note:** If the Enterprise Viewer and the Alfresco Repository are located on the same server, then the URL can be: `http://localhost:<alfrescoPort>/alfresco/OpenContent`.

   (OPTIONAL) This step is only required if using the Enterprise Viewer and leveraging the "Collaboration Server" functionality for collaborative annotation functionality:

    Update the following properties:

    * `collaborationModeEnabled=true`
    * `collaborationEndpoint=http://${server}:${port}`

    Replace the `${server}` and `${port}` placeholders in the above URL with the correct server and port values for the environment being installed to (See the section [Install collaboration features]({% link enterprise-viewer/latest/install/index.md %}#collab))

8. For AEV 3.5.1 or later, verify the `secureBrowserCookies` configuration. If you are planning to setup SSL then `secureBrowserCookies` should be set to `true`, else it should be `false` (the default).

   In the `openannotate-override-placeholders.properties` set the following property accordingly: `secureBrowserCookies=`

9. For AEV 3.5.1 or later, verify the `application.secureBrowserCookies` configuration. If you are planning to setup SSL then `application.secureBrowserCookies` should be set to `true`, or else it should be `false` (the default).

   In the `opencontent-override-placeholder.properties` set the following property accordingly: `application.secureBrowserCookies=`

10. Copy the `opencontent-override-placeholders.properties` and `openannotate-override-placeholders.properties` files to the Tomcat classpath, for example, in the `TOMCAT_HOME/shared/classes` directory.

11. Start Tomcat.

12. Confirm you can access AEV at `http://{server}/OpenAnnotate`.

### Install web applications on Alfresco Tomcat {#alfresco-tomcat-oa}

This section walks through how to install the web applications on Alfresco Tomcat (recommended for easier non-Production environment installation).

1. Stop Alfresco Tomcat.

2. Copy the `OpenAnnotate.war` file into the `ALFRESCO_HOME/tomcat/webapps` directory.

   You'll find this WAR file in the `Web Applications` folder of the `alfresco-enterprise-viewer-package` zip.

3. Create a `classes` directory:

   Create a `classes` directory within the `ALFRESCO_HOME/tomcat/shared` directory, if it does not already exist.

4. Locate the `openannotate-override-placeholders.properties` file in the `Web Applications` folder of the `alfresco-enterprise-viewer-package` zip.

5. Update the provided `openannotate-override-placeholders.properties` file:

   Set the `ocRestEndpointAddress` property to point to the root REST endpoint URL for OpenContent within Alfresco:

   `{Application Base URL}/alfresco/OpenContent`

   > **Note:** The URL can also be: `http://localhost:<alfrescoPort>/alfresco/OpenContent`

6. (Optional) This step is only required if using the Enterprise Viewer and leveraging the "Collaboration Server" functionality for collaborative annotation functionality:

   Update the provided `openannotate-override-placeholders.properties` file:

   * `collaborationModeEnabled=true`
   * `collaborationEndpoint=http://${server}:${port}`

   Replace the `${server}` and `${port}` placeholders in the above URL with the correct server and port values for
   the environment being installed to. See the section [Install collaboration features]({% link enterprise-viewer/latest/install/index.md %}#collab).

7. For AEV 3.5.1 or later, verify the `secureBrowserCookies` configuration. If you are planning to setup SSL then `secureBrowserCookies` should be set to `true`, else it should be `false` (the default).

   In the `openannotate-override-placeholders.properties` set the following property accordingly: `secureBrowserCookies=`

8. For AEV 3.5.1 or later, verify the `application.secureBrowserCookies` configuration. If you are planning to setup SSL then `application.secureBrowserCookies` should be set to `true`, else it should be `false` (the default).

   In the `opencontent-override-placeholders.properties` set the following property accordingly: `application.secureBrowserCookies=`.

9. Copy the `opencontent-override-placeholder.properties` and `openannotate-override-placeholders.properties` file to the Tomcat classpath, for example, in the `TOMCAT_HOME/shared/classes` directory.

10. Start Alfresco Tomcat.

11. Confirm you can access AEV at `http://{server}/OpenAnnotate`.

## Configure Share extensions for AEV (optional)

> **Note:** These steps are only required if you wish to accomplish one or both of the following:
>
> * Use the Enterprise Viewer as the document viewer in the Share interface.
> * Include an action in the Share interface to launch a document in the Enterprise Viewer in a new tab.

1. Stop Alfresco.

2. Locate the `oa-alfresco.amp` in the `Alfresco Artifacts` folder of the `alfresco-enterprise-viewer-package` zip.

   Copy the AMP to the `ALFRESCO_HOME/amps` directory.

   From the directory where your Alfresco Tomcat lives, run this command (replacing `{ALFRESCO_HOME}` with the location of your `ALFRESCO_HOME`):

    Linux:

    ```java
    java -jar {ALFRESCO_HOME}/bin/alfresco-mmt.jar install {ALFRESCO_HOME}/amps/oa-alfresco.amp tomcat/webapps/alfresco.war -force
    ```

    Windows:

    ```java
    java\{javaVersion}\bin\java -jar {ALFRESCO_HOME}\bin\alfresco-mmt.jar install {ALFRESCO_HOME}\amps\oa-alfresco.amp tomcat\webapps\alfresco.war -force 
    ```

3. (Optional) This step is only required if using the Enterprise Viewer External Launcher action in Share. This adds a Share action to launch a document in the Enterprise Viewer in a new tab.

   Locate the `oa-share-external-launcher.amp` in the `Share Artifacts` folder of the `alfresco-enterprise-viewer-package` zip.

   > **Important:** If AEV and ACS are not running the same Tomcat or if you don't have a proxy setup to make it appear like they are, you will need to edit the following files in the AMP by extracting them or by editing them directly inside the AMP:
   >
   > * `/web/component/(documentlibrary or preview)/annotation-urls.js`
   > * `/web/component/(documentlibrary or preview)/annotation-urls-min.js`
   >
   > Update the `Alfresco.constants.EXTERNAL_LAUNCHER_ANNOTATION_URL` variable within these files.
   >
   >    This variable needs to be updated with the URL of the server that Enterprise Viewer is going to be deployed on (even if Enterprise Viewer is deployed on the same server as the Share web application).
   >
   >    For example:
   >
   >    ```text
   >    Alfresco.constants.EXTERNAL_LAUNCHER_ANNOTATION_URL = "http://localhost:8080/OpenAnnotate/login/external.htm";
   >    ```
   >
   >    These URLs are relative by default, so you only need to update them if AEV and ACS are running on separate Tomcats and you don't have a proxy setup to make it appear like they are running on the same Tomcat.

   Then, copy the AMP to the `ALFRESCO_HOME/amps_share` directory (create the directory if it doesn't exist).

   From the directory where your Alfresco Tomcat is installed, run the following command (replacing `{ALFRESCO_HOME}` with the location of your `ALFRESCO_HOME`):

    Linux:

    ```bash
    java -jar {ALFRESCO_HOME}/bin/alfresco-mmt.jar install {ALFRESCO_HOME}/amps_share/oa-share-external-launcher.amp tomcat/webapps/share.war -force
    ```

    Windows:

    ```bash
    java\{javaVersion}\bin\java -jar {ALFRESCO_HOME}\bin\alfresco-mmt.jar install {ALFRESCO_HOME}\amps_share\oa-share-external-launcher.amp tomcat\webapps\share.war -force 
    ```

4. (Optional) This step is only required if using the Enterprise Viewer Web Preview in Share. It replaces the OOB Share viewer with the Enterprise Viewer.

   Locate the `oa-share-webpreview.amp` in the `Share Artifacts` folder of the alfresco-enterprise-viewer-package zip.

   > **Important:** If AEV and ACS are not running the same Tomcat or if you don't have a proxy setup to make it appear like they are, you will need to edit the following files in the AMP by extracting them or by editing them directly inside the AMP:
   >  
   >    * `/web/component/(documentlibrary or preview)/annotation-urls.js`
   >    * `/web/component/(documentlibrary or preview)/annotation-urls-min.js`
   >
   > In both cases, you need to update the `Alfresco.constants.WEBPREVIEW_ANNOTATION_URL` variable within these files.
   >
   >    This variable needs to be updated with the URL of the server that Enterprise Viewer is going to be deployed on (even if Enterprise Viewer is deployed on the same server as the Share web application).
   >
   >   For example:
   >
   >   ```text
   >   Alfresco.constants.WEBPREVIEW_ANNOTATION_URL = "http://localhost:8080/OpenAnnotate/login/external.htm";
   >   ```
   >
   >   These URLs are relative by default, so you only need to update them if AEV and ACS are running on separate Tomcats and you don't have a proxy setup to make it appear like they are running on the same Tomcat.

   Then, copy the AMP to the `ALFRESCO_HOME/amps_share` directory (create the directory if it doesn't exist).

   From the directory where your Alfresco Tomcat lives, run this command (replacing `{ALFRESCO_HOME}` with the location of your `ALFRESCO_HOME`):

   Linux:

    ```bash
    java -jar {ALFRESCO_HOME}/bin/alfresco-mmt.jar install {ALFRESCO_HOME}/amps_share/oa-share-webpreview.amp tomcat/webapps/share.war -force
    ```

   Windows:

    ```bash
    java\{javaVersion}\bin\java -jar {ALFRESCO_HOME}\bin\alfresco-mmt.jar install {ALFRESCO_HOME}\amps_share\oa-share-webpreview.amp tomcat\webapps\share.war -force 
    ```

5. Delete current Share deployed WAR files.

   Navigate to the `ALFRESCO_HOME/tomcat/webapps` directory and delete the `share` folder (if it exists).

6. Start Alfresco.

7. (Optional) You can verify these AMPs were deployed correctly by doing the following:

    * `oa-share-external-launcher.amp` - open an asset in Share and look at the Document Actions panel on the right-hand side of the screen. Ensure that the asset has a PDF rendition or a suitable image rendition available for Enterprise Viewer. If you installed the `oa-share-external-launcher.amp`, the "Enterprise Viewer" action should be available.

    * `oa-share-webpreview.amp` - open an asset in Share. If you installed the `oa-share-webpreview.amp` and the asset has a PDF rendition or a suitable image rendition available for Enterprise Viewer, the asset should appear in "Alfresco Enterprise Viewer" directly in the Share application screen.
---
title: Java 17 Support
---

Deploying ACA/AEV in a Java 17 runtime environment is supported with the 3.5.1 release of ACA/AEV via two different approaches. “Illegal reflective accesses” previously generated warnings in older JDK versions, but as of JDK 17, reflection is forbidden out of the box, unless the given modules are explicitly requested. See further information on why reflection has become forbidden in the JDK 17 release documentation: [JEP 403: Strongly Encapsulate JDK Internals](https://openjdk.org/jeps/403){:target="_blank"}.

## Impact on ACA/AEV

ACA/AEV utilize Ehcache as their caching mechanism. Cache sizes are limited by bytes out of the box in ACA/AEV to prevent caches from growing larger than what the system resources allow. Ehcache manages byte based cache limits by utilizing reflection (which is now forbidden with JDK 17).

## Utilizing ACA/AEV with JDK 17

### Option 1 - Allow reflection

In order to deploy ACA/AEV in a Java 17 runtime environment, you can add java command line flags in the Java Runtime Environment where ACS is installed to allow reflection to continue to occur in Java 17.

For example:

You can add the following flags to the `_JAVA_OPTIONS` environment variable:

```java
--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
```

The `_JAVA_OPTIONS` environment variable passes options to any JVM process started on your system. When a JVM starts, it parses the value of `_JAVA_OPTIONS` as if the parameters were at the command-line of Java.  So adding those options to this environment variable in the system where ACS is installed will allow for reflection to occur on those classes on any JVM process started on the system.

### Option 2 - Limit cache sizes based on entries

Limiting Ehcache cache sizes by the number of entries instead of bytes prevents Ehcache from needing to utilize reflection which keeps us in the bounds of what JDK 17 allows out of the box.  This can be done by overriding the ACA/AEV `ehcache.xml` configuration file in a custom AMP and reconfiguring the Ehcache configuration files to limit cache sizes by the number of entries.

In each cache configuration, replace the following properties:

```xml
maxBytesLocalHeap=
maxBytesLocalDisk=
```

with:

```xml
maxEntriesLocalHeap=
maxEntriesLocalDisk=
```

For example, the out of the box ACA/AEV cache configuration file for ACA/AEV 3.5.1 is:

```xml
<ehcache xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="../config/ehcache.xsd" updateCheck="false">
    <!-- *** Whatever you change here, you must change in all other ehcache.xml 
        files. They need to be maintained. *** -->

    <!-- where to store the files written to disk on overflow -->
    <diskStore path="java.io.tmpdir" />

    <!-- cache for the content of our objects -->
    <cache name="oc-content" 
        eternal="true" 
        maxBytesLocalHeap="150M"
        maxBytesLocalDisk="5G" 
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>
    <!-- cache for getting the content info of an object -->
    <cache name="oc-contentInfo" 
        eternal="true" 
        maxBytesLocalHeap="25M"
        maxBytesLocalDisk="5G" 
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the page transformations from PDFs to PNG for our objects -->
    <cache name="oc-pages" 
        eternal="true" 
        maxBytesLocalHeap="250M"
        maxBytesLocalDisk="5G" 
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the section-row boxes for text select tools for OpenAnnotate -->
    <cache name="oc-page-section-word-data" 
        eternal="true" 
        maxBytesLocalHeap="25M" 
        maxBytesLocalDisk="5G"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the wordMaps for text searching in for OpenAnnotate -->
    <cache name="oa-search-word-maps" 
        eternal="true"
        maxBytesLocalHeap="25M" 
        maxBytesLocalDisk="5G"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the overlays of our objects -->
    <cache name="oc-document-overlays" 
        eternal="true"
        maxBytesLocalHeap="50M" 
        maxBytesLocalDisk="5G"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>
    
    <!-- cache for the document info of our objects in OpenAnnotate-->
    <cache name="oa-document-info" 
        eternal="true" 
        maxBytesLocalHeap="25M"
        maxBytesLocalDisk="5G" 
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the object types that should be externally indexed -->
    <cache name="objectTypes-to-index" 
        eternal="true"
        maxBytesLocalHeap="50M" 
        maxBytesLocalDisk="5G"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the asset Files -->
    <cache name="assetFiles" 
        eternal="true"
        maxBytesLocalHeap="50M" 
        maxBytesLocalDisk="100M"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>
    
    <!-- cache for template objects -->
    <cache name="oc-template"
        timeToLiveSeconds="60"
        maxEntriesLocalHeap="5000" 
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="none" />
    </cache>
</ehcache>
```

and a sample override:

```xml
<ehcache xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="../config/ehcache.xsd" updateCheck="false">
    <!-- *** Whatever you change here, you must change in all other ehcache.xml 
        files. They need to be maintained. *** -->

    <!-- where to store the files written to disk on overflow -->
    <diskStore path="java.io.tmpdir" />

    <!-- cache for the content of our objects -->
    <cache name="oc-content" 
        eternal="true" 
        maxEntriesLocalHeap="30"
        maxEntriesLocalDisk="5000"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>
    <!-- cache for getting the content info of an object -->
    <cache name="oc-contentInfo" 
        eternal="true"  
        maxEntriesLocalHeap="100"
        maxEntriesLocalDisk="1000"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the page transformations from PDFs to PNG for our objects -->
    <cache name="oc-pages" 
        eternal="true" 
        maxEntriesLocalHeap="50"
        maxEntriesLocalDisk="500"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the section-row boxes for text select tools for OpenAnnotate -->
    <cache name="oc-page-section-word-data" 
        eternal="true" 
        maxEntriesLocalHeap="15"
        maxEntriesLocalDisk="500"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the wordMaps for text searching in for OpenAnnotate -->
    <cache name="oa-search-word-maps" 
        eternal="true"
        maxEntriesLocalHeap="15"
        maxEntriesLocalDisk="500"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the overlays of our objects -->
    <cache name="oc-document-overlays" 
        eternal="true"
        maxEntriesLocalHeap="10"
        maxEntriesLocalDisk="500"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>
    
    <!-- cache for the document info of our objects in OpenAnnotate-->
    <cache name="oa-document-info" 
        eternal="true" 
        maxEntriesLocalHeap="100"
        maxEntriesLocalDisk="1000"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the object types that should be externally indexed -->
    <!--  Specific to Elastic Search. Keeps track of which object types should be indexed -->
    <cache name="objectTypes-to-index" 
        eternal="true"
        maxEntriesLocalHeap="100"
        maxEntriesLocalDisk="500"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>

    <!-- cache for the asset Files -->
    <!-- these are the asset files from the aca configs -->
    <cache name="assetFiles" 
        eternal="true"
        maxEntriesLocalHeap="5"
        maxEntriesLocalDisk="10"
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="localTempSwap" />
    </cache>
    
    <!-- cache for template objects -->
    <cache name="oc-template"
        timeToLiveSeconds="60"
        maxEntriesLocalHeap="5000" 
        memoryStoreEvictionPolicy="LRU">
        <persistence strategy="none" />
    </cache>
</ehcache>
```

> **Note:** The override file should be configured such that the entry limits are based on the expected sizes of cache entries so that the caches don’t grow outside system resources.

## Override in a custom AMP

1. Edit the `opencontent-extension-override-config.xml` file in your client AMP to include the following two beans:

    ```xml
        <bean id="cacheManager" class="org.springframework.cache.ehcache.EhCacheCacheManager" p:cache-manager-ref="ehcacheOverride"/>

        <bean id="ehcacheOverride" class="org.springframework.cache.ehcache.EhCacheManagerFactoryBean" p:config-location="classpath:alfresco/module/com.tsgrp.opencontent/extension/config/ehcache-override.xml" p:shared="true"/> 
    ```

2. Place your `ehcache-override.xml` file within your custom AMP at the path specified in the `ehcacheOverride` bean.
---
title: Prerequisites and sizing
---

## Recommended software environment

Server-side

* Server operating system:
  * Windows Server 2012R2 (64-bit) or Red Hat Enterprise Linux (64-bit)
  * Other versions of Windows and Linux are supported, contact us for more details
* Web server:
  * Tomcat 8.x+ (64-bit)
  * Other application server wrappers are supported, contact us for more details
* Java:
  * Java 11 + (64-bit)
  * If you are using Java 17, refer to our [Java 17 support guide]({% link enterprise-viewer/latest/install/java-support.md %}).

Client Browsers:

1. Internet Explorer 11 +
2. Firefox
3. Chrome
4. Safari

## Recommended hardware environment

Virtual servers (VMWare-based) and Enterprise Viewer are fully compatible and supported. Bare metal
servers with an OS directly installed are also supported.

## Server sizing (based on peak and average concurrent user loads)

### Review monthly statistics

For this evaluation, we’ll assume all the users are concurrent users.

| Concurrent reviewers & viewers (Users) | Recommended server specifications |
| -------------------------------------- | --------------------------------- |
| Peak users | Average users | Total RAM | Load balanced servers |
| ---------- | ------------- | --------- | --------------------- |
| 1,000+ | 500 | 64 GB^ | 2 - 4 |
| 500 | 250 | 32 GB^ | 2 |
| 200 | 100 | 16 GB^ | 1 - 2 |
| 100 | 50 | 8 GB^ | 1 |
| 50 | 20 | 6 GB^ | 1 |

**_“Users”_** _includes both reviewers themselves, and anyone viewing annotated documents._

****_Total RAM_** _is total RAM, split evenly across all servers, when multiple load balanced servers are called
for._

*****_Load Balanced Servers._** _Each server is assumed to have 4 CPUs._

*** Memory recommendations are between Enterprise Viewer, OpenContent, and AEVT. If these are on separate servers the memory can be divided between them. Our initial recommended split is 50% / 40% / 10% between AEVT / OpenContent / Enterprise Viewer

## Sample of server sizing

### Review monthly statistics example

For this evaluation, we'll assume all the users are concurrent users.

| Month | Total reviewers & viewers | Avg. day reviewers & viewers |
| ----- | ------------------------- | ---------------------------- |
| Jan- 14 | 5,748 | 287 |
| Feb- 14 | 7,184 | 359 |
| Mar- 14 | 7,230 | 362 |
| Apr- 14 | 7,866 | 393 |
| May- 14 | 6,232 | 312 |
| Jun- 14 | 6,023 | 301 |
| Jul- 14 | 7,019 | 351 |
| Aug- 14 | 7,246 | 362 |
| Sep- 14 | 8,782 | 439 |
| Oct- 14 | 10,069 | 503 |
| Total | 73,399 | 367 |

We can see here three key figures:

* Lowest value: 287
* Peak value: 503
* Average value: 367

It means the system must be able to handle a maximum of 500 concurrent users.

### Recommended options

Based on these assumptions, the following options are recommended:

1. 2 servers with the following specifications:
   * 4 CPUs
   * 32 GB RAM per server
   * Tomcat Java options:
      * `Xms512M`
      * `Xmx 20 G`
      * `XX:MaxPermSize=256m`
      * `XX:-DisableExplicitGC`
   * `web.xml`
      * `maxThreads=2 50`
   * 30 GB HDD space
   * Servers must be load-balanced the load-balancer must have:
      * Session affinity: enabled
      * Web server probe: recommended
2. 4 servers with the following specifications
   * 4 CPUs
   * 16 GB RAM per server
   * Tomcat Java Options:
      * `Xms512M`
      * `Xmx1 0 G`
      * `XX:MaxPermSize=256m`
      * `XX:-DisableExplicitGC`
   * `web.xml`
      * `maxThreads= 125`
   * 30 GB HDD space
   * Servers must be load-balanced the load-balancer must have:
     * Session affinity: enabled
     * Web server probe : recommended
---
title: Upgrade Alfresco Enterprise Viewer
---

No data model or breaking updates are required to upgrade versions of Alfresco Enterprise Viewer from version 3.3 to version 3.5. The only significant change in this version from an infrastructure point of view is that the Alfresco Enterprise Video Viewer (AEVV, formerly known as OpenAnnotate Video) is now embedded within the Enterprise Viewer web application. In version 3.3, AEVV was deployed as a separate web application in its own context.

Follow these steps to upgrade Enterprise Viewer 3.3 to 3.5

* Backup previous WARs, Alfresco and Share web directories.
* Follow standard install steps, replacing/backing up previous installation artifacts as needed.
* Remove OpenAnnotate Video standalone web application (OpenAnnotateVideo.war).
* Remove any proxy rules for /OpenAnnotateVideo.
* Start up and verify the application is working as expected.

> **Note:** Video link URLs have changed slightly with the newly embedded AEVV web application. Ensure your network settings or previous direct links are updated if necessary.

## Upgrading to 3.5.1 and above

For AEV 3.5.1 or later, verify the `secureBrowserCookies` configuration. If you have setup SSL then `secureBrowserCookies` should be set to `true`, else it should be `false` (the default).

In the `openannotate-override-placeholders.properties` set the following property accordingly: `secureBrowserCookies=`.

## Upgrading to 3.6 and above

For AEV 3.6 or later, the Control Document type is set to `aw:qualityDocument` by default. In case of a custom type set, you will need to override it by completing the following steps.

1. Override the bean in `opencontent-extension-override-module-ctx.xml` as follows:

   ```xml
   <bean id="paasExtendPermissionModel" parent="permissionModelBootstrap">
     <property name="model" value="alfresco/module/com.tsgrp.opencontent/model/ocPermissionDefinitionsOverride.xml"/>
   </bean>
   ```

3. Then create `ocPermissionDefinitionsOverride.xml` at the specified path in your custom AMP with the contents of the original `ocPermissionDefinitions.xml`. 

4. Replace the type `aw:qualityDocument` with your current or desired control document type. 
---
title: Supported platforms
---

The following are the supported platforms for the Alfresco Enterprise Viewer 4.0:

| Version | Notes |
| ------- | ----- |
| Content Services 23.x | |
| Search Services 2.x | |
| Search Enterprise 4.x | |
---
title: Using Enterprise Viewer
---

This section details everything that you need to know in order to take complete advantage of the Enterprise Viewer application.

## Mode Dropdown

The Enterprise Viewer has four modes:

* Add Annotations
* Redact Content
* Edit Pages
* Add Signature

Users can be launched directly into any of these modes. By default, a document is launched into annotation mode. The mode dropdown can also be disabled:

![Img Txt]({% link enterprise-viewer/images/aev-mode-dropdown.png %})
![Img Txt]({% link enterprise-viewer/images/aev-mode-dropdown2.png %})

### Add Annotations

Add Annotations mode allows the user to annotate the document.

See the [Add Annotations Interface section]({% link enterprise-viewer/latest/using/index.md %}#add-annotations-interface) for more information.

### Redact Content

Redact Content mode allows the user to redact text and images in the document.

See the [Redact Content Interface section]({% link enterprise-viewer/latest/using/index.md %}#redact-content-interface) for more information.

### Edit Pages

Edit Pages mode allows the user to edit pages by reordering, splitting, rotating, or sectioning them.

See the [Edit Pages Interface section]({% link enterprise-viewer/latest/using/index.md %}#edit-pages-interface) for more information.

### Add Signatures

Add Signatures mode allows the user to add a signature to the document.

See the [Add Signatures Interface section]({% link enterprise-viewer/latest/using/index.md %}#add-signatures-interface) for more information.

## Add Annotations Interface

This section walks through the interface used to add annotations.

### Toolbar

The toolbar contains all the core functionality of the Enterprise Viewer in Annotation mode. This is where document navigation and zooming occur, and where annotations can be created, saved, and more information on Enterprise Viewer is found.

It is located at the top of the Enterprise Viewer window:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar.png %})

Dark grey buttons cannot be used until certain actions are made. A button that is in use will have a blue interior.

#### Manual Page Navigation

If the page number entered is not a number, this value gets reset to the current page. If the page number entered is lower than the first page, the user is navigated to the first page. If the page number entered is higher than the last page, the user is navigated to the last page.

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar2.png %})

Manually entering a value into this text field and then hitting the Enter key will navigate to the new page number.

This text field is located to the right of the Enterprise Viewer logo and to the left of the **Fit to Height** button.

#### Total Number of Pages

This is a non-editable field denoting the total number of pages for the document.

#### Fit to Height

The **Fit to Height** button is located to the right of the Manual Page Navigation text field and to the left of the **Fit to Width** button.

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar3.png %})

Clicking this button automatically calculates the zoom level to make the window show the entire height of the document. This does not take into account the width of the document, and thus scroll bars may appear horizontally depending on the page's aspect ratio against the size of the window.

#### Fit to Width

The **Fit to Width** button is located to the right of the **Fit to Height** button and to the left of the **Next Page** button. The **Fit to Width** button is to the left of the **Zoom Out** button if the **Next Page** button is not displayed in the toolbar:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar4.png %})

Clicking this button automatically calculates the zoom level to make the window show the entire width of the document. This does not take into account the height of the document, and thus scroll bars may appear vertically depending on the page's aspect ratio against the size of the window.

#### Next Page

The **Next Page** button is located to the right of the **Fit to Width** button and to the left of the **Previous Page** button.

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar5.png %})

Clicking this button takes the user to the next page of the document. The button will become disabled once the user reaches the end of the document.

> **Note:** This feature is unavailable if the document does not have more than one page.

#### Previous Page

The **Previous Page** button is located to the right of the **Next Page** button and to the left of the **Zoom Out** button.

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar6.png %})

Clicking this button takes the user to the previous page of the document. The button will become disabled once the user reaches the beginning of the document.

> **Note:** This feature is unavailable if the document does not have more than one page.

#### Zoom Out

The **Zoom Out** button is located to the right of the **Previous Page** button and to the left of the **Zoom In** button. The **Zoom Out** button is to the right of the **Fit to Width** button if the **Previous Page** button is not displayed in the toolbar.

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar7.png %})

Clicking this button zooms out in increments of ten. While zooming out, if possible, the current middle of the page will remain in the middle (unless zooming out reveals an image that does not need to be scrolled).

If the target zoom level is below the minimum zoom level, the zoom is set to the minimum zoom level. This is set for performance and usability reasons.

#### Zoom In

The **Zoom In** button is located to the right of the **Zoom Out** button and to the left of the Download dropdown.

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar8.png %})

Clicking this button zooms in using increments of ten. While zooming in, the current middle of the page will remain in the middle.

If the target zoom level is above the maximum zoom level, the zoom is set to the maximum zoom level. This is set for performance and usability reasons.

#### Download Dropdown

Provides various options related to downloading, checking in, or checking out documents:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar9.png %})

##### Annotated PDF Download

Clicking the following button downloads the document to be used for annotating documents offline. All annotations other than the current users will be locked in the downloaded PDF:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar10.png %})

##### Checkin Annotated PDF

Clicking the following button will allow the user to check-in a document that has been checked out for offline use. This will update the online annotations with any differences present in the offline copy. The annotations in the repository will match the annotations from the offline copy following check in, regardless of any changes made in the repository between the annotated pdf download and checking in the document:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar11.png %})

Attempting to check in a PDF not downloaded via the "Offline Annotated PDF Download" action, or a PDF downloaded from a different document will fail.

##### Print Annotated PDF

Clicking the following button will print a version of the PDF with annotations. This is unrelated to checking in and checking out documents:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar12.png %})

##### Extract Pages

Clicking the following button will allow the user to choose which pages to download. The user can type in the selected pages or select them by clicking the box in the top left corner of each page. The user must then select split PDF which will download the user's selected pages:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar13.png %})

> **Note:** This feature is unavailable if the document does not have more than one page.

##### Annotated PDF Download

Similar to Offline Annotated PDF Download, but this is not meant for annotating documents offline and checking them back in. This is simply for downloading. Other users' annotations will not be locked:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar14.png %})

##### Download Original

Clicking the following button will download a version of the PDF without annotations, only the base document:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar15.png %})

#### Save

Clicking the following button will save any new or modified annotations to the server, as well as refresh any unmodified annotations from other users that have been updated:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar16.png %})

The **Save** button is located to the right of the **Download** dropdown and to the left of the **Undo** button.

#### Undo Last Change

Clicking the following button will undo the last modification that was made to the document prior to the last save of the document:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar17.png %})

The **Undo** button is located to the right of the **Save** button and to the left of the **Redo** button.

#### Redo Last Change

Clicking the following button will redo the last change made to the document prior to the last save of the document:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar18.png %})

The **Redo** button is located to the right of the **Undo** button and to the left of the **Refresh** button. The **Redo** button is to the left of the **Show/Hide Annotations** button if the **Refresh** button is not displayed in the toolbar.

#### Refresh Annotations

Clicking the following button will refresh any unmodified annotations from the server that have been updated by other users:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar19.png %})

The **Refresh Annotations** button is located to the right of the **Redo** button and to the left of **Show/Hide Annotations** button.

> **Note:** This feature will not appear if "Collaboration Mode" is active, as annotation refreshes happen in real-time.

#### Show/Hide Annotations

Clicking the following button will show or hide the annotations made to the document. If the button is active the annotations can be seen. Annotations cannot be seen if the button is deactivated:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar20.png %})

The **Show/Hide Annotations** button is located to the right of the **Refresh Annotations** button and to the left of the **Keep Tool Selected** button. The **Show/Hide Annotations** button is to the right of the **Redo** button if the **Refresh Annotations button** is not displayed in the toolbar.

#### Keep Tool Selected

Clicking the following button will keep the currently selected annotation tool selected. This allows users to be able to make multiple annotations of the same type without having to select their chosen tool multiple times:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar21.png %})

The **Keep Tool Selected** button is located to the right of the **Show/Hide Annotations** button and to the left of the **Selection Tool** button.

#### Annotation Tools

The buttons listed below denote the different types of interactions the user can have with the document itself, as opposed to single events of the previous toolbar items. The selections will persist until another selection is made, or they are unselected due to a particular event:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar22.png %})

All of the annotation tools can be used for clicking a toolbar button, dragging annotations around a page, dragging and resizing annotation dialogs. The user can also set the status of the annotation to `None`, `Accepted`, `Cancelled`, `Completed`, or `Rejected`. If the user does not set the status of the annotation, then it is set to `None` by default.

After an annotation is created, the annotation tool returns to its default cursor.

##### Selection Tool

The **Selection Tool** button is the default cursor when opening Enterprise Viewer and signifies that the mouse does not do anything out of the ordinary:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar23.png %})

The **Selection Tool** button is located to the right of the **Keep Tool Selected** button and to the left of the **Sticky Note** button.

##### Sticky Note

The **Sticky Note** button is used when a sticky note needs to be added to a page. Once the cursor is selected, the user can click anywhere on the page to add a sticky note. The sticky note will set its top left corner to where the user clicked, and an annotation dialog will pop up to allow the user to edit the text. The user can also use the Color Selection menu to change the color of the sticky note annotation:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar24.png %})

The **Sticky Note** button is located to the right of the **Selection Tool** button and to the left of the **Add Attachment** button.

##### Add Attachment

The **Add Attachment** button is used when a file needs to be attached to a page. Once the cursor is selected, the user can
click anywhere on the page to add an attachment annotation. The attachment will set its top left corner to where the
user clicked, and an annotation dialog will pop up to allow the user to edit the text. The user can also use the
Color Selection menu to change the color of the attachment annotation:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar25.png %})

The **Add Attachment** button is located to the right of the **Sticky Note** button and to the left of the **Text Select**
dropdown.

###### Downloading Attachment

Once an attachment annotation is added to the page, a user can download the file by simply clicking the
**Download Attachment** button in the dialog box of the annotation:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar26.png %})

#### Text Select Dropdown

The Text Select dropdown includes all the available text select annotations. These include Select Text, Highlight,
Strikeout, Insert Text, Underline, and Replace Text. The user can select one or more lines of text from any section to
make an annotation from this group.

The dialog box will appear from the top left corner of all the annotations in this group except for select text. The
select text annotation allows a user to copy their selection of text in order to paste it into another application:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar27.png %})

The **Text Select** dropdown is located to the right of the **Add Attachment** button and to the left of the **Color**
selection box.

##### Select Text

The **Select Text** button is used when text on the page needs to be selected to copy it. Once the cursor is selected,
the user can click on the text they wish to select. The user can then drag the mouse over the text to select it until
the mouse is released:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar28.png %})

The **Select Text** button is located in the **Text Select** dropdown above the **Highlight** button.

##### Highlight

The **Highlight** button is used when text needs to be highlighted on the page. Once the cursor is selected, the user
can click on the text they wish to highlight. The user then can drag the mouse over the text to highlight it until the
mouse is released:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar29.png %})

The **Highlight** button is located in the **Text Select** dropdown below the **Select Text** button and above the
**Strikeout** button.

##### Strikeout

The **Strikeout** button is used to strikethrough text on the page. Once the cursor is selected, the user can click on
the beginning point of the text they wish to strikeout. The user can then drag the mouse over the text striking it out
until the mouse is released:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar30.png %})

The **Strikeout** button is located in the **Text Select** dropdown below the **Highlight** button and above the
**Insert Text** button.

##### Insert Text

The **Insert Text** at placeholder button is used to add text to the document in an annotation dialog box. Once the
cursor is selected, the user can click on any text to add a placeholder. The placeholder will set its top left corner
to where the user clicked:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar31.png %})

The **Insert Text** button is located in the **Text Select** dropdown below the **Strikeout** button and above the
**Underline** button.

##### Underline

The **Underline** button is used to underline text on the page. Once the cursor is selected, the user can click on the
beginning point of the text they wish to underline. The user can then drag the mouse over the text underlining it until
the mouse is released:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar32.png %})

The **Underline** button is located in the **Text Select** dropdown below the **Insert Text** button and above the
**Replace Text** button.

##### Replace Text

The **Replace Text** button is used to replace text in the document in an annotation dialog box. Once the cursor is
selected, the user can click on any text to add a placeholder. The placeholder will set its top left corner to where
the user clicked:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar33.png %})

The **Replace Text** is located in the **Text Select** dropdown below the **Underline** button.

#### Color

Clicking this button will open a box displaying the available colors the user can choose. The user can select a color to
change the color of the annotation when using the line, arrow, ellipse, rectangle, free draw, highlight, strikeout, or
insert text as placeholder buttons. Once the desired tool is selected, the user can then select a new color that will
appear on the page when the tool is used. Only one color can be chosen at a time.

The annotation tools each have their own default color, which will appear when the user selects a new tool and a color
has not been chosen yet:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar34.png %})

The **Color** selection box is located to the right of the **Text Select** dropdown and to the left of the
**Drawing Tools** dropdown.

##### Set Default Color

The user can set the default color by choosing a color, then clicking the **Set Default** button. The user will be prompted
by a popup window asking whether they want to set the selected color as the default color. Setting the default color in
the picker specifies the color that will be set on page load and used for all types of annotations. This value is saved
in relation to the browser it was saved on:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar35.png %})

The **Set Default** button is located in the **Color** dropdown above the **Reset** button.

##### Reset Color

The user can reset the default color by clicking the **Reset** button. The user will be prompted by a popup window asking
whether they want to reset the default color. Doing this will default the color back to red.

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar36.png %})

The **Reset** button is located in the **Color** dropdown below the **Set Default** button.

#### Drawing Tools Dropdown

The **Drawing Tools** dropdown includes all the available drawing annotations. These include Line, Arrow, Ellipse,
Rectangle, Text Box, and Free Draw. The drawing annotation tools are drawn from where the user clicks on the page to
where the user's mouse is when unclicking:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar37.png %})

If the mouse has not been dragged far enough from the starting point, the annotation will not be drawn, and the
selected annotation tool will not be changed. Additionally, all drawing annotations can be resized by clicking on them
to highlight them and dragging them.

An annotation dialog will pop up to allow the user to edit the text. Clicking on drawing objects will also open a dialog
for notes.

The **Drawing Tools** dropdown is located to the right of the **Color** selection box and to the left of the **Stamps**
dropdown.

##### Draw Line

The **Draw Line** button is used when a line needs to be added to a page. Once the cursor is selected, the user can
click anywhere on the page to start the line. The user can then drag the mouse anywhere else on the page to put the
other end point of the line. A line will be drawn from one point to the other:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar38.png %})

The **Draw Line** button is located in the **Drawing Tools** dropdown above the **Draw Arrow** button.

##### Draw Arrow

The **Draw Arrow** button is used when an arrow needs to be added to a page. Once the cursor is selected, the user can
click anywhere on the page to start the arrow. The user can then drag the mouse anywhere else on the page to put the tip
of the arrow. An arrow will be drawn from one point to the other. The arrow will point to the second point. Dialog boxes
will be anchored at the beginning of the arrow:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar39.png %})

The **Draw Arrow** button is located in the **Drawing Tools** dropdown below the **Draw Line** button and above the
**Draw Ellipse** button.

##### Draw Ellipse

The **Draw Ellipse** button is used when an ellipse needs to be added to a page. Once the cursor is selected, the user
can click anywhere on the page to start the rectangle that will contain the ellipse. The user can then drag the mouse
anywhere else on the page to put the other end point of the rectangle containing the ellipse. An ellipse will be drawn
within the two points so that the top is the highest point in the rectangle containing it, the bottom is the lowest
point, and the sides are the two widest points. Dialog boxes will be anchored in the center of the ellipse:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar40.png %})

The **Draw Ellipse** button is located in the **Drawing Tools** dropdown below the **Draw Arrow** button and above the
**Draw Rectangle** button.

##### Draw Rectangle

The **Draw Rectangle** button is used when a rectangle needs to be added to a page. Once the cursor is selected, the
user can click anywhere on the page to start the rectangle. The user can then drag the mouse anywhere else on the page
to put the other corner of the rectangle. A rectangle will be drawn from one point to the other. Dialog boxes are
anchored in the beginning of the rectangle:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar41.png %})

The **Draw Rectangle** button is located in the **Drawing Tools** dropdown below the **Draw Ellipse** button.

##### Add Text Box

The **Text Box** button is used to add a text box to the document. Once the cursor is selected, the user can click
anywhere on the page to start the text box. The user can then drag the mouse anywhere else on the page to put the other
corner of the text box. A text box will be drawn from one point to the other. The user can use the comments section in
the dialog box to add their text:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar42.png %})

The **Text Box** button is located in the **Drawing Tools** dropdown below the **Draw Rectangle** button and above the
**Free Draw** button.

##### Free Draw

The **Free Draw** button is used for free hand drawing on the document. Once the cursor is selected, the user can
click anywhere on the page to start the free draw. The user can then drag the mouse anywhere else on the page until the
drawing is complete. Dialog boxes are anchored to the top left corner of the drawing:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar43.png %})

The **Free Draw** button is located in the **Drawing Tools** dropdown below the **Text Box** button.

#### Stamp Tools Dropdown

The **Stamps** dropdown includes all of the available stamp annotations. These include Approved, Reviewed, Accepted,
Rejected, and Checkmark. When one of these stamps are selected, a preview will appear on the document that will allow
the user to see how the stamp will look when it is placed on the document. The dialog box will appear from the top left
corner of the stamp annotation and will appear every time the annotation is selected:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar44.png %})

The **Stamps** dropdown is located to the right of the **Drawing Tools** dropdown and to the left of the **Help** button.

##### Approved Stamp

The **Approved Stamp** is used when an approved stamp needs to be added to a page. Once the approved stamp button is clicked,
a preview of the stamp will appear on the document to allow the user to see what the stamp annotation will look like
before it is placed on the document:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar45.png %})

The **Approved Stamp** is located in the **Stamps** Dropdown menu above the **Reviewed Stamp** button.

##### Reviewed Stamp

The **Reviewed Stamp** is used when a reviewed stamp needs to be added to a page. Once the reviewed stamp button is clicked,
a preview of the stamp will appear on the document to allow the user to see what the stamp annotation will look like
before it is placed on the document:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar46.png %})

The **Reviewed Stamp** button is located in the **Stamps** dropdown below the **Approved Stamp** and the
**Accepted Stamp** button.

##### Accepted Stamp

The **Accepted Stamp** is used when an accepted stamp needs to be added to a page. Once the accepted stamp button is
clicked, a preview of the stamp will appear on the document to allow the user to see what the stamp annotation will
look like before it is placed on the document:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar47.png %})

The **Accepted Stamp** button is located in the **Stamps** Dropdown menu below the **Reviewed Stamp** button and above
the **Rejected Stamp** button.

##### Rejected Stamp

The **Rejected Stamp** is used when a rejected stamp needs to be added to a page. Once the rejected stamp button is
clicked, a preview of the stamp will appear on the document to allow the user to see what the stamp annotation will look
like before it is placed on the document:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar48.png %})

The **Rejected Stamp** button is located in the **Stamps** dropdown below the **Accepted Stamp** button and above the
**Checkmark stamp** button.

##### Checkmark Stamp

The **Checkmark Stamp** is used when a checkmark stamp needs to be added to a page. Once the checkmark stamp button is
clicked, a preview of the stamp will appear on the document to allow the user to see what the stamp annotation will
look like before it is placed on the document:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar49.png %})

The **Checkmark Stamp** button is located in the **Stamps** dropdown below the **Rejected Stamp** button.

#### Help

The **Help** button is used to give the user more information regarding Enterprise Viewer. When this button is clicked a
new tab in the browser will open with Technology Services Group information regarding their services and description
of Enterprise Viewer:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar50.png %})

The **Help** button is located to the right of the **Stamp Tools** dropdown and to the left of the **Active Users** box.

#### Active Users

The **Active Users** box shows the user how many users are currently viewing the current document. Clicking this button
will change the tab in the sidebar to the **Participants** tab:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar51.png %})

The **Active Users** box is located to the right of the **Help** button and to the left of the **Load Time** text.

> **Note:** The **Active Users** box is only displayed if "Collaboration Mode" is active.

#### Load Time

The **Load Time** text shows the user how many seconds it took to load the document:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar52.png %})

The user can see more details when clicking on the text:

![Img Txt]({% link enterprise-viewer/images/aev-annotations-interface-toolbar53.png %})

The load time takes into consideration the time it took the user to login, the browser JavaScript load time,
the time it took to retrieve document information, the time it took to display the document, and the document's size. The
user can copy the load time information into their clipboard by clicking the Copy to **Clipboard** button found in the load
time information window:

The **Load Time** text is located to the right of the **Active Users** box.

### Right Sidebar

The right sidebar displays the annotation summary and search tabs. It is to the right of the document and below the
toolbar.

#### Hide Sidebar

The **Hide Sidebar** button allows the user to hide or show the sidebar depending upon the current state of the view. By
default, the sidebar is in view. When clicked, the sidebar will be hidden from the display. When the sidebar is not in
view, the button can be clicked to show the sidebar, and the sidebar will reappear in its default position:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar1.png %})

This button is located in the upper right corner of the sidebar.

#### Annotation Summary

The annotation summary tab is used to show the summaries of the annotations that have been made in the document:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar3.png %})

The user can export the summary to excel, print the summary, filter through the annotations, and view the summaries
in this tab:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar2.png %})

##### Export Summary to Excel

This **Export Summary to Excel** button is used to export the summaries to excel:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar4.png %})

When clicked a message will appear stating that the Excel sheet is being downloaded, and the user can continue to
annotate the document. The Excel sheet will display the annotation summaries in a table format. It will include but is
not limited to the title of the document, creation date, page, author, type, status, and comments.

The **Export Summary to Excel** button is located near the top of the Annotation **Summary** tab, to the right of the
**Annotation Summary** title, and to the left of the **Printable Summary** button.

##### Printable Summary

The **Printable Summary** button is used to print the annotation summaries:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar5.png %})

When clicked, a new window will open displaying all the annotation summaries in a table format. It will display the
object name, title, creation date, page, author, type, comment, status, and replies if any. The user can print the page
by selecting the window and clicking `Ctrl + P` or in a form of the user's choosing.

This **Printable Summary** button is located near the top right corner of the Annotation **Summary** tab and to the
right of the **Export Summary to Excel** button.

##### Filter Text Box

The filter text box allows the user to sort through the annotation summaries efficiently:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar6.png %})

When the user types in the text box, the annotation summary boxes will be sorted. The annotation summary boxes with
text matching the user's input will appear below the filter search box. The filter field will filter on the:

* Username of the annotation creator
* Contents of the annotation comment
* Date of the comment
* Page Number
* Annotation type (ex: Highlight, Cross-Out, Sticky Note)

This text box is located at the top of the Annotation **Summary** tab below the **Export Summary to Excel** and
**Printable Summary** buttons.

##### Filters

The **Filters** button allows the user to filter through the annotation summary boxes based upon the status and author:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar7.png %})

When clicked, a checkbox list will appear displaying status, author(s), and type options for user to select. Multiple
statuses, authors and/or types can be selected. The filters box can be used with the filter text box.

The **Filters** button is located on the immediate right of the **Filter Text Box**.

##### Clear Filters

The **Clear Filters** button is used to clear all filters from the filter text box and the filters button:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar8.png %})

When clicked, the text in the filters text box will be cleared as well as the selections made in the filters list.

The **Clear Filters** button will appear to the right of the **Filter Text Box** when there is text in the filter text
box or when a selection is made in the filters list.

##### Annotation Summary Boxes

The annotation summary boxes appear in the sidebar below the filter text box:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar9.png %})

They are used to display information regarding each annotation. Each annotation will have one corresponding annotation
summary box. An annotation summary box will display the author of the annotation, the date the annotation was created,
the page the annotation was made on, the type of annotation, and the status of the annotation.

If the status is set to none the status will not be displayed on the annotation summary boxes. The left side of the
box will display a color corresponding to the color of the annotation. When an annotation summary box is clicked the
user will be taken to that annotation in the document and the annotation dialogue box will appear.

The user can delete and edit their annotations through the annotation summary or in the dialogue box. The user can also
reply to theirs' and others' annotations.

###### Delete

Clicking this button will delete the annotation:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar10.png %})

This button will not appear if the user is trying to delete another user's annotation.

The **Delete** button is located in the top right corner of the annotation summary box and above the **Edit** button.

###### Edit

Clicking this button will open the text area of the annotation summary box and allow the user to edit their annotation
comment:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar11.png %})

This button will not appear if the user is trying to edit another user's annotation.

The **Edit** button is located in the annotation summary box below the Delete button and above the **Reply** button.

###### Reply

Clicking this button allows the user to reply to an annotation:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar12.png %})

A user can reply to their annotation as well as other's annotations. If an annotation with a reply is deleted, the reply
will be orphaned.

The **Reply** button is located in the annotation summary box below the **Edit** button.

#### Search

Clicking on the search tab will display the search tab which includes a search text box and arrows to move through the
search matches:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar13.png %})

##### Text Search

The text search box allows the user to search for text in the document:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar14.png %})

It does not search through annotation summary boxes or annotation dialogue boxes. When a user inputs text into the
search box, matching results will appear below the text search box. The results will be highlighted on the document.
The result the user is currently viewing will be highlighted a different color than the other results.

The matching result box that is in view has a corresponding color to the result text on the document. The text search
box is not case-sensitive.

##### Match Whole Words Only

Clicking this button will only display the results which match the whole word searched for in the text search box:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar15.png %})

For example, if the user searches for the word `the` with the **Match Whole Words Only** button activated, words such as
`them` or `there` will not appear in the search results.

The button is located to the right of the text search box and to the left of the **Previous Result** button.

##### Previous Result

Clicking this button will display the previous matching result from the text search:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar16.png %})

If there are no results previous to the result currently in view the button will not be in use.

This button is located to the right of the **Match Whole Words Only** button and to the left of the **Next Result** button.

##### Next Result

Clicking this button will display the next matching result from the text search:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar17.png %})

If there are no results after the result currently in view the button will not be in use.

This button is located to the right of the **Previous Result** button.

#### Participants

Clicking on the **Participants** tab will display the participants tab which includes a list of the current users and
a chat box that allows the user to chat with the other users viewing the document:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar18.png %})

> **Note:** The **Participants** tab only appears when "Collaboration Mode" is active, and the user is connected to the collaboration server.

##### Participants List

This section of the **Participants** tab shows the list of the current users viewing the document:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar19.png %})

When a new user starts viewing the document, their name will be added to the bottom of the list. When a user stops
viewing the document, their name will be removed from the list.

##### Following

This section of the Participants tab allows the user to follow another user when they are scrolling.

###### Follower

A user can follow another user by clicking on the other user's name:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar20.png %})

The user will jump to the page of the user they are following. The zoom level will also change to match that of the
followee. A icon will be displayed next to the name of the user they are following, and a notification will pop up at
the bottom of the page that says which user is being followed. The user can unfollow the user by clicking on the other
user's name.

###### Followee

A user will be notified that they are being followed by another user. An icon will be displayed next to the name of the
user that is following them, and a notification will pop up at the bottom of the page that says the user is being followed:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar21.png %})

The user can stop others from following them by clicking on the other user's name or clicking the **Stop All** button
in the notification.

> **Note:** The followee cannot follow another user while they are being followed.

##### Activate Chat

This section of the **Participants** tab allows the user to activate the chat box:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar22.png %})

The chat box is activated if the button is blue. The user can disable the chat box by clicking the **Activate Chat** button.
The button will turn grey and disable the text input box.

This button is located below the **Participants** List, to the right of the **Start Zoom Call** button, and above the Chat Box.

##### Start Zoom Call

The zoom integration feature allows a user to start a Zoom call within the Enterprise Viewer window between everyone
that is viewing the same document:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar23.png %})

The Zoom call can be recorded and saved back to the user's repository.

The **Start Zoom Call** button is located to the right of the **Activate Chat** button and to the left of the
**Start Microsoft Teams Call** button.

##### Start Microsoft Teams Call

The team integration feature allows a user to start a Microsoft Teams call within the Enterprise Viewer window between
everyone that is viewing the same document:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar24.png %})

The Microsoft Teams call can be recorded and saved back to the user's repository.

The **Start Microsoft Teams Call** button is located to the right of the **Start Zoom Call** button.

##### Chat Box

This section of the **Participants** tab allows the user to view the conversation with the other users who are also
currently viewing the document:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar25.png %})

Each new message that a user sends contains the user's name, the time at which they sent the message, and the content
of the message itself.

#### Send

The **Send** button allows the user to send a message of their own composition to the other participants of the
conversation:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar26.png %})

This button is located at the bottom right corner of the **Participants** tab, below the chat box.

### Left Sidebar

The left sidebar displays the thumbnails, bookmarks, and the attachments. It is located to the left of the document and below the toolbar.

#### Hide Sidebar

The **Hide Sidebar** button allows the user to hide the sidebar containing the list of bookmarks. When the button is
clicked, the sidebar will collapse into the left side of the Enterprise Viewer window. When the button is clicked again,
the sidebar will expand back into view:

![Img Txt]({% link enterprise-viewer/images/aev-right-sidebar1.png %})

This button is located in the upper right corner of the sidebar.

#### Thumbnails

The thumbnails sidebar displays all the thumbnails of the document, if available:

![Img Txt]({% link enterprise-viewer/images/aev-left-sidebar1.png %})

Clicking on an entry in the list will take the user to the page the user selected. Thumbnails are unavailable for
large documents.

It is located on the left side of the Enterprise Viewer window.

##### Annotation Indicator

An annotation indicator will appear on the page's thumbnail if an annotation was made on that page:

![Img Txt]({% link enterprise-viewer/images/aev-left-sidebar2.png %})

If no annotations have been made on the page, then an annotation indicator will not be displayed on the thumbnail:

![Img Txt]({% link enterprise-viewer/images/aev-left-sidebar3.png %})

##### User Icon

A user icon will appear on the thumbnail of the page a collaborator is on:

![Img Txt]({% link enterprise-viewer/images/aev-left-sidebar4.png %})

The icon will have the initials of the collaborator and will display the full name when the user hovers over the icon.
Multiple icons will appear as users view the same page.

#### Bookmarks

The bookmarks sidebar displays all the bookmarks that the document has, if available:

![Img Txt]({% link enterprise-viewer/images/aev-left-sidebar5.png %})

Clicking on an entry in the list will take the user to the section of the document where the bookmark begins.

It is located on the left side of the **Enterprise Viewer** window.

##### Expand All Bookmarks

The **Expand All Bookmarks** button allows the user to expand all the sub-lists in the bookmarks list in order for the
user to see all bookmarks in all categories:

![Img Txt]({% link enterprise-viewer/images/aev-left-sidebar6.png %})

This button is located in the top right corner of the **Bookmarks** sidebar and to the left of the
**Collapse All Bookmarks** button.

##### Collapse All Bookmarks

The **Collapse All Bookmarks** button allows the user to collapse all the sub-lists in the bookmarks list in order for
the user to see only the categories of bookmarks:

![Img Txt]({% link enterprise-viewer/images/aev-left-sidebar7.png %})

This button is located in the top right corner of the **Bookmarks** sidebar, to the right of the **Expand All Bookmarks**
button, and below the **Hide Sidebar** button.

#### Internal Links

Internal Links allow the user to jump to different places within the document:

![Img Txt]({% link enterprise-viewer/images/aev-left-sidebar8.png %})

An internal link will be highlighted light blue when a user hovers over it.

#### Attachments

The **Attachments** sidebar displays the attached documents that the document has, if any:

![Img Txt]({% link enterprise-viewer/images/aev-left-sidebar9.png %})

If there are no attached documents, the **Attachments** sidebar tab will not be displayed. Clicking on an entry in the
list will automatically download the attached document.

The **Attachments** sidebar is located on the left side of the **Enterprise Viewer** window.

#### Document List

The **Document List** sidebar displays documents that have been added to the document list, if any:

![Img Txt]({% link enterprise-viewer/images/aev-left-sidebar10.png %})

If no documents were added to the list, the **Document List** sidebar will not be displayed. The document list allows
you to easily switch between documents in Enterprise Viewer. To switch to a new document in Enterprise Viewer, click on
a document in the list.

The **Document List** sidebar is located on the left side of the **Enterprise Viewer** window.

> **Note:** The user will not be able to see the previous document in the document list unless it is added.

## Redact Content Interface

This is where document navigation and zooming occur, and where redactions can be created, saved, and more information on Enterprise Viewer is found.

### Toolbar

The toolbar contains all the core functionality to Enterprise Viewer in **Redact Content** mode:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar1.png %})

It is located at the top of the **Enterprise Viewer** window.

Dark grey buttons cannot be used until certain actions are made. A button that is in use will have a blue interior.

#### Manual Page Navigation

Manually entering a value into this text field and then hitting the **Enter** key will navigate to the new page number:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar2.png %})

If the page number entered is not a number, this value gets reset to the current page. If the page number entered is
lower than the first page, the user is navigated to the first page. If the page number entered is higher than the last
page, the user is navigated to the last page.

This text field is located to the right of the Enterprise Viewer logo and to the left of the **Fit to Height** button.

#### Total Number of Pages

This is a non-editable field denoting the total number of pages for the document.

#### Fit to Height

Clicking the **Fit to Height** button automatically calculates the zoom level to make the window show the entire height
of the document:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar3.png %})

This does not take into account the width of the document, and thus scroll bars may appear horizontally depending on
the page's aspect ratio against the size of the window.

The **Fit to Height** button is located to the right of the **Manual Page Navigation** text field and to the left of
the **Fit to Width** button.

#### Fit to Width

Clicking the **Fit to Width** button automatically calculates the zoom level to make the window show the entire width
of the document:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar4.png %})

This does not take into account the height of the document, and thus scroll bars may appear vertically depending on the
page's aspect ratio against the size of the window.

The **Fit to Width** button is located to the right of the **Fit to Height** button and to the left of the **Next Page**
button. The **Fit to Width** button is to the left of the **Zoom In** button if the **Next Page** button is not
displayed in the toolbar.

#### Next Page

Clicking the **Next Page** button takes the user to the next page of the document:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar5.png %})

The button will become disabled once the user reaches the end of the document.

The **Next Page** button is located to the right of the **Fit to Width** button and to the left of the **Previous Page**
button.

> **Note:** This feature is unavailable if the document does not have more than one page.

#### Previous Page

Clicking the **Previous Page** button takes the user to the previous page of the document:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar6.png %})

The button will become disabled once the user reaches the beginning of the document.

The **Previous Page** button is located to the right of the **Next Page** button and to the left of the **Zoom In**
button.

> **Note:** This feature is unavailable if the document does not have more than one page.

#### Zoom In

Clicking the **Zoom In** button zooms in using increments of ten:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar7.png %})

While zooming in, the current middle of the page will remain in the middle.

If the target zoom level is above the maximum zoom level, the zoom is set to the maximum zoom level. This is set for
performance and usability reasons.

The **Zoom In** button is located to the right of the **Previous Page** button and to the left of the **Zoom Out**
button. The **Zoom In** button is to the right of the **Fit to Width** button if the **Previous Page** button is not
displayed in the toolbar.

#### Zoom Out

Clicking the **Zoom Out** button zooms out using increments of ten:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar8.png %})

While zooming out, if possible, the current middle of the page will remain in the middle (unless zooming out reveals an
image that does not need to be scrolled).

If the target zoom level is below the minimum zoom level, the zoom is set to the minimum zoom level. This is set for
performance and usability reasons.

The **Zoom Out** is located to the right of the **Zoom In** button and to the left of the **Save** button.

#### Save

Clicking the **Save** button will save any new or modified redactions to the server, as well as refresh any unmodified
redactions from other users that have been updated:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar9.png %})

The **Save** button is located to the right of the **Zoom In** button and to the left of the **Undo** button.

#### Selection Tool

The **Selection Tool** button is the default cursor when opening Enterprise Viewer and signifies that the mouse does
not do anything out of the ordinary:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar10.png %})

The **Selection Tool** button is located to the right of the **Save** button and to the left of the **Draw Redaction**
button.

#### Draw Redaction

Clicking the **Draw Redaction** button allows the user to draw a redaction in a specific area of the page:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar11.png %})

Redactions are drawn in the form of rectangles. Once the cursor is selected, the user can click anywhere on the page to
start the redaction. The user can then drag the mouse to anywhere else on the page to put the other corner of the
redaction.

A dim gray rectangle will be drawn from one point to the other as a preview of what the redaction will look like.
Dialog boxes are anchored in the beginning of the redaction.

The annotation comment from the dialog box will appear on the redacted area once the redaction is saved:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar12.png %})

The redacted area will become dark grey with white text if there is an annotation comment, otherwise it will turn black.

The **Draw Redaction** button is located to the right of the **Save** button and to the left of the **Text Redaction**
button.

#### Text Redaction

Clicking the **Text Redaction** button allows the user to redact text in a document:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar13.png %})

Once the cursor is selected, the user can click on the text they wish to redact. The user can then drag the mouse over
the text to redact it until the mouse is released. The user may redact multiple lines. Certain text such as Social
Security numbers will be redacted automatically.

The annotation comment from the dialog box will appear on the redacted area once the redaction is saved:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar15.png %})

The redacted area will become dark grey with white text if there is an annotation comment, otherwise it will turn black.

The **Text Redaction** button is located to the right of the **Draw Redaction** button and to the left of the **Help**
button.

#### Help

The **Help** button is used to give the user more information regarding Enterprise Viewer:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar16.png %})

When this button is clicked a new tab in the browser will open with Alfresco information regarding services and
description of the Enterprise Viewer.

The **Help** button is located to the right of the **Text Redaction** button and to the left of the **Load Time** text.

#### Load Time

The **Load Time** text shows the user how many seconds it took to load the document:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar17.png %})

The user can see more details when clicking on the text:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar18.png %})

The load time takes into consideration the time it took the user to login, the browser JavaScript load time, the time it
took to retrieve document information, the time it took to display the document, and the document's size. The user can
copy the load time information into their clipboard by clicking the **Copy to Clipboard** button found in the load time
information window.

The **Load Time** text is located to the right of the **Help** button.

### Right Sidebar

The right sidebar displays the annotation summary and search tabs. It is to the right of the document and below the
toolbar.

#### Hide Sidebar

The **Hide Sidebar** button allows the user to hide or show the sidebar depending upon the current state of the view:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar19.png %})

By default, the sidebar is in view. When clicked the sidebar will be hidden from the display. When the sidebar is not
in view, the button can be clicked to show the sidebar, and it will then reappear in its default position.

The **Hide Sidebar** button is located in the upper right corner of the sidebar.

#### Annotation Summary

The annotation summary tab is used to show the summaries of the redactions that have been made in the document:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar21.png %})

The user can filter through the redactions and view the summaries in this tab:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar20.png %})

##### Filter Text Box

The **Filter** text box allows the user to sort through the annotation summaries efficiently:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar29.png %})

When the user types in the text box, the annotation summary boxes will be sorted. The annotation summary boxes with
text matching the user's input will appear below the filter search box. The filter field will filter on the:

* Username of the annotation creator
* Contents of the annotation comment
* Date of the comment
* Page Number
* Redaction type (ex: Redaction, Text Redaction)

This **Filter** text box is located at the top of the **Annotation Summary** above the summaries.

##### Filters

The **Filters** button allows the user to filter through the annotation summary boxes based upon the status and author:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar30.png %})

When clicked, a checkbox list will appear displaying status, author(s), and type options for user to select. Multiple
statuses, authors and/or types can be selected. The filters box can be used with the filter text box.

The **Filters** button is located on the immediate right of the **Filter** text box.

##### Clear Filters

The **Clear Filters** button is used to clear all filters from the filter text box and the filters button:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar31.png %})

When clicked the text in the filters text box will be cleared as well as the selections made in the filters list.
The clear filters button will appear to the right of the filter text box when there is text in the filter text box or
when a selection is made in the filters list.

##### Annotation Summary Boxes

The **Annotation Summary** boxes appear in the sidebar below the filter text box:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar32.png %})

The **Annotation Summary** boxes are used to display information regarding each redaction. Each redaction will have one
corresponding annotation summary box. An annotation summary box will display the author of the redaction, the date the
redaction was created, the page the redaction was made on, the type of redaction, and the status of the redaction.

If the status is set to none the status will not be displayed on the annotation summary boxes. The left side of the box
will display a color corresponding to the color of the annotation. When an annotation summary box is clicked the user
will be taken to that redaction in the document and the redaction dialogue box will appear.

#### Search

Clicking on the **Search** tab will display the search tab which includes a search text box, arrows to move through
the search matches, and a redact search result option:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar22.png %})

##### Bulk Redaction

The reason for redaction box and redact results button allows the user to redact all the search results:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar23.png %})

The user can type their reason for redacting the search results in the reason for redaction box. This reason will be
applied to each search result redaction. The redactions will be displayed in the annotation summary. A preview of the
redactions can be seen in the document.

The **Bulk Redaction** feature is located below the **Text Search** box and above the search results.

##### Text Search

The **Text Search** box allows the user to search for text in the document:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar24.png %})

It does not search through annotation summary boxes or annotation dialogue boxes. When a user inputs text into the
search box, matching results will appear below the text search box. The results will be highlighted on the document.
The result the user is currently viewing will be highlighted a different color than the other results. The matching
result box that is in view has a corresponding color to the result text on the document. The text search box is
not case-sensitive.

##### Match Whole Words Only

Clicking the **Match Whole Words Only** button will only display the results which match the whole word searched for
in the text search box:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar25.png %})

The button is located to the right of the **Text Search** box and to the left of the **Previous Result** button.

##### Previous Result

Clicking the **Previous Result** button will display the previous matching result from the text search:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar26.png %})

If there are no results previous to the result currently in view, then the button will not be in use.

The **Previous Result** button is located to the right of the **Text Search** box and to the left of the
**Match Whole Words Only** button.

##### Next Result

Clicking the **Next Result** button will display the next matching result from the text search:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar27.png %})

If there are no results after the result currently in view the button will not be in use.

The **Next Result** button is located to the right of the **Previous Result** button.

### Left Sidebar

This sidebar contains the bookmarks.

#### Bookmarks

The bookmarks sidebar displays all the bookmarks that the document has, if available:

![Img Txt]({% link enterprise-viewer/images/aev-redact-content-interface-toolbar28.png %})

Clicking on an entry in the list will take the user to the section of the document where the bookmark begins.

It is located on the left side of the **Enterprise Viewer** window.

## Edit Pages Interface

This is where document navigation and zooming occur, where the user can split the PDF, delete pages, rotate pages,
and section the document, and where more information on Enterprise Viewer is found.

### Toolbar

The toolbar contains all the core functionality to Enterprise Viewer in **Edit Pages** mode.

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar1.png %})

It is located at the top of the Enterprise Viewer window.

Dark grey buttons cannot be used until certain actions are made. A button that is in use will have a blue interior.

#### Manual Page Navigation

Manually entering a value into this text field and then hitting the **Enter** key will navigate to the new page number:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar2.png %})

If the page number entered is not a number, this value gets reset to the current page. If the page number entered is
lower than the first page, the user is navigated to the first page. If the page number entered is higher than the last
page, the user is navigated to the last page.

This text field is located to the right of the Enterprise Viewer logo and to the left of the **Fit to Width** button.

#### Total Number of Pages

This is a non-editable field denoting the total number of pages for the document.

#### Fit to Width

Clicking this button automatically calculates the zoom level to make the window show the entire width of the document:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar3.png %})

This does not take into account the height of the document, and thus scroll bars may appear vertically depending on the
page's aspect ratio against the size of the window.

The **Fit to Width button** is located to the right of the *Manual Page Navigation* text field and to the left of the
**Fit to Height** button.

#### Fit to Height

Clicking this button automatically calculates the zoom level to make the window show the entire height of the document:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar4.png %})

This does not take into account the width of the document, and thus scroll bars may appear horizontally depending on the
page's aspect ratio against the size of the window.

The **Fit to Height** button is located to the right of the **Fit to Width** button and to the left of the **Next Page**
button. The **Fit to Height** button is to the left of the **Zoom Out** button if the **Next Page** button is not
displayed in the toolbar.

#### Next Page

Clicking this button takes the user to the next page of the document:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar5.png %})

The button will become disabled once the user reaches the end of the document.

The **Next Page** button is located to the right of the **Fit to Height** button and to the left of the
**Previous Page** button.

> **Note:** This feature is unavailable if the document does not have more than one page.

#### Previous Page

Clicking this button takes the user to the previous page of the document:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar6.png %})

The button will become disabled once the user reaches the beginning of the document.

The **Previous Page** button is located to the right of the **Next Page** button and to the left of the **Zoom Out**
button.

> **Note:** This feature is unavailable if the document does not have more than one page.

#### Zoom Out

Clicking this button zooms out in increments of ten:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar7.png %})

While zooming out, if possible, the current middle of the page will remain in the middle (unless zooming out reveals an
image that does not need to be scrolled).

If the target zoom level is below the minimum zoom level, the zoom is set to the minimum zoom level. This is set for
performance and usability reasons.

The **Zoom out** button is located to the right of the **Previous Page** button and to the left of the **Zoom In**
button. The **Zoom Out** button is to the right of the **Fit to Height** button if the **Previous Page** button is not
displayed in the toolbar.

#### Zoom In

Clicking this button zooms in using increments of ten:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar8.png %})

While zooming in, the current middle of the page will remain in the middle.

If the target zoom level is above the maximum zoom level, the zoom is set to the maximum zoom level. This is set for
performance and usability reasons.

The **Zoom In** button is located to the right of the **Zoom Out** button and to the left of the **Save** button.

#### Save

Clicking this button will save any changes to the server, as well as refresh any unmodified annotations from other users
that have been updated:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar9.png %})

The **Save** button is located to the right of the **Zoom In** button and to the left of the **Split PDF** button.

#### Split PDF

Clicking the **Split PDF** button will prompt the user to select the pages for the split:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar10.png %})

The user can select the pages by clicking on the box in the upper left corner of the page or by typing the pages in the
blue notification located at the button of the screen. The selected pages will become green. The user then must click
the **Split PDF** button which is located in the notification. Doing so will create a new document with the selected
pages which has the same metadata and can be found in the same folder as the original document.

The **Split PDF** button is located to the right of the **Save** button and to the left of the **Delete Pages** button.

#### Delete Pages

Clicking the **Delete Pages** button will prompt the user to select the pages they wish to delete:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar11.png %})

The user can select the pages by clicking on the box in the upper left corner of the page or by typing the pages in the
blue notification located at the bottom of the screen. The selected pages will become red. The user then has to click the
**Delete Pages** button which is located in the notification.

The **Delete Pages** button is located to the right of the **Split PDF** button and to the left of the
**Rotate Page Counter-Clockwise** button.

#### Rotate Page Counter-Clockwise

Clicking this button will rotate all the pages counter-clockwise:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar12.png %})

If the user wants specific pages to rotate, the user must select them by clicking the box in the top left corner of the
page or by writing it in the range section of the notification in the bottom right corner.

The **Rotate-Page Counter-Clockwise** button is located to the right of the **Delete Pages** button and to the left of
the **Rotate Page Clockwise** button.

#### Rotate Page Clockwise

Clicking this button will rotate all the pages clockwise:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar13.png %})

If the user wants specific pages to rotate, the user must select them by clicking the box in the top left corner of the
page or by writing it in the range section of the notification in the bottom right corner.

The **Rotate Page Clockwise** button is located to the right of the **Rotate Page Counter-Clockwise** button and to the
left of the **Section Document** button.

#### Section Document {#section-doc-activate}

Clicking this button will allow the user to split the document into different sections:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar14.png %})

Sectioning is an efficient way to reorder large documents. A blue notification will appear in the bottom right corner where the user can name the section and select the range of pages for the section. The user must then select the **Create Section** button. The new section will appear in the left sidebar.

See [how to section a document]({% link enterprise-viewer/latest/using/index.md %}#section-docs).

The **Section Document** button is located to the right of the **Rotate Page Clockwise** button and to the left of the **Help** button.

#### Help

The **Help** button is used to give the user more information regarding Enterprise Viewer:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar15.png %})

When this button is clicked a new tab in the browser will open with Alfresco information regarding services and description of Enterprise Viewer.

The **Help** button is located to the right of the **Section Document** dropdown and to the left of the **Load Time**.

#### Load Time

The **Load Time** text shows the user how many seconds it took to load the document:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar16.png %})

The user can see more details when clicking on the text:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar17.png %})

The load time takes into consideration the time it took the user to login, the browser JavaScript load time, the time it took to retrieve document information, the time it took to display the document, and the document's size. The user can copy the load time information into their clipboard by clicking the **Copy to Clipboard** button found in the load time information window.

The **Load Time** text is located to the right of the **Help** button.

### Left Sidebar

This section covers the left side navigation bar in the Enterprise viewer.

#### Hide Sidebar

The **Hide Sidebar** button allows the user to hide the sidebar containing the list of sections:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar18.png %})

When the button is clicked, the sidebar will collapse into the left side of the Enterprise Viewer window. When the button is clicked again, the sidebar will expand back into view.

This button is located in the top right corner of the Sections sidebar.

#### Sections {#section-docs}

The **Sections** sidebar displays all the sections of the document, if available:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar19.png %})

Sectioning is an efficient way to reorder large documents. Unsectioned pages will be listed under *Unsectioned*. The pages belonging to each section are listed under the section's name. Clicking on an entry in the list in *Add Annotations* mode will take the user to the first page of the section.

See [how to activate the Section Document feature]({% link enterprise-viewer/latest/using/index.md %}#section-doc-activate) for more information.

It is located on the left side of the Enterprise Viewer window.

##### Creating a Section

The user can create a new section through the blue notification that appears in the bottom right corner:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar20.png %})

The user can name the section and type the range of pages for the section. The user must then select the
**Create Section** button in the notification. The new section will appear in the left sidebar.

##### Renaming a Section

Clicking this button allows the user to rename the section:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar21.png %})

A text box will appear under the section's name prompting the user to enter a new section name.

This button is located to the right of the section's name.

##### Edit Section

Clicking this button displays the thumbnails of the section:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar22.png %})

Thumbnails before reordering pages:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar23.png %})

The user can reorder the section by dragging the thumbnails to their desired positions:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar24.png %})

Thumbnails in new position with the pages reordered:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar25.png %})

The user must click the button again to exit thumbnail view.

This button is located to the left of the **Deleting a Section** button and below the **Clear All** button.

##### Deleting a Section

Clicking this button allows the user to delete the section:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar26.png %})

The pages from the deleted section will then be listed under *Unsectioned*.

This button is located to the right of the **Edit Section** button and below the **Clear All** button.

##### Reordering Sections

The user can reorder the sections by clicking on a section and dragging it to a new spot:

> **Note:** The user cannot reorder the sections if there are unsectioned pages.

##### Clear All

Clicking this button will clear all document sections and list the pages under *Unsectioned*:

![Img Txt]({% link enterprise-viewer/images/aev-edit-pages-interface-toolbar27.png %})

The user will be prompted by a question asking whether they are sure they want to clear all sections.

The **Clear All** button is located in the top right corner of the *Sections* sidebar below the **Hide Sidebar** button.

## Add Signatures Interface

This section covers the *Add Signatures* feature of the Enterprise Viewer.

### Toolbar

The toolbar contains all the core functionality to Enterprise Viewer in Signature mode:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar1.png %})

This is where document navigation and zooming occur, and signatures can be added, saved, and more information on
Enterprise Viewer is found.

It is located at the top of the Enterprise Viewer window.

Dark grey buttons cannot be used until certain actions are made. A button that is in use will have a blue interior.

#### Manual Page Navigation

Manually entering a value into this text field and then hitting the **Enter** key will navigate to the new page number:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar2.png %})

If the page number entered is not a number, this value gets reset to the current page. If the page number entered is
lower than the first page, the user is navigated to the first page. If the page number entered is higher than the last
page, the user is navigated to the last page.

This text field is located to the right of the Enterprise Viewer logo and to the left of the **Fit to Width** button.

#### Total Number of Pages

This is a non-editable field denoting the total number of pages for the document.

#### Fit to Width

Clicking this button automatically calculates the zoom level to make the window show the entire width of the document:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar3.png %})

This does not take into account the height of the document, and thus scroll bars may appear vertically depending on
the page's aspect ratio against the size of the window.

The **Fit to Width** button is located to the right of the *Manual Page Navigation* text field and to the left of the
**Fit to Height** button.

#### Fit to Height

Clicking this button automatically calculates the zoom level to make the window show the entire height of the document:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar4.png %})

This does not take into account the width of the document, and thus scroll bars may appear horizontally depending on
the page's aspect ratio against the size of the window.

The **Fit to Height** button is located to the right of the **Fit to Width** button and to the left of the
**Previous Page** button. The **Fit to Height** button is to the left of the **Zoom Out** button if the **Previous Page**
button is not displayed in the toolbar.

#### Previous Page

Clicking this button takes the user to the previous page of the document:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar5.png %})

The button will become disabled once the user reaches the beginning of the document.

The **Previous Page** button is located to the right of the **Fit to Height** button and to the left of the
**Next Page** button.

> **Note:** This feature is unavailable if the document does not have more than one page.

#### Next Page

Clicking this button takes the user to the next page of the document:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar6.png %})

The button will become disabled once the user reaches the end of the document.

The **Next Page** button is located to the right of the **Previous Page** button and to the left of the
**Zoom Out** button.

> **Note:** This feature is unavailable if the document does not have more than one page.

#### Zoom Out

Clicking this button zooms out in increments of ten:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar7.png %})

While zooming out, if possible, the current middle of the page will remain in the middle (unless zooming out reveals
an image that does not need to be scrolled).

If the target zoom level is below the minimum zoom level, the zoom is set to the minimum zoom level. This is set for
performance and usability reasons.

The **Zoom out** button is located to the right of the **Next Page** button and to the left of the **Zoom In** button.
The **Zoom Out** button is to the right of the **Fit to Height** button if the **Next Page** button is not displayed in
the toolbar.

#### Zoom In

Clicking this button zooms in using increments of ten:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar8.png %})

While zooming in, the current middle of the page will remain in the middle.

If the target zoom level is above the maximum zoom level, the zoom is set to the maximum zoom level. This is set for
performance and usability reasons.

The **Zoom In** button is located to the right of the **Zoom Out** button and to the left of the **Save** button.

#### Save

Clicking this button will save any new or modified annotations to the server, as well as refresh any unmodified
annotations from other users that have been updated:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar9.png %})

The **Save** button is located to the right of the **Zoom In** button and to the left of the **Selection Tool** button.

#### Selection Tool

The **Selection Tool** button is the default cursor when opening Enterprise Viewer and signifies that the mouse does
not do anything out of the ordinary:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar10.png %})

The **Selection Tool** button is located to the right of the **Save** button and to the left of the **Draw Signature**
button.

#### Draw Signature

Clicking this button allows the user to add a signature to the page:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar11.png %})

Once the cursor is selected, the user can click anywhere on the page to add a signature. The user will be prompted by a
popup window asking them to sign below. The user can clear the signature if needed. The user must click the insert
button of the popup window to insert the signature.

The **Draw Signature** button is located to the right of the **Selection Tool** button and to the left of the **Help**
button.

#### Help

The **Help** button is used to give the user more information regarding Enterprise Viewer:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar12.png %})

When this button is clicked a new tab in the browser will open with Alfresco information regarding services and
description of Enterprise Viewer.

The **Help** button is located to the right of the **Draw Signature** button and to the left of the *Load Time*.

#### Load Time

The **Load Time** text shows the user how many seconds it took to load the document:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar13.png %})

The user can see more details when clicking on the text:

![Img Txt]({% link enterprise-viewer/images/aev-add-sign-interface-toolbar14.png %})

The load time takes into consideration the time it took the user to login, the browser JavaScript load time, the time
it took to retrieve document information, the time it took to display the document, and the document's size. The user
can copy the load time information into their clipboard by clicking the Copy to Clipboard button found in the load time
information window.

The **Load Time** text is located to the right of the **Help** button.
