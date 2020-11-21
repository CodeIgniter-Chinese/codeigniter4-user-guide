################
Cookie 辅助函数
################

Cookie 辅助函数文件包含一些协助 Cookie 运行的函数。

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

加载 Cookie 辅助函数
======================

Cookie 辅助函数文件使用下面的代码加载::

	helper('cookie');

函数参考
===================

该辅助函数有下列可用函数:

.. php:function:: set_cookie($name[, $value = ''[, $expire = ''[, $domain = ''[, $path = '/'[, $prefix = ''[, $secure = false[, $httpOnly = false]]]]]]])

	:param	mixed	$name: Cookie 名称 *或* 对这函数所有通用参数的关联数组
	:param	string	$value: Cookie 值
	:param	int	$expire: 直到截止时的秒数
	:param	string	$domain: Cookie 域名 (通常是: .yourdomain.com)
	:param	string	$path: Cookie 路径
	:param	string	$prefix: Cookie 名称前缀
	:param	bool	$secure: 是否仅仅通过 HTTPS 发送 Cookie 
	:param	bool	$httpOnly: 是否从 JavaScript 中隐藏 Cookie 
	:rtype:	void

	辅助函数给你更友好的语法去 *设置* 浏览器的 Cookies. 辅助函数使用的说明参考 :doc:`响应库 </outgoing/response>` 
	, 同时对 ``Response::setCookie()`` 来说 Cookie 辅助函数是别称.

.. php:function:: get_cookie($index[, $xssClean = false])

	:param	string	$index: Cookie 名称
	:param	bool	$xss_clean: 返回值是否应用在 XSS 过滤中
	:returns:	返回 Cookie 值而如果没有则为空
	:rtype:	mixed

	辅助函数给你更友好的语法去 *获取* 浏览器的 Cookies. 辅助函数详细的使用说明参考 :doc:`传入请求库 </incoming/incomingrequest>` 
	同时辅助函数的作用非常近似于 ``IncomingRequest::getCookie()``, 
	你也许已经设置在你的 *application/Config/App.php* 文件里除了它也预置了 ``$cookiePrefix`` .

.. php:function:: delete_cookie($name[, $domain = ''[, $path = '/'[, $prefix = '']]])

	:param	string	$name: Cookie 名称
	:param	string	$domain: Cookie 域名 (通常是: .yourdomain.com)
	:param	string	$path: Cookie 路径
	:param	string	$prefix: Cookie 名称前缀
	:rtype:	void

	该函数让你删除一个 Cookie. 除非你已经设置了一个定制路径或者其他值，仅仅 Cookie 的名字是必须的。
	::

		delete_cookie('name');

	这个函数除了没有值和截止参数，它对 ``set_cookie()`` 来说在其他方面是恒等的。
	你能在第一参数里确定数组值或者你要设置离散参数。 
	::

		delete_cookie($name, $domain, $path, $prefix);
