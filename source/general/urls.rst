################
CodeIgniter URL
################

.. contents::
    :local:
    :depth: 2

默认情况下，CodeIgniter 的 URL 设计旨在对搜索引擎友好，同时也便于人类阅读。它不使用动态系统中常见的标准“查询字符串”形式，而是采用一种基于 **分段** 的方法::

    https://example.com/news/article/my_article

你可以使用 :doc:`URI 路由 </incoming/routing>` 功能灵活地定义 URL。

:doc:`URI 库 <../libraries/uri>` 和 :doc:`URL 库 <../helpers/url_helper>` 包含了可以轻松处理 URI 数据的函数。

.. _urls-url-structure:

URL 结构
=============

仅包含主机名的 Base URL
-----------------------------------

当你的 Base URL 为 **https://www.example.com/** 时，假设有以下 URL::

    https://www.example.com/blog/news/2022/10?page=2

我们使用以下术语：

========== ============================ =========================================
术语       示例                         描述
========== ============================ =========================================
Base URL   **https://www.example.com/** Base URL 通常表示为 **baseURL**。
URI path   /blog/news/2022/10
Route path /blog/news/2022/10           相对于 Base URL 的 URI 路径。
                                        也称为 **URI string**。
Query      page=2
========== ============================ =========================================

包含子文件夹的 Base URL
-----------------------------

当你的 Base URL 为 **https://www.example.com/ci-blog/** 时，假设有以下 URL::

    https://www.example.com/ci-blog/blog/news/2022/10?page=2

我们使用以下术语：

========== ==================================== =========================================
术语       示例                                 描述
========== ==================================== =========================================
Base URL   **https://www.example.com/ci-blog/** Base URL 通常表示为 **baseURL**。
URI path   /ci-blog/blog/news/2022/10
Route path /blog/news/2022/10                   相对于 Base URL 的 URI 路径。
                                                也称为 **URI string**。
Query      page=2
========== ==================================== =========================================

.. _urls-uri-security:

URI 安全
============

.. versionadded:: 4.4.7

.. important::
    从 v4.4.7 之前的版本升级的用户需要在 **app/Config/App.php** 中添加以下配置
    才能使用此功能::

        public string $permittedURIChars = 'a-z 0-9~%.:_\-';

为了帮助减少恶意数据传递到应用程序的可能性，CodeIgniter 对 URI 字符串（路由路径）中允许使用的字符有相当严格的限制。URI 只能包含下列字符：

-  字母数字文本（仅限拉丁字符）
-  波浪号：``~``
-  百分号：``%``
-  句点：``.``
-  冒号：``:``
-  下划线：``_``
-  减号：``-``
-  空格：`` ``

.. note::
    此检查由 ``Router`` 执行。Router 接收 ``SiteURI`` 类保存的 URL 编码值，
    解码后检查其是否包含不允许的字符串。

添加允许的字符
---------------------------

允许的字符可以通过 ``Config\App::$permittedURIChars`` 修改。

如果要在 URI 路径中使用 Unicode，需要修改它以允许使用这些字符。
例如，如果要使用孟加拉语，需要在 **app/Config/App.php** 中设置以下值::

    public string $permittedURIChars = 'a-z 0-9~%.:_\-\x{0980}-\x{09ff}';

完整的 Unicode 范围列表可以在维基百科的 `Unicode block`_ 中找到。

.. _Unicode block: https://en.wikipedia.org/wiki/Unicode_block

.. _urls-remove-index-php:

移除 index.php 文件
===========================

当使用 Apache Web 服务器时，默认情况下，URL 中需要包含 **index.php** 文件::

    example.com/index.php/news/article/my_article

如果服务器支持 URL 重写，你可以通过 URL 重写轻松移除这个文件。
不同的服务器处理方式不同，但这里我们将展示两种最常见的 Web 服务器示例。

.. _urls-remove-index-php-apache:

Apache Web 服务器
-----------------

Apache 必须启用 *mod_rewrite* 扩展。如果已启用，你可以使用 ``.htaccess`` 文件配合一些简单的规则。
以下是一个示例，它采用了“排除法”：即除了指定项之外，其他所有请求都会被重定向：

.. code-block:: apache

    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.*)$ index.php/$1 [L]

在此示例中，除了针对现有目录和现有文件的请求外，任何其他 HTTP 请求都会被视为对你的 index.php 文件的请求。

.. note:: 这些特定规则可能不适用于所有服务器配置。

.. note:: 确保从上述规则中排除任何需要从外部访问的资源文件。

.. _urls-remove-index-php-nginx:

Nginx
-----

在 Nginx 中，你可以定义一个 location 块并使用 ``try_files`` 指令来实现与上述 Apache 配置相同的效果：

.. code-block:: nginx

    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }

这将首先查找与 URI 匹配的文件或目录（根据 root 和 alias 指令的设置构造每个文件的完整路径），
然后将请求连同任何参数一起发送给 index.php 文件。
