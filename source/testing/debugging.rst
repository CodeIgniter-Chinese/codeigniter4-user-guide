##########################
调试应用程序
##########################

.. contents::
    :local:
    :depth: 2

*************
检查日志
*************

.. _codeigniter-error-logs:

CodeIgniter 错误日志
======================

CodeIgniter 根据 **app/Config/Logger.php** 中的设置记录错误信息。

默认配置下，日志文件每天存储在 **writable/logs** 目录中。
如果事情没有按预期进行，检查这些日志是个好主意！

你可以调整错误阈值以查看更多或更少的信息。详情请参见
:ref:`Logging <logging-configuration>`。

记录所有 SQL 查询
=======================

CodeIgniter 发出的所有 SQL 查询都可以被记录。
详情请参见 :ref:`Database Events <database-events-dbquery>`。

********************
替换 var_dump()
********************

虽然使用 Xdebug 和一个好的 IDE 对调试你的应用程序是不可或缺的，
但有时一个简单的 ``var_dump()`` 就足够了。CodeIgniter 通过捆绑
优秀的 PHP 调试工具 `Kint <https://kint-php.github.io/kint/>`_ 使这一点变得更好。

这远远超出了你通常的工具，提供了许多替代数据，
例如将时间戳格式化为可识别的日期，显示颜色的十六进制代码，
将数组数据显示为易于阅读的表格，等等。

启用 Kint
=============

默认情况下,Kint 仅在 **development** 和 **testing** :doc:`环境 </general/environments>` 中启用。当常量 ``CI_DEBUG`` 定义且值为 true 时就会启用它。常量定义在引导文件中(例如 **app/Config/Boot/development.php**)。

使用 Kint
==========

d()
---

``d()`` 方法将传入的唯一参数的数据全部输出到屏幕,允许脚本继续执行:

.. literalinclude:: debugging/001.php
    :lines: 2-

dd()
----

这个方法与 ``d()`` 一样,但会在输出数据后 ``die()``,请求不再执行后续代码。

trace()
-------

这会以 Kint 独特的方式提供当前执行点的回溯:

.. literalinclude:: debugging/002.php
    :lines: 2-

更多信息请参考 `Kint 文档 <https://kint-php.github.io/kint//>`_。

.. _the-debug-toolbar:

*****************
调试工具栏
*****************

调试工具栏可以一目了然地查看当前页面请求的信息,包括基准测试结果、执行的查询、请求和响应数据等。这在开发过程中有助于调试和优化。

.. note:: 调试工具栏仍在开发中,许多计划的功能尚未实现。

启用工具栏
====================

除 **production** 环境外,调试工具栏在其他所有 :doc:`环境 </general/environments>` 下默认启用。当常量 ``CI_DEBUG`` 定义且值为 true 时就会显示。常量定义在引导文件中(例如 **app/Config/Boot/development.php**),可以在其中修改以确定显示的环境。

.. note:: 当你的 ``baseURL`` 设置(在 **app/Config/App.php** 或 ``app.baseURL`` 在 **.env** 中)与实际 URL 不匹配时,不会显示调试工具栏。

工具栏本身显示为一个 :doc:`后置过滤器 </incoming/filters>`。你可以通过从 **app/Config/Filters.php** 文件的 ``$required``（或 ``$globals``）属性中移除 ``'toolbar'`` 来阻止它运行。

.. note:: 在 v4.5.0 之前，工具栏默认设置为 ``$globals``。

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

.. _debug-toolbar-hot-reload:

热重载
=============

.. versionadded:: 4.4.0

调试工具栏包含一个名为热重载的功能，它允许你对应用程序的代码进行更改，并在浏览器中自动重新加载，而无需刷新页面。这在开发过程中非常省时。

在开发过程中启用热重载，你可以点击工具栏左侧的按钮，它看起来像一个刷新图标。这将在所有页面上启用热重载，直到你禁用它。

热重载通过每秒扫描 **app** 目录中的文件并查找更改来工作。如果发现任何更改，它将向浏览器发送消息以重新加载页面。它不会扫描任何其他目录，因此如果你对 **app** 目录之外的文件进行更改，你需要手动刷新页面。

如果你需要监视 **app** 目录之外的文件，或者由于项目的大小而导致速度较慢，你可以在 **app/Config/Toolbar.php** 配置文件的 ``$watchedDirectories`` 和 ``$watchedExtensions`` 属性中指定要扫描的目录和文件扩展名。
