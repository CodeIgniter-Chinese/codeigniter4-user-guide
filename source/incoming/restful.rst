#########################
RESTful 资源处理
#########################

.. contents::
    :local:
    :depth: 2

Representational State Transfer (REST) 是一种分布式应用的架构风格，最早由 Roy Fielding 在其 2000 年的博士论文 `Architectural Styles and
the Design of Network-based Software Architectures
<https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm>`_ 中提出。
那篇论文读起来可能略显枯燥晦涩，相比之下，你可能会觉得 Martin Fowler 的 `Richardson Maturity Model <https://martinfowler.com/articles/richardsonMaturityModel.html>`_
是一份更通俗易懂的入门读物。

相比大多数软件架构，REST 承载了太多的解读与误读。简单来说，你的架构遵循 Roy Fielding 的原则越多，你的应用程序就越符合“RESTful”的标准。

CodeIgniter 通过其资源路由和 `ResourceController`，使得为你的资源创建 RESTful API 变得很容易。

***************
资源路由
***************

你可以使用 ``resource()`` 方法快速为一个资源创建一组 RESTful 路由。这会创建资源的完整 CRUD 所需的最常见的五个路由：创建新资源、更新现有资源、列出所有资源、显示单个资源和删除单个资源。第一个参数是资源名称：

.. literalinclude:: restful/001.php

.. note:: 上面的顺序是为了清晰起见，而在 RouteCollection 中创建路由的实际顺序确保了正确的路由解析。

.. important:: 路由是按照指定的顺序匹配的，所以如果你在 get 'photos/poll' 之前定义了资源 photos，那么资源的 show 操作的路由行会在 get 行之前被匹配。为了解决这个问题，将 get 行移到 resource 行之前，以便它被优先匹配。

第二个参数接受一个选项数组，可用于修改生成的路由。虽然这些路由是针对 API 使用的（允许更多的方法），但你可以传入 ``websafe`` 选项，使其生成的更新和删除方法能与 HTML 表单一起工作：

.. literalinclude:: restful/002.php

更改使用的控制器
==========================

你可以通过传入 ``controller`` 选项并指定控制器的名称来指定应使用的控制器：

.. literalinclude:: restful/003.php

.. literalinclude:: restful/017.php

.. literalinclude:: restful/018.php

另见 :ref:`controllers-namespace`。

更改使用的占位符
===========================

默认情况下，当需要资源 ID 时使用 ``(:segment)`` 占位符。你可以通过传入 ``placeholder`` 选项并指定要使用的新字符串来更改它：

.. literalinclude:: restful/004.php

限制生成的路由
=====================

你可以使用 ``only`` 选项限制生成的路由。这应该是要创建的方法名称的 **数组** 或 **逗号分隔列表**。只有匹配这些方法的路由才会被创建。其余的将被忽略：

.. literalinclude:: restful/005.php

否则你可以使用 ``except`` 选项移除未使用的路由。这也应该是方法名称的 **数组** 或 **逗号分隔列表**。此选项在 ``only`` 之后运行：

.. literalinclude:: restful/006.php

有效的方法有：``index``、``show``、``create``、``update``、``new``、``edit`` 和 ``delete``。

******************
ResourceController
******************

``ResourceController`` 为你的 RESTful API 提供了一个便捷的起点，其方法对应于上面的资源路由。

继承它，重写 ``modelName`` 和 ``format`` 属性，然后实现你想要处理的那些方法：

.. literalinclude:: restful/007.php

其路由将是：

.. literalinclude:: restful/008.php

****************
展示器路由
****************

你可以使用 ``presenter()`` 方法快速创建一个与资源控制器对齐的展示控制器。这将为控制器方法创建路由，这些方法将返回你的资源的视图，或处理从这些视图提交的表单。

这不是必须的，因为展示可以通过常规控制器来处理——这只是为了方便。它的用法类似于资源路由：

.. literalinclude:: restful/009.php

.. note:: 上面的顺序是为了清晰起见，而在 RouteCollection 中创建路由的实际顺序确保了正确的路由解析。

你不应让资源控制器和展示器控制器同时使用 `photos` 这一路由。你需要将它们区分开来，例如：

.. literalinclude:: restful/010.php

第二个参数接受一个选项数组，可用于修改生成的路由。

更改使用的控制器
==========================

你可以通过传入 ``controller`` 选项并指定控制器的名称来指定应使用的控制器：

.. literalinclude:: restful/011.php

.. literalinclude:: restful/019.php

.. literalinclude:: restful/020.php

另见 :ref:`controllers-namespace`。

更改使用的占位符
===========================

默认情况下，当需要资源 ID 时使用 ``(:segment)`` 占位符。你可以通过传入 ``placeholder`` 选项并指定要使用的新字符串来更改它：

.. literalinclude:: restful/012.php

限制生成的路由
=====================

你可以使用 ``only`` 选项限制生成的路由。这应该是要创建的方法名称的 **数组** 或 **逗号分隔列表**。只有匹配这些方法的路由才会被创建。其余的将被忽略：

.. literalinclude:: restful/013.php

否则你可以使用 ``except`` 选项移除未使用的路由。这也应该是方法名称的 **数组** 或 **逗号分隔列表**。此选项在 ``only`` 之后运行：

.. literalinclude:: restful/014.php

有效的方法有：``index``、``show``、``new``、``create``、``edit``、``update``、``remove`` 和 ``delete``。

*****************
ResourcePresenter
*****************

``ResourcePresenter`` 为展示资源视图以及处理这些视图中的表单数据提供了一个便捷的起点，其方法与上面的资源路由相对应。

继承它，重写 ``modelName`` 属性，然后实现你想要处理的那些方法：

.. literalinclude:: restful/015.php

其路由将是：

.. literalinclude:: restful/016.php

*******************************
展示器/控制器对比
*******************************

此表展示了 ``resource()`` 和 ``presenter()`` 创建的默认路由及其对应的控制器函数的对比。

================ ========= ====================== ======================== ====================== ======================
操作             方法      控制器路由             展示器路由               控制器函数             展示器函数
================ ========= ====================== ======================== ====================== ======================
**新建**         GET       photos/new             photos/new               ``new()``              ``new()``
**创建**         POST      photos                 photos                   ``create()``           ``create()``
创建（别名）     POST                             photos/create                                   ``create()``
**列表**         GET       photos                 photos                   ``index()``            ``index()``
**显示**         GET       photos/(:segment)      photos/(:segment)        ``show($id = null)``   ``show($id = null)``
显示（别名）     GET                              photos/show/(:segment)                          ``show($id = null)``
**编辑**         GET       photos/(:segment)/edit photos/edit/(:segment)   ``edit($id = null)``   ``edit($id = null)``
**更新**         PUT/PATCH photos/(:segment)                               ``update($id = null)``
更新（websafe）  POST      photos/(:segment)      photos/update/(:segment) ``update($id = null)`` ``update($id = null)``
**移除**         GET                              photos/remove/(:segment)                        ``remove($id = null)``
**删除**         DELETE    photos/(:segment)                               ``delete($id = null)``
删除（websafe）  POST                             photos/delete/(:segment) ``delete($id = null)`` ``delete($id = null)``
================ ========= ====================== ======================== ====================== ======================
