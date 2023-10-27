#####################
IncomingRequest 类
#####################

IncomingRequest 类为来自客户端(如浏览器)的 HTTP 请求提供了面向对象的表示。它扩展并可以访问 :doc:`Request </incoming/request>` 和 :doc:`Message </incoming/message>` 类的所有方法,以及下面列出的方法。

访问请求
*********************

如果当前类是 ``CodeIgniter\Controller`` 的后代,则已经为你填充了请求类的一个实例,可以将其作为类属性访问:

.. literalinclude:: incomingrequest/001.php

如果你不在控制器中,但仍然需要访问应用程序的 Request 对象,你可以通过 :doc:`Services 类 </concepts/services>` 获取它的一个副本:

.. literalinclude:: incomingrequest/002.php

不过,如果类是控制器之外的任何其他类,最好是将请求作为依赖项传递,以便将其保存为类属性:

.. literalinclude:: incomingrequest/003.php

确定请求类型
************************

请求可以是几种类型,包括 AJAX 请求或来自命令行的请求。这可以通过 ``isAJAX()`` 和 ``isCLI()`` 方法检查:

.. literalinclude:: incomingrequest/004.php

.. note:: ``isAJAX()`` 方法取决于 ``X-Requested-With`` 头,
    但在通过 JavaScript 发出的 XHR 请求中(即 fetch),该头默认不会发送。
    请参阅 :doc:`AJAX 请求 </general/ajax>` 部分了解如何避免此问题。

.. _incomingrequest-is:

is()
====

.. versionadded:: 4.3.0

自 v4.3.0 起,你可以使用 ``is()`` 方法。它返回布尔值。

.. literalinclude:: incomingrequest/040.php

getMethod()
===========

你可以使用 ``getMethod()`` 方法检查此请求所代表的 HTTP 方法:

.. literalinclude:: incomingrequest/005.php

默认情况下,该方法以小写字符串形式返回(即 ``'get'``、``'post'`` 等)。

.. important:: 将返回值转换为小写的功能已被弃用。它将在未来版本中删除,此方法将等效于 PSR-7。

你可以通过将调用包装在 ``strtoupper()`` 中获取大写版本::

    // 返回 'GET'
    $method = strtoupper($request->getMethod());

你还可以使用 ``isSecure()`` 方法检查请求是否通过 HTTPS 连接发出:

.. literalinclude:: incomingrequest/006.php

检索输入
******************

你可以通过 Request 对象检索来自 ``$_SERVER``、``$_GET``、``$_POST`` 和 ``$_ENV`` 的输入。
数据不会自动过滤,并以请求中传递的原始输入数据形式返回。

.. note:: 使用全局变量是不好的做法。基本上,应该避免使用它,建议使用 Request 对象的方法。

与直接访问它们(``$_POST['something']``)的主要优点是,如果项不存在,这些方法将返回 null,并且你可以对数据进行过滤。这使你可以方便地使用数据,而无需先测试一个项是否存在。换句话说,通常你可能会做这样的事情:

.. literalinclude:: incomingrequest/007.php

使用 CodeIgniter 内置的方法,你可以简单地这样做:

.. literalinclude:: incomingrequest/008.php

.. _incomingrequest-getting-data:

获取数据
============

``getVar()`` 方法将从 ``$_REQUEST`` 中获取数据,因此将返回 ``$_GET``、``$_POST`` 或 ``$_COOKIE`` 中的任何数据(取决于 php.ini `request-order <https://www.php.net/manual/en/ini.core.php#ini.request-order>`_ )。

.. note:: 如果传入请求的 ``Content-Type`` 标头设置为 ``application/json``,
    ``getVar()`` 方法会返回 JSON 数据,而不是 ``$_REQUEST`` 数据。

虽然这很方便,但你通常需要使用更具体的方法,如:

* ``$request->getGet()``
* ``$request->getPost()``
* ``$request->getCookie()``
* ``$request->getServer()``
* ``$request->getEnv()``

另外,还有一些实用程序方法可以从 ``$_GET`` 或 ``$_POST`` 中检索信息,同时保持控制查找顺序的能力:

* ``$request->getPostGet()`` - 首先检查 ``$_POST``,然后检查 ``$_GET``
* ``$request->getGetPost()`` - 首先检查 ``$_GET``,然后检查 ``$_POST``

.. _incomingrequest-getting-json-data:

获取 JSON 数据
=================

你可以使用 ``getJSON()`` 将 ``php://input`` 的内容作为 JSON 流获取。

.. note::  这无法检查传入的数据是否为有效的 JSON。你只应在知道正在期望 JSON 时使用此方法。

.. literalinclude:: incomingrequest/009.php

默认情况下,这将返回 JSON 数据中的任何对象作为对象。如果你想要将其转换为关联数组,请在第一个参数中传递 ``true``。

第二和第三个参数与 `json_decode <https://www.php.net/manual/en/function.json-decode.php>`_ PHP 函数的 ``depth`` 和 ``options`` 参数对应。

如果传入请求的 ``Content-Type`` 标头设置为 ``application/json``,你也可以使用 ``getVar()`` 来获取 JSON 流。以这种方式使用 ``getVar()`` 将始终返回一个对象。

从 JSON 获取特定数据
===============================

你可以通过向 ``getVar()`` 传入变量名来从 JSON 流中获取特定的数据片段,用于获取所需的数据,或者可以使用“点”表示法深入到 JSON 中,以获取不在根级别的数据。

.. literalinclude:: incomingrequest/010.php

如果要结果是一个关联数组而不是对象,可以使用 ``getJsonVar()`` ,并在第二个参数中传递 true。如果你无法保证传入请求具有正确的 ``Content-Type`` 标头,也可以使用此函数。

.. literalinclude:: incomingrequest/011.php

.. note:: 有关“点”表示法的更多信息,请参阅 ``Array`` 辅助函数中的 :php:func:`dot_array_search()` 文档。

.. _incomingrequest-retrieving-raw-data:

检索原始数据(PUT、PATCH、DELETE)
========================================

最后,你可以使用 ``getRawInput()`` 将 ``php://input`` 的内容作为原始流获取:

.. literalinclude:: incomingrequest/012.php

这将检索数据并将其转换为数组。像这样:

.. literalinclude:: incomingrequest/013.php

你还可以使用 ``getRawInputVar()``,从原始流中获取指定的变量并对其进行过滤。

.. literalinclude:: incomingrequest/039.php

.. _incomingrequest-filtering-input-data:

过滤输入数据
====================

为了保持应用程序的安全,你会想要过滤所有输入。你可以将要使用的过滤器类型作为这些方法的第二个参数传递。使用内置的 ``filter_var()`` 函数进行过滤。前往 PHP 手册获取 `有效过滤器类型列表 <https://www.php.net/manual/en/filter.filters.php>`_。

过滤 POST 变量的代码如下:

.. literalinclude:: incomingrequest/014.php

上面提到的所有方法都支持作为第二个参数传递过滤器类型, ``getJSON()`` 和 ``getRawInput()`` 除外。

检索标头
******************

你可以通过 ``headers()`` 方法访问与请求一起发送的任何标头,它返回一个数组,其中键是标头的名称,值是 ``CodeIgniter\HTTP\Header`` 的一个实例:

.. literalinclude:: incomingrequest/015.php

如果你只需要单个标头,可以将名称传递给 ``header()`` 方法。这将以不区分大小写的方式获取指定的标头对象(如果存在)。如果不存在,则返回 ``null``::

.. literalinclude:: incomingrequest/016.php

你可以始终使用 ``hasHeader()`` 来查看该请求中是否存在标头:

.. literalinclude:: incomingrequest/017.php

如果你需要将标头的值作为单行字符串,其中所有值在一行中,可以使用 ``getHeaderLine()`` 方法:

.. literalinclude:: incomingrequest/018.php

如果你需要将标头及其名称和值合并为单个字符串,只需将标头转换为字符串:

.. literalinclude:: incomingrequest/019.php

请求 URL
***************

你可以通过 ``$request->getUri()`` 方法检索表示当前 URI 的 :doc:`URI </libraries/uri>` 对象。你可以将此对象转换为字符串以获取当前请求的完整 URL:

.. literalinclude:: incomingrequest/020.php

该对象使你能够自行获取请求的任何部分:

.. literalinclude:: incomingrequest/021.php

您可以使用 ``getRoutePath()`` 方法来处理当前 URI 字符串（相对于您的 baseURL 的路径）。

.. note:: 自 v4.4.0 版本开始，可以使用 ``getRoutePath()`` 方法。在 v4.4.0 之前，``getPath()`` 方法返回相对于您的 baseURL 的路径。

上传的文件
**************

可以通过 ``$request->getFiles()`` 获取有关所有上传文件信息,它返回 ``CodeIgniter\HTTP\Files\UploadedFile`` 实例的数组。这有助于减轻使用上传文件时的痛苦,并使用最佳实践来最大程度地减少任何安全风险。

.. literalinclude:: incomingrequest/023.php

参见 :ref:`使用上传的文件 <uploaded-files-accessing-files>` 以获取详细信息。

你可以根据 HTML 文件输入中给出的文件名检索单独上传的文件:

.. literalinclude:: incomingrequest/024.php

你可以检索作为多文件上传一部分上传的同名文件数组,基于 HTML 文件输入中给出的文件名:

.. literalinclude:: incomingrequest/025.php

.. note:: 这里的文件对应于 ``$_FILES``。即使用户仅点击表单的提交按钮而不上传任何文件,文件也会存在。你可以通过 UploadedFile 中的 ``isValid()`` 方法检查文件是否实际被上传。有关详细信息,请参阅 :ref:`verify-a-file`。

内容协商
*******************

你可以通过 ``negotiate()`` 方法轻松地与请求协商内容类型:

.. literalinclude:: incomingrequest/026.php

有关更多详细信息,请参阅 :doc:`内容协商 </incoming/content_negotiation>` 页面。

类参考
***************

.. note:: 除了这里列出的方法之外,此类还继承了 :doc:`请求类 </incoming/request>` 和 :doc:`消息类 </incoming/message>` 的方法。

父类提供的可用方法有:

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

        :returns: 如果请求是从命令行发起的,则为 True,否则为 False
        :rtype: bool

    .. php:method:: isAJAX()

        :returns: 如果请求是 AJAX 请求,则为 True,否则为 False
        :rtype: bool

    .. php:method:: isSecure()

        :returns: 如果请求是 HTTPS 请求,则为 True,否则为 False
        :rtype: bool

    .. php:method:: getVar([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量/键的名称。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.php>`__ 找到。
        :param  int     $flags: 要应用的标志。标志列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.flags.php>`__ 找到。
        :returns:   如果没有提供参数,则返回 ``$_REQUEST``,否则如果找到则返回 REQUEST 值,如果没找到则为 null
        :rtype: array|bool|float|int|object|string|null

        第一个参数将包含要查找的 REQUEST 项的名称:

        .. literalinclude:: incomingrequest/027.php

        如果尝试检索的项目不存在,该方法将返回 null。

        第二个可选参数允许你通过 PHP 的过滤器运行数据。将所需的过滤器类型作为第二个参数传递:

        .. literalinclude:: incomingrequest/028.php

        若要返回所有 POST 项,请不带任何参数调用。

        要返回所有 POST 项并通过过滤器传递它们,请将第一个参数设置为 null,同时将第二个参数设置为要使用的过滤器:

        .. literalinclude:: incomingrequest/029.php

        要返回多个 POST 参数的数组,请传递所有所需键的数组:

        .. literalinclude:: incomingrequest/030.php

        这里也应用了相同的规则,要使用过滤检索参数,请将第二个参数设置为要应用的过滤器类型:

        .. literalinclude:: incomingrequest/031.php

    .. php:method:: getGet([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量/键的名称。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.php>`__ 找到。
        :param  int     $flags: 要应用的标志。标志列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.flags.php>`__ 找到。
        :returns:       如果没有提供参数,则返回 ``$_GET``,否则如果找到则返回 GET 值,如果没找到则为 null
        :rtype: array|bool|float|int|object|string|null

        此方法与 ``getVar()`` 相同,只是它获取 GET 数据。

    .. php:method:: getPost([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量/键的名称。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.php>`__ 找到。
        :param  int     $flags: 要应用的标志。标志列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.flags.php>`__ 找到。
        :returns:       如果没有提供参数,则返回 ``$_POST``,否则如果找到则返回 POST 值,如果没找到则为 null
        :rtype: array|bool|float|int|object|string|null

            此方法与 ``getVar()`` 相同,只是它获取 POST 数据。

    .. php:method:: getPostGet([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量/键的名称。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.php>`__ 找到。
        :param  int     $flags: 要应用的标志。标志列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.flags.php>`__ 找到。
        :returns:       如果没有指定参数,则返回 ``$_POST`` 和 ``$_GET`` 组合(冲突时优先 POST 值),
                        否则首先查找 POST 值,找不到则查找 GET 值,如果没找到则返回 null
        :rtype: array|bool|float|int|object|string|null

        这个方法的工作原理与 ``getPost()`` 和 ``getGet()`` 基本相同,只是结合了两者。
        它将在 POST 和 GET 流中搜索数据,先在 POST 中查找,然后在 GET 中查找:

        .. literalinclude:: incomingrequest/032.php

        如果没有指定索引,它将返回 POST 和 GET 流组合。
        如果名称冲突,将优先 POST 数据。

    .. php:method:: getGetPost([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量/键的名称。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.php>`__ 找到。
        :param  int     $flags: 要应用的标志。标志列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.flags.php>`__ 找到。
        :returns:       如果没有指定参数,则返回 ``$_GET`` 和 ``$_POST`` 组合(冲突时优先 GET 值),
                        否则首先查找 GET 值,找不到则查找 POST 值,如果没找到则返回 null
        :rtype: array|bool|float|int|object|string|null

        这个方法的工作原理与 ``getPost()`` 和 ``getGet()`` 基本相同,只是结合了两者。
        它将在 GET 和 POST 流中搜索数据,先在 GET 中查找,然后在 POST 中查找:

        .. literalinclude:: incomingrequest/033.php

        如果没有指定索引,它将返回 GET 和 POST 流组合。
        如果名称冲突,将优先 GET 数据。

    .. php:method:: getCookie([$index = null[, $filter = null[, $flags = null]]])

        :param  array|string|null    $index: COOKIE 名称
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.php>`__ 找到。
        :param  int     $flags: 要应用的标志。标志列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.flags.php>`__ 找到。
        :returns:        如果没有提供参数,则返回 ``$_COOKIE``,否则如果找到则返回 COOKIE 值,如果没有找到则为 null
        :rtype: array|bool|float|int|object|string|null

        此方法与 ``getPost()`` 和 ``getGet()`` 相同,只是它获取 cookie 数据:

        .. literalinclude:: incomingrequest/034.php

        要返回多个 cookie 值的数组,请传递所有所需键的数组:

        .. literalinclude:: incomingrequest/035.php

        .. note:: 与 :doc:`Cookie 辅助函数 <../helpers/cookie_helper>` 函数 :php:func:`get_cookie()` 不同,此方法不会在配置的 ``Config\Cookie::$prefix`` 值前加上前缀。

    .. php:method:: getServer([$index = null[, $filter = null[, $flags = null]]])

        :param  array|string|null    $index: 值名称
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.php>`__ 找到。
        :param  int     $flags: 要应用的标志。标志列表可在
                        `这里 <https://www.php.net/manual/en/filter.filters.flags.php>`__ 找到。
        :returns:        如果找到则返回 ``$_SERVER`` 项的值,否则为 null
        :rtype: array|bool|float|int|object|string|null

        此方法与 ``getPost()``、``getGet()`` 和 ``getCookie()`` 方法相同,只是它获取 getServer 数据(``$_SERVER``):

        .. literalinclude:: incomingrequest/036.php

        要返回多个 ``$_SERVER`` 值的数组,请传递所有所需键的数组。

        .. literalinclude:: incomingrequest/037.php

    .. php:method:: getUserAgent([$filter = null])

        :param  int $filter: 要应用的过滤器类型。过滤器列表可在
                    `这里 <https://www.php.net/manual/en/filter.filters.php>`__ 找到。
        :returns:  在 SERVER 数据中找到的用户代理字符串,如果没有找到则为 null。
        :rtype: CodeIgniter\\HTTP\\UserAgent

        此方法返回来自 SERVER 数据的用户代理字符串:

        .. literalinclude:: incomingrequest/038.php

    .. php:method:: getPath()

        :returns:        相对于 baseURL 的当前 URI 路径
        :rtype:    string

        该方法返回相对于 baseURL 的当前 URI 路径。

        .. note:: 在 v4.4.0 之前，这是确定“当前 URI”的最安全的方法，因为 ``IncomingRequest::$uri`` 可能不知道完整的 App 配置的 base URL。

    .. php:method:: setPath($path)

        .. deprecated:: 4.4.0

        :param    string    $path: 用作当前 URI 的相对路径
        :returns:        此传入请求
        :rtype:    IncomingRequest

        .. note:: 在 v4.4.0 之前，主要用于测试目的，这允许您设置当前请求的相对路径值，而不是依赖于 URI 检测。这也会更新底层的 ``URI`` 实例的新路径。
