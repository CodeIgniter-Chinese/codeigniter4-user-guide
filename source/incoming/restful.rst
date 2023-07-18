#########################
RESTful 资源处理
#########################

.. contents::
    :local:
    :depth: 2

表述性状态转移(REST)是一种用于分布式应用程序的架构风格,首先由 Roy Fielding 在他的 2000 年博士论文 `《Architectural Styles and the Design of Network-based Software Architectures》 <https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm>`_ 中描述。这可能有点枯燥,你可能会发现 Martin Fowler 的 `《Richardson 成熟度模型》 <https://martinfowler.com/articles/richardsonMaturityModel.html>`_ 是一个更温和的介绍。

REST 的解释和误解的方式比大多数软件体系结构都要多,可以说你在体系结构中采用的 Roy Fielding 原则越多,你的应用程序就越被认为是“RESTful”。

CodeIgniter 通过其资源路由和 `ResourceController` 可以轻松创建资源的 RESTful API。

***************
资源路由
***************

你可以使用 ``resource()`` 方法快速为单个资源创建一小 handful 的 RESTful 路由。这会创建完全 CRUD 资源所需的最常见的 5 个路由:创建新资源、更新现有资源、列出所有该资源、显示单个资源以及删除单个资源。第一个参数是资源名称:

.. literalinclude:: restful/001.php

.. note:: 上面的顺序是为了清晰起见,而实际创建路由的顺序在 RouteCollection 中确保了正确的路由解析

.. important:: 路由按指定顺序匹配,因此如果你在上方有一个资源 photos,然后有一个 get 'photos/poll',资源线的 show 操作的路由将在 get 线之前匹配。要解决此问题,请将 get 行移动到资源行之上,以便先匹配它。

第二个参数接受可以用于修改生成的路由的选项数组。虽然这些路由面向 API 使用,其中允许更多方法,但你可以传入 ``websafe`` 选项,使其生成适用于 HTML 表单的 update 和 delete 方法:

.. literalinclude:: restful/002.php

更改使用的控制器
==========================

你可以通过使用应该使用的控制器的名称传递 ``controller`` 选项来指定应该使用的控制器:

.. literalinclude:: restful/003.php

更改使用的占位符
===========================

默认情况下,当需要资源 ID 时,会使用 ``(:segment)`` 占位符。你可以通过传递 ``placeholder`` 选项及要使用的新字符串来更改此占位符:

.. literalinclude:: restful/004.php

限制生成的路由
=====================

你可以使用 ``only`` 选项限制生成的路由。这应该是 **数组** 或 **以逗号分隔的方法名列表**,应该创建这些方法。仅将创建与这些方法之一匹配的路由。其余的会被忽略:

.. literalinclude:: restful/005.php

否则,你可以使用 ``except`` 选项删除未使用的路由。这也应该是 **数组** 或 **以逗号分隔的方法名列表**。此选项在 ``only`` 之后运行:

.. literalinclude:: restful/006.php

有效的方法是:``index``、``show``、``create``、``update``、``new``、``edit`` 和 ``delete``。

******************
ResourceController
******************

``ResourceController`` 为你的 RESTful API 提供了一个方便的起点,其方法对应于上面的资源路由。

扩展它,覆盖 ``modelName`` 和 ``format`` 属性,然后实现你想要处理的那些方法:

.. literalinclude:: restful/007.php

路由如下:

.. literalinclude:: restful/008.php

****************
Presenter 路由
****************

你可以使用 ``presenter()`` 方法快速创建与资源控制器对齐的表示控制器。
这将创建对应于上面的资源控制器方法的路由,这些方法会为你的资源返回视图,
或处理来自这些视图的表单提交。

这不是必需的,因为表示可以通过常规控制器处理 - 这只是为了方便。
其用法与资源路由类似:

.. literalinclude:: restful/009.php

.. note:: 上面的顺序是为了清晰起见,而实际创建路由的顺序在 RouteCollection 中确保了正确的路由解析

你不会为资源和表示控制器都有 `photos` 路由。
你需要加以区分,例如:

.. literalinclude:: restful/010.php

第二个参数接受可以用于修改生成的路由的选项数组。

更改使用的控制器
==========================

你可以通过使用应该使用的控制器的名称传递 ``controller`` 选项来指定应该使用的控制器:

.. literalinclude:: restful/011.php

更改使用的占位符
===========================

默认情况下,当需要资源 ID 时,会使用 ``(:segment)`` 占位符。你可以通过传递 ``placeholder`` 选项及要使用的新字符串来更改此占位符:

.. literalinclude:: restful/012.php

限制生成的路由
=====================

你可以使用 ``only`` 选项限制生成的路由。这应该是 **数组** 或 **以逗号分隔的方法名列表**,应该创建这些方法。仅将创建与这些方法之一匹配的路由。其余的会被忽略:

.. literalinclude:: restful/013.php

否则,你可以使用 ``except`` 选项删除未使用的路由。这也应该是 **数组** 或 **以逗号分隔的方法名列表**。此选项在 ``only`` 之后运行:

.. literalinclude:: restful/014.php

有效的方法是:``index``、``show``、``new``、``create``、``edit``、``update``、``remove`` 和 ``delete``。

*****************
ResourcePresenter
*****************

``ResourcePresenter`` 为呈现资源视图以及处理这些视图中的表单数据提供了一个方便的起点,其方法与上面的资源路由对齐。

扩展它,重写 ``modelName`` 属性,然后实现你想要处理的方法:

.. literalinclude:: restful/015.php

路由如下:

.. literalinclude:: restful/016.php

*******************************
Presenter/Controller 对比
*******************************

此表比较了 `resource()` 和 `presenter()` 创建的默认路由及其相应的 Controller 函数。

================ ========= ====================== ======================== ====================== ======================
操作              方法      控制器路由             表示器路由              控制器函数             表示器函数
================ ========= ====================== ======================== ====================== ======================
**New**          GET       photos/new             photos/new               ``new()``              ``new()``
**Create**       POST      photos                 photos                   ``create()``           ``create()``
创建(别名)       POST                             photos/create                                   ``create()``
**List**         GET       photos                 photos                   ``index()``            ``index()``
**Show**         GET       photos/(:segment)      photos/(:segment)        ``show($id = null)``   ``show($id = null)``
显示(别名)       GET                              photos/show/(:segment)                          ``show($id = null)``
**Edit**         GET       photos/(:segment)/edit photos/edit/(:segment)   ``edit($id = null)``   ``edit($id = null)``
**Update**       PUT/PATCH photos/(:segment)                               ``update($id = null)``
更新(网页安全)    POST      photos/(:segment)      photos/update/(:segment) ``update($id = null)`` ``update($id = null)``
**Remove**       GET                              photos/remove/(:segment)                        ``remove($id = null)``
**Delete**       DELETE    photos/(:segment)                               ``delete($id = null)``
删除(网页安全)    POST                             photos/delete/(:segment) ``delete($id = null)`` ``delete($id = null)``
================ ========= ====================== ======================== ====================== ======================
