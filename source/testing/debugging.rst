**************************
调试你的应用
**************************

.. contents::
    :local:
    :depth: 2

================
取代 var_dump
================

尽管使用在调试你的应用程序时， XDebug 以及一个优秀的 IDE 是不可或缺的，有时候一个简单的 ``var_dump()`` 就是你所需要的。
CodeIgniter 通过集成了优秀的 `Kint <https://kint-php.github.io/kint/>`_ 调试工具来将这一过程更为优化。
该功能比你常用的工具更为方便，可以提供多种类型的可选数据，类似于时间戳格式化，以颜色的方式展示十六进制码，以便于阅读的方式输出数组数据等等等。

启用 Kint
=============

默认情况下，Kint 仅在 **development** and **testing** 环境中启用（开发和测试中）。该操作可以通过环境配置这节中所述的，修改主 **index.php** 文件中的 ``$useKint`` 值来实现::

    $useKint = true;

使用 Kint
==========

**d()**

``d()`` 方法用于输出所有其所接受的所有参数，并将其输出到屏幕上，并允许脚本继续执行::

    d($_SERVER);

**dd()**

与 ``d()`` 等同，除了该方法同时会执行 ``dies()`` ，导致该请求的后续代码无法执行。

**trace()**

该方法会对于当前执行点提供一个调用栈。以 Kint 独有的方式::

    trace();

更多信息请参阅 `Kint 主页 <https://kint-php.github.io/kint//>`_.

=================
调试工具条
=================

调试工具条提供了对于当前页面请求的快照信息，包括性能测试结果，运行的语句，请求和响应数据等。
而这些都在开发实践中证明了其在调试和优化过程中的实用性。

.. note:: 调试工具条仍处于构建中，并遗留着几个日后计划实现的特性功能

启用工具条
====================

工具条在 **除了** 生产环境之外的其他环境中默认启用。该功能会在 CI_DEBUG 这个常量被定义且值为正数时显示。
这一常量在启用文件（例如 ``app/Config/Boot/development.php`` 中）定义，并可被修改并决定该功能用于哪个环境。

工具条本身作为一个 :doc:`后置过滤器 </incoming/filters>` 所展示。你可以通过将其从**app/Config/Filters.php**文件的 ``$globals`` 属性中移除的方式来将其停用。

选择显示内容
---------------------

CodeIgniter 中装载了多个收集器，正如其名所示，用于收集数据并显示于工具条中。
你可以创建自己的收集器来定制化工具条。为了决定哪些收集器显示，我们又回到 **app/Config/Toolbar.php** 这一配置文件::

	public $collectors = [
		\CodeIgniter\Debug\Toolbar\Collectors\Timers::class,
		\CodeIgniter\Debug\Toolbar\Collectors\Database::class,
		\CodeIgniter\Debug\Toolbar\Collectors\Logs::class,
		\CodeIgniter\Debug\Toolbar\Collectors\Views::class,
 		\CodeIgniter\Debug\Toolbar\Collectors\Cache::class,
		\CodeIgniter\Debug\Toolbar\Collectors\Files::class,
		\CodeIgniter\Debug\Toolbar\Collectors\Routes::class,
		\CodeIgniter\Debug\Toolbar\Collectors\Events::class,
	];

将你不期望显示的收集器注释掉。并通过增加完全命名空间化的类名来增加自定义收集器。
这里给定的收集器将影响哪些区块将会显示，以及哪些信息将会在时间线上呈现

.. note:: 某些区块，例如数据库和日志，将会仅在含有内容时展示。否则将会被移除以节省显示空间。

CodeIgniter 装载的控制器为:

* **Timers** 收集性能测试数据，包括系统和应用的
* **Database** 展示所有数据库连接所执行的查询语句与其运行时间
* **Logs** 所有日志信息将会在这里展示。在持久运行的系统或者是有许多日志项目的系统中，该功能可能会导致内存问题并需要被禁用。
* **Views** 以时间线的方式显示视图加载时间，并在独立区块中显示传递给该视图的所有数据。
* **Cache** 将会显示缓存命中和未命中情况以及执行时间
* **Files** 显示在本次请求中加载的所有文件列表
* **Routes** 显示对于当前路由以及系统中定义的所有路由的信息
* **Events** 显示本次请求中所有加载的事件的列表

设置性能测试目标
========================

为了使性能测试器可以收集并展示性能测试数据，你必须使用特定的语法来标记测试点。

请阅读以下信息以设置性能测试基点 :doc:`基准测试类 </testing/benchmark>`

创建自定义收集器
==========================

创建自定义收集器是一件简单直接的事情。你可以创建一个完全命名空间标识的类，并继承 ``CodeIgniter\Debug\Toolbar\Collectors\BaseCollector`` ，从而自动加载器可以将其定位。
该类提供了许多你可以用于重载的方法，并含有四个需要设置的属性，来帮助你决定如何使用收集器::

	<?php namespace MyNamespace;

	use CodeIgniter\Debug\Toolbar\Collectors\BaseCollector;

	class MyCollector extends BaseCollector
	{
		protected $hasTimeline   = false;

		protected $hasTabContent = false;

		protected $hasVarData    = false;

		protected $title         = '';
	}

**$hasTimeline** 对于任何想要在工具条的时间线上显示信息的收集器来说，该属性应该被设置为 ``true`` 。如果该属性为 true 的话，你需要实现 ``formatTimelineData()`` 方法以格式化并返回需要显示的数据。

**$hasTabContent** 对于任何想要拥有自定义标签的收集器来说，该属性应该被设置为 ``true`` 。如果该属性为 true 的话，你需要提供 ``$title`` 值，并实现 ``display()`` 方法以渲染标签页内容。
如果你需要在标签标题右侧显示额外的信息的话，需要实现 ``getTitleDetails()`` 方法。

**$hasVarData** 如果该收集器需要为 ``变量`` 标签页增加额外数据的话，该值应被设为 ``true`` 。如果该值为 true ，你需要实现 ``getVarData()`` 方法。

**$title** 在展开的标签页上显示

显示工具条标签
------------------------

为了显示一个工具条标签，你必须:

1. 将需要同时显示在工具条标题和标签头部的文本赋值给 ``$title`` .
2. 将 ``$hasTabContent`` 属性设置为 ``true``.
3. 实现 ``display()`` 方法.
4. 也可以选择性地实现 ``getTitleDetails()`` 方法.

``display()`` 方法创建了标签内部显示的HTML内容。由于标签的标题会自动交由工具条来处理，因此该方法不会影响它。这一方法会返回一个 HTML 字符串。

``getTitleDetails()`` 方法会返回一个用于显示在标签页标题右侧的字符串，该方法可用于更多额外的概览信息。
例如，在数据库标签页上显示所有连接所执行的查询数，以及在文件标签页上显示打开的文件总个数等。

提供时间线数据
-----------------------

为了提供在时间线上展示的数据，你必须:

1. 将 ``$hasTimeline`` 变量设为 ``true``.
2. 实现 ``formatTimelineData()`` 方法.

``formatTimelineData()`` 方法必须返回一个以时间线可用的格式的数组，其中以正确的方式排序并返回正确的信息。内层数据必须包含以下信息::

	$data[] = [
		'name'      => '',     // 在时间线左侧显示的名字
		'component' => '',     // 在时间线中间列出的部件名
		'start'     => 0.00,   // 开始时间，例如 microtime(true)
		'duration'  => 0.00    // 持续时间，例如 mircrotime(true) - microtime(true)
	];

提供变量
--------------

为了将数据加入到变量标签页中，你必须:

1. 将 ``$hasVarData`` 变量设为 ``true``
2. 实现 ``getVarData()`` 方法。

``getVarData()`` 方法应当返回一个需要显示的以键值对格式的数组
外层数组的键为变量标签页的标签名::

	$data = [
		'section 1' => [
		    'foo' => 'bar',
		    'bar' => 'baz'
		],
		'section 2' => [
		    'foo' => 'bar',
		    'bar' => 'baz'
		]
	 ];
