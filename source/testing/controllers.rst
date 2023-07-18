###################
测试控制器
###################

几个新帮助类和 trait 使得测试控制器变得方便。在测试控制器时,你可以执行控制器中的代码,而无需先运行整个应用程序引导过程。
通常,使用 :doc:`功能测试工具 <feature>` 将更简单,但如果需要,此功能仍可提供。

.. note:: 由于整个框架没有启动,所以有时你无法以这种方式测试控制器。

.. contents::
    :local:
    :depth: 2

帮助 Trait
================

要启用控制器测试,你需要在测试中使用 ``ControllerTestTrait`` trait:

.. literalinclude:: controllers/001.php

一旦包含了trait,你就可以开始设置环境,包括请求和响应类、请求体、URI等。你可以使用 ``controller()`` 方法指定要使用的控制器,传入控制器的完全限定类名。最后,用要运行的方法名作为参数调用 ``execute()`` 方法:

.. literalinclude:: controllers/002.php

帮助方法
==============

controller($class)
------------------

指定要测试的控制器的类名。第一个参数必须是完全限定的类名(即包含命名空间):

.. literalinclude:: controllers/003.php

execute(string $method, ...$params)
-----------------------------------

在控制器内执行指定的方法。第一个参数是要运行的方法名:

.. literalinclude:: controllers/004.php

通过指定第二个和后续参数,你可以将它们传递给控制器方法。

这将返回一个新的帮助类,它提供了许多用于检查响应本身的例程。有关详细信息,请参阅下文。

withConfig($config)
-------------------

允许你传入修改后的 **app/Config/App.php** 以使用不同设置进行测试:

.. literalinclude:: controllers/005.php

如果未提供,将使用应用程序的 App 配置文件。

withRequest($request)
---------------------

允许你提供适合测试需求的 **IncomingRequest** 实例:

.. literalinclude:: controllers/006.php

如果未提供,将使用具有默认应用程序值的新的 IncomingRequest 实例传入控制器。

withResponse($response)
-----------------------

允许你提供 **Response** 实例:

.. literalinclude:: controllers/007.php

如果未提供,将使用具有默认应用程序值的新的 Response 实例传入控制器。

withLogger($logger)
-------------------

允许你提供 **Logger** 实例:

.. literalinclude:: controllers/008.php

如果未提供,将使用具有默认配置值的新的 Logger 实例传入控制器。

withURI(string $uri)
--------------------

允许你提供新的 URI,模拟客户端访问此控制器时的 URL。如果你需要在控制器中检查 URI 片段,这很有帮助。唯一的参数是一个表示有效 URI 的字符串:

.. literalinclude:: controllers/009.php

在测试期间始终提供 URI 可以避免意外情况,这是一种好的实践。

withBody($body)
---------------

允许你为请求提供自定义主体。当测试 API 控制器并需要将 JSON 值设置为主体时,这很有用。唯一的参数是一个表示请求主体的字符串:

.. literalinclude:: controllers/010.php

检查响应
=====================

``ControllerTestTrait::execute()`` 返回 ``TestResponse`` 的一个实例。请参见 :doc:`测试响应 <response>` 以了解如何使用此类在测试用例中执行其他断言和验证。

过滤器测试
==============

与控制器测试类似,框架提供了工具来帮助针对自定义 :doc:`过滤器 </incoming/filters>` 及项目中的使用方式进行测试。

Helper Trait
----------------

与控制器测试器一样,你需要在测试用例中包含 ``FilterTestTrait`` 来启用这些功能:

.. literalinclude:: controllers/011.php

配置
-------------

由于与控制器测试的逻辑重叠,``FilterTestTrait`` 旨在与 ``ControllerTestTrait`` 一起使用,如果同一个类需要两者。
一旦包含了 trait,``CIUnitTestCase`` 将检测其 ``setUp`` 方法并准备测试所需的所有组件。如果需要特殊配置,可以在调用支持方法之前更改任何属性:

* ``$request`` 准备好的默认 ``IncomingRequest`` 服务的版本
* ``$response`` 准备好的默认 ``ResponseInterface`` 服务的版本
* ``$filtersConfig`` 默认的 ``Config\Filters`` 配置(注意:发现由 ``Filters`` 处理,所以不会包括模块别名)
* ``$filters`` 使用上述三个组件的 ``CodeIgniter\Filters\Filters`` 实例
* ``$collection`` 准备好的 ``RouteCollection`` 版本,其中包括 ``Config\Routes`` 的发现

默认配置通常对测试最有利,因为它最接近“实时”项目,但是(例如)如果要模拟过滤器意外触发未过滤的路由,可以将其添加到 Config 中:

.. literalinclude:: controllers/012.php

检查路由
---------------

第一个帮助方法是 ``getFiltersForRoute()``,它将模拟提供的路由并返回将为给定位置(“before”或“after”)运行的所有过滤器列表(按其别名),而不实际执行任何控制器或路由代码。这比控制器和 HTTP 测试具有很大的性能优势。

.. php:function:: getFiltersForRoute($route, $position)

    :param    string    $route: 要检查的URI
    :param    string    $position: 要检查的过滤器方法,“before”或“after”
    :returns:    将运行的每个过滤器的别名
    :rtype:    string[]

    用法示例:

    .. literalinclude:: controllers/013.php

调用过滤器方法
----------------------

配置中描述的属性都设置好了,以确保不干扰或不受其他测试的干扰的最大性能。下一个帮助方法将使用这些属性返回一个可调用的方法来安全地测试过滤器代码并检查结果。

.. php:function:: getFilterCaller($filter, $position)

    :param    FilterInterface|string    $filter: 过滤器实例、类或别名
    :param    string    $position: 要运行的过滤器方法,“before”或“after”
    :returns:    模拟过滤器事件的可调用方法
    :rtype:    Closure

    用法示例:

    .. literalinclude:: controllers/014.php

    请注意,``Closure`` 可以接受输入参数,这些参数会传入过滤器方法。

断言
----------

除了上面的帮助方法之外,``FilterTestTrait`` 还带有一些断言来简化测试方法。

assertFilter()
^^^^^^^^^^^^^^

``assertFilter()`` 方法检查给定路由在指定位置使用了过滤器(按其别名):

.. literalinclude:: controllers/015.php

assertNotFilter()
^^^^^^^^^^^^^^^^^

``assertNotFilter()`` 方法检查给定路由在指定位置没有使用过滤器(按其别名):

.. literalinclude:: controllers/016.php

assertHasFilters()
^^^^^^^^^^^^^^^^^^

``assertHasFilters()`` 方法检查给定路由在指定位置至少设置了一个过滤器:

.. literalinclude:: controllers/017.php

assertNotHasFilters()
^^^^^^^^^^^^^^^^^^^^^

``assertNotHasFilters()`` 方法检查给定路由在指定位置没有设置任何过滤器:

.. literalinclude:: controllers/018.php
