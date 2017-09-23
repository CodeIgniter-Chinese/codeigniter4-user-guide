*************
请求类
*************

请求类是 HTTP 请求的面向对象表现形式。这意味着它可以用于传入请求，例如来自浏览器的请求，以及将请求从应用程序发到到第三方应用的传出请求。

这个类提供了它们需要的共同的功能，但是这两种情况都有自定义的类，它们继承请求类，然后添加特定的功能。

从 :doc:`传入请求类 </libraries/incomingrequest>` 和 :doc:`CURL请求类 </libraries/curlrequest>` 了解更多信息。

===============
类参考
===============

.. php:class:: CodeIgniter\\HTTP\\IncomingRequest

	.. php:method:: getIPAddress()

		:returns: 可以检测到的用户 IP 地址，否则为 NULL ，如果 IP 地址无效，则返回 0.0.0.0
		:rtype: string

		返回当前用户的 IP 地址。如果 IP 地址无效，返回 '0.0.0.0' ::

			echo $request->getIPAddress();

		.. important:: 此方法会根据 ``App->proxy_ips`` 的配置，来返回 HTTP_X_FORWARDED_FOR、 HTTP_CLIENT_IP、HTTP_X_CLIENT_IP 或 HTTP_X_CLUSTER_CLIENT_IP 。

	.. php:method:: validIP($ip[, $which = ''])

		:param	string	$ip: IP 地址
		:param	string	$which: IP 协议 ('ipv4' 或 'ipv6')
		:returns:	IP 有效返回 true，否则返回 false
		:rtype:	bool

		传入一个 IP 地址，根据 IP 是否有效返回 true 或 false

		.. note:: $request->getIPAddress() 自动检测 IP 地址是否有效

                ::

			if ( ! $request->validIP($ip))
			{
                            echo 'Not Valid';
			}
			else
			{
                            echo 'Valid';
			}

		第二个参数可选，可以为 'ipv4' 或 'ipv6'。默认这两种格式会全部检查。


	.. php:method:: method([$upper = FALSE])

		:param	bool	$upper: 以大写还是小写返回方法名，TRUE 表示大写
		:returns:	HTTP 请求方法
		:rtype:	string

		返回 ``$_SERVER['REQUEST_METHOD']``, 并且转换字母到指定大写或小写
		::

			echo $request->method(TRUE); // Outputs: POST
			echo $request->method(FALSE); // Outputs: post
			echo $request->method(); // Outputs: post

	.. php:method:: getServer([$index = null[, $filter = null[, $flags = null]]])

		:param	mixed	$index: 要过滤的变量
		:param  int     $filter: 要过滤的类型，过滤类型列表 `见此 <http://php.net/manual/en/filter.filters.php>`_.
		:param  int     $flags: 过滤器ID. 完整列表 `见此 <http://php.net/manual/en/filter.filters.flags.php>`_.
		:returns:	$_SERVER 值，如果不存在则返回NULL
		:rtype:	mixed

		该方法与  :doc:`IncomingRequest 类 </libraries/incomingrequest>` 中的 ``post()``， ``get()`` 和 ``cookie()`` 方法相同。只是它只获取 getServer 数据(``$_SERVER``) ::

			$request->getServer('some_data');

		要返回多个 ``$_SERVER`` 值的数组，请将所有键作为数组传递。
		::

			$require->getServer(array('SERVER_PROTOCOL', 'REQUEST_URI'));
