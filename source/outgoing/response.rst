==============
HTTP 响应
==============

Response 类继承自 :doc:`HTTP Message 类 </incoming/message>`，并添加了仅适用于服务端响应客户端请求的方法。

.. contents::
    :local:
    :depth: 2

使用 Response 类
=========================

Response 类会在控制器实例化时自动传入，可通过 ``$this->response`` 访问。它与 ``Services::response()`` 返回的是同一实例，称为全局响应实例。

多数情况下无需直接操作此类，CodeIgniter 会自动发送标头和正文。页面成功创建所需内容时，这种自动处理非常理想。但当出现错误、需要返回特定状态码，或使用强大的 HTTP 缓存功能时，就可以直接操作此实例。

设置输出
------------------

需要直接设置脚本输出而非依赖 CodeIgniter 自动设置时，可使用 ``setBody`` 方法。通常与设置响应状态码配合使用：

.. literalinclude:: response/001.php

原因短语（'OK'、'Created'、'Moved Permanently'）会自动添加，但也可在 ``setStatusCode()`` 方法的第二个参数中自定义：

.. literalinclude:: response/002.php

使用 ``setJSON()`` 和 ``setXML()`` 方法可将数组格式化为 JSON 或 XML，并将 Content-Type 标头设置为对应的 MIME 类型。通常需要发送待转换的数组数据：

.. literalinclude:: response/003.php

设置标头
---------------

setHeader()
^^^^^^^^^^^

设置响应标头时，可使用 ``setHeader()`` 方法。

第一个参数为标头名称，第二个参数为值，可以是字符串或字符串数组，发送给客户端时会自动合并。

.. literalinclude:: response/004.php

使用这些方法而非 PHP 原生函数可避免标头过早发送导致错误，同时使测试成为可能。

.. important:: v4.6.0 起，如果先使用 PHP 原生 ``header()`` 函数设置标头，再使用 ``Response`` 类设置同一标头，之前的标头将被覆盖。

.. note:: 此方法仅设置标头到响应实例。因此，如果创建并返回另一个响应实例（例如调用 :php:func:`redirect()`），此处设置的标头不会自动发送。

appendHeader()
^^^^^^^^^^^^^^

如果标头已存在且可包含多个值，可使用 ``appendHeader()`` 和 ``prependHeader()`` 方法分别在值列表末尾或开头添加新值。第一个参数为标头名称，第二个参数为待追加或前置的值。

.. literalinclude:: response/005.php

removeHeader()
^^^^^^^^^^^^^^

使用 ``removeHeader()`` 方法可移除响应标头，该方法仅接受标头名称作为参数，不区分大小写。

.. literalinclude:: response/006.php

.. _response-redirect:

重定向
========

如需创建重定向，请使用 :php:func:`redirect()` 函数。

该函数返回 ``RedirectResponse`` 实例。此实例与 ``Services::response()`` 返回的全局响应实例不同。

.. warning:: 如果在调用 ``redirect()`` 之前设置了 Cookie 或响应标头，它们会设置到全局响应实例，不会自动复制到 ``RedirectResponse`` 实例。要发送它们，需要手动调用 ``withCookies()`` 或 ``withHeaders()`` 方法。

.. important:: 如需重定向，必须在 :doc:`控制器 <../incoming/controllers>` 或 :doc:`控制器过滤器 <../incoming/filters>` 的方法中返回 ``RedirectResponse`` 实例。注意 ``__construct()`` 或 ``initController()`` 方法无法返回任何值。如果忘记返回 ``RedirectResponse``，重定向不会执行。

重定向到 URI 路径
----------------------

传递相对于 baseURL 的 URI 路径时，使用 ``redirect()->to()``：

.. literalinclude:: ./response/028.php
    :lines: 2-

.. note:: 如果 URL 中包含需移除的 fragment，可在方法中使用 refresh 参数。
    例如 ``return redirect()->to('admin/home', null, 'refresh');``。

重定向到已定义的路由
---------------------------

传递 :ref:`路由名称 <using-named-routes>` 或用于 :ref:`反向路由 <reverse-routing>` 的 Controller::method 时，使用 ``redirect()->route()``：

.. literalinclude:: ./response/029.php
    :lines: 2-

向函数传递单个参数时，会作为路由名称或 Controller::method 进行反向路由处理，而非相对/完整 URI，效果与 ``redirect()->route()`` 相同：

.. literalinclude:: ./response/030.php
    :lines: 2-

返回上一页
-------------

返回上一页时，使用 ``redirect()->back()``：

.. literalinclude:: ./response/031.php
    :lines: 2-

.. note:: ``redirect()->back()`` 与浏览器"后退"按钮不同。Session 可用时，会跳转到"Session 期间上次访问的页面"。如果 Session 未加载或不可用，则使用 HTTP_REFERER 的安全过滤版本。

带 Cookie 的重定向
---------------------

在调用 ``redirect()`` 之前设置的 Cookie 会设置到全局响应实例，不会自动复制到 ``RedirectResponse`` 实例。

要发送 Cookie，需手动调用 ``withCookies()`` 方法。

.. literalinclude:: ./response/034.php
    :lines: 2-

带标头的重定向
---------------------

在调用 ``redirect()`` 之前设置的响应标头会设置到全局响应实例，不会自动复制到 ``RedirectResponse`` 实例。

要发送标头，需手动调用 ``withHeaders()`` 方法。

.. literalinclude:: ./response/035.php
    :lines: 2-

.. _response-redirect-status-code:

重定向状态码
--------------------

GET 请求的默认 HTTP 状态码为 302。但使用 HTTP/1.1 或更高版本时，POST/PUT/DELETE 请求使用 303，其他请求使用 307。

可指定状态码：

.. literalinclude:: ./response/032.php
    :lines: 2-

.. note:: 由于 Bug，v4.3.3 或更早的版本中，即使指定了状态码，实际重定向响应的状态码可能会被更改。详见 :ref:`变更记录 v4.3.4 <v434-redirect-status-code>`。

如果不了解 HTTP 重定向状态码，建议阅读 `HTTP 重定向 <https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Redirections>`_。

.. _force-file-download:

强制文件下载
===================

Response 类提供了简便的方式向客户端发送文件，提示浏览器下载数据到本地。此方法会设置相应的标头来完成下载。

第一个参数为 **下载文件的名称**，第二个参数为文件数据。

如果第二个参数设为 null，且 ``$filename`` 是存在的、可读的文件路径，则会读取该文件内容代替。

如果第三个参数设为 true，则会发送实际的文件 MIME 类型（基于文件名后缀），以便浏览器有对应的处理程序时可直接使用。

示例：

.. literalinclude:: response/007.php

如需下载服务器上已有的文件，需将第二个参数显式设为 ``null``：

.. literalinclude:: response/008.php

使用可选的 ``setFileName()`` 方法可更改发送到浏览器的文件名：

.. literalinclude:: response/009.php

.. note:: 响应对象必须被返回才能发送下载内容到客户端。由此响应可经过所有 **after** 过滤器后再发送给客户端。

.. _open-file-in-browser:

在浏览器中打开文件
--------------------

部分浏览器可显示 PDF 等文件。如需让浏览器直接显示而非保存文件，可调用 ``DownloadResponse::inline()`` 方法。

.. literalinclude:: response/033.php

HTTP 缓存
============

HTTP 规范内置了帮助客户端（通常为 Web 浏览器）缓存结果的工具。正确使用可大幅提升应用性能，因为客户端在内容未变更时无需再与服务端通信。没有比这更快的响应速度了。

通过 ``Cache-Control`` 和 ``ETag`` 标头来实现缓存。本指南不适合深入介绍所有缓存标头，可在 `Google 开发者文档 <https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching>`_ 获取详细说明。

默认情况下，通过 CodeIgniter 发送的所有响应对象都关闭了 HTTP 缓存。由于缓存选项和使用场景过于多样，无法设定合适的默认值，因此默认关闭。使用 ``setCache()`` 方法即可轻松设置所需的缓存值：

.. literalinclude:: response/010.php

``$options`` 接收关联数组形式的缓存控制选项（少数例外），主要应用于 ``Cache-Control`` 标头。可根据具体需求自由设置所有选项。虽然多数选项应用于 ``Cache-Control`` 标头，但 ``etag`` 和 ``last-modified`` 选项会智能地分配到对应的标头。

类参考
===============

.. note:: 除以下列出的方法外，此类还继承了
    :doc:`Message 类 </incoming/message>` 的方法。

继承自 Message 类的方法：

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
        :param string $reason: 可选的原因短语
        :returns: 当前 Response 实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置响应应发送的 HTTP 状态码：

        .. literalinclude:: response/015.php

        原因短语会根据官方列表自动生成。如需为自定义状态码设置原因短语，可将其作为第二个参数传入：

        .. literalinclude:: response/016.php

    .. php:method:: getReasonPhrase()

        :returns: 当前原因短语
        :rtype: string

        返回当前响应的状态码。如果未设置状态码，将返回空字符串：

        .. literalinclude:: response/017.php

    .. php:method:: setDate($date)

        :param DateTime $date: 用于设置响应时间的 DateTime 实例
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置响应的日期。``$date`` 参数必须是 ``DateTime`` 实例。

    .. php:method:: setContentType($mime[, $charset='UTF-8'])

        :param string $mime: 响应表示的内容类型
        :param string $charset: 响应使用的字符集
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置响应的内容类型：

        .. literalinclude:: response/019.php

        默认情况下，方法将字符集设为 ``UTF-8``。如需更改，可在第二个参数中传入字符集：

        .. literalinclude:: response/020.php

    .. php:method:: noCache()

        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置 ``Cache-Control`` 标头以关闭所有 HTTP 缓存。这是所有响应消息的默认设置：

        .. literalinclude:: response/021.php

    .. php:method:: setCache($options)

        :param array $options: 关联数组形式的缓存控制选项
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置 ``Cache-Control`` 标头，包括 ``ETags`` 和 ``Last-Modified``。常用选项：

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

        :param string|DateTime $date: 用于设置 Last-Modified 标头的日期
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置 ``Last-Modified`` 标头。``$date`` 对象可以是字符串或 ``DateTime`` 实例：

        .. literalinclude:: response/022.php

    .. php:method:: send(): Response

        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        告知响应将所有内容发送回客户端。会先发送标头，再发送响应正文。主应用的响应由 CodeIgniter 自动处理，无需手动调用此方法。

    .. php:method:: setCookie($name = ''[, $value = ''[, $expire = 0[, $domain = ''[, $path = '/'[, $prefix = ''[, $secure = false[, $httponly = false[, $samesite = null]]]]]]]])

        :param array|Cookie|string $name: Cookie 名称，或包含此方法所有可用参数的关联数组，或 ``CodeIgniter\Cookie\Cookie`` 实例
        :param string $value: Cookie 值
        :param int $expire: Cookie 过期时间（秒）。设为 ``0`` 时 Cookie 仅在浏览器打开期间有效
        :param string $domain: Cookie 域名
        :param string $path: Cookie 路径
        :param string $prefix: Cookie 名称前缀。设为 ``''`` 时使用 **app/Config/Cookie.php** 中的默认值
        :param bool $secure: 是否仅通过 HTTPS 传输 Cookie。设为 ``null`` 时使用 **app/Config/Cookie.php** 中的默认值
        :param bool $httponly: 是否仅允许 HTTP 请求访问 Cookie（禁止 JavaScript）。设为 ``null`` 时使用 **app/Config/Cookie.php** 中的默认值
        :param string $samesite: SameSite Cookie 参数的值。设为 ``''`` 时不设置 SameSite 属性。设为 ``null`` 时使用 **app/Config/Cookie.php** 中的默认值
        :rtype: void

        .. note:: v4.2.7 之前，由于 Bug，``$secure`` 和 ``$httponly`` 默认值为 ``false``，从未使用 **app/Config/Cookie.php** 中的值。

        将指定值的 Cookie 设置到 Response 实例。

        有两种方式可传递信息以设置 Cookie：数组方式和独立参数方式：

        **数组方式**

        此方式下，关联数组作为第一个参数传入：

        .. literalinclude:: response/023.php

        仅 ``name`` 和 ``value`` 是必需的。要删除 Cookie 可将其 ``value`` 设为空。

        ``expire`` 以 **秒** 为单位设置，会加到当前时间上。不要包含具体时间，而是填入从 *此刻* 起 Cookie 有效的秒数。如果 ``expire`` 设为零，Cookie 仅在浏览器打开期间有效。

        .. note:: 但如果 ``value`` 设为空字符串且 ``expire`` 设为 ``0``，Cookie 将被删除。

        无论站点如何被访问，要设置全站 Cookie，可在 ``domain`` 前加点，例如：
        .your-domain.com

        通常无需设置 ``path``，因为方法默认使用根路径。

        仅当需要避免服务器同名 Cookie 冲突时才需要 ``prefix``。

        仅当需要设为安全 Cookie 时，才将 ``secure`` 标志设为 ``true``。

        ``samesite`` 值控制 Cookie 如何在域名和子域名之间共享。允许值为 ``'None'``、``'Lax'``、``'Strict'`` 或空字符串 ``''``。设为空字符串时，将设置默认 SameSite 属性。

        **独立参数方式**

        也可通过独立参数设置 Cookie：

        .. literalinclude:: response/024.php

    .. php:method:: deleteCookie($name = ''[, $domain = ''[, $path = '/'[, $prefix = '']]])

        :param mixed $name: Cookie 名称或参数数组
        :param string $domain: Cookie 域名
        :param string $path: Cookie 路径
        :param string $prefix: Cookie 名称前缀
        :rtype: void

        删除已有 Cookie。

        .. note:: 此方法仅设置浏览器端删除 Cookie 的响应。

        仅 ``name`` 是必需的。

        仅当需要避免服务器同名 Cookie 冲突时才需要 ``prefix``。

        提供 ``prefix`` 时，仅删除该前缀下的 Cookie。
        提供 ``domain`` 时，仅删除该域名下的 Cookie。
        提供 ``path`` 时，仅删除该路径下的 Cookie。

        如果可选参数留空，则删除所有匹配名称的 Cookie。

        示例：

        .. literalinclude:: response/025.php

    .. php:method:: hasCookie($name = ''[, $value = null[, $prefix = '']])

        :param mixed $name: Cookie 名称或参数数组
        :param string $value: Cookie 值
        :param string $prefix: Cookie 名称前缀
        :rtype: bool

        检查 Response 是否包含指定的 Cookie。

        **说明**

        仅 ``name`` 是必需的。如果指定了 ``prefix``，会加到 Cookie 名称前。

        未提供 ``value`` 时，仅检查 Cookie 是否存在。
        提供了 ``value`` 时，检查 Cookie 是否存在且值匹配。

        示例：

        .. literalinclude:: response/026.php

    .. php:method:: getCookie($name = ''[, $prefix = ''])

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 名称前缀
        :rtype: ``Cookie|Cookie[]|null``

        返回指定的 Cookie，未找到时返回 ``null``。
        未提供 ``name`` 时，返回 ``Cookie`` 对象数组。

        示例：

        .. literalinclude:: response/027.php

    .. php:method:: getCookies()

        :rtype: ``Cookie[]``

        返回当前 Response 实例中设置的所有 Cookie。
        其中仅包含当前请求中明确指定要设置的 Cookie。
