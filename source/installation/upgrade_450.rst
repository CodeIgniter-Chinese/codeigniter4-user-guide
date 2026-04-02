#############################
从 4.4.8 升级到 4.5.0
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

强制文件变更
**********************

index.php 和 spark
===================

以下文件有重要变更，**必须将更新后的版本合并到你的应用中**：

- ``public/index.php``
- ``spark``

.. important:: 如果不更新上述文件，在执行 ``composer update`` 后，CodeIgniter 将无法正常工作。

    例如，升级流程如下：

    .. code-block:: console

        composer update
        cp vendor/codeigniter4/framework/public/index.php public/index.php
        cp vendor/codeigniter4/framework/spark spark

破坏性变更
****************

.. _upgrade-450-lowercase-http-method-name:

HTTP 方法名改为大写
==========================

Request::getMethod()
--------------------

由于历史原因，``Request::getMethod()`` 默认返回小写的 HTTP 方法名。

但方法标记是区分大小写的，因为它可能用于访问区分大小写方法名的对象系统。按照约定，标准方法应使用全大写 US-ASCII 字母。
参见 https://www.rfc-editor.org/rfc/rfc9110#name-overview。

现在，``Request::getMethod()`` 中已弃用的 ``$upper`` 参数被移除，``getMethod()`` 会返回原始的 HTTP 方法名，即类似 "GET"、"POST" 这样的全大写形式。

如果需要小写方法名，可使用 PHP 的 ``strtolower()`` 函数::

    strtolower($request->getMethod())

应用代码中应使用大写的 HTTP 方法名。

app/Config/Filters.php
----------------------

需要将 **app/Config/Filters.php** 中 ``$methods`` 的键改为大写::

    public array $methods = [
        'POST' => ['invalidchars', 'csrf'],
        'GET'  => ['csrf'],
    ];

CURLRequest::request()
----------------------

在之前的版本中，可以向 ``request()`` 方法传递小写 HTTP 方法。但这是一个缺陷，现在已修复。

现在必须传入正确的大写 HTTP 方法名，例如 ``GET``、``POST``。否则会得到错误响应::

    $client   = \Config\Services::curlrequest();
    $response = $client->request('get', 'https://www.google.com/', [
        'http_errors' => false,
    ]);
    $response->getStatusCode(); // 旧版本：200
                                // 当前版本：405

.. _upgrade-450-nested-route-groups-and-options:

嵌套路由组与选项
===============================

已修复一个问题：外层 ``group()`` 传入的选项无法与内层 ``group()`` 的选项合并。

请检查并修正你的路由配置，因为这可能改变实际应用的选项值。

例如：

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

现在，``csrf`` 过滤器会同时作用于 ``admin`` 和 ``admin/users`` 路由。
在之前版本中，仅作用于 ``admin``。
另见 :ref:`routing-nesting-groups`。

.. _upgrade-450-filter-execution-order:

过滤器执行顺序
======================

控制器过滤器的执行顺序已发生变化。
如果需要保持旧版本的执行顺序，可将 ``Config\Feature::$oldFilterOrder`` 设为 ``true``。另见 :ref:`filter-execution-order`。

1. 过滤器组的执行顺序已调整。

    前置过滤器::

        旧：route → globals → methods → filters
        新：globals → methods → filters → route

    后置过滤器::

        旧：route → globals → filters
        新：route → filters → globals

2. *路由* 过滤器与 *过滤器* 过滤器中的后置过滤器执行顺序现在反转。

    例如以下配置：

    .. code-block:: php

        // 在 app/Config/Routes.php 中
        $routes->get('/', 'Home::index', ['filter' => ['route1', 'route2']]);

        // 在 app/Config/Filters.php 中
        public array $filters = [
            'filter1' => ['before' => '*', 'after' => '*'],
            'filter2' => ['before' => '*', 'after' => '*'],
        ];

    前置过滤器::

        旧：route1 → route2 → filter1 → filter2
        新：filter1 → filter2 → route1 → route2

    后置过滤器::

        旧：route1 → route2 → filter1 → filter2
        新：route2 → route1 → filter2 → filter1

.. _upgrade-450-api-response-trait:

API\\ResponseTrait 与字符串数据
==================================

在之前版本中，如果向 trait 方法传入字符串数据，即使响应格式判定为 JSON，框架仍会返回 HTML 响应。

现在传入字符串数据时，会正确返回 JSON 响应。另见 :ref:`api-response-trait-handling-response-types`。

如需保持旧行为，可在控制器中将 ``$stringAsHtml`` 属性设为 ``true``。

FileLocator::findQualifiedNameFromPath()
========================================

在之前版本中，``FileLocator::findQualifiedNameFromPath()`` 返回的完全限定类名以 ``\`` 开头。现在已移除该前导 ``\``。

如果代码依赖此前行为，需要进行修正。

BaseModel::getIdValue()
=======================

``BaseModel::getIdValue()`` 已改为 ``abstract``，并移除了默认实现。

如果继承了 ``BaseModel``，需要在子类中实现 ``getIdValue()`` 方法。

Factories
=========

:doc:`../concepts/factories` 已改为 final 类。
在极少数情况下，如果继承了 Factories，请停止继承并将代码复制到自己的 Factories 类中。

自动路由（传统版）
=====================

在之前版本中，即使未找到对应控制器，也可能执行控制器过滤器。

该问题已修复：当找不到控制器时，将抛出 ``PageNotFoundException``，且不会执行过滤器。

如果你的代码依赖该行为（例如希望不存在页面也执行全局过滤器），请使用新的 :ref:`v450-required-filters`。

方法签名变更
========================

部分方法签名已发生变更。继承这些类的子类应更新其 API。
详见 :ref:`变更记录 <v450-method-signature-changes>`。

移除弃用项目
========================

部分已弃用项已被移除。如果仍在使用或扩展这些内容，需要升级代码。
详见 :ref:`变更记录 <v450-removed-deprecated-items>`。

破坏性增强
*********************

.. _upgrade-450-404-override:

覆盖 404 状态码
========================

在之前版本中，:ref:`404-override` 默认返回状态码 ``200``。
现在默认返回 ``404``。

如需返回 ``200``，需要在控制器中设置::

    $routes->set404Override(static function () {
        response()->setStatusCode(200);

        echo view('my_errors/not_found.html');
    });

Validation::run() 签名
===========================

``Validation::run()`` 和 ``ValidationInterface::run()`` 的方法签名已变更。
参数 ``$dbGroup`` 上的 ``?string`` 类型声明已移除。

扩展类也应移除该类型声明，以避免违反 LSP。

项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件发生了较大变更（包括弃用或视觉调整），建议将更新后的版本与应用进行合并：

配置
------

app/Config/Filters.php
^^^^^^^^^^^^^^^^^^^^^^

新增了 Required 过滤器，因此有如下变更。另见
:ref:`变更记录 <v450-required-filters>`。

基类已变更::

    class Filters extends \CodeIgniter\Config\Filters

在 ``$aliases`` 属性中新增::

    public array $aliases = [
        // ...
        'forcehttps'    => \CodeIgniter\Filters\ForceHTTPS::class,
        'pagecache'     => \CodeIgniter\Filters\PageCache::class,
        'performance'   => \CodeIgniter\Filters\PerformanceMetrics::class,
    ];

新增属性 ``$required``，内容如下::

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

``$global['after']`` 中的 ``'toolbar'`` 已移除。

其他
^^^^^^

- app/Config/Boot/production.php
    - ``error_reporting()`` 的默认错误级别改为 ``E_ALL & ~E_DEPRECATED``。
- app/Config/Cors.php
    - 新增，用于处理 CORS 配置。
- app/Config/Database.php
    - ``$default`` 中 ``charset`` 默认值改为 ``utf8mb4``。
    - ``$default`` 中 ``DBCollat`` 默认值改为 ``utf8mb4_general_ci``。
    - ``$tests`` 中 ``DBCollat`` 默认值改为 ``''``。
- app/Config/Feature.php
    - 新增 ``Config\Feature::$oldFilterOrder``，参见
      :ref:`filter-execution-order`。
    - 新增 ``Config\Feature::$limitZeroAsAll``，参见
      :ref:`v450-query-builder-limit-0-behavior`。
    - 移除 ``Config\Feature::$multipleFilters``，因为
      :ref:`multiple-filters` 现已默认启用。
- app/Config/Kint.php
    - 不再继承 ``BaseConfig``，以避免启用
      :ref:`factories-config-caching` 时出错。
- app/Config/Optimize.php
    - 新增，用于优化配置。
- app/Config/Security.php
    - 在 ``production`` 环境中，``$redirect`` 属性改为 ``true``。

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
多数仅为注释或格式调整，不影响运行时：

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
