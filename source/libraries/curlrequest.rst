#################
CURLRequest 类
#################

``CURLRequest`` 类是一个基于 CURL 的轻量级 HTTP 客户端，允许你与其他网站和服务器进行通信。它可以用于获取 Google 搜索结果、检索网页或图像，以及与 API 交互等多种用途。

.. contents::
    :local:
    :depth: 2

该类的设计灵感来源于 `Guzzle HTTP Client <http://docs.guzzlephp.org/en/latest/>`_ 库，因为它是使用最广泛的 HTTP 客户端库之一。在可能的情况下，我们保持了语法的一致性，以便当你的应用需要比本库更强大的功能时，只需极少修改即可迁移到 Guzzle。

.. note:: 本类需要 PHP 安装 `cURL 库 <https://www.php.net/manual/zh/book.curl.php>`_。这是非常常见的库，通常默认可用，但部分主机可能未提供，若遇到问题请与主机服务商确认。

**********************
CURLRequest 配置
**********************

.. _curlrequest-sharing-options:

共享选项
===============

.. important:: 此设置仅用于向后兼容。新项目请勿使用。即使你正在使用，我们也建议禁用它。

.. note:: 自 v4.4.0 起，默认值已改为 ``false``。

若要在请求间共享所有选项，请在 **app/Config/CURLRequest.php** 中将 ``$shareOptions`` 设为 ``true``：

.. literalinclude:: curlrequest/001.php

如果使用类的实例发送多个请求，此行为可能导致带有不必要标头和正文的错误请求。

.. note:: 在 v4.2.0 之前，由于一个错误，即使 ``$shareOptions`` 设为 false 请求体也不会重置。

*******************
加载类库
*******************

可以通过手动加载或通过 :doc:`Services 类 </concepts/services>` 加载本库。

使用 Services 类加载时，调用 ``curlrequest()`` 方法或全局函数 ``service()``：

.. literalinclude:: curlrequest/002.php

你可以在第一个参数中传递默认选项数组来修改 cURL 处理请求的方式。选项将在本文档后续部分说明：

.. literalinclude:: curlrequest/003.php

.. note:: 当 ``$shareOptions`` 为 false 时，传递给类构造函数的默认选项将用于所有请求。其他选项将在发送请求后重置。

手动创建类时，需要传入几个依赖项。第一个参数是 ``Config\App`` 类的实例，第二个是 URI 实例，第三个是 Response 对象，第四个是可选的默认 ``$options`` 数组：

.. literalinclude:: curlrequest/004.php

************************
使用类库
************************

使用 CURL 请求只需创建 Request 并获取 :doc:`Response 对象 </outgoing/response>`。它负责处理通信，之后你可以完全控制信息处理方式。

发起请求
===============

主要通过 ``request()`` 方法进行通信，该方法触发请求并返回 Response 实例。它接受 HTTP 方法、URL 和选项数组作为参数：

.. literalinclude:: curlrequest/005.php

.. important:: 默认情况下，如果返回的 HTTP 状态码大于等于 400，CURLRequest 将抛出 ``HTTPException``。若需获取响应，请参阅 `http_errors`_ 选项。

.. note:: 当 ``$shareOptions`` 为 false 时，传递给方法的选项将用于该请求。发送请求后这些选项会被清除。若要将选项应用于所有请求，请在构造函数中传递选项。

由于响应是 ``CodeIgniter\HTTP\Response`` 的实例，你可以访问所有常规信息：

.. literalinclude:: curlrequest/006.php

虽然 ``request()`` 方法最灵活，但也可以使用以下快捷方法。它们都将 URL 作为第一个参数，选项数组作为第二个：

.. literalinclude:: curlrequest/007.php

基础 URI
--------

可以在类实例化时通过选项设置 ``baseURI``。这允许你设置基础 URI，之后使用该客户端的所有请求都使用相对 URL。这在处理 API 时特别方便：

.. literalinclude:: curlrequest/008.php

当向 ``request()`` 方法或任何快捷方法提供相对 URI 时，它将根据 `RFC 2986 第 2 节 <https://tools.ietf.org/html/rfc3986#section-5.2>`_ 描述的规则与 baseURI 组合。以下是组合解析的示例：

    =====================   ================   ========================
    baseURI                 URI                结果
    =====================   ================   ========================
    \http://foo.com         /bar               \http://foo.com/bar
    \http://foo.com/foo     /bar               \http://foo.com/bar
    \http://foo.com/foo     bar                \http://foo.com/bar
    \http://foo.com/foo/    bar                \http://foo.com/foo/bar
    \http://foo.com         \http://baz.com    \http://baz.com
    \http://foo.com/?bar    bar                \http://foo.com/bar
    =====================   ================   ========================

使用响应
===============

每个 ``request()`` 调用返回的 Response 对象包含大量有用信息和实用方法。最常用的方法用于确定响应内容。

获取状态码和原因短语：

.. literalinclude:: curlrequest/009.php

从响应中检索标头：

.. literalinclude:: curlrequest/010.php

使用 ``getBody()`` 方法获取正文：

.. literalinclude:: curlrequest/011.php

正文是远程服务器返回的原始内容。如果内容类型需要格式化，你需要确保脚本能处理：

.. literalinclude:: curlrequest/012.php

***************
请求选项
***************

本节描述可传递给构造函数、``request()`` 方法或任何快捷方法的所有可用选项。

allow_redirects
===============

默认情况下，cURL 不会跟踪远程服务器返回的任何 "Location:" 标头。``allow_redirects`` 选项允许你修改此行为。

设为 ``true`` 时跟踪重定向：

.. literalinclude:: curlrequest/014.php

.. warning:: 请注意启用重定向可能会跳转到意外 URL，并可能导致 SSRF 攻击。

设为 ``false`` 将应用请求的默认设置：

.. literalinclude:: curlrequest/013.php

可以传递数组作为 ``allow_redirects`` 的值来指定新设置：

.. literalinclude:: curlrequest/015.php

.. note:: 当 PHP 处于安全模式或启用 open_basedir 时，跟踪重定向无效。

auth
====

允许为 `HTTP 基本认证 <https://www.ietf.org/rfc/rfc2069.txt>`_ 和 `摘要认证 <https://www.ietf.org/rfc/rfc2069.txt>`_ 提供凭据。值必须是数组，第一个元素是用户名，第二个是密码。第三个参数是认证类型（``basic`` 或 ``digest``）：

.. literalinclude:: curlrequest/016.php

body
====

对于支持正文的请求类型（如 PUT 或 POST），有两种设置正文的方式。第一种是使用 ``setBody()`` 方法：

.. literalinclude:: curlrequest/017.php

第二种是通过传递 ``body`` 选项。此方法为保持与 Guzzle API 兼容，功能与上例相同。值必须是字符串：

.. literalinclude:: curlrequest/018.php

cert
====

要指定 PEM 格式客户端证书的位置，可将完整文件路径作为字符串传递给 ``cert`` 选项。若需密码，可将值设为数组，第一个元素是证书路径，第二个是密码：

.. literalinclude:: curlrequest/019.php

connect_timeout
===============

默认情况下，CodeIgniter 不限制 cURL 连接网站的时间。可通过 ``connect_timeout`` 选项修改（单位：秒），0 表示无限等待：

.. literalinclude:: curlrequest/020.php

cookie
======

指定 cURL 用于读取和保存 cookie 值的文件名。通过 ``CURL_COOKIEJAR`` 和 ``CURL_COOKIEFILE`` 选项实现：

.. literalinclude:: curlrequest/021.php

debug
=====

当 ``debug`` 设为 ``true`` 时，将启用额外调试信息并输出到 STDERR。

这是通过设置 ``CURLOPT_VERBOSE`` 并回显输出来实现的。使用 ``spark serve`` 运行内置服务器时，输出将显示在控制台；否则写入服务器错误日志：

.. literalinclude:: curlrequest/034.php

可将文件名作为 debug 的值来将输出写入文件：

.. literalinclude:: curlrequest/022.php

delay
=====

允许在发送请求前暂停指定毫秒数：

.. literalinclude:: curlrequest/023.php

form_params
===========

通过 ``form_params`` 选项发送 application/x-www-form-urlencoded POST 请求的关联数组。如果未设置，会将 ``Content-Type`` 标头设为 ``application/x-www-form-urlencoded``：

.. literalinclude:: curlrequest/024.php

.. note:: ``form_params`` 不能与 `multipart`_ 选项共用。对于 ``application/x-www-form-urlencoded`` 请求使用 ``form_params``，对于 ``multipart/form-data`` 请求使用 ``multipart``。

.. _curlrequest-request-options-headers:

headers
=======

虽然可以使用 ``setHeader()`` 方法设置请求需要的标头，也可以通过选项传递关联数组。每个键是标头名称，值是该标头字段值的字符串或字符串数组：

.. literalinclude:: curlrequest/025.php

如果标头在构造函数中传递，它们将被视为默认值，会被后续标头数组或 ``setHeader()`` 调用覆盖。

http_errors
===========

默认情况下，当返回的 HTTP 状态码大于等于 400 时，CURLRequest 会抛出 ``HTTPException``。

若需查看响应正文，可将 ``http_errors`` 设为 ``false`` 以返回内容：

.. literalinclude:: curlrequest/026.php

json
====

``json`` 选项用于轻松上传 JSON 编码数据作为请求正文。会添加 ``application/json`` 的 Content-Type 标头，覆盖已设置的任何 Content-Type。数据可以是 ``json_encode()`` 接受的任何值：

.. literalinclude:: curlrequest/027.php

.. note:: 此选项不允许自定义 ``json_encode()`` 函数或 Content-Type 标头。如需此功能，需手动编码数据并通过 CURLRequest 的 ``setBody()`` 方法传递，同时使用 ``setHeader()`` 方法设置 Content-Type。

multipart
=========

需要通过 POST 请求发送文件和其他数据时，可使用 ``multipart`` 选项和 `CURLFile 类 <https://www.php.net/manual/zh/class.curlfile.php>`_。

值应为要发送的 POST 数据关联数组。为安全起见，已禁用通过前缀 ``@`` 上传文件的旧方法。要发送的文件必须作为 CURLFile 实例传递：

.. literalinclude:: curlrequest/028.php

.. note:: ``multipart`` 不能与 `form_params`_ 选项共用。对于 ``application/x-www-form-urlencoded`` 请求使用 ``form_params``，对于 ``multipart/form-data`` 请求使用 ``multipart``。

.. _curlrequest-request-options-proxy:

proxy
=====

.. versionadded:: 4.4.0

可通过传递关联数组作为 ``proxy`` 选项来设置代理：

.. literalinclude:: curlrequest/035.php

query
=====

通过传递关联数组作为 ``query`` 选项来发送查询字符串参数：

.. literalinclude:: curlrequest/029.php

timeout
=======

默认情况下，cURL 函数执行没有时间限制。可通过 ``timeout`` 选项修改（单位：秒），0 表示无限等待：

.. literalinclude:: curlrequest/030.php

user_agent
==========

指定请求的 User Agent：

.. literalinclude:: curlrequest/031.php

verify
======

此选项描述 SSL 证书验证行为。若 ``verify`` 为 ``true``，启用 SSL 证书验证并使用操作系统提供的默认 CA 包。设为 ``false`` 将禁用验证（不安全，允许中间人攻击）。设为自定义证书路径可启用验证。默认值为 true：

.. literalinclude:: curlrequest/032.php

.. _curlrequest-version:

force_ip_resolve
================

.. versionadded:: 4.6.0

设置 HTTP 处理器使用 ``v4`` （仅 IPv4）或 ``v6`` （IPv6）协议：

.. literalinclude:: curlrequest/036.php

version
=======

要设置使用的 HTTP 协议版本，可传递版本号字符串或浮点数（通常为 ``1.0``、``1.1``，v4.3.0 起支持 ``2.0``）：

.. literalinclude:: curlrequest/033.php
