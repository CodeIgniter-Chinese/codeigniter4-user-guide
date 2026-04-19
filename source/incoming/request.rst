#############
Request 类
#############

Request 类是 HTTP 请求的面向对象表示。该类既可用于处理传入请求（例如浏览器访问应用的请求），也可用于处理传出请求（例如从应用发往第三方应用的请求）。

此类提供了两者所需的通用功能，但在实际开发中，通常会使用继承自 Request 类的子类来调用特定功能。

关于更多使用细节，请参阅 :doc:`IncomingRequest 类 <./incomingrequest>` 和 :doc:`CURLRequest 类 <../libraries/curlrequest>` 的文档。

***************
类参考
***************

.. php:namespace:: CodeIgniter\HTTP

.. php:class:: Request

    .. php:method:: getIPAddress()

        :returns: 如果能检测到，则返回用户的 IP 地址；如果 IP 地址无效，则返回 ``0.0.0.0``。
        :rtype:   string

        返回当前用户的 IP 地址。如果 IP 地址无效，该方法将返回 ``0.0.0.0``：

        .. literalinclude:: request/001.php

        .. important:: 此方法会参考 ``Config\App::$proxyIPs`` 设置，并针对允许的 IP 地址返回由 HTTP 标头报告的客户端 IP。

    .. php:method:: isValidIP($ip[, $which = ''])

        .. deprecated:: 4.0.5
           请改用 :doc:`../libraries/validation`。

        .. important:: 此方法已废弃，将在未来版本中移除。

        :param    string $ip: IP 地址
        :param    string $which: IP 协议（``ipv4`` 或 ``ipv6``）
        :returns: 地址有效返回 true，否则返回 false
        :rtype:   bool

        输入 IP 地址，并根据其是否有效返回布尔值（true 或 false）。

        .. note:: 上述 $request->getIPAddress() 方法会自动验证 IP 地址。

            .. literalinclude:: request/002.php

        可接受可选的第二个字符串参数（``ipv4`` 或 ``ipv6``）来指定 IP 格式。默认情况下会同时检查两种格式。

    .. php:method:: getMethod()

        :returns: HTTP 请求方法
        :rtype: string

        返回 ``$_SERVER['REQUEST_METHOD']``。

        .. literalinclude:: request/003.php

    .. php:method:: setMethod($method)

        .. deprecated:: 4.0.5
           请改用 :php:meth:`CodeIgniter\\HTTP\\Request::withMethod()`。

        :param string $method: 设置请求方法。用于模拟请求。
        :returns: 当前请求
        :rtype: Request

    .. php:method:: withMethod($method)

        .. versionadded:: 4.0.5

        :param string $method: 设置请求方法。
        :returns: 新的请求实例
        :rtype: Request

    .. php:method:: getServer([$index = null[, $filter = null[, $flags = null]]])

        :param    mixed     $index: 变量名
        :param    int       $filter: 要应用的过滤器类型。过滤器列表详见 `PHP 手册 <https://www.php.net/manual/zh/filters.php>`__。
        :param    int|array $flags: 要应用的标志。标志列表详见 `PHP 手册 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__。
        :returns: 如果找到则返回 ``$_SERVER`` 项的值，否则返回 null
        :rtype:   mixed

        此方法与 :doc:`IncomingRequest 类 <./incomingrequest>` 中的 ``getPost()``、``getGet()`` 和 ``getCookie()`` 类似，仅用于获取服务器数据（``$_SERVER``）：

        .. literalinclude:: request/004.php

        如需返回包含多个 ``$_SERVER`` 值的数组，请以数组形式传递所有需要的键。

        .. literalinclude:: request/005.php

    .. php:method:: getEnv([$index = null[, $filter = null[, $flags = null]]])

        .. deprecated:: 4.4.4 此方法自始至终无法正常工作。请改用
            :php:func:`env()`。

        :param    mixed     $index: 变量名
        :param    int       $filter: 要应用的过滤器类型。过滤器列表详见 `PHP 手册 <https://www.php.net/manual/zh/filters.php>`__。
        :param    int|array $flags: 要应用的标志。标志列表详见 `PHP 手册 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__。
        :returns: 如果找到则返回 ``$_ENV`` 项的值，否则返回 null
        :rtype:   mixed

        此方法与 :doc:`IncomingRequest 类 <./incomingrequest>` 中的 ``getPost()``、``getGet()`` 和 ``getCookie()`` 类似，仅用于获取环境变量数据（``$_ENV``）：

        .. literalinclude:: request/006.php

        如需返回包含多个 ``$_ENV`` 值的数组，请以数组形式传递所有需要的键。

        .. literalinclude:: request/007.php

    .. php:method:: setGlobal($method, $value)

        :param    string $method: 方法名称
        :param    mixed  $value:  要添加的数据
        :returns: 当前请求
        :rtype:   Request

        允许手动设置 PHP 全局变量的值，如 ``$_GET``、``$_POST`` 等。

    .. php:method:: fetchGlobal($method [, $index = null[, $filter = null[, $flags = null]]])

        :param    string    $method: 输入过滤器常量
        :param    mixed     $index: 变量名
        :param    int       $filter: 要应用的过滤器类型。过滤器列表详见 `PHP 手册 <https://www.php.net/manual/zh/filters.php>`__。
        :param    int|array $flags: 要应用的标志。标志列表详见 `PHP 手册 <https://www.php.net/manual/zh/filter.constants.php#filter.constants.flags.generic>`__。
        :rtype:   mixed

        从全局变量（如 cookie、get、post 等）中获取一个或多个项目。获取时可通过传入过滤器对输入进行过滤。
