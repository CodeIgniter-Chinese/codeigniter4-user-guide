###################
服务器需求
###################

.. contents::
    :local:
    :depth: 2

***************************
PHP 及所需扩展
***************************

需要 `PHP <https://www.php.net/>`_ 8.1 或更高版本，并启用以下 PHP 扩展：

  - `intl <https://www.php.net/manual/en/intl.requirements.php>`_
  - `mbstring <https://www.php.net/manual/en/mbstring.requirements.php>`_
  - `json <https://www.php.net/manual/en/json.requirements.php>`_

.. warning:: PHP 7.4 的生命周期结束日期是 2022 年 11 月 28 日。如果你仍在使用 PHP 7.4，应立即升级。PHP 8.0 的生命周期结束日期将是 2023 年 11 月 26 日。

.. warning::
    - PHP 7.4 的生命周期结束日期是 2022 年 11 月 28 日。
    - PHP 8.0 的生命周期结束日期是 2023 年 11 月 26 日。
    - 如果你仍在使用 PHP 7.4 或 8.0，你应该立即升级。
    - PHP 8.1 的生命周期结束日期将是 2024 年 11 月 25 日。

***********************
可选的 PHP 扩展
***********************

你的服务器上应启用以下 PHP 扩展:

  - `mysqlnd <https://www.php.net/manual/en/mysqlnd.install.php>`_ (如果你使用 MySQL)
  - `curl <https://www.php.net/manual/en/curl.requirements.php>`_ (如果你使用 :doc:`CURLRequest </libraries/curlrequest>`)
  - `imagick <https://www.php.net/manual/en/imagick.requirements.php>`_ (如果你使用 :doc:`Image </libraries/images>` 类的 ImageMagickHandler)
  - `gd <https://www.php.net/manual/en/image.requirements.php>`_ (如果你使用 :doc:`Image </libraries/images>` 类的 GDHandler)
  - `simplexml <https://www.php.net/manual/en/simplexml.requirements.php>`_ (如果你格式化 XML)

当你使用缓存服务器时,需要启用以下 PHP 扩展:

  - `memcache <https://www.php.net/manual/en/memcache.requirements.php>`_ (如果你使用 Memcache 和 :doc:`Cache </libraries/caching>` 类的 MemcachedHandler)
  - `memcached <https://www.php.net/manual/en/memcached.requirements.php>`_ (如果你使用 Memcached 和 :doc:`Cache </libraries/caching>` 类的 MemcachedHandler)
  - `redis <https://github.com/phpredis/phpredis>`_ (如果你使用 :doc:`Cache </libraries/caching>` 类的 RedisHandler)

当你使用 PHPUnit 时,需要启用以下 PHP 扩展:

   - `dom <https://www.php.net/manual/en/dom.requirements.php>`_ (如果你使用 :doc:`TestResponse </testing/response>` 类)
   - `libxml <https://www.php.net/manual/en/libxml.requirements.php>`_ (如果你使用 :doc:`TestResponse </testing/response>` 类)
   - `xdebug <https://xdebug.org/docs/install>`_ (如果你使用 ``CIUnitTestCase::assertHeaderEmitted()``)

.. _requirements-supported-databases:

*******************
支持的数据库
*******************

大多数 Web 应用程序开发都需要数据库。
目前支持的数据库有:

  - MySQL,通过 ``MySQLi`` 驱动程序(仅版本 5.1 及以上)
  - PostgreSQL,通过 ``Postgre`` 驱动程序(仅版本 7.4 及以上)
  - SQLite3,通过 ``SQLite3`` 驱动程序
  - Microsoft SQL Server,通过 ``SQLSRV`` 驱动程序(仅版本 2012 及以上)
  - Oracle 数据库,通过 ``OCI8`` 驱动程序(仅版本 12.1 及以上)

并非所有驱动程序都已为 CodeIgniter4 转换/重写。
下面列出了未完成的驱动程序。

  - MySQL (5.1+) 通过 *pdo* 驱动程序
  - Oracle 通过 *pdo* 驱动程序
  - PostgreSQL 通过 *pdo* 驱动程序
  - MSSQL 通过 *pdo* 驱动程序
  - SQLite 通过 *sqlite* (2 版本)和 *pdo* 驱动程序
  - CUBRID 通过 *cubrid* 和 *pdo* 驱动程序
  - Interbase/Firebird 通过 *ibase* 和 *pdo* 驱动程序
  - ODBC 通过 *odbc* 和 *pdo* 驱动程序(应注意 ODBC 实际上是抽象层)
