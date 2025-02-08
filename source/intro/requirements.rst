###################
服务器要求
###################

.. contents::
    :local:
    :depth: 2

***************************
PHP 与必需扩展
***************************

需要 `PHP <https://www.php.net/>`_ 8.1 或更高版本，并启用以下 PHP 扩展：

  - `intl <https://www.php.net/manual/en/intl.requirements.php>`_
  - `mbstring <https://www.php.net/manual/en/mbstring.requirements.php>`_
  - `json <https://www.php.net/manual/en/json.requirements.php>`_

.. warning::
    - PHP 7.4 的生命周期结束日期是 2022 年 11 月 28 日。
    - PHP 8.0 的生命周期结束日期是 2023 年 11 月 26 日。
    - **如果你仍在使用 PHP 7.4 或 8.0，应该立即升级。**
    - PHP 8.1 的生命周期结束日期将是 2025 年 12 月 31 日。

.. note::
    - PHP 8.4 需要 CodeIgniter 4.6.0 或更高版本。
    - PHP 8.3 需要 CodeIgniter 4.4.4 或更高版本。
    - PHP 8.2 需要 CodeIgniter 4.2.11 或更高版本。
    - PHP 8.1 需要 CodeIgniter 4.1.6 或更高版本。
    - **请注意我们只维护最新版本。**

***********************
可选 PHP 扩展
***********************

建议在服务器上启用以下 PHP 扩展：

  - `mysqlnd <https://www.php.net/manual/en/mysqlnd.install.php>`_ (如果使用 MySQL)
  - `curl <https://www.php.net/manual/en/curl.requirements.php>`_ (如果使用 :doc:`CURLRequest </libraries/curlrequest>`)
  - `imagick <https://www.php.net/manual/en/imagick.requirements.php>`_ (如果使用 :doc:`Image </libraries/images>` 类的 ImageMagickHandler)
  - `gd <https://www.php.net/manual/en/image.requirements.php>`_ (如果使用 :doc:`Image </libraries/images>` 类的 GDHandler)
  - `simplexml <https://www.php.net/manual/en/simplexml.requirements.php>`_ (如果处理 XML 格式)

使用缓存服务器时需要以下 PHP 扩展：

  - `memcache <https://www.php.net/manual/en/memcache.requirements.php>`_ (如果使用 :doc:`Cache </libraries/caching>` 类的 MemcachedHandler 配合 Memcache)
  - `memcached <https://www.php.net/manual/en/memcached.requirements.php>`_ (如果使用 :doc:`Cache </libraries/caching>` 类的 MemcachedHandler 配合 Memcached)
  - `redis <https://github.com/phpredis/phpredis>`_ (如果使用 :doc:`Cache </libraries/caching>` 类的 RedisHandler)

使用 PHPUnit 时需要以下 PHP 扩展：

   - `dom <https://www.php.net/manual/en/dom.requirements.php>`_ (如果使用 :doc:`TestResponse </testing/response>` 类)
   - `libxml <https://www.php.net/manual/en/libxml.requirements.php>`_ (如果使用 :doc:`TestResponse </testing/response>` 类)
   - `xdebug <https://xdebug.org/docs/install>`_ (如果使用 ``CIUnitTestCase::assertHeaderEmitted()``)

.. _requirements-supported-databases:

*******************
支持的数据库
*******************

大多数 Web 应用程序需要数据库支持。当前支持的数据库包括：

  - MySQL（通过 ``MySQLi`` 驱动，仅支持 5.1 及以上版本）
  - PostgreSQL（通过 ``Postgre`` 驱动，仅支持 7.4 及以上版本）
  - SQLite3（通过 ``SQLite3`` 驱动）
  - Microsoft SQL Server（通过 ``SQLSRV`` 驱动，仅支持 2012 及以上版本）
  - Oracle Database（通过 ``OCI8`` 驱动，仅支持 12.1 及以上版本）

并非所有驱动都已为 CodeIgniter4 完成转换/重写。以下是尚未完成的驱动列表：

  - MySQL (5.1+) 通过 *pdo* 驱动
  - Oracle 通过 *pdo* 驱动
  - PostgreSQL 通过 *pdo* 驱动
  - MSSQL 通过 *pdo* 驱动
  - SQLite 通过 *sqlite* (版本 2) 和 *pdo* 驱动
  - CUBRID 通过 *cubrid* 和 *pdo* 驱动
  - Interbase/Firebird 通过 *ibase* 和 *pdo* 驱动
  - ODBC 通过 *odbc* 和 *pdo* 驱动（需注意 ODBC 实际上是一个抽象层）
