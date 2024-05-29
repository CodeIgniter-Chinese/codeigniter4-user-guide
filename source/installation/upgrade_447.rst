#############################
从 4.4.6 升级到 4.4.7
#############################

请参阅与你的安装方法对应的升级说明。

- :ref:`Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`Composer 安装 将 CodeIgniter4 添加到一个现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

**********************
强制文件更改
**********************

URI 安全性
============

添加了检查 URI 中不包含不允许的字符串的功能。
此检查等同于 CodeIgniter 3 中的 URI 安全性。

我们建议你启用此功能。在 **app/Config/App.php** 文件中添加以下内容::

        public string $permittedURIChars = 'a-z 0-9~%.:_\-';.

详情请参阅 :ref:`urls-uri-security`。

错误文件
===========

错误页面已更新。请更新以下文件：

- app/Views/errors/html/debug.css
- app/Views/errors/html/error_exception.php

****************
重大变更
****************

.. _upgrade-447-filter-paths:

控制器过滤器中的路径
===========================

已修复 :doc:`../incoming/filters` 处理的 URI 路径未进行 URL 解码的错误。

.. note:: 请注意 :doc:`Router <../incoming/routing>` 处理 URL 解码后的 URI 路径。

``Config\Filters`` 中有一些地方可以指定 URI 路径。如果路径在 URL 解码后有不同的值，请将它们更改为 URL 解码后的值。

例如：

.. code-block:: php

    public array $globals = [
        'before' => [
            'csrf' => ['except' => '%E6%97%A5%E6%9C%AC%E8%AA%9E/*'],
        ],
        // ...
    ];

↓

.. code-block:: php

    public array $globals = [
        'before' => [
            'csrf' => ['except' => '日本語/*'],
        ],
        // ...
    ];

Time::difference() 和夏令时
===========================

在以前的版本中，当使用 ``Time::difference()`` 比较日期时，如果由于夏令时 (DST) 导致日期包含不同于 24 小时的一天，则会返回意外结果。详情请参阅 :ref:`Times and Dates 中的备注 <time-viewing-differences>`。

此错误已修复，因此在这种情况下，日期比较将被移后一日。

在某些不太可能的情况下，如果你希望保持以前版本的行为，请在将要比较的两个日期传递给 ``Time::difference()`` 之前，将它们的时区更改为 UTC。

*************
项目文件
*************

**项目空间**（root, app, public, writable）中的一些文件收到了更新。由于这些文件位于 **system** 范围之外，没有你的干预它们不会被更改。

有一些第三方的 CodeIgniter 模块可以帮助合并对项目空间的更改：`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件进行了重要更改（包括弃用或视觉调整），建议你将更新的版本与应用程序合并：

配置
------

- app/Config/App.php
    - 添加了属性 ``$permittedURIChars``。详情请参阅 :ref:`urls-uri-security`。

所有更改
===========

这是一个 **项目空间** 内所有收到更改的文件列表；
许多将只是简单的注释或格式更改，对运行时没有影响：

- app/Config/App.php
- app/Config/Cache.php
- app/Config/ContentSecurityPolicy.php
- app/Config/Database.php
- app/Config/Exceptions.php
- app/Config/Filters.php
- app/Config/Format.php
- app/Config/Logger.php
- app/Config/Mimes.php
- app/Config/Routing.php
- app/Config/Toolbar.php
- app/Config/Validation.php
- app/Config/View.php
- app/Controllers/BaseController.php
- app/Views/errors/html/debug.css
- app/Views/errors/html/error_exception.php
- composer.json
