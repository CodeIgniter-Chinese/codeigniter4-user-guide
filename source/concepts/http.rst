##########################
处理 HTTP 请求
##########################

为了充分利用 CodeIgniter,你需要对 HTTP 请求和响应的工作原理有基本的了解。由于这是你在开发 Web 应用程序时使用的内容,所以所有想要成功的开发人员都必须了解 HTTP 背后的概念。

本章的第一部分概述了概念。在概念说明清楚之后,我们将讨论在 CodeIgniter 中如何处理请求和响应。

.. contents::
    :local:
    :depth: 2

什么是 HTTP?
*************

HTTP 简单来说就是一种基于文本的约定,允许两台机器互相通信。当浏览器请求一个页面时,它会问服务器是否可以获取该页面。然后服务器准备好页面,并向请求它的浏览器发送响应。基本上就这么简单。显然,你可以使用一些复杂的功能,但基础真的非常简单。

HTTP 是用于描述该交换约定的术语。它代表超文本传输协议(HyperText Transfer Protocol)。你开发 Web 应用程序的目标是始终了解浏览器正在请求什么,并能够做出适当的响应。

请求
===========

每当客户端(Web 浏览器、智能手机应用等)发出请求时,它都会向服务器发送一小段文本消息并等待响应。

请求看起来类似这样::

    GET / HTTP/1.1
    Host codeigniter.com
    Accept: text/html
    User-Agent: Chrome/46.0.2490.80

此消息显示了客户端请求所需的所有信息。它告诉请求的方法(GET、POST、DELETE 等)和它支持的 HTTP 版本。

请求还包括可以包含广泛信息的可选请求头,例如客户端希望以什么语言显示内容,客户端接受的格式类型等等。如果你想查看一下,Wikipedia 有一篇文章列出了 `所有标题字段 <https://en.wikipedia.org/wiki/List_of_HTTP_header_fields>`_。

响应
============

一旦服务器接收到请求,你的应用程序将获取该信息并生成一些输出。服务器将你的输出作为其对客户端的响应的一部分进行打包。这也表示为类似这样的简单文本消息:

::

    HTTP/1.1 200 OK
    Server: nginx/1.8.0
    Date: Thu, 05 Nov 2015 05:33:22 GMT
    Content-Type: text/html; charset=UTF-8

    <html>
        . . .
    </html>

响应告诉客户端它使用的 HTTP 规范版本,可能最重要的是状态码(200)。状态码是对客户端具有非常特定含义的标准化代码之一。这可以告诉它请求成功(200),或者页面未找到(404)。如果你想查看完整的 HTTP 状态码列表,请访问 IANA 的 `完整 HTTP 状态码列表 <https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml>`_。

使用请求和响应
***********************************

虽然 PHP 提供了与请求和响应标头交互的方式,但 CodeIgniter 和大多数框架一样,将它们抽象化,以便为它们提供一致、简单的接口。:doc:`IncomingRequest 类 </incoming/incomingrequest>` 是 HTTP 请求的面向对象表示。它提供了你需要的一切:

.. literalinclude:: http/001.php

请求类会默默地为你完成很多工作,你永远不需要担心。``isAJAX()`` 和 ``isSecure()`` 方法检查了几种不同的方法来确定正确的答案。

.. note:: ``isAJAX()`` 方法依赖于 ``X-Requested-With`` 标头,在某些情况下,这在通过 JavaScript 发出的 XHR 请求中默认不会发送(即 fetch)。请参阅 :doc:`AJAX 请求 </general/ajax>` 部分了解如何避免此问题。

CodeIgniter 还提供了一个 :doc:`Response 类 </outgoing/response>`,它是 HTTP 响应的面向对象表示。这为你构建对客户端的响应提供了一个简单而强大的方式:

.. literalinclude:: http/002.php

此外,Response 类允许你使用 HTTP 缓存层进行工作以获得最佳性能。
