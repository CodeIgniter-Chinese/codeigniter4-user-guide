###########
URI 路由
###########

.. contents::
    :local:
    :depth: 3

什么是 URI 路由？
********************

URI 路由将 URI 与控制器的方法关联起来。

CodeIgniter 有两种路由方式。一种是 **定义式路由**，另一种是 **自动路由**。通过定义式路由，你可以手动定义路由规则，这种方式允许更灵活的 URL 结构。自动路由则基于约定自动映射 HTTP 请求到对应的控制器方法，无需手动定义路由。

首先我们来看定义式路由。如需使用自动路由，请参阅 :ref:`auto-routing-improved`。

.. _defined-route-routing:

设置路由规则
*********************

路由规则定义在 **app/Config/Routes.php** 文件中。在该文件中，你会看到创建了一个 RouteCollection 类的实例（``$routes``），用于指定自定义路由条件。可以使用占位符或正则表达式来定义路由。

当定义路由时，需选择与 HTTP 方法（请求方法）对应的路由方法。例如处理 GET 请求时使用 ``get()`` 方法：

.. literalinclude:: routing/001.php

路由左侧指定 **路由路径** （相对于 BaseURL 的 URI 路径，以 ``/`` 开头），右侧映射到 **路由处理器** （控制器和方法 ``Home::index``），并可传递参数给控制器。

控制器和方法应按静态方法的形式列出，使用双冒号分隔类和方法，例如 ``Users::list``。

若方法需要参数，可在方法名后使用斜杠分隔：

.. literalinclude:: routing/002.php

示例
========

以下是几个基础路由示例：

当 URL 第一段包含 **journals** 时，将映射到 ``\App\Controllers\Blogs`` 类，并调用 :ref:`默认方法 <routing-default-method>` （通常为 ``index()``）：

.. literalinclude:: routing/006.php

当 URL 包含 **blog/joe** 时，映射到 ``\App\Controllers\Blogs`` 类的 ``users()`` 方法，ID 参数设为 ``34``：

.. literalinclude:: routing/007.php

当 URL 第一段为 **product**，第二段为任意内容时，映射到 ``\App\Controllers\Catalog`` 类的 ``productLookup()`` 方法：

.. literalinclude:: routing/008.php

当 URL 第一段为 **product**，第二段为数字时，映射到 ``\App\Controllers\Catalog`` 类的 ``productLookupByID()`` 方法，并将匹配值作为参数传递：

.. literalinclude:: routing/009.php

.. _routing-http-verb-routes:

HTTP 方法路由
================

可以使用任意标准 HTTP 方法（GET、POST、PUT、DELETE、OPTIONS 等）：

.. literalinclude:: routing/003.php

通过 ``match()`` 方法传入方法数组，可匹配多个 HTTP 方法：

.. literalinclude:: routing/004.php

指定路由处理器
=========================

.. _controllers-namespace:

控制器的命名空间
----------------------

当以字符串形式指定控制器和方法名时，若控制器名称未以 ``\`` 开头，系统会自动添加 :ref:`routing-default-namespace`：

.. literalinclude:: routing/063.php

若以 ``\`` 开头，则视为完全限定类名：

.. literalinclude:: routing/064.php

也可通过 ``namespace`` 选项指定命名空间：

.. literalinclude:: routing/038.php

详见 :ref:`assigning-namespace`。

数组可调用语法
---------------------

.. versionadded:: 4.2.0

从 v4.2.0 开始，可使用数组可调用语法指定控制器：

.. literalinclude:: routing/013.php
   :lines: 2-

或使用 ``use`` 关键字：

.. literalinclude:: routing/014.php
   :lines: 2-

若忘记添加 ``use App\Controllers\Home;``，控制器类名将被解析为 ``\Home`` 而非 ``App\Controllers\Home``。

.. note:: 使用数组可调用语法时，类名始终视为完全限定类名，因此 :ref:`routing-default-namespace` 和 :ref:`namespace 选项 <assigning-namespace>` 将失效。

数组可调用语法与占位符
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

若存在占位符，参数将按指定顺序自动设置：

.. literalinclude:: routing/015.php
   :lines: 2-

但在路由中使用正则表达式时，自动配置的参数可能不正确。此时可手动指定参数：

.. literalinclude:: routing/016.php
   :lines: 2-

使用闭包
--------------

可使用匿名函数（闭包）作为路由目标。当用户访问对应 URI 时，该函数将被执行，适用于快速执行小任务或显示简单视图：

.. literalinclude:: routing/020.php

指定路由路径
======================

占位符
------------

典型路由示例如下：

.. literalinclude:: routing/005.php

路由的第一个参数是待匹配的 URI，第二个参数是目标路由。当 URL 路径第一段为 "product" 且第二段为数字时，将使用 ``Catalog`` 类的 ``productLookup`` 方法。

占位符是代表正则表达式模式的字符串，在路由过程中会被替换为实际正则表达式，主要用于提升可读性。

可用占位符列表：

============ ===========================================================================================================
占位符       描述
============ ===========================================================================================================
(:any)       匹配从该位置到 URI 末尾的所有字符，可能包含多个段
(:segment)   匹配除斜杠（``/``）外的任意字符，限制为单个段
(:num)       匹配任意整数
(:alpha)     匹配任意字母字符串
(:alphanum)  匹配任意字母数字组合字符串
(:hash)      与 ``(:segment)`` 相同，便于识别使用哈希 ID 的路由
============ ===========================================================================================================

.. note:: ``{locale}`` 不能作为占位符或路由其他部分，保留用于 :doc:`本地化 </outgoing/localization>`。

.. _routing-placeholder-any:

(:any) 的行为
^^^^^^^^^^^^^^^^^^^^^^

注意单个 ``(:any)`` 会匹配 URL 中的多个段（如果存在）。

例如路由：

.. literalinclude:: routing/010.php

将匹配 **product/123**、**product/123/456**、**product/123/456/789** 等。

默认情况下，上述示例中若 ``$1`` 占位符包含斜杠（``/``），传递给 ``Catalog::productLookup()`` 时仍会分割为多个参数。

.. note:: 自 v4.5.0 起，可通过配置选项修改此行为，详见 :ref:`multiple-uri-segments-as-one-parameter`。

控制器实现应考虑最大参数数量：

.. literalinclude:: routing/011.php

或使用 `可变数量的参数值列表 <https://www.php.net/manual/zh/functions.arguments.php#functions.variable-arg-list>`_：

.. literalinclude:: routing/068.php

.. important:: 请勿在 ``(:any)`` 后放置其他占位符，因为传递给控制器方法的参数数量可能变化。

若不需要匹配多段，应在定义路由时使用 ``(:segment)``：

.. literalinclude:: routing/012.php

该路由仅匹配 **product/123**，其他情况返回 404 错误。

自定义占位符
-------------------

可创建自定义占位符来完全定制路由体验。

使用 ``addPlaceholder()`` 方法添加新占位符，第一个参数是占位符字符串，第二个参数是替换的正则表达式。需在添加路由前调用：

.. literalinclude:: routing/017.php

正则表达式
-------------------

可使用正则表达式定义路由规则。允许任何有效正则表达式及反向引用。

.. important:: 注意：使用反向引用时需使用美元符号语法而非双反斜杠语法。典型正则路由示例：

    .. literalinclude:: routing/018.php

上述示例中，类似 **products/shirts/123** 的 URI 将调用 ``Products`` 控制器的 ``show()`` 方法，原始第一、二段作为参数传递。

通过正则表达式可捕获包含斜杠的段（通常用于分隔多个段）。例如用户访问受密码保护区域后重定向回原页面：

.. literalinclude:: routing/019.php

默认情况下，若 ``$1`` 占位符包含斜杠，传递给 ``Auth::login()`` 时仍会分割为多个参数。

.. note:: 自 v4.5.0 起，可通过配置选项修改此行为，详见 :ref:`multiple-uri-segments-as-one-parameter`。

关于正则表达式学习，推荐访问 `regular-expressions.info <https://www.regular-expressions.info/>`_。

.. note:: 可混合使用占位符和正则表达式。

.. _view-routes:

视图路由
===========

.. versionadded:: 4.3.0

若只需渲染无逻辑视图，可使用 ``view()`` 方法（始终视为 GET 请求）。第二个参数指定视图名称：

.. literalinclude:: routing/065.php

若路由中使用占位符，可通过 ``$segments`` 数组在视图中访问：

.. literalinclude:: routing/066.php

.. _redirecting-routes:

重定向路由
==================

网站改版常需页面重定向。使用 ``addRedirect()`` 方法指定旧路由重定向到新路由。第一个参数是旧路由 URI 模式，第二个参数是新 URI 或命名路由名称，第三个参数是 HTTP 状态码（默认 302 临时重定向）：

.. literalinclude:: routing/022.php

.. note:: 自 v4.2.0 起，``addRedirect()`` 支持占位符。

匹配重定向路由时，用户将在控制器加载前立即跳转。

环境限制
========================

可创建仅特定环境可见的路由（如开发者本地工具）。使用 ``environment()`` 方法，参数为环境名称，闭包内定义的路由仅在该环境下可用：

.. literalinclude:: routing/028.php

任意 HTTP 方法路由
==========================

.. important:: 此方法仅为向后兼容保留，新项目请勿使用。建议使用更合适的 HTTP 方法路由。

.. warning:: 使用 :doc:`CSRF 保护 </libraries/security>` 时，不会保护 **GET** 请求。若 ``add()`` 方法指定的 URI 可通过 GET 访问，CSRF 保护将失效。

使用 ``add()`` 方法定义支持任意 HTTP 方法的路由：

.. literalinclude:: routing/031.php

.. note:: 使用 HTTP 方法路由可提升性能，因为仅存储匹配当前请求方法的路由。

批量映射路由
=======================

.. important:: 此方法仅为向后兼容保留，新项目请勿使用。建议使用更合适的方法。

.. warning:: 由于 ``map()`` 内部调用 ``add()``，同样不推荐使用。

使用 ``map()`` 方法批量定义路由数组：

.. literalinclude:: routing/021.php

.. _command-line-only-routes:

仅命令行路由
========================

.. note:: 建议使用 Spark 命令处理 CLI 脚本，而非通过 CLI 调用控制器。详见 :doc:`../cli/cli_commands`。

通过 HTTP 方法创建的路由 CLI 不可访问，但 ``add()`` 创建的路由仍可在命令行使用。使用 ``cli()`` 方法创建仅 CLI 可用的路由：

.. literalinclude:: routing/032.php

.. warning:: 若启用 :ref:`auto-routing-legacy` 并将命令文件置于 **app/Controllers**，他人可能通过自动路由（传统）HTTP 访问该命令。

全局选项
**************

所有路由创建方法（``get()``、``post()``、:doc:`resource() <restful>` 等）均可接受选项数组作为最后一个参数，用于修改或限制生成的路由：

.. literalinclude:: routing/033.php

.. _applying-filters:

应用过滤器
================

可通过为路由添加过滤器来修改特定路由行为（如身份验证或 API 日志记录）。过滤器值可以是字符串或字符串数组：

* 匹配 **app/Config/Filters.php** 中定义的别名
* 过滤器类名

详见 :ref:`控制器过滤器 <filters-aliases>`。

.. warning:: 若在 **app/Config/Routes.php** 设置路由过滤器（非 **app/Config/Filters.php**），建议禁用自动路由（传统）。启用 :ref:`auto-routing-legacy` 时，控制器可能通过不同 URL 访问，导致路由过滤器未生效。详见 :ref:`use-defined-routes-only`。

别名过滤器
------------

你可以为过滤器值指定一个 :ref:`在 app/Config/Filters.php 中定义 <filters-aliases>` 的别名。

.. literalinclude:: routing/034.php

可为别名过滤器的 ``before()`` 和 ``after()`` 方法传递参数：

.. literalinclude:: routing/035.php

类名过滤器
----------------

.. versionadded:: 4.1.5

直接指定过滤器类名：

.. literalinclude:: routing/036.php

.. _multiple-filters:

多重过滤器
----------------

.. versionadded:: 4.1.5

.. important:: 自 v4.5.0 起始终启用 *多重过滤器* ，v4.5.0 之前默认禁用，如需使用请参考 :ref:`从 4.1.4 升级到 4.1.5 <upgrade-415-multiple-filters-for-a-route>`。

指定过滤器数组：

.. literalinclude:: routing/037.php

过滤器参数
^^^^^^^^^^^^^^^^

可向过滤器传递额外参数：

.. literalinclude:: routing/067.php

此例中数组 ``['dual', 'noreturn']`` 将作为 ``$arguments`` 传递给过滤器的 ``before()`` 和 ``after()`` 方法。

.. _assigning-namespace:

分配命名空间
===================

虽然系统会自动添加 :ref:`routing-default-namespace` 到生成的控制器，但可通过 ``namespace`` 选项指定不同命名空间：

.. literalinclude:: routing/038.php

新命名空间仅作用于单路由创建方法（如 get、post 等）。对于创建多路由的方法（如 ``group()``），新命名空间将附加到所有生成的路由。

限制主机名
=================

通过“hostname”选项限制路由组仅在特定域名或子域生效：

.. literalinclude:: routing/039.php

此示例仅允许 **accounts.example.com** 域名访问，主域 **example.com** 不可用。

多主机名限制
------------------------------

.. versionadded:: 4.6.0

支持多个主机名限制：

.. literalinclude:: routing/073.php

限制子域
===================

通过 ``subdomain`` 选项限制路由仅在特定子域可用：

.. literalinclude:: routing/040.php

设置值为星号（``*``）可匹配任意子域，但无子域的 URL 不匹配：

.. literalinclude:: routing/041.php

.. important:: 此功能并非完美，生产环境前需充分测试。某些含点的域名可能导致误判。

偏移匹配参数
=================================

通过 ``offset`` 选项数值偏移匹配参数。适用于 API 版本号或语言字符串作为首段的情况：

.. literalinclude:: routing/042.php

.. _reverse-routing:

反向路由
***************

反向路由允许通过控制器、方法及参数定义链接，由路由器查找当前路由。这使得修改路由定义无需更新应用代码，常用于视图创建链接。

使用 :php:func:`url_to()` 辅助函数获取路由。第一个参数是完全限定的控制器和方法（用双冒号分隔），后续参数传递路由参数：

.. literalinclude:: routing/029.php

.. _using-named-routes:

命名路由
************

你可以为路由命名以使你的应用更健壮。这为路由应用一个名称，之后可以被调用，即使路由定义发生变化，应用中所有使用 :php:func:`url_to()` 构建的链接仍能正常工作，而无需你做任何修改。通过传递 ``as`` 选项并指定路由名称来为路由命名：

.. literalinclude:: routing/030.php

这样做还有一个额外的好处，就是让视图更具可读性。

.. note:: 默认情况下，所有定义的路由都有与其路径匹配的名称，其中占位符被相应的正则表达式替换。例如，如果你定义一个路由如 ``$routes->get('edit/(:num)', 'PostController::edit/$1');``，你可以使用 ``route_to('edit/([0-9]+)', 12)`` 生成相应的 URL。

.. warning:: 根据 :ref:`routing-priority`，如果首先定义了一个未命名的路由 (例如 ``$routes->get('edit', 'PostController::edit');``），然后定义了另一个命名路由，其名称与第一个路由的路径相同 (例如 ``$routes->get('edit/(:num)', 'PostController::edit/$1', ['as' => 'edit']);``），第二个路由将不会被注册，因为它的名称会与第一个路由的自动分配名称冲突。

分组路由
***************

你可以使用 ``group()`` 方法将路由分组到一个共用名称下。分组名称会成为出现在组内定义路由之前的一个路径段。这允许你减少构建大量共享相同开头字符串的路由所需的输入量，例如在构建管理区域时：

.. literalinclude:: routing/023.php

这将会为 **users** 和 **blog** URI 添加 **admin** 前缀，处理如 **admin/users** 和 **admin/blog** 的 URL。

设置命名空间
=================

如果你需要为分组分配选项，例如 :ref:`assigning-namespace`，请在回调函数之前进行设置：

.. literalinclude:: routing/024.php

这将处理指向 ``App\API\v1\Users`` 控制器的资源路由，对应的 URI 为 **api/users**。

设置过滤器
===============

你也可以为一组路由使用特定的 :doc:`过滤器 <filters>`。这将在控制器之前或之后始终运行该过滤器。这在身份验证或 API 日志记录场景中特别有用：

.. literalinclude:: routing/025.php

过滤器的值必须与 **app/Config/Filters.php** 中定义的别名之一匹配。

.. note:: 在 v4.5.4 之前的版本中，由于存在 bug，传递给 ``group()`` 的过滤器不会合并到传递给内部路由的过滤器中。

设置其他选项
=====================

有时可能需要为路由组应用过滤器或其他配置选项（如命名空间、子域等），而无需添加前缀。此时可将前缀设为空字符串：

.. literalinclude:: routing/027.php

.. _routing-nesting-groups:

嵌套分组
==============

支持多层级分组以实现更精细的组织结构：

.. literalinclude:: routing/026.php

此例将处理 **admin/users/list** URL。外层 ``group()`` 的 ``filter`` 选项会与内层 ``group()`` 的选项合并。上述代码中，``admin`` 路由运行 ``myfilter1:config`` 过滤器，``admin/users/list`` 路由运行 ``myfilter1:config`` 和 ``myfilter2:region`` 过滤器。

.. note:: v4.6.0 之前，同一过滤器无法使用不同参数多次运行。

内层 ``group()`` 的选项会覆盖外层同名选项。

.. note:: v4.5.0 之前存在 bug，外层 ``group()`` 的选项不会与内层合并。

.. _routing-priority:

路由优先级
**************

路由按定义顺序注册到路由表中。当访问 URI 时，将执行首个匹配的路由。

.. warning:: 若同一路由路径被多次定义且处理器不同，仅首个定义的路由生效。

可通过运行 :ref:`spark routes <routing-spark-routes>` 命令查看路由表。

调整路由优先级
=======================

处理模块路由时，若应用路由包含通配符可能导致模块路由无法正确处理。通过 ``priority`` 选项可降低路由处理优先级（数值越大优先级越低）：

.. literalinclude:: routing/043.php

要禁用此功能，传入 ``false`` 参数：

.. literalinclude:: routing/044.php

.. note:: 默认所有路由优先级为 0，负值将转为绝对值。

.. _routes-configuration-options:

路由配置选项
****************************

RouteCollection 类提供多个全局配置选项（位于 **app/Config/Routing.php**），可根据需求调整。

.. note:: **app/Config/Routing.php** 配置文件自 v4.4.0 起新增，旧版本需在 **app/Config/Routes.php** 使用 setter 方法修改设置。

.. _routing-default-namespace:

默认命名空间
=================

匹配控制器时，系统会将默认命名空间值添加到控制器名称前（默认 ``App\Controllers``）。设为空字符串（``''``）则需每个路由指定完全限定命名空间：

.. literalinclude:: routing/045.php

若控制器已命名空间化，可修改此值减少输入：

.. literalinclude:: routing/046.php

.. _routing-default-method:

默认方法
==============

当路由处理器仅指定控制器名时，使用此设置的方法（默认 ``index``）：
::

    // In app/Config/Routing.php
    public string $defaultMethod = 'index';

.. note:: ``$defaultMethod`` 也常用于自动路由。
    请参见 :ref:`自动路由（改进版） <routing-auto-routing-improved-default-method>`
    或 :ref:`自动路由（传统版） <routing-auto-routing-legacy-default-method>`。

如果你定义了以下路由::

    $routes->get('/', 'Home');

当路由匹配时，将执行 ``App\Controllers\Home`` 控制器的 ``index()`` 方法。

.. note:: 方法名称以 ``_`` 开头时不能用作默认方法。
    但是，从 v4.5.0 开始，允许使用 ``__invoke`` 方法。

转换 URI 短横线
====================

此选项在自动路由中将短横线（``-``）自动转为下划线（因短横线非有效类/方法名字符）：

.. literalinclude:: routing/049.php

.. note:: 在使用自动路由（改进版）时，在 v4.4.0 之前，如果 ``$translateURIDashes`` 为 true，两个 URI 对应一个控制器方法，一个 URI 用于破折号（例如 **foo-bar**），另一个 URI 用于下划线（例如 **foo_bar**）。这是错误的行为。从 v4.4.0 开始，下划线的 URI（**foo_bar**）不可访问。

.. _use-defined-routes-only:

仅使用定义路由
=======================

v4.2.0 起默认禁用自动路由。

当未找到与当前 URI 匹配的定义路由时，系统尝试通过自动路由匹配控制器方法。将 ``$autoRoute`` 设为 ``false`` 可完全禁用自动路由：

.. literalinclude:: routing/050.php

.. warning:: 启用 :doc:`CSRF 保护 </libraries/security>` 时，**GET** 请求不受保护。若 URI 可通过 GET 访问，CSRF 保护将失效。

.. _404-override:

404 重写
============

当找不到与当前 URI 匹配的页面时，系统将显示一个通用的 404 页面。通过在路由配置文件中使用 ``$override404`` 属性，你可以为 404 路由定义控制器类/方法。

.. literalinclude:: routing/051.php

你还可以在路由配置文件中使用 ``set404Override()`` 方法指定在发生 404 错误时执行的操作。该值可以是一个有效的类/方法对，或者是一个闭包：

.. literalinclude:: routing/069.php

.. note:: 从 v4.5.0 开始，404 覆盖功能默认将响应状态代码设置为 ``404``。在之前的版本中，状态代码是 ``200``。
    如果你想在控制器中更改状态代码，请参见 :php:meth:`CodeIgniter\\HTTP\\Response::setStatusCode()` 获取有关如何设置状态代码的信息。

按优先级处理路由
============================

启用或禁用按优先级处理路由队列。在路由选项中降低优先级。默认禁用。
此功能影响所有路由。有关降低优先级的示例用法，请参阅 :ref:`routing-priority`：

.. literalinclude:: routing/052.php

.. _multiple-uri-segments-as-one-parameter:

多 URI 段作为单一参数
======================================

.. versionadded:: 4.5.0

启用此选项后，匹配多段的占位符（如 ``(:any)``）将作为单一参数传递（即使包含斜杠）：

.. literalinclude:: routing/070.php

例如路由：

.. literalinclude:: routing/010.php

将匹配 **product/123**、**product/123/456**、**product/123/456/789** 等等。
如果 URI 是 **product/123/456**，``123/456`` 将被传递给 ``Catalog::productLookup()`` 方法的第一个参数。

自动路由（改进版）
***********************

.. versionadded:: 4.2.0

这是更安全的新自动路由系统，详见 :doc:`auto_routing_improved`。

.. _auto-routing-legacy:

自动路由（传统版）
*********************

.. important:: 这个功能只为了向后兼容而存在。在新项目中不要使用它。即使你已经在使用它，我们也推荐你使用 :ref:`auto-routing-improved` 替代。

自动路由(传统)是来自 CodeIgniter 3 的路由系统。它可以根据约定自动路由 HTTP 请求,并执行相应的控制器方法。

推荐在 **app/Config/Routes.php** 文件中定义所有路由,或者使用 :ref:`auto-routing-improved`。

.. warning:: 为了防止配置错误和编码错误,我们建议你不要使用自动路由(传统)功能。很容易创建容易受攻击的应用程序,其中控制器过滤器或 CSRF 保护被绕过。

.. important:: 自动路由(传统)会将任何 HTTP 方法的 HTTP 请求路由到控制器方法。

启用传统自动路由
============================

自 v4.2.0 起，默认禁用自动路由。

要使用它,你需要在 **app/Config/Routing.php** 中将 ``$autoRoute`` 选项设置为 ``true``::

    public bool $autoRoute = true;

并且在 **app/Config/Feature.php** 中，将属性 ``$autoRoutesImproved`` 设置为 ``false``::

    public bool $autoRoutesImproved = false;

URI 分段（传统版）
=====================

遵循模型-视图-控制器（MVC）模式，URL 中的各段通常表示::

    example.com/class/method/ID

1. 第一段表示应被调用的控制器 **class**
2. 第二段表示应被调用的类 **method**
3. 第三段及后续各段表示将传递给控制器的 ID 和其他变量

考虑以下 URI::

    example.com/index.php/helloworld/index/1

在上述示例中，CodeIgniter 将尝试查找名为 **Helloworld.php** 的控制器，并执行 ``index()`` 方法，同时传递 ``'1'`` 作为第一个参数。

更多信息请参阅 :ref:`控制器中的自动路由(传统模式) <controller-auto-routing-legacy>`。

.. _routing-auto-routing-legacy-configuration-options:

配置选项（传统版）
==============================

这些选项在 **app/Config/Routing.php** 文件中可用。

默认控制器(传统版)
---------------------------

针对网站根 URI(传统版)
^^^^^^^^^^^^^^^^^^^^^^^^^^

当用户访问你网站的根（例如，**example.com**）时，除非存在明确的路由，否则将根据 ``$defaultController`` 属性设定的值来确定要使用的控制器。

对于这个属性，默认值是 ``Home``，它匹配在 **app/Controllers/Home.php** 的控制器::

    public string $defaultController = 'Home';

针对目录 URI(传统版)
^^^^^^^^^^^^^^^^^^^^^^^^^^

默认控制器也在未找到匹配的路由且 URI 指向控制器目录中的目录时使用。例如,如果用户访问 **example.com/admin**,如果在 **app/Controllers/Admin/Home.php** 中找到了一个控制器,则会使用它。

更多信息请参阅 :ref:`控制器中的自动路由(传统) <controller-auto-routing-legacy>`。

.. _routing-auto-routing-legacy-default-method:

默认方法（传统版）
-----------------------

这与默认控制器设置类似,但用于在找到与 URI 匹配的控制器但不存在方法段时确定使用的默认方法。默认值为 ``index``。

在此示例中,如果用户访问 **example.com/products**,且存在 ``Products`` 控制器,将执行 ``Products::listAll()`` 方法:

    public string $defaultMethod = 'listAll';

验证路由
*****************

通过 :doc:`spark 命令 </cli/spark_commands>` 查看所有路由：

.. _routing-spark-routes:

spark 路由
============

显示所有路由及过滤器：

.. code-block:: console

    php spark routes

输出示例：

.. code-block:: none

    +---------+---------+---------------+-------------------------------+----------------+---------------+
    | Method  | Route   | Name          | Handler                       | Before Filters | After Filters |
    +---------+---------+---------------+-------------------------------+----------------+---------------+
    | GET     | /       | »             | \App\Controllers\Home::index  |                | toolbar       |
    | GET     | feed    | »             | (Closure)                     |                | toolbar       |
    +---------+---------+---------------+-------------------------------+----------------+---------------+

*Method* 列显示路由监听的 HTTP 方法。

*Route* 列显示要匹配的路由路径。定义路由的路由以正则表达式表示。

自 v4.3.0 起, *Name* 列显示路由名称。``»`` 表示名称与路由路径相同。

.. important:: 系统并非完美。对于包含如 ``([^/]+)`` 或 ``{locale}`` 的正则表达式模式的路由，显示的 *Filters* 可能不正确（如果你在 **app/Config/Filters.php** 中为过滤器设置了复杂的 URI 模式），或者它显示为 ``<unknown>``。

    :ref:`spark filter:check <spark-filter-check>` 命令可以用来检查 100% 准确的过滤器。

自动路由(改进版)
-----------------------

当你使用自动路由(改进版)时,输出类似以下内容:

.. code-block:: none

    +-----------+-------------------------+---------------+-----------------------------------+----------------+---------------+
    | Method    | Route                   | Name          | Handler                           | Before Filters | After Filters |
    +-----------+-------------------------+---------------+-----------------------------------+----------------+---------------+
    | GET(auto) | product/list/../..[/..] |               | \App\Controllers\Product::getList |                | toolbar       |
    +-----------+-------------------------+---------------+-----------------------------------+----------------+---------------+

*Method* 将显示为 ``GET(auto)``。

*Route* 列中的 ``/..`` 表示一个段。``[/..]`` 表示可选。

.. note:: 当启用自动路由并且你有 ``home`` 路由时,它也可以通过 ``Home`` 访问,或者通过 ``hOme``、``hoMe``、``HOME`` 等访问,但是该命令只会显示 ``home``。

如果你看到以 ``x`` 开头的路由,如下所示,这表示一个无效路由,不会路由,但是控制器有公共方法进行路由。

.. code-block:: none

    +-----------+----------------+------+-------------------------------------+----------------+---------------+
    | Method    | Route          | Name | Handler                             | Before Filters | After Filters |
    +-----------+----------------+------+-------------------------------------+----------------+---------------+
    | GET(auto) | x home/foo     |      | \App\Controllers\Home::getFoo       | <unknown>      | <unknown>     |
    +-----------+----------------+------+-------------------------------------+----------------+---------------+

上面的示例显示你有 ``\App\Controllers\Home::getFoo()`` 方法,但是它没有路由,因为它是默认控制器(默认为 ``Home``),默认控制器名称必须在 URI 中省略。你应该删除 ``getFoo()`` 方法。

.. note:: 在 v4.3.4 之前,由于一个错误,无效路由会显示为正常路由。

自动路由(传统)
---------------------

当你使用自动路由(传统)时,输出类似以下内容:

.. code-block:: none

    +--------+--------------------+---------------+-----------------------------------+----------------+---------------+
    | Method | Route              | Name          | Handler                           | Before Filters | After Filters |
    +--------+--------------------+---------------+-----------------------------------+----------------+---------------+
    | auto   | product/list[/...] |               | \App\Controllers\Product::getList |                | toolbar       |
    +--------+--------------------+---------------+-----------------------------------+----------------+---------------+

*Method* 将显示为 ``auto``。

*Route* 列中的 ``[/...]`` 表示任意数量的段。

.. note:: 当启用自动路由并且你有 ``home`` 路由时,它也可以通过 ``Home`` 访问,或者通过 ``hOme``、``hoMe``、``HOME`` 等访问,但是该命令只会显示 ``home``。

.. _routing-spark-routes-sort-by-handler:

按处理程序排序
---------------

.. versionadded:: 4.3.0

你可以按 *Handler* 对路由进行排序:

.. code-block:: console

    php spark routes -h

.. _routing-spark-routes-specify-host:

指定主机
------------

.. versionadded:: 4.4.0

通过 ``--host`` 指定请求主机：

.. code-block:: console

    php spark routes --host accounts.example.com

获取路由信息
***************************

在 CodeIgniter 4 中，理解和管理路由信息对于有效处理 HTTP 请求至关重要。这涉及到检索有关活动控制器和方法的详细信息，以及应用于特定路由的过滤器。下面，我们探讨如何访问这些路由信息，以帮助完成诸如日志记录、调试或实现条件逻辑等任务。

检索当前控制器/方法名称
==============================================

在某些情况下，你可能需要确定当前 HTTP 请求触发了哪个控制器和方法。这对于日志记录、调试或基于活动控制器方法的条件逻辑非常有用。

CodeIgniter 4 提供了一种简单的方法来使用 ``Router`` 类访问当前路由的控制器和方法名称。以下是一个示例：

.. literalinclude:: routing/071.php

当你需要动态地与控制器交互或记录处理特定请求的方法时，这个功能特别有用。

获取当前路由的活动过滤器
============================================

:doc:`过滤器 <filters>` 是一个强大的功能，使你能够在处理 HTTP 请求之前或之后执行诸如身份验证、日志记录和安全检查等操作。要访问特定路由的活动过滤器，你可以使用 ``Router`` 类中的 :php:meth:`CodeIgniter\\Router\\Router::getFilters()` 方法。

此方法返回当前正在处理的路由的活动过滤器列表：

.. literalinclude:: routing/072.php

.. note:: ``getFilters()`` 方法仅返回为特定路由定义的过滤器。
     它不包括全局过滤器或在 **app/Config/Filters.php** 文件中指定的过滤器。

获取当前路由的匹配路由选项
===================================================

当我们定义路由时，它们可能具有可选参数：``filter``、``namespace``、``hostname``、``subdomain``、``offset``、``priority``、``as``。所有这些参数都已在上面详细描述过。
另外，如果我们使用 ``addRedirect()``，我们还可以期待 ``redirect`` 键。
要访问这些参数的值，我们可以调用 ``Router::getMatchedRouteOptions()``。以下是返回数组的示例：

.. literalinclude:: routing/074.php
