##############################
从 4.3.3 升级到 4.3.4
##############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
****************

重定向状态码
====================

- 由于修复了一个 Bug，重定向的状态码可能发生变化。参见
  :ref:`变更记录 v4.3.4 <v434-redirect-status-code>`；如果状态码不符合你的预期，
  请参考 :ref:`指定状态码 <response-redirect-status-code>`。

Forge::modifyColumn() 与 NULL
==============================

一次 Bug 修复可能改变了
:ref:`$forge->modifyColumn() <db-forge-modifyColumn>` 结果中的 NULL 约束。参见
:ref:`变更记录<v434-forge-modifycolumn>`。
若要设置期望的 NULL 约束，请将 ``Forge::modifyColumn()`` 调整为始终显式指定 ``null`` 键。

请注意，该 Bug 可能已经在之前的版本中导致了非预期的 NULL 约束变更。

项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件发生了较大的改动（包括弃用项或界面调整），建议将更新后的版本合并到你的应用中：

配置
------

- app/Config/Generators.php

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
其中许多只是简单的注释或格式调整，对运行时没有影响：

- app/Config/App.php
- app/Config/Generators.php
- composer.json
- public/index.php
