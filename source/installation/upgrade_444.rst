#############################
从 4.4.3 升级到 4.4.4
#############################

请参考对应于你的安装方法的升级指南。

- :ref:`Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`Composer 安装在已有项目中添加 CodeIgniter4 升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

**********************
强制性文件更改
**********************

错误文件
===========

更新以下文件以显示正确的错误信息：

- app/Views/errors/cli/error_exception.php
- app/Views/errors/html/error_exception.php

****************
重大更改
****************

.. _upgrade-444-validation-with-dot-array-syntax:

使用 Dot 数组语法验证
================================

如果你在验证规则中使用 :ref:`Dot 数组语法 <validation-dot-array-syntax>`，已修复了一个 ``*`` 在错误下标验证数据的错误。

在以前的版本中，规则 key ``contacts.*.name`` 错误地捕获了任何级别的数据，如 ``contacts.*.name``，``contacts.*.*.name``，``contacts.*.*.*.name`` 等。

以下代码解释了详细信息：

.. literalinclude:: upgrade_444/001.php
   :lines: 2-

如果你有依赖于这个错误的代码，修复规则 key。

验证规则匹配和差异
====================================

由于在严格和传统规则中使用 ``matches`` 和 ``differs`` 验证非字符串类型数据的情况下已经修复了错误，如果你正在使用这些规则并验证非字符串数据，验证结果可能会被更改（修复）。

注意，传统规则不应该用于验证非字符串的数据。

在 CURLRequest 中使用 `ssl_key` 选项已被移除
==========================================================

CURLRequest 选项 `ssl_key` 不再被识别。
如果在使用，选项 `ssl_key` 必须被选项 `verify` 替代，以定义 CURLRequest 的 CA 包路径。

CURLRequest 选项 `verify` 也可以像往常一样接受 *布尔值*。

*************
项目文件
*************

**项目空间** （root，app，public，writable）中的一些文件已经更新。由于这些文件在 **system** 范围之外，没有你的干预不会发生改变。

有一些第三方 CodeIgniter 模块可用于帮助合并对项目空间的更改：`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

所有更改
===========

这是 **项目空间** 中所有更改的文件列表；
许多文件只是简单的注释或格式更改，对运行时没有影响：

- app/Config/App.php
- app/Config/Autoload.php
- app/Config/Boot/development.php
- app/Config/Boot/testing.php
- app/Config/Cache.php
- app/Config/Email.php
- app/Config/Filters.php
- app/Config/Kint.php
- app/Config/Modules.php
- app/Config/Publisher.php
- app/Config/Session.php
- app/Views/errors/cli/error_exception.php
- app/Views/errors/html/error_exception.php
- composer.json
- env
- spark
