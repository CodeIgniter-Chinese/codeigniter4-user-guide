###################
服务器要求
###################

.. contents::
    :local:
    :depth: 2

***************************
PHP 与必需扩展
***************************

需要 `PHP <https://www.php.net/>`_ 8.2 或更高版本，并启用以下 PHP 扩展：

  - `intl <https://www.php.net/manual/zh/intl.requirements.php>`_
  - `mbstring <https://www.php.net/manual/zh/mbstring.installation.php>`_

.. warning::
    - PHP 7.4 已于 2022 年 11 月 28 日停止维护。
    - PHP 8.0 已于 2023 年 11 月 26 日停止维护。
    - PHP 8.1 已于 2025 年 12 月 31 日停止维护。
    - **如果仍在使用 8.2 以下的 PHP 版本，请立即升级。**
    - PHP 8.2 将于 2026 年 12 月 31 日停止维护。

.. note::
    - PHP 8.5 要求 CodeIgniter 4.7.0 或更高版本。
    - PHP 8.4 要求 CodeIgniter 4.6.0 或更高版本。
    - PHP 8.3 要求 CodeIgniter 4.4.4 或更高版本。
    - PHP 8.2 要求 CodeIgniter 4.2.11 或更高版本。
    - PHP 8.1 要求 CodeIgniter 4.1.6 或更高版本。
    - **请注意，官方仅维护最新版本。**

***********************
可选的 PHP 扩展
***********************

建议服务器启用以下 PHP 扩展：

  - `mysqlnd <https://www.php.net/manual/zh/mysqlnd.install.php>`_ （若使用 MySQL）
  - `curl <https://www.php.net/manual/zh/curl.requirements.php>`_ （若使用 :doc:`CURLRequest </libraries/curlrequest>`）
  - `imagick <https://www.php.net/manual/zh/imagick.requirements.php>`_ （若在 :doc:`图像处理 </libraries/images>` 类中使用 ImageMagickHandler）
  - `gd <https://www.php.net/manual/zh/image.requirements.php>`_ （若在 :doc:`图像处理 </libraries/images>` 类中使用 GDHandler）
  - `simplexml <https://www.php.net/manual/zh/simplexml.requirements.php>`_ （若需格式化 XML）

使用缓存服务器时，需要启用以下 PHP 扩展：

  - `memcache <https://www.php.net/manual/zh/memcache.requirements.php>`_ （若在 :doc:`缓存 </libraries/caching>` 类中通过 Memcache 使用 MemcachedHandler）
  - `memcached <https://www.php.net/manual/zh/memcached.requirements.php>`_ （若在 :doc:`缓存 </libraries/caching>` 类中通过 Memcached 使用 MemcachedHandler）
  - `redis <https://github.com/phpredis/phpredis>`_ （若在 :doc:`缓存 </libraries/caching>` 类中使用 RedisHandler）

使用 PHPUnit 时，需要启用以下 PHP 扩展：

   - `dom <https://www.php.net/manual/zh/dom.requirements.php>`_ （若使用 :doc:`TestResponse </testing/response>` 类）
   - `libxml <https://www.php.net/manual/zh/libxml.requirements.php>`_ （若使用 :doc:`TestResponse </testing/response>` 类）
   - `xdebug <https://xdebug.org/docs/install>`_ （若使用 ``CIUnitTestCase::assertHeaderEmitted()``）

.. _requirements-supported-databases:

*******************
支持的数据库
*******************

绝大多数 Web 应用开发都需要数据库。
目前支持的数据库包括：

  - MySQL，通过 ``MySQLi`` 驱动（仅限 5.1 及以上版本）
  - PostgreSQL，通过 ``Postgre`` 驱动（仅限 7.4 及以上版本）
  - SQLite3，通过 ``SQLite3`` 驱动
  - Microsoft SQL Server，通过 ``SQLSRV`` 驱动（仅限 2012 及以上版本）
  - Oracle Database，通过 ``OCI8`` 驱动（仅限 12.1 及以上版本）

并非所有驱动程序都已针对 CodeIgniter 4 完成迁移或重写。
以下列出了尚未完成的驱动：

  - MySQL（5.1+），通过 *pdo* 驱动
  - Oracle，通过 *pdo* 驱动
  - PostgreSQL，通过 *pdo* 驱动
  - MSSQL，通过 *pdo* 驱动
  - SQLite，通过 *sqlite* （版本 2）和 *pdo* 驱动
  - CUBRID，通过 *cubrid* 和 *pdo* 驱动
  - Interbase/Firebird，通过 *ibase* 和 *pdo* 驱动
  - ODBC，通过 *odbc* 和 *pdo* 驱动（注：ODBC 实际上是一个抽象层）
