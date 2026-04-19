###############
Session 测试
###############

使用 ArrayHandler Session 驱动，可轻松测试应用程序中的 Session 行为。
与其他 Session 驱动不同，ArrayHandler 不会将数据持久化到磁盘、数据库或外部存储。
这样可以在单元测试或集成测试期间安全地模拟 Session 交互，且不影响真实的 Session 数据。

使用此驱动可完全在内存中设置、检索和断言 Session 数据，使测试更快速、更独立。
虽然生产环境通常使用文件、数据库或缓存驱动，但 ArrayHandler 专为支持测试工作流并防止副作用而设计。

.. contents::
   :local:
   :depth: 2

初始化 Session
=====================

可使用 ArrayHandler 驱动初始化测试用 Session。下例展示了如何通过正确配置创建 Session 实例：

.. literalinclude:: session_testing/001.php

设置与检索数据
===========================

初始化完成后，即可像平时一样设置并检索 Session 值：

.. literalinclude:: session_testing/002.php

.. note::

   Session 数据存储在内存中，生命周期与 ArrayHandler 对象一致。
   对象销毁后（通常在请求或测试结束时），数据将丢失。

测试用例示例
=================

以下是在 PHPUnit 测试中使用 ArrayHandler 的简单示例：

.. literalinclude:: session_testing/003.php

Session 断言
==================

在 ArrayHandler 中使用 PHPUnit 断言
------------------------------------------

在单元测试中直接使用 Session 和 ArrayHandler 测试时，请使用标准的 PHPUnit 断言。
由于此时是直接与 Session 对象（而非响应对象）交互，因此 ``assertSessionHas()`` 和 ``assertSessionMissing()`` 在此上下文中不可用。

.. literalinclude:: session_testing/004.php

通过 TestResponse 进行 Session 断言
-----------------------------------

测试控制器或 HTTP 响应时，可使用 CodeIgniter 4 提供的 Session 断言辅助函数，例如 ``TestResponse`` 对象中的 ``assertSessionHas()`` 和 ``assertSessionMissing()``。
这些辅助函数允许在 HTTP 请求/响应生命周期内对 Session 状态进行断言。
更多详情请参阅：:ref:`Session 断言 <response-session-assertions>`

自定义 Session 值
=====================

在功能测试中，可通过 ``withSession()`` 方法为单个测试提供自定义 Session 数据。
由此可在请求期间模拟登录用户或特定角色等 Session 状态。
完整详情与示例请参阅：:ref:`设置 Session 值 <feature-setting-session-values>`
