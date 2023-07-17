###################
服务器需求
###################

.. contents::
    :local:
    :depth: 2

***************************
PHP 及所需扩展
***************************

需要 `PHP <https://www.php.net/>`_ 7.4 或更高版本,并启用以下 PHP 扩展:

  - `intl <https://www.php.net/manual/en/intl.requirements.php>`_
  - `mbstring <https://www.php.net/manual/en/mbstring.requirements.php>`_
  - `json <https://www.php.net/manual/en/json.requirements.php>`_

***********************
可选的 PHP 扩展
***********************

您的服务器上应启用以下 PHP 扩展:

  - `mysqlnd <https://www.php.net/manual/en/mysqlnd.install.php>`_ (如果您使用 MySQL)
  - `curl <https://www.php.net/manual/en/curl.requirements.php>`_ (如果您使用 :doc:`CURLRequest </libraries/curlrequest>`)
  - `imagick <https://www.php.net/manual/en/imagick.requirements.php>`_ (如果您使用 :doc:`Image </libraries/images>` 类的 ImageMagickHandler)
  - `gd <https://www.php.net/manual/en/image.requirements.php>`_ (如果您使用 :doc:`Image </libraries/images>` 类的 GDHandler)
  - `simplexml <https://www.php.net/manual/en/simplexml.requirements.php>`_ (如果您格式化 XML)

当您使用缓存服务器时,需要启用以下 PHP 扩展:

  - `memcache <https://www.php.net/manual/en/memcache.requirements.php>`_ (如果您使用 Memcache 和 :doc:`Cache </libraries/caching>` 类的 MemcachedHandler)
  - `memcached <https://www.php.net/manual/en/memcached.requirements.php>`_ (如果您使用 Memcached 和 :doc:`Cache </libraries/caching>` 类的 MemcachedHandler)
  - `redis <https://github.com/phpredis/phpredis>`_ (如果您使用 :doc:`Cache </libraries/caching>` 类的 RedisHandler)

当您使用 PHPUnit 时,需要启用以下 PHP 扩展:

   - `dom <https://www.php.net/manual/en/dom.requirements.php>`_ (如果您使用 :doc:`TestResponse </testing/response>` 类)
   - `libxml <https://www.php.net/manual/en/libxml.requirements.php>`_ (如果您使用 :doc:`TestResponse </testing/response>` 类)
   - `xdebug <https://xdebug.org/docs/install>`_ (如果您使用 ``CIUnitTestCase::assertHeaderEmitted()``)

.. _requirements-supported-databases:

*******************
支持的数据库
*******************

大多数 Web 应用程序开发都需要数据库。
目前支持的数据库有:

  - MySQL,通过 ``MySQLi`` 驱动程序(仅版本 5.1 及以上)
  - PostgreSQL,通过 ``Postgre`` 驱动程序(仅版本 7.4 及以上)
  - SQLite3,通过 ``SQLite3`` 驱动程序
  - Microsoft SQL Server,通过 ``SQLSRV`` 驱动程序(仅版本 2005 及以上)
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
