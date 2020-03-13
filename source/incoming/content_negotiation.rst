*******************
内容协商
*******************

内容协商是一种用来根据客户端和服务端可处理的资源类型，来决定返回给客户端哪种类型的内容的机制。
该机制可用来决定客户端是想要 HTML 还是想要 JSON ，一个图片是应该以 JPG 还是以 PNG 格式返回，或者支持哪种类型的压缩方法等。
这些决策是通过分析四个不同的请求头，而这些请求头里支持多个带有优先级的值选项。手动对这些值选项进行优先级匹配通常是较有挑战性的，因此 CodeIgniter提供了 ``Negotiator`` 来处理以上过程。

=================
加载类文件
=================

你可以通过 Service 类来手动加载一个该类的实例::

	$negotiator = \Config\Services::negotiator();

以上操作会获取所有的请求实例并自动将其自动注入到 Negotiator （协商，下同）类中。

该类并不需要主动加载。而是通过请求的 ``IncomingRequest`` 实例来进行范文。
尽管你并不能通过这一过程直接访问该实例，你可以通过 ``negotiate()`` 方法来调用它的所有方法::

	$request->negotiate('media', ['foo', 'bar']);

当通过该方法访问实例时，第一个参数是你需要匹配的内容的类型，第二个是所支持的类型值构成的数组。

===========
协商
===========

本节中，我们将讨论四种可以用来协商的类型，并展示如何通过上述两种方法来进行内容协商。

媒体
=====

第一层首先要看的就是媒体协商。该协商方式是通过 ``Accept`` 请求头进行的，并且是可用的请求头中最为复杂的类型之一。
一个常见的例子就是客户端告诉服务端其所需要的数据格式，而这种操作在 API 中最为常见。例如，一个客户端可能从一个 API 终点请求 JSON 编码的数据::

	GET /foo HTTP/1.1
	Accept: application/json

该服务器需要提供一个所支持的该内容的类型列表。在本例中，API 可能需要返回像原生 HTML ，JSON 或者是 XML 格式的数据。而根据客户端偏好，该列表应顺序返回::

	$supported = [
		'application/json',
		'text/html',
		'application/xml'
	];

	$format = $request->negotiate('media', $supported);
	// 或者是
	$format = $negotiate->media($supported);

在本例中，客户端和服务器协商一致，将数据以 JSON 的格式返回，因此 'json' 就会从协商方法中返回。默认情况下，如果没有匹配到，在 ``$support`` 数组中的第一个成员就会返回。
尽管在某些情况下，你可能会强制要求服务端进行严格匹配格式。因此如果你将 ``true`` 作为最后参数传入时，在匹配不到时就会返回空字符串::

	$format = $request->negotiate('media', $supported, true);
	// 或
	$format = $negotiate->media($supported, true);

语言
========

另一个常见的用法就是用于决定需要返回的内容的语言。如果你运行的是一个单语言网站，该功能显然并没有什么影响。
但是如果对于那些提供多语言内容的网站来说，该功能就会变得非常有用，基于浏览器将通常会在 ``Accept-Language`` 请求头中发送偏好的语言类型::

	GET /foo HTTP/1.1
	Accept-Language: fr; q=1.0, en; q=0.5

本例中，浏览器偏好法语，并次偏好英语。如果你的网站支持英语或德语，那么你就会如下操作::

	$supported = [
		'en',
		'de'
	];

	$lang = $request->negotiate('language', $supported);
	// 或
	$lang = $negotiate->language($supported);

本例中，"en"将作为当前语言返回。如果没有产生匹配，就会返回 ``$supported`` 数组的第一个成员，因此该成员将会一直作为偏好语言。

编码
========

``Accept-Encoding`` 请求头包含了客户端所期望接收到的字符集，用于确定客户端支持哪种类型的压缩方式::

	GET /foo HTTP/1.1
	Accept-Encoding: compress, gzip

你的 web 服务器将会定义可以使用的压缩类型。某些服务器，例如 Apache , 只支持了 **gzip** ::

	$type = $request->negotiate('encoding', ['gzip']);
	// 或
	$type = $negotiate->encoding(['gzip']);

更多信息，参阅 `Wikipedia <https://en.wikipedia.org/wiki/HTTP_compression>`_.

字符集
=============

所期待的字符集类型会通过 ``Accept-Charset`` 请求头来传值::

	GET /foo HTTP/1.1
	Accept-Charset: utf-16, utf-8

默认情况下，如果没有匹配的话就会返回 **utf-8** ::

	$charset = $request->negotiate('charset', ['utf-8']);
	// 或者是
	$charset = $negotiate->charset(['utf-8']);

