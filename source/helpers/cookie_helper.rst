###############
Cookie 辅助函数
###############

Cookie 辅助函数文件包含了帮助处理 cookie 的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: cookie_helper/001.php

可用函数
===================

以下函数可用:

.. php:function:: set_cookie($name[, $value = ''[, $expire = 0[, $domain = ''[, $path = '/'[, $prefix = ''[, $secure = false[, $httpOnly = false[, $sameSite = '']]]]]]]])

    :param    array|Cookie|string    $name: Cookie 名称 *或* 此函数可用的所有参数的关联数组 *或* ``CodeIgniter\Cookie\Cookie`` 的实例
    :param    string    $value: Cookie 值
    :param    int    $expire: 到期秒数。如果设置为 ``0`` 则 cookie 仅在浏览器打开时有效
    :param    string    $domain: Cookie 域名(通常:.yourdomain.com)
    :param    string    $path: Cookie 路径
    :param    string    $prefix: Cookie 名称前缀。如果为 ``''``,则使用 **app/Config/Cookie.php** 中的默认值
    :param    bool    $secure: 是否仅通过 HTTPS 发送 cookie。如果为 ``null``,则使用 **app/Config/Cookie.php** 中的默认值
    :param    bool    $httpOnly: 是否从 JavaScript 隐藏 cookie。如果为 ``null``,则使用 **app/Config/Cookie.php** 中的默认值
    :param    string    $sameSite: SameSite cookie 参数的值。如果为 ``null``,则使用 **app/Config/Cookie.php** 中的默认值
    :rtype:    void

    .. note:: 在 v4.2.7 之前,由于一个 bug, ``$secure`` 和 ``$httpOnly`` 的默认值是 ``false``,
        从不使用 **app/Config/Cookie.php** 中的值。

    该辅助函数为设置浏览器 cookie 提供了更友好的语法。有关其用法的描述,请参阅
    :doc:`Response 库 </outgoing/response>`,因为此函数是
    :php:meth:`CodeIgniter\\HTTP\\Response::setCookie()` 的别名。

    .. note:: 这个辅助函数只设置全局响应实例的浏览器 Cookie（由 ``Services::response()`` 返回）。所以，如果你创建并返回另一个响应实例（例如，如果你调用 :php:func:`redirect()`），这里设置的 Cookie 不会自动发送。

.. php:function:: get_cookie($index[, $xssClean = false[, $prefix = '']])

    :param    string    $index: Cookie 名称
    :param    bool    $xssClean: 是否对返回的值应用 XSS 过滤
    :param    string|null  $prefix: Cookie 名称前缀。如果设置为 ``''``,将使用 **app/Config/Cookie.php** 中的默认值。如果设置为 ``null``,则没有前缀
    :returns:    cookie 值,如果未找到则为 null
    :rtype:    mixed

    .. note:: 从 v4.2.1 开始,引入了第三个参数 ``$prefix``,并且由于一个错误修复,行为发生了一些变化。详见 :ref:`升级 <upgrade-421-get_cookie>`。

    这个辅助函数为你提供了更友好的语法来获取浏览器的 Cookie。有关其使用的详细描述，请参考 :doc:`IncomingRequest 库 </incoming/incomingrequest>`，因为这个函数的行为与 :php:meth:`CodeIgniter\\HTTP\\IncomingRequest::getCookie()` 非常相似，只是它还会在前面添加你在 **app/Config/Cookie.php** 文件中设置的 ``Config\Cookie::$prefix``。

    .. warning:: 使用 XSS 过滤是一个不好的做法。它不能完美地防止 XSS 攻击。在视图中建议使用正确 ``$context`` 的 :php:func:`esc()`。

.. php:function:: delete_cookie($name[, $domain = ''[, $path = '/'[, $prefix = '']]])

    :param string $name: Cookie 名称
    :param string $domain: Cookie 域名(通常:.yourdomain.com)
    :param string $path: Cookie 路径
    :param string $prefix: Cookie 前缀
    :rtype: void

    允许你删除一个 cookie。除非你设置了自定义路径或其他值,否则只需要 cookie 的名称。

    .. literalinclude:: cookie_helper/002.php

    此函数与 :php:func:`set_cookie()` 其他方面相同,只是它没有 ``value`` 和 ``expire`` 参数。

    这也只是为删除全局响应实例（由 ``Services::response()`` 返回）的浏览器 Cookie 设置浏览器 Cookie。

    .. note:: 当你使用 :php:func:`set_cookie()` 时,如果 ``value`` 设置为空字符串且 ``expire`` 设置为 ``0``,则 cookie 将被删除。
        如果 ``value`` 设置为非空字符串且 ``expire`` 设置为 ``0``,则 cookie 仅在浏览器打开时有效。

    你可以在第一个参数中提交值数组,也可以设置离散参数。

    .. literalinclude:: cookie_helper/003.php

.. php:function:: has_cookie(string $name[, ?string $value = null[, string $prefix = '']])

    :param string $name: Cookie 名称
    :param string|null $value: Cookie 值
    :param string $prefix: Cookie 前缀
    :rtype: bool

    检查在全局响应实例中（由 ``Services::response()`` 返回）是否存在同名的 Cookie。这是 :php:meth::`CodeIgniter\\HTTP\\Response::hasCookie()` 的别名。
