##############
错误处理
##############

CodeIgniter 通过异常机制构建了错误报告系统，既包含 `SPL 集合 <https://www.php.net/manual/en/spl.exceptions.php>`_ 中的异常，也提供了框架专属的异常类型。

根据运行环境的配置，当发生错误或抛出异常时，默认行为是显示详细错误报告（除非应用处于 ``production`` 环境）。在 ``production`` 环境中，会显示更通用的信息以保持最佳用户体验。

.. contents::
    :local:
    :depth: 2

使用异常
================

本节为新手程序员或不熟悉异常使用的开发者提供快速概览。

什么是异常
------------------

异常是当程序 "抛出" 异常时发生的事件。这会中断当前脚本流程，并将执行权转交给错误处理程序以显示相应的错误页面：

.. literalinclude:: errors/001.php

捕获异常
-------------------

当调用可能抛出异常的方法时，可以使用 ``try/catch`` 代码块来捕获异常：

.. literalinclude:: errors/002.php

如果 ``$userModel`` 抛出异常，该异常会被捕获并执行 catch 块中的代码。在此示例中，脚本终止并输出 ``UserModel`` 定义的错误信息。

捕获特定异常
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

上例中我们捕获所有类型的 Exception。若只需捕获特定类型的异常（如 ``DataException``），可在 catch 参数中指定。其他未被捕获的异常类型将传递给错误处理程序：

.. literalinclude:: errors/003.php

这种方式便于自行处理错误或在脚本结束前执行清理操作。若希望错误处理程序按常规方式处理，可在 catch 块中重新抛出异常：

.. literalinclude:: errors/004.php

配置
=============

错误报告
---------------

当 PHP ini 设置中的 ``display_errors`` 启用时，CodeIgniter 将显示包含所有错误的详细报告

默认情况下，CodeIgniter 在 ``development`` 和 ``testing`` 环境中显示详细错误报告，在 ``production`` 环境中不显示任何错误。

.. image:: ../images/error.png

可通过设置 ``CI_ENVIRONMENT`` 变量来更改环境配置，详见 :ref:`setting-environment`。

.. important:: 禁用错误报告不会阻止错误日志的写入。

.. warning:: 注意 **.env** 文件中的设置会被添加到 ``$_SERVER`` 和 ``$_ENV``。副作用是当显示详细错误报告时，**你的敏感凭证可能被公开暴露**。

异常日志记录
------------------

默认情况下，除 "404 - 页面未找到" 异常外，所有异常都会被记录。可通过修改 **app/Config/Exceptions.php** 中的 ``$log`` 值来开关此功能：

.. literalinclude:: errors/005.php

要忽略其他状态码的日志记录，可在同一文件中设置：

.. literalinclude:: errors/006.php

.. note:: 如果当前 :ref:`日志设置 <logging-configuration>` 未配置记录 ``critical`` 级别错误（所有异常均按此级别记录），异常可能仍不会被记录。

.. _logging_deprecation_warnings:

记录弃用警告
----------------------------

.. versionadded:: 4.3.0

在 v4.3.0 之前，所有通过 ``error_reporting()`` 报告的错误都会被抛出为 ``ErrorException`` 对象。

随着 PHP 8.1+ 的普及，用户可能会遇到因 `向内部函数的非空参数传递 null 值 <https://wiki.php.net/rfc/deprecate_null_to_scalar_internal_arg>`_ 导致的异常抛出。

为简化迁移到 PHP 8.1 的过程，从 v4.3.0 开始，CodeIgniter 新增了仅记录弃用错误（``E_DEPRECATED`` 和 ``E_USER_DEPRECATED``）而不将其作为异常抛出的功能。

默认情况下，CodeIgniter 在开发环境中仅记录弃用警告而不抛出异常。在生产环境中，既不记录也不抛出异常。

配置
^^^^^^^^^^^^^

该功能的配置步骤如下：
首先确保 **Config\Exceptions** 已更新并包含以下两个新属性：

.. literalinclude:: errors/012.php

其次，根据 ``Config\Exceptions::$deprecationLogLevel`` 设置的日志级别，检查 ``Config\Logger::$threshold`` 定义的日志阈值是否涵盖该级别。如未涵盖需相应调整：

.. literalinclude:: errors/013.php

配置完成后，后续弃用警告将按配置记录而不作为异常抛出。

该功能也支持用户自定义弃用警告：

.. literalinclude:: errors/014.php

测试应用时若需强制抛出弃用警告，可设置环境变量 ``CODEIGNITER_SCREAM_DEPRECATIONS`` 为真值。

框架异常
====================

.. _exception-design:

异常设计
----------------

自 v4.6.0 起，框架抛出的所有异常类：

- 实现 ``CodeIgniter\Exceptions\ExceptionInterface``
- 继承 ``CodeIgniter\Exceptions\LogicException`` 或 ``CodeIgniter\Exceptions\RuntimeException``

.. note:: 框架仅抛出上述类型异常，但 PHP 或其他使用的库可能抛出其他异常。

框架抛出的两种基础异常类：

LogicException
--------------

``CodeIgniter\Exceptions\LogicException`` 继承自 ``\LogicException``。该异常表示程序逻辑错误，应直接通过修改代码修复。

RuntimeException
----------------

``CodeIgniter\Exceptions\RuntimeException`` 继承自 ``\RuntimeException``。该异常在运行时发生错误时抛出。

其他可用框架异常：

PageNotFoundException
---------------------

用于触发 404 页面未找到错误：

.. literalinclude:: errors/007.php

可传递自定义消息替代默认的 404 页面信息。默认 404 视图文件位置参见 :ref:`http-status-code-and-error-views`。

如果在 **app/Config/Routing.php** 或 **app/Config/Routes.php** 中配置了 :ref:`404-override`，将调用该覆盖配置而非标准 404 页面。

ConfigException
---------------

当配置类值无效或配置类类型不符时使用此异常：

.. literalinclude:: errors/008.php

该异常提供退出码 3。

DatabaseException
-----------------

在数据库连接创建失败或临时丢失等数据库错误时抛出：

.. literalinclude:: errors/009.php

该异常提供退出码 8。

RedirectException
-----------------

.. note:: 自 v4.4.0 起，``RedirectException`` 的命名空间已变更。原为 ``CodeIgniter\Router\Exceptions\RedirectException``，该旧类已在 v4.6.0 移除。

此特殊异常允许覆盖其他响应路由并强制重定向到指定 URI：

.. literalinclude:: errors/010.php

``$uri`` 是相对于 baseURL 的 URI 路径。可指定替代默认值（``302``，"临时重定向"）的重定向代码：

.. literalinclude:: errors/011.php

自 v4.4.0 起，第一个参数可使用实现 ResponseInterface 的对象。此方案适用于需要添加额外头信息或 cookies 的场景：

.. literalinclude:: errors/018.php

.. _error-specify-http-status-code:

在异常中指定 HTTP 状态码
==========================================

.. versionadded:: 4.3.0

自 v4.3.0 起，可通过让异常类实现 ``CodeIgniter\Exceptions\HTTPExceptionInterface`` 来指定 HTTP 状态码。

当 CodeIgniter 异常处理器捕获到实现 ``HTTPExceptionInterface`` 的异常时，异常代码将作为 HTTP 状态码。

.. _http-status-code-and-error-views:

HTTP 状态码与错误视图
=========================

异常处理器会显示与 HTTP 状态码对应的错误视图（如果存在）。

例如，``PageNotFoundException`` 实现了 ``HTTPExceptionInterface``，其异常代码 ``404`` 将作为 HTTP 状态码。当该异常被抛出时：

- 网页请求会显示 **app/Views/errors/html** 目录下的 **error_404.php**
- CLI 请求会显示 **app/Views/errors/cli** 目录下的 **error_404.php**

若无对应 HTTP 状态码的视图文件，将显示 **production.php** 或 **error_exception.php**。

.. note:: 若 PHP ini 设置中 ``display_errors`` 开启，将选择 **error_exception.php** 并显示详细错误报告。

建议在 **app/Views/errors/html** 目录下自定义所有错误视图。

可为特定 HTTP 状态码创建错误视图。例如创建 "400 Bad Request" 错误视图需添加 **error_400.php**。

.. warning:: 若存在对应 HTTP 状态码的错误视图文件，异常处理器将始终显示该文件。必须确保视图文件在生产环境中不会自行显示详细错误信息。

.. _error-specify-exit-code:

在异常中指定退出码
=============================

.. versionadded:: 4.3.0

自 v4.3.0 起，可通过让异常类实现 ``CodeIgniter\Exceptions\HasExitCodeInterface`` 来指定退出码。

当 CodeIgniter 异常处理器捕获到实现 ``HasExitCodeInterface`` 的异常时，将从 ``getExitCode()`` 方法获取退出码。

.. _custom-exception-handlers:

自定义异常处理器
=========================

.. versionadded:: 4.4.0

若需更精细控制异常显示方式，可定义自定义处理器并指定其应用场景。

定义新处理器
------------------------

首先创建实现 ``CodeIgniter\Debug\ExceptionHandlerInterface`` 的新类。也可继承 ``CodeIgniter\Debug\BaseExceptionHandler``，该类包含默认异常处理器使用的实用方法。新处理器需实现 ``handle()`` 方法：

.. literalinclude:: errors/015.php

此示例展示了典型的最小实现：显示视图并以正确退出码终止。``BaseExceptionHandler`` 还提供其他辅助功能和对象。

配置新处理器
---------------------------

在 **app/Config/Exceptions.php** 配置文件的 ``handler()`` 方法中指定使用新异常处理器类：

.. literalinclude:: errors/016.php

可使用任意逻辑决定是否处理异常，最常见的是检查 HTTP 状态码或异常类型。若应由自定义类处理，则返回该类实例：

.. literalinclude:: errors/017.php
