CodeIgniter 的 URL
===================

默认情况下，CodeIgniter 的 URL 被设计成让搜索引擎和人类都容易阅读的。而不是使用与动态系统相似的标准的“查询字符串”方式的 URL，CodeIgniter 采用了基于 **段** 的方式：

    https://example.com/news/article/my_article

你可以使用 :doc:`URI 路由 </incoming/routing>` 来定义 URL。

:doc:`URI 库 <../libraries/uri>` 和 :doc:`URL 帮助库 <../helpers/url_helper>` 包含了一些函数，方便你处理 URI 数据。

.. _urls-url-structure:

URL 结构
========

基础 URL 只包含主机名
---------------------

当你拥有基础 URL **https://www.example.com/** 并想象以下 URL 时：

    https://www.example.com/blog/news/2022/10?page=2

我们使用以下术语：

======== ============================
基础 URL **https://www.example.com/**
URI 路径 /blog/news/2022/10
路由      /blog/news/2022/10
查询      page=2
======== ============================

基础 URL 包含子文件夹
--------------------

当你拥有基础 URL **https://www.example.com/ci-blog/** 并想象以下 URL 时：

    https://www.example.com/ci-blog/blog/news/2022/10?page=2

我们使用以下术语：

======== ====================================
基础 URL **https://www.example.com/ci-blog/**
URI 路径 /ci-blog/blog/news/2022/10
路由      /blog/news/2022/10
查询      page=2
======== ====================================

.. _urls-remove-index-php:

删除 index.php 文件
======================

默认情况下，URL 中将包括 **index.php** 文件：

    example.com/index.php/news/article/my_article

如果你的服务器支持重写 URL，你可以轻松地通过 URL 重写来删除此文件。不同的服务器处理方式不同，我们在这里将为两个最常见的 Web 服务器提供一些示例。

.. _urls-remove-index-php-apache:

Apache Web 服务器
------------------------

Apache 必须启用 *mod_rewrite* 扩展。如果启用了，你可以使用一个带有一些简单规则的 ``.htaccess`` 文件。以下是这样一个文件的示例，使用“反向”方法，在该方法中除了指定的项，其他所有内容都将被重定向：

.. code-block:: apache

    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.*)$ index.php/$1 [L]

在此示例中，任何 HTTP 请求，除了那些针对现有目录和现有文件的请求外，都将被视为对 index.php 文件的请求。

.. note:: 这些特定规则可能不适用于所有服务器配置。

.. note:: 确保还要从上述规则中排除你可能需要从外部访问的任何资产。

.. _urls-remove-index-php-nginx:

NGINX
--------

在 NGINX 中，你可以定义一个 location 块，并使用 ``try_files`` 指令来获得与上面 Apache 配置相同的效果：

.. code-block:: nginx

    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }

它首先查找与 URI 匹配的文件或目录（从根和别名指令的设置构造每个文件的完整路径），然后将请求与任何参数一起发送到 index.php 文件。
