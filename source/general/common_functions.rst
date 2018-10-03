##############################
公共函数和全局常量
##############################

CodeIgniter 你可以在任何地方使用它们，并且不需要加载任何 类库或辅助函数。

.. contents::
    :local:
    :depth: 2

================
公共函数
================

服务访问器函数
=================

.. php:function:: cache ( [$key] )

    :param  string $key: 需从缓存中检索的参数名 (可选)
    :返回: 缓存对象或从缓存取回的变量
    :返回类型: mixed

    若 $key 不存在, 则返回缓存引擎实例. 若 $key有值存在, 则返回 $key 当前存储在缓存中的值，若值不存在则返回false.

    Examples::

     	$foo = cache('foo');
    	$cache = cache();

.. php:function:: env ( $key[, $default=null])

	:param string $key: 需检索的环境变量中的参数名
	:param mixed  $default: 如参数值不存在则返回默认值.
	:返回: 运行环境变量, 默认值, 或者 null.
	:返回类型: mixed

	用于检索事前设置在环境变量中的变量值,若无设置则返回默认值.
	若没有找到健值则返回一个布尔值结果（false）.

        在特定的运行环境中利用 .env 文件设置环境变量非常有用，例如数据库设置，API健值等.

.. php:function:: esc ( $data, $context='html' [, $encoding])

	:param   string|array   $data: 被输出的信息.
	:param   string   $context: 被输出内容的上下文. 默认值 'html'.
	:param   string   $encoding: 编码字符串.
	:返回: 输出的数据（The escaped data）.
	:返回类型: string

	页面中包含的输出数据, 它在防止 XSS 攻击时很有用。
	使用Zend Escaper library把控过滤中的数据。

	若 $data 为字符串, 则简单转义并且返回。
	若 $data 为数组, 则遍历数组，转义 key/value 键值对中的 'value'。

	有效的 context 值: html, js, css, url, attr, raw, null

.. php:function:: helper( $filename )

	:param   string   $filename: 加载的辅助类文件的名称.

        加载辅助类文件。

	详情参照 the :doc:`helpers` 页.

.. php:function:: lang(string $line[, array $args]): string

	:param string $line: 检索文本的行
	:param array  $args: 一组数组数据，用于替代占位符.

	检索一个基于某个别名字符串的本地特定文件。

        更多详细信息请见 the :doc:`Localization </libraries/localization>` 页.

.. php:function:: session( [$key] )

	:变量 string $key: 在session中查找的健值名称.
	:返回: $key的值或者null，若$key不存在则返回一个session object实例。
	:返回类型: mixed

	提供一个访问 session 类和检索存储值的便捷方法。更多信息详见 the :doc:`Sessions </libraries/sessions>` 页.

.. php:function:: timer( [$name] )

	:param string $name: 检测点的名称.
	:返回: Timer 实例
	:返回类型: CodeIgniter\Debug\Timer

	提供一个快速访问 Timer class的便捷的方法。 你可以将基准点的名称作为唯一参数传递。这将从这一点开始计时，
	如果这个名称的计时器已经运行，则停止计时。

	Example::

		// Get an instance
		$timer = timer();

		// Set timer start and stop points
		timer('controller_loading');    // Will start the timer
		. . .
		timer('controller_loading');    // Will stop the running timer

.. php:function:: view ($name [, $data [, $options ]])

	:param   string   $name: 被加载的文件名
	:param   array   $data: 键值对数组，在视图中能被获取。
	:param   array    $options: 可选的参数数组，用于传递值给渲染类.
	:返回: 视图的输出.
	:返回类型: string

	抓取当前的 RendererInterface-compatible 类（界面渲染类），告诉它展示特定的视图。给控制器、库、路由闭包提供了一种便捷的方法。

	目前，在 $options 数组里只有一个选项是可用的，saveData 指定在同一个请求中，在多次调用 view() 时数据将连续。默认情况下，
	在显示该单一视图文件之后，该视图的数据被丢弃。

	$option 数组主要用于与第三方库整合，例如Twig。

	Example::

		$data = ['user' => $user];

		echo view('user_profile', $data);

	 详情参见 the :doc:`Views <views>` 页。

其他函数
=======================

.. php:function:: csrf_token ()

	:返回: 当前 CSRF token 名称。
	:返回类型: string

	返回当前 CSRF token名称。

.. php:function:: csrf_hash ()

	:返回: 当前 CSRF hash值.
	:返回类型: string

	返回当前 CSRF hash 的值.

.. php:function:: csrf_field ()

	:返回:  带有全部请求CSRF信息的隐藏input的HTML字符串。
	:返回类型: string

	返回已插入CSRF信息的隐藏input:

		<input type="hidden" name="{csrf_token}" value="{csrf_hash}">

.. php:function:: force_https ( $duration = 31536000 [, $request = null [, $response = null]] )

	:param  int  $duration: 浏览器的秒数应该将此资源的链接转换为 HTTPS 。
	:param  RequestInterface $request: 当前请求对象的实例。
	:param  ResponseInterface $response: 当前响应对象的实例。

	检查页面当前是否通过HTTPS访问，如果不是，则用户通过HTTPS重定向回当前URI。
	将设置 HTTP 严格的传输安全标头，该命令指示现代浏览器自动将HTTP请求修改为 $duration 参数时间的HTTPS请求。

.. php:function:: is_cli ()

	:返回: 如果脚本是从命令行执行的，则为true，否则为false。
	:返回类型: bool

.. php:function:: log_message ($level, $message [, array $context])

	:param   string   $level: 级别程度
	:param   string   $message: 写入日志的信息.
	:param   array    $context: 一个标记和值的联合数组被替换到 $message
	:返回: 如果写入日志成功则为 TRUE ，如果写入日志出现问题则为 FALSE 。
	:返回类型: bool

	使用 application/Config/Logger.php 中定义的日志处理程序记录日志。

	级别可为以下值: **emergency**, **alert**, **critical**, **error**, **warning**,
	**notice**, **info**, or **debug**.

	Context 可用于替换 message 字符串中的值。详情参见 the:doc:`Logging Information <logging>` 页。

.. php:function:: redirect( $uri[, ...$params ] )

	:param  string  $uri: 重定向URI。
	:param  mixed   $params: 在 :meth:RouteCollection::reverseRoute 方法中可使用单个或多个附加参数。

	这是方便的方法，它可以与当前的全局 $request 和 $router 实例一起重定向，使用命名路由/反向路由（named/reverse-routed）来确定要访问的 URL 。
	若没有发现则按惯常的重定向方式转向，让``$response->redirect()``判定适合的方法和代码。

	你需要使用更加明确的 ``$response->redirect() ``。

.. php:function:: redirect_with_input( $uri[, ...$params] )

	:param string $uri: 重定向URI。
	:param mixed  $params: 一个或更多附加参数可被用于 the :meth:`RouteCollection::reverseRoute` 方法。

	跟``redirect()``方法等同, 该session刷新的请求中的 $_GET 和 $_POST的值除外。
	在下一页的请求, 表单辅助类的 ``set_*`` 方法将首先检查旧的输入数据, 若没发现, 则当前的 GET/POST 将被检查。

	.. 注意:: 为了取回旧的值, session必须被启用，优先调用函数.

.. php:function:: remove_invisible_characters($str[, $url_encoded = TRUE])

	:param	string	$str: 输入字符串
	:param	bool	$url_encoded: 是否移除URL编码字符
	:返回:	已过滤的字符串
	:返回类型:	string

	这个函数防止在 ASCII 字符之间插入空字符(NULL)，例如 Java\\0script。

	范例::

		remove_invisible_characters('Java\\0script');
		// 返回: 'Javascript'

.. php:function:: route_to ( $method [, ...$params] )

	:param   string   $method: 命名路由别名, 或匹配controller/method名称。
	:param   mixed   $params: 一个或更多参数被传递到路由中匹配。

	以指定的路由别名或 controller::method 组合为依据生成一个相对 URI 。如果提供参数，将执行参数。

	详情参见 the :doc:`routing` 页。

.. php:function:: service ( $name [, ...$params] )

	:param   string   $name: 加载的服务名称
	:param   mixed    $params: 一个或多个参数传递到服务方法。
	:返回: 指定的服务类的实例。
	:返回类型: mixed

	提供简易访问任何在系统中定义的服务，详见the :doc:`Services <../concepts/services>` 。
	这将总是返回类的共享实例，因此不管在单个请求中调用多少次，都只会创建一个类实例。

	范例::

		$logger = service('logger');
		$renderer = service('renderer', APPPATH.'views/');

.. php:function:: single_service ( $name [, ...$params] )

	:param   string   $name: 加载的服务名称
	:param   mixed    $params: 一个或多个参数传递到服务方法。
	:返回: 指定的服务类的实例。
	:返回类型: mixed

	等同于前面所描述的 **service()** 函数, 除了所有调用该函数将返回一个类的新实例。
	 **service** 返回的是相同的实例。

.. php:function:: stringify_attributes ( $attributes [, $js] )

	:param   mixed    $attributes: 字符串, 键值对数组, 或者对象
	:param   boolean  $js: TRUE 若值不需要引用 (Javascript风格)
	:返回: 字符串包含键值对属性, 逗号分隔
	:返回类型: string

	辅助函数用于转换字符串, 数组, 或者字符串的对象属性。


================
全局常量
================

以下的常量在你的应用中的任何地方有效。

核心常量
==============

.. php:const:: ROOTPATH

	主应用目录路径. 如前述的 ``public``.

.. php:const:: APPPATH

	**application** 目录的路径。

.. php:const:: BASEPATH

	**system** 目录的路径。

.. php:const:: FCPATH

	保存的前端控制器目录的路径。

.. php:const:: SELF

	前端控制器的路径, **index.php**.

.. php:const:: WRITEPATH

	**writable** 目录的路径。


时间常量
==============

.. php:const:: SECOND

	等于 1.

.. php:const:: MINUTE

	等于 60.

.. php:const:: HOUR

	等于 3600.

.. php:const:: DAY

	等于 86400.

.. php:const:: WEEK

	等于 604800.

.. php:const:: MONTH

	等于 2592000.

.. php:const:: YEAR

	等于 31536000.

.. php:const:: DECADE

	等于 315360000.
