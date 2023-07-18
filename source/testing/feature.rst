####################
HTTP 功能测试
####################

功能测试允许您查看对应用程序的单次调用的结果。这可能是返回单个网页表单的结果,访问 API 端点等等。这很方便,因为它允许您测试单个请求的整个生命周期,确保路由工作正常,响应格式正确,分析结果等等。

.. contents::
    :local:
    :depth: 2

测试类
==============

功能测试要求所有测试类使用 ``CodeIgniter\Test\DatabaseTestTrait`` 和 ``CodeIgniter\Test\FeatureTestTrait`` traits。由于这些测试工具依赖于适当的数据库准备,如果实现自己的方法,必须始终确保调用 ``parent::setUp()`` 和 ``parent::tearDown()``。

.. literalinclude:: feature/001.php

请求页面
=================

从本质上讲,功能测试只是允许您在应用程序上调用一个端点并获取结果。要做到这一点,请使用 ``call()`` 方法。第一个参数是要使用的 HTTP 方法(最常见的是 GET 或 POST)。第二个参数是要测试的站点上的路径。第三个参数接受一个数组,用于填充与您使用的 HTTP 动词对应的全局变量。因此,**GET** 方法会填充 **$_GET** 变量,**post** 请求会填充 **$_POST** 数组。

.. literalinclude:: feature/002.php

为每个 HTTP 动词提供了缩写方法,以减少输入并增加清晰度:

.. literalinclude:: feature/003.php

.. note:: 并非每个 HTTP 动词都适合 ``$params`` 数组,但为了一致性而包含它。

设置不同的路由
------------------------

您可以通过将“routes”数组传递到 ``withRoutes()`` 方法来使用自定义路由集合。这将覆盖系统中的任何现有路由:

.. literalinclude:: feature/004.php

每个“routes”都是一个包含 HTTP 动词(或“add”表示全部)、要匹配的 URI 和路由目的地的 3 元素数组。

设置会话值
----------------------

您可以使用 ``withSession()`` 方法在单次测试期间设置自定义会话值。这需要一个键/值对数组,在发出此请求时,它应存在于 ``$_SESSION`` 变量中,或者为 ``null`` 表示应使用 ``$_SESSION`` 的当前值。这在测试认证等方面很有用。

.. literalinclude:: feature/005.php

设置标头
---------------

您可以使用 ``withHeaders()`` 方法设置标头值。这需要一个键/值对数组,它将作为调用中的标头传递:

.. literalinclude:: feature/006.php

绕过事件
----------------

事件在应用程序中很有用,但在测试中可能 problematic。特别是用于发送电子邮件的事件。您可以使用 ``skipEvents()`` 方法告诉系统跳过任何事件处理:

.. literalinclude:: feature/007.php

格式化请求
-----------------------

您可以使用 ``withBodyFormat()`` 方法设置请求正文的格式。当前,这支持 `json` 或 `xml`。这将获取传递到 ``call()``、``post()``、``get()`` 等中的参数,并以给定格式分配给请求正文。这也会相应地为请求设置 `Content-Type` 标头。当测试 JSON 或 XML API 时,这很有用,以便以控制器期望的形式设置请求。

.. literalinclude:: feature/008.php

设置正文
----------------

您可以使用 ``withBody()`` 方法设置请求的正文。这允许您按照想要的格式设置正文格式。如果要测试更复杂的 XML,建议使用此方法。这也不会为您设置 Content-Type 标头,如果需要,可以使用 ``withHeaders()`` 方法设置它。

检查响应
=====================

``FeatureTestTrait::call()`` 返回 ``TestResponse`` 的一个实例。请参阅 :doc:`测试响应 <response>` 以了解如何使用此类在测试用例中执行其他断言和验证。
