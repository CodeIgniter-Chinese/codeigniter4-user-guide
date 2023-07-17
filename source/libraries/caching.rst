##############
缓存驱动
##############

CodeIgniter 提供了一些最常用的快速动态缓存的封装。除基于文件的缓存外,所有缓存都需要特定的服务器要求,如果服务器要求不符,会抛出一个致命异常。

.. contents::
    :local:
    :depth: 2

*************
使用示例
*************

下面的示例展示了在控制器中的一种常见用法:

.. literalinclude:: caching/001.php

你可以通过 Services 类直接获取缓存引擎的一个实例:

.. literalinclude:: caching/002.php

*********************
配置缓存
*********************

缓存引擎的所有配置都在 **app/Config/Cache.php** 中。该文件中可用的选项如下:

$handler
========

这是启动缓存引擎时使用的主处理程序的名称。可用名称有:dummy、file、memcached、redis、predis、wincache。

$backupHandler
==============

如果首选的 ``$handler`` 不可用,则此处是要加载的下一个缓存处理程序。由于文件系统总是可用的,因此这通常是 ``File`` 处理程序,但可能不适合更复杂的多服务器设置。

$prefix
=======

如果你有多个应用程序使用相同的缓存存储,你可以在这里添加一个自定义的前缀字符串,该字符串会添加到所有键名的前面。

$ttl
====

没有指定时保存项目的默认秒数。

.. warning:: 这在框架处理程序中没有使用,因为有 60 秒的硬编码值,但对项目和模块可能有用。这会在未来的版本中替换硬编码值。

$file
=====

这是一组针对 ``File`` 处理程序的设置数组,用来确定其应如何保存缓存文件。

$memcached
==========

这是在使用 ``Memcache(d)`` 处理程序时要使用的一组服务器数组。

$redis
======

使用 ``Redis`` 和 ``Predis`` 处理程序时,希望使用的 Redis 服务器的设置。

******************
命令行工具
******************

CodeIgniter 提供了几个可以从命令行使用的 :doc:`commands </cli/spark_commands>`,以帮助你使用缓存。
这些工具不是使用缓存驱动所必需的,但可能对你有帮助。

cache:clear
===========

清除当前系统缓存::

    > php spark cache:clear

cache:info
==========

显示当前系统中的文件缓存信息::

    > php spark cache:info

.. note:: 这个命令只支持 File 缓存处理程序。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Cache

.. php:class:: CacheInterface

    .. php:method:: isSupported()

        :returns: 如果支持则为 ``true``,不支持则为 ``false``
        :rtype: bool

    .. php:method:: get($key): mixed

        :param string $key: 缓存项名称
        :returns: 项的值,如果没找到则为 ``null``
        :rtype: mixed

        这个方法将尝试从缓存中获取一个项。如果该项不存在,该方法将返回 null。

        例如:

        .. literalinclude:: caching/003.php

    .. php:method:: remember(string $key, int $ttl, Closure $callback)

        :param string $key: 缓存项名称
        :param int $ttl: 生存时间,以秒为单位
        :param Closure $callback: 当缓存项返回 null 时要调用的回调
        :returns: 缓存项的值
        :rtype: mixed

        从缓存中获取一个项。如果返回 ``null``,则调用回调并保存结果。无论哪种方式,都会返回该值。

    .. php:method:: save(string $key, $data[, int $ttl = 60[, $raw = false]])

        :param string $key: 缓存项名称
        :param mixed $data: 要保存的数据
        :param int $ttl: 生存时间,以秒为单位,默认 60
        :param bool $raw: 是否保存原始值
        :returns: 保存成功则为 ``true``,失败则为 ``false``
        :rtype: bool

        这个方法将一个项保存到缓存存储中。如果保存失败,该方法将返回 ``false``。

        例如:

        .. literalinclude:: caching/004.php

        .. note:: ``$raw`` 参数仅由 Memcache 使用,以允许使用 ``increment()`` 和 ``decrement()``。

    .. php:method:: delete($key): bool

        :param string $key: 缓存项名称
        :returns: 删除成功则为 ``true``,失败则为 ``false``
        :rtype: bool

        这个方法将从缓存中删除一个特定的项。如果删除失败,该方法将返回 false。

        例如:

        .. literalinclude:: caching/005.php

    .. php:method:: deleteMatching($pattern): integer

        :param string $pattern: 要匹配缓存项键的 glob 样式模式
        :returns: 已删除项的数量
        :rtype: integer

        这个方法将一次性从缓存中删除多个项,方法是通过 glob 样式模式匹配它们的键。它将返回已删除项的总数。

        .. important:: 这个方法只在 File、Redis 和 Predis 处理程序中实现。由于局限,在 Memcached 和 Wincache 处理程序中无法实现。

        例如:

        .. literalinclude:: caching/006.php

        关于 glob 样式语法的更多信息,请查看
        `Glob (programming) <https://en.wikipedia.org/wiki/Glob_(programming)#Syntax>`_。

    .. php:method:: increment($key[, $offset = 1]): mixed

        :param string $key: 缓存 ID
        :param int $offset: 要添加的步长/值
        :returns: 成功则返回新值,失败则返回 ``false``
        :rtype: mixed

        对一个原始存储的值执行原子增量操作。

        例如:

        .. literalinclude:: caching/007.php

    .. php:method:: decrement($key[, $offset = 1]): mixed

        :param string $key: 缓存 ID
        :param int $offset: 要减少的步长/值
        :returns: 成功则返回新值,失败则返回 ``false``
        :rtype: mixed

        对一个原始存储的值执行原子减量操作。

        例如:

        .. literalinclude:: caching/008.php

    .. php:method:: clean()

        :returns: 清除成功则为 ``true``,失败则为 ``false``
        :rtype: bool

        这个方法将‘清空’整个缓存。如果缓存文件的删除失败,该方法将返回 false。

        例如:

        .. literalinclude:: caching/009.php

    .. php:method:: getCacheInfo()

        :returns: 整个缓存数据库的信息
        :rtype: mixed

        这个方法将返回整个缓存的信息。

        例如:

        .. literalinclude:: caching/010.php

        .. note:: 返回的信息及数据结构取决于所使用的适配器。

    .. php:method:: getMetadata(string $key)

        :param string $key: 缓存项名称
        :returns: 缓存项的元数据。缺少项时为 ``null``,如果绝对到期时间是永不过期,则至少应包含 "expire" 键的数组。
        :rtype: array|null

        这个方法将返回缓存中特定项的详细信息。

        例如:

        .. literalinclude:: caching/011.php

        .. note:: 返回的信息和数据结构取决于所使用的适配器。一些适配器(File、Memcached、Wincache)对缺失的项仍然返回 ``false``。

    .. php:staticmethod:: validateKey(string $key, string $prefix)

        :param string $key: 潜在的缓存键
        :param string $prefix: 可选的前缀
        :returns: 验证和加前缀后的键。如果键超过了驱动的最大键长度,它将被哈希。
        :rtype: string

        这个方法由处理程序方法用来检查键是否有效。它会对非字符串、无效字符和空长度抛出 ``InvalidArgumentException``。

        例如:

        .. literalinclude:: caching/012.php

*******
驱动程序
*******

基于文件的缓存
==================

与来自 Output 类的缓存不同,基于文件的驱动缓存允许缓存视图文件的一部分。谨慎使用此功能,并确保对应用进行基准测试,因为在某个点上,磁盘 I/O 将抵消缓存的积极效果。这需要一个真正可写的缓存目录。

Memcached 缓存
=================

可以在缓存配置文件中指定 Memcached 服务器。可用选项如下:

.. literalinclude:: caching/013.php

有关 Memcached 的更多信息,请查看
`https://www.php.net/memcached <https://www.php.net/memcached>`_。

WinCache 缓存
================

在 Windows 下,你也可以使用 WinCache 驱动程序。

有关 WinCache 的更多信息,请查看
`https://www.php.net/wincache <https://www.php.net/wincache>`_。

Redis 缓存
=============

Redis 是一个内存中的键值存储,可以以 LRU 缓存模式运行。要使用它,你需要 `Redis server 和 phpredis PHP 扩展 <https://github.com/phpredis/phpredis>`_。

连接到 redis 服务器的配置选项存储在缓存配置文件中。可用选项如下:

.. literalinclude:: caching/014.php

有关 Redis 的更多信息,请查看
`https://redis.io <https://redis.io>`_。

Predis 缓存
==============

Predis 是一个用于 Redis 键值存储的灵活且功能完善的 PHP 客户端库。要使用它,从项目根目录的命令行中运行::

    > composer require predis/predis

有关 Redis 的更多信息,请查看
`https://github.com/nrk/predis <https://github.com/nrk/predis>`_。

Dummy 缓存
===========

这是一个缓存后端,将始终“未命中”。它不存储任何数据,但允许你在不支持你选择的缓存的环境中保持缓存代码。
