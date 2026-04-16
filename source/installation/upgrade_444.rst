#############################
从 4.4.3 升级到 4.4.4
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

错误文件
===========

请更新以下文件，以显示正确的错误消息：

- app/Views/errors/cli/error_exception.php
- app/Views/errors/html/error_exception.php

****************
破坏性变更
****************

.. _upgrade-444-validation-with-dot-array-syntax:

使用点数组语法的验证
================================

如果你在验证规则中使用 :ref:`点数组语法 <validation-dot-array-syntax>`，
那么 ``*`` 会在错误维度中验证数据的缺陷现已修复。

在之前的版本中，规则键 ``contacts.*.name`` 会错误地匹配任意层级的数据，
例如 ``contacts.*.name``、``contacts.*.*.name``、``contacts.*.*.*.name`` 等。

以下代码说明了详细情况：

.. literalinclude:: upgrade_444/001.php
   :lines: 2-

如果你的代码依赖该缺陷，需要修正规则键。

Validation 规则中的 matches 和 differs
======================================

由于 Strict Rules 和 Traditional Rules 中 ``matches`` 与 ``differs`` 在验证非字符串类型数据时的缺陷已被修复，
如果你使用这些规则来验证非字符串数据，验证结果可能会发生变化（即得到修正）。

请注意，Traditional Rules 不应用于验证非字符串数据。

CURLRequest 中移除了 `ssl_key` 选项
==========================================================

CURLRequest 选项 `ssl_key` 已不再被识别。

如果你正在使用该选项，必须将 `ssl_key` 替换为 `verify` 选项，
以便为 CURLRequest 定义 CA bundle 的路径。

和以往一样，CURLRequest 选项 `verify` 也可以接受 *boolean* 值。

*************
项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

所有变更
===========

以下列出了 **项目空间** 中所有发生变更的文件；
其中多数只是注释或格式调整，不会影响运行时行为：

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
