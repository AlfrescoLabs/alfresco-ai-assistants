---
title: Alfresco Process Services
---

Process Services is an enterprise Business Process Management (BPM) solution targeted at business people and developers. At its core is a high performance open-source business process engine based on [Activiti](https://www.activiti.org/){:target="_blank"} with the flexibility and scalability to handle a wide variety of critical processes. Process Services provides a powerful suite of end user tools and integrates with a range of enterprise systems, including Alfresco Content Services, Box and Google Drive.

Starting from Process Services 24.1, six out-of-the box workflows provide a faster time to value for these frequently used simple workflows. The workflows are for assigning tasks, review, and approval:

* New Task
* New Task (group)
* Review and Approve (group review)
* Review and Approve (one or more reviewers)
* Review and Approve (pooled review)
* Review and Approve (single reviewer)

See the [Preconfigured workflows]({% link process-services/latest/using/workflows.md %}) documentation for more details.
---
title: Administration of Process Services
---

This section goes through the high level architecture of Process Services and using the Process Services Administrator application.

## Architecture

Process Services is a suite of components on top of the Activiti BPMN 2.0 platform that can be run on-premise or hosted on a private or public cloud, single, or multitenant.

For more information about Activiti BPM, see [Activiti.org](https://www.activiti.org){:target="_blank"}.

The following diagram gives a high-level overview of the technical components in Process Services.

![high_level_architecture_aps]({% link process-services/images/high_level_architecture_aps.png %}){:height="450px" width="638px"}

Process Services is packaged as a standard Java Web application (WAR file) that can be deployed in any supported Java web container. The WAR file contains the Java logic, REST API resources, and the user interface HTML and JavaScript files. The application is stateless, which means it does not use any sessions, and requests can be handled by any node in a clustered setup (see [Cluster configuration and monitoring](#cluster-configuration-and-monitoring) for more information on multi-node setup).

## Technical implementation details

* The Process Engine (enterprise edition) is embedded within Process Services and directly used through its Java API.
* The ReST API has two parts:
    * The ReST API that exposes operations in the context of the applications that are part of Process Services. This ReST API is used by the user interface and should be used in most cases.
    * The ReST API that exposes the core engine API directly. Note that this interface is intended for highly custom applications as it exposes the full capabilities and data within the Process Engine. Consequently, a user with the *tenant admin* or *tenant manager* role is needed to access this part of the ReST API for security reasons.
* The application requires Java 7 and is compliant with JEE 6 technologies. The Process Engine itself also supports Java 6, however for components such as Elasticsearch, Process Services requires Java 7 or Java 8. Review the [Supported platforms]({% link process-services/latest/support/index.md %}) list for more information on supported platforms.
* The backend logic specific to the Process Services logic is implemented using Spring 4 and JPA (Hibernate).
* All user interfaces are written using HTML5 and AngularJS.

Process Services uses the following external systems:

* A relational database.
* An Elasticsearch installation. Note that the application ships with an embedded Elasticsearch by default.
* A file system (shared file system in multi-node setup) where content is stored.
* An identity management store such as LDAP or Active Directory (optional). By default, a database-backed user and group store is used.

The Process Engine is managed using the Administrator application. This is also provided as a WAR file.

The App Designer is an Eclipse plugin that can be used by developers to create BPMN 2.0 process definitions within their Eclipse IDE. You can also configure the plugin to pull and push process definition models.

The application can also connect to other on-premise or cloud systems, such as Alfresco Content Services, Box, and Google Drive (not shown in the diagram).

To learn more about Process Services architecture, see our [Alfresco ArchiTech Talks video](https://www.youtube.com/watch?v=gyz2By2g1p8){:target="_blank"}.

## Multi-node clustered setup

You can run the application on multiple servers, for performance, resilience or for failover reasons. The application architecture is designed to be stateless. This means that any server can handle any request from any user. When using multiple servers, it is enough to have a traditional load balancer (or proxy) in front of the servers running the Process Services application. Scaling out is done in a "horizontal" way, by adding more servers behind the load balancer.

![multi-node-setup]({% link process-services/images/multi-node-setup.png %})

Note that each of the servers will connect to the same relational database. While scaling out by adding more servers, make sure that the database can handle the additional load.

## Logging in Process Services

There are several customization options for logging in Process Services.

Process Services uses [log4j2](https://logging.apache.org/log4j/2.x/manual/){:target="_blank"} for logging.

Process Services installs with the default Logback configuration reading from `<Tomcat install location>/webapps/activiti-app/WEB-INF/classes/log4j2.properties` and the equivalent location for Process Services Administrator.

The default configuration can be overridden by placing your own `log4j2.properties` in `<Tomcat install location>/lib`.

By default Process Services logs to the console. If you want to log to a file, you must edit the logging configuration file to specify a file appender, and location. For example, you can use the following file appender definition:

```
appender.rolling.type=RollingFile
appender.rolling.name=RollingAppender
appender.rolling.fileName=share.log
appender.rolling.filePattern=share.log.%d{yyyy-MM-dd}
appender.rolling.layout.type=PatternLayout
{%raw%}appender.rolling.layout.pattern=%d{yyyy-MM-dd} %d{ABSOLUTE} %-5p [%c] [%t] %replace{%m}{[\r\n]+}{}%n{%endraw%}
appender.rolling.policies.type = Policies
appender.rolling.policies.time.type=TimeBasedTriggeringPolicy
appender.rolling.policies.time.interval=1

rootLogger.appenderRef.rolling.ref=RollingAppender 
```

## Process Services Administrator

The Administrator app can be used to inspect and manage the data for a Process Engine (or cluster of engines). It's also used for cluster configuration and monitoring. It is distributed as a separate web application (WAR file).

Typically, there is one single Administrator application for multiple environments (for example, development, testing, production, and so on), which is accessed by a handful of users (system administrators). Generally, it is not necessary to have multiple instances of this application running.

The Process Engine is cluster-enabled so, together with the Process Services Administrator, a user can configure and monitor a cluster (or multiple different clusters) through a graphical user interface. The clustered engines will use the same configuration and will report metrics and status back to the Process Services Administrator where they are displayed.

See [install Process Services Administrator]({% link process-services/latest/install/manual.md %}#install-process-services-administrator) to install the Process Services Administrator application.

### Administrator database configuration

The database for the Administrator app is configured using the following properties. See the [Database configuration]({% link process-services/latest/config/database.md %}) section for more information about how to configure Process Services.

For example (using MySQL):

```text
com.mysql.cj.jdbc.Driver
datasource.url=jdbc:mysql://127.0.0.1:3306/activitiadmin?characterEncoding=UTF-8
datasource.username=alfresco
datasource.password=alfresco
hibernate.dialect=org.hibernate.dialect.MySQLDialect
```

### Cluster configuration and monitoring

Process Services Administrator can show the process data and manage the configuration of multiple clusters. In this context a *cluster* is a number of Process Engines that logically belong together. Note that this does not relate to the way that these engines are architecturally set up: embedded, exposed through REST, with or without a load balancer in front, and so on.

Also note that the Administrator is capable of inspecting the information of each Process Engine (if configured correctly). It is not, therefore, solely bound to using the Process Engine in Process Services, but to all enterprise Process Engines.

Multiple clusters can be configured and managed through the Process Services Administrator. This is displayed in the drop-down in the top-right corner:

![cluster_dropdown]({% link process-services/images/cluster_dropdown.png %})

>**Note**. Each of the engines in a cluster should point to the same database schema.

To access the data of a cluster, the Administrator application uses one Process Services REST application per cluster (to avoid direct access to the database from the Administrator or potentially to manage different engine versions).

The REST API endpoints can be included in your application using the Maven artifact `com.activiti.activiti-rest`. It is configured in a similar way as the Administrator.

No special setup is needed when using Process Services, as it contains the necessary REST API endpoints out of the box.

As shown in the diagram below, any cluster can consist of multiple engine nodes (pointing to the same database schema), the data that is managed in the Administrator is fetched through an Process Services REST application only.

![admin_app_arch]({% link process-services/images/admin_app_arch.png %})

In the same drop-down as shown above, a new cluster can be created. Note that a user will be created when doing so. This user is configured with the role of *cluster manager* and is used to send information to the HTTP REST API of the Administrator application, but it cannot log in into the Administrator application as a regular user for safety reasons.

The REST endpoint for each cluster can be configured through the Administrator. Simply change the settings for the endpoint on the **Configuration > Engine** page while the cluster of choice is selected in the drop-down in the top-right corner. The current endpoint configuration is also shown on this page:

![endpoint-config]({% link process-services/images/endpoint-config.png %})

The Process Engine and the Administrator app communicate through HTTP REST calls. To send or get information from the Administrator app, you must configure the Process Engine with a correct URL and credentials.

For the engine, this can be done programmatically:

```java
processEngineConfig.enableClusterConfig();
processEngineConfig.setEnterpriseAdminAppUrl("http://localhost:8081/activiti-admin");
processEngineConfig.setEnterpriseClusterName("development");
processEngineConfig.setEnterpriseClusterUserName("dev");
processEngineConfig.setEnterpriseClusterPassword("dev");
processEngineConfig.setEnterpriseMetricSendingInterval(30);
```

This configures the base HTTP API URL, the name of the cluster that the engine is part of, the credentials of the user allowed to send data to the API and the time interval between sending data to the Administrator application (in seconds).

Process Services includes the Process Engine. To enable engine clustering you can set the properties (similar to the programmatical approach) directly in the configuration file:

```text
cluster.enable=true
cluster.config.adminapp.url=http://localhost:8081/activiti-admin
cluster.config.name=development
cluster.config.username=dev
cluster.config.password=dev
cluster.config.metricsendinginterval=30
```

Process Services also sends extra metrics to the Administrator application. To configure the rate of sending, a cron expression can be set (by default the same as the rate of sending for the Process Engine):

```text
cluster.config.app.metricsendingcronexpression=0/30 * * * * ?
```

Alternatively, you can generate a jar file with these settings through the **Configuration > Generate cluster jar** button. If you place the jar file on the classpath (or used as a Maven dependency if using a local Maven repository) of an engine or Process Services application, it will have precedence over the properties files.

Once the application is running, metrics for that node in the cluster are shown in the Admin application:

![node-joined-cluster]({% link process-services/images/node-joined-cluster.png %})

In the Admin application, the following two settings can be changed:

```text
cluster.monitoring.max.inactive.time=600000
cluster.monitoring.inactive.check.cronexpression=0 0/5 * * * ?
```

* `cluster.monitoring.max.inactive.time`: This a period of time, expressed in milliseconds, that indicates when a node is deemed to be inactive and is removed from the list of nodes of a cluster (nor will it appear in the **monitoring** section of the application). When a node is properly shut down, it will send out an event indicating it is shut down. From that point on, the data will be kept in memory for the amount of time indicated here. When a node is not properly shut down (for example, hardware failure), this is the period of time before removal, since the time the last event is received. Make sure the value here is higher than the sending interval of the nodes, to avoid that nodes incorrectly removed. By default `10 minutes`.
* `cluster.monitoring.inactive.check.cronexpression`: A cron expression that configures when the check for inactive nodes is made. When executed, this will mark any node that hasn’t been active for `cluster.monitoring.max.inactive.time` seconds, as an inactive node. By default, every `5 minutes`.

#### Cluster master configuration

For each cluster, a *master configuration* can be defined. When the instance boots up, it will request the master configuration data from the Administrator application. For this to work, the `cluster.x` properties (or equivalent programmatic setters) listed above need to be set correctly.

There is one additional property that can be set: `cluster.master.cfg.required=`. This is a boolean value, which if set to `true` will stop the instance from booting up when the Admin app could not be reached or no master configuration is defined. In case of `false`, the instance will boot up using the local properties file instead of the master configuration.

The master configuration works for both clusters of embedded Process Engines or Process Services instances. The two can not be mixed within the same cluster though.

>**Note**: When changing the master configuration, the cluster instances would need a reboot. The Administrator application will show a warning for that node too in the **monitoring** tab, saying the master configuration currently being used is incorrect.

### HTTP communication with Administrator

Communication with the Administrator Application is done using HTTP REST calls. The calls use HTTP Basic Authentication for security, but do use different users, depending on the use case.

Process Services and the Administrator Application do not share user stores because:

* Typically, there are only a handful of users involved with the Administrator Application.
* The Administrator Application can be used independently.

The following pictures gives a high-level overview:

![admin-app-communication01]({% link process-services/images/admin-app-communication01.png %})

* The Process Engine pushes and pulls data to and from the Administrator Application REST API. These calls use basic authentication with a user defined in the Administrator Application user store (relational database). Such a user is automatically created when a new cluster configuration is created (see above), but its credentials need to be configured on the engine/Suite app side (see the `cluster.xx` properties.)
* The Administrator Application allows you to browse and manage data in an Enterprise Process Engine. It calls the REST API to do so, using a user defined in the user store of the Suite Application (or any other authentication mechanism for the embedded engine use case).

For Process Services: The user needs to have a *Tenant Admin* or *Tenant Manager* role, as the Administrator Application gives access to all data of the engine.

The following diagram illustrates what this means for an end user:

![admin-app-communication02]({% link process-services/images/admin-app-communication02.png %})

An end user logs in through the UI, both on the Suite as the Admin Application. Again, the user store is not shared between the two.

It’s important to understand that the HTTP REST calls done against the Suite REST API, are done using the credentials of the Suite application using a user defined in the user store of the Suite Application. This user can be configured through the Administrator Application UI.

In case of using LDAP, a equivalent reasoning is made:

![admin-app-communication03]({% link process-services/images/admin-app-communication03.png %})

The user that logs into the Administrator Application is defined in the relational database of the Administrator Application. However, the HTTP REST call will now use a user that is defined in LDAP.

### Configure the REST app for use with the Administrator application

When using the Process Engine embedded in a custom application (or multiple embedded engines), it is still needed to set up a REST endpoint that the Administrator application can use to communicate with to see and manage data in the engines cluster.

Process Services already contains this REST API, so you must add this additional REST app.

Out of the box, the REST application is configured to have a default admin user for authentication and uses an in memory H2 database. The latter of course needs to be changed to point to the same database as the engines are using.

The easiest way to do this, is to change the properties in the `/WEB-INF/classes/META-INF/db.properties` file with the correct datasource parameters. Make sure the driver jar is on the classpath.

To change default user, change the settings in `/WEB-INF/classes/META-INF/engine.properties`. In the same file, you can also configure the following basic engine settings:

* `engine.schema.update`: Indicates if the database schema should be upgraded after booting the engine (if this is needed). The default value is `true`.
* `engine.asyncexecutor.enabled`: Indicates if the async job executor is enabled. By default, it is set to `false`, as this is better done on the engine nodes itself otherwise you would have to make sure the classpath has all the delegates used in the various processes.
* `engine.asyncexecutor.activate`: Instructs the Process Engine to start the Async executor thread pool at startup. The default value is `false`.
* `engine.history.level`: The history level of the process engine. **Make sure this matches the history level in the other engines in the cluster**, as otherwise this might lead to inconsistent data. The default value is `audit`.

If these two property files are insufficient in configuring the process engine, you can override the complete process engine configuration in a Spring xml file located at `/WEB-INF/classes/META-INF/activiti-custom-context.xml`. Uncomment the bean definitions and configure the engine without restrictions, similar to a normal Activiti Process Engine configuration.

The out-of-the-box datasource uses C3P0 as connection pooling framework. In the same file, you can configure this datasource and transaction manager.

The application uses Spring Security for authentication. By default, it will use the Process Services identityService to store and validate the user. To change it, add a bean with id `authenticationProvider` to `/WEB-INF/classes/META-INF/activiti-custom-context.xml`. The class should implement the `org.springframework.security.authentication.AuthenticationProvider` interface (see Spring docs for multiple implementations).

>**Note:** The Rest app is not compatible with using a master configuration. It needs to be configured through the properties or the spring context XML.

### Using Process Services Administrator application

Use the Administrator application to perform basic administration functions in Process Services. For example, you can
inspect the state of Process Engines, delete an app, view when an app was deployed, or monitor clusters.

The Administrator application has the following tabs:

* **Apps** - Use for deleting apps, redeploying an app to another cluster, and downloading apps.
* **Deployments** - View the current deployment and its content such as process definitions, deploy time, tenant information and so on.
* **Definitions** - View process definitions and their related instances.
* **Instances** - View running or completed process instances for each process definition. You can also see related information for each process definition, such as, tasks, variables, subprocesses, jobs, decision tables, and forms information. In addition, you can download binary process data for troubleshooting process issues.
* **Tasks** - View tasks information and perform actions on them, such as edit, assign/claim, delegate, complete tasks. In addition, you can view task forms, sub tasks, variables, and identity links for a particular task.
* **Jobs** - View the current job details based on its Process Instance ID, due date, and Job Id. Exceptions are displayed if the jobs failed to execute (For example, if a mail server could not be reached).
* **Monitoring** - Enables you to monitor the cluster information.
* **Configuration** - Add and configure cluster information. See [Cluster configuration and monitoring](#cluster-configuration-and-monitoring) for more information.

#### Deploy apps

You can deploy apps in various ways in the Administrator application. For example, you can upload and publish an app model from a zip file, deploy an existing app from one cluster to another, or redeploy an existing app model to another cluster. Deploying app models to another cluster is particularly useful when your app needs to be progressed from staging to production or copied from the development environment to production. However, when any changes made to the development environment need to be carried over to production, you should select the target cluster (the production system in this case) in the Administrator application and redeploy your app.

* To upload and publish an app model from a zip file, in the Administrator application, click **Apps > Publish an app model**.

**Prerequisite**: Make sure you have configured at least two clusters. To create a new cluster, select **Clusters list > Create new cluster**.

![cluster]({% link process-services/images/cluster.png %})

**To deploy an app model to a different cluster**:

1. Go to **Admin App** > **Apps** and then select an app model.
2. Click **Publish an app model**. The Publish app model dialog box appears.
3. Select **Publish app to another cluster** and select the cluster you want your app to be published to.
4. Click **Publish**.

**To redeploy an existing app to a different cluster:**

1. Go to **Admin App** > **Apps** tab.
2. Select the app that you need to move to a different cluster, and then click **Redeploy an app to another cluster**. A dialog box to select a cluster appears.
3. Select the cluster that you would like your app to be moved to, and then click **Deploy**. If the process app already exists, it is versioned and updated.

**To download an app:**

1. Go to **Admin App** > **Apps** tab.
2. Select the app that you want to download.
3. Click **Download app**.

**To delete an app**:

1. Go to **Admin App** > **Apps** tab.
2. Select the app that you want to delete.
3. Click **Delete App**.

#### Download binary process data

Sometimes, you may experience an issue with a process and you need to resolve the problem. The Administrator app gives you the option to download the binary process data for use in troubleshooting and investigating process issues.

1. Go to the Administrator app and then click **Instances**.

2. Find the binary process data from the variables list.

    ![binary-download]({% link process-services/images/binary-download.png %})

3. Click the **download** button.

    The ![]({% link process-services/images/binary-download-icon.png %}){:height="18px" width="18px"} button appears for binary variables only as the process designer detects the underlying object type.

    The binary process data is downloaded to the local machine. The file is provided in a serialized binary format.

    >**Note:** It is not possible to upload binary process data files.

#### Read-only access to the Administrator app

You may have users in your organization who assist when debugging problems and need to access the information in the Administrator app, but who don't need to make changes. You can give these users permission for read-only access to the Administrator app. This ensures that these users are able to contribute to issue trouble shooting without accidentally breaking any operational processes.

A read-only user can log in just like any other user but their permissions control the ready-only option.

>**Note:** The read only admin is a feature to avoid accidental changes to the system by trusted users. If you don’t trust such a user, we do not advise giving them access to a read only admin view account. This feature ensures a level of security for the UI only and it is possible for a user with read-only UI permission to make changes through the REST API.

1. Create the user in the Administrator app.

2. Click the **Read only user** check box.

    ![Read-only-user]({% link process-services/images/Read-only-user.png %})

3. Click **Create user**.

    The new user can log in and access the Administration app but does not have the ability to make any changes.
---
title: Application configuration
---

There are several configuration options for application, process and task management.

## Application access

It is possible to configure whether users get access to the model editors (the **App Designer** application) and the analytics application.

Access to the default application is configured through *capabilities*. In the admin UI, it is possible to create *system groups*. These groups have a set of capabilities. All users part of that group have those capabilities.

The following settings configure app access when a new user is created in the system (manual or through LDAP sync). To enable access, set the property `app.[APP-NAME].default.enabled` to `true`. If `true`, a newly created user will be given access to this app.

The access is configured by adding the user to a group with a certain capability that enabled the app. The name of that group can be configured using the `app.[APP-NAME].default.capabilities.group` property. If this property is set, and the `app.[APP-NAME].default.enabled property` is set to `true`, the group with this name will be used to add the user to and provide access to the app. If the group does not exist, it is created. If the property is commented, and `app.[APP-NAME].default.enabled property`, a default name is used.

Current possible app names: `{ analytics | kickstart }`

|Property|Default|
|--------|-------|
|app.analytics.default.enabled|`true`|
|app.analytics.default.capabilities.group|`analytics-users`|
|app.kickstart.default.enabled|`true`|
|app.kickstart.default.capabilities.group|`kickstart-users`|

The following setting, if set to `true`, will create a default example app with some simple review and approve 
processes for every newly created user.

|Property|Default|
|--------|-------|
|app.review-workflows.enabled|`false`|

## User creation

When the application starts for the first time, it will verify that there is at least one user in the system. If not, a user with superuser rights will be created.

The default user ID to sign in with is `admin@app.activiti.com` using password `admin`. 

>**Important**: This should be changed after signing in for the first time.

The initial user details can be modified (must be done `before` first start up) with following properties:

|Property|Description|
|--------|-----------|
|admin.email|The email address used to create the first user, which also acts as the sign in identifier.|
|admin.group|Capabilities in Process Services are managed by adding users into certain groups. The first user will have all capabilities enabled. This property defines the name of the group to which the first user will be added. By default it is `Superusers`.|

## Login session

It is possible to invalidate the current Process Services app login session when you close the web browser. By default, closing the web browser will maintain the session cookie and will keep the current login session open.

To invalidate the login session, do the following:

1. Open the `<InstallLocation>/tomcat/lib/activiti-app.properties` file.

2. Locate and set `security.use-http-session` to true.

    ```text
    security.use-http-session=true
    ```

    Set this property to `false` if you do not wish to enable this behavior.

## Process definition cache

The Process Engine operates in a stateless way. However, there is data that will never change, which makes it a prime candidate for caching.

A process definition is an example of such *static data*. When you deploy a BPMN 2.0 XML file to the Process Engine, the engine parses it to something it can execute, and stores the XML and some data, such as the description, business key, in the database. Such a process definition will never change. Once it’s in the database, the stored data will remain the same until the process definition is deleted.

On top of that, parsing a BPMN 2.0 XML to something executable is quite a costly operation compared with other engine operations. This is why the Process Engine internally uses a process definition cache to store the parsed version of the BPMN 2.0 XML.

![activiti-proc-def-cache]({% link process-services/images/activiti-proc-def-cache.png %})

In a multi-node setup, each node will have a cache of process definitions. When a node goes down and comes up, it will rebuild the cache as it handles process instances, tasks. and so on.

The process definition cache size can be set by the following property:

|Property|Description|
|--------|-----------|
|activiti.process-definitions.cache.max|The number of process definitions kept in memory. When the system needs to cope with many process definitions concurrently, it is advised to make this value higher than the default. The default value is `128`. |

## Validator configuration

By default, Process Services is configured in a way that process modelers have access to all powerful features of the Process Engine. In many organizations this is not a problem, as the people who are modeling are trusted IT people or business analysts.

However, some organizations may expose the modeling tools of Process Services directly to all end users giving them access to the full array of its capabilities. In such a scenario, some users may gather sensitive data or swamp the resources of the servers. Therefore, various *validators* are introduced that can be enabled or disabled, when required. These validators are run before a process model is deployed to the engine and will block deployment in case of a validation error.

### Disable tasks

The following validators disable the usage of certain tasks. The various validators are configured through the regular Process Services properties. The default value for these validators is `false`. Set the property to `true` to enable the validator.

* `validator.editor.bpmn.disable.startevent.timer|signal|message|error`: Disables the usage of the timer, signal, message or error start event in a process definition.
* `validator.editor.bpmn.disable.scripttask`: Disables the usage of the *script task* in a process definition. Disabling script tasks is typically something you’ll want to do when exposing the modeling tools to end users. Scripts, contrary to the service tasks, don’t need any class on the classpath to be executed. As such, it’s very easy with scripts to execute code with bad intentions.
* `validator.editor.bpmn.disable.servicetask`: Disables the usage of the *service task* in a process definition. Service tasks are used to call custom logic when the process instance executes the service task. A service task is configured to either use a class that needs to be put on the classpath or an expression. This setting disables the usage of service tasks completely.
* `validator.editor.bpmn.disable.executionlistener`: Disables the possibility to define execution listeners in a BPMN process definition. Execution listeners allow to add custom logic to the process diagram that is not visible in the diagram. This setting also disables task listeners on tasks.
* `validator.editor.bpmn.disable.mailtask`: Disables the *mail task* that is used for sending emails.
* `validator.editor.bpmn.disable.intermediatethrowevent`: Disables the usage of all intermediate throw events: none, signal, message, error. They can be used to create infinite loops in processes.
* `validator.editor.bpmn.disable.manualtask`: Disables the usage of the *manual task* task in a process definition.
* `validator.editor.bpmn.disable.businessruletask`: Disables the usage of the *business rule task* in a process definition.
* `validator.editor.bpmn.disable.cameltask`: Disables the usage of the *Camel task* in a process definition. Camel tasks can interact with Apache Camel for various system integrations and have, like regular `JavaDelegate` classes access to the whole engine.
* `validator.editor.bpmn.disable.muletask`: Disables the usage of the *Mule task* in a process definition. Mule tasks are used to interact with a Mule server.

### Limit functionality

The following validators don’t disable a task as a whole, but rather a feature:

* `validator.editor.bpmn.disable.startevent.timecycle`: Allows the usage of a timer start event, but not with a *timeCycle* attribute, as it could be used to create process instances or tasks for many people very quickly, or simply to stress the system resources.
* `validator.editor.bpmn.limit.servicetask.only-class`: Limits the service task to only be configured with a class attribute (so no expression or delegate expression is allowed). Since the available classes are restricted by what is on the classpath, there is a strict control over which logic is exposed.
* `validator.editor.bpmn.limit.usertask.assignment.only-idm`: Limits the user task assignment to only the values that can be selected using the *Identity Store* option in the assignment pop-up. The reasoning to do this, is that this is the only way *safe* values can be selected. Otherwise, by allowing fixed values like expression, a random bean could be invoked or used to get system information.
* `validator.editor.bpmn.disable.loopback`: Disables looping back with a sequence flow from an element to itself. If enabled, it is possible this way to create infinite loops (if not applied correctly).
* `validator.editor.bpmn.limit.multiinstance.loop`: Limits the loop functionality of a multi-instance: only a loop cardinality between 1 and 10 is allowed and a collection nor completion condition is allowed. So basically, only very simple loops are permitted. Currently applied to call activities, sub processes and service tasks.
* `validator.editor.dmn.expression`: Validates the expressions in the decision tables to be correct according to the DMN specification. **By default this is `true` (unlike the others!)**. This means that by default, the DMN decision tables are checked for correctness. If using the structured expression editor to fill in the decision tables, the resulting expressions will be valid. However,if you want to type any MVEL expressions, this property needs to be set
to `false`.

## Log back-end metrics

The application uses SLF4J bounded to Log4j 2. The `log4j2.properties` configuration file can be found in the `WEB-INF/classes` folder of the WAR file.

See [SLF4J](http://www.slf4j.org/){:target="_blank"} and [Log4j 2](https://logging.apache.org/log4j/2.x/){:target="_blank"} for more information.

For all REST API endpoints available in the application, metrics are gathered about run-time performance. These statistics can be written to the log.

|Property|Description|
|--------|-----------|
|metrics.console.reporter.enabled|Boolean value. If `true`, the REST API endpoint statistics will be logged. The default value is `false`. |
|metrics.console.reporter.interval|The interval of logging in seconds. Do note that these logs are quite large, so this should not be set to be too frequent. The default value is `60`. |

>**Note** that the statistics are based on the run-time timings since the last start up. When the server goes down, the metrics are lost.

Example output for one REST API endpoint:

```text
com.activiti.runtime.rest.TaskQueryResource.listTasks
  count = 4
  mean rate = 0.03 calls/second
  1-minute rate = 0.03 calls/second
  5-minute rate = 0.01 calls/second
  15-minute rate = 0.00 calls/second
  min = 5.28 milliseconds
  max = 186.55 milliseconds
  mean = 50.74 milliseconds
  stddev = 90.54 milliseconds
  median = 5.57 milliseconds
  75% <= 141.34 milliseconds
  95% <= 186.55 milliseconds
  98% <= 186.55 milliseconds
  99% <= 186.55 milliseconds
  99.9% <= 186.55 milliseconds
```

## Group manager involvement

When a task is created that has one or more candidate groups assigned, the group managers for those groups will be automatically involved with the created task. To stop group managers from being involved, set the following property to `false`.

|Property|Default|
|--------|-------|
|app.runtime.groupTasks.involveGroupManager.enabled|`true`|

>**Note:** Users that do not have a primary group defined may not have a group manager. To define the primary group, go to **Identity Management > Users > Select an action > Change primary group**.

## Process and task query lists

Process Services provides REST API operations that allow you to query tasks, process instances, historic tasks and historic process instances. You can also request to include task and process variables by using the parameters `includeTaskLocalVariables` and `includeProcessVariables` and setting their values to `true`. When executing REST API calls that include these variables, the result sets could be quite large and you may wish to limit or control the list size provided in the response. The following table shows the properties you can set in the `activiti-app.properties` file to configure this.

|Property|Description|
|--------|-----------|
|query.task.limit|Limits the number of tasks returned from the query `GET /runtime/tasks`.|
|query.execution.limit|Limits the number of process instances returned from the query `GET /runtime/process-instances`.|
|query.historic.task.limit|Limits the number of historic tasks returned from the query `POST /enterprise/historic-tasks/query`.|
|query.historic.process.limit|Limits the number of historic process instances returned from the query `POST /enterprise/historic-process-instances/query`.|

>**Note:**
>
>* You cannot specify the `includeTaskLocalVariables` parameter when using the process and historic process query operations. This is only available for `GET /runtime/tasks` and `POST /enterprise/historic-tasks/query`. You can use the `includeProcessVariables` parameter for all queries specified in the table and apply the corresponding property configuration.
>* If the property configuration for a query limit is not enabled in `activiti-app.properties`, the default limit for the number of instances returned is `20000`.
>* If you omit the `includeTaskLocalVariables` and `includeProcessVariables` parameters or set them to `false`, the request excludes the variables from the response and does not apply the query limit configurations.
>* Setting higher limits for the process or task query properties results in more records fetched from the database. This is likely to mean that you experience slower REST API response times.

## Languages

The Process Services interface is supported for use with a number of languages that have been through a 
quality assurance (QA) and linguistic testing cycle.

Process Services is supported with the following languages:

* US English
* Swedish
* Spanish
* French
* Italian
* Japanese
* Norwegian Bokmå
* Dutch
* Brazilian Portuguese
* Russian
* Simplified Chinese

To change the display language for Process Services, configure the appropriate language in your browser settings.
---
title: Configure authentication
---

The authentication methods that can be configured for Process Services are:

* [The Identity Service](#identity-service)
* [OAuth 2](#oauth-2)
* [LDAP and Active Directory](#ldap-and-active-directory)
* [Kerberos and Active Directory](#kerberos-and-active-directory)

## Identity Service

Process Services can be configured to authenticate using the [Identity Service]({% link identity-service/1.2/index.md %}).

The Identity Service allows you to configure user authentication between a supported LDAP provider or SAML identity provider and the Identity Service for Single Sign On (SSO) capabilities.

The Identity Service needs to be [deployed]({% link identity-service/1.2/install/index.md %}) and [configured]({% link identity-service/1.2/config/index.md %}) with an identity provider before being set up with other Alfresco products.

Once the Identity Service has been deployed, you will need to [configure Process Services](#properties) to authenticate with it.

>**Note:** Please refer to the [supported platforms]({% link process-services/latest/support/index.md %}) page to see which parts of Process Services are compatible with the Identity Service.

>**Note:** Process Services requires an email address as the user name when logging into the Identity Service.

### Properties

Use this information to configure Process Services to authenticate via Identity Service.

Configure the `activiti-identity-service.properties` file using the below properties:

> **Note:** A [full list of possible properties](https://www.keycloak.org/docs/latest/securing_apps/index.html#_java_adapter_config) is also available.

|Property|Description|
|--------|-----------|
|activiti.identity-service.enabled| *Required.* Enable or disable authentication via the Identity Service. The default value is `false`.|
|activiti.identity-service.realm| *Required.* Name of the realm configured in the Identity Service. The default value is `alfresco`.|
|activiti.identity-service.auth-server-url| *Required.* Base URL of the Identity Service server in the format `http://localhost:8180/auth`.|
|activiti.identity-service.resource| *Required.* The **Client ID** for the client created within your realm that points to Process Services. The default value is `alfresco`.|
|activiti.identity-service.principal-attribute| *Required.* The attribute used to populate the field `UserPrincipal` with. This property needs to be set to `email` to work with Process Services.|
|activiti.identity-service.credentials.secret| *Optional.* The secret key for this client if the access type is not set to `public`.|
|activiti.use-browser-based-logout| *Optional.* Sets whether signing out of Process Services calls the Identity Service `logout URL`. If set to `true`, set the **Admin URL** to `https://{server}:{port}/activiti-app/` under the client settings in the Identity Service management console.|
|activiti.identity-service.cookie-auth-enabled| *Optional.* When set to `true` enables cookie-based authentication that will work alongside the Identity Service authentication.|
|activiti.identity-service.retry.maxAttempts| Sets the maximum number of attempts for retries. The default value is `20`.|
|activiti.identity-service.retry.delay| Sets the delay between the retries. The default value is `10000`.|

#### Renamed properties

Starting from Alfresco Process Services 24.1, as part of replacing the Keycloak adapter with Spring security, the properties prefix changed from `keycloak.*` to `activiti.identity-service.*`. The new property names are:

* `activiti.identity-service.enabled=false`
* `activiti.identity-service.realm=alfresco`
* `activiti.identity-service.auth-server-url=http://localhost:8180/auth`
* `activiti.identity-service.resource=alfresco`
* `activiti.identity-service.principal-attribute=email`
* `activiti.identity-service.credentials.secret=`
* `alfresco.content.sso.enabled=${activiti.identity-service.enabled}`
* `alfresco.content.sso.client_id=${activiti.identity-service.resource}`
* `alfresco.content.sso.client_secret=${activiti.identity-service.credentials.secret}`
* `alfresco.content.sso.realm=${activiti.identity-service.realm}`
* `alfresco.content.sso.auth_uri=${activiti.identity-service.auth-server-url}/realms/${alfresco.content.sso.realm}/protocol/openid-connect/auth`
* `alfresco.content.sso.token_uri=${activiti.identity-service.auth-server-url}/realms/${alfresco.content.sso.realm}/protocol/openid-connect/token`

#### New properties

Here is a list of new properties in Alfresco Process Service 24.1:

* `activiti.identity-service.retry.maxAttempts=20`
* `activiti.identity-service.retry.delay=10000`

#### Removed properties

Starting from Process Services 24.1, as part of replacing the Keycloak adapter with Spring security, the following unused `keycloak.*` properties have been removed:

* `keycloak.ssl-required=none`
* `keycloak.confidential-port=8443`
* `keycloak.public-client=true`
* `keycloak.always-refresh-token=true`
* `keycloak.autodetect-bearer-only=true`
* `keycloak.token-store=session`
* `keycloak.enable-basic-auth=true`

## OAuth 2

To use the OAuth 2 client for authenticating login to the APS web application, you first need to configure it using
the information obtained by the OAuth 2 authorization server.

The following entries show the properties you need to edit in `activiti-app.properties` and how you might set them for a typical configuration.

```text
security.oauth2.authentication.enabled=true
security.oauth2.client.clientId=<client_id>
security.oauth2.client.clientSecret=<secret_key>
security.oauth2.client.userAuthorizationUri=https://github.com/login/oauth/authorize
security.oauth2.client.tokenName=oauth_token
security.oauth2.client.accessTokenUri=https://github.com/login/oauth/access_token
security.oauth2.client.userInfoUri=https://api.github.com/user
```

|Property|Description|
|--------|-----------|
|security.oauth2.authentication.enabled|Enables or disables the OAuth 2 client. To enable the OAuth 2 client, set this property to `true`. To disable it, set this property to `false`.|
|security.oauth2.client.clientId|Client ID provided by the OAuth 2 Authorization server.|
|security.oauth2.client.clientSecret|Client Secret provided by the OAuth 2 Authorization server.|
|security.oauth2.client.checkToken|Configures the OAuth 2 Authorization to be used. Only set this property if you are using an internal authentication server. It contains the authorization URL obtained from the Authorization server. Example: `security.oauth2.client.checkToken=http://localhost:9999/oauth/check_token`|
|security.oauth2.client.userAuthorizationUri|Implementation of the Authorization endpoint from the OAuth 2 specification. Accepts authorization requests, and handles user approval if the grant type is authorization code.|
|security.oauth2.client.tokenName|Name of the token that will be used as parameter in the request.|
|security.oauth2.client.accessTokenUri|Endpoint for token requests as described in the OAuth 2 specification. Once login access to the application on the authorization server has been allowed, the server provides the client (APS application) with the access token. This is exchanged with the authorization server residing on the Uri set within this property.|
|security.oauth2.client.userInfoUri|Uri of the user. This is used to retrieve user details from the authorization server.|

>**Note:** The user name used for Process Services application login should also exist on the external authentication server. Note also that the Process Services user name is an email address.

## LDAP and Active Directory

It’s possible to hook up a centralized user data store with Process Services. Any server supporting the LDAP protocol
can be used. Special configuration options and logic has been included to work with Active Directory (AD) systems too.

From a high-level overview, the external Identity Management (IDM) integration works as follows:

* Periodically, all user and group information is synchronized asynchronously. This means that all data for users (name, email address, group membership and so on) is copied to the Process Services database. This is done to improve performance and to efficiently store more user data that doesn’t belong to the IDM system.

* If the user logs in to Process Services, the authentication request is passed to the IDM system. On successful authentication there, the user data corresponding to that user is fetched from the Process Services database and used for the various requests. Note that no passwords are saved in the database when using an external IDM.

Note that the LDAP sync only needs to be activated and configured on one node in the cluster (but it works when activated on multiple nodes, but this will of course lead to higher traffic for both the LDAP system and the database).

The configuration of the external IDM authentication/synchronization is done in the same way as the regular properties. There is a properties file named `activiti-ldap.properties` in the `WEB-INF/classes/META-INF/` folder in the WAR file. The values in a file with the same name on the classpath have precedence over the default values in the former file.

In addition, in the same folder, the `example-activiti-ldap-for-ad.properties` file contains an example configuration 
for an Active Directory system.

### Server connection

The following code snippet shows the properties involved in configuring a connection to an LDAP server (Active Directory is similar). These are the typical parameters used when connecting with an LDAP server. Advanced parameters are commented out in the example below:

```text
# The URL to connect to the LDAP server
ldap.authentication.java.naming.provider.url=ldap://localhost:10389

# The default principal to use (only used for LDAP sync)
ldap.synchronization.java.naming.security.principal=uid=admin,ou=system

# The password for the default principal (only used for LDAP sync)
ldap.synchronization.java.naming.security.credentials=secret

# The authentication mechanism to use for synchronization
#ldap.synchronization.java.naming.security.authentication=simple

# LDAPS truststore configuration properties
#ldap.authentication.truststore.path=
#ldap.authentication.truststore.passphrase=
#ldap.authentication.truststore.type=
# Set to 'ssl' to enable truststore configuration via subsystem's properties
#ldap.authentication.java.naming.security.protocol=ssl

# The LDAP context factory to use
#ldap.authentication.java.naming.factory.initial=com.sun.jndi.ldap.LdapCtxFactory

# Requests timeout, in miliseconds, use 0 for none (default)
#ldap.authentication.java.naming.read.timeout=0

# See http://docs.oracle.com/javase/jndi/tutorial/ldap/referral/jndi.html
#ldap.synchronization.java.naming.referral=follow
```

It is possible to configure connection pooling for the LDAP/AD connections. This is an advanced feature and is only needed when creating a connection to the IDM system has an impact on system performance.

The connection pooling is implemented using the Spring-LDAP framework. Below are all the properties that it is possible to configure. These follow the semantics of the properties possible for Spring-LDAP and are described [here](http://docs.spring.io/spring-ldap/docs/2.0.2.RELEASE/reference/#pooling){:target="_blank"}.

```text
# -----------------------
# LDAP CONNECTION POOLING
# -----------------------

# Options=
# nothing filled in: no connection pooling
# 'jdk': use the default jdk pooling mechanism
# 'spring': use the spring ldap connection pooling facilities. These can be configured further below
#ldap.synchronization.pooling.type=spring

# Following settings follow the semantics of org.springframework.ldap.pool.factory.PoolingContextSource
#ldap.synchronization.pooling.minIdle=0
#ldap.synchronization.pooling.maxIdle=8
#ldap.synchronization.pooling.maxActive=0
#ldap.synchronization.pooling.maxTotal=-1
#ldap.synchronization.pooling.maxWait=-1
# Options for exhausted action: fail | block | grow
#ldap.synchronization.pooling.whenExhaustedAction=block
#ldap.synchronization.pooling.testOnBorrow=false
#ldap.synchronization.pooling.testOnReturn=false
#ldap.synchronization.pooling.testWhileIdle=false
#ldap.synchronization.pooling.timeBetweenEvictionRunsMillis=-1
#ldap.synchronization.pooling.minEvictableIdleTimeMillis=1800000
#ldap.synchronization.pooling.numTestsPerEvictionRun=3

# Connection pool validation (see http://docs.spring.io/spring-ldap/docs/2.0.2.RELEASE/reference/#pooling for semantics)
# Used when any of the testXXX above are set to true
#ldap.synchronization.pooling.validation.base=
#ldap.synchronization.pooling.validation.filter=
# Search control: object, oneLevel, subTree
#ldap.synchronization.pooling.validation.searchControlsRefs=
```

### Authentication

To enable authentication via LDAP or AD, set the following property:

```text
ldap.authentication.enabled=true
```

In some organizations, a case insensitive log in is allowed with the LDAP ID. By default, this is disabled. To enable, set following property to `false`.

```text
ldap.authentication.casesensitive=false
```

Next, set the following property to specify the user ID pattern for an authenticating LDAP user:

```text
ldap.authentication.dnPattern=uid={0},ou=users,dc=alfresco,dc=com
```

However, if the users are in structured folders (organizational units for example), a direct pattern cannot be used. In this case, leave the property either empty or comment it out. Now, a query will be performed using the `ldap.synchronization.personQuery` (see below) with the `ldap.synchronization.userIdAttributeName` to find the user and their distinguished (DN) name. That DN will then be used to sign in.

When using Active Directory, two additional properties need to be set:

```text
ldap.authentication.active-directory.enabled=true
ldap.authentication.active-directory.domain=alfresco.com
```

The first property enables Active Directory support and the second property is the domain of the user ID (that is, `userId@domain`) to sign in using Active Directory.

If the domain does not match with the `rootDn`, it is possible to set is explicitly:

```text
ldap.authentication.active-directory.rootDn=DC=somethingElse,DC=com
```

And also the filter that is used (which defaults to a `userPrincipalName` comparison) can be changed:

```text
ldap.authentication.active-directory.searchFilter=(&(objectClass=user)(userPrincipalName={0}))
```

The following property can be set to `true` to allow for basic authentication to be used as a fallback for
LDAP authentication. This allows for system or service users to be utilized for certain actions, such as making specific REST API calls:

```text
ldap.allow.database.authenticaion.fallback=true
```

### Synchronization

The synchronization component will periodically query the IDM system and change the user and group database. There are two synchronization *modes*: full and differential.

Full synchronization queries **all** data from the IDM and checks every user, group, and membership to be valid. The resource usage is heavier than the differential synchronization in this type of synchronization and therefore, it is usually only triggered on the very first sync when Process Services starts up and is configured to use an external IDM. This is so that all users and groups are available in the database.

#### Full synchronization

The frequency in which it runs is set using a cron expression:

```text
ldap.synchronization.full.enabled=true
ldap.synchronization.full.cronExpression=0 0 0 * * ?
```

Differential synchronization is *lighter*, in terms of performance, as it only queries the users and groups that have
changed since the last synchronization. One downside is that it cannot detect deletions of users and groups. Consequently, a full synchronization needs to run periodically (but less than a differential synchronization typically) to account for these deletions.

```text
ldap.synchronization.differential.enabled=true
ldap.synchronization.differential.cronExpression=0 0 */4 * * ?
```

Do note that all synchronization results are logged, both in the regular logging and in a database table named `IDM_SYNC_LOG`.

The synchronization logic builds on two elements:

* Queries that return the correct user/group/membership data
* A mapping of LDAP attributes to attributes used within the Process Services system

There are a lot of properties to configure, so do base your configuration on one of the two files in the `META-INF` folder, as these contain default values. You only need to add the specific properties to your custom configuration file if the default values are not appropriate.

#### Generic synchronization settings

These are settings that are generic or shared between user and group objects. For each property, an example setting of a *regular* LDAP system (that is, ApacheDS) and Active Directory is shown.

|Property|Description|
|--------|-----------|
|ldap.synchronization.distinguishedNameAttributeName|The attribute that is the **Disinguished Name** in the system. For example: `dn`. |
|ldap.synchronization.modifyTimestampAttributeName|The name of the **Operational** attribute recording the last update time for a group or user. Important for the differential query. For example in LDAP: `modifyTimestamp` and in AD: `whenChanged`. |
|ldap.synchronization.createTimestampAttributeName|The name of the operational attribute recording the create time for a group or user. Important for the differential query. For example in LDAP: `createTimestamp` and in AD: `whenCreated`. |
|ldap.synchronization.timestampFormat|The timestamp format. This is specific to the directory servers and can vary. For example in LDAP: `yyyyMMddHHmmss.SSS’Z'` and in AD: `yyyyMMddHHmmss'.0Z'`. |
|ldap.synchronization.timestampFormat.locale.language|The timestamp format locale language for parsing. Follows the `java.util.Locale semantics` For example: `en`. |
|ldap.synchronization.timestampFormat.locale.country|The timestamp format locale country. Follows the `java.util.Locale` semantics. For example: `GB`. |
|ldap.synchronization.timestampFormat.timezone|The timestamp format timezone. Follows the `java.text.SimpleDateFormat` semantics. For example: `GMT`. |

#### User synchronization settings

|Property|Description|
|--------|-----------|
|ldap.synchronization.users.ignoreCase|If this property is set to `true` then the synchronization will ignore the case that users are stored in within the source database when syncing users.|
|ldap.synchronization.userSearchBase|The user search base restricts the LDAP user query to a sub section of a tree on the LDAP server. For example: `ou=users,dc=alfresco,dc=com`. |
|ldap.synchronization.syncAdditionalUsers|Set to `true` if users outside of the `userSearchBase` but included in the `groupSearchBase` should be synchronized.|
|ldap.synchronization.personQuery|The query to select all objects that represent the users to import (used in the **Full Synchronization Query**). For example in LDAP: `(objectclass\=inetOrgPerson)` and in AD: `(&(objectclass\=user)(userAccountControl\:1.2.840.113556.1.4.803\:\=512))`|
|ldap.synchronization.personDifferentialQuery|The query to select objects that represent the users to import that have changed since a certain time (used in the **Differential Synchronization Query**).|
|ldap.synchronization.userIdAttributeName|The attribute name on people objects found in LDAP to use as the user ID in Alfresco. For example in LDAP: `uid` and in AD: `cn`. |
|ldap.synchronization.userFirstNameAttributeName|The attribute on person objects in LDAP to map to the first name property of a user. For example: `givenName`. |
|ldap.synchronization.userLastNameAttributeName|The attribute on person objects in LDAP to map to the last name property of a user. For example in LDAP: `sn` and in AD: `cn`. |
|ldap.synchronization.userEmailAttributeName|The attribute on person objects in LDAP to map to the email property of a user. For example: `mail`. |
|ldap.synchronization.userType|The person type in the directory server. For example in LDAP: `inetOrgPerson` and in AD: `user`. |
|ldap.synchronization.activate.users|Determines if users should be activated during synchronization.<br><br>Possible values: <br><br>- `NONE`: No users will be activated during LDAP synchronization (default).<br>- `APP`: Only users that have been deactivated through the APS UI will be activated.<br>- `LDAP`: Only users that have been deactivated in a previous LDAP synchronization will be activated.<br> - `ANY`: Activates all users regardless of the way they were deactivated before.<br><br>The default value is `NONE`. <br><br>Added in Process Services 24.1.|

You can configure which users should be made administrators in the system. Delimit multiple entries with a `;` (semi-colon) as commas can’t be used.

>**Note**: No trimming of spaces will be applied and the property value must be an exact string match to the user DN value not an LDAP/AD query string.

```text
ldap.synchronization.tenantAdminDn=uid=joram,ou=users,dc=alfresco,dc=com;uid=tijs,ou=users,dc=alfresco,dc=com
```

When using multi-tenancy, the administrator of all tenants can be configured as follows. Similar rules for delimiting apply as above.

>**Note:** The property value must be an exact string match to the user DN value not an LDAP/AD query string.

```text
ldap.synchronization.tenantManagerDn=uid=joram,ou=users,dc=alfresco,dc=com
```

It’s important to set at least `1` user with admin rights. Otherwise no user will be able to sign into the system and administer it.

#### Group synchronization settings

|Property|Description|
|--------|-----------|
|ldap.synchronization.groupSearchBase|The group search base restricts the LDAP group query to a sub section of a tree on the LDAP server. For example: `ou=groups,dc=alfresco,dc=com`. |
|ldap.synchronization.groupQuery|The query to select all objects that represent the groups to import (used in **Full Synchronization**). For example in LDAP: `(objectclass\=groupOfNames)` and in AD: `(objectclass\=group)`. |
|ldap.synchronization.groupDifferentialQuery|The query to select objects that represent the groups to import that have changed since a certain time (used in the **Differential Synchronization**).|
|ldap.synchronization.groupIdAttributeName|The attribute on LDAP group objects to map to the authority name property in Process Services. For example: `cn`. |
|ldap.synchronization.groupMemberAttributeName|The attribute in LDAP on group objects that defines the DN for its members. This is an important setting as is defines **group memberships** of users and **parent-child** relations between groups. For example: `member`. |
|ldap.synchronization.groupType|The group type in LDAP. For example in LDAP: `groupOfNames` and in AD: `group`. |

#### Add users to an LDAP group

Active Directory sets a limit on the number of attributes stored in a group that are retrievable in a single query. To overcome this, you can use incremental retrieval of data. This involves limiting the number of attribute values in
a single query. To reduce the number of times the query is required to contact the server, set the number of values requested as close, as possible, to the maximum.

Process Services provides the capability to configure the number of group members retrieved per query subject to the limitations imposed by Active Directory. Follow these steps to enable this:

1. Open the `<InstallLocation>/tomcat/webapps/activiti-app/WEB-INF/classes/META-INF/activiti-app/activiti-ldap.properties` file.
2. Set the following property to `true`.

    ```text
    ldap.synchronization.groupMemberRangeEnabled=true
    ```

3. Set the maximum number of members to retrieve in a single query.

    ```text
    ldap.synchronization.groupMemberRangeSize=1500
    ```

    >**Note:** This value should not exceed the limit set by Active Directory. If this is greater than the Active Directoy limit, no members are returned. See [https://msdn.microsoft.com/en-us/library/ms676302(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/ms676302(v=vs.85).aspx){:target="_blank"} for information related to the maximum number of values returned in a single query in Active Directory. For further information regarding the behavior of the range attribute see [https://msdn.microsoft.com/en-us/library/ms676302(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/ms676302(v=vs.85).aspx){:target="_blank"}.

>**Note:** If you set the enablement property to `true`, the default value for `ldap.synchronization.groupMemberRangeSize` is set to `1000`.

#### Paging

It is possible to use paging when connecting to an LDAP server (some even mandate this).

To enable paging when fetching users or groups, set following properties:

```text
ldap.synchronization.paging.enabled=true
ldap.synchronization.paging.size=500
```

By default, paging is disabled.

#### Batch insert

It is possible to tweak the *batch size* when doing an LDAP sync.

The *insert* batch size limits the amount of data being inserted in one transaction (for example, 100 users per transactions are inserted).By default, this is 5. The *query* batch size is used when data is fetched from the Process Services database (for example, fetching users to check for deletions when doing a full sync).

```text
ldap.synchronization.db.insert.batch.size=100
ldap.synchronization.db.query.batch.size=100
```

## Kerberos and Active Directory

Process Services support for Kerberos SSO allows customers with existing Kerberos AD infrastructure to quickly and easily set up Windows-based SSO for their users’ access. It’s established as a security standard in many organizations and does not require additional infrastructure. It allows users secure access to the Process Services app (`activiti-app`) without explicit login through a web browser.

You must first set up accounts for use on a Microsoft Active Directory domain controller. It is important to identify each of the servers in your cluster that will be running the Process Services (`activiti-app.war`) web application.
These instructions also apply to simple non-clustered installations, where a single `activiti-app.war` runs on a single host.

These instructions use the following naming conventions for the example server, `server1.alfresco.org`:

* `<host>` is the server host name (without domain name suffix). For example, `server1`.
* `<hostnetbios>` is the resolved value of the `cifs.serverName` property if the server is part of the Active Directory domain (typically the host name with the letter 'A' appended) or the host name otherwise (without domain name suffix). For example, `server1A`.
* `<domain>` is the DNS domain. For example, `alfresco.org`.
* `<domainnetbios>` is the Windows domain NetBIOS name. For example, `alfresco`.
* `<REALM>` is t he DNS domain in upper case. For example, `ALFRESCO.ORG`.

### Prerequisites

You must ensure that you have configured LDAP (LDAP synchronization in particular). You can use Kerberos SSO in combination with LDAP authentication and also database authentication. You can use both of these as fallback scenarios in the case that the user's browser does not support Kerberos authentication.

### Configuration steps

Kerberos SSO configuration can be divided into three parts:

* (1) Steps to configure Active Directory and are performed by an Administrator against the domain controllers
* (2) Steps to configure the machine where Process Services is hosted (for example, creating the `krb5.ini` file)
* (3) Steps to set configuration properties

1. Create accounts for the SSO authentication filters by repeating the following steps for each server in the cluster that will be running the activiti-app.war file.

    1. In the Active Directory Users and Computers application, choose **Action > New > User**, then enter the full name as HTTP <host> and the user log in name as http<host>.

    2. Click **Next**.

    3. Enter a password.

    4. Enable **Password never expires** and disable **User must change password at next logon**.

    5. Click **Next**.

    6. Click **Finish**.

    7. Right-click the new user account name, and then select **Properties**.

    8. Select the **Account** tab and enable the **Do not require Kerberos preauthentication** option in the **Account Options** section.

    9. From the command prompt, use the `ktpass` utility to generate key tables for this account as shown:

        ```bash
        ktpass -princ HTTP/<host>.<domain>@<REALM> -pass <password> -mapuser 
        <domainnetbios>\http<host> -crypto all -ptype KRB5_NT_PRINCIPAL -out 
        c:\temp\http<host>.keytab -kvno 0
        ```

    10. Create the Service Principal Names (SPN) for the account using the `setspn` utility.

        ```bash
        setspn -a HTTP/<host> http<host>
        setspn -a HTTP/<host>.<domain> http<host>
        ```

        >**Note:** When configuring Kerberos on a cluster through a load balancer, use the proxy name as the Service Principal Names (SPN).

    11. In the Active Directory Users and Computers application, right click on the `http<host>` user and select **Properties**.

    12. Select the **Delegation** tab. If you cannot see the **Delegation** tab, do one or both of the following:

        * Check that you ran the specified `setspn` command correctly. Delegation is only intended to be used by service accounts, which should have registered SPNs, as opposed to a regular user account which typically does not have SPNs.
        * Raise the functional level of your domain to Windows Server 2012 R2 x64. To do this:
            * Open **Active Directory Domains and Trusts**.
            * In the console tree, right-click the applicable domain and then click **Raise Domain Functional Level**.
            * In **Select an available domain functional level**, click **Windows Server 2012**, and then click **Raise**.

    13. In the user **Delegation** tab, select the **Trust this user for delegation to any service (Kerberos only)** check box.

    Copy the key table files created in steps 1 and 2 to the servers they were named after. Copy the files to a protected area, such as `C:\etc\` or `/etc`.

2. On each server in the cluster that will be running the APS web application (`activiti-app.war`), repeat the following steps:

    1. Set up the Kerberos ini file to point to the Windows domain controller.

        The default location is `%WINDIR%\\krb5.ini`, where `%WINDIR%` is the location of your Windows directory, for example, `C:\Windows\krb5.ini`. If the file does not already exist (for example, if the Kerberos libraries are not installed on the target server), you must copy these over or create them from scratch. See [Kerberos Help](http://web.mit.edu/kerberos/krb5-1.12/doc/admin/conf_files/krb5_conf.html) for more information on the `krb5.conf` file. In this example, our Windows domain controller host name is `adsrv.alfresco.org`.

        ```text
        [libdefaults]
        default_realm = ALFRESCO.ORG
        default_tkt_enctypes = rc4-hmac
        default_tgs_enctypes = rc4-hmac

        [realms]
        ALFRESCO.ORG = {
           kdc = adsrv.alfresco.org
           admin_server = adsrv.alfresco.org
        }

        [domain_realm]
        adsrv.alfresco.org = ALFRESCO.ORG
        .adsrv.alfresco.org = ALFRESCO.ORG
        ```

        >**Note:** Specify the realm in uppercase.

        The Kerberos ini file for Linux is `/etc/krb5.conf`.

    2. Set up the Java login configuration file.

        For JBoss, open the `$JBOSS_HOME/standalone/configuration/standalone.xml` file.

        In the `<subsystem xmlns="urn:jboss:domain:security:1.2">` section, add the following:

        ```xml
        <security-domain name="alfresco" cache-type="default">  
            <authentication>  
                  <login-module code="com.sun.security.auth.module.Krb5LoginModule" flag="sufficient"/>  
            </authentication>  
        </security-domain> 
        ```

        Add the following security-domain sections:

        ```xml
        <security-domain name="AlfrescoHTTP" cache-type="default">
        	<authentication>
        			<login-module code="com.sun.security.auth.module.Krb5LoginModule" flag="required">
        			   <module-option name="debug" value="true"/>
        			   <module-option name="storeKey" value="true"/>
        			   <module-option name="useKeyTab" value="true"/>
        			   <module-option name="doNotPrompt" value="true"/>
        			   <module-option name="isInitiator" value="false"/>
        			   <module-option name="keyTab" value="C:/etc/http<host>.keytab"/>
        			   <module-option name="principal" value="HTTP/<host>.<domain>"/>
        			</login-module>
        	</authentication>
        </security-domain>
        ```

        For other environments, in the Java security folder (for example, `C:\Alfresco\java\lib\security`), create a file named `java.login.config` with entries as shown below.

        ```text
        Alfresco {
           com.sun.security.auth.module.Krb5LoginModule sufficient;
        };

        AlfrescoHTTP
        {
           com.sun.security.auth.module.Krb5LoginModule required
           storeKey=true
           useKeyTab=true
           doNotPrompt=true
           keyTab="C:/etc/http<host>.keytab"
           principal="HTTP/<host>.<domain>";
        };

        com.sun.net.ssl.client {
           com.sun.security.auth.module.Krb5LoginModule sufficient;
        };

        other {
           com.sun.security.auth.module.Krb5LoginModule sufficient;
        };
        ```

    3. Enable the login configuration file by adding the following line to the main Java security configuration file, usually at `java\lib\security\java.security`.

        ```text
        login.config.url.1=file:${java.home}/lib/security/java.login.config
        ```

    4. If the Process Services server is not part of the Active Directory domain, ensure that its clock is kept in sync with the domain controller's, for example, by configuring the domain controller as an NTP server.

3. To complete Kerberos SSO enablement, perform the following configuration steps after completing the actions described in step 1 and step 2 above:

    >**Note:** Use the same server as that used in part 2 of Kereberos SSO configuration to carry out these steps.

    1. Open the `<InstallLocation>/tomcat/lib/activiti-ldap.properties` file.

        >**Note:** You will need to create this file if it does not already exist.

    2. Specify the configuration settings listed in the table below.

    |Property name|Description|
    |-------------|-----------|
    |kerberos.authentication.enabled|A switch for activating functionality for Kerberos SSO authentication. This applies to both the APS user interface and the REST API. The default value is `FALSE`. |
    |kerberos.authentication.principal|The Service Principal Name (SPN). For example, `HTTP/alfresco.test.activiti.local`.|
    |kerberos.authentication.keytab|The file system path to the key table file. For example, `C:/alfresco/alfrescohttp.keytab`.|
    |kerberos.authentication.krb5.conf|The file system path to the local server. For example, `C:/Windows/krb5.ini`.|
    |kerberos.allow.ldap.authentication.fallback|Determines whether to allow login for unsupported client browsers using LDAP credentials. The default value is `FALSE`. |
    |kerberos.allow.database.authentication.fallback|Determines whether to allow login for unsupported client browsers using database credentials. The default value is `FALSE`. |
    |kerberos.allow.samAccountName.authentication|Authentication of the user id using the short form (for example username instead of username@domain.com). The default value is `FALSE`. |
    |security.authentication.use-externalid|A setting that enables the use of Kerberos authentication. The default value is `FALSE`. |
---
title: Configure content systems
---

You can connect Process Services to external content systems and publish content as part of a process. With Alfresco Content Services it is also possible to retrieve and update content, as well as invoke certain repository actions.

Process Services can connect to the following content systems:

* [Alfresco Content Services](#content-services)
* [Box](#box)
* [Google Drive](#google-drive)

Content that is uploaded as part of a task or process can be stored in a [file system](#file-system) or [Amazon S3](#amazon-s3).

## Content Services

An Alfresco Content Services connection allows for content to be uploaded to a Content Services repository as part of a Process Services form or using a Publish to Alfresco task in a process.

It is also possible to retrieve and update content properties in a Content Services repository as well as invoking content actions as part of a process using the following BPMN elements:

* Publish to Alfresco
* Retrieve Alfresco properties
* Update Alfresco properties
* Call Alfresco Action

There are three ways to configure a connection to Content Services:

* [Using the Identity Service to configure Single Sign On (SSO)](#configure-a-connection-using-single-sign-on)
* [Using basic authentication](#configure-a-connection-using-basic-authentication)
* [Using the Share Connector]({% link process-services/latest/using/share-connector.md %})

### Configure a connection using Single Sign On

A Content Services connection to Process Services can be created using the Identity Service so that communication between the two systems is achieved using tokens instead of stored credentials. You need the following:

* Content Services version 6.1.1 or later.
* The Identity Service configured between Process Services and Content Services.
* The properties are configured in `activiti-identity-service.properties` for SSO.

Configuring the Alfresco Repository location:

1. Sign into Process Services as an administrator.
2. Navigate to **Identity Management > Tenants > Alfresco Repositories**.
3. Add a new repository or edit an existing connection.
4. Configure the following settings for the repository connection:

    |Setting|Description|
    |-------|-----------|
    |Name|A name for the repository connection.|
    |Alfresco tenant|The tenant to create the repository under.|
    |Repository base URL|The base URL of the repository instance to connect to.|
    |Share base URL|The base URL of Share for the repository instance to connect to.|
    |Alfresco version|The version of Content Services to connect to. This must be version 6.1.1 or later to use SSO.|
    |Authentication type|The authentication type of the connection. Select **Identity Service authentication** to use SSO.|

Authenticate users for Alfresco Repository communication:

After a repository connection has been configured to use SSO users need to authorize their Content Services credentials for use by Process Services by doing the following:

1. Sign into Process Services.
2. Navigate to **Identity Management > Personal**
3. Select the **Authorize** button against the **Alfresco Repository** configured for SSO.

>**Note:** If a repository **Authentication type** is changed then users are required to reauthorize their credentials for it.

>**Note**: If a user's authorization token expires whilst they have Content Services tasks assigned to them they will stay in a pending state until the user reauthorizes against the repository.

The following properties need to be set in the `activiti-identity-service.properties` file to connect to Content Services using SSO:

>**Note:** Many of the following properties to configure SSO with Content Services use [Identity Service properties]({% link process-services/latest/config/authenticate.md %}#identity-service) as their default values.

|Property|Description|
|--------|-----------|
|alfresco.content.sso.enabled|Sets whether SSO is enabled between Process Services and Content Services. For example `${activiti.identity-service.enabled}`. |
|alfresco.content.sso.client_id|The **Client ID** within the realm that points to Process Services. For example `${activiti.identity-service.resource}`. |
|alfresco.content.sso.client_secret|The secret key for the Process Services client. For example `${activiti.identity-service.credentials.secret}`. |
|alfresco.content.sso.realm|The realm that is configured for the Content Services and Process Services clients. For example `${activiti.identity-service.realm}`. |
|alfresco.content.sso.scope|Sets the duration that tokens are valid for. For example using the value`offline_access` a token is valid even after a user logs out as long as the token is used at least once every 30 days. See the [Keycloak documentation](https://www.keycloak.org/docs/latest/server_admin/#_offline-access){:target="_blank"} for further information. |
|alfresco.content.sso.javascript_origins|The base URL for the Javascript origins of the Process Services instance. For example `http://localhost:9999`. |
|alfresco.content.sso.auth_uri|The authorization URL. For example `${activiti.identity-service.auth-server-url}/realms/${alfresco.content.sso.realm}/protocol/openid-connect/auth`. |
|alfresco.content.sso.token_uri|The authorization token URL. For example `${activiti.identity-service.auth-server-url}/realms/${alfresco.content.sso.realm}/protocol/openid-connect/token`. |
|alfresco.content.sso.redirect_uri|The redirect URI for authorization. The value in the example column needs to be updated with the correct base URL for the Process Services instance. For example `http://localhost:9999/activiti-app/rest/integration/sso/confirm-auth-request`. |

### Configure a connection using basic authentication

A Content Services connection to Process Services can be created using basic authentication. A user's credentials for Content Services will be stored encrypted in Process Services.

The following properties need to be set in `activiti-app.properties` to encrypt Content Services user credentials:

|Property|Description|
|--------|-----------|
|security.encryption.ivspec|A 128-bit initialization vector to encrypt credentials using AES/CBC/PKCS5PADDING. This will be 16 characters long.|
|security.encryption.secret|A 128-bit secret key to encrypt credentials using AES/CBC/PKCS5PADDING. This will be 16 characters long.|

Configuring the Alfresco Repository location:

1. Sign into Process Services as an administrator.
2. Navigate to **Identity Management > Tenants > Alfresco Repositories**.
3. Add a new repository or edit an existing connection.
4. Configure the following settings for the repository connection:

    |Setting|Description|
    |-------|-----------|
    |Name|A name for the repository connection.|
    |Alfresco tenant|The tenant to create the repository under.|
    |Repository base URL|The base URL of the repository instance to connect to.|
    |Share base URL|The base URL of Share for the repository instance to connect to.|
    |Alfresco version|The version of Alfresco Content Services to connect to.|
    |Authentication type|The authentication type of the connection. Select **Default authentication** to use basic authentication.|

Authenticate users for Alfresco Repository communication:

After a repository connection has been configured for basic authentication, users need to enter their Content Services credentials for use by Process Services by doing the following:

1. Sign into Process Services.
2. Navigate to **Identity Management > Personal**
3. Click the **Alfresco Repository** configured for basic authentication.
4. Enter their Alfresco Content Services user name and password.

## Box

A Box connection allows for content to be uploaded to Box as part of a Process Services form or using a Publish to Box task in a process.

A [Box developer account](https://developers.box.com){:target="_blank"} is required to setup a connection to Box.

The following properties need to be set in the `activiti-app.properties` file to enable Box connections to be used in Process Services:

|Property|Description|
|--------|-----------|
|box.disabled|Set this to `false` to enable Box connections to be configured in forms and processes. |
|box.web.auth_uri|Set this to the value provided in the example column to configure the Box authentication URI. For example `https://app.box.com/api/oauth2/authorize`. |
|box.web.token_uri|Set this to the value provided in the example column to configure the Box token URI. For example `https://app.box.com/api/oauth2/token`. |
|box.web.redirect_uris|Update the base of the URL provided in the example column to reflect your Process Services installation. For example `http://localhost:8080/activiti-app/app/rest/integration/box/confirm-auth-request`. |
|box.web.javascript_origins|Sets the base URL of Javascript origins. For example `http://localhost:8080/activiti-app`.|
|box.web.client_id|The client ID obtained from your Box developer account.|
|box.web.client_secret|The client secret obtained from your Box developer account.|

## Google Drive

A Google Drive connection allows for content to be uploaded to Google Drive as part of a Process Services form or using a publish to Google Drive task in a process.

A [Google developer account](https://developers.google.com/drive/v2/reference/){:target="_blank"} is required to setup a connection to Google Drive.

The following properties need to be set in the `activiti-app.properties` file to enable Google Drive connections to be used in Process Services:

|Property|Description|
|--------|-----------|
|googledrive.web.disabled|Set this to `false` to enable Google Drive connections to be configured in forms and processes. |
|googledrive.web.auth_uri|Set this to the value provided in the example column to configure the Google Drive authentication URI. For example `https://accounts.google.com/o/oauth2/auth`. |
|googledrive.web.token_uri|Set this to the value provided in the example column to configure the Google Drive token URI. For example `https://accounts.google.com/o/oauth2/token`. |
|googledrive.web.auth_provider_x509_cert_url|Set this to the value provided in the example column to configure the Google Drive x509 certificate URL. For example `https://www.googleapis.com/oauth2/v1/certs`. |
|googledrive.web.redirect_uris|Update the base of the URL provided in the example column to reflect your Process Services installation. For example `http://localhost:8080/activiti-app/app/rest/integration/google-drive/confirm-auth-request`. |
|googledrive.web.javascript_origins|Sets the base URL of Javascript origins. For example `http://localhost:8080/activiti-app`. |
|googledrive.web.client_id|The client ID obtained from your Google developer account.|
|googledrive.web.client_secret|The client secret obtained from your Google developer account.|
|googledrive.web.client_email|The client email associated to your Google developer account.|
|googledrive.web.client_x509_cert_url|The client x509 certificate URL obtained from your Google developer account.|

## Content storage

Process Services enables you to upload content, such as attaching a file to a task or a form.

Content can be stored locally by setting the property below to `fs`. Alternatively, you can use Amazon S3 for 
content storage by setting it to `s3`.

```text
contentstorage.type
```

### File system

To configure file system for content storage, set the following properties in the `activiti-app.properties` file:

>**Note:** Please note that the property file located at `tomcat/lib/activiti-app.properties` has priority over the one found at `/tomcat/webapps/activiti-app/WEB-INF/classes/META-INF/activiti-app.properties`.

|Property|Description|
|--------|-----------|
|contentstorage.fs.rootFolder|Name and location of the root folder. **Important:** When using multiple instances of the application, make sure that this path references a shared network drive. This is so that all nodes are able to access all content as the application is stateless and any server can handle any request. For example `/data`. |
|contentstorage.fs.createRoot|Sets whether the root folder is created by default. For example `true`. |
|contentstorage.fs.depth|Depth of the folder tree. For example `4`. |
|contentstorage.fs.blockSize|Maximum number of files in a single folder. For example `1024`.|

### Amazon S3

To configure Amazon S3 for content storage, set the following properties in the `activiti-app.properties` file:

|Property|Description|
|--------|-----------|
|contentstorage.s3.accessKey|Set to the S3 access key. The access key is required to identify the Amazon Web Services account and can be obtained from the Amazon Web Services site [AWS Credentials](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html).|
|contentstorage.s3.secretKey|Set to the S3 secret key.The secret key is required to identify the Amazon Web Services account and can be obtained from the Amazon Web Services site [AWS Credentials](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html).|
|contentstorage.s3.bucketName|Set to the S3 bucket name.The bucket name must be unique among all Amazon Web Services users globally. If the bucket does not already exist, it will be created, but the name must not have already been taken by another user. See [S3 bucket restrictions](http://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html) for more information on bucket naming.|
|contentstorage.s3.objectKeyPrefix|Set to your AWS object prefix.|
---
title: Database configuration
---

Set the following properties to update the database properties.

## JDBC connection

Set the following properties to configure a JDBC connection:

|Property|Description|
|--------|-----------|
|datasource.driver|The JDBC driver used to connect to the database. Note that the driver must be on the classpath of the web application.|
|datasource.url|The JDBC URL used to connect to the database.|
|datasource.username|The user of the database system that is used to connect to the database.|
|datasource.password|The password of the above user.|

Example:

```text
com.mysql.cj.jdbc.Driver
datasource.url=jdbc:mysql://127.0.0.1:3306/activiti?characterEncoding=UTF-8

datasource.username=alfresco
datasource.password=alfresco
```

### Connection pooling

When using JDBC Connection Parameters, you can configure the following connection pool settings 
to suit the anticipated load:

|Property|Description|
|--------|-----------|
|datasource.min-pool-size|The minimum number of connections in the connection pool. For example `5`. |
|datasource.max-pool-size|The maximum number of connections in the connection pool. For example `100`. |
|datasource.acquire-increment|The number of additional connections the system will try to acquire each time the connection pool is exhausted. For example `5`. |
|datasource.preferred-test-query|The query used to verify that the connection is still valid. The value depends on the database: `select 1` for H2, MySQL, PostgreSQL and Microsoft SQL Server, `SELECT 1 FROM DUAL` for Oracle and `SELECT current date FROM sysibm.sysdummy1` for DB2.|
|datasource.test-connection-on-checkin|Boolean value. If `true`, an operation will be performed asynchronously on every connection checkin to verify that the connection is valid. For best performance, a proper `datasource.preferred-test-query` should be set.|
|datasource.test-connection-on-checkout|Boolean value. If `true`, an operation will be performed asynchronously on every connection checkout to verify that the connection is valid. Testing Connections on checkout is the simplest and most reliable form of Connection testing. For best performance, a proper `datasource.preferred-test-query` should be set.|
|datasource.max-idle-time|The number of seconds a connection can be pooled before being discarded. For example `1800`. |
|datasource.max-idle-time-excess-connections|Number of seconds that connections in excess of `minPoolSize` should be permitted to remain idle in the pool before being discarded. The intention is that connections remain in the pool during a load spike. For example `1800`. |

The connection pooling framework used is [C3P0](http://www.mchange.com/projects/c3p0/){:target="_blank"}. It has extensive documentation on the settings described above.

## JNDI data source

If a JNDI data source is configured in the web container or application server, the JNDI name should be set with the following properties:

|Property|Description|
|--------|-----------|
|datasource.jndi.name|The JNDI name of the datasource. This varies depending on the application server or web container. For example `jdbc/activitiDS`. |
|datasource.jndi.resourceRef|Set whether the look up occurs in a J2EE container, that is, if the prefix `java:comp/env/` needs to be added if the JNDI name doesn’t already contain it. For example `true`. |

Example (on JBoss EAP 6.3):

```text
datasource.jndi.name=java:jboss/datasources/activitiDS
```

## Hibernate settings

The Process Services specific logic is written using JPA 2.0 with Hibernate as implementation. Note that the Process Engine itself uses [MyBatis](http://mybatis.github.io/mybatis-3/){:target="_blank"} for full control of each SQL query.

Set the following properties.

|Property|Description|
|--------|-----------|
|hibernate.dialect| *Required.* The dialect implementation that Hibernate uses. This is database specific.|

The following values are used to test Process Services.

|Database|Dialect|
|--------|-------|
|H2|`org.hibernate.dialect.H2Dialect`|
|MySQL|`org.hibernate.dialect.MySQLDialect`|
|Oracle|`org.hibernate.dialect.Oracle10gDialect`|
|SQL Server|`org.hibernate.dialect.SQLServerDialect`|
|DB2|`org.hibernate.dialect.DB2Dialect`|
|PostgreSQL|`org.hibernate.dialect.PostgreSQLDialect`|

Optionally, the `hibernate.show_sql` property can be set to `true` if the SQL being executed needs to be printed to the log.

>**Note:** You will need to research the exact dialect for your exact version of database as it may differ from what was used to test Process Services.
---
title: Configure external integrations
---

The external systems that can be integrated with Process Services are:

* [Email server](#email-server)
* [Elasticsearch](#elasticsearch)
* [Microsoft Office](#microsoft-office)

## Email Server

The application sends out emails to users on various events. For example, when a task is assigned to the user.

Set the following properties to configure the email server:

|Property|Description|
|--------|-----------|
|email.enabled|Enables or disables the email functionality as a whole. By default, it is set to `false`, therefore make sure to set it to `true` when you require the email functionality.|
|email.host|The host address of the email server.|
|email.port|The port on which the email server is running.|
|email.useCredentials|Boolean value. Indicates if the email server needs credentials to make a connection. If so, both username and password need to be set.|
|email.username|The username used as credentials when `email.useCredentials` is `true`.|
|email.password|The password used as credentials when `email.useCredentials` is `true`.|
|email.ssl|Defines if SSL is needed for the connection to the email server.|
|email.tls|Defines if TLS is needed for the connection to the email server. This needs to be `true` when Google mail is used as the mail server for example.|
|email.from.default|The email address that is used in the `from` field of any email sent.|
|email.from.default.name|The name that is used in the `from` field of the email sent.|
|email.feedback.default|Some emails will have a feedback email address that people can use to send feedback. This property defines this.|

Emails are created by a template engine. The emails can contain various links to the runtime system to bring the 
user straight to the correct page in the web application.

Set the following property to correct the links. The example in the following table uses `localhost` as host address 
and `/activiti-app` as the context root:

|Property|Example|
|--------|-------|
|email.base.url|[http://localhost:8080/activiti-app](http://localhost:8080/activiti-app)|

## Elasticsearch

Elasticsearch is used in Process Services as a data store for generating analytics and reports. [Elasticsearch](http://www.elasticsearch.org/){:target="_blank"} is an open source data store for [JSON](http://www.json.org/){:target="_blank"} documents. Its main features include fast full text search and analytics.

Process Services uses a REST connection to communicate with a remote instance of Elasticsearch. The application creates a Java Low Level REST client, which allows you to configure Process Services to index event data into a remote Elasticsearch service. The REST client internally uses the Apache HTTP Async Client to send HTTP requests. This allows communication with an Elasticsearch cluster through HTTP.

A REST connection between Elasticsearch and Process Services has three points to be aware of:

* REST operations made using the native transport protocol are not supported. The Elasticsearch service exposes only the REST API and not the transport protocol. Operations must therefore be run across an HTTP connection.
* No data is stored on the server on which the application is running. The data fully resides within the Elasticsearch cluster in the remote environment.
* In multi-tenant setups, four indexes are created per tenant.

For more details regarding the REST client, see [Java Low Level REST Client](https://www.elastic.co/guide/en/elasticsearch/client/java-rest/current/java-rest-low.html){:target="_blank"}.

If migrating from an embedded Elasticsearch instance, see [rebuilding Elasticsearch instances](#rebuild-indexes) after configuring a connection to an external Elasticsearch instance via REST.

For information about the compatibility between the REST client and the remote Elasticsearch cluster environment, see [Communicating with an Elasticsearch Cluster using HTTP](https://www.elastic.co/guide/en/elasticsearch/client/java-rest/current/_motivations_around_a_new_java_client.html){:target="_blank"}.

### Properties

The following properties need to be configured in `activiti-app.properties` for Elasticsearch:

|Property|Description|
|--------|-----------|
|elastic-search.server.type|The server type for Elasticsearch configuration. Set this to **rest** to enable the REST client implementation.|
|elastic-search.rest-client.port|The port running Elasticsearch, for example `9200`. |
|elastic-search.rest-client.connect-timeout|Connection timeout for the REST client, for example `1000`. |
|elastic-search.rest-client.socket-timeout|Socket timeout for the REST client, for example `5000`. |
|elastic-search.rest-client.address|IP address of the REST client, for example `localhost`. |
|elastic-search.rest-client.schema|Sets whether the connection uses http or https, for example `http`. |
|elastic-search.rest-client.auth.enabled|Sets whether authentication is enabled for the REST connection, for example `false`|
|elastic-search.rest-client.username|The username of the Elasticsearch user, for example `admin`.|
|elastic-search.rest-client.password|The password for the Elasticsearch user, for example `esadmin`. |
|elastic-search.rest-client.keystore|The keystore used to encrypt the connection to the Elasticsearch instance.|
|elastic-search.rest-client.keystore.type|The type of keystore used for encryption, for example `jks`. |
|elastic-search.rest-client.keystore.password|The password of keystore used for encryption.|
|elastic-search.default.index.name|The default prefix for the default tenant, for example `activiti`. |
|elastic-search.tenant.index.prefix|The prefix used for indexing in multi-tenant setups, for example `activiti-tenant-`. |

Backing up the data stored in Elasticsearch is described in detail in the [Elastic search documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-snapshots.html){:target="_blank"}. When using the **snapshot** functionality of ElasticSearch, you must enable the HTTP interface and create firewall
rules to prevent the general public from accessing it.

### Event processing for analytics

The main concept of event processing is depicted in the following diagram.

![analytics-event-processing]({% link process-services/images/analytics-event-processing.png %})

1. The Process Engine is configured to generate events related to process execution (for example, processes started, task completed, and so on). These events are stored in the database such that there is no problem with database transactions. Meaning, writing the events to the database succeeds or fails with the regular process execution data.
2. A component called **event processor** will asynchronously check for new entries in the database table for the events. The events will be processed and transformed to JSON.
3. The JSON event is asynchronously sent to Elasticsearch. From that point on the data will show up in the reports.

The event processor is architected to work without collisions in a multi-node clustered setup. Each of the event processors will first try to lock events before processing them. If a node goes down during event processing (after locking), an **expired events processor** component will pick them up and process them as regular events.

The event processing can be configured, however leaving the default values as they are helps cater for typical scenarios.

|Property|Description|
|--------|-----------|
|event.generation.enabled|Set to false if no events need to be generated. Do note that the reporting/analytics event data is then lost forever. The default value is `true`. |
|event.processing.enabled|Set to false to not do event processing. This can be useful in a clustered setup where only some nodes do the processing. The default value is `true`. |
|event.processing.blocksize|The number of events that are attempted to be locked and fetched to be processed in one transaction. Larger values equate to more memory usage, but less database traffic. The default value is `100`. |
|event.processing.cronExpression|The cron expression that defines how often the events generated by the Process Engine are processed (that is, read from the database and fed into Elastic Search). By default 30 seconds. If events do not need to appear quickly in the analytics, it is advised to make this less frequent to put less load on the database. The default value is `0/30 \* \* \* \* ?`. |
|event.processing.expired.cronExpression|The cron expression that defines how often **expired** events are processed. These are events that were locked, but never processed (such as when the node processing them went down). The default value is `0 0/30 \* \* \* ?`. |
|event.processing.max.locktime|The maximum time an event can be **locked** before it is seen as expired. After that it can be taken by another processor. Expressed in milliseconds. The default value is `600000`. |
|event.processing.processed.events.action|To keep the database table where the Process Engine writes the events small and efficient, processed events are either moved to another table or deleted. Possible values are *move* and *delete*. Move is the safe option, as it allows for reconstructing the Elasticsearch index if the index was to get corrupted for some reason. The default value is `move`. |
|event.processing.processed.action.cronExpression|The cron expression that defines how often the action above happens. The default value is `0 25/45 \* \* \* ?`. |

### Rebuild indexes

Occasionally, an Elasticsearch index can get corrupted and become unusable. All data that are sent to Elasticsearch is stored in the relational database (except if the property `event.processing.processed.events.action` has been set to delete, in which case the data is lost).

You might have to rebuild the indexes when changing the core Elasticsearch settings (for example, number of shards).

Events are stored in the **ACT_EVT_LOG** table before they are processed. The **IS_PROCESSED_** flag is set to `0` when inserting an event and changing it to `1` to process for ElasticSearch. An asynchronous component will move those table rows with `1` for the flag to the **PROCESSED_ACTIVITI_EVENTS**.

Therefore, to rebuild the Elasticsearch index, you must do the following:

* Remove the data from Elasticsearch (deleting the data folders for example in the embedded mode)
* Copy the rows from `PROCESSED_ACTIVITI_EVENTS` to `ACT_EVT_LOG` and setting the `IS_PROCESSED` flag to `0` again.

Note also, due to historical reasons, the `DATA_` column has different types in `ACT_EVT_LOG` (byte array) and `PROCESSED_ACTIVITI_EVENTS` (long text). So a data type conversion is needed when moving rows between those tables.

See the example-apps folder that comes with Process Services. It has an event-backup-example folder, in which a Maven project can be found that carries out the data type conversion. You can also use this to back up and restore events. Note that this example uses Java, but it can also be done with other languages. It first writes the content of `PROCESSED_ACTIVITI_EVENTS` to a .csv file. This is also useful when this table becomes too big in size: store the data in a file and remove the rows from the database table.

## Microsoft Office

The Microsoft Office integration (opening an Office document directly from the browser) doesn’t need any specific configuration. However, the protocol used for the integration mandates the use of **HTTPS** servers by default. This means that Process Services must run on a server that has HTTPS and its certificates are correctly configured.

If this is not possible for some reason, change the setting on the machines for **each** user to make this feature work.

For Windows, see:

[http://support.microsoft.com/kb/2123563](http://support.microsoft.com/kb/2123563){:target="_blank"}

For OS X, execute following terminal command:

```bash
defaults -currentHost write com.microsoft.registrationDB hkey_current_user\\hkey_local_machine\\software\\microsoft\\office\\14.0\\common\\internet\\basicauthlevel -int 2
```

Note that this is not a recommended approach from a security point of view.
---
title: Configure Process Services
---

Configure Process Services using a properties file named `activiti-app.properties`. This file must be placed on the application server’s classpath to be found.

Additionally, the properties file is available with the following options:

* An `activiti-app.properties` file with default values in the WAR file (or exploded WAR folder) under the `WEB-INF/classes/META-INF/activiti-app` folder.
* An `activiti-app.properties` file with custom values on the classpath. For example, the `WEB-INF/classes` folder of the WAR, the `/lib` folder of Tomcat, or other places specific to the web container being used.

The values of a configuration file on the classpath have precedence over the values in the `WEB-INF/classes/META-INF/activiti-app/activiti-app.properties` file.

For the Process Services user interface, there is an additional configuration file named `app-cfg.js`. This file is located inside the .war file’s `script` directory.

At a minimum, the application requires the following settings to run:

* A [database connection]({% link process-services/latest/config/database.md %}) using a JDBC connection or JNDI data source.
* An accurate [Hibernate dialect]({% link process-services/latest/config/database.md %}#hibernate-settings).

All other properties use the default settings, which allows the application to start up and run.

## General settings

By default, the following property is defined:

|Property|Description|
|--------|-----------|
|server.contextroot|The context root on which the user accesses the application. This is used in various places to generate URLs to correct resources. The default value is `activiti-app`. |

## Security settings

By default, the following properties are defined:

> **Important:** If you set the property `security.sanitize-element-names.enabled` to `false` it will make Process Services less secure. Ensure you read the description for more information.  

|Property|Description|
|--------|-----------|
|security.rememberme.key|Used for cookie validation. In a multi-node setup, all nodes must have the same value for this property.|
|security.csrf.disabled|When `true`, the cross-site forgery (CSRF) protection is disabled. The default value is `false`. |
|security.signup.disabled|When `true`, the Process Services sign up functionality is disabled. An error message sign up is not possible will be displayed. The default value is `false`. |
|security.sanitize-element-names.enabled|In some instances, you may need to use the `<`, `>`, `'`, `"`, `+` special characters for the elements that make up your processes. To do this however you must deactivate sanitation and set this property to `false`. The default is `true`. **Important:** If you deactivate sanitation, by setting this property to `false`, you will render Process Services to be less secure and potentially make your code subject to XSS vulnerability attacks. You can minimize the risk by utilizing the HTTPS security protocol.  |

## Encrypt configuration properties

You can encrypt sensitive properties in the `activiti-app.properties`, `activiti-admin.properties` and `activiti-ldap.properties` configuration files.

> **Note:** The generation of `ENCRYPTEDPASSWORD` should be done on the JVM of Process Services.

1. Choose an algorithm.

    If you do not specify an algorithm to Jasypt, then you effectively obtain the default of `PBEWithMD5AndDES`. Some algorithms may appear in the list but may not be usable as the JRE policy blocks them.

    If you want to increase your range of choices then you can modify the JRE policies: [Default Policy Implementation and Policy File Syntax](https://docs.oracle.com/javase/8/docs/technotes/guides/security/PolicyFiles.html){:target="_blank"}. There is an equivalent for the IBM JRE: [IBM WebSphere Java unrestricted policy files](https://www.ibm.com/support/pages/ibm-websphere-java-unrestricted-policy-files){:target="_blank"}.

    Algorithms using AES are generally considered most secure. TripleDES also passes security checks at present. You should consult your security department for advice specific to your organization and the needs of your server.

2. Use the JVM of APS.

    Move into your working directory. For example, if you are using Tomcat on Unix, `cd` to `tomcat_home/webapps/activiti-app/WEB-INF/lib` and then run `java -cp jasypt-1.9.3.jar org.jasypt.intf.cli.JasyptPBEStringEncryptionCLI input=<database password> password=secretpassword algorithm=PBEWithMD5AndDES`

    > **Note:** You should try and avoid using quotes. Also check that you can decrypt the value, preferably using the intended JRE.

3. Configure your application server to set the encryption algorithm and secret encryption password.

    If, for example, you are using Tomcat on Unix then you could include a shell script called `setenv.sh` in `tomcat_home/bin` with the following content:

    ```text
    export JAVA_OPTS="$JAVA_OPTS -Djasypt.encryptor.password=secretpassword -Djasypt.encryptor.algorithm=PBEWITHSHA1ANDDESEDE -Djasypt.encryptor.iv-generator-classname=org.jasypt.iv.NoIvGenerator"
    ```

    This assumes that your password is `secretpassword` and you are using the algorithm `PBEWITHSHA1ANDDESEDE`. The configuration could alternatively be done in `startup.sh`.

    If you then run using `catalina.sh` you will see the secret password in the logging on application startup. This is a Tomcat feature, which you can disable by removing `<Listener className="org.apache.catalina.startup.VersionLoggerListener" />` from your Tomcat's `server.xml` [Turn off Tomcat logging via Spring Boot Application](https://stackoverflow.com/questions/35485826/turn-off-tomcat-logging-via-spring-boot-application){:target="_blank"} You may initially, however, want to leave this on for diagnostic purposes until you’ve proven you’ve got encryption working. For an example of this, see [Pass user defined environment variable to tomcat](https://stackoverflow.com/questions/17019233/pass-user-defined-environment-variable-to-tomcat){:target="_blank"}.

    For other servers there will be other ways of setting environment/JVM variables. These values can be read as JVM parameters, environment variables or as property file entries (though you would not want to put the secret encryption password in a property file). Therefore, with WebSphere they could set using JVM parameter config [Setting generic JVM arguments in WebSphere Application Server](http://www-01.ibm.com/support/docview.wss?uid=swg21417365){:target="_blank"} or environment variable config [Introduction: Variables](https://www.ibm.com/support/knowledgecenter/en/SSAW57_8.5.5/com.ibm.websphere.nd.doc/ae/welcvariables.html){:target="_blank"}.

4. Start the application.

    The application should now start as normal. If it doesn’t, try without the encrypted values and without the encryption parameters to determine whether the problem is related to the encryption setup. Check that you are able to encrypt and decrypt with Jasypt to rule out any issues due to copy-paste errors.

5. Logging.

    Some property values (though not sensitive ones) are logged by Alfresco applications if the log level is set high. If you want to restrict this then reduce the log level in`log4j.properties`

## CORS

To enable Cross Origin Resource Sharing (CORS) in Process Services, set the `cors.enabled` property to true in the
`activiti-app.properties` file.

>**Note:** This feature is only supported on Tomcat application server.

```text
# CORS CONFIGURATION
#
cors.enabled=true
```

When CORS is enabled, CORS requests can be made to all endpoints under `/activiti-app/api`.

Also, some additional properties are made available which can be configured to further fine tune CORS. This will make CORS available only to certain origins or to restrict the valid HTTP methods that can be used and headers that can be sent with CORS-enabled requests.

```text
cors.enabled=false
cors.allowed.origin.patterns=*
cors.allowed.methods=GET,POST,HEAD,OPTIONS,PUT,DELETE
cors.allowed.headers=Authorization,Content-Type,Cache-Control,X-Requested-With,accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers,X-CSRF-Token
cors.exposed.headers=Access-Control-Allow-Origin,Access-Control-Allow-Credentials
cors.support.credentials=truecors.preflight.maxage=10
```

|Property|Description|
|--------|-----------|
|cors.allowed.origins|Specifies A list of origins for which cross-origin requests are permitted. A value specified may be a specific domain, e.g `https://domain32.com`, or the CORS defined special value `*` for all origins. For matched pre-flight and actual requests the Access-Control-Allow-Origin response header can be either be the matched domain value or to `*`. **Note:** The CORS spec does not allow `*` when `allowCredentials` is set to `true` and `cors.allowed.origin.patterns` should be used instead.|
|cors.allowed.origin.patterns|Alternative to `cors.allowed.origins` supports the more flexible origins patterns and `*` can be used anywhere in the host name in addition to port lists. For example: `https://*.domain32.com` domains ending with `domain32.com`, `https://*.domain32.com:[8080,8081]` domains ending with `domain32.com` on port `8080` or port `8081`, and `https://*.domain32.com:[*]`- domains ending with domain32.com on any port, including the default port. In contrast to `cors.allowed.origins` which only supports `*` and cannot be used with `allowCredentials`, when a `cors.allowed.origin.patterns` is matched, the Access-Control-Allow-Origin response header is set to the matched origin and not `*` including the pattern. `cors.allowed.origin.patterns` can be used together with `setAllowCredentials(java.lang.Boolean)` set to true.|
|cors.allowed.methods|Configures which HTTP requests are permitted. GET, POST, HEAD, OPTIONS, PUT, DELETE|
|cors.allowed.headers|Specifies the headers that can be set manually or programmatically in the request headers in addition to the ones set by the user agent (for example, Connection). The default values are: <br><br>Authorization<br><br>Content-Type<br><br>Cache-Control<br><br>X-Requested-With<br><br>Accept<br><br>Origin<br><br>Access-Control-Request-Method<br><br>Access-Control-Request-Headers<br><br>X-CSRF-Token|
|cors.exposed.headers|Allows you to whitelist the headers that the client can access from the server. The default value exposes the following headers:<br><br>Access-Control-Allow-Origin<br><br>Access-Control-Allow-Credentials|
|cors.support.credentials|Determines whether HTTP cookie and HTTP Authentication-based credentials are allowed. The default value is `true`.|
|cors.preflight.maxage|Preflighted requests use the `OPTIONS` method to first verify the resource availability and then request it. This property determines the maximum time (in minutes) for caching a preflight request. The default value is `10`.|

To disable CORS set the following property in the `activiti-app.properties` file:

```text
cors.enabled=false
```

## Cross-Site Request Forgery (CSRF)

Cross-Site Request Forgery, also referred to as CSRF, is one of the most common form of attacks plaguing web browsers. This type of attack results in a malicious request being submitted on a user’s behalf without their consent.

Typically, when the CSRF setting is enabled and an HTTP request against a web application is made, then the token values sent from the client to the server are validated to prevent unauthorized requests that were not generated by the server. The CSRF tokens are usually stored on the server and verified every time a request is sent. However, in Process Services, this feature has been implemented slightly differently, wherein, CSRF tokens are generated on the client instead of the server and placed in a cookie `CSRF-TOKEN` and a header `X-CSRF-TOKEN`. The server side then verifies if the header and cookie values match.

Where:

* `X-CSRF-TOKEN` = header value
* `CSRF-TOKEN` = cookie value

This provides extra security as the cookie that belongs to Process Services can only be accessed for pages generated 
or served by the Process Services domain.

>**Note:** The CSRF protection is only available for resources used by the web application, such as the private REST API (not public REST API).

By default, the CSRF protection setting is enabled in Process Services, however to disable it, make the following changes:

1. Open the `activiti-app.properties` file from the `<ActivitiInstall>/tomcat/lib` folder.
2. Locate the `security.csrf.disabled` setting and then modify it to `true`. For example: `security.csrf.disabled=true`

## License configuration

If you start up the application without a license, it will enter read only mode; however, you can upload a license from the user interface at a later stage. In this situation, use the following configuration properties to configure the license.

|Property|Description|
|--------|-----------|
|license.multi-tenant|If no license is available on first bootstrap this property decides if system will go into single or multi-tenant mode. The default value is `false`. |
|license.default-tenant|If no license is available on first bootstrap this property decides the name of the default tenant. The default value is `tenant`. |
|license.allow-upload|Decides if license uploads should be allowed in the system or not. The default value is `true`. |

## Cookie configuration

Process Services uses an HTTP cookie to store a user session. You can use multiple cookies for different browsers and devices. The application uses a database table to store the cookie values (called **tokens** internally), to allow a shared persistent session store in a multi-node setup.

It’s possible to change the settings regarding cookies:

|Property|description|default|
|--------|-----------|-------|
|security.cookie.max-age|The maximum age of a cookie, expressed in seconds. The max-age determines the period in which the browser will send the cookie with the requests.|2678400 (31 days)|
|security.cookie.refresh-age|The age of a cookie before it is refreshesd. Refreshing means a new token will be created and a new cookie will be returned which the browser will use for subsequent requests. Setting the refresh-age low, will result in many new database rows when the user is using the application.To avoid that a user is suddenly logged out when using the application when reaching the max-age above, tokens are refreshed after this period (expressed in seconds).|86400 (1 day)|

By default, cookies will have the `secure` flag set, when the request being made is HTTPS. If you only want to use the remember-me cookie over HTTPS (i.e. make the *secure* flag mandatory), set the property `security.cookie.always-secure` to `true`.

To avoid that the persistent token table gets too full, a background job periodically removes obsolete cookie token values. Possible settings:

|Property|description|default|
|--------|-----------|-------|
|security.cookie.database-removal.max-age|The maximum age an entry in the database needs to have to be removed.|Falls back to the `security.cookie.max-age` setting if not found. This effectively means that cookies which are no longer valid could be removed immediately from the database table.|
|security.cookie.database-removal.cronExpression|The cron expression determining when the obsolete database table entries for the cookie values will be checked for removal.|`0 0 1 * * ?` (01:00 at night)|
---
title: Configure multi-schema, multi-tenancy
---

It is possible to run Process Services in "multi-schema multi-tenancy" mode (MS-MT). This is a multi-tenant setup where every tenant has its own database schema. This means that the data of one tenant is completely separated from the data of other tenants.

This is an alternative to the "regular" multi-tenant mode, where the data of all tenants is stored in the same database schema and the data gets a "tenant tag" to identity which tenant the data belongs to. The following diagram shows this setup:

![msmt-regular-mt]({% link process-services/images/msmt-regular-mt.png %})

The main benefit of this setup is the ease of setup and configuration: there is no difference with setting up a single-tenant or multi-tenant. Each request can be handled by any node and the loadbalancer simply can route using simple routing algorithms.

The downside of this setup is clearly that the database can become the bottleneck if it has to hold all the data of all tenants and there is no "physical separation" of the tenant data.

The MS-MT setup looks as follows:

![msmt-overview1]({% link process-services/images/msmt-overview1.png %})

The most important benefit of this approach is that the data of each tenant is completely separated from the data of other tenants. Since only data of one tenant is stored in the database schema, queries will generally be more performant.

The downside of this approach is immediately visible in this diagram: each node needs to have a connection pool to the database schema of the tenant. With many tenants, this can mean quite a bit of "housekeeping" that will need to be performed compared to the previous approach (which can be negative for performance). Note that there is a "master database" or "primary database" in this diagram. This database stores the configurations of the tenant data sources and the mapping between user and tenant.

Alternatively, as shown in the following diagram, it is possible to configure the Suite nodes as such that they only manage a certain list of tenants (for example in the picture below the last node only manages tenant Z, and the first two manage tenant A and B, but not Z). Although this alleviates the downside of the previous setup, it does come with an extra cost: the load balancer now needs to be more intelligent and needs to route the incoming request to the appropriate node. This means that the request needs information to differentiate as to which tenant the request is coming from. This needs custom coding on the client side and is not by default available in the Process Services web client.

![msmt-overview2]({% link process-services/images/msmt-overview2.png %})

Taking this to the extreme, it is possible to have one (or more nodes) for one tenant. However, in that case it is probably easier to run a single tenant Process Services for each tenant. The remarks about the load balancer and enriching the request with tenant information as in the previous setup still apply.

## Limitations

Currently, following known limitations apply to the multi-schema multi-tenancy (MS-MT) feature:

* As with regular multi-tenancy, it is not possible to configure the out of the box LDAP synchronization to synchronize users to different tenants.
* The tenant can **only be configured through the REST API**, not via the "identity management" app.
* Users need to be created by a user that is a "Tenant Administrator", **not** a "Tenant Manager".
* Updating a tenant configuration (more specifically: switching the data source) cannot be done dynamically, a restart of all nodes is required for it to be picked up.
* A user id needs to be unique across all tenants (cft. an email). This is because a mapping {user id, tenant id} will be stored in the primary database to determine the correct tenant data source.

## Implementation

This section describes how the MS-MT feature works and can be skipped if only interested in setting up an 
MS-MT Process Services.

The MS-MT feature depends on this fundamental architecture:

* There is one **primary datasource**
    * The configurations of the tenants is stored here (for example their data source configuration).
    * The user to tenant mapping is stored here (although this can be replaced by custom logic).
    * The "Tenant Manager" user is stored here (as this user doesn’t belong to any tenant).
* There are **x data sources**
    * The tenant specific data is stored here.
    * For each tenant, a datasource configuration similar to a single tenant datasource configuration needs to be provided.
    * For each tenant datasource, a connection pool is created.
* When a request comes in, the tenant is determined.
    * A **tenant identifier** is set to a threadlocal (making it available for all subsequent logic executed next by that thread).
    * The `com.activiti.database.TenantAwareDataSource` switched to the correct tenant datasource based on this threadlocal.

The following diagram visualizes the above points: when a request comes in, the security classes for authentication (configured using Spring Security) will kick in before executing any logic. The request contains the `userId`. Using this `userId`, the **primary datasource** is consulted to find the `tenantId` that corresponds with it (note: this information is cached in a configurable way so the primary datasource is not hit on every request. But it does mean that user removals from a tenant can take a configurable amount of time to be visible on all nodes). This does mean that in MS-MT mode, there is a (very small) overhead on each request which isn’t there in the default mode.

The `tenantId` is now set on a threadlocal variable (mimicking how Spring Security and its `SecurityContext` works). If the value is ever needed, it can be retrieved through the `com.activiti.security.SecurityUtils.getCurrentTenantId()` method.

When the logic is now executed, it will typically start a new database transaction. In MS-MT mode, the default DataSource implementation is replaced by the `com.activiti.database.TenantAwareDataSource` class. This implementation returns the datasource corresponding with the `tenantId` value set on the threadlocal. The logic itself remains unchanged.

![msmt-tech-impl]({% link process-services/images/msmt-tech-impl.png %})

The MS-MT feature does have a technical impact on some other areas too:

* All default caches (process, forms, apps, script files, …) cache based on the db id as key. In MS-MT mode, the db id is not unique over tenants and the cache switches to a *cache per tenant* implementation.
* Event processing (for analytics) by default polls the database for new events which needs to be sent to Elastic Search. In MS-MT mode, the events for each tenant datasource are polled.
* The Process Engine job executor (responsible for timers and async continuations) polls the database for new jobs to execute. In MS-MT mode, this polling needs to happen for each tenant datasource.
* The Hibernate id generator keeps by default a pool of identifiers for each entity primary key in memory. Hibernate keeps the *lastest id* stored in a database table. In MS-MT mode however, there should be a pool for each tenant and the id generator needs to use the correct tenant datasource for refreshing the pool of ids.
* A similar story applies for the Process Engine id generator.

## Getting started

To run Process Services, you need to have installed a *multi-tenant* license. Switching to MS-MT mode is done setting the *tenancy.model* property to *isolated*.

```text
tenancy.model=isolated
```

When using MS-MT, there always needs to be a *primary datasource*. This datasource is configured exactly the same as when configuring the single datasource. For example when using a Mysql database:

```text
datasource.url=jdbc:mysql://127.0.0.1:3306/primary-activiti?characterEncoding=UTF-8
com.mysql.cj.jdbc.Driver
datasource.username=alfresco
datasource.password=alfresco

hibernate.dialect=org.hibernate.dialect.MySQLDialect
```

Booting up Process Services now will create the regular tables in the *primary-activiti* schema, plus some additional tables specific to the *primary datasource* (such tables are prefixed with **MSMT_**). A default user with tenant manager capabilities is created (the login email and password can be controlled with the `admin.email` and `admin.passwordHash` properties) too.

One thing to remember is that there are no REST endpoints specific to MS-MT. All the existing tenant endpoints simply behave slightly different when running in MSMT mode. Using this tenant manager user (credentials in the basic auth header), it is now possible to add new tenants by calling the REST API:

```bash
POST http://your-domain:your-port/activiti-app/api/enterprise/admin/tenants
```

with the following JSON body:

```json
{
    "name" : "alfresco",
    "configuration" : "tenant.admin.email=admin@alfresco.com\n
    com.mysql.cj.jdbc.Driver\n
    datasource.url=jdbc:mysql://127.0.0.1:3306/tenant-alfresco?characterEncoding=UTF-8\n
    datasource.username=alfresco\n
    datasource.password=alfresco"
}
```

Note that in some databases such as postgres, you may need to set the **database.schema** or **database.catalog** for database who work with catalogs.

Note the `\n` in the body of the configuration property.

Also note that this configuration will be stored encrypted (using the `security.encryption.secret` secret).

This will:

* Create a tenant named `alfresco`.
* Data of this tenant is stored in the database schema `tenant-alfresco`.
* A default tenant administrator user with the email login `admin@alfresco.com` is created, with the default password `admin` (this can be changed after log in).

When executing this request, in the logs you will see the tenant being created in MSMT mode:

```text
INFO com.activiti.msmt.MsmtIdmService  - Created tenant 'alfresco' in primary datasource (with id '1')
```

In the logs, you’ll see:

* The datasource connection pool for this tenant being created.
* The Liquibase logic creating the correct tables.

At the end, you’ll see the following message indicating all is ready:

```text
INFO com.activiti.msmt.MsmtIdmService  - Created tenant 'alfresco' in tenant datasource (with id '1')
INFO com.activiti.msmt.MsmtIdmService  - Registered new user 'admin@alfresco.com' with tenant '1'
```

You can now log in into the web UI using *admin@alfresco.com/admin*, change the password and add some users. These users can of course also be added via the REST API using the tenant admin credentials.

A new tenant can easily be added in a similar way:

```bash
POST http://your-domain:your-port/activiti-app/api/enterprise/admin/tenants
```

with body

```json
{
    "name" : "acme",
    "configuration" : "tenant.admin.email=admin@acme.com\n
    com.mysql.cj.jdbc.Driver\n
    datasource.url=jdbc:mysql://127.0.0.1:3306/tenant-acme?characterEncoding=UTF-8\n
    datasource.username=alfresco\n
    datasource.password=alfresco"
}
```

When the tenant admin for this tenant, *admin@acme.com* logs in, no data of the other one can be seen (as is usual in multi-tenancy). Also when checking the *tenant-alfresco* and *tenant_acme* schema, you’ll see the data is contained to the tenant schema.

The tenant manager can get a list of all tenants:

```bash
GET http://your-domain:your-port/activiti-app/api/enterprise/admin/tenants
```

```json
[
  {
    "id": 2,
    "name": "acme"
  },
  {
    "id": 1,
    "name": "alfresco"
  }
]
```

To get specific information on a tenant, including the configuration:

```
GET http://your-domain:your-port/activiti-app/api/enterprise/admin/tenants/1
```

which gives:

```json
{
  "id": 1,
  "name": "alfresco",
  "created": "2016-04-27T09:22:33.511+0000",
  "lastUpdate": null,
  "domain": null,
  "active": true,
  "maxUsers": null,
  "logoId": null,
  "configuration": "tenant.admin.email=admin@alfresco.com\n
  com.mysql.cj.jdbc.Driver\n
  datasource.url=jdbc:mysql://127.0.0.1:3306/tenant-alfresco?characterEncoding=UTF-8\n
  datasource.username=alfresco\n
  datasource.password=alfresco"
}
```

## Behavior

Assuming a multi-node setup: when creating new tenants, the REST call is executed on one particular node. After the tenant is successfully created, users can log in and use the application without any problem on any node (so the loadbalancer can simply randomly distribute for example). However, some functionality that depends on backgrounds threads (the job executor, for example) will only start after a certain period of time since the creation of the tenant on another node.

This period of time is configured via the `msmt.tenant-validity.cronExpression` cron expression (by default every 10 minutes).

Similarly, when a tenant is deleted, the deletion will happen on one node. It will take a certain amount of time (also configured through the `msmt.tenant-validity.cronExpression` property) before the deletion has rippled through all the nodes in a multi-node setup.

Note that tenant datasource configuration are not automatically picked up and require a reboot of all nodes. However, changing the datasource of a tenant should happen very infrequently.

## Properties

There are some configuration properties specific to MS-MT:

* `tenancy.model` : possible values are `shared` (default if omitted) or `isolated`. Isolated switched a multi-tenant setup to MS-MT.
* `msmt.tenant-validity.cronExpression` : the cron expression that determines how often the validity of tenants must be checked (see previous section) (by default every 10 minutes).
* `msmt.async-executor.mode` : There are two implementations of the Async job executor for the Activiti core engine. The default is `isolated`, where for each tenant a full async executor is booted up. For each tenant there will be acquire threads, a threadpool and queue for executing threads. The alternative value for this property is `shared-queue*`, where there are acquire threads for each tenant, but the actual job execution is done by a shared threadpool and queue. This saves some server resources, but could lead to slower job processing in case there are many jobs.
* `msmt.bootstrapped.tenants` : a semicolon separated list of tenant names. Can be used to make sure one node in a multi-node setup only takes care of the tenants in the list. Does require that the loadbalancer also uses similar logic.

## Pluggability

Following interfaces can be used to replace the default implementations of MS-MT related functionality:

* `com.activiti.api.msmt.MsmtTenantResolver` : used when the user authenticates and the tenant id is determined. The default implementation uses a database table (with caching) to store the user id to tenant id relationship.
* `com.activiti.api.msmt.MsmtUserKeyResolver` : works in conjuction with the Default `MsmtTenantResolver`, returns the user id for a user. By default returns the email or external id (if external id is used).
* `com.activiti.api.datasource.DataSourceBuilderOverride` : called when a tenant datasource configuration is used to create a datasource. If there is a bean on the classpath implementing this interface, the logic will be delegated to this bean to create the `javax.sql.DataSource`. By default, a c3p0 DataSource / connection pool will be created for the configuration.
---
title: Develop extensions for Process Services
---

This guide describes how to develop extensions and customize Process Services.

Before beginning, you should read the [Installing]({% link process-services/latest/install/index.md %}) and [Configuring]({% link process-services/latest/config/index.md %}) sections to make sure you have an understanding of how Process Services is installed and configured.

## Maven modules

When customizing, overriding, or creating new logic in Process Services, it is useful to be able to develop against the relevant Maven modules.

The following Maven modules are the most important ones.

The diagram is structured in such a way that the lowest module is a dependency of the module one up higher (and so forth).

![maven_modules]({% link process-services/images/maven_modules.png %})

All Maven modules have `com.activiti` as Maven `groupId`. The version of the artifact is the release version of Process Services.

* `activiti-app-model` : Contains the *domain objects*, annotated with JPA annotations for persistency and various Spring repositories for executing the actual database operations. Also has the Java pojos of the JSON representations that are used for example as responses by the REST endpoints.
* `activiti-app-logic` : Contains the services and actual BPM Suite logic.
* `activiti-app-rest` : Contains the REST endpoints that are used by the UI and the public API.
* `activiti-app-dependencies` : Contains all the Process Services dependencies. It is also a convenient Maven module (packaging type is *pom*) for development.
* `activiti-app` : Contains configuration classes.
* `activiti-app-root`: Contains the root pom. **Do not use this for development.**

## Start and task form customization

The start and task forms that are part of a task view can be customized for specific requirements. The following JavaScript code example provides an overview of all the form and form field events that can be used to implement custom logic.

By default, a file name `render-form-extensions.js` in the `workflow/extensions` folder is present and loaded in the `index.html` file of the `workflow` folder. It has empty methods by default:

```javascript
var ALFRESCO = ALFRESCO || {};

ALFRESCO.formExtensions = {

    // This method is invoked when the form field have been rendered
    formRendered:function(form, scope) {

    },

    // This method is invoked when input values change (ng-change function)
    formFieldValueChanged:function(form, field, scope) {

    },

    // This method is invoked when an input field gets focus (focus event with ng-focus function)
    formFieldFocus:function(form, field, scope) {

    },

    // This method is invoked when an input field has lost focus (blur event with ng-blur function)
    formFieldBlur:function(form, field, scope) {

    },

    // This method is invoked when a person has been selected in the people picker
    formFieldPersonSelected:function(form, field, scope) {

    },

    // This method is invoked when an email has been filled-in in the people picker
    formFieldPersonEmailSelected:function(form, field, scope) {

    },

    // This method is invoked when a person has been removed in the people picker
    formFieldPersonRemoved:function(form, field, scope) {

    },

    // This method is invoked when a group has been selected in the functional group picker
    formFieldGroupSelected:function(form, field, scope) {

    },

    // This method is invoked when a group has been removed in the functional group picker
    formFieldGroupRemoved:function(form, field, scope) {

    },

    // This method is invoked when content has been uploaded in the upload field
    formFieldContentUploaded:function(form, field, scope) {

    },

    // This method is invoked when content has been removed in the upload field
    formFieldContentRemoved:function(form, field, scope) {

    },

    // This method is invoked when the REST values or set in a dropdown, radio or typeahead field
    formFieldRestValuesSet:function(form, field, scope) {

    },

    // This method is invoked when the complete or an outcome button has been clicked and before the task is completed.
    formBeforeComplete:function(form, outcome, scope) {

    },

    // This method is invoked when input values change (ng-change function) in a dynamic table
    formTableFieldValueChanged:function(form, field, columnDefinition, editRow, scope) {

    },

    // This method is invoked when an input field gets focus (focus event with ng-focus function) in a dynamic table
    formTableFieldFocus:function(form, field, columnDefinition, editRow, scope) {

    },

    // This method is invoked when an input field has lost focus (blur event with ng-blur function) in a dynamic table
    formTableFieldBlur:function(form, field, columnDefinition, editRow, scope) {

    },

    // This method is invoked when the REST values or set in a dropdown field in a dynamic table
    formTableFieldRestValuesSet:function(form, field, columnDefinition, editRow, scope) {

    },

    // This method is invoked when the form fields have been rendered in the dynamic table popup
    formTableRendered:function(form, field, columnDefinitions, editRow, scope) {

    },

    // This method is invoked when the complete button has been clicked and before the dynamic table popup is completed.
    formTableBeforeComplete:function(form, field, editRow, scope) {

    },

    // This method is invoked when the cancel button has been clicked and before the dynamic table popup is cancelled.
    formTableBeforeCancel:function(form, field, editRow, scope) {

    },

    // This method is invoked when input values change (ng-change function) and will disable the complete buttons when false (boolean) is returned.
    formValidateFieldValueChanged:function(form, field, scope) {

    },

    // This method is invoked when the complete button has been clicked and will prevent the form completion when false (boolean) is returned.
    formValidateBeforeSubmit:function(form, outcome, scope) {

    },

    // This method is invoked when input values change (ng-change function) in a dynamic table and will disable the save button when false (boolean) is returned.
    formTableValidateFieldValueChanged:function(form, field, columnDefinition, editRow, scope) {

    },

    // This method is invoked when the complete button has been clicked and before the dynamic table popup is completed and prevent the form completion
    // when false (boolean) is returned.
    formTableValidateBeforeComplete:function(form, field, editRow, scope) {

    },

    // This method is invoked when a task is completed successfully
    taskCompleted:function(taskId, form, scope) {

    },

    // This method is invoked when a task is completed unsuccessfully
    taskCompletedError:function(taskId, errorResponse, form, scope) {

    },

    // This method is invoked when a task is saved successfully
    taskSaved:function(taskId, form, scope) {

    },

    // This method is invoked when a task is saved unsuccessfully
    taskSavedError:function(taskId, errorResponse, form, scope) {

    }
};
```

This file can be changed to add custom logic. Alternatively, it is also possible to add new JavaScript files and reference them in the `index.html` file (do take those files in account when upgrading to newer versions of the application) but it is also possible to load additional folders using the resource loader, see [Custom web resources](#custom-web-resources).

In every event method the full form variable is passed as a parameter. This form variable contains the form identifier and name, but also the full set of form fields with type and other configuration information.

In addition the changed field is passed when applicable and the Angular scope of the form renderer is also included. This is a regular Angular directive (that is, isolated) scope, with all methods available.

For example, to get the current user:

```javascript
formRendered:function(form, scope) {
    var currentUser = scope.$root.account;
    console.log(currentUser);
}
```

## Custom form fields

Custom form field types can be added through custom *form stencils*. A form stencil is based on the default form stencil and can have default form field types removed, reordered, tweaked (changing the name, icon, and so on.) or have new form field types.

Form stencils are defined in the **Stencils** section of the App Designer. A new form field type consists of the following:

* An HTML template that is rendered when drag and dropping from the palette on the form canvas is the form builder.
* An HTML template that is rendered when the form is displayed at run-time.
* An optional custom AngularJS controller in case custom logic needs to be applied to the form field.
* An optional list of third party scripts that are needed when working with the form field at run-time.

**Static image custom form field:**

This is a very basic example of a custom form field type that simply displays a static image.

Create a new form stencil in the App Designer and click the **Add new item** link.

The **Form run-time template** (the HTML used when the form is rendered at run-time) and the **Form editor template** (the HTML used in the form builder) is the same here:

```html
<img src="http://activiti.org/images/activiti_logo.png"></img>
```

**Dynamic image custom form field:**

Create another new item for the form stencil, for example, create a configurable image. Unlike the static image of the previous example, the user building the form will be able to select the image that will be displayed.

The **Form runtime template** needs to show the image that the form builder has selected. Assume that a property `url` is set (see later on). Note the use of `ng-src` (see [AngularJs docs on ng-src](https://docs.angularjs.org/api/ng/directive/ngSrc){:target="_blank"} to have a dynamic image:

```html
<img ng-src="{{field.params.customProperties.url}}"></img>
```

Note the syntax **field.params.customProperties** to get access to the non-default properties of the form field.

The **Form editor template** simply needs to be a generic depiction of an image or even simpler like here, just a bit of text:

```html
<i>The custom image here</i>
```

Don’t forget to add a property `url` to this stencil item with the name `url` and type `text`.

**Dynamic pie chart custom form field:**

This example is more advanced then the previous two: it contains a simple list of number fields with a button at the bottom to add a new line item, while generating a pie chart on the right.

We’ll use the [Epoch library](https://github.com/fastly/epoch){:target="_blank"} as an example here. Download the following files from its Github site:

* [d3.min.js](https://raw.githubusercontent.com/mbostock/d3/v3.5.6/d3.min.js){:target="_blank"}
* [epoch.min.js](https://raw.githubusercontent.com/fastly/epoch/0.6.0/epoch.min.js){:target="_blank"}

Create a new form stencil item and name it "Chart". Scroll down to the **Script library imports** section, and upload 
the two libraries. At run-time, these third party libraries will be included when the form is rendered.

**Note**: The order in which the third party libraries are defined is important. Since the Epoch library depends on d3, d3 needs to be first in the table and epoch second (as that is the order in which they are loaded at run-time).

The **Form editor template** is the easy part. We could just use an image of a pie chart here.

```html
<img src="url_to_pie_chart_image.png"></img>
```

First define the controller for this form field type. The controller is an AngularJs controller, that does mainly three things:

* Keep a model of the line items
* Implement a callback for the button that can be clicked
* Store the value of the form field in the proper format of Process Services

```javascript
angular.module('activitiApp')
    .controller('MyController', ['$rootScope', '$scope', function ($rootScope, $scope) {

        console.log('MyController instantiated');

        // Items are empty on initialisation
        $scope.items = [];

        // The variable to store the piechart data (non angular)
        var pieChart;

        // Epoch can't use the Angular model, so we need to clean it
        // (remove hashkey etc, specific to Angular)
        var cleanItems = function(items) {
            var cleanedItems = [];
            items.forEach(function(item) {
               cleanedItems.push( { label: item.label, value: item.value} );
            });

            return cleanedItems;
        };

        // Callback for the button
        $scope.addItem = function() {

            // Update the model
            $scope.items.push({ label: 'label ' + ($scope.items.length + 1), value: 0 });

            // Update the values for the pie chart
            // Note: Epoch is not an angular lib so doesn't use the model directly
            if (pieChart === undefined) {

                pieChart = jQuery('.activiti-chart-' + $scope.field.id).epoch({
                    type: 'pie',
                    data: cleanItems($scope.items)
                });
                console.log('PieChart created');

            } else {

                $scope.refreshChart();

            }

        };


        // Callback when model value changes
        $scope.refreshChart = function() {
            pieChart.update(cleanItems($scope.items));
            console.log('PieChart updated');
        };


        // Register this controller to listen to the form extensions methods
        $scope.registerCustomFieldListener(this);

        // Deregister on form destroy
        $scope.$on("$destroy", function handleDestroyEvent() {
            console.log("destroy event");
            $scope.removeCustomFieldListener(this);
        });

        // Setting the value before completing the task so it's properly stored
        this.formBeforeComplete = function(form, outcome, scope) {
            console.log('Before form complete');
            $scope.field.value = JSON.stringify(cleanItems($scope.items));
        };

        // Needed when the completed form is rendered
        this.formRendered = function(form, scope) {
            console.log(form);
            form.fields.forEach(function(field) {
                if (field.type === 'readonly'
                      && $scope.field.id == field.id
                      && field.value
                      && field.value.length > 0) {

                    $scope.items = JSON.parse(field.value);
                    $scope.isDisabled = true;

                    pieChart = jQuery('.activiti-chart-' + $scope.field.id).epoch({
                        type: 'pie',
                        data: cleanItems($scope.items)
                    });

                }
            });
        };

}]);
```

The **Form runtime template** needs to reference this controller, use the model and link the callback for the button:

```javascript
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/epoch/0.6.0/epoch.min.css">

<div ng-controller="MyController" style="float:left;margin: 35px 20px 0 0;">
    <div ng-repeat="item in items">
          <input type="text" ng-model="item.label" style="width:200px; margin: 0 10px 10px 0;" ng-change="refreshChart()">
          <input type="number" ng-model="item.value" style="width: 80px; margin-bottom: 10px;" ng-change="refreshChart()">
    </div>

    <div>
        <button class="btn btn-default btn-sm" ng-click="addItem()" ng-disabled="isDisabled">
           Add item
        </button>
    </div>
</div>

<div class="epoch category10" ng-class="'activiti-chart-' + field.id" style="display:inline-block;width: 200px; height: 200px;"></div>
<div class="clearfix"></div>
```

At run-time, the following will be rendered:

![example-form-stencil]({% link process-services/images/example-form-stencil.png %})

## Custom web resources

If you want to add additional JavaScript functionality or override CSS rules, you can configure lists of additional web resources that are loaded by the browser for each Process Services app. You do this by configuring a new resource in the `tomcat/webapps/activiti-app` folder.

Following is an example of a new resource section in the `app-cfg.js` file located in the 
`tomcat/webapps/activiti-app/scripts` folder:

```json
ACTIVITI.CONFIG.resources = {
    '*': [
        {
            'tag': 'link',
            'rel': 'stylesheet',
            'href': ACTIVITI.CONFIG.webContextRoot + '/custom/style.css?v=1.0'
        }
    ],
    'workflow': [
        {
            'tag': 'script',
            'type': 'text/javascript',
            'src': ACTIVITI.CONFIG.webContextRoot + '/custom/javascript.js?v=1.0'
        }
    ]
};
```

The `ACTIVITI.CONFIG.resources` object makes it possible to load different files for each of the Activiti applications using their names as key for a list of additional resources that shall be loaded, the different app names are: `landing`, `analytics`, `editor`, `idm` and `workflow`. The `*` key means that a default resource list will be used unless there is a specific config key for the app being loaded.

For example, if a user would enter the `editor` app, with the config above deployed, `custom/style.css` would be the
only custom resource that would be loaded. If a user would go to the `workflow` app, `custom/javascript.js` would be
the only custom resource that would be loaded. So if `workflow` also wants to load the `custom/style.css` that would
have to be specified again inside the *workflow* resource list.

>**Note:** Remember to modify the `v`-parameter when you have done changes to your files to avoid the browser from using a cached version of your custom logic.

## Document Templates

Use the **Generate Document** task to generate a PDF or Microsoft Word document based on a Word document template (.docx). You can insert process variables in the MS Word template that will be replaced with actual values during document transformation.

A document template can be:

* **Tenant wide**: Anyone can use this template in their processes. Useful for company templates.
* **Process model specific**: This template is uploaded while modeling the process model, and is bound to the lifecycle of the process model.

When exporting an App model, process model document templates are included by default and are uploaded again on import. Tenant document templates are not exported, however matched by the document template name as names are unique for tenant document templates.

In the `.docx` template, you can insert process variables using the following syntax:

```text
<<[myVariable]>>
```

Since the above method does not perform `null` checks, an exception will be thrown at run-time if the variable is `null`. Therefore, use the following method to prevent such errors:

```text
<<[variables.get("myVariable")]>>
```

If this variable is `null`, a default value will be inserted instead. You can also provide a default value:

```text
<<[variables.get("myVariable", "myDefaultValue")]>>
```

>**Note**: Form field types such as Dropdown, Radio button, and Typeahead use `myVariable_ID` for ID and `myVariable_LABEL` for label value. The ID is the actual value used by service tasks and are inserted by default. To display the label value in the generated document, use `myVariable_LABEL`.

The document generation method uses libraries provided by Aspose in the back-end.

When using the **Generate Document** task, make sure that you use the correct syntax for your variables and expressions. Surround your variables with `<<[..]>>` characters. For example:

* `<<[variableid]>>`
* `<<[variables.get("variableid")]>>`
* `<<[variables.get("variableid","adefaultifnull")]>>`

Some more examples:

* If/else conditional blocks:
    * Text type: `<<if [textfield==day]>> AM, <<else>> PM \<</if>>`
    * Amount type: `<<if [annualsalary > $40000]>>, it is generous, <<else>> a standard starting salary \<</if>>`
    * Checkbox: `<<if [senstitiveflag=="true"]>>it is Confidential, <<else>> Not Confidential \<</if>>`
* Date type: `<<[datefield]>>`
* Format date type: `<<[datefield]:"yyyy.MM.dd">>`
* Number/amount: `<<[amountfield]>>`
* String Boolean: `<<[Genericcheckbox]>>`
* Radio button / Typehead / dropdown: Select `<<[Options_LABEL]>> with an ID <<[Options_ID]>>`

The audit log is also generated the same way.

For example, the following snippet from the template shows advanced constructs:

![doc-gen-template-example]({% link process-services/images/doc-gen-template-example.png %})

It is also possible to have custom Spring bean that processes the process variables just before rendering the document, [Processing document generation variables](#processing-document-generation-variables).

## Custom Logic

Custom logic in a business process is often implemented using a `JavaDelegate` implementation or a Spring bean.

To build against a specific version of Process Services, add the following dependency to your Maven `pom.xml` file:

```xml
<dependencies>
    <dependency>
        <groupId>com.activiti</groupId>
        <artifactId>activiti-app-logic</artifactId>
        <version>${suite.version}</version>
    </dependency>
</dependencies>
```

### Java Delegates

The simplest option is to create a class that implements the `org.activiti.engine.delegate.JavaDelegate` interface.

```java
package my.company;

import org.activiti.engine.delegate.DelegateExecution;
import org.activiti.engine.delegate.JavaDelegate;

public class MyJavaDelegate implements JavaDelegate {

    public void execute(DelegateExecution execution) throws Exception {
        System.out.println("Hello from the class delegate");
        execution.setVariable("var1", "Hello from the class delegate");
    }

}
```

Build a jar with this class, and add it to the classpath. In the Service task configuration, set the `class` property to using the fully qualified classname (in this case `my.company.MyJavaDelegate`).

### Spring Beans

Another option is to use a Spring bean. It is possible to use a `delegateExpression` on a service task that resolves
at run-time to an instance of `org.activiti.engine.delegate.JavaDelegate`. Alternatively, and probably more useful, is to use a general Spring bean. The application automatically scans all beans in the `com.activiti.extension.bean` package. For example:

```java
package com.activiti.extension.bean;

import org.activiti.engine.impl.pvm.delegate.DelegateExecution;
import org.springframework.stereotype.Component;

@Component("helloWorldBean")
public class HelloWorldBean {

        public void sayHello(DelegateExecution execution) {
                System.out.println("Hello from " + this);
                execution.setVariable("var3", " from the bean");
        }


}
```

Build a jar with this class, and add it to the classpath. To use this bean in a service task, set the `expression` property to `${helloWorldBean.sayHello(execution)}`.

It is possible to define custom configuration classes (using the Spring Java Config approach) if this is needed (for example when sharing dependencies between delegate beans, complex bean setup, etc.). The application automatically scans for configuration classes in the `package com.activiti.extension.conf;` package. For example:

```java
package com.activiti.extension.conf;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class CustomConfiguration {

        @Bean
        public SomeBean someBean() {
                return new SomeBean();
        }

}
```

Which can be injected in the bean that will be called in a service task:

```java
package com.activiti.extension.bean;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.activiti.extension.conf.SomeBean;

@Component("helloWorldBeanWithInjection")
public class HelloWorldBeanWithInjection {

        @Autowired
        private SomeBean someBean;

        public void sayHello() {
                System.out.println(someBean.getValue());
        }

}
```

To get the current user, it is possible to use the `com.activiti.common.security.SecurityUtils` helper class.

**Bean Whitelisting**

By default, you can specify any Spring bean for use in an expression. While this provides ease of use (since any beans you develop will be automatically scanned for as described above), it also increases the possibilities of misuse and security threats. To help prevent these issues from happening, you can whitelist Spring beans by making the following changes:

1. Open the `<InstallLocation>/tomcat/lib/activiti-app.properties` file.
2. Locate and set `beans.whitelisting.enabled` to true.

    ```text
    beans.whitelisting.enabled=true
    ```

    >**Note:** If this property is missing from the `activiti-app.propertie`s file, beans whitelisting is disabled.

3. To whitelist Spring beans, use the following configuration setting:

    ```text
    activiti-app/WEB-INF/classes/activiti/beans-whitelist.conf
    ```

**Example usage of bean whitelisting:**

To use a `userCount` variable in a **Display Text** field, `${userCount}`, add the following line in the Expression
property within a Service Task:

```javascript
${execution.setVariable('userCount', userService.getUserCount())}
```

If `beans.whitelisting.enabled` is set to false or the property is missing, the process is completed and the **Display Text** field should show the value of the `usercount` variable.

To complete the process successfully using bean whitelisting, you must set `beans.whitelisting.enabled` to true and add the bean name to `beans-whitelist.conf`:

```text
# list bean names that should be whitelisted
   userService
```

>**Note:** All beans declared in `com.activiti.extension.bean` are considered as whitelisted.

>**Note:** This note applies to users of Process Services version 1.6.0 to 1.6.2 inclusive as well as apps published in these versions. Whitelisting for publish tasks is exempt from version 1.6.3. If you wish to use tasks that publish to Box, Google Drive or Alfresco and have enabled bean whitelisting, the following beans need to be explicitly whitelisted in `beans-whitelist.conf`:
>
>* repositoryService
>* formRepository
>* objectMapper
>* relatedContentService
>* relatedContentProcessor
>* historyService
>* alfrescoMetadataProcessor

**Service Task Class Whitelisting**

This provides an alternative to bean whitelisting that enables more fine-grained control over what a developer can execute. 
For example, you can configure which patterns you allow to be executed using expressions.

You can also whitelist full class names or package patterns such as `com.activiti.*`.

To whitelist service task classes, do the following:

1. Open the `<InstallLocation>/tomcat/lib/activiti-app.properties` file.
2. Locate and set `service.task.class.whitelisting.enabled` to true.

    ```text
    class.whitelisting.enabled=true
    ```

    >**Note:** If this property is missing from the `activiti-app.properties` file, service task whitelisting is disabled.

3. **This step applies only to users of Process Services version 1.6.0 to 1.6.2 inclusive as well as apps published in these versions. Whitelisting for publish tasks is exempt from version 1.6.3.** To use Alfresco, Box or Google drive to publish tasks with service task whitelisting enabled, add the following entries to `activiti-app/WEB-INF/classes/activiti/whitelisted-classes.conf`:
    * `com.activiti.runtime.activiti.bean.BoxStepActivityBehavior`
    * `com.activiti.runtime.activiti.bean.GoogleDriveStepActivityBehavior`
    * `com.activiti.runtime.activiti.KickstartAlfrescoPublishDelegate`
    * `com.activiti.runtime.activiti.KickstartAlfrescoCloudPublishDelegate`

**Whitelisting Scripting Languages**

To whitelist scripting languages that, for example, might be used in script tasks such as JavaScript, juel and groovy, add the script types in `activiti-app/WEB-INF/classes/activiti/whitelisted-scripts.conf`:

```text
#Here you can specify which script types are allowed to be executed
javascript
js
ecmascript
groovy
juel
```

>**Note:** Whitelisting configuration affects any type of script execution whether this involves script tasks or any other situation in which a script might be used. Also note that this is verified at runtime. If a scripting language is not whitelisted the related task or activity will not run.

**Class whitelisting in JavaScript**

You can also configure whitelisting for JavaScript classes that are available for use in JavaScript. The following steps show you how to do this. They are, however, only applicable where you have enabled secure scripting for JavaScript. This will be the case if you have set the property `javascript.secure-scripting.enabled` to true:

```text
javascript.secure-scripting.enabled=true
```

1. Open the `<InstallLocation>/tomcat/lib/activiti-app.properties` file.
2. Locate and set `javascript.secure-scripting.enable-class-whitelisting` to true.

    ```text
    javascript.secure-scripting.enable-class-whitelisting = true
    ```

3. To allow the execution of JavaScript classes, add them to `activiti-app/WEB-INF/classes/activiti/javascript-whitelist-classes.conf`:

    ```text
    java.lang.System
    java.util.ArrayList
    org.apache.tomcat.util.log.SystemLogHandler
    ```

>**Note:** The enablement of secure scripting for Java classes used in JavaScript is turned on when either the setting is missing from the properties file or commented out.

### Default Spring Beans

Use the following sections for information about the default spring beans in Process Services.

#### Audit Log Bean (auditLogBean)

The `auditLogBean` can be used to generate audit logs in `.pdf` format for a completed process instance or a completed task. The log will be saved as a field value for the process and the task (if a task audit log is generated).

>**Note:** Audit logs can only be used against a completed process instance or a completed task.

The following code can be used in the expression of a service task to generate a process instance audit log named *My first process instance audit log*. The third argument determines if the current date shall be appended to the file name. The pdf will be associated with the process field `myFieldName`.

```javascript
${auditLogBean.generateProcessInstancePdf(execution, 'My first process instance audit log', true, 'myFieldName')}
```

To create a task audit log named *My first task audit log* add the following expression to the "complete" event in a task listener. Again the third argument determines if the current date shall be appended to the file name. The pdf will be associated with the field `myFieldName`.

```javascript
${auditLogBean.generateTaskPdf(task, 'My first task audit log', true, 'myFieldName')}
```

You can view the audit logs from the My Tasks app by clicking the "Audit Log" link when viewing the details of a completed process or task. When doing so the following two rest calls are made.

Process instance audit log:

```bash
GET app/rest/process-instances/{process-instance-id}/audit
```

Task audit log:

```bash
GET app/rest/tasks/{task-id}/audit
```

#### Document Merge Bean (documentMergeBean)

The `documentMergeBean` can be used to merge the content of multiple documents (files of type `.doc` or `.docx`) from a process into a single document which will be become the value of a provided process variable. The file name of the new document will be set to the file name of the first field in the list followed by the string "_merged" and the suffix from the same field.

In the following example, the content of `myFirstField` and `mySecondField` will be merged into a new document with the field ID set to `myFirstField` and the filename set to:

`<filename-from-myFirstField>_merged.<filenameSuffix-from-myFirstFields>`

The new document will become the value of a process variable named `myProcessVariable`.

```javascript
${documentMergeBean.mergeDocuments('myFirstField,mySecondField', 'myProcessVariable', execution)}
```

#### Email Bean (emailBean)

The `emailBean` can be used to retrieve the email of the current user or the process initiator.

To get the email of the current user use the following expression where `123` is the `userId`:

```javascript
${emailBean.getEmailByUserId(123, execution)}
```

To get the email of the process initiator use the following expression:

```javascript
${emailBean.getProcessInitiator(execution)}
```

#### User Info Bean (userInfoBean)

The `userInfoBean` makes it possible to get access to general information about a user or just the email of a user.

To get general information about a user (the data that can be found in `com.activiti.domain.idm.User`), use the following expression where `userId` is the database ID of the user and can be supplied either as a `Long` or a `String`:

```javascript
${userInfoBean.getUser(123, execution)}
```

To get the email of a user use the following expression where `123` is the database id of the user and can be supplied either as a `Long` or a `String`:

```javascript
${userInfoBean.getEmail(123, execution)}
```

To get the first name of a user use the following expression where `123` is the database id of the user and can be supplied either as a `Long` or a `String`:

```javascript
${userInfoBean.getFirstName(123, execution)}
```

To get the last name of a user use the following expression where `123` is the database id of the user and can be supplied either as a `Long` or a `String`:

```javascript
${userInfoBean.getLastName(123, execution)}
```

To get both first name and last name of a user use the following expression where `123` is the database id of the user and can be supplied either as a `Long` or a `String`:

```javascript
${userInfoBean.getFullName(123, execution)}
```

To get a user object representing the current user use the following expression where the returned value is an instance of `LightUserRepresentation` containing fields like `id`, `firstName`, `lastName`, `email`, `externalId`, `pictureId`:

```javascript
${userInfoBean.getCurrentUser()}
```

To get a user’s primary group name use the following expression where `123` is the database id of the user and can be supplied either as a `Long` or a `String`:

```javascript
${userInfoBean.getPrimaryGroupName(123)}
```

To get a group object representing a user’s primary group use the following expression where the return value is an instance of `LightGroupRepresentation`, containing id, name, externalId and status, and where `123` is the database id of the user and can be supplied either as a `Long` or a `String`:

```javascript
${userInfoBean.getPrimaryGroup(123)}
```

### Hook points

A *hook point* is a place where custom logic can be added. Typically this is done by implementing a certain interface and putting the class implementing the interface on the classpath where it can be found by the classpath component scanning (package `com.activiti.extension.bean` for example).

#### Login/LogoutListener

**interface**: `com.activiti.api.security.LoginListener` and `com.activiti.api.security.LogoutListener`

**Maven module**: `activiti-app-logic`

An implementation of this class will get a callback when a user logs in or logs out.

Example:

```java
package com.activiti.extension.bean;

@Component
public class MyLoginListener implements LoginListener {
    private static final Logger logger = LoggerFactory.getLogger(GfkLoginListener.class);

    public void onLogin(User user) {
            logger.info("User " + user.getFullName() + " has logged in");
    }
}
```

#### Process engine configuration configurer

**interface**: `com.activiti.api.engine.ProcessEngineConfigurationConfigurer`

**Maven module**: `activiti-app-logic`

An implementation of this class will get called when the Activiti process engine configuration is initialized, but before the process engine is built. This allows for customization to the process engine configuration.

Example:

```java
@Component
public class MyProcessEngineCfgConfigurer implements ProcessEngineConfigurationConfigurer {
    public void processEngineConfigurationInitialized( SpringProcessEngineConfiguration springProcessEngineConfiguration) {
            ...​ // Tweaking the process engine configuration
    }
}
```

#### Rule engine configuration configurer

**interface**: `com.activiti.api.engine.DmnEngineConfigurationConfigurer`

**Maven module**: `activiti-app-logic`

An implementation of this class will get called when the Process Services rule engine configuration is initialized,
but before the process engine is built. This allows for customization to the rule engine configuration.

Example:

```java
@Component
public class MyDmnEngineCfgConfigurer implements DmnEngineConfigurationConfigurer {
    public void dmnEngineConfigurationInitialized(DmnEngineConfiguration dmnEngineConfiguration) {
            ... // Tweaking the rule engine configuration
    }
}
```

#### Process Engine event listeners

It is possible to listen to events fired by the Process Engine. By default (and if enabled) there is a listener that captures these events, processes them before sending them to Elasticsearch (which is used for analytics). If the event data should be going somewhere else, for example an external BI warehouse, the following interface should be implemented and can be used to execute any logic when the event is fired.

See the *example apps* folder that comes with Process Services. It has a *jdbc-event-listener* folder, in which a Maven project can be found that captures these events and stored them relationally in another database.

**interface**: `com.activiti.service.runtime.events.RuntimeEventListener`

**Maven module**: `activiti-app-logic`

All implementations exposing this interface will be injected into the process engine at run time.

Example:

```java
package com.activiti.extension.bean;

import com.activiti.service.runtime.events.RuntimeEventListener;
import org.activiti.engine.delegate.event.ActivitiEvent;

@Component
public class PostgresEventListener implements RuntimeEventListener {

    @Override
    public boolean isEnabled() {
        return true;
    }

    @Override
    public void onEvent(ActivitiEvent activitiEvent) {
        // TODO: handle event here
    }

    @Override
    public boolean isFailOnException() {
        return false;
    }
}
```

#### Processing document generation variables

**interface**: `com.activiti.api.docgen.TemplateVariableProcessor`

**Maven module**: `activiti-app-logic`

This section describes the implementation of the document generation task for generating a document based on a MS Word docx template.

An implementation of this class will get called before the variable is passed to the template processor, making it possible to change the value that will be used as the variable name in the template.

Example:

```java
@Component
public class MyTemplateVariableProcessor implements TemplateVariableProcessor {
    public Object process(RuntimeDocumentTemplate runtimeDocumentTemplate, DelegateExecution execution, String variableName, Object value) {
            return value.toString() + "___" + "HELLO_WORLD";
    }
}
```

Using the above example, you can add *"HELLO_WORLD"* to all variable usages in the template. However, you can also add sophisticated implementations based on process definition lookup using the process definition ID from the execution and inject the `RepositoryService` in your bean.

In addition to the process definition, the `runtimeDocumentTemplate` is passed to distinguish for which process and template the variables are being prepared.

>**Note:** Only variables with the format `variables.get("myVariable")` in the .docx template will be passed to the `TemplateVariableProcessor` implementation.

#### Business Calendar

Use the business calendar when calculating due dates for tasks.

You can override the default business calendar implementation, for example, to include bank holidays, company holidays, and so on. To override the default implementation, add a Spring bean implementing the `com.activiti.api.calendar.BusinessCalendarService` to the classpath with the `@Primary` notation.

Check the Javadoc on the `BusinessCalendarService` for more information.

```java
@Primary
@Service
public class MyBusinessCalendarService implements BusinessCalendarService {

  ...

}
```

Below is an example implementation that takes weekend days into account when calculating due dates.

```java
@Primary
@Service
public class SkipWeekendsBusinessCalendar implements BusinessCalendarService {

    protected static final int DAYS_IN_WEEK = 7;
    protected List<Integer> weekendDayIndex;

    protected DateFormat dateFormat = new SimpleDateFormat("dd-MM-yyyy");

    public SkipWeekendsBusinessCalendar() {

        // add Saturday and Sunday as weekend days
        weekendDayIndex.add(6);
        weekendDayIndex.add(7);
    }

    public Date addToDate(Date date, int years, int months, int days, int hours, int minutes, int seconds) {
        return calculateDate(new DateTime(date), years, months, days, hours, minutes, seconds, 1);
    }

    public Date subtractFromDate(Date date, int years, int months, int days, int hours, int minutes, int seconds) {
        return calculateDate(new DateTime(date), years, months, days, hours, minutes, seconds, -1);
    }

    protected Date calculateDate(DateTime relativeDate, int years, int months, int days, int hours, int minutes, int seconds, int step) {
        // if date is on a weekend skip to a working day
        relativeDate = skipWeekEnds(relativeDate, step);
        Period period = new Period(years, months, 0, days, hours, minutes, seconds, 0);

        // add weekends to period
        period = period.plusDays(countWeekEnds(relativeDate, period, step));

        // add/subtract period to get the final date, again if date is on a weekend skip to a working day
        return skipWeekEnds(addPeriod(relativeDate, period, step), step).toDate();
    }

    protected DateTime addPeriod(DateTime relativeDate, Period period, int step) {
        if (step < 0) {
            return relativeDate.minus(period);
        }
        return relativeDate.plus(period);
    }

    protected DateTime skipWeekEnds(DateTime relativeDate, int step) {
        while(weekendDayIndex.contains(relativeDate.getDayOfWeek())) {
            relativeDate = relativeDate.plusDays(step);
        }
        return relativeDate;
    }

    protected int countWeekEnds(DateTime relativeDate, Period period, int step) {
        // get number of days between two dates
        int days = Math.abs(Days.daysBetween(relativeDate, addPeriod(relativeDate, period, step)).getDays());
        int count = 0;

        for(int weekendDay : weekendDayIndex) {
            count+=countWeekDay(relativeDate, weekendDay, days, step);
        }
        return count;
    }

    protected int countWeekDay(DateTime relativeDate, int weekDay, int days, int step) {
        int count = 0;
        DateTime dt = relativeDate.toDateTime();

        // if date's day of week is not the target day of week
        // skip to target day of week
        if(weekDay != relativeDate.getDayOfWeek()) {
            int daysToSkip = 0;

            if (step > 0) {
                if (weekDay > relativeDate.getDayOfWeek()) {
                    daysToSkip = weekDay - relativeDate.getDayOfWeek();
                } else {
                    daysToSkip = weekDay - relativeDate.getDayOfWeek() + DAYS_IN_WEEK;
                }
            } else {
                if (weekDay > relativeDate.getDayOfWeek()) {
                    daysToSkip = Math.abs(weekDay - relativeDate.getDayOfWeek() - DAYS_IN_WEEK);
                } else {
                    daysToSkip = relativeDate.getDayOfWeek() - weekDay;
                }
            }

            // return if target day of week is beyond range of days
            if (daysToSkip > days) {
                return 0;
            }

            count++;
            dt = dt.plusDays(daysToSkip * step);
            days-=daysToSkip;
        }

        if (days>=DAYS_IN_WEEK) {
            dt = dt.plusDays(days * step);
            count+=(Weeks.weeksBetween(relativeDate, dt).getWeeks() * step);
        }

        return count;
    }

    @Override
    public DateFormat getStringVariableDateFormat() {
        return dateFormat;
    }
```

### Custom REST endpoints

It’s possible to add custom REST endpoints to the BPM Suite, both in the regular REST API (used by the BPM Suite html/javascript UI) and the *public* API (using basic authentication instead of cookies).

The REST API is built using Spring MVC. Please check the [Spring MVC documentation](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/mvc.html){:target="_blank"} on how to create new Java beans to implement REST endpoints.

To build against the REST logic of Process Services and its specific dependencies, add following dependency to your Maven `pom.xml` file:

```xml
<dependencies>
    <dependency>
        <groupId>com.activiti</groupId>
        <artifactId>activiti-app-rest</artifactId>
        <version>${suite.version}</version>
    </dependency>
</dependencies>
```

A very simple example is shown below. Here, the Process Services `TaskService` is injected and a custom response is fabricated. Of course, this logic can be anything.

```java
package com.activiti.extension.rest;

import com.activiti.domain.idm.User;
import com.activiti.security.SecurityUtils;
import org.activiti.engine.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/rest/my-rest-endpoint")
public class MyRestEndpoint {
    @Autowired
    private TaskService taskService;

    @RequestMapping(method = RequestMethod.GET, produces = "application/json")
    public MyRestEndpointResponse executeCustonLogic() {
        User currentUser = SecurityUtils.getCurrentUserObject();
        long taskCount = taskService.createTaskQuery().taskAssignee(String.valueOf(currentUser.getId())).count();

        MyRestEndpointResponse myRestEndpointResponse = new MyRestEndpointResponse();
        myRestEndpointResponse.setFullName(currentUser.getFullName());
        myRestEndpointResponse.setTaskCount(taskCount);
        
        return myRestEndpointResponse;
    }

    private static final class MyRestEndpointResponse {
        private String fullName;
        private long taskCount;
        
        // Getters and setters
    }
}
```

>**Note.** The bean needs to be in the `com.activiti.extension.rest` package to be found.

Create a jar containing this class, and add it to the classpath.

A class like this in the `com.activiti.extension.rest` package will be added to the rest endpoints for the application (e.g. for use in the UI), which use the cookie approach to determine the user. **The url will be mapped under /app**. So, if logged in into the UI of the BPM Suite, one could go to `http://localhost:8080/activiti-app/app/rest/my-rest-endpoint` and see the result of the custom rest endpoint:

```json
{"fullName":" Administrator","taskCount":8}
```

To add a custom REST endpoint to the *public REST API*, protected by basic authentication, a similar class should be placed in the `com.activiti.extension.api package`:

```java
package com.activiti.extension.api;

import com.activiti.domain.idm.User;
import com.activiti.security.SecurityUtils;
import org.activiti.engine.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/enterprise/my-api-endpoint")
public class MyApiEndpoint {
    @Autowired
    private TaskService taskService;

    @RequestMapping(method = RequestMethod.GET, produces = "application/json")
    public MyRestEndpointResponse executeCustonLogic() {
        User currentUser = SecurityUtils.getCurrentUserObject();
        long taskCount = taskService.createTaskQuery().taskAssignee(String.valueOf(currentUser.getId())).count();

        MyRestEndpointResponse myRestEndpointResponse = new MyRestEndpointResponse();
        myRestEndpointResponse.setFullName(currentUser.getFullName());
        myRestEndpointResponse.setTaskCount(taskCount);
        
        return myRestEndpointResponse;
    }

    private static final class MyRestEndpointResponse {
        private String fullName;
        private long taskCount;

        // Getters and setters
    }
}
```

Note that the endpoint needs to have `/enterprise` as first element in the url, as this is configured in the `SecurityConfiguration` to be protected with basic authentication (more specific, the `api/enterprise/*` is).

Which can be accessed like the regular API:

```bash
curl -u admin@app.activiti.com:password http://localhost:8080/activiti-app/api/enterprise/my-api-endpoint

{"fullName":" Administrator","taskCount":8}
```

>**Note:** Due to classloading, it is currently not possible to put jars with these custom rest endpoints in the global or common classpath (for example `tomcat/lib` for Tomcat). They should be put in the web application classpath (for example `WEB-INF/lib`).

### Custom rule expression functions

The rule engine uses MVEL as an expression language. In addition to the built-in MVEL expression functions there are some additional custom expression functions provided. These are accessible through the structured expression editor within the decision table editor.

The provided custom methods can be overridden by your own custom expression functions or custom methods can be added. This is possible via a hook point in the rule engine configuration (see [Rule engine configuration configurer](#rule-engine-configuration-configurer)).

You can configure the Engine with additional expression functions by implementing `CustomExpressionFunctionRegistry`.

**interface**: `com.activiti.dmn.engine.impl.mvel.config.CustomExpressionFunctionRegistry`

**Maven module**: `activiti-dmn-engine`

Example:

```java
import com.activiti.dmn.engine.CustomExpressionFunctionRegistry;
import org.springframework.stereotype.Component;

import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;

@Component
public class MyCustomExpressionFunctionsRegistry implements CustomExpressionFunctionRegistry {

    public Map<String, Method> getCustomExpressionMethods() {
        Map<String,Method> myCustomExpressionMethods = new HashMap<>();

        try {
            String expressionToken = "dosomething";
            Method customExpressionMethod = SomeClass.class.getMethod("someMethod", String.class);
            myCustomExpressionMethods.put(expressionToken, customExpressionMethod);
        } catch (NoSuchMethodException e) {
            // handle exception
        }

        return myCustomExpressionMethods;
    }
}
```

This registry must be provided to the rule engine configuration using the hook point (see [Rule engine configuration configurer](#rule-engine-configuration-configurer)).

This example adds the expression function from the example above to the default custom expression functions.

Example:

```java
import com.activiti.dmn.engine.DmnEngineConfiguration;
import org.springframework.beans.factory.annotation.Autowired;

public class MyDmnEngineCfgConfigurer implements DmnEngineConfigurationConfigurer {
    @Autowired
    MyCustomExpressionFunctionsRegistry myExpressionFunctionRegistry;

    public void dmnEngineConfigurationInitialized(DmnEngineConfiguration dmnEngineConfiguration) {
        dmnEngineConfiguration.setPostCustomExpressionFunctionRegistry(myExpressionFunctionRegistry);
    }
}
```

Overriding the default custom expression functions can be done by:

```java
dmnEngineConfiguration.setCustomExpressionFunctionRegistry(myExpressionFunctionRegistry);
```

## Custom Data Models

You can create Custom Data Models that connect to external sources and perform custom data operations when working with entity objects.

Implement `AlfrescoCustomDataModelService` to manage operations such as insert, update, and select data in Custom Data Models.

**interface**: `com.activiti.api.datamodel.AlfrescoCustomDataModelService`

**maven module**: `activiti-app-logic`

Follow these steps to implement the `AlfrescoCustomDataModelService` interface:

1. Create an external class named `AlfrescoCustomDataModelServiceImpl` and add it to the classpath.

    Note that it should be in a package that can be scanned, such as `com.activiti.extension.bean`.

2. Implement the class as follows:

    ```java
    package com.activiti.extension.bean;
    
    import java.util.List;
    
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.stereotype.Service;
    
    import com.activiti.api.datamodel.AlfrescoCustomDataModelService;
    import com.activiti.model.editor.datamodel.DataModelDefinitionRepresentation;
    import com.activiti.model.editor.datamodel.DataModelEntityRepresentation;
    import com.activiti.runtime.activiti.bean.datamodel.AttributeMappingWrapper;
    import com.activiti.variable.VariableEntityWrapper;
    import com.fasterxml.jackson.databind.ObjectMapper;
    import com.fasterxml.jackson.databind.node.ObjectNode;
    
    @Service
    public class AlfrescoCustomDataModelServiceImpl implements AlfrescoCustomDataModelService {
    
        @Autowired
        protected ObjectMapper objectMapper;
    
        @Override
        public String storeEntity(List<AttributeMappingWrapper> attributeDefinitionsAndValues, DataModelEntityRepresentation entityDefinition,
                DataModelDefinitionRepresentation dataModel) {
            // save entity data and return entity id
        }
    
        @Override
        public ObjectNode getMappedValue(DataModelEntityRepresentation entityValue, String mappedName, Object variableValue) {
            // fetch entity data and return as an ObjectNode
        }
    
        @Override
        public VariableEntityWrapper getVariableEntity(String keyValue, String variableName, String processDefinitionId, DataModelEntityRepresentation entityValue) {
            // fetch entity data and return as a VariableEntityWrapper
        }
    
    }
    ```

This implementation of `AlfrescoCustomDataModelServiceImpl` class is called, for example, when a select, insert, or update operation on a custom data model is performed.

## Custom reports

There are a number of out-of-the-box reports in the Analytics app, which can be augmented with your own custom reports.

Custom reports have full access to the Elasticsearch indexes generated by Process Services when it is enabled.

See [Event processing for analytics]({% link process-services/latest/config/external.md %}#event-processing-for-analytics) for details on how to configure events to be sent to Elasticsearch.

The following section assumes that you have a reasonable understanding of what Elasticsearch is and an understanding of indexes, types and type mappings. The [Elasticsearch Definitive Guide](https://www.elastic.co/guide/en/elasticsearch/guide/1.x/index.html){:target="_blank"} is a great learning resource if you are new to the engine and there is also a [Reference Guide](https://www.elastic.co/guide/en/elasticsearch/reference/1.7/index.html){:target="_blank"} which you should find helpful to refer to as you start using it directly yourself.

### Implementing custom reports

Assuming that you have started to see some data show up in the ElasticSearch store and therefore in the out-of-the-box reports, and you have used the Sense tool or cURL to develop some custom search queries of your own, you are ready to start implementing the custom Spring bean required in order to plug the report into the Process Services UI.

1. Basic concepts

    A custom report is a custom section available in the Analytics app and also within each published app, which shows one or more custom reports.

    Each report is implemented by a Spring bean which is responsible for two things:

    1. Perform an ElasticSearch search query using the Java client API.

    2. Convert the search results (hits or aggregations) into chart or table data and add this to the response.

    The UI will automatically display the correct widgets based on the data that your bean sends.

2. Bean implementation

    Your Spring bean will be discovered automatically via annotations but must be placed under the package `com.activiti.service.reporting`. Since this package is used for the out-of-the-box reports it is recommended that custom reports use the sub-package such as `com.activiti.service.reporting.custom`.

    The overall structure of the class will be as follows, for the full source please see the web link at the end of this section.

    ```java
    package com.activiti.service.reporting.custom;
    
    import com.activiti.domain.reporting.ParametersDefinition;
    import com.activiti.domain.reporting.ReportDataRepresentation;
    import com.activiti.service.api.UserCache;
    import com.activiti.service.reporting.AbstractReportGenerator;
    import org.activiti.engine.ProcessEngine;
    import org.elasticsearch.client.Client;
    import org.springframework.stereotype.Component;
    
    import java.util.Map;
    
    @Component(CustomVariablesReportGenerator.ID)
    public class CustomVariablesReportGenerator extends AbstractReportGenerator {
    
        public static final String ID = "report.generator.fruitorders";
        public static final String NAME = "Fruit orders overview";
    
        @Override
        public String getID() {
            return ID;
        }
    
        @Override
        public String getName() {
            return NAME;
        }
    
        @Override
        public ParametersDefinition getParameterDefinitions(Map<String, Object> parameterValues) {
            return new ParametersDefinition();
        }
    
        @Override
        public ReportDataRepresentation generateReportData(ProcessEngine processEngine,
                                                           Client elasticSearchClient, String indexName, UserCache userCache,
                                                           Map<String, Object> parameterMap) {
    
            ReportDataRepresentation reportData = new ReportDataRepresentation();
    
            // Perform queries and add report data here
    
            return reportData;
        }
    ```

    You must implement the `generateReportData()` method which is declared abstract in the superclass, and you can choose to override the `getParameterDefinitions()` method if you need to collect some user-selected parameters from the UI to use in your query.

3. Implementing `generateReportData()`

    The `generateReportData()` method of your bean is responsible for two things:

    * Perform one or more ElasticSearch queries to fetch report data

    * Populate chart/table data from the query results

    A protected helper method `executeSearch()` is provided which provides a concise syntax to execute an ElasticSearch search query given a query and optional aggregation, the implementation of which also provides logging of the query generated by the Java client API before it is sent. This can help with debugging your queries using Sense, or assist you in working out why the Java client is not generating the query you expect.

    ```java
    return executeSearch(elasticSearchClient,
                    indexName,
                    ElasticSearchConstants.TYPE_VARIABLES,
                    new FilteredQueryBuilder(
                            new MatchAllQueryBuilder(),
                            FilterBuilders.andFilter(
                                    new TermFilterBuilder("processDefinitionKey", PROCESS_DEFINITION_KEY),
                                    new TermFilterBuilder("name._exact_name", "customername")
                            )
                    ),
                    AggregationBuilders.terms("customerOrders").field("stringValue._exact_string_value")
            );
    ```

    The log4j 2 configuration required to log queries being sent to ElasticSearch via `executeSearch()` is as follows

    ```text
    log4j.logger.com.activiti.service.reporting.AbstractReportGenerator=DEBUG
    ```

    Alternatively you can manually execute any custom query directly via the `Client` instance passed to the `generateReportData()` method, for example:

    ```java
    return elasticSearchClient
                    .prepareSearch(indexName)
                    .setTypes(ElasticSearchConstants.TYPE_PROCESS_INSTANCES)
                    .setQuery(new FilteredQueryBuilder(new MatchAllQueryBuilder(), applyStatusProcessFilter(status)))
                    .addAggregation(
                            new TermsBuilder(AGGREGATION_PROCESS_DEFINITIONS).field(EventFields.PROCESS_DEFINITION_ID)
                                    .subAggregation(new FilterAggregationBuilder(AGGREGATION_COMPLETED_PROCESS_INSTANCES)
                                            .filter(new ExistsFilterBuilder(EventFields.END_TIME))
                                            .subAggregation(new ExtendedStatsBuilder(AGGREGATION_STATISTICS).field(EventFields.DURATION))));
    ```

    Generating chart data from queries can be accomplished easily using the converters in the `com.activiti.service.reporting.converters` package. This avoids the need to iterate over returned query results in order to populate chart data items.

    Initially two converters `AggsToSimpleChartBasicConverter` and `AggsToMultiSeriesChartConverter` are provided to populate data for pie charts (which take a single series of data) and bar charts (which take multiple series) respectively. These two classes are responsible for iterating over the structure of the ES data, while the member classes of `com.activiti.service.reporting.converters.BucketExtractors` are responsible for extracting an actual value from the buckets returned in the data.

    ```java
    ReportDataRepresentation reportData = new ReportDataRepresentation();
    
    PieChartDataRepresentation pieChart = new PieChartDataRepresentation();
    pieChart.setTitle("No. of orders by customer");
    pieChart.setDescription("This chart shows the total number of orders placed by each customer");
    
    new AggsToSimpleChartBasicConverter(searchResponse, "customerOrders").setChartData(
            pieChart,
            new BucketExtractors.BucketKeyExtractor(),
            new BucketExtractors.BucketDocCountExtractor()
    );
    
    reportData.addReportDataElement(pieChart);
    
    SingleBarChartDataRepresentation chart = new SingleBarChartDataRepresentation();
    chart.setTitle("Total quantities ordered per month");
    chart.setDescription("This chart shows the total number of items that were ordered in each month");
    chart.setyAxisType("count");
    chart.setxAxisType("date_month");
    
    new AggsToMultiSeriesChartConverter(searchResponse, "ordersByMonth").setChartData(
            chart,
            new BucketExtractors.DateHistogramBucketExtractor(),
            new BucketExtractors.BucketAggValueExtractor("totalItems")
    );
    
    reportData.addReportDataElement(chart);
    ```

    For more details see the full source on the [activiti-custom-reports](https://github.com/Alfresco/activiti-custom-reports){:target="_blank"} GitHub project.

## Custom identity synchronization

Process Services needs user, group, and membership information in its database. The main reason is performance (for example quick user/group searches) and data consistency (for example models are linked to users through foreign keys). In the Process Services logic, this is typically referred to as Identity Management (IDM).

Out of the box, all IDM data is stored directly in the database. So when you create a user or group as a tenant administrator, the data ends up in the database tables.

However, typically, the users/groups of a company are managed in a centralized data store such as LDAP (or Active Directory). Process Services can be configured to connect to such a server and synchronize the IDM data to the database table.

See [External Identity Management]({% link process-services/latest/config/authenticate.md %}#ldap-and-active-directory) for more information on how to set this up. The basic idea behind it is that the LDAP server will periodically be polled and the IDM data in the database tables will be synchronized: created, updated or deleted depending on what the LDAP server returns and what currently is in the database tables.

This section describes what is needed to have a similar synchronization of IDM data coming from another source. The `com.activiti.service.idm.LdapSyncService` responsible for synchronizing IDM data from an LDAP/Active Directory store, uses the same hook points as the ones described below and can thus be seen as an advanced example.

### Example implementation

Create a simple example synchronization service that demonstrates clearly the concepts and classes to be used. In this example, use a simple text file to represent our *external IDM source*. The `users.txt` looks as follows (each line is a user and user data is separated by semi-colons):

```text
jlennon;John;Lennon;john@beatles.com;johnpassword;10/10/2015
rstarr;Ringo;Starr;ringo@beatles.com;ringopassword;11/10/2015
gharrison;George;Harrison;george@beatles.com;georgepassword;12/10/2015
pmccartney;Paul;McCartney;paul@beatles.com;paulpassword;13/10/2015
```

The `groups.txt` file is similar (the group name followed by the member ids and a timestamp):

```text
beatles:jlennon;rstarr;gharrison;pmccartney:13/10/2015
singers:jlennon;pmccartney:17/10/2015
```

The application expects *one* instance implementing the `com.activiti.api.idm.ExternalIdmSourceSyncService` interface to be configured when synchronizing with an external IDM source. This interface requires a few methods to either synchronous or asynchronous do a full or differential sync. In a full sync, all data is looked at and compared. A differential sync only returns what has changed since a certain date. The latter is of course used for performance reasons. For example, the default settings for LDAP do a full sync every night and a differential sync every four hours.

You can also implement the `com.activiti.api.idm.ExternalIdmSourceSyncService` interface directly, but there is an easier way: all the logic to fetch data from the tables, compare, create, update or delete users, groups or membership is encapsulated in the `com.activiti.api.idm.AbstractExternalIdmSourceSyncService` class. It is advised to extend this class when creating a new external source synchronization service, as in that case the only logic that needs to be written is the actual fetching of the IDM data from the external source.

Create a `FileSyncService` class. Note the package, `com.activiti.extension.bean`, which is automatically component scanned. The class is annotated with `@Component` (`@Service` would also work).

```java
package com.activiti.extension.bean;

@Component
public class FileSyncService extends AbstractExternalIdmSourceSyncService {
  ...
}
```

The acom.activiti.api.idm.ExternalIdmSourceSyncServicea defines the different abstract methods that can be implemented. For example:

The `additionalPostConstruct()` method will be called after the bean is constructed and the dependencies are injected.

```java
protected void additionalPostConstruct() {
                // Nothing needed now
}
```

It’s the place to add additional post construction logic, like reading properties from the configuration file. Note the `env` variable is available for that, which is a standard `org.springframework.core.env.Environment` instance:

```java
protected void additionalPostConstruct() {
    myCustomConfig = env.getProperty("my.custom.property");
}
```

The `getIdmType()` method simply returns a `String` identifying the external source type. It is used in the logging
that is produced when the synchronization is happening.

```java
protected String getIdmType() {
  return "FILE";
}
```

The `isFullSyncEnabled(Long tenantId)` and `isDifferentialSyncEnabled(Long tenantId)` configures whether or not respectively the *full* and/or the *differential* synchronization is enabled.

```java
protected boolean isFullSyncEnabled(Long tenantId) {
  return true;
}

protected boolean isDifferentialSyncEnabled(Long tenantId) {
  return false;
}
```

>**Note** that the `tenantId` is passed here. In a non-multitenant setup, this parameter can simply be ignored. All methods of this superclass have the `tenantId` parameter. In a multi-tenant setup, one should write logic to loop over all the tenants in the system and call the sync methods for each of the tenants separately.

The following two methods will configure when the synchronizations will be scheduled (and executed asynchronously). The return value of these methods should be a (Spring-compatible) cron expression. Note that this typically will be configured in a configuration properties file rather than hardcoded. When `null` is returned, that particular synchronization won’t be scheduled.

```java
protected String getScheduledFullSyncCronExpression() {
    return "0 0 0 * * ?"; // midnight
}

protected String getScheduledDifferentialSyncCronExpression() {
    return null;
}
```

Now we get to the important part of the implementation: the actual fetching of users and groups. This is the method that is used during a *full synchronization*.

```java
protected ExternalIdmQueryResult getAllUsersAndGroupsWithResolvedMembers(Long tenantId) {
    try {
      List<ExternalIdmUserImpl> users = readUsers();
      List<ExternalIdmGroupImpl> groups = readGroups(users);
      return new ExternalIdmQueryResultImpl(users, groups);
    } catch (Exception e) {
      e.printStackTrace();
    }
    return null;
}
```

The return result, an instance of `com.activiti.domain.sync.ExternalIdmQueryResult`, which has a list of users in the form of `com.activiti.domain.sync.ExternalIdmUser` instances and a list of groups in the form of `com.activiti.domain.sync.ExternalIdmGroup` instances.

Note that each group has its members and child groups in it. Also note that these are all *interfaces*, so you are free to return any instance that implements these interfaces. By default there are simple POJO implementations of said interfaces: `com.activiti.domain.sync.ExternalIdmQueryResultImpl`, `com.activiti.domain.sync.ExternalIdmUserImpl` and `com.activiti.domain.sync.ExternalIdmGroupImpl`. These POJOs are also used in the example implementation above.

>**Important note**: the `ExternalIdmUser` interface also defines a `getPassword()` method. Only return the actual password here if you want the user to authenticate against the default tables. The returned password will be securely hashed and stored that way. Return `null` if the authentication is done against an external system (LDAP is such an example). See further down to learn more about custom authentication.

The `readUsers()` and `readGroups()` methods will read the `.txt` mentioned above from the classpath and create instances of user and groups classes using the information in those files. For example:

```java
protected List<ExternalIdmUserImpl> readUsers() throws IOException, ParseException {
    List<ExternalIdmUserImpl> users = new ArrayList<ExternalIdmUserImpl>();

    InputStream inputStream = this.getClass().getClassLoader().getResourceAsStream("users.txt");
    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
    String line = bufferedReader.readLine();
    while (line != null) {

        String[] parsedLine = line.split(";");

        ExternalIdmUserImpl user = new ExternalIdmUserImpl();
        user.setId(parsedLine[0]);
        user.setOriginalSrcId(parsedLine[0]);
        user.setFirstName(parsedLine[1]);
        user.setLastName(parsedLine[2]);
        user.setEmail(parsedLine[3]);
        user.setPassword(parsedLine[4]);
        user.setLastModifiedTimeStamp(dateFormat.parse(parsedLine[5]));

        users.add(user);
        line = bufferedReader.readLine();
    }

    inputStream.close();
    return users;
}

protected List<ExternalIdmGroupImpl> readGroups(List<ExternalIdmUserImpl> users) throws IOException, ParseException {

    List<ExternalIdmGroupImpl> groups = new ArrayList<ExternalIdmGroupImpl>();

    InputStream inputStream = this.getClass().getClassLoader().getResourceAsStream("groups.txt");
    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
    String line = bufferedReader.readLine();
    while (line != null) {

        String[] parsedLine = line.split(":");
        String groupId = parsedLine[0];

        ExternalIdmGroupImpl group = new ExternalIdmGroupImpl();
        group.setOriginalSrcId(groupId);
        group.setName(groupId);

        List<ExternalIdmUserImpl> members = new ArrayList<ExternalIdmUserImpl>();
        String[] memberIds = parsedLine[1].split(";");
        for (String memberId : memberIds) {
                for (ExternalIdmUserImpl user : users) {
                        if (user.getId().equals(memberId)) {
                                members.add(user);
                        }
                }
        }
        group.setUsers(members);

        group.setLastModifiedTimeStamp(dateFormat.parse(parsedLine[2]));

        groups.add(group);
        line = bufferedReader.readLine();
    }

    inputStream.close();
    return groups;
}
```

For the *differential synchronization* a similar implementation could be made. Note that now a timestamp is passed, which indicates that the method should only return user/groups that are changed since that timestamp.

```java
protected List<? extends ExternalIdmUser> getUsersModifiedSince(Date latestSyncDate, Long tenantId) {
...​
}

protected List<? extends ExternalIdmGroup> getGroupsModifiedSince(Date latestSyncDate, Long tenantId) {
....
}
```

The last two methods we need to implement are to indicate which users should become a tenant admin (or a tenant manager in a multi-tenant setup). This method should return an array of string with the *id used in the external IDM store*. More specifically, the strings in this array will be compared with the value in the `ExternalIdmUser.getOriginalSrcId()` method. Note that in practice these strings often will come from a configuration file rather than being hardcoded.

```java
protected String[] getTenantManagerIdentifiers(Long tenantId) {
return null; // No tenant manager
}

protected String[] getTenantAdminIdentifiers(Long tenantId) {
  return new String[] { "jlennon" };
}
```

That’s all there is to it. As shown, no actual synchronization logic needs to be written when extending from the `AbstractExternalIdmSourceSyncService` class. The implementation should only worry about configuration and the actual fetching of the user and group information.

### Synchronization on boot

On a first boot, all users/groups must sync for the first time, otherwise nobody would be able to log in. The LDAP synchronization logic does this automatically. When creating a custom synchronization service, a custom `BootstrapConfigurer` can be used to do the same thing:

```java
package com.activiti.extension.bean;

@Component
public class MyBootstrapConfigurer implements BootstrapConfigurer {

  @Autowired
  private FileSyncService fileSyncService;

  public void applicationContextInitialized(org.springframework.context.ApplicationContext applicationContext) {
    fileSyncService.asyncExecuteFullSynchronizationIfNeeded(null);
  }
}
```

This implements the `com.activiti.api.boot.BootstrapConfigurer` interface. If there is an instance implementing this interface on the classpath, it will be called when the application is booting up (more precisely: after the Spring application context has been initialized). Here, the class we created in the previous section, `FileSyncService` is injected. Note we add it to the component scanned package again and added the `@component` identifier.

Call the `asyncExecuteFullSynchronizationIfNeeded()` method. The `null` parameter means *the default tenant* (that is, this is a non-multitenant setup). This is a method from the `com.activiti.api.idm.ExternalIdmSourceSyncService` interface, which will do a full sync if no initial synchronization was done before.

As a side note, all synchronization logs are stored in a table `IDM_SYNC_LOG` in the database.

### Synchronization log entries

When a synchronization is executed, a log is kept. This log contains all information about the synchronization: users/groups that are created, updates of existing users/groups, membership additions/deletions and so on.

To access the log entries, an HTTP REST call can be done:

```bash
GET /api/enterprise/idm-sync-log-entries
```

Which returns a result like this (only an initial synchronization happened here):

```json
[{"id":1,"type":"initial-ldap-sync","timeStamp":"2015-10-16T22:00:00.000+0000"}]
```

This call uses the following url parameters:

* `tenantId`: Defaults to the `tenantId` of the users
* `start` and `size`: Used for getting paged results back instead of one (potentially large) list.

Note that this call can only be done by a *tenant administrator*, or *tenant manager* in a multi-tenant setup.

We can now get the detailed log for each sync log entry, by taking an id from the previous response:

```bash
GET /api/enterprise/idm-sync-log-entries/{id}/logfile
```

This returns a `.log` file that contains for our example implementation:

```text
created-user: created user John Lennon (email=john.lennon@thebeatles.com) (dn=jlennon)
added-capability: added capability tenant-mgmt to user jlennon
created-user: created user Ringo Starr (email=ringo.starr@thebeatles.com) (dn=rstarr)
created-user: created user George Harrison (email=george.harrison@beatles.com) (dn=gharrison)
created-user: created user Paul McCartney (email=paul.mccartney@beatles.com) (dn=pmccartney)
created-group: created group beatles
added-user-to-group: created group membership of user jlennon for group beatles
added-user-to-group: created group membership of user rstarr for group beatles
added-user-to-group: created group membership of user gharrison for group beatles
added-user-to-group: created group membership of user pmccartney for group beatles
created-group: created group singers
added-user-to-group: created group membership of user jlennon for group singers
added-user-to-group: created group membership of user pmccartney for group singers
```

### Custom authentication

When using a custom external IDM source, you may need to authenticate against that source (For example, LDAP).

See [Global security override](#global-security-override) for more information on how to use the `users.txt` file as an authentication mechanism.

## Security configuration overrides

Configure security with the `com.activiti.conf.SecurityConfiguration` class. It allows you to switch between database and LDAP/Active Directory authentication out of the box. It also configures REST endpoints under "/app" to be protected using a cookie-based approach with tokens and REST endpoints under "*/api*" to be protected by Basic Auth.

You can override these defaults, if the out-of-the-box options are not adequate for your environment. The following sections describe the different options.

All the *overrides* described in the following sections follow the same pattern of creating a Java class that implements a certain interface. This class needs to be annotated by `@Component` and must be found in a package that is component-scanned.

>**Note:** Webapp and API use the same Spring HTTP security for authentication. To distinguish the security configurations, you should specify the path that the configuration applies to. These use `/app` and `/api` by default. For example, API configuration should begin with the following:
>
>```java
>httpSecurity.antMatcher("/api/**")
>```

### Global security override

Global security override is the most important override. It allows you to replace the default authentication mechanism.

The interface to implement the global security override is called `com.activiti.api.security.AlfrescoSecurityConfigOverride`. It has one method `configureGlobal` which is called instead of the default logic. It sets up either database-backed or LDAP-backed authentication if an instance implementing this interface is found on the classpath.

Building further on the [Example implementation](#example-implementation), use the `users.txt` file, in combination with the `FileSyncService`, so that the application uses the user information in the file to execute authentication.

Spring Security (which is used as underlying framework for security) expects an implementation of the `org.springframework.security.authentication.AuthenticationProvider` to execute the actual authentication logic. What we have to do in the *configureGlobal* method is then instantiate our custom class:

```java
package com.activiti.extension.bean;

@Component
public class MySecurityOverride implements AlfrescoSecurityConfigOverride {

  public void configureGlobal(AuthenticationManagerBuilder auth, UserDetailsService userDetailsService) {
    MyAuthenticationProvider myAuthenticationProvider = new MyAuthenticationProvider();
    myAuthenticationProvider.setUserDetailsService(userDetailsService);
    auth.authenticationProvider(myAuthenticationProvider);
  }

}
```

Note how this example passed the default `UserDetailsService` to this authentication provider. This class is responsible for loading the user data (and its capabilities or *authorities* in Spring Security lingo) from the database tables. Since we synchronized the user data using the same source, we can just pass it to our custom class.

So the actual authentication is done in the `MyAuthenticationProvider` class here. In this simple example, we just have to compare the password value in the `users.txt` file for the user. To avoid having to do too much low-level Spring Security plumbing, we let the class extend from the `org.springframework.security.authentication.dao.AbstractUserDetailsAuthenticationProvider` class.

```java
public static class MyAuthenticationProvider extends AbstractUserDetailsAuthenticationProvider {

  protected Map<String, String> userToPasswordMapping = new HashMap<String, String>();

  protected UserDetailsService userDetailsService;

  public MyAuthenticationProvider() {

    // Read users.txt, and create a {userId, password} map
    try {
      InputStream inputStream = this.getClass().getClassLoader().getResourceAsStream("users.txt");
      BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
      String line = bufferedReader.readLine();
      while (line != null) {
        String[] parsedLine = line.split(";");
        userToPasswordMapping.put(parsedLine[0], parsedLine[4]);
        line = bufferedReader.readLine();
      }

      inputStream.close();
      } catch (Exception e) {
        e.printStackTrace();
      }
    }


  protected void additionalAuthenticationChecks(UserDetails userDetails, UsernamePasswordAuthenticationToken authentication) throws AuthenticationException {

    // We simply compare the password in the token to the one in the users.txt file

    String presentedPassword = authentication.getCredentials().toString();
    String actualPassword = userToPasswordMapping.get(userDetails.getUsername());

    if (!StringUtils.equals(presentedPassword, actualPassword)) {
      throw new BadCredentialsException("Bad credentials");
    }
  }

  protected UserDetails retrieveUser(String username, UsernamePasswordAuthenticationToken authentication) throws AuthenticationException {

    // Here we simply defer the loading to the UserDetailsService that was passed to this instance

    UserDetails loadedUser = null;
    try {
      loadedUser = userDetailsService.loadUserByUsername(username);
    } catch (Exception e) {
      throw new AuthenticationServiceException(e.getMessage(), e);
    }
    return loadedUser;
  }

}
```

There’s one last bit to configure. By default, the application is configured to log in using the email address. Set the following property to switch that to the `externalId`, meaning the id coming from the external IDM source (`jlennon` in the `users.txt` file for example):

```text
security.authentication.use-externalid=true
```

Use the following property to configure case-sensitivity for logins:

```text
security.authentication.casesensitive=true
```

Alternatively, you can override the `AuthenticationProvider` that is used (instead of overriding the `configureGlobal`) by implementing the `com.activiti.api.security.AlfrescoAuthenticationProviderOverride` interface.

#### REST Endpoints security overrides

You can change the default security configuration of the REST API endpoints by implementing the `com.activiti.api.security.AlfrescoApiSecurityOverride` interface. By default, the REST API endpoints use the Basic Authentication method.

Similarly, you can override the default cookie+token based security configuration with the regular REST endpoints (those used by the UI) by implementing the `com.activiti.api.security.AlfrescoWebAppSecurityOverride` interface.

>**Note:** Webapp and API use the same Spring HTTP security for authentication. To distinguish the security configurations, you should specify the path that the configuration applies to. These use `/app` and `/api` by default. For example, API configuration should begin with the following:

```java
httpSecurity.antMatcher("/api/**")
```

#### UserDetailsService override

If the default `com.activiti.security.UserDetailsService` does not meet the requirement (although it should cover most use cases), you can override the implementation with the `com.activiti.api.security.AlfrescoUserDetailsServiceOverride` interface.

### PasswordEncoder override

By default, Process Services uses the `org.springframework.security.crypto.password.StandardPasswordEncoder` for encoding passwords in the database. Note that this is only relevant when using database-backed authentication (so does not hold LDAP/Active Directory). This is an encoder that uses SHA-256 with 1024 iterations and a random salt.

You can override the default setting by implementing the `com.activiti.api.security.AlfrescoPasswordEncoderOverride` interface.
---
title: Process Services ReST API
---

Process Services comes with a ReST API. The ReST API exposes the generic Process Engine operations. It also includes a dedicated set of ReST API endpoints for features specific to Process Services.

**Important:** An internal ReST API also exists that is used as ReST endpoints by the JavaScript user interface. Do NOT use this API as the ReST API URLs might modify the product to use unsupported features. In addition, the internal ReST API uses a different authentication mechanism tailored towards web browser use.

## Enabling CORS

Solutions that use Process Services REST APIs may be in a different domain or port. This is known as Cross Origin Resource Sharing (CORS).

By default, CORS is not allowed to provide a high level of security. This can be alleviated by using web proxies which consolidate different domains and ports or by enabling CORS in Process Services configuration. For more information, see [Configuring CORS]({% link process-services/latest/config/index.md %}#cors).

## ReST API Authorization

The REST API uses authorization rules to determine a user’s access control for a process instance or task.

You can use any of the following methods for REST API user authentication:

* Basic authentication
* [OAuth 2 SSO](#oauth-2-sso-overview)
* Impersonation

If you are using basic authentication, you must set all requests with the `Authorization` header.

If you are using OAuth 2 to authenticate users for SSO, see [OAuth 2 SSO](#oauth-2-sso-overview) for more information.

If you choose to use Impersonation, you can impersonate a user with an Admin account to authenticate and set a different user for authorization. To enable this, add the `activiti-user` and `activiti-user-value-type` request headers to the REST API. Where, `activiti-user` should be set to the required user account identifier and `activiti-user-value-type` to the user account identifier type. The header `activiti-user-value-type` can be one of the following values:

* `userIdType`: User’s database ID
* `userEmailType`: User’s Email address
* `userExternalIdType`: User’s ID in an external authentication service such as LDAP or Active Directory

For example, in the `external-form-example` Web application, an Admin account is used for authentication and a different user account to implement authorization.

>**Note:** You must have an Admin role to be able to add the above request headers. In addition, the users should have already been added to Process Services manually, or by synchronization with LDAP or Active Directory.

### OAuth 2 SSO overview

The OAuth 2.0 authorization framework enables an application to access protected resources on behalf of a user without storing a password.

OAuth 2.0 defines four roles:

* **Resource owner**: Specifies the user who authorizes an application to access their account or protected resources (REST APIs).
* **Resource server**: Specifies the server hosting the protected resources (REST APIs). In this case, it is Process Services.
* **Client**: Specifies your build application that makes protected resource (REST APIs) requests on behalf of the resource owner. Before it may do so, it must be authorized by the resource owner.
* **Authorization server**: Specifies the server issuing access tokens to the client after successfully authenticating against Ping Identity, Azure Identity Services, or Site Minder.

OAuth 2 SSO support in Process Services introduces a new set of components that allow developers to leverage the Alfresco REST APIs using OAuth 2 authorization.

![oauth-overview]({% link process-services/images/oauth-overview.png %}){:height="356px" width="700px"}

The addition of OAuth 2 in Process Services is the first step towards a single standards-authorization and identity services across the Alfresco Digital Business Platform. Using OAuth you can have:

* a standard-based authorization infrastructure to integrate applications and solutions using Process Services REST APIs with other enterprise applications which use OAuth.

* configurable integration with OAuth authorization servers that can issue OAuth 2 tokens, such as Ping Identity, Azure Identity Services, or Site Minder, with support for custom and JWT tokens.
* a unified OAuth 2 stack to facilitate OAuth 2 SSO for ADF and other applications across both Process Services and Alfresco Content Services.

#### OAuth 2 SSO features

Use this information to understand the features of OAuth 2 SSO for Process Services.

OAuth 2 introduces the following new features:

* A **built-in OAuth 2 client** delivered as a part of the Process Services. The client can request and handle OAuth 2 tokens from the OAuth 2.0 Authorization Servers.
* The **Alfresco OAuth 2 Authorization Server** - a fully functioning lightweight micro service that simplifies development, testing, and deployment of REST based applications using OAuth 2 for authorization.
* A special **OAuth 2 gateway** to Alfresco Content Services that allows use of OAuth 2 authorization to Alfresco Content Services.

>**Note:** OAuth 2 SSO does not eliminate the issues of different identity systems and requires user synchronization with the Process Services user database.

#### Installing OAuth 2 SSO for Process Services

Use this information to install OAuth 2 SSO for Process Services.

Installing OAuth 2 module:

The OAuth 2 module is an integrated library of the Process Services. It Is automatically installed as part of the `activiti-app` web application.

Installing Alfresco OAuth 2 Authorization server

The Alfresco OAuth 2 Authorization server is available as a java web archive (WAR) available to Process Services via [Alfresco's maven repository](https://artifacts.alfresco.com/nexus/content/repositories/activiti-enterprise-releases/org/alfresco/alfresco-oauth2/1.0.0/alfresco-oauth2-1.0.0.war){:target="_blank"}.

#### Configuring OAuth 2 for the Process Services

To configure OAuth 2, you need to register your application with an OAuth 2 Authorization server and then configure the OAuth 2 client using the `activiti-app.properties` file.

**Registering with an OAuth 2 Authorization server**

When using an OAuth 2 server, you need to register your application with the authorization server.

This will vary from server to server but the server will invariably provide:

* a client Id to identify your application. This is often a part of the URLs provided by the server.
* the client secret that must be kept secret.
* an authorization URL to use in your application.

All these components are used in configuring the OAuth 2 client. For more information, see *Configuring the OAuth 2 client* below.

You may use an OAuth 2 Authorization server of your choice but for applications involving Alfresco Content Services, it is recommended that you use the Alfresco OAuth 2 Authorization server. To know more about installing and configuring the Alfresco OAuth 2 Authorization server, see [Configuring the Alfresco OAuth 2 Authorization server](#configoauthserver).

Note that OAuth 2 is an authorization system and not an identity management system. Although it eliminates the need for custom applications to login via the REST API, it still requires all users to have a profile in Process Services with a user name that matches the user name of the OAuth 2 Authorization server. However, there is no need for the passwords to match. Passwords are only useful if you want to allow users to log in to the standard Alfresco Content Services application.

You can use LDAP sync or the Alfresco Content Services Security Extensions to have a single identity service for both the Alfresco Content Services profiles and the OAuth 2 Authorization server.

**Configuring the OAuth 2 client**

To use the OAuth 2 client from your REST applications, you first need to configure it using the information obtained by the OAuth 2 authorization server.

To configure the OAuth 2 client, add the following properties to the `activiti-app.properties` file:

```text
security.oauth2.authentication.enabled=true
security.oauth2.client.clientId=alfresco
security.oauth2.client.clientSecret=secret
security.oauth2.client.checkToken=http://localhost:9191/oauth/check_token
```

|Property|Description|
|--------|-----------|
|security.oauth2.authentication.enabled|Enables or disables the OAuth 2 client. To enable the OAuth 2 client, set this property to `true`. To disable it, set this property to `false`.|
|security.oauth2.client.clientId|Specifies the credentials used by the Process Services OAuth 2 client to communicate with the OAuth 2 Authorization server.|
|security.oauth2.client.clientSecret|Specifies the credentials used by the Process Services OAuth 2 client to communicate with the OAuth 2 Authorization server.|
|security.oauth2.client.checkToken|Configures the OAuth 2 Authorization to be used. It contains the authorization URL obtained from the Authorization server.|
|security.oauth2.basicAuth.enabled|Enables or disables basic authentication when OAuth 2 is configured. The default value is `false`.|

**Using the OAuth 2 module**

After successfully configuring the Process Services OAuth 2 module, you can develop, test, and deploy the applications using the Process Services REST APIs and OAuth 2.

As a developer, you can integrate the OAuth 2 flow, which starts with getting the authorization token. For browser, mobile, and other UI-based applications, this will usually be done using a login UI interface provided by the service to the user. For communication purpose, the server-side applications will use the client secret.

OAuth 2 caters for four authorization scenarios called *grant types*. These are:

* **Authorization Code** for applications running on a web server, browser, or mobile app.
* **Password** for logging in with a user name and password.
* **Client credentials** for application access by confidential clients.
* **Implicit** that has been superseded by the Authorization Code scenario with a no secret code.

As a developer, you can choose the scenario that best suits your use case and the specific problem you are trying to solve. This will be a direct call between your code and the authorization server.

After obtaining the token, you integrate it and use it as a part of calling the Process Services REST APIs. This is done by adding the token as an Authorization header.

```text
Authorization: Bearer <token>
```

For example, to call the rest API for the `app-version`, either use:

```bash
GET /activiti-app/api/enterprise/app-version HTTP/1.1
Host: activiti.example.com
Authorization: Bearerd1c7dc0b-b1e1-4039-923e-55199473bd5b
```

or use:

```bash
$  curl -i -H "Authorization: Bearer d1c7dc0b-b1e1-4039-923e-55199473bd5b"
        http://localhost:8080/activiti-app/api/enterprise/app-version
```

When a REST request is made using the OAuth 2 header, Process Services acts as the Resource Server of the OAuth 2 specification. Using the OAuth 2 module Process Services attempts to validate the token against the OAuth 2 Authorization server. This is done using the URL specified in the `security.oauth2.client.checkToken` property of the `activiti-app.properties` file.

Here's an example of the HTTP call made by Process Services OAuth 2 module to validate the token:

```bash
POST /introspect HTTP/1.1
Host: ${security.oauth2.client.checkToken}
Accept: application/json
Content-Type: application/x-www-form-urlencoded
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW <- base 64 encoding ${security.oauth2.client.clientId}:${security.oauth2.client.clientSecret}

token=CHECK_ACCESS_TOKEN
```

The Authorization server responds with a JSON object as specified in the [Introspection Response of the OAuth 2 specification](https://tools.ietf.org/html/rfc7662#section-2.2){:target="_blank"}. One of the properties of the object is the user name, which matches the user name found in the user database of Process Services. This allows the process service to identify which registered user is the one associated to the REST request.

Spring security is used to call the OAuth 2 server and validate the token. Token validation is an area that has been standardised recently. For more information, see [OAuth 2.0 Token Introspection](https://tools.ietf.org/html/rfc7662){:target="_blank"}. Commercial OAuth 2 servers or services may not be yet compliant with the standard. For more information, see [http://stackoverflow.com/questions/12296017](http://stackoverflow.com/questions/12296017/how-to-validate-an-oauth-2-0-access-token-for-a-resource-server){:target="_blank"}.

For non-standard validation approaches, you may use `apiSecurityOverride` of the security extensibility provided by Process Services and override the `com.activiti.security.oauth2.Oauth2RequestHeaderService` class using `@Component(value = "ActivitiOauth2RequestHeaderService")`.

#### Configuring the Alfresco OAuth 2 Authorization server {#configoauthserver}

You can configure the Alfresco OAuth 2.0 Authorization server using the `application.properties` file.

You can provide the `application.properties` file in the following locations:

* A `/config` subdirectory of the current directory
* The current directory
* A classpath `/config` package
* The classpath root

The server loads the properties from the `application.properties` file in order of precedence. The properties defined in locations higher in the list override those defined in lower locations.

The properties file contains the following properties

|Property|Description|Default Value|
|--------|-----------|-------------|
|Server.port|Specifies the port on which the Authorization server runs.|`9191`|
|zuul.routes.ecm.url|Specifies the end-point URL for Alfresco Cloud Services installation to use.|`http://localhost:8080`|
|zuul.routes.bpm.url|Specifies the end-point URL for Process Services installation to use.|`http://localhost:9999`|
|zuul.routes.ecm.path|Specifies the default path for ECM requests. For example, `http://localhost:9191/ecm/alfresco/api/-default-/public/alfresco/versions/1/people`.|`/ecm`|
|zuul.routes.bpm.path|Specifies the default path for the BPM requests. For example, `http://localhost:9191/bpm/activiti-app/api/enterprise/app-version`.|`/bpm`|
|authentication.oauth.jwt|Enables or disables the use of JWT tokens. Set it to `true` to instruct the server to use JWT tokens. Set it to `false` to configure the server to use the proprietary Alfresco token.|`false`|
|authentication.oauth.corsFilter|Enable (`true`) or disable (`false`) CORS requests.|`false`|
|authentication.oauth.ecm|Enables (`true`) or disable (`false`) authentication against Alfresco Content Services.|`true`|
|authentication.oauth.bpm|Enables (`true`) or disable (`false`) authentication against Process Services.|`true`|
|authentication.oauth.tokenValidityInSeconds|Specifies the token lifetime or the lifetime in seconds of the access token.|`604800`|

#### Running the Alfresco OAuth 2 Authorization server

You can run the Alfresco OAuth 2 Authorization server as a Java executable from the command line.

```bash
java -jar alfresco-oauth2-<version>.war
```

The server provides a health check point to use:

```bash
$ curl -i -H "Authorization: Bearer <access_token>" http://localhost:9191/management/health
```

Here's the sample response:

```json
{"status":"UP"}
```

#### Using the Alfresco OAuth 2 Authorization server

The Alfresco OAuth 2 Authorization server can be used as part of the OAuth 2 flows. The server needs to be used in conjunction with the LDAP sync for users from the Alfresco Content Services LDAP directory.

Use this information to know how the different scenarios are supported.

**Authorization code grant type** 

```html
http://tools.ietf.org/html/rfc6749#section-4.1
```

The authorization code grant type is used to obtain both access tokens and refresh tokens. It is optimized for confidential clients, such as server side application. Since this is a redirection-based flow, the client must be capable of interacting with the resource owner's `user-agent` (typically, a web browser) and capable of receiving incoming requests (via redirection) from the Authorization server.

*Authorization Request:*

Here's an example of the authorization request:

```bash
curl  -XPOST -vu alfrescoapp:secret 'http://localhost:9191/authorize?response_type=code&client_id=alfrescoapp&state=xyz&
redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb
```

where:

|Parameter|Description|
|---------|-----------|
|response_type|*Required*. This value must be set to `**code**`.|
|client_id|*Required*. Specifies the client identifier.|
|redirect_uri|*Required*. Specifies the redirection endpoint after authentication.|
|state|*Optional*. Specifies an opaque value used by the client to maintain state between the request and callback sent for preventing cross-site request forgery.|

Your OAuth 2 module initiates the flow by directing the resource owner's user-agent to the authorization endpoint.

![auth-endpoint]({% link process-services/images/auth-endpoint.png %}){:height="286px" width="560px"}

The Authorization server authenticates the resource owner.

![resource-owner]({% link process-services/images/resource-owner.png %}){:height="382px" width="560px"}

The Authorization server establishes whether the resource owner grants or denies the client's access request.

![client-access-request]({% link process-services/images/client-access-request.png %}){:height="353px" width="560px"}

Assuming the resource owner grants access, the authorization server redirects the user-agent back to the client using 
the redirection URI provided earlier.

*Response:*

Here's an example of the authorization response:

```html
HTTP/1.1 302 Found Location:
http://example.com/cb?code=SplxlOBeZQQYbYS6WxSbIA&state=xyz
```

where:

|Parameter|Description|
|---------|-----------|
|code|*Required*. Specifies the authorization code generated by the authorization server. The authorization code MUST expire shortly after it is issued to mitigate the risk of leaks. A maximum authorization code lifetime of 10 minute is RECOMMENDED. The client MUST NOT use the authorization code more than once.|
|state|*Required*. Specifies if this parameter was present in the client authorization request. It specifies the exact value received from the client.|

*Access Token Request:*

The client makes a request to the token endpoint in order to get the `access_token`:

```bash
curl  -XPOST -vu alfrescoapp:secret
http://localhost:9191/grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA&redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb
```

where:

|Parameter|Description|
|---------|-----------|
|grant_type|*Required*. This value must be set to `**authorization_code**`.|
|code|*Required*. Specifies the authorization code received from the Authorization server.|
|redirect_uri|*Required*. Specifies the redirection endpoint after authentication.|
|client_id|*Required*. Specifies if the client is not authenticating with the Authorization server.|

*Response:*

Here's an example of response:

```json
{
   "access_token":"2YotnFZFEjr1zCsicMWpAA",
   "token_type":"example",
   "expires_in":3600, 
   "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA"
   "example_parameter":"example_value"
}
```

**Implicit grant type**

The implicit grant type ([http://tools.ietf.org/html/rfc6749#section-4.2](http://tools.ietf.org/html/rfc6749#section-4.2){:target="_blank"} ) is used to obtain access tokens (it does not support the issuance of refresh tokens) and is optimized for public clients known to operate a particular redirection URI. These clients are typically implemented in a browser using a scripting language such as JavaScript clients or mobile applications. This flow is recommended when storing client id and client secret is not recommended

*Authorization request:*

Here's an example of the authorization request:

```bash
curl  -XPOST -vu alfrescoapp:secret 'http://localhost:9191//authorize?response_type=token&
client_id=alfrescoapp&state=xyz&redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb'
```

where:

|Parameter|Description|
|---------|-----------|
|response_type|*Required*. This value MUST be set to `token`.|
|client_id|*Required*. Specifies the client identifier.|
|redirect_uri|*Optional*. Specifies the redirection endpoint after authentication.|
|scope|*Optional*. Specifies if the client is not authenticating with the Authorization server.|
|state|*Required*. Specifies an opaque value used by the client to maintain state between the request and callback sent for preventing cross-site request forgery.|

*Response:*

If the resource owner grants access request, the Authorization server issues an access token and delivers it to the client. The following response is sent:

```html
HTTP/1.1 302 Found Location:
http://example.com/cb#access_token=91202244-431f-444a-b053-7f50716f2012&state=xyz&token_type=bearer&expires_in=3600
```

where:

|Parameter|Description|
|---------|-----------|
|access_token|*Required*. Specifies the access token issued by the Authorization server.|
|token_type|*Required*. Specifies the type of token.|
|expires_in|*Recommended*. Specifies the lifetime in seconds of the access token.|
|scope|*Optional*. Specifies if the client is not authenticating with the Authorization server.|
|state|*Recommended*. Specifies an opaque value used by the client to maintain state between the request and callback sent for preventing cross-site request forgery.|

**Resource owner password credentials grant type**

The [resource owner password credentials grant type](http://tools.ietf.org/html/rfc6749#section-4.3){:target="_blank"} is suitable in cases where the resource owner has a trust relationship with the client, such as the device operating system or a highly privileged application.

*Access Token Request:*

Here's an example of the access token request:

```
curl  -XPOST -vu alfrescoapp:secret 
'http://localhost:9191/oauth/token?username=admin&password=tiger&grant_type=password'
```

where:

|Parameter|Description|
|---------|-----------|
|grant_type|*Required*. This value MUST be set to `password`.|
|username|*Required*. Specifies the resource owner username.|
|password|*Required*. Specifies the resource owner password.|
|scope|*Optional*. Specifies if the client is not authenticating with the Authorization server.|

*Response:*

Here's an example response:

```json
{
   "access_token":"821c99d4-2c9f-4990-b68d-18eacaff54b2",
   "token_type":"bearer"
   "refresh_token":"e6f8624f-213d-4343-a971-980e83f734be",
   "expires_in":1799,
   "scope":"read write"
}
```

**Fetching `access_token` by submitting `refresh_token`**

*Request:*

Here's an example request:

```bash
curl  -XPOST -vu alfrescoapp:secret
'http://localhost:9191/oauth/token?grant_type=refresh_token&refresh_token=<refresh_token>'
```

where:

|Parameter|Description|
|---------|-----------|
|grant_type|*Required*. This value Value MUST be set to `refresh_token`.|
|refresh_token|*Required*. Specifies the refresh token issued to the client.|

*Response:*

Here's an example response:

```json
{
      "access_token":"821c99d4-2c9f-4990-b68d-18eacaff54b2",
      "token_type":"bearer"
      "refresh_token":"e6f8624f-213d-4343-a971-980e83f734be",
      "expires_in":1799,
      "scope":"read write"
}
```

**Access secure resource**

*Request:*

```bash
curl -i -H "Authorization: Bearer <access_token>"
http://localhost:9191/secure
```

*Response:*

```text
Secure Hello!
```


**Client credentials**

The [client credentials grant type](http://tools.ietf.org/html/rfc6749#section-4.4){:target="_blank"} is not currently implemented.

**External Token**

As defined in the [OAuth 2 specification](https://tools.ietf.org/html/rfc6749#section-4.5){:target="_blank"}, it is possible to define custom grant. You can override the generation of the token using the `grant_type`, `external_auth`. Additionally, you can submit the token and the refresh token. This grant type can be used in the scenario where the OAuth server is already present and you want to use the proxy part of this server.

Set the following properties:

```text
authentication.oauth.client.accessTokenUri= http://AUTH_SERVER/oauth/token
authentication.oauth.client.userAuthorizationUri=http://AUTH_SERVER/oauth/authorize
authentication.oauth.client.clientId=  YOUR_CLIENT
authentication.oauth.client.clientSecret= YOUR_SECRET
```

*Access Token Request:*

Here's an example access token request:

```bash
curl -XPOST -vu alfrescoapp:secret 
'http://localhost:9191/oauth/token?username=admin&password=admin&access_token=YOUR_CUSTOM_TOKEN&
refresh_token=YOUR_CUSTOM_REFRESH_TOKEN&grant_type=external_token'
```

where:

|Parameter|Description|
|---------|-----------|
|`grant_type`|*Required*. This value MUST be set to `external_token`.|
|`username`|*Required*. Specifies the resource owner username.|
|`password`|*Required*. Specifies the resource owner password.|
|`scope`|*Optional*. Specifies if the client is not authenticating with the Authorization server.|

*Response:*

```json
{    
     "access_token":"821c99d4-2c9f-4990-b68d-18eacaff54b2",
     "token_type":"bearer"
     "refresh_token":"e6f8624f-213d-4343-a971-980e83f734be",
     "expires_in":1799,
     "scope":"read write"
}
```

## Using the ReST API Explorer

Process Services comes with a built-in REST API Explorer. This lets you discover and test the REST APIs of a locally running Process Services instance.

The REST API Explorer is based on the [OpenAPI (Swagger) initiative](https://openapis.org/){:target="_blank"} and provides an interface for the REST API. You can browse the available API endpoints and test operations available within a particular API group.

Access the REST API Explorer at this link: `http://localhost:8080/activiti-app/api-explorer.html`.

There is also a public [REST API Explorer](https://activiti.alfresco.com/activiti-app/api-explorer.html){:target="_blank"}.

This screenshot shows what the REST API Explorer looks like:

![api-explorer-home-page]({% link process-services/images/api-explorer-home-page.png %}){:height="388px" width="574px"}

Click on a link to view the available operations for a particular group of APIs.

For example, to explore the operations on a specific entity, **Admin Tenants: Manage Tenants API**, just click on it:

![manage-tenants-api-operations]({% link process-services/images/manage-tenants-api-operations.png %}){:height="272px" width="743px"}

Click on an operation to test it against the locally running Process Services instance.

![test-manage-tenants]({% link process-services/images/test-manage-tenants.png %})

When you click **Try it out!**, you'll see the following response:

![rest-api-result]({% link process-services/images/rest-api-result.png %}){:height="740px" width="900px"}

## RAML support

Process Services provides a RAML file that works with popular REST API development tools.

The RAML file complements the REST API Explorer, providing a best-in-class enterprise tooling for APIs.

RESTful API Modeling Language (RAML) is a language to describe RESTful APIs. The language is YAML-based with a json
format available, and it provides the constructs to describe RESTful or practically-RESTful APIs. Practically-RESTful APIs are those that do not comply with the all constraints of REST.

The language aims to promote reuse, discovery and pattern-sharing, as well as merit-based emergence of patterns. Tooling for RAML varies from modeling to software life cycle management and API description conversion. For more information about RAML, see [https://raml.org](https://raml.org){:target="_blank"}.

Process Services provides a description of all enterprise REST APIs using RAML and in json format. The description follows RAML 0.8 but can easily be converted to the recent RAML 1.0 standard by using tools like Apimatic.

You can access the RAML description of all Enterprise REST APIs in Process Services using the following URL:

```html
http(s)://<Process Services host>:port/activiti-app/raml/activiti.raml
```

This URL returns the entire RAML description of the enterprise APIs.

**Using the RAML file for Process Services**

The Process Services RAML file can be used with tools supporting RAML to integrate it in API life cycle of enterprise systems.

Mulesoft provides a free RAML IDE called API Workbench. This is a plugin for the free editor, Atom, that can be used to view the Process Services RAML file. For information on how to download and setup the Atom plugin, see [http://apiworkbench.com/docs](http://apiworkbench.com/docs){:target="_blank"}.

In addition, Mulesoft provides a web-based RAML API designer that can be used to combine Process Services REST APIs in RAML-based API and system design. See [https://www.mulesoft.com/platform/api/anypoint-designer](https://www.mulesoft.com/platform/api/anypoint-designer){:target="_blank"}.

For a full list of tools that can use RAML throughout the entire application development life cycle see [http://raml.org/projects/projects](http://raml.org/projects/projects){:target="_blank"}.

## Process Services ReST API

The REST API exposes data and operations that are specific to Process Services.

In contrast to the Process Engine REST API, the Process Services REST API can be called using any user. The following sections describe the supported REST API endpoints.

### Server Information

To retrieve information about the Process Services version, use the following command:

```bash
GET api/enterprise/app-version
```

**Response:**

```json
{
   "edition": "Alfresco Activiti Enterprise BPM Suite",
   "majorVersion": "1",
   "revisionVersion": "0",
   "minorVersion": "2",
   "type": "bpmSuite",
}
```

### Profile

This operation returns account information for the current user. This is useful to get the name, email, the groups that the user is part of, the user picture, and so on.

```bash
GET api/enterprise/profile
```

**Response:**

```json
{
     "tenantId": 1,
     "firstName": "John",
     "password": null,
     "type": "enterprise",
     "company": null,
     "externalId": null,
     "capabilities": null,
     "tenantPictureId": null,
     "created": "2015-01-08T13:22:36.198+0000",
     "pictureId": null,
     "latestSyncTimeStamp": null,
     "tenantName": "test",
     "lastName": "Doe",
     "id": 1000,
     "lastUpdate": "2015-01-08T13:34:22.273+0000",
     "email": "johndoe@alfresco.com",
     "status": "active",
     "fullname": "John Doe",
     "groups": [
          {
               "capabilities": null,
               "name": "analytics-users",
               "tenantId": 1,
               "users": null,
               "id": 1,
               "groups": null,
               "externalId": null,
               "status": "active",
               "lastSyncTimeStamp": null,
               "type": 0,
               "parentGroupId": null
          },
          {
               "capabilities": null,
               "name": "Engineering",
               "tenantId": 1,
               "users": null,
               "id": 2000,
               "groups": null,
               "externalId": null,
               "status": "active",
               "lastSyncTimeStamp": null,
               "type": 1,
               "parentGroupId": null
          },
          {
               "capabilities": null,
               "name": "Marketing",
               "tenantId": 1,
               "users": null,
               "id": 2001,
               "groups": null,
               "externalId": null,
               "status": "active",
               "lastSyncTimeStamp": null,
               "type": 1,
               "parentGroupId": null
          }
     ]
}
```

To update user information (first name, last name or email):

```bash
POST api/enterprise/profile
```

The body of the request should resemble the following text:

```json
{
    "firstName" : "John",
    "lastName" : "Doe",
    "email" : "john@alfresco.com",
    "company" : "Alfresco"
}
```

To get the user picture, use following REST call:

```bash
GET api/enterprise/profile-picture
```

To change this picture, do an HTTP POST to the same URL, with the picture as multipart file in the body.

Finally, to change the password:

```bash
POST api/enterprise/profile-password
```

with a json body that looks like

```json
{
    "oldPassword" : "12345",
    "newPassword" : "6789"
}
```

### Runtime Apps

When a user logs into Process Services, the landing page is displayed containing all the apps that the user is allowed to see and use.

The corresponding REST API request to get this information is:

```bash
GET api/enterprise/runtime-app-definitions
```

**Response:**

```json
{
     "size": 3,
     "total": 3,
     "data": [
          {
               "deploymentId": "26",
               "name": "HR processes",
               "icon": "glyphicon-cloud",
               "description": null,
               "theme": "theme-6",
               "modelId": 4,
               "id": 1
          },
          {
               "deploymentId": "2501",
               "name": "Sales onboarding",
               "icon": "glyphicon-asterisk",
               "description": "",
               "theme": "theme-1",
               "modelId": 1002,
               "id": 1000
          },
          {
               "deploymentId": "5001",
               "name": "Engineering app",
               "icon": "glyphicon-asterisk",
               "description": "",
               "theme": "theme-1",
               "modelId": 2001,
               "id": 2000
          }
     ],
     "start": 0
}
```

The `id` and `modelId` property of the apps are important here, as they are used in various operations described below.

### App Definitions List

When a user logs into Process Services, the landing page is displayed containing all the apps that the user is allowed to see and use.

The corresponding REST API request to get this information is:

```bash
GET api/enterprise/runtime-app-definitions
```

**Response:**

```json
{
     "size": 3,
     "total": 3,
     "data": [
          {
               "deploymentId": "26",
               "name": "HR processes",
               "icon": "glyphicon-cloud",
               "description": null,
               "theme": "theme-6",
               "modelId": 4,
               "id": 1
          },
          {
               "deploymentId": "2501",
               "name": "Sales onboarding",
               "icon": "glyphicon-asterisk",
               "description": "",
               "theme": "theme-1",
               "modelId": 1002,
               "id": 1000
          },
          {
               "deploymentId": "5001",
               "name": "Engineering app",
               "icon": "glyphicon-asterisk",
               "description": "",
               "theme": "theme-1",
               "modelId": 2001,
               "id": 2000
          }
     ],
     "start": 0
}
```

The `id` and `modelId` property of the apps are important here, as they are used in various operations described below.

### App Import And Export

It is possible to export app definitions and import them again. From the REST API point of view, this is useful to bootstrap an environment (for users or continuous integration).

To export an app definition, you need the `modelId` from a runtime app or the `id` of an app definition model, and call:

```bash
GET api/enterprise/app-definitions/{modelId}/export
```

This will return a zip file containing the app definition model and all related models (process definitions and forms).

To import an app again, post the zip file as multipart file to:

```bash
POST api/enterprise/app-definitions/import
```

To import an app to an existing app definition to create a new version instead of importing a new app definition, post the zip file as multipart file to:

```bash
POST api/enterprise/app-definitions/{modelId}/import
```

### App Publish and Deploy

Before an app model can be used, it needs to be published. This can be done through following call:

```bash
POST api/enterprise/app-definitions/{modelId}/publish
```

A JSON body is required for the call. You can either use an empty one or the following example:

```json
{
    "comment": "",
    "force": false
}
```

To add it to your landing page, `deploy` the published app:

```bash
POST api/enterprise/runtime-app-definitions
```

Where, `appDefinitions` is an array of IDs, for example:

```json
{
    "appDefinitions" : [{"id" : 1}, {"id" : 2}]
}
```

### Process Definition Models List

To retrieve a list of process definition models:

```bash
GET api/enterprise/models?filter=myprocesses&modelType=0&sort=modifiedDesc
```

The request parameters

* `filter` : Possible values: `myprocesses`, `sharedWithMe`, `sharedWithOthers`, `favorite`.
* `modelType` : Must be `0` for process definition models.
* `sort` : Possible values: `modifiedDesc`, `modifiedAsc`, `nameAsc`, `nameDesc` (default `modifiedDesc`).

### Model Details and History

Both app definition and process definition models are versioned.

To retrieve details about a particular model (process, form, decision rule or app):

```bash
GET api/enterprise/models/{modelId}
```

**Example response:**

```json
{
     "createdBy": 1,
     "lastUpdatedBy": 1,
     "lastUpdatedByFullName": " Administrator",
     "name": "aad",
     "id": 2002,
     "referenceId": null,
     "favorite": false,
     "modelType": 0,
     "comment": "",
     "version": 3,
     "lastUpdated": "2015-01-10T16:24:27.893+0000",
     "stencilSet": 0,
     "description": "",
     "createdByFullName": " Administrator",
     "permission": "write",
     "latestVersion": true
}
```

The response shows the current version of the model.

To retrieve a thumbnail of the model:

```bash
GET api/enterprise/models/{modelId}/thumbnail
```

To get the version information for a model:

```bash
GET api/enterprise/models/{modelId}/history
```

**Example response:**

```json
{
     "size": 2,
     "total": 2,
     "data": [
          {
               "createdBy": 1,
               "lastUpdatedBy": 1,
               "lastUpdatedByFullName": " Administrator",
               "name": "aad",
               "id": 3000,
               "referenceId": null,
               "favorite": null,
               "modelType": 0,
               "comment": "",
               "version": 2,
               "lastUpdated": "2015-01-10T16:15:50.579+0000",
               "stencilSet": 0,
               "description": "",
               "createdByFullName": " Administrator",
               "permission": null,
               "latestVersion": false
          },
          {
               "createdBy": 1,
               "lastUpdatedBy": 1,
               "lastUpdatedByFullName": " Administrator",
               "name": "aad",
               "id": 2000,
               "referenceId": null,
               "favorite": null,
               "modelType": 0,
               "comment": null,
               "version": 1,
               "lastUpdated": "2015-01-10T16:07:41.831+0000",
               "stencilSet": 0,
               "description": "",
               "createdByFullName": " Administrator",
               "permission": null,
               "latestVersion": false
          }
     ],
     "start": 0
}
```

To get a particular older version:

```bash
GET api/enterprise/models/{modelId}/history/{modelHistoryId}
```

To create a new model:

```bash
POST api/enterprise/models/
```

with a json body that looks like:

```json
{
    "modelType": 0,
    "name": "My process",
    "description": "This is my favourite process!"
}
```

The modelType property defines the kind of model that is created:

* 0 is a BPMN 2.0 process model
* 1 is a step process model
* 2 is a form model
* 3 is an app model
* 4 is a decision table model

Following properties are optional:

* *stencilSet* : the identifier of the stencilset in case a non-default stencilset needs to be used.

To update the details of a model:

```bash
PUT api/enterprise/models/{modelId}
```

with a json body that looks like:

```json
{
    "name": "New name",
    "description": "New description"
}
```

To favorite a model:

```bash
PUT api/enterprise/models/{modelId}
```

with as json body:

```json
{
    "favorite": true
}
```

To delete a model:

```bash
DELETE api/enterprise/models/{modelId}
```

To duplicate a model:

```bash
POST api/enterprise/models/{modelId}/clone
```

with as json body:

```json
{
    "name": "Cloned model"
}
```

To convert a step process to a BPMN 2.0 process, add `"modelType" : 0` to the body.

### BPMN 2.0 Import and Export

To export a process definition model to a BPMN 2.0 XML file:

```bash
GET api/enterprise/models/{processModelId}/bpmn20
```

For a previous version of the model:

```bash
GET api/enterprise/models/{processModelId}/history/{processModelHistoryId}/bpmn20
```

To import a BPMN 2.0 xml file:

```bash
POST api/enterprise/process-models/import
```

With the BPMN 2.0 XML file in the body as a multipart file and the file as value for the `file` property.

### Process Definitions

Get a list of process definitions (visible within the tenant of the user):

```bash
GET api/enterprise/process-definitions
```

**Example response:**

```json
{
     "size": 5,
     "total": 5,
     "data": [
          {
            "id": "demoprocess:1:7504",
            "name": "Demo process",
            "description": null,
            "key": "demoprocess",
            "category": "http://www.activiti.org/test",
            "version": 1,
            "deploymentId": "7501",
            "tenantId": "tenant_1",
            "hasStartForm": true
          },
          ...
     ],
     "start": 0
}
```

Following parameters are available:

* `latest`: A boolean value, indicating that only the latest versions of process definitions must be returned.
* `appDefinitionId`: Returns process definitions that belong to a certain app.

To get the candidate starters associated to a process definition:

```bash
GET api/enterprise/process-definitions/{processDefinitionId}/identitylinks/{family}/{identityId}
```

Where:

* `processDefinitionId`: The ID of the process definition to get the identity links for.
* `family`: Indicates groups or users, depending on the type of identity link.
* `identityId`: The ID of the identity.

To add a candidate starter to a process definition:

```bash
POST api/enterprise/process-definitions/{processDefinitionId}/identitylinks
```

**Request body (user)**:

```json
{
    "user" : "1"
}
```

**Request body (group)**:

```json
{
    "group" : "1001"
}
```

To delete a candidate starter from a process definition:

```bash
DELETE api/enterprise/process-definitions/{processDefinitionId}/identitylinks/{family}/{identityId}
```

### Start Form

When process definition has a start form (`hasStartForm` is `true` as in the call above), the start form can be 
retrieved as follows:

```bash
GET api/enterprise/process-definitions/{process-definition-id}/start-form
```

**Example response:**

```json
{
  "processDefinitionId": "p1:2:2504",
  "processDefinitionName": "p1",
  "processDefinitionKey": "p1",
  "fields": [
    {
      "fieldType": "ContainerRepresentation",
      "id": "container1",
      "name": null,
      "type": "container",
      "value": null,
      "required": false,
      "readOnly": false,
      "overrideId": false,
      "placeholder": null,
      "optionType": null,
      "hasEmptyValue": null,
      "options": null,
      "restUrl": null,
      "restIdProperty": null,
      "restLabelProperty": null,
      "layout": null,
      "sizeX": 0,
      "sizeY": 0,
      "row": 0,
      "col": 0,
      "visibilityCondition": null,
      "fields": {
        "1": [
          {
            "fieldType": "FormFieldRepresentation",
            "id": "label1",
            "name": "Label1",
            "type": "text",
            "value": null,
            "required": false,
            "readOnly": false,
            "overrideId": false,
            "placeholder": null,
            "optionType": null,
            "hasEmptyValue": null,
            "options": null,
            "restUrl": null,
            "restIdProperty": null,
            "restLabelProperty": null,
            "layout": {
              "row": 0,
              "column": 0,
              "colspan": 1
            },
            "sizeX": 1,
            "sizeY": 1,
            "row": 0,
            "col": 0,
            "visibilityCondition": null
          }
        ],
        "2": [ ]
      }
    },
    {
      "fieldType": "DynamicTableRepresentation",
      "id": "label21",
      "name": "Label 21",
      "type": "dynamic-table",
      "value": null,
      "required": false,
      "readOnly": false,
      "overrideId": false,
      "placeholder": null,
      "optionType": null,
      "hasEmptyValue": null,
      "options": null,
      "restUrl": null,
      "restIdProperty": null,
      "restLabelProperty": null,
      "layout": {
        "row": 10,
        "column": 0,
        "colspan": 2
      },
      "sizeX": 2,
      "sizeY": 2,
      "row": 10,
      "col": 0,
      "visibilityCondition": null,
      "columnDefinitions": [
        {
          "id": "p2",
          "name": "c2",
          "type": "String",
          "value": null,
          "optionType": null,
          "options": null,
          "restUrl": null,
          "restIdProperty": null,
          "restLabelProperty": null,
          "required": true,
          "editable": true,
          "sortable": true,
          "visible": true
        }
      ]
    }
  ],
  "outcomes": [ ]
}
```

Note: To retrieve field values such as the `typeahead` field, use the following REST endpoint:

```bash
GET api/enterprise/process-definitions/{processDefinitionId}/start-form-values/{field}
```

This returns a list of form values.

### Start Process Instance

To start process instances, use:

```bash
POST api/enterprise/process-instances
```

With a json body that contains following properties:

* `processDefinitionId`: The process definition identifier. Do not use it with processDefinitionKey.
* `processDefinitionKey`: The process definition key. Do not use it with `processDefinitionId`.
* `name`: The name to give to the created process instance.
* `values`: A JSON object with the form field Id and form field values. The Id of the form field is retrieved from the start form call (see above).
* `outcome`: If the start form has outcomes, this is one of those values.
* `variables`: Contains a JSON array of variables. Values and outcomes can’t be used with variables.

The response will contain the process instance details including the ID.

Once started, the completed form (if defined) can be fetched using:

```bash
GET /enterprise/process-instances/{processInstanceId}/start-form
```

### Process Instance List

To get the list of process instances:

```bash
POST api/enterprise/process-instances/query
```

with a json body containing the query parameters. The following parameters are possible:

* `processDefinitionId`
* `appDefinitionId`
* state (possible values are `running`, `completed` and `all`)
* sort (possible values are `created-desc`, `created-asc`, `ended-desc`, `ended-asc`)
* start (for paging, default 0)
* size (for paging, default 25)

**Example response:**

```json
{
    "size": 6,
    "total": 6,
    "start": 0,
    "data":[
            {"id": "2511", "name": "Test step - January 8th 2015", "businessKey": null, "processDefinitionId": "teststep:3:29"...},
            ...
    ]
}
```

To get a process instance:

```bash
GET api/enterprise/process-instances/{processInstanceId}
```

To get diagram for a process instance:

```bash
GET api/enterprise/process-instances/{processInstanceId}/diagram
```

To delete a Process Instance:

```bash
DELETE api/enterprise/process-instances/{processInstanceId}
```

To suspend a process instance:

```bash
PUT api/enterprise/process-instances/{processInstanceId}/suspend
```

To activate a process instance:

```bash
PUT api/enterprise/process-instances/{processInstanceId}/activate
```

Where, `processinstanceId` is the Id of the process instance.

### Get Process Instance Details

```bash
GET api/enterprise/process-instances/{processInstanceId}
```

### Delete a Process Instance

```bash
DELETE api/enterprise/process-instances/{processInstanceId}
```

### Process Instance Audit Log As JSON

If you need the audit log information as a JSON you can use the next URL:

```bash
GET api/enterprise/process-instances/{process-instance-id}/audit-log
```

**Response**

**`200 Ok`**

Returns a JSON string representing the full audit log for the requested process instance. For example:

```json
{
  "processInstanceId": "5",
  "processInstanceName": "myProcessInstance",
  "processDefinitionName": "TEST decision process",
  "processDefinitionVersion": "1",
  "processInstanceStartTime": "Wed Jan 20 16:18:46 EET 2016",
  "processInstanceEndTime": null,
  "processInstanceInitiator": "Mr Activiti",
  "entries": [
    {
      "index": 1,
      "type": "startForm",
      "timestamp": "Wed Jan 20 16:18:46 EET 2016",
      "selectedOutcome": null,
      "formData": [
        {
          "fieldName": "Text1",
          "fieldId": "text1",
          "value": "TEST"
        }
      ],
      "taskName": null,
      "taskAssignee": null,
      "activityId": null,
      "activityName": null,
      "activityType": null
      "startTime": "Thu Feb 16 16:32:05 GMT 2017",
      "endTime": "Thu Feb 16 16:32:05 GMT 2017",
      "durationInMillis": 1
    },
    {
      "index": 2,
      "type": "activityExecuted",
      "timestamp": "Wed Jan 20 16:18:46 EET 2016",
      "selectedOutcome": null,
      "formData": [],
      "taskName": null,
      "taskAssignee": null,
      "activityId": "startEvent1",
      "activityName": "",
      "activityType": "startEvent"
      "startTime": "Thu Feb 16 16:32:05 GMT 2017",
      "endTime": "Thu Feb 16 16:32:09 GMT 2017",
      "durationInMillis": 24054
    },
    {
      "index": 3,
      "type": "activityExecuted",
      "timestamp": "Wed Jan 20 16:18:47 EET 2016",
      "selectedOutcome": null,
      "formData": [],
      "taskName": null,
      "taskAssignee": null,
      "activityId": "sid-15E18ED8-252F-4A24-9E93-68F53FE28535",
      "activityName": "",
      "activityType": "serviceTask"
      "startTime": "Thu Feb 16 16:32:05 GMT 2017",
      "endTime": "Thu Feb 16 16:32:09 GMT 2017",
      "durationInMillis": 24054
    },
    {
      "index": 4,
      "type": "activityExecuted",
      "timestamp": "Wed Jan 20 16:18:48 EET 2016",
      "selectedOutcome": null,
      "formData": [],
      "taskName": null,
      "taskAssignee": null,
      "activityId": "sid-001FD811-C171-40E3-9C62-602621672022",
      "activityName": "",
      "activityType": "userTask"
      "startTime": "Thu Feb 16 16:32:05 GMT 2017",
      "endTime": "Thu Feb 16 16:32:09 GMT 2017",
      "durationInMillis": 24054
    },
    {
      "index": 5,
      "type": "taskCreated",
      "timestamp": "Wed Jan 20 16:18:48 EET 2016",
      "selectedOutcome": null,
      "formData": [],
      "taskName": null,
      "taskAssignee": "Mr Activiti",
      "activityId": null,
      "activityName": null,
      "activityType": null
      "startTime": "Thu Feb 16 16:32:05 GMT 2017",
      "endTime": "Thu Feb 16 16:32:09 GMT 2017",
      "durationInMillis": 24054
    }
  ],
  "decisionInfo": {
    "calculatedValues": [
      {
        "name": "outputVariable1",
        "value": "1.0"
      }
    ],
    "appliedRules": [
      {
        "title": "Rule 1 (TEST Decision Table 1)",
        "expressions": [
          {
            "type": "CONDITION",
            "variable": "text1",
            "value": "== 'TEST'"
          },
          {
            "type": "OUTCOME",
            "variable": "outputVariable1",
            "value": "1"
          }
        ]
      }
    ]
  }
}
```

### Process instance variables

A process instance can have several variables.

To get process instance variables:

```bash
GET api/enterprise/process-instances/{processInstanceId}/variables
```

Where, `processInstanceId` is the Id of the process instance.

To create process instance variables:

```bash
PUT api/enterprise/process-instances/{processInstanceId}/variables
```

To update existing variables in a process instance:

```bash
PUT api/enterprise/process-instances/{processInstanceId}/variables
```

**Example response**:

```json
{
     "name":"myVariable",
     "type":"string",
     "value":"myValue"
}
```

Where:

* `name` - Name of the variable
* `type` - Type of variable, such as string
* `value` - Value of the variable

To update a single variable in a process instance:

```bash
PUT api/enterprise/process-instances/{processInstanceId}/variables/{variableName}
```

To get a single variable in a process instance:

```bash
GET api/enterprise/process-instances/{processInstanceId}/variables/{variableName}
```

To get all process instance variables:

```bash
GET api/enterprise/process-instances/{processInstanceId}/variables
```

To get a specific process instance variable:

```bash
GET api/enterprise/process-instances/{processInstanceId}/variables/{variableName}
```

To delete a specific process instance variable:

```bash
DELETE api/enterprise/process-instances/{processInstanceId}/variables/{variableName}
```

### Process Instance Identity links

Either the users or groups involved with a process instance.

To create an identity link of a process instance:

```bash
POST api/enterprise/process-instances/{processInstanceId}/identitylinks
```

**Example request**:

```json
{
     "user": "1",
     "type": "customType"
}
```

Get identity links of a process instance:

```bash
GET api/enterprise/process-instances/{processInstanceId}/identitylinks
```

Get identity links by family type of a process instance:

```bash
GET api/enterprise/process-instances/{processInstanceId}/identitylinks/{family}
```

Where, `Family` should contain users or groups, depending on the identity you want to link.

To get involved people in a process instance:

```bash
GET api/enterprise/process-instances/{processInstanceId}/identitylinks
```

You can get identity links for either user or groups. For example:

```bash
GET api/enterprise/process-instances/{processInstanceId}/identitylinks/users
GET api/enterprise/process-instances/{processInstanceId}/identitylinks/groups
```

### Task List

To return a list of tasks, use:

```bash
POST api/enterprise/tasks/query
```

which includes a JSON body containing the query parameters.

The following parameters are available:

* `appDefinitionId`
* `processInstanceId`
* `processDefinitionId`
* `text` (the task name will be filtered with this, using *like* semantics : `%text%`)
* `assignment`
    * `assignee` : where the current user is the assignee
    * `candidate`: where the current user is a task candidate
    * `group_x`: where the task is assigned to a group where the current user is a member of. The groups can be fetched through the profile REST endpoint
    * no value: where the current user is involved
* `state` (`completed` or `active`)
* `includeProcessVariables` (set to `true` to include process variables in the response)
* `includeTaskLocalVariables` (set to `true` to include task variables in the response)
* `sort` (possible values are `created-desc`, `created-asc`, `due-desc`, `due-asc`)
* `start` (for paging, default 0)
* `size` (for paging, default 25)

**Example response:**

```json
{
    "size": 6,
    "total": 6,
    "start": 0,
    "data":[
            {
                "id": "2524",
                "name": "Task",
                "description": null,
                "category": null,
                "assignee":{"id": 1, "firstName": null, "lastName": "Administrator", "email": "admin@app.activiti.com"},
                "created": "2015-01-08T10:58:37.193+0000",
                "dueDate": null,
                "endDate": null,
                "duration": null,
                "priority": 50,
                "processInstanceId": "2511",
                "processDefinitionId": "teststep:3:29",
                "processDefinitionName": "Test step",
                "processDefinitionDescription": null,
                "processDefinitionKey": "teststep",
                "processDefinitionCategory": "http://www.activiti.org/test",
                "processDefinitionVersion": 3,
                "processDefinitionDeploymentId": "26",
                "formKey": "5"
            }
            ...
    ]
}
```

### Task Details

```bash
GET api/enterprise/tasks/{taskId}
```

Response is similar to the list response.

### Task Form

```bash
GET api/enterprise/task-forms/{taskId}
```

The response is similar to the response from the Start Form.

To retrieve Form field values that are populated through a REST back-end:

```bash
GET api/enterprise/task-forms/{taskId}/form-values/{field}
```

Which returns a list of form field values

To complete a Task form:

```bash
POST api/enterprise/task-forms/{taskId}
```

with a json body that contains:

* `values`: A json object with the form field ID - form field values. The Id of the form field is retrieved from the start form call (see above).
* `outcome`: Retrieves outcome values if defined in the Start form.

To save a Task form:

```bash
POST api/enterprise/task-forms/{taskid}/save-form
```

**Example response**:

```json
{

"values": {"formtextfield":"snicker doodle"},
"numberfield":"6",
"radiobutton":"red"

}
```

Where the json body contains:

* `values` : A json object with the form field ID - form field values. The Id of the form field is retrieved from the Start Form call (see above).

To retrieve a list of variables associated with a Task form:

```bash
GET api/enterprise/task-forms/{taskid}/variables
```

**Example response**

```json
[
  {
    "id": "initiator",
    "type": "string",
    "value": "3205"
  },
  {
    "id": "FormField2",
    "type": "string",
    "value": "TestVariable2"
  },
  {
    "id": "FormField1",
    "type": "string",
    "value": "TestVariable1"
  }
]
```

### Create a Standalone Task

To create a task (for the user in the authentication credentials) that is not associated with a process instance:

```bash
POST api/enterprise/tasks
```

with a json body that contains the following properties:

* `name`
* `description`

### Task Actions

To update the details of a task:

```bash
PUT api/enterprise/tasks/{taskId}
```

with a json body that can contain `name`, `description` and `dueDate` (ISO 8601 string)

For example:

**Example request body:**

```json
{
  "name" : "IchangedTaskName",
  "description" : "description-updated",
  "dueDate" : "2015-01-11T22:59:59.000Z",
  "priority":10,
  "formKey": "100"
}
```

To delegate a task:

```bash
PUT api/enterprise/tasks/{taskId}/action/delegate
```

**Example request body**:

```json
{
     "userId": "1000"
}
```

To resolve a task:

```bash
PUT api/enterprise/tasks/{taskId}/action/resolve
```

To complete a task (standalone or without a task form) (**Note**: No json body needed!):

```bash
PUT api/enterprise/tasks/{taskId}/action/complete
```

To claim a task (in case the task is assigned to a group):

```bash
PUT api/enterprise/tasks/{taskId}/action/claim
```

No json body needed. The task will be claimed by the user in the authentication credentials.

To assign a task to a user:

```bash
PUT api/enterprise/tasks/{taskId}/action/assign
```

with a json body that contains the `assignee` property set to the `ID` of a user.

To involve a user with a task:

```bash
PUT api/enterprise/tasks/{taskId}/action/involve
```

with a json body that contains the `userId` property set to the `ID` of a user.

To remove an involved user from a task:

```bash
PUT api/enterprise/tasks/{taskId}/action/remove-involved
```

with a json body that contains the `userId` property set to the `ID` of a user.

To attach a form to a task:

```bash
PUT api/enterprise/tasks/{taskId}/action/attach-form
```

with a json body that contains the `formId` property set to the the `ID` of a form.

To attach a form to a task:

```bash
DELETE api/enterprise/tasks/{taskId}/action/remove-form
```

### Task Variables

To create new task variables:

```bash
POST api/enterprise/tasks/{taskId}/variables
```

To get all task variables:

```bash
GET api/enterprise/tasks/{taskId}/variables
```

To get a task variable by name:

```bash
GET api/enterprise/tasks/{taskId}/variables/{variableName}
```

To update an existing task variable:

```bash
PUT api/enterprise/tasks/{taskId}/variables/{variableName}
```

**Example response**:

```json
{
     "name":"myVariable",
     "scope":"local",
     "type":"string",
     "value":"myValue"
}
```

Where:

* `name` - Name of the variable.
* `scope` - Global or local. If global is provided, then the variable will be a process-instance variable.
* `type` - Type of variable, such as string.
* `value` - Value of the variable.

To delete a task variable:

```bash
DELETE api/enterprise/tasks/{taskId}/variables/{variableName}
```

To delete all task variables:

```bash
DELETE api/enterprise/tasks/{taskId}/variables
```

Where, `taskId` is the ID of the task.

### Task Identity links

To get all identity links for a task:

```bash
GET api/enterprise/tasks/{taskId}/identitylinks
```

To create an identity link on a task:

```bash
POST api/enterprise/tasks/{taskId}/identitylinks
```

**Example response**:

```json
{
     "user": "1",
     "type": "customType"
}
```

To get a single identity link on a task:

```bash
GET api/enterprise/tasks/{taskId}/identitylinks/{family}/{identityId}/{type}
```

To delete an identity link on a task:

```bash
DELETE api/enterprise/tasks/{taskId}/identitylinks/{family}/{identityId}/{type}
```

Where:

* `taskId`: The ID of the task.
* `family`: Indicates either groups or users, depending on the type of identity.
* `identityId`: The ID of the identity.
* `type`: The type of identity link.

### User Task Filters

Custom task queries can be saved as a user task filter. To get the list of task filters for the authenticated user:

```bash
GET api/enterprise/filters/tasks
```

with an option request parameter `appId` to limit the results to a specific app.

To get a specific user task filter:

```bash
GET api/enterprise/filters/tasks/{userFilterId}
```

To create a new user task filter:

```bash
POST api/enterprise/filters/tasks
```

with a json body that contains following properties:

* `name` : Name of the filter.
* `appId` : App ID where the filter can be used.
* `icon` : Path of the icon image.
* `filter`
    * `sort` : Possible values: created-desc, created-asc, due-desc, due-asc.
    * `state` : Open, completed.
    * `assignment` : Involved, assignee, or candidate.

To update a user task filter:

```bash
PUT api/enterprise/filters/tasks/{userFilterId}
```

with a json body that contains following properties:

* `name` : Name of the filter
* `appId` : App ID where the filter can be used.
* `icon` : Path of the icon image.
* `filter`
    * `sort` : Created-desc, created-asc, due-desc, due-asc.
    * `state` : Open, completed.
    * `assignment` : Involved, assignee, or candidate

To delete a user task filter:

```bash
DELETE api/enterprise/filters/tasks/{userFilterId}
```

To order the list of user task filters:

```bash
PUT api/enterprise/filters/tasks
```

with a json body that contains following properties:

* `order` : Array of user task filter IDs.
* `appId` : App ID.

To get a list of user process instance filters

```bash
GET api/enterprise/filters/processes
```

with an option request parameter `appId` to limit the results to a specific app.

To get a specific user process instance task filter:

```bash
GET api/enterprise/filters/processes/{userFilterId}
```

To create a user process instance task filter:

```bash
PUT  api/enterprise/filters/processes
```

with a json body that contains following properties:

* `name` : Name of the filter.
* `appId` : App ID where the filter can be used.
* `icon` : Path of the icon image.
* `filter`
    * `sort` : Created-desc, created-asc.
    * `state` : Running, completed, or all.

To update a user process instance task filter:

```bash
PUT  api/enterprise/filters/processes/{userFilterId}
```

with a json body that contains following properties:

* `name` : Name of the filter.
* `appId` : App ID, where the filter can be used.
* `icon` : Path of the icon image.
* `filter`
    * `sort` : Possible values: created-desc, created-asc.
    * `state` : Running, completed, or all.

To delete a user process instance task filter

```bash
DELETE  api/enterprise/filters/processes/{userFilterId}
```

### Comments

Comments can be added to a process instance or a task.

To get the list of comments:

```bash
GET api/enterprise/process-instances/{processInstanceId}/comments
```

```bash
GET api/enterprise/tasks/{taskId}/comments
```

To create a comments:

```bash
POST api/enterprise/process-instances/{processInstanceId}/comments
```

```bash
POST api/enterprise/tasks/{taskId}/comments
```

with in the json body one property called `message`, with a value that is the comment text.

### Checklists

You can add checklists to a task for tracking purposes.

To get a checklist:

```bash
GET api/enterprise/tasks/{taskId}/checklist
```

To create a checklist:

```bash
POST api/enterprise/tasks/{taskId}/checklist
```

**Example request body:**

```json
{
    "assignee": {"id": 1001},
    "name": "mySubtask",
    "parentTaskId": "20086"
}
```

To change the order of the items on a checklist:

```bash
PUT api/enterprise/tasks/{taskId}/checklist
```

with a json body that contains an ordered list of checklist items ids:

* `order` : Array of checklist item ids

### Task Audit Info (as JSON)

To obtain the audit information for a specific task in JSON format, use the following URL:

```bash
GET api/enterprise/tasks/{taskId}/audit
```

**Response**

***200 Ok***

If everything works as expected and the task is accessible to the current user, then the response will be as follows:

```json
{
  "taskId": "18",
  "taskName": null,
  "processInstanceId": "5",
  "processDefinitionName": "TEST decision process",
  "processDefinitionVersion": 1,
  "assignee": "Mr Activiti",
  "startTime": "Wed Jan 20 22:03:05 EET 2016",
  "endTime": "Wed Jan 20 22:03:09 EET 2016",
  "formData": [],
  "selectedOutcome": null,
  "comments": []
}
```

## Process Engine ReST API

The Process Engine REST API is a supported equivalent of the Activiti Open Source API. This means that all operations described in the [Activiti User Guide](http://activiti.org/userguide/index.html#_rest_api){:target="_blank"} are available as documented there, except for REST endpoints that are not relevant for the enterprise product (for example, forms, as they are implemented differently).

This REST API is available on `<your-server-and-context-root>/api/`

For example, fetching process definitions is described as an HTTP GET on `repository/process-definitions`. This maps to:

```xml
<your-server-and-context-root>/api/repository/process-definitions
```

>**Note:** You can control access to the Engine API using the “Access the Activiti REST API” capability (**Identity Management -> Capabilities**). This matches the Activiti Engine (Java) API, which is agnostic of user permissions. This means that when calling any of the operations, the tenant identifier must **always be provided in the url**, even if the system does not have multitenancy (there will always be one tenant in that case):

For example `<your-server-and-context-root>/api/repository/process-definitions?tenantId=tenant_1`

## Historic processes and tasks

This section covers the examples for querying historic process instances and task instances in the Process Services API. You can query for historic process instances and tasks to get information about ongoing and past process instances, or tasks.

### Historic process instance queries

To run a historic process instance query:

```bash
POST api/enterprise/historic-process-instances/query
```

To run a historic task instance query:

```bash
POST api/enterprise/historic-tasks/query
```

### Get historic process instances

The following table lists the request parameters to be used in the JSON body POST. For example, to filter historic process instances that completed before the given date (`startedBefore`):

```bash
POST api/enterprise/historic-process-instances/query
```

With a JSON body request:

```json
{
"startedBefore":"2016-06-16",
}
```

Example response:

```json
{
"size": 25,
"total": 200,
"start": 0,
  "data": [
    {
      "id": "2596",
      "name": "Date format example - June 7th 2016",
      "businessKey": null,
      "processDefinitionId": "dateformatexample:1:2588",
      "tenantId": "tenant_1",
      "started": "2016-06-07T14:18:34.433+0000",
      "ended": null,
      "startedBy": {
        "id": 1,
        "firstName": null,
        "lastName": "Administrator",
        "email": "admin@app.activiti.com"
      },
{
"id": "2596",
. . .
```

Where, `size` is the size of the page or number of items per page. By default, the value is `25`, `start` is the page to start on. Pages are counted from 0-N. By default, the value is 0, which means 0 will be the first page.

|`processInstanceId`|An ID of the historic process instance.|
|`processDefinitionKey`|The process definition key of the historic process instance.|
|`processDefinitionId`|The process definition id of the historic process instance.|
|`businessKey`|The business key of the historic process instance.|
|`involvedUser`|An involved user of the historic process instance. Where, `InvolvedUser` is the ID of the user.|
|`finished`|Indicates if the historic process instance is complete. Where, the value may only be `True`, as the default values are `True` or `False`.|
|`superProcessInstanceId`|An optional parent process id of the historic process instance.|
|`excludeSubprocesses`|Returns only historic process instances which aren’t sub-processes.|
|`finishedAfter`|Returns historic process instances that finished after the given date. The date is displayed in `yyyy-MM-ddTHH:MM:SS` format.|
|`finishedBefore`|Returns historic process instances that finished before the given date. The date is displayed in `yyyy-MM-ddTHH:MM:SS` format.|
|`startedAfter`|Returns historic process instances that were started after the given date. The date is displayed in `yyyy-MM-ddTHH:MM:SS` format.|
|`startedBefore`|Returns historic process instances that were started before the given date. The date is displayed in `yyyy-MM-ddTHH:MM:SS` format.|
|`startedBy`|Returns only historic process instances that were started by the selected user.|
|`includeProcessVariables`|Indicates if the historic process instance variables should be returned.|
|`tenantId`|Returns instances with the given `tenantId`.|
|`tenantIdLike`|Returns instances with a `tenantId` like the given value.|
|`withoutTenantId`|If true, only returns instances without a `tenantId` set. If false, the `withoutTenantId` parameter is ignored.|

### Get historic task instances

The following table lists the request parameters that can be used in the JSON body POST. For example, in case of `taskCompletedAfter`:

```bash
POST api/enterprise/historic-tasks/query
```

With a json body request:

```json
{
"taskCompletedAfter":"2016-06-16",
"size":50,
"start":0
}
```

Example response:

```json
{
  "size": 4,
  "total": 4,
  "start": 0,
  "data": [
    {
      "id": "7507",
      "name": "my task",
      "assignee": {
        "id": 1000,
        "firstName": "Homer",
        "lastName": "Simpson",
        "email": "homer.simpson@gmail.com"
      },
      "created": "2016-06-17T15:14:26.938+0000",
      "dueDate": null,
      "endDate": "2016-06-17T16:09:39.197+0000",
      "duration": 3312259,
      "priority": 50,
. . .
```

|`taskId`|An ID of the historic task instance.|
|`processInstanceId`|The process instance id of the historic task instance.|
|`processDefinitionKey`|The process definition key of the historic task instance.|
|`processDefinitionKeyLike`|The process definition key of the historic task instance, which matches the given value.|
|`processDefinitionId`|The process definition id of the historic task instance.|
|`processDefinitionName`|The process definition name of the historic task instance.|
|`processDefinitionNameLike`|The process definition name of the historic task instance, which matches the given value.|
|`processBusinessKey`|The process instance business key of the historic task instance.|
|`processBusinessKeyLike`|The process instance business key of the historic task instance that matches the given value.|
|`executionId`|The execution id of the historic task instance.|
|`taskDefinitionKey`|The task definition key for tasks part of a process|
|`taskName`|The task name of the historic task instance.|
|`taskNameLike`|The task name with like operator for the historic task instance.|
|`taskDescription`|The task description of the historic task instance|
|`taskDescriptionLike`|The task description with like operator for the historic task instance.|
|`taskDefinitionKey`|The task identifier from the process definition for the historic task instance.|
|`taskDeleteReason`|The task delete reason of the historic task instance.|
|`taskDeleteReasonLike`|The task delete reason with like operator for the historic task instance.|
|`taskAssignee`|The assignee of the historic task instance.|
|`taskAssigneeLike`|The assignee with like operator for the historic task instance.|
|`taskOwner`|The owner of the historic task instance.|
|`taskOwnerLike`|The owner with like operator for the historic task instance.|
|`taskInvolvedUser`|An involved user of the historic task instance. Where, *InvolvedUser* is the User ID.|
|`taskPriority`|The priority of the historic task instance.|
|`finished`|Indicates if the historic task instance is complete.|
|`processFinished`|Indicates if the process instance of the historic task instance is finished.|
|`parentTaskId`|An optional parent task ID of the historic task instance.|
|`dueDate`|Returns only historic task instances that have a due date equal to this date.|
|`dueDateAfter`|Returns only historic task instances that have a due date after this date.|
|`dueDateBefore`|Returns only historic task instances that have a due date before this date.|
|`withoutDueDate`|Returns only historic task instances that have no due-date. When false value is provided, this parameter is ignored.|
|`taskCompletedOn`|Returns only historic task instances that have been completed on this date.|
|`taskCompletedAfter`|Returns only historic task instances that have been completed after this date.|
|`taskCompletedBefore`|Return only historic task instances that have been completed before this date.|
|`taskCreatedOn`|Returns only historic task instances that were created on this date.|
|`taskCreatedBefore`|Returns only historic task instances that were created before this date.|
|`taskCreatedAfter`|Returns only historic task instances that were created after this date.|
|`includeTaskLocalVariables`|Indicates if the historic task instance local variables should be returned.|
|`includeProcessVariables`|Indicates if the historic task instance global variables should be returned.|
|`tenantId`|Returns historic task instances with the given tenantId.|
|`tenantIdLike`|Returns historic task instances with a tenantId like the given value.|
|`withoutTenantId`|If `true`, only returns historic task instances without a `tenantId` set. If `false`, `withoutTenantId` is ignored.|

### User and Group lists

A common use case is when a user wants to select another user or group, for example, when assigning a task.

To retrieve users:

```bash
GET api/enterprise/users
```

Use the following parameters:

* `filter`: Filters by the user’s first and last name.
* `email`: Retrieves users by email
* `externalId`: Retrieves users by their external ID.
* `externalIdCaseInsensitive`: Retrieves users by external ID, ignoring case.
* `externalId`: Retrieves users by their external ID (set by the LDAP sync, if used)
* `excludeTaskId`: Excludes users that are already part of this task.
* `excludeProcessId`: Excludes users that are already part of this process instance.

**Example response:**

```json
{
    "size": 2,
    "total": 2,
    "start": 0,
    "data": [
        {
            "id": 1,
            "firstName": null,
            "lastName": "Administrator",
            "email": "admin@app.activiti.com"
        },
        {
            "id": 1000,
            "firstName": "John",
            "lastName": "Doe",
            "email": "johndoe@alfresco.com"
        }
    ]
}
```

To retrieve a picture of a user:

```bash
GET api/enterprise/users/{userId}/picture
```

To retrieve groups:

```bash
GET api/enterprise/groups
```

with optional parameter `filter` that filters by group name.

Additional options:

* `externalId`: Retrieves a group by their external ID.
* `externalIdCaseInsensitive`: Retrieves a group by their external ID, ignoring case.

**Example response:**

```json
{
     "size": 2,
     "total": 2,
     "data": [
          {
               "externalId": null,
               "name": "Engineering",
               "id": 2000
          },
          {
               "externalId": null,
               "name": "Marketing",
               "id": 2001
          }
     ],
     "start": 0
}
```

Get the users for a given group:

```bash
GET api/enterprise/groups/{groupId}/users
```

**Example response:**

```json
{
     "size": 3,
     "total": 3,
     "data": [
          {
               "email": "john@alfresco.com",
               "lastName": "Test",
               "firstName": "John",
               "id": 10
          },
          {
               "email": "mary@alfresco.com",
               "lastName": "Test",
               "firstName": "Mary",
               "id": 8
          },
          {
               "email": "patrick@alfresco.com",
               "lastName": "Test",
               "firstName": "Patrick",
               "id": 9
          }
     ],
     "start": 0
}
```

With a json body that contains:

* `order` : An array of user task filter IDs

### Content

Content such as documents and other files can be attached to process instances and tasks.

To retrieve the content attached to a process instance:

```bash
GET api/enterprise/process-instances/{processInstanceId}/content
```

By default, this will return all content: The related content (for example content uploaded via the UI in the "related content" section of the task detail page) and the field content (content uploaded as part of a form).

To only return the related content, add `?isRelatedContent=true` to the url. Similarly, add `?isRelatedContent=false` when the return response should include only field content.

Similarly, for a task:

```bash
GET api/enterprise/tasks/{taskId}/content
```

By default, this will return all content: The related content (for example content uploaded via the UI in the "related content" section of the task detail page) and the field content (content uploaded as part of a form).

To only return the related content, add `?isRelatedContent=true` to the url. Similarly, add `?isRelatedContent=false` when the return response should include only field content.

**Example response:**

```json
{
  "size": 5,
  "total": 5,
  "start": 0,
  "data": [
    {
      "id": 4000,
      "name": "tasks.PNG",
      "created": "2015-01-01T01:01:01.000+0000",
      "createdBy": {
        "id": 1,
        "firstName": "null",
        "lastName": "Admin",
        "email": "admin@app.activiti.com",
        "pictureId": 5
      },
      "relatedContent": true,
      "contentAvailable": true,
      "link": false,
      "mimeType": "image/png",
      "simpleType": "image",
      "previewStatus": "queued",
      "thumbnailStatus": "queued"
    }
        ]
}
```

To get content metadata:

```bash
GET api/enterprise/content/{contentId}
```

To delete content:

```bash
DELETE api/enterprise/content/{contentId}
```

To get the actual bytes for content:

```bash
GET api/enterprise/content/{contentId}/raw
```

To upload content to a process instance:

```bash
POST api/enterprise/process-instances/{processInstanceId}/raw-content
```

where the body contains a *multipart file*. Add the `isRelatedContent` parameter to the url to set whether the content 
is *related* or not. For a process instance, this currently won’t have any influence on what is visible in the UI. Note that the default value for this parameter is `false`.

To upload content to a task:

```bash
POST api/enterprise/tasks/{taskId}/raw-content
```

where the body contains a *multipart file*. Add the `isRelatedContent` parameter to the url to set whether the content is *related* or not. If `true`, the content will show up in the "related content" section of the task details. Note that the default value for this parameter is `false`.

To relate content (eg from Alfresco) to a process instance:

```bash
POST api/enterprise/process-instances/{processInstanceId}/content
```

where the json body contains following properties:

* name
* link (boolean)
* source
* sourceId
* mimeType
* linkUrl

Add the `isRelatedContent` parameter to the url to set whether the content is related or not. If `true`, the content will show up in the "related content" section of the task details. Note that the default value for this parameter is `true` (different from the call above with regular content!).

**Example body (from Alfresco OnPremise):**

```json
{
   "name":"Image.png",
   "link":true,
   "source":"alfresco-1",
   "sourceId":"30358280-88de-436e-9d4d-8baa9dc44f17@swsdp",
   "mimeType":"image/png"
}
```

To upload content for a task:

```bash
POST api/enterprise/process-instances/{taskId}/content
```

Where the json body contains following properties:

* name
* link (boolean)
* source
* sourceId
* mimeType
* linkUrl

In case of a start form with content fields, there is no task or process instance to relate to.

Following REST endpoints can be used:

```bash
POST api/enterprise/content/raw
```

### Thumbnails

To retrieve the thumbnail of a certain piece of content:

```bash
GET api/enterprise/content/{contentId}/rendition/thumbnail
```

### Identity Management

For more info about Identity Management, see [this]({% link process-services/latest/using/process/index.md %}#identity-management) section.

#### Tenants

Following REST endpoints are **only available for users that are either a tenant admin or a tenant manager**.

Get all tenants (tenant manager only):

```bash
GET api/enterprise/admin/tenants
```

Create a new tenant (tenant manager only):

```bash
POST api/enterprise/admin/tenants
```

the json body of this post contains two properties: `name` and `active` (boolean).

Update a tenant:

```bash
PUT api/enterprise/admin/tenants/{tenantId}
```

the json body of this post contains two properties: `name` and `active` (boolean).

Get tenant details:

```bash
GET api/enterprise/admin/tenants/{tenantId}
```

Delete a tenant:

```bash
DELETE api/enterprise/admin/tenants/{tenantId}
```

Get tenant events:

```bash
GET api/enterprise/admin/tenants/{tenantId}/events
```

Get tenant logo:

```bash
GET api/enterprise/admin/tenants/{tenantId}/logo
```

Change tenant logo:

```bash
POST api/enterprise/admin/tenants/{tenantId}/logo
```

where the body is a multi part file.

>**Note:** The *Create a new tenant* and *Delete a tenant* endpoints are not available where you have installed a *single-tenant* license.

#### Users

Following REST endpoints are **only available for users that are either a tenant admin or a tenant manager**.

Get a list of users:

```bash
GET api/enterprise/admin/users
```

with parameters

* `filter` : Filters by user name.
* `status` : Possible values are `pending`, `inactive`, `active`, `deleted`.
* `sort` : Possible values are `createdAsc`, `createdDesc`, `emailAsc` or `emailDesc` (default `createdAsc`).
* `start` : Used for paging.
* `size` : Use for paging.

To create a new user:

```bash
POST api/enterprise/admin/users
```

with a json body that **must** have following properties:

* email
* firstName
* lastName
* password
* status (possible values are `pending`, `inactive`, `active`, `deleted`)
* type (enterprise or trial. Best to set this to enterprise)
* tenantId

Update user details:

```bash
PUT api/enterprise/admin/users/{userId}
```

with a json body containing `email`, `firstName` and `lastName`

Update user password:

```bash
PUT api/enterprise/admin/users
```

with a json body like

```json
{
        "users" : [1098, 2045, 3049]
        "password" : "123"
}
```

Note that the `users` property is an array of user ids. This allows for bulk changes.

Update user status:

```bash
PUT api/enterprise/admin/users
```

with a json body like

```json
{
        "users" : [1098, 2045, 3049]
        "status" : "inactive"
}
```

Note that the `users` property is an array of user ids. This allows for bulk changes.

Update user tenant id (only possible for _tenant manager):

```bash
PUT api/enterprise/admin/users
```

with a json body like

```json
{
        "users" : [1098, 2045, 3049]
        "tenantId" : 1073
}
```

Note that the `users` property is an array of user ids. This allows for bulk changes.

#### Groups

The following REST endpoints are **only available for users that are either a tenant admin or a tenant manager**.

Internally, there are two types of groups:

* **Functional groups**: Map to organizational units.
* **System groups**: Provide users capabilities. When you assign a capability to a group, every member of that group is assigned with the capability.

Get all groups:

```bash
GET api/enterprise/admin/groups
```

Optional parameters:

* `tenantId` : Useful to a Tenant Manager user
* `functional` (boolean): Only return functional groups if true

Get group details:

```bash
GET api/enterprise/admin/groups/{groupId}
```

**Example response:**

```json
{
     "capabilities": [{
          "name": "access-reports",
          "id": 1
     }],
     "name": "analytics-users",
     "tenantId": 1,
     "users": [
          {
               "tenantId": 1,
               "firstName": null,
               "password": null,
               "type": "enterprise",
               "company": null,
               "externalId": null,
               "capabilities": null,
               "tenantPictureId": null,
               "created": "2015-01-08T08:30:25.164+0000",
               "pictureId": null,
               "latestSyncTimeStamp": null,
               "tenantName": null,
               "lastName": "Administrator",
               "id": 1,
               "lastUpdate": "2015-01-08T08:30:25.164+0000",
               "email": "admin@app.activiti.com",
               "fullname": " Administrator",
               "groups": null
          },
          {
               "tenantId": 1,
               "firstName": "John",
               "password": null,
               "type": "enterprise",
               "company": null,
               "externalId": null,
               "capabilities": null,
               "tenantPictureId": null,
               "created": "2015-01-08T13:22:36.198+0000",
               "pictureId": null,
               "latestSyncTimeStamp": null,
               "tenantName": null,
               "lastName": "Doe",
               "id": 1000,
               "lastUpdate": "2015-01-08T13:34:22.273+0000",
               "email": "johndoe@alfresco.com",
               "fullname": "John Doe",
               "groups": null
          }
     ],
     "id": 1,
     "groups": [],
     "externalId": null,
     "status": "active",
     "lastSyncTimeStamp": null,
     "type": 0,
     "parentGroupId": null
}
```

Use the optional request parameter `includeAllUsers` (boolean value, by default true) to avoid getting all the users at once (not ideal if there are many users).

Use the following call:

```bash
GET api/enterprise/admin/groups/{groupId}/users?page=2&pageSize=20
```

Create new group:

```bash
POST api/enterprise/admin/groups
```

Where the json body contains following properties:

* `name`
* `tenantId`
* type (0 for system group, 1 for functional group)
* `parentGroupId` (only possible for functional groups. System groups can’t be nested)

Update a group:

```bash
PUT api/enterprise/admin/groups/{groupId}
```

Only the `name` property can be in the json body.

Delete a group:

```bash
DELETE api/enterprise/admin/groups/{groupId}
```

Add a user to a group:

```bash
POST api/enterprise/admin/groups/{groupId}/members/{userId}
```

Delete a user from a group:

```bash
DELETE api/enterprise/admin/groups/{groupId}/members/{userId}
```

Get the list of possible capabilities for a system group:

```bash
GET api/enterprise/admin/groups/{groupId}/potential-capabilities
```

Add a capability from previous list to the group:

```bash
POST api/enterprise/admin/groups/{groupId}/capabilities
```

where the json body contains one property `capabilities` that is an array of strings.

Remove a capability from a group:

```bash
DELETE api/enterprise/admin/groups/{groupId}/capabilities/{groupCapabilityId}
```

#### Alfresco Content Services repositories

A tenant administrator can configure one or more Alfresco Content Services repositories to use when working with content. To retrieve the repositories configured for the tenant of the user used to do the request:

```bash
GET api/enterprise/profile/accounts/alfresco
```

which returns something like:

```json
{
     "size": 2,
     "total": 2,
     "data": [
          {
               "name": "TS",
               "tenantId": 1,
               "id": 1,
               "accountUsername": "jbarrez",
               "created": "2015-03-26T14:24:35.506+0000",
               "shareUrl": "http://ts.alfresco.com/share",
               "lastUpdated": "2015-03-26T15:37:21.174+0000",
               "repositoryUrl": "http://ts.alfresco.com/alfresco",
               "alfrescoTenantId": ""
          },
          {
               "name": "TsTest",
               "tenantId": 1,
               "id": 1000,
               "accountUsername": "jbarrez",
               "created": "2015-03-26T15:37:36.448+0000",
               "shareUrl": "http://tstest.alfresco.com/share",
               "lastUpdated": "2015-03-26T15:37:36.448+0000",
               "repositoryUrl": "http://tstest.alfresco.com/alfresco",
               "alfrescoTenantId": ""
          }
     ],
     "start": 0
}
```
---
title: Install using containers
---

There are two options for installing Process Services using containers:

* For trials, testing and development it's recommended to deploy with Docker for Desktop.
* For production environments, there's a reference Helm chart available for installation into a Kubernetes cluster.

> **Note:** See the [Deployment and Containerization Support Policy]({% link support/latest/policies/deployment.md %}) for information regarding the supportability of Docker images and Helm charts.

## Install with Docker

Process Services and Process Services Administrator can be deployed using separate Docker containers.

The Docker images for Process Services are available on [Docker Hub](https://hub.docker.com/u/alfresco/){:target="_blank"}.

To download the images from Docker Hub, use the following commands:

```bash
docker pull alfresco/process-services:24.1.0
```

```bash
docker pull alfresco/process-services-admin:24.1.0
```

>**Note:** If a tag isn't supplied then the latest version will be downloaded.

To run the containers locally using Docker for Desktop, use the following commands specifying a port for them to map to:

```bash
docker run -p {port}:8080 alfresco/process-services
```

```bash
docker run -p {port}:8080 alfresco/process-services-admin
```

For example, to run Process Services Administrator on port 8095 use the following:

```bash
docker run -p 8095:8080 alfresco/process-services-admin
```

Once the containers have started up, visit the following URLs to access the applications:

* `http://localhost:{port}/activiti-app`
* `http://localhost:{port}/activiti-admin`

For example `http://localhost:8095/activiti-admin` if running the Administrator application on port 8095.

>**Note:** Docker for Desktop is not a production environment.

It is possible to override the default environment variables for Process Services and Process Services Administrator,
see next sections.

### Configure Process Services variables

It is possible to override the default variable values used by the Docker container.

There are three options for specifying your own variables during a Docker deployment:

* Mount your own `activiti-app.properties` and optionally an `activiti-identity-service.properties` file in `/usr/local/tomcat/lib` using Docker volumes.
* Specifying environment variables for each properties file that points to an accessible location such as an S3 bucket:

  * Use the `EXTERNAL_ACTIVITI_APP_PROPERTIES_FILE` environment variable for an `activiti-app.properties` file.
  * Use the `EXTERNAL_ACTIVITI_IDENTITY_SERVICE_PROPERTIES_FILE` environment variable for an `activiti-identity-service.properties` file.

    >**Note:** If you choose this option, the files will be automatically downloaded into the contextual folder.

* Configure the environment variables in the Docker container by overriding the default values.

Variables that correspond to the `activiti-app.properties` file:

|Property|Description|
|--------|-----------|
|ACTIVITI_DATASOURCE_DRIVER|The JDBC driver used to connect to the database. The default is `org.h2.Driver`. |
|ACTIVITI_HIBERNATE_DIALECT|The dialect that Hibernate uses that is specific to the database type. The default is `org.hibernate.dialect.H2Dialect`. |
|ACTIVITI_LICENSE_MULTI_TENANT|Set whether the license used is a multi-tenant one or not. The default is `false`. |
|ACTIVITI_DATASOURCE_URL|The location of the database that will be used. The default is `jdbc:h2:mem:db1;DB_CLOSE_DELAY=1000`. |
|ACTIVITI_DATASOURCE_USERNAME|The username to access the database with. The default is `alfresco`. |
|ACTIVITI_DATASOURCE_PASSWORD|The password for the `ACTIVITI_DATASOURCE_USERNAME` user. The default is `alfresco`. |
|ACTIVITI_ADMIN_EMAIL|The email address for the default administrator user. The default is `admin@app.activiti.com`. |
|ACTIVITI_ADMIN_PASSWORD_HASH|The hashed password for `ACTIVITI_ADMIN_EMAIL` user. The default is ``. |
|ACTIVITI_CORS_ENABLED|Sets whether Cross Origin Resource Sharing (CORS) is enabled or not. The default is `true`. |
|ACTIVITI_CORS_ALLOWED_ORIGINS|The host origins allowed in CORS requests. There is not a default value set. You can't use `*`.|
|ACTIVITI_CORS_ALLOWED_ORIGIN_PATTERNS| The host origin patterns allowed in CORS requests. The default is `*` but you can also use a pattern.|
|ACTIVITI_CORS_ALLOWED_METHODS|The HTTP request methods allowed for CORS requests. The default is `GET,POST,HEAD,OPTIONS,PUT,DELETE`. |
|ACTIVITI_CORS_ALLOWED_HEADERS|The headers that can be set in CORS requests. The default is `Authorization,Content-Type,Cache-Control,X-Requested-With,accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers,X-CSRF-Token`. |
|ACTIVITI_CSRF_DISABLED|Sets whether Cross Site Request Forgery is disabled or not. The default is `true`. |
|ACTIVITI_ES_SERVER_TYPE|Set this to rest to enable the REST client implementation. The default is `rest`. |
|ACTIVITI_ES_REST_CLIENT_ADDRESS|The IP address of the Elasticsearch instance. The default is `localhost`. |
|ACTIVITI_ES_REST_CLIENT_PORT|The port to contact Elasticsearch through. The default is `9200`. |
|ACTIVITI_ES_REST_CLIENT_SCHEMA|Sets whether the connection to Elasticsearch uses http or https. The default is `http`. |
|ACTIVITI_ES_REST_CLIENT_AUTH_ENABLED|Sets whether authentication is enabled for the REST connection to Elasticsearch. The default is `false`. |
|ACTIVITI_ES_REST_CLIENT_USERNAME|The username of the Elasticsearch user. The default is `admin`. |
|ACTIVITI_ES_REST_CLIENT_PASSWORD|The password for the Elasticsearch user. The default is `esadmin`. |
|ACTIVITI_ES_REST_CLIENT_KEYSTORE|The keystore used to encrypt the connection to the Elasticsearch instance. |
|ACTIVITI_ES_REST_CLIENT_KEYSTORE_TYPE|The type of keystore used for encrypting the Elasticsearch connection data. The default is `jks`. |
|ACTIVITI_ES_REST_CLIENT_KEYSTORE_PASSWORD|The password for the keystore used encrypting the Elasticsearch connection data. |

Variables that correspond to the `activiti-identity-service.properties` file:

|Property|Description|
|--------|-----------|
|IDENTITY_SERVICE_ENABLED|Sets whether the Identity Service is enabled or not. The default is `false`. |
|IDENTITY_SERVICE_REALM|The name of the realm used by the Identity Service. The default is `alfresco`. |
|IDENTITY_SERVICE_SSL_REQUIRED|Sets whether communication to and from the Identity Service is over HTTPS or not. The default is `none`. |
|IDENTITY_SERVICE_RESOURCE|The Client ID for Process Services within the Identity Service realm. The default is `alfresco`. |
|IDENTITY_SERVICE_PRINCIPAL_ATTRIBUTE|The attribute used to populate `UserPrincipal` with. This needs to be set to `email` for Process Services to authenticate with the Identity Service. |
|IDENTITY_SERVICE_ALWAYS_REFRESH_TOKEN|Sets whether the token is refresh for every request to the Identity Service or not. The default is `true`. |
|IDENTITY_SERVICE_AUTODETECT_BEARER_ONLY|Allows for unauthorized access requests to be redirected to the Identity Service sign in page. The default is `true`. |
|IDENTITY_SERVICE_TOKEN_STORE|The location of where the account information token is stored. The default is `session`. |
|IDENTITY_SERVICE_ENABLE_BASIC_AUTH|Sets whether basic authentication is allowed is supported by the adapter. The default is `true`. |
|IDENTITY_SERVICE_PUBLIC_CLIENT|Sets whether the adapter sends credentials for the client to the Identity Service. It will not send the credentials if this is set to `true`. |
|IDENTITY_SERVICE_AUTH|Sets the authentication URL for the Identity Service. The `localhost` value and port number need to be replaced with the DNS or address used for the deployment, for example `http://localhost:8080/auth`. |
|IDENTITY_CREDENTIALS_SECRET|The secret key for the client if the access type is not `public`. |
|IDENTITY_SERVICE_USE_BROWSER_BASED_LOGOUT|Sets whether signing out of Process Services calls the Identity Service `logout URL`. If set to `true`, set the **Admin URL** to `https://{server}:{port}/activiti-app/` under the client settings in the Identity Service management console. |

#### Configure Process Services Administrator variables

It is possible to override the default variable values used by the Docker container.

There are three options for specifying your own variables during a Docker deployment:

* Mount your own `activiti-admin.properties` file in `/usr/local/tomcat/lib` using Docker volumes
* Use the environment variable `ACTIVITI_ADMIN_EXTERNAL_PROPERTIES_FILE` to point to an accessible location such as an S3 bucket:

    ```yaml
    environment:
      ACTIVITI_ADMIN_EXTERNAL_PROPERTIES_FILE: https://your-s3-bucket.com/activiti-admin.properties
    ```

* Configure the environment variables in the Docker container by overriding the default values:

|Property|Description|
|--------|-----------|
|ACTIVITI_ADMIN_DATASOURCE_DRIVER|The JDBC driver used to connect to the database for Process Services Administrator. The default is `org.h2.Driver`. |
|ACTIVITI_ADMIN_HIBERNATE_DIALECT|The dialect that Hibernate uses that is specific to the database type for the Process Services Administrator. The default is `org.hibernate.dialect.H2Dialect`. |
|ACTIVITI_ADMIN_REST_APP_HOST|The location of the Administrator API. This should be set to the DNS name of the deployment. The default is `localhost`. |
|ACTIVITI_ADMIN_REST_APP_PORT|The port for the Administrator API. The default is `80`. |
|ACTIVITI_ADMIN_REST_APP_USERNAME|The default user for the Admin API. The default is `admin@app.activiti.com`. |
|ACTIVITI_ADMIN_REST_APP_PASSWORD|The default password for the Admin API. The default is `admin`. |

## Install on Amazon EKS

Use the following information as a reference guide to deploy Process Services on Amazon's Elastic Container Service for Kubernetes (Amazon EKS).

**Important:** Deployment on AWS such as with Amazon EKS, is only recommended for customers with a good knowledge of Process Services, and strong competencies in AWS and containerized deployment.

There are several prerequisites for deploying on Amazon EKS using Helm charts:

* An Amazon EKS environment. See [Amazon's EKS getting started Guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html){:target="_blank"} as a reference point.
* A Kubernetes namespace configured for Process Services.
* Helm and Tiller configured in the Kubernetes cluster. See [Helm's quickstart guide](https://docs.helm.sh/using_helm/#quickstart-guide){:target="_blank"} for reference.

Use the following steps to deploy Process Services, Process Services Administrator, a Postgres database and optionally the [Identity Service]({% link identity-service/1.2/index.md %}):

1. Create a Kubernetes secret to access images in Quay.

    1. Sign into Quay.io with your credentials using the following command:

        ```bash
        docker login quay.io
        ```

    2. Generate a base64 value for your `dockercfg` using one of the following commands:

        ```bash
        # Linux
        cat ~/.docker/config.json | base64
        ```

        ```bash
        # Windows
        base64 -w 0 ~/.docker/config.json
        ```

    3. Create a file called `secrets.yaml` and add the following content to it, using your base64 string from the previous step as the `.dockerconfigjson` value:

        ```yaml
        apiVersion: v1
        kind: Secret
        metadata:
          name: quay-registry-secret
        type: kubernetes.io/dockerconfigjson
        data:
          .dockerconfigjson: <your-base64-string>
        ```

    4. Upload your `secrets.yaml` file to the namespace you are deploying into using the following command:

        ```bash
        kubectl create -f <file-location>/secrets.yaml --namespace=$NAMESPACE
        ```

2. Create a Kubernetes secret for the Process Services license file with the following command:

    ```bash
    kubectl create secret generic licenseaps --from-file=./activiti.lic
    --namespace=$NAMESPACE
    ```

3. Add the Alfresco Kubernetes repository to Helm with the following command:

    ```bash
    helm repo add alfresco-stable https://kubernetes-charts.alfresco.com/stable
    ```

4. [Update the properties](#helm-properties) for the Process Services chart.

5. **(Optional)**: To enable the Identity Service:

    1. Enable the Identity Service in the `alfresco-infrastructure` section of the `values.yaml`:

        ```text
        alfresco-identity-service:
        enabled: true
        ```

    2. Set the Process Services environment variable `IDENTITY_SERVICE_ENABLED` to `true`.

    3. Set the Process Services environment variable `IDENTITY_SERVICE_AUTH` to `http://$DNS/auth`.

6. Deploy the chart using a command similar to the following:

    ```bash
    helm install alfresco-stable/alfresco-process-services --set dnsaddress="http://$DNS" --namespace=$NAMESPACE --set license.secretName=licenseaps
    ```

The applications will be available at the following URLs:

* Process Services: `http://$DNS/activiti-app`
* Process Services Administrator: `http://$DNS/activiti-admin`
* Identity Service administrator console: `http://$DNS/auth/admin`

>**Note:** To change the context paths of any of the applications, edit the ingress paths:

```yaml
ingress:
    path: /activiti-app
```

### Helm properties

The following information details the properties that can be set for Process Services when deploying via Helm on Amazon's Elastic Container Service for Kubernetes (Amazon EKS).

The following properties can be configured in the `values.yaml` file or overridden as environment variables:

|Property|Description|
|--------|-----------|
|ACTIVITI_DATASOURCE_DRIVER|The JDBC driver used to connect to the database. The default is `org.postgresql.Driver`. |
|ACTIVITI_HIBERNATE_DIALECT|The dialect that Hibernate uses that is specific to the database type. The default is `org.hibernate.dialect.PostgreSQLDialect`. |
|ACTIVITI_LICENSE_MULTI_TENANT|Set whether the license used is a multi-tenant one or not. The default is `false`. |
|ACTIVITI_DATASOURCE_URL|The location of the database that will be used. |
|ACTIVITI_DATASOURCE_USERNAME|The username to access the database with. The default is `alfresco`. |
|ACTIVITI_DATASOURCE_PASSWORD|The password for the `ACTIVITI_DATASOURCE_USERNAME` user. The default is `alfresco`. |
|ACTIVITI_CORS_ENABLED|Sets whether Cross Origin Resource Sharing (CORS) is enabled or not. The default is `true`. |
|ACTIVITI_CORS_ALLOWED_ORIGINS|The host origins allowed in CORS requests. There is not a default value set. You can't use `*`.|
|ACTIVITI_CORS_ALLOWED_ORIGIN_PATTERNS| The host origin patterns allowed in CORS requests. The default is `*` but you can also use a pattern.|
|ACTIVITI_CORS_ALLOWED_METHODS|The HTTP request methods allowed for CORS requests. The default is `GET,POST,HEAD,OPTIONS,PUT,DELETE`. |
|ACTIVITI_CORS_ALLOWED_HEADERS|The headers that can be set in CORS requests. The default is `Authorization,Content-Type,Cache-Control,X-Requested-With,accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers,X-CSRF-Token`. |
|ACTIVITI_CSRF_DISABLED|Sets whether Cross Site Request Forgery is disabled or not. The default is `true`. |
|ACTIVITI_ES_SERVER_TYPE|Set this to rest to enable the REST client implementation. The default is `rest`. |
|ACTIVITI_ES_REST_CLIENT_ADDRES|The IP address of the REST client. The default is `localhost`. |
|ACTIVITI_ES_REST_CLIENT_PORT|The port to contact Elasticsearch through. The default is `9200`. |
|ACTIVITI_ES_REST_CLIENT_SCHEMA|Sets whether the connection to Elasticsearch uses http or https. The default is `http`. |
|ACTIVITI_ES_REST_CLIENT_AUTH_ENABLED|Sets whether authentication is enabled for the REST connection to Elasticsearch. The default is `false`. |
|ACTIVITI_ES_REST_CLIENT_USERNAME|The username of the Elasticsearch user. The default is `admin`. |
|ACTIVITI_ES_REST_CLIENT_PASSWORD|The password for the Elasticsearch user. The default is `esadmin`. |
|ACTIVITI_ES_REST_CLIENT_KEYSTORE|The keystore used to encrypt the connection to the Elasticsearch instance. |
|ACTIVITI_ES_REST_CLIENT_KEYSTORE_TYPE|The type of keystore used for encrypting the Elasticsearch connection data. The default is `jks`. |
|ACTIVITI_ES_REST_CLIENT_KEYSTORE_PASSWORD|The password for the keystore used encrypting the Elasticsearch connection data. |
|ACTIVITI_ADMIN_DATASOURCE_DRIVER|The JDBC driver used to connect to the database for Process Services Administrator. The default is `org.postgresql.Driver`. |
|ACTIVITI_ADMIN_HIBERNATE_DIALECT|The dialect that Hibernate uses that is specific to the database type for the Process Services Administrator. The default is `org.hibernate.dialect.PostgreSQLDialect`. |
|ACTIVITI_ADMIN_EMAIL|The email address for the default administrator user. The default is `admin@app.activiti.com`. |
|ACTIVITI_ADMIN_PASSWORD_HASH|The hashed password for `ACTIVITI_ADMIN_EMAIL` user. |
|ACTIVITI_ADMIN_REST_APP_HOST|The location of the Administrator API. This should be set to the DNS name of the deployment. The default is `localhost`. |
|ACTIVITI_ADMIN_REST_APP_PORT|The port for the Administrator API. The default is `80`. |
|ACTIVITI_ADMIN_REST_APP_USERNAME|The default user for the Admin API. The default is `admin@app.activiti.com`. |
|ACTIVITI_ADMIN_REST_APP_PASSWORD|The default password for the Admin API. The default is `admin`. |
|APP_CONFIG_BPM_HOST|The location of Process Services. The default is `http://DNS`. |
|IDENTITY_SERVICE_ENABLED|Sets whether the Identity Service is enabled or not. The default is `false`. |
|IDENTITY_SERVICE_REALM|The name of the realm used by the Identity Service. The default is `alfresco`. |
|IDENTITY_SERVICE_SSL_REQUIRED|Sets whether communication to and from the Identity Service is over HTTPS or not. The default is `none`. |
|IDENTITY_SERVICE_RESOURCE|The Client ID for Process Services within the Identity Service realm. The default is `alfresco`. |
|IDENTITY_SERVICE_PRINCIPAL_ATTRIBUTE|The attribute used to populate `UserPrincipal` with. This needs to be set to `email` for Process Services to authenticate with the Identity Service. |
|IDENTITY_SERVICE_ALWAYS_REFRESH_TOKEN|Sets whether the token is refresh for every request to the Identity Service or not. The default is `true`. |
|IDENTITY_SERVICE_AUTODETECT_BEARER_ONLY|Allows for unauthorized access requests to be redirected to the Identity Service sign in page. The default is `true`. |
|IDENTITY_SERVICE_TOKEN_STORE|The location of where the account information token is stored. The default is `session`. |
|IDENTITY_SERVICE_ENABLE_BASIC_AUTH|Sets whether basic authentication is allowed is supported by the adapter. The default is `true`. |
|IDENTITY_SERVICE_PUBLIC_CLIENT|Sets whether the adapter sends credentials for the client to the Identity Service. It will not send the credentials if this is set to `true`. |
|IDENTITY_CREDENTIALS_SECRET|The secret key for the client if the access type is not `public`. |
|IDENTITY_SERVICE_AUTH|Sets the authentication URL for the Identity Service. The `localhost` value and port number need to be replaced with the DNS or address used for the deployment. The default is `http://localhost:8080/auth`. |
|IDENTITY_SERVICE_USE_BROWSER_BASED_LOGOUT|Sets whether signing out of Process Services calls the Identity Service `logout URL`.If set to `true`, set the **Admin URL** to `https://{server}:{port}/activiti-app/` under the client settings in the Identity Service management console. The default is `true`. |
---
title: Install Process Services
nav: false
---

There are several options for installing Process Services and its associated applications.

The applications available to deploy are:

* Process Services
* Process Services Administrator

The following methods are available to deploy Process Services:

* [Install with setup Wizards]({% link process-services/latest/install/manual.md %}#install-using-setup-wizards)
* [Install manually]({% link process-services/latest/install/manual.md %}#install-manually)
* [Install using containers]({% link process-services/latest/install/container.md %})

## Container concepts

Installing Process Services using containers introduces a number of concepts.

You can start Process Services from a number of Docker images. These images are available in the repositories [Docker Hub](https://hub.docker.com){:target="_blank"} and [Quay](https://quay.io/){:target="_blank"}. However, starting individual Docker containers based on these images, and configuring them to work together might not be the most productive way to get up and running.

There are **Helm charts** available to deploy Process Services in a Kubernetes cluster, for example, on Amazon Web Services (AWS). These charts are a deployment template which can be used as the basis for your specific deployment needs. The Helm charts are undergoing continual development and improvement and should not be used "as-is" for a production deployment, but should help you save time and effort deploying Process Services for your organization.

The following is a list of concepts and technologies that you'll need to understand as part of installing Process Services using containers. If you know all about Docker, then you can skip this part.

### Virtual Machine Monitor (Hypervisor)

A Hypervisor is used to run other OS instances on your local host machine. Typically it's used to run a different OS on your machine, such as Windows on a Mac. When you run another OS on your host it is called a guest OS, and it runs in a Virtual Machine (VM).

### Image

An image is a number of layers that can be used to instantiate a container. This could be, for example, Java and Apache Tomcat. You can find all kinds of Docker images on the public repository [Docker Hub](https://hub.docker.com/){:target="_blank"}. There are also private image repositories (for things like commercial enterprise images), such as the one Alfresco uses called [Quay](https://quay.io/){:target="_blank"}.

### Container

An instance of an image is called a container. If you start this image, you have a running container of this image. You can have many running containers of the same image.

### Docker

Docker is one of the most popular container platforms. [Docker](https://www.docker.com/){:target="_blank"} provides functionality for deploying and running applications in containers based on images.

### Dockerfile

A **Dockerfile** is a script containing a successive series of instructions, directions, and commands which are run to form a new Docker image. Each command translates to a new layer in the image, forming the end product. The Dockerfile replaces the process of doing everything manually and repeatedly. When a Dockerfile finishes building, the end result is a new image, which you can use to start a new Docker container.

### Difference between containers and virtual machines

It's important to understand the difference between using containers and using VMs. Here's a picture from [What is a Container - Docker](https://www.docker.com/what-container){:target="_blank"}:

![vm-vs-container]({% link process-services/images/vm-vs-container.png %})

The main difference is that when you run a container, you are not starting a complete new OS instance. This makes containers much more lightweight and quicker to start. A container also takes up much less space on your
hard-disk as it doesn't have to ship the whole OS.
---
title: Install manually
---

There are two options for installing Process Services without using containers, depending on the environment you are deploying in:

* For trials, testing and development it's recommended to install using a setup wizard.
* For production environments it is recommended that you install manually.

## Install using setup wizards

There are setup wizards available for Linux, macOS and Windows operating systems.

> **Important**: The setup wizards are evaluation copies that are useful for trials and experimentation. The h2 database provided with them is not suitable for use in a production environment.

The setup wizards install their own Apache Tomcat container for Process Services, an h2 database and all prerequisite software for Process Services to run on your chosen operating system.

{% capture linux %}

Use these instructions to install Process Services on Linux.

1. Download the Linux setup wizard from your trial email.

2. Locate the bin you just downloaded and run the following command against it to update its permissions:

    ```bash
    chmod 777 <installer file name>
    ```

3. Run the setup wizard using the following command:

    ```bash
    ./<installer file name>
    ```

4. Read and accept the **License Agreement**.

5. Use the default **Installation Directory** or choose your own.

6. Select an **Installation Profile**.

7. Complete the installation.

    >**Note:** A message will appear displaying the default credentials and URL to use.

8. Navigate to your installation directory and run the following command to start the application:

    ```bash
    ./start-process-services.sh
    ```

    >**Note:** The default installation location is `/home/{user}/alfresco/process-services-{version}`

9. Enter `http://localhost:8080/activiti-app` into a browser once the application has started to begin using Process Services.

    >**Note:** Use the default credentials to log in. View the `process-services-readme.txt`, by default found in `/home/{user}/alfresco/process-services-{version}`, if you can't remember them.

10. Install the administrator application:

    1. Rename the file `activiti-admin.war.undeployed` found in `/home/{user}/alfresco/process-services-{version}/tomcat/webapps` to `activiti-admin.war`

    2. Stop and restart Tomcat.

    3. Navigate to `http://localhost:8080/activiti-admin` once the application has started back up.

{% endcapture %}
{% capture mac %}

Use these instructions to install Process Services on a Mac.

1. Download the Mac setup wizard from your trial email.

2. Locate the dmg you just downloaded using **Finder** and double click it.

3. Double click the Alfresco logo to launch the setup wizard.

    >**Note:** Click **Open** if you are prompted about opening files from the internet.

4. Read and accept the **License Agreement**.

5. Use the default **Installation Directory** or choose your own.

6. Select an **Installation Profile**.

7. Complete the installation.

    >**Note:** A message will appear displaying the default credentials and URL to use.

8. Navigate to your installation directory and double click the **StartProcessServices** application.

    >**Note:** The default installation location is `Applications\alfresco\process-services-{version}`

9. Enter `http://localhost:8080/activiti-app` into a browser once the application has started to begin using Process Services.

    >**Note:** Use the default credentials to log in. View the `process-services-readme.txt`, by default found in `Applications\alfresco\process-services-{version}`, if you can't remember them.

10. Install the administrator application:

    1. Rename the file `activiti-admin.war.undeployed` found in `Applications\alfresco\process-services-{version}\tomcat\webapps` to `activiti-admin.war`

    2. Stop and start Tomcat via the **Terminal** or by closing and re-opening the **StartProcessServices** application.

    3. Navigate to `http://localhost:8080/activiti-admin` once the application has started back up.

{% endcapture %}
{% capture windows-setup %}

Use these instructions to install Process Services on Windows.

1. Download the Windows setup wizard from your trial email.

2. Locate the exe you just downloaded and double click it to launch the setup wizard.

3. Read and accept the **License Agreement**.

4. Use the default **Installation Directory** or choose your own.

5. Select an **Installation Profile**.

6. Complete the installation.

    >**Note:** A message will appear displaying the default credentials and URL to use.

7. Navigate to your installation directory and double click the **StartProcessServices** application.

    >**Note:** The default installation location is `C:\Program Files\alfresco\process-services-{version}`

8. Enter `http://localhost:8080/activiti-app` into a browser once the application has started to begin using Process Services.

    >**Note:** Use the default credentials to log in. View the `process-services-readme.txt`, by default found in `C:\Program Files\alfresco\process-services-{version}`, if you can't remember them.

9. Install the administrator application:

    1. Rename the file `activiti-admin.war.undeployed` found in `C:\Program Files\alfresco\process-services-{version}\tomcat\webapps` to `activiti-admin.war`

    2. Stop and start Tomcat via the **Command Line** or by closing and re-opening the **StartProcessServices** application.

    3. Navigate to `http://localhost:8080/activiti-admin` once the application has started back up.

{% endcapture %}

{% include tabs.html tableid=setup opt1="Linux" content1=linux opt2="MacOS" content2=mac opt3="Windows" content3=windows-setup %}

After installing you will need to [apply a valid license file](#license) to your installation.

## Install manually

To install Process Services and the administrator application manually, download the relevant Web Application Archive (WAR) files.

It is recommended that you install the administrator application in a separate container to Process Services in a production environment. It is possible to install the two applications in the same web container, however separate containers allows them to be managed in isolation from one another.

The download files are available from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

### Install Process Services

Use these instructions to install the Process Services application using the WAR file.

Ensure you have read the [supported platforms]({% link process-services/latest/support/index.md %}) to confirm that your web container and database combination is supported before commencing with installation.

1. Install your web container and database.

    >**Note:** The following steps use Tomcat and MySQL for examples.

2. Create a schema for the `activiti-app` application. The default name is `activiti`

    In MySQL:

    ```sql
    CREATE DATABASE activiti DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    ```

3. Create a user and password. This example will use `alfresco/alfresco`

    In MySQL:

    ```sql
    CREATE USER 'alfresco'@'localhost' IDENTIFIED BY 'alfresco';
    ```

4. Grant full privileges on the schema to this new user.

    In MySQL:

    ```sql
    GRANT ALL ON activiti.* TO 'alfresco'@'localhost';
    ```

5. Edit the `activiti-app.properties` file supplied with the WAR file.

    1. Uncomment the correct properties for the database you have installed.

    2. Update the values for the schema and credentials created in the previous steps and check that the `hibernate.dialect` property matches your chosen database type.

        For example:

        ```text
        com.mysql.cj.jdbc.Driver
        datasource.url=jdbc:mysql://127.0.0.1:3306/activiti?characterEncoding=UTF-8
        datasource.username=alfresco
        datasource.password=alfresco
        hibernate.dialect=org.hibernate.dialect.MySQLDialect
        ```

        >**Note:** Example syntax is provided in the `activiti-app.properties` file for other database types.

        > **Important:** Ensure that the driver for your database is on the classpath of the web application.

    3. Set a location for the file content to be at using `contentstorage.fs.rootFolder`.
       
        > **Important:** Ensure that the path exists; for example if you set `contentstorage.fs.rootFolder=/var/lib/act_data` the path `/var/lib/act_data` must exist and be accessible by the process user.  
        > If the folder doesn't exist them you won't be able to upload files from your pc to Activiti.
 
    4. Set a location for the search and analytics indexes using `elastic-search.data.path`.

6. Ensure that the driver for your database is on the classpath of your web container.

    For Tomcat and MySQL:

    Copy the MySQL java connector jar to `<Tomcat install location>/lib`

7. Copy the `activiti-app.war` and `activiti-app.properties` files to your web container.

    For Tomcat:

    * `<Tomcat install location>/webapps/activiti-app.war`
    * `<Tomcat install location>/lib/activiti-app.properties`

8. Start up your web container.

    For Tomcat:

    * On Linux or MacOS run `<Tomcat install location>\\bin\\catalina.sh`
    * On Windows run `<Tomcat install location>/bin/catalina.bat`

9. Enter `http://localhost:8080/activiti-app` into a browser to begin using Process Services.

After installing you will need to [apply a valid license file](#license) to your installation.

### Install Process Services Administrator

Use these instructions to install Process Services Administrator using the WAR file.

Ensure you have read the [supported platforms]({% link process-services/latest/support/index.md %}) to confirm that your web container and database combination is supported before commencing with installation.

1. Install your web container and database.

    >**Note:** The following steps use Tomcat and MySQL for examples.

2. Create a schema for the `activiti-admin` application. The default name is `activitiadmin`

    In MySQL:

    ```sql
    CREATE DATABASE activitiadmin DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    ```

3. Create a user and password. This example will use `alfresco/alfresco`

    > **Important:** You do not need to complete this step if you use the same user you created when [installing Process Services](#install-process-services) and can skip to the next step.

    In MySQL:

    ```sql
    CREATE USER 'alfresco'@'localhost' IDENTIFIED BY 'alfresco';
    ```

4. Grant full privileges on the schema to this new user.

    In MySQL:

    ```sql
    GRANT ALL ON activitiadmin.* TO 'alfresco'@'localhost';
    ```

5. Edit the `activiti-admin.properties` file supplied with the main Process Services WAR file download.

    1. Uncomment the correct properties for the database you have installed.

    2. Update the values for the schema and credentials created in the previous steps and check that the `hibernate.dialect` property matches your chosen database type.

        For example:

        ```text
        com.mysql.cj.jdbc.Driver
        datasource.url=jdbc:mysql://127.0.0.1:3306/activitiadmin?characterEncoding=UTF-8
        datasource.username=alfresco
        datasource.password=alfresco
        hibernate.dialect=org.hibernate.dialect.MySQLDialect
        ```

        >**Note:** Example syntax is provided in the `activiti-admin.properties` file for other database types.

6. Copy the `activiti-admin.war` and `activiti-admin.properties` files to your web container.

    For Tomcat:

    * `<Tomcat install location>/webapps/activiti-admin.war`
    * `<Tomcat install location>/lib/activiti-admin.properties`

7. Start up your web container.

    For Tomcat:

    * On Linux or MacOS run `<Tomcat install location>\bin\catalina.sh`
    * On Windows run `<Tomcat install location>/bin/catalina.bat`

8. Enter `http://localhost:8080/activiti-admin` into a browser to begin using Process Services Administrator.

After installing you will need to [apply a valid license file](#license) to your installation.

## License

A valid license file is required to run Process Services.

A license file can be obtained from [support](https://support.alfresco.com){:target="_blank"} or a link is provided via email to download a temporary (30-day) license if you signed up for a free trial.

Logging into Process Services as an administrator will display a notification if a license is not currently valid.
Notifications are displayed when:

* No valid license file can be found
* A license file has expired or is not valid until a date in the future
* The current license file is close to expiring

There are two methods for uploading a license file to Process Services.

### Upload a license

To upload a license through the user interface:

1. Click the **UPLOAD LICENSE** button or use the top menu **Administrator** > **Upload license**

2. Browse to, or drag your `activiti.lic` file into the pop-up.

Alternatively, you can manually move the `activiti.lic` file into the web container.

For example using Tomcat: `<Tomcat install location>\lib\`
---
title: Supported platforms
---

Here is a list of the individual components that have been through the complete Alfresco Quality Assurance and Certification activities for Alfresco Process Services 24.x.

Choose a combination of products to build your own Supported Stack. If anything is unclear then please contact our Support team - submit a case via [Hyland Community]({% link support/latest/contact.md %}).

{% capture twenty-four-two %}

| Version | Notes |
| ------- | ----- |
| **Operating systems** | |
| Red Hat Enterprise Linux 9 | |
| Red Hat Enterprise Linux 8.8 | |
| Windows Server 2022 | |
| Rocky Linux 9 | |
| Rocky Linux 8.8 | |
| CentOS 8 x64 | |
| CentOS 7 x64 | |
| Ubuntu 22.04 | |
| Amazon Linux 2 | |
| | |
| **Databases** | |
| MariaDB 10.6 | 3.1.4 |
| MySQL 8.0 | `mysql-connector-java-8.0.33.jar` |
| MS SQL Server 2022 | `mssql-jdbc-11.2.jar` |
| MS SQL Server 2019 | `mssql-jdbc-10.2.jar` |
| Oracle 19c | 21.7.0.0 |
| PostgreSQL 15.4 | `postgresql-42.5.1.jar` |
| PostgreSQL 14.9 | `postgresql-42.5.1.jar` |
| PostgreSQL 13.12 | `postgresql-42.5.1.jar` |
| Amazon Aurora | Use of Amazon Aurora is supported only if it is configured to emulate one of the supported versions of PostgreSQL or MySQL listed above, and the listed JDBC driver is used. |
| | |
| **Application servers** | |
| Tomcat 10 | |
| Jetty 12 | |
| | |
| **JDKs** | |
| OpenJDK 17 |  |
| Amazon Corretto 17 |  |
| | |
| **Browsers** | |
| Mozilla Firefox | |
| Microsoft Edge | Versions based on Chromium only |
| MS Internet Explorer 11 | |
| Chrome | |
| | |
| **Third party integrations** | |
| Elasticsearch 8.13.1 | |
| | |
| **Services** | |
| Alfresco Content Services 23.x |  |
| | |
| **Integrations** | |
| Identity Service 2.0 | For use with LDAP and SAML |
| Identity Service 1.2 | For use with LDAP and SAML |
| Identity Service 1.1 | For use with LDAP and SAML |
| | |
| **Applications** | |
| Alfresco Digital Workspace 4.4 |
| Alfresco Digital Workspace 4.3 | Requires Alfresco Process Services 2.4.2. |
| | |
| **Related components** | |
| VMWare ESXi 5.1.0 | For supported guest operating systems |
| Spring Boot 3.2.3 |
| Spring 6.1.4 |

{% endcapture %}

{% capture twenty-four-one %}

| Version | Notes |
| ------- | ----- |
| **Operating systems** | |
| Red Hat Enterprise Linux 9 | |
| Red Hat Enterprise Linux 8.8 | |
| Windows Server 2022 | |
| Rocky Linux 9 | |
| Rocky Linux 8.8 | |
| CentOS 8 x64 | |
| CentOS 7 x64 | |
| Ubuntu 22.04 | |
| Amazon Linux 2 | |
| | |
| **Databases** | |
| MariaDB 10.6 | 3.1.4 |
| MySQL 8.0 | `mysql-connector-java-8.0.33.jar` |
| MS SQL Server 2022 | `mssql-jdbc-11.2.jar` |
| MS SQL Server 2019 | `mssql-jdbc-10.2.jar` |
| Oracle 19c | 21.7.0.0 |
| PostgreSQL 15.4 | `postgresql-42.5.1.jar` |
| PostgreSQL 14.9 | `postgresql-42.5.1.jar` |
| PostgreSQL 13.12 | `postgresql-42.5.1.jar` |
| Amazon Aurora | Use of Amazon Aurora is supported only if it is configured to emulate one of the supported versions of PostgreSQL or MySQL listed above, and the listed JDBC driver is used. |
| | |
| **Application servers** | |
| Tomcat 10 | |
| Jetty 12 | |
| | |
| **JDKs** | |
| OpenJDK 17 |  |
| Amazon Corretto 17 |  |
| | |
| **Browsers** | |
| Mozilla Firefox | |
| Microsoft Edge | Versions based on Chromium only |
| MS Internet Explorer 11 | |
| Chrome | |
| | |
| **Third party integrations** | |
| Elasticsearch 7.17.18 | |
| | |
| **Services** | |
| Alfresco Content Services 23.x |  |
| | |
| **Integrations** | |
| Identity Service 1.2 | For use with LDAP and SAML |
| Identity Service 1.1 | For use with LDAP and SAML |
| | |
| **Applications** | |
| Alfresco Digital Workspace 4.3 | Requires Alfresco Process Services 2.4.2. |
| | |
| **Related components** | |
| VMWare ESXi 5.1.0 | For supported guest operating systems |

{% endcapture %}

{% include tabs.html tableid="supported-platforms" opt1="24.2" content1=twenty-four-two opt2="24.1" content2=twenty-four-one %}
---
title: Upgrade Process Services
---

You can upgrade from earlier versions of Process Services.

> **Note:** Before upgrading, you should back up your database and properties files, such as `activiti-app.properties`.

There are two methods for upgrading:

* Using the Process Services setup wizard
* Manually

> **Important:** If you integrate Process Services with Alfresco Content Services then be aware that from version 1.11 only repositories on version 5.2 and later are supported. Upgrade to a later version of Alfresco Content Services before updating Process Services to continue using this functionality.

## Upgrade using a setup wizard

You can use the Process Services setup wizard to upgrade to the latest version. The process is similar to [installing for the first time]({% link process-services/latest/install/manual.md %}#install-using-setup-wizards).

Follow these steps to upgrade:

1. Double-click the Process Services setup wizard.
2. Follow the instructions to install the latest version of Process Services.
3. After the installation is complete, copy the `activiti.lic` file to the Process Services installation directory: `<Install>/tomcat/lib` folder.

Alternatively, copy the license to your home directory using the terminal (OSX) or command prompt (Windows):

```bash
~/.activiti/enterprise-license/
```

```bash
C:\.activiti\enterprise-license
```

>**Tip**: You can also upload a [license]({% link process-services/latest/install/manual.md %}#license) from the user interface.

## Upgrade manually

You can upgrade using the WAR file in your application server distribution. These instructions use the WAR file from the Apache Tomcat based distribution, however you can choose from different distributions for various application servers.

Review the [Supported Stacks]({% link process-services/latest/support/index.md %}) list to see what’s supported.

Follow these steps to upgrade using the War file:

1. Stop the web server running the application.
2. Deploy the new WAR file in your web server by placing it in the `/webapps` folder in Tomcat.
3. Boot up the web server and start Process Services to check if it’s working as expected.

Any database upgrade changes should have now been applied.

## Upgrading from 1.x to 2.x

When you upgrade from Process Services 1.x to 2.x you are upgrading from Activiti 5.x to 7.x. There are breaking changes that you need to be aware of in order for your system to function correctly after you have upgraded.

> **Note:** You do not need to migrate your database when upgrading from 1.x to 2.x.

1. Navigate to [Hyland Community](https://community.hyland.com/){:target="_blank"} and download the latest Process Services installation file.  

2. In your 1.x installation you must ensure you set `activiti5.migration.enabled=true` and `activiti.engine5.enabled=true` in the `activiti-app.properties` file before migrating to Process Services 2.x.

    Setting the properties to `True` converts non-asynchronous processes to Activiti 7.x.

3. Upgrade to the latest version of Process Services using the installation file.

4. Once all in flight Process Services 1.x processes are complete you must set `activiti5.migration.enabled=false` and `activiti.engine5.enabled=false` in the `activiti-app.properties` file.

All process definitions that are Async/Timer will still be using Activiti 5.x but all other processes, including non-asynchronous processes, will be running on Activiti 7.x. This means your business operations can resume and any new processes will run on Activiti 7.x.
If you want to run the Process Services 2.3.6 installation again you must set `activiti5.migration.enabled=false` to ensure future applications restart.
Once all Process Services 1.x asynchronous processes are complete you must disable the Activiti 5.x engine by setting `activiti.engine5.enabled=false` in the `activiti-app.properties` file.

### Alfresco Process Services breaking changes

#### PVM classes

All classes from the `org.activiti.engine.impl.pvm` package and subpackages have been removed. This is because the `_PVM_` (Process Virtual Machine) model has been removed and replaced by a simpler and more lightweight model.
This means that `ActivitiImpl`, `ProcessDefinitionImpl`, `ExecutionImpl`, `TransitionImpl` are invalid.

Generally, most of the usage of these classes in version 5 came down to getting information that was contained in the process definition. In version 6, all the process definition information can be found through the _BpmnModel_, which is a Java representation of the BPMN 2.0 XML for the process definition (enhanced to make certain operations and searches easier).

The quickest way to get the `BpmnModel` for a process definition is to use the `org.activiti.engine.impl.util.ProcessDefinitionUtil` class:

```java
// The whole model
ProcessDefinitionUtil.getBpmnModel(String processDefinitionId);
// Only the specific process definition
ProcessDefinitionUtil.getProcess(String processDefinitionId);
```

#### ActivityExecution is replaced by DelegateExecution

We removed `ActivityExecution` and replaced it where used with the `DelegateExecution` class.

All methods from the `ActivityExecution` class are copied to the `DelegateExecution` class.

#### Job, timer, suspended and dead letter jobs

Activiti 5 had only 1 job table and this meant that a fairly complex query had to be executed to get the jobs that needed to be executed from the database.

From Activiti 6, the jobs have been split up in a job `ACT_RU_JOB`, timer `ACT_RU_TIMER_JOB`, suspended `ACT_RU_SUSPENDED_JOB`, and `ACT_RU_DEADLETTER_JOB` dead letter table.

#### Signaling an execution

In Activiti 6, the `signal()` methods have been renamed to `trigger()`.

This also means that `SignalableActivityBehavior`, the interface to be implemented for behaviors that can be `triggered` from external sources, is now called `TriggerableActivityBehavior`.

#### Checked Exceptions

In version 5, the delegate classes like `JavaDelegate` and `ActivityBehavior` had `throws Exception` in their signature. As with any modern framework, the use of checked Exceptions has been removed in version 6.

#### Delegate classes

`org.activiti.engine.impl.pvm.delegate.ActivityBehavior` has changed package and lives now in `org.activiti.engine.impl.delegate`.

The method `getEngineServices()` have been removed from `DelegateExecution`. It's possible to retrieve services like `RepositoryService` from `org.activiti.engine.impl.context.Context` using `Context.getProcessEngineConfiguration().getRepositoryService()`.

#### Identity management classes removed
In Activiti 7, the package `org.activiti.engine.identity` and all it's classes like `User` and `Group` were removed. While the classes have been removed the database tables like `ACT_ID_USER` and `ACT_ID_GROUP` will not be removed when upgrading from APS 1.x to APS 2. However, they'll not be created if you start APS 2 on a new database.

### Alfresco Process Services third-party breaking changes

The following are third party breaking changes that have occured.

* Spring framework upgraded from 5 to 6
* Spring boot upgraded from 2.x to 3
* Hibernate upgraded from 5.x to 6
* Jakarta EE
* Tomcat 10
* Java 17

> **Note:** If you have custom code, you’ll need to upgrade these components to use the latest APIs.
---
title: Getting started with Process Services
---

With Process Services it's easy to create, publish, and use process models and apps.

This Getting Started tutorial shows you in 3 steps how to create and use a simple expense approval process app.

## Prerequisites

Before you begin, make sure that you've following the instructions in [Installing Process Services]({% link process-services/latest/install/index.md %}).

If you’ve registered for our [cloud trial](https://www.alfresco.com/platform/process-services-bpm/trial/online){:target="_blank"} you don’t need to install anything and are ready to go.

## Step 1: Create a process definition

This is the first of three simple steps in creating a process app.

In this step, you are going to design a simple expense approval process (definition) that includes three BPMN elements:

* A **start event** to trigger the process by submitting a new expense
* A **user task** to approve or reject the request
* An **end event** to end the process

This process also includes 2 web forms.

1. Open Process Services from one of the following options:

    * **Local installation**

    * Address - `http://localhost:8080/activiti-app/#/`
    * Username - `admin@app.activiti.com/`
    * Password - `admin`

    * **Cloud trial** - [APS App Cloud](https://activiti.alfresco.com/activiti-app/#/){:target="_blank"} and use your online trial sign in details.

    ![Activiti App Landing Page]({% link process-services/images/gs-dashboard.png %})

2. Select **App Designer** on your dashboard.

3. Select **Create Process**.

4. Give the process model a name (for example “Expense approval”) and a description, then select the **BPMN Editor** as the Editor type.

5. Select **Create new model**.

    >**Note:** If this is the first time you’ve used Process Services then some help tips may be displayed. You can click **Next** to watch them or press Esc. to close them.

6. The start event is displayed on the canvas as a circle. Double-click on it and type a name, for example “Submit expense”, then click on the canvas.

7. Click the circle again and drag and drop the ![User Task]({% link process-services/images/gs-ico-user-task.png %}){:height="18px" width="18px"} User task icon to the right.

    ![Drag and Drop User Task]({% link process-services/images/gs-drag-user-task.png %})

    This adds a user task after the start event.

8. Double-click on the user task and type a name, for example “Review”, then click on the canvas.

    ![Review Task]({% link process-services/images/gs-review.png %})

9. Click the user task again and drag and drop the ![End event]({% link process-services/images/gs-end-event.png %}){:height="18px" width="18px"} end event icon (circle) to the right.

10. Double-click on the end event and type a name, for example “End process”, then click on the canvas.

    ![End Process]({% link process-services/images/gs-end-process.png %})

    The process model now has three stages:

    ![Three stages]({% link process-services/images/gs-three-stages.png %})

11. Click ![Validate Model]({% link process-services/images/gs-ico-validate.png %}){:height="18px" width="18px"} **Validate the model** on the toolbar.

    This checks models (processes, web forms, decision tables, data models, and stencils) for errors. If there are errors then a message shows you details on how to resolve them.

    Once it’s validated, you can add forms to the process using the Forms editor. This example needs two forms to be added:

    * One for the requester to submit the expense (start event)
    * One for the manager to review the expense request (user task).

    You can create forms:

    * Directly from the Process editor (embedded in the BPMN model)
    * Separately from the process model and then reference them in the design by adding a key

    In this example they’ll be created directly from the Process editor.

12. Click the start event and then click **Referenced form** in the properties panel.

    ![Submit expense]({% link process-services/images/gs-submit-expense.png %})

13. Click **New form** in the Form reference window.

14. Give the form a name (for example “Submit expense”) and a description, the click **Create form**.

    This opens the Form editor.

15. Drag stencils onto the Design canvas in this order:

    * Text
    * Amount
    * Date
    * Attach File

16. Hover over the **Text** stencil and click the ![Edit]({% link process-services/images/gs-ico-edit.png %}){:height="18px" width="18px"} Edit icon, then type "Text" as the Label and click **Close**.

    Repeat this step for the other stencils you added, and type the following labels:

    * Amount
    * Date
    * Attachment

    ![Add Labels]({% link process-services/images/gs-add-labels.png %})

17. Click ![Save]({% link process-services/images/gs-ico-save.png %}){:height="18px" width="18px"} then **Save and close editor**.

18. In the Process editor click the review expense user task and then click **Referenced form** in the properties panel.

19. Give the form a name (for example “Expense review”) and a description, the click **Create form**.

20. Drag stencils onto the Design canvas in this order:

    * Text
    * Amount
    * Date
    * Attach File

21. Hover over the Text stencil and click the Edit icon, then type "Text" as the Label and click **Close**.

    Repeat this step for the other stencils you added, and type the following labels:

    * Amount
    * Date
    * Attachment

    ![Add Labels]({% link process-services/images/gs-add-labels2.png %})

22. Click the **Outcomes** tab to add a custom outcome so that the reviewer can approve or reject the expense.

23. Select **Use custom outcomes for this form**and in the **Possible** outcomes add two outcomes:

    * Approve
    * Reject

    ![Outcomes]({% link process-services/images/gs-outcomes.png %})

24. Click ![Save]({% link process-services/images/gs-ico-save.png %}){:height="18px" width="18px"} then **Save and close editor.**

25. In the Process editor click ![Save]({% link process-services/images/gs-ico-save.png %}){:height="18px" width="18px"} then **Save**.

## Step 2: Create and publish the process application

Once you’ve created a process definition, you can create an app and add the process to it, then publish the app.

1. Click **App Designer** on your dashboard then click the **Apps** tab and select **Create App**.

2. Give the app a name (for example “Expense Approval”) and a description, then click **Create new app definition**.

3. Click **Edit included models**.

4. Select the Expense approval model. The ![Selected icon]({% link process-services/images/gs-selected.png %}){:height="18px" width="18px"} icon shows that you’ve selected it. Then click **Close**.

5. Click ![Save icon]({% link process-services/images/gs-ico-save.png %}){:height="18px" width="18px"} then select the **Publish?** option and **Save and close editor**.

6. Click ![Back icon]({% link process-services/images/gs-back.png %}){:height="18px" width="18px"} to return to your dashboard.

7. Click + to add a new app then select the Expense Approval app and click **Deploy**.

   ![App added]({% link process-services/images/gs-app-added.png %})

   The Expense Approval app is added to your dashboard.

## Step 3: Use the process application

When you’ve created and published a process app, it can be used to request a new expense for approval.

1. Click the **Expense Approval** app on your dashboard then click **Start**.

2. Complete the requested information and click **Start Process** to submit the new expense.

   ![Start process]({% link process-services/images/gs-start-process.png %})

   The Processes page now shows the new expense approval request. From here you can add comments or cancel the process.

   If you click **Show diagram** you can see the current status of your expense claim. The active user task is highlighted in green to indicate it's at review stage. Click **Close** to go back to the claim.

   ![Green review]({% link process-services/images/gs-green-review.png %})

3. Click **Review** under Active Tasks to review the claim.

   >**Note:** This would usually be done by a user with the required approval level.

   ![Approve expense]({% link process-services/images/gs-approve-expense.png %})

4. Click **Approve** to complete the task.

   This completes the claim as it is now at the end of the process flow.

   >**Note:** To review completed tasks click the **Processes** tab, then click **New Filter** and select **Completed as the Process State**.

   ![Approved]({% link process-services/images/gs-approved.png %})

   You can click **Audit Log** to download a PDF audit report. The template used for the Audit Log is part of the configuration settings and can be customized to your specific needs.

Now that you’ve set up and used your first process app, check the rest of the documentation to learn more advanced uses of Process Services.
---
title: Overview of using Process Services
---

The [Process Services application]({% link process-services/latest/using/process/index.md %}) describes how to model process definitions, forms and decision tables.

* If you're planning to run Process Services with other Alfresco applications, you can use Alfresco Digital Workspace as the end-user interface by configuring the [Process Services extension]({% link digital-workspace/latest/process/index.md %}). This extension provides Process Services functionality for end users within Digital Workspace for starting and managing tasks and processes that are currently running.
* If you're planning to use Process Services as a standalone application, you'll need to develop a custom UI using the process component for the Application Development Framework (ADF). See the [ADF Documentation](https://www.alfresco.com/abn/adf/docs/){:target="_blank"} for more details.

To quickly get started with Process Services by creating, publishing and using your first application, see the [Getting Started Guide]({% link process-services/latest/using/getting-started.md %}).
---
title: Using the Share Connector
---

The Share Connector enables you to start and run processes and tasks in an Alfresco Share environment. You can create process definitions in Process Services, and deploy them to Share.

>**Important:** The Share Connector is deprecated and [no longer supported](https://hub.alfresco.com/t5/alfresco-content-services-blog/architecture-changes-for-alfresco-content-services-version-6-0/ba-p/288930){:target="_blank"} in Alfresco Content Services 6.0. Existing deployments are supported throughout the life cycle of Alfresco Content Services 5.x. Deployments should now use the [Application Development Framework](https://www.alfresco.com/ecm-software/application-development-framework){:target="_blank"}.

Installing Share Connector changes the standard workflow and task management to access the processes and tasks by default, however you can still use the standard Share workflow capabilities.

After you have installed the Share Connector on an Alfresco Content Services system, the following new features are available:

* The Process Services user interface for working with processes and tasks embedded in Share.
* A Review Process app displayed in the Process Services user interface that includes the following pre-defined process definitions:

    * Ad hoc Task
    * Group ad hoc task
    * Review and Approve - Group
    * Review and Approve - Single person

    >**Note**: The four processes are already deployed to Share. When you start a workflow in Alfresco Content Services, you can choose from any of the pre-defined processes.

* Capability to add native Share users when selecting people and documents in a workflow.
* A new option in Share to add a new My Tasks dashlet to your home dashboard. This dashlet shows tasks created using the Share Connector. You can filter the tasks shown by: Active Tasks, Completed Tasks, Tasks Due Today, Tasks Assigned to Me, Unassigned (Pooled Tasks), and Overdue Tasks.
* Options to create workflows when initiating a workflow on a document in Share, or from the My Tasks dashlet.
* The old Alfresco My Tasks dashlet, so you can still see the old internal workflows and receive new site invitations.
* The old Alfresco My Tasks page by clicking **My Workflow Tasks** on the new My Tasks page, so you can still work with your old internal tasks.
* The old My Workflows page by clicking **Workflows I’ve started** on the new Processes page, so you can still work with your old internal workflows.
* The Workflows panel on the Document details page listing both internal and external workflows.

## Share Connector features

The Share Connector has the following features:

* **Integrated UI** - The Process Services user interface for working with processes and tasks is embedded into the Share user interface exposing processes called *Review Processes*. When selecting people and documents, the native Share components are used.
* **Review Processes** - This is available from within Share, and includes four processes: *Ad hoc Task*, *Group ad hoc task*, *Review and Approve - Group* and *Review and Approve - Single person*.
* **Site Specific Processes** - You can change the default process for a site to display a specific process app by adding an aspect included in the Share Connector to the site's *documentLibrary* folder. For detailed steps, see [Changing the default process for a site](#changing-the-default-process-for-a-site).
* **My Activiti Tasks** dashlet - Lists new tasks created using the Share Connector. You can filter tasks by: *Active Tasks, Completed Tasks, Tasks Due Today, Tasks Assigned to Me, Unassigned (Pooled Tasks), Overdue Tasks*.
* **Starting processes** - *Start workflow* in the *Document Library*, *Document details page*, and *My Activiti Tasks* creates new external processes instead of the old internal workflows in Share.
* **Activiti Task list view** - *My Tasks* page lists new external tasks using the Process Services user interface.
* **Activiti Process list view** - *Processes* page lists new external processes using the Process Services user interface.
* **Customized Share header** - The Share header menu links point to new Process Services pages for processes and tasks instead of the old pages. A link to the Process Services user interface is also available in the same menu.
* You can still reach your old internal workflows and create new ones:
    * The original *My Tasks* dashlet is still available, making it possible to list old internal workflows but also receive new site invitations.
    * The original *My Tasks* page can still be accessed by clicking the *Internal Tasks* link on the new Activiti *My Tasks* page, making it possible to continue working with the internal workflows.
    * The original *My Workflows* page can still be accessed by clicking the *Internal Workflows* link on the new Activiti *Processes* page, making it possible to continue working with the internal workflows.
    * The original *Start Workflow* page can still be accessed by clicking the *Start Workflow* link on the new Activiti *Start Process* page, making it possible to continue creating new internal workflows.
    * The *Workflows* panel on the *Document details* page will list both internal and external workflows.

## Set up the Share Connector

This section describes how to install the Share Connector in a production environment.

To set up the Share Connector, you need to configure an LDAP user database for common use between Alfresco Content Services and Process Services. This allows both systems to sync their user database against a single LDAP server. If you do not use the same LDAP user database, the Share Connector will not work.

>**Note:** If you want to get the Share Connector up and running as quickly as possible but not in a production environment, then you can use [Setting up the Share Connector Demo](#setting-up-the-share-connector-demo).

### Alfresco Content Services configuration

Alfresco Content Services can be used to:

* Upload or link related content (for example, for a task)
* Upload or link content in a form

The connection for an Alfresco Content Services installation is created by an administrator through the user interface. Accounts for connecting to an Alfresco Content Services installation are created by the users themselves.

Passwords are stored encrypted in the database. An `init` vector and secret key are used for the encryption. These keys can be changed from the default values as follows:

```text
# Passwords for non-OAuth services (eg. on-premise alfresco) are encrypted using AES/CBC/PKCS5PADDING
# It needs a 128-bit initialization vector (http://en.wikipedia.org/wiki/Initialization_vector) and a 128-bit secret key
# represented as 16 ascii characters below
security.encryption.ivspec=9kje56fqwX8lk1Z0
security.encryption.secret=wTy53pl09aN4iOkL
```

>**Note:** When the connector installed on your Alfresco Content Services server you will be able to use the Task application from Share.

#### LDAP settings in Alfresco Content Services

You must set up LDAP in Alfresco Content Services.

Detailed instructions are available in [configure LDAP]({% link content-services/latest/admin/auth-sync.md %}#configure-ldap).

For a working example of an LDAP subsystem, check the LDAP demo provided in the `activiti-share-connector.zip`. The demo amp file contains sample LDAP configuration files for getting Alfresco Content Services setup up with an LDAP (it contains no Share Connector files) configuration.

For example:

1. Unzip the `activiti.alfresco.repo-demo-ldap-X.X.X.amp` file by renaming it from `.amp` to `.zip`. You'll see some files marked with ACTIVITI SHARE CONNECTOR DEMO in the `ldap-authentication.properties` file.
2. Configure the `ldap-authentication.properties` file to match your LDAP settings, and then zip the files again and rename it back to `.amp` before dropping into the amps folder.

>**Note:** When zipping the files, follow the same structure as the original .amp file and make sure that no new root folders are introduced to the new .zip file.

#### Deploying AMPs

The Share Connector is applied to an installation using two AMP files.

From `activiti-share-connector-x.x.x.zip`, copy the AMPs to the correct amps folder in the Alfresco Content Services 
installation. For example:

* Copy the `<zip>/alfresco/amps/alfresco-connector-repo-x.x.x.amp` AMP to `<alfresco-dir>/amps`
* Copy the `<zip>/alfresco/amps_share/alfresco-connector-share-x.x.x.amp` AMP to `<alfresco-dir>/amps_share`

Install the AMPs by running the following command on a terminal from within theAlfresco Content Services installation directory, 
and then follow the instructions:

```bash
bin/apply_amps.sh
```

#### Modifying the default settings

You can modify the default settings by changing either the port or the repository configuration.

#### Process Services port

The default settings assume that Process Services is running on `http://127.0.0.1:8080/`. If so, you don’t have to do anything.

If you have Process Services running on another domain or port (that is, 9090), you can override the default setting by adding the following line at the bottom of the `<alfresco-tomcat>/shared/classes/alfresco-global.properties` file in Tomcat, where the repository is located:

```text
activiti.domain=http://127.0.0.1:9090
```

#### Alfresco Content Services repository configuration

The following steps explain how to configure the repository settings.

**Modify the default integration name**

You can modify the default Alfresco Content Services integration name by setting the value of 
`activiti.alfrescoRepositoryName`. This value must correspond to an Alfresco Content Services repository 
configured in Activiti. The default name for the integration is `alfresco-1`, however you can modify it, if required

1. Locate the alfresco-global.properties` file located at `<alfresco-tomcat>/shared/classes>`:

    ```text
    activiti.alfrescoRepositoryName=alfresco-1
    ```

2. Modify the value after the hyphen (`-`) with a number that matches the `Id` of the repository. The `repository Id` is available as a column in the **Activiti app > Identity Management app > Tenants > Alfresco Repositories** list.

**Modify the Activiti app name**

You can modify the Activiti app name to display the same app name in Share by modifying the following value in the `alfresco-global.properties` file:

```text
activiti.appDefinitionName=Some Custom App
```

**Set the secret key**

When Alfresco Content Services communicates with Process Services, it sends a secret token and user name and switches 
it for user specific Process Services token.

To override the default secret token, specify an `activiti.secret` property in the `alfresco-global.properties` file.

```text
activiti.secret=my-custom-secret
```

The secret token must match the `Repository secret` field for the repository in the Identity Management app.

The secret token appears in clear text, therefore, to avoid saving it like that:

1. Override the value (and all other properties) using Alfresco Content Services subsystems and JMX.
2. To connect to an Alfresco Content Services server using JMX, see:

    [Using a JMX client to change settings dynamically]({% link content-services/latest/config/index.md %}#using-jmx-client-to-change-settings-dynamically).

3. Once connected, navigate to `/Alfresco/Configuration/Activiti/default/Attributes` and modify the value for `activiti.secret`.

### Process Services configuration

Login to the Process Services landing page to set up the configuration for the Share Connector.

#### Configuring LDAP settings

You can find the LDAP settings for Process Services in the `activiti-ldap.properties` file located here:

```text
webapps/activiti-app/WEB-INF/classes/META-INF/activiti-app/activiti-ldap.properties
```

The default configuration works with the sample LDAP settings provided with the installation bundle, however you can easily override them by creating a new file called `<InstallLocation>/lib/activiti-ldap.properties`, and override the properties that requires changing.

For further details about configuring LDAP for Process Services, see [External Identity Management (LDAP/Active Directory)]({% link process-services/latest/config/authenticate.md %}#ldap-and-active-directory).

#### Alfresco Content Services settings

To configure Alfresco Content Services settings in Process Services, you must perform the following steps:

* Enable Share Connector
* Add a repository

##### Enable Share Connector

By default, the bundled *Review Processes* app is not created. To create one, add the following file into the 
`<InstallLocation>/lib/activiti-app.properties`.

```text
# Enable the Share Connector process app
app.review-workflows.enabled=true
```

Restart Process Services for it to take effect.

##### Add a repository

You can add a repository from the Identity Management app.

1. Start the Process Services server and log in as administrator.

2. Open the **Profile Management (Identity Management)** app, and click **Tenants** tab > **Alfresco Repositories**.

3. In **Alfresco Repositories**, create a repository pointing to the Alfresco Content Services server and Share Connector. The following is an example of the form, assuming you are running Alfresco Content Services on the same machine and on port 8080:

|Field|Value|
|-----|-----|
|Name|Acme’s Server|
|Alfresco tenant|Tenant name to use in Alfresco. When left blank, it uses the default tenant (-default-).|
|Repository base URL|[http://127.0.0.1:8080/alfresco/](http://127.0.0.1:8080/alfresco/)|
|Share base URL|[http://127.0.0.1:8080/share/](http://127.0.0.1:8080/share/)|
|Alfresco Share connector|(enabled)|
|Secret|activiti-share-connector-secret|

Once the repository is created, you can see your new repository in the **Alfresco Repositories** list. If the ID is setto 1, you are good to go and all default values are fine. However, if it is set to something else, for example, `1002`, you must stop the server and make sure your Id appears as `alfresco-1002` in the following files, and then restart your servers:

* In the Alfresco Content Services `tomcat/shared/classes/alfresco-global.properties` - Override the default by adding a new line with `activiti.alfrescoRepositoryName=alfresco-1002`
* In the Process Services `tomcat/lib/activiti-app.properties` - The property named `integration.login.alfresco-1.secret` should be named `integration.login.alfresco-1002.secret`

In addition, to make this repository work for features such as **Publish to Alfresco** or browse Alfresco for documents from Process Services, verify that a user has a user account for the repository.

#### Change the default process for a site

You can change the default process name for a site to the exact same name as the Process App name.

The easiest way to do this is to follow these steps:

1. From the **Repository** view in Alfresco Content Services, navigate to a site’s **Document Library** folder.
2. From the **Site Details** page, click **More > Manage Aspects** and add the **Activiti Process App** aspect.
3. Edit the folder properties and enter the name of the Process App in the **Process App Definition Name** field.

Where:

Aspect Id = `abs:activitiProcessApp`
Property = `abs:appDefinitionName`

#### Troubleshooting the Share Connector

**To see debug messages from Share Connector:**

1. Rename the `custom-log4j.properties.sample` file in the following location:

    ```text
    tomcat/shared/classes/alfresco/extension/
    ```

2. Remove the `.sample` suffix, and add the following line:

    ```text
    log4j.logger.com.activiti.alfresco=debug
    ```

## Set up the Share Connector demo

This section describes how to set up the Share Connector demo.

### Install Alfresco Content Services

1. Install Alfresco Content Services using the installer in Advanced mode. For Tomcat Port configuration, make sure you bump up each port by 10, for example, 8080 to 8090 and so on.
2. After the installation is complete, start Alfresco Content Services using the Application Manager app located in the home folder.
3. Verify if Alfresco Content Services works on `http://127.0.0.1:8090/share/`, log out, and stop just the *Tomcat Server* in the Application Manager app.
4. Copy the following files from the `activiti-share-connector.zip` to their corresponding folders inside the Alfresco Content Services installation directory:
    * `<zip>/alfresco/amps/activiti.alfresco.repo-X.X.X.amp` to `<alfresco-dir>/amps`
    * `<zip>/alfresco/amps_share/activiti.alfresco.share-X.X.X.amp` to `<alfresco-dir>/amps_share`
    * `<zip>/alfresco/tomcat/webapps-ldap` (copy the folder) to `<alfresco-dir>/tomcat`
        The `webapps-ldap` folder is maintained separately to ensure that it boots up before Alfresco Content Services and becomes available when it tries syncing its database against the LDAP server.

5. To configure the `webapps-ldap` folder to get picked up and run before *webapps* by Tomcat, copy the xml snippet in `<zip>/alfresco/tomcat/conf/server-ldap-snippet.xml` into your `<alfresco-dir>/tomcat/conf/server.xml` and make sure it’s placed above the existing `<Service>` element.
6. Open the `alfresco-global-properties` file and add the following configuration setting:

    ```text
    authentication.chain=ldap1:ldap
    ```

7. Copy the folder `alfresco/extension/subsystems/Authentication/ldap/ldap1/ldap-authentication.properties` from the `activiti-share-connector.zip` to `tomcat/webapps/alfresco/WEB-INF/classes/alfresco/extension/subsystems/Authentication/ldap/ldap1/ldap-authentication.properties`
8. Install the amps into Alfresco Content Services by running the following command on a terminal from your installation directory, and then follow the instructions:

    ```bash
    bin/apply_amps.sh
    ```

    >**Note:** With the standard installs you are likely to have `OutOfMemoryExceptions` due to Perm Gen space issues if you run Java 1.6 or 1.7. To prevent this, edit `tomcat/bin/setenv.sh` or equivalent and make sure to set `XX:MaxPermSize` to 512M as follows:

    ```text
    JAVA_OPTS="-XX:MaxPermSize=512M -Xms512M -Xmx8192M $JAVA_OPTS"
    ```

### Install the Share Connector

Follow these steps to install the Share Connector:

1. Install Process Services using the installer.

2. Verify the database configuration. By default, the demo H2 database is used, therefore you might want to configure Process Services to use the same database as your Alfresco Content Services installation.
    * Typically, you should create a new database schema for Process Services to use, and then configure it as described in [Database configuration]({% link process-services/latest/config/database.md %}).

3. Make sure your Process Services app has a license installed. You can add a license file manually to the `tomcat/lib` directory, or load it through the user interface.

    To load a license file from the UI, see [uploading_a_license_from_the_user_interface]({% link process-services/latest/install/manual.md %}#license) Make sure you sign out from Process Services and stop the server.

4. To use the same demo LDAP server, copy the following file from `activiti-share-connector.zip` into its corresponding folder in the Process Services installation directory:

    ```text
    <zip>/activiti/tomcat/lib/activiti-ldap.properties_ to _<activiti-dir>/tomcat/lib
    ```

5. Uncomment or add the following lines at the bottom of the `tomcat/lib/activiti-app.properties` file inside the installation folder.

    ```text
    # Enable the Alfresco Share Connector app
    app.review-workflows.enabled=true
    ```

### Start the servers for Share Connector

1. From the Application Manager, restart Alfresco Content Services to restart the Tomcat server. To ensure that the Alfresco Content Services server has fully started, check the application log and wait for the `INFO: Server startup in XXXX ms` message.
2. After the Alfresco Content Services server and the demo LDAP server have started, run Process Services as instructed by the installer and navigate to the **Identity Management** app [http://127.0.0.1:8080/activiti-app/idm/](http://127.0.0.1:8080/activiti-app/idm/).
3. Log in with admin/password defined in the demo LDAP.
4. Go to the **Tenants** page > **Alfresco Repositories** tab, and add a repository pointing to your Alfresco Content Services server:

|Field|Value|
|-----|-----|
|Name|My server name|
|Alfresco tenant|Tenant name to use in Alfresco Content Services. When left blank, it uses the default tenant (`-default-`).|
|Repository base url|[http://127.0.0.1:8090/alfresco/](http://127.0.0.1:8090/alfresco/)|
|Share base url|[http://127.0.0.1:8090/share/](http://127.0.0.1:8090/share/)|
|Alfresco Share connector|(enabled)|
|Secret|`activiti-share-connector-secret`|

**Notes**:

* The default secret is the text `activiti-share-connector-secret`, which can be changed to a different value in the Alfresco Content Services alfresco-global.properties by the property `activiti.secret`.
* After the repository is created, you can see your new repository in the **Alfresco Repositories** list. If the ID is set to 1, then all default values are fine. However, if it is set to something else, for example, `1002`, you must stop your servers and make sure your ID appears as `alfresco-1002` in the following files and then restart your servers:
* In the `alfresco-global.properties` file, override the default setting by adding a new line, substituting the ID as appropriate:

    ```text
    activiti.alfrescoRepositoryName=alfresco-1002
    ```

### Use the Share Connector

This section describes how to get started with using the Share Connector.

>**Note:** Make sure that LDAP is running before you start Alfresco Content Services and Process Services so they can sync their user databases against the LDAP server.

1. View Alfresco Share on `http://127.0.0.1:8090/share/` and Process Services on `http://127.0.0.1:8080/activiti-app/`
2. Login as a user that exist in the demo LDAP system:

    |Username|Password|Process Services role|Alfresco Content Services role|
    |--------|--------|---------------------|------------------------------|
    |jluc|password|tenant manager|user|
    |kirk|password|tenant admin|user|
    |wesley|password|user|user|
    |admin|password|admin|admin|

    >**Note:** The password for the admin user is `password` instead of the credentials used for installing Alfresco Content Services. This is because the password set in the demo LDAP server is applicable for users.

3. On the Alfresco Content Services personal dashboard page, click **Tools** and add the *My Activiti Tasks* dashlet.

When logging into Process Services as an *admin*, you can view the process definitions and *Review Processes* app inside the App Designer application by selecting the *Shared with Me* filter.

### Process Services Administrator application

You can use the Process Services Administrator application with the [Setting up the Share Connector Demo](#setting-up-the-share-connector-demo), however you must first update the endpoint in the Administrator application.

To update the Process Services endpoint:

1. Sign in to the Process Services app with the default admin/admin credentials:

    [http://127.0.0.1:8080/activiti-admin/](http://127.0.0.1:8080/activiti-admin/)

    A message appears indicating that an error occurred while getting data from the server.

2. Click **Edit Activiti REST endpoint** and set the **Username** to `admin` and **Password** to `password`, then click **Save**.

    A confirmation message appears confirming that the endpoints were successfully updated.

## Using the Share Connector demo

Follow these steps to start creating and running processes in Alfresco Share.

>**Note:** The LDAP demo server installed with the demo includes four fixed users. The password for each user is password. The following four users are set up so you can try out various groups and user scenarios.

* *jluc* is a tenant manager in Process Services, a user in Alfresco Content Services, and in the groups engineering and marketing.
* *kirk* is a tenant admin in Process Services, a user in Alfresco Content Services, and in the group engineering.
* *wesley* is a user in Process Services and a user in Alfresco Content Services. He is not a member of any group.
* *admin* is an admin in Process Services and an admin in Alfresco Content Services. This is the only user who has the ability to deploy process definitions from Process Services to Share.

1. Go to the installed Alfresco Share system at [http://localhost:8090/share](http://localhost:8090/share) and login with the following user credentials:

    *userid*: `admin`
    *password*: `password`

    Share Connector installs a demo LDAP system which provides several fixed userid/password pairs. The admin user Id provides permissions to start tasks and processes on Share, and to create and deploy processes and apps on the embedded Process Services. On your personal dashboard, click the **Tools** icon on the top-right and add the **My Activiti Tasks** dashlet.

    This dashlet is now displayed as well as the original My Tasks dashlet. Use the new dashlet to control processes and tasks inside Alfresco Share.

2. Go to [http://localhost:8080/activiti-app/](http://localhost:8080/activiti-app/), and log in with the userid `admin` and the password `password`.

    In the embedded app, you can create process definitions and deploy them to Alfresco Share.

### Start a workflow on a file

In your site’s document library in Alfresco Share, you can start a workflow on one or more files. The following steps
describe how to initiate a workflow using one of the pre-defined processes on two files.

**Prerequisite**: You must create your own site in Alfresco Share and have some files and folders added to it.

1. Find the file(s) you want to start the workflow on and click **Selected Items > Start Workflow** in the menu bar.

    The **Start Workflow** page appears.

2. Select the **Ad hoc Task** predefined process from the list of processes.

    The start form for the process is displayed.

    Note that the two files selected are already shown in the upload field of the form. When you start a workflow on a file or files, the selected content items are always associated with the first upload field in the process definition.

3. Fill in the start form, assigning the process to yourself, and click **Start Process**.

    The process is initiated, and the first task appears active.

You have successfully started an process on the selected files in an site.

### Start a workflow in Alfresco Share

This tutorial walks you through the steps required to run your first process as a workflow from Alfresco Share using the **My Activiti Tasks** dashlet.

All process definitions that you deploy to Apps in Process Services are available to you in Alfresco Share. This section assumes that you have deployed the first process workflow using the app-creating-process tutorial described in [Getting Started]({% link process-services/latest/using/getting-started.md %}). If not, follow the tutorial to deploy the workflow.

1. Go to the Alfresco Share dashboard, `http://localhost:8090/share`.

    You run a process as a workflow.

2. In your **My Workflow Tasks** dashlet, click **Start Workflow**.

    The Start Workflow dialog appears.

    Note that the alphabetical list of process definitions includes your first process.

3. Select your **First Process**.

    The workflow is initiated and the page now displays the form for the start task in this workflow, just like it does in Process Services.

4. Fill in the form.

    Note that when you click **Select a file** for the project files, a dialog to choose a file for Share appears to select files from the Alfresco Content Services repository.

5. Click **Start process** to start the workflow.

    The My Workflow page now displays the active and completed tasks in your workflow.

6. Click the **Review project** task.

    The My tasks page is displayed.

7. Add a review comment and click **Accept** to continue with the next step in the workflow, and continue until you have completed all tasks in the workflow.

You have run a process definition as a workflow in Share. My tasks, My workflows pages, and the associated Process Services for this Share site can all be accessed from the **Tasks** menu.

### Create rules

You can create rules to manage folders in a process. There are two ways to create rules in the Share Connector:

* **[Create your own rules]({% link content-services/latest/using/content/rules.md %})** for creating new set of rules for a folder
* **[Link to an existing rules set]({% link content-services/latest/using/content/rules.md %}#linking-to-an-existing-rule-set)** to reuse the existing set of rules defined for another folder

The options are listed under **Perform Actions**. Follow the steps until you reach the Process Services specific actions (under More Actions), and then continue as follows.

**To create rules for processes**:

1. Create a rule or link to an existing rules set.
2. From **New Rules > Perform Actions**, select **Start Activiti Process** to initiate a process from Process Services.
3. Click **Start Activiti Process**.
4. Customize the rule with the following options:
    * **Process Definition** - Select from the predefined process definitions based on where you want to apply the rule to.
    * **Process Name** - Enter a process name for your rule.
    * **Content form field** - Select content for attaching a content type field in the form.
    * **Additional form fields** - Select additional criteria for the rule such as Assignee, Due Date, Task Description, Message, and add their values. To select more than one criteria, click **+** (plus icon).
5. You can also select from the following **Other Options**:
    * **Disable rule** - Turns off any existing rules.
    * **Run applies to subfolders** - Applies the rule to this folder and all its subfolders.
    * **Run rule in the background** - Runs the rule in the background. You can also select an action to run if an error occurs with the rule. These actions are set up by your Administrator.
6. Click **Create** or **Create and Create Another** to save this rule and start creating another one.

The rule is applied to the selected folder and displayed on the **Rules** page. Once a rule is added, the following options become available:

* **Inherit Rules** - Use for applying rules to inherit from a parent folder. You can turn the rule on and off by clicking on it.
* **New Rule** - Click to add more rules to a folder as you need in the same way as you would add new rules.
* **Run Rules** - Click to manually run the rules on existing folder items or subfolders at any time.

## Integrate Process Services with Alfresco Content Services

When Process Services is integrated with an Alfresco Content Services server, the following types of communication are supported:

* Browse sites and their documents within the Process Services UI
* Publish documents to Alfresco Content Services
* Download documents from Alfresco Content Services
* Preview of downloaded document in the Process Services UI

This section provides details to achieve the integration between the two applications.

### Communication between Process Services and Alfresco Content Services

Process Services uses the CMIS REST bindings available in Alfresco Content Services and the *OpenCMIS* client library to communicate.

When connecting to Alfresco Content Services, it uses the `org.apache.chemistry.opencmis.client.runtime.SessionFactory.createSession(Map<String, String> parameters)` method.

Use the following parameters for user credentials:

```javascript
parameters.put(SessionParameter.USER, username);
parameters.put(SessionParameter.PASSWORD, password);
```

If a user account for the repository is already defined inside the Process Services Identity Management app, then the user name and password of that user account will be used.

However, if there is no user account defined and the repository configuration in the Identity Management app is configured to use the Share Connector, then Process Services will pass a secret key with the user name to Alfresco Content Services to create a ticket. The username is defined in the `EXTERNAL_ID` column of the `USERS` database table.

The secret key can be retrieved by calling a REST service (web script) in Alfresco Content Services, which was deployed when installing the Share Connector module in the repository, using the following HTTP call:

```bash
POST http://alfrescoserver.com/alfresco/service/activiti/sso/alfresco-ticket
{
    "secret": "activiti-share-connector-secret",
    "username": "kermit"
}
```

which will return 200 with the following response body:

```json
{
    "ticket": "abc123"
}
```

When Process Services receives this ticket, it will use the string `"ROLE_STRING"` (instead of using a "real" username) as the user parameter and the ticket as the password parameter:

```javascript
parameters.put(SessionParameter.USER, "ROLE_TICKET");
parameters.put(SessionParameter.PASSWORD, ticket);
```

In addition, Process Services uses the Public API (for example, when listing sites for a user) and regular HTTP calls with `basic auth`. For an existing user account, the user name and password are specified in the same way. However, if the Share Connector is configured for the repository, use the constant `ROLE_TICKET` as the user name and the ticket received from Alfresco Content Services as password with basic authentication.
---
title: Preconfigured workflows
---

Tasks and workflows help you keep track of the things you and other users need to do. You can create a standalone task or workflow, or you can attach a file to it.

A workflow is a process that controls a specific task, such as a document review. Each task can be assigned to one or more people when a workflow is being created. Workflow creators can select to automatically send a notification email to users that are assigned a task as part of the workflow, but whether an email is sent or not the task will be visible in the users My Tasks.

Once all the task actions required by a workflow have been finished, the workflow will move from active to completed status. At this point you’re free to delete the workflow.
Individual users manage their own tasks, and the person who created a workflow manages the workflow.

Starting from Process Services 24.1, six out-of-the box workflows provide a faster time to value for these frequently used simple workflows. The workflows are for assigning tasks, review, and approval:

* New Task
* New Task (group)
* Review and Approve (group review)
* Review and Approve (one or more reviewers)
* Review and Approve (pooled review)
* Review and Approve (single reviewer)

There are several stages to setting up a Preconfigured Workflows app before you can use it. To enable the Preconfigured workflows, ensure that the `app.review-workflows.enabled` property is set to `true` in the `activiti-app.properties` file. 


To get started:

1. Create a tenant.

      This is when you enable the **Preconfigured workflows** app.

2. Change the owner.

3. Configure a preconfigured workflow.

4. Create a user.

5. Create a group.

6. Start a workflow.

Once a workflow has been created, you can also:

* View workflows that you started.
* Cancel an active workflow.
* Delete a completed workflow.
* View tasks and workflows.
* Manage tasks.

## Creating a tenant

You need to create a tenant before you can start creating workflows. 

> **Note:**  Skip this step if you are using single tenant mode.

To create a tenant, complete the following steps.

1. Log in as admin to Alfresco Process Services as the admin user.

2. Select **Identity Management**.

3. Select **Tenants**.

4. Select **Create tenant**.

      The **Create tenant** dialog box appears.

5. Enter the following details as per your requirements.

      * Enter the **Name** – The name of your tenant, for example, tenant1.
      * Specify the **Maximum allowed users in this tenant** - This is set at `10` by default.

6. Select the **Deploy preconfigured workflows** checkbox.

7. Add the details about the workflow owner including **First name**, **Last name**, **Email**, and **Password**. 

      You can also assign a workflow owner from the list of created users.

8. Click **Save**.

## Changing the owner of preconfigured workflow

The workflow app needs to be manually deleted before changing the owner of preconfigured workflow.

To change the owner of a preconfigured workflow, complete the following steps.

1. Log in to Alfresco Process Services.

2. Select **Identity Management**.

3. Select **Tenants**.

4. Select **Edit Tenant**.

5. Select a user as the owner of the workflow in the current tenant.

      You can choose a new user or the existing user.

6. Click **Save**.

## Configuring a preconfigured workflow

All users in a tenant can access the preconfigured workflows. The owner of the tenant is the only user that can make edits to the workflow process.

To configure a preconfigured workflow, complete the following steps.

1. Log in to Alfresco Process Services.

2. Select **App Designer**.

3. Select the preconfigured workflow that you want to change.

4. Make the edits and save them.

      The edited changes are now visible to all the users of the tenant.

## Creating a user

To create a user in a tenant, complete the following steps.

1. Log in to Alfresco Process Services.

2. Select **Identity Management**.

3. Select **User**.

4. Select **Create user**.

      The **Create user** window appears.

5. Enter the following details.

      * **Email** of the user.
	  * **Password** of the user.
      *	**First name** of the user.
      * **Last name** of the user.
	  * Select your **Tenant** from the drop-down list.
	  * Enter the **Company** name.
      * Select the **Status** and **Type**.

6. Click **Save**.

## Creating a group

To create a group in a tenant, complete the following steps.

1. Log in to Alfresco Process Services.

2. Select **Identity Management**.

3. Select **Organization**.

4. Select your tenant from the drop-down list.
 
      A workflow group will be visible by default. You can add other users to this group so they can have access to view the workflow.

5. Select **Create group**. Name your group and click **Save**.

6. Click **+ add users** to add users to your group.

## Starting a workflow

You can attach a workflow directly to one or more files. Starting a workflow generates a workflow task such as a review.

1. Log in to Alfresco Process Services.

2. Select **Task App**.

3. Click on the **+Start** button.

      The Start Workflow page opens.

4. Select a workflow from the Workflow list.

      The following preconfigured workflows are available:

	  * New Task: Assign a new task to yourself or another user.
	  * New Task (group): Assign a new task to a group.
	  * Review and Approve (group review): Set up review and approval of content, assigning the workflow task to a single group.
	  * Review and Approve (one or more reviewers): Request file approval from one or more users.
	  * Review and Approve (pooled review): Set up review and approval of content, assigning the workflow task to multiple users. One user can take ownership of the task at a   time, completing it or returning it to the pool to be claimed by another user associated with the task.
	  * Review and Approve (single reviewer): Set up review and approval of content, assigning the workflow task to a single user.

      The appropriate workflow form displays where you enter the details of the workflow task being initiated. Required fields are marked with an asterisk (*).

5. Enter details for the workflow in the General section.

      * In the **Message** field describe the task requirements, such as Please review the attached content. This should clearly explain to the user what they are expected to do. This text displays in My Tasks for the workflow task.
	  * Select a **Priority** setting for the task.
        > **Note:**  By default, the priority is set to **Medium**.
	  * Select a **Due** date for the task.

6. Select the user(s) or group to assign the task generated by the workflow to.

      You assign the task to either a user or a user group depending on the type of workflow selected.

	  * In the **Reviewers** section click **Select** and type the full or partial name of a user.
	  * Click the user that you want to add.
        > **Note:** You can select multiple users for the Send Document(s) For Review task.
      * Click **OK**.
	  * If your task is assigned to more than one person, complete the **Required Approval Percentage** field. Enter the percentage of reviewers that must approve the task before it can be marked as complete.

7. Select a file under **Items**, if required.

## Viewing workflows you started

You can view the full details of all workflows that you have started.

1. Click **Tasks** then **Workflows I've Started**.

    The Workflows I've Started page displays the workflows you have created. You can use the filters in the browsing pane to view a specific set of workflows.

2. Hover over the workflow you want to view and click **View History**.

    > **Note:** You can also click the workflow title.

    The Details page displays all information related to this workflow.

    * Click **View Current Tasks** at the top of the page to jump to the Current Tasks section which displays the tasks generated from the selected workflow. From here you can view ![view task]({% link content-services/images/ico-view-task.png %}) or edit ![configure]({% link content-services/images/ico-configure.png %}) a task.
    * Click the link in the Most Recently Completed Task section to view details on the last task completed as part of this workflow. This task also appears in the History section.
    * Look at completed tasks in the History section. Click a task to view its details.
    * Click an item in the Items list to see it in the file preview screen. Click your browser’s Back button to return to the Workflow Details page.
    * If you started the workflow you can click to **Cancel Workflow** to cancel an active workflow **Delete Workflow** to delete a completed workflow.

3. Click **Workflows I’ve Started** to return to the workflow list.

## Cancelling an active workflow

You can cancel an active workflow if you find you don’t need it anymore. This deletes all tasks related to the workflow.

1. On the **Workflows I’ve Started** page, make sure you’ve selected the Active view in the explorer pane.

2. Hover over the workflow you want to cancel and click **Cancel Workflow**.

      A message prompts you to confirm the action.

3. Click **Yes**.

      The selected workflow is cancelled and removed from the workflow list. All tasks related to the workflow are deleted, which removes them from the Active view on the My Tasks page. They are also removed from **My Tasks**.

## Deleting a completed workflow

Once you’re finished with a workflow, you can delete it to clear it from the workflow list. This also deletes all tasks associated with the workflow.

1. On the **Workflows I’ve Started** page, select the Completed view in the explorer pane.

2. Hover over a workflow and click **Delete Workflow**.

      A message prompts you to confirm the deletion.

3. Click **Yes**.

      The workflow is deleted and removed from the workflow list. The tasks related to the workflow are deleted, which removes them from the Completed view on the My Tasks page. They are also removed from My Tasks.

## Viewing tasks and workflows

You can view the details for an individual task or for the workflow that initiated a task.

1. Click **Tasks** then **Workflows I've Started**.

    > **Note:** You can also view and edit tasks from My Tasks.

2. On the My Tasks page, hover over a task and click an action:

    * **View Task**: Displays the task details
    * **View Workflow**: Displays the workflow details

    > **Note:** An icon (![pooled]({% link content-services/images/im-pooled.png %})) indicates a pooled task. Pooled tasks that can be claimed are marked as **Unassigned**.

3. Click the **Task Details** and **Workflow Details** options to move between the two page views.

    The Task Details page displays all information related to this task.

    * In the Items list, click an item to preview it in the library. Click your browser’s Back button to return to the Task Details page.
    * Click **Edit** to edit the task.

    The Workflow Details page displays the information for the workflow that generated this task.

    * Click **View Process Diagram** to display a graphical representation of the workflow. A red border highlights the current stage of the workflow. Click anywhere on the graphic to close it.
    * Click **View Current Tasks** at the top of the page to jump to the Current Tasks section which displays the tasks generated from the selected workflow. From here you can view ![view task]({% link content-services/images/ico-view-task.png %}) or edit ![configure]({% link content-services/images/ico-configure.png %}) a task.
    * Click the link in the Most Recently Completed Task section to view details on the last task completed as part of this workflow. This task also appears in the History section.
    * Look at completed tasks in the History section. Click a task to view it's details.
    * Click an item in the Items list to see it in the file preview screen. Click your browser’s Back button to return to the Workflow Details page.
    * If you started the workflow you can click to **Cancel Workflow** to cancel an active workflow.

## Managing tasks

Tasks assigned to you appear in two places: the My Tasks personal and the My Tasks page. Each task stays assigned to you until you complete or reassign it.

1. Click **Tasks** then **My Tasks**.

2. Hover over a task and click **Edit Task**.

    The Edit Task page appears displaying the task details. The actions available on this page depend on the task type.

    > **Note:** You can also access this page from My Tasks: click the **Edit Task** icon.

3. Manage the selected task in one or more of the following ways:

    * **Update**: If the task is in progress but not yet complete, you can change the task status and add a comment indicating your progress. Remember to click **Save and Close**. The task stays assigned to you.
    * **Reassign**: Click **Reassign** and use the search field provided to find a user. Click **Select** to the right of a user to reassign the task to that person.
    * **Approve or Reject**: When you're done with a task you can update the task status, add a comment indicating the work done, and then click either **Approve** or **Reject**. The task returns to the user who started the workflow and no longer appears in your task list.
    * **Claim**: Click **Claim** to take responsibility for a pooled task. This action is available only for pooled tasks that are unassigned.
    * **Release to Pool**: Click **Release to Pool** to place a task back in the pool. The task will appear in the task list as *Unassigned* and can be claimed by another user. This action is available only for pooled tasks that are currently owned by you.
    * **Add**: Click **Add** beneath the file list to locate and select files to add to the task. This action is available only for Adhoc tasks.
    * **Task Done**: When you complete a task it returns to the user who started the associated workflow. Click **Task Done** to finish a task. This removes it from your task list.

    When the selected action is complete you are redirected to an appropriate screen.
---
title: Using the App Designer
---

Use the App Designer to create process models, forms, app definitions, and share your models and definitions with others. As you create items, they appear as tiles on their respective page. The Last Modified drop-down on the top-right enables you to sort the display order ranging from last modified, oldest first, name order, or reverse name order. Use the filter on the left to filter the list of displayed items. Additionally, if you are unable to find a specific process, use the search box to find more processes. If your processes require human input, then you will need forms to gather it.

![Kickstart App]({% link process-services/images/app-kickstart.png %})

You can filter the list of Business Process Models using the following options on the left:

* **My items** - View all your processes / app definitions / data models / stencils / reusable forms / reusable decision tables. The filter name changes based on the tab you are in. For example, in case of the Forms tab, it changes to My reusable forms and to My App definitions when you are in the Apps tab.
* **Shared with Me** - View items shared by others with you.
* **Shared with Others** - View items that you have shared with others.
* **Favorited** - View your favorite items.
* **Everyone’s** - View all processes regardless of who created them.

>**Note:** The **Everyone’s** filter is applicable for admin purposes only. You can’t use this option to allow others to reuse the model. To allow someone else to use this model, it has to be shared first.

The App Designer panel includes the following tabs:

* **Processes** - Provide tools for creating new processes, modifying existing processes, and importing processes from outside Process Services. If your account has the capability, you can also import existing models that are defined in BPMN 2.0 standard format.

>**Note:** If you haven’t created any processes yet, then you will see shortcuts for creating a process. You can use the simple [Step editor]({% link process-services/latest/using/process/step.md %}), or the more powerful [BPMN editor]({% link process-services/latest/using/process/bpmn.md %}). If you are not familiar with the BPMN 2.0 Business Process Model language, then the Step Editor is for you. However, if you’d like to create complex processes, then the BPMN Editor will let you use the full power of the language. It’s helpful if you’re familiar with BPMN 2.0 for using the BPMN Editor.

* **Forms** - Provide tools for creating new forms, and modifying existing forms. Filter the list of displayed forms using the options on the left. You can view all your forms, or just those shared by others with you, or those you have shared with others, or just those you have favorited. If you haven’t created any forms yet, then a new button called Create a new form now! will appear on the **Forms** tab.

* **Decision Tables** - List decision tables that can be used across processes. Decision tables are an easy way to define business rules.

* **Apps** - Create new apps, modify existing apps, and import apps from outside Process Services. You create an app to group one or more of your processes, so you manipulate them as one unit. You can make an app available for yourself and share it with others. An app can contain no process at all, which allows you to create simple task list.

* **Data Models** - Enable you to map your business data with a relational database or a custom API such as a customer database, patient database, and so on. You can create business objects to connect to an external database that can be accessed by all processes in your application.

* **Stencils** - A stencil is a palette consisting of both standard and customized controls that are common to the Step editor, BPMN editor, and Forms editor. When you create a process or a form, you can specify a specific stencil or use the default for the editor you are using.

    >**Note:** When editing a form in the form editor, you can change the existing stencil assigned to the form.

    1. Click the Form Stencils drop-down list in the upper right corner of the screen.
    2. Select a stencil from the list.
    3. The new stencil is assigned to the form and its controls appear in the form palette.

    >**Note:** When you change stencils and a field existing in the form canvas is not available in the new stencil, a validation error is displayed. To resolve this issue, remove the field from the form canvas.

## App Designer editor

Open the App Designer editor by clicking a process definition, reusable form, reusable decision table, app definition,
data models, or the stencils tab. The App Designer editor provides features such as copy, comment, delete, add to favorites, share with others, and export. You can also open the corresponding editor to make changes to the content, and perform actions specific to the item type. For example, you can publish an app definition or edit a process.

![Kickstart App Editor]({% link process-services/images/app-kickstart-editor-1.png %})

In the above example, the App Designer editor was opened for an app definition called publisher. The editor always displays the details of the selected item on the top panel along with a set of buttons on the top right. The right-most button opens the editor corresponding to the item displayed. So in the example, the right-most button opens the app editor. If a process definition created via the step editor is opened in the App Designer editor, then the App Editor would open the step editor.

> **Note:** An asterisk (*) appears before the page title in your browser when there are unsaved processes in your **My Processes** list.

## Create your first process

In Process Services, you create a process models to represent a series of tasks in your business process. This tutorial guides you through creating a simple process model.

The process you are modeling here is a simplified business project lifecycle. Each project has a name, type, due date, and documents associated with it. Each project is started, and then reviewed to determine if it should be accepted on to the project list, or rejected.

1. From your landing page, click the **App Designer** app tile.

2. Click the **Create Process** Button.

    The Create a new business process model dialog appears.

3. Give your new process model a name.

    For example, **First Process**.

4. In the Editor type drop-down, select the Step editor.

5. Click **Create new model**.

    The Step editor is displayed.

    The first step, Process start, is already added to your process. You are going to set the process to start by having the user complete a form.

6. Click on the Process start step.

    It expands to allow you to change the step.

    If you have some forms in your Forms library, they will be listed here, and you can pick one, but in this tutorial we will create a new form.

7. Click on the Start form box.

8. Click **Create form**.

    The Create a new form dialog appears. The form you create now is part of this process model and is not available in your forms library for use in other process models. If you want to create a form you can reuse in other process models you can do so from the Forms page.

9. Give the new form a name.

    For example, `Start form`.

10. Click **Create new form**.

    The Form Editor is displayed. Design the form by dragging and dropping the field types from the palette to the Form Editor. You can hover over each field in the Design area, and click the pencil icon to edit the field properties, or to remove the field from the form. Each field type offers different options. You can also add a display label in the process to reference a value entered in a field by a user in a running process. You can also define if the field is mandatory for the form to be completed. In this tutorial, you just give labels to the fields.

11. Drag and drop the required fields from the palette to the canvas on the right-hand side.

    From the screen shot you can see your form has four fields.

    1. A Text field for the project name.
    2. A Date field for the project’s start date.
    3. A group of three Radio buttons to select the project type.
    4. An Attach control to allow the user to store project documents.

12. Click the **Save** icon to save your form.

    You are back in the Step editor.

13. Clicking the + icon below the Process start box to add the first step in your process.

    You need to add a Human step that can be used to assign a task to a user.

14. Select the Human step and fill in a name in the step box just created.

    For this tutorial, use the name `Review project`.

    The Human step allows you to select who the task should be assigned to. You can assign the person who initiated the process, a single named user, a set of candidate users, or depending on the type of your account, a group of users. When a task is assigned to a group or a list of candidate users, all of those users can see the task in their task list, and will need to claim it in order to complete the task. For this tutorial, you will assign all tasks to the process initiator, that’s you, so you can run the process and see the tasks yourself.

15. You need to create a form to allow review comments before we create the next step in the process.
    1. On the Form tab for the Review project step, create a new form called `decide`.
    2. Add a Multiline text field and name it **Review comment**.
    3. Select the Outcomes tab and choose the Use custom outcomes for this form option, and add two outcomes: Accept and Reject.
    4. Save the form, and return to the step editor.

16. Add a Choice step by clicking the + icon below the Review Project step.

    This step allows you to take a different action depending on the outcome selected in the associated form.

    You can add more choices by clicking on the + icon in the middle of the Choice step. For this tutorial, we only need two based on your accept and reject outcomes.

17. Click on the First choice box. A dialog allows you to select a condition based on existing form fields or outcomes. For this tutorial, set the First choice to a Form outcome. Choose the `decide` form from the drop-down list of those already added to the process, and then select it to be Equals, to the value Accept.

18. Click on the Second choice box, and repeat the last step, this time choosing the value Reject.

19. You need to add a task to be done if a project review is accepted.
    1. Under the First choice click the + icon.
    2. Add a Human step with the name `Update project list`.

20. You need to add a task to be done if a project review is rejected.
    1. Under the Second choice click the + icon.
    2. Add a Human step with the name `Inform project leader of rejection`.
    3. Since the process should stop after rejection, add an End process step under the `Inform project leader of rejection` step.

21. Add a final step after the accept/reject choice step to display the project details by clicking the + icon at the bottom of the step diagram.
    1. Add a Human step with the name `Show Project Details`.
    2. On the Form tab for this step, create a new form. Drag a Display text field to the canvas, and enter a text message to display.

        The text can contain references to values for forms in the process. In addition, there is a helper drop-down list from which a form field reference can be selected. It is inserted at the current cursor position in the text.

    3. Save the form.

        The step editor is displayed.

22. Save your completed process model.

    Your process is listed in the Process tab as a thumbnail of the process. You can edit any process from the list by clicking the BPMN Editor button in the top right corner of the thumbnail. You can see additional information about a model by clicking on the thumbnail itself or the Show Details button in the top right corner of the thumbnail. This takes you to the Details page for the process model. Here, you can see a read-only preview of the model and the actions you can perform on it.

Now that you have created a process, you need to create your first app so you can publish and deploy your process model.

## Create your first app

You create a Process App to group together a number of process definitions so they are available to yourself or other users. A Process App is a container for handling a group of published processes and deploying them to a Process Engine.

This tutorial leads you through the steps required to create and use an app containing a single process definition.

1. Go to **App Designer > Apps** tab, and click **Create App**.

    The Create a new app definition dialog appears.

2. Enter a name for your app and click **Create a new app definition**.

    Use the name **My First App** for this tutorial.

3. Choose an icon and theme for your new app tile.

4. Click **Edit included models** and select a process(s) of your choice. In this case, select the published model from the [create your first process](#create-your-first-process) section.

5. Click **Save**, and select the **Publish** check box in the Save app definition dialog to save and publish your app.

    Publishing an app makes it available to everyone you’ve shared it with.

6. You can now add the app as a tile on your landing page.
    1. On the landing page, click on the last tile labeled with a + (plus) icon. The Add app to landing page dialog appears.
    2. Select **My First App** from the list of published apps and click **Deploy**.

        A new app tile is added to your Landing page.

Your app is now deployed and ready to be used.

## Start your first process

You start a process from the **Processes** tab of the **Task app** page. In this section, you are going to start and monitor the process you designed in the previous section. To start the process, first add a process to an app and deploy that app.

The following steps use the process model created in the [create your first process](#create-your-first-process) section, and the corresponding app created and deployed in the [create your first app](#create-your-first-app) section.

1. Go to the **Task App > Processes** tab, and click **Start**. button

    The form you created in the "Creating your first process" section is displayed. . Fill in the details on the form, and add any documents you need, and click **START PROCESS**.

    You are returned to the **Processes** page, which displays the process list with the process that you just started.

    On the **Processes** page, you can view running processes and see the current and completed tasks. You can also add comments that are available for anyone involved in the process.

2. Now that you have started the process, you should complete the tasks you defined in it. Go to the **Tasks** tab.

    The first step in the process is a task to review the project, and accept or reject it. Remember that when you created the first step in Step Editor, you specified that the task should be assigned to the process initiator. Since you started the process, you are the process initiator and this task is assigned to you.

3. Click **Show Details** or **Show Form**.

    At this stage you can add people, documents, and comments to the task.

4. Click **Show Form** to return to the form and then **Accept**.

    The Review Project task is complete and a new task, Update Project List is displayed. You defined this as a choice step in Step Editor, if the user choice was to accept the project.

5. Click **Complete** to go to the next step.

    The task that shows the details of the accepted project is displayed.

6. Click **Complete**.

    You have now completed all the tasks in the process and there are no tasks displayed for you in the Tasks tab. Now, if you click on the Processes tab, you’ll not see any running processes.

You have started your first process, performed the tasks assigned to you in that process, and completed a process successfully.

## Create a single task

As you have seen from previous sections, processes are made up of individual tasks. You can also create a single task 
for yourself or others and assign it for completion. This section guides you through the steps for creating and completing a single task.

In this example you will add a single task `Brush teeth` and complete the task yourself.

1. On the **Tasks** tab of the Task app page click the **CREATE TASK** button

    The **New task** dialog appears.

2. Give your new task a name, and optionally a description, and click **Create**.

    Your new task appears in the task list, and the task details are displayed in the right-hand panel.

    Now you have created a task you can alter the details such as the assignee and the Due date, involve others in the task, add a document and add comments to be shared with other collaborators in the task. For this simple task of `Brushing teeth`, you are just going to add a due date of `today`. . Click **Due date**.

    A date chooser drops down.

3. Click **Due today**.

    The Due date now has a timer displayed showing the number of hours before the end of the day. Many fields displayed in Process Services can accept user input when you click on them. The Assignee field the task is another example.

4. When you’ve brushed your teeth, click **Complete** in the task details area.

    The task is removed from the open task list.

5. By default, your task list displays only open tasks. That is why you no longer see the task you just completed. For completed tasks click the **COMPLETED TASKS** filter in the right-most column of the Tasks tab.

You have created and completed your first single task and used some of the filtering capabilities of the Task app.
---
title: Using the BPMN Editor 
---

With the BPMN editor you can create process definitions using the capabilities of BPMN 2.0. You build your process by dragging and dropping from a palette of grouped components to a canvas on which your process diagram is built.

![BPMN Editor]({% link process-services/images/app-bpmn-editor-1.png %})

The BPMN editor is structured into several areas:

* **Palette**

    On the left side of BPMN editor is the palette, which consists of collapse-able groups of BPMN objects.

* **Canvas**

    On the right side of BPMN editor is the canvas, where the BPMN objects can be added to create a process model.

* **Properties sheet**

    Below the canvas is the properties sheet, which shows the properties of the selected BPMN object on the canvas, or if no BPMN object is selected, the properties of the process itself. You can click on any of the properties to modify its value. The property sheet is collapse-able to allow you more screen space to view your process diagram.

* **Toolbar**

    The toolbar is displayed on the top with a set of grouped command icons. You can save and validate your model, delete selected elements in the diagram, cut, copy and paste selected elements, undo and redo the last action, zoom the process diagram, eliminate crossing connector lines by adding and removing bend-points, view the BPMN editor tour, and provide feedback to the Process Services team.

    When you first use the BPMN editor, a short guided tour runs showing you the components of the editor and running through the initial steps involved in creating a process definition. You can rerun the tour at any time by clicking the icon in the toolbar.

When you open the BPMN editor to create a new process definition, the canvas already contains a Start Event. Clicking on any event on the canvas frames the event icon with a dotted line and reveals a number of controls.

The controls below the icon allow you to delete the BPMN object, or change in to another object in the same group. For example, you can change a Start event to a Start timer event. The controls to the right of the icon allow you to specify the next object type in the process. The list presented includes only those object types that are valid in the sequence after the current object. In addition, there are controls that allow you to create flows connecting other existing events in your diagrams, and to annotate the event.

There are two ways of adding BPMN objects to your process:

* Use the controls that appear when you click on a current object icon. Using this method will create a valid connector between the current event icon and the new event icon.

* Drag and drop an object icon from the palette. In this case you add flows to the current event icons in the process yourself by picking the icons from the palette.

The following object groups are shown in a collapsible list in the palette. The groups consist of all the objects available in the BPMN 2.0 specification, and additional Process Services extensions such as the Publish to Alfresco task, Publish to Box, Publish to Google Drive.

## Start events

A start event indicates where a process starts. You can define a start event in one of the following ways:

* [Start on no specific trigger](#none-start-event)
* [Start at specific time intervals](#start-timer-event)
* [Start when a specific signal is raised](#start-signal-event)
* [Start on the arrival of a message](#start-message-event)
* [Start as a result of an error](#start-error-event)

In the XML representation, the type start event is specified as a sub-element.

Start events are always catching: a start event waits until a specific trigger occurs.

### None start event

A start event with an unspecified trigger. BPMN 2.0 refers to this as a none start event. It is visualized as a circle with no icon.

![bpmn.none-start-event]({% link process-services/images/bpmn.none-start-event.png %})

A none start event can have a *start form*. If so, the start form will be displayed when selecting the process definition from the *processes* list. Note that a process instance is not started until the start form is submitted. A none start event without a form will simply have a button displayed to start the process instance.

>**Note:** A subprocess always has a none start event.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Execution listeners|Execution listeners configured for this element instance. An execution listener is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Process Initiator|The process variable in which the user ID of the initiator of this instance should be stored.|
|Form key|A key that provides a reference to a form. This property is available for compatibility with Activiti, but should not be used directly when using Forms. Use the `Referenced form` property instead.|
|Referenced form|A form reference.|
|Form properties|A form definition with a list of form properties. Form properties are the way forms are defined in the community version of Process Services. Configuring them has no impact on the rendered form in the Process Services, the `Referenced form` property should be used instead.|

### Start timer event

A timer start event initiates a process instance at specific time. You can use it both for processes which must start only once and for processes that must start in repeated time intervals.

It is visualized as a circle with a clock icon.

![bpmn.timer-start-event]({% link process-services/images/bpmn.timer-start-event.png %})

Note that a process instance started by a timer start event can’t have a start form, as it is started by the system. Similarly, it does not have a process initiator like a *none start event*. As such when assigning tasks later on in the process definition, keep in mind that the assignment *'assigned to process initiator'* will not work.

>**Note:** A subprocess can’t have a timer start event.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this instance.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Time Cycle|A timer cycle defined in [ISO 8601](http://en.wikipedia.org/wiki/ISO_8601){:target="_blank"} format, for example: `R3/PT10H`.|
|Time Date in ISO-8601|A point in time defined as an [ISO 8601](http://en.wikipedia.org/wiki/ISO_8601){:target="_blank"} date, for example: `2015-04-12T20:20:32Z`.|
|Time Duration|A period of time defined as an [ISO 8601](http://en.wikipedia.org/wiki/ISO_8601){:target="_blank"} duration, for example: `PT5M`.|

### Start signal event

A signal start event starts a process instance using a named signal. The signal is fired from a process instance using the intermediary signal throw event (or programmatically through the java or REST API). In both cases, a process instance for any process definitions that have a signal start event with the same name are started. You can select a synchronous or asynchronous start of the process instances.

A signal start event is visualized as a circle with a triangle inside. The triangle is white inside.

![bpmn.signal-start-event]({% link process-services/images/bpmn.signal-start-event.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Signal reference|The name of the signal that initiates this event. Note that signal references are configured on the root level of the process instance and then linked to the signal start event via this property. To configure it, deselect any other element and click the **Signal definitions** property.|

### Start message event

A message start event starts a process instance using a named message. It is mainly used for starting process instances from external systems.

It is depicted as a circle with an envelope icon inside. The envelope is white inside.

![bpmn.message-start-event]({% link process-services/images/bpmn.message-start-event.png %})

When you deploy a process definition with one or more message start events, consider the following points:

* The name of the message start event must be unique across the whole process definition. Process Services will throw an exception on deployment of a process definition with two or more message start events that reference the same message or with two or more message start events that reference messages with the same name.
* The name of the message start event must be unique across all deployed process definitions. Process Services will throw an exception on deployment of a process definition with one or more message start events that reference a message with the same name as a message start event already deployed in a different process definition.
* When a new version of a process definition is deployed, the message subscriptions of the previous version are canceled. This is also true for message events that are not present in the new version.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Execution listeners|Execution listeners configured for this instance. An execution listener is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Message reference|The name of the message that initiates this event. Note that messages are configured on the root level of the process instance and then linked to the message start event via this property. To configure it, deselect any other element and click the **Message definitions** property.|

### Start error event

An error start event triggers an event Sub-Process. An error start event can’t be used for starting a process instance.

It is visualized as a circle with lightning icon inside. The icon is white inside.

![bpmn.error-start-event]({% link process-services/images/bpmn.error-start-event.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Error reference|The name of the error that initiates this event. This reference needs to match the error identifier thrown by the event that throws the particular error.|

## Activities

An activity describes a single item of work to be performed in a process. Process Services provides some Activity types that are additional to those described in the BPMN 2.0 specification.

The types of activities are:

* [User task](#user-task)
* [Service task](#service-task)
* [Script task](#script-task)
* [Business rule task](#business-rule-task)
* [Receive task](#receive-task)
* [Manual task](#manual-task)
* [Mail task](#mail-task)
* [Camel task](#camel-task)
* [Mule task](#mule-task)
* [REST call task](#rest-call-task)
* [Generate document task](#generate-document-task)
* [Decision task](#decision-task)
* [Store entity task](#store-entity-task)

An activity is always visualized as a rectangle with rounded corners.

### User task

A user task enables you to model work to be done by a human actor. When process execution arrives at a user task in
the process definition, it creates a new task in the task list of the assignee or assignees defined in the task.

A user task is depicted as a rounded rectangle with a user icon on the top-left corner.

![bpmn.user-task]({% link process-services/images/bpmn.user-task.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Assignment|Configures to who this task should be assigned. It is possible to use **Fixed Values** (advanced usage: these are Process Services expressions, for example by invoking a class or Spring bean) or use the **Identity Store** option. It is recommended to use **Identity Store** to select groups and users in the system:<br><br>**Assigned to process initiator**<br><br>The user that started the process instance will be the assignee of this task.<br><br>**Assigned to process initiator’s (primary) group manager**<br><br>The group manager of the user that started the process instance will be the assignee of this task.<br><br>**Assigned to single user**<br><br>A single user who will be the assignee of the task. This user will see the task in their **Involved tasks** task list. It is possible to reference a user that was selected in a previous form field (tab **Form field**).<br><br>**Assigned to group manager**<br><br>The group manager of the user will be the assignee of the task. Only users that have a primary group defined will have a group manager. To define a primary group, go to **Identity Management** > **Users** > **Select an action** > **Change primary group**.<br><br>**Candidate users**<br><br>One or more users as the **candidate(s)** of the group. The task will show up in their **Queued tasks** task list. The task is not yet assigned to them. They first have to **claim** the task, which will make that one user the assignee. The other users won’t see that task in a task list anymore. It is possible to reference users that were selected in a previous form field (tab **Form field**).<br><br>**Candidate groups**<br><br>One or more groups whose members will be the **candidate** of the group. The task will show up in their **Queued tasks** task list. The task is not yet assigned to them. They first have to **claim** the task, which will make that one user the assignee. The other users won’t see that task in a task list anymore. It is possible to reference groups that were selected in a previous form field (tab **Form field**).<br><br>**Allow process initiator to complete task**<br><br>When checked, the user that started the process instance (process initiator) can complete the task. This is checked by default. <br><br>**Deactivate user task re-assignment**<br><br> When checked a modeler can deactivate re-assignment to an end user outside the specified list of candidate users/groups. This means that the assignment and subsequent re-assignment of the task would be limited to only the provided list of users/groups, and not to anyone outside this list. If task assignment is based on a single user and the checkbox is checked then only that user will be able to perform the task. The option is selected by default. |
|Referenced form|Allows to configure or create the form for this task. This form (also called _task form) will be rendered when the task is shown in the task list of the user. A user task typically always has a form defined.|
|Form key|This is a property that exists for compatibility with the community version. When working with task lists and forms, do not set this property.|
|Form properties|This is a property that exists for compatibility with Process Services community. When using Process Services to work with task lists and forms, do not set this property.|
|Due date|Allows to configure a due date for the task. In the task list, tasks can be sorted by due date to see which tasks are needed to be completed the soonest. The possible ways of configuring are:<br><br>**No due date**<br><br>This is the default value.<br><br>**Expression definition (Advanced)**<br><br>Uses an Process Services expression to resolve the due date (for example, this expression could call a Spring bean).<br><br>**Fixed duration after task creation**<br><br>Allows to configure an amount of time, starting from the creation of the task.<br><br>**Based on field**<br><br>Allows to configure the due date based on a previous field in the process instance, by adding or subtracting a certain amount of time.<br><br>**Based on variable**<br><br>Allows to configure the due date based on a variable previously declared in the process instance, by adding or subtracting a certain amount of time.|
|Allow email notifications|When enabled, an email will be sent to the assignee when the task is assigned to them.|
|Email template|The template of the email to use when **Allow email notifications** is enabled. A custom email template can be selected from a list available to the tenant, or a new custom template created for the application. See [custom templates]({% link process-services/latest/using/process/index.md %}#custom-email-templates) for instructions on creating a template.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be created as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listener lets you execute Java code or evaluate an expression when an event occurs during process execution.|
|Multi-Instance type|Determines if this task is performed multiple times and how. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.<br><br>|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|(Used with Multi-Instance type) The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|
|Is for compensation|If this activity is used for compensating the effects of another activity, you can declare it to be a compensation handler. For more information on compensation handlers see the Developer Guide.|

### Service task

Use a service task to invoke an external Java class or execute an expression (for example to call a Spring bean).

A service task is visualized as a rounded rectangle with a cog icon inside.

![bpmn.service-task]({% link process-services/images/bpmn.service-task.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element instance.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Class|The name of the Java class that implements your service task. Your class must implement `JavaDelegate` or `ActivityBehavior`. For more information on methods of invoking Java logic from a service task see the Developer Guide|
|Expression|An expression that either executes logic in the expression itself (for example `${execution.setVariable(myVar, someValue)}`) or calls a method on a bean known by the Activiti engine (for example `${someBean.callMethod}`). You can pass parameters (like the current `execution`) to the method in the expression. For more information on methods of invoking Java logic from a service task see the Developer Guide.|
|Delegate expression||
|Class fields|Field extensions for the service task.|
|Result variable name|The name of a process variable in your process definition in which to store the result of this service task. This is only valid when using an `expression`.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. For more information on multi-instance, see the Developer documentation. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|
|Is for compensation|If this activity is used for compensating the effects of another activity, you can declare it to be a compensation handler. For more information on compensation handlers see the Developer Guide.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|

For a service task it is recommended to make them asynchronous. For example, suppose a service task is called after the user completes a form. When the service task is synchronous, the logic will be executed during the completion action of the user. This means the user has to wait until this logic is finished to have the UI refreshed. Often, this is not needed or wanted. By making the service task asynchronous, the UI will be refreshed when the task is completed. The logic will be executed later.

### Script task

A script task defines a JavaScript script or other script language (JSR-223 compatible language) that is executed when a process instance executes this step.

A script task is visualized as a rounded rectangle with a paper icon inside.

![bpmn.script-task]({% link process-services/images/bpmn.script-task.png %})

|Property|Description|
|--------|-----------|
|Script format|The [JSR-223](http://jcp.org/en/jsr/detail?id=223) name of the scripting engine your script is written for. By default, Process Services supports **javascript** and **groovy** formats.|
|Script|The actual script that will be executed.|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Variables|In the script, it is possible to set new process variables (using `execution.setVariable(myVariable, myValue)`), however these won’t show up automatically in dropdowns later on (like the sequence flow condition builder, forms, etc.). To make them show up, configure this property with the variables that are set or exported by this script task.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Multi-Instance type|Determines if this task is performed multiple times and how. For more information on multi-instance, The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|
|Is for compensation|If this activity is used for compensating the effects of another activity, you can declare it to be a compensation handler. For more information on compensation handlers see the Developer Guide.|

### Business rule task

A Business rule task executes one or more rules.

Business rule tasks are mainly there for compatibility with the community product Activiti. Alfresco recommends that you use [Decision tables]({% link process-services/latest/using/process/rules.md %}) with Process Services

A business rule is depicted as a rounded rectangle with a table icon in the top-left corner.

![bpmn.business-rule-task]({% link process-services/images/bpmn.business-rule-task.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Rules|A comma-separated list of rules to include or exclude in this task.|
|Input variables|A comma-separated list of process variables to be used as input variables to your rules.|
|Exclude|If you check Exclude only rules that you have not specified in Rules will be executed. If the Exclude is unchecked, only the rules you have specified in Rules will be executed.|
|Result variable|The name of a process variable in your process definition in which to store the result of this task. the result variable is returned as a list of objects. If you do not specify a result variable name, the default name `org.activiti.engine.rules.OUTPUT` is used.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. For more information on multi-instance, see the Developer Guide. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|
|Is for compensation|If this activity is used for compensating the effects of another activity, you can declare it to be a compensation handler. For more information on compensation handlers see the Developer Guide.|

### Receive task

A Receive Task waits for the arrival of an external trigger. This trigger is sent programmatically (via Java or REST API). For process to process triggering, use the signal events.

A receive task is visualized as a rounded rectangle with an envelope icon in the top-left corner.

![bpmn.receive-task]({% link process-services/images/bpmn.receive-task.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Variables|When the API is used to trigger the continuation of the process instance, a set of variables can be passed. However, these won’t appear automatically in drop-down lists later (like the sequence flow condition builder, forms, and so on.). To make them appear, this property needs to be configured with those variables that are set or exported by the script task.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. For more information on multi-instance, see the Developer Guide. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|
|Is for compensation|If this activity is used for compensating the effects of another activity, you can declare it to be a compensation handler. For more information on compensation handlers see the Developer Guide.|

### Manual task

A Manual Task defines a task that is external to Process Services. You use it to model work done which the Process Engine does not know of. A manual task is handled as a pass-through activity, the Process Engine automatically continues the process from the instant process execution arrives at a manual task activity.

![bpmn.manual-task]({% link process-services/images/bpmn.manual-task.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|
|Is for compensation|If this activity is used for compensating the effects of another activity, you can declare it to be a compensation handler. For more information on compensation handlers see the Developer Guide.|

### Mail task

You can enhance your business process with this automatic mail service task that sends emails to one or more recipients. The task supports normal email features such as cc lists, bcc lists, and HTML content.

The mail task is depicted as a rounded rectangle with an envelope icon in the top-left corner.

![bpmn.mail-task]({% link process-services/images/bpmn.mail-task.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|To|The recipient of the e-mail. You can specify multiple recipients in a comma-separated list. When using a fixed value, this can be an expression. It is also possible, like with the user task, to use the **Identity store** option here to pick users that are known in the system or to reference people that were selected in form fields prior to this email task.|
|From|The sender’s email address. If you do not specify this, the default configured system-wide setting **from** address is used. This can be an expression.|
|Subject|The subject of this email. This can be an expression.|
|Cc|The cc list for this email. You can specify multiple recipients in a comma-separated list. This can be an expression.|
|Bcc|The bcc list for this email. You can specify multiple recipients in a comma-separated list. This can be an expression.|
|Text|The text content of this email. You can specify this as well as HTML to support email clients that do not support rich content. The client will fall back to this text-only alternative.|
|Html|The HTML content of this email.|
|Charset|The charset for this email. By default UTF8 will be used.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|
|Is for compensation|If this activity is used for compensating the effects of another activity, you can declare it to be a compensation handler. For more information on compensation handlers see the Developer Guide.|

### Camel task

You use the Camel task to send messages to, and receive messages from Apache Camel.

A camel task is visualized as a rounded rectangle with a camel icon in the top-left corner.

![bpmn.camel-task]({% link process-services/images/bpmn.camel-task.png %})

You can find more information on Apache Camel [here](http://camel.apache.org/){:target="_blank"}. Note that Camel is by default not installed and would need to be added by the system admin.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Camel context|A camel context definition. If you do not specify a context, the default Camel context is used.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|
|Is for compensation|If this activity is used for compensating the effects of another activity, you can declare it to be a compensation handler. For more information on compensation handlers see the Developer Guide.|

### Mule task

Use the Mule task to send messages to the Mule ESB (Enterprise Service Bus).

A mule task is visualized as a rounded rectangle with the Mule logo in the top-left corner.

![bpmn.mule-task]({% link process-services/images/bpmn.mule-task.png %})

You can find more information on [Mule ESB here](https://www.mulesoft.com/resources/esb/what-mule-esb){:target="_blank"}. Note that Mule is by default not installed and would need to be added by the system admin.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Endpoint url|The Mule endpoint you want to send your message to.|
|Language|The language you want to use to evaluate the payloadExpression, for example [juel](http://juel.sourceforge.net).|
|Payload expression|An expression for the message’s payload.|
|Result variable|The name of the variable to store the result of the invocation.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|
|Is for compensation|If this activity is used for compensating the effects of another activity, you can declare it to be a compensation handler. For more information on compensation handlers see the Developer Guide.|

### REST call task

The rest call task is used to communicate with a REST endpoint. The endpoint can be defined in the process definition, or it can be defined company-wide by an administrator. In the latter case, a logical name is all that is needed.

A rest call task is visualized as a rounded rectangle with a rocket icon the top-left corner.

![bpmn.rest-call-task]({% link process-services/images/bpmn.rest-call-task.png %})

Note that the REST call task always is executed asynchronously.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Endpoint|Defines which REST endpoint to call. It is an endpoint defined company-wide by the administrator (simply select a logical name in the dropdown) or a URL. You can also use a previously defined form fields or variables to build up the URL.<br><br>Use the **Test** button to test the end-point.<br><br> ![]({% link process-services/images/endpoint.png %})<br><br>If the request mapping (see next property) contains key/value properties or a JSON template, you will be prompted to provide test values for the parameters before the endpoint is tested.<br><br>![]({% link process-services/images/endpoint-check.png %})|
|Request mapping|Allows to construct the actual request. HTTP GET represents the URL parameters whereas POST/PUT is the JSON body that is created when the request is sent. You can also use fixed values, form fields, or variables defined prior to this activity.<br><br>![]({% link process-services/images/requestmapping.png %})<br><br>For nested or complex request bodies for POST requests, you can specify a JSON Template which is evaluated at run-time.<br><br>![]({% link process-services/images/request-mapping.png %})<br><br>The JSON editor provides syntax highlighting and will highlight any JSON syntax errors on the line number indicator.|
|Response mapping|Maps the JSON response from the REST endpoint to process variables. You can use a nested notation (for example `prop1.prop2.prop3`) for mapping values. The mapped response values can be used as variables in further steps of the process.|

### Generate document task

The Generate document task generates a document in Word or PDF format and stores the reference to the document as a process variable. The document is based on a (Word) template that describes how the document needs to be rendered, using process variables and various constructs (such as if-clauses and loops).

See [Document Templates]({% link process-services/latest/develop/dev-ext.md %}#document-templates) in the Developing section for how to modify the template for the Generate document task.

A Generate document task appears as a rounded rectangle with a document icon on the top-left corner.

![bpmn.generate-document-task]({% link process-services/images/bpmn.generate-document-task.png %})

|Property|Description|
|--------|-----------|
|ID|A unique identifier for this task element.|
|Name|A name for this task element.|
|Documentation|A description of this task element.|
|Template|The template which is used to generate the document. It can be uploaded as part of the process definition, or can be defined company-wide by an administrator and reused by multiple process definitions.|
|Output format|The document output format will be either PDF or Word.|
|Document variable|This is the process variable in which the reference to the generated document is stored.|
|File name|The name of the document that will be created by the task.|
|Additional data source names|A comma separated list of data sources the document will use as the source of the expressions.|
|Additional data source expressions|A comma separated list of expressions to be included in the document.|

### Decision task

You use a decision task to select a decision table while designing your process model. A decision table enables you to define a set of business rules that will be applied when it’s executed. See the [business rules]({% link process-services/latest/using/process/rules.md %}) section for more information.

A decision task is depicted as a rounded rectangle with a table icon the top-left corner.

![bpmn.decision-task]({% link process-services/images/bpmn.decision-task.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Reference decision table|Defines the actual decision table that will be executed. The decision table can be part of the process definition (a so-called **embedded** decision table) or defined on itself (a so-called **reusable** decision table).|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|
|Is for compensation|If this activity is used for compensating the effects of another activity, you can declare it to be a compensation handler. For more information on compensation handlers see the Developer Guide.|

### Store Entity task

Use the Store entity task to update data models or entities with process values such as variables or form fields. The updated entities can then be mapped to variables and used while creating processes.

![storeentity]({% link process-services/images/storeentity.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Attribute mapping|Attributes mapped for this element instance. Click to invoke the Change value for "Attribute Mapping" dialog, where you can map entities or Data Models with form fields and variables used in your process. See the [Data Models]({% link process-services/latest/using/process/models.md %}) section for more details.|

## Structural components

You use structural components to group multiple components in a sub process to reuse in a parent process definition,
and to embed and call other process definitions from inside your own process.

The types of structural components are:

* [Sub-process](#sub-process)
* [Collapsed sub-process](#collapsed-sub-process)
* [Event sub-process](#event-sub-process)
* [Call activity](#call-activity)

### Sub-process

A sub process is a single activity that contains activities, gateways, and events which form a process. A sub process is completely embedded inside a parent process.

A sub-process is visualized as a rounded rectangle:

![bpmn.embedded-subprocess]({% link process-services/images/bpmn.embedded-subprocess.png %})

You can use a sub process to create a new scope for events. Events that are thrown during execution of the sub process, can be caught by [Boundary events](#boundary-events) on the boundary of the sub process, creating a scope for that event limited to just the sub process.

Sub-processes must have the following characteristics:

* A sub process has exactly one none start event. No other start event types are permitted. A sub process must have at least one end event.
* Sequence flow cannot cross sub process boundaries.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|

### Collapsed sub-process

You use a collapsed sub-process to add an existing process from your available process definitions as a sub-process to the process definition you are currently editing.

When you drag a collapsed sub-process from the palette to your canvas, and click on the Referenced Subprocess property, you are presented with a visual list of the process definitions you have access to. You can choose from the list, and the chosen process will be added to the current process definition. Note the process chosen must have exactly one none start event, and no other start event type, and it must have at least one end event.

Note that during process instance execution, there is no difference between a collapsed or embedded sub-process. They both share the full process instance context (unlike a [call activity](#call-activity)).

Note that when you click on the plus icon in a collapsed sub-process, the BPMN editor will open the referenced sub-process definition.

A collapsed sub-process is visualized as a rounded rectangle with a plus icon inside.

![bpmn.collapsed-subprocess]({% link process-services/images/bpmn.collapsed-subprocess.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element instance.|
|Referenced Subprocess|The process definition this collapsed sub-process contains.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|

### Event sub-process

An event sub-process is a sub-process that is triggered by an event. You can use an event sub-process in your main process, or in any sub-process.

The event sub-process start event defines the event to be handled by the sub-process, so the type of start event you use must have an event associated with it – none start events are not supported but the event sub-processes. Your event sub-process can be started by a start message event, start signal event or a start error event. The subscription to the start event is created when the scope, process instance or sub-process, hosting the event sub-process is created. The subscription is removed when the scope is destroyed.

Your event sub-process does not have any incoming or outgoing sequence flows. An event sub-process is triggered by an event, so there can be no incoming sequence flow.

The best way to look at an event subprocess is as a *method* or *routine* that is called when something happens, and handle it appropriately.

An event sub-process is visualized like a sub-process with a dashed border.

![bpmn.event-subprocess]({% link process-services/images/bpmn.event-subprocess.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|

### Call activity

A call activity is used to execute another process definition as part of the current process instance.

The main difference between a sub-process and a call activity is that the call activity does not share context with
the process instance. Process variables are explicitly mapped between the process instance and the call activity.

A call activity is visualized as a rounded rectangle with a thick border.

![bpmn.call-activity]({% link process-services/images/bpmn.call-activity.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Called element|This is the identifier of the process definition that should be called.|
|In parameters|Configures the process variables that are mapped into the called process instance when it’s executed. It’s possible to copy values directly (using the **source** attribute) or with an expression (using the **source expression** attribute) in a **target** variable of the called process instance.|
|Out parameters|Configures the process variables that are mapped from the called process instance into the parent process instance.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Execution listeners|Execution listeners configured for this instance. An execution listeners is a piece of logic that is not shown in the diagram and can be used for technical purposes.|
|Multi-Instance type|Determines if this task is performed multiple times and how. The possible values are:<br><br>**None**<br><br>The task is performed once only.<br><br>**Parallel**<br><br>The task is performed multiple times, with each instance potentially occurring at the same time as the others.<br><br>**Sequential**<br><br>The task is performed multiple times, one instance following on from the previous one.|
|Cardinality (Multi-instance)|The number of times the task is to be performed.|
|Collection (Multi-instance)|The name of a process variable which is a collection. For each item in the collection, an instance of this task will be created.|
|Element variable (Multi-instance)|A process variable name which will contain the current value of the collection in each task instance.|
|Completion condition (Multi-instance)|A multi-instance activity normally ends when all instances end. You can specify an expression here to be evaluated each time an instance ends. If the expression evaluates to true, all remaining instances are destroyed and the multi-instance activity ends.|

## Gateways

You use gateways to control the flow of execution in your process.

In order to explain how Sequence Flows are used within a Process, BPMN 2.0 uses the concept of a token. Tokens traverse sequence flows and pass through the elements in the process. The token is a theoretical concept
used to explain the behavior of Process elements by describing how they interact with a token as it “traverses” the structure of the Process. Gateways are used to control how tokens flow through sequence flows as they converge and diverge in a process.

As the term gateway suggests, it is a gating mechanism that either allows or prevents passage of a token through the gateway. As tokens arrive at a gateway, they can be merged together on input and/or split apart on output from the gateway.

A gateway is displayed as a diamond, with an icon inside. The icon depicts the type of gateway.

The types of gateway are:

* [Exclusive gateway](#exclusive-gateway)
* [Parallel gateway](#parallel-gateway)
* [Inclusive gateway](#inclusive-gateway)
* [Event based gateway](#event-based-gateway)

### Exclusive gateway

You use an exclusive gateway to model a decision in your process. When execution arrives at an exclusive gateway, the outgoing sequence flows are evaluated in the order in which they are defined. The first sequence flow whose condition evaluates to true, or which does not have a condition set, is selected and the process continues.

An exclusive gateway is visualized as a diamond shape with an X inside.

![bpmn.exclusive-gateway]({% link process-services/images/bpmn.exclusive-gateway.png %})

Note that if no sequence flow is selected, an exception will be thrown.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Flow order|Select the order in which the sequence flow conditions are evaluated. The first sequence flow that has a condition that evaluates to true (or has no condition) will be selected to continue.|

### Parallel gateway

You use a parallel gateway to model concurrency in a process. It allows you to fork multiple outgoing paths of execution or join multiple incoming paths of execution.

A parallel gateway is visualized as a diamond shape with a plus icon:

![bpmn.parallel-gateway]({% link process-services/images/bpmn.parallel-gateway.png %})

In a fork, all outgoing sequence flows are followed in parallel, which creates one concurrent execution for each sequence flow.

In a join, all concurrent executions arriving at the parallel gateway wait at the gateway until an execution has arrived for every incoming sequence flow. Then the process continues past the joining gateway. Note that the gateway simply waits until the required number of executions has been reached and does not check if the executions are coming from different incoming sequence flow.

A single parallel gateway can both fork and join, if there are multiple incoming and outgoing sequence flow. The gateway will first join all incoming sequence flows, before splitting into multiple concurrent paths of executions.

>**Note**. Unlike other gateways, the parallel gateway does not evaluate conditions. Any conditions defined on the sequence flow connected with the parallel gateway are ignored.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced)Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|

### Inclusive gateway

You use an inclusive to join and fork multiple sequence flows based on conditions.

Like an exclusive gateway you can define conditions on outgoing sequence flows and the inclusive gateway will evaluate them, but an inclusive gateway can take more than one sequence flow, like the parallel gateway.

All outgoing sequence flow conditions are evaluated. Every sequence flow with a condition that evaluates to true, is followed in parallel, creating one concurrent execution for each sequence flow.

The join behavior for an inclusive gateway is more complex than the parallel gateway counterparts. All concurrent executions arriving at the inclusive gateway wait at the gateway until executions that *can* reach the inclusive gateway have reached the inclusive gateway. To determine this, all current executions of the process instance are evaluated, checking if there is a path from that point in the process instance to the inclusive gateway. (ignoring any conditions on the sequence flow). When one such execution is found, the inclusive gateway join behavior does not activate.

An inclusive gateway is visualized as a diamond shape with a circle icon inside:

![bpmn.inclusive-gateway]({% link process-services/images/bpmn.inclusive-gateway.png %})

Note that an inclusive gateway can have both fork and join behavior, in which case there are multiple incoming and outgoing sequence flows for the same inclusive gateway. The gateway will join all incoming sequence flows that have a process token, before splitting into multiple concurrent paths of executions for the outgoing sequence flows that have a condition that evaluates to true.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element instance.|
|Name|A name for this element instance.|
|Documentation|A description of this element instance.|
|Asynchronous|(Advanced) Define this task as asynchronous. That is, the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. That is, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Flow order|Select the order in which the sequence flow conditions are evaluated. This is of less importance as for the exclusive gateway, as all outgoing sequenceflow conditions will be evaluated anyway.|

### Event based gateway

You use an event gateway to route process flow based on events.

Each outgoing sequence flow of the event gateway must be connected to an intermediate catching event. When process execution reaches an event gateway execution is suspended, and for each outgoing sequence flow, an event subscription is created. The flow for the event that occurs first, will be followed.

Outgoing sequence flows connect to an event gateway are never "executed", but they do allow the process engine to determine which events an execution arriving at an event-based gateway needs to subscribe to. The following restrictions apply to event gateways:

* The gateway must have two or more outgoing sequence flows.
* An event-based gateway can only be followed by intermediate catching events. Receive tasks after an event gateway are not supported by Process Services.
* An intermediate catching event connected to an event gateway must have a single incoming sequence flow.

An event gateway is visualized as a diamond shape with a plus icon inside. Unlike the parallel gateway, the plus icon is not colored black inside:

![bpmn.event-gateway]({% link process-services/images/bpmn.event-gateway.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element instance.|
|Name|A name for this element instance.|
|Documentation|A description of this element instance.|
|Asynchronous|(Advanced) Define this task as asynchronous. This means the task will not be executed as part of the current action of the user, but later. This can be useful if it’s not important to have the task immediately ready.|
|Exclusive|(Advanced) Define this task as exclusive. This means that, when there are multiple asynchronous elements of the same process instance, none will be executed at the same time. This is useful to solve race conditions.|
|Flow order|Select the order in which the sequence flow conditions are evaluated.|

## Boundary events

You use boundary events to handle an event associated with an activity. A boundary event is always attached to an activity.

While the activity the boundary event is attached to *is active* (meaning the process instance execution is currently executing it right there), the boundary event is listening for a certain type of trigger. When the event is caught, the activity is either interrupted and the sequence flow going out of the event is followed (interrupting behavior) or a new execution is created from the boundary event (non-interrupting behavior).

The types of boundary event are:

* [Boundary timer event](#boundary-timer-event)
* [Boundary error event](#boundary-error-event)
* [Boundary signal event](#boundary-signal-event)
* [Boundary message event](#boundary-message-event)
* [Boundary cancel and compensation event](#boundary-cancel-and-compensation-event)

### Boundary timer event

A boundary timer event puts a timer on the activity it is defined on. When the timer fires, the sequence flow going out the boundary event is followed.

A boundary timer event is visualized as a circle with a clock icon inside:

![bpmn.boundary-timer]({% link process-services/images/bpmn.boundary-timer.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Cancel activity|Defines if the boundary event interrupts the activity is defined upon or not.|
|Time Cycle|A timer cycle defined in [ISO 8601](http://en.wikipedia.org/wiki/ISO_8601){:target="_blank"} format, for example: `R3/PT10H`.|
|Time Date in ISO-8601|A point in time defined as an [ISO 8601](http://en.wikipedia.org/wiki/ISO_8601){:target="_blank"} date, for example: `2015-04-12T20:20:32Z`.|
|Time Duration|A period of time defined as a [ISO 8601](http://en.wikipedia.org/wiki/ISO_8601){:target="_blank"} duration, for example: `PT5M`.|

### Boundary error event

A boundary error event catches an error that is thrown within the boundaries of the activity the event is based on and continues process execution from the event.

A boundary error event is always interrupting.

A boundary timer event is visualized as a circle with a lightning icon inside:

![bpmn.boundary-error]({% link process-services/images/bpmn.boundary-error.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Error reference|The identifier of the error to catch.|

### Boundary signal event

A boundary signal event listens to a signal being fired (from within the process instance or system-wide) while the activity upon which the event is defined is active.

A boundary signal event is visualized as a circle with a triangle icon inside:

![bpmn.boundary-signal]({% link process-services/images/bpmn.boundary-signal.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Signal reference|The signal to listen to. Signals are defined on the root process definition level and are linked with this property.|

### Boundary message event

A boundary message event listens to a message being received while the activity upon which the event is defined is active.

A boundary message event is visualized as a circle with an envelope icon inside:

![bpmn.boundary-message]({% link process-services/images/bpmn.boundary-message.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Message reference|The message to listen to. Messages are defined on the root process definition level and are linked with this property.|

### Boundary cancel and compensation event

The boundary cancel and compensation event are currently experimental features. See [http://activiti.org/userguide/index.html#bpmnBoundaryCancelEvent](https://www.activiti.org/5.x/userguide/index.html#bpmnBoundaryCancelEvent){:target="_blank"} for more information on them.

## Intermediate catching events

An intermediate catching event is a step in the process where the process needs to wait for a specific trigger (in BPMN this is described as *catching* semantics).

An intermediate event is displayed as two concentric circles containing an icon. The icon shows the type of intermediate event:

![bpmn.intermediate-catch-events]({% link process-services/images/bpmn.intermediate-catch-events.png %})

Conceptually, the intermediate catch events are close to the boundary events, with that exception they don’t define a scope (the activity) for when the event is active. An intermediate catch event is active as long as the trigger hasn’t happened. A boundary event on the other hand can be destroyed if the activity completed.

All the supported intermediate catch events are configured similar to their boundary event counterparts.

## Intermediate throwing events

An intermediate throw event is used to explicitly throw an event of a certain type.

Currently, two types are supported:

* The **none intermediate throwing event**. No event is thrown. This is mainly used as a marker in the process definition (for example to attach execution listeners that are used to indicate somehow that some state in the process has been reached).
* The **signal intermediate throwing event**. Throws a signal event that will be caught by boundary signal events or intermediate signal catch events listening to that particular signal event.

An intermediate event is displayed as two concentric circles which may contain an icon. If present, 
the icon shows the type of intermediate event. A throwing none event contains no icon.

## End events

You use an end event to signify the end of a process or sub-process, or the end of a path in a process or sub-process.

In a subprocess or process instance, only when all executions have reached an end event will the subprocess be continued or the whole process instance ended.

An end event is displayed as thick black circle which may contain an icon. If present, the icon shows the type of end event. A none end event has no icon.

The types of end event are:

* [None end event](#none-end-event)
* [Error end event](#error-end-event)
* [Terminate end event](#terminate-end-event)
* [Cancel end event](#cancel-end-event)

### None end event

A none end event ends the current path of execution.

![bpmn.none-end-event]({% link process-services/images/bpmn.none-end-event.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Execution listeners|Execution listeners configured for this event.|

### Error end event

You use the end error event to throw an error and end the current path of execution.

![bpmn.error-end-event]({% link process-services/images/bpmn.error-end-event.png %})

The error can be caught by an intermediate boundary error event that matches the error. If no matching boundary error event is found, an exception will be thrown

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Execution listeners|Execution listeners configured for this instance.|
|Error reference|The error identifier. This is used to find a matching catching boundary error event. If the name does not match any defined error, then the error is used as the error code in the thrown exception.|

### Terminate end event

When a terminate end event is reached, the current process instance or sub-process will be terminated. Conceptually, when an execution arrives in a terminate end event, the first scope (process or sub-process) will be determined and ended. Note that in BPMN 2.0, a sub-process can be an embedded sub-process, call activity, event sub-process or transaction sub-process. This rule applies in general, for example, when there is a multi-instance call activity or embedded subprocess, only that instance will be ended, the other instances and the process instance are not affected.

![bpmn.terminate-end-event]({% link process-services/images/bpmn.terminate-end-event.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Execution listeners|Execution listeners configured for this.|

### Cancel end event

The cancel end event ends the current path of execution and throws a cancel event that can be caught on the boundary of a transaction subprocess.

![bpmn.cancel-end-event]({% link process-services/images/bpmn.cancel-end-event.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Execution listeners|Execution listeners configured for this.|

## Swimlanes

You use swimlanes to display activities in your process divided by business function or participant group. A process definition can have one swimlane diagram containing one pool, which in turn contains one or more lanes. The pool represents the whole process, and each lane corresponds to a business function or participant group.

For example, the process of selling a book consists of several activities: ordering a book, processing the order, shipping the book, and reading the book. However, the activities are performed by participants in different groups: by the customer, by the sales department, by the warehouse, or store. In the following diagram, process definitions have one pool called Sell a book with three lanes: Customer, Sales, and Store. The process sequence flow moves between lanes in the pool as the order progresses.

![bpmn.swimlanes.png]({% link process-services/images/bpmn.swimlanes.png %})

When you drag a pool to your process diagram, it creates an unnamed pool containing one unnamed lane. You can add lanes by dragging a lane icon from the palette to the canvas. When you hover over the name box of the pool, the whole pool border turns green, indicating the lane will be added to the pool when you release the mouse button.

## Artifacts

You use artifacts to provide additional information about the process. The BPMN editor supports the text annotation artifact which associates additional text to an element in your process, or to the process itself. The text does not influence the execution of a process and is provided by the process designer to give information to the user of the process.

**Text annotation**

You can set the following properties in the property sheet:

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element instance|
|Name|A name for this element instance|
|Documentation|A description of this element instance|
|Text|The text you want to display in your annotation|

## Alfresco Content Services actions

Use this section for actions specific to Alfresco Content Services content store:

* Publish to Alfresco task - upload content to Alfresco Repository
* Retrieve Alfresco Properties - fetch metadata (properties) for content in the Alfresco Repository
* Update Alfresco Properties - update metadata (properties) for content in the Alfresco Repository
* Call Alfresco Action - invoke a Repository Action

### Publish to Alfresco task / Box / Google Drive

The publish task enables you to publish items that were created or modified during process instance execution to a content store. Currently, the following content stores are supported:

* Alfresco Content Services
* Box
* Google Drive

A publish task is depicted as a rounded rectangle with the icon of the content store on the top-left corner.

![bpmn.publish-task.png]({% link process-services/images/bpmn.publish-task.png %})

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Alfresco / Box / Google Drive Content|Configures what content to publish. You can select a previously defined form field or all the content that was updated during the process instance execution.|
|Alfresco / Box / Google Drive Destination|Configures where the content will be published to. You can publish the content using the process initiator or a specific user (this is important when it comes to permissions in the content store).|

### Retrieve Alfresco Properties

The Retrieve Alfresco Properties option enables you to retrieve content-specific properties from Alfresco Content Services and map it to a form field or variable, for example properties of a document. You can retrieve document information after a document is added or referenced via the Attachment form field in Share Connector.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Alfresco properties|Retrieves Alfresco Content Services properties for content stored in the form editor or variable, and allows mapping them.|

### Update Alfresco Properties

The Update Alfresco Properties option enables you to update content-specific properties in Alfresco Content Services via a form field or variable. For example, you can update properties of a document linked from Alfresco Content Services via a form attachment field, or process variable.

The Properties sheet displays the same fields as Retrieve Alfresco properties, except that is used for updating properties rather than retrieving.

### Call Alfresco Action

See this [documentation]({% link process-services/latest/using/process/step.md %}#call-alfresco-action).
---
title: Using the Form Editor 
---

The form editor provides a powerful drag and drop interface to let you design forms from a rich set of controls. You can define form outcomes and create forms with multiple tabs. Individual controls and whole tabs can be made visible depending on the value of other form fields and process variables. You can design your form with groups of controls in varying numbers of columns.

![app-form-editor]({% link process-services/images/app-form-editor-1.png %})

In the example above, the form editor is open on a form containing two controls, a text box, and a multiline text box.

## Form Controls

The form controls for each field determine how the field is displayed and handled.

|Control|Description|
|-------|-----------|
|Text|Allows you to enter text.|
|Multi-line Text|Enables you to enter multiple lines of text within a text box.|
|Number|Allows you to enter a number.|
|Checkbox|Allows selection and deselection of the field.|
|Date|Allows selection of a date from a pop-up calendar.|
|Date/Time|The behavior is similar to that of the Date control, with the added capability of allowing selection of a time value.|
|Dropdown|Allows you to select an item from a displayed list of items.|
|Typeahead|On entering data, displays filtered information in a list and allows selection of a value.|
|Amount|Allows you to input data representing an amount of money and to define a currency type.|
|Radio buttons|Allows you to choose an item from a predefined list.|
|People|Allows you to select a person from a list.|
|Group of people|Allows you to create a group of people by selecting names from a list.|
|Dynamic table|Allows you to input multiple rows of data in a table.|
|Hyperlink|Displays a hyperlink.|
|Header|Acts as a container into which you can drag and drop other control fields. You can organize these into columns and label them. You can also add a title in the header element.|
|Attach file|Allows you to upload and attach files from the file system or other sources, for example, Box, Google Drive. See next section for more info.|
|Display value|Allows you to display the value of a field or variable previously submitted in any form.|
|Display text|Allows you to display text for a field. You can also display values previously submitted in any form, and include this within the text.|

### Attach file

Allows you to upload and attach files from the file system or other sources, for example, Box, Google Drive.

|Property|Description|
|Label|The name of the field that will appear on the rendered form.|
|Override ID?|Sets whether the root folder is created by default.|
|ID|The unique ID of the field.|
|Required|Checking this box makes a field mandatory.|
|Colspan|Then number of columns a field spans.|
|Placeholder|The default value of the field.|
|Allow multiple files to be attached|Checking this box will allow for more than one file to be uploaded.|
|Just link to files, do not copy files to Process Services|Checking this box means that the form submission only contains the path to the upload(s) rather than uploading the actual file(s)|
|File source|Sets the location for where files can be uploaded from. Alfresco Content is from an APS instance, whilst local file is local to the form filler|

>**Note:** Setting `alfresco.content.useLatestVersion` to `true` in `activiti-app.properties` will ensure that the latest version of the file will be used.
---
title: Overview of Process Services
---

Process Services can be accessed by default under `/activiti-app`, for example `http://localhost:8080/activiti-app`.

## The landing page

The landing page is your user interface to Process Services. Each tile gives you tools for distinct sets of tasks:

![Process Services landing age]({% link process-services/images/gs-dashboard.png %})

The landing page is the starting point from which you can use:

* **App Designer** - to design your processes.
* **My Tasks** - to view your task inbox or queue.
* **Profile management** / **Identity management** - to manage user and group capabilities
* **Analytics** - to generate reports on process performance

Depending on the capabilities of your account you may or may not get access to the **App Designer** or **Analytics**.

**Profile management** will appear for you only if you are a user. This is where you manage your personal information. If you have administrator capabilities, then **Profile management** will be displayed as **Identity management**. Use this tile to access your profile page as well as to manage user, group, and capability management pages for your tenant or the whole system.

You can click on the Process Services logo at any time to return to your landing page.

Your landing page is dynamic, and new tiles will appear when you create new process apps in the App Designer and deploy them in the Task App.

You'll also see a list of shortcuts for tasks you might want to do next.

>**Note:** If you are an administrator, your landing page is slightly different. Instead of the Profile management tile, you’ll find a more powerful set of tools called the Identity management tile.

All pages display the App Navigator icon in the far-right corner of the header. It provides useful 1-click shortcuts to various parts of the app. You can navigate instantly to all your process models, tasks, processes, stencils, forms, decision tables, quickly start any process, view the tasks and processes for a published and deployed app, or view and change your profile. As you deploy process apps, the App Navigator will also show shortcuts for the newly created process apps.

## Task App

Use the Task App to access your task list and work on tasks assigned to you from the Processes tab. This is also where you initiate new processes and tasks.

![App My Tasks]({% link process-services/images/app-my-tasks.png %})

The Task App menu bar has tabs for working with tasks, processes, reports, and a Start button, which is a shortcut to start a process using a published process definition.

>**Note:** If you haven’t created any tasks for yourself, and there are no tasks assigned for you from current processes or from other users, then James will appear with shortcuts to help you create a task or start a published process.

### Tasks tab

The Tasks tab is organized into three columns.

* The left column lets you filter the list of displayed tasks. There are four pre-defined filters and a New Filter control which lets you define and name your own filters. Any filters you create are added to the list of displayed filters.
* The middle column provides tools for creating new tasks, and lists the tasks included by the current active filter. Click on the accordion icon above the list of tasks to change the default display order from Newest first to oldest first, Due last order, or Due first order.
* The right column is displayed when you click on a task in the middle column. It displays the selected task details and also tools for completing open tasks and for viewing the audit log of a completed task.

>**Note:** The Audit log button is only available for a completed process instance or a completed task.

#### Using a new filter in tasks and processes

When you create a new filter in the Tasks tab or Processes tab, you can filter by process definition, the state of the task/process, by task name, and by assignment. You can also change the default sort order.

* **Process definition**

    Select an active (running) process name, and display only those tasks that are associated with that process.

* **State**

    Choose to display tasks or processes based on its state. For tasks, select Completed or Open. Completed is selected by default. For processes, select Running, complete, or All. Running is selected by default.

* **Assignment**

    Select tasks in which you are involved, or tasks that have been assigned to you, or tasks where you are one of the several candidates. This is only applicable to the Tasks tab.

* **Sort**

    Sort the list by Newest first, Oldest first, Due last, or Due first.

* **Task name / Process Name**

    Type a string to search for matching task names or process name depending on the tab you’re in.

* **Filter icon and name**

    Select an icon for your new filter by clicking on the funnel icon, and specify a name for the filter.

>**Note:** If you have no tasks or processes running, then James will appear with a shortcut to let you create a new task for yourself or start an existing process and track its progress.

### Processes tab

Use the Processes tab to start a new process from a list of published process definitions. The Processes tab is organized into three columns similar to the Tasks tab (see above) except that instead of tasks, process details are displayed. You can also create a new filter to filter by process definitions, process state, and by process name.

### Reports tab

Use the Reports tab to generate reports based on the available parameters. You can view the reports that you saved in the Analytics App. For more information, see [Analytics App](#analytics-app).

## Profile management

You can add a photo to your profile.

To edit your profile, click **Profile management**.

On the **Personal** page you can edit your details, such as your name, change your password, and view your group membership and capabilities.

To add your photo, click the image to the left of your name and upload the desired photo.

![Personal profile]({% link process-services/images/3.png %})

## Identity management

These are operations to manage tenants, groups and users. This is useful for example to bootstrap environments with the correct identity data.

### Tenants tab

Use the Tenants tab for creating new tenants, and modifying existing tenants.

By default, the details of the currently selected tenant are displayed. You can edit the name of the current tenant
and configure various settings as follows:

* **Logo** - Add or update your existing logo.

* **Events** - A log of management events for the tenant.

* **Alfresco repositories** - Configure your on-premise repositories. See *Create Alfresco repository*.

* **Endpoints** - Configure your RESTful endpoints and Basic Authentication for endpoints.

* **Data sources** - Register your data sources for using in Data Model.

* **Document templates** - Upload a Microsoft Word (.docx) file that can be used as a template in processes.

* **Email templates** - Create new custom email templates, view or edit the existing templates (both standard and custom). For information on creating custom templates, see next section about Custom email templates.

* **Config** - Configure settings for Box metadata support, validate decision table expressions, and enable or disable the option for involved users to edit forms. In addition, you can define the minimum length for the password, and the date format for forms (for example, *D-M-YYYY*).

#### Custom email templates

Create custom email templates to send an email to the assigned user of a user task after the task is assigned to them.

Custom email templates can be created centrally or within an application when it is being designed.

Templates can contain process and task variables using the format `${title}` where the variable is called `title`.

The following predefined variables can also be used depending on the `assignment` of the [user task]({% link process-services/latest/using/process/bpmn.md%}#user-task):

|Assignment|Variable|
|----------|--------|
|Single User Task|`taskCreator`, `taskName`, `taskDirectUrl`, `homeUrl`|
|Group Task|`groupName`, `taskName`, `taskDirectUrl`, `homeUrl`|
|Candidate User Task|`taskName`, `taskDirectUrl`, `homeUrl`|

>**Note:** If a process or task variable uses the same name as a predefined variable, the value of the process or task variable takes precedence in the template.

The following is an example of a custom email template using variables:

```text
A ${taskName} has been assigned to ${userName} for approval by ${dateDue}. 

If a response is not received within ${sla} it will be automatically approved. 
```

Custom email templates can be created at the tenant level or per application:

##### Tenant level templates

>**Note:** Users require the **Administration of tenant of this group** permission to manage email templates.

1. Navigate to **Identity Management** > **Tenants** > **Email templates**.
2. Select **Create new email template** on the **Custom email templates** tab.
3. Write and save a new custom email template with a name, subject and email body.

Existing custom templates can managed, edited and deleted in the same location.

##### Application level templates

1. Add a user task to a process and check the **Allow email notifications** property for it.
2. Select the **Custom template** property in the same user task.
3. Write and save a new custom email template with a name, subject and email body.

### Users tab

The users tab provides tools for managing users. The current users are displayed on the right panel. You can select from the list of users and use **Select an action** to change details, status, account type, password, and primary group of the user. In addition, you can create a new user, or filter the list of current users by status, account type, email or name, and company.

### Capabilities tab

Use the Capabilities tab for managing the capabilities and groups of users that are available for this tenant.

There are two types of groups:

* **Capability groups** - Groups that can be granted with variety of capabilities.

* **Organization groups** - Functional groups that reflect the structure of your organization.

The following capability groups are available by default:

* **Analytics-users** - Access the Analytics app to view reports.

* **Superusers** - Administration of tenant of this group gives full administration rights for the current tenant to the selected group.

* **App Designer** - Access to App Designer app that allows you to design and publish process definitions.

In addition, an Administrator can grant to the following capabilities to any of the capabilities groups:

* Access Analytics app

* Access App Designer app

* Access the REST API

* Access to all tenants' models

* Administration of tenant of this group

* Publish app to user dashboard

* Upload license

You create and delete capabilities groups, add and remove users to and from a group, and add and remove capabilities to and from all users in a group.

### Organization tab

Use the Organization tab to create functional groups that reflect the structure of your organization. Groups are used to grant access to apps or tasks. You can also add and remove users to and from a group, and create subgroups within a group.

#### Create a group

1. Click **Create group**.
2. Enter a name, for example *Group 1* and *Group 2*.
3. Click **Save**.

```text
Group 1

Group 2
```

Result: *Group 1* and *Group 2* have been created as groups.

#### Create a subgroup

1. Select a group, for example *Group 1*.
2. Click **Create subgroup**.
3. Enter a name, for example *Group 1.1*.
4. Click **Save**.

```text
Group 1 
    Group 1.1

Group 2
```

Result: *Group 1.1* has been created as a subgroup of *Group 1*.

#### Add an existing group

1. Select a group, for example *Group 2*.
2. Click **add existing group**.
3. Enter an existing group name, for example *Group 1.1*.
4. Select the group from the dropdown menu.

```text
Group 1 

Group 2 
    Group 1.1
```

Result: *Group 1.1* has been moved from being a subgroup of *Group 1* to *Group 2*.

Another example:

1. Select a group, for example *Group 1*.
2. Click **add existing group**.
3. Enter an existing group name, for example *Group 2*.
4. Select the group from the dropdown menu.

```text
Group 1 
    Group 2 
        Group 1.1
```

Result: *Group 2* has been added as a subgroup of *Group 1* and *Group 1.1* persists as a subgroup of *Group 2*.

#### Delete a group

1. Select a group to delete, for example *Group 1*.
2. Click the delete button (trashcan icon).
3. Click the delete button again.

```text
Group 1 (deactivated)
    Group 2 (deactivated)
        Group 1.1 (deactivated)
```

Result: *Group 1* has now been deleted.

>**Note:** When you first click the delete button a group, it will be deactivated, until all its tasks are complete. To delete the group completely, click the delete button a second time. When you delete a group, this will delete all its subgroups.

#### Add users to a group

1. Select a group to add users to.
2. Search for a user to add, for example *user1*.
3. Select the user from dropdown menu.

|Email|Name|
|-----|----|
|user1@app.activiti.com|user1|

Result: *user1* has been added to the group.

#### Assign a group manager

1. Select a group to assign a manager to.
2. Click **select user** next to Group manager.
3. Search for a user to appoint as manager, for example *user2*.
4. Select the user from the dropdown menu.

Result: *user2* has been appointed as the group manager.

>**Note:** All changes made in the Organization tab are listed in the [Tenants tab](#tenants-tab) under Events.

## Analytics App

Use the Analytics tile to add standard reports and configure custom reports for performance and throughput statistics of your processes. You can view the Analytics App tile only if your account has the Analytics capability. Before generating process reports, make sure to run your processes at least a few times.

![Analytics App]({% link process-services/images/32.png %})

When you visit the Analytics App for the first time, you'll see some useful hints on the welcome screen.

![Analytics App Reports]({% link process-services/images/james-reports.png %})

The Analytics App has the following tabs:

* **Reports** - Use this to add standard reports in Process Services and view the existing reports.
* **Configure** - Use this to configure standard reports and custom reports.

### Configure standard reports

In Process Services, you can add Standard reports at a click of a button. You can choose to add all standard reports at once or configure only the reports you’re interested in. For example, you can configure your report panel to isolate Task related reports such as Task overview and Task service level agreement reports, or custom reports that are based on generated reports (see [Customizing reports](#customize-reports)).

#### Add standard reports

* From the **Analytics app** > **Reports** tab, click **Add some standard reports now** link. The following standard reports appear in your Reports panel on the left:

    * Process definition heat map
    * Process definition overview
    * Process instances overview
    * Task overview
    * Task service level agreement

Alternatively, you can also add the same set of standard reports via the Configure tab. To remove your existing reports from the Reports panel, click **Reset all my reports**.

Once you have added the standard reports, you can access them from the Reports panel and generate them based on the
required filter parameters. If the data is available, it will be presented in graph and tabular form, depending on the report selected.

### Filter reports

You can filter most reports by the following parameters:

* Date range
* Process definition
* Process Status
* Task (Task related report only)
* Task Status (Task related report only)

Some reports such as Task service level agreement and Process instances overview reports have additional parameters.

### Customize reports

You can customize reports by selecting the Process Status and Date Range parameters. You can also create new reports 
by modifying the filter option of an existing report and saving it with a new name.

#### Generate and save a Task overview report

1. Sign in to Process Services as a user with Administrator privileges.

2. Click **Analytics App** > **Configure** and then Task overview.

3. Select from the following filter options:

    * **Process Definition** - Process definitions for the selected user.
    * **Date Range** - Tasks from Today, Yesterday, Last 7 days, Previous month, Current year, or Custom Range.
    * **Task Status** - All tasks, Active, or Complete.
    * **Aggregate dates by** - Tasks by hour, day, week, month, or year.
        Relevant data for Task Counts, Task counts by assignee, Number of tasks divided by date interval, Task Duration, and statistics of all tasks are presented in graphical, tabular, and table formats. In addition, there’s an option to view the previous chart data in a table format.

4. Click **Export Data** to generate the report in csv format.

5. Optionally, to save the report with the selected filter options, click **Save this report**. You can also choose to save the report by a new name for easy identification. For example, if your report is specific to a task called Patients List, you could save the report as Task overview for Patients' list.

![Task overview]({% link process-services/images/taskoverview.png %})

You can generate all other reports in the same way by using the appropriate filter options. You are now ready to explore the advanced reporting and analytic features in Process Services.
---
title: Using Data Models 
---

A Data Model enables you to access and manipulate data related to a business process in Process Services. For example, you can define a data model that maps to a relational database (via JDBC) or a custom API to connect to an external source such as a patient database or a customer database.

To use the Data Model functionality effectively, perform one or all of the following steps:

* Reference an entity while mapping variables.
* Make entity fields visible in the process by mapping them.
* Reference mapped entity fields in forms when creating or editing forms.
* Reference entity fields in expressions when creating or maintaining decision tables.

## Connect a data model to a relational database

You can establish connection from your process with a relational database. To enable the connection, you must first register the data source for your tenant in the [Identity Management app]({% link process-services/latest/using/process/index.md %}#identity-management) in Process Services.

To configure the data source follow these steps:

1. In the **Identity Management** app, click **Tenants > Data sources**.
2. Click the **+** (plus icon) and configure the following settings (see the `activiti-app.properties` file for more details):
    * **Name** – Name of your data source. For example, modeler.
    * **JDBC url** – The JDBC URL used to connect to the database. For example:
        `jdbc:mysql://127.0.0.1:3306/modeler?characterEncoding=UTF-8`.
    * **Driver class** – The JDBC driver used to connect to the database. For example: `com.mysql.jdbc.Driver`.
    * **Username & Password** – The username and password of the account used to connect to the database.
3. Click **Save**.

## Define data models

Once defined, Data Models enable you to read, insert, update, and delete entities while working through your process.

When configuring data source and data models for DBMSs you will normally require the JDBC driver to be available at run-time. Process Services is only supplied with the driver for the H2 database. For other DBMSs (MySQL, Oracle, PostgreSQL) make sure that the relevant JDBC drivers are in the classpath, for example the Tomcat library path or `<Process Services Installation>/tomcat/webapps/activiti-app/WEB-INF/lib`.

You can either manually define a data model or import it from an existing data source, such as a relational database schema or an Alfresco Content Services content model.

To define a data model follow these steps:

1. From the **App Designer**, click **Data Models**. The Data Models page is displayed.
2. Click **Create Data Model**. The Create a new data model dialog box appears. Or to import an existing data model, click **Import Data Model**.
3. Select the data source that you defined in Identity Management.
4. Click **Add Entity** and enter data in the following fields:
    * **Entity name** – The name you want to use for the entity, for example, Customer.
    * **Entity description** **(optional)** – Description of the entity.
    * **Table name** – The database table name that you want the entity to be mapped to, for example Customer.
    * **Attributes** – Displays the entity attributes as you add them.
5. Click **Add Attribute** and enter data in the following fields:
    * **Attribute name** – Name you want to use for the attribute, for example, Customer Id.
    * **Attribute description (optional)** – Description of the attribute.
    * **Column name** – Column name as specified in the database, for example, id.
    * **Attribute type** – One of the following attribute types: String, number, date.
    * **Primary key** – Select to indicate if the attribute is a primary key or not.
    * **Database generated value (autoincrement)** - Select this if the primary key is set to autoincrement in the database.
    * **Required** – Select to indicate if the attribute should be mandatory or not.
6. Save the data model.

>**Note:** The **Remove entity** and **Remove attribute** buttons can be used to remove entities and attributes respectively.

## Import data models

Use these instructions to import a data model from a database schema.

To import a data model follow these steps:

1. From the **App Designer**, click **Data Models**.
    The **Data Models** page is displayed.
2. Click **Create Data Model**.
    The Create a new data model dialog box appears. Or to import an existing data model, click **Import Data Model**.
3. Select the data source that you defined in Identity Management.
4. Click **Import**.
    This examines the RDBMS of the datasource and creates an entity and an attribute for each table. In this example, we use the MySQL sample database, [Sakila](https://dev.mysql.com/doc/sakila/en/sakila-installation.html){:target="_blank"}.

    ![data-models]({% link process-services/images/data-models.png %})

5. You can now change the attributes, save the model, and use it as if it was created manually.
6. If you attempt to re-import a database schema, you can either:
    * cancel the operation,
    * skip overwriting the existing entities and only import entities added since the last import, or
    * overwrite all entities.

    ![dataimport-options]({% link process-services/images/dataimport-options.png %})

    If you overwrite, any changes made to the entities and the attributes since your last import will be lost.
7. You may also use **Import attributes** for individual entities which updates the attributes of the selected entity. This is useful if you have only made changes to a single table. In our example, the field region was added in the city table.

    ![entities]({% link process-services/images/entities.png %})

    To import attributes:

    * Select the entity you want to update.
    * Click **Import attributes**.
    * You will prompted again to select how to handle the existing attributes.
        You can either:
        * cancel the operation,
        * skip overwriting the existing entities and only import entities added since the last import, or
        * overwrite all entities.
        Select **Skip** overwriting existing attributes if you have renamed attributes and you want to save your changes while adding new attributes.
        Select **Overwrite** if you want to reset the changes you have made to the attributes and bring in new additions.

## Using the data model in a process

Once you have defined the data model for a database data source, the next step is to use them in forms, decision tables, and process conditions, by mapping them into form fields or process variables. For example, to use patients’ information, you can map their information such as their name and address into your forms.

To start accessing data using your data model, follow these steps:

1. From the **App Designer**, create a simple business process model with a BPMN task that includes a Start event, Store entity task, and an End task.

    ![datamodel_1]({% link process-services/images/datamodel_1.png %})

2. From the BPMN editor, select the Start event and then click **Referenced Form** to select an existing form, or create a new form. The Form reference dialog box appears.
3. Select the form that you want to customize and click **Open**.
4. In the selected form, drag a text type field from the palette, rename it as Company name and then save it.
5. From the BPMN editor, click **Form field to data model mapping**. A dialog box to change value for form field to data mapping appears.
6. Map the fields for Company Name as shown below:

    ![datamodel_2]({% link process-services/images/datamodel_2.png %})

7. From the BPMN editor, click the **Store entity task** and then **Attribute mapping** to edit the mappings. The Change value for Attribute mapping dialog box appears.

    ![Datamodel_3]({% link process-services/images/Datamodel_3.png %})

8. Select the **Mapped data model** and **Mapped entity**.
9. Add a new variable or use an existing variable. In this case, select an existing one: *ThisCompany – Customer*.
10. Map the attribute names with mapped value by selecting the required attribute in the Attribute table as shown below:

    ![Datamodel_4]({% link process-services/images/Datamodel_4.png %})

11. Configure the variable for the selected mapping, and then click **Save**.
12. Publish your app and verify the data connection by making changes to the process data.

### Map complex custom control values

Process Services provides capability to write data from a complex custom control to a data model, allowing the data in the custom control to be externalized.

Developers can define a ‘value path’ that is stored in Process Services and made available to the developer at runtime, allowing them programmatic access to the information in the custom control. This information can then be extracted into a custom data model.

The implementation uses the Alfresco data model service `AlfrescoCustomDataModelService` to connect the custom data models to external sources and perform custom data operations. The value path should be injected into the wrapper bean class to make it available with the mapped complex data model field at application runtime. The value path value is stored in JSON format in the database.

An optional 'Field value path' is available for custom controls in the **Attribute mapping** for the 'Store Entity task'.

1. From the BPMN editor, click the Store Entity task containing your attribute mappings.
2. Click **Attribute mapping** to edit the mappings. The **Change value for Attribute mapping dialog** dialog box appears.

    ![custom-control-field-value]({% link process-services/images/custom-control-field-value.png %})

3. Click on an entry in the Attribute table and then click the **Form field** tab.
4. Select the custom control from the **Form field** dropdown list and assign a value path in the **Field value path** field.
5. Click **Save** to save your changes.
6. The values from the custom control will be made available in the specified value path at runtime.

>**Note:** The developer must manage the protocol for storing data in a custom control (such as JSON in a text field) and the data extraction scheme (such as the developer implemented and documented syntax for extraction) for mapping custom control values.

>**Note:** The developer is also responsible for taking the data storage protocol and mapping scheme available to them and writing values to the custom control. This also extends to making sure the field value path is specified correctly, as exception handling is not included.

## Save data using your data model

As you collect new data about an entity, you may wish to save this back to the database. However, as this is not done automatically when a form is saved, you must create a task in your process to explicitly save the data you want.

To save data using the data model, follow these steps:

1. From the **App Designer**, edit the business process model you created above to access data.
2. In the **Visual Editor**, drag the **Store entity task** activity type from the palette and place before the process **End**.
3. Remove the link from the selected task and connect the Store task between it and the process End.
4. Edit the Store entity task activity and click the attribute mapping field. Configure the following settings in the Attribute Mapping dialog box:
    * **Mapped data model** – Select the data model to map your entity with.
    * **Mapped entity** – Select the entity to map your data model with.
    * **New Variable/ existing variable** – Create a new variable or select an existing variable.
    * **Attribute name** – Map the attribute names with the relevant form fields by selecting the relevant form field value from the drop-down list. For example, Customer Id with ID and Customer name with Name.
    * **Mapped value type** – Select one of the value types for mapping attributes. In the above example, Form field was selected. However, you can also map your attributes with a static field or variable.
5. Create a new app definition and associate your process with it.
6. Deploy the app and test it by updating the data. For example:
    * Open your app and click **+ START**. The form fields that you defined in your process appear.
    * Edit an existing Id (column name) with a new customer name and verify if the changes appear in your database.

**Sample database table**

While working on the data model functionality, locate or create a database table and its columns from your database and make sure to create matching attributes in your Data Model. For example, the following customer table was used for the customer data model in the above sections.

![Datamodels_5]({% link process-services/images/Datamodels_5.png %}){:height="350px" width="600px"}

## Create data models for folders

You can map entities to the Alfresco Content Services repository to create data models for Alfresco Content Services folders.

### Configure the data source

Before defining a data model for Alfresco Content Services folders entities, you need to establish a repository connection and register the data source in your tenant.

1. In the Identity Management app, click **Tenants** then **Alfresco Repositories**.
2. Click **+** and set the followings:
    * **Name** - Name of the Alfresco Content Services repository, for example, local
    * **Repository Base URL** – This is the base URL for the repository, for example, `http://localhost:8080/alfresco`
    * **Share Base URL** – This is the base URL for the Alfresco Share installation, for example, `http://localhost:8080/share`
    * **Alfresco version** – The version of the Alfresco Content Services repository, usually version 4.2 or higher
3. Click **Save**.

### Define folder entity data models

Once you've configured the data source you can define folder entity data models.

1. Select the **Alfresco** Data Model type.

    This loads the repository source menu.

2. Select **Repository source** then click **Add entity** to add an entity that maps to custom folder node in the repository.

3. Give the entity a name, such as Custom Folder.

4. Specify the node type, including any aspects that should be applied. In this example select **TODO**. This is an instruction to create the folder with a custom type.

    **Tip:** Use commas to separate type and aspects.

    >**Note:** Use the `F:` prefix for the type as it's a custom type.

5. Specify any custom aspects to apply and any out-of-the-box aspects if needed, for example `cm:titled`.

    >**Note:** These are also referred to as secondary types in the CMIS standard.

6. After you've entered the type and aspects definitions, specify all other relevant properties. There following properties are mandatory:

    * `cmis:name` (or `cm:name`) - used to specify the name of the new node
    * `cmis:parentId` - used to specify what parent node the new node should be created under

    When creating a new entity the Data Model designer automatically creates the required fields as well as the most commonly used attributes:

    |Attribute Name|Content Services Property|Entity Time|
    |--------------|-------------------------|-----------|
    |ID|`sys:node-uuid`|string|
    |Name|`cm:name`|datasource.driverstring|
    |Title|`cm:title`|datasource.urlstring|
    |Created|`cm:created`|date|
    |Creator|`cm:creator`|string|
    |Modified|`cm:modified`|date|
    |Modifier|`cm:modifier`|string|
    |Parent|`cm:parentId`|string|

    All folder entities require at least one attribute that maps to the `cm:name` property. It can also map to the `cmis:name` property, if you prefer to use CMIS property names.

7. After the entity and the default attributes are generated, click **Add Attribute** to add entities to map the remaining folder properties.

8. When you're done, click **Save**.

## Import content models

With Alfresco Content Services you can define and use custom content models using either XML or the Alfresco Share Model Manager. You can import content models and use them in your data models.

See [Model Manager]({% link content-services/latest/config/models.md %}) for more details.

1. Export the model from Alfresco Content Services.

2. Unzip the downloaded file.

    This creates a folder with two XML files.

    * the content model definition, with a file name similar to <content model name>.xml
    * the content modeler configuration file with a file name similar to `CMM_<content model name>_module.xml`. This is only required for re-importing a model into Alfresco Share so isn't relevant for the import operation.

3. In the App Designer select **Data Models** and create a new (or edit an existing) folder data model.

4. On the Entities list click **Import**.

    This prompts you to select the content model file.

5. Go to the location of the unarchived file and select the content model file, for example, `healthCareModel.xml`. Ignore the `CMM<mode name> _module xml` file.

    ![data-model-select]({% link process-services/images/data-model-select.png %})

6. Click **Open** and the corresponding entry and attributes are created.

    ![data-model-create]({% link process-services/images/data-model-create.png %})

    Unlike database schemas, importing a content model doesn't overwrite an existing entity if it's currently selected. If the name already exists then an error will be displayed. If it doesn't exist then a new entity is created with the content models using the type name (`<type name=”.. >`) as the entities name.

    You need to activate the content model in Alfresco Share to use it in deployed process applications.

## Using folder entities in process applications

When you've created a folder data model, you can use it in several ways.

* Create a folder entity in the Alfresco Content Services repository with the folder metadata
* Update an existing folder entity in the Alfresco Content Services repository using the Store Entity Task
* Retrieve and display the folder entity and its related metadata in a form

### Create folder entities

You can create an Alfresco Content Services folder entity in Alfresco Content Services repository with the folder metadata.

1. In the App Designer create a new or open an existing process in the BPMN Editor.

2. Create a new BPMN process and add your logic to collect the folder entity data.

    This is usually a form with the appropriate fields, as in the following example. This example uses a form to provide the Name, Description, and Title for the folder entity and under the parent folder, and is used as the referenced form of the start task.

    ![data-model-sample-form]({% link process-services/images/data-model-sample-form.png %})

3. From the Components List of the BPMN Editor, drag and drop a **Store Entity Task**.

4. Select the Store Entity Task and make it a Create Folder.

    ![data-model-entity-task]({% link process-services/images/data-model-entity-task.png %})

5. Click on the **Attribute Mapping** property.

6. From the Mapping Configuration screen select the relevant data model. In this example the Simple Folder Model is used.

7. Click **New variable** to store the result of creating an folder entity. In this example MyF is used.

    This can be used in expressions, parameters, and other mappings later on in the process. Use this variable to retrieve the ID of the folder entity for future operations such as update or retrieve.

8. For each folder data model attribute listed in Attribute name, select a form field to use for mapping the form fields to the attributes to be stored. You can also select process variables, but in this example the values from the form are used.

9. Leave the Id attribute empty.

    This indicates to the task that a new folder should be created. Specifying the Id updates an existing folder.

10. Enter a Name attribute to be used as the name of the new folder.

11. Click **Save**.

    ![data-model-attribute-map]({% link process-services/images/data-model-attribute-map.png %})

12. Save the process then publish and deploy the application.

13. Start a process and enter the details in the start form.

    ![data-model-process]({% link process-services/images/data-model-process.png %})

14. Click **Start Process**.

    The new process instance is created. You can sign in to Alfresco Share and see the new folder created, and see that in the properties the Name, Title, and Description are set to the values entered in the form.

    ![data-model-share]({% link process-services/images/data-model-share.png %})

### Configure the folder entity parent

To create a folder entity you need to provide a parent for the entity parent folder. This can be configured in three different ways.

1. As part of an end-user form

    1. Specify the folder entity parent as in [create folder entities](#create-folder-entities).

    2. In the Form Designer drag and drop the new **Attach Folder** field.

        ![data-model-attach-folder]({% link process-services/images/data-model-attach-folder.png %})

    3. Click the configure option ![ico-configure]({% link process-services/images/ico-configure.png %}){:height="18px" width="18px"} for the new field to display the Field Configuration screen.

    4. Click **Attach Folder options**.

        ![data-model-add-folder-options]({% link process-services/images/data-model-add-folder-options.png %})

    5. Enter the Repository source.

        This is the Alfresco Content Services repository where folder entities will be stored.

    6. Click **Select folder** for the Start folder and select a parent folder.

        This is the folder under which the folder entity will be stored.

        You can choose whether to allow users to change the default value and select a new folder. This means the user can select folders in collaborative processes where folders are available. This also allows administrators to provide folder-based grouping of content. For example, the administrator can define a number of different folders for each region.

        Alternatively, you can hide this field and enforce a single parent throughout the process application.

2. Default parent setting via a configuration process

    This is a variation of the previous method. The parent folder is created and stored as the default for other processes to store all their folder entities.

    1. Create a form to use to configure the parent folder.

    2. Use variable mapping to map the Attach Folder field to a process variable, for example `folderParent`.

    ![data-model-variable-mapping]({% link process-services/images/data-model-variable-mapping.png %})

    You can now use the default folder parent value in various ways, including:

    * Storing it as a persisted configuration setting and using in other processes
    * Mapping it to a model attribute in the Store Entity task

    ![data-model-map-to-model]({% link process-services/images/data-model-map-to-model.png %})

    This method stops the user from knowing the details of where the entity is stored. You'll need to create a process starting with a form that allows the user to select a parent folder.

3. Programmatically

    The previous approach is possible because parent folder information is stored in a process variable as JSON, for example:

    ```json
    { "path":
      { "id": "47cb278d-c775-444f-a23e-b9f2d92390da",
        "title":"documentLibrary > my-folder",
        "folderTree":[{"id":"ec5eb0ec-76a0-4175-adbf-dcf3842ed00c","title":"documentLibrary","simpleType":"folder","folder":true},
                      {"id":"47cb278d-c775-444f-a23e-b9f2d92390da","title":"my-folder","simpleType":"folder","folder":true}]
      },
      "account":
          {"id":"alfresco-1",
           "name":"local"},
      "site":
          {"id":"health-care",
           "title":"health care"}
       }
    ```

    The Store Entity task can recognize the JSON format and extract the values needed. Process developers can construct the parent folder dynamically in code, scripting, or expressions, and store it in a process variable.

### Update folder entities

Updating a Alfresco Content Services folder entity is similar to creating one using Store Entity tasks, with different key mapped fields.

1. In the App Designer create a new or open an existing process in the BPMN Editor.

2. Select **Start** and click on the reference form.

3. Create a form similar to those created in [create folder entities](#create-folder-entities).

    ![data-model-update-form]({% link process-services/images/data-model-update-form.png %})

4. Click **Save and Close** to return to the BPMN Process Editor.

5. From the Components List of the BPMN Editor, drag and drop a **Store Entity Task**.

    ![data-model-update-form-flow]({% link process-services/images/data-model-update-form-flow.png %})

6. Click on the **Attribute Mapping** property.

7. From the Mapping Configuration screen select the relevant data model. In this example the Simple Folder Model is used.

8. Select a previously created variable holding a folder entity or click **New variable** to store the result of updating the folder entity.

9. For each folder data model attribute listed in Attribute name, select a form field to use for mapping the form fields to the attributes to be updated.

    Unlike the creation operation, the Id attribute is required to update the folder entity. Alternatively, you can supply the parent folder and name of folder instead of the folder id. When you supply a folder id and folder name this renames the folder.

    ![data-model-update-folder]({% link process-services/images/data-model-update-folder.png %})

10. Click **Save**.

11. Save the process then publish and deploy the application.

12. In the application start a new process.

13. Select the parent folder of the folder entity and type in the name of the folder you want to update.

14. Type in a new description and title and click **Start Process**.

    You can sign in to Alfresco Share open the folder to see the updated Title and Description.

### Retrieve and use a folder entity

As with other data models, there are two ways you can retrieve Alfresco Content Services folder entities and 
use them in a process or decision table.

1. Using the form field to data model mapping

    Using the **form field to data model mapping** property in a start or user task to map the form fields to the models attributes. Follow the same process described in [Using the data model in a process](#using-the-data-model-in-a-process).

2. Using variables obtained from Stored Entity tasks

    When creating or updating folder entities, the entity can be stored in a variable.

    >**Note:** `MyF` and `GetMyFolder` were the examples in [create folder entities](#create-folder-entities) and [update folder entities](#update-folder-entities).

    These variables can then be used in the process expressions and parameters, forms, or decision tables. To use a variable in a form:

    1. Extend the example you created in Updating folder entities by adding a User Task action.

    2. Create a new form display folder.

        ![data-model-retrieve-folder]({% link process-services/images/data-model-retrieve-folder.png %})

    3. From the form control toolbox drag and drop a Display Value field.

    4. Use the field configuration to select the variable.

        >**Note:** The `myGetFolder` variable is an object with all the model attributes listed.

    5. Select a Name and Description.

        ![data-model-retrieve-variable]({% link process-services/images/data-model-retrieve-variable.png %})

        ![data-model-display-folder]({% link process-services/images/data-model-display-folder.png %})

    6. Click **Save**.

    7. Save the process then publish and deploy the application.

    8. Create a new process and then [create folder entities](#create-folder-entities) and [update folder entities](#update-folder-entities).

        After updating the folder entity a new task is created which uses the Display Folder name to show the entity attributes.

        ![data-model-new-display-folder]({% link process-services/images/data-model-new-display-folder.png %})
---
title: Configure Data persistence
---

When you build a process you use Form variables and declare Process variables. You can either give values to these variables or you can allow a user to give values to them once the process has started. 
Once the process has completed however, all these values are stored in your database but are no longer needed. You can use the Data persistence functionality to free up space in your database when creating a process, and remove this redundant data.

1. Create a new process.

2. Click Data persistence.

    ![data persistence]({% link process-services/images/data-persistence.png %})

3. Once you have clicked on Data persistence you are presented with several configuration options. Select the one that best suits your requirements. 

    ![change value]({% link process-services/images/change-value.png %})

    * **Save All** Selects all variables that are used in the process and stores them in the database. Select this option if it is important for your organization to be able to revisit the input variables at a later date. Provides the lowest database performance. 
    * **Save specified processes** Allows you to select what input variables to persist in the database. Provides higher database performance.
    * **Don’t Save any** All variables used in the process will be deleted from the database. Select this option if is not important for your organization to be able to revisit the input variables at a later date. Provides maximum database performance. This option leaves an initiator that describes when the process started and ended, for example, `45095`, `45094`, `45094`, NULL, `initiator`, `string`, `0`, NULL, NULL, NULL, `2`, NULL, `2022-01-25 13:37:52.373`, `2022-01-25 13:37:52.373`.

4. If you select the **Form Fields** heading and you can select which processes are to persist in the database. Select the process from the left pane and use the buttons in the middle to configure how they are handled. 

    ![form button]({% link process-services/images/form-button.png %})

5. If you select the **Process Variables** heading you can select which process variables are to persist in the database. Use the radio buttons on the right to configure how they are handled. Click **Save**.

    ![form radio]({% link process-services/images/form-radio.png %})

When you have finished you can see how many properties you have selected not to persist.

![not persisted]({% link process-services/images/not-persisted.png %})












---
title: Using business rules (decision tables)
---

There are many situations in a business process where you wish to evaluate some data you have collected and come to some conclusion or decision. Business rules provide a natural way to express the logic of decision making. Typical decision examples are calculating discounts, credit ratings, who to assign tasks to, what service level (SLA) to use, and so on.

There are business rule systems that are hugely complex and intended for a wide range of uses. You can, of course, integrate Process Services to these systems if they provide what you need. Often, within a business process, the rules can be very focused and need to be managed by business users. This is where Process Services decision tables provide a natural solution.

In a decision table you only test, set and create variables using a set of business rules. There are no other side effects possible, such as calling out to external systems, because these are not needed: a process can do all this using the full range of its BPM capabilities before or after a Decision Table task.

You can think of a Decision Table as a spreadsheet that allows you to define a row for each business rule, with columns representing each variable that needs to be tested or set. There are two parts to a rule: the *conditions* (**if** they all match, the rule "succeeds") and the *conclusions* (**then** set some values). In each cell of the table there can be a value expression that is used to try and match against variable’s values, or to calculate the value to set. When a Decision Table is evaluated, it tries all the rules in turn (so ordering of rules matters), testing and setting values. Depending on how you want the rules to be interpreted, you can set the rules to stop as soon as one rule matches and succeeds in setting its values, or to run through all the rules, setting values for every matching rule. If it runs through all rules, you can think of the last successful rule winning, as it may overwrite values that were set for the same variables in other successful rules.

Decision tables follow the [Decision Model Notation (DMN) specification](http://www.omg.org/spec/DMN/1.0/){:target="_blank"}.

In the following, we will create a simple process that makes use of a Decision task and its Decision Table. We will use the [BPMN editor]({% link process-services/latest/using/process/bpmn.md %}), but you can just as well use the [Step editor]({% link process-services/latest/using/process/step.md %}) to achieve the same result.

First let’s take a look at the process we want to create:

![decision-process]({% link process-services/images/decision-process.png %})

In this "Annual Work Review" process, a user can enter the details of his or hers achievements for the current year, and if the work efforts have gone beyond the employee’s obligations a bonus will be given and an email sent notifying the user about it. The logic to decide if a bonus should be given or not is implemented using a Decision Table in the "Calculate bonus" Decision task above. Before we take a look at the Decision Table itself, let’s quickly take a look at the tasks before the "Calculate bonus" Decision task.

The process' start form is shown below and defines 4 fields: `obligationsCompleted` (boolean), `additionalAchievements` (string), `completedDate` (date) and `dueDate` (date). See the [Form editor]({% link process-services/latest/using/process/form.md %}) section for more information on how to create forms.

![decision-process-start-form]({% link process-services/images/decision-process-start-form.png %})

The second task in the process is a "Script task" that we are using to load some demo user data. It has format *javascript* and declares 2 variables: `yearsOfService` (integer) and `salary` (integer) in the **Variables** property dialog. In the **Script** property dialog for the script task the following code has been added to get some employee data:

```javascript
execution.setVariable("salary", 1000);
execution.setVariable("yearsOfService", 5);
```

Now we are ready to create our Decision Table that will have all the input values it needs to decide if a bonus should be given or not. The decision task is created by dragging and dropping a "Decision Task" from the "Activities" section in the editor palette. The only mandatory property is the "Referenced decision table" property in which you should choose "New decision table". Enter "Calculate Bonus" as the name and click the "Create decision table" button to be taken to the decision table editor, as shown below.

![decision-table-editor]({% link process-services/images/decision-table-editor.png %})

Before starting to look at the details of the editor, let’s start by looking at the rules that we want to create to decide if a bonus should be given or not. The logic (or the rules) we will create can be seen in the Decision Table below:

![decision-table-editor-rules]({% link process-services/images/decision-table-editor-rules.png %})

The logic can be summarized as:

* IF the user has completed the obligations AND has performed additional achievements AND has worked for the company more than 5 years AND completed the obligations 3 months before the due date
    * THEN the bonus is 5% of the salary
* IF the user has completed the obligations AND has performed additional achievements
    * THEN the bonus is 3% of the salary
* IF the user has completed the obligations AND has worked for the company more than 5 years
    * THEN the bonus is 3% of the salary
* IF the user has completed the obligations AND completed the obligations 3 months before the due date
    * THEN the bonus is 3% of the salary
* IF none of the rules above matched (empty cells are treated as an automatic match)
    * THEN the user gets no bonus

The expressions in each cell is an MVEL expression. MVEL is an embeddable scripting language that you can read more about [here](http://mvel.documentnode.com/){:target="_blank"}. Note though that you don’t have to write MVEL syntax yourself but can use the edit icon in each cell to display a structured expression dialog where you can create these expressions through a simple interface. Once you are familiar with the syntax you can just enter them directly in the cells, like editing a spreadsheet.

>**Note:** By default it is NOT possible to type in any MVEL expression, but only a sub-set that is supported by the structured expression editor. If you want to be able to write more complex MVEL expressions, you may do so globally by your system administrator setting the `validator.editor.dmn.expression` property in `activiti-app.properties` to `false`. By disabling the default validation you will be able to run any MVEL expression, but you will not get the same help validating that your syntax is correct. Also, you will get a warning message in the structured editor when trying to open an expression it isn’t able to recognize.

Even if you don’t know MVEL, most expressions are self-explanatory. The complex date expression `< fn_subtractDate(dueDate,0,3,0)` probably requires a small explanation though. A custom calculation for dates is
used that takes the `dueDate` as the first parameter and then will calculate a date value by subtracting from it the last 3 parameters for `years`, `months` and `days`. In this case the expression checks if the `completedDate` is 3 months before the due date.

Now create the decision table for yourself. The first thing you need to do is add four input expressions using the Add input button in the Decision Table editor. For each of these, select the process variable or form field to use as input for the column. When adding `yearsOfService` it should look like the following.

![decision-table-input-expression]({% link process-services/images/decision-table-input-expression.png %})

Then you need to add an output column by clicking **Add output**, making sure the dialog looks as below to create a new process variable named `bonus`.

![decision-table-output-expression]({% link process-services/images/decision-table-output-expression.png %})

Time to add our rules. Feel free to type them directly into the cell or use the structured editor (which pops up when clicking the edit icon to the right in each cell). Below you can see how the structured editor looks like when adding the date expression from above.

![decision-table-expression-date]({% link process-services/images/decision-table-expression-date.png %})

When done, click **Validate** to make sure your decision table doesn’t contain errors. Note that once you click **Validate**, the editor will validate your table for every change you make. When you’re happy with your table, click the save icon. You will be prompted to give a "Decision Table key" which can be any value unique to the process.

Back at the BPMN editor add an "Exclusive gateway" and from it add a new "End event" by clicking the circle with the thick border. Select the arrow that connects them and enable the "Default flow" property.

Now drag and drop a "Mail task" and set its "To" property’s "Fixed value" to `${emailBean.getProcessInitiator(execution)}` so it sends the email to the initiator of the process. Then enter values for its "Subject" and "Text" (or "Html") properties. Add a sequence flow arrow to connect the gateway to the email task and make sure to set its "Flow condition" property to have an advanced condition as in the image below.

![decision-process-gateway-condition]({% link process-services/images/decision-process-gateway-condition.png %})

Finally, draw the sequence flow arrow from the mail task to the end event.

We are now ready to use our Decision Table in the Task app. Once you have deployed your process, start an Annual Work Review process by entering the following details in its Start form and click **Start Process**.

![decision-process-start]({% link process-services/images/decision-process-start.png %})

The process detail view is displayed as shown below. After a decision table is executed in a process, it is listed in the Executed Decision Tables section. If something caused the decision table to fail during execution, a red icon with a message is displayed stating an error occurred. Click the **Calculate Bonus** decision table in the user interface to see details about the decision table and its evaluation.

![decision-process-details]({% link process-services/images/decision-process-details.png %})

A decision table is a bit like a black box. You can see the history of it when it was executed. In the image below you can see the audit trail of the decision table.

![decision-process-table-audit]({% link process-services/images/decision-process-table-audit.png %})

An input cell marked with a blue border indicates that the expression in the cell matched the input value. If a cell border is red it means it did not match. If it has no border it means it wasn’t evaluated at all (for example, a previous cell had failed to match and is shown as red). If an exception occurs during evaluation it is also marked with a red border, but also with a red error icon in the right part of the cell.

An output cell only displays the value that was set by its expression. A blue border indicates that it was successfully set. A red border indicates an error occurred during execution of the cell expression. For tooltip information, position your cursor over a cell. An example of this can be seen in the image above where the output cell sets the bonus to "30": hover over the cell and the expression used to calculate the value is displayed.

To see a list of all the input values that were provided to the decision table before execution, click the "Input values" section and you will see the table below.

![decision-process-table-audit-input]({% link process-services/images/decision-process-table-audit-input.png %})

To see a list of all the output values that were set by the decision table after execution, click the "Output values" section and you will see the table below.

![decision-process-table-audit-output]({% link process-services/images/decision-process-table-audit-output.png %})

You may have noticed that we haven’t yet mentioned anything about the decision table’s "Hit policy". The hit policy decides "how" the decision table will be executed when rules succeed (a "hit"). In our decision table we have selected "First (single pass)", which means the decision engine will execute all rules in the given order until it has found a rule where all cell expressions match their input values. Then no further rules will be tested and the outcome expressions specified on the successful rule will be used to set the output values.

Empty cells are considered to be an automatic match, meaning that a rule with only empty cells will always be treated as succeeding (a hit). In our decision table we have such a rule in row #5, but with the input we gave, it will find a match on row #4 and the rule on row #5 will never get tested.

If we change the Hit policy in our table to be "Any (single pass)" the result after executing the decision table will be different. The execution evaluate all rows until the last rule, even if it found a rule that matched on a previous row.

Given the rules in our example, the *Any* hit policy does not make much sense, since the result would always be that bonus is set to "0" because the last rule always matches, no matter what input is given.
---
title: Using the Step Editor 
---

The Step Editor guides you through creating a business process through a sequence of simple steps. The processes you create using the step editor do not exploit the full power of BPMN 2.0 like those created by the BPMN editor, but you can use it to design both simple and quite complex process models, without knowledge of BPMN 2.0.

![app-step-editor-1]({% link process-services/images/app-step-editor-1.png %})

The editor has a menu bar with buttons to save your model, validate that the model is a complete BPMN 2.0 model definition, provide feedback to the Process Services team, and to close the editor.

When you open the step editor on a new process definition, you can see the first step, the Process start step is already added to the process diagram for you. When you mouse-over a step, the stop becomes click-able. Click on it, and the details of the step are displayed and can be edited. This design principle is reflected throughout the Process Services app. You can mouse-over and click text areas to modify their content, and variables to change their values. So for the Process start step, you can click on the single Process trigger variable and choose the trigger type:

The editor will guide you in creating your process. For example, when a form is required, it will present you with a list of existing forms and provide you with a button to create a new form.

Below the last step in a sequence, there is a + (plus) icon. Click on this to add a step to your process.

You can move steps around in your process Click in the top-right of the step and the step will be outlined in green, and the + icons will change to green discs.

![app-step-editor-7]({% link process-services/images/app-step-editor-7.png %})

Click the green disk at which you want your highlighted step to move, and the step is moved to that position in the flow:

![app-step-editor-8]({% link process-services/images/app-step-editor-8.png %})

In addition to the Process start step, there are five types of step you can add to your process.

## Create a process

To create a process definition / model with the **Step Editor**, follow these steps:

1. Select **App Designer** from the Activiti App dashboard.
2. Select **Create Process**. The **Create a new business process model** dialog box appears.
3. Give the process model a name and a description, 
4. Then select the **Step Editor** as the Editor type.
5. Click **Create new model**. The **Step Editor** page is displayed.
    By default, **Step Editor** includes a number of **Steps**, however this depends on the **Stencil** that you selected for editing the process model.
6. Click **Process start** to expand and start by setting the process trigger to User filling a form.

    ![8]({% link process-services/images/8.png %})

7. Click **Create form** to create a new form or select an existing form from your **Forms** library. The **Form Editor** is displayed.

    ![7]({% link process-services/images/7.png %})

    >**Note:** Any form that’s created this way will not be available in your Forms library because it was created as part of this process model. To create a form that you can reuse in other process models, you must create it from the main **Forms** page. In this example, the form is defined in the **Step Editor**.

    The Forms editor has the following tabs:

    * **Design** - Define the layout of form fields from the palette.
    * **Tabs** - Customize tab names to display in the form.
    * **Outcomes** - Define the outcome buttons for the form.
    * **Style** - Define the style (css) for the form elements. For example, adding the following style in the Style panel will convert the field background to blue:

        ```json
            .fields {
            background-color: blue;
        }
        ```

    * **Javascript** - Define javascript code for an element in the form. For example:

        ```javascript
        // __var currentUser = scope.$root.account;__
           __console.log(currentUser);__
          __alert ("Hello World!");__
        ```

    * **Properties** - Define custom properties (metadata) for the form. This is particularly useful when using a custom form renderer (Jave API or Rest API) to retrieve the properties.
    * **Variables** - Define variables in the form.

        You can design the form layout by dragging and dropping the required field type from the palette on the left to the form editor.

        ![pallete]({% link process-services/images/pallete.png %})

        For each field dropped in the **Design** area, you can hover over it and edit the field properties using the pencil icon. Alternatively, click **X** to remove a field from the form.

        >**Note:** The options that become available in the edit view are determined by the field type selected from the palette. For example, a checkbox field has General, Visibility, and Style tabs, whereas a radio button field type might have an additional tab called Options.

        Add labels for the selected fields. Optionally, you can reference a display label with the value entered by a user running the process. In addition, you can also define if the field is required to be filled before the form can be completed.

        ![10]({% link process-services/images/10.png %})

8. When you’ve finished designing the form, click **Save**. You’ll be returned to the **Step Editor**.
9. Click the **+** (plus) icon at the bottom of the **Process start** box to add the first step in your process. The steps available to you are defined by the **Stencil** you associated the model with. The default stencil includes a **Human step** that can be used to assign a task to the user.
10. Select the **Human step** and fill in a name within the step box that you just created.

![11]({% link process-services/images/11.png %})

![12]({% link process-services/images/12.png %})

You can also specify who this task should be assigned to. For example:

* Someone who initiated the process
* A single user
* A set of candidate users or depending on the type of account, a group of users.

>**Note:** When a task is assigned to a group or a list of candidate users, all of those users can see the task in their tasks list, however to complete the task they must claim it first.

### Assign tasks to a process

To simplify a process, assign all tasks to the process initiator (i.e. the person who started the process)
so that you can run the process and have the tasks assigned to yourself.

1. Click **Forms > Create Form**. The **Create a new form** dialog box appears.
2. Enter a form name and click **Save**.
3. Drag a multiline text field and drop it to the form. Name the label as **Review comment**.
4. Click the **Outcomes** tab and then select **Use custom outcomes for this form**.
5. In **possible outcomes**, add the following outcomes and then save the form:
    
    * **Accept**

    * **Reject**

        ![13]({% link process-services/images/13.png %})

        The next step depends on the outcome selected in the previous step.

6. Add a **Choice step** by clicking the **+** (plus) icon below the **Review Project** step.

    ![14]({% link process-services/images/14.png %})

    You can also add additional choices by clicking the **+** (plus) icon in the center of the **Choice step**.

7. Click the relevant choice box to set the condition for the selected choice. The Edit choice dialog appears where you can select the condition based on the existing form fields or outcomes.
8. For the first choice, click **Form Outcome** and select the following values: **Review form > Equal > Accept**.

    ![15]({% link process-services/images/15.png %})

9. Click **Save**. Repeat the same for second choice: **Review form > Equal > Reject**.

    >**Note:** Provide a meaningful name for the choice steps if you can.

10. Add a task that should be done once the project review is accepted by clicking the + under the **First choice** box.

    ![16]({% link process-services/images/16.png %})

11. Now, add a simple human task called **Update Project List**. Under the **Second choice** box, add a human task with a name **Inform Project Leader of Rejection**. The aim is for the process to stop when the rejection task is completed. Therefore, add a **Stop step** to the bottom of this task.

    ![17]({% link process-services/images/17.png %})

12. Continue with adding steps to the **First choice**, or in this case continue to add them after completing the Choice step by clicking the **+** at the very bottom. We’ll just add a Human task with the name Show Project Details.

    ![18]({% link process-services/images/18.png %})

13. On the **Forms** tab for this task, create a new form. Drag a **Display text** field from the palette and enter the text message to display. The text can contain references to values added by a user in previous forms. There is a helper drop down that you can select from to insert the given reference at the cursor position in the text.

    ![19]({% link process-services/images/19.png %})

14. Add some text as shown. Then drag a **Display value** field from the palette and set it to display the project files by selecting the appropriate field from the list.

    ![20]({% link process-services/images/20.png %})

15. Save the form to return to the **Step Editor**. In addition, save the process model you’ve just designed.

All your processes are listed with a thumbnail of the process. You can edit a process from the list by clicking **Visual Editor**. For any additional information about a model, click the thumbnail itself or the **Show Details** button on the top right corner of the thumbnail. This takes you to the **Details** page for the process model where you can see the preview model as well as the actions that you can perform on it.

![21]({% link process-services/images/21.png %})

**Tips**:

* When you edit and save a model, you can choose for the changes to be saved as a new version.
* Previous versions can be accessed from the **History** popup, as can any commentary from the **Comments** popup, where you can add further comments.
* Other action buttons are self-explanatory such as deleting, starring (favorites), sharing, and downloading the model.

### Create a process app to host the process

Now that we have a process defined, it will need to be hosted in a so called Process App, which in turn is published to the Dashboard. Let’s create a Process App using the **Apps** page.

1. Click **App Designer** on your dashboard then click the **Apps** tab and select **Create App**.
2. Select an icon and theme for the tile. You can have an app without any process definitions linked to it, which lets you create a simple custom task list.
3. Click **Edit included models** to use the process we’ve just defined, and select from the lists to add a model.

    ![22]({% link process-services/images/22.png %})

4. Save the app and select the option to publish the app in the **Save** dialog to return the Apps list view.

    You can do similar actions on an app in its **Details** page for all models, such as deleting and sharing. You can also publish the app directly instead of doing it via the Save dialog. Publishing an app makes it available to everyone you’ve shared it with to add to their landing page. Let’s add it to our landing page so we can see our process in action.

5. On your landing page, click the tile with the + (plus) icon. The Add app to landing page dialog appears.
6. Choose the apps you want to add and click **Deploy**. A new tile will be added to your landing page.

## Manage Processes and Tasks

To work with process instances and task instances created from a process model you use the **Tasks** and **Processes** applications.

### Start a process

1. Click **+ START** in the menu bar area. A list of available processes are displayed, which in our case will be only one. When you select it, the Start form we created above is displayed. You can also change the name by clicking the title on the right panel. By default the current date is added to the name of the process.

   ![27]({% link process-services/images/27.png %})

2. Fill in the form and click **Start Process**.

   You will be returned to the **Processes** page, showing the details of the newly started process in your process list.

   ![29]({% link process-services/images/29.png %})

   You can always view a process to see what the current and completed tasks are, as well as add comments that will be available for anyone involved in the process at any stage. If you go to the **Task** page that we just created, you will see the first step in the process is that of a task to review the project, and accept or reject it. The task was assigned to you because it was set to the process initiator, and you started the process.

   ![30]({% link process-services/images/30.png %})

   Before you fill in the review summary and choose accept or reject, you can still add people, documents, and comments by clicking on the **Show details** button in the task header area. You can get back to the form from there by clicking the **Show form** button. If you click the **Accept** button, the **Review Project** task will disappear and instead a new task, **Update Project List** will appear. This is because you defined it as the next choice step in the Step Editor, if the choice was to accept the project. You can just click the **Complete** button to move to the next step, which is a task to show the details of the accepted project.

   ![31]({% link process-services/images/31.png %})

### Manage tasks

1. Click **Tasks** in the menu bar area. This will only show the tasks created within this app or as part of the processes from the app.
2. Click on the hint box next to James to create a task and fill in some text. You will now have a task in your task list.

   ![24]({% link process-services/images/24.png %})

3. Complete a task by clicking **Complete**. The task will no longer be available in your task list. Before you click Complete, you can do a variety of things with a task, such as give it a due date or assign it to someone else.

   ![25]({% link process-services/images/25.png %})

   When you involve someone else in a task, it will appear in their tasks list. This enables them to contribute to the task such as add comments, documents, and even involve more people. However, only the person who is assigned the task with can actually complete it. In the following example we’ve added a document, a comment, and involved a person.

   ![26]({% link process-services/images/26.png %})

4. Click **Complete**. If you wish to view that task again, you can click the **Completed Tasks** filter on the left pane. By default, you will see all tasks you are involved with, however you can customize your view to:

    * Tasks that are directly assigned to you
    * Tasks where you are listed as a candidate
    * Tasks that belong to the group you’re member of

    >**Note:** Not all user accounts may have groups assigned.

    Now that the tasks have been created, let’s start the process we designed earlier.

When you complete this task, your task list and your process list will be empty. If you prefer to see all your tasks and processes in one place rather than through different process apps, you can use the **My Tasks** tile to get your complete task and process lists.

### Using Involved Tasks

As well as allowing individual collaboration on a task, you can also involve groups. You can use this feature as an alternative to manually selecting multiple individuals when involving them with a task.

Use these instructions to extend task involvement to include groups of users.

1. Click **Task App**.

    ![task-app]({% link process-services/images/task-app.png %})

    The Tasks App screen is displayed and the involved **Tasks** option is highlighted.

    ![tasks]({% link process-services/images/tasks.png %})

2. Create a new Involved Task.

    1. Enter the task name in the **NAME** field.

    2. Click **CREATE**.

    The new Involved Task is displayed.

    ![involved-task]({% link process-services/images/involved-task.png %})

3. Click **Invite groups of people and start collaborating**.

4. Specify the name of the group you want to collaborate with on the task.

    ![report]({% link process-services/images/report.png %})

    If the group exists, the matching group name is displayed on the screen.

    ![groupname]({% link process-services/images/groupname.png %})

5. Select the matching group.

    ![add-group]({% link process-services/images/add-group.png %})

6. Click **Groups +** to add more groups.

    ![add-more-groups]({% link process-services/images/add-more-groups.png %})

7. Click **Complete** to complete the group involved task.

## Different types of steps

The following section goes through the different types of steps you can use. The types of step are:

* [Human](#human-step)
* [Email](#email-step)
* [Choice](#choice-step)
* [Sub process](#sub-process-step)
* [REST call](#rest-call-step)
* [Generate document](#generate-document-step)
* [Decision](#decision-step)
* [Content-related](#content-related-step)

### Human step

A human step is a task to be completed by a user. You choose who to assign the task to, provide a form for that user to complete, define a due date for the task, and set a timer. If a timer is triggered, it will allow Process Services to take an action related to the task, such as reassign it to another user and so on.

The Human step dialog is divided into four tabs:

* [Details tab](#details-tab)
* [Form tab](#form-tab)
* [Due date tab](#due-date-tab)
* [Timer tab](#timer-tab)

#### Details tab

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element|
|Name|A name for the task.|
|Documentation|A description of the task.|
|Assignment|Configure to who this task should be assigned. You can assign the task to one of the following assignees:<br><br>**Assigned to process initiator**<br><br>The user that started the process instance, which could be you, or a user you have shared the process definition with. The process initiator is the default assignee.<br><br>**Assigned to process initiator’s (primary) group manager**<br><br>The group manager of the user that started the process instance.<br><br>**Assigned to single user**<br><br>When selected, an additional Assignee field is displayed enabling you to search for a single user or select someone using an email address. If that person is not currently an Process Services user, they will receive an invite.<br><br>**Assigned to group manager**<br><br>When selected, an additional Group field is displayed enabling you to search for a group manager or select a form field (providing you have defined a form). Only users that have a primary group defined will have a group manager. You can define a primary group via **Identity Management** > **Users** > **Select an action** > **Change primary group**.<br><br>**Candidate users**<br><br>When selected, an additional Candidates field is displayed enabling you to add one or more candidates. You can add Process Services users or select someone using an email address. If that person is not currently an Process Services user, they will receive an invite. All of the selected candidates are eligible to complete the task. The task will show up in their *Queued tasks* task list. The task is not assigned until they have claimed it, which will make the user the assignee.<br><br>**Candidate groups**<br><br>When selected, an additional Groups field is displayed enabling you to add one or more groups of Process Services users. The task will show up in their *Queued tasks* task list. The task is not assigned until they’ve claimed it. The other users won’t see that task in a task list anymore.<br><br>**Allow process initiator to complete a task**<br><br>When checked, the user that started the process instance (process initiator) can complete the task. This is checked by default. This option is available only for Candidate Groups, Candidate Users, and Assign to single user options.|

#### Form tab

You can select a form to display when the task runs. You can select an existing form, or create a new one. Forms that you create here while designing your process definition are accessible to steps in this process definition only. Forms that you have designed in the Forms tab of the Process Services app can be reused by any process definition owned by someone you have shared the form with. Both types of form are listed in the chooser dialog. You can filter the available list of forms by entering text in the Filter box.

#### Due date tab

If you specify a Due date, then the time remaining until that date will be displayed in the task details when the process is running. If the task is not completed in that time, then the amount of time since the due date is displayed. You have the following options for setting a due date:

* **No due date for this task**

    This is the default value.

* **Fixed duration after creation**

    Specifies a Due date in years, months, days, hours, minutes and seconds after the task is started.

* **Based on field**

    Select a date field from a list of those available in forms of this process definition. You can add or subtract a specified amount of time in years, months, days, hours, minutes and seconds from the value of the chosen date field to create a Due date.

* **Based on variable**

    Select a variable from the list of those available in forms of this process. You can add or subtract a specified amount of time in years, months, days, hours, minutes and seconds from the value of the chosen date field to create a Due date.

#### Timer tab

Timer is similar to Due date, except you specify a time after which some action will be performed on the task by Process Services. You can also specify an action for the task to be taken when the timer completes.

You have three options for setting a timer:

* **No action**

    This is the default value.

* **Reassign task**

    You specify another assignee in exactly the same way as you specify the original assignee on the Details tab. When the timer completes, the task is assigned to the specified user, candidates users, or candidate groups.

* **Keep task**

    When you specify Keep task, a new Timer date reached substep appears inside the current step with the + icon underneath it. You can add one or more subtasks inside this step by clicking this icon. When the timer completes, the task remains active, and the first substep becomes active too. The process continues running substeps as each substep is completed. Note that when you specify substeps here, the list of steps available now includes a **Go to** step. This allows you to choose one of the main process steps to run after this one.

* **End task**

    When you specify End task, a new Timer date reached substep appears inside the current step with the + icon underneath it. You can add one or more subtasks inside this step by clicking this icon. When the timer completes, the task ends, and the first substep becomes active. The process continues running substeps as each substep is completed. Note that when you specify substeps here, the list of steps available now includes a Goto step. This allows you to choose one of the main process steps to run after this one.

* **End the process**

    When the timer completes, all active tasks in the process are canceled and the process ends.

### Email step

When an email step starts in a running process, it sends an email with a fixed text body and a fixed title to a single or multiple recipients.

The email step dialog contains two tabs that let you fully define the task.

Name and Description are simple text fields that help you and others to identify the task in your task list.

Recipient type lets you choose who receives the email defined in this step:

* **Process initiator recipient**

    The user who starts the process is the sole recipient of the email. This is the default.

* **Single user recipient**

    If you choose this option, a Recipient field is displayed to allow you to search for single user or select someone using an email address.

* **Multiple user recipients**

    If you choose this option a second Recipients field is displayed to allow you add one or more users. You can add Process Services users or select someone using an email address.

### Choice step

A choice step enables you to start one of two or more sequences of substeps for your process, based on conditions.

Use the Name and Description fields in the choice step dialog to define the task for your task list.

When you select the Choices tab for a new choice step, it shows two choice boxes. You can use the + (plus) icon between them to add more choices. Click the choice box you to edit the choice and name it.

You can also add from one of the following conditions:

* **No condition**

    This choice runs its sub-steps if none of the other choices conditions are met. Note that only one of the choices in a choice step can specify this condition for the model to validate. This is the default.

* **Form field**

    This choice runs its sub-steps if the value of a field in a form satisfies a conditional statement. If you click this option, the following options are available:

    * Select a field in a form that is used in this process definition.
    * Choose an operator from equal, not equal, less than, greater than, less than or equal to, greater than or equal to, empty, not empty.
    * Specify a value. For example, select a radio button field named **direction** from a form, choose the **equals** operator, and type the value **Left**.

* **Form outcome**

    This choice runs its substeps if the outcome of a form that matches the one specified for the choice is selected by the person assigned with the task. If you click this option, the following options are available:

    * Select an outcome of a form used in this process definition.
    * Choose an operator from equals or Not equals.
    * Select a value of the outcome from the list. For example, select an outcome named **direction** from a form, choose the Equals operator, and choose the value **Turn left** from the drop-down list.

There are two steps that you can add at the end of a substep sequence in a choice step that change the flow of control in the process. See next 2 sections.

#### End process Step

An end process step is available only when defining a substep within a choice step. You use an end process step to stop the process within a choice step in your process definition. Since this is a terminal step, no + (plus) icon appears after the step.

In the **End process step** dialog > **Details** tab, define the task name and description.

#### Goto step

The Goto step is available only when defining a substep within a choice step. You use a goto step to jump to a named step within your process definition. Like the End process step, it is a terminal step and no + (plus) icon appears after it.

1. In the **Goto step** dialog > **Details** tab, type a Name and Description in order to help you and others to identify the tasks in your task list.
2. Select a Goto step in this process definition to follow next.

    The process definition used here illustrates models for driving a car. If you turn left, then you continue your journey. As long as you continue turning left, your journey continues. If you turn right, you drive a short distance to your final destination. The goto step provides two ways of managing the flow of control in a process:

3. You can implement repetition, as illustrated.
4. You can also move the flow of tasks to another step in the current process.

### Sub process step

A sub process step enables you to create a step that itself contains a sequence of steps that constitute a complete process definition. When saved, this definition is added to the list of substeps available to your main process definition. This gives you a method of managing complex processes by refining repeated sequences of steps into a sub step. This can make your process definition easier to comprehend visually.

The sub step dialog contains one tab that lets you fully define the task.

A sub process lets you choose a sub process that you have already defined in this process definition, or you can create a new sub process that is reusable in this process definition.

### REST call step

This step allows you make an arbitrary REST call. You can define a full endpoint directly or use an endpoint defined by an administrator on your Process Services server. You can supply parameters to the call directly in the URL or from process variables in forms, and you can extract properties from the JSON response into process variables for use in your process definition.

>**Note:** A user with administration privileges will need to add endpoints for standard REST calls, with Username and Password pairs that are permitted for basic authentication. An administrator can add these endpoints and authentications on the Tenant page of the [Identity Management]({% link process-services/latest/using/process/index.md %}#identity-management) app. The benefit of using standard endpoints is that they can be easily switched for test and deployment configurations. It is also possible to use a REST step to call the Process Services REST API.

The REST call step dialog contains four tabs that let you fully define the call.

Name and Description are simple text fields that help you and others to identify the task in your task list.

You define the URL for your REST call in this tab.

* **HTTP Method**

    This is the method associated with the REST call. The default is GET, but you must select between GET, POST, PUT, and DELETE based on the documentation for your chosen API call. The example shown in the screenshot, is using the `api/enterprise/app-version` REST call, which is documented as a GET call.

* **Base endpoint**

    You select one from a list of endpoints that have been defined by your administrator. In the example the endpoint for the local Process Services server REST API, `http://localhost:8080/activiti-app/`, has been chosen.

* **Rest URL**

    Copy the URL fragment from your selected REST API call. In this example we are using `api/enterprise/app-version`.

    You may also choose to enter the full URL, especially for REST services that have not been defined by your administrator, for example, `http://httpbin.org/post`. This can be useful during development and prototyping cycles.

    In all cases, you can use the **Test** button to test your endpoint.

    ![ReST call]({% link process-services/images/rest-call.png %})

* **Form Field/Variables**

    You can insert values previously submitted in any form (or variables) in your process definition, into the REST URL. The value will be inserted at the position of the cursor in the Rest url field.

Some REST calls require a JSON request body. You can add one or more JSON properties using this tab.

For each property you define the name, property type and value. The value can either be a fixed value, or you can select the value of a form field from a list of available form fields in your process definition.

REST calls return a JSON response body. You can define one or more pairs JSON response properties and process variables. When the step completes, each process variable will contain the value of the returned response property. You can use those values later in your process. In this example, the returned JSON property edition will be contained in the process variable `activitiedition`, which is a form field in a form used for displaying the edition string later in the process definition.

For complex and nested POST request bodies, specify a JSON Template which is evaluated at run-time. The JSON editor provides syntax highlighting and will highlight any JSON syntax errors on the line number indicator.

![ReST call 2]({% link process-services/images/restcall.png %})

### Generate document step

Use this step to generate a Microsoft Word or PDF document from a template in Microsoft Word. The process step will substitute any variables you place in the template document with process and form variables. You can upload global template documents for use by all users, or upload personal template documents for your own use.

>**Note:** A user with administration privileges can upload global templates. An administrator can add templates on the Tenant page of the [Identity Management]({% link process-services/latest/using/process/index.md %}#identity-management) app.

The Generate Document step dialog contains the following tabs to define the task:

* **Details tab**

    * **Name and Description** - Type the name and description of your task.
    * **Output name** - Type the name of your output document.
    * **Output format** - Click the format that you want to view your generated document: PDF or Word.

* **Template tab**

    Select from a list of company templates that an administrator has uploaded or upload your own personal templates by clicking **Upload Template**. In the above example, the `offer.docx` company template is selected.

    You can also filter the list of company templates with a search string, and download any template to see what form and process variable substitutions are made in the template.

* **Variable tab**

    Enter a variable name that you have used in the document.

    In the template, you can substitute `<<[name]>>` in the output document with the form variable name, for example:

![Doc Template]({% link process-services/images/doc_template.png %})

Templates are processed using the LINQ reporting engine.

You can also use expressions to build more complex templates. For example, the following excerpt was used in an HR offer letter of XXX Corp called *offer-letter.docx*:

```text
    Your initial salary will be <<if [annualsalary > 30000]>>a generous
<<else>>a standard starting<</if>> $<<[annualsalary]>> per year
```

The sample template referred above uses conditional expressions that tests the value of the form variable `annualsalary` and outputs one of the two different text phrases, depending on that value.

To test the *offer.docx* template, create a process definition that uses the template. For example:

1. Create a process with the option started by user filling in a form.
2. Create a form called starter with four fields: a text field with the ID name, a set of radio buttons with the ID department, and two number fields with the IDs annualsalary and annualbonus.
3. Once you have filled the form, the Generate Document step will take the `offer.docx` template (mentioned above) and generate a document with a name defined by value of the Variable tab, `offer-letter.docx`.
4. Create an app to include the process definition that you just defined, and then publish the app.
5. Click **Start Process**. The Generate Document step is executed and the `offer-letter.docx` document is generated.

In this example, the Generate Document step is the last step in the process definition, therefore you can view and download the generated document of the completed process in the Process Services process view.

### Decision step

The decision step enables you to create a Decision Table. A decision table is an easier expression to creating business rules.

See the [Business rules - decision tables]({% link process-services/latest/using/process/rules.md %}) section for more details on Decision Tables.

### Content-related step

Use this section to link create content related steps.

#### Retrieve Alfresco Properties

The Retrieve Alfresco Properties option enables you to retrieve content-specific properties from Alfresco Content Services and map it to a form field or variable, for example, properties of a document. You can retrieve document information after a document is added or referenced via the Attachment form field in the Share Connector.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Alfresco properties|Retrieves Alfresco Content Services properties for content stored in the form editor or variable, and allows mapping them.|

#### Update Alfresco Properties

The Update Alfresco Properties option enables you to update content-specific properties in Alfresco Content Services 
using a form field or variable. For example, you can update properties of a document linked from Alfresco Content Services 
via a form attachment field, or process variable.

The Properties sheet displays the same fields as Retrieve Alfresco properties, except that is used for updating 
properties rather than retrieving.

#### Call Alfresco Action

The Call Alfresco Action enables you to invoke standard Alfresco Content Services actions from Process Services.

>**Note:** Alfresco Actions are asynchronous. This is important to note if you have multiple tasks executing against the same node(s) in Alfresco Content Services. To control a sequence of actions against a node, use a [Service Task]({% link process-services/latest/using/process/bpmn.md %}#service-task) instead.

|Property|Description|
|--------|-----------|
|Id|A unique identifier for this element.|
|Name|A name for this element.|
|Documentation|A description of this element.|
|Content|Retrieves properties Alfresco Content Services for content stored in the form editor or variable.|
|Act as|Identity of the caller: Process Initiator or Specific User. Selecting **Specific User** lets you select a different user. When the Identity Service is configured for Alfresco Content Services and Process Services, a stored token will be used for authentication to Alfresco Content Services.|
|Repository|Changes the repository account. For example: Alfresco Content Services.|
|Action|Lists a range of actions specific to Alfresco Content Services. Select the options to make changes to the default name and value depending on your requirement. The options are as follows:<br><br>**extract-metadata**<br><br>Extracts embedded metadata from files and added to the file properties. Alfresco Content Services supports Microsoft Office document properties, LibreOffice, and a number of other formats.<br><br>**move**<br><br>Moves the files and subfolders to the locations of your choices in Share if you edit the following value with the exact location of your document in Share: `workspace://SpacesStore/<ID>`.<br><br>**add aspect**<br><br>Adds a property aspect to files for additional behaviors or properties.<br><br>**specialise-type**<br><br>Changes a file’s content type, if applicable. For example, you can changes a standard file into a policy document and adds the appropriate metadata for that content type.<br><br>**script**<br><br>Runs a custom JavaScript script from the Data Dictionary/Scripts folder. There are a number of sample scripts available. The list can vary depending on how Alfresco Content Services is configured.<br><br>**check-in**<br><br>Checks in files that are currently checked out. For example, files will be checked in before being moved to another folder. Select the option to indicate whether they will be checked in as minor or major versions.<br><br>**transform and copy content**<br><br>Action for transforming and copying content. You can add copies of files, in the format of your choice, to another location. For example, you can generate a copy of a Word document in PDF format in a different folder.<br><br>**remove-features**<br><br>Removes a property aspect from files to remove functionality or properties.<br><br>**check-out**<br><br>Checks out files automatically with a working copy created in the location of your choice. Select the option to associate a name or type with the file.<br><br>**copy**<br><br>Creates copies of files in the location of your choice. Set the additional deep-copy and overwrite-copy options to true if you want to copy or overwrite sub-folders and their contents.<br><br>**transform-image**<br><br>Action for transforming and copying image files in the format of your choice to another location. For example, you can generate a copy of GIF file in PNG format in a different folder.|

#### Publish to Alfresco

This step enables you to write a document or all documents uploaded in your process to an Alfresco Content Services on-premise repository.

>**Note:** A user with administration privileges will need to add accounts for the Alfresco Content Services repositories that you can publish to. An administrator can add repositories on the Tenant page of the [Identity Management]({% link process-services/latest/using/process/index.md %}#identity-management) app. The list of repositories you can publish to is then shown on your Personal Info page. If you click on a repository, an account to access the repository is added for you.

The Publish to Alfresco step dialog contains three tabs that let you fully define the task.

Name and Description are simple text fields that help you and others to identify the task in your task list.

* **Publish all content loaded in process**

    This is the default. All files that have been uploaded in an upload field in a form before this step are published to the specified location in the repository

* **Publish content uploaded in field**

    If you select this option a second field Form field displays a list of form fields from all the forms in your process. You can select one from the list.

* **Destination**

    This is the folder in an Alfresco repository to which the selected content will be published. Click **Select Folder** to display a dialog that lets you choose a folder from the available Alfresco repositories defined in your Process Services app. Once you have selected a folder, the repository details and folder path are displayed in this field.

* **Subfolder**

    If you check create or reuse subfolder, a second field **Based on field** displays a list of fields from all the forms in your process. You can select one from the list. A folder with a name based on the content of the selected field will be created or reused within the specified destination folder to publish the content selected. If you do not select this option, all the items of content will be published directly to the specified destination folder.

#### Publish to Box

This is similar to the Publish to Alfresco step, but for [Box](https://www.box.com/){:target="_blank"}.

Note that a Box account needs to be configured in the **Identity Management** > **Personal** tab.

#### Publish to Google Drive

This is similar to the Publish to Alfresco task step, but for [Google Drive](https://www.google.com/drive/){:target="_blank"}.

Note that a Google Drive account doesn’t need to be configured. A popup shows up when you have to select a document/folder and no account is found. This popup will allow you to log in with the Google Drive credentials and use this account thereafter.
