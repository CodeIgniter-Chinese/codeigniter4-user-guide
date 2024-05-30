##############
错误处理
##############

CodeIgniter 通过“异常（Exception）”在你的系统中内置了错误报告,包括
`SPL 集合 <https://www.php.net/manual/en/spl.exceptions.php>`_,以及框架提供的一些“异常”。

取决于你的环境设置,当抛出错误或异常时的默认操作是显示详细的错误报告,除非应用程序在 ``production`` 环境下运行。
在 ``production`` 环境中,会显示更通用的消息以对用户保持最佳体验。

.. contents::
    :local:
    :depth: 2

使用异常
================

本节简要概述了对异常不太了解的新程序员或开发人员的情况。

什么是异常
------------------

异常简单来说就是在抛出异常时发生的事件。这将中止脚本的当前流程,然后执行将转移到错误处理程序,后者将显示适当的错误页面:

.. literalinclude:: errors/001.php

捕获异常
-------------------

如果你正在调用可能抛出异常的方法,你可以使用 ``try/catch`` 块捕获该异常:

.. literalinclude:: errors/002.php

如果 ``$userModel`` 抛出异常,则会捕获它并执行 catch 块中的代码。在这个例子中,脚本终止,并回显 ``UserModel`` 定义的错误信息。

捕获特定异常
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在上面的示例中,我们捕获任何类型的异常。如果我们只想监视特定类型的异常,如 ``DataException``,我们可以在 catch 参数中指定它。任何其他抛出的不属于捕获的异常子类的异常都将传递给错误处理程序:

.. literalinclude:: errors/003.php

这在自己处理错误或在脚本结束前执行清理时很有用。如果你想要错误处理程序正常工作,你可以在 catch 块内抛出一个新异常:

.. literalinclude:: errors/004.php

配置
=============

错误报告
---------------

默认情况下，CodeIgniter 在 ``development`` 和 ``testing`` 环境下会显示包含所有错误的详细错误报告，并且在 ``production`` 环境下不会显示任何错误。

.. image:: ../images/error.png

你可以通过设置 ``CI_ENVIRONMENT`` 变量来更改你的环境。请参阅 :ref:`setting-environment`。

.. important:: 禁用错误报告并不会停止在错误发生时写入日志。

.. warning:: 请注意，**.env** 文件中的设置会添加到 ``$_SERVER`` 和 ``$_ENV`` 中。作为副作用，这意味着如果显示详细的错误报告，**你的安全凭据将被公开**。

记录异常
------------------

默认情况下,除了“404 - Page Not Found”异常之外的所有异常都会记录日志。这可以通过设置 **app/Config/Exceptions.php** 的 ``$log`` 值来打开和关闭:

.. literalinclude:: errors/005.php

要忽略其他状态码的日志记录,可以在同一文件中设置要忽略的状态码:

.. literalinclude:: errors/006.php

.. note:: 如果你的当前 :ref:`日志配置 <logging-configuration>` 没有设置记录 ``critical`` 错误的话，异常仍然可能不会被记录，因为所有的异常都作为 ``critical`` 错误来记录。

.. _logging_deprecation_warnings:

弃用警告日志
------------

.. versionadded:: 4.3.0

默认情况下，所有由 ``error_reporting()`` 报告的错误都会作为 ``ErrorException`` 对象抛出。这包括 ``E_DEPRECATED`` 和 ``E_USER_DEPRECATED`` 错误。随着 PHP 8.1+ 的使用激增，许多用户可能会看到由于 `passing null to non-nullable arguments of internal functions <https://wiki.php.net/rfc/deprecate_null_to_scalar_internal_arg>`_ 抛出的异常。为了简化向 PHP 8.1 的迁移，你可以指示 CodeIgniter 记录这些弃用警告，而不是抛出它们。

首先，确保你的 ``Config\Exceptions`` 副本已更新了两个新属性并设置如下：

.. literalinclude:: errors/012.php

接下来，根据你在 ``Config\Exceptions::$deprecationLogLevel`` 中设置的日志级别，检查 ``Config\Logger::$threshold`` 中定义的日志门槛是否涵盖了弃用日志级别。如果没有，请相应调整。

.. literalinclude:: errors/013.php

之后，后续的弃用警告将会被记录而不是抛出。

此功能也适用于用户弃用警告：

.. literalinclude:: errors/014.php

对于测试你的应用程序，你可能希望总是抛出弃用警告。你可以通过将环境变量 ``CODEIGNITER_SCREAM_DEPRECATIONS`` 设置为真值来配置这一点。

框架异常
====================

以下框架异常可用:

PageNotFoundException
---------------------

这用于表示 404，页面未找到错误：

.. literalinclude:: errors/007.php

你可以传入一个消息到异常中,它将显示在404页面上的默认消息位置:

有关默认的 404 视图文件位置，请参见 :ref:`http-status-code-and-error-views`。

如果你在 **app/Config/Routing.php** 或 **app/Config/Routes.php** 中指定了 :ref:`404-override`，那么将会调用这个覆盖页面，而不是标准的 404 页面。

ConfigException
---------------

当配置类的值无效时,或者配置类不是正确的类型时,应使用此异常:

.. literalinclude:: errors/008.php

这提供退出代码 3。

DatabaseException
-----------------

此异常用于数据库错误,例如无法创建数据库连接或连接暂时丢失时:

.. literalinclude:: errors/009.php

这提供退出代码 8。

RedirectException
-----------------

.. note:: 自 v4.4.0 起，``RedirectException`` 的命名空间已更改。之前是 ``CodeIgniter\Router\Exceptions\RedirectException``。之前的类已被弃用。

此异常是一个特殊情况,允许覆盖所有其他响应路由并强制重定向到特定的 URI:

.. literalinclude:: errors/010.php

``$uri`` 是相对于 baseURL 的 URI 路径。你还可以提供一个重定向代码，以替代默认值 (``302``, "temporary redirect"):

.. literalinclude:: errors/011.php

另外，自 v4.4.0 版本开始，可以将实现了 ResponseInterface 接口的类的对象用作第一个参数。这种解决方案适用于需要在响应中添加额外的头部或 Cookie 的情况。

.. literalinclude:: errors/018.php

.. _error-specify-http-status-code:

在异常中指定 HTTP 状态码
==========================================

.. versionadded:: 4.3.0

从 v4.3.0 开始,你可以为异常类指定 HTTP 状态码来实现
``CodeIgniter\Exceptions\HTTPExceptionInterface``。

当 CodeIgniter 的异常处理程序捕获实现了 ``HTTPExceptionInterface`` 的异常时,异常代码将成为 HTTP 状态码。

.. _http-status-code-and-error-views:

HTTP 状态码和错误视图
=========================

异常处理程序会显示对应于 HTTP 状态码的错误视图（如果存在的话）。

例如，``PageNotFoundException`` 实现了 ``HTTPExceptionInterface``，所以它的异常代码 ``404`` 将成为 HTTP 状态码。因此，如果它被抛出，系统将在处理网页请求时显示 **app/Views/errors/html** 文件夹中的 **error_404.php**。如果是通过 CLI 调用，系统将显示 **app/Views/errors/cli** 文件夹中的 **error_404.php**。

如果没有与 HTTP 状态码对应的视图文件，那么将显示 **production.php** 或 **error_exception.php**。

.. note:: 如果在 PHP INI 配置中开启了 ``display_errors``，将选择 **error_exception.php** 并显示详细的错误报告。

你应该自定义 **app/Views/errors/html** 文件夹中的所有错误视图以适应你的站点。

你还可以为特定的 HTTP 状态码创建错误视图。例如，如果你想创建一个 "400 Bad Request" 的错误视图，添加 **error_400.php**。

.. warning:: 如果存在对应 HTTP 状态码的错误视图文件，异常处理程序将无论环境如何显示该文件。视图文件必须自行实现，不在生产环境中显示详细的错误信息。

.. _error-specify-exit-code:

在你的异常中指定退出代码
=============================

.. versionadded:: 4.3.0

自 v4.3.0 起，你可以为你的异常类指定退出代码，以实现 ``CodeIgniter\Exceptions\HasExitCodeInterface``。

当实现了 ``HasExitCodeInterface`` 的异常被 CodeIgniter 的异常处理程序捕获时，从 ``getExitCode()`` 方法返回的代码将成为退出代码。

.. _custom-exception-handlers:

自定义异常处理程序
=========================

.. versionadded:: 4.4.0

如果你需要更多地控制异常的显示方式，现在可以定义自己的处理程序并指定它们适用的情况。

定义新的处理程序
------------------------

第一步是创建一个新的类，该类实现了 ``CodeIgniter\Debug\ExceptionHandlerInterface`` 接口。你还可以扩展 ``CodeIgniter\Debug\BaseExceptionHandler`` 类。该类包含了许多在默认异常处理程序中使用的实用方法。新的处理程序必须实现一个方法：``handle()``：

.. literalinclude:: errors/015.php

这个示例定义了通常需要的最少代码 - 显示一个视图并使用适当的退出代码退出。然而，``BaseExceptionHandler`` 提供了许多其他的辅助函数和对象。

配置新的处理程序
---------------------------

告诉 CodeIgniter 使用你的新异常处理程序类是在 **app/Config/Exceptions.php** 配置文件的 ``handler()`` 方法中完成的：

.. literalinclude:: errors/016.php

你可以使用任何逻辑来确定应用程序是否应该处理异常，但最常见的两种情况是检查 HTTP 状态码或异常的类型。如果你的类应该处理它，则返回一个新的实例：

.. literalinclude:: errors/017.php
