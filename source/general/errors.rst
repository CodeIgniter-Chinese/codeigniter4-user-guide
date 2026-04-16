##############
错误处理
##############

CodeIgniter 通过异常机制为你的系统构建错误报告功能，包括 `SPL 集合 <https://www.php.net/manual/zh/spl.exceptions.php>`_ 以及框架提供的一些异常。

根据你的环境设置，
当抛出错误或异常时，默认操作是显示详细的错误报告，除非应用程序运行在 ``production`` 环境中。在 ``production`` 环境中，会显示更通用的消息，以保持用户的最佳体验。

.. contents::
    :local:
    :depth: 2

使用异常
================

本节为新程序员或对使用异常没有经验的开发者提供一个快速概览。

什么是异常
-------------------

异常只是在异常被"抛出"时发生的事件。这会停止脚本的当前流程，
然后将执行权发送给错误处理器，错误处理器会显示相应的错误页面：

.. literalinclude:: errors/001.php

捕获异常
-------------------

如果你调用的方法可能会抛出异常，可以使用 ``try/catch`` 来捕获该异常：

.. literalinclude:: errors/002.php

如果 ``$userModel`` 抛出异常，它会被捕获，catch 块中的代码会被执行。在这个例子中，
脚本会终止，并输出 ``UserModel`` 定义的错误消息。

捕获特定异常
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在上面的例子中，我们捕获任何类型的异常。如果我们只想监控特定类型的异常，
比如 ``DataException``，可以在 catch 参数中指定。任何其他抛出的异常
如果不是被捕获异常的子类，将被传递给错误处理器：

.. literalinclude:: errors/003.php

这对于自己处理错误或在脚本结束前执行清理操作很有用。如果你希望
错误处理器正常工作，可以在 catch 块中抛出新异常：

.. literalinclude:: errors/004.php

配置
=============

错误报告
---------------

当 PHP ini 设置中的 ``display_errors`` 启用时，CodeIgniter 将显示
包含所有错误的详细错误报告

因此默认情况下，CodeIgniter 会在 ``development`` 和 ``testing`` 环境中
显示详细的错误报告，在 ``production`` 环境中不显示任何错误。

.. image:: ../images/error.png

你可以通过设置 ``CI_ENVIRONMENT`` 变量来更改你的环境。
参见 :ref:`setting-environment`。

.. important:: 禁用错误报告并不会在有错误时停止日志的写入。

.. warning:: 请注意，**.env** 文件中的设置会被添加到 ``$_SERVER``
    和 ``$_ENV`` 中。作为副作用，这意味着如果显示了详细的错误报告，
    **你的安全凭据将被公开暴露**。

异常日志记录
------------------

默认情况下，除了 "404 - Page Not Found" 异常之外的所有异常都会被记录。这可以通过
设置 **app/Config/Exceptions.php** 中的 ``$log`` 值来开启或关闭：

.. literalinclude:: errors/005.php

要忽略对其他状态码的日志记录，可以在同一文件中设置要忽略的状态码：

.. literalinclude:: errors/006.php

.. note:: 如果你当前的 :ref:`日志设置 <logging-configuration>`
    没有设置为记录 ``critical`` 错误（所有异常都被记录为此级别），
    异常的日志记录可能仍然不会发生。

.. _logging_deprecation_warnings:

记录弃用警告
----------------------------

.. versionadded:: 4.3.0

在 v4.3.0 之前，所有由 ``error_reporting()`` 报告的错误都会被抛出为
``ErrorException`` 对象。

但随着 PHP 8.1+ 的普及，许多用户可能会看到为
`向非空内部函数参数传递 null <https://wiki.php.net/rfc/deprecate_null_to_scalar_internal_arg>`_
抛出的异常。

为了简化向 PHP 8.1 的迁移，从 v4.3.0 开始，CodeIgniter 提供了
只记录弃用错误（``E_DEPRECATED`` 和 ``E_USER_DEPRECATED``）
而不将其作为异常抛出的功能。

默认情况下，CodeIgniter 只在开发环境中记录弃用警告而不抛出异常。
在生产环境中，不会进行日志记录，也不会抛出异常。

配置
^^^^^^^^^^^^^

此功能的设置如下。
首先，确保你的 ``Config\Exceptions`` 副本已更新为包含两个新属性，
并按以下方式设置：

.. literalinclude:: errors/012.php

接下来，根据你在 ``Config\Exceptions::$deprecationLogLevel`` 中设置的日志级别，
检查 ``Config\Logger::$threshold`` 中定义的日志记录器阈值是否覆盖了弃用日志级别。
如果没有，相应地调整它。

.. literalinclude:: errors/013.php

之后，后续的弃用警告将按配置记录而不会作为异常抛出。

此功能也适用于用户弃用：

.. literalinclude:: errors/014.php

为了测试应用程序，你可能希望总是在弃用时抛出异常。可以通过
将环境变量 ``CODEIGNITER_SCREAM_DEPRECATIONS`` 设置为真值来配置此功能。

框架异常
====================

.. _exception-design:

异常设计
----------------

从 v4.6.0 开始，框架抛出的所有异常类：

- 实现 ``CodeIgniter\Exceptions\ExceptionInterface``
- 继承 ``CodeIgniter\Exceptions\LogicException`` 或 ``CodeIgniter\Exceptions\RuntimeException``

.. note:: 框架只抛出上述类型的异常类，但 PHP
    或使用的其他库可能会抛出其他异常。

框架抛出的异常有两个基类：

LogicException
--------------

``CodeIgniter\Exceptions\LogicException`` 继承 ``\LogicException``。
此异常表示程序逻辑中的错误。这类异常应该直接导致修复你的代码。

RuntimeException
----------------

``CodeIgniter\Exceptions\RuntimeException`` 继承 ``\RuntimeException``。
如果发生只能在运行时发现的错误，会抛出此异常。

框架还提供以下异常：

PageNotFoundException
---------------------

用于表示 404 Page Not Found 错误：

.. literalinclude:: errors/007.php

你可以向异常传递消息，该消息将显示在 404 页面上替换默认消息。

有关默认 404 视图文件位置，请参见 :ref:`http-status-code-and-error-views`。

如果在 **app/Config/Routing.php** 或 **app/Config/Routes.php** 中指定了
:ref:`404-override`，则会调用它而不是标准的 404 页面。

ConfigException
---------------

当配置类的值无效，或配置类不是正确的类型等情况时，应使用此异常：

.. literalinclude:: errors/008.php

该异常提供退出代码 3。

DatabaseException
-----------------

为数据库错误抛出此异常，例如无法创建数据库连接，
或连接暂时丢失时：

.. literalinclude:: errors/009.php

该异常提供退出代码 8。

RedirectException
-----------------

.. note:: 从 v4.4.0 开始，``RedirectException`` 的命名空间已更改。
    之前它是 ``CodeIgniter\Router\Exceptions\RedirectException``。
    之前的类在 v4.6.0 中已被移除。

此异常是一个特殊情况，允许覆盖所有其他响应路由并强制重定向到特定 URI：

.. literalinclude:: errors/010.php

``$uri`` 是相对于 baseURL 的 URI 路径。你也可以提供
重定向代码来代替默认值（``302``，"临时重定向"）：

.. literalinclude:: errors/011.php

另外，从 v4.4.0 开始，实现 ResponseInterface 的类的对象可以用作第一个参数。
此解决方案适用于需要在响应中添加额外头部或 Cookie 的情况。

.. literalinclude:: errors/018.php

.. _error-specify-http-status-code:

在异常中指定 HTTP 状态码
==========================================

.. versionadded:: 4.3.0

从 v4.3.0 开始，你可以为你的异常类指定 HTTP 状态码，以实现
``CodeIgniter\Exceptions\HTTPExceptionInterface``。

当实现 ``HTTPExceptionInterface`` 的异常被 CodeIgniter 的异常处理器捕获时，
异常代码将成为 HTTP 状态码。

.. _http-status-code-and-error-views:

HTTP 状态码和错误视图
================================

异常处理器显示与 HTTP 状态码对应的错误视图（如果存在）。

例如，``PageNotFoundException`` 实现了 ``HTTPExceptionInterface``，
所以其异常代码 ``404`` 将是 HTTP 状态码。因此如果它被抛出，
当是 Web 请求时，系统将显示 **app/Views/errors/html** 文件夹中的
**error_404.php**。如果是通过 CLI 调用，系统将显示
**app/Views/errors/cli** 文件夹中的 **error_404.php**。

如果没有与 HTTP 状态码对应的视图文件，将显示 **production.php**
或 **error_exception.php**。

.. note:: 如果 PHP ini 设置中的 ``display_errors`` 开启，
    会选择 **error_exception.php** 并显示详细的错误报告。

你应该为你的网站自定义 **app/Views/errors/html** 文件夹中的所有错误视图。

你也可以为特定的 HTTP 状态码创建错误视图。例如，如果你想为
"400 Bad Request" 创建错误视图，添加 **error_400.php**。

.. warning:: 如果存在具有相应 HTTP 状态码的错误视图文件，
    异常处理器将显示该文件，而不管环境如何。
    视图文件必须以在生产环境中不显示详细错误消息的方式自行实现。

.. _error-specify-exit-code:

在异常中指定退出代码
===================================

.. versionadded:: 4.3.0

从 v4.3.0 开始，你可以为你的异常类指定退出代码，以实现
``CodeIgniter\Exceptions\HasExitCodeInterface``。

当实现 ``HasExitCodeInterface`` 的异常被 CodeIgniter 的异常处理器捕获时，
从 ``getExitCode()`` 方法返回的代码将成为退出代码。

.. _custom-exception-handlers:

自定义异常处理器
=========================

.. versionadded:: 4.4.0

如果你需要更多控制异常的显示方式，现在可以定义自己的处理器并
指定它们何时应用。

定义新处理器
------------------------

第一步是创建一个实现 ``CodeIgniter\Debug\ExceptionHandlerInterface`` 的新类。
你也可以继承 ``CodeIgniter\Debug\BaseExceptionHandler``。
这个类包含许多默认异常处理器使用的实用方法。
新处理器必须实现一个方法：``handle()``：

.. literalinclude:: errors/015.php

这个例子定义了通常需要的最小代码量 - 显示视图并以适当的
退出代码退出。但是，``BaseExceptionHandler`` 提供了许多其他辅助函数和对象。

配置新处理器
---------------------------

告诉 CodeIgniter 使用你的新异常处理器类是在 **app/Config/Exceptions.php**
配置文件的 ``handler()`` 方法中完成的：

.. literalinclude:: errors/016.php

你可以使用应用程序需要的任何逻辑来确定是否应该处理异常，
但最常见的是检查 HTTP 状态码或异常类型。如果你的类应该处理它，
则返回该类的新实例：

.. literalinclude:: errors/017.php
