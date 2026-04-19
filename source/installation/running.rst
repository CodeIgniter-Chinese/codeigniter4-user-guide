################
运行你的应用
################

.. contents::
    :local:
    :depth: 3

CodeIgniter 4 应用可以通过多种方式运行：部署在 Web 服务器上、使用虚拟化环境，或使用 CodeIgniter 的命令行工具进行测试。
本节将介绍如何使用这些方式，并说明各自的优缺点。

.. important:: 务必注意文件名的大小写。许多开发者在 Windows 或 macOS 上使用大小写不敏感的文件系统进行开发。
    然而，大多数服务器环境使用的是大小写敏感的文件系统。
    如果文件名大小写不正确，在本地可运行的代码在服务器上将无法工作。

如果刚接触 CodeIgniter，请先阅读用户指南中的
:doc:`入门 </intro/index>`
章节，开始学习如何构建动态 PHP 应用。祝你使用愉快！

.. _initial-configuration:

*********************
初始配置
*********************

配置站点 URI
============================

使用文本编辑器打开 **app/Config/App.php** 文件。

#. $baseURL
    将站点的基础 URL 设置为 ``$baseURL``。
    如果需要更高的灵活性，也可以在 :ref:`.env <dotenv-file>` 文件中将 baseURL
    设置为 ``app.baseURL = 'http://example.com/'``。
    **baseURL 必须始终以斜杠结尾！**

    .. note:: 如果 ``baseURL`` 未正确设置，在开发模式下，
        调试工具栏可能无法正常加载，页面显示时间也可能明显变长。

#. $indexPage
    如果不希望在站点 URI 中包含 **index.php**，请将 ``$indexPage`` 设置为 ``''``。
    当框架生成站点 URI 时，会使用此设置。

    .. note:: 你可能需要配置 Web 服务器，才能通过不包含 **index.php** 的 URL 访问站点。
        参见 :ref:`CodeIgniter URL <urls-remove-index-php>`。

配置数据库连接设置
======================================

如果计划使用数据库，请使用文本编辑器打开 **app/Config/Database.php** 文件，
并设置数据库参数。
也可以在 **.env** 文件中进行这些设置。
详情请参见 :ref:`数据库配置 <database-config-explanation-of-values>`。

设置为开发模式
=======================

如果不是在生产服务器上运行，请在 **.env** 文件中将 ``CI_ENVIRONMENT`` 设置为
``development``，以便使用提供的调试工具。
详情请参见 :ref:`setting-development-mode`。

.. important:: 在生产环境中，应当禁用错误显示以及任何仅用于开发的功能。
    在 CodeIgniter 中，可以通过将环境设置为 "production" 来实现。
    默认情况下，应用将以 "production" 环境运行。
    另请参阅 :ref:`environment-constant`。

设置 writable 文件夹权限
==============================

如果通过 Web 服务器（如 Apache 或 Nginx）运行站点，
需要修改项目中 **writable** 文件夹的权限，
使其对 Web 服务器所使用的用户或账号可写。

.. _spark-phpini-check:

检查 PHP ini 设置
=========================

.. versionadded:: 4.5.0

`PHP ini 配置`_ 会改变 PHP 的行为。
CodeIgniter 提供了一个命令，用于检查重要的 PHP 设置。

.. _PHP ini 配置: https://www.php.net/manual/zh/ini.list.php

.. code-block:: console

    php spark phpini:check

*Recommended* 列显示的是生产环境下的推荐值。
在开发环境中，这些值可能有所不同。

.. note::
    如果无法使用 spark 命令，也可以在控制器中调用 ``CheckPhpIni::run(false)``。

    例如：

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

CodeIgniter 4 内置了一个本地开发服务器，
基于 PHP 内置 Web 服务器并结合 CodeIgniter 路由。
可以在项目主目录中使用以下命令启动：

.. code-block:: console

    php spark serve

服务器启动后，可以在浏览器中通过 http://localhost:8080 访问应用。

.. note:: 内置开发服务器仅应用于本地开发环境，绝不能用于生产服务器。

如果需要在 localhost 以外的主机名上运行站点，
首先需要将该主机名添加到 **hosts** 文件中。
文件的具体位置因操作系统而异，
但在所有类 Unix 系统（包括 macOS）中，
通常位于 **/etc/hosts**。

本地开发服务器支持三个命令行选项进行自定义：

- 使用 ``--host`` CLI 选项指定运行应用的主机名：

    .. code-block:: console

        php spark serve --host example.dev

- 默认端口为 8080。如果有多个站点运行，或该端口已被占用，
  可以使用 ``--port`` CLI 选项指定其他端口：

    .. code-block:: console

        php spark serve --port 8081

- 也可以使用 ``--php`` CLI 选项指定要使用的 PHP 版本，
  其值为 PHP 可执行文件的路径：

    .. code-block:: console

        php spark serve --php /usr/bin/php7.6.5.4

***************************
FrankenPHP 的 Worker 模式
***************************

.. versionadded:: 4.7.0

.. important:: Worker 模式目前处于 **实验阶段**。目前官方唯一支持的 Worker 实现为 **FrankenPHP**，该项目由 PHP 基金会支持。

FrankenPHP 是一款支持 Worker 模式的现代 PHP 应用服务器，允许应用程序在同一 PHP 进程中处理多个请求，从而提升性能。

快速上手
===========

1. 通过 `静态二进制文件 <https://github.com/php/frankenphp/releases>`_ 安装 FrankenPHP

2. 生成 Worker 模式文件：

.. code-block:: console

    php spark worker:install

3. 启动服务器：

.. code-block:: console

    frankenphp run

有关详细配置、性能调优以及状态管理的重要注意事项，请参阅 :doc:`worker_mode`。

*******************
使用 Apache 托管
*******************

CodeIgniter4 Web 应用通常运行在 Web 服务器上。
Apache HTTP Server 是“标准”平台，
本用户指南中的大部分内容都基于 Apache。

Apache 在许多平台中默认集成，
也可以通过 `Bitnami <https://bitnami.com/stacks/infrastructure>`_
下载包含数据库引擎和 PHP 的集成包。

配置主配置文件
==========================

启用 mod_rewrite
--------------------

“mod_rewrite” 模块用于支持不包含 "index.php" 的 URL，
用户指南默认启用该模块。

请确保在主配置文件（如 **apache2/conf/httpd.conf**）中
启用了（取消注释）该模块：

.. code-block:: apache

    LoadModule rewrite_module modules/mod_rewrite.so

设置文档根目录
---------------------

还需要确保默认文档根目录的 ``<Directory>`` 元素中，
``AllowOverride`` 设置已启用：

.. code-block:: apache

    <Directory "/opt/lamp/apache2/htdocs">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

使用 VirtualHost 托管
========================

推荐使用“虚拟主机”来运行应用，
可以为每个项目设置不同的别名。

启用 vhost_alias_module
---------------------------

请确保在主配置文件（如 **apache2/conf/httpd.conf**）中
启用了（取消注释）虚拟主机模块：

.. code-block:: apache

    LoadModule vhost_alias_module modules/mod_vhost_alias.so

添加主机别名
-----------------

在 **hosts** 文件中添加主机别名，
类 Unix 平台通常是 **/etc/hosts**，
Windows 则是 **c:\\Windows\\System32\\drivers\\etc\\hosts**。

在文件中添加一行，
例如 ``myproject.local`` 或 ``myproject.test``::

    127.0.0.1 myproject.local

设置 VirtualHost
-------------------

在虚拟主机配置文件中为 Web 应用添加一个 ``<VirtualHost>`` 元素，
例如 **apache2/conf/extra/httpd-vhost.conf**：

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

上述配置假设项目目录结构如下：

.. code-block:: text

    apache2/
       ├── myproject/      (项目目录)
       │      └── public/  (myproject.local 的 DocumentRoot)
       └── htdocs/

重启 Apache。

测试
-------

完成以上配置后，
可以在浏览器中通过 **http://myproject.local/** 访问 Web 应用。

每次修改 Apache 配置后，都需要重启 Apache。

使用子目录托管
======================

如果希望使用类似 **http://localhost/myproject/** 的 baseURL，
可以通过以下三种方式实现。

创建符号链接
--------------

将项目目录放置在以下位置，其中 **htdocs** 为 Apache 文档根目录::

    ├── myproject/ (项目目录)
    │      └── public/
    └── htdocs/

进入 **htdocs** 目录并创建符号链接：

.. code-block:: console

    cd htdocs/
    ln -s ../myproject/public/ myproject

使用 Alias
-----------

将项目目录放置在以下位置，其中 **htdocs** 为 Apache 文档根目录::

    ├── myproject/ (项目目录)
    │      └── public/
    └── htdocs/

在主配置文件（如 **apache2/conf/httpd.conf**）中添加：

.. code-block:: apache

    Alias /myproject /opt/lamp/apache2/myproject/public
    <Directory "/opt/lamp/apache2/myproject/public">
        AllowOverride All
        Require all granted
    </Directory>

重启 Apache。

添加 .htaccess
----------------

最后的手段是在项目根目录中添加 **.htaccess**。

不建议将项目目录直接放在文档根目录下。
但在共享主机等别无选择的情况下，可以使用此方法。

将项目目录放置在以下位置，并创建 **.htaccess** 文件，其中 **htdocs** 为 Apache 文档根目录::

    └── htdocs/
        └── myproject/ (项目目录)
            ├── .htaccess
            └── public/

编辑 **.htaccess** 内容如下：

.. code-block:: apache

    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteRule ^(.*)$ public/$1 [L]
    </IfModule>

    <FilesMatch "^\.">
        Require all denied
        Satisfy All
    </FilesMatch>

并移除 **public/.htaccess** 中的重定向设置：

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
        # Checks to see if the user is attempting to access a valid file,
        # such as an image or css document, if this isn't true it sends the
        # request to the front controller, index.php

使用 mod_userdir 托管（共享主机）
=======================================

在共享主机环境中，常见做法是使用 Apache 模块 “mod_userdir”，
自动为每个用户启用虚拟主机。
要在这些用户目录中运行 CodeIgniter4，需要额外配置。

以下内容假设服务器已配置好 mod_userdir。
有关启用该模块的说明，请参阅
`Apache 官方文档 <https://httpd.apache.org/docs/2.4/howto/public_html.html>`_。

由于 CodeIgniter4 默认期望服务器在 **public/index.php** 中找到框架前端控制器，
必须将该位置指定为请求查找的替代路径
（即使 CodeIgniter4 安装在用户 Web 目录中）。

默认的用户 Web 目录 **~/public_html** 由 ``UserDir`` 指令指定，
通常位于 **apache2/mods-available/userdir.conf**
或 **apache2/conf/extra/httpd-userdir.conf**：

.. code-block:: apache

    UserDir public_html

因此，需要配置 Apache，
使其在尝试提供默认目录之前，
优先查找 CodeIgniter 的 public 目录：

.. code-block:: apache

    UserDir "public_html/public" "public_html"

同时也要为 CodeIgniter 的 public 目录设置相应的选项和权限。
一个示例 **userdir.conf** 如下：

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

移除 index.php
======================

参见 :ref:`CodeIgniter URL <urls-remove-index-php-apache>`。

设置运行环境
===================

参见 :ref:`处理多个环境 <environment-apache>`。

******************
使用 Nginx 托管
******************

Nginx 是第二大常用的 Web 托管 HTTP 服务器。
下面示例展示了在 Ubuntu Server 下，
使用 PHP 8.1 FPM（Unix 套接字）的配置。

default.conf
============

该配置支持不包含 "index.php" 的 URL，
并对以 ".php" 结尾的 URL 使用 CodeIgniter 的
“404 - File Not Found”。

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

            # With php-fpm:
            fastcgi_pass unix:/run/php/php8.1-fpm.sock;
            # With php-cgi:
            # fastcgi_pass 127.0.0.1:9000;
        }

        error_page 404 /index.php;

        # deny access to hidden files such as .htaccess
        location ~ /\. {
            deny all;
        }
    }

设置运行环境
===================

参见 :ref:`处理多个环境 <environment-nginx>`。

*************************************
部署到共享托管服务
*************************************

参见 :ref:`部署 <deployment-to-shared-hosting-services>`。

*********************
引导启动应用
*********************

在某些场景下，
需要加载框架但并不实际运行整个应用。
这在为项目进行单元测试时尤其有用，
也适合第三方工具对代码进行分析或修改。

框架为这些场景提供了两个独立的引导脚本：

- **system/Test/bootstrap.php**：主要用于单元测试。
- **system/util_bootstrap.php**：用于其他需要访问框架的脚本。
  建议在非测试脚本中使用该文件，因为当抛出异常时，它不会优雅地失败。

在引导过程中，
项目的大多数路径都会被定义。
可以使用预定义常量来覆盖这些路径，
但如果使用默认设置，
请确保路径与所选安装方式的预期目录结构保持一致。
