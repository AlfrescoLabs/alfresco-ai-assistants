---
title: Alfresco Search Enterprise 
---

Alfresco Content Services supports the Elasticsearch platform for searching within the repository using Alfresco Search Enterprise 4.0.

[Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html){:target="_blank"} is an open source enterprise search platform that uses the [Lucene](https://lucene.apache.org/){:target="_blank"} engine for indexing and searching. Elasticsearch is written in Java and runs as a standalone search server. The Alfresco Repository sends HTTP requests to the Elasticsearch REST API to search for content and metadata. The Alfresco Elasticsearch connector updates the cores and indexes in Elasticsearch. This consumes ActiveMQ messages produced by the Alfresco Repository when folders, documents, and permissions are created or updated in the repository.

> **Note:** The alfresco index is the only index in Elasticsearch used for searching live content. The index used for content marked as deleted (named *archive* in previous versions) is not available when using Elasticsearch.

The **Search** feature is provided by the Alfresco Repository itself which communicates with the Elasticsearch server that then performs the required format translation for queries and results. The Elasticsearch index contains all the content, metadata, and permissions for a single document, so no external Elasticsearch plugin is required.

The **Indexing** feature is provided by a Spring Boot application called Alfresco Elasticsearch connector. The application is split into two main components called **Live Indexing** and **Re-indexing**, for more see [Indexing]({% link search-enterprise/latest/admin/index.md %}#alfresco-elasticsearch-connector).

Alfresco Search Enterprise consists of the following components:

* Alfresco Content Services 23.1
* Elasticsearch 7.17.x - any version between 7.10.x and 7.17.x inclusive, is compatible. (It can be used as a standard managed service or can be installed using default configuration)
* Alfresco Elasticsearch Connector 4.0

> **Note:** Elasticsearch 7.10.2 is the last Apache2-licensed version. The Elasticsearch connector can also use [Amazon OpenSearch](https://aws.amazon.com/opensearch-service/the-elk-stack/what-is-opensearch/){:target="_blank"}.

The services required for Alfresco Search Enterprise are included in the following diagram.

![architecture]({% link search-enterprise/images/elasticsearch_connector_architecture.png %})

> **Note:** For a full list of features supported by Alfresco Search Services, but not yet for Alfresco Search Enterprise, see [Unsupported]({% link search-enterprise/latest/using/unsupported.md %}).
---
title: Overview
---

There are a number of processes and procedures for maintaining and administering the Search Enterprise environment.

## Pre-indexing considerations

The Exact Term search feature that allows searching using the equals operator `=`, is disabled by default to save index space.
It's possible to enable it for specific properties and property types using the `/alfresco/search/elasticsearch/config/exactTermSearch.properties` configuration file located in the Alfresco Repository.

| Property | Description |
| -------- | ----------- |
| alfresco.cross.locale.datatype.0 | A new cross locale field is added for any property of this data-type to enable exact term search. For example, {http://www.alfresco.org/model/dictionary/1.0}text. The Exact Term search is disabled by default. |
| alfresco.cross.locale.property.0 | A new cross locale field is added for the property to enable exact term search. For example, {http://www.alfresco.org/model/content/1.0}content. The Exact Term search is disabled by default. |

You can add as many data types and properties as you like by adding lines and incrementing the associated index:

```bash
alfresco.cross.locale.datatype.0={http://www.alfresco.org/model/dictionary/1.0}text
alfresco.cross.locale.datatype.1={http://www.alfresco.org/model/dictionary/1.0}content
alfresco.cross.locale.datatype.2={http://www.alfresco.org/model/dictionary/1.0}mltext
alfresco.cross.locale.property.0={http://www.alfresco.org/model/content/1.0}content
```

To overwrite this configuration when using Docker compose you can mount this file as an external volume. The following sample describes a local configuration to be applied to the Elasticsearch Search Subsystem when using Docker compose:

```yml
services:
  alfresco:
    volumes:
      - ./exactTermSearch.properties:/usr/local/tomcat/webapps/alfresco/WEB-INF/classes/alfresco/search/elasticsearch/config/exactTermSearch.properties
```

> **Note:** Once complete you must perform a re-index. It is recommended you enable the exact term feature before you start creating an index.

You can also add these environment variables directly to the Alfresco `JAVA_OPTS` section of your Docker compose file.

```yml
services:
    alfresco:
        image: quay.io/alfresco/alfresco-content-repository:23.1.0
        mem_limit: 1900m
        environment:
            JAVA_TOOL_OPTIONS: -Dencryption.keystore.type=JCEKS -Dencryption.cipherAlgorithm=DESede/CBC/PKCS5Padding -Dencryption.keyAlgorithm=DESede -Dencryption.keystore.location=/usr/local/tomcat/shared/classes/alfresco/extension/keystore/keystore -Dmetadata-keystore.password=mp6yc0UD9e -Dmetadata-keystore.aliases=metadata -Dmetadata-keystore.metadata.password=oKIWzVdEdA -Dmetadata-keystore.metadata.algorithm=DESede
            JAVA_OPTS: -Ddb.driver=org.postgresql.Driver
                ...
                -alfresco.cross.locale.datatype.0={http://www.alfresco.org/model/dictionary/1.0}text
                -alfresco.cross.locale.datatype.1={http://www.alfresco.org/model/dictionary/1.0}content
                -alfresco.cross.locale.datatype.2={http://www.alfresco.org/model/dictionary/1.0}mltext
                -alfresco.cross.locale.property.0={http://www.alfresco.org/model/content/1.0}content
                ...
```

### Mapping

When you index a document that contains a new field, Search Enterprise adds the field dynamically to the document, or to the inner objects within a document. Inner objects inherit the dynamic setting from their parent object or from the mapping type. A dynamic parameter controls whether new fields are added dynamically. The default value is `true` and should be disabled to avoid a large index, unless a large index is necessary. This can be done when you create the index, using the following command:

```bash
curl -XPUT '<Search Enterprise URL>:<port>/<index name>?pretty' -H 'Content-Type: application/json' -d'
{
  "mappings": {
        "dynamic": "false"
    }
}'
```

### Sharding

A shard is a small chunk of memory where indexed data is stored. Before you index Search Enterprise you can configure how many shards and replicas you want to use. How you configure the shards will depend on your intended data volume and the size of each shard. Here's the command to use:

```bash
curl -XPUT '<Search Enterprise URL>:<port>/<index name>?pretty' -H 'Content-Type: application/json' -d'
{
  "settings" :{
    "number_of_shards":<expected number of shards>,
    "number_of_replicas":<0 for no replica, 1 for 1 replica of each shards and so on>
  }
}
```

### Near real-time search

Per-segment searching has decreased the delay between indexing a document and when it is able to be visible to your search queries. In Search Enterprise, the lightweight process of writing and opening a new segment is called a refresh. By default, each shard is automatically refreshed every second. Using parameters you can increase the refresh rate to increase the speed of the indexing process, or you can disable it completely.

To speed up the process:

```bash
curl -XPUT "<Search Enterprise URL>:<port>/<index name>/_settings" -H 'Content-Type: application/json' -d '{ "index" : { "refresh_interval" : "60s"  }}'
```

To disable the refresh rate:

```bash
curl -XPUT "<Search Enterprise URL>:<port>/<index name>/_settings" -H 'Content-Type: application/json' -d '{ "index" : { "refresh_interval" : "-1"  }}'
```

## Alfresco Elasticsearch connector

**Indexing** is provided by a Spring boot application called the Elasticsearch connector. This application contains two main components that build and maintain the index in Elasticsearch.

* *Live Indexing*: Metadata, and Content and Permissions from Alfresco Repository are consumed using ActiveMQ messages so they can be indexed in the Elasticsearch server. The information created and updated in the Alfresco Repository is not immediately available in Elasticsearch, because it takes time to process the messages coming from the Alfresco Repository. The previous [Eventual consistency]({% link search-services/latest/install/index.md %}#eventual-consistency) approach, based on transactions and used for Solr deployments, has been replaced by this new approach based on ActiveMQ messages.

* *Re-indexing*: Indexing the information of a pre-populated Alfresco Repository or catching up with Alfresco Repositories that have missed some ActiveMQ messages is provided by the re-indexing component. Metadata and Permissions from the Alfresco Repository is retrieved using a direct JDBC connection to the Alfresco Database. The re-indexing application also generates content indexing messages in ActiveMQ in order to get the content indexed. It may take some time to process all these requests after the re-indexing application has finished.

### New Repository

When creating a new Alfresco Repository you must use the Elasticsearch connector applications in the following sequence:

1. Start the Content Services Stack, including the Elasticsearch connector live indexing services, and the Elasticsearch server.
2. Configure the Elasticsearch connector re-indexing app to point to the database, the Elasticsearch server, and the ActiveMQ server.
3. Run the re-indexing app from the command line replacing the connection details as appropriate:

```java
$ java -jar alfresco-elasticsearch-reindexing-4.0.0-app.jar \
--alfresco.reindex.jobName=reindexByIds \
--spring.elasticsearch.rest.uris=http://localhost:9200 \
--spring.datasource.url=jdbc:postgresql://localhost:5432/alfresco \
--spring.datasource.username=alfresco \
--spring.datasource.password=alfresco \
--spring.activemq.broker-url=tcp://localhost:61616?jms.useAsyncSend=true \
--alfresco.reindex.prefixes-file=file:reindex.prefixes-file.json
```

When completed successfully you will see:  

```text
o.s.batch.core.step.AbstractStep         : Step: [reindexByIdsStep] executed in 4s952ms
o.a.r.w.ElasticsearchRepoEventItemWriter : Total indexed documents:: 845
o.a.r.listeners.JobLifecycleListener     : Current Status: COMPLETED
```

Once the command has completed, metadata and permissions from the out-of-the-box repository nodes are indexed in the Elasticsearch server. Additionally, the Elasticsearch connector live indexer will add existing content, the new metadata, permissions, and new content when nodes are created, updated or deleted.

### Existing Repository

When using a pre-populated Alfresco Repository, use the Elasticsearch connector applications in the following sequence:

1. Ensure the Content Services Stack with SOLR, which is configured as the search subsystem, is running.
2. Start the Elasticsearch server.
3. Configure the Elasticsearch connector re-indexing app to point to the database, the Elasticsearch server, and the ActiveMQ server.
4. Run the re-indexing app and replace the connection details as appropriate:

```java
$ java -jar alfresco-elasticsearch-reindexing-4.0.0-app.jar \
--alfresco.reindex.jobName=reindexByIds \
--spring.elasticsearch.rest.uris=http://localhost:9200 \
--spring.datasource.url=jdbc:postgresql://localhost:5432/alfresco \
--spring.datasource.username=alfresco \
--spring.datasource.password=alfresco \
--spring.activemq.broker-url=tcp://localhost:61616?jms.useAsyncSend=true \
--alfresco.reindex.prefixes-file=file:reindex.prefixes-file.json
```

When completed successfully you will see:

```text
o.a.r.w.ElasticsearchRepoEventItemWriter : Total indexed documents:: 80845
o.a.r.listeners.JobLifecycleListener     : Current Status: COMPLETED
```

Once the command has completed, metadata from any existing Repository nodes will be indexed in the Elasticsearch server. Additionally, the Elasticsearch connector live indexer will add existing content, which may take a while. Ensure ActiveMQ is available until all the content transformation request messages have been processed. Then change the Alfresco Repository configuration to use the Elasticsearch as the search subsystem and then re-start the Repository.

> **Note:** To ensure all the content transformation requests have been processed the ActiveMQ Web Console should be used. By default, the Web Console is available at `http://127.0.0.1:8161` and accessed using default credentials. Any queues related to content transformation, usually through `acs-repo-transform-request`, should not have any pending messages.

### Partial Indexing

Over time some data may not be indexed correctly. This can be caused by prolonged network connectivity issues. The re-indexing application provides two strategies to fill the gaps in the Elasticsearch index:

* Fetch by IDS (`alfresco.reindex.jobName=reindexByIds`): index nodes in an interval of database `ALF_NODE.id` column.
* Fetch by DATE (`alfresco.reindex.jobName=reindexByDate`): index nodes in an interval of database `ALF_TRANSACTION.commit_time_ms` column.

#### Ids Range

The following sample re-indexes all the nodes in the Alfresco Repository which have an `ALF_NODE.id` value between `1` and `10000`.

```java
java -jar target/alfresco-elasticsearch-reindexing-4.0.0-app.jar \
  --alfresco.reindex.jobName=reindexByIds \
  --alfresco.reindex.pagesize=100 \
  --alfresco.reindex.batchSize=100  \
  --alfresco.reindex.fromId=1 \
  --alfresco.reindex.toId=10000 \
  --alfresco.reindex.concurrentProcessors=2
```

#### Date Range

The following sample re-indexes all the nodes in the Alfresco Repository which have a value for `ALF_TRANSACTION.commit_time_ms` between `202001010000` and `202104180000`. Date time values are written in the format `yyyyMMddHHmm`.

```java
 java -jar target/alfresco-elasticsearch-reindexing-4.0.0-app.jar \
  --alfresco.reindex.jobName=reindexByDate \
  --alfresco.reindex.pagesize=100 \
  --alfresco.reindex.batchSize=100  \
  --alfresco.reindex.concurrentProcessors=6 \
  --alfresco.reindex.fromTime=202001010000 \
  --alfresco.reindex.toTime=202104180000
```

## Deploying at Scale

This section describes how to run Search Enterprise at scale. Recommendations are based on testing carried out against a 50 million node repository.

The following services are required:

* Alfresco Content Repository deployed as a Tomcat server using the `alfresco.war` application.
* Alfresco Database to store metadata and other relevant information for the content repository.
* Alfresco Transform Service deployed as a Spring boot application with several transformation services (ImageMagick, LibreOffice, PDF Renderer and LibreOffice).
* Alfresco Shared File store deployed as a Spring boot application to serve transformed files by the Transform Service.
* Alfresco Elasticsearch Connector deployed as a Spring boot application with several indexing services, mediation, metadata, and content.
* Alfresco ActiveMQ which is message-oriented middleware and shares messages between the content repository, the Elasticsearch connector and the Transform Service.
* Elasticsearch server.

### Identifying critical paths

To identify the services used for the different features provided by Search Enterprise the following critical paths should be reviewed:

* Indexing metadata and permissions
* Indexing content
* Searching metadata and content

![flows]({% link search-enterprise/images/elasticsearch_flows.png %})

#### Metadata and Permissions

Each time a node is created or updated in the content repository, new messages with metadata and permissions are sent to ActiveMQ. The Elasticsearch connector consumes these messages and sends the indexing requests to the Elasticsearch server.

#### Content

Every time a content node is created or updated in the content repository, new messages are sent to ActiveMQ. The Elasticsearch connector consumes these messages from ActiveMQ and creates new transformation messages back into ActiveMQ. The Content Repository consumes the transformation messages and offloads the transformation of documents into plain text to the Transform Service. Once the transformation has been performed, the content repository produces a transformation complete message in ActiveMQ and uploads the plain text file to a Shared File store. The Elasticsearch connector consumes these messages and downloads the extracted text from the Shared File store. Then the text in the document is sent for indexing to the Elasticsearch server.

#### Searching metadata and content

Searching operations are handled by the content repository REST API. Depending on the search syntax used (only AFTS is currently supported), the content repository translates the search query to the Elasticsearch REST API language and sends the search request to Elasticsearch.

### Metadata indexing performance

A misconfigured or deployed system can result in a significant delay between the time when documents are created or updated in the content repository and when they appear in the search results (indexed in the Elasticsearch server).

The following information describes how to identify bottlenecks in the system's performance. It also gives recommendations on how to mitigate those bottlenecks when only indexing metadata.

#### Alfresco Repository

When the content repository is updating the database the document's metadata in the database sends messages to the ActiveMQ topic `alfresco.repo.event2`. The rate of created or updated documents depends on the content repository cluster performance.

Recommendations:

* Increase resources for the server if CPU load or memory consumption is high.
* Increase database pool if no connections are available.
* Increase the number of threads if no threads are available.
* Increase the number of content repository nodes in the cluster.

#### Database

The database is updated to create new nodes or to modify existing ones. Additionally, the queries are executed in the database to populate metadata for returned entities in the REST API responses for search queries. These operations are mainly related to `ALF_NODE` and `ALF_NODE_PROPERTIES` tables.

Recommendations:

* Increase resources for the server if CPU load or memory consumption is high.
* Regularly update statistics for `ALF_NODE` and `ALF_NODE_PROPERTIES` tables to optimise query planner performance.

#### Elasticsearch connector

This service consumes messages from the ActiveMQ topic `alfresco.repo.event2` and produces or consumes ActiveMQ messages from the queue `metadata.event`.

Recommendations:

* Always use a pool of connections to ActiveMQ (`spring.activemq.pool.enabled` set to `true` with `spring.activemq.pool.max-connections` sized).
* Increase the number of consumers for the `live-indexing-mediation` component if the messages enqueued count is significantly greater than messages dequeued for the ActiveMQ topic `alfresco.repo.event2`.
* Increase the number of consumers for the `live-indexing-metadata` component if the messages enqueued count is significantly greater than messages dequeued for the ActiveMQ queue `metadata.event`.

#### ActiveMQ

ActiveMQ transports messages from the content repository and the Elasticsearch connector. It also communicates between the content repository and the Transform Service communication.

Recommendations:

* Increase resources for the server if CPU load or memory consumption is high.

#### Elasticsearch server

The Elasticsearch server gets indexing requests from the Elasticsearch connector. If all other services are working as expected, an increment in messages enqueued without the dequeuing operation for queue `metadata.event` may indicate the Elasticsearch server requires more resources. Slow responses for a search query can also indicate insufficient resources for the server.

Recommendations:

* Increase resources for the server if CPU load or memory consumption is high.
* Increase resources for the server if ingestion rate is decreasing with higher volumes of data.

### Permissions indexing performance

#### Alfresco Repository

Recommendations:

* Increase resources for the server if CPU load or memory consumption is high.
* Increase database pool if no connections are available.
* Increase the number of threads if no threads are available.
* Increase the number of content repository nodes in the cluster.

### Content indexing performance

#### Alfresco Repository

Recommendations:

* Increasing the number of concurrent consumers for the ActiveMQ queue `acs-repo-transform-request`, can lead to missed content transformations. If you keep this value below `10` all the documents will be transformed.

#### Elasticsearch connector

Recommendations:

* Increase the timeout used to contact the Shared file store via HTTP, you set the value in `alfresco.sharedFileStore.timeout`. This helps to avoid issues when the Shared File store response is slower than usual under a large load.
* Increase the content retry delay used to retrieve content from the Shared File store, you set the value in `alfresco.content.event.retry.delay`. This helps when you are uploading a large document into the system.
* Select the correct configuration for the Shared File store content age scheduler. If you have disk space issues you can reduce it. You must consider you may find unexpected exceptions with a content reinsert request.

### Searching performance

The Elasticsearch connector uses an out-of-the-box Elasticsearch server, for more see [Tune for search speed](https://www.elastic.co/guide/en/elasticsearch/reference/master/tune-for-search-speed.html){:target="_blank"}.

### Re-indexing

The Re-indexing app has been tested on reading replicas with a Postgres database. Tests have been performed on the local environment and AWS. To run database read replicas in AWS follow these guidelines [AWS read replicas](https://aws.amazon.com/rds/features/read-replicas){:target="_blank"}.

For using the read replica in the re-indexing phase, configure the reindexing component for targeting the correct read replica:

```bash
spring.datasource.url=jdbc:postgresql://<READ_REPLICA_ADDRESS>:<READ_REPLICA_PORT>/alfresco
```

### Re-index using remote partitioning

It can take a large amount of time when re-indexing a large Alfresco Repository instance using a single re-index process. You can scale the re-index node vertically to improve performance, but this may also not enough. Using [remote partitioning](https://docs.spring.io/spring-batch/docs/current/reference/html/scalability.html#partitioning){:target="_blank"}, and a Spring Batch feature, you can scale horizontally the Re-indexing service.

```text
 ┌─────────────────────────┐                             ┌────────────────┐
 │         Manager         │                             │    Worker 1    │
 │                         │   Produce     ┌────────────►│                ├───┐
 │                         │   partition   │             │* Read partition│   │
 │ * DB Schema Validation  │   requests┌───┴──────┐      │* Index nodes   │   │
 │                         ├──────────►│ ActiveMQ │      └──────┬─────────┘   │
 │ * Partition creation    │◀──────────┤          │ ◀───────────┘             │
 │                         │           └───┬──────┘                           │
 │                         │   Consumes    │ ▲                                │
 │                         │   workers     │ │                                │
 │                         │   replies     │ │                                │
 │                         │               │ │                                │
 │                         │               │ │                                │
 │                         │               │ │                                │
 │                         │               │ │           ┌────────────────┐   │
 └───────────┬─────────────┘               │ └───────────┤    Worker n    │   │
             │                             │             │                │   │
             │                             └────────────►│* Read partition│   │
             │                                           │* Index nodes   │   │
             │                                           └────────┬───────┘   │
             │           ┌────────────┐                           │           │
             │           │ Shared     │◄──────────────────────────┘           │
             └──────────►│ Database   │                                       │
                         │            │◄──────────────────────────────────────┘           
                         └────────────┘
```

This solution requires a manager node that executes verification steps, like database schema validation, and creates partitions and multiple worker nodes that index the partition. The manager sends partitions to the worker using ActiveMQ.

To use this feature you need to run a manager node and at least a worker node. To scale up the system you can increase the number of worker nodes by setting the property `alfresco.reindex.partitioning.grid-size`. The number of worker nodes usually equals the grid size, but if it is more a worker will consume multiple partitions.

The system will automatically select the partition strategy depending on the job name, currently there is:

* Partition by id range
* Partition by date range

Both strategies split the specified range into multiple ranges depending on the grid size.

_Manager_:

```shell
java -jar alfresco-elasticsearch-reindexing-4.0.1-app.jar \
  --alfresco.reindex.jobName=reindexByIds \
  --alfresco.reindex.partitioning.type=manager \
  --alfresco.reindex.pagesize=100 \
  --alfresco.reindex.batchSize=100  \
  --alfresco.reindex.fromId=0 \
  --alfresco.reindex.toId=10000 \
  --spring.batch.datasource.url=jdbc:postgresql://<IP address of host>:<port number>/alfresco \
  --spring.batch.datasource.username=alfresco \
  --spring.batch.datasource.password=alfresco \
  --spring.batch.datasource.driver-class-name=org.postgresql.Driver \
  --spring.batch.drop.script=classpath:/org/springframework/batch/core/schema-drop-postgresql.sql \
  --spring.batch.schema.script=classpath:/org/springframework/batch/core/schema-postgresql.sql
  --spring.elasticsearch.rest.uris=http://<IP address of host>:<port number> 
  --spring.datasource.url=jdbc:postgresql://<IP address of host>:<port number>/alfresco 
  --spring.datasource.username=alfresco 
  --spring.datasource.password=alfresco 
  --spring.activemq.broker-url=tcp://localhost:<port number>
```

_Worker_:

```shell
java -jar alfresco-elasticsearch-reindexing-4.0.0-app.jar \
  --alfresco.reindex.partitioning.type=worker \
  --alfresco.reindex.pagesize=100 \
  --alfresco.reindex.batchSize=100 \
  --alfresco.reindex.concurrentProcessors=2 \
  --spring.batch.datasource.url=jdbc:postgresql://localhost:5432/alfresco \
  --spring.batch.datasource.username=springBatchUser \
  --spring.batch.datasource.password=****** \
  --spring.batch.datasource.driver-class-name=org.postgresql.Driver \
  --spring.batch.drop.script=classpath:/org/springframework/batch/core/schema-drop-postgresql.sql \
  --spring.batch.schema.script=classpath:/org/springframework/batch/core/schema-postgresql.sql
```

You don't need to specify a job name for the worker because the configuration to use it is in the manager step context. This also means that you don't need to restart a worker if the job name specified in the manager configuration changes.

The worker will not stop automatically because it is always up and running in order to wait for the new partition to index.
The manager will automatically stop when all partitions have been indexed.

#### Batch Job Store DB

When using remote partitioning you are required to use a shared database that is accessible from all nodes. The database will contain the Batch job store. Spring batch will automatically create required tables, and those tables don't contain sensitive data, so you can wipe them when required and you don't need to back them up. It is recommended you use a unique database user to read the partition, and for managing the Spring batch. A list of supported databases can be retrieved, for more see [Enum DatabaseType
](https://docs.spring.io/spring-batch/docs/current/api/org/springframework/batch/support/DatabaseType.html){:target="_blank"}, and all available SQL initialization scripts are available, for more see [spring-batch](https://github.com/spring-projects/spring-batch/tree/main/spring-batch-core/src/main/resources/org/springframework/batch/core){:target="_blank"}.

When using a different database you need to add to the Java classpath and to the right connection driver. The Re-indexing service is a Spring boot application which means you can't add the JAR to the classpath, but instead you need to use a different command, for example:

```shell
 java -cp alfresco-elasticsearch-reindexing-4.0.0-app.jar:mysql-connector-java-8.0.25.jar
   -Dloader.main=org.alfresco.reindexing.ReindexingApp org.springframework.boot.loader.PropertiesLauncher
   --alfresco.reindex.jobName=reindexByIds
   --alfresco.reindex.partitioning.type=manager
   --alfresco.reindex.fromId=0
   --alfresco.reindex.toId=10000
   --spring.batch.datasource.url=jdbc:mysql://localhost:3306/alfresco
   --spring.batch.datasource.username=batchUser
   --spring.datasource.username=batchUser
   --spring.batch.datasource.password=*****
   --spring.datasource.password=*****
   --spring.batch.datasource.driver-class-name=com.mysql.jdbc.Driver
   --spring.datasource.driver-class-name=com.mysql.jdbc.Driver
   --spring.batch.drop.script=classpath:/org/springframework/batch/core/schema-drop-mysql.sql
   --spring.batch.schema.script=classpath:/org/springframework/batch/core/schema-mysql.sql
```

From version 3.3.x you can use a different database, for more see [Support for different databases]({% link search-enterprise/latest/config/index.md %}#support-for-different-databases).

#### Failures handling

If the manager** fails or a worker fails you can check which partitions were indexed in the log and launch them again by restarting the Re-indexing service.

#### Partition definition

The Re-indexing service creates partitions but only partitions the interval between the specified range, it is necessary to select the right range in order to avoid empty partitions. For instance, you can select the min and max values from the Alfresco database and then use those values in the configuration properties.

When re-indexing by ID range you can retrieve min and max values by executing the query below and using them for `alfresco.reindex.fromId` and `alfresco.reindex.toId`:

```sql
select min(id) as fromId, max(id) as toId from alf_node;
```

When re-indexing by date range you can retrieve min and max values by executing the query below and using them for `alfresco.reindex.fromTime` and `alfresco.reindex.toTime`:

```sql
select to_char(to_timestamp(min(commit_time_ms)/1000),'YYYYMMDDHHMI') as fromTime, to_char(to_timestamp(max(commit_time_ms)/1000),'YYYYMMDDHHMI') as toTime from alf_transaction;
```

It is easier to have unbalanced partitions when indexing by date range. Due to this it is recommended you use this strategy only when you are interested in indexing a specific date range. It is only recommended to perform a reindex by id range when you need to perform a full re-index.

## Indexing only metadata

The Re-indexing application may be used to index only metadata. You can also exclude the content indexation from the process.

To apply this configuration, set the parameter `alfresco.reindex.contentIndexingEnabled` to `false`:

```shell
java -jar alfresco-elasticsearch-reindexing-4.0.0-app.jar \
    --alfresco.reindex.contentIndexingEnabled=false
```

## Indexing PATH property

By default, the re-indexing PATH property is disabled. To enable this feature, set the parameter `alfresco.reindex.pathIndexingEnabled` to `true`.

```shell
java -jar alfresco-elasticsearch-reindexing-4.0.0-app.jar \
    --alfresco.reindex.pathIndexingEnabled=true
```

## Enabling and disabling re-indexing features recommendations

By default the re-indexing application uses the following configuration:

* `alfresco.reindex.metadataIndexingEnabled=true`
* `alfresco.reindex.contentIndexingEnabled=true`
* `alfresco.reindex.pathIndexingEnabled=false`

The re-indexing metadata process also indexes permissions associated with the document. This means when disabling metadata re-indexing,  the content and path will not be updated for non-indexed documents. Only indexed documents will be updated with content and path.

The main use case to re-index only content or path is a fully metadata indexed repository that needs to update / complete the content or path.

## Bulk metadata indexing

You can customize Search Enterprise by having the index ready with just the metadata of uploaded files or with the content of the files as well. If you have the content of your files indexed there are time and cost implications you must consider and it is only recommended when necessary.
This example describes how to set up Search Enterprise to show the speed achievable when processing one billion files. Amazon Web Services have been used as the host but your setup will be specific to your requirements.

The configuration used in this example:

**Search Enterprise Data Node**

* AWS Elasticsearch `7.10` with Availability Zone: `1-AZ`.
* Number of Data Nodes: `3`.
* Instance Type: `r6g.2xlarge.search`.
* Storage type: EBS.
* EBS volume type: Provisioned IOPS (SSD).
* EBS volume size: `1000GB` per node.
* Fielddata cache allocation: `20`.
* Max clause count: `1024`.

**Indexing Instance**

* Amazon EC2 Indexing instance to run `alfresco-elasticsearch-connector-distribution-3.2.1`.
* Indexing Instance type: `t2.2xlarge` (8vCPUs, `32GB` RAM).
* Number of Amazon EC2 Instances for Indexing: `3`.
* Number of threads running on instance 1 and 2 is `7` each with `6` threads on instance 3. Total threads running in parallel is `20`.
* Maximum Heap allocated to each thread is `4GB` (`-Xmx4G`).

**Search Enterprise Master Node**

* Number of Master Nodes: `3`.
* Master Node instance type: `m5.large.search`.
* Master node is added for resilience, and can be avoided without having significant impact.

**Search Enterprise Settings**

* Number of Primary shards: `32`.
* Number of Replica shards: `0`.
* Refresh time: Disabled.
* Translog flush threshold: `2GB`

**Other Components**

* Active MQ: `mq.m4.large`.
* RDS is used as the Database with `db.r5.2xlarge` running PostgreSQL.
* Amazon EC2 Instance running Content Services and the Transform Service: `m5a.xlarge`
* Content Services: `7.2.0`.

The deployment architecture of the system:

![architecture]({% link search-enterprise/images/database-configuration.png %})

### Configure Search Enterprise

Amazon Web Services recommend each shard should be not more than `50GB`. For this example of one billion files the estimated total size of metadata to be indexed is `1.3TB`. The shard size here can be set to `40GB` which equals 32 shards.

On the same VPC set the number of shards:

```curl
curl -XPUT 'https://<Elasticsearch DNS>:443/alfresco?pretty' -H 'Content-Type: application/json' -d'
{
  "settings" :{
        "number_of_shards":32,
        "number_of_replicas":0
  }
}'
```

You can set other critical parameters such as the refresh interval and the translog flush threshold using curl. The refresh interval is the time in which indexed data is searchable and should be disabled. This is done by setting it to `-1` or by setting it to a higher value during indexing to avoid the unnecessary usage of resources. The translog flush threshold is set to a higher size, for example `2GB`, to avoid it periodically flushing during the indexing process.

To set the refresh interval to `-1` to disable it:

```curl
curl -XPUT "https://<Elasticsearch DNS>:443/alfresco/_settings" -H 'Content-Type: application/json' -d '{ "index" : { "refresh_interval" : "-1"  }}'
```

To set the translog flush threshold to `2GB`:

```curl
curl -XPUT "https://<Elasticsearch DNS>:443/alfresco/_settings?pretty" -H 'Content-Type: application/json' -d '{"index":{"translog.flush_threshold_size" : "2GB"}}'
```

To verify the settings:

```curl
curl -XGET "https://<Elasticsearch DNS>:443/alfresco/_settings?pretty" -H 'Content-Type: application/json' -d '{ "index" : { "refresh_interval" }}'
```

To setup the Re-Indexing Instance:

1. Deploy three Amazon EC2 instances in the same VPC as all the other services.

2. Attach the Amazon EC2 instances to a security group that allows all incoming traffic from the other services.

3. Install Java 17 on all three instances.

4. Copy `alfresco-elasticsearch-connector-distribution-3.2.1` to the three Amazon EC2 instances.

   Run `7` threads on each of the two instances and `6` on the third instance to achieve a total of `20` thread count.

5. In a command prompt on the VPC `cd` to where `alfresco-elasticsearch-reindexing-3.1.1-app.jar` is located.

6. Run the following Indexing command with your specific configuration, where:

    * `server.port` - a unique port number to run the required number of threads needed for an instance. For example, to run 7 threads from instance one, you must copy the code 7 times and provide a unique port in each of the 7 sets of commands.
    * `alfresco.reindex.fromId` and `alfresco.reindex.toId` - a unique `nodeID` for each thread. You can equally distribute the total file count among the threads. In this example, 1B among 20 threads with each thread receiving 50 million each. For example:
        * For Thread 1: `alfresco.reindex.fromId=0` and `alfresco.reindex.toId=50000000`
        * For Thread 2: `alfresco.reindex.fromId=50000001` and `alfresco.reindex.toId=100000000`
        * For Thread 3: `alfresco.reindex.fromId=100000001` and `alfresco.reindex.toId=150000000`
        * For Thread 20: `alfresco.reindex.fromId=950000001` and `alfresco.reindex.toId=1000000000`

Indexing Command:

```java
nohup java -Xmx4G -jar alfresco-elasticsearch-reindexing-3.2.1-app.jar \
--server.port=<unique port> \
--alfresco.reindex.jobName=reindexByIds \
--spring.elasticsearch.rest.uris=https://<Elasticsearch DNS>:443 \
--spring.datasource.url=jdbc:postgresql://<DB Writer URL>:5432/alfresco \
--spring.datasource.username=**** \
--spring.datasource.password=**** \
--alfresco.accepted-content-media-types-cache.enabled=false \
--spring.activemq.broker-url=failover:\(ssl://<Broker 1>:61617,ssl://<Broker 2>:61617\) \
--spring.activemq.user=alfresco \
--spring.activemq.password=***** \
--alfresco.reindex.fromId=0 \
--alfresco.reindex.toId=50000000 \
--alfresco.reindex.multithreadedStepEnabled=true \
--alfresco.reindex.concurrentProcessors=30 \
--alfresco.reindex.metadataIndexingEnabled=true \
--alfresco.reindex.contentIndexingEnabled=false \
--alfresco.reindex.pathIndexingEnabled=true \
--alfresco.reindex.pagesize=10000 \
--alfresco.reindex.batchSize=1000  &
Indexing Speed
```

The table summarizes different indexing capabilities obtained with different data volumes but with identical infrastructure and configuration as outlined above.

![statistics]({% link search-enterprise/images/database-statistics.png %})

## Search Enterprise Healthcheck

The Healthcheck allows you to check the status of the Search Enterprise index by sampling a configurable number of nodes. It does this by comparing the latest update for these nodes with the latest update for the equivalent database record. If these do not match, within a configurable tolerance, an error is reported. If you have nodes that have failed to index the Healthcheck provides a way of reindexing them.
The Healthcheck can be run nightly to ensure that any updates in the last 24 hour period are up to date. Using the Healthcheck gives you confidence that all your repository content is searchable.

### Configure Healthcheck in the Repository

The Alfresco Repository includes configuration properties for the Healthcheck. The property values are included in the `alfresco-global.properties` configuration file. To use these properties you must first activate the Search Enterprise Subsystem, for more see [Configure Subsystem in Repository]({% link search-enterprise/latest/install/index.md %}#configure-subsystem-in-repository). You can also use the [JConsole]({% link content-services/latest/config/index.md %}#configure-with-jconsole) to configure the Healthcheck.  

| Property | Description |
| -------- | ----------- |
| elasticsearch.healthcheck.id.minRange | The minimum healthcheck database node ID. A node must have a database ID greater than or equal to the specified value that is included in the healthcheck. |
| elasticsearch.healthcheck.id.maxRange | The maximum healthcheck database node ID. A node must have a database ID that is less than or equal to the specified value that is included in the healthcheck. |
| elasticsearch.healthcheck.date.minRange | The minimum healthcheck database node update date. A node must have a database update date that is greater than or equal to the specified value that is included in the healthcheck. The default is `2023-01-01T23:59:00Z`. |
| elasticsearch.healthcheck.date.maxRange | The maximum healthcheck database node update date. A node must have a database update date that is less than or equal to the specified value that is included in the healthcheck. The default is `2023-01-07T23:59:00Z`. |
| elasticsearch.healthcheck.batchSize | The number of nodes aggregated from the database to be checked in Search Enterprise in one go. The property cannot be greater than `10000`. The default is `10000` |
| elasticsearch.healthcheck.confidenceThresholdInMs | A threshold value in milliseconds that can be used to help you avoid false positives. It can be used in cases where the timestamp difference between the database and Search Enterprise is below the threshold. An example of this is when you are managing out of order events, or in circumstances where you have expected delays in indexing. The default is `1000`. |
| elasticsearch.healthcheck.pollingRatio | The distance between nodes to check. For example, if you set this property  to `10`, then every 10th node within the configured range is checked. The default is `1`. |
| elasticsearch.healthcheck.timeoutInHours | The number of hours the healthcheck is allowed to run. If the time out is exceeded, the healthcheck is stopped and only the results found until the healthcheck is stopped will be displayed. The default is `1`. |
| elasticsearch.healthcheck.startTime | The scheduled time to automatically start the healthcheck. The default is `2030-12-30T23:59:00Z`. |
| elasticsearch.healthcheck.intervalPeriod | The period of time the healthcheck should wait between repeated executions after the first scheduled execution. The possible values are: `Month`, `Week`, `Day`, `Hour`, `Minute`, or `Second`. The default is `Week`. |
| elasticsearch.healthcheck.intervalCount | Sets how many periods should be waited between each scheduled execution. The default is `1`. |
| elasticsearch.healthcheck.nodeAspectsToExclude | A comma-separated list of node aspects. Nodes with any of the aspects from the specified list will be excluded from the healthcheck. The default is `sys:hidden`. |

> **Note:** You can only set one range format, either ID or Date. This means two properties for one of the range formats must always be empty.

### Run Healthcheck Job

Use the JConsole to run the Healthcheck.

> **Note:** The MBean `Alfresco:Name=ElasticsearchHealthcheck` is exposed and allows you to manage the Healthcheck.

1. Open a command prompt and `cd` to your JDK installation directory.

2. Open the Java Monitoring & Management Console window by entering: `jconsole`.

3. Double click the **Alfresco Content Services Java** process.

    The JConsole connects to the managed bean, or MBean server hosting the subsystems.
    For Tomcat, the Java process is labelled: `org.apache.catalina.startup.Bootstrap start`.

4. Select the **MBeans** tab.

    The available managed beans are displayed in the console.

5. Navigate to **Alfresco** > **ElasticsearchHealthcheck** > **Operations**.

6. Select one of the following:

  * `triggerHealthcheckJobs()` - run Healthcheck immediately.
  * `scheduleHealthcheckJob()` - schedule a healthcheck job, according to the `elasticsearch.healthcheck.startTime` and `elasticsearch.healthcheck.intervalPeriod` properties.
  * `unscheduleHealthcheckJob()` - unschedule a Healthcheck job.

### The Healthcheck Job results

1. Open the Admin Console, for more see [Launch Admin Console]({% link content-services/latest/admin/admin-console.md %}#launch-admin-console).

2. In the **Repository Services** section, click **Search Service**.

3. Select the **Service Status** tab.

![health]({% link search-enterprise/images/health-check.png %})

The **Service Status** tab gives information on the status of the latest Healthcheck execution, latest healthcheck settings, and scheduled healthcheck settings. At the bottom of the page there is a list of the latest Healthcheck events sorted by date. You can see ranges of nodes where discrepancies in the indexing were found. This means the range starts immediately after the previous correctly indexed node and finishes immediately before the first next correctly indexed node. You can also see the number of issues found within each range.

### Logging

You will see a similar output if the Healthcheck has completed and some issues were found:

`2023-10-11 12:57:15 2023-10-11T10:57:15,693 [] INFO  [validator.job.ElasticsearchValidationActionExecutor] [pool-14-thread-1] The Elasticsearch healthcheck job finished with 642 issues in 2 ranges.`

You will see a similar output if the Healthcheck is completed without any issues being found:

`2023-10-11 11:40:01 2023-10-11T09:40:01,786 [] INFO  [validator.job.ElasticsearchValidationActionExecutor] [pool-16-thread-1] The Elasticsearch healthcheck job finished with no issues.`

You can obtain detailed logs for the Healthcheck that provide all ranges of information to do with any issues according to the current Healthcheck execution. You do this by activating the TRACE level for the `org.alfresco.repo.search.impl.elasticsearch.admin.validator.job.ElasticsearchValidationActionExecutor` class, for more see [Set log levels]({% link content-services/latest/admin/troubleshoot.md %}#set-log-levels).

You will see a similar output:

```text
2023-10-11 12:57:15 2023-10-11T10:57:15,548 [] DEBUG [validator.job.ElasticsearchValidationActionExecutor] [pool-14-thread-1] The Elasticsearch healthcheck job started.
2023-10-11 12:57:15 2023-10-11T10:57:15,690 [] TRACE [validator.job.ElasticsearchValidationActionExecutor] [pool-14-thread-1] The Elasticsearch healthcheck job found 638 discrepancies in date range (2023-10-11T10:50:02.124Z, 2023-10-11T10:50:28.395Z)
2023-10-11 12:57:15 2023-10-11T10:57:15,690 [] TRACE [validator.job.ElasticsearchValidationActionExecutor] [pool-14-thread-1] The Elasticsearch healthcheck job found 4 discrepancies in date range (2023-10-11T10:56:10.164Z, 2023-10-11T10:57:15.519Z)
2023-10-11 12:57:15 2023-10-11T10:57:15,693 [] INFO  [validator.job.ElasticsearchValidationActionExecutor] [pool-14-thread-1] The Elasticsearch healthcheck job finished with 642 issues in 2 ranges.
```
---
title: Overview
---

Use the following information to configure Search Enterprise.

The Admin console is used to manage the interaction between Alfresco and Search Enterprise from the Alfresco Repository. This gives you the ability to determine the high-level health of the Search Enterprise index.

To use Search Enterprise with the Alfresco Content Services platform the following configuration must be applied:

* For *searching* features the Alfresco Repository properties must be configured in the `alfresco-global.properties` file. This can also be done as an environment variable by configuring the Search Subsystem.
* The Elasticsearch connector environment variables related to communication with the Alfresco Repository (Database, ActiveMQ and Transform Service) must be set and the Elasticsearch server for *indexing* features.

> **Note:** To ensure backward compatibility, the exact same property values are used for configuring connection to the Opensearch Search subsystem (*'elasticsearch'* prefixes and aliases shall not change).

## Alfresco Repository

Alfresco Repository provides configuration properties for the Elasticsearch Search subsystem that defines the connection to the external Elasticsearch server, for more see [Subsystem]({% link search-enterprise/latest/install/index.md %}#configure-subsystem-in-repository).

Additional property values can be included in the global configuration file `alfresco-global.properties`

|Property|Description|
|--------|-----------|
| elasticsearch.host | Name of the Elasticsearch server. The default value is `localhost`. |
| elasticsearch.port | Port of the Elasticsearch server. The default value is `9200`. |
| elasticsearch.baseUrl | Context path for the Elasticsearch server endpoint. |
| elasticsearch.secureComms | Set secure communications for requests to the Elasticsearch server. When you set this value to `https`, adding the Elasticsearch Trusted CA certificate to Alfresco Repository Truststore is required. Once this done communication with the Elasticsearch server is managed with the HTTPS protocol. When you set this value to `none`, communication to the Elasticsearch server is managed with the HTTP protocol. |
| elasticsearch.ssl.host.name.verification | When using the HTTPS protocol, this property controls the Elasticsearch server TLS certificate and includes a CN with the real DNS hostname. To use the property set the value to be `true`, to ignore the property set the value to `false`. The default value is `false`. |
| elasticsearch.user | Username for Elasticsearch server. It is left empty by default. |
| elasticsearch.password | Password for Elasticsearch server. It is left empty by default. |
| elasticsearch.max.total.connections | Maximum number of HTTP(s) connections allowed for the Elasticsearch server. The default value is `30`. |
| elasticsearch.max.host.connections | Maximum number of HTTP(s) connections allowed for an Elasticsearch endpoint. The default value is `30`. |
| elasticsearch.http.socket.timeout | Maximum timeout in milliseconds to wait for a socket response. The default value is `30000`. |
| elasticsearch.http.connection.timeout | Maximum timeout in milliseconds to wait for a socket connection. The default value is `1000`. |
| elasticsearch.indexName | Name of the index to be used in the Elasticsearch server. The default value is `alfresco`. |
| elasticsearch.createIndexIfNotExists | An Index is created in the Elasticsearch server when this value is set to `true`. The default value is `false`. |
| elasticsearch.retryPeriodSeconds | Number of seconds to wait before retrying the Elasticsearch index initialization. The default value is `10`. |
| elasticsearch.retryAttempts | Number of attempts to try Elasticsearch index initialization. The default value is `3`. |
| elasticsearch.lockRetryPeriodSeconds | Number of seconds to wait before retrying the Elasticsearch index initialization in lock mode. The default value is `10`. |
| elasticsearch.query.includeGroupsForRoleAdmin | Include groups for Role Admin in permission filters when this value is set to `true`. The default value is `false`. |
| elasticsearch.index.mapping.total_fields.limit | Mapping limit settings: The maximum number of fields in Alfresco index. When working on deployments including a large collection of custom content models, this value may be increased, but it is not recommended. The default value is `7500`. |
| elasticsearch.index.max_result_window | Maximum number of results that can be returned by a single query. The default value is `10000`. |
| elasticsearch.io.threadCount | Number of I/O Dispatcher threads to be used by the underlying Elasticsearch REST client. This number must be greater than zero, otherwise the default value will be used. The default value is `java.lang.Runtime.getRuntime().availableProcessors()`.<br><br> Added in Content Services 23.1.|

Some of the properties above can be edited in the Search Admin Console, but values will be applied only to the Alfresco Repository instance. To update values for the Elasticsearch connector update its property file manually. **Note:** It is important that the Elasticsearch connector and repository configuration match, otherwise the search functionality will be impaired.

Additionally, these properties can be set as environment variables in Alfresco Repository Docker Image when using Docker Compose. In the following sample, `elasticsearch.host` and `elasticsearch.createIndexIfNotExists` override the default values.

```docker
alfresco:
    image: quay.io/alfresco/alfresco-content-repository:23.1.0
    environment:
        JAVA_OPTS: "
        -Dindex.subsystem.name=elasticsearch
        -Delasticsearch.host=elasticsearch
        -Delasticsearch.createIndexIfNotExists=true
        "
```

## Alfresco Elasticsearch connector

The indexing feature is provided by a Spring Boot application called Elasticsearch connector. This application includes two main components that build and maintain the index in Elasticsearch:

* *Re-Indexing*: Indexing the information of a pre-populated Alfresco Repository or catching up with Alfresco Repositories that has missed some ActiveMQ messages is provided by the re-indexing component.

* *Live Indexing*: Metadata, and Content and Permissions from the Alfresco Repository are consumed using ActiveMQ messages so they can be indexed in the Elasticsearch server.

### Alfresco Re-indexing app

Alfresco re-indexing app requires a working Alfresco Repository Database and the Elasticsearch server.

The tool may be used as a standalone jar file. The table below lists the main configuration properties that can be specified through the Spring Boot configuration.

| Property | Description |
| -------- | ------------|  
| server.port | Default HTTP port, each module defines itself. The default value is `8190`. |
| alfresco.reindex.jobName | The data fetching strategy to use: `reindexByIds`, or `reindexByDate`. The default value is `reindexByIds`. |
| alfresco.reindex.batchSize | The batch size of documents inserted into Elasticesearch by the re-indexing app.  The default value is `100`. |
| alfresco.reindex.pagesize | The page size of nodes fetched from the Alfresco dabatase. The default value is `100`. |
| alfresco.reindex.concurrentProcessors | Number of parallel processors. The default value is `10`. |
| alfresco.reindex.fromId | Start ID for fetching nodes (_reindexByIds_). The default value is `0`. |
| alfresco.reindex.toId | End ID for fetching nodes (_reindexByIds_) is configured. The default value is `20000000000`. |
| alfresco.reindex.fromTime | Start time for fetching nodes (_reindexByDate_), pattern: yyyyMMddHHmm. The default value is `190001010000`. |
| alfresco.reindex.toTime | End time for fetching nodes (_reindexByDate_), pattern: yyyyMMddHHmm. The default value is `203012312359`. |
| spring.datasource.url | JDBC url of the Alfresco database. The default value is `jdbc:postgresql://localhost:5432/alfresco`. |
| spring.datasource.username | Username for the Alfresco database. The default value is `alfresco`. |
| spring.datasource.password | Password for the Alfresco database. The default value is `alfresco`. |
| spring.elasticsearch.rest.uris | Rest(s) url of Elasticsearch. The default value is `http://elasticsearch:9200`. |
| spring.elasticsearch.rest.username | Username for Elasticsearch when using Basic Authentication. |
| spring.elasticsearch.rest.password | Password for username in Elasticsearch when using Basic Authentication. |
| spring.activemq.broker-url | ActiveMQ Broker url, use async sending to improve performance. The default value is `tcp://localhost:61616?jms.useAsyncSend=true`. |
| spring.activemq.user | ActiveMQ Broker user. The default is `admin`. |
| spring.activemq.password | ActiveMQ Broker password. The default is `admin`. |
| alfresco.reindex.multithreadedStepEnabled | Enable steps to be executed in parallel threads. Retrying settings are only applied when this property is set to `true`. The default value is `false`. |
| alfresco.reindex.retryingEnabled | Retry the execution of a step in case of fail. The default value is `true`. |
| alfresco.reindex.retryingMaxCount | Number of times to retry the step before throwing an error. The default value is `3`. |
| alfresco.reindex.retryingInitialDelay | Waiting time before retrying the step in milliseconds. The default value is `1000`. |
| alfresco.reindex.retryingDelayIntervalMultiplier | Every try should wait N times the initial delay, where N is the number specified in this property. The default value is `2`. |
| alfresco.reindex.retryingMaxDelay | Maximum delay to be waited before executing a retry on a step. The default value is `30000`. |
| alfresco.reindex.prefixes-file | File with namespaces-prefixes mapping. The default value is `classpath:reindex.prefixes-file.json`. |
| alfresco.reindex.partitioning.type | Remote node type, can be master or worker. If not specified, the app runs as a single node instance. By default it is left empty. |
| alfresco.reindex.partitioning.grid-size | Number of partitions, usually equals the number of available workers. The default value is `3`. |
| alfresco.reindex.partitioning.requests-queue | Request queue for remote partitioning. `org.alfresco.search.reindex.requests.` |
| alfresco.reindex.partitioning.replies-queue | Reply queue for remote partitioning. `org.alfresco.search.reindex.replies`. |
| alfresco.db.minimum.schema.version | Minimum Alfresco Repository database version supported: 14002. |
| alfresco.accepted-content-media-types-cache.base-url | URL to get the list of Content Media Types supported. The default URL is `http://localhost:8090/transform/config`. |
| alfresco.accepted-content-media-types-cache.enabled | Cache the list of Content Media Types supported in memory. The default value is `true`. |
| alfresco.reindex.metadataIndexingEnabled | Re-index document metadata. The default value is `true`. |
| alfresco.reindex.contentIndexingEnabled | Re-index document content. The default value is `true`. |
| alfresco.reindex.pathIndexingEnabled | Re-index document Path property. The default value is `false`. |

There are two strategies to fill the gaps in the Elasticsearch server when provoked by ActiveMQ unavailability or any other external cause:

* Fetch by IDS `alfresco.reindex.jobName=reindexByIds`: index nodes in an interval of database `ALF_NODE.id` column
* Fetch by DATE `alfresco.reindex.jobName=reindexByDate`: index nodes in an interval of database `ALF_TRANSACTION.commit_time_ms` column

Sample invocation for Fetch by IDS.

```java
java -jar target/alfresco-elasticsearch-reindexing-4.0.0-app.jar \
  --alfresco.reindex.jobName=reindexByIds \
  --alfresco.reindex.pagesize=100 \
  --alfresco.reindex.batchSize=100  \
  --alfresco.reindex.fromId=1 \
  --alfresco.reindex.toId=10000 \
  --alfresco.reindex.concurrentProcessors=2
```

Sample invocation for Fetch by DATE.

```java
 java -jar target/alfresco-elasticsearch-reindexing-4.0.0-app.jar \
  --alfresco.reindex.jobName=reindexByDate \
  --alfresco.reindex.pagesize=100 \
  --alfresco.reindex.batchSize=100  \
  --alfresco.reindex.concurrentProcessors=6 \
  --alfresco.reindex.fromTime=202001010000 \
  --alfresco.reindex.toTime=202104180000
```

### Alfresco Live Indexing app

The Alfresco Live Indexing app requires a working Alfresco ActiveMQ service, Alfresco Shared File store service, and the Elasticsearch server.

The table below lists the main configuration properties that can be specified through the Spring boot configuration.

|Property|Description|
|--------|-----------|
| server.port |Default HTTP port, each module defines itself. The default value is `8190`.|
| spring.activemq.broker-url | ActiveMQ broker url. The default value is `tcp://localhost:61616`. |
| spring.activemq.user | ActiveMQ username. The default value is `admin`. |
| spring.activemq.password | ActiveMQ password. The default value is `admin`. |
| spring.jms.cache.enabled | Cache JMS sessions. The default value is `false`. |
| spring.elasticsearch.rest.uris | Comma-separated list of Elasticsearch endpoints. The default value is `http://localhost:9200`. |
|elasticsearch.indexName | Name of the index to be used in Elasticsearch server. The default value is `alfresco`.|
| alfresco.content.refresh.event.queue | The channel where transform requests are re-inserted by the content event aggregator as consequence of a failure. The default value is `org.alfresco.search.contentrefresh.event`. |
| alfresco.content.event.retry.maxAllowed | Maximum number of redelivery attempts allowed. `0` is used to disable redelivery, and `-1` will attempt redelivery forever until it succeeds. |
| alfresco.content.event.retry.backoff | Exponential backoff multiplier that can be used to multiply each consequent redelivery delay. |
| alfresco.content.event.retry.delay | Initial delay in milliseconds between redelivery attempts. Subsequent delays will be affected by the backoff multiplier. |
| alfresco.content.event.retry.maxDelay | An upper bound in milliseconds for the computed redelivery delay. This is used when you specify backoff multiplied delays and is used to avoid the delay growing too large. |
| acs.repo.transform.request.endpoint | Alfresco Repository channel. The default value is `activemq:queue:acs-repo-transform-request?jmsMessageType=Text`. |
| alfresco.sharedFileStore.baseUrl | Alfresco Shared FileStore endpoint. The default value is `http://127.1.0.1:8099/alfresco/api/-default-/private/sfs/versions/1/file/`. |
| alfresco.sharedFileStore.timeout | Alfresco Shared FileStore maximum read timeout in milliseconds. The default value is `4000`. |
| alfresco.sharedFileStore.maxBufferSize | Alfresco Shared FileStore maximum buffer size (-1 for unlimited buffer). The default value is `-1`. |
| alfresco.event.topic | Topic name for Alfresco Repository events. The default value is `activemq:topic:alfresco.repo.event2`. |
| alfresco.metadata.event.channel | Alfresco Metadata channel. The default value is `activemq:queue:org.alfresco.search.metadata.event`. |
| alfresco.content.event.channel | Alfresco Content channel. The default value is `activemq:queue:org.alfresco.search.content.event`. |
| alfresco.metadata.event.queue | Alfresco Metadata queue name. The default value is `org.alfresco.search.metadata.event`. |
| alfresco.metadata.retry.event.queue | Alfresco Error event queue name. The default value is `org.alfresco.search.metadata.retry.event`. |
| metadata.events.batch.size | Maximum number of events per batch. The default value is `10`. |
| metadata.events.batch.timeout | Maximum timeout in milliseconds for batch creation. The default value is `1000`. |
| alfresco.retransmission.max.attempts | Maximum number of retries in case of transient failure processing. The default value is `3`. |
| alfresco.event.retry.delay | Delay time for error event in milliseconds. The default value is `1000`. |
| alfresco.mediation.filter-file | The configuration file which contains fields and node types blacklists. The default value is `classpath:mediation-filter.yml`. |
| alfresco.accepted-content-media-types-cache.refresh-time  | Time until you refresh the cache. We can disable the scheduler by replacing the value of the cron expression with a dash "-". In case you want to refresh the cache contents before the next scheduled refresh we should restart the application. The default value is `0 0 * * * *`. |
| alfresco.accepted-content-media-types-cache.enabled | Property to set if you want to enable or disable the cache for contacting the Transform Core AIO. The default value is `true`. |
| alfresco.accepted-content-media-types-cache.base-url | URL to get the list of Content Media Types supported. The default URL is `http://localhost:8090/transform/config`. |
| alfresco.path.retry.delay | Delay in milliseconds to retry a Path indexing operation. The default value is `1000`. |
| alfresco.path.retry.maxAttempts | Maximum number of attempts to retry a Path indexing operation. The default value is `3`. |
| alfresco.path-indexing-component.enabled | Index Path property. The default value is `true`. |
| alfresco.content-indexing-component.enabled | Index content property. The default value is `true`. |

Within the Elasticsearch connector there is a subset of components that index data. A component called Mediation subscribes to the channel indicated by the `alfresco.event.topic` attribute, as seen in the table above, and processes the incoming node events. The configuration of that component allows you to declare three blacklist sets for filtering out nodes or attributes to be indexed. These blacklists can be specified in the file using the `alfresco.mediation.filter-file` attribute, as seen in the table above. The default file is called `mediation-filter.yml` that must be in the module classpath, see the sample content of that file:

```bash
mediation:
  nodeTypes:
     - nodeType1
     - nodeType2
     - ...
     . nodeTypeN
  contentNodeTypes:
     - nodeType1
     - nodeType2
     - ...
     . nodeTypeN
  nodeAspects:
     - nodeAspect1
     - nodeAspect2
     - …
     - nodeAspectN
  fields:
     - field1
     - field2
     - ...
     . fieldN
```

Where:

* **nodeTypes**: if the node wrapped in the incoming event has a type which is included in this set, the node processing is skipped.
* **contentNodeTypes**: if the node wrapped in the incoming event has a content change associated with it and it has a type which is included in this set, then the corresponding content processing won't be executed. This means nodes belonging to one of the node types in this set, won't have any content indexed in Elasticsearch.
* **nodeAspects**: if the node wrapped in the incoming event has an aspect which is included in this set, the node processing is skipped.
* **fields**: fields listed in this set are removed from the incoming nodes metadata. This means fields in this set won't be sent to Elasticsearch for indexing, and therefore they won't be searchable.

To override some of these values command line system properties can be specified. Using the standard Spring boot approach, the name of the property must be converted to uppercase and dots must be changed by underscore characters. The following sample overrides the default values for three different properties.

```java
$ java -DSPRING_ELASTICSEARCH_REST_URIS=http://localhost:9200
 -DSPRING_ACTIVEMQ_BROKERURL=nio://activemq:61616
 -DALFRESCO_SHAREDFILESTORE_BASEURL=http://localhost:8099/alfresco/api/-default-/private/sfs/versions/1/file/
 -jar alfresco-elasticsearch-live-indexing-4.0.0-app.jar
```

The same convention can be used when deploying the Elasticsearch connector using the Docker compose template.

```docker
live-indexing:
    image: quay.io/alfresco/alfresco-elasticsearch-live-indexing
    environment:
        SPRING_ELASTICSEARCH_REST_URIS: http://elasticsearch:9200
        SPRING_ACTIVEMQ_BROKERURL: nio://activemq:61616
        ALFRESCO_SHAREDFILESTORE_BASEURL: http://shared-file-store:8099/alfresco/api/-default-/private/sfs/versions/1/file/
```

For example, content indexing for `cm:content` documents can be disabled using the following Docker configuration:

```docker
    live-indexing-mediation:
        image: quay.io/alfresco/alfresco-elasticsearch-live-indexing-mediation:${LIVE_INDEXING_MEDIATION_TAG}
        depends_on:
            - elasticsearch
            - alfresco
        environment:
            SPRING_ELASTICSEARCH_REST_URIS: http://elasticsearch:9200
            SPRING_ACTIVEMQ_BROKERURL: nio://activemq:61616
            ALFRESCO_MEDIATION_FILTER-FILE: file:/usr/tmp/mediation-filter.yml
        volumes:
            - ./mediation-filter.yml:/usr/tmp/mediation-filter.yml
```

The file `mediation-filter.yml` includes default content and also the `cm:content` filter.

```bash
$ cat mediation-filter.yml
mediation:
  nodeTypes:
  contentNodeTypes:
    - cm:content
  nodeAspects:
    - sys:hidden
  fields:
    - cmis:changeToken
```

See [Externalized Configuration](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-external-config){:target="_blank"} for more.

## Scaling up

All Elasticsearch connector services can be scaled up to use an ActiveMQ Connection Pool to increase the number of Consumers.

To use the ActiveMQ Connection Pool, add the following properties to your `.env` file in Docker compose. The Pool size is set to `100` in the sample.

```bash
$ cat .env
ACTIVEMQ_POOL_ENABLED=true
ACTIVEMQ_POOL_SIZE=100
```

Spring related properties can be associated to the Elasticsearch connector when declaring the service in the `docker-compose.yml` file.

```docker
    live-indexing-metadata:
        image: quay.io/alfresco/alfresco-elasticsearch-live-indexing-metadata:${LIVE_INDEXING_METADATA_TAG}
        environment:
            SPRING_ACTIVEMQ_BROKERURL: nio://activemq:61616
            SPRING_ACTIVEMQ_POOL_ENABLED: ${ACTIVEMQ_POOL_ENABLED}
            SPRING_ACTIVEMQ_POOL_MAXCONNECTIONS: ${ACTIVEMQ_POOL_SIZE}
```

To increase the consumer number you must check the property name in the `application.properties` file for the service and to then override it in the `docker-compose.yml` file. The following sample increases the consumer number to `20` for `elasticsearch-live-indexing-metadata`.

```docker
    live-indexing-metadata:
        image: quay.io/alfresco/alfresco-elasticsearch-live-indexing-metadata:${LIVE_INDEXING_METADATA_TAG}
        environment:
            INPUT_ALFRESCO_METADATA_BATCH_EVENT_CHANNEL: sjms-batch:metadata.event?completionTimeout=1000&completionSize=10&aggregationStrategy=#eventAggregator&?consumerCount=20
```
## Bulk deletion and ingestion

After the completion of a bulk deletion process, some scheduled jobs execute to clean up the environment for the next set of tasks. Executing a bulk ingestion process when the clean-up jobs are running impacts the performance of the ingestion process.

Therefore, when you plan to execute the bulk ingestion process after a bulk deletion process completes, it is recommended that you consider the following best practices:

* Start the bulk ingestion process after 25 minutes of the completion of the deletion process.
* Schedule the clean-up jobs after you complete the bulk ingestion.
* If you have configured the log files to include clean-up job notifications, monitor the log files and resume the ingestion after the cleanup is complete.

## Using HTTP Basic Authentication to access Elasticsearch

When using the Elasticsearch server with the HTTP Basic Authentication protocol you must add your Elasticsearch credentials to the `alfresco-global.properties` configuration file.

```bash
elasticsearch.user=elastic
elasticsearch.password=bob123
```

Additionally, for every "live-indexing" service from the Elasticsearch connector the same credentials must be configured. Use Java and the following global properties:

```bash
SPRING_ELASTICSEARCH_REST_USERNAME=elastic
SPRING_ELASTICSEARCH_REST_PASSWORD=bob123
```

The environment variables can be passed as a command line argument when running the Spring boot application locally or they can be added to the `environment` service section when using Docker Compose. The example above connects to an Elasticsearch server configured with the following values:

```docker
elasticsearch:
  image: elasticsearch:7.10.2
  environment:
    - discovery.type=single-node
    - xpack.security.enabled=true
    - ELASTIC_PASSWORD=bob123
```

You must also add these credentials to the Kibana app.

```docker
kibana:
   image: kibana:7.10.1
   environment:
     - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
     - ELASTICSEARCH_USERNAME=elastic
     - ELASTICSEARCH_PASSWORD=bob123
```

## Using HTTPS to access Elasticsearch for end to end encryption

When using the Elasticsearch server with the HTTPs protocol, additional configuration should be added to the Alfresco Repository.

A _truststore_ file, including public certificate and certificate chain from Elasticsearch HTTPs endpoint, must be added to the `alfresco-global.properties` configuration file.

Add the following properties to use the _truststore_ file from the Alfresco Repository. The `encryption.ssl.truststore.passwordFileLocation=` property has been intentionally left blank as the keystore includes only public information.

```docker
encryption.ssl.truststore.location=/usr/local/tomcat/alf_data/keystore/truststore.jceks
encryption.ssl.truststore.passwordFileLocation=
encryption.ssl.truststore.type=JCEKS
```

If you are using Docker compose, add the same properties in the `JAVA_OPTS` section for the Alfresco service using the "-D" prefix.

Additionally, for every "live-indexing" service from the Elasticsearch connector the same _truststore_ must be configured. Use Java and the following global properties:

```java
JAVAX_NET_SSL_TRUSTSTORE=/usr/local/tomcat/alf_data/keystore/truststore.jceks
JAVAX_NET_SSL_TRUSTSTOREPASSWORD=
JAVAX_NET_SSL_TRUSTSTORETYPE=JCEKS
```

These environment variables can be passed as command line arguments when running the spring boot application locally or they can be added to the `environment` service section when using Docker compose.

## Exact Term Search

The Exact Term search feature, that allows searching using the equals operator `=`, is disabled by default to save index space. It's possible to enable it for specific properties and property types using the following configuration file `/alfresco/search/elasticsearch/config/exactTermSearch.properties` located in the Alfresco Repository.

**Note:** Once you have the Exact term search configured a re-index is required. If you need the feature from the beginning, it is recommended to enable it before your first index is created.

|Property|Description|
|--------|-----------|
| alfresco.cross.locale.datatype.0 | A new cross locale field has been added for any property of this data-type. For example `{http://www.alfresco.org/model/dictionary/1.0}text`. |
| alfresco.cross.locale.property.0 | A new cross locale field to cover exact term search) has been added for the property. For example `{http://www.alfresco.org/model/content/1.0}content`. |

You can add as many data-types and properties as you like by adding lines and incrementing the associated index:

```bash
alfresco.cross.locale.datatype.0={http://www.alfresco.org/model/dictionary/1.0}text
alfresco.cross.locale.datatype.1={http://www.alfresco.org/model/dictionary/1.0}content
alfresco.cross.locale.datatype.2={http://www.alfresco.org/model/dictionary/1.0}mltext
alfresco.cross.locale.property.0={http://www.alfresco.org/model/content/1.0}content
```

In order to overwrite this configuration when using Docker, mount this file as an external volume. Following sample describes a local configuration to be applied to Elasticsearch Search Subsystem when using Docker Compose deployment:

```docker
services:
  alfresco:
    volumes:
      - ./exactTermSearch.properties:/usr/local/tomcat/webapps/alfresco/WEB-INF/classes/alfresco/search/elasticsearch/config/exactTermSearch.properties
```

## Support for different databases

PostgreSQL is the default database for Search Enterprise. You can use different databases with Search Enterprise, but they must be configured within your system and must match the database used by Content Services. The other types of databases supported by Search Enterprise are: MySQL, MariaDB, Microsoft SQL Server, and Oracle.

Add parameters to the startup script or in the command line when you run the reindexing app. You can use the following parameters.

| Property | Description |
| -------- | ------------|  
| spring.datasource.url | *Required*. The database name. |
| spring.datasource.username | *Required*. Enter the username for the database. |
| spring.datasource.password | *Required*. Enter the password for the username. |
| spring.datasource.hikari.maximumpoolsize | *Optional*. Sets the maximum size of the connections in HikariCP. |
| alfresco.dbtype | *Optional*. Use this property to set your database type. When you set the type of database you are using the database auto-detection type is turned off. The supported values are: `postgresql`, `mysql`, `mariadb`, `sqlserver`, and `oracle`. |

For example:
```
java -jar alfresco-elasticsearch-reindexing-4.0.0.1.jar --spring.datasource.url="jdbc:sqlserver://<your-server>.<your-domain>.com:1433;databaseName=alfresco;integratedSecurity=true"
```

### Provide custom JDBC Drivers

Search Enterprise only provides the PostgreSQL driver by default and it is bundled with the Search Enterprise executable components. If you want to use a different database to PostgreSQL you must provide the correct JDBC configuration and corresponding driver.
The drivers are loaded from a directory called `db-drivers` that must be present at the same directory level as the executable `.jar` file.

For example:

```text
├── `alfresco-elasticsearch-reindexing-x.x.x-app.jar`
└── `db-drivers`
    └── `mydb-driver.jar`
```

If you are using Docker Compose to install Search Enterprise you must add the JDBC driver information inside the docker container.

For example:

```yaml
services:
    reindexing-service:
        image: quay.io/alfresco/alfresco-elasticsearch-reindexing:latest
        mem_limit: 1024m
        environment:
        - ...
        volumes:
            - ./<location>/jdbc/drivers:/opt/db-drivers:ro
```
---
title: Language support
---

Search Enterprise supports multiple languages. You can configure other languages using the `src/main/resources/alfresco/search/elasticsearch/config/locale` configuration file.

> **Note:** Some supported languages require the installation of a plug-in and some Asian languages may also require installation of the [ICU analysis plug-in](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html){:target="_blank"} Where there is a plug-in required, you must install it on every node in the cluster.

The following languages are supported:

| Language | Search Enterprise language | Plug-in required |
| -------- | -------------------------- | ---------------- |
| fr | light_french | Not required |
| de | light_german | Not required |
| it | light_italian | Not required |
| es | light_spanish | Not required |
| nl | dutch | Not required |
| pl | polish | [Stempel Polish analysis plug-in](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-stempel.html){:target="_blank"}. |
| ja | japanese | [Japanese (kuromoji) analysis plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-kuromoji.html){:target="_blank"} and [ICU analysis plug-in](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html){:target="_blank"}. |
| ru | russian | Not required |
| pt | light_Portugese | Not required |
| zh | simplified Chinese | [Smart Chinese analysis plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-smartcn.html){:target="_blank"} and [ICU analysis plug-in](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html){:target="_blank"}. |
| cs | czech | Not required |
| da | danish | Not required |
| sv | swedish | Not required |
| fi | finnish | Not required |
| nb | norwegian | Not required |

## Add language

You must update the Content Services `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` configuration file to enable the language you want to use with Search Enterprise. For example to use French you must add `-Delasticsearch.index.locale=fr`, and `-Dfile.encoding=utf-8`.

### Docker Compose

If you are installing Search Enterprise using a Docker Compose file you must instruct Alfresco that you are using another language in addition to English. For example, to use French you must add the following environment variable to the Alfresco service (`alfresco`):

```yml
JAVA_OPTS: "
  -Delasticsearch.index.locale=fr
"
```

You must also instruct Alfresco and Search Enterprise to use `UTF-8` encoding. This applies to the Alfresco service as well as the Elasticsearch live-indexing and Full-indexing services:

```yml
JAVA_OPTS: "
  -Dfile.encoding=utf-8
"
```

## Custom configuration

To create a custom configuration you must create a `JSON` file in the locale configuration directory: `src/main/resources/alfresco/search/elasticsearch/config/locale`. The file must follow the naming convention of `xx_locale.json` where `xx` is the two character locale code. Use the following code example to create your own configuration file. In this case the example is for the French language.

```json
{
  "settings": {
    "analysis": {
      "analyzer": {
        "locale_content": {
          "type": "french"
        },
        "locale_text_index": {
          "tokenizer": "whitespace",
          "filter": [
            "asciifolding",
            "custom_word_delimiter_graph",
            "lowercase",
            "flatten_graph",
            "french_stemmer_multiplexer"
          ]
        },
        "locale_text_query": {
          "tokenizer": "whitespace",
          "filter": [
            "asciifolding",
            "custom_word_delimiter_graph",
            "lowercase",
            "french_stemmer_multiplexer"
          ]
        }
      },
      "filter": {
        "french_stemmer": {
          "type": "stemmer",
          "language": "light_french"
        },
        "french_stemmer_multiplexer": {
          "type": "multiplexer",
          "filters": [ "french_stemmer" ]
        }
      }
    }
  }
}
```

The `analysis` section contains three analyzers and any custom defined filters. Each analyzer section must contain at least one tokenizer. You can optionally include a number of filters which can then modify the tokens, for example to convert text to lowercase for the index. `locale_content` is a symmetric content analyzer, which in this example is set to `french`. `locale_text_index` is an asymmetric text analyzer, which you set to use whitespace as the delimiter. It has several filters including a custom defined filter, in this instance its called `french_stemmer_multiplexer`. The `locale_text_query` section contains an asymmetric text query analyzer which is also set to use whitespace as the delimiter. It has several filters, including, in this case, one called `french_stemmer_multiplexer`. The filter section contains any custom defined filters that are used by the analyzers. In this case the filter is called `french_stemmer_multiplexer`.

## Checking configuration

You can check your language configuration.

To verify that the index was created using the correct locale configuration:

`curl -s '{$hostname}:9200/alfresco/_settings/' | jq `

To check how your text is split into tokens:

`curl -X GET "{$hostname}:9200/alfresco/_analyze?pretty" -H 'Content-Type: application/json' -d'{"analyzer" : "locale_content", "text" : "I found a dog."}'`

> **Note:** For a new environment ensure that the initial reindexing is run first.

To verify that the content of a particular node has been correctly extracted and stored in the index:

`curl -s {$hostname}:9200/alfresco/_doc/{$nodeId} | jq ._source`

To execute  a search query:

`curl -s -u admin:admin --header "Content-Type: application/json" -d '{"query":{"query":"dog","language":"afts"}}' "{$hostname}:8080/alfresco/api/-default-/public/search/versions/1/search" | jq .list.entries`
---
title: Transactional metadata query
---

Alfresco Content Services supports the execution of a subset of the CMIS Query Language (CMIS QL) and Alfresco Full Text Search (AFTS) queries directly against the database. Also, the noindex subsystem supports queries only against the database. This collection of features is called transactional metadata query (TMDQ).

TMDQ supports use cases where eventual consistency is not the preferred option.

The Elasticsearch subsystem is eventually consistent. The amount of time a change a change takes to reflect in the index is normally less than 1 second, but can be longer under heavy load, or for complex/cascading updates. Elasticsearch indexes the metadata and the content of each updated node, in the order in which the nodes were last changed. The indexing components will try to index information about nodes as fast as possible, but content indexing is likely to be limited by the time needed to extract text from the files and all indexing will be affected by the rate at which the nodes are being changed.

Some queries can be executed both transactionally against the database or with eventual consistency against the Elasticsearch index. Only a subset of queries using the AFTS or CMIS query languages can be executed against the database. No queries using the Lucene query language can be used against the database whereas, `selectNodes` (XPATH) on the Java API always goes against the database, walking and fetching nodes as required.

In general, TMDQ does not support:

* Structural queries.
* Full text search.
* Special fields (For example `SITE`).
* Faceting.
* Any aggregation.
   > **Note:** This includes counting the total number of matches for the query.

AFTS and CMIS queries are parsed to an abstract form. This is then sent to an execution engine. There are two execution engines: the database and the Elasticsearch index. The default is to try the database first and fall back to the Elasticsearch index, if the query is not supported against the database. This is configurable for a search subsystem and per query using the Java API.

> **Note:** Alfresco Content Services supports TMDQ by default.

## Options supported by Query Languages

Use this information to know what options are supported by the v1 REST API, CMIS Query Language (QL), and Alfresco Full Text Search Query Language (FTS QL).

### v1 REST API and TMDQ

For the v1 REST API, anything that is not a simple query, a filter query, an option that affects these, or an option that affects what is returned for each node in the results, is not supported by TMDQ.

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

The v1 REST API does not support TMDQ for:

* `templates`
* `localisation` and `timezone`
* `facetQueries`
* `facetFields`
* `highlight`
* `ranges facets`

The use of these with TMDQ is undefined. Some of these options will be ignored and results will come from the database; others will cause the database query to fail and ACS will fail over to return results from the search index.

The V1 REST API ignores the SQL `SELECT` part of a CMIS query and generates the results as it would do for AFTS.

### CMIS QL & TMDQ

For CMIS QL, all expressions except for `CONTAINS()`, `SCORE()`, and `IN_TREE()` can now be executed against the database. Most data types are supported except for the CMIS uri and html types. Strings are supported but only if they are 1024 characters or less in length.

Primary and secondary types are supported and require inner joins to link them together. You can skip joins to secondary types from the fetch in CMIS using the v1 REST API. You would need an explicit `SELECT` list and supporting joins from a CMIS client. You still need joins to secondary types for predicates and ordering. As CMIS SQL supports ordering as part of the query language, you have to do it there and not via the v1 REST API sort.

For multi-valued properties, CMIS QL supports `ANY` semantics from SQL 92. A query against a multi-lingual property, such as title or description, is treated as multi-valued and may match in any language. In the results, you will see the best value for your locale, which may not match the query. Also, ordering will consider any value.

### UPPER() and LOWER()

`UPPER()` and `LOWER()` functions were in early drafts for the CMIS 1.0 specification, but were subsequently dropped. These are not part of the CMIS 1.0 or 1.1 specifications. They are not supported in TMDQ.

### Alfresco FTS QL & TMDQ

It is more difficult to write AFTS queries that use TMDQ as the default behaviour is to use full text queries for text and full text queries cannot be served by the database. Also, special fields like `SITE` and `TAG` that are derived from paths or other nodes will not be handled by the database. `TYPE`, `ASPECT` and the related exact matches will work with TMDQ. All property data types are fine but strings should be less than 1024 characters in length. Text queries have to be prefixed with `=` to avoid full text search.

Ranges, PATH, and ANCESTOR are not currently supported.

### Database & TMDQ

Some differences between the database and TMDQ:

* The database has specific fixed collation as defined by the database schema. This affects all string comparisons, such as ordering or case sensitivity in equality. Elasticsearch uses Java localised collation and supports more advanced ordering and multi-lingual fields. The two engines can produce different results for lexical comparison, case sensitivity, ordering, or when using `mltext` properties.
* The database post filters the results to apply permissions. As a result, no total count can be provided and large result sets are not well supported. This also affects paging behaviour. Permission evaluation is truncated by time or number of evaluations. TMDQ is not intended to scale to tens of thousands of nodes. It will not perform well for users who can only read one node in a million. It cannot tell you how many results matched the query and cannot support aggregations. It will try to do enough to give you the page requested. The Elasticsearch index can apply permissions at query and facet time, allowing queries to scale to billions of nodes.
* The CMIS part of the query and `CONTAINS()` part are melded together into a single abstract query representation. By default, in CMIS the `CONTAINS()` expression implies full text search, so the queries will go to the Elasticsearch index.
* The database does not score. It will return results in some order that depends on the query plan, unless you ask for specific ordering. A three part `OR` query, where some documents match more than one constraint, is treated as equal. For Elasticsearch index queries, the more parts of an `OR` match, the higher is the score. The docs that match more optional parts of the query will come higher up.
* Queries from Share will not use TMDQ as they will most likely have a full text part to the query and ask for facets.
* Exact term search will behave differently when executed against the database or the search index. This is due to how tokenisation is applied to strings in the search index, for more see [Exact Term Queries](https://hub.alfresco.com/t5/alfresco-content-services-blog/exact-term-queries-in-search-services-2-0/ba-p/302200).

### Exact match and patterns

TMDQ can support exact match on all properties (subject to database collation) regardless of the property index configuration in the data model. All text properties can support pattern matching. The database index supports a fixed number of leading characters. The database store a maximum string size before it overflows to another form. Only short form strings can be used in database queries.

Elasticsearch supports exact match on all non-text properties. Text properties only support exact and pattern matches if set to tokenised `both` or `false` in the data model. Elasticsearch provides supports values up to approximately 32,700 UTF-8 bytes.

The following specific CMIS QL fields are supported:

* `cmis:parentId`
* `cmis:objectId`
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

### Support for special fields in TMDQ using AFTS

* TYPE
* ASPECT
* EXACTTYPE
* EXACTASPECT
* PARENT - Note that database queries will not contain any categories since there is no notion of category paths in the database

> **Note:** CMIS QL does not support any use of `CONTAINS()` using the database.

Transactional Metadata Query and the Elasticsearch index queries are intended to support different use cases. They differ in queries and options that they support and in the results they generate with respect to collation and scoring.

## Transactional metadata queries supported by database

Use this information to understand the queries supported by the database.

The Alfresco Full Text Search (FTS) query text can be used standalone or it can be embedded in CMIS-SQL using the `CONTAINS()` predicate function. The CMIS specification supports a subset of Alfresco FTS. For more information on search syntax, see [Alfresco Full Text Search Reference]({% link search-services/latest/using/index.md %}).

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
  * Supports comparisons using `=`, `<>`, `<`, `<=`, `>=`, `>`, `IN`, `NOT IN` and `LIKE`.
  * Supports ordering for single-valued properties, for example:

    ```sql
    select * from cmis:document where cmis:name <> 'fred' order by cmis:name
    ```

* `integer`, `double`, and `float`
  * Supports comparisons, such as `=`, `<>`, `<`, `<=`, `>=`, `>`, `IN`, `NOT IN`.
  * Supports ordering for single-valued properties.
* `boolean`
  * Support for comparisons `=` and `<>`
  * Supports ordering for single-valued properties.
* `id`
  * Supports `cmis:objectId`, `cmis:baseTypeId`, `cmis:objectTypeId` and `cmis:parentId` fields.
  * Support for comparisons, using `=`, `<>`, `IN` and `NOT IN`.
  * Ordering using a property, which is a CMIS identifier, is not supported.
* `datetime`
  * Supports comparisons, such as `=`, `<>`, `<`, `<=`, `>=`, `>`, `IN` and `NOT IN`.
  * Support ordering for single-valued properties, for example:

    ```sql
    select * from cmis:document where cmis:lastModificationDate = '2010-04-01T12:15:00.000Z' order by
     cmis:creationDate ASC
    ```

While the CMIS URI data type is not supported, multi-valued properties and multi-valued predicates as defined in the CMIS specification are supported.

  For example:

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
* `IN_FOLDER` predicate function

## Unsupported predicates

The following predicates are not supported by TMDQ:

* TEXT search predicate, such as `CONTAINS()` and `SCORE()`
* `IN_TREE()` predicate

## Supported logical operators

The following logical operators are supported:

* `AND` 
* `NOT`
* `OR`

## Other operators

In the following cases, the query will go to the database but the result might not be as expected. In all other unsupported cases, the database query will fail and fall back to be executed against the Elasticsearch subsystem.

* `IS NOT NULL`
* `IS NULL`: Currently, this operator will only find properties that are explicitly NULL as opposed to the property not existing.
* `SORT`: The multi-valued and `mltext` properties will sort according to one of the values. Ordering is not localized and relies on the database collation. It uses an `INNER JOIN`, which will also filter NULL values from the result set.
* `d:mltext`: This data type ignores locale. However, if there is more than one locale, the localised values behave as a multi-valued string. Ordering on `mltext` will be undefined as it is effectively multi-valued.

## Configuring transactional metadata query

Configure the transaction metadata query using the subsystem properties.

The common properties used to configure the transactional metadata query for the search subsystems are:

* `query.cmis.queryConsistency`
* `query.fts.queryConsistency`

These properties should be set in the `<TOMCAT_HOME>/shared/classes/alfresco-global.properties` file.

> **Important:** The name of these properties has changed. They were called `solr.query.cmis.queryConsistency` and `solr.query.fts.queryConsistency` but these were deprecated. The old names of the properties will still work with Elasticsearch but it is highly recommended you update them in your configuration.

The default value for these properties is `TRANSACTIONAL_IF_POSSIBLE`. However, you can override it with any of the following permitted values:

* `EVENTUAL`
* `TRANSACTIONAL`

The `query.cmis.queryConsistency` and `query.fts.queryConsistency` properties can also be set per query on the `SearchParameters` and `QueryOptions` objects in the V1 REST API.

## Configuring search in Alfresco Share

The following sections describe how to configure search in Alfresco Share.

### Controlling permissions checking

TMDQ may take a long time when trying to create a page of results with a sparse result set. You can limit the time Alfresco Content Services spends per TMDQ query by configuring a maximum duration or a maximum number of permission checks before returning. Setting this limit increases search speed and reduces the use of resources but may result in the user receiving a partial page of results for expensive queries.

You can limit both the time spent and the number of documents checked before Alfresco Content Services returns search results using the `system.acl.maxPermissionCheckTimeMillis` and the `system.acl.maxPermissionChecks` properties. The default values are 10000 and 1000 respectively.

1. Open the `<classpathRoot>/alfresco-global.properties` file.

2. Set the `system.acl.maxPermissionCheckTimeMillis` property.

    For example, `system.acl.maxPermissionCheckTimeMillis=20000`.

3. Set the `system.acl.maxPermissionChecks` property.

    For example, `system.acl.maxPermissionChecks=2000`.

    > **Note:** If you increase these values and have a query that returns a very large number of results, (a) the search results will take longer to be returned to the user, and (b) the system will spend longer to check permissions, leading to the possibility of performance degradation. If you set these values to a low number, you run the risk of inconsistent search results every time you run the same search. These settings are also applied when paging. So paging the results will only go up to the maximum returned results based on these settings.

### Limiting search results

Use this information to control the maximum number of items that an Alfresco Share search returns.

By default, the Share search feature returns a maximum of 250 search results. You can extend this number of search results to return more than 250 entries.

1. Download your `share-config.xml` file found at `tomcat/webapps/share/WEB-INF/classes/alfresco/share-config.xml`, for more see [Share Configuration Extension Point](https://docs.alfresco.com/content-services/latest/develop/share-ext-points/share-config/).

2. Open the `share-config.xml` file and copy the `<config evaluator="string-compare" condition="Search" replace="true">` section.

3. Open the `<web-extension>share-config-custom.xml` file and then paste the copied section.

4. Locate the `<max-search-results>250</max-search-results>` property and then edit the value to your preferred number of search results.

5. For the changes to take effect, refresh the Alfresco Content Services web scripts. To refresh the web scripts:

    1. Navigate to the web scripts Home page.

        For example, go to: `http://<your-host>:8080/share/page/index`.

    2. Click **Refresh Web Scripts**.

        You have now refreshed the web scripts and set a limit to the number of items a search in Share returns.
---
title: Overview
---

Alfresco Search Enterprise 4.0 consists of Alfresco Content Services, Elasticsearch Server, and the Elasticsearch connector. Use this information to install the Elasticsearch connector, which can be deployed using either JAR files, Docker Compose, or Helm.

## Prerequisites

* Alfresco Content Services 23.1 that includes Alfresco ActiveMQ, Alfresco Transform Service, and Database, for more see [Install overview]({% link content-services/latest/install/index.md %}).
* Elasticsearch 7.17.x - any version between 7.10.x and 7.17.x inclusive, is compatible. It may be used as a standard managed service or can be installed with the default configuration, for more see [Install Elasticsearch server](#install-elasticsearch-server).
* Elasticsearch Connector 4.0

See the [Supported platforms]({% link search-enterprise/latest/support/index.md %}) for more.

## Configure Subsystem in Repository

You must first activate and configure the Search Services subsystem in Content Services by using either the `TOMCAT_HOME>/shared/classes/alfresco-global.properties` file or the [Repository Admin Web Console]({% link content-services/latest/admin/admin-console.md %}).

Add the following lines to the configuration file `alfresco-global.properties` to enable the Elasticsearch Search subsystem.

```bash
# Set the Elasticsearch subsystem
index.subsystem.name=elasticsearch
# Elasticsearch index properties
elasticsearch.indexName=alfresco
elasticsearch.createIndexIfNotExists=true
# Elasticsearch server properties
elasticsearch.host=localhost
elasticsearch.port=9200
elasticsearch.baseUrl=/
```

These configuration properties are used by Content Services to communicate with the Elasticsearch server. In the example above a plain HTTP connection is configured, but Alfresco Repository also supports communication with Elasticsearch server using Basic Authentication and the HTTPs protocol, for more see [Subsystem]({% link search-services/latest/config/index.md %}).

If using the Repository Admin Web Console select `Repository Services > Search Service` and set the properties from that web page, see below.

![console]({% link search-enterprise/images/alfresco_repo_web_console.png %})

> **Note:** In Content Services 7.1, the `Test Connection` button will fail if your Elasticsearch server does not include the "alfresco" index. You are however still able to `Save` your configuration and the index will be created automatically.

## Install using JAR files

Use this information to install the Elasticsearch connector on the same machine as Content Services using JAR files.

1. Download the `alfresco-elasticsearch-connector-distribution-4.0.0.zip` file from [Hyland Community](https://community.hyland.com/){:target="_blank"} and extract it.  

2. Verify all the required services are available:

* Alfresco ActiveMQ, by default `nio://activemq:61616`
* Alfresco Shared FileStore endpoint, by default http://shared-file-store:8099/alfresco/api/-default-/private/sfs/versions/1/file/
* Alfresco Database, by default `localhost:5432`
* Elasticsearch server, by default http://elasticsearch:9200

Once you have extracted the Elasticsearch connector zip file you install the Alfresco re-indexing app, and then the Alfresco live indexing app.

### Alfresco Re-indexing app

The Elasticsearch connector *Live Indexing* component listens to messages from ActiveMQ. This means some initial information from Alfresco Repository must be indexed using the *Re-indexing* component. The *Re-indexing* component can also be used to index a pre-populated Alfresco Repository.

1. Generate a JSON mapping of namespace to prefix, for your deployed content models.
  
    To help you build the JSON file you can use [Alfresco Model Namespace-Prefix Mapping](https://github.com/AlfrescoLabs/model-ns-prefix-mapping){:target="_blank"}.

2. Copy the [JAR deployment](https://github.com/AlfrescoLabs/model-ns-prefix-mapping/releases/download/1.0.0/model-ns-prefix-mapping-1.0.0.jar){:target="_blank"} file for this module to your local Alfresco Repository deployment, for detailed information on how to deploy a Simple JAR Alfresco Repository see [Simple Module (JAR)](https://docs.alfresco.com/content-services/latest/develop/extension-packaging/#simplemodule){:target="_blank"}.

3. Once installed, the JSON mapping file can be obtained by using `http://localhost:8080/alfresco/s/model/ns-prefix-map`, see the Simplified response:

    ```json
    {
      "prefixUriMap": {
        "http://www.alfresco.org/model/custommodelmanagement/1.0": "cmm",
        "http://www.alfresco.org/model/datalist/1.0": "dl",
        "http://www.alfresco.org/model/emailserver/1.0": "emailserver",
        "http://www.alfresco.org/model/action/1.0": "act",
        "http://www.alfresco.org/model/system/1.0": "sys",
        "http://www.alfresco.org/model/cmis/1.0/cs01": "cmis",
        "http://www.alfresco.org/model/bpm/1.0": "bpm",
        "http://www.alfresco.org/model/dictionary/1.0": "d",
        "http://www.alfresco.org/model/linksmodel/1.0": "lnk",
        "http://www.alfresco.org/model/workflow/invite/moderated/1.0": "imwf",
        "http://www.alfresco.org/model/workflow/invite/nominated/1.0": "inwf",
        "http://www.alfresco.org/model/content/1.0": "cm",
        "http://www.alfresco.org/model/content/smartfolder/1.0": "smf",
        "http://www.alfresco.org/model/cmis/custom": "cmiscustom",
        "http://www.alfresco.org/model/site/1.0": "st",
        "http://www.alfresco.org/model/application/1.0": "app",
        "http://www.alfresco.org/model/imap/1.0": "imap",
        "http://www.alfresco.org/model/aos/1.0": "aos",
        "custom.model": "custom",
        "": ""
      }
    }
    ```

4. Save this content in a new file named `reindex.prefixes-file.json`.

5. Run the re-indexing application from the command line by passing the already generated JSON file and details for the Database and Elasticsearch servers.

> **Note:** Due to this application providing default values for Alfresco Repository Database username and password, it's strongly recommended you set these credentials using the command line. This ensures database credentials won't be stored in the server filesystem.

```java
java -jar alfresco-elasticsearch-reindexing-4.0.0-app.jar \
--alfresco.reindex.jobName=reindexByIds \
--spring.elasticsearch.rest.uris=http://localhost:9200 \
--spring.datasource.url=jdbc:postgresql://localhost:5432/alfresco \
--spring.datasource.username=alfresco \
--spring.datasource.password=alfresco \
--alfresco.reindex.prefixes-file=file:reindex.prefixes-file.json \
--alfresco.acceptedContentMediaTypesCache.baseurl=http://localhost:8090/transform/config \
--spring.activemq.broker-url=nio://localhost:61616
```

When completed successfully you will see:  

```text
o.s.batch.core.step.AbstractStep         : Step: [reindexByIdsStep] executed in 4s952ms
o.a.r.w.ElasticsearchRepoEventItemWriter : Total indexed documents:: 845
o.a.r.listeners.JobLifecycleListener     : Current Status: COMPLETED
```

Once the program has been executed, the existing Alfresco Repository nodes are available in Search Enterprise.

> **Note:** Additional use cases are be covered in the [Administer]({% link search-enterprise/latest/admin/index.md %}) documentation.

### Alfresco Live Indexing app

The Elasticsearch connector *Live Indexing* app can be started from the command line as a standard Spring Boot application.

1. Start the Live Indexing app.

```java
java -jar alfresco-elasticsearch-live-indexing-4.0.0-app.jar
```

If your services are deployed on a different server or port the following parameters can be used.

```java
java -jar alfresco-elasticsearch-live-indexing-4.0.0-app.jar \
--spring.activemq.broker-url=nio://localhost:61616 \
--spring.elasticsearch.rest.uris=http://localhost:9200 \
--alfresco.sharedFileStore.baseUrl=http://localhost:8099/alfresco/api/-default-/private/sfs/versions/1/file/ \
--alfresco.acceptedContentMediaTypesCache.baseurl=http://localhost:8090/transform/config \
--elasticsearch.indexName=alfresco
```

If required additional memory may be assigned to these services using the default JVM options. For instance, to start the Elasticsearch connector with 2 GB of RAM.

```java
java -Xmx2G -jar alfresco-elasticsearch-live-indexing-4.0.0-app.jar
```

By default, the Elasticsearch connector is started using port 8080. This port can be changed using the default Spring Boot command line parameter `server.port`. For instance, to start the Elasticsearch Connector using port `8083`.

```java
java -jar alfresco-elasticsearch-live-indexing-4.0.0-app.jar --server.port=8083
```

Once all services are up and running the Elasticsearch index will be populated and search queries will work as expected when using supported Alfresco applications such as Alfresco Digital Workspace.

## Install using Docker Compose

Use this information to quickly start up the Elasticsearch connector using Docker compose. Due to the limited capabilities of Docker compose, this deployment method is only recommended for development and test environments. You can perform the Docker compose deployment using the source code or downloading the distribution zip file. Both of these methods produce the same `docker-compose.yaml` file needed when deploying Content Services.

> **Note:** The Docker compose file provided is only for test and development purposes.

### Prerequisites

* [Docker](https://docs.docker.com/install/){:target="_blank"}
  * This allows you to run Docker images and Docker compose on a single computer.
* [Docker compose](https://docs.docker.com/compose/install/){:target="_blank"}
  * Docker compose is included as part of some Docker installers. If it's not part of your installation, then install it separately after you've installed Docker.

  > **Note:** The Elasticsearch connector Docker images from Quay.io are only for Enterprise customers. You need credentials to be able to pull these images from Quay.io. Alfresco customers can request their credentials by logging a ticket at [Alfresco Support](https://community.hyland.com/){:target="_blank"}{:target="_blank"}.

### Using source code

Create the Docker compose file using the source code.

1. Retrieve the Elasticsearch connector source code with a Git client using SSH:

    ```bash
    git clone git@github.com:Alfresco/alfresco-elasticsearch-connector.git
    ```

2. Move to the folder where you cloned the project and build it using Maven:

    ```bash
    cd alfresco-elasticsearch-connector
    mvn clean install -DskipTests
    ```

    The Docker compose file is created in the `alfresco-elasticsearch-connector-distribution/src/main/resources/docker-compose` folder.

3. Move to the Docker compose folder in the distribution module:

    ```bash
    cd /alfresco-elasticsearch-connector-distribution/src/main/resources/docker-compose
    ```

### Using distribution zip

Create the Docker compose file using the distribution zip file.

1. Download the `alfresco-elasticsearch-connector-distribution-4.0.0.zip` file from [Hyland Community](https://community.hyland.com/){:target="_blank"}.

2. Unzip the distribution zip file into a folder:

    ```bash
    unzip alfresco-elasticsearch-connector-distribution-*.zip -d alfresco-elasticsearch-connector-distribution
    ```

3. Move to the Docker compose folder in the distribution folder:

    ```bash
    cd alfresco-elasticsearch-connector-distribution/docker-compose
    ```

### Deployment steps

Deploy the Docker compose file you created.

1. Log in to Quay.io using your credentials:

    ```bash
    $ docker login https://quay.io
    ```

2. Deploy Alfresco Content Services. The `docker-compose.yml` you generated includes the Repository, ADW, database, Transform Service, ActiveMQ, Alfresco Elasticsearch Connector, Elasticsearch, and Kibana.

    ```bash
    $ docker-compose up --build --force-recreate
    ```

The command downloads the images and fetches all the dependencies, then creates each container, and starts the system.

Wait for the logs to show the following message:

```bash
alfresco_1 | 05-Sep-2021 13:36:37.893 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in 148870 ms
```

If you encounter errors whilst the system is starting up:

* Stop the session (by using `CONTROL+C`).
* Try allocating more memory resources, as advised in `docker-compose.yml`. For example, in Docker, change the memory setting in `Preferences (or Settings) > Advanced > Memory`, to at least 16 GB.
* Make sure you restart Docker and wait for the process to finish before continuing.

Open your browser and check everything starts up correctly:

* Administration and REST APIs http://localhost:8080/alfresco
* Alfresco Digital Workspace (UI) http://localhost:8080/workspace
* ActiveMQ Admin Web Console http://localhost:8161/admin
* Elasticsearch server http://localhost:9200
* Kibana http://localhost:5601

Log in as the administrator with the default username and password.

> **Note:** Remember to run the Alfresco Re-indexing app as described above in order to add existing Alfresco Repository nodes to the Elasticsearch server.

### Alternative deployment

By default, the Docker compose template deploys the Elasticsearch connector services individually:

* `live-indexing-mediation` the service manages ActiveMQ messages from Alfresco Repository and Alfresco Transform Service
* `live-indexing-content` the service indexes content in Search Enterprise
* `live-indexing-metadata` the service indexes metadata in Search Enterprise
* `live-indexing-path` the service indexes path queries in Search Enterprise

The `docker-compose.yml` file you generated includes:

```bash
live-indexing-mediation:
    image: quay.io/alfresco/alfresco-elasticsearch-live-indexing-mediation:${LIVE_INDEXING_MEDIATION_TAG}
    environment:
        SPRING_ELASTICSEARCH_REST_URIS: http://elasticsearch:9200
        SPRING_ACTIVEMQ_BROKERURL: nio://activemq:61616

live-indexing-content:
    image: quay.io/alfresco/alfresco-elasticsearch-live-indexing-content:${LIVE_INDEXING_CONTENT_TAG}
    environment:
        SPRING_ELASTICSEARCH_REST_URIS: http://elasticsearch:9200
        SPRING_ACTIVEMQ_BROKERURL: nio://activemq:61616
        ALFRESCO_SHAREDFILESTORE_BASEURL: http://shared-file-store:8099/alfresco/api/-default-/private/sfs/versions/1/file/

live-indexing-metadata:
    image: quay.io/alfresco/alfresco-elasticsearch-live-indexing-metadata:${LIVE_INDEXING_METADATA_TAG}
    environment:
        SPRING_ELASTICSEARCH_REST_URIS: http://elasticsearch:9200
        SPRING_ACTIVEMQ_BROKERURL: nio://activemq:61616

live-indexing-path:
    image: quay.io/alfresco/alfresco-elasticsearch-live-indexing-path:${LIVE_INDEXING_PATH_TAG}
    environment:
        SPRING_ELASTICSEARCH_REST_URIS: http://elasticsearch:9200
        SPRING_ACTIVEMQ_BROKERURL: nio://activemq:61616
```

Alternatively, you can use the all-in-one Docker image for the Elasticsearch connector named `alfresco-elasticsearch-live-indexing` that includes every service:

```bash
live-indexing:
    image: quay.io/alfresco/alfresco-elasticsearch-live-indexing
    environment:
        SPRING_ELASTICSEARCH_REST_URIS: http://elasticsearch:9200
        SPRING_ACTIVEMQ_BROKERURL: nio://activemq:61616
        ALFRESCO_SHAREDFILESTORE_BASEURL: http://shared-file-store:8099/alfresco/api/-default-/private/sfs/versions/1/file/
```

> **Note:** If the Elasticsearch server is available on your environment, `elasticsearch` and `kibana` services can be removed from the `docker-compose.yml` file. You can adjust the references to the `elasticsearch` service in your Docker compose file to use your Elasticsearch deployment.

## Install using Helm

Use this information to install the the Elasticsearch connector using Helm. The deployment of the Content Services stack for Kubernetes using Helm is available at [Alfresco Content Services Containerized Deployment](https://github.com/Alfresco/acs-deployment){:target="_blank"}.

Depending on where you want to install Content Services you must follow the appropriate instructions for the Kubernetes cluster, for more see [Docker Desktop](https://github.com/Alfresco/acs-deployment/blob/master/docs/helm/docker-desktop-deployment.md){:target="_blank"} or [AWS EKS](https://github.com/Alfresco/acs-deployment/blob/master/docs/helm/eks-deployment.md){:target="_blank"}.

To replace Search Services with the Elasticsearch Connector you must configure the [values.yaml](https://github.com/Alfresco/acs-deployment/blob/master/helm/alfresco-content-services/values.yaml){:target="_blank"} file and set the `alfresco-elasticsearch-connector.enabled` property to `true` and `alfresco-search.enabled` to `false`.

The Elasticsearch Connector will start four new Kubernetes deployments for live indexing:

* **Mediation:** must be always a single node. It orchestrates events from Alfresco Repository.
* **Metadata:** is responsible for indexing node metadata.
* **Content:** indexes content.
* **Path:** indexes the path of a node.

Additionally, a Kubernetes job will be started to reindex existing content in Search Enterprise. It is recommended you only run this job at the initial startup. You can enable or disable the setting in the `alfresco-elasticsearch-connector.reindexing.enabled` property file by using `true` or `false`.

To deploy Content Services with the Elasticsearch connector:

 ```bash
 helm install acs alfresco/alfresco-content-services \
 --values esc_values.yaml \
 --set externalPort="80" \
 --set externalProtocol="http" \
 --set externalHost="localhost" \
 --set global.alfrescoRegistryPullSecrets=my-registry-secrets \
 --set repository.replicaCount=1 \
 --set transformrouter.replicaCount=1 \
 --set pdfrenderer.replicaCount=1 \
 --set imagemagick.replicaCount=1 \
 --set libreoffice.replicaCount=1 \
 --set tika.replicaCount=1 \
 --set transformmisc.replicaCount=1 \
 --set postgresql-syncservice.resources.requests.memory="500Mi" \
 --set postgresql-syncservice.resources.limits.memory="500Mi" \
 --set postgresql.resources.requests.memory="500Mi" \
 --set postgresql.resources.limits.memory="500Mi" \
 --set alfresco-search.resources.requests.memory="1000Mi" \
 --set alfresco-search.resources.limits.memory="1000Mi" \
 --set share.resources.limits.memory="1500Mi" \
 --set share.resources.requests.memory="1500Mi" \
 --set repository.resources.limits.memory="2500Mi" \
 --set repository.resources.requests.memory="2500Mi"\
 --timeout 10m0s \
 --namespace=alfresco
 ```

If you are using Docker Desktop locally, you must set `antiAffinity` to `soft` and it is recommended you reduce the Elasticsearch server resources:

```docker
 elasticsearch:
   enabled: true
   antiAffinity: "soft"

   # Shrink default JVM heap.
   esJavaOpts: "-Xmx128m -Xms128m"

   # Allocate smaller chunks of memory per pod.
   resources:
     requests:
       cpu: "100m"
       memory: "512M"
     limits:
       cpu: "1000m"
       memory: "512M"

   # Request smaller persistent volumes.
   volumeClaimTemplate:
     accessModes: [ "ReadWriteOnce" ]
     storageClassName: "hostpath"
     resources:
       requests:
         storage: 100M
```

When the system is up and running, you can access the Kibana console using port forwarding:

```bash
 kubectl port-forward service/acs-kibana 5601:5601 -n alfresco
```

and then you can access the console http://localhost:5601/app/kibana.

If you need access to the Elasticsearch server directly you have to perform the same operation:

```bash
 kubectl port-forward service/elasticsearch-master 9200:9200 -n alfresco
```

and then you can access the server http://localhost:9200/.

More properties that can be used to configure the chart are available [here](https://github.com/Alfresco/acs-deployment/tree/master/helm/alfresco-content-services/charts/alfresco-elasticsearch-connector/README.md){:target="_blank"}.

## Install Elasticsearch server

The Elasticsearch connector uses a standard Elasticsearch server. No additional plugin is required.

Other alternatives may be selected for your Elasticsearch installation, for more see [Installing Elastic Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html){:target="_blank"}. Alternatively, a managed service from [Elasticsearch](https://www.elastic.co/elasticsearch/service){:target="_blank"} or [Amazon AWS](https://aws.amazon.com/elasticsearch-service/){:target="_blank"} can be used.

Both Alfresco Repository and the Elasticsearch connector support communication with the Elasticsearch server using HTTP or HTTPs protocol with or without HTTP Basic Authentication.

> **Note:** The Elasticsearch server does not require any additional software from Alfresco in order to be used by Alfresco Search Enterprise 4.0.
---
title: Supported platforms
---

The following are the supported platforms for Search Enterprise 4.0.x:

| Version | Notes |
| ------- | ----- |
| Content Services 23.x | Including ActiveMQ, Alfresco Transform Service, and the database |
|  | Check the [Alfresco Content Services Supported platforms]({% link content-services/latest/support/index.md %}) page for specific versions of the individual components. |
| | |
| **Java** | |
| JDK 17 or OpenJDK 17 | |
| | |
| Elasticsearch server 7.17.x | |
| Elasticsearch server 7.16.x | |
| Elasticsearch server 7.15.x | |
| Elasticsearch server 7.14.x | |
| Elasticsearch server 7.13.x | |
| Elasticsearch server 7.12.x | |
| Elasticsearch server 7.11.x | |
| Elasticsearch server 7.10.x | |
| Opensearch server 1.3.x | |
| | |
| **Applications** | |
| Alfresco Enterprise Viewer 4.0.x | |

> **Note:** Elasticsearch/Opensearch does not require any additional software from Alfresco in order to be used by Alfresco Search Enterprise 4.0.
---
title: Upgrade to Search Enterprise
---

Use this information to upgrade from Search Services 2.x to Search Enterprise 4.x.

> **Note:** A full re-index is required when you upgrade from Search Services 2.x to Search Enterprise 4.x because the search engine is switching from Solr to Elasticsearch. If it is necessary for you to have a backup of the old SOLR index, then it must be copied elsewhere before you re-index.

Search Enterprise 4.x is compatible with Alfresco Content Services 7.1 and above, which means you need to upgrade to this version before applying the following steps.

## Configure Subsystem in Repository

Before upgrading you must activate and configure the Search Services subsystem in Content Services, for more see [Subsystem]({% link search-enterprise/latest/install/index.md %}#configure-subsystem-in-repository).

## Install Elasticsearch connector

The Elasticsearch connector can be installed using JAR files, Docker compose, or Helm, for more see [Install]({% link search-enterprise/latest/install/index.md %}).

Once everything is up and running, use the Elasticsearch connector Re-indexing application to populate the Elasticsearch index. This operation may take a while, depending on the number of documents in your repository and on the indexing options selected (metadata, content and path). While the re-indexing process is progressing, the documents will gradually be available for searching.

When the Re-indexing application has finished, the new and updated documents will be uploaded to the Elasticsearch index by the Elasticsearch connector service using ActiveMQ messages.

## Replicate an existing Content Services 7.1 (and above) deployment

Your current Content Services stack can continue to run while you are indexing the repository to Elasticsearch. This means you can continue to use the 'old' service until the process completes. It's recommended you create a read replica of the database so the indexing process won't affect service performance.

![replicated-environment]({% link search-enterprise/images/elasticsearch-upgrading-1.png %})

1. Create a read-only Replica for your database.

2. Configure Alfresco Repository Search Subsystem to use `elasticsearch` and switch database configuration to the read-only replica database.

3. Install the Elasticsearch server.

4. Install Elasticsearch connector.

5. Once everything is up and running, use the Elasticsearch connector Re-indexing application to populate the Elasticsearch index. This operation may take a while, depending on the number of documents in your Repository and on the indexing options selected (metadata, content and path).

6. Test the replicated environment is working as expected in terms of searching and indexing operations.

7. Switch the existing production environment to the replicated environment by using the original database and removing the previous Search Services components based on SOLR.

![upgraded-environment]({% link search-enterprise/images/elasticsearch-upgrading-2.png %})

> **Note:** You may need to use the Elasticsearch Re-indexing application to update to the latest changes. After that, new and updated documents will be uploaded to the Elasticsearch index by the Elasticsearch connector service using ActiveMQ messages.

## Zero downtime upgrade

You can upgrade from Search Services 2.x without experiencing any downtime, to Search Enterprise 4.x when you are using Content Services 7.2 and above.

1. Start an Elasticsearch 4.x instance, for more see [Overview]({% link search-enterprise/latest/install/index.md %}).

    Currently your installation is using Solr.

    ![add-empty]({% link search-enterprise/images/add-empty-elasticsearch.png %})

2. Start a mirrored environment by replicating the content repository and Content Services.

    You create a mirrored environment because the upgrade will not impact the primary environment. Use the Elasticsearch instance you created as the content repository for the mirrored environment. Once you have mirrored the environment do not change the content repository and only use it in read-only mode. If you do not need to preserve the content repository then you only need to mirror Content Services.

    ![mirror-acs]({% link search-enterprise/images/mirror-acs-environment.png %})

3. Create an Elasticsearch index by executing a search query on the mirrored environment.

    Verify the index is created and its metadata correctly reflects your data model.

    > **Note:** The index is not created when you mirrored the content repository and Content Services.

4. Populate the index with existing data.

    The index is populated and is based on the replicated database and is achieved by starting re-indexing on the mirrored environment. For more see [re-indexing]({% link search-enterprise/latest/config/index.md %}#alfresco-re-indexing-app).

    > **Note:** A window displays that states the primary database does not reflect the up to date index.

    ![initial-reindexing]({% link search-enterprise/images/initial-re-indexing.png %})

5. Shutdown the mirrored environment.

    You are left with an Elasticsearch server with a populated index.

    > **Note:** The index is not yet in sync with the primary environment.

    ![shutdown-mirrored]({% link search-enterprise/images/shutdown-mirrored.png %})

6. Keep your index up to date with changes made through Content Services.

    To do this start live indexing on the primary environment. For more see [live-indexing]({% link search-enterprise/latest/config/index.md %}#alfresco-live-indexing-app).

    > **Note:** Even after starting live indexing there is still a gap from when you took a snapshot to when you started live indexing.

    ![start-live-indexing]({% link search-enterprise/images/start-live-indexing.png %})

7. Start re-indexing on the Solr environment.

    To close the gap in the Elasticsearch index start re-indexing on the Solr environment.

    > **Note:** Live indexing keeps the Elasticsearch environment index up to date.

    ![final-reindexing]({% link search-enterprise/images/final-re-Indexing.png %})

8. Switch to Elasticsearch.

    To switch to Elasticsearch access the Admin Console at runtime. Once you have done this you still have both Search Services and Search Enterprise running but Content Services is using Elasticsearch.

   > **Note:** If you experience any issues you can still revert back to using Solr.

    ![switch-elasticsearch]({% link search-enterprise/images/switch-elasticsearch.png %})

9. Shutdown Search Services.

    Confirm your new environment is working as expected and remove all the Solr based search services.

    ![shutdown-solr]({% link search-enterprise/images/shutdown-solr.png %})

## Upgrade from legacy Content Services

You can upgrade from the legacy versions of Content Services 5.2.x and 6.2.x with Search Services (Solr) to Content Services 7.x with Search Enterprise. You can do this with minimal performance impact on your production environment, and you do not need to reindex Solr. 

1. Start an Elasticsearch 4.x instance, for more see [Overview]({% link search-enterprise/latest/install/index.md %}).

    Currently your installation is using Solr.

    ![start-elasticsearch]({% link search-enterprise/images/start-elasticsearch.png %})

2. Start a mirrored environment by replicating the content repository and Content Services.

    You create a mirrored environment because the upgrade will not impact the primary environment. Use the Elasticsearch instance you created as the content repository for the mirrored environment. Once you have mirrored the environment do not change the content repository and only use it in read-only mode. If you do not need to preserve the content repository then you only need to mirror Content Services.

    ![start-mirrored]({% link search-enterprise/images/start-mirrored.png %})

    The goal of this step is to have a similar environment as you would have after doing a regular upgrade. If any custom upgrade procedure is required you can also apply it to the mirrored environment.The mirrored environment uses the same content store as the production one. During the metadata upgrade on the mirrored environment some content could be created. This should not affect the live environment because it won’t be referenced by the live metadata Store. This is a compromise between replicating the whole content store which can be time consuming and expensive, and having a small amount of unreferenced data. If it’s not possible to share the content store then a replicated content store can be used.

    > **Important:** The mirrored environment is used just to populate the Elasticsearch index. It’s important that this environment is isolated from the live environment i.e. do not join it to the production cluster or access the live metadata store.
3. Create an Elasticsearch index by executing a search query on the mirrored environment.

    Verify the index is created and its metadata correctly reflects your data model.

    > **Note:** The index is not created when you mirrored the content repository and Content Services.
    ![elastic-index]({% link search-enterprise/images/elastic-index.png %})

4. Populate the index with existing data.

    The index is populated and is based on the replicated database and is achieved by starting re-indexing on the mirrored environment. For more see [re-indexing]({% link search-enterprise/latest/config/index.md %}#alfresco-re-indexing-app).

    > **Note:** A window displays that states the primary database does not reflect the up to date index.
    ![populate-index]({% link search-enterprise/images/populate-index.png %})

5. Shutdown the mirrored environment.

    You are left with an Elasticsearch server with a populated index.

    > **Note:** The index is not yet in sync with the primary environment.
    ![shutdown-mirrored-two]({% link search-enterprise/images/shutdown-mirrored-two.png %})

6. Upgrade the initial environment.

    You now have a legacy version of Content Services using Solr and an Elasticsearch server that has an almost complete version of the index. Upgrade the legacy environment and then switch the search engine from Solr to Elasticsearch.

    ![upgrading-initial-enviro]({% link search-enterprise/images/upgrading-initial-enviro.png %})

7. Close the gap in the Elasticsearch index.

    You do this by starting the Elasticsearch re-indexing component, and only for the data modified after taking the snapshot you created for the mirrored environment.

    ![close-elasticsearch-gap]({% link search-enterprise/images/close-elasticsearch-gap.png %})

8. Wait for re-indexing to complete.

    Once re-indexing is complete you have upgraded Content Services to have an up to date Elasticsearch index.

    ![final-state]({% link search-enterprise/images/final-state.png %})

Once this has completed the work can be summarized with the diagram below.

![end-user-perspective]({% link search-enterprise/images/end-user-perspective.png %})---
title: Field queries
---

The fields listed and the corresponding query execution behavior are common to AFTS, Lucene, and CMIS query languages.

## Type and Aspect Queries

Type and Aspect queries have several things in common and both of them expect a name as the field value, specifically:

* If the value is an unqualified name it will be expanded to a fully qualified name using the default namespace.
* If the value is a prefixed name the prefix is expanded, for example `cm:name => {http://www.alfresco.org/model/content/1.0}content}name`.
* If the value is a fully qualified name then it is used in that form.

**Important:** Prefix and wildcard queries in the namespace part, for example `TYPE:{http://www.*}person` won't work, whereas `TYPE:{http://www.alfresco.org/model/content/1.0}pers*` does work. Descendant expansion in prefix and wildcard queries, for example `TYPE: cm:pers*` will not expand to `cm:person descendants`.

## ALL (Field, Prefix, Range, Wildcard, Fuzzy)

The ALL virtual field (i.e. it is not in the index) expands to all fields defined:

* In `SearchParameters::allAttributes` (the object representation of the corresponding attribute in the ReST API search request) or if they are empty in `DictionaryService::getAllProperties`.

## SITE (Field)

The `SITE` virtual field allows you to limit the search results of a given site. This example describes how to narrow down your search results to a single site called `mysite`:

```afts
test AND SITE:mysite
```

You can limit the results to **any** site. To do this you need to use a special site value `_ALL_SITES_`, for example:

```afts
test AND SITE:_ALL_SITES_
```

You can use the `_EVERYTHING_` special value when the `SITE` condition should be ignored, for example:

```afts
test AND SITE:_EVERYTHING_
```

## TEXT (Field, Prefix, Range, Wildcard, Fuzzy)

The TEXT virtual field (i.e. it is not in the index) expands to all fields defined:

* In `SearchParameters::textAttributes` (the object representation of the corresponding attribute in the ReST API Search Request) or if they are empty, the `AlfrescoDefaultTextFields` (i.e. `cm:name`, `cm:title`, `cm:description`, `cm:content`).
This generates a term centric multi-field query:

For example:

```afts
TEXT:(test AND file AND term3 )
```

This query is expanded to:

```afts
(cm:title:test OR cm:name:test OR cm:description:test OR cm:content:test) AND
(cm:title:file OR cm:name:file OR cm:description:file OR cm:content:file) AND
(cm:title:term3 OR cm:name:term3 OR cm:description:term3 OR cm:content:term3)
```

> **Note:** This means that a full query in AND matches documents that contains all the terms in the query, in any of the fields involved.

## DataType (Field, Prefix, Range, Wildcard, Fuzzy)

This query is executed when the field name corresponds to a `datatype` definition using its prefixed or fully qualified form, for example `d:text, {http://www.alfresco.org/model/dictionary/1.0}text)`.

The query produced is a boolean query which includes an optional clause for each property associated to the input `datatype` definition.

## Permission Queries

Fields that are related to ACL information are stored directly as part of the Elasticsearch documents. As a consequence of that, the corresponding queries are plain `term`/ `range` / `prefix` / `fuzzy` queries using the following fields:

* Property (Field, Prefix, Range, Wildcard, Fuzzy)  
* OWNER (Field, Prefix, Wildcard, Fuzzy)
* READER (Field, Prefix, Wildcard, Fuzzy)
* AUTHORITY (Field, Prefix, Wildcard, Fuzzy)
* DENIED (Field, Prefix, Wildcard, Fuzzy)

## ID (Field, Prefix, Wildcard)

The ID (virtual) field maps to an Elasticsearch document id (_id) and it corresponds to the Alfresco node identifier, for example `5fef4b5d-4527-40e5-94fa-1878ef7a54eb`.

## EXISTS (Field)

The query intent can be summarized in “give me all nodes that have a value for the property/field I requested”. This is very similar to the previous one, the difference is that the `NULLPROPERTIES` field is not involved in this scenario.

The value of a clause whose field is `EXISTS` could be:

* An unqualified name will be expanded to a fully qualified name using the default namespace.
* a prefixed name is expanded, for example `cm:name => {http://..}content}name)`.
* a fully qualified name.
* a field name, for example ID, OWNER, READER.

If the value is associated to a property definition then a boolean query is executed that has the following clause:

* `PROPERTIES` (MUST) Otherwise, in case of a field (e.g. OWNER, ID, READER) a wildcard query is built using that field, for example `OWNER:*`.
---
title: Filtering Paging and Sorting
---

## Searching by content type and controlling paging and sorting

The V1 ReST APIs paging can also be controlled but is accomplished via the body rather than a query parameter. The results can also be sorted. The body example shows how to execute a search to find all files ordered by the `cm:name` property. It shows how you can search for a specific content type with the `TYPE` keyword. It also only shows 25 results rather than the default 100 including skipping the first 10 results.

```json
{
  "query": {
    "query": "+TYPE:\"cm:content\"",
    "language": "afts"
  },
  "paging": {
    "maxItems": "25",
    "skipCount": "10"
  },
  "sort": [{"type":"FIELD", "field":"cm:name", "ascending":"false"}]
}
```

This is what the call looks like assuming you have stored the query JSON data in a file called `paging-sort-query.json`:

```bash
$ curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' --header 'Authorization: Basic VElDS0VUXzIxYzAzOWMxNjFjYzljMDNmNmNlMzAwYzAyMDY5YTQ2OTQwZmYzZmM=' --data-binary '@paging-sort-query.json' 'http://localhost:8080/alfresco/api/-default-/public/search/versions/1/search' | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 13836    0 13622  100   214  31387    493 --:--:-- --:--:-- --:--:-- 31880
{
  "list": {
    "pagination": {
      "count": 25,
      "hasMoreItems": true,
      "skipCount": 10,
      "maxItems": 25
    },
    "entries": [
      {
        "entry": {
           "name": "WebSiteReview.mp4",
...        }
      },
      {
        "entry": {
           "name": "turbine.JPG",
...        }
      },
      {
        "entry": {
           "name": "translatable.ftl",
...        }
      },
      {
        "entry": {
          "name": "text-file.txt",
...        }
      },
      {
          "name": "test return value.js.sample",
...        }
      },
      {
        "entry": {
          "name": "test-file.txt",
...        }
      },
      {
          "name": "system-overview.html",
...        }
      },
      {
        "entry": {
          "name": "start-pooled-review-workflow.js",
...        }
      },
      {
        "entry": {
          "name": "some-stuff.txt",
...        }
      },
      {
        "entry": {
          "name": "somefile.txt",
...        }
      },
 ...
    ]
  }
}
```

The results have been truncated for clarity.

## Faceted search

There are two types of facet queries, and fields. A query facet returns the count of results for the given query. You can provide multiple facet queries in one request. A field facet returns a number of "buckets" for a field, providing the count of results that fit into each bucket.

The example body shows a search request that looks for files that have a `cm:name` or `cm:title` starting with "test". You can also specify if you want to know how many of the results are small files, how many are plain text files, how many are images, and how many are Office files. Additionally, the `creator` facet field is included, which indicates how many of the results were created by each user:

```json
{
  "query": {
    "query": "(name:\"test*\" OR title:\"test*\") AND TYPE:\"cm:content\""
  },
  "facetQueries": [
    {"query": "content.size:[0 TO 10240]", "label": "Small Files"},
    {"query": "content.mimetype:'text/plain'", "label": "Plain Text"},
    {"query": "content.mimetype:'image/jpeg' OR content.mimetype:'image/png' OR content.mimetype:'image/gif'", "label": "Images"},
    {"query": "content.mimetype:'application/msword' OR content.mimetype:'application/vnd.ms-excel'", "label": "Office"}
  ], 
  "facetFields": {"facets": [{"field": "creator"}]}
}
```

This is what the call looks like assuming you have stored the query JSON data in a file called `facet-query.json`:

```bash
$ curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' --header 'Authorization: Basic VElDS0VUXzIxYzAzOWMxNjFjYzljMDNmNmNlMzAwYzAyMDY5YTQ2OTQwZmYzZmM=' --data-binary '@facet-query.json' 'http://localhost:8080/alfresco/api/-default-/public/search/versions/1/search' | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  6359    0  5793  100   566   141k  14150 --:--:-- --:--:-- --:--:--  159k
{
  "list": {
    "pagination": {
      "count": 9,
      "hasMoreItems": false,
      "totalItems": 9,
      "skipCount": 0,
      "maxItems": 100
    },
    "context": {
      "consistency": {
        "lastTxId": 193
      },
      "facetQueries": [
        {
          "label": "Office",
          "filterQuery": "content.mimetype:'application/msword' OR content.mimetype:'application/vnd.ms-excel'",
          "count": 3
        },
        {
          "label": "Small Files",
          "filterQuery": "content.size:[0 TO 10240]",
          "count": 3
        },
        {
          "label": "Plain Text",
          "filterQuery": "content.mimetype:'text/plain'",
          "count": 1
        },
        {
          "label": "Images",
          "filterQuery": "content.mimetype:'image/jpeg' OR content.mimetype:'image/png' OR content.mimetype:'image/gif'",
          "count": 3
        }
      ],
      "facetsFields": [
        {
          "label": "creator",
          "buckets": [
            {
              "label": "admin",
              "filterQuery": "creator:\"admin\"",
              "count": 9,
              "display": "Administrator"
            }
          ]
        }
      ]
    },
    "entries": [
      {
        "entry": {
          "isFile": true,
          "createdByUser": {
            "id": "admin",
            "displayName": "Administrator"
          },
          "modifiedAt": "2019-11-07T10:43:43.279+0000",
          "nodeType": "cm:content",
          "content": {
            "mimeType": "text/plain",
            "mimeTypeName": "Plain Text",
            "sizeInBytes": 9,
            "encoding": "UTF-8"
          },
          "parentId": "6b661ba4-830b-457d-af04-46f174351536",
          "createdAt": "2019-11-07T10:43:43.279+0000",
          "isFolder": false,
          "search": {
            "score": 1
          },
          "modifiedByUser": {
            "id": "admin",
            "displayName": "Administrator"
          },
          "name": "test-file.txt",
          "location": "nodes",
          "id": "9613e418-b1c1-4889-8866-4dccda66a258"
        }
      },
      ...
    ]
  }
}
```

The `facetQueries` object has an entry for each query supplied in the result whereas the `facetsFields` object contains an entry for each requested field which in turn contains the count for each bucket.
---
title: Search query syntax
---

Alfresco Search Enterprise supported search query syntax.

## Applications and Frameworks

* [ADF Search Components](https://www.alfresco.com/abn/adf/docs/){:target="_blank"}
* [ACA - Alfresco Content Application](https://github.com/alfresco/alfresco-content-app){:target="_blank"}
* [Alfresco Digital Workspace]({% link digital-workspace/latest/index.md %})
* [ReST API (only when using FTS search syntax)]({% link content-services/latest/develop/rest-api-guide/searching.md %})

> **Note:** Alfresco Share web application is not supported

## Search Features

* ACL Permission checks
* Sorting by relevancy
* [Searching by content type and controlling paging and sorting]({% link content-services/latest/develop/rest-api-guide/searching.md %}#searching-by-content-type-and-controlling-paging-and-sorting)
* [Faceted search]({% link content-services/latest/develop/rest-api-guide/searching.md %}#faceted-search)
* Filter by content size and mimetype
* Inclusion of additional properties in search results

## Search for a single term

Single terms are tokenized before the search according to the appropriate data dictionary definition(s).

If you do not specify a field, it will search in the content and in the following properties: name, title and description. This is a shortcut for searching *all properties of type content*. Terms can not contain a whitespace.

```bash
banana
TEXT:banana
```

Both of these queries will find any nodes with the word "banana" in any property of type `d:content`, however the first one will also get results from properties `cm:name`, `cm:title` or `cm:description`.

If the appropriate data dictionary definition(s) for the field supports both FTS and un-tokenized search, then FTS search will be used. FTS will include synonyms if the analyzer generates them.

## Search in fields

Search specific fields rather than the default. Terms, and phrases can all be preceded by a field. If not the default field `TEXT` is used.

```bash
field:term
field:"phrase"
field:'phrase'
=field:exact
~field:expand
```

> **Note:** Exact Term searching, using the equals operator (`=field:exact` in the samples above) is only allowed if the default Alfresco Repository configuration has been changed to enable this feature.

Fields fall into three types, property fields, special fields, and fields for data types. Property fields evaluate the search term against a particular property, special fields are described in the following table, and data type fields evaluate the search term against all properties of the given type.

|Type|Description|
|-----------|----|
|Property|Fully qualified property, for example `{http://www.alfresco.org/model/content/1.0}name:apple`.|
|Property|Fully qualified property, for example `@{http://www.alfresco.org/model/content/1.0}name:apple`.|
|Property|CMIS style property, for example `cm_name:apple`.|
|Property|Prefix style property, for example `cm:name:apple`.|
|Property|Prefix style property, for example `@cm:name:apple`.|
|Property|ID, for example `ID:'599a6862-070c-49a7-a744-b88da949c31e'`.|
|Property|TEXT, for example `TEXT:apple`.|
|Property|OWNER, for example `OWNER:'admin'`.|
|Property|READER, for example `READER:'GROUP_EVERYONE'`.|
|Property|DENIED, for example `DENIED:'GROUP_EVERYONE'`.|
|Special|TYPE, for example `TYPE:"qname"`.|
|Special|ASPECT, for example `ASPECT:"qname"`.|
|Special|SITE, for example `SITE:"shortname of the site"`.|
|Special|TAG, for example `TAG:"name of the tag"`.|
|Special|ALL, for example `ALL:'admin'`.|
|Special|EXISTS, for example `EXISTS cm:name:'Sample-Document.docx'`.|
|Special|ISNODE, for example `ISNODE cm:name:'Sample-Document.docx'`.|
|Field for Data Type|Fully qualified Data Type, for example `{http://www.alfresco.org/model/dictionary/1.0}content:apple`.|
|Field for Data Type|Data Type style property, for example `d:content:apple`.|

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

## Search for a phrase

Phrases are enclosed in double quotes. Any embedded quotes can be escaped using ''. If no field is specified then the default `TEXT` field will be used, as with searches for a single term.

The whole phrase will be tokenized before the search according to the appropriate data dictionary definition(s).

```afts
"big yellow banana"
```

## Search for wildcards

Wildcards are supported in terms, phrases, and exact phrases using `*` to match zero, one, or more characters and `?` to match a single character.

The `*` wildcard character can appear on its own and implies Google-style. The "anywhere after" wildcard pattern can be combined with the `=` prefix for identifier based pattern matching. Search will return and highlight any word that begins with the root of the word truncated by the `*` wildcard character.

All of the following will find the term apple.

```afts
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

> **Note:** Exact Term searching, using the equals operator (`=*ple` in the samples above), is only allowed if the default Alfresco Repository configuration has been changed in order to enable this feature.

When performing a search that includes a wildcard character, it is best to wrap your search term in double quotation marks. This ensures all metadata and content are searched.

## Search for conjunctions

Single terms, and phrases can be combined using `AND` in upper, lower, or mixed case.

The `AND` operator is interpreted as "every term is required".

```afts
big AND yellow
```

These queries search for nodes that contain all the terms `big` and `yellow` in any content or in properties `cm:name`, `cm:title` or `cm:description`.

### Search for disjunctions

Single terms, and phrases can be combined using `OR` in upper, lower, or mixed case.

The `OR` operator is interpreted as "at least one is required, more than one or all can be returned".

By default search fragments will be `ORed` together.

```text
big yellow banana
big OR yellow OR banana
TEXT:big TEXT:yellow TEXT:banana
TEXT:big OR TEXT:yellow OR TEXT:banana
```

These queries search for nodes that contain at least one of the terms `big`, `yellow`, or `banana` in any content. The first two will also get results from properties `cm:name`, `cm:title` or `cm:description`.

## Search for negation

You can narrow your search results by excluding words with the `NOT` syntax. Single terms, and phrases can be combined using “`NOT`” in upper, lower, or mixed case, or prefixed with “`!`” or “`-`”. These queries search for nodes that contain the terms yellow in any content.

```text
yellow NOT banana
yellow !banana
yellow -banana
NOT yellow banana
-yellow banana
!yellow banana
```

> **Note:** In the three initial samples above, since `OR` is the default operator for searching, the results are expected to include every node with "yellow" and every node without the "banana" term. If you want to get nodes with the "yellow" term and without the term "banana", use the following expression: `yellow AND NOT banana`.

The `NOT` operator can only be used for string keywords and doesn’t work for numerals or dates.

Prefixing any search qualifier with a `-` excludes all results that are matched by that qualifier.

## Search for optional, mandatory, and excluded elements of a query

Sometimes `AND` and `OR` are not enough. If you want to find documents that must contain the term "car", score those with the term "red" higher, but do not match those just containing "red".

|Operator|Description|
|--------|-----------|
|","|The field, phrase, group is optional; a match increases the score.|
|"+"|The field, phrase, group is mandatory. |
|"-", "!"|The field, phrase, group must not match.|

The following example finds documents that contain the term "car", score those with the term "red" higher, but does not match those just containing "red":

```afts
+car |red
```

> **Note:** At least one element of a query must match, or not match, for there to be any results.

All `AND` and `OR` constructs can be expressed with these operators.

## Escaping characters

Any character can be escaped using the backslash "`\`" in terms, IDs (field identifiers), and phrases. Java unicode escape sequences are supported. Whitespace can be escaped in terms and IDs.

For example:

```afts
cm:my\ content:my\ name
```

## Search for ranges

Inclusive ranges can be specified in Google-style. There is an extended syntax for more complex ranges. Unbounded ranges can be defined using MIN and MAX for numeric and date types and "u0000" and "FFFF" for text (anything that is invalid).

|Lucene/CMIS|Google|Description|Example|
|------|------|-----------|-------|
|`[#1 TO #2]`|`#1..#2`|The range #1 to #2 inclusive ``#1 <= x <= #2``|`0..5``[0 TO 5]`|
|`<#1 TO #2]`| |The range #1 to #2 including #2 but not #1.`#1 < x <= #2`|`<0 TO 5]`|
|`[#1 TO #2>`| |The range #1 to #2 including #1 but not #2.`#1 <= x < #2`|`[0 TO 5>`|
|`<#1 TO #2>`| |The range #1 to #2 exclusive.`#1 < x < #2`|`<0 TO 5>`|

```afts
TEXT:apple..banana
my:int:[0 TO 10]
my:float:2.5..3.5
my:float:0..MAX
mt:text:[l TO "uFFFF"]
```

When searching for a date range you can use a partial date. Elasticsearch replaces the missing date components with the values below:

* Month of year: 01
* Day of month: 01
* Hour of day: 23
* Minute of hours:  59
* Second of minute: 59
* Nano of second:   999_999_999

The last four items will be replaced with 0 when the date component is missing in the minimum date in a range expression, e.g. [1950 to 2021] will be executed as [1950-01-01T00:00:00 TO 2021-01-01T23:59:59].

In the REST API you can specify the timezone to be used in search for date ranges.

```json
{
    "query": {
        "query": "cm:created:['2021-05-01T09:00:00' TO '2021-05-28T09:05:59']",
        "language": "afts"
    },
    "localization": {
        "timezone": "Asia/Yerevan"
    }
}
```

## Query time boosts

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

### Search using date math

Date range queries can be more powerful when applying date math functions. AFTS supports adding and subtracting periods, as well as rounding:

| AFTS query | Description |
| ---------- | ----------- |
| `acme:projectStartDate:[NOW TO NOW+1DAY>` | Documents that have a project start date in the next twenty four hours. |
| `acme:projectStartDate:[NOW/DAY TO NOW/DAY+1DAY>` | Documents that have a project start date from the current day. The current day is defined as from midnight to midnight (UTC), **Note:** The subtle difference between this query and the one above. |
| `acme:projectStartDate:[NOW-1MONTH/YEAR TO NOW-1MONTH/YEAR+1DAY>` | Documents with a project start date in the first day of the current year, or in the first day of last year if it is currently January. **Note:** It's possible to chain date math functions together. |
| `cm:created:[2020-11-01T12:34:00/YEAR TO NOW>` | Documents that were created since the the start of 2020. **Note:** It's also possible to apply date math to absolute points in time. |

All of these examples have used an inclusive lower bound and an exclusive upper bound. Other bounds can be used but Search Enterprise performs rounding based on the type of bound being used:

| AFTS Bound | Description | Elasticsearch rounding behaviour |
| ---------- | ------- | ----------------------- |
| `[NOW/YEAR TO ...` | Inclusive lower bound. | From the start of the current year. |
| `<NOW/YEAR TO ...` | Exclusive lower bound. | After the end of the current year. |
| `... TO NOW/YEAR]` | Inclusive upper bound. | Until the end of the current year. |
| `... TO NOW/YEAR>` | Exclusive upper bound. | Before the start of the current year. |

For more details see the [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html#range-query-date-math-rounding).

## Search for an exact term

> **Note:** Exact Term searching is only allowed if the default Alfresco Repository configuration has been changed in order to enable this feature, for more see [Pre-indexing considerations]({% link search-enterprise/latest/admin/index.md %}#pre-indexing-considerations).

To search for an exact term you must prefix it with "=". The supported syntax:

```afts
=term
=term1 =term2
="multi term phrase"
=field:term
=field:term1 =field:term2
=field:“multi term phrase”
```

If you don’t specify a field the search runs against name, description, title, and content. If the field specified is `TOKENIZED=false`, only the full field is matched. If the field you specified is `TOKENIZED=TRUE` or `TOKENIZED=BOTH` then the search is run on the cross locale tokenized version of the field.

> **Note:** Exact Term Search is disabled by default, for more see [Pre-indexing considerations]({% link search-enterprise/latest/admin/index.md %}#pre-indexing-considerations).

## Searches that involve stopwords

[Stopwords](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-stop-tokenfilter.html#analysis-stop-tokenfilter-stop-words-by-lang){:target="_blank"} are removed from the query.

For example:

```afts
stopword1 quick fox stopword2 brown
```

becomes

```afts
quick fox brown
```

This behavior is different from Search and Insight Engine and Search Services in that it keeps stopwords in the query to build positional queries, for example:

```afts
stopword1 quick fox stopword2 brown
```

becomes

```afts
stopword1_quick quick fox_stopword2 fox stopword2_brown brown
```

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

## Requesting optional item information

We have taken what we're calling a "performance first" approach with the API. This means that each endpoint, by default, only returns the item information that is efficient to retrieve.

If additional processing is required on the server side to obtain the item information, then it's made available via the `include` query parameter.

The `http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/-my-/children?include=properties,aspectNames` request shows how you can also include the properties and aspects for each node in your home folder when listing its children.

As with the `orderBy` and `where` parameters, the `include` parameter is specific to the endpoint so you’ll need to consult the API Explorer to see what extra item information is available.
---
title: Query languages
---

AFTS is the primary query language for use with Search Enterprise. In addition to AFTS the Lucene, and CMIS query languages are also supported. If you require any additional queries to be written in the future, Alfresco recommends the use of AFTS.

The search string syntax depends on the given query language and can differ significantly between AFTS, Lucene, and CMIS. However, there are some shared aspects that provide the same behavior in the languages, for more see [Field queries]({% link search-enterprise/latest/using/field.md %}).

For a list of unsupported features see [Unsupported]({% link search-enterprise/latest/using/unsupported.md %}).

## Lucene query language

The Lucene language is provided by the IR framework and the query API is built on top of the Lucene standard query parser. For more details see [Apache Lucene - Query Parser Syntax](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html){:target="_blank"}. The Search Enterprise documentation provides Apache Lucene - Query Parser Syntax information specific to Alfresco.

Properties are attributes defined in an Alfresco content model. They are identified by qualified names, meaning they are composed of:

* a namespace
* a local name

This avoids conflicts between local names used in multiple models, for example `finance:name` and `cm:name`.

A property can be declared in queries using three notations:

* Unqualified name, for example `title`. In this case it will be associated to the default namespace. The property is therefore assumed to exist and to be valid in the default content model.

```afts
@title:OOP
@title:(Object Oriented Programming)
```

* Prefixed name, for example `cm:title`. The prefix is the short form of a given namespace. It must be uniquely associated to a namespace and to a content model.

```afts
@cm:title:OOP
@cm:title:(Object Oriented Programming)
```

* Fully qualified name. In this case the property name uses the full namespace and the local name.

```http
@{http://www.alfresco.org/model/content/1.0}title:OOP
@{http://www.alfresco.org/model/content/1.0}title:(Object Oriented Programming)
```

When prefixes and fully qualified names are used, the property has to be prefixed with the @ symbol and this is one of the main differences between AFTS and Lucene. Special characters (i.e. characters that have a special meaning in Lucene) need to be escaped using the backslash.

## CMIS query language

The CMIS query language can be used with the Search Enterprise v1 REST API or by using the CMIS interface. CMIS is often used when you migrate to or from Alfresco. If you want to use the v1 REST API you must indicate this by using the parameter `language=CMIS`. The [CMIS specification](https://docs.oasis-open.org/cmis/CMIS/v1.1/CMIS-v1.1.html){:target="_blank"} outlines the usable search query syntax. Queries run with CMIS are generally used to make sure that what you have imported has worked correctly. You can also use third-party tools that use CMIS as their query language.

> **Note:** When checking equality of a string field `SELECT * FROM cmis:document WHERE abc:stringfield = 'stringvalue'` when using the exact term search feature, it is important to consider how the field is indexed. For more details see [Exact term search]({% link search-enterprise/latest/config/index.md %}#exact-term-search).

### CMIS queries

These are some examples of the CMIS query language.

```sql
- strict queries
SELECT * FROM Document WHERE CONTAINS("quick")
- Alfresco extensions
SELECT * FROM Document D WHERE CONTAINS(D, 'cmis:name:\'Tutorial\'')
SELECT cmis:name as BOO FROM Document D WHERE CONTAINS('BOO:\'Tutorial\'')
```

```sql
Simple select examples - unfiltered
SELECT * FROM cmis:document
SELECT * FROM cm:person
```

```sql
Select with where clauses
SELECT * FROM cmis:folder WHERE cmis:description IS NOT NULL
SELECT * FROM cmis:document WHERE CONTAINS('apple')
SELECT * FROM cmis:document WHERE cmis:name <> 'carrot.docx'
```

```sql
Joining aspects to filter by properties
SELECT * FROM cmis:document AS D JOIN exif:exif AS E ON D.cmis:objectId = E.cmis:objectId WHERE E.exif:pixelXDimension <= 640
```
---
title: Path queries
---

The PATH field is the Elasticsearch field which contains the `primaryHierarchy` attribute that consists of a list of `noderefs`. Field indexing is different for re-indexing and live indexing components because they rely on different sources of information. The setup sequence for new systems is:

1. RDBMS (re-indexing)

2. Events (live indexing)

The live indexing component populates the PATH field on Elasticsearch documents starting from the `primaryHierarchy` attribute found in the node event. The `primaryHierarchy` attribute captures the primary hierarchy of ancestors of the resource affected, which means the folder path of the content. The first element is the immediate parent. For example this is a node event which contains that information:

```JSON
{
  "specversion": "1.0",
  "type": "org.alfresco.event.node.Created",
  "id": "97c1b36c-c569-4c66-8a31-7a8d0b6b804a",
  "source": "/f6d21231-618e-4f12-a920-e498660c5b9d",
  "time": "2020-04-27T12:37:03.560134+01:00",
  "dataschema": "https://api.alfresco.com/schema/event/repo/v1/nodeCreated",
  "datacontenttype": "application/json",
  "data": {
   ...
      "primaryHierarchy": [
        "521aac1c-20eb-444b-a137-2da3d35ee1a8",
        "2641bbe1-39ff-44dc-b47f-736552ad46cc"
      ],
     ... 
    }
  }
}
```

During the first system bootstrap for new systems the initial folder hierarchy is created before the event subsystem is started. This means standard folders like `Company home`, `Data dictionary`, and `Sites` are not going to be picked up by the live indexing component. Due to this some members of the `primaryHierarchy` can't be de-referenced. This occurs for new folders and documents that are created after the initial system start up, and because the live indexing component does not have enough information to construct the `PATH` field.

To overcome this scenario the recommended setup sequence for new systems that require PATH query functionality is:

1. Startup new content repository.

2. Perform full re-index

3. Continue with live indexing.

## Nodes / NodeTypes Blacklist

The live indexing and re-indexing components rely on a configuration file which acts as a blacklist, the file contains:

* The list of node types to be excluded from indexing.
* The list of node types with content excluded from indexing.
* The list of property names to be excluded from (metadata) indexing.

The blacklist file path is specified through Spring configuration capabilities, which means:

* A property called `alfresco.mediation.filter-file` in the module `application.properties`.
* A system property called `-Dalfresco.mediation.filter-file`.

The default value of that property is `classpath:mediation-filter.yml` and points to a file that is included in the bundle which provides no rules, i.e.:

```text
mediation:
  nodeTypes:
  contentNodeTypes:
```

When a blacklisted entry is configured you can have specific branches of the repository without PATH queries being indexed for any nodes in them. This can happen if the nodes in the hierarchy are excluded from the index in the modelling, re-indexing, or live indexing component's of the configuration.

If some nodes are excluded from search indexing, then their children's PATH will not be able to be constructed. **Note:** This is even the case when the children themselves are indexed using their metadata and content. The following example is for live indexing:  

1. A node event is received by the Mediation part of the live indexing component.

2. The Mediation detects the node being blacklisted. According to the configuration the node is not sent to Elasticsearch.

3. Another node event arrives.

4. The node within the event has a `primaryHierarchy` attribute whose content refers to the blacklisted node above.  

5. The PATH field cannot be built because there’s at least one member of the `primaryHierarchy` that cannot be dereferenced.

> **Note:** Make sure the live indexing and re-indexing components are pointing to the same blacklist configuration i.e. the same file or different file within the same content, otherwise the runtime filtering applied to nodes will be different depending on which indexing component is executed.

## AFTS category PATH queries

You can search for content within categories when using a `PATH` query. For example, `PATH:"/cm:categoryRoot/cm:general_classifiable/cm:Region/cm:ASIA//*"` will match anything within the `ASIA` category or any of its descendants. It will also match the descendant category nodes, which can be filtered out by type if required.

Solr stores every category path twice, once starting with `/cm:categoryRoot/cm:general_classifiable` and once starting with `/cm:general_classifiable`. Search Enterprise only stores the longer path to reduce the index size. This means that some absolute path queries that work with Solr will need a prefix of `/cm:categoryRoot` to work with Search Enterprise.
---
title: Troubleshooting
---

Use this information to troubleshoot any technical issues you may be experiencing.

## Search for failed Transformations

It is possible to search for all documents that have failed to transform by running a simple query using Kibana or the Elasticsearch REST API:

```json
{
  "query": {
      "term": {
        "cm%3Acontent%2Etr_status": {
          "value": "TRANSFORM_FAILED"
        }
      }
  }
}
```

### Debug queries generated for Elasticsearch

Enabling queries slowly in Elasticsearch with a threshold of `0` seconds, will dump every query received by Elasticsearch in the logs.

```bash
$ curl -XPUT "http://elasticsearch:9200/alfresco/_settings" -H 'Content-Type: application/json' -d'{  
 "index.search.slowlog.threshold.query.warn": "0s",  
 "index.search.slowlog.threshold.query.info": "0s",
 "index.search.slowlog.threshold.query.debug": "0s",  
 "index.search.slowlog.threshold.query.trace": "0s",  
 "index.search.slowlog.threshold.fetch.warn": "0s",  
 "index.search.slowlog.threshold.fetch.info": "0s",  
 "index.search.slowlog.threshold.fetch.debug": "0s",  
 "index.search.slowlog.threshold.fetch.trace": "0s",  
 "index.indexing.slowlog.threshold.index.warn": "0s",  
 "index.indexing.slowlog.threshold.index.info": "0s",  
 "index.indexing.slowlog.threshold.index.debug": "0s",  
 "index.indexing.slowlog.threshold.index.trace": "0s", 
 "index.indexing.slowlog.threshold.index.trace": "0s",
 "index.indexing.slowlog.level": "trace",  
 "index.indexing.slowlog.source": "1000"}'
```---
title: Unsupported features
---

The following features, which were supported with Search and Insight Engine 2.x and Search Services 2.x (Solr) are not supported in the latest release for Search Enterprise 4.x.

## Indexing

* Indexing of nodes created during content repository bootstrap. For example, the sample site data.

## Search features

* Fingerprinting
* Resource limiting
* Scoped search
* Statistics

### Search Syntax

* Fuzzy matching
* Field Facets Pagination
* Field Facets Tags Exclusion

### Field Queries

* PATHWITHREPEATS
* PNAME
* ANAME
* NPATH
* QNAME
* PRIMARYASSOCQNAME
* PRIMARYASSOCTYPEQNAME
* FINGERPRINT
* ISROOT
* ISCONTAINER
* CASCADETX
* DBID
* TX
* TXID
* INTXID
* TXCOMMITTIME
* ACLID
* INACLTXID
* ACLTXID
* ACLTXCOMMITTIME
* TENANT
* OWNERSET
* READERSET
* AUTHSET
* DENYSET
* FTSSTATUS

## Behavior of unsupported fields

Supplying an unsupported or non-existent field will cause a query to fail. This is a change in behavior from Search and Insight Engine and Search Services, which silently ignore these issues.

Search Enterprise focuses on the most commonly used features, and in some cases allows you to work around unsupported features.
The following are examples of how to use different fields for queries:

| Old Query | Replacement Query |
| --------- | ----------------- |
| QNAME:'comment' | TYPE:'fm:post' |
| PNAME:'0/wiki' | PATH:'//cm:wiki/*' |
| NPATH:'2/Company Home/Sites/swsdp' | PATH: '/app:company_home/st:sites/cm:swsdp/*' |
| ANAME:'0/cdefb3a9-8f55-4771-a9e3-06fa370250f6' | PARENT:'cdefb3a9-8f55-4771-a9e3-06fa370250f6' |

## Query languages

* SQL query language using JDBC Driver

## Unsupported data types and properties

Data types and properties supported in Search and Insight Engine 2.x and Search Services 2.x that are not currently supported for Search Enterprise 4.x.

* http&#65279;://www.alfresco.org/model/dictionary/1.0}any
* http&#65279;://www.alfresco.org/model/dictionary/1.0}assocref
* http&#65279;://www.alfresco.org/model/dictionary/1.0}childassocref
* http&#65279;://www.alfresco.org/model/dictionary/1.0}locale
* http&#65279;://www.alfresco.org/model/dictionary/1.0}qname
