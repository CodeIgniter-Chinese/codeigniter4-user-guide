##################
API 响应特性
##################

大多数现代 PHP 开发需要构建 API,无论是简单地为 javascript 密集的
单页应用提供数据,还是作为独立产品。CodeIgniter 提供了一个 API 响应特性,可以
与任何控制器一起使用,使常见的响应类型简单化,而无需记住哪个 HTTP 状态码
应该用于哪种响应类型。

.. contents::
    :local:
    :depth: 2

*************
示例用法
*************

下面的示例显示了控制器中常见的使用模式。

.. literalinclude:: api_responses/001.php

在此示例中,返回 HTTP 状态码 201,以及通用的状态消息“Created”。方法
存在最常见的用例:

.. literalinclude:: api_responses/002.php

***********************
处理响应类型
***********************

当你在任何这些方法中传递数据时,它们将根据以下标准确定数据类型以格式化结果:

* 如果数据是字符串,它将被视为要返回给客户端的 HTML。
* 如果数据是数组,它将根据控制器的 ``$this->format`` 值进行格式化。如果为空,
  它将尝试用客户端请求的内容类型协商内容类型,默认为 JSON
  如果在 **Config/Format.php** 中的 ``$supportedResponseFormats`` 属性未指定其他格式。

要定义用于格式化的格式器,请编辑 **Config/Format.php**。 ``$supportedResponseFormats`` 包含应用程序可以
自动格式化响应的 mime 类型列表。默认情况下,系统知道如何格式化 XML 和 JSON 响应:

.. literalinclude:: api_responses/003.php

这是在 :doc:`内容协商 </incoming/content_negotiation>` 期间确定要返回哪种类型响应时使用的数组。
如果客户端请求和你支持的之间没有匹配,则返回此数组中的第一种格式。

接下来,你需要定义用于格式化数据数组的类。这必须是一个完全限定的类名,并且该类必须实现
``CodeIgniter\Format\FormatterInterface``。开箱即用地支持 JSON 和 XML 的格式化程序:

.. literalinclude:: api_responses/004.php

因此,如果请求在 **Accept** 头中请求 JSON 格式的数据,传递给任何 ``respond*`` 或 ``fail*``
方法的数据数组将由 ``CodeIgniter\Format\JSONFormatter`` 类格式化。生成的 JSON 数据将发送回客户端。

***************
类参考
***************

.. php:method:: setResponseFormat($format)

    :param string $format: 要返回的响应类型, ``json`` 或 ``xml``

    这定义了在响应中格式化数组时使用的格式。如果为 ``$format`` 提供 null 值,它将通过内容协商自动确定。

.. literalinclude:: api_responses/005.php

.. php:method:: respond($data[, $statusCode = 200[, $message = '']])

    :param mixed  $data: 要返回给客户端的数据。字符串或数组。
    :param int    $statusCode: 要返回的 HTTP 状态码。默认为 200
    :param string $message: 要返回的自定义“原因”消息。

    这是特性中所有其他方法用于向客户端返回响应的方法。

    ``$data`` 元素可以是字符串或数组。默认情况下,字符串将作为 HTML 返回,
    而数组将通过 json_encode 运行并返回为 JSON,除非 :doc:`内容协商 </incoming/content_negotiation>`
    确定应以不同格式返回。

    如果传递了 ``$message`` 字符串,它将替代标准 IANA 原因代码用于
    响应状态。但是,并非每个客户端都会遵守自定义代码,它们会使用与状态码匹配的 IANA 标准。

    .. note:: 由于它在活动的 Response 实例上设置状态码和主体,所以这应该始终
        是脚本执行中的最后一个方法。

.. php:method:: fail($messages[, int $status = 400[, string $code = null[, string $message = '']]])

    :param mixed $messages: 遇到的错误消息的字符串或字符串数组。
    :param int   $status: 要返回的 HTTP 状态码。默认为 400。
    :param string $code: 自定义的 API 特定错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: 客户端首选格式的多部分响应。

    这是表示失败响应的通用方法,所有其他“fail”方法都使用它。

    ``$messages`` 元素可以是字符串或字符串数组。

    ``$status`` 参数是应返回的 HTTP 状态码。

    由于许多 API 更适合使用自定义错误码,所以第三个参数可以传入自定义错误码。如果没有值,它将与 ``$status`` 相同。

    如果传递了 ``$message`` 字符串,它将替代标准 IANA 原因代码用于
    响应状态。但是,并非每个客户端都会遵守自定义代码,它们会使用与状态码匹配的 IANA 标准。

    响应是一个包含两个元素的数组:“error”和“messages”。“error”元素包含错误的状态码。
    “messages”元素包含错误消息数组。它看起来像:

    .. literalinclude:: api_responses/006.php

.. php:method:: respondCreated($data = null[, string $message = ''])

    :param mixed  $data: 要返回给客户端的数据。字符串或数组。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    设置在创建新资源时通常使用的适当状态码,通常为 201:

    .. literalinclude:: api_responses/007.php

.. php:method:: respondDeleted($data = null[, string $message = ''])

    :param mixed  $data: 要返回给客户端的数据。字符串或数组。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    设置由于此 API 调用删除新资源而通常使用的适当状态码,通常为 200。

    .. literalinclude:: api_responses/008.php

.. php:method:: respondNoContent(string $message = 'No Content')

    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    设置在服务器成功执行命令但没有可发送回客户端的有意义响应时通常使用的适当状态码,通常为 204。

    .. literalinclude:: api_responses/009.php

.. php:method:: failUnauthorized(string $description = 'Unauthorized'[, string $code = null[, string $message = '']])

    :param string  $description: 要显示给用户的错误消息。
    :param string $code: 自定义的 API 特定错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    设置用户未经授权或授权不正确时使用的适当状态码。状态码为 401。

    .. literalinclude:: api_responses/010.php

.. php:method:: failForbidden(string $description = 'Forbidden'[, string $code=null[, string $message = '']])

    :param string  $description: 要显示给用户的错误消息。
    :param string $code: 自定义的 API 特定错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    与 ``failUnauthorized()`` 不同,当请求的 API 端点从不允许时,应使用此方法。
    未授权意味着鼓励客户端使用不同的凭据重试。禁止意味着客户端不应重试,因为它不会有帮助。状态码通常为 403。

    .. literalinclude:: api_responses/011.php

.. php:method:: failNotFound(string $description = 'Not Found'[, string $code=null[, string $message = '']])

    :param string  $description: 要显示给用户的错误消息。
    :param string $code: 自定义的 API 特定错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    设置在找不到请求的资源时使用的适当状态码。状态码通常为 404。

    .. literalinclude:: api_responses/012.php

.. php:method:: failValidationErrors($errors[, string $code=null[, string $message = '']])

    :param mixed  $errors: 要显示给用户的错误消息或消息数组。
    :param string $code: 自定义的 API 特定错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    设置在客户端发送的数据未通过验证规则时使用的适当状态码。状态码通常为 400。

    .. literalinclude:: api_responses/013.php

.. php:method:: failResourceExists(string $description = 'Conflict'[, string $code=null[, string $message = '']])

    :param string  $description: 要显示给用户的错误消息。
    :param string $code: 自定义的 API 特定错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    设置在客户端试图创建的资源已经存在时使用的适当状态码。状态码通常为 409。

    .. literalinclude:: api_responses/014.php

.. php:method:: failResourceGone(string $description = 'Gone'[, string $code=null[, string $message = '']])

    :param string  $description: 要显示给用户的错误消息。
    :param string $code: 自定义的 API 特定错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    设置在先前删除的请求资源不再可用时使用的适当状态码。状态码通常为 410。

    .. literalinclude:: api_responses/015.php

.. php:method:: failTooManyRequests(string $description = 'Too Many Requests'[, string $code=null[, string $message = '']])

    :param string  $description: 要显示给用户的错误消息。
    :param string $code: 自定义的 API 特定错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    设置当客户端调用 API 端点次数过多时使用的适当状态码。这可能是由于某种形式的限流或速率限制。状态码通常为 400。

    .. literalinclude:: api_responses/016.php

.. php:method:: failServerError(string $description = 'Internal Server Error'[, string $code = null[, string $message = '']])

    :param string $description: 要显示给用户的错误消息。
    :param string $code: 自定义的 API 特定错误码。
    :param string $message: 要返回的自定义“原因”消息。
    :returns: Response 对象的 send() 方法的值。

    设置服务器错误时使用的适当状态码。

    .. literalinclude:: api_responses/017.php
