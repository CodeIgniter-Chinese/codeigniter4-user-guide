###########
URI 路由
###########

.. contents::
    :local:
    :depth: 3

什么是 URI 路由？
********************

URI 路由将 URI 与控制器的方法关联起来。

CodeIgniter 有两种路由方式：**定义路由** 和 **自动路由**。
使用定义路由，可以手动定义路由，从而实现灵活的 URL。
自动路由根据约定，自动路由 HTTP 请求并执行相应的控制器方法，无需手动定义路由。

首先介绍定义路由。如需使用自动路由，请参阅 :ref:`auto-routing-improved`。

.. _defined-route-routing:

设置路由规则
*********************

路由规则定义在 **app/Config/Routes.php** 文件中。在该文件中，你会看到它创建了一个 RouteCollection 类的实例（``$routes``），允许你指定自己的路由规则。路由可以使用占位符或正则表达式来定义。

定义路由时，需要选择与 HTTP 方法（请求方法）对应的方法。如果预期接收 GET 请求，使用 ``get()`` 方法：

.. literalinclude:: routing/001.php

路由接收左侧的 **路由路径**（相对于 BaseURL 的 URI 路径，``/``），并将其映射到右侧的 **路由处理程序**（控制器和方法 ``Home::index``），同时传递应传递给控制器的任何参数。

控制器和方法的列出方式应与使用静态方法的方式相同，即用双冒号分隔类和方法，如 ``Users::list``。

如果该方法需要传递参数，则在方法名之后列出参数，用正斜杠分隔：

.. literalinclude:: routing/002.php

示例
========

以下是一些基本的路由示例。

URL 第一段包含 **journals** 单词，将映射到 ``\App\Controllers\Blogs`` 类和 :ref:`默认方法 <routing-default-method>`（通常为 ``index()``）：

.. literalinclude:: routing/006.php

URL 包含 **blog/joe** 段，将映射到 ``\App\Controllers\Blogs`` 类和 ``users()`` 方法。ID 将被设置为 ``34``：

.. literalinclude:: routing/007.php

URL 以 **product** 作为第一段，第二段为任意内容，将映射到 ``\App\Controllers\Catalog`` 类和 ``productLookup()`` 方法：

.. literalinclude:: routing/008.php

URL 以 **product** 作为第一段，第二段为数字，将映射到 ``\App\Controllers\Catalog`` 类和 ``productLookupByID()`` 方法，将匹配结果作为变量传递给方法：

.. literalinclude:: routing/009.php

.. _routing-http-verb-routes:

HTTP 方法路由
================

可以使用任何标准 HTTP 方法（GET、POST、PUT、DELETE、OPTIONS 等）：

.. literalinclude:: routing/003.php

可以通过将多个方法作为数组传递给 ``match()`` 方法来指定路由应匹配的多个方法：

.. literalinclude:: routing/004.php

指定路由处理程序
=========================

.. _controllers-namespace:

控制器的命名空间
----------------------

当以字符串形式指定控制器和方法名时，如果控制器名称未以 ``\`` 开头，系统会自动添加 :ref:`routing-default-namespace`：

.. literalinclude:: routing/063.php

如果开头有 ``\``，则被视为完全限定的类名：

.. literalinclude:: routing/064.php

也可以使用 ``namespace`` 选项指定命名空间：

.. literalinclude:: routing/038.php

详情请参阅 :ref:`assigning-namespace`。

数组可调用语法
---------------------

.. versionadded:: 4.2.0

自 v4.2.0 起，可以使用数组可调用语法指定控制器：

.. literalinclude:: routing/013.php
   :lines: 2-

或使用 ``use`` 关键字：

.. literalinclude:: routing/014.php
   :lines: 2-

如果忘记添加 ``use App\Controllers\Home;``，控制器类名将被解释为 ``\Home``，而不是 ``App\Controllers\Home``。

.. note:: 使用数组可调用语法时，类名始终被解释为完全限定的类名。因此 :ref:`routing-default-namespace` 和 :ref:`命名空间选项 <assigning-namespace>` 不会生效。

数组可调用语法与占位符
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果存在占位符，将自动按指定顺序设置参数：

.. literalinclude:: routing/015.php
   :lines: 2-

但是，如果在路由中使用正则表达式，自动配置的参数可能不正确。在这种情况下，可以手动指定参数：

.. literalinclude:: routing/016.php
   :lines: 2-

使用闭包
--------------

可以使用匿名函数（即闭包）作为路由映射的目标。当用户访问该 URI 时将执行此函数。这对于快速执行小任务或仅显示简单视图非常方便：

.. literalinclude:: routing/020.php

指定路由路径
======================

占位符
------------

典型路由如下所示：

.. literalinclude:: routing/005.php

在路由中，第一个参数是待匹配的 URI，第二个参数是目标路由。在上面的示例中，如果在 URL 路径的第一段找到 "product"，并在第二段找到数字，则使用 ``Catalog`` 类和 ``productLookup`` 方法。

占位符只是表示正则表达式模式的字符串。在路由过程中，这些占位符被正则表达式的值替换。它们主要用于提高可读性。

以下是可用的占位符：

============ ===========================================================================================================
占位符       描述
============ ===========================================================================================================
(:any)       匹配从该位置到 URI 结尾的所有字符。可能包含多个 URI 段。
(:segment)   匹配除正斜杠（``/``）以外的任何字符，将结果限制为单个段。
(:num)       匹配任意正整数。
(:alpha)     匹配任意字母字符串
(:alphanum)  匹配任意字母数字字符串或整数，或两者的任意组合。
(:hash)      与 ``(:segment)`` 相同，但可用于轻松查看哪些路由使用哈希 ID。
============ ===========================================================================================================

.. note:: ``{locale}`` 不能用作占位符或路由的其他部分，因为它保留用于 :doc:`本地化 </outgoing/localization>`。

.. _routing-placeholder-any:

(:any) 的行为
^^^^^^^^^^^^^^^^^^^^^^

注意，单个 ``(:any)`` 将在 URL 中匹配多个段（如果存在）。

例如路由：

.. literalinclude:: routing/010.php

将匹配 **product/123**、**product/123/456**、**product/123/456/789** 等。

默认情况下，在上面的示例中，如果 ``$1`` 占位符包含斜杠（``/``），在传递给 ``Catalog::productLookup()`` 时仍会被拆分为多个参数。

.. note:: 自 v4.5.0 起，可以通过配置选项更改此行为。
    详情请参阅 :ref:`multiple-uri-segments-as-one-parameter`。

控制器中的实现应考虑最大参数数量：

.. literalinclude:: routing/011.php

或者可以使用 `可变数量的参数值列表 <https://www.php.net/manual/zh/functions.arguments.php#functions.variable-arg-list>`_：

.. literalinclude:: routing/068.php

.. important:: 不要在 ``(:any)`` 之后放置任何占位符，因为传递给控制器方法的参数数量可能会改变。

如果匹配多个段不是预期的行为，在定义路由时应使用 ``(:segment)``。使用上面的示例 URL：

.. literalinclude:: routing/012.php

将仅匹配 **product/123**，其他情况返回 404 错误。

自定义占位符
-------------------

可以创建自己的占位符，用于路由文件以完全自定义体验和可读性。

使用 ``addPlaceholder()`` 方法添加新占位符。第一个参数是用作占位符的字符串，第二个参数是应替换它的正则表达式模式。需在添加路由前调用：

.. literalinclude:: routing/017.php

正则表达式
-------------------

如果愿意，可以使用正则表达式定义路由规则。允许任何有效的正则表达式，也支持反向引用。

.. important:: 注意：如果使用反向引用，必须使用美元符号语法而不是双反斜杠语法。典型的正则表达式路由如下所示：

    .. literalinclude:: routing/018.php

在上面的示例中，类似于 **products/shirts/123** 的 URI 将改为调用 ``Products`` 控制器类的 ``show()`` 方法，并将原始第一段和第二段作为参数传递给它。

使用正则表达式，还可以捕获包含正斜杠（``/``）的段，这通常代表多个段之间的分隔符。

例如，如果用户访问 Web 应用程序的密码保护区域，并且希望在登录后将其重定向回同一页面，可能会发现此示例很有用：

.. literalinclude:: routing/019.php

默认情况下，在上面的示例中，如果 ``$1`` 占位符包含斜杠（``/``），在传递给 ``Auth::login()`` 时仍会被拆分为多个参数。

.. note:: 自 v4.5.0 起，可以通过配置选项更改此行为。
    详情请参阅 :ref:`multiple-uri-segments-as-one-parameter`。

对于不了解正则表达式但想了解更多内容的人，`regular-expressions.info <https://www.regular-expressions.info/>`_ 可能是一个不错的起点。

.. note:: 还可以将占位符与正则表达式混合使用。

.. _view-routes:

视图路由
===========

.. versionadded:: 4.3.0

如果只想渲染一个没有关联逻辑的视图，可以使用 ``view()`` 方法。此方法始终视为 GET 请求。该方法接受要加载的视图名称作为第二个参数。

.. literalinclude:: routing/065.php

如果在路由中使用占位符，可以在视图中的特殊变量 ``$segments`` 内访问它们。它们以数组形式可用，按它们在路由中出现的顺序索引。

.. literalinclude:: routing/066.php

.. _redirecting-routes:

重定向路由
==================

任何存在足够长时间的网站必然会有页面发生迁移。可以使用 ``addRedirect()`` 方法指定应重定向到其他路由的路由。第一个参数是旧路由的 URI 模式。第二个参数是要重定向到的新 URI 或命名路由的名称。第三个参数是应随重定向一起发送的 HTTP 状态码。默认值为 ``302``，这是临时重定向，在大多数情况下推荐使用：

.. literalinclude:: routing/022.php

.. note:: 自 v4.2.0 起，``addRedirect()`` 可以使用占位符。

如果在页面加载期间匹配到重定向路由，用户将立即重定向到新页面，然后才会加载控制器。

环境限制
========================

可以创建仅在特定环境中可见的路由集。用于创建仅在开发人员本地机器上可用，而测试或生产服务器上无法访问的工具。可以使用 ``environment()`` 方法。第一个参数是环境名称。此闭包内定义的任何路由只能从给定环境访问：

.. literalinclude:: routing/028.php

任意 HTTP 方法的路由
==========================

.. important:: 此方法仅出于向后兼容而存在。不要在新项目中使用。即使已经在使用，也建议使用更合适的 HTTP 方法路由。

.. warning:: 虽然 ``add()`` 方法看起来很方便，但建议始终使用上述基于 HTTP 方法的路由，因为它更安全。如果使用 :doc:`CSRF 保护 </libraries/security>`，它不会保护 **GET** 请求。如果 ``add()`` 方法中指定的 URI 可以通过 GET 方法访问，CSRF 保护将无法工作。

使用 ``add()`` 方法定义支持任意 HTTP 方法的路由：

.. literalinclude:: routing/031.php

.. note:: 使用基于 HTTP 方法的路由还会提供轻微的性能提升，因为只存储与当前请求方法匹配的路由，从而在尝试查找匹配时需要扫描的路由更少。

批量映射路由
=======================

.. important:: 此方法仅出于向后兼容而存在。不要在新项目中使用。即使已经在使用，也建议使用更合适的 HTTP 方法路由。

.. warning:: ``map()`` 方法也不推荐使用，因为它在内部调用 ``add()``。

虽然 ``add()`` 方法简单易用，但使用 ``map()`` 方法同时处理多个路由通常更方便。可以定义路由数组，然后将其作为第一个参数传递给 ``map()`` 方法，而不是为每个需要添加的路由调用 ``add()`` 方法：

.. literalinclude:: routing/021.php

.. _command-line-only-routes:

仅命令行路由
========================

.. note:: 建议使用 Spark 命令处理 CLI 脚本，而不是通过 CLI 调用控制器。
    有关详细信息，请参阅 :doc:`../cli/cli_commands` 页面。

通过 HTTP 方法创建的路由在 CLI 中不可访问，但由 ``add()`` 方法创建的路由仍可从命令行使用。

可以使用 ``cli()`` 方法创建仅在命令行中工作，且无法从 Web 浏览器访问的路由：

.. literalinclude:: routing/032.php

.. warning:: 如果启用 :ref:`auto-routing-legacy` 并将命令文件放在 **app/Controllers** 中，任何人都可以通过自动路由（传统）通过 HTTP 访问该命令。

全局选项
**************

创建路由的所有方法（``get()``、``post()``、:doc:`resource() <restful>` 等）都可以接受一个选项数组，这些选项可以修改生成的路由或进一步限制它们。``$options`` 数组始终是最后一个参数：

.. literalinclude:: routing/033.php

.. _applying-filters:

应用过滤器
================

可以通过提供在控制器之前或之后运行的过滤器，来修改特定路由的行为。这在身份验证或 API 日志记录期间特别方便。

过滤器的值可以是字符串或字符串数组：

* 匹配 **app/Config/Filters.php** 中定义的别名
* 过滤器类名

有关定义别名的更多信息，请参阅 :ref:`控制器过滤器 <filters-aliases>`。

.. warning:: 如果在 **app/Config/Routes.php** 中设置路由的过滤器（而不是在 **app/Config/Filters.php** 中），建议禁用自动路由（传统）。启用 :ref:`auto-routing-legacy` 时，控制器可能通过与配置的路由不同的 URL 访问，在这种情况下，指定给路由的过滤器将不会应用。请参阅 :ref:`use-defined-routes-only` 以禁用自动路由。

别名过滤器
------------

为过滤器值指定 :ref:`在 app/Config/Filters.php 中定义 <filters-aliases>` 的别名：

.. literalinclude:: routing/034.php

还可以提供要传递给别名过滤器的 ``before()`` 和 ``after()`` 方法的参数：

.. literalinclude:: routing/035.php

类名过滤器
----------------

.. versionadded:: 4.1.5

可以为过滤器值指定过滤器类名：

.. literalinclude:: routing/036.php

.. _multiple-filters:

多重过滤器
----------------

.. versionadded:: 4.1.5

.. important:: 自 v4.5.0 起，*多重过滤器* 始终处于启用状态。在 v4.5.0 之前，*多重过滤器* 默认禁用。如果要在 v4.5.0 之前使用，请参阅 :ref:`从 4.1.4 升级到 4.1.5 <upgrade-415-multiple-filters-for-a-route>` 了解详情。

可以为过滤器值指定数组：

.. literalinclude:: routing/037.php

过滤器参数
^^^^^^^^^^^^^^^^

可以向过滤器传递额外的参数：

.. literalinclude:: routing/067.php

在此示例中，数组 ``['dual', 'noreturn']`` 将作为 ``$arguments`` 传递给过滤器的 ``before()`` 和 ``after()`` 方法。

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

也可以限制多个主机名，例如：

.. literalinclude:: routing/073.php

限制子域
===================

当存在 ``subdomain`` 选项时，系统将限制路由仅在该子域上可用。只有当子域是查看应用程序所使用的子域时，路由才会匹配：

.. literalinclude:: routing/040.php

设置值为星号（``*``）可匹配任意子域，但无子域的 URL 不匹配：

.. literalinclude:: routing/041.php

.. important:: 此功能并非完美，在生产环境中使用之前应对特定域进行测试。大多数域应该可以正常工作，但一些边缘情况，特别是包含句点的域名（不用于分隔后缀或 www）可能导致误报。

偏移匹配的参数
=================================

可以使用 ``offset`` 选项通过任何数值偏移路由中的匹配参数，该值是偏移的段数。

这在开发 API 时可能很有益，因为第一段 URI 是版本号。当第一参数是语言字符串时也可以使用：

.. literalinclude:: routing/042.php

.. _reverse-routing:

反向路由
***************

反向路由允许通过控制器、方法及参数定义链接，并让路由器查找当前的路由。这使得修改路由定义无需更新应用代码。常用于在视图中创建链接。

例如，如果有一个想要链接到的照片库的路由，可以使用 :php:func:`url_to()` 辅助函数获取应使用的路由。第一个参数是完全限定的控制器和方法，用双冒号（``::``）分隔，就像编写初始路由本身一样。剩下的参数会传递给路由：

.. literalinclude:: routing/029.php

.. _using-named-routes:

命名路由
************

可以为路由命名以使应用程序更不易出错。这为路由分配了一个名称，可以稍后调用，即使路由定义更改，应用程序中使用 :php:func:`url_to()` 构建的所有链接仍将工作，而无需进行任何更改。通过传入带有路由名称的 ``as`` 选项来命名路由：

.. literalinclude:: routing/030.php

这样做还具有使视图更易读的附加好处。

.. note:: 默认情况下，所有定义的路由的名称都与其路径匹配，占位符替换为相应的正则表达式。例如，如果定义路由如 ``$routes->get('edit/(:num)', 'PostController::edit/$1');``，可以使用 ``route_to('edit/([0-9]+)', 12)`` 生成相应的 URL。

.. warning:: 根据 :ref:`routing-priority`，如果首先定义了一个未命名的路由（例如 ``$routes->get('edit', 'PostController::edit');``），然后定义了另一个与第一个路由路径相同名称的路由（例如 ``$routes->get('edit/(:num)', 'PostController::edit/$1', ['as' => 'edit']);``），第二个路由将不会被注册，因为它的名称会与第一个路由自动分配的名称冲突。

分组路由
***************

可以使用 ``group()`` 方法将路由分组到一个共用名称下。该组名称会成为一个 URI 段，显示在该组内定义的路由之前。这使你能够减少创建大量共享相同起始字符串的路由所需的输入，例如在构建管理后台时：

.. literalinclude:: routing/023.php

这将为 **users** 和 **blog** URI 添加 **admin** 前缀，处理如 **admin/users** 和 **admin/blog** 的 URL。

设置命名空间
=================

如果需要为组分配选项，如 :ref:`assigning-namespace`，请在回调之前执行：

.. literalinclude:: routing/024.php

这将处理到 ``App\API\v1\Users`` 控制器的资源路由，URI 为 **api/users**。

设置过滤器
===============

你也可以为一组路由使用特定的 :doc:`过滤器 <filters>`。过滤器总是在控制器之前或之后运行。这个功能在身份验证或 API 日志记录时特别方便：

.. literalinclude:: routing/025.php

过滤器的值必须与 **app/Config/Filters.php** 中定义的别名之一匹配。

.. note:: 在 v4.5.4 之前，由于一个 Bug，传递给 ``group()`` 的过滤器不会合并到传递给内部路由的过滤器中。

设置其他选项
=====================

在某些情况下，你可能希望把一些路由分组，以便统一应用过滤器，或其他路由配置选项（如命名空间、子域名等）。
如果你并不需要为这个分组添加 URI 前缀，可以在定义分组时将前缀设为空字符串。这样，分组中的路由在访问路径上看起来就像这个分组不存在一样，但仍然会应用该分组中设置的路由配置选项：

.. literalinclude:: routing/027.php

.. _routing-nesting-groups:

嵌套分组
==============

支持多层级分组以实现更精细的组织结构：

.. literalinclude:: routing/026.php

这段配置将会处理 **admin/users/list** 这个 URL。

传递给外层 ``group()`` 的 ``filter`` 选项，会与内层 ``group()`` 中的 ``filter`` 选项合并生效。
因此，上面的代码中，对于 ``admin`` 这个路由，只会执行 ``myfilter1:config``。对于 ``admin/users/list`` 这个路由，则会同时执行 ``myfilter1:config`` 和 ``myfilter2:region``。

.. note:: 在 v4.6.0 之前，同一个过滤器不能以不同的参数被多次执行。

对于其他存在重叠的配置项，如果在内层 ``group()`` 中传入了新的值，那么这些值会覆盖外层 ``group()`` 中对应的设置。

.. note:: 在 v4.5.0 之前，由于一个 Bug，外层 ``group()``` 中传入的选项不会与内层 ``group()``` 的选项进行合并。

.. _routing-priority:

路由优先级
**************

路由按照定义的顺序注册到路由表中。这意味着访问 URI 时，将执行第一个匹配的路由。

.. warning:: 如果路由路径被多次定义且处理程序不同，仅首个定义的路由生效。

可以通过运行 :ref:`spark routes <routing-spark-routes>` 命令来检查路由表中注册的路由。

调整路由优先级
=======================

在使用模块时，如果应用程序中的路由包含通配符，可能会出现问题。
然后模块路由将无法正确处理。
你可以通过使用 ``priority`` 选项降低路由处理的优先级来解决此问题。
该参数接受正整数和零。在 ``priority`` 中指定的数字越大，处理队列中的路由优先级越低：

.. literalinclude:: routing/043.php

要禁用此功能，必须使用参数 ``false`` 调用该方法：

.. literalinclude:: routing/044.php

.. note:: 默认情况下，所有路由的优先级均为 0。
    负整数将强制转换为绝对值。

.. _routes-configuration-options:

路由配置选项
****************************

RoutesCollection 类提供了几个影响所有路由的选项，可以进行修改以满足你的应用程序的需求。
这些选项在 **app/Config/Routing.php** 中可用。

.. note:: 配置文件 **app/Config/Routing.php** 自 v4.4.0 起添加。
    在以前的版本中，在 **app/Config/Routes.php** 中使用 setter 方法来更改设置。

.. _routing-default-namespace:

默认命名空间
=================

将控制器与路由匹配时，系统会将默认命名空间值添加到控制器名称前面。
默认情况下，此值为 ``App\Controllers``。

如果将值设置为空字符串（``''``），则让每个路由指定完整命名空间的控制器：

.. literalinclude:: routing/045.php

如果你的控制器未显式使用命名空间，则无需更改此项。
如果你为控制器使用了命名空间，则可以更改此值以减少输入：

.. literalinclude:: routing/046.php

.. _routing-default-method:

默认方法
==============

当路由处理程序只有控制器名称而没有列出方法名称时，使用此设置。
默认值为 ``index``。
::

    // In app/Config/Routing.php
    public string $defaultMethod = 'index';

.. note:: ``$defaultMethod`` 也与自动路由通用。
    请参阅 :ref:`自动路由（改进版）<routing-auto-routing-improved-default-method>`
    或 :ref:`自动路由（传统版）<routing-auto-routing-legacy-default-method>`。

如果你定义以下路由::

    $routes->get('/', 'Home');

当路由匹配时，将执行 ``App\Controllers\Home`` 控制器的 ``index()`` 方法。

.. note:: 不能使用以 ``_`` 开头的方法名称作为默认方法。
    但是，从 v4.5.0 开始，允许使用 ``__invoke`` 方法。

转换 URI 中的短横线
====================

该选项允许在使用自动路由时，自动将 URI 中的短横线（``-``）替换为控制器和方法名中的下划线，从而减少额外的路由定义。
这是因为短横线不是合法的类名或方法名字符，直接使用会导致致命错误：

.. literalinclude:: routing/049.php

.. note:: 使用自动路由（改进版）时，在 v4.4.0 之前，如果
    ``$translateURIDashes`` 为 true，带短横线（如 **foo-bar**）和带下划线（如 **foo_bar**）
    的两个 URI 会指向同一个控制器方法，这是不正确的行为。
    自 v4.4.0 起，带下划线的 URI（**foo_bar**）将无法访问。

.. _use-defined-routes-only:

仅使用已定义的路由
=======================

自 v4.2.0 起，自动路由默认被禁用。

当没有找到匹配的定义路由时，如果启用了自动路由，系统会尝试根据控制器和方法名进行匹配。

可以通过将 ``$autoRoute`` 设为 false，禁用这种自动匹配，从而仅允许访问已定义的路由：

.. literalinclude:: routing/050.php

.. warning:: 如果使用 :doc:`CSRF 保护 </libraries/security>`，它不会保护 **GET**
    请求。如果某个 URI 可通过 GET 方法访问，CSRF 保护将不会生效。

.. _404-override:

404 重写
============

当找不到与当前 URI 匹配的页面时，系统将显示一个通用的 404 视图。通过在路由配置文件中使用 ``$override404`` 属性，你可以为 404 路由定义控制器类/方法。

.. literalinclude:: routing/051.php

你还可以在路由配置文件中使用 ``set404Override()`` 方法指定在发生 404 错误时执行的操作。该值可以是一个有效的类/方法对，或者是一个闭包：

.. literalinclude:: routing/069.php

.. note:: 从 v4.5.0 开始，404 覆盖功能默认将响应状态码设置为 ``404``。
    在以前的版本中，状态码为 ``200``。
    如果要在控制器中更改状态码，请参阅
    :php:meth:`CodeIgniter\\HTTP\\Response::setStatusCode()` 了解如何设置状态码。

按优先级处理路由
============================

用于启用或禁用按优先级处理路由队列。降低优先级通过路由选项进行设置。
该功能默认禁用，并会影响所有路由。
降低优先级的示例请参见 :ref:`routing-priority`：

.. literalinclude:: routing/052.php

.. _multiple-uri-segments-as-one-parameter:

将多个 URI 分段作为一个参数
======================================

.. versionadded:: 4.5.0

启用此选项后，匹配多个段的占位符（例如 ``(:any)``）将直接作为一个参数传递，即使它包含多个段。

.. literalinclude:: routing/070.php

例如以下路由：

.. literalinclude:: routing/010.php

将匹配 **product/123**、**product/123/456**、**product/123/456/789** 等。
如果 URI 是 **product/123/456**，则 ``123/456`` 会作为第一个参数传递给 ``Catalog::productLookup()`` 方法。

自动路由（改进版）
***********************

.. versionadded:: 4.2.0

自动路由（改进版）是一套新的、更安全的自动路由系统。

有关详细信息，请参阅 :doc:`auto_routing_improved`。

.. _auto-routing-legacy:

自动路由（传统版）
*********************

.. important:: 该功能仅用于向后兼容。不要在新项目中使用。
    即使已经在使用，也强烈建议改用 :ref:`auto-routing-improved`。

自动路由（传统版）是 CodeIgniter 3 的路由系统。
可根据约定自动将 HTTP 请求路由到控制器方法。

建议在 **app/Config/Routes.php** 文件中定义所有路由，或使用 :ref:`auto-routing-improved`。

.. warning:: 为了防止配置错误和编码失误，强烈不建议使用自动路由（传统版）。它很容易导致控制器过滤器或 CSRF 保护被绕过，从而产生安全漏洞。

.. important:: 自动路由（传统版）会将 **任意** HTTP 方法的请求都路由到控制器方法。

启用自动路由（传统版）
============================

自 v4.2.0 起，默认情况下禁用自动路由。

要启用该功能，需要在 **app/Config/Routing.php** 中将 ``$autoRoute`` 设为 ``true``::

    public bool $autoRoute = true;

并在 **app/Config/Feature.php** 中将 ``$autoRoutesImproved`` 设为 ``false``::

    public bool $autoRoutesImproved = false;

URI 分段（传统版）
=====================

在遵循 MVC 模式时，URL 中的分段通常表示为::

    example.com/class/method/ID

1. 第一段表示要调用的控制器 **类**。
2. 第二段表示要调用的控制器 **方法**。
3. 第三段及后续段表示传递给控制器的 ID 或其他变量。

例如以下 URI::

    example.com/index.php/helloworld/index/1

在该示例中，CodeIgniter 会尝试找到名为 **Helloworld.php** 的控制器，并执行 ``index()`` 方法，同时将 ``'1'`` 作为第一个参数传入。

有关更多信息，请参阅 :ref:`控制器中的自动路由（传统版）<controller-auto-routing-legacy>`。

.. _routing-auto-routing-legacy-configuration-options:

配置选项（传统版）
==============================

这些选项定义在 **app/Config/Routing.php** 中。

默认控制器（传统版）
---------------------------

站点根 URI（传统版）
^^^^^^^^^^^^^^^^^^^^^^^^^^

当用户访问站点根目录（如 **example.com**）时，如果未显式定义路由，将使用 ``$defaultController`` 属性指定的控制器。

默认值为 ``Home``，对应控制器文件 **app/Controllers/Home.php**::

    public string $defaultController = 'Home';

目录 URI（传统版）
^^^^^^^^^^^^^^^^^^^^^^^^^^

当未找到匹配路由，且 URI 指向控制器目录中的某个子目录时，也会使用默认控制器。
例如访问 **example.com/admin**，如果存在 **app/Controllers/Admin/Home.php**，则会使用该控制器。

有关更多信息，请参阅 :ref:`控制器中的自动路由（传统版）<controller-auto-routing-legacy>`。

.. _routing-auto-routing-legacy-default-method:

默认方法（传统版）
-----------------------

该设置与默认控制器类似，用于在找到匹配控制器、但 URI 中未指定方法段时，确定要调用的默认方法。默认值为 ``index``。

在下面的示例中，如果用户访问 **example.com/products**，且存在 ``Products`` 控制器，则会执行 ``Products::listAll()`` 方法::

    public string $defaultMethod = 'listAll';

验证路由
*****************

CodeIgniter 提供了以下 :doc:`命令 </cli/spark_commands>` 用于显示所有路由。

.. _routing-spark-routes:

spark 路由
============

显示所有路由和过滤器：

.. code-block:: console

    php spark routes

输出示例如下：

.. code-block:: none

    +---------+---------+---------------+-------------------------------+----------------+---------------+
    | Method  | Route   | Name          | Handler                       | Before Filters | After Filters |
    +---------+---------+---------------+-------------------------------+----------------+---------------+
    | GET     | /       | »             | \App\Controllers\Home::index  |                | toolbar       |
    | GET     | feed    | »             | (Closure)                     |                | toolbar       |
    +---------+---------+---------------+-------------------------------+----------------+---------------+

*Method* 列表示路由监听的 HTTP 方法。

*Route* 列表示要匹配的路由路径。定义路由的路径会以正则表达式形式显示。

自 v4.3.0 起，*Name* 列显示路由名称。``»`` 表示路由名称与路径相同。

.. important:: 该系统并非完美。对于包含正则表达式（如 ``([^/]+)`` 或 ``{locale}``）的路由，如果在 **app/Config/Filters.php** 中为过滤器设置了复杂的 URI 模式，显示的 *Filters* 可能不正确，或显示为 ``<unknown>``。

    可以使用 :ref:`spark filter:check <spark-filter-check>` 命令检查 100% 准确的过滤器信息。

自动路由（改进版）
-----------------------

使用自动路由（改进版）时，输出示例如下：

.. code-block:: none

    +-----------+-------------------------+---------------+-----------------------------------+----------------+---------------+
    | Method    | Route                   | Name          | Handler                           | Before Filters | After Filters |
    +-----------+-------------------------+---------------+-----------------------------------+----------------+---------------+
    | GET(auto) | product/list/../..[/..] |               | \App\Controllers\Product::getList |                | toolbar       |
    +-----------+-------------------------+---------------+-----------------------------------+----------------+---------------+

*Method* 列会显示为 ``GET(auto)``。

*Route* 列中的 ``/..`` 表示一个分段。``[/..]`` 表示可选分段。

.. note:: 启用自动路由时，如果存在 ``home``` 路由，也可以通过 ``Home``、``hOme``、``hoMe``、``HOME``` 等方式访问，但命令输出中只会显示 ``home``。

如果看到以 ``x`` 开头的路由，表示该路由无效，不会被路由，但控制器中存在可路由的 public 方法。

.. code-block:: none

    +-----------+----------------+------+-------------------------------------+----------------+---------------+
    | Method    | Route          | Name | Handler                             | Before Filters | After Filters |
    +-----------+----------------+------+-------------------------------------+----------------+---------------+
    | GET(auto) | x home/foo     |      | \App\Controllers\Home::getFoo       | <unknown>      | <unknown>     |
    +-----------+----------------+------+-------------------------------------+----------------+---------------+

该示例表示存在 ``\App\Controllers\Home::getFoo()`` 方法，但由于它是默认控制器（默认为 ``Home``），默认控制器名称不能出现在 URI 中，因此不会被路由。应删除 ``getFoo()`` 方法。

.. note:: 在 v4.3.4 之前，由于一个 Bug，无效路由会被显示为普通路由。

自动路由（传统版）
---------------------

使用自动路由（传统版）时，输出示例如下：

.. code-block:: none

    +--------+--------------------+---------------+-----------------------------------+----------------+---------------+
    | Method | Route              | Name          | Handler                           | Before Filters | After Filters |
    +--------+--------------------+---------------+-----------------------------------+----------------+---------------+
    | auto   | product/list[/...] |               | \App\Controllers\Product::getList |                | toolbar       |
    +--------+--------------------+---------------+-----------------------------------+----------------+---------------+

*Method* 列会显示为 ``auto``。

*Route* 列中的 ``[/...]`` 表示任意数量的分段。

.. note:: 启用自动路由时，如果存在 ``home`` 路由，也可以通过 ``Home``、``hOme``、``hoMe``、``HOME``` 等方式访问，但命令输出中只会显示 ``home``。

.. _routing-spark-routes-sort-by-handler:

按处理程序排序
---------------

.. versionadded:: 4.3.0

可以按 *Handler* 对路由进行排序：

.. code-block:: console

    php spark routes -h

.. _routing-spark-routes-specify-host:

指定主机
------------

.. versionadded:: 4.4.0

可以使用 ``--host`` 选项，在请求 URL 中指定主机名：

.. code-block:: console

    php spark routes --host accounts.example.com

获取路由信息
***************************

在 CodeIgniter 4 中，理解并管理路由信息对于高效处理 HTTP 请求至关重要。
这包括获取当前控制器和方法，以及应用于特定路由的过滤器信息。
下面将介绍如何访问这些路由信息，以辅助日志记录、调试或实现条件逻辑等任务。

获取当前控制器 / 方法名称
==============================================

在某些情况下，可能需要确定当前 HTTP 请求触发了哪个控制器和方法。
这对于日志记录、调试，或基于当前控制器方法实现条件逻辑非常有用。

CodeIgniter 4 提供了 ``Router`` 类，可以方便地获取当前路由的控制器和方法名称，示例如下：

.. literalinclude:: routing/071.php

当需要动态与控制器交互，或记录处理请求的方法时，该功能尤其有用。

获取当前路由的活动过滤器
============================================

:doc:`过滤器 <filters>` 是一项强大的功能，可在处理 HTTP 请求之前或之后执行身份验证、日志记录和安全检查等操作。要获取当前路由的活动过滤器，可以使用 ``Router`` 类中的 :php:meth:`CodeIgniter\\Router\\Router::getFilters()` 方法。

该方法会返回当前路由正在使用的过滤器列表：

.. literalinclude:: routing/072.php

.. note:: ``getFilters()``` 方法仅返回为该特定路由定义的过滤器，不包含全局过滤器，也不包含 **app/Config/Filters.php** 中定义的过滤器。

获取当前路由匹配的选项
===================================================

在定义路由时，可以设置一些可选参数：``filter``、```namespace``、``hostname``、``subdomain``、``offset``、``priority``、``as``。这些内容在前文中已有说明。此外，如果使用了 ``addRedirect()``，还可能包含 ``redirect`` 键。
要访问这些参数的值，可以调用 ``Router::getMatchedRouteOptions()``。以下是返回数组的示例：

.. literalinclude:: routing/074.php
