#############
请求类
#############

请求类是 HTTP 请求的面向对象表示。这旨在适用于传入请求,例如来自浏览器对应用程序的请求,以及传出请求,例如应用程序对第三方应用程序的请求所用的请求。

这个类提供了它们都需要的常见功能,但这两种情况都有自定义类来扩展请求类以添加特定功能。在实践中,你需要使用这些类。

有关更多使用详细信息,请参阅 :doc:`IncomingRequest 类 <./incomingrequest>` 和 :doc:`CURLRequest 类 <../libraries/curlrequest>` 的文档。

***************
类参考
***************

.. php:namespace:: CodeIgniter\HTTP

.. php:class:: Request

    .. php:method:: getIPAddress()

        :returns: 如果可以检测到,则为用户的 IP 地址。如果 IP 地址不是有效的 IP 地址,则返回 ``0.0.0.0``。
        :rtype:   string

        返回当前用户的 IP 地址。如果 IP 地址无效,该方法将返回 ``0.0.0.0``:

        .. literalinclude:: request/001.php

        .. important:: 该方法会考虑 ``Config\App::$proxyIPs`` 设置,并将 HTTP 头中报告的允许 IP 地址的客户端 IP 地址返回。

    .. php:method:: isValidIP($ip[, $which = ''])

        .. deprecated:: 4.0.5
           请改用 :doc:`../libraries/validation`。

        .. important:: 此方法已弃用。它将在未来版本中删除。

        :param    string $ip: IP 地址
        :param    string $which: IP 协议(``ipv4`` 或 ``ipv6``)
        :returns: 如果地址有效则为 true,如果无效则为 false
        :rtype:   bool

        将 IP 地址作为输入,并根据它是否有效返回 true 或 false(布尔值)。

        .. note:: 上面的 ``$request->getIPAddress()`` 方法会自动验证 IP 地址。

            .. literalinclude:: request/002.php

        可选的第二个字符串参数为“ipv4”或“ipv6”来指定 IP 格式。默认检查这两种格式。

    .. php:method:: getMethod([$upper = false])

        .. important:: ``$upper`` 参数的使用已被弃用。它将在未来版本中删除。

        :param bool $upper: 是否以大写或小写返回请求方法名称
        :returns: HTTP 请求方法
        :rtype: string

        返回 ``$_SERVER['REQUEST_METHOD']``,可选择设置为大写或小写。

        .. literalinclude:: request/003.php

    .. php:method:: setMethod($method)

        .. deprecated:: 4.0.5
           请改用 :php:meth:`CodeIgniter\\HTTP\\Request::withMethod()`。

        :param string $method: 设置请求方法。在伪造请求时使用。
        :returns: 这个请求
        :rtype: Request

    .. php:method:: withMethod($method)

        .. versionadded:: 4.0.5

        :param string $method: 设置请求方法。
        :returns: 新的请求实例
        :rtype: Request

    .. php:method:: getServer([$index = null[, $filter = null[, $flags = null]]])

        :param    mixed     $index: 值名称
        :param    int       $filter: 要应用的过滤类型。过滤器列表可在 `PHP 手册 <https://www.php.net/manual/en/filter.filters.php>`__ 中找到。
        :param    int|array $flags: 要应用的标志。标志列表可在 `PHP 手册 <https://www.php.net/manual/en/filter.filters.flags.php>`__ 中找到。
        :returns: 如果找到,则返回 ``$_SERVER`` 项目的值,如果没有找到,则为 null
        :rtype:   mixed

        此方法与 :doc:`IncomingRequest 类 <./incomingrequest>` 中的 ``getPost()``、``getGet()`` 和 ``getCookie()`` 方法相同,只是它获取服务器数据(``$_SERVER``):

        .. literalinclude:: request/004.php

        要返回多个 ``$_SERVER`` 值的数组,请传递所有所需键的数组。

        .. literalinclude:: request/005.php

    .. php:method:: getEnv([$index = null[, $filter = null[, $flags = null]]])

        :param    mixed     $index: 值名称
        :param    int       $filter: 要应用的过滤类型。过滤器列表可在 `PHP 手册 <https://www.php.net/manual/en/filter.filters.php>`__ 中找到。
        :param    int|array $flags: 要应用的标志。标志列表可在 `PHP 手册 <https://www.php.net/manual/en/filter.filters.flags.php>`__ 中找到。
        :returns: 如果找到,则返回 ``$_ENV`` 项目的值,如果没有找到,则为 null
        :rtype:   mixed

        此方法与 :doc:`IncomingRequest 类 <./incomingrequest>` 中的 ``getPost()``、``getGet()`` 和 ``getCookie()`` 方法相同,只是它获取环境数据(``$_ENV``):

        .. literalinclude:: request/006.php

        要返回多个 ``$_ENV`` 值的数组,请传递所有所需键的数组。

        .. literalinclude:: request/007.php

    .. php:method:: setGlobal($method, $value)

        :param    string $method: 方法名称
        :param    mixed  $value:  要添加的数据
        :returns: 这个请求
        :rtype:   Request

        允许手动设置 PHP 全局变量的值,如 ``$_GET``、``$_POST`` 等。

    .. php:method:: fetchGlobal($method [, $index = null[, $filter = null[, $flags = null]]])

        :param    string    $method: 输入过滤常量
        :param    mixed     $index: 值名称
        :param    int       $filter: 要应用的过滤类型。过滤器列表可在 `PHP 手册 <https://www.php.net/manual/en/filter.filters.php>`__ 中找到。
        :param    int|array $flags: 要应用的标志。标志列表可在 `PHP 手册 <https://www.php.net/manual/en/filter.filters.flags.php>`__ 中找到。
        :rtype:   mixed

        从 cookie、get、post 等全局变量中获取一个或多个项目。可以通过传递过滤器在检索时可选地过滤输入。
