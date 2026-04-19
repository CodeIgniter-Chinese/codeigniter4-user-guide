#####################
IncomingRequest 类
#####################

IncomingRequest 类提供了客户端（如浏览器）HTTP 请求的面向对象表示。
除了下文列出的方法外，此类还继承并可访问 :doc:`Request </incoming/request>` 和 :doc:`Message </incoming/message>` 类的所有方法。

.. contents::
    :local:
    :depth: 2

访问请求
*********************

如果当前类继承自 ``CodeIgniter\Controller``，则 Request 类的实例已自动填充，并可通过类属性访问：

.. literalinclude:: incomingrequest/001.php

如果不在控制器内，但仍需访问应用程序的 Request 对象，可通过 :doc:`Services 类 </concepts/services>` 获取副本：

.. literalinclude:: incomingrequest/002.php

不过，如果类不是控制器，建议将 Request 作为依赖项传入并存为类属性：

.. literalinclude:: incomingrequest/003.php

判断请求类型
************************

请求可能有多种类型，包括 AJAX 请求或命令行请求。可使用 ``isAJAX()`` 和 ``isCLI()`` 方法进行检查：

.. literalinclude:: incomingrequest/004.php

.. note:: ``isAJAX()`` 方法依赖于 ``X-Requested-With`` 标头。在某些情况下，通过 JavaScript（如 fetch）发起的 XHR 请求默认不会发送该标头。请参阅 :doc:`AJAX 请求 </general/ajax>` 章节了解如何解决此问题。

.. _incomingrequest-is:

is()
====

.. versionadded:: 4.3.0

自 v4.3.0 起，可使用 ``is()`` 方法。该方法接受 HTTP 方法、``'ajax'`` 或 ``'json'``，并返回布尔值。

.. note:: 虽然 HTTP 方法区分大小写，但此参数不区分大小写。

.. literalinclude:: incomingrequest/040.php

getMethod()
===========

可使用 ``getMethod()`` 方法检查此请求代表的 HTTP 方法：

.. literalinclude:: incomingrequest/005.php

HTTP 方法区分大小写。按照惯例，标准方法均由大写 US-ASCII 字母定义。

.. note:: v4.5.0 之前，该方法默认返回小写字符串（如 ``'get'``、``'post'`` 等），但这其实是一个 Bug。

可通过 ``strtolower()`` 封装调用以获取小写版本::

    // 返回 'get'
    $method = strtolower($request->getMethod());

还可使用 ``isSecure()`` 方法检查是否通过 HTTPS 连接发起请求：

.. literalinclude:: incomingrequest/006.php

获取输入数据
****************

可通过 Request 对象从 ``$_GET``、``$_POST``、``$_COOKIE``、``$_SERVER`` 和 ``$_ENV`` 中获取输入。
数据不会被自动过滤，将返回请求传入的原始输入数据。

.. note:: 使用全局变量并非良好实践。原则上应避免使用，建议使用 Request 对象的方法。

使用这些方法而非直接访问（如 ``$_POST['something']``）的主要优势在于：如果项不存在将返回 null，且支持数据过滤。这使得在使用数据前无需先测试其是否存在。换言之，通常可能需要这样做：

.. literalinclude:: incomingrequest/007.php

使用 CodeIgniter 的内置方法，只需：

.. literalinclude:: incomingrequest/008.php

.. _incomingrequest-getting-data:

获取数据
============

getGet()
--------

``getGet()`` 方法将从 ``$_GET`` 中获取数据。

* ``$request->getGet()``

getPost()
---------

``getPost()`` 方法将从 ``$_POST`` 中获取数据。

* ``$request->getPost()``

getCookie()
-----------

``getCookie()`` 方法将从 ``$_COOKIE`` 中获取数据。

* ``$request->getCookie()``

getServer()
-----------

``getServer()`` 方法将从 ``$_SERVER`` 中获取数据。

* ``$request->getServer()``

getPostGet()
------------

此外，还有一些实用方法可从 ``$_GET`` 或 ``$_POST`` 中检索信息，并支持控制搜索顺序：

* ``$request->getPostGet()`` - 先检查 ``$_POST``，再检查 ``$_GET``

getGetPost()
------------

* ``$request->getGetPost()`` - 先检查 ``$_GET``，再检查 ``$_POST``

getVar()
--------

.. important:: 此方法仅为了向后兼容而存在。请勿在新项目中使用。即使已经在用，也建议换用其他更合适的方法。

``getVar()`` 方法将从 ``$_REQUEST`` 中获取数据，因此会返回来自 ``$_GET``、``$_POST`` 或 ``$_COOKIE`` 的任何数据（取决于 php.ini 中的 `request-order <https://www.php.net/manual/zh/ini.core.php#ini.request-order>`_）。

.. warning:: 如果只想验证 POST 数据，请勿使用 ``getVar()``。较新的值会覆盖旧值。如果在 `request-order <https://www.php.net/manual/zh/ini.core.php#ini.request-order>`_ 中将 "C" 设置在 "P" 之后，同名的 Cookie 值可能会覆盖 POST 值。

.. note:: 如果传入请求的 ``Content-Type`` 标头设为 ``application/json``，``getVar()`` 方法将返回 JSON 数据而非 ``$_REQUEST`` 数据。

.. _incomingrequest-getting-json-data:

获取 JSON 数据
=================

可使用 ``getJSON()`` 将 ``php://input`` 的内容作为 JSON 流获取。

.. note:: 此方法无法检查传入数据是否为有效的 JSON，仅应在确定预期为 JSON 时使用。

.. literalinclude:: incomingrequest/009.php

默认情况下，该方法将 JSON 数据中的所有对象作为对象返回。如果希望将其转换为关联数组，请将第一个参数设为 ``true``。

第二和第三个参数分别对应 PHP 函数 `json_decode() <https://www.php.net/manual/zh/function.json-decode.php>`_ 的 ``$depth`` 和 ``$flags`` 参数。

从 JSON 获取特定数据
===============================

通过向 ``getJsonVar()`` 传入变量名，可获取 JSON 流中的特定数据；也可使用“点”语法深入 JSON 获取非根级别的数据。

.. literalinclude:: incomingrequest/010.php

如果希望结果是关联数组而非对象，可在第二个参数传入 true：

.. literalinclude:: incomingrequest/011.php

.. note:: 有关“点”语法的更多信息，请参阅 ``数组`` 辅助函数中 :php:func:`dot_array_search()` 的文档。

.. _incomingrequest-retrieving-raw-data:

获取原始数据（PUT、PATCH、DELETE）
========================================

最后，可使用 ``getRawInput()`` 将 ``php://input`` 的内容作为原始流获取：

.. literalinclude:: incomingrequest/012.php

这将检索数据并将其转换为数组。如下所示：

.. literalinclude:: incomingrequest/013.php

也可使用 ``getRawInputVar()`` 从原始流中获取特定变量并进行过滤。

.. literalinclude:: incomingrequest/039.php

.. _incomingrequest-filtering-input-data:

过滤输入数据
====================

为了维护应用程序安全，应在访问所有输入时进行过滤。可将过滤器类型作为这些方法的第二个参数传入。过滤功能使用原生的 ``filter_var()`` 函数。关于有效过滤器类型的列表，请参考 PHP 手册中的 `可用过滤器列表 <https://www.php.net/manual/zh/filters.php>`_。

过滤 POST 变量示例如下：

.. literalinclude:: incomingrequest/014.php

除 ``getJSON()`` 和 ``getRawInput()`` 外，上述所有方法均支持在第二个参数中传入过滤器类型。

获取标头
******************

可使用 ``headers()`` 方法访问随请求发送的所有标头。该方法返回一个数组，键为标头名称，值为 ``CodeIgniter\HTTP\Header`` 实例：

.. literalinclude:: incomingrequest/015.php

如果只需要单个标头，可将名称传入 ``header()`` 方法。如果该标头存在，将以不区分大小写的方式获取指定的标头对象；否则返回 ``null``：

.. literalinclude:: incomingrequest/016.php

可随时使用 ``hasHeader()`` 检查此请求中是否存在某个标头：

.. literalinclude:: incomingrequest/017.php

如果需要以字符串形式获取一行内的所有标头值，可使用 ``getHeaderLine()`` 方法：

.. literalinclude:: incomingrequest/018.php

如果需要包含名称和值的完整标头字符串，直接将标头转换为字符串即可：

.. literalinclude:: incomingrequest/019.php

请求 URL
***************

可通过 ``$request->getUri()`` 方法获取代表当前请求 URI 的 :doc:`URI </libraries/uri>` 对象。将此对象转换为字符串可获取当前请求的完整 URL：

.. literalinclude:: incomingrequest/020.php

该对象提供了获取请求中任何部分的完整能力：

.. literalinclude:: incomingrequest/021.php

可使用 ``getRoutePath()`` 处理当前 URI 字符串（相对于 baseURL 的路径）。

.. note:: ``getRoutePath()`` 方法自 v4.4.0 起可用。在 v4.4.0 之前，``getPath()`` 方法返回相对于 baseURL 的路径。

上传文件
**************

可通过 ``$request->getFiles()`` 获取所有上传文件的信息，该方法返回 ``CodeIgniter\HTTP\Files\UploadedFile`` 实例数组。这有助于简化上传文件的处理，并采用最佳实践以降低安全风险。

.. literalinclude:: incomingrequest/023.php

详情请参阅 :ref:`处理上传文件 <uploaded-files-accessing-files>`。

可根据 HTML 文件输入框中给定的文件名，单独获取某个上传文件：

.. literalinclude:: incomingrequest/024.php

如果是多文件上传，可根据 HTML 文件输入框中给定的文件名，获取同名上传文件的数组：

.. literalinclude:: incomingrequest/025.php

.. note:: 此处获取的文件对象本质上对应于 ``$_FILES``。即使用户仅点击表单提交按钮而未上传任何文件，该文件依然存在。可通过 UploadedFile 中的 ``isValid()`` 方法检查文件是否确实已上传。详情请参阅 :ref:`verify-a-file`。

内容协商
*******************

可通过 ``negotiate()`` 方法轻松与请求进行内容类型协商：

.. literalinclude:: incomingrequest/026.php

有关更多详情，请参阅 :doc:`内容协商 </incoming/content_negotiation>` 页面。

类参考
***************

.. note:: 除了此处列出的方法外，此类还继承了 :doc:`Request 类 </incoming/request>` 和 :doc:`Message 类 </incoming/message>` 的方法。

继承自父类的可用方法包括：

* :meth:`CodeIgniter\\HTTP\\Request::getIPAddress`
* :meth:`CodeIgniter\\HTTP\\Request::isValidIP`
* :meth:`CodeIgniter\\HTTP\\Request::getMethod`
* :meth:`CodeIgniter\\HTTP\\Request::setMethod`
* :meth:`CodeIgniter\\HTTP\\Request::getServer`
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

        :returns: 如果请求是从命令行发起的，返回 true，否则返回 false。
        :rtype: bool

    .. php:method:: isAJAX()

        :returns: 如果请求是 AJAX 请求，返回 true，否则返回 false。
        :rtype: bool

    .. php:method:: isSecure()

        :returns: 如果请求是 HTTPS 请求，返回 true，否则返回 false。
        :rtype: bool

    .. php:method:: getVar([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量名/键名。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在 `可用过滤器列表 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可在 `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:   如果未提供参数则返回 ``$_REQUEST``；如果找到则返回 REQUEST 值，未找到则返回 null。
        :rtype: array|bool|float|int|object|string|null

        .. important:: 此方法仅为了向后兼容而存在。请勿在新项目中使用。即使已经在用，也建议换用其他更合适的方法。

        此方法与 ``getGet()`` 完全相同，只是它获取的是 REQUEST 数据。

    .. php:method:: getGet([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量名/键名。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在 `可用过滤器列表 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可在 `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:       如果未提供参数则返回 ``$_GET``；如果找到则返回 GET 值，未找到则返回 null。
        :rtype: array|bool|float|int|object|string|null

        第一个参数包含要查找的 GET 项名称：

        .. literalinclude:: incomingrequest/041.php

        如果要获取的项目不存在，该方法将返回 null。

        第二个可选参数支持通过 PHP 过滤器运行数据。将所需的过滤器类型作为第二个参数传入：

        .. literalinclude:: incomingrequest/042.php

        若要返回所有 GET 项的数组，请在调用时不带任何参数。

        若要返回所有 GET 项并对其进行过滤，请将第一个参数设为 null，同时将第二个参数设为要使用的过滤器：

        .. literalinclude:: incomingrequest/043.php

        若要返回多个 GET 参数的数组，请将所有需要的键作为数组传入：

        .. literalinclude:: incomingrequest/044.php

        此处规则相同，若要在检索参数时进行过滤，请将第二个参数设为要应用的过滤器类型：

        .. literalinclude:: incomingrequest/045.php

    .. php:method:: getPost([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量名/键名。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在 `此处 <https://www.php.net/manual/zh/filters.php>`__ 找到。
        :param  int     $flags: 要应用的标志。标志列表可在 `此处 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 找到。
        :returns:       如果未提供参数则返回 ``$_POST``；如果找到则返回 POST 值，未找到则返回 null。
        :rtype: array|bool|float|int|object|string|null

        此方法与 ``getGet()`` 完全相同，只是它获取的是 POST 数据。

    .. php:method:: getPostGet([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量名/键名。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在 `可用过滤器列表 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可在 `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:       如果未指定参数，则返回合并后的 ``$_POST`` 和 ``$_GET`` （名称冲突时优先使用 POST 值）；否则先查找 POST 值，未找到则查找 GET 值，若均未找到则返回 null。
        :rtype: array|bool|float|int|object|string|null

        此方法的工作方式与 ``getPost()`` 和 ``getGet()`` 基本相同，只是将二者结合。它会同时在 POST 和 GET 流中搜索数据，先查找 POST，然后查找 GET：

        .. literalinclude:: incomingrequest/032.php

        如果未指定索引，将返回合并后的 POST 和 GET 流。若发生名称冲突，将优先使用 POST 数据。

    .. php:method:: getGetPost([$index = null[, $filter = null[, $flags = null]]])

        :param  string  $index: 要查找的变量名/键名。
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在 `可用过滤器列表 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可在 `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:       如果未指定参数，则返回合并后的 ``$_GET`` 和 ``$_POST`` （名称冲突时优先使用 GET 值）；否则先查找 GET 值，未找到则查找 POST 值，若均未找到则返回 null。
        :rtype: array|bool|float|int|object|string|null

        此方法的工作方式与 ``getPost()`` 和 ``getGet()`` 基本相同，只是将二者结合。它会同时在 GET 和 POST 流中搜索数据，先查找 GET，然后查找 POST：

        .. literalinclude:: incomingrequest/033.php

        如果未指定索引，将返回合并后的 GET 和 POST 流。若发生名称冲突，将优先使用 GET 数据。

    .. php:method:: getCookie([$index = null[, $filter = null[, $flags = null]]])

        :param  array|string|null    $index: COOKIE 名称
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在 `可用过滤器列表 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可在 `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:        如果未提供参数则返回 ``$_COOKIE``；如果找到则返回 COOKIE 值，未找到则返回 null。
        :rtype: array|bool|float|int|object|string|null

        此方法与 ``getPost()`` 和 ``getGet()`` 完全相同，只是它获取的是 Cookie 数据：

        .. literalinclude:: incomingrequest/034.php

        若要返回多个 Cookie 值的数组，请将所有需要的键作为数组传入：

        .. literalinclude:: incomingrequest/035.php

        .. note:: 与 :doc:`Cookie 辅助函数 <../helpers/cookie_helper>` 中的 :php:func:`get_cookie()` 函数不同，此方法不会自动附加配置的 ``Config\Cookie::$prefix`` 值。

    .. php:method:: getServer([$index = null[, $filter = null[, $flags = null]]])

        :param  array|string|null    $index: 值名称
        :param  int     $filter: 要应用的过滤器类型。过滤器列表可在 `可用过滤器列表 <https://www.php.net/manual/zh/filters.php>`__ 中找到。
        :param  int     $flags: 要应用的标志。标志列表可在 `过滤器标志 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到。
        :returns:        如果找到则返回 ``$_SERVER`` 项的值，未找到则返回 null。
        :rtype: array|bool|float|int|object|string|null

        此方法与 ``getPost()``、``getGet()`` 和 ``getCookie()`` 方法完全相同，只是它获取的是 Server 数据（``$_SERVER``）：

        .. literalinclude:: incomingrequest/036.php

        若要返回多个 ``$_SERVER`` 值的数组，请将所有需要的键作为数组传入。

        .. literalinclude:: incomingrequest/037.php

    .. php:method:: getUserAgent()

        :returns: SERVER 数据中的 User Agent 字符串；如果未找到则返回 null。
        :rtype: CodeIgniter\\HTTP\\UserAgent

        此方法从 SERVER 数据中返回 User Agent 实例：

        .. literalinclude:: incomingrequest/038.php

    .. php:method:: getPath()

        :returns: 当前相对于 baseURL 的 URI 路径
        :rtype: string

        此方法返回当前相对于 baseURL 的 URI 路径。

        .. note:: v4.4.0 之前，这是确定“当前 URI”最安全的方法，因为 ``IncomingRequest::$uri`` 可能无法识别应用程序中完整的基准 URL 配置。
