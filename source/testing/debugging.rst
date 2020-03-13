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

In order for the Profiler to compile and display your benchmark data you must name your mark points using specific syntax.

Please read the information on setting Benchmark points in the :doc:`Benchmark Library </testing/benchmark>` page.

创建自定义收集器
==========================

Creating custom collectors is a straightforward task. You create a new class, fully-namespaced so that the autoloader
can locate it, that extends ``CodeIgniter\Debug\Toolbar\Collectors\BaseCollector``. This provides a number of methods
that you can override, and has four required class properties that you must correctly set depending on how you want
the Collector to work
::

	<?php namespace MyNamespace;

	use CodeIgniter\Debug\Toolbar\Collectors\BaseCollector;

	class MyCollector extends BaseCollector
	{
		protected $hasTimeline   = false;

		protected $hasTabContent = false;

		protected $hasVarData    = false;

		protected $title         = '';
	}

**$hasTimeline** should be set to ``true`` for any Collector that wants to display information in the toolbar's
timeline. If this is true, you will need to implement the ``formatTimelineData()`` method to format and return the
data for display.

**$hasTabContent** should be ``true`` if the Collector wants to display its own tab with custom content. If this
is true, you will need to provide a ``$title``, implement the ``display()`` method to render out tab's contents,
and might need to implement the ``getTitleDetails()`` method if you want to display additional information just
to the right of the tab content's title.

**$hasVarData** should be ``true`` if this Collector wants to add additional data to the ``Vars`` tab. If this
is true, you will need to implement the ``getVarData()`` method.

**$title** is displayed on open tabs.

显示工具条标签
------------------------

为了显示一个工具条标签，你必须:

1. Fill in ``$title`` with the text displayed as both the toolbar title and the tab header.
2. Set ``$hasTabContent`` to ``true``.
3. Implement the ``display()`` method.
4. Optionally, implement the ``getTitleDetails()`` method.

The ``display()`` creates the HTML that is displayed within the tab itself. It does not need to worry about
the title of the tab, as that is automatically handled by the toolbar. It should return a string of HTML.

The ``getTitleDetails()`` method should return a string that is displayed just to the right of the tab's title.
it can be used to provide additional overview information. For example, the Database tab displays the total
number of queries across all connections, while the Files tab displays the total number of files.

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
