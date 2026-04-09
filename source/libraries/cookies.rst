#######
Cookie
#######

**HTTP Cookie** （网页 Cookie、浏览器 Cookie）是服务器发送到用户浏览器的一小段数据。浏览器可存储该数据，并在后续向同一服务器发送请求时将其回传。通常用于判断两个请求是否来自同一浏览器，例如保持用户登录状态，为无状态的 HTTP 协议记录状态信息。

Cookie 主要用于三种场景：

- **会话管理**：登录状态、购物车、游戏分数或服务器需要记住的其他信息
- **个性化**：用户偏好、主题和其他设置
- **追踪**：记录和分析用户行为

为高效地向浏览器发送 Cookie，CodeIgniter 提供 ``CodeIgniter\Cookie\Cookie`` 类来抽象 Cookie 交互操作。

.. contents::
    :local:
    :depth: 2

****************
创建 Cookie
****************

目前可通过四种方式创建新的 ``Cookie`` 值对象。

.. literalinclude:: cookies/001.php

构造 ``Cookie`` 对象时，仅需 ``name`` 属性，其余均为可选。若未修改可选属性，将使用 ``Cookie`` 类中保存的默认值。

覆盖默认值
===================

要覆盖类中当前存储的默认值，可向静态方法 ``Cookie::setDefaults()`` 传入 ``Config\Cookie`` 实例或包含默认值的数组。

.. literalinclude:: cookies/002.php

向 ``Cookie::setDefaults()`` 传入 ``Config\Cookie`` 实例或数组会覆盖当前默认值，并在传入新默认值前一直生效。

临时更改默认值
------------------------------------

若不希望此行为生效，仅需临时更改默认值，可利用 ``Cookie::setDefaults()`` 返回旧默认值数组的特性。

.. literalinclude:: cookies/003.php

*****************************
访问 Cookie 属性
*****************************

实例化后，可通过 getter 方法轻松访问 ``Cookie`` 的属性。

.. literalinclude:: cookies/004.php

*****************
不可变 Cookie
*****************

新的 ``Cookie`` 实例是 HTTP Cookie 的不可变值对象表示。因其不可变性，修改实例的任意属性不会影响原实例，修改操作 **始终** 返回新实例，需保留该新实例才能使用。

.. literalinclude:: cookies/005.php

********************************
验证 Cookie 属性
********************************

HTTP Cookie 受多项规范约束，必须遵守才能被浏览器接受。因此创建或修改 ``Cookie`` 的某些属性时，会进行验证以确保符合规范。

若存在违规情况，将抛出 ``CookieException`` 异常。

验证 Name 属性
=============================

Cookie 名称可使用任意 US-ASCII 字符，但以下字符除外：

- 控制字符
- 空格或制表符
- 分隔符，如 ``( ) < > @ , ; : \ " / [ ] ? = { }``

若将 ``$raw`` 参数设为 ``true``，验证将更为严格。因为 PHP 的 `setcookie() <https://www.php.net/manual/zh/function.setcookie.php>`_ 和 `setrawcookie() <https://www.php.net/manual/zh/function.setrawcookie.php>`_ 会拒绝名称无效的 Cookie。此外，Cookie 名称不能为空字符串。

验证 Prefix 属性
===============================

使用 ``__Secure-`` 前缀时，Cookie 必须设置 ``$secure`` 标志为 ``true``。若使用 ``__Host-`` 前缀，Cookie 必须满足以下条件：

- ``$secure`` 标志设为 ``true``
- ``$domain`` 为空
- ``$path`` 必须为 ``/``

验证 SameSite 属性
=================================

SameSite 属性接受三个值：

- **Lax**：常规跨站点子请求（如向第三方网站加载图片或框架）不发送 Cookie，但用户导航到源站点时（如点击链接）会发送。
- **Strict**：Cookie 仅在第一方上下文中发送，不会随第三方网站发起的请求一起发送。
- **None**：Cookie 在所有上下文中发送，即响应第一方和跨源请求时均会发送。

CodeIgniter 允许将 SameSite 属性设为空字符串。传入空字符串时，将使用 ``Cookie`` 类中保存的默认 SameSite 设置。可通过上述 ``Cookie::setDefaults()`` 方法更改默认 SameSite 设置。

近期 Cookie 规范已变更，现代浏览器若未提供 SameSite 值，则默认使用 ``Lax``。若将 SameSite 设为空字符串且默认 SameSite 也为空字符串，Cookie 将被赋予 ``Lax`` 值。

若 SameSite 设为 ``None``，需确保 ``Secure`` 也设为 ``true``。

写入 SameSite 属性时，``Cookie`` 类不区分大小写地接受以上任一值。也可使用类常量简化操作。

.. literalinclude:: cookies/006.php

***************
发送 Cookie
***************

在 Response 对象的 ``CookieStore`` 中设置 ``Cookie`` 对象，框架会自动发送这些 Cookie。

使用 :php:meth:`CodeIgniter\\HTTP\\Response::setCookie()` 进行设置：

.. literalinclude:: cookies/017.php

也可使用 :php:func:`set_cookie()` 辅助函数：

.. literalinclude:: cookies/018.php

**********************
使用 Cookie Store
**********************

.. note:: 通常无需直接使用 CookieStore。

``CookieStore`` 类表示 ``Cookie`` 对象的不可变集合。

从 Response 获取 Store
===============================

可从当前 ``Response`` 对象访问 ``CookieStore`` 实例。

.. literalinclude:: cookies/007.php

创建 CookieStore
====================

CodeIgniter 提供另外三种方式创建 ``CookieStore`` 新实例。

.. literalinclude:: cookies/008.php

.. note:: 使用全局 :php:func:`cookies()` 函数时，仅当第二个参数 ``$getGlobal`` 设为 ``false`` 时才会使用传入的 ``Cookie`` 数组。

检查 Store 中的 Cookie
=========================

检查 ``CookieStore`` 实例中是否存在 ``Cookie`` 对象，可使用以下方式：

.. literalinclude:: cookies/009.php

获取 Store 中的 Cookie
========================

从 Cookie 集合中获取 ``Cookie`` 实例非常简单：

.. literalinclude:: cookies/010.php

直接从 ``CookieStore`` 获取 ``Cookie`` 实例时，无效名称将抛出 ``CookieException`` 异常。

.. literalinclude:: cookies/011.php

从当前 ``Response`` 的 Cookie 集合获取 ``Cookie`` 实例时，无效名称仅返回 ``null``。

.. literalinclude:: cookies/012.php

从 ``Response`` 获取 Cookie 时若未提供参数，将显示 Store 中的所有 ``Cookie`` 对象。

.. literalinclude:: cookies/013.php

.. note:: 辅助函数 :php:func:`get_cookie()` 从当前 ``Request`` 对象而非 ``Response`` 获取 Cookie。该函数检查 ``$_COOKIE`` 数组中是否设置了该 Cookie 并立即获取。

在 Store 中添加/移除 Cookie
================================

如前所述，``CookieStore`` 对象不可变。需保存修改后的实例才能继续操作，原实例保持不变。

.. literalinclude:: cookies/014.php

.. note:: 从 Store 移除 Cookie **不会** 从浏览器中删除。若要从浏览器删除 Cookie，必须将同名空值 Cookie 放入 Store。

与当前 ``Response`` 对象中的 Store Cookie 交互时，可安全地添加或删除 Cookie，无需担心 Cookie 集合的不可变性。``Response`` 对象会用修改后的实例替换原实例。

.. literalinclude:: cookies/015.php

发送 Store 中的 Cookie
============================

.. important:: 此方法自 4.1.6 版本起已弃用，并在 4.6.0 版本中移除。

通常无需手动发送 Cookie，CodeIgniter 会自动处理。但若确实需要手动发送，可使用 ``dispatch`` 方法。与发送其他标头一样，需先通过 ``headers_sent()`` 检查标头是否尚未发送。

.. literalinclude:: cookies/016.php

**********************
Cookie 个性化设置
**********************

``Cookie`` 类内置合理的默认值，确保 Cookie 对象创建顺畅。但可通过修改 **app/Config/Cookie.php** 文件中的 ``Config\Cookie`` 类来定义自定义设置。

==================== ===================================== ========= =====================================================
设置                 选项/类型                             默认值    描述
==================== ===================================== ========= =====================================================
**$prefix**          ``string``                            ``''``    添加到 Cookie 名称的前缀。
**$expires**         ``DateTimeInterface|string|int``      ``0``     过期时间戳。
**$path**            ``string``                            ``/``     Cookie 的路径属性。
**$domain**          ``string``                            ``''``    Cookie 的域名属性（可带尾部斜杠）。
**$secure**          ``true``/``false``                    ``false`` 是否仅通过 HTTPS 发送。
**$httponly**        ``true``/``false``                    ``true``  是否对 JavaScript 不可访问。
**$samesite**        ``Lax``/``None``/``Strict``           ``Lax``   SameSite 属性。
**$raw**             ``true``/``false``                    ``false`` 是否使用 ``setrawcookie()`` 发送。
==================== ===================================== ========= =====================================================

运行时可使用 ``Cookie::setDefaults()`` 方法手动提供新的默认值。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Cookie

.. php:class:: Cookie

    .. php:staticmethod:: setDefaults([$config = []])

        :param \\Config\\Cookie|array $config: 配置数组或实例
        :rtype: array<string, mixed>
        :returns: 旧的默认值

        通过注入 ``Config\Cookie`` 配置或数组的值，为 Cookie 实例设置默认属性。

    .. php:staticmethod:: fromHeaderString(string $header[, bool $raw = false])

        :param string $header: ``Set-Cookie`` 标头字符串
        :param bool $raw: 是否不对 Cookie 进行 URL 编码并通过 ``setrawcookie()`` 发送
        :rtype: ``Cookie``
        :returns: ``Cookie`` 实例
        :throws: ``CookieException``

        从 ``Set-Cookie`` 标头创建新的 Cookie 实例。

    .. php:method:: __construct(string $name[, string $value = ''[, array $options = []]])

        :param string $name: Cookie 名称
        :param string $value: Cookie 值
        :param array $options: Cookie 选项
        :rtype: ``Cookie``
        :returns: ``Cookie`` 实例
        :throws: ``CookieException``

        构造新的 Cookie 实例。

    .. php:method:: getId()

        :rtype: string
        :returns: Cookie 集合中索引使用的 ID。

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

        创建带有更新 URL 编码选项的新 Cookie。

    .. php:method:: withPrefix([string $prefix = ''])

        :param string $prefix:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建带有新前缀的新 Cookie。

    .. php:method:: withName(string $name)

        :param string $name:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建带有新名称的新 Cookie。

    .. php:method:: withValue(string $value)

        :param string $value:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建带有新值的新 Cookie。

    .. php:method:: withExpires($expires)

        :param DateTimeInterface|string|int $expires:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建带有新过期时间的新 Cookie。

    .. php:method:: withExpired()

        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建将从浏览器中过期的新 Cookie。

    .. php:method:: withNeverExpiring()

        .. important:: 此方法自 4.2.6 版本起已弃用，并在 4.6.0 版本中移除。

        :param string $name:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建几乎永不过期的新 Cookie。

    .. php:method:: withDomain(?string $domain)

        :param string|null $domain:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建带有新域名的新 Cookie。

    .. php:method:: withPath(?string $path)

        :param string|null $path:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建带有新路径的新 Cookie。

    .. php:method:: withSecure([bool $secure = true])

        :param bool $secure:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建带有新 "Secure" 属性的新 Cookie。

    .. php:method:: withHTTPOnly([bool $httponly = true])

        :param bool $httponly:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建带有新 "HttpOnly" 属性的新 Cookie。

    .. php:method:: withSameSite(string $samesite)

        :param string $samesite:
        :rtype: ``Cookie``
        :returns: 新的 ``Cookie`` 实例

        创建带有新 "SameSite" 属性的新 Cookie。

    .. php:method:: toHeaderString()

        :rtype: string
        :returns: 返回可作为标头字符串传递的字符串表示。

    .. php:method:: toArray()

        :rtype: array
        :returns: 返回 Cookie 实例的数组表示。

.. php:class:: CookieStore

    .. php:staticmethod:: fromCookieHeaders(array $headers[, bool $raw = false])

        :param array $header: ``Set-Cookie`` 标头数组
        :param bool $raw: 是否不使用 URL 编码
        :rtype: ``CookieStore``
        :returns: ``CookieStore`` 实例
        :throws: ``CookieException``

        从 ``Set-Cookie`` 标头数组创建 CookieStore。

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
        :returns: 检查集合中是否存在由名称和前缀标识的 ``Cookie`` 对象。

    .. php:method:: get(string $name[, string $prefix = '']): Cookie

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 前缀
        :rtype: ``Cookie``
        :returns: 按名称和前缀检索 Cookie 实例。
        :throws: ``CookieException``

    .. php:method:: put(Cookie $cookie): CookieStore

        :param Cookie $cookie: Cookie 对象
        :rtype: ``CookieStore``
        :returns: 新的 ``CookieStore`` 实例

        存储新 Cookie 并返回新集合，原集合保持不变。

    .. php:method:: remove(string $name[, string $prefix = '']): CookieStore

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 前缀
        :rtype: ``CookieStore``
        :returns: 新的 ``CookieStore`` 实例

        从集合中移除 Cookie 并返回更新后的集合，原集合保持不变。

    .. php:method:: dispatch(): void

        .. important:: 此方法自 4.1.6 版本起已弃用，并在 4.6.0 版本中移除。

        :rtype: void

        发送 Store 中的所有 Cookie。

    .. php:method:: display(): array

        :rtype: array
        :returns: 返回 Store 中的所有 Cookie 实例。

    .. php:method:: clear(): void

        :rtype: void

        清空 Cookie 集合。
