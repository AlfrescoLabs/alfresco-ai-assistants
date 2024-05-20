---
title: Alfresco Process Automation
---

Alfresco Process Automation (APA) is a low-code application development platform available as a service on Alfresco Cloud. It has been designed for organizations to quickly and easily create intelligent solutions that orchestrate and streamline from simple to complex content-centric business processes. It is meant to serve multiple business domains and its cloud-native architecture offers maximum availability and dynamic scaling.

It is composed of three main components: ​

* The Modeling Application, where professional developers and non-technical power users create, update, and release applications.

* The Admin Application, where administrators deploy applications, manage user permissions, and monitor deployed applications.

* The Digital Workspace, where end-users can start new content-centric processes, and manage their work.
---
title: Architecture
---

Process Automation provides a set of microservices and components that interact with Alfresco Cloud.

A high-level architectural diagram of Process Automation is:

![High level architectural diagram]({% link process-automation/images/arch-overview.png %})

## Modeling service

The modeling service is the backend service for the [Modeling Application]({% link process-automation/latest/model/index.md %}). It stores all project and model definitions into its own database that is then used by the [deployment service](#deployment-service) to deploy the projects. The database is deployed at the platform level and is independent of the databases used by applications.

The modeling service also contains a set of simulation services so that decision table and script functionality can be tested during the modeling experience.

![Modeling service diagram]({% link process-automation/images/arch-modeling.png %})

## Deployment service

The deployment service is used to create deployment descriptors and deploy released projects.

The deployment service reads released project data from the modeling service database, but stores information related to deployment descriptors and deployments in its own database. This database is deployed at the platform level and is independent of the databases used by applications. The deployment service is the backend service for the [Admin Application]({% link process-automation/latest/admin/index.md %}).

![Deployment service diagram]({% link process-automation/images/arch-deployment.png %})

Once a payload has been submitted to the deployment service through the API or using the Administrator Application a sequence of events happen:

* The first thing is validation to ensure the payload contains no errors and that there are no conflicts with any other application names already deployed into the cluster.

* Once validation has passed a series of data enrichment is applied to the payload specifying default values.

* After data enrichment is complete the payload is saved to the deployment service database as a descriptor.

* The final stage to deploy uses the Kubernetes API to deploy the images into their own namespace. This also includes a persistent volume that is mounted in the new namespace.

    > **Note**: Each application is deployed into its own namespace.

## Identity Service

The [Identity Service]({% link identity-service/latest/index.md %}) is used for authentication throughout the Process Automation environment.

## Application runtime bundle

The application runtime bundle is a set of services that manage models at runtime. The service is deployed for each application and stores data in a database used solely for that application.

![Application runtime bundle diagram]({% link process-automation/images/arch-runtime.png %})

### Process runtime

The process runtime is an instance of the process engine that executes the process definitions. A synchronous REST API and an asynchronous message-based API are exposed by the process engine and [events]({% link process-automation/latest/model/processes/events.md %}) are emitted and consumed via Spring Cloud Streams.

### Form runtime

The form runtime contains the functionality required for [forms]({% link process-automation/latest/model/forms.md %}) at runtime.

### DMN runtime

The DMN runtime contains the functionality required for [decision tables]({% link process-automation/latest/model/decisions.md %}) at runtime.

### Script runtime

The script runtime contains the functionality required to execute [scripts]({% link process-automation/latest/model/scripts.md %}) at runtime.

### Preference

User preferences such as interface filters are retained in a key value store within the application database.

## Application query service

The application query service is a set of services used to query data stored by the [application runtime bundle](#application-runtime-bundle). The service is deployed for each application and reads the data stored in the application runtime database.

![Application query service diagram]({% link process-automation/images/arch-query.png %})

### Query

Tables for querying application data are separate to the runtime tables so that queries can be run without accessing any runtime services. Some data aggregation is performed on the tables to improve querying.

### Audit

Audit log tables for all application transactions are separate to the runtime tables so that they can be queried without accessing any runtime services. No data aggregation or manipulation is run against audit logs to enforce an accurate audit trail.

### Notification

The tables used for querying application data are also be used to set up [GraphQL](https://graphql.org/learn/){:target="_blank"} against in order to query specific events and use web sockets with.

## Process storage service

The process storage service is used for storing data in the Content Services repository. The service is deployed for each application.

## Connectors

Connectors are used to execute logic outside of the [application runtime bundle](#application-runtime-bundle). When the process flow reaches a connector, the values are sent from the process instance to a connector using the [message broker](#message-broker) to be used as part of the logic. The results are sent back to the process instance after the connector has finished and the process flow continues.

## Message broker

The message broker deployed with Process Automation routes the events emitted by the application runtime bundle to other services asynchronously.
---
title: Admin overview
nav: false
---

Administration is used to deploy the projects created through modeling and manage the processes and tasks created within the deployed applications.

## Admin Application

The Admin Application is where released projects created in the [Modeling Application]({% link process-automation/latest/model/index.md %}) can be deployed. Once a released project has been deployed it is referred to as an application.

The Admin Application is accessed using the `/admin` URL, for example `https://alfresco.com/admin`.

There are three main areas the Admin Application covers:

* A [DevOps section]({% link process-automation/latest/admin/release.md %}) used to deploy projects, and manage and upgrade applications.
* A  [Process Admin section]({% link process-automation/latest/admin/monitor.md %}) used to manage process instances, tasks and the audit details of all applications.
* An [Identity section]({% link process-automation/latest/admin/users.md %}) used to manage users and groups and assign their permissions.---
title: Process administration
---

The **Process Admin** section of the Admin Application is used to manage applications, process instances, user tasks, service tasks, auditing, and data cleanup.

You can only see this section if you have the `ACTIVITI_ADMIN` role. The information you see in each section is controlled by which applications you have been given administrator access to during [deployment]({% link process-automation/latest/admin/release.md %}#deployment) or afterwards by [updating the application permissions]({% link process-automation/latest/admin/release.md %}#manage-permissions).

## Configure columns

You can configure the columns of the Applications List, Process Instances, User Tasks, and Service Tasks lists in the Admin App.

The order of the columns can be adjusted.

1. Expand the **Process Admin** section on the left of the Admin App and then select **Applications List**, **Process Instances**, **User Tasks**, or **Service Tasks**.

2. Access the six dots on the top left of a column by hovering your mouse over the name of the column.

3. Click and hold the six dots and then move the column on top of another column.

    This moves the columns to the left one position and the column you are moving takes the place of the one underneath.

![Move column]({% link process-automation/images/move-column-admin.png %})

The columns that are visible can be adjusted.

1. Expand the **Process Admin** section on the left of the Admin App and then select **Applications List**, **Process Instances**, **User Tasks**, or **Service Tasks**.

2. Click the three dots on the right of the last column.

3. Select which columns you want show and then click **Apply**.

![Select columns]({% link process-automation/images/select-columns-admin.png %})

## Applications List

The **Applications List** section is for viewing the applications you have released.

### Properties {#applications-properties}

The columns for each application are:

| Property | Description |
| -------- | ----------- |
| Application name | The name of the application. |
| Description | A description of the application, if entered when the application was released. |
| Version | The version of the application. |
| Release | The amount of times the application has been released. |
| Workspace | If the application is the Workspace, there is a link to it. |
| Three dots | Right click on the three dots to access the [Process Instances](#process-instances), [User Tasks](#user-tasks), [Service Tasks](#service-tasks), [Audit](#audit), or [Data Cleanup](#data-cleanup) sections. |
| Star icon | Use the icon to select which application you want to 'favorite'. The application you select will appear first in the search lists, when using the search in the **Process Instances**, **User Tasks**, and **Service Tasks** sections. |

## Process Instances

The **Process Instances** section is for monitoring all active, completed, and suspended process instances that are running in each application. Use the filters to find process instances. To automatically populate the [Service Tasks](#service-tasks) section with all the service tasks of a process instance, click the three dots next to a process instance and select **Service Tasks**.

### Properties {#process-properties}

The properties for each process instance are:

| Property | Description |
| -------- | ----------- |
| ID | The unique ID of the process instance. |
| Name | The name given to the process instance when it was started. |
| Status | The current status of the process instance. See the table below for a list of possible statuses. |
| Created | The name of the user that started the process instance. |
| Start Date | The time since the process instance was started. |
| App Release Version | The [version of the application]({% link process-automation/latest/admin/release.md %}#upgrade) the process instance is using. |

> **Note:** Further details are available to view for each process instance by clicking on it. A properties panel will appear on the right-hand side of the screen.

The status of process instances are:

| Status | Description |
| ------ | ----------- |
| RUNNING | The process instance is currently running. |
| COMPLETED | The process instance has been completed. |
| SUSPENDED | The process instance is currently suspended and cannot continue until it is reactivated. |
| CANCELLED | The process instance has been cancelled and cannot be completed. |

### User tasks

Use the **User Tasks** option to monitor all active, assigned, completed, and suspended tasks that are running for the process instance.

### Service tasks

Use the **Service Tasks** option to monitor all [service tasks]({% link process-automation/latest/model/processes/bpmn.md %}#service-task) that are running for the process instance.

### Variables

Use the **Variables** option to view and edit the [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) values for a process instance.

The properties for variables are:

| Property | Description |
| -------- | ----------- |
| Name | The name of the process variable. |
| Type | The [type]({% link process-automation/latest/model/processes/index.md %}#process-variable-properties) of the process variable. |
| Value | The current value of the variable. The word `json` will be displayed for JSON variables. Click it to view the full JSON value. |
| Edit | If the process instance status is `RUNNING` then the `Value` of a process variable can be updated. |

### Audit {#process-instance-audit}

Use the **Audit** option to view all audit logs for the selected process instance. This will open the [audit](#audit) section with the filter restricted to the application and process instance ID of the selected process instance.

### Activate

Use the **Activate** option to resume a suspended process instance.

Activating a process instance will change the status to `RUNNING`.

> **Note:** The **Activate** option is only available to process instances with a status of `SUSPENDED`.

### Suspend

Use the **Suspend** option to pause a process instance. This will stop any action from completing in the process instance. Use the **Activate** option to resume a suspended process instance.

Suspending a process instance will change the status to `SUSPENDED`.

> **Note:** The **Suspend** option is only available to process instances with a status of `RUNNING`.

### Diagram

Use the **Diagram** option to view which stage the process is currently at and the path that the process instance has taken to get there. The currently active task or activity is highlighted in bold red. The process flow taken is highlighted in red.

### Cancel

Use the **Cancel** option to cancel a process instance. This will stop any action from completing in the process instance. Cancelled process instances cannot be restarted or worked on again.

Cancelling a process instance will change the status to `CANCELLED`.

> **Note:** The **Cancel** option is not available to process instances with a status of `COMPLETED`.

### Delete {#process-instance-delete}

Use the **Delete** option to delete a process instance. When you delete a process instance you will permanently delete it and all of its data and the operation cannot be undone. You can delete one or more selected process instances, regardless of what state they are in. You can delete more than one at the same time by using the **Select multiple** check box on the top right. Once you have selected multiple process instances, click **Delete** from the top right.

## User Tasks

The **User Tasks** section is for monitoring all active, assigned, completed, and suspended tasks that are running in each application.

### Properties {#task-properties}

The properties for each task are:

| Property | Description |
| -------- | ----------- |
| ID | The unique ID of the task. |
| Task Name | The name given to the task. |
| Assignee | The user assigned to the task. |
| Status | The current status of the task. See the table below for a list of possible statuses. |
| Created Date | The time since the task was started. |
| Last Modified | The time since the task was last updated. |
| Parent ID | The ID of a parent task if the standalone task has one. |

Further details are available to view for each task by clicking on it. A properties panel will appear on the right-hand side of the screen and certain properties can be edited if the status is `CREATED` or `ASSIGNED`.

The status of tasks are:

| Status | Description |
| ------ | ----------- |
| CREATED | The task has been created but not yet assigned. |
| ASSIGNED | The task has been assigned but not yet completed. |
| COMPLETED | The task has been completed. |
| SUSPENDED | The task is suspended because the process instance it belongs to has been suspended. It cannot be completed until the process instance is activated. |
| CANCELLED | The task has been cancelled and cannot be completed. |

#### Select multiple user tasks

You can delete or change the assignee of multiple user tasks at the same time.

1. Select the **Select Multiple** check box on the top right.  

2. Use the check boxes on the left next to each user task to select the ones you want to change.

    You can also select all of the user tasks at once by selecting the check box at the top of the list.

3. Click **Delete** or **Change assignee** from the three dots menu on the top right.

    This change will apply to all of the user tasks you have selected on the left.

4. Follow the prompts and confirm to delete the user tasks or select a new assignee and then click **Assign**.

### Variables {#task-variables}

Use the **Variables** option to view and edit the [task variables]({% link process-automation/latest/model/forms.md %}#form-variables) values for a user task.

> **Note:** Task variables are also known as form variables from a modeling perspective.

The properties for task variables are:

| Property | Description |
| -------- | ----------- |
| Name | The name of the task variable. |
| Type | The [type]({% link process-automation/latest/model/forms.md %}#form-variable-properties) of the task variable. |
| Value | The current value of the task variable. The word `json` will be displayed for JSON variables. Click it to view the full JSON value. |
| Edit | If the task status is `CREATED` or `ASSIGNED` then the `Value` of a task variable can be updated. |

### Sibling tasks

Use the **Sibling Tasks** option to view any other standalone tasks that share the same parent task.

### Audit {#task-audit}

Use the **Audit** option to view all audit logs for the selected task. This will open the [audit](#audit) section with the filter restricted to the application and the `Event ID` of the selected user task.

## Service Tasks

The **Service Tasks** section is for monitoring all [service tasks]({% link process-automation/latest/model/processes/bpmn.md %}#service-task) that are running in each application. You can enter a **ProcessInstanceID** in the filter to view all the service tasks of a specific process instance. See [Process Instances](#process-instances) for how to automatically populate the **Service Tasks** section with the service tasks of a particular process instance.

> **Note:** This includes [connectors]({% link process-automation/latest/model/connectors/index.md %}), [decision tables]({% link process-automation/latest/model/decisions.md %}) and [scripts]({% link process-automation/latest/model/scripts.md %}).

### Properties {#service-properties}

The properties for each service task are:

| Property | Description |
| -------- | ----------- |
| ID | The unique ID of the service task. |
| Activity Name | The name given to the service task within the process definition. |
| Status | The current status of the service task. See the table below for a list of possible statuses. |
| Started Date | The time since the service task was started. |
| Completed Date | The time the service task was completed. It will be blank if the service task has not yet been completed. |

The status of tasks are:

| Status | Description |
| ------ | ----------- |
| STARTED | The service task has started to execute. |
| COMPLETED | The service task has been completed. |
| CANCELLED | The service task has been cancelled and cannot be completed. |
| ERROR | The service task had an error during execution. |

### View error

Use the **View Error** option on a service task with the status of `ERROR`. This will display a detailed stack trace of the error associated with the service task.

## Audit

The **Audit** section provides details of all the [events]({% link process-automation/latest/model/processes/events.md %}) that have occurred in applications.

All audit events can be filtered based on the application, event type, event ID, or process instance ID. Use the **Export** button on the top right to download a `.CSV` list of all the audit events. Even if you have filtered the audit events you still download all the audit events for the selected application.

### Properties {#audit-properties}

The properties for each audit event are:

| Property | Description |
| -------- | ----------- |
| Event Type | The type of the event that occurred, for example `SEQUENCE_FLOW_TAKEN` shows where a [sequence flow]({% link process-automation/latest/model/processes/bpmn.md %}#sequence-flow) was followed. |
| Event Time | The timestamp for when the event happened. |
| Event ID | The unique ID of the event. |
| Process Instance ID | The process instance ID of the process that the event occurred in. |
| Event Action | The payload of the event in JSON format. Click to view the details. |

## Data Cleanup

You can clean up historical data using the Create cleanup job process from within the Admin App.

1. Sign into the Admin App.

2. Expand **Process Admin** from the left pane.

3. Select **Data Cleanup**.

4. Click the **+** symbol on the top right to create a new cleanup job.

5. Use the application you want to run the Create cleanup job process for from the drop down menu.

6. Use the applications process definition you want to cleanup.

    You can select multiple process definitions. If you do not select a process definition for the application all process definitions are selected.

7. Use the period of time you want to retain any completed or cancelled processes.

8. Click **Yes I agree** to creating the cleanup job and then click **CREATE**.

![Cleanup Job]({% link process-automation/images/cleanup-job.png %})
---
title: Project deployment
--- 

The **DevOps** section of the Admin Application is used to deploy projects and manage and upgrade applications.

## Project releases

The **Project Releases** section displays a list of all [released projects]({% link process-automation/latest/model/projects.md %}#release-a-project) created in the Modeling Application.

 > **Note**: If you can't find your project in the list, make sure it has been released.

To release a project:

1. Sign in to the Modeling Application.

2. Find or search for your project in the list of projects.

3. Select the **Release** action from the **Options** column for the project.

4. Enter a **Name** for the release and optionally add a **Comment**.

### Properties {#project-properties}

The properties for a released project are:

| Property | Description |
| -------- | ----------- |
| Project Name | Displays the release name of the project. |
| Created By | Displays which user released the project. |
| Created | The time lapsed since the version of the project was released. |
| Comment | Displays the comment entered when the new project was released. |
| Uploaded | An icon displays if the project was uploaded. |
| Latest project release | The version number of the project. |
| Actions | A list of actions that can be made against the released project: {::nomarkdown} <ul><li><b>Download</b> Bundles the project contents into a zipped folder to import it into a different environment.</li><li><b>Restore this release</b> Allows you to restore the release to this version. If you use this action the current models of the project will be replaced with those present in the release. If you want to preserve your current status you must create another release which you can restore it later.</li><li><b>Edit release</b> You can change the name of the release or update the comment made about it.</li></ul>{:/} |

### Deployment

After choosing to **Deploy** a released project, there are a number of configuration settings required depending on the contents of the project.

> **Note**: When a project is deployed, a [deployment descriptor](#deployment-descriptors) is created. Deployment descriptors can be exported from one environment and imported into another, for example between test and production. See the [deployment service architecture]({% link process-automation/latest/admin/architecture.md %}#deployment-service) for further details on the deployment process.

{% capture name %}

All projects require an application name for when they are deployed.

> **Reminder**: Projects are referred to as applications when they are deployed.

1. Provide an **Application Name** for the project. The name must be unique and must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example: `finance-application`.

2. Select which released version of the project to deploy.

{% endcapture %}
{% capture admin %}

All applications require at least one administrator to manage the application. Administrators have access to the [Process Admin]({% link process-automation/latest/admin/monitor.md %}) actions for an application.

Select a user or group to administer the application. The user or group must exist and cannot be set as a static value.

{% endcapture %}
{% capture user %}

The users selected for an application are those able to start process instances and tasks for it.

> **Note**: Any users or groups that were assigned to [user tasks]({% link process-automation/latest/model/processes/bpmn.md %}#user-task) using the **Identity** method will already be entered in this field.

Select the users and groups that can access the application. The users and groups must exist and cannot be set as static values.

{% endcapture %}
{% capture connector %}

> **Note**: This tab will not appear if there are no [connectors]({% link process-automation/latest/model/connectors/index.md %}) in the project being deployed.

Applications that contain connectors need to have their [configuration parameters]({% link process-automation/latest/model/connectors/index.md %}#configuration-parameters) set.

All parameters will appear as key value pairs and additional pairs can be added by clicking **Add config variable**.

Any default values, or values entered whilst modeling the project will be pre-filled but can still be updated.

{% endcapture %}
{% capture storage %}

The storage options are used to set the default location for where data related to a process is stored. This data includes content uploaded from [attach file fields]({% link process-automation/latest/model/forms.md %}#attach-file-fields) in forms, [generated documents]({% link process-automation/latest/model/connectors/generate.md %}), [signed documents]({% link process-automation/latest/model/connectors/docusign.md %}) and content edited using the [content connector]({% link process-automation/latest/model/connectors/content.md %}).

> **Note**: The default location set for the application storage will be used to store the content from the above actions if none of the target locations are set in their configuration. For example, if `targetFile`, `targetFolder`, `targetFolderId` and `targetFolderPath` are not set for the DocuSign connector, the signed document will be stored in the default storage location.

The options for the storage location are:

* **Store content in the following ACS site** can use an existing site in the repository to store the data or create a new one as part of the deployment process.

* **Store content in the folder with the following relative path** can store the application data in a specific folder rather than a site.

> **Important**: Connectors can read and write from files and folders outside of the default storage location, however the service accounts must be given explicit [permission]({% link process-automation/latest/model/connectors/index.md %}#permissions) to read and write to those files and folders.

> **Important**: Users filling in forms with an [attach file field]({% link process-automation/latest/model/forms.md %}#attach-file-fields) must be given explicit permission to the upload directory if it is outside of the default storage location for the application.

{% endcapture %}

{% include tabs.html tableid="deploy-steps" opt1="Application Name" content1=name opt2="Admin Access" content2=admin opt3="User Access" content3=user opt4="Connectors" content4=connector opt5="Storage" content5=storage %}

You can see the progress of the deployment process. The completed steps are marked with an orange tick, while the incomplete ones are marked with an empty circle.

After clicking **Create** the deployment descriptor will be created and the application deployed, if **Deploy** was selected.

### Delete

You can delete a released project from the Admin App by selecting the three dots next to the project you want to delete and select **Delete**.

### Promote a project release from one environment to another

You can download a project release and then upload it to another environment. This is useful because you can test a new project release on a staging environment and then upload it to a production environment.

To upload a project release to another environment:

1. Navigate to the project where you want to download the project release.  

2. On the Releases window click the three dots next to the release you want to upload to another environment and then click **Download**.

    A zip file of the project release is created and downloads to your machine.

3. Navigate to the environment where you want to upload the project release.

4. Navigate to the project where you want to upload the project release.

5. Go to the Releases window and click the **Upload** icon.

6. Select the project release you created earlier.

Once you have uploaded the project release it will appear in the list of project releases you have on the Releases window.

## Deployment descriptors

The **Deployment Descriptors** section displays a list of all deployment descriptors in the environment. These are created by the [deployment service]({% link process-automation/latest/admin/architecture.md %}#deployment-service) whenever a project is deployed.

Deployment descriptors are fully configured projects that can be exported and imported between environments, for example between test and production.

### Properties {#deploy-properties}

The properties for deployment descriptors are:

| Property | Description |
| -------- | ----------- |
| Name | The name of the descriptor and the name that will be used for the application. |
| Status | The status of the descriptor. Once it has been created it will display as `DescriptorCreated`. |
| Created | The date and time the descriptor was created. |
| Modified | The date and time since the descriptor was last modified. |

### Export and import

Deployment descriptors can be exported as `.zip` files using the **Export Deployment Descriptor** option against a specific descriptor.

A previously exported deployment descriptor can be imported using the **Import** button in the **Deployment Descriptors** page.

> **Note**: A deployment descriptor cannot be imported if it uses the same name as a deployment descriptor that already exists.

## Application instances

The **Application Instances** section displays a list of all deployed applications, and applications currently in the process of being deployed. Applications can have their permissions updated.

> **Reminder:** Projects are referred to as applications when they are deployed.

### Properties {#application-properties}

The properties for application instances are:

| Property | Description |
| -------- | ----------- |
| Application name | The name of the application. |
| Project release | Number of the latest project release. |
| Runtime version | Version of software on which the application is running. |
| Updated | Date of the last update of the application. |
| Created | The time since the application was deployed. |
| Status | The status of the application. Once fully deployed it will display as `Running`. |
| Workspace | A link to the [user interface]({% link process-automation/latest/model/interfaces.md %}) for the application. |

### Undeploy

The **Undeploy** action removes a deployed application.

> **Important**: Undeploying an application will remove all data related to the application including processes and tasks. It is not possible to retrieve this data once an application has been undeployed.

### Redeploy

If deployment of an application fails, you can use the **Redeploy** action to quickly start the deployment again.

### Manage permissions

The **Manage Permissions** option allows for additional users to be granted user or administrator access to an application without having to upgrade it.

### Monitoring

You can monitor the health of your installation by using the Monitoring dashboard. There is a dashboard for each deployed application.

To access the dashboard.

1. Log in to the Alfresco Admin App.

2. Expand **Devops** from the left pane and select **Application Instances**.

3. Click the three dots next to the application you want to monitor and select **Monitoring**.

You will see the Monitoring dashboard for the application. Services that are operational have a green dot. Services that are operational but may have some problems have a yellow dot. **Note:** Generally these problems fix automatically. Services that are not operating and require assistance have a red dot. Services that have an unknown state have a grey dot. To gain more insight into a service you can expand it to see more detailed information.

![monitoring dashboard]({% link process-automation/images/monitoring-dashboard.png %})

### Upgrade

Upgrading an application allows for a new version of a released project to be deployed to an existing application. Tasks and process instances that are in progress and based on a previous application version can still be completed, however any new ones started will use the new model definitions. An application can be upgraded to a released project version that is lower than the one currently deployed, however the application version will still increment.

> **Note:** The upgrade process is transactional, which means that if there is an error during the upgrade process the application is automatically rolled back to the previous stable version.

The version of an application is incremental and independent of the released project version, for example:

| Released project version | Application version |
| :----------------------: | :-----------------: |
| 1 | 1 |
| 2 | 2 |
| 4 | 3 |
| 5 | 4 |
| 3 | 5 |
| 10 | 6 |

The upgrade process displays the same configuration as [deploying](#deployment) an application. The only field that cannot be changed when upgrading is the application name.

To upgrade an application:

1. Log in to the Alfresco Admin App.

2. Expand **Devops** from the left pane and select **Application Instances**.

3. Click the three dots next to the application you want to upgrade.

4. Select **Upgrade**.

5. Select the details you want to upgrade and click **Upgrade**.

### Update runtime version

Regularly updating your application to the latest runtime version is a best practice.

To update the runtime version:

1. Log in to the Alfresco Admin App.

2. Expand **Devops** from the left pane and select **Application Instances**.

3. Click the three dots next to the application you want to update.

4. Select **Update runtime version**.

### Logs

You can view Deployment Service Logs, Runtime Bundle Logs, and Process Storage Logs to help understand any errors you may be having with your installation. The Deployment Service Logs are always available because they belong to a shared service. The logs use different blue highlighting to indicate the app being viewed. The Runtime Bundle Logs and the Storage Logs are unavailable if the app is not deployed correctly.

To view the logs:

1. Log in to the Alfresco Admin App.

2. Expand **Devops** from the left pane and select **Application Instances**.

3. Click the three dots next to the application you want review.

4. Select **Logs** and then the logs you want to view.

The log text is color coded. White indicates no issue. Yellow indicates a warning, and Red indicates an error.

### Development configuration

If local development is enabled, you can see the variables required for it, such as a client id, after clicking **Development configuration**.---
title: Users and groups
---

The **Identity** section of the Admin Application is used to create and manage users, groups and their roles.

## Users

The **Users** section displays the current list of users in the system.

### Properties {#user-properties}

The properties for users are:

| Property | Description |
| -------- | ----------- |
| ID | A unique identifier for the user. This is system generated and cannot be changed. |
| Username | A username for the user that they will be known by in Process Automation. |
| Email | An email address associated to the user. |
| First Name | The first name of the user. |
| Last Name | The last name of the user. |

### Add a user

To add a user:

1. Sign into the Admin Application.

2. Expand the **Identity** section and select **Users**.

3. Click the **Add User** button.

4. Fill in the properties for a user and click **Save**.

Once the user has been created, **Edit** the user to assign groups and roles to the user and reset a user's password.

> **Note**: A `Username` cannot be changed once a user has been created.

## Groups

The **Groups** section displays the current list of groups in the system.

Groups are used to quickly assign multiple roles to users and for logically assigning permissions to applications with. They can also be used to create group assignments for [user tasks]({% link process-automation/latest/model/processes/bpmn.md %}#user-task).

### Properties {#group-properties}

The properties for groups are:

| Property | Description |
| -------- | ----------- |
| ID | A unique identifier for the group. This is system generated and cannot be changed. |
| Name | A name to identify the group.

### Add a group

To add a group:

1. Sign into the Admin Application.

2. Expand the **Identity** section and select **Groups**.

3. Click the **Add Group** button.

4. Give a name to the group and click **Save**.

Once the group has been created, **Edit** the group to assign roles to it.

## Roles

The **Roles** section displays the current list of roles in the system.

Roles are used to provide access to the Modeling Application and different areas of the Admin Application.

The roles available are:

| Role | Description |
| ---- | ----------- |
| ACTIVITI_ADMIN | Provides access to the Admin Application. Users with this role are able to see the **Process Admin** section for applications that they have been given administrator access to when an application was [deployed]({% link process-automation/latest/admin/release.md %}#deployment). |
| ACTIVITI_DEVOPS | Provides access to the Admin Application. Users with this role are able to see the [**DevOps**]({% link process-automation/latest/admin/release.md %}) section in order to deploy and manage deployed projects. |
| ACTIVITI_IDENTITY | Provides access to the Admin Application. Users with this role are able to see the **Identity** section and manage users, groups and roles. |
| ACTIVITI_MODELER | Provides access to the [Modeling Application]({% link process-automation/latest/model/index.md %}). Users with this role are able to model and release projects. |
| ACTIVITI_USER | Users require this role to be given user access to an application. |
| APPLICATION_MANAGER | Provides access to the Admin Application. Users with this role are able to see the **Process Admin** section but only the **Process Instances** and **User Tasks** tabs are available. All actions are available for **Process Instances** and **User Tasks** except **Variables** and **Audit**. |
---
title: Develop Process Automation
---

Use the following to develop and customize Process Automation.

## External systems communication

Communication with an external system should use the [REST connector]({% link process-automation/latest/model/connectors/rest.md %}) or the [Lambda connector]({% link process-automation/latest/model/connectors/aws.md %}#lambda).

> **Important**: The REST service and the AWS Lambda account and function need to be hosted outside of the Alfresco hosted environment.

Both connectors can send and return JSON payloads from a process. The REST connector can also be configured as a [trigger]({% link process-automation/latest/model/triggers.md %}#webhooks) for webhooks.

## Extend the Digital Workspace

The default [end user interface]({% link process-automation/latest/model/interfaces.md %}) provided with Process Automation is the [Alfresco Digital Workspace]({% link digital-workspace/latest/index.md %}).
Starting with Process Automation version 7.12, large parts of the Digital Workspace can be easily customized by editing the provided UI, see [creating a custom user interface](#create-a-custom-user-interface). If you're using a version older than 7.12, use the instructions below to extend your Digital Workspace.

### Setup

To start developing Digital Workspace customizations:

1. Request the source code from [Support](https://support.alfresco.com/){:target="_blank"}.

2. Unzip the source code into your development environment and create a `.env` file in the root folder.

3. Insert the following contents in the `.env` file:

    ```bash
    # GENERAL
    AUTH_TYPE="OAUTH"
    PROVIDER="ALL"
    LOG_LEVEL="TRACE"
    ACA_BRANCH="develop"

    # ADW + APA
    API_HOST="https://..."
    API_CONTENT_HOST="https://..."
    API_PROCESS_HOST="https://..."
    OAUTH_HOST="https://..."
    IDENTITY_HOST="https://..."

    PLUGIN_PROCESS_SERVICE=true

    APP_CONFIG_APPS_DEPLOYED="[{"name": "..."}]"
    ```

4. Update the contents of the `.env` file with the following:

    | Property | Description |
    | -------- | ----------- |
    | API_HOST | The API host for the environment in the format `https://alfresco.com`. |
    | API_CONTENT_HOST | The API host for the content services in the format `https://alfresco.com`. |
    | API_PROCESS_HOST | The API host for the process services in the format `https://alfresco.com`. |
    | OAUTH_HOST | The authentication host in the format `https://alfresco.com/auth/realms/alfresco`. |
    | IDENTITY_HOST | The identity service host in the format `https://alfresco.com/auth/realms/alfresco`. |
    | APP_CONFIG_APPS_DEPLOYED | The name of the deployed application to extend the Digital Workspace against. The name is set when the application is deployed, for example `[{"name": "invoice-approval-application"}]`. |

5. Run the following command from the root of your local Digital Workspace: `npm run start content-en-cloud`.

6. Your local Digital Workspace is now connected to your hosted Process Automation application and can be extended, tested and debugged.

### Develop

The Digital Workspace is built using the Application Development Framework. There are a set of [content components](https://www.alfresco.com/abn/adf/docs/content-services/){:target="_blank"} and a set of [process components](https://www.alfresco.com/abn/adf/docs/process-services-cloud/){:target="_blank"} that can be extended.

> **Note**: Process Automation uses the Process Services **Cloud** components.

### Upload

Once the extended Digital Workspace has been fully customized and tested it can be deployed.

1. Remove the `.env` file from your source code.

2. Upload your source code to your Alfresco S3 bucket.

    > **Note**: Please contact [Support](https://support.alfresco.com/){:target="_blank"} if you do not have the details of this bucket.

3. Raise a [Support request](https://support.alfresco.com/){:target="_blank"} with this information:

    * A link to the source code in S3.
    * The name of the application to update.

        > **Note**: This should match what is configured in the `app.config.json` for the interface.

    * The environment the application is deployed in.
    * When the application should be updated with the new interface.

### Extend task list with custom columns

The Digital Workspace provides a default group of columns for your task list. The columns can be changed and configured in the `process-services-cloud.extension.json` file of the [Process Services Cloud extension library](https://github.com/Alfresco/alfresco-apps/tree/develop/libs/content-ee/process-services-cloud-extension){:target="_blank"}.

Here is an example of a task list with default columns preset:

```json
{
  "features": {
    "taskList": {
        "presets": {
            "default": [
                columns schema
            ]
        }
    }
  }
}
```

![Task list with default columns]({% link process-automation/images/task-list-default-columns.png %})

### Add a column in the task list using a task property

To display the task list with new columns, edit the `process-services-cloud.extension.json` file, and insert an entry into the `features.taskList.presets.default` section.

```json
{
  "features": {
    "taskList": {
        "presets": {
            "default": [
                { ...Default Columns schema },
                {
                    "id": "app.task.processDefinitionName",
                    "key": "processDefinitionName",
                    "type": "text",
                    "title": "processDefinitionName",
                    "sortable": true
                },
                {
                    "id": "app.task.appName",
                    "key": "appName",
                    "type": "text",
                    "title": "appName",
                    "sortable": true
                }
            ]
        }
    }
  }
}
```

When you restart the application you will see the new columns in the task list.

![Task list with new columns]({% link process-automation/images/task-list-new-columns.png %})

### Replace a default preset in the task list

To display a task list with new columns already preset, edit the `process-services-cloud.extension.json` file to include the definition of your own set of columns, and insert an entry into the `features.taskList.presets.my-task-presets` section.

```json
{
  "features": {
    "taskList": {
        "presets": {
            "default": [
                { Default Columns schema },
            ],
            "my-task-presets": [
                {
                    "id": "app.task.name",
                    "key": "name",
                    "type": "text",
                    "title": "Name",
                    "sortable": true
                },
                {
                    "id": "app.task.status",
                    "key": "status",
                    "type": "text",
                    "title": "Status",
                    "sortable": true
                },
                {
                    "id": "app.task.processDefinitionName",
                    "key": "processDefinitionName",
                    "type": "text",
                    "title": "processDefinitionName",
                    "sortable": true
                },
                {
                    "id": "app.task.appName",
                    "key": "appName",
                    "type": "text",
                    "title": "appName",
                    "sortable": true
                }
            ]
        }
    }
  }
}
```

To activate the new columns edit the [task-list-cloud-ext.component](https://github.com/Alfresco/alfresco-apps/blob/develop/libs/content-ee/process-services-cloud-extension/src/lib/features/task-list/components/task-list-cloud-ext/task-list-cloud-ext.component.ts){:target="_blank"} file and change the `this.columns = this.extensions.getTaskListPreset` property from `default` to `my-task-presets`.

```typescript
  this.columns = this.extensions.getTaskListPreset('my-task-presets'); 
```

![Task list additional columns]({% link process-automation/images/task-list-additional-columns.png %})

### Add a column in the Task list using a custom template

To display a task list with a custom column template you first need to create a custom component.
For example, to create custom templates for the task name, due date, and priority properties edit the `process-services-cloud.extension.json` file in the following way.

```typescript
import { ChangeDetectionStrategy, Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { TaskDetailsCloudModel } from '@alfresco/adf-process-services-cloud';

@Component({
  selector: 'custom-template-name-column',
  template: `
    <mat-list>
        <mat-list-item>
            <div mat-line>{{ displayValue.name }}</div>
            <div mat-line [ngStyle]="{ 'padding-top': '5px' }">
                <span [ngStyle]="{ 'font-weight': 'bold' }">Assignee :</span>
                <span> {{ displayValue.assignee }}</span>
            </div>
        </mat-list-item>
    </mat-list>
    `,
  host: { class: 'adf-datatable-content-cell adf-name-column' },
})
export class TaskNameComponent implements OnInit {

  @Input()
  context: any;

  displayValue: TaskDetailsCloudModel;

  constructor() {}

  ngOnInit() {
    this.displayValue = this.context?.row?.obj;
  }
}
```

```typescript
import { Component, Input, OnInit } from '@angular/core';
import { TaskDetailsCloudModel } from '@alfresco/adf-process-services-cloud';

@Component({
  selector: 'custom-template-priority-column',
  template: `
    <mat-form-field>
      <mat-label>Change Priority</mat-label>
      <mat-select [(ngModel)]="selectedValue" name="priority">
        <mat-option *ngFor="let priority of priorities" [value]="priority">
          {{priority}}
        </mat-option>
      </mat-select>
    </mat-form-field>
    `,
  host: { class: 'adf-datatable-content-cell adf-name-column' },
})
export class TaskPriorityComponent implements OnInit {

  @Input()
  context: any;

  displayValue: TaskDetailsCloudModel;

  priorities: string[] = ['None', 'High', 'Low', 'Normal'];
  selectedValue: string;

  constructor() {}

  ngOnInit() {
    this.displayValue = this.context?.row?.obj;
    this.selectedValue = this.displayValue.priority;
  }
}
```

```typescript
import { Component, Input, OnInit } from '@angular/core';
import { ProcessInstanceCloud } from '@alfresco/adf-process-services-cloud';

@Component({
  selector: 'custom-template-duedate-column',
  template: `
    <mat-form-field>
        <input matInput [matDatepicker]="picker" placeholder="Change due date" />
        <mat-datepicker-toggle matSuffix [for]="picker"></mat-datepicker-toggle>
        <mat-datepicker #picker></mat-datepicker>
    </mat-form-field>
    `,
  host: { class: 'adf-datatable-content-cell adf-name-column' },
})
export class TaskDueDateComponent implements OnInit {

  @Input()
  context: any;

  displayValue: TaskDetailsCloudModel;

  constructor() {}

  ngOnInit() {
    this.displayValue = this.context?.row?.obj;
  }
}
```

Register the custom components in the [task-list.module.ts](https://github.com/Alfresco/alfresco-apps/blob/9a7c4106fb5befc05bb45e2703bd70c6a7436fb1/libs/content-ee/process-services-cloud-extension/src/lib/features/task-list/task-list.module.ts){:target="_blank"} file. For more on how to register a custom component see [Registration](https://github.com/Alfresco/alfresco-content-app/blob/develop/docs/extending/registration.md){:target="_blank"}.


```typescript
@NgModule({
    declarations: [TaskNameComponent, TaskPriorityComponent, TaskDueDateComponent ]
})

export class TasksListCloudModule {
    constructor(extensions: ExtensionService) {
        extensions.setComponents({
            'app.taskList.columns.name': TaskNameComponent,
            'app.taskList.columns.priority': TaskPriorityComponent,
            'app.taskList.columns.dueDate': TaskDueDateComponent
        });
    }
}
```

Once you have registered your components, you need to register your new template component. To do this you need to add your new column to the `your-app.extensions.json` file:

```json
{
  "features": {
    "taskList": {
        "presets": {
            "default": [
                {
                  "id": "app.task.name",
                  "key": "name",
                  "title": "Name",
                  "type": "text",
                  "template": "app.taskList.columns.name",
                  "sortable": true
                },
                {
                  "id": "app.task.dueDate",
                  "key": "status",
                  "title": "Due Date",
                  "type": "text",
                  "template": "app.taskList.columns.dueDate",
                  "sortable": true
                },
                {
                  "id": "app.task.priority",
                  "key": "priority",
                  "title": "Priority",
                  "type": "text",
                  "template": "app.taskList.columns.priority",
                  "sortable": true
                }
            ]
        }
    }
  }
}
```

Restart the application and you will see the custom columns in the task list based on the new custom template.

![Task list with custom template]({% link process-automation/images/task-list-custom-template.png %})

### Extend process list with custom columns

The Digital Workspace provides a default group of columns for your process list. The columns can be changed and configured in the `process-services-cloud.extension.json` file of the [Process Services Cloud extension library](https://github.com/Alfresco/alfresco-apps/tree/develop/libs/content-ee/process-services-cloud-extension){:target="_blank"}.

Process list with default columns preset.

```json
{
  "features": {
    "processList": {
        "presets": {
            "default": [
                columns schema
            ]
        }
    }
  }
}
```

![Process list with default columns]({% link process-automation/images/process-list-default-columns.png %})

### Add a column in the process list using a process instance property

To display the process list with new columns, edit the `process-services-cloud.extension.json` file, and insert an entry into the `features.processList.presets.default` section.

```json
{
  "features": {
    "processList": {
        "presets": {
            "default": [
                { Default Columns schema },
                {
                    "id": "app.process.processDefinitionId",
                    "key": "processDefinitionId",
                    "type": "text",
                    "title": "ProcessDefinitionId",
                    "sortable": true
                },
                {
                    "id": "app.process.appName",
                    "key": "appName",
                    "type": "text",
                    "title": "appName",
                    "sortable": true
                }
            ]
        }
    }
  }
}
```

When you restart the application you will see the new columns in the process list.

![Process list with new columns]({% link process-automation/images/process-list-new-columns.png %})

### Replace a default preset in the process list

To display a process list with new columns already preset, edit the `process-services-cloud.extension.json` file to include the definition of your own set of columns, and insert an entry into the `features.processList.presets.my-process-presets` section.

```json
{
  "features": {
    "processList": {
        "presets": {
            "default": [
                { Default Columns schema },
            ],
            "my-process-presets": [
                {
                    "id": "app.process.id",
                    "key": "id",
                    "type": "text",
                    "title": "Process Id",
                    "sortable": true
                },
                                {
                    "id": "app.process.name",
                    "key": "name",
                    "type": "text",
                    "title": "appName",
                    "sortable": true
                },
                {
                    "id": "app.process.appName",
                    "key": "appName",
                    "type": "text",
                    "title": "appName",
                    "sortable": true
                }
            ]
        }
    }
  }
}
```

To activate the new columns edit the [process-list-cloud-ext.component](https://github.com/Alfresco/alfresco-apps/blob/develop/libs/content-ee/process-services-cloud-extension/src/lib/features/process-list/components/process-list/process-list-cloud-ext.component.ts){:target="_blank"} file and change the `this.columns = this.extensions.getProcessListPreset` property from `default` to `my-process-presets`.

```typescript
  this.columns = this.extensions.getProcessListPreset('my-process-presets');
```

![Process list with new columns]({% link process-automation/images/process-list-additional-columns.png %})

### Add a column in the process list using a custom template

To display a process list with a custom column template you first need to create a custom component.
For example, to create custom templates for the process name, and status properties, edit the `process-services-cloud.extension.json` file in the following way.

```typescript
import { ChangeDetectionStrategy, Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { ProcessInstanceCloud } from '@alfresco/adf-process-services-cloud';

@Component({
  selector: 'custom-template-name-column',
  template: `
      <mat-list>
        <mat-list-item>
            <div mat-line>{{ displayValue.name }}</div>
            <div mat-line [ngStyle]="{ 'padding-top': '5px' }">
                <span [ngStyle]="{ 'font-weight': 'bold' }">{{ 'ADF_CLOUD_PROCESS_LIST.PROPERTIES.STARTED_BY' | translate }} :</span>
                <span> {{ displayValue.initiator }}</span>
            </div>
        </mat-list-item>
      </mat-list>
    `,
  changeDetection: ChangeDetectionStrategy.OnPush,
  encapsulation: ViewEncapsulation.None,
  host: { class: 'adf-datatable-content-cell adf-name-column' },
})
export class ProcessNameComponent implements OnInit {

  @Input()
  context: any;

  displayValue: ProcessInstanceCloud;

  constructor() {}

  ngOnInit() {
    this.displayValue = this.context?.row?.obj;
  }
}
```

```typescript
import { ChangeDetectionStrategy, Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { ProcessInstanceCloud } from '@alfresco/adf-process-services-cloud';

@Component({
  selector: 'custom-template-status-column',
  template: `
    <mat-chip-list>
        <mat-chip>
            <div [ngStyle]="{ 'padding-right': '5px' }">
                <mat-icon *ngIf="displayValue.status === 'COMPLETED'" [ngStyle]="{ 'color': 'green' }">check_circle</mat-icon>
                <mat-icon *ngIf="displayValue.status === 'RUNNING'"   [ngStyle]="{ 'color': 'green' }">settings</mat-icon>
                <mat-icon *ngIf="displayValue.status === 'SUSPENDED'" [ngStyle]="{ 'color': 'red' }">block</mat-icon>
                <mat-icon *ngIf="displayValue.status === 'CANCELLED'" [ngStyle]="{ 'color': 'red' }">highlight_off</mat-icon>
            </div>
            <span>{{displayValue.status}}</span>
        </mat-chip>
    </mat-chip-list> 
    `,
  changeDetection: ChangeDetectionStrategy.OnPush,
  encapsulation: ViewEncapsulation.None,
  host: { class: 'adf-datatable-content-cell adf-name-column' },
})
export class ProcessStatusComponent implements OnInit {

  @Input()
  context: any;

  displayValue: ProcessInstanceCloud;

  constructor() {}

  ngOnInit() {
    this.displayValue = this.context?.row?.obj;
  }
}
```

Register the custom components in the [process-list.module.ts](https://github.com/Alfresco/alfresco-apps/blob/develop/libs/content-ee/process-services-cloud-extension/src/lib/features/process-list/process-list.module.ts){:target="_blank"} file. For more on how to register a custom component see [Registration](https://github.com/Alfresco/alfresco-content-app/blob/develop/docs/extending/registration.md){:target="_blank"}.

```typescript
@NgModule({
    declarations: [ ProcessNameComponent, ProcessStatusComponent ]
})

export class ProcessListCloudModule {
    constructor(extensions: ExtensionService) {
        extensions.setComponents({
            'app.processList.columns.name': ProcessNameComponent,
            'app.processList.columns.status': ProcessStatusComponent
        });
    }
}
```

Once you have registered your components, you need to register your new template component. To do this you need to add your new column to the `your-app.extensions.json` file:

```json
{
  "features": {
    "processList": {
        "presets": {
            "default": [
                {
                  "id": "app.process.name",
                  "key": "name",
                  "title": "ADF_CLOUD_PROCESS_LIST.PROPERTIES.NAME",
                  "type": "text",
                  "template": "app.processList.columns.name",
                  "sortable": true
                },
                {
                  "id": "app.process.status",
                  "key": "status",
                  "title": "ADF_CLOUD_PROCESS_LIST.PROPERTIES.STATUS",
                  "type": "text",
                  "template": "app.processList.columns.status",
                  "sortable": true
                }
            ]
        }
    }
  }
}
```

Restart the application and you will see the custom columns in the process list based on the new custom template.

![Process list custom template]({% link process-automation/images/process-list-custom-template.png %})

## Create a custom user interface

Starting with Process Automation version 7.12, custom user interfaces can be modified, starting from the default interface. If you're using older Process Automation version and wish to modify the user interface, see [extending digital workspace](#extend-the-digital-workspace) instead.

To create a custom user interface:

1. Sign in to the Modeling Application and open a project.

2. Click the three dots next to **UI** and then select **Create Custom UI**.

3. Enter the name of the custom UI.

If you want to develop the custom UI basing on the existing default UI of the application, select **Generate from template** and click **download source code link**. Once your custom UI is ready to be deployed select **Upload** (you need to build your application and create a zip from the build).

### Develop a custom user interface

Custom UIs can be developed using hyland nx generators.

The downloaded zip includes instructions how to customize application. To see the instructions, refer to **plugins-generators.md** file within the downloaded ZIP package.

### Upload {#custom-upload}

Once the custom interface has been fully developed and tested it can be deployed.

1. Sign in to the Modeling Application and open a project.

2. Select the created custom UI under the UI drop-down list.

3. Click **Upload**.

4. Upload the custom UI as a ZIP file.

## Custom form fields

To include custom form fields within a form, the [form field customizations](https://github.com/Alfresco/alfresco-ng2-components/blob/develop/docs/user-guide/extensibility.md){:target="_blank"} must be included in the [customization of Digital Workspace](#extend-the-digital-workspace) or the [development of a custom user interface](#develop-a-custom-user-interface).

> **Note**: The custom field can be [included in a form]({% link process-automation/latest/model/forms.md %}#custom-form-widgets) before the custom interface has been deployed.

## REST API

The REST APIs are accessed differently depending on whether a service is an application or platform-specific. For application endpoints, the application name will form part of the endpoint.

The OpenAPI specifications for application endpoints require the `{application-name}` element in the URL:

* Application runtime bundle: `{domain-name}/{application-name}/rb/swagger-ui/index.html`.
* Application query service: `{domain-name}//{application-name}/query/swagger-ui/index.html`.

The query service can also use GraphQL to expand the querying and can be accessed at: `{domain-name}/{application-name}/notifications/graphiql`.

## Clean up historical data

You can use the REST API or the Create cleanup job process from within the Admin App to clean up your historical data.

### Clean up using REST API

You can clean up historical data using the REST API by using specific keys as input paramaters.

| Property | Description |
| -------- | ----------- |
| `historicRetentionDays` | *Required.* The number of days to retain any completed or cancelled processes. |
| `processDefinitionKeys` | *Optional.* A list of process definition keys to clean up. If omitted, all current process definitions are queried from the database and applied to delete the criteria. The default is `null`. |
| `limitSize` | *Optional.* A parameter that specifies the delete query size limit for performance. The default is `1000` rows. |
| `schemaPrefix` | *Optional.* A parameter that specifies the schema prefix, i.e. `public`. The default is an empty string. |
| `async` | *Optional.* A parameter that specifies the job execution strategy via the task executor. The default is true. |

For example:

`POST /v1/admin/batch/jobs/executions/cleanup-query-process-instance-history-job`

```json
{
  "historicRetentionDays": 10,
  "processDefinitionKeys": ["ConnectorProcess", "HeadersConnectorProcess"],
  "limitSize": 100,
  "schemaPrefix": "public",
  "async": true
}
```

### Replay service task using REST API

If a service task does not complete due to a Cloud connector failure it's possible to replay the task and send a new integration request. To do this you must provide the execution id and the definition id of the service task:

`POST /v1/executions/{executionId}/replay/service-task`

```json
{
   "flowNodeId": "flowNodeId"
}
```
---
title: Authentication
--- 

Use Authentication when your system requires access to external REST services.
An authentication called **Application Service Credentials** is already created for use within Process Automation. The authentication can be used when you create radio buttons or dropdown lists on your forms. The authentication is selected from the **Authentication** dropdown list, accessed from: **Field Editor > Advanced > REST Service > Authentication**. The authentication it uses is the same as the authentication assigned to the script runtime user.

> **Note:** The name **Application Service Credentials** cannot be used for one of your own authentications because it is reserved.

## Properties

The basic properties of creating authentication are:

| Property | Description |
| -------- | ----------- |
| Authentication name | *Required.* The name used to identify the authentication. The name must be in lowercase and be between one and 26 characters in length, for example `token1auth`. |
| Authentication description | *Optional.* A description of the authentication, for example `Basic authentication used`. |
| Authentication type | *Required.* Select the type of authentication, for example `Basic`. There are three types of authentication you can use, `Basic`, `Client credentials`, and `Bearer token`. |
| Secured | *Optional.* When selected, credentials are defined during deployment time, or de-select the checkbox to provide them during modeling time. These credentials are used when contacting the external API. |
| Clientid | *Required.* When using Client credentials authentication, enter the client id, for example `Client-1`. |
| Client secret | *Required.* When using Client credentials authentication, enter the client secret for the API, for example `client.secret`. |
| Endpoint| *Required.* When using Client credentials authentication, enter the end point of the server, for example `client.endpoint`. The endpoint entered is validated before you can save the authentication. |
| Scope | *Required.* When using Client credentials authentication, enter one or more scope values that make up part of the API account you want to access, for example `api.account.one`. The scope entered is validated before you can save the authentication. |
| Token | *Required.* When using Bearer token authentication, enter the bearer token for the API, for example `bearer-token`. |

 > **Note**
 >
 > All the configuration parameters can be overridden at deployment time.

## Create authentication

To create authentication:

1. Sign into the Modeling Application and open a project.

2. Click the **+** next to Authentications.

3. Enter a name for the authentication.

   Optionally, enter a description for the authentication.

4. Select an authentication type from the dropdown list.

   Optionally, deselect **Secured** so you can enter a username and password that is used when contacting the API.

## Authentication

The following is an authentication created using Basic authentication and a username and password.

![Authentication]({% link process-automation/images/authentication.png %})

## Upgrade authentication for deployed application

You can upgrade the authentication of your deployed application.

To upgrade your authentication:

1. Expand the **Devops** section on the left of the Admin App and then select **Application Instances**.

2. For the application you want to upgrade, click the three dots on the right of the last column and then select **Upgrade**.

3. Select the version you want to upgrade to from the **Upgrade** dropdown list.

   If you select a version of the application that is identical to the currently deployed one, you will optionally be able to change the configuration values further in this process. If you select a different version of the application that does not have the same configuration values as the currently deployed one, you will be forced to re-enter the authentication values for that application further in this process.

4. If you want users to receive an email each time a process assigns them a task, select **Enable user task mail notifications** and then select the **Authentications** tab.

5. Select **Change the authentication values** to change the current authentication values and then click **Upgrade**.

   If you are upgrading to a different version of the application to the currently deployed one, the **Change the authentication values** check box will not be visible. Instead, you will be required to re-enter the authentication values of the authentication assigned to the version of the application you are upgrading to.

6. Click **Upgrade**.

   **Important:** For your authentications that are not secure, in other words you did not select the **Secured** check box when the authentication was created, the configuration values already set in the Modeling Application will be automatically applied during the upgrade process. For your authentications that are secure, in other words you did select the **Secured** check box when the authentication was created, you must must re-enter the authentication values on the **Authentications** tab when performing the upgrade.

## Delete authentication

To delete an authentication:

1. Sign into the Modeling App and open the project that contains the authentication you want to delete.

2. Expand the **Authentications** section on the left.

3. Select the authentication you want to delete.

4. Click the three dots and then select **Delete**.

5. You will see **Deleting the authentication may affect your project if this authentication is already in use**. Click **Confirm** if you still want to delete the authentication.
---
title: Content models
---

Content models describe how data should be stored in the repository and the metadata that can be associated to the content and folders within that model.

Each model is identified by a unique namespace, prefix and name, and made up of custom types, aspects, properties and constraints.

![Content model diagram]({% link process-automation/images/content-model.png %})

## Properties

The properties of a content model are:

| Property | Description |
| -------- | ----------- |
| Content model name | *Required.* The name of the content model. Must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example `finance`. |
| Namespace | *Required.* A namespace unique within the repository for the content model to sit under. This ensures that all custom types, aspects and properties are also unique within the repository. The default value will append the `Name` of the model, for example `http://finance.com/model/finance`. |
| Prefix | *Required.* An abbreviation of the `namespace` of a content model to refer to types and aspects without needing to use the full namespace. The default value will be the `Name` of the model, for example `finance`. |
| Creator | *Optional.* The author of the model. The default value is the currently signed in user, for example `modeler`. |
| Content model description | *Optional.* A free text description of what the content model is for, for example `A content model for recording financial accounts records.` |

## Create a content model

Content models can be global in scope, so they are available to import into multiple projects or they can be created at an individual project level.

### Create a global content model

To create a global content model:

1. Sign into the Modeling Application and click on **Content Models**.

2. Click the **NEW** dropdown.

3. Select **Content Model** and enter a name and optional description.

To use a global content model within a specific project:

1. Sign into the Modeling Application and open a project.

2. Click the **NEW** dropdown.

3. Select **Import > Content Model** and choose the model to import.

### Create a content model in a project

To create a content model in a project:

1. Sign into the Modeling Application and open a project.

2. Click the **NEW** dropdown.

3. Select how to create the content model:

    * **Create > Content Model** creates a new, empty form.

    * **Upload > Content Model** allows for uploading an existing content model `.xml` file into the Modeling Application.

    Alternatively use the **+** or **Upload** buttons next to **Content Models** in the left-hand menu.

4. Enter a name and optional description.

## Content model modeling

Content models are created within a project and are exclusive to that project unless the content model scope is changed to global. Once a content model is global it will appear at the same level as projects in the modeling application and can be imported into other projects.

Use the **Turn global** option under [actions](#actions) when a content model is selected to change the scope to global.

> **Note**: It is not possible to change the scope back to a single project once the **Turn global** option has been used. The content model will need to be removed from the project and either recreated, or reimported.

### Custom types

Custom types set the properties and relationships that a file of that type can support. Custom types can inherit the properties of a parent type. `Content` and `Folder` are two example types that are already defined in Alfresco Content Services.

The properties of a custom type are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the custom type. Custom type names can only contain alphanumeric characters, hyphens and underscores, for example `supplier-invoice`. |
| Parent type | *Required.* A parent type for the custom type. All properties and aspects assigned to the parent are inherited by the child, for example `cm:content`. |
| Title | *Optional.* A display label for the custom type that will be displayed to users, for example `Supplier Invoice`. |
| Description | *Optional.* A free text description of what the custom type is for, for example `An invoice received from a supplier.` |

Custom types are stored as JSON, for example:

```json
{
  "parentName": "cm:content",
  "name": "supplier-invoice",
  "prefixedName": "finance:supplier-invoice",
  "description": "An invoice received from a supplier.",
  "title": "Supplier Invoice",
  "properties": []
}
```

### Aspects

Aspects are a collection of properties that can be used to describe data and behavior. A file must be of one type, however it can have multiple aspects attached to it. `Classifiable` and `Versionable` are two example aspects that are already defined in Alfresco Content Services.

The properties of an aspect are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the custom aspect. Custom aspect names can only contain alphanumeric characters, hyphens and underscores, for example `isArchivable`. |
| Title | *Optional.* A display label for the custom aspect that will be displayed to users, for example `Archivable`. |
| Description | *Optional.* A free text description of what the custom aspect is for, for example `The status of the document for archiving purposes.` |

Aspects are stored as JSON, for example:

```json
{
  "name": "isArchivable",
  "prefixedName": "finance:isArchivable",
  "description": "The status of the document for archiving purposes.",
  "title": "Archivable",
  "properties": []
}
```

### Properties

Properties are the metadata that describe content. `Author` is an example property that is already defined in Alfresco Content Services used for specifying who wrote the content.

Properties can be assigned to a custom type or an aspect. Select which type or aspect to create the property under before creating it.

The properties of properties are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the property. Property names can only contain alphanumeric characters, hyphens and underscores, for example `datePaid`.  |
| Title | *Optional.* A display label for the property that will be displayed to users, for example `Date Paid`. |
| Description | *Optional.* A free text description of what the property is for. For example `The date the invoice was paid.` |
| Data type | *Optional.* The data type of the property. See the following table for a list of data types, for example `d:date`. |
| Mandatory | *Optional.* Set whether the property is mandatory, for example `false`. |
| Multiple | *Optional.* Set whether the property can contain multiple values, for example `false`. |
| Default value | *Optional.* Set a default value for the property. |
| Constraint | *Optional.* Set a constraint on the values that can be entered for the property, for example `Regular expression`. |
| Indexing | *Optional.* Set whether the property can be searched on and how it is searchable, for example `Free text`. |

The options for data types of properties are:

| Data type | Description |  
| --------- | ----------- |
| d:text | A sequence of characters |
| d:mltext | A multilingual sequence of characters containing localized representations |
| d:int | A positive whole number |
| d:float | A float value |
| d:double | A double value generally used for decimal values |
| d:date | A specific date in the format `DD-MM-YYYY` |
| d:datetime | A specific date and time |
| d:boolean | A value of either `true` or `false` |

The options for constraints of properties are:

| Constraint type | Description |
| --------------- | ----------- |
| Regular expression | Set a regular expression that values must match to be valid for example, a regular expression that matches four letters followed by four digits would be: `/^[A-Za-z]{4}\d{4}$/` |
| Minimum / maximum length | Set the minimum and maximum number of characters a value for the property can be, for example `0` and `10`. |
| Minimum / maximum value | Set the minimum and maximum values for properties, for example `5`. |
| List of values | Set a list of predefined values the property must be chosen from, for example `payable`,`non-payable`,`unknown`. |
| Java class | Set the fully qualified Java class to use for restricting the values of the property. |

The index options of properties are:

| Search type | Description |  
| --------- | ----------- |
| None | The property is not searchable. |
| Free text | Property is searchable but the values will not be available in the search result filters. |
| List of values - whole match | This option enables you to filter on a property in the search results while searching for the whole term. |
| List of values - partial match | This option enables you to filter on a property in the search results while searching the property using wildcard characters. |
| Pattern - unique matches | This option enables you to use unique identifiers which are searched on the basis of the full value of the property. The property itself will not be shown as a filter in the search results. |
| Pattern - many matches | This option enables you to use identifiers which could be searched on the basis of the full value or via the wild card characters. The property itself will not be shown as a filter in the search results. |

Properties are stored as JSON, for example:

```json
{
  "name": "datePaid",
  "prefixedName": "finance:datePaid",
  "title": "Date Paid",
  "description": "The date the invoice was paid.",
  "dataType": "d:date",
  "facetable": "UNSET",
  "indexTokenisationMode": "TRUE",
  "multiValued": false,
  "mandatoryEnforced": false,
  "mandatory": false,
  "indexed": true
}
```

## Actions

The actions that can be run against a content model are:

| Action | Description |
| ------ | ----------- |
| Download content model | Download the XML for the content model. |
| Validate | Run validation against the content model. Any errors can be seen in the log history at the bottom of the Modeling Application and are flagged in a pop-up box. |
| Save | Save any changes made to the content model. |
| Turn global | Changes the content model to have a global scope, so it can be imported into multiple projects. This action is only available if the content model is not already of global scope. |
| Remove from project | Removes the content model from the project. This action is only available if the content model is already set to global scope. |
| Delete | Delete the content model. |
---
title: Data Models
---

A data model allows you to represent complex objects your application is handling. It allows you to define the standard data structure you will use in your application using JSON schema. A data model is useful when you want to query an internal or external service that has a specific structure.
The data model editor allows you to visually create the JSON schema and the JSON editor allows you to see the JSON code of the schema. When you use a data model it provides auto-completion in your scripts and expressions. You can also map a data model with your variables and connector properties. You can use the Upload button to upload a previously defined JSON schema that you have downloaded from Process Automation.

These instructions describe how to make a data model for a specific process but you can create a data model for use at a global level where the same data model properties can be used across multiple processes. To create a global data model Click **New** > **Data model** from the home screen. Alternatively you can transform your data model into a global one by selecting the three dots on the right hand side of your open data model and selecting **Turn global**.  

> > **Note:** If you transform your data model into a global one you are unable to revert it.

## Properties

The properties of a data model are:

| Property | Description |
| -------- | ----------- |
| Data model name | *Required.* The name of the data model. Must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example 'person'. |
| Type | *Required.* Use the Type field to select the JSON schema type you want to use, for example `object`. You can select more than one JSON schema type from the dropdown list, except you cannot select more than one type from the Modelling app section. |
| Upload | *Optional.* You can upload a predefined data model. It must be in JSON schema format, for more see [JSON schema](https://json-schema.org/){:target="_blank"}. |
| Data model description | *Optional.* A free text description of what the data model is, for example 'This data model represents a person in an organization'. |

## Create a data model

The following example creates a data model that represents a person, including their name, date of birth, and gender.

> **Note:** Data models are specific to your installation and configuration. The example described here creates a data model called Person. The model ensures that any service that uses the Person object understands its structure. This example is simple but it allows you to see how the process works but your data models could be more involved.

### Create a data model for a specific process

To create a data model:

1. Sign into the Modeling Application and open a Project, and then click the **+** icon next to **Data Models**.

    > **Note:** You are able to upload already defined data models by using the **Upload** button next to Data models. Any data model you upload must be written in the JSON format.

2. Enter a name for the data model, for example 'person'.

3. Enter a description for the data model, for example 'This model provides the data structure for the object Person'.

    You are presented with the Data Model Editor.

4. From the **Type** dropdown list select **object** from the JSON schema types section.

    You select object because the person data model will contain different fields.

    You can click the cog icon to access the advanced settings which are standard JSON schema configuration settings, for more see [JSON schema](https://json-schema.org/).

5. In the title field enter a meaningful title.

    The title entered will be seen by a user when using a form with this data model.

6. Click the **+** icon to add a property to the Person object.

    A new row is created.

7. Enter `Name` for the new row and then select the **Required** check box.

    Selecting the required check box ensures when a new person is added, the entry must include a Name.

8. From the **Type** dropdown list select **string**.

9. In the title field enter a meaningful title.

10. Click the **+** icon to add another property to the Person object.

11. Enter `DateOfBirth` for the new row.

12. From the **Type** dropdown list select **date** from the Modelling app section.

13. Click the **+** icon to add another property to the Person object.

14. Enter `Gender` for the new row and then select the **Required** check box.

15. From the **Type** dropdown list select **enum** from the Enumeration section and then enter a meaningful title in the title field.

16. Select the cog icon to access the Advanced settings and enter the gender definitions you would like to include in the **Enumerated values** box. Click **Save**.

    You can see the JSON definition of the enumerated values in the preview section.

17. Click the **Save** icon to save the data model and then to see the JSON file created of the data model, click the **JSON Editor** button .

  > **Note:** You can also use references in your data model, for more see [Using Ref in a data model](#using-ref-in-a-data-model).

```JSON
{
    "description": "This model provides the data structure for the object Person.",
    "type": "object",
    "properties": {
        "Name": {
            "type": "string",
            "title": "Name of person"
        },
        "DateOfBirth": {
            "$ref": "#/$defs/primitive/date"
        },
        "Gender": {
            "enum": [
                "male",
                "female"
            ],
            "title": "Gender"
        }
    },
    "title": "Person",
    "required": [
        "Name"
    ]
}
```

You have created a data model called Person that can be used in Process Automation. Use the Simulator on the right to view how the information you have added to the data model appears on a form. You can test the rules you have created for each property and you can see the JSON output when a new person is added.

![Data model]({% link process-automation/images/data-model.png %})

### Using a data model in a process

To use the data model you created in a project:

1. In the Modelling Application click the **+** icon next to processes and create a new process called 'person-process'.

2. Select **Create REST connector** from the **Connectors** menu.

3. Select **Create new instance** from the **Connector Editor Settings** window and enter 'rest-connector-person' for the connector name and then click **Apply**.

4. Use an arrow to connect to the Rest connector object.

5. Select the Rest connector object and then click the **Append task** icon.

6. Select the second object and click the **Change type** icon and then select **User Task**.

7. Ensure the User task is still selected and then click **Assignment** in the properties pane.

8. Select **Identity** and find the user you want to assign the task to and then click **Assign**.

9. Select the User task and click **Append EndEvent**.

10. Click anywhere in the whitespace to de-select the tasks and then click **Edit Process Variables** in the properties pane.

11. Click the **+** symbol and enter a name for the variable called 'Person'.

12. Click the **Type** dropdown list and select Data Models and then select the person data model. Click **Update**.

    You can see the properties of your data model in the Process variables window.

13. Select the REST connector object and then from the **Action** dropdown list select **Get**.

     You are calling a service using the REST connector.

14. In the Output mapping section select the Process variable for the `restResult` field to be `person`.

     This means your person variable will be populated with the result which means you can use the data within your person task.

15. Select the User task again and create a new form from the properties menu and call it 'person' and then add a textbox to it.

16. In the **Field Editor** of the textbox add a label called 'Name' and then click **Save**.

    > **Note:** You must add a text box for each of the fields you created when you made the data model and you must label them accordingly.

    You now have a user task that is using a form called person and that form contains a checkbox called 'Name'.
  
17. Go back to the process and select the user task and then edit the **Process variable/Value** field of the parameter called 'Name' that is under input mapping.

     > **Note:** You must do this for all the fields you want on your form.

18. On the **Edit variable mapping** window select **Expression** and add `${person.Name}` and then click **Update**.

    You have added the value that the Name field will use on the form. You can use the auto-completion functionality to enter the expression.

    > **Note:** You must do this for all the fields you want on your form.

You now have a data model that is being used by a process that is processing complex objects.

### Using Ref in a data model

You can also use references when constructing your data model. Using the person data model you created earlier as an example, you can use reuse the defined reference in several properties of the data model. For example a reference called ID (which is used company wide as the ID of an employee), and might be constructed of a username, and position could be reused in numerous properties. A reference cannot be used in other data models.

To use references in a data model:

1. In the person data model click the **+** icon next to the references field to add a definition.

2. Enter 'ID' for the name of the reference and from the **Type** dropdown list select **object**.

3. In the title field enter a meaningful title.

4. Click the **+** icon again to add another row.

5. Enter 'Username' for the name of the row and From the **Type** dropdown list select **object**.

6. In the title field enter a meaningful title.

7. In the main section of the person data model click the **+** icon again to add another property row.

8. Enter a name for the new row and then select the **Required** check box.

9. From the **Type** dropdown list select **ref** under the composition heading.

10. From the second **Type** dropdown list that appears select the references block you want to use and then click **Save**.

You now have a reference being used within your person data model.

![Ref Data model]({% link process-automation/images/ref-data-models.png %})
---
title: Decision tables
--- 

Decision tables are used to manage business decisions within process workflows. They adhere to the Decision Model and Notation (DMN) standard. Decision tables take at least one input and have at least one output. The inputs are evaluated against a set of rules defined by the modeler and then produce the relevant output(s) that match those rules back to the process.

Decision tables can be added to a process definition by creating a [business rule task]({% link process-automation/latest/model/processes/bpmn.md %}#business-rule-task) and selecting the `name` of a decision table from the dropdown.

## Properties

The basic properties of a decision table are:

| Property | Description |
| -------- | ----------- |
| Decision table name | *Required.* The name of the decision table. Must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example `temperature-evaluation`. |
| Decision table description | *Optional.* A description of what the decision table should be used for, for example `Decision table to select an ice cream flavor based on temperature.` |

## Create a decision table

To create a decision table:

1. Sign into the Modeling Application and open a project.

2. Click the **NEW** dropdown.

3. Select how to create the decision table:

    * **Create > Decision Table** creates a new, empty decision table.

    * **Upload > Decision Table** allows for uploading an existing decision table `.xml` file into the Modeling Application.

    Alternatively use the **+** or **Upload** buttons next to **Decision Tables** in the left-hand menu.

4. Enter a name and optional description.

## Decision table modeling

The following is a decision table that selects the best flavor of ice cream to eat based on which day of the week it is and what the temperature is. This example will be used to assist in explaining the different elements that make up a decision table.

![Example decision table]({% link process-automation/images/decision-table.png %})

### Inputs

Inputs are the fields a decision table evaluates against. In the ice cream decision table the inputs are `dayOfWeek` and `temperature` of data types `string` and `integer` respectively. [Process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) and a [mapping type]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping) are used to pass the value of an input into the decision table to be evaluated. Inputs also contain a label which are `Day of the week` and `Temperature (Celsius)` in the example.

The following is the XML for input variable `dayOfWeek`:

```xml
<input id="InputClause_Ice_cream" label="Day of the week" activiti:inputVariable="dayOfWeek">
   <inputExpression id="LiteralExpression_Ice_cream" typeRef="string" />
</input>
```

![Example decision table inputs]({% link process-automation/images/decision-input.png %})

Input entries, or values are the possible input values to match against for each rule in a decision table. In the ice cream example, possible values include `Monday` and `>=25`.

> **Note**: Inputs can have a `-` in a column that matches any value passed in. This appears as blank in the associated XML.

The following is the XML for the input entry of row 1:

```xml
<inputEntry id="UnaryTests_0pwpzaz">
   <text></text>
</inputEntry>
<inputEntry id="UnaryTests_0g2rex3">
   <text>&gt;35</text>
</inputEntry>
```

Input entries use the FEEL (Friendly Enough Expression Language) language.

### Outputs

Outputs are the result(s) that a decision table comes to after evaluating the inputs. Output columns have a `name` and a `label`. Output values can be passed back to the process using [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) and setting the desired [mapping type]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping). In the ice cream decision table the output `name` is `flavor` and it is of data type `string`.

The following is the XML for the output from the ice cream decision table

```xml
<output id="OutputClause_Ice_cream" label="Flavor" name="flavor" typeRef="string" />
```

![Example decision table output]({% link process-automation/images/decision-output.png %})

Output entries are the possible outputs for each rule in a decision table. In the ice cream example, possible values include `Triple chocolate` and `Honeycomb`.

The following is the output entry for row 10:

```xml
<outputEntry id="LiteralExpression_1olsqqv">
   <text>"Triple chocolate"</text>
</outputEntry>
```

### Rules

Each row in a decision table is known as a rule. A rule evaluates which outputs are valid for the input(s) provided. In the ice cream flavor example, the following are some of the rules:

![Example decision table rules]({% link process-automation/images/decision-rules.png %})

* On a Monday when the temperature is below 25°c, you should eat pistachio ice cream.
* On a Wednesday when the temperature is 25°c or above, you should eat vanilla ice cream.
* On a Friday you should eat triple chocolate ice cream, irrespective of temperature.
* On Saturdays or Sundays when the temperature is 25°c or above, you should eat mint chocolate ice cream.
* When the temperature is above 35°c you should eat lemon sorbet, irrespective of the day.

> **Note**: If there are multiple inputs in a single rule, decision tables use an `AND` operator between the inputs.

[Simulation](#simulating-decision-tables) allows you to see which rules are satisfied by testing input values.

The XML for a rule is the combination of the input and output entries with a unique rule `id`. The following is an example for rule or row 12:

```xml
<rule id="DecisionRule_1drb7gg">
   <inputEntry id="UnaryTests_07yha3g">
      <text>"Saturday","Sunday"</text>
   </inputEntry>
   <inputEntry id="UnaryTests_00i1d80">
       <text>&gt;=25</text>
   </inputEntry>
   <outputEntry id="LiteralExpression_1i6ddhb">
        <text>"Mint chocolate"</text>
   </outputEntry>
</rule>
```

### Hit policies

Underneath the name of the decision table is a letter that sets the hit policy for a decision table. Hit policies are used to set how rules are evaluated when a decision table is executed.

Using the ice cream example, the letter is `F` which is a `FIRST` hit policy. This means that whilst multiple rules can be matched, only the first one matched will be returned as the output. The rules are evaluated in the order they are defined in the decision table.

![Example decision table hit policy]({% link process-automation/images/decision-policy.png %})

Hit policies are defined at the top level of a decision table XML:

```xml
<decisionTable id="DecisionTable_Ice_cream" hitPolicy="FIRST">
```

### Annotations

On the far right of a decision table is a column for annotations. This is just a place to store notes and is only visible to the modeler.

![Example decision table annotation]({% link process-automation/images/decision-annotation.png %})

Annotations are contained in a `description` property of a rule in the XML:

```xml
<rule id="DecisionRule_0vx00qh">
   <description>Treat day.</description>
...
</rule>
```

## Hit policy types

Hit policies define how many rules can be matched in a decision table and which of the results are included in the output.

The default hit policy is `UNIQUE`.

| Hit policy | Description |
| ---------- | ----------- |
| `U`: `UNIQUE` | Only a single rule can be matched. If more than one rule is matched the hit policy is violated |
| `A`: `ANY` | Multiple rules can be matched. All matching rules must have identical entries for their output and if matching rules have different output entries the hit policy is violated |
| `F`: `FIRST` |  Multiple rules can be matched. Only the output of the first rule that is matched will be used, with rules being evaluated in the order they are defined in the decision table |
| `R`: `RULE ORDER` |  Multiple rules can be matched. All outputs are returned in the order that rules are defined in the decision table |
| `O` : `OUTPUT ORDER` | Multiple rules can be matched. All outputs are returned in the order that output values are defined in the decision table |
| `P` : `PRIORITY` | Multiple rules can be matched. Only the output with the highest priority will be used, with priority being calculated based on the order rules are specified in descending order |
| `C`: `COLLECT` | Multiple rules can be satisfied and multiple outputs will be generated with no ordering. Aggregators can be used to group the results which will generate only a single output. See the following rows for collect aggregators. |
| `C +`: `COLLECT SUM` | The sum of the output values is used to generate a single output |
|`C <`: `COLLECT MIN` | The lowest value output is used to generate a single output |
| `C >`: `COLLECT MAX`| The highest value output is used to generate a single output |
| `C #`: `COLLECT COUNT`| The total number of outputs is used to generate a single output |

## Decision table simulation

Once you have designed a decision table, you can test which rules are satisfied by entering test input values.

In the UI click the **Simulate** button after entering the input values to simulate. The results will be populated in the outputs section.

The payload of the API accepts an XML file of the decision table definition, the table name and the test input values as JSON and returns the output values as JSON.

## Actions

The actions that can be run against a decision table are:

| Action | Description |
| ------ | ----------- |
| Download decision table | Download the XML for the decision table. |
| Validate | Run validation against the decision table. Any errors can be seen in the log history at the bottom of the Modeling Application and are flagged in a pop-up box. |
| Save | Save any changes made to the decision table. |
| Delete | Delete the decision table. |
---
title: Files
---

Any type of file can be uploaded and used within a project. The file you upload will usually be an image or a script, and the script can contain a template for use within the modelling application.

## Properties

The basic properties of a file are:

| Property | Description |
| -------- | ----------- |
| File name | *Required.* The name of the file. Must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example `order-template`. |
| File description | *Optional.* A description of what the file should be used for, for example `A template for orders to follow`. |
| Private | *You must select either 'Private' or 'Public'*. Private files are only available within the Runtime Bundle Docker container and are specified using the `FILES_PATH` environment variable. For example, you could use the file as an email template. |
| Public | *You must select either 'Private' or 'Public'*. Public files can be used within a Docker container and are specified using the `FILES_PATH` environment variable and they can also be accessed using HTTP. For example, customizing the Digital Workspace logo. |

## Create a file

To create a file:

1. Sign into the Modeling Application and open a project.

2. Click the **NEW** dropdown.

3. The **Create > File** and **Upload > File** options both require a file to be uploaded into the Modeling Application. Alternatively use the **+** or **Upload** buttons next to **Files** in the left-hand menu.

4. Enter a name and optional description.

## File modeling

The **File Editor** only allows a file to be renamed or uploaded and the **Metadata** contains the properties related to the file, such as its mimetype.

Once a file has been uploaded and given a name, it can be used in a process definition as a [process variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type `file`. 

## Actions

The actions that can be run against a file are:

| Action | Description |
| ------ | ----------- |
| Download file | Download the file. |
| Validate | Run validation against the file. Any errors can be seen in the log history at the bottom of the Modeling Application and are flagged in a pop-up box. |
| Save | Save any changes made to the file. |
| Delete | Delete the file. |
---
title: Forms
---

Forms are used to capture data into specially designed field types such as text, date, file uploads and multiple choice radio buttons. They are where human intervention is required within a process and this intervention is handled by filling in a form that is displayed in a user’s task list.

Forms can be used in three different ways:

* As part of a [user task]({% link process-automation/latest/model/processes/bpmn.md %}#user-task) that will create a task for an assigned user, or group of users when the process flow reaches that element.

* As part of a [start event]({% link process-automation/latest/model/processes/bpmn.md %}#start-events) used at the beginning of a process instance. Forms behave in the same way as when they are linked to a user task, however forms linked to start events cannot be saved part way through filling them in.

* As standalone tasks where the form can be used in a task that is not associated to any process.

Forms can also be based on [content models]({% link process-automation/latest/model/content-models.md %}) allowing content metadata to be updated within a form and subsequently managed in a process using the [content connector]({% link process-automation/latest/model/connectors/content.md %}).

## Properties

The basic properties of a form are:

| Property | Description |
| -------- | ----------- |
| Form name | *Required.* The name of the form. Must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example `claims-form`. |
| Form description | *Optional.* A description of what the form should be used for, for example `A form to collect the details of any claims.`. |

Two additional properties can be set for a form when no form field is selected:

| Property | Description |
| -------- | ----------- |
| Allow form to be used in standalone tasks | Set whether the form can be used in standalone tasks or not. Standalone tasks are tasks not associated with a process instance. |
| Update form files metadata from fields on submit | If set to `true`, when the form is submitted and it contains files in an [attach file field](#attach-file-fields) that have been sourced from Content Services, the metadata for those files will be updated with the values entered into any other fields on the form. |
| Set left label for fields | Set all field labels to appear on the left side instead of at the top of the field. |
| Edit form rules | You can create custom form rules that apply to a form or to the widgets on a form. Form rules are created and run by a user of the form. Each form rule has an event trigger, event conditions, and actions. |

## Create a form

To create a form:

1. Sign into the Modeling Application and open a project.

2. Click the **NEW** dropdown.

3. Select how to create the form:

    * **Create > Form** creates a new, empty form.

    * **Upload > Form** allows for uploading an existing form `.json` file into the Modeling Application.

    Alternatively use the **+** or **Upload** buttons next to **Forms** in the left-hand menu.

4. Enter a name and optional description.

5. (Optional) If the form is going to be used to manage content metadata, check the **Create initial form content from a content model** box.

6. (Optional) Choose which custom type and custom aspects should be used in the form and whether inherited properties should be included. The list will be generated from the [content models]({% link process-automation/latest/model/content-models.md %}) available to the project the form is created in.

> **Note**: Creating a form based on a content model will automatically create form fields for the properties included in the selected custom type and aspects. These fields will retain any constraints set for them in their content model, such as regular expressions. An [attach file field](#attach-file-fields) will also be added with the label `nodes` for attaching content to the form.

## Form modeling

The Modeling Application contains two tabs for creating and editing forms.

### Form Editor

The **Form Editor** is the GUI for modeling forms by dragging and dropping form fields from the palette onto the form designer. The palette contains all of the [form field](#form-fields) types that can be used to model a form. The **Form Editor** also has the ability to create multiple tabs and rows, as well as create custom outcomes.

#### Tabs

Tabs can be used to logically separate the content of a form into different sections. Use the **Add tab** button to create additional tabs and set a name that will appear to users at runtime. [Visibility conditions](#visibility-conditions) can also be set on each tab to show or hide them based on values entered into the form.

### Rows

Each row of form fields can be split into a number of columns; 1, 2, 3, 4, 6, 12. To change the number of columns within a row select the row object that contains the fields and use the dropdown.

#### Outcomes

Outcomes are custom buttons that can be added for users to click to complete a form, for example `Agree` and `Disagree`. Use the **Add outcome** button to add additional outcomes.

### JSON Editor

The **JSON Editor** contains the JSON that describes the form. Changes made in the **Form Editor** or in the **JSON Editor** are reflected in the other. When importing or downloading a form the `.JSON` file will reflect what is in the **JSON Editor**.

## Form fields

All form fields display a field editor when they are created in the GUI. Each field has a tab for general properties that are common amongst the majority of form fields, with some also having a tab for advanced properties that are specific to that field type.

The general properties of form fields are:

| Property | Description |
| -------- | ----------- |
| Label | The name of the field that will appear on the rendered form, for example `First name`. |
| ID | The unique ID of the field, for example `Text070upd`. |
| Required? | Checking this box makes a field mandatory. |
| Read-only | Sets whether the field can be filled in by a form filler or not. |
| Colspan | The number of columns a field spans. This is limited by the number of columns within the [row](#rows). |
| Placeholder | The default value of the field. |
| Tooltip | Tooltip information that will appear on the rendered form field providing help text to a form filler. |

> **Note**: Any exceptions to the general properties are stated in the section specific to that field type. For example, the header field type does not have the `Required?` property.

Each form field can also have a set of visibility conditions set on it where the field will either be hidden or displayed depending upon the values of other fields or variables within that form. The **Edit Visibility Conditions** button is displayed in the properties of every field.

The steps of visibility conditions are:

| Step | Description | Options |
| ---- | ----------- | ------- |
| Depends on | The field or variable that will be evaluated | A field or variable within the form. |
| If it's | The comparison operator between **Depends on** and **Value** | `equal to`, `not equal to`, `empty`, `not empty`. |
| Value | The value, field or variable that the **Depends on** step is evaluating against | A field or variable within the form or a static value. |
| Next condition operator | The operator for evaluating against further conditions | `and`, `and not`, `or`, `or not`. |

> **Note**: Conditions are evaluated in the order they are declared.

### Amount fields

Amount fields are for entering a value depicting currency.

The advanced properties for an amount field are:

| Property | Description |
| -------- | ----------- |
| Min value | Sets the minimum value that can be entered into the field. |
| Max value | Sets the maximum value that can be entered into the field. |
| Currency | Sets the currency symbol for the field, for example `$`, `£` or `€`. |
| Enable decimals | Checking this box will allow for decimal places to be entered into the field. |

### Attach file fields

Attach file fields are used so that form fillers can upload files with their submission.

The advanced properties for an attach file field are:

| Property | Description |
| -------- | ----------- |
| Allow multiple file attachments | Checking this box will allow for more than one file to be uploaded. |
| File source | Sets the location for where files can be uploaded from. `Alfresco Content` is from a Content Services instance, whilst `Alfresco Content and Local` allows uploads from Content Services and a form filler's local machine. |
| Destination folder path | If you select `Static path` the location where files uploaded from a local machine should be stored in Alfresco Content Services, composed of an alias and a relative path. For example, `-root-/User Homes/hruser` or `-my-` will both store the files in `/Company Home/User Homes/hruser`. You can also determine how files are uploaded by setting the destination upload path dynamically by selecting either option A: `Based on string variable type` or option B: `Based on folder variable type`.|
| Display show file option | Checking this box will allow the form filler to view uploaded files. |
| Display download file option | Checking this box will allow the form filler to download any uploaded files. |
| Display retrieve metadata option | Checking this box will allow the form filler to view the metadata of uploaded files. |
| Display remove file option | Checking this box will allow the form filler to remove uploaded files from the form. |
| Content Properties to display | You can select up to two custom properties to display next to the file name. |
| Display upload new version option | Checking this box allows the **Upload new version** option to display in the Digital Workspace, when you click the three dots next to a file. If you upload a new version of a file you can indicate if the changes are minor or major, and you can write a comment about what the changes are or why the changes were made. |

> **Important**: Users filling in a form with an attach file field need to be given explicit access to the upload directory if it is outside of the [default storage location]({% link process-automation/latest/admin/release.md %}#deploy-steps/storage) for the application.

### Checkbox fields

Checkbox fields are `boolean` values. They are either checked or unchecked.

Checkbox fields do not have the `Placeholder` property, nor do they have an advanced properties tab.

### Date fields

Date fields are for `date` type data.

The advanced properties for a date field are:

| Property | Description |
| -------- | ----------- |
| Default value | Sets the default date of the field. If you want the default date to be 'today' and that is the current day then you can select the **Today** checkbox. |
| Set dynamic date range | When turned on you can enter a **Minimum** and **Maximum** date range. This forces the date picker to only allow a user to select a date within the configured period, and any dates outside of the date range will be grayed out. **Note:** When using dynamic date range, the **Min Date** and **Max Date** fields are unavailable. |
| Min date | Sets the earliest date that can be entered into the field. |
| Max date | Sets the latest date that can be entered into the field. |
| Date format | Sets the format of how a date is entered into the field. For example: `YYYY-MM-DD` would display as `2001-10-01` for 1st October, 2001. |

### Display text fields

Display text fields allow the form designer to display a line of fixed text to the form filler. This text is not editable by the filler themselves. The `Text to display` property is used to enter the text.

Display text fields do not have the `Read-only`, `Placeholder`, and `Required?` fields, nor do they have an advanced properties tab.

### Display Rich text

Display Rich text allows you to add HTML formatted text to forms. You can test how the text will look at design time by using the preview button, before pushing the form to a live environment. The Display Rich text editor includes standard formatting tools such as headings, font color, hyperlinks, and code blocks.

> **Note:** Once created the form only displays read-only text and does not capture any values.

![payslip]({% link process-automation/images/payslip.png %})

### Display value fields

Display value fields allow the form designer to display a value previously entered in the form. The `variables` property is used to select a [form variable](#form-variables) to display.

Display value fields do not have the `Read-only`, `Placeholder`, and `Required?` fields, nor do they have an advanced properties tab.

### Dropdown fields

Dropdown fields allow the form designer to define a set of options that a form filler must choose from a list.

When you use dropdown fields in Process Automation, you can enter any character of the item you are searching for to limit the amount of returned entries. This includes any part of a sentence. This feature works when there are more than five entries and is useful when your lists are large.

You can select single or multiple entries from a dropdown list to use them further in your process.

When designing a dropdown list in the modeling application, the list items can be:

* [Entered manually]({% link process-automation/latest/model/forms.md %}#manual-dropdown-fields)
* [Read from a REST service]({% link process-automation/latest/model/forms.md %}#rest-service-dropdown-fields)
* [Populated from a JSON type Variable]({% link process-automation/latest/model/forms.md %}#variable-dropdown-fields)

#### Manual dropdown fields

The advanced properties for a manual dropdown field allow for a set of options to be entered with a `name` and `id` for each option set. Selecting the radio button next to an option will set it as the `empty value`. An empty value is taken to mean the field is empty if this option is selected when the form is filled in.

#### REST Service dropdown fields

The advanced properties for a **REST Service** dropdown field are:

| Property | Description |
| -------- | ----------- |
| Authentication | The authentication type. |
| REST URL | The URL of the REST service. |
| Path to array in JSON response | The path to the JSON response. Enter `.` to use the full path. |
| ID property | The ID of the REST service. |
| Label property | The name of the REST service. |
| Conditional | Turn this option on if you would like to link your dropdown widget with another dropdown widget and to create a conditional relationship between them. For example, if you select a country from one dropdown widget, the second dropdown widget will only show cities from that country. |
| Depends on | Select which other dropdown widget you would like to connect with. |
| If equal | Select which child entry of the **Depends on** field you want to work with and add subordinate entries for it. |

#### Variable dropdown fields

The following is an example of a Form Variable in JSON format:

```json
{
  "response": {
    "data": {
      "available_cars":
        [
          {
            "car_id": 1,
            "car_name": "Ferrari 458",
            "car_price": "500000"
          },
          {
            "car_id": 2,
            "car_name": "Lamborghini Urus",
            "car_price": "150000"
          }
        ]
    },
    "pagination": {
      "maxItems": 100
    }
  }
}
```

> **Note**: You must create a JSON type Form Variable, not a Process Variable, prior to configuring a dropdown field to use it. If no such Variable exists, the only selectable option available when configuring the dropdown field is: **No form variable (JSON)**.

The advanced properties for a **Variable** dropdown field are:

| Property | Description |
| -------- | ----------- |
| Form variable (JSON) | Form Variable to be used by the runtime application to populate the dropdown options. |
| Path to array in JSON | Path where the dropdown option data is located, for example: `response.data.available_cars`. |
| ID property | Informs the runtime application which element in the variable value is to be used as an ID for each dropdown option. This value is used as a payload when the user selects a dropdown option. For example: `car_id`. |
| Label property | Informs the runtime application which element in the variable value is to be used as the label for each dropdown option. This is what the user sees in the dropdown list when selecting it. For example: `car_name`. |

The modeling application also supports JSON variables structured according to a default configuration. Provided that the data in the JSON type Form Variable has the proper structure, the data is displayed correctly in the dropdown field without needing to specify the path, ID, and label values at the modeling level. The default configuration is the following:

| Property | Default |
| -------- | ------- |
| path | `data` |
| ID | `id` |
| label | `name` |

The following is an example of a JSON variable with this structure:

```json
{
    "data": [
        {
            "id": "default-pet-1",
            "name": "Dog"
        },
        {
            "id": "default-pet-2",
            "name": "Cat"
        },
        {
            "id": "default-pet-3",
            "name": "Parrot"
        }
    ]
}
```

#### Creating a conditional relationship between dropdown lists

To create a conditional relationship between two dropdown lists using Country and City as an example:

1. Add two dropdown widgets to your form.

2. Name one of them Country and the other one City.

3. Select the City dropdown widget and click the **Advanced** tab.

4. Select **Manual** and turn on the **Conditional** field.

    **Note:** You can only have the following relationships: manual parent and manual child, manual parent and REST child, REST parent and REST child.

5. Select Country from the **Depends on** dropdown list.

6. Select the Country dropdown widget and click the **Advanced** tab.

7. Add a name for the label and then add all the Countries using the **Add option** field.

8. Select the City dropdown widget again and click the **Advanced** tab.

9. From the **If equal** dropdown list select the Country you want to work with and then add all the cities you would like available in the dropdown list.

**Note:** You can link as many dropdown fields as you want.

When using a **REST Service** you can use the ID of the linked widget in the REST URL. For example, if your URL is `https://mydomain.com/get-cities/country=${Country}` the value inside `${}` is the ID of the linked widget. If my widget had an ID called `my-dropdown` your URL would be `https://mydomain.com/get-cities/country=${my-dropdown}`.
The `${my-dropdown-id}` can be used in any position of the URL, for example you can also use `https://mydomain.com/country=${Country}/get-cities`. When authentication is required for the REST service you can select the authentication type from the Authentication dropdown list. For how to create authentication types see, [Authentication]({% link process-automation/latest/model/authentication.md %}).

### File viewer fields

File viewer fields display the content uploaded from an [attach file field](#attach-file-fields).

File viewer fields do not have the `Placeholder` or `Tooltip` properties.

The advanced properties for a file viewer field are:

| Property | Description |
| -------- | ----------- |
| Linked attach file widget | Sets which attach file field should be displayed. |

### Group fields

Group fields allow form fillers to select a single or multiple groups from the list of groups available in the application.

Group fields do not have a `Placeholder` property.

The advanced properties for a group field are:

| Property | Description |
| -------- | ----------- |
| Mode | Sets whether only a single, or multiple groups can be selected. |

### Headers

Header fields are subtitle fields that can be used as section containers on a tab. They cannot be filled in by a form filler as they only display a subtitle.

Header fields have a `Number of columns` property rather than the `Colspan` property and they do not have the `Read-only`, `Placeholder`, `Tooltip` and `Required?` properties.

The advanced properties for a header field are:

| Property | Description |
| -------- | ----------- |
| Allow collapse | Checking this box allows the header container to be collapsed with a `+` or `-` when the form is filled in. |
| Collapse by default | Checking this box will load the form with the header section already collapsed. This property is only available if the `Allow collapse` property is checked. |

### Hyperlink fields

Hyperlink fields allow the form designer to expose a link that form fillers can click on whilst they are filling out a form.

Hyperlink fields do not have the `Read-only` and `Placeholder` properties.

The advanced properties for a hyperlink field are:

| Property | Description |
| -------- | ----------- |
| Hyperlink URL | The URL that the field will launch when clicked. |
| Display text | The text that is displayed for the URL, for example `Click here to view the expenses policy`. |

### Multiline text fields

Multiline text fields are for entering `string` data across multiple lines.

The advanced properties for a multiline text field are:

| Property | Description |
| -------- | ----------- |
| Min length | Sets the minimum character count for text that can be entered into the field including whitespace. |
| Max length | Sets the maximum character count for text that can be entered into the field including whitespace. |
| Regex pattern | A regular expression can be entered that will validate the text entered into the field. For example, a regular expression that matches four letters followed by four digits would be `/^[A-Za-z]{4}\d{4}$/`. |

### Number fields

Number fields are for entering `integer` data.

The advanced properties for a number field are:

| Property | Description |
| -------- | ----------- |
| Min value | Sets the minimum `integer` value that can be entered into the field. |
| Max value | Sets the maximum `integer` value that can be entered into the field. |

### People fields

People fields allow form fillers to select a single or multiple users from the list of users that have access to the application.

People fields do not have a `Placeholder` property.

The advanced properties for a people field are:

| Property | Description |
| -------- | ----------- |
| Mode | Sets whether only a single, or multiple users can be selected. |
| Select the logged user as default user | Select when you want the logged in user to be pre-populated in the people widget. |
| Groups Restriction | Specify a group or groups of users who are permitted to display in a widget at runtime. If multiple groups are added, the users must belong to all groups in order to be displayed in a widget at runtime. |

### Radio buttons

Radio button fields allow the form designer to define a set of options a form filler must choose from. This list can be a manually entered set of options or it can read from a REST service.

The advanced properties for a manual radio button field allow for a set of options to be entered with a `name` and `id` for each option set. You can change the position of the radio buttons by dragging them into the order you want them to appear. You can also set if you want your radio buttons aligned vertically or horizontally.

The advanced properties for a REST radio button field are:

| Property | Description |
| -------- | ----------- |
| Authentication | The authentication type. |
| REST URL | The URL of the REST service. |
| Path to array in JSON response | The path to the JSON response. Enter `.` to use the full path. |
| ID property | The ID of the REST service. |
| Label property | The name of the REST service. |

When authentication is required for the REST service you can select the authentication type from the Authentication dropdown list. For how to create authentication types see, [Authentication]({% link process-automation/latest/model/authentication.md %}).

### Text fields

Text fields are for entering `string` data in a single line.

The advanced properties for a text field are:

| Property | Description |
| -------- | ----------- |
| Min length | Sets the minimum character count for text that can be entered into the field including whitespace. |
| Max length | Sets the maximum character count for text that can be entered into the field including whitespace. |
| Regex pattern | A regular expression can be entered that will validate the text entered into the field. For example, a regular expression that matches four letters followed by four digits would be `/^[A-Za-z]{4}\d{4}$/`. |
| Input mask | Set the format for how data may be entered into the field. For example `(00) 0000-0000` for a mandatory 8-digit phone number and 2-digit area code will not allow for letters to be entered at all. |
| Reversed | This reverses the entry for an `Input mask` and reads the text from right to left instead. |
| Input mask placeholder | The placeholder to demonstrate the format of an `Input mask`. For example `(__) ____-____` in the phone number example. |

### Metadata viewer

The Metadata viewer can be used to view the metadata of any file you upload or attach to your GUI using the Attach file widget.  

To create a form that contains the Metadata viewer:

1. Create or edit an existing form, for more see [Create a form](#create-a-form).

2. Add the Attach file widget to the form.

3. Add the Metadata viewer widget to the form.

4. Select the **Advanced** tab of the Metadata viewer widget on the **Field Editor** pane.

5. From the **Linked attach file widget** dropdown menu select the Attach file widget you want to link with the Metadata viewer.

   You can add more than one Attach file widget and Metadata viewer widgets to a single form.

The advanced properties for the Metadata viewer are:

| Property | Description |
| -------- | ----------- |
| Expanded | Select the check box to enable the properties viewer to display all of the properties groups and not just the default properties. |
| Display default properties | Select the check box if you want to display the default properties. |
| Display empty | Select the check box to allow the display of empty values in the card view. |
| Editable | Select the check box to display the metadata in an editable view where it can be updated. |
| Multi | Select the check box to allow more than one properties group to be expanded at the same time. |
| Copy to clipboard on click | Select the check box to allow the value of a property to be copied to the clipboard when it is clicked. |
| Use chips for multi-value properties | Select the check box to allow the display of multi-value properties as chips. |
| Display aspect | Select the Aspect you wish to display as an expanded card. |
| Preset | The name or configuration of the the metadata preset. Click the preset button to configure the metadata you would like visible in your GUI, for more on presets see [Application config presets](https://www.alfresco.com/abn/adf/docs/content-services/components/content-metadata-card.component/#application-config-presets){:target="_blank"}. |

### Data Table

The Data Table can be used to display data in a table.

To create a form that contains the Data Table:

1. Create or edit an existing form, for more see [Create a form](#create-a-form).

2. Add the Data Table widget to the form.

The advanced properties for the Data Table are:

| Property | Description |
| -------- | ----------- |
| Rowspan | The number of rows a field spans. |
| Form variable (JSON) | Displays a drop-down list of all available JSON type form variables. These variables can be used by the application to populate the data table. If there are no JSON variables, the list is empty. You can create one, following instructions in [Create a form variable](#create-a-form-variable). |
| Path to array in JSON | Configuration of the path where the fetched data belongs. Each nested object is added using a dot as a separator. |

The following Data Table types are available: text, number, amount, date, boolean, json, and icon.

You can define additional properties for:

| Property | Type | Description |
| -------- | ----------- | ----------- |
| locale | number, amount, date | Language code in ICU format, for example en_US. It impacts the format of the shown data, such as dates. |
| digitsInfo | number, amount, date | Decimal places, according to the Angular Decimal Pipe. |
| decimalConfig | number | Configuration of the displayed decimal number, including properties: locale and digitsInfo. |
| currencyConfig | amount | Configuration of the displayed currency, including properties: locale (currency formatting), digitsInfo, code (currency code, such as USD or EUR), display (currency symbol, such as $ or €). |
| dateConfig | date | Configuration of the displayed date, including properties: locale (date formatting), format (selection of pre-defined Angular Date Pipe formats), tooltipFormat (formatting of the displayed tooltip). |

You can edit the schema definition, using the Edit Schema Definition under the Data Table properties pane. The column schema definition is used to specify how the table is displayed in detail, including the column header (title) or sorting. The schema is edited in the JSON editor.

The following is an example of a schema definition:

```json
[
    {
        "type": "number",
        "key": "id",
        "title": "No",
        "sortable": true,
        "draggable": true
    },
    {
        "type": "date",
        "key": "creation_date",
        "title": "Creation date",
        "sortable": true,
        "draggable": true,
        "dateConfig": {
            "locale": "en-GB",
            "format": "full",
            "tooltipFormat": ""
        }
    },
    {
        "type": "number",
        "key": "people",
        "title": "Numbers of interested people",
        "sortable": true,
        "draggable": true,
        "decimalConfig": {
            "digitsInfo": "1.0-0",
            "locale": "pl-PL"
        }
    },
    {
        "type": "amount",
        "key": "cost",
        "title": "Cost of maintenance",
        "sortable": true,
        "draggable": true,
        "currencyConfig": {
            "code": "EUR",
            "digitsInfo": "2.2-2",
            "display": "€",
            "locale": "de-DE"
        }
    }
]
```

## Custom form widgets

Form widgets provide the ability to add custom form fields into a form. There are two stages to including a custom form field in a project:

* Create a custom form widget within the Modeling Application and use it within a form.
* [Develop]({% link process-automation/latest/develop/index.md %}) a custom user interface or extend the Digital Workspace to include the logic for the form widget using the [Application Development Framework (ADF)](https://www.alfresco.com/abn/adf/docs/){:target="_blank"}.

### Custom form widget properties

The basic properties of a form widget are:

| Property | Description |
| -------- | ----------- |
| Form widget name | *Required.* The name of the form widget. Must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example `custom-field`. |
| Value type | *Required.* The type the field will be treated as when mapping it to [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables), for example a Boolean form widget can only map to a process variable of type boolean. |
| Icon | *Required.* An SVG image for the field icon. |
| Form description | *Optional.* A description of what the field does. |

> **Note**: The recommendation is to use the value type of `JSON` to create complex custom form widgets.

### Create a custom form widget

To create a custom form widget in the Modeling Application:

1. Sign into the Modeling Application and open a project.

2. Click the **NEW** dropdown.

3. Select how to create the form widget:

    * **Create > Form Widget** creates a new, empty form widget.

    * **Upload > Form Widget** allows for uploading an existing form widget `.JSON` file into the Modeling Application.

    Alternatively use the **+** or **Upload** buttons next to **Form Widgets** in the left-hand menu.

4. Enter a name and optional description.

5. Select the value type for the form widget and upload an icon for it in the form field palette.

Once a custom form widget has been created in a project, it will appear in the palette when designing a form under the ellipsis header.

### Develop a custom form widget

See the [developer section]({% link process-automation/latest/develop/index.md %}#custom-form-fields) for details on how to develop the custom form widget behavior and how to include it in a custom user interface.

## Form variables

Form variables can be used to pass and receive values from [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables). They can be used to set the [visibility conditions](#visibility-conditions) of form fields and to [display values](#display-value-fields) to form fillers.

### Form variable properties

The properties for a form variable are:

| Property | Description |
| -------- | ----------- |
| name | A unique name that can contain alphanumeric characters and underscores but must begin with a letter, for example `var_3`. |
| type | A data type selected from a dropdown. See the following table for a list of data types, for example `String`. |
| required | Sets whether the form variable must contain a value when the task is started, for example `false`. |
| value | An optional default value for the form variable, for example `ice-cream`. |

The data types that a form variable can be set as are:

| Type | Description |
| ---- | ----------- |
| String | A sequence of characters, for example `#Mint-Ice-Cream-4!`. |
| Integer | A positive whole number, for example `642`. |
| Boolean | A value of either `true` or `false`. |
| Date | A specific date in the format `YYYY-MM-DD`, for example `2020-04-22`. |
| Datetime | A specific date and time in the format `YYYY-MM-DD HH:mm:ss`, for example `2020-09-10 22:30:00`. |
| File | A [file]({% link process-automation/latest/model/files.md %}) uploaded into a process definition or as part of a process instance or task. |
| JSON | A JSON object, for example `{"flavor" : "caramel"}`. |
| Folder | A folder object described as JSON, for example `"name": "mint-folder"`. |
| Array | A comma separated list of entries, for example `mint, strawberry, vanilla` that will be formatted to `["mint","strawberry","vanilla"]`. |

### Create a form variable

To create a form variable:

1. Select the project and form to create a form variable in, within the Modeling Application.

2. Select the **Edit Form Variables** button by clicking on a blank section of the canvas.

3. Use the **+** symbol to add new variables and enter a name, type, optional value and select whether it is required or not.

## Actions

The actions that can be run against a form are:

| Action | Description |
| ------ | ----------- |
| Download form | Download the JSON for the form. |
| Validate | Run validation against the form. Any errors can be seen in the log history at the bottom of the Modeling Application and are flagged in a pop-up box. |
| Save | Save any changes made to the form. |
| Delete | Delete the form. |

## Form rules

Form rules can be used to populate one field depending on the response given by a user in another field. In the example described here you create a form rule called **how_to_address** that has two fields on it, the first is called **Gender** and the second is called **Title**. The first field is a dropdown list and contains the options **Man**, **Woman**, and **Other**. If **Woman** is selected then the second field is automatically populated with **Ms**. The form rule ensures that any interaction with the form will contain consistent responses. This is a simple example and your form rules could be more involved.

These instructions are in two parts. You first create a form, and then second create the form rules.

> **Note:** Form rules are specific to your installation and configuration.

### Create the form

First you must create a form that can be used to configure the form rule:

1. Sign into the Modeling Application and open a Project, click the three dots next to **Forms** and then select the **+** icon.

    > **Note:** You are able to upload already created forms by using the **Upload** button. Any form you upload must be written in the JSON format.

2. Enter a name for the form and then click **Create**.

    In this example the form is called **how-to-address**.

3. Add a [Dropdown](#dropdown-fields) widget with the following configuration:

    * **Label** called Gender
    * **ID** called genderID
    * Three options with **Male**, **Female**, and **Other** as their IDs and Labels.

4. Add a [display value field](#display-value-fields) widget with the following configuration:

    * **Label** called Title
    * **ID** called titleID

5. Select the form again by clicking the area above the word **outcome**, see screen shot.

    ![Form editor]({% link process-automation/images/form-editor.png %})

6. In the **Form Editor** pane click **Edit Form Variables**.

7. Click the **+** icon and create a new variable with the name **title**.

8. From the **Type** dropdown list select **Primitives** and then **string**, and then click **Update**.

9. Select the **Display value** widget, and from the **Field Editor** pane select the **title** variable from the **Variables** dropdown list.

You have created a form where you can create form rules.

### Create form rules within the form  

To create form rules within the form:

1. Select the form again by clicking the area above the word **outcome** and then click **Edit form rules**.

2. Click the green **+** icon to create a new rule.

3. From the **Event source** dropdown list click **Form events** and select **Form loaded**.

4. Click the **+** icon next to **Actions** to create a new action.

5. From the **Action type** dropdown list click **Update variable** and select **Title**.

    You are selecting the display value widget you created earlier.

6. Click the **Edit** button next to the **Event output** dropdown list that is under the **Event output/Value** heading.

7. Select **Value** from the right hand side and enter a value in the **Value** field, for example *Select your gender*, and then click **Update**.

    This message will appear in the blank field of the display value widget before a user has selected their gender from the **Gender** dropdown list.

8. Click the green **+** icon again to create a new rule.

9. From the **Event source** dropdown list click **Field events** and then Click **Gender** and select **Gender - field value changes**.

10. Click the **+** icon next to **Condition** to create a new condition.

11. Select **Gender** from underneath the **title (Form fields)** heading.

12. Select **Equals** and then **Value** from the top right.

13. Enter **Female** into the **Value** field and then click **Save**.  

14. Click the green **+** icon next to **Actions** to create a new action.

15. From the **Action type** dropdown list click **Update variable** and select **Title**.

16. Click the **Edit** button next to the **Event output** dropdown list which is under the **Event output/Value** heading.

17. Select **Value** from the right hand side and enter a value, for example **Ms** and then click **Update**.

    You are configuring the form to display **Ms** in the **Title** display value field widget when a user selects **Female** from the **Gender** dropdown list.  

18. Create a **Gender - fieldValueChanged** form rule for each of the options within your dropdown list. In this example you would create another one for **Male**, and another one for **Other**.

    > **Note:** You must create a **Gender - fieldValueChanged** form rule for each of the elements in your dropdown list.

19. When you have created the relevant form rules click **Save**.

20. Select **Preview** from the **Eye** icon dropdown list and test the responses in the form are correct.  

## Change preview size

You can change the size of the form you want to preview. This is useful because the form size can simulate the different sizes of the devices that will be using the form. You can customize the size of the form or select which device you want to emulate.

To change the size of the preview select **Preview** from the **Eye** icon dropdown list and select how you want to preview your form.

![Form size]({% link process-automation/images/form-size.png %})---
title: Modeling overview
---

Modeling is used to create the templates for automating content-based business processes.

## Modeling Application

The Modeling Application is where all models are created and edited. They are stored in projects that can be [deployed by the Admin Application]({% link process-automation/latest/admin/release.md %}#deployment) when the templates are complete.

The Modeling Application is accessed using the `/modeling` URL, for example `https://alfresco.com/modeling`.

## Models

Models are the components that make up a [project]({% link process-automation/latest/model/projects.md %}). The types of model available to use within a project are:

* [Processes]({% link process-automation/latest/model/processes/index.md %}) are the collection of components that are used to build and represent business processes using [BPMN 2.0 specification](https://www.omg.org/spec/BPMN/2.0/){:target="_blank"}.
* [Forms]({% link process-automation/latest/model/forms.md %}) are used to capture data into specially designed field types such as text, date, file uploads and multiple choice radio buttons. They are filled in by users of an application.
* [Authentications]({% link process-automation/latest/model/authentication.md %}) are used when your system requires access to external REST services.
* [Connectors]({% link process-automation/latest/model/connectors/index.md %}) are used to handle interactions with external systems as part of a process. This includes actions such as retrieving, generating, updating and storing content in the Content Services repository, sending emails and utilizing services such as AWS Comprehend, Textract, Rekognition and Lambda functions.
* [Decision tables]({% link process-automation/latest/model/decisions.md %}) are used to manage business decisions within process workflows.
* [User interfaces]({% link process-automation/latest/model/interfaces.md %}) set the end user interface for users to interact with content, tasks and processes for the project.
* [Files]({% link process-automation/latest/model/files.md %}) are a collection of files that can be used within the application. A file can be an image or a script.
* [Scripts]({% link process-automation/latest/model/scripts.md %}) are used to execute a custom script as part of a process
* [Triggers]({% link process-automation/latest/model/triggers.md %}) are used to define a set of event criteria. When the event criteria specified in the trigger is met, the event is published and an action containing a payload is kicked off.
* [Content models]({% link process-automation/latest/model/content-models.md %}) describe how data should be stored in the repository and the metadata that can be associated to the content and folders within that model.
* [Data models]({% link process-automation/latest/model/data-models.md %}) allow you to describe objects your application is handling. You can define the standard data structure you will use in your application using JSON schema.
---
title: User interfaces
---

The user interfaces (UI) section sets an end user interface for users to interact with content, tasks, and processes for the project using [Alfresco Digital Workspace]({% link process-automation/latest/using/index.md %}).

## Properties

The basic properties of a UI are:

| Property | Description |
| -------- | ----------- |
| UI name | *Required.* The name of the interface. Must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example `order-template`. |
| Content and Process | *Required.* Select **Content** to force all the widgets in the Digital Workspace that refer to content, processes, and tasks to be displayed. Select **Process** when you want only the widgets that refer to processes, and tasks to be displayed. Additionally if **Process** is selected then the landing page can be configured that allows the user who runs the application to be redirected to the list of running processes, or to their list of My Tasks. |
| UI description | *Optional.* A description of what the interface should be used for, for example `A template for orders to follow.` |
| Default System Logo | *Optional.* The default system logo image. The recommended size for the logo is 28x28 px. **Note:** To set a new logo the file must be uploaded in advance with the visibility flag set to public, for more see [Files]({% link process-automation/latest/model/files.md %}). |
| Application title | *Optional.* The name of the application. This is the name that will appear in the header and on the tab of your browser. |
| Header text color HEX code | *Optional.* The color of the header text on the user interface using hexadecimal numbers. For example `#b39eba`. |
| Header color HEX code | *Optional.* The color of the header background on the user interface using hexadecimal numbers. For example `#b39oba`. |
| Default Background Header Image | *Optional.* The default background header image.  **Note:** To set a new background image the file must be uploaded in advance with the visibility flag set to public, for more see [Files]({% link process-automation/latest/model/files.md %}). |

## Create default UI

To create a default UI:

1. Sign in to the Modeling Application and open a project.

2. Click the three dots next to **UI** and then select **Create Default UI**.

3. Enter a name and optional description.

4. Click **Create UI**.  

## Upload default UI

The UI definition is normally created using the [create default UI tool](#create-default-ui) and downloaded as a JSON file by clicking **Download UI**. You can follow the steps in this section to reuse a default UI definition in another project or UI.

> **Note**: To upload a custom UI, follow the steps in [Create custom UI](#create-custom-ui) instead.

To upload a default UI definition:

1. Sign in to the Modeling Application and open a project.

2. Click the three dots next to **UI** and then select **Upload**.

3. Select the JSON file that contains the UI definition.

## Create custom UI

You can create a custom UI outside of the Modeling Application. The custom UI can be an Application Development Framework (ADF) application. It can also be any single page application, such as React or Vanilla HTML, CSS, or JavaScript, that conforms to the UI schema. To verify this, upload your JSON definition and click the **Validate UI** button.

> **Important:** Before uploading your custom UI, ensure that it has a valid application entry point in either an `index.html` or `index.htm` file. The custom UI must be contained in a zip archive with the `index.html` or `index.htm` file at its root. The archive size cannot exceed 50 mb.

> **Note**: ADF comes with a JavaScript library for managing bearer token authentication handling and renewal, which solution builders using other Custom UI implementations will have to manage.

To create a custom UI:

1. Sign in to the Modeling Application and open a project.

2. Click the three dots next to **UI** and then select **Create custom UI**.

3. Enter a name and optional description.

4. If you do not have a customized zip file yet, select **Generate from Template** to generate a custom UI from a UI template, which contains the source code from the Workspace application. The template zip file can be then downloaded and customized in a different application.

5. Once you have a zip file with custom UI, click the **Upload** button and select the zip file that contains your Custom UI.

## Theme

You can add a theme to the Digital Workspace.

### Use the Modeling Application to change the theme

To change the theme using the **UI** properties in the Modeling Application.  

1. Sign in to the Modeling Application.

2. Select the **UI** you want to change and enter the new configuration properties under the **Theme** heading.

    > **Note:** You can only change the **Theme** of the **Default UI**.

3. Save the **UI**.

The properties of the UI theme are:

> **Note:** See example image below.

| Property | Description |
| ----------- |----------- |
| Primary color | The color is used to highlight important parts of your application, for example the text for the selected link in the left pane. |
| Accent color | The color is used to accent highlight areas of your UI and make parts of it stand out more, for example it can be used for floating action buttons, selection controls such as sliders and switches, highlighting selected text or Progress bars, and some links. |
| Text color | The default text color used for the application. |
| Background color | The color of the background, for example the color of the background of the left pane. |
| Font size | The base font size in pixels. Other font sizes are calculated depending on the base size|
| Font family | The family the font belongs to, for example Cursive. |
| Web font URL | Where the specific information about the font used is gathered from, for [example](https://fonts.googleapis.com/css2?family=Inspiration&display=swap){:target="_blank"}.  |

![ADW Colors]({% link process-automation/images/ADW-colors.png %})

### Deploy the theme

If you are deploying using the Modeling Application or Docker compose you must provide the correct configuration and the theme will be generated at startup.
After updating the properties for the custom theme in the Modeling Application, new entries for the **UI** are added to this file: `"customCssPath": "./assets/theme/custom.css" (i.e. /[app-name]/ui/[ui-name]/assets/theme/custom.css)`

For example:

```javascript
"theme": {
   "primaryColor": "#d92ea8",
   "accentColor": "#2eb7d9",
   "textColor": "#672ed9",
   ```

Once you have deployed your application using the admin app, the values from the the `theme` javascript are used for generating the `custom.css` file. If using Docker compose the `custom.css` file is generated during the Docker startup process. The `custom.css` file is used for altering the application theme and the new theme can be found under the `customCssPath` value.

## User interface modeling

Once a user interface has been created, set the type to `content` to deploy the Digital Workspace with the application. This can be accessed by users once a project has been [deployed]({% link process-automation/latest/admin/release.md %}#deployment) using the format `ui/<name>`, for example `https://alfresco.com/finance-project/ui/content-app`.

> **Note**: An instance of Digital Workspace will be deployed with each application that can only start processes created within that same application. Only users assigned [user access]({% link process-automation/latest/admin/release.md %}#deploy-steps/user) to the application will be able to access the interface.

Custom end user actions can be created for the Digital Workspace. This enables custom options to be added to various menus displayed to users. Rules can be set for the actions to only display on files or folders with specific names, or when an aspect is applied to a node. There are three parts to defining custom actions:

* The [action](#actions) itself that will executed when the option is clicked.
* A list of one or more [rules](#rules) to describe which nodes the action will be displayed on.
* The [feature](#features) the action will be displayed on, for example the header or a context menu.

### Actions

There are four types of end user actions that can be configured:

* [Events](#event) that are used in conjunction with a [trigger]({% link process-automation/latest/model/triggers.md %}) to start a trigger action when clicked by a user.
* [Forms](#form) that display a [form]({% link process-automation/latest/model/forms.md %}) to the user to fill in, independent of a user task or process.
* [Navigation](#navigation) to set a URL to redirect to when clicked by the user.
* [Start process](#start-process) to start a named process when clicked by the user, and optionally include the file the action was launched from when clicked.

#### Event

Event actions are directly referenced by [triggers]({% link process-automation/latest/model/triggers.md %}) when they are clicked. This means that an action can post a predefined message to a Slack channel or send an email notifying an email group about the document.

> **Note:** If a [user interface trigger action]({% link process-automation/latest/model/triggers.md %}#user-interface) is not created that references the event action then nothing will happen when the action is clicked by an end user.

The properties of an event action are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the action. **Note:** This is not the text that will appear to the end user in a menu. |
| Type | *Required.* The type of action will be `Event`. |
| Use selected nodes in action | *Optional.* Sets whether the nodes selected when the action is clicked can be used in the event or not, for example `true`. |

#### Form

Form actions open a [form]({% link process-automation/latest/model/forms.md %}) in Digital Workspace that users can fill in when the action is clicked. The form in question can be completely independent of a process and user task. Forms allow users to enter some information and use the output, for example to use a [trigger]({% link process-automation/latest/model/triggers.md %}#forms) on the form submission event.

The properties of a form action are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the action. **Note:** This is not the text that will appear to the end user in a menu. |
| Type | *Required.* The type of action will be `Form`. |
| Form | *Required.* The name of the form to display when the action is clicked. |
| Use selected nodes in action | *Optional.* Sets whether the nodes selected when the action is clicked can be used in the form or not, for example `true`. |

#### Navigation

Navigation actions open a link when they are clicked by an end user. The link can be relative, for example opening another document from the repository, or the link can be absolute, such as to open another application.

The properties of a navigation action are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the action. **Note:** This is not the text that will appear to the end user in a menu. |
| Type | *Required.* The type of action will be `Navigation`. |
| Target | *Required.* The absolute or relative link the action will direct to, for example `https://wikipedia.org`. |
| Open in new tab | *Optional.* Sets whether the link opens in a new tab or not, for example `false`. |
| Use selected nodes in action | *Optional.* Sets whether the nodes selected when the action is clicked can be used in the navigation URL or not, for example `true`. |

> **Note:** The `Target` can use the variable `${nodes}` if `Use selected nodes in action` is set to `true` to pass the node ID to the link, for example `personal-files/(viewer:view/${nodes})?location=%2Fpersonal-files`.

#### Start process

A start process action will start a process when the action is clicked. If the selected process contains a form on the [start event]({% link process-automation/latest/model/processes/bpmn.md %}#start-events) with an [attach file field]({% link process-automation/latest/model/forms.md %}#attach-file-fields) and `Use selected nodes in action` is set to `true`, then the file that was selected when the action was clicked will be attached to it automatically.

The properties of a start process action are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the action. **Note:** This is not the text that will appear to the end user in a menu. |
| Type | *Required.* The type of action will be `Start process`. |
| Process | *Required.* The name of the process to start when the action is clicked. |
| Use selected nodes in action | *Optional.* Sets whether the nodes selected when the action is clicked can be used in the process or not, for example `true`. |

### Rules

Rules are used to define when an action is displayed to the end user. This is achieved using a series of evaluators, operators and optional nested groups.

Rule groups must:

* All be met for the action to display using **Every**.
* At least one met for the action to display using **Some**.
* Must not be met for the action to display using **Not**.

> **Note:** Individual evaluators in a rule can be set to evaluate negatively using the `!` against them. For example, if the evaluator `app.navigation.isTrashCan` is set to evaluate negatively then the user must *not* be in the trashcan for the action to appear.

Some evaluators take additional operators such as `contains`, `equals` or `matches`. For example, the evaluator `selection.currentFolder.name` can use a fully qualified folder name such as `Invoices` or use a regular expression such as `^(I|i)nvoices`.

#### Application evaluators

Application evaluators check a user's permissions on files and folders to set whether action will be displayed.

The application evaluators are:

| Evaluator | Description |
| --------- | ----------- |
| app.selection.canDelete | User has permission to delete selected node(s). |
| app.selection.canDownload | User can download selected node(s). |
| app.selection.notEmpty | At least one node is selected. |
| app.selection.canUnshare | User is able to remove selected node(s) from public sharing. |
| app.selection.canAddFavorite | User can add selected node(s) to favorites. |
| app.selection.canRemoveFavorite | User can remove selected node(s) from favorites. |
| app.selection.first.canUpdate | User has permission to update selected node(s). |
| app.selection.file | A single File node is selected. |
| app.selection.file.canShare | User is able to share the selected file. |
| app.selection.file.isShared | A shared node is selected. |
| app.selection.file.isLocked | File is locked for editing. |
| app.selection.file.isLockOwner | File is locked and current user is the lock owner. |
| app.selection.file.canUploadVersion | User can update file version. |
| app.selection.library | A single Library node is selected. |
| app.selection.isPrivateLibrary | A private Library node is selected. |
| app.selection.hasLibraryRole | The selected Library node has a role property. |
| app.selection.hasNoLibraryRole | The selected Library node has no role property. |
| app.selection.folder | A single Folder node is selected. |
| app.selection.folder.canUpdate | User has permissions to update the selected folder. |
| app.selection.file.canLock | User has permissions to lock file. |
| app.selection.file.canUnlock | User has permissions to unlock file. |
| repository.isQuickShareEnabled | Whether the quick share repository option is enabled or not. |
| canCopyNode | Checks if user can copy selected node. |
| canToggleJoinLibrary | Checks if user can perform 'Join' or 'Cancel Join Request' on a library. |
| canEditFolder | Checks if user can edit the selected folder. |
| isTrashcanItemSelected | Checks if user has trashcan item selected. |
| canViewFile | Checks if user can view the file. |
| canLeaveLibrary | Checks if user can Leave selected library. |
| canToggleSharedLink | Checks if user can toggle shared link mode. |
| canShowInfoDrawer | Checks if user can show Info Drawer for the selected node. |
| canManageFileVersions | Checks if user can manage file versions for the selected node. |
| canManagePermissions | Checks if user can manage permissions for the selected node. |
| canToggleEditOffline | Checks if user can toggle Edit Offline mode for selected node. |
| user.isAdmin | Checks if user is admin. |
| app.canShowLogout | Whether logout action should be present or not. |
| app.isLibraryManager | Checks if user is library manager. |

#### Navigation evaluators

Navigation evaluators use the location within the repository structure to set whether an action will be displayed.

The navigation evaluators are:

| Evaluator | Description |
| --------- | ----------- |
| app.navigation.folder.canCreate | User can create content in the currently opened folder. |
| app.navigation.folder.canUpload | User can upload content to the currently opened folder. |
| app.navigation.isTrashcan | User is using the Trashcan page. |
| app.navigation.isNotTrashcan | Current page is not a Trashcan. |
| app.navigation.isLibraries | User is using a Libraries or Library Search Result page. |
| app.navigation.isNotLibraries | Current page is not a Libraries page. |
| app.navigation.isSharedFiles | User is using the Shared Files page. |
| app.navigation.isNotSharedFiles | Current page is not Shared Files. |
| app.navigation.isFavorites | User is using the Favorites page. |
| app.navigation.isNotFavorites | Current page is not Favorites. |
| app.navigation.isRecentFiles | User is using the Recent Files page. |
| app.navigation.isNotRecentFiles | Current page is not Recent Files. |
| app.navigation.isSearchResults | User is using the Search Results page. |
| app.navigation.isNotSearchResults | Current page is not the Search Results. |
| app.navigation.isSharedPreview | Current page is preview Shared Files. |
| app.navigation.isFavoritesPreview | Current page is preview Favorites. |
| app.navigation.isSharedFileViewer | Current page is shared file preview page. |
| app.navigation.isPreview | Current page is Preview. |
| app.navigation.isPersonalFiles | Current page is Personal Files. |
| app.navigation.isLibraryFiles | Current page is Library Files. |

#### Node property evaluators

Node property evaluators use the types, aspects and properties of folders and files to set whether an action will be displayed.

The node property evaluators are:

| Evaluator | Description |
| --------- | ----------- |
| selection.files.type | All the selected files are of the input type. |
| selection.files.aspect | All the selected files have the input aspect. |
| selection.files.property | All the selected files have the indicated property and their values satisfy the condition. |
| selection.files.name | All the selected files match the condition in their name. |
| selection.folders.type | All the selected folders are of the input type. |
| selection.folders.aspect | All the selected folders have the input aspect. |
| selection.folders.property | All the selected folders have the indicated property and their values satisfy the condition. |
| selection.folders.name | All the selected folders match the condition in their name. |
| selection.currentFolder.type | The current folder is of the input type. |
| selection.currentFolder.aspect | The current folder has the input aspect. |
| selection.currentFolder.property | The current folder has the indicated property and their values satisfy the condition. |
| selection.currentFolder.name | The current folder matches the condition in their name. |

### Features

A user action can be associated to a feature once it has been defined and the rules for when to display it have been configured. This determines in which menu or view the action is displayed.

The properties to configure the action feature are:

| Property | Description |
| -------- | ----------- |
| Title | *Required.* The text displayed to the end user in the menu, for example `Start invoice process`. |
| Description | *Optional.* The tooltip for the action in the menu, for example `Start the invoice process with the intial invoice attached.`. |
| Icon | *Required.* The icon that will be displayed to the end user in the menu next to the `Title`. |
| Order | *Optional.* The order the action will appear in the menu list. The higher the number the lower down the list, or further right in a list it is displayed. |
| Action | *Required.*  The selected action to execute. |
| Visibility | *Optional.* The rule to use for evaluating whether a user can see the action. |
| Enabled | *Optional.* The rule to use for evaluating whether the action is enabled or not. |

Actions can be displayed in different parts of the Digital Workspace by associating them with different features.

#### Application header feature

The application header will display an action next to the search bar and user information:

![application header image]({% link process-automation/images/feature-app-header.png %})

#### Application header menu feature

The application header menu will display an action in the application header menu next to items such as **Settings** and **About**:

![application header menu image]({% link process-automation/images/feature-app-header-menu.png %})

#### Application toolbar feature

The application toolbar will display an action underneath the header where items such as a breadcrumb are normall placed:

![application toolbar image]({% link process-automation/images/feature-app-toolbar.png %})

#### Dropdown button feature

The dropdown button will display an action in the left-hand menu as a new item:

![dropdown button image]({% link process-automation/images/feature-dropdown.png %})

#### Context menu feature

The context menu will display an action in the menu displayed when right-clicking a node:

![context menu image]({% link process-automation/images/feature-context-menu.png %})

#### Sidebar feature

The sidebar will display an action in the properties sidebar:

![sidebar image]({% link process-automation/images/feature-sidebar.png %})

#### Sidebar toolbar feature

The sidebar toolbar will display an action on the toolbar within the properties sidebar:

![sidebar toolbar image]({% link process-automation/images/feature-sidebar-toolbar.png %})

#### Viewer feature

The viewer will display an action on the file viewer page:

![viewer image]({% link process-automation/images/feature-viewer.png %})

#### Viewer toolbar feature

The viewer toolbar will display an action on the toolbar located on the file viewer page:

![viewer toolbar image]({% link process-automation/images/feature-viewer-toolbar.png %})

#### Viewer toolbar menu feature

The viewer toolbar menu will display an action in the dropdown menu in the toolbar located on the file viewer page:

![viewer toolbar menu image]({% link process-automation/images/feature-viewer-toolbar-menu.png %})

#### Viewer shared feature

The shared viewer will display an action on the file viewer page of a shared file:

![viewer shared image]({% link process-automation/images/feature-viewer-shared.png %})

#### Viewer shared toolbar feature

The shared viewer toolbar will display an action on the toolbar located on the file viewer page of a shared file:

![viewer shared toolbar image]({% link process-automation/images/feature-viewer-shared-toolbar.png %})

## Custom user interfaces

Custom user interfaces can be [developed]({% link process-automation/latest/develop/index.md %}) with the [Application Development Framework](https://www.alfresco.com/abn/adf/docs/){:target="_blank"} and deployed as part of the project.

## User interface actions

The actions that can be run against an interface are:

| Action | Description |
| ------ | ----------- |
| Download UI | Download the JSON for the interface. |
| Validate | Run validation against the interface. Any errors can be seen in the log history at the bottom of the Modeling Application and are flagged in a pop-up box. |
| Save | Save any changes made to the interface. |
| Save As | Save As allows you to save a another copy of a model. This new saved copy will not affect the orirginal model. |
| Delete | Delete the interface. |

## Auditing

When an event action is performed you will find an entry in the Audit service, the information visible depends on the Action type.

| Action type | Event type | Description |
| ----------- |----------- | ----------- |
| Event | USER_ACTION_NAMED_EVENT | This event is sent from the [Form runtime]({% link process-automation/latest/admin/architecture.md %}#form-runtime) and provides information about the user action, such as the name of the interface in which the action was performed, the name of the event and the nodes selected when the action was performed. |
| Form | USER_ACTION_FORM_SUBMITTED |  This event is sent from the [Form runtime]({% link process-automation/latest/admin/architecture.md %}#form-runtime) and provides information about the form submitted from the user action, such as the name of the interface in which the action was performed, id of the submitted form, the values submitted, or the outcome pressed. |
| Start process | PROCESS_STARTED | This event is sent from the [Process runtime]({% link process-automation/latest/admin/architecture.md %}#process-runtime) and provides information about the process definition and the process instance created. |
---
title: Projects
--- 

Projects are the top level component of the business process being modeled. They contain all of the logic for the models that make up the business process such as forms, processes, content models and connectors.

Some example projects are available for you to use to help you get started, for more see [Example projects](#example-projects).

## Create a project

To create a project:

1. Sign into the Modeling Application.

2. Click the **NEW** dropdown.

3. Select how to create the project:

    * **Create Project** creates a new, empty project.

    * **Upload Project** allows for uploading an existing project `.zip` into the Modeling Application.

4. Enter a **Project name** and optional **Project description** if **Create Project** was chosen.

You can use the **Save as** function to save a new copy of a project from the projects view screen or from the home screen. This is accessed by clicking on the three dots and selecting **Save as**.  

## Properties

The properties for a project are:

| Property | Description |
| -------- | ----------- |
| Project name | *Required.* A unique name for a project. Project names must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example: `project-4-a` |
| Project description | *Optional.* A short description of what the project is for. |

Once a project has been created or uploaded into the Modeling Application, the following properties are displayed:

| Property | Description |
| -------- | ----------- |
| Name | The name of the project as it appears in the Modeling Application. |
| Updated | The amount of time that has lapsed since the last update to the project. |
| Created | Displays how long ago the project was created. |
| Created By | Displays which user created the project. |
| Version | Displays the current version of the project. |
| Collaborators | Displays an icon for each of the collaborators that are collaborating on a project, for more see [Collaborators](#collaborators). |
| Options | A list of actions that can be made against the project: {::nomarkdown}<ul><li><b>Edit</b> allows the project name and description to be updated.</li><li><b>Delete</b> removes the project.</li><li><b>Download</b> bundles the project contents into a zipped folder to import it into a different environment.</li><li><b>Collaborators</b> is for managing the project permissions.</li><li><b>Release</b> creates a new version of the project.</li><li><b>View Releases</b> shows the metadata related to each release of the project.</li></ul>{:/} |
| Star icon | Use the icon to select which projects you want to add to the **Favorite projects** view. |

## Collaborators

By default users can only view the projects they have created. The **Collaborators** option allows user access to be managed for individual projects. A collaborator can do anything the creator can do except for deleting the project.

To add a collaborator to a project:

1. Select the **Collaborators** option against a project.
2. Search for the user to add as a collaborator and click **Add**.

## Release a project

Projects are version controlled through the release action. When a project is first created its version will be set to 0 and will increment by 1 every time it is released.

> **Note**: A project must have been released in order to deploy it. Version 0 of a project can't be deployed.

To release a project:

1. Save any changes to the project components.
2. Navigate to the project list page of the Modeling Application.
3. Select the **Release** action from the **Options** column for the project.

Selecting the **View Releases** option for a project displays the version history for the project.

You can restore your project to a previous release by selecting the three dots to the right of the release you want to restore, and then selecting **Restore this Release**.

## Validate a project

Validation is run when any model within a project is saved. The **Validate** option is available to all model types and can be run on demand using the tick in the top toolbar. Project level validation will be run against all models in the project.

Any validation errors in a model will be displayed in the log at the bottom of the screen. Expand the log by clicking on the bottom tool bar to view log details.

## Folder structure

When you download a project, the extracted zip file will contain a folder for each model type within the project.  

The following is an example of an exploded zip file of a project called *holiday*:

```bash
/holiday/
    /connectors/
        emailConnector.json
    /decision-tables/
        auto-approve-extensions.json
        auto-approve.xml
    /files/
        approval-policy.bin
        approval-policy-extensions.json	
    /forms/
        approval-form.json
    /processes/
        approve-extensions.json
        approve.bpmn.xml
        request-extensions.json
        request.bpmn20.xml
    /scripts/
        update-calendar.bin
        update-calendar-extensions.json
    /triggers/
        approval-email.json
    /ui/
        process.json
    /content-models/
        holiday-model.xml
        holiday-model-extensions.json
    holiday.json

```

### Files

File definitions are created and stored for each model in a project:

* `<connector-name>.json` is the format that connector definitions are stored in.  
* `<decision-table-name>.xml` is the format that decision table definitions are stored in.
* `<decision-table-name>-extensions.json` is the format that decision table UIDs are stored in.
* `<file-name>.bin` is the binary format that uploaded files are stored as.
* `<file-name>-extensions.json` is the format that stores the metadata for the associated uploaded file.
* `<form-name>.json` is the format that form definitions are stored in.
* `<process-definition-name>.bpmn20.xml` is the format that process definitions are stored in.
* `<process-definition-name>-extensions.json` is the format that stores the properties for BPMN elements that are outside the scope of the BPMN standard.
* `<script-name>.bin` is the binary format that scripts are stored as.
* `<script-name>-extensions.json` is the format that stores the metadata and variables for a script.
* `<trigger-name>.json` is the format that triggers are stored in.
* `<ui-name>.json` is the format that UI definitions are stored in for content or process.
* `<content-model-name>.xml` is the format the content model is stored in.
* `<content-model>-extensions.json` is the format that stores the content model metadata.
* `<project-name>.json` is the project manifest that stores the name and version of a project.

## Example projects

To help you get started example projects for Audio and Video Transcription, Personal Identifiable Information Detection, and Invoice Review process are provided. Once you access the example projects you can make copies of them and save them as your own. Once saved, they can be reconfigured for your own purposes, including deploying your own applications that are based on them.

![Example projects]({% link process-automation/images/example-projects.png %})

### Access example projects

To access an example project:

1. Sign into the Modeling Application.

2. Click **Example Projects** from the left pane.

3. Select the example project you want to work with.

4. Click **Duplicate and open**.

5. Enter an appropriate name and click **Duplicate**.

![Duplicate projects]({% link process-automation/images/duplicate-projects.png %})

## Search Projects

You can search for any of the components that make up your projects.
Use the **Magnifying icon** on the top left above the Project tree to search for components.
In the image you can see all the components of the project that have 'company' in their name.

![Search projects]({% link process-automation/images/search-projects.png %})
---
title: Scripts
---

Scripts are used to execute a script as part of a process. Process variables can be passed to the script and the results of a script can be sent back to a process instance as process variables. Any JavaScript that is created by the modeling application has the same permissions assigned to it as the logged in user. This is helpful because it allows the logged in user to test their own scripts with their own files.

Script design uses the functionality of the [Monaco Editor](https://github.com/Microsoft/monaco-editor){:target="_blank"} and uses the [GraalVM JavaScript Engine](https://github.com/graalvm/graaljs){:target="_blank"} for execution.

Scripts are added to a process definition using a [script task]({% link process-automation/latest/model/processes/bpmn.md %}#script-task).

## Properties

The basic properties of a script are:

| Property | Description |
| -------- | ----------- |
| Script name | *Required.* The name of the script. Must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example `order-script` |
| Language | *Required.* The development language the script is written in, for example `Javascript`. |
| Script description | *Optional.* A description of what the script should be used for, for example `Returns the prefixed order number.` |

## Create a script

To create a script:

1. Sign into the Modeling Application and open a project.

2. Click the **NEW** dropdown.

3. Select how to create the script:

    * **Create > Script** creates a new, empty script.

    * **Upload > Script** allows for uploading an existing script `.bin` file into the Modeling Application.

    Alternatively use the **+** or **Upload** buttons next to **Scripts** in the left-hand menu.

4. Enter a name and optional description.

## Script modeling

The Modeling Application contains two tabs for creating and managing scripts.

The **Script Editor** is the GUI for modeling scripts by typing in the declared language. The editor has autocomplete functionality for APIs and script variables. The **Metadata** contains the properties related to the script.

![auto complete]({% link process-automation/images/auto-complete.png %})

### Simulation

Once a script has been written, it can be simulated by entering potential inputs and viewing their output.

In the UI click the **Simulate** button after entering the input values to simulate. The results will be populated in the outputs section.

## Variables

There are two types of variables associated with a script. Script variables are stored as JSON and are used to pass values between a process and a script. Declared variables are used within the script body itself.

### Script variables

Script variables can be used to pass and receive values from [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables).

The properties for a script variable are:

| Property | Description |
| -------- | ----------- |
| name | A unique name that can contain alphanumeric characters and underscores but must begin with a letter, for example `var_3` |
| type | A data type selected from a dropdown. See the following table for a list of data types, for example `String` |
| required | Sets whether the script variable must contain a value when the task is started, for example `false` |
| value | An optional default value for the script variable, for example `ice-cream` |

The data types that a script variable can be set as are:

| Type | Description |
| ---- | ----------- |
| String | A sequence of characters, for example `#Mint-Ice-Cream-4!` |
| Integer | A positive whole number, for example `642` |
| Boolean | A value of either `true` or `false` |
| Date | A specific date in the format `YYYY-MM-DD`, for example `2020-04-22` |
| Datetime | A specific date and time in the format `YYYY-MM-DD HH:mm:ss`, for example `2020-09-10 22:30:00` |
| File | A [file]({% link process-automation/latest/model/files.md %}) uploaded into a process definition or as part of a process instance or task |
| JSON | A JSON object, for example `{"flavor" : "caramel"}` |
| Folder | A folder object described as JSON, for example `"name": "mint-folder"` |
| Array | A comma separated list of entries, for example `mint, strawberry, vanilla` that will be formatted to `["mint","strawberry","vanilla"]` |

### Declared variables

Declared variables are used within the script itself and can be set to the value of a script variable by using the prefix `variables.` to reference the script variable. An input variable will set a declared variable to the value of a script variable when the script is executed.

For example, in a process the script variables `cost` and `orders` will have their values set from process variables. The declared variables `costOfItem` and `numberOfOrders` can then be set to these values using the following:

```javascript
let costOfItem = variables.cost;
let numberOfOrders = variables.orders;
```

The value of the script variable `totalCost` will then be set after the script has executed by using the following: 

```javascript
variables.totalCost = costOfItem * numberOfOrders;
```

The value of the script variable `totalCost` can finally be sent back to the process by [mapping it to a process variable]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping).

## Process scripts

Scripts can be used to start a process instance by building a payload.

For example, use the process definition ID and set the process variables using:

```javascript
let startProcessInstanceCmd = processPayloadBuilder.start()
	.withProcessDefinitionKey("Process_GyW7Ekkw")
	.withVariable("orderNumber": variables.orderNumber)
	.withVariable("quantity": variables.quantity)
	.build();
commandProducer.send(startProcessInstanceCmd);
```

### Content APIs

The following content APIs are supported:

* `ActionService`
* `GroupService`
* `NodeService`
* `PeopleService`
* `QueryService`
* `SearchService`
* `SiteService`
* `TagService`

> **Note:** The API scripts can be tested in the simulator on the scripts window.

You can create the object by accessing the API which then allows you to make use of all its methods.

For example:

```javascript
const nodeBodyCreate = { name: variables.name, nodeType: "cm:folder" };
const nodeService = new NodeService();
nodeService.createNode(variables.parentNodeId, nodeBodyCreate);
```

### Runtime APIs

The following APIs are supported:

* `ProcessInstanceAdminControllerImplApi`
* `ProcessInstanceControllerImplApi`
* `ProcessInstanceTasksControllerImplApi`
* `ProcessInstanceVariableAdminControllerImplApi`
* `ProcessInstanceVariableControllerImpl`
* `TaskAdminControllerImplApi`
* `TaskControllerImplApi`
* `TaskVariableAdminControllerImplApi`
* `TaskVariableControllerImplApi`

Using the following names you can perform all the actions related to the APIs mentioned above:

* `RuntimeProcessInstanceAdminService`: APA Runtime Process Instance Admin REST API (it includes `ProcessInstanceAdminControllerImplApi`, and `ProcessInstanceVariableAdminControllerImplApi`)
* `RuntimeProcessInstanceService`: APA Runtime Process Instance REST API (it includes `ProcessInstanceControllerImplApi`, `ProcessInstanceTasksControllerImplApi`, and `ProcessInstanceVariableControllerImpl`)
* `RuntimeTaskAdminService`: APA Runtime Task Admin API (it includes `TaskControllerImplApi`, and `TaskVariableAdminControllerImplApi`)
* `RuntimeTaskService`: APA Runtime Task API (it includes `TaskControllerImplApi`, and `TaskVariableControllerImplApi`)

For example:

```javascript
const startProcessPayload = { businessKey: variables.businessKey, payloadType: 'StartProcessPayload', processDefinitionKey: variables.processKey, variables: { fileArray: variables.fileArray } };
const runtimeProcessInstanceService = new RuntimeProcessInstanceService();
runtimeProcessInstanceService.startProcess(startProcessPayload);
```

### Query APIs

The following APIs are currently supported:

* `ProcessInstanceAdminControllerApi`
* `ProcessInstanceControllerApi`
* `ProcessInstanceDeleteControllerApi`
* `ProcessInstanceDiagramAdminControllerApi`
* `ProcessInstanceDiagramControllerApi`
* `ProcessInstanceServiceTasksAdminControllerApi`
* `ProcessInstanceTasksControllerApi`
* `ProcessInstanceVariableAdminControllerApi`
* `ProcessInstanceVariableControllerApi`
* `TaskAdminControllerApi`
* `TaskControllerApi`
* `TaskVariableAdminControllerApi`
* `TaskVariableControllerApi`

You can use the following names to perform all the actions related to the APIs indicated above:

* `QueryProcessInstanceAdminService`: APA Query Process Instance Admin REST API (it includes `ProcessInstanceAdminControllerApi`, `ProcessInstanceDiagramAdminControllerApi`, `ProcessInstanceServiceTasksAdminControllerApi`, and `ProcessInstanceVariableAdminControllerApi`)
* `QueryProcessInstanceService`: APA Query Process Instance REST API (it includes `ProcessInstanceControllerApi`, `ProcessInstanceDeleteControllerApi`, `ProcessInstanceDiagramControllerApi`, `ProcessInstanceTasksControllerApi`, and `ProcessInstanceVariableControllerApi`)
* `QueryTaskAdminService`: APA Query Task Admin API (it includes `TaskAdminControllerApi`, and `TaskVariableAdminControllerApi`)
* `QueryTaskService`: APA Query Task API (it includes `TaskControllerApi`, and `TaskVariableControllerApi`)

For example:

```javascript
const queryProcessInstanceAdminService = new QueryProcessInstanceAdminService();
queryProcessInstanceAdminService.findById('idProcess');
```

### Form API

The following API is currently supported:

* `FormApi`

You can use the following name to perform all the actions related to the API indicated above:

* `FormService`: APA Form API (it includes `FormApi`)

For example:

```javascript
const formId = variables.formId;
const formService = new FormService();
const form = formService.getFormDefinition(formId);
```

## Actions

The actions that can be run against a script are:

| Action | Description |
| ------ | ----------- |
| Download script | Download the bin file for the script. |
| Validate | Run validation against the script. Any errors can be seen in the log history at the bottom of the Modeling Application and are flagged in a pop-up box. |
| Save | Save any changes made to the script. |
| Delete | Delete the script. |
---
title: Triggers
---

Triggers are used to define a set of event criteria. When the event criteria specified in the trigger is met, the event is published and an action containing a payload is kicked off.

> **Note**: Triggers are not referenced in a process definition.

## Properties

The basic properties of a trigger are:

| Property | Description |
| -------- | ----------- |
| Trigger name | *Required.* The name of the trigger. Must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example `email-trigger` |
| Trigger description | *Optional.* A description of what the trigger should be used for, for example `Starts a process when an order request email is received.` |

## Create a trigger

To create a trigger:

1. Sign into the Modeling Application and open a project.

2. Click the **NEW** dropdown.

3. Select how to create the trigger:

    * **Create > Trigger** creates a new, empty trigger.

    * **Upload > Trigger** allows for uploading an existing trigger `.json` file into the Modeling Application.

    Alternatively use the **+** or **Upload** buttons next to **Triggers** in the left-hand menu.

4. Enter a name and optional description.

## Events {#events}

Trigger events include specific [BPMN]({% link process-automation/latest/model/processes/bpmn.md %}) states occurring in a process such as a timer being fired, a form being saved or events related to [connectors]({% link process-automation/latest/model/connectors/index.md %}) such as an email being received or a webhook REST request.

The events that can be created for a trigger are:

* [BPMN engine activities](#bpmn-engine-events)
* [Form save and submission events](#forms)
* [A user interface event action](#user-interface)
* [Content connector events](#content-connector)
* [An email being received](#email-received)
* [An SMS being received](#sms-received)
* [A Slack message being received](#slack-message-received)
* [An incoming webhook](#webhooks)

**Note:** The events handled in triggers follow the [Cloud Events](https://cloudevents.io/) specification. All the information described there and the specific information of the event is contained inside the `data` field.

### BPMN engine events

[BPMN engine events]({% link process-automation/latest/model/processes/events.md %}) are events generated as part of the life cycle of processes. They include events such as when BPMN activity is started, saved, submitted or completed. These events can be monitored by a trigger and an event published when specific criteria are met, for example when a timer with a certain ID is fired.

BPMN engine events are mostly configured using the `elementId` which is the `ID` of the [BPMN element]({% link process-automation/latest/model/processes/bpmn.md %}) within a process definition.

### Forms

The saving and submission of a [form]({% link process-automation/latest/model/forms.md %}) can be monitored as a trigger event. The specific form and the process definition it is attached to are used to create the trigger event.

### User interface

A [custom end-user action]({% link process-automation/latest/model/interfaces.md %}#event) of type **Event** can be set on the Digital Workspace user interface. When a user clicks the action in the Ditial Workspace an event is fired that can be linked to a trigger action.

The input parameters for a user interface action are:

| Parameter | Description |
| --------- | ----------- |
| uIName | *Required.* The name of the user interface that contains the action, for example `content`. |
| Name | *Required.* The name of the action of type **Event** to monitor, for example `share-with-accounts`. |

### Content connector

[Content connector]({% link process-automation/latest/model/connectors/content.md %}) events that can be monitored as trigger events include creating, updating and moving files, folders and content types. Content types are read from any [content models]({% link process-automation/latest/model/content-models.md %}) attached to the project.

### Email received

The [email service]({% link process-automation/latest/model/connectors/email.md %}) contains an **EMAIL_RECEIVED** event. This event allows for inbound emails to be monitored and an event published when specific criteria are met.

The input parameters for receiving an email are:

| Parameter | Description |
| --------- | ----------- |
| condition | *Optional.* An expression created using the [Condition Builder]({% link process-automation/latest/using/index.md %}#condition-builder) that when true triggers an action. The event content described by its model can be used in the expression. |
| pattern | *Required.* A regular expression that selects which emails trigger an action. Java catching group syntax can be used to create groups from the pattern as variables, for example `Order Number (?<orderNumber>.+)`. The variables can then be used in `echo` and `echoError`, for example `${orderNumber}`. |
| echo | *Optional.* An email sent to the original sender of the email that is matched, for example `Your reference number is ${orderNumber}`. |
| echoError | *Optional.* An email sent to the original sender if an error occurs when publishing the event, for example `There was a problem publishing that event.` |

The output parameters that can be used as values within the trigger action for receiving an email are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| matchGroups | JSON | *Optional.* Any matching groups found using the regular expression in `pattern`. |
| emailSubject | String | *Optional.* The subject line of the matched email. |
| emailTo | String | *Optional.* The recipient of the matched email. |
| emailFrom | String | *Optional.* The sender of the matched email. |
| emailBody | String | *Optional.* The message body of the matched email. |

> **Note**: Groups found in `matchGroups` can be used within a trigger action variable using the syntax `${matchGroups.group}`, for example `${matchGroups.orderNumber}`.

> **Important**: The [configuration parameters]({% link process-automation/latest/model/connectors/email.md %}#configuration-parameters) for the email service contain some parameters that are specific to configuring a trigger.

### SMS received

The [Twilio connector]({% link process-automation/latest/model/connectors/twilio.md %}) contains an **SMS_RECEIVED** event. This event allows for inbound SMS messages to be monitored and an event published when specific criteria are met.

The input parameters for receiving an SMS are:

| Parameter | Description |
| --------- | ----------- |
| condition | *Optional.* An expression created using the [Condition Builder]({% link process-automation/latest/using/index.md %}#condition-builder) that when true triggers an action. The event content described by its model can be used in the expression. |
| pattern | *Required.* A regular expression that selects which messages trigger an action. Java catching group syntax can be used to create groups from the pattern as variables, for example `Order Number (?<orderNumber>.+)`. The variables can then be used in `echo` and `echoError`, for example `${orderNumber}`. |
| echo | *Optional.* A message sent to the original sender of the text that is matched, for example `Your reference number is ${orderNumber}`. |
| echoError | *Optional.* A message sent to the original sender if an error occurs when publishing the event, for example `There was a problem publishing that event.` |

The output parameters that can be used as values within the trigger action for receiving an SMS are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| matchGroups | JSON | *Optional.* Any matching groups found using the regular expression in `pattern`. |
| originalMessage | String | *Optional.* The contents of the SMS message. |
| to | String | *Optional.* The recipient of the matched message. |
| from | String | *Optional.* The sender of the matched message. |

> **Note**: Groups found in `matchGroups` can be used within a trigger action variable using the syntax `${matchGroups.group}`, for example `${matchGroups.orderNumber}`.

### Slack message received

The [Slack connector]({% link process-automation/latest/model/connectors/slack.md %}) contains a **MESSAGE_RECEIVED** event. This event allows for Slack messages to be monitored and an event published when specific criteria are met.

> **Note:** Make sure the Slack connector [event subscription]({% link process-automation/latest/model/connectors/slack.md %}#event-subscription) has been configured to receive notifications from the Slack API.

The input parameters for a received Slack message are:

| Parameter | Description |
| --------- | ----------- |
| condition | *Optional.* An expression created using the [Condition Builder]({% link process-automation/latest/using/index.md %}#condition-builder) that when true triggers an action. The event content described by its model can be used in the expression.|
| pattern | *Required.* A regular expression that selects which messages trigger an action. Java catching group syntax can be used to create groups from the pattern as variables, for example `Order Number (?<orderNumber>.+)`. The variables can then be used in `echo` and `echoError`, for example `${orderNumber}`. |
| echo | *Optional.* A message sent to the user of the message that is matched, for example `Your reference number is ${orderNumber}`. |
| echoError | *Optional.* A message sent to the user of the message that is matched if an error occurs when publishing the event, for example `There was a problem publishing that event.` |
| channelTypes | *Optional.* The channel types to be monitored in Slack, for example `direct-message`,`public-channel` or `mention`. |

The output parameters that can be used as values within the trigger action for a received Slack message are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| matchGroups | JSON | *Optional.* Any matching groups found using the regular expression in `pattern`. |
| originalMessage | String | *Optional.* The contents of the Slack message. |
| slackChannelId | String | *Optional.* The channel the matched message was sent in. |
| slackUserId | String | *Optional.* The Slack user that sent the matched message. |

> **Note**: Groups found in `matchGroups` can be used within a trigger action variable using the syntax `${matchGroups.group}`, for example `${matchGroups.orderNumber}`.

### Webhooks

The [REST connector]({% link process-automation/latest/model/connectors/rest.md %}) can be used to publish an endpoint that external systems such as GitHub can consume as part of a trigger. The trigger then monitors this webhook and will publish any events that match the specific criteria as part of a project.

The input parameters for the **INCOMING_WEBHOOK** event is:

| Parameter | Description |
| --------- | ----------- |
| condition | *Optional.* An expression created using the [Condition Builder]({% link process-automation/latest/using/index.md %}#condition-builder) that when true triggers an action. The event content described by its model can be used in the expression. |
| path | *Required.* The webhook path to monitor. The format begins `https://<environment>.com/<project-name>/<connector-name>/events/` followed by a custom value, for example `https://alfresco.com/finance-project/rest-connector-1/events/github`. |
| method | *Optional.* A list of HTTP methods that can trigger an action. |
| condition | *Optional.* The condition that must evaluate to true to trigger an action. |
| status | *Optional.* The status code to return to the external service. |
| headers | *Optional.* The key value pairs that must match in order to publish the event. Use the **+** symbol to add more pairs. |
| params | *Optional.* The request parameter key value pairs that must match in order to publish the event. Use the **+** symbol to add more pairs. |
| body | *Optional.* The JSON body to send to the external service. |

The output parameters that can be used as values within the trigger action for a webhook are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| method | String | *Optional.* The HTTP method of the request. |
| path | String | *Optional.* The relative path of the request URL. |
| params | JSON | *Optional.* The query string or form parameters of the request. |
| headers | JSON | *Optional.* The headers of the request. |
| body | JSON | *Optional.* The body of the HTTP request. |

> **Important**: The [configuration parameter]({% link process-automation/latest/model/connectors/rest.md %}#configuration-parameters) for the REST connector is used for sending a response to the external system from the webhook.

## Actions

Trigger actions include starting a process instance, sending a BPMN signal or any [connector action]({% link process-automation/latest/model/connectors/index.md %}#actions). An action contains a payload that is sent from the trigger to the action being started.

The values for action payloads can be set in different ways depending on the action being sent and the source event type that generated the action. For example, if the Slack **MESSAGE_RECEIVED** event is used, then the value of an action can use the value of the `slackChannelId` the message was received from or an expression based on the event model.

The ways in which an action can be set are as:

* **Variables** are variables from the source event, for example using a BPMN engine activity as an event will allow the variables such as the `processDefinitionKey` as a value.

* **Expressions**: can be entered using a JSON editor to create more complex mappings from JSON objects, such as `${temperature.celsius}` will use the value for the object `celsius`.

* **Values** are static values that can be entered when the trigger action is modeled.

The actions that can be set on a trigger are:

* [Start a process](#start-a-process)
* [Send a signal](#send-a-signal)
* [Receive a message](#receive-a-message)
* [Execute a script](#execute-a-script)
* [Any content connector action](#content-connector-actions)
* [Any connector action](#connector-actions)

### Start a process

The action to start a process will begin a process instance when the event criteria are met. The payload for the start process action is:

| Property | Description |
| -------- | ----------- |
| processDefinitionKey | *Required.* The process definition the action will use to create a process instance with. The process definition must be in the same project as the trigger. |
| name | *Required.* The name that will be given to the process instance, for example `slackUserId`. |
| payloadType | *Required.* The type of payload. This is set to `StartProcessPayload` and cannot be changed. |
| businessKey | *Optional.* A business key ID for the process instance. |
| variables | *Optional.* Values from the trigger event can be mapped to [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) in the process definition. If the trigger event was a connector, this includes output parameters in the connector event. |

### Send a signal

The action to send a signal will send a named signal of global scope when an event criteria are met. The signal can be caught by the catching signal events [signal start events]({% link process-automation/latest/model/processes/bpmn.md %}#signal-start-event), [signal intermediate catch events]({% link process-automation/latest/model/processes/bpmn.md %}#signal-intermediate-catch-event) and [signal boundary events]({% link process-automation/latest/model/processes/bpmn.md %}#signal-boundary-event). The payload for the send signal action is:

| Property | Description |
| -------- | ----------- |
| name | *Required.* The name of the signal to emit, for example `Signal_0n91cib`. |
| payloadType | *Required.* The type of payload. This is set to `SignalPayload` and cannot be changed. |
| variables | *Optional.* Values from the trigger event can be mapped to [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) in the process definition. If the trigger event was a connector, this includes output parameters in the connector event. |

### Receive a message

The action to receive a message will send a named message when an event criteria are met. The message can be caught by the message catching events [message intermediate catch events]({% link process-automation/latest/model/processes/bpmn.md %}#message-intermediate-catch-event) and [message boundary events]({% link process-automation/latest/model/processes/bpmn.md %}#message-boundary-event). The payload for the receive message action is:

| Property | Description |
| -------- | ----------- |
| name | *Required.* The name of the message to send, for example `Message_077epax`. |
| correlationKey | *Required.* A [correlation key]({% link process-automation/latest/model/processes/bpmn.md %}#message-int-cat/message) must be provided when sending a message from a trigger, for example `014-245`. |
| payloadType | *Required.* The type of payload. This is set to `ReceiveMessagePayload` and cannot be changed. |
| variables | *Optional.* Values from the trigger event can be sent as part of the message payload. |

### Send a start message

The action to send a start message will send a named message when an event criteria are met. The message can be caught by a [message start event]({% link process-automation/latest/model/processes/bpmn.md %}#message-start-event) to start a process instance. The payload for the start message action is:

| Property | Description |
| -------- | ----------- |
| name | *Required.* The name of the message to send, for example `Message_077epax`. |
| payloadType | *Required.* The type of payload. This is set to `StartMessagePayload` and cannot be changed. |
| businessKey | *Optional.* A business key ID for the process instance. |
| variables | *Optional.* Values from the trigger event can be sent as part of the message payload. |

### Execute a script

The action to execute a script will execute a named [script]({% link process-automation/latest/model/scripts.md %}) when an event criteria are met. The script must exist in the same project as the trigger.

| Property | Description |
| -------- | ----------- |
| scriptName | *Required.* The name of the script to execute. This is set by selecting a script to execute, for example `update-orders-script`. |
| scriptId | *Required.* The ID of the script to execute. This is set by selecting a script to execute, for example `19ced673-e701-4e6c-ace6-f8aaee5455eb`. |
| variables | *Optional.* Values from the trigger event can be mapped to script variables to be used as part of the execution. |

### Content connector actions

The [content connector]({% link process-automation/latest/model/connectors/content.md %}) is used to execute actions against the Content Services repository. The actions available involve creating, selecting, updating and managing content.

All of the actions that the content connector can execute as part of a service task can also be used as trigger actions. The properties are the same as they are when the action is attached to a service task.

### Connector actions

[Connectors]({% link process-automation/latest/model/connectors/index.md %}) are used to handle interactions with external systems. This includes actions such as sending emails and utilizing services such as AWS Textract, Rekognition and Lambda functions.

All of the actions that connectors can execute as part of a service task can also be used as trigger actions. The properties are the same as they are when the action is attached to a service task.

> **Note**: Connector actions as part of a trigger are also tied to the connector instance. If different configuration is required to a connector used within a process then create a new connector instance for the trigger.
---
title: AWS connectors
---

There are five connectors that can be used to invoke different Amazon Web Services (AWS):

* [Lambda](#lambda)
* [Comprehend](#comprehend)
* [Rekognition](#rekognition)
* [Textract](#textract)
* [Transcribe](#transcribe)

All Amazon connectors are displayed on the process diagram with their respective AWS logos.

> **Important**: All AWS connectors require an AWS account with permission to access the features provided by Amazon. This account is separate to the Alfresco hosted environment and should be created and managed by customers.

## Lambda

The **INVOKE** action is used by the Lambda connector to invoke [Amazon Web Services (AWS) Lambda functions](https://aws.amazon.com/lambda/){:target="_blank"}.

The input parameters to invoke a Lambda function are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| function | String | *Required.* The name of the Lambda function to invoke, for example `lambda-2`. |
| payload | JSON | *Optional.* The payload that will be passed to the Lambda function as a JSON object. |

The output parameters from invoking a Lambda function are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| lambdaPayload | JSON | *Optional.* The Lambda function results payload. |
| lambdaStatus | Integer | *Optional.* The Lambda function invocation status code. |
| lambdaLog | String | *Optional.* The log produced during the function invocation. |

### Lambda configuration parameters

The configuration parameters for the Lambda connector are:

| Parameter | Description |
| --------- | ----------- |
| AWS_LAMBDA_AWS_ACCESS_KEY | *Required.* The access key to authenticate against AWS. |
| AWS_LAMBDA_AWS_SECRET_KEY | *Required.* The secret key to authenticate against AWS. |
| AWS_LAMBDA_AWS_REGION | *Required.* The region of AWS to invoke the Lambda functions. |

### Lambda errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the Lambda connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| SERVICE_ERROR | The service encountered an internal error. |
| INVALID_REQUEST | The request body could not be parsed as JSON. |
| REQUEST_TOO_LARGE | The request payload exceeded the Invoke request body JSON input limit. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| BAD_REQUEST | The server could not understand the request due to invalid syntax. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refuses to authorize it. |
| NOT_FOUND | The server could not find what was requested. |
| METHOD_NOT_ALLOWED | The request method is known by the server but is not supported. |
| NOT_ACCEPTABLE | The server cannot produce a response matching the list of acceptable values. |
| REQUEST_TIMEOUT | The server would like to shut down this unused connection. |
| CONFLICT | The request conflicts with current state of the server. |
| GONE | No longer available. |
| UNPROCESSABLE_ENTITY | The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions. |
| LOCKED | The resource that is being accessed is locked. |
| FAILED_DEPENDENCY | The request failed due to failure of a previous request. |
| INTERNAL_SERVER_ERROR | The server has encountered a situation it doesn't know how to handle. |
| NOT_IMPLEMENTED | The request method is not supported by the server and cannot be handled. |
| BAD_GATEWAY | The server got an invalid response. |
| SERVICE_UNAVAILABLE | The server is not ready to handle the request. |
| GATEWAY_TIMEOUT | The server is acting as a gateway and cannot get a response in time. |

## Comprehend

The Comprehend connector provides a standard mechanism to extract entities and Personally identifiable information (PII) entities from text in your documents. The **ENTITY** action is used by the Comprehend connector to execute [Amazon Comprehend](https://aws.amazon.com/comprehend/){:target="_blank"} natural language processing (NLP) services and identify and analyze text from specific plain text files. The Comprehend connector supports default entity recognition, custom entity recognition, and custom document classification.

> **Note:** The Comprehend connector can only receive either **files** or **text** but not both at the same time.

The Comprehend connector can extract entities and PII from the following file formats:

* `text/plain`
* `application/x-tar`
* `/zip`
* `/vnd.ms-outlook`
* `/pdf (max size in bytes: 26214400)`
* `/msword`
* `/vnd.ms-project`
* `/vnd.ms-outlook`
* `/vnd.ms-powerpoint`
* `/vnd.visio`
* `/vnd.ms-excel`
* `/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
* `/vnd.ms-word.document.macroenabled.12`
* `/vnd.openxmlformats-officedocument.wordprocessingml.document`
* `/vnd.ms-word.template.macroenabled.12`
* `/vnd.openxmlformats-officedocument.wordprocessingml.template`
* `/vnd.ms-powerpoint.template.macroenabled.12`
* `/vnd.openxmlformats-officedocument.presentationml.template`
* `/vnd.ms-powerpoint.addin.macroenabled.12`
* `/vnd.ms-powerpoint.slideshow.macroenabled.12`
* `/vnd.openxmlformats-officedocument.presentationml.slideshow`
* `/vnd.ms-powerpoint.presentation.macroenabled.12`
* `/vnd.openxmlformats-officedocument.presentationml.presentation`
* `/vnd.ms-powerpoint.slide.macroenabled.12`
* `/vnd.openxmlformats-officedocument.presentationml.slide`
* `/vnd.ms-excel.addin.macroenabled.12`
* `/vnd.ms-excel.sheet.binary.macroenabled.12`
* `/vnd.ms-excel.sheet.macroenabled.12`
* `/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
* `/vnd.ms-excel.template.macroenabled.12`
* `/vnd.openxmlformats-officedocument.spreadsheetml.template`
* `/x-cpio`
* `/java-archive`
* `/x-netcdf`
* `/msword`
* `/vnd.ms-word.document.macroenabled.12`
* `/vnd.openxmlformats-officedocument.wordprocessingml.document`
* `/vnd.ms-word.template.macroenabled.12`
* `/vnd.openxmlformats-officedocument.wordprocessingml.template`
* `/x-gzip`
* `/x-hdf`
* `text/html`
* `/vnd.apple.keynote`
* `/vnd.ms-project`
* `/vnd.apple.numbers`
* `/vnd.oasis.opendocument.chart`
* `/vnd.oasis.opendocument.image`
* `/vnd.oasis.opendocument.text-master`
* `/vnd.oasis.opendocument.presentation`
* `/vnd.oasis.opendocument.spreadsheet`
* `/vnd.oasis.opendocument.text`
* `/ogg`
* `/vnd.oasis.opendocument.text-web`
* `/vnd.oasis.opendocument.presentation-template`
* `/vnd.oasis.opendocument.spreadsheet-template`
* `/vnd.oasis.opendocument.text-template`
* `/vnd.apple.pages`
* `/pdf "maxSourceSizeBytes": 26214400,`
* `/vnd.ms-powerpoint.template.macroenabled.12`
* `/vnd.openxmlformats-officedocument.presentationml.template`
* `/vnd.ms-powerpoint.addin.macroenabled.12`
* `/vnd.ms-powerpoint.slideshow.macroenabled.12`
* `/vnd.openxmlformats-officedocument.presentationml.slideshow`
* `/vnd.ms-powerpoint`
* `/vnd.ms-powerpoint.presentation.macroenabled.12`
* `/vnd.openxmlformats-officedocument.presentationml.presentation`
* `/x-rar-compressed`
* `/rss+xml`
* `/rtf`
* `/vnd.ms-powerpoint.slide.macroenabled.12`
* `/vnd.openxmlformats-officedocument.presentationml.slide`
* `/vnd.sun.xml.writer`
* `text/xml`
* `/vnd.visio`
* `/xhtml+xml`
* `/vnd.ms-excel.addin.macroenabled.12`
* `/vnd.ms-excel`
* `/vnd.ms-excel.sheet.binary.macroenabled.12`
* `/vnd.ms-excel.sheet.macroenabled.12`
* `/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
* `/vnd.ms-excel.template.macroenabled.12`
* `/vnd.openxmlformats-officedocument.spreadsheetml.template`
* `/x-compress`
* `text/csv`
* `/msword`

### AWS Configuration

The Amazon Comprehend APIs that are called using the connector are:

* [DetectDominantLanguage](https://docs.aws.amazon.com/comprehend/latest/dg/API_DetectDominantLanguage.html){:target="_blank"}
* [DetectEntities](https://docs.aws.amazon.com/comprehend/latest/dg/API_DetectEntities.html){:target="_blank"}
* [BatchDetectEntities](https://docs.aws.amazon.com/comprehend/latest/dg/API_BatchDetectEntities.html){:target="_blank"}
* [StartEntitiesDetectionJob](https://docs.aws.amazon.com/comprehend/latest/dg/API_StartEntitiesDetectionJob.html){:target="_blank"}
* [DescribeEntitiesDetectionJob](https://docs.aws.amazon.com/comprehend/latest/dg/API_DescribeEntitiesDetectionJob.html){:target="_blank"}
* [DetectPiiEntities](https://docs.aws.amazon.com/comprehend/latest/dg/API_DetectPiiEntities.html){:target="_blank"}
* [StartPiiEntitiesDetectionJob](https://docs.aws.amazon.com/comprehend/latest/dg/API_StartPiiEntitiesDetectionJob.html){:target="_blank"}
* [DescribePiiEntitiesDetectionJob](https://docs.aws.amazon.com/comprehend/latest/dg/API_DescribePiiEntitiesDetectionJob.html){:target="_blank"}
* [StartDocumentClassificationJob](https://docs.aws.amazon.com/comprehend/latest/dg/API_StartDocumentClassificationJob.html)

To perform these calls it uses the AWS Comprehend SDK. This requires IAM users with the correct permissions to be created. The easiest way to do this is to give an IAM user the AWS managed policy `ComprehendFullAccess`. If you want to be stricter with access rights see [the list of all comprehend API permissions.](https://docs.aws.amazon.com/comprehend/latest/dg/comprehend-api-permissions-ref.html)

The Asynchronous calls also require the ability to read and write to an Amazon S3 bucket so the IAM user must have access to the configured bucket. As well as the IAM user accessing the data the Comprehend service itself requires access, for more see [Role-Based Permissions Required for Asynchronous Operations
](https://docs.aws.amazon.com/comprehend/latest/dg/access-control-managing-permissions.html#auth-role-permissions).

To allow the library to use this IAM user when communicating with the Comprehend service an AWS access key and secret key must be available, for more see [Using the Default Credential Provider Chain
](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html#credentials-default)

#### DetectDominantLanguage

You need to supply the calls that detect the language of the text document that is going to be processed. To do this, the connector calls the `DetectDominantLanguage` API. The `DetectDominantLanguage` call only works on text smaller than a configurable limit, the default is 5000 bytes. The connector uses the first bytes/characters of the document to determine what language to use when making calls to AWS Comprehend to determine which language is being used.

The `DetectDominantLanguage` service currently supports a greater set of languages than the entity detection services. It does this by checking the returned language against a configurable list of available languages.

> **Note:** Currently only EN and ES are supported by AWS entity detection. If the detected language is not in this list a configurable default language is used instead, which is EN by default.

#### Entities

The following are the different types of entities:

| Entity |
| --------- |
| DetectEntities |
| BatchDetectEntities |
| StartEntitiesDetectionJob |
| DescribeEntitiesDetectionJob |

Depending on the size of the input the connector will process it in a different a way.

The `DetectEntities` operation will be called if the supplied text file is smaller than a configurable limit, by default 5000 bytes. If the input file is larger than this then a different API must be used.

The `BatchDetectEntitie` is used if the file is larger than the `DetectEntities` limit although it also has a configurable limit, by default 125000 bytes. When you use the Batch API call the input file is split into chunks of less than the configurable limit, by default 5000 bytes.

The `StartEntitiesDetectionJob` and `DescribeEntititesDetectionJob` are used if the input file is larger than the `BatchDetectEntities` limit, by default 5000 bytes. Similar to the batch approach, the input file will be divided into a set of smaller files of a certain configured size. When dividing the original file, the engine ensures that it only includes full words and does not split on a non whitespace character.

The divided files are then uploaded to Amazon S3 using the same key prefix for all files. When all of them have been uploaded an asynchronous entity detection job is started. This is then followed by a polling process to check the status of the job until it finishes or the timeout is reached.

If the asynchronous job finishes successfully a compressed output file (`output.tar.gz`) with the result will be written by Amazon Comprehend. The file will be saved to the same bucket within a directory that is using the same key prefix. For more see [Asynchronous Batch Processing
](https://docs.aws.amazon.com/comprehend/latest/dg/how-async.html). The output file is downloaded from Amazon S3 and parsed into a `BatchDetectEntitiesResult` object. At the end of the process, all the resource files are cleaned, both locally and at Amazon S3.

#### PII Entities

| Entity |
| --------- |
| DetectPiiEntities |
| StartPiiEntitiesDetectionJob |
| DescribePiiEntitiesDetectionJob |

Depending on the size of the input the connector will process it in a different way.

The `DetectPiiEntities` operation will be called if the supplied text file is smaller than a configurable limit, by default 5000 bytes. If the input file is larger than this then a different API must be used.

The `StartPiiEntitiesDetectionJob` and `DescribePiiEntitiesDetectionJob` are used if the input file is larger than the `AsynchDetectPIIEntities` limit, by default 5000 bytes. The input file will be divided into a set of smaller files of a certain configured size. When dividing the original file, the engine ensures that it only includes full words and will not split on a non whitespace character.

The divided files are then uploaded to Amazon S3 using the same key prefix for all files. When all of them have been uploaded an asynchronous entity detection job is started. This is then followed by a polling process to check the status of the job until it finishes or the timeout is reached.

If the asynchronous job finishes successfully a compressed output file (`output.tar.gz`) with the result will be written by Amazon Comprehend. The file will be saved to the same bucket within a directory that is using the same key prefix. For more see [Asynchronous Batch Processing
](https://docs.aws.amazon.com/comprehend/latest/dg/how-async.html). The output file is downloaded from Amazon S3 and parsed into a `BatchDetectPiiResult` object. At the end of the process, all the resource files are cleaned, both locally and at Amazon S3.

The `StartDocumentClassificationJob` operation is always performed asynchronously. It requires a custom model and the classifier ARN must be provided. You can provide the custom classification ARN in two ways:

1. Use the `AWS_COMPREHEND_CUSTOM_CLASSIFICATION_ARN` environment variable when deploying the application.

2. Use the `customClassificationArn` input variable in the connector action. If the variable is not provided the `AWS_COMPREHEND_CUSTOM_CLASSIFICATION_ARN` value is used.

### BPMN Tasks Configuration

The following describes an example of how the text analysis connector is setup in AAE:

![BPMN]({% link process-automation/images/analysis-process.png %})

As part of the BPMN definition process, any service task responsible for triggering the text analysis `comprehend.ENTITY` has to be set as the value for its implementation attribute.

The following variables must be configured for the text analysis to function.

The input parameters of Entity detection are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| files | Array | *Optional.* The file to be analysed. If multiple files are passed, then only the first one will be analysed. |
| text | String | *Optional.* The Text to be analysed. If the `files` parameter is set, then this should be left blank. |
| maxEntities | Integer | *Optional.* The maximum number of entities that is returned. The parameter defaults to `${aws.comprehend.defaultMaxResults}`. |
| confidenceLevel | Float | *Optional.* The minimum confidence level for a entity expressed by a float number between 0 and 1. The parameter defaults to `${aws.comprehend.defaultConfidence}`. |
| timeout | Integer | *Optional.* The timeout for the remote call to the Comprehend service in milliseconds. The parameter defaults to `${aws.comprehend.asynchTimeout}`. |
| customRecognizerArn | String | *Optional.* The custom recognizer ARN endpoint. If left blank, the Comprehend service will use the value given to the `AWS_COMPREHEND_CUSTOM_RECOGNIZER_ARN` environment variable. |

> **Note:** The connector must receive either files or text but not both at the same time.

The following is an example of the POST body for the Activiti REST API `http://{{domain}}/{{applicationName}}/rb/v1/process-instances` endpoint:

```json
{
  "processDefinitionKey": "TextAnalysisProcessTest",
  "processInstanceName": "processTextAnalysisTest_Simple",
  "businessKey": "MyBusinessKey",
  "variables": {
    "file" : [
        {
            "nodeId":"ad844189-9afb-4afb-965b-380db73022aa"
    	}
    ],
  	"maxEntities" : 50,
  	"confidenceLevel" : "0.95",
	"timeout" : 10000
  },
  "payloadType":"StartProcessPayload"
}
```

In the business process definition, the text analysis service task called **textAnalysisTask** has the implementation attribute configured to use the connector.

```bash
<bpmn2:serviceTask id="ServiceTask_0j2v2yc" name="textAnalysisTask" implementation="comprehend.ENTITY">
  <bpmn2:incoming>SequenceFlow_0kibr65</bpmn2:incoming>
  <bpmn2:outgoing>SequenceFlow_1048knn</bpmn2:outgoing>
</bpmn2:serviceTask>
```

The input parameters of PII Entity detection are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| files | Array | *Optional.* The file to be analysed. If multiple files are passed, then only the first one will be analysed. |
| text | String | *Optional.* The Text to be analysed. If the `files` parameter is set, then this should be left blank. |
| maxEntities | Integer | *Optional.* The maximum number of entities that is returned. The parameter defaults to `${aws.comprehend.defaultMaxResults}`. |
| confidenceLevel | Float | *Optional.* The minimum confidence level for a entity expressed by a float number between 0 and 1. The parameter defaults to `${aws.comprehend.defaultConfidence}`. |
| timeout | Integer | *Optional.* The timeout for the remote call to the Comprehend service in milliseconds. The parameter defaults to `${aws.comprehend.asynchTimeout}`. |

> **Note:** The connector must receive either files or text but not both at the same time.

The input parameters of Document classification are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| files | Array | *Optional.* The file to be analysed. If multiple files are passed, then only the first one will be analysed. |
| text | String | *Optional.* The Text to be analysed. If the `files` parameter is set, then this should be left blank. |
| maxEntities | Integer | *Optional.* The maximum number of entities that is returned. The parameter defaults to `${aws.comprehend.defaultMaxResults}`. |
| confidenceLevel | Float | *Optional.* The minimum confidence level for a entity expressed by a float number between 0 and 1. The parameter defaults to `${aws.comprehend.defaultConfidence}`. |
| timeout | Integer | *Optional.* The timeout for the remote call to the Comprehend service in milliseconds. The parameter defaults to `${aws.comprehend.asynchTimeout}`. |
| customClassificationArn | String | *Optional.* The custom recognizer ARN endpoint. If left blank, the Comprehend service will use the value given to the `AWS_COMPREHEND_CUSTOM_CLASSIFICATION_ARN` environment variable. **Note:** The `AWS_COMPREHEND_CUSTOM_CLASSIFICATION_ARN` environment variable does not have a default value. If it is being used then you must also set a value for it. |

> **Note:** The connector must receive either files or text but not both at the same time.

The output parameters from the entity detection are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| awsResponse | JSON | *Optional.* The result of the analysis from the Comprehend service. |
| aisResponse | JSON | *Optional.* The result of the analysis in [Alfresco Intelligence Service]({% link intelligence-services/latest/index.md %}) format. |
| entities | JSON | *Optional.* The result object containing the entities detected. |

The output parameters from the PII entity detection are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| awsResponse | JSON | *Optional.* The result of the analysis from the Comprehend service. |
| piiEntityTypes | JSON | *Optional.* The result object containing the PII entities detected. |

The output parameters from the Document classification are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| awsResponse | Object | *Optional.* The object that contains the original result of the text analysis performed by the Comprehend service. |
| documentClassificationClasses | Array | *Optional.* An array that contains the list of the different classes detected in the analysis. |

### Comprehend configuration parameters

The configuration parameters for the Comprehend connector are:

| Parameter | Description |
| --------- | ----------- |
| AWS_ACCESS_KEY_ID | *Required.* The access key to authenticate against AWS. |
| AWS_SECRET_KEY | *Required.* The secret key to authenticate against AWS. |
| AWS_REGION | *Required.* The region of AWS to use the Comprehend service. |
| AWS_S3_BUCKET | *Required.* The name of the S3 bucket to use. |
| AWS_COMPREHEND_ROLE_ARN | *Required.* The Amazon Resource Name for Comprehend to use. |

### Comprehend errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the Comprehend connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| INVALID_RESULT_FORMAT | The REST service result payload cannot be parsed. |
| TEXT_SIZE_LIMIT_EXCEEDED | The size of the input text exceeds the limit. |
| TOO_MANY_REQUEST | The request throughput limit was exceeded. |
| UNSUPPORTED_LANGUAGE | The language of the input text can't be processed. |
| CLIENT_EXECUTION_TIMEOUT | The execution ends because of timeout. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| BAD_REQUEST | The server could not understand the request due to invalid syntax. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refuses to authorize it. |
| NOT_FOUND | The server could not find what was requested. |
| METHOD_NOT_ALLOWED | The request method is known by the server but is not supported. |
| NOT_ACCEPTABLE | The server cannot produce a response matching the list of acceptable values. |
| REQUEST_TIMEOUT | The server would like to shut down this unused connection. |
| CONFLICT | The request conflicts with current state of the server. |
| GONE | No longer available. |
| UNPROCESSABLE_ENTITY | The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions. |
| LOCKED | The resource that is being accessed is locked. |
| FAILED_DEPENDENCY | The request failed due to failure of a previous request. |
| INTERNAL_SERVER_ERROR | The server has encountered a situation it doesn't know how to handle. |
| NOT_IMPLEMENTED | The request method is not supported by the server and cannot be handled. |
| BAD_GATEWAY | The server got an invalid response. |
| SERVICE_UNAVAILABLE | The server is not ready to handle the request. |
| GATEWAY_TIMEOUT | The server is acting as a gateway and cannot get a response in time. |

### Limitations

PDF files larger than 26214400 bytes are not supported.

## Rekognition

The **LABEL** action is used by the Rekognition connector to execute [Amazon Rekognition](https://aws.amazon.com/rekognition/){:target="_blank"} services to identify and label the objects in JPEG and PNG files that are less than 15mb in size.

The Amazon Rekognition API that is called is the [Detect Labels API](https://docs.aws.amazon.com/rekognition/latest/dg/API_DetectLabels.html){:target="_blank"}.

Files between 5mb and 15mb are uploaded to an Amazon S3 bucket before processing. The [IAM](https://aws.amazon.com/iam/){:target="_blank"} user configured to run the Rekognition service requires access to this bucket, the [Rekognition service itself](https://docs.aws.amazon.com/rekognition/latest/dg/access-control-overview.html){:target="_blank"} and to have the `rekognition:DetectLabels` permission.

The input parameters of the Rekognition connector are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Required.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to send for analysis. |
| mediaType | String | *Optional.* The media type of the file to be analyzed, for example `/octect-stream`. |
| maxLabels | Integer | *Optional.* The maximum number of labels to be return. The default value is `10`. |
| confidenceLevel | String | *Optional.* The confidence level to use in the analysis between 0 and 1, for example `0.75`. |
| timeout | Integer | *Optional.* The timeout period for calling the Rekognition service in milliseconds, for example `910000`. |

The output parameters from the Rekognition analysis are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| awsResponse | JSON | *Optional.* The result of the analysis from the Rekognition service. |
| aisResponse | JSON | *Optional.* The result of the image analysis in [Alfresco Intelligence Service]({% link intelligence-services/latest/index.md %}) format. |
| labels | JSON | *Optional.* The result object containing the labels detected. |

### Rekognition configuration parameters

The configuration parameters for the Rekognition connector are:

| Parameter | Description |
| --------- | ----------- |
| AWS_ACCESS_KEY_ID | *Required.* The access key to authenticate against AWS. |
| AWS_SECRET_KEY | *Required.* The secret key to authenticate against AWS. |
| AWS_REGION | *Required.* The region of AWS to use the Rekognition service in. |
| AWS_S3_BUCKET | *Required.* The name of the S3 bucket to use. |

### Rekognition errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the Rekognition connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT| The input variable has an invalid type. |
| INVALID_RESULT_FORMAT | The REST service result payload cannot be parsed. |
| PROVISIONED_THROUGHPUT_EXCEEDED | The number of requests exceeded your throughput limit. |
| ACCESS_DENIED | The user is not authorized to perform the action. |
| IMAGE_TOO_LARGE | The input image size exceeds the allowed limit. |
| INVALID_IMAGE_FORMAT | The provided image format is not supported. |
| LIMIT_EXCEEDED | The service limit was exceeded. |
| THROTTLING_ERROR | The service is temporarily unable to process the request. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| BAD_REQUEST | The server could not understand the request due to invalid syntax. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refuses to authorize it. |
| NOT_FOUND | The server could not find what was requested. |
| METHOD_NOT_ALLOWED | The request method is known by the server but is not supported. |
| NOT_ACCEPTABLE | The server cannot produce a response matching the list of acceptable values. |
| REQUEST_TIMEOUT | The server would like to shut down this unused connection. |
| CONFLICT | The request conflicts with current state of the server. |
| GONE | No longer available. |
| UNPROCESSABLE_ENTITY | The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions. |
| LOCKED | The resource that is being accessed is locked. |
| FAILED_DEPENDENCY | The request failed due to failure of a previous request. |
| INTERNAL_SERVER_ERROR | The server has encountered a situation it doesn't know how to handle. |
| NOT_IMPLEMENTED | The request method is not supported by the server and cannot be handled. |
| BAD_GATEWAY | The server got an invalid response. |
| SERVICE_UNAVAILABLE | The server is not ready to handle the request. |
| GATEWAY_TIMEOUT | The server is acting as a gateway and cannot get a response in time. |

## Textract

The **EXTRACT** action is used by the Textract connector to execute [Amazon Textract](https://aws.amazon.com/textract/){:target="_blank"} to extract text and metadata from JPEG and PNG files that are less than 5mb in size.

The Amazon Textract APIs called are the [Detect Document Text API](https://docs.aws.amazon.com/textract/latest/dg/API_DetectDocumentText.html){:target="_blank"} which joins all `LINE` block objects with a line separator between them and the [Analyze Document API](https://docs.aws.amazon.com/textract/latest/dg/API_AnalyzeDocument.html){:target="_blank"} with `FORM` and `TABLES` analysis.

The [IAM](https://aws.amazon.com/iam/){:target="_blank"} user configured to run the Textract services needs to have the `textract:DetectDocumentText` and `textract:AnalyzeDocument` permissions.

The input parameters of the Textract connector are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Required.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to send for extraction. |
| outputFormat | String | *Optional.* The format of the output file. Possible values are `JSON` and `TXT`. The default value is `JSON`. |
| confidenceLevel | String | *Optional.* The confidence level to use in the analysis between 0 and 1, for example `0.75`. |
| timeout | Integer | *Optional.* The timeout period for calling the Textract service in milliseconds, for example `910000`. |

The output parameters from the Textract analysis are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| awsResult | JSON | *Optional.* The result of the analysis from the Textract service. |

### Textract configuration parameters

The configuration parameters for the Textract connector are:

| Parameter | Description |
| --------- | ----------- |
| AWS_ACCESS_KEY_ID | *Required.* The access key to authenticate against AWS. |
| AWS_SECRET_KEY | *Required.* The secret key to authenticate against AWS. |
| AWS_REGION | *Required.* The region of AWS to use the Textract service. |
| AWS_S3_BUCKET | *Required.* The name of the S3 bucket to use. |

### Textract errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the Textract connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT| The input variable has an invalid type. |
| INVALID_RESULT_FORMAT | The REST service result payload cannot be parsed. |
| PROVISIONED_THROUGHPUT_EXCEEDED | The number of requests exceeded your throughput limit. |
| ACCESS_DENIED | The user is not authorized to perform the action. |
| IMAGE_TOO_LARGE | The input image size exceeds the allowed limit. |
| INVALID_IMAGE_FORMAT | The provided image format is not supported. |
| LIMIT_EXCEEDED | The service limit was exceeded. |
| THROTTLING_ERROR | The service is temporarily unable to process the request. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| BAD_REQUEST | The server could not understand the request due to invalid syntax. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refuses to authorize it. |
| NOT_FOUND | The server could not find what was requested. |
| METHOD_NOT_ALLOWED | The request method is known by the server but is not supported. |
| NOT_ACCEPTABLE | The server cannot produce a response matching the list of acceptable values. |
| REQUEST_TIMEOUT | The server would like to shut down this unused connection. |
| CONFLICT | The request conflicts with current state of the server. |
| GONE | No longer available. |
| UNPROCESSABLE_ENTITY | The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions. |
| LOCKED | The resource that is being accessed is locked. |
| FAILED_DEPENDENCY | The request failed due to failure of a previous request. |
| INTERNAL_SERVER_ERROR | The server has encountered a situation it doesn't know how to handle. |
| NOT_IMPLEMENTED | The request method is not supported by the server and cannot be handled. |
| BAD_GATEWAY | The server got an invalid response. |
| SERVICE_UNAVAILABLE | The server is not ready to handle the request. |
| GATEWAY_TIMEOUT | The server is acting as a gateway and cannot get a response in time. |

## Transcribe

The transcribe connector provides a standard mechanism to obtain speech to text information from audio and video files using [Amazon Transcribe](https://aws.amazon.com/transcribe/){:target="_blank"}.

### Installation

The connector is a Spring Boot application that is included as a separate service of your AAE deployment.

### AWS Configuration

Alfresco recommends you access AWS using AWS Identity and Access Management (IAM). To use IAM to access AWS, create an IAM user, add the user to an IAM group with administrative permissions, and then grant administrative permissions to the IAM user. You can then access AWS using a special URL and the IAM user's credentials.

### BPMN Tasks Configuration

As part of BPMN definition process, any service task responsible for triggering speech to text needs to set **_transcribe.TRANSCRIBE_** as the value for its implementation attribute.

In addition to the above configuration, these variables are required to perform the audio analysis:

The input parameters of the transcribe connector are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | Array | *Required.* File to be transcribed. If multiple files are passed, only the first one will be processed. |
| timeout | Integer | *Optional.* Timeout for the remote call to transcribe service in milliseconds. The default is `${aws.transcribe.asynchTimeout}`. |
| generateWebVTT | Boolean | *Optional* The output webVTT is only populated if generateWebVTT is set to `true`. |

The output parameters of the Transcribe connector are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| awsResult | JSON | *Optional.* Result of the AWS Transcribe speech to text process. |
| transcription | String | *Required.* Transcription result. |
| webVTT | JSON | *Optional* Subtitles result in Web Video Text Tracks format. |

### Transcribe configuration parameters

The configuration parameters for the Transcribe connector are:

| Parameter | Description |
|-----------|-------------|
| AWS_ACCESS_KEY_ID | *Required.* The access key to authenticate against AWS. |
| AWS_SECRET_KEY | *Required.* The secret key to authenticate against AWS. |
| AWS_REGION | *Required.* The region of AWS to use the Textract service. |
| AWS_S3_BUCKET | *Required.* The name of the S3 bucket to use. |
| AWS_TRANSCRIBE_LANGUAGES | List of comma separated languages that are spoken in the audio/video file. |

### Transcribe errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the Transcribe connector are:

| Error | Description  |
|-------|--------------|
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| INVALID_RESULT_FORMAT | The REST service result payload cannot be parsed. |
| LIMIT_EXCEEDED | The service limit was exceeded. |
| ACCESS_DENIED | The user is not authorized to perform the action. |
| INTERNAL_FAILURE | An internal Amazon Lex error occurred. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| BAD_REQUEST | The server could not understand the request due to invalid syntax. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refused to authorize it. |
| NOT_FOUND | The server could not find what was requested. |
| METHOD_NOT_ALLOWED | The request method is known by the server but is not supported. |
| NOT_ACCEPTABLE | The server cannot produce a response matching the list of acceptable values. |
| REQUEST_TIMEOUT | The server is requesting to shut down this unused connection. |
| CONFLICT | The request conflicts with the current state of the server. |
| GONE | No longer available. |
| UNPROCESSABLE_ENTITY | The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions. |
| LOCKED | The resource that is being accessed is locked. |
| FAILED_DEPENDENCY | The request failed due to failure of a previous request. |
| INTERNAL_SERVER_ERROR | The server has encountered a situation and does not know how to handle it. |
| NOT_IMPLEMENTED | The request method is not supported by the server and cannot be handled. |
| BAD_GATEWAY | The server got an invalid response. |
| SERVICE_UNAVAILABLE | The server is not ready to handle the request. |
| GATEWAY_TIMEOUT | The server is acting as a gateway and cannot get a response in time. |

### Limitations

Minimum confidence is not currently supported. The confidence is however included as part of the response.
---
title: Content service 
---

The Content service is used to execute actions against the Content Services repository. The actions available involve creating, selecting, updating and managing content throughout a process. The content can be uploaded as part of the process, retrieved from the repository or stored in the repository.

All Content service actions are displayed on the process diagram with the Alfresco logo.

## Create a Content service task

Content services are stored separately in the palette from other services. To create a Content service:

1. Sign into the Modeling Application and open a project and process.

2. Click the Alfresco logo in the tool palette and select the content action.

3. Drag the action onto the diagram canvas and fill in the properties.

> **Note**: The Content service does not have any [configuration parameters]({% link process-automation/latest/model/connectors/index.md %}#configuration-parameters) as it connects directly to the Content Services repository. This means that only a single instance of the service is required per project.

## Properties

The Content service is implemented as a [service task]({% link process-automation/latest/model/processes/bpmn.md %}#service-task). All the properties available to a service task are those required by the Content service. The three most important ones to understand for the Content service are:

| Property | Description |
| -------- | ----------- |
| Implementation | *Required.* Displays the name of the service the task is using. This will be **_content-service_**. |
| Action | *Required.* Selects which action the Content service task should execute, for example `SELECT_FILE`. |
| Mapping type | *Required.* Sets how data should be passed between the service and the process by mapping the [input and output parameters]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping). For example, setting the details of the file to select and which process variable will store it. |

### Parameter precedence

When using actions to manage content within a process it is important to understand the precedence of their parameters.

Files and folders can all be selected in multiple ways for each action. The following order dictates which parameter will be used if multiple parameters are passed to the Content service:

**nodeId / fileId / folderId** > **file / folder** > **path / filePath / folderPath** > **searchQuery**

If an action can take a file or a folder as an input and both are filled in, the file will take precedence over the folder.  

## Create actions

Create actions are used to create a new file or folder to store in the repository, reuse in another task within the process, or both.

The create actions are:

* [Create a file](#create-file)
* [Create a folder](#create-folder)

### Create file

The **CREATE_FILE** action is used to create a new file.

The input parameters to create a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| fileName | String | *Required.* A name for the file to be created. |
| targetFolder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to create the new file in. |
| targetFolderId | String | *Requires one.* The nodeId of the folder to create the new file in. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| targetFolderPath | String | *Requires one.* The location path or relative path of the folder to create the new file in. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| autorename | Boolean | *Optional.* If set to `true`, the new file will have an integer added to its name if a file already exists with the same `fileName`. |
| targetFileType | Content-Type | *Optional.* The type to set the new file as, for example `fin:invoice`. |
| targetFileMetadata | Content-Metadata | *Optional.* Metadata to store with the new file. This is a JSON object of key value pairs. See below for an example. |
| underscoreMetadata | Boolean | *Optional.* If set to `true`, the input `targetFileMetadata` can have its namespace prefixes written with `_` instead of `:`, for example `cm_title` instead of `cm:title`. The output `response` will also have its prefixes replaced. This allows the JSON to be used in an expression, for example `${metadata.cm_title}`, whereas `${metadata.cm:title}` is not valid. |

> **Note**: `underscoreMetadata` can be set to `true` and the `targetFileMetadata` input can still use `:` with the service successfully executing the action. If `underscoreMetadata` is set to `false` and `targetFileMetadata` uses `_` then the service will fail to execute the action.

An example of the `targetFileMetadata` that can be sent with the file is:

```json
{
"ahr:contract-type": "Full Time",
"ahr:full-name": "John Doe",
"ahr:role": "Developer"
}
```

The output parameters from creating a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call creating the folder. |
| file | File | *Optional.* The created file available to be mapped to a [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables). |

### Create folder

The **CREATE_FOLDER** action is used to create a new folder.

The input parameters to create a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| folderName | String | *Required.* A name for the folder to be created. |
| targetFolder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to create the new folder in. |
| targetFolderId | String | *Requires one.* The nodeId of the folder to create the new folder in. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| targetFolderPath | String | *Requires one.* The location path or relative path of the folder to create the new folder in. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| autorename | Boolean | *Optional.* If set to `true`, the new folder will have an integer added to its name if a folder already exists with the same `folderName`. |
| targetFolderType | Content-Type | *Optional.* The type to set the new folder as. |
| targetFolderMetadata | Content-Metadata | *Optional.* Metadata to store with the new folder. This is a JSON object of key value pairs. See below for an example. |
| underscoreMetadata | Boolean | *Optional.* If set to `true`, the input `targetFolderMetadata` can have its namespace prefixes written with `_` instead of `:`, for example `cm_title` instead of `cm:title`. The output `response` will also have its prefixes replaced. This allows the JSON to be used in an expression, for example `${metadata.cm_title}`, whereas `${metadata.cm:title}` is not valid. |

> **Note**: `underscoreMetadata` can be set to `true` and the `targetFolderMetadata` input can still use `:` with the service successfully executing the action. If `underscoreMetadata` is set to `false` and `targetFolderMetadata` uses `_` then the service will fail to execute the action.

An example of the `targetFolderMetadata` that can be sent with the folder is:

```json
{
"ahr:contract-type": "Full Time",
"ahr:full-name": "John Doe",
"ahr:role": "Developer"
}
```

The output parameters from creating a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call creating the folder. |
| folder | Folder | *Optional.* The created folder available to be mapped to a [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables). |

## Select actions

Select actions are used to select a file, a files content, a folder or the metadata for a node and store it in a process variable to use in another task within the process.

The selection actions are:

* [Select a file](#select-file)
* [Select a folder](#select-folder)
* [Select a node's metadata](#select-metadata)

### Select file

The **SELECT_FILE** action is used to select a file and store it in a variable.

The input parameters to select a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to select. |
| nodeId | String | *Requires one.* The nodeId of the file to select. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the file to select. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| searchQuery | String | *Requires one.*  A search query to find the file to select. This is in Alfresco Full Text Search (AFTS) format, for example: `cm:title:test`. |
| searchMaxItems | Integer | *Optional.* The maximum number of items returned by the `searchQuery`. The default value is `100`. |
| searchSkipCount | Integer | *Optional.* The number of items in the result to skip before returning the results. The default value is `0`. |

The output parameters from selecting a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call selecting the file. |
| file | File | *Optional.* The selected file available to be mapped to a [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables). |

### Select folder

The **SELECT_FOLDER** action is used to select a folder and store it in a variable.

The input parameters to select a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to select. |
| nodeId | String | *Requires one.* The nodeId of the folder to select. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the folder to select. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| searchQuery | String | *Requires one.*  A search query to find the folder to select. This is in Alfresco Full Text Search (AFTS) format, for example: `cm:title:test`. |
| searchMaxItems | Integer | *Optional.* The maximum number of items returned by the `searchQuery`. The default value is `100`. |
| searchSkipCount | Integer | *Optional.* The number of items in the result to skip before returning the results. The default value is `0`. |

The output parameters from selecting a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call selecting the folder. |
| folder | Folder | *Optional.* The selected folder available to be mapped to a [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables). |

### Select metadata

The **SELECT_METADATA** action is used to select the metadata for a file or folder and store it in a variable.

The input parameters to select the metadata of a file or folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to select the metadata for. |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to select the metadata for. |
| nodeId | String | *Requires one.* The ID of the node to select the metadata for. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the node to select the metadata for. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| underscoreMetadata | Boolean | *Optional.* If set to `true`, the output `metadata` will have its namespace prefixes written with `_` instead of `:`, for example `cm_title` instead of `cm:title`. This allows the JSON to be used in an expression, for example `${metadata.cm_title}`, whereas `${metadata.cm:title}` is not valid. |

The output parameters from selecting the metadata of a file or folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call selecting the metadata of the file or folder. |
| metadata | Content-Metadata | *Required.* The metadata of the selected file or folder. This is a JSON object of key value pairs that can be mapped to a process variable of type JSON. See below for an example. |

## Copy and move actions

Cope and move actions are used copy and move files and folders within the repository.

The copy and move actions are:

* [Copy a file](#copy-file)
* [Move a file](#move-file)
* [Copy a folder](#copy-folder)
* [Move a folder](#move-folder)

### Copy file

The **COPY_FILE** action is used to copy a file and place the copy in a new location.

The input parameters to copy a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| sourceFile | File | *Requires one source.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to select the file to copy. |
| sourceId | String | *Requires one source.* The nodeId of the file to copy. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| sourcePath | String | *Requires one source.* The location path or relative path of the file to copy. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| targetFolder | Folder | *Requires one target.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to move the copied file into. |
| targetFolderId | String | *Requires one target.* The nodeId of the folder to move the copied file into. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| targetFolderPath | String | *Requires one target.* The location path or relative path of the folder to move the copied file into. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |

The output parameters from copying a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call copying the file. |
| file | File | *Optional.* The copied file available to be mapped to a [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables). |

### Move file

The **MOVE_FILE** action is used to move a file from one location to another.

The input parameters to move a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| sourceFile | File | *Requires one source.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to select the file to move. |
| sourceId | String | *Requires one source.* The nodeId of the file to move. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| sourcePath | String | *Requires one source.* The location path or relative path of the file to move. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| targetFolder | Folder | *Requires one target.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to move the file into. |
| targetFolderId | String | *Requires one target.* The nodeId of the folder to move the file into. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| targetFolderPath | String | *Requires one target.* The location path or relative path of the folder to move the file into. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |

The output parameters from moving a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call moving the file. |
| file | File | *Optional.* The moved file available to be mapped to a [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables). |

### Copy folder

The **COPY_FOLDER** action is used to copy a folder and place the copy in a new location.

The input parameters to copy a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| sourceFolder | Folder | *Requires one source.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to select the folder to copy. |
| sourceId | String | *Requires one source.* The nodeId of the folder to copy. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| sourcePath | String | *Requires one source.* The location path or relative path of the folder to copy. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| targetFolder | Folder | *Requires one target.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to move the copied folder into. |
| targetFolderId | String | *Requires one target.* The nodeId of the folder to move the copied folder into. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| targetFolderPath | String | *Requires one target.* The location path or relative path of the folder to move the copied folder into. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |

The output parameters from copying a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call copying the folder. |
| folder | Folder | *Optional.* The copied folder available to be mapped to a [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables). |

### Move folder

The **MOVE_FOLDER** action is used to move a folder from one location to another.

The input parameters to move a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| sourceFolder | Folder | *Requires one source.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to select the folder to move. |
| sourceId | String | *Requires one source.* The nodeId of the folder to move. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| sourcePath | String | *Requires one source.* The location path or relative path of the folder to move. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| targetFolder | Folder | *Requires one target.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to move the source folder into. |
| targetFolderId | String | *Requires one target.* The nodeId of the folder to move the source folder into. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| targetFolderPath | String | *Requires one target.* The location path or relative path of where to move the source folder into. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |

The output parameters from moving a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call moving the folder. |
| folder | Folder | *Optional.* The moved folder available to be mapped to a [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables). |

## Update actions

Update actions are used to update the contents of files and folders as well as setting other properties on nodes, such as permissions, tags, aspects and lock status.

The update actions are:

* [Update the contents of a file](#update-file-content)
* [Update the metadata of a node](#update-metadata)
* [Set permissions on a node](#set-permissions)
* [Lock a node](#lock-node)
* [Unlock a node](#unlock-node)
* [Add an aspect to a node](#add-aspect)
* [Remove an aspect from a node](#remove-aspect)
* [Update tags for a node](#update-tag)
* [Set the content type of a node](#set-type)

### Update file content

The **UPDATE_FILE_CONTENT** action is used to update the contents of a file, creating a new version of it.

The input parameters to update the content of a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| targetFile | File | *Requires one target.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file that should be updated. |
| targetFileId | String | *Requires one target.* The nodeId of the file to that should be updated. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| targetFilePath | String | *Requires one target.* The location path or relative path of the file that should be updated. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| sourceFile | File | *Requires one source.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file that is the new, updated file. |
| sourceText | String | *Requires one source.* The new source for the file described as a block of text. |
| sourceJson | JSON | *Requires one source.* The new source for the file described in JSON format.
| newName | String | *Optional.* A new file name for the file being updated, including the file extension. For example `updated_draft.txt`. |
| majorVersion | Boolean | *Optional.* If set to `true` then the update will create a new major version of the file. |
| versionComment | String | *Optional.* A comment that will appear in the version history of the updated file. |

The output parameters from updating the contents of a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call updating the contents of the file. |

### Update metadata

The **UPDATE_METADATA** action is used to update the metadata for a file or folder.

The input parameters to update the metadata of a file or folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to update. |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to update. |
| nodeId | String | *Requires one.* The ID of the node to update. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the node to update. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| metadata | Content-Metadata | *Required.* Metadata to update the file or folder with. This is a JSON object of key value pairs. See below for an example. |
| underscoreMetadata | Boolean | *Optional.* If set to `true`, the input `metadata` can have its namespace prefixes written with `_` instead of `:`, for example `cm_title` instead of `cm:title`. The output `response` will also have its prefixes replaced. This allows the JSON to be used in an expression, for example `${metadata.cm_title}`, whereas `${metadata.cm:title}` is not valid. |

> **Note**: `underscoreMetadata` can be set to `true` and the `metadata` input can still use `:` with the service successfully executing the action. If `underscoreMetadata` is set to `false` and `metadata` uses `_` then the service will fail to execute the action.

An example of the `metadata` that can be sent with the file or folder is:

```json
{
"ahr:contract-type": "Full Time",
"ahr:full-name": "John Doe",
"ahr:role": "Developer"
}
```

The output parameters from updating the metadata of a file or folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call updating the metadata of the file or folder. |

### Set permissions

The **SET_PERMISSIONS** action is used to assign roles to a list of users on a file or folder.

The input parameters to set permissions are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to set the permissions for. |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to set the permissions for. |
| nodeId | String | *Requires one.* The ID of the node to set the permissions for. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the node to set the permission for. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| users | Array | *Required.* An array of users to give the permissions to, for example `hruser, salesuser` or `["hruser", "salesuser"]`. |
| role | String | *Required.* The role to provide to the users, for example `Contributor`. |

The output parameters from setting permissions are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call setting permissions. |

### Lock node

The **LOCK_NODE** action is used to lock a file or folder so that it cannot be edited.

The input parameters to lock a node are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to lock. |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to lock. |
| nodeId | String | *Requires one.* The ID of the node to lock. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the node to lock. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| lockType | String | *Required.* The type of lock to apply to the node: {::nomarkdown} <ul><li><b>ALLOW_OWNER_CHANGES</b>: Allows the owner of the node to continue to edit it. This is the default value.</li><li><b>FULL</b>: No changes can be made to the node until it is unlocked.</li></ul>{:/} |
| timeToExpire | Integer | *Required.* The number of seconds until the lock expires. If set to `0` then the lock will not expire until it is explicitly unlocked using an [unlock](#unlock-node) event. |
| lifetime | String | *Required.* Set whether the lock is persisted in the database or not, the possible values are: {::nomarkdown} <ul><li><b>PERSISTENT</b>:  The lock will be persisted in the database. This is the default value.</li><li><b>EPHEMERAL</b>: The lock will be a volatile in-memory lock. This should be used if frequent short-term locks are being used that don't need to be kept when the repository restarts to avoid the overhead of writing to the database.</li></ul>{:/} |

The output parameters from locking a file or folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call locking the file or folder. |

### Unlock node

The **UNLOCK_NODE** action is used to unlock a locked file or folder so that it is editable.

The input parameters to unlock a node are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to unlock. |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to unlock. |
| nodeId | String | *Requires one.* The ID of the node to unlock. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the node to unlock. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |

The output parameters from unlocking a file or folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call unlocking the file or folder. |

### Add aspect

The **ADD_ASPECT** action is used to add an aspect to a file or folder.

The input parameters to add an aspect are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to add the aspect to. |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to add the aspect to. |
| nodeId | String | *Requires one.* The ID of the node to add the aspect to. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the node to add the aspect to. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| aspect | Content-Aspect-Selector | *Required.* The aspect to add to the file or folder, for example `rv:reviewable`. |
| nodeMetadata | Content-Metadata | *Optional.* Metadata to store with the file or folder. This is a JSON object of key value pairs. See below for an example. |
| underscoreMetadata | Boolean | *Optional.* If set to `true`, the input `nodeMetadata` can have its namespace prefixes written with `_` instead of `:`, for example `cm_title` instead of `cm:title`. The output `response` will also have its prefixes replaced. This allows the JSON to be used in an expression, for example `${metadata.cm_title}`, whereas `${metadata.cm:title}` is not valid. |

> **Note**: `underscoreMetadata` can be set to `true` and the `nodeMetadata` input can still use `:` with the service successfully executing the action. If `underscoreMetadata` is set to `false` and `nodeMetadata` uses `_` then the service will fail to execute the action.

An example of the `nodeMetadata` that can be sent with the file or folder is:

```json
{
"ahr:contract-type": "Full Time",
"ahr:full-name": "John Doe",
"ahr:role": "Developer"
}
```

The output parameters from adding an aspect are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call adding the aspect. |

### Remove aspect

The **REMOVE_ASPECT** action is used to remove an aspect from a file or folder.

The input parameters to remove an aspect are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to remove the aspect from. |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to remove the aspect from. |
| nodeId | String | *Requires one.* The ID of the node to remove the aspect from. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the node to remove the aspect from. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| aspect | Content-Aspect-Selector | *Required.* The aspect to remove from the file or folder, for example `rv:reviewable`. |

The output parameters from removing an aspect are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call removing the aspect. |

### Update tag

The **UPDATE_TAG** action is used to update the tags for a file or folder.

The input parameters to update tags are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to update the tags for. |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to update the tags for. |
| nodeId | String | *Requires one.* The ID of the node to update the tags for. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the node to update the tags for. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| tags | Array | *Required.* A list of tags to update for the file or folder, for example `wip, draft` or `["wip", "draft"]`. |

The output parameters from updating tags are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call updating tags. |

### Set type

The **SET_TYPE** action is used to set the content type for a file or folder.

The input parameters to set the type of a file or folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to set the type for. |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to set the type for. |
| nodeId | String | *Requires one.* The ID of the node to set the type for. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| path | String | *Requires one.* The location path or relative path of the node to set the type for. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| nodeType | Content-Type-Selector | *Required.* The type to set for the file or folder, for example `fin:invoice`. |
| nodeMetadata | Content-Metadata | *Optional.* Metadata to store with the file or folder. This is a JSON object of key value pairs. See below for an example. |
| underscoreMetadata | Boolean | *Optional.* If set to `true`, the input `nodeMetadata` can have its namespace prefixes written with `_` instead of `:`, for example `cm_title` instead of `cm:title`. The output `response` will also have its prefixes replaced. This allows the JSON to be used in an expression, for example `${metadata.cm_title}`, whereas `${metadata.cm:title}` is not valid. |

> **Note**: `underscoreMetadata` can be set to `true` and the `nodeMetadata` input can still use `:` with the service successfully executing the action. If `underscoreMetadata` is set to `false` and `nodeMetadata` uses `_` then the service will fail to execute the action.

An example of the `nodeMetadata` that can be sent with the file or folder is:

```json
{
"ahr:contract-type": "Full Time",
"ahr:full-name": "John Doe",
"ahr:role": "Developer"
}
```

The output parameters from setting the type of a file or folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call selecting the metadata of the file or folder. |

## Governance actions

The governance actions are used to declare content as records in the repository.

> **Note:** Governance actions require [Alfresco Governance Services]({% link governance-services/latest/index.md %}) to be installed in Alfresco Cloud.

The governance actions are:

* [Declare a record](#declare-record)

### Declare record

The **DECLARE_RECORD** action is used to declare a file as a record.

The input parameters to declare a record are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to declare as a record. |
| fileId | String | *Requires one.* The nodeId of the file to declare as a record. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| filePath | String | *Requires one.* The location path or relative path of the file to declare as a record. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |
| hideRecord | Boolean | *Optional.* Set whether the record is hidden from its current parent folder, for example `true`. |
| targetFolder | Folder | *Optional.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to store the record in. |
| targetFolderId | String | *Optional.* The nodeId of the folder to store the record in. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| targetFolderPath | String | *Optional.* The location path or relative path of the folder to store the record in. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |

The output parameters from declaring a record are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call declaring the record. |

## Security Marks

The **ADD_SECURITY_MARKS** action is used to add security marks to specific content.  
To add security marks in Process Automation you must have configured security marks in Governance Services. For information on security marks in Governance Services, see [Security Marks and Classification
]({% link governance-services/latest/using/smc.md %})

The input parameters from add security marks are:

| Property | Type | Description |
| -------- | ---- | ----------- |
| file | file | *Required.* Alfresco Content Services file to be updated. File variables are initialised by content actions or content events in triggers. E.g: 'Initialise a file variable by mapping it to the output of the generated document task. |
| folder | folder | *Required.* Alfresco Content Services folder to be updated. Folder variables are initialised by content actions or content events in triggers. |
| path | String | *Required.* Location or relative path of the node to be updated. For example, a location path could be `/app:company_home/app:user_homes/cm:hruser` and a relative path could be `/User Homes/hruser` (by default the relative path is from Company Home). |  
| nodeId | String | *Required.* Node ID of the file or folder in Alfresco Content Services. For example: `a6a977a6-c728-4038-8dbc-d914c4d8cfb3`. |
| securityGroupName | String | *Required.* Security group that contains the security marks to be assigned. E.g: 'PII'. |
| securityMarks | array | *Required.* Array including the name of the security marks to be added. |

The output parameters from add security marks are:

| Property | Type | Description |
| -------- | ---- | ----------- |
| response | json | Response for the calls. |

The **GET_SECURITY_MARKS** action is used to get security marks from specific content.

The input parameters from get security marks are:

| Property | Type | Description |
| -------- | ---- | ----------- |
| file | file | *Required.* Alfresco Content Services file from which security maks are retrieved. File variables are initialised by content actions or content events in triggers. E.g: 'Initialise a file variable by mapping it to the output of the generated document task. |
| folder | folder | *Required.* Alfresco Content Services folder from which security maks are retrieved. Folder variables are initialised by content actions or content events in triggers. |
| path | String | *Required.* Location or relative path of the node in Alfresco Content Services. For example a location path could be `/app:company_home/app:user_homes/cm:hruser` and a relative path could be `/User Homes/hruser` (by default the relative path is from Company Home). |
| nodeId | String | *Required.* Node ID of the file or folder in Alfresco Content Services. Example:\n'a6a977a6-c728-4038-8dbc-d914c4d8cfb3 |
| securityGroupName | String | *Required.* Security group that contains the security marks to be assigned. E.g: 'PII'. |

The output parameters from get security marks are:

| Property | Type | Description |
| -------- | ---- | ----------- |
| response | json | Response for the calls. |
| securityMarks | array | Array including security marks of the node for the provided security group. |

## Delete actions

The delete actions are used to delete files and folders from the repository.

The delete actions are:

* [Delete a file](#delete-file)
* [Delete a folder](#delete-folder)

### Delete file

The **DELETE_FILE** action is used to delete a file.

The input parameters to delete a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file to delete. |
| fileId | String | *Requires one.* The nodeID of the file to delete. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| permanent | Boolean | *Optional.*  If set to `true` the file will be deleted permanently and not moved to the trashcan. |

The output parameters from deleting a file are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call deleting the file. |

### Delete folder

The **DELETE_FOLDER** action is used to delete a folder.

The input parameters to delete a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| folder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to delete. |
| folderId | String | *Requires one.* The nodeID of the folder to delete. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| permanent | Boolean | *Optional.*  If set to `true` the folder will be deleted permanently and not moved to the trashcan. |

The output parameters from deleting a folder are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| response | JSON | *Optional.* The response from the call deleting the folder. |

## Errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the Content service are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| INVALID_RESULT_FORMAT | The service result payload cannot be parsed. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| BAD_REQUEST | The server could not understand the request due to invalid syntax. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refuses to authorize it. |
| NOT_FOUND | The server could not find what was requested. |
| METHOD_NOT_ALLOWED | The request method is known by the server but is not supported. |
| NOT_ACCEPTABLE | The server cannot produce a response matching the list of acceptable values. |
| REQUEST_TIMEOUT | The server would like to shut down this unused connection. |
| CONFLICT | The request conflicts with current state of the server. |
| GONE | No longer available. |
| UNPROCESSABLE_ENTITY | The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions. |
| LOCKED | The resource that is being accessed is locked. |
| FAILED_DEPENDENCY | The request failed due to failure of a previous request. |
| INTERNAL_SERVER_ERROR | The server has encountered a situation it doesn't know how to handle. |
| NOT_IMPLEMENTED | The request method is not supported by the server and cannot be handled. |
| BAD_GATEWAY | The server got an invalid response. |
| SERVICE_UNAVAILABLE | The server is not ready to handle the request. |
| GATEWAY_TIMEOUT | The server is acting as a gateway and cannot get a response in time. |
---
title: Database connectors
---

There are three database connectors that can be used to execute queries against:

* [MariaDB](#mariadb)
* [PostgreSQL](#postgresql)
* [Microsoft SQL Server](#microsoft-sql-server)

> **Note:** The Oracle connector has been removed due to issues with its licensing.

All database connectors are displayed on the process diagram with their respective logos.

> **Important**: All databases should be hosted outside of the Alfresco hosted environment and should be created and managed by customers.

> **Note**: All queries are sent as prepared statements using parameters. SQL injection is not possible.

## MariaDB

The [MariaDB](https://mariadb.org/){:target="_blank"} connector has four actions it can execute: **INSERT**, **UPDATE**, **DELETE** and **SELECT**.

### MariaDB insert

The MariaDB **INSERT** action is used to execute an insert statement against a MariaDB database.

The input parameters for an insert statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
INSERT INTO flavors (flavor)
VALUES ({type});
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from an insert statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* The number of rows in the database that were affected by the statement. |

### MariaDB update

The MariaDB **UPDATE** action is used to execute an update statement against a MariaDB database.

The input parameters for an update statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
UPDATE flavors
SET flavor = {type}
WHERE flavor = "mint-choc";
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from an update statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* The number of rows in the database that were affected by the statement. |

### MariaDB delete

The MariaDB **DELETE** action is used to execute a delete statement against a MariaDB database.

The input parameters for a delete statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
DELETE FROM flavors
WHERE flavor = {type};
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from a delete statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* The number of rows in the database that were affected by the statement. |

### MariaDB select

The MariaDB **SELECT** action is used to execute a select query against a MariaDB database.

The input parameters for an insert statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
SELECT TOP 10 * FROM flavors
WHERE flavor = {type}
ORDER BY ingredients DESC;
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from a select query are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* A JSON object containing the selected data. |

### MariaDB configuration parameters

The configuration parameters for the MariaDB connector are:

| Parameter | Description |
| --------- | ----------- |
| DB_USERNAME | *Required.* The database user to execute the statement as, for example `connector-user`. |
| DB_PASSWORD | *Required.* The password for the database user executing the statement. |
| MARIADB_HOST | *Optional.* The host address of the database, for example `mariadb.example.com`. |
| MARIADB_PORT | *Optional.* The port of the hosted database, for example `421`. |
| DB_NAME | *Optional.* The name of the database to execute the statement against, for example `inventory`. |
| DB_DATASOURCE | *Required.* The database datasource, the default value is a concatenation of `MARIADB_HOST`, `MARIADB_PORT` and `DB_NAME`: `jdbc:mysql://${MARIADB_HOST}:${MARIADB_PORT}/${DB_NAME}`. |
| DB_DRIVER_CLASS_NAME | *Optional.* The database driver to use. The default value is `org.mariadb.jdbc.Driver`. |

### MariaDB errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the MariaDB connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| DATA_ACCESS_ERROR | Unable to access data. |
| DATA_INTEGRITY_VIOLATION_ERROR | Data integrity violation error occurs when performing database operation. |
| CONNECTION_ERROR | Cannot connect to a database instance. |
| SQL_GRAMMAR_ERROR | Invalid syntax error. |
| DUPLICATE_KEY_ERROR | Duplicate key error occurs when performing database operation. |
| OPTIMISTIC_LOCK_ERROR | Optimistic error occurs when performing database operation. |
| DEAD_LOCK_ERROR | Deadlock error occurs when performing database operation. |
| PERMISSION_DENIED_ERROR | Lack of permission to the resource and method requested. |
| UNKNOWN_ERROR | Unexpected runtime error. |

## PostgreSQL

The [PostgreSQL](https://www.postgresql.org/){:target="_blank"} connector has four actions it can execute: **INSERT**, **UPDATE**, **DELETE** and **SELECT**.

### PostgreSQL insert

The PostgreSQL **INSERT** action is used to execute an insert statement against a PostgreSQL database.

The input parameters for an insert statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
INSERT INTO flavors (flavor)
VALUES ({type});
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from an insert statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* The number of rows in the database that were affected by the statement. |

### PostgreSQL update

The PostgreSQL **UPDATE** action is used to execute an update statement against a PostgreSQL database.

The input parameters for an update statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
UPDATE flavors
SET flavor = {type}
WHERE flavor = "mint-choc";
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from an update statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* The number of rows in the database that were affected by the statement. |

### PostgreSQL delete

The PostgreSQL **DELETE** action is used to execute a delete statement against a PostgreSQL database.

The input parameters for a delete statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
DELETE FROM flavors
WHERE flavor = {type};
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from a delete statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* The number of rows in the database that were affected by the statement. |

### PostgreSQL select

The PostgreSQL **SELECT** action is used to execute a select query against a PostgreSQL database.

The input parameters for an insert statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
SELECT TOP 10 * FROM flavors
WHERE flavor = {type}
ORDER BY ingredients DESC;
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from a select query are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* A JSON object containing the selected data. |

### PostgreSQL configuration parameters

The configuration parameters for the PostgreSQL connector are:

| Parameter | Description |
| --------- | ----------- |
| DB_USERNAME | *Required.* The database user to execute the statement as, for example `connector-user`. |
| DB_PASSWORD | *Required.* The password for the database user executing the statement. |
| POSTGRES_HOST | *Optional.* The host address of the database, for example `postgres.example.com`. |
| POSTGRES_PORT | *Optional.* The port of the hosted database, for example `421`. |
| DB_NAME | *Optional.* The name of the database to execute the statement against, for example `inventory`. |
| DB_DATASOURCE | *Required.* The database datasource, the default value is a concatenation of `POSTGRES_HOST`, `POSTGRES_PORT` and `DB_NAME`: `jdbc:postgresql://${POSTGRES_HOST}:${POSTGRES_PORT}/${DB_NAME}`. |
| DB_DRIVER_CLASS_NAME | *Optional.* The database driver to use. The default value is `org.postgresql.Driver`. |

### PostgreSQL errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the PostgreSQL connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| DATA_ACCESS_ERROR | Unable to access data. |
| DATA_INTEGRITY_VIOLATION_ERROR | Data integrity violation error occurs when performing database operation. |
| CONNECTION_ERROR | Cannot connect to a database instance. |
| SQL_GRAMMAR_ERROR | Invalid syntax error. |
| DUPLICATE_KEY_ERROR | Duplicate key error occurs when performing database operation. |
| OPTIMISTIC_LOCK_ERROR | Optimistic error occurs when performing database operation. |
| DEAD_LOCK_ERROR | Deadlock error occurs when performing database operation. |
| PERMISSION_DENIED_ERROR | Lack of permission to the resource and method requested. |
| UNKNOWN_ERROR | Unexpected runtime error. |

## Microsoft SQL Server

The [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server/sql-server-2019){:target="_blank"} connector has four actions it can execute: **INSERT**, **UPDATE**, **DELETE** and **SELECT**.

### SQL Server insert

The SQL Server **INSERT** action is used to execute an insert statement against a SQL Server database.

The input parameters for an insert statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
INSERT INTO flavors (flavor)
VALUES ({type});
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from an insert statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* The number of rows in the database that were affected by the statement. |

### SQL Server update

The SQL Server **UPDATE** action is used to execute an update statement against a SQL Server database.

The input parameters for an update statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
UPDATE flavors
SET flavor = {type}
WHERE flavor = "mint-choc";
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from an update statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* The number of rows in the database that were affected by the statement. |

### SQL Server delete

The SQL Server **DELETE** action is used to execute a delete statement against a SQL Server database.

The input parameters for a delete statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
DELETE FROM flavors
WHERE flavor = {type};
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from a delete statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* The number of rows in the database that were affected by the statement. |

### SQL Server select

The SQL Server **SELECT** action is used to execute a select query against a SQL Server database.

The input parameters for an insert statement are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| query | String | *Required.* The query to execute against the database. |
| metadata | JSON | *Optional.* The list of parameters to pass to the query. |

The `metadata` parameter can be used to pass variables into the `query` parameter.

For example, if the contents of `metadata` are:

```json
{
"type" : "mint"
}
```

This can be used in the `query` parameter as:

```sql
SELECT TOP 10 * FROM flavors
WHERE flavor = {type}
ORDER BY ingredients DESC;
```

> **Note:** The `{ }` are declared without quotations.

The output parameters from a select query are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| result | Integer | *Optional.* A JSON object containing the selected data. |

### SQL Server configuration parameters

The configuration parameters for the SQL Server connector are:

| Parameter | Description |
| --------- | ----------- |
| DB_USERNAME | *Required.* The database user to execute the statement as, for example `connector-user`. |
| DB_PASSWORD | *Required.* The password for the database user executing the statement. |
| SQLSERVER_HOST | *Optional.* The host address of the database, for example `sqlserver.example.com`. |
| SQLSERVER_PORT | *Optional.* The port of the hosted database, for example `421`. |
| DB_NAME | *Optional.* The name of the database to execute the statement against, for example `inventory`. |
| DB_DATASOURCE | *Required.* The database datasource, the default value is a concatenation of `SQLSERVER_HOST`, `SQLSERVER_PORT` and `DB_NAME`: `jdbc:sqlserver://${SQLSERVER_HOST}:${SQLSERVER_PORT}/${DB_NAME}`. |
| DB_DRIVER_CLASS_NAME | *Optional.* The database driver to use. The default value is `com.microsoft.sqlserver.jdbc.SQLServerDriver`. |

### SQL Server errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the SQL Server connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| DATA_ACCESS_ERROR | Unable to access data. |
| DATA_INTEGRITY_VIOLATION_ERROR | Data integrity violation error occurs when performing database operation. |
| CONNECTION_ERROR | Cannot connect to a database instance. |
| SQL_GRAMMAR_ERROR | Invalid syntax error. |
| DUPLICATE_KEY_ERROR | Duplicate key error occurs when performing database operation. |
| OPTIMISTIC_LOCK_ERROR | Optimistic error occurs when performing database operation. |
| DEAD_LOCK_ERROR | Deadlock error occurs when performing database operation. |
| PERMISSION_DENIED_ERROR | Lack of permission to the resource and method requested. |
| UNKNOWN_ERROR | Unexpected runtime error. |---
title: DocuSign connector
---

The DocuSign connector provides a standard mechanism in Alfresco Process Automation to send documents for digital signing in
[DocuSign](https://www.docusign.com){:target="_blank"}. The DocuSign connector is displayed on the process diagram as a pen.

> **Important:** The DocuSign connector requires a DocuSign account to handle document signing. This account is separate to the Alfresco hosted environment and should be created and managed by customers.

The actions that can be executed using the DocuSign connector are:

* [SEND_FOR_SIGNATURE](#send_for_signature)
* [DOWNLOAD_DOCUMENT](#download_document)

As part of the BPMN definition process, any service task that is responsible for sending or downloading a document must set the `docusignconnector.SEND_FOR_SIGNATURE` or `docusignconnector.DOWNLOAD_DOCUMENT` properties as the value for its implementation attribute.

The following input parameters must also be provided for the DocuSign API in the Service task depending on the implementation.

### BPMN Tasks Configuration

This [process definition](https://github.com/Alfresco/alfresco-process-connector-services/blob/develop/alfresco-process-docusign-connector-spring-boot-starter/docuSignProcess.bpmn20.xml){:target="_blank"} shows an example of how to set up the connector in Process Automation.

As part of BPMN definition process, any Service Task responsible for sending the document needs to set `docusignconnector.SEND_FOR_SIGNATURE` or `docusignconnector.DOWNLOAD_DOCUMENT` as the value for its implementation attribute.

In addition to the above, these input variables must be provided for the DocuSign API in the Service Task depending on the implementation:

## SEND_FOR_SIGNATURE

The **SEND_FOR_SIGNATURE** action is used by the DocuSign connector to request a digital signature on a document.

The input parameters for SEND_FOR_SIGNATURE are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| signers | JSON | *Optional.* The list of signers, including email, name, sign here page, sign here tab label, position X and position Y, when the document is going to be signed by more than one signer. |
| recipientEmail | String | *Required.* The email address of the signer when the document is going to be signed by only one signer. |
| recipientName | String | *Optional.* The name of the signer, which means the email recipient, when the document is going to be signed by only one signer. |
| emailSubject | String | *Optional.* The subject line of the email sent with the document to sign. |
| metadata | JSON | *Optional.* Metadata of the document. |
| file | File | *Required.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file containing the document to be signed. |
| nodeFormat | String | *Optional.* The format of the document to be signed. Values are `pdf` or `docx`. |
| outputFileName | String | *Optional.* The name of the file that will be created, for example `invoice.pdf`. |
| documentId | Integer | *Optional.* Correlation ID to send to the DocuSign API, for example `250`. |
| signHereTabLabel | String  | *Optional.* **Sign Here** page in the document when the document is only going to be signed by one signer. |
| signHerePage | String | *Optional.* The page number in the document the `Sign Here` box will appear on, when the document is going to be signed by only one signer, for example `3`. |
| signHereX | String | *Optional.* The X position of the `Sign Here` box in the document, when the document is going to be signed by only one signer, for example `100`. |
| signHereY | String | *Optional.* The Y position of the `Sign Here` box in the document, when the document is going to be signed by only one signer, for example `50`. |
| timeout | Integer | *Optional.* The timeout period to wait for the document to be signed in milliseconds, for example `910000`. |
| allowMarkup | Boolean | *Optional.* Allow recipients to make changes to your documents by covering up existing text and replacing it with new text. Recipients can decide to use a special markup text field which they can place anywhere on the document. It can be scaled and optionally filled in. All changes must be reviewed and approved by all signers. |
| agents | JSON | *Optional.* The list of agents, including email and name, assigned as agents to the document. |
| carbonCopies | JSON | *Optional.* The list of carbon copies, including email, name, sign here page, sign here tab label, position X and position Y, assigned as recipients who should receive a copy of the envelope, but do not need to sign it. |
| certifiedDeliveries | JSON | *Optional.* The list of certified deliveries, including email, and name, who are assigned as recipients who must receive the completed documents for the envelope to be completed, but do not need to sign it. |
| editors | JSON | *Optional.* The list of editors, including email and name, assigned as editors on the document. |
| inPersonSigners | JSON | *Optional.* The list of in person signers, including email, name, signerName, hostName, sign here page, sign here tab label, position X and position Y, assigned as signers that are in the same physical location as a DocuSign user. These users act as a Signing Host for the transaction. The signer name and the host name are mandatory. Signer name is the full legal name of a signer for the envelope. Host name is the name of the signing host. |
| intermediaries | JSON | *Optional.* The list of intermediaries, including email, and name assigned as recipients. You are not required to add name and email information for recipients at the same level or subsequent level in the routing order, until subsequent agents, editors, or intermediary recipient types are added. |
| notaries | JSON | *Optional.* The list of notaries, including email, name, sign here page, sign here tab label, position X and position Y, assigned as notaries on the document. |
| witnesses | JSON | *Optional.* The list of witnesses including email, name, sign here page, sign here tab label, position X and position Y, assigned as witnesses on the document. |

> **Note:** The connector can only receive either **signers** or **recipientEmail** but not both at the same time. The connector must receive either **signHereTabLabel** or **signHerePage** to fixed the positioning. If one of them is null the signature can be where the signer selects.

The output parameters from SEND_FOR_SIGNATURE are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| envelopeId | String | Envelope ID of the document. |
| status | String | Status of the envelope. |
| URI | String | URI related to the envelope. |
| docusignOutput | JSON | DocuSign output after sending the document for signature. |

## DOWNLOAD_DOCUMENT

The **DOWNLOAD_DOCUMENT** action is used by the DocuSign connector to download the envelope from DocuSign. It takes into account the `envelopeId` that is the UUID that relates to the envelope.

The input parameters for DOWNLOAD_DOCUMENT are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| outputFileName | String | *Optional.* The name of the file that will be created, for example `invoice.pdf`. |
| envelopeId | String | *Required.* UUID related to the envelope from the DocuSign API. |
| targetFolder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to store the signed document in. |
| targetFolderId | String | *Optional.* The target folder ID to save the document in Content Services. |
| targetFolderPath | String | *Requires one.* The location path or relative path of the folder to store the signed document in Content Services. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` or a relative path: `/User Homes/hruser`.  |
| targetFileType | String | *Optional.* The type to set for the signed file, for example `fin:invoice`. |
| targetFileMetadata | Content-Metadata | *Optional.* Metadata assigned to the signed document in Content Services. |
| underscoreMetadata | Boolean | *Optional.* If set to `true` the received prefixed property names contain underscores (_) instead of colons (:) for separating the namespace prefix from the property name. |

The output parameters from DOWNLOAD_DOCUMENT are:

| Property  | Type | Description |
| --------- | ---- | ----------- |
| file | File | The file stored in Content Services of the document. |

No exceptions or errors are thrown by the connector, however all exceptions are caught and logged. The task execution is always successful, and errors will be returned in an error event.

The following is an example of the POST body for the Activiti REST API endpoint `http://{{domain}}/{{applicationName}}-rb/v1/process-instances`:

```JSON
{
  "processDefinitionKey": "DocuSignProcessTest",
  "processInstanceName": "processDocuSignTest_Simple",
  "businessKey": "MyBusinessKey",
  "variables": {
  	"recipientEmail" : "test@test.com",
  	"recipientName" : "AAE Test",
  	"emailSubject" : "Sign this document",
    "files" : [
        {
  	        "nodeId" : "<node-id-of-document-to-be-signed>"
        }
    ],
  	"outputFileName" : "testFileName.docx",
  	"nodeFormat" : "docx",
  	"documentId" : "10",
  	"signHerePage" : "1",
  	"signHereX" : "100",
  	"signHereY" : "200",
  	"timeout: "3600"
  },
  "payloadType":"StartProcessPayload"
}
```

In the business process definition, the service task called **docuSignTask** has the implementation attribute configured to use the connector.

```bash
<bpmn2:serviceTask id="ServiceTask_1cheezm" name="docuSignTask" implementation="docuSignConnector.SEND_FOR_SIGNATURE">
      <bpmn2:incoming>SequenceFlow_1siaofh</bpmn2:incoming>
      <bpmn2:outgoing>SequenceFlow_0nmtcso</bpmn2:outgoing>
</bpmn2:serviceTask>
```

No exceptions or errors are thrown by the connector. All exceptions are caught and logged. The task execution is always successful, and errors will be returned in an error event.

### Configuration

1. Log into the DocuSign eSignature console and click Settings on the top right.

2. Click the **ADD CONFIGURATION** dropdown list and select **Custom**.

3. Under Listener Settings, select **Active Connection** from the **Status** dropdown list.

4. Under Listener Settings, enter your **URL to Publish** URL.

    The pattern of the URL must follow: `{domain-name}/{application-name}/connector/{connector_name}/listener`.

5. Under Event Settings, select **Aggregate** from the **Event Message Delivery Mode** dropdown list.

6. Under **Event settings > Trigger events > Envelope Events**, ensure the following are selected:

    * **Envelope Sent**
    * **Envelope Delivered**
    * **Envelope Signed/Completed**
    * **Envelope Declined**
    * **Envelope Voided**

7. Under **Event settings > Trigger events > Recipient Events**, ensure the following are selected:

    * **Recipient Sent**
    * **Recipient Auto Responded**
    * **Recipient Delivered**
    * **Recipient Signed/Completed**
    * **Recipient Declined**
    * **Recipient Authentication Failure**

8. Click **SAVE CONFIGURATION**.

![Settings]({% link process-automation/images/settings.png %})

#### Logs and failures

Once the listener has been created and is working you can see the logs and the failures from the same menu. You can click on one of the logs or failures and a popup with information is displayed.

#### Triggers for DocuSign events

1. From the Modeling Application, create a new trigger with one of the [events](#events).

2. You can filter the trigger using the condition field, which is an expression that must be true in order to trigger an action.

### DocuSign Environment Configuration

The connector uses the DocuSign client library that relies on the DocuSign REST API and uses OAuth JWT for authentication, for more see [OAuth JWT](https://developers.docusign.com/esign-rest-api/guides/authentication/oauth2-jsonwebtoken){:target="_blank"}.

The basic steps to achieve this are:

1. Create a DocuSign account, for more see [Sign documents for free](https://www.docusign.co.uk/esignature/sign-documents-free){:target="_blank"}.

    Register for a free developer sandbox account.

2. Configure an app for JWT in DocuSign, for more see [How to get an access token with JWT Grant authentication](https://developers.docusign.com/esign-rest-api/guides/authentication/oauth2-jsonwebtoken){:target="_blank"}.

    You need the private RSA key for the connector configuration.

3. Grant consent to the app, for more see [How to obtain individual consent](https://developers.docusign.com/esign-rest-api/guides/authentication/obtaining-consent){:target="_blank"}.

    The same user account from step 1. can be used, or a new one can be created.

### Events

The DocuSign connector produces events when the DocuSign envelope changes its status.

> **Note:** These events can be consumed by the process using Triggers. For example, a BPMN catch message event inside a process can be waiting for a trigger event that is set to `ENVELOPE_DECLINED`, and a trigger action set to throw a BPMN message.

The events are:

* `ENVELOPE_VOIDED` -  The envelope has been voided by the sender or has expired. The void reason indicates whether the envelope was manually voided or expired.
* `ENVELOPE_DECLINED` - The envelope has been declined by one of the recipients.
* `ENVELOPE_COMPLETED` - The envelope has been completed by all of the recipients.
* `ENVELOPE_DELIVERED` - This event is sent when all recipients have opened the envelope through the DocuSign signing website. This does not signify an email delivery of an envelope.
* `ENVELOPE_SENT` - This event is sent when the email notification, with a link to the envelope, is sent to at least one recipient or when it is a recipient's turn to sign during embedded signing. The envelope remains in this state until all recipients have viewed the envelope.

For more on events see [Webhook event triggers](https://developers.docusign.com/platform/webhooks/connect/event-triggers/){:target="_blank"}.

When a Process Automation process is instantiated this way, the following variables are populated:

| Property | Type | Description |
| -------- | ---- | ----------- |
| envelopeId | String | Envelope ID of the document. |
| documents | Array | Documents related to the envelope and data related to them like uri, and id. |
| extendedFields | JSON | Additional fields like decline reason etc. |

The connector is listening for events using the webhook that follows the pattern:

`- {domain-name}/{application-name}/connector/{connector_name}/listener`

## Errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the DocuSign connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| MISSING_SOURCE_FILE | Input file not found. |
| MISSING_TARGET_FILE | Target file and folder not found. |
| SIGNING_TIMEOUT | Signing document timeout. |
| STATUS_NOT_FOUND | Error polling DocuSign for status. |
| MISSING_TOKEN | Could not update or obtain token. |
| ERROR_READING_FILE | Error reading input file. |
| ENVELOPE_NOT_CREATED | Could not create envelope in DocuSign. |
| ERROR_WRITING_FILE | Could not create or write result node. |
| ERROR_RETRIEVING_FILE | Could not retrieve document from DocuSign. |
| MISSING_ENVELOPE | The `envelopeId` is missing. |
---
title: Email service
---

The email service is used to send emails using the SMTP protocol as part of a process instance.  

The email service is displayed on the process diagram as an envelope.

> **Important**: The email service requires an email server to use. This server is separate to the Alfresco hosted environment and should be created and managed by customers.

## Send

The **SEND** action is used by the email service to send an email and optional attachments.

The input parameters to send an email are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| to | String | *Required.* The email addresses to send to, for example `jane.doe@jdoe.com`. Multiple addresses are separated by a comma. |
| from  | String | *Required.* The email address of the sender, for example `noreply@jdoe.com`. |
| cc | String | *Optional.* A carbon copy list of email addresses. Multiple addresses are separated by a comma. |
| bcc | String | *Optional.* A blind carbon copy list of email addresses. Multiple addresses are separated by a comma. |
| subject | String | *Optional.* The subject line of the email, for example `Order No: 1234`. |
| attachments | File | *Optional.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file containing attachments to send with the email. |
| charset | String | *Optional* Set the character set of the email, for example `UTF-8`. |
| html | String | *Optional.* The body of the email in HTML, for example `<p><b>Hello!</b></p>`. |
| text | String | *Optional.* The body of the email in plain non-rich text. Can be sent in addition to `html` and will be used as a fall-back if HTML is not supported by the email client reading the email. |
| template | File | *Optional.* The body of the email generated from a [FreeMarker template](https://freemarker.apache.org/docs/dgui_quickstart_basics.html){:target="_blank"} stored as a file variable. |
| metadata | JSON | *Optional.* Metadata to be used by the `template` when generating the file to include [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) in the output. |

### Template

A [FreeMarker template](https://freemarker.apache.org/docs/dgui_quickstart_basics.html){:target="_blank"} can be used to generate the body of the email. Optional metadata can also be used with the template to insert values from [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) into the document template.

An example of the `metadata` that can be used by the template is:

```json
{
"iceCream": {
	"flavor":"Mint"
	},
"timeOfYear": {
	"season":"Summer"
	}
}
```

An example of how the template can import values from the `metadata` is:

```html
<html>
<head>
  <title>Welcome!</title>
</head>
<body>
  <h1>Welcome to ${timeOfYear.season}!</h1>
  <p>Our latest product is ${iceCream.flavor} ice cream!</p>
</body>
</html>
```

## Configuration parameters

The configuration parameters for the email service are:

| Parameter | Description |
| --------- | ----------- |
| EMAIL_HOST | *Required.* The host address of the email server. |
| EMAIL_PORT | *Required.* The port the email server is running on. |
| EMAIL_USERNAME | *Required.* The username the connector will use to contact the email server. |
| EMAIL_PASSWORD | *Required.* The password of the user the connector will use to contact the email server. |
| EMAIL_SMTP_AUTH | *Required.* Sets whether the connection to the email server requires authentication, for example `true`. |
| EMAIL_SMTP_STARTTLS | *Required.*  Sets whether the connection uses TLS, for example `true`. |

## Errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the email service are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| TEMPLATE_READ_ERROR | Cannot read the FreeMarker template. |
| TEMPLATE_METADATA_ERROR | The template references non-existing metadata. |
| TEMPLATE_SYNTAX_ERROR | Invalid FreeMarker syntax. |
| EMAIL_CONNECTION_ERROR | Unable to connect to the email service. |
| EMAIL_AUTHENTICATION_ERROR | Unable to authenticate into the email service. |
| EMAIL_SEND_ERROR | Unable to send the email. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| BAD_REQUEST | The server could not understand the request due to invalid syntax. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refuses to authorize it. |
| NOT_FOUND | The server could not find what was requested. |
| INTERNAL_SERVER_ERROR | The server has encountered a situation it doesn't know how to handle. |
| BAD_GATEWAY | The server got an invalid response. |
| SERVICE_UNAVAILABLE | The server is not ready to handle the request. |
| GATEWAY_TIMEOUT | The server is acting as a gateway and cannot get a response in time. |
---
title: Generate document
---

The generate document service is used to create DOCX and PDF files using a template. The generated document is then saved to the Content Services repository and can be reused throughout the process.

A generate document task is displayed as a stack of documents on the process diagram.

## Create a generate document task

The generate document service is stored in the palette separate from other connectors. To create a generate document task:

1. Sign into the Modeling Application and open a project and process.

2. Click the stack of documents in the tool palette.

3. The option to use an existing instance of the connector or create a new one will display.

    * **Create a new instance** if it is the first time using the generate document service within the project, and give it a name.

    * Select an existing instance if the generate document service has already been used within the project.

4. Drag the task onto the diagram canvas and fill in the properties.

> **Note**: The generate document service does not have any [configuration parameters]({% link process-automation/latest/model/connectors/index.md %}#configuration-parameters) as it connects directly to the Content Services repository. This means that only a single instance of the connector is required per project.

## Properties

The generate document service is implemented as a [service task]({% link process-automation/latest/model/processes/bpmn.md %}#service-task). All the properties available to a service task are those required by the generate document service. The three most important ones to understand for the generate document service are:

| Property | Description |
| -------- | ----------- |
| Implementation | *Required.* Displays the name of the connector the task is using. This will be the name chosen when creating a connector instance. |
| Action | *Required.* Selects which action the connector task should execute, for example `GENERATE`. |
| Mapping type | *Required.* Sets how data should be passed between the connector and the process by mapping the [input and output parameters]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping). For example, setting the details of the file to select and which process variable will store it. |

## Generate

The **GENERATE** action is used to create a new document using a template, store it in the repository and create it as a variable for reuse within the process.

The input parameters to generate a document are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| template | File | *Required.* The [template](#template) to use for generating the file stored as a file variable. |
| metadata | JSON | *Optional.* Metadata to be used by the `template` when generating the file to include [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) in the output. |
| outputFileName | String | *Optional.* The name of the generated file, for example `onboarding-form`. |
| outputFormat | String | *Optional*. The file type for the generated document. Possible values are DOCX and PDF. The default value if PDF. |
| targetFileMetadata | Content-Metadata | *Optional.* Metadata to store the file with. This is a JSON object of key value pairs. See below for an example. |
| underscoreMetadata | Boolean | *Optional.* If set to `true`, the input `targetFileMetadata` can have its namespace prefixes written with `_` instead of `:`, for example `cm_title` instead of `cm:title`. This allows the JSON to be used in an expression, for example `${metadata.cm_title}`, whereas `${metadata.cm:title}` is not valid. |
| targetFileType | Content-Type | *Optional.* The type to set for the generated file, for example `fin:invoice`. |
| targetFile | File | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type file that should be updated. |
| targetFolder | Folder | *Requires one.* A [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) of type folder to store the new file in. |
| targetFolderId | String | *Requires one.* The nodeId of the folder to store the new file in. For example `775a8f2d-8123-49a7-ae1f-f3f49d4eae20`. |
| targetFolderPath | String | *Requires one.* The location path or relative path of the folder to store the new file in. For example, a location path: `/app:company_home/app:user_homes/cm:hruser` and a relative path: `/User Homes/hruser`. |

> **Note**: `underscoreMetadata` can be set to `true` and the `targetFileMetadata` input can still use `:` with the connector successfully executing the action. If `underscoreMetadata` is set to `false` and `targetFileMetadata` uses `_` then the connector will fail to execute the action.

An example of the `targetFileMetadata` that can be stored with the document is:

```json
{
"ahr:contract-type": "Full Time",
"ahr:full-name": "John Doe",
"ahr:role": "Developer"
}
```

The output parameters from generating a document are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| file | File | *Optional.* The generated document available to be mapped to a [variable]({% link process-automation/latest/model/processes/index.md %}#process-variables). |

## Template

A template is used to generate a document. Optional metadata can also be used with the template to insert values from [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) into the document template.

An example of the `metadata` that can be used by the template is:

```json
{
"iceCream": {
	"flavor":"Mint"
	},
"timeOfYear": {
	"season":"Summer"
	}
}
```

An example of how the template can import values from the `metadata` is:

```bash
Current season: <<[timeOfYear.get("season")]>>
Flavor of the month: <<[iceCream.get("flavor")]>>
```

In the generated document this would display as:

```text
Current season: Summer
Flavor of the month: Mint
```

## Errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the generate document service are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| INVALID_RESULT_FORMAT | The REST service result payload cannot be parsed. |
| TEMPLATE_READ_ERROR | Cannot read the document template. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| BAD_REQUEST | The server could not understand the request due to invalid syntax. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refuses to authorize it. |
| NOT_FOUND | The server could not find what was requested. |
| METHOD_NOT_ALLOWED | The request method is known by the server but is not supported. |
| NOT_ACCEPTABLE | The server cannot produce a response matching the list of acceptable values. |
| REQUEST_TIMEOUT | The server would like to shut down this unused connection. |
| CONFLICT | The request conflicts with current state of the server. |
| GONE | No longer available. |
| UNPROCESSABLE_ENTITY | The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions. |
| LOCKED | The resource that is being accessed is locked. |
| FAILED_DEPENDENCY | The request failed due to failure of a previous request. |
| INTERNAL_SERVER_ERROR | The server has encountered a situation it doesn't know how to handle. |
| NOT_IMPLEMENTED | The request method is not supported by the server and cannot be handled. |
| BAD_GATEWAY | The server got an invalid response. |
| SERVICE_UNAVAILABLE | The server is not ready to handle the request. |
| GATEWAY_TIMEOUT | The server is acting as a gateway and cannot get a response in time. |
---
title: Overview of connectors
---

Connectors are used to handle interactions with external systems as part of a process. This includes actions such as retrieving, generating, updating and storing content in the Content Services repository, sending emails and utilizing services such as AWS Textract, Rekognition and Lambda functions.

## Properties

Connectors are implemented as a [service task]({% link process-automation/latest/model/processes/bpmn.md %}#service-task). All the properties available to a service task are those required by a connector. The three most important ones to understand for connectors are:

| Property | Description |
| -------- | ----------- |
| Implementation | *Required.* Displays the name of the connector the task is using. This will be the name chosen when creating a connector instance. |
| Action | *Required.* Selects which action the connector task should execute, for example `SELECT_FILE`. |
| Mapping type | *Required.* Sets how data should be passed between the connector and the process by mapping the [input and output parameters]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping). For example, setting the details of the file to select and which process variable will store it. |

## Create a connector

Connectors are created as [BPMN elements]({% link process-automation/latest/model/processes/bpmn.md %}) by dragging them into a process definition from the palette:

1. Sign into the Modeling Application and open a project and process.

2. Click the image of a plug in the tool palette and select the connector to create.

3. The option to use an existing instance of the connector or create a new one will display.

    * **Create a new instance** if it is the first time using the connector within the project and give it a name.

    * Select an existing instance if the connector has already been used within the project and the tasks will share the same [configuration parameters](#configuration-parameters), for example using the same SMTP provider to send an email.

4. Drag the connector onto the diagram canvas and fill in the properties.

## Add a connector instance to a process

While editing a process, you can add a connector instance in the flow.

1. Create a new instance by selecting the connector type from the toolbar
![Connector toolbar]({% link process-automation/images/connector-toolbar.png %})

2. Once selected, create a new connector instance or use an existing one:
![Create new connector instance]({% link process-automation/images/create-new-connector-instance.png %})

3. Add the connector to the process and configure its properties:
![Configure connector]({% link process-automation/images/configure-connector.png %})

The documentation below covers more details about properties of each individual connector.

## Connector modeling

Every connector instance created in a process definition will be created in the **Connectors** section of a project using the `name` assigned to the instance.

> **Note**: Creating multiple instances of the same connector within a project is only required if different [configuration parameters](#configuration-parameters) are going to be set.

Clicking on a connector instance will display its actions, events, configuration parameters and errors. These properties all stored in JSON format and can be viewed in the **JSON Editor**. Downloading a connector instance will display the contents of the **JSON Editor**.

### Actions

Actions are the operations a connector can take, for example sending a message on Slack and creating a channel in Slack are two different actions. A connector instance can execute any number of actions, however each [service task]({% link process-automation/latest/model/processes/bpmn.md %}#service-task) can only execute one.

Each action has a set of input parameters and output parameters. Input parameters are values sent from the process for the connector to execute, and output parameters are the values the connector sends back to the process after it has executed. The values sent as input and output parameters are defined using the **Mapping type** property on the service task and [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping).

The properties for input and output parameters are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the parameter, for example `userId`. |
| Description | *Optional.* A free text description of the parameter, for example `The ID of a Slack user`. |
| Type | *Required.* The data type of the parameter, for example `String`. |
| Required | *Optional.* Set whether the parameter requires a value when being used, for example `true`. |

An example of the JSON for the Slack connector **SEND_MESSAGE** action is:

```json
    "actions": {
        "88296a50-f6cf-496e-b433-5d794788fc8f": {
            "id": "88296a50-f6cf-496e-b433-5d794788fc8f",
            "name": "SEND_MESSAGE",
            "description": "Sends a standalone message to a Slack conversation. Conversations can be public or private channels, or direct messages.",
            "inputs": [
                {
                    "id": "f7435a5c-20bd-46e4-9d26-901a9dabb87c",
                    "name": "userId",
                    "description": "Internal Slack user id. If present, the message will be sent as a direct message.",
                    "type": "string"
                },
...
            ],
            "outputs": [
                {
                    "id": "c9daca61-6ecd-4dd2-b8b0-f1f99589cd52",
                    "name": "slackError",
                    "description": "If present, it describes the error occurred trying to send the message.",
                    "type": "string"
                },
...
            ]
        },
```

### Events

Events are used as part of defining event criteria in a [trigger]({% link process-automation/latest/model/triggers.md %}). When the event criteria specified in a trigger are met, an action is started. Certain connectors can be used for defining event criteria. For example, the email service event **MESSAGE_RECEIVED** can be used to monitor inbound emails. If a pattern defined in the trigger is met then a trigger action is started.

See [triggers]({% link process-automation/latest/model/triggers.md %}) for further details on creating event criteria based on connectors.

Connector events contain a set of input and output parameters and the definition of the content of the event. Input parameters can be used to define a pattern for when an event should be created and output parameters can be used as values within a trigger action.

The properties for input and output parameters are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the parameter, for example `pattern`. |
| Description | *Optional.* A free text description of the parameter, for example `A regular expression to match against incoming messages`. |
| Type | *Required.* The data type of the parameter, for example `String`. |
| Required | *Optional.* Set whether the parameter requires a value when being used, for example `true`. |

An example of the JSON for the email service **MESSAGE_RECEIVED** event is:

```json
"events": {
        "62bfa43e-a495-4786-9495-1e24eedf1a1f": {
            "id": "62bfa43e-a495-4786-9495-1e24eedf1a1f",
            "name": "EMAIL_RECEIVED",
            "description": "Event that is dispatched when an email is received",
            "inputs": [
                {
                    "id": "3dbe2c22-dfc2-41c6-a576-7797f9fbeb62",
                    "name": "pattern",
                    "description": "Regular expression that any incoming message shall match in order to be published as events. Regular expressions can contain matching groups delimited by '(' and ')'. Matching groups can be used in variables and the echo message.",
                    "type": "string"
                },
...
            ],
            "outputs": [
                {
                    "id": "fa6b0f2a-ca79-476b-ba4e-f0f082eff47c",
                    "name": "matchGroups",
                    "description": "Matching groups between pattern and message. They can be used in variables and the echo messages.",
                    "type": "json"
                },
...
            ],
            "model": {
                "$schema": "https://json-schema.org/draft/2019-09/schema",
                "type": "object",
                "properties": {
                  "emailTo": {
                    "type": "string"
                  },
                  "emailFrom": {
                    "type": "string"
                  },
                  "emailSubject": {
                     "type": "string"
                  },
                  "emailBody": {
                    "type": "string"
                  }
                },
                "required": [
                    "emailTo",
                    "emailFrom"
                ]
            }
        }
    },
```

The `model` field describes the information that is included inside the data field of the Cloud Event handled in a trigger, for more see [Trigger events]({% link process-automation/latest/model/triggers.md %}#events). This allows you to create a condition for a [Trigger]({% link process-automation/latest/model/triggers.md %}) using the [Condition Builder]({% link process-automation/latest/using/index.md %}#condition-builder) and that is based on the event information.
You can add or edit the model of the event in the editor by clicking the **Add Model Schema** or **Edit Model Schema** button.

![Model Schema Editor]({% link process-automation/images/model-schema-editor.png %})

In the editor on the left you can configure a JSON schema to describe an event. In the editor on the right you can enter a JSON object and validate it matches the schema on the left by clicking the `Validate` button. If it matches you will receive a validation success message.

### Configuration parameters

Configuration parameters are the environment variables specific to each connector instance. Environment variables refer to the configuration settings for a connector, for example the AWS account to connect to, the instance of Slack to create a channel in or the SMTP server to use to send emails from.

Multiple instances of the same connector within a project are only required if different configuration parameters are going to be set for the connector tasks used in the process.

The properties of configuration parameters are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the parameter, for example `SLACK_XOXB`. |
| Description | *Optional.* A free text description of what the parameter is for. For example `The Slack bot user token.` |
| Required | *Required.* Set whether the parameter requires a value when being used, for example `true`. |
| Secure | *Optional.* Indicates a sensitive property. Properties that are set as secure cannot have their information entered in the Modeling Application and must be entered during [deployment]({% link process-automation/latest/admin/release.md %}#deployment) to avoid storing them as plain text in the user interface and database. |
| Value | *Optional.* An optional default value for the parameter. This can be overridden at deployment time, for example `xoxb-`. |

The `Value` field for configuration parameters can be filled out during modeling or when the project is [deployed]({% link process-automation/latest/admin/release.md %}#deployment). Even if properties are entered whilst modeling, they can still be overridden at deployment.

> **Note**: Properties marked as `Secure` shouldn't have their values entered whilst modeling.

An example of the JSON for the Slack connector **MESSAGE_RECEIVED** configuration parameters is:

```json
    "config": [
        {
            "name": "SLACK_XOXB",
            "description": "Slack bot user token",
            "value": "",
            "required": true

        },
        {
            "name": "SLACK_XOXP",
            "description": "Slack admin user token",
            "value": "",
            "required": true
        }
    ],
```

### Errors

Connectors have a set of errors defined in their configuration. These errors are thrown when the error occurs in the execution of a connector action and can be caught by [error boundary events]({% link process-automation/latest/model/processes/bpmn.md %}#error-boundary-event) or [error start events]({% link process-automation/latest/model/processes/bpmn.md %}#error-start-event). This allows connector errors to be handled as business errors.

When an error boundary event is attached to a service task that contains a connector, a list of errors that can be thrown by that connector can be selected as the `error` to catch. Error start events will see a list of errors from the connectors in the project.

The properties of errors are:

| Property | Description |
| -------- | ----------- |
| Name | *Required.* The name of the error, for example `INVALID_INPUT`. |
| Description | *Optional.* A free text description of what the parameter is for. For example `An input variable had an invalid type.` |
| Code | *Required.* The error code that will be caught by an error boundary or error start event, for example `INVALID_INPUT`. |

An example of the JSON for the email service **INVALID_INPUT** error is:

```json
    "errors": [
        {
            "name": "INVALID_INPUT",
            "description": "The input variable has an invalid type",
            "code": "INVALID_INPUT"
        },
```

## Permissions

When a project is [deployed]({% link process-automation/latest/admin/release.md %}#deployment) service accounts are created for each connector used. The format of the service account name is: `service-account-connector-<connector-name>-<application-name>`.

Read and write access is granted to each service account on the [default storage location]({% link process-automation/latest/admin/release.md %}#deploy-steps/storage). If the connector reads or writes to files and folders held elsewhere in the repository, the service account will need to be manually given explicit permission to those directories otherwise the connector action will fail.

> **Note**: The service accounts for an application are all added to a group named `<application-name>-service-group` so that permissions can be manually assigned for an entire application if required. This also makes it easier when adding permissions because service group can be found by the application name. This approach is useful when granting permissions to a content folder in the Digital Workspace, when using the copy, move, or update actions, for example `MOVE_FILE`.
---
title: Calendar connector
---

The Calendar connector uses the [Microsoft Graph](https://docs.microsoft.com/en-us/graph/use-the-api){:target="_blank"} API to integrate with Microsoft Outlook.

The Calendar connector is displayed on the process diagram with the calendar icon.

> **Important**: The Calendar connector and user both require a Microsoft Outlook client. The Calendar connector requires a Microsoft Outlook account. The account is separate to the Alfresco hosted environment and should be created and managed by an administrator.

The actions that can be executed using the Calendar connector are:

* [Create a calendar event](#create-a-calendar-event) creates an event or appointment in the calendar.
* [Update a calendar event](#update-a-calendar-event) updates an event or appointment in the calendar.
* [Get schedule availability](#get-schedule-availability) retrieves user availability.

## Configuration

### Calendar connector configuration parameters

The Calendar connector uses the Microsoft Teams credentials to connect with a Microsoft account.
The configuration parameters for the Calendar connector are:

| Parameter | Description |
|-----------|-------------|
| TEAMS_CLIENT_ID | *Required.* The client identifier to be used for authentication. |
| TEAMS_CLIENT_SECRET | *Required.* The client secret to be used for authentication. |
| TEAMS_SCOPE | The scopes requested by the connector in the Teams instance OAuth protocol. |
| TEAMS_TENANT | The Teams tenant to be used by the connector. |

### Calendar connector errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the Calendar connector are:

| Error | Description |
|-------|-------------|
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| INVALID_REQUEST | An invalid request is received. |
| SCHEDULE_ERROR | An error occurred from attempting to get the availability. |
| UNKNOWN_ERROR | An unexpected error occurred during the execution of the action. |

In addition to the above configuration the following properties are required to perform calendar operations.

## Create a calendar event

The `createTeamsEventCalendar` action is used by the Calendar connector to create a calendar event in Microsoft Outlook.

The input parameters to create a calendar event in Microsoft Outlook are:

| Property  | Type | Description |
| --- | --- | --- |
| subject | String | *Required.* Subject of the calendar event. |
| text | String | *Optional.* Body of the calendar event. |
| startDate | DateTime | *Required.* Start Date / Time of the event. |
| minutes | Integer | *Required.* Duration in minutes of the event. |
| endDate | DateTime | *Required.* End Date / Time of the event. |
| attendees | Array | *Required.* List of attendees email addresses. |
| location | String | *Optional.* Location of the event. |
| timeZone | String | *Optional.* Timezone of the event. In general, the `timeZone` property can be set to any of the [time zones supported by Microsoft Windows](https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/default-time-zones){:target="_blank"} as well as the additional [time zones supported by the calendar API](https://docs.microsoft.com/en-us/graph/api/resources/datetimetimezone?view=graph-rest-1.0#additional-time-zones){:target="_blank"}. By default, **GMT Standard Time**.|
| onlineMeeting | Boolean | *Optional.* Adds an online Teams meeting to the event. |
| attachments | File | *Optional.* File to attach to the calendar event. |

The output parameters to create a calendar event in Microsoft Outlook are:

| Property  | Type | Description |
| --- | --- | --- |
| result | JSON | *Optional.* Response with the identifier returned by the Teams API. |

## Update a calendar event

The `updateTeamsEventCalendar` action retrieves calendar event information for a specific event in Microsoft Outlook.

The input parameters to update an event in Microsoft Outlook are:

| Property | Type | Description |
| --- | --- | --- |
| subject | String | *Required.* Subject of the calendar event. |
| text | String | *Required.* Body of the calendar event. |
| startDate | DateTime | *Required.* Start Date / Time of the event. |
| minutes | Integer | *Required.* Duration in minutes of the event. |
| endDate | DateTime | *Required.* End Date / Time of the event. |
| attendees | Array | *Required.* List of attendees email addresses. |
| location | String | *Optional.* Location of the event. |
| timeZone | String | *Required.* Timezone of the event. In general, the `timeZone` property can be set to any of the [time zones supported by Microsoft Windows](https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/default-time-zones){:target="_blank"} as well as the additional [time zones supported by the calendar API](https://docs.microsoft.com/en-us/graph/api/resources/datetimetimezone?view=graph-rest-1.0#additional-time-zones){:target="_blank"}. By default, **GMT Standard Time**.|

The input parameter used to update an event in Microsoft Outlook is:

| Property | Type | Description |
| --- | --- | --- |
| result | JSON | *Required.* Response with the identifier returned by the Teams API. |

## Get schedule availability

The `getScheduleAvailability` action retrieves a users availability information for a specific period of time.

The input parameters to get the schedule availability in Microsoft Outlook are:

| Property  | Type | Description |
| --- | --- | --- |
| startDate | DateTime | *Required.* Start date of the period of time to query. The time period must be less than 42 days.|
| endDate | DateTime | *Required.* End date of the period of time to query. The time period must be less than 42 days.|
| timeZone | String | *Optional.* Time zone e.g: **Pacific Standard Time**. The `timeZone` property can be set to any of the [time zones currently supported by Microsoft Windows](#https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/default-time-zones){:target="_blank"} as well as the additional [time zones supported by the calendar API](#https://docs.microsoft.com/en-us/graph/api/resources/datetimetimezone?view=graph-rest-1.0){:target="_blank"}. By default, `GMT Standard Time`.|
| scheduleAddress | array | *Required.* Email address of a user, group, or room. |
| availabilityViewInterval | Integer | *Required.* Defines the granularity, in minutes, used to represent the users availability. Default value: `60`. |

The output parameters to get the schedule availability in Microsoft Outlook are:

| Property  | Type | Description |
| --- | --- | --- |
| availabilityView | String | *Required.* Merged view of availability for the specific period of time. The merged view is a string that consists of time slots covering that day, with each time slot using the following convention: `n0` - free, `n1` - tentative, `n2` - busy, `n3` - out of office, `n4` - working elsewhere. |
| availability | String | *Required.* Single value that represents a global availability status for the required period. `0` - a user is free during the whole interval. `1` - all the existing slots in the required period are either free or tentative (at least one of them is tentative). `2` - all the existing slots in the required period are either free or tentative or busy (at least one of them is busy). `3` - all the existing slots in the required period are either free or tentative or busy or out of the office (at least one of them is  out of the office). `4` - all the existing slots in the required period are either free or tentative or busy or out of the office or working elsewhere (at least one of them is working elsewhere). |
| scheduleItems | JSON | *Required.* List of objects containing each of the events in the user`s calendar. |
| workingHours | JSON | *Required.* Indicates the days of the week and time intervals when the user can be available. |

## Remove a calendar event

The `removeTeamsEventCalendar` action removes an event or appointment in the calendar.

The input parameters to remove an event or appointment in Microsoft Outlook are:

| Property  | Type | Description |
| --- | --- | --- |
| id | String | *Required.* Identifier of the calendar event.|
---
title: REST connector
---

The REST connector is used to provide a connection with a REST service. It can also be used to configure a [webhook]({% link process-automation/latest/model/triggers.md %}#webhooks) as an incoming trigger.

The REST connector appears on the process diagram as a pair of curly brackets. When configuring the REST connector you can use [Authentication]({% link process-automation/latest/model/authentication.md %}).

> **Important**: All REST services need to be separate to the Alfresco hosted environment and should be created and managed by customers.

The actions that can be executed using the REST connector are:

* [GET](#get)
* [HEAD](#head)
* [POST](#post)
* [PUT](#put)
* [PATCH](#patch)
* [DELETE](#delete)
* [OPTIONS](#options)
* [TRACE](#trace)

## GET

The **GET** action is used to send HTTP GET requests.

The input parameters for GET are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restUrl | String | *Required.* URL of the REST endpoint including the protocol and path, for example `http://alfresco.com`. |
| restUrlParams | JSON | *Optional.* JSON map of the URL parameter names and values to append to the URL. |
| restUrlEncoded | Boolean | *Optional.* Set whether the URL should be encoded or not, for example `true`. |
| requestHeaders | JSON |  *Optional.* A JSON map of the request header names and values. Values can be fixed values or variables. |
| circuitBreaker | Boolean | *Optional.* Set whether the circuit breaker is enabled, for example `true`. |
| timeout | Integer | *Optional.* The timeout period to wait for the service in milliseconds, for example `910000`. |

The output parameters from GET are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restResult | JSON | *Optional.* The response from the REST service call. |
| restStatus | Integer | *Optional.* The HTTP response status code from the REST service call. |
| responseHeaders | JSON | *Optional.* The HTTP response headers from the REST service call. |

## HEAD

The **HEAD** action is used to send HTTP HEAD requests.

The input parameters for HEAD are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restUrl | String | *Required.* URL of the REST endpoint including the protocol and path, for example `http://alfresco.com`. |
| restUrlParams | JSON | *Optional.* JSON map of the URL parameter names and values to append to the URL. |
| restUrlEncoded | Boolean | *Optional.* Set whether the URL should be encoded or not, for example `true`. |
| requestHeaders | JSON |  *Optional.* A JSON map of the request header names and values. Values can be fixed values or variables. |
| circuitBreaker | Boolean | *Optional.* Set whether the circuit breaker is enabled, for example `true`. |
| timeout | Integer | *Optional.* The timeout period to wait for the service in milliseconds, for example `910000`. |

The output parameters from HEAD are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restStatus | Integer | *Optional.* The HTTP response status code from the REST service call. |
| responseHeaders | JSON | *Optional.* The HTTP response headers from the REST service call. |

## POST

The **POST** action is used to send HTTP POST requests.

The input parameters for POST are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restUrl | String | *Required.* URL of the REST endpoint including the protocol and path, for example `http://alfresco.com`. |
| restUrlParams | JSON | *Optional.* JSON map of the URL parameter names and values to append to the URL. |
| restUrlEncoded | Boolean | *Optional.* Set whether the URL should be encoded or not, for example `true`. |
| requestHeaders | JSON |  *Optional.* A JSON map of the request header names and values. Values can be fixed values or variables. |
| requestPayload | JSON | *Optional.* The body of the request. |
| circuitBreaker | Boolean | *Optional.* Set whether the circuit breaker is enabled, for example `true`. |
| timeout | Integer | *Optional.* The timeout period to wait for the service in milliseconds, for example `910000`. |

The output parameters from POST are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restResult | JSON | *Optional.* The response from the REST service call. |
| restStatus | Integer | *Optional.* The HTTP response status code from the REST service call. |
| responseHeaders | JSON | *Optional.* The HTTP response headers from the REST service call. |

### Use the POST action to send files

You can use the `RequestPayload` property in the expression editor to reference and send a file from another location using the **POST** action.

To use the **POST** action to send files:

1. In the Modelling Application click the **+** icon next to processes and create a new process called `send-file`.

2. Create a **User task** called `Attach file`.

3. Create a **REST Connector** called `Send POST request`.

4. Join the **User task** to the **REST Connector**.

5. Select the **REST Connector** and from the **Properties pane** select the **POST** action from the **Action** dropdown list.

6. Click the edit icon next to **RequestPayload** under the **Input mapping** section.

7. In the **Value** column on the right add the following.

    ```{
    "base64File": "${getBase64FileContent(file)}"
       }
        ```

    Where `file` is the file process variable and might have a different name in your process.

8. Select the **restUrI** parameter on the left and then select **Value** on the right.

9. Enter the UrI you want to use, for example `https://postman-echo.com` and then click **Update**.

This process can now be used in your forms to send a file.

> **Note:** The maximum file size for each file is 10 MB and the files are processed one-by-one to decrease the amount of memory used. If you have a large number of concurrent processes with bigger files, the execution time might be longer than usual.

## PUT

The **PUT** action is used to send HTTP PUT requests.

The input parameters for PUT are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restUrl | String | *Required.* URL of the REST endpoint including the protocol and path, for example `http://alfresco.com`. |
| restUrlParams | JSON | *Optional.* JSON map of the URL parameter names and values to append to the URL. |
| restUrlEncoded | Boolean | *Optional.* Set whether the URL should be encoded or not, for example `true`. |
| requestHeaders | JSON |  *Optional.* A JSON map of the request header names and values. Values can be fixed values or variables. |
| requestPayload | JSON | *Optional.* The body of the request. |
| circuitBreaker | Boolean | *Optional.* Set whether the circuit breaker is enabled, for example `true`. |
| timeout | Integer | *Optional.* The timeout period to wait for the service in milliseconds, for example `910000`. |

The output parameters from PUT are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restResult | JSON | *Optional.* The response from the REST service call. |
| restStatus | Integer | *Optional.* The HTTP response status code from the REST service call. |
| responseHeaders | JSON | *Optional.* The HTTP response headers from the REST service call. |

## PATCH

The **PATCH** action is used to send HTTP PATCH requests.

The input parameters for PATCH are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restUrl | String | *Required.* URL of the REST endpoint including the protocol and path, for example `http://alfresco.com`. |
| restUrlParams | JSON | *Optional.* JSON map of the URL parameter names and values to append to the URL. |
| restUrlEncoded | Boolean | *Optional.* Set whether the URL should be encoded or not, for example `true`. |
| requestHeaders | JSON |  *Optional.* A JSON map of the request header names and values. Values can be fixed values or variables. |
| requestPayload | JSON | *Optional.* The body of the request. |
| circuitBreaker | Boolean | *Optional.* Set whether the circuit breaker is enabled, for example `true`. |
| timeout | Integer | *Optional.* The timeout period to wait for the service in milliseconds, for example `910000`. |

The output parameters from PATCH are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restResult | JSON | *Optional.* The response from the REST service call. |
| restStatus | Integer | *Optional.* The HTTP response status code from the REST service call. |
| responseHeaders | JSON | *Optional.* The HTTP response headers from the REST service call. |

## DELETE

The **DELETE** action is used to send HTTP DELETE requests.

The input parameters for DELETE are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restUrl | String | *Required.* URL of the REST endpoint including the protocol and path, for example `http://alfresco.com`. |
| restUrlParams | JSON | *Optional.* JSON map of the URL parameter names and values to append to the URL. |
| restUrlEncoded | Boolean | *Optional.* Set whether the URL should be encoded or not, for example `true`. |
| requestHeaders | JSON |  *Optional.* A JSON map of the request header names and values. Values can be fixed values or variables. |
| circuitBreaker | Boolean | *Optional.* Set whether the circuit breaker is enabled, for example `true`. |
| timeout | Integer | *Optional.* The timeout period to wait for the service in milliseconds, for example `910000`. |

The output parameters from DELETE are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restResult | JSON | *Optional.* The response from the REST service call. |
| restStatus | Integer | *Optional.* The HTTP response status code from the REST service call. |
| responseHeaders | JSON | *Optional.* The HTTP response headers from the REST service call. |

## OPTIONS

The **OPTIONS** action is used to send HTTP OPTIONS requests.

The input parameters for OPTIONS are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restUrl | String | *Required.* URL of the REST endpoint including the protocol and path, for example `http://alfresco.com`. |
| restUrlParams | JSON | *Optional.* JSON map of the URL parameter names and values to append to the URL. |
| restUrlEncoded | Boolean | *Optional.* Set whether the URL should be encoded or not, for example `true`. |
| requestHeaders | JSON |  *Optional.* A JSON map of the request header names and values. Values can be fixed values or variables. |
| circuitBreaker | Boolean | *Optional.* Set whether the circuit breaker is enabled, for example `true`. |
| timeout | Integer | *Optional.* The timeout period to wait for the service in milliseconds, for example `910000`. |

The output parameters from OPTIONS are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restStatus | Integer | *Optional.* The HTTP response status code from the REST service call. |
| responseHeaders | JSON | *Optional.* The HTTP response headers from the REST service call. |

## TRACE

The **TRACE** action is used to send HTTP TRACE requests.

The input parameters for TRACE are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restUrl | String | *Required.* URL of the REST endpoint including the protocol and path, for example `http://alfresco.com`. |
| restUrlParams | JSON | *Optional.* JSON map of the URL parameter names and values to append to the URL. |
| requestHeaders | JSON |  *Optional.* A JSON map of the request header names and values. Values can be fixed values or variables. |
| circuitBreaker | Boolean | *Optional.* Set whether the circuit breaker is enabled, for example `true`. |
| timeout | Integer | *Optional.* The timeout period to wait for the service in milliseconds, for example `910000`. |

The output parameters from TRACE are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| restResult | JSON | *Optional.* The response from the REST service call. |
| restStatus | Integer | *Optional.* The HTTP response status code from the REST service call. |

## Configuration parameters

The configuration parameters for the REST connector are:

| Parameter | Description |
| --------- | ----------- |
| EVENT_NOT_MATCH_STATUS | *Optional.* The HTTP response code to return to an external system if no triggers are matched by an incoming webhook request, for example `404`. |

> **Note**: The configuration parameters for the REST connector are used for configuring webhooks using [triggers]({% link process-automation/latest/model/triggers.md %}).

## Errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the REST connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| BAD_REQUEST | The server could not understand the request due to invalid syntax. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refuses to authorize it. |
| NOT_FOUND | The server could not find what was requested. |
| METHOD_NOT_ALLOWED | The request method is known by the server but is not supported. |
| NOT_ACCEPTABLE | The server cannot produce a response matching the list of acceptable values. |
| PROXY_AUTHENTICATION_REQUIRED | The request has not been applied because it lacks valid authentication. |
| REQUEST_TIMEOUT | The server would like to shut down this unused connection. |
| CONFLICT | The request conflicts with current state of the server. |
| GONE | No longer available. |
| INTERNAL_SERVER_ERROR | The server has encountered a situation it doesn't know how to handle. |
| NOT_IMPLEMENTED | The request method is not supported by the server and cannot be handled. |
| BAD_GATEWAY | The server got an invalid response. |
| SERVICE_UNAVAILABLE | The server is not ready to handle the request. |
| GATEWAY_TIMEOUT | The server is acting as a gateway and cannot get a response in time. |
---
title: Salesforce connector
---

The Salesforce connector is used to integrate with an installation of [Salesforce](https://salesforce.com){:target="_blank"} and have a process operate on Salesforce objects.

The Salesforce connector is displayed on the process diagram with the Salesforce logo.

> **Important**: The Salesforce connector requires a Salesforce account to use. This account is separate to the Alfresco hosted environment and should be created and managed by customers.

The actions that can be executed using the Salesforce connector are:

* [Create an object instance](#create-an-object-instance)
* [Get an object instance](#get-an-object-instance)
* [Update an object instance](#update-an-object-instance)
* [Delete an object instance](#delete-an-object-instance)
* [Query an object instance](#query-an-object-instance)
* [Submit a Salesforce object instance for approval](#submit-an-object-instance-for-approval)
* [Query the current approval processes in Salesforce](#query-approval-process)
* [Approve a Salesforce object instance submitted for approval](#approve-an-object-instance-submitted-for-approval)
* [Reject a Salesforce object instance submitted for approval](#reject-an-object-instance-submitted-for-approval)
* [Create a new custom object in Salesforce](#create-a-custom-object-definition)

> **Important**: The Salesforce connector requires a [Salesforce developer account](https://developer.salesforce.com/signup){:target="_blank"} to interact with and a **Connected App** set up to interact with the Process Automation connector.

## Create an object instance

The **CREATE** action is used by the Salesforce connector to create a new Salesforce object.

The input parameters to create an object are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| SObjectName | String | *Required.* The name of the Salesforce object to create, for example `Account`. |
| salesforcePayload | JSON | *Required.* The payload to send to Salesforce as a JSON map. See [Salesforce API documentation](https://developer.salesforce.com/docs/api-explorer/sobject/Account){:target="_blank"} for valid fields to send. |

The output parameters from creating an object in Salesforce are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceResult | String | *Optional.* The result from the REST or SOAP call from Salesforce. |
| salesforceStatus | String | *Optional.* The HTTP status code of the response. |

## Get an object instance

The **GET** action is used by the Salesforce connector to retrieve a Salesforce object.

The input parameters to get an object are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| SObjectName | String | *Required.* The name of the Salesforce object to get, for example `Account`. |
| SObjectId | String | *Required.* The Salesforce object ID, for example `accountId`. |

The output parameters from getting an object from Salesforce are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceResult | String | *Optional.* The result from the REST or SOAP call from Salesforce. |
| salesforceStatus | String | *Optional.* The HTTP status code of the response. |

## Update an object instance

The **UPDATE** action is used by the Salesforce connector to update a Salesforce object.

The input parameters to update an object are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| SObjectName | String | *Required.* The name of the Salesforce object to update, for example `Account`. |
| SObjectId | String | *Required.* The Salesforce object ID, for example `accountId`. |
| salesforcePayload | JSON | *Required.* The payload to send to Salesforce as a JSON map. See [Salesforce API documentation](https://developer.salesforce.com/docs/api-explorer/sobject/Account){:target="_blank"} for valid fields to send. |

The output parameters from updating an object from Salesforce are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceStatus | String | *Optional.* The HTTP status code of the response. |

## Delete an object instance

The **DELETE** action is used by the Salesforce connector to delete a Salesforce object.

The input parameters to delete an object are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| SObjectName | String | *Required.* The name of the Salesforce object to delete, for example `Account`. |
| SObjectId | String | *Required.* The Salesforce object ID, for example `accountId`. |

The output parameters from deleting an object from Salesforce are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceStatus | String | *Optional.* The HTTP status code of the response. |

## Query an object instance

The **QUERY** action is used by the Salesforce connector to query a Salesforce object.

The input parameters to query an object are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceQuery | String | *Required.* The query to execute against Salesforce, for example `SELECT name FROM account`. |

The output parameters from querying an object from Salesforce are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceResult | String | *Optional.* The result from the REST or SOAP call from Salesforce. |
| salesforceStatus | String | *Optional.* The HTTP status code of the response. |

## Submit an object instance for approval

The **APPROVAL_SUBMIT** action is used by the Salesforce connector to submit a Salesforce object for approval.

The input parameters to submit an object for approval are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforcePayload | JSON | *Required.* The payload to send to Salesforce as a JSON map. See [Salesforce API documentation](https://developer.salesforce.com/docs/api-explorer/sobject/Account){:target="_blank"} for valid fields to send. |

The output parameters from submitting an object for approval are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceResult | String | *Optional.* The result from the REST or SOAP call from Salesforce. |
| salesforceStatus | String | *Optional.* The HTTP status code of the response. |

## Query approval process

The **APPROVAL_LIST** action is used by the Salesforce connector to query Salesforce objects awaiting approval.

The output parameters from querying objects awaiting approval are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceResult | String | *Optional.* The result from the REST or SOAP call from Salesforce. |
| salesforceStatus | String | *Optional.* The HTTP status code of the response. |

## Approve an object instance submitted for approval

The **APPROVAL_APPROVE** action is used by the Salesforce connector to approve a Salesforce object that is awaiting approval.

The input parameters to approve an object awaiting approval are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforcePayload | JSON | *Required.* The payload to send to Salesforce as a JSON map. See [Salesforce API documentation](https://developer.salesforce.com/docs/api-explorer/sobject/Account){:target="_blank"} for valid fields to send. |

The output parameters from approving an object awaiting approval are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceResult | String | *Optional.* The result from the REST or SOAP call from Salesforce. |
| salesforceStatus | String | *Optional.* The HTTP status code of the response. |

## Reject an object instance submitted for approval

The **APPROVAL_REJECT** action is used by the Salesforce connector to reject a Salesforce object that is awaiting approval.

The input parameters to reject an object awaiting approval are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforcePayload | JSON | *Required.* The payload to send to Salesforce as a JSON map. See [Salesforce API documentation](https://developer.salesforce.com/docs/api-explorer/sobject/Account){:target="_blank"} for valid fields to send. |

The output parameters from rejecting an object awaiting approval are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceResult | String | *Optional.* The result from the REST or SOAP call from Salesforce. |
| salesforceStatus | String | *Optional.* The HTTP status code of the response. |

## Create a custom object definition

The **CUSTOM_OBJECT_CREATE** action is used by the Salesforce connector to create a custom Salesforce object definition.

The input parameters to create a custom object definition are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforcePayload | JSON | *Required.* The payload to send to Salesforce as a JSON map. See [Salesforce API documentation](https://developer.salesforce.com/docs/api-explorer/sobject/Account){:target="_blank"} for valid fields to send. |

The output parameters from creating an object definition are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| salesforceResult | String | *Optional.* The result from the REST or SOAP call from Salesforce. |
| salesforceStatus | String | *Optional.* The HTTP status code of the response. |

## Configuration parameters

The configuration parameters for the Salesforce connector are:

| Parameter | Description |
| --------- | ----------- |
| SALESFORCE_CLIENT_ID | *Required.* The ID of your Salesforce account. When viewing your application in the Salesforce App Manager this is called the **Consumer Key**.  |
| SALESFORCE_CLIENT_SECRET | *Required.* The secret associated to your Salesforce account. When viewing your application in the Salesforce App Manager this is called the **Consumer Secret**. |
| SALESFORCE_USERNAME | *Required.* The user that the connector will use to interact with Salesforce. |
| SALESFORCE_PASSWORD | *Required.* The password for the user that will interact with Salesforce. |
| SALESFORCE_SECURITY_TOKEN | *Required.* The security token for the user that will interact with Salesforce. To obtain this token, log into Salesforce as the user and navigate to **Settings > My Personal Information**. |
| SALESFORCE_URL_LOGIN | *Required.* The URL to login to Salesforce, for example `https://login.salesforce.com/services/oauth2/token`. |
| SALESFORCE_SOAP_URL_LOGIN | *Required.* The URL for SOAP requests, for example `https://login.salesforce.com/services/Soap/c/45.0`. |
| SALESFORCE_VERSION | *Required.* The version of Salesforce, for example `45.0`. |

## Errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the Salesforce connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| REQUEST_TIMEOUT | Salesforce request timeout. |
| CIRCUIT_BREAKER_OPEN | Max number of retries reached without success. |
| MISSING_TOKEN | Salesforce access token could not be obtained. |
| CONNECTION_ERROR | Salesforce connection error. |
---
title: Slack connector
---

The Slack connector is used to integrate with the [Slack](https://slack.com){:target="_blank"} web API and REST time messaging API to create Slack channels and send messages to channels or users.

The Slack connector is displayed on the process diagram with the Slack logo.

> **Important**: The Slack connector requires a Slack account to use. This account is separate to the Alfresco hosted environment and should be created and managed by customers.

The actions that can be executed using the Slack connector are:

* [Send a message](#send-message) to a specific user or channel (public or private)
* [Create a new channel](#create-channel) (public or private)

## Send message

The **SEND_MESSAGE** action is used by the Slack connector to send a message to a user or channel.

The input parameters to send a message in Slack are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| channelId | String | *Requires one.* The channel ID to send the message to. |
| channelName | String | *Requires one.* The name of the channel to send the message to. |
| userId | String | *Requires one.* The user ID of the message recipient. |
| userEmail | String | *Requires one.* The email address of the message recipient. |
| text | String | *Required.* The contents of the message. The message supports [Freemarker](https://freemarker.apache.org/docs/dgui_datamodel_basics.html){:target="_blank"} syntax, for example `${fullName.lastName}` can be used from the `metadata` parameter to include variables. |
| metadata | JSON | *Optional.* Metadata to be used by the `text` parameter to include [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) in a message. |
| requestResponse | String | *Optional.* Set to `no` and a response will be sent back to the process immediately after the message is sent. Set to `any` and a response will be sent back to the process only after a reply is received in the same channel. Set to `thread` and a response will be sent back to the process only after a reply is received in a thread. |

The output parameters from sending a message in Slack are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| message | String | *Optional.* The message received in the channel or thread if the input parameter `requestResponse` was set to `any` or `thread`. |

## Create channel

The **CREATE_CHANNEL** action is used by the Slack connector to create a new public or private channel in Slack.

The input parameters to create a channel in Slack are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| channelName | String | *Required.* The name of the channel to be created. |
| channelType | String | *Required.* Set whether the channel is `public` or `private`. |
| members | String | *Required.*  A list of members that will be invited to join the new channel using Slack IDs or email addresses. |

The output parameters from creating a channel in Slack are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| slackResult | JSON | *Optional.* An object containing the details of the newly created channel. |

An example of a channel creation in the `slackResult` is:

```json
{
  "ok":true,
  "channel":{
    "id":"CFWSKMFR6",
    "name":"my_channel",
    "is_channel":true,
    "created":1549985348,
    "is_archived":false,
    "is_general":false,
    "unlinked":0,
    "creator":"UFX13DBJM",
    "name_normalized":"my_channel",
    "is_shared":false,
    "is_org_shared":false,
    "is_member":true,
    "is_private":false,
    "is_mpim":false,
    "last_read":"0000000000.000000",
    "latest":null,
    "unread_count":0,
    "unread_count_display":0,
    "members":[
      "UFX13DBJM",
      "DFWSKM0HH"
    ],
    "topic":{
      "value":"",
      "creator":"",
      "last_set":0
    },
    "purpose":{
      "value":"",
      "creator":"",
      "last_set":0
    },
    "previous_names":[],
    "priority":0
  }
}
```

## Configuration

The Slack connector requires a Slack application and a Slack bot in order to function. The application and bot need to be configured correctly.

1. Use the [Slack website](https://api.slack.com/apps){:target="_blank"} to create an application.

    > **Note**: You will need to be logged in as a workspace administrator to create an application.

2. Use the following URL to create a bot in the application you created: `https://api.slack.com/apps/<app_id>/bots`.

3. Use the following URL to configure the scope and permissions of the application and bot: `https://api.slack.com/apps/<app_id>/oauth`.

    The required [scope and permissions](https://api.slack.com/scopes){:target="_blank"} are:

    * app_mentions:read
    * channels:read
    * channels:manage
    * groups:read
    * groups:write
    * mpim:read
    * mpim:write
    * users:read
    * users:read.email
    * chat:write
    * chat:write.public
    * im:read
    * im:write

4. Use the following URL to obtain the Slack bot token and signing secret: `https://api.slack.com/apps/<app_id>/oauth`.

### Configuration parameters

The configuration parameters for the Slack connector are:

| Parameter | Description |
| --------- | ----------- |
| SLACK_BOT_TOKEN | *Required.* The Slack bot user token obtained from configuring Slack, beginning `xoxb-`. |
| SLACK_SIGNING_SECRET | *Required.* The Slack signing secret obtained from the **Basic Information** page in Slack. |

### Event subscription

To use Slack as a [trigger]({% link process-automation/latest/model/triggers.md %}) the Slack bot needs to subscribe to events.

1. Use the following URL to configure the events: `https://api.slack.com/apps/<app_id>/event-subscriptions`.

2. Set the **Request URL** for Slack to post HTTP requests to as: `https://<cluster-name>/<application-name>/connector/<connector-name>/slack/events`. Where:

    * `cluster-name` is the name of the cluster running Process Automation.
    * `application-name` is the name of the application the trigger is configured for.
    * `connector-name` is the name of the Slack connector instance in the application.

3. Subscribe the Slack bot user to the following events:

    * app_mention
    * message.channels
    * message.groups
    * message.im
    * message.npim

## Errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the Slack connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| INVALID_RESULT_FORMAT | The REST service result payload cannot be parsed. |
| USER_NOT_FOUND | User is not found. |
| CHANNEL_NOT_FOUND | Channel is not found. |
| INVALID_REQUEST | A null response is received while sending message. |
| INVALID_CHANNEL | There is a problem with the channel. |
| MSG_TOO_LONG | Message text is too long. |
| FATAL_ERROR | The server could not complete the operation without encountering a catastrophic error. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refuses to authorize it. |
| REQUEST_TIMEOUT | The server would like to shut down this unused connection. |
---
title: Microsoft Teams connector
---

The Microsoft Teams connector uses the [Microsoft Graph](https://docs.microsoft.com/en-us/graph/use-the-api){:target="_blank"} API to integrate with Microsoft Teams.

The Teams connector is displayed on the process diagram with the Teams logo.

> **Important**: The Teams connector and user both require a Microsoft Teams client. The Teams connector requires a Microsoft Teams account. The account is separate to the Alfresco hosted environment and should be created and managed by an administrator.

The actions that can be executed using the Teams connector are:

* [Get Teams](#get-teams) retrieves all teams of the organization.
* [Create Teams channel](#create-teams-channel) creates a new public or private channel.
* [Get channels](#get-channels) retrieves all existing channels for a specific team.

## Configuration

### Teams connector configuration parameters

The configuration parameters for the Teams connector are:

| Parameter | Description |
|-----------|-------------|
| TEAMS_CLIENT_ID | *Required.* The client identifier to be used for authentication. |
| TEAMS_CLIENT_SECRET | *Required.* The client secret to be used for authentication. |
| TEAMS_USERNAME | *Required.* The MS Teams user to impersonate `in:wq` the connector. |
| TEAMS_SCOPE | Thr scopes requested by the connector in the Teams instance OAuth protocol. |
| TEAMS_TENANT | The Teams tenant to be used by the connector. |

### Teams connector errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that
can be handled by the Teams connector are:

| Error | Description |
|-------|-------------|
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| INVALID_REQUEST | An invalid request is received. |
| UNKNOWN_ERROR | An unexpected error occurred during the execution of the action. |

In addition to the above configuration the following properties are required to perform Teams operations:

## Get Teams

The `getTeams` action is used by the Teams connector and retrieves all of the visible teams of the organization.

The input parameter to retrieve all of the visible teams is:

| Property | Type | Description |
|----------|------|-------------|
| teamName | String | *Optional.* Name of the team. If this property is null, the action will return all the teams. |

The output parameter to retrieve all of the visible teams is:

| Property | Type | Description |
|----------|------|-------------|
| result | JSON | *Optional.* Response with the team name and the identifier returned by the Teams API. |

## Create Teams Channel

The `createTeamsChannel` action is used by the Teams connector to create a new public or private channel in Teams.

The input parameters to create a new private or public channel are:

| Property | Type | Description |
|----------|------|-------------|
| teamId | String | *Required.* Identifier of the team in which the channel will be created. |
| channelName | String | *Required.* Name of the channel. |
| channelType | String | *Optional.* Type of the channel. |

The output parameters to create a new private or public channel are:

| Property | Type | Description |
|----------|------|-------------|
| result | JSON | *Optional.* Response with the channel name and the description returned by the Teams API. |
| channelId | String | *Optional.* Identifier of the channel created. |

## Get channels

The `getChannels` action is used by the Teams connector to retrieve all the existing channels from a
specific team.

The input parameters to retrieve all the existing channels from a specific team are:

| Property | Type | Description |
|----------|------|-------------|
| teamId | String | *Required.* Identifier of the team. |
| channelName | String | *Optional.* Name of the channel. If this property is null, the action will return all the channels. |

The output parameter to retrieve all the existing channels from a specific team is:

| Property | Type | Description |
|----------|------|-------------|
| result   | JSON | *Optional.* Response with the identifier, the name, the membership type, and the web url returned by the Teams API. |   
---
title: Twilio connector
---

The Twilio connector is used to integrate with an instance of [Twilio](https://twilio.com){:target="_blank"} to send SMS messages. 

The Twilio connector is displayed on the process diagram with the Twilio logo.

> **Important**: The TWilio connector requires a Twilio account to use. This account is separate to the Alfresco hosted environment and should be created and managed by customers.

## Send SMS

The **SEND_SMS** action is used by the Twilio connector to send an SMS message.

The input parameters to send an SMS are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| smsFrom | String | *Required.* The phone number the SMS will be sent from. |
| smsTo | String | *Required.* The list of numbers the SMS will be sent to. |
| smsBody | String | *Required.* The contents of the SMS. The message supports [Freemarker](https://freemarker.apache.org/docs/dgui_datamodel_basics.html){:target="_blank"} syntax, for example `${fullName.lastName}` can be used from the `metadata` parameter to include variables.|
| metadata | JSON | *Optional.* Metadata to be used by the `smsBody` parameter to include [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) in a message. |

The output parameters from sending an SMS using Twilio are:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| smsResult | JSON | *Optional.* An object containing a map of message IDs and destination numbers the message was sent to. |

## Configuration

An account ID and token are required by the connector to access Twilio. These are specific to your Twilio account and act as the authorization credentials.

The values are provided by Twilio when an account is created. They can also be located in the [Twilio setup page](https://www.twilio.com/console/project/settings){:target="_blank"}.

### Configuration parameters

The configuration parameters for the Slack connector are:

| Parameter | Description |
| --------- | ----------- |
| TWILIO_ACCOUNT | *Required.* Your account name obtained from Twilio. |
| TWILIO_TOKEN | *Required.* A token for your account obtained from Twilio. |

## Errors

The possible [errors]({% link process-automation/latest/model/connectors/index.md %}#errors) that can be handled by the Twilio connector are:

| Error | Description |
| ----- | ----------- |
| MISSING_INPUT | A mandatory input variable was not provided. |
| INVALID_INPUT | The input variable has an invalid type. |
| TWILIO_CONNECTION_ERROR | Unable to connect to Twilio service. |
| AUTHENTICATION_CONNECTION_ERROR | Unable to authenticate to Twilio. |
| INVALID_REQUEST_ERROR | Invalid request. |
| INVALID_TO_PHONE_NUMBER_ERROR | Invalid 'to' phone number. |
| INVALID_FROM_PHONE_NUMBER_ERROR | Invalid 'from' phone number. |
| PERMISSION_DENIED_ERROR | Lack of permission to the resource and method requested. |
| INVALID_REGION_TO_PHONE_NUMBER_ERROR | Permission to send an SMS has not been enabled for the region indicated by the 'To' number. |
| TEMPLATE_READ_ERROR | Cannot read the Freemarker template. |
| TEMPLATE_METADATA_ERROR | The template references non-existing metadata. |
| TEMPLATE_SYNTAX_ERROR | Invalid Freemarker syntax. |
| UNKNOWN_ERROR | Unexpected runtime error. |
| BAD_REQUEST | The server could not understand the request due to invalid syntax. |
| UNAUTHORIZED | The request has not been applied because it lacks valid authentication. |
| FORBIDDEN | The server understood the request but refuses to authorize it. |
| NOT_FOUND | The server could not find what was requested. |
| METHOD_NOT_ALLOWED | The request method is known by the server but is not supported. |
| NOT_ACCEPTABLE | The server cannot produce a response matching the list of acceptable values. |
| REQUEST_TIMEOUT | The server would like to shut down this unused connection. |
| CONFLICT | The request conflicts with current state of the server. |
| GONE | No longer available. |
| UNPROCESSABLE_ENTITY | The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions. |
| LOCKED | The resource that is being accessed is locked. |
| FAILED_DEPENDENCY | The request failed due to failure of a previous request. |
| INTERNAL_SERVER_ERROR | The server has encountered a situation it doesn't know how to handle. |
| NOT_IMPLEMENTED | The request method is not supported by the server and cannot be handled. |
| BAD_GATEWAY | The server got an invalid response. |
| SERVICE_UNAVAILABLE | The server is not ready to handle the request. |
| GATEWAY_TIMEOUT | The server is acting as a gateway and cannot get a response in time. |
---
title: BPMN
---

BPMN elements are used to model processes and include other models created within a project into a process definition.

## Start events

A process must always contain at least one start event as they define how a process begins.

The types of start event are:

* [Start events](#start-event)
* [Error start events](#error-start-event)
* [Message start events](#message-start-event)
* [Signal start events](#signal-start-event)
* [Timer start events](#timer-start-event)

### Start event

Start events are where the trigger is unspecified for starting a process. The trigger can be using a form, manually through the Digital Workspace, using the REST API or from a [trigger]({% link process-automation/latest/model/triggers.md %}).

{% capture start-prop %}

#### Basic properties

The basic properties for a start event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the start event. This is system generated and cannot be altered, for example `StartEvent_1w29b3h`. |
| Name | *Optional.* The name of the start event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the start event does. |

#### Form name

An optional [form]({% link process-automation/latest/model/forms.md %}) can be used to begin a process. The form must exist within the same project as the process definition to be selected. Select a form from the dropdown, else create a new form using the **+** symbol.

Once a form has been selected, it can be edited using the **Open Form** symbol.

#### Mapping type

The mapping type sets how data is passed between the start event and the process. There are [five options]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping) for how to send this data. The default value is **Don't map variables**. For form widgets and form variables you can add static values. For example you can pass a form variable called `path` which can be a file location or URL.

{% endcapture %}
{% capture start-img %}

Start events are displayed as a single thin circle without an icon inside.

{% endcapture %}
{% capture start-xml %}

An example of the XML of a start event without a form defined is:

```xml
<bpmn2:startEvent id="StartProcess_1" name="FormStart_4">
	<bpmn2:outgoing>SequenceFlow_1</bpmn2:outgoing>
</bpmn2:startEvent>
```

An example of the XML of a start event with a form defined is:

```xml
<bpmn2:startEvent id="StartProcess_1" name="FormStart_4" activiti:formKey="form-4ccd023b-d607-4cab-8623-da4c87dd9611">
	<bpmn2:outgoing>SequenceFlow_1</bpmn2:outgoing>
</bpmn2:startEvent>
```

> **Note**: The `activiti:formKey` is the `id` of the form used to start the process.

{% endcapture %}

{% include tabs.html tableid="start" opt1="Properties" content1=start-prop opt2="Appearance" content2=start-img opt3="XML" content3=start-xml %}

### Error start event

Error start events can only be used in [event sub-processes](#event-sub-processes). They begin an event sub-processes when a named error is received.

{% capture error-start-prop %}

#### Basic properties

The basic properties for an error start event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the error start event. This is system generated and cannot be altered, for example `StartEvent_1w29b3h`. |
| Name | *Optional.* The name of the error start event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the error start event does. |

#### Form name

An optional [form]({% link process-automation/latest/model/forms.md %}) can be used to begin a process. The form must exist within the same project as the process definition to be selected. Select a form from the dropdown, else create a new form using the **+** symbol.

Once a form has been selected, it can be edited using the **Open Form** symbol.

#### Mapping type

The mapping type sets how data is passed between the error start event and the process. There are [five options]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping) for how to send this data. The default value is **Send no variables**.

#### Error

An error needs to be defined for the error start event to catch. A previously created **Error** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. An **Error name** and **Error code** can then be set.

{% endcapture %}
{% capture error %}

Error events are used to model an exception in a business process. Errors are thrown by error end events and caught by error start events and error boundary events.

The `errorRef` property in the `errorEventDefinition` of an error event element will match against the `id` of an error when viewing the **XML Editor**.

Error events are displayed as a lightning bolt icon inside different shapes that differentiate between the event types. A solid lightning bolt represents a throwing event, whilst a hollow lightning bolt represents a catching event.

To create a new error use the **+** symbol against an error event such as a start error event, or make sure no BPMN element is selected by clicking on a blank section of the process canvas and the **Edit Errors** button will be visible in the right-hand properties panel.

{% endcapture %}
{% capture error-start-img %}

Error start events are displayed as a single thin circle with a hollow lightning bolt icon inside.

{% endcapture %}
{%capture error-start-xml %}

An example of the XML of an error start event is:

```xml
<bpmn2:startEvent id="StartEvent3">
	<bpmn2:errorEventDefinition errorRef="Error_0vbkbeb" />
</bpmn2:startEvent>
```

An example of the XML of an error is:

```xml
<bpmn2:error id="Error_0vbkbeb" name="payment-failed-error" errorCode="404" />
```

{% endcapture %}

{% include tabs.html tableid="error-start" opt1="Properties" content1=error-start-prop opt2="Error" content2=error opt3="Appearance" content3=error-start-img opt4="XML" content4=error-start-xml %}

### Message start event

Message start events begin a process instance when a named message is received.

{% capture message-start-prop %}

#### Basic properties

The basic properties for a message start event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the message start event. This is system generated and cannot be altered, for example `StartEvent_1w29b3h`. |
| Name | *Optional.* The name of the message start event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the message start event does. |

#### Form name

An optional [form]({% link process-automation/latest/model/forms.md %}) can be used to begin a process. The form must exist within the same project as the process definition to be selected. Select a form from the dropdown, else create a new form using the **+** symbol.

Once a form has been selected, it can be edited using the **Open Form** symbol.

#### Mapping type

The mapping type sets how data is passed between the message start event and the process. There are [five options]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping) for how to send this data. The default value is **Send no variables**.

#### Message

A message needs to be defined for the message start event to catch when it is thrown. A previously created **Message** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. A **Message name** and payload can then be set.

{% endcapture %}
{% capture message %}

#### Message

Messages have a name and contain a payload. They are sent by message throwing events and received by message catching events in a 1:1 relationship between throw events and catch events. Messages contain a payload known as a message payload and can be passed between scopes, for example between two different process definitions within the same diagram that are separated by different [pools](#pools-and-lanes).

The message `id` property of a message is matched against the `messageRef` property in the corresponding throw and catch message elements when viewing the **XML Editor**.

To create a new message use the **+** symbol against a message event such as a message boundary event, or make sure no BPMN element is selected by clicking on a blank section of the process canvas and the **Edit Messages** button will be visible in the right-hand properties panel.

Message events are displayed as an envelope icon inside different shapes that differentiate between the event types. A solid envelope represents a throwing event, whilst a hollow envelope represents a catching event.

#### Message payloads

Message payloads contain a set of values that are sent from a throwing event and received by a catching event.

Message payloads can only be created on a message throw event and contain one or more properties that have a `name`, `type` and `value`. The property types for payloads are:

| Type | Description |
| ---- | ----------- |
| String | A sequence of characters, for example `#Mint-Ice-Cream-4!` |
| Integer | A positive whole number, for example `642` |
| Boolean | A value of either `true` or `false` |
| Date | A specific date in the format `YYYY-MM-DD`, for example `2020-04-22` |
| Variable | A value passed from a [process variable]({% link process-automation/latest/model/processes/index.md %}#process-variables). |

The receiving message catch event is then used to map the received values in the payload to process variables in its own scope.

Message payload mappings can be viewed in the **Extensions Editor** of a process diagram. Throwing events are mapped as `inputs` and catching events are mapped as `outputs` from an event.

#### Correlation keys

Message events can optionally contain a correlation key. If a correlation key is present then when a message is thrown it uses the `activiti:correlationKey` value and the `messageRef` of the throwing event to match against the same two properties in a catching event. If only one property is matched then the message will not be caught.

Using a [process variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) for the correlation key in a throwing event and a static value for its corresponding catching event allows for the message to only be caught in specific circumstances.

> **Note**: Message start events cannot contain a correlation key unless they are used in a [sub process](#sub-processes-and-call-activities).

#### Message flows

When messages are used between two different [pools](#pools-and-lanes) the sequence flow that connects them is a dotted line called a message flow. The message flow is part of the `collaboration` element in the XML created by introducing a pool. Message flows reference the throwing message event as the `sourceRef` and the catching message event as the `targetRef`.

{% endcapture %}
{% capture message-start-img %}

Message start events are displayed as a single thin circle with a hollow envelope icon inside.

{% endcapture %}
{% capture message-start-xml %}

An example of the XML of a message start event is:

```xml
<bpmn2:startEvent id="StartEvent2">
	<bpmn2:outgoing>SequenceFlow_1</bpmn2:outgoing>
	<bpmn2:messageEventDefinition messageRef="Message_15xakkk" />
</bpmn2:startEvent>
```

An example of the XML of a message is:

```xml
<bpmn2:message id="Message_15xakkk" name="Message_15xakkk" />
```

An example of the XML of a message payload is:

```json
    "mappings": {
        "EndEvent_0ss2fp3": {
            "inputs": {
                "name": {
                    "type": "variable",
                    "value": "username"
                },
                "order-number": {
                    "type": "value",
                    "value": 1459283
                }
            }
        }
    },
```

An example of the XML of a message with a correlation key is:

```xml
<bpmn2:endEvent id="EndEvent_1">
	<bpmn2:incoming>SequenceFlow_8</bpmn2:incoming>
	<bpmn2:messageEventDefinition messageRef="Message_1hxecs2" activiti:correlationKey="${userId}" />
```

In this example the message will only be caught if a catching event has a `messageRef` of `Message_1hxecs2` and an `activiti:correlationKey` that matches the value of `userId`.

An example of the XML of a message flow is:

```xml
<bpmn2:collaboration id="Collaboration_0kgbwi1">
	<bpmn2:participant id="Participant_1i6u1my" processRef="Process_1d9yxsm" />
	<bpmn2:participant id="Participant_10umhbc" processRef="Process_1piiyp4" />
	<bpmn2:messageFlow id="MessageFlow_0vh4zdb" sourceRef="Event_00acemq" targetRef="Event_13u5jtf" />
</bpmn2:collaboration>
```

{% endcapture %}

{% include tabs.html tableid="message-start" opt1="Properties" content1=message-start-prop opt2="Message" content2=message opt3="Appearance" content3=message-start-img opt4="XML" content4=message-start-xml %}

### Signal start event

Signal start events begin a process instance using a caught, named signal.

{% capture signal-start-prop %}

#### Basic properties

The basic properties for a signal start event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the signal start event. This is system generated and cannot be altered, for example `StartEvent_1w29b3h`. |
| Name | *Optional.* The name of the signal start event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the signal start event does. |

#### Signal

A signal needs to be defined for the signal start event to catch. A previously used **Signal** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. A **Signal name** can then be set.

Signals can be restricted to the process instance they are thrown in, or be global in scope. The scope of a global signal is restricted to the project they are used in.

{% endcapture %}
{% capture signal %}

Signal events can be either catching or throwing. A throwing signal event will emit a signal when it is reached in a process instance that will be picked up by any catching signal event with a matching signal name. Signals can be restricted to the process instance they are thrown in, or be global in scope. The scope of a global signal is restricted to the project they are used in.

The `id` of a signal will match against the `signalRef` of a catching or throwing event.

Signal events are displayed as a triangle icon inside different shapes that differentiate between the event types. A solid triangle represents a throwing event, whilst a hollow triangle represents a catching event.

{% endcapture %}
{% capture signal-start-img %}

Signal start events are displayed as a single thin circle with a hollow triangle icon inside.

{% endcapture %}
{% capture signal-start-xml %}

An example of the XML of a signal start event is:

```xml
<bpmn2:startEvent id="StartEvent1">
	<bpmn2:outgoing>SequenceFlow_1</bpmn2:outgoing>
 	<bpmn2:signalEventDefinition signalRef="Signal_0hnsd2r" />
</bpmn2:startEvent>
```

An example of the XML of a signal with a global scope is:

```xml
<bpmn2:signal id="Signal_0hnsd2r" name="Signal_0hnsd2r" />
```

An example of the XML of a signal with a process instance scope is:

```xml
<bpmn2:signal id="Signal_0hnsd2r" name="Signal_0hnsd2r" activiti:scope="processInstance" />
```

{% endcapture %}

{% include tabs.html tableid="signal-start" opt1="Properties" content1=signal-start-prop opt2="Signal" content2=signal opt3="Appearance" content3=signal-start-img opt4="XML" content4=signal-start-xml %}

### Timer start event

Timer start events begin a process at a specific time once or repeatedly at intervals.

{% capture timer-start-prop %}

#### Basic properties

The basic properties for a timer start event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the timer start event. This is system generated and cannot be altered, for example `StartEvent_1w29b3h`. |
| Name | *Optional.* The name of the timer start event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the timer start event does. |

### Form name

An optional [form]({% link process-automation/latest/model/forms.md %}) can be used to begin a process. The form must exist within the same project as the process definition to be selected. Select a form from the dropdown, else create a new form using the **+** symbol.

Once a form has been selected, it can be edited using the **Open Form** symbol.

#### Mapping type

The mapping type sets how data is passed between the timer start event and the process. There are [five options]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping) for how to send this data. The default value is **Send no variables**.

#### Timer

A choice of timer must be set for timer start events, based on a **Cycle**, **Date** or **Duration**.

{% endcapture %}
{% capture timer %}

Timer events are used to influence events at specific times, after a set amount of time has passed or at intervals. All timer events use the international standard [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601){:target="_blank"} for specifying time formats.

> **Note**: All properties within `timerEventDefinition` can accept process variables as their values as long as they are in ISO 8601 or cron expression format.

Timer events are displayed as a clock icon inside different shapes that differentiate between the event types.

#### timeDate

The `timeDate` property for timer events defines a specific date and time in ISO 8601 format for when the trigger will be fired and can include a specified time zone.

The following is an example of the `timerEventDefinition` using a `timeDate`:

* `2017-05-17` represents the 17th May 2017 in *YYYY-MM-DD* format
* `T12:42:23` represents the time of 12:42:23 in *hh:mm:ss* format
* `Z` represents that the time format is in UTC (Coordinated Universal Time). The time can also contain UTC offsets such as `+01` for an hour ahead of UTC. When an offset is defined the `Z` is not required, for example: `T12:42:23+01`

#### timeDuration

The `timeDuration` property for timer events defines how long a timer should wait in ISO 8601 format before the trigger is fired.

The following are the letters used to refer to duration:

| Letter | Description |
| ------ | ----------- |
| `P` | Designates that the following letters and numbers represent a duration. Must always be present |
| `Y` | Represents a year and follows the number of years, for example `P2Y` is 2 years |
| `M` | Represents a month and follows the number of months when preceded by a `P`, for example `P3Y4M` is 2 years and 4 months |
| `W` | Represents a week and follows the number of weeks, for example `P10W` for 10 weeks |
| `D` | Represents a day and follows the number of days, for example `P1Y1M1D` for 1 year, 1 month and 1 day |
| `T` | Designates that the following letters represent a duration of hours to seconds. Must always be present to refer to hours, minutes and seconds |
| `H` | Represents an hour and follows the number of hours, for example `P1DT0.5H` for 1 day and half an hour |
| `M` | Represents a minute and follows the number of minutes when preceded by a `T`, for example `PT1M` for 1 minute |
| `S` | Represents a second and follows the number of seconds, for example `P2Y3M4DT5H6M7S` for 2 years, 3 months, 4 days, 5 hours, 6 minutes and 7 seconds |

#### timeCycle

The `timeCycle` property for timer events defines intervals for the trigger to fire at. Intervals can be defined using the time intervals that adhere to the ISO 8601 standard or by using cron expressions.

##### Time intervals

Time intervals use the syntax `R/` to set a number of repetitions, for example `R5/` would repeat five times. 

Following the repetition, a duration can be set for when the repetition occurs, for example `R5/PT10H` would repeat every 10 hours, five times.

> **Note** The duration uses the same format as for `timeDuration`.

An optional end date can also be set after the duration and separated by a `/`.

> **Note**: The end date uses the same format as for `timeDate`.

##### Cron expression intervals

[Cron expressions](https://en.wikipedia.org/wiki/Cron#CRON_expression){:target="_blank"} can also be used to define repeating triggers for timer events.  

{% endcapture %}
{% capture timer-start-img %}

Timer start events are displayed as a single thin circle with a clock icon inside.

{% endcapture %}
{% capture timer-start-xml %}

An example of the XML of a timer start event is:

```xml
<bpmn2:startEvent id="StartEvent3">
    <bpmn2:outgoing>SequenceFlow_1</bpmn2:outgoing>
    <timerEventDefinition>
        <timeCycle xsi:type="bpmn2:tFormalExpression">R10/2020-12-10T13:00/PT12H</timeCycle>
    </timerEventDefinition>
</bpmn2:startEvent>
```

> **Note**: This will start the process 10 times, at 12 hour intervals starting on the 10th December 2020.

An example of the XML for `timeDate` is:

```xml
<bpmn2:timerEventDefinition> 
  <bpmn2:timeDate xsi:type="bpmn2:tFormalExpression">2017-05-17T12:42:23Z</bpmn2:timeDate>
</bpmn2:timerEventDefinition>
```

An example of the XML for `timeDuration` is:

```xml
<bpmn2:timerEventDefinition>
  <bpmn2:timeDuration xsi:type="bpmn2:tFormalExpression">P5D</bpmn2:timeDuration>
</bpmn2:timerEventDefinition>
```

> **Note**: This represents a duration of 5 days.

An example of the XML for `timeCycle` using time interval syntax is:

``` xml
<bpmn2:timerEventDefinition>
  <bpmn2:timeCycle xsi:type="bpmn2:tFormalExpression">R3/PT30M</bpmn2:timeCycle>
</bpmn2:timerEventDefinition> 
```

> **Note**: This represents three repetitions every 30 minutes.

An example of the XML for `timeCycle` using a cron expression is:

```xml
<bpmn2:timerEventDefinition>
  <bpmn2:timeCycle>0 0/5 * * * ?</bpmn2:timeCycle>
</bpmn2:timerEventDefinition>
```

> **Note**: This represents a trigger firing every 5 minutes beginning at the top of the hour.

{% endcapture %}

{% include tabs.html tableid="timer-start" opt1="Properties" content1=timer-start-prop opt2="Timer" content2=timer opt3="Appearance" content3=timer-start-img opt4="XML" content4=timer-start-xml %}

## End events

End events indicate where the current process flow ends, therefore there can be no outgoing [sequence flow](#sequence-flow) from an end event. Different types of end event can have have actions other than just ending the process flow execution path.

The types of end event are:

* [End events](#end-event)
* [Error end events](#error-end-event)
* [Message end events](#message-end-event)
* [Terminate end events](#terminate-end-event)

### End event

End events complete the process flow with no additional behavior.

{% capture end-prop %}

#### Basic properties

The basic properties for an end event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the end event. This is system generated and cannot be altered, for example `EndEvent_00ln22h`. |
| Name | *Optional.* The name of the end event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the end event does. |

{% endcapture %}
{% capture end-img %}

End events are displayed as a single thick circle without an icon inside.

{% endcapture %}
{% capture end-xml %}

An example of the XML of an end event is:

```xml
<bpmn2:endEvent id="EndEvent_1">
    <bpmn2:incoming>SequenceFlow_1</bpmn2:incoming>
</bpmn2:endEvent>
```

{% endcapture %}

{% include tabs.html tableid="end" opt1="Properties" content1=end-prop opt2="Appearance" content2=end-img opt3="XML" content3=end-xml %}

### Error end event

Error end events throw an error when the process flow reaches them.

{% capture error-end-prop %}

#### Basic properties

The basic properties for an error end event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the error end event. This is system generated and cannot be altered, for example `EndEvent_00ln22h`. |
| Name | *Optional.* The name of the error end event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the error end event does. |

#### Error

An error needs to be defined for the error end event to throw. A previously created **Error** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. An **Error name** and **Error code** can then be set.

{% endcapture %}
{% capture error-end-img %}

Error end events are displayed as a single thick circle with a solid lightning bolt icon inside.

{% endcapture %}
{% capture error-end-xml %}

An example of the XML of an error end event is:

```xml
<bpmn2:endEvent id="EndEvent_1">
    <bpmn2:incoming>SequenceFlow_8</bpmn2:incoming>
    <bpmn2:errorEventDefinition errorRef="Error_3vbkafg" />
</bpmn2:endEvent>
```

An example of the XML of an error is:

```xml
<bpmn2:error id="Error_3vbkafg" name="payment-failed-error" errorCode="404" />
```

{% endcapture %}

{% include tabs.html tableid="error-end" opt1="Properties" content1=error-end-prop opt2="Error" content2=error opt3="Appearance" content3=error-end-img opt4="XML" content4=error-end-xml %}

### Message end event

Message end events complete the process flow and send a message event.

{% capture message-end-prop %}

#### Basic properties

The basic properties for a message end event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the message end event. This is system generated and cannot be altered, for example `EndEvent_00ln22h`. |
| Name | *Optional.* The name of the message end event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the message end event does. |

#### Message

A message needs to be defined for the message end event to send. A previously created **Message** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. A **Message name** and payload can then be set.

{% endcapture %}
{% capture message-end-img %}

Message end events are displayed as a single thick circle with a solid envelope icon inside.

{% endcapture %}
{% capture message-end-xml %}

An example of the XML of a message end event is:

```xml
<bpmn2:endEvent id="EndEvent_1">
	<bpmn2:incoming>SequenceFlow_1</bpmn2:incoming>
	<bpmn2:messageEventDefinition messageRef="Message_45sdihj" />
</bpmn2:endEvent>
```

An example of the XML of a message is:

```xml
<bpmn2:message id="Message_15xakkk" name="Message_15xakkk" />
```

An example of the XML of a message payload is:

```json
    "mappings": {
        "EndEvent_0ss2fp3": {
            "inputs": {
                "name": {
                    "type": "variable",
                    "value": "username"
                },
                "order-number": {
                    "type": "value",
                    "value": 1459283
                }
            }
        }
    },
```

An example of the XML of a message with a correlation key is:

```xml
<bpmn2:endEvent id="EndEvent_1">
	<bpmn2:incoming>SequenceFlow_8</bpmn2:incoming>
	<bpmn2:messageEventDefinition messageRef="Message_1hxecs2" activiti:correlationKey="${userId}" />
```

In this example the message will only be caught if a catching event has a `messageRef` of `Message_1hxecs2` and an `activiti:correlationKey` that matches the value of `userId`.

An example of the XML of a message flow is:

```xml
<bpmn2:collaboration id="Collaboration_0kgbwi1">
	<bpmn2:participant id="Participant_1i6u1my" processRef="Process_1d9yxsm" />
	<bpmn2:participant id="Participant_10umhbc" processRef="Process_1piiyp4" />
	<bpmn2:messageFlow id="MessageFlow_0vh4zdb" sourceRef="Event_00acemq" targetRef="Event_13u5jtf" />
</bpmn2:collaboration>
```

{% endcapture %}

{% include tabs.html tableid="message-end" opt1="Properties" content1=message-end-prop opt2="Message" content2=message opt3="Appearance" content3=message-end-img opt4="XML" content4=message-end-xml %}

### Terminate end event

Terminate end events cause the current process scope to be immediately ended, including any parallel process flows. The scope is determined by the location of the terminate end event. If the terminate end event is in a [sub-process](#expanded-and-collapsed-sub-processes) or [call activity](#call-activity), only the sub-process or call activity instance will be ended, not the parent or originating process instance. In the case of a multi-instance sub-process or call activity only a single instance will be ended.

{% capture terminate-end-prop %}

#### Basic properties

The basic properties for a terminate end event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the terminate end event. This is system generated and cannot be altered, for example `EndEvent_00ln22h`. |
| Name | *Optional.* The name of the terminate end event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the terminate end event does. |

{% endcapture %}
{% capture terminate-end-img %}

Terminate end events are displayed as a single thick circle with a solid circle inside.

{% endcapture %}
{% capture terminate-end-xml %}

An example of the XML of a terminate end event is:

```xml
<bpmn2:endEvent id="EndEvent_1">
	<bpmn2:incoming>SequenceFlow_1</bpmn2:incoming>
	<bpmn2:terminateEventDefinition id="TerminateEventDefinition_0j911ut"/>
</bpmn2:endEvent>
```

{% endcapture %}

{% include tabs.html tableid="terminate-end" opt1="Properties" content1=terminate-end-prop opt2="Appearance" content2=terminate-end-img opt3="XML" content3=terminate-end-xml %}

## Intermediate events

Intermediate events can be used at any point throughout a process. They always provide additional behavior such as throwing a signal or catching a timer.

The types of intermediate event are:

* [Message intermediate catch events](#message-intermediate-catch-event)
* [Message intermediate throw events](#message-intermediate-throw-event)
* [Signal intermediate catch events](#signal-intermediate-catch-event)
* [Signal intermediate throw events](#signal-intermediate-throw-event)
* [Timer intermediate catch events](#timer-intermediate-catch-event)

### Message intermediate catch event

Message intermediate catching events cause the process flow to wait until the message named in the `messageRef` property is received before it proceeds.

{% capture message-int-cat-prop %}

#### Basic properties

The basic properties for a message intermediate catch event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the message intermediate catch event. This is system generated and cannot be altered, for example `IntermediateThrowEvent_1yohpmt`. |
| Name | *Optional.* The name of the message intermediate catch event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the message intermediate catch event does. |

#### Message

A message needs to be defined for the message intermediate catch event to catch. A previously created **Message** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. A **Message name** and payload can then be set.

{% endcapture %}
{% capture message-int-cat-img %}

Message intermediate catching events are displayed as two thin concentric circles with a hollow envelope icon inside.

{% endcapture %}
{% capture message-int-cat-xml %}

An example of the XML of a message intermediate catch events is:

```xml
<bpmn2:intermediateCatchEvent id="IntermediateCatchEvent2">
	<bpmn2:incoming>SequenceFlow_5</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_6</bpmn2:outgoing>
    <bpmn2:messageEventDefinition messageRef="Message_6" />
</bpmn2:intermediateCatchEvent>
```

An example of the XML of a message is:

```xml
<bpmn2:message id="Message_15xakkk" name="Message_15xakkk" />
```

An example of the XML of a message payload is:

```json
    "mappings": {
        "EndEvent_0ss2fp3": {
            "inputs": {
                "name": {
                    "type": "variable",
                    "value": "username"
                },
                "order-number": {
                    "type": "value",
                    "value": 1459283
                }
            }
        }
    },
```

An example of the XML of a message with a correlation key is:

```xml
<bpmn2:endEvent id="EndEvent_1">
	<bpmn2:incoming>SequenceFlow_8</bpmn2:incoming>
	<bpmn2:messageEventDefinition messageRef="Message_1hxecs2" activiti:correlationKey="${userId}" />
```

In this example the message will only be caught if a catching event has a `messageRef` of `Message_1hxecs2` and an `activiti:correlationKey` that matches the value of `userId`.

An example of the XML of a message flow is:

```xml
<bpmn2:collaboration id="Collaboration_0kgbwi1">
	<bpmn2:participant id="Participant_1i6u1my" processRef="Process_1d9yxsm" />
	<bpmn2:participant id="Participant_10umhbc" processRef="Process_1piiyp4" />
	<bpmn2:messageFlow id="MessageFlow_0vh4zdb" sourceRef="Event_00acemq" targetRef="Event_13u5jtf" />
</bpmn2:collaboration>
```

{% endcapture %}

{% include tabs.html tableid="message-int-cat" opt1="Properties" content1=message-int-cat-prop opt2="Message" content2=message opt3="Appearance" content3=message-int-cat-img opt4="XML" content4=message-int-cat-xml %}

### Message intermediate throw event

Message intermediate throw events send the message event named in the `messageRef` property when the process flow reaches them.

{% capture message-int-thro-prop %}

#### Basic properties

The basic properties for a message intermediate throw event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the message intermediate throw event. This is system generated and cannot be altered, for example `IntermediateThrowEvent_1yohpmt`. |
| Name | *Optional.* The name of the message intermediate throw event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the message intermediate throw event does. |

#### Message

A message needs to be defined for the message intermediate throw event to catch. A previously created **Message** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. A **Message name** and payload can then be set.

{% endcapture %}
{% capture message-int-thro-img %}

Message intermediate throwing events are displayed as two thin concentric circles with a solid envelope icon inside.

{% endcapture %}
{% capture message-int-thro-xml %}

An example of the XML of a message intermediate throw events is:

```xml
<bpmn2:intermediateThrowEvent id="IntermediateThrowEvent1">
	<bpmn2:incoming>SequenceFlow_5</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_6</bpmn2:outgoing>
    <bpmn2:messageEventDefinition messageRef="Message_6" />
</bpmn2:intermediateThrowEvent>
```

An example of the XML of a message is:

```xml
<bpmn2:message id="Message_15xakkk" name="Message_15xakkk" />
```

An example of the XML of a message payload is:

```json
    "mappings": {
        "EndEvent_0ss2fp3": {
            "inputs": {
                "name": {
                    "type": "variable",
                    "value": "username"
                },
                "order-number": {
                    "type": "value",
                    "value": 1459283
                }
            }
        }
    },
```

An example of the XML of a message with a correlation key is:

```xml
<bpmn2:endEvent id="EndEvent_1">
	<bpmn2:incoming>SequenceFlow_8</bpmn2:incoming>
	<bpmn2:messageEventDefinition messageRef="Message_1hxecs2" activiti:correlationKey="${userId}" />
```

In this example the message will only be caught if a catching event has a `messageRef` of `Message_1hxecs2` and an `activiti:correlationKey` that matches the value of `userId`.

An example of the XML of a message flow is:

```xml
<bpmn2:collaboration id="Collaboration_0kgbwi1">
	<bpmn2:participant id="Participant_1i6u1my" processRef="Process_1d9yxsm" />
	<bpmn2:participant id="Participant_10umhbc" processRef="Process_1piiyp4" />
	<bpmn2:messageFlow id="MessageFlow_0vh4zdb" sourceRef="Event_00acemq" targetRef="Event_13u5jtf" />
</bpmn2:collaboration>
```

{% endcapture %}

{% include tabs.html tableid="message-int-thro" opt1="Properties" content1=message-int-thro-prop opt2="Message" content2=message opt3="Appearance" content3=message-int-thro-img opt4="XML" content4=message-int-thro-xml %}

### Signal intermediate catch event

Signal intermediate catching events cause the process flow to wait until the signal named in the `signalRef` property is received before it proceeds.

{% capture signal-int-cat-prop %}

#### Basic properties

The basic properties for a signal intermediate catch event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the signal intermediate catch event. This is system generated and cannot be altered, for example `IntermediateThrowEvent_1yohpmt`. |
| Name | *Optional.* The name of the signal intermediate catch event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the signal intermediate catch event does. |

#### Signal

A signal needs to be defined for the signal intermediate catch event to catch. A previously used **Signal** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. A **Signal name** can then be set.

Signals can be restricted to the process instance they are thrown in, or be global in scope. The scope of a global signal is restricted to the project they are used in.

{% endcapture %}
{% capture signal-int-cat-img %}

Signal intermediate catching events are displayed as two thin concentric circles with a hollow triangle icon inside.

{% endcapture %}
{% capture signal-int-cat-xml %}

An example of the XML of a signal intermediate catch events is:
	
```xml
<bpmn2:intermediateCatchEvent id="IntermediateCatchEvent2">
	<bpmn2:incoming>SequenceFlow_5</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_6</bpmn2:outgoing>
    <bpmn2:signalEventDefinition signalRef="Signal_0hnsd2r" />
</bpmn2:intermediateCatchEvent>
```

An example of the XML of a signal with a global scope is:

```xml
<bpmn2:signal id="Signal_0hnsd2r" name="Signal_0hnsd2r" />
```

An example of the XML of a signal with a process instance scope is:

```xml
<bpmn2:signal id="Signal_0hnsd2r" name="Signal_0hnsd2r" activiti:scope="processInstance" />
```

{% endcapture %}

{% include tabs.html tableid="signal-int-cat" opt1="Properties" content1=signal-int-cat-prop opt2="Signal" content2=signal opt3="Appearance" content3=signal-int-cat-img opt4="XML" content4=signal-int-cat-xml %}

### Signal intermediate throw event

Signal intermediate throw events are events that emit a signal when they are reached in the process flow. The signal that is emitted is then caught by any catching signal events with a name matching the signal that was thrown.

{% capture signal-int-thro-prop %}

#### Basic properties

The basic properties for a signal intermediate throw event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the signal intermediate throw event. This is system generated and cannot be altered, for example `IntermediateThrowEvent_1yohpmt`. |
| Name | *Optional.* The name of the signal intermediate throw event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the signal intermediate throw event does. |

#### Signal

A signal needs to be defined for the signal intermediate throw event to emit when it is reached. A previously used **Signal** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. A **Signal name** can then be set.

Signals can be restricted to the process instance they are thrown in, or be global in scope. The scope of a global signal is restricted to the project they are used in.

{% endcapture %}
{% capture signal-int-thro-img %}

Signal intermediate throw events are displayed as two thin concentric circles with a solid triangle icon inside.

{% endcapture %}
{% capture signal-int-thro-xml %}

An example of the XML of a signal intermediate catch events is:

```xml
<bpmn2:intermediateThrowEvent id="IntermediateThrowEvent1">
	<bpmn2:incoming>SequenceFlow_3</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_4</bpmn2:outgoing>
   <bpmn2:signalEventDefinition signalRef="Signal_1jiw9tp" />
</bpmn2:intermediateThrowEvent>
```

An example of the XML of a signal with a global scope is:

```xml
<bpmn2:signal id="Signal_0hnsd2r" name="Signal_0hnsd2r" />
```

An example of the XML of a signal with a process instance scope is:

```xml
<bpmn2:signal id="Signal_0hnsd2r" name="Signal_0hnsd2r" activiti:scope="processInstance" />
```

{% endcapture %}

{% include tabs.html tableid="signal-int-thro" opt1="Properties" content1=signal-int-thro-prop opt2="Signal" content2=signal opt3="Appearance" content3=signal-int-thro-img opt4="XML" content4=signal-int-thro-xml %}

### Timer intermediate catch event

Timer intermediate catching events cause the process flow to wait until a specific time or interval is reached. The time to wait is defined in the `timerEventDefinition` property.

{% capture timer-int-cat-prop %}

#### Basic properties

The basic properties for a timer intermediate catch event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the timer intermediate catch event. This is system generated and cannot be altered, for example `IntermediateThrowEvent_1yohpmt`. |
| Name | *Optional.* The name of the timer intermediate catch event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the timer intermediate catch event does. |

#### Timer

A choice of timer must be set for timer start events, based on a **Cycle**, **Date** or **Duration**.

{% endcapture %}
{% capture timer-int-cat-img %}

Timer intermediate catch events are displayed as two thin concentric circles with a clock icon inside.

{% endcapture %}
{% capture timer-int-cat-xml %}

An example of the XML of a signal intermediate catch events is:

```xml
<bpmn2:intermediateCatchEvent id="IntermediateCatchEvent5">
	<bpmn2:incoming>SequenceFlow_3</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_4</bpmn2:outgoing>
	<bpmn2:timerEventDefinition>
  		<bpmn2:timeDuration xsi:type="bpmn2:tFormalExpression">P5D</bpmn2:timeDuration>
	</bpmn2:timerEventDefinition>
</bpmn2:intermediateCatchEvent>
```

> **Note**: This will wait five days before continuing the process.

An example of the XML for `timeDate` is:

```xml
<bpmn2:timerEventDefinition> 
  <bpmn2:timeDate xsi:type="bpmn2:tFormalExpression">2017-05-17T12:42:23Z</bpmn2:timeDate>
</bpmn2:timerEventDefinition>
```

An example of the XML for `timeDuration` is:

```xml
<bpmn2:timerEventDefinition>
  <bpmn2:timeDuration xsi:type="bpmn2:tFormalExpression">P5D</bpmn2:timeDuration>
</bpmn2:timerEventDefinition>
```

> **Note**: This represents a duration of 5 days.

An example of the XML for `timeCycle` using time interval syntax is:

``` xml
<bpmn2:timerEventDefinition>
  <bpmn2:timeCycle xsi:type="bpmn2:tFormalExpression">R3/PT30M</bpmn2:timeCycle>
</bpmn2:timerEventDefinition> 
```

> **Note**: This represents three repetitions every 30 minutes.

An example of the XML for `timeCycle` using a cron expression is:

```xml
<bpmn2:timerEventDefinition>
  <bpmn2:timeCycle>0 0/5 * * * ?</bpmn2:timeCycle>
</bpmn2:timerEventDefinition>
```

> **Note**: This represents a trigger firing every 5 minutes beginning at the top of the hour.

{% endcapture %}

{% include tabs.html tableid="timer-int-cat" opt1="Properties" content1=timer-int-cat-prop opt2="Timer" content2=timer opt3="Appearance" content3=timer-int-cat-img opt4="XML" content4=timer-int-cat-xml %}

## Boundary events

Boundary events are assigned to other BPMN elements such as service tasks and user tasks. They are used by dragging the selected boundary type onto the BPMN element to influence and using the spanner icon to select the type of boundary event to use.

Whilst the element that the boundary event is attached to is being executed within a process instance, the boundary event is waiting for its trigger event. Once that event occurs the behavior can follow one of two paths:

* Interrupting behavior where the element's execution is terminated by the boundary event and the sequence flow out of the boundary event is followed. Interrupting boundary events are displayed as solid lines.

* Non-interrupting behavior where the element's execution continues and a new sequence flow is followed from the boundary event in parallel to the main sequence flow. Non-interrupting boundary events are displayed as dashed lines.

> **Note**: Depending on the boundary type, a trigger may never reach the attached boundary event. For example a signal may not be thrown for a signal boundary event to catch.

Boundary events use the `attachedToRef` property to indicate the `id` of the element they are attached to. Interrupting behavior is the default for boundary events. Non-interrupting events contain the `cancelActivity=false` property.

The types of boundary event are:

* [Error boundary events](#error-boundary-event)
* [Message boundary events](#message-boundary-event)
* [Signal boundary events](#signal-boundary-event)
* [Timer boundary events](#timer-boundary-event)

### Error boundary event

Error boundary events catch error events on the boundary of another element. Error boundary events are always interrupting, so as soon as an error is caught all process execution within the element they are attached to ceases.

{% capture error-bound-prop %}

#### Basic properties

The basic properties for an error boundary event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the error boundary event. This is system generated and cannot be altered, for example `IntermediateThrowEvent_1yohpmt`. |
| Name | *Optional.* The name of the error boundary event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the error boundary event does. |

#### Error

An error needs to be defined for the error boundary event to catch. A previously created **Error** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. An **Error name** and **Error code** can then be set.

{% endcapture %}
{% capture error-bound-img %}

Error boundary events are displayed as two thin concentric circles with a hollow lightning bolt icon inside attached to the border of another BPMN element.

{% endcapture %}
{% capture error-bound-xml %}

An example of the XML of an error boundary events is:

```xml
<bpmn2:boundaryEvent id="BoundaryEvent2" attachedToRef="ServiceTask1">
	<bpmn2:errorEventDefinition errorRef="Error_0vbkbeb" />
</bpmn2:boundaryEvent>
```

An example of the XML of a signal is:

```xml
<bpmn2:error id="Error_0vbkbeb" name="payment-failed-error" errorCode="404" />
```

{% endcapture %}

{% include tabs.html tableid="error-bound" opt1="Properties" content1=error-bound-prop opt2="Error" content2=error opt3="Appearance" content3=error-bound-img opt4="XML" content4=error-bound-xml %}

### Message boundary event

Message boundary events are attached to the boundary of another element. When a named message is received by the message boundary event, the process flow will be interrupted or a concurrent flow will be created depending on whether the event is interrupting or non-interrupting.

{% capture message-bound-prop %}

#### Basic properties

The basic properties for a message boundary event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the message boundary event. This is system generated and cannot be altered, for example `IntermediateThrowEvent_1yohpmt`. |
| Name | *Optional.* The name of the message boundary event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the message boundary event does. |

#### Message

A message needs to be defined for the message boundary event to catch when it is thrown. A previously created **Message** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. A **Message name** and payload can then be set.

{% endcapture %}
{% capture message-bound-img %}

Message boundary events are displayed as two thin concentric circles, or two thin dashed concentric circles, with a hollow envelope icon inside attached to the border of another BPMN element.

{% endcapture %}
{% capture message-bound-xml %}

An example of the XML of an interrupting message boundary events is:

```xml
<bpmn2:boundaryEvent id="BoundaryEvent1" attachedToRef="UserTask2">
	<bpmn2:outgoing>SequenceFlow5</bpmn2:outgoing>
	<bpmn2:messageEventDefinition messageRef="Message_15xakkk" />
</bpmn2:boundaryEvent>
```

An example of the XML of a non-interrupting message boundary events is:

```xml
<bpmn2:boundaryEvent id="BoundaryEvent3" cancelActivity="false" attachedToRef="SubProcess2">
	<bpmn2:outgoing>SequenceFlow8</bpmn2:outgoing>
	<bpmn2:messageEventDefinition messageRef="Message_02satcd" />
</bpmn2:boundaryEvent>
```

The XML representation of a message is:

```xml
<bpmn2:message id="Message_02satcd" name="Message_02satcd" />
```

An example of the XML of a message payload is:

```json
    "mappings": {
        "EndEvent_0ss2fp3": {
            "inputs": {
                "name": {
                    "type": "variable",
                    "value": "username"
                },
                "order-number": {
                    "type": "value",
                    "value": 1459283
                }
            }
        }
    },
```

An example of the XML of a message with a correlation key is:

```xml
<bpmn2:endEvent id="EndEvent_1">
	<bpmn2:incoming>SequenceFlow_8</bpmn2:incoming>
	<bpmn2:messageEventDefinition messageRef="Message_1hxecs2" activiti:correlationKey="${userId}" />
```

In this example the message will only be caught if a catching event has a `messageRef` of `Message_1hxecs2` and an `activiti:correlationKey` that matches the value of `userId`.

An example of the XML of a message flow is:

```xml
<bpmn2:collaboration id="Collaboration_0kgbwi1">
	<bpmn2:participant id="Participant_1i6u1my" processRef="Process_1d9yxsm" />
	<bpmn2:participant id="Participant_10umhbc" processRef="Process_1piiyp4" />
	<bpmn2:messageFlow id="MessageFlow_0vh4zdb" sourceRef="Event_00acemq" targetRef="Event_13u5jtf" />
</bpmn2:collaboration>
```

{% endcapture %}

{% include tabs.html tableid="message-bound" opt1="Properties" content1=message-bound-prop opt2="Message" content2=message opt3="Appearance" content3=message-bound-img opt4="XML" content4=message-bound-xml %}

### Signal boundary event

Signal boundary events can be considered catching events as they always wait to receive a named signal from a throwing event.

{% capture signal-bound-prop %}

#### Basic properties

The basic properties for a signal boundary event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the signal boundary event. This is system generated and cannot be altered, for example `IntermediateThrowEvent_1yohpmt`. |
| Name | *Optional.* The name of the signal boundary event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the signal boundary event does. |

#### Signal

A signal needs to be defined for the signal boundary event to catch. A previously used **Signal** can be selected from the dropdown in its properties, or a new one created using the **+** symbol. A **Signal name** can then be set.

Signals can be restricted to the process instance they are thrown in, or be global in scope. The scope of a global signal is restricted to the project they are used in.

{% endcapture %}
{% capture signal-bound-img %}

Signal boundary events are displayed as two thin concentric circles with a hollow triangle icon inside attached to the border of another BPMN element.

{% endcapture %}
{% capture signal-bound-xml %}

An example of the XML of a signal boundary events is:

```xml
<bpmn2:boundaryEvent id="BoundaryEvent1" attachedToRef="ServiceTask3">
      <bpmn2:signalEventDefinition signalRef="Signal_0iikg75" />
</bpmn2:boundaryEvent>
```

An example of the XML of a signal with a global scope is:

```xml
<bpmn2:signal id="Signal_0hnsd2r" name="Signal_0hnsd2r" />
```

An example of the XML of a signal with a process instance scope is:

```xml
<bpmn2:signal id="Signal_0hnsd2r" name="Signal_0hnsd2r" activiti:scope="processInstance" />
```

{% endcapture %}

{% include tabs.html tableid="signal-bound" opt1="Properties" content1=signal-bound-prop opt2="Signal" content2=signal opt3="Appearance" content3=signal-bound-img opt4="XML" content4=signal-bound-xml %}

### Timer boundary event

Timer boundary events can be interrupting or non-interrupting. They wait for a specified time before triggering and can also be set to trigger at multiple intervals.

{% capture timer-bound-prop %}

#### Basic properties

The basic properties for a timer boundary event are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the timer boundary event. This is system generated and cannot be altered, for example `IntermediateThrowEvent_1yohpmt`. |
| Name | *Optional.* The name of the timer boundary event. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the timer boundary event does. |

#### Timer

A choice of timer must be set for timer start events, based on a **Cycle**, **Date** or **Duration**.

{% endcapture %}
{% capture timer-bound-img %}

Timer boundary events are displayed as two thin concentric circles, or two thin dashed concentric circles, with a clock icon inside attached to the border of another BPMN element.

{% endcapture %}
{% capture timer-bound-xml %}

An example of the XML of an interrupting timer boundary events is:

```xml
<bpmn2:boundaryEvent id="BoundaryEvent3" attachedToRef="UserTask1">
	<bpmn2:outgoing>SequenceFlow5</bpmn2:outgoing>
	<bpmn2:timerEventDefinition>
		<bpmn2:timeDuration xsi:type="bpmn2:tFormalExpression">PT10M</bpmn2:timeDuration>
	</bpmn2:timerEventDefinition>
</bpmn2:boundaryEvent>
```

An example of the XML of a non-interrupting timer boundary events is:

```xml
<bpmn2:boundaryEvent id="BoundaryEvent4" cancelActivity="false" attachedToRef="SubProcess1">
	<bpmn2:outgoing>SequenceFlow8</bpmn2:outgoing>
	<bpmn2:timerEventDefinition>
		<bpmn2:timeDuration xsi:type="bpmn2:tFormalExpression">P5D</bpmn2:timeDuration>
	</bpmn2:timerEventDefinition>
</bpmn2:boundaryEvent>
```

An example of the XML for `timeDate` is:

```xml
<bpmn2:timerEventDefinition> 
  <bpmn2:timeDate xsi:type="bpmn2:tFormalExpression">2017-05-17T12:42:23Z</bpmn2:timeDate>
</bpmn2:timerEventDefinition>
```

An example of the XML for `timeDuration` is:

```xml
<bpmn2:timerEventDefinition>
  <bpmn2:timeDuration xsi:type="bpmn2:tFormalExpression">P5D</bpmn2:timeDuration>
</bpmn2:timerEventDefinition>
```

> **Note**: This represents a duration of 5 days.

An example of the XML for `timeCycle` using time interval syntax is:

``` xml
<bpmn2:timerEventDefinition>
  <bpmn2:timeCycle xsi:type="bpmn2:tFormalExpression">R3/PT30M</bpmn2:timeCycle>
</bpmn2:timerEventDefinition> 
```

> **Note**: This represents three repetitions every 30 minutes.

An example of the XML for `timeCycle` using a cron expression is:

```xml
<bpmn2:timerEventDefinition>
  <bpmn2:timeCycle>0 0/5 * * * ?</bpmn2:timeCycle>
</bpmn2:timerEventDefinition>
```

> **Note**: This represents a trigger firing every 5 minutes beginning at the top of the hour.

{% endcapture %}

{% include tabs.html tableid="timer-bound" opt1="Properties" content1=timer-bound-prop opt2="Timer" content2=timer opt3="Appearance" content3=timer-bound-img opt4="XML" content4=timer-bound-xml %}

## Gateways

Gateways are used to deal with convergence and divergence of the process flow. They allow for more than one fork of a process to be followed, or they can evaluate conditions so that a different route may be followed for each specific set of circumstances.

The types of gateway are:

* [Exclusive gateways](#exclusive-gateway)
* [Inclusive gateways](#inclusive-gateway)
* [Parallel gateways](#parallel-gateway)

### Exclusive gateway

Exclusive gateways represent a decision within a process.

Once the process flow reaches an exclusive gateway, all of the outgoing sequence flow options are evaluated in the order they are defined. The first option that evaluates to true is the sequence flow that is followed. A default sequence flow can be set incase none of the outgoing sequence flows evaluate to true.

{% capture excl-gate-prop %}

#### Basic properties

The basic properties for an exclusive gateway are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the exclusive gateway. This is system generated and cannot be altered, for example `Gateway_1ppp31l`. |
| Name | *Optional.* The name of the exclusive gateway. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the exclusive gateway does. |

#### Default sequence flow

The name of a [sequence flow](#sequence-flow) can be used to select a default flow for the gateway to take. This path will be followed if none of the other sequence flows evaluate to true. Conditional expressions can be configured on sequence flows to select which path is taken.

{% endcapture %}
{% capture excl-gate-img %}

Exclusive gateways are displayed as a single thin diamond shape with an X icon inside.

> **Note**: A single thin diamond on its own defaults to an exclusive gateway, however the BPMN specification does not allow diamonds with, and without, an X in the same process definition.

{% endcapture %}
{% capture excl-gate-xml %}

An example of the XML of an exclusive gateway is:

```xml
<bpmn2:exclusiveGateway id="ExclusiveGateway_1" name="Content Accepted?" default="SequenceFlow_2">
	<bpmn2:incoming>SequenceFlow_1</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_2</bpmn2:outgoing>
	<bpmn2:outgoing>SequenceFlow_3</bpmn2:outgoing>
</bpmn2:exclusiveGateway>
    <bpmn2:sequenceFlow id="SequenceFlow_1" sourceRef="Task_1" targetRef="ExclusiveGateway_1" />
    <bpmn2:sequenceFlow id="SequenceFlow_2" name="yes" sourceRef="ExclusiveGateway_1" targetRef="Task_2">
		<bpmn2:conditionExpression xsi:type="bpmn:tFormalExpression">${content.approved == true}</bpmn2:conditionExpression>
	</bpmn2:sequenceFlow>
    <bpmn2:sequenceFlow id="SequenceFlow_3" name="no" sourceRef="ExclusiveGateway_1" targetRef="Task_3">
		<bpmn2:conditionExpression xsi:type="bpmn:tFormalExpression">${content.approved == false}</bpmn2:conditionExpression>
    </bpmn2:sequenceFlow>
```

{% endcapture %}

{% include tabs.html tableid="excl-gate" opt1="Properties" content1=excl-gate-prop opt2="Appearance" content2=excl-gate-img opt3="XML" content3=excl-gate-xml %}

### Inclusive gateway

Inclusive gateways allow for convergence and divergence in a process, however they also allow for conditional sequence flows.

Once the process flow reaches an inclusive gateway, all of the outgoing sequence flows are evaluated and all flows that evaluate to true are followed for divergent behavior. A default sequence flow can be set incase none of the outgoing sequence flows evaluate to true.

For a converging inclusive gateway, the process waits until all active sequence flows reach the gateway before continuing.

{% capture incl-gate-prop %}

#### Basic properties

The basic properties for an inclusive gateway are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the inclusive gateway. This is system generated and cannot be altered, for example `Gateway_1ppp31l`. |
| Name | *Optional.* The name of the inclusive gateway. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the inclusive gateway does. |

#### Default sequence flow

The name of a [sequence flow](#sequence-flow) can be used to select a default flow for the gateway to take. This path will be followed if none of the other sequence flows evaluate to true. Conditional expressions can be configured on sequence flows to select which path is taken.

{% endcapture %}
{% capture incl-gate-img %}

Inclusive gateways are displayed as a single thin diamond shape with a circle inside.

{% endcapture %}
{% capture incl-gate-xml %}

An example of the XML of an inclusive gateway is:

```xml
<bpmn2:inclusiveGateway id="InclusiveGateway_1" name="Content Metadata" default="SequenceFlow_2">
	<bpmn2:incoming>SequenceFlow_1</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_2</bpmn2:outgoing>
	<bpmn2:outgoing>SequenceFlow_3</bpmn2:outgoing>
</bpmn2:inclusiveGateway>
    <bpmn2:sequenceFlow id="SequenceFlow_1" sourceRef="Task_1" targetRef="InclusiveGateway_1" />
    <bpmn2:sequenceFlow id="SequenceFlow_2" name="yes" sourceRef="InclusiveGateway_1" targetRef="Task_2">
		<bpmn2:conditionExpression xsi:type="bpmn:tFormalExpression">${content.size == "A4"}</bpmn2:conditionExpression>
	</bpmn2:sequenceFlow>
    <bpmn2:sequenceFlow id="SequenceFlow_3" name="no" sourceRef="InclusiveGateway_1" targetRef="Task_3">
		<bpmn2:conditionExpression xsi:type="bpmn:tFormalExpression">${content.origin == "Email"}</bpmn2:conditionExpression>
    </bpmn2:sequenceFlow>
```

{% endcapture %}

{% include tabs.html tableid="incl-gate" opt1="Properties" content1=incl-gate-prop opt2="Appearance" content2=incl-gate-img opt3="XML" content3=incl-gate-xml %}

### Parallel gateway

Parallel gateways represent a concurrent convergence or divergence in a process.

Divergence means that all sequence flows exiting a parallel gateway are executed concurrently. A converging parallel gateway waits for all concurrent sequence flows to arrive at the gateway, before continuing with the process.

Parallel gateways do not evaluate conditions. Any conditions set on a sequence flow will be ignored by the parallel gateway.

> **Note**: It is possible for a single parallel gateway to execute both converging and diverging behavior.

{% capture para-gate-prop %}

#### Basic properties

The basic properties for a parallel gateway are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the parallel gateway. This is system generated and cannot be altered, for example `Gateway_1ppp31l`. |
| Name | *Optional.* The name of the parallel gateway. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the parallel gateway does. |

{% endcapture %}
{% capture para-gate-img %}

Parallel gateways are displayed as a single thin diamond shape with a + icon inside.

{% endcapture %}
{% capture para-gate-xml %}

An example of the XML of a parallel gateway is:

```xml
<bpmn2:parallelGateway id="Fork_1">
	<bpmn2:sequenceFlow id="SequenceFlow_1" sourceRef="Fork_1" targetRef="UserTask_1" />
 	</bpmn2:sequenceFlow>
 	<bpmn2:sequenceFlow id="SequenceFlow_2" sourceRef="Fork_1" targetRef="ServiceTask_1" />
 	</bpmn2:sequenceFlow>
</bpmn2:parallelGateway>
```

{% endcapture %}

{% include tabs.html tableid="para-gate" opt1="Properties" content1=para-gate-prop opt2="Appearance" content2=para-gate-img opt3="XML" content3=para-gate-xml %}

## Tasks

Tasks are used in a process to include other models from a project in a process.

The types of task are:

* [Business rule tasks](#business-rule-task)
* [Script tasks](#script-task)
* [Service tasks](#service-task)
* [User tasks](#user-task)

### Business rule task

Business rule tasks are used to include [decision tables]({% link process-automation/latest/model/decisions.md %}) in a process definition.

Business rule tasks are essentially treated as service tasks and will always have the `implementation` value of `dmn-connector.EXECTUTE_TABLE`. The `name` of the decision table that is associated to the business rule task is used as the `value` under `_activiti_dmn_table_` when viewing the **Extensions Editor**.

{% capture business-prop %}

#### Basic properties

The basic properties for a business rule task are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the business rule task. This is system generated and cannot be altered, for example `ServiceTask_0a1cgxd`. |
| Name | *Optional.* The name of the business rule task. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the business rule task does. |

#### Multi-instance type

Business rule tasks can be set to repeat sequentially or in parallel when the process flow reaches them.

#### Decision table name

The name of the [decision table]({% link process-automation/latest/model/decisions.md %}) to use. The decision table must exist within the same project as the process definition to be selected. Select a decision table from the dropdown, else create a new one using the **+** symbol.

#### Mapping type

The mapping type sets how data is passed between the decision table and the process. There are [five options]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping) for how to send this data. The default value is **Send no variables**.

{% endcapture %}
{% capture multi %}

Multi-instance allows for the element to be repeated within a process. There are two options for how to execute multi-instance elements: sequentially or in parallel.

* Sequential executions only ever have a single instance running at any one time. The next instance will only start after the previous one has been completed.

* Parallel executions start all instances at once, meaning they are all active and can all be worked on at the same time.

Multi instance elements are displayed as three parallel lines at the bottom of the original element. Sequential lines are horizontal and parallel lines are vertical.

#### Variables

Each multi-instance execution has three variables:

| Variable | Description |
| -------- | ----------- |
| nrOfInstances | The total number of instances |
| nrOfActiveInstances | The number of currently active instances. For sequential multi-instances the value will always be 1 |
| nrOfCompletedInstances | The number of instances that have already been completed |

> **Note**: These variables can be used in multi-instance expressions without having to be declared as [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables).

Each instance in the multi-instance execution also has an instance-local variable that is not visible to other instances, nor to the process instance:

| Variable | Description |
| -------- | ----------- |
| loopCounter | The index in the for-each loop of that particular instance |

#### Cardinality

Cardinality sets the number of instances to be executed by the multi-instance element. This can be set as a static value, a [process variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) or calculated as an expression.

#### Collection

A collection can be used to set the number of instances to be executed by referencing a list of items.

An element variable can optionally be used with a collection. An element variable is used to create a variable for each instance of the multi-instance element and each variable created by the element variable is assigned one value from the collection.

#### Completion condition

A completion condition can optionally be included for multi-instances. When the completion condition evaluates to `true`, all remaining instances are cancelled and the multi-instance activity ends.

#### Results

A result collection can be set to aggregate the results from each instance into a variable. The result collection is created as a process variable after instance execution has finished.

The result element variable is used to select the field or variable from the BPMN element to aggregate into the result collection.

{% endcapture %}
{% capture business-img %}

Business rule tasks are displayed as a single, thin rounded rectangle with a table icon inside.

{% endcapture %}
{% capture business-xml %}

An example of the XML of a business rule task is:

```xml
<bpmn2:serviceTask id="ServiceTask_4" implementation="dmn-connector.EXECUTE_TABLE" />
```

An example of the **Extensions Editor** JSON of a process containing a business rule task is:

```json
"constants": {
	"ServiceTask_2f85xew": {
		"_activiti_dmn_table_": {
			"value": "my-decision-table-1"
            }
        }
    },
```

An example of the XML for an element that contains sequential multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics isSequential="true" />
```

An example of the XML for an element that contains parallel multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics  isSequential="false" />
```

or

```xml
<bpmn2:multiInstanceLoopCharacteristics />

```

An example of the XML of multi-instance cardinality is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>5</bpmn2:loopCardinality>
</bpmn2:multiInstanceLoopCharacteristics>
```

An example of the XML of a multi-instance collection is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${user}">
	<bpmn2:incoming>SequenceFlow_5</bpmn2:incoming>
	<bpmn2:multiInstanceLoopCharacteristics activiti:collection="${userList.users}" activiti:elementVariable="user">
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The `activiti:collection` references a process variable called `userList` that contains the following JSON:
>
>```json
>{"users":["user1", "user2", "user3"]}
>```
>
>In the example:
>
>* Three user tasks will be created because there are three items in the process variable that `activiti:collection` uses.
>* A variable will be created for each instance called `users` with the values `user1`, `user2` and `user3` because the `activiti:elementVariable` is set to `"users"`.
>* A user tasks will be assigned to each of the users because the `activiti:assignee` is set to `{users}` which is the name of the variable created in each instance by the element variable.

An example of the XML of a multi-instance completion condition is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>10</bpmn2:loopCardinality>
	<bpmn2:completionCondition>${nrOfCompletedInstances/nrOfInstances >= 0.6 }</bpmn2:completionCondition>
</bpmn2:multiInstanceLoopCharacteristics>
```

> **Note**: The completion condition will be met when 60% of instances have been completed and the remaining 4 instances will be cancelled.

An example of the XML of a multi-instance element is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${users}">
	<bpmn2:multiInstanceLoopCharacteristics isSequential="true">
		<bpmn2:loopCardinality>4</bpmn2:loopCardinality>
		<bpmn2:loopDataOutputRef>choices</bpmn2:loopDataOutputRef>
		<bpmn2:outputDataItem name="flavor" />
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The user task will run 4 times sequentially and the values of `flavor` from the form will be stored as a JSON object in the variable `choices`. The process variable `choices` will contain a list of results similar to the following:
>
>```json
>["chocolate", "mint", "strawberry"]
>```

{% endcapture %}

{% include tabs.html tableid="business" opt1="Properties" content1=business-prop opt2="Multi-instance" content2=multi opt3="Appearance" content3=business-img opt4="XML" content4=business-xml %}

### Script task

Script tasks are used to include [scripts]({% link process-automation/latest/model/scripts.md %}) in a process definition.

Script tasks are essentially treated as service tasks and will always have the `implementation` value of `script.EXECUTE`. The `name` of the script that is associated to the script task is used as the `value` under `_activiti_script_` when viewing the **Extensions Editor**.

{% capture script-prop %}

#### Basic properties

The basic properties for a script task are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the script task. This is system generated and cannot be altered, for example `ServiceTask_0a1cgxd`. |
| Name | *Optional.* The name of the script task. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the script task does. |

#### Multi-instance type

Script tasks can be set to repeat sequentially or in parallel when the process flow reaches them.

#### Script name

The name of the [script]({% link process-automation/latest/model/scripts.md %}) to use. The script must exist within the same project as the process definition to be selected. Select a script from the dropdown, else create a new one using the **+** symbol.

#### Mapping type

The mapping type sets how data is passed between the script and the process. There are [five options]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping) for how to send this data. The default value is **Send no variables**.

{% endcapture %}
{% capture script-img %}

Script tasks are displayed as a single thin, rounded rectangle with a script icon inside.

{% endcapture %}
{% capture script-xml %}

An example of the XML of a script task is:

```xml
<bpmn2:serviceTask id="Task_0gpdh83" name="Order script" implementation="script.EXECUTE">
	<bpmn2:documentation>A script to loop and update the list of orders.</bpmn2:documentation>
</bpmn2:serviceTask>
```

An example of the **Extensions Editor** JSON of a process containing a script task is:

```json
    "constants": {
        "Task_0ykbcv0": {
            "_activiti_script_": {
                "value": "order-script"
            }
        }
    }
```

An example of the XML for an element that contains sequential multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics isSequential="true" />
```

An example of the XML for an element that contains parallel multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics  isSequential="false" />
```

or

```xml
<bpmn2:multiInstanceLoopCharacteristics />

```

An example of the XML of multi-instance cardinality is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>5</bpmn2:loopCardinality>
</bpmn2:multiInstanceLoopCharacteristics>
```

An example of the XML of a multi-instance collection is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${user}">
	<bpmn2:incoming>SequenceFlow_5</bpmn2:incoming>
	<bpmn2:multiInstanceLoopCharacteristics activiti:collection="${userList.users}" activiti:elementVariable="user">
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The `activiti:collection` references a process variable called `userList` that contains the following JSON:
>
>```json
>{"users":["user1", "user2", "user3"]}
>```
>
>In the example:
>
>* Three user tasks will be created because there are three items in the process variable that `activiti:collection` uses.
>* A variable will be created for each instance called `users` with the values `user1`, `user2` and `user3` because the `activiti:elementVariable` is set to `"users"`.
>* A user tasks will be assigned to each of the users because the `activiti:assignee` is set to `{users}` which is the name of the variable created in each instance by the element variable.

An example of the XML of a multi-instance completion condition is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>10</bpmn2:loopCardinality>
	<bpmn2:completionCondition>${nrOfCompletedInstances/nrOfInstances >= 0.6 }</bpmn2:completionCondition>
</bpmn2:multiInstanceLoopCharacteristics>
```

> **Note**: The completion condition will be met when 60% of instances have been completed and the remaining 4 instances will be cancelled.

An example of the XML of a multi-instance element is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${users}">
	<bpmn2:multiInstanceLoopCharacteristics isSequential="true">
		<bpmn2:loopCardinality>4</bpmn2:loopCardinality>
		<bpmn2:loopDataOutputRef>choices</bpmn2:loopDataOutputRef>
		<bpmn2:outputDataItem name="flavor" />
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The user task will run 4 times sequentially and the values of `flavor` from the form will be stored as a JSON object in the variable `choices`. The process variable `choices` will contain a list of results similar to the following:
>
>```json
>["chocolate", "mint", "strawberry"]
>```

{% endcapture %}

{% include tabs.html tableid="script" opt1="Properties" content1=script-prop opt2="Multi-instance" content2=multi opt3="Appearance" content3=script-img opt4="XML" content4=script-xml %}

### Service task

Service tasks are used to include [connectors]({% link process-automation/latest/model/connectors/index.md %}), business rule tasks and script tasks in a process.

> **Note**: Service tasks do not emit the `TASK_CREATED` and `TASK_COMPLETED` events. The `INTEGRATION_REQUESTED` and `INTEGRATION_RESULT_RECEIVED` events should be monitored to report or track service tasks instead.

{% capture service-prop %}

#### Basic properties

The basic properties for a service task are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the service task. This is system generated and cannot be altered, for example `ServiceTask_0a1cgxd`. |
| Name | *Optional.* The name of the service task. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the service task does. |

#### Multi-instance type

Script tasks can be set to repeat sequentially or in parallel when the process flow reaches them.

#### Implementation

The implementation value is used to associate a connector with a service task. For business rule tasks and script tasks this value is set by default and cannot be changed. The format is `<connector-name>.<connector-action>`.

#### Action

An action selects which of the connector actions that service task should execute, for example whether to send a message or create a new channel in Slack when using the [Slack connector]({% link process-automation/latest/model/connectors/slack.md %}).

#### Mapping type

The mapping type sets how data is passed between the connector and the process. There are [five options]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping) for how to send this data. The default value is **Send no variables**.

{% endcapture %}
{% capture service-img %}

Service tasks are displayed as a single, thin rounded rectangle with a cog icon inside.

{% endcapture %}
{% capture service-xml %}

An example of the XML of a service task is:

```xml
<bpmn2:serviceTask id="Task_19x7wuh" name="send-email" implementation="email-connector.SEND">
	<bpmn2:documentation>A connector that sends an email.</bpmn2:documentation>
	<bpmn2:incoming>SequenceFlow_19fgs1w</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_64jaw7e</bpmn2:outgoing>
</bpmn2:serviceTask>
```

An example of the XML for an element that contains sequential multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics isSequential="true" />
```

An example of the XML for an element that contains parallel multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics  isSequential="false" />
```

or

```xml
<bpmn2:multiInstanceLoopCharacteristics />

```

An example of the XML of multi-instance cardinality is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>5</bpmn2:loopCardinality>
</bpmn2:multiInstanceLoopCharacteristics>
```

An example of the XML of a multi-instance collection is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${user}">
	<bpmn2:incoming>SequenceFlow_5</bpmn2:incoming>
	<bpmn2:multiInstanceLoopCharacteristics activiti:collection="${userList.users}" activiti:elementVariable="user">
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The `activiti:collection` references a process variable called `userList` that contains the following JSON:
>
>```json
>{"users":["user1", "user2", "user3"]}
>```
>
>In the example:
>
>* Three user tasks will be created because there are three items in the process variable that `activiti:collection` uses.
>* A variable will be created for each instance called `users` with the values `user1`, `user2` and `user3` because the `activiti:elementVariable` is set to `"users"`.
>* A user tasks will be assigned to each of the users because the `activiti:assignee` is set to `{users}` which is the name of the variable created in each instance by the element variable.

An example of the XML of a multi-instance completion condition is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>10</bpmn2:loopCardinality>
	<bpmn2:completionCondition>${nrOfCompletedInstances/nrOfInstances >= 0.6 }</bpmn2:completionCondition>
</bpmn2:multiInstanceLoopCharacteristics>
```

> **Note**: The completion condition will be met when 60% of instances have been completed and the remaining 4 instances will be cancelled.

An example of the XML of a multi-instance element is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${users}">
	<bpmn2:multiInstanceLoopCharacteristics isSequential="true">
		<bpmn2:loopCardinality>4</bpmn2:loopCardinality>
		<bpmn2:loopDataOutputRef>choices</bpmn2:loopDataOutputRef>
		<bpmn2:outputDataItem name="flavor" />
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The user task will run 4 times sequentially and the values of `flavor` from the form will be stored as a JSON object in the variable `choices`. The process variable `choices` will contain a list of results similar to the following:
>
>```json
>["chocolate", "mint", "strawberry"]
>```

{% endcapture %}

{% include tabs.html tableid="service" opt1="Properties" content1=service-prop opt2="Multi-instance" content2=multi opt3="Appearance" content3=service-img opt4="XML" content4=service-xml %}

### User task

User tasks represent a stage in the process where human action is required.

Human action is handled by a task being assigned to specific users or groups. The task that is assigned can be modeled using a [form]({% link process-automation/latest/model/forms.md %}). Once a task is completed, the process flow continues on to the next element in the process. When a new user task is added to a process diagram, it is automatically assigned to the process initiator.

{% capture user-prop %}

#### Basic properties

The basic properties for a user task are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the user task. This is system generated and cannot be altered, for example `UserTask_0w526j8`. |
| Name | *Optional.* The name of the user task. This will be displayed on the canvas. |
| Description | *Optional.* A free text description of what the user task does.<br><br>The description can be made dynamic by writing an expression, for example: `${workflowType} for ${dealNumber} Closing Coordinator Task - Review Document`. In the Digital Workspace and the Admin app, the expression is dynamically rendered as a user-friendly task description. For example, the previous expression might render as: **Commitment and Policy for DEA1235385 Closing Coordinator Task - Review Document**. |

#### Assignment

The users or groups that are able to complete a task. A single user can be assigned or candidates can be set. Candidates are a list of users or groups that may claim a task at runtime. A single user or candidates must be set for a user task.  

A single assignee is set in the XML attribute `activiti:assignee` and candidates in the attribute `activiti:candidateGroups`. On the **Task Assignment** window use the dropdown menu on the top right to set if the assignment is for a single user or for candidates. If for candidates, from the **Assignment type** dropdown list, select either **Sequential** or **Manual** assignment types. Assigning a task manually means a user is assigned the task by another user or themselves. Assigning tasks sequentially means tasks are assigned automatically in a 'round-robin' scenario.

Users and groups can be set from three different sources:

* **Static** values are a free text field that has no validation as to whether a user exists or not. The text entered will require an exact match to a `username` in the product environment for the user task to be correctly assigned at runtime.

* **Identity** allows for [users and groups]({% link process-automation/latest/admin/users.md %}) to be searched for and selected for the assignment. The users and groups must exist whilst modeling to display in this list.

* **Expression** allows for an expression using [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) to be used to select users and groups for the assignment. Expressions can be a simple process variable such as `${userToAssign}` or an expression such as `${userDetails.username}` that uses a process variable of type JSON. A JSON editor is provided for creating expressions for assignment, however the editor will only be displayed if there are process variables in the process.

    > **Note**: The value `"assignee": "${initiator}"` can be set as an expression without creating a process variable. This will assign the task to the user that started the process instance.  

The assignments for user tasks are stored in the `assignments` property of the **Extensions Editor**.

> **Note**: Users and groups that are selected as assignees or candidates in a user task are automatically added as [users]({% link process-automation/latest/admin/release.md %}#deploy-steps/user) when deploying an application if they are set using the static or identity options. Setting an assignee or candidate using the expression source will require the potential users or groups to be manually assigned users when deploying an application.

#### Due date

An optional date and time for a user task to be completed by in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601){:target="_blank"} format. There are three different ways of adding a due date:

* Select **Use static date** then choose the time and date using the date picker.

* Select **Use time duration** then enter a time in Months, Days, Hours, and Minutes.

* Select **Use process variable** then choose a process variable from the dropdown list. This option uses a process variable that must use the type `datetime`.

Checking the **Use process variable** box for due date allows a [process variable]({% link process-automation/latest/model/processes/index.md %}#process-variables) to be used to generate the date. The process variable must be of type `datetime`.

#### Multi-instance type

Script tasks can be set to repeat sequentially or in parallel when the process flow reaches them.

#### Priority

An optional priority for the user task between 0 and 4. The priority property is to aid end users in their task management.  

#### Form name

A [form]({% link process-automation/latest/model/forms.md %}) can be assigned to the user task. The form must exist within the same project as the process definition to be selected. Select a form from the dropdown, else create a new form using the **+** symbol.

Once a form has been selected, it can be edited using the **Open Form** symbol.

#### Mapping type

The mapping type sets how data is passed between the user task and the process. There are [five options]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping) for how to send this data. The default value is **Send no variables**.

{% endcapture %}
{% capture user-img %}

User tasks are displayed as a single thin, rounded rectangle with a user icon inside.

{% endcapture %}
{% capture user-xml %}

An example of the XML of a user task is:

```xml
<bpmn2:userTask id="UserTask_0gpdh83" name="Order" activiti:formKey="form-38098a3e-bff1-46cb-ba0f-0c94fdb287ed" activiti:assignee="${userDetails.username}" activiti:dueDate="2020-01-01T01:00:00" activiti:priority="2">
	<bpmn2:documentation>A form to choose the flavor of ice cream.</bpmn2:documentation>
	<bpmn2:incoming>SequenceFlow_02eaofe</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_14ma5mo</bpmn2:outgoing>
</bpmn2:userTask>
```

An example of the XML for an element that contains sequential multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics isSequential="true" />
```

An example of the XML for an element that contains parallel multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics  isSequential="false" />
```

or

```xml
<bpmn2:multiInstanceLoopCharacteristics />

```

An example of the XML of multi-instance cardinality is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>5</bpmn2:loopCardinality>
</bpmn2:multiInstanceLoopCharacteristics>
```

An example of the XML of a multi-instance collection is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${user}">
	<bpmn2:incoming>SequenceFlow_5</bpmn2:incoming>
	<bpmn2:multiInstanceLoopCharacteristics activiti:collection="${userList.users}" activiti:elementVariable="user">
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The `activiti:collection` references a process variable called `userList` that contains the following JSON:
>
>```json
>{"users":["user1", "user2", "user3"]}
>```
>
>In the example:
>
>* Three user tasks will be created because there are three items in the process variable that `activiti:collection` uses.
>* A variable will be created for each instance called `users` with the values `user1`, `user2` and `user3` because the `activiti:elementVariable` is set to `"users"`.
>* A user tasks will be assigned to each of the users because the `activiti:assignee` is set to `{users}` which is the name of the variable created in each instance by the element variable.

An example of the XML of a multi-instance completion condition is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>10</bpmn2:loopCardinality>
	<bpmn2:completionCondition>${nrOfCompletedInstances/nrOfInstances >= 0.6 }</bpmn2:completionCondition>
</bpmn2:multiInstanceLoopCharacteristics>
```

> **Note**: The completion condition will be met when 60% of instances have been completed and the remaining 4 instances will be cancelled.

An example of the XML of a multi-instance element is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${users}">
	<bpmn2:multiInstanceLoopCharacteristics isSequential="true">
		<bpmn2:loopCardinality>4</bpmn2:loopCardinality>
		<bpmn2:loopDataOutputRef>choices</bpmn2:loopDataOutputRef>
		<bpmn2:outputDataItem name="flavor" />
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The user task will run 4 times sequentially and the values of `flavor` from the form will be stored as a JSON object in the variable `choices`. The process variable `choices` will contain a list of results similar to the following:
>
>```json
>["chocolate", "mint", "strawberry"]
>```

{% endcapture %}

{% include tabs.html tableid="user" opt1="Properties" content1=user-prop opt2="Multi-instance" content2=multi opt3="Appearance" content3=user-img opt4="XML" content4=user-xml %}

## Sub-processes and call activities

Sub-processes and call activities are used to define separate processes. Sub-processes are defined and executed within the same process definition as the parent process, whilst call activities start a completely separate process.

The types of sub-process are:

* [Call activities](#call-activity)
* [Expanded and collapsed sub-processes](#expanded-and-collapsed-sub-processes)
* [Event sub-processes](#event-sub-processes)

### Call activity

Call activities are used to start an instance of another process definition. The original process waits until the called process is complete before continuing with its own process flow.

The `calledElement` property uses a `processDefinitionId` to define which process to start.

> **Note**: When a call activity element is executed it receives its own `processInstanceId`. The [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) of a call activity are also completely separate to those in the parent process.

> **Note**: Call activities can only be used to start a process instance of a process definition that exists in the same application as the process that is calling it.

{% capture call-prop %}

#### Basic properties

The basic properties for a call activity are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the call activity. This is system generated and cannot be altered, for example `CallActivity_1kb3t8n`. |
| Name | *Optional.* The name of the call activity. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the call activity does. |

#### Multi-instance type

Sub-processes can be set to repeat sequentially or in parallel when the process flow reaches them.

#### Called element

The process definition the call activity should start is set using the called element property.

The called element can be set in two ways:

* **Static** values select a process definition name from a dropdown list.

* **Expression** values allow an expression to be set to dynamically call a process definition based on an expression or process variable.

#### Mapping type

The mapping type sets how data is passed between the parent process and the process being started by the call activity. There are [five options]({% link process-automation/latest/model/processes/index.md %}#process-variable-mapping) for how to send this data. The default value is **Send no variables**.

> **Note**: if an **Expression** is used to set which process definition to call in the call element property, it is not possible to explicitly map the variable exchange in the mapping type.

{% endcapture %}
{% capture call-img %}

Call activities are displayed as a single, thick rounded rectangle without an icon inside.

{% endcapture %}
{% capture call-xml %}

An example of the XML of a call activity is:

```xml
<bpmn2:callActivity id="Task_5" name="Start request process" calledElement="process-a6d6ca00-cbb6-45d6-ae24-50ef53d37cc4">
	<bpmn2:incoming>SequenceFlow_8</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_9</bpmn2:outgoing>
</bpmn2:callActivity>
```

An example of the XML for an element that contains sequential multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics isSequential="true" />
```

An example of the XML for an element that contains parallel multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics  isSequential="false" />
```

or

```xml
<bpmn2:multiInstanceLoopCharacteristics />

```

An example of the XML of multi-instance cardinality is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>5</bpmn2:loopCardinality>
</bpmn2:multiInstanceLoopCharacteristics>
```

An example of the XML of a multi-instance collection is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${user}">
	<bpmn2:incoming>SequenceFlow_5</bpmn2:incoming>
	<bpmn2:multiInstanceLoopCharacteristics activiti:collection="${userList.users}" activiti:elementVariable="user">
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The `activiti:collection` references a process variable called `userList` that contains the following JSON:
>
>```json
>{"users":["user1", "user2", "user3"]}
>```
>
>In the example:
>
>* Three user tasks will be created because there are three items in the process variable that `activiti:collection` uses.
>* A variable will be created for each instance called `users` with the values `user1`, `user2` and `user3` because the `activiti:elementVariable` is set to `"users"`.
>* A user tasks will be assigned to each of the users because the `activiti:assignee` is set to `{users}` which is the name of the variable created in each instance by the element variable.

An example of the XML of a multi-instance completion condition is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>10</bpmn2:loopCardinality>
	<bpmn2:completionCondition>${nrOfCompletedInstances/nrOfInstances >= 0.6 }</bpmn2:completionCondition>
</bpmn2:multiInstanceLoopCharacteristics>
```

> **Note**: The completion condition will be met when 60% of instances have been completed and the remaining 4 instances will be cancelled.

An example of the XML of a multi-instance element is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${users}">
	<bpmn2:multiInstanceLoopCharacteristics isSequential="true">
		<bpmn2:loopCardinality>4</bpmn2:loopCardinality>
		<bpmn2:loopDataOutputRef>choices</bpmn2:loopDataOutputRef>
		<bpmn2:outputDataItem name="flavor" />
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The user task will run 4 times sequentially and the values of `flavor` from the form will be stored as a JSON object in the variable `choices`. The process variable `choices` will contain a list of results similar to the following:
>
>```json
>["chocolate", "mint", "strawberry"]
>```

{% endcapture %}

{% include tabs.html tableid="call" opt1="Properties" content1=call-prop opt2="Multi-instance" content2=multi opt3="Appearance" content3=call-img opt4="XML" content4=call-xml %}

### Expanded and collapsed sub-processes

Sub-processes are also known as embedded sub-processes and can be expanded or collapsed. Elements for the sub-process can only be dragged into an expanded sub-process. Use the spanner icon against a sub-process to toggle between a collapsed and expanded state.

A sub-process requires a start and an end event. Only a [standard start event](#start-event) can be used in embedded sub-processes. The sequence flow within a sub-process cannot cross its boundary without the sub-process completing. The advantage of a sub-process is that it creates its own scope within a process. This allows for boundary events to be attached to the sub-process.

> **Note**: When a sub-process is executed as part of a process instance, it does not receive a new `processInstanceId`. The elements within the sub-process will be executed under the ID of the parent process. [Process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) are also shared between a sub-process and its parent with no additional mapping required.

{% capture sub-prop %}

#### Basic properties

The basic properties for a sub-process are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the sub-process. This is system generated and cannot be altered, for example `CallActivity_1kb3t8n`. |
| Name | *Optional.* The name of the sub-process. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the sub-process does. |

#### Multi-instance type

Sub-processes can be set to repeat sequentially or in parallel when the process flow reaches them.

{% endcapture %}
{% capture sub-img %}

Whilst expanded, sub-processes are displayed as a single, thin rounded rectangle with the other BPMN elements they contain visible.

Whilst collapsed, sub-processes are displayed as a single, thin rounded rectangle with a `+` symbol. The BPMN elements they contain are not visible in this state.

{% endcapture %}
{% capture sub-xml %}

An example of the XML of a sub-process is:

```xml
<bpmn2:subProcess id="SubProcess1">
	<bpmn2:incoming>SequenceFlow_8</bpmn2:incoming>
	<bpmn2:outgoing>SequenceFlow_9</bpmn2:outgoing>
	...
</bpmn2:subProcess>
```

An example of the XML for an element that contains sequential multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics isSequential="true" />
```

An example of the XML for an element that contains parallel multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics  isSequential="false" />
```

or

```xml
<bpmn2:multiInstanceLoopCharacteristics />

```

An example of the XML of multi-instance cardinality is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>5</bpmn2:loopCardinality>
</bpmn2:multiInstanceLoopCharacteristics>
```

An example of the XML of a multi-instance collection is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${user}">
	<bpmn2:incoming>SequenceFlow_5</bpmn2:incoming>
	<bpmn2:multiInstanceLoopCharacteristics activiti:collection="${userList.users}" activiti:elementVariable="user">
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The `activiti:collection` references a process variable called `userList` that contains the following JSON:
>
>```json
>{"users":["user1", "user2", "user3"]}
>```
>
>In the example:
>
>* Three user tasks will be created because there are three items in the process variable that `activiti:collection` uses.
>* A variable will be created for each instance called `users` with the values `user1`, `user2` and `user3` because the `activiti:elementVariable` is set to `"users"`.
>* A user tasks will be assigned to each of the users because the `activiti:assignee` is set to `{users}` which is the name of the variable created in each instance by the element variable.

An example of the XML of a multi-instance completion condition is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>10</bpmn2:loopCardinality>
	<bpmn2:completionCondition>${nrOfCompletedInstances/nrOfInstances >= 0.6 }</bpmn2:completionCondition>
</bpmn2:multiInstanceLoopCharacteristics>
```

> **Note**: The completion condition will be met when 60% of instances have been completed and the remaining 4 instances will be cancelled.

An example of the XML of a multi-instance element is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${users}">
	<bpmn2:multiInstanceLoopCharacteristics isSequential="true">
		<bpmn2:loopCardinality>4</bpmn2:loopCardinality>
		<bpmn2:loopDataOutputRef>choices</bpmn2:loopDataOutputRef>
		<bpmn2:outputDataItem name="flavor" />
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The user task will run 4 times sequentially and the values of `flavor` from the form will be stored as a JSON object in the variable `choices`. The process variable `choices` will contain a list of results similar to the following:
>
>```json
>["chocolate", "mint", "strawberry"]
>```

{% endcapture %}

{% include tabs.html tableid="sub" opt1="Properties" content1=sub-prop opt2="Multi-instance" content2=multi opt3="Appearance" content3=sub-img opt4="XML" content4=sub-xml %}

### Event sub-processes

Event sub-processes are triggered by an event such as a signal or error and require a start and end event. As they are triggered by events an event sub-process can't be started by a standard start event. Instead start events such as error start events or message start events are used.

Event sub-processes are not connected to the main process flow as they can only be triggered by an event. The XML for an event sub-process contains the `triggeredByEvent` property set to `true`.  

Event sub-processes can be placed at the process level or inside a sub-process.

> **Note**: When an event sub-process is executed as part of a process instance, it does not receive a new `processInstanceId`. The elements within the event sub-process will be executed under the ID of the parent process. [Process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) are also shared between an event sub-process and its parent with no additional mapping required.

{% capture event-prop %}

#### Basic properties

The basic properties for an event sub-process are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the event sub-process. This is system generated and cannot be altered, for example `CallActivity_1kb3t8n`. |
| Name | *Optional.* The name of the event sub-process. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the event sub-process does. |

#### Multi-instance type

Sub-processes can be set to repeat sequentially or in parallel when the process flow reaches them.

{% endcapture %}
{% capture event-img %}

Event sub-processes are displayed as a single, thin dotted rectangle.

{% endcapture %}
{% capture event-xml %}

An example of the XML of an event sub-process is:

```xml
<bpmn2:subProcess id="EventSubProcess2" triggeredByEvent="true">
	...
</bpmn2:subProcess>
```

An example of the XML for an element that contains sequential multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics isSequential="true" />
```

An example of the XML for an element that contains parallel multi-instance elements is:

```xml
<bpmn2:multiInstanceLoopCharacteristics  isSequential="false" />
```

or

```xml
<bpmn2:multiInstanceLoopCharacteristics />

```

An example of the XML of multi-instance cardinality is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>5</bpmn2:loopCardinality>
</bpmn2:multiInstanceLoopCharacteristics>
```

An example of the XML of a multi-instance collection is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${user}">
	<bpmn2:incoming>SequenceFlow_5</bpmn2:incoming>
	<bpmn2:multiInstanceLoopCharacteristics activiti:collection="${userList.users}" activiti:elementVariable="user">
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The `activiti:collection` references a process variable called `userList` that contains the following JSON:
>
>```json
>{"users":["user1", "user2", "user3"]}
>```
>
>In the example:
>
>* Three user tasks will be created because there are three items in the process variable that `activiti:collection` uses.
>* A variable will be created for each instance called `users` with the values `user1`, `user2` and `user3` because the `activiti:elementVariable` is set to `"users"`.
>* A user tasks will be assigned to each of the users because the `activiti:assignee` is set to `{users}` which is the name of the variable created in each instance by the element variable.

An example of the XML of a multi-instance completion condition is:

```xml
<bpmn2:multiInstanceLoopCharacteristics>
	<bpmn2:loopCardinality>10</bpmn2:loopCardinality>
	<bpmn2:completionCondition>${nrOfCompletedInstances/nrOfInstances >= 0.6 }</bpmn2:completionCondition>
</bpmn2:multiInstanceLoopCharacteristics>
```

> **Note**: The completion condition will be met when 60% of instances have been completed and the remaining 4 instances will be cancelled.

An example of the XML of a multi-instance element is:

```xml
<bpmn2:userTask id="UserTask_1n1uk4a" activiti:assignee="${users}">
	<bpmn2:multiInstanceLoopCharacteristics isSequential="true">
		<bpmn2:loopCardinality>4</bpmn2:loopCardinality>
		<bpmn2:loopDataOutputRef>choices</bpmn2:loopDataOutputRef>
		<bpmn2:outputDataItem name="flavor" />
	</bpmn2:multiInstanceLoopCharacteristics>
</bpmn2:userTask>
```

> **Note**: The user task will run 4 times sequentially and the values of `flavor` from the form will be stored as a JSON object in the variable `choices`. The process variable `choices` will contain a list of results similar to the following:
>
>```json
>["chocolate", "mint", "strawberry"]
>```

{% endcapture %}

{% include tabs.html tableid="event" opt1="Properties" content1=event-prop opt2="Multi-instance" content2=multi opt3="Appearance" content3=event-img opt4="XML" content4=event-xml %}

## Sequence flows, pools and lanes

Sequence flows represent the direction of flow in a process, whilst pools and lanes are used to model different participants, personas and process definitions in the same diagram.

### Sequence flow

Sequence flows represent the direction of flow in a process. The can be drawn between BPMN elements using the **Global connect tool**.

{% capture sequence-prop %}

#### Basic properties

The basic properties for a sequence flow are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the sequence flow. This is system generated and cannot be altered, for example `SequenceFlow_1y8xkql`. |
| Name | *Optional.* The name of the sequence flow. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the sequence flow does. |

#### Condition expression

A condition expression can be set when a sequence flow is connected to an inclusive or exclusive gateway. Conditions will be evaluated to decide whether a path is taken or not. The expression syntax can reference process variables using expressions such as `${content.approved} == false}` where that path will be taken if the `approved` attribute of the variable `content` is set to `false`.

Another example of conditional expressions when evaluating a sequence flow is using amounts, for example `${amount>500}` will take the sequence flow if the process variable `amount` is greater than 500 at the point the gateway is reached.

{% endcapture %}
{% capture sequence-img %}

Sequence flows are displayed as single black lines with an arrow indicating the direction of flow.

{% endcapture %}
{% capture sequence-xml %}

An example of the XML of a sequence flow is:

```xml
<bpmn2:incoming>SequenceFlow_1</bpmn2:incoming>
<bpmn2:outgoing>SequenceFlow_2</bpmn2:outgoing>
```

An example of the XML of a sequence flow with a condition expression set is:

```xml
<bpmn2:sequenceFlow id="SequenceFlow_1" name="no" sourceRef="ExclusiveGateway_1" targetRef="Task_1">
	<bpmn2conditionExpression xsi:type="bpmn:tFormalExpression">${content.approved == false}</bpmn2:conditionExpression>
</bpmn2:sequenceFlow>
```

{% endcapture %}

{% include tabs.html tableid="sequence" opt1="Properties" content1=sequence-prop opt2="Appearance" content2=sequence-img opt3="XML" content3=sequence-xml %}

### Pools and lanes

Pools allow multiple process definitions to be modeled in a single diagram, or to utilize lanes to show the personas interacting with a process defintion. An example of using two pools would be for a customer to fill out an order in one process definition that sends a message on order completion triggering a second process defintion for a warehouse team to action. The two processes would have two completely different process instance IDs at runtime but can be modeled on the same diagram to capture the business process in a single location.

Lanes are used to display different personas interacting with a process definition to the modeler. They have no impact on a process at runtime. Lanes are sub-divisions of pools and cannot exist without them. They can also be nested for example to show different teams within a department.

> **Important**: The scope of [process variables]({% link process-automation/latest/model/processes/index.md %}#process-variables) are restricted to each process definition.

{% capture pool-prop %}

#### Basic properties

The basic properties for a pool are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the pool. This is system generated and cannot be altered, for example `Participant_0efla7f`. |
| Documentation | *Optional.* A free text description of what the pool does. |

> **Note**: Pools use the process definition name rather than having an additional name property.

{% endcapture %}
{% capture lane-prop %}

#### Basic properties

The basic properties for a lane are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for the lane. This is system generated and cannot be altered, for example `Lane_1ikh7j5`. |
| Name | *Optional.* The name of the lane. This will be displayed on the canvas. |
| Documentation | *Optional.* A free text description of what the lane does. |

{% endcapture %}
{% capture pool-xml %}

An example of the XML of a pool is:

```xml
<bpmn2:collaboration id="Collaboration_0kgbwi1">
	<bpmn2:participant id="Participant_1i6u1my" processRef="Process_1d9yxsm" />
	<bpmn2:participant id="Participant_10umhbc" processRef="Process_1piiyp4" />
</bpmn2:collaboration>
```

An example of the XML of a lane is:

```xml
<bpmn2:process id="Process_1d9yxsm">
	<bpmn2:laneSet id="LaneSet_1b8nhx7">
		<bpmn2:lane id="Lane_104t61m" name="HR Department">
			<bpmn2:flowNodeRef>Event_0b61hqt</bpmn2:flowNodeRef>
			<bpmn2:flowNodeRef>Gateway_1dmrhcn</bpmn2:flowNodeRef>
		</bpmn2:lane>
		<bpmn2:lane id="Lane_1i3x8rz" name="Finance Department">
			<bpmn2:flowNodeRef>Task_16ju082</bpmn2:flowNodeRef>
			<bpmn2:flowNodeRef>Event_00acemq</bpmn2:flowNodeRef>
		</bpmn2:lane>
</bpmn2:laneSet>
```

{% endcapture %}

{% include tabs.html tableid="pools" opt1="Pools" content1=pool-prop opt2="Lanes" content2=lane-prop opt3="XML" content3=pool-xml %}
---
title: Engine events
---

Engine events are events generated as part of the life cycle of processes. They include events such as when BPMN activity is started, saved, submitted or completed. They can be used as [trigger events]({% link process-automation/latest/model/triggers.md %}) and for [audit]({% link process-automation/latest/admin/monitor.md %}#audit) purposes.

## Properties

All engine events have a common set of properties describing the service they are using and a common set of properties describing the event.

The service properties are:

| Name | Description |
| ---- | ----------- |
|  appName  | The name of the application, for example `finance-application`. |
|  appVersion  | The version number of the application, for example `3`.  |
|  serviceName  | The name of the service in the application, for example `rb-finance-application`.  |
|  serviceFullName  | The full name of the service in the application. This is the same as `serviceName`. |
|  serviceType  | The type of service, for example `runtime-bundle`.  |
|  serviceVersion  | The version of the service. |
|  messageId  | The ID of the message that carried the event. All events that are part of the same transaction are aggregated into the same message. |
|  sequenceNumber  | The sequence index of an event within a message. |
|  entityId  | The ID of an entity included in a message. |

The event properties are:

| Name | Description |
|------|-------------|
| id | The event ID. |
| entity | The entity included in the message. |
| timestamp | The timestamp of the event. |
| eventType | The type of event. |
| processInstanceId | The process instance ID. |
| parentProcessInstanceId | The parent process instance ID if one exists. |
| processDefinitionId | The process definition ID. |
| processDefinitionKey | The process definition key. |
| processDefinitionVersion | The version of the process definition. |
| businessKey | The business key associated to the process instance if one exists. |

## Event Types

| Event | Description |
| ----- | ----------- |
| ACTIVITY_STARTED | An activity is starting to execute. This event is sent just before an activity is executed. |
| ACTIVITY_CANCELLED | An activity has been cancelled. |
| ACTIVITY_COMPLETED | An activity has been completed. |
| ERROR_RECEIVED | An activity has received an error event. |
| SIGNAL_RECEIVED | An activity has received a signal. |
| TIMER_FIRED | A timer has been fired. It will be followed by either a `TIMER_EXECUTED` or `TIMER_FAILED` event. |
| TIMER_CANCELLED | A timer has been cancelled, for example if a task was completed before the timer expired. |
| TIMER_SCHEDULED | A timer has been scheduled. |
| TIMER_EXECUTED | A timer has executed. |
| TIMER_FAILED | A timer failed to fire. |
| TIMER_RETRIES_DECREMENTED | The retry count for a timer has been decreased. |
| MESSAGE_WAITING | A message catch event is waiting to receive a message. |
| MESSAGE_RECEIVED | An activity received a message. |
| MESSAGE_SENT | A message throw event has sent a message. |
| INTEGRATION_REQUESTED | The application runtime bundle has sent a request to a connector. |
| INTEGRATION_RESULT_RECEIVED | The application runtime bundle has received a result from a connector. |
| PROCESS_DEPLOYED | A new process definition is available. These events are sent when the application runtime bundle first starts and on any restarts. |
| PROCESS_CREATED | A process instance has been created. |
| PROCESS_STARTED | A process instance has been started. |
| PROCESS_COMPLETED | A process instance has been completed. This event is sent after the final `ACTIVITY_COMPLETED` event is sent. |
| PROCESS_CANCELLED | A process instance has been cancelled. |
| PROCESS_SUSPENDED | A process instance has been suspended. |
| PROCESS_RESUMED | A previously suspended process instance has been resumed. |
| PROCESS_UPDATED | A process instance has been updated. |
| SEQUENCE_FLOW_TAKEN | A sequence flow between two activities has been taken. |
| START_MESSAGE_DEPLOYED | A start message event is waiting to catch a message. Similar to `MESSAGE_WAITING` but specific to start message events. |
| MESSAGE_SUBSCRIPTION_CANCELLED | A message event subscription entity has been deleted. For example, if a process instance is deleted that had an active catch message event activity. |
| TASK_CREATED | A task has been created. Note that [service tasks]({% link process-automation/latest/model/processes/bpmn.md %}#service-task) do not emit a `TASK_CREATED` event. The `INTEGRATION_REQUESTED` event should be monitored to report or track service tasks. |
| TASK_UPDATED | A task has been updated. |
| TASK_ASSIGNED | A task has been assigned. |
| TASK_COMPLETED | A task has been completed. Note that [service tasks]({% link process-automation/latest/model/processes/bpmn.md %}#service-task) do not emit a `TASK_COMPLETED` event. The `INTEGRATION_RESULT_RECEIVED` event should be monitored to report or track service tasks. |
| TASK_SUSPENDED | A task has been suspended. |
| TASK_ACTIVATED | A previously suspended task has been reactivated. |
| TASK_CANCELLED | A task has been cancelled. |
| TASK_CANDIDATE_USER_ADDED | A user has been added to the list of candidates for a task. |
| TASK_CANDIDATE_USER_REMOVED | A user has been removed from the list of candidates for a task. |
| TASK_CANDIDATE_GROUP_ADDED | A group has been added to the list of candidates for a task. |
| TASK_CANDIDATE_GROUP_REMOVED | A group has been removed from the list of candidates for a task. |
| VARIABLE_CREATED | A variable has been created. |
| VARIABLE_UPDATED | A variable has been updated. |
| VARIABLE_DELETED | A variable has been deleted. |
---
title: Overview of processes
---

Processes are the collection of components that are used to build and represent business processes using [BPMN 2.0 specification](https://www.omg.org/spec/BPMN/2.0/){:target="_blank"}.

There are three concepts associated with modeling processes to understand and differentiate between:

* **Diagrams** are the container that process definitions are modeled in. A process diagram can contain multiple process definitions when [pools]({% link process-automation/latest/model/processes/bpmn.md %}#pools-and-lanes) are used to separate them. Process diagrams are color coded with the following definitions:

  * Blue indicates completed nodes
  * Green indicates current active nodes
  * Red indicates failed nodes

* **Process definitions** are the templates that a process follows, made up of BPMN elements and sequence flows. A process definition describes the business logic that will be followed repeatedly at runtime.

* **Process instances** are specific running instances of a process definition. Each process instance will have a unique process instance ID but they can share the same process definition ID indicating which process definition was used to start the process instance. There can be any number of process instances running using the same process definition in an N:1 relationship.

## Create a process

To create a process:

1. Sign into the Modeling Application and open a project.

2. Click the **NEW** dropdown.

3. Select how to create the process:

    * **Create > Process** creates a new, empty diagram and process definition.

    * **Upload > Process** allows for uploading an existing diagram `.bpmn20.xml` file into the Modeling Application.

    Alternatively use the **+** or **Upload** buttons next to **Processes** in the left-hand menu.

4. Enter a name, optional description, and optional process category.

	By default the name will be shared between the diagram and process definition and the description will apply to the process definition. If you enter a process category the process will be added under the process category heading in the left pane, and if the process category does not already exist it will be created. If you do not enter a process category name it will appear under the uncategorized heading.

### Import a process from Process Services

Process diagrams exported from [Alfresco Process Services]({% link process-services/latest/index.md %}) can be imported into the Modeling Application by selecting the **APS Process** option when choosing to [create a new process](#create-a-process) by importing an existing model.

The Process Service element types that are supported for import are:

| Process Services type | Process Automation type | Notes |
| --------------------- | ----------------------- | ----- |
| Script task | [Script task]({% link process-automation/latest/model/processes/bpmn.md %}#script-task) | A script and a script task will be created for each script. {::nomarkdown}<ul><li>Only Javascript is supported.</li><li>Multi-instance is not supported.</li><li>Execution listeners removed.</li><li> Asynchronous option removed.</li><li>Exclusive option removed.</li><li>Is for compensation option removed.</li><li>A script task is created as a service task in Process Automation.</ul>{:/} |
| User task | [User task]({% link process-automation/latest/model/processes/bpmn.md %}#user-task) | A user task will be created for each user task. {::nomarkdown}<ul><li>Forms are not supported.</li><li>Date format is a fixed date.</li><li>Due date is not supported.</li><li><code>Initiator</code> is set as the assignee in Process Automation.</li><li>Category option removed.</li><li>Exclusive option removed.</li><li>Allow email notifications option removed.</li><li>Email template option removed.</li><li>Task and execution listeners removed.</li><li>Asynchronous option removed.</li></ul>{:/} |
| Mail task | [Email service]({% link process-automation/latest/model/connectors/email.md %}) | An instance of the email service is created and an email service task is created for each mail task. {::nomarkdown}<ul><li>A single email service instance is created for all mail tasks that are imported.</li><li>Some connector parameters are imported from Process Services, whilst others need to be set.</li><li>All parameters will need to be mapped between process variables.</li><li>Connector needs to be configured.</li><li>Multi-instance is not supported.</li><li>Execution listeners removed.</li><li> Asynchronous option removed.</li><li>Exclusive option removed.</li><li>Is for compensation option removed.</li><li>Any JSON templates will not be imported.</li></ul>{:/} |
| REST call task | [REST connector]({% link process-automation/latest/model/connectors/rest.md %}) | An instance of the REST connector is created and a REST connector task is created for each REST call task. {::nomarkdown}<ul><li>A single REST connector instance is created for all REST call tasks that are imported.</li><li>Some connector parameters are imported from Process Services, whilst others need to be set.</li><li>All parameters will need to be mapped between process variables.</li><li>Connector needs to be configured.</li><li>Multi-instance is not supported.</li><li>Execution listeners removed.</li><li> Asynchronous option removed.</li><li>Exclusive option removed.</li><li>Is for compensation option removed.</li></ul>{:/} |

## Diagrams

Diagrams hold one or more process definitions. If multiple process definitions are modeled within a diagram it is important to remember that the scope of each is restricted and the only way to communicate between them is via [message](#message) or [error](#error) events.

### Diagram properties

The properties for a diagram are:

| Property | Description |
| -------- | ----------- |
| ID | *Required.* The unique identifier for a diagram. This is system generated and cannot be altered, for example `model-1bf32338-2bc2-4af2-9496-e9a031e22142` |
| Diagram name | *Required.* The name of the diagram. Diagram names must be in lowercase and between 1 and 26 characters in length. Alphanumeric characters and hyphens are allowed, however the name must begin with a letter and end alphanumerically, for example `requests-and-orders`. |

### Diagram XML

The ID and name of a diagram are set as XML attributes of the `definitions` element, for example:

```xml
<bpmn2:definitions id="model-1bf32338-2bc2-4af2-9496-e9a031e22142" name="requests-and-orders">
```

## Process definitions

Process definitions are designed using [BPMN elements]({% link process-automation/latest/model/processes/bpmn.md %}) which in turn can reference other modeled components within a project such as forms, connectors and decision tables.

A process definition is created when a diagram is created and it will share the same name as the diagram. Use the BPMN element [pools]({% link process-automation/latest/model/processes/bpmn.md %}#pools-and-lanes) to create separate process definitions within a diagram.

### Process definition properties

The properties for a process definition are:

| Property | Description |
| -------- | ----------- |
| Process ID | *Required.* The unique identifier for a process definition. This is system generated and cannot be altered, for example `Process_1w18m9x`. |
| Process definition name | *Required.* The name of the process definition. Process definition names must be between 1 and 26 characters in length, they can also contain spaces, numbers, and consist of lower and upper case letters, for example `Request Process`. |
| Executable | *Required.* If set as `false` then the process definition will be deployed at runtime but it will not be possible to create any process instances using it. The default value is `true`. |
| Documentation | *Optional.* A free text description of what the process definition does, for example `A process to request stock orders`. |
| Process Category | *Optional.* Enter a free text description of your process categories. When creating a process you can either create a new process category or select one you have already created that appears in the dropdown list. When you use the **Diagram Editor** you can see the process category a process is assigned to under the Category property heading.  |

### Process definition XML

The ID, name and executable status of a process definition are set as XML attributes of the `process` element. Documentation is a sub-element of `process`, for example:

```xml
<bpmn2:process id="Process_1w18m9x" name="request-process" isExecutable="false">
        <bpmn2:documentation>A process to request stock orders</bpmn2:documentation>
```

## Process modeling

The Modeling Application contains three tabs for creating and editing processes.

### Diagram Editor

The **Diagram Editor** is the GUI for modeling processes by dragging and dropping items from the palette. The palette contains the [BPMN elements]({% link process-automation/latest/model/processes/bpmn.md %}) that can be used to model a process and import other models created in the Modeling Application into a process. The palette also contains four tools for editing items on the canvas:

| Tool | Description |
| ---- | ----------- |
| Hand | Use the hand tool to pan around the diagram and select elements to view their properties. |
| Global connect | Use the global connect tool to draw [sequence flows]({% link process-automation/latest/model/processes/bpmn.md %}#sequence-flow) between elements on the diagram. |
| Create/remove space | Use the create/remove space tool to move elements around the diagram. |
| Lasso | Use the lasso tool to drag a box and select multiple elements on the diagram. |

### XML Editor

The **XML Editor** contains the XML for the process diagram. Changes made in the **Diagram Editor** or in the **XML Editor** are reflected in the other. When importing or downloading a process the `.bpmn20.xml` file will reflect what is in the **XML Editor**.

XML excerpts are provided as examples with each [BPMN element]({% link process-automation/latest/model/processes/bpmn.md %}).

### Extensions Editor

The **Extensions Editor** is a JSON editor that stores any extensions made for process definitions. When a diagram contains more than one process definition, there will be an entry for each in the **Extensions Editor**. Extensions are broken down into four areas:

| Extension type | Description |
| -------------- | ----------- |
| constants | Constants are values that will not change for the duration of a process such as the service task implementation of a decision table. |
| mappings | Mappings are the record of how variables are passed between the process and other models and BPMN elements such as user tasks, decision tables and scripts.  |
| properties | Properties store the details of process variables. |
| assignments | Assignments store the user and group assignations for [user tasks]({% link process-automation/latest/model/processes/bpmn.md %}#user-task). |

## Process variables

Process variables are used to store values and pass them between BPMN elements throughout a process instance. For example, values entered into a form as part of a user task can be sent to process variables in the process, which in turn can send those values to a decision table to evaluate and choose the direction the process should take.

The scope of process variables is restricted to a process definition and not to the diagram it is created in, which is important to consider when using multiple [pools]({% link process-automation/latest/model/processes/bpmn.md %}#pools-and-lanes).

### Process variable properties

The properties for a process variable are:  

| Property | Description |
| -------- | ----------- |
| name | A unique name that can contain alphanumeric characters and underscores but must begin with a letter, for example `var_3` |
| type | A data type selected from a dropdown. See the following table for a list of data types, for example `String` |
| required | Sets whether the process variable must contain a value when a process instance is started, for example `false` |
| value | An optional default value for the process variable, for example `ice-cream` |

> **Note**: There are four process variable names that are created automatically and should not be used as custom process variable names. `nrOfInstances`, `nrOfActiveInstances`, `nrOfCompletedInstances` and `loopCounter` are used by [multi-instance elements]({% link process-automation/latest/model/processes/bpmn.md %}).

The data types that a process variable can be set as are:

| Type | Description |
| ---- | ----------- |
| String | A sequence of characters, for example `#Mint-Ice-Cream-4!`. |
| Integer | A positive whole number, for example `642`. |
| Boolean | A value of either `true` or `false`. |
| Date | A specific date in the format `YYYY-MM-DD`, for example `2020-04-22`. You can also select `Today` from the Value column, which will take the form `${now()}` in the Expression column. |
| Datetime | A specific date and time in the format `YYYY-MM-DD HH:mm:ss`, for example `2020-09-10 22:30:00`. |
| File | A [file]({% link process-automation/latest/model/files.md %}) uploaded into a process definition or as part of a process instance or task. |
| JSON | A JSON object, for example `{"flavor" : "caramel"}`. |
| Folder | A folder object described as JSON, for example `"name": "mint-folder"`. |
| Array | A comma separated list of entries, for example `mint, strawberry, vanilla` that will be formatted to `["mint","strawberry","vanilla"]`. |

### Create a process variable

To create a process variable:

1. Select the project and process to create a process variable for in the Modeling Application.

2. Select **Edit Process Variables** against the correct process definition:

    * If the diagram contains only one process definition, make sure no BPMN element is selected by clicking on a blank section of the canvas and the **Edit Process Variables** button will be visible in the right-hand properties panel.
    * If the diagram contains more than one process definition then click on the individual [pools]({% link process-automation/latest/model/processes/bpmn.md %}#pools-and-lanes) to view the **Edit Process Variables** button for each definition.

3. Use the **+** symbol to add new variables and enter a name, type, optional value, and select whether it is required or not.

	If you want the variable to be available in the Processes, and Tasks lists of the Digital Workspace click **Yes** below **Available in the web application**, and enter a display name. Once added to the Digital workspace you can select the new column by accessing the three dots on the top right.

	 ![Process variable digital workspace]({% link process-automation/images/process-variable-digital.png %})

> **Note**: The details of any process variables can be viewed in the properties section of the [extensions editor](#extensions-editor), for example:

```json
{
    "properties": {
        "17aa41f7-9a0c-49c0-805b-045243f8a7e5": {
            "id": "17aa41f7-9a0c-49c0-805b-045243f8a7e5",
            "name": "firstName",
            "type": "string",
            "required": false,
        },
```

### Process variable mapping

**Mapping** is a property of BPMN elements such as [user tasks]({% link process-automation/latest/model/processes/bpmn.md %}#user-task), [service tasks]({% link process-automation/latest/model/processes/bpmn.md %}#service-task) and [script tasks]({% link process-automation/latest/model/processes/bpmn.md %}#script-task). It describes how data should be passed between a process and models such as forms, connectors, and scripts in a process. The data can be passed to variables within those models, such as form variables and script variables or other values in the model such as form fields, connector inputs and outputs and decision table inputs and outputs. Mapping this data is split between input mappings and output mappings:

* Input mapping sets how and which data is sent from process variables to another model within the process.

* Output mapping sets how and which data is sent from models within the process back to process variables.

There are five options for setting the **Mapping** behavior:

{% capture none %}

**Don't map variables** is the default behavior.

When variables are not mapped, there is no transfer of data between process variables and other models within the process.

For example, if **Don't map variables** is selected for a user task in a process then none of the form fields will be populated with values from earlier within the process instance. Similarly, when the form is completed none of the values entered by the user can be reused later in the process, such as within a decision table.

{% endcapture %}
{% capture map %}

**Map variables** allows each input and output to be explicitly mapped between process variables and the values or variables within another model.

If **Map variables** is selected as the **Mapping** type, there are three ways of mapping variables that can be chosen by selecting the edit icon next to any input or output parameters:

* **Process Variables** are regular process variables that must match the type of the source or target parameter. For example an input parameter of type `string` cannot map to a process variable of type `file`.

* **Expressions**: Expressions can be entered using a JSON editor to create more complex mappings such as mapping JSON process variables to input and output parameters. For example, using `${temperature.celsius}` will use the value for the object `celsius`.

	In the following example this would result in a value of `16`:

	```json
	{
  	"day": "Monday",
  	"temperature": {
    	"celsius": 16,
    	"fahrenheit": 66
  		}
	}
	```

* Static **Values** can be entered rather than using process variables.

An example of using the **Map variables** option is a decision table that contains the input `Price` and the output `Decision` and the process contains the process variables `Total` and `customerResponse` the mapping can be configured like the following:

![Map variables example image]({% link process-automation/images/map-variables.png %}){:height="300px" width="190px"}

At runtime, the value for the process variable `Total` will be sent as the input to the decision table when that point in the process instance is reached. Once the decision table has evaluated the input, the value of the output `Decision` will be sent back to the process variable `customerResponse` which can then be used later in the process, such as in sending an email to a customer.

{% endcapture %}
{% capture inputs %}

**Map all input variables** will automatically map the values of process variables to values or variables within a model if their names are identical. Outputs are not mapped at all, so there will be no transfer of data from the model, back to process variables.

For example, if **Map all input variables** is selected for an instance of the email service, process variables named `to`, `subject` and `text` can be used to automatically set the values for the recipient, subject and message in the connector. No output variables are required to be sent back to the process as the execution of the email service is always treated as successful.

{% endcapture %}
{% capture outputs %}

**Map all output variables** will automatically map values or variables from a model to process variables in the process if their names are identical. If there is no process variable with a matching name to one of the outputs of the model it will be created when the model is executed using the name of the output value or variable. Inputs are not mapped at all, so there will be no initial transfer of data from process variables to the other model.

For example, if **Map all output variables** is selected for a start event that contains a form, the data entered to start the process can be used further in the process by mapping the values from fields within the form to process variables in the process. Process variables can be created during modeling time that use the same name as form fields, or alternatively they will be created automatically once the user task is completed at runtime.

{% endcapture %}
{% capture all %}

**Map all variables** will automatically map the values of process variables to values or variables within a model if their names are identical. It will also map values or variables from a model to the process variables in the process if their names are idenitcal. Additionally, for output variables only, if there is no process variable with a matching name to one of the outputs of the model it will be created when the model is executed using the name of the output value or variable.

For example, if **Map all variables** is selected for a user task that contains an `orderStatus` field on the form, a process variable with the name `orderStatus` can be used to set the status of an order automatically when the user task is started. Before the task is completed, a user can update the `orderStatus` field on the form and it will update the same process variable when the task is finished with the new status. Additionally, all the other form fields will be created as process variables when the task is completed.

{% endcapture %}

{% include tabs.html tableid="mapping" opt1="Don't map variables" content1=none opt2="Map variables" content2=map opt3="Map input variables" content3=inputs opt4="Map output variables" content4=outputs opt5="Map all variables" content5=all %}

Any mapping configured in a process is stored in the **Extensions Editor** using the ID of the BPMN element. If not sending any variables then the ID of the element will not appear in the mappings section. The following is an example of explicitly mapping variables:

```json
"mappings": {
    "Task_1f1wpht": {
    	"inputs": {
    		"flavor": {
    			"type": "variable",
    			"value": "choice"
    			},
    		"price": {
    			"type": "value",
    			"value": "${lookUp.price}"
    			},
    		"Limit": {
    			"type": "value",
    			"value": 200
    			}
    		}
    	}
    },
}
```

### Capture assignee of completed task

You can use output mapping and the `sys_task_assignee` pre-defined variable to capture the assignee of a completed task. This is helpful because you could use the assignee information in another process. For example, you could use this in a support context where whoever the assignee of a completed task is could be the contact person for the account for which the task was carried out.

> **Note:** The `sys_task_assignee` variable is a system variable and cannot be edited.

To create a process that captures the assignee of a completed task:

1. Create a [form]({% link process-automation/latest/model/forms.md %}).

2. Create a process that includes a [User task]({% link process-automation/latest/admin/monitor.md %}#user-tasks).

3. From the **Properties** pane select the form you created from the **Form name** dropdown list.  

4. From the **Mapping type** dropdown list select **Map variables**.

5. Deselect the **User task** by clicking anywhere in the white space and then click **Edit Process Variables** from the right pane.

6. Click the **+** icon and enter a name for the process variable in the **Name** field.

7. From the **Type** dropdown list select **Primitives** then select **string** and then click **Update**.

8. Select your **User task** again and from the `sys_task_assignee` dropdown menu under **Output mapping** select the process variable you have just created.

You now have a process that captures the assigned user of a completed task.

## Errors

Errors are used by error catching events and error throwing events to model business exceptions using [BPMN elements]({% link process-automation/latest/model/processes/bpmn.md %}). They can be created and managed at the individual error event level, or at a diagram level. Unlike process variables, errors can be shared between process definitions in the same diagram.

To manage all errors in a diagram:

* Make sure no BPMN element is selected by clicking on a blank section of the canvas and the **Edit Errors** button will be visible in the right-hand properties panel.

* If the diagram contains more than one process definition then clicking on the individual [pools]({% link process-automation/latest/model/processes/bpmn.md %}#pools-and-lanes) will also show the **Edit Errors** button.

## Messages

Messages are used by message catching events and message throwing events to send a message and optional payload between [BPMN elements]({% link process-automation/latest/model/processes/bpmn.md %}). They can be created and managed at the individual message event level, or at a diagram level. Unlike process variables, messages can be shared between process definitions in the same diagram.

To manage all messages in a diagram:

* Make sure no BPMN element is selected by clicking on a blank section of the canvas and the **Edit Messages** button will be visible in the right-hand properties panel.

* If the diagram contains more than one process definition then clicking on the individual [pools]({% link process-automation/latest/model/processes/bpmn.md %}#pools-and-lanes) will also show the **Edit Messages** button.

## Actions

The actions that can be run against a process are:

| Action | Description |
| ------ | ----------- |
| Save process diagram as SVG | Download the process diagram in `svg` format. |
| Download process | Download the `.bpmn20.xml` for the process. |
| Validate | Run validation against the process. Any errors can be seen in the log history at the bottom of the Modeling Application and are flagged in a pop-up box. |
| Save | Save any changes made on the process diagram. |
| Delete | Delete the process diagram. |

## Edit User Task Notifications

Use the **Edit User Task Notification** window to edit the default email templates used for processes. You can configure the **From** and **Subject** fields for the selected user task so that at runtime they will send task email notifications that are not the default, to the assignee or candidate.

The fields on the **Assignee** tab and **Candidate** tabs are:

| Action | Description |
| ------ | ----------- |
| From | Enter an email address that the task will be sent from. |
| Subject | Enter a message for the user that will recieve the notification. For example `The task ${taskName} awaits your response.` |
| Email template | Select the email template you want to use. You can select from the, **Default email template**, **From file**, **From URL**, and **Create new email template**. |

## Edit Process Permissions

Use the **Edit Process Permissions** window to configure who can start a new process. The permission levels available are: **Everyone can start it**, **Nobody can start it**, or **Specific users/groups** can start it.
---
title: Using Process Automation
---

The default user interface for managing content, processes and tasks is the [Alfresco Digital Workspace]({% link digital-workspace/latest/index.md %}). An instance of the Digital Workspace is deployed with every application and used to manage the processes associated with that application.

Users need to have been given [user access]({% link process-automation/latest/admin/release.md %}#deploy-steps/user) to an application in order to access and manage content and processes in the Digital Workspace.

> **Note**: The Digital Workspace can be [extended]({% link process-automation/latest/develop/index.md %}#extend-the-digital-workspace) or replaced with a [custom interface]({% link process-automation/latest/develop/index.md %}#develop-a-custom-user-interface) built using the Application Development Framework.

## Processes

The **Processes** section is used for monitoring all the process instances in the application. The three default views are:

* **Running** which displays all in-flight process instances.
* **Completed** which displays all process instances that have been completed.
* **All** which displays all in-flight, completed, cancelled and suspended process instances.

### Properties {#process-properties}

The properties for each process instance are:

| Property | Description |
| -------- | ----------- |
| Name | The name given to the process instance when it was started. |
| Process Definition Name | The [process definition]({% link process-automation/latest/model/processes/index.md %}) the instance is using. |
| Status | The current status of the process instance. See the table below for a list of possible statuses. |
| Start Date | The time since the process instance was started. |
| Completed Date | The time since the process instance was completed. It will be blank if the process instance has not yet been completed. |
| Started By | The name of the user that started the process instance. |

> **Note**: Further details are available to view for each process instance by clicking on it. A properties panel will appear on the right-hand side of the screen.

The status of process instances are:

| Status | Description |
| ------ | ----------- |
| RUNNING | The process instance is currently running. |
| COMPLETED | The process instance has been completed. |
| SUSPENDED | The process instance is currently suspended and cannot continue until it is reactivated. |
| CANCELLED | The process instance has been cancelled and cannot be completed. |

### Start a process instance

To start a process instance:

1. Sign into the Digital Workspace.

2. Click **Start Process**.

3. Select the process you would like to start from the modal window.

    If you defined categories when you created your processes, they will be organized within those categories.

4. Click **START PROCESS**.

    > **Note:** Once you have selected the process you would like to work with from the modal window you can copy and share the URL with another user, so they can start the process. This user must have credentials to sign into the Digital Workspace.

All Alfresco Digital Workspace users who have initiated a process or participated in one can see all the tasks from the process, including the tasks assigned to other users. To see the list of tasks navigate to **Process Management** > **Processes** > **Running** > **Process details**.

### Start a process instance from a file

Process instances can also be started from a file in the repository. If the process definition contains a [start event]({% link process-automation/latest/model/processes/bpmn.md %}#start-event) that contains a form with an [attach file field]({% link process-automation/latest/model/forms.md %}#attach-file-fields) then the content will be attached to the process as it is started.

1. Sign into the Digital Workspace.

2. Navigate to, or search for the file to start the process with.

3. Right click on the file and select **Start Process**.

4. Select the process definition to use from the dropdown. If the definition does not contain an upload field then a notice is displayed.

5. Give the process instance a name and click **Start Process**.

### Filter process instances

The default process instance views can be updated by changing the filters. New views can also be created by editing the filters for a view and selecting saving a new one.

The properties for filters are:

| Property | Description |
| -------- | ----------- |
| Process Name | The name of the process instances to display. |
| Process Definition | The process definition to filter by. |
| Status | The statuses of process instances to display. |
| Sort by | The column to sort by, for example `Process Name`, `Status` or `Initiator`. |
| Order by | Whether the ordering is ascending or descending. |
| Completed Date | The date range for when the process instances were completed. |
| Started Date | The date range for when the process instances were started. |

Once you have customized a filter, there are two options:

* **Save filter**: Selecting this will save the filter over the current view.
* **Save filter as**: Selecting this will give you the option to provide a name for a new view for your filter and add it under the **Processes** section.

You can use the **Delete filter** option at any time to remove a view.

## Tasks

The **Tasks** section is used for monitoring all the tasks in the application. The three default views are:

* **My Tasks** which displays all tasks assigned to the user.
* **Queued Tasks** which displays all unclaimed tasks the user is eligible to claim.
* **Completed Tasks** which displays all tasks completed by the user.

In the Digital Workspace you are notified of new tasks assigned to you next to **My Tasks** and **Queued Tasks**. The number within the indicator displays how many tasks of that type you have been assigned. If at least one task has not been seen yet the indicator will be orange. The number within the task counter will continue to display until the tasks are completed.

### Properties {#task-properties}

The properties for each process instance are:

| Property | Description |
| -------- | ----------- |
| Name | The name of the task. |
| Status | The current status of the task. See the table below for a list of possible statuses. |
| Assignee | The user assigned to the task. It will be blank if the task is unclaimed. |
| Status | The current status of the task. See the table below for a list of possible statuses. |
| Created Date | The time since the task was started. |
| Last Modified | The time since the task was last updated. |
| Due Date | The date and time the task is due to be completed by. |
| Priority | The relative priority of the task. |

> **Note**: Further details are available to view for each task by clicking on it. A properties panel will appear on the right-hand side of the screen.

The status of tasks are:

| Status | Description |
| ------ | ----------- |
| CREATED | The task has been created but not yet assigned. |
| ASSIGNED | The task has assigned but not yet completed. |
| COMPLETED | The task has been completed. |
| SUSPENDED | The task is suspended because the process instance it belongs to has been suspended. It cannot be completed until the process instance is activated. |
| CANCELLED | The task has been cancelled and cannot be completed. |

### Claim and release tasks

Tasks that are assigned to a [candidate group]({% link process-automation/latest/model/processes/bpmn.md %}#user) can be claimed by an individual user to work on the task. Claiming a task will remove it from other candidates **Queued Tasks** list.

To claim a task:

1. Sign into the Digital Workspace.

2. Click on the **Queued Tasks** view under **Tasks**.

3. Click on the task to claim and select **Claim**. The task status will update to `ASSIGNED`.

Tasks that have been claimed from a candidate group can also be released. This will remove it from your **My Tasks** list and put it back in **Queued Tasks**.

To release a task:

1. Sign into the Digital Workspace.

2. Click on the **My Tasks** view under **Tasks**.

3. Click on the task to release and select **Release**. The task status will update to `CREATED`.

### Filter tasks

The default task views can be updated by changing the filters. New views can also be created by editing the filters for a view and selecting saving a new one.

The properties for filters are:

| Property | Description |
| -------- | ----------- |
| Status | The statuses of tasks to display. |
| Assignee | The tasks assigned to which user to display. |
| Process Definition | The process definition to filter by. |
| Task Name | The name of the tasks to display. |
| Priority | The relative priority level of tasks to display. |
| Sort by | The column to sort by, for example `Created Date`, `Status` or `Priority`. |
| Order by | Whether the ordering is ascending or descending. |
| Due Date | The date range for when the tasks are due by. |
| Completed Date | The date range for when the tasks were completed. |

Once you have customized a filter, there are two options:

* **Save filter**: Selecting this will save the filter over the current view.
* **Save filter as**: Selecting this will give you the option to provide a name for a new view for your filter and add it under the **Tasks** section.

You can use the **Delete filter** option at any time to remove a view.

## Configure Process and Task lists

You can configure the columns of the Process and Task lists in the Digital Workspace.

The order of the columns can be adjusted.

1. Navigate to Process Management on the left and then select any Process or Task list.

2. Access the six dots on the top right of a column by hovering your mouse over the name of the column.

3. Click and hold the six dots and then move the column on top of another column.

    This moves the columns to the left one position and the column you are moving takes the place of the one underneath.

![Move column]({% link process-automation/images/move-column.png %})

The columns that are visible can be adjusted.

1. Navigate to Process Management on the left and then select any Process or Task list.

2. Click the three dots on the right of the last column.

3. Select which columns you want show and then click **Apply**.

![Select columns]({% link process-automation/images/select-columns.png %})

### Column width

You can adjust the width of the columns of the **Process Management** section. To do this select the edge of the columns and adjust them to the desired width. Once you change one column, all the columns with the same name are also adjusted. If you log out and then log back in again, the new column widths is preserved.

This feature is enabled by default for the **Process Management** section. If you want to adjust the column widths in the same way for the **Personal Files** or **File Libraries** sections of the Digital Workspace, you must turn it on by editing the `libs/content-ee/process-services-cloud-extension/assets/process-services-cloud.extension.json` file and adding the following:

```json
"column-resizing": [
                    {
                        "id": "column-resizing",
                        "enabled": true
                    }
                ]
```

## Condition builder {#condition-builder}

The condition builder is a tool that helps you build a JUEL expression for a condition. The condition is composed of a set of boolean statement(s) that are linked by an operator. This means the condition to be created is a statement evaluated as a boolean value. The following is an example.

![Condition builder]({% link process-automation/images/condition-builder.png %})

* Click the **$** button to switch the condition builder to an expression editor where you can display and edit the JUEL expression.

* Click the **+** button to add a new statement editor.

* The available operators are:
  * **Every**: All statements must be true for the condition to be evaluated as true.
  * **At least one**: The condition will be evaluated to be true when one or more of the statements are true.
  * **None**: If all the statements are false, then the condition will be evaluated to be true.
  
  > **Note:** The operator between statements is the same for all the statements.

* Click the **-** button to remove the statement.

### Statement editor

The statement editor manages boolean statements. A boolean statement normally consists of two statements and an operator between them, for example `<left-statement> <operator> <right-statement>`.

The statement editor reproduces the structure, the following is an example.

![Statement editor]({% link process-automation/images/statement-editor.png %})

#### Left statement

The left-statement can be one of the available variables or a JUEL expression. Switching between variable and JUEL expression can be done using the tabs at the top of the left side.
The available operators between statements are:

* Equals
* Not equals
* Greater than
* Greater or equals than
* Less than
* Less or equals than
* Not set

> **Note:** The `Not set` operator means that the expression is a single statement expression which means no right-statement is needed.

#### Right statement

The right-statement can be one of the available variables, a JUEL expression, or a value if the left-statement is a variable value.

## Expression editor

The expression editor is a code editor that provides autocompletion and hints when writing an expression that may contain a JUEL expression. In the expression editor you can test JUEL expressions by first setting the values of variables and then once the expression has been created it can be tested by clicking the **Test** button. The result is displayed in the gray area above the variables.
The expression editor appears in the following places:

* Task mapping dialog: when selecting an expression as a variable value
* Variable dropdown selector: when using the dollar button
* User task assignment dialog
* Called element dialog: when using an expression to resolve the called element
* In the email template dialog: when setting the template for the email used in user tasks
* In the condition builder
* When setting the value of a JSON variable

Click the green button to expand the modal dialog to be full size, the following is an example.

> **Note:** The green button only displays if the expression editor has been configured for it to show.

![Expression editor]({% link process-automation/images/expression-editor.png %})

### Autocompletion

The autocompletion function is based on the context of the project and depends on where the expression is going to be used. It lets the user know which variables in that context are available. The autocompletion is displayed as the user types but can also be triggered by using the following keyboard shortcuts:

* In Windows or Linux: `Ctrl + Space`
* In MacOS: `Ctrl + Space` or `Fn + Ctrl + Space`

The following is an example.

![Auto completion]({% link process-automation/images/auto-completion.png %})

Autocompletion displays suggestions for operators, in the example `empty` and `eq`, and for variables `event` in the screenshot.

Autocompletion can also show method suggestions and attributes when using the ‘dot’ accessor, in the example below `equals` and `hashcode` are methods while `data` and `datacontenttype` are attributes of the `event` object.

![Event]({% link process-automation/images/event.png %})

### Hints

The expression editor provides helpful information when you place the cursor over an element of it. For example, in the image the cursor has been placed over the word `event` and a hint is displayed that provides a description of the `event` variable.

![Hints]({% link process-automation/images/hints.png %})

## Process Analytics

> **Important:** Process Analytics is only applicable for use by Alfresco Activiti Enterprise customers who are self managed. It is not compatible for use with Process Automation.

Process Analytics exposes a set of APIs that can be used to query business metrics about process instances and user tasks. The query language it uses is GraphQL.

> **Note:** You must have the `ACTIVITI_ANALYTICS` role in the Identity Service to be able to execute queries.

### Information available for process instances

* Process instance duration in seconds (minimum, maximum, or average)
* Total number of process instances (count)

Data can be filtered by:

* date range
* application name
* process definition name
* process status

Grouped by:

* process definition name
* process instance name

Aggregated by:

* time intervals (minute, hour, day, week, month, quarter, year)
* process status

### Information available for user tasks

* User task duration in seconds (minimum, maximum or average)
* Total number of user tasks (count)

Data can be filtered by:

* date range
* application name
* process definition name
* user task status

Grouped by:

* process definition name
* user task name
* user task assignee

Aggregated by:

* time intervals (minute, hour, day, week, month, quarter, year)
* process status

#### To use the process analytics APIs

Before you use the process analytics APIs you must use the Admin app and change the password of the person who will be using them. When using the process analytics playground use incognito mode for your browser. You access the playground by navigating to `https://{domain-name}/analytics/playground/`. Use your new credentials to log into the system and you will see a similar screen to below.

![Process Analytics]({% link process-automation/images/process-analytics.png %})

There are two tabs on the right side of the Playground: **Docs** and **Schema**. You can use them to learn about the structure of the APIs.

#### Example queries

Here are some examples of GraphQL queries that can be used in the Playground.

**Example 1:** Number of user tasks completed in 2022 aggregated by month

```json
{
  taskMetrics(
    query: {
      range: {
        from: "2022-01-01T00:00:00Z"
        to: "2022-12-31T00:00:00Z"
      } 
    } 
  ) 
  { 
    timer(name: activiti_user_task_completed) { 
      count 
      interval(by: task_completed_date, period: month, format: "yyyy-mm") 
    } 
  } 
} 
```

**Example 2:** Average process duration of the processes completed in June 2022 aggregated by day and grouped by process definition name

```json
{
  processMetrics(
    query: {
      range: {
        from: "2022-06-01T00:00:00Z"
        to: "2022-06-30T00:00:00Z"
      }
    }
  )
  {
    timer(name: activiti_process_instance_completed) {
      duration (stat: avg)
      interval(by: process_completed_date, period: day, format: "yyyy-mm-dd")
      group (by: process_definition_name)
    }
  }
}
```
