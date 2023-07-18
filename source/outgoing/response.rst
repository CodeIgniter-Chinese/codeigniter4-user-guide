==============
HTTP 响应
==============

Response 类通过只适合服务器对调用它的客户端做出响应的方法来扩展 :doc:`HTTP 消息类 </incoming/message>` 。

.. contents::
    :local:
    :depth: 2

使用响应
=========================

一个 Response 类实例会为您实例化并传入控制器中。它可以通过 ``$this->response`` 访问。许多时候您不需要直接接触该类,因为 CodeIgniter 会为您发送 header 和 body。如果页面成功地创建了它被要求的内容,情况就是这样。当事情出错时,或者您需要发送非常具体的状态码回应,或者利用 HTTP 缓存的强大功能,它就为您提供了这些。

设置输出
------------------

当您需要直接设置脚本的输出,而不依赖于 CodeIgniter 自动获取时,您可以用 ``setBody`` 方法手动设置。这通常与设置响应的状态码一起使用:

.. literalinclude:: response/001.php

原因短语(“OK”、“Created”、“Moved Permanently”)将被自动添加,但您可以在 ``setStatusCode()`` 方法的第二个参数中添加自定义原因:

.. literalinclude:: response/002.php

您可以将一个数组格式化为 JSON 或 XML,并通过 ``setJSON`` 和 ``setXML`` 方法将 content type header 设置为适当的 MIME 类型。通常,您会传递一个数据数组进行转换:

.. literalinclude:: response/003.php

设置标题
---------------

您经常需要为响应设置标题。Response 类使得这非常简单,通过 ``setHeader()`` 方法。第一个参数是标题的名称。第二个参数是值,可以是字符串或在发送到客户端时将正确组合的字符串数组。与使用原生 PHP 函数相比,使用这些函数可以确保标题不会过早发送,从而造成错误,并使测试成为可能。

.. literalinclude:: response/004.php

如果标题已经存在且可以有多个值,则可以使用 ``appendHeader()`` 和 ``prependHeader()`` 方法将值添加到值列表的末尾或开头。第一个参数是标题名称,第二个参数是要追加或前置的价值。

.. literalinclude:: response/005.php

可以使用 ``removeHeader()`` 方法从响应中删除标题,该方法仅将标题名称作为唯一参数。这不区分大小写。

.. literalinclude:: response/006.php

.. _response-redirect:

重定向
========

如果您想要创建一个重定向,请使用 :php:func:`redirect()` 函数。
它将返回一个 ``RedirectResponse`` 实例。

.. important:: 如果您想要重定向,必须在 :doc:`Controller <../incoming/controllers>`
    或 :doc:`Controller Filter <../incoming/filters>` 的方法中返回 ``RedirectResponse`` 实例。
    请注意,``__construct()`` 或 ``initController()`` 方法不能返回任何值。
    如果您忘记返回 ``RedirectResponse``,将不会发生重定向。

重定向到一个 URI 路径
----------------------

当您想传递一个 URI 路径(相对于 baseURL)时,使用 ``redirect()->to()``:

.. literalinclude:: ./response/028.php
    :lines: 2-

.. note:: 如果您的 URL 中有一个您想要删除的片段,您可以在该方法中使用 refresh 参数。
    就像 ``return redirect()->to('admin/home', null, 'refresh');`` 一样。

重定向到定义的路由
---------------------------

当您想传递一个 :ref:`路由名称 <using-named-routes>` 或 Controller::method
进行 :ref:`反向路由 <reverse-routing>` 时,使用 ``redirect()->route()``:

.. literalinclude:: ./response/029.php
    :lines: 2-

当将参数传递到函数中时,它被视为路由名称或 Controller::method 进行反向路由,而不是相对/完整 URI,
它的处理方式与使用 ``redirect()->route()`` 相同:

.. literalinclude:: ./response/030.php
    :lines: 2-

重定向回上一页面
-------------

当您想要重定向回上一页面时,使用 ``redirect()->back()``:

.. literalinclude:: ./response/031.php
    :lines: 2-

.. note:: ``redirect()->back()`` 与浏览器的“后退”按钮不同。
    当 Session 可用时,它会将访问者带到“在 Session 期间查看的最后一页”。
    如果没有加载 Session,或者 Session 不可用,那么将使用 HTTP_REFERER 的安全版本。

.. _response-redirect-status-code:

重定向状态码
--------------------

GET 请求的默认 HTTP 状态码是 302。但是,当使用 HTTP/1.1
或更高版本时,对于 POST/PUT/DELETE 请求使用 303,对于所有其他请求使用 307。

您可以指定状态码:

.. literalinclude:: ./response/032.php
    :lines: 2-

.. note:: 由于一个错误,在 v4.3.3 或更早版本中,即使指定了状态码,
    实际重定向响应的状态码也可能被改变。
    请参阅 :ref:`ChangeLog v4.3.4 <v434-redirect-status-code>`。

如果您不知道重定向的 HTTP 状态码,建议阅读
`Redirections in HTTP <https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections>`_。

.. _force-file-download:

强制文件下载
===================

Response 类提供了一种简单的方法来将文件发送给客户端,提示浏览器下载数据到计算机。这会设置适当的头使其发生。

第一个参数是**希望下载的文件的名称**,第二个参数是文件数据。

如果将第二个参数设置为 null,且 ``$filename`` 是一个存在的可读文件路径,
则将读取其内容。

如果将第三个参数设置为布尔值 true,那么将发送实际的基于文件名扩展名的文件 MIME 类型,
所以如果浏览器有该类型的处理程序,就可以使用它。

示例:

.. literalinclude:: response/007.php

如果您想从服务器下载现有文件,您需要为第二个参数显式传递 ``null`` :

.. literalinclude:: response/008.php

使用可选的 ``setFileName()`` 方法可以更改发送到客户端浏览器的文件名:

.. literalinclude:: response/009.php

.. note:: 必须返回响应对象以便下载被发送到客户端。这允许在被发送到客户端之前通过所有的 **after** 过滤器来传递响应。

HTTP 缓存
============

内置于 HTTP 规范的是帮助客户端(通常是网页浏览器)缓存结果的工具。如果使用正确,这可以为您的应用程序带来巨大的性能提升,因为它会告诉客户端他们不需要联系服务器,因为没有变化。您再也找不到更快的了。

这是通过 ``Cache-Control`` 和 ``ETag`` 头处理的。本指南不是适合对所有缓存头功能进行透彻的介绍,但是您可以在 `Google Developers <https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching>`_ 上很好地理解它。

默认情况下,通过 CodeIgniter 发送的所有响应对象都关闭了 HTTP 缓存。由于我们无法创建一个好的默认值,除了关闭它之外的选项太多了。根据您的需要设置缓存值非常简单,可以通过 ``setCache()`` 方法完成:

.. literalinclude:: response/010.php

``$options`` 数组简单地以 key/value 对的形式获取通常分配给 ``Cache-Control`` 头的数组。您可以自由地根据具体情况完全设置所需的所有选项。虽然大多数选项应用于 ``Cache-Control`` 头,但它也智能地处理 ``etag`` 和 ``last-modified`` 选项到适当的头。

.. _content-security-policy:

内容安全策略
=======================

防止站点遭受 XSS 攻击的最佳保护之一是在站点上实现内容安全策略。这会强制您列出站点 HTML 中拉入的每一个内容源,包括图像、样式表、javascript 文件等。浏览器将拒绝不符合白名单的内容源。这个白名单在响应的 ``Content-Security-Policy`` 头中创建,可以用多种不同的方式进行配置。

这听起来很复杂,在一些网站上,确实可能具有挑战性。但是,对于许多简单的网站来说,其中所有内容都由同一域服务(http://example.com), integrating 它非常简单。

由于这是一个复杂的主题,本用户指南不会详细介绍所有细节。欲了解更多信息,您应访问以下网站:

* `Content Security Policy 主站点 <https://content-security-policy.com/>`_
* `W3C 规范 <https://www.w3.org/TR/CSP>`_
* `HTML5Rocks 入门 <https://www.html5rocks.com/en/tutorials/security/content-security-policy/>`_
* `SitePoint 的文章 <https://www.sitepoint.com/improving-web-security-with-the-content-security-policy/>`_

打开 CSP
--------------

.. important:: :ref:`Debug 工具栏 <the-debug-toolbar>` 可能使用 Kint,它
    输出内联脚本。因此,打开 CSP 时,Debug 工具栏的 CSP nonce 将自动输出。
    但是,如果您不使用 CSP nonce,这将改变 CSP 头以实现您不打算的方式,
    它的行为与生产环境不同;如果您想验证 CSP 的行为,请关闭 Debug 工具栏。

默认情况下,不支持此功能。要在应用程序中启用支持,请编辑 **app/Config/App.php** 中的 ``CSPEnabled`` 值:

.. literalinclude:: response/011.php

启用后,响应对象将包含 ``CodeIgniter\HTTP\ContentSecurityPolicy`` 的一个实例。
**app/Config/ContentSecurityPolicy.php** 中设置的值将应用于该实例,如果运行时不需要更改,那么格式正确的头将被发送,您就完成了。

启用 CSP 后,会向 HTTP 响应添加两行头:一个是 **Content-Security-Policy** 头,其中包含策略以标识在不同上下文中明确允许的内容类型或来源;另一个是 **Content-Security-Policy-Report-Only** 头,它标识将被允许但也将报告给您选择的目标的内容类型或来源。

我们的实现提供了对默认处理的支持,可以通过 ``reportOnly()`` 方法更改。
当向 CSP 指令添加额外条目时,如下所示,它将添加到适当的用于阻止或防止的 CSP 头中。这可以在每次调用的基础上通过提供可选的第二个参数来覆盖。

运行时配置
---------------------

如果您的应用程序需要在运行时进行更改,您可以在控制器中通过 ``$this->response->getCSP()`` 访问实例。
该类包含许多与适当的头值映射非常清楚的方法。示例如下,使用不同的组合参数,尽管所有这些“添加”方法都接受指令名称或指令名称数组:

.. literalinclude:: response/012.php

每个“添加”方法的第一个参数是一个适当的字符串值或值数组。

``reportOnly()`` 方法允许您为后续源指定默认报告处理,除非被覆盖。例如,您可以指定 youtube.com 被允许,然后提供几个允许但报告的源:

.. literalinclude:: response/013.php

内联内容
--------------

可以将网站设置为不保护自己页面上的内联脚本和样式,因为这可能是用户生成内容的结果。为了防止这种情况,CSP 允许您在 ``<style>`` 和 ``<script>`` 标签中指定一个 nonce,并将这些值添加到响应的头中。这在实际生活中是一个痛点,但是在代码中生成效果最好。为了简化这一过程,您可以在标签中包含一个 ``{csp-style-nonce}`` 或 ``{csp-script-nonce}`` 占位符,它将自动为您处理::

    // 原始的
    <script {csp-script-nonce}>
        console.log("Script won't run as it doesn't contain a nonce attribute");
    </script>

    // 变为
    <script nonce="Eskdikejidojdk978Ad8jf">
        console.log("Script won't run as it doesn't contain a nonce attribute");
    </script>

    // 或者
    <style {csp-style-nonce}>
        . . .
    </style>

.. warning:: 如果攻击者注入类似 ``<script {csp-script-nonce}>`` 的字符串,它可能会成为带有这个功能的真正 nonce 属性。您可以在 **app/Config/ContentSecurityPolicy.php** 中使用 ``$scriptNonceTag`` 和 ``$styleNonceTag`` 属性自定义占位符字符串。

如果您不喜欢这种自动替换功能,可以在 **app/Config/ContentSecurityPolicy.php** 中设置 ``$autoNonce = false`` 来关闭它。

在这种情况下,您可以使用函数 :php:func:`csp_script_nonce()` 和 :php:func:`csp_style_nonce()` ::

	// 原始的
	<script <?= csp_script_nonce() ?>>
		console.log("Script won't run as it doesn't contain a nonce attribute");
	</script>

	// 变为
	<script nonce="Eskdikejidojdk978Ad8jf">
		console.log("Script won't run as it doesn't contain a nonce attribute");
	</script>

	// 或者
	<style <?= csp_style_nonce() ?>>
		. . .
	</style>

类参考
===============

.. note:: 除了这里列出的方法之外,该类还继承了 :doc:`消息类 </incoming/message>` 的方法。

父类提供的可用方法有:

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

        :returns: 当前 HTTP 状态码
        :rtype: int

        返回当前响应的状态码。如果没有设置状态码,将抛出 BadMethodCallException:

        .. literalinclude:: response/014.php

    .. php:method:: setStatusCode($code[, $reason=''])

        :param int $code: HTTP 状态码
        :param string $reason: 可选的原因短语
        :returns: 当前的 Response 实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置应随此响应一起发送的 HTTP 状态码:

        .. literalinclude:: response/015.php

        原因短语将根据官方列表自动生成。如果您需要为自定义状态码设置自己的原因短语,可以将原因短语作为第二个参数传递:

        .. literalinclude:: response/016.php

    .. php:method:: getReasonPhrase()

        :returns: 当前的原因短语
        :rtype: string

        返回当前状态码的原因短语。如果未设置状态,将返回空字符串:

        .. literalinclude:: response/017.php

    .. php:method:: setDate($date)

        :param DateTime $date: 带有要为此响应设置时间的 DateTime 实例
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置此响应使用的日期。``$date`` 参数必须是一个 ``DateTime`` 实例。

    .. php:method:: setContentType($mime[, $charset='UTF-8'])

        :param string $mime: 此响应所代表的内容类型
        :param string $charset: 此响应使用的字符集
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置此响应所代表的内容类型:

        .. literalinclude:: response/019.php

        默认情况下,该方法将字符集设置为 ``UTF-8``。如果需要更改此设置,可以将字符集作为第二个参数传递:

        .. literalinclude:: response/020.php

    .. php:method:: noCache()

        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置 ``Cache-Control`` 头关闭所有 HTTP 缓存。这是所有响应消息的默认设置:

        .. literalinclude:: response/021.php

    .. php:method:: setCache($options)

        :param array $options: 各种缓存控制设置的键/值数组
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置 ``Cache-Control`` 头,包括 ``ETags`` 和 ``Last-Modified``。典型的键包括:

        * etag
        * last-modified
        * max-age
        * s-maxage
        * private
        * public
        * must-revalidate
        * proxy-revalidate
        * no-transform

        当传入 last-modified 选项时,它可以是日期字符串或 DateTime 对象。

    .. php:method:: setLastModified($date)

        :param string|DateTime $date: 要设置 Last-Modified 头的日期
        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        设置 ``Last-Modified`` 头。``$date`` 对象可以是字符串或 ``DateTime`` 实例:

        .. literalinclude:: response/022.php

    .. php:method:: send(): Response

        :returns: 当前响应实例
        :rtype: ``CodeIgniter\HTTP\Response``

        告诉响应将所有内容发送回客户端。这将首先发送 header,然后是响应 body。对于主应用程序响应,您不需要调用它,因为 CodeIgniter 会自动处理。

    .. php:method:: setCookie($name = ''[, $value = ''[, $expire = ''[, $domain = ''[, $path = '/'[, $prefix = ''[, $secure = false[, $httponly = false[, $samesite = null]]]]]]]])

        :param array|Cookie|string $name: Cookie 名称或参数数组或 ``CodeIgniter\Cookie\Cookie`` 实例
        :param string $value: Cookie 值
        :param int $expire: Cookie 到期时间,以秒为单位。如果设置为 ``0`` cookie 将只保持浏览器打开时有效
        :param string $domain: Cookie 域名
        :param string $path: Cookie 路径
        :param string $prefix: Cookie 名称前缀。如果设置为 ``''``,将使用 **app/Config/Cookie.php** 中的默认值
        :param bool $secure: 是否只通过 HTTPS 传输 cookie。如果设置为 ``null``,将使用 **app/Config/Cookie.php** 中的默认值
        :param bool $httponly: 是否只将 cookie accessible 用于 HTTP 请求(无 JavaScript)。如果设置为 ``null``,将使用 **app/Config/Cookie.php** 中的默认值
        :param string $samesite: SameSite cookie 参数的值。如果设置为 ``''``,cookie 将不设置 SameSite 属性。如果设置为 ``null``,将使用 **app/Config/Cookie.php** 中的默认值
        :rtype: void

        .. note:: 在 v4.2.7 之前版本,由于一个错误,``$secure`` 和 ``$httponly`` 的默认值为 ``false``,
            从未使用来自 **app/Config/Cookie.php** 的这些值。

        使用您指定的值设置 cookie。有两种传递信息的方式以便可以设置 cookie:数组方法和离散参数:

        **数组方法**

        使用此方法,关联数组作为第一个参数传递:

        .. literalinclude:: response/023.php

        仅 ``name`` 和 ``value`` 是必需的。要删除 cookie,请将 ``expire`` 置空。

        ``expire`` 以**秒**设置,将添加到当前时间。不要包括时间,而只设置从*现在*希望 cookie 有效的秒数。如果 ``expire`` 设置为零,cookie 将只在浏览器打开时有效。

        .. note:: 但是如果同时将 ``value`` 设置为空字符串和 ``expire`` 设置为 ``0``,
            cookie 将被删除。

        对于无论如何请求站点的站点范围 cookie,在域名前添加站点 URL,如:
        .your-domain.com

        通常不需要 ``path``,因为该方法设置根路径。

        仅在需要避免与服务器上其他同名 cookie 的名称冲突时才需要 ``prefix``。

        仅在希望通过设置为 ``true`` 将其设置为安全 cookie 时才需要 ``secure`` 标志。

        ``samesite`` 值控制 cookie 在域和子域之间的共享方式。允许的值是 ``'None'``、``'Lax'``、 ``'Strict'`` 或空字符串 ``''``。
        如果设置为空字符串,将设置默认的 SameSite 属性。

        **离散参数**

        如果您愿意,可以通过传递使用各个参数的数据来设置 cookie:

        .. literalinclude:: response/024.php

    .. php:method:: deleteCookie($name = ''[, $domain = ''[, $path = '/'[, $prefix = '']]])

        :param mixed $name: Cookie 名称或参数数组
        :param string $domain: Cookie 域名
        :param string $path: Cookie 路径
        :param string $prefix: Cookie 名称前缀
        :rtype: void

        删除现有的 cookie。

        仅 ``name`` 是必需的。

        仅当需要避免与服务器上其他同名 cookie 的名称冲突时才需要 ``prefix``。

        如果希望只删除该子集的 cookie,请提供 ``prefix``。
        如果只希望删除该域的 cookie,请提供 ``domain`` 名称。
        如果只希望删除该路径的 cookie,请提供 ``path`` 名称。

        如果任何可选参数为空,则同名的 cookie 将在所有情况下被删除。

        例子:

        .. literalinclude:: response/025.php

    .. php:method:: hasCookie($name = ''[, $value = null[, $prefix = '']])

        :param mixed $name: Cookie 名称或参数数组
        :param string $value: cookie 值
        :param string $prefix: Cookie 名称前缀
        :rtype: bool

        检查响应是否具有指定的 cookie。

        **注意**

        仅 ``name`` 是必需的。如果指定了 ``prefix``,它将被添加到 cookie 名称前。

        如果没有给出 ``value``,该方法仅检查具有给定名称的 cookie 是否存在。
        如果给出 ``value``,则该方法检查具有给定名称和值的 cookie 是否存在。

        例子:

        .. literalinclude:: response/026.php

    .. php:method:: getCookie($name = ''[, $prefix = ''])

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 名称前缀
        :rtype: ``Cookie|Cookie[]|null``

        如果找到,返回指定的 cookie,否则返回 ``null``。
        如果没有给出 ``name``,则返回 ``Cookie`` 对象数组。

        例子:

        .. literalinclude:: response/027.php

    .. php:method:: getCookies()

        :rtype: ``Cookie[]``

        返回当前在 Response 实例中设置的所有 cookie。
        这些是您在当前请求期间明确指定要设置的任何 cookie。
