---
title: Alfresco Governance Services
---

Governance Services combines Records Management with Security Controls and Classification.

Governance Services is fully compliant with a baseline of DoD 5015.02. With Governance Services you can fully automate 
the record lifecycle from capture through retention to final destruction. Users can create records direct from any 
Alfresco Share site. On top of this security controls and classification give you complete control over who can see 
which records and when.
---
title: Administration of Governance Services
---

RM Admin Tools is where you configure the Records Management site.

The user who created the Records Management site is automatically made a member of the Records Management Administrator group. 
Other users can access different areas of the **RM Admin Tools** depending on the {% include tooltip.html word="capabilities" text="capabilities" %} given to the role that they're in.

## Opening Admin Tools

You can easily configure Governance Services using the Admin Tools.

> **Note:** The user who created the Governance Services site is automatically made a member of the Governance Services Administrator group. Other users can access different areas of the **Admin Tools** depending on the capabilities given to the role that they're in.

In a Governance Services site click **Admin Tools** to open the **Audit** page, with various other options available on the left-hand side. Click a tool to manage that part of your site.

## Audit

The Audit tool is used for external audits to demonstrate compliance to regulatory requirements, and for internal audits for 
process improvement.

It displays auditing information collected from the system to show whether business rules are being followed, and to ensure 
that any unauthorized activity can be identified and traced. This tool is especially important for systems that deal with 
classified information.

The Audit tool maintains a complete trace of all the actions on every record and cannot be altered. 
The information that is captured and stored includes:

* Any action on any record, folder, category, or the {% include tooltip.html word="fileplan" text="File Plan" %}
* The user who carried out the action
* The date and time of the action

The Audit tool displays by default when you access the RM Admin Tools.

### Running an audit

The Audit tool displays by default when you open the Records Management Console.

When you run an audit you can select to run a full audit or you can filter the results.

1. If you want to filter the audit results then choose from one or more of the following options:

    |Filter action|
    |-------------|
    |By default only the first 20 log entries are displayed. Use this option to select the number of displayed entries.|
    |Select from and to dates for actions to include in the audit.|
    |Click **Specify** and search for then select a user you want to audit, then click **Add**.|
    |Select an event type to audit. You can only select one event type.|

2. When you've selected the audit filters you want, click **Run Audit Report**.

    > **Note:** If you don't want to filter the results, then just click **Run Audit Report** without making any filter selections.

The most recent entries in the log (up to 20) display in chronological order. You can see who performed each event, the user's role, and when it was performed. You can also click a column header to sort the results.

> **Tip:** Click **Details** to see more information on a specific event.

### What's in an audit?

When you run an audit, you are provided with details of all the actions that have taken place in your Records Management site.

The type of action that is recorded in the audit log includes:

* Capture of all electronic records: file, declare, undeclared
* Re-categorization of an electronic record within the file plan: a move
* Any change to any {% include tooltip.html word="retentionschedule" text="retention schedule" %} (instructions): create, modify, destroy
* Any retention actions carried out by authorized roles: {% include tooltip.html word="cutoff" text="cut off" %}, retain, transfer, review, close folder, reopen folder
* The adding or removal of an object to a {% include tooltip.html word="fileplan" text="File Plan" %}
* Any change made to any metadata associated with File Plan or electronic records, for example, change to vital record indicator
* Amendment and deletion of metadata by a user
* Any internal or user event triggered by the system or by the user, for example, SUPERSEDED, GAO Audit, End of Fiscal Year, and so on
* Changes made to the access permissions
* Creation, amendment, or deletion of a user or group
* Changes made to the {% include tooltip.html word="capabilities" text="capabilities" %} (functional access permissions)
* Changes made to supplemental markings
* Export and import
* Deletion / destruction of records
* Changes to the auditing levels and settings
* Search operations carried out by users
* Creating or deleting a hold

### Stopping and starting the audit log

If you have an audit running then you can stop it and restart it later.

1. Click **Stop** in the Audit tool of the **Admin Tools** if you have an audit running.

    A dialog box prompts you to confirm the action.

2. Click **Yes**.

    The auditing tool stops capturing and storing the activity in the Records Management system.

3. To start the audit log again, click **Start**. When prompted, click **Yes** to confirm the action.

### Filing the audit log as a record

When you've run an audit log you then have the option to file it as a record.

1. When you've run an audit, click **File as Record** in the Audit tool of the RM Admin Tools.

2. Choose the destination folder for the audit record.

3. Click **OK**.

    A message confirms that the audit log has been filed as a record in the selected folder in the File Plan.

    > **Note:** You'll need to add any required metadata before the record can be completed.

4. Click **OK** to dismiss the message. You can also click **View Record** to display the audit report in the Records Management site.

### Exporting the audit log

You can export the audit log which is useful for archiving it regularly so that you can examine or analyze system activity.

When you export the audit log, this doesn't affect the audit log in the system.

When you've run an audit, click **Export** in the Audit tool of the RM Admin Tools. Depending on your browser you'll be prompted to open or save the file or it will be saved automatically. The exported audit log is an HTML file.

### Viewing the full log

You can view the full contents of the log file in a separate window. From there you can save an HTML version of the 
report on your computer or in the Records Management File Plan.

1. When you've run an audit, click **View Recent Log** in the Audit tool of the RM Admin Tools.

    A separate window opens displaying the audit log.

2. You can save the log report in one or both of the following ways:

    * Click **Export** to save the report to your computer.
    * Click **File as Record** to file the report in the File Plan.
    
    > **Note:** If you select **File as Record** you'll need to add any required metadata before the record can be completed.

3. Close the window.

### Clearing the audit log

If you've run an audit you can quickly clear it to delete all captured actions.

1. When you've run an audit, click **Clear Full Log** in the Audit tool of the RM Admin Tools.

    A message prompts you to confirm the action.

2. Click **Yes** to clear the audit log.

## Custom metadata

Records Management has default sets of metadata for records, record {% include tooltip.html word="category" text="categories" %}, record folders, and non-electronic documents.

You can also add custom metadata that you can associate with each of these different types of records management objects.

You can choose from text fields, date pickers, check boxes, and if you've set up a 
[list of values](#list-of-values), selection menus.

If required you can choose to make specific custom data mandatory, so that users have to include it when they are 
completing a record.

> **Note:** If you add mandatory metadata to a records management object type that already has existing instances, the newly mandatory metadata won't be applied to existing instances, as this could cause inconsistencies with the File Plan.

### Creating custom metadata

You can create custom metadata for record categories, record folders, records, and non-electronic documents. 
When you create custom metadata, you can't delete it.

1. Click **Custom Metadata** in the RM Admin Tools.

2. Select an option in the Object column: **Non-Electronic Document**, **Record**, **Record Category**, or **Record Folder**.

    The right column lists any custom metadata that's already been defined for the selected object.

3. Click **New**.

    The **New Metadata** page displays.

4. Type a name for the metadata in the **Name** field.

    This name is used as the label on the Edit Metadata page.

5. Select a data **Type**.

    The type can be of the following values:

    |Type|Description|
    |--------|---------------|
    |Text|Adds a text field to the Edit Metadata page. When you select this option, you can select the **Use selection list** check box, so instead of a text field there will be a selection menu of the list created with the [List of Values tool](#list-of-values).|
    |Check box|Adds a check box to the Edit Metadata page.|
    |Date|Adds a date field to the Edit Metadata page.|

    > **Note:** The **Use selection list** option is only available if a list has been created with the [List of Values tool](#list-of-values).

6. To configure this metadata field as a selection menu:

    1. Select the **Use selection list** check box.

    2. Select a list name from the menu.

7. Select the **Mandatory** check box to set this metadata to be mandatory on the Edit Metadata page.

    > **Note:** Mandatory metadata must be completed before a record can be set to completed.

8. Click **Create**.

The new metadata displays in the right column of the Custom Metadata page.

### Editing custom metadata

You can easily edit any custom metadata that you've set up.

1. Click **Custom Metadata** in the RM Admin Tools.

2. Select an option in the Object column: **Non-Electronic Document**, **Record**, **Record Category**, or **Record Folder**.

    The right column lists any custom metadata that's already been defined for the selected object.

3. Click **Edit** to the right of the metadata you want to work with.

    The Edit Metadata Property page displays.

4. Make the required changes then click **Save**.

    > **Note:** You can't edit the type (text, boolean or date) or the Mandatory option for existing custom metadata.

## Define roles

Records Management roles and {% include tooltip.html word="capabilities" text="capabilities" %} control what functionality is available to users.

Alfresco has several default roles that users and groups can be assigned to:

* Records Management Administrator
* Records Management Power User
* Records Management Records Manager
* Records Management Security Officer
* Records Management User

> **Note:** There are also In-Place Readers and In-Place Writers roles but you can't assign users or groups to these in the RM Admin Tools.

These are displayed when you open the Define Roles tool. You can create as many more roles as you need.

Capabilities control what each role can do in the Records Management system, and with nearly 60 unique capabilities to choose from, they can vary hugely between roles.

> **Tip:** The role of Records Management Administrator has all capabilities assigned to it, so take a look at this to see the full list of capabilities available.

You assign users and groups who will all require the same levels of functionality to a role (a user can be assigned to multiple roles at the same time). Assign users and groups to roles using the [Users and Groups tool](#users-and-groups). You can manage roles to change the capabilities that they have.

Capabilities don't conflict and are not hierarchical. A user can be granted a single capability and that capability will not grant any further capabilities. Any user can have zero or more capabilities within the system. A user that has no capabilities is effectively barred from the Records Management system.

> **Tip:** Remember that roles and capabilities are different to permissions, which are set against folders and categories directly in the File Plan.

### Viewing the capabilities for a role

All existing roles are displayed when you open the Define Roles tool.

1. Click **Define Roles** in the RM Admin Tools.

2. In the Roles column, select a role to view.

    The list of capabilities assigned to that role display in the Capabilities column.

3. Select another role to view its assigned capabilities.

### Adding new roles

There are five default Records Management roles, but you can add as many more as you need.

1. Click **Define Roles** in the RM Admin Tools.

2. Click **New Role**.

    The New Role page displays all available capabilities, which are organized into groups. You can choose individual items or an entire group to define the {% include tooltip.html word="category" text="categories" %} for the role you're creating.

3. Enter a name for the role.

4. Select the capabilities that you wish to apply to the role.

    1. To select an individual capability within a group, click the check box.

    2. To select a group of capabilities, click **Select All**.

        For example, to select all capabilities for controlling folders, click **Select All** for the Folder Control group.

    > **Note:** A new role should at a minimum be given the **View Records** capability so that it can at least view records in the File Plan.

5. Click **Create**.

The new role displays in the list of available roles. Now you can add users and groups to the role.

### Editing a role

You can edit a role whenever you need to make changes to its name or the capabilities it's been assigned.

1. Click **Define Roles** in the RM Admin Tools.

2. In the Roles column, select the role you want to edit.

3. Click **Edit Role**.

4. Edit the name and capabilities as required.

5. Click **Save**.

### Deleting a role

You can delete a role whenever you need to.

> **Important:** Once a role is deleted all users and groups in the role will no longer have access to Records Management.

1. Click **Define Roles** in the RM Admin Tools.

2. In the Roles column, select the role you want to delete.

3. Click **Delete Role**.

    A message prompts you to confirm the action.

4. Click **OK**.

## Email Mappings

One of the many ways that you can file data in the Records Management system is by storing inbound emails as records.

The IMAP protocol allows email applications that support IMAP to connect to and interact with Alfresco repositories 
directly from the mail application.

Alfresco has multiple maps between email headers and Alfresco metadata properties set up by default. 
You can view these with the Email Mappings tool.

This means that when an email is saved to Records Management, metadata from the email header is captured and mapped to 
metadata for the record.

For example, an email `Subject` heading is mapped by default to the Alfresco property `title`. 
This is displayed as in the Email Mappings tool as `messageSubject` to `cm:title`. 
The email header field `messageSubject` is on the left and is separated by the word “to”, 
which indicates that it is mapped to a property `cm:title`.

When you're viewing emails within the Records Management system, the `title` property shows the email’s `Subject` heading.

As well as the default mappings, you can also add your own or delete existing ones.

### Adding an email map

The pre-defined email mappings cover the most commonly used email headers. You can include additional email header 
mappings using the Email Mappings tool.

1. Click **Email Mappings** in the RM Admin Tools.

2. Type the email header field in the **Map** box or select one from the menu.

3. Click **Select** to select an Alfresco property name.

    You can select an Alfresco property or a custom property.

4. Click **Add**.

    The new mapping displays in the list of email mappings.

### Deleting an email map

You can delete an email map whenever it's no longer needed.

1. Click **Email Mappings** in the RM Admin Tools.

2. Browse the list to find the mapping you want to delete.

3. Click **Delete** then click **Yes** to confirm.

    This removes the mapping from the list.

## Events

The life cycle of a record is controlled by either time-based or event-based triggers that are set in the retention schedule. 
You can edit events and create entirely new ones. When you create an event, you can't delete it.

Events are triggered when actions occur on a record or folder, such as it being versioned, {% include tooltip.html word="cutoff" text="cut off" %}, {% include tooltip.html word="recordfolderclosed" text="closed" %}, superseded, 
or obsoleted. All events belong to one of the following event types:

* *Simple* - a standard Records Management event
* *Obsoleted* - an item is invalid or out of date and is generally not replaced
* *Superseded* - an item is invalid or out of date and is to be replaced with a current record
* *Cross Referenced Record Transferred* - a record that is cross referenced is transferred

The following default events are available in Records Management:

* Abolished - *Simple*
* All Allowances Granted Are Terminated - *Simple*
* Case Closed - *Simple*
* Case Complete - *Simple*
* No longer needed - *Simple*
* Obsolete - *Obsoleted*
* Redesignated - *Simple*
* Related Record Transferred to Inactive Storage - *Cross Referenced Record Transferred*
* Separation - *Simple*
* Study Complete - *Simple*
* Superseded - *Superseded*
* Training Complete - *Simple*
* WGI action complete - *Simple*

### Creating a new event

Records Management provides an extensive list of events, but it's easy to add to these.

1. Click **Events** in the RM Admin Tools.

2. Click **New Event**.

    The New Event page displays.

3. In the **Name** field, enter a name for the event.

4. In the **Type** field, select the event type from the following:

    * *Simple* - a standard Records Management event that must be manually completed by a user
    * *Obsoleted* - an event that is automatically completed when a record is obsoleted by another record based on their relationship
    * *Superseded* - an event that is automatically completed when a record is superseded by another record based on their relationship
    * *Cross Referenced Record Transferred* - an event that is automatically completed when a cross referenced record (based on their relationship) is transferred
    * *Versioned* - an event that is automatically completed when a record is versioned

5. Click **Save**.

The new event displays on the Events page.

### Editing an event

You can edit all events, whether they are system defaults or ones that you've created.

> **Note:** It's recommended that you don't edit events that are actively in use on your system.

1. Click **Events** in the RM Admin Tools.

2. Browse the list to find the event you want to edit.

3. Click **Edit**.

    The Edit Event page displays.

4. Change the details as necessary.

5. Click **Save**.

## List of values

When users edit metadata for folders and records, one of the field types available is a list of values.

Two predefined lists are provided with Records Management:

* *Supplemental Markings*: security categories that are recommended by the DoD 5015.2
* *Transfer Locations*: the names of your storage locations

> **Note:** These are available for both standard and {% include tooltip.html word="dod50152std" text="DoD 5015.2-STD" %} compliant File Plans.

You need to provide values for these lists so that users can select from them when they edit metadata. 
The recommended values for Supplemental Markings are Confidential, Restricted, Secret, Top Secret and Unclassified.

You can also set up new lists as needed, and you can use these lists when you [create custom metadata](#creating-custom-metadata).

Where the value is a text string, you can also enter the value using a list of values menu. For example, 
on the Edit Metadata page, you enter the value for the Mimetype field by selecting a value from the menu.

> **Important:** Administrators can see all security marks and other metadata when browsing the repository (for example, using the Node Browser).

### Creating a list of values

Creating a list is a two step process. First you create the empty list and then you edit it to add the values. 
Once you create a list, you cannot delete it.

1. Click **List of Values** in the RM Admin Tools.

2. Click **New List**.

    The New List dialog box displays.

3. In the **Name** field, enter a name for the list.

    > **Note:** The list name must be unique.

4. Click **OK**.

The name of the new list displays on the Lists page.

### Editing a list of values

Use the Edit feature to add and delete values for a list. You can also control the user and group access to 
the values in the list.

1. Click **List of Values** in the RM Admin Tools.

2. Locate the list you want to modify, and then click **Edit**.

    The Edit List page displays.

3. To add values to the list:

    1. In the empty field at the top of the page, type the new value.

    2. Click **Add**.

        The value name displays in the Values table.

    > **Note:** You can click **Delete** next to a value to remove it from the list.

4. To control the user and group access to the individual values in the list:

    1. In the Values table, click the value you want to set access for.

        The selected value is highlighted.

    2. On the right side of the page, click **Add**.

        The Add Access dialog box displays.

    3. In the search field, type the full or partial name of a user or group.

        You must enter at least three (3) characters.

    4. Click **Search**.

        A list of users and groups matching the search criteria displays.

    5. Click **Add** to the right of the user or group you want to have access to the selected value.

        The user or group displays in the right column. You can add as many users and groups as required.

    > **Note:** Only users that you give access to here will be able to see the value when they edit metadata.

5. When you have finished editing the values and access, click **Done** to save all changes.

### Renaming a list of values

If you need to rename a list of values then it's very easy to do.

1. Click **List of Values** in the RM Admin Tools.

2. Locate the list you want to rename, and then click **Rename**.

    The Rename List dialog box displays.

3. Edit the list name and then click **OK**.

The modified name displays on the Lists page.

## Relationships

In the File Plan you can create relationships between records.

There are two types of relationships that can be established between records:

* *Bi-directional* - a two-way relationship such as a cross-reference
* *Parent/Child* - a relationship where the child is dependant upon its parent, such as when the parent is superseded by the child

The names given to individual relationships are based on the different types of referencing, and are what makes each one unique.

You can see the default relationship types that are included in Records Management and you can create new and manage 
existing relationships.

### Creating a new relationship

The RM Admin Tools has several default relationships. You can add more relationships, but once you create a relationship 
you can't delete it.

1. Click **Relationships** in the RM Admin Tools.

2. Click **New Relationship**.

    The New Relationship page displays.

3. Select the relationship type:

    * Bi-directional
    * Parent/Child

4. If the relationship type is Bi-directional, complete the Label field, and if the relationship type is Parent/Child, complete the Source and Target fields.

    The values you enter display in the File Plan when a user creates the reference.

    > **Tip:** The existing default values give good examples of how to label relationships.

5. Click **Save**.

    The new relationship appears in the list.

### Editing a relationship

You can't delete relationships once they're created, but you can edit them.

1. Click **Relationships** in the RM Admin Tools.

2. Locate the relationship you want to modify, and then click **Edit**.

    The Edit Relationship page displays. You can't change the relationship type; only the field values can be modified.

3. Make the necessary changes:

    * If the relationship type is Bi-directional, edit the Label field.
    * If the relationship type is Parent/Child, edit the Source and Target fields.

4. Click **Save**.

## User Rights Report

The User Rights Report gives you a summary of the Records Management site users, groups, and roles.

The report is divided into three sections:

* *Users* - All users of the Records Management site, and the roles and groups they are a member of
* *Roles* - All roles in the Records Management site, and the users in those roles
* *Groups* - All groups that are members of the Records Management site, and the users in those groups

You can access the report by clicking **User Rights Report** in the RM Admin Tools.

## Users and groups

Alfresco users and groups are created by the Alfresco administrator using the Alfresco Share Admin Tools. 
You can then assign these users and groups to Records Management roles using the Users and Groups tool in the RM Admin Tools.

Once you've [assigned them to a role](#define-roles) they'll be able to use the level of Records Management 
functionality that role has been given.

> **Note:** There are some system groups that are generated by default, such as `site_swsdp_SiteManager`. These can't be assigned to a role.

### Adding users and groups to a role

Adding users and groups to a role gives them permission to use the level of Records Management functionality 
that role has been given.

1. Click **Users and Groups** in the RM Admin Tools.

    All existing roles are displayed. When you click on a role the groups and users assigned to that role are displayed.

2. Locate the role you want to add groups or users to and click on it.

    Existing groups and users assigned to the role are displayed.

3. Click **Add** next to Groups or Users, depending on which you want to add.

    The Add User or Add Group page displays.

4. Enter a search term and click **Search**.

    All users or groups matching your search are displayed.

5. Click **Add** next to the user or group that you want to add to the role.

    The new group users is added to the role.

    > **Note:** You can remove a group or user from a role at any time by selecting them and clicking **Remove** then **Yes** to confirm.
---
title: Configure Governance Services
---

Use the information on this page to configure Governance Services.

## Alfresco global properties settings

Use this information to understand the `alfresco-global.properties` properties related to the Governance Services.

Properties for the Governance Services are listed in the `<configRoot>/classes/alfresco/module/org_alfresco_module_rm/alfresco-global.properties` 
file. 

For example:

```text
rm.ghosting.enabled=true
rm.notification.role=RecordsManager
imap.server.attachments.extraction.enabled=false
audit.enabled=true
audit.rm.enabled=true
audit.rm.runas=admin
cache.writersSharedCache.maxItems=10000
cache.writersSharedCache.cluster.type=fully-distributed
rm.rule.runasadmin=true
rm.autocompletesuggestion.minfragmentsize=2
rm.autocompletesuggestion.maxsuggestions.path=5
rm.autocompletesuggestion.maxsuggestions.node=5
rm.autocompletesuggestion.maxsuggestions.date=5
rm.autocompletesuggestion.nodeParameterSuggester.aspectsAndTypes=rma:record,cm:content
rm.dispositionlifecycletrigger.cronexpression=0 0/5 * * * ?
rm.dispositionlifecycletrigger.batchsize=500
```

> **Note:** These settings supplement any settings in the `<classpathRoot>/alfresco-global.properties` file. If a property appears in both files, the Governance Services property overrides the `<classpathRoot>/alfresco-global.properties` value.

Any property that is `false` by default, is not shown in the `alfresco-global.properties` file.

A full listing of the properties and their values is shown in this table:

|Setting|Meaning|
|-------|-------|
|audit.enabled|Enable/disable auditing. Default is `true`.|
|audit.rm.enabled|Enable/disable Governance Services auditing. Default is `true`.|
|audit.rm.runas|Set the user that the audit log runs under. Default is `system`. Alfresco doesn't audit events triggered by the system; for example, cron jobs. Set this value to `admin` for these jobs if you want them to be captured in the audit log.<br><br>Alternatively, create a user, provide the correct permissions and configure the jobs to run as that user.|
|audit.rm.viewLog.maxSize=100|The log can be viewed from Share or directly via the Audit log web script. By default the log does not exceed 100 entries. If the maximum size of the log is not configured in the alfresco-global-properties file then it will default to 100. If you include the size parameter in the request it will only be applied if it is less than or equal to the maximum size allowed, or it will be ignored.|
|cache.writersSharedCache.cluster.type|Extended permission service cache: type of cluster used. Default is `fully-distributed`.|
|cache.writersSharedCache.maxItems|Extended permission service cache: maximum number of items (node references) that are stored in the writer caches. Default is `10000`.|
|dm.classified.content.cleansing.trashcan.enabled|Use this setting to override the trashcan functionality of Content Services. The default value is `false`.|
|imap.server.attachments.extraction.enabled|Enable/disable IMAP server attachments. Default is `false`.|
|rm.autocompletesuggestion.maxsuggestions.date|Auto-complete suggestions: maximum number of date suggestions to provide. Default is `5`.|
|rm.autocompletesuggestion.maxsuggestions.node|Auto-complete suggestions: maximum number of node suggestions to provide. Default is `5`.|
|rm.autocompletesuggestion.maxsuggestions.path|Auto-complete suggestions: maximum number of path suggestions to provide. Default is `5`.|
|rm.autocompletesuggestion.minfragmentsize|Auto-complete suggestions: Minimum size of fragment to trigger a search. Default is `2`.|
|rm.autocompletesuggestion.nodeParameterSuggester.aspectsAndTypes|Auto-complete suggestions: Comma-separated list of types and aspects used by the node parameter autocomplete suggester. Default is `rma:record,cm:content`.|
|rm.completerecord.mandatorypropertiescheck.enabled|This setting is used to ensure completion of records. When it is set to true, Governance Services will only complete a record if all the mandatory properties have a value. When it is set to false you can complete a record with mandatory properties missing. <br><br> **Note:** This setting should be set to false when using Governance Services with Outlook Integration.|
|rm.content.cleaner|This setting is used in conjunction with `rm.content.cleansing.enabled=true`. Default is `contentCleanser.522022M`.<br><br>When content is sent for deletion, it is cleansed using the default 5220.22-M algorithm. The content is then destroyed, and the node is deleted (if ghosting is not enabled).<br><br>If you add a custom content cleaner bean, this can be specified using this property.|
|rm.content.cleansing.enabled|Set whether content can be deleted immediately (data cleansing). This applies to deleted (destroyed) classified records and classified documents.<br><br>The default setting of `false` allows deleted (destroyed) files to be restored (from the Trashcan if they are documents, or by using a recovery tool, if they are records).<br><br>This approach is only effective for installations with a single magnetic disk. In other situations, such as RAID or SSD, hardware techniques or process ensure that the content is non-recoverable.|
|rm.dispositionlifecycletrigger.cronexpression|Disposition lifecycle trigger cron job expression. Default is `0 0/5 * * * ?`.|
|rm.dispositionlifecycletrigger.batchsize|Disposition lifecycle batch size to process records. Default is `500` and value must be greater than `0`.|
|rm.ghosting.enabled|Enable/disable ghosting of records, when a record is deleted. Default is `true`.|
|rm.notification.role|Specify which role receives notifications; for example, when notifications when vital records are due for review. Default is `RecordsManager`.<br><br>A background job executes by default every 15 minutes to search for vital records that are due for review, and sends a notification. The template for the email notification is editable, and is stored in the Governance Services section of the Data Dictionary.|
|rm.record.contributors.group.enabled|Set which groups can perform Governance Services actions; for example, File as Record. Default is `false`. <br><br>If this is set to `true`, only members of the RECORD_CONTRIBUTORS group can perform these actions.|
|rm.rule.runasadmin|Require admin rights/ normal rights to run rules. Default is `true`.|
|version.store.enableAutoVersionOnTypeChange|Set whether a version is automatically created when the type of a document is changed. Default is `false`.|

## Customizing the end of the financial year {#customize-end-of-year}

You can set the end date of the financial year and the end of the financial quarter.

> **Important:** If you make adjustments to your financial year as per the instructions below, it is important you carry out the same procedure on your new installation every time you upgrade to a new version of Governance Services.

1. Navigate to the `<TOMCAT_HOME>/webapps/alfresco/WEB-INF/lib/alfresco-repository-xxx.jar` file in your installation.

2. Copy the `alfresco-repository-xxx.jar` to `<temp-dir>/alfresco-repository-xxx.zip` and extract the contents

2. From the extracted ZIP file copy `alfresco/period-type-context.xml` to `<TOMCAT_HOME>/shared/classes/alfresco/extension`.

3. Rename the file to `custom-period-type-context.xml`.

4. Change all the `value` properties to suit the dates of your financial year.

    For example, the following would customize your system to start the financial year in October.

    ```xml
    <bean id="period.end.of.financial.month" class="org.alfresco.repo.dictionary.types.period.EndOfFinancialMonth" >
       <property name="startDayOfMonth">
           <value>1</value>
       </property>
       <property name="startMonth">
           <value>10</value>
       </property>
    </bean>
    <bean id="period.end.of.financial.quarter" class="org.alfresco.repo.dictionary.types.period.EndOfFinancialQuarter" >
       <property name="startDayOfMonth">
           <value>1</value>
       </property>
       <property name="startMonth">
           <value>12</value>
       </property>
    </bean>
    <bean id="period.end.of.financial.year" class="org.alfresco.repo.dictionary.types.period.EndOfFinancialYear" >
       <property name="startDayOfMonth">
           <value>1</value>
       </property>
       <property name="startMonth">
           <value>9</value>
       </property>
    </bean>
    ```

5. Restart the server.

6. (Optional) If you change your financial periods this does not update any previously set calculated schedules and you will need to edit all {% include tooltip.html word="retentionschedule" text="retention schedule" %}s to ensure the new period start date is used. See [Editing a retention schedule]({% link governance-services/latest/using/retention-schedules.md %}#editing-a-retention-schedule).  
---
title: Governance Services APIs
---

Governance Services provides two APIs, the GS Core API and the GS Security Marks API.

> **Note:** The GS Security Marks API isn't available in Governance Services Community Edition.

The APIs are designed for you to create remote clients to manage the {% include tooltip.html word="fileplan" text="File Plan" %}. You can easily explore and test the endpoints using the Governance Services API Explorer. 

You can download the API Explorer from:

* [Alfresco Nexus repository](https://nexus.alfresco.com/nexus/#welcome){:target="_blank"}

The Governance Services distribution zip contains the `alfresco-governance-services-enterprise-rest-api-explorer-23.x.x.xxx.war` file.

> **Note:** Contact [Alfresco Support](https://support.alfresco.com/){:target="_blank"} for log in credentials.

Deploy it on the same port as Governance Services and test the APIs with your server directly from the API Explorer.

The following table provides a brief overview of each API.

|API|Description|
|---|-----------|
|GS Core API|This is the main public API for interfacing your client application with Governance Services. The REST API gives you access to core functionality. You can use it to manage the Governance Services site, record categories, record folders, unfiled containers and unfiled record folders, upload new records or declare an existing file as record, file records in the file plan and get information about transfers.|
|GS Security Marks API|The Security Marks API gives you access to the classification and security controls features of Governance Services. You can use it to manage classification guides, reasons, values, and declassification exemptions, as well as security control settings.|
---
title: Creating the Records Management site
---

After you've installed the Records Management AMP files, you're ready to go ahead and create a Records Management site.

1. Start Alfresco, and then log in using your administrator credentials.

2. Open the **Sites** menu and click **Create Site**.

    > **Tip:** You can also click **Create Site** on the My Sites dashlet.

3. Select **Records Management Site** as the Type.

    The Name, URL Name and Description will be completed for you automatically. You can edit the Description if needed. The URL name is used as part of the site URL.

    > **Note:** The site visibility can't be changed as only public sites are available for Records Management. You can only create one records management site.

4. Select a Compliance option to define which compliance model to use for your {% include tooltip.html word="fileplan" text="File Plan" %}. This selection defines the metadata available for records in the file plan.

    * **Standard** - The standard set of record metadata is available.
    * **DoD 5015.2-STD** - Record metadata required for {% include tooltip.html word="dod50152std" text="DoD 5015.2-STD" %} is available. Mandatory metadata includes the originator, the originating organization, the File Plan, the destroy action.
    
    > **Note:** If you select **Standard** then users can still customize the metadata available on individual records.

5. Click **Save**.

You'll see the dashboard for the new Records Management site which you can now customize. Sites that you create are automatically added to your **Favorites** list. Now you can:

* [Load Test Data]({% link governance-services/latest/using/the-fileplan.md %}#loading-test-data) by adding the Import Data Set dashlet for an example of how to structure a File Plan
* Use the **RM Admin Tools** on the Records Management dashboard **More** menu to access the administration features

> **Note:** The user who created the Records Management site is automatically made a member of the Records Management Administrator role. Other users can access different areas of the **RM Admin Tools** depending on the capabilities given to the role that they're in.
---
title: Install using Docker Compose
---

Use this information to quickly deploy Governance Services using Docker Compose. 
Due to the limited capabilities of Docker Compose, this deployment method is 
recommended for development and test environments only.

## Prerequisites and supported platforms

* [Docker](https://docs.docker.com/install/){:target="_blank"}
    * This allows you to run Docker images and Docker Compose on a single computer.
* [Docker Compose](https://docs.docker.com/compose/install/){:target="_blank"}
    * Docker Compose is included as part of some Docker installers. If it's not part of your installation, then install it separately after you've installed Docker.
* Access to [Quay](http://www.quay.io){:target="_blank"}
    * Alfresco customers can request Quay.io credentials by logging a ticket at [Alfresco Support](https://support.alfresco.com/). These credentials are required to pull private (Enterprise-only) Docker images from Quay.io.

> **Note:** Make sure that the following ports are free on your computer: 5432, 8080. These ports are set in the `docker-compose.yml` file.

## Deployment steps

1. Download the `docker-compose.yml` file by accessing the Content Services [Download Trial](https://www.hyland.com/en/resources/alfresco-ecm-download) page, which will give you a 30-day license.

2. Save the file in a local folder.

3. Edit the file and change the following two services:

    Add a `#` prefix to the Alfresco Content Repository and Alfresco Share Docker image locations so they are commented out, 
    and add the Alfresco Governance image locations:

    ```text
    services:
        alfresco:
            #image: alfresco/alfresco-content-repository:23.x.x
            image: quay.io/alfresco/alfresco-governance-repository-enterprise:23.x.x
            mem_limit: 1700m
    ```

    ```text
        share:
            #image: alfresco/alfresco-share:23.x.x
            image: quay.io/alfresco/alfresco-governance-share-enterprise:23.x.x
            mem_limit: 1g
    ```

    Replace the ACS versions (for example, ACS 23.1.1) with the compatible AGS versions (for example, AGS 23.1.1).

4. In a command prompt login to Quay using the following command (to open up access to Enterprise Docker images):

    ```bash
    $ docker login quay.io
        login against server at https://quay.io/v1/
        Username: <Quay.io Credential Username>
        Password: <Quay.io Credential Password>
    ```

5. In the command prompt change directory to the location of the `docker-compose.yml` file and deploy Governance Services using the following command:

   ```bash
    $ docker-compose up
   ```

   This downloads the images, fetches all the dependencies, creates each container, and then starts the system. If you downloaded the project and changes were made to the project settings, any new images will be pulled from Quay before the system starts.

   As an alternative, you can also start the containers in the background by running:

   ```bash
    $ docker-compose up -d
   ```

6. Wait for the logs to complete.

    ```text
    ...
    alfresco_1            | ... INFO ... [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
    alfresco_1            | ... INFO ... [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["ajp-nio-8009"]
    alfresco_1            | ... INFO ... [main] org.apache.catalina.startup.Catalina.start Server startup in 226026 ms
    ```

    If you encounter errors whilst the system is starting up:

    * Stop the session (by using `CONTROL+C`).
    * Remove the container (using the `--rmi all` option). For example:

       ```bash
       $ docker-compose down --rmi all
       ```

    * Try allocating more memory resources, as advised in `docker-compose.yml`. For example, in Docker, change the memory setting in **Preferences** (or **Settings**) > **Advanced** > **Memory**, to at least 6 GB. Make sure you restart Docker and wait for the process to finish before continuing.
    * Go back and retry the deployment.

    > **Note:** Although 16 GB is the required minimum memory setting, keep in mind that 6 GB is much lower than the required minimum, and may need to be adapted for your environment.

7. Open your browser and check everything starts up correctly:

    * Share: `http://localhost:8080/share`

Final step before you can start with Records Management is to [create the Records Management site]({% link governance-services/latest/install/create-rm-site.md %}).
---
title: Governance Services Installation Options
---

This information guides you through installing Governance Services. You can use the containerized deployment 
method using Docker Compose, as there is no GUI installer, or you can install using the standard AMP files contained 
in the distribution zip.

There are two options for installing the Governance Service:

* [Install using Docker Compose]({% link governance-services/latest/install/docker.md %}) Due to the limited capabilities of Docker Compose, this deployment method is recommended for development and test environments only.
* [Install using the distribution ZIP]({% link governance-services/latest/install/zip.md %})

> **Note:** For more information about what containerized deployment and Docker Compose means, see the Alfresco Content Services deployment documentation - [Understanding containerized deployment]({% link content-services/latest/install/containers/index.md %}).

Instructions are also provided for [upgrading the Governance Service]({% link governance-services/latest/upgrade/index.md %}).
---
title: Uninstalling the Governance Services AMP files
---

The Governance Services AMP files can be uninstalled using the Module Management Tool (MMT).

Governance Services consists of two AMP files, which are applied during installation. One of the AMP files, 
representing the core Governance Services functionality, is applied to the Alfresco Repository WAR file, and the other, 
representing the Governance Services UI component is applied to the Alfresco Share WAR file. 

Both of the AMP files need to be removed in order to uninstall Governance Services. 
Use the Module Management Tool (MMT) to do this. For more information on the tool, 
see [Module Management Tool (MMT)]({% link content-services/latest/develop/extension-packaging.md %}#using-the-module-management-tool-mmt)

The MMT is a command line tool. The syntax for uninstalling an AMP file using MMT is:

```bash
$ java -jar bin\alfresco-mmt.jar uninstall <ModuleId> <WARFileLocation>
```

> **Note:** The `apply_amps` command does not uninstall AMP files (even if you remove the AMP files manually from the `amps` and `amps_share` directories). Use `apply_amps` to install AMP files only.

1. Change into the root of the Alfresco installation directory.

2. Find the core Governance Services AMP file using the following command:

    ```bash
    $ java -jar bin\alfresco-mmt.jar list tomcat\webapps\alfresco.war                                  
    ```

    This shows the core RM components:

    ```bash
    Module 'org_alfresco_module_rm' installed in 'webapps/alfresco'
       -    Title:        AGS Repo
       -    Version:      23.1
       -    Install Date: null
       -    Description:   Alfresco Governance Services Repository Extension
    Module 'alfresco-rm-enterprise-repo' installed in 'webapps/alfresco'
       -    Title:        AGS Enterprise Repo
       -    Version:      23.1
       -    Install Date: Thurs Nov 02 08:50:15 UTC 2023
       -    Description:   Alfresco Governance Services Enterprise Repository Extension    
   ```

    To uninstall the AMP file, you'll need the Enterprise Module ID `alfresco-rm-enterprise-repo`.

3. Find the Share RM AMP file using the following command:

    ```bash
    $ java -jar bin\alfresco-mmt.jar list tomcat\webapps\share.war                        
    ```

    This shows the Share RM component:

    ```bash
    Module 'alfresco-rm-enterprise-share' installed in 'tomcat\webapps\share.war'
    -    Title:        Alfresco Record Management Share Extension
    -    Version:      23.1
    -    Install Date: Thurs Nov 02 08:50:15 UTC 2023
    -    Description:   Alfresco Record Management Share Extension              
    ```

    To uninstall the AMP file, you'll need the Enterprise Module ID `alfresco-rm-enterprise-share`.

4. Use these commands to uninstall the AMP files:

    ```bash
    $ java -jar bin\alfresco-mmt.jar uninstall alfresco-rm-enterprise-repo tomcat\webapps\alfresco.war            
    ```

    ```bash
    $ java -jar bin\alfresco-mmt.jar uninstall alfresco-rm-enterprise-share tomcat\webapps\share.war            
    ```

5. You can check that the AMP files have been removed by rerunning the commands:

    ```bash
    $ java -jar bin\alfresco-mmt.jar list tomcat\webapps\alfresco.war                        
    ```

    and

    ```bash
    $ java -jar bin\alfresco-mmt.jar list tomcat\webapps\share.war                                      
    ```

6. Delete the `tomcat\webapps\alfresco` and `tomcat\webapps\share` folders in the Alfresco installation directory.

    Deleting these directories forces Tomcat to read the edited WAR files when Alfresco is restarted.

7. Restart Alfresco to see your changes.
---
title: Install using the distribution ZIP
---

Governance Services is installed by applying two AMP files to an existing Alfresco Content Services installation.

The Governance Services distribution zip file contains the following files:

|alfresco-governance-services-enterprise-repo-23.x.x.xxx.amp|Contains Governance Services functionality that's applied to an existing Alfresco Content Services installation.|
|alfresco-governance-services-enterprise-share-23.x.x.xxx.amp|Contains Governance Services functionality that's applied to an existing Alfresco Share installation.|

> **Note:** Install the AMPs manually using the Module Management Tool (MMT), rather than using the `apply_amps` tool.

1. Browse to [Hyland Community](https://community.hyland.com/){:target="_blank"} and download `alfresco-governance-services-enterprise-distribution-23.x.0.zip`.

2. Stop the Alfresco Content Services server.

3. Delete the `tomcat\webapps\alfresco` and `tomcat\webapps\share` folders in the Alfresco Content Services installation directory.

    Deleting these directories forces Tomcat to read the edited WAR files when Alfresco Content Services is restarted.

    > **Note:** If you are using non-Windows systems, such as Mac OS X and Linux, you'll need to replace the backslashes by forward slashes in directory paths.

4. Copy the AMP files to the Alfresco `amps` and `amps_share` directories.

    * Copy the `alfresco-governance-services-enterprise-repo-23.x.x.xxx.amp` file to the Alfresco `amps` directory.
    * Copy the `alfresco-governance-services-enterprise-share-23.x.x.xxx.amp` file to the Alfresco `amps_share` directory.

5. Change into the root of the Alfresco Content Services installation directory. Directories specified in the following procedures are relative to this directory.

6. Run the following commands to install the AMP files:

    ```bash
    java -jar bin\alfresco-mmt.jar install amps\alfresco-governance-services-enterprise-repo-23.x.x.xxx.amp tomcat\webapps\alfresco.war
    ```

    ```bash
    java -jar bin\alfresco-mmt.jar install amps_share\alfresco-governance-services-enterprise-share-23.x.x.xxx.amp tomcat\webapps\share.war
    ```

7. Start the Alfresco Content Services server.

8. Check the AMP files have been installed successfully, using these commands:

    ```bash
    java -jar bin\alfresco-mmt.jar list tomcat\webapps\alfresco.war
    ```

    and

    ```bash
    java -jar bin\alfresco-mmt.jar list tomcat\webapps\share.war
    ```

9. Start Share by browsing to:

    `http://<your-server-name>:<port number>/share`

    > **Note:** When you install Governance Services the Security Controls features are installed at the same time.

Final step before you can start with Records Management is to [create the Records Management site]({% link governance-services/latest/install/create-rm-site.md %}).
---
title: Supported platforms
---

The following are the supported platforms for the Alfresco Governance Services version 23.x:

{% capture twenty-three-two %}

| Version | Notes |
| ------- | ----- |
| Alfresco Content Services 23.2 | |

{% endcapture %}

{% capture twenty-three-one %}

| Version | Notes |
| ------- | ----- |
| Alfresco Content Services 23.1 | |

{% endcapture %}

{% include tabs.html tableid="supported-platforms" opt1="23.2" content1=twenty-three-two opt2="23.1" content2=twenty-three-one %}
---
title: Tutorials
---

This section contains different types of tutorials, such as video tutorials.---
title: Governance services video tutorials
---

Watch these videos for tips on using Governance Services.

## Create a Records Management site

This video shows how to create a Records Management Share site, which is required before you can start doing any Records Management.

{% include media.html id="CB3QIwIkpLQ" %}

## Import Records Management test data

In this video you will see how data can be loaded into a Records Management Share site.  

{% include media.html id="PkG_aYiI-IQ" %}

## Create a Record Category  

Here we will learn how to create a {% include tooltip.html word="category" text="Record Category" %}.

{% include media.html id="Q_Ypor_k1oQ" %}

## Create a Retention Schedule  

Here we will learn how to create a {% include tooltip.html word="retentionschedule" text="Retention Schedule" %}.

{% include media.html id="ZG5b4kdizSA" %}

## Create Retention Schedule Steps  

Here we will learn how to create the {% include tooltip.html word="retentionschedule" text="Retention Schedule" %} steps.

{% include media.html id="PhFefFDrvFk" %}

## Create a Record Folder  

Here we will learn how to create a Record Folder, which is used to store records.

{% include media.html id="7-DIuHbUQ6g" %}

## Set User Permissions  

Learn how to set up permissions for users in this video.

{% include media.html id="jjn1FSqdtl4" %}

## File a Record  

See how you can file a record.

{% include media.html id="YfJBxc2lF5o" %}

## File an Unfiled Record  

Learn how to file a record that is {% include tooltip.html word="unfiledrecords" text="unfiled" %}.

{% include media.html id="LXexwAlyXjI" %}

## Add a Record Type  

See how to add metadata for records by applying a record type.

{% include media.html id="vJR078QVINM" %}

## Edit Record Metadata  

In this video we learn how to update the record metadata.

{% include media.html id="9fCoNMeLXCg" %}

## Complete a Record  

Learn how to {% include tooltip.html word="recordcompleted" text="complete" %} a record.

{% include media.html id="B6MVNxOSllE" %}

## Process Records  

In this video you learn how to process individual records or records in a folder.

{% include media.html id="UWE8Qmgo8Bo" %}

## Automate the File Plan  

In the {% include tooltip.html word="fileplan" text="File Plan" %} you can define {% include tooltip.html word="category" text="category" %} and folder rules to manage your content automatically.

{% include media.html id="T7SRZGi2e8A" %}---
title: Security controls and classification video tutorials 
---

Watch these videos for tips on using security controls and classification.

## Create Security Controls

Learn how to create {% include tooltip.html word="securitycontrol" text="security controls" %}.  

{% include media.html id="ZvktCkmgPGU" %}

## Set Security Clearance

Learn how to set {% include tooltip.html word="securityclearance" text="security clearance" %}.  

{% include media.html id="AgEtLz6c4i0" %}

## Create Classification Guide

Learn how to create a {% include tooltip.html word="securityclassification" text="classification" %} guide.  

{% include media.html id="5s_PC5pGJg8" %}

## Classify Items

In this video you will learn how to {% include tooltip.html word="securityclassification" text="classify" %} items.

{% include media.html id="DEZT8jBG-fE" %}

## Classification Reasons

Learn how to add information to an item about why it has been classified in a specific way.

{% include media.html id="iAWD_LRbOBQ" %}

## Declassification Time Frame

Learn how to configure the amount of time the system will use to declassify items.

{% include media.html id="7JDVenHTbro" %}

## Declassification Exemptions

Learn how to indicate why an item has been declassified.

{% include media.html id="-WVc2EjGr1I" %}

---
title: Upgrade Governance Services
---

To upgrade Governance Services you need to make sure you're running the correct version of Alfresco Content Services.

Check the [Supported Platforms]({% link content-services/latest/support/index.md %}) and 
the [Alfresco Content Services upgrade paths]({% link content-services/latest/upgrade/index.md %}).

When your Alfresco Content Services installation is upgraded, you can apply the new AMP files for Governance Services.

1. Ensure your current production environment is running a version that is supported for upgrading.

2. Download Alfresco Content Services 23.x and the compatible Governance Services Distribution ZIP from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

3. Upgrade to Alfresco Content Services.

    For more information about upgrading Alfresco Content Services, see [Upgrading Alfresco]({% link content-services/latest/upgrade/index.md %}).

    You can start the server at this point to verify that the upgrade was successful.

4. Apply the Governance Services to the upgraded Alfresco Content Services installation.

    Follow the instructions in [Install using the distribution ZIP]({% link governance-services/latest/install/zip.md %}).

    > **Note:** If you have {% include tooltip.html word="easyaccessrecords" text="easy access records" %} (previously know as in-place records) that are pre-2.3.0.8 versions of Records Management, then you also need to [run a webscript](#easy_access_upgrade) so that easy access records created in pre-2.3.0.8 sites are shown in the search results of users without Records Management permissions.

5. Restart the Alfresco Content Services server, if it is already running.

6. Login to Alfresco Share to view the Records Management data.

Your existing Records Management data is migrated to Alfresco Content Services.

Any existing Records Management data is preserved when you upgrade from a previous version of Records Management  
(it is 'patched' in the same way as updated data in the server). The {% include tooltip.html word="fileplan" text="File Plan" %} structures will appear as they did 
in 1.0 and the previous Records Management site is migrated. Therefore, you do not need to create the Records Management site again.

From Records Management 2.0 onwards you cannot create a record series; instead you create a record category with 
no {% include tooltip.html word="retentionschedule" text="retention schedule" %}. The record series is retained as a deprecated model construct to be used when migrating 
existing record series from a 1.0 installation. This means that any previously created record series will appear and 
behave as record categories in 2.2, but will be of the deprecated type record series (directly extended from record category). 
If any custom data was defined for record series in 1.0, this will still appear in the Records Management site, 
but only for the migrated record series.

Note also that any pre-configured saved searches from your previous version are not available after an upgrade.

## Upgrading easy access records from pre-2.3.0.8 versions {#easy_access_upgrade}

If you upgrade from a pre-2.3.0.8 version of Records Management, then an additional web script needs to be run so that 
easy access records (previously known as in-place records) created in pre-2.3.0.8 sites are shown in the search results 
of users without Records Management permissions.

It can be run as a one-off operation to convert all existing records or, for better performance on larger repositories, 
it can also be run on a user-defined number of records.

> **Note:** Easy access records created on Records Management 2.3.0.8 and later are shown without running the web script.

There are four parameters available for the web script.

* `batchsize` (mandatory) - the batch size to process records in. So, for example, if you enter `batchsize=100`, then records will be processed in consecutive batches of 100.
* `maxProcessedRecords` (optional) - the maximum number of records to be processed. If unspecified, this value defaults to that of the `batchsize`. If set to 0, all records are processed.
* `export` (optional) - true or false (the default is false). If true is selected then a list of processed records is exported in csv format. The list shows the file name and file node reference.
* `parentNodeRef` (optional) - process records in a specified folder and its sub-folders. See step 3 for how to get the `parentNodeRef` node reference.

You need Alfresco Administrator permissions to run the web script.

1. Paste or type `http://<server name>:<server port>/alfresco/s/api/rm/rm-dynamicauthorities` into your browser.

2. Append your required parameters, for example:

    * To process 50 records in one batch of 50 type `http://<server name>:<server port>/alfresco/s/api/rm/rm-dynamicauthorities?batchsize=50`
    * To process 100 records in two batches of 50 type `http://<server name>:<server port>/alfresco/s/api/rm/rm-dynamicauthorities?batchsize=50&maxProcessedRecords=100`
    * To process all pre-2.3.0.8 records in batches of 100 type `http://<server name>:<server port>/alfresco/s/api/rm/rm-dynamicauthorities?batchsize=100&maxProcessedRecords=0`
    * To process 10 records in one batch of 10 with csv output type `http://<server name>:<server port>/alfresco/s/api/rm/rm-dynamicauthorities?batchsize=10&maxProcessedRecords=10&export=true`

3. Press Enter to run the web script. You may be prompted for your system username and password.

    > **Note:** If you enter a large batch number then your browser may time out. The process will continue running in the background and details will be recorded in the server logs. As such, it's recommended that you set a `maxProcessedRecords` or use `parentNodeRef` to process a folder at a time.

    > **Tip:** To get the `parentNodeRef` for a folder go to its parent folder, then hover over the folder and select **View Details**. The node ref will be shown in the browser address.

    ![Finding a node ref]({% link governance-services/images/finding-node-ref.png %})

4. Results and/or errors are reported as a JSON-formatted string, or a CSV file if you use the `export` parameter. Processed records are shown in the `alfresco.log` as below:

    ```text
    2016-09-16 13:46:44,409 INFO  [org.alfresco.repo.web.scripts.roles.DynamicAuthoritiesGet] [http-apr-8080-exec-6] Processing – BEGIN
    [ output cut ]
    2016-09-16 13:46:47,131 INFO  [org.alfresco.repo.web.scripts.roles.DynamicAuthoritiesGet] [http-apr-8080-exec-6] Processing record file149 (2016-1474021730514).txt - BEGIN
    2016-09-16 13:46:47,150 INFO  [org.alfresco.repo.web.scripts.roles.DynamicAuthoritiesGet] [http-apr-8080-exec-6] Processing record file149 (2016-1474021730514).txt - END
    2016-09-16 13:46:47,152 INFO  [org.alfresco.repo.web.scripts.roles.DynamicAuthoritiesGet] [http-apr-8080-exec-6] Processing record file150 (2016-1474021731516).txt - BEGIN
    2016-09-16 13:46:47,174 INFO  [org.alfresco.repo.web.scripts.roles.DynamicAuthoritiesGet] [http-apr-8080-exec-6] Processing record file150 (2016-1474021731516).txt - END
    2016-09-16 13:46:47,238 INFO  [org.alfresco.repo.web.scripts.roles.DynamicAuthoritiesGet] [http-apr-8080-exec-6] Processing - END
    2016-09-16 13:46:47,238 INFO  [org.alfresco.repo.web.scripts.roles.DynamicAuthoritiesGet] [http-apr-8080-exec-6] Processed first 100 records.
    ```

---
title: Auditing and reporting
---

You can view audit logs for record {% include tooltip.html word="category" text="categories" %}, record folders, active content, and records, and whenever a record or 
folder is transferred, added to a {% include tooltip.html word="fileplan" text="File Plan" %}, {% include tooltip.html word="accession" text="accessioned" %}, or destroyed, you can file a report to keep a record of the process.

> **Note:** You can only view audit logs if your Alfresco administrator has given you the Access Audit permission.

Whenever a record is transferred, added to a hold, accessioned or destroyed, you have the option to file a report. 
The report contains details of the item, the retention authority, what the retention step was, when it was performed, 
who by, and any location changes. The report is filed as a record.

The audit log contains the entire history of an object since the point it was added to the File Plan, and can be useful 
for finding out about specific events that have occurred during an objects life cycle, and any users that have been involved.

Every entry in the audit log is timestamped and where metadata has been changed, the original values and changed values are recorded.

When viewing an audit log you can also select to export it or to file it as a record.

> **Note:** Users with access to the RM Admin Tools can run an audit of the entire Records Management system.

## Filing a report

Whenever a record or folder is transferred, added to a hold, accessioned, or destroyed, you can file a report to 
keep a record of the process.

When you file a report it's filed as a record which you can then complete and process as with any other record.

1. In the File Plan hover over a destroyed folder or record, or a folder or record awaiting transfer or accession completion, and click **File Report**.

    > **Note:** Records and folders waiting for transfer and accession completion are stored by default in the **Transfers** area in the explorer panel. Records on a hold are stored by default in the **Holds** area in the explorer panel.

2. Reports are filed by default to the **Unfiled Records** area of the File Plan. To select an alternate location deselect the **File report to 'Unfiled Records'** option and choose a different destination folder.

    > **Note:** As with all records you must select a folder, not a category, to file the report to.

3. Click **File Report**.

The report is filed as an incomplete record in your selected destination.

## Viewing an audit log

You can view audit logs for record categories, record folders, and records.

1. Hover over a record category, folder, or record in the File Plan and click **More** then **View Audit Log**.

    > **Note:** You can only view audit logs if your Alfresco administrator has given you the Access Audit permission.

    The audit log displays.

You can click **Export** to export the audit log, or **File as Record** to select a location in the File Plan and file the audit log as a record.
---
title: Automating the File Plan
---

In the {% include tooltip.html word="fileplan" text="File Plan" %} you can define {% include tooltip.html word="category" text="category" %} and folder rules to manage your content automatically. You can come up with many creative solutions to make sure specific content processes are automated so you don't have to do the work yourself.

Rules dictate how content entering, leaving, or currently residing in a category or folder is managed.

There are three parts to a content rule:

* The event that triggers the rule
* The conditions the content has to meet
* The action performed on the content

The events that can trigger a rule are:

* A content item arrives in the folder
* A content item leaves the folder (it's moved or deleted)
* A content item in the folder is modified

Here are some examples of how you can use rules to automate repetitive tasks:

* All records without a record type placed in a category are associated with a specific record type
* All incomplete records placed in a folder are completed
* All records that are {% include tooltip.html word="cutoff" text="cut off" %} in a folder have the event Case Closed completed
* All folders created in a specific category are added to a File Plan

## Defining rules for a category or folder

Use rules to manage your File Plan content automatically. There are two ways to define rules: create your own rules or 
link to rules already created for a different category or folder.

When you define a rule, it only applies to new content added to the category/folder. Items that were in the 
category/folder before the rule was defined aren't affected by it. You can manually apply the category/folder 
rules with the **Run Rules** action.

If you create rules for a category, depending on the rule settings, they can apply to folders and categories created in 
the category, records placed in folders in the category, or both.

> **Note:** Even if a category/folder doesn't have its own rules, it could have inherited category/folder from a parent folder. A message on the Rules page lets you know if this is the case.

### Creating a rule

You can create rules for a category or folder, in much the same way that you might apply rules to your emails.

> **Note:** If a category/folder already has rules applied to it (indicated by the ![]({% link governance-services/images/rules-icon.png %}){:height="18px" width="18px"} icon) you can add new rules to it by [adding to a set of rules]({% link content-services/latest/using/content/rules.md %}).

1. Click **Manage Rules** when you're in the folder or category you want to set rules for in the File Plan.

    > **Tip:** You can also hover over a folder or category in the File Plan and click **More** then **Manage Rules**.

2. Click **Create Rules**.

3. Enter a name and a description (optional) for the rule.

4. Select when the rule will be triggered:

    * **Items are created or enter this folder**: The rule will be applied to content that gets added to this category/folder. This includes any item that is copied to, created in, or uploaded to the folder.
    * **Items are updated**: When an item in this folder is modified, the rule will be applied to it.
    * **Items are deleted or leave this folder**: The rule will be applied to content that is moved out of the category/folder or deleted.

    > **Note:** A rule can have more than one event, condition, and action. Click the + or - icons to add or remove rows.

5. Select if the rule will be applied **If the following apply**, **If the following don't apply**, or both.

    Here are 3 examples of conditions that you could apply to trigger a rule:

    * The rule is applied if the record title contains the word 'urgent' (**If the following apply**)
    * The rule is applied if the record title does not contain the word 'urgent' (**If the following don't apply**)
    * The rule is applied if the record title contains the word 'urgent', unless the record was created before a specified date (**If the following apply** and **If the following don't apply**)

6. Select criteria for which content the rule will apply to, and remember that you can use the + and - icons to add and remove extra criteria.

    > **Note:** Selecting **Show more** on these menus displays the Select property screen where you can select additional properties. Click the folders on the left of the screen to show the properties they contain on the right of the screen. Selecting **Show in menu** selects that property and adds it to all criteria menus when setting up the current rule.

7. Select the action you want performed when the conditions are met.

    When you've selected an action you might need to select further options, for example if you select to reject items click **Reject** to specify a reason.

    If you select **File to**, **Copy to**, **Move to**, **File Version as Record** or **File as Record** you can specify the location of where to store the record by entering a location in **Record Folder Location**, for example `/category/subcategory/folder`. Click **Select** to choose an existing folder or a combination of the two. Select **Create Full Path to Folder** to ensure the specified path is created if it doesn't already exist. It won't be created if it doesn't fit the File Plan structure.

    > **Note:** For **File Version as Record** and **File as Record** you don't have to select a destination folder and if you don't the created record can be found in the unfiled records area.

    There are also extensive [autocomplete options](#rules-autocomplete-options).

    If you select **Execute script** then scripts are only available if they've been set up by your Alfresco administrator in **Repository > Data Dictionary > Records Management > Records Management Scripts**.

    If you select **Worm Lock** you must have configured Amazon S3. For more information on WORM Lock see [Working with Amazon S3 WORM]({% link governance-services/latest/using/worm.md %})

8. Select additional options:

    * **Turn off rule**: Switch off the rule.
    * **Rule applies to subfolders**: Apply the rule to this category and all its subcategories and subfolders.
    * **Run rule in background** Lets you continue working while the rule is running. You can also select an action to run if there's a problem with the rule with the rule. These actions are the same as the Execute script action, and are set up by your Alfresco administrator.

9. Click **Create**, or **Create and Create Another** to save this rule and start creating another.

#### Rules autocomplete options

If you type part of a record property at any place in the path then autocomplete options are displayed.

For example, if you type *rm* then you'll be offered options that include:

* Date filed `{node.rma:dateFiled}`
* Identifier `{node.rma:identifier}`
* Location `{node.rma:location}`

Records will be put into the File Plan based on each individual record property value.

So for example you could set a path of `/category/{node.rma:location}`. When the rule is run records with a Location property of `US` would be put in `/category/US`, and records with a Location property of `France` would be put in `/category/France`.

Date options set that part of the path to the date the rule is run. For example if it's run on `Monday` then:

* Short Day `{date.day.short} = Mon`
* Long Day `{date.day.long} = Monday`

By default  autocomplete options are based on the first two letters you type, and only five options for each type of suggestion are offered at a time. Type more letters to narrow down the displayed options.

> **Tip:** This can be configured in the properties file.

Available autocomplete options are:

* Last accessed = `node.cm:accessed`
* When created = `node.cm:created`
* Creator = `node.cm:creator`
* Description = `node.cm:description`
* Last modified = `node.cm:modified`
* Modifier = `node.cm:modifier`
* Name = `node.cm:name`
* Title = `node.cm:title`
* Date filed = `node.rma:dateFiled`
* Unique database ID = `node.rma:dbUniquenessId`
* Identifier = `node.rma:identifier`
* Location = `node.rma:location`
* Original = `node name node.rma:origionalName`
* Node ID = `node.sys:node-uuid`
* Store ID = `node.sys:store-identifier`
* Store protocol = `node.sys:store-protocol`
* Short Day (for example, Mon) = `date.day.short, date.day`
* Long Day (for example, Monday) = `date.day.long`
* Day Number (for example, 1) = `date.day.number`
* Day of Month (for example, 18) = `date.day.month`
* Day of Year (for example, 216) = `date.day.year`
* Short Month (for example, Jan) = `date.month.short`
* Month (for example, Jan) = `date.month`
* Long Month (for example, January) = `date.month.long`
* Month Number (for example, 01) = `date.month.number`
* Short Year (for example, 14) = `date.year.short`
* Year (for example, 14) = `date.year`
* Long Year (for example, 2014) = `date.year.long`
* Week of Year (for example, 31) = `date.year.week`

### Linking to an existing rule set

The **Link to Rule Set** option lets you reuse an existing rule set that's already defined for another category or folder.

> **Note:** If a category or folder already has linked rules applied (indicated by the ![]({% link governance-services/images/rules-icon.png %}){:height="18px" width="18px"} icon) you can link to new rules by [linking to a different rule set](#linking-to-a-different-rule-set).

1. Hover over a category/folder with no rules applied and click **More** then **Manage Rules**.

2. Click **Link to Rule Set**.

3. Find the category/folder you want to use.

    Select the site then select a folder. Check the rules listed to make sure you're linking to the correct folder.

    > **Note:** Locations that you don't have permission to access are disabled.

4. Click **Link**.

    > **Note:** You can click **View Rule Set** to view the rule details, or **Change** to select a different rule to link to.

5. Click **Done**.

## Working with a set of rules

You can easily view and maintain the individual rules that makes up the rule set. You can add, edit, and delete rules, make a rule inactive, and change the run order. You can also manually run rules.

You can create many rules to form a full set of rules, and then apply multiple rules to categories and folders.

When you select the **Manage Rules** action for a category/folder with defined rules, the Rules page is split into two.

The left side of the page lists the rules that make up the rule set. If the category/folder inherits rules from a parent category/folder, those rules appear here too. The rules run in the order they're listed. Inherited rules are always run first.

A check mark to the left of the rule means it's active.

Selecting an individual rule in this list displays its details on the right side of the page.

### Adding to a set of rules

A set of rules can include any number of individual rules, and you can add new rules to a category or folder as you need.

1. Click **Manage Rules** when you're in the folder or category in the File Plan you want to manage rules for.

    > **Tip:** You can also hover over a category/folder with rules applied (indicated by the ![]({% link governance-services/images/rules-icon.png %}){:height="18px" width="18px"} icon) and click **More** then **Manage Rules**.

2. Click **New Rule**.

    On the New Rule page you can add a new rule to a set of rules in exactly the same way as the first time you created a rule, see [creating a rule](#creating-a-rule).

After creating the last rule you return to the Rules page. Any new rules created are added at the end of the rule set.

### Editing a rule

You might need to revisit your rules from time to time and make some changes to keep them current. If you don’t want to use a specific rule anymore but think you might need it again in the future, you can just disable it.

1. Click **Manage Rules** when you're in the folder or category in the File Plan you want to edit rules for.

    > **Tip:** You can also hover over a category/folder with rules applied (indicated by the ![]({% link governance-services/images/rules-icon.png %}){:height="18px" width="18px"} icon) and click **More** then **Manage Rules**.

2. On the left side of the page, click the rule you want to edit.

    > **Note:** This will be shown in the rule summary on the right side of the page. You can't edit linked or inherited rules here; that has to be done in the category/folder where they were created.

3. Click **Edit**.

4. Make your changes. You can edit any of the rule details: name, description, rule definition, and options.

5. Click **Save**.

### Reordering the rules in the rule set

As part of managing your rule set you can pick the order in which the rules are run. If your category or folder has inherited rules, those are always run first in the order they're listed. Any rules marked as inactive are skipped.

1. Click **Manage Rules** when you're in the folder or category in the File Plan you want to reorder rules for.

    > **Tip:** You can also hover over a category/folder with rules applied (indicated by the ![]({% link governance-services/images/rules-icon.png %}){:height="18px" width="18px"} icon) and click **More** then **Manage Rules**.

2. On the left side of the page drag and drop rules to where you want them in the list.

    > **Note:** You can't reorder linked or inherited rules here; that has to be done in the folder where they were created. Click **Reset** to return the rule set to its last saved order.

3. Click **Save**.

### Turning off inherited rules

If a category or folder is inheriting rules from a parent category or folder, you can easily turn them on and off as needed.

Turning inherited rules on and off works at an individual category/folder level, and will not affect any other categories/folders.

1. Click **Manage Rules** when you're in the folder or category in the File Plan you want to switch off inherited rules for.

    > **Tip:** You can also hover over a category/folder with rules applied (indicated by the ![]({% link governance-services/images/rules-icon.png %}){:height="18px" width="18px"} icon) and click **More** then **Manage Rules**.

    If a category/folder has inherited rules these are displayed on the left side of the page.

2. Click **Inherit Rules**.

    Any inherited rules are turned off for the category/folder and **Don't Inherit Rules** is shown. You can click **Don't Inherit Rules** to turn inherited rules back on for the category/folder.

### Deleting a rule

When a category or folder has a rule applied that you don't need anymore, you can delete the individual rule.

1. Click **Manage Rules** when you're in the folder or category in the File Plan you want to delete rules for.

    > **Tip:** You can also hover over a category/folder with rules applied (indicated by the ![]({% link governance-services/images/rules-icon.png %}){:height="18px" width="18px"} icon) and click **More** then **Manage Rules**.

2. On the left side of the page, click the rule you want to delete.

    If you might want to use the rule again, consider disabling it instead. Edit the rule to do that.

    > **Note:** You can't delete linked or inherited rules here; that has to be done in the folder where they were created.

3. Click **Delete**.

4. When you're asked to confirm the deletion, click **Delete**.

## Working with linked rules

When a category or folder has linked rules there are less editing options than when it has its own set of rules. You can either link to a different rule set or you can break the link completely.

When you select the **Manage Rules** action for a category or folder with linked rules, the Rules page shows the name and path of the category/folder whose rule set is being referenced.

> **Note:** The category/folder might also inherit rules from a parent category/folder. A message lets you know if this is the case.

Changes to the rule set have to be done in the category/folder where the rules were originally defined. It's easy to get to the Rules page for the source category/folder: just click **View Rule Set**.

### Linking to a different rule set

If you want to change the rules you're linked to, you can easily link to a different rule set.

1. Click **Manage Rules** when you're in the folder or category in the File Plan you want to change linked rules for.

    > **Tip:** You can also hover over a category/folder with rules applied (indicated by the ![]({% link governance-services/images/rules-icon.png %}){:height="18px" width="18px"} icon) and click **More** then **Manage Rules**.

2. Click **Change**.

    > **Note:** This option only shows if the category/folder has linked rules.

3. Select the site then select a folder.

    You can only select locations you have permission to access.

4. Click **Link**.

    This breaks the link to the original rule set and links you to the new one.

5. Click **Done**.

### Breaking the link to a rule set

If you don't need your rules anymore, breaking the link is easy. This leaves the category/folder without any rules.

1. Click **Manage Rules** when you're in the folder or category in the File Plan you want to break a link to rules for.

    > **Tip:** You can also hover over a category/folder with rules applied (indicated by the ![]({% link governance-services/images/rules-icon.png %}){:height="18px" width="18px"} icon) and click **More** then **Manage Rules**.

2. Click **Unlink**.

    The link between the current category/folder and the linked rules is now broken.
---
title: Working with Azure Immutable Blob (WORM) Storage
---

You can use the Azure Immutable Blob (WORM) Storage by creating a Rule and an Action in Governance Services.

WORM storage (Immutable Blob Storage) is an Azure Blob Storage capability allows you to store objects using the write once, 
read many (WORM) model. Records moved to WORM storage use an Azure Blob Storage Container that is configured to support object locking . 
The movement of records is controlled through record folder rules and actions. You use the WORM model 
where it is a requirement that your data is not changed once it has been written to disk. This may be a requirement of 
yours due to regulatory compliance in the governmental, financial, or healthcare sectors.

The movement of records to WORM storage and through to disposition can be fully automated. A folder rule is configured 
to test records for the classification that requires WORM storage. This may be based on when a records enters a folder 
or complex meta data conditions. When triggered the rule causes the Object Lock action to be initiated in Azure Blob Storage. 
This action is configured with the required WORM retention period in days. For records that are moved to WORM locked 
storage any retention schedules that may have been applied are interrupted. At the end of the required retention period 
in WORM storage the records are automatically returned to the original default Azure Blob container to allow normal record operations 
to re-commence, including the application of retention schedules and disposition.

While retained in WORM storage additional controls are applied to prevent any user including administrators from deleting 
the records. Adding records to one or more legal holds during the WORM storage retention period causes the Azure Blob Storage legal 
hold flag to be set on the record in Azure Blob Storage. This prevents deletion or editing of the record in Azure Blob Storage even if the 
WORM retention period has expired. Once the record has been removed from all legal holds it was added to, the legal hold 
flag is cleared and the record can be removed from the WORM container once the retention period has expired.

There is some configuration required before you can use this feature. For more see 
[Creating a container in Azure Blob Storage for use as WORM storage](#createcontainerforworm).

Once you have created the container in Azure Blob Storage for use as WORM storage you can use it as storage. For more see 
[Using WORM storage](#usingworm).

Although the content of a WORM-locked record will be protected against modifications, any copies of WORM-locked records 
in other record folders will be stored using the rules for that folder. Consequently, copies of records may not be protected 
by the same restrictions.

You are unable to reject a Record that is stored in WORM storage and you can't move Records that are stored in WORM storage.

## Configuring a storage account and creating a storage container in Azure for use as WORM storage {#createcontainerforworm}

These steps describe how to use the Azure Portal to create a storage container for use as WORM storage 
(Azure Blob Level Immutability) in Azure. Once you have created the container you can create rules for a category or folder to 
store your data using WORM storage.

For more on creating rules see [Creating a rule]({% link governance-services/latest/using/automate-fileplan.md %}#creating-a-rule).

> **Note:** Ensure you have the required Azure login credentials before you begin.

* Installed Alfresco Content Services 23.2 (or above).
* Installed Alfresco Content Connector for Azure 5.0.0 (or above) with multiple container support enabled.
  * For more see [Configuring multiple storage containers in Azure Connector]({% link microsoft-azure/latest/config/index.md %}#configuring-multiple-storage-containers).
* Set the following properties in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file:

    | Property                                    | Description                                                                                                                                                                                                                |
    |---------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | worm.contentstore                           | This property is the key of the content store that has a WORM container.                                                                                                                                                   |
    | worm.retentionPeriod                        | This property controls the default retention period. It is specified in days and the default value is `2192` which is six years.                                                                                             |
    | connector.az.store2.retentionPeriodProperty | This property passes the AGS property which stores the unlock date of an object to Content Connector for Azure. You must enter this value: `{http://www.alfresco.org/model/recordsmanagemententerprise/1.0}wormUnlockDate`. |
    | rm.wormUnlockRecords.cronExpression         | This cron expression is used to specify how often the unlock job should run in Governance Services. The default is 15 minutes.                                                                                             |
    | connector.az.store2.blobImmutabilityPolicy  | This property controls immutability policy type at single blob level. Possible values: `Unlocked`(default)/`Locked`                                                                                                        |

1. Log in to your Azure Portal.

    You can only enable Blob immutability policy on the creation level, so you must create a new Storage Account to enable WORM feature.

2. Click **Create resource** and type **storage account** in the search field.

3. Once the **Storage account** tile is displayed, expand the **Create** dropdown at the bottom of the tile and choose **Storage account**.

4. On the first screen choose the desired subscription, resource group, enter a name for the storage, select the required Region, and then click **Next**. You can keep all other options default.

5. Under the next two tabs, you can leave all options default or change them at your convenience.

6. Under the **Data protection** tab you must select the **Enable versioning for blobs** and **Enable version-level immutability support** checkboxes.

    It is recommended to set `Keep all versions` under **Enable versioning for blobs**.

7. You can leave the next two tabs with default values or modify them at your convenience and go to **Review** tab where you should click **Create** button.

8. Under your storage account with versioning and version-level immutability support you need to create a storage container which is WORM capable.

9. Under your newly created Storage Account go to the **Containers** tab and click **+Container** (create container).

    Type in the container name. Under **Advanced** section select **Enable version-level immutability support** and click **Create**

10. You may want to set default retention based immutability policy for your container.

    To do so, go to the **Containers** tab, click the ellipsis (3 dots) for your container and choose **Access policy**.

11. Under the **Immutable blob storage** section choose add policy.

    1. Choose `Time-based retention` policy type and type in the desired number of days in `Set retention period for` field and click **Save**.

        This retention period must match the retention period you configured in the Alfresco Global Properties file for the `worm.retentionPeriod` property.

    2. To use this bucket as WORM storage you must now create rules for a category or folder in Governance Services using the **WORM lock** action. If you use the REST API you can use the action without a rule.

## Using WORM storage {#usingworm}

These steps describe how to use WORM storage with Governance Services, how to use WORM storage when you specify a 
retention period, and when you use Legal Hold.

This task assumes you have:

* Created a container in Azure Blob Storage for use as WORM storage.
  * For more see [Creating a container in Azure Blob Storage for use as WORM storage](#createcontainerforworm).
* Familiarised yourself with how to create rules in Governance Services.
  * For more see [Creating a rule]({% link governance-services/latest/using/automate-fileplan.md %}#creating-a-rule).

1. Log in to Governance Services.

2. (Optional) Click **More** and then **Add to Hold** if you want to use a Legal Hold for your new rule.

    Select the Hold you want to add the folders or categories to and click **OK**.

3. Click **More** and then **Manage Rules** for the folder or category you want to set rules for.

    > **Note:** If you have selected a Hold then you will need specific IAM permissions on your AWS account to delete the record after the WORM-lock has expired.

4. Click **Create Rules**.

5. Enter a name for the new rule.

6. Define the rule.

7. Select **WORM lock** from the **Perform Action** drop-down list.

8. Enter a retention period in days.

    If you don't enter a retention period, the default period used is the one you set for the `worm.retentionPeriod` property in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file.

    > **Note:** When using the WORM Lock action you must select **Run in Background** when creating rules for your categories or folders.

9. Click **Create**.
---
title: Easy access records
---

In many cases you might want to create records from files that already exist in Alfresco, rather than 
creating a record from scratch.

With Alfresco Records Management you can declare files in non-Records Management site as records. When you create an 
"easy access record", a record of the file is added to the Records Management site. The file is still visible in its 
original site, identified by the ![Easy access record]({% link governance-services/images/ico-rm-inplace.png %}){:height="18px" width="18px"} icon, 
but is locked and with a limited set of actions available.

This means that most users never need to think about records, {% include tooltip.html word="fileplan" text="file plans" %}, 
or {% include tooltip.html word="retentionschedule" text="retention schedule" %}s. They just declare the 
file as a record, and the rest is handled by the Records Administrator and any rules that they've set up.

When a record is created from a file it's added to the {% include tooltip.html word="unfiledrecords" text="Unfiled Records" %} 
area of the Records Management site. 
A Records Manager then has numerous options for [Filing an unfiled record]({% link governance-services/latest/using/file-records.md %}#filing-an-unfiled-record) and 
[Managing unfiled records]({% link governance-services/latest/using/manage-fileplan.md %}#managing-unfiled-records)

There are three options available for declaring files as records:

* **File as Record**

    Use File as Record to declare records from files in non-Governance Services sites and then select a destination folder where they will be filed as a record.

    > **Note:** You don't have to select a destination folder and if you don't the created record can be found in the unfiled records area.

* **File Version as Record**

    Use File Version as Record to create a record from a version of a file and then to select a destination folder where the version will be filed as a record.

    > **Note:** You don't have to select a destination folder and if you don't the created record can be found in the unfiled records area.

* **Auto-Declare Options**

    Each time a new major or minor version of the file is created, the version is declared as a record and added to the Unfiled Records area, in the explorer panel of the Records Management site. It's identified there as a version record by the ![Version record]({% link governance-services/images/ico-record-version.png %}){:height="18px" width="18px"} icon.

    It's still available in its original site, with a full set of actions available, identified by the ![Major revisions]({% link governance-services/images/ico-rm-major-revisions.png %}){:height="18px" width="18px"} major versions icon or the ![All revisions]({% link governance-services/images/ico-rm-all-revisions.png %}){:height="18px" width="18px"} all versions icon.

    > **Note:** Your Alfresco Administrator can choose to only make these options available to certain users only. If they've done this then you'll need to be a member of the RECORD_CONTRIBUTORS group for these options to be available.

    And as with standard Alfresco functionality you need to have the required permissions before you can do anything with files.


You can see version details of records created from versions in the file preview screen on the Records Management site. 
When records are created from versions of the same file, a relationship between the records is automatically created.

You can also classify a file and declare it as a record at a later date, and it will keep 
any classifications applied. See next section.

## Classifying files and folders

You can classify files and folders and apply {% include tooltip.html word="securitymark" text="security mark" %}s so that they can only be viewed or accessed by users who 
have the required {% include tooltip.html word="securityclassification" text="security classification" %}.

There are four security classification levels you can assign. {% include tooltip.html word="securitygroups" text="Security groups" %} provide additional classification options.

> **Note:** You can also [classify records]({% link governance-services/latest/using/smc.md %}#classifyrecordsfolderscategories) in the File Plan.

See [Classification rules and tips]({% link governance-services/latest/using/smc.md %}#classification-rules-and-tips) for more on classifying content.

You can autoclassify by by adding instructions, manually apply classifications and security marks, or both.

1. In the Document Library of an Alfresco site hover over a file or folder and select **More**, then **Classify**.

   You can classify using both **Security Classification** and **Security Groups**. You'll only see the classification options that you have security clearance for.

2. **To autoclassify:**

3. Click **Add Instructions**.

4. Click on a guide to view its topics.

5. Click ![Add instructions]({% link governance-services/images/ico-instructions-action.png %}){:height="18px" width="18px"} next to the topic you want to apply instructions from then click **Select**.

   > **Tip:** You can click **View** to check what classification level and security marks the topic instructions contain.

6. Repeat for as many topics as you want to add.

7. Click **Apply**.

    All the topics you've selected will have their instructions applied to the item you're classifying.

    > **Tip:** If topics contain instructions that clash then the higher level of classification will apply. For example if you add two topics, one with a classification level of Top Secret, and one with Secret, then the Top Secret level will apply.

8. **To add Other Classification Source References**

   > **Note:** This step is not required to classify an item.

9. Enter the name of the source document from which the classification of the item has been derived.

10. Enter the name of the organization that produced the document.

11. Enter the {% include tooltip.html word="fileplan" text="File Plan" %} of the document.

12. **To manually add classifications and security marks:**

13. If you want to classify a folder and its contents, select **Apply Classification to Folder Contents**.

    This option is only visible when classifying a folder. Only the top level folder and its immediate children are classified and only the metadata of the parent is carried over to the children. If a new child object is added at a later date it does not inherit the properties of its parent.

14. Select a classification from:

    * **Top Secret**
    * **Secret**
    * **Confidential**
    * **Unclassified**
    
    > **Tip:** If you select **Unclassified** then the item will be available to all users.

15. Enter a classification agency, for example, government or other body (optional).

16. Select one or more classification reasons from the list of available reasons.

17. You can optionally set a **Downgrade Schedule** or a **Declassification Schedule**.

    **Downgrade Schedule**

    Set a schedule for when the item will be downgraded, for example, from Top Secret to Secret. You can enter a specific date for the downgrade to take place, an event that means a downgrade should be considered, and instructions on how to carry out the downgrade. All of these are optional, but once you've entered a downgrade date, event, or both, you're required to enter instructions.

    **Declassification Schedule**

    Set a schedule for when the file will be declassified. These means when its classification level will be set to Unclassified. You can enter a specific date for the declassification to take place, an event that means declassification should be considered, and exemptions for when declassification shouldn't take place. All of these are optional.

    > **Note:** Downgrade and declassification schedules are not automated. Any reclassification needs to be done manually.

18. Click security marks to apply them to the item, and again to remove them.

    You cannot use security marks you do not posses when classifying content, unless you also use a security mark you do posses from the same group. If you have a security mark from a security group 'any' then you can view and assign all other marks from that group. When using marks (either when Classifying Content or creating Instructions) that you don't posses, you must include a mark from the same group to avoid losing access to the content. An error will appear if you attempt to create an instruction using only a mark you don't have, or have not included a mark from the same group.

    See [How security controls work]({% link governance-services/latest/using/smc.md %}#how-security-controls-work) for more details.

19. Click **Classify**.

    The item now displays its classification level, and can only be seen by those with the required {% include tooltip.html word="securityclassification" text="security classification" %}.

    > **Tip:** Items set to Unclassified with no applied security marks can be seen by all users.

    The option to **Share** the file is no longer available for Top Secret, Secret, or Confidential items. When a file or folder is declared as a record it retains its classification level and any security marks.

    The classification reason and classification-related properties can be seen in the **Properties** when you preview the file.

    > **Note:** When you classify a file it isn't added to the Records Management site File Plan. If you want to create a record from it you still need to [declare the file as a record](#declaring-a-file-as-a-record)

    If you delete a classified file then it's permanently deleted and isn't available in your Trashcan. If you delete a classified folder then all of its content is permanently deleted, even items that haven't been directly classified themselves.

## File as Record

You can create records from files in non-Governance Services sites and select the destination folder where they will be filed as a record.

1. In the Document Library of an Alfresco site find the file you want to declare as a record and file to a specific location.

2. Hover over the file and click **More** then **File as Record**.

3. Select where you want to file the record.

4. Click **Declare and File**.

   The file is added to the chosen destination folder in your Governance Services site. It's still visible in the original site, identified by the ![Easy access record]({% link governance-services/images/ico-rm-inplace.png %}){:height="18px" width="18px"} icon, but is locked and has a limited set of actions.
    
   > **Note:** If the file is locked, you won't see the **File as Record** action. A file that has been filed as a record can be deleted but the record remains in the File Plan.

## File version as a record

When files are updated in Alfresco, a new version number of the file is created. You can declare one or more of these 
versions as records, allowing you to keep a record of the changes that have been made throughout the life cycle of a file.

1.  In the Document Library of an Alfresco site find the file you want to file a version of as a record.

    > **Tip:** You can see a file's version history by clicking on the file, then in the file preview screen scrolling down to the Version History section. You can revert to previous versions by clicking the ![Revert version]({% link governance-services/images/ico-revert-version.png %}){:height="18px" width="18px"} icon.

2.  Hover over the file and click **More** then **File Version as Record**. Select a location where you would like to file the record.

    You don't have to select a destination folder and if you don't the created record can be found in the unfiled records area.

    > **Note:** If the file is locked or synced with an Alfresco in the Cloud site you won't see the **File version as Record** action. A file that has been filed as a record can be deleted but the record remains in the File Plan.

You can find these records in the {% include tooltip.html word="unfiledrecords" text="Unfiled Records" %} folder in the File Plan explorer panel. New records display in the 
File Plan as incomplete records. Any required metadata needs to be added before the records can be set to complete.

> **Note:** A file that has had versions declared as records can be deleted. The records remain in the File Plan.

If you delete or destroy a record that was declared from a version, then that version is marked as deleted and can't be accessed. Other versions of the file remain unaffected.

> **Tip:** You can also set up folder rules in a non-Records Management site so the file versions can be automatically declared as records. For example, you could create a rule that when a file is tagged as "Confirmed", then a record will be created of that file version and added to the Records Management site. Version details will be available when looking at the record in the file preview screen on the Records Management site.

## Setting auto-declare options

You can set up auto-declare option for files so that major and minor version numbers will automatically be declared as records.

Auto-declare options are set on a file by file basis, though you can set up a folder rule and apply auto-declare settings 
to multiple files.

1. In the Document Library of an Alfresco site find the file you want to set auto-declare options for.

2. Hover over the file and click **More** then **Auto-Declare Options**.

    The Set Auto-Declare Options screen opens with the default setting of **Never**.

3. Select to automatically declare versions as records:

    * **For major versions only**

        Each time a new major version of the file is created, the version is declared as a record and added to the Unfiled Records area, in the explorer panel of your Records Management site. It's identified there as a version record by the ![Version record]({% link governance-services/images/ico-record-version.png %}){:height="18px" width="18px"} icon. In its originating site it'll display the ![Major revisions]({% link governance-services/images/ico-rm-major-revisions.png %}){:height="18px" width="18px"} icon, and the ![Easy access record]({% link governance-services/images/ico-rm-inplace.png %}){:height="18px" width="18px"} icon next to each recorded version in the Version History section of the file preview screen.

    * **For all major and minor versions**

        Each time a new major or minor version of the file is created, the version is declared as a record and added to the Unfiled Records area, in the explorer panel of your Records Management site. It's identified there as a version record by the ![Version record]({% link governance-services/images/ico-record-version.png %}){:height="18px" width="18px"} icon. In its originating site it'll display the ![All revisions]({% link governance-services/images/ico-rm-all-revisions.png %}){:height="18px" width="18px"} icon, and the ![Easy access record]({% link governance-services/images/ico-rm-inplace.png %}){:height="18px" width="18px"} icon next to each recorded version in the Version History section of the file preview screen.

4. Click **OK** to save these settings.

    You can change the settings whenever you need to, but any records already created will be unaltered.


From this point forwards, each time a new version of the file is saved, a record is automatically created from the version and can be filed in the File Plan. You can find them in the Unfiled Records area in the File Plan explorer panel. New records display in the File Plan as incomplete records. Any required metadata needs to be added before the records can be set to complete. Version details will be available when looking at the record in the file preview screen on the Records Management site.

> **Note:** A file that has had versions declared as records can be deleted. The records remain in the File Plan.

## Moving easy access records

Although easy access records have most of their options removed, you can still move them to a different place in their originating site.

This can be useful if you want to keep files that have been declared as records in a dedicated part of a site.

1. In the Document Library of an Alfresco site find a file that's been declared as a record.

2. Hover over the file and select **Move Record**.

3. Choose the folder where you want to place the content.

    Files that have been declared as records can be moved to anywhere in their current site, but cannot be moved to a different site.

4. Click **Move**.

    The file is moved to it's new location in the site. The record of the file in the Records Management site is unaffected.

## Hiding easy access records

Once a file has been declared as a record, you have the option to hide it from its originating site.

This can help to avoid any confusion with site members trying to work with files that have been declared as records.

Once hidden, the record created from the file is available as usual in the Records Management site, but in its originating site it's no longer available in the document library.

1. In the Document Library of an Alfresco site find a file that's been declared as a record.

2. Hover over the file and select **Hide Record**.

3. Click **OK** to confirm that you want to hide the record.

    The record's now hidden from the Document Library. Once a record has been hidden it can't be unhidden. If a record is rejected from the Records Management site then it will become visible again with a warning that it's been rejected.

## Rejected records

After you've created a record from a file, the Records Manager has the option to reject the record from the Records Management site.

If they reject the record then the original file will display a warning that it's a **Rejected Record**. At this point the options to declare the file as a record aren't available. You can:

* Click ![Rejected record reason]({% link governance-services/images/ico-rm-rejectreason.png %}){:height="18px" width="18px"} to view the reason why the record was rejected.
* Click ![Remove rejected warning]({% link governance-services/images/ico-delete.png %}){:height="18px" width="18px"} to remove the rejection warning. The options to declare the file as a record are now available again.
---
title: Governance Services FAQ
---

Here are the answers to some frequently asked questions about Records Management.

## What are the differences between a DoD 5015.2 and standard Records Management sites?

When you create a Records Management site you can choose to create a DoD 5015.2 site or a standard site. 
If your organization is required to meet DoD 5015.2 compliance, then select **{% include tooltip.html word="dod50152std" text="DoD 5015.2-STD" %}**. 
Records on a DoD 5015.2 site have additional mandatory metadata the must be completed. 
Mandatory metadata includes the originator, the originating organization, the {% include tooltip.html word="fileplan" text="File Plan" %}, the destroy action.

## How does classification interact with standard Records Management permissions?

There are two levels of interaction between classification and permissions. To view a classified file or record you 
need to have read permissions for that file and the required clearance level. 
To classify a file or record, or edit the classification, you need to have read and file permission and clearance 
to use the classification level(s) involved.

## Why can't I see a classified record when I have the required clearance?

Having the required clearance level isn't all that's needed to view a classified record. 
You also need to have the required permissions, including but not restricted to permission to view the category, 
permission to view the folder, and permission to view the record.

## Why are the tags showing more files than I can see?

Depending on your {% include tooltip.html word="securityclassification" text="security classification" %} level, some files or records might be hidden from you in Alfresco. 
The tags link displays the total number of files that have that tag, but when you click it you'll only be able to 
see those that you have access to.

![Hidden tagged files]({% link governance-services/images/rm-tags-faq.png %})

## Why can't I upload a file when I have the required permissions?

In each folder you can't have multiple files of the same name. You might have permissions to add files, 
but may not have {% include tooltip.html word="securityclassification" text="security classification" %} to see, for example, files that have been classified as Top Secret. 
If you try to upload a file when there is already one in the folder, even if you can't see it, 
you'll receive a message: Unexpected error occurred during upload of new content.

## Are RSS feeds secure?

RSS feeds are secure, but the login credentials are stored by the browser you're using and not Alfresco. 
As such it's recommended that you close your browser after logging out of Alfresco and / or lock your computer 
while you're away from it.

## Why isn't hot backup working properly?

The default behavior for classified records is "immediate delete", which means that content is deleted immediately, 
and will not be included in a hot backup. If you have performed a hot backup and you try to retrieve content 
that was deleted, a Requested resource is not available message is displayed.

## Records uploaded using CIFS, WebDav, or FTP don't have any content?

There's a known issue that when users with the Records Management User role and Read and File permissions add a 
record using CIFS, WebDav, or FTP, the record is added but it's content is removed. Other issues may also occur. 
It's recommended that users in this situation are given an alternate Records Management role to resolve the issue.

---
title: Filing records
---

Filing records is the process of classifying records and putting them into the correct location in the {% include tooltip.html word="fileplan" text="File Plan" %}.

There are three ways that you can create records:

* Create a record by uploading files
* Create a non-electronic record that references a physical record such as a paper record or microfilm
* Select an item in another Alfresco site (non-Records Management) and declare it as a record

> **Note:** You can also import folders, {% include tooltip.html word="category" text="categories" %}, and even entire File Plans, and any records that they contain, see [Exporting and importing File Plan content]({% link governance-services/latest/using/manage-fileplan.md %}#exporting-and-importing-file-plan-content).

Your Alfresco administrator can also set up your system so that emails to specified addresses are captured and stored 
as records.

A record is not considered to be complete until all the required metadata has been added to it. 
You select **Edit Metadata** to complete required metadata.

In {% include tooltip.html word="dod50152std" text="DoD 5015.2-STD" %} compliant Records Management sites you can also select to **Add Record Metadata** and associate 
the file with a record type, so that when you edit metadata there is type-specific metadata to add.

Once that's done you can select to **Complete Record** and it will be subject to the retention rules that apply to 
the folder you've placed it in.

> **Note:** When you set up a record category or folder you can specify that it will be used to hold **Vital Records**. A vital record must be reviewed on a periodic basis, as defined on the record category or folder.

## Filing an electronic record

Electronic records are files that are uploaded to a records folder. Non-{% include tooltip.html word="electronicrecord" text="electronic records" %} might be paper files that 
can be stored in a physical location.

1. In the record folder where you want to file a record click **File**.

2. Click **Electronic**.

3. Click **Select Records to File** and find the file that you want to upload.

    > **Tip:** You can also select multiple items in the standard multi-select way.

    The files are uploaded as record and display in the {% include tooltip.html word="fileplan" text="File Plan" %} as incomplete records. You need to make sure any 
    required metadata is added before you can set records to {% include tooltip.html word="recordcompleted" text="complete" %}.

See also video explaining [filing an electronic record]({% link governance-services/latest/tutorial/governance-services/index.md %}#file-a-record).

## Filing a non-electronic record

Non-electronic records might be paper files that can be stored in a physical location. Filing a non-electronic record in the File Plan means the file can be traced and details of where it is physically stored can be recorded.

1. In the record folder where you want to file a record click **File**.

2. Click **Non-electronic**.

3. Enter details for the file you are making a record of.

    Only the Name and Title are required, but you should enter enough information so that the record will be recognized by other users.

4. Click **Save**.

    A new record is created and displays in the File Plan as an incomplete record. You need to make sure any required metadata is added before you can set records to complete.

## Filing an unfiled record

When you've declared a record from a non-Records Management site it's added to the **Unfiled Records** area. 
You now need to add it to a records folder.

1. Click the **Unfiled Records** area on the explorer panel on the left of the page.

    All {% include tooltip.html word="unfiledrecords" text="unfiled records" %} are displayed.

    > **Note:** You can add additional folders to the **Unfiled Records** area to create a folder hierarchy to help manage unfiled records. You can also declare items as records directly from within the **Unfiled Records** area structure.

2. Hover over an unfiled record and click **More** then **File to...**.

3. Select a records folder to file the record in then click **File**.

    > **Note:** There are multiple other actions available including **Reject** so you can reject the record from the {% include tooltip.html word="fileplan" text="File Plan" %}, and **Move to** so you can move the record to another location in the **Unfiled Records** hierarchy.

The record's added to the File Plan, and if you haven't already you can now go and edit metadata.

See also video explaining [filing an unfiled record]({% link governance-services/latest/tutorial/governance-services/index.md %}#file-an-unfiled-record).

## Adding record metadata

All records in the {% include tooltip.html word="fileplan" text="File Plan" %} have metadata, which you can think of as records properties.

If you associate the record with a specific type by selecting the **Add Record Metadata** option then additional metadata 
options are required for the record. You need to complete all the required metadata before you can set a record to {% include tooltip.html word="recordcompleted" text="complete" %}.

The **Add Record Metadata** option is only available in {% include tooltip.html word="dod50152std" text="DoD 5015.2-STD" %} compliant Records Management sites.

> **Note:** Adding record metadata isn't mandatory, but can be useful to allow additional metadata to be added against a file.

1. Hover over an incomplete record in the File Plan and click **More** then **Add Record Metadata**.

    > **Tip:** For non-{% include tooltip.html word="electronicrecord" text="electronic records" %} the **Add Record Metadata** is available as soon as you hover over them, you don't need to click **More**.

    The available record types are displayed.

2. Select the appropriate record type.

    |Record type|Description|
    |-----------|-----------|
    |Web Record|A web page.|
    |Scanned Record|A file that is scanned into the Records Management system.|
    |PDF Record|A PDF file.|
    |Digital Photograph Record|A photographic image file.|

    > **Tip:** You can select multiple items in the standard multi-select way.

3. Click **OK**.

    Some record metadata is mandatory. Before you can complete a record, you must edit the metadata to complete the mandatory fields.

Icons next to the record show the record types that it's been associated with. Hover over an icon to display the record type.

See also video explaining [adding record metadata]({% link governance-services/latest/tutorial/governance-services/index.md %}#add-a-record-type).

## Editing record metadata

You can edit record metadata to add information to a record.

Before you can {% include tooltip.html word="recordcompleted" text="complete" %} a record, you must enter any required details about the record in the metadata. You can't edit record metadata after you have set the record to complete.

1. Hover over a record in the {% include tooltip.html word="fileplan" text="File Plan" %} and click **Edit Metadata**.

    The **Edit Metadata** page displays. The metadata fields you see on this page depend on the file type, and whether or not record types have been associated with the file. The metadata is divided into sections, with additional sections dependant on if a record type has been associated with the item.

2. Enter the record metadata. 

    If your Records Management system is {% include tooltip.html word="dod50152std" text="DoD 5015.2-STD" %} compliant then every file includes the DOD5015 Record section, which is a default set of basic metadata fields. The default record metadata fields are:

    |Property/metadata|Description|
    |-----------------|-----------|
    |Publication date|*Required*. The date that the record is published. Select the date from the calendar selection box.|
    |Originator|*Required*. The person or department in the originating organization.|
    |Originating Organization|*Required*. The organization that created the record.|
    |Media Type|The general media type such as audio, video, or document.|
    |Format|The format in which the record is stored, such as electronic or physical file.|
    |Date received|The date that the record was received from the originator.|
    |Addressee|The email address of the originating organization to be used for correspondence.|
    |Other Addressee|The secondary recipients of the message (CC).|
    |Location|The physical location of the record, generally only applicable to non-{% include tooltip.html word="electronicrecord" text="electronic records" %}.|
    |Supplemental Marking List|Any additional properties applicable to the record. This list is defined by the Alfresco administrator in the **List of Values** in the RM Admin Tools.<br><br>This is available in both standard and DoD 5015.2-STD compliant File Plans.|

    You can't save this page until you complete any required fields.

3. Click **Save**.

See also video explaining [editing record metadata]({% link governance-services/latest/tutorial/governance-services/index.md %}#edit-record-metadata).

## Requesting record information

If you need additional information to complete a record, you can request this from other users.

1. Hover over a record in the File Plan and click **More** then **Request Information**.

2. Click **Select** and select a user or group to request the information from.

3. Enter details of what you need in the Requested information box.

4. Click **Request Information**.

    A task will be assigned to the selected user and will show in their My Tasks dashlet. Once they mark the task as done the information they provide will be shown in a task assigned to the user who requested the information. Access the information through your My Tasks dashlet and click Task Done to close the information request.

## Completing a record

Content added to the {% include tooltip.html word="fileplan" text="File Plan" %} must be set to complete before it is recognized as a record.

1. Hover over an incomplete record in the File Plan and click **Complete Record**.

    > **Tip:** Incomplete records are marked.

    If a record has mandatory metadata that hasn't been completed then a message lets you know that required metadata is missing.

Once a record is {% include tooltip.html word="recordcompleted" text="completed" %}, it comes under the control of the record {% include tooltip.html word="category" text="category" %} it is filed under, and security restrictions apply.

> **Note:** A record can be filed in multiple categories, see [Linking records]({% link governance-services/latest/using/manage-fileplan.md %}#linking-records) for more details.

See also video explaining [completing a record]({% link governance-services/latest/tutorial/governance-services/index.md %}#complete-a-record).---
title: Managing the File Plan
---

The record {% include tooltip.html word="category" text="categories" %}, record folders, and records in the File Plan structure each have an appropriate set of actions. You can access the actions by hovering over an item in the File Plan or by clicking on an item name. Use these actions to manage the File Plan.

> **Note:** The standard Alfresco **Copy to**, **Move to** and renaming options are available for record categories, record folders, and records. See [Keeping your library organized]({% link content-services/latest/using/content/manage.md %}#organizing-content) for further details.

## Managing record categories

There are various options available to help you manage record categories. These are available to users with the appropriate {% include tooltip.html word="capabilities" text="capabilities" %}.

In the File Plan hover over a record category to display the available actions:

|Action|Select this to...|
|------|-----------------|
|View Details|View the record category details page, where you can see the metadata and a full list of actions.|
|Edit Metadata|Edit the record category metadata.|
|Manage Permissions|Set the user and group access for the category.|
|Copy to|Create a copy of the category in another location in the File Plan.|
|Move to|Move the category to another location in the File Plan.|
|Delete|Delete the category from the File Plan.|
|View Audit Log|View the auditing information for the category. The Audit Log displays the activity information and has options to export and file as a record.|
|Manage rules|Create and edit rules so that category content is managed automatically.|

### Viewing record category details

The record category details page gives you access to the actions available to be performed on the category, the custom metadata, the {% include tooltip.html word="retentionschedule" text="retention schedule" %}, and the category URL.

1. Hover over a record category in the File Plan and click **View Details**.

    The details page displays. On this page, you can see the metadata, the retention schedule, and the available actions in the Actions list.

    If no retention schedule has been set for the record category, you create it here. If a retention schedule exists, you can edit it.

    Where a retention schedule exists, click **View Description** in the Retention Steps section to display the description for a particular step.

2. Click the location link above the record category name to return to the File Plan.

### Editing a record category

You can edit a record category if you need to make any changes to its metadata.

1. Hover over a record category in the File Plan and click **Edit Metadata**.

    The Edit Metadata page displays.

2. Edit the metadata details as necessary.

3. Click **Save**.

### Deleting a record category

When you don't need a record category any more you can delete it.

1. Hover over a record category in the File Plan and click **Delete**.

    A confirmation dialog box displays.

2. Click **Delete**.

    The record category is removed from the Records Management system.

    > **Important:** This will also delete the folders and records within the record category.

## Managing record folders

There are various options available to help you manage record folders. These are available to users with the appropriate {% include tooltip.html word="capabilities" text="capabilities" %}.

In the File Plan hover over a record folder to display the available actions. The standard actions available are shown. Additional options are available dependant on the stage a folder is at in the retention schedule. See the relevant topics for further details.

|Action|Select this to...|
|------|-----------------|
|View Details|View the record folder details page, where you can see the metadata and a full list of actions.|
|Edit Metadata|Edit the record folder metadata.|
|Close Folder|Close the folder. A {% include tooltip.html word="recordfolderclosed" text="closed" %} record folder cannot accept records for filing. When you close the folder, this action toggles to the **Re-open Folder** action.|
|Edit Retention Date|If a folder is subject to a folder level {% include tooltip.html word="retentionschedule" text="retention schedule" %}, you can review the retention date for the next step in the retention schedule that applies to the folder.|
|Review All|Mark all vital records in a folder as having been reviewed.|
|Add to Hold|Hold the folder. You can view on {% include tooltip.html word="fileplan" text="File Plan" %} folders in the **Holds** area on the explorer panel. When you hold the folder, this action toggles to the **Remove from Hold** action.|
|Copy to|Create a copy of the folder in another location in the File Plan.|
|Move to|Move the folder to another location in the File Plan.|
|Manage Permissions|Set the user and group access for the folder.|
|Delete|Delete the folder from the File Plan.|
|View Audit Log|View the auditing information for the folder. The Audit Log displays the activity information in a new window and has options to export or file this information as a record.|
|Manage rules|Create and edit rules so that folder content is managed automatically.|

> **Note:** When the folder is closed or on hold, a limited set of actions is available.

### Viewing record folders

The record folder details page gives you access to the actions available to be performed on the folder, the custom metadata, and the folder URL.

1. Hover over a record folder in the File Plan and click **View Details**.

    The details page displays. On this page, you can see the metadata and the available actions in the Actions list.

2. Click the location link above the record folder name to return to the File Plan.

### Editing a record folder

You can edit a record folder if you need to make any changes to its metadata.

1. Hover over a record folder in the File Plan and click **Edit Metadata**.

    The Edit Metadata page displays.

2. Edit the metadata details as necessary.

3. Click **Save**.

### Completing folder events

If a retention schedule has event-based steps, then you need to complete those events before the schedule can move on to the next step. Some steps are automatically completed but most of them you need to complete manually.

1. Click the title of a folder in the File Plan.

    The record details page is displayed. All incomplete events for the current schedule step are displayed.

2. Click **Complete Event**.

3. In the complete Event box select a date and time for the completion of the event..

4. Click **OK**.

When all incomplete events are complete the folder can move onto the next step in the schedule.

### Editing a folder retention date

If a folder is subject to a folder level retention schedule, you can review the retention date for the next step in the retention schedule that applies to the folder. This is done at folder level only and does not affect the retention schedule.

1. Hover over a folder in the File Plan and click **More** then **Edit Retention Date**.

    The Edit Retention Date dialog box displays. The current retention date is highlighted.

2. Select a new retention date and click **Update**.

    A message displays confirming that the retention date is updated. This overrules any review dates set in the retention schedule.

### Processing records in a folder

See [processing records](#processing-records) under managing records section.

### Adding record folders to a hold

Users with the appropriate {% include tooltip.html word="capabilities" text="capabilities" %} can add record folders to a hold.

A hold allows objects on hold for a particular reason to be tracked as a set. Holds prevent changes to on hold objects, which have their retention schedules suspended until the hold is removed.

> **Note:** When you add a folder to a hold, all records within the folder are also added to the hold. The records can't be removed from the hold individually, they can only be removed from the hold by removing the entire folder.

1. Hover over a record folder in the File Plan and click **More** then **Add to Hold**.

    The Add to Hold screen displays.

    > **Note:** This option isn't available if no holds have been set up in the Holds area or you don't have permission to put records on the existing holds.

2. Select one or more holds and click **OK**.

    A message displays confirming that the folder is on hold, and the folder now displays the ![Frozen]({% link governance-services/images/ico-rm-frozen.png %}){:height="18px" width="18px"} icon.

    > **Note:** Records and folders remain on hold until they have been removed from all holds they're added to.


The folder remains in its' place in the File Plan. It is also shown in the **Holds** area of the explorer panel.

> **Note:** To remove a record folder from a hold hover over it in the File Plan or the Holds area and select **Remove from Hold**.

### Closing a record folder

Users with the appropriate capability (Folder Control) can close folders. {% include tooltip.html word="recordfolderclosed" text="Closed" %} folders cannot accept any further records.

1. Hover over a record folder in the File Plan and click **Close Folder**.

    A message displays confirming that the folder is closed.

    > **Note:** The action for this folder changes to **Re-open Folder**, which allows the folder to be reopened.

### Deleting a record folder

When you don't need a record folder any more you can delete it.

1. Hover over a record folder in the File Plan and click **Delete**.

    A confirmation dialog box displays.

2. Click **Delete**.

    The record folder is removed from the Records Management system.

    > **Note:** This will also delete the records within the record folder.

## Managing records

There are various options available to help you manage record. These are available to users with the appropriate {% include tooltip.html word="capabilities" text="capabilities" %}.

In the File Plan hover over a record to display the available actions. The standard actions available are shown. 
Additional options are available dependant on the stage a record is at in the {% include tooltip.html word="retentionschedule" text="retention schedule" %}. 
See the relevant topics for further details.

|Action|Select this to...|
|------|-----------------|
|Download|Download the file to your computer.|
|Edit Metadata|Edit the metadata for the record.|
|Complete Record|Declare the file as a record. All required metadata fields must be complete. When you declare the file as a record, this action toggles to the **Reopen Record** action.|
|Reviewed|Marks a vital record as reviewed.|
|Reopen Record|Revert the item back to an incomplete record.|
|Add Record Metadata|Associate an undeclared record with one or more record types. This option is only available in {% include tooltip.html word="dod50152std" text="DoD 5015.2-STD" %} compliant Records Management sites.|
|Add to Hold|Hold the record. You can view on hold records in the **Holds** area on the explorer panel. When you hold the record, this action toggles to the **Remove from Hold** action.|
|Copy to|Create a copy of the record in another location in the File Plan.|
|Move to|Move the record to another location in the File Plan.|
|File to|File an unfiled record to the File Plan.|
|Link to|File a record in multiple locations in the File Plan and create a link. This gives the appearance of duplicating the record in another location, though actually there is just one record stored in multiple folders. Changes made to the record in one location will be reflected in the other locations.|
|Unlink Record|Available for records that have been linked from another record, you can unlink the record. This will remove it from the folder it was linked to.|
|Delete|Delete the record from the File Plan.|
|View Audit Log|View the auditing information for this record. The Audit Log displays the activity information in a new window and has options to export or file this information as a record.|
|Reject|Reject an unfiled record. If you select to reject a record then you need to enter a reason for the rejection. This reason be viewed when looking at the file the record was created from in it's originating site.|
|Request Information|Request further information about a record from other users. This is only available for incomplete records.|
|Manage Permissions|Use the **Manage Permissions** option to control user permissions for records.|
|Add Relationship|Add a relationship between records such as a cross-reference or obsoleted by.|

When a record has been completed not all of these actions will be available.

When the record is on hold (identified by the ![Frozen]({% link governance-services/images/ico-rm-frozen.png %}){:height="18px" width="18px"} icon), a limited set of actions is available.

Vital records display the ![Vital record]({% link governance-services/images/ico-rm-vitalrecord.png %}){:height="18px" width="18px"} icon.

### Viewing records

The record details page gives you access to the actions available to be performed on a record, the custom metadata, references to and from other records, and the record URL.

1. Click the title of a record in the File Plan.

    The record details page displays. On this page, you can see the record details and the available actions in the Actions list.

2. Click the location link above the record name to return to the File Plan.

### Linking records

You can link records to a folder other than the one they're filed in to file them in multiple locations in the File Plan.

This gives the effect of "duplicating" the record in another location, though there is still only one record, but it's now contained in more than one folder. Changes made to the record in one location will be reflected in all the other locations, and this includes deleting the record.

> **Important:** It's recommended that you don't link a record to a location where it will be subject to a retention schedule with different steps or a different sequence of steps.

> **Note:** The link option is only available to users who have the Link Records capability assigned to them by the Records Management Administrator.

1. Hover over a record in the File Plan and click **More** then **Link to**.

2. Select a folder in the File Plan to link a record to.

3. Click **Link**.

    A link is created in the destination folder. All copies of the record display the ![Linked]({% link governance-services/images/ico-rm-linkedrecord.png %}){:height="18px" width="18px"} icon.

    > **Note:** Linked records won't move to the next retention step until the period for the current step has been completed in all retention schedules it falls under. So in effect they follow the retention schedule that has the longest period for a step.


You can click **More** then **Unlink Record** against the record in the destination folder. This will remove the linked record from the destination folder.

> **Note:** The unlink option is only available to users who have the Unlink Records capability assigned to them by the Records Management Administrator.

### Creating relationships between records

You can add relationships to records to create a connection between them. This can be useful, for example, to track records that have been superseded or obsoleted.

1. Hover over a record in the File Plan and click **More** then **Add Relationship**.

2. Select a relationship type in the New Relationship screen.

    > **Note:** Most relationships don't alter or affect a record in any way, they are just used to create an association between records.

    However, if you select Obsoleted by/Obsoletes or Superseded by/Supersedes, then any outstanding retention schedule obsoleted or superseded events will be automatically completed.

3. Click **Select Record** and then select a record to create a relationship with by clicking ![Add]({% link governance-services/images/ico-add.png %}){:height="18px" width="18px"}.

4. Click **OK**.

    The selected record is shown in the New Relationship screen.

5. Click **Create**.

    You can repeat these steps to add relationships to multiple other records. You can see details of any relationships when you click on a record to preview it, and relationships can be added and deleted here if you have the correct permissions.

    When records are created from versions of the same file, a relationship between the records is automatically created.

### Reviewing vital records

If you've set up a review period for vital records in the record category or folder, you can review this for individual records.

Users with Records Manager permissions receive a notification email when vital records are due for review.

1. When a record is due for review hover over it in the File Plan.

    > **Tip:** You can search for vital records using the **Records Search** on the **More** menu. Records that are due for review will display a warning symbol in the search results.

2. Click **Reviewed**.

    A message displays saying that the record has been successfully reviewed. The review date is displayed in the record audit log.

### Managing unfiled records

All records filed from a non-Records Management site are added to the {% include tooltip.html word="unfiledrecords" text="Unfiled Records" %} area by default.

> **Tip:** Access the Unfiled Records area using the explorer panel to the left of the File Plan.

Unfiled records can have been {% include tooltip.html word="declareasrecord" text="declared" %} as records from a non-Records Management site, from within the Unfiled Records area, or could be reports generated from within the File Plan. [Filing an unfiled record]({% link governance-services/latest/using/file-records.md %}#filing-an-unfiled-record) describes how records in the Unfiled Records area are processed.

You don't have to use this area as a flat structure, you can configure it to your own requirements.

You can create a full folder hierarchy within the Unfiled Records area and use [rules]({% link governance-services/latest/using/automate-fileplan.md %}) to automate the processing of unfiled records.

You can use the **Manage Permissions** option to control which users can file and reject unfiled records.

There are also many of the usual options available, including the options to copy and move records and folders within the Unfiled Records area. If you select to **Reject** a record then you need to enter a reason for the rejection. This reason can be viewed when looking at the file the record was created from in its originating site.

### Completing record events

If a {% include tooltip.html word="retentionschedule" text="retention schedule" %} has event-based steps, then you need to complete those events before the schedule can move on to the next step. Some steps are automatically completed but most of them you need to complete manually.

1. Click the title of a record in the File Plan.

    The record details page is displayed. All incomplete events for the current schedule step are displayed.

2. Click **Complete Event**.

3. In the complete Event box select a date and time for the completion of the event.

4. Click **OK**.

When all incomplete events are complete the record can move onto the next step in the schedule.

### Editing a review date

If you've set up a review period for vital records in the record category or folder, you can edit the review date for individual records.

1. Hover over a record in the File Plan and click **More** then **Edit Review Date**.

    The Edit Review Date dialog box displays. The current review date is highlighted.

2. Select a new review date and click **Update**.

    A message displays confirming that the review date is updated. This overrules any review dates set at folder or category level.

### Editing a record retention date

If a record is subject to a record level retention schedule, you can review the retention date for the next step in the retention schedule that applies to the record. This is done at record level only and does not affect the retention schedule.

1. Hover over a record in the File Plan and click **More** then **Edit Retention Date**.

    The Edit Retention Date dialog box displays. The current retention date is highlighted.

2. Select a new retention date and click **Update**.

    A message displays confirming that the retention date is updated. This overrules any review dates set in the retention schedule, even if you update the retention schedule.

### Processing records

Retention steps are generally completed manually, though retain and cut off steps can be completed automatically 
by a system process that is run daily. You can also set up a rule to complete steps automatically.

If a retention step is complete (the time period is finished or the required {% include tooltip.html word="events" text="events" %} have been completed), 
then additional options are available for folders or records, dependant on whether the {% include tooltip.html word="retentionschedule" text="retention schedule" %} 
is set to folder or record level.

If you apply an action to a folder then it will also be applied to all records within the folder.

1. Hover over a folder/record in the {% include tooltip.html word="fileplan" text="File Plan" %} and click the action that is available to move to the next step in the retention schedule.

    |Action|Select this to...|
    |------|-----------------|
    |Cut off|Cuts off the record/folder and triggers the retention period. Records can't be added to a folder that's been cut off.|
    |End Retention|Ends the retention period for the record/folder.|
    |Transfer|Transfers the record/folder to the previously specified location. An audit trail and metadata is retained.By default {% include tooltip.html word="transfer" text="transferred" %} records/folders are temporarily held in the Transfers area of the File Plan until you hover over them and click **Complete Transfer**.|
    |Accession|Transfers the record/folder to the previously specified location. An audit trail and metadata is retained.<br><br>This usually involves the specific legal and physical transfer of records between organizations.<br><br>By default {% include tooltip.html word="accession" text="accessioned" %} records/folders are temporarily held in the Transfers area of the File Plan until you hover over them and click **Complete Transfer**.|
    |Destroy|Removes the record/folder content from the Records Management system. If the **Maintain record metadata after destroy** option is selected in the retention schedule, then a visual representation of the record, an audit trail, and metadata is retained in the File Plan.<br><br>If the record was declared from a file in an Alfresco site then the file is also removed.|

    > **Note:** Each time you manually run an action, that option is replaced with the next action step in the retention schedule, and a new option for undoing the step you've just done, for example, **Undo Cut Off**.

    Icons next to the record/folder indicate their current stage in the schedule.

See also video explaining [processing records]({% link governance-services/latest/tutorial/governance-services/index.md %}#process-records).

### Adding records and record folders from the File Plan to a hold

Users with the appropriate {% include tooltip.html word="capabilities" text="capabilities" %} can add records, and record folders to a hold to freeze them. Holds prevent changes to on hold items, which have their retention schedules suspended until the hold is removed.

> **Note:** Smart folders can't be added to a hold. Adding system files to a hold is also not supported and could create errors, this includes data dictionary files.

A hold allows objects on hold for a particular reason to be tracked as a set.

> **Note:** When you add a record folder to a hold, all records within the folder are also added to the hold. The records can't be removed from the hold individually, they can only be removed from the hold by removing the entire folder.

> **Tip:** This functionality isn't available if at least one hold hasn’t been set up or you don't have permission to put records on the existing holds.

1. Hover over a record or record folder in the File Plan and click **More** and then **Add to Hold**.

    To add more than one item to a hold at the same time, select each one and click the **Select Items** drop down list and then select **Add to Hold**.

    The Add to Hold screen displays.

2. Select one or more holds and click **OK**.

    A message displays confirming that the record or record folder is on hold, and it displays the ![Frozen]({% link governance-services/images/ico-rm-frozen.png %}){:height="18px" width="18px"} icon.

    > **Note:** Records and folders remain on hold until they have been removed from all the holds they're added to.


The record remains in its place in the File Plan. It is also shown in the **Holds** area of the explorer panel.

> **Note:** To remove a record from a hold hover over it in the File Plan or the Holds area and select **Remove from Hold**. See [Removing items from hold]({% link governance-services/latest/using/search-records.md %}#removing-items-from-hold).

### Adding content from the Document Library to a hold

Users with the appropriate {% include tooltip.html word="capabilities" text="capabilities" %} can add content to a hold to freeze them. Holds prevent changes to on hold items.

> **Note:** Adding system files to a hold is not supported and could create errors, this includes data dictionary files.

A hold allows items on hold for a particular reason to be tracked as a set.

> **Tip:** This functionality isn't available if at least one hold hasn’t been set up or you don't have permission to put content on the existing holds.

1. Hover over your content in the Document Library and click **More** and then **Add to Hold**.

    To add more than one item to a hold at the same time, select each one and click the **Selected Items** drop down list and then select **Add to Hold**.

    The Add to Hold screen displays.

2. Select one or more holds and click **OK**.

    A message displays confirming the content is on hold, and the content now displays the ![Frozen]({% link governance-services/images/ico-rm-frozen.png %}){:height="18px" width="18px"} icon.

    > **Note:** Content remains on hold until it has been removed from all the holds they're added to.


The content remains in its place in the Document Library. It is also shown in the **Holds** area of the File Plan explorer panel.

> **Note:** To remove content from a hold hover over it in the File Plan, Document Library or the Holds area and select **Remove from Hold**. From the Holds area in the File Plan and from the List view in the File Plan you can remove more than one item at a time. You do this by selecting your items and clicking the **Selected Items** drop down list and then **Remove from Hold**. See [Removing items from hold]({% link governance-services/latest/using/search-records.md %}#removing-items-from-hold).

### Reverting a record to be an incomplete record

If you need to stop a record from being subject to retention schedules, you can reopen it so that it reverts to being an incomplete record.

1. Hover over a record in the File Plan and click **More** then **Reopen**.

    The record is now marked as an incomplete record in the file plan and is not subject to the rules of the retention schedule. You can set it to complete again whenever needed.

### Deleting records

When you don't need a record any more you can delete it.

1. Hover over a record in the File Plan and click **Delete**.

    A confirmation dialog box displays.

2. Click **Delete**.

    The record is removed from the Records Management system. If the record was declared from a file in an Alfresco site then the file is also removed.

## Managing records holds

You can add content, records, and record folders to a hold to freeze them. For records, and record folders this would also suspend their retention schedules.

You can create as many different holds as you want, which are represented as folders in the Holds area.

> **Tip:** Access the Holds area using the explorer panel to the left of the File Plan.

In the Holds area there's a **New Hold** option which you use to set up your different hold types. Once you have a list of different holds you can put content, records, and, record folders on as many of the different holds as required.

You can also add records to a hold directly from your search results, see [Adding search results to a hold - Records Search]({% link governance-services/latest/using/search-records.md %}#addsearchresults2holdRecordsSearch) and [Adding search results to a hold - Share search]({% link governance-services/latest/using/search-records.md %}#addsearchresults2holdShareSearch).

When you add a record folder to a hold, all records within the folder are also added to the hold. They'll stay on hold until removed from the hold or the hold is deleted.

In the Holds area you can see your holds. When you go into a hold you can see the items it contains. The items aren't removed from the File Plan. They retain their place in the File Plan or Collaboration site with limited actions available, and are identified as being on hold by the ![Frozen]({% link governance-services/images/ico-rm-frozen.png %}){:height="18px" width="18px"} icon.

> **Note:** Only users with permissions to view a hold will see the ![Frozen]({% link governance-services/images/ico-rm-frozen.png %}){:height="18px" width="18px"} icon next to records in the File Plan that are on that hold. Users without permission to view the hold will see the record but have no indication that it is on a hold. This provides confidentially on record holds.

You can use the **Manage Permissions** option to control which users can view, create, edit, and delete holds. Users who don't have read permission for a specific hold will not receive any indication that records it contains are in that hold.

> **Tip:** You can hover over a hold and click **Generate Hold Report** to create a report on the hold. The report is filed as an incomplete record in your selected destination.
  
Users with the appropriate capabilities can create multiple holds that are then used when records are put on hold. See next section.

### Creating holds

Users with the appropriate {% include tooltip.html word="capabilities" text="capabilities" %} can create multiple holds that are then used when records are put on hold.

> **Tip:** You can only put records on hold if holds have been created to add them to.

1. Click on the Holds area of the File Plan in the explorer panel, and click **New Hold**.

2. Enter a Name, Description and Reason for the hold.

    > **Note:** The reason will be used to when deciding which hold a record should be put on.

3. Click **Save**.

    A new hold is now available for putting records on. You put records on hold by hovering over them in the File Plan and selecting the **Add to Hold** option.

You can edit and delete holds by hovering over them in the File Plan and selecting the appropriate option, as well as managing their permissions and viewing an audit log.

## Exporting and importing File Plan content

You can quickly and easily import and export Records Management content, from individual record folders through to an entire File Plan.

This can be useful if you want to quickly build your File Plan, or parts of it, based on a File Plan that already exists on an Alfresco system.

You can move entire blocks of content – record categories, record folders, records, metadata, and retention schedules – within a File Plan or to another File Plan.

Files are imported and exported using the Alfresco Content Package (ACP) format. You can also choose to import and export the content as a zip file. Exported files contain all structural information including record categories, folders, and retention schedules, so they make for seamless building of a File Plan in another Alfresco system.

### Exporting content

Exporting a records category or folder bundles the contents and structure into an Alfresco Content Package (ACP). You can also choose to export the content as a zip file.

1. In the File Plan click the check boxes for the record category and/or folders you want to export.

2. Click **Selected Items** then **Export**.

3. Select the file format for the export and click **OK**.

    > **Note:** A zip file retains the file structure, making it bigger than an ACP. In an ACP the file structure is stored in an xml file.

    Depending on your browser, you are either prompted to specify a destination or the file is automatically downloaded to a default location.

### Exporting a File Plan

Exporting a File Plan bundles the contents and structure of the entire plan into an Alfresco Content Package (ACP). You can also choose to export the plan as a zip file.

1. Anywhere in the File Plan click **Export All**.

2. Select the file format for the export and click **OK**.

    > **Note:** A zip file retains the file structure, making it bigger than an ACP. In an ACP the file structure is stored in an xml file.

    Depending on your browser, you are either prompted to specify a destination or the file is automatically downloaded to a default location.

### Importing content

Importing an Alfresco Content Package (ACP) or zip file into a Records Management system expands the package to its original structure. Existing content will not be overwritten.

1. Go to the level in the File Plan structure where you want to import the ACP/zip file.

2. Click **Import**.

3. Click **Select Import File** and find the file that you want to upload.

    > **Important:** You should only import an ACP/zip file that was exported from another Records Management File Plan.

    The Records Management content is extracted from the uploaded file with it's original structure maintained.
---
title: Managing permissions
---

To ensure the security of your Records Management system you can easily manage user permissions to control which 
users and groups can see and work in different sections of the {% include tooltip.html word="fileplan" text="File Plan" %}.

In Alfresco Records Management there are 2 different methods for managing what users can and can't do:

* Roles and {% include tooltip.html word="capabilities" text="capabilities" %} are managed by the Alfresco administrator, and control the actions users have within the 
File Plan, such as the ability to create record categories or record folders.
* User permissions are managed at folder and category level, and control whether users can read and file or just read.

User permissions aren't granted by default. If a user hasn't been given permission to read a folder or category, 
then they won't see it in the File Plan. Only Records Management Administrators are granted access to all areas of 
the File Plan by default.

By managing your user permissions you can create restricted areas of the File Plan that are only available to 
selected users. For an area that all users should have access to, you need to make sure that all users have been 
given permission to see it.

## Setting user permissions

Setting user permissions on folders and {% include tooltip.html word="category" text="categories" %} lets you control who can see and work in different areas of the {% include tooltip.html word="fileplan" text="File Plan" %}.

> **Tip:** Remember that until you have given users permission for a folder or category they won't be able to see it or work with its contents.

1. Click **Manage Permissions** when you're in the folder or category you want to set permissions for in the File Plan.

    > **Tip:** You can also hover over a folder in the File Plan and click **More** then **Manage Permissions**, or a category in the File Plan and click **Manage Permissions**.

    The **Manage Permissions** page opens with the name of the selected folder or category displayed. Any users and groups that currently have permissions assigned are also displayed. You can change existing user permissions or **Remove** them entirely.

2. Click **Add User or Group**.

3. Enter the name of an individual user, a group, or a Records Management role and click **Search**.

    All users, groups, and roles matching the search are displayed.

4. Click **Add** next to the user, group, or role that you want to add permissions for.

    > **Tip:** You can add permissions for as many users, groups, and roles as you want.

5. Select either **Read and File** or **Read Only**.

    Read and File allows users to work with content, whereas users with Read Only permission can only view content.

6. When you're finished click **Save** to return to the File Plan.

    The permissions you've set are now applied to the folder or category you selected and any folders or categories it contains. You can change these as needed on a folder or category basis.


See also video explaining [setting user permissions]({% link governance-services/latest/tutorial/governance-services/index.md %}#set-user-permissions).---
title: Introduction to using Governance Services
---

With Governance Services you store and control all your records in a dedicated site. 
A Governance Services site is like other Alfresco sites, but with additional controls placed on its content.

Access a Governance Services site just as you would any other Alfresco site, from the **My Sites** dashlet or the **Sites** menu.

Instead of storing your files in a document library as you do in a "regular" Alfresco site, in a Governance Services 
site you file your records in the *File Plan*. And you can't edit the content of records; once they're in the File Plan 
record content is considered to be final.

You file records by adding them from your computer to the File Plan, or if you're in another Alfresco site you can 
declare a file as a record and it will be added to the Governance Services site. Once files are added to the File Plan 
you can edit their metadata (properties) but you can't edit their actual content.

## Records management roles

Although Governance Services has a huge amount of functionality available, it's actually pretty easy to learn the essentials and get up and running.

What you do in Governance Services will vary hugely depending on your role, and how your company is organized. 

As a *Records Manager* you're responsible for ensuring the Records Management site is properly organized and managed. The background configuration of the site should be managed by your Records Management administrator in the RM Admin Tools. This leaves you to get on with managing the site organization, devising and ensuring the implementation of retention and disposal schedules, and enabling appropriate access to information.

As a *User* of the Records Management site you need to file records and process them as easily as possible. Your Records Manager will have organized the site and set up retention and retention schedules, leaving you to get on with managing and processing the site records.

## Life cycle of a record

You can create a record either by uploading it to the 
Records Management {% include tooltip.html word="fileplan" text="File Plan" %}, or by declaring a file in another Alfresco site as a record.

When you have added all required metadata to a record you can mark the record as {% include tooltip.html word="recordcompleted" text="complete" %}. 
This makes it an active part of the File Plan, and subject to the rules of the {% include tooltip.html word="retentionschedule" text="retention schedule" %} it is 
associated with.

It then goes through various time and {% include tooltip.html word="events" text="event" %} based steps such as {% include tooltip.html word="cutoff" text="cut off" %} and retention, 
until it is eventually transferred elsewhere, or destroyed, according to its retention schedule.

![Record Lifecycle]({% link governance-services/images/record-lifecycle.png %})

## Further information

If you're new to Alfresco then take a look at [Using Alfresco]({% link content-services/latest/using/index.md %}) to help you get started.

For more details on setting up and administering Governance Services see [Administering Records Management]({% link governance-services/latest/admin/index.md %}).

> **Note:** It's recommended that you use the File Plan for Governance Services actions rather than going through the repository.
---
title: Retention schedule
---

Retention schedules define how records are managed in the Records Management system until their eventual destruction 
or transfer to another location. The period between a record being completed and becoming part of the {% include tooltip.html word="fileplan" text="File Plan" %}, 
and being destroyed/transferred is known as its retention period.

A retention schedule is attached to a record {% include tooltip.html word="category" text="category" %}, and once a file has been completed as a record it's subject to 
the rules of the retention schedule that's attached to the category it's in.

A retention schedule contains one or more steps that define a particular action to be carried out. 
These actions can be carried out after a period of time, after certain events, or a combination of the two.

The steps that can make up a retention schedule are:

|Option|Description|
|------|-----------|
|Cut off|This is the first step in a retention schedule. Once a record is cut off this triggers the records retention period. You can't add records to a folder that's been cut off.|
|Retain|This is an alternative first step that is a 'placeholder' step which delays the next retention step until after a selected time period or event.|
|Transfer|Records are transferred from one location to another. This can be applicable to both electronic and non-electronic records, and will be used, for example, when transferring records from an organization to an archive.|
|Accession|An advanced form of transfer usually involving the specific legal and physical transfer of records between organizations.|
|Destroy|Electronic records are removed from the Records Management system and destroyed, and non-electronic records must be destroyed.|

> **Note:** You can add multiple steps to a retention schedule, but the first step must be either a Cut off or Retain action, and no steps can be added after the Destroy action.

When a retention schedule is created you specify whether its instructions are applied at folder or record level.

* Folder level - you manage the folder through the retention schedule and all the records it contains are processed as a single entity.
* Record level - records in a folder are managed individually through the retention schedule and can be at different stages of the retention process to other records in the folder.

> **Tip:** When a record folder is cut off, this cuts off all individual records in the folder, regardless of their current state.

Retention steps can be manually completed once they are considered eligible (the time period has passed and/or the events 
have been completed), though the retain and cut off steps can be completed automatically by a system process that is run daily. 
All other retention steps must be completed manually, or by setting up a rule to complete them automatically. 
If a retention step is complete, then additional options are available for folders or records, dependant on whether the 
retention schedule is set to folder or record level, see [Actioning retention steps]({% link governance-services/latest/using/manage-fileplan.md %}#processing-records).

## Example of a retention schedule

Retention schedules can be set up to account for all different kinds of operational processes.

Here is an example of the steps in a fairly straightforward retention schedule.

Records that are associated with this schedule will be cut off after one month in the File Plan. They will then be retained in the File Plan for two years or until they're no longer needed, whichever comes first. At that point they will then be destroyed.

![Retention Schedule example]({% link governance-services/images/schedule-example.png %})

## Creating a retention schedule

A retention schedule is created against and associated with a record {% include tooltip.html word="category" text="category" %}. First you create a summary of the schedule, then the steps in the schedule.

1. Hover over a record category in the {% include tooltip.html word="fileplan" text="File Plan" %} and click **View Details**.

    The **Category Details** page displays and if the category already has a retention schedule then you'll see the schedule summary and steps.

2. Click **Create Retention Schedule**.

3. In the **General** section, click **Edit**.

4. Complete all fields:

    |Field|Description|
    |-----|-----------|
    |Retention Authority|The authority that states how the record should be retained and disposed, for example *Sarbanes-Oxley Act (SOX)* or *Corporate procedures*.|
    |Retention Instructions|A summary of the retention schedule.This information is not actively used but this text is displayed in the record category summary in the File Plan, and is important from a legal perspective.|
    |Applied to|**Record Folder**: the retention schedule is applied to folders and all operations occur at the folder level. With this setting, you cannot manage records as individual units. If you {% include tooltip.html word="cutoff" text="cut off" %} the folder, all records will be cut off. <br><br> **Record**: the retention schedule is applied to records and all operations occur at the record level.|

    > **Note:** If you add folders to a category before setting up the retention schedule, then you can only select **Record Folder**.

5. Click **Save**.

    The category details page now displays a summary of the new or updated retention schedule.

Next you need to add steps to the retention schedule.

See also video explaining [creating a retention schedule]({% link governance-services/latest/tutorial/governance-services/index.md %}#create-a-retention-schedule).

## Creating retention schedule steps

When you've set up a retention schedule, you need to add retention steps. The steps give the retention schedule 
it's control over records and folders.

1. Hover over a record {% include tooltip.html word="category" text="category" %} in the {% include tooltip.html word="fileplan" text="File Plan" %} and click **View Details**.

    The **Category Details** page displays showing the retention schedule summary.

2. In the **Retention Steps** section, click **Edit**.

    The **Edit Retention Schedule** page displays.

3. Click **Add Step** and select a retention action.

    |Option|Description|
    |------|-----------|
    |Cut off|This is the first step in a retention schedule. Once a record is cut off this triggers the records retention period. You can't add records to a folder that's been cut off.|
    |Retain|This is an alternative first step that is a 'placeholder' step which delays the next retention step until after a selected time period or event.|
    |Transfer|Records are transferred from one location to another. This can be applicable to both electronic and non-{% include tooltip.html word="electronicrecord" text="electronic records" %}, and will be used, for example, when transferring records from an organization to an archive.|
    |Accession|An advanced form of {% include tooltip.html word="transfer" text="transfer" %} usually involving the specific legal and physical transfer of records between organizations.|
    |Destroy|Electronic records are removed from the Records Management system and destroyed, and non-electronic records must be destroyed.|

    > **Note:** You can add multiple steps to a retention schedule, but the first step must be either a Cut off or Retain action, and no steps can be added after the Destroy action.

4. Select whether the action will be triggered after a period of time or when a specified {% include tooltip.html word="events" text="event" %} occurs:

    |Option|Description|
    |------|-----------|
    |After a period of|Select the time period after which the step action will take place.<br><br> **Note:** If you select XML Duration from the Period Type drop down list you can specify a time interval using XML syntax.<br><br>The syntax should take the form of:<br><br>P = Period (required)<br><br>nY = Number of years<br><br>nM = Number of months<br><br>nD = Number of days<br><br>T = Start time of a time section (required if specifying hours, minutes, or seconds)<br><br>nH = Number of hours<br><br>nM = Number of minutes<br><br>nS = Number of seconds<br><br>For example, 'P2M10D' represents two months and ten days.<br><br>Created Date = The date when the file or record is first added to Alfresco.<br><br>Retention Action = The date when the last retention action took place. Don't select this for the first step in the schedule.<br><br>The "Quarter" option splits the year into 4 sets of 3 months, beginning with Jan/Feb/March. "Financial Quarter" is the same but based on the start of your system-configured financial year. See [Customizing the end of the financial year]({% link governance-services/latest/config/index.md %}#customize-end-of-year).|
    |When event happens|Select the event after which the step action will take place.<br><br>Most events must be completed manually in the record details page, or you can use rules to automatically complete these events.<br><br>The Obsolete, Superseded, and Related Record Transferred To Inactive Storage events are automatically completed when [relevant relationships are set up between records]({% link governance-services/latest/using/manage-fileplan.md %}#creating-relationships-between-records).|

    > **Note:** You can select both options, or multiple events, and have the action triggered by **Whichever event is earlier** or **When all events have happened**.

    The date selected here is displayed as the **Retention as of date** in the details page for records or folders, depending on which the retention applies to. If you select an event then this field will display *None*, and you should complete the event on the details page.

5. If you added a Destroy step then there is an additional **Keep record metadata after record destruction** option. If you select this option then destroyed records are still represented in the File Plan rather than being completely deleted. An audit trail and metadata remain but the records can't be accessed.

    > **Note:** The metadata is maintained indefinitely unless it is manually deleted from the File Plan by someone with the ALFRESCO\_ADMINISTRATOR role, or another role that has been given permissions to delete the metadata.

6. Enter a **Step Description**.

7. Click **Save**.

    > **Tip:** You can click the ![Edit icon]({% link governance-services/images/ico-configure.png %}){:height="18px" width="18px"} edit icon or ![Delete icon]({% link governance-services/images/ico-delete.png %}){:height="18px" width="18px"} delete icon next to a step to edit or delete it.

8. When you've entered all the required steps click **Done**.


You return to the category details page, which displays the retention steps. Click **View Description** to the right of a step to display the description.

See also video explaining [creating retention schedule steps]({% link governance-services/latest/tutorial/governance-services/index.md %}#create-retention-schedule-steps).

## Editing a retention schedule

Once a retention schedule has been created you can go back and edit it at any point.

1. Hover over a record category in the File Plan and click **View Details**.

    The category details page displays and if the category already has a retention schedule then you'll see the schedule summary and steps.

2. In the General section click **Edit** to edit the basic details, or click **Edit** in the Retention Steps section to edit, add, or delete steps.

3. When you've finished click **Done**.
---
title: Searching records
---

You can use the Records Search to quickly search the {% include tooltip.html word="fileplan" text="File Plan" %} to find records, and save your search query to use again.

You can either do a basic search, just searching for a term as you would in a search engine, or you can use the 
advanced search functionality. There's lots of options available for you to set really specific searches that you 
can use again and again. See [Advanced search options](#advanced-search-options) for more details on getting the most 
out of the search tool.

## Accessing the Records Search

You can search records to find those that you're looking for, and save searches for future use.

1. In the Records Management site click **Records Search**.

    The Search page displays.

2. Click the **Criteria** tab to perform a search or the **Results** tab to view the results of a search.

## Creating a search

You can search all the contents of your Records Management site. You can narrow the results of your search by specifying relevant metadata fields and container types ({% include tooltip.html word="category" text="category" %}, folder, record). Once you create a search, you can save it to use again.

See [Advanced search options](#advanced-search-options) for how to get the most out of the search facility.

1. On the Records Search **Criteria** tab enter a search term in the box.

2. If you want you can use the **Search by** field and **Search Date** options to do a more advanced search.

    |Search criteria|Description|
    |---------------|-----------|
    |Search by|Select from the options available what you want to search for. When you select an option it's added to the field below where you can then enter your search criteria. For example if you select **Retention Schedule > Retention Action Name**, the field name `retentionActionName:` is added and you can then type a retention action name, such as `retentionActionName:cutoff`. Don't insert a space between the colon and the search term. You can select multiple criteria.|
    |Search Date|Select a date to search on or even multiple dates, see [searching for date ranges](#searching-for-date-ranges).|

3. Expand the **Results options** section and specify the content you want displayed in the search results.

    1. In the Metadata section, select the metadata fields that you want to display in the search results. The metadata name becomes a column title in the results table, which can then be sorted.

    2. In the Order section, specify how you want to sort the search results.

    3. In the Components section, select the type of components you want the search to return.

4. Click **Search**.

    The search results display in a table on the Results tab.

Clicking **New Search** returns you to the Criteria tab and clears the search fields, setting them to their default values. This lets you easily create a new search.

### Search query examples

Use these examples to see how the Search by and Search Date options work.

* **Finding folders/records due for cut off before 1st Jan 2010**

    `dispositionActionName:cutoff and dispositionActionAsOf:[MIN TO "2010-01-01"]`

* **Finding records due for transfer before 1st Jan 2010**

    `dispositionActionName:transfer and dispositionActionAsOf:[MIN TO "2010-01-01"]`

* **Finding categories or folders with a monthly cycling date**

    `vitalRecordReviewPeriod::month`

    > **Note:** Ensure that you've selected the component in the**Results options** section.

### Search field options

If you select to **Search by** for a search, then the following fields are available if you select a **Content**, **Record**, or **Retention Schedule** field.

|Title|Field name|Description|
|-----|----------|-----------|
|Keywords (text and name)|`keywords`|Used to search for the name, title, description fields, and text. This field is tokenized.|
|Identifier|`identifier`|The unique identifier for the record. The system generates this identifier.|
|Name|`name`|The name of the record. This is populated with the name of the file that was uploaded.|
|Title|`title`|The title of the record. This is populated with the name of the file that was uploaded. Change the value to show the title of the record.|
|Description|`description`|A short description of the record.|
|Creator|`creator`|The person(s) who created this record.|
|Created|`created`|The date that this record was created.|
|Modifier|`modifier`|The last user to make any modifications to this record.|
|Modified|`modified`|The time that the last modification occurred.|
|Author|`author`|The name of the document author(s).|
|Originator|`originator`|The person or department in the Originating Organization.|
|Date Filed|`dateFiled`|The date that the record was filed.|
Publication Date|`publicationDate`|The date that the record is published. Select the date from the calendar selection box.|
|Review Date|`reviewDate`|The date that this record is due for review.|
|Originating Organization|`originatingOrganization`|This is who created the document/record in the first place. Often this will be the organization running the software, but in some cases might be an external organization.|
|Media Type|`mediaType`|The type of the media.|
|Format|`format`|The media on which the record is stored.|
|Date Received|`dateReceived`|The date that the record was received from the originator.|
|Location|`location`|The physical location of the record. This is mainly applicable to non-electronic records.|
|Addressee|`address`|The address of the originating organization to be used for correspondence.|
|Other Addressee|`otherAddress`|The CC list from an email.|
|Supplemental Marking List|`markings`|This list is defined in the RM List of Values tool in the RM Admin Tools.|
|Retention Events|`dispositionEvents`|User defined retention events.|
|Retention Action Name|`dispositionActionName`|The name of the retention action. The values can be Accession, Destroy, Retain, Transfer, and Cutoff.|
|Retention Action As of Date|`dispositionActionAsOf`|The date that the retention action occurred.|
|Retention Events Eligible|`dispositionEventsEligible`|Specifies whether this record has any eligible events. The values can be true or false.|
|Retention Period|`dispositionPeriod`|The period of time to which the retention action is set. The values can be day, fymonthend, fyquarterend, fyyearend, monthend, quarterend, yearend, immediately, month, none, notset, quarter, week, or year.|
|Has Retention Schedule|`dispositionSchedule`|Specifies whether this record is under a {% include tooltip.html word="retentionschedule" text="retention schedule" %}. The value can be true or false.|
|Retention Instructions|`dispositionInstructions`|The text summary of the retention steps.|
|Retention Authority|`dispositionAuthority`|The legislation relevant to the retention instructions, in particular, relating to the disposal of the record. For example, GRS 2 Item 7.|
|Hold Reason|`holdReason`|The reason that the record is in the Hold area.|
|Vital Record Review Period|`vitalRecordReviewPeriod`|The review period set for a vital record. The values can be day, fymonthend, fyquarterend, fyyearend, monthend, quarterend, yearend, immediately, month, none, notset, quarter, week, year.|

### Search record type field options

If you select to **Search by** for a search, then the following fields are available if you select a **Web Record**, **Scanned Record**, **PDF Record**, or **Digital Photograph Record** field.

> **Note:** These options are only available in {% include tooltip.html word="dod50152std" text="DoD 5015.2-STD" %} compliant Records Management sites.

|Record type|Special type name|Description|
|-----------|-----------------|-----------|
|Scanned records|`dod:scannedFormat`|Image Format|
|Scanned records|`dod:scannedFormatVersion`|Image Format Version|
|Scanned records|`dod:resolutionX`|Image Resolution X|
|Scanned records|`dod:resolutionY`|Image Resolution Y|
|Scanned records|`dod:scannedBitDepth`|Scanned Bit Depth|
|PDF records|`dod:producingApplication`|Producing Application|
|PDF records|`dod:producingApplicationVersion`|Producing Application Version|
|PDF records|`dod:pdfVersion`|PDF version|
|PDF records|`dod:creatingApplication`|Creating application|
|PDF records|`dod:documentSecuritySettings`|Document security settings|
|Digital photograph records|`dod:caption`|Caption|
|Digital photograph records|`dod:photographer`|Photographer|
|Digital photograph records|`dod:copyright`|Copyright|
|Digital photograph records|`dod:bitDepth`|Bit Depth|
|Digital photograph records|`dod:imageSizeX`|Image Size X|
|Digital photograph records|`dod:imageSizeY`|Image Size Y|
|Digital photograph records|`dod:imageSource`|Image Source|
|Digital photograph records|`dod:compression`|Compression setting|
|Digital photograph records|`dod:iccIcmProfile`|ICC/ICM profile|
|Digital photograph records|`dod:exifInformation`|EXIF information|
|Web records|`dod:webFileName`|Web file name|
|Web records|`dod:captureMethod`|Method of capture|
|Web records|`dod:contentManagementSystem`|Content management System|
|Web records|`dod:webPlatform`|Web platform|
|Web records|`dod:webSiteName`|Web site name|
|Web records|`dod:webSiteURL`|Web site URL|
|Web records|`dod:captureDate`|Date of capture|
|Web records|`dod:contact`|Capture contact|

## Using a saved search

The Records Management site includes a number of default searches that you can use instead of creating your own. You also have access to searches you've created and saved yourself, as well as those created by other users.

1. On the Records Search page click **Saved Searches** and select a search option.

    The **Critera** tab is auto-filled with the saved search options. You can change these if you want.

2. Click **Search**.

    The search results display in a table on the Results tab.

## Saving a search

When you've run a search and are looking at the search results, you can select to save it.

1. Click **Save Search**.

2. Enter a **Name** and **Description** for the search.

3. Click **Save**.

    The search you save will be available for all site members.

The saved search displays in the **Saved Searches** menu on the Search page. The same list is available 
in the explorer panel of the File Plan.

> **Note:** The saved search feature saves only the search query and not the results. This means that when you next use the saved search, you might get different results, depending on the activity in the Records Management system.

## Printing search results

You can print the search results.

1. Click the Records Search **Results** tab to view the search results.

2. Click **Printer Layout**.

3. Print the page using your browser print option.

4. Click **Screen Layout** to return to the standard view.

## Exporting search results

You can export search results as an Alfresco Content Package (ACP).

1. Click the Records Search **Results** tab to view the search results.

2. Click **Export**.

    Depending on your browser you are prompted to open or save the file.

    > **Note:** You can also export the results from the Printer Layout view.

## Deleting a saved search

You can delete any of your own saved searches, and if you have the required user permissions 
you can also delete the default searches included with the Records Management site.

1. Click the **Saved Searches** menu on the **Search** page to view the available search queries.

2. Select the query you want to delete.

    The **Critera** tab is displayed so you can check that this is the search you want to delete.

3. Click **Delete Search**.

4. Click **Remove** to confirm the deletion.

## Adding search results to a hold - Records Search {#addsearchresults2holdRecordsSearch}

Users with the appropriate {% include tooltip.html word="capabilities" text="capabilities" %} can add records, and record folders to a hold to freeze them. 
A hold allows objects on hold for a particular reason to be tracked as a set. Holds prevent changes to on hold objects, 
which have their retention schedules suspended until the hold is removed. When you add a folder to a hold, 
all records within the folder are also added to the hold.

1. Click the Records Search tab and search for an item you wish to add to a hold.

2. Review the search results and select the check box next to the item(s) you want to add to a hold.

3. Click the **Selected Items** drop down list and select **Add to Hold**.

    The Add to Hold screen displays.

4. Select one or more holds and click **OK**.

    A message displays confirming that the record or folder is on hold.

    > **Note:** If no holds have been set up in the Holds area then the screen will be empty. Records and folders remain on hold until they have been removed from all holds they're added to.

The selected records and/or folders remain in their place in the File Plan. They are also shown in the **Holds** area of the explorer panel.

> **Note:** To remove a record from a hold hover over it in the File Plan or the Holds area and select **Remove from Hold**. You can remove more than one record at a time by selecting your items and then clicking the **Selected Items** drop down list and then **Remove from Hold**.

## Adding search results to a hold - Share search {#addsearchresults2holdShareSearch}

Users with the appropriate {% include tooltip.html word="capabilities" text="capabilities" %} can add search result items from the main Share search to a hold. 
This means you can select search results from a records management site or from a collaboration site, and add them to a hold. 
This includes content, records, and record folders. For records and record folders this would also suspend their 
retention schedules. When you add a record folder to a hold, all records within the folder are also added to the hold.

> **Note:** Smart folders can't be added to a hold but each individual item in a smart folder can be added to a hold.

1. Within the Share search bar, search for an item you wish to add to a hold.

2. Review the search results and select the check box next to the item(s) you want to add to a hold.

3. Click the **Selected Items** drop down list and select **Add to Hold**.

4. Select one or more holds and click **OK**.

    A message displays confirming that the item or items you have selected are now on hold.

    > **Note:** If no holds have been set up in the Holds area then the screen will be empty. Content, records, and records folders remain on hold until they have been removed from all holds they're added to.

The selected content, records, and records folders remain in their place in the File Plan, or Document Library (depending on the type of item on hold). They are also shown in the **Holds** area of the explorer panel.

> **Note:** To remove content from a hold hover over it in the File Plan, Document Library or the Holds area and select **Remove from Hold**. From the Holds area in the File Plan and from the List view in the File Plan you can remove more than one item at a time. You do this by selecting your items and clicking the **Selected Items** drop down list and then **Remove from Hold**.

## Removing items from hold

You can remove an item from a hold.

> **Note:** From the Holds area in the File Plan and from the List view in the File Plan you can remove more than one item at a time. You do this by selecting your items and clicking the **Selected Items** drop down list and then **Remove from Hold**.

1. In the folder where your items are stored, select the item you want to remove from the hold.

2. Select **Remove from Hold** from the **Selected Items** drop down list.

3. Select the hold where the item is to be removed from.

4. Click **Remove**.

## Advanced search options

As well as basic searches where you search for a specific word, you can also create more complex full text searches with multiple matches, tokens, phrases, wildcards, ranges, and grouping.

Full text searches can be very simple, using a text string, or you can do more complex searches with multiple matches, tokens, phrases, wildcards, ranges, and grouping. The search syntax follows the format:

```text
<field-name>:<search-value>
```

* `<field-name>` is the field within Records Management. For example, `identifier` is the field name for the unique record identifier.
* `:` (colon) separates the field name from the search value. Make sure there's no space between the colon separator and the value.
* `<search-value>` is the value that you want to search for.

Alfresco Records Management has a large number of fields to search against, see [Search field options](#search-field-options) and [Search record type field options](#search-record-type-field-options). The search query requires that you enter the internal name of these fields in the text box. The **Search by** menu list assists you when entering the fields.

To search for phrases, wrap the value string in "quotes". You can also use the wildcard matching characters, question mark (?) for a single character, and asterisk (\*) for zero or more characters to apply to any text value.

### Searching for text

To search for a simple text string in any record content, enter the text string.

For example, to find the text “healthcare” in any completed record:

1. Type `healthcare` in the **Search Text** box.

2. In the **Results options** section, select the components you want to search.

    To find a simple text string in any record name, title, description, or content, enter the following in the Query Text box:

    `keywords:healthcare`

    The keywords field is a special field name that allows you to match against the name, title, description, and content of a record.

    The basic syntax for matching against a field in search queries is the syntax format of the keywords field, then the colon (:), followed by the value to match against.

### Search using wildcards

An example of a simple wildcard query is to match any word starting with 'health' in any record name, title, description, or content.

1. In the **Search Text** box, enter:

    `keywords:health*`

2. In the **Results options** section, select the components you want to search..

The single and multiple wildcard characters can be combined as needed. For example, "*care" and "*car?" both match "healthcare".

### Searching for multiple fields

Multiple fields can be combined to match additional results. Each field, by default, will be OR combined with the previous.

1. In the **Search Text** box, enter:

    `keywords:healthcare keywords:hospital`

2. To return results that only contain both terms, use AND between the terms:

    `keywords:healthcare AND keywords:hospital`

3. In the **Results options** section, select the components you want to search.


The NOT operator and grouping of terms with brackets "(" and ")" are supported. For example:

```text
(KEYWORDS:healthcare AND KEYWORDS:hospital) AND NOT KEYWORDS:clinic
```

### Searching for phrases

To search for phrases, wrap the value string in "double quotes". An example of phrase matching is to match the 
field `originator` with the phrase “John Smith”.

1. In the **Search Text** box, enter:

    `originator:"John Smith"`

2. In the **Results options** section, select the components you want to search.


Wildcards are supported within phrase matching. For example, to match records that contain the text "John Smith" or 
"John Smithe" in the **Originator** metadata field, use the following query text:

```text
originator:"John Smith*" 
```

You can also escape embedded quotes in a phrase using back slash `\`.

### Searching for exact term

To search for exact terms, prefix the term with an equals symbol (`=`). An example of exact term matching is to 
match the word “part”.

1. In the **Search Text** box, enter:

    `=part`

2. In the **Results options** section, select the components you want to search.

This search will match "part" but will not match other terms that contain "part", such as "partners".

### Searching for dates

To search for date values, you can match date fields exactly.

To return records that were filed on 10th September 2009:

1. In the **Search by** menu, select **Records** and then **Date Filed**.

2. Select the date using the **Search Date** control. The query text displays as:

    `"2009-09-10"`

### Searching for date ranges

To search for date values, you can match date fields in a range.

To return date ranges, the syntax requires the From and To dates to be surrounded by square brackets. 
For example, to return records that were filed on or before the 10th January 2010:

1. In the **Search by** menu, select **Records** and then **Date Filed**.

2. Add the following search query:

    `[MIN TO "2010-01-10"]`


You must surround the query with square brackets. Use the `TO` token between dates to represent the range.

Use the `MIN` special token to denote the minimum possible date that can be represented by the system.

Use the `MAX` and `NOW` special tokens to indicate the maximum possible date and the current date, respectively.

For example, to find all records that were filed today, use the following query text:

```text
dateFiled:NOW
```

### Searching for special types

To search for special types, you can match the special type names using ASPECT.

> **Note:** These options are only available in {% include tooltip.html word="dod50152std" text="DoD 5015.2-STD" %} compliant Records Management sites.

For example, to search for all digital photograph records:

1. In the **Search Text**box, type:

    `ASPECT:"dod:digitalPhotographRecord"`

2. In the **Results options** section, select the check box for **Records**.

You can also search on the following special fields:

|Special fields|Description|
|--------------|-----------|
|dod:scannedRecord|Search for all scanned records.|
|dod:pdfRecord|Search for all PDF records.|
|dod:webRecord|Search for all web page records.|

### Searching for empty strings

An example of searching for empty strings is to match all the empty Location fields.

1. In the **Search Text** box, enter:

    `location:””`

2. In the **Results options** section, select the check box for **Records (Completed only)** and deselect the other component options.

3. Click **Search**.

The Results tab shows the completed records that have empty Location fields.

### Searching for components

In the **Results options** section, the Components area allows you to select the type of components to search. You can search for Records, Record Folders, and Record Categories, as well as On Hold and {% include tooltip.html word="cutoff" text="Cut Off" %} records. For record searches, you can also search for incomplete records and vital records.

For example, to search for only vital records:

1. In the **Results options** section, select the check box for **Records (Completed Only)**.

2. Select the check box for **Vital Only**.

3. In the **Metadata** section, select the check box for **Vital Record**.

4. Click **Search**.

The Results tab shows the vital records (the Vital Record field has a value of Yes).

> **Note:** The vital records that are due for review will have the ![]({% link governance-services/images/rm-vr-dueforreview.png %}){:height="18px" width="18px"} icon next to Yes.

### Searching using special operators

Additional special operators can form rich search queries. The following special operations are available:

* `ISNULL:"<field>"` matches a field that has not been set to any value
* `ISNOTNULL:"<field>"` matches a field that contains any value

For example:

1. To return all records where the Description metadata field has not been set to any value, type:

    `ISNULL:"cm:description"`

2. To return all records where the Subject metadata field has been set to any value:

    `ISNOTNULL:"cm:title"`

---
title: Security Marks and Classification
---

You can add security controls to files, records, folders, and {% include tooltip.html word="category" text="categories" %} so that only users with the required security 
level can view or access them.

> **Note:** When you install **Enterprise** the Security Controls features are installed at the same time.

Security controls is the collective term for security classifications and security groups, which in turn are made up of 
one or more security marks.

There is one predefined **Classification** security group, but you can add as many additional security groups as you need.

Files, records, folders, and categories can be classified using the **Classify** option to apply a 
security classification and security marks.

You can set up classification guides so that users can auto-classify content.

When an item is classified it can only be seen by those with the required security clearance, and the security classification 
level is shown on screen. Users without the necessary security clearance won't have access to it or even know that it's there. 
When a classified file is {% include tooltip.html word="declareasrecord" text="declared" %} as a record it retains its 
classification level and security marks.
                           
User security clearance is set for a user (or user group) by assigning security marks to them.

You can create **Classification Reasons** to help identify and align the reasons why content is classified. 
Governance Services comes pre-configured with some common classification reasons but you can edit, delete, and make your own.

> **Tip:** Security controls are configured and assigned through the standard Alfresco Admin Tools, and can be used completely independently of a records management site if required.

## Classification life cycle

If you have the required security clearance and file permissions can classify and reclassify files, records, folders, and categories.

1. An Alfresco Administrator can create security controls. Go to **Admin Tools** > **Security Controls** > **Configure** > **Security Marks**.

   ![Create security groups]({% link governance-services/images/rm-security-groups.png %})

2. An Alfresco Administrator assigns security clearance levels to a user. Go to **Admin Tools** > **Security Controls** > **Configure** > **Assign**.

   ![Set security clearance]({% link governance-services/images/rm-classification-clearance.png %})

3. You are given the file permissions needed to edit [files]({% link content-services/latest/using/permissions.md %})/[records]({% link governance-services/latest/admin/index.md %}#adding-users-and-groups-to-a-role).

   ![Set site role]({% link governance-services/images/rm-classification-role.png %})

4. Select to classify a file, record, folder, or category.

   ![Classify option]({% link governance-services/images/rm-classification-classify.png %})

5. Selects security classification and/or security marks.

   ![Classify file]({% link governance-services/images/rm-classify-file.png %})

6. The classified item is only seen by those with the required security clearance.

   ![Classification label]({% link governance-services/images/rm-classification-label.png %})

7. You can reclassify the item as required, following the Downgrade Schedule or Declassification Schedule where appropriate.

   ![Edit classification]({% link governance-services/images/rm-classification-edit.png %})

## How security controls work

Both the predefined Classification security group and any custom security groups function in largely the same way, 
with a few important differences.

In both cases you can apply security marks to both records, folders, and categories in a Records Management site, 
and files and folders in a standard Alfresco site. These same marks are applied to users to set their security clearance levels.

When you {% include tooltip.html word="classify" text="classify" %} a file or record using their **Classify** option, the Classify Content screen is split into two sections. 
The top part is for setting classification and the bottom part for applying additional security marks. 
You can apply both classification and additional security marks to files (or records) at the same time.

> **Note:** Standard [Alfresco permissions]({% link content-services/latest/using/permissions.md %}) and [Records Management permissions]({% link governance-services/latest/using/manage-permissions.md %}) continue to apply as well as any additional classifications.

### Classification security group

There are four classification levels you can [apply to files and records](#classifyrecordsfolderscategories):

* **Top Secret**
* **Secret**
* **Confidential**
* **Unclassified** (typically used to differentiate a file or record that used to be classified, or will become so in future)

There are three clearance levels that can be [assigned to users](#setting-security-clearance):

* **Top Secret** - Can see files and records with any classification level
* **Secret** - Can see secret, confidential and unclassified files and records
* **Confidential** - Can see confidential and unclassified files and records

> **Note:** The default Alfresco Administrator has Top Secret clearance. All other users have No Clearance until their clearance is changed.

You can't classify a file higher than your own security level. So if your security clearance is Confidential, 
you can't classify a file as Top Secret.

Security clearance levels are enforced for files and records that have been classified. For example, 
if a record has been classified as Top Secret, then:

* User 1 (Top Secret clearance) - can see and work with the record
* User 2 (Confidential clearance) - doesn't see the record in the {% include tooltip.html word="fileplan" text="File Plan" %}

User 1 would see the following, whereas User 2 would only see the Unclassified file that has no classification label:

![Classified files]({% link governance-services/images/rm-classified-files.png %})

When you set security classification for a file or record you must record a reason for the classification. 
Downgrade and declassification schedule option give additional control over the classification lifecycle.

### Custom security groups

You can create an unlimited number of security groups, which in turn can contain an unlimited number of security marks. 
The marks are then [applied to files and records](#classifyrecordsfolderscategories) and [assigned to users](#setting-security-clearance).

When you create a new security group there are three Group Types available:

* **All**= Users must have all security marks from the group that are applied to a file to see that file.

    Example: A Security Group named Training contains security marks of Media and Data Handling. To see a file marked as both Media or Data Handling, then a user must have both Media and Data Handling clearance.

* **Any** = Users must have at least one of the security marks from the group that are applied to a file to see that file.

    Example: A Security Group named Nationality contains security marks of UK, US, and Aus. To see a file marked as UK and US, then a user must have UK and / or US clearance.

* **Hierarchical** = Security marks are ranked in the order they're created. The mark created first in a security group has the greatest clearance, the one created last the least clearance.

    Example: The predefined Classification group has marks of Top Secret, Secret, and Classified. To see a file classified as Secret, then the user must have Secret or Top Secret clearance.

Using the above examples, if a record has been classified as Media, Data Handling, US, and UK, then:

* User 1 (Media, Data Handling, and UK) - can see and work with the record
* User 2 (Media and UK) - doesn't see the record in the File Plan

> **Note:** Files and records aren't visibly labelled with custom security marks in the same way as they are with security classification marks.

## How security clearance works

Security clearance is the assignment of security marks to users.

Once marks are applied to content then users can only see that content if they have the required security clearance.

> **Note:** Standard [Alfresco permissions]({% link content-services/latest/using/permissions.md %}) and [Records Management permissions]({% link governance-services/latest/using/manage-permissions.md %}) continue to apply as well as any security clearance.

When security groups are created there are three different Group Types available, and each one controls how the user sees content, see [How security controls work](#how-security-controls-work).

Users with Alfresco Administrator permissions can [set and edit the security clearance of users and user groups](#setting-security-clearance).

When assigning marks to users or user groups, marks that are inherited from another group aren't shown. Only marks that are assigned directly to this user / group are displayed. If a user (or group) has inherited security marks from a group, then these are added to their directly assigned marks.

**Hierarchy based security clearance**

For hierarchy based security groups such as the prefined Classification group, a user who is assigned one mark and inherits another has the clearance of the higher of the two. For example, a user who has Confidential clearance directly assigned, and has inherited Top Secret clearance from a group, will have Top Secret Clearance.

**Non-hierarchy based security clearance**

For non-hierarchy based security groups the security marks are added together, so that a user who is directly assigned the UK mark, and inherits the US mark from a group, will have clearance for both UK and US marked files.

## How classification guides work

You'll usually have a number of common classification requirements for different types of content. 
For example, all staff records may require the same security levels to access them.

Instead of setting these individually, you can [create classification guides](#creating-classification-guides) to use as 
templates for {% include tooltip.html word="classify" text="classifying" %} content quickly and accurately.

You can create as many classification guides as you want and make them as complex or as simple as you need.

Each guide is made up of one or more topics. A topic can contain further subtopics, or a set of instructions. 
If you select to add instructions you can choose security classification, including a classification agency and 
reasons and downgrade and declassification schedules, as well as any additional security marks that are set up.

You can choose to make a guide available for use in classification by setting it to **On**, or to leave it **Off** 
until you're ready for it to be used.

When people are [classifying content](#classifyrecordsfolderscategories) they can select to **Add Instructions** and 
browse through the classification guides to find the instructions they want. When the instructions are applied 
to content then all the security classifications and controls the instructions contain are automatically applied to that content.

**Example**

The following example shows a classification guide for Staff Records. This guide contains a topic named Medical Records 
which has has instructions to include the US and Senior Manager security marks.

If a file was classified using these instructions then it would only be visible to users who have security clearance 
for US and Senior Manager levels.

![Classified files]({% link governance-services/images/classification-guide-example.png %})

## Creating a security group

Each security group is made up of one or more security marks.

These marks can then be assigned to users and content to control which users can see which content.

For example, the predefined security group is Classification and contains the marks Top Secret, Secret, and Confidential. 
Only users assigned to the Top Secret mark can see files that have been marked as Top Secret. 
This works in the same way for any additional security groups that you set up.

You can set up additional security groups to match your company requirements, for example, security groups for 
nationality and job role.

1. Click **Admin Tools** and then click **Security Controls > Configure**.

2. Click **Create Security Group**.

3. Enter a name for the security group.

4. Select a Group Type for how security clearance will be applied for this group:

    * **All**= Users must have all security marks from the group that are applied to a file to see that file.

        Example: A Security Group named Training contains security marks of Media and Data Handling. To see a file marked as both Media or Data Handling, then a user must have both Media and Data Handling clearance.

    * **Any** = Users must have at least one of the security marks from the group that are applied to a file to see that file.

        Example: A Security Group named Nationality contains security marks of UK, US, and Aus. To see a file classified as UK and US, then a user must have UK and / or US clearance.

    * **Hierarchical** = Security marks are ranked in the order they're created. The mark created first in a security group has the greatest clearance, the one created last the least clearance.

        Example: The predefined Classification group has marks of Top Secret, Secret, and Classified. To see a file classified as Secret, then the user must have Secret or Top Secret clearance.

5. Click **Create**.

    Once you've created a security group you can:

    * Click on the group to [add security marks to it](#adding-security-marks-to-a-security-group)
    * Click ![Edit group]({% link governance-services/images/ico-configure.png %}){:height="18px" width="18px"} to edit the group name.
    * Click ![Delete group]({% link governance-services/images/ico-trashcan.png %}){:height="18px" width="18px"} to delete the group. You can't delete a group or its marks if it contains marks that are assigned to content.

        > **Note:** No-one else can access a security group until you add security marks to it.

        Once marks are added to the group, only users who have been assigned one of the marks can see the group.

## Adding security marks to a security group

You can add multiple security marks to a security group.

These marks can then be assigned to users and content to control which users can see which content.

For example, the predefined security group is Classification and contains the marks Top Secret, Secret, and Confidential. 
Only users assigned to the Top Secret mark can see files that have been marked as Top Secret.

You can set up additional security groups to match your company requirements, for example, security groups for 
nationality and job role.

1. Click **Admin Tools** and then click **Security Controls > Configure**.

2. Click on a security group.

    > **Tip:** You can't add security marks to the predefined Classification security group.

3. Enter a name for a new security mark.

    You can use the same names for marks in different security groups, but within a security group each name must be unique.

4. Click **Create**.

5. Now repeat until you have added all the security marks you want to (you can always add more later).

    > **Note:** You can always click ![Delete]({% link governance-services/images/ico-delete.png %}){:height="18px" width="18px"} to delete a security mark from the group. You can't delete a mark that's been assigned to a file. If you delete the last mark from a group then no-one else can access the group until you add marks to it.

## Setting security clearance

Alfresco Administrators can assign different clearance levels to users and groups that give access to files and 
records within their clearance level.

> **Note:** You need to have the Alfresco Administrator role to set security clearance. You can't change the clearance level of the default Alfresco Administrator.

1. Click **Admin Tools** and then click **Security Controls > Assign**.

    Users and groups are shown with their current classification clearance (the predefined security group).

    * **Top Secret** - Can see all files and records with any classification level
    * **Secret** - Can see secret, confidential, and unclassified files and records
    * **Confidential** - Can see confidential, and unclassified files and records
    * **No Clearance** - Can see unclassified files and records
    
    Hover over **Details** to see all security groups and security marks assigned to a user.

    > **Note:** You won't see marks assigned to a user if you don't have clearance for them.

2. Type a user's name or group name into the filter box to find the user / group.

    > **Tip:** You can sort users by clicking **Name**, and view a user profile by clicking a user name.

    Click to select to view Groups and Users, or just Users or Groups.

3. Hover over a user or group and click **Set Security Controls** next to them to change the security groups and marks they're assigned.

    > **Note:** You can only assign Security Marks for the groups you are a part of.

4. Currently assigned security marks are highlighted. Click a security mark to assign it to the user / group, and again to unassign it.

    > **Note:** Marks that are inherited from another group aren't shown, only marks that are assigned directly to this user / group.

5. Click **Apply**, and any changes you've made are applied.

    > **Note:** If a user has marks assigned that you don't have access to then these will be unaffected by any changes you make.

## Creating classification guides

Classification guides can be used to quickly {% include tooltip.html word="classify" text="classify" %} content with a preset collection of security controls.

You can create an unlimited number of guides, and each one can contain one or more topics. 
Topics can then contain either subtopics or instructions.

Instructions are a collection of security marks and classification details. When you classify content with a topic 
(or topics) it's classification details are populated with those in the topic.

You can build up guides and they won't be available for use until you set them to **On**. 
Find out more in [How classification guides work](#how-classification-guides-work).

1. Click **Admin Tools** and then click **Security Controls > Classification Guides**.

2. Click **New Guide**.

3. Enter a name for the guide.

4. Enter an Originating Organization, for example, government or other body.

5. Enter a guide {% include tooltip.html word="publicationdate" text="publication date" %}. This is the date when the guide should be made available.

6. Select whether to make the guide available for classifying content.

    If it's not yet ready then you can leave it Off and switch in On at a later stage.

7. Click **Save**.

    The guide is now listed and you can now add topics to it.

8. Click on the guide name then click **New Topic**.

    > **Tip:** You can click on a guide (not the guide name) then click ![Edit group]({% link governance-services/images/ico-configure.png %}){:height="18px" width="18px"} to edit the guide, or ![Delete group]({% link governance-services/images/ico-trashcan.png %}){:height="18px" width="18px"} to delete it.

9. Enter a name and optional description for the topic.

    You can now click **Save** and add sub-topics, or select instructions to add to a topic.

10. To add instructions click on **Security Classifications** and/or **Security Groups**:

    * **Security Classifications** - Select a classification level, a classification reason, and any other required classification details
    * **Security Groups** - Select all the required security marks

        > **Note:** You cannot use security marks you do not posses when classifying content, unless you also use a security mark you do posses from the same group. If you have a security mark from a security group 'any' then you can view and assign all other marks from that group. When using marks (either when Classifying Content or creating Instructions) that you don't posses, you must include a mark from the same group to avoid losing access to the content. An error will appear if you attempt to create an instruction using only a mark you don't have, or have not included a mark from the same group.

11. Click **Save**.

    If the guide is switched **On** then users can select from the topics it contains to automatically classify content.

    > **Note:** If you delete a guide containing instructions that are currently being used to classify content, then the content will retain its classification.

    If you edit a guide's instructions then that won't modify the classification level or marks applied to content previously classified using that instruction.

## Classifying records, record folders, and record categories {#classifyrecordsfolderscategories}

You can {% include tooltip.html word="classify" text="classify" %} records, record folders, and record {% include tooltip.html word="category" text="categories" %} and apply security marks so that they can only be 
viewed or accessed by users who have the required security clearance.

There are four security classification levels that you can assign. Security groups provide additional classification options.

> **Note:** You can also [classify files]({% link governance-services/latest/using/easy-access-records.md %}#classifying-files-and-folders) in Alfresco sites.

See [Classification rules and tips](#classification-rules-and-tips) for more on classifying content.

You can autoclassify by adding instructions, manually apply classifications and security marks, or both.

1. In the File Plan hover over a record, folder, or category and select **More**, then **Classify**.

    You can classify using both **Security Classification** and **Security Groups**. You'll only see the classification options that you have security clearance for.

2. **To autoclassify:**

3. Click **Add Instructions**.

4. Click on a guide to view its topics.

5. Click ![Add instructions]({% link governance-services/images/ico-instructions-action.png %}){:height="18px" width="18px"} next to the topic you want to apply instructions from then click **Select**.

    > **Tip:** You can click **View** to check what classification level and security marks the topic instructions contain.

6. Repeat for as many topics as you want to add.

7. Click **Apply**.

    All the topics you've selected will have their instructions applied to the item you're classifying.

    > **Tip:** If topics contain instructions that clash then the higher level of classification will apply. For example if you add two topics, one with a classification level of Top Secret, and one with Secret, then the Top Secret level will apply.

8. **To add Other Classification Source References**

    > **Note:** This step is not required to classify an item.

9. Enter the name of the source document from which the classification of the item has been derived.

10. Enter the name of the organization that produced the document.

11. Enter the {% include tooltip.html word="publicationdate" text="publication date" %} of the document.

12. **To manually add classifications and security marks:**

13. If you want to classify a folder and its contents, select **Apply Classification to Folder Contents**.

    This option is only visible when classifying a folder. Only the top level folder and its immediate children are classified and only the metadata of the parent is carried over to the children. If a new child object is added at a later date it does not inherit the properties of its parent.

14. Select a classification from:

    * **Top Secret**
    * **Secret**
    * **Confidential**
    * **Unclassified**
    
    > **Tip:** If you select **Unclassified** then the item will be available to all users.

15. Enter a classification agency, for example, government or other body (optional).

16. Select one or more classification reasons from the list of available reasons.

17. You can optionally set a **Downgrade Schedule** or a **Declassification Schedule**.

    **Downgrade Schedule**

    Set a schedule for when the item will be downgraded, for example, from Top Secret to Secret. You can enter a specific date for the downgrade to take place, an event that means a downgrade should be considered, and instructions on how to carry out the downgrade. All of these are optional, but once you've entered a downgrade date, event, or both, you're required to enter instructions.

    **Declassification Schedule**

    Set a schedule for when the item will be declassified. This means when its classification level will be set to Unclassified. You can enter a specific date for the declassification to take place, an event that means declassification should be considered, and exemptions for when declassification shouldn't take place. All of these are optional.

    > **Note:** Downgrade and declassification schedules are not automated. Any reclassification needs to be done manually.

18. Click security marks to apply them to the item, and again to remove them.

    See [How security controls work](#how-security-controls-work) for more details.

19. Click **Classify**.

    The item now displays its classification level, and can only be seen by those with the required security clearance.

    > **Tip:** Items set to Unclassified with no applied security marks can be seen by all users.

    The classification reason and classification-related properties can be seen in the **Properties** when you preview the item.

### Classification Reasons

Once configured Classification Reasons are used because they provide you with information relevant to your 
organization about why an item is being classified.

1. Go to > **Admin Tools** > **Security Controls** > **Configure** and then the **Classification Reasons** tab.

2. Enter a **Reason Code** and a **Description** for the new **Classification Reason** and click the **Add** icon.

    Use the other icons to **Delete** and **Edit** the other **Classification Reasons**.

### Classification rules and tips

When you classify content there are a few rules that help you maintain secure classification.

**Security clearance and permissions**

If a user doesn't have the required security clearance, then they won't be able to see record, folders, or categories 
that have been classified. For example, if a record has been classified as Top Secret, then:

* User 1 (Top Secret clearance) - can see and work with the record, following the usual [Alfresco permission rules]({% link content-services/latest/using/permissions.md %}).
* User 2 (Confidential clearance) - doesn't see the record.

To classify records, folders, or categories:

* You must have permissions to edit them. This means having a Read and File permission on them.
* You must have been given a security clearance higher than No Clearance (unless the item is set as Unclassified).

You also can't classify items higher than your own security level. So if your classification clearance is Confidential, you can't classify a record as Top Secret.

CAUTION:

Users with Admin permissions can classify repository top level folders such as the Data Dictionary and Sites. It's recommended to *not* do this to avoid potential issues for other users.

**Classifying folders and categories**

When you classify folders and categories, there may be restrictions on the levels you can set if they contain content that has already been classified. As such you might want to consider classifying folders and categories before you classify their content. The rules are:

* Items can't be classified higher than the folder or category they are in (not applicable if the folder or category hasn't been classsified).
* A folder or category can't be classified lower than any items it contains.
* Classified items can't be moved, copied, or linked to folder or categories lower than their classification.

## Declassification

An item can be declassified when it is no longer considered to be classified. Declassification occurs after a period 
of time has elapsed or an event occurs.

Go to **Admin Tools > Security Controls > Configure** to review the following declassification settings.

Governance Services comes configured with some common **Declassification Exemptions** but you can edit, delete, 
and create your own. You use these when you want to record the reasoning why the declassification time frame isn't being followed. 
Typically this occurs when you want to extend the Declassification Time Frame for some of your items in the repository.

You can also configure the **Declassification Time Frame** which determines how long by default, 
items in the repository are classified for until they are eligible for declassification. 
You have the option to adjust the Declassification Time Frame for new files or for all files in the repository. 
If there is an exemption attached to an item in the repository, its declassification time frame wont change if you 
change the settings on the Declassification Time Frame page.

> **Note:** When using the feature ensure you read the information messages that are offered before you make any changes.

### Declassification Exemptions

Declassification Exemptions are used when classifying content to indicate why the default Declassification 
Time Frame should not be applied.

1. Go to > **Admin Tools** > **Security Controls** > **Configure** > **Declassification Exemptions**tab.

2. Enter an **Exemption Code** and a **Description** for the new **Declassification Exemption** and click the **Add** icon.

    Use the other icons to **Delete** and **Edit** the other Declassification Exemptions.

### Change Declassification Time Frame

The Declassification Time Frame screen is where you set the declassification period your system will use 
when declassifying items in Governance Services.

1. Go to **Admin Tools** > **Security Controls** > **Configure** > **Declassification Time Frame tab**.

    The **Calendar Icon** displays the current **Declassification Time Frame**.

2. Select a new Declassification Time Frame from the drop down list and click **Save**.

3. Click **Apply to Existing Items** if you want to change the Declassification Time Frame of items already in Governance Services.

    This process may take some time to complete.

## Reclassifying content

You can edit classification details and change the assigned security marks, as well as reclassifying content to downgrade, 
upgrade, and declassify it.

When a file, record, folder, or {% include tooltip.html word="category" text="category" %} is originally classified, a downgrade or declassification schedule can be set up. 
It's recommended that you follow this schedule when reclassifying.

You also can't reclassify a content higher than your own security level. So if your security clearance is Confidential, 
you can't reclassify content as Top Secret.

See [Classification rules and tips](#classification-rules-and-tips) for more on classifying content.

> **Note:** Content can be reclassified multiple times.

1. Hover over a classified file, record, folder, or category and select **More**, then **Edit Classification**.

2. Autoclassify by clicking **Add Instructions**, or edit the classification manually using the steps below.

3. Select a classification from:

    * **Top Secret**
    * **Secret**
    * **Confidential**
    * **Unclassified**
    
    > **Tip:** If you select unclassified then the content will be available to all users. The classification reason can be seen in its properties when you preview files and records or view the details of folders and categories.

4. You can edit most fields without choosing a new classification. If you select a new classification then you need to state who is doing the reclassification and the reason for doing it.

    > **Note:** If the content has previously been reclassified then the person who classified it and their reason are displayed. You can edit these if required.

5. Update other **Security Classification** details as required.

6. Click security marks to apply them to the content, and again to remove them.

    See [How security controls work](#how-security-controls-work) for more details.

7. Click **Save**.

    The content now displays its classification level, and can only be seen by those with the required security clearance.

    > **Tip:** Content set to Unclassified with no applied security marks can be seen by all users.

    > **Note:** The option to **Share** a file (not applicable for records) is no longer available for Top Secret, Secret, or Confidential files. When a file is declared as a record it retains its classification level and any security marks.

    The classification reason and classification-related properties can be seen in its properties when you preview files and records or view the details of folders and categories.
---
title: The File Plan
---

The File Plan is a container for records, folders, {% include tooltip.html word="category" text="categories" %} and retention schedules. It's effectively a virtual filing cabinet 
for storing records, and is the basic structure of Records Management. This structure lets you classify and group records with similar 
characteristics.

The top level of the File Plan is created when you create a Records Management site. This is like an empty 
virtual filing cabinet - you then add drawers (categories), folders, and records to it.

![File Plan]({% link governance-services/images/file-plan.png %}){:height="400px" width="150px"}

Remember that it's far more versatile than a physical filing cabinet, but the following rules are enforced when working 
with the File Plan structure:

* The top level of the File Plan can only contain record categories.
* A category can contain other categories and folders.
* A folder can contain only records.

The structure of the File Plan will generally reflect different parts of your organization and can be made up of the following elements:

* **Record category**

    The record category contains the retention and retention schedules for its folders and records. In other words it controls how records are managed, and how they're disposed of when they're not needed any more.

* **Record folder**

    A record folder is created in a record category, and inherits the attributes of the record category. The record folder is considered to be under the control of the record category. Once the record folder is created, security restrictions apply. A record folder can be open or {% include tooltip.html word="recordfolderclosed" text="closed" %}, and a closed record folder cannot accept records for filing.

* **Record**

    A record is a document in the File Plan. It's filed in a record folder, and is under the control of a record category.

* **Vital record**

    A vital record is a record that is considered to be essential to the operation of an organization. A vital record must be reviewed periodically, according to its review period. The review period is attached to the record category or folder.


You can create a File Plan structure from scratch or [load the Records Management test data](#loading-test-data) to use as a starting point. This gives you a sample File Plan that you can rework to meet your needs.

You can also automate the File Plan by [applying rules to categories and folders]({% link governance-services/latest/using/automate-fileplan.md %}). This means that records can be moved automatically through the record lifecycle, without you having to do any of the work.

## Opening the File Plan 

You can use the File Plan to manage, view, and work with records.

1. Click **File Plan** in the Records Management site.

    The records list takes up most of the File Plan main page. You can filter the records list and navigate the File Plan using the explorer panel down the left side of the page.

2. Use the **Options** menu to select how you want to view the library content, and the sorting options to sort records.


> **Note:** It's recommended that you use the File Plan for Records Management actions rather than going through the repository.

## Browsing the File Plan

The File Plan consists of an explorer panel and a content list.

The explorer panel has the following sections:

* **Navigation**

    A tree view of the records management hierarchy. The ![]({% link governance-services/images/Subfolders.png %}){:height="18px" width="18px"} icon indicates a category contains subfolders. Click the icon to view its contents.

* **File Plan**

    A list of transition types that records can be in. You can click these to view all matching records.

* **Saved Searches**

    A list of the saved searches. You can click these to view all matching records.


The location path above the content list shows your current position in the File Plan hierarchy. Each location path item is a link so you can easily return to any part of the current navigation path. Click ![Navigate Up]({% link governance-services/images/navigate-up-icon.png %}){:height="18px" width="18px"} to display the contents of the folder one level higher.

Use the sort menu to change the criteria used to sort the File Plan contents. You can toggle between ascending and descending sort order.


## Building the File Plan

The File Plan is built up by adding levels made up of {% include tooltip.html word="category" text="categories" %} and folders.

Only a few users have the capability to add folders and categories, and this is tightly controlled to make sure that your system remains compliant. Capabilities are assigned to user roles in the RM Admin Tools. You might be assigned the capability to create folders but not categories, or just have the capability to add records.

> **Note:** Capabilities given to a role are not the same as permissions. Capabilities define what you can do in the Records Management site, whereas permissions are specific to sections of the File Plan. Permissions are applied at category and folder level using the **Manage Permissions** option, and you use these to decide which users can see specific sections of the File Plan, and if they can read and file in that section. See [Managing permissions]({% link governance-services/latest/using/manage-permissions.md %}) for further details.

When you create a container (category or folder) the system records the date of creation and the user who created it. This information is recorded in the object's metadata. Metadata can be thought of as a set of properties, and are where all key information about an item, folder, or category is stored. Record categories carry the most metadata as they hold the retention instructions for the whole category.

The following rules are enforced when working with the File Plan structure:

* The top level of the File Plan can only contain record categories.
* A category can contain other categories and folders.
* A folder can contain only records.

### Loading test data

You can load Records Management test data which creates a sample File Plan that you can use to get started.

> **Note:** The test data is intended to give you an idea how a File Plan is structured. You don't need to load it if you don't want to.

1. Click ![]({% link governance-services/images/settings-icon.png %}){:height="18px" width="18px"} then **Customize Dashboard**.

    The Customize Dashboard page displays the current layout and configuration of your dashboard.

2. Click **Add Dashlets** and drag and drop the RM Data Set Import dashlet onto the columns below:

3. Click **OK** to save the dashboard configuration.

    The Import Data Set dashlet is added to the site dashboard.

4. Select **DOD 5015 Example Data** from the Data Set menu on the new dashlet and click **Import**.

    A sample File Plan and associated data is imported to your Returns Management site. You can explore and edit the File Plan as you would with a plan you created from scratch.

### Adding a record category

You can create a record {% include tooltip.html word="category" text="category" %} at the top level in the {% include tooltip.html word="fileplan" text="File Plan" %} or within another record category.

1. In the File Plan go to the location for the new record category.

2. Click **New Category**.

    The **New Record Category** dialog box displays.

3. Enter details for the new category. 

    |Metadata field|Description|
    |--------------|-----------|
    |Name|*Required.* The name for the record category.|
    |Title|*Required.* The title for the record category.|
    |Description|A description of the record category.|
    |Record Category ID|*Required.* A unique identifier for the record category is generated automatically. You can change this now, but you can't edit it once the category has been created.|
    |Vital Record Indicator|Defines whether records in this category have a review process. The Vital Record Indicator is applied to all record folders within that category. You can change this at folder level. <br><br>Users with Records Manager permissions receive a notification email when vital records are due for review.|
    |Period|The time period for the review cycle. Reviews are recurring based on the period you select. The review period is required when the **Vital Record Indicator** option is selected. The review period is displayed on the details page for folders and records in the category. <br><br> **Note:** The "Quarter" option splits the year into 4 sets of 3 months, beginning with Jan/Feb/March. "Financial Quarter" is the same but based on the start date of your system-configured financial year.|
    |Expression|Enter a number as the **Expression** to accompany the **Period** type. If you enter “Week” and “3”, this would mean a review cycle of 3 weeks. <br><br>If you select a Period that doesn't require an Expression then this field isn't available.|

4. Click **Save**.

    The new category displays in the File Plan.

See also video explaining [adding a record category]({% link governance-services/latest/tutorial/governance-services/index.md %}#create-a-record-category).

### Adding a record folder

You can add record folders within a record {% include tooltip.html word="category" text="category" %}.

1. Select a folder in the {% include tooltip.html word="fileplan" text="File Plan" %}.

2. Click **New Folder**.

    The **New Record Folder** dialog box displays.

3. Enter details for the new category. 

    |Metadata field|Description|
    |------------------|---------------|
    |Name|*Required*. The name for the record folder.|
    |Title|*Required*. The title for the record folder.|
    |Description|A description of the record folder.|
    |Record Folder ID|*Required*. A unique identifier for the record folder is generated automatically. You can change this now, but you can't edit it once the folder has been created.|
    |Location|If relevant specify the physical location of the records contained within this folder.|
    |Supplemental Marking List|If available, select any suitable properties from the list. Entries on this list are set up by your Alfresco administrator and are only available if you have been given the required permission.|
    |Vital Record Indicator|Defines whether records in this folder have a review process. The Vital Record Indicator is applied to all records within the folder. You can change this at record level.<br><br> **Note:** If you don't select this option and the category the folder is in has a Vital Record Indicator set, then the category setting will be applied to the folder once it is created.<br><br>If you do select this option it will override any Vital Record Indicator set in the category.<br><br>Users with Records Manager permissions receive a notification email when vital records are due for review.|
    |Period|The time period for the review cycle. Reviews are recurring based on the period you select. The Review Period is required when the **Vital Record Indicator** check box is selected.<br><br> **Note:** The "Quarter" option splits the year into 4 sets of 3 months, beginning with Jan/Feb/March. "Financial Quarter" is the same but based on the start date of your system-configured financial year. See [Customizing the end of the financial year]({% link governance-services/latest/config/index.md %}#customize-end-of-year).<br><br>The review period is displayed on the details page for records in the folder.|
    |Expression|Enter a number as the **Expression** to accompany the **Period** type. If you enter “Week” and “3”, this would mean a review cycle of 3 weeks.<br><br>If you select a Period that doesn't require an Expression then this field isn't available.|

4. Click **Save**.

    The new folder is now shown in the File Plan.

The new record folder is marked as ![]({% link governance-services/images/ico-rm-folder-open.png %}){:height="18px" width="18px"} Open, which means that records can be filed in it. The date of opening is the same as the creation date.

See also video explaining [adding a record folder]({% link governance-services/latest/tutorial/governance-services/index.md %}#create-a-record-folder).  ---
title: Working with Amazon S3 WORM
---

You can use the Amazon S3 WORM storage by creating a Rule and an Action in Governance Services.

WORM storage (Object Lock in Amazon S3) is an Amazon S3 capability that allows you to store objects using the write once, 
read many (WORM) model. Records moved to WORM storage use an Amazon S3 bucket that is configured to support object locking 
in compliance mode. The movement of records is controlled through record folder rules and actions. You use the WORM model 
where it is a requirement that your data is not changed once it has been written to disk. This may be a requirement of 
yours due to regulatory compliance in the governmental, financial or healthcare sectors.

The movement of records to WORM storage and through to disposition can be fully automated. A folder rule is configured 
to test records for the classification that requires WORM storage. This may be based on when a records enters a folder 
or complex meta data conditions. When triggered the rule causes the Object Lock action to be initiated in Amazon S3. 
This action is configured with the required WORM retention period in days. For records that are moved to WORM locked 
storage any retention schedules that may have been applied are interrupted. At the end of the required retention period 
in WORM storage the records are automatically returned to the original default S3 bucket to allow normal record operations 
to re-commence, including the application of retention schedules and disposition.

While retained in WORM storage additional controls are applied to prevent any user including administrators from deleting 
the records. Adding records to one or more legal holds during the WORM storage retention period causes the Amazon S3 legal 
hold flag to be set on the record in Amazon S3. This prevents deletion or editing of the record in Amazon S3 even if the 
WORM retention period has expired. Once the record has been removed from all legal holds it was added to the legal hold 
flag is cleared and the record can be removed from the WORM bucket once the retention period has expired.

There is some configuration required before you can use this feature, for more see 
[Creating a bucket in Amazon S3 for use as WORM storage](#createbucketforworm).

Once you have created the bucket in Amazon S3 for use as Worm storage you can use it as storage, for more see 
[Using WORM storage](#usingworm).

Although the content of a WORM-locked record will be protected against modifications, any copies of WORM-locked records 
in other record folders will be stored using the rules for that folder. Consequently, copies of records may not be protected 
by the same restrictions.

You are unable to reject a Record that is stored in WORM storage and you can't move Records that are stored in WORM storage.

## Creating a bucket in Amazon S3 for use as WORM storage {#createbucketforworm}

These steps describe how to use the AWS Management Console to create a bucket for use as WORM storage 
(Amazon S3 Object Lock) in Amazon S3. Once you have created the bucket you can create rules for a category or folder to 
store your data using WORM storage.

For more on creating rules see [Creating a rule]({% link governance-services/latest/using/automate-fileplan.md %}#creating-a-rule).

> **Note:** Ensure you have the required AWS login credentials before you begin.

This task assumes you have:

* Installed Alfresco Content Services 7.0 and above.
  * For more see [Supported platforms]({% link governance-services/latest/support/index.md %}).
* Installed Alfresco Content Connector for AWS S3 3.1 and above with multiple bucket support enabled.
  * For more see [Configuring multiple buckets using S3 Connector]({% link aws-s3/latest/config/index.md %}#multibucketconfig).
* Set the following properties in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file:

    |Property| Description                                                                                                                                                                                                                 |
    |--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    |worm.contentstore| *ACS 23.2, S3 Connector 6.1.0 and above.* This property is the key of the content store that has a WORM bucket.                                                                                                              |
    |worm.retentionPeriod| *ACS 23.2, S3 Connector 6.1.0 and above.* This property controls the default retention period. It is specified in days and the default value is 2192 which is six years.                                                     |
    |s3.worm.contentstore| *ACS versions older than 23.2, S3 Connector versions older than 6.1.0.* This property is the key of the content store that has a WORM bucket.                                                                                                  |
    |s3.worm.retentionPeriod| *ACS versions older than 23.2, S3 Connector versions older than 6.1.0.* This property controls the default retention period. It is specified in days and the default value is `2192` which is six years.                                                                        |
    |connector.s3.store2.retentionPeriodProperty| This property passes the AGS property which stores the unlock date of an object to Content Connector for AWS S3. You must enter this value: `{http://www.alfresco.org/model/recordsmanagemententerprise/1.0}wormUnlockDate`. |
    |rm.wormUnlockRecords.cronExpression| This cron expression is used to specify how often the unlock job should run in Governance Services. The default is 15 minutes.                                                                                              |

1. Log in to your AWS Management Console.

2. Expand **All services** and under the Storage heading select **S3**.

3. In the S3 buckets window, click **Create bucket**.

4. Enter a name for the Bucket and select the required Region and then click **Next**.

5. Under the Versioning heading, select **Keep all versions of an object in the same bucket** check box.

    To enable Object Lock you must select this check box.

6. Expand **Advanced Settings** and under the Object Lock heading select **Permanently allow objects in this bucket to be locked** and click **Next**.

    > **Note:** You must have Object Lock enabled in order to use Governance Services with WORM storage. For more on Object Lock see [S3 Object Lock overview](https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock-overview.html){:target="_blank"}.

7. Ensure **Block all public access** is selected and click **Next**.

8. Click **Create bucket**.

    You are now back at the S3 buckets window.

9. Select the check box next to the bucket you have just created and click **Properties**.

10. Under the Advanced settings heading click the **Object lock** tile.

11. Select `Compliance` or `Governance` retention mode as per your preferences (you may want to contant your Legal Department to define that).

12. Enter a Retention period in Days and click **Save**.

    This retention period must match the retention period you configured in the Alfresco Global Properties file for property `worm.retentionPeriod`/`s3.worm.retentionPeriod`.

    To use this bucket as WORM storage you must now create rules for a category or folder in Governance Services using the **WORM lock** action. If you use the REST API you can use the action without a rule.

## Using WORM storage {#usingworm}

These steps describe how to use WORM storage with Governance Services and how to use WORM storage when you specify a 
retention period and when you use Legal Hold.

This task assumes you have:

* Created a bucket in Amazon S3 for use as WORM storage.
  * For more see [Creating a bucket in Amazon S3 for use as WORM storage](#createbucketforworm).
* Familiarised yourself with how to create rules in Governance Services.
  * For more see [Creating a rule]({% link governance-services/latest/using/automate-fileplan.md %}#creating-a-rule).

1. Log in to Governance Services.

2. (Optional) Click **More** and then **Add to Hold** if you want to use a Legal Hold for your new rule.

3. (Con't Optional) Select the Hold you want to add the folders or categories to and click **OK**.

4. Click **More** and then **Manage Rules** for the folder or category you want to set rules for.

    > **Note:** If you have selected a Hold then you will need specific IAM permissions on your AWS account to delete the record after the WORM-lock has expired.

5. Click **Create Rules**.

6. Enter a name for the new rule.

7. Define the rule.

8. Select **WORM lock** from the **Perform Action** drop down list.

9. Enter a retention period. In days.

    If you don't enter a retention period the default period used is the one you set for this property `worm.retentionPeriod`/`s3.worm.retentionPeriod` in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file.

    > **Note:** When using the WORM Lock action you must select **Run in Background** when creating rules for your categories or folders.

10. Click **Create**.
