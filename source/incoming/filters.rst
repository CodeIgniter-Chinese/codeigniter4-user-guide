##################
控制器过滤器
##################

.. contents::
    :local:
    :depth: 2

控制器过滤器允许您在控制器执行之前或之后执行操作。与 :doc:`事件 <../extending/events>` 不同,您可以选择应用过滤器的特定 URI。传入过滤器可以修改请求,而后置过滤器可以操作甚至修改响应,提供了很大的灵活性和能力。使用过滤器可以执行的一些常见任务示例:

* 对传入请求执行 CSRF 保护
* 根据角色限制站点的区域访问
* 对某些端点执行速率限制
* 显示“维护中”页面
* 执行自动内容协商
* 等等...

*****************
创建过滤器
*****************

过滤器是简单的类,实现了 ``CodeIgniter\Filters\FilterInterface``。它们包含两个方法:``before()`` 和 ``after()``,这些方法分别包含在控制器之前和之后运行的代码。您的类必须包含这两个方法,但如果不需要可以留空。过滤器骨架类如下:

.. literalinclude:: filters/001.php

Before 过滤器
==============

替换请求
-----------------

在任何过滤器中,您都可以返回 ``$request`` 对象,它将替换当前的请求,允许您进行更改,这些更改在控制器执行时仍然存在。

停止后续过滤器
----------------------

当您有一系列过滤器时,您可能还希望在某个过滤器后停止后续过滤器的执行。您可以通过返回任何非空结果轻松地实现这一点。如果 before 过滤器返回空结果,仍将执行控制器操作或后续过滤器。

非空结果规则的一个例外是 ``Request`` 实例。在 before 过滤器中返回它不会停止执行,只会替换当前的 ``$request`` 对象。

返回响应
------------------

由于 before 过滤器是在执行控制器之前执行的,所以有时您可能希望停止控制器中的操作。

这通常用于执行重定向,如下面的示例:

.. literalinclude:: filters/002.php

如果返回 ``Response`` 实例,将向客户端发送响应,并停止脚本执行。这对于实现 API 的速率限制很有用。请参见 :doc:`Throttler <../libraries/throttler>` 以获取示例。

.. _after-filters:

After 过滤器
=============

After 过滤器与 Before 过滤器几乎完全相同,只是您只能返回 ``$response`` 对象,并且无法停止脚本执行。这确实允许您修改最终输出,或者只是做一些最终输出的事情。这可以用于确保某些安全头正确设置,缓存最终输出,或者使用禁用词过滤器过滤最终输出。

*******************
配置过滤器
*******************

创建过滤器后,您需要配置它们的运行时机。这是在 **app/Config/Filters.php** 中完成的。该文件包含四个属性,允许您配置过滤器的确切运行时机。

.. note:: 最安全的应用过滤器方法是 :ref:`禁用自动路由 <use-defined-routes-only>`,并 :ref:`设置过滤器到路由 <applying-filters>`。

.. warning:: 建议您在过滤器设置中的 URI 末尾始终添加 ``*``。因为控制器方法可能比您想象的通过不同的 URL 访问。例如,当启用 :ref:`auto-routing-legacy` 时,如果您有 ``Blog::index``,它可以通过 ``blog``、``blog/index`` 和 ``blog/index/1`` 等方式访问。

$aliases
========

``$aliases`` 数组用于将简单名称与一个或多个完全限定的类名相关联,这些类名是要运行的过滤器:

.. literalinclude:: filters/003.php

别名是强制性的,如果您稍后尝试使用完整的类名,系统将抛出错误。以这种方式定义使得切换使用的类变得简单。非常适合当您决定需要更改到不同的身份验证系统时,因为您只需要更改过滤器的类即可完成。

您可以将多个过滤器组合成一个别名,使复杂的过滤器组非常简单:

.. literalinclude:: filters/004.php

您应该根据需要定义尽可能多的别名。

$globals
========

第二部分允许您定义任何应用于框架的每个请求的过滤器。在这里使用太多可能会对性能产生影响,所以要小心。可以通过将别名添加到 before 或 after 数组来指定过滤器:

.. literalinclude:: filters/005.php

除了少数 URI
---------------------

有时您希望将过滤器应用于几乎所有请求,但有一些应该不受影响。一个常见的示例是,如果您需要从 CSRF 保护过滤器中排除几个 URI,以允许第三方网站的请求访问一个或两个特定的 URI,同时保持其余 URI 受保护。要做到这一点,请在别名旁边添加一个包含 ``except`` 键和要匹配的 URI 值的数组:

.. literalinclude:: filters/006.php

在过滤器设置中可以使用 URI 的任何位置,您都可以使用正则表达式,或者像在这个例子中使用星号 (``*``) 作为通配符,匹配之后的所有字符。在这个例子中,任何以 ``api/`` 开头的 URL 都将被免于 CSRF 保护,但网站的表单将全部受保护。如果您需要指定多个 URI,可以使用 URI 模式数组:

.. literalinclude:: filters/007.php

$methods
========

.. warning:: 如果使用 ``$methods`` 过滤器,您应该 :ref:`禁用自动路由(传统) <use-defined-routes-only>`,因为 :ref:`auto-routing-legacy` 允许任何 HTTP 方法访问控制器。以您不期望的方法访问控制器可能会绕过过滤器。

您可以将过滤器应用于所有某种 HTTP 方法的请求,如 POST、GET、PUT 等。在此数组中,您需要以**全小写**指定方法名称。它的值将是要运行的过滤器数组:

.. literalinclude:: filters/008.php

.. note:: 与 ``$globals`` 或 ``$filters`` 属性不同,这些只能作为 before 过滤器运行。

除了标准的 HTTP 方法外,这也支持一个特殊情况:``cli``。``cli`` 方法将应用于所有从命令行运行的请求。

$filters
========

该属性是一个过滤器别名数组。对于每个别名,您可以为 ``before`` 和 ``after`` 数组指定过滤器应该应用到的一系列 URI 模式:

.. literalinclude:: filters/009.php

过滤器参数
================

在配置过滤器时,可以在设置路由时向过滤器传递其他参数:

.. literalinclude:: filters/010.php

在这个例子中,数组 ``['dual', 'noreturn']`` 将在过滤器的 ``before()`` 和 ``after()`` 实现方法的 ``$arguments`` 中传递。

******************
确认过滤器
******************

CodeIgniter 提供了以下 :doc:`命令 <../cli/spark_commands>` 来检查路由的过滤器。

.. _spark-filter-check:

filter:check
============

.. versionadded:: 4.3.0

使用 **GET** 方法检查路由 ``/`` 的过滤器::

    > php spark filter:check get /

输出如下所示:

.. code-block:: none

    +--------+-------+----------------+---------------+
    | Method | Route | Before Filters | After Filters |
    +--------+-------+----------------+---------------+
    | GET    | /     |                | toolbar       |
    +--------+-------+----------------+---------------+

您还可以通过 ``spark routes`` 命令查看路由和过滤器。
参见 :ref:`URI 路由 <routing-spark-routes>`。

****************
提供的过滤器
****************

CodeIgniter4 提供的过滤器有: :doc:`Honeypot <../libraries/honeypot>`、:ref:`CSRF <cross-site-request-forgery>`、``InvalidChars``、``SecureHeaders`` 和 :ref:`DebugToolbar <the-debug-toolbar>`。

.. note:: 过滤器按配置文件中定义的顺序执行。但是,如果启用,``DebugToolbar`` 总是最后执行,因为它应该能够捕获其他过滤器中发生的所有事情。

InvalidChars
=============

此过滤器禁止用户输入数据(``$_GET``、``$_POST``、``$_COOKIE``、``php://input``)包含以下字符:

- 无效的 UTF-8 字符
- 除换行和制表符之外的控制字符

.. _secureheaders:

SecureHeaders
=============

此过滤器添加 HTTP 响应头,您的应用程序可以使用它们来提高应用程序的安全性。

如果要自定义头,请扩展 ``CodeIgniter\Filters\SecureHeaders`` 并覆盖 ``$headers`` 属性。并在 **app/Config/Filters.php** 中更改 ``$aliases`` 属性:

.. literalinclude:: filters/011.php

如果您想了解安全头,请参阅 `OWASP 安全头项目 <https://owasp.org/www-project-secure-headers/>`_。
