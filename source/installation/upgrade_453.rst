#############################
从 4.5.2 升级到 4.5.3
#############################

请参考与你的安装方式对应的升级说明。

- :ref:`Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`Composer 安装 将 CodeIgniter4 添加到一个现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

*************
项目文件
*************

**项目空间** （root, app, public, writable）中的一些文件收到了更新。由于这些文件位于 **system** 范围之外，没有你的干预它们不会被更改。

.. note:: 有一些第三方的 CodeIgniter 模块可以帮助合并项目空间的变化：
    `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容更改
===============

以下文件收到了显著更改（包括弃用或视觉调整），建议你将更新版本与你的应用程序合并：

配置
------

- composer.json

所有更改
===========

以下是 **项目空间** 中所有收到更改的文件列表；许多更改将是简单的注释或格式调整，不会影响运行时：

- composer.json
