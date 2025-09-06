#############################
从 4.6.1 升级到 4.6.2
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`Composer 安装 App Starter 升级指南 <app-starter-upgrading>`
- :ref:`Composer 安装 将 CodeIgniter4 添加到现有项目 升级指南 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级指南 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

*************
项目文件
*************

**项目空间** （root、app、public、writable）中的一些文件接收了更新。由于这些文件位于 **system** 范围之外，它们不会在没有你的干预的情况下被更改。

.. note:: 有一些第三方 CodeIgniter 模块可用于协助合并项目空间的更改：
    `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容更改
===============

以下文件有重要更改（包括弃用或视觉调整），建议你将更新的版本与你的应用程序合并：

Config
------

- app/Config/Autoload.php
- app/Config/Cache.php
- app/Config/Cookie.php
- app/Config/DocTypes.php
- app/Config/Logger.php
- app/Config/Mimes.php
- app/Config/Modules.php
- app/Config/Optimize.php
- app/Config/Paths.php

所有更改
===========

这是 **项目空间** 中所有发生变更的文件列表；许多将是简单的注释或格式化，对运行时没有影响：

- app/Config/Autoload.php
- app/Config/Cache.php
- app/Config/Cookie.php
- app/Config/DocTypes.php
- app/Config/Logger.php
- app/Config/Mimes.php
- app/Config/Modules.php
- app/Config/Optimize.php
- app/Config/Paths.php
- app/Views/errors/html/debug.css
- app/Views/errors/html/error_exception.php
- preload.php
- public/index.php
- spark