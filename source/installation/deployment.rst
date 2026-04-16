##########
部署
##########

.. contents::
    :local:
    :depth: 3

************
优化
************

在将 CodeIgniter 应用部署到生产环境之前，可以通过多种方式提升应用程序的运行效率。

本节介绍 CodeIgniter 提供的优化功能。

.. _spark_optimize:

spark optimize
==============

.. versionadded:: 4.5.0

``spark optimize`` 命令会执行以下优化操作：

- `移除开发依赖包`_
- 启用 `配置缓存`_
- 启用 `FileLocator 缓存`_

Composer 优化
=====================

移除开发依赖包
---------------------

部署时，务必运行以下命令：

.. code-block:: console

    composer install --no-dev

上述命令会移除仅用于开发、在生产环境中不需要的 Composer 包，从而显著减少 vendor 目录的体积。

指定需要发现的包
-------------------------------

如果启用了 Composer 包自动发现机制，在需要时会扫描所有 Composer 包。但实际上并不需要扫描非 CodeIgniter 的包，因此通过指定需要扫描的包，可以避免不必要的扫描开销。

参见 :ref:`modules-specify-composer-packages`。

配置缓存
==============

.. important:: 一旦缓存完成，在删除缓存之前，配置值将不会发生任何变化，
    即使配置文件或 **.env** 已被修改。

缓存 Config 对象可以提升性能。但在更改 Config 值后，必须手动删除缓存。

参见 :ref:`factories-config-caching`。

FileLocator 缓存
===================

缓存 FileLocator 查找到的文件路径可以提升性能。但在添加、删除或修改文件路径后，必须手动删除缓存。

参见 :ref:`file-locator-caching`。

PHP 预加载
==============

通过 PHP 预加载，可以指示服务器在启动时将函数、类等关键文件加载到内存中。
这样，这些元素在所有请求中都能直接使用，跳过常规的加载过程，从而提升应用性能。
但代价是内存占用增加，并且任何更改都需要重启 PHP 引擎才能生效。

.. note:: 如果要使用 `预加载 <https://www.php.net/manual/zh/opcache.preloading.php>`_，
    我们提供了一个 `预加载脚本 <https://github.com/codeigniter4/CodeIgniter4/blob/develop/preload.php>`_。

要求
-----------

使用预加载需要一个专用的 PHP 处理器。通常，Web 服务器配置为使用一个 PHP 处理器，因此一个应用需要一个专用的 Web 服务器。
如果希望在同一台 Web 服务器上为多个应用使用预加载，需要将服务器配置为使用虚拟主机，并为每个虚拟主机分配一个 PHP 处理器，
例如使用多个 PHP-FPM，每个虚拟主机对应一个 PHP 处理器。
预加载会通过读取 ``opcache.preload`` 中指定的文件，将相关定义保留在内存中。

.. note:: 参见 :ref:`running-multiple-app`，了解如何使用一个核心 CodeIgniter4 来处理多个应用。

配置
-------------

如果 PHP 使用了拆分的 INI 配置，请打开 ``php.ini`` 或 ``xx-opcache.ini``，
并建议设置 ``opcache.preload=/path/to/preload.php`` 以及 ``opcache.preload_user=myuser``。

.. note:: ``myuser`` 是运行 Web 服务器的用户。
    如果需要查找拆分 INI 配置的位置，可以运行 ``php --ini``，
    或打开 ``phpinfo()``，并搜索 *Additional .ini files parsed*。

请确保使用 appstarter 安装方式。如果使用手动安装，则必须修改 ``include`` 路径中的目录。

.. literalinclude:: preloading/001.php

.. _deployment-to-shared-hosting-services:

*************************************
部署到共享主机服务
*************************************

.. important::
    **index.php** 已不再位于项目根目录中！
    出于更好的安全性和组件分离考虑，它已被移动到 **public** 目录中。

    这意味着必须将 Web 服务器配置为指向项目的 **public** 目录，
    而不是项目根目录。

指定文档根目录
============================

最佳做法是在服务器配置中，将文档根目录设置为 **public** 目录::

    └── example.com/ (项目目录)
        └── public/  (文档根目录)

请向你的主机服务提供商确认是否可以更改文档根目录。
如果无法更改，请继续查看下一种方式。

使用两个目录
=====================

第二种方式是使用两个目录，并调整路径。
一个目录用于应用，另一个目录作为默认的文档根目录。

将 **public** 目录中的内容上传到 **public_html** （默认的文档根目录），
并将其他文件上传到应用目录中::

    ├── example.com/ (用于应用程序)
    │       ├── app/
    │       ├── vendor/ (或 system/)
    │       └── writable/
    └── public_html/ (默认的文档根目录)
            ├── .htaccess
            ├── favicon.ico
            ├── index.php
            └── robots.txt

更多细节请参见
`在共享主机（cPanel）上安装 CodeIgniter 4 <https://forum.codeigniter.com/showthread.php?tid=76779>`_。

添加 .htaccess
================

最后一种方式是在项目根目录中添加 **.htaccess**。

不建议将项目目录直接放在文档根目录下。
但如果没有其他选择，可以使用这种方式。

按如下结构放置项目目录，其中 **public_html** 是文档根目录，
并创建 **.htaccess** 文件::

    └── public_html/     (默认的文档根目录)
        └── example.com/ (项目目录)
            ├── .htaccess
            └── public/

然后按如下内容编辑 **.htaccess**：

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
