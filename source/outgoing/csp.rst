.. _content-security-policy:

#######################
内容安全策略
#######################

.. contents::
    :local:
    :depth: 2

********************************
什么是内容安全策略？
********************************

防御 XSS 攻击的最佳手段之一是在网站中实施内容安全策略（CSP）。为此需要明确授权 HTML 中包含的各类资源，如图片、样式表和 JavaScript 文件等内容源。浏览器将自动拦截未经明确批准的来源内容。此类授权规则通过响应中的 ``Content-Security-Policy`` 标头进行定义，并提供多种配置选项。

这听起来很复杂，在某些网站上确实如此。但对于许多内容均由同一域名（如 **http://example.com**）提供的简单站点而言，集成 CSP 非常容易。

由于这是一个复杂的主题，本用户指南不会展开所有细节。如需深入了解，建议访问以下站点：

* `内容安全策略主站 <https://content-security-policy.com/>`_
* `W3C 规范 <https://www.w3.org/TR/CSP>`_
* `HTML5Rocks 的介绍 <https://www.html5rocks.com/en/tutorials/security/content-security-policy/>`_
* `SitePoint 的文章 <https://www.sitepoint.com/improving-web-security-with-the-content-security-policy/>`_

**************
启用 CSP
**************

.. important:: :ref:`调试工具栏 <the-debug-toolbar>` 可能会使用 Kint，后者会输出内联脚本。因此，启用 CSP 后，系统会自动为调试工具栏输出 CSP nonce。但如果未使用 CSP nonce，CSP 标头会变为非预期内容，且行为与生产环境不同；如需验证 CSP 行为，请关闭调试工具栏。

默认情况下，CSP 支持处于关闭状态。要在应用中启用该支持，请编辑 **app/Config/App.php** 中的 ``CSPEnabled`` 值：

.. literalinclude:: csp/011.php

启用后，响应对象将包含 ``CodeIgniter\HTTP\ContentSecurityPolicy`` 实例。系统会将 **app/Config/ContentSecurityPolicy.php** 中的配置值应用到该实例；若运行时无需修改，发送格式正确的响应头后即可完成操作。

启用 CSP 后，HTTP 响应中会添加两行标头：一行是 **Content-Security-Policy** 标头，包含明确允许的内容类型或来源策略；另一行是 **Content-Security-Policy-Report-Only** 标头，用于指定允许的内容类型或来源，并将触发规则的情况上报至指定的目的地。

本实现提供了一种默认处理方式，可通过 ``reportOnly()`` 方法进行更改。如下所示，向 CSP 指令添加新条目时，该条目会被添加到对应的拦截型或防御型 CSP 标头中。在调用添加方法时，通过提供可选的第二个参数，即可针对单次调用覆盖此默认行为。

*********************
运行时配置
*********************

如果应用需要在运行时进行更改，可在控制器中通过 ``$this->response->getCSP()`` 访问该实例。

该类包含多个方法，与需要设置的标头值一一对应。下面展示了不同的参数组合示例，所有方法均接受指令名或指令名数组作为参数：

.. literalinclude:: csp/012.php

各个 "add" 方法的第一个参数为适当的字符串值，或其数组。

仅报告
===========

``reportOnly()`` 方法用于指定后续来源的默认报告处理方式，除非另行覆盖。

例如，可以指定允许 youtube.com，然后提供多个允许但会被报告的来源：

.. literalinclude:: csp/013.php

上报指令
====================

若要指定报告发送的 URL，可使用 ``setReportURI()`` 方法。

.. versionadded:: 4.7.0

CSP Level 3 弃用了 ``report-uri`` 指令，转而推荐使用 ``report-to``。因此，可使用 ``setReportToEndpoint()`` 方法为 CSP 报告设置上报地址。在添加此指令前，请确保已通过 ``addReportingEndpoints()`` 方法定义了上报地址。

.. literalinclude:: csp/015.php

为向后兼容不支持 ``report-to`` 指令的浏览器，在使用 ``setReportToEndpoint()`` 方法时，CodeIgniter4 也会自动设置 ``report-uri`` 指令。

.. _csp-clear-directives:

清除指令
================

如需清除现有 CSP 指令，可使用 ``clearDirective()`` 方法：

.. literalinclude:: csp/014.php

**************
内联内容
**************

网站页面可能因包含用户生成的内容，导致内联脚本和样式未能获得有效保护。为此，CSP 允许在 ``<style>`` 和 ``<script>`` 标签中指定 nonce（随机数），并将这些值添加到响应头中。

使用占位符
==================

在实际开发中，手动处理这些随机数非常繁琐，而采用动态生成的方式安全性最高。为简化操作，只需在标签中加入 ``{csp-style-nonce}`` 或 ``{csp-script-nonce}`` 占位符，系统便会自动完成转换::

    // 原始代码
    <script {csp-script-nonce}>
        console.log("由于不包含 nonce 属性，此脚本将无法运行");
    </script>

    // 转换后
    <script nonce="Eskdikejidojdk978Ad8jf">
        console.log("由于不包含 nonce 属性，此脚本将无法运行");
    </script>

    // 或者
    <style {csp-style-nonce}>
        . . .
    </style>

.. warning:: 若攻击者注入了类似 ``<script {csp-script-nonce}>`` 的字符串，此功能可能会将其转换为真实的 nonce 属性。为规避风险，可通过 **app/Config/ContentSecurityPolicy.php** 中的 ``$scriptNonceTag`` 和 ``$styleNonceTag`` 属性自定义占位符字符串。

.. _csp-using-functions:

使用函数
===============

若不希望使用上述自动替换功能，可将 **app/Config/ContentSecurityPolicy.php** 中的 ``$autoNonce`` 设置为 ``false``。

此时，可改用 :php:func:`csp_script_nonce()` 和 :php:func:`csp_style_nonce()` 函数::

    // 原始代码
    <script <?= csp_script_nonce() ?>>
        console.log("由于不包含 nonce 属性，此脚本将无法运行");
    </script>

    // 转换后
    <script nonce="Eskdikejidojdk978Ad8jf">
        console.log("由于不包含 nonce 属性，此脚本将无法运行");
    </script>

    // 或者
    <style <?= csp_style_nonce() ?>>
        . . .
    </style>
