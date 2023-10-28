#######
Cookie
#######

一个 **HTTP Cookie** (网站 Cookie、浏览器 Cookie)是一个服务器发送到用户浏览器的一小段数据。浏览器可以存储它,并在以后向同一服务器的请求中发送它。通常,它用于判断两个请求是否来自同一个浏览器 - 例如,用于保持用户登录状态。它为无状态的 HTTP 协议保存状态信息。

Cookie 主要用于三个目的:

- **会话管理**:登录、购物车、游戏分数或服务器需要记住的任何其他内容
- **个性化**:用户首选项、主题和其他设置
- **跟踪**:记录和分析用户行为

为了帮助你有效地向浏览器发送 Cookie，CodeIgniter 提供了 ``CodeIgniter\Cookie\Cookie`` 类来抽象化 Cookie 的交互。

.. contents::
    :local:
    :depth: 2

****************
创建 Cookie
****************

目前有四种方式可以创建一个新的 ``Cookie`` 值对象。

.. literalinclude:: cookies/001.php

在构造 ``Cookie`` 对象时,只需要 ``name`` 属性是必需的。其余的都是可选的。如果没有修改可选属性,它们的值将由 ``Cookie`` 类中保存的默认值填充。

覆盖默认值
===================

要覆盖类中当前存储的默认值,你可以传递一个 ``Config\Cookie`` 实例或默认值数组给静态 ``Cookie::setDefaults()`` 方法。

.. literalinclude:: cookies/002.php

将 ``Config\Cookie`` 实例或数组传递给 ``Cookie::setDefaults()`` 将有效地覆盖你的默认值,并且持续到新的默认值被传递。

有限的时间内更改默认值
------------------------------------

如果你不想要这种行为,而只是想在有限的时间内更改默认值,你可以利用 ``Cookie::setDefaults()`` 的返回值,它返回旧的默认值数组。

.. literalinclude:: cookies/003.php

*****************************
访问 Cookie 的属性
*****************************

一旦实例化,你就可以通过使用其 getter 方法之一轻松访问 ``Cookie`` 的属性。

.. literalinclude:: cookies/004.php

*****************
不可变 Cookie
*****************

新的 ``Cookie`` 实例是一个 HTTP cookie 的不可变值对象表示。由于是不可变的,修改实例的任何属性都不会影响原始实例。修改 **总是** 返回一个新实例。你需要保留这个新实例才能使用它。

.. literalinclude:: cookies/005.php

********************************
验证 Cookie 的属性
********************************

一个 HTTP cookie 受到几个规范的约束,这些规范需要遵循才能被浏览器接受。因此,在创建或修改 ``Cookie`` 的某些属性时,会对其进行验证,以检查它们是否遵循规范。

如果报告了违规,则会抛出 ``CookieException``。

验证名称属性
=============================

cookie 名称可以是任何 US-ASCII 字符,以下字符除外:

- 控制字符;
- 空格或制表符;
- 分隔符,例如 ``( ) < > @ , ; : \ " / [ ] ? = { }``

如果将 ``$raw`` 参数设置为 ``true``,则会严格进行此验证。这是因为 PHP 的 `setcookie() <https://www.php.net/manual/en/function.setcookie.php>`_ 和 `setrawcookie() <https://www.php.net/manual/en/function.setrawcookie.php>`_ 会拒绝具有无效名称的 cookie。另外,cookie 名称不能为空字符串。

验证前缀属性
===============================

在使用 ``__Secure-`` 前缀时,必须将 cookie 的 ``$secure`` 标志设置为 ``true``。如果使用 ``__Host-`` 前缀,cookie 必须展示以下特征:

- 将 ``$secure`` 标志设置为 ``true``
- ``$domain`` 为空
- ``$path`` 必须为 ``/``

验证 SameSite 属性
=================================

SameSite 属性只接受三个值:

- **Lax**: 在第三方站点加载图像或框架等正常跨站子请求时不会发送 Cookie,但是在用户导航到源站点时会发送(即点击链接时)。
- **Strict**: Cookie 只会在第一方环境下发送,不会随第三方网站发起的请求一起发送。
- **None**: 在所有环境下发送 Cookie,即对第一方和跨域请求的响应中都会发送。

但是,CodeIgniter 允许你将 SameSite 属性设置为空字符串。提供空字符串时,将使用 ``Cookie`` 类中保存的默认 SameSite 设置。如上所述,你可以使用 ``Cookie::setDefaults()`` 更改默认 SameSite。

最近的 cookie 规范做了更改,要求现代浏览器在未提供时给一个默认的 SameSite。这个默认的是 ``Lax``。如果你已将 SameSite 设置为空字符串,而默认的 SameSite 也为空字符串,你的 cookie 将被赋予 ``Lax`` 值。

如果将 SameSite 设置为 ``None``,你需要确保 ``Secure`` 也设置为 ``true``。

在编写 SameSite 属性时, ``Cookie`` 类以不区分大小写的方式接受任何这些值。你也可以利用类的常量来避免麻烦。

.. literalinclude:: cookies/006.php

***************
发送 Cookie
***************

将 ``Cookie`` 对象设置在 Response 对象的 ``CookieStore`` 中，框架会自动发送 Cookie。

使用 :php:meth:`CodeIgniter\\HTTP\\Response::setCookie()` 来设置：

.. literalinclude:: cookies/017.php

你也可以使用 :php:func:`set_cookie()` 辅助函数：

.. literalinclude:: cookies/018.php

**********************
使用 Cookie 存储
**********************

.. note:: 通常情况下，不需要直接使用 CookieStore。

``CookieStore`` 类表示 ``Cookie`` 对象的一个不可变集合。

从 Response 获取存储
===============================

可以从当前的 ``Response`` 对象访问 ``CookieStore`` 实例。

.. literalinclude:: cookies/007.php

创建 CookieStore
====================

CodeIgniter 提供了另外三种创建 ``CookieStore`` 新实例的方法。

.. literalinclude:: cookies/008.php

.. note:: 在使用全局 :php:func:`cookies()` 函数时,只有在第二个参数 ``$getGlobal`` 设置为 ``false`` 时,才会考虑传递的 ``Cookie`` 数组。

检查存储中的 Cookie
=========================

要检查 ``CookieStore`` 实例中是否存在一个 ``Cookie`` 对象,你可以用几种方法:

.. literalinclude:: cookies/009.php

获取存储中的 Cookie
========================

在 cookie 集合中检索一个 ``Cookie`` 实例非常简单:

.. literalinclude:: cookies/010.php

从 ``CookieStore`` 直接获取 ``Cookie`` 实例时,无效名称会抛出 ``CookieException``。

.. literalinclude:: cookies/011.php

从当前 ``Response`` 的 cookie 集合获取 ``Cookie`` 实例时,无效名称只会返回 ``null``。

.. literalinclude:: cookies/012.php

如果在从 ``Response`` 获取 cookie 时没有提供参数,则会显示存储中的所有 ``Cookie`` 对象。

.. literalinclude:: cookies/013.php

.. note:: 辅助函数 :php:func:`get_cookie()` 从当前的 ``Request`` 对象获取 cookie,而不是从 ``Response`` 获取。如果该 cookie 已设置,此函数会检查 ``$_COOKIE`` 数组并立即获取它。

在存储中添加/删除 Cookie
================================

如前所述, ``CookieStore`` 对象是不可变的。你需要保存修改后的实例才能对其进行操作。原始实例保持不变。

.. literalinclude:: cookies/014.php

.. note:: 从存储中删除 cookie **不会** 从浏览器中删除它。
    如果你打算从浏览器中删除 cookie,你必须向存储放入一个具有相同名称的空值 cookie。

当与当前 ``Response`` 对象中的 cookie 存储进行交互时,你可以安全地添加或删除 cookie,而不用担心 cookie 集合的不可变性质。 ``Response`` 对象将用修改后的实例替换该实例。

.. literalinclude:: cookies/015.php

分派存储中的 Cookie
=============================

.. deprecated:: 4.1.6

.. important:: 该方法已被弃用。将在未来的版本中移除。

更多时候,你不需要自己手动发送 cookie。CodeIgniter 会为你做这件事。但是,如果你真的需要手动发送 cookie,你可以使用 ``dispatch`` 方法。就像发送其他标头一样,你需要确保标头还未发送,方法是检查 ``headers_sent()`` 的值。

.. literalinclude:: cookies/016.php

**********************
Cookie 个性化
**********************

``Cookie`` 类中已经有了一些默认设置,以确保平滑地创建 cookie 对象。但是,你可能希望通过更改 **app/Config/Cookie.php** 文件中的以下 ``Config\Cookie`` 类来定义自己的设置。

==================== ===================================== ========= =====================================================
设置                 选项/类型                             默认值      描述
==================== ===================================== ========= =====================================================
**$prefix**          ``string``                            ``''``    要添加到 cookie 名称前面的前缀。
**$expires**         ``DateTimeInterface|string|int``      ``0``     过期时间戳。
**$path**            ``string``                            ``/``     cookie 的 path 属性。
**$domain**          ``string``                            ``''``    cookie 的 domain 属性,带尾部斜杠。
**$secure**          ``true/false``                        ``false`` 是否通过安全的 HTTPS 发送。
**$httponly**        ``true/false``                        ``true``  是否不可通过 JavaScript 访问。
**$samesite**        ``Lax|None|Strict|lax|none|strict''`` ``Lax``   SameSite 属性。
**$raw**             ``true/false``                        ``false`` 是否使用 ``setrawcookie()`` 进行分派。
==================== ===================================== ========= =====================================================

在运行时,你可以使用 ``Cookie::setDefaults()`` 方法手动提供新的默认值。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Cookie

.. php:class:: Cookie

    .. php:staticmethod:: setDefaults([$config = []])

        :param \\Config\\Cookie|array $config: 配置数组或实例
        :rtype: array<string, mixed>
        :returns: 旧的默认值

        通过从 ``Config\Cookie`` 配置或数组中注入值来设置 Cookie 实例的默认属性。

    .. php:staticmethod:: fromHeaderString(string $header[, bool $raw = false])

        :param string $header: ``Set-Cookie`` 头字符串
        :param bool $raw: 是否不进行 URL 编码并通过 ``setrawcookie()`` 发送
        :rtype: ``Cookie``
        :returns: ``Cookie`` 实例
        :throws: ``CookieException``

        从 ``Set-Cookie`` 头创建一个新的 Cookie 实例。

    .. php:method:: __construct(string $name[, string $value = ''[, array $options = []]])

        :param string $name: cookie 名称
        :param string $value: cookie 值
        :param array $options: cookie 选项
        :rtype: ``Cookie``
        :returns: ``Cookie`` 实例
        :throws: ``CookieException``

        构造一个新的 Cookie 实例。

    .. php:method:: getId()

        :rtype: string
        :returns: 在 cookie 集合中的索引 ID。

    .. php:method:: getPrefix(): string
    .. php:method:: getName(): string
    .. php:method:: getPrefixedName(): string
    .. php:method:: getValue(): string
    .. php:method:: getExpiresTimestamp(): int
    .. php:method:: getExpiresString(): string
    .. php:method:: isExpired(): bool
    .. php:method:: getMaxAge(): int
    .. php:method:: getDomain(): string
    .. php:method:: getPath(): string
    .. php:method:: isSecure(): bool
    .. php:method:: isHTTPOnly(): bool
    .. php:method:: getSameSite(): string
    .. php:method:: isRaw(): bool
    .. php:method:: getOptions(): array

    .. php:method:: withRaw([bool $raw = true])

        :param bool $raw:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个更新了 URL 编码选项的新的 Cookie。

    .. php:method:: withPrefix([string $prefix = ''])

        :param string $prefix:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个带有新前缀的新的 Cookie。

    .. php:method:: withName(string $name)

        :param string $name:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个带有新名称的新的 Cookie。

    .. php:method:: withValue(string $value)

        :param string $value:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个带有新值的新的 Cookie。

    .. php:method:: withExpires($expires)

        :param DateTimeInterface|string|int $expires:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个带有新的 cookie 过期时间的新的 Cookie。

    .. php:method:: withExpired()

        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个从浏览器过期的新的 Cookie。

    .. php:method:: withNeverExpiring()

        .. deprecated:: 4.2.6

        .. important:: 这个方法已弃用。它将在未来的版本中删除。

        :param string $name:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个几乎永不过期的新的 Cookie。

    .. php:method:: withDomain(?string $domain)

        :param string|null $domain:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个带有新域的新的 Cookie。

    .. php:method:: withPath(?string $path)

        :param string|null $path:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个带有新路径的新的 Cookie。

    .. php:method:: withSecure([bool $secure = true])

        :param bool $secure:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个带有新的“Secure”属性的新的 Cookie。

    .. php:method:: withHTTPOnly([bool $httponly = true])

        :param bool $httponly:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个带有新的“HttpOnly”属性的新的 Cookie。

    .. php:method:: withSameSite(string $samesite)

        :param string $samesite:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建一个带有新的“SameSite”属性的新的 Cookie。

    .. php:method:: toHeaderString()

        :rtype: string
        :returns: 可以作为头字符串传递的字符串表示。

    .. php:method:: toArray()

        :rtype: array
        :returns: 返回 Cookie 实例的数组表示形式。

.. php:class:: CookieStore

    .. php:staticmethod:: fromCookieHeaders(array $headers[, bool $raw = false])

        :param array $header: ``Set-Cookie`` 头数组
        :param bool $raw: 是否不使用 URL 编码
        :rtype: ``CookieStore``
        :returns: ``CookieStore`` 实例
        :throws: ``CookieException``

        从 ``Set-Cookie`` 头数组创建一个 CookieStore。

    .. php:method:: __construct(array $cookies)

        :param array $cookies: ``Cookie`` 对象数组
        :rtype: ``CookieStore``
        :returns: ``CookieStore`` 实例
        :throws: ``CookieException``

    .. php:method:: has(string $name[, string $prefix = ''[, ?string $value = null]]): bool

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 前缀
        :param string|null $value: Cookie 值
        :rtype: bool
        :returns: 检查由名称和前缀标识的 ``Cookie`` 对象是否存在于集合中。

    .. php:method:: get(string $name[, string $prefix = '']): Cookie

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 前缀
        :rtype: ``Cookie``
        :returns: 检索由名称和前缀标识的 Cookie 实例。
        :throws: ``CookieException``

    .. php:method:: put(Cookie $cookie): CookieStore

        :param Cookie $cookie: 一个 Cookie 对象
        :rtype: ``CookieStore``
        :returns: 新的 ``CookieStore`` 实例

        存储一个新 cookie 并返回一个新集合。原始集合保持不变。

    .. php:method:: remove(string $name[, string $prefix = '']): CookieStore

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 前缀
        :rtype: ``CookieStore``
        :returns: 新的 ``CookieStore`` 实例

        从集合中删除一个 cookie 并返回更新后的集合。原始集合保持不变。

    .. php:method:: dispatch(): void

        :rtype: void

        分派存储中的所有 cookie。

    .. php:method:: display(): array

        :rtype: array
        :returns: 返回存储中的所有 cookie

    .. php:method:: clear(): void

        :rtype: void

        清除 cookie 集合。
