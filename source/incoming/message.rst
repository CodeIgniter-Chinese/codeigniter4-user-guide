#############
HTTP 消息
#############

Message 类提供了一个统一的接口，用于访问 HTTP 消息中“请求”和“响应”所共有的部分，其中包括消息正文、协议版本、操作标头信息的辅助方法，以及处理内容协商的方法。

这个类是 :doc:`Request 类 <../incoming/request>` 和
:doc:`Response 类 <../outgoing/response>` 的父类，通常不直接使用。

***************
类参考
***************

.. php:namespace:: CodeIgniter\HTTP

.. php:class:: Message

    .. php:method:: getBody()

        :returns: 当前消息正文
        :rtype: mixed

        返回当前消息正文，如果已设置的话。如果正文不存在，返回 null：

        .. literalinclude:: message/001.php

    .. php:method:: setBody($data)

        :param  mixed  $data: 消息正文。
        :returns: Message|Response 实例，允许方法链式调用。
        :rtype: CodeIgniter\\HTTP\\Message|CodeIgniter\\HTTP\\Response

        设置当前请求的正文。

    .. php:method:: appendBody($data)

        :param  mixed  $data: 消息正文。
        :returns: Message|Response 实例，允许方法链式调用。
        :rtype: CodeIgniter\\HTTP\\Message|CodeIgniter\\HTTP\\Response

        将数据追加到当前请求的正文。

    .. php:method:: populateHeaders()

        :returns: void

        扫描并解析 SERVER 数据中的标头，并将其存储以供后续访问。
        :doc:`IncomingRequest 类 <../incoming/incomingrequest>` 使用此方法使
        当前请求的标头可用。

        标头是以 ``HTTP_`` 开头的任何 SERVER 数据，例如 ``HTTP_HOST``。每个标头
        都会从标准的大写加下划线格式转换为单词首字母大写加短横线的格式。
        字符串前面的 ``HTTP_`` 会被移除。因此 ``HTTP_ACCEPT_LANGUAGE`` 变为
        ``Accept-Language``。

    .. php:method:: headers()

        :returns: 所有找到的标头的数组。
        :rtype: array

        返回所有找到或之前设置的标头的数组。

    .. php:method:: header($name)

        :param  string  $name: 你要获取值的标头名称。
        :returns: 返回单个标头对象。如果存在多个同名标头，则返回标头对象的数组。
        :rtype: \CodeIgniter\\HTTP\\Header|array

        允许你获取单个消息标头的当前值。``$name`` 是不区分大小写的标头名称。
        虽然标头在内部如上所述进行了转换，但你可以使用任何大小写形式访问标头：

        .. literalinclude:: message/002.php

        如果标头有多个值，``getValue()`` 将返回值的数组。你可以使用 ``getValueLine()``
        方法以字符串形式获取值：

        .. literalinclude:: message/003.php

        你可以通过传入第二个参数作为过滤值来过滤标头：

        .. literalinclude:: message/004.php

    .. php:method:: hasHeader($name)

        :param  string  $name: 你要检查是否存在的标头名称。
        :returns: 如果存在返回 true，否则返回 false。
        :rtype: bool

    .. php:method:: getHeaderLine($name)

        :param  string $name: 要获取的标头名称。
        :returns: 表示标头值的字符串。
        :rtype: string

        以字符串形式返回标头的值。当标头有多个值时，此方法允许你轻松获取标头值的
        字符串表示形式。这些值会被适当地连接起来：

        .. literalinclude:: message/005.php

    .. php:method:: setHeader($name, $value)

        :param string $name: 要设置值的标头名称。
        :param mixed  $value: 要设置的标头值。
        :returns: 当前 Message|Response 实例
        :rtype: CodeIgniter\\HTTP\\Message|CodeIgniter\\HTTP\\Response

        设置单个标头的值。``$name`` 是不区分大小写的标头名称。如果集合中尚不存在
        该标头，则会创建它。``$value`` 可以是字符串或字符串数组：

        .. literalinclude:: message/006.php

    .. php:method:: removeHeader($name)

        :param string $name: 要移除的标头名称。
        :returns: 当前消息实例
        :rtype: CodeIgniter\\HTTP\\Message

        从消息中移除标头。``$name`` 是不区分大小写的标头名称：

        .. literalinclude:: message/007.php

    .. php:method:: appendHeader($name, $value)

        :param string $name: 要修改的标头名称
        :param string  $value: 要添加到标头的值。
        :returns: 当前消息实例
        :rtype: CodeIgniter\\HTTP\\Message

        向现有标头添加值。该标头必须已经是值的数组，而不是单个字符串。
        如果是字符串，将抛出 LogicException 异常。

        .. literalinclude:: message/008.php

    .. php:method:: prependHeader($name, $value)

        :param string $name: 要修改的标头名称
        :param string  $value: 要在标头前面添加的值。
        :returns: 当前消息实例
        :rtype: CodeIgniter\\HTTP\\Message

        向现有标头前面添加一个值。该标头必须已经是值的数组，而不是单个字符串。
        如果是字符串，将抛出 LogicException 异常。

        .. literalinclude:: message/009.php

    .. php:method:: addHeader($name, $value)

        .. versionadded:: 4.5.0

        :param string $name: 要添加的标头名称。
        :param string  $value: 标头的值。
        :returns: 当前消息实例
        :rtype: CodeIgniter\\HTTP\\Message

        添加具有相同名称的标头（不仅仅是标头值）。
        仅当你设置多个同名标头时使用此方法，

        .. literalinclude:: message/011.php

    .. php:method:: getProtocolVersion()

        :returns: 当前 HTTP 协议版本
        :rtype: string

        返回消息的当前 HTTP 协议。如果未设置，将返回 ``1.1``。

    .. php:method:: setProtocolVersion($version)

        :param string $version: HTTP 协议版本
        :returns: 当前消息实例
        :rtype: CodeIgniter\\HTTP\\Message

        设置此消息使用的 HTTP 协议版本。有效值为
        ``1.0``、``1.1``、``2.0`` 和 ``3.0``：

        .. literalinclude:: message/010.php
