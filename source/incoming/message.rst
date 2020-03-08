=============
HTTP 消息
=============

消息类为HTTP消息中的请求和响应的实现提供了一个通用的接口，包括消息体，协议版本，处理消息头的工具和一些进行内容协商的方法。

该类是 :doc:`请求类 </incoming/request>` 和 :doc:`响应类 </outgoing/response>` 共有的父类。
因此某些方法，例如内容协商方法等，可能只适用于请求和响应，而对于其他方法不适用，但是我们将其聚合在该类中
从而使得处理头的方法可以定义在相同的位置。

什么是内容协商
============================

内容协商的核心机制，其实只是HTTP实现的一个简单的部分，即允许单个资源适用于不止一种内容类型，从而允许客户端选择适合自己的数据类型。

一个典型的案例就是，该浏览器无法播放PNG格式的文件，并且只能请求GIF或者JPEG格式的图片文件。而当资源服务器接收到该请求时，
它将会检查可用的文件类型是否能满足客户端所请求的，并选择本身所支持的格式中，最为适合的图片格式，在本例中就可能会返回一个JPEG的图片文件。

同样的协商方式会在以下四种数据类型中提现:

* **媒体/文档类型** - 可以是图片的类型格式，或者是HTML、XML或JSON.
* **字符集Character Set** - 该文档所属的字符集，通常是UTF-8
* **文档编码Document Encoding** - 通常是返回结果的压缩类型（译者注：例如gzip）
* **文档语言Document Language** - 对于支持多语言的站点，有助于决定返回哪种语言格式

***************
类的参考文档
***************

.. php:class:: CodeIgniter\\HTTP\\Message

	.. php:method:: body()

		:returns: 当前的消息体
		:rtype: string

		返回当前消息的实体部分，如果实体不存在或者已经被发送过，返回null::

			echo $message->body();

	.. php:method:: setBody([$str])

	   :param  string  $str: 消息体对应的字符串.
	   :returns: 该消息实例，用于链式调用
	   :rtype: CodeIgniter\\HTTP\\Message 实例.

		设置当前请求的实体内容

	.. php:method:: populateHeaders()

		:returns: void

		扫描并处理SERVER数据中找到的请求头内容，并将其存储以供下次使用。该方法用于 :doc:`请求类 Class </incoming/incomingrequest>` 从而使得当前的请求头内容可被使用.

                这里所指的请求头实际上是所有以 ``HTTP_`` 开头的SERVER数据，例如 ``HTTP_POST`` 。每个消息都会从被从标准的大小写格式转换为首字母大写并以横线(-)连接的格式。
		并移除了开头的 ``HTTP_`` 部分，故而 ``HTTP_ACCEPT_LANGUAGE`` 变成了 ``Accept-Language`` 。

	.. php:method:: getHeaders()

		:returns: 一个包括了所有能确定的头部的数组.
		:rtype: array

		返回所有能确定或者是先前设定过的头

	.. php:method:: getHeader([$name[, $filter = null]])

		:param  string  $name: 你想要获取对应的值的头的名字
		:param  int  $filter: 所需要使用的过滤器类型。可供使用的过滤器见表 `过滤器 <https://www.php.net/manual/en/filter.filters.php>`_ 。
		:returns: 当前头的值。如果该头有多个值，就会以数组的形式返回
		:rtype: string|array|null

		使你可以获取单个消息头的当前值。 ``$name`` 对应的是大小写敏感的头名。由于在上述例子中已经对头进行了内部转换，你可以通过任何大小写方式格式来传值::

			// 这些都等同:
			$message->getHeader('HOST');
			$message->getHeader('Host');
			$message->getHeader('host');

		如果该头有多个值，就会以数组的形式返回. 你可以使用 ``headerLine()`` 方法来将这些数据转换为字符串的形式来返回::

			echo $message->getHeader('Accept-Language');

			// 输出如下:
			[
				'en',
				'en-US'
			]

		你可以通过将过滤器的值作为第二个参数传递给该函数::

			$message->getHeader('Document-URI', FILTER_SANITIZE_URL);

	.. php:method:: headerLine($name)

		:param  string $name: 需要获取的头的名字.
		:returns: 头所对应的值（字符串形式）
		:rtype: string

		将该头对应的值以字符串形式返回。该方法使得你可以在该头对应多个值时，将头对应的值轻松地以字符串形式返回。值以逗号分隔形式::

			echo $message->headerLine('Accept-Language');

			// 输出:
			en, en-US

	.. php:method:: setHeader([$name[, $value]])
                :noindex:

		:param string $name: 需要设置值的头的名字
		:param mixed  $value: 需要设置的值
		:returns: 当前消息实例
		:rtype: CodeIgniter\\HTTP\\Message

	为单个头赋值。 ``$name`` 是该头所对应的大小写敏感的命名。如果该头部当前不存在就会被创建。``$value`` 可以是字符串或者一个字符串数组::

			$message->setHeader('Host', 'codeigniter.com');

	.. php:method:: removeHeader([$name])

		:param string $name: 需要移除的头的名字.
		:returns: 当前消息实例
		:rtype: CodeIgniter\\HTTP\\Message

		从消息中移除指定头. ``$name`` 是该头所对应的大小写敏感的命名::

			$message->remove('Host');

	.. php:method:: appendHeader([$name[, $value]]))

		:param string $name:  需要修改的头的名字
		:param mixed  $value: 需要为该头增加的值
		:returns: 当前消息实例
		:rtype: CodeIgniter\\HTTP\\Message

		为一个现存的头增加值。该头的值不可以是单个字符串，必须是一个数组。如果是单个字符串的话会抛出一个 LogicException 异常
		::

			$message->appendHeader('Accept-Language', 'en-US; q=0.8');

	.. php:method:: protocolVersion()

		:returns: 当前HTTP协议版本
		:rtype: string

		返回当前消息对应的HTTP 协议版本，如果没有设定过的话就会返回 ``null`` ，可选值为 ``1.0`` 和 ``1.1`` 。

	.. php:method:: setProtocolVersion($version)

		:param string $version: HTTP协议版本
		:returns: 当前消息实例
		:rtype: CodeIgniter\\HTTP\\Message

		为当前消息所使用的HTTP协议设定版本。可赋值为 ``1.0`` 或 ``1.1``::

			$message->setProtocolVersion('1.1');

	.. php:method:: negotiateMedia($supported[, $strictMatch=false])

		:param array $supported: 系统所支持的媒体类型构成的数组
		:param bool $strictMatch: 是否需要严格匹配
		:returns: 对于所请求的媒体格式，返回程序支持的媒体类型
		:rtype: string

		用于处理 ``Accept`` 请求头并将其与应用程序所支持的媒体类型进行对比来给出最合适的类型。本方法会返回一个合适的媒体类型，第一个参数是应用程序所支持的类型，用于和客户端所请求的类型进行比对::

			$supported = [
				'image/png',
				'image/jpg',
				'image/gif'
			];
			$imageType = $message->negotiateMedia($supported);

		``$supported`` 数组里成员的顺序应该以程序优先返回的顺序进行定义，其中第一个成员应该是应用程序所期待的返回类型，其余降序排列。如果和请求的类型匹配不上，就默认返回数组里的第一个成员。

		根据 `RFC <https://tools.ietf.org/html/rfc7231#section-5.3>`_ ，协商匹配可以选择以返回一个默认值（就如该方法所做的那样），或者是返回一个空字符串。如果你希望进行严格匹配并返回一个空字符串的话，请为第二个参数传值 ``true`` ::

			// 如果匹配不到就返回一个空字符串
			$imageType = $message->negotiateMedia($supported, true);

		匹配流程实际上同时考虑到了请求类型的优先级和在RFC中的明确性。这就意味着请求头的值越明确，所对应的优先级就越高，（除非通过 ``q`` 的值来修改）
		更多细节请阅读 `appropriate section of the RFC <https://tools.ietf.org/html/rfc7231#section-5.3.2>`_

	.. php:method:: negotiateCharset($supported)

		:param array $supported: 系统所支持的字符集构成的数组
		:returns: 对于所请求的字符集类型，所能匹配到的最优先的字符集
		:rtype: string

		和 ``negotiateMedia()`` 方法一样，只是用于匹配 ``Accept-Charset`` 请求头::

			$supported = [
				'utf-8',
				'iso-8895-9'
			];
			$charset = $message->negotiateCharset($supported);

		匹配不到的情况下，返回默认的 ``utf-8`` 字符集。

	.. php:method:: negotiateEncoding($supported)

		:param array $supported: 系统所支持的字符编码构成的数组
		:returns: 对于所请求的字符编码，所能匹配到的最优先的字符编码
		:rtype: string

		与上述两个方法类似，用于匹配 ``Accept-Encoding`` 请求头；无法匹配时返回 ``$supported`` 数组的第一个元素::

			$supported = [
				'gzip',
				'compress'
			];
			$encoding = $message->negotiateEncoding($supported);

	.. php:method:: negotiateLanguage($supported)

		:param array $supported: 系统所支持的语言构成的数组
		:returns: 对于所请求的语言，所能匹配到的最优先的语言
		:rtype: string

		与上述三个个方法类似，用于匹配 Accept-Language 请求头；无法匹配时返回 ``$supported`` 数组的第一个元素::

			$supported = [
				'en',
				'fr',
				'x-pig-latin'
			];
			$language = $message->negotiateLanguage($supported);

		关于语言标记的更多信息，请参阅 `RFC 1766 <https://www.ietf.org/rfc/rfc1766.txt>`_ 。
