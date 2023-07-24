#############################
从 4.2.1 升级到 4.2.2
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

网页缓存错误修复
========================

- :doc:`../general/caching` 现在会在 :ref:`after-filters` 执行后缓存 Response 数据。
- 例如,如果你启用 :ref:`secureheaders`,那么从缓存中获取页面时现在也会发送 Response 头。

.. important:: 如果你编写了 **基于此错误的代码**,假定“after”过滤器中的 Response 更改不会被缓存,那么 **敏感信息可能会被缓存并泄露**。如果是这种情况,请更改代码以禁用对页面的缓存。

其它
======

- ``Forge::createTable()`` 方法不再执行 ``CREATE TABLE IF NOT EXISTS``。当 ``$ifNotExists`` 为 true 时,如果在 ``$db->tableExists($table)`` 中未找到表,则执行 ``CREATE TABLE``。
- ``Forge::_createTable()`` 的第二个参数 ``$ifNotExists`` 已被废弃。它不再被使用,将在未来版本中移除。
- 当使用 :php:func:`random_string()` 的第一个参数为 ``'crypto'`` 时,现在如果把第二个参数 ``$len`` 设置为奇数,会抛出 ``InvalidArgumentException``。请将参数改为偶数。

重大增强
*********************

项目文件
*************

**项目空间** 中的许多文件(根目录、app、public、writable)都已更新。由于这些文件超出 **系统** 范围,如果不进行干预,它们将不会更改。有一些第三方 CodeIgniter 模块可以协助合并项目空间的更改: `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除非极少数情况进行错误修复,否则对项目空间文件的任何更改都不会破坏你的应用程序。在下一个主要版本之前,这里注明的所有更改都是可选的,强制性更改将在上面部分介绍。

内容更改
===============

* app/Views/errors/html/error_404.php
* app/Views/welcome_message.php
* public/index.php
* spark

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

* app/Config/App.php
* app/Config/Constants.php
* app/Config/Logger.php
* app/Config/Paths.php
* app/Views/errors/html/error_404.php
* app/Views/welcome_message.php
