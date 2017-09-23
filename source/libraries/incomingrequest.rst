=====================
IncomingRequest 类
=====================

IncomingRequest 类提供了一个客户端（比如 浏览器）HTTP 请求的面向对象封装。
基于它可以访问所有 :doc:`Request </libraries/request>` 和 :doc:`Message </libraries/message>` 中的方法， 以及以下列出的方法。


.. contents:: 目录

获得请求
=====================

如果当前控制器继承了 ``CodeIgniter\Controller``，则一个 Request 类的实例已被初始化并可作为属性被使用::

	class UserController extends CodeIgniter\Controller
	{
		public function index()
		{
			if ($this->request->isAJAX())
			{
				. . .
			}
		}
	}

如果在控制器外使用 Request 对象，可以通过 :doc:`Services class </concepts/services>` 获得实例::

	$request = \Config\Services::request();

推荐将 Request 对象作为一个依赖注入到当前类中并保存为一个属性::

	use CodeIgniter\HTTP\RequestInterface;

	class SomeClass
	{
		protected $request;

		public function __construct(RequestInterface $request)
		{
			$this->request = $request;
		}
	}

	$someClass = new SomeClass(\Config\Services::request());


判断请求类型
========================

请求有多种来源，包含使用 AJAX 发起和使用 CLI 发起的。可通过 ``isAJAX()`` and ``isCLI()`` 来检测::

	// Check for AJAX request.
	if ($request->isAJAX())
	{
		. . .
	}

	// Check for CLI Request
	if ($request->isCLI())
	{
		. . .
	}

你可以检测请求的 HTTP 类型 :: 

	// Returns 'post'
	$method = $request->getMethod();

该方法默认返回类型是小写的字符串 （比如 'get', 'post' 等等），你可以通过传递 ``true`` 参数来获得大写的返回结果::

	// Returns 'GET'
	$method = $request->getMethod(true);

还可以通过 ``isSecure()`` 方法检测请求是否是 HTTPS::

	if (! $request->isSecure())
	{
		force_https();
	}


数据读取
================

你可以通过 Request 对象读取 $_SERVER, $_GET, $_POST, $_ENV, $_SESSION 内的信息。
因为输入数据不会自动过滤，只会返回请求时的原始数据。而使用这些方法去替代直接获取数据的（比如 $_POST['something']）主要优点是当参数不存在时会返回 null ，而且你还能做数据过滤。这可以使你很方便的直接使用 数据而不需要先去判断某个参数是否存在。换句话说，一般情况下你以前会这么做:: 

	$something = isset($_POST['foo']) ? $_POST['foo'] : NULL;

而使用 CodeIgniter 的内建方法你可以很简单的做到同样的事::

	$something = $request->getVar('foo');

因为 ``getVar()`` 方法从 $_REQUEST 获得数据，所以使用它可以获得 $_GET, $POST, $_COOKIE 内的数据。虽然这很方便，但是你有时也需要使用一些特定的方法，比如::

* ``$request->getGet()``
* ``$request->getPost()``
* ``$request->getServer()``
* ``$request->getCookie()``

另外，还有一些实用的方法可以同时获取 $_GET 或者 $_POST 的数据，因为有获取顺序的问题，我们提供了以下方法::

* ``$request->getPostGet()`` - 先 $_POST, 后 $_GET
* ``$request->getGetPost()`` - 先 $_GET, 后 $_POST

**获取JSON数据**

你可以使用 ``getJSON()`` 去获取 php://input 传递的 JSON 格式的数据。

.. note::  因为无法检测来源数据是否具有有效的JSON格式，所以只有当你确认数据来源格式是JSON后才可使用。

::

	$json = $request->getJSON();

默认情况下，这会返回一个 JSON 数据对象。如果你需要一个数据，请传递 ``true`` 作为第一个参数。

该方法的第二和第三个参数则分别对应 `json_decode <http://php.net/manual/en/function.json-decode.php>`_ 方法的 ``depth`` 和 ``options`` 参数.

**获取原始数据 （获取 Method 为 PUT, PATCH, DELETE 传递的数据）**

最后，你可以通过 ``getRawInput()`` 去获取 php://input 传递的原始数据。

	$data = $request->getRawInput();

这会返回数据并转换为数组。比如::

	var_dump($request->getRawInput());

	[
		'Param1' => 'Value1',
		'Param2' => 'Value2'
	]

数据过滤
--------------------

为了保证应用程序的安全，必须过滤所有输入的数据。你可以传递过滤类型到方法的最后一个参数里。会调用系统方法 ``filter_var()`` 去过滤。具体过滤类型可以参考 PHP 手册里的列表 `valid
filter types <http://php.net/manual/en/filter.filters.php>`_.

过滤一个 POST 变量可以这么做::

	$email = $request->getVar('email', FILTER_SANITIZE_EMAIL);

以上提到的方法中除了 ``getJSON()`` 和 ``getRawInput()`` ，都支持给最后一个参数传递类型来实现过滤。

获取数据头
==================

你可以通过 ``getHeaders()`` 方法获得请求的数据头，该方法会以数组形式返回所有的数据头信息，数据的键值为数据头名称，值则为一个 ``CodeIgniter\HTTP\Header`` 的实例::

	var_dump($request->getHeaders());

	[
		'Host' => CodeIgniter\HTTP\Header,
		'Cache-Control' => CodeIgniter\HTTP\Header,
		'Accept' => CodeIgniter\HTTP\Header,
	]

如果你只是想获得某个头的信息，你可以将数据头名称作为参数传递给 ``getHeader()`` 方法。数据头名称无视大小写，如果存在则返回指定头信息。如果不存在则返回 ``null`` ::

	// 以下这些效果一样
	$host = $request->getHeader('host');
	$host = $request->getHeader('Host');
	$host = $request->getHeader('HOST');

你可以使用 ``hasHeader()`` 去判断请求头是否存在::

	if ($request->hasHeader('DNT'))
	{
		// Don't track something...
	}

如果你需要某个头的值并在一行字符串内输出，可以使用 ``getHeaderLine()`` 方法::

	// Accept-Encoding: gzip, deflate, sdch
    echo 'Accept-Encoding: '.$request->getHeaderLine('accept-encoding');

如果你需要完整头信息，输出包括全部名称和值的字符串，可以使用如下方法做转换::

	echo (string)$header;


请求地址
===============

你可以通过访问 ``$request->uri`` 属性获取代表当前访问信息的 doc:`URI <uri>` 对象。通过以下方法获取当前请求的完整访问地址::

	$uri = (string)$request->uri;

该对象赋予了你访问全部请求信息的能力::

	$uri = $request->uri;

	echo $uri->getScheme();         // http
	echo $uri->getAuthority();      // snoopy:password@example.com:88
	echo $uri->getUserInfo();       // snoopy:password
	echo $uri->getHost();           // example.com
	echo $uri->getPort();           // 88
	echo $uri->getPath();           // /path/to/page
	echo $uri->getQuery();          // foo=bar&bar=baz
	echo $uri->getSegments();       // ['path', 'to', 'page']
	echo $uri->getSegment(1);       // 'path'
	echo $uri->getTotalSegments();  // 3

上传文件
==============

所有上传文件的信息可以通过 ``$request->getFiles()`` 方法获得，该方法会返回一个 :doc:`FileCollection </libraries/uploaded_files>` 实例。这会有助于减少处理文件上传的工作量，以及使用最佳方案去降低安全风险。
::

	$files = $request->getFiles();

	// Grab the file by name given in HTML form
	if ($files->hasFile('uploadedFile')
	{
		$file = $files->getFile('uploadedfile');

		// Generate a new secure name
		$name = $file->getRandomName();

		// Move the file to it's new home
		$file->move('/path/to/dir', $name);

		echo $file->getSize('mb');      // 1.23
		echo $file->getExtension();     // jpg
		echo $file->getType();          // image/jpg
	}

你也可以通过HTML中提交的文件名去获取单个上传文件::

	$file = $request->getFile('uploadedfile');

内容协商
===================

你可以很轻松的通过 ``negotiate()`` 方法来完成信息内容类型的协商::

	$language    = $request->negotiate('language', ['en-US', 'en-GB', 'fr', 'es-mx']);
	$imageType   = $request->negotiate('media', ['image/png', 'image/jpg']);
	$charset     = $request->negotiate('charset', ['UTF-8', 'UTF-16']);
	$contentType = $request->negotiate('media', ['text/html', 'text/xml']);
	$encoding    = $request->negotiate('encoding', ['gzip', 'compress']);

查看 :doc:`Content Negotiation </libraries/content_negotiation>` 获得更多细节。

***************
类信息参考
***************

.. note:: 除了这里列出的，本类还继承了 :doc:`Request Class </libraries/request>`  和 :doc:`Message Class </libraries/message>` 的方法。

以下方法由父类提供::

* :meth:`CodeIgniter\\HTTP\\Request::getIPAddress`
* :meth:`CodeIgniter\\HTTP\\Request::validIP`
* :meth:`CodeIgniter\\HTTP\\Request::getMethod`
* :meth:`CodeIgniter\\HTTP\\Request::getServer`
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

.. php:class:: CodeIgniter\\HTTP\\IncomingRequest

	.. php:method:: isCLI()

		:returns: 由命令行发起的请求会返回 true ，其他返回 false。
		:rtype: bool

	.. php:method:: isAJAX()

		:returns: AJAX请求返回 true ，其他返回 false。
		:rtype: bool

	.. php:method:: isSecure()

		:returns: HTTPS请求返回 true ，其他返回 false。
		:rtype: bool

	.. php:method:: getVar([$index = null[, $filter = null[, $flags = null]]])

		:param  string  $index: 需要查找的数据名。
		:param  int     $filter: 过滤类型。参见列表 `查看 <http://php.net/manual/en/filter.filters.php>`_。
		:param  int     $flags: 过滤器名，值为过滤器的预定义变量名。 参见列表 `查看 <http://php.net/manual/en/filter.filters.flags.php>`_。
		:returns: 不传参数会返回 REQUEST 中的所有元素，传参并且参数存在则返回对应的 REQUEST 值，不存在返回 null
		:rtype: mixed|null

		第一个参数包含需要查找的数据名 ::

			$request->getVar('some_data');

		如数据不存在则返回 null 。

		只需传递期望的过滤类型到第二个参数，就可以帮助你完成数据过滤 ::

			$request->getVar('some_data', FILTER_SANITIZE_STRING);

		不传任何参数会得到一个包含全部 REQUEST 数据的数组。

		第一个参数 null ，第二个参数设置过滤类型，可获得一个被过滤的包涵全部 REQUEST 数据的数组 ::

			$request->getVar(null, FILTER_SANITIZE_STRING); // returns all POST items with string sanitation

		获取多个键值的信息，可以将需要的键值以数组形式传递给第一个参数 ::

			$request->getVar(['field1', 'field2']);

		与之前一样，此时传递过滤类型给第二个参数，也可获得过滤后的数据 ::

			$request->getVar(['field1', 'field2'], FILTER_SANITIZE_STRING);

	.. php:method:: getGet([$index = null[, $filter = null[, $flags = null]]])

		:param  string  $index: 需要查找的数据名。
		:param  int     $filter: 过滤类型。参见列表 `查看 <http://php.net/manual/en/filter.filters.php>`_。
		:param  int     $flags: 过滤器名，值为过滤器的预定义变量名。 参见列表 `查看 <http://php.net/manual/en/filter.filters.flags.php>`_。
		:returns: 不传参数会返回 GET 中的所有元素，传参并且参数存在则返回对应的 GET 值，不存在返回 null
		:rtype: mixed|null

		该方法与 ``getVar()`` 类似, 只返回 GET 的数据。

	.. php:method:: getPost([$index = null[, $filter = null[, $flags = null]]])

		:param  string  $index: 需要查找的数据名。
		:param  int     $filter: 过滤类型。参见列表 `查看 <http://php.net/manual/en/filter.filters.php>`_。
		:param  int     $flags: 过滤器名，值为过滤器的预定义变量名。 参见列表 `查看 <http://php.net/manual/en/filter.filters.flags.php>`_。
		:returns: 不传参数会返回 POST 中的所有元素，传参并且参数存在则返回对应的 POST 值，不存在返回 null
		:rtype: mixed|null

		该方法与 ``getVar()`` 类似, 只返回 POST 的数据。

	.. php:method:: getPostGet([$index = null[, $filter = null[, $flags = null]]])

		:param  string  $index: 需要查找的数据名。
		:param  int     $filter: 过滤类型。参见列表 `查看 <http://php.net/manual/en/filter.filters.php>`_。
		:param  int     $flags: 过滤器名，值为过滤器的预定义变量名。 参见列表 `查看 <http://php.net/manual/en/filter.filters.flags.php>`_。
		:returns: 不传参数会返回 POST／GET 中的所有元素，传参并且参数存在则返回对应的 POST／GET 值，不存在返回 null
		:rtype: mixed|null

		该方法和 ``getPost()``，``getGet()`` 类似，它会同时查找 POST 和 GET 两个数组来获取数据， 先查找 POST ，再查找 GET::

			$request->getPostGet('field1');

	.. php:method:: getGetPost([$index = null[, $filter = null[, $flags = null]]])

		:param  string  $index: 需要查找的数据名。
		:param  int     $filter: 过滤类型。参见列表 `查看 <http://php.net/manual/en/filter.filters.php>`_。
		:param  int     $flags: 过滤器名，值为过滤器的预定义变量名。 参见列表 `查看 <http://php.net/manual/en/filter.filters.flags.php>`_。
		:returns: 不传参数会返回 POST／GET 中的所有元素，传参并且参数存在则返回对应的 POST／GET 值，不存在返回 null
		:rtype: mixed|null

		该方法和 ``getPost()``，``getGet()`` 类似，它会同时查找 POST 和 GET 两个数组来获取数据， 先查找 GET ，再查找 POST::

			$request->getGetPost('field1');

	.. php:method:: getCookie([$index = null[, $filter = null[, $flags = null]]])

		:param  string  $index: COOKIE 名。
		:param  int     $filter: 过滤类型。参见列表 `查看 <http://php.net/manual/en/filter.filters.php>`_。
		:param  int     $flags: 过滤器名，值为过滤器的预定义变量名。 参见列表 `查看 <http://php.net/manual/en/filter.filters.flags.php>`_。
		:returns: 不传参数会返回 COOKIE 中的所有元素，传参并且参数存在则返回对应的 COOKIE 值，不存在返回 null
		:rtype: mixed

		该方法与 ``getPost()``，``getGet()`` 类似, 只返回 COOKIE 的数据 ::

			$request->getCookie('some_cookie');
			$request->getCookie('some_cookie', FILTER_SANITIZE_STRING); // with filter

		获取多个键值的信息，可以将需要的键值以数组形式传递给第一个参数 ::

			$request->getCookie(array('some_cookie', 'some_cookie2'));

		.. note:: 与 :doc:`Cookie Helper <../helpers/cookie_helper>`
			function :php:func:`get_cookie()` 不同, 该方法不会自动添加配置中 ``$config['cookie_prefix']`` 的值。

	.. php:method:: getServer([$index = null[, $filter = null[, $flags = null]]])

		:param  string  $index: 服务器信息名。
		:param  int     $filter: 过滤类型。参见列表 `查看 <http://php.net/manual/en/filter.filters.php>`_。
		:param  int     $flags: 过滤器名，值为过滤器的预定义变量名。 参见列表 `查看 <http://php.net/manual/en/filter.filters.flags.php>`_。
		:returns: 不传参数会返回 SERVER 中的所有元素，传参并且参数存在则返回对应的 SERVER 值，不存在返回 null
		:rtype: mixed

		该方法与 ``getPost()``，``getGet()`` ，``getCookie()`` 类似, 只返回 SERVER 的数据 ::

			$request->getServer('some_data');

		获取多个键值的信息，可以将需要的键值以数组形式传递给第一个参数 ::

			$request->getServer(['SERVER_PROTOCOL', 'REQUEST_URI']);

	.. php:method:: getUserAgent([$filter = null])

		:param  int  $filter: 过滤类型。参见列表 `查看  <http://php.net/manual/en/filter.filters.php>`_。
		:returns:  包含 User Agent 信息的字符串，不存在返回 null
		:rtype: mixed

		该方法从服务器信息哪查找并以字符串形式返回 User Agent ::

			$request->getUserAgent();
