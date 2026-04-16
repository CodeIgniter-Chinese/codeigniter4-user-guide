##########################
调试应用
##########################

.. contents::
    :local:
    :depth: 2

*************
查看日志
*************

.. _codeigniter-error-logs:

CodeIgniter 错误日志
======================

CodeIgniter 会根据 **app/Config/Logger.php** 的配置记录错误日志。

默认情况下，日志文件按天存储在 **writable/logs** 目录中。
如果程序运行不符合预期，建议查阅这些日志文件。

此外，还可以通过调整错误阈值来控制日志信息的详略程度。详见
:ref:`日志记录 <logging-configuration>`。

记录所有 SQL 查询
=======================

CodeIgniter 执行的所有 SQL 查询均可被记录。详见 :ref:`数据库事件 <database-events-dbquery>`。

********************
替代 var_dump()
********************

虽然 Xdebug 和优秀的 IDE 是调试应用不可或缺的利器，
但有时只需简单的 ``var_dump()`` 就能解决问题。
CodeIgniter 内置了优秀的 PHP 调试工具 `Kint <https://kint-php.github.io/kint/>`_，使调试体验更上一层楼。

Kint 的功能远超常规工具，能提供更丰富的辅助信息。
例如：将时间戳转换为易读的日期、将十六进制色值直接显示为颜色、
以表格形式展示数组数据以便阅读等，功能远不止于此。

启用 Kint
=============

默认情况下，Kint 仅在 **development** 和 **testing** :doc:`环境 </general/environments>` 中启用。只要常量 ``CI_DEBUG`` 已定义且值为真，Kint 就会启用。该常量在启动文件（如 **app/Config/Boot/development.php**）中定义。

使用 Kint
==========

d()
---

``d()`` 方法将传入参数的所有数据输出到屏幕，脚本继续执行：

.. literalinclude:: debugging/001.php
    :lines: 2-

dd()
----

此方法与 ``d()`` 功能完全一致，但会同时调用 ``die()``，随后将停止执行当前请求的后续代码。

trace()
-------

此方法提供当前执行点的回溯跟踪，带有 Kint 独有的展示风格：

.. literalinclude:: debugging/002.php
    :lines: 2-

更多信息，请参阅 `Kint 官网 <https://kint-php.github.io/kint//>`_。

.. _the-debug-toolbar:

*****************
调试工具栏
*****************

调试工具栏提供当前页面请求的概览信息，包括基准测试结果、已执行的查询、请求和响应数据等。这些在开发过程中非常有用，可帮助调试和优化应用。

.. note:: 调试工具栏仍在开发中，部分计划功能尚未实现。

启用工具栏
====================

默认情况下，除 **production** 外的所有 :doc:`环境 </general/environments>` 都会启用工具栏。只要常量 ``CI_DEBUG`` 已定义且值为 true，工具栏就会显示。该常量在启动文件（如 **app/Config/Boot/development.php**）中定义，可以在此修改以控制哪些环境显示工具栏。

.. note:: 当 ``baseURL`` 设置（位于 **app/Config/App.php** 或 **.env** 中的 ``app.baseURL``）与实际 URL 不匹配时，不会显示调试工具栏。

工具栏本身通过 :doc:`后置过滤器 </incoming/filters>` 实现。如需彻底禁用，可在 **app/Config/Filters.php** 中从 ``$required`` （或 ``$globals``）属性中移除 ``'toolbar'``。

.. note:: v4.5.0 之前的版本中，工具栏默认设置在 ``$globals`` 中。

选择显示内容
---------------------

CodeIgniter 内置了多个收集器。顾名思义，其作用是收集数据并展示在工具栏上。开发者也可轻松创建自定义收集器来定制工具栏。若要决定显示哪些收集器，请查看 **app/Config/Toolbar.php** 配置文件：

.. literalinclude:: debugging/003.php

只需注释掉无需显示的收集器即可。若要添加自定义收集器，在此处提供完全限定类名即可。此处的配置将直接影响显示的选项卡以及时间轴呈现的信息。

.. note:: 某些选项卡（如 Database 和 Logs）仅在有内容时显示。否则将自动隐藏，以确保在小屏幕上也能正常显示。

CodeIgniter 内置的收集器包括：

* **Timers**：收集系统和应用的所有基准测试数据。
* **Database**：显示所有数据库连接执行的查询列表及其执行时间。
* **Logs**：显示所有已记录的日志信息。在长时间运行或日志量巨大的系统中，此项可能会导致内存问题，建议禁用。
* **Views**：在时间轴上显示视图渲染时间，并在独立选项卡中展示传递给视图的数据。
* **Cache**：显示缓存命中、未命中情况以及执行时间。
* **Files**：列出当前请求加载的所有文件。
* **Routes**：显示当前路由信息以及系统中定义的所有路由。
* **Events**：列出当前请求触发的所有事件。

设置基准测试标记点
========================

如需让分析器编译并显示基准测试数据，必须使用特定语法来命名标记点。

请阅读 :doc:`基准测试 </testing/benchmark>` 页面中关于设置基准测试标记点的信息。

创建自定义收集器
==========================

创建自定义收集器非常简单。只需编写一个继承自 ``CodeIgniter\Debug\Toolbar\Collectors\BaseCollector`` 的新类，并使用完整的命名空间以便自动加载器识别。基类提供了一系列可重写的方法，同时包含 4 个必需的类属性，开发者需根据收集器的具体需求对其进行正确设置：

.. literalinclude:: debugging/004.php

**$hasTimeline** 设为 ``true`` 时，收集器可在工具栏的时间轴中显示信息。启用此选项后，需要实现 ``formatTimelineData()`` 方法来格式化并返回待展示的数据。

**$hasTabContent** 设为 ``true`` 时，收集器可显示自己的自定义内容选项卡。启用此选项后，需要提供 ``$title``、实现 ``display()`` 方法来渲染选项卡内容，如果要在选项卡标题右侧显示额外信息，还需要实现 ``getTitleDetails()`` 方法。

**$hasVarData** 设为 ``true`` 时，收集器可向 ``Vars`` 选项卡添加额外数据。启用此选项后，需要实现 ``getVarData()`` 方法。

**$title** 显示在打开的选项卡上。

显示工具栏选项卡
------------------------

要显示工具栏选项卡，必须：

1. 为 ``$title`` 赋值，该文本将同时作为工具栏和选项卡的标题。
2. 将 ``$hasTabContent`` 设为 ``true``。
3. 实现 ``display()`` 方法。
4. 可根据需要实现 ``getTitleDetails()`` 方法。

``display()`` 方法用于生成选项卡中显示的 HTML 内容。由于工具栏会自动处理标题，该方法只需返回 HTML 字符串即可。

``getTitleDetails()`` 方法返回的字符串将直接显示在选项卡标题右侧，常用于提供额外的概览信息。例如，Database 选项卡会显示所有连接的查询总数，而 Files 选项卡则显示加载的文件总数。

提供时间轴数据
-----------------------

要在时间轴上显示信息，必须：

1. 将 ``$hasTimeline`` 设为 ``true``。
2. 实现 ``formatTimelineData()`` 方法。

``formatTimelineData()`` 方法必须返回一个数组，内部数组的格式需符合时间轴的排序和展示要求。内部数组须包含以下信息：

.. literalinclude:: debugging/005.php

提供变量数据
--------------

要向 Vars 选项卡添加数据，必须：

1. 将 ``$hasVarData`` 设为 ``true``。
2. 实现 ``getVarData()`` 方法。

``getVarData()`` 方法应返回一个包含关联数组的数组。外层数组的键名即为 Vars 选项卡上的区块名称：

.. literalinclude:: debugging/006.php

.. _debug-toolbar-hot-reload:

热重载
=============

.. versionadded:: 4.4.0

调试工具栏包含一项名为“热重载”的功能。修改应用代码后，浏览器会自动重载页面，无需手动刷新。此功能可显著节省开发时间。

开发时，点击工具栏左侧类似于刷新图标的按钮即可启用热重载。启用后，所有页面都将保持热重载状态，直至手动关闭。

热重载的工作原理是每秒扫描一次 **app** 目录下的文件。一旦检测到更改，便会通知浏览器重新加载页面。由于该功能不会扫描其他目录，因此修改 **app** 以外的文件时，仍需手动刷新页面。

若需监视 **app** 以外的目录，或因项目庞大导致扫描速度下降，可在 **app/Config/Toolbar.php** 配置文件中，通过修改 ``$watchedDirectories`` 和 ``$watchedExtensions`` 属性来指定要扫描的目录及文件扩展名。
