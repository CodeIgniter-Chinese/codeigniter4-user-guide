###################
服务器安装要求
###################

需要7.2或更新版本的 `PHP <https://www.php.net/>`_ 同时需要安装 `*intl* 扩展 <https://www.php.net/manual/en/intl.requirements.php>`_ 。

在服务器同时需要启用以下PHP扩展:
``php-json``, ``php-mbstring``, ``php-mysqlnd``, ``php-xml``

为了能够使用 :doc:`CURLRequest </libraries/curlrequest>` ，你需要安装 `libcurl <https://www.php.net/manual/en/curl.requirements.php>`_ 。

对于大多数web应用程序来说，一个数据库是不可或缺的。以下是我们支持的数据库:

  - MySQL (5.1+) 通过 *MySQLi* 驱动使用
  - PostgreSQL 通过 *Postgre* 驱动使用
  - SQLite3 通过 *SQLite3* 驱动使用

CodeIgniter4 并没有转换或重写所有的驱动，下列显示了几个很棒的数据库与它们对应的驱动

  - MySQL (5.1+) 通过 *pdo* 驱动
  - Oracle 通过 *oci8* 和 *pdo* 驱动使用
  - PostgreSQL 通过 *pdo* driver
  - MS SQL 通过 *mssql*, *sqlsrv* (2005版本及以上使用)和 *pdo* 驱动使用
  - SQLite 通过 *sqlite* (version 2) 和 *pdo* 驱动使用
  - CUBRID 通过 *cubrid* 和 *pdo* 驱动使用
  - Interbase/Firebird 通过 *ibase* and *pdo* 驱动使用
  - ODBC 通过 *odbc* 和 *pdo* 驱动使用（你应该知道ODBC实际上只是一个抽象层）
