####################
HTTP 功能测试
####################

功能测试允许你查看对应用程序的单次调用的结果。这可能是返回单个网页表单的结果,访问 API 端点等等。这很方便,因为它允许你测试单个请求的整个生命周期,确保路由工作正常,响应格式正确,分析结果等等。

.. contents::
    :local:
    :depth: 2

测试类
==============

功能测试要求所有测试类使用 ``CodeIgniter\Test\DatabaseTestTrait`` 和 ``CodeIgniter\Test\FeatureTestTrait`` traits。由于这些测试工具依赖于适当的数据库准备,如果实现自己的方法,必须始终确保调用 ``parent::setUp()`` 和 ``parent::tearDown()``。

.. literalinclude:: feature/001.php

.. _feature-requesting-a-page:

请求页面
=================

基本上，功能测试允许您调用应用程序上的一个端点，并获取结果返回。
为此，您可以使用 ``call()`` 方法。

1. 第一个参数是要使用的 HTTP 方法（通常是 GET 或 POST）。
2. 第二个参数是要测试的站点上的 URI 路径。
3. 第三个参数 ``$params`` 接受一个数组，用于填充您正在使用的 HTTP 动词的超全局变量。因此，**GET** 方法将填充 **$_GET** 变量，而 **POST** 请求将填充 **$_POST** 数组。``$params`` 也用于 :ref:`feature-formatting-the-request`。

   .. note:: ``$params`` 数组并不适用于每个 HTTP 动词，但为了保持一致性而包含在内。

.. literalinclude:: feature/002.php

缩写方法
-----------------

为每个 HTTP 动词提供了缩写方法,以减少输入并增加清晰度:

.. literalinclude:: feature/003.php

设置不同的路由
------------------------

你可以通过将“routes”数组传递到 ``withRoutes()`` 方法来使用自定义路由集合。这将覆盖系统中的任何现有路由:

.. literalinclude:: feature/004.php

每个“routes”都是一个包含 HTTP 动词(或“add”表示全部)、要匹配的 URI 和路由目的地的 3 元素数组。

设置会话值
----------------------

你可以使用 ``withSession()`` 方法在单次测试期间设置自定义会话值。这需要一个键/值对数组,在发出此请求时,它应存在于 ``$_SESSION`` 变量中,或者为 ``null`` 表示应使用 ``$_SESSION`` 的当前值。这在测试认证等方面很有用。

.. literalinclude:: feature/005.php

设置标头
---------------

你可以使用 ``withHeaders()`` 方法设置标头值。这需要一个键/值对数组,它将作为调用中的标头传递:

.. literalinclude:: feature/006.php

绕过事件
----------------

事件在应用程序中很有用,但在测试中可能 problematic。特别是用于发送电子邮件的事件。你可以使用 ``skipEvents()`` 方法告诉系统跳过任何事件处理:

.. literalinclude:: feature/007.php

.. _feature-formatting-the-request:

格式化请求
-----------------------

您可以使用 ``withBodyFormat()`` 方法设置请求体的格式。目前支持 ``json`` 或 ``xml``。
这在测试 JSON 或 XML API 时非常有用，因为您可以设置请求的格式，以符合控制器的预期。

这将接收传递给 ``call()``, ``post()``, ``get()``... 的参数，并将它们分配给请求体，以给定的格式。

这还将相应地设置请求的 `Content-Type` 标头。

.. literalinclude:: feature/008.php

.. _feature-setting-the-body:

设置 Body
----------------

您可以使用 ``withBody()`` 方法设置请求的 Body。这允许您按照所需的格式设置请求 Body。如果您有更复杂的 XML 需要测试，建议使用此方法。

这不会为您设置 `Content-Type` 标头。如果需要，您可以使用 ``withHeaders()`` 方法设置它。

检查响应
=====================

``FeatureTestTrait::call()`` 返回 ``TestResponse`` 的一个实例。请参阅 :doc:`测试响应 <response>` 以了解如何使用此类在测试用例中执行其他断言和验证。
