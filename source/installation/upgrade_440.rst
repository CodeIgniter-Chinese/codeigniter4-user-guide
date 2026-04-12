##############################
从 4.3.8 升级到 4.4.0
##############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

安全
********

使用 $this->validate()
============================

在控制器中的 :ref:`$this->validate() <controller-validate>` 曾存在一个已知的潜在漏洞，可能被绕过验证。
该攻击可能导致开发者将未验证的空数据误认为已通过验证，从而继续处理。

为确保获取的是已验证的数据，新增了
:ref:`Validation::getValidated() <validation-getting-validated-data>` 方法。

因此，在控制器中使用 ``$this->validate()`` 时，应使用新的
``Validation::getValidated()`` 方法来获取验证后的数据。

.. literalinclude:: ../libraries/validation/045.php
   :lines: 2-

破坏性变更
****************

.. _upgrade-440-uri-setsegment:

URI::setSegment() 变更
========================

由于一个缺陷，在之前的版本中，当指定最后一个段为 ``+2`` 时不会抛出异常。
该缺陷已被修复。

如果你的代码依赖该行为，需要修正段编号。

.. literalinclude:: upgrade_440/002.php
   :lines: 2-

站点 URI 变更
================

- 由于当前 URI 判定机制的重构，框架返回的站点 URI 或 URI 路径可能与之前版本略有不同，这可能导致测试代码失败。如有失败，请更新断言。
- 当 baseURL 包含子目录，并且通过 ``URI::getPath()`` 获取当前 URI 相对于 baseURL 的路径时，应改用新的 ``SiteURI::getRoutePath()`` 方法。

详见 :ref:`v440-site-uri-changes`。

扩展 Exceptions 时
==========================

如果扩展了 ``CodeIgniter\Debug\Exceptions``，且未重写 ``exceptionHandler()`` 方法，
那么在 **app/Config/Exceptions.php** 中定义新的 ``Config\Exceptions::handler()`` 方法后，
将会执行所指定的异常处理器。

原有重写的代码将不再执行，因此需要通过定义自定义异常处理器来进行必要的调整。

详见 :ref:`custom-exception-handlers`。

自动路由（改进版）与 translateURIDashes
==============================================

当使用自动路由（改进版）且 ``$translateURIDashes`` 为 true
（``$routes->setTranslateURIDashes(true)``）时，在之前的版本中由于缺陷，
一个控制器方法会对应两个 URI：一个使用短横线（如 **foo-bar**），另一个使用下划线（如 **foo_bar**）。

该缺陷已修复，现在带下划线的 URI（**foo_bar**）将无法访问。

如果存在指向下划线 URI（**foo_bar**）的链接，请更新为使用短横线（**foo-bar**）。

向 Factories 传递带命名空间的类名
==================================================

向 Factories 传递带命名空间的类名时，其行为已发生变化。
详见 :ref:`变更记录 <v440-factories>`。

如果存在如下代码 ``model(\Myth\Auth\Models\UserModel::class)``
或 ``model('Myth\Auth\Models\UserModel')`` （可能出现在第三方包中），
且期望加载 ``App\Models\UserModel``，则需要在首次加载该类之前定义要加载的类名::

    Factories::define('models', 'Myth\Auth\Models\UserModel', 'App\Models\UserModel');

详见 :ref:`factories-defining-classname-to-be-loaded`。

接口变更
=================

部分接口已发生变更。实现这些接口的类需要更新其 API 以匹配新的定义。
详见 :ref:`v440-interface-changes`。

方法签名变更
========================

部分方法签名已发生变更。继承这些类的类需要更新其 API 以匹配新的定义。
详见 :ref:`v440-method-signature-changes`。

此外，一些构造函数以及 ``Services::security()`` 的参数类型也已变更。
如果调用时传入了参数，需要相应调整参数值。
详见 :ref:`v440-parameter-type-changes`。

RouteCollection::$routes
========================

受保护属性 ``$routes`` 的数组结构已为提升性能而修改。

如果扩展了 ``RouteCollection`` 并使用了 ``$routes``，需要更新代码以匹配新的数组结构。

必要的文件更改
**********************

index.php 和 spark
===================

以下文件有重大变更，**必须将更新后的版本合并到你的应用中**：

- ``public/index.php`` （另见 :ref:`v440-codeigniter-and-exit`）
- ``spark``

.. important:: 如果未更新上述文件，在执行 ``composer update`` 后，CodeIgniter 将无法正常运行。

    升级步骤示例如下：

    .. code-block:: console

        composer update
        cp vendor/codeigniter4/framework/public/index.php public/index.php
        cp vendor/codeigniter4/framework/spark spark

配置文件
============

app/Config/App.php
------------------

属性 ``$proxyIPs`` 必须为数组。如果不使用代理服务器，应设置为
``public array $proxyIPs = [];``。

.. _upgrade-440-config-routing:

app/Config/Routing.php
----------------------

为简化路由系统，进行了如下调整：

- 新增 **app/Config/Routing.php** 文件，用于存放原本位于 Routes 文件中的配置。
- **app/Config/Routes.php** 已简化，仅保留路由定义，不再包含配置和冗余说明。
- 不再自动加载按环境划分的 routes 文件。

需要执行以下操作：

1. 将新框架中的 **app/Config/Routing.php** 复制到你的 **app/Config** 目录，并进行配置。
2. 删除 **app/Config/Routes.php** 中不再需要的所有配置项。
3. 如果使用按环境划分的 routes 文件，将其添加到 **app/Config/Routing.php** 中的 ``$routeFiles`` 属性中。

app/Config/Toolbar.php
----------------------

需要为 :ref:`debug-toolbar-hot-reload` 添加新的属性 ``$watchedDirectories`` 和 ``$watchedExtensions``::

    --- a/app/Config/Toolbar.php
    +++ b/app/Config/Toolbar.php
    @@ -88,4 +88,31 @@ class Toolbar extends BaseConfig
          * `$maxQueries` defines the maximum amount of queries that will be stored.
          */
         public int $maxQueries = 100;
    +
    +    /**
    +     * --------------------------------------------------------------------------
    +     * Watched Directories
    +     * --------------------------------------------------------------------------
    +     *
    +     * Contains an array of directories that will be watched for changes and
    +     * used to determine if the hot-reload feature should reload the page or not.
    +     * We restrict the values to keep performance as high as possible.
    +     *
    +     * NOTE: The ROOTPATH will be prepended to all values.
    +     */
    +    public array $watchedDirectories = [
    +        'app',
    +    ];
    +
    +    /**
    +     * --------------------------------------------------------------------------
    +     * Watched File Extensions
    +     * --------------------------------------------------------------------------
    +     *
    +     * Contains an array of file extensions that will be watched for changes and
    +     * used to determine if the hot-reload feature should reload the page or not.
    +     */
    +    public array $watchedExtensions = [
    +        'php', 'css', 'js', 'html', 'svg', 'json', 'env',
    +    ];
     }

app/Config/Events.php
---------------------

需要添加如下代码，为 :ref:`debug-toolbar-hot-reload` 注册路由::

    --- a/app/Config/Events.php
    +++ b/app/Config/Events.php
    @@ -4,6 +4,7 @@ namespace Config;

     use CodeIgniter\Events\Events;
     use CodeIgniter\Exceptions\FrameworkException;
    +use CodeIgniter\HotReloader\HotReloader;

     /*
      * --------------------------------------------------------------------
    @@ -44,5 +45,11 @@ Events::on('pre_system', static function () {
         if (CI_DEBUG && ! is_cli()) {
             Events::on('DBQuery', 'CodeIgniter\Debug\Toolbar\Collectors\Database::collect');
             Services::toolbar()->respond();
    +        // Hot Reload route - for framework use on the hot reloader.
    +        if (ENVIRONMENT === 'development') {
    +            Services::routes()->get('__hot-reload', static function () {
    +                (new HotReloader())->run();
    +            });
    +        }
         }
     });

app/Config/Cookie.php
---------------------

**app/Config/App.php** 中的 Cookie 配置项已不再使用。

1. 将新框架中的 **app/Config/Cookie.php** 复制到你的 **app/Config** 目录，并进行配置。
2. 删除 **app/Config/App.php** 中（从 ``$cookiePrefix`` 到 ``$cookieSameSite``）的属性。

app/Config/Security.php
-----------------------

**app/Config/App.php** 中的 CSRF 配置项已不再使用。

1. 将新框架中的 **app/Config/Security.php** 复制到你的 **app/Config** 目录，并进行配置。
2. 删除 **app/Config/App.php** 中（从 ``$CSRFTokenName`` 到 ``$CSRFSameSite``）的属性。

app/Config/Session.php
----------------------

**app/Config/App.php** 中的 Session 配置项已不再使用。

1. 将新框架中的 **app/Config/Session.php** 复制到你的 **app/Config** 目录，并进行配置。
2. 删除 **app/Config/App.php** 中（从 ``$sessionDriver`` 到 ``$sessionDBGroup``）的属性。

重大改进
*********************

- **Routing：** ``RouteCollection::__construct()`` 的方法签名已变更，新增第三个参数 ``Routing $routing``。扩展类也必须添加该参数，以避免违反 LSP。
- **Validation：** ``Validation::check()`` 的方法签名已变更，移除了 ``$rule`` 参数上的 ``string`` 类型提示。扩展类也应移除该类型提示，以避免违反 LSP。

项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件发生了较大的改动（包括弃用项或界面调整），建议将更新后的版本合并到你的应用中：

配置
------

- app/Config/CURLRequest.php
    - :ref:`$shareOptions <curlrequest-sharing-options>` 的默认值已更改为 ``false``。
- app/Config/Exceptions.php
    - 新增 ``handler()`` 方法，用于定义自定义异常处理器。
      详见 :ref:`custom-exception-handlers`。

所有变更
===========

以下列出了 **项目空间** 中所有发生变更的文件；
其中多数只是注释或格式调整，不会影响运行时行为：

- app/Config/App.php
- app/Config/CURLRequest.php
- app/Config/Cookie.php
- app/Config/Database.php
- app/Config/Events.php
- app/Config/Exceptions.php
- app/Config/Filters.php
- app/Config/Routes.php
- app/Config/Routing.php
- app/Config/Toolbar.php
- public/index.php
- spark
