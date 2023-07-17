运行您的应用程序
################

.. contents::
    :local:
    :depth: 2

CodeIgniter 4 应用程序可以通过多种方式运行：托管在 Web 服务器上，使用虚拟化，或者使用 CodeIgniter 的命令行工具进行测试。本节介绍如何使用每种技术，并解释了它们的一些优缺点。

.. important:: 关于文件名的大小写，您应该始终小心。许多开发者在 Windows 或 macOS 上使用大小写不敏感的文件系统进行开发。然而，大多数服务器环境使用大小写敏感的文件系统。如果文件名大小写不正确，则在服务器上无法正常工作的代码在本地环境下也将无法正常工作。

如果您是 CodeIgniter 的新手，请阅读用户指南的 :doc:`入门指南 </intro/index>` 部分，开始学习构建动态 PHP 应用程序的方法。祝您使用愉快！

.. _initial-configuration:

初始配置
=====================

#. 使用文本编辑器打开 **app/Config/App.php** 文件，并将您的基本 URL 设置为 ``$baseURL``。如果您需要更灵活的配置，也可以在 :ref:`.env <dotenv-file>` 文件中设置 baseURL，例如 ``app.baseURL = 'http://example.com/'``。 （始终在基本 URL 后加上斜杠！）

    .. note:: 如果未正确设置 ``baseURL``，在开发模式下，调试工具栏可能无法正确加载，并且网页显示可能需要更长的时间。

#. 如果您打算使用数据库，使用文本编辑器打开
   **app/Config/Database.php** 文件，并设置您的
   数据库设置。或者，您也可以在 **.env** 文件中进行设置。
#. 如果它不在生产服务器上，请在 **.env** 文件中将 ``CI_ENVIRONMENT`` 设置为 ``development``，以便利用提供的调试工具。有关详细信息，请参阅 :ref:`设置开发模式 <setting-development-mode>`。

    .. important:: 在生产环境中，您应该禁用错误显示和任何其他仅用于开发的功能。在 CodeIgniter 中，可以通过将环境设置为“production”来实现。默认情况下，应用程序将使用“production”环境运行。另请参阅 :ref:`environment-constant`。

.. note:: 如果您将使用 Web 服务器（例如 Apache 或 Nginx）运行您的站点，您需要修改项目中的 ``writable`` 文件夹的权限，以便由 Web 服务器使用的用户或账户具有写入权限。

本地开发服务器
========================

CodeIgniter 4 自带一个本地开发服务器，利用 PHP 的内置 Web 服务器和 CodeIgniter 的路由功能。您可以使用 ``serve`` 脚本来启动它，在主目录下使用以下命令行::

    > php spark serve

这将启动服务器，并且您现在可以在浏览器中通过 http://localhost:8080 查看您的应用程序。

.. note:: 内置的开发服务器应该只在本地开发机器上使用。绝对不要在生产服务器上使用。

如果您需要在除 localhost 之外的主机上运行站点，您首先需要将主机添加到您的 ``hosts`` 文件中。该文件的确切位置在每个主要操作系统中都有所不同，不过所有的类 Unix 系统（包括 OS X）通常将该文件保存在 **/etc/hosts** 中。

可以使用三个命令行选项自定义本地开发服务器：

- 您可以使用 ``--host`` CLI 选项指定要在其上运行应用程序的不同主机::

    > php spark serve --host example.dev

- 默认情况下，服务器运行在端口 8080 上，但您可能有多个站点正在运行，或者已经有另一个应用程序使用该端口。您可以使用 ``--port`` CLI 选项指定一个不同的端口::

    > php spark serve --port 8081

- 您还可以使用 ``--php`` CLI 选项指定要使用的特定版本的 PHP，其值设置为要使用的 PHP 可执行文件的路径::

    > php spark serve --php /usr/bin/php7.6.5.4

使用 Apache 托管
===================

CodeIgniter 4 Web 应用程序通常托管在 Web 服务器上。Apache 的 ``httpd`` 是“标准”平台，在我们的大部分文档中都默认使用它。

Apache 随附于许多平台，但也可以从 `Bitnami <https://bitnami.com/stacks/infrastructure>`_ 下载包含数据库引擎和 PHP 的捆绑包。

.htaccess
---------

我们的用户指南假设使用了“mod_rewrite”模块，该模块允许 URL 中没有 "index.php"，请确保该模块已启用（取消注释）在主配置文件中，例如 ``apache2/conf/httpd.conf``::

    LoadModule rewrite_module modules/mod_rewrite.so

还要确保默认文档根目录的 <Directory> 元素也启用了此设置，在 "AllowOverride" 设置中::

    <Directory "/opt/lamp/apache2/htdocs">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

去除 index.php
----------------------

请参阅 :ref:`CodeIgniter URLs <urls-remove-index-php-apache>`。

虚拟主机
---------------

我们建议使用“虚拟主机”来运行您的应用程序。您可以为您工作的每个应用程序设置不同的别名。

确保虚拟主机模块已在主配置文件中启用（取消注释），例如 ``apache2/conf/httpd.conf``::

    LoadModule vhost_alias_module modules/mod_vhost_alias.so

在您的 "hosts" 文件中添加一个主机别名，通常在类 Unix 系统的平台上是 ``/etc/hosts``，在 Windows 上是 ``c:/Windows/System32/drivers/etc/hosts``。在文件中

添加一行。例如，可以是 "myproject.local" 或 "myproject.test"::

    127.0.0.1 myproject.local

在虚拟主机配置内添加一个 <VirtualHost> 元素，例如在虚拟主机配置文件中的 ``apache2/conf/extra/httpd-vhost.conf``::

    <VirtualHost *:80>
        DocumentRoot "/opt/lamp/apache2/htdocs/myproject/public"
        ServerName myproject.local
        ErrorLog "logs/myproject-error_log"
        CustomLog "logs/myproject-access_log" common
    </VirtualHost>

如果您的项目文件夹不是 Apache 文档根目录的子文件夹，则您的 <VirtualHost> 元素可能需要嵌套的 <Directory> 元素，以授予 Web 服务器对文件的访问权限。

使用 mod_userdir（共享主机）
--------------------------------

在共享托管环境中的常见做法是使用 Apache 模块 "mod_userdir" 自动启用每个用户的虚拟主机。为了允许从这些每个用户目录中运行 CodeIgniter4，需要进行额外的配置。

以下假设服务器已经配置了 mod_userdir。关于启用此模块的指南可在 `Apache 文档 <https://httpd.apache.org/docs/2.4/howto/public_html.html>`_ 中找到。

因为 CodeIgniter4 默认情况下期望服务器在 ``/public/index.php`` 处找到框架前端控制器，所以您必须指定此位置作为搜索请求的替代位置（即使 CodeIgniter4 安装在每个用户的 Web 目录中）。

默认的用户 Web 目录 ``~/public_html`` 是由 ``UserDir`` 指令指定的，通常位于 ``/apache2/mods-available/userdir.conf`` 或 ``/apache2/conf/extra/httpd-userdir.conf`` 中::

    UserDir public_html

因此，您需要配置 Apache，在尝试提供默认服务之前，首先查找 CodeIgniter 的 public 目录::

    UserDir "public_html/public" "public_html"

还请确保为 CodeIgniter 的 public 目录指定选项和权限。一个 ``userdir.conf`` 可能如下所示::

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

设置环境
-------------------

请参阅 :ref:`处理多环境 <environment-apache>`。

测试
-------

通过上述配置，您的 Web 应用程序将可以通过 URL ``http://myproject.local`` 在浏览器中访问。

每当更改 Apache 配置时，都需要重新启动 Apache。

使用 Nginx 托管
==================

Nginx 是第二个最广泛使用的 Web 托管 HTTP 服务器。这里您可以找到使用 PHP 7.3 FPM（unix sockets）的 Ubuntu Server 的示例配置。

default.conf
------------

此配置使 URL 中没有 "index.php"，并对以 ".php" 结尾的 URL 使用 CodeIgniter 的 "404 - 文件未找到"。

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
            fastcgi_pass unix:/run/php/php7.3-fpm.sock;
            # 使用 php-cgi：
            # fastcgi_pass 127.0.0.1:9000;
        }

        error_page 404 /index.php;

        # 拒绝访问隐藏文件，例如 .htaccess
        location ~ /\. {
            deny all;
        }
    }

设置环境
-------------------

请参阅 :ref:`处理多环境 <environment-nginx>`。

引导应用程序
=====================

在某些场景中，您可能希望加载框架，而不实际运行整个应用程序。这对于对项目进行单元测试非常有用，但也可以用于使用第三方工具来分析和修改您的代码。该框架提供了一个专门用于这种情况的单独引导脚本：``system/Test/bootstrap.php``。

大多数路径到您的项目都在引导过程中定义。您可以使用预定义的常量覆盖这些路径，但是当使用默认值时，请确保您的路径与预期的目录结构对齐，以适应您的安装方法。
