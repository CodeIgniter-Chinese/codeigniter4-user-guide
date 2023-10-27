#############################
从 4.4.1 升级到 4.4.2
#############################

请参考与您的安装方法相对应的升级说明。

- :ref:`使用 Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`使用 Composer 安装将 CodeIgniter4 添加到现有项目并进行升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

项目文件
*************

**项目空间**（根目录、app、public、writable）中的一些文件已经更新。由于这些文件位于 **system** 范围之外，如果没有您的干预，它们将不会更改。

有一些第三方的 CodeIgniter 模块可用于帮助合并项目空间的更改：`在 Packagist 上查看 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

所有更改
===========

这是 **项目空间** 中所有已更改的文件列表；其中许多只是注释或格式化的简单更改，对运行时没有影响：

- app/Config/Migrations.php
- app/Config/View.php
- composer.json
