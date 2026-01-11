###############
Cookie 辅助函数
###############

Cookie 辅助函数文件包含协助处理 Cookie 的相关函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数：

.. literalinclude:: cookie_helper/001.php

可用函数
===================

提供以下函数：

.. php:function:: set_cookie($name[, $value = ''[, $expire = 0[, $domain = ''[, $path = '/'[, $prefix = ''[, $secure = false[, $httpOnly = false[, $sameSite = '']]]]]]]])

    :param    array|Cookie|string    $name: Cookie 名称 *或* 包含所有可用参数的关联数组 *或* ``CodeIgniter\Cookie\Cookie`` 实例
    :param    string    $value: Cookie 值
    :param    int    $expire: 过期前的秒数。如果设置为 ``0``，Cookie 仅在浏览器打开期间有效
    :param    string    $domain: Cookie 域名（通常为：.yourdomain.com）
    :param    string    $path: Cookie 路径
    :param    string    $prefix: Cookie 名称前缀。如果设置为 ``''``，则使用 **app/Config/Cookie.php** 中的默认值
    :param    bool    $secure: 是否仅通过 HTTPS 发送 Cookie。如果设置为 ``null``，则使用 **app/Config/Cookie.php** 中的默认值
    :param    bool    $httpOnly: 是否对 JavaScript 隐藏 Cookie。如果设置为 ``null``，则使用 **app/Config/Cookie.php** 中的默认值
    :param    string    $sameSite: SameSite Cookie 参数的值。如果设置为 ``null``，则使用 **app/Config/Cookie.php** 中的默认值
    :rtype:    void

    .. note:: 在 v4.2.7 之前，由于一个 bug，``$secure`` 和 ``$httpOnly`` 的默认值为 ``false``，
        **app/Config/Cookie.php** 中的这些值从未被使用。

    此辅助函数提供了更友好的语法来设置浏览器 Cookie。
    有关其使用的描述，请参阅 :doc:`Response 库 </outgoing/response>`，
    因为该函数是 :php:meth:`CodeIgniter\\HTTP\\Response::setCookie()` 的别名。

    .. note:: 此辅助函数仅将浏览器 Cookie 设置到 ``Services::response()`` 返回的全局 Response
        实例中。因此，如果你创建并返回另一个 Response 实例（例如，如果你调用 :php:func:`redirect()`），
        此处设置的 Cookie 将不会自动发送。

.. php:function:: get_cookie($index[, $xssClean = false[, $prefix = '']])

    :param    string    $index: Cookie 名称
    :param    bool    $xssClean: 是否对返回值应用 XSS 过滤
    :param    string|null  $prefix: Cookie 名称前缀。如果设置为 ``''``，将使用 **app/Config/Cookie.php** 中的默认值。如果设置为 ``null``，则不使用前缀
    :returns:    Cookie 值，如果未找到则返回 null
    :rtype:    mixed

    .. note:: 自 v4.2.1 起，引入了第三个参数 ``$prefix``，由于 bug 修复，行为发生了一些变化。详情请参阅 :ref:`升级 <upgrade-421-get_cookie>`。

    此辅助函数提供了更友好的语法来获取浏览器 Cookie。
    有关其使用的详细描述，请参阅 :doc:`IncomingRequest 库 </incoming/incomingrequest>`，
    因为该函数与 :php:meth:`CodeIgniter\\HTTP\\IncomingRequest::getCookie()` 的行为非常相似，
    不同之处在于它还会在 **app/Config/Cookie.php** 文件中你设置的
    ``Config\Cookie::$prefix`` 前面加上前缀。

    .. warning:: 使用 XSS 过滤是一种不良实践。它不能完全防止 XSS 攻击。建议在视图中使用正确 ``$context`` 的 :php:func:`esc()` 函数。

.. php:function:: delete_cookie($name[, $domain = ''[, $path = '/'[, $prefix = '']]])

    :param string $name: Cookie 名称
    :param string $domain: Cookie 域名（通常为：.yourdomain.com）
    :param string $path: Cookie 路径
    :param string $prefix: Cookie 名称前缀
    :rtype: void

    允许你删除一个 Cookie。除非你设置了自定义路径或其他值，
    否则只需要 Cookie 的名称即可。

    .. literalinclude:: cookie_helper/002.php

    此函数在其他方面与 :php:func:`set_cookie()` 完全相同，只是
    它没有 ``value`` 和 ``expire`` 参数。

    这也只是将用于删除 Cookie 的浏览器 Cookie 设置到
    ``Services::response()`` 返回的全局 Response 实例中。

    .. note:: 当你使用 :php:func:`set_cookie()` 时，
        如果 ``value`` 设置为空字符串且 ``expire`` 设置为 ``0``，则 Cookie 将被删除。
        如果 ``value`` 设置为非空字符串且 ``expire`` 设置为 ``0``，则 Cookie 仅在浏览器打开期间有效。

    你可以在第一个参数中提交一个值数组，
    也可以设置离散的参数。

    .. literalinclude:: cookie_helper/003.php

.. php:function:: has_cookie(string $name[, ?string $value = null[, string $prefix = '']])

    :param string $name: Cookie 名称
    :param string|null $value: Cookie 值
    :param string $prefix: Cookie 前缀
    :rtype: bool

    检查在 ``Services::response()`` 返回的全局 Response 实例中
    是否存在指定名称的 Cookie。这是
    :php:meth:`CodeIgniter\\HTTP\\Response::hasCookie()` 的别名。
