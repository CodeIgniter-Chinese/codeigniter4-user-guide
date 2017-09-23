==============
HTTP 响应
==============

响应类扩展了 :doc:`HTTP 消息类 </libraries/message>` ，只适用于服务器返回响应给调用它的客户端。

.. contents:: Page Contents

使用响应类
=========================

响应类被实例化并传递到控制器。可以通过 ``$this->response`` 访问它。很多时候不需要直接使用它，因为 CodeIgniter 会为你发送标头和正文。
如果一切正常，页面会成功创建被请求的内容。
但是当出现问题时，或者当你需要发送指定的状态码，或者想要使用强大的 HTTP 缓存，可以立即使用它。

设置输出内容
------------------

当需要直接设置脚本的输出内容时，不要依赖CodeIgniter来自动获取它，应该手动调用 ``setBody`` 方法。通常用于设置响应的状态码。 ::

	$this->response->setStatusCode(404)
	               ->setBody($body);

响应中的原因短语 ('OK', 'Created', 'Moved Permenantly') 将被自动添加，但也可以通过为 ``setStatusCode()`` 方法设置第二个参数来添加自定义的原因。 ::

	$this->response->setStatusCode(404, 'Nope. Not here.');

设置 HTTP 头
---------------

通常，你需要为响应设置 HTTP 头。响应类通过 ``setHeader()`` 方法简化了这个操作。

``setHeader()`` 方法的第一个参数是 HTTP 头的名称，第二个参数是值，它可以是字符串或值的数组，当发送到客户端时将被正确组合。

使用这些函数而不是使用PHP原生函数，可以确保不会过早发送 HTTP 头导致错误，并使测试成为可能。 ::

	$response->setHeader('Location', 'http://example.com')
			 ->setHeader('WWW-Authenticate', 'Negotiate');

如果 HTTP 头已经存在并且可以有多个值，可以使用 ``appendHeader()`` ``prependHeader()`` 方法分别将值添加到值列表的结尾或开头。

第一个参数是 HTTP 头的名称，第二个参数是添加到结尾或开头的值。
::

	$response->setHeader('Cache-Control', 'no-cache')
			->appendHeader('Cache-Control', 'must-revalidate');

HTTP 头可以用 ``removeHeader()`` 方法移除，此方法只接受 HTTP 头的名称作为唯一参数。并且不区分大小写。
::

	$response->removeHeader('Location');

文件下载
===================

响应类提供了一个简单地将文件发送给客户端的方法，提示浏览器下载文件。会设置适当的标题来实现。

第一个参数是 **下载文件的名称**，第二个参数是文件内容。

如果将第二个参数设为 NULL， 并且 ``$filename`` 是一个已存在的，可读的文件路径，那么将会使用这个路径下的内容作为文件内容。

如果将第三个参数设置为布尔值 TRUE，那么实际的文件的 MIME 类型(基于文件扩展名)将被发送，这样当浏览器拥有该类型的处理程序 - 可以使用到它。

示例::

	$data = 'Here is some text!';
	$name = 'mytext.txt';
	$response->download($name, $data);

如果要从服务器下载现有的文件，你需要这样做::

	// photo.jpg 的内容将被自动读取
	$response->download('/path/to/photo.jpg', NULL);

HTTP 缓存
============

内置的 HTTP 规范是帮助客户端(通常是web浏览器)缓存结果的工具。

正确使用它，可以为应用程序带来巨大的性能提升，因为它会告诉客户端不需要联系服务器，因为没有任何改变。你不会比这更快。

这些都通过 ``Cache-Control`` 和 ``Etag`` 头来处理。本指南并不适合完整介绍缓存的功能，但你可以在 `Google Developers <https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching>`_ 和 `Mobify Blog <https://www.mobify.com/blog/beginners-guide-to-http-cache-headers/>`_ 中了解更多。

默认情况下，所有通过 CodeIgniter 发送的响应都是关闭了 HTTP 缓存的。
但在实际应用中，情况千变万化，无法简单的设置一个合适的默认值，除非关闭它，
不过，可以通过 ``setCache()`` 方法设置你需要的缓存的值。这非常简单 ::

	$options = [
		'max-age'  => 300,
		's-maxage' => 900,
		'etag'     => 'abcde',
	];
	$this->response->setCache($options);

``$options`` 是一个简单的键值对数组，它们被分配给 ``Cache-Control`` 头。你也可以根据具体情况自由设定所有选项。

虽然大多数选项都应用于 ``Cache-Control`` 头，但它会智能地处理 ``etag`` 和 ``last-modified`` 选项到适当的头。

内容安全策略(CSP)
=======================

对XSS攻击的最佳保护方式之一是在站点上实施内容安全策略。

这迫使你将从你网站的 HTML 中载入的每一个内容来源列入白名单中，包括图片，样式表，JavaScript文件等。浏览器将拒绝白名单外的的内容。这个白名单在响应的 ``Content-Security-Policy`` 标头中创建，并且有多种配置方式。

这听起来很复杂，在某些网站上肯定会有挑战性。对于很多简单的网站，所有的内容由相同的域名(http://example.com)提供，整合起来非常简单。

由于这是一个复杂的主题，本用户指南将不会覆盖所有细节。有关更多信息，你应该访问以下网站:

* `Content Security Policy main site <http://content-security-policy.com/>`_
* `W3C Specification <https://www.w3.org/TR/CSP>`_
* `Introduction at HTML5Rocks <http://www.html5rocks.com/en/tutorials/security/content-security-policy/>`_
* `Article at SitePoint <https://www.sitepoint.com/improving-web-security-with-the-content-security-policy/>`_

启用CSP
--------------

默认情况下，CSP策略是禁用的。想要在应用程序中启用CSP，修改 **application/Config/App.php** 中的 ``CSPEnabled`` 的值 ::

	public $CSPEnabled = true;

当开启后，响应对象将包含一个 ``CodeIgniter\HTTP\ContentSecurityPolicy`` 的实例。

在 **application/Config/ContentSecurityPolicy.php** 中设置的值应用于这个实例，如果在运行时没有修改，那么将会发送正确的格式化后的标题，并且完成所有操作。

运行时配置
---------------------

如果你的应用需要在运行时进行更改，则可以访问 ``$response->CSP`` 实例。该类拥有很多方法，可以很清晰地映射到你需要设置的 header 头 ::

	$reportOnly = true;

	$response->CSP->reportOnly($reportOnly);
	$response->CSP->setBaseURI('example.com', true);
	$response->CSP->setDefaultSrc('cdn.example.com', $reportOnly);
	$response->CSP->setReportURI('http://example.com/csp/reports');
	$response->CSP->setSandbox(true, ['allow-forms', 'allow-scripts']);
	$response->CSP->upgradeInsecureRequests(true);
	$response->CSP->addChildSrc('https://youtube.com', $reportOnly);
	$response->CSP->addConnectSrc('https://*.facebook.com', $reportOnly);
	$response->CSP->addFontSrc('fonts.example.com', $reportOnly);
	$response->CSP->addFormAction('self', $reportOnly);
	$response->CSP->addFrameAncestor('none', $reportOnly);
	$response->CSP->addImageSrc('cdn.example.com', $reportOnly);
	$response->CSP->addMediaSrc('cdn.example.com', $reportOnly);
	$response->CSP->addObjectSrc('cdn.example.com', $reportOnly);
	$response->CSP->addPluginType('application/pdf', $reportOnly);
	$response->CSP->addScriptSrc('scripts.example.com', $reportOnly);
	$response->CSP->addStyleSrc('css.example.com', $reportOnly);

内联内容
--------------

可以设置一个网站不保护自己的页面上的内联脚本和样式，因为这可能是用户生成的内容的结果。
为了防止这种情况，CSP 允许你再 <style> 和 <script> 标记中指定一个随机数，并将这些值添加到响应头中。
这样处理很痛苦，但是却是最安全的。
为了简单起见，你可以在代码中包含 {csp-style-nonce} 或 {csp-script-nonce} 占位符，程序将会自动为你处理 ::

	// Original
	<script {csp-script-nonce}>
	    console.log("Script won't run as it doesn't contain a nonce attribute");
	</script>

	// Becomes
	<script nonce="Eskdikejidojdk978Ad8jf">
	    console.log("Script won't run as it doesn't contain a nonce attribute");
	</script>

	// OR
	<style {csp-style-nonce}>
		. . .
	</style>

***************
类参考
***************

.. note:: 除了这里列出的方法，响应类还继承了 :doc:`消息类 </libraries/message>` 的方法。

父类提供的可用的方法:

* :meth:`CodeIgniter\\HTTP\\Message::body`
* :meth:`CodeIgniter\\HTTP\\Message::setBody`
* :meth:`CodeIgniter\\HTTP\\Message::populateHeaders`
* :meth:`CodeIgniter\\HTTP\\Message::headers`
* :meth:`CodeIgniter\\HTTP\\Message::header`
* :meth:`CodeIgniter\\HTTP\\Message::headerLine`
* :meth:`CodeIgniter\\HTTP\\Message::setHeader`
* :meth:`CodeIgniter\\HTTP\\Message::removeHeader`
* :meth:`CodeIgniter\\HTTP\\Message::appendHeader`
* :meth:`CodeIgniter\\HTTP\\Message::protocolVersion`
* :meth:`CodeIgniter\\HTTP\\Message::setProtocolVersion`
* :meth:`CodeIgniter\\HTTP\\Message::negotiateMedia`
* :meth:`CodeIgniter\\HTTP\\Message::negotiateCharset`
* :meth:`CodeIgniter\\HTTP\\Message::negotiateEncoding`
* :meth:`CodeIgniter\\HTTP\\Message::negotiateLanguage`
* :meth:`CodeIgniter\\HTTP\\Message::negotiateLanguage`

.. php:class:: CodeIgniter\\HTTP\\Response

	.. php:method:: statusCode()

		:returns: 此次响应的 HTTP 状态码
		:rtype: int

		返回此响应的当前状态码，如果没有设置状态码，则会抛出 BadMethodCallException 异常。::

			echo $response->statusCode();

	.. php:method:: setStatusCode($code[, $reason=''])

		:param int $code: HTTP 状态码
		:param string $reason: 一个可选的原因短语
		:returns: 当前的响应实例
		:rtype: CodeIgniter\\HTTP\\Response

		设置此次响应的 HTTP 状态码 ::

		    $response->setStatusCode(404);

		原因短语将会根据协议规定自动的生成。如果你需要为自定义状态码设置自己的愿意短语，你可以将原因短语作为第二个参数传递 ::

			$response->setStatusCode(230, "Tardis initiated");

	.. php:method:: reason()

		:returns: 当前的原因短语。
		:rtype: string

		返回此响应的当前状态码。如果没有设置状态，将返回一个空字符串 ::

			echo $response->reason();

	.. php:method:: setDate($date)

		:param DateTime $date: 一个设置了此响应的时间的 DateTime 实例。
		:returns: 	当前的响应类实例
		:rtype: CodeIgniter\\HTTP\\Response

		设置响应的时间。 ``$date`` 参数必须是一个 ``DateTime`` 实例 ::

			$date = DateTime::createFromFormat('j-M-Y', '15-Feb-2016');
			$response->setDate($date);

	.. php:method:: setContentType($mime[, $charset='UTF-8'])

		:param string $mime: 响应的内容类型
		:param string $charset: 此响应使用的字符集。
		:returns: 	当前的响应类实例
		:rtype: CodeIgniter\\HTTP\\Response

		设置此响应的内容类型 ::

			$response->setContentType('text/plain');
			$response->setContentType('text/html');
			$response->setContentType('application/json');

		默认情况下，该方法将字符集设置为 ``UTF-8``。如果你需要修改，可以将字符集作为第二个参数传递 ::

			$response->setContentType('text/plain', 'x-pig-latin');

	.. php:method:: noCache()

		:returns: 当前的响应类实例
		:rtype: CodeIgniter\\HTTP\\Response

		设置 ``Cache-Control`` 标头来关闭所有的 HTTP 缓存。这是所有响应消息的默认设置 ::
			
			$response->noCache();
			
			// Sets the following header:
			Cache-Control: no-store, max-age=0, no-cache

	.. php:method:: setCache($options)

		:param array $options: 一组缓存设置的键值
		:returns: 当前的响应类实例
		:rtype: CodeIgniter\\HTTP\\Response

		设置 ``Cache-Control`` 标头，包括 ``ETags`` 和 ``Last-Modified`` 。 典型的键有:

		* etag
		* last-modified
		* max-age
		* s-maxage
		* private
		* public
		* must-revalidate
		* proxy-revalidate
		* no-transform

		当设置了 last-modified 选项时，它的值可以是一个 date 字符串，或一个 DateTime 对象。

	.. php:method:: setLastModified($date)

		:param string|DateTime $date: 设置 Last-Modified 的时间
		:returns: 当前的响应类实例
		:rtype: CodeIgniter\\HTTP\\Response

		设置 ``Last-Modified`` 头。 ``$date`` 可以是一个字符串或一个 ``DateTime`` 实例 ::

			$response->setLastModified(date('D, d M Y H:i:s'));
			$response->setLastModified(DateTime::createFromFormat('u', $time));

	.. php:method:: send()

		:returns: 当前的响应类实例
		:rtype: CodeIgniter\\HTTP\\Response

		通知响应类发送内容给客户端。这将首先发送 HTTP 头，然后是响应的主体内容。对于主应用程序的响应，你不需要调用它，因为它由 CodeIgniter 自动处理。

	.. php:method:: setCookie($name = ''[, $value = ''[, $expire = ''[, $domain = ''[, $path = '/'[, $prefix = ''[, $secure = FALSE[, $httponly = FALSE]]]]]]])

		:param	mixed	$name: Cookie 名称或参数数组
		:param	string	$value: Cookie 值
		:param	int	$expire: Cookie 过期时间，单位：秒
		:param	string	$domain: Cookie 作用域
		:param	string	$path: Cookie 可用的路径
		:param	string	$prefix: Cookie 前缀
		:param	bool	$secure: 是否只通过 HTTPS 传输 Cookie
		:param	bool	$httponly: 是否只允许 HTTP 请求读取cookie，JavaScript不可以读取
		:rtype:	void

		设置一个包含你指定的值的 Cookie 。有两种将信息传递给该方法的方式:数组和独立参数:

		**数组方式**

		使用此方法，将关联数组传递给第一个参数 ::

			$cookie = array(
				'name'   => 'The Cookie Name',
				'value'  => 'The Value',
				'expire' => '86500',
				'domain' => '.some-domain.com',
				'path'   => '/',
				'prefix' => 'myprefix_',
				'secure' => TRUE
			);

			$response->setCookie($cookie);

		**注意事项**

		只需要名称和值。要删除 Cookie ，将其设置为过期即可。

		过期时间使用 **秒数** , 将从当前时间开始计算。

		不要设置为一个具体的时间，而只是从 *now* 开始的你希望 Cookie 有效的秒数。

		如果过期时间设置为零，Cookie 将只在浏览器打开时有效，浏览器关闭时则被清除。

		对于整站的 Cookie ， 无论你的网站是被如何请求的，请将你的网址添加到到 **domain** 中并且以 . 开始，例如:
		.your-domain.com

		通常不需要该路径，因为默认已经设置了根目录。

		仅当你需要避免与服务器的其他相同命名的 Cookie 冲突时，才需要前缀。

		仅当你想要加密 Cookie 时才需要设置 secure 项为 TRUE。

		**独立参数**

		如果你愿意，也可以使用单个参数传递数据来设置 Cookie。 ::

			$response->setCookie($name, $value, $expire, $domain, $path, $prefix, $secure);

