#############################
从 4.4.8 升级到 4.5.0
#############################

请参阅与你的安装方法对应的升级说明。

- :ref:`Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`Composer 安装 将 CodeIgniter4 添加到一个现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

**********************
强制文件更改
**********************

index.php 和 spark
===================

以下文件进行了重大更改，
**你必须将更新的版本** 合并到你的应用程序中：

- ``public/index.php``
- ``spark``

.. important:: 如果不更新上述文件，在运行 ``composer update`` 之后 CodeIgniter 将无法正常工作。

    升级步骤例如如下：

    .. code-block:: console

        composer update
        cp vendor/codeigniter4/framework/public/index.php public/index.php
        cp vendor/codeigniter4/framework/spark spark

****************
重大变更
****************

.. _upgrade-450-lowercase-http-method-name:

小写 HTTP 方法名
==========================

Request::getMethod()
--------------------

由于历史原因，``Request::getMethod()`` 默认返回小写的 HTTP 方法名。

但是方法标记是区分大小写的，因为它可能用作区分大小写的方法名的对象系统的网关。按照惯例，标准化的方法都定义为全大写的 US-ASCII 字母。详情见 https://www.rfc-editor.org/rfc/rfc9110#name-overview。

现在，``Request::getMethod()`` 中已弃用的 ``$upper`` 参数已被移除，而 ``getMethod()`` 返回的是原样的 HTTP 方法名。即，大写形式如 "GET", "POST" 等等。

如果你需要小写的 HTTP 方法名，请使用 PHP 的 ``strtolower()`` 函数::

    strtolower($request->getMethod())

并且在你的应用代码中应使用大写的 HTTP 方法名。

app/Config/Filters.php
----------------------

你应将 **app/Config/Filters.php** 中 ``$methods`` 的键更新为大写::

    public array $methods = [
        'POST' => ['invalidchars', 'csrf'],
        'GET'  => ['csrf'],
    ];

CURLRequest::request()
----------------------

在之前的版本中，你可以将小写的 HTTP 方法传递给 ``request()`` 方法。这个错误已被修复。

现在，你必须传递正确的 HTTP 方法名，如 ``GET``, ``POST``。否则你会得到错误响应::

    $client   = \Config\Services::curlrequest();
    $response = $client->request('get', 'https://www.google.com/', [
        'http_errors' => false,
    ]);
    $response->getStatusCode(); // 之前版本：200
                                // 现在版本：405

.. _upgrade-450-nested-route-groups-and-options:

嵌套路由组和选项
===============================

阻止传递给外部 ``group()`` 的选项与内部 ``group()`` 的选项合并的错误已被修复。

请检查并更正你的路由配置，因为这可能会更改应用的选项值。

例如，

.. code-block:: php

    $routes->group('admin', ['filter' => 'csrf'], static function ($routes) {
        $routes->get('/', static function () {
            // ...
        });

        $routes->group('users', ['namespace' => 'Users'], static function ($routes) {
            $routes->get('/', static function () {
                // ...
            });
        });
    });

现在，``csrf`` 过滤器将为 ``admin`` 和 ``admin/users`` 路由执行。
在之前的版本中，它仅为 ``admin`` 路由执行。
另请参阅 :ref:`routing-nesting-groups`。

.. _upgrade-450-filter-execution-order:

过滤器执行顺序
======================

控制器过滤器执行顺序已更改。
如果你希望维持之前版本的执行顺序，请在 ``Config\Feature::$oldFilterOrder`` 中设置 ``true``。另请参阅 :ref:`filter-execution-order`。

1. 过滤器组的执行顺序已更改。

    前置过滤器::

        之前: route → globals → methods → filters
        现在: globals → methods → filters → route

    后置过滤器::

        之前: route → globals → filters
        现在: route → filters → globals

2. 在 *Route* 过滤器和 *Filters* 过滤器中的后置过滤器执行顺序现在是反向的。

    与以下配置有关：

    .. code-block:: php

        // 在 app/Config/Routes.php 中
        $routes->get('/', 'Home::index', ['filter' => ['route1', 'route2']]);

        // 在 app/Config/Filters.php 中
        public array $filters = [
            'filter1' => ['before' => '*', 'after' => '*'],
            'filter2' => ['before' => '*', 'after' => '*'],
        ];

    前置过滤器::

        之前: route1 → route2 → filter1 → filter2
        现在: filter1 → filter2 → route1 → route2

    后置过滤器::

        之前: route1 → route2 → filter1 → filter2
        现在: route2 → route1 → filter2 → filter1

.. _upgrade-450-api-response-trait:

API\\ResponseTrait 和字符串数据
==================================

在以前的版本中，如果你将字符串数据传递给 trait 方法，即使响应格式被确定为 JSON，框架还是会返回 HTML 响应。

现在，如果你传递字符串数据，它将正确返回 JSON 响应。另请参阅 :ref:`api-response-trait-handling-response-types`。

如果你希望保持之前版本的行为，请在控制器中将 ``$stringAsHtml`` 属性设置为 ``true``。

FileLocator::findQualifiedNameFromPath()
========================================

在以前的版本中，``FileLocator::findQualifiedNameFromPath()`` 返回带有前导 ``\`` 的完全限定类名。现在，前导 ``\`` 已被移除。

如果你的代码依赖于带前导 ``\`` 的结果，请修正。

BaseModel::getIdValue()
=======================

``BaseModel::getIdValue()`` 已更改为 ``abstract``，实现已被移除。

如果你扩展了 ``BaseModel``，请在子类中实现 ``getIdValue()`` 方法。

Factories
=========

:doc:`../concepts/factories` 已更改为最终类。
在极不可能的情况下，如果你继承了 Factories，请停止继承并将代码复制到你的 Factories 类中。

自动路由（传统）
=====================

在以前的版本中，即使未找到相应的控制器，也可能会执行控制器过滤器。

此错误已被修复，现在如果未找到控制器，将抛出 ``PageNotFoundException`` 且不会执行过滤器。

如果你的代码依赖于此错误，例如你期望即使在不存在的页面上也会执行全局过滤器，请使用新的 :ref:`v450-required-filters`。

方法签名更改
========================

一些方法签名已更改。扩展它们的类应更新其 API 以反映这些更改。详情请参阅 :ref:`ChangeLog <v450-method-signature-changes>`。

移除的弃用项
========================

一些弃用项已被移除。如果你仍在使用这些项或扩展这些类，请升级你的代码。详情请参阅 :ref:`ChangeLog <v450-removed-deprecated-items>`。

打破性增强
*********************

.. _upgrade-450-404-override:

404 覆盖状态码
========================

在以前的版本中，:ref:`404-override` 默认返回状态码为 ``200`` 的响应。现在它默认返回 ``404``。

如果你需要 ``200``，请在控制器中设置::

    $routes->set404Override(static function () {
        response()->setStatusCode(200);

        echo view('my_errors/not_found.html');
    });

Validation::run() 签名
===========================

``Validation::run()`` 和 ``ValidationInterface::run()`` 的方法签名已更改。``$dbGroup`` 参数的 ``?string`` 类型提示已被移除。扩展的类也应移除该参数以不破坏 LSP。

*************
项目文件
*************

**项目空间**（root, app, public, writable）中的一些文件收到了更新。由于这些文件位于 **system** 范围之外，没有你的干预它们不会被更改。

有一些第三方的 CodeIgniter 模块可以帮助合并对项目空间的更改：`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件进行了重要更改（包括弃用或视觉调整），建议将更新的版本与应用程序合并：

配置
------

app/Config/Filters.php
^^^^^^^^^^^^^^^^^^^^^^

已添加必需过滤器，因此做了以下更改。另请参阅 :ref:`ChangeLog <v450-required-filters>`。

基类已更改::

    class Filters extends \CodeIgniter\Config\Filters

在 ``$aliases`` 属性中添加了以下项目::

    public array $aliases = [
        // ...
        'forcehttps'    => \CodeIgniter\Filters\ForceHTTPS::class,
        'pagecache'     => \CodeIgniter\Filters\PageCache::class,
        'performance'   => \CodeIgniter\Filters\PerformanceMetrics::class,
    ];

添加了一个新属性 ``$required``，并设置如下::

    public array $required = [
        'before' => [
            'forcehttps', // 强制全局安全请求
            'pagecache',  // 网页缓存
        ],
        'after' => [
            'pagecache',   // 网页缓存
            'performance', // 性能指标
            'toolbar',     // 调试工具栏
        ],
    ];

``$global['after']`` 中的 ``'toolbar'`` 被移除。

其他
^^^^^^

- app/Config/Boot/production.php
    - ``error_reporting()`` 的默认错误级别已更改为 ``E_ALL & ~E_DEPRECATED``。
- app/Config/Cors.php
    - 添加了处理 CORS 配置。
- app/Config/Database.php
    - ``$default`` 中 ``charset`` 的默认值已更改为 ``utf8mb4``。
    - ``$default`` 中 ``DBCollat`` 的默认值已更改为 ``utf8mb4_general_ci``。
    - ``$tests`` 中 ``DBCollat`` 的默认值已更改为 ``''``。
- app/Config/Feature.php
    - 添加了 ``Config\Feature::$oldFilterOrder``。另请参阅 :ref:`filter-execution-order`。
    - 添加了 ``Config\Feature::$limitZeroAsAll``。另请参阅 :ref:`v450-query-builder-limit-0-behavior`。
    - 移除了 ``Config\Feature::$multipleFilters``，因为现在 :ref:`multiple-filters` 已经默认启用。
- app/Config/Kint.php
    - 不再继承 ``BaseConfig``，因为启用 :ref:`factories-config-caching` 可能会导致错误。
- app/Config/Optimize.php
    - 添加了处理优化配置。
- app/Config/Security.php
    - 在 ``production`` 环境中将 ``$redirect`` 属性更改为 ``true``。

所有更改
===========

这是一个 **项目空间** 内所有收到更改的文件列表；
许多将只是简单的注释或格式更改，对运行时没有影响：

- app/Config/Autoload.php
- app/Config/Boot/production.php
- app/Config/Cache.php
- app/Config/Cors.php
- app/Config/Database.php
- app/Config/Feature.php
- app/Config/Filters.php
- app/Config/Generators.php
- app/Config/Kint.php
- app/Config/Optimize.php
- app/Config/Routing.php
- app/Config/Security.php
- app/Config/Session.php
- app/Views/errors/cli/error_exception.php
- app/Views/errors/html/error_exception.php
- app/Views/welcome_message.php
- composer.json
- env
- phpunit.xml.dist
- preload.php
- public/index.php
- spark
