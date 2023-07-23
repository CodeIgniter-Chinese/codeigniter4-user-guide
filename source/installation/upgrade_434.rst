##############################
从 4.3.3 升级到 4.3.4
##############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

重定向状态码
====================

- 由于一个错误修复,重定向的状态码可能会改变。参见
  :ref:`更新日志 v4.3.4 <v434-redirect-status-code>`,如果状态码不是
  你想要的,可以 :ref:`指定状态码 <response-redirect-status-code>`。

Forge::modifyColumn() 和 NULL
==============================

一个错误修复可能改变了 :ref:`$forge->modifyColumn() <db-forge-modifyColumn>`
的结果中的 NULL 约束。参见 :ref:`更新日志 <v434-forge-modifycolumn>`。
要设置所需的 NULL 约束,请更改 ``Forge::modifyColumn()`` 以始终
指定 ``null`` 键。

请注意,该错误可能在以前的版本中改变了意外的 NULL 约束。

项目文件
*************

**项目空间** 中的一些文件(根目录、app、public、writable)已更新。由于这些文件超出 **系统** 范围,如果不进行干预,它们将不会更改。

有一些第三方 CodeIgniter 模块可以协助合并项目空间的更改:`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容更改
===============

以下文件已作出重大更改(包括弃用或视觉调整),建议你将更新版本与应用程序合并:

配置
------

- app/Config/Generators.php

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

- app/Config/App.php
- app/Config/Generators.php
- composer.json
- public/index.php
