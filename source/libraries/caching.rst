##############
缓存驱动
##############

CodeIgniter 封装了多种流行的快速动态缓存方式。除基于文件的缓存外，其他缓存方式都需要特定的服务器环境支持，若服务器环境不满足要求，将抛出致命异常。

.. contents::
    :local:
    :depth: 2

*************
使用示例
*************

以下示例展示在控制器中的常见用法。

.. literalinclude:: caching/001.php

可通过全局函数 ``service()`` 直接获取缓存引擎实例：

.. literalinclude:: caching/002.php

.. _libraries-caching-configuring-the-cache:

*********************
配置缓存
*********************

缓存引擎的所有配置均在 **app/Config/Cache.php** 文件中完成。该文件包含以下配置项：

$handler
========

指定启动缓存引擎时使用的首要处理器名称。
可用名称包括：dummy、file、memcached、redis、predis、wincache。

$backupHandler
==============

当首选 ``$handler`` 不可用时，将加载此备用缓存处理器。
通常使用 ``File`` 处理器，因为文件系统始终可用，但在复杂的多服务器环境中可能不适用。

$prefix
=======

当多个应用共用同一缓存存储时，可在此处添加自定义前缀字符串，该前缀将添加到所有键名之前。

$ttl
====

未指定保存时间时的默认秒数。

警告：框架处理器未使用此配置（硬编码为 60 秒），但可能对项目和模块有用。未来版本将替换该硬编码值。

$file
=====

专用于 **File** 处理器的设置数组，用于确定缓存文件的保存方式。

$memcached
==========

使用 **Memcached** 处理器时的服务器数组。

$redis
======

使用 **Redis** 和 **Predis** 处理器时的 Redis 服务器设置。

******************
命令行工具
******************

CodeIgniter 内置多个 :doc:`命令 </cli/spark_commands>`，可从命令行辅助使用缓存。
这些工具不是使用缓存驱动的必需组件，但可能有所帮助。

cache:clear
===========

清除当前系统缓存：

.. code-block:: console

    php spark cache:clear

cache:info
==========

显示当前系统的文件缓存信息：

.. code-block:: console

    php spark cache:info

.. note:: 此命令仅支持 File 缓存处理器。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Cache

.. php:class:: CacheInterface

    .. php:method:: isSupported()

        :returns: 支持返回 ``true``，不支持返回 ``false``
        :rtype: bool

    .. php:method:: get($key): mixed

        :param string $key: 缓存项名称
        :returns: 项值，未找到返回 ``null``
        :rtype: mixed

        尝试从缓存存储中获取项。若项不存在，返回 null。

        示例：

        .. literalinclude:: caching/003.php

    .. php:method:: remember(string $key, int $ttl, Closure $callback)

        :param string $key: 缓存项名称
        :param int $ttl: 存活时间（秒）
        :param Closure $callback: 缓存项返回 null 时调用的回调
        :returns: 缓存项的值
        :rtype: mixed

        从缓存获取项。若返回 ``null``，将调用回调并保存结果。无论哪种情况，均返回值。

    .. php:method:: save(string $key, $data[, int $ttl = 60])

        :param string $key: 缓存项名称
        :param mixed $data: 要保存的数据
        :param int $ttl: 存活时间（秒，默认 60）
        :returns: 成功返回 ``true``，失败返回 ``false``
        :rtype: bool

        将项保存到缓存存储。保存失败返回 ``false``。

        示例：

        .. literalinclude:: caching/004.php

    .. php:method:: delete($key): bool

        :param string $key: 缓存项名称
        :returns: 成功返回 ``true``，失败返回 ``false``
        :rtype: bool

        从缓存存储删除指定项。删除失败返回 false。

        示例：

        .. literalinclude:: caching/005.php

    .. php:method:: deleteMatching($pattern): integer

        :param string $pattern: 匹配缓存项键的 glob 风格模式
        :returns: 删除的项数
        :rtype: integer

        通过 glob 风格模式匹配键，从缓存存储批量删除多项。返回删除项的总数。

        .. important:: 此方法仅在 File、Redis 和 Predis 处理器中实现。
            由于限制，无法在 Memcached 和 Wincache 处理器中实现。

        示例：

        .. literalinclude:: caching/006.php

        关于 glob 风格语法的更多信息，请参见
        `Glob (programming) <https://en.wikipedia.org/wiki/Glob_(programming)#Syntax>`_。

    .. php:method:: increment($key[, $offset = 1]): mixed

        :param string $key: 缓存 ID
        :param int $offset: 增加步长/值
        :returns: 成功返回新值，失败返回 ``false``
        :rtype: mixed

        对原始存储值执行原子递增。

        示例：

        .. literalinclude:: caching/007.php

    .. php:method:: decrement($key[, $offset = 1]): mixed

        :param string $key: 缓存 ID
        :param int $offset: 减少步长/值
        :returns: 成功返回新值，失败返回 ``false``
        :rtype: mixed

        对原始存储值执行原子递减。

        示例：

        .. literalinclude:: caching/008.php

    .. php:method:: clean()

        :returns: 成功返回 ``true``，失败返回 ``false``
        :rtype: bool

        "清理"整个缓存。缓存文件删除失败返回 false。

        示例：

        .. literalinclude:: caching/009.php

    .. php:method:: getCacheInfo()

        :returns: 整个缓存数据库的信息
        :rtype: mixed

        返回整个缓存的信息。

        示例：

        .. literalinclude:: caching/010.php

        .. note:: 返回的信息和数据结构取决于所使用的适配器。

    .. php:method:: getMetadata(string $key)

        :param string $key: 缓存项名称
        :returns: 缓存项的元数据。缺失项返回 ``null``，或返回至少包含 "expire" 键（绝对 Unix 过期时间，永不过期则为 ``null``）的数组。
        :rtype: array|null

        返回缓存中指定项的详细信息。

        示例：

        .. literalinclude:: caching/011.php

        .. note:: 返回的信息和数据结构取决于所使用的适配器。部分适配器（File、Memcached、Wincache）
              对缺失项仍返回 ``false``。

    .. php:staticmethod:: validateKey(string $key, string $prefix)

        :param string $key: 候选缓存键
        :param string $prefix: 可选前缀
        :returns: 验证并添加前缀的键。若键超出驱动最大键长度，将进行哈希。
        :rtype: string

        处理器方法使用此方法验证键是否有效。非字符串、无效字符和空长度将抛出 ``InvalidArgumentException``。

        示例：

        .. literalinclude:: caching/012.php

*******
驱动
*******

基于文件的缓存
==================

需要缓存目录对应用可写。

谨慎使用，并确保对应用进行基准测试，因为磁盘 I/O 可能抵消缓存带来的性能提升。

Memcached 缓存
=================

Memcached 服务器可在缓存配置文件中指定。可用选项如下：

.. literalinclude:: caching/013.php

关于 Memcached 的更多信息，请参见
`https://www.php.net/memcached <https://www.php.net/memcached>`_。

WinCache 缓存
================

在 Windows 下，也可使用 WinCache 驱动。

关于 WinCache 的更多信息，请参见
`https://www.php.net/wincache <https://www.php.net/wincache>`_。

Redis 缓存
=============

Redis 是一个内存键值存储，可在 LRU 缓存模式下运行。
使用需 `Redis 服务器和 phpredis PHP 扩展 <https://github.com/phpredis/phpredis>`_。

连接 Redis 服务器的配置选项存储在缓存配置文件中。可用选项如下：

.. literalinclude:: caching/014.php

关于 Redis 的更多信息，请参见
`https://redis.io <https://redis.io>`_。

Predis 缓存
==============

Predis 是一个灵活且功能完整的 Redis 键值存储 PHP 客户端库。
使用前需先在项目根目录执行：

.. code-block:: console

    composer require predis/predis

关于 Redis 的更多信息，请参见
`https://github.com/nrk/predis <https://github.com/nrk/predis>`_。

Dummy 缓存
===========

这是一个始终"未命中"的缓存后端。不存储任何数据，
但可以在不支持所选缓存的环境中保留缓存代码。
