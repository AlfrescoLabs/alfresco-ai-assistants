---
title: Alfresco Digital Workspace
---
Alfresco Digital Workspace is a new content management application built with the Alfresco Application Development Framework (ADF). The user interface has been streamlined making simple tasks such as uploading, downloading, searching for content, and collaborating with others much easier. You can create public, moderated, and private libraries. Access for other users to these libraries can be configured by setting permissions, at an individual or group level. Libraries can be added to your favorites list so they can be accessed easily. The search feature is powerful and can be tailored to create customized search forms that can show specific filters based on your metadata. These individualized forms will help you quickly find what you are looking for.

Alfresco Governance Services functionality for end users is available, including record declaration. Alfresco Process Services processes and tasks can also be accessed and completed from Alfresco Digital Workspace.

You can edit and collaborate with colleagues on existing Microsoft Word, Excel, and PowerPoint files you have stored in Alfresco Content Services (originating from Microsoft Office Online) if you use [Alfresco Collaboration Connector for Microsoft 365]({% link microsoft-365/latest/index.md %}).

The Alfresco Digital Workspace simplifies content management and provides comprehensive extensibility features for developers, using ADF, and allows them to easily and quickly create custom solutions for specific use cases.

The Alfresco Digital Workspace is automatically deployed as part of Alfresco Content Services using Helm charts or a Docker Compose file. You can also manually install Alfresco Content Services using standard WAR files and then configure the installation to include Alfresco Digital Workspace.

{% include media.html id="giypeO8Q4cs" %}

## Web Content Accessibility Guidelines (WCAG) 2.1

The Digital Workspace has been independently tested for its accessibility using the WCAG 2.1 AA, Section 508, and EN 301 standards. It complies with these regulations that ensure an online computer-based system is completely accessible by all of the general public, including those with disabilities. See the following websites for more details:

* [Understanding WCAG 2.1](https://www.gov.uk/service-manual/helping-people-to-use-your-service/understanding-wcag){:target="_blank"}
* [WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21){:target="_blank"}
* [Government-wide Section 508 Assessment](https://www.section508.gov/){:target="_blank"}
* [EN 301 549 - Accessibility requirements for ICT products and services](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf){:target="_blank"}
---
title: Configure Digital Workspace
---

Alfresco Digital Workspace settings are in the following file `../digital-workspace/app.config.json`. You can use the file to tailor Alfresco Digital Workspace easily and without making any code changes. The file can be updated while Alfresco Digital Workspace is still running and users will see the changes once their pages are reloaded.

For more in-depth documentation about how to configure Digital Workspace, see [Application features](https://alfresco-content-app.netlify.com/#/features/){:target="_blank"}.

The following settings can be configured in `../digital-workspace/app.config.json`.

| Property/Sub-property | Description |
| --------  | ----------- |
| adf-start-process/name | The name of the process as it appears in Alfresco Process Services including the current days date and time. The default setting for this is %{processDefinition} - %{datetime}, which will produce, 'Capital Approval Process - Jun 17, 2020, 11:02:07 AM'.|
| adf-start-process/processDefinitionName | The name of the definition of the process you are using to create an instance, for example `Capital Approval Process definition`.|
| adf-versions-manager/allowComments | Toggle version comments on/off.|
| aosHost | Server address of the AOS endpoint, for example `https://repository.domain.com/alfresco/aos`. **Note:** Server address has to be https.|
| application/name | Application name that will be shown in the header of the application and in the page/tab title, for example `Digital Workspace`|
| application/copyright | Copyright text shown on the login page, for example `© 2017 - 2020 Alfresco Software, Inc. All rights reserved`.|
| application/logo | Path to the logo shown in the application header for example, `assets/images/alfresco-logo-flower.svg`|
| authtype | Determines the type of authentication. To use Single Sign-on mode you must change this property to OAuth, for example `basic`. See [Single Sign-On (SSO)](https://www.alfresco.com/abn/adf/docs/core/components/login.component/#single-sign-on-sso).|
| bpmHost | Server address of Alfresco Process Services, for example `https://processservices.domain.com:port`|
| content-metadata/presets | Add custom aspects and properties to be shown in the information drawer. |
| content-metadata/custom | Add custom aspects and properties to be shown in the information drawer. |
| ecmHost | Server address of Alfresco Content Services, for example `https://repository.domain.com:port` |
| files/excluded | Restrict users from uploading certain types of files and folders by setting or extending the list of rules at the "files.excluded" path for example, ".DS_Store", "desktop.ini", "Thumbs.db", ".git" | |
| files/match-options, no case | Ensures that the exclusions are case insensitive, for example `true`. |
| files/allowDownload |Toggle downloads of versions on/off, `true` or `false`.|
| headerColor | Value for the header background color of the application, for example `#2196F3` |
| languagePicker | Enable manual language selection menu, `true` or `false`.|
| languages/key | Key for language picker menu options, for example  `en` |
| languages/label | Label to display in the language picker menu, for example, `English`|
| pagination/size | Set the default number of items to be displayed on a page, for example `25` |
| pagination/supportedPageSizes | Change the items available in the pagination control, for example `25`, `50`, `100`. |
| processService | Toggles the Alfresco Process Services plugin to be on/off, `"true"` or `"false"`. **Note:** You must include the quotation marks. |
| search/include | Specify the node information returned by the API with the search results set. |
| search/sortng | Search result sorting options available, and which option is the default.|
| search/filterqueries | Specify what content should, and shouldn’t be returned in the results set.|
| search/facetFields | Allows the configuration of the search results filter options.|
| search/facetQueries | Allows the configuration of the search results filter options.|
| search/categories | Allows the configuration of the search results filter options.|
| search/aca:fields | Specify the metadata fields that will be included in search queries.|
| sidenav/preserveState | Remember the users choice of sidenav minimized or expanded, `true` or `false`.|
| sideNav/expandedSidenav | Side navigation expanded by default, `true` or `false`.|
| viewer.maxRetries | The preview mechanism used to view a file tries to open it and if its unsuccessful it waits 20 seconds and then tries again. The process involves converting the file (multiple file formats are supported depending on content type) and if it takes more than 20 seconds the system will say that the content isn't supported. This time out can be increased by adding a value for this property. If you enter 2 the wait time before time out will be 40 seconds|
| viewer.enableFileAutoDownload | Specify if a large file is automatically downloaded. Use either `true` or `false`. |
| viewer.enableDownloadPrompt | Specify if the Digital Workspace user is prompted before downloading a large file. The default is `true`. |
| viewer.downloadPromptDelay | In seconds, specify the amount of time to delay a prompt to the Digital Workspace user, before displaying a download large file message. The default is `50`. |
| viewer.enableDownloadPromptReminder | Specify if the Digital Workspace user is prompted with a reminder, before downloading a large file. The default is `true`. |
| viewer.downloadPromptReminderDelay | In seconds, specify the amount of time to delay a reminder prompt, to the Digital Workspace user, before displaying another download large file message. The default is `30`. |
| viewer.fileAutoDownloadSizeThresholdInMB | In megabytes, specify the largest file size a file can be, before the Digital Workspace does not download it automatically. The default is `15`. |

## Dynamic view

You can edit the columns you want to see in any of the file views in the Digital Workspace. This configuration applies to the view you are in and any additional pagination part of that view. Currently the selection reverts back to the original view, once you click away.

1. Log in to the Digital Workspace.

2. In the view you want to adjust, select the three dots on the top right.

3. Deselect the columns you don't want to see in the view and then click **Apply**.

    The columns are no longer visible in the view.

### Drag and drop

You can manually edit the position of the columns in any of the file views in Digital Workspace. To do so, complete the following steps.

1. Log in to the Digital Workspace.

2. In the view you want to adjust, drag and drop the columns to your desired position. 

    > **Note:**
    > * A column can be dragged to a different position if the ``draggable`` parameter of the column is set to ``true`` in the Config file.
    > * The position does not revert back to the original view, once you click away.

### Configure default columns

A system administrator can use the `app.extension.json` file to configure which columns are visible by default. If the file is not adjusted all the columns will show by default.

1. Open your `../digital-workspace/app.extension.json` file.

2. Add `"isHidden": true` to any of the columns of the `files`, `libraries`, or `trashcan` sections of the file, and then save it. For example, to hide the `role` column in the `libraries` section:

      ```json
      {
      "id": "app.libraries.role",
      "key": "role",
      "title": "APP.DOCUMENT_LIST.COLUMNS.ROLE",
      "type": "text",
      "class": "adf-no-grow-cell",
      "sortable": true,
      "template": "app.columns.libraryRole",
      "desktopOnly": false,
      "isHidden": true,
      "order": 40
    },
    ```

    The `role` column no longer displays by default.  

## Permissions

Permissions for folders and files in the Digital Workspace can be assigned and viewed easily.
To view the permissions of a folder or file in the Digital Workspace, select the file or folder, right click it, and select **Permissions**. You are presented with the Permissions tab.

The type of permissions a user or group has for a file is determined by what role they have.

For more information on roles see [User roles and permissions]({% link content-services/latest/using/permissions.md %})

### Setting permissions

Setting permissions for folders and files allows you to manage what type of access a user has for a folder or file. From within the Permissions tab you can assign a user or a group to have a specific type of access based on what role you assign them.
> **Note:** You can also delete permissions from here by using the Bin icon next to the user or group that has permissions assigned to it.

1. From within the permissions tab use the Add icon to add a user or group.

2. Search for the user or group you want to assign access to your folder or file and then click **SELECT**.

3. Select the role you want to assign to the user or group and then click **ADD**.

    If you are assigning a role to a group you can select a different role for the administrator of that group than for the rest of the users in the group.

4. (Optional) Use the slider to allow the added users or groups to inherit the permissions from the parent folder.

## Search

The default search capability in the Digital Workspace contains six filters that can be used to refine the searches you make against your content. You can use the search filters in conjunction with each other to help further refine your results. The contents of the filters can be configured to suit your needs and can be based on the metadata you have chosen to assign to your content. Dublin core and Effectivity element sets have additionally been provided for you to use to help filter your content, if you are using those standard classification types. They can be selected under the **Filter Set** heading.

### Search filters

Use the **Logic** filter to match or exclude words, and phrases. Use the **Properties** filter to limit, exclude, or exactly match files of a certain size. You can also filter by file type. Use the **Date** filter to find files created or modified within specific time periods. Use the **Location** filter to include locations of where you would like to focus your search results, for example Europe, or Marketing. Use the **Tags** filter to include content that has been tagged, for more see [Tags]({% link content-services/latest/admin/control-center.md %}#tags). Use the **Categories** filter to include content that has been categorized, for more see [Categories]({% link content-services/latest/admin/control-center.md %}#categories).

![search]({% link digital-workspace/images/search-user-interface.png %})

### Search configuration

The search filters that are available in the Digital Workspace can be refined and tailored to your specific needs by creating custom search forms. Each form can contain a set of filters that are relevant to a particular task or user group within your organization. You can select the most useful search form from the drop-down lists on the search results page. For details on how to create and configure search forms for a more intuitive search experience, see the [Search Configuration Guide](https://github.com/Alfresco/alfresco-ng2-components/blob/develop/docs/user-guide/search-configuration-guide.md){:target="_blank"}.

![search]({% link digital-workspace/images/search-integration.png %})

---
title: Deploy front-end applications
---

Use the example to launch a front-end application that sits on top of the Alfresco backend services. The example uses the Alfresco Content Services - Community Edition version of the front-end application. You can repeat the same exercise with the Alfresco Content Services - Enterprise Edition.

## Deploy Alfresco Content App {#deploy-aca}

To develop a front-end application using the Alfresco Community Edition (the open source version), use the Content App as a starting point.

### Prerequisites {#prereqs-aca}

* Deploy Alfresco Community Edition and make sure it's accessible from your browser:

    ```bash
    http://localhost:8080/alfresco
    ```

* `Node.js` 18.x

### Deploy Content App

Deploy the Content App using the following steps:

1. Open a command prompt and clone the following GitHub repository to a working directory:

    ```bash
    git clone https://github.com/Alfresco/alfresco-content-app.git
    ```

2. Navigate to the `alfresco-content-app` directory and create a file named `.env` with the following content:

    ```bash
    APP_CONFIG_ECM_HOST="http://localhost:8080"
    APP_CONFIG_PLUGIN_AOS=false
    APP_CONFIG_PLUGIN_CONTENT_SERVICE=true
    ```

    > **Note:** Enter your Alfresco Content Services URL as the `APP_CONFIG_ECM_HOST` value.

3. Run the following commands to start the application:

    ```bash
    npm install
    npm start
    ```
  
    The application is available at `http://localhost:4200` and you must use the Alfresco Content Services credentials.

The Alfresco Content App should be running in development mode in your development environment.

## Deploy Alfresco Digital Workspace {#deploy-adw}

If you're an Alfresco customer or official partner, you can use the Enterprise application instead of the open source software. To develop an Alfresco front-end application, make sure the required software is available on your system.

### Prerequisites {#prereqs-enterprise}

* Deploy ACS Enterprise Edition and make sure it's accessible from your browser:

    ```bash
    http://localhost:8080/alfresco
    ```

* `Node.js` 18.x

### Deploy Digital Workspace

Deploy Digital Workspace using the following steps:

1. Request a local copy of the `alfresco-apps` GitHub repository project from [Hyland Community](https://community.hyland.com/tskb){:target="_blank"}.

    There are two distributions available to run with the Digital Workspace:

    | Distribution | Description |
    | ------------ | ----------- |
    | `content-ee` | *Default.* The Digital Workspace with the Process Services extension |

    > **Note:** This project uses the monorepo structure with several monorepo apps.

2. Create the following `.env` file.

    ```bash
    BASE_URL="http://localhost:8080"
    APP_CONFIG_ECM_HOST="http://localhost:8080"
    APP_CONFIG_PROVIDER="ECM"
    APP_CONFIG_AUTH_TYPE="BASIC"
    APP_CONFIG_PLUGIN_AOS=false
    APP_CONFIG_PLUGIN_CONTENT_SERVICE=true
    APP_CONFIG_PLUGIN_PROCESS_SERVICE=false
    APP_CONFIG_PLUGIN_AI_SERVICE=false
    ```

    > **Note:** The Digital Workspace 4.4.x uses the Content Application version 4.4.x.

3. Open a command prompt and run the following command to install all third-party dependencies:

    ```bash
    npm ci
    ```

4. Run the application:

    ```bash
    npm start  content-ee
    ```

    The application is available at `http://localhost:4200` and you must use the Alfresco Content Services credentials to log in.

    The configuration provided for the sample above is the minimal required for your development environment to locally test the Alfresco Repository, but additional environment variables are available.

    ```bash
    # App config settings
    APP_CONFIG_BPM_HOST="<url>"
    APP_CONFIG_ECM_HOST="<url>"
    APP_CONFIG_OAUTH2_HOST="<url>"
    APP_CONFIG_IDENTITY_HOST="<url>"
    APP_CONFIG_PROVIDER="ALL"
    APP_CONFIG_AUTH_TYPE="OAUTH"
    APP_CONFIG_OAUTH2_CLIENTID="alfresco"
    APP_CONFIG_OAUTH2_IMPLICIT_FLOW=true
    APP_CONFIG_OAUTH2_SILENT_LOGIN=true
    APP_CONFIG_OAUTH2_REDIRECT_SILENT_IFRAME_URI="{protocol}//{hostname}{:port}/assets/silent-refresh.html"
    APP_CONFIG_OAUTH2_REDIRECT_LOGIN=/
    APP_CONFIG_OAUTH2_REDIRECT_LOGOUT=/
    APP_CONFIG_APPS_DEPLOYED="[{"name": "simpleapp"}]"
    APP_CONFIG_LANDING_PAGE="/personal-files"

    # CONTENT RELATED
    APP_CONFIG_PLUGIN_PROCESS_SERVICE=true
    APP_CONFIG_PLUGIN_AI_SERVICE=true
    APP_CONFIG_PLUGIN_AOS=true
    APP_CONFIG_PLUGIN_CONTENT_SERVICE=true
    APP_CONFIG_CUSTOM_MODELED_EXTENSION = "{}"

    # CONTENT - MICROSOFT PLUGIN RELATED
    APP_CONFIG_PLUGIN_MICROSOFT_ONLINE=true
    APP_CONFIG_MICROSOFT_ONLINE_OOI_URL="<url>"
    APP_CONFIG_MICROSOFT_ONLINE_CLIENTID="<clientid>"
    APP_CONFIG_MICROSOFT_ONLINE_AUTHORITY="<url>"
    APP_CONFIG_MICROSOFT_ONLINE_REDIRECT="<url>"

    # CONTENT - MICROSOFT INTEGRATION TEST RELATED
    MICROSOFT_USER_INITIALS="<user-initials>"
    MICROSOFT_EMAIL="<email>"
    MICROSOFT_USER2_INITIALS="<user-initials>"
    MICROSOFT_EMAIL2="<email>"
    MICROSOFT_PASSWORD="<password>"
    MOO_LOGIN_URL="<url>"
    ```

## Generate and deploy an ADF App {#deploy-adf}

You can develop a custom ADF application that adds features, behaviors, and customizations. Using the [Yeoman](https://yeoman.io/){:target="_blank"} scaffolding tool you can quickly create applications for testing in your development environment. The [Yeoman Generator for Alfresco ADF Applications](https://github.com/Alfresco/generator-alfresco-adf-app){:target="_blank"} is available for free as an open source project on GitHub.

Below are the available tutorials on the most common and requested tasks about developing ADF based applications. To build, debug, test, or troubleshoot the Alfresco Digital Workspace and ADF-based applications see [Manage Digital Workspace]({% link digital-workspace/latest/develop/manage.md %}).

### Prerequisites {#prereqs-adf}

* Deploy ACS Enterprise Edition and make sure it's accessible from your browser:

    ```bash
    http://localhost:8080/alfresco
    ```

* `Node.js` 18.x

> **Note:** All Angular development is done using the Typescript language.

### Generate the app

1. To ensure you have Yeoman installed, open a command prompt and enter:

    ```bash
    yo --version
    ```

    If this is not already installed, run:

    ```shell
    npm install -g yo
    ```

   > **Note:** If you're on Linux or MacOS, you might need to run the following commands using `sudo`.

2. Install the latest version of the Alfresco Yeoman Generator ADF App:

    ```shell
    npm install -g generator-alfresco-adf-app@latest
    ```

3. Install the Angular CLI:

    ```shell
    npm install -g @angular/cli
    ```

    Angular CLI makes it easy to create components, libraries, and more. You can check what version of the installed version Angular CLI you have installed by using the `ng v` command in the terminal.

4. Generate the application:

    ```shell
    yo alfresco-adf-app
    ```

5. Enter a name and choose **Content Services** as the application blueprint and then enter `Y` to install the dependencies.

    The Yeoman generator creates a new project and installs all dependencies required for your application.

    > **Note:** The Yeoman generator creates a new directory for your project. You must work within this directory.

6. To configure the application to work with Content Services, open the `proxy.conf.js` file in a code editor.

7. Modify `"target": "http://localhost:8080"` so that it matches your Content Services URL and then save the file.

    You don't need `/alfresco` at the end of the target URL. For example, if you've launched Alfresco Content Services using Docker Compose, your Alfresco Content Services repository might be available at `http://localhost:8080/alfresco`. In this case, your `proxy.conf.json` file might look like:

    ```json
    module.exports = {
        "/alfresco": {
        "target": "http://localhost:8080",
        "secure": false,
        "changeOrigin": true
        }
    };
    ```

    > **Note:** If you're running an online trial, the Content Services URL is provided in the welcome email.

    For the online trial, the `proxy.conf.json` file might look like:

    ```json
    module.exports = {
        "/alfresco": {
        "target": "https://xyz.trials.alfresco.com",
        "secure": false,
        "changeOrigin": true
        }
    };
   ```

### Start the app

1. Start the application:

    ```bash
    npm start
    ```

    A browser window will automatically open up at `http://localhost:4200`.

2. Click the key icon in the side navigation to log in.

    > **Note:** If you're running an online trial, the Content Services login credentials are provided in the welcome email.

You can browse, upload, and preview documents in the repository with this application.

## Troubleshooting and support

Ask questions in the Application Development Framework section of the [Alfresco Forum](https://hub.alfresco.com/t5/application-development/ct-p/developing){:target="_blank"} or in the Alfresco [Gitter Discussions](https://gitter.im/Alfresco/alfresco-ng2-components){:target="_blank"}.

If you're an Alfresco customer or partner, you can also request support in [Hyland Community](https://community.hyland.com/tskb){:target="_blank"}.
---
title: Build extensions
---

The Alfresco Application Development Framework (ADF) extension mechanism allows you to add, remove, and change the behavior of your applications. The extension mechanism supports the Digital Workspace, and is the recommended way to make direct changes to its source code.

Customizations that are implemented through the extension mechanism are more maintainable because the changes are modular and isolated from the core of the application. This approach to customizing the Digital Workspace ensures upgrades are easier to manage and test.

Use the Digital Workspace and develop an extension if your use case is mainly covered by the Digital Workspace functionality. However, some additional changes are required to meet the expectations and the requirements. In case of complex changes, a custom ADF based application is an alternative.

## How to create an extension

Use this information to develop a `hello word` extension for the Digital Workspace.

### Prerequisites

* Alfresco Content Services - Enterprise Edition.
  * Open your browser and check everything starts up correctly:

    ```bash
    http://localhost:8080/alfresco
    ```

* `Node.js` 18.x

* Download the Digital Workspace project from [Nexus](https://nexus.alfresco.com/nexus/#nexus-search;quick~digital%20workspace){:target="_blank"}.

### Create a Digital Workspace extension

Use the [Nx](https://nx.dev/) developer tools for monorepos to create the Digital Workspace extension.

1. Install `nx` cli globally:

    ```bash
    npm install -g nx
    ```

2. Create a new extension called `my-extension` from the root directory of the Digital Workspace project:

    ```bash
    nx g @nrwl/angular:lib my-extension
    ```

    Leave the default values of the command unless you're familiar with what they mean.

    In the `libs/my-extension` path you'll find the following structure:

    * The `src` folder contains all the typescript source code
    * The `index.ts` file defines all the inclusions of the extension
    * The `lib/my-extension.module.ts` file defines the module class for the extension
    * The `README.md` file contains documentation
    * Other files are for testing and configuration

    > **Note:** For more on creating libraries using Nx see [Angular Nx Tutorial - Step 8: Create Libs](https://nx.dev/angular-tutorial/08-create-libs){:target="_blank"}

3. Once `my-extension` is created, add the configuration to the extension module by editing the `./libs/my-extension/src/lib/my-extension.module.ts` file:

    ```java
    // Add the following import to the page.
    import { provideExtensionConfig } from '@alfresco/adf-extensions';
    // Add providers as described below.
    NgModule({
      imports: [CommonModule],
      providers: [
        provideExtensionConfig(['my-extension.json'])
      ]
    })
    export class MyExtensionModule {}
    ```

4. Create a directory called `libs/my-extension/assets`:

    This directory is used to program the extension to add a new item called **hello world** to the **New** button on the landing page of the Digital Workspace.

5. Create a file called `libs/my-extension/assets/my-extension.json` with the following content:

    ```json
    {
      "$version": "1.0.0",
      "$id": "my.extension",
      "$name": "my adf extension",
      "$description": "my adf extension",
      "$license": "Apache-2.0",
      "actions": [],
      "features": {
        "create": [
          {
            "id": "my.extension.hello.world",
            "title": "BYE BYE WORLD! (Logout)",
            "order": 50,
            "actions": {
              "click": "LOGOUT"
            }
          }
        ]
      },
      "routes": [],
      "rules": []
    }
    ```

    > **Note:** After the Digital Workspace extension has been created, ensure the `tsconfig.base.json` file includes a link to the `libs/my-extension/src/index.ts` file as part of the paths item. These are default paths that are set during the creation of the extension. It's useful to verify the paths when troubleshooting.

6. Edit the `apps/content-ee/src/app/extensions.module.ts` file to add the extension module to the application using the following format:

    ```java
    // Add the following import to the page.
    import { MyExtensionModule } from '@alfresco-dbp/my-extension';
    @NgModule({
        imports: [
            ...,
            MyExtensionModule,
        ],
    })
    export class AppExtensionsModule {}
    ```

7. Edit the `angular.json` file by adding the following configuration to the `projects/content-ee/targets/build/options/assets` section:

    This configuration ensures the extension is visible from the Digital Workspace app.

    ```json
    {
      "input": "libs/my-extension/assets",
      "output": "/assets/plugins/",
      "glob": "my-extension.json"
    },
    ```

8. From a command prompt start the Digital Workspace:

    ```shell
    npm start content-ee
    ```

You have now added a new option to the **New** button called **BYE BYE WORLD!**. The new option initiates the logout command from the current Digital Workspace session. For more see [Extending](https://alfresco-content-app.netlify.app/#/extending/){:target="_blank"} and [Application Development Framework Tutorials](https://www.alfresco.com/abn/adf/){:target="_blank"}.

![Development options]({% link digital-workspace/images/adw-extension-new-button.png %})

### Replace existing extension

You can replace an existing extension with a new one you have created. To achieve this you must have an existing extension called `my-extension`, and its structure must be compliant with the content and structure of the current `projects/my-extension` file.

1. Run the following command from a command prompt from inside the root folder of the Digital Workspace project:

    ```bash
    nx g @nrwl/angular:lib my-extension
    ```

    > **Note:** Ensure you use the same name as the existing extension, in this example it's called `my-extension`.

Once complete, delete the content of the `libs/my-extension` directory, and replace it with the source code of the new Digital Workspace extension.

## How to add a new page and menu item

You can create a new page and a new menu item in the Digital Workspace. To achieve this you must have a working Digital Workspace extension as well as the full repository. Using the examples above, you should have an extension called `my-extension`.

1. Create a new folder called `libs/my-extension/src/lib/my-first-page`, and add a new file into it called `my-first-page.component.ts` with the following information:

    ```java
    import { Component, } from '@angular/core';
    @Component({
        selector: 'my-first-page',
        template: "<h1>HELLO WORLD!</h1>"
        })
    export class MyFirstPageComponent {}
    ```

2. Edit the `my-extension.json` file in the `libs/my-extension/assets` folder and add the following to the `routes` array:

    ```json
    {
        ...,
        "routes": [
            {
                "id": "my.extension.myFirstPage",
                "path": "my-first-page",
                "parentRoute": "",
                "layout": "app.layout.main",
                "component": "my.extension.components.my-first-page",
                "auth": [
                    "content-services.auth"
                ]
            }
        ],
        "rules": []
    }
    ```

3. Declare the component identifier directly in the extension's module by editing the `libs/my-extension/src/lib/my-extension.module.ts` file with the following:

    ```java
    // Add the following imports.
    import { ExtensionService } from '@alfresco/adf-extensions';
    import { MyFirstPageComponent } from './my-first-page/my-first-page.component';
    // Change the NgModule as follows.
    @NgModule({
      ...,
      declarations: [MyFirstPageComponent]
    })
    export class MyExtensionModule {
      constructor(extensions: ExtensionService) {
        extensions.setComponents({
          'my.extension.components.my-first-page': MyFirstPageComponent,
        });
      }
    }
    ```

    You have added a new route (URI) to the application through the extension. You can test everything is working properly by launching the `npm start content-ee` command and pointing your browser to `http://localhost:4200/#my-first-page`.

4. To add a menu item that points to the new page, edit the `my-extension.json` file in the `libs/my-extension/assets` folder and add the following to the `features` element:

    ```json
    {
      ...
      "features": {
        ...,
        "navbar": [
          {
            "id": "app.navbar.primary",
            "items": [
              {
                "id": "app.navbar.libraries.menu",
                "children": [
                  {
                    "id": "app.navbar.libraries.all-libraries",
                    "title": "My first page",
                    "description": "My first page",
                    "order": 400,
                    "route": "my-first-page",
                    "rules": {
                      "visible": "app.content-services.isEnabled"
                    }
                  }]
              }]
          }]
      },
      ...
    }
    ```

Below you can see what the layout looks like:

![ADW Extension New Library]({% link digital-workspace/images/adw-extension-new-library.png %})
---
title: Front-end app development overview
---

You can develop with and adapt the Digital Workspace or integrate your own solutions. To do this you can use the Digital Workspace extensions or create a custom app using the Alfresco Application Development Framework (ADF). The Digital Workspace is a fully supported application that is available to customers and partners working with **Alfresco Content Services - Enterprise Edition**.

If your project uses **Alfresco Content Services - Community Edition** or other open source components you must use Alfresco Content Application instead of the Digital Workspace. The Content Application is a free, open source example of an application created using the Application Development Framework, and its use is not supported by Alfresco support.

![Develop front-end]({% link digital-workspace/images/develop-front-end.png %}){:height="259px" width="536px"}

## Front-end experience

Front-end applications are a subset of client interactions, and Alfresco provides an Angular-based Application Development Framework for creating them. The backend services provided by Alfresco products use a REST API foundation layer for all client interactions of the platform.

### Front-end applications

The Application Development Framework is an open source project that defines a set of services and visual components that you can use to create bespoke end-user applications. The framework is not an end-user application itself, but it enables you to create your own applications.

The image explains the relationship between the front-end applications and backend Alfresco services, i.e. the Digital Workspace, the Content Application, and the Application Development Framework.

![Development options]({% link digital-workspace/images/develop-arch.png %}){:height="455px" width="536px"}

## Development options

The following options are provided to start developing a front-end for Alfresco depending on the customization required. We have open source and enterprise applications if the customization is minimal. However, if you need to develop very comprehensive extensions, you can use the Application Development Framework.

* Enterprise customers can use the Digital Workspace as a starting point.
  * See [Deploy Alfresco Digital Workspace]({% link digital-workspace/latest/develop/deploy.md %}#deploy-adw) for more details.
  * To develop extensions, see [Digital Workspace extensions]({% link digital-workspace/latest/develop/extensions.md %}) or create a custom app using the Alfresco [Application Development Framework (ADF)]({% link digital-workspace/latest/develop/deploy.md %})

* Community customers can use the [Content Application](https://alfresco-content-app.netlify.app/#/){:target="_blank"} as a starting point.
  * See [Deploy Alfresco Content App]({% link digital-workspace/latest/develop/deploy.md %}#deploy-aca) for more details.
  * To develop extensions, see [Content App extensions]({% link digital-workspace/latest/develop/extensions.md %}).

* Customers that require extensive customizations can use the Application Development Framework as a starting point.
  * See [Generate and deploy an ADF App]({% link digital-workspace/latest/develop/deploy.md %}#deploy-adf) for more details.

## Mobile development

Native mobile frameworks and applications are provided by Alfresco. You can access the Mobile Workspace code in the following GitHub repositories:

* [Android](https://github.com/alfresco/alfresco-mobile-workspace-android){:target="_blank"}
* [iOS](https://github.com/alfresco/alfresco-mobile-workspace-ios){:target="_blank"}
---
title: Manage Digital Workspace
---

Learn how to run the Digital Workspace in your local development environment from the source code and manage it from a developer perspective.

## Prerequisites and requirements

* Alfresco Content Services - Enterprise Edition:
  * Open your browser and check everything starts up correctly:

    ```bash
    http://localhost:8080/alfresco
    ```

* `Node.js` 18.x

## Clone and launch the front-end application

Once Content Services is up and running, you must make the source code of the project available locally in your development environment. If you're an Alfresco customer or partner, you can get a local copy of the project by opening a request in [Hyland Community](https://community.hyland.com/tskb){:target="_blank"}.

1. In the `alfresco-apps` directory, create a file named `.env` with the following content.

    Enter the Content Services URL as the `APP_CONFIG_ECM_HOST` value.

    ```bash
    BASE_URL="http://localhost:8080"
    APP_CONFIG_ECM_HOST="http://localhost:8080"
    APP_CONFIG_PROVIDER="ECM"
    APP_CONFIG_AUTH_TYPE="BASIC"
    APP_CONFIG_PLUGIN_AOS=false
    APP_CONFIG_PLUGIN_CONTENT_SERVICE=true
    APP_CONFIG_PLUGIN_PROCESS_SERVICE=false
    APP_CONFIG_PLUGIN_AI_SERVICE=false
    ```

    > **Note:** The Digital Workspace 4.4.x uses the Content Application version 4.4.x.

2. Run the following commands to start the application:

    ```bash
    npm ci
    npm start content-ee
    ```

    The application is available at `http://localhost:4200`. Use the Content Services credentials to log in.

    The configuration provided for the sample above is the minimal required for your development environment to locally test the Alfresco Repository, but additional environment variables are available.

    ```bash
    # App config settings
    APP_CONFIG_BPM_HOST="<url>"
    APP_CONFIG_ECM_HOST="<url>"
    APP_CONFIG_OAUTH2_HOST="<url>"
    APP_CONFIG_IDENTITY_HOST="<url>"
    APP_CONFIG_PROVIDER="ALL"
    APP_CONFIG_AUTH_TYPE="OAUTH"
    APP_CONFIG_OAUTH2_CLIENTID="alfresco"
    APP_CONFIG_OAUTH2_IMPLICIT_FLOW=true
    APP_CONFIG_OAUTH2_SILENT_LOGIN=true
    APP_CONFIG_OAUTH2_REDIRECT_SILENT_IFRAME_URI="{protocol}//{hostname}{:port}/assets/silent-refresh.html"
    APP_CONFIG_OAUTH2_REDIRECT_LOGIN=/
    APP_CONFIG_OAUTH2_REDIRECT_LOGOUT=/
    APP_CONFIG_APPS_DEPLOYED="[{"name": "simpleapp"}]"
    APP_CONFIG_LANDING_PAGE="/personal-files"

    # CONTENT RELATED
    APP_CONFIG_PLUGIN_PROCESS_SERVICE=true
    APP_CONFIG_PLUGIN_AI_SERVICE=true
    APP_CONFIG_PLUGIN_AOS=true
    APP_CONFIG_PLUGIN_CONTENT_SERVICE=true
    APP_CONFIG_CUSTOM_MODELED_EXTENSION = "{}"

    # CONTENT - MICROSOFT PLUGIN RELATED
    APP_CONFIG_PLUGIN_MICROSOFT_ONLINE=true
    APP_CONFIG_MICROSOFT_ONLINE_OOI_URL="<url>"
    APP_CONFIG_MICROSOFT_ONLINE_CLIENTID="<clientid>"
    APP_CONFIG_MICROSOFT_ONLINE_AUTHORITY="<url>"
    APP_CONFIG_MICROSOFT_ONLINE_REDIRECT="<url>"

    # CONTENT - MICROSOFT INTEGRATION TEST RELATED
    MICROSOFT_USER_INITIALS="<user-initials>"
    MICROSOFT_EMAIL="<email>"
    MICROSOFT_USER2_INITIALS="<user-initials>"
    MICROSOFT_EMAIL2="<email>"
    MICROSOFT_PASSWORD="<password>"
    MOO_LOGIN_URL="<url>"
    ```

## Build, promote, test

The Digital Workspace is a standard Angular application, and its lifecycle follows the same principles and best practices of any other standard Angular application. Use this information to learn how to install it using different distributions, how to add or remove unwanted modules, how to promote the application for use in different environments, and how to test it.

1. In a command prompt, enter:

    ```bash
    npm install
    ```

    There are two distributions available to run with the Digital Workspace:

    | Distribution | Description |
    | ------------ | ----------- |
    | `content-ee` | *Default.* The Digital Workspace with the Process Services extension |

2. Select the command to start the application:

    ```bash
    npm start <content-ee> [prod]
    ```

    > **Note:** For the Alfresco Content Application or any other ADF-based application, the command is `npm start`.

3. Select the command to build the application:

    ```bash
    npm run build <content-ee|content-apa> [prod]
    ```

    > **Note:** For the Alfresco Content Application or any other ADF-based application, the command is `npm run build`.

    Once the build has finished a new folder called `dist` is created inside the root directory of the project. Inside the `dist` directory there is a collection of files that represent the distribution of your application.

## Remove modules before building

To remove any modules from the distribution, access the `apps/content-ee/src/app/extensions.module.ts` file and remove the ones that are not needed.

```java
@NgModule({
    imports: [
        AosExtensionModule,
        AcaAboutModule,
        AcaSettingsModule,
        AiViewModule,
        RecordModule,
        ProcessServicesExtensionModule,
        ContentServicesExtensionModule,
        ExtensionsOrderExtensionModule,
    ],
})
export class AppExtensionsModule {}
```

## Promote to a different environment

The compiled application is available as a collection of files in the `dist` directory. If you want to use the application in a different environment all you need to do is copy the files over to your new server.

## Testing

Unit tests on the Content Application or the Digital Workspace are developed and executed using Karma - for more see [Karma](https://karma-runner.github.io/latest/index.html){:target="_blank"}.

Unit tests are developed in files with extension `specs.ts`. Almost every component has a related `specs.ts` file stored directly in the same folder as the component. A unit test can look like:

```java
it('...description...', () => {
    // Source code.
});
```

## Troubleshooting and support

Ask questions in the Application Development Framework section of the [Alfresco Forum](https://hub.alfresco.com/t5/application-development/ct-p/developing){:target="_blank"} or in the Alfresco [Gitter Discussions](https://gitter.im/Alfresco/alfresco-ng2-components){:target="_blank"}.

If you're an Alfresco customer or partner, you can also request support in [Hyland Community](https://community.hyland.com/tskb){:target="_blank"}.
---
title: Governance Services
---

Alfresco Digital Workspace has been extended to include Alfresco Governance Services functionality for end users. Working with records is quick and easy to do via the action menus of the Digital Workspace.
This feature requires Alfresco Governance Services.

See the following video for a quick introduction to the governance features.

> **Note:** This video contains functionality that's no longer available (i.e. working with archived files in Amazon Glacier).

{% include media.html id="D3TGksKU7yw" %}
---
title: Install Containerized
---
Alfresco Governance Services capabilities are all available from the right click menu. You can view, move, and delete records from the collaboration site. You can also declare files as records with the ability to declare multiple files in one action. Rules that facilitate the automation of Governance Services are fully compatible with Alfresco Digital Workspace.

> **Note:** When records are deleted from a collaboration site they are not removed from the records management file plan; only the view of the record from the collaboration site is deleted and the record continues to be managed in the file plan.

## Understanding records icons

These icons represent actions and states of your records and files.

|Alfresco Governance Services icon|Alfresco Governance Services icon for small resolution monitors|Description|
|---------------------------------|---------------------------------------------------------------|-----------|
|![declare-file-as-record]({% link digital-workspace/images/ic-declare-record-action.png %})||Click the icon to declare a file as a record.|
|![declared-as-record]({% link digital-workspace/images/adw-record.png %})|![declared-as-record]({% link digital-workspace/images/ic-easy-access-record-small-scrn-size.png %})|The file has been successfully declared as a record.|
|![rejected]({% link digital-workspace/images/adw-record-rejected.png %})|![rejected]({% link digital-workspace/images/ic-record-alert.png %})|The file has been rejected as a record. A message displays the reason why it was rejected. For example for having incomplete metadata.|
---
title: Security Marks
---

Use the Digital Workspace to assign Security Marks to files and folders. Doing this limits their accessibility from users that do not have the correct user rights.

1. Sign into the Digital Workspace.

2. Right click on the file or folder you want to add Security Marks to and select **Security Marks**.

    You will see all the Security Marks that are available.

3. Select which Security Marks you want assigned to the file or folder and click **Save**.

![security-marks]({% link digital-workspace/images/security-marks.png %})

Once you have saved the Security Marks for the file or folder the ones you have selected will be visible in the Security Marks column.

> **Note:** If you have more than can be displayed in the column you can click the **Display all** button.

See the [Security Controls]({% link content-services/latest/admin/control-center.md %}#security-controls) section of the Content Services - Control Center documentation for more details.---
title: Install Containerized
---

Alfresco Digital Workspace is deployed as part of Alfresco Content Services using Helm charts or a Docker Compose file. Both these methods include a lightweight, pre configured, NGINX server and Digital Workspace application. Due to the limited capabilities of Docker Compose, this deployment method is recommended for development and test environments only.

It is recommended you familiarize yourself with the concepts of containerized deployment before working with Helm charts, and Docker. See [Understanding containerized deployment]({% link content-services/latest/install/containers/index.md %}) for more information.

Follow these links to find out how to deploy Digital Workspace using Helm charts or Docker Compose:

* [Deploying Alfresco Content Services with Helm charts on AWS]({% link content-services/latest/install/containers/helm.md %}).
* [Deploying using Docker Compose]({% link content-services/latest/install/containers/docker-compose.md %}).
---
title: Installing Digital Workspace
---
There are a number of different ways to deploy Alfresco Digital Workspace. You can deploy it using Docker images that are packaged in Helm charts or using Docker Compose. You can also install Alfresco Content Services using standard WAR files contained in the distribution zip, and then configure the installation to include Alfresco Digital Workspace.

The deployment methods are:

* [Containerized deployment]({% link digital-workspace/latest/install/containerized.md %}). Due to the limited capabilities of Docker Compose, this deployment method is recommended for development and test environments only.
* [Installing into Tomcat]({% link digital-workspace/latest/install/tomcat.md %})
* [Installing into a different web server]({% link digital-workspace/latest/install/other-webserver.md %})
---
title: Install into other webserver
---
You can deploy Alfresco Digital Workspace into a different web server than where Alfresco Content Services is running. You can use another instance of Tomcat, a lightweight web server such as NGINX, or you can use a web server of your choice. First you need to install Alfresco Content Services 7.2 or above using the distribution zip. See [Installing using distribution zip]({% link content-services/latest/install/zip/index.md %}) for more information.

1. Log in to [Hyland Community](https://community.hyland.com/products/alfresco){:target="_blank"}.

2. Go to **Product downloads** and select Alfresco Digital Workspace.

3. Download `alfresco-digital-workspace-adw-x.x.x.zip` for the required version.

   `alfresco-digital-workspace-adw-x.x.x.zip` is the file name followed by the version of the Digital Workspace, for example `alfresco-digital-workspace-adw-2.1.0.zip`.

4. On the server where you want to host the Digital Workspace extract the files to `<webserver-location>/html`.

   > **Note:** This is the public html folder.

5. Browse the extracted files and open `app.config.json` in a text editor.

6. Edit the `app.config.json` file and change the `ecmHost` property to be the same as your Alfresco Content Services server and allocated port. For example:

    `http://<acsservername>:port`

7. Also in the `app.config.json` file, change the `baseShareUrl` property to be the server name of the Digital Workspace. For example:

      `http://<appservername>:port/alfresco-digital-workspace-adw-x.x.x` (`alfresco-digital-workspace-adw-x.x.x` being the name of the zip file)

   > **Note:** If Quickshare is disabled in Alfresco Content Services ignore this step.

    To disable Quickshare, set `system.quickshare.enabled=false` in the \tomcat\shared\classes\alfresco-global.properties file. For more information, see [Using the alfresco-global.properties file]({% link content-services/latest/config/index.md %}#using-alfresco-globalproperties).

8. Save the file.

9. Open your browser and access the Digital Workspace:

    `http://<appservername>:8080/alfresco-digital-workspace-adw-x.x.x`

> **Note:** When deploying Alfresco Digital Workspace to a different web server, it is recommended you setup Cross-Origin Resource Sharing (CORS). For more information, see [Cross Origin Resource Sharing (CORS) filters]({% link content-services/latest/config/repository.md %}#cors-configuration) and [Cross-Origin Resource Sharing (CORS)](https://enable-cors.org/){:target="_blank"}.
---
title: Install into Tomcat 
---
To install Alfresco Digital Workspace into Tomcat, you first need to install Alfresco Content Services 7.2 or above using the distribution zip. See [Installing using distribution zip]({% link content-services/latest/install/zip/index.md %}) for more information.

1. Log in to [Hyland Community](https://community.hyland.com/products/alfresco){:target="_blank"}.

2. Go to **Product downloads** and select Alfresco Digital Workspace.

3. Download `alfresco-digital-workspace-adw-x.x.x.war` for the required version.

    `alfresco-digital-workspace-adw-x.x.x.war` is the file name followed by the version of the Digital Workspace, for example `alfresco-digital-workspace-adw-2.1.0.war`.

4. On the server that will host the Digital Workspace move the `alfresco-digital-workspace-adw-x.x.x.war` file to the `<TOMCAT_HOME>/webapps` folder.

   > **Note:** Tomcat extracts the files automatically.

5. Browse the extracted `alfresco-digital-workspace-adw-x.x.x` directory and open the `app.config.json` file in a text editor.

6. Edit the `app.config.json` file and change the `ecmHost` property to be the same as your Alfresco Content Services server and allocated port. For example:

    `http://<acsservername>:port`

7. Also in the `app.config.json` file, change the `baseShareUrl` property to be the same as your Digital Workspace server and allocated port. For example:

    `http://<appservername>:port/alfresco-digital-workspace-adw-x.x.x` (`alfresco-digital-workspace-adw-x.x.x` being the name of the WAR file)

   > **Note:** If Quickshare is disabled in Alfresco Content Services ignore this step.

    To disable Quickshare, set `system.quickshare.enabled=false` in the `\tomcat\shared\classes\alfresco-global.properties` file.

    For more information, see [Using the alfresco-global.properties file]({% link content-services/latest/config/index.md %}#using-alfresco-globalproperties).

8. Save the file.

9. Open your browser and access the Digital Workspace:

    `http://<appservername>:8080/alfresco-digital-workspace-adw-x.x.x`
---
title: Image Management
---

Image Management allows you to view and manipulate your image files in the Digital Workspace.

Features provided with Image Management include enhanced image manipulation with image crop and rotate capabilities
and [IPTC](https://iptc.org/standards/photo-metadata/){:target="_blank"} metadata extraction.

## Uploading images

Image Management provides information and features about image files that you upload in the Digital Workspace.

1. Select the folder in the File Library where you want to add your content.

2. You can drag and drop images, or select **NEW > Upload File** from the toolbar, as you would normally in the Digital Workspace.

   You will see the image in the folder listing:

   ![folder-listing]({% link digital-workspace/images/adw-folder-listing.png %})

   Click on the image file to see the preview rendition of the image:

   ![image-preview]({% link digital-workspace/images/adw-image-preview.png %})

   A rendition is a version of the original image, for example, a copy of an image that is optimized for web viewing. By default, not all renditions are created after uploading. It is only when a user first views the image that a rendition is created.

## Viewing IPTC and EXIF metadata

Image Management provides additional information and features in Digital Workspace when you view image files.

1. Select an image in the Document Library, as you would normally in Digital Workspace, by clicking the thumbnail or name, to view it in the file preview screen.

2. Click the information button in the top toolbar ![info-panel]({% link digital-workspace/images/adw-properties-panel-button.png %}){:height="32px" width="150px"}

3. Make sure the **Properties** tab is visible at the bottom. Scroll down until you see the **More information** button in the lower right corner

4. Click the **More information** button, which should display extra media properties sections as follows:

   ![image-preview]({% link digital-workspace/images/adw-media-props-sections.png %}){:height="300px" width="150px"}

5. Click the **IPTC** section to see IPTC metadata:

   ![image-preview]({% link digital-workspace/images/adw-iptc-metadata.png %}){:height="600px" width="150px"}

>**Note:** IPTC metadata is also mapped to existing description (IPTC caption/description) and title (IPTC headline) properties, hover over the filename in the File library, and the IPTC property values are displayed.

>**Note:** The IPTC Content Model needs to be bootstrapped into Alfresco Content Services for the IPTC metadata extraction to work.

## Manipulating images

Image Management provides features to allow you to edit image files in Digital Workspace.

1. Select an image from the File Library, as you would normally in the Digital Workspace, by clicking the thumbnail or name, to view it in the file preview screen.

2. The ![image-preview]({% link digital-workspace/images/adw-image-crop-rotate-panel.png %}){:height="32px" width="150px"} panel is visible at the bottom of the preview screen, and it provides crop and rotate actions, and the possibility to save the manipulated image.

3. To crop the image use the following icon:

    * ![crop icon]({% link digital-workspace/images/adw-image-crop-icon.png %}){:height="18px" width="18px"}: click this icon to start crop manipulation of an image. A grid appears on top of the image. Hold down your left mouse button to select an area of the image using the grid:

      ![image-preview]({% link digital-workspace/images/adw-image-crop-action.png %})

      You will now see two new actions in the panel under the image, one for saving (marked in blue), and a cross for canceling the crop.

    * Save or cancel the crop manipulation. If you **Save** the manipulated image a new minor file version is created (original image is file version 1.0). To cancel any crop action click **Cancel** (X).

4. To rotate the image use the following icon:

   * ![rotate icon]({% link digital-workspace/images/adw-image-rotate-icon.png %}){:height="18px" width="18px"}: click this icon to start rotating the image.

    You will now see two new actions in the panel under the image, one for saving the rotation, and a cross for canceling the rotation manipulation.

   * Save or cancel the rotation. If you **Save** the manipulated image a new minor file version is created (original image is file version 1.0). To cancel any rotation action click **Cancel** (X).

You can also use the scroll wheel to navigate large images.
---
title: Configuring Process Services
---
You must configure Alfresco Digital Workspace to work with Alfresco Process Services. You cannot use Alfresco Digital Workspace with Alfresco Process Services if you do not have Single Sign-On (SSO) configured between Alfresco Process Services and Alfresco Content Services.

> **Note:** For information on how to configure Alfresco Process Services and Alfresco Content Services to use SSO see [Configure an Alfresco Content Services connection using Single Sign On (SSO)]({% link process-services/latest/config/content.md %}#configure-a-connection-using-single-sign-on).

1. Ensure you have installed Alfresco Digital Workspace, see [Installation overview]({% link digital-workspace/latest/install/index.md %})

2. Access the ../digital-workspace/app.config.json file and set the following properties:

* Set the `processService` property to `"true"` (you must include the quotation marks)
* Set the `bpmHost` property, for example <https://processservices.domain.com:port>
* (Optional) Set the `adf-start-process` property, by default it is set to `%{processDefinition} - %{datetime}`
* Change the `providers` property to `all`
   > **Note:** You can configure Alfresco Process Services in greater detail by changing the `../digital-workspace/app.config.json` file further. See [Configure Digital Workspace]({% link digital-workspace/latest/config/index.md %}) for a definition of all these properties. For more information on the other properties available using the Alfresco Development Framework see [Process Services API](https://www.alfresco.com/abn/adf/docs/process-services/){:target="_blank"}.
---
title: Process Services
---
Alfresco Digital Workspace has been extended to include Alfresco Process Services functionality for end users.

These features require Alfresco Process Services to be configured with Alfresco Content Services.

If you are an administrator and want to create new processes in Alfresco Process Services for use in Alfresco Digital Workspace see [Create your first process]({% link process-services/latest/using/process/app-designer.md %}#create-your-first-process).
---
title: Managing Processes
---
You can view and manage your Alfresco Process Services processes in Alfresco Digital Workspace.

1. Log in to Alfresco Digital Workspace.

2. Expand **Process Management** and under the **Processes** heading you can see all your processes.

    The headings are pre defined filters.

    * **Running** - All processes that are running.
    * **Completed** - All processes that are completed.
    * **All** - All processes regardless of state.

3. Right click a process and select **View**.

    You can see all the tasks associated with that process.

4. Right click a **Task** and select **View** to edit that task.

5. Enter more information and click **Save**.

6. (Optional) To complete the task click **Complete**.

## View Process History

You can view the history of a process in the Digital Workspace. The history of a process is available to whoever initiates the process, has a task assigned to them within the process, or has completed at least one task in the process.

To view the history of a process:

1. Log in to Alfresco Digital Workspace.

2. Expand **Process Management** and under the **Tasks** heading you can see all your task related information.

3. Right click on any task in the **My tasks**, **Queued tasks**, or **Completed tasks** area and then select **Process History**.

You will now see the history of a process, which can include, **Status**, **Task Name**, **Assignee**, and **Completed by**.

![Process History]({% link digital-workspace/images/process-history.png %})
---
title: Starting processes
---
You can start a process in Alfresco Digital Workspace, with or without a file attached to it. If you attach a file to the process, you can view the file again by clicking on its hyperlink file name.

1. Log in to Alfresco Digital Workspace.

2. Click the **Start Process** button

    You can also navigate to a file you want to work with using a process, and then right click on it and select **Start Process**.

3. Select the Process you want to use from the list of processes.

    Use the search bar to find the process you want to work with if you have a large amount of processes. Recently used processes appear at the the top of the list.

4. A default Process name is pre filled but it can be changed or more information can be added.

5. Enter any other information required by the Alfresco Process Services form.

    What can be entered into the form will be specific to your organization and the type of form in Alfresco Process Services. If you have selected to work with a specific file already you will see the file as an attachment.

6. Click **START PROCESS**.

    Once the process starts you can view the running process by clicking **View running process** at the bottom of the window.

   > **Note:** You can also start a process by right clicking a file in your search results and selecting **Start Process**.

## Part of running process badge

Badges are icons visible next to your documents, and they are designed to represent different statuses of them. The **Part of running process** badge is visible for documents that are currently in a workflow. To check the processes involved with the document, complete the following steps:

1. Click on the running processes badge.

    A side panel containing all the metadata opens.

2. Click on **Linked Process** to view a list of all the currently running processes of that particular document. 

    The name of all the linked processes along with their starting date is displayed. 

3. Click on **View Details** to view more information about the specific process.

   > **Note:**  You will require permission to access the details.
---
title: Managing tasks
---
You can view and manage your tasks in Alfresco Digital Workspace.

1. Log in to Alfresco Digital Workspace.

2. Expand **Process Management** and under the **Tasks** heading you can see all your task related information.

     The headings are pre defined filters.

     * **My Tasks** - All tasks assigned to you.
     * **Involved Tasks** - All involved tasks.
     * **Queued Tasks** - All queued tasks.
     * **Completed Tasks** - All completed tasks.

3. Right click a task and select **View**.

4. Enter more information and click **Save**.

5. (Optional) To complete the task click **Complete**.

## Print or save a task form

You can print or save to `.pdf` the task forms, including any information entered into the fields.

1. Navigate to the task form you want to print.

2. Click the **Print Form** icon on the top right.

3. Select if you want to print or save as a `.pdf`, and then click **Print** or **Save**.

The output shows the task form, including the name of the task on the top left and the URL of your instance of the Digital Workspace on the top right. The print out saves the entire task form, even if you must scroll to get to the end of it.

![Print]({% link digital-workspace/images/print.png %})
---
title: Supported Platforms
---
The following are the supported platforms for Alfresco Digital Workspace 4.4.x:

| Version | Notes |
| ------- | ----- |
| Content Services 23.x | |
| Content Services 7.4 | |
| Content Services 7.3 | |
| Content Services 7.2 | |
| Content Services 7.1 | |---
title: Troubleshooting
---
Here are the answers to some frequently asked questions.

### When attempting to login a problem with CORS is reported

Refer to [Cross Origin Resource Sharing (CORS) filters]({% link content-services/latest/config/repository.md %}#cors-configuration}) and [Cross-Origin Resource Sharing (CORS)](https://enable-cors.org/){:target="_blank"}.

### Can I customize the Digital Workspace

Yes, there are a number of customizations available that can be configured in `../digital-workspace/app.config.json`. See [Configure Digital Workspace]({% link digital-workspace/latest/config/index.md %}) for more details. The application can also be extended using the ADF Extension framework. See [Extending](https://alfresco-content-app.netlify.com/#/extending/).

### I have installed an extension and the Digital Workspace does not work

First disable the extension and check the Digital Workspace works correctly. If this resolves the issue contact the extension developer for assistance.

### Does the Digital Workspace work with Alfresco Governance Services

Yes, the Digital Workspace supports Alfresco Governance Services. See [Governance Services]({% link digital-workspace/latest/governance/index.md %}).

### Does the Digital Workspace support Smart Folders

Smart Folder access is supported but Smart Folders cannot be created in this application.

### How do I setup SSL

SSL configurations differ from one installation to the next. Here is one approach to the setup of NGINX using SSL, see [https://nginx.org/en/docs/http/configuring_https_servers.html](https://nginx.org/en/docs/http/configuring_https_servers.html){:target="_blank"}.

For information on generating self-trusted certificates for local testing and development purposes, see [https://letsencrypt.org/docs/certificates-for-localhost/](https://letsencrypt.org/docs/certificates-for-localhost/){:target="_blank"}.

### What browsers does the Digital Workspace support

The Digital Workspace supports the following Evergreen browsers:

* Apple Safari
* Google Chrome
* Microsoft Edge
* Mozilla Firefox

### Is Single Sign-On (SSO) supported with the Digital Workspace

Yes, the Digital Workspace supports Single Sign-On with the Identity Service. See [Alfresco SSO Guide]({% link identity-service/latest/tutorial/sso/index.md %}) for more details.

The Digital Workspace does not support SAML Single Sign-On (SSO) for Alfresco Content Services. Users can login with their credentials using basic authentication, but SAML authentication must not be enforced.

See [SAML Single Sign-On (SSO) Module for Alfresco Content Services]({% link saml-module/latest/index.md %}) for more information.

### How can I change my profile in the Digital Workspace

To change your profile, locate the Profile menu item on the top right and click the profile image, and then click **My Profile**.

You can edit the **General** and **Company details** sections by clicking **Edit**. Once you have made the required changes, click **Save**.
---
title: Folder rules
---

In the Digital Workspace you can define folder rules to manage your content automatically, in the same way email clients use rules to filter messages and incoming spam. Rules dictate how content entering, leaving, or currently residing in a folder is managed. When you define a rule, it only applies to new content added to the folder. Items that were in the folder before the rule was defined aren't affected by it.

> **Note:** Even if a folder doesn't have its own rules, it could have inherited rules from a parent folder.

There are three parts to a folder rule:

* The event that triggers the rule.
* The conditions the content has to meet.
* The action performed on the content.

The events that can trigger a rule are:

* A content item arrives in the folder.
* A content item leaves the folder (it's moved or deleted).
* A content item in the folder is modified.

Here are some examples of how you can use rules to automate repetitive tasks:

* Content with certain criteria that enter a folder can be linked to a category.
* Content with certain criteria that enter a folder can have aspects added, or removed.
* Content with certain criteria that enter a folder can execute a script.

## Creating a rule

You can create rules for a folder within the Digital Workspace.

1. Right click a folder in the Digital Workspace and select **Manage rules**.

2. Click the **Create rule** button.

3. Enter a name and a description for the rule.

4. Select when the rule will be triggered:

    * **Items are created or enter this folder**: The rule will be applied to content that gets added to the folder. This includes any item that is copied to, created in, or uploaded to the folder.
    * **Items are updated**: When an item in this folder is modified, the rule will be applied to it.
    * **Items are deleted or leave this folder**: The rule will be applied to content that is moved out of the folder or deleted.

    > **Note:** A rule can have more than one trigger.

5. Select if the rule will be applied using **If**, **NOT If**, or both. You can also add a condition group.

    Here are some examples of conditions that you could apply to trigger a rule:

    * The rule is applied if the record title contains the word 'urgent' (**If**).
    * The rule is applied if the record title does not contain the word 'urgent' (**NOT If**).
    * The rule is applied if the record title contains the word 'urgent', unless the record was created before a specified date (**If** and **NOT If**).

6. Select criteria for which content the rule will apply to.

7. Select the actions performed when the conditions are met, and any other sub action required for that specific action.

    For example, if you select **Move**, you must also enter a location in the **Destination folder** field.

8. Select additional options:

    * **Run rule in background**: Lets you continue working while the rule is running. You can also select an action to run if there's a problem with the rule.
    * **Rule applies to subfolders**: Apply the rule to this folder and all its subfolders.
    * **Disable rule**: Switch off the rule.

9. Click **Create** to save the rule.

The folder rule created will immediately start managing your content.
---
title: Tags and Categories
---

You can assign tags, and create tags in the Digital Workspace. You can also assign categories in the Digital Workspace. Tags and categories help organize your content so that related information is easy to find, whether it be connected through different projects or concepts. For more information on tags and categories and how to set this up using the Control Center, see [tags]({% link content-services/latest/admin/control-center.md %}#tags) or [categories]({% link content-services/latest/admin/control-center.md %}#categories).

## Tags

You can assign tags, and create tags for your content within the Digital Workspace.

1. Sign into the Digital Workspace.

2. Find the content you want to work with and select it by clicking once on the **Type** icon next to its **Name**.

3. Click the **View Details** button on the top right.

4. Click the **Edit icon** at the bottom of the **Details pane**.

5. Click the **+** symbol next to **Tags**.

6. Search for and select the tag or tags you want to add to your content, or you can provide a name and create a new tag from here, and then click **Save Changes**

   If you create a new tag it will be created in the Control Center.

## Categories

You can assign categories to your content within the Digital Workspace.

1. Sign into the Digital Workspace.

2. Find the content you want to work with and select it by clicking once on the **Type** icon next to its **Name**.

3. Click the **View Details** button on the top right.

4. Click the **Edit icon** at the bottom of the **Details pane**.

5. Click the **+** symbol next to **Categories**.

6. Search for the category or categories you want to add to your content, and then click **Save Changes**.

> **Note:** You can't create new categories in the Digital Workspace, you can only create them from the Control Center.
