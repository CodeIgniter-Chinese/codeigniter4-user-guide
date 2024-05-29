################
CodeIgniter URL
################

.. contents::
    :local:
    :depth: 2

默认情况下,CodeIgniter 的 URL 旨在对搜索引擎和人类友好。它使用基于 **段** 的方法,而不是与动态系统同义的标准“查询字符串”方法::

    https://example.com/news/article/my_article

你可以使用 :doc:`URI 路由 </incoming/routing>` 功能灵活地定义 URL。

:doc:`URI库 <../libraries/uri>` 和 :doc:`URL辅助函数 <../helpers/url_helper>` 包含可以轻松使用 URI 数据的函数。

.. _urls-url-structure:

URL 结构
=============

基本 URL 仅包含主机名
-----------------------------------

当你有基本 URL **https://www.example.com/** 并想象以下 URL 时::

    https://www.example.com/blog/news/2022/10?page=2

我们使用以下术语:

========== ============================ =========================================
术语       例子                         描述
========== ============================ =========================================
基本 URL   **https://www.example.com/** 基本 URL 通常表示为 **baseURL**。
URI 路径   /blog/news/2022/10
路由路径   /blog/news/2022/10           相对于基本 URL 的 URI 路径。它也称为 **URI 字符串**。
查询       page=2
========== ============================ =========================================

基本 URL 包含子文件夹
-----------------------------

当你有基本 URL **https://www.example.com/ci-blog/** 并想象以下 URL 时::

    https://www.example.com/ci-blog/blog/news/2022/10?page=2

我们使用以下术语:

========== ==================================== =========================================
术语       例子                                  描述
========== ==================================== =========================================
基本 URL   **https://www.example.com/ci-blog/** 基本 URL 通常表示为 **baseURL**。
URI 路径   /ci-blog/blog/news/2022/10
路由路径   /blog/news/2022/10                    相对于基本 URL 的 URI 路径。它也称为 **URI 字符串**。
查询       page=2
========== ==================================== =========================================

.. _urls-uri-security:

URI 安全性
==========

.. versionadded:: 4.4.7

.. important::
    从 v4.4.7 版本之前升级的用户需要在 **app/Config/App.php** 中添加以下内容才能使用此功能::

        public string $permittedURIChars = 'a-z 0-9~%.:_\-';

为了帮助尽量减少可能将恶意数据传递到你的应用程序的可能性，CodeIgniter 对 URI 字符串（路由路径）允许的字符相当严格。URI 只能包含以下内容：

- 字母数字文本（仅限拉丁字符）
- 波浪号：``~``
- 百分号：``%``
- 句点：``.``
- 冒号：``:``
- 下划线：``_``
- 减号：``-``
- 空格：`` ``

.. note::
    该检查由 ``Router`` 执行。Router 获取由 ``SiteURI`` 类保存的 URL 编码值，对其进行解码，然后检查它是否包含不允许的字符串。

添加允许的字符
----------------

可以通过 ``Config\App::$permittedURIChars`` 更改允许的字符。

如果你想在 URI 路径中使用 Unicode，请对其进行修改以允许使用这些字符。例如，如果你想使用孟加拉语字符，你需要在 **app/Config/App.php** 中设置以下值::

    public string $permittedURIChars = 'a-z 0-9~%.:_\-\x{0980}-\x{09ff}';

可以在维基百科的 `Unicode block`_ 中找到完整的 Unicode 范围列表。

.. _Unicode block: https://en.wikipedia.org/wiki/Unicode_block

.. _urls-remove-index-php:

删除 index.php 文件
===========================

当你使用 Apache Web 服务器时，默认情况下，在你的 URL 中需要 **index.php** 文件::

    example.com/index.php/news/article/my_article

如果你的服务器支持重写 URL,你可以使用 URL 重写轻松删除此文件。这由不同的服务器以不同的方式处理,但我们将在这里展示两个最常见的 Web 服务器的示例。

.. _urls-remove-index-php-apache:

Apache Web 服务器
-----------------

Apache 必须启用 *mod_rewrite* 扩展。如果是,你可以使用一些简单规则的 ``.htaccess`` 文件。这里是一个这样文件的示例,使用“否定”方法,其中重定向除指定项之外的所有内容:

.. code-block:: apache

    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.*)$ index.php/$1 [L]

在这个例子中,除了现有目录和现有文件的任何 HTTP 请求都被视为对你的 index.php 文件的请求。

.. note:: 这些特定规则可能不适用于所有服务器配置。

.. note:: 也要从上述规则中排除你可能需要从外界访问的任何资源。

.. _urls-remove-index-php-nginx:

Nginx
-----

在 Nginx 中,你可以定义一个位置块并使用 ``try_files`` 指令来获取与我们在上面的 Apache 配置中相同的效果:

.. code-block:: nginx

    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }

这将首先查找与 URI 匹配的文件或目录(从 root 和 alias 指令的设置构造每个文件的完整路径),然后将请求以及任何参数发送到 index.php 文件。
