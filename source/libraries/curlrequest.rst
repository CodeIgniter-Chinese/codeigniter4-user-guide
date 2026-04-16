#################
CURLRequest 类
#################

``CURLRequest`` 类是一个基于 CURL 的轻量级 HTTP 客户端，用于与其他网站和服务器通信。可用于获取 Google 搜索结果、检索网页或图片，或与 API 交互等。

.. contents::
    :local:
    :depth: 2

该类的设计灵感来源于 `Guzzle HTTP Client <http://docs.guzzlephp.org/en/latest/>`_ 库，因为它是使用最广泛的 HTTP 客户端库之一。在可能的情况下，语法保持一致，若应用需要比本类更强大的功能，迁移到 Guzzle 时只需做少量修改。

.. note:: 此类需要 PHP 安装 `cURL 扩展 <https://www.php.net/manual/zh/book.curl.php>`_。这是非常常见的扩展，通常默认可用，但并非所有主机都提供，如遇问题请与主机提供商确认。

**********************
CURLRequest 配置
**********************

.. _curlrequest-sharing-options:

共享选项
===============

.. important:: 此设置仅为向后兼容而存在，新项目请勿使用。即使已在使用，也建议禁用。

.. note:: 自 v4.4.0 起，默认值已更改为 ``false``。

如需在请求之间共享所有选项，在 **app/Config/CURLRequest.php** 中将 ``$shareOptions`` 设为 ``true``：

.. literalinclude:: curlrequest/001.php

若用类的实例发送多个请求，此行为可能导致请求出错，附带不必要的 HTTP 标头和请求体。

.. note:: 在 v4.2.0 之前，即使 ``$shareOptions`` 为 false，由于 Bug 请求体也不会重置。

*******************
加载类
*******************

可通过手动方式或 :doc:`Services 类 </concepts/services>` 加载此类。

使用 Services 类调用 ``curlrequest()`` 方法或全局函数 ``service()``：

.. literalinclude:: curlrequest/002.php

可在第一个参数中传入默认选项数组，修改 cURL 处理请求的方式。选项说明见本文后续部分：

.. literalinclude:: curlrequest/003.php

.. note:: 当 ``$shareOptions`` 为 false 时，传入类构造函数的默认选项将用于所有请求，其他选项在发送请求后重置。

手动创建类时，需要传入几个依赖项。第一个参数是 ``Config\App`` 类的实例，第二个参数是 URI 实例，第三个参数是 Response 对象，第四个参数是可选的默认 ``$options`` 数组：

.. literalinclude:: curlrequest/004.php

************************
使用类
************************

使用 CURL 请求只需创建请求并获取 :doc:`Response 对象 </outgoing/response>`。此类用于处理通信，之后可完全控制信息的处理方式。

发起请求
===============

大多数通信通过 ``request()`` 方法完成，该方法发送请求并返回 Response 实例。参数为 HTTP 方法、URL 和选项数组。

.. literalinclude:: curlrequest/005.php

.. important:: 默认情况下，若返回的 HTTP 状态码大于等于 400，CURLRequest 将抛出 ``HTTPException``。如需获取响应内容，参见 `http_errors`_ 选项。

.. note:: 当 ``$shareOptions`` 为 false 时，传入方法的选项仅用于该请求，发送后清除。若要将选项用于所有请求，请在构造函数中传入。

由于响应是 ``CodeIgniter\HTTP\Response`` 的实例，可使用所有常规方法：

.. literalinclude:: curlrequest/006.php

``request()`` 方法最为灵活，也可使用以下快捷方法。它们都以 URL 为第一参数，选项数组为第二参数：

.. literalinclude:: curlrequest/007.php

基础 URI
--------

可在类实例化时通过选项设置 ``baseURI``。设置基础 URI 后，可使用相对 URL 进行所有请求，与 API 交互时尤为方便：

.. literalinclude:: curlrequest/008.php

当向 ``request()`` 方法或任何快捷方法传入相对 URI 时，将按照 `RFC 2986 第 2 节 <https://tools.ietf.org/html/rfc3986#section-5.2>`_ 描述的规则与 baseURI 组合。以下是组合解析的示例：

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

每次 ``request()`` 调用都返回包含大量有用信息和方法的 Response 对象。常用方法用于确定响应本身。

可获取响应的状态码和原因短语：

.. literalinclude:: curlrequest/009.php

可从响应中检索 HTTP 标头：

.. literalinclude:: curlrequest/010.php

响应体可通过 ``getBody()`` 方法获取：

.. literalinclude:: curlrequest/011.php

响应体是远程服务器提供的原始内容。若内容类型需要格式化，需确保脚本进行处理：

.. literalinclude:: curlrequest/012.php

***************
请求选项
***************

本节描述可传入构造函数、``request()`` 方法或任何快捷方法的所有可用选项。

allow_redirects
===============

默认情况下，cURL 不会跟随远程服务器返回的 "Location:" 标头。``allow_redirects`` 选项可修改此行为。

设为 ``true`` 将跟随重定向：

.. literalinclude:: curlrequest/014.php

.. warning:: 请注意，启用重定向可能会跳转到意外的 URL，可能引发 SSRF 攻击。

设为 ``false`` 将对请求应用默认设置：

.. literalinclude:: curlrequest/013.php

可传入数组作为 ``allow_redirects`` 选项的值，指定新设置替代默认值：

.. literalinclude:: curlrequest/015.php

.. note:: PHP 处于安全模式或启用 open_basedir 时，跟随重定向功能不可用。

auth
====

用于提供 `HTTP Basic <https://www.ietf.org/rfc/rfc2069.txt>`_ 和 `Digest <https://www.ietf.org/rfc/rfc2069.txt>`_ 认证的认证详情。脚本可能需要额外工作来支持 Digest 认证，此选项仅代为传递用户名和密码。值必须是数组，第一个元素为用户名，第二个为密码，第三个为认证类型，可选 ``basic`` 或 ``digest``：

.. literalinclude:: curlrequest/016.php

body
====

对于支持请求体的请求类型（如 PUT 或 POST），有两种方式设置请求体。第一种使用 ``setBody()`` 方法：

.. literalinclude:: curlrequest/017.php

第二种通过传入 ``body`` 选项。这是为了保持 Guzzle API 兼容性，功能与上例完全相同。值必须是字符串：

.. literalinclude:: curlrequest/018.php

cert
====

指定 PEM 格式客户端证书位置时，将文件的完整路径字符串作为 ``cert`` 选项传入。若需要密码，将值设为数组，第一个元素为证书路径，第二个为密码：

.. literalinclude:: curlrequest/019.php

connect_timeout
===============

默认情况下，CodeIgniter 不限制 cURL 尝试连接网站的时间。如需修改此值，可通过 ``connect_timeout`` 选项传入秒数，传入 0 表示无限等待：

.. literalinclude:: curlrequest/020.php

cookie
======

指定 CURL 用于读取和保存 Cookie 值的文件名。通过 ``CURL_COOKIEJAR`` 和 ``CURL_COOKIEFILE`` 选项实现。示例：

.. literalinclude:: curlrequest/021.php

debug
=====

传入 ``debug`` 并设为 ``true`` 时，将启用额外调试输出到 STDERR。

这是通过设置 ``CURLOPT_VERBOSE`` 并回显输出来实现的。因此使用 ``spark serve`` 运行内置服务器时，将在控制台看到输出，否则输出将写入服务器错误日志。

.. literalinclude:: curlrequest/034.php

可将文件名作为 debug 的值传入，使输出写入文件：

.. literalinclude:: curlrequest/022.php

delay
=====

允许在发送请求前暂停指定的毫秒数：

.. literalinclude:: curlrequest/023.php

form_params
===========

通过 ``form_params`` 选项传入关联数组，可发送 application/x-www-form-urlencoded 格式的 POST 请求数据。若未设置，这将把 ``Content-Type`` 标头设为 ``application/x-www-form-urlencoded``：

.. literalinclude:: curlrequest/024.php

.. note:: ``form_params`` 不能与 `multipart`_ 选项同时使用，只能二选一。``form_params`` 用于 ``application/x-www-form-urlencoded`` 请求，``multipart`` 用于 ``multipart/form-data`` 请求。

.. _curlrequest-request-options-headers:

headers
=======

虽然可使用 ``setHeader()`` 方法设置请求所需的所有 HTTP 标头，但也可将标头的关联数组作为选项传入。每个键是标头名称，每个值是表示标头字段值的字符串或字符串数组：

.. literalinclude:: curlrequest/025.php

若标头传入构造函数，则视为默认值，后续任何标头数组或 ``setHeader()`` 调用都将覆盖它们。

http_errors
===========

默认情况下，若返回的 HTTP 状态码大于等于 400，CURLRequest 将抛出 ``HTTPException``。

如需查看响应体，可将 ``http_errors`` 设为 ``false`` 以返回内容：

.. literalinclude:: curlrequest/026.php

json
====

``json`` 选项用于轻松上传 JSON 编码数据作为请求体。添加 ``application/json`` 的 Content-Type 标头，覆盖任何已设置的 Content-Type。提供给此选项的数据可以是 ``json_encode()`` 接受的任何值：

.. literalinclude:: curlrequest/027.php

.. note:: 此选项不允许自定义 ``json_encode()`` 函数或 Content-Type 标头。若需此功能，需手动编码数据，通过 CURLRequest 的 ``setBody()`` 方法传入，并使用 ``setHeader()`` 方法设置 Content-Type 标头。

multipart
=========

需要通过 POST 请求发送文件和其他数据时，可使用 ``multipart`` 选项和 `CURLFile 类 <https://www.php.net/manual/zh/class.curlfile.php>`_。

值应为要发送的 POST 数据的关联数组。为安全起见，通过在文件名前加 ``@`` 前缀来上传文件的旧方法已被禁用。要发送的任何文件必须作为 CURLFile 实例传入：

.. literalinclude:: curlrequest/028.php

.. note:: ``multipart`` 不能与 `form_params`_ 选项同时使用，只能二选一。``form_params`` 用于 ``application/x-www-form-urlencoded`` 请求，``multipart`` 用于 ``multipart/form-data`` 请求。

.. _curlrequest-request-options-proxy:

proxy
=====

.. versionadded:: 4.4.0

通过传入关联数组作为 ``proxy`` 选项可设置代理：

.. literalinclude:: curlrequest/035.php

query
=====

通过 ``query`` 选项传入关联数组，可发送查询字符串：

.. literalinclude:: curlrequest/029.php

timeout
=======

默认情况下，cURL 函数允许无时间限制地运行。可通过 ``timeout`` 选项修改。值应为允许函数执行的秒数，使用 0 表示无限等待：

.. literalinclude:: curlrequest/030.php

user_agent
==========

设置请求的用户代理（User Agent）：

.. literalinclude:: curlrequest/031.php

verify
======

此选项描述 SSL 证书验证行为。若 ``verify`` 选项为 ``true``，启用 SSL 证书验证并使用操作系统提供的默认 CA 捆绑包。设为 ``false`` 将禁用证书验证（这不安全，允许中间人攻击）。可设为包含 CA 捆绑包路径的字符串，以使用自定义证书来启用验证。默认值为 true：

.. literalinclude:: curlrequest/032.php

.. _curlrequest-version:

force_ip_resolve
================

.. versionadded:: 4.6.0

设置 HTTP 处理器使用 ``v4`` （仅 IPv4）或 ``v6`` （IPv6）协议：

.. literalinclude:: curlrequest/036.php

version
=======

设置使用的 HTTP 协议版本，可传入版本号的字符串或浮点数（通常为 ``1.0`` 或 ``1.1``，自 v4.3.0 起支持 ``2.0``）：

.. literalinclude:: curlrequest/033.php
