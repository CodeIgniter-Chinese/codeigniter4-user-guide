################
运行你的应用程序
################

.. contents::
    :local:
    :depth: 3

CodeIgniter 4 应用程序可以以多种不同的方式运行：托管在 Web 服务器上、使用虚拟化技术，或者使用 CodeIgniter 的命令行工具进行测试。本节介绍如何使用每种技术，并解释其中的一些优缺点。

.. important:: 在文件名的大小写方面应始终小心。许多开发人员在 Windows 或 macOS 上使用不区分大小写的文件系统进行开发。然而，大多数服务器环境使用区分大小写的文件系统。如果文件名大小写不正确，本地上正常工作的代码在服务器上将无法正常工作。

如果你是 CodeIgniter 的新手，请阅读用户指南的 :doc:`入门 </intro/index>` 部分，开始学习如何构建动态的 PHP 应用程序。祝你使用愉快！

.. _initial-configuration:

*********************
初始配置
*********************

为你的站点 URI 进行配置
============================

使用文本编辑器打开 **app/Config/App.php** 文件。

#. $baseURL
    将你的基本 URL 设置为 ``$baseURL``。如果你需要更大的灵活性，可以在 :ref:`.env <dotenv-file>` 文件中设置 baseURL，例如 ``app.baseURL = 'http://example.com/'``。**始终在基本 URL 的末尾使用斜杠！**

    .. note:: 如果你没有正确设置 ``baseURL``，在开发模式下，调试工具栏可能无法正确加载，网页可能需要更长的时间才能显示。

#. $indexPage
    如果你不想在站点 URI 中包含 **index.php**，请将 ``$indexPage`` 设置为 ``''``。当框架生成你的站点 URI 时，将使用此设置。

    .. note:: 你可能需要配置你的 Web 服务器以访问不包含 **index.php** 的 URL。请参阅 :ref:`CodeIgniter URL <urls-remove-index-php>`。

配置数据库连接设置
======================================

如果你打算使用数据库，使用文本编辑器打开 **app/Config/Database.php** 文件并设置数据库配置。或者，你也可以在 **.env** 文件中设置这些配置。详细信息请参阅 :ref:`数据库配置 <database-config-explanation-of-values>`。

设置为开发模式
=======================

如果不是在生产服务器上，请在 **.env** 文件中将 ``CI_ENVIRONMENT`` 设置为 ``development``，以利用提供的调试工具。有关详细信息，请参阅 :ref:`setting-development-mode`。

.. important:: 在生产环境中，应禁用错误显示和任何其他仅用于开发的功能。在 CodeIgniter 中，可以通过将环境设置为 "production" 来实现。默认情况下，应用程序将在 "production" 环境下运行。另请参阅 :ref:`environment-constant`。

设置可写文件夹权限
==============================

如果你将使用 Web 服务器（例如 Apache 或 nginx）运行你的站点，你需要修改项目中的 **writable** 文件夹的权限，以便它可以被你的 Web 服务器使用的用户或帐户写入。

.. _spark-phpini-check:

检查 PHP ini 设置
=========================

.. versionadded:: 4.5.0

`PHP ini 设置`_ 更改 PHP 的行为。CodeIgniter 提供了一个命令来检查重要的 PHP 设置。

.. _PHP ini 设置: https://www.php.net/manual/en/ini.list.php

.. code-block:: console

    php spark phpini:check

*推荐* 列显示了生产环境的推荐值。它们在开发环境中可能会有所不同。

.. note::
    如果你不能使用 spark 命令，可以在你的控制器中使用 ``CheckPhpIni::run(false)``。

    例如，

    .. code-block:: php

        <?php

        namespace App\Controllers;

        use CodeIgniter\Security\CheckPhpIni;

        class Home extends BaseController
        {
            public function index(): string
            {
                return CheckPhpIni::run(false);
            }
        }

************************
本地开发服务器
************************

CodeIgniter 4 自带一个本地开发服务器，利用 PHP 的内置 Web 服务器和 CodeIgniter 的路由功能。你可以使用以下命令在主目录中启动它：

.. code-block:: console

    php spark serve

这将启动服务器，你现在可以在浏览器中通过 http://localhost:8080 查看你的应用程序。

.. note:: 内置的开发服务器只应在本地开发机器上使用。它绝不能在生产服务器上使用。

如果你需要在除 localhost 之外的主机上运行站点，你首先需要将主机添加到你的 **hosts** 文件中。文件的确切位置因每个主要操作系统而异，但所有的类 Unix 类型的系统（包括 macOS）通常将文件保存在 **/etc/hosts** 中。

本地开发服务器可以使用三个命令行选项进行自定义：

- 你可以使用 ``--host`` CLI 选项指定要运行应用程序的不同主机：

    .. code-block:: console

        php spark serve --host example.dev

- 默认情况下，服务器在端口 8080 上运行，但你可能有多个站点正在运行，或者已经有其他应用程序使用该端口。你可以使用 ``--port`` CLI 选项指定不同的端口：

    .. code-block:: console

        php spark serve --port 8081

- 你还可以使用 ``--php`` CLI 选项指定要使用的特定版本的 PHP，将其值设置为你要使用的 PHP 可执行文件的路径：

    .. code-block:: console

        php spark serve --php /usr/bin/php7.6.5.4

*******************
使用 Apache 托管
*******************

CodeIgniter 4 网站通常托管在 Web 服务器上。Apache HTTP Server 是“标准”平台，在我们的文档中假定使用它。

Apache 与许多平台捆绑在一起，但也可以从 `Bitnami <https://bitnami.com/stacks/infrastructure>`_ 下载捆绑了数据库引擎和 PHP 的版本。

配置主配置文件
==========================

启用 mod_rewrite
--------------------

"mod_rewrite" 模块允许在 URL 中不包含 "index.php"，我们在用户指南中假定了这一点。

确保在主配置文件中启用（取消注释）重写模块，例如 **apache2/conf/httpd.conf**：

.. code-block:: apache

    LoadModule rewrite_module modules/mod_rewrite.so

设置文档根目录
---------------------

还要确保默认文档根目录的 ``<Directory>`` 元素也启用了这一点，在 ``AllowOverride`` 设置中：

.. code-block:: apache

    <Directory "/opt/lamp/apache2/htdocs">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

使用虚拟主机托管
========================

我们建议使用“虚拟主机”来运行你的应用程序。你可以为你工作的每个应用程序设置不同的别名，

启用 vhost_alias_module
---------------------------

确保在主配置文件中启用（取消注释）虚拟主机模块，例如 **apache2/conf/httpd.conf**：

.. code-block:: apache

    LoadModule vhost_alias_module modules/mod_vhost_alias.so

添加主机别名
-----------------

在你的 "hosts" 文件中添加主机别名，通常在 Unix 类型平台上为 **/etc/hosts**，在 Windows 上为 **c:\Windows\System32\drivers\etc\hosts**。

在文件中添加一行。例如，可以是 ``myproject.local`` 或 ``myproject.test``::

    127.0.0.1 myproject.local

设置虚拟主机
-------------------

在虚拟主机配置中添加一个 ``<VirtualHost>`` 元素，用于你的 Web 应用程序，例如 **apache2/conf/extra/httpd-vhost.conf**：

.. code-block:: apache

    <VirtualHost *:80>
        DocumentRoot "/opt/lamp/apache2/myproject/public"
        ServerName   myproject.local
        ErrorLog     "logs/myproject-error_log"
        CustomLog    "logs/myproject-access_log" common

        <Directory "/opt/lamp/apache2/myproject/public">
            AllowOverride All
            Require all granted
        </Directory>
    </VirtualHost>

上述配置假设项目文件夹位于以下位置：

.. code-block:: text

    apache2/
       ├── myproject/      (项目文件夹)
       │      └── public/  (myproject.local 的 DocumentRoot)
       └── htdocs/

重启 Apache。

测试
-------

使用上述配置，在浏览器中使用 URL **http://myproject.local/** 访问你的 Web 应用程序。

每当更改 Apache 配置时，都需要重新启动 Apache。

使用子文件夹进行托管
======================

如果你希望使用类似 **http://localhost/myproject/** 的子文件夹 baseURL，有三种方法可以实现。

创建符号链接
--------------

将你的项目文件夹放置在以下位置，其中 **htdocs** 是 Apache 的文档根目录::

    ├── myproject/ (项目文件夹)
    │      └── public/
    └── htdocs/

导航到 **htdocs** 文件夹并创建符号链接，如下所示：

.. code-block:: console

    cd htdocs/
    ln -s ../myproject/public/ myproject

使用别名
-----------

将你的项目文件夹放置在以下位置，其中 **htdocs** 是 Apache 的文档根目录::

    ├── myproject/ (项目文件夹)
    │      └── public/
    └── htdocs/

在主配置文件中添加以下内容，例如 **apache2/conf/httpd.conf**：

.. code-block:: apache

    Alias /myproject /opt/lamp/apache2/myproject/public
    <Directory "/opt/lamp/apache2/myproject/public">
        AllowOverride All
        Require all granted
    </Directory>

重启 Apache。

添加 .htaccess
----------------

最后的选择是在项目根目录中添加 **.htaccess** 文件。

不建议将项目文件夹放置在文档根目录中。但是，如果你没有其他选择，例如在共享服务器上，你可以使用此方法。

将你的项目文件夹放置在以下位置，其中 **htdocs** 是 Apache 的文档根目录，并创建 **.htaccess** 文件::

    └── htdocs/
        └── myproject/ (项目文件夹)
            ├── .htaccess
            └── public/

并将 **.htaccess** 编辑如下：

.. code-block:: apache

    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteRule ^(.*)$ public/$1 [L]
    </IfModule>

    <FilesMatch "^\.">
        Require all denied
        Satisfy All
    </FilesMatch>

并且移除 **public/.htaccess** 中的重定向设置：

.. code-block:: diff

    --- a/public/.htaccess
    +++ b/public/.htaccess
    @@ -16,16 +16,6 @@ Options -Indexes
        # http://httpd.apache.org/docs/current/mod/mod_rewrite.html#rewritebase
        # RewriteBase /

    -   # Redirect Trailing Slashes...
    -   RewriteCond %{REQUEST_FILENAME} !-d
    -   RewriteCond %{REQUEST_URI} (.+)/$
    -   RewriteRule ^ %1 [L,R=301]
    -
    -   # Rewrite "www.example.com -> example.com"
    -   RewriteCond %{HTTPS} !=on
    -   RewriteCond %{HTTP_HOST} ^www\.(.+)$ [NC]
    -   RewriteRule ^ http://%1%{REQUEST_URI} [R=301,L]
    -
        # 检查用户是否尝试访问有效文件，
        # 例如图像或 css 文档，如果不是真的则将请求发送到前端控制器 index.php

使用 mod_userdir 进行托管（共享主机）
=======================================

在共享托管环境中，常见做法是使用 Apache 模块 "mod_userdir" 自动启用每个用户的虚拟主机。需要额外的配置才能允许 CodeIgniter4 从这些每个用户目录中运行。

以下假设服务器已经配置为 mod_userdir。有关启用此模块的指南，请参阅 Apache 文档中的 `相关部分 <https://httpd.apache.org/docs/2.4/howto/public_html.html>`_。

由于 CodeIgniter4 默认情况下期望服务器在 **public/index.php** 中找到框架前端控制器，因此你必须指定此位置作为替代位置以搜索请求（即使 CodeIgniter4 安装在每个用户的 Web 目录中）。

默认的用户 Web 目录 **~/public_html** 由 ``UserDir`` 指令指定，通常位于 **apache2/mods-available/userdir.conf** 或 **apache2/conf/extra/httpd-userdir.conf** 中：

.. code-block:: apache

    UserDir public_html

因此，你需要配置 Apache 在尝试提供默认服务之前首先查找 CodeIgniter 的 public 目录：

.. code-block:: apache

    UserDir "public_html/public" "public_html"

确保还为 CodeIgniter 的 public 目录指定选项和权限。一个 **userdir.conf** 可能如下所示：

.. code-block:: apache

    <IfModule mod_userdir.c>
        UserDir "public_html/public" "public_html"
        UserDir disabled root

        <Directory /home/*/public_html>
            AllowOverride All
            Options MultiViews Indexes FollowSymLinks
            <Limit GET POST OPTIONS>
                # Apache <= 2.2:
                # Order allow,deny
                # Allow from all

                # Apache >= 2.4:
                Require all granted
            </Limit>
            <LimitExcept GET POST OPTIONS>
                # Apache <= 2.2:
                # Order deny,allow
                # Deny from all

                # Apache >= 2.4:
                Require all denied
            </LimitExcept>
        </Directory>

        <Directory /home/*/public_html/public>
            AllowOverride All
            Options MultiViews Indexes FollowSymLinks
            <Limit GET POST OPTIONS>
                # Apache <= 2.2:
                # Order allow,deny
                # Allow from all

                # Apache >= 2.4:
                Require all granted
            </Limit>
            <LimitExcept GET POST OPTIONS>
                # Apache <= 2.2:
                # Order deny,allow
                # Deny from all

                # Apache >= 2.4:
                Require all denied
            </LimitExcept>
        </Directory>
    </IfModule>

删除 index.php
======================

请参阅 :ref:`CodeIgniter URL <urls-remove-index-php-apache>`。

设置环境
===================

请参阅 :ref:`处理多个环境 <environment-apache>`。

******************
使用 Nginx 托管
******************

Nginx 是第二常用的用于 Web 托管的 HTTP 服务器。以下是一个在 Ubuntu Server 上使用 PHP 8.1 FPM（Unix 套接字）的示例配置。

default.conf
============

此配置使 URL 中不包含 "index.php"，并对以 ".php" 结尾的 URL 使用 CodeIgniter 的 "404 - File Not Found"。

.. code-block:: nginx

    server {
        listen 80;
        listen [::]:80;

        server_name example.com;

        root  /var/www/example.com/public;
        index index.php index.html index.htm;

        location / {
            try_files $uri $uri/ /index.php$is_args$args;
        }

        location ~ \.php$ {
            include snippets/fastcgi-php.conf;

            # 使用 php-fpm：
            fastcgi_pass unix:/run/php/php8.1-fpm.sock;
            # 使用 php-cgi：
            # fastcgi_pass 127.0.0.1:9000;
        }

        error_page 404 /index.php;

        # 禁止访问隐藏文件，如 .htaccess
        location ~ /\. {
            deny all;
        }
    }

设置环境
===================

请参阅 :ref:`处理多个环境 <environment-nginx>`。

*************************************
部署到共享主机服务
*************************************

参见 :ref:`Deployment <deployment-to-shared-hosting-services>`。

*********************
引导应用程序
*********************

在某些情况下，你可能希望加载框架而不实际运行整个应用程序。这对于对项目进行单元测试非常有用，但也可能对使用第三方工具分析和修改代码很有用。框架提供了一个专门用于此场景的独立引导脚本：**system/Test/bootstrap.php**。

在引导过程中，大部分项目路径都会被定义。你可以使用预定义的常量来覆盖这些路径，但是当使用默认值时，请确保你的路径与安装方法的预期目录结构对齐。
