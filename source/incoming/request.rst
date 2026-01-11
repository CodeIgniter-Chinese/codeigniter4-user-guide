#############
Request 类
#############

Request 类是 HTTP 请求的面向对象表示。这既适用于传入请求（例如浏览器向应用程序发出的请求），
也适用于传出请求（例如应用程序向第三方应用程序发送的请求）。

该类提供了两者所需的通用功能，但两种情况都有从 Request 类继承的自定义类以添加特定功能。
在实践中，你需要使用这些子类。

有关更多使用细节，请参阅 :doc:`IncomingRequest 类 <./incomingrequest>` 和
:doc:`CURLRequest 类 <../libraries/curlrequest>` 的文档。

***************
类参考
***************

.. php:namespace:: CodeIgniter\HTTP

.. php:class:: Request

    .. php:method:: getIPAddress()

        :returns: 用户的 IP 地址，如果可以检测到。如果 IP 地址无效，则返回 ``0.0.0.0``。
        :rtype:   string

        返回当前用户的 IP 地址。如果 IP 地址无效，该方法将返回 ``0.0.0.0``：

        .. literalinclude:: request/001.php

        .. important:: 该方法会考虑 ``Config\App::$proxyIPs`` 设置，对于允许的 IP 地址，将返回由 HTTP 标头报告的客户端 IP 地址。

    .. php:method:: isValidIP($ip[, $which = ''])

        .. deprecated:: 4.0.5
           请改用 :doc:`../libraries/validation`。

        .. important:: 该方法已废弃。将在未来版本中移除。

        :param    string $ip: IP 地址
        :param    string $which: IP 协议（``ipv4`` 或 ``ipv6``）
        :returns: 如果地址有效返回 true，否则返回 false
        :rtype:   bool

        接收一个 IP 地址作为输入，根据其是否有效返回 true 或 false（布尔值）。

        .. note:: 上面的 $request->getIPAddress() 方法会自动验证 IP 地址。

            .. literalinclude:: request/002.php

        接受可选的第二个字符串参数 ``ipv4`` 或 ``ipv6`` 以指定 IP 格式。默认情况下检查这两种格式。

    .. php:method:: getMethod()

        :returns: HTTP 请求方法
        :rtype: string

        返回 ``$_SERVER['REQUEST_METHOD']``。

        .. literalinclude:: request/003.php

    .. php:method:: setMethod($method)

        .. deprecated:: 4.0.5
           请改用 :php:meth:`CodeIgniter\\HTTP\\Request::withMethod()`。

        :param string $method: 设置请求方法。在伪造请求时使用。
        :returns: 当前请求对象
        :rtype: Request

    .. php:method:: withMethod($method)

        .. versionadded:: 4.0.5

        :param string $method: 设置请求方法。
        :returns: 新的请求实例
        :rtype: Request

    .. php:method:: getServer([$index = null[, $filter = null[, $flags = null]]])

        :param    mixed     $index: 值名称
        :param    int       $filter: 要应用的过滤器类型。可以在 `PHP 手册 <https://www.php.net/manual/zh/filters.php>`__ 中找到过滤器列表。
        :param    int|array $flags: 要应用的标志。可以在 `PHP 手册 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到标志列表。
        :returns: 如果找到则返回 ``$_SERVER`` 项目值，否则返回 null
        :rtype:   mixed

        此方法与 :doc:`IncomingRequest 类 <./incomingrequest>` 中的 ``getPost()``、``getGet()`` 和 ``getCookie()`` 方法相同，
        只是它获取服务器数据（``$_SERVER``）：

        .. literalinclude:: request/004.php

        要返回包含多个 ``$_SERVER`` 值的数组，请将所有需要的键作为数组传递。

        .. literalinclude:: request/005.php

    .. php:method:: getEnv([$index = null[, $filter = null[, $flags = null]]])

        .. deprecated:: 4.4.4 此方法从一开始就无法正常工作。请改用
            :php:func:`env()`。

        :param    mixed     $index: 值名称
        :param    int       $filter: 要应用的过滤器类型。可以在 `PHP 手册 <https://www.php.net/manual/zh/filters.php>`__ 中找到过滤器列表。
        :param    int|array $flags: 要应用的标志。可以在 `PHP 手册 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到标志列表。
        :returns: 如果找到则返回 ``$_ENV`` 项目值，否则返回 null
        :rtype:   mixed

        此方法与 :doc:`IncomingRequest 类 <./incomingrequest>` 中的 ``getPost()``、``getGet()`` 和 ``getCookie()`` 方法相同，
        只是它获取环境变量数据（``$_ENV``）：

        .. literalinclude:: request/006.php

        要返回包含多个 ``$_ENV`` 值的数组，请将所有需要的键作为数组传递。

        .. literalinclude:: request/007.php

    .. php:method:: setGlobal($method, $value)

        :param    string $method: 方法名称
        :param    mixed  $value:  要添加的数据
        :returns: 当前请求对象
        :rtype:   Request

        允许手动设置 PHP 全局变量的值，如 ``$_GET``、``$_POST`` 等。

    .. php:method:: fetchGlobal($method [, $index = null[, $filter = null[, $flags = null]]])

        :param    string    $method: 输入过滤器常量
        :param    mixed     $index: 值名称
        :param    int       $filter: 要应用的过滤器类型。可以在 `PHP 手册 <https://www.php.net/manual/zh/filters.php>`__ 中找到过滤器列表。
        :param    int|array $flags: 要应用的标志。可以在 `PHP 手册 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__ 中找到标志列表。
        :rtype:   mixed

        从全局变量（如 cookie、get、post 等）中获取一项或多项。
        可以在检索时通过传入过滤器来过滤输入。
