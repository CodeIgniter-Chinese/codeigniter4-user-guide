#######
Cookie
#######

**HTTP Cookie** （网页 Cookie、浏览器 Cookie）是服务器发送到用户浏览器的一小段数据。浏览器会存储该数据并在后续向同一服务器发起请求时将其带回。通常用于判断两个请求是否来自同一浏览器——例如保持用户登录状态。它为无状态的 HTTP 协议提供了状态信息记忆能力。

Cookies 主要用于以下三个场景：

- **会话管理**：登录状态、购物车、游戏分数等需要服务器记忆的信息
- **个性化设置**：用户偏好、主题及其他配置
- **行为追踪**：记录和分析用户行为

为帮助你高效地向浏览器发送 Cookies，CodeIgniter 提供了 ``CodeIgniter\Cookie\Cookie`` 类来抽象化 Cookie 交互。

.. contents::
    :local:
    :depth: 2

****************
创建 Cookie
****************

目前有四种方式创建新的 ``Cookie`` 值对象：

.. literalinclude:: cookies/001.php

构建 ``Cookie`` 对象时，仅 ``name`` 属性为必填项，其他属性均为可选。若未修改可选属性，它们的值将由 ``Cookie`` 类中保存的默认值填充。

覆盖默认值
===================

要覆盖类中存储的默认值，可以通过静态方法 ``Cookie::setDefaults()`` 传入 ``Config\Cookie`` 实例或包含默认值的数组：

.. literalinclude:: cookies/002.php

向 ``Cookie::setDefaults()`` 传递 ``Config\Cookie`` 实例或数组将永久覆盖默认值，直到传入新的默认值为止。

临时修改默认值
------------------------------------

若希望临时修改默认值而非永久覆盖，可利用 ``Cookie::setDefaults()`` 返回旧默认值数组的特性：

.. literalinclude:: cookies/003.php

*****************************
访问 Cookie 属性
*****************************

实例化后，可通过 getter 方法轻松访问 ``Cookie`` 属性：

.. literalinclude:: cookies/004.php

*****************
不可变 Cookie
*****************

``Cookie`` 实例是 HTTP Cookie 的不可变值对象。由于其不可变性，修改实例属性不会影响原实例，修改操作 **始终** 返回新实例。需保留新实例方可使用：

.. literalinclude:: cookies/005.php

********************************
验证 Cookie 属性
********************************

HTTP Cookie 受多个规范约束以确保浏览器接受。因此在创建或修改 ``Cookie`` 的某些属性时，会进行规范符合性验证。若验证失败将抛出 ``CookieException``。

验证名称属性
=============================

Cookie 名称可为任意 US-ASCII 字符，但以下字符除外：

- 控制字符
- 空格或制表符
- 分隔字符：``( ) < > @ , ; : \ " / [ ] ? = { }``

若设置 ``$raw`` 参数为 ``true`` 将执行严格验证，因为 PHP 的 `setcookie() <https://www.php.net/manual/zh/function.setcookie.php>`_ 和 `setrawcookie() <https://www.php.net/manual/zh/function.setrawcookie.php>`_ 会拒绝无效名称。此外，名称不能为空字符串。

验证前缀属性
===============================

使用 ``__Secure-`` 前缀时，必须设置 ``$secure`` 标志为 ``true``。使用 ``__Host-`` 前缀时需满足：

- ``$secure`` 标志设为 ``true``
- ``$domain`` 为空
- ``$path`` 必须为 ``/``

验证 SameSite 属性
=================================

SameSite 属性接受三个值：

- **Lax** （宽松模式）：跨站子请求（如图片加载）不发送 Cookie，但导航到源站时（如点击链接）会发送
- **Strict** （严格模式）：仅在第一方上下文中发送 Cookie
- **None** （无限制）：所有上下文中均发送 Cookie

CodeIgniter 允许将 SameSite 设为空字符串，此时使用 ``Cookie`` 类保存的默认值。可通过上文所述的 ``Cookie::setDefaults()`` 修改默认值。

现代浏览器规范要求未指定 SameSite 时默认使用 ``Lax``。若 SameSite 设为空字符串且默认值也为空，则 Cookie 将被赋予 ``Lax`` 值。

当设置 SameSite 为 ``None`` 时，必须同时设置 ``Secure`` 为 ``true``。

``Cookie`` 类接受不区分大小写的 SameSite 值，也可使用类常量简化操作：

.. literalinclude:: cookies/006.php

***************
发送 Cookie
***************

将 ``Cookie`` 对象存入 Response 对象的 ``CookieStore`` 中，框架会自动发送 Cookie。

使用 :php:meth:`CodeIgniter\\HTTP\\Response::setCookie()` 设置：

.. literalinclude:: cookies/017.php

也可使用 :php:func:`set_cookie()` 辅助函数：

.. literalinclude:: cookies/018.php

**********************
使用 Cookie 存储库
**********************

.. note:: 通常无需直接操作 CookieStore。

``CookieStore`` 类表示 ``Cookie`` 对象的不可变集合。

从 Response 获取存储库
===============================

可通过当前 ``Response`` 对象访问 ``CookieStore`` 实例：

.. literalinclude:: cookies/007.php

创建 CookieStore
====================

CodeIgniter 提供三种方式创建新 ``CookieStore`` 实例：

.. literalinclude:: cookies/008.php

.. note:: 使用全局函数 :php:func:`cookies()` 时，仅当第二个参数 ``$getGlobal`` 设为 ``false`` 时才会考虑传入的 ``Cookie`` 数组。

检查存储库中的 Cookie
=========================

可通过多种方式检查 ``CookieStore`` 实例中是否存在某 ``Cookie`` 对象：

.. literalinclude:: cookies/009.php

获取存储库中的 Cookie
========================

从 Cookie 集合中检索 ``Cookie`` 实例非常简单：

.. literalinclude:: cookies/010.php

直接从 ``CookieStore`` 获取实例时，无效名称会抛出 ``CookieException``：

.. literalinclude:: cookies/011.php

从当前 ``Response`` 的 Cookie 集合获取时，无效名称返回 ``null``：

.. literalinclude:: cookies/012.php

若从 ``Response`` 获取时不带参数，将显示存储库中所有 ``Cookie`` 对象：

.. literalinclude:: cookies/013.php

.. note:: 辅助函数 :php:func:`get_cookie()` 从当前 ``Request`` 对象而非 ``Response`` 获取 Cookie。该函数检查 ``$_COOKIE`` 数组并直接获取。

添加/删除存储库中的 Cookie
================================

如前所述，``CookieStore`` 对象不可变。需保存修改后的实例才能生效，原实例保持不变：

.. literalinclude:: cookies/014.php

.. note:: 从存储库删除 Cookie **不会** 从浏览器删除。若要从浏览器删除 Cookie，必须向存储库添加同名空值 Cookie。

与当前 ``Response`` 对象中的 Cookies 交互时，可安全添加/删除 Cookies，无需担心集合的不可变性。``Response`` 对象会自动替换为修改后的实例：

.. literalinclude:: cookies/015.php

分发存储库中的 Cookie
=============================

.. important:: 该方法在 4.1.6 版本弃用，4.6.0 版本移除。

通常无需手动发送 Cookie，CodeIgniter 会自动处理。如需手动发送，可使用 ``dispatch`` 方法。需通过 ``headers_sent()`` 检查确保标头未发送：

.. literalinclude:: cookies/016.php

**********************
Cookie 个性化配置
**********************

``Cookie`` 类已预设合理默认值以确保正常创建。可通过修改 **app/Config/Cookie.php** 中的 ``Config\Cookie`` 类配置项来自定义：

==================== ===================================== ========= =====================================================
设置项               选项/类型                             默认值    描述
==================== ===================================== ========= =====================================================
**$prefix**          ``string``                            ``''``    Cookie 名前缀
**$expires**         ``DateTimeInterface|string|int``      ``0``     过期时间戳
**$path**            ``string``                            ``/``     Cookie 路径属性
**$domain**          ``string``                            ``''``    Cookie 域名属性（带尾部斜线）
**$secure**          ``true``/``false``                    ``false`` 是否仅通过 HTTPS 发送
**$httponly**        ``true``/``false``                    ``true``  是否禁止 JavaScript 访问
**$samesite**        ``Lax``/``None``/``Strict``           ``Lax``   SameSite 属性
**$raw**             ``true``/``false``                    ``false`` 是否使用 ``setrawcookie()`` 发送
==================== ===================================== ========= =====================================================

运行时可通过 ``Cookie::setDefaults()`` 方法手动设置新默认值。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Cookie

.. php:class:: Cookie

    .. php:staticmethod:: setDefaults([$config = []])

        :param \\Config\\Cookie|array $config: 配置数组或实例
        :rtype: array<string, mixed>
        :returns: 旧默认值数组

        通过注入 ``Config\Cookie`` 配置或数组来设置 Cookie 实例的默认属性。

    .. php:staticmethod:: fromHeaderString(string $header[, bool $raw = false])

        :param string $header: ``Set-Cookie`` 标头字符串
        :param bool $raw: 是否使用原始 Cookie
        :rtype: ``Cookie``
        :returns: ``Cookie`` 实例
        :throws: ``CookieException``

        从 ``Set-Cookie`` 标头创建新 Cookie 实例。

    .. php:method:: __construct(string $name[, string $value = ''[, array $options = []]])

        :param string $name: Cookie 名称
        :param string $value: Cookie 值
        :param array $options: Cookie 选项
        :rtype: ``Cookie``
        :returns: ``Cookie`` 实例
        :throws: ``CookieException``

        构造新 Cookie 实例。

    .. php:method:: getId()

        :rtype: string
        :returns: 用于 Cookie 集合索引的 ID

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
        :returns: 新 ``Cookie`` 实例

        创建带更新 URL 编码选项的新 Cookie。

    .. php:method:: withPrefix([string $prefix = ''])

        :param string $prefix:
        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建带新前缀的 Cookie。

    .. php:method:: withName(string $name)

        :param string $name:
        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建带新名称的 Cookie。

    .. php:method:: withValue(string $value)

        :param string $value:
        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建带新值的 Cookie。

    .. php:method:: withExpires($expires)

        :param DateTimeInterface|string|int $expires:
        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建带新过期时间的 Cookie。

    .. php:method:: withExpired()

        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建即将过期的 Cookie。

    .. php:method:: withNeverExpiring()

        .. important:: 该方法在 4.2.6 版本弃用，4.6.0 版本移除。

        :param string $name:
        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建永不过期的 Cookie（已移除）。

    .. php:method:: withDomain(?string $domain)

        :param string|null $domain:
        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建带新域名的 Cookie。

    .. php:method:: withPath(?string $path)

        :param string|null $path:
        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建带新路径的 Cookie。

    .. php:method:: withSecure([bool $secure = true])

        :param bool $secure:
        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建带新 "Secure" 属性的 Cookie。

    .. php:method:: withHTTPOnly([bool $httponly = true])

        :param bool $httponly:
        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建带新 "HttpOnly" 属性的 Cookie。

    .. php:method:: withSameSite(string $samesite)

        :param string $samesite:
        :rtype: ``Cookie``
        :returns: 新 ``Cookie`` 实例

        创建带新 "SameSite" 属性的 Cookie。

    .. php:method:: toHeaderString()

        :rtype: string
        :returns: 可作为标头字符串传递的字符串表示

    .. php:method:: toArray()

        :rtype: array
        :returns: Cookie 实例的数组表示

.. php:class:: CookieStore

    .. php:staticmethod:: fromCookieHeaders(array $headers[, bool $raw = false])

        :param array $header: ``Set-Cookie`` 标头数组
        :param bool $raw: 是否使用原始 Cookie
        :rtype: ``CookieStore``
        :returns: ``CookieStore`` 实例
        :throws: ``CookieException``

        从 ``Set-Cookie`` 标头数组创建 CookieStore。

    .. php:method:: __construct(array $cookies)

        :param array $cookies: Cookie 对象数组
        :rtype: ``CookieStore``
        :returns: ``CookieStore`` 实例
        :throws: ``CookieException``

    .. php:method:: has(string $name[, string $prefix = ''[, ?string $value = null]]): bool

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 前缀
        :param string|null $value: Cookie 值
        :rtype: bool
        :returns: 检查指定名称和前缀的 Cookie 是否存在

    .. php:method:: get(string $name[, string $prefix = '']): Cookie

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 前缀
        :rtype: ``Cookie``
        :returns: 获取指定名称和前缀的 Cookie 实例
        :throws: ``CookieException``

    .. php:method:: put(Cookie $cookie): CookieStore

        :param Cookie $cookie: Cookie 对象
        :rtype: ``CookieStore``
        :returns: 新 ``CookieStore`` 实例

        存储新 Cookie 并返回新集合，原集合保持不变。

    .. php:method:: remove(string $name[, string $prefix = '']): CookieStore

        :param string $name: Cookie 名称
        :param string $prefix: Cookie 前缀
        :rtype: ``CookieStore``
        :returns: 新 ``CookieStore`` 实例

        移除 Cookie 并返回新集合，原集合保持不变。

    .. php:method:: dispatch(): void

        .. important:: 该方法在 4.1.6 版本弃用，4.6.0 版本移除。

        :rtype: void

        分发存储库中所有 Cookies（已移除）。

    .. php:method:: display(): array

        :rtype: array
        :returns: 返回存储中的所有 Ccookie

    .. php:method:: clear(): void

        :rtype: void

        清除 Cookie 集合。
