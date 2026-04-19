####################
HTTP 功能测试
####################

功能测试用于查看应用程序单次调用的执行结果，涵盖返回单个 Web 表单结果、访问 API 接口等场景。此功能非常实用，支持测试单个请求的完整生命周期，从而确保路由正常工作、响应格式正确，并可对执行结果进行分析。

.. contents::
    :local:
    :depth: 2

测试类
==============

进行功能测试时，所有测试类均须使用 ``CodeIgniter\Test\DatabaseTestTrait`` 与 ``CodeIgniter\Test\FeatureTestTrait``。鉴于这些测试工具依赖正确的数据库初始化，若在类中重写了相关方法，务必确保调用 ``parent::setUp()`` 与 ``parent::tearDown()``。

.. literalinclude:: feature/001.php

.. _feature-requesting-a-page:

请求页面
=================

功能测试本质上就是调用应用上的某个接口并返回结果。为此，可使用 ``call()`` 方法。

1. 第一个参数是要使用的 HTTP 方法（最常用的是 ``GET`` 或 ``POST``）。
2. 第二个参数是要测试的站点 URI 路径。
3. 第三个参数 ``$params`` 接受一个数组，用于填充所使用的 HTTP 方法对应的超全局
   变量。因此，**GET** 方法会填充 ``$_GET`` 变量，而 **POST** 请求则会填充
   ``$_POST`` 数组。``$params`` 也可用于
   :ref:`feature-formatting-the-request`。

   .. note:: ``$params`` 数组并不适用于所有 HTTP 方法，但为保持一致性而保留。

.. literalinclude:: feature/002.php
   :lines: 2-

快捷方法
-----------------

为每个 HTTP 方法提供了快捷方法，以简化输入并使意图更清晰：

.. literalinclude:: feature/003.php
   :lines: 2-

设置不同路由
------------------------

可以通过将路由数组传递给 ``withRoutes()`` 方法来使用自定义路由集合，该方法会覆盖
系统中任何现有的路由：

.. literalinclude:: feature/004.php
   :lines: 2-

每个「路由」是一个包含 3 个元素的数组，包含 HTTP 方法（或使用 "add" 表示所有）、
要匹配的 URI 以及路由目标。

.. _feature-setting-session-values:

设置 Session 值
----------------------

可以使用 ``withSession()`` 方法在单个测试期间设置自定义 Session 值。该方法接受一个关联数组，
这些值在发出请求时会存在于 ``$_SESSION`` 变量中；也可传入 ``null``，
表示使用 ``$_SESSION`` 的当前值。这对于测试认证等场景很有用。

.. literalinclude:: feature/005.php
   :lines: 2-

设置 Header
---------------

使用 ``withHeaders()`` 方法可设置 Header 值。该方法接收一个关联数组，并将其作为 Header 随请求一同发送：

.. literalinclude:: feature/006.php
   :lines: 2-

跳过事件
----------------

事件在应用中很有用，但在测试期间可能会带来问题。尤其是用于发送邮件的事件。可以
使用 ``skipEvents()`` 方法告诉系统跳过任何事件处理：

.. literalinclude:: feature/007.php
   :lines: 2-

.. _feature-formatting-the-request:

格式化请求
-----------------------

使用 ``withBodyFormat()`` 方法可设置请求体格式，目前支持 ``json`` 与 ``xml``。
在测试 JSON 或 XML API 时，此功能可按控制器预期的格式构造请求。

该方法会自动将传给 ``call()``、``post()`` 或 ``get()`` 等方法的参数，按指定格式转换并填入请求体。

同时自动设置相应的 `Content-Type` 标头。

.. literalinclude:: feature/008.php
   :lines: 2-

.. _feature-setting-the-body:

设置请求体
----------------

可以使用 ``withBody()`` 方法设置请求体，可按需自行格式化请求体。
如果要测试更复杂的 XML，推荐使用此方法。

该方法不会自动设置 `Content-Type` 标头。如果需要，可以使用 ``withHeaders()`` 方法设置。

检查响应
=====================

``FeatureTestTrait::call()`` 返回一个 ``TestResponse`` 实例。有关如何在测试用例中
使用此类执行额外断言和验证，请参阅 :doc:`测试响应 <response>`。
