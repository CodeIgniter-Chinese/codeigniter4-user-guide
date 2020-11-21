##############
缓存驱动器
##############

CodeIgniter 提供了几种最常用的快速缓存的封装，除了基于文件的缓存， 其他的缓存都需要对服务器进行特殊的配置，如果配置不正确，将会抛出 一个致命错误异常（Fatal Exception）。

.. contents::
    :local:
    :depth: 2

*************
示例代码
*************

以下示例代码展示控制器中的常见使用模式。

::

	if ( ! $foo = cache('foo'))
	{
		echo 'Saving to the cache!<br />';
		$foo = 'foobarbaz!';

		// Save into the cache for 5 minutes
		cache()->save('foo', $foo, 300);
	}

	echo $foo;

你可以通过 Services 类直接获取缓存引擎的实例::

    $cache = \Config\Services::cache();

    $foo = $cache->get('foo');

=====================
配置缓存
=====================

缓存引擎的所有配置都在 **application/Config/Cache.php** 文件中。在该文件中，以下项目可用。

**$handler**

$handler 处理器是启动引擎时应用作主处理程序。可用的名称有： dummy, file, memcached, redis, wincache。

**$backupHandler**

在第一选择 $hanlder 不可用的情况下，这是要加载的下一个缓存处理程序。这通常是 **文件** 处理程序，因为文件系统始终可用，但可能不适合更复杂的多服务器设置。

**$prefix**

如果您有多个应用程序使用相同的缓存存储，则可以在此处添加一个前缀到所有键名称的自定义前缀。

**$path**

 ``file`` 处理程序使用它来显示应该将缓存文件保存到哪里。

**$memcached**

这是使用 ``Memcache(d)`` 处理程序时将使用的一系列服务器。

**$redis**

使用 ``Redis`` 处理程序时要使用的Redis服务器的设置。

===============
类参考
===============

.. php:method:: isSupported()

	:returns:	如果支持，则为TRUE，否则为FALSE
	:rtype:	布尔值

.. php:method:: get($key)

	:param	string	$key: Cache 缓存项名称
	:returns:	项目值或FALSE如果没有找到
	:rtype:	mixed

	此方法将尝试从缓存存储中获取项目。如果该项目不存在，该方法将返回FALSE。

	Example::

		$foo = $cache->get('my_cached_item');

.. php:method:: save($key, $data[, $ttl = 60[, $raw = FALSE]])

	:param	string	$key: Cache item name
	:param	mixed	$data: the data to save
	:param	int	$ttl: Time To Live, in seconds (default 60)
	:param	bool	$raw: Whether to store the raw value
	:returns:	TRUE on success, FALSE on failure
	:rtype:	string

	此方法将会将项目保存到缓存存储。如果保存失败，该方法将返回FALSE。

	Example::

		$cache->save('cache_item_id', 'data_to_cache');

.. note:: 该 ``$raw`` 参数仅由 Memcache 使用，以便允许使用 ``increment()`` 和 ``decrement()``。

.. php:method:: delete($key)

	:param	string	$key: name of cached item
	:returns:	TRUE on success, FALSE on failure
	:rtype:	bool

	此方法将从缓存存储中删除特定项目。如果项目删除失败，该方法将返回FALSE。

	Example::

		$cache->delete('cache_item_id');

.. php:method:: increment($key[, $offset = 1])

	:param	string	$key: Cache ID
	:param	int	$offset: Step/value to add
	:returns:	New value on success, FALSE on failure
   	:rtype:	mixed

	Performs atomic incrementation of a raw stored value.
	执行原始存储值的原子增量

	Example::

		// 'iterator' has a value of 2

		$cache->increment('iterator'); // 'iterator' is now 3

		$cache->increment('iterator', 3); // 'iterator' is now 6

.. php:method:: decrement($key[, $offset = 1])

	:param	string	$key: Cache ID
	:param	int	$offset: Step/value to reduce by
	:returns:	New value on success, FALSE on failure
	:rtype:	mixed

	执行原始存储值的原子递减。

	Example::

		// 'iterator' has a value of 6

		$cache->decrement('iterator'); // 'iterator' is now 5

		$cache->decrement('iterator', 2); // 'iterator' is now 3

.. php:method:: clean()

	:returns:	TRUE on success, FALSE on failure
	:rtype:	bool

	此方法将 'clean' 整个缓存。如果缓存文件的删除失败，该方法将返回FALSE。
	Example::

			$cache->clean();

.. php:method:: cache_info()

	:returns:	Information on the entire cache database
	:rtype:	mixed

	此方法将返回整个缓存中的信息。

	Example::

		var_dump($cache->cache_info());

.. note:: 返回的信息和数据的结构取决于正在使用的适配器。

.. php:method:: getMetadata($key)

	:param	string	$key: Cache item name
	:returns:	Metadata for the cached item
	:rtype:	mixed

	此方法将返回缓存中特定项目的详细信息。

	Example::

		var_dump($cache->getMetadata('my_cached_item'));

.. note:: 返回的信息和数据的结构取决于正在使用的适配器。

*******
驱动器
*******

==================
基于文件的缓存
==================

和输出类的缓存不同的是，基于文件的缓存支持只缓存视图的某一部分。使用这个缓存时要注意， 确保对你的应用程序进行基准测试，因为当磁盘 I/O 频繁时可能对缓存有负面影响。

=================
Memcached 缓存
=================

可以在缓存配置文件中指定多个 Memcached 服务器。

关于 Memcached 的更多信息，请参阅 `http://php.net/memcached <http://php.net/memcached>`_。

================
WinCache 缓存
================

在 Windows 下，你还可以使用 WinCache 缓存。

关于 WinCache 的更多信息，请参阅 `http://php.net/wincache <http://php.net/wincache>`_。

=============
Redis 缓存
=============

Redis 是一个在内存中以键值形式存储数据的缓存，使用 LRU（最近最少使用算法）缓存模式， 要使用它，你需要先安装  `Redis 服务器和 phpredis 扩展 <https://github.com/phpredis/phpredis>`_。

连接 Redis 服务器的配置信息必须保存到 application/config/redis.php 文件中，可用参数有::

	$config['host'] = '127.0.0.1';
	$config['password'] = NULL;
	$config['port'] = 6379;
	$config['timeout'] = 0;

有关Redis的更多信息，请参阅 `http://redis.io <http://redis.io>`_。

=========================
虚拟缓存（Dummy Cache）
=========================

这是一个永远不会命中的缓存，它不存储数据，但是它允许你在当使用的缓存在你的环境下不被支持时， 仍然保留使用缓存的代码。
