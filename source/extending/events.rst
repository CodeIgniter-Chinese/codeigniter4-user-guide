事件
#####################################

CodeIgniter 事件特性提供了一种方法来修改框架的内部运作流程或功能，而无需修改核心文件的能力。CodeIgniter 遵循着一个特定的流程来
运行。但是，在某些情况下，你可能想在执行特定流程时执行某些特定的操作。例如在加载控制器之前或之后立即运行一个特定的脚本。或者在其他的
某些位置触发你的脚本。

事件已发布/订阅模式工作，可以在脚本执行过程中的某个时刻触发事件。其他脚本可以通过向 Events 类来注册订阅事件，使它知道在脚本触发事件
时该执行什么操作。

启用事件
===============

事件始终处于启用状态，并且全局可用。

定义事件
=================

大多数的事件都定义在 **app/Config/Events.php** 文件中。不过你也可以通过 Events 类的 ``on()`` 方法定义事件。第一个参数是事件
名称，第二个参数是当触发该事件时执行的操作::

	use CodeIgniter\Events\Events;

	Events::on('pre_system', ['MyClass', 'MyFunction']);

在这个例子中，任何时候触发 **pre_controller** 事件，都会创建 ``MyClass`` 实例并运行 ``MyFunction`` 方法。

第二个参数可以是 PHP 能识别的任何 `可调用结构 <https://www.php.net/manual/en/function.is-callable.php>`_::

	// 调用 some_function 方法
	Events::on('pre_system', 'some_function');

	// 调用实例方法
	$user = new User();
	Events::on('pre_system', [$user, 'some_method']);

	// 调用静态方法
	Events::on('pre_system', 'SomeClass::someMethod');

	// 使用闭包形式
	Events::on('pre_system', function(...$params)
	{
		. . .
	});



设置执行优先顺序
------------------

由于可以将多个方法订阅到一个事件中，因此需要一种方式来定义这些方法的调用顺序。你可以通过传递优先级作为 ``on()`` 方法的第三个参数来实现。
事件系统将优先执行优先级较低的值，优先级最高的值为 1::

    Events::on('post_controller_constructor', 'some_function', 25);

如果出现相同优先级的情况，那么事件系统将按定义的顺序执行。

.. note:: 可以理解为事件系统会根据事件名称分组排序，按第三个参数升序排列，然后依次执行。

Codeigniter 内置了三个常量供您使用，仅供参考。你也可以不使用它，但你会发现他们有助于提高可读性::

	define('EVENT_PRIORITY_LOW', 200);
	define('EVENT_PRIORITY_NORMAL', 100);
	define('EVENT_PRIORITY_HIGH', 10);

排序后，将按顺序执行所有订阅者。如果任意订阅者返回了布尔类型 ``false``，订阅者将停止执行。

发布自定义的事件
==========================

使用事件系统，你可以轻松创建自己的事件。要使用此功能，只需要调用 **Events** 类的 ``trigger()`` 方法即可::

	\CodeIgniter\Events\Events::trigger('some_event');

当然，你也可以为订阅者传递任意数量的参数，订阅者将会按相同的顺序接收参数::

	\CodeIgniter\Events\Events::trigger('some_events', $foo, $bar, $baz);

	Events::on('some_event', function($foo, $bar, $baz) {
		...
	});

模拟事件
=================

在测试期间，你可能不希望事件被真正的触发，因为每天发送数百封电子邮件记缓慢又适得其反。你可以告诉 Events 类使用 ``simulate()`` 方法
模拟运行事件。如果为 **true**，那么将跳过所有事件，不过其他的内容都会正常运行::

    Events::simulate(true);

你也可以传递 **false** 停止模拟::

    Events::simulate(false);

事件触发点
============

以下是 Codeigniter 核心代码中可用的事件触发点列表:

* **pre_system** 系统执行过程中最早被调用。此时，只有 基准测试类 和 钩子类 被加载了， 还没有执行到路由或其他的流程。
* **post_controller_constructor** 在你的控制器实例化之后立即执行，控制器的任何方法都还未调用。
* **post_system** 最终数据发送到浏览器之后，系统执行结束时调用。
