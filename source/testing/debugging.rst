**************************
调试应用程序
**************************

.. contents::
    :local:
    :depth: 2

================
替换 var_dump
================

虽然使用 XDebug 和良好的 IDE 可以帮助调试应用程序,但有时一个快速的 ``var_dump()`` 就能搞定。CodeIgniter 通过内置优秀的 `Kint <https://kint-php.github.io/kint/>`_ PHP 调试工具使调试更便利。Kint 比常规工具提供了更多功能,如将时间戳格式化为可识别日期,将十六进制代码显示为颜色,以表格形式展示数组数据方便阅读等等。

启用 Kint
=============

默认情况下,Kint 仅在 **development** 和 **testing** :doc:`环境 </general/environments>` 中启用。当常量 ``CI_DEBUG`` 定义且值为 true 时就会启用它。常量定义在引导文件中(例如 **app/Config/Boot/development.php**)。

使用 Kint
==========

d()
---

``d()`` 方法将传入的唯一参数的数据全部输出到屏幕,允许脚本继续执行:

.. literalinclude:: debugging/001.php

dd()
----

这个方法与 ``d()`` 一样,但会在输出数据后 ``die()``,请求不再执行后续代码。

trace()
-------

这会以 Kint 独特的方式提供当前执行点的回溯:

.. literalinclude:: debugging/002.php

更多信息请参考 `Kint 文档 <https://kint-php.github.io/kint//>`_。

.. _the-debug-toolbar:

=================
调试工具栏
=================

调试工具栏可以一目了然地查看当前页面请求的信息,包括基准测试结果、执行的查询、请求和响应数据等。这在开发过程中有助于调试和优化。

.. note:: 调试工具栏仍在开发中,许多计划的功能尚未实现。

启用工具栏
====================

除 **production** 环境外,调试工具栏在其他所有 :doc:`环境 </general/environments>` 下默认启用。当常量 ``CI_DEBUG`` 定义且值为 true 时就会显示。常量定义在引导文件中(例如 **app/Config/Boot/development.php**),可以在其中修改以确定显示的环境。

.. note:: 当你的 ``baseURL`` 设置(在 **app/Config/App.php** 或 ``app.baseURL`` 在 **.env** 中)与实际 URL 不匹配时,不会显示调试工具栏。

工具栏本身作为 :doc:`After 过滤器 </incoming/filters>` 显示。可以通过在 **app/Config/Filters.php** 的 ``$globals`` 属性中删除它来完全禁用。

选择显示内容
---------------------

CodeIgniter 默认带有多个 Collector ,它们收集要在工具栏上显示的数据。你可以方便地自定义 Collector 。要确定显示哪些收集器,请查看配置文件 **app/Config/Toolbar.php**:

.. literalinclude:: debugging/003.php

注释掉不想显示的收集器。通过提供完全限定类名,这里可以添加自定义收集器。出现的收集器将决定显示的选项卡和时间线上的信息。

.. note:: 比如数据库和日志,只有存在内容的选项卡才会显示。否则它们会在小屏幕上删除。

CodeIgniter 带有以下收集器:

* **Timers** 收集系统和应用程序的所有基准数据。
* **Database** 显示所有数据库连接执行的查询与耗时。
* **Logs** 显示记录的任何信息。长时间运行的系统中可能导致内存问题,应禁用它。
* **Views** 在时间线显示视图渲染时间,在单独选项卡显示传递给视图的数据。
* **Cache** 显示缓存命中、未命中信息和执行时间。
* **Files** 显示请求期间加载的所有文件的列表。
* **Routes** 显示当前和所有定义的路由信息。
* **Events** 显示请求期间加载的所有事件列表。

设置基准点
========================

为展示定界器的基准数据,必须使用特定语法命名标记点。

请参考 :doc:`基准测试库 </testing/benchmark>` 文档中的说明。

创建自定义收集器
==========================

创建自定义收集器很简单。创建一个新的类,使用命名空间完全限定以便自动加载,它需要扩展 ``CodeIgniter\Debug\Toolbar\Collectors\BaseCollector``。BaseCollector 提供可重写的方法,并要求正确设置四个必需类属性以确定收集器的行为:

.. literalinclude:: debugging/004.php

如果任何收集器要在时间线显示信息,应将 ``$hasTimeline`` 设为 ``true``。如果为 true,需要实现 ``formatTimelineData()`` 方法来格式化返回显示的数据。

如果收集器要显示自定义选项卡和内容,应将 ``$hasTabContent`` 设为 ``true``。如果为 true,需要提供 ``$title``、实现 ``display()`` 渲染选项卡内容,如果要在标题右侧显示额外信息,还可能需要实现 ``getTitleDetails()``。

如果要向 ``Vars`` 选项卡添加数据,应将 ``$hasVarData`` 设为 ``true``,并实现 ``getVarData()``。

``$title`` 显示在打开的选项卡上。

显示工具栏选项卡
------------------------

显示工具栏选项卡需要:

1. 在 ``$title`` 填入显示为工具栏和选项卡标题的文本。
2. 将 ``$hasTabContent`` 设为 ``true``。
3. 实现 ``display()`` 方法渲染内容。
4. 可选地,实现 ``getTitleDetails()``。

``display()`` 返回显示在选项卡中的 HTML,不需要处理标题,由工具栏自动处理。它应返回 HTML 字符串。

``getTitleDetails()`` 返回在标题右侧显示的字符串,可提供概述信息。比如,数据库选项卡显示所有连接的查询总数,文件选项卡显示总文件数。

提供时间线数据
-----------------------

提供时间线数据需要:

1. 将 ``$hasTimeline`` 设为 ``true``。
2. 实现 ``formatTimelineData()``。

``formatTimelineData()`` 必须以时间线可以排序和显示的格式返回数组数组。内部数组必须包含:

.. literalinclude:: debugging/005.php

提供 Vars
--------------

向 Vars 选项卡添加数据需要:

1. 将 ``$hasVarData`` 设为 ``true``
2. 实现 ``getVarData()``。

``getVarData()`` 应返回包含要显示的键值对数组的数组。外部数组的键为 Vars 选项卡中的部分名称:

.. literalinclude:: debugging/006.php
