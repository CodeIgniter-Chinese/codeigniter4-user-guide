##############################
从 4.3.8 升级到 4.4.0
##############################

请参考与你的安装方法对应的升级说明。

- :ref:`使用 Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`使用 Composer 安装将 CodeIgniter4 添加到现有项目并进行升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

安全性
********

使用 $this->validate() 时
============================

在控制器的 :ref:`$this->validate() <controller-validate>` 中存在已知的潜在漏洞，可绕过验证。
攻击可以使开发人员误解未经验证的空数据为已验证数据并继续处理。

已添加 :ref:`Validation::getValidated() <validation-getting-validated-data>` 方法，以确保获取已验证数据。

因此，在你的控制器中使用 ``$this->validate()`` 时，应使用新的 ``Validation::getValidated()`` 方法获取已验证的数据。

.. literalinclude:: ../libraries/validation/045.php
   :lines: 2-

破坏性变更
****************

.. _upgrade-440-uri-setsegment:

URI::setSegment() 更改
========================

由于一个错误，在之前的版本中，如果指定了最后一个段 ``+2``，将不会抛出异常。这个错误已经修复。

如果你的代码依赖于这个错误，请修复段编号。

.. literalinclude:: upgrade_440/002.php
   :lines: 2-

站点 URI 更改
================

- 由于对当前 URI 确定进行了重新制定，框架可能以与以前版本不同的方式返回站点 URI 或 URI 路径。这可能会破坏你的测试代码。如果现有测试失败，请更新断言。
- 如果你的 baseURL 具有子目录，并且通过 ``URI::getPath()`` 方法获取当前 URI 的相对路径到 baseURL，你必须改用新的 ``SiteURI::getRoutePath()`` 方法。

有关详细信息，请参见 :ref:`v440-site-uri-changes`。

当你扩展异常时
==========================

如果你扩展了 ``CodeIgniter\Debug\Exceptions`` 并且未覆盖 ``exceptionHandler()`` 方法，那么在 **app/Config/Exceptions.php** 中定义新的 ``Config\Exceptions::handler()`` 方法将导致执行指定的异常处理程序。

你的覆盖代码将不再执行，因此请通过定义自己的异常处理程序进行必要的更改。

请参阅 :ref:`custom-exception-handlers` 了解详细信息。

自动路由（改进版）和 translateURIDashes
==============================================

在使用自动路由（改进版）和 ``$translateURIDashes`` 为 true 时（``$routes->setTranslateURIDashes(true)``），在以前版本中由于错误，两个 URI 对应一个控制器方法，一个 URI 用于破折号（例如 **foo-bar**），另一个 URI 用于下划线（例如 **foo_bar**）。

此错误已经修复，现在不再支持下划线 URI（**foo_bar**）。

如果你有指向下划线 URI（**foo_bar**）的链接，请将其更新为破折号 URI（**foo-bar**）。

传递带有命名空间的类名到工厂时
==================================================

传递带有命名空间的类名到工厂的行为已更改。有关详细信息，请参见 :ref:`ChangeLog <v440-factories>`。

如果你有类似于 ``model(\Myth\Auth\Models\UserModel::class)`` 或
``model('Myth\Auth\Models\UserModel')`` 的代码（代码可能在第三方包中），并且希望加载你的 ``App\Models\UserModel``，你需要在加载该类之前定义要加载的类名::

    Factories::define('models', 'Myth\Auth\Models\UserModel', 'App\Models\UserModel');

有关详细信息，请参见 :ref:`factories-defining-classname-to-be-loaded`。

接口更改
=================

已进行了一些接口更改。实现它们的类应该更新其 API 以反映更改。有关详细信息，请参见 :ref:`v440-interface-changes`。

方法签名更改
========================

已进行了一些方法签名更改。扩展它们的类应该更新其 API 以反映更改。有关详细信息，请参见 :ref:`v440-method-signature-changes`。

此外，某些构造函数和 ``Services::security()`` 的参数类型已更改。如果你使用这些参数调用它们，请更改参数值。有关详细信息，请参见 :ref:`v440-parameter-type-changes`。

RouteCollection::$routes
========================

受保护属性 ``$routes`` 的数组结构已进行了修改以提高性能。

如果你扩展了 ``RouteCollection`` 并使用了 ``$routes``，请更新你的代码以匹配新的数组结构。

必要的文件更改
**********************

index.php 和 spark
===================

以下文件已经接收到重大更改，**你必须将更新后的版本与你的应用程序合并**：

- ``public/index.php`` (还请参阅 :ref:`v440-codeigniter-and-exit` )
- ``spark``

.. important:: 如果你不更新上述文件，运行 ``composer update`` 后 CodeIgniter 将无法正常工作。

    升级过程，例如如下：

    .. code-block:: console

        composer update
        cp vendor/codeigniter4/framework/public/index.php public/index.php
        cp vendor/codeigniter4/framework/spark spark

配置文件
============

app/Config/App.php
------------------

属性 ``$proxyIPs`` 必须是数组。如果你不使用代理服务器，则它必须为 ``public array $proxyIPs = [];``。

.. _upgrade-440-config-routing:

app/Config/Routing.php
----------------------

为了清理路由系统，进行了以下更改：

- 新的 **app/Config/Routing.php** 文件保存了以前在 Routes 文件中的设置。
- **app/Config/Routes.php** 文件经过简化，仅包含路由，没有设置和冗余的内容。
- 不再自动加载特定于环境的路由文件。

因此，你需要执行以下操作：

1. 从新框架中复制 **app/Config/Routing.php** 到你的 **app/Config** 目录，并进行配置。
2. 删除不再需要的 **app/Config/Routes.php** 中的所有设置。
3. 如果使用特定于环境的路由文件，请将它们添加到 **app/Config/Routing.php** 中的 ``$routeFiles`` 属性中。

app/Config/Toolbar.php
----------------------

你需要添加新属性 ``$watchedDirectories`` 和 ``$watchedExtensions`` 以进行 :ref:`debug-toolbar-hot-reload`::

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

你需要添加代码以为 :ref:`debug-toolbar-hot-reload` 添加一个路由::

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

**app/Config/App.php** 中的 Cookie 配置项不再使用。

1. 从新框架中复制 **app/Config/Cookie.php** 到你的 **app/Config** 目录，并进行配置。
2. 删除 **app/Config/App.php** 中的属性（从 ``$cookiePrefix`` 到 ``$cookieSameSite``）。

app/Config/Security.php
-----------------------

**app/Config/App.php** 中的 CSRF 配置项不再使用。

1. 从新框架中复制 **app/Config/Security.php** 到你的 **app/Config** 目录，并进行配置。
2. 删除 **app/Config/App.php** 中的属性（从 ``$CSRFTokenName`` 到 ``$CSRFSameSite``）。

app/Config/Session.php
----------------------

**app/Config/App.php** 中的 Session 配置项不再使用。

1. 从新框架中复制 **app/Config/Session.php** 到你的 **app/Config** 目录，并进行配置。
2. 删除 **app/Config/App.php** 中的属性（从 ``$sessionDriver`` 到 ``$sessionDBGroup``）。

重大改进
*********************

- **路由：** ``RouteCollection::__construct()`` 的方法签名已更改。添加了第三个参数 ``Routing $routing``。扩展类应该同样添加参数以不违反 LSP。
- **验证：** ``Validation::check()`` 的方法签名已更改。``$rule`` 参数上的 ``string`` 类型提示已被删除。扩展类应该同样删除类型提示以不违反 LSP。

项目文件
*************

**项目空间** 中的一些文件（根目录、app、public、writable）已接收到更新。由于这些文件位于 **system** 范围之外，它们将不会在没有你干预的情况下更改。

有一些第三方 CodeIgniter 模块可帮助你合并对项目空间的更改：`在 Packagist 上查看 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容更改
===============

以下文件已接收到重大更改（包括弃用或视觉调整），建议你将更新后的版本与你的应用程序合并：

配置
------

- app/Config/CURLRequest.php
    - :ref:`$shareOptions <curlrequest-sharing-options>` 的默认值已更改为 ``false``。
- app/Config/Exceptions.php
    - 添加了新方法 ``handler()``，定义自定义异常处理程序。
      请参阅 :ref:`custom-exception-handlers`。

所有更改
===========

这是 **项目空间** 中所有文件的更改列表；其中许多将是对运行时没有影响的注释或格式化：

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
