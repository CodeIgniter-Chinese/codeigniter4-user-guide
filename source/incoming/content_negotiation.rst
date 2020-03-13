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

When accessed this way, the first parameter is the type of content you're trying to find a match for, while the
second is an array of supported values.

===========
协商
===========

In this section, we will discuss the 4 types of content that can be negotiated and show how that would look using
both of the methods described above to access the negotiator.

媒体
=====

The first aspect to look at is handling 'media' negotiations. These are provided by the ``Accept`` header and
is one of the most complex headers available. A common example is the client telling the server what format it
wants the data in. This is especially common in API's. For example, a client might request JSON formatted data
from an API endpoint::

	GET /foo HTTP/1.1
	Accept: application/json

The server now needs to provide a list of what type of content it can provide. In this example, the API might
be able to return data as raw HTML, JSON, or XML. This list should be provided in order of preference::

	$supported = [
		'application/json',
		'text/html',
		'application/xml'
	];

	$format = $request->negotiate('media', $supported);
	// or
	$format = $negotiate->media($supported);

In this case, both the client and the server can agree on formatting the data as JSON so 'json' is returned from
the negotiate method. By default, if no match is found, the first element in the $supported array would be returned.
In some cases, though, you might need to enforce the format to be a strict match. If you pass ``true`` as the
final value, it will return an empty string if no match is found::

	$format = $request->negotiate('media', $supported, true);
	// or
	$format = $negotiate->media($supported, true);

语言
========

Another common usage is to determine the language the content should be served in. If you are running only a single
language site, this obviously isn't going to make much difference, but any site that can offer up multiple translations
of content will find this useful, since the browser will typically send the preferred language along in the ``Accept-Language``
header::

	GET /foo HTTP/1.1
	Accept-Language: fr; q=1.0, en; q=0.5

In this example, the browser would prefer French, with a second choice of English. If your website supports English
and German you would do something like::

	$supported = [
		'en',
		'de'
	];

	$lang = $request->negotiate('language', $supported);
	// or
	$lang = $negotiate->language($supported);

In this example, 'en' would be returned as the current language. If no match is found, it will return the first element
in the $supported array, so that should always be the preferred language.

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

