############
基准测试类
############

CodeIgniter 提供了两个独立的工具来帮助你对代码进行基准测试，并测试不同的选项：Timer 和 Iterator。Timer 允许你轻松计算脚本执行中两点之间的时间。迭代器允许你设置多个变量并运行这些测试，记录性能和内存统计信息，以帮助你确定哪个版本是最佳的。

Timer类始终处于活动状态，从框架被调用的那一刻开始，直到发送输出到用户之前，才能使整个系统执行的时间非常准确。

.. contents::
    :local:
    :depth: 2

===============
使用定时器
===============

使用Timer，你可以测量执行应用程序的两个时刻之间的时间。这样可以轻松测量应用程序的不同方面的性能。所有测量都是使用 ``start()`` 和 ``stop()`` 方法完成的。

该 ``start()`` 方法采用单个参数：此定时器的名称。你可以使用任何字符串作为计时器的名称。它仅用于你以后参考以了解哪个测量是::

	$benchmark = \Config\Services::timer();
	$benchmark->start('render view');

该 ``stop()`` 方法将要停止的计时器的名称作为唯一的参数，也是::
	$benchmark->stop('render view');

该名称不区分大小写，但除此之外必须与你在启动计时器时给出的名称相匹配。

或者，你可以使用 :doc:`全局函数 </general/common_functions>` ``timer()`` 来启动和停止定时器::

	// Start the timer
	timer('render view');
	// Stop a running timer,
	// if one of this name has been started
	timer('render view');

查看你的基准点
=============================

当你的应用程序运行时，你设置的所有定时器都将由Timer类收集。它不会自动显示它们。你可以通过调用 ``getTimers()`` 方法检索所有的计时器。该方法返回一组基准信息，包括开始，结束和持续时间::

	$timers = $benchmark->getTimers();

	// Timers =
	array(
		'render view' => array(
			'start' => 1234567890,
			'end' => 1345678920,
			'duration' => 15.4315      // number of seconds
		)
	)

你可以通过传递要显示的小数位数作为唯一参数来更改计算持续时间的精度。默认值为小数点后面的 4 个数字::

	$timers = $benchmark->getTimers(6);

计时器会自动显示在 :doc:`Debub 工具栏中</general/debugging>`。

显示执行时间
=========================

该 ``getTimers()`` 方法将为你的项目中的所有计时器提供原始数据，你可以使用 `getElapsedTime()` 方法检索单个计时器的持续时间（以秒为单位）。第一个参数是要显示的定时器的名称。第二个是要显示的小数位数。默认为4::

	echo timer()->getElapsedTime('render view');
	// Displays: 0.0234

==================
使用迭代器
==================

Iterator是一个简单的工具，旨在让你尝试解决方案中的多个变体，以查看速度差异和不同内存使用模式。你可以添加任何数量的 “任务”，以便运行，该类将运行任务数百或数千次以获得更清晰的性能。然后，你的脚本可以检索和使用结果，或显示为HTML表格。

创建任务运行
=====================

任务在 Closures 内定义。任务创建的任何输出将被自动丢弃。它们通过 `add()` 方法添加到 Iterator 类中。第一个参数是您想要引用这个测试的名称;第二个参数是 Closure，它自己本身::

	$iterator = new \CodeIgniter\Benchmark\Iterator();

	// Add a new task
	$iterator->add('single_concat', function()
		{
			$str = 'Some basic'.'little'.'string concatenation test.';
		}
	);

	// Add another task
	$iterator->add('double', function($a='little')
		{
			$str = "Some basic {$little} string test.";
		}
	);


运行任务
=================

你一旦添加了要运行的任务，你可以使用 ``run()`` 方法多次循环任务。默认情况下，它将循环运行 1000 次。这对大多数简单的测试来说可能就足够了，如果你需要运行测试多次，你可以将你希望运行数字作为第一个参数传递值::

	// Run the tests 3000 times.
	$iterator->run(3000);

一旦运行，它将返回带有测试结果的 HTML 表格。如果你不希望显示结果，可以通过传递第二个参数为 false::

	// Don't display the results.
	$iterator->run(1000, false);
