#############################
从 4.2.1 升级到 4.2.2
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
****************

网页缓存 Bug 修复
========================

- :doc:`../general/caching` 现在会在 :ref:`after-filters` 执行完成之后，缓存 Response 数据。
- 例如，如果启用了 :ref:`secureheaders`，当页面来自缓存时，现在也会发送 Response 标头。

.. important:: 如果你曾 **基于这个 Bug 编写代码**，并假定在 “后置” 过滤器中对 Response 的修改不会被缓存，那么 **敏感信息可能会被缓存并造成泄露风险**。如果存在这种情况，请修改代码，禁用该页面的缓存。

其他
======

- 方法 ``Forge::createTable()`` 不再执行 ``CREATE TABLE IF NOT EXISTS``。当 `$ifNotExists` 为 true 时，如果在 ``$db->tableExists($table)`` 中未找到该表，才会执行 ``CREATE TABLE``。
- ``Forge::_createTable()`` 的第二个参数 ``$ifNotExists`` 已被弃用。该参数已不再使用，并将在未来版本中移除。
- 当使用 :php:func:`random_string()` 且第一个参数为 ``'crypto'`` 时，如果将第二个参数 ``$len`` 设为奇数，现在会抛出 ``InvalidArgumentException``。请将该参数改为偶数。

破坏性增强
*********************

项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。
目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除了极少数用于修复 Bug 的情况外，对项目空间文件所做的更改不会破坏你的应用。
    此处列出的所有更改在下一个主版本发布之前都是可选的，任何强制性更改都会在上面的章节中说明。

内容变更
===============

* app/Views/errors/html/error_404.php
* app/Views/welcome_message.php
* public/index.php
* spark

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
其中许多只是简单的注释或格式调整，对运行时没有任何影响：

* app/Config/App.php
* app/Config/Constants.php
* app/Config/Logger.php
* app/Config/Paths.php
* app/Views/errors/html/error_404.php
* app/Views/welcome_message.php
