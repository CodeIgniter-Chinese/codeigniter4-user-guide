###################
测试控制器
###################

新增的辅助类与 Trait 使测试控制器更加便捷。测试控制器时，可直接运行控制器内部代码，无需经历完整的应用引导流程。通常使用 :doc:`功能测试工具 <feature>` 会更简便，但若有特殊需求，也可使用此功能。

.. note:: 由于未引导整个框架，某些情况下可能无法以此方式测试控制器。

.. contents::
    :local:
    :depth: 2

辅助 Trait
================

要启用控制器测试，需在测试中使用 ``ControllerTestTrait``：

.. literalinclude:: controllers/001.php

引入此 Trait 后，即可开始设置环境，包括请求和响应类、请求体、URI 等。通过 ``controller()`` 方法指定要使用的控制器，传入控制器的完全限定类名。最后，调用 ``execute()`` 方法，将方法名作为参数传入：

.. literalinclude:: controllers/002.php

辅助方法
==============

controller($class)
------------------

指定要测试的控制器类名。第一个参数必须是完全限定类名（即包含命名空间）：

.. literalinclude:: controllers/003.php

execute(string $method, ...$params)
-----------------------------------

在控制器内执行指定方法。第一个参数是要运行的方法名：

.. literalinclude:: controllers/004.php

通过指定第二个及后续参数，可将其传递给控制器方法。

此方法返回一个新的辅助类，提供多种检查响应的例程。详见下文。

withConfig($config)
-------------------

支持传入修改后的 **app/Config/App.php**，以测试不同设置：

.. literalinclude:: controllers/005.php

如未提供，将使用应用的 App 配置文件。

withRequest($request)
---------------------

可根据测试需求提供定制的 **IncomingRequest** 实例：

.. literalinclude:: controllers/006.php

如未提供，将创建一个使用应用默认值的全新 IncomingRequest 实例并传入控制器。

withResponse($response)
-----------------------

可提供 **Response** 实例：

.. literalinclude:: controllers/007.php

如未提供，将创建一个使用应用默认值的全新 Response 实例并传入控制器。

withLogger($logger)
-------------------

可提供 **Logger** 实例：

.. literalinclude:: controllers/008.php

如未提供，将创建一个使用默认配置值的全新 Logger 实例并传入控制器。

withUri(string $uri)
--------------------

用于提供新 URI，模拟控制器运行时的客户端访问 URL。如需在控制器内检查 URI 片段，此方法非常有用。唯一参数是代表有效 URI 的字符串：

.. literalinclude:: controllers/009.php

测试时始终提供 URI 是良好的实践，可避免意外情况。

.. note:: 自 v4.4.0 起，此方法会创建带 URI 的新 Request 实例。
    因为 Request 实例应包含 URI 实例。此外，如果 URI 字符串中的主机名
    与 ``Config\App`` 不匹配，将设置有效的主机名。

withBody($body)
---------------

可自定义请求体。测试 API 控制器时，如需将 JSON 数据设为请求体，此功能非常实用。唯一参数是代表请求体的字符串：

.. literalinclude:: controllers/010.php

检查响应
=====================

``ControllerTestTrait::execute()`` 返回 ``TestResponse`` 实例。有关如何在测试用例中使用此类执行额外断言和验证，请参阅 :doc:`Testing Responses <response>`。

测试过滤器
==============

与控制器测试类似，框架提供的工具可用于测试自定义 :doc:`过滤器 </incoming/filters>` 及其在路由中的应用。

辅助 Trait
----------------

与控制器测试一样，需在测试用例中引入 ``FilterTestTrait`` 以启用这些功能：

.. literalinclude:: controllers/011.php

配置
-------------

由于与控制器测试逻辑重合，``FilterTestTrait`` 可与 ``ControllerTestTrait`` 搭配使用，方便在同一个类中同时调用。
引入此 Trait 后，``CIUnitTestCase`` 会自动检测其 ``setUp`` 方法，并准备测试所需的所有组件。如需特殊配置，可在调用支持方法前修改相关属性：

* ``$request``：已就绪的默认 ``IncomingRequest`` 服务实例
* ``$response``：已就绪的默认 ``ResponseInterface`` 服务实例
* ``$filtersConfig``：默认 ``Config\Filters`` 配置（注：自动发现由 ``Filters`` 类处理，因此此处不包含模块别名）
* ``$filters``：使用上述三个组件生成的 ``CodeIgniter\Filters\Filters`` 实例
* ``$collection``：已就绪的 ``RouteCollection`` 实例，包含对 ``Config\Routes`` 的自动发现

默认配置最接近真实运行的项目，通常是测试的首选。但若需模拟过滤器在未配置过滤器的路由上意外触发等情况，可将其手动添加到配置中：

.. literalinclude:: controllers/012.php

检查路由
---------------

第一个辅助方法 ``getFiltersForRoute()`` 用于模拟指定路由，并返回在特定位置（“before” 或 “after”）本应运行的所有过滤器别名列表。由于该方法不会实际执行任何控制器或路由代码，其性能表现远胜于控制器测试与 HTTP 测试。

.. php:function:: getFiltersForRoute($route, $position)

    :param    string    $route: 要检查的 URI
    :param    string    $position: 要检查的过滤器方法，"before" 或 "after"
    :returns:    将运行的每个过滤器的别名
    :rtype:    string[]

    使用示例：

    .. literalinclude:: controllers/013.php

调用过滤器方法
----------------------

配置中描述的属性均已设置，以确保在不干扰其他测试的前提下实现最佳性能。下一个辅助方法将使用这些属性返回一个可调用的方法，以安全地测试过滤器代码并检查结果。

.. php:function:: getFilterCaller($filter, $position)

    :param    FilterInterface|string    $filter: 过滤器实例、类或别名
    :param    string    $position: 要运行的过滤器方法，"before" 或 "after"
    :returns:    运行模拟过滤器事件的可调用方法
    :rtype:    Closure

    使用示例：

    .. literalinclude:: controllers/014.php

    注意 ``Closure`` 可接受输入参数，这些参数会传递给过滤器方法。

断言
----------

除上述辅助方法外，``FilterTestTrait`` 还提供一些断言，可简化测试方法。

assertFilter()
^^^^^^^^^^^^^^

``assertFilter()`` 方法检查指定位置的给定路由是否使用了该过滤器（通过别名）：

.. literalinclude:: controllers/015.php

assertNotFilter()
^^^^^^^^^^^^^^^^^

``assertNotFilter()`` 方法检查指定位置的给定路由是否未使用该过滤器（通过别名）：

.. literalinclude:: controllers/016.php

assertHasFilters()
^^^^^^^^^^^^^^^^^^

``assertHasFilters()`` 方法检查指定位置的给定路由是否至少设置了一个过滤器：

.. literalinclude:: controllers/017.php

assertNotHasFilters()
^^^^^^^^^^^^^^^^^^^^^

``assertNotHasFilters()`` 方法检查指定位置的给定路由是否未设置任何过滤器：

.. literalinclude:: controllers/018.php
