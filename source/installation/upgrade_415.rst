#############################
从 4.1.4 升级到 4.1.5
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
================

BaseBuilder 与 Model 类中 set() 方法的变更
-------------------------------------------------------

为修复一个缺陷，已移除对 ``$value`` 参数的类型转换。该缺陷会导致向 ``set()`` 方法传入数组和字符串参数时，行为不一致。
如果你自行继承了 ``BaseBuilder`` 类或 ``Model`` 类，并且重写了 ``set()`` 方法，则需要将其定义从
``public function set($key, ?string $value = '', ?bool $escape = null)``
修改为
``public function set($key, $value = '', ?bool $escape = null)``。

Session DatabaseHandler 的数据库表变更
-----------------------------------------------

为优化性能，Session 表中以下字段的类型已发生变更。

- MySQL
    - ``timestamp``
- PostgreSQL
    - ``ip_address``
    - ``timestamp``
    - ``data``

请更新 Session 表的定义。新的定义请参见 :doc:`/libraries/sessions`。

该变更最早在 v4.1.2 中引入。但由于 `一个缺陷 <https://github.com/codeigniter4/CodeIgniter4/issues/4807>`_，
DatabaseHandler 驱动此前无法正常工作。

CSRF 防护
---------------

由于修复了一个缺陷，当应用 CSRF 过滤器时，CSRF 防护现在不仅适用于 **POST**，
也适用于 **PUT/PATCH/DELETE** 请求。

当使用 **PUT/PATCH/DELETE** 请求时，需要发送 CSRF Token。
如果这些请求不需要 CSRF 防护，则应为其移除 CSRF 过滤器。

如果希望保持与旧版本相同的行为，请在 **app/Config/Filters.php** 中按如下方式设置 CSRF 过滤器：

.. literalinclude:: upgrade_415/001.php

仅在使用 ``form_open()`` 自动生成 CSRF 字段时，才需要保护 **GET** 方法。

.. warning:: 一般来说，如果你使用 ``$methods`` 过滤器，应当 :ref:`禁用自动路由（传统版） <use-defined-routes-only>`，
    因为 :ref:`auto-routing-legacy` 允许使用任何 HTTP 方法访问控制器。
    使用非预期的方法访问控制器，可能会绕过过滤器。

CURLRequest 标头变更
-------------------------

在旧版本中，如果未提供自定义标头，``CURLRequest`` 会发送来自浏览器的请求标头。
该问题现已修复。如果你的请求依赖这些标头，升级后请求可能会失败。

在这种情况下，请手动添加所需的标头。
添加方法请参见 :ref:`CURLRequest 类 <curlrequest-request-options-headers>`。

查询构建器变更
---------------------

出于优化和缺陷修复的目的，以下行为（主要用于测试）已发生变更。

- 当使用 ``insertBatch()`` 和 ``updateBatch()`` 时，``$query->getOriginalQuery()`` 的返回值已改变。
  现在它不再返回包含绑定参数的查询，而是返回实际执行的查询。
- 当 ``testMode`` 为 ``true`` 时，``insertBatch()`` 将返回一个 SQL 字符串数组，而不是受影响的行数。
  此变更用于确保返回的数据类型与 ``updateBatch()`` 方法一致。

破坏性增强
=====================

.. _upgrade-415-multiple-filters-for-a-route:

为路由设置多个过滤器
----------------------------

新增了为单个路由设置多个过滤器的功能。

.. important:: 该功能默认被禁用，因为它会破坏向后兼容性。

如果需要使用此功能，必须在 ``app/Config/Feature.php`` 中将属性 ``$multipleFilters`` 设置为 ``true``。
启用后：

- ``CodeIgniter\CodeIgniter::handleRequest()`` 使用
    - ``CodeIgniter\Filters\Filters::enableFilters()``，而不是 ``enableFilter()``
- ``CodeIgniter\CodeIgniter::tryToRouteIt()`` 使用
    - ``CodeIgniter\Router\Router::getFilters()``，而不是 ``getFilter()``
- ``CodeIgniter\Router\Router::handle()`` 使用
    - 属性 ``$filtersInfo``，而不是 ``$filterInfo``
    - ``CodeIgniter\Router\RouteCollection::getFiltersForRoute()``，而不是 ``getFilterForRoute()``

如果你继承了上述类，则需要进行相应修改。

以下方法和属性已被弃用：

- ``CodeIgniter\Filters\Filters::enableFilter()``
- ``CodeIgniter\Router\Router::getFilter()``
- ``CodeIgniter\Router\RouteCollection::getFilterForRoute()``
- ``CodeIgniter\Router\RouteCollection`` 的属性 ``$filterInfo``

相关功能请参见 :ref:`applying-filters`。

项目文件
=============

项目空间（根目录、app、public、writable）中的大量文件已更新。
由于这些文件位于 system 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除极少数用于缺陷修复的情况外，对项目空间文件的修改不会破坏你的应用。
    此处列出的所有变更在下一个主版本发布前都是可选的，
    任何强制性变更都会在上述章节中说明。

内容变更
---------------

以下文件发生了较大的改动（包括弃用项或界面调整），建议将更新后的版本合并到你的应用中：

* ``app/Config/CURLRequest.php``
* ``app/Config/Cache.php``
* ``app/Config/Feature.php``
* ``app/Config/Generators.php``
* ``app/Config/Publisher.php``
* ``app/Config/Security.php``
* ``app/Views/welcome_message.php``

所有变更
-----------

以下是项目空间中所有发生变更的文件列表；
其中许多仅为注释或格式调整，不会影响运行时行为：

* ``app/Config/CURLRequest.php``
* ``app/Config/Cache.php``
* ``app/Config/Feature.php``
* ``app/Config/Generators.php``
* ``app/Config/Kint.php``
* ``app/Config/Publisher.php``
* ``app/Config/Security.php``
* ``app/Views/welcome_message.php``
