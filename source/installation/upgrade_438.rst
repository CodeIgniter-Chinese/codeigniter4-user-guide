#############################
从 4.3.7 升级到 4.3.8
#############################

请参考与您的安装方法相对应的升级说明。

- :ref:`使用 Composer 安装的应用程序启动器升级 <app-starter-upgrading>`
- :ref:`使用 Composer 安装的将 CodeIgniter4 添加到现有项目中升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

项目文件
*************

**项目空间**（根目录、app、public、writable）中的一些文件已经更新。由于这些文件位于 **system** 范围之外，因此不会在没有您干预的情况下进行更改。

有一些第三方 CodeIgniter 模块可用于帮助合并对项目空间的更改：`在 Packagist 上查看 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容更改
===============

以下文件已经进行了重大更改（包括弃用或视觉调整），建议您将更新后的版本与您的应用程序合并：

配置
------

- composer.json

所有更改
===========

这是 **项目空间** 中所有已更改的文件的列表；其中许多只是注释或格式变化，对运行时没有影响：

- composer.json
