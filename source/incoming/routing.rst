###########
URI 路由
###########

.. contents::
    :local:
    :depth: 3

什么是 URI 路由?
********************

URI 路由将一个 URI 与一个控制器的方法相关联。

CodeIgniter 有两种路由方式。一种是 **定义路由**,另一种是 **自动路由**。
通过定义路由,你可以手动定义路由规则。它允许灵活的 URL。
自动路由根据约定自动将 HTTP 请求路由到相应的控制器方法。无需手动定义路由。

首先,让我们看看定义路由。如果你想使用自动路由,请参阅 :ref:`auto-routing-improved`。

.. _defined-route-routing:

设置路由规则
*********************

路由规则定义在 **app/Config/Routes.php** 文件中。你会看到它实例化了
RouteCollection 类 (``$routes``),允许你指定自己的路由标准。
路由可以使用占位符或正则表达式来指定。

在指定路由时,你要为对应的 HTTP 动词(请求方法)选择一个方法。
如果你期望一个 GET 请求,请使用 ``get()`` 方法:

.. literalinclude:: routing/001.php

一个路由将 **路由路径** (相对于 BaseURL 的 URI 路径, ``/``)放在左边,
并将其映射到右边的 **路由处理程序** (控制器和方法 ``Home::index``),
以及应该传递给控制器的任何参数。

控制器和方法应该用双冒号 ``::`` 分隔类和方法的方式列出,就像使用静态方法 ``Users::list`` 一样。

如果该方法需要传递参数,则它们应该在方法名后以正斜杠分隔列出:

.. literalinclude:: routing/002.php

示例
========

这是一些基本的路由示例。

URL 的第一个段包含 **journals** 的情况下，会被映射到 ``\App\Controllers\Blogs`` 类，
以及 :ref:`默认方法 <routing-default-method>`，通常是 ``index()``:

.. literalinclude:: routing/006.php

包含路径段 **blog/joe** 的 URL 将被映射到 ``\App\Controllers\Blogs`` 类的 ``users()`` 方法。
ID 将被设置为 ``34``:

.. literalinclude:: routing/007.php

以 **product** 作为第一个段的 URL,任何内容作为第二段,将被映射到 ``\App\Controllers\Catalog`` 类
和 ``productLookup()`` 方法:

.. literalinclude:: routing/008.php

以 **product** 作为第一个段,数字作为第二段的 URL,将被映射到 ``\App\Controllers\Catalog`` 类
和 ``productLookupByID()`` 方法,并将匹配项作为变量传递给该方法:

.. literalinclude:: routing/009.php

.. _routing-http-verb-routes:

HTTP 动词路由
================

你可以使用任何标准的 HTTP 动词(GET、POST、PUT、DELETE、OPTIONS 等):

.. literalinclude:: routing/003.php

你可以通过将它们作为数组传递给 ``match()`` 方法来指定路由应匹配的多个动词:

.. literalinclude:: routing/004.php

指定路由处理程序
=========================

.. _controllers-namespace:

控制器的命名空间
----------------------

当你以字符串的形式指定控制器和方法名称时,如果控制器没有以 ``\`` 开头,
将会在前面加上 :ref:`routing-default-namespace`:

.. literalinclude:: routing/063.php

如果你在开头加上 ``\``,它将被视为完全限定的类名:

.. literalinclude:: routing/064.php

你也可以使用 ``namespace`` 选项指定命名空间:

.. literalinclude:: routing/038.php

详细信息请参阅 :ref:`assigning-namespace`。

数组可调用语法
---------------------

.. versionadded:: 4.2.0

自 v4.2.0 起,你可以使用数组可调用语法来指定控制器:

.. literalinclude:: routing/013.php
   :lines: 2-

或者使用 ``use`` 关键字:

.. literalinclude:: routing/014.php
   :lines: 2-

如果你忘记添加 ``use App\Controllers\Home;``，控制器类名会被解释为 ``\Home``，而不是 ``App\Controllers\Home``。

.. note:: 当你使用数组可调用语法时,类名总是被解释为完全限定的类名。
    所以 :ref:`routing-default-namespace` 和 :ref:`namespace 选项 <assigning-namespace>`
    没有效果。

数组可调用语法和占位符
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果有占位符,它将自动按指定顺序设置参数:

.. literalinclude:: routing/015.php
   :lines: 2-

但是,如果在路由中使用正则表达式,自动配置的参数可能不正确。
在这种情况下,你可以手动指定参数:

.. literalinclude:: routing/016.php
   :lines: 2-

使用闭包
--------------

你可以使用匿名函数或闭包作为路由映射的目标。当用户访问该 URI 时,此函数将被执行。
这对于快速执行小任务或只显示简单视图很方便:

.. literalinclude:: routing/020.php

指定路由路径
======================

占位符
------------

一个典型的路由可能如下所示:

.. literalinclude:: routing/005.php

在路由中,第一个参数包含要匹配的 URI,而第二个参数包含它应该路由到的目标。
在上面的示例中,如果在 URL 路径的第一个段中找到了字面词“product”,并且在第二个段中找到了一个数字,
则使用 ``Catalog`` 类和 ``productLookup`` 方法。

占位符只是代表正则表达式模式的字符串。在路由过程中,这些占位符会被正则表达式的值替换。
它们主要用于可读性。

你可以在路由中使用以下占位符:

============ ===========================================================================================================
占位符       描述
============ ===========================================================================================================
(:any)       将匹配从那点到 URI 结尾的所有字符。这可能包括多个 URI 段。
(:segment)   将匹配任何除正斜杠 (``/``) 之外的字符,限制结果为单个段。
(:num)       将匹配任何整数。
(:alpha)     将匹配任何字母字符字符串
(:alphanum)  将匹配任何字母字符字符串或整数,或两者的任意组合。
(:hash)      与 ``(:segment)`` 相同,但可以用来轻松看出哪些路由使用散列 ID。
============ ===========================================================================================================

.. note:: ``{locale}`` 不能作为占位符或路由的其他部分使用,因为它保留用于
    :doc:`localization </outgoing/localization>`。

.. _routing-placeholder-any:

(:any) 的行为
^^^^^^^^^^^^^^^^^^^^^^

请注意,单个 ``(:any)`` 将在 URL 中匹配多个段(如果存在)。

例如,路由:

.. literalinclude:: routing/010.php

将匹配 **product/123**、**product/123/456**、**product/123/456/789** 等等。

默认情况下，在上面的例子中，如果 ``$1`` 占位符包含斜杠（``/``），在传递给
``Catalog::productLookup()`` 时，它仍然会被拆分为多个参数。

.. note:: 自 v4.5.0 起，你可以通过配置选项更改此行为。
    详情请参见 :ref:`multiple-uri-segments-as-one-parameter`。

控制器中的实现应考虑最大参数:

.. literalinclude:: routing/011.php

或者你可以使用 `变长参数列表 <https://www.php.net/manual/en/functions.arguments.php#functions.variable-arg-list>`_：

.. literalinclude:: routing/068.php

.. important:: 不要在 ``(:any)`` 后面放任何占位符。因为传递给控制器方法的参数数量可能会改变。

如果匹配多个段不是预期的行为,那么在定义路由时应该使用 ``(:segment)``。对于上面的示例 URL:

.. literalinclude:: routing/012.php

将只匹配 **product/123**,其余示例将生成 404 错误。

自定义占位符
-------------------

你可以创建自己的占位符,在路由文件中使用它们以完全自定义体验和可读性。

你可以使用 ``addPlaceholder()`` 方法添加新占位符。第一个参数是将用作占位符的字符串。
第二个参数是它应该被替换的正则表达式模式。这必须在添加路由之前调用:

.. literalinclude:: routing/017.php

正则表达式
-------------------

如果你愿意,可以使用正则表达式来定义路由规则。允许任何有效的正则表达式,以及反向引用。

.. important:: 注意:如果使用反向引用,必须使用美元语法而不是双反斜杠语法。
    一个典型的 RegEx 路由可能如下所示:

    .. literalinclude:: routing/018.php

在上面的示例中,类似于 **products/shirts/123** 的 URI 将调用 ``Products``
控制器类的 ``show()`` 方法,并将原始的第一个和第二个段作为参数传递给它。

使用正则表达式,你也可以捕获包含正斜杠 (``/``) 的段,通常表示多个段之间的分隔符。

例如,如果用户访问你的 Web 应用程序的密码保护区域,并且你希望能够在他们登录后将他们重定向回同一页面,你可能会发现此示例很有用:

.. literalinclude:: routing/019.php

默认情况下，在上面的例子中，如果 ``$1`` 占位符包含斜杠（``/``），在传递给
``Auth::login()`` 时，它仍然会被拆分为多个参数。

.. note:: 自 v4.5.0 起，你可以通过配置选项更改此行为。
    详情请参见 :ref:`multiple-uri-segments-as-one-parameter`。

对于那些不了解正则表达式并希望学习更多知识的人, `regular-expressions.info <https://www.regular-expressions.info/>`_ 可能是一个不错的起点。

.. note:: 你也可以将占位符与正则表达式结合使用。

.. _view-routes:

视图路由
===========

.. versionadded:: 4.3.0

如果你只想渲染一个没有关联逻辑的视图,你可以使用 ``view()`` 方法。这始终被视为 GET 请求。
该方法接受要加载的视图名称作为第二个参数。

.. literalinclude:: routing/065.php

如果在路由中使用占位符,则可以在名为 ``$segments`` 的特殊变量中访问它们。它们以数组形式提供,索引顺序与路由中的出现顺序相同。

.. literalinclude:: routing/066.php

.. _redirecting-routes:

重定向路由
==================

任何存在足够长的站点都会有页面移动的情况。你可以使用 ``addRedirect()`` 方法指定应重定向到其他路由的路由。
第一个参数是旧路由的 URI 模式。第二个参数是重定向的新 URI,或命名路由的名称。
第三个参数是应随重定向一起发送的 HTTP 状态码。默认值为 ``302``,这是临时重定向,在大多数情况下都推荐使用:

.. literalinclude:: routing/022.php

.. note:: 自 v4.2.0 起, ``addRedirect()`` 可以使用占位符。

如果在页面加载期间匹配到重定向路由,用户将在控制器加载之前立即重定向到新页面。

环境限制
========================

你可以创建一组路由,这些路由只能在某些环境中查看。这允许你创建仅开发人员才能在其本地机器上使用的工具,这些工具在测试或生产服务器上无法访问。
可以使用 ``environment()`` 方法来完成。第一个参数是环境的名称。此闭包中定义的任何路由只能从给定环境访问:

.. literalinclude:: routing/028.php

任意 HTTP 动词的路由
==========================

.. important:: 这个方法只为了向后兼容而存在。在新项目中不要使用它。即使你已经在使用它，我们也建议你使用另一种更适合的方法。

.. warning:: 尽管 ``add()`` 方法看起来很方便,但建议始终使用基于 HTTP 动词的路由,如上所述,因为它更安全。
    如果你使用 :doc:`CSRF 保护 </libraries/security>`,它不会保护 **GET** 请求。
    如果 ``add()`` 方法中指定的 URI 可以通过 GET 方法访问,CSRF 保护将不起作用。

可以定义具有任意 HTTP 动词的路由。你可以使用 ``add()`` 方法:

.. literalinclude:: routing/031.php

.. note:: 使用基于 HTTP 动词的路由还会提供略微的性能提升,因为只存储与当前请求方法匹配的路由,
    从而在尝试找到匹配项时扫描的路由更少。

映射多个路由
=======================

.. important:: 这个方法只为了向后兼容而存在。在新项目中不要使用它。即使你已经在使用它，我们也建议你使用另一种更适合的方法。

.. warning:: 不推荐使用 ``map()`` 方法,就像 ``add()`` 一样,因为它在内部调用 ``add()``。

尽管 ``add()`` 方法使用简单,但通常更方便的是同时使用多个路由,使用 ``map()`` 方法。
你可以定义一个路由数组,然后将其作为第一个参数传递给 ``map()`` 方法,而不是为你需要添加的每个路由调用 ``add()`` 方法:

.. literalinclude:: routing/021.php

.. _command-line-only-routes:

仅命令行路由
========================

.. note:: 建议使用 Spark 命令作为 CLI 脚本,而不是通过 CLI 调用控制器。请参阅
    :doc:`../cli/cli_commands` 页面以获取详细信息。

任何通过基于 HTTP 动词的路由方法创建的路由也将无法从 CLI 访问，但通过 ``add()`` 方法创建的路由仍然可以从命令行访问。

你可以使用 ``cli()`` 方法创建只能从命令行使用、无法从 Web 浏览器访问的路由:

.. literalinclude:: routing/032.php

.. warning:: 如果启用 :ref:`auto-routing-legacy` 并将命令文件放在 **app/Controllers** 中,
    任何人都可以在 Auto Routing(传统)的帮助下通过 HTTP 访问该命令。

全局选项
**************

创建路由的所有方法(``get()``、``post()``、:doc:`resource() <restful>` 等)都可以带有一个选项数组,
以修改生成的路由或进一步限制它们。``$options`` 数组始终是最后一个参数:

.. literalinclude:: routing/033.php

.. _applying-filters:

应用过滤器
================

你可以通过在控制器之前或之后提供要运行的过滤器来更改特定路由的行为。这在认证或 API 日志记录时特别方便。

过滤器的值可以是字符串或字符串数组:

* 与 **app/Config/Filters.php** 中定义的别名匹配。
* 过滤器类名

请参阅 :ref:`控制器过滤器 <filters-aliases>` 了解更多关于定义别名的信息。

.. warning:: 如果你在 **app/Config/Routes.php** 中为路由设置过滤器(而不是在 **app/Config/Filters.php** 中)
    建议禁用 Auto Routing(传统)。当启用 :ref:`auto-routing-legacy` 时,控制器可能可以通过与配置路由不同的 URL 访问,
    在这种情况下,你为该路由指定的过滤器将不会应用。请参阅 :ref:`use-defined-routes-only` 以禁用自动路由。

别名过滤器
------------

你可以为过滤器值指定一个 :ref:`在 app/Config/Filters.php 中定义 <filters-aliases>` 的别名。

.. literalinclude:: routing/034.php

你还可以提供要传递给别名过滤器的 ``before()`` 和 ``after()`` 方法的参数:

.. literalinclude:: routing/035.php

类名过滤器
----------------

.. versionadded:: 4.1.5

你可以为过滤器值指定一个过滤器类名：

.. literalinclude:: routing/036.php

.. _multiple-filters:

多重过滤器
----------------

.. versionadded:: 4.1.5

.. important:: 自 v4.5.0 起，*多重过滤器* 始终启用。
    在 v4.5.0 之前，*多重过滤器* 默认是禁用的。
    如果你想在 v4.5.0 之前的版本中使用，请参见
    :ref:`从 4.1.4 升级到 4.1.5 <upgrade-415-multiple-filters-for-a-route>`
    了解详情。

你可以为过滤器值指定一个数组：

.. literalinclude:: routing/037.php

过滤器参数
^^^^^^^^^^^^^^^^

可以向过滤器传递额外的参数：

.. literalinclude:: routing/067.php

在这个例子中，数组 ``['dual', 'noreturn']`` 将作为 ``$arguments`` 传递给过滤器的 ``before()`` 和 ``after()`` 实现方法。

.. _assigning-namespace:

分配命名空间
===================

虽然 :ref:`routing-default-namespace` 将被预先添加到生成的控制器中,
但你也可以在任何选项数组中使用 ``namespace`` 选项指定要使用的不同命名空间。
值应该是要修改的命名空间:

.. literalinclude:: routing/038.php

新的命名空间仅在该调用期间应用于任何创建单个路由的方法,如 get、post 等。
对于创建多个路由的任何方法,新的命名空间将附加到该函数生成的所有路由,或者在 ``group()`` 的情况下,附加到闭包中生成的所有路由。

限制主机名
=================

你可以通过在选项数组中传递“hostname”选项以及允许的域来限制路由组仅在应用程序的某些域或子域中运行:

.. literalinclude:: routing/039.php

此示例只允许指定主机在域完全匹配 **accounts.example.com** 时工作。
它不会在主站点 **example.com** 中工作。

限制子域名
===================

当存在 ``subdomain`` 选项时,系统将只允许路由在该子域上可用。仅当应用程序正在查看的子域是路由定义的子域时,才会匹配该路由:

.. literalinclude:: routing/040.php

你可以通过将值设置为星号 (``*``) 来限制到任何子域。如果你从一个没有任何子域存在的 URL 查看,这将不会匹配:

.. literalinclude:: routing/041.php

.. important:: 该系统并不完美,在生产中使用之前,应针对你的特定域进行测试。大多数域都应正常工作,但某些极端情况的域,尤其是域本身中包含句点(不用于分隔后缀或 www)的域可能会导致误报。

偏移匹配参数
=================================

你可以使用 ``offset`` 选项以任意数字值偏移路由中的匹配参数,值是要偏移的段数。

当使用 API 的第一个 URI 段是版本号时,这很有用。它也可以在第一个参数是语言字符串时使用:

.. literalinclude:: routing/042.php

.. _reverse-routing:

反向路由
***************

反向路由允许你定义控制器和方法,以及任何参数,使链接应该指向的位置,并让路由器查找当前路由。
这允许路由定义更改而不必更新应用程序代码。这通常在视图中用于创建链接。

例如,如果你有一个指向相册的路由要链接到,你可以使用 :php:func:`url_to()` 辅助函数来获取应该使用的路由。
第一个参数是用双冒号 (``::``) 分隔的完全限定的控制器和方法,就像编写初始路由本身一样。
任何应该传递给路由的参数在后面传入:

.. literalinclude:: routing/029.php

.. _using-named-routes:

命名路由
************

你可以命名路由以使应用程序更加健壮。这会给路由指定一个名称,以后可以调用此名称,即使路由定义发生更改,
使用 :php:func:`url_to()` 构建的应用程序中的所有链接也仍然有效,而无需进行任何更改。
通过传递 ``as`` 选项及路由名称来命名路由:

.. literalinclude:: routing/030.php

这也使视图更具可读性。

分组路由
***************

你可以使用 ``group()`` 方法在共同名称下对路由进行分组。组名称成为出现在组内定义的路由之前的一个段。
这允许你减少构建共享开头字符串的大量路由所需的输入,例如构建管理区域:

.. literalinclude:: routing/023.php

这将为 **users** 和 **blog** URI 添加前缀 **admin**,处理像 **admin/users** 和 **admin/blog** 这样的 URL。

设置命名空间
=================

如果你需要为组分配选项,如 :ref:`assigning-namespace`,请在回调之前执行:

.. literalinclude:: routing/024.php

这将处理指向 ``App\API\v1\Users`` 控制器的资源路由,URI 为 **api/users**。

设置过滤器
===============

你还可以为路由组使用特定的 :doc:`过滤器 <filters>`。这将始终在控制器之前或之后运行过滤器。
这在认证或 API 日志记录时特别方便:

.. literalinclude:: routing/025.php

过滤器的值必须与 **app/Config/Filters.php** 内定义的别名之一匹配。

.. note:: 在 v4.5.4 之前，由于一个 bug，传递给 ``group()`` 的过滤器没有合并到传递给内部路由的过滤器中。

设置其他选项
=====================

在某些时候,你可能要对路由进行分组以应用过滤器或其他路由配置选项,如命名空间、子域名等,而不一定需要为组添加前缀。
你可以传入空字符串代替前缀,该组中的路由将路由,就好像组从未存在过一样,但具有给定的路由配置选项:

.. literalinclude:: routing/027.php

.. _routing-nesting-groups:

嵌套分组
==============

如果需要,可以在组内嵌套组进行更细粒度的组织:

.. literalinclude:: routing/026.php

这将处理在 **admin/users/list** 的 URL。

``filter`` 选项传递给外部的 ``group()`` 时，会与内部的 ``group()`` 过滤器选项合并。
上述代码对路由 ``admin`` 运行 ``myfilter1:config``，对路由 ``admin/users/list`` 运行 ``myfilter1:config`` 和 ``myfilter2:region``。

.. note:: 同一个过滤器不能带不同的参数多次运行。

任何传递给内部 ``group()`` 的其他重叠选项都会覆盖它们的值。

.. note:: 在 v4.5.0 之前，由于一个错误，传递给外部 ``group()`` 的选项不会与内部 ``group()`` 的选项合并。

.. _routing-priority:

路由优先级
**************

路由以它们被定义的顺序注册到路由表中。这意味着当访问一个 URI 时,第一个匹配的路由将被执行。

.. warning:: 如果使用不同的处理程序多次定义路由路径,则只注册第一个定义的路由。

你可以通过运行 :ref:`spark routes <routing-spark-routes>` 命令来检查路由表中的注册路由。

更改路由优先级
=======================

在使用模块时,如果应用程序中的路由包含通配符,则模块路由将无法正确处理。
你可以通过使用 ``priority`` 选项降低路由处理优先级来解决此问题。该参数接受正整数和零。
在 ``priority`` 中指定的数字越高,处理队列中的路由优先级越低:

.. literalinclude:: routing/043.php

要禁用此功能,必须使用 ``false`` 参数调用该方法:

.. literalinclude:: routing/044.php

.. note:: 默认情况下,所有路由的优先级都是 0。负整数将被转换为绝对值。

.. _routes-configuration-options:

路由配置选项
****************************

RoutesCollection 类提供了几个选项，可以影响所有路由，并且可以根据你的应用程序需求进行修改。这些选项可以在 **app/Config/Routing.php** 文件中找到。

.. note:: 配置文件 **app/Config/Routing.php** 自 v4.4.0 版本开始添加。
    在之前的版本中，使用 **app/Config/Routes.php** 中的 setter 方法来更改设置。

.. _routing-default-namespace:

默认命名空间
=================

在将控制器与路由匹配时,路由器会在路由指定的控制器前面添加默认的命名空间值。
默认值为 ``App\\Controllers``。

如果你将值设置为空字符串 (``''``),它会让每个路由指定完全限定的控制器:

.. literalinclude:: routing/045.php

如果你的控制器没有明确指定命名空间,则不需要更改此值。如果你的控制器指定了命名空间,那么你可以更改此值以节省输入:

.. literalinclude:: routing/046.php

.. _routing-default-method:

默认方法
==============

该设置在路由处理器只有控制器名称而没有方法名称列出时使用。默认值是 ``index``。
::

    // 在 app/Config/Routing.php 中
    public string $defaultMethod = 'index';

.. note:: ``$defaultMethod`` 也常用于自动路由。
    请参见 :ref:`自动路由（改进版） <routing-auto-routing-improved-default-method>`
    或 :ref:`自动路由（传统版） <routing-auto-routing-legacy-default-method>`。

如果你定义了以下路由::

    $routes->get('/', 'Home');

当路由匹配时，将执行 ``App\Controllers\Home`` 控制器的 ``index()`` 方法。

.. note:: 方法名称以 ``_`` 开头时不能用作默认方法。
    但是，从 v4.5.0 开始，允许使用 ``__invoke`` 方法。

转换 URI 中的破折号
====================

该选项允许你在使用自动路由时，自动将控制器和方法的 URI 段中的破折号（``-``）替换为下划线，从而节省了额外的路由条目。这是必需的，因为破折号不是有效的类或方法名称字符，如果你尝试使用它，将会导致致命错误：

.. literalinclude:: routing/049.php

.. note:: 在使用自动路由（改进版）时，在 v4.4.0 之前，如果 ``$translateURIDashes`` 为 true，两个 URI 对应一个控制器方法，一个 URI 用于破折号（例如 **foo-bar**），另一个 URI 用于下划线（例如 **foo_bar**）。这是错误的行为。从 v4.4.0 开始，下划线的 URI（**foo_bar**）不可访问。

.. _use-defined-routes-only:

仅使用定义的路由
=======================

自 v4.2.0 起,默认禁用自动路由。

当未找到与当前 URI 匹配的定义路由时,如果启用了自动路由,系统将尝试将该 URI 与控制器和方法匹配。

你可以通过将 ``$autoRoute`` 属性设置为 false 来禁用此自动匹配,
并且只限制路由为你定义的路由:

.. literalinclude:: routing/050.php

.. warning:: 如果你使用 :doc:`CSRF 保护 </libraries/security>`,它不会保护 **GET** 请求。
    如果 URI 可以通过 GET 方法访问,CSRF 保护将不起作用。

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
此功能影响所有路由。有关降低优先级的示例用法,请参阅 :ref:`routing-priority`:

.. literalinclude:: routing/052.php

.. _multiple-uri-segments-as-one-parameter:

将多个 URI 段作为一个参数
======================================

.. versionadded:: 4.5.0

启用此选项时，匹配多个段的占位符，例如 ``(:any)``，将直接按原样传递给一个参数，即使它包含多个段。

.. literalinclude:: routing/070.php

例如，以下路由：

.. literalinclude:: routing/010.php

将匹配 **product/123**、**product/123/456**、**product/123/456/789** 等等。
如果 URI 是 **product/123/456**，``123/456`` 将被传递给 ``Catalog::productLookup()`` 方法的第一个参数。

.. _auto-routing-improved:

自动路由(改进版)
***********************

.. versionadded:: 4.2.0

自 v4.2.0 起,引入了新的更安全的自动路由。

.. note:: 如果你熟悉自动路由,在 CodeIgniter 3.x 到 4.1.x 中默认启用,
    你可以在 :ref:`ChangeLog v4.2.0 <v420-new-improved-auto-routing>` 中看到区别。

当未找到与 URI 匹配的定义路由时,如果启用了自动路由,系统将尝试将该 URI 与控制器和方法匹配。

.. important:: 出于安全考虑,如果控制器在定义的路由中使用,自动路由(改进版)不会路由到该控制器。

自动路由可以根据约定自动路由 HTTP 请求,并执行相应的控制器方法。

.. note:: 自动路由(改进版)默认禁用。要使用它,请参阅下文。

.. _enabled-auto-routing-improved:

启用自动路由
===================

要使用它,你需要在 **app/Config/Routing.php** 中将 ``$autoRoute`` 选项设置为 ``true``::

    public bool $autoRoute = true;

并且你需要在 **app/Config/Feature.php** 中将属性 ``$autoRoutesImproved`` 设置为 ``true``::

    public bool $autoRoutesImproved = true;

URI 段
============

按照 MVC 方法,URL 中的段通常代表::

    example.com/class/method/ID

1. 第一个段表示要调用的控制器 **类**。
2. 第二个段表示要调用的类 **方法**。
3. 第三个及任何其他段表示要传递给控制器的 ID 和任何变量。

考虑此 URI::

    example.com/index.php/helloworld/hello/1

在上面的示例中,当发送 **GET** 方法的 HTTP 请求时,自动路由会尝试找到名为 ``App\Controllers\Helloworld`` 的控制器,
并使用 ``'1'`` 作为第一个参数执行 ``getHello()`` 方法。

.. note:: 自动路由(改进版)执行的控制器方法需要 HTTP 动词(``get``、``post``、``put`` 等)前缀,如 ``getIndex()``、``postCreate()``。

更多信息请参阅 :ref:`控制器中的自动路由(改进版) <controller-auto-routing-improved>`。

.. _routing-auto-routing-improved-configuration-options:

配置选项
=====================

这些选项在 **app/Config/Routing.php** 文件中可用。

默认控制器
------------------

针对网站根 URI
^^^^^^^^^^^^^^^^^

当用户访问你站点的根目录(即 **example.com**)时,除非为它明确定义了路由,否则使用的控制器由 ``$defaultController`` 属性设置的值确定。

默认值为 ``Home``,它与 **app/Controllers/Home.php** 中的控制器匹配::

    public string $defaultController = 'Home';

针对目录 URI
^^^^^^^^^^^^^^^^^

默认控制器也在未找到匹配的路由且 URI 指向控制器目录中的目录时使用。例如,如果用户访问 **example.com/admin**,如果在 **app/Controllers/Admin/Home.php** 中找到了一个控制器,则会使用它。

更多信息请参阅 :ref:`控制器中的自动路由(改进版) <controller-auto-routing-improved>`。

.. _routing-auto-routing-improved-default-method:

默认方法
--------------

这与默认控制器设置类似,但用于在找到与 URI 匹配的控制器但不存在方法段时确定使用的默认方法。默认值为 ``index``。

在此示例中,如果用户访问 **example.com/products**,且存在 ``Products`` 控制器,将执行 ``Products::getListAll()`` 方法::

    public string $defaultMethod = 'listAll';

.. important:: 你无法使用控制器的默认方法名称访问控制器。在上面的示例中,你可以访问 **example.com/products**,但是如果访问 **example.com/products/listall** 将找不到。

.. _auto-routing-improved-module-routing:

模块路由
==============

.. versionadded:: 4.4.0

即使你使用 :doc:`../general/modules` 并将控制器放置在不同的命名空间中，你仍可以使用自动路由。

要路由到一个模块，必须在 **app/Config/Routing.php** 中设置 ``$moduleRoutes`` 属性::

    public array $moduleRoutes = [
        'blog' => 'Acme\Blog\Controllers',
    ];

键是模块的第一个 URI 段，值是控制器的命名空间。在上述配置中，**http://localhost:8080/blog/foo/bar** 将被路由到 ``Acme\Blog\Controllers\Foo::getBar()``。

.. note:: 如果你定义了 ``$moduleRoutes``，模块的路由将优先生效。在上面的示例中，即使你有 ``App\Controllers\Blog`` 控制器，**http://localhost:8080/blog** 也将被路由到默认控制器 ``Acme\Blog\Controllers\Home``。

.. _auto-routing-legacy:

自动路由(传统)
*********************

.. important:: 这个功能只为了向后兼容而存在。在新项目中不要使用它。即使你已经在使用它，我们也推荐你使用 :ref:`auto-routing-improved` 替代。

自动路由(传统)是来自 CodeIgniter 3 的路由系统。它可以根据约定自动路由 HTTP 请求,并执行相应的控制器方法。

推荐在 **app/Config/Routes.php** 文件中定义所有路由,或者使用 :ref:`auto-routing-improved`。

.. warning:: 为了防止配置错误和编码错误,我们建议你不要使用自动路由(传统)功能。很容易创建容易受攻击的应用程序,其中控制器过滤器或 CSRF 保护被绕过。

.. important:: 自动路由(传统)会将任何 HTTP 方法的 HTTP 请求路由到控制器方法。

启用自动路由(传统)
============================

自 v4.2.0 起,默认禁用自动路由。

要使用它,你需要在 **app/Config/Routing.php** 中将 ``$autoRoute`` 选项设置为 ``true``::

    public bool $autoRoute = true;

并且在 **app/Config/Feature.php** 中，将属性 ``$autoRoutesImproved`` 设置为 ``false``::

    public bool $autoRoutesImproved = false;

URI 段(传统)
=====================

在上面的示例中,CodeIgniter 会尝试找到一个名为 **Helloworld.php** 的控制器,并执行 ``index()`` 方法。

更多信息请参阅 :ref:`控制器中的自动路由(传统) <controller-auto-routing-legacy>`。

.. _routing-auto-routing-legacy-configuration-options:

配置选项(传统)
==============================

这些选项在 **app/Config/Routing.php** 文件中可用。

默认控制器(传统)
---------------------------

针对网站根 URI(传统)
^^^^^^^^^^^^^^^^^^^^^^^^^^

当用户访问你网站的根（例如，**example.com**）时，除非存在明确的路由，否则将根据 ``$defaultController`` 属性设定的值来确定要使用的控制器。

对于这个属性，默认值是 ``Home``，它匹配在 **app/Controllers/Home.php** 的控制器::

    public string $defaultController = 'Home';

针对目录 URI(传统)
^^^^^^^^^^^^^^^^^^^^^^^^^^

默认控制器也在未找到匹配的路由且 URI 指向控制器目录中的目录时使用。例如,如果用户访问 **example.com/admin**,如果在 **app/Controllers/Admin/Home.php** 中找到了一个控制器,则会使用它。

更多信息请参阅 :ref:`控制器中的自动路由(传统) <controller-auto-routing-legacy>`。

.. _routing-auto-routing-legacy-default-method:

默认方法(传统)
-----------------------

这与默认控制器设置类似,但用于在找到与 URI 匹配的控制器但不存在方法段时确定使用的默认方法。默认值为 ``index``。

在此示例中,如果用户访问 **example.com/products**,且存在 ``Products`` 控制器,将执行 ``Products::listAll()`` 方法:

    public string $defaultMethod = 'listAll';

确认路由
*****************

CodeIgniter 有以下 :doc:`命令 </cli/spark_commands>` 可显示所有路由。

.. _routing-spark-routes:

spark 路由
============

显示所有路由和过滤器:

.. code-block:: console

    php spark routes

输出类似以下内容:

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

你可以使用 ``--host`` 选项在请求 URL 中指定主机：

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
