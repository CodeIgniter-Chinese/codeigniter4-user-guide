#############################
从 4.6.x 升级到 4.7.0
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

****************
重大变更
****************

要求 PHP 8.2
================

最低 PHP 版本要求已更新为 **PHP 8.2**。

若当前运行环境版本低于 PHP 8.2，请在升级 CodeIgniter 前先升级 PHP。

验证规则 ``regex_match`` 的占位符
=======================================

``regex_match`` 验证规则中的占位符现在必须使用双大括号。

如果此前使用的是单大括号，例如 ``regex_match[/^{placeholder}$/]``，请更新为：
``regex_match[/^{{placeholder}}$/]``。

此改动是为了避免与正则表达式中的量词（如 ``{1,3}``）产生歧义。

模型主键验证时机与异常
==================================================

``insertBatch()`` 和 ``updateBatch()`` 方法现在遵循模型设置，如 ``updateOnlyChanged`` 和 ``allowEmptyInserts``。此项变更确保了所有插入与更新操作处理逻辑的一致性。

主键值现在会在执行数据库查询前，在 ``insert()``/``insertBatch()`` （非自增模式）、``update()`` 和 ``delete()`` 中进行验证。

无效的主键值现在将抛出 ``InvalidArgumentException``，而非数据库层的 ``DatabaseException``。

如果代码中通过捕获 ``DatabaseException`` 来处理无效主键，请更新代码以同时处理 ``InvalidArgumentException``。

实体变更检测现为深度比较
===================================

``Entity::hasChanged()`` 和 ``Entity::syncOriginal()`` 现在会对数组和对象执行深度比较。

由于现在会检测嵌套变更，若此前依赖浅比较（基于引用）的行为，请检查实体的更新流程和相关测试。

此外，当 ``$recursive`` 为 ``true`` 时，``Entity::toRawArray()`` 现在会递归转换实体数组。

加密处理程序密钥状态
============================

当通过 ``encrypt()``/``decrypt()`` 的 ``$params`` 参数传递密钥时，``OpenSSLHandler`` 和 ``SodiumHandler`` 不再改变处理程序内部的密钥状态。

如果代码依赖于“仅传递一次密钥并在后续隐式复用”，请改为在 ``Config\\Encryption`` 中进行显式密钥配置（或在创建加密服务时传递自定义配置）。

接口变更
=================

部分接口已发生变更。实现框架接口的类应更新其 API 以反映这些变化。

详情请参阅 :ref:`变更记录 <v470-interface-changes>`。

方法签名变更
========================

部分方法签名已发生变更。继承框架类的子类应更新其方法签名以保持 LSP（里氏替换原则）兼容性。

详情请参阅 :ref:`变更记录 <v470-method-signature-changes>`。

属性签名变更
==========================

部分属性的类型签名已更改（例如可为空的 ``Entity::$dataCaster``）。如果继承了这些类，请相应地更新代码。

详情请参阅 :ref:`变更记录 <v470-property-signature-changes>`。

移除已弃用项
========================

已移除部分弃用项。如果应用仍在调用或继承这些 API，请在升级前更新代码。

详情请参阅 :ref:`变更记录 <v470-removed-deprecated-items>`。

*************
项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

.. note:: 目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
    `在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件发生了较大变更（包括弃用或视觉调整），建议将更新后的版本与应用进行合并：

配置
------

- app/Config/Migrations.php
    - 添加了 ``Config\Migrations::$lock``，默认值为 ``false``。

此版本新增了以下文件：

- app/Config/Hostnames.php
- app/Config/WorkerMode.php

所有变更
===========

以下列出了 **项目空间** 中所有已变更的文件；
其中很多只是注释或格式调整，不会影响运行时行为：

- app/Config/CURLRequest.php
- app/Config/Cache.php
- app/Config/ContentSecurityPolicy.php
- app/Config/Email.php
- app/Config/Encryption.php
- app/Config/Format.php
- app/Config/Hostnames.php
- app/Config/Images.php
- app/Config/Migrations.php
- app/Config/Optimize.php
- app/Config/Paths.php
- app/Config/Routing.php
- app/Config/Session.php
- app/Config/Toolbar.php
- app/Config/UserAgents.php
- app/Config/View.php
- app/Config/WorkerMode.php
- public/index.php
- spark
