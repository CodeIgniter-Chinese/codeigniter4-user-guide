#############################
从 4.4.4 升级到 4.4.5
#############################

请参考与你的安装方法相对应的升级指南。

- :ref:`Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`Composer 安装将 CodeIgniter4 添加到现有项目的升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

*************
项目文件
*************

**项目空间** （根目录，app，public，writable）中的一些文件接收到更新。由于这些文件在 **system** 范围之外，它们不会在没有你的干预的情况下被更改。

有一些第三方 CodeIgniter 模块可用于帮助合并对项目空间的更改：`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

所有更改
===========

这是在 **项目空间** 中接收到更改的所有文件的列表；许多文件只是简单的注释或格式更改，对运行时没有影响：

- composer.json
