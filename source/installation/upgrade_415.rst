#############################
从 4.1.4 升级到 4.1.5
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
================

BaseBuilder 和 Model 类中 set() 方法的变化
-------------------------------------------------------

已移除 ``set()`` 方法中 ``$value`` 参数的强制转换,以修复一个将数组和字符串参数传递给 ``set()`` 方法时会有不同处理的bug。如果你扩展了 ``BaseBuilder`` 类或 ``Model`` 类并修改了 ``set()`` 方法,则需要将其定义从
``public function set($key, ?string $value = '', ?bool $escape = null)`` 改为
``public function set($key, $value = '', ?bool $escape = null)``。

Session DatabaseHandler 的数据库表更改
-----------------------------------------------

为了优化,session 表中的以下列的类型发生了改变:

- MySQL
    - ``timestamp``
- PostgreSQL
    - ``ip_address``
    - ``timestamp``
    - ``data``

请更新 session 表的定义。参见 :doc:`/libraries/sessions` 查看新的定义。

此更改在 v4.1.2 中引入。但由于 `一个错误 <https://github.com/codeigniter4/CodeIgniter4/issues/4807>`_,
DatabaseHandler 驱动程序无法正常工作。

CSRF 保护
---------------

由于一个错误修复,当应用 CSRF 过滤器时,CSRF 保护现在不仅适用于 **POST** 请求,也适用于 **PUT/PATCH/DELETE** 请求。

当你使用 **PUT/PATCH/DELETE** 请求时,你需要发送 CSRF token。或者如果你不需要为它们提供 CSRF 保护,可以为这些请求移除 CSRF 过滤器。

如果你想要与先前版本相同的行为,可以在 **app/Config/Filters.php** 中像下面这样设置 CSRF 过滤器:

.. literalinclude:: upgrade_415/001.php

只有在你使用 ``form_open()`` 自动生成 CSRF 字段时才需要保护 **GET** 方法。

.. warning:: 一般来说,如果你使用 ``$methods`` 过滤器,你应该 :ref:`禁用自动路由(传统) <use-defined-routes-only>`,
    因为 :ref:`auto-routing-legacy` 允许任意 HTTP 方法访问一个控制器。
    用你不期望的方法访问控制器可能会绕过过滤器。

CURLRequest 头更改
-------------------------

在以前的版本中,如果你没有提供自己的 header, ``CURLRequest`` 会发送来自浏览器的请求 header。
这个错误已被修复。如果你的请求依赖 header,升级后你的请求可能会失败。
在这种情况下,需要手动添加必要的 header。
参见 :ref:`CURLRequest 类 <curlrequest-request-options-headers>` 了解如何添加。

Query Builder 更改
---------------------

为了优化和修复一个错误,主要用于测试的以下行为已经改变。

- 当你使用 ``insertBatch()`` 和 ``updateBatch()`` 时, ``$query->getOriginalQuery()`` 的返回值已改变。它不再返回带有绑定参数的查询,而是返回实际运行的查询。
- 如果 ``testMode`` 为 ``true``, ``insertBatch()`` 将返回 SQL 字符串数组,而不是受影响的行数。此更改是为了使返回的数据类型与 ``updateBatch()`` 方法相同。

重大增强
=====================

.. _upgrade-415-multiple-filters-for-a-route:

为路由设置多个过滤器
----------------------------

一个为路由设置多个过滤器的新功能。

.. important:: 默认情况下,此功能是禁用的。因为它破坏了向后兼容性。

如果要使用它,需要在 ``app/Config/Feature.php`` 中将 ``$multipleFilters`` 属性设置为 ``true``。
如果启用它:

- ``CodeIgniter\CodeIgniter::handleRequest()`` 使用
    - ``CodeIgniter\Filters\Filters::enableFilters()``,而不是 ``enableFilter()``
- ``CodeIgniter\CodeIgniter::tryToRouteIt()`` 使用
    - ``CodeIgniter\Router\Router::getFilters()``,而不是 ``getFilter()``
- ``CodeIgniter\Router\Router::handle()`` 使用
    - 属性 ``$filtersInfo``,而不是 ``$filterInfo``
    - ``CodeIgniter\Router\RouteCollection::getFiltersForRoute()``,而不是 ``getFilterForRoute()``

如果你扩展了上述类,则需要更改它们。

以下方法和属性已被废弃:

- ``CodeIgniter\Filters\Filters::enableFilter()``
- ``CodeIgniter\Router\Router::getFilter()``
- ``CodeIgniter\Router\RouteCollection::getFilterForRoute()``
- ``CodeIgniter\Router\RouteCollection`` 的属性 ``$filterInfo``

有关功能的信息,请参阅 :ref:`applying-filters`。

项目文件
=============

项目空间(根目录、app、public、writable)中的许多文件都已更新。由于这些文件超出系统范围,如果不进行干预,它们将不会更改。有一些第三方 CodeIgniter 模块可用于帮助合并项目空间中的更改: `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除非极少数情况进行错误修复,否则对项目空间文件的任何更改都不会破坏你的应用程序。在下一个主要版本之前,这里注明的所有更改都是可选的,强制性更改将在上面部分介绍。

内容更改
---------------

以下文件已作出重大更改(包括弃用或视觉调整),建议你将更新版本与应用程序合并:

* ``app/Config/CURLRequest.php``
* ``app/Config/Cache.php``
* ``app/Config/Feature.php``
* ``app/Config/Generators.php``
* ``app/Config/Publisher.php``
* ``app/Config/Security.php``
* ``app/Views/welcome_message.php``

所有更改
-----------

这是项目空间中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

* ``app/Config/CURLRequest.php``
* ``app/Config/Cache.php``
* ``app/Config/Feature.php``
* ``app/Config/Generators.php``
* ``app/Config/Kint.php``
* ``app/Config/Publisher.php``
* ``app/Config/Security.php``
* ``app/Views/welcome_message.php``
