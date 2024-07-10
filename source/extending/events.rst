事件
#####################################

CodeIgniter 的事件功能提供了一种方式，可以在不修改核心文件的情况下，接入并修改框架的内部工作流程。当 CodeIgniter 运行时，它会遵循一个特定的执行过程。但是，在某些情况下，你可能会希望在某些特定的执行阶段执行某些操作。例如，你可能想在控制器加载之前或之后运行一个脚本，或者你可能想在其他位置触发自己的脚本。

事件基于 *发布/订阅* 模式工作，在脚本执行期间的某个点触发一个事件。其他脚本可以通过注册到事件类来“订阅”该事件，让事件类知道它们希望在触发该事件时执行一个动作。

.. contents::
    :local:
    :depth: 2

启用事件
===============

事件总是启用的,并全局可用。

定义事件
=================

大多数事件在 **app/Config/Events.php** 文件中定义。你可以使用 ``Events`` 类的 ``on()`` 方法为一个事件订阅一个操作。第一个参数是要订阅的事件名称。第二个参数是一个回调,在触发该事件时会运行它:

.. literalinclude:: events/001.php

在这个例子中,每当执行 ``pre_system`` 事件时,会创建 ``MyClass`` 的一个实例并运行 ``myFunction()`` 方法。注意,第二个参数可以是 PHP 支持的任何形式的 `可调用项 <https://www.php.net/manual/en/function.is-callable.php>`_:

.. literalinclude:: events/002.php

设置优先级
------------------

由于可以为单个事件订阅多个方法,因此你需要一种定义这些方法调用顺序的方式。你可以通过在 ``on()`` 方法的第三个参数传递一个优先级值来实现这一点。较低的值会先执行,值 1 具有最高优先级,对较低值没有限制:

.. literalinclude:: events/003.php

具有相同优先级的任何订阅者都会按定义的顺序执行。

从 v4.2.0 开始,定义了三个类常量供你使用,它们为值设置了一些有用的范围。你不需要使用它们,但你可能会发现它们有助于提高可读性:

.. literalinclude:: events/004.php

.. important:: 常量 ``EVENT_PRIORITY_LOW``、``EVENT_PRIORITY_NORMAL`` 和 ``EVENT_PRIORITY_HIGH`` 已弃用,定义移至 ``app/Config/Constants.php``。这些将在未来版本中删除。

对订阅者排序后,会按顺序执行所有订阅者。如果任何订阅者返回布尔假值,则将停止执行订阅者。

发布你自己的事件
==========================

Events 库也使你可以在自己的代码中简单地创建事件。要使用此功能,你只需要用事件名称调用 **Events** 类的 ``trigger()`` 方法:

.. literalinclude:: events/005.php

通过添加更多参数,你可以向订阅者传递任意数量的参数。订阅者将以定义的相同顺序获取参数:

.. literalinclude:: events/006.php

模拟事件
=================

在测试期间,你可能不希望事件实际触发,因为每天发送数百封电子邮件既缓慢又适得其反。你可以使用 ``simulate()`` 方法告诉 Events 类仅模拟运行事件。当值为 **true** 时,在 trigger 方法期间将跳过所有事件。但是其他一切都将正常工作。

.. literalinclude:: events/007.php

你可以通过传递 false 来停止模拟:

.. literalinclude:: events/008.php

.. _event-points:

事件挂钩点
============

用于 Web 应用
-------------

以下是由 **public/index.php** 触发的可用事件挂钩点列表:

* **pre_system** 在系统执行早期调用。URI、Request 和 Response 已经实例化，但页面缓存检查、路由和“before”控制器过滤器的执行尚未发生。
* **post_controller_constructor** 在控制器实例化后立即调用，但在任何方法调用发生之前。
* **post_system** 在系统执行结束时、在执行“after”控制器过滤器之后、最终渲染的页面发送到浏览器之前调用。

.. _event-points-for-cli-apps:

用于 CLI 应用
-------------

以下是 :doc:`../cli/spark_commands` 触发的可用事件点列表:

* **pre_command** 在命令代码执行之前调用。
* **post_command** 在命令代码执行之后调用。

其他
------

以下是每个库可用的事件点列表:

* **email** 在 ``CodeIgniter\Email\Email`` 成功发送电子邮件之后调用。接收一个包含 ``Email`` 类属性的数组作为参数。
* **DBQuery** 在数据库查询成功或失败后调用。接收 ``Query`` 对象。
* **migrate** 在成功调用 ``latest()`` 或 ``regress()`` 进行迁移后调用。接收当前 ``MigrationRunner`` 属性以及方法名称。
