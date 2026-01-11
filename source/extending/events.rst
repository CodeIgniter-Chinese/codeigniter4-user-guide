事件
#####################################

CodeIgniter 的事件（Events）功能提供了一种在不修改核心文件的情况下，介入并修改框架内部工作流程的方法。当 CodeIgniter 运行时，它遵循一个特定的执行流程。然而，你可能希望在执行流程的特定阶段执行某些操作。例如，你可能希望在控制器加载前或加载后立即运行一个脚本，或者希望在其他某个位置触发你自己的脚本。

事件基于 *发布/订阅* 模式工作，即在脚本执行过程中的某个时刻触发一个事件。其他脚本可以通过向 Events 类注册来“订阅”该事件，从而告知系统，当该事件被触发时，它们希望执行某个操作。

.. contents::
    :local:
    :depth: 2

启用事件
===============

事件始终处于启用状态，并且全局可用。

定义事件
=================

大多数事件在 **app/Config/Events.php** 文件中定义。你可以使用 ``Events`` 类的 ``on()`` 方法，将一个操作订阅到一个事件。第一个参数是要订阅的事件名称，第二个参数是当该事件被触发时将要运行的可调用对象（callable）：

.. literalinclude:: events/001.php

在这个例子中，每当 ``pre_system`` 事件被执行时，就会创建 ``MyClass`` 的实例并运行 ``myFunction()`` 方法。注意第二个参数可以是 PHP 识别的*任何*形式的`可调用对象 <https://www.php.net/manual/zh/function.is-callable.php>`_：

.. literalinclude:: events/002.php

设置优先级
------------------

由于多个方法可以订阅同一个事件，你需要一种方式来定义这些方法的调用顺序。你可以通过将优先级数值作为 ``on()`` 方法的第三个参数来实现。数值越小，优先级越高，执行越早，其中值为 1 的优先级最高，而较低的数值则没有限制：

.. literalinclude:: events/003.php

具有相同优先级的订阅者将按照它们被定义的顺序执行。

自 v4.2.0 版本起，定义了三个类常量供你使用，它们为这些数值设置了一些有用的范围。虽然你不是必须使用这些常量，但你可能会发现它们有助于提高代码的可读性：

.. literalinclude:: events/004.php

.. important:: ``EVENT_PRIORITY_LOW``、``EVENT_PRIORITY_NORMAL`` 和 ``EVENT_PRIORITY_HIGH`` 这三个常量已在 v4.6.0 版本中移除。

排序后，所有订阅者将按顺序执行。如果任何一个订阅者返回了布尔值 false，则订阅者的执行将会停止。

发布自定义事件
==========================

Events 库也使得在你自己的代码中创建事件变得非常简单。要使用此功能，你只需在 **Events** 类上调用 ``trigger()`` 方法，并传入事件的名称即可：

.. literalinclude:: events/005.php

你可以通过添加额外的参数，向订阅者传递任意数量的参数。订阅者将按照定义的顺序接收这些参数：

.. literalinclude:: events/006.php

模拟事件
=================

在测试过程中，你可能不希望事件实际触发，因为每天发送数百封电子邮件既耗时又适得其反。你可以通过 ``simulate()`` 方法告诉 Events 类仅模拟事件的运行。当参数为 **true** 时，所有事件都将在触发方法中被跳过。不过，其他所有功能仍会正常工作。

.. literalinclude:: events/007.php

你可以通过传递 false 来停止模拟：

.. literalinclude:: events/008.php

.. _event-points:

事件点
============

Web 应用
------------

以下是通过 **public/index.php** 调用的 Web 应用程序可用的事件点列表：

* **pre_system** 在系统执行早期调用。此时 URI、Request 和 Response 已被实例化，但页面缓存检查、路由以及“before”控制器过滤器的执行尚未发生。
* **post_controller_constructor** 在你的控制器实例化后立即调用，但在任何方法调用发生之前。
* **post_system** 在最终渲染的页面被发送到浏览器之前调用，位于系统执行的末尾，在“after”控制器过滤器执行之后。

.. _event-points-for-cli-apps:

CLI 应用
------------

以下是 :doc:`../cli/spark_commands` 可用的事件点列表：

* **pre_command** 在命令代码执行之前立即调用。
* **post_command** 在命令代码执行之后立即调用。

其他
------

以下是各个库可用的事件点列表：

* **email** 从 ``CodeIgniter\Email\Email`` 成功发送电子邮件后调用。接收一个包含 ``Email`` 类属性的数组作为参数。
* **DBQuery** 在数据库查询之后（无论成功与否）调用。接收 ``Query`` 对象。
* **migrate** 在成功调用 ``latest()`` 或 ``regress()`` 进行迁移后调用。接收 ``MigrationRunner`` 的当前属性以及方法的名称。
