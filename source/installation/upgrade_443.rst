#############################
从 4.4.2 升级到 4.4.3
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`使用 Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`使用 Composer 将 CodeIgniter4 添加到现有项目中升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

必要的文件更改
**********************

error_exception.php
===================

以下文件已经发生了重大更改，**你必须将更新的版本与你的应用程序合并**：

- app/Views/errors/html/error_exception.php

项目文件
*************

**项目空间** (根目录、app、public、writable) 中的一些文件已经更新。由于这些文件位于 **system** 范围之外，因此在没有你的干预下不会更改。

有一些第三方 CodeIgniter 模块可用于帮助合并对项目空间的更改：`在 Packagist 上查看 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

所有更改
===========

这是 **项目空间** 中所有已经更改的文件的列表；其中许多只是注释或格式化的简单更改，对运行时没有影响：

- app/Config/Boot/development.php
- app/Config/Boot/production.php
- app/Config/Boot/testing.php
- app/Config/Filters.php
- app/Views/errors/html/error_404.php
- app/Views/errors/html/error_exception.php
