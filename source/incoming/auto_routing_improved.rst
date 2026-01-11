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

默认情况下，所有路由都必须在配置文件中 :ref:`定义 <defined-route-routing>`。

但是，使用 **自动路由（改进版）**，你可以根据约定定义控制器名称及其方法名称，它将被自动路由。换句话说，无需手动定义路由。

如果启用自动路由（改进版），当找不到与 URI 匹配的已定义路由时，系统将尝试根据该 URI 匹配控制器和方法。

.. important:: 出于安全考虑，如果一个控制器已在定义的路由中被使用，那么自动路由（改进版）将不会再路由到该控制器。

.. note:: 自动路由（改进版）默认禁用。要使用它，请参见
    :ref:`enabled-auto-routing-improved`。

**************************************
与自动路由（传统版）的区别
**************************************

:ref:`auto-routing-legacy` 是 CodeIgniter 3 中的路由系统。如果你不熟悉它，可以跳到下一节。

如果你很了解它，以下是 **自动路由（改进版）** 的一些变化：

- 控制器方法需要带有 HTTP 动词前缀，如 `` getIndex() ``、`` postCreate() ``。
    - 由于开发者总是明确知道 HTTP 方法，因此使用预期之外的 HTTP 方法发出的请求将永远不会执行到该控制器。
- URI 中必须省略默认控制器（默认为 ``Home``）和默认方法（默认为 ``index``）。
    - 这保证了控制器方法与 URI 的一一对应关系。
    - 例如，默认情况下，你可以访问 ``/``，但 ``/home`` 和 ``/home/index`` 将返回 404 错误。
- 检查方法参数数量。
    - 如果 URI 中的参数多于方法参数，将返回 404 错误。
- 不支持 ``_remap()`` 方法。
    - 这保证了控制器方法与 URI 的一一对应关系。
    - 但提供了 :ref:`auto-routing-improved-default-method-fallback` 功能作为替代。
- 无法访问已在“定义路由”中配置的控制器。
    - 这将通过 **自动路由** 访问的控制器与通过 **定义路由** 访问的控制器完全分离开来。

.. _enabled-auto-routing-improved:

******************************
启用自动路由（改进版）
******************************

要使用该功能，需在 **app/Config/Routing.php** 中将 ``$autoRoute`` 选项设为 ``true``::

    public bool $autoRoute = true;

同时需在 **app/Config/Feature.php** 中将 ``$autoRoutesImproved`` 属性设为 ``true``::

    public bool $autoRoutesImproved = true;

.. important:: 当你使用自动路由（改进版）时，必须删除
    **app/Config/Routes.php** 中的 ``$routes->get('/', 'Home::index');``。因为
    已定义路由优先于自动路由，出于安全原因，已定义路由中定义的控制器会被自动路由（改进版）拒绝访问。

************
URI 分段
************

遵循 MVC 模式，URL 中的分段通常表示::

    http://example.com/{class}/{method}/{param1}

1. 第一分段表示要调用的控制器 **类**。
2. 第二分段表示要调用的类 **方法**。
3. 第三及后续分段表示传递给控制器方法的 **参数**。

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

使用你的文本编辑器，在 **app/Controllers** 目录中创建一个名为 **HelloWorld.php** 的文件，并将以下代码放入其中。

.. literalinclude:: auto_routing_improved/020.php

.. important:: 文件名必须为 **HelloWorld.php**。使用自动路由（改进版）时，控制器类名必须采用大驼峰式命名法。

注意 ``HelloWorld`` 控制器继承自 ``BaseController``。若不需要 BaseController 的功能，也可直接继承 ``CodeIgniter\Controller``。

BaseController 提供了方便的组件加载方式，并包含所有控制器共用的功能。你可以在任何新控制器中继承此类。

.. important:: 通过自动路由（改进版）执行的控制器方法需要添加 HTTP 动词（``get``、``post``、``put`` 等）前缀，如 ``getIndex()``、``postCreate()``。

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

访问你的站点
===============

现在使用类似这样的 URL 访问你的站点::

    http://example.com/hello-world

系统会自动将 URI 中的减号（``-``）转换为控制器和方法的大驼峰式命名。

例如，URI ``sub-dir/hello-controller/some-method`` 将执行 ``SubDir\HelloController::getSomeMethod()`` 方法。

成功操作后将显示::

    Hello World!

****************************
控制器命名示例
****************************

以下为有效控制器名称，因为 ``App\Controllers\HelloWorld`` 采用大驼峰式命名：

.. literalinclude:: auto_routing_improved/009.php

以下为 **无效命名**。因为首字母（``h``）不是大写。

.. literalinclude:: auto_routing_improved/010.php

以下同样是 **无效命名**。因为首字母（``h``）不是大写。

.. literalinclude:: auto_routing_improved/011.php

******************
控制器方法
******************

方法可见性
=================

当你定义一个可通过 HTTP 请求执行的方法时，该方法必须声明为 ``public``。

.. warning:: 出于安全考虑，请将所有工具方法声明为 ``protected`` 或 ``private``。

默认方法
==============

在上面的示例中，方法名是 ``getIndex()``。该方法（HTTP 动词 + ``Index()``）被称为 **默认方法**，当 URI 的 **第二分段** 为空时加载。

常规方法
==============

URI 的第二分段决定调用控制器中的哪个方法。

让我们试试。向你的控制器添加一个新方法：

.. literalinclude:: auto_routing_improved/021.php

现在访问以下 URL 来查看 ``getComment()`` 方法::

    http://example.com/hello-world/comment/

你将看到新消息。

************************************
向方法传递 URI 分段
************************************

如果你的 URI 包含超过两个分段，它们将作为参数传递给方法。

例如，假设你有这样一个 URI::

    http://example.com/products/shoes/sandals/123

该方法将接收第 3、4 分段（``'sandals'`` 和 ``'123'``）：

.. literalinclude:: auto_routing_improved/022.php

.. note:: 如果 URI 中的参数多于方法参数，自动路由（改进版）不会执行该方法，并返回 404 错误。

******************
默认控制器
******************

**默认控制器** 是在 URI 以目录名结尾或未指定 URI（如访问站点根 URL）时使用的特殊控制器。

默认情况下，默认控制器是 ``Home``。

.. note:: 只在默认控制器中定义默认方法（对于 GET 请求是 ``getIndex()``）。
    如果你定义任何其他公共方法，该方法将不会被执行。

有关更多信息，请参阅 :ref:`routing-auto-routing-improved-configuration-options`。

.. _auto-routing-improved-default-method-fallback:

***********************
默认方法回退
***********************

.. versionadded:: 4.4.0

如果 URI 中代表方法名的分段所对应的控制器方法不存在，并且（在该控制器中）定义了默认方法，那么剩余的 URI 分段将会被传递给这个默认方法来执行。

.. literalinclude:: controllers/024.php

访问以下 URL::

    http://example.com/product/15/edit

该方法将接收第 2、3 分段（``'15'`` 和 ``'edit'``）：

.. important:: 如果 URI 中的参数多于方法参数，
    自动路由（改进版）不会执行该方法，并返回 404 错误。

回退到默认控制器
==============================

如果 URI 中代表控制器名的分段所对应的控制器不存在，并且该目录中存在默认控制器（默认为 ``Home``），那么剩余的 URI 分段将会被传递给该默认控制器的默认方法。

例如，当你在 **app/Controllers/News** 目录中有以下默认控制器 ``Home`` 时：

.. literalinclude:: controllers/025.php

访问以下 URL::

    http://example.com/news/101

将找到 ``News\Home`` 控制器和默认的 ``getIndex()`` 方法。因此默认方法将获取第二 URI 分段（``'101'``）：

.. note:: 如果存在 ``App\Controllers\News`` 控制器，则优先使用。
    URI 段按顺序搜索，使用找到的第一个控制器。

.. note:: 如果 URI 中的参数多于方法参数，
    自动路由（改进版）不会执行该方法，并返回 404 错误。

************************************************
将控制器组织到子目录中
************************************************

在构建大型应用程序时，你可能希望将控制器按层级结构放入子目录中来管理。CodeIgniter 支持这种做法。

你只需在 **app/Controllers** 主目录下创建子目录，然后将相应的控制器类（文件）放入这些目录中即可。

.. important:: 目录名必须以大写字母开头，并且是大驼峰式命名。

使用此功能时，URI 的第一分段必须指定目录。例如，假设你有一个位于以下位置的控制器::

    app/Controllers/Products/Shoes.php

要调用上述控制器，你的 URI 看起来会是这个样子::

    http://example.com/products/shoes/show/123

.. note:: **app/Controllers** 和 **public** 目录不能存在同名目录，否则 Web 服务器将直接访问该目录而不会路由到 CodeIgniter。

每个子目录都可以包含一个默认控制器。如果 URL 访问的路径 *刚好* 是这个子目录（即没有指定具体的控制器名），那么这个默认控制器就会被调用。实现方法很简单：你只需在该目录中放置一个控制器，确保它的名称与你在 **app/Config/Routing.php** 文件中指定的默认控制器名称一致即可。

***************************************
控制器/方法与 URI 对应示例
***************************************

在默认配置下，当收到一个 **GET** 请求时，控制器/方法与 URI 之间的对应关系如下：

============================ ============================ =============================================
控制器/方法                  URI                          说明
============================ ============================ =============================================
``Home::getIndex()``         /                            默认控制器和默认方法。
``Blog::getIndex()``         /blog                        默认方法。
``UserProfile::getIndex()``  /user-profile                默认方法。
``Blog::getTags()``          /blog/tags
``Blog::getNews($id)``       /blog/news/123
``Blog\Home::getIndex()``    /blog                        ``Blog`` 子目录中的默认控制器和默认方法。若存在 ``Blog`` 控制器则优先使用
``Blog\Tags::getIndex()``    /blog/tags                   ``Blog`` 子目录中的默认方法。若存在 ``Blog`` 控制器则优先使用
``Blog\News::getIndex($id)`` /blog/news/123               ``Blog`` 子目录中的默认方法后备机制。若存在 ``Blog`` 控制器则优先使用
============================ ============================ =============================================

****************
应用过滤器
****************

应用控制器过滤器可在控制器方法执行前后添加处理逻辑，适用于身份验证或 API 日志记录等场景。

使用自动路由时，需在 **app/Config/Filters.php** 中设置要应用的过滤器。
有关设置过滤器的更多信息，请参阅 :doc:`控制器过滤器 <filters>`。

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

在未找到匹配的路由，且 URI 恰好指向控制器目录下的某个（子）目录时，系统也会启用默认控制器。例如，当用户访问 **http://example.com/admin** 时，如果系统在 **app/Controllers/Admin/Home.php** 路径下找到了相应的控制器，那么该控制器便会被调用。

.. important:: 无法通过控制器名称对应的 URI 来访问默认控制器。当默认控制器是 ``Home`` 时，可以访问 **http://example.com/**，但如果访问 **http://example.com/home**，则会返回 404 错误。

.. _routing-auto-routing-improved-default-method:

默认方法
==============

此设置的工作原理与默认控制器相似，但其用途是确定默认方法。当系统找到了匹配 URI 的控制器，但 URI 中却不存在用于指定方法的分段时，系统便会转而使用这个默认方法。默认值为 ``index``。

在此示例中，如果用户访问 **example.com/products**，而此时恰好存在一个 ``Products`` 控制器，那么 ``Products::getListAll()`` 方法就会被执行::

    public string $defaultMethod = 'listAll';

.. important:: 无法通过默认方法名对应的 URI 来访问该控制器。在上面的例子中，可以访问 **example.com/products**，但如果试图访问 **example.com/products/listall**，则会返回 404 错误。

.. _translate-uri-to-camelcase:

将 URI 转换为大驼峰命名
==========================

.. versionadded:: 4.5.0

.. note:: 从 v4.6.0 开始，``$translateUriToCamelCase`` 选项默认启用。

从 v4.5.0 开始，实现了 ``$translateUriToCamelCase`` 选项，它与当前 CodeIgniter 的编码标准配合良好。

此选项可自动将 URI 中的减号（``-``）转换为控制器和方法的大驼峰式命名。

例如，URI ``sub-dir/hello-controller/some-method`` 将执行 ``SubDir\HelloController::getSomeMethod()`` 方法。

.. note:: 启用此选项时，``$translateURIDashes`` 选项将被忽略。

禁用将 URI 转换为大驼峰命名
----------------------------------

.. note:: 禁用“将 URI 转换为大驼峰命名”的选项仅用于向后兼容，不建议禁用。

要禁用它，你需要在 **app/Config/Routing.php** 中将 ``$translateUriToCamelCase`` 选项更改为 ``false``::

    public bool $translateUriToCamelCase = false;

.. _auto-routing-improved-module-routing:

**************
模块路由
**************

.. versionadded:: 4.4.0

即使使用 :doc:`../general/modules` 并将控制器放置在不同命名空间，仍可使用自动路由。

要路由到模块，必须在 **app/Config/Routing.php** 中设置 ``$moduleRoutes`` 属性::

    public array $moduleRoutes = [
        'blog' => 'Acme\Blog\Controllers',
    ];

键名是模块的第一个 URI 分段，值是控制器命名空间。在上述配置中，**http://localhost:8080/blog/foo/bar** 将被路由到 ``Acme\Blog\Controllers\Foo::getBar()``。

.. note:: 若你定义了 ``$moduleRoutes``，则该模块的路由将 **优先**（被处理）。在上面的示例中，即便你（的应用中）存在 ``App\Controllers\Blog`` 控制器，访问 **http://localhost:8080/blog** 的请求也（仍）将被路由至（模块的）默认控制器 ``Acme\Blog\Controllers\Home``。
