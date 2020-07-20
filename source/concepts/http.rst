##############
处理 HTTP 请求
##############

为了充分地使用 CodeIgniter，你需要对 HTTP 请求和响应的工作方式有基本的了解。因为在开发Web应用时需要处理 HTTP 请求，所以对于所有想要成功的开发者来说，
理解 HTTP 背后的概念是 **必须** 的。

本章的第一部分会给出一些关于 HTTP 的概述，接着我们会讨论怎样用 CodeIgniter 来处理 HTTP 请求与响应。

什么是 HTTP ？
==============

HTTP 是两台计算机相互通信的一种基于文本的协议。当浏览器请求页面时，它会询问服务器是否可以获取该页面。然后，
服务器准备页面并将响应发送回发送请求的浏览器。就是这样简单，也可以说复杂些，但基本就是这样。

HTTP 是用于描述该交换约定的术语。它代表超文本传输协议（Hypertext Transfer Protocol）。开发 web 应用程序时，
你的目标只是了解浏览器的要求，并能够做出适当的响应。

HTTP 请求
-----------

当客户端（浏览器，手机软件等）尝试发送 HTTP 请求时，客户端会向服务器发出一条文本消息然后等待响应。

这条文本消息会像这样： ::

	GET / HTTP/1.1
	Host codeigniter.com
	Accept: text/html
	User-Agent: Chrome/46.0.2490.80

这条消息包含了所有服务器可能需要的信息。比如它请求的 method（GET，POST，DELETE 等）、它所支持的 HTTP 版本。

该请求还包括许多可选的请求头字段，这些头字段可以包含各种信息，例如客户端希望内容显示为哪种语言，
客户端接受的格式类型等等。 Wikipedia 上有一篇文章，列出了 `所有的请求头字段
<https://en.wikipedia.org/wiki/List_of_HTTP_header_fields>`_ （译者注：国内用户如果无法访问的话，
可以查看 `在MDN上的页面 <https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers>`_ ）。

HTTP 响应
------------

服务器收到请求后，你的 web 应用程序会处理这条信息然后输出一些响应结果。服务器会将你的响应结果打包为对
客户端的的你的响应结果打包为对客户端的响应的一部分。服务器对客户端的响应消息看起来会像这样： ::

	HTTP/1.1 200 OK
	Server: nginx/1.8.0
	Date: Thu, 05 Nov 2015 05:33:22 GMT
	Content-Type: text/html; charset=UTF-8

	<html>
		. . .
	</html>

响应消息告诉客户端服务器正在使用的 HTTP 版本规范，以及响应状态码（200）。状态码是标准化的对客户端具有非常特定
含义的代码。它可以告诉客户端响应成功（200），或者找不到页面（404）等等。 在 IANA 可以找到 
`完整的响应状态码列表 <https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml>`_ 。

对 HTTP 请求和响应的处理
-----------------------------------

虽然 PHP 提供了与 HTTP 请求和响应进行交互的原生方式，但 CodeIgniter 像大多数框架一样，将它们抽象化，让你拥有一个
一致、简单的接口。:doc:`IncomingRequest 类 </incoming/incomingrequest>` 类是 HTTP 请求的面向对象的表示形式。
它提供你所需要的一切： ::

	use CodeIgniter\HTTP\IncomingRequest;

	$request = service('request');

	// 请求的 uri（如 /about ）
	$request->uri->getPath();

	// 检索 $_GET 与 $_POST 变量
	$request->getGet('foo');
	$request->getPost('foo');

	// 从 $_REQUEST 检索，其中应同时包含 $_GET 和 $_POST 内容
	$request->getVar('foo');

	// 从 AJAX 调用中检索 JSON
	$request->getJSON();

	// 检索 server 变量
	$request->getServer('Host');

	// 检索 HTTP 请求头，使用不区分大小写的名称
	$request->getHeader('host');
	$request->getHeader('Content-Type');

	$request->getMethod();  // GET, POST, PUT 等等

request 类会在后台为你做很多工作，你无需担心。 ``isAJAX()`` 和 ``isSecure()`` 函数会自动检查几种不同的 method 来
最后确定正确的答案。

.. note:: ``isAJAX()`` 函数依赖于 ``X-Requested-With`` 头部，这个头部在一些情况下，不会在 XHR 请求中通过 JavaScript 默认发送。想要了解如何避免这个问题，请参考 :doc:`AJAX Requests </general/ajax>` 章节

CodeIgniter 还提供了 :doc:`Response 类 </outgoing/response>` ，它是 HTTP 响应的面向对象式表示。
它为你提供一种简单而强大的方法来构造对客户的响应： ::

  use CodeIgniter\HTTP\Response;

  $response = service('response');

  $response->setStatusCode(Response::HTTP_OK);
  $response->setBody($output);
  $response->setHeader('Content-type', 'text/html');
  $response->noCache();

  // 把响应结果发给浏览器
  $response->send();

另外， :doc:`Response 类 </outgoing/response>` 还允许你处理 HTTP 缓存层以获得最佳性能。

