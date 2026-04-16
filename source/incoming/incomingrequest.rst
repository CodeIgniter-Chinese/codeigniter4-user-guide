#####################
IncomingRequest 类
#####################

IncomingRequest 类提供了来自客户端（如浏览器）的 HTTP 请求的面向对象表示。
除了下面列出的方法外，它还扩展并可以访问 :doc:`Request </incoming/request>` 和 :doc:`Message </incoming/message>`
类的所有方法。

.. contents::
    :local:
    :depth: 2

访问请求
*********************

如果当前类继承自 ``CodeIgniter\Controller``，那么 Request 类的一个实例已经为你填充好了，并且可以作为类属性访问：

.. literalinclude:: incomingrequest/001.php

如果你不在控制器中，但仍然需要访问应用程序的 Request 对象，你可以通过 :doc:`Services 类 </concepts/services>` 获取它的副本：

.. literalinclude:: incomingrequest/002.php

不过，如果类不是控制器，最好将请求作为依赖项传入，并将其保存为类属性：

.. literalinclude:: incomingrequest/003.php

确定请求类型
************************

请求可能有多种类型，包括 AJAX 请求或来自命令行的请求。这可以通过 ``isAJAX()`` 和 ``isCLI()`` 方法来检查：

.. literalinclude:: incomingrequest/004.php

.. note:: ``isAJAX()`` 方法依赖于 ``X-Requested-With`` 标头，
    在某些情况下，JavaScript 发起的 XHR 请求（例如 fetch）默认不会发送该标头。
    关于如何避免此问题，请参阅 :doc:`AJAX 请求 </general/ajax>` 章节。

.. _incomingrequest-is:

is()
====

.. versionadded:: 4.3.0

从 v4.3.0 开始，你可以使用 ``is()`` 方法。它接受 HTTP 方法、``'ajax'``
或 ``'json'`` 作为参数，并返回布尔值。

.. note:: HTTP 方法应该是区分大小写的，但参数是不区分大小写的。

.. literalinclude:: incomingrequest/040.php

getMethod()
===========

你可以使用 ``getMethod()`` 方法检查此请求代表的 HTTP 方法：

.. literalinclude:: incomingrequest/005.php

HTTP 方法是区分大小写的，按照惯例，标准化方法使用全大写 US-ASCII 字母定义。

.. note:: 在 v4.5.0 之前，默认情况下，该方法返回小写字符串
    （即 ``'get'``、``'post'`` 等）。但这其实是一个 bug。

你可以通过将调用包装在 ``strtolower()`` 中来获取小写版本::

    // Returns 'get'
    $method = strtolower($request->getMethod());

你还可以使用 ``isSecure()`` 方法检查请求是否通过 HTTPS 连接发起：

.. literalinclude:: incomingrequest/006.php

获取输入
****************

你可以通过 Request 对象从 ``$_GET``、``$_POST``、``$_COOKIE``、``$_SERVER``
和 ``$_ENV`` 中获取输入。
数据不会自动过滤，返回的是请求中传递的原始输入数据。

.. note:: 使用全局变量是不好的做法。基本上应该避免使用，推荐使用 Request 对象的方法。

使用这些方法而不是直接访问（``$_POST['something']``）的主要优点是，
如果 Key 不存在，它们将返回 null，并且你可以对数据进行过滤。这让你方便地
使用数据，而不必先测试 Key 是否存在。换句话说，通常你可能会这样做：

.. literalinclude:: incomingrequest/007.php

使用 CodeIgniter 的内置方法，你可以简单地这样做：

.. literalinclude:: incomingrequest/008.php

.. _incomingrequest-getting-data:

获取数据
============

getGet()
--------

``getGet()`` 方法将从 ``$_GET`` 中拉取数据。

* ``$request->getGet()``

getPost()
---------

``getPost()`` 方法将从 ``$_POST`` 中拉取数据。

* ``$request->getPost()``

getCookie()
-----------

``getCookie()`` 方法将从 ``$_COOKIE`` 中拉取数据。

* ``$request->getCookie()``

getServer()
-----------

``getServer()`` 方法将从 ``$_SERVER`` 中拉取数据。

* ``$request->getServer()``

getEnv()
--------

.. deprecated:: 4.4.4 此方法从一开始就无法工作。请改用 :php:func:`env()`。

``getEnv()`` 方法将从 ``$_ENV`` 中拉取数据。

* ``$request->getEnv()``

getPostGet()
------------

此外，还有一些实用方法用于从 ``$_GET`` 或 ``$_POST`` 中检索信息，同时
保持控制查找顺序的能力：

* ``$request->getPostGet()`` - 先检查 ``$_POST``，然后检查 ``$_GET``

getGetPost()
------------

* ``$request->getGetPost()`` - 先检查 ``$_GET``，然后检查 ``$_POST``

getVar()
--------

.. important:: 此方法仅为了向后兼容而存在。请勿在
    新项目中使用它。即使你已经在使用它，我们也建议你使用
    其他更合适的方法。

``getVar()`` 方法将从 ``$_REQUEST`` 中拉取数据，因此将返回来自 ``$_GET``、``$_POST`` 或 ``$_COOKIE`` 的任何数据（取决于 php.ini 中的 `request-order <https://www.php.net/manual/zh/ini.core.php#ini.request-order>`_）。

.. warning:: 如果你只想验证 POST 数据，请勿使用 ``getVar()``。
    较新的值会覆盖较旧的值。如果 Cookie 与 POST 数据同名，并且你在 `request-order <https://www.php.net/manual/zh/ini.core.php#ini.request-order>`_
    中将 "C" 设置在 "P" 之后，那么 POST 值可能会被 Cookie 覆盖。

.. note:: 如果传入请求的 ``Content-Type`` 标头设置为 ``application/json``，
    则 ``getVar()`` 方法将返回 JSON 数据而不是 ``$_REQUEST`` 数据。

.. _incomingrequest-getting-json-data:

获取 JSON 数据
=================

你可以使用 ``getJSON()`` 将 ``php://input`` 的内容作为 JSON 流获取。

.. note::  这无法检查传入数据是否为有效 JSON，你应该只在知道
    期望的是 JSON 时才使用此方法。

.. literalinclude:: incomingrequest/009.php

默认情况下，这将把 JSON 数据中的任何对象作为对象返回。如果你希望将其转换为关联数组，请传入 ``true`` 作为第一个参数。

第二个和第三个参数对应于 PHP 函数
`json_decode() <https://www.php.net/manual/zh/function.json-decode.php>`_ 的 ``$depth`` 和 ``$flags`` 参数。

获取 JSON 特定数据
===============================

你可以通过将变量名传入 ``getJsonVar()`` 来从 JSON 流中获取特定的数据，
或者你可以使用“点”表示法深入 JSON 以获取不在根级别的数据。

.. literalinclude:: incomingrequest/010.php

如果你希望结果是关联数组而不是对象，你可以在第二个参数中传入 true：

.. literalinclude:: incomingrequest/011.php

.. note:: 有关“点”表示法的更多信息，请参阅 ``数组`` 辅助函数中 :php:func:`dot_array_search()` 的文档。

.. _incomingrequest-retrieving-raw-data:

获取原始数据（PUT、PATCH、DELETE）
========================================

最后，你可以使用 ``getRawInput()`` 将 ``php://input`` 的内容作为原始流获取：

.. literalinclude:: incomingrequest/012.php

这将检索数据并将其转换为数组。像这样：

.. literalinclude:: incomingrequest/013.php

你还可以使用 ``getRawInputVar()`` 从原始流中获取指定变量并进行过滤。

.. literalinclude:: incomingrequest/039.php

.. _incomingrequest-filtering-input-data:

过滤输入数据
====================

为了维护应用程序的安全性，你应该在访问所有输入时对其进行过滤。你可以
将要使用的过滤器类型作为这些方法的第二个参数传递。原生 ``filter_var()``
函数用于过滤。请前往 PHP 手册查看 `可用过滤器列表 <https://www.php.net/manual/zh/filters.php>`_。

过滤 POST 变量如下所示：

.. literalinclude:: incomingrequest/014.php

除 ``getJSON()`` 和 ``getRawInput()`` 外，上述所有方法都支持作为第二个参数传入的过滤器类型。

获取标头
******************

你可以使用 ``headers()`` 方法访问随请求发送的任何标头，该方法返回
所有标头的数组，键为标头名称，值为 ``CodeIgniter\HTTP\Header``
的实例：

.. literalinclude:: incomingrequest/015.php

如果你只需要单个标头，可以将名称传入 ``header()`` 方法。如果存在，这将
不区分大小写地获取指定的标头对象。如果不存在，则返回 ``null``：

.. literalinclude:: incomingrequest/016.php

你始终可以使用 ``hasHeader()`` 来查看此请求中是否存在该标头：

.. literalinclude:: incomingrequest/017.php

如果你需要将标头值作为一行中包含所有值的字符串，可以使用 ``getHeaderLine()`` 方法：

.. literalinclude:: incomingrequest/018.php

如果你需要整个标头，包括名称和值都在单个字符串中，只需将标头转换为字符串即可：

.. literalinclude:: incomingrequest/019.php

请求 URL
***************

你可以通过 ``$request->getUri()`` 方法检索代表此请求当前 URI 的 :doc:`URI </libraries/uri>` 对象。
你可以将此对象转换为字符串以获取当前请求的完整 URL：

.. literalinclude:: incomingrequest/020.php

该对象赋予你完全的能力来单独获取请求的任何部分：

.. literalinclude:: incomingrequest/021.php

你可以使用 ``getRoutePath()`` 处理当前的 URI 字符串（相对于 baseURL 的路径）。

.. note:: ``getRoutePath()`` 方法自 v4.4.0 起可用。在 v4.4.0 之前，
    ``getPath()`` 方法返回相对于 baseURL 的路径。

上传文件
**************

可以通过 ``$request->getFiles()`` 检索有关所有上传文件的信息，该方法返回
``CodeIgniter\HTTP\Files\UploadedFile`` 实例的数组。这有助于减轻处理上传文件的痛苦，
并使用最佳实践来最大限度地减少任何安全风险。

.. literalinclude:: incomingrequest/023.php

有关详细信息，请参阅 :ref:`处理上传文件 <uploaded-files-accessing-files>`。

你可以根据 HTML 文件输入框中给出的文件名，检索单独上传的文件：

.. literalinclude:: incomingrequest/024.php

你可以根据 HTML 文件输入框中给出的文件名，检索在多文件上传过程中上传的同名文件数组：

.. literalinclude:: incomingrequest/025.php

.. note:: 此处获取的文件对象本质上对应于 ``$_FILES``。即便用户只是点击了表单的提交按钮而没有上传任何文件，该文件对象依然会存在。你应该通过 UploadedFile 中的 ``isValid()`` 方法来检查文件是否确实已上传。更多详情请参见 :ref:`verify-a-file` 章节。

内容协商
*******************

你可以通过 ``negotiate()`` 方法轻松地与请求协商内容类型：

.. literalinclude:: incomingrequest/026.php

有关更多详细信息，请参阅 :doc:`内容协商 </incoming/content_negotiation>` 页面。

类参考
***************

.. note:: 除了这里列出的方法外，此类还继承了
    :doc:`Request 类 </incoming/request>` 和 :doc:`Message 类 </incoming/message>` 的方法。

父类提供的可用方法包括：

* :meth:`CodeIgniter\\HTTP\\Request::getIPAddress`
* :meth:`CodeIgniter\\HTTP\\Request::isValidIP`
* :meth:`CodeIgniter\\HTTP\\Request::getMethod`
* :meth:`CodeIgniter\\HTTP\\Request::setMethod`
* :meth:`CodeIgniter\\HTTP\\Request::getServer`
* :meth:`CodeIgniter\\HTTP\\Request::getEnv`
* :meth:`CodeIgniter\\HTTP\\Request::setGlobal`
* :meth:`CodeIgniter\\HTTP\\Request::fetchGlobal`
* :meth:`CodeIgniter\\HTTP\\Message::getBody`
* :meth:`CodeIgniter\\HTTP\\Message::setBody`
* :meth:`CodeIgniter\\HTTP\\Message::appendBody`
* :meth:`CodeIgniter\\HTTP\\Message::populateHeaders`
* :meth:`CodeIgniter\\HTTP\\Message::headers`
* :meth:`CodeIgniter\\HTTP\\Message::header`
* :meth:`CodeIgniter\\HTTP\\Message::hasHeader`
* :meth:`CodeIgniter\\HTTP\\Message::getHeaderLine`
* :meth:`CodeIgniter\\HTTP\\Message::setHeader`
* :meth:`CodeIgniter\\HTTP\\Message::removeHeader`
* :meth:`CodeIgniter\\HTTP\\Message::appendHeader`
* :meth:`CodeIgniter\\HTTP\\Message::prependHeader`
* :meth:`CodeIgniter\\HTTP\\Message::getProtocolVersion`
* :meth:`CodeIgniter\\HTTP\\Message::setProtocolVersion`

.. php:namespace:: CodeIgniter\HTTP

.. php:class:: IncomingRequest

    .. php:method:: isCLI()

        :returns: 如果请求是从命令行发起的，则返回 true，否则返回 false。
        :rtype: bool

    .. php:method:: isAJAX()

        :returns: 如果请求是 AJAX 请求，则返回 true，否则返回 false。
        :rtype: bool

    .. php:method:: isSecure()

        :returns: 如果请求是 HTTPS 请求，则返回 true，否则返回 false。
        :rtype: bool

    .. php:method:: getVar([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量/键的名称。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可以在
                        `可用过滤器列表 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可以在
                        `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:   如果未提供参数，则返回 ``$_REQUEST``，否则如果找到则返回 REQUEST 值，如果未找到则返回 null
        :rtype: array|bool|float|int|object|string|null

        .. important:: 此方法仅为了向后兼容而存在。请勿在
            新项目中使用它。即使你已经在使用它，我们也建议你使用
            其他更合适的方法。

        此方法与 ``getGet()`` 相同，只是它获取 REQUEST 数据。

    .. php:method:: getGet([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量/键的名称。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可以在
                        `过滤器类型 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可以在
                        `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:       如果未提供参数，则返回 ``$_GET``，否则如果找到则返回 GET 值，如果未找到则返回 null
        :rtype: array|bool|float|int|object|string|null

        第一个参数将包含你要查找的 GET 项的名称：

        .. literalinclude:: incomingrequest/041.php

        如果你尝试检索的项不存在，该方法返回 null。

        第二个可选参数允许你通过 PHP 的过滤器运行数据。作为第二个参数传入
        所需的过滤器类型：

        .. literalinclude:: incomingrequest/042.php

        要返回所有 GET 项的数组，请不带任何参数调用。

        要返回所有 GET 项并通过过滤器，请将第一个参数设置为 null，
        同时将第二个参数设置为你要使用的过滤器：

        .. literalinclude:: incomingrequest/043.php

        要返回多个 GET 参数的数组，请将所有需要的键作为数组传递：

        .. literalinclude:: incomingrequest/044.php

        这里适用相同的规则，要检索经过过滤的参数，请将第二个参数设置为
        要应用的过滤器类型：

        .. literalinclude:: incomingrequest/045.php

    .. php:method:: getPost([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量/键的名称。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可以在
                        `这里 <https://www.php.net/manual/zh/filters.php>`__ 找到。
        :param  int     $flags: 要应用的标志。标志列表可以在
                        `这里 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 找到。
        :returns:       如果未提供参数，则返回 ``$_POST``，否则如果找到则返回 POST 值，如果未找到则返回 null
        :rtype: array|bool|float|int|object|string|null

        此方法与 ``getGet()`` 相同，只是它获取 POST 数据。

    .. php:method:: getPostGet([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量/键的名称。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可以在
                        `过滤器类型 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可以在
                        `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:       如果未指定参数，则返回 ``$_POST`` 和 ``$_GET`` 的组合（发生冲突时首选 POST 值），
                        否则查找 POST 值，如果未找到则查找 GET 值，如果未找到任何值则返回 null
        :rtype: array|bool|float|int|object|string|null

        此方法的工作方式与 ``getPost()`` 和 ``getGet()`` 几乎相同，只是组合在一起。
        它将搜索 POST 和 GET 流中的数据，首先在 POST 中查找，
        然后在 GET 中查找：

        .. literalinclude:: incomingrequest/032.php

        如果未指定索引，它将返回 POST 和 GET 流的组合。
        但在名称冲突的情况下，POST 数据将被优先考虑。

    .. php:method:: getGetPost([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量/键的名称。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可以在
                        `过滤器类型 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可以在
                        `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:       如果未指定参数，则返回 ``$_GET`` 和 ``$_POST`` 的组合（发生冲突时首选 GET 值），
                        否则查找 GET 值，如果未找到则查找 POST 值，如果未找到任何值则返回 null
        :rtype: array|bool|float|int|object|string|null

        此方法的工作方式与 ``getPost()`` 和 ``getGet()`` 几乎相同，只是组合在一起。
        它将搜索 GET 和 POST 流中的数据，首先在 GET 中查找，
        然后在 POST 中查找：

        .. literalinclude:: incomingrequest/033.php

        如果未指定索引，它将返回 GET 和 POST 流的组合。
        但在名称冲突的情况下，GET 数据将被优先考虑。

    .. php:method:: getCookie([$index = null[, $filter = null[, $flags = null]]])

        :param  array|string|null    $index: COOKIE 名称
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可以在
                        `过滤器类型 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可以在
                        `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:        如果未提供参数，则返回 ``$_COOKIE``，否则如果找到则返回 COOKIE 值，如果未找到则返回 null
        :rtype: array|bool|float|int|object|string|null

        此方法与 ``getPost()`` 和 ``getGet()`` 相同，只是它获取 Cookie 数据：

        .. literalinclude:: incomingrequest/034.php

        要返回多个 Cookie 值的数组，请将所有需要的键作为数组传递：

        .. literalinclude:: incomingrequest/035.php

        .. note:: 与 :doc:`Cookie 辅助函数 <../helpers/cookie_helper>`
            中的函数 :php:func:`get_cookie()` 不同，此方法 **不会** 添加
            你配置的 ``Config\Cookie::$prefix`` 值作为前缀。

    .. php:method:: getServer([$index = null[, $filter = null[, $flags = null]]])

        :param  array|string|null    $index: 值名称
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可以在
                        `过滤器类型 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可以在
                        `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:        如果找到则返回 ``$_SERVER`` 项目值，如果未找到则返回 null
        :rtype: array|bool|float|int|object|string|null

        此方法与 ``getPost()``、``getGet()`` 和 ``getCookie()``
        方法相同，只是它获取服务器数据（``$_SERVER``）：

        .. literalinclude:: incomingrequest/036.php

        要返回多个 ``$_SERVER`` 值的数组，请将所有需要的键作为数组传递。

        .. literalinclude:: incomingrequest/037.php

    .. php:method:: getUserAgent()

        :returns:  在 SERVER 数据中找到的用户代理字符串，如果未找到则为 null。
        :rtype: CodeIgniter\\HTTP\\UserAgent

        此方法返回来自 SERVER 数据的用户代理实例：

        .. literalinclude:: incomingrequest/038.php

    .. php:method:: getPath()

        :returns:        相对于 baseURL 的当前 URI 路径
        :rtype:    string

        此方法返回相对于 baseURL 的当前 URI 路径。

        .. note:: 在 v4.4.0 之前，这是确定“当前 URI”的最安全方法，
            因为 ``IncomingRequest::$uri`` 可能不知道基本 URL 的完整 App 配置。

    .. php:method:: setPath($path)

        .. deprecated:: 4.4.0

        :param    string    $path: 用作当前 URI 的相对路径
        :returns:        此 IncomingRequest 实例
        :rtype:    IncomingRequest

        .. note:: 在 v4.4.0 之前，主要仅用于测试目的，这
            允许你设置当前请求的相对路径值，而不是依赖于 URI 检测。
            这也更新了底层的 ``URI`` 实例为新路径。
