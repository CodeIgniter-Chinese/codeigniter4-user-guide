######################
数据库配置
######################

.. contents::
    :local:
    :depth: 3

.. note::
    请参阅 :ref:`requirements-supported-databases` 以获取当前支持的数据库驱动。

***********
配置文件
***********

CodeIgniter 有一个配置文件,可让你存储数据库连接值(用户名、密码、数据库名称等)。配置文件位于 **app/Config/Database.php**。你也可以在 **.env** 文件中设置数据库连接值。下面详细介绍。

设置默认数据库
========================

配置设置存储在一个类属性中,该属性是一个数组,原型如下:

.. literalinclude:: configuration/001.php

类属性的名称是连接名称,在连接时可以用作指定组名。

.. note:: SQLite3 数据库的默认位置是 **writable** 文件夹。如果要更改位置，则必须设置新文件夹（例如，'database' => WRITEPATH . 'db/database_name.db'）的完整路径。

DSN
---

某些数据库驱动程序（如 Postgre、OCI8）需要完整的 DSN（Data Source Name）字符串才能连接。但是，如果你没有为需要 DSN 字符串的驱动程序指定 DSN 字符串，CodeIgniter 将尝试使用其余提供的设置来构建它。

如果指定了 DSN,你应该使用 ``'DSN'`` 配置设置,就像你正在使用驱动程序的底层原生 PHP 扩展一样,如下所示:

.. literalinclude:: configuration/002.php
    :lines: 11-15

通用方式的 DSN
^^^^^^^^^^^^^^^^^^^^^^^

你还可以以通用方式(URL 格式)设置 DSN。在这种情况下,DSN 必须具有以下原型:

.. literalinclude:: configuration/003.php
    :lines: 11-14

要使用 DSN 字符串的通用版本覆盖默认配置值,请将配置变量作为查询字符串添加:

.. literalinclude:: configuration/004.php
    :lines: 11-15

.. literalinclude:: configuration/010.php
    :lines: 11-15

.. note:: 如果你提供了一个 DSN 字符串,但缺少配置字段中存在的一些有效设置(例如数据库字符集),CodeIgniter 将会追加它们。

故障转移
---------

你还可以针对主连接由于某些原因无法连接的情况指定故障转移。可以通过像这样为连接设置故障转移来指定故障转移:

.. literalinclude:: configuration/005.php

你可以指定任意多个故障转移。

设置多个数据库
==========================

你可以可选地存储多个连接值集。例如,如果你在单个安装下运行多个环境(开发、生产、测试等),则可以为每个环境设置一个连接组,然后根据需要在组之间切换。例如,要设置“测试”环境,你可以这样做:

.. literalinclude:: configuration/006.php

然后,要在全局范围内告诉系统使用该组,请设置配置文件中的此变量:

.. literalinclude:: configuration/007.php

.. note:: 名称 ``test`` 任意的。它可以是你想要的任何内容。默认情况下,我们已经将主连接的名称设置为 ``default``,但它也可以重命名为与项目更相关的名称。

自动更改数据库
================================

你可以修改配置文件以检测环境并自动更新 ``defaultGroup`` 值为正确的值,方法是在类构造函数中添加所需的逻辑:

.. literalinclude:: configuration/008.php

.. _database-config-with-env-file:

**************************
使用 .env 文件配置
**************************

你还可以在 **.env** 文件中保存你的配置值，其中包含当前服务器的数据库设置。你只需要输入与默认配置组中的设置不同的值。这些值应该遵循以下格式，其中 ``default`` 是组名::

    database.default.username = 'root';
    database.default.password = '';
    database.default.database = 'ci4';

但是你不能通过设置环境变量来添加新属性,也不能将标量值更改为数组。有关详细信息,请参阅 :ref:`env-var-replacements-for-data`。

因此,如果要对 MySQL 使用 SSL,你需要一个 hack。例如,在你的 **.env** 文件中将数组值设置为 JSON 字符串:

::

    database.default.encrypt = {"ssl_verify":true,"ssl_ca":"/var/www/html/BaltimoreCyberTrustRoot.crt.pem"}

并在 Config 类的构造函数中解码它:

.. literalinclude:: configuration/009.php

.. _database-config-explanation-of-values:

**********************
值的描述
**********************

================ ===========================================================================================================
 名称            描述
================ ===========================================================================================================
**DSN**          DSN 连接字符串(一体化配置序列)。
**hostname**     数据库服务器的主机名。通常是 'localhost'。
**username**     用于连接数据库的用户名。(``SQLite3`` 不使用此用户名)
**password**     用于连接数据库的密码。(``SQLite3`` 不使用此密码)
**database**     要连接的数据库名称。

                 .. note:: CodeIgniter 不支持在表名和列名中使用点 (``.``)。
                    从 v4.5.0 版本开始，支持带点的数据库名。
**DBDriver**     数据库驱动名称。驱动名称区分大小写。
                 你可以设置完全限定的类名以使用自定义驱动。
                 支持的驱动:``MySQLi``、``Postgre``、``SQLite3``、``SQLSRV`` 和 ``OCI8``。
**DBPrefix**     可选的表前缀,在运行时会添加到表名中 :doc:`查询构建器 <query_builder>` 查询。这允许多个 CodeIgniter 安装共享一个数据库。
**pConnect**     true/false (布尔值)- 是否使用持久连接。
**DBDebug**      true/false (布尔值)- 当发生数据库错误时是否抛出异常。
**charset**      与数据库通信使用的字符集。
**DBCollat**     （仅限 ``MySQLi``）与数据库通信时使用的字符集。
**swapPre**      一个默认的表前缀,应该与 ``DBPrefix`` 互换。这对于分布式应用程序很有用,在那里你可能运行手动编写的查询,并需要最终用户仍可自定义前缀。
**schema**       （仅限 ``Postgre`` 和 ``SQLSRV``）数据库模式，默认值因驱动而异。
**encrypt**      （仅限 ``MySQLi`` 和 ``SQLSRV``）是否使用加密连接。
                 有关 ``MySQLi`` 设置，请参见 :ref:`MySQLi encrypt <mysqli-encrypt>`。
                 ``SQLSRV`` 驱动程序接受 true/false。
**compress**     （仅限 ``MySQLi``）是否使用客户端压缩。
**strictOn**     （仅限 ``MySQLi``）true/false（布尔值）- 是否强制使用“严格模式”连接，有助于确保在开发应用程序时使用严格的 SQL。
**port**         数据库端口号 - 默认端口为空字符串 ``''`` (或使用 ``SQLSRV`` 动态端口)。
**foreignKeys**  （仅限 ``SQLite3``）true/false (布尔值)- 是否启用外键约束。

                 .. important:: SQLite3 外键约束默认关闭。
                     请参阅 `SQLite 文档 <https://www.sqlite.org/pragma.html#pragma_foreign_keys>`_。
                     要实施外键约束,请将此配置项设置为 true。
**busyTimeout**  （仅限 ``SQLite3``）毫秒（int）- 当表被锁定时，休眠指定时间。
**synchronous**  （仅限 ``SQLite3``）标志（int）- 控制事务期间 SQLite 将数据刷新到磁盘的严格程度。
                 使用 `null` 可保持默认设置。该功能自 v4.6.0 版本起可用。
**numberNative** （仅限 ``MySQLi``）true/false（布尔值）- 是否启用 MYSQLI_OPT_INT_AND_FLOAT_NATIVE。
**foundRows**    （仅限 ``MySQLi``）true/false（布尔值）- 是否启用 MYSQLI_CLIENT_FOUND_ROWS。
**dateFormat**   默认的日期/时间格式，如 PHP 的 `DateTime format`_。
                 * ``date``        - 日期格式
                 * ``datetime``    - 日期和时间格式
                 * ``datetime-ms`` - 带毫秒的日期和时间格式
                 * ``datetime-us`` - 带微秒的日期和时间格式
                 * ``time``        - 时间格式
                 这一功能可以从 v4.5.0 版本开始使用，你可以通过例如 ``$db->dateFormat['datetime']`` 来获取值。
                 当前，数据库驱动程序不会直接使用这些值，但 :ref:`Model <model-saving-dates>` 会使用它们。
================ ===========================================================================================================

.. _DateTime format: https://www.php.net/manual/en/datetime.format.php

.. note:: 根据你使用的数据库驱动程序(``MySQLi``、``Postgre`` 等),并非所有的值都是必需的。例如,在使用 ``SQLite3`` 时,你不需要提供用户名或密码,数据库名称将是数据库文件的路径。

MySQLi
======

hostname
--------

配置一个 Socket 连接
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

要通过文件系统套接字连接到 MySQL 服务器，应在 ``'hostname'`` 设置中指定套接字的路径。CodeIgniter 的 MySQLi 驱动程序会注意到这一点并正确配置连接。

.. literalinclude:: configuration/011.php
    :lines: 11-18

.. _mysqli-encrypt:

encrypt
-------

MySQLi 驱动程序接受包含以下选项的数组：

* ``ssl_key``    - 私钥文件的路径
* ``ssl_cert``   - 公钥证书文件的路径
* ``ssl_ca``     - 证书颁发机构文件的路径
* ``ssl_capath`` - 包含以 PEM 格式存储的可信 CA 证书的目录路径
* ``ssl_cipher`` - 允许用于加密的密码列表，用冒号（``:``）分隔
* ``ssl_verify`` - true/false (布尔值) - 是否验证服务器证书
