##########################
处理 HTTP 请求
##########################

为了充分利用 CodeIgniter，你需要对 HTTP 请求和响应的工作原理有基本的了解。由于在开发 Web 应用程序时，你所处理的正是这些内容，因此对于所有希望取得成功的开发者来说，理解 HTTP 背后的概念是**必须**的。

本章的第一部分将进行概述。在了解基本概念之后，我们将讨论如何在 CodeIgniter 中处理请求和响应。

.. contents::
    :local:
    :depth: 2

什么是 HTTP？
*************

HTTP 只是一种基于文本的约定，它允许两台机器相互通信。当浏览器请求一个页面时，它会询问服务器是否可以获取该页面。服务器随后准备页面，并将响应发送回请求它的浏览器。基本上就是这样。显然，其中存在一些你可以利用的复杂性，但基本原理其实相当简单。

HTTP 是用于描述这种交换约定的术语，其全称为超文本传输协议（HyperText Transfer Protocol）。你在开发 Web 应用时的目标，是始终了解浏览器正在请求什么，并能够做出适当的响应。

请求
===========

每当客户端（如 Web 浏览器、智能手机应用等）发出请求时，它都会向服务器发送一条小的文本消息，然后等待响应。

该请求可能看起来像这样::

    GET / HTTP/1.1
    Host codeigniter.com
    Accept: text/html
    User-Agent: Chrome/46.0.2490.80

此消息显示了，了解客户端请求所需的所有信息。它告诉了请求的方法（GET、POST、DELETE 等）以及其支持的 HTTP 版本。

请求还包含许多可选的请求头，其中可以包含各种信息，例如客户端希望内容以何种语言显示、客户端接受的格式类型等等。如果你想了解更多信息，Wikipedia 上有一篇文章列出了所有 `请求头字段 <https://en.wikipedia.org/wiki/List_of_HTTP_header_fields>`_。

响应
============

一旦服务器收到请求，你的应用程序就会利用这些信息生成一些输出。服务器会将你的输出打包，作为对客户端响应的一部分。这也被表示为一条简单的文本消息，可能看起来像这样::

    HTTP/1.1 200 OK
    Server: nginx/1.8.0
    Date: Thu, 05 Nov 2015 05:33:22 GMT
    Content-Type: text/html; charset=UTF-8

    <html>
        . . .
    </html>

响应会告诉客户端它正在使用哪个版本的 HTTP 规范，而其中最重要的是状态码（200）。状态码是经过标准化的一系列代码，对客户端具有特定的含义。它可以告诉客户端请求成功了（200），或页面未找到（404）。你可以前往 IANA 查看 `完整的 HTTP 状态码列表 <https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml>`_。

处理请求和响应
***********************************

虽然 PHP 提供了与请求和响应头交互的方式，但像大多数框架一样，CodeIgniter 对它们进行了抽象，为你提供了一个一致且简单的接口。:doc:`IncomingRequest 类 </incoming/incomingrequest>` 是 HTTP 请求的面向对象表示。它为你提供了所需的一切：

.. literalinclude:: http/001.php

请求类在后台为你做了大量工作，你无需为此担心。``isAJAX()`` 和 ``isSecure()`` 方法会检查多种不同的方式来确定正确的答案。

.. note:: ``isAJAX()`` 方法依赖于 ``X-Requested-With`` 头，但在某些情况下，通过 JavaScript 发起的 XHR 请求（例如 fetch）默认不会发送该头。请参阅 :doc:`AJAX 请求 </general/ajax>` 章节，了解如何避免此问题。

CodeIgniter 还提供了一个 :doc:`Response 类 </outgoing/response>`，它是 HTTP 响应的面向对象表示。这为你提供了一种简单而强大的方式来构建对客户端的响应：

.. literalinclude:: http/002.php

此外，Response 类还允许你操作 HTTP 缓存层，以获得最佳性能。
