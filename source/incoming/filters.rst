##################
控制器过滤器
##################

.. contents::
    :local:
    :depth: 3

控制器过滤器允许你在控制器执行之前或之后执行操作。与 :doc:`事件 <../extending/events>` 不同，你可以选择将过滤器应用于特定的 URI 或路由。前置过滤器可以修改请求，而后置过滤器可以对响应进行操作甚至修改，从而提供了很大的灵活性和功能。

使用过滤器可以执行的一些常见任务示例:

* 对传入请求执行 CSRF 保护
* 根据角色限制站点的区域访问
* 对某些端点执行速率限制
* 显示“维护中”页面
* 执行自动内容协商
* 等等...

*****************
创建过滤器
*****************

过滤器是简单的类,实现了 ``CodeIgniter\Filters\FilterInterface``。它们包含两个方法:``before()`` 和 ``after()``,这些方法分别包含在控制器之前和之后运行的代码。你的类必须包含这两个方法,但如果不需要可以留空。过滤器骨架类如下:

.. literalinclude:: filters/001.php

前置过滤器
==============

替换请求
-----------------

在任何过滤器中,你都可以返回 ``$request`` 对象,它将替换当前的请求,允许你进行更改,这些更改在控制器执行时仍然存在。

停止后续过滤器
----------------------

当你有一系列过滤器时,你可能还希望在某个过滤器后停止后续过滤器的执行。你可以通过返回任何非空结果轻松地实现这一点。如果前置过滤器返回空结果,仍将执行控制器操作或后续过滤器。

非空结果规则的一个例外是 ``Request`` 实例。在前置过滤器中返回它不会停止执行,只会替换当前的 ``$request`` 对象。

返回响应
------------------

由于前置过滤器是在执行控制器之前执行的,所以有时你可能希望停止控制器中的操作。

这通常用于执行重定向,如下面的示例:

.. literalinclude:: filters/002.php

如果返回 ``Response`` 实例,将向客户端发送响应,并停止脚本执行。这对于实现 API 的速率限制很有用。请参见 :doc:`Throttler <../libraries/throttler>` 以获取示例。

.. _after-filters:

后置过滤器
=============

后置过滤器与前置过滤器几乎完全相同,只是你只能返回 ``$response`` 对象,并且无法停止脚本执行。这确实允许你修改最终输出,或者只是做一些最终输出的事情。这可以用于确保某些安全头正确设置,缓存最终输出,或者使用禁用词过滤器过滤最终输出。

*******************
配置过滤器
*******************

配置过滤器的运行方式有两种。一种是在 **app/Config/Filters.php** 中进行配置，另一种是在 **app/Config/Routes.php** 中进行配置。

如果你想为定义的路由指定过滤器，请使用 **app/Config/Routes.php** 并参考 :ref:`URI 路由 <applying-filters>`。

.. note:: 应用过滤器最安全的方法是 :ref:`禁用自动路由 <use-defined-routes-only>`，并 :ref:`将过滤器设置到路由 <applying-filters>`。

app/Config/Filters.php
======================

**app/Config/Filters.php** 文件包含四个属性，允许你精确配置过滤器的运行时机。

.. warning:: 建议你在过滤器设置中的 URI 末尾始终添加 ``*``。因为控制器方法可能比你想象的通过不同的 URL 访问。例如,当启用 :ref:`auto-routing-legacy` 时,如果你有 ``Blog::index()``,它可以通过 ``blog``、``blog/index`` 和 ``blog/index/1`` 等方式访问。

.. _filters-aliases:

$aliases
--------

``$aliases`` 数组用于将一个简单的名称与一个或多个完全限定类名关联起来，这些类名是要运行的过滤器：

.. literalinclude:: filters/003.php

别名是强制性的，如果你尝试稍后使用完整的类名，系统会抛出错误。

以这种方式定义它们可以简化类的切换。当你决定需要更换不同的认证系统时，这种方式非常有用，因为你只需更改过滤器的类即可。

你可以将多个过滤器组合成一个别名，使得应用复杂的过滤器集变得简单：

.. literalinclude:: filters/004.php

你应该根据需要定义尽可能多的别名。

.. _filters-required:

$required
---------

.. versionadded:: 4.5.0

本章节允许你定义 **Required Filters** （必需过滤器）。它们是应用于框架所做的每个请求的特殊过滤器。它们在其他种类的过滤器之前和之后应用，这些过滤器将在下面解释。

.. note:: Required Filters 总是会被执行。然而，如果路由不存在，则只会执行 Before Filters。

你应该注意在这里使用的数量，因为在每个请求上运行太多可能会带来性能影响。但默认设置的过滤器提供了框架功能。如果移除，这些功能将不再工作。详细信息请参见 :ref:`provided-filters`。

过滤器可以通过将它们的别名添加到 ``before`` 或 ``after`` 数组中来指定：

.. literalinclude:: filters/013.php

.. _filters-globals:

$globals
--------

本章节允许你定义任何应用于框架的每个有效请求的过滤器。

在这里使用太多可能会对性能产生影响,所以要小心。

可以通过将别名添加到 ``before`` 或 ``after`` 数组来指定过滤器:

.. literalinclude:: filters/005.php

排除少数 URI
^^^^^^^^^^^^^^^^^^^^^

有时候你想将过滤器应用于几乎每个请求，但有一些请求需要被排除在外。一个常见的例子就是，如果你需要从 CSRF 保护过滤器中排除几个 URI，以允许第三方网站的请求访问一个或两个特定的 URI，同时保持其余 URI 的保护。

要做到这一点，请在别名旁边添加一个包含 ``except`` 键和要匹配的 URI 路径（相对于 BaseURL）值的数组：

.. literalinclude:: filters/006.php

.. warning:: 在 v4.4.7 之前，由于一个漏洞，被过滤器处理的 URI 路径没有进行 URL 解码。换句话说，路由中指定的 URI 路径和过滤器中指定的 URI 路径可能会不同。详细信息请参见 :ref:`upgrade-447-filter-paths`。

在过滤器设置中，任何可以使用 URI 路径（相对于 BaseURL）的地方，你都可以使用正则表达式，或者像上面的例子中那样，使用星号 (``*``) 作为通配符来匹配其后的所有字符。在这个例子中，任何以 ``api/`` 开头的 URI 路径都将被排除在 CSRF 保护之外，但网站的表单将全部受到保护。

如果你需要指定多个 URI,可以使用 URI 路径模式数组:

.. literalinclude:: filters/007.php

$methods
--------

.. warning:: 如果使用 ``$methods`` 过滤器,你应该 :ref:`禁用自动路由(传统) <use-defined-routes-only>`,因为 :ref:`auto-routing-legacy` 允许任何 HTTP 方法访问控制器。以你不期望的方法访问控制器可能会绕过过滤器。

你可以对某个 HTTP 方法（如 ``POST``、``GET``、``PUT`` 等）的所有请求应用过滤器。其值将是一个要运行的过滤器数组：

.. literalinclude:: filters/008.php

.. note:: 与 ``$globals`` 或 ``$filters`` 属性不同,这些只能作为前置过滤器运行。

除了标准的 HTTP 方法外，这里还支持一个特殊情况：``CLI``。``CLI`` 方法将应用于所有从命令行运行的请求。

.. note:: 在 v4.5.0 之前，由于一个错误，你需要以 **小写** 指定 HTTP 方法名称。

$filters
--------

该属性是一个过滤器别名数组。对于每个别名,你可以为 ``before`` 和 ``after`` 数组指定过滤器应该应用到的一系列 URI 路径（相对于 BaseURL）模式:

.. literalinclude:: filters/009.php

.. warning:: 在 v4.4.7 之前，由于一个漏洞，被过滤器处理的 URI 路径没有进行 URL 解码。换句话说，路由中指定的 URI 路径和过滤器中指定的 URI 路径可能会不同。详细信息请参见 :ref:`upgrade-447-filter-paths`。

.. _filters-filters-filter-arguments:

过滤器参数
^^^^^^^^^^^^^^^^

.. versionadded:: 4.4.0

在配置 ``$filters`` 时，可以传递额外的参数给过滤器：

.. literalinclude:: filters/012.php

在这个例子中，当 URI 匹配 ``admin/*'`` 时，数组 ``['admin', 'superadmin']`` 将作为 ``$arguments`` 传递给 ``group`` 过滤器的 ``before()`` 方法。当 URI 匹配 ``admin/users/*'`` 时，数组 ``['users.manage']`` 将作为 ``$arguments`` 传递给 ``permission`` 过滤器的 ``before()`` 方法。

.. _filter-execution-order:

过滤器执行顺序
================

.. important:: 从 v4.5.0 开始，过滤器的执行顺序发生了变化。如果你希望保持与之前版本相同的执行顺序，你必须将 ``Config\Feature::$oldFilterOrder`` 设置为 ``true``。

过滤器按照以下顺序执行：

- **前置过滤器**: required → globals → methods → filters → route
- **后置过滤器**: route → filters → globals → required

.. note:: *required* 过滤器可以从 v4.5.0 开始使用。

.. note:: 在 v4.5.0 之前，指定给路由（在 **app/Config/Routes.php** 中）的过滤器会先于在 **app/Config/Filters.php** 中指定的过滤器执行。而在 Route 过滤器和 Filters 过滤器的后置过滤器执行顺序并没有倒序。详细信息请参见 :ref:`升级指南 <upgrade-450-filter-execution-order>`。

******************
确认过滤器
******************

CodeIgniter 提供了以下 :doc:`命令 <../cli/spark_commands>` 来检查路由的过滤器。

.. _spark-filter-check:

filter:check
============

.. versionadded:: 4.3.0

例如，使用 **GET** 方法检查路由 ``/`` 的过滤器:

.. code-block:: console

    php spark filter:check get /

输出如下所示:

.. code-block:: none

    +--------+-------+----------------+---------------+
    | Method | Route | Before Filters | After Filters |
    +--------+-------+----------------+---------------+
    | GET    | /     |                | toolbar       |
    +--------+-------+----------------+---------------+

你还可以通过 ``spark routes`` 命令查看路由和过滤器，
但是当你在路由中使用正则表达式时，它可能无法显示准确的过滤器。
具体详情请查看 :ref:`URI 路由 <routing-spark-routes>`。

.. _provided-filters:

****************
自带的过滤器
****************

CodeIgniter4 自带的过滤器有：

- ``cors`` => :doc:`../libraries/cors`
- ``csrf`` => :ref:`CSRF <cross-site-request-forgery>`
- ``toolbar`` => :ref:`DebugToolbar <the-debug-toolbar>`
- ``honeypot`` => :doc:`Honeypot <../libraries/honeypot>`
- ``invalidchars`` => :ref:`invalidchars`
- ``secureheaders`` => :ref:`secureheaders`
- ``forcehttps`` => :ref:`forcehttps`
- ``pagecache`` => :doc:`PageCache <../general/caching>`
- ``performance`` => :ref:`performancemetrics`

.. note:: 过滤器按配置文件中定义的顺序执行。但是,如果启用, ``DebugToolbar`` 总是最后执行,因为它应该能够捕获其他过滤器中发生的所有事情。

.. _forcehttps:

ForceHTTPS
==========

.. versionadded:: 4.5.0

此过滤器提供了“强制全局安全请求”功能。

如果你将 ``Config\App:$forceGlobalSecureRequests`` 设置为 true，这将强制所有对该应用程序的请求通过安全连接（HTTPS）进行。如果传入的请求不安全，用户将被重定向到页面的安全版本，并且会设置 HTTP 严格传输安全 (HSTS) 头。

.. _performancemetrics:

PerformanceMetrics
==================

.. versionadded:: 4.5.0

此过滤器提供性能指标的伪变量。

如果你想显示从 CodeIgniter 启动到最终输出发送到浏览器前这一时间段的总耗时，只需在一个视图文件中放置这个伪变量::

    {elapsed_time}

如果你想在视图文件中显示你的内存使用量，使用此伪变量::

    {memory_usage}

如果你不需要此功能，请从 ``$required['after']`` 中移除 ``'performance'``。

.. _invalidchars:

InvalidChars
=============

此过滤器禁止用户输入数据(``$_GET``、``$_POST``、``$_COOKIE``、``php://input``)包含以下字符:

- 无效的 UTF-8 字符
- 除换行和制表符之外的控制字符

.. _secureheaders:

SecureHeaders
=============

此过滤器添加 HTTP 响应头,你的应用程序可以使用它们来提高应用程序的安全性。

如果要自定义头,请扩展 ``CodeIgniter\Filters\SecureHeaders`` 并覆盖 ``$headers`` 属性。并在 **app/Config/Filters.php** 中更改 ``$aliases`` 属性:

.. literalinclude:: filters/011.php

如果你想了解安全头,请参阅 `OWASP 安全头项目 <https://owasp.org/www-project-secure-headers/>`_。
