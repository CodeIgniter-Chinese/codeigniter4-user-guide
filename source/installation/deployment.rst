##########
部署
##########

.. contents::
    :local:
    :depth: 3

************
优化
************

在将你的 CodeIgniter 应用程序部署到生产环境之前，有若干事情可以做以提高应用程序的运行效率。

本节将描述 CodeIgniter 提供的优化功能。

.. _spark_optimize:

spark optimize
==============

.. versionadded:: 4.5.0

``spark optimize`` 命令执行以下优化操作：

- `移除开发包`_
- 启用 `配置缓存`_
- 启用 `FileLocator 缓存`_

Composer 优化
==============

移除开发包
------------

当你部署时，不要忘记运行以下命令：

.. code-block:: console

    composer install --no-dev

上述命令将移除仅在开发环境中需要的 Composer 包，这些包在生产环境中并不需要。这将极大地减少 vendor 目录的大小。

指定发现的包
------------------

如果启用了 Composer 包自动发现功能，则在需要时所有的 Composer 包都会被扫描。但没有必要扫描那些不是 CodeIgniter 包的包，所以指定需要扫描的包可以防止不必要的扫描。

参见 :ref:`modules-specify-composer-packages`。

配置缓存
==============

.. important:: 一旦被缓存，配置值在缓存被删除之前将不会被改变，即使配置文件或 **.env** 被修改。

缓存配置对象可以提高性能。然而，在更改配置值时必须手动删除缓存。

参见 :ref:`factories-config-caching`。

FileLocator 缓存
===================

缓存 FileLocator 找到的文件路径可以提高性能。然而，在添加/删除/更改文件路径时必须手动删除缓存。

参见 :ref:`file-locator-caching`。

PHP 预加载
================

使用 PHP 预加载，你可以指示服务器在启动时将核心文件如函数和类加载到内存中。这意味着这些元素在所有请求中都可立即使用，跳过了通常的加载过程，从而提升了应用程序的性能。然而，这会带来增加内存使用的代价，并且需要重启 PHP 引擎才能生效。

.. note:: 如果你想使用 `预加载 <https://www.php.net/manual/en/opcache.preloading.php>`_，
    我们提供了 `预加载脚本 <https://github.com/codeigniter4/CodeIgniter4/blob/develop/preload.php>`_。

需求
-----------

使用预加载需要一个专门的 PHP 处理器。通常情况下，Web 服务器配置为使用一个 PHP 处理器，所以一个应用程序需要一个专用的 Web 服务器。如果你想在一个 Web 服务器上为多个应用使用预加载，请配置你的服务器以使用带有多个 PHP 处理器的虚拟主机，例如多个 PHP-FPM，每个虚拟主机使用一个 PHP 处理器。预加载通过读取在 ``opcache.preload`` 中指定的文件将相关定义保留在内存中。

.. note:: 参见 :ref:`running-multiple-app` 以使用一个核心的 CodeIgniter4 处理多个应用。

配置
-------------

打开 ``php.ini`` 或 ``xx-opcache.ini`` （如果你将 INI 配置分离开来），建议设置 ``opcache.preload=/path/to/preload.php`` 和 ``opcache.preload_user=myuser``。

.. note:: ``myuser`` 是在你的 Web 服务器中运行的用户。如果你想找到分离的 INI 配置的位置，只需运行 ``php --ini`` 或打开 ``phpinfo()`` 文件并搜索 *Additional .ini files parsed*。

确保你使用的是 appstarter 安装。如果使用手动安装，你必须更改 ``include`` 路径中的目录。

.. literalinclude:: preloading/001.php

.. _deployment-to-shared-hosting-services:

*************************************
部署到共享主机服务
*************************************

.. important::
    **index.php** 不再位于项目的根目录中！它已移动到 **public** 目录中，这样更安全，并能更好地分离组件。

    这意味着你应该配置你的 Web 服务器指向项目的 **public** 目录，而不是项目根目录。

指定文档根目录
============================

最好的方式是在服务器配置中将文档根目录设置为 **public** 目录：

    └── example.com/ (项目目录)
        └── public/  (文档根目录)

请与你的主机服务提供商确认是否可以更改文档根目录。如果不能更改文档根目录，请参考下一种方法。

使用两个目录
=====================

第二种方式是使用两个目录，并调整路径。
一个用于应用程序，另一个是默认的文档根目录。

将 **public** 目录的内容上传到 **public_html** （默认的文档根目录），其他文件上传到用于应用程序的目录::

    ├── example.com/ (用于应用程序)
    │       ├── app/
    │       ├── vendor/ (或 system/)
    │       └── writable/
    └── public_html/ (默认的文档根目录)
            ├── .htaccess
            ├── favicon.ico
            ├── index.php
            └── robots.txt

参见
`Install CodeIgniter 4 on Shared Hosting (cPanel) <https://forum.codeigniter.com/showthread.php?tid=76779>`_
获取详细信息。

添加 .htaccess
================

最后一招是在项目根目录中添加 **.htaccess** 文件。

不建议将项目文件夹放在文档根目录中。然而，如果没有其他选择，你可以使用这种方法。

按照以下方式放置你的项目文件夹，其中 **public_html** 是文档根目录，并创建 **.htaccess** 文件：

    └── public_html/     (默认的文档根目录)
        └── example.com/ (项目文件夹)
            ├── .htaccess
            └── public/

并按如下内容编辑 **.htaccess**：

.. code-block:: apache

    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteRule ^(.*)$ public/$1 [L]
    </IfModule>

    <FilesMatch "^\.">
        Require all denied
        Satisfy All
    </FilesMatch>

然后，删除 **public/.htaccess** 中的重定向设置：

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
        # 检查用户是否试图访问有效文件，如图片或 css 文档，如果不是真的，则将
        # 请求发送到前端控制器 index.php
