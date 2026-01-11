###################
服务器要求
###################

.. contents::
    :local:
    :depth: 2

***************************
PHP 及必需扩展
***************************

需要 `PHP <https://www.php.net/>`_ 8.1 或更新版本，并启用以下 PHP 扩展：

  - `intl <https://www.php.net/manual/en/intl.requirements.php>`_
  - `mbstring <https://www.php.net/manual/en/mbstring.requirements.php>`_
  - `json <https://www.php.net/manual/en/json.requirements.php>`_

.. warning::
    - PHP 7.4 的生命周期已于 2022 年 11 月 28 日结束。
    - PHP 8.0 的生命周期已于 2023 年 11 月 26 日结束。
    - **如果仍在使用 PHP 7.4 或 8.0，请立即升级。**
    - PHP 8.1 的生命周期将于 2025 年 12 月 31 日结束。

.. note::
    - PHP 8.4 需要 CodeIgniter 4.6.0 或更高版本。
    - PHP 8.3 需要 CodeIgniter 4.4.4 或更高版本。
    - PHP 8.2 需要 CodeIgniter 4.2.11 或更高版本。
    - PHP 8.1 需要 CodeIgniter 4.1.6 或更高版本。
    - **请注意，我们只维护最新版本。**

***********************
可选的 PHP 扩展
***********************

服务器上建议启用以下 PHP 扩展：

  - `mysqlnd <https://www.php.net/manual/zh/mysqlnd.install.php>`_（如果使用 MySQL）
  - `curl <https://www.php.net/manual/zh/curl.requirements.php>`_（如果使用 :doc:`CURLRequest </libraries/curlrequest>`）
  - `imagick <https://www.php.net/manual/zh/imagick.requirements.php>`_（如果使用 :doc:`图像处理 </libraries/images>` 类的 ImageMagickHandler）
  - `gd <https://www.php.net/manual/zh/image.requirements.php>`_（如果使用 :doc:`图像处理 </libraries/images>` 类的 GDHandler）
  - `simplexml <https://www.php.net/manual/zh/simplexml.requirements.php>`_（如果需要格式化 XML）

当使用缓存服务器时，需要以下 PHP 扩展：

  - `memcache <https://www.php.net/manual/zh/memcache.requirements.php>`_（如果使用 :doc:`缓存 </libraries/caching>` 类的 MemcachedHandler 并搭配 Memcache）
  - `memcached <https://www.php.net/manual/zh/memcached.requirements.php>`_（如果使用 :doc:`缓存 </libraries/caching>` 类的 MemcachedHandler 并搭配 Memcached）
  - `redis <https://github.com/phpredis/phpredis>`_（如果使用 :doc:`缓存 </libraries/caching>` 类的 RedisHandler）

当使用 PHPUnit 时，需要以下 PHP 扩展：

   - `dom <https://www.php.net/manual/zh/dom.requirements.php>`_（如果使用 :doc:`TestResponse </testing/response>` 类）
   - `libxml <https://www.php.net/manual/zh/libxml.requirements.php>`_（如果使用 :doc:`TestResponse </testing/response>` 类）
   - `xdebug <https://xdebug.org/docs/install>`_（如果使用 ``CIUnitTestCase::assertHeaderEmitted()``）

.. _requirements-supported-databases:

*******************
支持的数据库
*******************

大多数 Web 应用程序都需要数据库。
当前支持的数据库包括：

  - 通过 ``MySQLi`` 驱动的 MySQL（仅支持 5.1 及以上版本）
  - 通过 ``Postgre`` 驱动的 PostgreSQL（仅支持 7.4 及以上版本）
  - 通过 ``SQLite3`` 驱动的 SQLite3
  - 通过 ``SQLSRV`` 驱动的 Microsoft SQL Server（仅支持 2012 及以上版本）
  - 通过 ``OCI8`` 驱动的 Oracle Database（仅支持 12.1 及以上版本）

并非所有驱动都已为 CodeIgniter 4 转换或重写完成。
以下列表列出了尚未完成的驱动：

  - 通过 *pdo* 驱动的 MySQL（5.1+）
  - 通过 *pdo* 驱动的 Oracle
  - 通过 *pdo* 驱动的 PostgreSQL
  - 通过 *pdo* 驱动的 MSSQL
  - 通过 *sqlite*（版本 2）和 *pdo* 驱动的 SQLite
  - 通过 *cubrid* 和 *pdo* 驱动的 CUBRID
  - 通过 *ibase* 和 *pdo* 驱动的 Interbase/Firebird
  - 通过 *odbc* 和 *pdo* 驱动的 ODBC（需要注意，ODBC 实际上是一个抽象层）
