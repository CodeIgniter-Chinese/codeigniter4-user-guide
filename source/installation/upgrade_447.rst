#############################
从 4.4.6 升级到 4.4.7
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

**********************
强制文件变更
**********************

URI 安全
============

新增了用于检查 URI 是否包含不允许字符串的功能。
该检查与 CodeIgniter 3 中的 URI 安全机制等效。

建议启用此功能。在 **app/Config/App.php** 中添加以下内容::

        public string $permittedURIChars = 'a-z 0-9~%.:_\-';.

详情参见 :ref:`urls-uri-security`。

错误文件
===========

错误页面已更新。请更新以下文件：

- app/Views/errors/html/debug.css
- app/Views/errors/html/error_exception.php

****************
破坏性变更
****************

.. _upgrade-447-filter-paths:

控制器过滤器中的路径
===========================

已修复一个问题：:doc:`../incoming/filters` 处理的 URI 路径未进行 URL 解码。

.. note:: 请注意，:doc:`路由 <../incoming/routing>` 处理的是已 URL 解码的 URI 路径。

``Config\Filters`` 中有多个位置可用于指定 URI 路径。如果这些路径在 URL 解码后值不同，请将其修改为解码后的值。

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

Time::difference() 与夏令时
===========================

在之前的版本中，当使用 ``Time::difference()`` 比较日期时，如果由于夏令时（DST）导致日期中包含非 24 小时的时段，可能会返回不符合预期的结果。详情参见 :ref:`时间与日期中的说明 <time-viewing-differences>`。

该问题已修复，因此在这种情况下，日期比较结果现在会相差一天。

如果你确实需要保持旧版本的行为（这种情况较少见），请在将日期传递给 ``Time::difference()`` 之前，将参与比较的两个时间都转换为 UTC 时区。

*************
项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件发生了较大变更（包括弃用或视觉调整），建议将更新后的版本与应用进行合并：

配置
------

- app/Config/App.php
    - 新增属性 ``$permittedURIChars``。详情参见 :ref:`urls-uri-security`。

所有变更
===========

以下列出了 **项目空间** 中所有已发生变更的文件；
其中很多只是简单的注释或格式调整，不会影响运行时行为：

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
