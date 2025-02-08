.. _auto-routing-improved:

#######################
自动路由（改进版）
#######################

.. versionadded:: 4.2.0

.. contents::
    :local:
    :depth: 3

*********************************
什么是自动路由（改进版）？
*********************************

默认情况下，所有路由都必须在配置文件中通过 :ref:`defined <defined-route-routing>` 方式定义。

但通过 **自动路由（改进版）**，你可以根据约定定义控制器名称及其方法名称，系统将自动进行路由。换句话说，无需手动定义路由。

启用自动路由（改进版）后，当未找到与 URI 匹配的已定义路由时，系统将尝试根据控制器和方法进行匹配。

.. important:: 出于安全考虑，若控制器已在定义的路由中使用，则自动路由（改进版）不会路由到该控制器。

.. note:: 自动路由（改进版）默认禁用。要启用请参阅 :ref:`enabled-auto-routing-improved`。

**************************************
与自动路由（旧版）的差异
**************************************

:ref:`auto-routing-legacy` 是 CodeIgniter 3 的路由系统。如果你不熟悉该功能，可直接阅读下一章节。

如果你已了解旧版路由，以下是 **自动路由（改进版）** 的主要变化：

- 控制器方法需要添加 HTTP 动词前缀如 ``getIndex()``、``postCreate()``
    - 由于开发者始终明确 HTTP 方法，使用非预期的 HTTP 方法请求将不会执行控制器
- URI 中必须省略默认控制器（默认为 ``Home``）和默认方法（默认为 ``index``）
    - 这保证了控制器方法与 URI 的一一对应关系
    - 例如默认情况下可访问 ``/``，但 ``/home`` 和 ``/home/index`` 将返回 404 错误
- 检查方法参数数量
    - 若 URI 中的参数数量超过方法参数数量，将返回 404 错误
- 不支持 ``_remap()`` 方法
    - 这保证了控制器方法与 URI 的一一对应关系
    - 但提供了 :ref:`auto-routing-improved-default-method-fallback` 功能作为替代
- 无法访问已定义路由中的控制器
    - 通过 **自动路由** 访问的控制器与通过 **定义路由** 访问的控制器完全分离

.. _enabled-auto-routing-improved:

******************************
启用自动路由（改进版）
******************************

要使用该功能，需在 **app/Config/Routing.php** 中将 ``$autoRoute`` 选项设为 ``true``::

    public bool $autoRoute = true;

同时需在 **app/Config/Feature.php** 中将 ``$autoRoutesImproved`` 属性设为 ``true``::

    public bool $autoRoutesImproved = true;

.. important:: 使用自动路由（改进版）时，必须移除 **app/Config/Routes.php** 中的 ``$routes->get('/', 'Home::index');`` 行。因为定义路由优先级高于自动路由，且出于安全考虑，自动路由（改进版）会拒绝访问已定义路由中的控制器。

************
URI 分段
************

遵循 MVC 模式，URL 中的分段通常表示::

    http://example.com/{class}/{method}/{param1}

1. 第一分段表示要调用的控制器 **类**
2. 第二分段表示要调用的类 **方法**
3. 第三及后续分段表示传递给控制器方法的 **参数**

示例 URI::

    http://example.com/hello-world/hello/1

当使用 **GET** 方法发送 HTTP 请求时，自动路由（改进版）会尝试查找名为 ``App\Controllers\HelloWorld`` 的控制器，并执行 ``getHello()`` 方法，同时传递 ``'1'`` 作为第一个参数。

.. note:: 通过自动路由（改进版）执行的控制器方法需要添加 HTTP 动词（``get``、``post``、``put`` 等）前缀，如 ``getIndex()``、``postCreate()``。

.. note:: 当控制器的短名称与 URI 的第一分段匹配时，该控制器将被加载。

**************************
实践演练：Hello World!
**************************

让我们创建一个简单控制器来演示该功能。

创建控制器
===================

在 **app/Controllers** 目录中创建名为 **HelloWorld.php** 的文件，并添加以下代码：

.. literalinclude:: auto_routing_improved/020.php

.. important:: 文件名必须为 **HelloWorld.php**。使用自动路由（改进版）时，控制器类名必须采用大驼峰式命名法。

注意 ``HelloWorld`` 控制器继承自 ``BaseController``。若不需要基控制器功能，也可直接继承 ``CodeIgniter\Controller``。

BaseController 提供了方便的组件加载方式，并包含所有控制器共用的功能。你可以在任何新控制器中继承此类。

.. important:: 通过自动路由（改进版）执行的控制器方法必须添加 HTTP 动词前缀，如 ``getIndex()``、``postCreate()``。

检查路由
================

可通过 ``spark routes`` 命令查看路由信息：

.. code-block:: console

    php spark routes

成功操作后将显示：

.. code-block:: none

    +-----------+-------------+------+---------------------------------------+----------------+---------------+
    | Method    | Route       | Name | Handler                               | Before Filters | After Filters |
    +-----------+-------------+------+---------------------------------------+----------------+---------------+
    | GET(auto) | hello-world |      | \App\Controllers\HelloWorld::getIndex |                |               |
    +-----------+-------------+------+---------------------------------------+----------------+---------------+

详情请参阅 :ref:`routing-spark-routes`。

访问页面
===============

现在通过以下 URL 访问你的站点::

    http://example.com/hello-world

系统会自动将 URI 中的短横线（``-``）转换为控制器和方法的大驼峰式命名。

例如 URI ``sub-dir/hello-controller/some-method`` 将执行 ``SubDir\HelloController::getSomeMethod()`` 方法。

成功操作后将显示::

    Hello World!

****************************
控制器命名示例
****************************

以下为有效控制器名称，因为 ``App\Controllers\HelloWorld`` 采用大驼峰式命名：

.. literalinclude:: auto_routing_improved/009.php

以下为无效命名，因为首字母（``h``）未大写：

.. literalinclude:: auto_routing_improved/010.php

以下同样无效，因为首字母（``h``）未大写：

.. literalinclude:: auto_routing_improved/011.php

******************
控制器方法
******************

方法可见性
=================

通过 HTTP 请求执行的方法必须声明为 ``public``。

.. warning:: 出于安全考虑，请将所有工具方法声明为 ``protected`` 或 ``private``。

默认方法
==============

上述示例中的 ``getIndex()`` 方法称为 **默认方法**，当 URI 的 **第二分段** 为空时将被调用。

常规方法
==============

URI 的第二分段决定调用控制器中的哪个方法。

添加新方法进行测试：

.. literalinclude:: auto_routing_improved/021.php

现在访问以下 URL 查看 ``getComment()`` 方法::

    http://example.com/hello-world/comment/

你将看到新消息。

************************************
向方法传递 URI 分段
************************************

若 URI 包含超过两个分段，后续分段将作为参数传递给方法。

示例 URI::

    http://example.com/products/shoes/sandals/123

该方法将接收第 3、4 分段（``'sandals'`` 和 ``'123'``）：

.. literalinclude:: auto_routing_improved/022.php

.. note:: 若 URI 参数数量超过方法参数数量，自动路由（改进版）不会执行该方法，并返回 404 错误。

******************
默认控制器
******************

**默认控制器** 是在 URI 以目录名结尾或未指定 URI（如访问站点根 URL）时使用的特殊控制器。

默认控制器为 ``Home``。

.. note:: 默认控制器中只应定义默认方法（GET 请求对应 ``getIndex()``）。若定义其他公共方法，这些方法将无法执行。

更多信息请参考 :ref:`routing-auto-routing-improved-configuration-options`。

.. _auto-routing-improved-default-method-fallback:

***********************
默认方法回退
***********************

.. versionadded:: 4.4.0

当 URI 方法名分段对应的控制器方法不存在，但默认方法已定义时，剩余 URI 分段将传递给默认方法执行。

.. literalinclude:: controllers/024.php

访问以下 URL::

    http://example.com/product/15/edit

该方法将接收第 2、3 分段（``'15'`` 和 ``'edit'``）：

.. important:: 若 URI 参数数量超过方法参数数量，自动路由（改进版）不会执行该方法，并返回 404 错误。

回退至默认控制器
==============================

当 URI 控制器名分段对应的控制器不存在，但目录中存在默认控制器（默认为 ``Home``）时，剩余 URI 分段将传递给默认控制器的默认方法。

示例在 **app/Controllers/News** 目录中创建默认控制器 ``Home``：

.. literalinclude:: controllers/025.php

访问以下 URL::

    http://example.com/news/101

系统将找到 ``News\Home`` 控制器及其默认 ``getIndex()`` 方法。默认方法将接收第二 URI 分段（``'101'``）：

.. note:: 若存在 ``App\Controllers\News`` 控制器，则优先使用。URI 分段将按顺序搜索，使用首个找到的控制器。

.. note:: 若 URI 参数数量超过方法参数数量，自动路由（改进版）不会执行该方法，并返回 404 错误。

************************************************
控制器子目录组织
************************************************

在大型应用中，你可能希望将控制器组织到子目录中。CodeIgniter 支持此功能。

只需在 **app/Controllers** 下创建子目录（目录名必须以大写字母开头并采用大驼峰式命名），并将控制器类存放其中。

示例控制器路径::

    app/Controllers/Products/Shoes.php

调用该控制器的 URI 形如::

    http://example.com/products/shoes/show/123

.. note:: **app/Controllers** 和 **public** 目录不能存在同名目录，否则 Web 服务器将直接访问该目录而不会路由到 CodeIgniter。

每个子目录可包含默认控制器，当 URL 仅包含子目录时将调用该控制器。需确保默认控制器名称与 **app/Config/Routing.php** 中配置一致。

***************************************
控制器/方法与 URI 对应示例
***************************************

在默认配置下，GET 请求的控制器/方法与 URI 对应关系如下：

============================ ============================ =============================================
控制器/方法                   URI                          说明
============================ ============================ =============================================
``Home::getIndex()``         /                            默认控制器和默认方法
``Blog::getIndex()``         /blog                        默认方法
``UserProfile::getIndex()``  /user-profile                默认方法
``Blog::getTags()``          /blog/tags
``Blog::getNews($id)``       /blog/news/123
``Blog\Home::getIndex()``    /blog                        子目录 ``Blog`` 中的默认控制器和默认方法。若存在 ``Blog`` 控制器则优先使用
``Blog\Tags::getIndex()``    /blog/tags                   子目录 ``Blog`` 中的默认方法。若存在 ``Blog`` 控制器则优先使用
``Blog\News::getIndex($id)`` /blog/news/123               子目录 ``Blog`` 中的默认方法回退。若存在 ``Blog`` 控制器则优先使用
============================ ============================ =============================================

****************
应用过滤器
****************

应用控制器过滤器可在控制器方法执行前后添加处理逻辑，适用于身份验证或 API 日志记录等场景。

使用自动路由时，需在 **app/Config/Filters.php** 中设置要应用的过滤器。详情请参阅 :doc:`控制器过滤器 <filters>` 文档。

.. _routing-auto-routing-improved-configuration-options:

*********************
配置选项
*********************

以下选项位于 **app/Config/Routing.php** 文件。

默认控制器
==================

站点根 URI
-----------------

当用户访问站点根目录（如 **http://example.com**）时，除非存在显式路由，否则将使用 ``$defaultController`` 属性指定的控制器。

默认值为 ``Home``，对应 **app/Controllers/Home.php** 控制器::

    public string $defaultController = 'Home';

目录 URI
-----------------

当未找到匹配路由且 URI 指向控制器目录时，也使用默认控制器。例如用户访问 **http://example.com/admin**，若存在 **app/Controllers/Admin/Home.php** 控制器，则使用该控制器。

.. important:: 无法通过控制器名称的 URI 访问默认控制器。当默认控制器为 ``Home`` 时，可访问 **http://example.com/**，但访问 **http://example.com/home** 将返回 404 错误。

.. _routing-auto-routing-improved-default-method:

默认方法
==============

此设置与默认控制器类似，用于确定当找到匹配 URI 的控制器但未指定方法分段时使用的默认方法。默认值为 ``index``。

示例配置::

    public string $defaultMethod = 'listAll';

当用户访问 **example.com/products** 且存在 ``Products`` 控制器时，将执行 ``Products::getListAll()`` 方法。

.. important:: 无法通过默认方法名称的 URI 访问控制器。上述示例中可访问 **example.com/products**，但访问 **example.com/products/listall** 将返回 404 错误。

.. _translate-uri-to-camelcase:

URI 转驼峰命名
==========================

.. versionadded:: 4.5.0

.. note:: 自 v4.6.0 起，``$translateUriToCamelCase`` 选项默认启用

自 v4.5.0 起实现的 ``$translateUriToCamelCase`` 选项完美适配当前 CodeIgniter 的编码规范。

此选项可自动将 URI 中的短横线（``-``）转换为控制器和方法的大驼峰式命名。

示例 URI ``sub-dir/hello-controller/some-method`` 将执行 ``SubDir\HelloController::getSomeMethod()`` 方法。

.. note:: 启用此选项时，``$translateURIDashes`` 选项将被忽略。

禁用 URI 转驼峰命名
----------------------------------

.. note:: 禁用 "URI 转驼峰命名" 的选项仅用于向后兼容，不建议禁用。

在 **app/Config/Routing.php** 中将 ``$translateUriToCamelCase`` 设为 ``false`` 即可禁用::

    public bool $translateUriToCamelCase = false;

.. _auto-routing-improved-module-routing:

**************
模块路由
**************

.. versionadded:: 4.4.0

即使使用 :doc:`../general/modules` 并将控制器放置在不同命名空间，仍可使用自动路由。

要路由到模块，需在 **app/Config/Routing.php** 中设置 ``$moduleRoutes`` 属性::

    public array $moduleRoutes = [
        'blog' => 'Acme\Blog\Controllers',
    ];

键名为模块的第一个 URI 分段，值为控制器命名空间。上述配置中，**http://localhost:8080/blog/foo/bar** 将路由到 ``Acme\Blog\Controllers\Foo::getBar()``。

.. note:: 若定义 ``$moduleRoutes``，模块路由将优先处理。上述示例中即使存在 ``App\Controllers\Blog`` 控制器，**http://localhost:8080/blog** 仍会路由到默认控制器 ``Acme\Blog\Controllers\Home``。
