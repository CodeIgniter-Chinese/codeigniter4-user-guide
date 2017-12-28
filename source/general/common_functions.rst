##############################
公共函数和全局常量
##############################

CodeIgniter 你可以在任何地方使用它们，并且不需要加载任何 类库或辅助函数。

.. contents:: Page Contents
	:local:

================
公共函数
================

服务访问器函数
=================

.. php:function:: cache ( [$key] )

    :参数  string $key: The 需从缓存中检索的参数名 (可选)
    :返回: 缓存对象或从缓存取回的变量
    :返回类型: mixed

    若 $key 不存在, 则返回缓存引擎实例. 若 $key
    有值存在, 则返回 $key 当前存储在缓存中的值,
    若值不存在则返回false.

    Examples::

     	$foo = cache('foo');
    	$cache = cache();

.. php:function:: env ( $key[, $default=null])

	:参数 string $key: 需检索的环境变量中的参数名
	:参数 mixed  $default: 如参数值不存在则返回默认值.
	:返回: 运行环境变量, 默认值, 或者 null.
	:返回类型: mixed

	用于检索事前设置在环境变量中的变量值,若无设置则返回默认值. 
	若没有找到健值则返回一个布尔值结果（false）.

        在特定的运行环境中设置变量非常有用，例如数据库设置，API健值等.

.. php:function:: esc ( $data, $context='html' [, $encoding])

	:参数   string|array   $data: 被输出的信息.
	:参数   string   $context: 被输出内容的上下文. 默认值 'html'.
	:参数   string   $encoding: 编码字符串.
	:返回: 输出的数据（The escaped data）.
	:返回类型: string

	页面中包含的输出数据, 它在防止 XSS 攻击时很有用。
	使用Zend Escaper library把控过滤中的数据。

	若 $data 为字符串, 则直接把输出返回.
	若 $data 为数组, 则遍历key/value键值对中的'value'.

	有效的上下文值: html, js, css, url, attr, raw, null

.. php:function:: helper( $filename )

	:参数   string   $filename: 加载的辅助类文件的名称.

        加载辅助类文件。

	详情参照 the :doc:`helpers` 页.

.. php:function:: lang(string $line[, array $args]): string

	:参数 string $line: 检索文本的行
	:参数 array  $args: 一组数组数据，用于替代占位符.

	检索一个基于某个别名字符串的本地特定文件。

        更多详细信息请见 the :doc:`Localization </libraries/localization>` 页.

.. php:function:: session( [$key] )

	:变量 string $key: 在session中查找的健值名称.
	:返回: $key的值或者null，若$key不存在则返回一个session object实例。
	:返回类型: mixed

	提供一个便捷的方式访问session类和检索存储于其中的值.更多信息详见 the :doc:`Sessions </libraries/sessions>` 页.

.. php:function:: timer( [$name] )

	:参数 string $name: 检测点的名称.
	:返回: Timer 实例
	:返回类型: CodeIgniter\Debug\Timer

	提供一个便捷的方法快速访问 Timer class. 你可忽略参数，其将从此刻开始计时；
	或者停止计时某名称检测点，如果该名称检测点已经在运行。

	Example::

		// Get an instance
		$timer = timer();

		// Set timer start and stop points
		timer('controller_loading');    // Will start the timer
		. . .
		timer('controller_loading');    // Will stop the running timer

.. php:function:: view ($name [, $data [, $options ]])

	:参数   string   $name: 被加载的文件名
	:参数   array   $data: 键值对数组，在视图中能被获取。
	:参数   array    $options: 可选的参数数组，用于传递值给渲染类.
	:返回: 视图的输出.
	:返回类型: string

        抓取当前的界面渲染类（RendererInterface-compatible class）
	并请求它递交特定的视图. 提供了便捷的方法给控制器、类库、路由闭包使用,

	通常, 唯一有效可选项使用`$options`数组是, 在同一次请求中数据持续保持在多次调用view()中。 缺省情况下,传给view的数据会
	被丢弃，在显示单独的view文件后.

	$option数组主要作用为提供第三方类库整合，例如Twig。

	Example::

		$data = ['user' => $user];

		echo view('user_profile', $data);

	 详情参见 the :doc:`Views <views>` 页。

Miscellaneous Functions
=======================

.. php:function:: csrf_token ()

	:returns: The name of the current CSRF token.
	:rtype: string

	Returns the name of the current CSRF token.

.. php:function:: csrf_hash ()

	:returns: The current value of the CSRF hash.
	:rtype: string

	Returns the current CSRF hash value.

.. php:function:: csrf_field ()

	:returns: A string with the HTML for hidden input with all required CSRF information.
	:rtype: string

	Returns a hidden input with the CSRF information already inserted:

		<input type="hidden" name="{csrf_token}" value="{csrf_hash}">

.. php:function:: force_https ( $duration = 31536000 [, $request = null [, $response = null]] )

	:param  int  $duration: The number of seconds browsers should convert links to this resource to HTTPS.
	:param  RequestInterface $request: An instance of the current Request object.
	:param  ResponseInterface $response: An instance of the current Response object.

	Checks to see if the page is currently being accessed via HTTPS. If it is, then
	nothing happens. If it is not, then the user is redirected back to the current URI
	but through HTTPS. Will set the HTTP Strict Transport Security header, which instructs
	modern browsers to automatically modify any HTTP requests to HTTPS requests for the $duration.

.. php:function:: is_cli ()

	:returns: TRUE if the script is being executed from the command line or FALSE otherwise.
	:rtype: bool

.. php:function:: log_message ($level, $message [, array $context])

	:param   string   $level: The level of severity
	:param   string   $message: The message that is to be logged.
	:param   array    $context: An associative array of tags and their values that should be replaced in $message
	:returns: TRUE if was logged succesfully or FALSE if there was a problem logging it
	:rtype: bool

	Logs a message using the Log Handlers defined in **application/Config/Logger.php**.

	Level can be one of the following values: **emergency**, **alert**, **critical**, **error**, **warning**,
	**notice**, **info**, or **debug**.

	Context can be used to substitute values in the message string. For full details, see the
	:doc:`Logging Information <logging>` page.

.. php:function:: redirect( $uri[, ...$params ] )

	:param  string  $uri: The URI to redirect the user to.
	:param  mixed   $params: one or more additional parameters that can be used with the :meth:`RouteCollection::reverseRoute` method.

	Convenience method that works with the current global ``$request`` and
	``$router`` instances to redirect using named/reverse-routed routes
	to determine the URL to go to. If nothing is found, will treat
	as a traditional redirect and pass the string in, letting
	``$response->redirect()`` determine the correct method and code.

	If more control is needed, you must use ``$response->redirect()`` explicitly.

.. php:function:: redirect_with_input( $uri[, ...$params] )

	:param string $uri: The URI to redirect the user to.
	:param mixed  $params: one or more additional parameters that can be used with the :meth:`RouteCollection::reverseRoute` method.

	Identical to the ``redirect()`` method, except this flashes the request's $_GET and $_POST values to the session.
	On the next page request, the form helper ``set_*`` methods will check for data within the old input first, then,
	if it's not found, the current GET/POST will be checked.

	.. note:: In order to retrieve the old, the session MUST be started prior to calling the function.

.. php:function:: remove_invisible_characters($str[, $url_encoded = TRUE])

	:param	string	$str: Input string
	:param	bool	$url_encoded: Whether to remove URL-encoded characters as well
	:returns:	Sanitized string
	:rtype:	string

	This function prevents inserting NULL characters between ASCII
	characters, like Java\\0script.

	Example::

		remove_invisible_characters('Java\\0script');
		// Returns: 'Javascript'

.. php:function:: route_to ( $method [, ...$params] )

	:param   string   $method: The named route alias, or name of the controller/method to match.
	:param   mixed   $params: One or more parameters to be passed to be matched in the route.

	Generates a relative URI for you based on either a named route alias, or a controller::method
	combination. Will take parameters into effect, if provided.

	For full details, see the :doc:`routing` page.

.. php:function:: service ( $name [, ...$params] )

	:param   string   $name: The name of the service to load
	:param   mixed    $params: One or more parameters to pass to the service method.
	:returns: An instance of the service class specified.
	:rtype: mixed

	Provides easy access to any of the :doc:`Services <../concepts/services>` defined in the system.
	This will always return a shared instance of the class, so no matter how many times this is called
	during a single request, only one class instance will be created.

	Example::

		$logger = service('logger');
		$renderer = service('renderer', APPPATH.'views/');

.. php:function:: single_service ( $name [, ...$params] )

	:param   string   $name: The name of the service to load
	:param   mixed    $params: One or more parameters to pass to the service method.
	:returns: An instance of the service class specified.
	:rtype: mixed

	Identical to the **service()** function described above, except that all calls to this
	function will return a new instance of the class, where **service** returns the same
	instance every time.

.. php:function:: stringify_attributes ( $attributes [, $js] )

	:param   mixed    $attributes: string, array of key value pairs, or object
	:param   boolean  $js: TRUE if values do not need quotes (Javascript-style)
	:returns: String containing the attribute key/value pairs, comma-separated
	:rtype: string

	Helper function used to convert a string, array, or object of attributes to a string.


================
Global Constants
================

The following constants are always available anywhere within your application.

Core Constants
==============

.. php:const:: ROOTPATH

	The path to the main application directory. Just above ``public``.

.. php:const:: APPPATH

	The path to the **application** directory.

.. php:const:: BASEPATH

	The path to the **system** directory.

.. php:const:: FCPATH

	The path to the directory that holds the front controller.

.. php:const:: SELF

	The path to the front controller, **index.php**.

.. php:const:: WRITEPATH

	The path to the **writable** directory.


Time Constants
==============

.. php:const:: SECOND

	Equals 1.

.. php:const:: MINUTE

	Equals 60.

.. php:const:: HOUR

	Equals 3600.

.. php:const:: DAY

	Equals 86400.

.. php:const:: WEEK

	Equals 604800.

.. php:const:: MONTH

	Equals 2592000.

.. php:const:: YEAR

	Equals 31536000.

.. php:const:: DECADE

	Equals 315360000.
