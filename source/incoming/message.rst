#############
HTTP 消息
#############

Message 类为 HTTP 消息中请求和响应共有的部分提供了一个接口,包括消息体、协议版本、用于处理头的实用程序以及处理内容协商的方法。

此类是 :doc:`请求类 <../incoming/request>` 和 :doc:`响应类 <../outgoing/response>` 都扩展的父类。

***************
类参考
***************

.. php:namespace:: CodeIgniter\HTTP

.. php:class:: Message

    .. php:method:: getBody()

        :returns: 当前消息体
        :rtype: mixed

        如果已设置,返回当前消息体。如果不存在正文,则返回 null:

        .. literalinclude:: message/001.php

    .. php:method:: setBody($data)

        :param  mixed  $data: 消息的正文。
        :returns: Message|Response 实例以允许链式调用方法。
        :rtype: CodeIgniter\\HTTP\\Message|CodeIgniter\\HTTP\\Response

        设置当前请求的消息体。

    .. php:method:: appendBody($data)

        :param  mixed  $data: 消息的正文。
        :returns: Message|Response 实例以允许链式调用方法。
        :rtype: CodeIgniter\\HTTP\\Message|CodeIgniter\\HTTP\\Response

        向当前请求的消息体附加数据。

    .. php:method:: populateHeaders()

        :returns: void

        扫描并解析 SERVER 数据中的标头,并存储以供以后访问。
        这由 :doc:`IncomingRequest 类 <../incoming/incomingrequest>` 使用,以使当前请求的标头可用。

        标头是以 ``HTTP_`` 开头的任何服务器数据,如 ``HTTP_HOST``。每个消息都从其标准的大写和下划线格式转换为 ucwords 和破折号格式。
        从字符串中删除前导 ``HTTP_``。因此 ``HTTP_ACCEPT_LANGUAGE`` 变成 ``Accept-Language``。

    .. php:method:: headers()

        :returns: 找到的所有标头的数组。
        :rtype: array

        返回找到或先前设置的所有标头的数组。

    .. php:method:: header($name)

        :param  string  $name: 你要检索其值的标头的名称。
        :returns: 返回单个标头对象。如果存在多个同名标头,则返回标头对象数组。
        :rtype: \CodeIgniter\\HTTP\\Header|array

        允许你检索单个消息标头的当前值。``$name`` 是不区分大小写的标头名称。
        尽管内部会按上述方式转换标头,但你可以使用任何情况访问标头:

        .. literalinclude:: message/002.php

        如果标头有多个值, ``getValue()`` 将返回值数组。你可以使用 ``getValueLine()`` 方法将值作为字符串检索:

        .. literalinclude:: message/003.php

        你可以通过第二个参数传递过滤值来过滤标头:

        .. literalinclude:: message/004.php

    .. php:method:: hasHeader($name)

        :param  string  $name: 你要查看其是否存在的标头的名称。
        :returns: 如果存在则返回 true,否则返回 false。
        :rtype: bool

    .. php:method:: getHeaderLine($name)

        :param  string $name: 要检索的标头的名称。
        :returns: 表示标头值的字符串。
        :rtype: string

        以字符串形式返回标头的值。当标头有多个值时,此方法使你可以轻松获取标头值的字符串表示形式。值被适当连接:

        .. literalinclude:: message/005.php

    .. php:method:: setHeader($name, $value)

        :param string $name: 要为其设置值的标头的名称。
        :param mixed  $value: 要设置标头的值。
        :returns: 当前的 Message|Response 实例
        :rtype: CodeIgniter\\HTTP\\Message|CodeIgniter\\HTTP\\Response

        设置单个标头的值。``$name`` 是标头的不区分大小写的名称。如果集合中还不存在该标头,则会创建它。``$value`` 可以是字符串或字符串数组:

        .. literalinclude:: message/006.php

    .. php:method:: removeHeader($name)

        :param string $name: 要删除的标头的名称。
        :returns: 当前消息实例
        :rtype: CodeIgniter\\HTTP\\Message

        从消息中删除标头。``$name`` 是标头的不区分大小写的名称:

        .. literalinclude:: message/007.php

    .. php:method:: appendHeader($name, $value)

        :param string $name: 要修改的标头的名称
        :param string  $value: 要添加到标头的值。
        :returns: 当前消息实例
        :rtype: CodeIgniter\\HTTP\\Message

        向现有标头添加一个值。标头必须已经是一个值数组,而不是单个字符串。如果它是一个字符串,则会抛出 LogicException。

        .. literalinclude:: message/008.php

    .. php:method:: prependHeader($name, $value)

        :param string $name: 要修改的标头的名称
        :param string  $value: 要在标头前面添加的值。
        :returns: 当前消息实例
        :rtype: CodeIgniter\\HTTP\\Message

        在现有标头前面添加一个值。标头必须已经是一个值数组,而不是单个字符串。如果它是一个字符串,则会抛出 LogicException。

        .. literalinclude:: message/009.php

    .. php:method:: getProtocolVersion()

        :returns: 当前的 HTTP 协议版本
        :rtype: string

        返回消息的当前 HTTP 协议。如果未设置,将返回 ``null``。可接受的值为 “1.0”、“1.1” 和 “2.0”。

    .. php:method:: setProtocolVersion($version)

        :param string $version: HTTP 协议版本
        :returns: 当前消息实例
        :rtype: CodeIgniter\\HTTP\\Message

        设置此消息使用的 HTTP 协议版本。有效值为 “1.0”、“1.1” 和 “2.0”:

        .. literalinclude:: message/010.php
