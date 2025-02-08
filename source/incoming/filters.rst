##################
控制器过滤器
##################

.. contents::
    :local:
    :depth: 3

控制器过滤器允许你在控制器执行前后执行特定操作。与 :doc:`事件 <../extending/events>` 不同，你可以选择将过滤器应用于特定的 URI 或路由。前置过滤器可以修改请求（Request），而后置过滤器可以操作甚至修改响应（Response），这为开发者提供了极大的灵活性和控制力。

以下是使用过滤器实现的常见场景示例：

* 对传入请求实施 CSRF 保护
* 根据用户角色限制网站区域访问
* 对特定端点进行速率限制
* 显示「网站维护中」页面
* 执行自动内容协商
* 以及其他更多应用场景...

*****************
创建过滤器
*****************

过滤器是实现了 ``CodeIgniter\Filters\FilterInterface`` 接口的简单类。它们包含两个方法：``before()`` 和 ``after()``，分别用于在控制器执行前后运行代码。你的类必须包含这两个方法，但如果不需要具体实现，可以保持方法体为空。一个基础的过滤器类结构如下：

.. literalinclude:: filters/001.php

前置过滤器
==============

替换请求对象
-----------------
在任何前置过滤器中，你可以返回修改后的 ``$request`` 对象，该对象将替换当前请求，确保控制器执行时使用的是修改后的请求实例。

终止后续过滤器执行
----------------------
当存在多个过滤器时，你可能需要在某个过滤器之后终止后续过滤器的执行。只需返回 **任意非空值** 即可实现。若前置过滤器返回空值，控制器操作及后续过滤器仍会继续执行。

需要注意的是，返回 ``Request`` 实例属于例外情况。在前置过滤器中返回该实例不会终止执行流程，仅会替换当前的 ``$request`` 对象。

返回响应对象
------------------
由于前置过滤器在控制器执行前运行，有时你可能希望阻止控制器的后续操作。这通常用于执行重定向，如下例所示：

.. literalinclude:: filters/002.php

如果返回 ``Response`` 实例，该响应将直接发送至客户端并终止脚本执行。这在实现 API 速率限制时非常有用，具体示例可参考 :doc:`Throttler <../libraries/throttler>` 库文档。

.. _after-filters:

后置过滤器
=============

后置过滤器与前置过滤器类似，但只能返回 ``$response`` 对象且无法终止脚本执行。这允许你修改最终输出内容或对其进行后续处理，例如确保安全头正确设置、缓存最终输出或实施敏感词过滤等。

*******************
配置过滤器
*******************

有两种方式配置过滤器的执行时机：一种在 **app/Config/Filters.php** 中配置，另一种在 **app/Config/Routes.php** 中配置。若需为定义的路由指定过滤器，请使用 **app/Config/Routes.php** 并参考 :ref:`URI 路由 <applying-filters>` 章节。

.. note:: 最安全的过滤器应用方式是 :ref:`禁用自动路由 <use-defined-routes-only>` 并 :ref:`为路由设置过滤器 <applying-filters>`。

app/Config/Filters.php
======================

**app/Config/Filters.php** 文件包含四个属性，用于精确控制过滤器的执行时机。

.. warning:: 建议在过滤器设置的 URI 末尾始终添加 ``*`` 通配符。因为控制器方法可能通过你未预料到的其他 URL 访问。例如，当启用 :ref:`传统自动路由 <auto-routing-legacy>` 时，若存在 ``Blog::index()`` 方法，可通过 ``blog``、``blog/index`` 和 ``blog/index/1`` 等路径访问。

.. _filters-aliases:

$aliases
--------
``$aliases`` 数组用于将一个简短的别名与一个或多个完整的过滤器类名关联：

.. literalinclude:: filters/003.php

别名是强制性的，若尝试直接使用完整类名，系统将抛出错误。

这种定义方式便于后续更换过滤器类（例如切换认证系统时），只需修改别名对应的类即可完成迁移。

你还可以将多个过滤器组合到一个别名下，简化复杂过滤器集的配置：

.. literalinclude:: filters/004.php

根据需求定义任意数量的别名。

.. _filters-required:

$required
---------

.. versionadded:: 4.5.0

第二部分用于定义 **必选过滤器**。这些特殊过滤器会应用于框架处理的每个请求，且在其他类型过滤器之前和之后执行。

.. note:: 必选过滤器始终执行。但如果路由不存在，仅会执行前置过滤器。

需谨慎设置此处过滤器的数量，过多会影响请求处理性能。默认提供的必选过滤器支撑框架核心功能，移除可能导致相关功能失效。详见 :ref:`provided-filters`。

通过将别名添加至 ``before`` 或 ``after`` 数组来指定必选过滤器：

.. literalinclude:: filters/013.php

.. _filters-globals:

$globals
--------

第三部分用于定义应用于所有有效请求的全局过滤器。需注意过滤器数量对性能的影响。

通过将别名添加至 ``before`` 或 ``after`` 数组来指定全局过滤器：

.. literalinclude:: filters/005.php

排除特定 URI
^^^^^^^^^^^^^^^^^^^^^

有时需要对绝大多数请求应用过滤器，但排除少数例外。例如在 CSRF 保护中排除第三方网站可访问的特定 URI。

在别名旁添加包含 ``except`` 键和 URI 路径（相对于 BaseURL）的数组实现：

.. literalinclude:: filters/006.php

.. warning:: 在 v4.4.7 之前，由于漏洞，过滤器处理的 URI 路径未进行 URL 解码。即路由中的 URI 路径与过滤器配置的路径可能不一致。详见 :ref:`upgrade-447-filter-paths`。

在过滤器设置中，可使用正则表达式或通配符（``*``）匹配 URI 路径。上例中，所有以 ``api/`` 开头的路径将豁免 CSRF 保护。

如需指定多个路径，可使用路径模式数组：

.. literalinclude:: filters/007.php

$methods
--------

.. warning:: 若使用 ``$methods`` 过滤器，应 :ref:`禁用传统自动路由 <use-defined-routes-only>`，因为 :ref:`传统自动路由 <auto-routing-legacy>` 允许通过任意 HTTP 方法访问控制器，可能导致过滤器被绕过。

可为特定 HTTP 方法（如 POST、GET、PUT 等）的所有请求应用过滤器。其值为要运行的过滤器数组：

.. literalinclude:: filters/008.php

.. note:: 与 ``$globals`` 或 ``$filters`` 不同，这些过滤器仅作为前置过滤器运行。

除标准 HTTP 方法外，还支持特殊值 ``CLI``，该值应用于所有命令行请求。

.. note:: v4.5.0 之前版本需使用 **小写** 指定 HTTP 方法名称。

$filters
--------

该属性是过滤器别名数组。每个别名可指定 ``before`` 和 ``after`` 数组，包含过滤器应应用的 URI 路径模式（相对于 BaseURL）：

.. literalinclude:: filters/009.php

.. warning:: 在 v4.4.7 之前，由于漏洞，过滤器处理的 URI 路径未进行 URL 解码。详见 :ref:`upgrade-447-filter-paths`。

.. _filters-filters-filter-arguments:

过滤器参数
^^^^^^^^^^^^^^^^

.. versionadded:: 4.4.0

配置 ``$filters`` 时，可向过滤器传递额外参数：

.. literalinclude:: filters/012.php

本例中，当 URI 匹配 ``admin/*`` 时，数组 ``['admin', 'superadmin']`` 将作为 ``$arguments`` 传递给 ``group`` 过滤器的 ``before()`` 方法；当匹配 ``admin/users/*`` 时，数组 ``['users.manage']`` 将传递给 ``permission`` 过滤器的 ``before()`` 方法。

.. note:: v4.6.0 之前版本，同一过滤器无法使用不同参数多次运行。

.. _filter-execution-order:

过滤器执行顺序
================

.. important:: 自 v4.5.0 起，过滤器执行顺序已变更。如需保持旧版顺序，请将 ``Config\Feature::$oldFilterOrder`` 设为 ``true``。

过滤器按以下顺序执行：

- **前置过滤器**：必选 → 全局 → 方法 → 过滤器 → 路由
- **后置过滤器**：路由 → 过滤器 → 全局 → 必选

.. note:: *必选* 过滤器自 v4.5.0 起可用。

.. note:: v4.5.0 之前版本，路由过滤器（在 **app/Config/Routes.php** 中定义）优先于 **app/Config/Filters.php** 中的过滤器执行，且后置过滤器的执行顺序未反转。详见 :ref:`升级指南 <upgrade-450-filter-execution-order>`。

******************
验证过滤器配置
******************

CodeIgniter 提供以下 :doc:`命令 <../cli/spark_commands>` 用于检查路由的过滤器配置。

.. _spark-filter-check:

filter:check
============
.. versionadded:: 4.3.0

示例：检查 ``/`` 路由的 GET 方法过滤器配置：

.. code-block:: console

    php spark filter:check get /

输出结果如下：

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

.. note:: 自 v4.6.0 起，输出表格中会显示过滤器参数，并展示实际使用的过滤器类名。

也可通过 ``spark routes`` 命令查看路由和过滤器，但使用正则表达式定义路由时可能显示不准确。详见 :ref:`URI 路由 <routing-spark-routes>`。

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
- ``pagecache`` => :doc:`页面缓存 <../general/caching>`
- ``performance`` => :ref:`performancemetrics`

.. note:: 过滤器按配置文件中的顺序执行。但若启用，``DebugToolbar`` 始终最后执行，以便捕获其他过滤器的所有操作。

.. _forcehttps:

ForceHTTPS
==========

.. versionadded:: 4.5.0

该过滤器提供「强制全局安全请求」功能。若设置 ``Config\App:$forceGlobalSecureRequests`` 为 true，所有请求必须通过 HTTPS 连接。若请求不安全，用户将被重定向至安全页面，并设置 HSTS 头。

.. _performancemetrics:

PerformanceMetrics
==================

.. versionadded:: 4.5.0

该过滤器提供性能指标伪变量。若需在视图中显示从框架启动到输出生成的总耗时，使用::

    {elapsed_time}

显示内存使用量则使用::

    {memory_usage}

若不需要此功能，从 ``$required['after']`` 中移除 ``'performance'``。

.. _invalidchars:

InvalidChars
=============

该过滤器禁止用户输入数据（``$_GET``、``$_POST``、``$_COOKIE``、``php://input``）包含以下字符：

- 无效 UTF-8 字符
- 除换行符和制表符外的控制字符

.. _secureheaders:

SecureHeaders
=============

该过滤器添加增强应用安全性的 HTTP 响应头。如需自定义头信息，可继承 ``CodeIgniter\Filters\SecureHeaders`` 并覆盖 ``$headers`` 属性，然后在 **app/Config/Filters.php** 中修改 ``$aliases``：

.. literalinclude:: filters/011.php

有关安全头的详细信息，请参考 `OWASP 安全头项目 <https://owasp.org/www-project-secure-headers/>`_。
