#############################
从 4.4.7 升级到 4.4.8
#############################

请参阅与你的安装方法对应的升级说明。

- :ref:`Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`Composer 安装 将 CodeIgniter4 添加到一个现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

*************
项目文件
*************

**项目空间**（root, app, public, writable）中的一些文件收到了更新。由于这些文件位于 **system** 范围之外，没有你的干预它们不会被更改。

有一些第三方的 CodeIgniter 模块可以帮助合并对项目空间的更改：`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

所有更改
===========

这是一个 **项目空间** 内所有收到更改的文件列表；
许多将只是简单的注释或格式更改，对运行时没有影响：

- app/.htaccess
- public/.htaccess
- writable/.htaccess
