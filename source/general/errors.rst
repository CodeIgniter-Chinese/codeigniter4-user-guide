##############
错误处理
##############

CodeIgniter 通过 Exceptions 在你的系统中内置了错误报告,包括
`SPL 集合 <https://www.php.net/manual/en/spl.exceptions.php>`_,以及框架提供的一些自定义 exceptions。
取决于你的环境设置,当抛出错误或异常时的默认操作是显示详细的错误报告,除非应用程序在 ``production`` 环境下运行。
在这种情况下,会显示更通用的消息以对用户保持最佳体验。

.. contents::
    :local:
    :depth: 2

使用 Exceptions
================

本节简要概述了对 Exceptions 不太了解的新程序员或开发人员的情况。

Exceptions 简单来说就是在抛出异常时发生的事件。这将中止脚本的当前流程,然后执行将转移到错误处理程序,后者将显示适当的错误页面:

.. literalinclude:: errors/001.php

如果你正在调用可能抛出异常的方法,你可以使用 ``try/catch`` 块捕获该异常:

.. literalinclude:: errors/002.php

如果 ``$userModel`` 抛出异常,则会捕获它并执行 catch 块中的代码。在这个例子中,脚本终止,并回显 ``UserModel`` 定义的错误信息。

在上面的示例中,我们捕获任何类型的 Exception。如果我们只想监视特定类型的异常,如 ``UnknownFileException``,我们可以在 catch 参数中指定它。任何其他抛出的不属于捕获的异常子类的异常都将传递给错误处理程序:

.. literalinclude:: errors/003.php

这在自己处理错误或在脚本结束前执行清理时很有用。如果你想要错误处理程序正常工作,你可以在 catch 块内抛出一个新异常:

.. literalinclude:: errors/004.php

配置
=============

默认情况下,CodeIgniter 将在 ``development`` 和 ``testing`` 环境中显示所有错误,并且在 ``production`` 环境中不显示任何错误。你可以通过在 **.env** 文件中设置 ``CI_ENVIRONMENT`` 变量来更改此设置。

.. important:: 禁用错误报告并不会停止在错误发生时写入日志。

记录 Exceptions
------------------

默认情况下,除了 404 - 页面未找到异常之外的所有异常都会记录日志。这可以通过设置 **app/Config/Exceptions.php** 的 ``$log`` 值来打开和关闭:

.. literalinclude:: errors/005.php

要忽略其他状态码的日志记录,可以在同一文件中设置要忽略的状态码:

.. literalinclude:: errors/006.php

.. note:: 如果你当前的日志设置没有配置记录**关键**错误,则仍可能不会为exceptions记录日志,因为所有exceptions都记录为关键错误。

框架 Exceptions
====================

以下框架异常可用:

PageNotFoundException
---------------------

这用于表示 404 页面未找到错误。抛出时,系统将显示在 **app/Views/errors/html/error_404.php** 中找到的视图。你应该自定义站点的所有错误视图。如果在 **app/Config/Routes.php** 中指定了 404 覆盖页面,则会调用它而不是标准的 404 页面:

.. literalinclude:: errors/007.php

你可以传入一个消息到异常中,它将显示在404页面上的默认消息位置:

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

此异常是一个特殊情况,允许覆盖所有其他响应路由并强制重定向到特定路由或 URL:

.. literalinclude:: errors/010.php

``$route`` 可以是命名路由、相对 URI 或完整 URL。你还可以提供要使用的重定向代码,而不是默认值(``302``、“临时重定向”):

.. literalinclude:: errors/011.php

.. _error-specify-http-status-code:

在异常中指定 HTTP 状态码
==========================================

.. versionadded:: 4.3.0

从 v4.3.0 开始,你可以为异常类指定 HTTP 状态码来实现
``HTTPExceptionInterface``。

当 CodeIgniter 的异常处理程序捕获实现了 ``HTTPExceptionInterface`` 的异常时,异常代码将成为 HTTP 状态码。

.. _error-specify-exit-code:

在异常中指定退出代码
===================================

.. versionadded:: 4.3.0

从 v4.3.0 开始,你可以为异常类指定退出代码来实现
``HasExitCodeInterface``。

当 CodeIgniter 的异常处理程序捕获实现了 ``HasExitCodeInterface`` 的异常时, ``getExitCode()`` 方法返回的代码将成为退出代码。

.. _logging_deprecation_warnings:

记录弃用警告
============================

.. versionadded:: 4.3.0

默认情况下, ``error_reporting()`` 报告的所有错误都会作为 ``ErrorException`` 对象抛出。这些错误包括 ``E_DEPRECATED`` 和 ``E_USER_DEPRECATED`` 错误。随着 PHP 8.1+ 的大规模使用,许多用户可能会看到由于 `向内部函数的非空参数传递 null <https://wiki.php.net/rfc/deprecate_null_to_scalar_internal_arg>`_ 抛出的异常。为了方便迁移到 PHP 8.1,你可以指示 CodeIgniter 记录弃用而不是抛出它们。

首先,确保你的 ``Config\Exceptions`` 副本已更新,并设置如下:

.. literalinclude:: errors/012.php

接下来,根据在 ``Config\Exceptions::$deprecationLogLevel`` 中设置的日志级别,检查在 ``Config\Logger::$threshold`` 中定义的记录器阈值是否涵盖了弃用日志级别。如果没有,请相应调整它。

.. literalinclude:: errors/013.php

之后,后续的弃用将被记录而不是抛出。

此功能也适用于用户弃用:

.. literalinclude:: errors/014.php

为了测试你的应用程序,你可能希望始终在弃用时抛出。你可以通过将环境变量 ``CODEIGNITER_SCREAM_DEPRECATIONS`` 设置为真值来配置此行为。
