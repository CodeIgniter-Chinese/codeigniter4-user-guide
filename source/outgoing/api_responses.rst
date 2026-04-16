##################
API 响应 Trait
##################

现代 PHP 开发中，构建 API 已成为常见需求，无论是为 JavaScript 密集型单页应用提供数据，还是作为独立产品。CodeIgniter 提供了 API 响应 Trait，可与任何控制器配合使用，简化常见响应类型的处理，无需记忆不同响应类型应返回的 HTTP 状态码。

.. contents::
    :local:
    :depth: 2

*************
使用示例
*************

以下示例展示了控制器中的常见用法模式。

.. literalinclude:: api_responses/001.php

此示例返回 HTTP 状态码 201 及通用状态消息 "Created"。该 Trait 为最常见的用例提供了方法：

.. literalinclude:: api_responses/002.php

.. _api-response-trait-handling-response-types:

***********************
处理响应类型
***********************

调用这些方法传入数据时，系统将根据以下规则确定数据类型以格式化结果：

* 根据控制器的 ``$this->format`` 值确定格式。
  若该值为 ``null``，将尝试与客户端请求进行内容协商，
  默认使用 **app/Config/Format.php** 中 ``$supportedResponseFormats`` 属性的第一个元素（默认为 JSON）。
* 数据将按格式进行格式化。若非 JSON 格式且数据为字符串，将视为 HTML 返回给客户端。

.. note:: 在 v4.5.0 之前，由于一个 Bug，若数据为字符串，即使格式为 JSON 也会被视为 HTML。

如需定义所使用的格式化程序，请编辑 **app/Config/Format.php**。``$supportedResponseFormats`` 包含应用可自动格式化的 MIME 类型。系统默认支持 XML 和 JSON 响应格式：

.. literalinclude:: api_responses/003.php

进行 :doc:`内容协商 </incoming/content_negotiation>` 时，通过该数组确定返回的响应类型。若客户端请求与支持的格式不匹配，则返回数组中的第一个格式。

接下来，需要定义用于格式化数据数组的类。必须是完全限定类名，且该类必须实现 ``CodeIgniter\Format\FormatterInterface``。框架内置支持 JSON 和 XML 的格式化程序：

.. literalinclude:: api_responses/004.php

因此，若请求在 **Accept** 标头中要求 JSON 格式的数据，传递给任何 ``respond*`` 或 ``fail*`` 方法的数据数组将由 ``CodeIgniter\Format\JSONFormatter`` 类格式化，生成的 JSON 数据将返回给客户端。

***************
类参考
***************

.. php:method:: setResponseFormat($format)

    :param string $format: 要返回的响应类型，``json`` 或 ``xml``

    用于定义响应中数组格式化的方式。若将 ``$format`` 设为 ``null``，则通过内容协商自动确定格式。

.. literalinclude:: api_responses/005.php

.. php:method:: respond($data[, $statusCode = 200[, $message = '']])

    :param mixed  $data: 要返回给客户端的数据，字符串或数组。
    :param int    $statusCode: 要返回的 HTTP 状态码，默认为 200
    :param string $message: 要返回的自定义“原因”消息。

    Trait 中的其他方法均通过此方法向客户端返回响应。

    ``$data`` 参数可以是字符串或数组。默认情况下，字符串作为 HTML 返回，数组则经 json_encode 处理后作为 JSON 返回；除非通过 :doc:`内容协商 </incoming/content_negotiation>` 确定了其他返回格式。

    若传入 ``$message`` 字符串，则会替换响应状态中标准的 IANA 原因短语。但并非所有客户端都支持自定义代码，部分客户端仍会使用与状态码对应的 IANA 标准说明。

    .. note:: 由于此方法会设置当前 Response 实例的状态码和正文，因此应始终作为脚本执行过程中的最后一个方法调用。

.. php:method:: fail($messages[, int $status = 400[, string $code = null[, string $message = '']]])

    :param mixed $messages: 包含遇到错误消息的字符串或字符串数组。
    :param int   $status: 要返回的 HTTP 状态码，默认为 400。
    :param string $code: 自定义 API 专用错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: 以客户端首选格式返回的 multi-part 响应。

    表示失败响应的通用方法，所有其他 "fail" 方法均使用此方法。

    ``$messages`` 元素可为字符串或字符串数组。

    ``$status`` 参数为应返回的 HTTP 状态码。

    由于许多 API 更适合使用自定义错误码，可在第三个参数中传入自定义错误码。若未提供值，将与 ``$status`` 相同。

    若传入 ``$message`` 字符串，将替代响应状态的标准 IANA 原因码。但并非所有客户端都支持自定义原因码，部分客户端仍会使用与状态码匹配的 IANA 标准。

    响应为包含两个元素的数组：``error`` 和 ``messages``。``error`` 元素包含错误状态码，``messages`` 元素包含错误消息数组。格式如下：

    .. literalinclude:: api_responses/006.php

.. php:method:: respondCreated($data = null[, string $message = ''])

    :param mixed  $data: 要返回给客户端的数据，字符串或数组。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    创建新资源时设置相应的状态码，通常为 201：

    .. literalinclude:: api_responses/007.php

.. php:method:: respondDeleted($data = null[, string $message = ''])

    :param mixed  $data: 要返回给客户端的数据，字符串或数组。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    API 调用成功删除资源时设置相应的状态码，通常为 200。

    .. literalinclude:: api_responses/008.php

.. php:method:: respondNoContent(string $message = 'No Content')

    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    服务器成功执行命令但无内容返回时，设置相应的状态码，通常为 204：

    .. literalinclude:: api_responses/009.php

.. php:method:: failUnauthorized(string $description = 'Unauthorized'[, string $code = null[, string $message = '']])

    :param string  $description: 向用户显示的错误消息。
    :param string $code: 自定义 API 专用错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    未经授权或授权错误时设置相应的状态码，状态码为 401。

    .. literalinclude:: api_responses/010.php

.. php:method:: failForbidden(string $description = 'Forbidden'[, string $code=null[, string $message = '']])

    :param string  $description: 向用户显示的错误消息。
    :param string $code: 自定义 API 专用错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    与 ``failUnauthorized()`` 不同，当请求的 API 端点完全禁止访问时，应使用此方法。Unauthorized 即建议客户端更换凭据重试。Forbidden 则表示重试无效，不应再次尝试。状态码为 403。

    .. literalinclude:: api_responses/011.php

.. php:method:: failNotFound(string $description = 'Not Found'[, string $code=null[, string $message = '']])

    :param string  $description: 向用户显示的错误消息。
    :param string $code: 自定义 API 专用错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    找不到请求的资源时设置相应的状态码，状态码为 404。

    .. literalinclude:: api_responses/012.php

.. php:method:: failValidationErrors($errors[, string $code=null[, string $message = '']])

    :param mixed  $errors: 向用户显示的错误消息或消息数组。
    :param string $code: 自定义 API 专用错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    客户端发送的数据未通过验证规则时设置相应的状态码，通常为 400。

    .. literalinclude:: api_responses/013.php

.. php:method:: failResourceExists(string $description = 'Conflict'[, string $code=null[, string $message = '']])

    :param string  $description: 向用户显示的错误消息。
    :param string $code: 自定义 API 专用错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    客户端尝试创建的资源已存在时，设置相应的状态码，通常为 409。

    .. literalinclude:: api_responses/014.php

.. php:method:: failResourceGone(string $description = 'Gone'[, string $code=null[, string $message = '']])

    :param string  $description: 向用户显示的错误消息。
    :param string $code: 自定义 API 专用错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    请求的资源此前已被删除且不再可用时，设置相应的状态码。状态码通常为 410。

    .. literalinclude:: api_responses/015.php

.. php:method:: failTooManyRequests(string $description = 'Too Many Requests'[, string $code=null[, string $message = '']])

    :param string  $description: 向用户显示的错误消息。
    :param string $code: 自定义 API 专用错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    客户端调用 API 端点次数过多时设置相应的状态码。通常源于流量控制或频率限制。状态码通常为 400。

    .. literalinclude:: api_responses/016.php

.. php:method:: failServerError(string $description = 'Internal Server Error'[, string $code = null[, string $message = '']])

    :param string $description: 向用户显示的错误消息。
    :param string $code: 自定义 API 专用错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象 send() 方法的返回值。

    服务器发生错误时设置相应的状态码。

    .. literalinclude:: api_responses/017.php
