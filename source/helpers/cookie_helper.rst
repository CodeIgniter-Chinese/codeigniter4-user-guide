#############
小型文字档案（cookie）辅助函数
#############

Cookie 辅助函数文件包含一些协助 Cookie 运行的函数。

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

加载 cookie 辅助函数
===================

辅助函数文件使用下面的代码加载::

	helper('cookie');

通用函数
===================

下面的函数是通用函数:


.. php:function:: set_cookie($name[, $value = ''[, $expire = ''[, $domain = ''[, $path = '/'[, $prefix = ''[, $secure = false[, $httpOnly = false]]]]]]])

	:param	mixed	$name: Cookie 名称 '或' 对这函数所有通用参数的关联数组
	:param	string	$value: Cookie 值
	:param	int	$expire: 直到截止时的秒数
	:param	string	$domain: Cookie 域名 (通常是: .yourdomain.com)
	:param	string	$path: Cookie 路径
	:param	string	$prefix: Cookie 名称前缀
	:param	bool	$secure: 是否仅仅通过 HTTPS 发送 cookie
	:param	bool	$httpOnly: 是否从 JavaScript 中隐藏 Cookie
	:rtype:	void


辅助函数给你更友好的语法去设置浏览器的 Cookies. 对于 Cookie 设置函数使用描述参考 :doc: `响应库 <../libraries/response>` , 
像这样的函数的别名是 ``Response::setCookie()``.


.. php:function:: get_cookie($index[, $xssClean = false])

	:param	string	$index: Cookie 名称
	:param	bool	$xss_clean: 返回值是否应用在 XSS 过滤中
	:returns:	返回 cookie 值而如果没有则为空
	:rtype:	mixed

	
辅助函数给你更友好的语法去 *获取* 浏览器的 Cookies. 对于 Cookie 获取函数详细的使用描述参考
:doc: `传入请求库 <../libraries/incomingrequest>` , 像这样的函数应用非常近似于 ``IncomingRequest::getCookie()`` , 
你也许会设置在你的 *application/Config/App.php* 文件里除了它也会预置在 ``$cookiePrefix`` 中 .
	

.. php:function:: delete_cookie($name[, $domain = ''[, $path = '/'[, $prefix = '']]])

	:param	string	$name: Cookie 名称
	:param	string	$domain: Cookie 域名 (通常是: .yourdomain.com)
	:param	string	$path: Cookie 路径
	:param	string	$prefix: Cookie 名称前缀
	:rtype:	void
	

该函数让你删除一个 cookie. 除非你已经设置了一个定制路径或者其他值，Cookie 的名字仅仅必须的。
	::

		delete_cookie('name');

删除 cookie 函数对 ``set_cookie()`` 来说是以另外的方式恒等的，除了它没有值和截止参数。你能在第一参数里确定数组值或者你要设置 *非连续* 参数。 
	::

		delete_cookie($name, $domain, $path, $prefix);
