#################
CURLRequest类
#################

``CURLRequest`` 类是一个轻量级的基于 CURL 的 HTTP 客户端，用于同其他网站和服务器进行沟通。该类可用于获取谷歌搜索的内容，抓取一个网站页面或一个图片，
或者是用来同 API 进行信息传递等诸多功能。

.. contents::
    :local:
    :depth: 2

该类模仿了 `Guzzle HTTP Client <http://docs.guzzlephp.org/en/latest/>`_ 库，因为该库被广泛应用于多方面。
我们尽可能地与 Guzzle 保持语法一致，不过如果你需要一些额外的功能的话（比如该类并未提供的功能之类的），可能需要稍微更改一下语法来使用 Guzzle 库。

.. note:: 该类需要安装你的 PHP 版本的 `cURL 库 <https://www.php.net/manual/en/book.curl.php>`_ 。该库是一个在大多数情况下都广泛被使用的库，但不是所有服务器都安装了它。
    因此请检查你的服务器上安装了该库以解决依赖问题。

*******************
加载该类库
*******************

该类库可以通过手动加载或者通过 :doc:`服务类 </concepts/services>` 加载。

通过服务类来加载 ``curlrequest()`` 方法::

	$client = \Config\Services::curlrequest();

你可以将一个默认选项数组作为参数传递给该方法作为第一个参数，用于修改 cURL 处理请求的方式。选项描述如下::

	$options = [
		'base_uri' => 'http://example.com/api/v1/',
		'timeout'  => 3
	];
	$client = \Config\Services::curlrequest($options);

当手动创建类实例时，你需要传递一些依赖。第一个参数是 ``Config\App`` 类的实例。第二个参数是一个 URI 实例。第三个参数是一个 Response 类的对象。
第四个参数是一个可选的 ``$options`` 数组::

	$client = new \CodeIgniter\HTTP\CURLRequest(
		new \Config\App(),
		new \CodeIgniter\HTTP\URI(),
		new \CodeIgniter\HTTP\Response(new \Config\App()),
		$options
	);

************************
使用该类库
************************

处理 CURL 请求基本上只是创建一个 Request 请求并获取 :doc:`Response 对象 </outgoing/response>` 的过程。这一过程就是用来处理数据交换的。
这一过程后，你可以对获得的信息进行完全自定义的处理.

发送请求
===============

大多数交流会话是通过 ``request()`` 方法进行的，该方法触发请求并返回一个 Response 实例。该方法将 HTTP 动词， URL 信息和选项数组作为请求参数。::

	$client = \Config\Services::curlrequest();

	$response = $client->request('GET', 'https://api.github.com/user', [
		'auth' => ['user', 'pass']
	]);

由于该响应是 ``CodeIgniter\HTTP\Response`` 类的一个实例对象，故而可以通过调用该类的对应方法::

	echo $response->getStatusCode();
	echo $response->getBody();
	echo $response->getHeader('Content-Type');
	$language = $response->negotiateLanguage(['en', 'fr']);

尽管 ``request()`` 方法非常灵活，你也可以使用以下的简称方法。
这些方法将 URL 作为第一个参数并将选项数组作为第二个参数::

* $client->get('http://example.com');
* $client->delete('http://example.com');
* $client->head('http://example.com');
* $client->options('http://example.com');
* $client->patch('http://example.com');
* $client->put('http://example.com');
* $client->post('http://example.com');

base_uri （基础 URI ）
---------------------------

``base_uri`` 可以在该类实例化时作为一个选项进行设置。
该参数使得你可以设置一个基础 URI ，并在该实例对象进行请求时使用相对 URL 路径。这一操作在和 API 通信时特别管用::

	$client = \Config\Services::curlrequest([
		'base_uri' => 'https://example.com/api/v1/'
	]);

	// GET http:example.com/api/v1/photos
	$client->get('photos');

	// GET http:example.com/api/v1/photos/13
	$client->delete('photos/13');

当 ``request()`` 方法或者其他简称方法接受相对 URI 作为参数时，就会将 base_uri 和该相对 URI 根据 `RFC 2986, section 2 <https://tools.ietf.org/html/rfc3986#section-5.2>`_ 进行组合
以下是一些组合的例子

	=====================   ================   ========================
	base_uri                URI                Result
	=====================   ================   ========================
	`http://foo.com`        /bar               `http://foo.com/bar`
	`http://foo.com/foo`    /bar               `http://foo.com/bar`
	`http://foo.com/foo`    bar                `http://foo.com/bar`
	`http://foo.com/foo/`   bar                `http://foo.com/foo/bar`
	`http://foo.com`        `http://baz.com`   `http://baz.com`
	`http://foo.com/?bar`   bar                `http://foo.com/bar`
	=====================   ================   ========================

使用响应
===============
每个 ``request()`` 函数调用都会返回一个包含有许多有用信息和方法的 Response 实例对象。最通用的方法使得你可以定制化地处理响应对象本身。

你可以获取响应的状态码以及状态原因::

	$code   = $response->getStatusCode();    // 200
	$reason = $response->getReason();      // OK

你可以获取响应头::

	// 获取一个响应头的内容
	echo $response->getHeaderLine('Content-Type');

	// 获取所有响应头
	foreach ($response->getHeaders() as $name => $value)
	{
		echo $name .': '. $response->getHeaderLine($name) ."\n";
	}

响应体可以通过 ``getBody()`` 方法来获取::

	$body = $response->getBody();

响应体是远端服务器提供的原生响应内容。如果内容类型需要格式化的话，你需要保证在代码中这样处理::

	if (strpos($response->getHeader('content-type'), 'application/json') !== false)
	{
		$body = json_decode($body);
	}

***************
请求选项
***************

本节描述了在构造函数， ``request()`` 方法以及所有简称方法中可以传递的所有可用选项。

allow_redirects
===============

默认情况下， CURL 会遵循远端服务器返回的所有的 "Location:" 响应头规则。 ``allow_redirects`` 选项使得你可以修改这一执行过程。

如果该值被设为 ``false`` ，就不会执行任何的重定向规则。

	$client->request('GET', 'http://example.com', ['allow_redirects' => false]);

设为 ``true`` 时就会执行请求的默认设置::

	$client->request('GET', 'http://example.com', ['allow_redirects' => true]);

	// 设置以下默认选项:
	'max'       => 5, // 终止前最多的重定向次数
	'strict'    => true, // 在重定向过程中确保发送的 POST 请求始终保持为 POST （译注：某些服务器会在重定向时修改请求方法，例如 304 重定向时修改请求方式为 GET)
	'protocols' => ['http', 'https'] // 限制重定向使用一个或多个协议

你可以为 ``allow_redirects`` 选项传递一个选项数组用于重定向时使用新的设置，而不是默认设置::

	$client->request('GET', 'http://example.com', ['allow_redirects' => [
		'max'       => 10,
		'protocols' => ['https'] // Force HTTPS domains only.
	]]);

.. note:: 当 PHP 在 safe_mode 或者 open_basedir 选项开启时，不会进行重定向。

auth
====

使得你可以为 `HTTP Basic <https://www.ietf.org/rfc/rfc2069.txt>`_ 和 `Digest <https://www.ietf.org/rfc/rfc2069.txt>`_ 和认证过程提供细节信息。
你的脚本文件需要执行额外操作以支持诊断认证——只需要在访问时传递用户名和密码。第三个参数是认证的类型，可以是 ``basic`` 或者 ``digest``::

	$client->request('GET', 'http://example.com', ['auth' => ['username', 'password', 'digest']]);

body
====

对于支持请求体的方法，例如 PUT 或者是 POST 来说，有两种方法来设置请求体。
第一种是使用 ``setBody()`` 方法::

	$client->setBody($body)
	       ->request('put', 'http://example.com');

第二种方法是通过传递一个 ``body`` 选项。该方式是为了与 Guzzle 兼容起见的，并提供了和上述方式一样的功能。该值必须是一个字符串::

	$client->request('put', 'http://example.com', ['body' => $body]);

cert
====

指定一个 PEM 格式的客户端证书的位置，通过为 ``cert`` 选项来传递绝对路径的方式来实现。
如果需要密码的话，为该选项数组的第一个元素的值为路径，第二个元素的值设为密码::

    $client->request('get', '/', ['cert' => ['/path/getServer.pem', 'password']);

connect_timeout
===============

默认情况下， CodeIgniter 并未对 cURL 尝试连接一个网站的时间进行限制。
如果你需要修改这个值，可以通过为 ``connect_timeout`` 选项提供时间秒数值的方式来进行。传值为0时，无限等待::

	$response->request('GET', 'http://example.com', ['connect_timeout' => 0]);

cookie
======

该选项指定了 CURL 用于存取 cookie 值的文件名。这一过程通过使用 CURL_COOKIEJAR 和 CURL_COOKIEFILE 选项来实现。
例如::

	$response->request('GET', 'http://example.com', ['cookie' => WRITEPATH . 'CookieSaver.txt']);

debug
=====

当 ``debug`` 被传递并设为 ``true`` 时，就会启动额外的调试模式并在脚本执行时输出标准错误流信息( STDERR )。
该操作是通过传递 CURLOPT_VERBOSE 并返回输出来实现的。
因此当你需要利用 ``spark serve`` 运行一个内置服务器时，将会看到命令行中的输出内容。否则输出就会被写入到服务器的错误日志中::

	$response->request('GET', 'http://example.com', ['debug' => true]);

可以通过将文件名作为参数传入的方式，将输出写入到文件中::

	$response->request('GET', 'http://example.com', ['debug' => '/usr/local/curl_log.txt']);

delay
=====

使得你可以在发送请求前延迟指定的毫秒时间::

	// 延时2秒
	$response->request('GET', 'http://example.com', ['delay' => 2000]);

form_params
===========

你可以通过为 ``form_params`` 选项传递关联数组的方式，在一个 application/x-www-form-urlencoded POST 请求里发送表单数据。
该操作会将 ``Content-Type`` 请求头强制设为 ``application/x-www-form-urlencoded`` ::

	$client->request('POST', '/post', [
		'form_params' => [
			'foo' => 'bar',
			'baz' => ['hi', 'there']
		]
	]);

.. note:: ``form_params`` 不能和 ``multipart`` 选项一起使用。你可以非此即彼地使用这两个选项。``form_params`` 用于 ``application/x-www-form-urlencoded`` 请求，而 ``multipart`` 用于 ``multipart/form-data`` 请求。

headers
=======

尽管你可以通过 ``setHeader()`` 方法来传递任何请求头，你也可以通过为选项传递关联数组作为参数的方式来实现自定义请求头。
该关联数组中每个键都是请求头的名字，而值就是一个字符串或者是一个字符串数组，包括着请求头字段的值::

	$client->request('get', '/', [
		'headers' => [
			'User-Agent' => 'testing/1.0',
			'Accept'     => 'application/json',
			'X-Foo'      => ['Bar', 'Baz']
		]
	]);

如果请求头在构造函数中被传入时，就会被设为默认选项。而默认选项会被后续设置的选项或者 ``setHeader()`` 的调用所覆盖。

http_errors
===========

默认情况下，CURLRequest 类会在 HTTP 状态码大于等于400时结束请求并报错。
你可以通过将 ``http_errors`` 选项设为 ``false`` 的方式来返回内容::

    $client->request('GET', '/status/500');
    // 自动失败报错

    $res = $client->request('GET', '/status/500', ['http_errors' => false]);
    echo $res->getStatusCode();
    // 500

json
====

``json`` 选项用于上传 JSON 编码的数据作为请求体。同时会在请求头上加入 Content-Type 为 ``application/json`` 。
并覆盖先前设置的 Content-Type 请求头。传递给该选项的参数可以是任何 ``json_encode()`` 函数所接受的参数::

	$response = $client->request('PUT', '/put', ['json' => ['foo' => 'bar']]);

.. note:: 该选项不允许对 ``json_encode()`` 和 Content-Type 请求头进行自定义地修改。如果你需要这一功能，
        就需要手动编码数据并将其传递给 CURLRequest 类的 ``setBody()`` 方法，并通过 ``setHeader()`` 方法来设置 Content-Header 请求头。

multipart
=========

如果你想通过 POST 请求来发送文件或者其他数据时，可以使用 ``multipart`` 选项和 `CURLFile 类 <https://www.php.net/manual/en/class.curlfile.php>`_ 。
该选项的值应当是一个需要关联数组，包含有需要发送的数据。为了安全起见，上传文件时在前缀上加上 `@` 的遗留方法已被禁止。你所需要发送的文件应当以 CURLFile 类的实例的方式传递::

	$post_data = [
		'foo'      => 'bar',
		'userfile' => new \CURLFile('/path/to/file.txt')
	];

.. note:: ``multipart`` 不能和 ``form_params`` 选项一起使用。你可以非此即彼地使用这两个选项。
        ``form_params`` 用于 ``application/x-www-form-urlencoded`` 请求，而 ``multipart`` 用于 ``multipart/form-data`` 请求。

query
=====

你可以通过为 ``query`` 选项传递一个关联数组的方式来发送查询字符串信息::

	// 发送一个 GET 请求来获取 /get?foo=bar 的结果
	$client->request('GET', '/get', ['query' => ['foo' => 'bar']]);

timeout
=======

默认情况下， cURL 函数可以执行任意长的时间，不受时间限制。你可以通过 ``timeout`` 选项来修改这一过程。选项值是你需要这个函数运行的时间。使用0来无限等待::

	$response->request('GET', 'http://example.com', ['timeout' => 5]);

verify
======

该选项描述了 SSL 验证鉴权行为。
如果 ``verify`` 选项被设为 ``true`` ，就开始 SSL 鉴权操作并使用系统提供默认的 CA 包文件。如果设为 ``false`` ，就会禁用鉴权操作（这一行为不安全，并可能导致中间人攻击！）。
你可以将该参数设为一个 CA 包文件所在的路径，从而进行自定义的鉴权操作。该选项默认值为 true ::

	// 使用系统的 CA 包文件（默认设置）
	$client->request('GET', '/', ['verify' => true]);

	// 使用硬盘上的一个自定义的 SSL 鉴权文件
	$client->request('GET', '/', ['verify' => '/path/to/cert.pem']);

	// 完全禁用鉴权（不安全！）
	$client->request('GET', '/', ['verify' => false]);

version
=======

你可以通过为版本参数传递一个字符串或者浮点数（特别是1.0，或1.1，尚未支持2.0）的方式来设置协议版本::

	// 强制使用 HTTP/1.0
	$client->request('GET', '/', ['version' => 1.0]);
