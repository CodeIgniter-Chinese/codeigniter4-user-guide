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

你可以采取的最好的防范 XSS 攻击的措施之一就是在网站上实施内容安全策略（CSP）。这要求你指定并授权在你的网站 HTML 中包含的每一个内容源，包括图片、样式表、JavaScript 文件等等。浏览器会拒绝来自未明确授权的源的内容。这个授权在响应的 ``Content-Security-Policy`` 头部中定义，并提供了各种配置选项。

这听起来很复杂，在某些网站上，确实可以是一项挑战。但是，对于许多简单的网站，其中所有的内容都由同一个域名（比如，**http://example.com**）提供，集成起来非常简单。

由于这是一个复杂的主题，这个用户指南不会详细介绍所有的细节。更多信息，你应该访问以下网站：

* `内容安全策略主站 <https://content-security-policy.com/>`_
* `W3C 规范 <https://www.w3.org/TR/CSP>`_
* `HTML5Rocks 的介绍 <https://www.html5rocks.com/en/tutorials/security/content-security-policy/>`_
* `SitePoint 的文章 <https://www.sitepoint.com/improving-web-security-with-the-content-security-policy/>`_

**************
开启 CSP
**************

.. important:: :ref:`Debug Toolbar <the-debug-toolbar>` 可能会使用 Kint，它会输出内联脚本。因此，当 CSP 开启时，CSP nonce 会自动为 Debug Toolbar 输出。然而，如果你没有使用 CSP nonce，这将会改变你并未打算的 CSP 头部，它的行为将会与生产环境中的不同；如果你想验证 CSP 的行为，关闭 Debug Toolbar。

默认情况下，这项支持是关闭的。要在你的应用程序中启用支持，编辑 **app/Config/App.php** 中的 ``CSPEnabled`` 值：

.. literalinclude:: csp/011.php

当启用时，响应对象会包含一个 ``CodeIgniter\HTTP\ContentSecurityPolicy`` 的实例。**app/Config/ContentSecurityPolicy.php** 中设定的值会被应用到这个实例，如果在运行时不需要任何改变，那么正确格式化的头部就会被发送，你就完成了所有的工作。

在启用 CSP 后，两行头部行会被添加到 HTTP 响应：一个 **Content-Security-Policy** 头部，它的策略明确允许不同上下文的内容类型或源，和一个 **Content-Security-Policy-Report-Only** 头部，它识别将被允许但也会被报告给你选择的目标的内容类型或源。

我们的实现提供了一个默认的处理方法，可以通过 ``reportOnly()`` 方法进行更改。当一个额外的条目被添加到 CSP 指令，如下所示，它将被添加到适当的 CSP 头部以进行阻止或预防。这可以在每次调用的基础上被覆盖，通过向添加方法调用提供一个可选的第二个参数。

*********************
运行时配置
*********************

如果你的应用程序需要在运行时进行更改，你可以在你的控制器中通过 ``$this->response->getCSP()`` 访问实例。

这个类包含了一些方法，这些方法与你需要设置的适当的头部值相当明显的映射。下面展示了一些例子，它们有不同的参数组合，尽管所有的都接受一个指令名或者它们的数组：

.. literalinclude:: csp/012.php

每个 "add" 方法的第一个参数是一个适当的字符串值，或者是它们的数组。

仅报告
=======

``reportOnly()`` 方法允许你为后续的资源指定默认的报告处理方式，除非被覆盖。

例如，你可以指定 youtube.com 被允许，然后提供几个允许但需要报告的资源：

.. literalinclude:: csp/013.php

.. _csp-clear-directives:

清除指令
========

如果你想清除现有的 CSP 指令，可以使用 ``clearDirective()`` 方法：

.. literalinclude:: csp/014.php

**************
内联内容
**************

有可能设置一个网站不保护其自身页面上的内联脚本和样式，因为这可能是用户生成内容的结果。为了防止这种情况，CSP 允许你在 ``<style>`` 和 ``<script>`` 标签中指定一个 nonce，并将这些值添加到响应的头部。

使用占位符
==================

这在现实生活中是很痛苦的，当它在飞行中生成时最安全。为了简化这个过程，你可以在标签中包含一个 ``{csp-style-nonce}`` 或 ``{csp-script-nonce}`` 占位符，它将自动为你处理::

    // 原始
    <script {csp-script-nonce}>
        console.log("脚本不会运行，因为它不包含 nonce 属性");
    </script>

    // 变为
    <script nonce="Eskdikejidojdk978Ad8jf">
        console.log("脚本不会运行，因为它不包含 nonce 属性");
    </script>

    // 或者
    <style {csp-style-nonce}>
        . . .
    </style>

.. warning:: 如果攻击者注入像 ``<script {csp-script-nonce}>`` 这样的字符串，它可能会因为这个功能而成为真实的 nonce 属性。你可以在 **app/Config/ContentSecurityPolicy.php** 中通过 ``$scriptNonceTag`` 和 ``$styleNonceTag`` 属性自定义占位符字符串。

.. _csp-using-functions:

使用函数
===============

如果你不喜欢上面的自动替换功能，你可以通过在 **app/Config/ContentSecurityPolicy.php** 中设置 ``$autoNonce = false`` 来关闭它。

在这种情况下，你可以使用函数，:php:func:`csp_script_nonce()` 和 :php:func:`csp_style_nonce()`::

    // 原始
    <script <?= csp_script_nonce() ?>>
        console.log("脚本不会运行，因为它不包含 nonce 属性");
    </script>

    // 变为
    <script nonce="Eskdikejidojdk978Ad8jf">
        console.log("脚本不会运行，因为它不包含 nonce 属性");
    </script>

    // 或者
    <style <?= csp_style_nonce() ?>>
        . . .
    </style>
