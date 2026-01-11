##################
控制器过滤器
##################

.. contents::
    :local:
    :depth: 3

控制器过滤器允许你在控制器执行之前或之后执行操作。与 :doc:`事件 <../extending/events>` 不同，你可以选择过滤器将应用于哪些特定的 URI 或路由。前置过滤器可以修改请求（Request），而后置过滤器可以对响应（Response）进行操作甚至修改它，从而提供了极大的灵活性和控制力。

使用过滤器执行的常见任务示例包括：

* 对传入请求实施 CSRF 保护
* 根据角色限制网站的访问区域
* 对特定端点执行速率限制
* 显示"维护中"页面
* 执行自动内容协商
* 等等...

*****************
创建过滤器
*****************

过滤器是实现 ``CodeIgniter\Filters\FilterInterface`` 的简单类。
它们包含两个方法：``before()`` 和 ``after()``，分别存放控制器执行前和执行后运行的代码。
类必须包含这两个方法，但如果不需要，可以让方法保持为空。过滤器类的基本结构如下：

.. literalinclude:: filters/001.php

前置过滤器
==============

替换请求
-----------------

从任何过滤器中，你可以返回 ``$request`` 对象，它将替换当前请求，允许你进行修改，
这些修改在控制器执行时仍然存在。

停止后续过滤器
----------------------

此外，当你有多个过滤器时，你可能还希望在某个过滤器之后停止后续过滤器的执行。
这可以通过返回 **任何非空** 结果轻松实现。如果前置过滤器返回空结果，
控制器操作或后续过滤器仍将执行。

非空结果规则的一个例外是 ``Request`` 实例。
在前置过滤器中返回它不会停止执行，只会替换当前的 ``$request`` 对象。

返回响应
------------------

由于前置过滤器在控制器执行之前执行，有时你可能希望阻止控制器中的操作发生。

这通常用于执行重定向，如以下示例：

.. literalinclude:: filters/002.php

如果返回了 ``Response`` 实例，响应将被发送回客户端，脚本执行将停止。
这对于为 API 实现速率限制很有用。详见 :doc:`Throttler <../libraries/throttler>` 的示例。

.. _after-filters:

后置过滤器
=============

后置过滤器与前置过滤器几乎相同，不同之处在于你只能返回 ``$response`` 对象，
并且无法停止脚本执行。这确实允许你修改最终输出，或简单地处理最终输出。
这可用于确保以正确方式设置某些安全头，或缓存最终输出，
甚至使用敏感词过滤器过滤最终输出。

*******************
配置过滤器
*******************

在过滤器运行时有两种配置方式。一种在 **app/Config/Filters.php** 中完成，另一种在 **app/Config/Routes.php** 中完成。

如果你想为定义的路由指定过滤器，请使用 **app/Config/Routes.php** 并参考 :ref:`URI 路由 <applying-filters>`。

.. note:: 应用过滤器的最安全方法是 :ref:`禁用自动路由 <use-defined-routes-only>`，并 :ref:`将过滤器设置到路由 <applying-filters>`。

app/Config/Filters.php
======================

**app/Config/Filters.php** 文件包含四个属性，允许你准确配置过滤器何时运行。

.. warning:: 建议在过滤器设置中的 URI 末尾始终添加 ``*``。
    因为控制器方法可能通过你未预料到的其他 URL 访问。
    例如，当 :ref:`auto-routing-legacy` 启用时，若存在 ``Blog::index()``，
    它可以通过 ``blog``、``blog/index`` 和 ``blog/index/1`` 等方式访问。

.. _filters-aliases:

$aliases
--------

``$aliases`` 数组用于将一个简单的名称与一个或多个完整的过滤器类名关联起来：

.. literalinclude:: filters/003.php

别名是强制性的，如果你稍后尝试使用完整的类名，系统将抛出错误。

以这种方式定义别名使得切换使用的类变得简单。例如，当你决定更改为不同的身份验证系统时，只需更改过滤器的类即可，非常方便。

你可以将多个过滤器组合成一个别名，从而轻松应用复杂的过滤器集：

.. literalinclude:: filters/004.php

你可以根据需要定义任意数量的别名。

.. _filters-required:

$required
---------

.. versionadded:: 4.5.0

第二个部分允许你定义 **必选过滤器**。
这是特殊的过滤器，应用于框架处理的每一个请求。它们在其他类型的过滤器之前和之后应用，
这些过滤器将在下面解释。

.. note:: 必选过滤器始终会被执行。但是，如果路由不存在，则仅执行前置过滤器。

你应该注意在这里使用的过滤器数量，因为在每个请求上运行太多过滤器可能会对性能产生影响。但是默认设置的过滤器提供了框架功能。如果移除，这些功能将不再工作。详见 :ref:`provided-filters`。

通过将别名添加到 ``before`` 或 ``after`` 数组来指定过滤器：

.. literalinclude:: filters/013.php

.. _filters-globals:

$globals
--------

第三部分用于定义应用于所有有效请求的全局过滤器。

你应该注意在这里使用的过滤器数量，因为在每个请求上运行太多过滤器可能会对性能产生影响。

通过将别名添加到 ``before`` 或 ``after`` 数组来指定过滤器：

.. literalinclude:: filters/005.php

排除特定 URI
^^^^^^^^^^^^^^^^^^^^^

有些时候，你希望将过滤器应用于几乎所有请求，但有少数请求需要排除在外。一个常见的例子是，如果你需要从 CSRF 保护过滤器中排除几个 URI，以允许来自第三方网站的请求访问一个或两个特定的 URI，同时保持其余部分的保护。

要做到这一点，请添加一个带有 ``except`` 键的数组，并将要匹配的 URI 路径（相对于 BaseURL）作为值与别名放在一起：

.. literalinclude:: filters/006.php

.. warning:: 在 v4.4.7 之前，由于一个 bug，过滤器处理的 URI 路径未进行 URL 解码。换句话说，路由中指定的 URI 路径和过滤器中指定的 URI 路径可能不同。详见 :ref:`upgrade-447-filter-paths`。

在过滤器设置中任何可以使用 URI 路径（相对于 BaseURL）的地方，你都可以使用正则表达式，或者像上面的例子一样，使用星号 (``*``) 作为通配符以匹配之后的所有字符。在这个例子中，任何以 ``api/`` 开头的 URI 路径都将免受 CSRF 保护，但网站的表单都将受到保护。

如果你需要指定多个 URI 路径，可以使用 URI 路径模式数组：

.. literalinclude:: filters/007.php

$methods
--------

.. warning:: 如果你使用 ``$methods`` 过滤器，你应该 :ref:`禁用自动路由（传统版） <use-defined-routes-only>`，因为 :ref:`auto-routing-legacy` 允许任何 HTTP 方法访问控制器。使用你不期望的方法访问控制器可能会绕过过滤器。

你可以将过滤器应用于某个 HTTP 方法的所有请求，如 ``POST``、``GET``、``PUT`` 等。
它的值应该是一个要运行的过滤器数组：

.. literalinclude:: filters/008.php

.. note:: 与 ``$globals`` 或 ``$filters`` 属性不同，这些只作为前置过滤器运行。

除了标准的 HTTP 方法外，这里还支持一种特殊情况：``CLI``。``CLI``` 方法将应用于所有从命令行运行的请求。

.. note:: 在 v4.5.0 之前，由于一个 bug，你需要以 **小写** 指定 HTTP 方法名称。

$filters
--------

此属性是一个过滤器别名数组。对于每个别名，你可以指定 ``before`` 和 ``after`` 数组，其中包含该过滤器应应用的 URI 路径（相对于 BaseURL）模式列表：

.. literalinclude:: filters/009.php

.. warning:: 在 v4.4.7 之前，由于一个 bug，过滤器处理的 URI 路径未进行 URL 解码。换句话说，路由中指定的 URI 路径和过滤器中指定的 URI 路径可能不同。详见 :ref:`upgrade-447-filter-paths`。

.. _filters-filters-filter-arguments:

过滤器参数
^^^^^^^^^^^^^^^^

.. versionadded:: 4.4.0

配置 ``$filters`` 时，可以将额外的参数传递给过滤器：

.. literalinclude:: filters/012.php

在这个例子中，当 URI 匹配 ``admin/*`` 时，数组 ``['admin', 'superadmin']`` 将作为 ``$arguments`` 传递给 ``group`` 过滤器的 ``before()`` 方法。
当 URI 匹配 ``admin/users/*`` 时，数组 ``['users.manage']`` 将作为 ``$arguments`` 传递给 ``permission`` 过滤器的 ``before()`` 方法。

.. note:: 在 v4.6.0 之前，同一个过滤器不能使用不同的参数运行多次。

.. _filter-execution-order:

过滤器执行顺序
======================

.. important:: 从 v4.5.0 开始，过滤器的执行顺序已更改。如果你希望保持与以前版本相同的执行顺序，必须将 ``Config\Feature::$oldFilterOrder`` 设置为 ``true``。

过滤器按以下顺序执行：

- **前置过滤器**：required（必选） → globals（全局） → methods（方法） → filters（特定） → route（路由）
- **后置过滤器**：route（路由） → filters（特定） → globals（全局） → required（必选）

.. note:: *必选（required）* 过滤器自 v4.5.0 起可以使用。

.. note:: 在 v4.5.0 版本之前，指定给路由的过滤器（位于 **app/Config/Routes.php**）会先于 **app/Config/Filters.php** 中指定的过滤器执行。此外，路由过滤器与 Filters 配置中的后置过滤器执行顺序此前并未反转。详见 :ref:`升级指南 <upgrade-450-filter-execution-order>`。

******************
验证过滤器配置
******************

CodeIgniter 提供了以下 :doc:`命令 <../cli/spark_commands>` 来检查路由的过滤器。

.. _spark-filter-check:

filter:check
============

.. versionadded:: 4.3.0

例如，检查 **GET** 方法下路由 ``/`` 的过滤器：

.. code-block:: console

    php spark filter:check get /

输出如下：

.. code-block:: none

    +--------+-------+----------------------+-------------------------------+
    | Method | Route | Before Filters       | After Filters                 |
    +--------+-------+----------------------+-------------------------------+
    | GET    | /     | forcehttps pagecache | pagecache performance toolbar |
    +--------+-------+----------------------+-------------------------------+

    Before Filter Classes:
    CodeIgniter\Filters\ForceHTTPS → CodeIgniter\Filters\PageCache
    After Filter Classes:
    CodeIgniter\Filters\PageCache → CodeIgniter\Filters\PerformanceMetrics → CodeIgniter\Filters\DebugToolbar

.. note:: 自 v4.6.0 起，过滤器参数已显示在输出表中。此外，实际的过滤器类名已显示在末尾。

你也可以通过 ``spark routes`` 命令查看路由和过滤器，但当你对路由使用正则表达式时，它可能无法显示准确的过滤器。详见 :ref:`URI 路由 <routing-spark-routes>`。

.. _provided-filters:

****************
内置过滤器
****************

CodeIgniter4 内置以下过滤器：

- ``cors`` => :doc:`../libraries/cors`
- ``csrf`` => :ref:`CSRF <cross-site-request-forgery>`
- ``toolbar`` => :ref:`DebugToolbar <the-debug-toolbar>`
- ``honeypot`` => :doc:`Honeypot <../libraries/honeypot>`
- ``invalidchars`` => :ref:`invalidchars`
- ``secureheaders`` => :ref:`secureheaders`
- ``forcehttps`` => :ref:`forcehttps`
- ``pagecache`` => :doc:`PageCache <../general/caching>`
- ``performance`` => :ref:`performancemetrics`

.. note:: 过滤器按照配置文件中定义的顺序执行。但是，如果启用了 ``DebugToolbar``，它总是最后执行，以便捕获其他过滤器的所有操作。

.. _forcehttps:

ForceHTTPS
==========

.. versionadded:: 4.5.0

此过滤器提供"强制全局安全请求"功能。

如果你将 ``Config\App:$forceGlobalSecureRequests`` 设置为 true，所有请求必须通过 HTTPS 连接。如果传入的请求不安全，用户将被重定向到页面的安全版本，并设置 HTTP 严格传输安全 (HSTS) 标头。

.. _performancemetrics:

PerformanceMetrics
==================

.. versionadded:: 4.5.0

此过滤器提供性能指标的伪变量。

如果你想显示从 CodeIgniter 启动那一刻到最终输出发送到浏览器之前的总耗时，只需在视图中放置这个伪变量::

    {elapsed_time}

如果你想在视图文件中显示内存使用情况，请使用此伪变量::

    {memory_usage}

如果你不需要此功能，请从 ``$required['after']`` 中移除 ``'performance'``。

.. _invalidchars:

InvalidChars
=============

此过滤器禁止用户输入数据（``$_GET``、``$_POST``、``$_COOKIE``、``php://input``）包含以下字符：

- 无效的 UTF-8 字符
- 除换行符和制表符之外的控制字符

.. _secureheaders:

SecureHeaders
=============

此过滤器添加 HTTP 响应标头，你的应用程序可以使用这些标头来提高安全性。

如果你想自定义标头，请继承 ``CodeIgniter\Filters\SecureHeaders`` 并覆盖 ``$headers`` 属性。然后在 **app/Config/Filters.php** 中更改 ``$aliases`` 属性：

.. literalinclude:: filters/011.php

如果你想了解有关安全标头的信息，请参阅 `OWASP Secure Headers Project <https://owasp.org/www-project-secure-headers/>`_。
