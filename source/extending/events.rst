事件
#####################################

CodeIgniter 的事件功能提供了一种无需修改核心文件即可介入和修改框架内部工作机制的方式。当 CodeIgniter 运行时，它遵循特定的执行流程。然而，有时你可能希望在执行流程的特定阶段触发某些操作。例如，你可能想在控制器加载之前或之后立即运行一个脚本，或者在某个其他位置触发你自己的脚本。

事件基于*发布/订阅*模式工作，在脚本执行期间的某个时刻触发一个事件。其他脚本可以通过向 Events 类注册来"订阅"该事件，以告知框架当该事件触发时它们希望执行某个操作。

.. contents::
    :local:
    :depth: 2

启用事件
===============

事件始终处于启用状态，并且全局可用。

定义事件
=================

大多数事件定义在 **app/Config/Events.php** 文件中。你可以使用 ``Events`` 类的 ``on()`` 方法为事件订阅一个操作。第一个参数是要订阅的事件名称，第二个参数是当事件触发时要运行的可调用对象：

.. literalinclude:: events/001.php

在这个例子中，每当 ``pre_system`` 事件被执行时，就会创建 ``MyClass`` 的实例并运行 ``myFunction()`` 方法。注意第二个参数可以是 PHP 识别的*任何*形式的`可调用对象 <https://www.php.net/manual/en/function.is-callable.php>`_：

.. literalinclude:: events/002.php

设置优先级
------------------

由于多个方法可以订阅同一个事件，你需要一种方式来定义这些方法的调用顺序。你可以通过向 ``on()`` 方法的第三个参数传递优先级值来实现。数值越小优先级越高执行越早，1 为最高优先级，没有最低值限制：

.. literalinclude:: events/003.php

具有相同优先级的订阅者将按照它们被定义的顺序执行。

自 v4.2.0 起，定义了三个类常量供你使用，这些常量设置了有用的数值范围。虽然不强制使用，但它们有助于提高可读性：

.. literalinclude:: events/004.php

.. important:: 常量 ``EVENT_PRIORITY_LOW``、``EVENT_PRIORITY_NORMAL`` 和 ``EVENT_PRIORITY_HIGH`` 已在 v4.6.0 中移除。

排序完成后，所有订阅者将按顺序执行。如果任何订阅者返回布尔值 false，则订阅者的执行将停止。

发布自定义事件
==========================

Events 类库也让你可以轻松在自己的代码中创建事件。要使用此功能，只需在 **Events** 类上调用 ``trigger()`` 方法并指定事件名称：

.. literalinclude:: events/005.php

你可以通过添加额外参数将任意数量的参数传递给订阅者。订阅者将按照定义顺序接收这些参数：

.. literalinclude:: events/006.php

模拟事件
=================

在测试期间，你可能不希望实际触发事件，因为每天发送数百封邮件既缓慢又适得其反。你可以使用 ``simulate()`` 方法让 Events 类仅模拟运行事件。当设置为 **true** 时，所有事件都将在触发方法中被跳过，其他操作仍会正常进行。

.. literalinclude:: events/007.php

你可以通过传递 false 来停止模拟：

.. literalinclude:: events/008.php

.. _event-points:

事件点
============

Web 应用
------------

以下是 Web 应用程序中由 **public/index.php** 调用的可用事件点列表：

* **pre_system** 在系统执行的早期被调用。此时 URI、Request 和 Response 已实例化，但尚未进行页面缓存检查、路由和"before"控制器过滤器的执行。
* **post_controller_constructor** 在控制器实例化后立即调用，但在任何方法调用之前。
* **post_system** 在最终渲染页面发送到浏览器之前调用，在系统执行结束时，在"after"控制器过滤器执行之后。

.. _event-points-for-cli-apps:

CLI 应用
------------

以下是针对 :doc:`../cli/spark_commands` 的可用事件点列表：

* **pre_command** 在命令代码执行之前立即调用。
* **post_command** 在命令代码执行之后立即调用。

其他
------

以下是各库可用的通用事件点列表：

* **email** 当 ``CodeIgniter\Email\Email`` 成功发送邮件后调用。接收 ``Email`` 类的属性数组作为参数。
* **DBQuery** 在数据库查询（无论成功与否）之后调用。接收 ``Query`` 对象。
* **migrate** 在成功调用 ``latest()`` 或 ``regress()`` 迁移方法后调用。接收 ``MigrationRunner`` 的当前属性以及方法名称。
