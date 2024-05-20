---
title: Alfresco Search and Insight Engine 
---

Alfresco Search and Insight Engine is our new generation of analytics using Alfresco Search Services. It fully supports aspects, properties, ACLs, and Custom Metadata. It also supports SQL queries for reporting on the Solr data store using JDBC, and the dashboard comes pre-configured with some common reports.

Alfresco Search and Insight Engine enables scalability and performance under load for Alfresco Search Services. An Alfresco Search and Insight Engine subscription is required to deploy Search Services and Insight capability to separate server(s), to alleviate load or to split the search index across multiple servers for scalability (sharding).

Alfresco Insight Zeppelin is built on top of Apache Zeppelin 0.8.2 and comes bundled as a report builder. It is pre-configured to easily build custom reports with SQL, including against Custom Metadata. Alfresco Insight Zeppelin is the only supported visualization tool that works with Search and Insight Engine.

Currently the following are not supported with Alfresco Search and Insight Engine 2.0:

* Alfresco Process Services
* Reporting on audit and activity feeds from Alfresco Content Services
* Multi-tenancy
---
title: Overview
---

## Back up

There are a number of ways to back up Search and Insight Engine. You can set the Solr indexes backup properties either by:

* Using the Admin Console.
* Editing the `alfresco-global.properties` file.
* Using a JMX client, such as JConsole.

{% capture console %}

<!--### Set up Solr backup properties using Share Admin Console-->

You can only see the Admin Console if you're an administrator.

1. Launch the Admin Console. For information, see [Launch Admin Console]({% link content-services/latest/admin/admin-console.md %}#launch-admin-console).
2. In the **Repository Services** section, click **Search Service**.

    You see the Search Service page.

3. Scroll down to the **Backup Settings** section. ![]({% link insight-engine/images/solr6-backupsie.png %})

    Here, you can specify the backup location and edit backup properties for each core of the Solr index: **Main Store** and **Archive Store**.

    * **Backup Location**: Specifies the full-path location for the backup to be stored. This location must be on the machine on which Search and Insight Engine is installed or it must be a location which is accessible from the Solr host. For example, `/opt/alfresco-insight-engine/backups/alfresco`.
    * **Backup Cron Expression**: Specifies a Quartz cron expression that defines when backups occur. Solr creates a timestamped sub-directory for each index back up you make.
    * **Backups To Keep**: Specifies the maximum number of index backups that Solr should store.
4. Click **Save**.

{% endcapture %}

{% capture properties %}

<!--### Specifying Solr backup directory by using alfresco-global.properties file-->

This task shows how to specify the Solr backup directory by using the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file.

To set the Solr backup directory using the `alfresco-global.properties` file, set the value of the following properties to the full path where the backups should be kept:

```bash
solr.backup.archive.remoteBackupLocation=
solr.backup.alfresco.remoteBackupLocation=
```

The values set on a subsystem will mean that the property values from configuration files may be ignored. Use the Share Admin Console or JMX client to set the backup location.

{% endcapture %}

{% capture jmx %}

<!--### Back up Solr indexes using JMX client-->

If you have installed the Oracle Java SE Development Kit (JDK), you can use the JMX client, JConsole, to backup Solr indexes, edit Solr backup properties and setup the backup directory.

* You can set the backup of Solr indexes using the JMX client, such as JConsole on the **JMX MBeans > Alfresco > Schedule > DEFAULT > MonitoredCronTrigger > search.alfrescoCoreBackupTrigger > Operations > executeNow** tab. The default view is the Solr core summary. Alternatively, navigate to **MBeans > Alfresco > SolrIndexes > coreName > Operations > backUpIndex** tab. Type the directory name in the **remoteLocation** text box and click **backUpIndex**.
* Solr backup properties can be edited using the JMX client on the **JMX MBeans > Alfresco > Configuration > Search > managed > solr6 > Attributes** tab. The default view is the Solr core summary.

    ![]({% link insight-engine/images/solr6jmx.png %})

* To use JMX client to setup Solr backup directory, navigate to **MBeans tab > Alfresco > Configuration > Search > managed > solr > Attributes** and change the values for `solr.backup.alfresco.remoteBackupLocation` and `solr.backup.archive.remoteBackupLocation properties`.
* You may also trigger a backup with an HTTP command which instructs the /replication handler to backup Solr, for example:

    ```http
    http://localhost:8080/solr/alfresco/replication?command=backup&location={{existingDirectory}}&numberToKeep=4&wt=xml
    ```

    where:

  * `location` specifies the path where the backup will be created. If the path is not absolute then the backup path will be relative to Solr's instance directory.
  * `numberToKeep` specifies the number of backups to keep.

{% endcapture %}

{% include tabs.html opt1="Using Admin Console" content1=console opt2="Using properties" content2=properties opt3="Using JMX" content3=jmx %}

## Solr logging

You can set different debug logging levels for Solr components using the Solr log4j properties.

1. Locate the `<solrRootDir>/log4j-solr.properties` file.

2. Edit it to add your required logging setting. For example:

    ```bash
    log4j.logger.org.alfresco.solr.tracker.MetadataTracker=DEBUG
    ```

3. Changes to the log4j-solr.properties file will be re-read by Solr when it starts up. If you need to make changes to the logging level while the system is running, going to the following URL (either in a browser or for example, using curl) will cause Solr to re-load the properties file.

    ```http
    https://<solrHostName>:<solrPort>/solr/admin/cores?action=LOG4J&resource=log4j-solr.properties
    ```

## Document fingerprints

Alfresco Content Services 6.2 provides support for Document Fingerprints to find related documents. Document Fingerprinting is performed by algorithms that map data, such as documents and files to shorter text strings, also known as fingerprints. This feature is exposed as a part of the Alfresco Full Text Search Query Language.

> **NOTE:** Document fingerprints is disabled by default, for more see [Document Fingerprints]({% link insight-engine/latest/config/performance.md %}#disable-document-fingerprint)

Document Fingerprints can be used to find similar content in general or biased towards containment. The language adds a new `FINGERPRINT` keyword:

```bash
FINGERPRINT:<DBID | NODEREF | UUID>
```

By default, this will find documents that have any overlap with the source document. The `UUID` option is likely to be the most useful as `UUID` is present in the public API. To specify a minimum amount of overlap, use:

```bash
FINGERPRINT:<DBID | NODEREF | UUID>_<%overlap>
FINGERPRINT:<DBID | NODEREF | UUID>_<%overlap>_<%probability>
```

To find documents that have 20% overlap with the document 1234, use:

```bash
FINGERPRINT:1234_20
```

To execute a faster query that will be 80% confident anything brought back will overlap by 20%, use:

```bash
FINGERPRINT:1234_20_80
```

To support fingerprint queries, additional information is added to the Solr 6 index using the rerank template. This makes the indexes approximately 15% bigger. Document Fingerprint can only be disabled by changing the schema.

### Similarity and containment

Document similarity covers duplicate detection, near duplicate detection, and finding different renditions of the same content. This is important to find and reduce redundant information. Fingerprints can provide a distance measure to other documents, often based on Jaccard distance/ similarity coefficient, to support *more like this* and clustering. The distance can also be used as a basis for graph traversal.

The Jaccard similarity coefficient is a commonly used indicator of the similarity between two sets. For sets *A* and *B* it is defined to be the ratio of the amount of common content to the total content of two documents, as defined here:

![]({% link insight-engine/images/union.png %})

This distance can be used to compare the similarity of any two documents with any other pair of documents.

Containment is a related concept but is more about inclusion. For example, many email threads include parts or all of previous messages. Containment is not symmetrical like the measure of similarity above, and is defined as:

![]({% link insight-engine/images/containment.png %})

It represents how much of the content of a given document is common to another document. This distance can be used to compare a single document (A) to any other document.

### Minhashing

Minhashing is a technique for quickly estimating how similar two sets of documents are. It is an example of a text processing pipeline.

First, the text is split into a stream of words. These words are then combined into five word sequences, known as shingles, to produce a stream of shingles. The 5-word shingles are then hashed, for example, in 512 different ways; keeping the lowest hash value for each hash. This results in 512 repeatably random samples of 5-word sequences from the text represented by the hash of the shingle. The same text will generate the same set of 512 minhashes. Similar text will generate many of the same hashes. It turns out that if 10% of all the min hashes from two documents overlap then it is a great estimator that `J(A,B) = 0.1`.

* ***Why 5 word sequences?***: Word embedding suggests 5 or more words are enough to describe the context and meaning of a central word. Based on the distribution of words for 2 word shingles, 3 word shingles, 4 word shingles, and 5 word shingles found on the web, it was found that at 5 word shingles, the frequency distribution flattens and broadens compared with the trend seen for 1, 2, 3 and 4 word shingles.
* ***Why 512 hashes?***: With a well distributed hash function this should give good hash coverage for 2,500 words and around 10% for 25,000, or something like 100 pages of text. We used a 128-bit hash to encode both the hash set position (see later) and hash value to minimise collision compared with a 64 bit encoding including bucket/set position.

***Example 1***

A document contains a single sentence of *The quick brown fox jumps over the lazy dog*, that would be broken down into the following 5-word long shingles:

   1. The quick brown fox jumps
   2. quick brown fox jumps over
   3. brown fox jumps over the
   4. fox jumps over the lazy
   5. jumps over the lazy dog

So, our document as a set looks like:

```bash
Set A = new Set(["The quick brown fox jumps", "quick brown fox jumps over", "brown fox jumps over the", "fox jumps over the lazy", "jumps over the lazy dog"]);
```

These sets of shingles can then be compared for similarity using the Jaccard Coefficient.

![]({% link insight-engine/images/minhash.png %})

***Example 2***

Here are two summaries of the 1.0 and 1.1 CMIS specification. It demonstrates, amongst other things, how sensitive the measure is to small changes. Adding a single word affects 5 shingles.

![]({% link insight-engine/images/minhash-example.png %})

The content overlap of the full 1.0 CMIS specification found in the 1.1 CMIS specification, C(1.0, 1.1) is approximately 52%.
---
title: Monitor and troubleshoot
---

This page helps you monitor and resolve any Solr index issues that might arise as a result of a transaction.

## Perform a full reindex with Solr

This task describes how to perform a full Solr reindex.

The task assumes you are using only one Solr instance for all nodes in the Alfresco Content Services cluster. If not, then you need to repeat the process on each Solr instance used in the cluster.

1. Confirm the location of the Solr core directories for archive and alfresco cores. This can be determined from the solrcore.properties file for both the cores. By default, the solrcore.properties file can be found at `<SOLR_HOME>/solrhome/alfresco/conf` or `<SOLR_HOME>/solrhome/archive/conf`. The Solr core location is defined in the `solrcore.properties` file as:

    For Solr, the default data.dir.root path is:

    ```bash
    data.dir.root=<SOLR_HOME>/solrhome/
    ```

2. Shut down Solr (if running on a separate application server).

3. Delete the contents of the index data directories for each Solr core at `${data.dir.root}/${data.dir.store}`.

    ```bash
    <SOLR_HOME>/solrhome/alfresco/index/
    <SOLR_HOME>/solrhome/archive/index/
    ```

4. Delete all the Alfresco Content Services models for each Solr core at `${data.dir.root}`.

   ```bash
   <SOLR_HOME>/solrhome/alfrescoModels
   ```

5. Start up the application server that runs Solr.

6. Monitor the application server logs for Solr at `<SOLR_HOME>/logs/solr.log`. You will get the following warning messages on bootstrap:

    ```bash
    WARNING: [alfresco] Solr index directory '<SOLR_HOME>/solrhome/alfresco/index' doesn't exist. Creating new index...
    09-May-2018 09:23:42 org.apache.solr.handler.component.SpellCheckComponent inform
    WARNING: No queryConverter defined, using default converter
    09-May-2018 09:23:42 org.apache.solr.core.SolrCore initIndex
    WARNING: [archive] Solr index directory '<SOLR_HOME>/solrhome/archive/index' doesn't exist. Creating new index...
    ```

7. Use the Solr administration console to check the health of the Solr index.

    > **Note:** The process of building the Solr indexes can take some time depending on the size of the repository. To monitor reindexing progress, use the Solr administration console and check the logs for any issues during this activity.

    While the reindex is taking place, some searches may not return the full set of results.

To copy the indexes from a recently re-indexed Solr node to another Solr node, follow these steps:

1. Make sure both the Solr nodes have the same version of the index server.
2. (Optional) Copy the models from node1 to node2 and validate that they are compatible.
3. Fix any configuration issues, for example, renaming the core, updating the configuration to point to the correct data, indexes, and Alfresco Content Services.
4. Disable index tracking on node2 by setting the `enable.alfresco.tracking` property to `false` in `solrcore.properties`.
5. Go to the Solr Admin Web interface to monitor information about each core.
6. Stop node2 and enable tracking by setting the `enable.alfresco.tracking` property to `true` in `solrcore.properties`.
7. Restart the Solr server on node2.

The new index on node2 should start tracking and come up-to-date.

## Unindexed transactions

You can check the status of the Solr index to identify the nodes to a transaction that failed to index.

To generate a report for Solr 6, including the last transaction indexed and the time, use:

```http
http://localhost:8443/solr/admin/cores?action=REPORT&wt=xml
```

The `REPORT` parameter compares the database with the index and generates an overall status report with the following details:

* `DB transaction count`: indicates the transaction count on the database.
* `DB acl transaction count`: indicates the ACL transaction count on the database.
* `Count of duplicated transactions in the index`: indicates the number of transactions that appear more than once in the index. The value of this parameter should be zero. If not, there is an issue with the index.
* `Count of duplicated acl transactions in the index`: indicates the number of ACL transactions that appear more than once in the index. The value of this parameter should be zero. If not, there is an issue with the index.
* `Count of transactions in the index but not the database`: indicates the number of transactions in the index but not in the database. This count includes empty transactions that have been purged from the database. The value of this parameter should be zero. If not, there might be an issue with the index.
* `Count of acl transactions in the index but not the DB`: indicates the number of ACL transactions in the index but not in the database. The value of this parameter should be zero. If not, there is an issue with the index. Note that empty ACL transactions are not purged from the database.
* `Count of missing transactions from the Index`: indicates the number of transactions in the database but not in the index. The value of this index should be zero when the index is up-to-date.
* `Count of missing acl transactions from the Index`: indicates the number of ACL transactions in the database but not in the index. The value of this index should be zero when the index is up-to-date.
* `Index transaction count`: indicates the number of transactions in the index.
* `Index acl transaction count`: indicates the number of ACL transactions in the index.
* `Index unique transaction count`: indicates the number of unique transactions in the index.
* `Index unique acl transaction count`: indicates the number of unique ACL transactions in the index.
* `Index leaf count`: indicates the number of docs and folders in the index.
* `Count of duplicate leaves in the index`: indicates the number of duplicate docs or folders in the index. The value of this parameter should be zero. If not, there is an issue with the index.
* `Last index commit time`: indicates the time stamp for the last transaction added to the index. It also indicates that transactions after this time stamp have not yet been indexed.
* `Last Index commit date`: indicates the time stamp as date for the last transaction added to the index. It also indicates that transactions after this date have not yet been indexed.
* `Last TX id before holes`: indicates that transactions after this ID will be checked again to make sure they have not been missed. This is computed from the index at start up time. By default, it is set an hour after the last commit time found in the index. Solr tracking, by default, goes back an hour from the current time to check that no transactions have been missed .
* `First duplicate`: indicates if there are duplicate transactions in the index. It returns the ID of the first duplicate transaction.
* `First duplicate acl tx`: indicates if there are duplicate ACL transactions in the index. It returns the ID of the first duplicate ACL transaction.
* `First transaction in the index but not the DB`: if the related count is > 0, it returns the ID of the first offender.
* `First acl transaction in the index but not the DB`: if the related count is > 0, it returns the ID of the first offender.
* `First transaction missing from the Index`: if the related count is > 0, it returns the ID of the first offender.
* `First acl transaction missing from the Index`: if the related count is > 0, it returns the ID of the first offender.
* `First duplicate leaf in the index`: if the related count is > 0, it returns the ID of the first offender.

To generate a summary report for Solr 6, use:

```http
http://localhost:8443/solr/admin/cores?action=SUMMARY&wt=xml
```

With multi-threaded tracking, you can specify additional tracking details and tracking statistics:

* `detail=true`: provide statistics per tracking thread.
* `hist=true`: provides a histogram of the times taken for tracking operations for each tracking thread.
* `reset=true`: resets all tracking statistics.
* `values=true`: reports (by default) the last 50 values recorded for each tracking operation for each thread

The `SUMMARY` parameter provides the status of the tracking index and reports the progress of each tracking thread. It generates a report with the following details:

* `Active`: indicates the tracker for the core active.
* `Last Index Commit Time`: indicates the time stamp for the last transaction that was indexed.
* `Last Index Commit Date`: indicates the time stamp as a date for the last transaction that was indexed. Changes made after this time are not yet in the index.
* `Lag`: indicates the difference in seconds between the last transaction time stamp on the server and the time stamp for the last transaction that was indexed.
* `Duration`: indicates the time lag as an XML duration.
* `Approx transactions remaining`: indicates the approximate number of transactions to index in order to bring the index up-to-date. It is calculated as the last transaction ID on the server minus the last transaction ID indexed. It includes all the missing and empty transactions.
* `Approx transaction indexing time remaining`: it is based on Approx transactions remaining, the average number of nodes per transaction and the average time to index a node (how long the index will take to be up-to-date). The estimate is in the most appropriate scale, for example, seconds, minutes, hours and days.
* `Model sync times (ms)`: indicates summary statistics for model sync time. It supports additional information with &detail=true, &hist=true and &value=true.
* `Acl index time (ms)`: indicates summary statistics for ACL index time. It supports additional information with &detail=true, &hist=true and &value=true.
* `Node index time (ms)`: indicates summary statistics for node index time. It supports additional information with &detail=true, &hist=true and &value=true.
* `Acl tx index time (ms)`: indicates the summary statistics for ACL transaction index time. It supports additional information with &detail=true, &hist=true and &value=true.
* `Tx index time (ms)`: indicates summary statistics for transaction index time. It specifies the estimated time required to bring the index up-to-date.
* `Docs/Tx`: indicates summary statistics for the number of documents per transaction. It supports additional information with &detail=true, &hist=true and &value=true.
* `Doc Transformation time (ms)`: indicates summary statistics for document transformation time. It supports additional information with &detail=true, &hist=true and &value=true.

## Troubleshooting

Use this information to repair a transaction that failed to index.

> **Note:** The default URL for the Solr index is `http://localhost:8080/solr/`

To repair an unindexed or failed transaction (as identified by the REPORT option in the [Unindexed Solr Transactions](#unindexed-transactions) section), run the following report:

```http
http://localhost:8080/solr/admin/cores?action=FIX
```

The `FIX` parameter compares the database with the index and identifies any missing or duplicate transactions. It then updates the index by either adding or removing transactions.

Use the PURGE parameter to remove transactions, acl transactions, nodes and acls from the index. It can also be used for testing wrong transactions and then to fix them.

```http
http://localhost:8080/solr/admin/cores?action=PURGE&txid=1&acltxid=2&nodeid=3&aclid=4
```

Use the `REINDEX` parameter to reindex a transaction, acl transactions, nodes and acls.

```http
http://localhost:8080/solr/admin/cores?action=REINDEX&txid=1&acltxid=2&nodeid=3&aclid=4
```

Use the `INDEX` parameter to create entries in the index. It can also be used to create duplicate index entries for testing.

```http
http://localhost:8080/solr/admin/cores?action=INDEX&txid=1&acltxid=2&nodeid=3&aclid=4
```

Use the `RETRY` parameter to retry indexing any node that failed to index and was skipped. In other words, it enables the users to attempt to fix documents that failed to index in the past and appear in the solr report (`http://localhost:8080/solr/admin/cores?action=REPORT&wt=xml`) with the field **Index error count**.

```http
http://localhost:8080/solr/admin/cores?action=RETRY
```

Use the following setting to specify an option core for the report. If it is absent, a report is produced for each core. For example:

```bash
&core=alfresco
&core=archive
```

You can also fix index issues, check the index cache and backup individual indexes by using JMX. The status of the index can be checked using the JMX client on the **JMX MBeans > Alfresco > solrIndexes > `<store>`** tabs. The default view is the Solr core summary. The operations run the same consistency checks that are available by URL.

## Solr troubleshooting for SSL configurations

When you have an Alfresco Content Services installation that requires an SSL configuration, you might encounter connection issues.

If Solr search and/or the Solr tracking is not working properly, you might see this message on the Tomcat console:

```text
Aug 22, 2011 8:19:21 PM org.apache.tomcat.util.net.jsse.JSSESupport handShake
WARNING: SSL server initiated renegotiation is disabled, closing connection
```

This message indicates that one side of the SSL connections is trying to renegotiate the SSL connection. This form of negotiation was found to be susceptible to man-in-the-middle attacks and it was disabled in the Java JSEE stack until a fix could be applied.

Refer to the following link for more information: [Transport Layer Security (TLS) Renegotiation Issue Readme](https://www.oracle.com/java/technologies/javase/tlsreadme2.html){:target="_blank"}.

Refer also to the following links:

* [https://www.gremwell.com/enabling\_ssl\_tls\_renegotiation\_in\_java](https://www.gremwell.com/enabling_ssl_tls_renegotiation_in_java){:target="_blank"}
* [https://tomcat.apache.org/tomcat-6.0-doc/config/http.html](https://tomcat.apache.org/tomcat-6.0-doc/config/http.html){:target="_blank"}

If your version of Java does not have the fix, you need to re-enable renegotiation by performing the following steps:

1. Add the `-Dsun.security.ssl.allowUnsafeRenegotiation=true` option to `JAVA_OPTS`.
2. Add the `allowUnsafeLegacyRenegotiation="true"` option to the Tomcat SSL connector.
---
title: SOLR Admin REST API
---
In addition to default SOLR Core Admin API actions, Alfresco SOLR provides several actions that can be executed via HTTP requests that specify an action parameter, with additional action specific arguments provided as additional parameters.

The Base URL for every action is:

```http
http://localhost:8983/solr/admin/cores?action=<action>
```

> **Note:** `<action>` is the name of the action to be invoked.

By default, responses are expressed in XML but if you add the URL parameter `wt=json` the response will be in JSON.

Every action response includes a `responseHeader` with the execution time and the status of the request.

```json{
    "responseHeader": {
      "QTime": 1,
      "status": 0
  }
}
```

> **Note:** When the status is `0`, the request has been executed successfully. You do need to review all additional nodes in the response to check they also executed successfully. When the status isn't `0`, the server logs contain an internal error raised by the request.

## Synchronous Actions

The execution of the action is performed as part of the request handling. An `action.status` value is included in the response that indicates if the action has been performed successfully or not. If the action fails, an additional `errorMessage` value is included in the response.

Generic `success` response:

```json
{
  "responseHeader": {
    "QTime": 1,
    "status": 0
  },
  "action": {
    "status": "success"
  }
}
```

Generic `error` response:

```json
{
   "responseHeader": {
      "QTime": 1,
      "status": 0
  },
  "action": {
    "errorMessage": "Core alfresco has NOT been created as storeRef param is required",
    "status": "error"
  }
}
```

## Actions for Cores

The following actions are for SOLR Core operations.

### `newCore` and its alias `newindex`

To create a new SOLR core.

```http
http://localhost:8983/solr/admin/cores?action=newCore&coreName=(coreName)&storeRef=(storeRef)
```

* **`(coreName)`**

    The name of the core you want to create.

* **`(storeRef)`**

    The name of the SOLR Core store. For example `workspace://SpaceStore`, `archive://SpaceStore`.

Optional URL parameters can be added to the URL.

* **`shardIds`**

    A string that includes a list of ShardIds that are separated with a comma.

* **`numShards`**

    The number of shards to be created.

* **`template`**

    The name of the SOLR template used to create the core (rerank, norerank).

* **`replicationFactor`**

    The number of core replicas.

* **`nodeInstance`**

    Number of the node instance.

* **`numNodes`**

    Number of nodes.

### `newDefaultIndex` and its alias `newdefaultcore`

To create a new core in SOLR with default settings.

```http
http://localhost:8983/solr/admin/cores?action=newDefaultIndex&coreName=(coreName)
```

* **`(coreName)`**

    The name of the core you want to create.

Optional URL parameters can be added to the URL.

* **`storeRef`**

    The name of the SOLR core store. For example workspace://SpaceStore, archive://SpaceStore.

* **`template`**

    The name of the SOLR template used to create the core (rerank, norerank).

### `updateCore` and its alias `updateindex`

To reload an existing core in Solr.

```http
http://localhost:8983/solr/admin/cores?action=updateCore&coreName=(coreName)
```

* **`(coreName)`**

    The name of the core you want to update.

### `check`

Enable check flag on a SOLR core or on every SOLR core.

```http
http://localhost:8983/solr/admin/cores?action=check
```

Optional URL parameters can be added to the URL.

* **`coreName`**

    The name of the core you want to create.

## Master/Slave differences of the admin endpoints

The table shows the differences of the admin endpoints.

|Action|Master|Slave|
|------|------|-----|
|check|Returns an empty response from Solr (only the response header) without an error message.|Same as master.|
|nodereport*|Full node report response is returned.|Minimal node report response including a warning message that alerts you about the slave nature of the receiver (i.e. "This response comes from a slave core and it contains minimal information").|
|aclreport*|Full acl report response is returned.|A response with a warning message that will alert you that the action is not available on slave nodes.|
|txreport|Full Tx report response is returned.|A response with a warning message that will alert you that the action is not available on slave nodes.|
|acltxreport*|Full response is returned.|A response with a warning message that will alert you that the action is not available on slave nodes.|
|rangecheck|Full RangeCheck response (only if the core is using `DBID_RANGE` routing).|A response with a warning message that will alert you that the action is not available on slave nodes.|
|expand|Full Expand response (only if the core is using `DBID_RANGE` routing).|A response with a warning message that will alert you that the action is not available on slave nodes.|
|report|Full core report.|A response with a warning message that will alert you that the action is not available on slave nodes.|
|purge, reindex, retry, index, fix|Action correctly executed.|No action taken. Empty response returned.|
|summary*|Master/Standalone node summary.|Slave node summary (minimal, compared with master).|
|new core/new index|No difference between master and slave.|No difference between master and slave.|
|updatecore/updateindex|No difference between master and slave.|No difference between master and slave.|
|updateshared|No difference between master and slave.|No difference between master and slave.|
|removecore|No difference between master and slave.|No difference between master and slave.|
|newdefaultindex/newdefaultcore|No difference between master and slave.|No difference between master and slave.|
|log4j|No difference between master and slave.|No difference between master and slave.|

> **Note:** * If the `core` or `coreName` parameter is missing the response will return the report for each registered core.

## Actions for Shards

The following actions are for SOLR shard operations.

### `rangecheck`

To get a detailed report including storage and sizing for the shards configured with the `Shard_DB_ID_RANGE` method.

> **Note:** If SOLR is not using this configuration, the node `expand` is set to `-1` in the response.

```http
http://localhost:8983/solr/admin/cores?action=rangecheck&coreName=(coreName)
```

* **`(coreName)`**

    The name of the core you want to check.

Sample successful response:

```json
{
  "responseHeader": {
    "QTime": 1,
    "status": 0
  },
  "action": {
    "status": "success"
  }
  "start": 0,
  "end": 10000,
  "nodeCount": 1000,
  "minDbid": 1,
  "maxDbid": 5000,
  "density": 50,
  "expand": 10000,
  "expanded": false
}
```

### `expand`

Use this to expand the range for a shard configured with the `DB_ID_RANGE` method when more than 75% of your space has been used. The configuration does not persist in the solrcore.properties file. If the expansion has not been applied, the node expand is set to `-1` in the response.

```http
http://localhost:8983/solr/admin/cores?action=expand&coreName=(coreName)&add=(add)
```

* **`(coreName)`**

    The name of the core you want to expand.

* **`(add)`**

    The count of the DB ID numbers to be added to the range.

Sample successful response:

```json
{
  "responseHeader": {
    "QTime": 1,
    "status": 0
  },
  "action": {
    "status": "success"
  }
  "expand": 10000
}
```

## Actions for Reloading Resources

The following actions are for reloading property files in memory for SOLR Cores.

### `updateShared`

To update memory loading from the shared.properties file for each core.

```http
http://localhost:8983/solr/admin/cores?action=updateShared
```

### `log4j`

To update memory loading from the log4j.properties file for each core.

```http
http://localhost:8983/solr/admin/cores?action=log4j
```

## Asynchronous Actions

The following actions are performed as part of a maintenance step in Tracker scheduled jobs. The value of `action.status` is always set to `scheduled` and the details of the action are logged with INFO level in classes `org.alfresco.solr.tracker.MetadataTracker` and `org.alfresco.solr.tracker.AclTracker`.

Sample `scheduled` Response:

```json
{
  "responseHeader": {
    "QTime": 1,
    "status": 0
  },
  "action": {
    "status": "scheduled"
  }
}
```

### `purge`

Add a `nodeid`, `txid`, `acltxid`, or `aclid` to be purged from a SOLR core or from every SOLR core on the next maintenance operation performed by `MetadataTracker` and `AclTracker`.

```http
http://localhost:8983/solr/admin/cores?action=purge
```

> **Note:** If indexing has been disabled the `purge` request cannot be executed. Enable indexing and then resubmit the command..

The optional URL parameters that can be added:

* **`core`**

    The name of the core to be purged.

* **`txid`**

    The number of the transaction to purge.

* **`acltxid`**

    The number of the ACL transaction to purge.

* **`nodeId`**

    The number of the node to purge.

* **`aclid`**

    The number of the ACL to purge.

### `reindex`

Add a `nodeid`, `txid`, `acltxid`, or `aclid` or SOLR query to be reindexed on a SOLR core or on every SOLR core on the next maintenance operation performed by the `MetadataTracker` and `AclTracker`. SOLR documents are removed and then indexed in this section.

```http
http://localhost:8983/solr/admin/cores?action=reindex
```

> **Note:** If indexing has been disabled the `reindex` request cannot be executed. Enable indexing and then resubmit the command..

The optional URL parameters that can be added:

* **`core`**

    The name of the core to be rendexed.

* **`txid`**

    The number of the transaction to reindex.

* **`acltxid`**

    The number of the ACL transaction to reindex.

* **`nodeId`**

    The number of the node to reindex.

* **`aclid`**

    The number of the ACL to purge.

* **`query`**

    The SOLR query to reindex the results, for example `cm:name:A*`.

### `retry`

Reindex every node marked as ERROR in a core or in every core. Error mode Ids are included in the response for every core.

```http
http://localhost:8983/solr/admin/cores?action=retry
```

> **Note:** If indexing has been disabled the `retry` request cannot be executed. Enable indexing and then resubmit the command..

The optional URL parameter that can be added:

* **`core`**

    The name of the core to be retried.

```json
{
  "responseHeader": {
    "QTime": 1,
    "status": 0
  },
  "action": {
    "status": "scheduled",
    "alfresco": [1, 2]
  }
}
```

### `fix`

Find transactions and ACLs missing or duplicated in the cores and add them to be reindexed on the next maintenance operation performed by `MetadataTracker` and `AclTracker` transactions. ACLs to be reindexed are included in the response.

```http
http://localhost:8983/solr/admin/cores?action=fix
```

> **Note:** If indexing has previously been disabled the `dryRun` parameter will be forced to be true which will result in no work being scheduled.

The optional URL parameters that can be added:

* **`core`**

    The name of the core to be fixed.

* **`dryRun`**

    This optional parameter when set to true generates a health report but reindex work is not scheduled. When set to false reindex work is scheduled. The default value is `true`.

* **`fromTxCommitTime`**

    This optional parameter indicates the lower bound (the minimum transaction commit time) of the target transactions that you want to check or fix.

* **`toTxCommitTime`**

    This optional parameter indicates the upper bound (the maximum transaction commit time) of the target transactions that you want to check or fix.

Sample `scheduled` response

```json
{
  {
     "responseHeader": {
         "QTime": 1,
         "status": 0
  },
  "action": {
      "status": "scheduled",
      "txToReindex": {
        "txInIndexNotInDb": {
             "192": 282  <- Tx 192 is associated to 282 nodes (they will be deleted)
             "827": 99   <- Tx 827 is associated to 99 nodes (they will be deleted)
              ...
         },
        "duplicatedTx": {
             "992": 8  <- Tx 992 is associated to 8 nodes (they will be deleted)
             "127": 82   <- Tx 127 is associated to 82 nodes (they will be deleted)
             ...
        },
        "missingTx": {
             "888": 84  <- Tx 888 is associated to 84 nodes (they will be added/replaced in the index)
             "929": 12   <- Tx 929 is associated to 12 nodes (they will be added/replaced in the index)
             ...
        }
      },
      "aclChangeSetToReindex": {
            // Provides the same subsection as txToReindex,
            // ACLTXID -> ACLs counts instead of TXID -> DBID
      }
}
```

### `enable-indexing`

Starts the tracking process. The following syntax enables indexing on all (master or standalone) cores:

```http
http://localhost:8983/solr/admin/cores?action=enable-indexing
```

If you call the REPORT action there will be additional information returned

```bash
<str name="ACL Tracker>enabled</str>
<str name="Metadata Tracker>enabled</str>
```

If you call the SUMMARY action there will be additional information returned

```bash
<bool name="ACLTracker Enabled">true</str>
<bool name="MetadataTracker Enabled">true</str>
<bool name="ContentTracker Enabled">true</str>
<bool name="CascadeTracker Enabled">true</str>
```

The URL parameters that can be used:

* **`core` (Optional)**

    The name of the core. In the instance that it is missing the command is applied to all master or standalone cores.

### `disable-indexing`

Stops the tracking process. The following syntax disables indexing on all (master or standalone) cores.:

> **Note:** If tracking has started and this command is used then a rollback of all the trackers is performed. To start tracking again, use ENABLED-INDEXING.

```http
http://localhost:8983/solr/admin/cores?action=disable-indexing
```

If you call the REPORT action there will be additional information returned

```bash
<str name="ACL Tracker>enabled</str>
<str name="Metadata Tracker>enabled</str>
```

If you call the SUMMARY action there will be additional information returned

```bash
<bool name="ACLTracker Enabled">true</str>
<bool name="MetadataTracker Enabled">true</str>
<bool name="ContentTracker Enabled">true</str>
<bool name="CascadeTracker Enabled">true</str>
```

The URL parameters that can be used:

* **`core` (Optional)**

    The name of the core. In the instance that it is missing the command is applied to all master or standalone cores.

## Generic Reports

The following actions return the requested report for a core including nodes, transactions, and ACLs.

### `report`

Get a detailed report for a specific core or for every core. The API accepts filtering based on `commitTime`, `txid`, and `acltxid`.

```http
http://localhost:8983/solr/admin/cores?action=report
```

Optional URL parameters can be added:

* **`core`**

    The name of the core used to get the report.

* **`fromTime`**

    The time from transaction commit to filtering the report results.

* **`toTime`**

    The time to transaction commit to filtering the report results.

* **`fromTx`**

    From transaction Id to filtering report results.

* **`toTx`**

    To transaction Id time to filter report results.

* **`toCalTx`**

    To ACL tranasction Id to filter transaction Id time to filter report results.

Sample response

```json
{
  "responseHeader": {
    "QTime": 2834,
    "status": 0
  },
  "report": {
    "alfresco": {
      "Node count with FTSStatus Dirty": 0,
      "Last indexed change set commit time": 1580999915335,
      "Count of acl transactions in the index but not the DB": 0,
      "Index node count": 1783,
      "Last TX id before holes": -1,
      "Index unindexed count": 0,
      "Count of duplicate unindexed docs in the index": 0,
      "Index error count": 0,
      "Count of duplicated acl transactions in the index": 0,
      "Node count with FTSStatus Clean": 495,
      "Count of missing acl transactions from the Index": 0,
      "Last indexed transaction commit date": "2020-02-06T14:38:35",
      "DB transaction count": 557,
      "Last indexed change set commit date": "2020-02-06T14:38:35",
      "Count of missing transactions from the Index": 0,
      "Count of duplicate nodes in the index": 0,
      "Count of duplicated transactions in the index": 0,
      "Index unique acl transaction count": 223,
      "Index transaction count": 555,
      "DB acl transaction count": 225,
      "Last indexed transaction commit time": 1580999915357,
      "Index acl transaction count": 223,
      "Count of transactions in the index but not the DB": 0,
      "Alfresco version": "5.0.0",
      "Last changeset id before holes": -1,
      "Count of duplicate error docs in the index": 0,
      "Node count with FTSStatus New": 0,
      "Index unique transaction count": 555
    }
  }
}
```

The **`report`** action compares the database with the index and generates an overall status report with the following details:

* DB transaction count: the transaction count on the database.
* DB acl transaction count: the ACL transaction count on the database.
* Count of duplicated transactions in the index: the number of transactions that appear more than once in the index. The value of this property should be zero. If it isn't zero there is an issue with the index.
* Count of duplicated acl transactions in the index: the number of ACL transactions that appear more than once in the index. The value of this property should be zero. If it isn't zero there is an issue with the index.
* Count of transactions in the index but not the database: the number of transactions in the index but not in the database. This count includes empty transactions that have been purged from the database. The value of this property should be zero. If it isn't zero there is an issue with the index.
* Count of acl transactions in the index but not the DB: the number of ACL transactions in the index but not in the database. The value of this property should be zero. If it isn't zero there is an issue with the index.

    > **Note:** Empty ACL transactions are not purged from the database.

* Count of missing transactions from the Index: the number of transactions in the database but not in the index. The value of this index should be zero when the index is up-to-date.
* Count of missing acl transactions from the Index: the number of ACL transactions in the database but not in the index. The value of this property should be zero when the index is up-to-date.
* Index transaction count: the number of transactions in the index.
* Index acl transaction count: the number of ACL transactions in the index.
* Index unique transaction count: the number of unique transactions in the index.
* Index unique acl transaction count: the number of unique ACL transactions in the index.
* Index leaf count: the number of docs and folders in the index.
* Count of duplicate leaves in the index: the number of duplicate docs or folders in the index. The value of this property should be zero. If it isn't zero there is an issue with the index.
* Last index commit time: the time stamp for the last transaction added to the index. It also indicates that transactions after this time stamp have not yet been indexed.
* Last Index commit date: the time stamp set as a date for the last transaction added to the index. It also indicates that transactions after this date have not yet been indexed.
* Last TX id before holes: indicates that transactions after this ID will be checked again to make sure they have not been missed. This is computed from the index at start up time. By default, it is set an hour after the last commit time found in the index. Solr tracking, by default, goes back an hour from the current time to check that no transactions have been missed.
* First duplicate: indicates if there are duplicate transactions in the index. It returns the ID of the first duplicate transaction.
* First duplicate acl tx: indicates if there are duplicate ACL transactions in the index. It returns the ID of the first duplicate ACL transaction.
* First transaction in the index but not the DB: if the related count is > 0, it returns the ID of the first offender.
* First acl transaction in the index but not the DB: if the related count is > 0, it returns the ID of the first offender.
* First transaction missing from the Index: if the related count is > 0, it returns the ID of the first offender.
* irst acl transaction missing from the Index: if the related count is > 0, it returns the ID of the first offender.
* First duplicate leaf in the index: if the related count is > 0, it returns the ID of the first offender.

### `summary`

Get a detailed report for a core for every core including information related to handlers and trackers.

```http
http://localhost:8983/solr/admin/cores?action=summary&core=(coreName)
```

Optional URL parameters can be added:

* **`detail`**

    When true provides statistics per tracking thread.

* **`hist`**

    When true provides a histogram of the times taken for tracking operations for each tracking thread.

* **`values`**

    When true adds reports for the last 50 values recorded for each tracking operation for each thread.

    > **Note:** This parameter is boolean and when false returns 0 values for each tracking operation for each thread.

* **`reset`**

    When true resets all tracking statistics.

Sample response

```json
{
    "responseHeader":{
      "QTime":13,
      "status":0
    },
    "Summary":{
      "alfresco":{
          "Id for last Change Set in index":226,
          "MetadataTracker Active":false,
          "Alfresco Transactions in Index":555,
          "Date for last TX on server":"2020-02-06T14:41:59.950Z",
          "/alfresco":{
            "75thPcRequestTime":0,
            "5minRateRequestsPerSecond":0,
            "totalTime":0,
            "timeouts":0,
            "clientErrors":0,
            "requests":0,
            "avgRequestsPerSecond":0,
            "medianRequestTime":0,
            "serverErrors":0,
            "15minRateRequestsPerSecond":0,
            "avgTimePerRequest":0,
            "999thPcRequestTime":0,
            "handlerStart":1581000031727,
            "99thPcRequestTime":0,
            "errors":0,
            "95thPcRequestTime":0
        },
        "/cmis":{
            "75thPcRequestTime":0,
            "5minRateRequestsPerSecond":0,
            "totalTime":0,
            "timeouts":0,
            "clientErrors":0,
            "requests":0,
            "avgRequestsPerSecond":0,
            "medianRequestTime":0,
            "serverErrors":0,
            "15minRateRequestsPerSecond":0,
            "avgTimePerRequest":0,
            "999thPcRequestTime":0,
            "handlerStart":1581000031728,
            "99thPcRequestTime":0,
            "errors":0,
            "95thPcRequestTime":0
        },
        "Last Index Change Set Commit Time":1580999915335,
        "Model sync times (ms)":{
            "Mean":246.96260820000003,
            "StdDev":326.9164253039973,
            "Min":94.789114,
            "Start":"2020-02-06T14:40:33.545Z",
            "Max":1161.517117,
            "Varience":106874.34913354406,
            "N":10
        },
        "ContentTracker Active":false,
        "Alfresco Error Nodes in Index":0,
        "Acl index time (ms)":{
            "Mean":13.28818242857143,
            "StdDev":25.299723059509738,
            "Min":0.568837,
            "Start":"2020-02-06T14:40:40.367Z",
            "Max":99.07898,
            "Varience":640.0759868878888,
            "N":14
        },
        "Alfresco States in Index":2,
        "Doc Transformation time (ms)":{
            "Mean":134.3180220945674,
            "StdDev":122.68196650026313,
            "Min":12.922844,
            "Start":"2020-02-06T14:41:00.304Z",
            "Max":1585.515237,
            "Varience":15050.864904371685,
            "N":497
        },
        "/alfrescoAuthorityCache":{
            "lookups":0,
            "hits":0,
            "cumulative_evictions":0,
            "size":0,
            "hitratio":0,
            "evictions":0,
            "cumulative_lookups":0,
            "cumulative_hitratio":0,
            "warmupTime":0,
            "inserts":0,
            "cumulative_inserts":0,
            "cumulative_hits":0
        },
        "Approx content indexing time remaining":"0.095 Seconds",
        "Approx change sets remaining":1,
        "Approx transactions remaining":2,
        "/filterCache":{
            "lookups":15,
            "hits":15,
            "cumulative_evictions":0,
            "size":8,
            "hitratio":1,
            "evictions":0,
            "cumulative_lookups":15,
            "cumulative_hitratio":1,
            "warmupTime":0,
            "inserts":8,
            "cumulative_inserts":8,
            "cumulative_hits":15
        },
        "Last Index TX Commit Date":"2020-02-06T14:38:35.357Z",
        "TX Duration":"P0YT3M24.593S",
        "Searcher":{
            "numDocs":3269,
            "searcherName":"Searcher@b4ba711[alfresco] main",

"reader":"ExitableDirectoryReader(UninvertingDirectoryReader(Uninverting(_b(6.
6.0):C3268/355:delGen=1) Uninverting(_7(6.6.0):C1)
Uninverting(_c(6.6.0):C355)))",
             "deletedDocs":355,
             "registeredAt":"2020-02-06T14:41:20.191Z",
             "maxDoc":3624,
             "indexVersion":40,
             "warmupTime":0,
             "caching":true,

"readerDir":"org.apache.lucene.store.NRTCachingDirectory:NRTCachingDirectory(M
MapDirectory@/opt/alfresco-search-services/solrhome/alfresco/index
lockFactory=org.apache.lucene.store.NativeFSLockFactory@1fba8d61;
maxCacheMB=48.0 maxMergeSizeMB=4.0)",
              "openedAt":"2020-02-06T14:41:20.188Z"
            },
            "Per node B":2689,
            "Node index time (ms)":{
              "Mean":1.8261068141263945,
              "StdDev":3.3853503764200137,
              "Min":0.018597,
              "Start":"2020-02-06T14:40:41.487Z",
              "Max":97.921274,
              "Varience":11.460597171127128,
              "N":2690
            },
            "Active":false,
            "/alfrescoPathCache":{
              "lookups":0,
              "hits":0,
              "cumulative_evictions":0,
              "size":0,
              "hitratio":0,
              "evictions":0,
              "cumulative_lookups":0,
              "cumulative_hitratio":0,
              "warmupTime":0,
              "inserts":0,
              "cumulative_inserts":0,
              "cumulative_hits":0
            },
            "Change Set Lag":"204 s",
            "Alfresco Unindexed Nodes":0,
            "Id for last TX in index":885,
            "Approx change set indexing time remaining":"0.005 Seconds",
            "FTS":{
              "Node count with FTSStatus Dirty":0,
              "Node count with FTSStatus Clean":495,
              "Node count with FTSStatus New":0
            },
            "Date for last Change Set on server":"2020-02-06T14:41:59.890Z",
            "Total Searcher Cache (GB)":0,
            "Timestamp for last TX on server":1581000119950,
            "Last Index TX Commit Time":1580999915357,
            "/afts":{
              "75thPcRequestTime":0,
              "5minRateRequestsPerSecond":0,
              "totalTime":0,
              "timeouts":0,
              "clientErrors":0,
              "requests":0,
              "avgRequestsPerSecond":0,
              "medianRequestTime":0,
              "serverErrors":0,
              "15minRateRequestsPerSecond":0,
              "avgTimePerRequest":0,
              "999thPcRequestTime":0,
              "handlerStart":1581000031727,
              "99thPcRequestTime":0,
              "errors":0,
              "95thPcRequestTime":0
            },
            "/queryResultCache":{
              "lookups":27,
              "hits":16,
              "cumulative_evictions":0,
              "size":11,
              "hitratio":0.59,
              "evictions":0,
              "cumulative_lookups":27,
              "cumulative_hitratio":0.59,
              "warmupTime":0,
              "inserts":11,
              "cumulative_inserts":11,
              "cumulative_hits":16
            },
            "Timestamp for last Change Set on server":1581000119890,
            "Number of Searchers":1,
            "AclTracker Active":false,
            "Searcher-0":{
              "Searcher":{
                "numDocs":3269,
                "searcherName":"Searcher@b4ba711[alfresco] main",
"reader":"ExitableDirectoryReader(UninvertingDirectoryReader(Uninverting(_b(6.
6.0):C3268/355:delGen=1) Uninverting(_7(6.6.0):C1)
Uninverting(_c(6.6.0):C355)))",
                "deletedDocs":355,
                "registeredAt":"2020-02-06T14:41:20.191Z",
                "maxDoc":3624,
                "indexVersion":40,
                "warmupTime":0,
                "caching":true,
"readerDir":"org.apache.lucene.store.NRTCachingDirectory:NRTCachingDirectory(M
MapDirectory@/opt/alfresco-search-services/solrhome/alfresco/index
lockFactory=org.apache.lucene.store.NativeFSLockFactory@1fba8d61;
maxCacheMB=48.0 maxMergeSizeMB=4.0)",
"openedAt":"2020-02-06T14:41:20.188Z"
            }
         },
         "ModelTracker Active":false,
         "Alfresco Acl Transactions in Index":223,
         "Last Index Change Set Commit Date":"2020-02-06T14:38:35.335Z",
         "Docs/Tx":{
            "Mean":5.816216216216217,
            "StdDev":25.00964629977419,
            "Min":1,
            "Start":"2020-02-06T14:40:43.852Z",
            "Max":547,
            "Varience":625.4824080398088,
            "N":555
           },
           "Approx transaction indexing time remaining":"0.047 Seconds",
           "Id for last Change Set on server":227,
           "TX Lag":"204 s",
           "Alfresco Acls in Index":706,
           "Change Set Duration":"P0YT3M24.555S",
           "Id for last TX on server":887,
           "Alfresco Nodes in Index":1783,
           "On disk (GB)":"0.004466"
       }
   }
}
```

The `summary` action provides the status of the tracking index and reports the progress of each tracking thread and generates a report with the following details:

* Active: the tracker for the core active.
* Last Index Commit Time: the time stamp for the last transaction that was indexed.
* Last Index Commit Date: indicates the time stamp as a date for the last transaction that was indexed.

    > **Note:** Changes made after this time are not yet in the index.

* Lag: the difference in seconds between the last transaction time stamp on the server and the time stamp for the last transaction that was indexed.
* Duration: the time lag as an XML duration.
* Approx transactions remaining: the approximate number of transactions to index in order to bring the index up-to-date. It is calculated by using the last transaction ID on the server minus the last transaction ID indexed. It includes all the missing and empty transactions.
* Approx transaction indexing time remaining: it is based on approx transactions remaining, the average number of nodes per transaction and the average time to index a node (how long the index will take to be up-to-date). The estimate is seconds, minutes, hours and days.
* Model sync times (ms): summary statistics for the model sync time. It supports additional information with &detail=true, &hist=true and &value=true.
* Acl index time (ms): summary statistics for ACL index time. It supports additional information with &detail=true, &hist=true and &value=true.
* Node index time (ms): summary statistics for node index time. It supports additional information with &detail=true, &hist=true and &value=true.
* Acl tx index time (ms): summary statistics for ACL transaction index time. It supports additional information with &detail=true, &hist=true and &value=true.
* Tx index time (ms): summary statistics for transaction index time. It specifies the estimated time required to bring the index up-to-date.
* Docs/Tx: summary statistics for the number of documents per transaction. It supports additional information with &detail=true, &hist=true and &value=true.
* Doc Transformation time (ms): summary statistics for document transformation time. It supports additional information with &detail=true, &hist=true and &value=true.

## Specific Reports

The following actions return the requested report for a node, transaction, and an ACL.

### `nodeReport`

Get a report from a nodeId with the associated `txId` and the indexing status.

```http
http://localhost:8983/solr/admin/cores?action=nodeReport&nodeid=(nodeid)
```

* **`(nodeid)`**

    The Id of the node to get the report.

Optional URL parameters can be added:

* **`core`**

    The name of the core used to get the report.

Sample response.

```json
{
  "responseHeader": {
    "QTime": 110,
    "status": 0
  },
  "report": {
    "alfresco": {
      "Node DBID": 200,
      "DB TX status": "UPDATED",
      "DB TX": 6,
      "Indexed Node Doc Count": 0
    },
    "archive": {
      "Node DBID": 200,
      "DB TX status": "UPDATED",
      "DB TX": 6,
      "Indexed Node Doc Count": 0
    }
  }
}
```

### `aclReport`

Get a report from an aclId with the count of documents associated with the ACL.

```http
http://localhost:8983/solr/admin/cores?action=aclReport&aclid=(aclid)
```

* **`(aclid)`**

    The Id of the ACL to get the report.

Optional URL parameters can be added:

* **`core`**

    The name of the core used to get the report.

Sample response.

```json
{
  "responseHeader": {
    "QTime": 31,
    "status": 0
  },
  "report": {
    "alfresco": {
      "Acl doc in index": 1,
      "Acl Id": 1
    },
    "archive": {
        "Acl doc in index": 1,
        "Acl Id": 1
    }
  }
}
```

### `txReport`

Get a report from a txId with detailed information related to the transaction.

```http
http://localhost:8983/solr/admin/cores?action=txReport&txid=(txid)
```

* **`(txid)`**

    The Id of the transaction to get the report.

Optional URL parameters can be added:

* **`core`**

    The name of the core used to get the report.

Sample response.

```json
{
  "responseHeader": {
    "QTime": 162,
  "status": 0
  },
  "report": {"alfresco": {
    "txDbNodeCount": 0,
    "nodes": {},
    "TXID": 1,
    "transaction": {
        "Node count with FTSStatus Dirty": 0,
        "Last indexed change set commit time": 1581004383258,
        "Count of acl transactions in the index but not the DB": 0,
        "Index node count": 1837,
        "Last TX id before holes": -1,
        "Index unindexed count": 0,
        "Count of duplicate unindexed docs in the index": 0,
        "Index error count": 0,
        "Count of duplicated acl transactions in the index": 0,
        "Node count with FTSStatus Clean": 501,
        "Count of missing acl transactions from the Index": 0,
        "Last indexed transaction commit date": "2020-02-06T15:53:03",
        "DB transaction count": 1,
        "Last indexed change set commit date": "2020-02-06T15:53:03",
        "Count of missing transactions from the Index": 0,
        "Count of duplicate nodes in the index": 0,
        "Count of duplicated transactions in the index": 0,
        "Index unique acl transaction count": 235,
        "Index transaction count": 568,
        "DB acl transaction count": 0,
        "Last indexed transaction commit time": 1581004383280,
        "Index acl transaction count": 235,
        "Count of transactions in the index but not the DB": 0,
        "Alfresco version": "5.0.0",
        "Last changeset id before holes": -1,
        "Count of duplicate error docs in the index": 0,
        "Node count with FTSStatus New": 0,
        "Index unique transaction count": 568
    }
  }}
}
```

### `aclTxreport`

Get a report from a aclTxId with detailed information related to nodes indexed for an ACL inside a transaction.

```http
http://localhost:8983/solr/admin/cores?action=aclTxReport&acltxid=(acltxid)
```

* **`acltxid`**

    The Id of the ACL transaction to get the report.

Optional URL parameters can be added:

 **`core`**

   The name of the core to get the report.

Sample response.

```json
{
    "responseHeader": {
      "QTime": 296,
        "status": 0
    },
    "report": {
      "alfresco": {
         "nodes": {
            "ACLID 1": {
                "Acl doc in index": null,
                "Acl Id": 1
            },
            "ACLID 2": {
                "Acl doc in index": null,
                "Acl Id": 2
            }
          },
          "aclTxDbAclCount": 2,
          "TXID": 1,
          "transaction": {
            "Node count with FTSStatus Dirty": 0,
            "Last indexed change set commit time": 1581004503216,
            "Count of acl transactions in the index but not the DB": 0,
            "Index node count": 1846,
            "Last TX id before holes": -1,
            "Index unindexed count": 0,
            "Count of duplicate unindexed docs in the index": 0,
            "Index error count": 0,
            "Count of duplicated acl transactions in the index": 0,
            "Node count with FTSStatus Clean": 502,
            "Count of missing acl transactions from the Index": 0,
            "Last indexed transaction commit date": "2020-02-06T15:55:03",
            "DB transaction count": 0,
            "Last indexed change set commit date": "2020-02-06T15:55:03",
            "Count of missing transactions from the Index": 0,
            "Count of duplicate nodes in the index": 0,
            "Count of duplicated transactions in the index": 0,
            "Index unique acl transaction count": 237,
            "Index transaction count": 571,
            "DB acl transaction count": 1,
            "Last indexed transaction commit time": 1581004503241,
            "Index acl transaction count": 237,
            "Count of transactions in the index but not the DB": 0,
            "Alfresco version": "5.0.0",
            "Last changeset id before holes": -1,
            "Count of duplicate error docs in the index": 0,
            "Node count with FTSStatus New": 0,
            "Index unique transaction count": 571
          }
        }
    }
}
```
---
title: Filtered search
---

Use this information to get an overview of the filtered search capability in Alfresco Share along with its configuration details. It also describes how to define your own custom filters.

Filtered search is a powerful search feature that allows users to filter and customize their results by applying multiple filters to their search results in a navigational way. Filtered search breaks up search results into multiple categories, typically showing counts for each, and allows the user to drill down or further restrict their search results based on those filters.

You can configure filtered search either by using the Filtered search configuration properties or by using the [Search Manager]({% link content-services/latest/admin/share-admin-tools.md %}#search-manager).

## Filtered search configuration properties

There are a number of default filtered search configuration properties defined. The default filtered search properties are explained here.

The following example shows how the default filters are defined:

```bash
#
# Alfresco default facets
# Note: If you have changed the filter's default value(s) via Share, then any
# subsequent changes of those default values won't be applied to the filter on
# server startup.
#

# Field-Facet-Qname => cm:content.mimetype
default.cm\:content.mimetype.filterID=filter_mimetype
default.cm\:content.mimetype.displayName=faceted-search.facet-menu.facet.formats
default.cm\:content.mimetype.displayControl=alfresco/search/FacetFilters
default.cm\:content.mimetype.maxFilters=5
default.cm\:content.mimetype.hitThreshold=1
default.cm\:content.mimetype.minFilterValueLength=4
default.cm\:content.mimetype.sortBy=DESCENDING
default.cm\:content.mimetype.scope=ALL
default.cm\:content.mimetype.scopedSites=
default.cm\:content.mimetype.isEnabled=true

# Field-Facet-Qname => cm:creator
default.cm\:creator.filterID=filter_creator
default.cm\:creator.displayName=faceted-search.facet-menu.facet.creator
default.cm\:creator.displayControl=alfresco/search/FacetFilters
default.cm\:creator.maxFilters=5
default.cm\:creator.hitThreshold=1
default.cm\:creator.minFilterValueLength=4
default.cm\:creator.sortBy=ALPHABETICALLY
default.cm\:creator.scope=ALL
default.cm\:creator.scopedSites=
default.cm\:creator.isEnabled=true

# Field-Facet-Qname => cm:modifier
default.cm\:modifier.filterID=filter_modifier
default.cm\:modifier.displayName=faceted-search.facet-menu.facet.modifier
default.cm\:modifier.displayControl=alfresco/search/FacetFilters
default.cm\:modifier.maxFilters=5
default.cm\:modifier.hitThreshold=1
default.cm\:modifier.minFilterValueLength=4
default.cm\:modifier.sortBy=ALPHABETICALLY
default.cm\:modifier.scope=ALL
default.cm\:modifier.scopedSites=
default.cm\:modifier.isEnabled=true

# Field-Facet-Qname => cm:created
default.cm\:created.filterID=filter_created
default.cm\:created.displayName=faceted-search.facet-menu.facet.created
default.cm\:created.displayControl=alfresco/search/FacetFilters
default.cm\:created.maxFilters=5
default.cm\:created.hitThreshold=1
default.cm\:created.minFilterValueLength=4
default.cm\:created.sortBy=INDEX
default.cm\:created.scope=ALL
default.cm\:created.scopedSites=
default.cm\:created.isEnabled=true

# Field-Facet-Qname => cm:modified
default.cm\:modified.filterID=filter_modified
default.cm\:modified.displayName=faceted-search.facet-menu.facet.modified
default.cm\:modified.displayControl=alfresco/search/FacetFilters
default.cm\:modified.maxFilters=5
default.cm\:modified.hitThreshold=1
default.cm\:modified.minFilterValueLength=4
default.cm\:modified.sortBy=INDEX
default.cm\:modified.scope=ALL
default.cm\:modified.scopedSites=
default.cm\:modified.isEnabled=true

# Field-Facet-Qname => cm:content.size
default.cm\:content.size.filterID=filter_content_size
default.cm\:content.size.displayName=faceted-search.facet-menu.facet.size
default.cm\:content.size.displayControl=alfresco/search/FacetFilters
default.cm\:content.size.maxFilters=5
default.cm\:content.size.hitThreshold=1
default.cm\:content.size.minFilterValueLength=4
default.cm\:content.size.sortBy=INDEX
default.cm\:content.size.scope=ALL
default.cm\:content.size.scopedSites=
default.cm\:content.size.isEnabled=true
```

### Filter property description

An example of a filter is `cm:modified`. It specifies the name of the filter field. It is the field on which you want to do a filtered search.

**filterID** - Specifies a unique name to identify the filter. Before adding a new filter, check the existing filters [Search Manager]({% link content-services/latest/admin/share-admin-tools.md %}#search-manager) to ensure that the `filterID` does not already exist.

**displayName** - Specifies the display name of the filter.

**displayControl** - Enables the user to decide the user interface control or how the filter is displayed on the **Search** page. The default option is **Check box**. `displayControl` is the full module name for an Aikau widget which is used for rendering the facet filters. By default, Alfresco Content Services provides `alfresco/search/FacetFilters` which is a basic rendering of the filters available for the facet.

**maxFilters** - Enables the user to select the maximum number of filters shown for search results. You can select to show more than one filter.

**hitThreshold** - Enables the user to select the minimum number of matches a filter result must have to be shown on the **Search** page.

**minFilterValueLength** - Specifies the minimum length of characters that a filter value must have to be displayed. This can be useful in hiding common short words.

**sortBy** - Enables the user to select the order in which the filter results must be shown on the **Search** page. The `sortBy` option is passed to the `FacetFilters` widget and defines how the filters should be sorted. This property has the following options:

|Option|Description|
|------|-----------|
|ALPHABETICALLY|Specifies the filter value A-Z.|
|REVERSE_ALPHABETICALLY|Specifies the filter value Z-A.|
|ASCENDING|Specifies the number of filter results (low to high).|
|DESCENDING|Specifies the number of filter results (high to low).|
|INDEX|This is a special value reserved for results rendered by filter queries.|

**scope** - Enables the user to select the sites where the filter will be available.

**scopedSites** - Displays a list of sites where the filter will be available.

**isEnabled** - Specifies if the filter is enabled for inclusion on the search results page. Disabled filters are not displayed. Only the filters you create via the Share console can be deleted; default filters must be disabled to hide them.

> **Note:** You cannot delete or modify any of the default filters, however you can disable them. To define your own custom filters, see [Defining custom search filters using configuration file](#defining-custom-search-filters-using-configuration-file).

## Defining custom search filters using configuration file

You can define and create your own custom filters for being displayed on the search results page.

You can define custom filters in the solr-facets-config-custom.properties file. You can also use this file to override the default filter properties.

1. Navigate to the `<classpathRoot>/alfresco/extension` directory.

2. Create the `solr-facets-config-custom.properties` file.

3. Open the `solr-facets-config-custom.properties` file and specify your custom filter properties.

    Here's an example of custom filter configuration:

    ```bash
    custom.cm\:description.filterID=filter_newFilter
    custom.cm\:description.displayName=faceted-search.facet-menu.facet.description
    custom.cm\:description.displayControl=alfresco/search/FacetFilters
    custom.cm\:description.maxFilters=3
    custom.cm\:description.hitThreshold=1
    custom.cm\:description.minFilterValueLength=2
    custom.cm\:description.sortBy=DESCENDING
    custom.cm\:description.scope=SCOPED_SITES
    custom.cm\:description.scopedSites=
    custom.cm\:description.isEnabled=true
    ```

    > **Note:** The values specified in the custom filters will overwrite the default filter's value. However, if you change the filter's default value(s) via Share, then any subsequent changes made to the filter values via the configuration files, won't be applied to the filter on server startup.---
title: Overview
---

Use the following information to configure Search and Insight Engine.

## Search and Insight Engine subsystem

There is a search subsystem and it can be used to connect to Search and Insight Engine (which is based on Solr 6).

Just like all previous versions of Solr, the activation and configuration of the Search and Insight Engine subsystem can be done by using either the `alfresco-global.properties` file or the Admin Console (see [Configuring using the Admin Console](#configure-using-the-admin-console)).

If you haven't set the following Solr-related properties in the `TOMCAT_HOME>/shared/classes/alfresco-global.properties` file, add these:

```bash
### Solr indexing ###
index.subsystem.name=solr6
solr.secureComms=https
solr.port=8983
solr.host=<hostname> [The host name where the Solr instance is located]
solr.baseUrl=/solr
```

These configuration properties are used by Alfresco Content Services to talk to Search and Insight Engine.

## Configure using the Admin Console

The topic describes the properties for configuring the Solr 6 search service.

1. Open the Admin Console. For more information, see [Launch Admin Console]({% link content-services/latest/admin/admin-console.md %}#launch-admin-console).

2. In the Repository Services section, click **Search Service** to see the Search Service page.

3. In the **Search Service** section, select **Solr 6** from the **Search Service In Use** list.

4. Set the Search and Insight Engine properties:

    |Solr search property|Description|
    |--------------------|-----------|
    |Content Tracking Enabled|This setting can be used to disable Solr 6 tracking by separate Solr instance(s) configured to track this server, for example `Yes`|
    |Solr Port (Non-SSL)|This specifies the application server's http port (non-secure) on which Solr 6 is running. This is only used if Solr 6 is configured to run without secure communications, for example `8080`|
    |Solr base URL|This specifies the base URL for the Solr 6 web application. Adjusting the URL does not change where Solr is hosted, it changes where Alfresco Content Services looks for Solr, for example `/solr6`.|
    |Solr Hostname|his specifies the hostname on which the Solr 6 server is running. Use localhost if running on the same machine, for example `localhost`.|
    |Solr SSL Port|his specifies the application server's https port on which Solr 6 is running, for example `8443`.|
    |Auto Suggest Enabled|This specifies that the Solr 6 auto-suggest feature is enabled. This feature presents suggestions of popular queries as a user types their query into the search box or text box, for example `0` .|
    |Last Indexed Transaction|This specifies the transaction ID most recently indexed by Solr 6, for example `17`.|
    |Approx Index Time Remaining|This specifies the estimated time that Solr 6 will take to complete indexing the current outstanding transactions, for example 0 seconds.|
    |Disk Usage (GB)|This specifies the disk space used by the latest version of the Solr 6 index. Allow at least double this value for background indexing management, for example `0.001748`.|
    |Index Lag|This specifies the time that indexing is currently behind the repository updates, for example `0 seconds`.|
    |Approx Transactions to Index|This specifies the estimated number of outstanding transactions that require indexing, for example 0.|
    |Indexing in Progress|This specifies if Solr 6 is currently indexing outstanding transactions, for example  .|
    |Memory Usage (GB)|This specifies the current memory usage. The value may vary due to transient memory used by background processing. The value does not include Lucene related caches, for example `No`.|
    |Backup Location (Main Store)|This specifies the location where the index backup for the main WorkspaceStore is stored on the Solr 6 server, for example `${dir.root}/solr6Backup/alfresco`.|
    |Backup Cron Expression (Main Store)|This specifies a unix-like expression, using the same syntax as the cron command, that defines when backups occur. The default value is 0 0 2 \* * ? meaning the backup is performed daily at 02.00.|
    |Backups To Keep (Main Store)|This specifies the number of backups to keep (including the latest backup), for example `3`.|
    |Backup Location (Archive Store properties)|This specifies the location where the index backup for ArchiveStore is stored on the Solr 6 server, for example `${dir.root}/solr6Backup/archive`.|
    |Backup Cron Expression (Archive Store properties)|This specifies a unix-like expression, using the same syntax as the cron command, that defines when backups occur. The default value is 0 0 4 \* * ? meaning the backup is performed daily at 04.00.|
    |Backups To Keep (Archive Store properties)|This specifies the number of backups to keep, for example `3`.|
    |CMIS Query|This specifies the default mode which defines if and when the database should be used to support a subset of the CMIS Query Language, for example `Use database if possible`.|
    |Alfresco Full Text Search|This specifies the default mode which defines if and when the database should be used to support a subset of the Alfresco Full Text Search, for example Use database if possible.|

5. Click **Save** to apply the changes you have made to the properties.

If you do not want to save the changes, click **Cancel**.

## Search and Insight Engine directory structure

After you've installed Search and Insight Engine, several directories and configuration files related to Solr will be available in the Search and Insight Engine home directory.

The Search and Insight Engine distribution (`alfresco-insight-engine-distribution-2.0.x.zip`) contains the following artifacts:

### solrhome directory

This is the Solr configuration directory that is specific to Alfresco. It contains the following sub-folders and files:

|Folder/File|Description|
|-----------|-----------|
|alfrescoModels|When you install Search and Insight Engine, it creates an empty alfrescoModels directory. When Solr first talks to Alfresco, it pulls the model definitions into this directory.|
|conf|This directory contains the shared.properties file. See [Search and Insight Engine externalized configuration](#search-and-insight-engine-externalized-configuration).|
|templates|This directory contains the core templates that define the base configuration for a new Solr core with some configuration properties. This directory also contains the `/rerank/conf/solrcore.properties` file which you can use to customize the Solr cores.|
|solr.xml|This file defines the Solr web application context. For more information see [Format of solr.xml](https://lucene.apache.org/solr/guide/6_6/format-of-solr-xml.html){:target="_blank"}|
|data|This folder is generated when a Solr core is created and is where Solr indexes are stored. The default location of the folder is `/opt/alfresco-search-services/data`.|

### logs directory

This directory contains the Solr-specific logging configuration file.

|Folder/File|Description|
|-----------|-----------|
|log4j.properties|This is the configuration file for Solr-specific logging. The Solr log file can be found at `<SOLR_HOME>/logs/solr.log`.|

* `solr directory`: This directory contains the Solr binaries and runtime Java library files.
* `solr.in.cmd`: Use this file to specify additional Solr configuration options for Windows.
* `solr.in.sh`: Use this file to specify additional Solr configuration options for non-Windows platforms, such as Linux and Mac OS X.
* `README.MD`: This file provides version information for Alfresco Content Services, Search and Insight Engine, and Solr.

### Search and Insight Engine externalized configuration

As a best practice, use the `alfresco-insight-engine/solr.in.sh` file (Linux-based platform) or `alfresco-insight-engine/solr.in.cmd` file (Windows-based platform) to set the external configuration that applies to all the Search and Insight Engine cores.

> **Note:** For any property, only the environment variables should be specified in the solr.in.sh/ solr.in.cmd file. For example, `SOLR_SOLR_HOST`, `SOLR_SOLR_PORT`, or `SOLR_ALFRESCO_PORT`.

The following configuration properties are used by an external client, such as Alfresco to talk to Solr. Besides the solr.in.sh/ solr.in.cmd file, you can also set these properties in the `alfresco-insight-engine/solrhome/conf/shared.properties` file.

> **Important:** From Search and Insight Engine 2.0 the `solr.content.dir` property has been removed. The `solr.content.dir` was a filesystem-based extension of the Solr index. It was used for maintaining a copy of the original data indexed in Solr. The storage the `solr.content.dir` provided is available in Solr itself which means that it can be safely removed from Search and Insight Engine 2.0 onwards. The removal of `solr.content.dir` does not mean a loss of functionality because the Solr storage capabilities still retain a copy of the data originally sent for indexing.

#### `solr.host`

|Description|Specifies the host name that Alfresco uses to talk to Solr.|
|JNDI Property|`java:comp/env/solr/host`|
|Java System Property|`solr.host or solr.solr.host`|
|Environment Variable|`SOLR_SOLR_HOST`|
|Default Value|`localhost`|

#### `solr.port`

|Description|Specifies the port Solr will listen to.|
|JNDI Property|`java:comp/env/solr/port`|
|Java System Property|`solr.port or solr.solr.port`|
|Environment Variable|`SOLR_SOLR_PORT`|
|Default Value|`8983`|

#### `solr.baseUrl`

|Description|Specifies the base URL of the Solr server.|
|JNDI Property|`java:comp/env/solr/baseurl`|
|Java System Property|`solr.baseurl or solr.solr.baseurl`|
|Environment Variable|`SOLR_SOLR_BASEURL`|
|Default Value|`/solr`|

#### `solr.content.dir` (removed from Search and Insight Engine 2.0)

|Description|Specifies the location of the Solr content directory.|
|JNDI Property|`java:comp/env/solr/content/dir`|
|Java System Property|`solr.content.dir or solr.solr.content.dir`|
|Environment Variable|`SOLR_SOLR_CONTENT_DIR`|
|Default Value|`<SOLR6_INSTALL_LOCATION>/contentstore`|

#### `solr.model.dir`

|Description|Specifies the location of the Solr model directory.|
|JNDI Property|`java:comp/env/solr/model/dir`|
|Java System Property|`solr.model.dir or solr.solr.model.dir`|
|Environment Variable|`SOLR_SOLR_MODEL_DIR`|
|Default Value|`<SOLR6_INSTALL_LOCATION>/solrhome/alfrescoModel`|

### Configurable per core values

These properties can also be set in the `alfresco-insight-engine/solrhome/templates/rerank/conf/solrcore.properties` file.

#### `alfresco.host`

|Description|Specifies the externally resolvable host name of the Alfresco web application.|
|JNDI Property|`java:comp/env/alfresco/host`|
|Java System Property|`alfresco.host or solr.alfresco.host`|
|Environment Variable|`SOLR_ALFRESCO_HOST`|
|Default Value|`localhost`|

#### `alfresco.port`

|Description|Specifies the externally resolvable port number of the Alfresco web application.|
|JNDI Property|`java:comp/env/alfresco/port`|
|Java System Property|`alfresco.port or solr.alfresco.port`|
|Environment Variable|`SOLR_ALFRESCO_PORT`|
|Default Value|`8080`|

#### `alfresco.baseUrl`

|Description|Configures the base URL to Alfresco web project.|
|JNDI Property|`java:comp/env/alfresco/baseurl`|
|Java System Property|`alfresco.baseurl or solr.alfresco.baseurl`|
|Environment Variable|`SOLR_ALFRESCO_BASEURL`|
|Default Value|`/alfresco`|

#### `alfresco.port.ssl`

|Description|Specifies the HTTPS port for the Alfresco instance that Solr should track and index.|
|JNDI Property|`java:comp/env/alfresco/port/ssl`|
|Java System Property|`alfresco.port.ssl or solr.alfresco.port.ssl`|
|Environment Variable|`SOLR_ALFRESCO_PORT_SSL`|
|Default Value|`8443`|

#### `data.dir.root`

|Description|Specifies the top level directory path for the indexes managed by Solr.|
|JNDI Property|`java:comp/env/data/dir/root`|
|Java System Property|`data.dir.root or solr.data.dir.root`|
|Environment Variable|`SOLR_DATA_DIR_ROOT`|
|Default Value|`[solr_home]`|

These external values can be overridden by the JNDI attributes from `java:comp/env`, Java System properties, or OS environment variables.

Note that:

* JNDI properties are always lowercase
* Java System properties are always lowercase
* Environment variables are always uppercase
* Property names in the property files are case sensitive

### Additional external configuration when using SSL

You need to set these properties only if you are configuring Search and Insight Engine with SSL. These properties can also be set in the `solrcore.properties` file.

#### `alfresco.secureComms`

|Description|Instructs Solr if it should talk to Alfresco over HTTP or HTTPS. Set to none if a plain HTTP connection should be used.|
|JNDI Property|`java:comp/env/alfresco/securecomms`|
|Java System Property|`alfresco.securecommssolr.securecomms`|
|Environment Variable|`SOLR_ALFRESCO_SECURECOMMS`|
|Default Value|`none / https`|

#### `alfresco.encryption.ssl.keystore.passwordFileLocation`

|Description|Specifies the location of the file containing the password that is used to access the CLIENT keystore.|
|JNDI Property|`java:comp/env/alfresco/encryption/ssl/keystore/passwordfilelocation`|
|Java System Property|`alfresco.encryption.ssl.keystore.passwordfilelocationsolr.encryption.ssl.keystore.passwordfilelocation`|
|Environment Variable|`SOLR_ALFRESCO_ENCRYPTION_SSL_KEYSTORE_PASSWORDFILELOCATION`|

#### `alfresco.encryption.ssl.truststore.passwordFileLocation`

|Description|Specifies the location of the file containing the password that is used to access the CLIENT truststore.|
|JNDI Property|`java:comp/env/alfresco/encryption/ssl/truststore/passwordfilelocation`|
|Java System Property|`alfresco.encryption.ssl.truststore.passwordfilelocation`|
|Environment Variable|`SOLR_ALFRESCO_ENCRYPTION_SSL_TRUSTSTORE_PASSWORDFILELOCATION`|

#### `alfresco.encryption.ssl.keystore.location`

|Description|Specifies the CLIENT keystore location reference. If the keystore is file-based, the location can reference any path in the file system of the node where the keystore is located.|
|JNDI Property|`java:comp/env/alfresco/encryption/ssl/keystore/location`|
|Java System Property|`alfresco.encryption.ssl.keystore.location`|
|Environment Variable|`SOLR_ALFRESCO_ENCRYPTION_SSL_KEYSTORE_LOCATION`|

#### `alfresco.encryption.ssl.truststore.location`

|Description|Specifies the CLIENT truststore location reference. If the truststore is file-based, the location can reference any path in the file system of the node where the truststore is located.|
|JNDI Property|`java:comp/env/alfresco/encryption/ssl/truststore/location`|
|Java System Property|`alfresco.encryption.ssl.truststore.location`|
|Environment Variable|`SOLR_ALFRESCO_ENCRYPTION_SSL_TRUSTSTORE_LOCATION`|

#### `alfresco.encryption.ssl.truststore.provider`

|Description|Specifies the Java provider that implements the type attribute (for example, JCEKS type). The provider can be left unspecified and the first provider that implements the truststore type specified is used.|
|JNDI Property|`java:comp/env/alfresco/encryption/ssl/truststore/provider`|
|Java System Property|`alfresco.encryption.ssl.truststore.provider`|
|Environment Variable|`SOLR_ALFRESCO_ENCRYPTION_SSL_TRUSTSTORE_PROVIDER`|

#### `alfresco.encryption.ssl.keystore.type`

|Description|Specifies the CLIENT keystore type.|
|JNDI Property|`java:comp/env/alfresco/encryption/ssl/keystore/type`|
|Java System Property|`alfresco.encryption.ssl.keystore.type`|
|Environment Variable|`SOLR_ALFRESCO_ENCRYPTION_SSL_KEYSTORE_TYPE`|
|Default Value|`JCEKS`|

#### `alfresco.encryption.ssl.keystore.provider`

|Description|Specifies the Java provider that implements the type attribute (for example, JCEKS type). The provider can be left unspecified and the first provider that implements the keystore type specified is used.|
|JNDI Property|`java:comp/env/alfresco/encryption/ssl/keystore/provider`|
|Java System Property|`alfresco.encryption.ssl.keystore.provider`|
|Environment Variable|`SOLR_ALFRESCO_ENCRYPTION_SSL_KEYSTORE_PROVIDER`|

#### `alfresco.encryption.ssl.truststore.type`

|Description|Specifies the CLIENT truststore type.|
|JNDI Property|`java:comp/env/alfresco/encryption/ssl/truststore/type`|
|Java System Property|`alfresco.encryption.ssl.truststore.type`|
|Environment Variable|`SOLR_ALFRESCO_ENCRYPTION_SSL_TRUSTSTORE_TYPE`|
|Default Value|`JCEKS`|

## Solr configuration files

When you install Search and Insight Engine, several Solr configuration files are made available to you. The section lists the Solr configuration files, their location in the directory structure, and their description.

> **Note:** Some of these files are only available once Search and Insight Engine has been started for the first time.

|Configuration File|Location|Description|
|------------------|--------|-----------|
|schema.xml|`<SOLR_HOME>/solrhome/<core>/conf`. For example `<SOLR_HOME>/solrhome/alfresco/conf` or `<SOLR_HOME>/solrhome/archive/conf`|This file defines the schema for the index including field type definitions with associated analyzers. It contains details about the fields that you can include in your document and also describes how those fields can be used when adding documents to the index or when querying those fields. The properties of this file are managed by an expert user.|
|core.properties|`<SOLR_HOME>/solrhome/alfresco/core.properties` or `<SOLR_HOME>/solrhome/archive/core.properties`|This file specifies the cores to be used by Solr.|
|solrconfig.xml|`<SOLR_HOME>/solrhome/alfresco/conf` or `<SOLR_HOME>/solrhome/archive/conf`|This file specifies the parameters for configuring Solr. Also, the Solr search components are added to this file. The properties of this file are managed by an expert Administrator user.|
|solrcore.properties| `<SOLR_HOME>/solrhome/alfresco/conf` or `<SOLR_HOME>/solrhome/archive/conf`|This is the property configuration file for a core. Solr supports system property substitution, so properties that need substitution can be put in to this file. There is one `solrcore.properties` file in each core's configuration directory. For details, see [Solr core configuration properties]({% link insight-engine/latest/config/properties.md %}). The properties of this file are managed by an Administrator user.|
|context.xml|`<SOLR_HOME>`|This file specifies the Solr web application context template to use when installing Solr in separate tomcat server.|
|ssl.repo.client.keystore|`<SOLR_HOME>/solrhome/alfresco/conf` or `<SOLR_HOME>/solrhome/archive/conf`|This keystore contains the Solr public/private RSA key pair.|
|ssl.repo.client.truststore|`<SOLR_HOME>/solrhome/alfresco/conf` or `<SOLR_HOME>/solrhome/archive/conf`|This keystore contains the trusted Alfresco Certificate Authority certificate (which has been used to sign both the repository and Solr certificates)|

> **Note:** The `solrcore.properties` configuration file is the property configuration file for a Solr core. There is one `solrcore.properties` file in each core's configuration directory. See [Solr core configuration properties]({% link insight-engine/latest/config/properties.md %}) for more.

## Alfresco Index Engine

You can host a separate instance of Alfresco Content Services 6.2 or above with Solr 6 for high scalability and for maximizing the throughput of your Alfresco services. This setup is termed Alfresco Index Engine.

This setup shows a single repository database and content store. There are four nodes with Alfresco/Share and two nodes with Solr, all accessing the content simultaneously. This set up provides a higher level of availability, reliability, and scalability, thereby maximizing the throughput of various Alfresco services. Nodes in a cluster are positioned behind a load balancer that delegates requests to cluster members based on any one member’s ability/availability to handle the load.

Each Alfresco/Share instance is deployed into its own Tomcat servlet container. Alfresco services and CPU runtime footprint are optimized for high throughput under heavy concurrency with such a deployment. The load balancer fronts the cluster, and directs traffic to the member of the cluster most able to handle the current request.

> **Note:** All the servers in a cluster should have static IP addresses assigned to them.

![]({% link insight-engine/images/cluster-throughput.png %})

In this deployment scenario the following flows are present:

* Client flow:
  * Client sends the request to the main load balancer to reach Share application.
  * Main load balancer analyses the load and redirects the client to one of Share hosts.
  * Main load balancer uses the JSESSIONID cookie to stick the client to one of Share nodes.
  * Share sends the web scripts requests to the local repository instance, renders the page, and returns it to the user via the main load balancer.

* Alfresco internal flow:
  * Repositories intercommunication is done via Hazelcast to replicate caches.
  * Repositories share the same contentstore available via NFS/SAMBA share.
  * Repositories share the same database schema.

* Alfresco Solr flow:
  * Tracking tier: Two Solr instances periodically query repositories to detect new transactions, fetch new content, and build local indexes. Tracking is done through the Solr load balancer, which analyses the load and distributes it across the repositories.
  * Search tier: Four repository instances query two Solr instances on demand through the Solr load balancer.

To implement this setup, see [Install and configure Content Services nodes]({% link content-services/latest/admin/cluster.md %}#install-and-configure-content-services-nodes).
---
title: Indexing recommendations
---

When upgrading from a previous Insight Engine version you should review these indexing considerations:

* [Cross Locale](#cross-locale) Enabling or disabling
* [Exact term search](#exact-term-search)
* [Document fingerprints]({% link insight-engine/latest/config/performance.md %}#disable-document-fingerprint) Enabling or disabling

## Cross Locale

By default, Insight Engine is provided with cross-language search support disabled. This default configuration affects all the deployment artifacts, i.e. using a zip file or Docker image.

If you use several languages across your organization, you must enable cross-language search support in all text fields. To do this update the `alfresco-insight-engine/solrhome/conf/shared.properties` configuration file:

```bash
 alfresco.cross.locale.datatype.0={http://www.alfresco.org/model/dictionary/1.0}text
 alfresco.cross.locale.datatype.1={http://www.alfresco.org/model/dictionary/1.0}content
 alfresco.cross.locale.datatype.2={http://www.alfresco.org/model/dictionary/1.0}mltext
```

> **Note:** A reindex of Insight Engine is required after applying the configuration.

## Exact term search

To [Search]({% link content-services/latest/using/search.md %}) you must prefix it with `=`.

> **Note:** Exact term search will not work correctly unless the [Cross Locale](#cross-locale) configuration is enabled. There are some limitations if you deploy Insight Engine with Cross Locale configuration **disabled**.

* The Equals operator `=` must not be used in the user search boxes within the user interface i.e Share, ACS and Digital Workspace, because it will produce 0 results and the following error will show in the SOLR Logs:

```bash
java.lang.UnsupportedOperationException:
Exact Term search is not supported unless you configure the field
<{http://www.alfresco.org/model/content/1.0}title> for cross locale search
```

* Facet labels may be shown incorrectly in the user interface because they include the localization prefix in addition to the original value. For instance `{en}value` instead of `value`.

* Queries used in Alfresco Search REST API only accept the equals operator `=` for content model properties when the tokenization is set to `false`. **Note:** If the tokenization is set to `false` then the `=` operator will perform an *exact field* search, rather than an *exact term* search. The other tokenization options `true` and `both` will raise an exception when being used with the equals operator. Changing the tokenization option for a property requires re-indexing all those values in SOLR, this means you must design your custom content model carefully before deploying it to a production environment. For example:

```xml
<property name="cm:sample">
    <type>d:text</type>
    <index enabled="true">
        <tokenised>false</tokenised>
    </index>
</property>
```

The following features are working as expected in Insight Engine 2.0 and above deployments with Cross Locale configuration **enabled**:

* Equals operator can be used from the user interface search boxes and the results are as expected
* Facet labels are returned without the localization prefix, so they are shown consistently in the user interface
* Queries used in Alfresco Search REST API accept the equals operator `=` for properties with every tokenisation option: `false`, `true` and `both`.
---
title: Secure keys
---

This section describes a recommended approach for generating secure keys and setting up certificates. It is not required that you use this approach if you have an alternative solution that you already use.

If you're installing Alfresco Content Services using the distribution zip, you need to generate certificates for the repository and Solr. By default, the distribution zips are configured to use SSL, so you'll need to generate these certificates to get your system to run successfully.

You can create the keystores, truststores and certificates required to configure SSL/mutual TLS authentication between different services in Alfresco Content Services, such as the repository and Solr.

## Generate secure keys for SSL communication

Use this information to generate certificates for SSL/mutual TLS authentication between the repository and Search and Insight Engine, using secure keys specific to your installation.

A certificates generator script, `run.sh` (for Linux) and `run.cmd` (for Windows) is provided in a GitHub project. The script consists of two parts - the first part is based on OpenSSL (to generate the certificates), and the second part is based on the Java `keytool` (to build the keystores and truststores). Here, we'll focus on running the script for a standalone Linux or Windows operating system.

Before you start, you must already have OpenSSL and `keytool` available in your system path.

1. Browse to the [https://github.com/Alfresco/alfresco-ssl-generator](https://github.com/Alfresco/alfresco-ssl-generator) GitHub project and click **Clone** or **Download**.

    If you downloaded the project, extract the files to a suitable location.

2. Change directory to the following location and run the script:

    (For Linux)

    ```bash
    cd /ssl-tool
    ./run.sh
    ```

    (For Windows)

    ```bash
    cd ssl-tool-win
    run.cmd
    ```

    By default, this creates a `keystores` folder in your current working directory.

    > **Note:** If the `keystores` folder isn't empty, the script exits without producing any keystore or truststore. You can safely, remove the `keystores` folder if you need to re-run the script.

See [Keystore directory structure](#keystore-directory-structure) for more and [Customize certificate generation](#customizing-certificate-generation) for a full list of parameters that allow you to customize your certificates. It is recommended that you set your own passwords when generating certificates.

## Customize certificate generation

Here is a full list of parameters that allow you to customize your certificates. These parameters will override the default values listed in the `run.sh` and `run.cmd` scripts.

|Parameter|Value|Description|
|---------|-----|-----------|
|alfrescoversion|enterprise/community|Sets the type of Alfresco environment. The default value is enterprise.|
|keysize|1024/2048/4096 |Specifies the RSA key length. The default value is 1024.|
|keystoretype|PKCS12/JKS/JCEKS|Sets the type of the keystores (containing private keys). The default value is JCEKS.|
|keystorepass|Any string|Specifies the password for the keystores|
|truststoretype|JKS/JCEKS|Sets the type of the truststores (containing public keys). The default value is JCEKS.|
|truststorepass|Any string|Specifies the password for the truststores|
|encstorepass|Any string|Specifies the password for the encryption keystore|
|encmetadatapass|Any string|Specifies the password for the encryption metadata|
|cacertdname| |Sets the Distinguished Name of the CA certificate, starting with a forward-slash. For example:`/C=GB/ST=UK/L=Maidenhead/O=Alfresco Software Ltd./OU=Unknown/CN=Custom Alfresco CA`|
|repocertdname| |Sets the Distinguished Name of the repository certificate, starting with a forward-slash. For example:`/C=GB/ST=UK/L=Maidenhead/O=Alfresco Software Ltd./OU=Unknown/CN=Custom Alfresco Repository`|
|solrcertdname| |Sets the Distinguished Name of the Solr certificate, starting with a forward-slash. For example:`/C=GB/ST=UK/L=Maidenhead/O=Alfresco Software Ltd./OU=Unknown/CN=Custom Alfresco Repository Client`|
|browsercertdname| |Sets the Distinguished Name of the browser certificate, starting with a forward-slash. For example:`/C=GB/ST=UK/L=Maidenhead/O=Alfresco Software Ltd./OU=Unknown/CN=Custom Browser Client`|
|caservername|Any string, localhost by default.|DNS Name of CA Server.|
|alfrescoservername|Any string, localhost by default.|DNS Name for Alfresco Server.|
|solrservername|Any string, localhost by default.|DNS Name For Solr Server.|
|alfrescoformat|classic, current|Default format for certificates: current for IE SS 2.0.0+ and classic for previous versions.|

> **Note:** If you plan to use custom DNames in your certificates, you must use double quotes around the values. For example:

```bash
$ ./run.sh -cacertdname  
"/C=GB/ST=UK/L=Maidenhead/O=Alfresco/OU=Unknown/CN=Windows Alfresco CA"
-repocertdname "/C=GB/ST=UK/L=Maidenhead/O=Alfresco/OU=Unknown/CN=Repo"
-solrcertdname "/C=GB/ST=UK/L=Maidenhead/O=Alfresco/OU=Unknown/CN=Solr"
```

It is recommended that you set your own passwords when generating certificates. For example:

(For Linux)

```bash
./run.sh -keystorepass “password" -truststorepass “password"
```

(For Windows)

```bash
run.cmd -keystorepass “password" -truststorepass “password"
```

## Keystore directory structure

The `keystores` directory contains the following structure and files:

```bash
keystores
├── alfresco
│   ├── keystore
│   ├── ssl.keystore
│   ├── ssl.truststore
├── client
│   └── browser.p12
└── solr
│   ├── ssl-repo-client.keystore
│   └── ssl-repo-client.truststore
└── zeppelin
    ├── ssl-repo-client.keystore
    └── ssl-repo-client.truststore
```

> **Note:** The `zeppelin` folder is only required if you're an Enterprise customer using Search and Insight Engine.

|File name|Description|
|---------|-----------|
|browser.p12|The PKCS12 keystore generated from `ssl.keystore` that contains the repository private key and certificate for use in browsers, such as Firefox.|
|keystore|Secret key keystore containing the secret key used to encrypt and decrypt node properties.|
|ssl.keystore|Repository keystore containing the repository private/public key pair and certificate.|
|ssl.truststore|Repository truststore containing certificates that the repository trusts.|
|ssl-repo-client.keystore|Solr SSL keystore containing the Solr private/public key pair and certificate.|
|ssl-repo-client.truststore|Solr truststore containing certificates that the repository trusts.|

## Set up certificates

Use this information to set up your generated certificates in their correct locations.

Before continuing, make sure that you've already completed the steps in [Generating secure keys for SSL communication](#generating-secure-keys-for-ssl-communication).

1. Copy the files under `/keystores/alfresco` to the Alfresco Content Services install location:

    ```bash
    ${ALF_DATA_DIR}/keystore
    ```

2. Copy the files under `/keystores/solr` to the Alfresco Search Services install location:

    ```bash
    <SOLR_HOME>/keystore
    ```

3. You can use the file under `keystores/client` from a browser to access the server using HTTPS on port 8443.

4. Override the SSL properties as shown.

    1. In `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` update the following:

        ```bash
        dir.keystore=${ALF_DATA_DIR}/keystore
        # encryption
        solr.secureComms=https
        # ssl encryption
        encryption.ssl.keystore.location=${dir.keystore}/ssl.keystore
        encryption.ssl.keystore.type=JCEKS
        encryption.ssl.keystore.keyMetaData.location=
        encryption.ssl.truststore.location=${dir.keystore}/ssl.truststore
        encryption.ssl.truststore.type=JCEKS
        encryption.ssl.truststore.keyMetaData.location=
        # secret key keystore configuration
        encryption.keystore.location=${dir.keystore}/keystore
        encryption.keystore.keyMetaData.location=
        encryption.keystore.type=JCEKS
        solr.host=localhost
        solr.port=8983
        solr.port.ssl=8983
        ```

        > **Note:** If you're using a different keystore or truststore type other than the default, `JCEKS`, you must change the value in the properties file.

    2. For the Tomcat SSL Connector in `<TOMCAT_HOME>/conf/server.xml` update the following:

        ```bash
        <Connector port="8443" protocol="HTTP\1.1"
            SSLEnabled="true" maxThreads="150" scheme="https"
            keystoreFile="/usr/local/tomcat/alf_data/keystore/ssl.keystore"
            keystorePass="password" keystoreType="JCEKS"
            secure="true" connectionTimeout="240000"
            truststoreFile="/usr/local/tomcat/alf_data/keystore/ssl.truststore"
            truststorePass="password" truststoreType="JCEKS"
            clientAuth="want" sslProtocol="TLS" />
        ```

        > **Note:** If you're using a different keystore or truststore type other than the default, `JCEKS`, you must change the value in the properties file. Also, make sure that the keystore and truststore file locations are correct for your environment.

    See [Installing the Tomcat application server]({% link content-services/latest/install/zip/tomcat.md %}) and [Solr configuration files]({% link insight-engine/latest/config/index.md %}#solr-configuration-files) for more.

5. Change the SSL properties in `<SOLR_HOME>/solrhome/templates/rerank/conf/solrcore.properties`.

    The `rerank` template is used to generate the `alfresco` and `archive` Solr cores when you first run Alfresco Search Services.

    ```bash
    # encryption
    alfresco.secureComms=https
    # ssl
    alfresco.encryption.ssl.keystore.type=JCEKS
    alfresco.encryption.ssl.keystore.location=<SOLR_HOME>/ssl-repo-client.keystore
    alfresco.encryption.ssl.keystore.passwordFileLocation=
    alfresco.encryption.ssl.truststore.type=JCEKS
    alfresco.encryption.ssl.truststore.location=<SOLR_HOME>/ssl-repo-client.truststore
    alfresco.encryption.ssl.truststore.passwordFileLocation=alfresco.host=localhost
    alfresco.port.ssl=8443
    ```

    > **Note:** If you're using a different keystore or truststore type other than the default, `JCEKS`, you must change the value in the properties file.

    If the `alfresco` and `archive` cores already exist, ensure that `alfresco.secureComms` is set to `https` for both the cores in the following files:

    ```bash
    <SOLR_HOME>/solrhome/alfresco/conf/solrcore.properties
    <SOLR_HOME>/solrhome/archive/conf/solrcore.properties
    ```

    See [Solr core configuration properties]({% link insight-engine/latest/config/properties.md %}) for more.
---
title: Configure OpenSearch
---

You can configure OpenSearch to use a search engine proxy.

[OpenSearch](https://github.com/dewitt/opensearch){:target="_blank"} is a collection of simple formats for sharing search string results, in order to extend existing schemas such as ATOM or RSS. The list of registered search engines is in /config/alfresco/web-scripts-config.xml. You can configure a search engine proxy so that the OpenSearch client indirectly submits a search request through the Alfresco Content Services Web Server (the proxy), rather than directly to the search engine.

1. Create a new file called /config/alfresco/extension/web-scripts-config-custom.xml.

    This file will contain the search engine proxy information.

2. Create a new search engine proxy, using the `proxy` attribute. For example:

    ```xml
    <engine label="Alfresco Open Source Talk" proxy="opentalk">
        <url type="application/rss+xml">http://blogs.alfresco.com/opentalk/
      os-query?s={searchTerms}&itemstart={startIndex?}&itempage={startPage?}
      &itemlimit={count?}</url>
    </engine>
    ```

   > **Note:** The value of the `proxy` attribute must be a unique name that identifies the search engine.

3. Save `/config/alfresco/extension/web-scripts-config-custom.xml`.
---
title: Performance Recommendations
---

From version 2.0.2, the custom `<SOLR6_INSTALL_LOCATION>/contentstore` folder has been removed. Metadata, Permissions, and Content for the Alfresco Repository nodes are fully stored in the SOLR Core standard indexes.

Since the total amount of storage could be equivalent between previous versions, the SOLR Core Index storage has been increased. In order to control the size and the performance of the SOLR index, the following actions may be performed:

* [Disable document FINGERPRINT](#disable-document-fingerprint) reduces storage requirements
* [Disable SOLR Document Cache](#disable-solr-document-cache) reduces RAM requirements
* [Optimize SOLR Index](#optimize-solr-index) improves search performance

Additionally, from version 2.0.2, SOLR Merging parameters have been exposed that can be configured within the `solrcore.properties` file. The default values function adequately for many use cases, however some recommendations are given to increase performance in large deployments.

## Disable document FINGERPRINT

From version 2.0.2 the document Fingerprint feature is disabled by default and appears in the `solrcore.properties` file as `alfresco.fingerprint=false`.

> **Note:** This configuration will generate smaller Lucene indexes when indexing and may help to reduce storage and to increase performance.

When applying this flag to an existing SOLR Core a full reindex is recommended. Since no more `MINHASH` properties will be calculated from the moment the property is set to `false`, existing Solr Documents won't be re-calculated in order to remove this additional information until a reindex is executed on the Solr Core.

The [Document Fingerprints]({% link insight-engine/latest/admin/index.md %}#document-fingerprints) feature can be used to get similar documents from SOLR using the reserved word `FINGERPRINT` in `FTS` search syntax. In order to provide these results, each document in the SOLR Index includes a list of `MINHASH` fields that create larger Lucene Indexes.

## Disable SOLR Document Cache

SOLR uses several [Caches](https://solr.apache.org/guide/6_6/query-settings-in-solrconfig.html#QuerySettingsinSolrConfig-Caches) in order to retain some result information in memory. Since version 2.0 this feature can be disabled in order to decrease the use of RAM memory.

From version 2.0.2, the SOLR Document Caches feature is disabled by default, including the following properties in the `solrcore.properties` file.

```bash
solr.documentCache.size=0
solr.documentCache.initialSize=0
solr.documentCache.autowarmCount=0
```

> **Note:** This configuration will require a smaller amount of RAM memory when searching which may help to reduce requirements and to increase performance.

When applying these flags to an existing SOLR Core, **no** re-indexing operation is recommended. Once the properties have been set in the `solrcore.properties` file, all the performance benefits will be available immediately.

## Optimize SOLR Index

During indexing, whenever a document is deleted or updated, the document is *marked as deleted* in its original segment. This generates some percentage of *waste* storage because the index will contain around 15% to 20% of deleted documents. Merging the Lucene Segment process will control this ratio with time, in order to maintain it as low as possible.
However, in some situations, especially after a bulk ingestion, the percentage of deleted documents can be up to 50%. This percentage is determined by the ratio of `numDocs` to `maxDocs`, which is shown in the Solr Admin interface.

> **Note:** The greater the ratio of deleted documents the Solr Index contains, the slower Search and Insight Engine will be at searching and indexing.

> **Note:** The *optimizing action* has been available by default since Search and Insight Engine 1.0.

Since optimizing the index is not a recommended operation in many use cases, this option will remove the deleted documents from your index. However, it will create segments which are much larger than the maximum considered for future merges. If you are optimizing your index periodically and can afford the time to optimize every time you rebuild your index, then optimizing is reasonable and it will increase the searching performance.

> **Note:** Ensure after the initial optimization, that a periodic execution of the optimization process is carried out in order to preserve the performance benefits.

This operation can be performed using the SOLR REST API (available at `http://127.0.0.1:8983/solr/alfresco/update?optimize=true` by default) or by clicking the `Optimize now` button in the **Core > Overview** section of the Solr Admin interface.

You can optimize the index by reducing it to `N` segments with `N` >= 1.

```text
http://127.0.0.1:8983/solr/alfresco/update?optimize=true&maxSegments=N
```

This can be useful for reducing the impact of the force merge operation. The advantages of using `N` >= 1 are:

* The force merge execution takes less resources.
* Avoids the production of a single large segment.

The value of `N` must be chosen carefully. `N` should be smaller than the current number of segments. Moreover, it is possible that some segments are not selected for merging. Consequentially, not all the deleted documents may be removed from the index.

## Merging parameters

From version 2.0.2, the following parameters have been exposed to be used from `solrcore.properties` file.

| Property | Description |
| -------- | ----------- |
| merge.policy.maxMergedSegmentMB | This number should be increased for large deployments. For instance, when using 40+ million indexed nodes with content on a SOLR Shard. You may use `10240` instead of `5120`. The default is `5120`. |
| merge.policy.maxMergeAtOnce | The numbers should be decreased in order to reduce the number of segments. This also improves searching performance when using 40+ million indexed nodes with content on a SOLR Shard. You may use `5` instead of `10`. The default value is `10`. **Note:** The value used must be the same as for `merge.policy.segmentsPerTier`. |
| merge.policy.segmentsPerTier | The numbers should be decreased in order to reduce the number of segments. This also improves searching performance when using 40+ million indexed nodes with content on a SOLR Shard. You may use `5` instead of `10`. The default value is `10`. **Note:** The value used must be the same as for `merge.policy.maxMergeAtOnce`. |
| merger.maxMergeCount | Increment this number for large deployments, so more merge operations can be executed simultaneously. The default value is `6`. |
| merger.maxThreadCount | This number should always be lower than the amount of dedicated CPUs and also lower than `mergermaxMergeCount`. Increment this number for large deployments in order to use all your available CPU threads. The default value is `3`. |

> **Note:** Changing any of these values requires a full re-index of your SOLR Core in order to get the performance benefits.
---
title: Properties
---

This page lists the configuration properties for a Solr core and the Solr index's full text search.

## Solr core configuration properties

The `solrcore.properties` configuration file is the property configuration file for a Solr core. There's one `solrcore.properties` file in each core's configuration directory. Use this information to understand the properties of this file, their description, and the default value.

|Property|Description|
|-------------|-----------|
|alfresco.aclBatchSize|This property is used for batch fetching updates during tracking, for example `10`.|
|alfresco.acl.tracker.maxParallelism|Defines the number of threads that are used when indexing documents using the ACL Tracker, for example `32`.|
|alfresco.baseUrl|This property configures the base URL to Alfresco Content Services web project, for example `/alfresco`. If you need to change the `baseUrl` value, see [Deploy with a different context path]{% link content-services/latest/config/repository.md %}#deploy-with-a-different-context-path).|
|alfresco.batch.count|This property indicates the number of updates that should be made to this core before a commit is executed, for example  `1000`.|
|alfresco.cascade.tracker.enabled|Index fields required for path-based queries. Disabling support for path queries (i.e. setting this to false) can speed up indexing in sharded systems, for example `true`.  NOTE: Updating this property will result in path-based fields not being populated. Consequently it should not be changed after the initial startup of the server.|
|alfresco.cascade.tracker.maxParallelism|Defines the number of threads that are used when indexing documents using the Cascade Tracker, for example `32`.|
|alfresco.changeSetAclsBatchSize|This property is used for batch fetching updates during tracking, for example `100`.|
|alfresco.content.tracker.maxParallelism|Defines the number of threads that are used when indexing documents using the Content Tracker, for example `32`.|
|alfresco.corePoolSize|This property specifies the pool size for multi-threaded tracking. It is used for indexing nodes, for example `3`.|
|alfresco.cron|This property specifies the cron expression that instructs Solr how often to track Alfresco Content Services and index new or updated content. The default value indicates that Solr tracks every 15 seconds i.e. `0/15 * * * * ? *`.|
|alfresco.doPermissionChecks|This property allows users to see the document name or properties on a search result, for example `true`.|
|alfresco.encryption.ssl.keystore.location|This property specifies the CLIENT keystore location reference. If the keystore is file-based, the location can reference any path in the file system of the node where the keystore is located, for example `ssl.repo.client.keystore`.|
|alfresco.encryption.ssl.keystore. passwordFileLocation|This property specifies the location of the file containing the password that is used to access the CLIENT keystore, also the default that is used to store keys within the keystore, for example `ssl-keystore-passwords.properties`.|
|alfresco.encryption.ssl.keystore.provider|This property specifies the Java provider that implements the `type` attribute (for example, JCEKS type). The provider can be left unspecified and the first provider that implements the keystore type specified is used.|
|alfresco.encryption.ssl.keystore.type|This property specifies the CLIENT keystore type, for example `JCEKS`.|
|alfresco.encryption.ssl.truststore.location|This property specifies the CLIENT truststore location reference. If the truststore is file-based, the location can reference any path in the file system of the node where the truststore is located, for example `ssl.repo.client.truststore`.|
|alfresco.encryption.ssl.truststore. passwordFileLocation|This property specifies the location of the file containing the password that is used to access the CLIENT truststore, also the default that is used to store keys within the truststore, for example `ssl-truststore-passwords.properties`.|
|alfresco.encryption.ssl.truststore.provider|This property specifies the Java provider that implements the `type` attribute (for example, JCEKS type). The provider can be left unspecified and the first provider that implements the truststore type specified is used.|
|alfresco.encryption.ssl.truststore.type|This property specifies the CLIENT truststore type, for example `JCEKS`.|
|alfresco.hole.retention|Each track will revisit all transactions from the timestamp of the last in the index, less this value, to fill in any transactions that might have been missed, for example `3600000`.|
|alfresco.host|This property specifies the host name for the instance that Solr should track and index, for example `localhost`.|
|alfresco.nodestate.tracker.cron|This property controls the frequency of registration of a Search Services shard to Alfresco Content Services, for example `0/10 * * * * ? *)`. **Note:** The value you set for `alfresco.nodestate.tracker.cron` should be lower than the value you set for `search.solrShardRegistry.shardInstanceTimeoutInSecond`, which is set in the `alfresco-global.properties` file.|
|alfresco.index.transformContent|If this property is set to false, the index tracker will not transform any content and only the metadata will be indexed, for example `false`.|
|alfresco.keepAliveTime|This property specifies the time (in seconds) to keep non-core idle threads in the pool, for example `120`.|
|alfresco.lag|When Solr tracking starts, it aims to get up to date to the current time (in seconds), less this lag, for example `1000`.|
|alfresco.maxHostConnections|This property is used for HTTP client configuration, for example `40`.|
|alfresco.maximumPoolSize|This property specifies the maximum pool size for multi-threaded tracking, for example `-1`.|
|alfresco.maxTotalConnections|This property is used for HTTP client configuration, for example `40`.|
|alfresco.metadata.ignore.datatype.0|This property configures the metadata pulling control, for example `cm:person`.|
|alfresco.metadata.ignore.datatype.1|This property configures the metadata pulling control, for example `app:configurations`.|
|alfresco.metadata.skipDescendantDocsForSpecificTypes|This property reduces the overhead caused by reindexing sites, for example `false`.|
|alfresco.metadata.tracker.maxParallelism|Defines the number of threads used when indexing documents using the Metadata Tracker, for example `32`.|
|alfresco.port|This property specifies the HTTP port for the instance that Solr should track and index, for example `8080`.|
|alfresco.port.ssl|This property specifies the HTTPS port for the instance that Solr should track and index, for example `8443`.|
|alfresco.secureComms|This property enables Shared Secret authentication or mTLS authentication with HTTPS. Set to `secret` if a Shared Secret HTTP header should be used for authentication, for example `https`.|
|alfresco.socketTimeout|This property specifies the amount of time Solr tracker will take to notice if the Alfresco Content Services web app shuts down first, if Alfresco Content Services and Solr are running on the same web application, for example `60000`.|
|alfresco.stores|This property specifies the repository store that this core should index, for example `workspace://SpacesStore`.|
|alfresco.threadDaemon|This property sets whether the threads run as daemon threads or not. If set to `false`, shut down is blocked else it is left unblocked, for example `true`.|
|alfresco.threadPriority|This property specifies the priority that all threads must have on the scale of 1 to 10, where 1 has the lowest priority and 10 has the highest priority, for example `5`.|
|alfresco.topTermSpanRewriteLimit|Term expansion is used to convert wildcard \* matches into a finite disjunction - e.g. "cat*" -> "cat OR category OR catalogue OR ... caterpillar". This property controls the number of terms in this disjunction, which are chosen from the index with preference given to more popular terms. If you increase the value too much you may not have good performance and if you decrease the value too much you may not receive any results. How you are affected by variations in the limit will depend on your installation, for example `1000`.|
|alfresco.transactionDocsBatchSize|This property is used for batch fetching updates during tracking, for example `100`.|
|alfresco.version|This property specifies the Alfresco Content Services version installed, for example `6.2`.|
|alfresco.workQueueSize|This property specifies the maximum number of queued work instances to keep before blocking against further adds, for example `-1`.|
|data.dir.root|This property specifies the top level directory path for the indexes managed by Solr, for example `/alfresco-insight-engine/solrhome`|
|data.dir.store|This property specifies the directory relative to data.dir.root where the data for this core is stored, for example `workspace/SpacesStore`|
|enable.alfresco.tracking|This property instructs Solr if it should index Alfresco Content Services content in the associated repository store or not, for example `true`.|
|max.field.length|This property specifies the maximum number of tokens to include for each field. By default, all tokens are added, for example `2147483647`.|
|maxScheduledTransactions|This optional parameter controls the maximum transactions to schedule for reindexing in the admin fix tool. If the admin fix action specifies a value for `maxScheduledTransactions` then the request parameter that is used in the solrcore.properties configuration file is ignored.|
|solr.authorityCache.autowarmCount|This property configures the Solr result cache, for example `0`.|
|solr.authorityCache.initialSize|This property configures the caches used in authority filter generation, for example `64`.|
|solr.authorityCache.size|This property configures the caches used in authority filter generation, for example `64`.|
|solr.deniedCache.autowarmCount|This property configures the Solr result cache, for example `0`.|
|solr.deniedCache.initialSize|This property configures the Solr result cache, for example `1024`.|
|solr.deniedCache.size|This property configures the Solr result cache, for example `4096`.|
|solr.documentCache.autowarmCount|This property configures the number of document objects to pre-populate from the old cache, for example `0`.|
|solr.documentCache.initialSize|This property configures the Solr document cache, for example `64`.|
|solr.documentCache.size|This property configures the Solr document cache, for example `64`.|
|solr.filterCache.autowarmCount|This property configures the number of entries to pre-populate from the old cache, for example `128`.|
|solr.filterCache.initialSize|This property specifies the initial capacity (number of entries) of the Solr filter cache. You may want to increase the value if you have many users, groups, and tenants, for example `64`.|
|solr.filterCache.size|This property specifies the maximum number of entries in the Solr filter cache. You may want to increase the value if you have many users, groups, and tenants, for example `64`.|
|solr.initial.transaction.range|When checking the consistency of the repository and index, the first transaction is compared in both the repository and index repositories. In order to receive that initial transaction from the database a range of between 0-2000 for transaction id should be used. This parameter can be used when the initial transaction id is greater than 2000, for example `0-2000`.|
|solr.maxBooleanClauses|This property specifies the number of Boolean clauses in a query. It can affect range or wildcard queries that expand to big Boolean queries, for example `10000`.|
|solr.nodeBatchSize|This property configures the batch fetch, for example `10`.|
|solr.ownerCache.autowarmCount|This property configures the Solr result cache, for example `0`.|
|solr.ownerCache.initialSize|This property configures the Solr result cache, for example `1024`.|
|solr.ownerCache.size|This property configures the Solr result cache, for example `4096`.|
|solr.pathCache.autowarmCount|This property configures the Solr result cache, for example `128`.|
|solr.pathCache.initialSize|This property configures the cache used for `PATH` query parts, for example `64`.|
|solr.pathCache.size|This property configures the cache used for `PATH` query parts, for example `64`.|
|solr.queryResultCache.autowarmCount|This property configures the number of search results to pre-populate from the old cache, for example `0`.|
|solr.queryResultCache.initialSize|Increase the value of this property to cache more query results, for example `1024`.|
|solr.queryResultCache.size|This property configures the number of query results. Increase the value to cache more query results, for example `1024`.|
|solr.queryResultMaxDocsCached|Set this property to a higher value if you expect to page through most results, for example `2000`.|
|solr.queryResultWindowSize|This property rounds-up a request number to the nearest multiple of the setting, thereby storing a range or window of documents to be quickly available, for example `200`.|
|solr.readerCache.autowarmCount|This property configures the Solr result cache, for example `0`.|
|solr.readerCache.initialSize|This property configures the Solr result cache, for example `1024`.|
|solr.readerCache.size|This property configures the Solr result cache, for example `4096`.|
|solr.request.content.compress|This property when set to `true` will compress the content that is sent back from the repository during system communication, for example `false`.|

## Full text search configuration properties

The Solr index's full text search properties influence the behavior of Solr indexes.

The main index and deltas all use the same configuration. The data dictionary settings for properties determine how individual properties are indexed.

If you wish to change the default value of a property, add the relevant property to the `TOMCAT_HOME>/shared/classes/alfresco-global.properties` file and then make the changes.

### Solr index properties

| Property | Description |
| -------- | ----------- |
| solr.host=localhost | The host name where the Solr instance is located |
| solr.port=8080 | The port number on which the Solr instance is running |
| solr.port.ssl=8443 | The port number on which the Solr SSL support is running. |
| solr.solrUser=solr | The Solr user name |
| solr.solrPassword=solr | The Solr password |
| solr.secureComms=https | The HTTPS connection |
| solr.solrConnectTimeout=5000 | The Solr connection timeouts in ms |
| solr.solrPingCronExpression=0 0/5 * * * ? * | The cron expression defining how often the Solr Admin client (used by JMX) pings Solr if it goes away |

### Data dictionary options

The indexing behavior for each property can be set in the content model. By default the index is eventually consistent with the created content and properties are tokenized when indexed. For more information on how to configure indexing for properties in the content model, view the [Content Services documentation]({% link content-services/latest/develop/repo-ext-points/content-model.md %}).

### Indexing options

If you want archive or zip files to be unzipped and the files included in the index, set the following property:

```bash
transformer.Archive.includeContents=true
```

The default setting is false.
---
title: Solr replication
---

Solr replication uses the master-slave model to distribute complete copies of a master index to one or more slave servers.

The master server receives all updates and all changes are made against a single master server. Changes made on the master are distributed to all the slave servers which service all query requests from the clients. This enables Solr to remain responsive even with high query traffic.

All trackers must be enabled on master nodes, while only model tracker and metadata tracker should be enabled on slaves.

The figure below shows a Solr configuration using index replication. The master server's index is replicated on the slaves.

![]({% link insight-engine/images/solr-replication.png %})

The master-slave replication requires non-SSL communication between the master server and the slave server.

## Advantages and disadvantages of a master-slave index replication

### Advantages

* Splits read and write load and operations
* Load distribution for search queries
* High availability for searching
* Any number of slave instances can be created to scale query performance
* Usually less frequent index updates on the slaves and better use of the cache

### Disadvantages

* Increased latency (sum of tracking and Solr replication latency)
* Occasional large IO load to replicate large merges
* Complicated load balance and management
* Reconfiguration if the master is lost

### Difference between the master-master and master-slave replication

|Master-master replication|Master-slave replication|
|-------------------------|------------------------|
|Requires all Solr nodes to do the leg-work of indexing.|Only the master server indexes or re-indexes. The slave servers only pull the completed indexes.|
|It is simple to set up. Each Solr node may have the same setup if the queries from Solr to the repository go through a load balancer instead of to a specific repository node.|It is not as simple as the master-master replication.|
|Achieves eventual consistency much more quickly than the master-slave replication.|Solr indexing is eventually consistent irrespective of the method used. It takes slightly longer in a master-slave replication because first the master index is updated and then that index change is replicated to the slave.|
|In a master-master replication, the master nodes can't be configured to perform differently in different situations.|In the master-slave replication, the master and slave nodes can be configured to perform better under different situations. For example, the master node can be configured for optimal indexing performance, while the slave node can be configured for optimal search performance.|
|Neither the master-master replication nor the master-slave replication includes any inbuilt functionality to switch Solr targets, in case one node fails.|Neither the master-master replication nor the master-slave replication includes any inbuilt functionality to switch Solr targets, in case one node fails.|
|If a master node went down, the load balancer will direct all the query requests to a Solr node that was still running.|If a slave node went down, the same load-balancer behaviour would be relied on. But if the master node went down, then intervention would be required to Designate a new master, then point the slaves to that new master, and then Point the new master to the repository|
| |Requires an additional master node, so has slightly higher pre-requisites.|

## Solr replication configuration

The Solr replication feature is implemented as a `RequestHandler`. The simplest configuration involves one Alfresco Content Services node, one Solr master, and one Solr slave.

The Solr master is configured to track the Alfresco Content Services instance while the Solr slave is configured to track the Solr master. The Alfresco Content Services instance is configured to send all the queries to the SOLR slave.

![]({% link insight-engine/images/solr-replication-conf.png %})

## Configuring the Alfresco Content Services instance

As usual, no SSL queries configured go to the slave.

### Configuring Solr master

The configuration affecting replication is controlled by a single file, `alfresco-insight-engine/solrhome/templates/re-rank/conf/solrconfig.xml`. To configure the master server, follow the steps below:

1. Edit the `alfresco-insight-engine/solrhome/templates/re-rank/conf/solrconfig.xml` file on the master server to change the default replication handler configuration. Remember to uncomment the `master` section.

    ```bash
    <requestHandler name="/replication" class="solr.ReplicationHandler" > 
        <!--
           To enable simple master/slave replication, uncomment one of the 
           sections below, depending on whether this solr instance should be
           the "master" or a "slave".  If this instance is a "slave" you will 
           also need to fill in the masterUrl to point to a real machine.
        -->
           <lst name="master">
             <str name="replicateAfter">commit</str>
             <str name="replicateAfter">startup</str>
             <str name="confFiles">schema.xml,stopwords.txt</str>
           </lst>

        <!--
           <lst name="slave">
             <str name="masterUrl">http://your-master-hostname:8983/solr</str>
             <str name="pollInterval">00:00:60</str>
           </lst>
        -->
    </requestHandler>
    ```

    where:

    |Parameter|Description|
    |--------------|-----------|
    |replicateAfter|String specifying action after which replication should occur. Valid values are, `commit`which triggers replication whenever a commit is performed on the master index,`optimize` which triggers replication whenever the master index is optimized and `startup` which triggers replication whenever the master index starts up. There can be multiple values for this parameter. If you use `startup`, you need to have a `commit` and/or `optimize` entry also if you want to trigger replication on future commits or optimizes.|
    |confFiles|Comma-separated list of configuration files to replicate.|

2. Make sure that the solrcore.properties file has the following settings:

    ```bash
    enable.master=true
    enable.slave=false
    ```

### Configuring Solr slave

Here again, the solrconfig.xml file controls the configuration affecting replication. To configure the slave server, follow the steps below:

1. Uncomment the `slave` section.

    ```bash
    <requestHandler name="/replication" class="solr.ReplicationHandler" > 
        <!--
           To enable simple master/slave replication, uncomment one of the 
           sections below, depending on whether this solr instance should be
           the "master" or a "slave".  If this instance is a "slave" you will 
           also need to fill in the masterUrl to point to a real machine.
        -->
       <!--
       <lst name="master">
             <str name="replicateAfter">commit</str>
             <str name="replicateAfter">startup</str>
             <str name="confFiles">schema.xml,stopwords.txt</str>
           </lst>
       -->
           <lst name="slave">
             <str name="masterUrl">http://your-master-hostname:8983/solr</str>
             <str name="pollInterval">00:00:60</str>
           </lst>
    </requestHandler>
    ```

    where:

    |Parameter name|Description|
    |--------------|-----------|
    |pollInterval|Interval in which the slave should poll master .Format is *hh:mm:ss*. If this is missing, the slave server does not poll automatically.|
    |masterUrl|Fully qualified URL for the replication handler of master. Make sure the `masterUrl` ends with `<tomcat base url>/solr/alfresco`.|

2. Set the master URL to point to the Solr master. Also, set how often the slave server should poll for changes.

    ```bash
    <str name="masterUrl">http://your-master-hostname:8983/solr/alfresco</str>
    <str name="pollInterval">00:00:60</str>
    ```

3. Set the following properties in the solrcore.properties file:

    ```bash
    enable.master=false
    enable.slave=true
    ```

In this configuration, the Solr instance will only track model changes from the Alfresco Content Services platform.

## Additional Solr configuration

Any configuration changes related to the core schema and configuration, or any changes in `<solr_home>/conf` must be made to all Solr instances. Replication can be configured to manage the distribution of other core related configuration files.

## Solr master-slave reconfiguration

There are additional master-slave configuration requirements for Solr, such as adding a slave server and promoting a slave server.

## Adding a slave server

To add another slave server to an existing replication configuration, see [Configuring Solr slave](#configuring-solr-slave).

## Promoting a slave

In the event of a downed master in a master-slave configuration, the slave servers can continue to service queries, but will no longer be able to index until a new master is instated. The process of promoting a slave to a master is manual. The state of slave servers may differ, so choose the most up-to-date slave to promote as the master server.

To promote a slave, follow the steps below:

1. Nominate the most up-to-date slave as the master.

    To choose the most up-to-date slave, follow the steps below:

    1. Go to Solr Admin web interface using:

        ```http
        https://localhost:8443/solr
        ```

    2. Select the appropriate core from the **Core Selector** list.
    3. Select **Replication**.

        The Replication screen shows the current replication status for the core, and lets you enable/disable replication. It also displays the version of the master and slave servers.

    4. Identify the slave whose index is closest to the master server or pick a slave that has the highest version.
    ![]({% link insight-engine/images/slave-version.png %})

2. Stop the Solr server on the new master.
3. In the alfresco-insight-engine/solrhome/templates/re-rank/conf/solrconfig.xml file, replace the Solr configuration in the replication handler that defines the slave with the one that defines the master.

    ```bash
    <requestHandler name="/replication" class="org.alfresco.solr.handler.AlfrescoReplicationHandler"> 
        <!--
           To enable simple master/slave replication, uncomment one of the 
           sections below, depending on whether this solr instance should be
           the "master" or a "slave".  If this instance is a "slave" you will 
           also need to fill in the masterUrl to point to a real machine.
        -->
           <lst name="master">
             <str name="replicateAfter">commit</str>
             <str name="replicateAfter">startup</str>
             <str name="confFiles">schema.xml,stopwords.txt</str>
           </lst>
       <!--
           <lst name="slave">
             <str name="masterUrl">http://your-master-hostname:8983/solr</str>
             <str name="pollInterval">00:00:60</str>
           </lst>
        -->
    </requestHandler>
    ```

4. Set the following properties in the solrcore.properties file:

    ```bash
    enable.master=true
    enable.slave=false
    ```

5. Configure all other slave servers (if any) to point to the new master server. Make sure that the state of the slave indexes is either behind or equal to the state of the master server. For more information, see [Configuring Solr slave](#configuring-solr-slave).

After the previously broken master server is fixed, it can either be discarded, run as a slave, or run as a second master. To run as a slave, make sure it is behind the new master. It can be restored from a back up of another slave or the current master server.

## Solr master-master reconfiguration

Use this information for setting up a master-master replication.

1. Set up two separate Solr instances where neither of them know about each other.

    See [Configuring Search and Insight Engine]({% link insight-engine/latest/config/index.md %}).

2. If you have a clustered environment, both the Solr installations can be done on their own Alfresco nodes in the cluster. If you don't have a clustered environment, both the Solr nodes can talk to their respective Alfresco node directly.

3. The Alfresco node can send queries to the load balancer and the load balancer can point them to either Solr node 1 (if it is up) or Solr node 2 (if Solr node 1 is down).

4. The load balancer will distribute the queries between the two Solr nodes, but then both the Solr nodes will be eventually consistent at different times.
---
title: Solr security
---

By default, communication between the repository and Solr is protected by SSL with mutual authentication. Both the repository and Solr have their own standard public/private key pair. To secure the two-way communication between the repository and Solr, you must generate your own keys.

> **Note:** For security reasons, you must generate a new set of keys to secure the Solr communication and access to the Solr Admin Console.

For more information, see [Configuring using the Admin Console]({% link insight-engine/latest/config/index.md %}#configuring-using-the-admin-console) and [Secure Keys]({% link insight-engine/latest/config/keys.md %}).

## Repository SSL keystores

Use this information to understand the keystores used by the repository for mutual TLS.

The keys and certificates required for mutual TLS on the repository side are set up in Tomcat.

1. Modify `<TOMCAT_HOME>/conf/server.xml` and add the following connector:

    ```bash
    <Connector port="8443" protocol="HTTP\1.1"
        connectionTimeout="20000"
        SSLEnabled="true" scheme="https" secure="true"
        sslProtocol="TLS" clientAuth="true"
        keystoreFile="xxxxxxx"
        keystorePass="yyyyy"
        truststoreFile="xxxxxxx"
        truststorePass="yyyyy"
    />
    ```

2. Copy the keystore and truststore files you created in [Generating secure keys for ssl communication]({% link insight-engine/latest/config/keys.md %}#generating-secure-keys-for-ssl-communication) to the machine that's running the repository.

3. Set the parameters in the connector, replacing the `xxxxxxx` and `yyyyy` values.

4. Make sure that the following property is added to the TOMCAT_HOME>/shared/classes/alfresco-global.properties file:

    ```bash
    solr.secureComms=https
   ```

## Solr SSL keystores

Solr core has two keystores that it uses for SSL. These are:

* `ssl.repo.client.keystore` contains a Solr public/private RSA key pair
* `ssl.repo.client.truststore` contains the trusted Alfresco Certificate Authority certificate (which has been used to sign both the repository and Solr certificates)

## Connecting to the SSL-protected Solr web application

The Solr Admin Web interface allows you to view Solr configuration details, run queries, and analyze document fields.

All Solr URLs, which are bundled within Alfresco Content Services, are protected by SSL. To use these URLs from a browser, you need to import a browser-compatible keystore to allow mutual authentication and decryption to work. The following steps describe how to import the keystore into your browser (these relate to Firefox, other browsers will have a similar mechanism):

1. Open the FireFox **Certificate Manager** by selecting **Firefox > Preferences > Advanced > Certificates > View Certificates > Your Certificates**.

2. Import the browser keystore `browser.p12` that is located in your `<ALFRESCO_HOME>/alf_data/keystore` directory.

3. Enter the password `alfresco`.

    A window displays showing that the keystore has been imported successfully. The **Certificate Manager** now contains the imported keystore with the repository certificate under the **Your Certificates** tab.

4. Close the **Certificate Manager** by clicking **OK**.

5. In the browser, navigate to a Solr URL, [https://localhost:8983/solr](https://localhost:8983/solr).

    The browser displays an error message window to indicate that the connection is untrusted. This is due to the certificate not being tied to the server IP address. In this case, view the certificate and confirm that it is signed by the Alfresco Certificate Authority.

6. Expand **I understand the risks**.

7. Select **Add Exception**.

8. Click **View** to display the certificate.

9. Confirm that the certificate was issued by Alfresco Certificate Authority, and then confirm the **Security Exception**.

Access to Solr is granted and the Solr Admin screen is displayed.

The Solr web interface makes it easy for administrators to view the Solr configuration details, run queries, and analyse document fields in order to calibrate a Solr configuration.

The main Solr Admin dashboard is divided into two parts: the left and center panels.

![]({% link insight-engine/images/solr-admin.png %})

## Solr Admin UI left panel

The left-side of the Solr Admin screen is a menu under the Solr logo that provides the navigation through the screens of the UI. The first set of links are for system-level information and configuration, and provide access to Logging, Core Admin and Java Properties, among other things.

After this information is a list of Solr cores configured for your Alfresco Content Services instance. Clicking on a core name shows a secondary menu of information and configuration options for that core specifically. Items in this list include the Schema, Config, Plugins, and an ability to perform queries on indexed data.

The different screens of the Solr Admin UI are described below.

### Logging

The **Logging** page shows messages from Solr's log files.

Under **Logging**, when you select **Level**, you see the hierarchy of classpaths and classnames for your Level instance. A row highlighted in yellow indicates that the class has logging capabilities. Click on a highlighted row, and a menu will appear to allow you to change the log level for that class. Characters in bold indicate that the class will not be affected by level changes to root.

![]({% link insight-engine/images/logging.png %})

### Core Admin

The **Core Admin** screen lets you manage your cores.

The buttons at the top of the screen enable you to add a new core, unload the core displayed, rename the currently displayed core, swap the existing core with one that you specify in a drop-down box, and reload the current core.

The main display and available actions provide another way of working with your cores.

![]({% link insight-engine/images/coreadmin.png %})

### Java Properties

The **Java Properties** screen displays all the properties of the JVM running Solr, including the classpaths, file encodings, JVM memory settings, operating system, and more.

![]({% link insight-engine/images/javaproperties.png %})

### Thread Dump

The **Thread Dump** screen lets you inspect the currently active threads on your server.

Each thread is listed and access to the stacktraces is available where applicable. Icons to the left indicate the state of the thread. For example, threads with a green check-mark in a green circle are in a `RUNNABLE` state.

On the right of the thread name, click the down-arrow to see the stacktrace for that thread.

![]({% link insight-engine/images/threaddump.png %})

### Core-specific tools

Click the **Core Selector** to display a list of Solr cores, with a search box that can be used to find a specific core.

When you select a core:

* the central part of the screen shows Statistics and other information about the selected core.
* a secondary menu opens under the core name with the administration options available for that particular core. The core-specific options are:

    |Options|Description|
    |-------|-----------|
    |Overview|This dashboard displays full statistics of the indexes. It shows the index count for each of the cores. It also provides a summary report and an FTS status report. The summary report displays information about the number of nodes in index, transactions in index, approximate transactions remaining, and so on. The FTS status report displays information about the FTS status clean, FTS status dirty, and FTS status new.|
    |Analysis|Allows data analysis according to the field, field type and dynamic rule configurations found in `schema.xml`.|
    |Dataimport|Displays information about the current status of the Data Import Handler. It enables you to import commands as defined by the options selected on the screen and defined in the configuration file.|
    |Documents|Provides a simple form allowing execution of various Solr indexing commands directly from the browser. The screen allows you to: Copy documents in JSON, CSV or XML and submit them to the index, upload documents (in JSON, CSV or XML), and Construct documents by selecting fields and field values|
    |Files|Displays the current core configuration files such as `solrconfig.xml` and `schema.xml`. Configuration files cannot be edited with this screen, so a text editor must be used.|
    |Ping|Enables you to ping a named core and determine whether the core is active. The Ping option does not open a page, but the status of the request can be seen on the core overview page shown when clicking on a collection name. The length of time the request has taken is displayed next to the Ping option, in milliseconds.|
    |Plugins/Stats|Displays statistics for plugins and other installed components.|
    |Query|Enables you to submit a structured query about various elements of a core.|
    |Replication|Displays current replication status for the core and lets you enable/disable replication.|
    |Schema Browser|Displays schema data in a browser window.|
    |Segments info|Visualization of the various segments in the underlying Lucene index for this core|

## Solr Admin UI center panel

The center of the screen shows the detail of the Solr core selected, such as statistics, summary report, and so on.

### Core-specific details

On the left-side of the Solr Admin screen, you will see **Core Selector**. Clicking on the menu displays a list of Solr cores hosted on this Solr node, with a search box that can be used to find a specific core by name.

This includes a sub-navigation for the option or text or graphical representation of the requested data.

See [Solr Admin UI left panel](#solr-admin-ui-left-panel) and [Solr Admin UI center panel](#solr-admin-ui-center-panel) to know more about each screen.

## Solr backup directory

To address the security issue [https://nvd.nist.gov/vuln/detail/CVE-2020-13941](https://nvd.nist.gov/vuln/detail/CVE-2020-13941){:target="_blank"}, it is necessary to configure the location parameter of the replication handler to be invariant.

This configuration is already provided in `solrconfig.xml`.

```xml
<requestHandler name="/replication" class="org.alfresco.solr.handler.AlfrescoReplicationHandler" > 
    <!--
    This invariant is needed to prevent the usage of location parameter in the replication handler APIs.
    There is no validation for location parameter. This results in a vulnerability described in https://nvd.nist.gov/vuln/detail/CVE-2020-13941
    -->
    <lst name="invariants">
        <str name="location">${solr.backup.dir:.}</str>
    </lst>
</requestHandler>
```

To specify the backup location you must configure a parameter called `solr.backup.dir` in the `solrcore.properties` file. The parameter determines the root backup directory and one must be created for each core, in advance of when you start Solr.

For example, if you have one core then the parameter might be set to `/var/data/solr/backup` and you must create that directory before starting Solr. If you have two cores, called `alfresco` and `archive`, then the parameter might be set to `/var/data/solr/backup/alfresco`, `/var/data/solr/backup/archive` and you must create those directories before starting Solr.
---
title: Transactional metadata query
---

Alfresco Content Services supports the execution of a subset of the CMIS Query Language (CMIS QL) and Alfresco Full Text Search (AFTS) queries directly against the database. Also, the noindex subsystem supports queries only against the database. This collection of features is called transactional metadata query (TMDQ).

TMDQ supports use cases where eventual consistency is not the preferred option.

The Solr subsystem is eventually consistent. A change can take any length of time to be reflected in the index, ranging from a few seconds to several minutes. Solr indexes the metadata and the content of each updated node, in the order in which the nodes were last changed. The rate at which the nodes are indexed is mainly determined by the time it takes to transform the content and the rate at which the nodes are being changed.

Some queries can be executed both transactionally against the database or with eventual consistency against the Solr index. Only queries using the AFTS or CMIS query languages can be executed against the database. The Lucene query language cannot be used against the database whereas, `selectNodes` (XPATH) on the Java API always goes against the database, walking and fetching nodes as required.

Improvements to tracking in the Alfresco Solr 6 integration results in less lag to metadata indexing. Metadata updates are impacted less by content indexing or the bulk updates to PATH for `move`, `rename`, `link` and, `unlink` operations.

The database can only be used for a subset of all the queries. These queries can be in the CMIS QL or AFTS QL. CMIS QL expressions are more likely to use TMDQ because of the default behavior to do exact matches. AFTS QL defaults to full text search and uses constructs not supported by the database engine. For example, PATH queries.

In general, TMDQ does not support:

* Structural queries, full text search, and special fields: This includes SITE that are derived from structure and long strings (> 1024 characters). Text fields support exact and pattern-based matching subject to the database collation. Filter queries are rewritten along with the main query to create one large query. Ordering is fine, but again subject to database collation for text.
* Faceting.
* Any aggregation: This includes counting the total number of matches for the query.

AFTS and CMIS queries are parsed to an abstract form. This is then sent to an execution engine. There are two execution engines: the database and the Solr index. The default is to try the database first and fall back to the Solr index, if the query is not supported against the database. This is configurable for a search subsystem and per query using the Java API.

To support TMDQ:

* Alfresco Content Services supports TMDQ by default.

## Features

The following are the available feature of the transactional metadata query.

* Transactional metadata query is supported for both Solr 6 and noindex search subsystems.
* Transactional metadata query does not support facets.
* When you enable transactional metadata queries, a query is parsed to check if all of its parts are supported by the database-based query engine. If yes, the database is used automatically.
* Using the database gives transactional consistency as opposed to the eventual consistency provided by Solr 6.
* If you use the transactional metadata query with the noindex subsystem, the search functionality in Alfresco Share won't work as it relies on full text search.
* Normally, a query will be executed against the database, if possible. Database execution of a query depends on the query itself. It also depends on the application of an optional patch to the database, which creates the required supporting database indexes. If the supporting indexes have been created, each index subsystem can be configured to:
* perform transactional execution of queries;
* execute queries transactionally, when possible, and fall back to eventual consistency; or
* always execute eventual consistency.
* When queries are executed against the database:
* Hidden nodes will be returned by the database, as they are in Alfresco Content Services 5.0.
* Large result sets are not supported because Alfresco Content Services does not evaluate permissions in query but as a post filter.
* Counts will not reflect the number of nodes that match the query.
* The `SearchParameters` and `QueryOptions` objects can be used to override this behaviour per query.
Alfresco Content Services supports the execution of a subset of the CMIS Query Language (CMIS QL) and Alfresco Full Text Search (AFTS) queries directly against the database. Also, the noindex subsystem supports queries only against the database. This collection of features is called transactional metadata query (TMDQ).

## Options supported by Query Languages

Use this information to know what options are supported by the Public API, CMIS Query Language (QL), and Alfresco Full Text Search Query Language (FTS QL).

### Public API and TMDQ

From public API, anything that is not a simple query, a filter query, an option that affects these, or an option that affects what is returned for each node in the results, is not supported by TMDQ.

TMDQ supports:

* `query`
* `paging`
* `include`
* `includeRequest`
* `fields`
* `sort`
* `defaults`
* `filterQueries`
* `scope` (single)
* `limits` for permission evaluation

The default limits for permission evaluation will restrict the results returned from TMDQ based on both the number of results processed and time taken. These can be increased, if required.

The Public API does not support TMDQ for:

* `templates`
* `localisation` and `timezone`
* `facetQueries`
* `facetFields`
* `facetIntervals`
* `pivots`
* `stats`
* `spellcheck`
* `highlight`
* `ranges facets`
* Solr `date math`

Some of these will be ignored and produce transactional results; others will fail and be eventual.

The Public API ignores the SQL select part of a CMIS query and generate the results as it would do for AFTS.

### CMIS QL & TMDQ

For CMIS QL, all expressions except for `CONTAINS()`, `SCORE()`, and `IN_TREE()` can now be executed against the database. Most data types are supported except for the CMIS uri and html types. Strings are supported but only if there are 1024 characters or less in length.

In Alfresco One 5.0, `OR`, decimal, and boolean types were not supported; it is only from Alfresco One 5.1 onwards that they are supported.

Primary and secondary types are supported and require inner joins to link them together. You can skip joins to secondary types from the fetch in CMIS using the public API. You would need an explicit `SELECT` list and supporting joins from a CMIS client. You still need joins to secondary types for predicates and ordering. As CMIS SQL supports ordering as part of the query language, you have to do it there and not via the Public API sort.

For multi-valued properties, CMIS QL supports `ANY` semantics from SQL 92. A query against a multi-lingual property, such as title or description, is treated as multi-valued and may match in any language. In the results, you will see the best value for your locale, which may not match the query. Also, ordering will consider any value.

### *UPPER() and LOWER()

`UPPER()` and `LOWER()` functions were in early drafts for the CMIS 1.0 specification, but were subsequently dropped. These are not part of the CMIS 1.0 or 1.1 specifications. They are not supported in TMDQ.

### Alfresco FTS QL & TMDQ

It is more difficult to write AFTS queries that use TMDQ as the default behaviour is to use full text queries for text. These cannot go against the database. Also, special fields like `SITE` and `TAG` that are derived from the structure will not go to the database. `TYPE`, `ASPECT` and the related exact matches work fine with TMDQ. All property data types are fine but strings should be less than 1024 characters in length. Text queries have to be prefixed with `=` to avoid full text search. Additionally, there is partial support for `PARENT` queries, but database queries will be missing any categories since there is no notion of category paths in the database.

Ranges, PATH, and ANCESTOR are not currently supported.

### Database & TMDQ

Some differences between the database and TMDQ:

* The database has specific fixed collation as defined by the database schema. This affects all string comparisons, such as ordering or case sensitivity in equality. Solr uses Java localised collation and supports more advanced ordering and multi-lingual fields. The two engines can produce different results for lexical comparison, case sensitivity, ordering, or when using `mltext` properties.
* The database results include hidden nodes. You can exclude them in the query. The Solr index results will never include hidden nodes and respects the index control aspect.
* The database post filters the results to apply permissions. As a result, no total count can be provided and large result sets are not well supported. This also affects paging behaviour. Permission evaluation is truncated by time or number of evaluations. TMDQ is not intended to scale to more than 10s of thousands of nodes. It will not perform well for users who can read one node in a million. It cannot and will not tell you how many results matched the query. To do this could require an inordinate number of permission checks. It does enough to give you the page requested. The Solr index can apply permissions at query and facet time to billions of nodes. For the same reason, do not expect any aggregation support in TMDQ.
* `CONTAINS()` support is complicated. The pure CMIS part of the query and `CONTAINS()` part are melded together into a single abstract query representation. By default, in CMIS the `CONTAINS()` expression implies full text search, so the queries will go to the Solr index.
* The database does not score. It will return results in some order that depends on the query plan, unless you ask for specific ordering. A three part `OR` query, where some documents match more than one constraint, is treated as equal. For Solr index queries, the more parts of an `OR` match, the higher is the score. The docs that match more optional parts of the query will come higher up.
* Queries from Share will not use TMDQ as they will most likely have a full text part to the query and ask for facets.

### Exact match and patterns

TMDQ can support exact match on all properties (subject to database collation) regardless of the property index configuration in the data model. All text properties can support pattern matching. The database index supports a fixed number of leading characters. The database store a maximum string size before it overflows to another form. Only short form strings can be used in database queries.

Solr supports exact match on all non-text properties. Text properties only support exact and pattern matches if set to tokenised `both` or `false` in the data model. Solr provides supports values up to approximately 32,700 UTF-8 bytes.

The following specific CMIS QL fields are supported:

* `cmis:parentId`
* `cmis:objectcId`
* `cmis:objectTypeId`
* `cmis:baseTypeId`
* `cmis:contentStreamMimeType`
* `cmis:contentStreamLength`

The following CMIS QL comparison operators are supported:

* `=`, `!=,` `<>`, `<`, `<=`, `>`, `>=`
* `IN`, `NOT IN`, `LIKE`

The following AFTS exact matches and patterns are supported:

* `=<field>:term`
* `=<field>:ter*`
* `=<field>:*erm`

### Full text search for CMIS QL and AFTS

* CMIS QL
  * IN_TREE()
  * IN_FOLDER()
* AFTS
  * PATH

### Supported for special fields in TMDQ using AFTS

* TYPE
* ASPECT
* EXACTTYPE
* EXACTASPECT
* PARENT - Note that database queries will not contain any categories since there is no notion of category paths in the database

> **Note:** CMIS QL does not support any use of CONTAINS() using the database.

Transactional Metadata Query and the Solr index queries are intended to support different use cases. They differ in queries and options that they support and in the results they generate with respect to collation and scoring.

## Transactional metadata queries supported by database

Use this information to understand the queries supported by the database.

The Alfresco Full Text Search (FTS) query text can be used standalone or it can be embedded in CMIS-SQL using the `contains()` predicate function. The CMIS specification supports a subset of Alfresco FTS. For more information on search syntax, see [Alfresco Full Text Search Reference]({% link insight-engine/latest/using/sql/syntax.md %}).

**CMIS QL**

The following object types and their sub-types are supported:

* `cmis:document`

    For example:

    ```sql
    select * from cmis:document
    ```

* `cmis:folder`

    For example:

    ```sql
    select * from cmis:folder 
    ```

* Aspects

    For example:

    ```sql
    select * from cm:dublincore 
    ```

## CMIS property data types

The `WHERE` and `ORDER BY` clauses support the following property data types and comparisons:

* `string`
  * Supports all properties and comparisons, such as `=`, `<>`, `<`, `<=`, `>=`, `>`, `IN`, `NOT IN`, `LIKE`
  * Supports ordering for single-valued properties
    For example:

    ```sql
    select * from cmis:document where cmis:name <> 'fred' order by cmis:name
    ```

* `integer`
  * Supports all properties and comparisons, such as `=`, `<>`, `<`, `<=`, `>=`, `>`, `IN`, `NOT IN`
  * Supports ordering for single-valued properties

* `double`
  * Supports all properties and comparisons, such as `=`, `<>`, `<`, `<=`, `>=`, `>`, `IN`, `NOT IN`
  * Supports ordering for single-valued properties
* `float`
  * Supports all properties and comparisons, such as `=`, `<>`, `<`, `<=`, `>=`, `>`, `IN`, `NOT IN`
  * Supports ordering for single-valued properties
* `boolean`
  * Supports properties and comparisons, such as `=` and `<>`
  * Supports ordering for single-valued properties
* `id`
  * Supports `cmis:objectId`, `cmis:baseTypeId`, `cmis:objectTypeId`, `cmis:parentId`, `=`, `<>`, `IN`, `NOT IN`
  * Ordering using a property, which is a CMIS identifier, is not supported
* `datetime`
  * Supports all properties and comparisons `=`, `<>`, `<`, `<=`, `>=`, `>`, `IN`, `NOT IN`
  * Supports ordering for single-valued properties
    For example:

    ```sql
    select * from cmis:document where cmis:lastModificationDate = '2010-04-01T12:15:00.000Z' order by
     cmis:creationDate ASC
    ```

> **Note:** While the CMIS URI data type is not supported, multi-valued properties and multi-valued predicates as defined in the CMIS specification are supported. For example,

```sql
select * from ext:doc where 'test' = ANY ext:multiValuedStringProperty
```

## Supported predicates

A predicate specifies a condition that is true or false about a given row or group. The following predicates are supported:

* Comparison predicates, such as `=`, `<>`, `<`, `<=`, `>=`, `>`, `<>`
  * `IN` predicate
  * `LIKE` predicate

    > **Note:** Prefixed expressions perform better and should be used where possible.

* `NULL` predicate 
* Quantified comparison predicate (`= ANY`)
* Quantified IN predicate (`ANY .... IN (....)`)
* `IN_FOLDER` predicate function

## Unsupported predicates

The following predicates are not supported:

* TEXT search predicate, such as `CONTAINS()` and `SCORE()` 
* `IN_TREE()` predicate

## Supported logical operators

The following logical operators are supported:

* `AND` 
* `NOT`
* `OR`

## Other operators

In the following cases, the query will go to the database but the result might not be as expected. In all other unsupported cases, the database query will fail and fall back to be executed against the Solr 6 subsystem.

* `IS NOT NULL`
* `IS NULL`: Currently, this operator will only find properties that are explicitly NULL as opposed to the property not existing.
* `SORT`: The multi-valued and `mltext` properties will sort according to one of the values. Ordering is not localized and relies on the database collation. It uses an `INNER JOIN`, which will also filter NULL values from the result set.
* `d:mltext`: This data type ignores locale. However, if there is more than one locale, the localised values behave as a multi-valued string. Ordering on `mltext` will be undefined as it is effectively multi-valued.
* `UPPER()` and `LOWER()`: Comparison predicates provide additional support for SQL `UPPER()` and LOWER() functions (that were dropped from a draft version of CMIS specification but are supported for backward compatibility).

## Configuring transactional metadata query

Configure the transaction metadata query using the subsystem properties.

The common properties used to configure the transactional metadata query for the search subsystems are:

* `solr.query.cmis.queryConsistency`
* `solr.query.fts.queryConsistency`

These properties should be set in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file.

The default value for these properties is `TRANSACTIONAL_IF_POSSIBLE`. However, you can override it with any of the following permitted values:

* `EVENTUAL`
* `TRANSACTIONAL`

The `solr.query.cmis.queryConsistency` and `solr.query.fts.queryConsistency` properties can also be set per query on the `SearchParameters` and `QueryOptions` objects.

## Configuring an optional patch for upgrade

Transactional metadata query requires two optional patches to be applied for full support. If no patch is applied there is no database support.

The first patch does not support boolean, float or double properties, and disjunction (OR). It adds the database support for TMDQ equivalent to an out-of-the-box Alfresco One 5.0 install (where float, double, boolean, and disjunctions are not supported).

The second patch adds the database support for TMDQ equivalent to an out-of-the-box Alfresco One 5.1 install. Some CMIS QL use cases where `OR` would be used are supported by using `IN`. In Alfresco One 5.1 and later versions, these restrictions go away after applying all TMDQ optional patches. The database size will be approximately 25% larger with all indexes applied.

To use or run a query against the `float`, `double`, or `boolean` property data types, you need to run an optional patch that adds the required indexes to the database. To do so, set the following property in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file:

```bash
system.metadata-query-indexes-more.ignored=false 
```

When using all other data types (such as `string`, `integer`, `id`, or `datetime`), to enable the patch that adds the required indexes to the database, set the following property in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file:

```bash
system.metadata-query-indexes.ignored=false 
```

If these optional patches are not run, the metadata query will not be used, regardless of the configuration. This configuration is checked when the subsystem is reloaded.

For a new install, the default behavior is to use the `TRANSACTIONAL_IF_POSSIBLE` metadata queries. For an upgraded system, the `TRANSACTIONAL_IF_POSSIBLE` metadata queries will be used only if the upgrade patches have been run.

## Adding optional indexes to a database

When you are upgrading the database, you can add optional indexes in order to support the metadata query feature. This information lets you know the likely duration of the upgrade and how to do it incrementally.

For large repositories, creating the database indexes to support the transactional metadata query can take some time. To check how long it will take, you can add the first index to the database and note the time taken. The full upgrade is estimated to take less than 10 times this value. However, this can vary depending on the structure of the data, the database, and the size of the repository.

The [SQL patch script](http://dev.alfresco.com/resource/AlfrescoOne/5.0/configuration/alfresco/dbscripts/upgrade/4.2/org.hibernate.dialect.Dialect/metadata-query-indexes.sql) can be run in parts, adding one index at a time. The patch is marked complete by the statement that inserts into alf_applied_patch. The patch can be marked as unapplied using the SQL delete statement.

## Configuring search in Alfresco Share

The following sections describe how to configure search in Alfresco Share.

## Controlling permissions checking

You can limit the time Alfresco Content Services spends on ensuring that the user executing the search has the necessary permissions to see each result. Setting this limit increases search speed and reduces the use of resources.

You can limit both the time spent and the number of documents checked before Alfresco Content Services returns a search query using the `system.acl.maxPermissionCheckTimeMillis` and the `system.acl.maxPermissionChecks` properties. The default values are 10000 and 1000 respectively.

1. Open the `<classpathRoot>/alfresco-global.properties` file.

2. Set the `system.acl.maxPermissionCheckTimeMillis` property.

    For example, `system.acl.maxPermissionCheckTimeMillis=20000`.

3. Set the `system.acl.maxPermissionChecks` property.

    For example, `system.acl.maxPermissionChecks=2000`.

    > **Note:** If you increase these values and have a query that returns a very large number of results, (a) the search results will take longer to be returned to the user, and (b) the system will spend longer to check permissions, leading to the possibility of performance degradation. If you set these values to a low number, you run the risk of inconsistent search results every time you run the same search. These settings are also applied when paging. So paging the results will only go up to the maximum returned results based on these settings.

From Content Services 7.x you can set these limits on a per query basis which overrides the values set in the `alfresco.global.properties` file.
To do this in the REST API you must add a limits element value to the request JSON:

```sql
"limits": {
  "permissionEvaluationTime": 20000,
  "permissionEvaluationCount": 2000
}
```

In the Java API the `SearchParameters` object has the following methods:

* `setMaxPermissionChecks(int)`
* `setMaxPermissionCheckTimeMillis(long)`

## Controlling search results

Use this information to control the maximum number of items that an Alfresco Share search returns.

By default, the Share search feature returns a maximum of 250 search results. You can extend this number of search results to return more than 250 entries.

1. Download the [share-config.xml](http://dev.alfresco.com/resource/AlfrescoOne/5.1/configuration/alfresco/share-config.xml) file.

2. Open the share-config.xml file and copy the `<config evaluator="string-compare" condition="Search" replace="true">` section.

3. Open the `<web-extension>share-config-custom.xml` file and then paste the copied section.

4. Locate the `<max-search-results>250</max-search-results>` property and then edit the value to your preferred number of search results.

5. For the changes to take effect, refresh the Alfresco Content Services web scripts. To refresh the web scripts:

    1. Navigate to the web scripts Home page.

        For example, go to: `http://<your-host>:8080/share/page/index`.

    2. Click **Refresh Web Scripts**.

        You have now refreshed the web scripts and set a limit to the number of items a search in Share returns.

> **Note:** Custom searches and searches from the node browser use the `solr.query.maximumResultsFromUnlimitedQuery` property to control search results. For more information, see [Solr core configuration properties
]({% link insight-engine/latest/config/index.md %}#solr-core-configuration-properties).
---
title: Setting up Solr sharding
---

After creating the shards manually, an Alfresco Content Services administrator has to instruct Alfresco Content Services how to find the indexes. This can either be done manually by configuring the indexes, or by allowing Alfresco Content Services to discover shards dynamically. This section describes how to create and configure Solr sharding.

As shown in the diagram below, the trackers communicate with the repository. When the user initiates a query, it can either be executed by manually mapping the stores (explicit configuration), or by shard registry via dynamic sharding. Dynamic sharding determines what best shards are available to answer a query. The shard registry stores all the information about that particular index, for example the status of the index, transactions in index, and so on.

![]({% link insight-engine/images/solr-shard-overview.png %})

The query is sent to Solr and then to the request handler. The request handler determines if the query is local or distributed. In case of a distributed query, the query is sent to other parts of the index and then combined into an overall result.

The distributed query is done is two phases. Phase 1 involves query and an initial round of faceting, and Phase 2 involves pulling back information from each relevant document and facet refinement.

The following diagram shows the difference between manual and dynamic sharding. In this example, there are 4 shards (1, 2, 3, and 4) and 2 instances for each shard (A & E, B & F, C & G, and D & H). Instances A, B, C, D, and F are up-to-date, while the instances E and G are lagging behind and can't be used. Shard instance H is silent and therefore, unavailable for querying.

![]({% link insight-engine/images/dynamic-shards.png %})

In manual sharding, the user is only aware of the existence of the shards and its instances but knows nothing about the status of each shard and its instance(s). So, the query can be sent to any instance. In dynamic sharding, Alfresco Content Services will use instance A, B, C, D, or F for querying.

![]({% link insight-engine/images/dynamic-sharding.png %})

At query time, Solr is aware of all the available nodes and selects one node as the coordinator (one node from all the available green ones) and sends the request to it. Also, the shards (A, B, C, D or A, F, C, D) to be used for that request are selected dynamically. In this case, Solr selects F instead of B. So, if one node lags behind or stops responding, Solr stops using it.

## Creating Solr shards manually

You can control the distribution of your index by creating, configuring, and registering shards manually.

### Manual sharding overview

An index can be distributed over several Solr nodes by creating and configuring shards. This can be achieved in three steps. First, the Solr nodes (i.e. instances of Alfresco Content Services) must be started, second the shards must be created, and finally Alfresco Content Services must be configured to point to the Solr nodes.

1. Set the configuration properties that apply to all the cores in a Solr instance in the `<ALFRESCO_HOME>/alfresco-insight-engine/solrhome/conf/shared.properties` file.

   For shard registration, Alfresco Content Services needs to know the Solr port where the requests should be sent. This can be configured, along with an explicit host name.

    ```bash
    solr.host=<hostname>
    solr.port=8983
    ```

    These properties will be used when registering all cores found under the `<SOLR_HOME>` directory. For more information, see [About shared.properties file](#about-shared.properties-file).

    Once the basic configuration is [complete]({% link insight-engine/latest/config/index.md %}#solr-configuration-files) then start the Solr nodes.

2. Setup and configure the Solr nodes.

    **Example: Creating shards**

Let's consider an example for creating 8 shards, 3 instances of each shard, and 6 Solr nodes. As shown below, each node will get 4 different shards.

|  |Shard 0|Shard 1|Shard 2|Shard 3|Shard 4|Shard 5|Shard 6|Shard 7|
|--|-------|-------|-------|-------|-------|-------|-------|-------|
|Node 1|x||||x|x|x||
|Node 2||x||||x|x|x|
|Node 3||x|x||||x|x|
|Node 4|x||x|x||||x|
|Node 5|x||x|x|x||||
|Node 6||x||x|x|x|||

To achieve this sharding configuration, follow the steps below for each Solr node N:

1. Delete any existing `alfresco` and `archive` cores using the following commands.

    ```http
    https://<hostnameN>:8983/solr/admin/cores?action=removeCore&storeRef=workspace://SpacesStore&coreName=alfresco
    https://<hostnameN>:8983/solr/admin/cores?action=removeCore&storeRef=workspace://SpacesStore&coreName=archive
    ```

2. Recreate the sharded cores to set up index tracking.

   Call the following URLs:

    ```http
    http://<hostnameN>:<portN>/solr/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=8&nodeInstance=N&replicationFactor=3&numNodes=6&template=rerank
    http://<hostnameN>:<portN>/solr/admin/cores?action=newCore&storeRef=archive://SpacesStore&numShards=8&nodeInstance=N&replicationFactor=3&numNodes=6&template=rerank
    ```

3. For each core (alfresco and archive), the properties can be set at the creation time or updated later.

    ```http
    https://<hostnameN>:<portN>/solr/admin/cores?action=updateCore&storeRef=system://system&property.data.dir.store=<SOME_VALUE>
    ```

You should now have six nodes with four cores, each actively tracking the repository. The following URL options are available for use:

|URL option|Description|
|----------|-----------|
|numShards|Specifies the number of logical shards, for example `8`.|
|storeRef|Specifies reference to a node store, for example `workspace://SpacesStore`|
|template|Defines the base configuration for a new Solr core with some configuration properties set using the URL as shown in Step 1(b).For more information, see [Core templates](#core-templates), for example `template=rerank`.|
|replicationFactor|Specifies the number of copies of each document (or, the number of physical instances to be created for each logical shard). A `replicationFactor` of 3 means that there will be 3 instances for each logical shard, for example `3`.|
|nodeInstance|Specifies the Solr node instance being configured, for example `6`.|
|numNodes|Returns the total number of Solr nodes for example `6`.|
|coreName|Specifies the name of the Solr core, for example `alfresco`.|
|property.<>|Specifies the property and its value, for example `property.data.dir.store=...`|

3. Configure Alfresco Content Services by setting the Solr subsystem properties.

    Set the three Solr subsystem properties for both the `alfresco` and `archive` cores in the alfresco-global.properties file. For example, you can set the properties as shown below:

    ```bash
    solr6.store.mappings.value.solrMappingAlfresco.nodeString=<hostname1>:<port1>/<url1>,<hostname2>:<port2>/<url2>
    solr6.store.mappings.value.solrMappingAlfresco.numShards=8
    solr6.store.mappings.value.solrMappingAlfresco.replicationFactor=3
    solr6.store.mappings.value.solrMappingArchive.nodeString=<hostname1>:<port1>/<url1>,<hostname2>:<port2>/<url2>
    solr6.store.mappings.value.solrMappingArchive.numShards=8
    solr6.store.mappings.value.solrMappingArchive.replicationFactor=3
    ```

In the above examples, `nodeString` is a list of URLs where the `alfresco` core can be accessed.

For a two node system with Solr node 1: `http://<hostname1>:<port1>/solr/#/alfresco`, and Solr node 2: `http://<hostname2>:<port2>/solr/#/alfresco`, then:

   ```bash
   solr6.store.mappings.value.solrMappingAlfresco.nodeString=<hostname1>:<port1>/solr/#/alfresco,<hostname2>:<port2>/solr/#/alfresco
   ```

Similarly, set `nodeString` for the `archive` core.

> **Note:** These properties can also be configured via a JMX client or using the subsystem properties to reference the composite beans.
> **Note:** If the host, port, or URL is missing, the subsystem default values (the ones set for a single index) will be used. Ensure the hosts are in the correct order. This is because Solr assumes that the shards are located on node 1, etc. as defined in the above list when generating queries. At query time, a Solr core is selected at random to do the distribution of all shards, again, selected at random.

### Core templates

Core templates are used to define the base configuration for a new Solr core with some configuration properties.

Search and Insight Engine provides two Solr core templates out of the box. These templates live in the following folders:

```bash
<SOLR_HOME>/templates/rerank
<SOLR_HOME>/templates/noRerank
```

* The `rerank` template includes tuning on rating scores in order to obtain finer relevance and precision.
* The `noRerank` template provides the same configuration but without tuning.

If you don't specify additional options when creating the cores, the `rerank` template is taken as the base configuration for both the `alfresco` and `archive` cores. For example, this is what happens when you use the "`-Dcreate.alfresco.defaults=alfresco,archive`" option. In this example, the `rerank` folder is copied to your deployment directories (as shown below), and `noRerank` is never used:

```bash
<SOLR_HOME>/templates/rerank >> <SOLR_HOME>/alfresco
<SOLR_HOME>/templates/rerank >> <SOLR_HOME>/archive
```

So, if you're creating your Solr cores from scratch, you only need to modify the following file:

```bash
<SOLR_HOME>/templates/rerank/conf/solrcore.properties
```

If you're using a persistent storage configuration, with both `alfresco` and `archive` cores, having indexes, you need to change the configuration for the properties file for each core:

```bash
<SOLR_HOME>/archive/conf/solrcore.properties
<SOLR_HOME>/alfresco/conf/solrcore.properties
```

The core templates are specified in the URL used for creating shards, as shown below:

```http
http://<hostN>:<portN>/solr/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=8&nodeInstance=N&replicationFactor=3&numNodes=6&**template=<template>**
```

The `<SOLR_HOME>/templates` directory contains the following structure:

|Templates|Description|
|---------|-----------|
|rerank|This template is an enhanced core configuration for Alfresco Content Services. To use rerank, you need to reindex using this template when creating a new core. It has more appropriate settings for sharding and supports indexes containing approximately 50-80M documents per shard.|
|noRerank|This template matches how the alfresco and archive cores were defined in Alfresco One 5.0. In addition, it supports auto-phrasing and query re-ranking.|

The core templates include `schema.xml` and `solrconfig.xml`. The main purpose is to create multiple cores on multiple machines with the same configuration.

> **Note:** The `aps` and `rerankWithQueryLog` templates have been removed from the default distribution of Search and Insight Engine from version 1.4 onwards.

#### Comparison between the rerank and noRerank templates

|No.|Rerank template|noRerank template|
|---|---------------|-----------------|
|1|The rerank template causes less duplication of the index, and therefore the index is more compact.|The noRerank template causes more duplication of the index, and therefore the index is large.|
|2|In the rerank template, stop words are included and indexed as common grams. By default, majority of the 100 most frequently used words in English language text are now treated as stop words. For more information, see `<SOLR_HOME>/templates/rerank/conf/lang/stopwords_en.txt`.|In the noRerank template, stop words are removed from the words that are tokenised in the English language. For more information, see `<SOLR_HOME>/templates/norerank/conf/lang/stopwords_en.txt`.|
|3|The rerank template supports real rerank with automatic phrasing (or auto-phrasing). Queries are run in two stages: 1. Stage one treats phrases as conjunctions and ignores expensive positional information. 2. Stage two reranks the top queries using a more expensive phrase. When a user provides individual search terms in a query, the automatic phrasing feature groups those individual terms into a search phrase and returns the query results for the phrase. |The noRerank core performs auto-phrasing without re-ranking but the auto-phrase is added to the query.|

### About shared.properties file

The `<ALFRESCO_HOME>/alfresco-insight-engine/solrhome/conf/shared.properties` file is used to set configuration that applies to all the cores in a Solr instance.

Most of these settings need to be replicated across all the Solr instances that are a part of the sharded index. However, there are some properties related to dynamic shard registration, such as host and port, which can be set for each machine.

These Solr instance specific settings can be omitted but you may have to define the correct host that the repository will use to communicate to Solr, for example, using an internal IP address in a cloud environment. By default, the host is detected by Java, the port will default to 8080, and the tomcat port is either determined by JMX or that explicitly defined in the shared.properties file.

The shared.properties file defines the:

* properties that are treated as identifiers
* properties that are used to generate suggestions
* data types that support cross locale/word splitting/token pattern
* properties that support cross locale/word splitting/token pattern
* `solr.host` property
* `solr.port` property

#### Properties defined in the shared.properties file

You can define which properties are treated as identifiers, regardless of how they are defined in the model. These properties must not be tokenised. If this list is changed, a reindex is required. You can also reindex by query. For more information, see [Reindex documents by query](#reindex-documents-by-query).

If you rename the shared.properties.sample file to shared.properties, it will use the same set of identifier properties that are used in Alfresco One 5.0.

```bash
# Properties treated as identifiers when indexed

alfresco.identifier.property.0={http://www.alfresco.org/model/content/1.0}creator
alfresco.identifier.property.1={http://www.alfresco.org/model/content/1.0}modifier
alfresco.identifier.property.2={http://www.alfresco.org/model/content/1.0}userName
alfresco.identifier.property.3={http://www.alfresco.org/model/content/1.0}authorityName
alfresco.identifier.property.4={http://www.alfresco.org/model/content/1.0}lockOwner
```

You can define which properties are used for suggestion.

```bash
# Suggestable Properties

#alfresco.suggestable.property.0={http://www.alfresco.org/model/content/1.0}name
#alfresco.suggestable.property.1={http://www.alfresco.org/model/content/1.0}title
#alfresco.suggestable.property.2={http://www.alfresco.org/model/content/1.0}description
#alfresco.suggestable.property.3={http://www.alfresco.org/model/content/1.0}content
```

Suggestion can also be configured for the search subsystem and for any SOLR core using properties. If the shared.properties file is missing in Alfresco Content Services 6.2, suggestion will be configured as it is in Alfresco One 5.0.

You can define which properties are used for tokenisation with the Solr word delimiter factory.

```bash
# Data types that support cross locale/word splitting/token patterns if tokenised

alfresco.cross.locale.property.0={http://www.alfresco.org/model/content/1.0}name
alfresco.cross.locale.property.1={http://www.alfresco.org/model/content/1.0}lockOwner
```

You can define which property types are used for tokenisation with the Solr word delimiter factory.

```bash
# Data types that support cross locale/word splitting/token patterns if tokenised

# alfresco.cross.locale.datatype.0={http://www.alfresco.org/model/dictionary/1.0}text
# alfresco.cross.locale.datatype.1={http://www.alfresco.org/model/dictionary/1.0}content
# alfresco.cross.locale.datatype.2={http://www.alfresco.org/model/dictionary/1.0}mltext
```

#### Support for cross-language search

The cross core configuration options to use specific locales for cross-locale searches are set in the shared.properties file. Cross language search uses the appropriate stemmed tokens for all locales.

For backward compatibility, this file is absent in Alfresco Content Services 6.2 to provide options equivalent to Alfresco One 5.0.

To configure cross-language search, follow the steps below:

1. Open the `<ALFRESCO_HOME>/alfresco-insight-engine/solrhome/conf/shared.properties.sample` file.
2. Set the following properties:

    ```bash
    alfresco.cross.locale.property.0={http://www.alfresco.org/model/content/1.0}name
    alfresco.cross.locale.property.1=...
    ```

    This sets the properties that should be dual tokenised.

    The cross-language search in Alfresco One 5.0 is now only used to provide support to split tokens (based on case and numbers) to generate `in word` tokens. The `in word` tokenisation is mainly used for name. For example, find `RedDog12` by `Red`, `Dog`, or `12`, `Dog12`, and so on. This property must be indexed and tokenised.

3. To specify the same behaviour based on the data type, set the following properties:

    ```bash
    alfresco.cross.locale.datatype.0={http://www.alfresco.org/model/dictionary/1.0}text
    alfresco.cross.locale.datatype.1=...
    ```

#### Query time expansion of locales

Query time expansion of locales can be defined in the `solrconfig.xml` file as part of the query language definition.

|Locale parameter|Description|
|----------------|-----------|
|autoDetectQueryLocale|If true, this uses the query typed in by the user to detect the locale.|
|autoDetectQueryLocales|This specifies a set of locales. One of these may be used in executing the query if `autoDetectQueryLocale=true`.|
|fixedQueryLocales|This specifies a fixed set of locales always used by the query.|

What locales are used?

* The locale for the current session is always used.
* If the `autoDetectQueryLocale` parameter is used, then the best match from `autoDetectQueryLocales` is used. If no parameter is set, then all the possible locales are used.
* All `fixedQueryLocales` are used.

Here are some example entries in the `solrconfig.xml` file:

```bash
<queryParser name="afts" class="org.alfresco.solr.query.AlfrescoFTSQParserPlugin">
    <str name="rerankPhase">QUERY_PHASE</str>
    <str name="autoDetectQueryLocale ">true</str>
    <str name="autoDetectQueryLocales ">en,fr,de</str>
</queryParser>
```

```bash
<queryParser name="afts" class="org.alfresco.solr.query.AlfrescoFTSQParserPlugin">
    <str name="rerankPhase">QUERY_PHASE</str>
    <str name="fixedQueryLocales">en,fr,de</str>
</queryParser>
```

These are query time options and do not require a reindex. Currently, these values cannot be set in the solrcore.properties file.

#### Enabling path queries

The property alfresco.cascade.tracker.enabled provides Index fields that are required for path-based queries when set to true (the default is `true`). Disabling support for path queries (i.e. setting this to `false`) can speed up indexing in sharded systems.

Updating this property from the default setting will result in path-based fields not being populated. Consequently it should not be changed after the initial startup of the server.

> **Note:** If `alfresco.cascade.tracker.enabled` is set to false and Solr is restarted, cascaded updates are disabled.

##### When you disable cascade tracking and do not index fields that are updated on cascaded updates

This is the default setting when cascade tracking is disabled and as a result many search queries will not work, even for users with an environment where parent entries are not updated (e.g when a parent node has been renamed), such as `SITE:swsdp`.

This approach ensures search queries affected by disabling cascade tracking will not work, rather than risking inconsistent query results.

Review how the following services are affected:

* CMIS
  * `IN_TREE`, `PATH`, `PARENT`, `ANCESTOR` queries will not work.
* Search API
  * Faceted Search (Facet Fields, Pivot Facet, Facet Range), PATH, NPATH, Secondary Association, Cascade Updates, Search with Sort queries will not work.
*SQL API
  * There are at least 70 less fields found in the Solr schema.
  * SITE, PATH: fields are not indexed and SQL queries based on these fields will return null values.
  * Queries will not be successful with these fields being used in predicates, for example queries with `<select * from alfresco where Site = ‘swsdp’>`.
* Share
  * Category Manager `http://localhost:8081/share/page/console/admin-console/category-manager` can't be used.
  * TAGs can't be created or browsed.
  * Your site can be defined as a Facet for Search Results (via Search manager) but it will not work.
  * Searching within a site (or within a folder) returns a list of content within the site. This will not work, for example using `SITE:swsdp` syntax or via node browser using PATH queries.
  * Node browser default PATH query doesn’t list system and category roots and PATH queries.
    If `alfresco.cascade.tracker.enabled` is set to false and Solr is restarted cascaded updates will be disabled. To avoid inconsistencies in the results, by default the fields that are updated on cascade updates are not indexed.

    When parent paths have been updated or renamed, path queries are affected because the correct parent paths are available in the database but the Solr indexes for any children are not updated. The result of this can be inconsistent results for path queries and queries where parent/path are used.

    These types of results will affect users when their environment allows for cascaded changes. The results of a search query that use the database and search/SQL, including the index, may not always match, if the parent path is updated (only in case of renaming a parent).

## Dynamic shard registration

In dynamic shard registration, shards register as a part of the tracking process to form indexes, thereby eliminating the need to follow the manual shard distribution pattern over Solr nodes.

Unlike manual sharding, dynamic sharding does not require shards and instances to be distributed correctly over a known set of hosts. Query is resilient, with a configurable delay to instances coming and going. For manual sharding, all instances must be available on the expected host at the expected URL. While dynamic shard registration allows different numbers of instances for any shard, manual sharding does not.

To enable dynamic sharding, set the following property in the `alfresco-global.properties` file:

```bash
solr.useDynamicShardRegistration=true
```

The following properties govern which instances are chosen for a query:

```bash
search.solrShardRegistry.purgeOnInit=true
search.solrShardRegistry.shardInstanceTimeoutInSeconds=300
search.solrShardRegistry.maxAllowedReplicaTxCountDifference=1000
```

|Property|Description|
|--------|-----------|
|search.solrShardRegistry.purgeOnInit|If true, this property removes persisted shard state from the database when the subsystem starts for example, true|
|search.solrShardRegistry.shardInstanceTimeoutInSeconds|Specifies that if a shard has not made a tracking request within this time, it will not be used for query. **Note:** When tracking large change sets or rebuilding your indexes, increase the shard timeout. For example, change the value of this property to 3200 or 7200 seconds|
|search.solrShardRegistry.maxAllowedReplicaTxCountDifference|Specifies that if any shard is more than this number of transactions behind the leading instance, it will not be used, for example 1000 transactions|
|search.solrShardRegistry.dbidRangeRefreshTimeoutInSeconds|This property controls the frequency of synchronisation of the shard information between multiple ACS instances for [DB_ID_RANGE]({% link insight-engine/latest/config/sharding/index.md %}#sharding-methods-db-id-range) sharding, for example `30`. <br/><br/>**Note:** This property is only used when you are using `DB_ID_RANGE` sharding with multiple ACS instances.|

If there is more than one index for a store, the most up to date index (the one that has indexed most transactions) will be used. For each shard, an instance is chosen at random from all the shards that are actively tracking and within 1000 transactions of the lead instance.

Shards are considered to be part of the same index if they:

* track the same store
* use the same template (and therefore, Solr schema)
* have the same number of shards
* use the same partitioning method with the same configuration, if any is required
* have the same setting to transform or ignore content

In dynamic sharding, shards can be created using the same API as manual sharding or you can list the required shards as a comma-separated list of `shardIds`.

```bash
http://localhost:8080/solr/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=10&
numNodes=1&nodeInstance=1&property.data.dir.root=<SOLR_HOME>/solrhome/workspace-SpacesStore&shardIds=0,1,2,3,4
```

The status of all the available indexes, shards, and instances can be found using a JMX client. For more information, see [Indexing JMX client](#Indexing JMX client).

Dynamic sharding will currently use partial indexes to answer queries. For example, there are two shards: Shard1 and Shard2. If there are no instances for Shard2, queries will only use Shard1.

### Installing and configuring Solr shards

Follow these steps to set up sharding of a non-sharded index or change the number of instances of an already sharded index.

> **Note:** Do not use SSL with sharding.

1. Create machines to host Solr shards.

    1. These machines are basically application servers that host the Solr webapp. If you install multiple Solr webapps on the same machine, each Solr instance must have a different configuration. In the `solr.xml` file, edit the following parameters so that all Solr instances point to different root directories for each node:

        * solr/home
        * solr/model/dir

        > **Note:** All the Solr instances hosting shards on a given host must have separate model and index locations.

2. Install and start Alfresco Content Services.

3. Delete the existing Solr indexes from the installation.

    Delete the alfresco and archive cores using the following commands:

    ```http
    https://localhost:8443/solr4/admin/cores?action=removeCore&storeRef=workspace://SpacesStore&coreName=alfresco
    https://localhost:8443/solr4/admin/cores?action=removeCore&storeRef=workspace://SpacesStore&coreName=archive
    ```

4. Add any custom core templates. For more information, see [Core templates](#Core templates).

5. Configure the <SOLR_HOME>/conf/shared.properties file. For more information, see [About shared.properties file](#About-shared.properties-file).

6. Start the Solr server.

7. Create your new index shards and instances by configuring the properties on the URL.

    ![]({% link insight-engine/images/shard_dynamic.png %})

    ```http
    http://localhost:8080/solr/admin/cores?action=newCore&storeRef=workspace://SpacesStore&
    numShards=10&numNodes=1&nodeInstance=1&template=rerank&property.data.dir.root=<>
    ```

    This URL configures a sharded cluster that contains 10 shards, 1 node, and 1 instance of each shard. The following options must be used in the URL:

     * `numShards` specifies the number of logical shards.
     * `numNodes` specifies the total number of Solr nodes.
     * `nodeInstance` is the actual Solr instance corresponding to that `host:port`.
     * `template` defines the basic configuration for a new Solr core with some configuration properties. For more information, see [Core templates](#Core templates).
     * `storeRef` specifies reference to a node store.
     Here's an example to show how to set a non-SSL port manually when creating a shard.

    **Example:** If you want a sharded Solr installation with a different Tomcat port (8090), set the `property.alfresco.port` property on the URL used to create the shard. The `property.alfresco.port` property specifies the port used to communicate with the repository (or repositories through a load balancer). This property can also be set if communicating through a different host or load balancer. In this example, we will set `property.alfresco.port=8090`, as shown below:

    ```http
    http://localhost:8080/solr/admin/cores?action=newCore&storeRef=workspace://SpacesStore&
    numShards=10&numNodes=1&nodeInstance=1&template=rerank&property.data.dir.root=<>&shardIds=0,1,2,3,4
    &property.alfresco.port=8090
    ```

8. The Solr cores will register and start tracking the indexes.

    If there are two indexes for the same store, the old index will be used until both the indexes are at the same state. Thereafter, both the indexes will be used.

9. Set the following properties in the `alfresco-global.properties` file.

    ```bash
    solr.secureComms=none
    solr.useDynamicShardRegistration=true
    ```

10. Restart Alfresco Content Services.

11. You can turn off any old indexes from tracking. To do so, wait for the instances to time out which lets the new index be up-to-date. Alternatively, navigate to the JMX sharding operations and clear out all the registered shards, and start again.

You have a new live index.

### High availability configuration

Sharding a Solr index is a highly scalable approach for improving the throughput and overall performance of large repositories. It provides high availability in case a shard/node fails.

Here are a few examples of a high availability configuration in a sharded Solr setup.

#### Example 1

In this example, you will setup a sharded cluster that contains:

* 3 hosts/machines
* 3 shards
* 2 copies

![]({% link insight-engine/images/shard-ha1.png %})

These are the steps to follow:

1. Create machines to host Solr shards.
2. Install and start Alfresco Content Services.
3. Delete the Alfresco and archive cores.
4. Configure the <SOLR_HOME>/conf/shared.properties file.
5. Start the Solr server.
6. Create your new index shards and instances by configuring the properties on the URL.

    ```http
    http://localhost:8090/solr4/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=3&numNodes=3&nodeInstance=1
    &template=rerank&property.data.dir.root=<>&shardIds=0,1&property.alfresco.port=8080
    ```

    ```http
    http://localhost:8070/solr4/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=3&numNodes=3&nodeInstance=2
    &template=rerank&property.data.dir.root=<>&shardIds=1,2&property.alfresco.port=8080
    ```

    ```http
    http://localhost:8070/solr4/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=3&numNodes=3&nodeInstance=3
    &template=rerank&property.data.dir.root=<>&shardIds=0,2&property.alfresco.port=8080
    ```

7. Set the following properties in the alfresco-global.properties file.

    ```bash
    solr.secureComms=none
    solr.useDynamicShardRegistration=true
    ```

8. Restart Alfresco Content Services.

#### Example 2

Another example to setup a sharded cluster that contains:

* 5 hosts/machines
* 5 shards
* 3 copies

![]({% link insight-engine/images/shard-ha2.png %})

These are the steps to follow:

1. Create machines to host Solr shards.
2. Install and start Alfresco Content Services.
3. Delete the Alfresco and archive cores.
4. Configure the `<SOLR_HOME>/conf/shared.properties` file.
5. Start the Solr server.
6. Create your new index shards and instances by configuring the properties on the URL.

    ```http
    http://localhost:8090/solr4/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=5&numNodes=5&nodeInstance=1
    &template=rerank&property.data.dir.root=<>&shardIds=0,1,2&property.alfresco.port=8080
    ```

    ```http
    http://localhost:8070/solr4/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=5&numNodes=5&nodeInstance=2
    &template=rerank&property.data.dir.root=<>&shardIds=1,2,3&property.alfresco.port=8080
    ```

    ```http
    http://localhost:8070/solr4/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=5&numNodes=5&nodeInstance=3
    &template=rerank&property.data.dir.root=<>&shardIds=2,3,4&property.alfresco.port=8080
    ```

    ```http
    http://localhost:8070/solr4/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=5&numNodes=5&nodeInstance=4
    &template=rerank&property.data.dir.root=<>&shardIds=0,3,4&property.alfresco.port=8080
    ```

    ```http
    http://localhost:8070/solr4/admin/cores?action=newCore&storeRef=workspace://SpacesStore&numShards=5&numNodes=5&nodeInstance=5
    &template=rerank&property.data.dir.root=<>&shardIds=0,1,4&property.alfresco.port=8080
    ```

7. Set the following properties in the `alfresco-global.properties` file.

    ```bash
    solr.secureComms=none
    solr.useDynamicShardRegistration=true 
    ```

8. Restart Alfresco Content Services.

For more information, see [Solr sharding]({% link insight-engine/latest/config/sharding/index.md %}).

### Configuring sharding with the Admin Console

Search and Insight Engine supports sharded indexes with SSL. Use the Search Server Sharding page to set up and configure a Solr 6 sharded search index.

Prerequisites for viewing the Search Server Sharding page:

* Check you have installed Alfresco Content Services 6.2 or above and have a valid license.

* Support for shard groups requires a clustered license. Make sure that you enable clustering on your Alfresco Content Services license. For more information, see [Install and configure Content Services nodes]({% link content-services/latest/admin/cluster.md %}#install-and-configure-content-services-nodes) and [Uploading a new license]({% link content-services/latest/admin/license.md %}#uploadlicense).

1. Open the Admin Console. For more information, see [Launch Admin Console]({% link content-services/latest/admin/admin-console.md %}#launch-admin-console).
2. In Repository Services, click **Search Server Sharding**.

    You see the Search Server Sharding page. It displays information about dynamic shard index registration, shard groups, and shard instances.

   ![sol6]({% link insight-engine/images/solr6-shard-home.png %})

3. Under Dynamic Shard Instance Registration, select **Dynamic Shard Instance Registration** and set the other shard instance properties.

    |Shard registration property|Description|
    |---------------------------|---------------|
    |Dynamic Shard Instance Registration Enabled|Select this property to enable dynamic shard instance registration. If disabled, manual shard registration is used, for example `Yes`.|
    |Purge at Startup|This property purges all persisted dynamic shard instance information at startup, for example `No`.|
    |Instance Timeout (seconds)|This specifies the number of seconds a shard instance can go without making a tracking call for transactions to the repository before it stops being used for queries. **Note:** When tracking large change sets or rebuilding your indexes, increase the shard timeout. For example, change the value of this property to 3200 or 7200 seconds.|
    |Max Instance Transaction Lag|This specifies the maximum number of transactions an instance can lag behind the lead instance of the shard before it stops being used for queries, for example 1000.|

4. Click **Refresh** to refresh this page.
5. Click **Purge** to remove all registered shard instance information and start from clean.
6. Click **Clean** to remove inactive registered shard instance information.
7. Click **Manage** to create and manage shard instances.
    You see the Index Server Shard Management window. Use this window to create individual shards or shard groups.

    ![]({% link insight-engine/images/solr6-shard-mgmt.png %})

    1. Use Existing Index Servers to view a list of existing index servers and to create new index servers.
        To add a new index server, specify the server address in **New Index Server** and click **Add**.
        You can view the newly created index server under Target Index Servers.
        Click **Add to Target Index Servers** next to the server you want to add to the list of target index servers. **Target Index Servers** displays a list of index servers where you want to make the new shards.
    2. Under Existing Core Names, you can view a list of the core names already in use.
    3. Under Target Index Servers, you can view a list of index servers that will be used for sharding.
        To remove an index server from the list of servers that will be used for sharding, click **Remove**.
    4. Next, you need to create a core for the shard. There are two ways to do this. You can either:

        * use the Manage Default Indexes and **Manage Shared Properties** sections to create default indexes - see Step 7 (e) and 7 (f); or
        * use the New Shard Group and New Shard Instance sections to create a shard group and instance - see Step 7 (g) and 7 (i).
    5. Use Manage Default Indexes to create default indexes on the servers listed in **Target Index Servers**.

        The Manage Default Indexes section:

        * appears only when you add a new index server.
        * creates a core for a given shard, and therefore, can be used as an alternative to creating shards using the **New Shard Group** section (Step 7f).

    ![]({% link insight-engine/images/solr6-manage-indexes.png %})

     > **Important:** The cores are visible in the Solr Admin web application **only after** you create them using the Index Server Sharding page.

     * Click **Create Alfresco Index** to create an unsharded Alfresco index.
     * Click **Create Archive** to create an unsharded archive index.

      Use the **Report** section at the end of this page to view the detailed core creation message.

      Check the Solr Admin UI to ensure that both the indexes are correctly listed.

     ![]({% link insight-engine/images/solr6_shard.png %})

    6. Use **Manage Shared Properties** to update the properties that apply to all Alfresco indexes on an Index Engine.

        ![]({% link insight-engine/images/manage-properties.png %})

        These properties are the same as in alfresco-insight-engine-distribution-2.0.x.zip/solrhome/conf/shared.properties. For example:

        ```bash
        solr.host=localhost
        solr.port=8983
        solr.baseurl=/solr
        ```

    7. Alternatively, to create a shard group, set the following properties under New Shard Group:

        |Shard group property|Description|
        |--------------------|---------------|
        |Template|This specifies the template used for the shard group, for example rerank|
        |Store|This specifies the stores that are queryable for all shards, for example `workspace://SpacesStore`|
        |Core|This specifies the name of the Solr core.|
        |Properties|This specifies the properties to set on the Solr instances. These are the same properties that are set in the solrcore.properties file, for example `solr.suggester.enabled``alfresco.secureComms=https`, `alfresco.port.ssl=8443`, `alfresco.commitInterval=20000`, and `alfresco.newSearcherInterval=30000`.|
        |Shards|This specifies the total number of shards, for example 1.|
        |Instances|This specifies the total number of instances, for example 1.|

        ![]({% link insight-engine/images/shard-target-index.png %})

    8. Click **Create Shards Group** to create new shards based on the ordered list of target index servers.

    9. To create a single shard instance, set the following properties under New Shard Instance:

        |Shard property|Description|
        |--------------|---------------|
        |Index Server URL|This specifies the URL to a single index server, for example `localhost:8080/sol`|
        |Nodes|This specifies the total number of Solr nodes that have been created, for example 1.|
        |Target Index Server|This specifies, out of all the solr nodes above, the number given to the target index server node for this new shard, for example 1.|
        |Shards|This specifies the specific shards to create, on the node given above. You can also specify a comma-separated list of shards.|

        See [Solr sharding]({% link insight-engine/latest/config/sharding/index.md %}) to view examples of creating shards when calling the REST URLs directly.

        ![]({% link insight-engine/images/shard-instance.png %})

    10. Click **Create Shards** to create the new shard based on the specified instance properties.

    11. Use Report to get detailed information on shard creation and execution.

        ![]({% link insight-engine/images/shard-report.png %})

    12. Click **Close** to close the Index Server Shard Management window.

    You have successfully created an `alfresco` core and an `archive` core. To verify, in a browser, navigate to the Solr URL, `https://localhost:8983/solr"https://localhost:8443/solr4`. In the Solr Admin UI, select the core selector drop-down list and verify that both the `alfresco` and `archive` cores are present in the list.

    Validate that you can execute queries from the search public API to the archive core.

    ```json
    curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'Authorization: Basic YWRtaW46YWRtaW4=' -d '{
      "query":
      {
        "query": "foo"
      },
      "scope":
      {
        "stores": ["archive://SpacesStore"]
      }
    }' 'http://localhost:8080/alfresco/api/-default-/public/search/versions/1/search'
    ```

8. Under Shard Groups, you can view information about all the shards in the group.

    |Property|Description|
    |---------------------------|-----------|
    |Template|This specifies the template used for the Solr core, for example rerank|
    |Low Instance Shards|This specifies a list of shards that have less than the maximum number of instances.|
    |Missing Shards|This specifies a comma-separated list of shards with no instances, for example `100`.|
    |Max Repository Transaction ID|This specifies the maximum number of transaction IDs in the repository, for example `14,637`.|
    |Max Live Instances|This specifies the maximum number of instances available for any shard that can be used to answer a query, for example `1`.|
    |Remaining Transactions|This specifies the maximum number of transactions remaining for all the lead instances of all the active shards, for example `2`.|
    |Number of Shards|This specifies the total number of shards, for example `4`.|
    |Min Active Instances|This specifies the minimum number of instances available for any shard that can be used to answer a query, for example `1`.|
    |Max Changeset ID|This specifies the highest change set id in the repository, for example `104`|
    |Mode|This specifies whether the instances are `SLAVE`, `MASTER`, or `MIXED`. **Note:** The `SLAVE` and `MIXED` instances are not supported for a sharded installation, for example master.|
    |Stores|This specifies the stores that are queryable for all instances, for example `workspace://SpacesStore`.|
    |Has Content|This property is enabled if content is included for all instances, for example `Enabled`|
    |Shard Method|This specifies the method used to define shards. The default shard method is `DB_ID`. You can specify your own shard method in Index Server Shard Management screen > New Shard Group > Properties. For example, `shard.method=ACL_ID`. You can also set this property in the `alfresco-insight-engine-distribution-2.0.x.zip/solrhome/templates/rerank/conf/solrcore.properties` file.|

    ![]({% link insight-engine/images/shard-group.png %})

9. Use the instance property table to view detailed entity information for all the shards. This is the same information that is displayed in the JMX console, for example, `Base URL`, `Host`, `Last Indexed Changeset Date`, and more.

    For more information, see [Indexing JMX client](#Indexing JMX client).

    1. Click **Summary** to go to the [http://localhost:8983/solr/admin/cores?action=SUMMARY](http://localhost:8983/solr/admin/cores?action=SUMMARY) page on Solr for the specific core.

        For more information, see [Unindexed Solr Transactions]({% link insight-engine/latest/admin/monitor.md %}#unindexed-transactions).

        ![]({% link insight-engine/images/solr6-summary.png %})

    2. Click **SOLR** to go to the Solr Admin screen for the specific core.

        For more information, see [Connecting to the SSL-protected Solr web application]({% link insight-engine/latest/config/security.md %})

10. The Shard Group Report section displays information about the shard groups and instances. A tabular view of this information is displayed in the shard table in Step 9. This information is read-only.

    ![]({% link insight-engine/images/shard-group-report.png %})

11. Click **Save** to apply the changes you have made to the index server shards.

    If you do not want to save the changes, click **Cancel**.

> **Note:** Alfresco recommends that you do not use the **Solr Admin Console > Core Admin > Unload** functionality to unload indexes (either whole indexes or shards that are part of an index). Unloading an index or a shard in this way will delete it and make it unavailable for query.

If you unload or delete a shard from the Solr Admin Console, ensure you restart the Solr server and restore your indexes so that Alfresco can work properly.

### Indexing JMX client

You can use a JMX client, such as JConsole, for monitoring the status of all the available indexes, shards and its instances, and other related information.

The JMX view of all the instancess, shards, and indexes that stick together is displayed at the **MBeans > Alfresco > FlocAdmin > Attributes > Flocs** node. The **Flocs** node displays a tabular view of all the indexes formed by shard instances by registering with any member of the Alfresco Content Services cluster.

1. Open a command console.

2. Enter the following command:

    jconsole

    The **JConsole: New Connection** window displays.

3. Double-click on the Java process.

    For Tomcat, the Java process is usually labelled as `org.apache.catalina.startup.Bootstrap start`.

    The **Java Monitoring & Management** window displays.

4. Select the **MBeans** tab.

    The available managed beans display in JConsole.

5. Navigate to **Alfresco > FlocAdmin**.

    The **Attributes** and **Operations** display below it in the tree.

6. Select **Attributes**.

   * **Floc/Index level information**

        All instances that stick together to form an index have the same value for the following settings:

    |Attribute name|Description|Is configurable or displays state|
    |--------------|-----------|---------------------------------|
    |activeTrackingMode|Specifies if the instances for the index are all `SLAVE`, `MASTER`, or `MIXED`. **Note:** The `SLAVE` and `MIXED` instances are not supported for a sharded installation.|State|
    |hasContent|If the index contains content, the value of this attribute is `true`, otherwise `false`.|Configurable|
    |lowReplicaShards|Specifies a comma separated list of shards that have less than `maxReplicas`.|State| |
    |maxReplicas|Specifies the number of instances for the shard which has the maximum number of instances, for example `1`.|State|
    |maxRepoChangeSetId|Specifies the maximum changeset id in the repository, for example `5029`.|State|
    |maxRepoTxId|Specifies the maximum transaction id in the repository, for example `16903`.|State|
    |maxTransactions|Specifies the maximum number of transactions in any instance.|State|
    |minReplicas|Specifies the number of instances for the shard which has the minimum number of instances, for example `1`.|State|
    |missingShards|Specifies a comma separated list of shards with no instances.|State|
    |numberOfShards|Specifies the total number of shards, for example `2`.|Configurable|
    |shardMethod|Specifies how the nodes and ACLs are split into shards, for example `MOD_ACL_ID`.|Configurable|
    |shards|Click to display tabular data for each shard, for example `Shards`.|Displays details|
    |stores|Specifies the stores that are indexed, for example `workspace://SpacesStore`.|Configurable|
    |template|Specifies the name of the template used to create each core with common configuration, for example `rerank`.|Configurable|

      * **Shard level information**

        You can navigate through each shard using the tabular navigation.

        |Attribute name|Description|Is configurable or displays state?|
        |--------------|-----------|----------------------------------|
        |#|Specifies the shard number, for example `0`.|Configurable|
        |activeCount|Specifies the number of instances that are currently able to answer queries, for example `1`.|State|
        |activeTrackingMode|Specifies if the instances for the shard are all `SLAVE`, `MASTER`, or `MIXED`. **Note:** The `SLAVE` and `MIXED` instances are not supported for a sharded installation.|State|
        |laggingCount|Specifies the number of instances that are currently unable to answer queries because they are too far behind, for example '0'.|State|
        |maxTransactionsRemaining|Specifies the maximum number of transactions left to index for any shard instance, for example `1`.|State|
        |maxTxId|Specifies the maximum number of transaction id indexes by any instance, for example `16903`.|State|
        |silentCount|Specifies the number of instances that are no longer tracking.|State|
        |replicas|Provide details for each instance in the shard, for example `Instances`.|Displays details|

      * **Instance level information**

        |Attribute name|Description|Displays location or state?|
        |--------------|-----------|---------------------------|
        |baseUrl|Specifies the URL to access the instance, for example `/solr4/alfresco-0/`|Location|
        |host|Specifies the host where the instance is located, for example `172.31.42.83`.|Location|
        |port|Specifies the port on the host where the instance is located.|Location|
        |lastIndexedChangeSetCommitTime|Specifies the date and time of the last indexed changeset, for example `Wed Oct 28 12:09:41 GMT 2015`.|State|
        |lastIndexedChangeSetId|Specifies the last indexed changeset id in the repository, for example `5029`.|State|
        |lastIndexedTxCommitTime|Specifies the date and time of the last indexed transaction, for example `Wed Oct 28 12:30:33 GMT 2015`.|State|
        |lastIndexedTxId|Specifies the transaction id of the last indexed transaction, for example `16903`.|State|
        |lastUpdated|Specifies when the instance was last updated, for example `Wed Oct 28 13:31:30 GMT 2015`.|State|
        |state|Specifies if the instance state is `ACTIVE`, `SILENT`, or `LAGGING`.|State|
        |trackingMode|Specifies if the tracking is performed by the master.|State|
        |transactionsRemaining|Specifies the number of transactions remaining to be indexed, for example `5`.|State|

7. Select **Operations**.

     `removeAgedOutShards` removes all the shards which are too far behind and no longer tracking or are unresponsive.

     `removeAll` removes all the shards that have registered and starts from clean.

8. If you are using a sharded installation, go to **MBeans > Alfresco > Configuration > Search > managed > solr6 > Attributes** and set the number of filters using the `solr.defaultShardedFacetLimit` property.

    ```bash
    solr.defaultShardedFacetLimit=20
    ```

9. If you are using a non-sharded installation, go to **MBeans > Alfresco > Configuration > Search > managed > solr6 > Attributes** and set the number of filters using the `solr.defaultUnshardedFacetLimit` property.

    ```bash
    solr.defaultUnshardedFacetLimit=100
    ```

### Finding shards at query time

Use a JMX client to find shards at query time.

1. In JConsole, go to **MBeans > Alfresco > Configuration > Search > managed > solr6 > Attributes**.

    All the Solr attributes are listed on this page.

2. Set the following properties:

    ```bash
    solr6.alfresco.numShards=10
    solr6.archive.numShards=10
    ```

3. In JConsole, go to **MBeans > Alfresco > Configuration > Search > managed > solr6 > solr6.store.mappings**.

4. Set `numShards` for `solrMappingAlfresco` and `solrMappingArchive`.

    1. Go to **solrMappingAlfresco > Attributes > numShards** and set the value of `numShards`.

        ```bash
        numShards=10
        ```

    2. Go to **solrMappingArchive > Attributes > numShards** and set the value of `numShards`.

        ```bash
        numShards=10
        ```

## Reindex documents by query

You can selectively reindex a small subset of the index based on a query. This enables a limited rebuild of the index.

Example 1: To reindex people after changing the first name and last name tokenisation, use the following single-threaded query:

```http
http://localhost:8983/solr/admin/cores?action=reindex&query=TYPE:"cm:person"
```

Example 2: To reindex jobs that failed or threw an exception when indexing, use the following query:

```http
http://localhost:8983/solr/admin/cores?action=reindex&query=EXCEPTIONMESSAGE:*
```

You must first run the query to see how many nodes are affected. If the result is large, you can add paging as part of the query in order to reindex in smaller batches.

```sql
<query> AND created:"2015-08"
```

Query based reindexing is also useful when changing the property type, changing tokenisation, adding new properties to be treated as identifiers, or when reindexing synonyms.

In a sharded setup, the reindex query will have to be run on all the nodes. The query will run for all shards on any node.
---
title: Solr sharding 
---

Solr sharding involves splitting a single Solr index into multiple parts, which may be on different machines. When the data is too large for one node, you can break it up and store it in sections by creating one or more shards, each containing a unique slice of the index.

Sharding is important for two primary reasons:

* It allows you to horizontally split or scale your content volume.
* It allows you to distribute operations, for example, index tracking, across shards (potentially on multiple nodes) therefore increasing performance/throughput.

Documents in the repository are distributed evenly across shards. You may have more than one shard, but a document will only be located in one shard and its instances. A conceptual shard can have any number of real instances. A shard tracks the appropriate subset of information from the repository.

> **Note:** Alfresco Content Services does not support slave shards or slave replicas.

A shard can have zero or more shard instances. Multiple shard instances have the following advantages:

* It provides high availability in case a shard/node fails.
* It allows you to scale out your search throughput because searches can be executed on all the instances in parallel.
* It increases performance: search requests are handled by the multiple shard instances.

Note that if your Solr indexes are sharded, then index backup will be disabled.

## Basic Solr sharding concepts

There are a few basic concepts that are core to understanding Solr sharding. Understanding these concepts from the outset will help in learning more about sharding.

### Useful terminology

|Term|Description|
|----|-----------|
|Node|A node represents an Alfresco Content Services instance.|
|Cluster|A cluster is composed of one or more Alfresco Content Services nodes.|
|Shard group|A shard group is a collection of documents. It is composed of one or more shards.|
|Shard|An index is split into chunks called shards.|

### Basic concepts

A cluster is a collection of one or more nodes (servers) that provide indexing and search capabilities across all nodes. A node is a single server that is part of your cluster, stores your data, and participates in the cluster's indexing and search capabilities.

An index is a collection of documents from the same store. An index can potentially store a large amount of data that can exceed the hardware limits of a single node. To solve this problem, Content Services provides the ability to subdivide your index into multiple pieces called shards.

When you create an index, you define the number of shards that you want. Each shard is in itself a fully-functional and independent Solr index that can be hosted on any index server. Index server includes a node which must be in the cluster. It is recommended to have a fail over mechanism in case a shard/node fails or goes offline. As a solution, you can make one or more copies of your index's shards into shard instances.

![]({% link insight-engine/images/solr_terms.png %})

To summarize, each index can be split into multiple shards. An index can also be replicated zero (meaning no instance) or more times. A shard tracks the appropriate subset of information from the repository. The number of copies of the total index depends on the minimum number of instances for each shard.

## Search and Insight Engine sharding methods

When an index grows too large to be stored on a single search server, it can be distributed across multiple search servers. This is known as sharding. The distributed/sharded index can then be searched using Alfresco/Solr's distributed search capabilities.

A specific configuration attribute, called `shard.method` defines the logic/strategy which controls how documents and ACLs are distributed across shards. Note this setting is configured in each Solr instance (i.e in each shard). So a shard will use that strategy for determining if the given incoming data belongs to it or not.

To use a specific sharding method, when creating a Solr node you must add the required configuration properties in `solrcore.properties`. The sharding method is set with the required property, `shard_method`. Additional properties may then be needed, depending on your chosen method. If an invalid `shard_method` is provided, then the system will fallback to DBID routing.

Search and Insight Engine can use any of the following methods for routing documents and ACLs to shards.

### ACL (MOD_ACL_ID) v1

This sharding method is available in all versions of Search and Insight Engine.

Nodes and access control lists are grouped by their ACL ID. This places the nodes together with all the access control information required to determine the access to a node in the same shard. Both the nodes and access control information are sharded. The overall index size will be smaller than other methods. Also, the ACL count is usually much smaller than the node count.

This method is beneficial if you have lots of ACLs and the documents are evenly distributed over those ACLs. For example, if you have many Share sites, nodes and ACLs are assigned to shards randomly based on the ACL and the documents to which it applies.

The node distribution may be uneven as it depends how many nodes share ACLs.
To use this method when creating a shard, set the following configuration:

```text
shard.method=MOD_ACL_ID
shard.instance=<shard.instance>
shard.count=<shard.count>
```

### ACL (ACL_ID) v2

This method is available in all versions of Search and Insight Engine.

This sharding method is the same as `ACL ID` v1 except that the murmur hash of the ACL ID is used in preference to its modulus. This gives better distribution of ACLs over shards. The distribution of documents over ACLs is not affected and so the shard sizes can still be skewed.

```text
shard.method=ACL_ID
shard.instance=<shard.instance>
shard.count=<shard.count>
```

### DBID (DB_ID)

This method is available in all versions of Search and Insight Engine and is the default sharding option in Solr 6. Nodes are evenly distributed over the shards at random based on the murmur hash of the DBID. The access control information is duplicated in each shard. The distribution of nodes over each shard is very even and shards grow at the same rate. Also, this is the fall back method if any other sharding information is unavailable.

To use this method when creating a shard, set the following configuration:

```text
shard.method=DB_ID
shard.instance=<shard.instance>
shard.count=<shard.count>
```

### DBID range (DB_ID_RANGE) {#sharding-methods-db-id-range}

This method is available in Search and Insight Engine 1.1 and later versions. This routes documents within specific DBID ranges to specific shards. It adds new shards to the cluster without requiring a reindex.

DBID range sharding is the only option to offer auto-scaling as opposed to defining your exact shard count at the start. All the other sharding methods require repartitioning in some way.

For each shard, you specify the range of DBIDs to be included. As your repository grows you can add shards. Note that when using `shard.range`, the range will be inclusive of the bottom value and exclusive of the top value.

**Example 1:** You may aim for shards of 20M nodes in size and expect it to get to 100M over five years. You could create the first shard for nodes 0-20M. As you approach node 20M, you can create the next shard for nodes 20M-40M, and so on.

To use this method when creating a shard, set the following configuration:

```text
shard.method=DB_ID_RANGE
shard.range=0-20000000
shard.instance=<shard.instance>
```

**Example 2:** If there are 100M (million) nodes and you want to split them into 10 shards with 10M nodes each. So, at the start you can specify:

* 10 shards
* a shard to include 0-10M
* the second shard will have 10M - 20M nodes, third shard will have 20M - 30M nodes, and so on.
    Date-based queries may produce results from only a subset of shards as DBID increases monotonically over time.

### Date/Datetime (DATE)

This method is available in all versions of Search and Insight Engine. The date-based sharding assigns dates sequentially through shards based on the month.

**Example:** If there are 12 shards, each month would be assigned sequentially to each shard, wrapping round and starting again for each year. The non-random assignment facilitates easier shard management - dropping shards or scaling out replication for some date range. Typical aging strategies could be based on the created date or destruction date.

If the property is not present on a node, sharding falls back to the DBID method to randomly distribute these nodes.

To use this method when creating a shard, set the following configuration:

```text
shard.key=exif:dateTimeOriginal
shard.method=DATE
shard.instance=<shard.instance>
shard.count=<shard.count>
```

Months can be grouped together, for example, by quarter. Each quarter of data would be assigned sequentially through the available shards.

```text
shard.date.grouping=3
```

### Metadata (PROPERTY)

This method is available in all versions of Search and Insight Engine. In this method, the value of some property is hashed and this hash is used to assign the node to a random shard. All nodes with the same property value will be assigned to the same shard

Only properties of type `d:text`, `d:date` and `d:datetime` can be used. For example, the recipient of an email, the creator of a node, some custom field set by a rule, or by the domain of an email recipient. The keys are randomly distributed over the shards using murmur hash.

If the property is not present on a node, sharding falls back to the DBID method to randomly distribute these nodes.

To use this method when creating a shard, set the following configuration:

```text
shard.key=cm:creator
shard.method=PROPERTY
shard.instance=<shard.instance>
shard.count=<shard.count>
```

It is possible to extract a part of the property value to use for sharding using a regular expression, for example, a year at the start of a string:

```text
shard.regex=^d{4}
```

If the regular expression doesn't match the property (e.g. the string doesn't start with a four-digit year) then this causes a fallback to DBID sharding.

### Explicit Sharding (EXPLICIT_ID)

This method is available in all versions of Search and Insight Engine. The node is assigned to a shard based on the value of a property (e.g. `cm:type`), which should contain the "explicit" numeric shard ID

This method is similar to sharding by metadata. Rather than hashing the property value, it explicitly defines the shard where the node should go. If the property is absent or an invalid number, sharding will fall back to using the `DBID` sharding method. Only text fields are supported. Nodes are allowed to move shards. You can add, remove or change the property that defines the shard.

To use this method when creating a shard, set the following configuration:

```text
shard.method=EXPLICIT_ID
shard.key=cm:targetShardInstance
shard.instance=<shard.instance>
shard.count=<shard.count>
```

> **Note:** The **ACL v1 (MOD_ACL_ID)** sharding method was the only method available in Solr4.

### Availability matrix

|Index Engine|ACL v1|DB ID|Date/time|Metadata|ACL v2|DBID range|Explicit|
|------------|------|-----|---------|--------|------|----------|--------|
|Content Services 5.2.0+ Solr 4| Y | N | N | N | N | N | N |
|Content Services 5.2.0+ Content Services 1.0| Y | Y | Y | Y | Y | N | N |
|Content Services 6.1+ Search Services or Search and Insight Engine 1.1 + 1.0| Y | Y | Y | Y | Y | Y | N |
|Content Services 6.1+ Search Services or Search and Insight Engine 1.2+| Y | Y | Y | Y | Y | Y | Y |

### Comparison Overview

|Index Engine|ACL v1|DB ID|Date/time|Metadata|ACL v2|DBID range|Explicit|
|------------|------|-----|---------|--------|------|----------|--------|
|All shards required| Y | Y | Y | Y | Y | N | Y |
|ACLs replicated on all shards| N | Y | Y | Y | N | Y | Y |
|Can add shards as the index grows| N | N | N | N | N | Y | N |
|Distribution of content over shards|Uneven|Very even|Quite even|Quite even|Quite even|Quite even|Quite even|
|Falls back to DBID sharding| N | N | Y | Y | N | N | Y |
|One shard gets new content| N | N |Possible|Possible| N | Y | N |
|Nodes can move shard| Y | N | Y | Y | Y | N | Y |

## Backing up Solr shards

To avoid any data loss, you can make backups of one or all the sharded Solr indexes.

Trigger a backup with an `HTTP` command which instructs the `/replication` handler to backup the Solr shards, for example:

```http
curl http://solrshard20xbm.alfresco.com:9000/solr/<CORE_NAME>/replication?command=backup&numberToKeep=1
```

where:

`<CORE_NAME>` specifies the name of the core you are working with.

`numberToKeep` specifies the number of backups to keep.

> **Note:** The `location` parameter used for previous versions is no longer accepted. To specify a backup folder, use the `solr.backup.dir` parameter in the `solrcore.properties` file.

### Backup status

The backup operation can be monitored to see if it has completed by sending the `details` command to the `/replication` handler, for example:

```http
http://solrshard20xbm.alfresco.com:9000/alfresco-search-backups/<CORE_NAME>/replication?command=details
```

## Best practices for setting up sharded Solr indexes

Use these best practices for setting up and using a sharded installation.

### Do I need sharding?

If you plan to store 50 million + documents in your repository, you should consider sharding to maximize indexing performance and to enable horizontal scaling to massive content repositories.

### Do I need dynamic shard registration?

You can set up sharding using either manual or dynamic shard registration. We recommend that you use dynamic shard registration because it is easier to implement than manual sharding.

### How many shards should I have?

A general rule of thumb is to divide the total number of documents by 50M (million). If you want to increase the query load or support more than 100 concurrent users, then check the memory specifications or the I/O specifications of the installation machine.

### What are the reindexing recommendations for a sharded installation

We recommend that existing customers should reindex using the `rerank` core. This has the following benefits:

* Smaller index
* Better query performance particularly for phrases and stop words
* Improved cross-language search

This should allow the user to store anywhere between 50 million - 80 million documents in a single shard. For more information, see the [AHow Alfresco powered a 1.2 Billion document deployment on Amazon Web Services](https://www.alfresco.com/blogs/power-platform/how-alfresco-powered-12-billion-document-deployment-amazon-web-services){:target="_blank"} and [Alfresco 1 billion documents press release with Amazon Aurora](https://www.alfresco.com/news/press-releases/alfresco-achieves-benchmarking-milestone-processing-1-billion-documents-amazon){:target="_blank"}.

> **Note:** Note that changing the number of shards requires a reindex.

### Does sharding work with SSL enabled?

Alfresco Content Services 6.x uses Search and Insight Engine (Solr 6), so sharding is supported with full SSL and non-SSL. Make sure you configure the Solr and SSL settings properly.

For more information, see [Installation options]({% link insight-engine/latest/install/options.md %}).

### Are there any considerations for query load and number of documents?

Before sharding your Solr index, it is important to consider your query load and the size of your repository. You need to create machines to host Solr. For more information, see [Configuring Search and Insight Engine]({% link insight-engine/latest/config/index.md %}). For example, if you need 5 shards, you need to setup those 5 machines, and have Solr instances running on all the 5 machines. Once your machines are ready, you are ready to set up or register shards.

For more information, see [Setting up Solr sharding]({% link insight-engine/latest/config/sharding/create.md %}#do-i-need-dynamic-shard-registration).

### After upgrading, can I use my current index while building a new sharded index?

Yes. After upgrading to Alfresco Content Services 6.2, continue to use the old search index server as before, setup a new sharded Solr server with the `rerank` template to reindex the data, and finally, switch over to the new sharded index once the indexing is done and the sharded Solr server is up-to-date.

#### Upgrading from 5.0 with Solr 4 to 6.2 (with zero downtime)

1. Upgrade to 6.2 and continue to use the Solr 4 search service as before.
2. Configure a separate sharded Solr 4 index to track the repository. For details, see [Solr Sharding](#solr-sharding). 
3. While the new sharded Solr 4 builds its indexes, you can monitor the progress using the Solr Admin Web interface. For details, see [Solr security]({% link insight-engine/latest/config/security.md %}.
4. When the sharded Solr 4 index is updated, enable the sharded Solr 4 index by setting the `solr.host` property.

### How do I know the new sharded index is up-to-date?

Go to the Solr Admin Web interface at `https://localhost:8443/solr/#/alfresco` and monitor the value of `Approx transactions remaining`. If the value is `0`, it indicates that the index up-to-date.

### Can different shards be inconsistent?

Yes. In a sharded setup, eventual consistency can introduce additional query inconsistencies.

A node can move between shards either by:

* Moving the node, or
* Adding a new access control list to a node that did not previously have any ACLs defined.

When this happens, the shards may index at different rates. It is possible to see:

* Two copies of the node if it is added to a new shard before it is deleted from the original shard.
* No node if it is deleted from the original shard before being added to a new shard.

Indexing is eventually consistent. When updates happen at the same time, no inconsistency is seen.
---
title: Overview
---

Installing Search and Insight Engine introduces additional features, including new sharding methods and sharding with SSL. Mutual TLS is not just used to encrypt data in transit, it is also used as an authentication mechanism between the repository and Search and Insight Engine.

It is possible to deploy Alfresco Content Services without mutual TLS between the repository and Search and Insight Engine, however this will expose internal APIs that give full access to the repository without authentication. In such a setup, it is critical to properly protect these APIs.

You may choose to secure Search and Insight Engine with SSL.

> **Note:** When choosing to secure Search and Insight Engine with SSL, be aware that there is a known issue when using Solr 6 where the SSL truststore and keystore passwords are visible as text in the Solr 6 process arguments. Alfresco recommends that you ensure the server running Solr 6 is security hardened and access is restricted to admin users only. For more information, see [Apache](https://issues.apache.org/jira/browse/SOLR-8897){:target="_blank"}.

> **Important:** Alfresco strongly recommends that you use firewalls and other infrastructure means to ensure that the Search and Insight Engine server is not accessible from anything other than trusted hosts and/or users, and only on the ports needed for Search and Insight Engine.

You can download the Search and Insight Engine installation file from [Hyland Community](https://community.hyland.com/products/alfresco){:target="_blank"}. Click **Product downloads**, and then select the version of the product you require.

## Prerequisites

The supported platforms are the combinations of operating systems, databases, and application servers that are tested and certified for Alfresco Content Services.

Before you install Search and Insight Engine you must install Alfresco Content Services 6.2 or later. You can install Search and Insight Engine using the distribution zip and Docker Compose, but the Docker Compose method of installation is only for development and test environments.

See [Supported platforms]({% link insight-engine/latest/support/index.md %}) for information about prerequisites and requirements.

## Solr overview

Alfresco Content Services supports use of the Solr search platform for searching within the repository.

Solr is an open source enterprise search platform that uses lucene as indexing and search engine. Solr is written in Java and runs as a standalone search server. Alfresco Content Services sends HTTP and XML input to Solr and searches for content. Solr updates the cores or indexes and returns the result of the query in XML or JSON format.

In all previous Alfresco Content Services versions, `Solr.war` was bundled with the repository. Starting from Alfresco Content Services 5.2.3, you no longer deploy a `Solr.war` to your application server. Alfresco Content Services 5.2 uses Solr 4 as the default search service index. Solr 6 is an independently executable standalone application powered by a Jetty server.  For improved and efficient search functionality, you can upgrade to Alfresco Content Services with Alfresco Search and Insight Engine (Solr 6).

There are two cores or indexes in Solr:

* **alfresco**: used for searching all live content stored at `<SOLR_HOME>/solrhome/alfresco` within the Solr search server.
* **archive**: used for searching content that has been marked as deleted at `<SOLR_HOME>/solrhome/archive` within the Solr search server.

![Solr overview]({% link insight-engine/images/solr.png %})

> **Important:** For security reasons, it is advised that you generate a new set of keys to secure your Solr communication and access to the Solr Admin Console.

For more information, see [Configuring using the Admin Console]({% link insight-engine/latest/config/index.md %}#configure-using-the-admin-console) and [Secure keys]({% link insight-engine/latest/config/keys.md %}).

## Eventual consistency

Alfresco Content Services 6.2 introduces the concept of eventual consistency to overcome the scalability limitations of in-transaction indexing.

Here's some background information on the evolution of eventual consistency in Alfresco:

* Alfresco Enterprise 3.x supported a transactional index of metadata using Apache Lucene.
* Alfresco Enterprise 4.0 introduced an eventually consistent index based on Apache Solr 1.4.
* Alfresco One 5.0 moved to Solr 4 and also introduced transaction metadata query (TMDQ). TMDQ was added specifically to support the transactional use cases that used to be addressed by the Lucene index in the previous versions. TMDQ uses the database and adds a collection of required indexes as optional patches.
* Alfresco One 5.1 supported a later version of Solr 4 and made improvements to TMDQ.
* Alfresco Content Services 5.2.x supports Solr 4, Solr 6, and TMDQ.
* Alfresco Content Services 6.x supports Solr 6, and TMDQ

When changes are made to the repository they are picked up by Solr via a polling mechanism. The required updates are made to the Index Engine to keep the two in sync. This takes some time. The Index Engine may well be in a state that reflects some previous version of the repository. It will eventually catch up and be consistent with the repository (assuming the repository is not constantly changing).

When a query is executed, it can happen in any one of the following ways:

* By default, if the query can be executed against the database, it will be.
* If not, the query goes to the Solr index.

There are some minor differences between the results. For example, collation and how permission are applied. Some queries are not supported by TMDQ, for example, facets, full text, in tree, and structure. If a query is not supported by TMDQ, it can only go to the Index Engine.

## What does eventual consistency mean?

If the Index Engine is up to date, a query against the database or the Index Engine will see the same state. The results may still be slightly different. If the index engine is behind the repository, the query may produce results that do not, as yet, reflect all the changes that have been made to the repository.

## Why the database and Index Engine may not be in sync

### Nodes may have been deleted

* Nodes are present in the index but deleted from the repository
  * Deleted nodes are filtered from the results when they are returned from the query. So, you may see a *short page* of results even though there are more results.
  * The result count may be lower than the facet counts.
  * Faceting will include the *to be deleted nodes* in the counts.

### Nodes may have been added

* Nodes have been added to the repository but are not yet in the index at all. These new nodes will not be found in the results or included in faceting.
* Nodes have been added to the repository but only the metadata is present in the index. These nodes cannot be found by the content.

### Nodes metadata has changed

* The index reflects out of date metadata.
  * Some out of date nodes may be in the results when they should not be.
  * Some out of date nodes may be missing from the results when they should not be.
  * Some nodes may be counted in the wrong facets due to out of date metadata.
  * Some nodes may be ordered using out of date metadata.

### Node content has changed

* The index reflects out of date content but the metadata is up to date.
  * Some out of date nodes may be in the results when they should not be.
  * Some out of date nodes may be missing from the results when they should not be.

### Node content and metadata has changed

* The index reflects the out of date metadata and content.
* The index reflects out of date content (the metadata is updated first).
  * Some out of date nodes may be in the results when they should not be.
  * Some out of date nodes may be missing from the results when they should not be.
  * Some nodes may be counted in facets due to out of date metadata.

### An update has been made to an ACL (adding an access control entry to a node)

* The old ACL is reflected in queries
  * Some out of date nodes may be in the results when they should not be.
  * Some out of date nodes may be missing from the results when they should not be.
  * The ACLs that are enforced may be out of date but are consistent with the repository state when the node was added to the index. The node and ACL may be out of date but permission for the content and metadata is consistent with this prior state. For nodes in the version index, they are assigned the ACL of the *live* node when the version was added to the index.

### A node may be continually updated

* It is possible that such a node may never appear in the index.
* By default, when the Index Engine tracks the repository, it only picks up changes that are older than one second. This is configurable. For example, if we are indexing node 27 in state 120, we only add information for node 27 if it is still in that state. If the node has moved on to state 236, we will skip node 27 until we have indexed state 236 (assuming it has not moved on again). This avoids pulling *later* information into the index which may have an updated ACE or present an overall view inconsistent with a repository state. An out-of-date state means we have older information in the index.

## Dealing with eventual consistency

Handling eventual consistency varies from one situation to another. If you need a transactional answer, the default behaviour will give you one, if it can. For some queries, it is not possible to get a transactional answer. If you are using Solr 6, the response from the Search public API will return some information to help. It will report the index state consistent with the query.

```json
"context": {
    "consistency": {
        "lastTxId": 18
    }
},
```

This can then be compared with the last transaction on the repository. If they are equal, the query was consistent. The repository state for each node is known when it is added to the index.

If your query goes to the Index Server and it is not up to date, it could be any of the reasons described [Why the database and Index Engine may not be in sync](#why-the-database-and-index-engine-may-not-be-in-sync).

Using the Index Engine based on Solr 6 gives better consistency for metadata updates. Some update operations that infrequently require many nodes to be updated are now done in the background. These are mostly `move` and `rename` operations that affect structure. So, a node is now renamed quickly. Any structural information that is consequently changed on all of its children is done afterwards.

Search and Insight Engine 1.0 also includes improved commit coordination and concurrency improvements. This reduces the time for the changes to be reflected in the index. Some of the delay also comes from the work that Solr does before an index goes live. This can be reduced by tuning. The cost is usually a query performance hit later.

For most use cases, eventual consistency is perfectly fine. For transactional use cases, TMDQ is the only solution unless the index and repository are in sync.
---
title: Installation options
---

You can install Search and Insight Engine using the distribution zip or Docker Compose. There are two different ways you can install the software, the first is with mutual TLS, and the second is without mutual TLS (HTTP with secret word in request header).

> **Important:** From version 2.0, you cannot install Search and Insight Engine without mutual TLS (plain HTTP) because it is no longer supported.

## Install with mutual TLS (zip)

Use this information to install Search and Insight Engine on the same machine as Alfresco Content Services with mutual TLS.

Mutual TLS is used for authentication between the Repository and Search and Insight Engine.

This task assumes you have:

* Installed Alfresco Content Services 6.2 or above, see [Supported platforms]({% link search-services/latest/support/index.md %}).
* Set the following properties in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file:

    ```text
    index.subsystem.name=solr6
    solr.secureComms=https
    solr.port=8983
    ```

> **Important:** Alfresco strongly recommends you use firewalls and other infrastructure means to ensure the Search and Insight Engine server is not accessible from anything other than trusted hosts and/or users, and only on the ports needed for Search and Insight Engine.

1. Download `alfresco-insight-engine-2.0.x.zip` from the [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2. Extract the Search and Insight Engine distribution.

    By default, the contents of `alfresco-insight-engine-2.0.x.zip` are decompressed in a root folder as `/alfresco-insight-engine`. See [Search and Insight Engine directory structure]({% link insight-engine/latest/config/index.md %}#search-and-insight-engine-directory-structure) for more details.

3. If you use several languages across your organization, you **must** enable cross-language search support in all fields. To do this update the `alfresco-insight-engine/solrhome/conf/shared.properties` file:

    ```bash
    alfresco.cross.locale.datatype.0={http://www.alfresco.org/model/dictionary/1.0}text
    alfresco.cross.locale.datatype.1={http://www.alfresco.org/model/dictionary/1.0}content
    alfresco.cross.locale.datatype.2={http://www.alfresco.org/model/dictionary/1.0}mltext
    ```

4. (Optional) Suggestion is disabled by default. To enable suggestion update the `alfresco-insight-engine/solrhome/conf/shared.properties` file.

    ```bash
    alfresco.suggestable.property.0={http://www.alfresco.org/model/content/1.0}name
    alfresco.suggestable.property.1={http://www.alfresco.org/model/content/1.0}title
    alfresco.suggestable.property.2={http://www.alfresco.org/model/content/1.0}description
    alfresco.suggestable.property.3={http://www.alfresco.org/model/content/1.0}content
    ```

    > **Note:** The spell check functionality does not work with Search and Insight Engine when suggestion is enabled.

5. To secure access to Search and Insight Engine, you must create a new set of keystores and keys.

    1. Generate secure keys specific to your Alfresco installation. For more information, see [Secure keys]({% link insight-engine/latest/config/keys.md %}#generate-secure-keys-for-ssl-communication).

    2. Create a new keystore directory at `alfresco-insight-engine/solrhome`.

    3. In the production environment, copy your custom keystore and truststore to the `alfresco-insight-engine/solrhome/keystore` directory.

    4. Update the SSL-related system properties by replacing `<SOLR_HOME> with alfresco-insight-engine/solrhome`, and set your keystore and truststore passwords.

        (Windows) update the `alfresco-insight-engine/solr.in.cmd` file:

        ```bash
        set SOLR_SSL_KEY_STORE=<SOLR_HOME>/keystore/ssl-repo-client.keystore
        set SOLR_SSL_KEY_STORE_PASSWORD=keystore
        set SOLR_SSL_KEY_STORE_TYPE=JCEKS
        set SOLR_SSL_TRUST_STORE=<SOLR_HOME>/keystore/ssl-repo-client.truststore
        set SOLR_SSL_TRUST_STORE_PASSWORD=truststore
        set SOLR_SSL_TRUST_STORE_TYPE=JCEKS
        set SOLR_SSL_NEED_CLIENT_AUTH=true
        set SOLR_SSL_WANT_CLIENT_AUTH=false
        ```

        (Linux) update the `alfresco-insight-engine/solr.in.sh` file:

        ```bash
        SOLR_SSL_KEY_STORE=<SOLR_HOME>/keystore/ssl-repo-client.keystore
        SOLR_SSL_KEY_STORE_PASSWORD=keystore
        SOLR_SSL_KEY_STORE_TYPE=JCEKS
        SOLR_SSL_TRUST_STORE=<SOLR_HOME>/keystore/ssl-repo-client.truststore
        SOLR_SSL_TRUST_STORE_PASSWORD=truststore
        SOLR_SSL_TRUST_STORE_TYPE=JCEKS
        SOLR_SSL_NEED_CLIENT_AUTH=true
        SOLR_SSL_WANT_CLIENT_AUTH=false
        ```

    5. Set the `SOLR_PORT` environment variable:

        (Windows) update the `alfresco-insight-engine/solr.in.cmd` file:

        ```bash
        set SOLR_PORT=8983
        ```

        (Linux) update the `alfresco-insight-engine/solr.in.sh` file:

        ```bash
        SOLR_PORT=8983
        ```

6. (Optional) If you want to install Search and Insight Engine on a separate machine, set the `SOLR_SOLR_HOST` and `SOLR_ALFRESCO_HOST` environment variables before starting Search and Insight Engine, for more see [Configuring Search and Insight Engine]({% link insight-engine/latest/config/index.md %}#search-and-insight-engine-externalized-configuration).

    (Windows) update the `alfresco-insight-engine/solr.in.cmd` file:

    ```bash
    set SOLR_SOLR_HOST=localhost
    ```

    ```bash
    set SOLR_ALFRESCO_HOST=localhost
    ```

    (Linux) update the `alfresco-insight-engine/solr.in.sh` file:

    ```bash
    SOLR_SOLR_HOST=localhost
    ```

    ```bash
    SOLR_ALFRESCO_HOST=localhost
    ```

7. To configure the Solr6 cores, set the following:

    * Before creating the alfresco and archive cores:
        * Set `alfresco.secureComms=https` in `alfresco-insight-engine/solrhome/templates/rerank/conf/solrcore.properties`.
        * Copy the custom keystores to the `alfresco-insight-engine/solrhome/keystore` directory.

            ```bash
            ssl-repo-client.keystore
            ssl-repo-client.truststore
            ```

    * If the alfresco and archive cores already exist, ensure that `alfresco.secureComms` is set to `https` for both the cores. For example:
        * `alfresco-insight-engine/solrhome/alfresco/conf/solrcore.properties`
        * `alfresco-insight-engine/solrhome/archive/conf/solrcore.properties`
8. For running a single instance of Search and Insight Engine (i.e. not sharded), use the following commands:

    ```bash
    cd alfresco-insight-engine
    ./solr/bin/solr start -a
    "-Dcreate.alfresco.defaults=alfresco,archive
    -Dsolr.ssl.checkPeerName=false
    -Dsolr.allow.unsafe.resourceloading=true
    -Dssl-keystore.password=keystore
    -Dssl-keystore.aliases=ssl-alfresco-ca,ssl-repo-client
    -Dssl-keystore.ssl-alfresco-ca.password=keystore
    -Dssl-keystore.ssl-repo-client.password=keystore
    -Dssl-truststore.password=truststore
    -Dssl-truststore.aliases=ssl-alfresco-ca,ssl-repo,ssl-repo-client
    -Dssl-truststore.ssl-alfresco-ca.password=truststore
    -Dssl-truststore.ssl-repo.password=truststore
    -Dssl-truststore.ssl-repo-client.password=truststore" -f
    ```

    > **Note:** The `-Dcreate.alfresco.defaults=alfresco,archive` command automatically creates the `alfresco` and `archive` cores. Therefore, you should only start Search and Insight Engine with `-Dcreate.alfresco.defaults=alfresco,archive` the first time you run Search and Insight Engine. Additionally, to ensure that Search and Insight Engine connects using the IPv6 protocol instead of IPv4, add `-Djava.net.preferIPv6Addresses=true` to the startup parameters. FInally, You should run this application as a dedicated user. For example, you can create a Solr user.

    The default port used is 8983.

    The command line parameter, `-a` passes additional JVM parameters, for example, system properties using `-D`.

    Once Search and Insight Engine is up and running, you should see a message like:

    ```text
    Waiting up to 180 seconds to see Solr running on port 8983 []  
    Started Solr server on port 8983 (pid=24289). Happy searching!
    ```

    To stop all instances of Search and Insight Engine, use:

    ```bash
    ./solr/bin/solr stop
    ```

    The logs are stored in the `alfresco-insight-engine/logs/solr.log` file, by default. This can be configured in `solr.in.sh` (for Linux) or `solr.in.cmd` (for Windows) using `SOLR_LOGS_DIR`.

    You have successfully created an `alfresco` core and an `archive` core. To verify, in a browser, navigate to the Solr URL, [https://localhost:8983/solr](https://localhost:8983/solr).

    > **Note:** You need to install the browser.p12 certificate in your browser before accessing this URL.

    In the Solr Admin UI, select the core selector drop-down list and verify that both the `alfresco` and `archive` cores are present.

    Allow a few minutes for Search and Insight Engine to start indexing.

If you are not using sharded Search and Insight Engine:

1. Access the **Admin Console > Search Service Sharding** page.
2. Deselect **Dynamic Shard Instance Registration**.
3. Select **Purge at Startup**.

## Install without mutual TLS - HTTP with secret word (zip)

Use this information to install Search and Insight Engine on the same machine as Alfresco Content Services without mutual TLS, using HTTP with a secret word in the request header. This means communication between the Repository and Search and Insight Engine is protected by a shared secret that is passed in a configurable request HTTP header.

**Important:** This installation method is only supported when using Content Services 7.1 and above.

This task assumes you have:

* Installed Alfresco Content Services 7.1 or above, see [Supported platforms]({% link search-services/latest/support/index.md %}).
* Set the following properties in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file:

    ```text
    index.subsystem.name=solr6
    solr.secureComms=secret
    solr.sharedSecret=password    
    solr.port.ssl=8983
    ```

> **Important:** To ensure the security of your system specify your own custom secret word for the `solr.sharedSecret` property, than the one provided in the example.

1. Download `alfresco-insight-engine-2.0.x.zip` from the [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2. Extract the Search and Insight Engine distribution.

    By default, the contents of `alfresco-insight-engine-2.0.x.zip` are decompressed in a root folder as `/alfresco-search-services`. See [Search and Insight Engine directory structure]({% link insight-engine/latest/config/index.md %}#search-and-search-services-directory-structure) for more details.

3. Configure HTTP.

    1. Open `solrhome/templates/rerank/conf/solrcore.properties`.

    2. Replace `alfresco.secureComms=https` with:

        ```bash
        alfresco.secureComms=secret
        alfresco.secureComms.secret=password
        ```

        This ensures that the Solr cores are created in plain HTTP mode with the shared secret communication method. The property `alfresco.secureComms.secret` includes the same word used in the `solr.sharedSecret` property in the Repository configuration.

        Alternatively, you can add this configuration in the system properties (using `-D`) when starting Solr. This alternative is safer because the shared secret is not stored in the filesystem. For example, add the following to the startup parameters in step **7**.

        ```bash
        -Dalfresco.secureComms=secret
        -Dalfresco.secureComms.secret=password
        ```

4. If you use several languages across your organization, you **must** enable cross-language search support in all fields. To do this add the following to the `alfresco-search-services/solrhome/conf/shared.properties` file:

    ```bash
    alfresco.cross.locale.datatype.0={http://www.alfresco.org/model/dictionary/1.0}text
    alfresco.cross.locale.datatype.1={http://www.alfresco.org/model/dictionary/1.0}content
    alfresco.cross.locale.datatype.2={http://www.alfresco.org/model/dictionary/1.0}mltext
    ```

5. (Optional) Suggestion is disabled by default. To enable suggestion update the `alfresco-search-services/solrhome/conf/shared.properties` file.

    ```bash
    alfresco.suggestable.property.0={http://www.alfresco.org/model/content/1.0}name
    alfresco.suggestable.property.1={http://www.alfresco.org/model/content/1.0}title
    alfresco.suggestable.property.2={http://www.alfresco.org/model/content/1.0}description
    alfresco.suggestable.property.3={http://www.alfresco.org/model/content/1.0}content
    ```

    > **Note:** The spell check functionality works with Search and Insight Engine when suggestion is enabled.

6. (Optional) If you want to install Search and Insight Engine on a separate machine, set the `SOLR_SOLR_HOST` and `SOLR_ALFRESCO_HOST` environment variables before starting Search and Insight Engine, for more see [Configuring Search and Insight Engine]({% link search-services/latest/config/index.md %}#search-services-externalized-configuration).

    (Windows) update the `alfresco-search-services`/`solr.in.cmd` file:

    ```bash
    set SOLR_SOLR_HOST=localhost
    ```

    ```bash
    set SOLR_ALFRESCO_HOST=localhost
    ```

    (Linux) update the alfresco-search-services/solr.in.sh file:

    ```bash
    SOLR_SOLR_HOST=localhost
    ```

    ```bash
    SOLR_ALFRESCO_HOST=localhost
    ```

7. To start Search and Insight Engine with all the default settings, use the following command:

    ```bash
    ./solr/bin/solr start -a "-Dcreate.alfresco.defaults=alfresco,archive"
    ```

    The command line parameter, `-a` passes additional JVM parameters, for example, system properties using `-D`.

    > **Note:** The `-Dcreate.alfresco.defaults=alfresco,archive` command automatically creates the `alfresco` and `archive` cores. Therefore, you should only start Search and Insight Engine with `-Dcreate.alfresco.defaults=alfresco,archive` the first time you run Search and Insight Engine. In addition you should run this application as a dedicated user. For example, you can create a Solr user. Finally, to ensure that Search and Insight Engine connects using the IPv6 protocol instead of IPv4, add `-Djava.net.preferIPv6Addresses=true` to the startup parameters.

    Once Search and Insight Engine is up and running, you should see a message similar to the following:

    ```bash
    Waiting up to 180 seconds to see Solr running on port 8983 []
    Started Solr server on port 8983 (pid=24289). Happy searching!
    ```

    To stop the currently running Search and Insight Engine instance, use:

    ```bash
    ./solr/bin/solr stop
    ```

    The logs are stored in the `alfresco-search-services/logs/solr.log` file, by default. This can be configured in `solr.in.sh` (for Linux) or `solr.in.cmd` (for Windows) using `SOLR_LOGS_DIR`.

    You have successfully created an `alfresco` core and an `archive` core. To verify, in a browser, navigate to the Solr URL, [http://localhost:8983/solr](http://localhost:8983/solr). In the Solr Admin UI, select the core selector drop-down list and verify that both the `alfresco` and `archive` cores are present.

    Allow a few minutes for Search and Insight Engine to start indexing.

8. Go to **Admin Console > Repository Services > Search Service** and verify that:

    1. You see the Solr 6 option in the **Search Service In Use** list.

    2. Under **Main (Workspace) Store Tracking Status**, the **Approx Transactions to Index** is **0**.

## Install with Docker Compose

Use this information to start up Alfresco Content Services 6.2 or above and Search and Insight Engine 2.0 using Docker Compose. Due to the limited capabilities of Docker Compose, this deployment method is recommended for development and test environments only.

### Prerequisites

* [Docker](https://docs.docker.com/install/){:target="_blank"}
  * This allows you to run Docker images and Docker Compose on a single computer.

* [Docker Compose](https://docs.docker.com/compose/install/){:target="_blank"}
  * Docker Compose is included as part of some Docker installers. If it's not part of your installation, then install it separately after you've installed Docker.

* Access to [Quay](https://quay.io/){:target="_blank"}
  * Docker requires access to certain images which are stored on Quay. You need to use the correct credentials provided by Alfresco to access these images. Contact [Alfresco Support](mailto:support@alfresco.com){:target="_blank"} to request the credentials.

> **Note:** Make sure the following ports are free on your computer: `5432`, `8080`. These ports are set in the `docker-compose.yml` file.

### Deployment steps

1. Download the latest Alfresco Content Services `docker-compose.yml` file by accessing the [Download Trial](https://www.hyland.com/en/resources/alfresco-ecm-download){:target="_blank"} page.

2. Save the file in a local folder.

3. Edit the file and change the `Solr 6` service. 

4. Add a `#` prefix to Alfresco Search and Insight Engine so it is commented out, and add the Alfresco Search and Insight Engine image location:

    ```yaml
        solr6:
            #image: alfresco/alfresco-search-services:2.0.x
            image: quay.io/alfresco/insight-engine:2.0.x
            ...
    ```

    > **Note:** If you want to use the Apache Zeppelin visualization interface with Search and Insight Engine you have to deploy it using Docker Compose along with Alfresco Content Services, you cannot install it manually. See [Building Reports and Dashboards]({% link insight-engine/latest/using/index.md %}#Installing with Docker Compose) for the additional container information you need to add to your `docker-compose.yml` file.

5. Save the file.

6. Log in to Quay using the following command:

    ```yaml
    $ docker login quay.io
                login against server at https://quay.io/v1/
                Username: <<Quay.io Credential Username>>
                Password: <<Quay.io Credential Password>>
    ```

7. Change directory to the location of the `docker-compose.yml` file and deploy Alfresco Content Services and Search and Insight Engine using the following command:

    ```bash
    docker-compose up
    ```

    This downloads the images, fetches all the dependencies, creates each container, and then starts the system. If you downloaded the project and changes were made to the project settings, any new images will be pulled from Quay before the system starts.

8. Wait for the logs to complete.

    If you encounter errors while the system is starting up:

    * Stop the session (by using `CONTROL+C`).
    * Remove the container (using the `--rmi all` option): For example `docker-compose down --rmi all`.
    * Try allocating more memory resources. As advised in `docker-compose.yml` set it to at least 16 GB. To adjust the memory, in Docker, go to **Preferences** (or **Settings**) > **Advanced** > **Memory**. Once you have adjusted the memory make sure you restart Docker and wait for the process to finish before continuing.
    * Go back to step 7 and retry the deployment.

9. Open your browser and check everything starts up correctly:

    * Alfresco: `http://localhost:8080/alfresco`
    * Share: `http://localhost:8080/share`
    * Solr: `http://localhost:8083/solr`

        > **Note:** When you access the solr url you will see the version of Search and Insight Engine that is installed.
---
title: Supported platforms
---

The following are the supported platforms for Search and Insight Engine:

| Version | Notes |
| ------- | ----- |
| Content Services 23.x | Requires Alfresco Search Services 2.0.8 and later |
| Content Services 7.4.x | |
| Content Services 7.3.x | |
| Content Services 7.2.x | |
| Content Services 7.1.x | |
| Content Services 7.0.x | |
| Content Services 6.2.x | |

> **Note:** Search and Insight Engine 2.0 is compatible with Java 11 as long as you run Zeppelin in a Java 8 runtime. You can do this either in a VM or separate Java 8 based server. Java 11.0.9.1 and other four part Java versions are not compatible with versions 2.0.2 and below due to a bug in Jetty. This issue is resolved in version 2.0.3.
---
title: Upgrade Search and Insight Engine
---

Use this information to upgrade from Search and Insight Engine 1.x to Search and Insight Engine 2.0.

> **Note:** A reindex is required when you upgrade from Search and Insight Engine 1.x to Search and Insight Engine 2.0. `solr.content.dir` is no longer used from Search and Insight Engine 2.0 and above. Solr itself provides that storage facility which means it can be safely removed, which we recommend, for more see [Search and Insight Engine externalized configuration]({% link insight-engine/latest/config/index.md %}#search-and-insight-engine-externalized-configuration). If it is necessary for you to have a backup of the old index and content store then it must be copied elsewhere before you reindex.

1. Stop Search and Insight Engine.

    ```bash
    ./solr/bin/solr stop
    ```

2. Backup or move the existing alfresco-insight-engine folder to a preferred location. For example, `alfresco-insight-engine-1.x`.

3. Browse to [Hyland Community](https://community.hyland.com/){:target="_blank"}.

4. Download and unzip the Search and Insight Engine distribution zip file to a preferred location:

    **alfresco-insight-engine-distribution-2.0.x.zip**

    By default, the contents are decompressed in a folder at `./alfresco-insight-engine`. The folder extracts into the same location as the zip file.

5. Start Search and Insight Engine 2.0.

    If the indexes for Solr are in another location (where you saved them in step 2), use the following commands to point Solr to the right location:

    Unix like systems

    ```bash
    ./solr/bin/solr start -a "-Dcreate.alfresco.defaults=alfresco,archive" -p <port>
    -Dsolr.model.dir=/your-preferred-location/solrhome/alfrescoModels
    -Ddata.dir.root=/your-preferred-location/solrhome/
    ```

    Microsoft Windows

    ```bash
    solr start -a "-Dcreate.alfresco.defaults=alfresco,archive" -p <port>
    -Dsolr.model.dir="your-preferred-locationsolrhomealfrescoModels"
    -Ddata.dir.root="your-preferred-locationsolrhome"
    ```

    > **Note:** To check what version of Search Services or Search and Insight Engine you have installed go to `http://localhost:8983/solr/`.
---
title: Migrate Search Services 
---

Use this information to migrate from Search Services to Search and Insight Engine using the distribution zip or docker compose, including how to migrate Search and Insight Engine to Search Services.

> **Note:** You can only migrate to Search Services using the distribution zip.

## Migrate with zip

You can migrate from Alfresco Content Services 6.2 or above with Search Services 1.3 or above to Alfresco Content Services with Search and Insight Engine 2.0. You can also migrate from Alfresco Content Services 5.x with Search Services 1.3 or below to Alfresco Content Services 6.2 or above with Search and Insight Engine 2.0.

* [Migrate Content Services 6.2 with Search Services 1.3 or above](#migrate-content-services-62-with-search-services-13-or-above)
* [Migrate Content Services 5.x with Search Services 1.3 or below](#migrate-content-services-5x-with-search-services-13-or-below)  

### Migrate Content Services 6.2 with Search Services 1.3 or above

Use this information to migrate from Alfresco Search Services 1.3 or above to Search and Insight Engine 2.0 using a distribution zip.

> **Note:** A reindex is required when you migrate from Search Services to Search and Insight Engine. `solr.content.dir` is no longer used from Search and Insight Engine 2.0 and above. Solr itself provides that storage facility which means it can be safely removed, which we recommend, for more see [Search and Insight Engine externalized configuration]({% link insight-engine/latest/config/index.md %}#search-and-insight-engine-externalized-configuration). If it is necessary for you to have a backup of the old index and content store then it must be copied elsewhere before you reindex.

1. Stop Search Services.

    ```bash
    ./solr/bin/solr stop
    ```

2. Backup or move the existing `alfresco-search-services` folder to a preferred location. For example, `alfresco-search-services-1.x`.

3. Browse to [Hyland Community](https://community.hyland.com/){:target="_blank"}.

4. Download and unzip the Search and Insight Engine distribution zip file to a preferred location:

    ```bash
    alfresco-insight-engine-distribution-2.0.x.zip
    ```

    By default, the contents are decompressed in a folder at `./alfresco-insight-engine`. The folder extracts into the same location as the zip file.

5. Your indexes for Solr are in another location, use the following commands to point Solr to the right location:

    Unix like systems

    ```bash
    ./solr/bin/solr start -a "-Dcreate.alfresco.defaults=alfresco,archive" -p <port>
    -Dsolr.model.dir=/your-preferred-location/solrhome/alfrescoModels
    -Ddata.dir.root=/your-preferred-location/solrhome/
    ```

    Microsoft Windows

    ```bash
    solr start -a "-Dcreate.alfresco.defaults=alfresco,archive" -p <port>
    -Dsolr.model.dir="your-preferred-locationsolrhomealfrescoModels"
    -Ddata.dir.root="your-preferred-locationsolrhome"
    ```

6. (Optional) If you have changed the `alfresco-search-services/solr.in.sh` or `alfresco-search-services/solr.in.cmd` file, you must restore it from your backup.

7. Start Search and Insight Engine.

    > **Note:** To check what version of Search Services or Search and Insight Engine you have installed go to `http://localhost:8983/solr/`.

### Migrate Content Services 5.x with Search Services 1.3 or below

There are two steps to migrating your installation from Alfresco Content Services 5.x with Alfresco Search Services to Alfresco Content Services 6.2 with  Search and Insight Engine. First you need to upgrade to Alfresco Content Services 6.2 with Search Services, and then migrate Search Services to Search and Insight Engine.

> **Note:** You can't upgrade Alfresco Content Services 5.x using Docker Compose.

1. Upgrade from Alfresco Content Services 5.x to Alfresco Content Services 6.2, for more see [Migrate Solr 4 to Solr 6]{% link search-services/latest/upgrade/migrate.md %}).

    > **Note:** You can't do this using Docker Compose.

2. Migrate from Search Services to Search and Insight Engine see [Migrate Content Services 6.2 with Search Services 1.3 or above](#migrate-content-services-62-with-search-services-13-or-above).

## Migrate using Docker Compose

If you already have Alfresco Content Services 6.2 with Alfresco Search Services 1.3, 1.4, or 2.0 installed, you can migrate to Search and Insight Engine 2.0. Due to the limited capabilities of Docker Compose, this migration method is recommended for development and test environments only.

Use this information to migrate from Search Services to Search and Insight Engine using Docker Compose.

> **Note:** A reindex is required when you migrate from Search Services to Search and Insight Engine. `solr.content.dir` is no longer used from Search and Insight Engine 2.0 and above. Solr itself provides that storage facility which means it can be safely removed, which we recommend, for more see [Search and Insight Engine externalized configuration]({% link insight-engine/latest/config/index.md %}#search-and-insight-engine-externalized-configuration). If it is necessary for you to have a backup of the old index and content store then it must be copied elsewhere before you reindex.

1. Insert the following container information into your `docker-compose.yml` file and save it.

    ```yaml
        solr6:
            #image: alfresco/alfresco-search-services:2.0.x (or 1.4, and 1.3)
            image: quay.io/alfresco/insight-engine:2.0.x
            mem_limit: 2500m
            environment:
                #Solr needs to know how to register itself with Alfresco
                    - SOLR_ALFRESCO_HOST=alfresco
                    - SOLR_ALFRESCO_PORT=8080
                #Alfresco needs to know how to call solr
                    - SOLR_SOLR_HOST=solr6
                    - SOLR_SOLR_PORT=8983
                #Create the default alfresco and archive cores
                    - SOLR_CREATE_ALFRESCO_DEFAULTS=alfresco,archive
                    - "SOLR_JAVA_MEM=-Xms2g -Xmx2g"
            ports:
                - 8083:8983 #Browser port
    ```

2. Use the following command to run the file and upgrade your Alfresco Content Services 6.2 installation:

    ```dockerfile
    docker-compose up

## Migrate to Search Services

Use this information to migrate from Search and Insight Engine 2.0 to Alfresco Search Services 2.0 using a distribution zip.

> **Note:** A reindex is required when you migrate from Search and Insight Engine to Search Services. `solr.content.dir` is no longer used from Search and Insight Engine 2.0 and above. Solr itself provides that storage facility which means it can be safely removed, which we recommend, for more see [Search and Insight Engine externalized configuration]({% link insight-engine/latest/config/index.md %}#search-and-insight-engine-externalized-configuration). If it is necessary for you to have a backup of the old index and content store then it must be copied elsewhere before you reindex.

1. Stop Search and Insight Engine.

    ```bash
    ./solr/bin/solr stop
    ```

2. Backup or move the existing `./alfresco-insight-engine` folder to a preferred location. For example, `alfresco-insight-engine-2.0`.

3. Browse to [Hyland Community](https://community.hyland.com/){:target="_blank"}.

4. Download and unzip the Search Services distribution zip file to a preferred location:

    ```bash
    alfresco-search-services-distribution-2.0.x.zip
    ```

    By default, the contents are decompressed in a folder at `./alfresco-search-services`. The folder extracts into the same location as the zip file.

5. (Optional) If you have changed the `alfresco-search-services/solr.in.sh` or `alfresco-search-services/solr.in.cmd` file, you must restore it from your backup.

6. Your indexes for Solr are in another location (where you saved them in step 2), use the following commands to point Solr to the right location:

    Unix like systems

    ```bash
    ./solr/bin/solr start -a "-Dcreate.alfresco.defaults=alfresco,archive" -p <port>
    -Dsolr.model.dir=/your-preferred-location/solrhome/alfrescoModels
    -Ddata.dir.root=/your-preferred-location/solrhome/
    ```

    Microsoft Windows

    ```bash
    solr start -a "-Dcreate.alfresco.defaults=alfresco,archive" -p <port>
    -Dsolr.model.dir="your-preferred-locationsolrhomealfrescoModels"
    -Ddata.dir.root="your-preferred-locationsolrhome"
    ```

7. Start Search Services.

    > **Note:** To check what version of Search Services or Search and Insight Engine you have installed go to `http://localhost:8983/solr/`.
---
title: Building reports and dashboards
---

Search and Insight Engine comes with a number of out-of-the box reports and a dashboard builder with pre-configured reports based on Insight Zeppelin. Insight Zeppelin is a web-based notebook that enables data-driven, interactive data analytics, data visualization, and collaborative documents using SQL.

To use the reports and dashboard builder, you need to install Insight Zeppelin.

> **Note:** For this version of Search and Insight Engine, cluster mode is not supported.

Use `http://localhost:9090/zeppelin` to access Insight Zeppelin user interface.

For information on Insight Zeppelin user Interface see [Explore Apache Zeppelin UI](https://zeppelin.apache.org/docs/0.8.1/quickstart/explore_ui.html){:target="_blank"}.

## Installation options

There are several options for installing Insight Zeppelin:

* [Installing with a distribution zip](#installing-with-a-distribution-zip).
* [Installing with Docker Compose](#installing-with-docker-compose).

> **Note** You do not need to install Insight Zeppelin in order to use Search and Insight Engine.

## Install with a distribution zip

Use this information to manually install Insight Zeppelin using a distribution zip.

1. Download the `alfresco-insight-zeppelin-2.0.x.zip` file from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2. Unzip the file.

3. Run the following script:

    On Unix-like systems: `ZEPPELIN_HOME/bin/substituter.sh`

    On Microsoft Windows: `ZEPPELIN_HOME/bin/substituter.cmd`

    This script reads the `zeppelin.properties` file in ZEPPELIN_HOME. Use the `zeppelin.properties` file to change the Alfresco Content Services repository connection details.

    Alternatively, you can pass `REPO_PROTOCOL`, `REPO_HOST`, and `REPO_PORT` to the script from the command line. For example, `REPO_PROTOCOL=https REPO_HOST=myhost REPO_PORT=8443./substituter.sh`. You don't have to pass all the variables just the ones you want to override. The default values are: `REPO_PROTOCOL=http, REPO_HOST=localhost, and REPO_PORT=8080`. The port number, context path or other properties can be changed in `ZEPPELIN_HOME/conf/zeppelin-env.sh` on Unix like systems (or `ZEPPELIN_HOMEconfzeppelin-env.cmd` for Microsoft Windows). See [Apache Zeppelin Configuration](https://zeppelin.apache.org/docs/0.7.3/install/configuration.html){:target="_blank"} for a full list of properties.

4. To start the Insight Zeppelin Server, run:

    On Unix like systems: `ZEPPELIN_HOME/bin/zeppelin-daemon.sh`

    On Microsoft Windows: `ZEPPELIN_HOMEbinzeppelin.cmd`

5. Open the user interface using:

    `http://localhost:9090/zeppelin`

6. Log in with your Alfresco Content Services credentials.

7. Create a new notebook or use the one provided.

8. To stop Insight Zeppelin, run:

    On Unix-like systems: `ZEPPELIN_HOME/bin/zeppelin-daemon.sh`

    On Microsoft Windows: Ctrl + C

By default Insight Zeppelin uses Alfresco Content Services to authenticate users, which means every user in Alfresco Content Services will be able to access Zeppelin. To limit the number of users, comment out all the `alfrescoRealm` related configuration settings in `ZEPPELIN_HOME/conf/shiro.ini`. You can configure your LDAP or AD to allow specific users access to Insight Zeppelin.

See the following configuration example showing that only users in the `ZeppelinUsers` group have access to the application.

```bash
ldapRealm = org.apache.zeppelin.realm.LdapRealm
ldapRealm.contextFactory.systemUsername = <principal>
ldapRealm.contextFactory.systemPassword = <password>
ldapRealm.searchBase = OU=Users,DC=test,DC=com
ldapRealm.userSearchFilter = (&(objectclass=person)(sAMAccountName={0})(memberOf:=CN=ZeppelinUsers,OU=Users,DC=test,DC=com))
ldapRealm.userSearchScope = subtree
ldapRealm.authorizationEnabled = true
ldapRealm.contextFactory.url = <ldap-url>
ldapRealm.userSearchAttributeName = sAMAccountName
ldapRealm.contextFactory.authenticationMechanism = simple
ldapRealm.userObjectClass = person
ldapRealm.groupObjectClass = group
ldapRealm.memberAttribute = member
securityManager.realms=$ldapRealm
```

### SSL encryption

Ideally Insight Zeppelin is deployed on a separate server. If Insight Zeppelin is using SSL to communicate with Alfresco Content Services you must add the following settings to each Interpreter configured with Insight Zeppelin:

```bash
alfresco.enable.ssl=true
alfresco.ssl.checkPeerName=false (If using Self Signed certificates)
javax.net.ssl.keyStoreType=JCEKS
javax.net.ssl.keyStore=../keystore/ssl.repo.client.keystore
javax.net.ssl.keyStorePassword=kT9X6oe68t
javax.net.ssl.trustStoreType=JCEKS
javax.net.ssl.trustStore=../keystore/ssl.repo.client.truststore
javax.net.ssl.trustStorePassword=kT9X6oe68t
```

Alternatively you can add the settings directly to the following JSON file: `ZEPPELIN_HOME/conf/interpreter.json`:

```json
"alfresco.enable.ssl": {
  "value": "true",
  "type": "string"
},
"solr.ssl.checkPeerName": {
  "value": "false",
  "type": "string"
},
"javax.net.ssl.keyStore": {
  "value": "/zeppelin/keystore/ssl.repo.client.keystore",
  "type": "string"
},
"javax.net.ssl.keyStorePassword": {
  "value": "kT9X6oe68t",
  "type": "string"
},
"javax.net.ssl.keyStoreType": {
  "value": "JCEKS",
  "type": "string"
},
"javax.net.ssl.trustStore": {
  "value": "/zeppelin/keystore/ssl.repo.client.truststore",
  "type": "string"
},
"javax.net.ssl.trustStorePassword": {
  "value": "kT9X6oe68t",
  "type": "string"
},
"javax.net.ssl.trustStoreType": {
  "value": "JCEKS",
  "type": "string"
}
```

Also, if the domain name of the Alfresco Content Services repository does not match the common name (CN) of the repository's SSL certificate, set the `solr.ssl.checkPeerName` property to `false`.

## Install with Docker Compose

You can deploy Insight Zeppelin by inserting the container details into the same Docker Compose file that you use for deploying Alfresco Content Services 6.2 and Search and Insight Engine.

For details about deployment using the Docker Compose file, see [Installation options]({% link insight-engine/latest/install/options.md %}#installing-with-docker-compose).

1. Open your `docker-compose.yml` file, and insert the following container information:

    ```YAML
    zeppelin:
        image: quay.io/alfresco/insight-zeppelin:2.0.x
        environment:
                - REPO_HOST=alfresco
                - REPO_PORT=8080
        ports:
        - “9090:9090”
    ```

2. Save the file.

3. Run Insight Zeppelin using `http://localhost:9090/zeppelin`.

## Create reports and dashboards

Insight Zeppelin lets you create reports using SQL. The reports can be put together to make a dashboard. You can also use other business intelligence tools.

### Insight Zeppelin

> **Note:** Before upgrading Insight Zeppelin ensure you backup your notes first. Then once the upgrade is complete you can re-import them. See [Export/Import Insight Zeppelin Notes](#export/import-insight-zeppelin-notes)

This is a list of pre-configured reports:

* Repository reports
  * Total storage used in bytes
  * Total number of documents
  * Total folders
  * Count of documents by MIMEtype

* Site reports
  * Total documents by site
  * Total documents by site and MIMEtype
  * Total volume by site in bytes
  * Activity reports

* Count of content created per day in the last 60 days
  * Count of content modified per day in the last 60 days
  * New documents by user and site
  * Modified documents by user and site
  * Count of locked content by user
  * Top largest documents

The following image shows an example dashboard created using the pre-configured reports.

![]({% link insight-engine/images/exampledashboard1.png %})

### Other business intelligence tools

In addition to using Insight Zeppelin for reporting you can also use any application that supports ODBC connectivity.

The CData ODBC Driver for Alfresco 2019 enables you to have real-time access to your data so you can run reports on the contents of the repository. Currently Alfresco has tested Tableau and Microsoft Excel. For more information and how to install the CData ODBC Driver see the following documentation [CData ODBC Driver for Alfresco 2019](http://cdn.cdata.com/help/SJE/odbc/default.htm).

### Export/Import Insight Zeppelin notes

Before upgrading Search and Insight Engine ensure you export each individual Insight Zeppelin note so you can reimport them after the upgrade. If you don't do this your notes will be lost as they do not carry over during the upgrade.

> **Note:** When importing an Insight Zeppelin note you may need to set its note permissions again.

Use these steps to export and import your Insight Zeppelin notes.

1. Go to Insight Zeppelin.

2. On the Welcome to Zeppelin home page access a note.

3. Click the **Export this note** button.

4. Return to the Welcome to Zeppelin home page and repeat the procedure for all your notes.

5. Once the upgrade is complete return to the Welcome to Zeppelin home page.

6. Click **Import note**.

7. Click **Select JSON file** and select the note you want to reimport.

    If you want to reimport the note with a different name you can enter it into the **Import as** field.

8. Repeat the procedure for all your notes.
---
title: SQL commands
---

Below is a list of the supported and unsupported SQL commands available to use when writing queries against your Solr datastore.

## Supported SQL commands

> **Note:** If an SQL command is not listed it is not supported.

### Select Statements

The basic syntax of the SQL select statement is as follows:

```sql
Select DBID, cm_creator as creator, `cm_content.size`  as `size` from alfresco where `cm_content.size` > 1000 order by  `cm_content.size` desc limit 100
```

### Table

The only table that can be specified is the alfresco table. The alfresco table contains the documents and fields that have been indexed within the Alfresco Indexing Server’s main Alfresco index.

### Fields

#### Standard fields

Alfresco has a set of standard fields, which can be referred to by name in the SQL field list. The DBID field in the example `SELECT` statement above is an example of a standard field.

The most useful ones are: `PARENT`, `PATH`, `ANCESTOR`, `TYPE`, `ASPECT`, `PROPERTIES`, `FIELDS`, `LID`, and `DBID`.

#### Fields from Content Models

Fields from Alfresco’s out of-the-box content models, as well as fields from custom content models can be referred to using the content model property qname, as in AFTS and the CMIS query language. The `cm_creator` field in the example SQL statement refers to the creator field in the out-of-the-box cm content model. Fields that have a unique local name over all prefixes do not need to use the prefix.

> **Note:** Use "_" to separate the prefix and the locale name as ":" would have to be escaped.

#### Escaping Fields

Fields that include reserved words or special characters will need to be escaped using the back tick character. The `cm_content.size` field in the example SQL statement is an example of back tick escaping. The only non-word character that can be used without escaping is the underscore “_”. We use Apache Calcite which has a list of reserved words that also need to be escaped, see [https://calcite.apache.org/docs/reference.html](https://calcite.apache.org/docs/reference.html){:target="_blank"}. You are most likely to hit reserved keywords picking aliases for fields.

#### Select Queries

A curated set of fields are returned by default when \* is used as the field list. Any field in the curated list of fields can be used in the SQL predicate and order by clause of a select * query.

The curated set of fields that are returned with select * queries include:

* `cm_name`
* `cm_created`
* `cm_creator`
* `cm_modified`
* `cm_modifier`
* `cm_owner`
* `OWNER`
* `TYPE`
* `LID`
* `DBID`
* `cm_title`
* `cm_description`
* `cm_content.size`
* `cm_content.mimetype`
* `cm_content.encoding`
* `cm_content.locale`
* `cm_lockOwner`
* `SITE`
* `PRIMARYPARENT`
* `PARENT`
* `PATH`
* `ASPECT`
* `QNAME`

If you are using a custom model you can specify the extra fields to appear in a select * query. You must add them to `alfresco-insight-engine/solrhome/conf/shared.properties` and they can take the form of either of the following formats:

> **Note:** The field list is case insensitive.

```sql
#Custom Model
solr.sql.alfresco.fieldnames=finance:amount, finance:emp,expense:recorded_at
```

Or

```sql
#Custom Model
solr.sql.alfresco.fieldnames=finance_amount, finance_emp,expense_recorded_at
```

Select * will also return any fields that appear in the predicates for the query, in the following format:

> **Note:** The predicates are case insensitive.

```sql
select * from alfresco where finance_amount > 0 and expense_recorded_at <= 'NOW/DAY'
```

This query will also return the fields `finance_amount` and `expense_recorded_at` in addition to the curated set of fields.

#### Arithmetic Operators

You can use arithmetic operations (+ - * /) on the SELECT clause.

```sql
select `expense:Amount` / `expense:ExchangeRate` from alfresco where TYPE = 'expense:expenseReport'
```

```sql
Select Site, sum(`cm:content.size`)/1000 as `Storage Used` from alfresco group by Site
```

```sql
Select expense_Currency, max(`expense:Amount`) * 100 as MaxAmount, sum(`expense:Amount`)/100 as SumAmount from alfresco group by expense_Currency
```

> **Note:** You can't use WHERE, GROUP BY, HAVING, and ORDER clauses with arithmetic operations.

#### Field Aliases

SQL field aliases are supported in the field list. Field aliases that contain special characters or reserved words need to be escaped with the back tick.

> **Note:** You can't use the WHERE, ORDER BY or HAVING clauses with field aliases.

To display the Aliases correctly use the following format:

```sql
select sum(`cm:content.size`) as StorageUsed from alfresco
```

If using Apache Zeppelin please note that aliases are only supported for the aggregate fields (count, sum, min, max, avg) and are ignored for non aggregate fields. For example, the following format would not display the field alias in Apache Zeppelin:

```sql
select `cm:content.size` as StorageUsed from alfresco
```

You can use the table prefix 'alfresco' within your queries or `()`. The following two examples return the same information.

```sql
select alfresco.`cm_content.size`, alfresco.cm_name from alfresco
```

Or

```sql
select (alfresco.`cm_content.size`), alfresco.cm_name from alfresco
```

### Count

Alfresco’s SQL count query is an aggregate function that is used to return the number of rows from a table that fulfil the criteria specified.

The following query returns the number of rows that have a value for cm_title.

```sql
SELECT count(cm_title) from alfresco
```

The following query returns the number of rows that have a distinct value for cm_title.

```sql
SELECT count(distinct(cm_title)) from alfresco
```

> **Note:** `count(field)` and `count( distinct field)` queries are not supported with a group by clause, for example:

```sql
SELECT Type, count(cm_name) from alfresco group by Type
```

Also the following data types are not supported when using `count(field)` and `count(distinct field)` queries: boolean, cm:content, text: if the text fields are defined as non-facetable and tokenised (free-text). For example they have the following indexing configuration:

```sql
<index enabled="true">
  <tokenised>TRUE</tokenised>
  <facetable>false</facetable>
</index>
```

### Predicate

Alfresco’s SQL predicate is designed to take advantage of the rich search capabilities available in the Alfresco Search Services.

#### Predicates on Text Fields

The basic predicate on a text field performs a phrase search. Below is the syntax of a basic predicate on a text field. It will search for the phrase 'hello world' in the cm_content field.

```sql
select cm_name, `cm_content.size` from alfresco where (cm_content = ‘hello world’)  
```

To gain full control of the search predicate for a specific field you can wrap the predicate in parenthesis and enter the query using Alfresco full text search syntax. For example to search for (hello OR world) in the cm_content field the following search predicate can be used:

```sql
select cm_name, `cm_content.size` from alfresco where cm_content = ‘(hello OR world)’
```

#### Predicates on String Identifier Fields

Predicates on string identifier fields will perform an exact match on the field. Below is an example of a SQL statement that will perform an exact match on the LID field:

```sql
select cm_name, `cm_content.size` from alfresco where LID = ‘value’
```

> **Note:** Most fields from the content models will perform full text search matches unless the property is defined as tokenised false in the model. This may not be what you expect.

#### Predicates on Numeric Fields

The predicate on numeric fields can perform =, >=, <= and Alfresco Solr range queries.

Below is an examples using the =, >=, <= range operators.

```sql
select cm_name, `cm_content.size` from alfresco where cm_content.size = 2000
select cm_name, `cm_content.size` from alfresco where cm_content.size >= 2000
select cm_name, `cm_content.size` from alfresco where cm_content.size <= 2000
select cm_name, `cm_content.size` from alfresco where `cm_content.size` ='[* TO 2000>'
```

Below are examples of Alfresco Solr range queries:

Selects all cm_content.size below 2000, with inclusive ranges. The square brackets are inclusive ranges.

```sql
select cm_name, `cm_content.size` from alfresco where cm_content.size ='[* TO 2000]'
```

Selects all cm_content.size below 2000, with an exclusive top range. < and > are exclusive ranges.

```sql
select cm_name, `cm_content.size` from alfresco where cm_content.size ='[* TO 2000>'
```

Selects all cm_content.size above 2000, with inclusive ranges.

```sql
select cm_name, `cm_content.size` from alfresco where cm_content.size ='[2000 TO *]'
```

Selects all cm_content.size above 2000, with an exclusive bottom range.

```sql
select cm_name, `cm_content.size` from alfresco where cm_content.size ='<2000 TO *]'
```

Selects all cm_content.size above 100 and below 2000, exclusively.

```sql
select cm_name, `cm_content.size` from alfresco where cm_content.size ='<100 TO 2000>'
```

#### Predicates on Null Fields

Predicates on null values can be constructed using `IS NULL`, `IS NOT NULL`, `IN (NULL)`, and `NOT IN (NULL)` operands to obtain the results.

The following IS NULL query will return all the rows that have a value of NULL for the field cm_content.size .

```sql
select cm_name, `cm_content.size` from alfresco where `cm_content.size` IS NULL
```

The following IS NOT NULL query will return all the rows that have a value different from NULL for the field `cm_content.size`.

```sql
select cm_name, `cm_content.size` from alfresco where `cm_content.size` IS NOT NULL
```

The following IN NULL query will return all the rows that have `cm_content.size` in 'system' or `NULL`.

```sql
select cm_name, cm_creator, `cm_content.size` from alfresco where cm_creator IN ('System', NULL)
```

The following `NOT IN NULL` query will return all the rows that have `cm_content.size` not in 'system' or `NULL`.

```sql
select cm_name, cm_creator, `cm_content.size` from alfresco where cm_creator NOT IN ('System', NULL)
```

The following `NOT IN (NULL)` query will return all the rows where `cm_content.size` is not equal to `0` and is not `NULL`.

```sql
select cm_name, `cm_content.size` from alfresco where `cm_content.size` NOT IN (0, NULL)
```

#### Nested Boolean Predicates

SQL predicates can be combined with Boolean operators `AND`, `OR` and `NOT` and nested with parenthesis.

```sql
SITE = ‘MySite’ AND `cm_content.mimetype` = 'text/plain'
```

#### SQL IN Operator

The SQL IN operator can be used in the predicate for both numeric and string fields. Null values are accepted as values in the filter list.

#### SQL NOT IN Operator

The SQL `NOT IN` operator can be used in the predicate for both numeric and string fields. Null values are accepted as values in the filter list, but due to SQL limitations the query will produce no results.

> **Note:** Use an equivalent query when fetching NULL values instead of including the null as a value of a `NOT IN` list.

#### Order By

SQL SELECT statements can contain an ORDER BY clause with one or more order by fields. String identifiers and numeric fields can be specific in the ORDER BY clause.

Below is an example of an ORDER BY on a numeric field:

```sql
select cm_creator, cm_name, exif_manufacturer, audio_trackNumber from alfresco order by audio_trackNumber asc
```

#### Limit

SQL SELECT statements can contain a `LIMIT` clause. If no limit is specified a default limit of 1000 is set.

> **Note:** Caution should be used when increasing the default limit as performance and memory consumption increase as the limit increases.

### SELECT DISTINCT statements

The basic syntax for `SELECT DISTINCT` is as follows:

```sql
select distinct cm_name from alfresco where cm_content = 'alfresco' order by cm_name asc
```

`SELECT DISTINCT` queries can also have multiple fields and multiple order by fields.

### Is Null statements

The basic syntax for Is Nulls is as follows:

```sql
select cm_name, `cm:content.size` from alfresco where `cm:content.size` IS NULL
```

### Is Not Null statements

The basic syntax for `Is Not Null` is as follows:

```sql
select cm_name, `cm_content.size` from alfresco where `cm_content.size` IS NOT NULL
```

### Aggregations Without GROUP BY

SQL aggregations without a `GROUP BY` clause return a single result tuple with the aggregation results. See below for an example:

```sql
select count(*) as docCount, avg(`cm_content.size`) as content_size from alfresco where cm_owner = 'xyz
```

#### Aggregate Result Tuple

If a field alias is specified for an aggregate function then the field alias will appear in the result tuple. If field aliases are not used then the field name for the aggregate functions will appear as follows: `EXPR$1`, `EXPR$2`. These values refer to the function expression by the order they appear in the field list, starting from 1. For example the first function that appears in the query will be named EXPR$1 in the result tuples.

### Aggregations With GROUP BY

SQL aggregations with a GROUP BY clause are also supported and take the following form:

```sql
select `cm_content.mimetype`, count(*) as total_count from alfresco group by `cm_content.mimetype` having count(*) < 4 order by count(*) asc
```

#### Aggregate functions

Alfresco SQL supports the following aggregation functions:

* `count(*)`
* `count(field)`
* `count(distinct field)`
* `sum(numeric_field)`
* `avg(numeric_field)`
* `min(numeric_field)`
* `max(numeric_field)`

#### Aggregation fields

Any numeric field can be used within the aggregations sum, avg, min, and max. As with the basic SELECT statements fields defined by content models can be referenced using the content model prefix. Fields that are reserved words or contain special characters need to be escaped with the back tick character.

#### Group By Fields

One or more fields can be specified as group by fields. Fields that are designated as facetable in a content model will provide the best aggregation results.

> **Note:** Group by is supported for text fields when the content model has the following setting for the text field.

* LOV whole or partial match
* unique match: partial, many

It’s not supported when the text field is either freetext or none.

#### Aggregate Result Tuples

If a field alias is specified for an aggregate function then the field alias will appear in the result tuple. If field aliases are not used then the field name for the aggregate functions will appear as follows: EXPR$1, EXPR$2. These values refer to the function expression by the order they appear in the query, starting from 1. For example the first function that appears in the query will be named EXPR$1 in the result tuples.

#### Order By (GROUP BY)

One or more fields may be used in the ORDER BY clause. The ORDER BY can include both fields from the field list and the result of the COUNT function. ORDER BY for other aggregate functions is not yet supported. Field aliases cannot be used in the ORDER BY clause. When referring to an aggregate function in the ORDER BY clause the function call as it appears in the field list should be used.

> **Note:** Order by is supported for text fields when the content model has the following setting for the text field.

* LOV whole or partial match
* unique match: partial, many

It’s not supported when the text field is either freetext or none.

#### Having

The `HAVING` clause is supported for aggregation functions only. Boolean logic and nested `HAVING` clauses are supported. The following comparison operations are supported in the `HAVING` clause: `=`, `>=`, `<=`, `!=`.

> **Note:** Support is limited for the `HAVING` clause in Search and Insight Engine 2.0.

#### Limit (GROUP BY)

A `LIMIT` clause can be used to limit the number of aggregations results. If no LIMIT clause is provided a default limit of 1000 is applied.

### Time Series Aggregations

There is specific support for SQL time series reporting through the use of virtual time dimensions. The following section describes how virtual time dimensions are used.

#### Virtual Time Dimensions

Search and Insight Engine automatically creates virtual time dimensions for every datetime field stored in the Alfresco Search Service. The three virtual time dimensions supported are:  `_day`, `_month`, `_year`. To use the virtual time dimensions append the virtual time dimension to any datetime field and use it in the `GROUP BY` clause. Below is an example where the `_day` dimension is appended to the `cm_created` datetime field. The query creates a daily time series report using the `cm_created_day` virtual time dimension.

```sql
select cm_created_day, count(*) as total from alfresco where cm_created >= 'NOW/DAY' group by cm_created_day
```

### Datetime Predicates

A datetime predicate can be used in the `WHERE` clause to control the datetime range of the time series report. This is a datetime predicate on the `cm_create`d field. Its important to note that the virtual time dimension field is only used in the field list and `GROUP BY` clause. The predicate is applied to the non-virtual datetime field in the index. This example uses a date math expression to specify a lower boundary for the time series report and is a datetime predicate on the `cm_created` field.

```sql
where cm_created >= 'NOW/DAY'
```

#### Unbounded Time Series Reports

> **Note:** The sections below describe how to set lower and upper boundaries using both fixed date and date math predicates.

If no datetime predicate is supplied, the following default lower and upper boundaries for the different time dimensions are used:

**day:**

* **lower:** current day minus 1 month
* **upper:** current full day

**month:**

* **lower:** current month minus 24 months
* **upper:** current full month

**year:**

* **lower:** current year minus 5 years
* **upper:** current full year

#### Fixed Datetime Predicates

Fixed datetime predicates are formatted according to a subset of ISO 8601. They require the full precision to be expressed in the statement, see the example below:

```sql
select cm_created_day, count(*) from alfresco where cm_created >= '2010-02-01T01:01:01Z' and cm_created <= '2010-02-14T23:59:59Z' group by cm_created_day
```

#### Date Math Predicates

Search and Insight Engine also supports a rich set of date math expressions. The example below uses a time series aggregation using date math predicates. The `NOW` clause signifies the current point in time with milli-second precision. The `NOW/MONTH` clause rounds the current point in time down to the current `MONTH`, i.e. The -6MONTHS subtracts 6 months from the current month. See the [Solr date math guide](https://lucene.apache.org/solr/guide/6_6/working-with-dates.html#WorkingwithDates-DateMathSyntax) for more details on date math syntax.

```sql
select cm_created_month, count(*) from alfresco where cm_created >= 'NOW/MONTH-6MONTHS' and cm_created <= 'NOW' group by cm_created_month
```

#### Autofilled Date/Time Ranges

Time series aggregation queries return an aggregation value for all date/time values that fall within the range. Date/time values that do not have data present within the range still appear in the result set with aggregation values of 0.

#### Single Dimension Group By

Time series aggregations that group by virtual time dimensions are currently limited to using a single group by field.

#### Order By (Datetime)

By default time series aggregation results are sorted in datetime ascending order. An order by clause can be used to change the direction of the datetime sort or sort by the result of the COUNT function. `ORDER BY` for other aggregate functions is not yet supported.

#### Having (Datetime)

A `HAVING` clause can be used to filter time series aggregations results.

## Unsupported SQL commands

Search and Insight Engine supports a subset of SQL. Below is a list of commonly used SQL commands that are not currently supported:

### Commands

* `CMIS QL functions IN_TREE, IN_FOLDER, SCORE, CONTAINS`
* `DATEDIFF`
* `DBID Range Queries`
* `HAVING` : Can only be applied to aggregate functions.
* `JOIN`
* `LIKE`
* `Multivalued fields`
* `String, Math Operators`
* `SUB-QUERIES`
* `UNION`

## Search using conjunctions

Single terms, phrases, and so on can be combined using "`AND`" in upper, lower, or mixed case.

```sql
big AND yellow AND banana
TEXT:big and TEXT:yellow and TEXT:banana
```

These queries search for nodes that contain the terms "big", "yellow", and "banana" in any content.
---
title: JDBC driver
---

Search and Insight Engine includes a JDBC thin client that can be used with Insight Zeppelin and other SQL clients.

To access the client log into [https://nexus.alfresco.com/nexus/#welcome](https://nexus.alfresco.com/nexus/#welcome) and search for `alfresco-insight-jdbc-2.0.0.jar`.

> **Note:** Contact [Alfresco Support](https://support.alfresco.com/){:target="_blank"} for log in credentials.

## Connection string

The connection string's host and port should point to the Alfresco Content Services repository. The Alfresco Content Services repository performs the authentication. It applies the access control lists to the request before forwarding the request to Search and Insight Engine.

The JDBC connection string uses the following format:

```bash
jdbc:alfresco://<alfresco-server-name>:<alfresco-server-port>?collection=alfresco
```

For example, this database URL property value:

```bash
jdbc:alfresco://localhost:8080?collection=alfresco
```

Will generate the following request:

`http://localhost:8080/alfresco/api/-default-/public/search/versions/1/jdbc`

> **Note:** When using the default HTTP port of 80 you do not need to add it to the database URL.

## Alfresco using web proxy with HTTPS

When Alfresco Content Services is configured to use HTTPS with a WebProxy like Apache HTTPd or NGINX, the JDBC connection string uses the following format:

```bash
jdbc:alfresco://localhost?collection=alfresco
```

> **Note:** When using the default connection port of 443 you do not need to add it to the connection string.

When using HTTPs you need to add the following driver properties:

```bash
javax.net.ssl.trustStoreType: JKS
javax.net.ssl.trustStore: /docker-compose/stores/trusted.jks
javax.net.ssl.trustStorePassword: alfresco

alfresco.enable.ssl: true
alfresco.ssl.checkPeerName: false
```

> **Note:** The trusted.jks file is a truststore that includes the public certificate of your Alfresco Content Services HTTPs endpoint. If you are using an SSL certificate that is trusted by your JVM, and it includes the real DNS in the CN field of the certificate, you only need to include the following configuration in the driver properties:

```bash
alfresco.enable.ssl: true
```

## Alfresco using mTLS

When Alfresco Content Services is configured to use mTLS to communicate with SOLR, the JDBC connection string uses the following format:

```bash
jdbc:alfresco://localhost:8443?collection=alfresco
```

You need to add the truststore and keystore from SOLR to the properties of the driver using the following:

```bash
javax.net.ssl.trustStoreType: JCEKS
javax.net.ssl.trustStore: /docker-compose/keystores/solr/ssl.repo.client.truststore
javax.net.ssl.trustStorePassword: kT9X6oe68t

javax.net.ssl.keyStoreType: JCEKS
javax.net.ssl.keyStore: /docker-compose/keystores/solr/ssl.repo.client.keystore
javax.net.ssl.keyStorePassword: kT9X6oe68t

alfresco.enable.ssl: true
alfresco.ssl.checkPeerName: false
```

## Authentication and authorization

The Search and Insight Engine JDBC driver logs into Alfresco Content Services using the same credentials used to access the Alfresco Content Services repository. The results of all queries are limited to the documents the user has been authorized to read.

### Usage

The Alfresco JDBC driver can be used from programs like [DbVisualizer](https://www.dbvis.com/) and [SquirrelSql](http://squirrel-sql.sourceforge.net/) but you can also write custom code using Java to perform SQL queries. For example:

```java
String sql = "select DBID, LID from alfresco where cm_content = 'world' order by DBID limit 10 ";
String alfrescoJson = "{"tenants":[""],"locales":["en_US"],"defaultNamespace":"http://www.alfresco.org/model/content/1.0","textAttributes":[],"defaultFTSOperator":"OR","defaultFTSFieldOperator":"OR","anyDenyDenies":true,"query":"name:*","templates":[],"allAttributes":[],"queryConsistency":"DEFAULT","authorities":["GROUP_EVERYONE","ROLE_ADMINISTRATOR","ROLE_AUTHENTICATED","admin"]}";

Properties props = new Properties();
props.put("alfresco.shards", "http://localhost:8983/solr/alfresco")
props.put("json", alfrescoJson);

String connectionString = "jdbc:alfresco://localhost:8080?collection=alfresco";
Connection con = null;
Statement stmt = null;
ResultSet rs = null;

try {
        con = DriverManager.getConnection(connectionString, props);
        stmt = con.createStatement();
        rs = stmt.executeQuery(sql);
        int i=0;
        while (rs.next()) {
            System.out.println(rs.getString("DBID"));
        }
    } finally {
        try { rs.close(); } catch(Exception e) {}
        try { stmt.close();} catch(Exception e) {}
        try { con.close();} catch(Exception e) {}
    }
}
```

### Additional notes

When using trusted certificates (included by default on the JVM), the java.net.ssl.trustStore properties setting can be skipped.

Trusted certificates (CAs) that appear by default in your local JVM can be obtained with the following command:

```bash
$ keytool -list -cacerts
```

When using a certificate, including the name of the server of the real DNS in the CN attribute of the certificate, the `alfresco.ssl.cheekPeerName` setting can be skipped.
---
title: Full text search reference
---

The following sections describe the Alfresco Full Text Search (FTS) syntax.

The Alfresco Full Text Search (FTS) query text can be used standalone or it can be embedded in CMIS-SQL using the `contains()` predicate function. The CMIS specification supports a subset of FTS. The full power of FTS can not be used and, at the same time, maintain portability between CMIS repositories.

FTS is exposed directly by the interface, which adds its own template, and is also used as its default field. The default template is:

```sql
%(cm:name cm:title cm:description ia:whatEvent ia:descriptionEvent lnk:title lnk:description TEXT)
```

When FTS is embedded in CMIS-SQL, only the CMIS-SQL-style property identifiers (`cmis:name`) and aliases, CMIS-SQL column aliases, and the special fields listed can be used to identify fields. The SQL query defines tables and table aliases after `from` and `join` clauses. If the SQL query references more than one table, the `contains()` function must specify a single table to use by its alias. All properties in the embedded FTS query are added to this table and all column aliases used in the FTS query must refer to the same table. For a single table, the table alias is not required as part of the `contains()` function.

When FTS is used standalone, fields can also be identified using `prefix:local-name` and `{uri}local-name` styles.

Query time boosts allow matches on certain parts of the query to influence the score more than others.

All query elements can be boosted: terms, phrases, exact terms, expanded terms, proximity (only in filed groups), ranges, and groups.

```bash
term^2.4
"phrase"^3
term~0.8^4
=term^3
~term^4
cm:name:(big * yellow)^4
1..2^2
[1 TO 2]^2
yellow AND (car OR bus)^3
```

## Search using date math

The date field types in Solr support the date math expressions.

The date math expression makes it easy to create times relative to fixed moments in time and includes the current time which can be represented using the special value of `NOW`.

### Date math syntax

The date math expressions consist either adding some quantity of time in a specified unit, or rounding the current time by a specified unit. Expressions can be chained and are evaluated left to right.

For example, to represents a point in time two months from now, use:

```text
NOW+2MONTHS
```

To represents a point in time one day ago, use:

```text
NOW-1DAY
```

A slash is used to indicate rounding. To represents the beginning of the current hour, use:

```text
NOW/HOUR
```

To represent a point in time six months and three days into the future and then rounds that time to the beginning of that day, use:

```text
NOW+6MONTHS+3DAYS/DAY
```

While date math is most commonly used relative to `NOW`, it can be applied to any fixed moment in time as well:

```text
1972-05-20T17:33:18.772Z+6MONTHS+3DAYS/DAY
```

> **Note:** Solr 6 date math supports `TODAY`.

## Search for disjunctions

Single terms, phrases, and so on can be combined using `OR` in upper, lower, or mixed case.

The `OR` operator is interpreted as "at least one is required, more than one or all can be returned".

If not otherwise specified, by default search fragments will be `ORed` together.

```text
big yellow banana
big OR yellow OR banana
TEXT:big TEXT:yellow TEXT:banana
TEXT:big OR TEXT:yellow OR TEXT:banana
```

These queries search for nodes that contain at least one of the terms `big`, `yellow`, or `banana` in any content.

## Escaping characters

Any character can be escaped using the backslash "" in terms, IDs (field identifiers), and phrases. Java unicode escape sequences are supported. Whitespace can be escaped in terms and IDs.

For example:

```sql
cm:my content:my name
```

## Search for an exact term

To search for an exact term you must prefix it with "=". The supported syntax:

* `=term`
* `=term1 =term2`
* `=“multi term phrase”`

    > **Note:** `=“multi term phrase”` returns documents only with the exact phrase and terms in the exact order.

* `=field:term`
* `=field:term1 =field:term2`
* `=field:“multi term phrase”`

If you don’t specify a field the search runs against name, description, title, and content. If the field specified is `TOKENIZED=false`, only the full field is matched. If the field you specified is `TOKENIZED=TRUE` or `TOKENIZED=BOTH` then the search is run on the cross locale tokenized version of the field.

> **Note:** If cross locale is not configured for the field then an exception occurs.

The list of default supported Alfresco properties is declared in the `<insight_engine_home>/solrhome/conf/shared.properties` file:

```text
alfresco.cross.locale.property.0={http://www.alfresco.org/model/content/1.0}name
alfresco.cross.locale.property.1={http://www.alfresco.org/model/content/1.0}lockOwner
```

You can extend that capability by uncommenting the lines below and performing a full reindex. This has the result of enabling cross locale on all properties defined with those property types:

```text
alfresco.cross.locale.datatype.0={http://www.alfresco.org/model/dictionary/1.0}text
alfresco.cross.locale.datatype.1={http://www.alfresco.org/model/dictionary/1.0}content
alfresco.cross.locale.datatype.2={http://www.alfresco.org/model/dictionary/1.0}mltext
```

## Search in fields

Search specific fields rather than the default. Terms, phrases, etc. can all be preceded by a field. If not the default field TEXT is used.

```bash
field:term
field:"phrase"
=field:exact
~field:expand
```

Fields fall into three types: property fields, special fields, and fields for data types.

Property fields evaluate the search term against a particular property, special fields are described in the following table, and data type fields evaluate the search term against all properties of the given type.

|Type|Description|
|-----------|----|
|Property|Fully qualified property, for example `{http://www.alfresco.org/model/content/1.0}name:apple`|
|Property|Fully qualified property, for example `@{http://www.alfresco.org/model/content/1.0}name:apple`|
|Property|CMIS style property, for example `cm_name:apple`.|
|Property|Prefix style property, for example `cm:name:apple`.|
|Property|Prefix style property, for example `@cm:name:apple`.|
|Property|TEXT, for example `TEXT:apple`.|
|Special|ID, for example `ID:"NodeRef"`|
|Special|ISROOT, for example `ISROOT:T`|
|Special|TX, for example `TX:"TX"`|
|Special|PARENT, for example `PARENT:"NodeRef"`|
|Special|PRIMARYPARENT, for example `PRIMARYPARENT:"NodeRef"`.|
|Special|QNAME, for example `QNAME:"app:company_home"`.|
|Special|CLASS, for example `CLASS:"qname"`.|
|Special|EXACTCLASS, for example `EXACTCLASS:"qname"`.
|Special|TYPE, for example `TYPE:"qname"`.
|Special|EXACTTYPE, for example `EXACTTYPE:"qname"`.
|Special|ASPECT for example `ASPECT:"qname"`.|
|Special|EXACTASPECT, for example `EXACTASPECT:"qname"`.|
|Special|ISUNSET for example `ISUNSET:"property-qname"`|
|Special|ISNULL, for example `ISNULL:"property-qname"`.|
|Special|ISNOTNULL, for example `ISNOTNULL:"property-qname"`.|
|Special|EXISTS for example `EXISTS:"name of the property"`.|
|Special|SITE for example `SITE:"shortname of the site"`.|
|Special|TAG. TAG: "name of the tag" **Note:** `TAG` must be in upper case.|
|Fully qualified data type|Data Type, `http://www.alfresco.org/model/dictionary/1.0}content:apple`|
|prefixed data type|Data Type, d:content:apple|

## Search in multi-value fields

When you search in multi-value fields there are additional options available than for [Search in fields](#search-in-fields). To search in multi-value fields your properties must have `Multiple` values enabled, for more see [Create a property
]({% link content-services/latest/config/models.md %}#create-a-property).

The following example queries are executed using a sample multi-valued property `"mul:os"` that stores values `"MacOS"` and `"Linux"`.

`mul:os:"MacOS"`

Returns the document because `"MacOS"` is one of the values of the property.

`mul:os:("MacOS" AND "Windows")`

Does not return a document because the property doesn't contain the value `"Windows"`.

`mul:os:("MacOS" OR "Windows")`

Returns the document because `"MacOS"` is one of the values of the property, even though `"Windows"` is not.

## Mixed FTS ID behavior

This relates to the priority defined on properties in the data dictionary, which can be both tokenized or untokenized.

Explicit priority is set by prefixing the query with "=" for identifier pattern matches.

The tilde (`~`) can be used to force tokenization.

## Search for fuzzy matching

Alfresco supports fuzzy searches based on the Lucene default Levenshtein Distance.

To do a fuzzy search use the tilde (`~`) symbol at the end of a single word term with a parameter between 0 and 1 to specify the required similarity. Use a value closer to 1 for higher similarity.

For example, to search for a term similar in spelling to *roam* use the fuzzy search:

```bash
roam~0.9
```

This search will find terms like *foam*, *roaming*, and *roams*.

## Search for grouping

Use parentheses to encapsulate `OR` statements for the search engine to execute them properly.

The `OR` operator is executed as "I would like at least one of these terms".

Groupings of terms are made using `( and )`. Groupings of all query elements are supported in general. Groupings are also supported after a field - field group.

The query elements in field groups all apply to the same field and cannot include a field.

```sql
(big OR large) AND banana  
title:((big OR large) AND banana)
```

## Search query literals

When you search, entries are generally a term or a phrase. The string representation you type in will be transformed to the appropriate type for each property when executing the query. For convenience, there are numeric literals but string literals can also be used.

### Date formatting

You can specify either a particular date or a date literal. A date literal is a fixed expression that represents a relative range of time, for example last month, this week, or next year.

`dateTime` field values are stored as Coordinated Universal Time (UTC). The date fields represent a point in time with millisecond precision. For date field formatting, Solr uses [DateTimeFormatter.ISO_INSTANT](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html#ISO_INSTANT){:target="_blank"}. The ISO instant formatter formats an instant in Coordinated Universal Time (UTC), for example:

```bash
YYYY-MM-DDThh:mm:ssZ
```

where,

* `YYYY` is the year.
* `MM` is the month.
* `DD` is the day of the month.
* `hh` is the hour of the day as on a 24-hour clock.
* `mm` is minutes.
* `ss` is seconds.
* `Z` is a literal `Z` character indicating that this string representation of the date is in UTC.

> **Note:** No time zone can be specified. The string representation of dates is always expressed in UTC, for example:

```bash
1972-05-20T17:33:18Z
```

### String literals

String literals for phrases can be enclosed in double quotes or single quotes. Java single character and `uXXXX`-based escaping are supported within these literals.

Integer and decimal literals conform to the Java definitions.

Dates as any other literal can be expressed as a term or phrase. Dates are in the format `......` Any or all of the time can be truncated.

In range queries, strings, term, and phrases that do not parse to valid type instance for the property are treated as open ended.

```bash
test:integer[ 0 TO MAX] matches anything positive
```

## Search for negation

You can narrow your search results by excluding words with the `NOT` syntax.

Single terms, phrases, and so on can be combined using "`NOT`" in upper, lower, or mixed case, or prefixed with "`!`" or "`-`".

These queries search for nodes that contain the terms `yellow` in any content.

```sql
yellow NOT banana
yellow !banana
yellow -banana
NOT yellow banana
-yellow banana
!yellow banana
```

The `NOT` operator can only be used for string keywords; it doesn't work for numerals or dates.

Prefixing any search qualifier with a `-` excludes all results that are matched by that qualifier.

## Search for optional, mandatory, and excluded elements of a query

Sometimes AND and OR are not enough. If you want to find documents that must contain the term "car", score those with the term "red" higher, but do not match those just containing "red".

|Operator|Description|
|--------|-----------|
|","|The field, phrase, group is optional; a match increases the score.|
|"+"|The field, phrase, group is mandatory (Note: this differs from Google - see "=")|
|"-", "!"|The field, phrase, group must not match.|

The following example finds documents that contain the term "car", score those with the term "red" higher, but does not match those just containing "red":

```sql
+car |red
```

> **Note:** At least one element of a query must match (or not match) for there to be any results.

All `AND` and `OR` constructs can be expressed with these operators.

## Search for a phrase

Phrases are enclosed in double quotes. Any embedded quotes can be escaped using ``. If no field is specified then the default TEXT field will be used, as with searches for a single term.

The whole phrase will be tokenized before the search according to the appropriate data dictionary definition(s).

```sql
"big yellow banana"
```

## Search for operator precedence

Operator precedence is SQL-like (not Java-like). When there is more than one logical operator in a statement, and they are not explicitly grouped using parentheses, `NOT` is evaluated first, then `AND`, and finally `OR`.

The following shows the operator precedence from highest to lowest:

```sql
"
[, ], <, >
()
~ (prefix and postfix), =
^
+, |, -
NOT,
AND
OR
```

`AND` and `OR` can be combined with `+`, `|`, `-` with the following meanings:

|AND (no prefix is the same as +)|Description|
|----------------------------------|-----------|
|`big AND dog`|big and dog must occur|
|`+big AND +dog`|big and dog must occur|
|`big AND +dog`|big and dog must occur|
|`+big AND dog`|big and dog must occur|
|`big AND \|dog`|big must occur and dog should occur|
|`\|big AND dog`|big should occur and dog must occur|
|`\|big AND \|dog`|both big and dog should occur, and at least one must match|
|`big AND -dog`|big must occur and dog must not occur|
|`-big AND dog`|big must not occur and dog must occur|
|`-big AND -dog`|both big and dog must not occur|
|`\|big AND -dog`|big should occur and dog must not occur|

|OR (no prefix is the same as +)|Description|
|---------------------------------|-----------|
|`dog OR wolf`|dog and wolf should occur, and at least one must match|
|`+dog OR +wolf`|dog and wolf should occur, and at least one must match|
|`dog OR +wolf`|dog and wolf should occur, and at least one must match|
|`+dog OR wolf`|dog and wolf should occur, and at least one must match|
|`dog OR \|wolf`|dog and wolf should occur, and at least one must match|
|`\|dog OR wolf`|dog and wolf should occur, and at least one must match|
|`\|dog OR \|wolf`|dog and wolf should occur, and at least one must match|
|`dog OR -wolf`|dog should occur and wolf should not occur, one of the clauses must be valid for any result|
|`-dog OR wolf`|dog should not occur and wolf should occur, one of the clauses must be valid for any result|
|`-dog OR -wolf`|dog and wolf should not occur, one of the clauses must be valid for any result|

## Embed queries in CMIS

These examples show how to embed queries in CMIS.

### Embedded in CMIS contains()

```sql
- strict queries
SELECT * FROM Document WHERE CONTAINS("zebra")
SELECT * FROM Document WHERE CONTAINS("quick")

- Alfresco extensions
SELECT * FROM Document D WHERE CONTAINS(D, 'cmis:name:\'Tutorial\'')
SELECT cmis:name as BOO FROM Document D WHERE CONTAINS('BOO:\'Tutorial\'')
```

### Search Service

```bash
ResultSet results = searchService.query(storeRef, SearchService.LANGUAGE_FTS_ALFRESCO, "quick");
```

```bash
SearchService.LANGUAGE_FTS_ALFRESCO = "fts-alfresco"
```

### Node Browser

FTS is supported in the node browser.

### JavaScript

```sql
search
{
   query: string,          mandatory, in appropriate format and encoded for the given language
   store: string,          optional, defaults to 'workspace://SpacesStore'
   language: string,       optional, one of: lucene, xpath, jcr-xpath, fts-alfresco - defaults to 'lucene'
   templates: [],          optional, Array of query language template objects (see below) - if supported by the language 
   sort: [],               optional, Array of sort column objects (see below) - if supported by the language
   page: object,           optional, paging information object (see below) - if supported by the language
   namespace: string,      optional, the default namespace for properties
   defaultField: string,   optional, the default field for query elements when not explicit in the query
   onerror: string         optional, result on error - one of: exception, no-results - defaults to 'exception'
}

sort
{
   column: string,         mandatory, sort column in appropriate format for the language
   ascending: boolean      optional, defaults to false
}

page
{
   maxItems: int,          optional, max number of items to return in result set
   skipCount: int          optional, number of items to skip over before returning results
}

template
{
   field: string,          mandatory, custom field name for the template
   template: string        mandatory, query template replacement for the template
}
```

For example:

```sql
 var def =
  {
     query: "cm:name:test*",
     language: "fts-alfresco"
  };
  var results = search.query(def); 
```

### Templates

FTS is not supported in FreeMarker.


## Search for proximity

Google-style proximity is supported.

To specify proximity for fields, use grouping.

```sql
big * apple
TEXT:(big * apple)
big *(3) apple
TEXT:(big *(3) apple)
```

## Search query templates

The FTS query language supports query templates. These are intended to help when building application specific searches.

A template is a query but with additional support to specify template substitution.

* **%field**

    Insert the parse tree for the current `ftstest` and replace all references to fields in the current parse tree with the supplied field.

* **%(field1, field2)%(field1 field2)**

    (The comma is optional.) Create a disjunction, and for each field, add the parse tree for the current `ftstest` to the disjunction, and then replace all references to fields in the current parse tree with the current field from the list.

|Name|Template|Example Query|Expanded Query|
|----|--------|-------------|--------------|
|t1|%cm:name|t1:n1|cm:name:n1|
|t1|%cm:name|t1:"n1"|cm:name:"n1"|
|t1|%cm:name|~t1:n1^4|~cm:name:n1^4|
|t2|%(cm:name, cm:title)|t2:"woof"|(cm:name:"woof" OR cm:title:"woof")|
|t2|%(cm:name, cm:title)|~t2:woof^4|(~cm:name:woof OR ~cm:title:woof)^4|
|t3|%cm:name AND my:boolean:true|t3:banana|(cm:name:banana AND my:boolean:true)|

Templates can refer to other templates.

```sql
nameAndTitle -> %(cm:name, cm:title)
nameAndTitleAndDesciption -> %(nameAndTitle, cm:description)
```

## Search for ranges

Inclusive ranges can be specified in Google-style. There is an extended syntax for more complex ranges. Unbounded ranges can be defined using MIN and MAX for numeric and date types and "u0000" and "FFFF" for text (anything that is invalid).

|Lucene|Google|Description|Example|
|------|------|-----------|-------|
|`[#1 TO #2]`|`#1..#2`|The range #1 to #2 inclusive ``#1 <= x <= #2``|`0..5``[0 TO 5]`|
|`<#1 TO #2]`| |The range #1 to #2 including #2 but not #1.`#1 < x <= #2`|`<0 TO 5]`|
|`[#1 TO #2>`| |The range #1 to #2 including #1 but not #2.`#1 <= x < #2`|`[0 TO 5>`|
|`<#1 TO #2>`| |The range #1 to #2 exclusive.`#1 < x < #2`|`<0 TO 5>`|

```sql
TEXT:apple..banana
my:int:[0 TO 10]
my:float:2.5..3.5
my:float:0..MAX
mt:text:[l TO "uFFFF"]
```

## Search for a single term

Single terms are tokenized before the search according to the appropriate data dictionary definition(s).

If you do not specify a field, it will search in the content and properties. This is a shortcut for searching all properties of type content. Terms can not contain a whitespace.

```sql
banana
TEXT:banana
```

Both of these queries will find any nodes with the word "banana" in any property of type `d:content`.

If the appropriate data dictionary definition(s) for the field supports both FTS and untokenized search, then FTS search will be used. FTS will include synonyms if the analyzer generates them. Terms cannot contain whitespace.

## Search for spans and positions

Spans and positions are not implemented. Positions will depend on tokenization.

Anything more detailed than one *(2) two are arbitrarily dependent on the tokenization. An identifier and pattern matching, or dual FTS and ID tokenization, might be the answer in these cases.

```sql
term[^] - start
term[$] - end
term[position]
```

These are of possible use but excluded for now. Lucene surround extensions:

```sql
and(terms etc)
99w(terms etc)
97n(terms etc)
```

## Search for term expansion

To force tokenization and term expansion, prefix the term with `~`.

For a property with both ID and FTS indexes, where the ID index is the default, force the use of the FTS index.

```sql
~running
```

## Search for wildcards

Wildcards are supported in terms, phrases, and exact phrases using `*` to match zero, one, or more characters and `?` to match a single character.

The `*` wildcard character can appear on its own and implies Google-style. The "anywhere after" wildcard pattern can be combined with the `=` prefix for identifier based pattern matching. Search will return and highlight any word that begins with the root of the word truncated by the `*` wildcard character.

The following will all find the term apple.

```sql
TEXT:app?e
TEXT:app*
TEXT:*pple
appl?
*ple
=*ple
"ap*le"
"***le"
"?????"
```

When performing a search that includes a wildcard character, it is best to wrap your search term in double quotation marks. This ensures all metadata and content are searched.
---
title: Sample Insight Zeppelin SQL
---

Using Insight Zeppelin you can create some reports with the following example SQL queries:

> **Note:** Insight Zeppelin comes with a note and example reports, see [Insight Zeppelin reports and notes]({% link insight-engine/latest/using/index.md %}).

### The number of documents in the repository

```sql
Select count(*) as Documents from alfresco
where TYPE='cm:content'
```

### The amount of storage used in the repository**

```sql
Select sum(`cm:content.size`) as `Storage Used (bytes)` from alfresco
```

### The amount of content created in the last 60 days

```sql
Select cm_created_day, count(*) from alfresco 
where cm_created >= 'NOW/DAY-60DAYS' 
group by cm_created_day
```

### The amount of new documents created by what user and for which site

```sql
Select SITE, cm_creator, count(*) as total from alfresco 
where NOT cm_creator = 'System' 
group by SITE, cm_creator order by total desc
```
