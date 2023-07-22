#################
CURLRequest 类
#################

``CURLRequest`` 类是一个轻量级的基于 CURL 的 HTTP 客户端,允许你与其他网站和服务器进行通信。它可以用于获取谷歌搜索的内容、检索网页或图片,或与 API 进行通信等多种用途。

.. contents::
    :local:
    :depth: 2

这个类模仿了 `Guzzle HTTP 客户端 <http://docs.guzzlephp.org/en/latest/>`_ 库,因为它是使用最广泛的库之一。在可能的情况下,语法保持相同,所以如果你的应用程序需要比这个库提供的功能更强大的东西,你将需要做很少的改变就可以过渡到使用 Guzzle。

.. note:: 这个类需要你的 PHP 版本中安装 `cURL 库 <https://www.php.net/manual/en/book.curl.php>`_。这是一个非常常见的库,通常是可用的,但并非所有主机都会提供它,所以如果你遇到问题,请与你的主机确认。

**********************
CURLRequest 配置
**********************

共享选项
===============

由于历史原因,默认情况下,CURLRequest 在请求之间共享所有选项。如果你使用该类的一个实例发送多个请求,这种行为可能会导致错误请求出现不必要的头和消息体。

你可以通过在 **app/Config/CURLRequest.php** 中将以下配置参数值编辑为 ``false`` 来更改此行为:

.. literalinclude:: curlrequest/001.php

.. note:: 在 v4.2.0 之前,即使 ``$shareOptions`` 为 false,由于一个 bug,请求消息体也不会被重置。

*******************
加载库
*******************

可以通过手动方式或通过 :doc:`Services 类 </concepts/services>` 来加载该库。

要通过 Services 类调用,使用 ``curlrequest()`` 方法:

.. literalinclude:: curlrequest/002.php

你可以在第一个参数中传递默认选项数组来修改 cURL 将如何处理请求。选项将在下文中描述:

.. literalinclude:: curlrequest/003.php

.. note:: 当 ``$shareOptions`` 为 false 时,传递给类构造函数的默认选项将用于所有请求。在发送请求后,其他选项将被清除。如果你想对所有请求使用选项,请在构造函数中传递选项。

手动创建类时,你需要传递一些依赖项。第一个参数是一个 ``Config\App`` 类的实例。第二个参数是一个 URI 实例。第三个参数是一个 Response 对象。第四个参数是可选的默认 ``$options`` 数组:

.. literalinclude:: curlrequest/004.php

************************
使用该库
************************

使用 CURL 请求非常简单,只需创建请求并获取返回的 :doc:`Response 对象 </outgoing/response>`。它旨在处理通信。之后你可以完全控制信息的处理方式。

发起请求
===============

大部分通信是通过 ``request()`` 方法完成的,它会发出请求,然后返回一个 Response 实例给你。它以 HTTP 方法、URL 和选项数组作为参数。

.. literalinclude:: curlrequest/005.php

.. note:: 当 ``$shareOptions`` 为 false 时,传入方法的选项将用于该请求。发送请求后,选项将被清除。如果你想对所有请求使用选项,请在构造函数中传入选项。

由于响应是一个 ``CodeIgniter\HTTP\Response`` 实例,你可以使用所有正常的信息:

.. literalinclude:: curlrequest/006.php

虽然 ``request()`` 方法是最灵活的,你也可以使用以下快捷方法。它们都以 URL 作为第一个参数,选项数组作为第二个参数:

.. literalinclude:: curlrequest/007.php

基本 URI
--------

可以在实例化类时将 ``baseURI`` 作为一个选项传入。这允许你设置一个基本 URI,然后使用相对 URL 对该客户端的所有请求进行调用。当与 API 一起使用时,这特别方便:

.. literalinclude:: curlrequest/008.php

当向 ``request()`` 方法或任何快捷方法提供相对 URI 时,它将根据 `RFC 2986 部分 2 <https://tools.ietf.org/html/rfc3986#section-5.2>`_ 描述的规则与 baseURI 组合。
为了节省你一些时间,这里有一些组合结果的示例。

    =====================   ================   ========================
    baseURI                 URI                结果
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

每个 ``request()`` 调用都会返回一个 Response 对象,其中包含大量有用的信息和一些有用的方法。最常用的方法让你确定响应本身。

你可以获取响应的状态码和原因短语:

.. literalinclude:: curlrequest/009.php

你可以从响应中检索标头:

.. literalinclude:: curlrequest/010.php

可以使用 ``getBody()`` 方法获取消息体:

.. literalinclude:: curlrequest/011.php

消息体是远程服务器提供的原始消息体。如果内容类型需要格式化,则需要确保脚本对其进行处理:

.. literalinclude:: curlrequest/012.php

***************
请求选项
***************

本节描述了可以传递到构造函数、``request()`` 方法或任何快捷方法中的所有可用选项。

allow_redirects
===============

默认情况下,cURL 将遵循远程服务器返回的所有“Location:”标头。``allow_redirects`` 选项允许你修改此行为。

如果将值设置为 ``false``,则它将不会遵循任何重定向:

.. literalinclude:: curlrequest/013.php

将其设置为 ``true`` 将对请求应用默认设置:

.. literalinclude:: curlrequest/014.php

你可以将数组作为 ``allow_redirects`` 选项的值传递,以指定新的设置以代替默认设置:

.. literalinclude:: curlrequest/015.php

.. note:: 当 PHP 在 safe_mode 中或启用 open_basedir 时,跟随重定向将不起作用。

auth
====

允许你为 `HTTP 基本认证 <https://www.ietf.org/rfc/rfc2069.txt>`_ 和 `摘要认证 <https://www.ietf.org/rfc/rfc2069.txt>`_ 提供认证细节。你的脚本可能需要做额外的工作来支持摘要认证 - 这只是简单地为你传递用户名和密码。值必须是一个数组,其中第一个元素是用户名,第二个是密码。第三个参数应该是要使用的认证类型,可以是 ``basic`` 或 ``digest``:

.. literalinclude:: curlrequest/016.php

body
====

对于支持 body 的请求类型(如 PUT、POST 等),有两种方式设置请求 body。第一种方式是使用 ``setBody()`` 方法:

.. literalinclude:: curlrequest/017.php

第二种方法是通过传递一个 ``body`` 选项。这是为了保持 Guzzle API 的兼容性,功能完全相同。值必须是一个字符串:

.. literalinclude:: curlrequest/018.php

cert
====

要指定客户端证书的位置,需要以字符串形式传递包含完整路径的 ``cert`` 选项。如果需要密码,请将值设置为一个数组,其中第一个元素是证书的路径,第二个是密码:

.. literalinclude:: curlrequest/019.php

connect_timeout
===============

默认情况下,CodeIgniter 不对 cURL 尝试连接到网站的时间施加限制。如果你需要修改此值,可以以秒为单位传递 ``connect_timeout`` 选项。你可以传递 0 以无限期等待:

.. literalinclude:: curlrequest/020.php

cookie
======

这指定了 CURL 应该使用的文件名,用于读取和保存 cookie 值。这是通过 CURL_COOKIEJAR 和 CURL_COOKIEFILE 选项完成的。例如:

.. literalinclude:: curlrequest/021.php

debug
=====

当 ``debug`` 被传递并设置为 ``true`` 时,这将在脚本执行期间启用写入 STDERR 的其他调试信息。这是通过传递 CURLOPT_VERBOSE 并回显输出来完成的。因此,当你通过 ``spark serve`` 运行内置服务器时,你会在控制台中看到输出。否则,输出将被写入服务器的错误日志中。

.. literalinclude:: curlrequest/034.php

你可以将文件名作为 debug 的值以将输出写入文件:

.. literalinclude:: curlrequest/022.php

delay
=====

允许在发送请求之前暂停一定的毫秒数:

.. literalinclude:: curlrequest/023.php

form_params
===========

你可以通过在 ``form_params`` 选项中传递关联数组来发送 application/x-www-form-urlencoded POST 请求中的表单数据。如果尚未设置,这将设置 ``Content-Type`` 标头为 ``application/x-www-form-urlencoded`` :

.. literalinclude:: curlrequest/024.php

.. note:: ``form_params`` 不能与 ``multipart`` 选项一起使用。你需要使用其中一个。对 ``application/x-www-form-urlencoded`` 请求使用 ``form_params``,对 ``multipart/form-data`` 请求使用 ``multipart``。

.. _curlrequest-request-options-headers:

headers
=======

虽然你可以使用 ``setHeader()`` 方法设置此请求需要的任何标头,但你也可以将关联数组的标头作为选项传递。每个键都是标头的名称,每个值是表示标头字段值的字符串或字符串数组:

.. literalinclude:: curlrequest/025.php

如果标头被传递到构造函数中,它们会被视为默认值,并被后续的标头数组或对 ``setHeader()`` 的调用覆盖。

http_errors
===========

默认情况下,如果返回的 HTTP 代码大于或等于 400,CURLRequest 将失败。你可以将 ``http_errors`` 设置为 ``false`` 来改为返回内容:

.. literalinclude:: curlrequest/026.php

json
====

``json`` 选项用于轻松地将 JSON 编码的数据作为请求的 body 上传。添加了 ``application/json`` 的 Content-Type 标头,覆盖任何可能已经设置的 Content-Type。传给此选项的数据可以是 ``json_encode()`` 接受的任何值:

.. literalinclude:: curlrequest/027.php

.. note:: 此选项不允许自定义 ``json_encode()`` 函数或 Content-Type 标头。如果你需要那种能力,你需要手动编码数据,通过 CURLRequest 的 ``setBody()`` 方法传递它,并使用 ``setHeader()`` 方法设置 Content-Type 标头。

multipart
=========

当你需要通过 POST 请求发送文件和其他数据时,可以使用 ``multipart`` 选项,以及 `CURLFile 类 <https://www.php.net/manual/en/class.curlfile.php>`_。值应该是一个关联数组,包含要发送的 POST 数据。为了更安全地使用,上传文件通过在名称前加上 `@` 的遗留方法已被禁用。你想要发送的任何文件必须作为 CURLFile 实例传递:

.. literalinclude:: curlrequest/028.php

.. note:: ``multipart`` 不能与 ``form_params`` 选项一起使用。你只能使用其中一个。对 ``application/x-www-form-urlencoded`` 请求使用
        ``form_params``,对 ``multipart/form-data`` 请求使用 ``multipart``。

query
=====

你可以通过作为 ``query`` 选项传递关联数组,来传递要作为查询字符串变量发送的数据:

.. literalinclude:: curlrequest/029.php

timeout
=======

默认情况下,允许 cURL 函数无限期运行,没有时间限制。你可以使用 ``timeout`` 选项对其进行修改。值应该是你希望函数执行的秒数。使用 0 表示无限期等待:

.. literalinclude:: curlrequest/030.php

user_agent
==========

允许指定请求的用户代理:

.. literalinclude:: curlrequest/031.php

verify
======

此选项描述了 SSL 证书验证行为。如果 ``verify`` 选项为 ``true``,它将启用 SSL 证书验证并使用操作系统提供的默认 CA 包。如果设置为 ``false``,它将禁用证书验证(这是不安全的,并允许中间人攻击!)。你可以将其设置为包含 CA 包路径的字符串,以使用自定义证书启用验证。默认值为 true:

.. literalinclude:: curlrequest/032.php

.. _curlrequest-version:

version
=======

要设置要使用的 HTTP 协议,你可以传递带有版本号的字符串或浮点数(通常为 ``1.0`` 或 ``1.1``,v4.3.0 开始支持 ``2.0``)。

.. literalinclude:: curlrequest/033.php
