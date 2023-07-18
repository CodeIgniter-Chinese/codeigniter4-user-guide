###########
URI 路由
###########

.. contents::
    :local:
    :depth: 3

什么是 URI 路由?
********************

URI 路由将一个 URI 与控制器的方法相关联。

CodeIgniter 有两种路由。一种是**定义路由**,另一种是**自动路由**。
使用定义路由,你可以手动定义路由。它支持灵活的 URL。
自动路由根据约定自动路由 HTTP 请求并执行相应的控制器方法。不需要手动定义路由。

首先,让我们看看定义路由。如果你想使用自动路由,请参阅 :ref:`auto-routing-improved`。

.. _defined-route-routing:

设置路由规则
*********************

路由规则定义在 **app/Config/Routes.php** 文件中。在其中你会看到它实例化了 RouteCollection 类(``$routes``),允许你指定自己的路由条件。
路由可以使用占位符或正则表达式来指定。

当你指定一个路由时,你要选择一个方法来对应 HTTP 动词(请求方法)。
如果你期望一个 GET 请求,请使用 ``get()`` 方法:

.. literalinclude:: routing/001.php

一个路由在左侧获取**路由路径**(相对于 BaseURL 的 URI 路径 ``/``),
并在右侧映射到**路由处理程序**(控制器和方法 ``Home::index``),
以及应该传递给控制器的任何参数。

控制器和方法应该列出它将使用的静态方法,
通过用双冒号分隔类和它的方法,像 ``Users::list``。

如果该方法需要传递参数,那么它们应该在方法名之后列出,用正斜杠分隔:

.. literalinclude:: routing/002.php

示例
========

以下是一些基本的路由示例。

如果 URI 的第一个段包含词汇 **journals**,它将映射到 ``\App\Controllers\Blogs`` 类,以及默认方法,通常是 ``index()``:

.. literalinclude:: routing/006.php

如果 URI 包含 **blog/joe** 段,它将映射到 ``\App\Controllers\Blogs`` 类和 ``users()`` 方法。
ID 将设置为 ``34``:

.. literalinclude:: routing/007.php

如果第一个段为 **product**,第二个段为任何内容,它将映射到 ``\App\Controllers\Catalog`` 类和 ``productLookup()`` 方法:

.. literalinclude:: routing/008.php

如果第一个段为 **product**,第二个段为数字,它将映射到 ``\App\Controllers\Catalog`` 类和 ``productLookupByID()`` 方法,并将匹配项作为变量传递给该方法:

.. literalinclude:: routing/009.php

HTTP 动词路由
================

你可以使用任何标准的 HTTP 动词(GET、POST、PUT、DELETE、OPTIONS 等):

.. literalinclude:: routing/003.php

你可以通过将它们作为数组传递给 ``match()`` 方法,指定路由应匹配的多个动词:

.. literalinclude:: routing/004.php

指定路由处理程序
=========================

控制器的命名空间
----------------------

当你以字符串形式指定控制器和方法名称时,如果控制器没有前导的 ``\``,
将会在控制器前加上 :ref:`routing-default-namespace` :

.. literalinclude:: routing/063.php

如果你在开头放置 ``\``,它将被视为完全限定的类名:

.. literalinclude:: routing/064.php

你还可以使用 ``namespace`` 选项指定命名空间:

.. literalinclude:: routing/038.php

有关详细信息,请参阅 :ref:`assigning-namespace`。

数组可调用语法
---------------------

.. versionadded:: 4.2.0

自 v4.2.0 起,你可以使用数组可调用语法来指定控制器:

.. literalinclude:: routing/013.php
   :lines: 2-

或者使用 ``use`` 关键字:

.. literalinclude:: routing/014.php
   :lines: 2-

如果你忘记添加 ``use App\Controllers\Home;``,控制器类名将被解释为
``Config\Home``,而不是 ``App\Controllers\Home``,因为
**app/Config/Routes.php** 顶部有 ``namespace Config;``。

.. note:: 当你使用数组可调用语法时,类名总是被解释为完全限定的类名。
    所以 :ref:`routing-default-namespace` 和 :ref:`namespace 选项 <assigning-namespace>` 都没有效果。

数组可调用语法和占位符
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果有占位符,它将自动按指定顺序设置参数:

.. literalinclude:: routing/015.php
   :lines: 2-

但是如果在路由中使用了正则表达式,自动配置的参数可能不正确。
在这种情况下,你可以手动指定参数:

.. literalinclude:: routing/016.php
   :lines: 2-

使用闭包
--------------

你可以使用匿名函数或闭包作为路由映射的目标。当用户访问该 URI 时,将执行此函数。这对于快速执行小任务或者简单显示视图很有用:

.. literalinclude:: routing/020.php

指定路由路径
======================

占位符
------------

一个典型的路由可能如下所示:

.. literalinclude:: routing/005.php

在路由中,第一个参数包含要匹配的 URI,而第二个参数包含它应该路由到的目标。在上面的示例中,如果在 URL 路径的第一个段中找到字面单词“product”,并在第二个段中找到一个数字,则使用 ``Catalog`` 类和 ``productLookup`` 方法。

占位符只是表示正则表达式模式的字符串。在路由过程中,这些占位符被正则表达式的值替换。它们主要用于可读性。

以下占位符可用于路由中:

============ ===========================================================================================================
占位符       描述
============ ===========================================================================================================
(:any)       将匹配从该点到 URI 结尾的所有字符。这可能包括多个 URI 段。
(:segment)   将匹配任何字符,除了正斜杠 (``/``),限制结果为单个段。
(:num)       将匹配任何整数。
(:alpha)     将匹配任意字符串的字母字符
(:alphanum)  将匹配任何字符串的字母字符或整数,或两者的任意组合。
(:hash)      与 ``(:segment)`` 相同,但可以用来轻松看出哪些路由使用散列 id。
============ ===========================================================================================================

.. note:: ``{locale}`` 不能用作占位符或路由的其他部分,因为它保留用于 :doc:`localization </outgoing/localization>`。

请注意,单个 ``(:any)`` 将在 URL 中存在多个段时匹配它们。例如,路由:

.. literalinclude:: routing/010.php

将匹配 **product/123**、**product/123/456**、**product/123/456/789** 等等。实现时控制器应考虑最大参数:

.. literalinclude:: routing/011.php

.. important:: 不要在 ``(:any)`` 之后放任何占位符。因为传递给控制器方法的参数数量可能会改变。

如果不希望出现多段匹配,在定义路由时应使用 ``(:segment)``。使用上面的示例 URL:

.. literalinclude:: routing/012.php

将只匹配 **product/123** 并为其他示例生成 404 错误。

自定义占位符
-------------------

你可以创建自己的占位符,在路由文件中使用它们以完全自定义体验和可读性。

使用 ``addPlaceholder()`` 方法添加新的占位符。第一个参数是用作占位符的字符串。第二个参数是它应该被替换的正则表达式模式。这必须在添加路由之前调用:

.. literalinclude:: routing/017.php

正则表达式
-------------------

如果你愿意,可以使用正则表达式定义路由规则。任何有效的正则表达式都是允许的,反向引用也允许。

.. important:: 注意:如果使用反向引用,你必须使用美元符号语法,而不是双反斜杠语法。
    一个典型的正则表达式路由可能如下所示:

    .. literalinclude:: routing/018.php

在上面的示例中,类似于 **products/shirts/123** 的 URI 将调用 ``Products`` 控制器类的 ``show()`` 方法,并将原始的前两个段作为参数传递给它。

使用正则表达式,你还可以捕获包含正斜杠 (``/``) 的段,通常代表多个段之间的分隔符。

例如,如果用户访问你 Web 应用程序的密码保护区域,并希望在登录后将他们重定向回相同的页面,你可能会发现此示例很有用:

.. literalinclude:: routing/019.php

对于那些不知道正则表达式并想了解更多知识的人,`regular-expressions.info <https://www.regular-expressions.info/>`_ 可能是一个不错的起点。

.. note:: 你也可以混合并匹配占位符和正则表达式。

.. _view-routes:

视图路由
===========

.. versionadded:: 4.3.0

如果你只想渲染一个与之不关联的逻辑的视图,可以使用 ``view()`` 方法。这始终被视为 GET 请求。
该方法接受要加载的视图名称作为第二个参数。

.. literalinclude:: routing/065.php

如果在路由中使用了占位符,你可以在特殊变量 ``$segments`` 中访问它们。它们以出现在路由中的顺序作为数组提供。

.. literalinclude:: routing/066.php

.. _redirecting-routes:

重定向路由
==================

任何长期存在的网站都会有页面移动。你可以使用 ``addRedirect()`` 方法指定应重定向到其他路由的路由。第一个参数是旧路由的 URI 模式。第二个参数是要重定向到的新 URI 或命名路由的名称。第三个参数是应随重定向一起发送的 HTTP 状态码。默认值为 ``302``,这是临时重定向,在大多数情况下都推荐:

.. literalinclude:: routing/022.php

.. note:: 从 v4.2.0 开始,``addRedirect()`` 可以使用占位符。

如果在页面加载期间匹配了重定向路由,用户将在加载控制器之前立即重定向到新页面。

环境限制
========================

你可以通过在选项数组中与允许的域一起传递“hostname”选项,将一组路由的功能限制为仅在某些域或子域中运行你的应用程序,

.. literalinclude:: routing/039.php

此示例仅当域完全匹配 **accounts.example.com** 时才允许指定的主机工作。它不会在主站点 **example.com** 上工作。

限制子域
===================

当存在 ``subdomain`` 选项时,系统将限制只在该子域上可用的路由。只有在通过子域查看应用程序时,路由才会匹配:

.. literalinclude:: routing/040.php

你可以通过将值设置为星号 (``*``) 来限制任何子域。如果正在查看的 URL 没有任何子域,则不会匹配此路由:

.. literalinclude:: routing/041.php

.. important:: 该系统并不完美,在生产中使用之前,应针对特定域进行测试。
    大多数域应正常工作,但某些边缘情况的域,尤其是域本身中包含句点(而不是用于分隔后缀或 www)的,可能会导致误报。

偏移匹配参数
=================================

通过在选项中传递“offset”选项以及任何数字值,你可以以任何数字值偏移匹配的参数。

这在开发 API 时很有用,其中第一个 URI 段是版本号。它也可以在第一个参数是语言字符串时使用:

.. literalinclude:: routing/042.php

.. _reverse-routing:

反向路由
***************

反向路由允许你定义控制器和方法,以及任何参数,链接应该指向的位置,并使路由器查找当前路由。这允许路由定义更改,而无需更新应用程序代码。这通常在视图中用于创建链接。

例如,如果你有一个指向相册的路由,你想要链接到它,可以使用 :php:func:`url_to()` 助手函数来获取应使用的路由。第一个参数是完全限定的控制器和方法,用双冒号(``::``)分隔,就像编写初始路由本身一样。任何应该传递给路由的参数随后传递:

.. literalinclude:: routing/029.php

.. _using-named-routes:

命名路由
**************

你可以命名路由以使应用程序不那么脆弱。这会为稍后可以调用的路由分配名称,即使路由定义发生变化,使用 :php:func:`url_to()` 构建的应用程序中的所有链接也仍然有效。通过在选项中传递 ``as`` 及路由的名称来命名路由:

.. literalinclude:: routing/030.php

这也有助于使视图更具可读性。

分组路由
***************

你可以使用 ``group()`` 方法在公共名称下对路由进行分组。组名称将成为出现在组内定义的路由之前的一个段。这允许你减少构建大量共享开头字符串的路由(如构建管理区域)所需的输入。

.. literalinclude:: routing/023.php

这将在 **users** 和 **blog** URI 前加上 **admin** 前缀,处理像 **admin/users** 和 **admin/blog** 这样的 URL。

设置命名空间
=================

如果你需要为组分配选项,比如 :ref:`assigning-namespace`,请在回调之前执行此操作:

.. literalinclude:: routing/024.php

这将处理指向 ``App\API\v1\Users`` 控制器的资源路由,URI 为 **api/users**。

设置过滤器
===============

你还可以为一组路由使用特定的 :doc:`过滤器 <filters>`。这将始终在控制器之前或之后运行过滤器。这在身份验证或 api 日志记录时特别方便:

.. literalinclude:: routing/025.php

过滤器的值必须匹配 **app/Config/Filters.php** 中定义的别名之一。

设置其他选项
=====================

在某些时候,你可能希望对路由分组以应用过滤器或其他路由配置选项,如命名空间、子域名等,而不一定需要为该组添加前缀。你可以在前缀位置传递空字符串,然后组中的路由将被路由,就像该组从未存在一样,但具有给定的路由配置选项:

.. literalinclude:: routing/027.php

嵌套分组
==============

如果需要,可以将组嵌套在组中进行更精细的组织:

.. literalinclude:: routing/026.php

这将处理 **admin/users/list** 的 URL。

.. note:: 传递给外部 ``group()`` 的选项(例如 ``namespace`` 和 ``filter``)不会与内部 ``group()`` 选项合并。

.. _routing-priority:

路由优先级
**************

路由以它们被定义的顺序注册到路由表中。这意味着当访问一个 URI 时,将执行第一个匹配的路由。

.. warning:: 如果使用不同的处理程序定义了一个路由路径多次,则只注册第一个定义的路由。

你可以通过运行 :ref:`spark routes <routing-spark-routes>` 命令来检查注册的路由。

更改路由优先级
=======================

在使用模块时,如果应用程序中的路由包含通配符,则可能会成为一个问题。
然后不会正确处理模块路由。
你可以通过使用路由选项中定义的 ``priority`` 降低路由处理的优先级来解决此问题。
该参数接受正整数和零。在 ``priority`` 中指定的数字越高,处理队列中的路由优先级越低:

.. literalinclude:: routing/043.php

要禁用此功能,你必须使用 ``false`` 参数调用该方法:

.. literalinclude:: routing/044.php

.. note:: 默认情况下,所有路由的优先级都是 0。
    负整数将转换为绝对值。

.. _routes-configuration-options:

路由配置选项
****************************

RouteCollection 类提供了几个选项,这些选项会影响所有路由,并可以根据你的应用程序需求进行修改。这些选项在 **app/Config/Routes.php** 的顶部可用。

.. _routing-default-namespace:

默认命名空间
=================

当匹配控制器与路由时,路由器会在路由指定的控制器前添加默认命名空间值。默认情况下,此值为 ``App\Controllers``。

如果将值设置为空字符串 (``''``),它会让每个路由指定完全限定名称的控制器:

.. literalinclude:: routing/045.php

如果你的控制器没有明确指定命名空间,则无需更改此设置。如果你对控制器指定了命名空间,则可以更改此值以节省输入:

.. literalinclude:: routing/046.php

转换 URI 破折号
====================

此选项允许你自动将控制器和方法的 URI 段中的破折号(``-``)替换为下划线,因此如果你需要这样做,可以节省额外的路由条目。这是必需的,因为破折号在类或方法名称中是无效的,如果尝试使用它会导致致命错误:

.. literalinclude:: routing/049.php

.. _use-defined-routes-only:

仅使用定义的路由
=======================

从 v4.2.0 开始,自动路由默认被禁用。

当没有找到匹配 URI 的定义路由时,如果启用了自动路由,系统将尝试将该 URI 与控制器和方法匹配。

你可以通过将 ``setAutoRoute()`` 选项设置为 false 来禁用这种自动匹配,
并将路由限制为你定义的路由:

.. literalinclude:: routing/050.php

.. warning:: 如果使用 :doc:`CSRF 保护 </libraries/security>`,它不会保护 **GET** 请求。
    如果 URI 通过 GET 方法可以访问,CSRF 保护将不起作用。

404 重写
============

当未找到与当前 URI 匹配的页面时,系统将显示一个通用的 404 视图。你可以通过 ``set404Override()`` 方法更改发生的操作。该值可以是与任何路由中的一样的有效类/方法对,或者是一个闭包:

.. literalinclude:: routing/051.php

.. note:: ``set404Override()`` 方法不会将响应状态码更改为 ``404``。
    如果你在设置的控制器中没有设置状态码,将返回默认状态码 ``200``。有关如何设置状态码的信息,请参见 :php:meth:`CodeIgniter\\HTTP\\Response::setStatusCode()`。

按优先级处理路由
============================

启用或禁用按优先级处理路由队列。通过在路由选项中定义降低优先级。默认禁用。此功能影响所有路由。
有关降低优先级的示例用法,请参阅 :ref:`routing-priority`:

.. literalinclude:: routing/052.php

.. _auto-routing-improved:

自动路由(改进版)
***********************

.. versionadded:: 4.2.0

从 v4.2.0 开始,引入了新的更安全的自动路由。

.. note:: 如果你熟悉自动路由,它在 CodeIgniter 3 到 4.1.x 中默认启用,你可以在
    :ref:`ChangeLog v4.2.0 <v420-new-improved-auto-routing>` 中看到差异。

当没有找到匹配 URI 的定义路由时,如果启用了自动路由,系统将尝试将该 URI 与控制器和方法匹配。

.. important:: 出于安全考虑,如果控制器在定义的路由中使用,自动路由(改进版)不会路由到该控制器。

自动路由可以根据约定自动路由 HTTP 请求,并执行相应的控制器方法。

.. note:: 自动路由(改进版)默认被禁用。要使用它,请参阅下文。

.. _enabled-auto-routing-improved:

启用自动路由
===================

要使用它,你需要在 **app/Config/Routes.php** 中将设置 ``setAutoRoute()`` 选项更改为 true::

    $routes->setAutoRoute(true);

并且你需要在 **app/Config/Feature.php** 中将属性 ``$autoRoutesImproved`` 更改为 ``true``::

    public bool $autoRoutesImproved = true;

URI 段
============

URL 中的段通常遵循模型-视图-控制器方法::

    example.com/class/method/ID

1. 第一个段表示应调用的控制器 **类**。
2. 第二个段表示应调用的类 **方法**。
3. 第三个和任何其他段表示将传递给控制器的 ID 和任何变量。

考虑这个 URI::

    example.com/index.php/helloworld/hello/1

在上面的示例中,当使用 **GET** 方法发送 HTTP 请求时,
自动路由会尝试找到一个名为 ``App\Controllers\Helloworld`` 的控制器,
并执行 ``getHello()`` 方法,并传递 ``'1'`` 作为第一个参数。

.. note:: 通过自动路由(改进版)执行的控制器方法需要 HTTP 动词(``get``、``post``、``put`` 等)前缀,如 ``getIndex()``、``postCreate()``。

有关更多信息,请参阅 :ref:`控制器中的自动路由 <controller-auto-routing-improved>`。

.. _routing-auto-routing-improved-configuration-options:

配置选项
=====================

这些选项在 **app/Config/Routes.php** 的顶部可用。

默认控制器
------------------

对于站点根 URI
^^^^^^^^^^^^^^^^^^

当用户访问站点的根目录(即 **example.com**)时,除非明确定义了路由,否则用于确定要使用的控制器的方法是由 ``setDefaultController()`` 方法设置的值。
默认值为 ``Home``,它与 **app/Controllers/Home.php** 中的控制器匹配:

.. literalinclude:: routing/047.php

对于目录 URI
^^^^^^^^^^^^^^^^^^

默认控制器也在没有找到匹配的路由且 URI 指向控制器目录中的目录时使用。
例如,如果用户访问 **example.com/admin**,如果在 **app/Controllers/Admin/Home.php** 中找到了一个控制器,则会使用它。

.. important:: 你无法使用控制器名称的 URI 访问默认控制器。
    当默认控制器为 ``Home`` 时,你可以访问 **example.com/**,但是如果访问 **example.com/home**,将找不到它。

参见 :ref:`控制器中的自动路由 <controller-auto-routing-improved>` 以获取更多信息。

默认方法
--------------

这与默认控制器设置的作用类似,但用于在找到与 URI 匹配的控制器但没有用于方法的段时,确定要使用的默认方法。默认值为 ``index``。

在此示例中,如果用户访问 **example.com/products**,并且存在 ``Products`` 控制器,
将执行 ``Products::listAll()`` 方法:

.. literalinclude:: routing/048.php

.. important:: 你无法使用默认方法名称的 URI 访问控制器。
    在上面的示例中,你可以访问 **example.com/products**,但是如果访问 **example.com/products/listall**,将找不到它。

.. _auto-routing-legacy:

自动路由(传统)
*********************

自动路由(传统)是 CodeIgniter 3 的路由系统。
它可以根据约定自动路由 HTTP 请求,并执行相应的控制器方法。

建议在 **app/Config/Routes.php** 文件中定义所有路由,
或使用 :ref:`auto-routing-improved`,

.. warning:: 为了防止配置错误和编码错误,我们建议你不要使用
    自动路由(传统)功能。很容易创建漏洞应用,其中控制器过滤器
    或 CSRF 保护被绕过。

.. important:: 自动路由(传统)将任何 HTTP 方法的 HTTP 请求路由到控制器方法。

启用自动路由(传统)
============================

从 v4.2.0 开始,自动路由默认被禁用。

要使用它,你需要在 **app/Config/Routes.php** 中将设置 ``setAutoRoute()`` 选项更改为 true::

    $routes->setAutoRoute(true);

URI 段(传统)
=====================

URL 中的段通常遵循模型-视图-控制器方法::

    example.com/class/method/ID

1. 第一个段表示应调用的控制器 **类**。
2. 第二个段表示应调用的类 **方法**。
3. 第三个和任何其他段表示将传递给控制器的 ID 和任何变量。

考虑这个 URI::

    example.com/index.php/helloworld/index/1

在上面的示例中,CodeIgniter 会尝试找到一个名为 **Helloworld.php** 的控制器,
并执行 ``index()`` 方法,并传递 ``'1'`` 作为第一个参数。

参见 :ref:`控制器中的自动路由(传统) <controller-auto-routing-legacy>` 以获取更多信息。

.. _routing-auto-routing-legacy-configuration-options:

配置选项(传统)
==============================

这些选项在 **app/Config/Routes.php** 的顶部可用。

默认控制器(传统)
---------------------------

对于站点根 URI(传统)
^^^^^^^^^^^^^^^^^^^^^^^^^^

当用户访问站点的根目录(即 example.com)时,除非明确定义了路由,否则用于确定要使用的控制器的方法是由 ``setDefaultController()`` 方法设置的值。默认值为 ``Home``,它与 **app/Controllers/Home.php** 中的控制器匹配:

.. literalinclude:: routing/047.php

对于目录 URI(传统)
^^^^^^^^^^^^^^^^^^^^^^^^^^

默认控制器也在没有找到匹配的路由且 URI 指向控制器目录中的目录时使用。
例如,如果用户访问 **example.com/admin**,如果在 **app/Controllers/Admin/Home.php** 中找到了一个控制器,则会使用它。

参见 :ref:`控制器中的自动路由(传统) <controller-auto-routing-legacy>` 以获取更多信息。

默认方法(传统)
-----------------------

这与默认控制器设置的作用类似,但用于在找到与 URI 匹配的控制器但没有用于方法的段时,确定要使用的默认方法。默认值为 ``index``。

在此示例中,如果用户访问 **example.com/products**,并且存在 ``Products`` 控制器,
将执行 ``Products::listAll()`` 方法:

.. literalinclude:: routing/048.php

确认路由
*****************

CodeIgniter 提供了以下 :doc:`命令 </cli/spark_commands>` 来显示所有路由。

.. _routing-spark-routes:

spark routes
============

显示所有路由和过滤器::

    > php spark routes

输出如下所示:

.. code-block:: none

    +---------+---------+---------------+-------------------------------+----------------+---------------+
    | 方法    | 路由    | 名称          | 处理程序                       | Before 过滤器 | After 过滤器 |
    +---------+---------+---------------+-------------------------------+----------------+---------------+
    | GET     | /       | »             | \App\Controllers\Home::index  |                | toolbar       |
    | GET     | feed    | »             | (Closure)                     |                | toolbar       |
    +---------+---------+---------------+-------------------------------+----------------+---------------+

*Method* 列显示路由正在监听的 HTTP 方法。

*Route* 列显示要匹配的路由路径。定义路由的路由路径以正则表达式表示。

自 v4.3.0 起,*Name* 列显示路由名称。``»`` 表示名称与路由路径相同。

.. important:: 该系统并不完美。如果使用自定义占位符,*Filters* 可能不正确。如果你想检查路由的过滤器,可以使用 :ref:`spark filter:check <spark-filter-check>` 命令。

自动路由(改进版)
-----------------------

当你使用自动路由(改进版)时,输出如下所示:

.. code-block:: none

    +-----------+-------------------------+---------------+-----------------------------------+----------------+---------------+
    | 方法      | 路由                    | 名称          | 处理程序                           | Before 过滤器 | After 过滤器 |
    +-----------+-------------------------+---------------+-----------------------------------+----------------+---------------+
    | GET(auto) | product/list/../..[/..] |               | \App\Controllers\Product::getList |                | toolbar       |
    +-----------+-------------------------+---------------+-----------------------------------+----------------+---------------+

*Method* 将是 ``GET(auto)``。

*Route* 列中的 ``/..`` 表示一个段。``[/..]`` 表示它是可选的。

.. note:: 当启用自动路由并且你有 ``home`` 路由时,它也可以通过 ``Home`` 或可能通过 ``hOme``、``hoMe``、``HOME`` 等访问,但命令将只显示 ``home``。

如果你看到以 ``x`` 开头的路由,如下所示,它表示一个无效的路由,不会路由,但控制器具有用于路由的公共方法。

.. code-block:: none

    +-----------+----------------+------+-------------------------------------+----------------+---------------+
    | 方法      | 路由            | 名称 | 处理程序                             | Before 过滤器 | After 过滤器 |
    +-----------+----------------+------+-------------------------------------+----------------+---------------+
    | GET(auto) | x home/foo     |      | \App\Controllers\Home::getFoo       | <未知>         | <未知>        |
    +-----------+----------------+------+-------------------------------------+----------------+---------------+

上面的示例向你显示了你具有 ``\App\Controllers\Home::getFoo()`` 方法,
但由于它是默认控制器(默认为 ``Home``),默认控制器名称必须在 URI 中省略,因此它不会路由。你应该删除 ``getFoo()`` 方法。

.. note:: 在 v4.3.4 之前,由于错误,无效路由会显示为正常路由。

自动路由(传统)
---------------------

当你使用自动路由(传统)时,输出如下所示:

.. code-block:: none

    +--------+--------------------+---------------+-----------------------------------+----------------+---------------+
    | 方法   | 路由                | 名称          | 处理程序                           | Before 过滤器 | After 过滤器 |
    +--------+--------------------+---------------+-----------------------------------+----------------+---------------+
    | auto   | product/list[/...] |               | \App\Controllers\Product::getList |                | toolbar       |
    +--------+--------------------+---------------+-----------------------------------+----------------+---------------+

*Method* 将是 ``auto``。

*Route* 列中的 ``[/...]`` 表示任意数量的段

.. note:: 当启用自动路由并且你有 ``home`` 路由时,它也可以通过 ``Home`` 或可能通过 ``hOme``、``hoMe``、``HOME`` 等访问,但命令将只显示 ``home``。

.. _routing-spark-routes-sort-by-handler:

按处理程序排序
---------------

.. versionadded:: 4.3.0

你可以按 *Handler* 对路由进行排序::

    > php spark routes -h
