==============
HTTP 响应
==============

Response 类继承自 :doc:`HTTP 消息类 </incoming/message>`，并添加了仅适用于服务器响应客户端请求的方法。

.. contents::
    :local:
    :depth: 2

使用响应类
=========================

系统会自动为你实例化一个 Response 类，并传递给你的控制器。你可以通过 ``$this->response`` 访问它。它与 ``Services::response()`` 返回的是同一个实例，我们称之为全局响应实例。

很多时候你不需要直接操作该类，因为 CodeIgniter 会自动处理头部和内容的发送。这在页面成功生成所需内容时非常方便。当出现错误、需要发送特定状态码或利用强大的 HTTP 缓存功能时，你可以直接使用该类。

设置输出内容
------------------

当需要直接设置脚本输出内容，而不依赖 CodeIgniter 自动获取时，可以使用 ``setBody`` 方法手动设置。通常与设置响应状态码配合使用：

.. literalinclude:: response/001.php

原因短语（'OK'、'Created'、'Moved Permanently'）会自动添加，但你也可以通过 ``setStatusCode()`` 方法的第二个参数自定义原因短语：

.. literalinclude:: response/002.php

你可以使用 ``setJSON()`` 和 ``setXML()`` 方法将数组格式化为 JSON 或 XML，并设置相应的内容类型头部。通常你会发送一个待转换的数据数组：

.. literalinclude:: response/003.php

设置头部
---------------

setHeader()
^^^^^^^^^^^

通常需要为响应设置头部。Response 类通过 ``setHeader()`` 方法简化了这个操作。

第一个参数是头部名称。第二个参数是值，可以是字符串或将被正确组合的值数组：

.. literalinclude:: response/004.php

使用这些方法代替原生 PHP 函数可以确保头部不会过早发送导致错误，并支持测试。

.. important:: 自 v4.6.0 起，如果使用 PHP 原生 ``header()`` 函数设置头部后，再通过 ``Response`` 类设置相同头部，前者将被覆盖。

.. note:: 此方法仅将头部设置到响应实例。因此，如果创建并返回另一个响应实例（例如调用 :php:func:`redirect()`），此处设置的头部不会自动发送。

appendHeader()
^^^^^^^^^^^^^^

如果头部已存在且允许多个值，可以使用 ``appendHeader()`` 和 ``prependHeader()`` 方法分别在值列表末尾或开头添加值。第一个参数是头部名称，第二个是要追加或前置的值：

.. literalinclude:: response/005.php

removeHeader()
^^^^^^^^^^^^^^

可以通过 ``removeHeader()`` 方法移除响应中的头部，参数为不区分大小写的头部名称：

.. literalinclude:: response/006.php

.. _response-redirect:

重定向
========

如需创建重定向，请使用 :php:func:`redirect()` 函数。

该函数返回一个 ``RedirectResponse`` 实例。这与 ``Services::response()`` 返回的全局响应实例不同。

.. warning:: 如果在调用 ``redirect()`` 前设置了 Cookie 或响应头部，它们会被设置到全局响应实例，而不会自动复制到 ``RedirectResponse`` 实例。要发送它们，需手动调用 ``withCookies()`` 或 ``withHeaders()`` 方法。

.. important:: 若要进行重定向，必须在 :doc:`控制器 <../incoming/controllers>` 或 :doc:`控制器过滤器 <../incoming/filters>` 的方法中返回 ``RedirectResponse`` 实例。注意 ``__construct()`` 或 ``initController()`` 方法不能返回任何值。如果忘记返回 ``RedirectResponse``，将不会发生重定向。

重定向到 URI 路径
----------------------

当需要传递相对于 baseURL 的 URI 路径时，使用 ``redirect()->to()``：

.. literalinclude:: ./response/028.php
    :lines: 2-

.. note:: 如果 URL 中包含需要移除的片段，可以在方法中使用 refresh 参数。例如 ``return redirect()->to('admin/home', null, 'refresh');``。

重定向到定义的路由
---------------------------

当需要传递 :ref:`路由名称 <using-named-routes>` 或用于 :ref:`反向路由 <reverse-routing>` 的 Controller::method 时，使用 ``redirect()->route()``：

.. literalinclude:: ./response/029.php
    :lines: 2-

当向函数传递参数时，会被视为反向路由的路由名称或 Controller::method，而非相对/完整 URI，效果等同于使用 ``redirect()->route()``：

.. literalinclude:: ./response/030.php
    :lines: 2-

返回重定向
-------------

当需要返回上一页时，使用 ``redirect()->back()``：

.. literalinclude:: ./response/031.php
    :lines: 2-

.. note:: ``redirect()->back()`` 与浏览器 "返回" 按钮不同。当 Session 可用时，它会将访问者带到 "Session 期间最后查看的页面"。如果 Session 未加载或不可用，则会使用经过处理的 HTTP_REFERER。

带 Cookie 的重定向
---------------------

如果在调用 ``redirect()`` 前设置了 Cookie，它们会被设置到全局响应实例，而不会自动复制到 ``RedirectResponse`` 实例。

要发送这些 Cookie，需手动调用 ``withCookies()`` 方法：

.. literalinclude:: ./response/034.php
    :lines: 2-

带头部的重定向
---------------------

如果在调用 ``redirect()`` 前设置了响应头部，它们会被设置到全局响应实例，而不会自动复制到 ``RedirectResponse`` 实例。

要发送这些头部，需手动调用 ``withHeaders()`` 方法：

.. literalinclude:: ./response/035.php
    :lines: 2-

.. _response-redirect-status-code:

重定向状态码
--------------------

GET 请求的默认 HTTP 状态码是 302。但在使用 HTTP/1.1 或更高版本时，POST/PUT/DELETE 请求使用 303，其他请求使用 307。

可以指定状态码：

.. literalinclude:: ./response/032.php
    :lines: 2-

.. note:: 由于漏洞，在 v4.3.3 或更早版本中，即使指定了状态码，实际重定向响应的状态码也可能被更改。详见 :ref:`更新日志 v4.3.4 <v434-redirect-status-code>`。

如果不了解 HTTP 重定向状态码，建议阅读 `HTTP 重定向 <https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Redirections>`_。

.. _force-file-download:

强制文件下载
===================

Response 类提供了向客户端发送文件并提示浏览器下载的简便方法。它会设置适当的头部来实现此功能。

第一个参数是 **下载文件的名称**，第二个参数是文件数据。

如果第二个参数设为 null 且 ``$filename`` 是存在的可读文件路径，则会读取该文件内容。

如果第三个参数设为 true，则会发送实际的文件 MIME 类型（基于文件扩展名），以便浏览器使用对应的处理器。

示例：

.. literalinclude:: response/007.php

如果要下载服务器上的现有文件，需显式将第二个参数设为 ``null``：

.. literalinclude:: response/008.php

使用可选的 ``setFileName()`` 方法修改发送到客户端浏览器的文件名：

.. literalinclude:: response/009.php

.. note:: 必须返回响应对象才能将下载内容发送到客户端。这允许响应在发送前通过所有 **after** 过滤器。

.. _open-file-in-browser:

在浏览器中打开文件
--------------------

某些浏览器可以显示 PDF 等文件。要告知浏览器显示而非保存文件，可调用 ``DownloadResponse::inline()`` 方法：

.. literalinclude:: response/033.php

HTTP 缓存
============

HTTP 规范内置了帮助客户端（通常是浏览器）缓存结果的工具。正确使用可以极大提升应用性能，因为它会告知客户端无需联系服务器（当内容未变化时）。

这通过 ``Cache-Control`` 和 ``ETag`` 头部实现。本指南不深入讲解所有缓存头部，但你可以通过 `Google 开发者文档 <https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching>`_ 获得详细理解。

默认情况下，CodeIgniter 发送的所有响应对象都关闭了 HTTP 缓存。由于场景差异过大，我们选择关闭作为默认设置。你可以通过 ``setCache()`` 方法轻松设置所需缓存值：

.. literalinclude:: response/010.php

``$options`` 数组接收键值对，除个别例外，这些参数会被分配到 ``Cache-Control`` 头部。你可以根据具体需求自由设置所有选项。虽然大多数选项应用于 ``Cache-Control`` 头部，但该方法会智能处理 ``etag`` 和 ``last-modified`` 选项到对应头部。

类参考
===============

.. note:: 除了列出的方法外，此类继承自 :doc:`消息类 </incoming/message>` 的方法。

继承自消息类的方法包括：

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

.. php:namespace:: CodeIgniter\HTTP

.. php:class:: Response

    .. php:method:: getStatusCode()

        :returns: 当前响应的 HTTP 状态码
        :rtype: int

        返回当前响应的状态码。如果未设置状态码，将抛出 BadMethodCallException：

        .. literalinclude:: response/014.php

    .. php:method:: setStatusCode($code[, $reason=''])

        :param int $code: HTTP 状态码
        :param string $reason: 可选原因短语
        :returns: 当前 Response 实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置响应应发送的 HTTP 状态码：

        .. literalinclude:: response/015.php

        原因短语会根据官方列表自动生成。如需为自定义状态码设置短语，可通过第二个参数传递：

        .. literalinclude:: response/016.php

    .. php:method:: getReasonPhrase()

        :returns: 当前原因短语
        :rtype: string

        返回当前响应的原因短语。如果未设置状态码，则返回空字符串：

        .. literalinclude:: response/017.php

    .. php:method:: setDate($date)

        :param DateTime $date: 包含响应时间的 DateTime 实例
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置响应日期。``$date`` 参数必须是 ``DateTime`` 实例。

    .. php:method:: setContentType($mime[, $charset='UTF-8'])

        :param string $mime: 响应内容类型
        :param string $charset: 响应字符集
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置响应内容类型：

        .. literalinclude:: response/019.php

        默认字符集为 ``UTF-8``。如需修改，可通过第二个参数传递：

        .. literalinclude:: response/020.php

    .. php:method:: noCache()

        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置 ``Cache-Control`` 头部关闭所有 HTTP 缓存。这是所有响应消息的默认设置：

        .. literalinclude:: response/021.php

    .. php:method:: setCache($options)

        :param array $options: 缓存控制键值对数组
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置 ``Cache-Control`` 头部，包括 ``ETags`` 和 ``Last-Modified``。常用键包括：

        * etag
        * last-modified
        * max-age
        * s-maxage
        * private
        * public
        * must-revalidate
        * proxy-revalidate
        * no-transform

        传递 last-modified 选项时，可以是日期字符串或 DateTime 对象。

    .. php:method:: setLastModified($date)

        :param string|DateTime $date: 设置 Last-Modified 头部的日期
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置 ``Last-Modified`` 头部。``$date`` 可以是字符串或 ``DateTime`` 实例：

        .. literalinclude:: response/022.php

    .. php:method:: send(): Response

        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        指示响应将所有内容发送回客户端。这会先发送头部，再发送响应体。主应用响应无需手动调用此方法，CodeIgniter 会自动处理。

    .. php:method:: setCookie($name = ''[, $value = ''[, $expire = 0[, $domain = ''[, $path = '/'[, $prefix = ''[, $secure = false[, $httponly = false[, $samesite = null]]]]]]]])

        :param array|Cookie|string $name: Cookie 名称 *或* 包含本方法所有参数的关联数组 *或* ``CodeIgniter\Cookie\Cookie`` 实例
        :param string $value: Cookie 值
        :param int $expire: Cookie 过期时间（秒）。设为 ``0`` 时 Cookie 仅在浏览器打开期间有效
        :param string $domain: Cookie 域名
        :param string $path: Cookie 路径
        :param string $prefix: Cookie 名称前缀。设为 ``''`` 时使用 **app/Config/Cookie.php** 的默认值
        :param bool $secure: 是否仅通过 HTTPS 传输。设为 ``null`` 时使用 **app/Config/Cookie.php** 的默认值
        :param bool $httponly: 是否仅允许 HTTP 请求访问（禁止 JavaScript）。设为 ``null`` 时使用 **app/Config/Cookie.php** 的默认值
        :param string $samesite: SameSite 参数值。设为 ``''`` 时不设置该属性。设为 ``null`` 时使用 **app/Config/Cookie.php** 的默认值
        :rtype: void

        .. note:: 在 v4.2.7 之前，由于漏洞，``$secure`` 和 ``$httponly`` 的默认值为 ``false``，且 **app/Config/Cookie.php** 中的值未被使用。

        向响应实例设置包含指定值的 Cookie。

        有两种传递信息设置 Cookie 的方式：数组法和离散参数法。

        **数组法**

        使用此方法时，第一个参数传递关联数组：

        .. literalinclude:: response/023.php

        仅需 ``name`` 和 ``value``。要删除 Cookie 可将 ``value`` 设为空。

        ``expire`` 以秒为单位，会添加到当前时间。请勿包含具体时间，只需设置从现在起有效的秒数。设为 ``0`` 时 Cookie 仅在浏览器打开期间有效。

        .. note:: 但如果 ``value`` 设为空字符串且 ``expire`` 为 ``0``，Cookie 将被删除。

        要为整个站点设置 Cookie（无论请求方式），域名前加句点，如：.your-domain.com

        通常无需设置 ``path``，因为方法默认使用根路径。

        仅在需要避免服务器上同名 Cookie 冲突时需设置 ``prefix``。

        仅在需要安全 Cookie 时设置 ``secure`` 为 ``true``。

        ``samesite`` 控制 Cookie 在域和子域间的共享方式。允许值为 ``'None'``、``'Lax'``、``'Strict'`` 或空字符串 ``''``。设为空字符串时使用默认 SameSite 属性。

        **独立参数**

        也可通过独立参数设置 Cookie：

        .. literalinclude:: response/024.php

    .. php:method:: deleteCookie($name = ''[, $domain = ''[, $path = '/'[, $prefix = '']]])

        :param mixed $name: Cookie 名称或参数数组
        :param string $domain: Cookie 域名
        :param string $path: Cookie 路径
        :param string $prefix: Cookie 名称前缀
        :rtype: void

        删除现有 Cookie。

        .. note:: 此方法只是设置浏览器 Cookie 来删除 Cookie。

        仅需 ``name`` 参数。

        仅在需要避免服务器上同名 Cookie 冲突时需设置 ``prefix``。

        设置 ``prefix`` 可限定仅删除该前缀的 Cookie。设置 ``domain`` 可限定仅删除该域名的 Cookie。设置 ``path`` 可限定仅删除该路径的 Cookie。

        如果任意可选参数为空，则删除所有符合条件的同名 Cookie。

        示例：

        .. literalinclude:: response/025.php

    .. php:method:: hasCookie($name = ''[, $value = null[, $prefix = '']])

        :param mixed $name: Cookie 名称或参数数组
        :param string $value: Cookie 值
        :param string $prefix: Cookie 名称前缀
        :rtype: bool

        检查响应是否包含指定 Cookie。

        **注意**

        仅需 ``name`` 参数。若指定 ``prefix``，会将其预置到 Cookie 名称前。

        若未提供 ``value``，仅检查是否存在该名称的 Cookie。
        若提供 ``value``，则同时检查 Cookie 是否存在且值匹配。

        示例：

        .. literalinclude:: response/026.php

    .. php:method:: getCookie($name = ''[, $prefix = ''])

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 名称前缀
        :rtype: ``Cookie|Cookie[]|null``

        返回找到的指定 Cookie，未找到则返回 ``null``。
        若未提供 ``name``，返回所有 ``Cookie`` 对象数组。

        示例：

        .. literalinclude:: response/027.php

    .. php:method:: getCookies()

        :rtype: ``Cookie[]``

        返回响应实例中当前设置的所有 Cookie。
        这些是你在本次请求中明确指定要设置的 Cookie。
