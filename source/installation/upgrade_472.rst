#############################
从 4.7.1 升级到 4.7.2
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

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

- 此版本未更改任何配置文件。

所有变更
===========

以下列出了 **项目空间** 中所有已变更的文件；
其中很多只是注释或格式调整，不会影响运行时行为：

- 此版本未更改任何项目文件。
