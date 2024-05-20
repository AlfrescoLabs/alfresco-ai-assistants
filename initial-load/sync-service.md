---
title: Alfresco Sync Service
---

Alfresco Sync Service is an add-on module that synchronizes files between the desktop and repository using web services. It's part of the Desktop Sync solution that consists of three components: Sync Service, Desktop Sync for Windows, and Desktop Sync for Mac. This documentation describes how to install, configure, and administer the Sync Service.

This release of Sync Service is a compatibility release to support Alfresco Content Services 23.x.

Here is a summary of the key capabilities:

* Clustering for scalability support
* Support for various databases: PostgreSQL, Oracle, MySQL, and AWS Aurora MySQL
* Support for AWS deployment
* Events monitoring for content, Governance Services, and permission changes

> **Note:** The Sync Service module can be applied to Alfresco Content Services. See [prerequisites]({% link sync-service/latest/install/index.md %}) and [Supported platforms]({% link sync-service/latest/support/index.md %}) for more.

The following diagram shows a simple representation of how Alfresco Content Services and the Sync Service interact with the Desktop Sync clients. See [Sync Service architecture]({% link sync-service/latest/admin/index.md %}) for more.

![Simple architecture for Sync Service]({% link sync-service/images/sync-simple-arch.png %})
---
title: Set up clustering
---

There are a number of prerequisites and configuration properties to consider when setting up Sync Service in a clustered environment.

## Prerequisites

For the Sync Service to run in clustered mode, ensure that your Alfresco Content Services instance has a clustering license installed and clustering is enabled.

## Clustering through load balancer

If you're using a load balancer, set the **dsync.service.uris** property to point to the address of the load balancer in `alfresco-global.properties`.

For example, if a load balancer is set up to run on `http://172.29.102.168:9999/alfresco`, modify the `alfresco-global.properties` file to include the following:

```bash
### DesktopSync ###
dsync.service.uris=http://172.29.102.168:9999/alfresco
```

## Clustering properties

Configure the sync server cluster by setting the following properties in the `config.yml` file.

> **Note:** These properties are optional.

| Clustering property | Description |
| ------------------- | ----------- |
| sync.cluster.enabled | *Optional*. This enables clustering. Example setting: true |
| sync.cluster.interface | *Optional*. This specifies a particular network interface to use for clustering. It might be a wildcard value, such as `10.256.*.*`, which means an attempt is made to bind with an interface having an IP address beginning with `10.256`. Example setting: `10.256.*.*` |
| sync.clusterCheck.timeout | *Optional*. This specifies the time to wait for a cluster node ping before marking the node as not alive (ms). Example setting: 4000 |
| sync.hazelcast.password | *Optional*. This specifies the password used by the cluster members to access or join the Hazelcast cluster. Example setting: synccluster |
| sync.hazelcast.port | *Optional*. This specifies the port to use for clustering. Example setting: 5701 |
| sync.hazelcast.autoinc.port | *Optional*. This enables Hazelcast to make several attempts to find a free port, starting at the value of `alfresco.hazelcast.port`. **Note:** It's recommended that you don't use this property. Example setting: false |
| sync.hazelcast.max.no.heartbeat.seconds | *Optional*. This specifies the maximum timeout of heartbeat (in seconds) for a node to assume it is dead. Example setting: 15 |
| sync.hazelcast.bind.any | *Optional*. This specifies if Hazelcast can bind to any/all interfaces. This must be `false` for the `sync.cluster.interface` property to have any meaningful effect. Example setting: false |
| sync.hazelcast.mancenter.enabled | *Optional*. This specifies if the Hazelcast Management Center (mancenter) is being used for cluster management. See the [Hazelcast documentation](https://docs.hazelcast.org/docs/management-center/3.8.4/manual/html/Deploying_and_Starting.html){:target="_blank"} for more information. Example setting: false|
| sync.hazelcast.mancenter.url | *Optional*. This specifies the mancenter URL. Example setting: `http://<host-ip>:<port>/mancenter`. |

> **Note:** Ensure that clocks on all the sync server nodes (cluster members) are synchronized using a tool like [ntp.org](https://www.ntp.org/){:target="_blank"}.

> **Note:** Ensure that all the cluster nodes have the same settings in `config.yml` file, with one possible exception. Only change the `<sync.cluster.interface>` property, if the IP address of the cluster node is specified instead of a wildcard value.

## AWS Auto Scaling groups

An AWS Auto Scaling group monitors your applications and automatically adjusts capacity to maintain steady, predictable performance at the lowest possible cost. Using AWS Auto Scaling, it's easy to setup application scaling for multiple resources across multiple services in minutes.

See [https://aws.amazon.com/autoscaling](https://aws.amazon.com/autoscaling/){:target="_blank"} for more information.

Given that Sync Service is stateless, it can be deployed easily with AWS Auto Scaling groups. However, there are some important aspects to keep in mind.

## General guidelines

* The recommended way to set up the `sync.cluster.interface` property is in the `config.yml` file. This specifies a particular network interface that Hazelcast uses for clustering. It could be a wildcard value, such as `10.256.*.*`, which means an attempt is made to bind with an interface having an IP address that begins with `10.256`:

    ```bash
    sync:
        cluster:
            interface: 10.256.*.*
    ```

    By doing this, all the dynamically started Sync instances will be able to see each other and form a cluster successfully.

* To run various operations on a Sync Service instance via JMX (for example, checking the number of instances in the cluster, running a cluster wide check to ensure that each member sees each other, shutting down the Sync Service etc.), you'll need to connect from a bastion host (i.e. a machine located in the same network as the instance). This is required because the `syncservice.sh` script that's embedded in the `AlfrescoSyncServer-5.0.x.zip` distribution zip doesn't specify a value for `java.rmi.server.hostname`. By doing this, JMX will bind to the private IP, allowing Sync instances to be started dynamically by AWS Auto Scaling groups.
* The last and most important aspect is to ensure that Sync Service is shut down gracefully, by running the `./syncservice.sh stop` command. This will prevent hanging database connections. In addition, this will allow the current sync instance to deregister from the database.

When Sync Service starts, Hazelcast tries to find the other cluster members by performing connections with IPs of previously registered clustered members stored in the database. By deregistering a *soon to be dead* cluster member from the database means a smaller number of connections will be attempted. This should result in faster startup times for Hazelcast and inherently the Sync Service.

Follow the steps listed in the [aws-lambda-lifecycle-hooks-function](https://github.com/aws-samples/aws-lambda-lifecycle-hooks-function){:target="_blank"} GitHub project to correctly run `./syncservice.sh stop` when the instance is terminated, where you'll be using Auto Scaling lifecycle hooks, Lambda, and the EC2 Run Command.

> **Note:** You'll need to modify some of the steps in [aws-lambda-lifecycle-hooks-function](https://github.com/aws-samples/aws-lambda-lifecycle-hooks-function){:target="_blank"}:

1. **Step 1 - Create an SNS topic to receive the result of the backup**

    Skip this step.

2. **Step 3 - Create an Auto Scaling group and configure the lifecycle hook**

    1. Instead of using the User Data to specify the script to install the AWS Systems Manager (SSM) agent, you can manually install it, and then only afterwards, create the necessary AMI.

        See [Manually Install SSM Agent on Amazon EC2 Linux Instances](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-manual-agent-install.html#agent-install-ubuntu){:target="_blank"} to identify the steps depending on the Linux flavor.

    2. Add the lifecycle hooks from the user interface.

    3. Add a lifecycle hook from the Auto Scaling Groups EC2 console.

        Complete the following fields:

        * Lifecycle Transition: Instance Terminate
        * Heartbeat Timeout: 300 seconds

            This defines the amount of time it takes from when the hook is invoked till the instance is terminated - `300s` should be more than enough for the `./syncservice.sh stop` command to run.

3. **Step 4 - Create an S3 bucket for files**

    Skip this step.

4. **Step 5 - Create the SSM document**

    The [EC2 Systems Manager Shared Resources Document](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-ssm-docs.html){:target="_blank"} can be simplified to just execute `./syncservice.sh stop`.

    There's no need to bother with adding code to complete the lifecycle hook, since this is done inside the [Python lambda](https://github.com/aws-samples/aws-lambda-lifecycle-hooks-function/blob/master/lambda_backup.py){:target="_blank"} (see the `abandon_lifecycle` method).

    ```bash
    {
        "schemaVersion": "1.2",
        "description": "Shuts down Sync Service",
        "parameters": {},
        "runtimeConfig": {
            "aws:runShellScript": {
                "properties": [
                    {
                        "id": "0.aws:runShellScript",
                        "runCommand": [
                            "#!/usr/bin/env bash",
                            "sudo /home/ubuntu/service-sync/syncservice.sh stop"
                        ]
                    }
                ]
            }
        }
    }
    ```

5. **Step 6 - Create the Lambda function**

    Make one small change to the Python script.

    1. In `def check_command(command_id, instance_id)`, before checking for the command execution status:

        ```bash
        response_iterator['CommandInvocations'][0]['Status']
        ```

    2. Check if the list is empty. For example:

        ```bash
        if not len(response_iterator['CommandInvocations']) == 0:
        ```
---
title: Sync Service Admin FAQs
---

Here's a list of common questions about administering Sync Service.

## Does Sync Service support Smart Folders

No, this version of Sync Service doesn't support Smart Folders.

## What tools can I use to validate the relative states of the MQ/Sync Service/Desktop Sync data/Alfresco data and the existing sync sets?

To bring the Sync Service and Alfresco Content Services repository in sync, see [Back up and restore Sync Service]({% link sync-service/latest/admin/index.md %}#back-up-and-restore-sync-service). Currently, there are no tools that can validate this.

## What is the starting order of Sync Service?

The sequence in which different Sync Service components should be started is:

1. Postgres
2. ActiveMQ
3. Alfresco Content Services repository (Share)
4. Sync Service

## In the event of a conflict, how do I resolve it?

The [conflict resolution matrix]({% link desktop-sync/latest/using/sync-conflict-guide.md %}) describes how Desktop Sync handles sync conflicts.

## What authentication do Desktop Sync and Sync Service support?

Alfresco Desktop Sync supports SAML authentication with the Identity Service. See the [Single Sign On Guide]({% link identity-service/latest/tutorial/sso/index.md %}) for more details.

Alfresco Desktop Sync also supports basic authentication with Alfresco Content Services where Identity Service is not being used.

> **Important:** Alfresco Desktop Sync does not support [SAML Module for Alfresco Content Services]({% link saml-module/latest/index.md %}). Users can log in with their credentials using basic authentication, but SAML authentication must not be enforced.

## How can I monitor ActiveMQ?

Access the ActiveMQ Web Console using `http://<servername>:8161/admin/queues.jsp`.

Make sure that the:

* name of the subscriber corresponds to the Sync Service ID.
* total number of **Messages Enqueued** is same as **Messages Dequeued**.

For detailed information, see [How can I monitor ActiveMQ?](https://activemq.apache.org/how-can-i-monitor-activemq.html){:target="_blank"}.

For information on ActiveMQ logging, see [How do I change the logging](https://activemq.apache.org/how-do-i-change-the-logging.html){:target="_blank"}.

## How can I monitor Sync Service?

To monitor Sync Service, see [Sync Service health check]({% link sync-service/latest/admin/monitor/index.md %}#sync-service-health-check).

To get detailed logging information on Sync Service, change the logging level in the `config.yml` file as shown below:

```bash
logging:
   level: DEBUG
loggers:
   "org.alfresco.service.common.auth": DEBUG
   "org.apache.activemq": DEBUG
   "com.sun.jersey.api.container.filter.LoggingFilter": WARN
   "org.alfresco.service": DEBUG
```

## Why does the Desktop Sync client connect for content selection then immediately go offline?

If the Desktop Sync client connects to Alfresco Content Services to start content selection then immediately goes offline, folders may already have been created, but no files have been synced; check the following:

* The Sync Service is running
* The Sync Service is accessible from the client - you can use the [Healthcheck URL]({% link sync-service/latest/admin/monitor/index.md %}#sync-service-health-check) in the clients browser
* The global properties file is correctly set up - see [Install Sync Service]({% link sync-service/latest/install/options.md %}#install-with-zip)

For example, if the Sync Service port is not open on the firewall, then the client won't be able to connect to the Desktop Sync service, or the Healthcheck URL. The port is set when installing the Sync Service, where the default is 9090.

> **Note:** Desktop Sync 1.2 (for Windows and Mac) performs a health check which prevents this from occurring.

## What can I check if content can't be added to or updated in Alfresco Content Services via Alfresco Share or another application?

To fix this issue, check if ActiveMQ is running and available to the repository. See [Prerequisites]({% link sync-service/latest/install/index.md %}) for more. A feature of the Sync Service is to provide resilience of the service, and ensuring that no critical event information is lost.

The recommendation is to run an ActiveMQ cluster to ensure high availability.

## Why has sync stopped working since upgrading the client operating system (for example to Mac OS X to Sierra High)?

If SSL has been enabled on the Sync Service without provision for a signed certificate, then the clients may fail to sync content. The log files contain a message "SSL peer certificate or SSH remote key was not OK". [Install the Sync Service]({% link sync-service/latest/install/index.md %}) with a valid security certificate or disable SSL for the synchronization server if required.

## How can I prevent the synchronization of a folder, or folder structure?

You can stop users from synchronizing folders by creating a custom model with an aspect, and then updating the configuration in Alfresco Content Services.

See [Limit folder synchronization]({% link sync-service/latest/admin/index.md %}#limit-folder-synchronization) for more.

## What tools can I use if either the desktop or Alfresco Content Services needs to restored from a backup?

See [Back up and restore Sync Service]({% link sync-service/latest/admin/index.md %}#back-up-and-restore-sync-service).

## Can Sync Service 5.x be used against a repository with Sync Service AMP 4.x installed?

We recommend using the same Sync Service and AMP version for better compatibility.
---
title: Administration overview
---

This information provides an overview of the Sync Service, and helps you to monitor and administer it.

## Sync Service architecture

With Alfresco Desktop Sync, users can sync content between their desktop and the repository. Use this information to find out more about the components of the Sync Service and the flow of information between the repository and the desktop during the synchronization process.

> **Important:** Desktop Sync will replicate content on local desktops for users with the appropriate access. If replication outside the repository is not allowed by your content policy you should not deploy Desktop Sync.

> **Important:** Desktop Sync can't synchronize content that appears in Smart Folders.

The Sync Service synchronizes files between the desktop and the repository using web services. The application currently synchronizes files in the document library of any site a user has access to. Because the content is synchronized automatically between both sides, the users can easily share information between devices. This allows for easy, automatic updates and backup of your data. Share automatically recognizes the updates made to the content via the device and adopts them by synchronizing the data.

### Components of Desktop Sync

The main components of the Desktop Sync application are:

1. **Repository**: This is the repository where the files, indexes, and database resides.
2. **Active MQ**: This is where the Alfresco repository writes messages about changes to the files, folders, subscriptions and device registrations.
3. **Sync Service:** This service keeps a record of all the changes. It manages a set of devices and computes the differences between the copy that all devices have of content, and the content that Alfresco repository has of the content.
4. **Device**: This specifies the desktop with which the user interacts. It receives and adds content from/to the repository directly.

![Desktop Sync components]({% link sync-service/images/sync-process.png %})

### Information flow

The synchronization process is based on the concept that the repository will publish messages when events happen that may be of interest to the clients. The clients then request the relevant events and use the information to stay in sync with the repository.

The Alfresco repository communicates any changes made to the files, folders, subscriptions and device registrations via a queue. The Sync Service reads the messages in the queue and persists the changes in the database. It determines and records whether the device copy of a particular file differs from the repository. The device makes a `GET` change service request to the Sync Service to get an update on any resources that have changed since the device was last synced. The Sync Service communicates the changes (if any) to the device. The device then uses CMIS and the changed data from the Sync Service to bring the client and the repository in sync.

The desktop can register and synchronize content directly to the repository.

## Desktop Sync process

When you log in to Desktop Sync for the first time, your device gets registered using the REST API in the repository Sync AMP. This creates an association in the repository between the person node and the device node.

Furthermore, when you subscribe to a folder, this creates an association representing the node that you have subscribed to.

The repository sends events to an ActiveMQ topic when:

* a device is registered or de-registered
* a node subscription is created or removed
* a node is added
* a node is removed
* a node is renamed
* a node is moved
* node content is changed
* node Permissions are changed
* User / Group is added to new or existing group
* User / Group is removed from a group
* a node is checked out, checked in and cancelled checked out
* a file / Folder is classified (requires Alfresco Records Management/Alfresco Governance Services)
* a file is declared as Record (requires Alfresco Records Management/Alfresco Governance Services)

> **Important:** If ActiveMQ is unavailable, the Alfresco instance will become read-only and no transactions will be committed.

The synchronization service consumes the events from the topic and persists them to the synchronization server PostgreSQL database. This is transactional - so if Postgres is down or unavailable, the events will remain in the ActiveMQ topic and the synchronization service will retry until the events have been successfully persisted to the database.

When a user subscribes to a folder in the repository, the Desktop Sync client performs a tree-walk against the repository (using the CMIS API). The folder structure and content is synced to the Desktop Sync client device. The Desktop Sync client will then poll the synchronization service for changes every 5 minutes, by default. Changes on the device will trigger a poll of the synchronization service for changes. The synchronization service responds with a set of events that represent what has changed in that folder since the last poll request. Based on that, the client determines what changes need to be pushed to the repository, what changes need to be pulled from the repository and which content is in conflict.

Note that the synchronization service doesn't store any authentication information, instead it proxies (and caches for a configurable period of time) authentication from Desktop Sync client poll requests to the repository authentication APIs.

> **Note:** In this release of Sync Service, the Desktop Sync clients support SAML authentication with the Identity Service. Desktop Sync also supports basic authentication with Alfresco Content Services where Identity Service is not being used.

## Limit folder synchronization

If you're an IT administrator, you can prevent folders being synchronized from the repository to Desktop Sync clients. This allows you to have granular control over the content that your Desktop Sync users can access on their desktops.

The main stages for this configuration are: create a custom model with an associated aspect, create a folder rule in Alfresco Share to automatically apply the aspect to new content, add the aspect to existing content, and then update the configuration in Alfresco Content Services.

1. Create a custom model from the **Model Manager** in Alfresco Share **Admin Tools**.

    Follow the steps in [Creating a new model]({% link content-services/latest/config/models.md %}#create-a-content-model).

    Note that you don't need to create a property for the custom model.

2. Click the model name to start creating an associated aspect.

    Follow the steps for [Creating new aspects]({% link content-services/latest/config/models.md %}#custom-types-aspects-and-properties).

    Add a **Display Label** for the aspect so you can identify it in Alfresco Share later.

3. Activate the custom model.

    1. Click **<< Show Models** to return to the list of models.

    2. Click **Actions** and then select **Activate**.

    The status is now **Active**. Active models can be used by your end users, and any custom aspects defined within the model can be applied to folders and files.

4. Access a site in the repository and view the folder within that site that you don't want to be synced.

    For example, you may choose not to sync the **documentLibrary** folder.

5. Create a folder rule that applies the aspect to newly created and updated content.

    Follow the steps in [Defining rules for a folder]({% link content-services/latest/using/content/rules.md %}#defining-rules-for-a-folder).

    Make sure you select the **Rule applies to subfolders** check box, so that the new aspect is automatically applied to new content added to the current folder and subfolders.

    See [Folder rules]({% link content-services/latest/using/content/rules.md %}) for more details.

6. Update the following property in `alfresco-global.properties` to include your custom model and aspect:

    ```bash
    dsync.filter.aspects=cm:workingcopy, ${dsync.filter.aspects.smartFolder}, <your_model>:<your_aspect>
    ```

    where:

    * `<your_model>` specifies the model name created in step 1
    * `<your_aspect>` specifies the aspect name created in step 2

7. Restart Alfresco Content Services.

> **Note:** Apply the new aspect to all existing content in the folder, and subfolders. Adding an aspect manually to existing folders doesn't cascade the extra functionality down the hierarchy. See [Applying aspects]({% link content-services/latest/using/content/files-folders.md %}#applyaspects) for more details.

> **Important:** Applying this property after users have synchronized folders and files won't automatically remove their existing synced content.

## Back up and restore Sync Service

The approach to backup and restore is to ensure that the repository is backed up before the Sync Service, so that a subsequent restore can simply remove any tracked repository changes that occurred after the repository backup.

1. To perform a backup of your Sync Service database, follow these steps:

    1. Backup your repository database. See [Back up and restore]({% link content-services/latest/admin/backup-restore.md %}).

    2. After you have successfully backed up the repository, wait for a couple of minutes to ensure that the synchronization server has correctly tracked the repository after the repository backup.

    3. Alternatively, ensure that all undelivered events in the event queue, `Consumer.<guid>.alfresco.repo.event2` have been delivered such that `Messages Dequeued == Number Of Pending Messages`. Here, `guid` is the synchronization server id, which can be determined from the `syncServiceIdCheck` in the health check response, `https://localhost:9090/alfresco/healthcheck`.

    4. Backup your synchronization service database using your database vendor's backup/restore tools.

2. To perform a restore, follow these steps:

    1. Use the ActiveMQ console to check that all the events in the event queue, `Consumer.<guid>.alfresco.repo.event2` have been consumed. Using the ActiveMQ console, you can either:

        * Remove any undelivered events in the Virtual Topic, `alfresco.repo.event2` and associated queue, `Consumer.<guid>.alfresco.repo.event2`.
        * Delete the Virtual Topic, `alfresco.repo.event2` and associated queue, `Consumer.<guid>.alfresco.repo.event2`.

        Here, `guid` is the synchronization server id, which can be determined from the `syncServiceIdCheck` in the health check response, `https://localhost:9090/alfresco/healthcheck`.

        Note that the Virtual Topic and associated queue will be recreated automatically.

    2. Restore the repository database. See [Back up and restore the repository]({% link content-services/latest/admin/backup-restore.md %}).

    3. Restore the Sync Service database using your database vendor's backup/restore tools.

    4. Restart the Sync Service with the following additional command line parameter:

        ```bash
        -Drecover=<repo admin username>:<repo admin password>
        ```

        The Sync Service will ensure that it and the repository are in sync during bootstrap, before becoming available for requests.
---
title: Troubleshoot Sync Service
---

Sorry you're having trouble syncing Sync Service.

To resolve data synchronizing issues between the desktop and Alfresco repository, we recommend you first try to isolate where the issue is occurring.

Your problem may be related to any one of the following issues.

## Desktop gets no response from the server

If you see a client error message when you try to synchronize data from the desktop to the repository, it could mean that either the repository or synchronization service is down.

Check that the repository, ActiveMQ and Sync Service are all up. Check the repository and Sync Service log files.

## Topic messages or events are not being dispatched

If you see that the ActiveMQ queue is growing, it could mean that the Sync Service is down. In such an event, the updates will not be pulled off ActiveMQ and the Sync Service will not get any updates or changes.

Check that the Sync Service is up. Check the Sync Service log for exceptions.

## Rollback transaction exceptions occur in clients, such as Sync client or Share, and in the repository log file

ActiveMQ down or repository connection to ActiveMQ down.

Note that if the repository can't contact ActiveMQ, all transactions will fail.

## Changes made from Share are not committed to the database

If you see that the changes made from Share are not getting queued in ActiveMQ or the Sync Service cannot request changes from subscription service, it means that ActiveMQ is down. In such an event, changes from Share cannot be synced to ActiveMQ, as a result both the synchronization and subscription services will be out of sync with Share. Also, the Sync Service will terminate.

Check the ActiveMQ, repository, and services logs. Restart ActiveMQ, the Sync Service, and the desktop to check if that resolves the issue.

## Desktop Sync cannot register, subscribe or synchronize with the repository

Try the following:

* Check that the repository is up.
* Check the repository log for exceptions.
* Make sure that the Sync Service amp has been applied to the repository.
* Check that the Sync Service is up.
* Check the Sync Service logs for exceptions.

## ActiveMQ is down

If you are using an ActiveMQ cluster, you benefit from reliable high performance and load balancing of messages. If ActiveMQ is down, the transaction will fail and any file(s) added to the Alfresco folder on your desktop will be deferred. In File Explorer/Finder, the file will show a blue icon and a notification is displayed on the system tray. When ActiveMQ is up and running again, the file is synced and shows a green icon in the File Explorer/Finder.

## Synchronization service is down

If the Alfresco folder goes down, the size of the `Consumer.*.alfresco.repo.event2` queue in ActiveMQ grows. The dispatched number does not increase and the events will be retained until the Sync Service comes back again.

While the Sync Service is down, any file to the Alfresco folder on your desktop will be deferred until the Alfresco folder is back up. In File Explorer/Finder, the file will shows a blue icon and a notification is displayed on the system tray.

## Repository is down

If the Alfresco repository is down, any file(s) added to the Alfresco folder will be deferred until the repository is back again. In File Explorer/Finder, the file will shows a blue icon and a notification is displayed on the system tray/notifications.

## Sync PostgreSQL database down

If you are using a PostgreSQL database cluster, the chances of your database being down are rare in a production environment. If it does occur, the files added to the Alfresco folder on the desktop will be deferred.

In File Explorer/Finder, the file will show a blue icon and a notification is displayed.

## Optimal memory setting

It is recommended that you use at least 2GB heap size for your installation. The optimal memory setting for your installation will largely depend on:

* The amount of sync activity; more syncs will require more memory.
* The number of sync changes per sync. Syncing files and folders consume memory until the sync is complete. After syncing is complete, the memory is reclaimed. By default, the client syncs every 5 minutes, but this needs to account for users going offline for long periods of time. So, the calculation must account for this time.
* The setting of the `sync.cache.expiryTime` property in the config.yml file. The default value is 30s. This will reclaim the memory used by a sync after 30s if it hasn't already been reclaimed.
---
title: Using Grafana
---

## Visualize metrics with Grafana

Grafana is one of many tools that allows you to pull data from Graphite, and allows you to create more customizable, and attractive charts and graphs. You may find your own preferred tool. Here are a couple of Sync Service metrics displayed in Grafana:

![Sync Service metrics in Grafana]({% link sync-service/images/grafana-metrics.png %})

You can create your own dashboard view with various charts and graphs in Grafana by using the following steps.

## Add a Graphite data source

Use these instructions to add a data source from Graphite to use with Grafana.

1. Open your browser and enter `http://<Grafana-host>:3000`.

2. Click **+ Add data source**.

3. Enter a **Name** for this data source.

4. Select **Graphite** from the **Type** menu.

5. Input the **URL** of the Graphite server.

    If you're using a **proxy**, input an IP address that's accessible from the Grafana backend. For example, use the subnet private IP when deployed in AWS:

    ```bash
    http://10.0.2.243:80
    ```

    If you have a **direct** connection, enter a publicly accessible IP:

    ```bash
    http://34.240.113.207:80
    ```

6. Use `Basic Auth` to start with. Graphite's default user and password are `root:root`.

7. Click **Save & Test**.

    You should see the message: `Data source is working`.

## Create your first dashboard

Use these instructions to create your first dashboard in Grafana, and start creating graphs/charts.

1. Open your browser and enter `http://<Grafana-host>:3000`.

2. Click **Create your first dashboard**.

3. Add a new graph by selecting a graph type:

    ![Add new graph]({% link sync-service/images/grafana-dash-new.png %})

4. Click **Panel Title** > **Edit** to select the metric to display in this graph:

    ![Edit dashboard]({% link sync-service/images/grafana-edit.png %})

5. In the **Metrics** tab, select the Graphite **Data Source**, and the value of the metric to display (such as the mean, 99th percentile, etc.).

    ![Metrics]({% link sync-service/images/grafana-dash-data.png %})

6. Click the disk icon ![Disk icon]({% link sync-service/images/disk-icon.png %}) to save the dashboard.

If you've previously saved a dashboard, you can import it using the following steps.

## Import an existing dashboard

Use these instructions to import an existing dashboard into Grafana.

You can import a dashboard that you saved as part of [creating your first dashboard](#create-your-first-dashboard).

1. Open your browser and enter `http://<Grafana-host>:3000`.

2. Click **Dashboards** then **Import**:

    ![Import dashboard]({% link sync-service/images/grafana-dash-import.png %})

3. Find the file you saved in step 6 of [Create your first dashboard](#create-your-first-dashboard) then import it.
---
title: Monitor Sync Service
---

Use this information to manage and monitor various aspects of Sync Service.

There are a number of areas that can be monitored, including:

* The ActiveMQ topic that is used to relay events from the repository to the Sync Service.
* The health of the Sync Service.

The health of the topic can be monitored using JMX and ActiveMQ advisories.

## JMX

Make sure that JMX is enabled in ActiveMQ. For more information, see [ActiveMQ - JMX](https://activemq.apache.org/jmx.html){:target="_blank"}.

ActiveMQ provides a publish/subscribe mechanism to relay node events from the repository to the Sync Service. The JMX beans that exposes information on the node events topic is:

```java
org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Topic,
destinationName=alfresco.repo.event2
```

The Sync Service consumes from a queue that is tied to the virtual topic. The JMX bean name of this queue is:

```java
org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Queue,
destinationName=Consumer.<SyncId>.alfresco.repo.event2
```

where `<SyncId>` is a UUID that uniquely represents the Sync Service. This UUID can be obtained from the [Sync Service health check](#sync-service-health-check).

## Configure and Monitor Advisories

ActiveMQ supports advisory messages or advisories which are added to a standard topic when something happens in ActiveMQ, for example, when a message is consumed or if a message is discarded.

Advisories can be read like any other topic. The following advisories can be useful to monitor:

* `sendAdvisoryIfNoConsumers` (for the node events, this advisory is not sent because events are persistent)
* `advisoryForSlowConsumers`
* `advisdoryForFastProducers`
* `advisoryForDiscardingMessages`
* `advisoryWhenFull`

The advisories can be configured in the `activemq.xml` file as follows:

```xml
<policyEntry topic="alfresco.repo.event2" advisoryForDelivery="true"
advisoryForConsumed="true" advisoryForSlowConsumers="true" sendAdvisoryIfNoConsumers="true"
advisoryForFastProducers="true">
```

For more information, see [Handling Advisory Messages](https://activemq.apache.org/components/cms/tutorials/handling-advisory-messages){:target="_blank"}.

## Sync Service health check

The Sync Service exposes a collection of health checks that are useful in managing the Sync Service. The health checks include the status of the Sync Service's ActiveMQ, database, and repository connections.

The Sync Service health check can be accessed using JMX (bean `health`) or a REST call:

```http
GET https://localhost:9090/alfresco/healthcheck
```

The output is something like:

```json
{
  "activeMQConnection": {
    "healthy": true,
    "message": "ActiveMQ connection Ok",
    "duration": 0,
    "timestamp": "2023-06-27T13:42:12.250Z"
  },
  "databaseConnection": {
    "healthy": true,
    "message": "Database connection Ok",
    "duration": 0,
    "timestamp": "2023-06-27T13:42:12.250Z"
  },
  "deadlocks": {
    "healthy": true,
    "duration": 3,
    "timestamp": "2023-06-27T13:42:12.454Z"
  },
  "eventsHealthCheck": {
    "healthy": true,
    "message": "Ok",
    "duration": 4,
    "timestamp": "2023-06-27T13:42:12.450Z"
  },
  "minimumClientVersion": {
    "healthy": true,
    "message": "1.0.1",
    "duration": 0,
    "timestamp": "2023-06-27T13:42:12.250Z"
  },
  "repositoryConnection": {
    "healthy": true,
    "message": "Repository connection Ok",
    "duration": 194,
    "timestamp": "2023-06-27T13:42:12.445Z"
  },
  "syncServiceIdCheck": {
    "healthy": true,
    "message": "0abd879e-bdc0-30be-8622-86e3f71f59a6",
    "duration": 7,
    "timestamp": "2023-06-27T13:42:12.250Z"
  },
  "versionCheck": {
    "healthy": true,
    "message": "    3.10.0 (2023-04-28T12:18:27Z)",
    "duration": 0,
    "timestamp": "2023-06-27T13:42:12.250Z"
  }
}
```

This table describes each part of the health check.

| Elements | Description |
| -------- | ----------- |
| "eventsHealthCheck" : { "healthy" : true, "message" : "Ok" }, | This specifies the health of the repository events tracking mechanism. It relies on the `nodeEventLag.99thPercentile` metric. This defines the time taken for events sent by the repository to be consumed by the Sync Service. It returns `false` if `nodeEventLag.99thPercentile/1000000000` > `sync.health.events.eventLagTolerance` (default value is 5000ms). If `false` this could mean that it's flooded with more events than the Sync Service can consume. It may take more than 5 seconds for an event to travel from Alfresco Content Services to Sync Service (via ActiveMQ). Also, check for clues in the Sync Service logs to see if it's unable to consume specific events. This makes ActiveMQ retry delivery, hence the increased `nodeEventLag`. |
| "activeMQConnection" : { "healthy" : true, "message" : "ActiveMQ connection Ok" }, | This specifies that the connection to ActiveMQ is healthy. |
| "repositoryConnection" : { "healthy" : true,         "message" : "Repository connection Ok" }, | This specifies that the Sync Service can connect to Alfresco, for example, hostname and port in config.yml. |
| "databaseConnection" : { "healthy" : true, "message" : "Database connection Ok" }, | This specifies that the Sync Service is connected to the database and making successful SQL calls. |
| "syncServiceIdCheck" : { "healthy" : true, "message" : "00f51927-12d5-4f1b-9979-287fa6fe2771" } | This specifies the ID used in the connection to ActiveMQ to identify itself to the queue. |
| "deadlocks" : { "healthy" : true },|All Dropwizard applications ship with the deadlocks health check installed by default, which uses the Java 1.6 built-in thread deadlock detection to determine if any threads are deadlocked. |
| "minimumClientVersion": { "healthy": true, "message": "1.0.1" }, | Specifies if the `dsync.client.version.min` has been specified in `alfresco-global.properties`. |

The following diagram shows the ActiveMQ queue consumer list. Here, the consumer name relates to the `syncServiceIdCheck` - `message`. Also, the **Number of Consumers** relates to the `maxConsumers` property which is specified in the `config.yml` file.

![Sync Service monitoring - Active MQ]({% link sync-service/images/ds-monitor.png %})

## Logging

The `config.yml` file contains the logging information.

```yaml
logging:
  level: INFO
  loggers:
    "org.alfresco.service.common.auth": WARN
    "org.apache.activemq": WARN
    "com.sun.jersey.api.container.filter.LoggingFilter": WARN
    "org.alfresco.service": INFO
  appenders:
    - type: console
      threshold: ALL
      timeZone: UTC
      target: stdout
      logFormat: "%-5level [%d{yyyy-MM-dd HH:mm:ss.SSS}] [%thread] %logger - %msg%n"
    - type: file
      threshold: ALL
      timeZone: UTC
      currentLogFilename: ./logs/sync-service.log
      archive: true
      archivedLogFilenamePattern: ./logs/sync-service-%d.log.gz
      archivedFileCount: 5
      logFormat: "%-5level [%d{yyyy-MM-dd HH:mm:ss.SSS}] [%thread] %logger - %msg%n"
```

## Sync Service metrics

The Sync Service exposes a collection of metrics that are useful in managing the Sync Service. These metrics can be accessed using JMX (see bean `metrics`) or a REST call:

```http
GET https://localhost:9090/alfresco/api/-default-/private/alfresco/versions/1/metrics
```

The response is JSON and contains all the metrics collected by the Sync Service. In particular:

| Metric Name | Type | Description |
| ----------- | ---- | ----------- |
| nodeEventLag | Timer (*) | Specifies the time taken for events sent by the repository to be consumed by the Sync Service. It is measured in milliseconds. |
| nodeEventsBrokerTime | Timer | Specifies the amount of time the event spends in the (ActiveMQ) broker. |
| nodeEventBrokerLag | Timer | Specifies the lag between events being sent to the (ActiveMQ) broker by the repository and the time at which the broker receives the event.|
| nodeEventConsumerLag | Timer | Specifies the lag between the broker sending out events and the Sync Service consuming them. |
| lagBetweenEventCreateAndSend | Timer | Specifies the lag between the event creation time and the time the event is sent to the (ActiveMQ) broker. |
| syncsTimedOut | Meter (**) | Specifies the syncs that have timed out (possibly due to long query times). |
| syncFailuresMeter | Meter | Specifies the sync failures. |
| syncsTimer|Timer | Specifies the distribution of sync times. |
| timePerCommit | Timer | Specifies the node event database commit times. |
| timePerEventUpdate | Timer | Specifies the node event database insert times. |
| timePerGetChanges  |Timer | Specifies the sync query times. |
| numActiveClusterMembers | Gauge (***) | Number of active Sync Service cluster members. |

(*) Timer measures the rate that a particular piece of code is called and the distribution of its duration. See [Timers](https://metrics.dropwizard.io/3.1.0/getting-started/#timers){:target="_blank"}.

(**) Meter measures the rate of events over time, for example, requests per seconds. See [Meters](https://metrics.dropwizard.io/3.1.0/getting-started/#meters){:target="_blank"}.

(***) Gauge is an instantaneous measurement of a value. See [Gauges](https://metrics.dropwizard.io/3.1.0/getting-started/#gauges){:target="_blank"}.

## Reporting Sync Service metrics to Graphite

In order to visualize the metrics listed above in a graphical manner, Sync Service can be configured to report all its metrics to [Graphite](https://graphite.readthedocs.io/en/latest/overview.html){:target="_blank"}. See the `sync.metrics.reporter.graphite.*` properties in [Configure the Sync Service]({% link sync-service/latest/config/index.md%}).

Here you can see a glimpse of how the `timePerCommit` metric looks like in Graphite:

![Sync Service metrics - Graphite]({% link sync-service/images/graphite-metrics.png %})

If one or more Sync Service instances form a cluster, the same metric is reported in the graph as an averaged value.
---
title: Configure Sync Service
---

Use this information to configure Sync Service.

You can also find additional information in:

* [Connect to Sync Service through JMX]({% link sync-service/latest/config/jmx.md %})
* [Run Sync Service via a script]({% link sync-service/latest/config/script.md %})

## Required properties

The out-of-the-box Sync Service provides an SSL key but it's recommended that you use your own SSL key.

To configure the Sync Service, update the `server.applicationConnectors.http.keyStore*` properties in the `sync/service-sync/config.yml` file.

The following table lists the Sync Service properties:

| Property | Description |
| -------- | ----------- |
| repo.scheme | *Required.* Specifies the repository URL scheme. The default value is `http`. |
| repo.hostname | *Required.* Specifies the repository hostname. The default value is `localhost`. |
| messaging.broker.host | *Required.* Specifies the ActiveMQ broker hostname. |
| messaging.broker.port | *Required.* Specifies the ActiveMQ broker port. |
| sql.db.url | *Required.* Specifies the sync database URL. |
| sql.db.username | *Required.* Specifies the sync database username. |
| sql.db.password | *Required.* Specifies the sync database password. |

## Optional properties

You can modify the installation, depending on your requirements, using the following optional properties in the `<installLocation>/service-sync/config.yml` file:

| Property | Description |
| -------- | ----------- |
| messaging.events.repo.node.maxConsumers |  Specifies the maximum size of the event consumer thread pool. Increase this to provide more threads for event consumption. |
| messaging.events.repo.node.numConsumers | Specifies the initial size of the event consumer thread pool. Depending on the load it will increase up to `maxConsumers`. |
| sync.health.events.eventLagTolerance | Specifies the event lag the synchronization service events health check will tolerate before displaying a warning (default is 5000ms). |
| sync.authentication.basicAuthUrl | Specifies the standard repository authentication URL that the synchronization service uses to authenticate sync requests. |
| sync.authentication.cache.expiryMs | Specifies the expiry time (in ms) of the synchronization service authentication cache. Setting this higher than the default client polling time (5 minutes) should ensure that sync requests do not need to re-authenticate with the repository very often, at the cost of more memory use. |
| sync.cleanup.keepPeriod | Specifies the length of time events are retained before being deleted (default is 28 days). |
| sync.cleanup.events.schedulerExpression | Specifies a cron expression used by Quartz to trigger the jobs that delete old node events, namely events that are older than a configured number of days/hours/minutes (see property `sync.cleanup.events.keepPeriod`). The default value is `0 0 * ? * *` (every hour). For more information about the cron expression, see the [CronTrigger tutorial](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/tutorial-lesson-06.html){:target="_blank"}. |
| sync.cleanup.events.numThreads | Specifies the maximum number of threads to use for event cleanup. |
| sync.cleanup.events.batchSize | Specifies the batch size for event cleanup. |
| sync.cleanup.events.maxItems | Specifies the maximum number of events that will be deleted once the cleaning job is triggered. |
| sync.cleanup.authEvents.schedulerExpression | Specifies a cron expression used by Quartz to trigger the jobs that delete old authority events. These are events that don't apply to a specific node, such as events generated when a group is deleted. The default value is `0 0 */4 ? * *`(every 4 hours). |
| sync.cleanup.txns.schedulerExpression | Specifies a cron expression used by Quartz to trigger the jobs that delete old transaction entries. The default value is `0 0 0-7 ? * *` (every hour between 00:00 and 7:00). |
| logging.level | Specifies the synchronization service logging level. |
| messaging.events.repo.node.redelivery.numRetries | Specifies the maximum number of redelivery attempts allowed to be performed by Apache Camel before the message is exhausted and is moved to the dead letter queue. `0` disables redelivery, and `-1` attempts redelivery forever until it succeeds. **Note:** This is an Apache Camel redelivery attempt, not ActiveMQ. ActiveMQ will try to redeliver the message based on the `jms.redeliveryPolicy.maximumRedeliveries` property which is appended to the `messaging.broker.url`. For example, if the Sync Service is terminated in the middle of a repository transaction, the Apache Camel redelivery configuration will have no effect. Also, Apache Camel will not redeliver the message if an exception of type `DoNotRetryException` occurs. |
| messaging.broker.url | Specifies the ActiveMQ connector URL. Set the value to specify your ActiveMQ location, and connection protocol. Optionally, you can override the default ActiveMQ options, such as `maximumRedeliveries` (default value is 6). |
| sync.metrics.reporter.graphite.address | IP/hostname of the [Graphite](https://github.com/hopsoft/docker-graphite-statsd){:target="_blank"} server where the Sync Service metrics will be sent|
| sync.metrics.reporter.graphite.enabled | Sets whether sending metrics to Graphite is enabled or not. |
| sync.metrics.reporter.graphite.pollingInterval | The amount of time between polls (in seconds). After every `<pollingInterval>` Graphite will receive a new batch of metrics from the Sync Service. |
| sync.metrics.reporter.graphite.prefix | Prefix used to prepend Sync Service metrics with. |
| sync.metrics.reporter.graphite.port | Port of the Carbon receiver. Carbon is one of the components of Graphite, and is responsible for receiving metrics over the network and writing them to disk using a storage backend. |

### Overriding ActiveMQ default properties via messaging.broker.url

Example: `jms.redeliveryPolicy.maximumRedeliveries`

This property specifies the maximum number of times a message will be redelivered by ActiveMQ before it is considered a poisoned pill and returned to the broker, so it can go to a Dead Letter Queue (DLQ).

* `0` is used to disable redelivery
* `-1` is used for unlimited redeliveries

The property can be appended to `messaging.broker.url`. It's recommended that you set it to the `messaging.events.repo.node.maxConsumers` value, so that when the Sync Service is terminated in the middle of a repository transaction, the message goes back to the broker queue rather than the dead letter queue. By doing this, when the Sync Service comes back online, the broker sends the message again.

For example:

```bash
failover:(tcp://localhost:61616?wireFormat.maxInactivityDurationInitalDelay=30000)?timeout=3000&jms.useCompression=true&startupMaxReconnectAttempts=0&jms.redeliveryPolicy.maximumRedeliveries=10
```

> **Note:** This redelivery is performed by ActiveMQ, not Apache Camel (i.e `messaging.events.repo.node.redelivery.numRetries`). To put this into perspective, consider a scenario where a message can't be acknowledged because of a DB exception. First, Apache Camel attempts to redeliver the message up to the maximum configured value. If it doesn't succeed, the message goes back to the broker, and Apache Camel resets its redelivery counter. Then, the broker attempts to redeliver the message based on its configured value (`jms.redeliveryPolicy.maximumRedeliveries`), if each time the message is sent and not acknowledged; Apache Camel again attempts to redeliver up to the maximum configured value. After all the redelivery attempts performed by Camel and ActiveMQ, the message is sent to the Dead Letter Queue.

## SAML configuration

Alfresco Desktop Sync users can authenticate through a SAML identity provider.

The following prerequisites are required - see the [Supported platforms]({% link sync-service/latest/support/index.md %}) page for specific versions:

* Alfresco Content Services
* Identity Service
* Alfresco Desktop Sync for Mac or Windows

Sync Service supplies the default configuration set in the `alfresco.global.properties` file directly to the Desktop Sync clients as users start the initial login.

See [Setting up Desktop Sync (Windows)]({% link desktop-sync/latest/install/index.md %}#install/windows/setting-up-desktop-sync-on-windows) and [Setting up Desktop Sync (Mac)]({% link desktop-sync/latest/install/index.md %}#install/mac/setting-up-desktop-sync-on-mac) for further details.

The Identity Service may be configured with multiple applications. If an application is created for Alfresco Desktop Sync, then specific configuration properties must be included in the `sync/service-sync/config.yml` file.

| Property | Description |
| -------- | ----------- |
| identity-service.auth-server-url | The base URL of the Identity Service. Example setting: `https://ids.example.com/auth` |
| identity-service.realm | The realm name configured in the Identity Service for Alfresco applications. Example setting: `alfresco` |
| identity-service.resource | The OAuth2 **Client ID** set up in the Identity Service for Alfresco Desktop Sync. Each application has a Client ID that's used to identify the application. The client needs to exist underneath the realm set for `identity-service.realm`. Example setting: `desktop-sync` |
| identity-service.credentials.secret | The secret key for this client if the access type isn't set to public. |
---
title: Connect to Sync Service through JMX
---

To connect to Sync Service remotely via a JMX client (for example, using JConsole), you need to start the Sync Service by enabling the JMX remote option and choose whether to disable authentication and/or SSL. This is because password authentication over the Secure Sockets Layer (SSL) and Transport Layer Security (TLS) is enabled by default.

## Insecure JMX connection

You can start the Sync Service with JMX remote enabled and all security disabled, but this isn't recommended for production systems.

1. Start the service with the following Java options by substituting the required host name and ports:

    ```java
    -Dcom.sun.management.jmxremote=true
    -Djava.rmi.server.hostname=<sync-service-IP>
    -Dcom.sun.management.jmxremote.port=<jmx-remote-port>
    -Dcom.sun.management.jmxremote.rmi.port=<jmx-rmi-port>
    -Dcom.sun.management.jmxremote.authenticate=false
    -Dcom.sun.management.jmxremote.ssl=false
    ```

    For example:

    ```bash
    cd <installLocation>/service-sync
    ```

    ```java
    java -Xmx2G -Dcom.sun.management.jmxremote=true -Djava.rmi.server.hostname=34.253.209.238
    -Dcom.sun.management.jmxremote.port=50800 -Dcom.sun.management.jmxremote.rmi.port=50801
    -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false
    -Djava.io.tmpdir=/var/tmp/dsync -cp postgresql.jar:service-sync-5.0.x.jar
    org.alfresco.service.sync.dropwizard.SyncService server config.yml
    ```

    > **Note:** Make sure the ports for `com.sun.management.jmxremote.port` and `com.sun.management.jmxremote.rmi.port` are open. Also, replace `service-sync-5.0.x.jar` with your exact version.

    > **Note:** For production systems, use both SSL client certificates to authenticate the client host, and password authentication for user management, by enabling `com.sun.management.jmxremote.authenticate` and `com.sun.management.jmxremote.ssl`.

2. Start JConsole by typing the following command:

    ```bash
    jconsole
    ```

3. Select **Remote Process**, and enter the Sync Service IP, and `com.sun.management.jmxremote.port` value, as shown in the example below.
4. Click **Connect**.

    ![JConsole - blank credentials]({% link sync-service/images/jconsole-blank.png %})

## JMX connection with authentication

Before enabling the authentication, first you need to create a password file. The file name isn't important. Use the following example for guidance.

> **Note:** If you're using an earlier JDK version than 9, then you'll need to specify the role in a separate `jmx.access` file.

1. Create the file `jmx.password`.

    `jmx.password` is the password file which defines the roles and their passwords.

    To be functional, a role must have an entry in the password file.

2. In the `jmx.password` file, add the role and the desired password.

    For example:

    ```bash
    alfrescoSync password
    ```

3. Change the `jmx.password` permission to read-only for the owner:

    For example:

    ```bash
    sudo chown dsync: jmx.password && sudo chmod 600 jmx.password
    ```

4. Start the Sync Service by enabling authentication, and pass on the path to the created file:

    ```java
    -Dcom.sun.management.jmxremote.authenticate=true
    -Dcom.sun.management.jmxremote.password.file=/path/to/jmx.password
    ```

    For example:

    ```bash
    cd <installLocation>/service-sync
    ```

    ```java
    java -Xmx2G -Dcom.sun.management.jmxremote=true -Djava.rmi.server.hostname=34.253.209.238
    -Dcom.sun.management.jmxremote.port=50800 -Dcom.sun.management.jmxremote.rmi.port=50801
    -Dcom.sun.management.jmxremote.authenticate=true
    -Dcom.sun.management.jmxremote.password.file=/path/to/jmx.password
    -Dcom.sun.management.jmxremote.ssl=false -Djava.io.tmpdir=/var/tmp/dsync
    -cp postgresql.jar:service-sync-5.0.x.jar org.alfresco.service.sync.dropwizard.SyncService
    server config.yml
    ```

    > **Note:** Replace `service-sync-5.0.x.jar` with your exact version.

5. Start JConsole and select **Remote Process**.

6. Enter the Sync Service IP, `com.sun.management.jmxremote.port` value, user name, and password, as shown in the example below.

7. Click **Connect**.

    ![JConsole]({% link sync-service/images/jconsole.png %})

## JMX connection with authentication and SSL

The out-of-the-box Sync Service provides keystore (`sync.jks`) and truststore (`sync.truststore`). The password for the keystore and truststore for the default installation is specified in the `applicationConnectors` section of the `config.yml` file:

```yaml
server:
    applicationConnectors:
         keyStorePassword:
```

The keystore contains a private key and a self-signed certificate for the Sync Service. The truststore contains the self-signed certificate exported from the keystore to create a trust relationship between the Sync Service and itself. In production systems, the truststore usually contains only certificates that are trusted and signed by certificate authorities (CA).

> **Note:** For production systems, it's strongly advised that you use your own SSL key and a certificate that's signed by a certificate authority.

1. Start the Sync Service by enabling SSL and pass on the path, password, and the store type to the keystore and truststore:

    ```java
    -Dcom.sun.management.jmxremote.ssl=true -Djavax.net.ssl.keyStore=/path/to/keystore
    -Djavax.net.ssl.keyStorePassword=<password> -Djavax.net.ssl.keyStoreType=<type>
    -Djavax.net.ssl.trustStore=/path/to/truststore -Djavax.net.ssl.trustStoreType=<type>
    -Djavax.net.ssl.trustStorePassword=<password>
    ```

    For example:

    ```bash
    cd <installLocation>/service-sync
    ```

    ```java
    java -Xmx2G -Dcom.sun.management.jmxremote=true -Djava.rmi.server.hostname=34.253.209.238
    -Dcom.sun.management.jmxremote.port=50800 -Dcom.sun.management.jmxremote.rmi.port=50801
    -Dcom.sun.management.jmxremote.authenticate=true
    -Dcom.sun.management.jmxremote.password.file=/path/to/jmx.password -Dcom.sun.management.jmxremote.ssl=true
    -Djavax.net.ssl.keyStore=/path/to/sync.jks -Djavax.net.ssl.keyStorePassword=<password>
    -Djavax.net.ssl.keyStoreType=JCEKS -Djavax.net.ssl.trustStore=/path/to/sync.truststore
    -Djavax.net.ssl.trustStoreType=JCEKS -Djavax.net.ssl.trustStorePassword=<password>  
    -Djava.io.tmpdir=/var/tmp/dsync -cp postgresql.jar:service-sync-5.0.x.jar org.alfresco.service.sync.dropwizard.SyncService
    server config.yml
    ```

    > **Note:** Replace `service-sync-5.0.x.jar` with your exact version.

2. Copy the Sync Service truststore into your local machine or export the Sync Service certificate into a new truststore. See the example steps in [How to export and import SSL certificate](#how-to-export-and-import-ssl-certificate).

3. Start JConsole:

    ```java
    jconsole -J-Djavax.net.ssl.trustStore=sync.truststore -J-Djavax.net.ssl.trustStoreType=JCEKS -J-Djavax.net.ssl.trustStorePassword=<password>
    ```

4. Select **Remote Process** and enter the Sync Service IP and `com.sun.management.jmxremote.port` valuevalue, user name, and password, as in the earlier example.

## How to export and import SSL certificate

1. Export the certificate from the `sync.jks` keystore.

    For example, you can use the Java keytool (`<JavaInstallationDir>/bin/keytool`):

    ```java
    keytool -exportcert -alias sync -keystore sync.jks -file synccer.cer -storetype jceks -storepass <password>
    ```

    This creates a `synccer.cer` file. This certificate can then be imported into the truststore so you can use it to start the JConsole.

2. Import the certificate into a truststore.

    For example, using the Java keytool:

    ```java
    keytool -importcert -alias sync -file synccer.cer -keystore sync.truststore -storetype JCEKS -storepass <yourPassword>
    ```

    This creates a truststore file of type JCEKS with the name `sync.truststore` (if it doesn't already exist).
---
title: Run Sync Service via a script
---

Use these instructions to run the Sync Service using a script.

Ensure that you've installed the required software before installing Sync Service.

Before you start the Sync Service, see the [Prerequisites]({% link sync-service/latest/install/index.md %}) and `Readme.txt` file included in the `AlfrescoSyncServer-5.0.x.zip` for more information.

1. Create a user that you'll use to run the process.

    1. For Linux:

        Create a user named **dsync** that you'll use to run the process, with user home set to `/opt/alfresco-sync-service`.

        For example:

        ```bash
        sudo useradd -m -d /opt/alfresco-sync-service dsync
        ```

        The format of the command is: `sudo useradd -m -d </PATH/TO/FOLDER> <USERNAME>`

    2. For Windows:

        You only need a dedicated user if JMX remote authentication is enabled. See `Readme.txt` file in `AlfrescoSyncServer-5.0.x.zip` for details.

2. Use one of the start up scripts from the distribution zip.

    * For Linux: `syncservice.sh`
    * For Windows: `syncservice.bat`

    On Linux:

    1. Make the script file executable:

        ```bash
        sudo chmod +x /opt/alfresco-sync-service/syncservice.sh
        ```

    2. Start the Sync Service by issuing the following command:

        ```bash
        sudo /opt/alfresco-sync-service/syncservice.sh start
        ```

    3. Stop the Sync Service by issuing the following command:

        ```bash
        sudo /opt/alfresco-sync-service/syncservice.sh stop
        ```

    On Windows:

    1. Run `syncservice.bat` to start the Sync Service.

    2. Press `CTRL+C` to stop the Sync Service, or via JMX. See `Readme.txt` for more.
---
title: Install and configure databases
---

Use these instructions to install and configure a database for Sync Service.

{% capture postgres %}

Alfresco recommends that you use a separate PostgreSQL instance for the Sync Service.

> **Note:** Only the Sync Service communicates with the database. It persists events taken from the JMS queue into the database. The repository doesn't communicate with the database.

The Sync Service isn't packaged with a PostgreSQL driver, so it'll need to be downloaded separately and cited in the start-up. See step [Starting the Sync Service]({% link sync-service/latest/install/options.md %}).

1. Download the appropriate driver that's compatible with JDBC42 from the [PostgreSQL JDBC Driver download](https://jdbc.postgresql.org/download.html){:target="_blank"} page.

2. Copy the JAR file into the same directory as the Sync Service JAR.

3. Increase the maximum connections setting in the PostgreSQL configuration file.

    1. Locate the configuration file:

        * Linux: `/var/lib/pgsql/9.4/data/postgresql.conf`
        * Windows: `C:\Program Files\PostgreSQL\9.4\data\postgresql.conf`

    2. Add or edit the `max_connections` property:

        ```bash
        max_connections = 450
        ```

        If `max_connections` is left unchanged, bear in mind that in the PostgreSQL database, the default `max_connections` is `100`. So, the value of the `db.pool.max` property in the `config.yml` file must be less than or equal to `100`.

        If there are multiple Sync Service instances forming a cluster hidden behind a load balancer, `max_connections` should be greater than or equal to the sum of all `db.pool.max` from all `config.yml` files.

        For example, if `max_connections=450`, and there are 3 Sync Service instances, then the correct setting in `config.yml` is `db.pool.max : 150`.

    3. Restart the database.

4. Review your memory requirements in `work_mem` in the `postgresql.conf` file in your PostgreSQL directory.

    Increasing the `work_mem` value increases performance and allows PostgreSQL to perform larger in-memory sorting. For more information about PostgreSQL performance, see  [Tuning PostgreSQL](https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server){:target="_blank"}.

5. Create a Postgres user with the username given by the sync property, `sql.db.username`, with password given by the sync property `sql.db.password`:

    ```sql
    CREATE USER alfresco WITH PASSWORD 'admin';
    ```

6. Create a Postgres database with the name given in the property,  `sql.db.url`, owned by the user `alfresco` that you will use to run PostgreSQL, and ensure that this user has write permissions on all tables and sequences.

    ```sql
    CREATE DATABASE alfresco OWNER alfresco ENCODING 'utf8';
    GRANT ALL PRIVILEGES ON DATABASE alfresco TO alfresco;
    ```

7. Ensure `sql.db.driver` and `sql.db.url` are correctly updated in the `config.yml` file, e.g.

    ```yaml
    sql:
        db:
            driver: org.postgresql.Driver
            url: jdbc:postgresql://localhost:5432/alfresco
    ```

### Additional PostgreSQL configuration requirements

For the Sync Service installation, there are some additional PostgreSQL database configuration requirements.

The PostgreSQL settings to configure depends on:

* Level of repository activity: A higher activity increases the database insert/update and auto_vacuum analyze load.
* Number of syncs: A higher number of syncs results in a higher query load. The sizing of memory buffers need to reflect this.
* Event size: The average event size is 1300 bytes.

#### Sync activity level

Setting affected by the sync activity level include:

* `work_mem`: The sync query result set sizes may be large for subscriptions that haven't been synced for a while. Also, the subscriptions need to be sorted. By default, the client will sync every 5 minutes so the number of sync changes is not likely to be very large, but clients that are offline will build up large outstanding sync result sets. Set `work_mem` higher if clients are expected to be offline for long periods of time.

#### Repository activity level

Settings affected by repository activity level include:

* `autovacuum_naptime`: The database is split into half between writes (event persistence) and reads (sync changes). For a more write heavy installation in which the repository updates outweigh the sync activity, this property needs to be set lower so that the new events are incorporated into the table statistics (and hence indexes are used optimally).
* `autovacuum_analyze_threshold`: The default value is 50 tuples. For a more repository update heavy installation, set this property to a low value to help with queries.

#### Disk space

Disk space is required for the events and subscriptions. The events use most of the disk space. A typical operation, such as add folder/document, update document, delete folder/document, move folder/document will result in 1-10 events. More complex operations, such as create site will generate more.

A cleanup job runs periodically to clean up events that are older than a configurable number. The default value is 28 days, so the disk space is required to cover this time period. The disk space is set using the `sync.cleanup` property in the `config.yml` file.

A rough estimate of disk space requirements for PostgreSQL database can be calculated as follows:

```bash
(#update operations per hour * 24*28 * 5 * 1300) / (1024*1024) MB
```

So based on the above assumptions and 100 operations per hour, we have ~416MB.

The following query will give the disk space usage for each of the Sync Service tables and indexes:

```sql
SELECT nspname || '.' || relname AS "relation",
    pg_size_pretty(pg_relation_size(C.oid)) AS "size"
FROM pg_class C
LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
WHERE nspname NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
AND relname like '%sync%'
ORDER BY pg_relation_size(C.oid) DESC
LIMIT 200;
```

{% endcapture %}

{% capture oracle %}

Alfresco recommends that you use a separate Oracle instance for the Sync Service.

> **Note:** Only the Sync Service communicates with the database. It persists events taken from the JMS queue into the database. The repository does not communicate with the database.

The Sync Service isn't packaged with an Oracle driver, so it'll need to be downloaded separately and cited in the start-up. See step [Starting the Sync Service]({% link sync-service/latest/install/options.md %}).

1. Download the Oracle database connector `ojdbc7.jar` from the [Oracle JDBC Driver download](https://www.oracle.com/database/technologies/jdbc-drivers-12c-downloads.html){:target="_blank"} page.

2. Copy the JAR file into the same directory as the Sync Service JAR.

    The JDBC driver for Oracle is in the JAR file: `ojdbc7.jar`.

    However, if you see the following error, then add the `Doracle.jdbc.thinLogonCapability=o3` parameter to `JAVA_OPTS`:

    ```bash
    java.sql.SQLException: OAUTH marshaling failure
    ```

3. The Oracle database must be created with the AL32UTF8 character set. Check the current character set by executing:

    ```sql
    SELECT value$ FROM sys.props$ WHERE name = 'NLS_CHARACTERSET' ;
    ```

    Have a look at this quick tutorial to alter the character set: [Change Oracle Database Character Set : NLS_CHARACTERSET](https://easyoradba.com/2010/07/02/change-oracle-database-character-set-nls_characterset/){:target="_blank"}.

4. Increase the maximum connections setting in the Oracle configuration file. The property `processes` specifies the maximum number of operating system user processes that can simultaneously connect to Oracle. This effectively determines the maximum number of concurrent users in the system.

    ```bash
    alter system set processes=450 scope=spfile
    ```

    The value of the `db.pool.max` property in the  `config.yml` file must be less than `processes`.

    If there are multiple Sync Service instances forming a cluster hidden behind a load balancer, `processes` should be greater than or equal to the sum of all `db.pool.max` from all `config.yml` files.

    For example, if `processes=450`, and there are 3 Sync Service instances, then the correct setting in `config.yml` is `db.pool.max : 150`.

5. Create a user with the username given by the sync property, `sql.db.username`, with password given by the sync property, `sql.db.password`:

    ```sql
    CREATE USER alfresco IDENTIFIED BY admin;
    ```

6. Grant the alfresco user Connect and Resource privileges in Oracle.

    1. Grant the user write permissions on all tables and sequences:

        ```sql
        GRANT CONNECT, RESOURCE TO alfresco;
        ```

    2. Configure the privileges by using one of the following commands:

        ```sql
        ALTER USER alfresco QUOTA <QUOTE_M> ON Users;
        ```

        or

        ```sql
        GRANT UNLIMITED TABLESPACE TO alfresco
        ```

        > **Note:** If the privileges on tablespace "USERS" aren't set correctly, you may see the following error:

        ```bash
        ORA-01950: no privileges on tablespace 'USERS'
        ```

7. Ensure `sql.db.driver` and `sql.db.url` are correctly updated in the `config.yml` file, for example:

    ```yaml
    sql:
        db:
            driver: oracle.jdbc.OracleDriver
            url: jdbc:oracle:thin:@//localhost:1521/xe
    ```

{% endcapture %}

{% capture mysql %}

Alfresco recommends that you use a separate MySQL instance for the Sync Service.

**Note:** Only the Sync Service communicates with the database. It persists events taken from the JMS queue into the database. The repository doesn't communicate with the database.

The Sync Service isn't packaged with a MySQL driver, so it'll need to be downloaded separately and cited in the start-up. See step [Starting the Sync Service]({% link sync-service/latest/install/options.md %}).

1. Download the MySQL database connector from the [MySQL JDBC Driver download](https://dev.mysql.com/downloads/connector/j/) page.

2. Copy the JAR file into the same directory as the Sync Service JAR.

3. Locate the configuration file:

    * For Linux: `/etc/my.cnf`
    * For Windows: `C:\Users\All Users\MySQL\MySQL Server 5.6\my.ini`

4. Increase the maximum connections setting in the MySQL configuration file. In the `mysqld` section, add or edit the `max_connections` property:

    ```bash
    max_connections = 450
    ```

    If `max_connections` is left unchanged, bear in mind that in the MySQL database, the default `max_connections` is `151`. So, the value of the `db.pool.max` property in the config.yml file must be less than or equal to `151`.

    If there are multiple Sync Service instances forming a cluster hidden behind a load balancer, `max_connections` should be greater than or equal to the sum of all `db.pool.max` from all `config.yml` files.

    For example, if `max_connections=450`, and there are 3 Sync Service instances, then the correct setting in `config.yml` is `db.pool.max : 150`.

5. Set the `max_allowed_packet` parameter to an appropriate size, for example `1M`.

    ```bash
    max_allowed_packet=1M
    ```

    This helps to avoid [Packet too large](https://dev.mysql.com/doc/refman/5.7/en/packet-too-large.html){:target="_blank"} exceptions, since the average event size is 1300 bytes.

6. To further improve InnoDB performance, you can increase the InnoDB buffer pool size.

    ```bash
    innodb_buffer_pool_size=2G
    ```

    The larger the InnoDB buffer pool, the more InnoDB acts like an in-memory database. The default value is `8M`. See the MySQL documentation on [Configuring the InnoDB buffer pool size](https://dev.mysql.com/doc/refman/5.7/en/innodb-buffer-pool-resize.html){:target="_blank"} for more details.

7. Divide your buffer pool into separate instances:

    ```bash
    innodb_buffer_pool_instances=4
    ```

    This can improve concurrency by reducing contention, as different threads read and write to cached pages. Default value is 1 when `innodb_buffer_pool_size<1G`.

8. Restart the database.

9. Create a MySQL user with the username given by the sync property, `sql.db.username`, with password given by the sync property, `sql.db.password`:

    ```sql
    CREATE USER 'alfresco' IDENTIFIED BY 'admin';
    ```

10. Create a MySQL database with the name given by the property, `sql.db.url`, owned by the user, `alfresco`:

    ```yaml
    sql:
        db:
            url: jdbc:mysql://localhost:3306/alfresco?useUnicode=yes&characterEncoding=UTF-8
    ```

    If the repository generates events for nodes with names or paths that require non-US-ASCII characters, you need to set the encoding for internationalization. This allows you to store content with accents in the repository. The database must be created with the UTF-8 character set and the `utf8_bin` collation. Although MySQL is a Unicode database, and uses Unicode strings in Java, the JDBC driver might corrupt your non-English data. Ensure that you keep the `?useUnicode=yes&characterEncoding=UTF-8` parameters at the end of the JDBC URL.

    > **Note:** Ensure that the MySQL database is set to use UTF-8 and InnoDB.

11. Ensure that the MySQL database is set to use UTF-8 and InnoDB:

    ```sql
    CREATE DATABASE alfresco DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
    GRANT ALL ON alfresco.* to alfresco IDENTIFIED BY 'admin';
    ```

12. Ensure `sql.db.driver` and `sql.db.url` are correctly updated in the `config.yml` file, for example:

    ```yaml
    sql:
        db:
            driver: com.mysql.jdbc.Driver
            url: jdbc:mysql://localhost:3306/alfresco?useUnicode=yes&characterEncoding=UTF-8
    ```

{% endcapture %}

{% include tabs.html tableid="databases" opt1="Postgres" content1=postgres opt2="Oracle" content2=oracle opt3="MySQL" content3=mysql %}
---
title: Installation overview
---

The Sync Service capability for Desktop Sync is delivered as a distribution zip file containing a repository AMP file, server files for the Sync Service, and third-party license information.

You can download the Alfresco Sync Service software from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

## Prerequisites

This section lists the environment/software prerequisites for installing and using the Sync Service.

See [Supported platforms]({% link sync-service/latest/support/index.md %}) for more.

### General requirements

* Messaging broker
  * See [Setting up ActiveMQ]({% link content-services/latest/config/activemq.md %}) for more information about installing ActiveMQ.

* Make sure that search indexing is [enabled]({% link search-services/latest/index.md %}).

## Installation options

There are several [options]({% link sync-service/latest/install/options.md %}) for installing the Sync Service:

* Install manually using a distribution ZIP
* Install using Helm charts or Docker Compose
---
title: Installation options
---

There are several options for installing the Sync Service:

* Install manually using a distribution ZIP
* Install using Helm charts or Docker Compose (i.e. [containerized deployment](#containerized-deployment))

> **Note:** It is recommended that you familiarize yourself with the concepts of containerized deployment before working with Docker, Kubernetes, and Helm.

## Install with zip

Use these instructions to install the Sync Service repository modules and services on Alfresco Content Services.

The Sync Service distribution zip file, `AlfrescoSyncServer-5.0.x.zip`, includes all the files required to provide the Sync Service. This file contains the following artifacts:

* `amps-repository` directory containing the Sync Service repository AMP: `alfresco-device-sync-repo-5.0.x.amp`
* `licenses` directory containing the 3rd-party licenses
* `service-sync` directory with:
  * `service-sync-5.0.x.jar` Sync Service JAR
  * `config.yml` property file
  * `syncservice` start/stop script
  * `sync.jks` SSL keys

> **Note:** The keystore `sync.jks` contains a self-signed certificate that should be used for testing purposes only. You'll need to provide your own SSL keys for a production environment.

> **Note:** Make sure you're running the correct versions of operating system and software before you install the AMP file. See [Prerequisites]({% link sync-service/latest/install/index.md %}) for more information.

1. Download `AlfrescoSyncServer-5.0.x.zip` from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2. Extract the `AlfrescoSyncServer-5.0.x.zip` file into a system directory; for example, `<installLocation>/`.

    We'll refer to this new directory (`<installLocation>/sync`), as the *Alfresco Sync Service installation directory*. In this directory you'll see these folders:

    * `amps-repository`
    * `licenses`
    * `service-sync`

3. Stop the Alfresco repository.

4. Use the Module Management Tool (MMT) to install the `alfresco-device-sync-repo-5.0.x.amp` AMP into the repository WAR.

    For more information, see instructions in [Install the AMP file]({% link content-services/latest/install/zip/amp.md %}).

    For example, to apply the `alfresco-device-sync-repo-5.0.x.amp`, use the following command:

    ```java
    java -jar <alfrescoInstallLocation>\bin\alfresco-mmt.jar install <installLocation>\amps-repository\alfresco-device-sync-repo-5.0.x.amp <installLocation>\tomcat\webapps\alfresco.war
    ```

5. Add the following properties to the `alfresco-global.properties` file:

    ```bash
    dsync.service.uris=https://<hostname>:9090/alfresco
    messaging.broker.url=failover:(tcp://localhost:61616)?timeout=3000
    ```

    where:

    * `dsync.service.uris` specifies the hostname of the Sync Service (or the load balancer hiding the Sync Service cluster) that Desktop Sync clients can see. For example, `https://<hostname>:9090/alfresco`.
    * The `dsync.service.uris` value needs to be set to an IP address or hostname of the Sync Service machine that can be accessed by the Desktop Sync clients outside the firewall. In addition, the port 9090 needs to be opened up in the firewall so that clients can access the Sync Service.
    * `messaging.broker.url` specifies the location of ActiveMQ.

6. Configure the Sync Service properties in the `<installLocation>/service-sync/config.yml` file.

    See [Configure Sync Service]({% link sync-service/latest/config/index.md %}).

    For example, edit the following properties:

    * repo:

        ```yaml
        hostname: localhost
        ```

        where `repo.hostname` is the IP address of the repository host.

    * messaging:

        ```yaml
        broker:
            host: localhost
        ```

        where `messaging.broker.host` is the IP address of the ActiveMQ host.

    * sql:

        ```yaml
        db:
            url: jdbc:postgresql:alfresco
        ```

        where `sql.db.url` is the URL of the Postgres database.

7. Start and configure PostgreSQL.

    For more information, see [Configuring PostgreSQL database for Desktop Sync]({% link sync-service/latest/install/database.md %}).

8. Start ActiveMQ.

    If ActiveMQ is down, the repository transactions will fail and rollback. In production environments, it's advisable that you run an ActiveMQ cluster in failover mode to avoid this situation. See [ActiveMQ master/slave configurations](https://activemq.apache.org/masterslave.html){:target="_blank"}.

    For more information, see [Setting up ActiveMQ]({% link content-services/latest/config/activemq.md %}).

9. Start the repository.

    > **Note:** Wait for the repository to fully start before proceeding to the next step.

10. Start the Sync Service.

    For Linux:

    ```bash
    cd <installLocation>/service-sync

    java -Xmx2G -Djava.io.tmpdir=/var/tmp/dsync -classpath <classpath to database.jar file>:service-sync-5.0.x.jar org.alfresco.service.sync.dropwizard.SyncService server config.yml
    ```

    See [Running Sync Service via a script]({% link sync-service/latest/config/script.md %}).

    For Windows:

    ```bash
    cd <installLocation>/service-sync

    java -Xmx2G -Djava.io.tmpdir=/users/<username>sync/tmp -classpath <classpath to database.jar file>;service-sync-5.0.x.jar org.alfresco.service.sync.dropwizard.SyncService server config.yml
    ```

    > **Note:** For production systems, you need to configure JMX authentication as password authentication over the Secure Sockets Layer (SSL) is enabled by default. However, in a test environment, you can disable all security, namely both password authentication and SSL, when you start the Java VM. See [Connect to Sync Service through JMX]({% link sync-service/latest/config/jmx.md %}) for configuration options. For more information, see the [JRE documentation](https://docs.oracle.com/javase/7/docs/technotes/guides/management/agent.html){:target="_blank"}.

    > **Note:** The PostgreSQL JDBC driver must be provided and included in the startup command line as shown above.

    For more information, see [Install and configure PostgreSQL database]({% link sync-service/latest/install/database.md %}).

11. Access Alfresco Share by browsing to:

    ```http
    http://<hostname>:8080/share
    ```

12. Check the repository and Sync Service log file (`<installLocation>/service-sync/logs/sync-service.log` by default) to see if the Sync Service started properly. The location of the log file can be configured using the `logging` properties in the `config.yml` file.

    To validate that the Sync Service is configured correctly, see [Sync Service health check]({% link sync-service/latest/admin/monitor/index.md %}#sync-service-health-check).

## SSL certificate for the synchronization server

Alfresco supplies a self-signed certificate with the Sync Service. This certificate is for testing purposes only, and it's not recommended for use in a production system.

## How to disable SSL for the synchronization server

1. In the `applicationConnector` section of the `config.yml` file, comment out or remove the lines from `type: https` to `validateCerts: false`.

    ```yaml
    server:
        type: default
        applicationConnectors:
            - type: http
              port: 9090
            # type: https
            # keyStorePath: ./sync.jks
            # keyStorePassword: N9SnIgrcAx7zWr
            # keyStoreType: JCEKS
            # validateCerts: false
    ```

2. For the `dsync.service.uris` property, replace `https` with `http` in the alfresco-global.properties file.

    For example, `dsync.service.uris=http://localhost:9090/alfresco`.

## Install and configure databases

The Sync Service is not packaged with a database driver, so it will need to be downloaded separately and cited in the start-up.

See instructions to [install and configure databases]({% link sync-service/latest/install/database.md %}).

## Containerized deployment

Sync Service can optionally be deployed as part of Alfresco Content Services using Helm charts or a Docker Compose file.

It is recommended that these deployment references are used as an accelerator by customers who have prior production experience with containerized deployment technologies like Docker, Kubernetes and Helm.

Follow these links to find out how to deploy Alfresco Content Services including the Sync Service using Helm charts or Docker Compose:

* [Install with Helm charts]({% link content-services/latest/install/containers/helm.md %})
* [Install with Docker Compose]({% link content-services/latest/install/containers/docker-compose.md %})

Due to the limited capabilities of Docker Compose, this deployment method is recommended for development and test environments only.

## Uninstalling Sync Service

To remove the Sync Service, uninstall the Sync Service AMP file, remove the Sync Service installation, and then remove the ActiveMQ topic.

1. Stop the Alfresco server.

2. Uninstall the Sync Service, AMP file in the repository, for example using the Module Management Tool (MMT):

    ```java
    java -jar bin/alfresco-mmt.jar uninstall alfresco-device-sync-repo-5.0.x.amp tomcat/webapps/alfresco.war
    ```

    [Uninstall an AMP file]({% link content-services/latest/install/zip/amp.md %}#uninstall-an-amp-file) provides information on how to uninstall the AMP file, and remove the AMP content from the WAR files.

3. Delete the Tomcat webapp directory.

    For example, delete `tomcat/webapps/alfresco`.

    Deleting these directories forces Tomcat to read the edited WAR files when Alfresco is restarted.

4. Review the `autoStart` properties in your `alfresco-global.properties` file to ensure that the events and messaging subsystems aren't set to start automatically.

    Uninstalling the AMP file removes any settings applied by the Sync Service repository module, however you should review custom `autoStart` properties to check that they're set to `false`:

    ```bash
    events.subsystem.autoStart=false
    messaging.subsystem.autoStart=false
    ```

5. Ensure that all system services relating to the Sync Service are stopped, disabled or removed. Disable all cron jobs, and ensure there are no active Analytics processes on your server.

    There are four system services to stop:
    * ActiveMQ
    * Event broker
    * Messaging broker
    * Sync Service

6. Ensure that Alfresco Content Services isn't physically connected to the Sync Service installation and that all related functions are disabled.

    You'll physically remove all parts of the Sync Service installation, so you must make sure this doesn't affect the Alfresco Content Services installation. Most Sync Service files are installed in `<installLocation>`, which you chose during installation (for example, `<installLocation>/sync`).

7. Remove the Sync Service installation and database.

    Navigate to the Sync Service installation directory. Remove all Sync Service files by running the `rm -rf` command, or run this command from another directory:

    ```bash
    rm -rf /<installLocation>/sync
    ```

8. Using the ActiveMQ Console, remove the ActiveMQ topic and queues matching the following names:

    ```bash
    Queue Consumer.*.alfresco.repo.event2
    Topic alfresco.repo.event2
    ```
---
title: Supported platforms
---

The following are the supported platforms for Alfresco Sync Service 4.0:

| Version | Notes |
| ------- | ----- |
| Alfresco Content Services 23.x | Optionally with Alfresco Governance Services 23.x |
| Identity Service 2.0 | Required for SAML authentication |
| Alfresco Desktop Sync for Windows 1.16 | |
| Alfresco Desktop Sync for Mac 1.16 | |
| | |
| | Check the [Alfresco Content Services Supported platforms]({% link content-services/latest/support/index.md %}) page for specific versions of the individual components. |
| **Java** | |
| OpenJDK 17 (64-bit) | |
| | |
| **Message brokers** |
| Apache ActiveMQ | |
| Amazon MQ | |
| | |
| **Operating systems** | |
| Windows Server | |
| Linux | |
| | |
| **Databases** |
| PostgreSQL | |
| MySQL | |
| Oracle | |
| Amazon Aurora MySQL | Using MariaDB driver |
---
title: Upgrade Sync Service
---

Use these instructions to upgrade your instance of the Sync Service from version 2.2.0.

1. Download the latest Sync Service zip file from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2. Stop the Alfresco Content Services server.

3. Stop the Sync Service.

4. Back up Alfresco Content Services using the instructions in [Back up and restore the repository]({% link content-services/latest/admin/backup-restore.md %}).

5. Backup your Sync Service database using the steps in [Back up and restore Sync Service]({% link sync-service/latest/admin/index.md %}#back-up-and-restore-sync-service).

6. Configure the Sync Service using the steps in [Install Sync Service]({% link sync-service/latest/install/options.md %}).

7. Test that you can connect successfully to Alfresco Content Services from Desktop Sync.

> **Important:** When you apply the new Sync Service AMPs, apply them to clean/ vanilla WAR files to avoid the risk of having multiple versions of the same AMP. See [Uninstalling an AMP file]({% link content-services/latest/install/zip/amp.md %}#uninstall-an-amp-file) for information about removing AMPs.

> **Important:** When upgrading, ensure that you use the new `config.yml` supplied in the latest Sync Service ZIP. Copy your existing settings from the `config.yml` file into the new file. The differences in the `config.yml` file between 2.2.0 and this version are detailed in the Releases Notes, which are available from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

> **Important:** When upgrading Alfresco Content Services, ensure that the correct license file is installed in the Alfresco folder before starting Alfresco Content Services; Alfresco will not start correctly with the Sync Service AMP applied when an invalid license is present. See [Uploading a new license]({% link content-services/latest/admin/license.md %}#uploadlicense) for details on adding license files.
